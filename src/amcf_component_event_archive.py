from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import zipfile
from pathlib import Path
from typing import Any

from amcf_adaptive_component_scheduler import ComponentUpdatePolicy, decide_component_update
from amcf_quality_metrics import ppm_bytes, read_ppm, sha256_bytes, write_ppm


AMCF_COMPONENT_EVENT_SCHEMA = "amcf-component-event-archive-v1"
FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


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


def _encode_webp(width: int, height: int, pixels: bytes) -> bytes:
    from PIL import Image

    image = Image.frombytes("RGB", (width, height), pixels)
    buffer = io.BytesIO()
    image.save(buffer, format="WEBP", lossless=True)
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


def _payload_bytes(width: int, height: int, pixels: bytes, *, use_webp: bool) -> tuple[str, bytes]:
    if use_webp:
        return "webp_lossless", _encode_webp(width, height, pixels)
    return "ppm_p6", ppm_bytes(width, height, pixels)


def _decode_payload(format_name: str, payload: bytes) -> tuple[int, int, bytes]:
    if format_name == "webp_lossless":
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
    base_format, base_payload = _payload_bytes(width, height, base_pixels, use_webp=use_webp)
    base_archive_path = f"base/base.{ 'webp' if use_webp else 'ppm' }"
    events: list[dict[str, Any]] = []
    source_hashes: list[dict[str, Any]] = []
    reconstructed = base_pixels
    last_update_frame: int | None = None
    total_pixels = width * height

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
        patch_format, patch_payload = _payload_bytes(bbox[2], bbox[3], patch_pixels, use_webp=use_webp)
        suffix = "webp" if patch_format == "webp_lossless" else "ppm"
        payload_path = f"events/frame_{frame_index:03d}_changed_region.{suffix}"
        event = {
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

    ceiling_bytes = source_size_ceiling_bytes
    source_video = source_manifest.get("source_video") if isinstance(source_manifest.get("source_video"), dict) else {}
    if ceiling_bytes is None and source_video:
        ceiling_bytes = int(source_video.get("bytes") or 0) or None
    if ceiling_bytes is None:
        ceiling_bytes = sum((source_root / str(entry["file"])).stat().st_size for entry in frame_entries)

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
        "components": [
            {
                "component_id": "changed_region",
                "component_type": "bounding_box_delta",
                "description": "Standard-library changed-region component fallback for local Main component-event archive parity.",
                "segmentation_mode": segmentation_mode,
            }
        ],
        "events": events,
        "source_frame_hashes": source_hashes,
        "dependency_status": {
            **dependency_status,
            "webp_payloads_requested": bool(prefer_webp),
            "webp_payloads_used": use_webp,
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
        _write_zip_member(zf, base_archive_path, base_payload)
        for event in events:
            x, y, event_width, event_height = event["bbox"]
            patch_pixels = _crop_pixels(frame_pixels_by_index[int(event["frame_index"])], width, [x, y, event_width, event_height])
            _, event_payload = _payload_bytes(event_width, event_height, patch_pixels, use_webp=use_webp)
            _write_zip_member(zf, event["payload_path"], event_payload)

    archive_bytes = output_archive_path.stat().st_size
    under_ceiling = archive_bytes <= int(ceiling_bytes)
    return {
        "ok": True,
        "archive_path": str(output_archive_path),
        "amcf_schema": AMCF_COMPONENT_EVENT_SCHEMA,
        "frame_count": len(loaded_frames),
        "event_count": len(events),
        "payload_format": "webp_lossless" if use_webp else "ppm_p6",
        "segmentation_mode": segmentation_mode,
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
            for event in sorted(events_by_frame.get(frame_index, []), key=lambda item: str(item["component_id"])):
                patch_width, patch_height, patch_pixels = _decode_payload(event["payload_format"], zf.read(event["payload_path"]))
                bbox = list(event["bbox"])
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
    }
    (output_dir / "decoded_component_event_manifest.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary
