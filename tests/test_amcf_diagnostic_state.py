from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive  # noqa: E402
from amcf_diagnostic_state import (  # noqa: E402
    AMCF_DIAGNOSTIC_STATE_SCHEMA,
    diagnostic_state_summary,
    load_diagnostic_state_manifest,
    normalize_test02_tracks_manifest,
)
from amcf_quality_metrics import compare_ppm_frame_folders  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class AmcfDiagnosticStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_diagnostic_state_"))
        self.source = self.tmp / "source"
        generate_source_frames(self.source, frame_count=4, width=48, height=32, fps=4)
        self.source_manifest = self.source / "source_frames_manifest.json"
        self.raw_tracks = self.tmp / "tracks_manifest.json"
        frames = []
        for frame_index in range(4):
            frames.append(
                {
                    "frame_index": frame_index,
                    "pts_seconds": frame_index / 4.0,
                    "tracks": [
                        {
                            "track_id": "moving_component",
                            "parent_id": None,
                            "label": "Moving Component",
                            "visible_state": "visible",
                            "occluded_state": "none",
                            "confidence": 0.99,
                            "bbox": [8 + frame_index, 8, 16, 12],
                            "contours": [[[8 + frame_index, 8], [24 + frame_index, 8], [24 + frame_index, 20], [8 + frame_index, 20]]],
                            "component_update": True,
                            "update_reason": "motion",
                        }
                    ],
                }
            )
        self.raw_tracks.write_text(
            json.dumps(
                {
                    "schema": "amcf-test02-tracks-v1",
                    "fps": 4,
                    "source_size": [48, 32],
                    "display_size": [24, 16],
                    "frames": frames,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_test02_manifest_normalizes_without_promoting_proxy_claims(self) -> None:
        normalized = normalize_test02_tracks_manifest(self.raw_tracks)
        self.assertEqual(normalized["schema"], AMCF_DIAGNOSTIC_STATE_SCHEMA)
        self.assertEqual(normalized["profile"], "test02_track_mask_state")
        self.assertEqual(normalized["source"]["frame_count"], 4)
        self.assertEqual(normalized["frames"][0]["tracks"][0]["geometry_contract"]["kind"], "polygon_contours")
        self.assertFalse(normalized["claim_boundary"]["semantic_object_amcf_solved"])
        self.assertFalse(normalized["process_contracts"]["12b_classical_proxy"]["object_identity_verified"])
        self.assertEqual(diagnostic_state_summary(normalized)["contour_track_frame_rows"], 4)

    def test_diagnostic_component_events_close_exact_residuals(self) -> None:
        archive_path = self.tmp / "diagnostic_component.amcf.zip"
        result = build_component_event_archive(
            self.source_manifest,
            archive_path,
            prefer_webp=False,
            diagnostic_state_manifest_path=self.raw_tracks,
            use_diagnostic_components=True,
        )
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["diagnostic_state"]["used_for_component_event_selection"])
        self.assertGreater(result["diagnostic_event_accounting"]["track_event_count"], 0)
        self.assertGreater(result["diagnostic_event_accounting"]["exact_residual_event_count"], 0)
        self.assertEqual(result["diagnostic_event_accounting"]["logical_diagnostic_track_row_count"], 4)
        self.assertTrue(result["diagnostic_event_accounting"]["all_logical_track_rows_retained_in_embedded_state"])

        with zipfile.ZipFile(archive_path, "r") as archive:
            manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
            self.assertIn("diagnostics/diagnostic_state.json", archive.namelist())
            self.assertTrue(any(event["payload_format"] == "amcf_masked_rgb_v1" for event in manifest["events"]))
            self.assertTrue(any(event["component_id"] == "diagnostic_residual" for event in manifest["events"]))

        decoded = decode_component_event_archive(archive_path, self.tmp / "decoded")
        self.assertTrue(decoded["ok"], decoded)
        quality = compare_ppm_frame_folders(self.source / "frames", Path(decoded["decoded_frames_dir"]))
        self.assertTrue(quality["ok"], quality)
        self.assertEqual(decoded["diagnostic_state"]["profile"], "test02_track_mask_state")
        self.assertTrue(decoded["diagnostic_state"]["embedded_state_validated"])
        self.assertEqual(decoded["diagnostic_state"]["embedded_state_summary"]["profile"], "test02_track_mask_state")

    def test_diagnostic_source_frame_count_mismatch_fails_closed(self) -> None:
        mismatch = json.loads(self.raw_tracks.read_text(encoding="utf-8"))
        mismatch["frames"] = mismatch["frames"][:2]
        mismatch["frames"][0]["frame_index"] = 0
        mismatch["frames"][1]["frame_index"] = 1
        mismatch_path = self.tmp / "mismatch_tracks.json"
        mismatch_path.write_text(json.dumps(mismatch), encoding="utf-8")
        with self.assertRaises(ValueError):
            build_component_event_archive(
                self.source_manifest,
                self.tmp / "should_not_build.amcf.zip",
                prefer_webp=False,
                diagnostic_state_manifest_path=mismatch_path,
                use_diagnostic_components=True,
            )

    def test_loader_rejects_unknown_schema(self) -> None:
        bad = self.tmp / "bad.json"
        bad.write_text(json.dumps({"schema": "not-amcf"}), encoding="utf-8")
        with self.assertRaises(ValueError):
            load_diagnostic_state_manifest(bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
