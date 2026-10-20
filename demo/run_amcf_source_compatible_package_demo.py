from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_source_compatible_package import (  # noqa: E402
    build_source_compatible_package,
    materialize_native_archive,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or materialize an AMCF source-compatible package.")
    parser.add_argument("--source-video", type=Path, required=True)
    parser.add_argument("--canonical-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--materialize-native", action="store_true")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    package_path = args.output / "source_compatible.amcf.zip"
    build = build_source_compatible_package(
        args.source_video,
        args.canonical_archive,
        package_path,
    )
    report = {"build": build}
    if args.materialize_native:
        report["materialize"] = materialize_native_archive(
            package_path,
            args.output / "materialized_native.amcf.zip",
        )
    report_path = args.output / "source_compatible_package_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
