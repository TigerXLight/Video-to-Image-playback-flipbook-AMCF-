from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_cross_corridor_roundtrip import write_cross_corridor_roundtrip_demo  # noqa: E402


def main() -> int:
    output_dir = REPO_ROOT / "output" / "amcf_cross_corridor_roundtrip"
    result = write_cross_corridor_roundtrip_demo(REPO_ROOT, output_dir)
    report = result["roundtrip_report"]
    print(
        json.dumps(
            {
                "ok": report["final_passed"],
                "output_folder": str(output_dir),
                "section_count": report["section_count"],
                "recovered_section_count": report["recovered_section_count"],
                "command_count": report["command_count"],
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
