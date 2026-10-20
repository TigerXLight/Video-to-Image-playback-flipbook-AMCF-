"""Verify a bounded local Test 14H archive without changing it."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_v2_14h_archive import decode_14h_archive  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    report, _frames = decode_14h_archive(args.archive)
    output = REPO_ROOT / "output" / "amcf_v2_14h_archive_decode"
    output.mkdir(parents=True, exist_ok=True)
    (output / "decode_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
