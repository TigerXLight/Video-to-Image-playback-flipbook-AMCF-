from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_test02_diagnostic_viewer import (  # noqa: E402
    build_test02_diagnostic_viewer,
    build_track_taxonomy,
    load_tracks_manifest,
    summarize_tracks_manifest,
)
from run_amcf_test02_diagnostic_viewer_demo import synthetic_tracks_manifest  # noqa: E402


class AmcfTest02DiagnosticViewerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_test02_viewer_"))
        self.manifest_path = self.tmp / "tracks_manifest.json"
        self.manifest_path.write_text(json.dumps(synthetic_tracks_manifest(), indent=2), encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_load_tracks_manifest_validates_shape(self) -> None:
        manifest = load_tracks_manifest(self.manifest_path)
        self.assertEqual(len(manifest["frames"]), 3)
        bad = self.tmp / "bad.json"
        bad.write_text(json.dumps({"frames": [{"frame_index": 0}]}), encoding="utf-8")
        with self.assertRaises(ValueError):
            load_tracks_manifest(bad)

    def test_track_taxonomy_preserves_parent_child_and_updates(self) -> None:
        taxonomy = {row["track_id"]: row for row in build_track_taxonomy(synthetic_tracks_manifest())}
        self.assertEqual(taxonomy["MIST_SPRAY"]["parent_id"], "WATERFALL_COLUMN")
        self.assertEqual(taxonomy["WATERFALL_COLUMN"]["component_update_count"], 2)
        self.assertEqual(taxonomy["MIST_SPRAY"]["component_update_count"], 1)
        self.assertGreater(taxonomy["WATERFALL_COLUMN"]["max_motion_p95_px_s"], 200)

    def test_summary_reports_diagnostic_contract(self) -> None:
        summary = summarize_tracks_manifest(synthetic_tracks_manifest())
        self.assertEqual(summary["track_count"], 2)
        self.assertTrue(summary["has_parent_child_taxonomy"])
        self.assertTrue(summary["has_motion_metrics"])
        self.assertEqual(summary["unsafe_acceptance_count"], 0)
        self.assertFalse(summary["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(summary["claim_boundary"]["physical_level_5_claimed"])
        self.assertFalse(summary["claim_boundary"]["manufactured_player_claimed"])

    def test_build_viewer_writes_same_clock_contour_controls(self) -> None:
        report = build_test02_diagnostic_viewer(
            tracks_manifest_path=self.manifest_path,
            output_dir=self.tmp / "viewer",
        )
        self.assertTrue(report["ok"])
        self.assertEqual(report["track_count"], 2)
        html = Path(report["viewer_html"]).read_text(encoding="utf-8")
        self.assertIn("contours", html)
        self.assertIn("difference", html)
        self.assertIn("Export frame data", html)
        copied = json.loads(Path(report["tracks_manifest"]).read_text(encoding="utf-8"))
        self.assertEqual(copied["frames"][0]["tracks"][1]["track_id"], "MIST_SPRAY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
