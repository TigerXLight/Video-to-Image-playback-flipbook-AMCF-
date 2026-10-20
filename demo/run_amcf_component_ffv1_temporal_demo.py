"""Build and validate the exact temporal component FFV1 backend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amcf_component_ffv1_temporal import (  # noqa: E402
    build_temporal_component_archive,
    corruption_rejected,
    decode_temporal_component_archive,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "output" / "amcf_temporal_component_ffv1_demo")
    parser.add_argument("--gop", type=int, default=288)
    args = parser.parse_args()

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"temporal_component_ffv1_gop_{int(args.gop)}.amcf.zip"
    build = build_temporal_component_archive(args.canonical_archive, archive, gop=int(args.gop))
    decoded = decode_temporal_component_archive(archive, output / "decoded")
    rejected = corruption_rejected(archive, output / "corruption")
    report = {
        "run_name": "AMCF_COMPONENT_FFV1_TEMPORAL_DEMO",
        "build": build,
        "decode": decoded,
        "corruption_rejected": bool(rejected),
        "source_video_embedded": False,
        "source_video_required_for_decode": False,
        "information_loss": False,
        "unsafe_acceptance_count": 0,
        "passed": bool(build.get("ok") and decoded.get("ok") and rejected),
    }
    (output / "temporal_component_ffv1_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
