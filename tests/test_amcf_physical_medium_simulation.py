import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.amcf_physical_medium_simulation import (
    build_report,
    sample_non_ideal_recovery_cases,
    summarize_recovery,
    vertical_stack_equivalence,
    write_report,
)


class PhysicalMediumSimulationTests(unittest.TestCase):
    def test_vertical_stack_preserves_amcf_playback(self):
        equivalence = vertical_stack_equivalence()
        self.assertTrue(equivalence.preserves_amcf_playback)
        self.assertEqual(equivalence.frames_compared, 288)
        self.assertEqual(equivalence.amcf_vs_physical_mean_mae, 0.0)

    def test_non_ideal_cases_recover_without_unsafe_acceptance(self):
        summary = summarize_recovery(sample_non_ideal_recovery_cases())
        self.assertTrue(summary["all_cases_recovered"])
        self.assertEqual(summary["highest_recovered_severity"], "severe")
        self.assertEqual(summary["unsafe_acceptance_count"], 0)

    def test_report_preserves_claim_boundaries(self):
        report = build_report()
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(report["claim_boundary"]["physical_level5_claimed"])
        self.assertFalse(report["claim_boundary"]["manufactured_player_claimed"])
        self.assertFalse(report["claim_boundary"]["real_sensor_validation_claimed"])

    def test_write_report_outputs_json_and_summary(self):
        with TemporaryDirectory() as tmp:
            report = write_report(Path(tmp))
            self.assertTrue(report["final_passed"])
            self.assertTrue((Path(tmp) / "physical_medium_simulation_report.json").exists())
            self.assertTrue((Path(tmp) / "PHYSICAL_MEDIUM_SIMULATION_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main()
