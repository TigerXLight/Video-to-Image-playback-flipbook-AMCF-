from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive  # noqa: E402
from amcf_component_event_viewer import build_component_event_viewer  # noqa: E402
from amcf_deliverable_package import build_deliverable_package, build_track_taxonomy_report  # noqa: E402
from amcf_quality_metrics import compare_ppm_frame_folders  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class AmcfDeliverablePackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_deliverable_"))
        self.source_dir = self.tmp / "source"
        generate_source_frames(self.source_dir, frame_count=4, width=48, height=32, fps=4)
        self.manifest_path = self.source_dir / "source_frames_manifest.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _build_inputs(self) -> tuple[Path, dict, dict, dict]:
        archive_path = self.tmp / "component_event_archive.amcf.zip"
        archive = build_component_event_archive(self.manifest_path, archive_path, prefer_webp=False)
        decoded = decode_component_event_archive(archive_path, self.tmp / "decoded")
        quality = compare_ppm_frame_folders(self.source_dir / "frames", Path(decoded["decoded_frames_dir"]))
        viewer = build_component_event_viewer(
            archive_report=archive,
            decoded_report=decoded,
            quality_report=quality,
            output_dir=self.tmp / "viewer",
        )
        return archive_path, decoded, quality, viewer

    def test_track_taxonomy_carries_local_main_categories_without_hardware_claims(self) -> None:
        report = build_track_taxonomy_report()
        self.assertTrue(report["ok"])
        self.assertIn("WATERFALL_COLUMN", {track["track_id"] for track in report["tracks"]})
        self.assertIn("FOREGROUND_TREE_LEFT", {track["track_id"] for track in report["tracks"]})
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(report["claim_boundary"]["physical_level_5_claimed"])
        self.assertFalse(report["claim_boundary"]["manufactured_player_claimed"])

    def test_deliverable_package_contains_archive_comparison_frames_viewer_and_zip(self) -> None:
        archive_path, decoded, quality, _viewer = self._build_inputs()
        result = build_deliverable_package(
            archive_path=archive_path,
            source_frames_dir=self.source_dir / "frames",
            decoded_frames_dir=Path(decoded["decoded_frames_dir"]),
            quality_report=quality,
            viewer_dir=self.tmp / "viewer",
            output_dir=self.tmp / "deliverable",
            fps=4,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["comparison_frame_count"], 4)
        self.assertEqual(result["track_taxonomy_count"], 8)
        self.assertEqual(result["unsafe_acceptance_count"], 0)
        self.assertFalse(result["claim_boundary"]["hardware_validation_claimed"])
        self.assertTrue(Path(result["zip_path"]).exists())
        with zipfile.ZipFile(result["zip_path"], "r") as zf:
            names = set(zf.namelist())
        self.assertIn("deliverable_manifest.json", names)
        self.assertIn("track_taxonomy.json", names)
        self.assertIn("comparison_frames/comparison_frame_000.ppm", names)
        self.assertIn("viewer/index.html", names)
        self.assertIn(archive_path.name, names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
