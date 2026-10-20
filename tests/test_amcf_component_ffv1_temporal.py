from __future__ import annotations

import bz2
import json
import shutil
import struct
import tempfile
import unittest
from pathlib import Path
import lzma
import zipfile

import numpy as np


PACKAGE = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(PACKAGE / "src"))

from amcf_component_ffv1_temporal import (  # noqa: E402
    EVENT_STRUCT,
    build_temporal_component_archive,
    corruption_rejected,
    decode_temporal_component_archive,
)


def put_varint(output: bytearray, value: int) -> None:
    while value >= 0x80:
        output.append((value & 0x7F) | 0x80)
        value >>= 7
    output.append(value)


def zigzag(value: int) -> int:
    return value * 2 if value >= 0 else (-value * 2) - 1


def encode_values(values: np.ndarray) -> bytes:
    output = bytearray()
    zero_run = 0
    for value in values.reshape(-1).tolist():
        value = int(value)
        if value == 0:
            zero_run += 1
            continue
        if zero_run:
            output.append(0)
            put_varint(output, zero_run)
            zero_run = 0
        put_varint(output, zigzag(value) + 1)
    if zero_run:
        output.append(0)
        put_varint(output, zero_run)
    return bytes(output)


def bgr_to_ycocg(values: np.ndarray) -> np.ndarray:
    b, g, r = (values[:, index].astype(np.int32) for index in range(3))
    co = r - b
    t = b + (co >> 1)
    cg = g - t
    y = t + (cg >> 1)
    return np.stack((y, co, cg), axis=1).astype(np.int16)


def encode_byte_delta(current: bytes, previous: bytes) -> bytes:
    output = bytearray()
    zero_run = 0
    for left, right in zip(current, previous):
        value = left ^ right
        if value == 0:
            zero_run += 1
            continue
        if zero_run:
            output.append(0)
            put_varint(output, zero_run)
            zero_run = 0
        put_varint(output, value + 1)
    if zero_run:
        output.append(0)
        put_varint(output, zero_run)
    return bytes(output)


def build_fixture(path: Path) -> None:
    width, height = 4, 2
    frame0 = np.arange(width * height * 3, dtype=np.uint8).reshape(height, width, 3)
    frame1 = (frame0.astype(np.uint16) + np.array([2, 0, 3], dtype=np.uint16)).astype(np.uint8)
    mask_packed = np.packbits(np.ones(width * height, dtype=np.uint8), bitorder="little").tobytes()
    zero_mask = bytes(len(mask_packed))
    mask0 = encode_byte_delta(mask_packed, zero_mask)
    mask1 = encode_byte_delta(mask_packed, mask_packed)
    mask_stream = bz2.compress(mask0 + mask1)
    payload0 = encode_values(bgr_to_ycocg(frame0.reshape(-1, 3).astype(np.int16)))
    payload1 = encode_values(bgr_to_ycocg((frame1.astype(np.int16) - frame0.astype(np.int16)).reshape(-1, 3)))
    residuals = payload0 + payload1
    events = b"".join((
        EVENT_STRUCT.pack(0, 0, 1, 0, 0, 0, 0, width, height, 0, len(mask0), 0, len(payload0), width * height),
        EVENT_STRUCT.pack(1, 0, 2, 0, 0, 0, 0, width, height, len(mask0), len(mask1), len(payload0), len(payload1), width * height),
    ))
    manifest = {
        "schema": "amcf-component-local-neighbor-mask-delta-v1",
        "source_reference": {"filename": "not-embedded.mp4", "bytes": 1234, "frames": 2, "width": width, "height": height, "fps": 1.0},
        "component_taxonomy": ["component_0"],
        "keyframe_interval": 2,
        "event_index": {"count": 2, "record_bytes": EVENT_STRUCT.size},
        "residual_stream": {"encoding": "reversible_ycocg_r_zero_run_zigzag_varint"},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("manifest/manifest.json", json.dumps(manifest).encode("utf-8"))
        archive.writestr("payload/events.bin", events)
        archive.writestr("payload/mask_delta_stream.bin.bz2", mask_stream)
        archive.writestr("payload/residual_stream.bin.lzma", lzma.compress(residuals))


@unittest.skipUnless(shutil.which("ffmpeg"), "FFmpeg is required for this exact backend test")
class TemporalComponentFfv1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_temporal_ffv1_"))
        self.canonical = self.tmp / "canonical.amcf.zip"
        build_fixture(self.canonical)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_decode_and_corruption_rejection(self) -> None:
        archive = self.tmp / "temporal.amcf.zip"
        built = build_temporal_component_archive(self.canonical, archive, gop=2)
        self.assertTrue(built["ok"])
        decoded = decode_temporal_component_archive(archive, self.tmp / "decoded")
        self.assertTrue(decoded["ok"], decoded)
        self.assertEqual(decoded["decoded_event_count"], 2)
        self.assertEqual(decoded["decoded_frame_count"], 2)
        self.assertTrue(corruption_rejected(archive, self.tmp / "corruption"))
        self.assertFalse(decoded["source_video_required_for_decode"])
        self.assertFalse(decoded["independent_complete_video_payload_present"])
        self.assertEqual(decoded["unsafe_acceptance_count"], 0)


if __name__ == "__main__":
    unittest.main()
