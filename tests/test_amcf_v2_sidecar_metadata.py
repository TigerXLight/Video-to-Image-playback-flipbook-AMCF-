from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_v2_sidecar_metadata import (  # noqa: E402
    SAFE_CLAIM_FLAGS,
    V2SidecarArchiveReader,
    build_demo_sidecar_archive,
    validate_sidecar_archive,
)


class AmcfV2SidecarMetadataTests(unittest.TestCase):
    def test_demo_sidecar_archive_builds_and_validates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "demo.amcfv2.zip"
            build_report = build_demo_sidecar_archive(archive, frame_count=4)
            validation_report = validate_sidecar_archive(archive)

        self.assertTrue(build_report["final_passed"])
        self.assertTrue(validation_report["final_passed"])
        self.assertEqual(validation_report["frame_count"], 4)
        self.assertEqual(validation_report["unsafe_acceptance_count"], 0)
        self.assertFalse(validation_report["hardware_validation_claimed"])
        self.assertFalse(validation_report["physical_level_5_claimed"])
        self.assertFalse(validation_report["manufactured_player_claimed"])

    def test_reader_exposes_frames_regions_and_lifespans(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "demo.amcfv2.zip"
            build_demo_sidecar_archive(archive, frame_count=5)
            with V2SidecarArchiveReader(archive) as reader:
                self.assertEqual(reader.list_frames(), [0, 1, 2, 3, 4])
                self.assertGreaterEqual(len(reader.regions_for_frame(1)), 1)
                lifespans = reader.proxy_region_lifespan()
                self.assertIn("proxy_region_a", lifespans)
                self.assertTrue(reader.verify_claim_flags_false())
                self.assertTrue(reader.payload_hashes_match())

    def test_claim_flags_are_present_and_false(self) -> None:
        self.assertTrue(SAFE_CLAIM_FLAGS)
        self.assertTrue(all(value is False for value in SAFE_CLAIM_FLAGS.values()))
        self.assertIn("hardware_validation_claimed", SAFE_CLAIM_FLAGS)
        self.assertIn("physical_level_5_claimed", SAFE_CLAIM_FLAGS)
        self.assertIn("manufactured_player_claimed", SAFE_CLAIM_FLAGS)

    def test_missing_required_entry_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "bad.amcfv2.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("manifest/native_manifest_14J.json", json.dumps({"claim_flags": SAFE_CLAIM_FLAGS}))
            with V2SidecarArchiveReader(archive) as reader:
                report = reader.summarize()

        self.assertFalse(report["final_passed"])
        self.assertGreater(len(report["missing_required_entries"]), 0)
        self.assertEqual(report["unsafe_acceptance_count"], 1)


if __name__ == "__main__":
    unittest.main()
