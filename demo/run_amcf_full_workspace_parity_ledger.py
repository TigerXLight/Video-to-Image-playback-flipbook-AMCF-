from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amcf_full_workspace_parity_ledger import build_full_workspace_parity_ledger, write_full_workspace_parity_outputs


OUTPUT_DIR = REPO_ROOT / "output" / "amcf_full_workspace_parity_ledger"


def main() -> None:
    report = build_full_workspace_parity_ledger(REPO_ROOT)
    outputs = write_full_workspace_parity_outputs(report, OUTPUT_DIR)
    printable = {
        "run_name": report["run_name"],
        "file_count": report["file_count"],
        "inspect_priority_count": report["inspect_priority_count"],
        "classification_counts": report["classification_counts"],
        "outputs": outputs,
        "unsafe_acceptance_count": report["unsafe_acceptance_count"],
        "hardware_validation_claimed": report["claim_boundary_flags"]["hardware_validation_claimed"],
        "physical_level_5_claimed": report["claim_boundary_flags"]["physical_level_5_claimed"],
        "manufactured_player_claimed": report["claim_boundary_flags"]["manufactured_player_claimed"],
        "final_passed": report["final_passed"],
    }
    print(json.dumps(printable, indent=2, sort_keys=True))
    raise SystemExit(0 if report["final_passed"] else 1)


if __name__ == "__main__":
    main()

