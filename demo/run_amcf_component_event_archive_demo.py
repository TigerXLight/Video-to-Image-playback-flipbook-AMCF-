from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "demo"))

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive, optional_dependency_status  # noqa: E402
from amcf_component_event_viewer import build_component_event_viewer  # noqa: E402
from amcf_quality_metrics import compare_ppm_frame_folders  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


RUN_NAME = "AMCF_LOCAL_MAIN_COMPONENT_EVENT_PARITY_V2"
OUTPUT_DIR = REPO_ROOT / "output" / "amcf_component_event_archive_demo"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def build_summary_markdown(report: dict) -> str:
    return "\n".join(
        [
            "# AMCF Component Event Archive Demo",
            "",
            f"Run name: `{RUN_NAME}`",
            "",
            "This is a software-only component-event archive parity demo derived from the local Main component archive direction.",
            "It does not claim hardware validation, physical Level 5 completion, manufactured-player completion, real printer integration, real scanner integration, or real player hardware.",
            "",
            "## Results",
            "",
            f"- final_passed: {str(report['final_passed']).lower()}",
            f"- component-event archive status: {report['component_event_archive_status']}",
            f"- frame count: {report['archive']['frame_count']}",
            f"- event count: {report['archive']['event_count']}",
            f"- payload format: {report['archive']['payload_format']}",
            f"- segmentation mode: {report['archive']['segmentation_mode']}",
            f"- viewer package: {report['viewer']['viewer_html']}",
            f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
            f"- hardware_validation_claimed: {str(report['claim_boundary']['hardware_validation_claimed']).lower()}",
            f"- physical_level_5_claimed: {str(report['claim_boundary']['physical_level_5_claimed']).lower()}",
            f"- manufactured_player_claimed: {str(report['claim_boundary']['manufactured_player_claimed']).lower()}",
            "",
            "Generated output is a demo artifact and is not hardware proof.",
            "",
        ]
    )


def run_demo(output_dir: Path = OUTPUT_DIR) -> dict:
    source_dir = output_dir / "source_frames"
    archive_path = output_dir / "component_event_archive.amcf.zip"
    decoded_dir = output_dir / "decoded"
    output_dir.mkdir(parents=True, exist_ok=True)

    generate_source_frames(source_dir, frame_count=6, width=64, height=40, fps=6)
    dependency_status = optional_dependency_status()
    segmentation_mode = "opencv_changed_region" if dependency_status["opencv_available"] else "changed_region"
    archive = build_component_event_archive(
        source_dir / "source_frames_manifest.json",
        archive_path,
        prefer_webp=True,
        segmentation_mode=segmentation_mode,
    )
    decoded = decode_component_event_archive(archive_path, decoded_dir)
    quality = compare_ppm_frame_folders(source_dir / "frames", decoded_dir / "decoded_frames")
    viewer = build_component_event_viewer(
        archive_report=archive,
        decoded_report=decoded,
        quality_report=quality,
        output_dir=output_dir / "viewer",
    )
    claim_boundary = archive["claim_boundary"]
    final_passed = (
        archive["ok"]
        and decoded["ok"]
        and quality["ok"]
        and viewer["ok"]
        and archive["unsafe_acceptance_count"] == 0
        and not claim_boundary["hardware_validation_claimed"]
        and not claim_boundary["physical_level_5_claimed"]
        and not claim_boundary["manufactured_player_claimed"]
    )
    report = {
        "run_name": RUN_NAME,
        "final_passed": final_passed,
        "component_event_archive_status": "IMPLEMENTED",
        "archive": archive,
        "decode": decoded,
        "quality": quality,
        "viewer": viewer,
        "claim_boundary": claim_boundary,
        "unsafe_acceptance_count": archive["unsafe_acceptance_count"],
        "generated_output_committed": False,
        "recommended_next_phase": "AMCF_LOCAL_MAIN_CLI_PARITY_V1",
    }
    write_json(output_dir / "component_event_archive_report.json", report)
    (output_dir / "COMPONENT_EVENT_ARCHIVE_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    return report


def main() -> None:
    print(json.dumps(run_demo(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
