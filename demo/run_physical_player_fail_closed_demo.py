from __future__ import annotations

import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_state_machine import (  # noqa: E402
    AMCFPhysicalPlayerStateMachine,
    build_failure_section,
    build_sample_cartridge,
    verify_physical_section,
)
from amcf_physical_player_state_machine_reports import (  # noqa: E402
    build_fail_closed_safety_report,
    build_unsafe_acceptance_audit,
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


def summarize_verification(name: str, kind: str, expected_id: str | None = None) -> dict[str, object]:
    section = build_failure_section(kind)
    verification = verify_physical_section(section, expected_id)
    return {
        "scenario": name,
        "decision": verification.decision,
        "reason": verification.reason,
        "severity": verification.severity,
        "display_allowed": verification.display_allowed,
        "unsafe_acceptance": verification.unsafe_acceptance,
        "warnings": verification.warnings,
    }


def run_demo() -> dict[str, object]:
    scenarios: list[dict[str, object]] = []

    valid = verify_physical_section(build_failure_section("valid"))
    scenarios.append(
        {
            "scenario": "valid section path",
            "decision": valid.decision,
            "reason": valid.reason,
            "display_allowed": valid.display_allowed,
            "unsafe_acceptance": valid.unsafe_acceptance,
        }
    )
    scenarios.append(summarize_verification("degraded colour warning path", "degraded_colour"))
    scenarios.append(summarize_verification("hash mismatch failure", "hash_mismatch"))
    scenarios.append(summarize_verification("missing marker failure", "missing_marker"))
    scenarios.append(summarize_verification("wrong section failure", "wrong_section", "expected_section_001"))
    scenarios.append(summarize_verification("invalid timing/index failure", "invalid_timing"))
    scenarios.append(summarize_verification("invalid registration failure", "invalid_registration"))
    scenarios.append(summarize_verification("unsupported section type failure", "unsupported_section_type"))
    scenarios.append(summarize_verification("missing metadata critical failure", "missing_metadata_critical"))
    scenarios.append(summarize_verification("unknown hash status failure", "unknown_hash_status"))

    timeout_machine = make_ready_machine()
    timeout_machine.prefetch_next()
    timeout_machine.simulate_prefetch_timeout()
    scenarios.append({"scenario": "prefetch timeout", "reason": timeout_machine.fail_closed_events[-1].reason, "display_allowed": False})

    hidden_gate_machine = make_ready_machine()
    hidden_gate_machine.begin_transition_blank()
    scenarios.append({"scenario": "hidden gate not ready", "reason": hidden_gate_machine.fail_closed_events[-1].reason, "display_allowed": False})

    view_gate_machine = AMCFPhysicalPlayerStateMachine()
    view_gate_machine.insert_cartridge(build_sample_cartridge("valid"))
    view_gate_machine.recognize_manifest()
    view_gate_machine.prefetch_current()
    view_gate_machine.verify_current()
    view_gate_machine.enter_playback_ready()
    scenarios.append({"scenario": "view gate unlocked", "reason": view_gate_machine.fail_closed_events[-1].reason, "display_allowed": False})

    no_blanking_machine = make_ready_machine()
    no_blanking_machine.prefetch_next()
    no_blanking_machine.verify_next()
    no_blanking_machine.stage_next()
    no_blanking_machine.switch_visible_section()
    scenarios.append({"scenario": "switch without blanking", "reason": no_blanking_machine.fail_closed_events[-1].reason, "display_allowed": False})

    unverified_next_machine = make_ready_machine()
    unverified_next_machine.prefetch_next()
    unverified_next_machine.hidden_gate_state.ready_for_switch = True
    unverified_next_machine.ab_gate_state.blanking_active = True
    unverified_next_machine.switch_visible_section()
    scenarios.append({"scenario": "unverified next section switch", "reason": unverified_next_machine.fail_closed_events[-1].reason, "display_allowed": False})

    shutter_machine = make_ready_machine()
    shutter_machine.prefetch_next()
    shutter_machine.verify_next()
    shutter_machine.stage_next()
    shutter_machine.simulate_shutter_failure("stuck_open")
    scenarios.append({"scenario": "shutter stuck open", "reason": shutter_machine.fail_closed_events[-1].reason, "display_allowed": False})

    illumination_machine = make_ready_machine()
    illumination_machine.simulate_illumination_failure("fault")
    scenarios.append({"scenario": "illumination fault", "reason": illumination_machine.fail_closed_events[-1].reason, "display_allowed": False})

    jam_machine = make_ready_machine()
    jam_machine.simulate_jam()
    scenarios.append({"scenario": "jam placeholder", "reason": jam_machine.fail_closed_events[-1].reason, "playback_state": jam_machine.playback_state})

    double_feed_machine = make_ready_machine()
    double_feed_machine.simulate_double_feed()
    scenarios.append({"scenario": "double-feed placeholder", "reason": double_feed_machine.fail_closed_events[-1].reason, "display_allowed": False})

    misfeed_machine = make_ready_machine()
    misfeed_machine.simulate_misfeed()
    scenarios.append({"scenario": "misfeed placeholder", "reason": misfeed_machine.fail_closed_events[-1].reason, "display_allowed": False})

    audio_machine = make_ready_machine()
    audio_decision = audio_machine.check_audio_sync(drift_ms=250, max_drift_ms=80)
    scenarios.append({"scenario": "audio sync limit", "reason": audio_decision.reason, "decision": audio_decision.decision, "display_allowed": audio_decision.display_allowed})

    aggregate_machine = make_ready_machine()
    aggregate_machine.step_forward()
    aggregate_machine.simulate_prefetch_timeout()
    audit = build_unsafe_acceptance_audit(aggregate_machine)
    safety_report = build_fail_closed_safety_report(aggregate_machine)

    all_fail_closed_events = []
    for machine in [
        timeout_machine,
        hidden_gate_machine,
        view_gate_machine,
        no_blanking_machine,
        unverified_next_machine,
        shutter_machine,
        illumination_machine,
        jam_machine,
        double_feed_machine,
        misfeed_machine,
    ]:
        all_fail_closed_events.extend(machine.to_dict()["fail_closed_events"])

    return {
        "scenarios": scenarios,
        "fail_closed_events": all_fail_closed_events,
        "unsafe_acceptance_audit": audit,
        "safety_report": safety_report,
        "scenario_count": len(scenarios),
        "fail_closed_event_count": len(all_fail_closed_events),
        "unsafe_acceptance_count": audit["unsafe_acceptance_count"],
        "hardware_validation_claimed": False,
        "physical_level5_claimed": False,
    }


def main() -> None:
    out = PACKAGE / "output" / "physical_player_fail_closed_demo"
    out.mkdir(parents=True, exist_ok=True)
    result = run_demo()
    (out / "fail_closed_scenarios.json").write_text(json.dumps(result["scenarios"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "fail_closed_events.json").write_text(json.dumps(result["fail_closed_events"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "unsafe_acceptance_audit.json").write_text(json.dumps(result["unsafe_acceptance_audit"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "safety_report.json").write_text(json.dumps(result["safety_report"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "FAIL_CLOSED_SUMMARY.md").write_text(
        "\n".join(
            [
                "# AMCF Physical Player Fail-Closed Demo",
                "",
                "This deterministic demo exercises software/control safety decisions for a future physical AMCF player.",
                "",
                "- hardware validation claimed: no",
                "- physical Level 5 claimed: no",
                "- real sensors/motors/cartridges/scans required: no",
                f"- fail-closed scenario count: {result['scenario_count']}",
                f"- fail-closed event count: {result['fail_closed_event_count']}",
                f"- unsafe_acceptance_count: {result['unsafe_acceptance_count']}",
                f"- safety report passed: {'yes' if result['safety_report']['passed'] else 'no'}",
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
                "scenario_count": result["scenario_count"],
                "fail_closed_event_count": result["fail_closed_event_count"],
                "unsafe_acceptance_count": result["unsafe_acceptance_count"],
                "safety_report_passed": result["safety_report"]["passed"],
                "hardware_validation_claimed": False,
                "physical_level5_claimed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
