from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_local_main_strict_parity import RUN_NAME, build_strict_parity_report  # noqa: E402


OUTPUT_DIR = REPO_ROOT / "output" / "amcf_local_main_strict_parity_proof"


def run_demo(*, frames: int = 4, output_dir: Path = OUTPUT_DIR) -> dict:
    return build_strict_parity_report(REPO_ROOT, output_dir, frames=frames, run_outputs=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run strict local Main vs public AMCF parity proof.")
    parser.add_argument("--frames", type=int, default=4)
    args = parser.parse_args()
    report = run_demo(frames=args.frames)
    print(
        json.dumps(
            {
                "run_name": RUN_NAME,
                "ok": report["summary"]["functional_output_parity_passed"],
                "byte_for_byte_identical_to_local_main": report["summary"]["byte_for_byte_identical_to_local_main"],
                "exact_hash_matches": report["summary"]["exact_hash_matches"],
                "output_folder": str(OUTPUT_DIR),
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "hardware_validation_claimed": report["claim_boundary"]["hardware_validation_claimed"],
                "physical_level_5_claimed": report["claim_boundary"]["physical_level_5_claimed"],
                "manufactured_player_claimed": report["claim_boundary"]["manufactured_player_claimed"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
