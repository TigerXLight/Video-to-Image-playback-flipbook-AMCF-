import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.amcf_semantic_level5_proof import (
    accepted_semantic_level5_runs,
    build_semantic_level5_report,
    semantic_proof_runs,
    write_semantic_level5_report,
)


class SemanticLevel5ProofTests(unittest.TestCase):
    def test_accepts_only_controlled_and_hoot_vectors_as_level5(self):
        accepted = [run for run in accepted_semantic_level5_runs() if run.status == "SEMANTIC_LEVEL5_ACCEPTED"]
        self.assertEqual({run.run_name for run in accepted}, {
            "AMCF_CONTROLLED_LOST_RECOVERED_LEVEL5_PROOF",
            "AMCF_HOOT_REAL_WORLD_LOST_RECOVERED_LEVEL5_SOLVER",
        })

    def test_pre_level5_runs_remain_unclaimed(self):
        unclaimed = [run for run in semantic_proof_runs() if run.status == "NOT_LEVEL5"]
        self.assertGreaterEqual(len(unclaimed), 4)
        self.assertTrue(all(not run.semantic_level5_claimed for run in unclaimed))

    def test_report_preserves_physical_claim_boundaries(self):
        report = build_semantic_level5_report()
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["semantic_level5_vector_count"], 2)
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(report["claim_boundary"]["physical_level5_claimed"])
        self.assertFalse(report["claim_boundary"]["manufactured_player_claimed"])
        self.assertFalse(report["claim_boundary"]["physical_player_proof_claimed"])

    def test_write_report_outputs_json_and_summary(self):
        with TemporaryDirectory() as tmp:
            report = write_semantic_level5_report(Path(tmp))
            self.assertTrue(report["final_passed"])
            self.assertTrue((Path(tmp) / "semantic_level5_proof_report.json").exists())
            self.assertTrue((Path(tmp) / "SEMANTIC_LEVEL5_PROOF_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main()
