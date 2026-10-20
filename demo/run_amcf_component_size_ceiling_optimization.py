"""Run the full-resolution component archive size/quality search."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


MAIN_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = MAIN_ROOT.parent
sys.path.insert(0, str(MAIN_ROOT / "src"))

from amcf_component_size_ceiling import optimize_component_archive  # noqa: E402


DEFAULT_SOURCE_MANIFEST = (
    WORKSPACE_ROOT
    / "Tests/Test AMCF_MAIN_PUBLIC_MEDIA_ACCEPTANCE/20261015_131327/local_main/amcf_encode/extracted_source/source_frames_manifest.json"
)
DEFAULT_OUTPUT = MAIN_ROOT / "output" / "amcf_component_size_ceiling_optimization"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = optimize_component_archive(args.source_manifest, args.output)
    (args.output / "component_size_ceiling_optimization_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# AMCF Component Size-Ceiling Optimization",
        "",
        f"- final_passed: `{str(report['final_passed']).lower()}`",
        f"- source size ceiling: `{report['source_size_ceiling_bytes']}` bytes",
        f"- unsafe_acceptance_count: `{report['unsafe_acceptance_count']}`",
        "",
        "## Candidates",
        "",
        "| quality | archive bytes | under ceiling | visual pass | mean MAE | mean SSIM |",
        "| ---: | ---: | :---: | :---: | ---: | ---: |",
    ]
    for item in report["candidates"]:
        visual = item["visual"]
        lines.append(
            f"| {item['quality']} | {item['archive_bytes']} | {str(item['under_source_size_ceiling']).lower()} | "
            f"{str(visual['passed']).lower()} | {visual['mean_mae']} | {visual['mean_ssim']} |"
        )
    lines += [
        "",
        "The optimizer never treats a size-only candidate as accepted; the selected candidate must satisfy both the byte ceiling and visual thresholds.",
        "",
        "Generated archives and decoded frames remain under `Main/output/` and are not source or release artifacts.",
    ]
    (args.output / "COMPONENT_SIZE_CEILING_OPTIMIZATION_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
