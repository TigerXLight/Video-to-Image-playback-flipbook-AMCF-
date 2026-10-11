from __future__ import annotations

import unittest

import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_state_machine import (  # noqa: E402
    AMCFPhysicalPlayerStateMachine,
    FAIL_CLOSED_HASH_MISMATCH,
    FAIL_CLOSED_MANIFEST_MISMATCH,
    STATE_CARTRIDGE_INSERTED,
    STATE_FAIL_CLOSED,
    STATE_MANIFEST_RECOGNIZED,
    STATE_NO_CARTRIDGE,
    STATE_PLAYBACK_READY,
    build_sample_cartridge,
)
from amcf_physical_player_state_machine_reports import build_state_machine_summary_markdown  # noqa: E402


class PhysicalPlayerStateMachineTests(unittest.TestCase):
    def make_ready_machine(self) -> AMCFPhysicalPlayerStateMachine:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("valid"))
        self.assertTrue(machine.recognize_manifest())
        self.assertTrue(machine.prefetch_current())
        self.assertTrue(machine.verify_current())
        self.assertTrue(machine.load_view_gate())
        self.assertTrue(machine.lock_view_gate())
        self.assertTrue(machine.enter_playback_ready())
        return machine

    def test_state_machine_starts_at_no_cartridge(self) -> None:
        self.assertEqual(AMCFPhysicalPlayerStateMachine().playback_state, STATE_NO_CARTRIDGE)

    def test_insert_cartridge_moves_to_cartridge_inserted(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("valid"))
        self.assertEqual(machine.playback_state, STATE_CARTRIDGE_INSERTED)

    def test_recognize_manifest_moves_to_manifest_recognized_for_valid_sample(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("valid"))
        self.assertTrue(machine.recognize_manifest())
        self.assertEqual(machine.playback_state, STATE_MANIFEST_RECOGNIZED)

    def test_invalid_manifest_fails_closed(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("manifest_mismatch"))
        self.assertFalse(machine.recognize_manifest())
        self.assertEqual(machine.playback_state, STATE_FAIL_CLOSED)
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_MANIFEST_MISMATCH)

    def test_prefetch_current_chooses_a_section(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("valid"))
        machine.recognize_manifest()
        self.assertTrue(machine.prefetch_current())
        self.assertEqual(machine.current_section_id, "section_000")

    def test_verify_current_accepts_valid_section(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("valid"))
        machine.recognize_manifest()
        machine.prefetch_current()
        self.assertTrue(machine.verify_current())
        self.assertTrue(machine.current_verification_state.display_allowed)

    def test_load_view_gate_requires_verification(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("valid"))
        machine.recognize_manifest()
        machine.prefetch_current()
        self.assertFalse(machine.load_view_gate())
        self.assertEqual(machine.playback_state, STATE_FAIL_CLOSED)

    def test_lock_view_gate_sets_locked_aligned_illumination_allowed(self) -> None:
        machine = self.make_ready_machine()
        self.assertTrue(machine.view_gate_state.locked)
        self.assertTrue(machine.view_gate_state.aligned)
        self.assertTrue(machine.view_gate_state.illumination_allowed)

    def test_playback_ready_requires_locked_verified_section(self) -> None:
        machine = self.make_ready_machine()
        self.assertEqual(machine.playback_state, STATE_PLAYBACK_READY)
        self.assertTrue(machine.safety_state.playback_allowed)

    def test_prefetch_next_finds_next_section(self) -> None:
        machine = self.make_ready_machine()
        self.assertTrue(machine.prefetch_next())
        self.assertEqual(machine.next_section_id, "section_001")

    def test_verify_next_rejects_hash_mismatch(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("hash_mismatch"))
        machine.recognize_manifest()
        machine.prefetch_current()
        machine.verify_current()
        machine.load_view_gate()
        machine.lock_view_gate()
        machine.enter_playback_ready()
        machine.prefetch_next()
        self.assertFalse(machine.verify_next())
        self.assertEqual(machine.fail_closed_events[-1].reason, FAIL_CLOSED_HASH_MISMATCH)

    def test_stage_next_requires_next_section_display_allowed(self) -> None:
        machine = self.make_ready_machine()
        machine.prefetch_next()
        self.assertFalse(machine.stage_next())
        self.assertEqual(machine.playback_state, STATE_FAIL_CLOSED)

    def test_transition_requires_hidden_gate_ready(self) -> None:
        machine = self.make_ready_machine()
        self.assertFalse(machine.begin_transition_blank())
        self.assertEqual(machine.playback_state, STATE_FAIL_CLOSED)

    def test_switch_visible_section_requires_blanking_active(self) -> None:
        machine = self.make_ready_machine()
        machine.prefetch_next()
        machine.verify_next()
        machine.stage_next()
        self.assertFalse(machine.switch_visible_section())
        self.assertEqual(machine.playback_state, STATE_FAIL_CLOSED)

    def test_park_old_section_adds_previous_section_to_reverse_buffer(self) -> None:
        machine = self.make_ready_machine()
        self.assertTrue(machine.step_forward())
        self.assertIn("section_000", machine.reverse_buffer_state.section_ids)

    def test_step_forward_performs_safe_transition_for_valid_next_section(self) -> None:
        machine = self.make_ready_machine()
        self.assertTrue(machine.step_forward())
        self.assertEqual(machine.current_section_id, "section_001")
        self.assertEqual(machine.unsafe_acceptance_count, 0)

    def test_step_forward_fails_closed_on_invalid_next_section(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        machine.insert_cartridge(build_sample_cartridge("hash_mismatch"))
        machine.recognize_manifest()
        machine.prefetch_current()
        machine.verify_current()
        machine.load_view_gate()
        machine.lock_view_gate()
        machine.enter_playback_ready()
        self.assertFalse(machine.step_forward())
        self.assertEqual(machine.playback_state, STATE_FAIL_CLOSED)

    def test_step_reverse_works_only_when_reverse_buffer_has_section(self) -> None:
        machine = self.make_ready_machine()
        self.assertFalse(machine.step_reverse())
        self.assertTrue(machine.step_forward())
        self.assertTrue(machine.step_reverse())

    def test_arbitrary_seek_outside_local_buffer_is_safely_denied(self) -> None:
        machine = self.make_ready_machine()
        self.assertFalse(machine.request_seek(section_id="section_999"))
        self.assertFalse(machine.seek_request_state.seek_available)
        self.assertEqual(machine.seek_request_state.denial_reason, "unsupported_or_not_in_local_buffer")

    def test_fail_closed_creates_fail_closed_decision(self) -> None:
        machine = AMCFPhysicalPlayerStateMachine()
        decision = machine.fail_closed("fail_closed_jam", "stop motion")
        self.assertEqual(decision.reason, "fail_closed_jam")
        self.assertEqual(len(machine.fail_closed_events), 1)

    def test_unsafe_acceptance_count_remains_zero(self) -> None:
        machine = self.make_ready_machine()
        machine.step_forward()
        self.assertEqual(machine.unsafe_acceptance_count, 0)

    def test_summary_says_software_control_simulator_only_and_no_hardware_validation_claimed(self) -> None:
        machine = self.make_ready_machine()
        summary = build_state_machine_summary_markdown(machine)
        self.assertIn("software/control simulator only", summary)
        self.assertIn("No physical hardware validation is claimed.", summary)
        self.assertIn("hardware validation claimed: no", summary)


if __name__ == "__main__":
    unittest.main(verbosity=2)
