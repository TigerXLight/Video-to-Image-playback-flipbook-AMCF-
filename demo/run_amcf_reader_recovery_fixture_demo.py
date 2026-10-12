from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_reader_recovery import write_reader_recovery_demo  # noqa: E402


def main() -> int:
    output_dir = REPO_ROOT / "output" / "amcf_reader_recovery_fixture"
    result = write_reader_recovery_demo(REPO_ROOT, output_dir)
    report = result["report"]
    print(
        json.dumps(
            {
                "ok": report["final_passed"],
                "output_folder": str(output_dir),
                "recovered_sections": len(report["recovered_sections"]),
                "diagnostic_requests": len(report["diagnostic_requests"]),
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "scanner_api_used": report["scanner_api_used"],
                "image_processing_used": report["image_processing_used"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
