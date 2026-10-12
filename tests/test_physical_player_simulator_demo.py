from __future__ import annotations

import sys
import unittest
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_integrated_demo_reports import (  # noqa: E402
    build_integrated_simulation_summary,
    build_integrated_summary_markdown,
    build_mechanism_profile_phase,
    run_fail_closed_phase,
    run_forward_playback_phase,
    run_reverse_seek_phase,
)


class PhysicalPlayerSimulatorDemoTests(unittest.TestCase):
    def test_integrated_demo_can_build_mechanism_profile_phase(self) -> None:
        phase = build_mechanism_profile_phase()
        self.assertTrue(phase["passed"])

    def test_default_mechanism_profile_is_folded_ab_motor_encoder_baseline(self) -> None:
        phase = build_mechanism_profile_phase()
        self.assertEqual(phase["default_profile_id"], "folded_ab_motor_encoder_baseline")

    def test_hardware_validated_profiles_count_is_zero(self) -> None:
        phase = build_mechanism_profile_phase()
        self.assertEqual(phase["hardware_validated_profiles_count"], 0)

    def test_physical_level_5_claimed_profiles_count_is_zero(self) -> None:
        phase = build_mechanism_profile_phase()
        self.assertEqual(phase["physical_level_5_claimed_profiles_count"], 0)

    def test_integrated_demo_can_run_forward_playback_phase(self) -> None:
        _machine, phase = run_forward_playback_phase()
        self.assertTrue(phase["passed"])

    def test_forward_playback_phase_records_at_least_one_transition(self) -> None:
        _machine, phase = run_forward_playback_phase()
        self.assertGreaterEqual(phase["forward_transition_count"], 1)

    def test_integrated_demo_can_run_fail_closed_phase(self) -> None:
        phase = run_fail_closed_phase()
        self.assertTrue(phase["passed"])

    def test_fail_closed_phase_records_at_least_one_fail_closed_event(self) -> None:
        phase = run_fail_closed_phase()
        self.assertGreaterEqual(phase["fail_closed_event_count"], 1)

    def test_integrated_demo_can_run_reverse_seek_phase(self) -> None:
        _machine, phase = run_reverse_seek_phase()
        self.assertTrue(phase["passed"])

    def test_reverse_seek_phase_records_reverse_success_or_safe_denial(self) -> None:
        _machine, phase = run_reverse_seek_phase()
        self.assertGreaterEqual(phase["reverse_successes"] + phase["reverse_denials"], 1)

    def test_arbitrary_seek_denial_is_recorded(self) -> None:
        _machine, phase = run_reverse_seek_phase()
        self.assertGreaterEqual(phase["arbitrary_seek_denied_count"], 1)

    def test_unsafe_acceptance_audit_passes(self) -> None:
        summary = build_integrated_simulation_summary()
        self.assertTrue(summary["unsafe_acceptance_audit"]["passed"])

    def test_unsafe_acceptance_count_is_zero(self) -> None:
        summary = build_integrated_simulation_summary()
        self.assertEqual(summary["unsafe_acceptance_audit"]["unsafe_acceptance_count"], 0)

    def test_unified_report_has_software_control_simulator_only_true(self) -> None:
        summary = build_integrated_simulation_summary()
        self.assertTrue(summary["software_control_simulator_only"])

    def test_unified_report_has_hardware_validation_claimed_false(self) -> None:
        summary = build_integrated_simulation_summary()
        self.assertFalse(summary["hardware_validation_claimed"])

    def test_unified_report_has_physical_level_5_claimed_false(self) -> None:
        summary = build_integrated_simulation_summary()
        self.assertFalse(summary["physical_level_5_claimed"])

    def test_unified_report_has_manufactured_player_claimed_false(self) -> None:
        summary = build_integrated_simulation_summary()
        self.assertFalse(summary["manufactured_player_claimed"])

    def test_final_passed_true_for_deterministic_nominal_integrated_run(self) -> None:
        summary = build_integrated_simulation_summary()
        self.assertTrue(summary["final_passed"])

    def test_summary_markdown_states_no_hardware_validation_claimed(self) -> None:
        summary = build_integrated_simulation_summary()
        markdown = build_integrated_summary_markdown(summary)
        self.assertIn("hardware validation claimed: false", markdown)


if __name__ == "__main__":
    unittest.main(verbosity=2)
