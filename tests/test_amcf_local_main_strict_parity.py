from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_local_main_strict_parity import (  # noqa: E402
    build_static_parity_matrix,
    compare_local_public_outputs,
    default_paths,
    inventory_file_parity,
)
from amcf_local_main_test02 import TRACK_ORDER, make_tracks  # noqa: E402


class AmcfLocalMainStrictParityTests(unittest.TestCase):
    def test_default_paths_find_local_main(self) -> None:
        paths = default_paths(PACKAGE)
        self.assertEqual(paths.local_main_root.name, "Main")
        self.assertTrue(paths.local_main_root.exists())

    def test_inventory_classifies_local_main_files(self) -> None:
        rows = inventory_file_parity(default_paths(PACKAGE))
        by_name = {row["local_file"]: row for row in rows}
        self.assertIn("amcf_test02.py", by_name)
        self.assertEqual(by_name["RUN_TEST02.cmd"]["classification"], "PORTABLE_PUBLIC_WRAPPER")
        self.assertEqual(by_name["requirements.txt"]["classification"], "DEPENDENCY_POLICY_PORTED")
        self.assertEqual(by_name["amcf_config.example.json"]["classification"], "CONFIG_PORTED")
        self.assertEqual(by_name["test_archive_decode.py"]["classification"], "LOCAL_SCHEMA_CHECK_PORTED")
        self.assertTrue(by_name["amcf_test02.py"]["public_exists"])
        self.assertTrue(by_name["amcf_tracking_test03a.py"]["public_exists"])
        self.assertTrue(by_name["amcf_vnext.py"]["exact_hash_match"])
        self.assertTrue(by_name["amcf_virtual_hardware.py"]["exact_hash_match"])

    def test_static_parity_matrix_has_no_hardware_claims(self) -> None:
        rows = inventory_file_parity(default_paths(PACKAGE))
        matrix = build_static_parity_matrix(rows)
        statuses = {row["area"]: row["status"] for row in matrix}
        self.assertIn("direct copied core files", statuses)
        self.assertEqual(statuses["machine wrappers and generated outputs"], "PUBLIC_PORTABLE_WRAPPERS")

    def test_public_local_main_module_preserves_track_taxonomy(self) -> None:
        self.assertEqual(len(TRACK_ORDER), 8)
        tracks = make_tracks()
        self.assertEqual(set(tracks), set(TRACK_ORDER))
        self.assertIn("WATERFALL_COLUMN", tracks)

    def test_output_comparison_requires_local_and_public_artifacts(self) -> None:
        comparison = compare_local_public_outputs(
            {
                "archive_exists": True,
                "zip_exists": True,
                "viewer_exists": True,
                "reconstructed_video_exists": True,
                "frame_count": 4,
                "track_ids": ["WATERFALL_COLUMN"],
                "under_source_size_ceiling": True,
                "elapsed_seconds": 2.0,
                "unsafe_acceptance_count": 0,
            },
            {
                "video_archive_exists": True,
                "component_archive_exists": True,
                "decoded_video_exists": True,
                "deliverable_zip_exists": True,
                "frame_count": 4,
                "track_taxonomy_count": 8,
                "track_ids": ["WATERFALL_COLUMN"],
                "under_source_size_ceiling": True,
                "elapsed_seconds": 1.0,
                "unsafe_acceptance_count": 0,
            },
        )
        self.assertTrue(comparison["functional_parity_passed"])
        self.assertFalse(comparison["strict_identity_passed"])
        self.assertFalse(comparison["same_functionality_performance_and_everything_else"])
        self.assertFalse(comparison["byte_identical_outputs"])
        self.assertTrue(comparison["performance"]["public_not_slower_than_local"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
