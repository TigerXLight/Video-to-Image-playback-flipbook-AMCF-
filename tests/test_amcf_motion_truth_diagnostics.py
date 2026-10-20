from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from amcf_motion_truth_diagnostics import Zone, analyze_pair, classify_zone, residual_motion, score_zones


try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


@unittest.skipUnless(cv2 is not None and np is not None, "optional OpenCV/NumPy unavailable")
class MotionTruthDiagnosticsTests(unittest.TestCase):
    def test_local_motion_is_detected_and_overlay_rendered(self):
        rng = np.random.default_rng(9)
        previous = rng.integers(0, 80, (64, 96, 3), dtype=np.uint8)
        current = previous.copy()
        cv2.rectangle(current, (40, 20), (54, 36), (250, 250, 250), -1)
        zones = [Zone("moving_zone", "high_local_motion", (35, 15, 25, 27)),
                 Zone("static_zone", "camera_motion_only_or_static", (2, 2, 20, 20))]
        report, overlay = analyze_pair(previous, current, zones)
        self.assertGreater(report["motion_mask_pixels"], 0)
        self.assertGreater(report["zones"][0]["active_motion_fraction"],
                           report["zones"][1]["active_motion_fraction"])
        self.assertEqual(overlay.shape, current.shape)
        self.assertTrue(report["human_review_required"])
        self.assertFalse(report["final_tracking_proof_claimed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["hardware_validation_claimed"])

    def test_known_translation_removes_background_motion(self):
        rng = np.random.default_rng(11)
        previous = rng.integers(0, 255, (64, 96, 3), dtype=np.uint8)
        matrix = np.array([[1, 0, 2], [0, 1, 0]], dtype=np.float32)
        current = cv2.warpAffine(previous, matrix, (96, 64), borderMode=cv2.BORDER_REFLECT)
        gray, mask = residual_motion(previous, current, matrix)
        self.assertEqual(int(np.count_nonzero(gray)), 0)
        self.assertEqual(int(np.count_nonzero(mask)), 0)

    def test_invalid_zone_rejected(self):
        gray = np.zeros((8, 8), dtype=np.uint8)
        with self.assertRaises(ValueError):
            score_zones(gray, gray, [Zone("outside", "high_local_motion", (6, 6, 4, 4))], 2)

    def test_original_03m_zone_thresholds(self):
        self.assertEqual(classify_zone("intermittent_small_object_motion", 0.02, 0),
                         "intermittent_small_object_motion")
        self.assertEqual(classify_zone("high_local_motion", 0.0, 0),
                         "camera_motion_only_or_static")


if __name__ == "__main__":
    unittest.main()
