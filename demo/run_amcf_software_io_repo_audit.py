from __future__ import annotations

import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
SRC = PACKAGE / "src"
sys.path.insert(0, str(SRC))

from amcf_software_io_repo_audit import RUN_NAME, write_audit_outputs  # noqa: E402


def main() -> None:
    output_dir = PACKAGE / "output" / "amcf_software_io_repo_audit"
    report = write_audit_outputs(output_dir, PACKAGE)
    print(
        json.dumps(
            {
                "ok": bool(report["final_passed"]),
                "run_name": RUN_NAME,
                "output_folder": str(output_dir),
                "branch": report["branch"],
                "head_commit": report["head_commit"],
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "hardware_validation_claimed": report["claim_boundary_flags"]["hardware_validation_claimed"],
                "physical_level_5_claimed": report["claim_boundary_flags"]["physical_level_5_claimed"],
                "manufactured_player_claimed": report["claim_boundary_flags"]["manufactured_player_claimed"],
                "generated_output_committed": report["generated_output_status"]["generated_output_committed"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
