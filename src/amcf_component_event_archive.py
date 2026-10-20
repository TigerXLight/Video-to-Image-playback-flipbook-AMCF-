from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import struct
import zipfile
from pathlib import Path
from typing import Any

from amcf_adaptive_component_scheduler import ComponentUpdatePolicy, decide_component_update
from amcf_diagnostic_state import (
    diagnostic_state_summary,
    diagnostic_tracks_for_frame,
    load_diagnostic_state_manifest,
    rasterize_track_mask,
    validate_diagnostic_state_manifest,
)
from amcf_quality_metrics import ppm_bytes, read_ppm, sha256_bytes, write_ppm


AMCF_COMPONENT_EVENT_SCHEMA = "amcf-component-event-archive-v1"
FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)
MASKED_RGB_MAGIC = b"AMCF-MASKED-RGB-V1\n"


def optional_dependency_status() -> dict[str, bool]:
    return {
        "pillow_available": importlib.util.find_spec("PIL") is not None,
        "opencv_available": importlib.util.find_spec("cv2") is not None,
        "skimage_available": importlib.util.find_spec("skimage") is not None,
    }


def _write_zip_member(zf: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, payload)


def _encode_webp(width: int, height: int, pixels: bytes, *, quality: int | None = None) -> bytes:
    from PIL import Image

    image = Image.frombytes("RGB", (width, height), pixels)
    buffer = io.BytesIO()
    if quality is None:
        image.save(buffer, format="WEBP", lossless=True)
    else:
        image.save(buffer, format="WEBP", lossless=False, quality=max(1, min(100, int(quality))), method=4)
    return buffer.getvalue()


def _decode_webp(payload: bytes) -> tuple[int, int, bytes]:
    from PIL import Image

    with Image.open(io.BytesIO(payload)) as image:
        rgb = image.convert("RGB")
        return rgb.width, rgb.height, rgb.tobytes()


def _changed_bbox(previous: bytes, current: bytes, width: int, height: int) -> tuple[list[int] | None, int]:
    if len(previous) != len(current):
        raise ValueError("frame payload lengths differ")
    min_x = width
    min_y = height
    max_x = -1
    max_y = -1
    changed_pixels = 0
    for pixel_index in range(width * height):
        offset = pixel_index * 3
        if previous[offset:offset + 3] != current[offset:offset + 3]:
            x = pixel_index % width
            y = pixel_index // width
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            changed_pixels += 1
    if changed_pixels == 0:
        return None, 0
    return [min_x, min_y, max_x - min_x + 1, max_y - min_y + 1], changed_pixels


def _opencv_changed_region(previous: bytes, current: bytes, width: int, height: int) -> tuple[list[int] | None, int, dict[str, Any]]:
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("OpenCV segmentation requested but cv2/numpy are not importable") from exc

    prev = np.frombuffer(previous, dtype=np.uint8).reshape((height, width, 3))
    curr = np.frombuffer(current, dtype=np.uint8).reshape((height, width, 3))
    diff = cv2.absdiff(prev, curr)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    changed_pixels = int(np.count_nonzero(mask))
    if changed_pixels == 0:
        return None, 0, {"strategy": "opencv_changed_region", "contour_count": 0, "changed_pixels": 0}
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c) >= 1.0]
    if not contours:
        return _changed_bbox(previous, current, width, height)[0], changed_pixels, {
            "strategy": "opencv_changed_region",
            "contour_count": 0,
            "changed_pixels": changed_pixels,
        }
    x_values: list[int] = []
    y_values: list[int] = []
    contour_boxes: list[list[int]] = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contour_boxes.append([int(x), int(y), int(w), int(h)])
        x_values.extend([int(x), int(x + w)])
        y_values.extend([int(y), int(y + h)])
    x0 = min(x_values)
    y0 = min(y_values)
    x1 = max(x_values)
    y1 = max(y_values)
    return [x0, y0, x1 - x0, y1 - y0], changed_pixels, {
        "strategy": "opencv_changed_region",
        "contour_count": len(contours),
        "contour_bboxes": contour_boxes,
        "changed_pixels": changed_pixels,
    }


def _crop_pixels(pixels: bytes, frame_width: int, bbox: list[int]) -> bytes:
    x, y, width, height = bbox
    out = bytearray()
    for row in range(y, y + height):
        start = (row * frame_width + x) * 3
        out.extend(pixels[start:start + width * 3])
    return bytes(out)


def _paste_patch(base: bytes, frame_width: int, bbox: list[int], patch_pixels: bytes) -> bytes:
    x, y, width, height = bbox
    out = bytearray(base)
    patch_offset = 0
    for row in range(y, y + height):
        start = (row * frame_width + x) * 3
        length = width * 3
        out[start:start + length] = patch_pixels[patch_offset:patch_offset + length]
        patch_offset += length
    return bytes(out)


def _encode_masked_rgb(width: int, height: int, pixels: bytes, mask: bytes) -> bytes:
    """Encode an exact RGB crop plus a bbox-local binary component mask."""
    expected_pixels = int(width) * int(height) * 3
    expected_mask = int(width) * int(height)
    if len(pixels) != expected_pixels or len(mask) != expected_mask:
        raise ValueError("masked RGB payload dimensions do not match pixel/mask lengths")
    return MASKED_RGB_MAGIC + struct.pack(">II", int(width), int(height)) + bytes(mask) + bytes(pixels)


def _decode_masked_rgb(payload: bytes) -> tuple[int, int, bytes, bytes]:
    header_size = len(MASKED_RGB_MAGIC) + 8
    if len(payload) < header_size or not payload.startswith(MASKED_RGB_MAGIC):
        raise ValueError("invalid masked RGB payload header")
    width, height = struct.unpack(">II", payload[len(MASKED_RGB_MAGIC):header_size])
    mask_size = int(width) * int(height)
    pixel_size = mask_size * 3
    if len(payload) != header_size + mask_size + pixel_size:
        raise ValueError("masked RGB payload length mismatch")
    mask_start = header_size
    pixels_start = mask_start + mask_size
    return int(width), int(height), payload[pixels_start:], payload[mask_start:pixels_start]


def _paste_masked_patch(
    base: bytes,
    frame_width: int,
    bbox: list[int],
    patch_pixels: bytes,
    mask: bytes,
) -> bytes:
    x, y, width, height = bbox
    expected_pixels = int(width) * int(height) * 3
    expected_mask = int(width) * int(height)
    if len(patch_pixels) != expected_pixels or len(mask) != expected_mask:
        raise ValueError("masked event payload does not match bbox")
    out = bytearray(base)
    for row in range(height):
        for column in range(width):
            mask_index = row * width + column
            if not mask[mask_index]:
                continue
            destination = ((y + row) * frame_width + (x + column)) * 3
            source = mask_index * 3
            out[destination:destination + 3] = patch_pixels[source:source + 3]
    return bytes(out)


def _payload_bytes(
    width: int,
    height: int,
    pixels: bytes,
    *,
    use_webp: bool,
    webp_quality: int | None = None,
) -> tuple[str, bytes]:
    if use_webp:
        format_name = "webp_lossless" if webp_quality is None else f"webp_lossy_q{int(webp_quality)}"
        return format_name, _encode_webp(width, height, pixels, quality=webp_quality)
    return "ppm_p6", ppm_bytes(width, height, pixels)


def _decode_payload(format_name: str, payload: bytes) -> tuple[int, int, bytes]:
    if format_name == "webp_lossless" or format_name.startswith("webp_lossy_q"):
        return _decode_webp(payload)
    if format_name == "ppm_p6":
        temp = io.BytesIO(payload)
        data = temp.getvalue()
        marker = data.find(b"\n255\n")
        if marker == -1:
            raise ValueError("invalid PPM patch payload")
        header = data[:marker + len(b"\n255\n")]
        parts = header.split()
        width = int(parts[1])
        height = int(parts[2])
        pixels = data[len(header):]
        if len(pixels) != width * height * 3:
            raise ValueError("PPM patch payload length mismatch")
        return width, height, pixels
    raise ValueError(f"unsupported payload format: {format_name}")


def _validate_diagnostic_state_contract(
    diagnostic_state: dict[str, Any],
    source_manifest: dict[str, Any],
    *,
    width: int,
    height: int,
    frame_count: int,
) -> None:
    source = diagnostic_state["source"]
    if int(source.get("frame_count", 0)) != int(frame_count):
        raise ValueError(
            "diagnostic state frame_count does not match source frame manifest: "
            f"{source.get('frame_count')} != {frame_count}"
        )
    diagnostic_width = int(source.get("width", 0))
    diagnostic_height = int(source.get("height", 0))
    if diagnostic_width <= 0 or diagnostic_height <= 0:
        raise ValueError("diagnostic state source dimensions must be positive")
    if diagnostic_width * height != diagnostic_height * width:
        raise ValueError(
            "diagnostic state and source frames have incompatible aspect ratios: "
            f"{diagnostic_width}x{diagnostic_height} vs {width}x{height}"
        )
    source_video = source_manifest.get("source_video")
    if isinstance(source_video, dict):
        source_sha = str(source_video.get("sha256") or "").lower()
        diagnostic_sha = str(source.get("sha256") or "").lower()
        if source_sha and diagnostic_sha and source_sha != diagnostic_sha:
            raise ValueError("diagnostic state source SHA-256 does not match source frame manifest")


def load_source_frame_manifest(path: str | Path) -> dict[str, Any]:
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    for key in ("frame_count", "width", "height", "fps", "frame_entries"):
        if key not in manifest:
            raise ValueError(f"source frame manifest missing {key}")
    return manifest


def build_component_event_archive(
    source_manifest_path: str | Path,
    output_archive_path: str | Path,
    *,
    source_size_ceiling_bytes: int | None = None,
    prefer_webp: bool = True,
    segmentation_mode: str = "changed_region",
    policy: ComponentUpdatePolicy | None = None,
    webp_quality: int | None = None,
    diagnostic_state_manifest_path: str | Path | None = None,
    use_diagnostic_components: bool = False,
) -> dict[str, Any]:
    source_manifest_path = Path(source_manifest_path)
    source_root = source_manifest_path.parent
    source_manifest = load_source_frame_manifest(source_manifest_path)
    output_archive_path = Path(output_archive_path)
    output_archive_path.parent.mkdir(parents=True, exist_ok=True)

    dependency_status = optional_dependency_status()
    use_webp = bool(prefer_webp and dependency_status["pillow_available"])
    width = int(source_manifest["width"])
    height = int(source_manifest["height"])
    frame_entries = sorted(source_manifest["frame_entries"], key=lambda entry: int(entry["frame_index"]))
    if not frame_entries:
        raise ValueError("source manifest has no frame entries")

    diagnostic_state: dict[str, Any] | None = None
    if diagnostic_state_manifest_path is not None:
        diagnostic_state = load_diagnostic_state_manifest(diagnostic_state_manifest_path)
        _validate_diagnostic_state_contract(
            diagnostic_state,
            source_manifest,
            width=width,
            height=height,
            frame_count=len(frame_entries),
        )
    if use_diagnostic_components and diagnostic_state is None:
        raise ValueError("use_diagnostic_components requires diagnostic_state_manifest_path")
    if use_diagnostic_components and not any(frame.get("tracks") for frame in diagnostic_state["frames"]):
        raise ValueError("diagnostic state has no track rows to drive component events")

    loaded_frames: list[tuple[int, Path, bytes]] = []
    frame_pixels_by_index: dict[int, bytes] = {}
    for entry in frame_entries:
        frame_path = source_root / str(entry["file"])
        frame_width, frame_height, pixels = read_ppm(frame_path)
        if frame_width != width or frame_height != height:
            raise ValueError(f"frame dimensions do not match manifest: {frame_path}")
        frame_index = int(entry["frame_index"])
        loaded_frames.append((frame_index, frame_path, pixels))
        frame_pixels_by_index[frame_index] = pixels

    base_index, base_path, base_pixels = loaded_frames[0]
    base_format, base_payload = _payload_bytes(
        width,
        height,
        base_pixels,
        use_webp=use_webp,
        webp_quality=webp_quality,
    )
    base_archive_path = f"base/base.{ 'webp' if use_webp else 'ppm' }"
    events: list[dict[str, Any]] = []
    source_hashes: list[dict[str, Any]] = []
    reconstructed = base_pixels
    last_update_frame: int | None = None
    total_pixels = width * height
    event_order = 0
    diagnostic_track_event_count = 0
    diagnostic_residual_event_count = 0
    diagnostic_mask_pixels = 0
    diagnostic_changed_pixels = 0
    diagnostic_logical_track_row_count = (
        sum(len(frame.get("tracks", [])) for frame in diagnostic_state["frames"])
        if diagnostic_state is not None
        else 0
    )

    if segmentation_mode not in {"changed_region", "opencv_changed_region"}:
        raise ValueError(f"unsupported segmentation mode: {segmentation_mode}")

    for frame_index, frame_path, frame_pixels in loaded_frames:
        source_hashes.append(
            {
                "frame_index": frame_index,
                "source_path": str(frame_path.name),
                "sha256": sha256_bytes(frame_pixels),
            }
        )
        if frame_index == base_index:
            last_update_frame = frame_index
            continue

        if use_diagnostic_components:
            # Track geometry drives candidate component events.  An exact
            # residual event is added for every changed pixel not covered by
            # those masks, so diagnostic quality can never silently damage
            # playback fidelity.
            working = reconstructed
            for track in sorted(
                diagnostic_tracks_for_frame(diagnostic_state, frame_index),
                key=lambda item: str(item.get("component_id", "")),
            ):
                if str(track.get("visible_state", "visible")).lower() in {"lost", "absent", "hidden"}:
                    continue
                geometry = rasterize_track_mask(track, width, height)
                if geometry is None:
                    continue
                bbox, mask_bytes, mask_pixels = geometry
                patch_pixels = _crop_pixels(frame_pixels, width, bbox)
                previous_patch = _crop_pixels(working, width, bbox)
                changed_inside_mask = sum(
                    1
                    for pixel_index, mask_value in enumerate(mask_bytes)
                    if mask_value
                    and patch_pixels[pixel_index * 3:pixel_index * 3 + 3]
                    != previous_patch[pixel_index * 3:pixel_index * 3 + 3]
                )
                if changed_inside_mask == 0:
                    continue
                patch_payload = _encode_masked_rgb(bbox[2], bbox[3], patch_pixels, mask_bytes)
                component_id = str(track.get("component_id", track.get("track_id", "diagnostic_component")))
                payload_path = f"events/frame_{frame_index:03d}_{event_order:05d}_{component_id}.amcfmask"
                event = {
                    "event_order": event_order,
                    "frame_index": frame_index,
                    "pts_seconds": frame_index / float(source_manifest["fps"]),
                    "component_id": component_id,
                    "track_id": str(track.get("track_id", component_id)),
                    "bbox": bbox,
                    "payload_path": payload_path,
                    "payload_format": "amcf_masked_rgb_v1",
                    "bytes": len(patch_payload),
                    "sha256": sha256_bytes(patch_payload),
                    "reason": str(track.get("update_reason", "diagnostic_component_state")),
                    "changed_pixels": changed_inside_mask,
                    "mask_pixels": mask_pixels,
                    "diagnostic_geometry": "polygon_contours",
                    "diagnostic_confidence": float(track.get("confidence", 0.0) or 0.0),
                }
                events.append(event)
                working = _paste_masked_patch(working, width, bbox, patch_pixels, mask_bytes)
                event_order += 1
                diagnostic_track_event_count += 1
                diagnostic_mask_pixels += mask_pixels
                diagnostic_changed_pixels += changed_inside_mask

            residual_bbox, residual_changed_pixels = _changed_bbox(working, frame_pixels, width, height)
            if residual_bbox is not None and residual_changed_pixels:
                patch_pixels = _crop_pixels(frame_pixels, width, residual_bbox)
                patch_format, patch_payload = _payload_bytes(
                    residual_bbox[2],
                    residual_bbox[3],
                    patch_pixels,
                    use_webp=use_webp,
                    webp_quality=webp_quality,
                )
                suffix = "webp" if patch_format.startswith("webp") else "ppm"
                payload_path = f"events/frame_{frame_index:03d}_{event_order:05d}_diagnostic_residual.{suffix}"
                events.append(
                    {
                        "event_order": event_order,
                        "frame_index": frame_index,
                        "pts_seconds": frame_index / float(source_manifest["fps"]),
                        "component_id": "diagnostic_residual",
                        "track_id": "diagnostic_residual",
                        "bbox": residual_bbox,
                        "payload_path": payload_path,
                        "payload_format": patch_format,
                        "bytes": len(patch_payload),
                        "sha256": sha256_bytes(patch_payload),
                        "reason": "uncovered_exact_residual",
                        "changed_pixels": residual_changed_pixels,
                        "changed_ratio": residual_changed_pixels / total_pixels,
                        "segmentation": {
                            "strategy": "diagnostic_track_masks_plus_exact_residual",
                            "covered_track_events": diagnostic_track_event_count,
                        },
                    }
                )
                working = _paste_patch(working, width, residual_bbox, patch_pixels)
                event_order += 1
                diagnostic_residual_event_count += 1
            if working != frame_pixels:
                raise AssertionError("diagnostic component event construction failed exact frame closure")
            reconstructed = working
            last_update_frame = frame_index
            continue

        if segmentation_mode == "opencv_changed_region":
            bbox, changed_pixels, segmentation_report = _opencv_changed_region(reconstructed, frame_pixels, width, height)
        else:
            bbox, changed_pixels = _changed_bbox(reconstructed, frame_pixels, width, height)
            segmentation_report = {"strategy": "changed_region", "changed_pixels": changed_pixels}
        decision = decide_component_update(
            frame_index=frame_index,
            last_update_frame=last_update_frame,
            changed_pixels=changed_pixels,
            total_pixels=total_pixels,
            policy=policy,
        )
        if bbox is None or not decision.should_update:
            continue
        patch_pixels = _crop_pixels(frame_pixels, width, bbox)
        patch_format, patch_payload = _payload_bytes(
            bbox[2],
            bbox[3],
            patch_pixels,
            use_webp=use_webp,
            webp_quality=webp_quality,
        )
        suffix = "webp" if patch_format == "webp_lossless" else "ppm"
        payload_path = f"events/frame_{frame_index:03d}_changed_region.{suffix}"
        event = {
            "event_order": event_order,
            "frame_index": frame_index,
            "pts_seconds": frame_index / float(source_manifest["fps"]),
            "component_id": "changed_region",
            "track_id": "changed_region",
            "bbox": bbox,
            "payload_path": payload_path,
            "payload_format": patch_format,
            "bytes": len(patch_payload),
            "sha256": sha256_bytes(patch_payload),
            "reason": decision.reason,
            "changed_pixels": changed_pixels,
            "changed_ratio": decision.changed_ratio,
            "segmentation": segmentation_report,
        }
        events.append(event)
        reconstructed = _paste_patch(reconstructed, width, bbox, patch_pixels)
        last_update_frame = frame_index
        event_order += 1

    ceiling_bytes = source_size_ceiling_bytes
    source_video = source_manifest.get("source_video") if isinstance(source_manifest.get("source_video"), dict) else {}
    if ceiling_bytes is None and source_video:
        ceiling_bytes = int(source_video.get("bytes") or 0) or None
    if ceiling_bytes is None:
        ceiling_bytes = sum((source_root / str(entry["file"])).stat().st_size for entry in frame_entries)

    component_ids = sorted({str(event["component_id"]) for event in events})
    if not component_ids:
        component_ids = ["changed_region"]
    components = [
        {
            "component_id": component_id,
            "component_type": "diagnostic_masked_component" if component_id != "diagnostic_residual" and use_diagnostic_components else "bounding_box_delta",
            "description": (
                "Track/contour-driven component event with an exact residual closure."
                if use_diagnostic_components and component_id != "diagnostic_residual"
                else "Exact changed-region component fallback for local Main component-event archive parity."
            ),
            "segmentation_mode": "diagnostic_track_masks_plus_exact_residual" if use_diagnostic_components else segmentation_mode,
        }
        for component_id in component_ids
    ]
    diagnostic_manifest_member = None
    diagnostic_block: dict[str, Any] = {
        "provided": diagnostic_state is not None,
        "used_for_component_event_selection": bool(use_diagnostic_components),
        "source_independent_decode": True,
        "generated_media_embedded": False,
        "state_member": None,
    }
    if diagnostic_state is not None:
        diagnostic_manifest_member = "diagnostics/diagnostic_state.json"
        diagnostic_block.update(
            {
                "state_member": diagnostic_manifest_member,
                "summary": diagnostic_state_summary(diagnostic_state),
                "profile": diagnostic_state.get("profile"),
            }
        )
    manifest = {
        "amcf_schema": AMCF_COMPONENT_EVENT_SCHEMA,
        "archive_payload_kind": "component_event_payloads",
        "source_type": source_manifest.get("source_type", "source_frames"),
        "frame_count": len(loaded_frames),
        "width": width,
        "height": height,
        "fps": int(source_manifest["fps"]),
        "created_by": "amcf_component_event_archive.py",
        "created_at": "2026-10-12T00:00:00Z",
        "base": {
            "frame_index": base_index,
            "payload_path": base_archive_path,
            "payload_format": base_format,
            "bytes": len(base_payload),
            "sha256": sha256_bytes(base_payload),
        },
        "components": components,
        "events": events,
        "source_frame_hashes": source_hashes,
        "diagnostic_state": diagnostic_block,
        "diagnostic_event_accounting": {
            "track_event_count": diagnostic_track_event_count,
            "exact_residual_event_count": diagnostic_residual_event_count,
            "logical_diagnostic_track_row_count": diagnostic_logical_track_row_count,
            "logical_track_rows_without_payload_event": max(
                0, diagnostic_logical_track_row_count - diagnostic_track_event_count
            ),
            "all_logical_track_rows_retained_in_embedded_state": bool(diagnostic_state is not None),
            "mask_pixels_written": diagnostic_mask_pixels,
            "changed_pixels_inside_track_masks": diagnostic_changed_pixels,
            "all_uncovered_pixels_closed_by_exact_residual": bool(use_diagnostic_components),
        },
        "dependency_status": {
            **dependency_status,
            "webp_payloads_requested": bool(prefer_webp),
            "webp_payloads_used": use_webp,
            "webp_quality": webp_quality,
            "webp_lossless": webp_quality is None,
            "standard_library_ppm_fallback_used": not use_webp,
            "opencv_segmentation_requested": segmentation_mode == "opencv_changed_region",
            "opencv_segmentation_used": segmentation_mode == "opencv_changed_region",
        },
        "archive_size_ceiling": {
            "ceiling_bytes": ceiling_bytes,
            "under_source_size_ceiling": None,
        },
        "capabilities": {
            "component_event_archive": True,
            "timestamped_updates": True,
            "bounding_box_changed_regions": True,
            "webp_payloads": use_webp,
            "ppm_fallback_payloads": not use_webp,
            "opencv_segmentation": segmentation_mode == "opencv_changed_region",
            "diagnostic_state": diagnostic_state is not None,
            "diagnostic_component_events": bool(use_diagnostic_components),
            "masked_component_payloads": bool(use_diagnostic_components and diagnostic_track_event_count),
            "psnr_metric": True,
            "ssim_metric": False,
            "viewer_package": False,
        },
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

    with zipfile.ZipFile(output_archive_path, "w") as zf:
        _write_zip_member(zf, "manifest.json", json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8"))
        if diagnostic_state is not None and diagnostic_manifest_member is not None:
            _write_zip_member(
                zf,
                diagnostic_manifest_member,
                json.dumps(diagnostic_state, indent=2, sort_keys=True).encode("utf-8"),
            )
        _write_zip_member(zf, base_archive_path, base_payload)
        for event in events:
            if event["payload_format"] == "amcf_masked_rgb_v1":
                track_rows = diagnostic_tracks_for_frame(diagnostic_state, int(event["frame_index"])) if diagnostic_state else []
                track = next(
                    (row for row in track_rows if str(row.get("component_id")) == str(event["component_id"])),
                    None,
                )
                if track is None:
                    raise ValueError(f"missing diagnostic track for event {event['component_id']}")
                geometry = rasterize_track_mask(track, width, height)
                if geometry is None:
                    raise ValueError(f"diagnostic track has no rasterizable geometry: {event['component_id']}")
                bbox, mask_bytes, _ = geometry
                if list(event["bbox"]) != list(bbox):
                    raise ValueError("diagnostic geometry changed between event planning and archive write")
                patch_pixels = _crop_pixels(frame_pixels_by_index[int(event["frame_index"])], width, bbox)
                event_payload = _encode_masked_rgb(bbox[2], bbox[3], patch_pixels, mask_bytes)
            else:
                x, y, event_width, event_height = event["bbox"]
                patch_pixels = _crop_pixels(frame_pixels_by_index[int(event["frame_index"])], width, [x, y, event_width, event_height])
                _, event_payload = _payload_bytes(
                    event_width,
                    event_height,
                    patch_pixels,
                    use_webp=use_webp,
                    webp_quality=webp_quality,
                )
            if sha256_bytes(event_payload) != event["sha256"]:
                raise AssertionError("event payload changed between planning and archive write")
            _write_zip_member(zf, event["payload_path"], event_payload)

    archive_bytes = output_archive_path.stat().st_size
    under_ceiling = archive_bytes <= int(ceiling_bytes)
    return {
        "ok": True,
        "archive_path": str(output_archive_path),
        "amcf_schema": AMCF_COMPONENT_EVENT_SCHEMA,
        "frame_count": len(loaded_frames),
        "event_count": len(events),
        "payload_format": (
            "mixed"
            if any(event["payload_format"] != (base_format if use_webp else "ppm_p6") for event in events)
            else base_format if use_webp else "ppm_p6"
        ),
        "segmentation_mode": segmentation_mode,
        "diagnostic_state": diagnostic_block,
        "diagnostic_event_accounting": manifest["diagnostic_event_accounting"],
        "dependency_status": manifest["dependency_status"],
        "archive_size_ceiling": {
            "ceiling_bytes": int(ceiling_bytes),
            "archive_bytes": archive_bytes,
            "under_source_size_ceiling": under_ceiling,
        },
        "archive_sha256": sha256_bytes(output_archive_path.read_bytes()),
        "claim_boundary": manifest["claim_boundary"],
        "unsafe_acceptance_count": 0,
    }


def decode_component_event_archive(archive_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    archive_path = Path(archive_path)
    output_dir = Path(output_dir)
    frames_dir = output_dir / "decoded_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("frame_*.ppm"):
        old.unlink()

    with zipfile.ZipFile(archive_path, "r") as zf:
        manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
        embedded_diagnostic_state: dict[str, Any] | None = None
        diagnostic_state_block = manifest.get("diagnostic_state", {})
        diagnostic_state_member = diagnostic_state_block.get("state_member")
        if diagnostic_state_member:
            if diagnostic_state_member not in zf.namelist():
                raise ValueError(f"diagnostic state member is missing: {diagnostic_state_member}")
            embedded_diagnostic_state = validate_diagnostic_state_manifest(
                json.loads(zf.read(diagnostic_state_member).decode("utf-8"))
            )
            expected_state_hash = diagnostic_state_block.get("summary", {}).get("state_sha256")
            if expected_state_hash and diagnostic_state_summary(embedded_diagnostic_state)["state_sha256"] != expected_state_hash:
                raise ValueError("embedded diagnostic state checksum does not match manifest summary")
        base = manifest["base"]
        base_width, base_height, current = _decode_payload(base["payload_format"], zf.read(base["payload_path"]))
        width = int(manifest["width"])
        height = int(manifest["height"])
        if base_width != width or base_height != height:
            raise ValueError("base payload dimensions do not match manifest")
        events_by_frame: dict[int, list[dict[str, Any]]] = {}
        for event in manifest.get("events", []):
            events_by_frame.setdefault(int(event["frame_index"]), []).append(event)
        decoded_entries: list[dict[str, Any]] = []
        for frame_index in range(int(manifest["frame_count"])):
            for event in sorted(
                events_by_frame.get(frame_index, []),
                key=lambda item: (int(item.get("event_order", 0)), str(item["component_id"])),
            ):
                payload = zf.read(event["payload_path"])
                if event.get("sha256") and sha256_bytes(payload) != event["sha256"]:
                    raise ValueError(f"event payload checksum mismatch: {event['payload_path']}")
                bbox = list(event["bbox"])
                if event.get("payload_format") == "amcf_masked_rgb_v1":
                    patch_width, patch_height, patch_pixels, mask = _decode_masked_rgb(payload)
                    if patch_width != bbox[2] or patch_height != bbox[3]:
                        raise ValueError("masked event payload dimensions do not match bbox")
                    current = _paste_masked_patch(current, width, bbox, patch_pixels, mask)
                else:
                    patch_width, patch_height, patch_pixels = _decode_payload(event["payload_format"], payload)
                    if patch_width != bbox[2] or patch_height != bbox[3]:
                        raise ValueError("event payload dimensions do not match bbox")
                    current = _paste_patch(current, width, bbox, patch_pixels)
            frame_path = frames_dir / f"frame_{frame_index:03d}.ppm"
            write_ppm(frame_path, width, height, current)
            decoded_entries.append({"frame_index": frame_index, "file": frame_path.name, "sha256": sha256_bytes(current)})

    summary = {
        "ok": True,
        "archive_path": str(archive_path),
        "decoded_frames_dir": str(frames_dir),
        "frame_count": len(decoded_entries),
        "event_count": len(manifest.get("events", [])),
        "fps": int(manifest.get("fps", 24) or 24),
        "unsafe_acceptance_count": int(manifest.get("unsafe_acceptance_count", 0)),
        "claim_boundary": manifest.get("claim_boundary", {}),
        "frames": decoded_entries,
        "diagnostic_state": {
            **manifest.get("diagnostic_state", {"provided": False}),
            "embedded_state_validated": embedded_diagnostic_state is not None,
            "embedded_state_summary": (
                diagnostic_state_summary(embedded_diagnostic_state)
                if embedded_diagnostic_state is not None
                else {}
            ),
        },
        "diagnostic_event_accounting": manifest.get("diagnostic_event_accounting", {}),
    }
    (output_dir / "decoded_component_event_manifest.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary
