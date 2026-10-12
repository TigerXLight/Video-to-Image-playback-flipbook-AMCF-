from __future__ import annotations

import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
SRC = PACKAGE / "src"
sys.path.insert(0, str(SRC))

from amcf_shared_package_model import write_demo_shared_package  # noqa: E402


def main() -> None:
    output_dir = PACKAGE / "output" / "amcf_shared_package_model"
    result = write_demo_shared_package(output_dir)
    report = result["validation_report"]
    print(
        json.dumps(
            {
                "ok": bool(report["final_passed"]),
                "output_folder": str(output_dir),
                "section_count": result["package"]["manifest"]["section_count"],
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "hardware_validation_claimed": report["claim_boundary_flags"]["hardware_validation_claimed"],
                "physical_level_5_claimed": report["claim_boundary_flags"]["physical_level_5_claimed"],
                "manufactured_player_claimed": report["claim_boundary_flags"]["manufactured_player_claimed"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
