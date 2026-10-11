from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from amcf_physical_player_state_machine import AMCFPhysicalPlayerStateMachine


def state_machine_to_dict(machine: AMCFPhysicalPlayerStateMachine) -> dict[str, Any]:
    return machine.to_dict()


def write_state_machine_timeline(machine: AMCFPhysicalPlayerStateMachine, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(machine.build_timeline(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_fail_closed_events(machine: AMCFPhysicalPlayerStateMachine, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(machine.to_dict()["fail_closed_events"], indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_unsafe_acceptance_audit(machine: AMCFPhysicalPlayerStateMachine) -> dict[str, Any]:
    return machine.audit_unsafe_acceptance()


def write_unsafe_acceptance_audit(machine: AMCFPhysicalPlayerStateMachine, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_unsafe_acceptance_audit(machine), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_fail_closed_safety_report(machine: AMCFPhysicalPlayerStateMachine) -> dict[str, Any]:
    audit = build_unsafe_acceptance_audit(machine)
    reasons = [event.reason for event in machine.fail_closed_events]
    return {
        "run_type": "physical_player_fail_closed_software_control_safety_model",
        "software_control_safety_model": True,
        "hardware_validation_claimed": False,
        "physical_level5_claimed": False,
        "real_sensors_required": False,
        "real_motors_required": False,
        "real_cartridges_required": False,
        "real_scans_required": False,
        "fail_closed_event_count": len(machine.fail_closed_events),
        "fail_closed_reasons_encountered": reasons,
        "unsafe_acceptance_count": audit["unsafe_acceptance_count"],
        "passed": audit["passed"] and machine.unsafe_acceptance_count == 0,
        "recommended_next_stage": "future hardware adapters should conform to this software safety contract before physical validation claims",
    }


def write_fail_closed_safety_report(machine: AMCFPhysicalPlayerStateMachine, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_fail_closed_safety_report(machine), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _events(machine: AMCFPhysicalPlayerStateMachine, event_type: str) -> list[dict[str, Any]]:
    return [event for event in machine.build_timeline() if event.get("event_type") == event_type]


def build_reverse_buffer_report(machine: AMCFPhysicalPlayerStateMachine) -> dict[str, Any]:
    return {
        "software_control_reverse_buffer": True,
        "hardware_validation_claimed": False,
        "physical_level5_claimed": False,
        "reverse_buffer_depth": machine.reverse_buffer_state.depth,
        "reverse_buffer_entries": machine.to_dict()["reverse_buffer_state"]["section_records"],
        "section_ids": list(machine.reverse_buffer_state.section_ids),
        "reverse_available": machine.reverse_buffer_state.reverse_available,
        "unsafe_acceptance_count": machine.unsafe_acceptance_count,
    }


def write_reverse_buffer_report(machine: AMCFPhysicalPlayerStateMachine, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_reverse_buffer_report(machine), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_seek_denial_report(machine: AMCFPhysicalPlayerStateMachine) -> dict[str, Any]:
    denials = [event for event in machine.build_timeline() if event.get("event_type") == "seek_denied"]
    arbitrary_denials = [event for event in denials if event.get("seek_status") == "seek_denied_arbitrary_not_supported"]
    return {
        "software_control_seek_denial": True,
        "hardware_validation_claimed": False,
        "physical_level5_claimed": False,
        "seek_denials": denials,
        "seek_denial_count": len(denials),
        "arbitrary_seek_denied_count": len(arbitrary_denials),
        "unsafe_acceptance_count": machine.unsafe_acceptance_count,
    }


def write_seek_denial_report(machine: AMCFPhysicalPlayerStateMachine, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_seek_denial_report(machine), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_reverse_seek_report(machine: AMCFPhysicalPlayerStateMachine) -> dict[str, Any]:
    audit = build_unsafe_acceptance_audit(machine)
    timeline = machine.build_timeline()
    reverse_attempts = len([event for event in timeline if event.get("event_type") == "reverse_requested"])
    reverse_successes = len([event for event in timeline if event.get("event_type") == "reverse_complete"])
    reverse_denials = len([event for event in timeline if event.get("event_type") == "reverse_denied"])
    seek_attempts = len([event for event in timeline if event.get("event_type") == "seek_requested"])
    seek_successes = len([event for event in timeline if event.get("event_type") == "seek_complete"])
    seek_denials = len([event for event in timeline if event.get("event_type") == "seek_denied"])
    arbitrary_seek_denied = len(
        [
            event
            for event in timeline
            if event.get("event_type") == "seek_denied" and event.get("seek_status") == "seek_denied_arbitrary_not_supported"
        ]
    )
    reverse_seek_fail_reasons = [
        item.reason
        for item in machine.fail_closed_events
        if item.reason
        in {
            "fail_closed_unverified_section",
            "fail_closed_hash_mismatch",
            "fail_closed_hidden_gate_not_ready",
            "fail_closed_unsafe_transition",
            "fail_closed_shutter_failure",
        }
    ]
    return {
        "run_type": "physical_player_reverse_seek_software_control_model",
        "software_control_reverse_seek_model": True,
        "hardware_validation_claimed": False,
        "physical_level5_claimed": False,
        "real_motors_required": False,
        "reverse_buffer_depth": machine.reverse_buffer_state.depth,
        "reverse_buffer_entries": machine.to_dict()["reverse_buffer_state"]["section_records"],
        "reverse_attempts": reverse_attempts,
        "reverse_successes": reverse_successes,
        "reverse_denials": reverse_denials,
        "seek_attempts": seek_attempts,
        "seek_successes": seek_successes,
        "seek_denials": seek_denials,
        "arbitrary_seek_denied_count": arbitrary_seek_denied,
        "fail_closed_count_during_reverse_seek": len(reverse_seek_fail_reasons),
        "fail_closed_reasons_during_reverse_seek": reverse_seek_fail_reasons,
        "unsafe_acceptance_count": audit["unsafe_acceptance_count"],
        "passed": audit["passed"] and machine.unsafe_acceptance_count == 0,
    }


def write_reverse_seek_report(machine: AMCFPhysicalPlayerStateMachine, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_reverse_seek_report(machine), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_state_machine_summary_markdown(machine: AMCFPhysicalPlayerStateMachine) -> str:
    summary = machine.build_summary()
    safety_report = build_fail_closed_safety_report(machine)
    lines = [
        "# AMCF Physical Player State Machine Summary",
        "",
        "This is a software/control simulator only. It defines deterministic control-state behavior that later physical hardware should conform to.",
        "",
        "## What Can Be Done Without Hardware",
        "",
        "- cartridge recognition policy",
        "- section verification decisions",
        "- A/B staging order",
        "- view-gate and hidden-gate readiness",
        "- transition blanking state",
        "- local reverse-buffer behavior",
        "- unsupported seek denial",
        "- fail-closed safety decisions",
        "",
        "No physical hardware validation is claimed.",
        "",
        "## Default Profile",
        "",
        "- carrier layout: folded_indexed_carrier",
        "- staging model: abstract_ab_staging",
        "- actuator family: motor_encoder",
        "- gate model: single_visible_gate_plus_hidden_staging",
        "- prefetch model: reader_prefetch_ahead",
        "- reverse model: limited_reverse_buffer",
        "",
        "## Run Summary",
        "",
        f"- number of events: {summary['event_count']}",
        f"- number of fail-closed events: {summary['fail_closed_event_count']}",
        f"- unsafe_acceptance_count: {summary['unsafe_acceptance_count']}",
        f"- safety report passed: {'yes' if safety_report['passed'] else 'no'}",
        f"- final playback state: {summary['final_playback_state']}",
        f"- final safety state: {summary['final_safety_state']}",
        "- manufactured hardware claimed: no",
        "- real sensors/motors/cartridges/scans required: no",
        "- hardware validation claimed: no",
    ]
    return "\n".join(lines) + "\n"
