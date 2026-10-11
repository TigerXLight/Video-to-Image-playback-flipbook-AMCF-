from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_digital_encoder import encode_source_frames  # noqa: E402
from amcf_digital_validator import validate_amcf_archive  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class SourceFramesToAmcfDigitalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_source_frames_"))
        self.source_root = self.tmp / "source_frames"
        self.archive = self.tmp / "sample_video_source.amcf.zip"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def make_archive(self) -> dict:
        manifest = generate_source_frames(self.source_root)
        encode_source_frames(self.source_root / "source_frames_manifest.json", self.archive)
        return manifest

    def test_sample_frames_generator_creates_expected_frame_count(self) -> None:
        manifest = generate_source_frames(self.source_root)
        self.assertEqual(manifest["frame_count"], 8)
        self.assertEqual(len(list((self.source_root / "frames").glob("*.ppm"))), 8)

    def test_encoder_creates_amcf_archive(self) -> None:
        self.make_archive()
        self.assertTrue(self.archive.exists())
        self.assertGreater(self.archive.stat().st_size, 0)

    def test_manifest_exists_in_archive(self) -> None:
        self.make_archive()
        with zipfile.ZipFile(self.archive, "r") as zf:
            self.assertIn("manifest.json", zf.namelist())

    def test_frame_payloads_exist_in_archive(self) -> None:
        self.make_archive()
        with zipfile.ZipFile(self.archive, "r") as zf:
            names = set(zf.namelist())
            for index in range(8):
                self.assertIn(f"frames/frame_{index:03d}.ppm", names)

    def test_hashes_validate(self) -> None:
        self.make_archive()
        result = validate_amcf_archive(self.archive)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["validated_payloads"], 8)

    def test_validator_passes_valid_archive(self) -> None:
        self.make_archive()
        self.assertTrue(validate_amcf_archive(self.archive)["ok"])

    def test_validator_rejects_tampered_payload(self) -> None:
        self.make_archive()
        tampered = self.tmp / "tampered.amcf.zip"
        with zipfile.ZipFile(self.archive, "r") as src, zipfile.ZipFile(tampered, "w", compression=zipfile.ZIP_DEFLATED) as dst:
            for name in src.namelist():
                payload = src.read(name)
                if name == "frames/frame_000.ppm":
                    payload += b"tamper"
                dst.writestr(name, payload)
        result = validate_amcf_archive(tampered)
        self.assertFalse(result["ok"])
        self.assertTrue(any("hash_mismatch" in error for error in result["errors"]))

    def test_validator_rejects_missing_payload(self) -> None:
        self.make_archive()
        missing = self.tmp / "missing_payload.amcf.zip"
        with zipfile.ZipFile(self.archive, "r") as src, zipfile.ZipFile(missing, "w", compression=zipfile.ZIP_DEFLATED) as dst:
            for name in src.namelist():
                if name != "frames/frame_001.ppm":
                    dst.writestr(name, src.read(name))
        result = validate_amcf_archive(missing)
        self.assertFalse(result["ok"])
        self.assertTrue(any("missing_payload" in error for error in result["errors"]))

    def test_no_physical_or_hardware_proof_claims_are_made(self) -> None:
        self.make_archive()
        with zipfile.ZipFile(self.archive, "r") as zf:
            manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
        boundary = manifest["claim_boundary"]
        self.assertFalse(boundary["physical_proof_claimed"])
        self.assertFalse(boundary["hardware_validation_claimed"])
        self.assertFalse(boundary["final_ui_claimed"])
        self.assertFalse(boundary["physical_prototype_built"])
        self.assertFalse(boundary["arbitrary_real_video_support_claimed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
