from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amcf_v0 import loader, toolchain


RUN_NAME = "AMCF_V0_PUBLIC_ARCHIVE_TOOLCHAIN_DEMO_V1"
OUTPUT_DIR = REPO_ROOT / "output" / "amcf_v0_public_archive_toolchain_demo"


def _write_demo_archive(path: Path) -> None:
    manifest = {
        "archive_schema_name": "AMCF v0 prototype archive",
        "archive_schema_version": "public-port-demo",
        "not_final_codec": True,
        "primary_viewer": "viewer/OPEN_FIRST_AMCF_04B_VIEWER.html",
        "primary_video": "media/original_vs_best_visual_baseline.mp4",
        "candidate_only_video": "media/candidate_only_best_visual_baseline.mp4",
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("viewer/OPEN_FIRST_AMCF_04B_VIEWER.html", "<!doctype html><title>AMCF v0 public demo</title>")
        z.writestr("viewer/OPEN_FIRST_AMCF_04B_README.md", "# AMCF v0 public demo\n")
        z.writestr("manifest/AMCF_04B_ARCHIVE_MANIFEST.json", json.dumps(manifest, indent=2))
        z.writestr("media/original_vs_best_visual_baseline.mp4", b"synthetic-video-placeholder")
        z.writestr("media/candidate_only_best_visual_baseline.mp4", b"synthetic-video-placeholder")
        z.writestr("docs/visual_gate_rules.md", "# Visual gate rules\n")


def build_demo_report() -> dict:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    archive = OUTPUT_DIR / "synthetic_public_v0.amcfv0.zip"
    extract_dir = OUTPUT_DIR / "extract"
    report_path = OUTPUT_DIR / "loader_validation_report.json"
    _write_demo_archive(archive)

    validation = loader.cmd_validate(
        type("Args", (), {"archive": str(archive), "out": str(extract_dir), "report": str(report_path)})()
    )
    component_manifest = OUTPUT_DIR / "component_manifest.json"
    component_manifest.write_text(
        json.dumps(
            {
                "component_schema_name": "AMCF v0 component stream",
                "component_schema_version": "public-port-demo",
                "source_baseline": "synthetic",
                "source_fps": 24,
                "source_frame_count": 2,
                "components": [{"component_id": "component_0001"}],
                "update_schedules": [],
                "mask_policy": {},
                "stream_policy": {},
                "compositor_policy": {},
                "visual_gate_policy": {},
                "limitations": ["synthetic demo fixture only"],
            }
        ),
        encoding="utf-8",
    )
    component_validation = toolchain.component_manifest_ok(component_manifest)
    final_passed = bool(validation["passed"] and component_validation["passed"])
    return {
        "run_name": RUN_NAME,
        "archive_path": str(archive),
        "validation_report_path": str(report_path),
        "component_manifest_path": str(component_manifest),
        "archive_validation_passed": validation["passed"],
        "component_manifest_validation_passed": component_validation["passed"],
        "unsafe_acceptance_count": 0,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "real_hardware_required": False,
        "final_passed": final_passed,
    }


def main() -> None:
    report = build_demo_report()
    output = OUTPUT_DIR / "amcf_v0_public_archive_toolchain_demo_report.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["final_passed"] else 1)


if __name__ == "__main__":
    main()

