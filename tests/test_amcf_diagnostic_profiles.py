from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from amcf_diagnostic_profiles import (  # noqa: E402
    default_roi_profile,
    diff_panel,
    flow_magnitude_heatmap,
    proxy_motion_audit,
    render_12b_water_object_candidate_video,
    render_03m_motion_truth_family,
    roi_motion_audit,
    _normalize_proxy_label,
    _proxy_color,
    waterfall_03m_zones,
)


try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


@unittest.skipUnless(cv2 is not None and np is not None, "optional OpenCV/NumPy unavailable")
class DiagnosticProfileTests(unittest.TestCase):
    def test_03m_profile_has_the_historical_seven_zones(self):
        zones = waterfall_03m_zones()
        self.assertEqual(len(zones), 7)
        self.assertEqual(zones[0].name, "waterfall_main_zone")
        self.assertEqual(zones[-1].name, "background_rock_or_static_scene_zone")
        self.assertEqual(zones[0].bbox, (250, 20, 115, 230))

    def test_03m_profile_scales_zones_without_changing_identity(self):
        zones = waterfall_03m_zones(1280, 640)
        self.assertEqual(zones[0].name, "waterfall_main_zone")
        self.assertEqual(zones[0].bbox, (500, 40, 230, 460))

    def test_03m_family_renders_all_historical_diagnostic_views(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "source.mp4"
            writer = cv2.VideoWriter(str(source), cv2.VideoWriter_fourcc(*"mp4v"), 12.0, (64, 32))
            for index in range(3):
                frame = np.zeros((32, 64, 3), dtype=np.uint8)
                frame[:, :, 1] = 40 + index * 20
                frame[8:16, 10 + index * 3 : 18 + index * 3] = (255, 255, 255)
                writer.write(frame)
            writer.release()
            report = render_03m_motion_truth_family(source, temp / "family", max_frames=3)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["frame_count"], 3)
            self.assertEqual(
                set(report["output_videos"]),
                {
                    "original_reference",
                    "raw_screen_motion",
                    "camera_compensated_residual",
                    "residual_motion_mask",
                    "zone_motion_overlay",
                    "component_coverage_overlay",
                    "camera_motion_vectors",
                    "missing_motion_regions",
                    "original_vs_motion_truth",
                },
            )
            self.assertTrue(all(Path(path).exists() for path in report["output_videos"].values()))

    def test_08e_heat_contract_is_deterministic_and_colored(self):
        rng = np.random.default_rng(19)
        previous = rng.integers(0, 255, (64, 96, 3), dtype=np.uint8)
        current = previous.copy()
        current[20:35, 40:55] = 255
        first = flow_magnitude_heatmap(previous, current)
        second = flow_magnitude_heatmap(previous, current)
        self.assertEqual(first.shape, current.shape)
        self.assertTrue(np.array_equal(first, second))
        self.assertGreater(int(np.count_nonzero(first)), 0)

    def test_diff_panel_keeps_shape_and_bounded_values(self):
        previous = np.zeros((8, 10, 3), dtype=np.uint8)
        current = np.full_like(previous, 40)
        result = diff_panel(previous, current, scale=8)
        self.assertEqual(result.shape, previous.shape)
        self.assertEqual(int(result.max()), 255)

    def test_proxy_taxonomy_normalizes_historical_prefixes(self):
        self.assertEqual(_normalize_proxy_label("proxy_person_or_moving_object"), "person_or_moving_object")
        self.assertEqual(_normalize_proxy_label("calibrated_water_or_fluid_motion"), "water_or_fluid_motion")

    def test_12b_proxy_palette_preserves_green_object_and_yellow_uncertain_layers(self):
        self.assertEqual(_proxy_color("proxy_person_or_moving_object", style="12B"), (0, 255, 0))
        self.assertEqual(_proxy_color("proxy_uncertain", style="12B"), (0, 255, 255))
        self.assertEqual(_proxy_color("proxy_person_or_moving_object"), (0, 255, 255))

    def test_12b_candidate_renderer_keeps_proposals_separate_from_tracks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "source.mp4"
            writer = cv2.VideoWriter(str(source), cv2.VideoWriter_fourcc(*"mp4v"), 10.0, (64, 32))
            for _ in range(2):
                writer.write(np.zeros((32, 64, 3), dtype=np.uint8))
            writer.release()
            proposals = temp / "proposals.json"
            proposals.write_text(
                '[{"frame_index": 0, "bbox": [4, 4, 8, 8], "preliminary_label": "person_or_moving_object_candidate"}, '
                '{"frame_index": 0, "bbox": [20, 4, 8, 8], "preliminary_label": "uncertain_motion_region"}]',
                encoding="utf-8",
            )
            tracks = temp / "tracks.json"
            tracks.write_text(
                '[{"track_id": "track_1", "label": "proxy_person_or_moving_object", '
                '"frame_start": 1, "frame_end": 1, "bboxes": [[4, 4, 8, 8]]}]',
                encoding="utf-8",
            )
            report = render_12b_water_object_candidate_video(source, proposals, tracks, temp / "out.mp4", max_frames=2)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["rendered_candidate_count"], 1)
            self.assertEqual(report["track_count"], 1)

    def test_proxy_motion_audit_distinguishes_leftward_candidates_from_reviewed_objects(self):
        tracks = [
            {
                "track_id": "candidate_left",
                "label": "proxy_person_or_moving_object",
                "frame_start": 1,
                "frame_end": 3,
                "bboxes": [[20, 10, 5, 5], [15, 10, 5, 5], [10, 10, 5, 5]],
            },
            {
                "reviewed_track_id": "confirmed_static",
                "final_label": "person_or_moving_object",
                "frame_start": 1,
                "frame_end": 1,
                "bboxes": [[30, 10, 5, 5]],
            },
        ]
        audit = proxy_motion_audit(tracks)
        self.assertEqual(audit["direction_counts"]["leftward"], 1)
        self.assertEqual(audit["reviewed_person_or_moving_object_count"], 1)
        self.assertFalse(audit["right_to_left_person_behavior_proven"])
        self.assertTrue(audit["semantic_correctness_proven"] is False)

    def test_10ab_roi_profiles_preserve_historical_names(self):
        third = default_roi_profile("third-water", 640, 360)
        fourth = default_roi_profile("fourth-people", 640, 360)
        self.assertEqual(set(third), {"center_water", "left_detail", "right_detail", "bottom_texture", "whole_frame"})
        self.assertEqual(
            set(fourth),
            {"center_people_or_motion", "left_detail", "right_detail", "static_reference", "whole_frame"},
        )

    def test_10ab_roi_motion_audit_matches_motion_ratio_contract(self):
        truth = [np.zeros((16, 16, 3), dtype=np.uint8) for _ in range(3)]
        selected = [frame.copy() for frame in truth]
        truth[1][4:8, 4:8] = 20
        truth[2][4:8, 4:8] = 40
        selected[1][4:8, 4:8] = 20
        selected[2][4:8, 4:8] = 40
        audit = roi_motion_audit(truth, selected, {"whole_frame": (0, 0, 16, 16)})
        self.assertEqual(audit["status"], "PASS")
        self.assertAlmostEqual(audit["roi_motion"]["whole_frame"]["selected_truth_ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()
