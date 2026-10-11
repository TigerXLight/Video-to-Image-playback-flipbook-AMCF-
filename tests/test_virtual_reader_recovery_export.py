from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_digital_encoder import encode_source_frames  # noqa: E402
from amcf_digital_validator import validate_amcf_archive  # noqa: E402
from amcf_physical_carrier import generate_physical_carrier_from_amcf_archive, validate_physical_carrier_package  # noqa: E402
from amcf_virtual_carrier_reader import (  # noqa: E402
    read_physical_carrier_package,
    recover_amcf_from_carrier_package,
    validate_recovered_amcf_state,
)
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class VirtualReaderRecoveryExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_recovery_"))
        self.source_root = self.tmp / "source_frames"
        self.archive = self.tmp / "sample_video_source.amcf.zip"
        self.carrier_root = self.tmp / "carrier_package"
        self.recovery_root = self.tmp / "recovery"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def make_package(self) -> None:
        generate_source_frames(self.source_root)
        encode_source_frames(self.source_root / "source_frames_manifest.json", self.archive)
        self.assertTrue(validate_amcf_archive(self.archive)["ok"])
        generate_physical_carrier_from_amcf_archive(self.archive, self.carrier_root)
        self.assertTrue(validate_physical_carrier_package(self.carrier_root)["ok"])

    def recover(self) -> dict:
        self.make_package()
        return recover_amcf_from_carrier_package(self.carrier_root, self.recovery_root, self.archive)

    def test_source_frames_generate(self) -> None:
        manifest = generate_source_frames(self.source_root)
        self.assertEqual(manifest["frame_count"], 8)

    def test_amcf_archive_creates_and_validates(self) -> None:
        generate_source_frames(self.source_root)
        encode_source_frames(self.source_root / "source_frames_manifest.json", self.archive)
        self.assertTrue(validate_amcf_archive(self.archive)["ok"])

    def test_physical_carrier_package_creates_and_validates(self) -> None:
        self.make_package()
        self.assertTrue(validate_physical_carrier_package(self.carrier_root)["ok"])

    def test_virtual_reader_reads_carrier_sections(self) -> None:
        self.make_package()
        result = read_physical_carrier_package(self.carrier_root)
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.section_count, 8)

    def test_recovered_amcf_state_exists(self) -> None:
        result = self.recover()
        self.assertTrue(result["ok"], result["errors"])
        self.assertTrue((self.recovery_root / "recovered_amcf_manifest.json").exists())

    def test_recovered_frame_count_matches_source_frame_count(self) -> None:
        result = self.recover()
        self.assertEqual(result["recovered_frame_count"], 8)

    def test_recovered_hashes_match_original_frame_hashes(self) -> None:
        self.recover()
        recovered = json.loads((self.recovery_root / "recovered_amcf_manifest.json").read_text(encoding="utf-8"))
        source_manifest = json.loads((self.source_root / "source_frames_manifest.json").read_text(encoding="utf-8"))
        source_hashes = [entry["sha256"] for entry in source_manifest["frame_entries"]]
        recovered_hashes = [entry["sha256"] for entry in recovered["recovered_frame_entries"]]
        self.assertEqual(recovered_hashes, source_hashes)

    def test_exported_recovered_frames_exist(self) -> None:
        self.recover()
        frames = sorted((self.recovery_root / "recovered_frames").glob("*.ppm"))
        self.assertEqual(len(frames), 8)

    def test_validator_passes_valid_recovery(self) -> None:
        self.recover()
        result = validate_recovered_amcf_state(self.recovery_root / "recovered_amcf_manifest.json")
        self.assertTrue(result["ok"], result["errors"])

    def test_recovery_rejects_missing_section(self) -> None:
        self.make_package()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        (self.carrier_root / manifest["sections"][0]["section_file"]).unlink()
        result = recover_amcf_from_carrier_package(self.carrier_root, self.recovery_root, self.archive)
        self.assertFalse(result["ok"])
        self.assertTrue(any("missing_section_file" in error for error in result["errors"]))

    def test_recovery_rejects_tampered_section_payload_hash_mismatch(self) -> None:
        self.make_package()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        section_path = self.carrier_root / manifest["sections"][0]["section_file"]
        section_path.write_text(section_path.read_text(encoding="utf-8") + "\nTAMPER\n", encoding="utf-8")
        result = recover_amcf_from_carrier_package(self.carrier_root, self.recovery_root, self.archive)
        self.assertFalse(result["ok"])
        self.assertTrue(any("section_file_hash_mismatch" in error for error in result["errors"]))

    def test_recovery_rejects_missing_required_lane(self) -> None:
        self.make_package()
        manifest_path = self.carrier_root / "physical_carrier_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["sections"][0]["lanes"].pop("metadata_lane")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        result = recover_amcf_from_carrier_package(self.carrier_root, self.recovery_root, self.archive)
        self.assertFalse(result["ok"])
        self.assertTrue(any("manifest_missing_required_lane" in error for error in result["errors"]))

    def test_recovery_rejects_duplicate_or_out_of_order_section_indices(self) -> None:
        self.make_package()
        manifest_path = self.carrier_root / "physical_carrier_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["sections"][1]["section_index"] = 0
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        result = recover_amcf_from_carrier_package(self.carrier_root, self.recovery_root, self.archive)
        self.assertFalse(result["ok"])
        joined = " ".join(result["errors"])
        self.assertTrue("duplicate_section_index" in joined or "out_of_order_section_index" in joined)

    def test_no_physical_or_hardware_proof_claims_are_made(self) -> None:
        self.recover()
        recovered = json.loads((self.recovery_root / "recovered_amcf_manifest.json").read_text(encoding="utf-8"))
        boundary = recovered["claim_boundary"]
        self.assertFalse(boundary["physical_proof_claimed"])
        self.assertFalse(boundary["hardware_validation_claimed"])
        self.assertFalse(boundary["final_ui_claimed"])
        self.assertFalse(boundary["manufacturing_readiness_claimed"])
        self.assertFalse(boundary["physical_prototype_built"])
        self.assertFalse(boundary["real_scanner_used"])
        self.assertFalse(boundary["actual_physical_scanning_claimed"])
        self.assertFalse(boundary["mp4_video_container_export_claimed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
