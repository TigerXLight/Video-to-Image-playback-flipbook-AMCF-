from __future__ import annotations

import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_integrated_demo_reports import write_integrated_demo_outputs  # noqa: E402


def main() -> None:
    out = PACKAGE / "output" / "physical_player_simulator_demo"
    summary = write_integrated_demo_outputs(out)
    print(
        json.dumps(
            {
                "ok": bool(summary["final_passed"]),
                "output_folder": str(out),
                "default_mechanism_profile_id": summary["default_mechanism_profile_id"],
                "profile_count": summary["mechanism_profile_phase"]["profile_count"],
                "forward_transition_count": summary["forward_playback_phase"]["forward_transition_count"],
                "fail_closed_scenario_count": summary["fail_closed_phase"]["scenario_count"],
                "fail_closed_event_count": summary["fail_closed_phase"]["fail_closed_event_count"],
                "reverse_attempts": summary["reverse_seek_phase"]["reverse_attempts"],
                "reverse_successes": summary["reverse_seek_phase"]["reverse_successes"],
                "reverse_denials": summary["reverse_seek_phase"]["reverse_denials"],
                "seek_attempts": summary["reverse_seek_phase"]["seek_attempts"],
                "seek_successes": summary["reverse_seek_phase"]["seek_successes"],
                "seek_denials": summary["reverse_seek_phase"]["seek_denials"],
                "arbitrary_seek_denied_count": summary["reverse_seek_phase"]["arbitrary_seek_denied_count"],
                "unsafe_acceptance_count": summary["unsafe_acceptance_audit"]["unsafe_acceptance_count"],
                "hardware_validation_claimed": summary["hardware_validation_claimed"],
                "physical_level_5_claimed": summary["physical_level_5_claimed"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
