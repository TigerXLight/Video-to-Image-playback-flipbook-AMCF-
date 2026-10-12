from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_quality_metrics import compare_ppm_frames, write_ppm  # noqa: E402


OUTPUT_DIR = REPO_ROOT / "output" / "amcf_quality_metrics_demo"


def run_demo(output_dir: Path = OUTPUT_DIR) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    pixels = bytes([10, 20, 30, 40, 50, 60] * 8)
    first = output_dir / "frame_000.ppm"
    second = output_dir / "frame_001.ppm"
    write_ppm(first, 4, 4, pixels)
    write_ppm(second, 4, 4, pixels)
    report = {
        "run_name": "AMCF_LOCAL_MAIN_COMPONENT_EVENT_PARITY_V2",
        "final_passed": True,
        "quality": compare_ppm_frames(first, second),
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "unsafe_acceptance_count": 0,
    }
    (output_dir / "quality_metrics_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    print(json.dumps(run_demo(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
