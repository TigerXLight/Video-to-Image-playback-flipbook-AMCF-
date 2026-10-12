from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from amcf_physical_player_mechanism_profile_reports import (
    build_mechanism_claim_boundary_report,
    build_mechanism_profile_ranking,
)
from amcf_physical_player_mechanism_profiles import all_mechanism_profiles, default_mechanism_profile
from amcf_physical_player_state_machine import (
    AMCFPhysicalPlayerStateMachine,
    build_failure_section,
    build_sample_cartridge,
    verify_physical_section,
)
from amcf_physical_player_state_machine_reports import (
    build_fail_closed_safety_report,
    build_reverse_seek_report,
    build_unsafe_acceptance_audit,
    write_state_machine_timeline,
)


RUN_NAME = "AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1"
BASE_COMMIT_HINT = "01093024f9bbd11d10615a0f526b4440e5f8f41b"


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


def build_mechanism_profile_phase() -> dict[str, Any]:
    profiles = all_mechanism_profiles()
    default_profile = default_mechanism_profile()
    ranking = build_mechanism_profile_ranking(profiles)
    claim_report = build_mechanism_claim_boundary_report(profiles)
    passed = (
        default_profile.profile_id == "folded_ab_motor_encoder_baseline"
        and claim_report["passed"]
        and len(ranking.hardware_validated_profiles) == 0
        and len(ranking.physical_level_5_claimed_profiles) == 0
    )
    return {
        "passed": passed,
        "default_profile_id": default_profile.profile_id,
        "profile_count": len(profiles),
        "hardware_validated_profiles_count": len(ranking.hardware_validated_profiles),
        "physical_level_5_claimed_profiles_count": len(ranking.physical_level_5_claimed_profiles),
        "ranking_report": {
            "profiles_ranked": ranking.profiles_ranked,
            "recommended_first_simulator_profile": ranking.recommended_first_simulator_profile,
            "research_profiles": ranking.research_profiles,
            "support_layer_profiles": ranking.support_layer_profiles,
            "experimental_profiles": ranking.experimental_profiles,
            "warnings": ranking.warnings,
        },
        "claim_boundary_report": claim_report,
    }


def run_forward_playback_phase() -> tuple[AMCFPhysicalPlayerStateMachine, dict[str, Any]]:
    machine = make_ready_machine()
    machine.step_forward()
    machine.step_forward()
    timeline = machine.build_timeline()
    transition_count = len([event for event in timeline if event.get("event_type") == "switch_visible_section"])
    audit = build_unsafe_acceptance_audit(machine)
    phase = {
        "passed": transition_count >= 1 and audit["unsafe_acceptance_count"] == 0,
        "forward_transition_count": transition_count,
        "final_playback_state": machine.playback_state,
        "unsafe_acceptance_count": audit["unsafe_acceptance_count"],
        "hardware_required": False,
    }
    return machine, phase


def run_fail_closed_phase() -> dict[str, Any]:
    scenarios: list[dict[str, Any]] = []

    def add_verification(name: str, kind: str, expected_id: str | None = None) -> None:
        verification = verify_physical_section(build_failure_section(kind), expected_id)
        scenarios.append(
            {
                "scenario": name,
                "decision": verification.decision,
                "reason": verification.reason,
                "display_allowed": verification.display_allowed,
                "unsafe_acceptance": verification.unsafe_acceptance,
            }
        )

    add_verification("valid section path", "valid")
    add_verification("degraded colour warning path", "degraded_colour")
    add_verification("hash mismatch failure", "hash_mismatch")
    add_verification("missing marker failure", "missing_marker")
    add_verification("wrong section failure", "wrong_section", "expected_section_001")
    add_verification("invalid registration failure", "invalid_registration")

    machines: list[AMCFPhysicalPlayerStateMachine] = []
    timeout_machine = make_ready_machine()
    timeout_machine.prefetch_next()
    timeout_machine.simulate_prefetch_timeout()
    machines.append(timeout_machine)

    hidden_gate_machine = make_ready_machine()
    hidden_gate_machine.begin_transition_blank()
    machines.append(hidden_gate_machine)

    view_gate_machine = AMCFPhysicalPlayerStateMachine()
    view_gate_machine.insert_cartridge(build_sample_cartridge("valid"))
    view_gate_machine.recognize_manifest()
    view_gate_machine.prefetch_current()
    view_gate_machine.verify_current()
    view_gate_machine.enter_playback_ready()
    machines.append(view_gate_machine)

    shutter_machine = make_ready_machine()
    shutter_machine.prefetch_next()
    shutter_machine.verify_next()
    shutter_machine.stage_next()
    shutter_machine.simulate_shutter_failure("stuck_open")
    machines.append(shutter_machine)

    illumination_machine = make_ready_machine()
    illumination_machine.simulate_illumination_failure("fault")
    machines.append(illumination_machine)

    jam_machine = make_ready_machine()
    jam_machine.simulate_jam()
    machines.append(jam_machine)

    double_feed_machine = make_ready_machine()
    double_feed_machine.simulate_double_feed()
    machines.append(double_feed_machine)

    misfeed_machine = make_ready_machine()
    misfeed_machine.simulate_misfeed()
    machines.append(misfeed_machine)

    audio_machine = make_ready_machine()
    audio_decision = audio_machine.check_audio_sync(drift_ms=250, max_drift_ms=80)
    scenarios.append({"scenario": "audio sync limit", "decision": audio_decision.decision, "reason": audio_decision.reason, "display_allowed": audio_decision.display_allowed})

    fail_closed_events: list[dict[str, Any]] = []
    unsafe_acceptance_count = 0
    for machine in machines:
        fail_closed_events.extend(machine.to_dict()["fail_closed_events"])
        unsafe_acceptance_count += machine.audit_unsafe_acceptance()["unsafe_acceptance_count"]
        if machine.fail_closed_events:
            scenarios.append({"scenario": machine.fail_closed_events[-1].reason, "reason": machine.fail_closed_events[-1].reason, "display_allowed": False})

    aggregate_machine = make_ready_machine()
    aggregate_machine.step_forward()
    aggregate_machine.simulate_prefetch_timeout()
    safety_report = build_fail_closed_safety_report(aggregate_machine)
    unsafe_acceptance_count += safety_report["unsafe_acceptance_count"]
    return {
        "passed": len(fail_closed_events) >= 1 and unsafe_acceptance_count == 0 and safety_report["passed"],
        "scenario_count": len(scenarios),
        "fail_closed_event_count": len(fail_closed_events),
        "unsafe_acceptance_count": unsafe_acceptance_count,
        "fail_closed_events": fail_closed_events,
        "safety_report": safety_report,
    }


def run_reverse_seek_phase() -> tuple[AMCFPhysicalPlayerStateMachine, dict[str, Any]]:
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

    invalid_seek_machine = make_ready_machine("hash_mismatch")
    invalid_seek_machine.request_seek(section_id="section_001")

    report = build_reverse_seek_report(machine)
    audit = build_unsafe_acceptance_audit(machine)
    phase = {
        "passed": report["passed"] and audit["unsafe_acceptance_count"] == 0,
        "reverse_attempts": report["reverse_attempts"],
        "reverse_successes": report["reverse_successes"],
        "reverse_denials": report["reverse_denials"],
        "seek_attempts": report["seek_attempts"],
        "seek_successes": report["seek_successes"],
        "seek_denials": report["seek_denials"],
        "arbitrary_seek_denied_count": report["arbitrary_seek_denied_count"],
        "fail_closed_event_count": len(machine.fail_closed_events) + len(invalid_seek_machine.fail_closed_events),
        "unsafe_acceptance_count": audit["unsafe_acceptance_count"] + invalid_seek_machine.audit_unsafe_acceptance()["unsafe_acceptance_count"],
        "invalid_seek_fail_closed_events": invalid_seek_machine.to_dict()["fail_closed_events"],
        "reverse_seek_report": report,
    }
    return machine, phase


def build_integrated_simulation_summary() -> dict[str, Any]:
    mechanism_phase = build_mechanism_profile_phase()
    forward_machine, forward_phase = run_forward_playback_phase()
    fail_closed_phase = run_fail_closed_phase()
    reverse_machine, reverse_seek_phase = run_reverse_seek_phase()
    forward_audit = build_unsafe_acceptance_audit(forward_machine)
    reverse_audit = build_unsafe_acceptance_audit(reverse_machine)
    unsafe_count = (
        forward_phase["unsafe_acceptance_count"]
        + fail_closed_phase["unsafe_acceptance_count"]
        + reverse_seek_phase["unsafe_acceptance_count"]
    )
    unsafe_audit = {
        "passed": forward_audit["passed"] and reverse_audit["passed"] and unsafe_count == 0,
        "unsafe_acceptance_count": unsafe_count,
        "unsafe_events_count": len(forward_audit["unsafe_events"]) + len(reverse_audit["unsafe_events"]),
        "checked_event_count": forward_audit["checked_event_count"] + reverse_audit["checked_event_count"],
        "checked_section_count": forward_audit["checked_section_count"] + reverse_audit["checked_section_count"],
    }
    claim_values_false = {
        "physical_hardware_claimed": False,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "real_sensors_required": False,
        "real_motors_required": False,
        "real_cartridges_required": False,
        "real_scans_required": False,
        "manufactured_player_claimed": False,
    }
    final_passed = (
        mechanism_phase["passed"]
        and forward_phase["passed"]
        and fail_closed_phase["passed"]
        and reverse_seek_phase["passed"]
        and unsafe_audit["passed"]
        and unsafe_audit["unsafe_acceptance_count"] == 0
        and all(value is False for value in claim_values_false.values())
    )
    return {
        "run_name": RUN_NAME,
        "base_commit_hint": BASE_COMMIT_HINT,
        "software_control_simulator_only": True,
        **claim_values_false,
        "default_mechanism_profile_id": mechanism_phase["default_profile_id"],
        "mechanism_profile_phase": mechanism_phase,
        "forward_playback_phase": forward_phase,
        "fail_closed_phase": fail_closed_phase,
        "reverse_seek_phase": reverse_seek_phase,
        "unsafe_acceptance_audit": unsafe_audit,
        "final_passed": final_passed,
        "recommended_next_stage": "future hardware adapter alignment or documentation polish; no hardware validation claim until real hardware tests exist",
    }


def write_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_integrated_simulation_summary(summary: dict[str, Any], path: str | Path) -> None:
    write_json(path, summary)


def build_integrated_summary_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# AMCF Physical Player Simulator Demo Summary",
        "",
        "This is a software/control simulator only. It integrates mechanism profiles, state-machine playback, fail-closed safety, bounded reverse/seek, and unsafe-acceptance auditing.",
        "",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        f"- default mechanism profile: {summary['default_mechanism_profile_id']}",
        f"- forward playback exercised: {'yes' if summary['forward_playback_phase']['passed'] else 'no'}",
        f"- fail-closed exercised: {'yes' if summary['fail_closed_phase']['passed'] else 'no'}",
        f"- reverse/seek exercised: {'yes' if summary['reverse_seek_phase']['passed'] else 'no'}",
        f"- unsafe_acceptance_count: {summary['unsafe_acceptance_audit']['unsafe_acceptance_count']}",
        f"- integrated report passed: {'yes' if summary['final_passed'] else 'no'}",
        "",
        "Generated outputs are demo artifacts, not hardware proof.",
        "",
    ]
    return "\n".join(lines)


def build_next_steps_markdown() -> str:
    return "\n".join(
        [
            "# Next Steps",
            "",
            "- Keep the simulator as the software/control contract for later physical-player hardware.",
            "- Do not claim manufactured hardware, real no-gap optical switching, real reverse hardware, arbitrary physical seek, or hardware validation until physical tests exist.",
            "- Future work may add adapter-specific recognition/control layers that conform to this integrated simulator contract.",
            "",
        ]
    )


def write_integrated_demo_outputs(output_dir: str | Path) -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = build_integrated_simulation_summary()
    forward_machine, _forward_phase = run_forward_playback_phase()
    reverse_machine, _reverse_phase = run_reverse_seek_phase()
    mechanism_phase = summary["mechanism_profile_phase"]
    claim_report = mechanism_phase["claim_boundary_report"]
    fail_closed_report = summary["fail_closed_phase"]["safety_report"]
    reverse_report = summary["reverse_seek_phase"]["reverse_seek_report"]
    unsafe_audit = summary["unsafe_acceptance_audit"]

    write_integrated_simulation_summary(summary, output_dir / "integrated_simulation_summary.json")
    write_json(output_dir / "mechanism_profile_report.json", mechanism_phase)
    write_state_machine_timeline(forward_machine, output_dir / "forward_playback_timeline.json")
    write_json(output_dir / "fail_closed_safety_report.json", fail_closed_report)
    write_json(output_dir / "reverse_seek_report.json", reverse_report)
    write_json(output_dir / "unsafe_acceptance_audit.json", unsafe_audit)
    write_json(output_dir / "claim_boundary_report.json", claim_report)
    (output_dir / "PHYSICAL_PLAYER_SIMULATOR_DEMO_SUMMARY.md").write_text(build_integrated_summary_markdown(summary), encoding="utf-8")
    (output_dir / "NEXT_STEPS.md").write_text(build_next_steps_markdown(), encoding="utf-8")
    # Keep the reverse machine evaluated so the integrated output writer exercises both orchestration paths.
    _ = reverse_machine
    return summary
