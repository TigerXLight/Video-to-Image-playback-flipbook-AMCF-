import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.amcf_release_candidate_acceptance import (
    build_release_candidate_acceptance_report,
    release_candidate_phases,
    write_release_candidate_acceptance_report,
)


class ReleaseCandidateAcceptanceTests(unittest.TestCase):
    def test_release_candidate_phase_chain_is_complete(self):
        phases = release_candidate_phases()
        self.assertEqual(len(phases), 8)
        names = {phase.run_name for phase in phases}
        self.assertIn("AMCF_ACCEPTANCE_HARNESS_AND_CI_STYLE_REGRESSION", names)
        self.assertIn("AMCF_ARCHIVE_WRITER_READER_INTEGRATION", names)
        self.assertIn("AMCF_RELEASE_CANDIDATE_REVIEW_AND_SIGNOFF", names)
        self.assertTrue(all(phase.status == "READY" for phase in phases))

    def test_acceptance_counts_and_claim_boundaries(self):
        report = build_release_candidate_acceptance_report()
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["valid_vectors_passed"], 9)
        self.assertEqual(report["invalid_vectors_rejected"], 9)
        self.assertEqual(report["tiny_archive_count"], 6)
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(report["claim_boundary"]["physical_level5_claimed"])
        self.assertFalse(report["claim_boundary"]["manufactured_player_claimed"])
        self.assertFalse(report["claim_boundary"]["semantic_level5_claimed_by_release_package"])

    def test_generated_release_zip_is_not_ported(self):
        report = build_release_candidate_acceptance_report()
        self.assertFalse(report["release_zip_ported"])
        self.assertFalse(report["generated_release_output_committed"])
        self.assertEqual(report["level5_claims_in_release_candidate"], [])

    def test_write_report_outputs_json_and_summary(self):
        with TemporaryDirectory() as tmp:
            report = write_release_candidate_acceptance_report(Path(tmp))
            self.assertTrue(report["final_passed"])
            self.assertTrue((Path(tmp) / "release_candidate_acceptance_report.json").exists())
            self.assertTrue((Path(tmp) / "RELEASE_CANDIDATE_ACCEPTANCE_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main()
