"""Camera-compensated local-motion diagnostics adapted from local Test 03M."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Zone:
    name: str
    expected_motion_type: str
    bbox: tuple[int, int, int, int]
    notes: str = ""


def _image_modules():
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("motion diagnostics require optional OpenCV and NumPy") from exc
    return cv2, np


def estimate_pair_transform(previous: Any, current: Any) -> tuple[Any, dict[str, Any]]:
    """Use sparse LK/RANSAC, then Farneback median translation as in 03M."""
    cv2, np = _image_modules()
    if previous.shape != current.shape or previous.ndim != 3 or previous.shape[2] != 3:
        raise ValueError("frames must have matching BGR dimensions")
    prev_gray = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
    points = cv2.goodFeaturesToTrack(prev_gray, maxCorners=320, qualityLevel=0.01, minDistance=7)
    matrix = np.array([[1, 0, 0], [0, 1, 0]], dtype=np.float32)
    info = {"method_used": "identity_fallback", "feature_count": 0,
            "inlier_count": 0, "inlier_ratio": 0.0, "quality": "poor"}
    if points is None:
        return matrix, info
    next_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, points, None)
    if next_points is None or status is None:
        return matrix, info
    good_previous = points[status.ravel() == 1].reshape(-1, 2)
    good_current = next_points[status.ravel() == 1].reshape(-1, 2)
    info["feature_count"] = int(len(good_previous))
    if len(good_previous) >= 10:
        estimate, inliers_mask = cv2.estimateAffinePartial2D(
            good_previous, good_current, method=cv2.RANSAC, ransacReprojThreshold=3
        )
        if estimate is not None:
            matrix = estimate.astype(np.float32)
            inliers = int(inliers_mask.sum()) if inliers_mask is not None else len(good_previous)
            ratio = inliers / len(good_previous)
            info.update(method_used="sparse_lk_affine_ransac", inlier_count=inliers,
                        inlier_ratio=ratio, quality="good" if ratio >= 0.55 else "weak")
            return matrix, info
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    matrix[0, 2] = float(np.median(flow[..., 0]))
    matrix[1, 2] = float(np.median(flow[..., 1]))
    info.update(method_used="farneback_median_translation_fallback", quality="fallback")
    return matrix, info


def residual_motion(previous: Any, current: Any, matrix: Any) -> tuple[Any, Any]:
    """Return the compensated difference and cleaned binary motion mask."""
    cv2, np = _image_modules()
    height, width = current.shape[:2]
    warped = cv2.warpAffine(previous, matrix, (width, height),
                            flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    difference = cv2.absdiff(current, warped)
    gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    return gray, mask


def classify_zone(expected: str, active_fraction: float, p95: float) -> str:
    if expected == "intermittent_small_object_motion" and active_fraction > 0.01:
        return "intermittent_small_object_motion"
    if active_fraction > 0.18 or p95 > 55:
        return "high_local_motion"
    if active_fraction > 0.08 or p95 > 35:
        return "moderate_local_motion"
    if active_fraction > 0.025 or p95 > 20:
        return "slight_local_motion"
    return "camera_motion_only_or_static"


def score_zones(gray: Any, mask: Any, zones: list[Zone], frame_index: int) -> list[dict[str, Any]]:
    _, np = _image_modules()
    height, width = gray.shape
    if mask.shape != gray.shape:
        raise ValueError("mask and difference dimensions differ")
    rows = []
    for zone in zones:
        x, y, w, h = zone.bbox
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
            raise ValueError(f"zone outside frame: {zone.name}")
        region = gray[y:y + h, x:x + w]
        region_mask = mask[y:y + h, x:x + w]
        active_count = int(np.count_nonzero(region_mask))
        fraction = active_count / (w * h)
        p95 = float(np.percentile(region, 95))
        rows.append({"frame_index": frame_index, "zone_name": zone.name,
                     "active_motion_pixel_count": active_count,
                     "active_motion_fraction": fraction,
                     "mean_residual_absdiff": float(np.mean(region)),
                     "p95_residual_absdiff": p95,
                     "expected_motion_type": zone.expected_motion_type,
                     "observed_motion_class": classify_zone(zone.expected_motion_type, fraction, p95),
                     "notes": zone.notes})
    return rows


def draw_zone_overlay(frame: Any, mask: Any, zones: list[Zone]) -> Any:
    cv2, np = _image_modules()
    if frame.shape[:2] != mask.shape:
        raise ValueError("frame and mask dimensions differ")
    highlight = np.zeros_like(frame)
    highlight[..., 1] = mask
    output = cv2.addWeighted(frame, 0.82, highlight, 0.18, 0)
    for zone in zones:
        x, y, w, h = zone.bbox
        color = ((180, 180, 180) if "static" in zone.expected_motion_type else (0, 255, 255))
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 1)
        cv2.putText(output, zone.name.replace("_zone", ""),
                    (x + 2, max(12, y + 12)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.32, color, 1, cv2.LINE_AA)
    return output


def analyze_pair(previous: Any, current: Any, zones: list[Zone], frame_index: int = 2) -> tuple[dict[str, Any], Any]:
    cv2, _ = _image_modules()
    matrix, transform = estimate_pair_transform(previous, current)
    gray, mask = residual_motion(previous, current, matrix)
    rows = score_zones(gray, mask, zones, frame_index)
    overlay = draw_zone_overlay(current, mask, zones)
    result = {"frame_index": frame_index, "transform": transform,
              "translation_dx": float(matrix[0, 2]), "translation_dy": float(matrix[1, 2]),
              "zones": rows, "motion_mask_pixels": int(cv2.countNonZero(mask)),
              "human_review_required": True, "final_tracking_proof_claimed": False,
              "unsafe_acceptance_count": 0, "hardware_validation_claimed": False,
              "physical_level_5_claimed": False, "manufactured_player_claimed": False}
    return result, overlay
