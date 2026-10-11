from __future__ import annotations

import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_state_machine import AMCFPhysicalPlayerStateMachine, build_sample_cartridge  # noqa: E402
from amcf_physical_player_state_machine_reports import (  # noqa: E402
    build_state_machine_summary_markdown,
    state_machine_to_dict,
    write_fail_closed_events,
    write_state_machine_timeline,
)


def run_nominal_machine() -> AMCFPhysicalPlayerStateMachine:
    machine = AMCFPhysicalPlayerStateMachine()
    machine.insert_cartridge(build_sample_cartridge("valid"))
    machine.recognize_manifest()
    machine.prefetch_current()
    machine.verify_current()
    machine.load_view_gate()
    machine.lock_view_gate()
    machine.enter_playback_ready()
    machine.step_forward()
    machine.step_forward()
    machine.step_forward()
    machine.request_seek(section_id="section_999_not_local")
    return machine


def run_fail_closed_machine() -> AMCFPhysicalPlayerStateMachine:
    machine = AMCFPhysicalPlayerStateMachine()
    machine.insert_cartridge(build_sample_cartridge("hash_mismatch"))
    machine.recognize_manifest()
    machine.prefetch_current()
    machine.verify_current()
    machine.load_view_gate()
    machine.lock_view_gate()
    machine.enter_playback_ready()
    machine.step_forward()
    return machine


def main() -> None:
    out = PACKAGE / "output" / "physical_player_state_machine_demo"
    out.mkdir(parents=True, exist_ok=True)
    machine = run_nominal_machine()
    fail_machine = run_fail_closed_machine()

    write_state_machine_timeline(machine, out / "state_machine_timeline.json")
    write_fail_closed_events(fail_machine, out / "fail_closed_events.json")
    (out / "final_state.json").write_text(json.dumps(state_machine_to_dict(machine), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "STATE_MACHINE_SUMMARY.md").write_text(build_state_machine_summary_markdown(machine), encoding="utf-8")

    result = {
        "ok": True,
        "output_folder": str(out),
        "final_playback_state": machine.playback_state,
        "fail_closed_event_count": len(fail_machine.fail_closed_events),
        "unsafe_acceptance_count": machine.unsafe_acceptance_count + fail_machine.unsafe_acceptance_count,
        "hardware_validation_claimed": False,
        "physical_hardware_claimed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
