from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
import zipfile
import zlib
from hashlib import sha256
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from amcf_v2_14h_archive import ArchiveFormatError, Image, decode_14h_archive  # noqa: E402


def webp(image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format="WEBP", lossless=True)
    return buffer.getvalue()


def write_fixture(path: Path, *, codec: str = "webp_patch", wrong_checksum: bool = False, omit_delta: bool = False, oversized_residual: bool = False) -> bytes:
    first = Image.new("RGB", (4, 4), (120, 40, 10))
    patch = Image.new("RGB", (2, 2), (10, 80, 220))
    second = first.copy()
    second.paste(patch, (1, 1))
    key_bytes = webp(first)
    if codec == "motion_xor_zlib":
        prediction = first.crop((1, 1, 3, 3)).tobytes()
        residual = bytes(a ^ b for a, b in zip(prediction, patch.tobytes()))
        delta_bytes = zlib.compress(residual + (b"\0" * 100 if oversized_residual else b""))
    else:
        delta_bytes = webp(patch)
    payload = {
        "path": "payloads/deltas/frame_000001/region_0000",
        "codec": codec,
        "size": len(delta_bytes),
        "sha256": sha256(delta_bytes).hexdigest(),
        "x": 1,
        "y": 1,
        "w": 2,
        "h": 2,
        "shape": [2, 2, 3],
        "source_x": 1,
        "source_y": 1,
    }
    manifest = {"amcf_test": "14H", "sample_id": "tiny", "variant_id": codec, "frame_count": 2, "resolution": {"width": 4, "height": 4, "channels": 3}}
    plan = {"frames": [
        {"frame_id": "frame_000000", "frame_index": 0, "type": "keyframe", "dependency": None, "payloads": [{"path": "payloads/keyframes/frame_000000.webp", "codec": "webp_frame", "size": len(key_bytes), "sha256": sha256(key_bytes).hexdigest()}]},
        {"frame_id": "frame_000001", "frame_index": 1, "type": "delta", "dependency": "frame_000000", "payloads": [payload]},
    ]}
    checks = {"frames": [
        {"frame_id": "frame_000000", "rgb_sha256": sha256(first.tobytes()).hexdigest()},
        {"frame_id": "frame_000001", "rgb_sha256": "0" * 64 if wrong_checksum else sha256(second.tobytes()).hexdigest()},
    ]}
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest/native_manifest_14H.json", json.dumps(manifest))
        archive.writestr("indexes/decode_plan_14H.json", json.dumps(plan))
        archive.writestr("checksums/frame_checksums_14H.json", json.dumps(checks))
        archive.writestr("payloads/keyframes/frame_000000.webp", key_bytes)
        if not omit_delta:
            archive.writestr(payload["path"], delta_bytes)
    return second.tobytes()


@unittest.skipIf(Image is None, "Pillow is unavailable")
class Test14HArchiveTests(unittest.TestCase):
    def test_webp_patch_decodes_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "sample.zip"
            expected = write_fixture(path)
            report, frames = decode_14h_archive(path, retain_frames=True)
            self.assertEqual(report["frame_count"], 2)
            self.assertTrue(report["all_checksums_match"])
            self.assertEqual(report["unsafe_acceptance_count"], 0)
            self.assertFalse(report["claim_boundary"]["hardware_validation_claimed"])
            self.assertEqual(frames[1].tobytes(), expected)

    def test_motion_xor_zlib_decodes_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "sample.zip"
            expected = write_fixture(path, codec="motion_xor_zlib")
            report, frames = decode_14h_archive(path, retain_frames=True)
            self.assertTrue(report["all_checksums_match"])
            self.assertEqual(frames[1].tobytes(), expected)

    def test_wrong_frame_checksum_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "sample.zip"
            write_fixture(path, wrong_checksum=True)
            with self.assertRaisesRegex(ArchiveFormatError, "decoded frame checksum mismatch"):
                decode_14h_archive(path)

    def test_missing_payload_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "sample.zip"
            write_fixture(path, omit_delta=True)
            with self.assertRaisesRegex(ArchiveFormatError, "missing archive member"):
                decode_14h_archive(path)

    def test_frame_limit_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "sample.zip"
            write_fixture(path)
            with self.assertRaisesRegex(ArchiveFormatError, "bounded frame count"):
                decode_14h_archive(path, max_frames=1)

    def test_oversized_residual_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "sample.zip"
            write_fixture(path, codec="motion_xor_zlib", oversized_residual=True)
            with self.assertRaisesRegex(ArchiveFormatError, "residual length mismatch"):
                decode_14h_archive(path)


if __name__ == "__main__":
    unittest.main()
