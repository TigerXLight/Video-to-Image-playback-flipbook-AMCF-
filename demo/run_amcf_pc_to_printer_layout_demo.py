from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_print_layout import write_print_layout_demo  # noqa: E402


def main() -> int:
    output_dir = REPO_ROOT / "output" / "amcf_pc_to_printer_layout"
    result = write_print_layout_demo(REPO_ROOT, output_dir)
    report = result["report"]
    print(
        json.dumps(
            {
                "ok": report["final_passed"],
                "output_folder": str(output_dir),
                "section_layout_count": report["section_layout_count"],
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "hardware_validation_claimed": report["claim_boundary_flags"]["hardware_validation_claimed"],
                "real_printer_driver_used": not report["no_hardware_printer_driver_used"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
