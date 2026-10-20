from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import amcf_material_coupon_analysis as coupon  # noqa: E402


class MaterialCouponAnalysisTests(unittest.TestCase):
    def test_synthetic_coupon_analysis_returns_safe_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = coupon.analyze_synthetic_coupon(tmp)
            self.assertTrue(result["ok"])
            self.assertEqual(result["unsafe_acceptance_count"], 0)
            self.assertFalse(result["claim_boundary"]["hardware_validation_claimed"])
            self.assertFalse(result["claim_boundary"]["physical_level_5_claimed"])
            self.assertFalse(result["claim_boundary"]["manufactured_player_claimed"])
            self.assertTrue(Path(result["paths"]["json"]).exists())
            self.assertTrue(Path(result["paths"]["csv"]).exists())

    def test_analysis_result_contains_expected_scores(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image = coupon.create_synthetic_coupon_ppm(Path(tmp) / "coupon.ppm")
            result = coupon.analyze_coupon_image(image, coupon_type="A")
            self.assertIn("registration_detection_score", result)
            self.assertIn("metadata_hash_lane_score", result)
            self.assertIn("fail_closed_decision", result)
            self.assertFalse(result["unsafe_acceptance_flag"])
            self.assertEqual(result["unsafe_acceptance_count"], 0)

    def test_missing_pillow_fails_closed(self) -> None:
        with mock.patch.object(coupon, "Image", None):
            result = coupon.analyze_coupon_image("missing_or_unread_image.png")
        self.assertTrue(result["fail_closed_decision"])
        self.assertFalse(result["unsafe_acceptance_flag"])
        self.assertEqual(result["unsafe_acceptance_count"], 0)

    def test_demo_runs(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "demo" / "run_amcf_material_coupon_analysis_demo.py")],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["ok"])
        self.assertEqual(data["unsafe_acceptance_count"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
