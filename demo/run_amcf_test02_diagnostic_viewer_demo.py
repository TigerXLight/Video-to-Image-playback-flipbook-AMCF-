from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_test02_diagnostic_viewer import build_test02_diagnostic_viewer  # noqa: E402


RUN_NAME = "AMCF_TEST02_DIAGNOSTIC_VIEWER_PARITY_PORT_V1"
OUTPUT_DIR = REPO_ROOT / "output" / "amcf_test02_diagnostic_viewer"


def synthetic_tracks_manifest() -> dict:
    return {
        "schema": "amcf-test02-tracks-v1",
        "fps": 24.0,
        "source_size": [384, 192],
        "display_size": [96, 48],
        "frames": [
            {
                "frame_index": 0,
                "pts_seconds": 0.0,
                "tracks": [
                    {
                        "track_id": "WATERFALL_COLUMN",
                        "parent_id": None,
                        "label": "Waterfall Column",
                        "confidence": 0.92,
                        "component_update": True,
                        "update_reason": "initial_state",
                        "motion_median_px_s": 0.0,
                        "motion_p95_px_s": 0.0,
                        "color_bgr": [0, 220, 255],
                        "contours": [[[140, 32], [184, 32], [184, 188], [140, 188]]],
                    },
                    {
                        "track_id": "MIST_SPRAY",
                        "parent_id": "WATERFALL_COLUMN",
                        "label": "Mist Spray",
                        "confidence": 0.88,
                        "component_update": True,
                        "update_reason": "initial_state",
                        "motion_median_px_s": 0.0,
                        "motion_p95_px_s": 0.0,
                        "color_bgr": [230, 160, 255],
                        "contours": [[[92, 36], [260, 36], [260, 88], [92, 88]]],
                    },
                ],
            },
            {
                "frame_index": 1,
                "pts_seconds": 1.0 / 24.0,
                "tracks": [
                    {
                        "track_id": "WATERFALL_COLUMN",
                        "parent_id": None,
                        "label": "Waterfall Column",
                        "confidence": 0.98,
                        "component_update": False,
                        "update_reason": "held_state",
                        "motion_median_px_s": 122.5,
                        "motion_p95_px_s": 220.25,
                        "color_bgr": [0, 220, 255],
                        "contours": [[[142, 34], [186, 34], [186, 188], [142, 188]]],
                    },
                    {
                        "track_id": "MIST_SPRAY",
                        "parent_id": "WATERFALL_COLUMN",
                        "label": "Mist Spray",
                        "confidence": 0.96,
                        "component_update": False,
                        "update_reason": "held_state",
                        "motion_median_px_s": 4.0,
                        "motion_p95_px_s": 9.0,
                        "color_bgr": [230, 160, 255],
                        "contours": [[[96, 38], [262, 38], [262, 90], [96, 90]]],
                    },
                ],
            },
            {
                "frame_index": 2,
                "pts_seconds": 2.0 / 24.0,
                "tracks": [
                    {
                        "track_id": "WATERFALL_COLUMN",
                        "parent_id": None,
                        "label": "Waterfall Column",
                        "confidence": 0.98,
                        "component_update": True,
                        "update_reason": "motion",
                        "motion_median_px_s": 128.0,
                        "motion_p95_px_s": 240.0,
                        "color_bgr": [0, 220, 255],
                        "contours": [[[144, 36], [188, 36], [188, 188], [144, 188]]],
                    },
                    {
                        "track_id": "MIST_SPRAY",
                        "parent_id": "WATERFALL_COLUMN",
                        "label": "Mist Spray",
                        "confidence": 0.94,
                        "component_update": False,
                        "update_reason": "held_state",
                        "motion_median_px_s": 4.5,
                        "motion_p95_px_s": 10.0,
                        "color_bgr": [230, 160, 255],
                        "contours": [[[98, 40], [264, 40], [264, 92], [98, 92]]],
                    },
                ],
            },
        ],
    }


def run_demo(output_dir: Path = OUTPUT_DIR) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "source_tracks_manifest.json"
    manifest_path.write_text(json.dumps(synthetic_tracks_manifest(), indent=2, sort_keys=True), encoding="utf-8")
    viewer = build_test02_diagnostic_viewer(tracks_manifest_path=manifest_path, output_dir=output_dir / "viewer")
    report = {
        "run_name": RUN_NAME,
        "final_passed": bool(
            viewer["ok"]
            and viewer["track_count"] == 2
            and viewer["has_parent_child_taxonomy"]
            and viewer["has_motion_metrics"]
            and viewer["unsafe_acceptance_count"] == 0
            and not viewer["claim_boundary"]["hardware_validation_claimed"]
        ),
        "viewer": viewer,
        "generated_output_committed": False,
        "recommended_next_phase": "AMCF_TESTS_NEWEST_TO_OLDEST_DEEP_REVIEW_CONTINUE_V1",
    }
    (output_dir / "test02_diagnostic_viewer_demo_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    report = run_demo()
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["final_passed"] else 1)


if __name__ == "__main__":
    main()
