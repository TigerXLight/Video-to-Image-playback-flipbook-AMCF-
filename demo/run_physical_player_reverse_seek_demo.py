from __future__ import annotations

import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_state_machine import AMCFPhysicalPlayerStateMachine, build_sample_cartridge  # noqa: E402
from amcf_physical_player_state_machine_reports import (  # noqa: E402
    build_reverse_seek_report,
    build_seek_denial_report,
    build_unsafe_acceptance_audit,
    write_fail_closed_events,
    write_reverse_buffer_report,
    write_reverse_seek_report,
    write_seek_denial_report,
    write_state_machine_timeline,
    write_unsafe_acceptance_audit,
)


def make_ready_machine(cartridge_kind: str = "valid") -> AMCFPhysicalPlayerStateMachine:
    machine = AMCFPhysicalPlayerStateMachine()
    machine.insert_cartridge(build_sample_cartridge(cartridge_kind))
    machine.recognize_manifest()
    machine.prefetch_current()
    machine.verify_current()
    machine.load_view_gate()
    machine.lock_view_gate()
    machine.enter_playback_ready()
    return machine


def run_primary_reverse_seek_path() -> AMCFPhysicalPlayerStateMachine:
    machine = make_ready_machine()
    machine.step_forward()
    machine.step_forward()
    machine.step_forward()
    machine.step_reverse()
    machine.request_seek(section_id="section_001")
    machine.request_seek(section_id="section_000")
    machine.reverse_buffer_state.section_records = []
    machine.reverse_buffer_state.section_ids = []
    machine.reverse_buffer_state.reverse_available = False
    machine.step_reverse()
    return machine


def run_invalid_seek_path() -> AMCFPhysicalPlayerStateMachine:
    machine = make_ready_machine("hash_mismatch")
    machine.request_seek(section_id="section_001")
    return machine


def main() -> None:
    out = PACKAGE / "output" / "physical_player_reverse_seek_demo"
    out.mkdir(parents=True, exist_ok=True)

    machine = run_primary_reverse_seek_path()
    invalid_seek_machine = run_invalid_seek_path()

    report = build_reverse_seek_report(machine)
    denial_report = build_seek_denial_report(machine)
    audit = build_unsafe_acceptance_audit(machine)
    fail_closed_events = machine.to_dict()["fail_closed_events"] + invalid_seek_machine.to_dict()["fail_closed_events"]

    write_state_machine_timeline(machine, out / "reverse_seek_timeline.json")
    write_reverse_buffer_report(machine, out / "reverse_buffer_report.json")
    write_seek_denial_report(machine, out / "seek_denial_report.json")
    (out / "fail_closed_events.json").write_text(json.dumps(fail_closed_events, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_unsafe_acceptance_audit(machine, out / "unsafe_acceptance_audit.json")
    write_reverse_seek_report(machine, out / "reverse_seek_report.json")
    (out / "REVERSE_SEEK_SUMMARY.md").write_text(
        "\n".join(
            [
                "# AMCF Physical Player Reverse/Seek Demo",
                "",
                "This deterministic demo exercises bounded software/control reverse and local seek behaviour for a future physical AMCF player.",
                "",
                "- hardware validation claimed: no",
                "- physical Level 5 claimed: no",
                "- real motors required: no",
                "- arbitrary physical seek claimed: no",
                f"- reverse attempts: {report['reverse_attempts']}",
                f"- reverse successes: {report['reverse_successes']}",
                f"- reverse denials: {report['reverse_denials']}",
                f"- seek attempts: {report['seek_attempts']}",
                f"- seek successes: {report['seek_successes']}",
                f"- seek denials: {report['seek_denials']}",
                f"- arbitrary seek denied count: {report['arbitrary_seek_denied_count']}",
                f"- fail-closed event count during reverse/seek: {len(fail_closed_events)}",
                f"- unsafe_acceptance_count: {audit['unsafe_acceptance_count']}",
                f"- reverse/seek report passed: {'yes' if report['passed'] else 'no'}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "ok": True,
                "output_folder": str(out),
                "reverse_attempts": report["reverse_attempts"],
                "reverse_successes": report["reverse_successes"],
                "reverse_denials": report["reverse_denials"],
                "seek_attempts": report["seek_attempts"],
                "seek_successes": report["seek_successes"],
                "seek_denials": report["seek_denials"],
                "arbitrary_seek_denied_count": report["arbitrary_seek_denied_count"],
                "fail_closed_event_count_during_reverse_seek": len(fail_closed_events),
                "unsafe_acceptance_count": audit["unsafe_acceptance_count"],
                "reverse_seek_report_passed": report["passed"],
                "hardware_validation_claimed": False,
                "physical_level5_claimed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
