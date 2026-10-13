from __future__ import annotations

import json
import importlib.util
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_component_event_archive import AMCF_COMPONENT_EVENT_SCHEMA, build_component_event_archive, decode_component_event_archive, optional_dependency_status  # noqa: E402
from amcf_component_event_viewer import build_component_event_viewer  # noqa: E402
from amcf_quality_metrics import compare_ppm_frame_folders  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class AmcfComponentEventArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_component_archive_"))
        self.source = self.tmp / "source"
        generate_source_frames(self.source, frame_count=5, width=48, height=32, fps=5)
        self.manifest = self.source / "source_frames_manifest.json"
        self.archive = self.tmp / "archive.amcf.zip"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_component_event_archive_with_ppm_fallback(self) -> None:
        result = build_component_event_archive(self.manifest, self.archive, prefer_webp=False)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["amcf_schema"], AMCF_COMPONENT_EVENT_SCHEMA)
        self.assertGreater(result["event_count"], 0)
        self.assertEqual(result["payload_format"], "ppm_p6")
        self.assertEqual(result["unsafe_acceptance_count"], 0)
        self.assertFalse(result["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(result["claim_boundary"]["physical_level_5_claimed"])
        self.assertFalse(result["claim_boundary"]["manufactured_player_claimed"])

    def test_manifest_contains_component_events_and_dependency_status(self) -> None:
        build_component_event_archive(self.manifest, self.archive, prefer_webp=False)
        with zipfile.ZipFile(self.archive, "r") as zf:
            manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
        self.assertEqual(manifest["archive_payload_kind"], "component_event_payloads")
        self.assertTrue(manifest["capabilities"]["component_event_archive"])
        self.assertTrue(manifest["capabilities"]["timestamped_updates"])
        self.assertTrue(manifest["capabilities"]["bounding_box_changed_regions"])
        self.assertFalse(manifest["capabilities"]["opencv_segmentation"])
        self.assertIn("pillow_available", manifest["dependency_status"])
        self.assertEqual(manifest["unsafe_acceptance_count"], 0)

    def test_decode_reconstructs_source_frames(self) -> None:
        build_component_event_archive(self.manifest, self.archive, prefer_webp=False)
        decoded = decode_component_event_archive(self.archive, self.tmp / "decoded")
        self.assertTrue(decoded["ok"])
        self.assertEqual(decoded["frame_count"], 5)
        quality = compare_ppm_frame_folders(self.source / "frames", Path(decoded["decoded_frames_dir"]))
        self.assertTrue(quality["ok"], quality)

    def test_size_ceiling_status_is_reported(self) -> None:
        result = build_component_event_archive(self.manifest, self.archive, source_size_ceiling_bytes=1, prefer_webp=False)
        ceiling = result["archive_size_ceiling"]
        self.assertEqual(ceiling["ceiling_bytes"], 1)
        self.assertFalse(ceiling["under_source_size_ceiling"])

    def test_optional_dependency_status_reports_without_claiming_features(self) -> None:
        status = optional_dependency_status()
        self.assertIn("pillow_available", status)
        self.assertIn("opencv_available", status)
        self.assertIn("skimage_available", status)

    @unittest.skipUnless(importlib.util.find_spec("PIL") is not None, "Pillow not available")
    def test_webp_payload_path_when_pillow_available(self) -> None:
        result = build_component_event_archive(self.manifest, self.archive, prefer_webp=True)
        self.assertEqual(result["payload_format"], "webp_lossless")
        self.assertTrue(result["dependency_status"]["webp_payloads_used"])
        decoded = decode_component_event_archive(self.archive, self.tmp / "decoded_webp")
        quality = compare_ppm_frame_folders(self.source / "frames", Path(decoded["decoded_frames_dir"]))
        self.assertTrue(quality["ok"], quality)

    @unittest.skipUnless(importlib.util.find_spec("cv2") is not None and importlib.util.find_spec("numpy") is not None, "OpenCV/numpy not available")
    def test_opencv_changed_region_segmentation_path(self) -> None:
        result = build_component_event_archive(self.manifest, self.archive, prefer_webp=False, segmentation_mode="opencv_changed_region")
        self.assertEqual(result["segmentation_mode"], "opencv_changed_region")
        self.assertTrue(result["dependency_status"]["opencv_segmentation_used"])
        with zipfile.ZipFile(self.archive, "r") as zf:
            manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
        self.assertTrue(manifest["capabilities"]["opencv_segmentation"])
        self.assertEqual(manifest["events"][0]["segmentation"]["strategy"], "opencv_changed_region")

    def test_viewer_package_is_static_inspection_only(self) -> None:
        archive = build_component_event_archive(self.manifest, self.archive, prefer_webp=False)
        decoded = decode_component_event_archive(self.archive, self.tmp / "decoded_viewer")
        quality = compare_ppm_frame_folders(self.source / "frames", Path(decoded["decoded_frames_dir"]))
        viewer = build_component_event_viewer(
            archive_report=archive,
            decoded_report=decoded,
            quality_report=quality,
            output_dir=self.tmp / "viewer",
        )
        self.assertTrue(viewer["ok"])
        self.assertTrue(Path(viewer["viewer_html"]).exists())
        self.assertFalse(viewer["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(viewer["claim_boundary"]["viewer_is_final_ui"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
