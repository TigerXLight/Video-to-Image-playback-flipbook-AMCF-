from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amcf_local_tests_progression_integration_ledger import (  # noqa: E402
    build_progression_integration_ledger,
    write_progression_integration_outputs,
)


OUTPUT_DIR = REPO_ROOT / "output" / "amcf_local_tests_progression_integration_ledger"


def main() -> None:
    report = build_progression_integration_ledger(REPO_ROOT)
    outputs = write_progression_integration_outputs(report, OUTPUT_DIR)
    printable = {
        "run_name": report["run_name"],
        "summary_available": report["summary_available"],
        "progression_group_count": len(report["progression_groups"]),
        "diagnostic_gap_groups": report["diagnostic_gap_groups"],
        "recommended_next_phase": report["recommended_next_phase"],
        "v2_14f_python_comparison": report["v2_14f_python_comparison"],
        "unsafe_acceptance_count": report["unsafe_acceptance_count"],
        "hardware_validation_claimed": report["claim_boundary_flags"]["hardware_validation_claimed"],
        "physical_level_5_claimed": report["claim_boundary_flags"]["physical_level_5_claimed"],
        "manufactured_player_claimed": report["claim_boundary_flags"]["manufactured_player_claimed"],
        "outputs": outputs,
        "final_passed": report["final_passed"],
    }
    print(json.dumps(printable, indent=2, sort_keys=True))
    raise SystemExit(0 if report["final_passed"] else 1)


if __name__ == "__main__":
    main()

