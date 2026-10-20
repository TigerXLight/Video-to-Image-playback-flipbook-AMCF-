"""Bounded, fail-closed reader for local Test 14H component archives."""

from __future__ import annotations

import io
import json
import zlib
import zipfile
from hashlib import sha256
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from PIL import Image
except ImportError:
    Image = None


class ArchiveFormatError(ValueError):
    """A 14H archive cannot be decoded without violating its recorded contract."""


def _member(zf: zipfile.ZipFile, name: str) -> bytes:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts:
        raise ArchiveFormatError("invalid archive member path")
    try:
        return zf.read(name)
    except KeyError as error:
        raise ArchiveFormatError(f"missing archive member: {name}") from error


def _json_member(zf: zipfile.ZipFile, name: str) -> dict[str, Any]:
    try:
        value = json.loads(_member(zf, name))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ArchiveFormatError(f"invalid JSON member: {name}") from error
    if not isinstance(value, dict):
        raise ArchiveFormatError(f"JSON member is not an object: {name}")
    return value


def _image(payload: bytes):
    if Image is None:
        raise RuntimeError("Pillow is required to decode 14H WebP payloads")
    try:
        with Image.open(io.BytesIO(payload)) as opened:
            image = opened.convert("RGB")
            image.load()
        return image
    except (OSError, ValueError) as error:
        raise ArchiveFormatError("invalid image payload") from error


def _positive_int(value: Any, label: str) -> int:
    if type(value) is not int or value <= 0:
        raise ArchiveFormatError(f"invalid {label}")
    return value


def _nonnegative_int(value: Any, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ArchiveFormatError(f"invalid {label}")
    return value


def _payload(zf: zipfile.ZipFile, item: dict[str, Any]) -> bytes:
    if not isinstance(item, dict) or not isinstance(item.get("path"), str):
        raise ArchiveFormatError("invalid payload record")
    data = _member(zf, item["path"])
    if len(data) != _nonnegative_int(item.get("size"), "payload size"):
        raise ArchiveFormatError("payload size mismatch")
    if sha256(data).hexdigest() != item.get("sha256"):
        raise ArchiveFormatError("payload checksum mismatch")
    return data


def _xor_patch(data: bytes, previous, item: dict[str, Any], width: int, height: int):
    source_x = _nonnegative_int(item.get("source_x"), "source x")
    source_y = _nonnegative_int(item.get("source_y"), "source y")
    patch_width = _positive_int(item.get("w"), "patch width")
    patch_height = _positive_int(item.get("h"), "patch height")
    if source_x + patch_width > width or source_y + patch_height > height:
        raise ArchiveFormatError("motion source exceeds frame bounds")
    if item.get("shape") != [patch_height, patch_width, 3]:
        raise ArchiveFormatError("residual shape mismatch")
    expected = patch_width * patch_height * 3
    try:
        decoder = zlib.decompressobj()
        residual = decoder.decompress(data, expected + 1)
    except zlib.error as error:
        raise ArchiveFormatError("invalid compressed residual") from error
    if len(residual) != expected or not decoder.eof or decoder.unconsumed_tail or decoder.unused_data:
        raise ArchiveFormatError("residual length mismatch")
    prediction = previous.crop((source_x, source_y, source_x + patch_width, source_y + patch_height)).tobytes()
    decoded = bytes(left ^ right for left, right in zip(prediction, residual))
    return Image.frombytes("RGB", (patch_width, patch_height), decoded)


def decode_14h_archive(path: str | Path, *, retain_frames: bool = False, max_frames: int = 120):
    """Return a verified report and optional RGB frames; reject any unsafe mismatch."""
    if Image is None:
        raise RuntimeError("Pillow is required to decode 14H WebP payloads")
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            raise ArchiveFormatError("duplicate archive member")
        manifest = _json_member(zf, "manifest/native_manifest_14H.json")
        plan = _json_member(zf, "indexes/decode_plan_14H.json")
        checks = _json_member(zf, "checksums/frame_checksums_14H.json")
        if manifest.get("amcf_test") != "14H":
            raise ArchiveFormatError("not a Test 14H archive")
        count = _positive_int(manifest.get("frame_count"), "frame count")
        if count > max_frames:
            raise ArchiveFormatError("archive exceeds bounded frame count")
        resolution = manifest.get("resolution")
        if not isinstance(resolution, dict) or resolution.get("channels") != 3:
            raise ArchiveFormatError("invalid RGB resolution")
        width = _positive_int(resolution.get("width"), "width")
        height = _positive_int(resolution.get("height"), "height")
        if width * height > 16_777_216:
            raise ArchiveFormatError("frame dimensions exceed bound")
        records = plan.get("frames")
        checksum_rows = checks.get("frames")
        if not isinstance(records, list) or not isinstance(checksum_rows, list) or len(records) != count or len(checksum_rows) != count:
            raise ArchiveFormatError("frame plan/checksum count mismatch")
        checksum_map = {}
        for row in checksum_rows:
            if not isinstance(row, dict) or not isinstance(row.get("frame_id"), str) or row["frame_id"] in checksum_map:
                raise ArchiveFormatError("invalid or duplicate frame checksum record")
            checksum_map[row["frame_id"]] = row.get("rgb_sha256")

        previous = None
        previous_id = None
        frames = []
        for index, row in enumerate(records):
            if not isinstance(row, dict) or row.get("frame_index") != index or row.get("frame_id") != f"frame_{index:06d}":
                raise ArchiveFormatError("frame order mismatch")
            frame_id = row["frame_id"]
            payloads = row.get("payloads")
            if not isinstance(payloads, list):
                raise ArchiveFormatError("invalid frame payload list")
            if row.get("type") == "keyframe":
                if row.get("dependency") is not None or len(payloads) != 1 or not isinstance(payloads[0], dict) or payloads[0].get("codec") != "webp_frame":
                    raise ArchiveFormatError("invalid keyframe")
                current = _image(_payload(zf, payloads[0]))
                if current.size != (width, height):
                    raise ArchiveFormatError("keyframe dimensions mismatch")
            elif row.get("type") == "delta":
                if previous is None or row.get("dependency") != previous_id:
                    raise ArchiveFormatError("unsafe frame dependency")
                current = previous.copy()
                for item in payloads:
                    if not isinstance(item, dict):
                        raise ArchiveFormatError("invalid delta payload")
                    x = _nonnegative_int(item.get("x"), "patch x")
                    y = _nonnegative_int(item.get("y"), "patch y")
                    patch_width = _positive_int(item.get("w"), "patch width")
                    patch_height = _positive_int(item.get("h"), "patch height")
                    if x + patch_width > width or y + patch_height > height:
                        raise ArchiveFormatError("patch exceeds frame bounds")
                    data = _payload(zf, item)
                    if item.get("codec") == "motion_xor_zlib":
                        patch = _xor_patch(data, previous, item, width, height)
                    elif item.get("codec") == "webp_patch":
                        patch = _image(data)
                        if patch.size != (patch_width, patch_height):
                            raise ArchiveFormatError("patch dimensions mismatch")
                    else:
                        raise ArchiveFormatError("unsupported delta codec")
                    current.paste(patch, (x, y))
            else:
                raise ArchiveFormatError("unsupported frame type")
            if sha256(current.tobytes()).hexdigest() != checksum_map.get(frame_id):
                raise ArchiveFormatError(f"decoded frame checksum mismatch: {frame_id}")
            if retain_frames:
                frames.append(current)
            previous = current
            previous_id = frame_id

    report = {
        "schema": "amcf-14h-bounded-archive-read-v1",
        "sample_id": manifest.get("sample_id"),
        "variant_id": manifest.get("variant_id"),
        "frame_count": count,
        "all_checksums_match": True,
        "unsafe_acceptance_count": 0,
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "semantic_objects_claimed": False,
            "general_compression_win_claimed": False,
        },
    }
    return report, frames
