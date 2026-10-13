from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
import importlib.util
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_quality_metrics import compare_ppm_frame_folders, compare_ppm_frames, mean_absolute_error_rgb, read_ppm, write_ppm  # noqa: E402


class AmcfQualityMetricsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_quality_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_ppm_roundtrip(self) -> None:
        pixels = bytes([1, 2, 3, 4, 5, 6] * 2)
        path = self.tmp / "frame_000.ppm"
        write_ppm(path, 2, 2, pixels)
        width, height, loaded = read_ppm(path)
        self.assertEqual((width, height), (2, 2))
        self.assertEqual(loaded, pixels)

    def test_mean_absolute_error(self) -> None:
        self.assertEqual(mean_absolute_error_rgb(bytes([0, 10]), bytes([10, 10])), 5.0)

    def test_compare_identical_frames_passes(self) -> None:
        first = self.tmp / "first.ppm"
        second = self.tmp / "second.ppm"
        pixels = bytes([20, 30, 40] * 4)
        write_ppm(first, 2, 2, pixels)
        write_ppm(second, 2, 2, pixels)
        report = compare_ppm_frames(first, second)
        self.assertTrue(report["ok"])
        self.assertEqual(report["mean_absolute_error"], 0.0)
        self.assertFalse(report["ssim_available"])

    def test_compare_frame_folders(self) -> None:
        expected = self.tmp / "expected"
        actual = self.tmp / "actual"
        expected.mkdir()
        actual.mkdir()
        pixels = bytes([9, 8, 7] * 4)
        write_ppm(expected / "frame_000.ppm", 2, 2, pixels)
        write_ppm(actual / "frame_000.ppm", 2, 2, pixels)
        report = compare_ppm_frame_folders(expected, actual)
        self.assertTrue(report["ok"])
        self.assertEqual(report["compared_frame_count"], 1)

    @unittest.skipUnless(importlib.util.find_spec("skimage") is not None and importlib.util.find_spec("numpy") is not None, "skimage/numpy not available")
    def test_ssim_available_when_optional_dependency_exists(self) -> None:
        first = self.tmp / "first_ssim.ppm"
        second = self.tmp / "second_ssim.ppm"
        pixels = bytes([20, 30, 40] * 64)
        write_ppm(first, 8, 8, pixels)
        write_ppm(second, 8, 8, pixels)
        report = compare_ppm_frames(first, second)
        self.assertTrue(report["ssim_available"])
        self.assertAlmostEqual(float(report["ssim"]), 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
