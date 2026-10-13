from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_optical_flow_tracking import build_optical_flow_track_report, optical_flow_dependency_status  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class AmcfOpticalFlowTrackingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_flow_"))
        self.source = self.tmp / "source"
        generate_source_frames(self.source, frame_count=5, width=64, height=40, fps=5)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_dependency_status_reports_optional_tools(self) -> None:
        status = optical_flow_dependency_status()
        self.assertIn("opencv_available", status)
        self.assertIn("numpy_available", status)

    @unittest.skipUnless(importlib.util.find_spec("cv2") is not None and importlib.util.find_spec("numpy") is not None, "OpenCV/numpy not available")
    def test_build_optical_flow_track_report(self) -> None:
        report = build_optical_flow_track_report(self.source / "source_frames_manifest.json", self.tmp / "flow")
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["frame_count"], 5)
        self.assertEqual(report["track_count"], 1)
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary"]["hardware_validation_claimed"])
        self.assertGreater(report["frames"][1]["flow_sample_count"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
