from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "demo"))

from amcf_optical_flow_tracking import build_optical_flow_track_report, optical_flow_dependency_status  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


OUTPUT_DIR = REPO_ROOT / "output" / "amcf_optical_flow_tracking_demo"


def run_demo(output_dir: Path = OUTPUT_DIR) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_dir = output_dir / "source_frames"
    generate_source_frames(source_dir, frame_count=6, width=64, height=40, fps=6)
    status = optical_flow_dependency_status()
    if not status["opencv_available"] or not status["numpy_available"]:
        report = {
            "ok": False,
            "skipped": True,
            "reason": "OpenCV/numpy are unavailable",
            "dependency_status": status,
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "unsafe_acceptance_count": 0,
        }
    else:
        flow = build_optical_flow_track_report(source_dir / "source_frames_manifest.json", output_dir)
        report = {
            "ok": flow["ok"],
            "skipped": False,
            "frame_count": flow["frame_count"],
            "track_count": flow["track_count"],
            "dependency_status": flow["dependency_status"],
            "hardware_validation_claimed": flow["claim_boundary"]["hardware_validation_claimed"],
            "physical_level_5_claimed": flow["claim_boundary"]["physical_level_5_claimed"],
            "manufactured_player_claimed": flow["claim_boundary"]["manufactured_player_claimed"],
            "unsafe_acceptance_count": flow["unsafe_acceptance_count"],
        }
    (output_dir / "OPTICAL_FLOW_TRACKING_SUMMARY.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    print(json.dumps(run_demo(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
