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
from amcf_physical_carrier import (  # noqa: E402
    REQUIRED_LANES,
    generate_physical_carrier_from_amcf_archive,
    validate_physical_carrier_package,
)
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class AmcfToPhysicalCarrierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_carrier_"))
        self.source_root = self.tmp / "source_frames"
        self.archive = self.tmp / "sample_video_source.amcf.zip"
        self.carrier_root = self.tmp / "carrier_package"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def make_package(self) -> dict:
        generate_source_frames(self.source_root)
        encode_source_frames(self.source_root / "source_frames_manifest.json", self.archive)
        self.assertTrue(validate_amcf_archive(self.archive)["ok"])
        return generate_physical_carrier_from_amcf_archive(self.archive, self.carrier_root)

    def test_source_frames_generate(self) -> None:
        manifest = generate_source_frames(self.source_root)
        self.assertEqual(manifest["frame_count"], 8)

    def test_amcf_archive_creates_and_validates(self) -> None:
        generate_source_frames(self.source_root)
        encode_source_frames(self.source_root / "source_frames_manifest.json", self.archive)
        self.assertTrue(self.archive.exists())
        self.assertTrue(validate_amcf_archive(self.archive)["ok"])

    def test_physical_carrier_package_creates(self) -> None:
        result = self.make_package()
        self.assertTrue(result["ok"])
        self.assertTrue((self.carrier_root / "physical_carrier_manifest.json").exists())
        self.assertTrue((self.carrier_root / "carrier_sections").exists())

    def test_section_count_matches_amcf_frame_count(self) -> None:
        self.make_package()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["section_count"], 8)
        self.assertEqual(len(manifest["sections"]), 8)

    def test_required_lanes_exist(self) -> None:
        self.make_package()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        self.assertTrue((self.carrier_root / "physical_carrier_manifest.json").exists())
        for lane in REQUIRED_LANES:
            self.assertIn(lane, manifest["lane_schema"])
            self.assertIn(lane, manifest["sections"][0]["lanes"])
            section_text = (self.carrier_root / manifest["sections"][0]["section_file"]).read_text(encoding="utf-8")
            self.assertIn(f"[{lane}]", section_text)

    def test_validator_passes_valid_package(self) -> None:
        self.make_package()
        result = validate_physical_carrier_package(self.carrier_root)
        self.assertTrue(result["ok"], result["errors"])

    def test_validator_rejects_missing_section(self) -> None:
        self.make_package()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        (self.carrier_root / manifest["sections"][0]["section_file"]).unlink()
        result = validate_physical_carrier_package(self.carrier_root)
        self.assertFalse(result["ok"])
        self.assertTrue(any(error.startswith("missing_section") for error in result["errors"]))

    def test_validator_rejects_hash_mismatch(self) -> None:
        self.make_package()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        section_path = self.carrier_root / manifest["sections"][0]["section_file"]
        section_path.write_text(section_path.read_text(encoding="utf-8") + "\nTAMPER\n", encoding="utf-8")
        result = validate_physical_carrier_package(self.carrier_root)
        self.assertFalse(result["ok"])
        self.assertTrue(any(error.startswith("section_file_hash_mismatch") for error in result["errors"]))

    def test_no_physical_or_hardware_proof_claims_are_made(self) -> None:
        self.make_package()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        boundary = manifest["claim_boundary"]
        self.assertFalse(boundary["physical_proof_claimed"])
        self.assertFalse(boundary["hardware_validation_claimed"])
        self.assertFalse(boundary["final_ui_claimed"])
        self.assertFalse(boundary["manufacturing_readiness_claimed"])
        self.assertFalse(boundary["physical_prototype_built"])
        self.assertFalse(boundary["real_printing_performed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
