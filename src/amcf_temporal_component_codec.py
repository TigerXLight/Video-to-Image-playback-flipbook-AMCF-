"""Motion-referenced temporal component archive codec for local Main.

This codec is intentionally separate from the generic changed-region archive.
It uses periodic keyframes and one packed XOR-residual payload per delta
frame.  The preservation path uses lossless PNG keyframes and exact residuals;
each residual tile may read its prediction from a locally motion-shifted
location in the previous reconstructed frame.  The archive is self-contained
and decoded frames are checked by SHA-256 before acceptance.  Lossy WebP
variants remain opt-in experiments and are never silently substituted for the
preservation path.
"""

from __future__ import annotations

import io
import json
import struct
import zipfile
from pathlib import Path
from typing import Any

from amcf_component_event_archive import load_source_frame_manifest
from amcf_quality_metrics import compare_ppm_frame_folders, read_ppm, sha256_bytes, write_ppm


SCHEMA = "amcf-temporal-component-archive-v1"
PACK_MAGIC = b"AMCFTR01"
GROUPED_PACK_MAGIC = b"AMCFTR02"
PACK_HEADER = struct.Struct(">I")
RECORD_HEADER = struct.Struct(">HHHHHHI")
GROUPED_HEADER = struct.Struct(">II")
GROUPED_RECORD_HEADER = struct.Struct(">HHHHHHII")


def _require_image_dependencies() -> tuple[Any, Any]:
    try:
        import numpy as np
        from PIL import Image
    except ImportError as error:
        raise RuntimeError("numpy and Pillow are required for temporal codec") from error
    return np, Image


def _encode_keyframe(
    pixels: bytes,
    width: int,
    height: int,
    quality: int,
    *,
    lossless: bool = False,
) -> tuple[bytes, str]:
    _, image_type = _require_image_dependencies()
    image = image_type.frombytes("RGB", (width, height), pixels)
    stream = io.BytesIO()
    if lossless:
        # Lossless WebP keeps the preservation guarantee while usually
        # producing a smaller keyframe than PNG for photographic frames.
        image.save(stream, format="WEBP", lossless=True, method=6)
        return stream.getvalue(), "webp"
    image.save(stream, format="WEBP", quality=max(1, min(100, int(quality))), method=4)
    return stream.getvalue(), "webp"


def _decode_keyframe(payload: bytes) -> tuple[int, int, bytes]:
    _, image_type = _require_image_dependencies()
    try:
        with image_type.open(io.BytesIO(payload)) as image:
            rgb = image.convert("RGB")
            rgb.load()
            return rgb.width, rgb.height, rgb.tobytes()
    except (OSError, ValueError) as error:
        raise ValueError("invalid temporal keyframe payload") from error


def _estimate_translation(previous: bytes, current: bytes, width: int, height: int) -> tuple[int, int, str]:
    try:
        import cv2
        import numpy as np
    except ImportError:
        return 0, 0, "no_op_dependency_fallback"
    previous_array = np.frombuffer(previous, dtype=np.uint8).reshape(height, width, 3)
    current_array = np.frombuffer(current, dtype=np.uint8).reshape(height, width, 3)
    previous_gray = cv2.cvtColor(previous_array, cv2.COLOR_RGB2GRAY).astype(np.float32)
    current_gray = cv2.cvtColor(current_array, cv2.COLOR_RGB2GRAY).astype(np.float32)
    try:
        shift, _response = cv2.phaseCorrelate(previous_gray, current_gray)
        return int(round(shift[0])), int(round(shift[1])), "opencv_phase_correlation"
    except cv2.error:
        return 0, 0, "opencv_phase_correlation_failed_fallback"


def _translated_prediction(previous: bytes, current: bytes, width: int, height: int, dx: int, dy: int) -> Any:
    np, _ = _require_image_dependencies()
    previous_array = np.frombuffer(previous, dtype=np.uint8).reshape(height, width, 3)
    current_array = np.frombuffer(current, dtype=np.uint8).reshape(height, width, 3)
    y_indices = np.clip(np.arange(height)[:, None] - int(dy), 0, height - 1)
    x_indices = np.clip(np.arange(width)[None, :] - int(dx), 0, width - 1)
    prediction = previous_array[y_indices, x_indices]
    return prediction, current_array


def _encode_quantized_residual(
    previous: bytes,
    current: bytes,
    width: int,
    height: int,
    dx: int,
    dy: int,
    residual_step: int,
    residual_quality: int | None = None,
) -> tuple[bytes, bytes, int]:
    if residual_step <= 0:
        raise ValueError("residual_step must be positive")
    np, image_type = _require_image_dependencies()
    prediction, current_array = _translated_prediction(previous, current, width, height, dx, dy)
    difference = current_array.astype(np.int16) - prediction.astype(np.int16)
    quantized = np.rint(difference / float(residual_step)).astype(np.int16)
    quantized = np.clip(quantized, -128, 127)
    reconstructed = np.clip(prediction.astype(np.int16) + quantized * int(residual_step), 0, 255).astype(np.uint8)
    residual_image = image_type.fromarray((quantized + 128).astype(np.uint8), "RGB")
    stream = io.BytesIO()
    if residual_quality is None:
        residual_image.save(stream, format="WEBP", lossless=True, method=4)
    else:
        residual_image.save(stream, format="WEBP", lossless=False, quality=max(1, min(100, int(residual_quality))), method=4)
    return stream.getvalue(), reconstructed.tobytes(), int(np.max(np.abs(current_array.astype(np.int16) - reconstructed.astype(np.int16))))


def _decode_quantized_residual(
    previous: bytes,
    payload: bytes,
    width: int,
    height: int,
    dx: int,
    dy: int,
    residual_step: int,
) -> bytes:
    np, image_type = _require_image_dependencies()
    try:
        with image_type.open(io.BytesIO(payload)) as image:
            residual_image = image.convert("RGB")
            residual_image.load()
    except (OSError, ValueError) as error:
        raise ValueError("invalid quantized residual payload") from error
    if residual_image.size != (width, height):
        raise ValueError("quantized residual dimensions mismatch")
    prediction, _current_unused = _translated_prediction(previous, previous, width, height, dx, dy)
    quantized = np.asarray(residual_image, dtype=np.int16) - 128
    reconstructed = np.clip(prediction.astype(np.int16) + quantized * int(residual_step), 0, 255).astype(np.uint8)
    return reconstructed.tobytes()


def _clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


def _crop_rgb(pixels: bytes, width: int, x: int, y: int, patch_width: int, patch_height: int) -> bytes:
    row_stride = width * 3
    patch_stride = patch_width * 3
    output = bytearray(patch_stride * patch_height)
    for row in range(patch_height):
        start = (y + row) * row_stride + x * 3
        target = row * patch_stride
        output[target:target + patch_stride] = pixels[start:start + patch_stride]
    return bytes(output)


def _xor_bytes(left: bytes, right: bytes) -> bytes:
    if len(left) != len(right):
        raise ValueError("residual operands differ in length")
    return bytes(a ^ b for a, b in zip(left, right))


def _pack_residuals(records: list[dict[str, Any]]) -> bytes:
    output = bytearray(PACK_MAGIC + PACK_HEADER.pack(len(records)))
    for record in records:
        payload = bytes(record["payload"])
        output.extend(RECORD_HEADER.pack(
            int(record["x"]), int(record["y"]), int(record["width"]), int(record["height"]),
            int(record["source_x"]), int(record["source_y"]), len(payload),
        ))
        output.extend(payload)
    return bytes(output)


def _pack_grouped_residuals(records: list[dict[str, Any]]) -> bytes:
    """Pack exact tile residuals into one shared compressed stream.

    The index remains explicit and deterministic, while a shared zlib stream
    avoids restarting the compressor for every tile.  This changes storage
    layout only; it does not quantize or discard residual bytes.
    """
    raw_stream = bytearray()
    index_rows: list[tuple[dict[str, Any], int, int]] = []
    for record in records:
        raw = bytes(record.get("raw_residual", b""))
        if not raw:
            import zlib
            raw = zlib.decompress(record["payload"])
        offset = len(raw_stream)
        raw_stream.extend(raw)
        index_rows.append((record, offset, len(raw)))
    import zlib
    compressed_stream = zlib.compress(bytes(raw_stream), 9)
    output = bytearray(GROUPED_PACK_MAGIC + GROUPED_HEADER.pack(len(index_rows), len(raw_stream)))
    for record, offset, size in index_rows:
        output.extend(GROUPED_RECORD_HEADER.pack(
            int(record["x"]), int(record["y"]), int(record["width"]), int(record["height"]),
            int(record["source_x"]), int(record["source_y"]), offset, size,
        ))
    output.extend(compressed_stream)
    return bytes(output)


def _unpack_residuals(payload: bytes, width: int, height: int) -> list[dict[str, Any]]:
    if payload.startswith(GROUPED_PACK_MAGIC):
        offset = len(GROUPED_PACK_MAGIC)
        if len(payload) < offset + GROUPED_HEADER.size:
            raise ValueError("invalid grouped temporal residual payload header")
        count, raw_size = GROUPED_HEADER.unpack_from(payload, offset)
        offset += GROUPED_HEADER.size
        rows: list[tuple[int, int, int, int, int, int, int, int]] = []
        for _ in range(count):
            if offset + GROUPED_RECORD_HEADER.size > len(payload):
                raise ValueError("truncated grouped temporal residual index")
            rows.append(GROUPED_RECORD_HEADER.unpack_from(payload, offset))
            offset += GROUPED_RECORD_HEADER.size
        import zlib
        try:
            raw_stream = zlib.decompress(payload[offset:])
        except zlib.error as error:
            raise ValueError("invalid grouped temporal residual stream") from error
        if len(raw_stream) != raw_size:
            raise ValueError("grouped temporal residual size mismatch")
        records: list[dict[str, Any]] = []
        for x, y, patch_width, patch_height, source_x, source_y, raw_offset, size in rows:
            if (
                patch_width <= 0 or patch_height <= 0 or
                x + patch_width > width or y + patch_height > height or
                source_x + patch_width > width or source_y + patch_height > height or
                raw_offset + size > len(raw_stream)
            ):
                raise ValueError("grouped temporal residual record exceeds frame bounds")
            records.append({
                "x": x, "y": y, "width": patch_width, "height": patch_height,
                "source_x": source_x, "source_y": source_y,
                "raw_residual": raw_stream[raw_offset:raw_offset + size],
            })
        return records
    if not payload.startswith(PACK_MAGIC) or len(payload) < len(PACK_MAGIC) + PACK_HEADER.size:
        raise ValueError("invalid temporal residual payload header")
    offset = len(PACK_MAGIC)
    count = PACK_HEADER.unpack_from(payload, offset)[0]
    offset += PACK_HEADER.size
    records: list[dict[str, Any]] = []
    for _ in range(count):
        if offset + RECORD_HEADER.size > len(payload):
            raise ValueError("truncated temporal residual record")
        x, y, patch_width, patch_height, source_x, source_y, size = RECORD_HEADER.unpack_from(payload, offset)
        offset += RECORD_HEADER.size
        if (
            patch_width <= 0 or patch_height <= 0 or
            x + patch_width > width or y + patch_height > height or
            source_x + patch_width > width or source_y + patch_height > height or
            offset + size > len(payload)
        ):
            raise ValueError("temporal residual record exceeds frame bounds")
        records.append({
            "x": x, "y": y, "width": patch_width, "height": patch_height,
            "source_x": source_x, "source_y": source_y,
            "payload": payload[offset:offset + size],
        })
        offset += size
    if offset != len(payload):
        raise ValueError("unexpected trailing temporal residual bytes")
    return records


def _paste_rgb(base: bytes, patch: bytes, width: int, x: int, y: int, patch_width: int, patch_height: int) -> bytes:
    output = bytearray(base)
    row_stride = width * 3
    patch_stride = patch_width * 3
    for row in range(patch_height):
        start = (y + row) * row_stride + x * 3
        source = row * patch_stride
        output[start:start + patch_stride] = patch[source:source + patch_stride]
    return bytes(output)


def _residual_records(
    previous: bytes,
    current: bytes,
    width: int,
    height: int,
    tile_size: int,
    dx: int,
    dy: int,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for y in range(0, height, tile_size):
        patch_height = min(tile_size, height - y)
        for x in range(0, width, tile_size):
            patch_width = min(tile_size, width - x)
            source_x = _clamp(x - dx, 0, width - patch_width)
            source_y = _clamp(y - dy, 0, height - patch_height)
            current_patch = _crop_rgb(current, width, x, y, patch_width, patch_height)
            prediction = _crop_rgb(previous, width, source_x, source_y, patch_width, patch_height)
            residual = _xor_bytes(current_patch, prediction)
            if not any(residual) and source_x == x and source_y == y:
                continue
            import zlib
            compressed = zlib.compress(residual, 9)
            records.append({
                "x": x, "y": y, "width": patch_width, "height": patch_height,
                "source_x": source_x, "source_y": source_y,
                "payload": compressed,
                "raw_residual": residual,
                "raw_bytes": len(residual),
            })
    return records


def _tile_motion_vector(
    previous: bytes,
    current: bytes,
    width: int,
    height: int,
    x: int,
    y: int,
    patch_width: int,
    patch_height: int,
    initial_dx: int,
    initial_dy: int,
    search_radius: int,
) -> tuple[int, int]:
    """Choose a local integer translation using a small deterministic search.

    The selected vector only changes the prediction.  The residual remains an
    exact XOR patch, so a poor vector increases payload size but cannot alter
    the reconstructed frame.
    """
    np, _ = _require_image_dependencies()
    previous_array = np.frombuffer(previous, dtype=np.uint8).reshape(height, width, 3)
    current_array = np.frombuffer(current, dtype=np.uint8).reshape(height, width, 3)
    current_patch = current_array[y:y + patch_height, x:x + patch_width].astype(np.int16)
    current_luma = (
        current_patch[..., 0] * 30 + current_patch[..., 1] * 59 + current_patch[..., 2] * 11
    ) / 100.0
    best: tuple[float, int, int] | None = None
    for dy in range(initial_dy - search_radius, initial_dy + search_radius + 1):
        source_y = _clamp(y - dy, 0, height - patch_height)
        for dx in range(initial_dx - search_radius, initial_dx + search_radius + 1):
            source_x = _clamp(x - dx, 0, width - patch_width)
            candidate = previous_array[source_y:source_y + patch_height, source_x:source_x + patch_width].astype(np.int16)
            candidate_luma = (
                candidate[..., 0] * 30 + candidate[..., 1] * 59 + candidate[..., 2] * 11
            ) / 100.0
            # Sample larger tiles more sparsely to keep the local search
            # bounded while retaining enough texture to distinguish local
            # motion from a global shift.
            sample_step = max(4, min(patch_width, patch_height) // 8)
            error = float(np.mean(np.abs(
                current_luma[::sample_step, ::sample_step] -
                candidate_luma[::sample_step, ::sample_step]
            )))
            item = (error, dx, dy)
            if best is None or item < best:
                best = item
    assert best is not None
    return int(best[1]), int(best[2])


def _local_motion_residual_records(
    previous: bytes,
    current: bytes,
    width: int,
    height: int,
    tile_size: int,
    initial_dx: int,
    initial_dy: int,
    search_radius: int,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for y in range(0, height, tile_size):
        patch_height = min(tile_size, height - y)
        for x in range(0, width, tile_size):
            patch_width = min(tile_size, width - x)
            dx, dy = _tile_motion_vector(
                previous, current, width, height, x, y, patch_width, patch_height,
                initial_dx, initial_dy, search_radius,
            )
            source_x = _clamp(x - dx, 0, width - patch_width)
            source_y = _clamp(y - dy, 0, height - patch_height)
            current_patch = _crop_rgb(current, width, x, y, patch_width, patch_height)
            prediction = _crop_rgb(previous, width, source_x, source_y, patch_width, patch_height)
            residual = _xor_bytes(current_patch, prediction)
            if not any(residual) and source_x == x and source_y == y:
                continue
            import zlib
            compressed = zlib.compress(residual, 9)
            records.append({
                "x": x, "y": y, "width": patch_width, "height": patch_height,
                "source_x": source_x, "source_y": source_y,
                "payload": compressed,
                "raw_residual": residual,
                "raw_bytes": len(residual),
            })
    return records


def build_temporal_component_archive(
    source_manifest_path: str | Path,
    output_archive_path: str | Path,
    *,
    keyframe_interval: int = 24,
    tile_size: int = 64,
    keyframe_quality: int = 90,
    source_size_ceiling_bytes: int | None = None,
    residual_codec: str = "packed_motion_xor_zlib",
    residual_step: int = 4,
    residual_quality: int | None = None,
    local_motion: bool = True,
    motion_search_radius: int = 1,
) -> dict[str, Any]:
    if keyframe_interval <= 0 or tile_size <= 0:
        raise ValueError("keyframe_interval and tile_size must be positive")
    if residual_codec not in {"packed_motion_xor_zlib", "quantized_residual_webp", "quantized_residual_webp_lossy"}:
        raise ValueError(f"unsupported residual codec: {residual_codec}")
    source_manifest_path = Path(source_manifest_path)
    source_root = source_manifest_path.parent
    manifest = load_source_frame_manifest(source_manifest_path)
    width = int(manifest["width"])
    height = int(manifest["height"])
    entries = sorted(manifest["frame_entries"], key=lambda item: int(item["frame_index"]))
    if not entries:
        raise ValueError("source manifest has no frames")
    source_video = manifest.get("source_video") if isinstance(manifest.get("source_video"), dict) else {}
    ceiling = source_size_ceiling_bytes or int(source_video.get("bytes") or 0) or None
    if ceiling is None:
        ceiling = sum((source_root / str(item["file"])).stat().st_size for item in entries)

    output_archive_path = Path(output_archive_path)
    output_archive_path.parent.mkdir(parents=True, exist_ok=True)
    payloads: dict[str, bytes] = {}
    frame_rows: list[dict[str, Any]] = []
    previous_reconstructed: bytes | None = None
    motion_methods: set[str] = set()
    total_residual_raw = 0
    total_residual_compressed = 0

    for position, entry in enumerate(entries):
        frame_index = int(entry["frame_index"])
        frame_path = source_root / str(entry["file"])
        frame_width, frame_height, current = read_ppm(frame_path)
        if (frame_width, frame_height) != (width, height):
            raise ValueError("source frame dimensions differ from manifest")
        keyframe = previous_reconstructed is None or position % keyframe_interval == 0
        if keyframe:
            keyframe_lossless = residual_codec == "packed_motion_xor_zlib"
            payload, keyframe_format = _encode_keyframe(
                current, width, height, keyframe_quality, lossless=keyframe_lossless,
            )
            payload_path = f"payloads/keyframes/frame_{frame_index:06d}.{keyframe_format}"
            payloads[payload_path] = payload
            decoded_width, decoded_height, reconstructed = _decode_keyframe(payload)
            if (decoded_width, decoded_height) != (width, height):
                raise ValueError("encoded keyframe dimensions differ from source")
            if residual_codec == "packed_motion_xor_zlib" and reconstructed != current:
                raise ValueError("lossless keyframe changed source pixels")
            frame_rows.append({
                "frame_index": frame_index,
                "frame_id": f"frame_{frame_index:06d}",
                "type": "keyframe",
                "dependency": None,
                "payload_path": payload_path,
                "payload_bytes": len(payload),
                "payload_sha256": sha256_bytes(payload),
                "source_sha256": sha256_bytes(current),
                "reconstructed_sha256": sha256_bytes(reconstructed),
            })
            previous_reconstructed = reconstructed
            continue

        dx, dy, method = _estimate_translation(previous_reconstructed, current, width, height)
        motion_methods.add(method)
        if residual_codec in {"quantized_residual_webp", "quantized_residual_webp_lossy"}:
            payload, reconstructed, reconstruction_max_error = _encode_quantized_residual(
                previous_reconstructed,
                current,
                width,
                height,
                dx,
                dy,
                residual_step,
                residual_quality if residual_codec == "quantized_residual_webp_lossy" else None,
            )
            payload_path = f"payloads/deltas/frame_{frame_index:06d}.webp"
            payloads[payload_path] = payload
            frame_rows.append({
                "frame_index": frame_index,
                "frame_id": f"frame_{frame_index:06d}",
                "type": "delta",
                "dependency": f"frame_{entries[position - 1]['frame_index']:06d}",
                "payload_path": payload_path,
                "payload_bytes": len(payload),
                "payload_sha256": sha256_bytes(payload),
                "motion": {"dx": dx, "dy": dy, "estimator": method},
                "residual_codec": residual_codec,
                "residual_step": residual_step,
                "reconstruction_max_error": reconstruction_max_error,
                "source_sha256": sha256_bytes(current) if residual_codec == "packed_motion_xor_zlib" else None,
                "reconstructed_sha256": sha256_bytes(reconstructed),
            })
            total_residual_raw += width * height * 3
            total_residual_compressed += len(payload)
            previous_reconstructed = reconstructed
            continue
        candidates = [(dx, dy), (0, 0)]
        if dx or dy:
            candidates.extend([(dx - 1, dy), (dx + 1, dy), (dx, dy - 1), (dx, dy + 1)])
        best: tuple[int, int, list[dict[str, Any]], bytes] | None = None
        for candidate_dx, candidate_dy in candidates:
            if local_motion:
                records = _local_motion_residual_records(
                    previous_reconstructed, current, width, height, tile_size,
                    candidate_dx, candidate_dy, max(0, int(motion_search_radius)),
                )
            else:
                records = _residual_records(
                    previous_reconstructed, current, width, height, tile_size,
                    candidate_dx, candidate_dy,
                )
            packed = _pack_grouped_residuals(records) if local_motion else _pack_residuals(records)
            if best is None or len(packed) < len(best[3]):
                best = (candidate_dx, candidate_dy, records, packed)
        assert best is not None
        best_dx, best_dy, records, packed = best
        payload_path = f"payloads/deltas/frame_{frame_index:06d}.bin"
        payloads[payload_path] = packed
        for record in records:
            total_residual_raw += int(record["raw_bytes"])
            total_residual_compressed += len(record["payload"])
        frame_rows.append({
            "frame_index": frame_index,
            "frame_id": f"frame_{frame_index:06d}",
            "type": "delta",
            "dependency": f"frame_{entries[position - 1]['frame_index']:06d}",
            "payload_path": payload_path,
            "payload_bytes": len(packed),
            "payload_sha256": sha256_bytes(packed),
            "motion": {"dx": best_dx, "dy": best_dy, "estimator": method},
            "tile_size": tile_size,
            "record_count": len(records),
        })
        # The packed XOR records reconstruct the current source exactly from
        # the encoder's previous reconstructed state.
        prediction_base = previous_reconstructed
        reconstructed = previous_reconstructed
        for record in records:
            prediction = _crop_rgb(prediction_base, width, record["source_x"], record["source_y"], record["width"], record["height"])
            residual = record.get("raw_residual") or __import__("zlib").decompress(record["payload"])
            patch = _xor_bytes(prediction, residual)
            reconstructed = _paste_rgb(reconstructed, patch, width, record["x"], record["y"], record["width"], record["height"])
        frame_rows[-1]["reconstructed_sha256"] = sha256_bytes(reconstructed)
        if residual_codec == "packed_motion_xor_zlib" and reconstructed != current:
            raise ValueError("lossless residual reconstruction changed source pixels")
        frame_rows[-1]["source_sha256"] = sha256_bytes(current)
        previous_reconstructed = reconstructed

    checksums = [
        {"frame_index": int(entry["frame_index"]), "frame_id": f"frame_{int(entry['frame_index']):06d}", "sha256": str(entry.get("sha256", ""))}
        for entry in entries
    ]
    archive_manifest = {
        "amcf_schema": SCHEMA,
        "frame_count": len(entries),
        "width": width,
        "height": height,
        "fps": int(manifest["fps"]),
        "keyframe_interval": keyframe_interval,
        "tile_size": tile_size,
        "keyframe_quality": keyframe_quality,
        "payload_model": residual_codec,
        "motion_model": "per_tile_integer_translation_search" if local_motion else "integer_translation_phase_correlation",
        "local_motion": bool(local_motion),
        "motion_search_radius": int(motion_search_radius),
        "preservation_mode": "lossless_exact_residual" if residual_codec == "packed_motion_xor_zlib" else "quality_gated_experimental",
        "residual_codec": residual_codec,
        "residual_pack": "grouped_shared_zlib" if local_motion and residual_codec == "packed_motion_xor_zlib" else "per_tile_zlib",
        "residual_step": residual_step,
        "residual_quality": residual_quality,
        "frames": frame_rows,
        "source_frame_hashes": checksums,
        "archive_size_ceiling": {"ceiling_bytes": ceiling, "under_source_size_ceiling": None},
        "dependency_status": {"numpy": True, "pillow": True, "opencv_motion_estimation": "opencv_phase_correlation" in motion_methods},
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "real_printer_required": False,
            "real_reader_required": False,
            "real_player_required": False,
            "real_scanner_required": False,
            "real_usb_required": False,
        },
        "unsafe_acceptance_count": 0,
    }
    def write_archive() -> None:
        with zipfile.ZipFile(output_archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            archive.writestr("manifest.json", json.dumps(archive_manifest, indent=2, sort_keys=True).encode("utf-8"))
            for path, payload in payloads.items():
                archive.writestr(path, payload)

    write_archive()
    archive_bytes = output_archive_path.stat().st_size
    under_ceiling = archive_bytes <= int(ceiling)
    archive_manifest["archive_size_ceiling"]["under_source_size_ceiling"] = under_ceiling
    # Persist the final ceiling result inside the archive manifest as well as
    # in the returned report.
    write_archive()
    archive_bytes = output_archive_path.stat().st_size
    return {
        "ok": True,
        "archive_path": str(output_archive_path),
        "amcf_schema": SCHEMA,
        "frame_count": len(entries),
        "keyframe_count": sum(row["type"] == "keyframe" for row in frame_rows),
        "delta_frame_count": sum(row["type"] == "delta" for row in frame_rows),
        "archive_bytes": archive_bytes,
        "source_size_ceiling_bytes": int(ceiling),
        "under_source_size_ceiling": under_ceiling,
        "motion_methods": sorted(motion_methods),
        "residual_raw_bytes": total_residual_raw,
        "residual_compressed_bytes": total_residual_compressed,
        "manifest": archive_manifest,
        "claim_boundary": archive_manifest["claim_boundary"],
        "unsafe_acceptance_count": 0,
    }


def decode_temporal_component_archive(archive_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    output_dir = Path(output_dir)
    frames_dir = output_dir / "decoded_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "r") as archive:
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
        if manifest.get("amcf_schema") != SCHEMA:
            raise ValueError("unsupported temporal component archive schema")
        width = int(manifest["width"])
        height = int(manifest["height"])
        previous: bytes | None = None
        decoded = 0
        for row in manifest["frames"]:
            payload = archive.read(row["payload_path"])
            if sha256_bytes(payload) != row["payload_sha256"]:
                raise ValueError("temporal payload checksum mismatch")
            if row["type"] == "keyframe":
                decoded_width, decoded_height, current = _decode_keyframe(payload)
                if (decoded_width, decoded_height) != (width, height):
                    raise ValueError("temporal keyframe dimensions mismatch")
            elif row["type"] == "delta":
                if previous is None:
                    raise ValueError("delta frame has no previous dependency")
                if row.get("residual_codec") in {"quantized_residual_webp", "quantized_residual_webp_lossy"}:
                    motion = row.get("motion") or {}
                    current = _decode_quantized_residual(
                        previous,
                        payload,
                        width,
                        height,
                        int(motion.get("dx", 0)),
                        int(motion.get("dy", 0)),
                        int(row.get("residual_step", manifest.get("residual_step", 1))),
                    )
                else:
                    prediction_base = previous
                    current = previous
                    for record in _unpack_residuals(payload, width, height):
                        import zlib
                        residual = record.get("raw_residual") or zlib.decompress(record["payload"])
                        expected = int(record["width"]) * int(record["height"]) * 3
                        if len(residual) != expected:
                            raise ValueError("temporal residual length mismatch")
                        prediction = _crop_rgb(prediction_base, width, record["source_x"], record["source_y"], record["width"], record["height"])
                        patch = _xor_bytes(prediction, residual)
                        current = _paste_rgb(current, patch, width, record["x"], record["y"], record["width"], record["height"])
            else:
                raise ValueError("unsupported temporal frame type")
            expected_frame_hash = row.get("reconstructed_sha256")
            if not isinstance(expected_frame_hash, str) or sha256_bytes(current) != expected_frame_hash:
                raise ValueError(f"decoded temporal frame checksum mismatch: {row.get('frame_index')}")
            if manifest.get("preservation_mode") == "lossless_exact_residual":
                expected_source_hash = row.get("source_sha256")
                if not isinstance(expected_source_hash, str) or sha256_bytes(current) != expected_source_hash:
                    raise ValueError(f"decoded temporal source mismatch: {row.get('frame_index')}")
            write_ppm(frames_dir / f"frame_{int(row['frame_index']):03d}.ppm", width, height, current)
            previous = current
            decoded += 1
    return {
        "ok": True,
        "archive_path": str(archive_path),
        "decoded_frames_dir": str(frames_dir),
        "frame_count": decoded,
        "unsafe_acceptance_count": 0,
        "claim_boundary": manifest["claim_boundary"],
    }


def assess_temporal_component_archive(
    source_manifest_path: str | Path,
    archive_path: str | Path,
    decoded_output_dir: str | Path,
    *,
    max_mae: float = 12.0,
    min_ssim: float = 0.85,
) -> dict[str, Any]:
    decoded = decode_temporal_component_archive(archive_path, decoded_output_dir)
    source_manifest = load_source_frame_manifest(source_manifest_path)
    source_frames = Path(source_manifest_path).parent / "frames"
    quality = compare_ppm_frame_folders(source_frames, Path(decoded["decoded_frames_dir"]))
    passed = (
        decoded["ok"] and quality["actual_frame_count"] == quality["expected_frame_count"] and
        quality["mean_absolute_error"] is not None and quality["mean_absolute_error"] <= max_mae and
        quality["mean_ssim"] is not None and quality["mean_ssim"] >= min_ssim
    )
    return {
        "decoded": decoded,
        "quality": quality,
        "visual_thresholds": {"max_mae": max_mae, "min_ssim": min_ssim},
        "visual_passed": bool(passed),
        "unsafe_acceptance_count": 0,
        "claim_boundary": decoded["claim_boundary"],
    }
