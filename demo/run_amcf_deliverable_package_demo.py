from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "demo"))

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive  # noqa: E402
from amcf_component_event_viewer import build_component_event_viewer  # noqa: E402
from amcf_deliverable_package import build_deliverable_package  # noqa: E402
from amcf_quality_metrics import compare_ppm_frame_folders  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


OUTPUT_DIR = REPO_ROOT / "output" / "amcf_deliverable_package_demo"


def run_demo(output_dir: Path = OUTPUT_DIR) -> dict:
    source_dir = output_dir / "source"
    archive_path = output_dir / "component_event_archive.amcf.zip"
    decoded_dir = output_dir / "decoded"
    viewer_dir = output_dir / "viewer"
    deliverable_dir = output_dir / "deliverable_package"

    generate_source_frames(source_dir, frame_count=6, width=64, height=40, fps=6)
    manifest_path = source_dir / "source_frames_manifest.json"
    archive = build_component_event_archive(manifest_path, archive_path, segmentation_mode="changed_region")
    decoded = decode_component_event_archive(archive_path, decoded_dir)
    quality = compare_ppm_frame_folders(source_dir / "frames", Path(decoded["decoded_frames_dir"]))
    viewer = build_component_event_viewer(
        archive_report=archive,
        decoded_report=decoded,
        quality_report=quality,
        output_dir=viewer_dir,
    )
    deliverable = build_deliverable_package(
        archive_path=archive_path,
        source_frames_dir=source_dir / "frames",
        decoded_frames_dir=Path(decoded["decoded_frames_dir"]),
        quality_report=quality,
        viewer_dir=viewer_dir,
        output_dir=deliverable_dir,
        fps=6,
    )
    report = {
        "run_name": "AMCF_LOCAL_MAIN_DELIVERABLE_VIEWER_PARITY_V1",
        "ok": archive["ok"] and decoded["ok"] and quality["ok"] and viewer["ok"] and deliverable["ok"],
        "archive": archive,
        "decode": decoded,
        "quality": quality,
        "viewer": viewer,
        "deliverable": deliverable,
        "generated_output_committed": False,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "unsafe_acceptance_count": 0,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "deliverable_package_demo_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    print(json.dumps(run_demo(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
