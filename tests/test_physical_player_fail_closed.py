from __future__ import annotations

import sys
import unittest
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_state_machine import (  # noqa: E402
    AMCFPhysicalPlayerStateMachine,
    DECISION_ACCEPTED,
    DECISION_ACCEPTED_WITH_WARNING,
    DECISION_HOLD_PREVIOUS_SAFE_STATE,
    DECISION_RESCAN_REQUIRED,
    DECISION_REJECTED_FAIL_CLOSED,
    FAIL_CLOSED_AUDIO_SYNC_LIMIT,
    FAIL_CLOSED_DOUBLE_FEED,
    FAIL_CLOSED_HASH_MISMATCH,
    FAIL_CLOSED_HIDDEN_GATE_NOT_READY,
    FAIL_CLOSED_ILLUMINATION_FAILURE,
    FAIL_CLOSED_JAM,
    FAIL_CLOSED_MISFEED,
    FAIL_CLOSED_MISSING_MARKER,
    FAIL_CLOSED_REGISTRATION_FAILURE,
    FAIL_CLOSED_UNSAFE_TRANSITION,
    FAIL_CLOSED_UNSUPPORTED_CARRIER,
    FAIL_CLOSED_UNVERIFIED_SECTION,
    FAIL_CLOSED_VIEW_GATE_NOT_LOCKED,
    FAIL_CLOSED_WRONG_SECTION,
    FAIL_CLOSED_UNKNOWN_CRITICAL_LANE,
    STATE_FAIL_CLOSED,
    STATE_MECHANICAL_STOP,
    build_failure_section,
    build_sample_cartridge,
    verify_physical_section,
)
from amcf_physical_player_state_machine_reports import (  # noqa: E402
    build_fail_closed_safety_report,
    build_unsafe_acceptance_audit,
)


class PhysicalPlayerFailClosedTests(unittest.TestCase):
    def make_ready_machine(self, cartridge_kind: str = "valid") -> AMCFPhysicalPlayerStateMachine:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge(cartridge_kind))
        self.assertTrue(machine.recognize_manifest())
        self.assertTrue(machine.prefetch_current())
        self.assertTrue(machine.verify_current())
        self.assertTrue(machine.load_view_gate())
        self.assertTrue(machine.lock_view_gate())
        self.assertTrue(machine.enter_playback_ready())
        return machine

    def test_valid_section_path_accepted(self) -> None:
        verification = verify_physical_section(build_failure_section("valid"))
        self.assertEqual(verification.decision, DECISION_ACCEPTED)
        self.assertTrue(verification.display_allowed)
        self.assertFalse(verification.unsafe_acceptance)

    def test_degraded_colour_accepted_with_warning_and_no_unsafe_acceptance(self) -> None:
        verification = verify_physical_section(build_failure_section("degraded_colour"))
        self.assertEqual(verification.decision, DECISION_ACCEPTED_WITH_WARNING)
        self.assertTrue(verification.display_allowed)
        self.assertFalse(verification.unsafe_acceptance)
        self.assertTrue(verification.warnings)

    def test_hash_mismatch_rejected_fail_closed(self) -> None:
        verification = verify_physical_section(build_failure_section("hash_mismatch"))
        self.assertEqual(verification.decision, DECISION_REJECTED_FAIL_CLOSED)
        self.assertEqual(verification.reason, FAIL_CLOSED_HASH_MISMATCH)
        self.assertFalse(verification.display_allowed)

    def test_missing_marker_rescan_or_fail_closed(self) -> None:
        verification = verify_physical_section(build_failure_section("missing_marker"))
        self.assertEqual(verification.decision, DECISION_RESCAN_REQUIRED)
        self.assertEqual(verification.reason, FAIL_CLOSED_MISSING_MARKER)
        self.assertFalse(verification.display_allowed)

    def test_wrong_section_rejected_fail_closed(self) -> None:
        verification = verify_physical_section(build_failure_section("wrong_section"), expected_section_id="expected_section_001")
        self.assertEqual(verification.decision, DECISION_REJECTED_FAIL_CLOSED)
        self.assertEqual(verification.reason, FAIL_CLOSED_WRONG_SECTION)
        self.assertFalse(verification.display_allowed)

    def test_invalid_timing_index_rejected_fail_closed(self) -> None:
        verification = verify_physical_section(build_failure_section("invalid_timing"))
        self.assertEqual(verification.decision, DECISION_REJECTED_FAIL_CLOSED)
        self.assertEqual(verification.reason, FAIL_CLOSED_UNVERIFIED_SECTION)
        self.assertFalse(verification.display_allowed)

    def test_invalid_registration_rejected_or_rescan_before_display(self) -> None:
        verification = verify_physical_section(build_failure_section("invalid_registration"))
        self.assertEqual(verification.decision, DECISION_RESCAN_REQUIRED)
        self.assertEqual(verification.reason, FAIL_CLOSED_REGISTRATION_FAILURE)
        self.assertFalse(verification.display_allowed)

    def test_unsupported_section_type_rejected_fail_closed(self) -> None:
        verification = verify_physical_section(build_failure_section("unsupported_section_type"))
        self.assertEqual(verification.decision, DECISION_REJECTED_FAIL_CLOSED)
        self.assertEqual(verification.reason, FAIL_CLOSED_UNSUPPORTED_CARRIER)
        self.assertFalse(verification.display_allowed)

    def test_unknown_critical_lane_rejected_fail_closed(self) -> None:
        verification = verify_physical_section(build_failure_section("unknown_hash_status"))
        self.assertEqual(verification.decision, DECISION_REJECTED_FAIL_CLOSED)
        self.assertEqual(verification.reason, FAIL_CLOSED_UNKNOWN_CRITICAL_LANE)
        self.assertFalse(verification.display_allowed)

    def test_prefetch_timeout_prevents_transition(self) -> None:
        machine = self.make_ready_machine()
        machine.prefetch_next()
        machine.simulate_prefetch_timeout()
        self.assertEqual(machine.fail_closed_events[-1].reason, "fail_closed_prefetch_timeout")
        self.assertFalse(machine.safety_state.transition_allowed)
        self.assertEqual(machine.unsafe_acceptance_count, 0)

    def test_view_gate_unlocked_prevents_display(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("valid"))
        machine.recognize_manifest()
        machine.prefetch_current()
        machine.verify_current()
        self.assertFalse(machine.enter_playback_ready())
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_VIEW_GATE_NOT_LOCKED)
        self.assertFalse(machine.view_gate_state.illumination_allowed)

    def test_hidden_gate_not_ready_prevents_transition(self) -> None:
        machine = self.make_ready_machine()
        self.assertFalse(machine.begin_transition_blank())
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_HIDDEN_GATE_NOT_READY)
        self.assertFalse(machine.safety_state.transition_allowed)

    def test_switch_without_blanking_is_denied(self) -> None:
        machine = self.make_ready_machine()
        machine.prefetch_next()
        machine.verify_next()
        machine.stage_next()
        self.assertFalse(machine.switch_visible_section())
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_UNSAFE_TRANSITION)

    def test_unverified_next_section_cannot_switch_visible(self) -> None:
        machine = self.make_ready_machine()
        machine.prefetch_next()
        machine.hidden_gate_state.ready_for_switch = True
        machine.ab_gate_state.blanking_active = True
        self.assertFalse(machine.switch_visible_section())
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_UNVERIFIED_SECTION)

    def test_shutter_failure_denies_transition(self) -> None:
        machine = self.make_ready_machine()
        machine.prefetch_next()
        machine.verify_next()
        machine.stage_next()
        self.assertFalse(machine.simulate_shutter_failure("stuck_open"))
        self.assertEqual(machine.fail_closed_events[-1].reason, "fail_closed_shutter_failure")

    def test_illumination_failure_denies_display_or_switch(self) -> None:
        machine = self.make_ready_machine()
        machine.simulate_illumination_failure("fault")
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_ILLUMINATION_FAILURE)
        self.assertFalse(machine.view_gate_state.illumination_allowed)

    def test_jam_creates_mechanical_stop_or_fail_closed(self) -> None:
        machine = self.make_ready_machine()
        machine.simulate_jam()
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_JAM)
        self.assertEqual(machine.playback_state, STATE_MECHANICAL_STOP)
        self.assertFalse(machine.safety_state.motion_allowed)

    def test_double_feed_fails_closed(self) -> None:
        machine = self.make_ready_machine()
        machine.simulate_double_feed()
        self.assertEqual(machine.playback_state, STATE_FAIL_CLOSED)
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_DOUBLE_FEED)

    def test_misfeed_fails_closed(self) -> None:
        machine = self.make_ready_machine()
        machine.simulate_misfeed()
        self.assertEqual(machine.playback_state, STATE_FAIL_CLOSED)
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_MISFEED)

    def test_audio_sync_limit_pauses_or_resyncs_safely(self) -> None:
        machine = self.make_ready_machine()
        decision = machine.check_audio_sync(drift_ms=250, max_drift_ms=80)
        self.assertEqual(decision.decision, DECISION_HOLD_PREVIOUS_SAFE_STATE)
        self.assertEqual(decision.reason, FAIL_CLOSED_AUDIO_SYNC_LIMIT)
        self.assertFalse(decision.transition_allowed)
        self.assertEqual(machine.unsafe_acceptance_count, 0)

    def test_unsafe_acceptance_audit_reports_zero(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        machine.simulate_double_feed()
        audit = build_unsafe_acceptance_audit(machine)
        self.assertTrue(audit["passed"])
        self.assertEqual(audit["unsafe_acceptance_count"], 0)

    def test_safety_report_says_hardware_validation_claimed_false(self) -> None:
        report = build_fail_closed_safety_report(self.make_ready_machine())
        self.assertFalse(report["hardware_validation_claimed"])

    def test_safety_report_says_physical_level5_claimed_false(self) -> None:
        report = build_fail_closed_safety_report(self.make_ready_machine())
        self.assertFalse(report["physical_level5_claimed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
