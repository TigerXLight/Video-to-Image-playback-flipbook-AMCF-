from __future__ import annotations

import sys
import unittest
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_state_machine import (  # noqa: E402
    AMCFPhysicalPlayerStateMachine,
    FAIL_CLOSED_HASH_MISMATCH,
    FAIL_CLOSED_HIDDEN_GATE_NOT_READY,
    FAIL_CLOSED_UNSAFE_TRANSITION,
    SEEK_DENIED_ARBITRARY_NOT_SUPPORTED,
    SEEK_DENIED_UNVERIFIED_TARGET,
    SEEK_RESOLVED_LOCAL_BUFFER,
    build_sample_cartridge,
    verify_physical_section,
)
from amcf_physical_player_state_machine_reports import (  # noqa: E402
    build_reverse_seek_report,
    build_unsafe_acceptance_audit,
)


class PhysicalPlayerReverseSeekTests(unittest.TestCase):
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

    def test_reverse_buffer_starts_empty(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        self.assertEqual(machine.reverse_buffer_state.section_ids, [])
        self.assertEqual(machine.reverse_buffer_state.section_records, [])

    def test_verified_displayed_sections_enter_reverse_buffer(self) -> None:
        machine = self.make_ready_machine()
        self.assertTrue(machine.step_forward())
        self.assertIn("section_000", machine.reverse_buffer_state.section_ids)
        self.assertTrue(machine.reverse_buffer_state.section_records[-1].safe_for_reverse)

    def test_invalid_sections_do_not_enter_safe_reverse_buffer(self) -> None:
        machine = self.make_ready_machine("hash_mismatch")
        machine.old_section_id = "section_001"
        machine.view_gate_state.locked = True
        machine.park_old_section()
        self.assertNotIn("section_001", machine.reverse_buffer_state.section_ids)

    def test_reverse_buffer_respects_configured_depth(self) -> None:
        machine = self.make_ready_machine()
        machine.reverse_buffer_state.depth = 2
        self.assertTrue(machine.step_forward())
        self.assertTrue(machine.step_forward())
        self.assertTrue(machine.step_forward())
        self.assertLessEqual(len(machine.reverse_buffer_state.section_ids), 2)
        self.assertEqual(machine.reverse_buffer_state.section_ids, ["section_001", "section_002"])

    def test_step_reverse_denied_when_buffer_empty(self) -> None:
        machine = self.make_ready_machine()
        self.assertFalse(machine.step_reverse())
        self.assertEqual(machine.reverse_buffer_state.reverse_denial_reason, "reverse_buffer_empty")

    def test_step_reverse_resolves_previous_safe_section(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        self.assertTrue(machine.step_reverse())
        self.assertEqual(machine.current_section_id, "section_000")

    def test_step_reverse_stages_previous_section_in_hidden_gate(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        self.assertTrue(machine.step_reverse())
        self.assertIn("reverse_staged", [event["event_type"] for event in machine.event_log])

    def test_step_reverse_uses_transition_blanking(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        self.assertTrue(machine.step_reverse())
        self.assertIn("reverse_transition_blank", [event["event_type"] for event in machine.event_log])

    def test_step_reverse_updates_current_section_id(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        machine.step_forward()
        self.assertTrue(machine.step_reverse())
        self.assertEqual(machine.current_section_id, "section_001")

    def test_step_reverse_records_timeline_events(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        machine.step_reverse()
        events = [event["event_type"] for event in machine.event_log]
        self.assertIn("reverse_requested", events)
        self.assertIn("reverse_complete", events)

    def test_reverse_target_hash_mismatch_fails_closed_or_denies_safely(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        target = machine._section_by_id("section_000")
        self.assertIsNotNone(target)
        target.hash_ok = False
        self.assertFalse(machine.step_reverse())
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_HASH_MISMATCH)

    def test_reverse_hidden_gate_not_ready_fails_closed(self) -> None:
        machine = self.make_ready_machine()
        self.assertFalse(machine.begin_transition_blank())
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_HIDDEN_GATE_NOT_READY)

    def test_reverse_without_blanking_denied(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        target_id = machine.reverse_buffer_state.section_ids[-1]
        machine.next_section_id = target_id
        machine.next_verification_state = verify_physical_section(machine._section_by_id(target_id), target_id)
        machine.stage_next()
        self.assertFalse(machine.switch_visible_section())
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_UNSAFE_TRANSITION)

    def test_local_buffer_seek_resolves_available_section(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        machine.step_forward()
        state = machine.resolve_seek_target(section_id="section_000")
        self.assertTrue(state.seek_available)
        self.assertEqual(state.seek_status, SEEK_RESOLVED_LOCAL_BUFFER)

    def test_local_buffer_seek_switches_only_verified_target(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        machine.step_forward()
        self.assertTrue(machine.request_seek(section_id="section_000"))
        self.assertEqual(machine.current_section_id, "section_000")

    def test_arbitrary_seek_outside_local_buffer_is_denied(self) -> None:
        machine = self.make_ready_machine()
        self.assertFalse(machine.request_seek(section_id=machine.current_section_id))
        self.assertEqual(machine.seek_request_state.seek_status, SEEK_DENIED_ARBITRARY_NOT_SUPPORTED)

    def test_seek_to_invalid_section_fails_closed_or_denies_safely(self) -> None:
        machine = self.make_ready_machine("hash_mismatch")
        self.assertFalse(machine.request_seek(section_id="section_001"))
        self.assertEqual(machine.seek_request_state.seek_status, SEEK_DENIED_UNVERIFIED_TARGET)
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_HASH_MISMATCH)

    def test_seek_denial_does_not_increment_unsafe_acceptance_count(self) -> None:
        machine = self.make_ready_machine()
        machine.request_seek(section_id="section_002")
        self.assertEqual(machine.unsafe_acceptance_count, 0)

    def test_reverse_seek_report_says_hardware_validation_claimed_false(self) -> None:
        report = build_reverse_seek_report(self.make_ready_machine())
        self.assertFalse(report["hardware_validation_claimed"])

    def test_reverse_seek_report_says_physical_level5_claimed_false(self) -> None:
        report = build_reverse_seek_report(self.make_ready_machine())
        self.assertFalse(report["physical_level5_claimed"])

    def test_unsafe_acceptance_audit_remains_zero(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        machine.request_seek(section_id="section_999")
        audit = build_unsafe_acceptance_audit(machine)
        self.assertTrue(audit["passed"])
        self.assertEqual(audit["unsafe_acceptance_count"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
