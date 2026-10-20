import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from amcf_residual_visual_acceptance import assess_candidate, visual_gate


class ResidualVisualAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.metric = {"frame_count_match": True, "fps_match": True,
                       "resolution_match": True, "mae": 2.0, "psnr": 40.0,
                       "temporal_difference_similarity": 1.0}

    def assess(self, metric=None, **kwargs):
        return assess_candidate(metric or self.metric, self.metric,
                                compressed_bytes=90, fullrate_component_bytes=200,
                                source_video_bytes=50, **kwargs)

    def test_pass_keeps_stream_and_source_size_distinct(self):
        report = self.assess()
        self.assertTrue(report["final_passed"])
        self.assertTrue(report["compression_proof_claimed"])
        self.assertFalse(report["compression_accounting"]["residual_stream_smaller_than_source_video"])
        self.assertEqual(report["compression_accounting"]["proof_scope"],
                         "residual_stream_vs_fullrate_component_estimate_only")

    def test_technical_mismatch_and_missing_metric_reject(self):
        wrong = dict(self.metric, frame_count_match=False)
        self.assertEqual(visual_gate(wrong, self.metric)["status"], "REJECTED")
        missing = dict(self.metric)
        missing.pop("psnr")
        self.assertEqual(visual_gate(missing, self.metric)["status"], "REJECTED")

    def test_temporal_uncertainty_needs_human_review(self):
        report = self.assess(dict(self.metric, temporal_difference_similarity=1.1))
        self.assertEqual(report["visual_gate"]["status"], "NEEDS_HUMAN_REVIEW")
        self.assertFalse(report["accepted_automatically"])
        self.assertTrue(report["human_review_required"])

    def test_metric_regression_stays_rejected_with_artifact_warning(self):
        report = self.assess(dict(self.metric, psnr=35.0), artifact_warning=True)
        self.assertEqual(report["visual_gate"]["status"], "REJECTED")
        self.assertFalse(report["compression_proof_claimed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["hardware_validation_claimed"])
        self.assertFalse(report["physical_level_5_claimed"])
        self.assertFalse(report["manufactured_player_claimed"])

    def test_suspected_artifact_blocks_automatic_acceptance(self):
        report = self.assess(artifact_warning=True)
        self.assertTrue(report["compression_proof_claimed"])
        self.assertTrue(report["human_review_required"])
        self.assertFalse(report["final_passed"])


if __name__ == "__main__":
    unittest.main()
