from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "demo"))

from amcf_cli import main as cli_main  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


OUTPUT_DIR = REPO_ROOT / "output" / "amcf_cli_workflow_demo"


def run_demo(output_dir: Path = OUTPUT_DIR) -> dict:
    source_dir = output_dir / "source"
    package_dir = output_dir / "encode"
    component_dir = output_dir / "component"
    decoded_dir = output_dir / "decode"
    print_dir = output_dir / "print_plan"
    generate_source_frames(source_dir, frame_count=4, width=48, height=32, fps=4)
    manifest = source_dir / "source_frames_manifest.json"
    statuses = [
        cli_main(["status"]),
        cli_main(["encode", "--input-frames-manifest", str(manifest), "--output", str(package_dir)]),
        cli_main(["component-archive", "--input-frames-manifest", str(manifest), "--output", str(component_dir)]),
        cli_main(["decode", "--input", str(package_dir / "package.amcf.zip"), "--output", str(decoded_dir)]),
        cli_main(["print-plan", "--input", str(package_dir / "package.amcf.zip"), "--output", str(print_dir)]),
    ]
    report = {
        "ok": all(code == 0 for code in statuses),
        "command_exit_codes": statuses,
        "output_folder": str(output_dir),
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "unsafe_acceptance_count": 0,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "cli_workflow_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    print(json.dumps(run_demo(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
