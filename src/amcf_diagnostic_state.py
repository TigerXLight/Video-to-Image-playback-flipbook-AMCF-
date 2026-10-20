"""Normalized diagnostic state for the AMCF component-event encoder.

The historical AMCF diagnostics are not one interchangeable mask format.  Test
02 carries per-frame track geometry and contours, 03M carries camera-aware
motion zones, 08E carries a derived motion heat contract, and 12E carries a
reviewed proxy taxonomy.  This module gives those process outputs one explicit
boundary so the encoder can consume the geometry-bearing part without silently
turning a heatmap or proxy box into a segmentation mask.

Only normalized state is suitable for archive integration.  Generated videos,
absolute local paths, and source MP4 bytes are deliberately excluded.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


AMCF_DIAGNOSTIC_STATE_SCHEMA = "amcf-diagnostic-state-v1"


def _read_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"diagnostic manifest must contain an object: {path}")
    return value


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return int(default)


def _point(point: Any) -> list[int] | None:
    if isinstance(point, str):
        parts = point.replace(",", " ").split()
        if len(parts) < 2:
            return None
        return [_int(parts[0]), _int(parts[1])]
    if isinstance(point, (list, tuple)) and len(point) >= 2:
        return [_int(point[0]), _int(point[1])]
    return None


def _contours(value: Any) -> list[list[list[int]]]:
    if not isinstance(value, list):
        return []
    output: list[list[list[int]]] = []
    for contour in value:
        if not isinstance(contour, list):
            continue
        points = [point for raw in contour if (point := _point(raw)) is not None]
        if len(points) >= 3:
            output.append(points)
    return output


def _bbox(value: Any) -> list[int] | None:
    if not isinstance(value, (list, tuple)) or len(value) < 4:
        return None
    result = [_int(item) for item in value[:4]]
    if result[2] <= 0 or result[3] <= 0:
        return None
    return result


def _normalize_track(track: dict[str, Any], source_width: int, source_height: int) -> dict[str, Any]:
    track_id = str(track.get("track_id", track.get("component_id", "unknown")))
    contours = _contours(track.get("contours"))
    bbox = _bbox(track.get("bbox"))
    return {
        "component_id": track_id,
        "track_id": track_id,
        "parent_id": track.get("parent_id"),
        "label": str(track.get("label", track_id)),
        "visible_state": str(track.get("visible_state", "visible")),
        "occluded_state": str(track.get("occluded_state", "none")),
        "confidence": _number(track.get("confidence"), 0.0),
        "centroid": list(track.get("centroid", [])) if isinstance(track.get("centroid"), list) else [],
        "area": _number(track.get("area"), 0.0),
        "bbox": bbox,
        "contours": contours,
        "motion": {
            "median_px_s": _number(track.get("motion_median_px_s")),
            "p95_px_s": _number(track.get("motion_p95_px_s")),
            "direction_deg": _number(track.get("motion_direction_deg")),
            "flow_sample_count": _int(track.get("flow_sample_count")),
            "global_compensation_px_s": list(track.get("global_compensation_px_s", []))
            if isinstance(track.get("global_compensation_px_s"), list)
            else [],
        },
        "component_update": bool(track.get("component_update", False)),
        "update_reason": str(track.get("update_reason", "unknown")),
        "archive_event": track.get("archive_event") if isinstance(track.get("archive_event"), dict) else None,
        "geometry_contract": {
            "kind": "polygon_contours" if contours else "bbox_only",
            "source_width": int(source_width),
            "source_height": int(source_height),
        },
    }


def normalize_test02_tracks_manifest(
    path: str | Path,
    *,
    source_video_sha256: str | None = None,
    source_video_name: str | None = None,
) -> dict[str, Any]:
    """Convert the historical Test 02 per-frame track manifest to AMCF state."""
    raw = _read_json(path)
    if raw.get("schema") != "amcf-test02-tracks-v1":
        raise ValueError(f"unsupported track manifest schema: {raw.get('schema')!r}")
    source_size = raw.get("source_size")
    if not isinstance(source_size, list) or len(source_size) < 2:
        raise ValueError("Test 02 manifest is missing source_size")
    source_width, source_height = _int(source_size[0]), _int(source_size[1])
    if source_width <= 0 or source_height <= 0:
        raise ValueError("Test 02 source_size must be positive")
    raw_frames = raw.get("frames")
    if not isinstance(raw_frames, list) or not raw_frames:
        raise ValueError("Test 02 manifest is missing frames")

    frames: list[dict[str, Any]] = []
    for raw_frame in sorted(raw_frames, key=lambda item: _int(item.get("frame_index"))):
        if not isinstance(raw_frame, dict):
            raise ValueError("diagnostic frame must be an object")
        frame_index = _int(raw_frame.get("frame_index"))
        tracks = raw_frame.get("tracks")
        if not isinstance(tracks, list):
            raise ValueError(f"frame {frame_index} is missing tracks")
        frames.append(
            {
                "frame_index": frame_index,
                "pts_seconds": _number(raw_frame.get("pts_seconds"), frame_index / max(_number(raw.get("fps"), 24.0), 1.0)),
                "tracks": [
                    _normalize_track(track, source_width, source_height)
                    for track in tracks
                    if isinstance(track, dict)
                ],
            }
        )

    taxonomy: dict[str, dict[str, Any]] = {}
    for frame in frames:
        for track in frame["tracks"]:
            row = taxonomy.setdefault(
                track["component_id"],
                {
                    "component_id": track["component_id"],
                    "track_id": track["track_id"],
                    "parent_id": track["parent_id"],
                    "label": track["label"],
                    "frame_count": 0,
                    "component_update_count": 0,
                    "contour_frame_count": 0,
                },
            )
            row["frame_count"] += 1
            row["component_update_count"] += int(track["component_update"])
            row["contour_frame_count"] += int(bool(track["contours"]))

    manifest = {
        "schema": AMCF_DIAGNOSTIC_STATE_SCHEMA,
        "profile": "test02_track_mask_state",
        "source": {
            "name": source_video_name or "",
            "sha256": source_video_sha256 or "",
            "width": source_width,
            "height": source_height,
            "fps": _number(raw.get("fps"), 24.0),
            "frame_count": len(frames),
        },
        "frames": frames,
        "taxonomy": [taxonomy[key] for key in sorted(taxonomy)],
        "process_contracts": {
            "test02_track_masks_contours_flow": {
                "present": True,
                "used_as_component_geometry": True,
                "source_schema": raw.get("schema"),
            },
            "03m_camera_compensated_zone_motion": {
                "present": False,
                "diagnostic_only_when_loaded": True,
            },
            "08e_motion_heat": {
                "present": False,
                "diagnostic_only_when_loaded": True,
            },
            "10a_10b_crop_review": {
                "present": False,
                "diagnostic_only_when_loaded": True,
                "roi_motion_audit_available": True,
            },
            "12b_classical_proxy": {
                "present": False,
                "diagnostic_only_when_loaded": True,
                "proxy_boxes_are_not_masks": True,
                "object_identity_verified": False,
            },
            "12d_calibrated_proxy": {
                "present": False,
                "diagnostic_only_when_loaded": True,
                "proxy_boxes_are_not_masks": True,
            },
            "12e_reviewed_proxy": {
                "present": False,
                "proxy_boxes_are_not_masks": True,
            },
            "hoot_semantic_level5": {
                "present": False,
                "bounded_dataset_claim_only": True,
            },
        },
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "semantic_object_amcf_solved": False,
        },
        "unsafe_acceptance_count": 0,
    }
    return validate_diagnostic_state_manifest(manifest)


def validate_diagnostic_state_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Validate normalized state and return it without weakening its claims."""
    if manifest.get("schema") != AMCF_DIAGNOSTIC_STATE_SCHEMA:
        raise ValueError("unsupported normalized diagnostic state schema")
    source = manifest.get("source")
    frames = manifest.get("frames")
    if not isinstance(source, dict) or not isinstance(frames, list) or not frames:
        raise ValueError("diagnostic state requires source and non-empty frames")
    for key in ("width", "height", "fps", "frame_count"):
        if key not in source:
            raise ValueError(f"diagnostic state source missing {key}")
    if _int(source["width"]) <= 0 or _int(source["height"]) <= 0 or _number(source["fps"]) <= 0:
        raise ValueError("diagnostic state source dimensions/fps must be positive")
    if _int(source["frame_count"]) != len(frames):
        raise ValueError("diagnostic state frame_count does not match frames")
    indexes = []
    for frame in frames:
        if not isinstance(frame, dict) or not isinstance(frame.get("tracks"), list):
            raise ValueError("diagnostic state frame must contain a tracks list")
        indexes.append(_int(frame.get("frame_index")))
        for track in frame["tracks"]:
            if not isinstance(track, dict) or not track.get("component_id"):
                raise ValueError("diagnostic state track is missing component_id")
    if indexes != sorted(set(indexes)):
        raise ValueError("diagnostic state frame indexes must be unique and sorted")
    return manifest


def enrich_diagnostic_state_manifest(
    manifest: dict[str, Any],
    *,
    process_profiles: dict[str, Any] | None = None,
    process_contracts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Attach non-pixel diagnostic contracts without changing track geometry."""
    enriched = json.loads(json.dumps(validate_diagnostic_state_manifest(manifest)))
    if process_profiles is not None:
        enriched["process_profiles"] = process_profiles
    if process_contracts is not None:
        current = dict(enriched.get("process_contracts", {}))
        current.update(process_contracts)
        enriched["process_contracts"] = current
    return validate_diagnostic_state_manifest(enriched)


def write_diagnostic_state_manifest(
    manifest: dict[str, Any],
    output_path: str | Path,
) -> dict[str, Any]:
    """Write a normalized, path-free state bundle for reproducible encoding."""
    manifest = validate_diagnostic_state_manifest(manifest)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "path": str(output_path),
        "schema": manifest["schema"],
        "profile": manifest.get("profile"),
        "state_sha256": diagnostic_state_sha256(manifest),
        "frame_count": len(manifest["frames"]),
        "unsafe_acceptance_count": int(manifest.get("unsafe_acceptance_count", 0)),
    }


def load_diagnostic_state_manifest(path: str | Path) -> dict[str, Any]:
    """Load normalized state or safely normalize the historical Test 02 schema."""
    path = Path(path)
    raw = _read_json(path)
    if raw.get("schema") == AMCF_DIAGNOSTIC_STATE_SCHEMA:
        return validate_diagnostic_state_manifest(raw)
    if raw.get("schema") == "amcf-test02-tracks-v1":
        return normalize_test02_tracks_manifest(path)
    raise ValueError(f"unsupported diagnostic state schema: {raw.get('schema')!r}")


def diagnostic_state_sha256(manifest: dict[str, Any]) -> str:
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def diagnostic_tracks_for_frame(manifest: dict[str, Any], frame_index: int) -> list[dict[str, Any]]:
    for frame in manifest["frames"]:
        if int(frame["frame_index"]) == int(frame_index):
            return list(frame.get("tracks", []))
    return []


def scaled_bbox(track: dict[str, Any], target_width: int, target_height: int) -> list[int] | None:
    bbox = _bbox(track.get("bbox"))
    source = track.get("geometry_contract", {})
    source_width = _int(source.get("source_width"), target_width)
    source_height = _int(source.get("source_height"), target_height)
    if bbox is None or source_width <= 0 or source_height <= 0:
        return None
    sx = target_width / source_width
    sy = target_height / source_height
    x, y, width, height = bbox
    x0 = max(0, min(target_width, int(round(x * sx))))
    y0 = max(0, min(target_height, int(round(y * sy))))
    x1 = max(x0, min(target_width, int(round((x + width) * sx))))
    y1 = max(y0, min(target_height, int(round((y + height) * sy))))
    if x1 <= x0 or y1 <= y0:
        return None
    return [x0, y0, x1 - x0, y1 - y0]


def rasterize_track_mask(
    track: dict[str, Any],
    target_width: int,
    target_height: int,
) -> tuple[list[int], bytes, int] | None:
    """Rasterize contour geometry into a bbox-local binary mask.

    This function intentionally rejects bbox-only proxy geometry.  A proxy is
    useful for review and display, but treating it as a component mask would
    silently change the AMCF event contract.
    """
    bbox = scaled_bbox(track, target_width, target_height)
    contours = track.get("contours")
    if bbox is None or not isinstance(contours, list) or not contours:
        return None
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("diagnostic component integration requires OpenCV and NumPy") from exc
    source = track.get("geometry_contract", {})
    source_width = _int(source.get("source_width"), target_width)
    source_height = _int(source.get("source_height"), target_height)
    sx = target_width / source_width
    sy = target_height / source_height
    x0, y0, width, height = bbox
    polygons = []
    for contour in contours:
        points = []
        for raw_point in contour:
            point = _point(raw_point)
            if point is None:
                continue
            points.append([int(round(point[0] * sx)) - x0, int(round(point[1] * sy)) - y0])
        if len(points) >= 3:
            polygons.append(np.asarray(points, dtype=np.int32).reshape((-1, 1, 2)))
    if not polygons:
        return None
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, polygons, 255)
    return bbox, bytes(mask.reshape(-1)), int(np.count_nonzero(mask))


def diagnostic_state_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    tracks = sum(len(frame.get("tracks", [])) for frame in manifest["frames"])
    contour_tracks = sum(
        1
        for frame in manifest["frames"]
        for track in frame.get("tracks", [])
        if track.get("contours")
    )
    return {
        "schema": manifest["schema"],
        "profile": manifest.get("profile"),
        "source": manifest["source"],
        "frame_count": len(manifest["frames"]),
        "track_frame_rows": tracks,
        "contour_track_frame_rows": contour_tracks,
        "taxonomy_count": len(manifest.get("taxonomy", [])),
        "state_sha256": diagnostic_state_sha256(manifest),
        "process_contracts": manifest.get("process_contracts", {}),
        "process_profiles": manifest.get("process_profiles", {}),
        "unsafe_acceptance_count": int(manifest.get("unsafe_acceptance_count", 0)),
    }
