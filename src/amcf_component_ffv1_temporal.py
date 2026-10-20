"""Exact temporal FFV1 storage for a canonical AMCF component archive.

The canonical AMCF event graph remains authoritative.  This module changes
only the physical storage of the exact component-owned pixel states: one
lossless FFV1 stream is written per component, with all event, mask, metadata,
and integrity members retained in the resulting archive.

The input archive is source-independent.  Its source-reference filename is
metadata only; no source video member is read or required for decoding.
"""

from __future__ import annotations

import bz2
from dataclasses import dataclass
import hashlib
import json
import lzma
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
from typing import Any
import zipfile

import numpy as np


EVENT_STRUCT = struct.Struct(">IBBhhHHHHIIIII")
PREDICTOR_NAMES = {
    0: "zero",
    1: "component_same",
    2: "component_global_shift",
    3: "frame_same",
    4: "frame_global_shift",
    5: "component_left_spatial",
}
FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


@dataclass
class CanonicalArchive:
    path: Path
    manifest: dict[str, Any]
    manifest_bytes: bytes
    raw_events: bytes
    mask_member: bytes
    events: list[dict[str, Any]]
    rows: list[dict[str, Any]]
    frames: list[np.ndarray]
    event_hashes: list[str]
    frame_hashes: list[str]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_member(archive: zipfile.ZipFile, name: str, data: bytes, *, stored: bool = True) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
    info.external_attr = 0o600 << 16
    archive.writestr(info, data)


def _get_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        if offset >= len(data):
            raise ValueError("truncated AMCF varint")
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, offset
        shift += 7
        if shift > 63:
            raise ValueError("AMCF varint overflow")


def _decode_values(data: bytes, expected: int) -> np.ndarray:
    """Decode the exact zero-run/zig-zag residual symbol stream."""
    output = np.empty(expected, dtype=np.int16)
    offset = 0
    index = 0
    while index < expected:
        token, offset = _get_varint(data, offset)
        if token == 0:
            run, offset = _get_varint(data, offset)
            if index + run > expected:
                raise ValueError("AMCF residual stream overrun")
            output[index:index + run] = 0
            index += run
            continue
        value = token - 1
        output[index] = (value >> 1) ^ -(value & 1)
        index += 1
    if offset != len(data):
        raise ValueError("AMCF residual stream has trailing bytes")
    return output


def _ycocg_to_bgr(values: np.ndarray) -> np.ndarray:
    y, co, cg = (values[:, index].astype(np.int32) for index in range(3))
    t = y - (cg >> 1)
    g = cg + t
    b = t - (co >> 1)
    r = co + b
    return np.stack((b, g, r), axis=1).astype(np.int16)


def _decode_byte_delta(data: bytes, raw_size: int, previous: bytes) -> bytes:
    output = bytearray()
    offset = 0
    while len(output) < raw_size:
        token, offset = _get_varint(data, offset)
        if token == 0:
            run, offset = _get_varint(data, offset)
            output.extend(b"\x00" * run)
        else:
            output.append(token - 1)
    if len(output) != raw_size or offset != len(data):
        raise ValueError("AMCF mask delta stream mismatch")
    return np.bitwise_xor(
        np.frombuffer(bytes(output), dtype=np.uint8),
        np.frombuffer(previous, dtype=np.uint8),
    ).tobytes()


def _unpack_mask(blob: bytes, height: int, width: int) -> np.ndarray:
    values = np.unpackbits(np.frombuffer(blob, dtype=np.uint8), bitorder="little")[: height * width]
    return values.reshape(height, width).astype(bool)


def _shifted_mask_values(state: np.ndarray, flat_indices: np.ndarray, dx: int, dy: int) -> np.ndarray:
    height, width = state.shape[:2]
    ys = flat_indices // width
    xs = flat_indices - (ys * width)
    source_y = np.clip(ys - int(dy), 0, height - 1)
    source_x = np.clip(xs - int(dx), 0, width - 1)
    return state[source_y, source_x].astype(np.int32)


def _rebuild_sparse_values(flat_indices: np.ndarray, base_values: np.ndarray, deltas: np.ndarray) -> np.ndarray:
    if len(flat_indices) != len(deltas):
        raise ValueError("component-local residual count mismatch")
    starts = np.r_[True, flat_indices[1:] != flat_indices[:-1] + 1]
    start_positions = np.flatnonzero(starts)
    end_positions = np.r_[start_positions[1:], len(flat_indices)]
    values = np.empty_like(deltas, dtype=np.int32)
    for start, end in zip(start_positions, end_positions):
        values[start:end] = base_values[start] + np.cumsum(deltas[start:end].astype(np.int32), axis=0)
    if np.any(values < 0) or np.any(values > 255):
        raise ValueError("component-local residual reconstructed outside uint8")
    return values


def _parse_events(raw_events: bytes) -> list[dict[str, Any]]:
    if len(raw_events) % EVENT_STRUCT.size:
        raise ValueError("canonical events.bin is not record aligned")
    events: list[dict[str, Any]] = []
    for offset in range(0, len(raw_events), EVENT_STRUCT.size):
        frame, component, flags, dx, dy, x, y, w, h, mask_offset, mask_bytes, residual_offset, residual_bytes, owned = EVENT_STRUCT.unpack_from(raw_events, offset)
        events.append({
            "frame_index": int(frame),
            "component_index": int(component),
            "keyframe": bool(flags & 1),
            "predictor": PREDICTOR_NAMES.get(flags >> 1, "unknown"),
            "dx": int(dx),
            "dy": int(dy),
            "bbox": [int(x), int(y), int(w), int(h)],
            "mask_offset": int(mask_offset),
            "mask_bytes": int(mask_bytes),
            "residual_offset": int(residual_offset),
            "residual_bytes": int(residual_bytes),
            "owned_pixels": int(owned),
        })
    return events


def _decode_canonical_frames(
    manifest: dict[str, Any],
    events: list[dict[str, Any]],
    mask_stream: bytes,
    residual_stream: bytes,
) -> tuple[list[dict[str, Any]], list[np.ndarray]]:
    width = int(manifest["source_reference"]["width"])
    height = int(manifest["source_reference"]["height"])
    frame_count = int(manifest["source_reference"]["frames"])
    components = list(manifest["component_taxonomy"])
    raw_mask_size = (width * height + 7) // 8
    previous_masks = [bytes(raw_mask_size) for _ in components]
    rows: list[dict[str, Any]] = []
    for ordinal, event in enumerate(events):
        start = event["mask_offset"]
        blob = mask_stream[start:start + event["mask_bytes"]]
        mask_packed = _decode_byte_delta(blob, raw_mask_size, previous_masks[event["component_index"]])
        previous_masks[event["component_index"]] = mask_packed
        mask = _unpack_mask(mask_packed, height, width)
        owned = int(np.count_nonzero(mask))
        if owned != event["owned_pixels"]:
            raise ValueError(f"canonical mask ownership mismatch at event {ordinal}")
        rows.append({**event, "ordinal": ordinal, "mask_packed": mask_packed})

    by_frame: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        by_frame.setdefault(row["frame_index"], []).append(row)
    states = {component: np.zeros((height, width, 3), dtype=np.uint8) for component in components}
    active_indices = {component: np.empty(0, dtype=np.int64) for component in components}
    previous_frame = np.zeros((height, width, 3), dtype=np.uint8)
    has_previous_frame = False
    frames: list[np.ndarray] = []
    residual_encoding = str(manifest.get("residual_stream", {}).get("encoding", ""))
    if "zero_run_zigzag" not in residual_encoding:
        raise ValueError(f"unsupported canonical residual encoding: {residual_encoding}")

    for frame_index in range(frame_count):
        if frame_index % int(manifest["keyframe_interval"]) == 0:
            states = {component: np.zeros((height, width, 3), dtype=np.uint8) for component in components}
            active_indices = {component: np.empty(0, dtype=np.int64) for component in components}
        frame_events = by_frame.get(frame_index, [])
        frame_masks: list[tuple[int, np.ndarray]] = []
        for event in frame_events:
            component_index = event["component_index"]
            mask = _unpack_mask(event["mask_packed"], height, width)
            flat_indices = np.flatnonzero(mask.reshape(-1))
            frame_masks.append((component_index, mask))
            component = components[component_index]
            state = states[component]
            predictor = event["predictor"]
            if event["keyframe"] or predictor == "zero":
                base_values = np.zeros((len(flat_indices), 3), dtype=np.int32)
            elif predictor == "component_same":
                base_values = state.reshape(-1, 3)[flat_indices].astype(np.int32)
            elif predictor == "component_global_shift":
                base_values = _shifted_mask_values(state, flat_indices, event["dx"], event["dy"])
            elif predictor == "frame_same":
                base_values = previous_frame.reshape(-1, 3)[flat_indices].astype(np.int32) if has_previous_frame else np.zeros((len(flat_indices), 3), dtype=np.int32)
            elif predictor == "frame_global_shift":
                base_values = _shifted_mask_values(previous_frame, flat_indices, event["dx"], event["dy"]) if has_previous_frame else np.zeros((len(flat_indices), 3), dtype=np.int32)
            elif predictor == "component_left_spatial":
                base_values = np.zeros((len(flat_indices), 3), dtype=np.int32) if event["keyframe"] else _shifted_mask_values(state, flat_indices, event["dx"], event["dy"])
            else:
                raise ValueError(f"unknown canonical predictor: {predictor}")

            start = event["residual_offset"]
            payload = residual_stream[start:start + event["residual_bytes"]]
            deltas = _ycocg_to_bgr(_decode_values(payload, event["owned_pixels"] * 3).reshape((-1, 3)))
            if predictor == "component_left_spatial":
                rebuilt = _rebuild_sparse_values(flat_indices, base_values, deltas)
            else:
                rebuilt = base_values + deltas
                if np.any(rebuilt < 0) or np.any(rebuilt > 255):
                    raise ValueError(f"canonical predictor reconstructed outside uint8 at event {event['ordinal']}")
            old_indices = active_indices[component]
            state_flat = state.reshape(-1, 3)
            if len(old_indices):
                state_flat[old_indices] = 0
            state_flat[flat_indices] = rebuilt.astype(np.uint8)
            active_indices[component] = flat_indices

        frame = np.zeros((height, width, 3), dtype=np.uint8)
        for component_index, mask in frame_masks:
            frame[mask] = states[components[component_index]][mask]
        frames.append(frame)
        previous_frame = frame
        has_previous_frame = True
    if len(frames) != frame_count:
        raise ValueError("canonical archive frame count mismatch")
    return rows, frames


def load_canonical_component_archive(path: str | Path) -> CanonicalArchive:
    path = Path(path).resolve()
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        if "manifest/manifest.json" not in names or "payload/events.bin" not in names:
            raise ValueError("canonical component archive is missing the event contract")
        if any(name.lower().endswith((".mp4", ".mov", ".avi")) for name in names):
            raise ValueError("canonical component archive must not embed source video")
        manifest_bytes = archive.read("manifest/manifest.json")
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        raw_events = archive.read("payload/events.bin")
        mask_member = archive.read("payload/mask_delta_stream.bin.bz2")
        residual_stream = lzma.decompress(archive.read("payload/residual_stream.bin.lzma"))
    events = _parse_events(raw_events)
    rows, frames = _decode_canonical_frames(manifest, events, bz2.decompress(mask_member), residual_stream)
    event_hashes: list[str] = []
    for row in rows:
        mask = _unpack_mask(row["mask_packed"], int(manifest["source_reference"]["height"]), int(manifest["source_reference"]["width"]))
        event_hashes.append(_sha256(frames[row["frame_index"]][mask].tobytes()))
    frame_hashes = [_sha256(frame.tobytes()) for frame in frames]
    return CanonicalArchive(path, manifest, manifest_bytes, raw_events, mask_member, events, rows, frames, event_hashes, frame_hashes)


def _component_bounds(rows: list[dict[str, Any]], component_count: int) -> dict[int, list[int]]:
    bounds: dict[int, list[int]] = {}
    for component in range(component_count):
        selected = [row["bbox"] for row in rows if row["component_index"] == component]
        if not selected:
            raise ValueError(f"component {component} has no retained events")
        left = min(box[0] for box in selected)
        top = min(box[1] for box in selected)
        right = max(box[0] + box[2] for box in selected)
        bottom = max(box[1] + box[3] for box in selected)
        bounds[component] = [left, top, right, bottom]
    return bounds


def _encode_component_stream(
    path: Path,
    component_rows: list[dict[str, Any]],
    bounds: list[int],
    frames: list[np.ndarray],
    width: int,
    height: int,
    ffmpeg_bin: str,
    gop: int,
    coder: int,
    context: int,
) -> None:
    left, top, right, bottom = bounds
    canvas_width = right - left
    canvas_height = bottom - top
    command = [
        ffmpeg_bin, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{canvas_width}x{canvas_height}",
        "-r", "1", "-i", "-", "-an", "-c:v", "ffv1", "-level", "3",
        "-coder", str(coder), "-context", str(context), "-g", str(gop), "-pix_fmt", "gbrp", str(path),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for row in component_rows:
            canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
            mask = _unpack_mask(row["mask_packed"], height, width)
            x, y, w, h = row["bbox"]
            local_mask = mask[y:y + h, x:x + w]
            crop = frames[row["frame_index"]][y:y + h, x:x + w]
            canvas[y - top:y - top + h, x - left:x - left + w][local_mask] = crop[local_mask]
            process.stdin.write(canvas.tobytes())
        process.stdin.close()
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr is not None else ""
        returncode = process.wait()
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
    except Exception:
        process.kill()
        process.wait()
        raise
    if returncode != 0:
        raise RuntimeError(f"FFV1 component encode failed: {stderr[-2000:]}")


def _resolve_ffmpeg(ffmpeg_bin: str) -> str:
    resolved = shutil.which(ffmpeg_bin) or (ffmpeg_bin if Path(ffmpeg_bin).exists() else None)
    if not resolved:
        raise RuntimeError(f"FFmpeg is required for the temporal component backend: {ffmpeg_bin}")
    return resolved


def build_temporal_component_archive(
    canonical_archive_path: str | Path,
    output_archive_path: str | Path,
    *,
    ffmpeg_bin: str = "ffmpeg",
    gop: int = 288,
    coder: int = 1,
    context: int = 1,
) -> dict[str, Any]:
    canonical = load_canonical_component_archive(canonical_archive_path)
    ffmpeg_bin = _resolve_ffmpeg(ffmpeg_bin)
    output_path = Path(output_archive_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    component_count = len(canonical.manifest["component_taxonomy"])
    width = int(canonical.manifest["source_reference"]["width"])
    height = int(canonical.manifest["source_reference"]["height"])
    bounds = _component_bounds(canonical.rows, component_count)
    by_component = {component: [] for component in range(component_count)}
    for row in canonical.rows:
        by_component[row["component_index"]].append(row)
    stream_info: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="amcf_temporal_ffv1_", dir=str(output_path.parent)) as temp_name:
        temp_dir = Path(temp_name)
        for component in range(component_count):
            stream_path = temp_dir / f"component_{component:02d}.mkv"
            _encode_component_stream(
                stream_path, by_component[component], bounds[component], canonical.frames,
                width, height, ffmpeg_bin, int(gop), int(coder), int(context),
            )
            left, top, right, bottom = bounds[component]
            stream_info.append({
                "component_index": component,
                "member": f"payload/component_streams/component_{component:02d}.mkv",
                "bounds": bounds[component],
                "width": right - left,
                "height": bottom - top,
                "frame_count": len(by_component[component]),
                "bytes": stream_path.stat().st_size,
                "temp_path": str(stream_path),
            })
        contract = {
            "archive_kind": "self_contained_exact_component_event_archive_temporal_ffv1",
            "canonical_manifest_sha256": _sha256(canonical.manifest_bytes),
            "canonical_events_sha256": _sha256(canonical.raw_events),
            "canonical_mask_member_sha256": _sha256(canonical.mask_member),
            "logical_event_count": len(canonical.rows),
            "frame_count": len(canonical.frames),
            "all_logical_events_retained": True,
            "canonical_masks_retained": True,
            "canonical_timestamps_ids_order_and_motion_metadata_retained": True,
            "diagnostic_contract_retained": True,
            "source_video_embedded": False,
            "source_video_required_for_decode": False,
            "independent_complete_video_payload_present": False,
            "information_loss_allowed": False,
            "unsafe_acceptance_count": 0,
        }
        variant_manifest = {
            "variant": "component_temporal_ffv1_gop",
            "payload_codec": "ffv1_lossless_gbrp",
            "payload_encoding": "component_canvas_raster_per_event_frame",
            "gop": int(gop),
            "coder": int(coder),
            "context": int(context),
            "component_streams": [{key: value for key, value in info.items() if key != "temp_path"} for info in stream_info],
            "source_independent": True,
            "all_event_state_hashes_required": True,
        }
        with zipfile.ZipFile(output_path, "w") as archive:
            _write_member(archive, "manifest/canonical_manifest.json", canonical.manifest_bytes)
            _write_member(archive, "manifest/temporal_ffv1_manifest.json", json.dumps(variant_manifest, indent=2, sort_keys=True).encode("utf-8"), stored=False)
            _write_member(archive, "metadata/preserved_contract.json", json.dumps(contract, indent=2, sort_keys=True).encode("utf-8"), stored=False)
            _write_member(archive, "payload/events.bin", canonical.raw_events)
            _write_member(archive, "payload/mask_delta_stream.bin.bz2", canonical.mask_member)
            _write_member(archive, "payload/event_state_hashes.bin", b"".join(bytes.fromhex(value) for value in canonical.event_hashes))
            _write_member(archive, "payload/frame_hashes.bin", b"".join(bytes.fromhex(value) for value in canonical.frame_hashes))
            _write_member(archive, "decoder/DECODER_CONTRACT.md", b"Decode all retained AMCF events and masks, then decode every component FFV1 stream. The source video is not required. Verify every event and frame hash.\n", stored=False)
            _write_member(archive, "manifest/component_stream_index.json", json.dumps([{key: value for key, value in info.items() if key != "temp_path"} for info in stream_info], indent=2, sort_keys=True).encode("utf-8"), stored=False)
            for info in stream_info:
                _write_member(archive, info["member"], Path(info["temp_path"]).read_bytes())
    return {
        "ok": True,
        "archive_path": str(output_path),
        "canonical_archive_path": str(canonical.path),
        "canonical_archive_bytes": canonical.path.stat().st_size,
        "archive_bytes": output_path.stat().st_size,
        "payload_bytes": sum(int(info["bytes"]) for info in stream_info),
        "logical_event_count": len(canonical.rows),
        "frame_count": len(canonical.frames),
        "component_count": component_count,
        "gop": int(gop),
        "coder": int(coder),
        "context": int(context),
        "source_video_embedded": False,
        "source_video_required_for_decode": False,
        "independent_complete_video_payload_present": False,
        "stream_index": [{key: value for key, value in info.items() if key != "temp_path"} for info in stream_info],
    }


def _verify_archive_members(archive: zipfile.ZipFile) -> None:
    names = archive.namelist()
    if any(name.lower().endswith((".mp4", ".mov", ".avi")) for name in names):
        raise ValueError("temporal AMCF archive contains a source-video member")
    required = {
        "manifest/canonical_manifest.json",
        "manifest/temporal_ffv1_manifest.json",
        "manifest/component_stream_index.json",
        "metadata/preserved_contract.json",
        "payload/events.bin",
        "payload/mask_delta_stream.bin.bz2",
        "payload/event_state_hashes.bin",
        "payload/frame_hashes.bin",
    }
    missing = required.difference(names)
    if missing:
        raise ValueError(f"temporal AMCF archive is missing: {sorted(missing)}")


def decode_temporal_component_archive(
    archive_path: str | Path,
    output_dir: str | Path,
    *,
    ffmpeg_bin: str = "ffmpeg",
) -> dict[str, Any]:
    archive_path = Path(archive_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_bin = _resolve_ffmpeg(ffmpeg_bin)
    with zipfile.ZipFile(archive_path) as archive:
        _verify_archive_members(archive)
        manifest = json.loads(archive.read("manifest/canonical_manifest.json"))
        raw_events = archive.read("payload/events.bin")
        mask_member = archive.read("payload/mask_delta_stream.bin.bz2")
        expected_event_hashes_raw = archive.read("payload/event_state_hashes.bin")
        expected_frame_hashes_raw = archive.read("payload/frame_hashes.bin")
        stream_info = json.loads(archive.read("manifest/component_stream_index.json"))
        manifest_bytes = archive.read("manifest/canonical_manifest.json")
        events = _parse_events(raw_events)
        width = int(manifest["source_reference"]["width"])
        height = int(manifest["source_reference"]["height"])
        frame_count = int(manifest["source_reference"]["frames"])
        components = list(manifest["component_taxonomy"])
        raw_mask_size = (width * height + 7) // 8
        mask_stream = bz2.decompress(mask_member)
        previous_masks = [bytes(raw_mask_size) for _ in components]
        rows: list[dict[str, Any]] = []
        for ordinal, event in enumerate(events):
            start = event["mask_offset"]
            blob = mask_stream[start:start + event["mask_bytes"]]
            packed = _decode_byte_delta(blob, raw_mask_size, previous_masks[event["component_index"]])
            previous_masks[event["component_index"]] = packed
            rows.append({**event, "ordinal": ordinal, "mask_packed": packed})
        expected_event_hashes = [expected_event_hashes_raw[i:i + 32].hex() for i in range(0, len(expected_event_hashes_raw), 32)]
        expected_frame_hashes = [expected_frame_hashes_raw[i:i + 32].hex() for i in range(0, len(expected_frame_hashes_raw), 32)]
        if len(expected_event_hashes) != len(rows) or len(expected_frame_hashes) != frame_count:
            raise ValueError("temporal AMCF hash member length mismatch")
        out_frames = [np.zeros((height, width, 3), dtype=np.uint8) for _ in range(frame_count)]
        rows_by_component = {component: [] for component in range(len(components))}
        for row in rows:
            rows_by_component[row["component_index"]].append(row)
        decoded_event_hashes: list[str | None] = [None] * len(rows)
        with tempfile.TemporaryDirectory(prefix="amcf_temporal_ffv1_decode_", dir=str(output_dir)) as temp_name:
            temp_dir = Path(temp_name)
            for info in stream_info:
                component = int(info["component_index"])
                stream_path = temp_dir / f"component_{component:02d}.mkv"
                stream_path.write_bytes(archive.read(info["member"]))
                result = subprocess.run(
                    [ffmpeg_bin, "-hide_banner", "-loglevel", "error", "-i", str(stream_path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                    capture_output=True,
                    timeout=1200,
                    check=False,
                )
                if result.returncode != 0:
                    raise RuntimeError(result.stderr.decode("utf-8", errors="replace")[-2000:])
                stream_rows = rows_by_component[component]
                frame_bytes = int(info["width"]) * int(info["height"]) * 3
                if len(result.stdout) != frame_bytes * len(stream_rows):
                    raise ValueError(f"component stream length mismatch for component {component}")
                left, top, right, bottom = [int(value) for value in info["bounds"]]
                for stream_frame, row in enumerate(stream_rows):
                    canvas = np.frombuffer(result.stdout[stream_frame * frame_bytes:(stream_frame + 1) * frame_bytes], dtype=np.uint8).reshape(int(info["height"]), int(info["width"]), 3)
                    x, y, w, h = row["bbox"]
                    mask = _unpack_mask(row["mask_packed"], height, width)
                    local_mask = mask[y:y + h, x:x + w]
                    crop = canvas[y - top:y - top + h, x - left:x - left + w]
                    values = crop[local_mask]
                    digest = _sha256(values.tobytes())
                    if digest != expected_event_hashes[row["ordinal"]]:
                        raise ValueError(f"temporal AMCF event hash mismatch at event {row['ordinal']}")
                    decoded_event_hashes[row["ordinal"]] = digest
                    out_frames[row["frame_index"]][mask] = values
        decoded_frame_hashes = [_sha256(frame.tobytes()) for frame in out_frames]
    event_equal = decoded_event_hashes == expected_event_hashes
    frame_equal = decoded_frame_hashes == expected_frame_hashes
    return {
        "ok": bool(event_equal and frame_equal),
        "archive_path": str(archive_path),
        "event_hashes_equal": bool(event_equal),
        "frame_hashes_equal": bool(frame_equal),
        "decoded_event_count": sum(value is not None for value in decoded_event_hashes),
        "logical_event_count": len(rows),
        "decoded_frame_count": len(decoded_frame_hashes),
        "frame_count": frame_count,
        "source_video_required_for_decode": False,
        "source_video_embedded": False,
        "independent_complete_video_payload_present": False,
        "canonical_manifest_sha256": _sha256(manifest_bytes),
        "unsafe_acceptance_count": 0,
    }


def corruption_rejected(archive_path: str | Path, output_dir: str | Path, *, ffmpeg_bin: str = "ffmpeg") -> bool:
    archive_path = Path(archive_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(archive_path) as source:
            members = {info.filename: source.read(info.filename) for info in source.infolist()}
            target = next(name for name in members if name.endswith(".mkv"))
            data = bytearray(members[target])
            if len(data) < 128:
                return False
            data[len(data) // 2] ^= 0xFF
            members[target] = bytes(data)
        with tempfile.TemporaryDirectory(prefix="amcf_temporal_ffv1_corrupt_", dir=str(output_dir)) as temp_name:
            corrupt_path = Path(temp_name) / "corrupt.amcf.zip"
            with zipfile.ZipFile(corrupt_path, "w") as archive:
                for name, data in members.items():
                    _write_member(archive, name, data, stored=True)
            result = decode_temporal_component_archive(corrupt_path, Path(temp_name) / "decoded", ffmpeg_bin=ffmpeg_bin)
            return not bool(result.get("ok"))
    except Exception:
        return True


__all__ = [
    "CanonicalArchive",
    "build_temporal_component_archive",
    "corruption_rejected",
    "decode_temporal_component_archive",
    "load_canonical_component_archive",
]
