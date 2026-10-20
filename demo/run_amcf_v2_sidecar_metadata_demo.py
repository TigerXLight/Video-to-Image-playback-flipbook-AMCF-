from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_v2_sidecar_metadata import build_demo_sidecar_archive, validate_sidecar_archive  # noqa: E402


RUN_NAME = "AMCF_V2_SIDECAR_METADATA_DEMO_V1"


def run_demo(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / "public_14j_sidecar_demo.amcfv2.zip"
    build_report = build_demo_sidecar_archive(archive_path, frame_count=4)
    validation_report = validate_sidecar_archive(archive_path)
    report = {
        "run_name": RUN_NAME,
        "archive_path": str(archive_path),
        "build_report": build_report,
        "validation_report": validation_report,
        "unsafe_acceptance_count": validation_report["unsafe_acceptance_count"],
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "generated_output_committed": False,
        "final_passed": bool(validation_report["final_passed"]),
    }
    (output_dir / "amcf_v2_sidecar_metadata_demo_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "AMCF_V2_SIDECAR_METADATA_DEMO_SUMMARY.md").write_text(
        "\n".join(
            [
                "# AMCF V2 Sidecar Metadata Demo Summary",
                "",
                f"- run_name: {RUN_NAME}",
                f"- final_passed: {str(report['final_passed']).lower()}",
                f"- frame_count: {validation_report['frame_count']}",
                f"- proxy_region_count: {validation_report['proxy_region_count']}",
                f"- unsafe_acceptance_count: {validation_report['unsafe_acceptance_count']}",
                "- hardware_validation_claimed: false",
                "- physical_level_5_claimed: false",
                "- manufactured_player_claimed: false",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return report


def main() -> int:
    report = run_demo(REPO_ROOT / "output" / "amcf_v2_sidecar_metadata_demo")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
