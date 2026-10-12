from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_software_io_fixtures import write_fixture_report  # noqa: E402


def main() -> int:
    output_dir = REPO_ROOT / "output" / "amcf_software_io_fixtures"
    report = write_fixture_report(REPO_ROOT, output_dir)
    print(
        json.dumps(
            {
                "ok": report["final_passed"],
                "output_folder": str(output_dir),
                "fixture_version": report["fixture_version"],
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "hardware_validation_claimed": report["claim_boundary_flags"]["hardware_validation_claimed"],
                "physical_level_5_claimed": report["claim_boundary_flags"]["physical_level_5_claimed"],
                "manufactured_player_claimed": report["claim_boundary_flags"]["manufactured_player_claimed"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
