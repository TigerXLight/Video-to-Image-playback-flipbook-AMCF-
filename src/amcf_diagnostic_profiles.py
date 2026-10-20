"""Profile-aware AMCF diagnostic renderers.

These are reusable process diagnostics, not accepted semantic/object claims.
The profiles preserve the local contracts selected by the progression:

* 03M: camera-compensated green zone-motion residuals.
* 08E: Farneback motion heat comparison for a truth/decoded pair.
* 12E: conservative reviewed proxy boxes, including narrow event review.

Generated videos remain caller-owned output and are never bundled as source
code or treated as canonical AMCF payloads.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from amcf_motion_truth_diagnostics import (
    Zone,
    draw_zone_overlay,
    estimate_pair_transform,
    residual_motion,
    score_zones,
)
from amcf_diagnostic_state import (
    diagnostic_tracks_for_frame,
    load_diagnostic_state_manifest,
    rasterize_track_mask,
)


def waterfall_03m_zones(width: int = 640, height: int = 320) -> list[Zone]:
    """Return the accepted Test 03M zone map, scaled from 640x320 if needed."""
    if width <= 0 or height <= 0:
        raise ValueError("diagnostic frame dimensions must be positive")
    sx = width / 640.0
    sy = height / 320.0
    base = [
        ("waterfall_main_zone", "high_local_motion", (250, 20, 115, 230), "Main waterfall column."),
        ("waterfall_left_zone", "high_or_moderate_local_motion", (175, 40, 100, 230), "Left waterfall motion."),
        ("tree_leaf_zone", "moderate_local_motion", (0, 0, 175, 190), "Tree leaves should move locally."),
        ("left_branch_zone", "slight_local_motion", (85, 20, 150, 130), "Branches left of waterfall move slightly."),
        (
            "white_people_left_of_waterfall_zone",
            "intermittent_small_object_motion",
            (145, 110, 125, 135),
            "White figures/people walking left of waterfall.",
        ),
        (
            "tree_trunk_or_static_tree_body_zone",
            "camera_motion_only_or_static",
            (0, 115, 160, 205),
            "Tree body should mostly be camera-registered static layer.",
        ),
        (
            "background_rock_or_static_scene_zone",
            "camera_motion_only_or_static",
            (425, 35, 165, 180),
            "Static reference/background zone.",
        ),
    ]
    zones: list[Zone] = []
    for name, expected, (x, y, zone_width, zone_height), notes in base:
        scaled_x = round(x * sx)
        scaled_y = round(y * sy)
        scaled_width = round(zone_width * sx)
        scaled_height = round(zone_height * sy)
        if scaled_x + scaled_width > width:
            scaled_width = width - scaled_x
        if scaled_y + scaled_height > height:
            scaled_height = height - scaled_y
        zones.append(Zone(name, expected, (scaled_x, scaled_y, scaled_width, scaled_height), notes))
    return zones


def flow_magnitude_heatmap(previous: Any, current: Any) -> Any:
    """Render the exact 08E Farneback/TURBO per-frame motion heat contract."""
    import cv2

    previous_gray = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(
        previous_gray,
        current_gray,
        None,
        0.5,
        3,
        15,
        3,
        5,
        1.2,
        0,
    )
    magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")
    return cv2.applyColorMap(normalized, cv2.COLORMAP_TURBO)


def diff_panel(previous: Any, current: Any, scale: int = 8) -> Any:
    """Return the historical 08E difference panel with bounded x-scale."""
    import cv2
    import numpy as np

    difference = cv2.absdiff(previous, current)
    return np.clip(difference.astype("int16") * int(scale), 0, 255).astype("uint8")


def default_roi_profile(profile: str, width: int, height: int) -> dict[str, tuple[int, int, int, int]]:
    """Return the historical 10A/10B crop-review regions for a frame size."""
    if width <= 0 or height <= 0:
        raise ValueError("diagnostic frame dimensions must be positive")
    normalized = str(profile).strip().lower().replace("_", "-")
    if normalized in {"third", "third-water", "10a", "10a-water"}:
        return {
            "center_water": (width // 4, height // 4, width // 2, height // 2),
            "left_detail": (0, 0, width // 3, height),
            "right_detail": (width * 2 // 3, 0, width - width * 2 // 3, height),
            "bottom_texture": (0, height * 2 // 3, width, height - height * 2 // 3),
            "whole_frame": (0, 0, width, height),
        }
    if normalized in {"fourth", "fourth-people", "10b", "10b-people"}:
        return {
            "center_people_or_motion": (width // 4, height // 4, width // 2, height // 2),
            "left_detail": (0, 0, width // 3, height),
            "right_detail": (width * 2 // 3, 0, width - width * 2 // 3, height),
            "static_reference": (width // 3, 0, width // 3, height // 3),
            "whole_frame": (0, 0, width, height),
        }
    raise ValueError(f"unknown 10A/10B ROI profile: {profile!r}")


def roi_motion_audit(
    truth_frames: Iterable[Any],
    selected_frames: Iterable[Any],
    rois: dict[str, tuple[int, int, int, int]],
    *,
    warning_low: float = 0.85,
    warning_high: float = 1.15,
) -> dict[str, Any]:
    """Match the 10A/10B ROI motion contract without changing source frames."""
    import cv2
    import numpy as np

    truth = list(truth_frames)
    selected = list(selected_frames)
    frame_count = min(len(truth), len(selected))
    summary: dict[str, dict[str, Any]] = {}
    for name, (x, y, width, height) in rois.items():
        truth_values: list[float] = []
        selected_values: list[float] = []
        for index in range(max(0, frame_count - 1)):
            truth_a = cv2.cvtColor(truth[index][y : y + height, x : x + width], cv2.COLOR_BGR2GRAY)
            truth_b = cv2.cvtColor(truth[index + 1][y : y + height, x : x + width], cv2.COLOR_BGR2GRAY)
            selected_a = cv2.cvtColor(selected[index][y : y + height, x : x + width], cv2.COLOR_BGR2GRAY)
            selected_b = cv2.cvtColor(selected[index + 1][y : y + height, x : x + width], cv2.COLOR_BGR2GRAY)
            truth_values.append(float(cv2.absdiff(truth_a, truth_b).mean()))
            selected_values.append(float(cv2.absdiff(selected_a, selected_b).mean()))
        truth_motion = float(np.mean(truth_values)) if truth_values else 0.0
        selected_motion = float(np.mean(selected_values)) if selected_values else 0.0
        ratio = selected_motion / truth_motion if truth_motion else None
        summary[name] = {
            "truth_motion": truth_motion,
            "selected_motion": selected_motion,
            "selected_truth_ratio": ratio,
            "frame_pairs": len(truth_values),
        }
    warnings = [
        f"{name} ratio {row['selected_truth_ratio']}"
        for name, row in summary.items()
        if row["selected_truth_ratio"] is not None
        and not (warning_low <= row["selected_truth_ratio"] <= warning_high)
    ]
    status = "PASS" if not warnings else ("NEEDS_HUMAN_REVIEW" if len(warnings) <= 2 else "REJECTED")
    return {
        "status": status,
        "frame_count": frame_count,
        "roi_motion": summary,
        "warnings": warnings,
        "unsafe_acceptance_count": 0,
    }


def _fit_diagnostic_panel(frame: Any, width: int = 240, height: int = 135) -> Any:
    """Letterbox a crop for the 10A/10B review grid without stretching it."""
    import cv2
    import numpy as np

    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    if frame is None or frame.size == 0:
        return canvas
    source_height, source_width = frame.shape[:2]
    scale = min(width / max(source_width, 1), height / max(source_height, 1))
    resized = cv2.resize(frame, (max(1, int(round(source_width * scale))), max(1, int(round(source_height * scale)))))
    y = (height - resized.shape[0]) // 2
    x = (width - resized.shape[1]) // 2
    canvas[y : y + resized.shape[0], x : x + resized.shape[1]] = resized
    return canvas


def render_roi_comparison_video(
    truth_video: Path,
    selected_video: Path,
    output_video: Path,
    *,
    roi_profile: str = "fourth-people",
    fullrate_video: Path | None = None,
    diff_scale: int = 8,
    max_frames: int | None = None,
) -> dict[str, Any]:
    """Render the 10A/10B truth/fullrate/selected/diff crop-review contract."""
    import cv2
    import numpy as np

    captures = [cv2.VideoCapture(str(truth_video)), cv2.VideoCapture(str(selected_video))]
    if fullrate_video is not None:
        captures.append(cv2.VideoCapture(str(fullrate_video)))
    if not all(capture.isOpened() for capture in captures):
        for capture in captures:
            capture.release()
        raise RuntimeError("could not open all ROI comparison inputs")
    fps = float(captures[0].get(cv2.CAP_PROP_FPS) or 30.0)
    writer = None
    frame_count = 0
    truth_frames: list[Any] = []
    selected_frames: list[Any] = []
    rois: dict[str, tuple[int, int, int, int]] | None = None
    try:
        while max_frames is None or frame_count < max_frames:
            reads = [capture.read() for capture in captures]
            if not all(ok and frame is not None for ok, frame in reads):
                break
            truth = reads[0][1]
            selected = reads[1][1]
            fullrate = reads[2][1] if fullrate_video is not None else None
            if truth.shape != selected.shape or (fullrate is not None and fullrate.shape != truth.shape):
                raise ValueError("ROI comparison inputs have different frame shapes")
            if rois is None:
                rois = default_roi_profile(roi_profile, truth.shape[1], truth.shape[0])
                panel_count = 4 if fullrate_video is not None else 3
                writer = _open_writer(output_video, fps, 240 * panel_count, 135 * len(rois))
            rows = []
            for name, (x, y, width, height) in rois.items():
                truth_crop = truth[y : y + height, x : x + width]
                selected_crop = selected[y : y + height, x : x + width]
                panels = [_label_08e(_fit_diagnostic_panel(truth_crop), "truth")]
                if fullrate is not None:
                    panels.append(_label_08e(_fit_diagnostic_panel(fullrate[y : y + height, x : x + width]), "fullrate"))
                panels.extend(
                    [
                        _label_08e(_fit_diagnostic_panel(selected_crop), "selected"),
                        _label_08e(_fit_diagnostic_panel(diff_panel(truth_crop, selected_crop, diff_scale)), f"diff x{diff_scale}"),
                    ]
                )
                rows.append(np.hstack(panels))
            writer.write(np.vstack(rows))
            truth_frames.append(truth)
            selected_frames.append(selected)
            frame_count += 1
    finally:
        for capture in captures:
            capture.release()
        if writer is not None:
            writer.release()
    if rois is None:
        raise RuntimeError("ROI comparison inputs contained no frames")
    audit = roi_motion_audit(truth_frames, selected_frames, rois)
    return {
        "status": "PASS" if frame_count > 0 else "FAIL",
        "profile": "10A_10B_roi_crop_motion_review",
        "truth_video": str(truth_video),
        "selected_video": str(selected_video),
        "fullrate_video": str(fullrate_video) if fullrate_video is not None else None,
        "output_video": str(output_video),
        "roi_profile": roi_profile,
        "roi_definitions": {name: list(values) for name, values in rois.items()},
        "frame_count": frame_count,
        "fps": fps,
        "diff_scale": diff_scale,
        "motion_audit": audit,
        "human_review_required": audit["status"] != "PASS",
        "unsafe_acceptance_count": 0,
    }


def _label(frame: Any, text: str) -> Any:
    import cv2

    output = frame.copy()
    cv2.rectangle(output, (0, 0), (min(output.shape[1], 480), 34), (0, 0, 0), -1)
    cv2.putText(output, text, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 1, cv2.LINE_AA)
    return output


def _label_08e(frame: Any, text: str) -> Any:
    """Use the exact banner typography from the historical 08E runner."""
    import cv2

    output = frame.copy()
    cv2.rectangle(output, (0, 0), (min(output.shape[1], 430), 34), (0, 0, 0), -1)
    cv2.putText(output, text, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)
    return output


def _open_writer(path: Path, fps: float, width: int, height: int) -> Any:
    import cv2

    path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"could not open diagnostic video writer: {path}")
    return writer


def render_zone_motion_video(
    input_video: Path,
    output_video: Path,
    *,
    zones: list[Zone] | None = None,
    max_frames: int | None = None,
) -> dict[str, Any]:
    """Stream the 03M camera-compensated green zone-motion diagnostic."""
    import cv2
    import numpy as np

    capture = cv2.VideoCapture(str(input_video))
    if not capture.isOpened():
        raise RuntimeError(f"could not open diagnostic input: {input_video}")
    fps = float(capture.get(cv2.CAP_PROP_FPS) or 30.0)
    ok, previous = capture.read()
    if not ok or previous is None:
        capture.release()
        raise RuntimeError(f"diagnostic input has no frames: {input_video}")
    height, width = previous.shape[:2]
    selected_zones = zones or waterfall_03m_zones(width, height)
    writer = _open_writer(output_video, fps, width, height)
    frame_count = 0
    zone_rows: list[dict[str, Any]] = []
    transform_rows: list[dict[str, Any]] = []
    try:
        empty_mask = np.zeros((height, width), dtype=np.uint8)
        writer.write(draw_zone_overlay(previous, empty_mask, selected_zones))
        frame_count = 1
        while max_frames is None or frame_count < max_frames:
            ok, current = capture.read()
            if not ok or current is None:
                break
            matrix, transform = estimate_pair_transform(previous, current)
            gray, mask = residual_motion(previous, current, matrix)
            frame_index = frame_count + 1
            zone_rows.extend(score_zones(gray, mask, selected_zones, frame_index))
            transform_rows.append({"frame_index": frame_index, **transform})
            writer.write(draw_zone_overlay(current, mask, selected_zones))
            previous = current
            frame_count += 1
    finally:
        capture.release()
        writer.release()
    return {
        "status": "PASS" if frame_count > 0 else "FAIL",
        "profile": "03M_waterfall_zone_motion",
        "input_video": str(input_video),
        "output_video": str(output_video),
        "frame_count": frame_count,
        "fps": fps,
        "resolution": [width, height],
        "zone_count": len(selected_zones),
        "zones": [zone.__dict__ for zone in selected_zones],
        "zone_rows": zone_rows,
        "transform_rows": transform_rows,
        "human_review_required": True,
        "final_tracking_proof_claimed": False,
        "unsafe_acceptance_count": 0,
    }


def _draw_residual_contours(frame: Any, mask: Any, *, minimum_area: float = 20.0, color: tuple[int, int, int] = (0, 255, 255)) -> Any:
    """Draw residual connected regions without turning them into AMCF masks."""
    import cv2

    output = frame.copy()
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    selected = [contour for contour in contours if cv2.contourArea(contour) >= minimum_area]
    if selected:
        cv2.drawContours(output, selected, -1, color, 1)
    return output


def _draw_component_coverage_overlay(frame: Any, residual_mask: Any, diagnostic_state: dict[str, Any] | None, frame_index: int) -> Any:
    """Overlay residual regions and real contour-backed Test 02 component coverage."""
    import cv2
    import numpy as np

    output = _draw_residual_contours(frame, residual_mask, minimum_area=20.0, color=(0, 255, 255))
    if diagnostic_state is None:
        return output
    height, width = frame.shape[:2]
    for track in diagnostic_tracks_for_frame(diagnostic_state, frame_index):
        packed = rasterize_track_mask(track, width, height)
        if packed is None:
            continue
        bbox, mask_bytes, _ = packed
        x, y, mask_width, mask_height = bbox
        local = np.frombuffer(mask_bytes, dtype=np.uint8).reshape((mask_height, mask_width))
        contours, _ = cv2.findContours(local, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        shifted = [contour + np.array([[[x, y]]], dtype=np.int32) for contour in contours]
        if shifted:
            cv2.drawContours(output, shifted, -1, (255, 0, 255), 1)
    return output


def _draw_camera_motion_vectors(frame: Any, matrix: Any, transform: dict[str, Any]) -> Any:
    """Show the estimated camera transform as a review diagnostic only."""
    import cv2

    output = frame.copy()
    height, width = output.shape[:2]
    center = (width // 2, height // 2)
    dx = float(matrix[0, 2])
    dy = float(matrix[1, 2])
    endpoint = (
        max(0, min(width - 1, int(round(center[0] + dx * 6.0)))),
        max(0, min(height - 1, int(round(center[1] + dy * 6.0)))),
    )
    cv2.arrowedLine(output, center, endpoint, (0, 255, 255), 2, cv2.LINE_AA, tipLength=0.25)
    cv2.putText(
        output,
        f"camera dx={dx:+.2f} dy={dy:+.2f} {transform.get('method_used', '')}",
        (8, 22),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    return output


def _draw_missing_motion_regions(frame: Any, residual_mask: Any) -> Any:
    """Show residual regions that still need component-coverage review."""
    import cv2

    output = _draw_residual_contours(frame, residual_mask, minimum_area=20.0, color=(0, 0, 255))
    cv2.putText(output, "residual regions requiring coverage review", (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
    return output


def render_03m_motion_truth_family(
    input_video: Path,
    output_dir: Path,
    *,
    diagnostic_state_manifest: Path | None = None,
    max_frames: int | None = None,
) -> dict[str, Any]:
    """Render the complete historical 03M diagnostic family in one pass.

    The outputs are process diagnostics only. The residual mask and coverage
    overlays never become component geometry unless the separate Test 02
    contour-backed state is explicitly supplied to the coverage view.
    """
    import cv2
    import numpy as np

    capture = cv2.VideoCapture(str(input_video))
    if not capture.isOpened():
        raise RuntimeError(f"could not open 03M diagnostic input: {input_video}")
    fps = float(capture.get(cv2.CAP_PROP_FPS) or 30.0)
    ok, previous = capture.read()
    if not ok or previous is None:
        capture.release()
        raise RuntimeError(f"03M diagnostic input has no frames: {input_video}")

    output_dir.mkdir(parents=True, exist_ok=True)
    height, width = previous.shape[:2]
    zones = waterfall_03m_zones(width, height)
    diagnostic_state = None
    if diagnostic_state_manifest is not None:
        diagnostic_state = load_diagnostic_state_manifest(diagnostic_state_manifest)

    paths = {
        "original_reference": output_dir / "03m_original_reference.mp4",
        "raw_screen_motion": output_dir / "03m_raw_screen_motion.mp4",
        "camera_compensated_residual": output_dir / "03m_camera_compensated_residual.mp4",
        "residual_motion_mask": output_dir / "03m_residual_motion_mask.mp4",
        "zone_motion_overlay": output_dir / "03m_zone_motion.mp4",
        "component_coverage_overlay": output_dir / "03m_component_coverage.mp4",
        "camera_motion_vectors": output_dir / "03m_camera_motion_vectors.mp4",
        "missing_motion_regions": output_dir / "03m_missing_motion_regions.mp4",
        "original_vs_motion_truth": output_dir / "03m_original_vs_motion_truth.mp4",
    }
    writers = {name: _open_writer(path, fps, width * (2 if name == "original_vs_motion_truth" else 1), height) for name, path in paths.items()}
    empty_mask = np.zeros((height, width), dtype=np.uint8)
    empty_frame = np.zeros_like(previous)
    identity = np.array([[1, 0, 0], [0, 1, 0]], dtype=np.float32)
    identity_info = {"method_used": "identity_first_frame"}
    transform_rows: list[dict[str, Any]] = []
    zone_rows: list[dict[str, Any]] = []
    missing_region_count = 0
    frame_count = 0

    def write_family_frame(frame: Any, raw_view: Any, residual_view: Any, mask_view: Any, zone_view: Any, coverage_view: Any, vector_view: Any, missing_view: Any) -> None:
        writers["original_reference"].write(frame)
        writers["raw_screen_motion"].write(raw_view)
        writers["camera_compensated_residual"].write(residual_view)
        writers["residual_motion_mask"].write(mask_view)
        writers["zone_motion_overlay"].write(zone_view)
        writers["component_coverage_overlay"].write(coverage_view)
        writers["camera_motion_vectors"].write(vector_view)
        writers["missing_motion_regions"].write(missing_view)
        writers["original_vs_motion_truth"].write(np.hstack([frame, zone_view]))

    try:
        first_zone = draw_zone_overlay(previous, empty_mask, zones)
        first_coverage = _draw_component_coverage_overlay(previous, empty_mask, diagnostic_state, 0)
        first_vector = _draw_camera_motion_vectors(previous, identity, identity_info)
        first_missing = _draw_missing_motion_regions(previous, empty_mask)
        write_family_frame(previous, empty_frame, empty_frame, cv2.cvtColor(empty_mask, cv2.COLOR_GRAY2BGR), first_zone, first_coverage, first_vector, first_missing)
        frame_count = 1
        while max_frames is None or frame_count < max_frames:
            ok, current = capture.read()
            if not ok or current is None:
                break
            matrix, transform = estimate_pair_transform(previous, current)
            gray, mask = residual_motion(previous, current, matrix)
            raw = cv2.absdiff(current, previous)
            raw_heat = cv2.applyColorMap(cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY), cv2.COLORMAP_INFERNO)
            raw_view = cv2.addWeighted(current, 0.75, raw_heat, 0.25, 0)
            residual_heat = cv2.applyColorMap(cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX), cv2.COLORMAP_TURBO)
            residual_view = cv2.addWeighted(current, 0.78, residual_heat, 0.22, 0)
            residual_view = _draw_residual_contours(residual_view, mask, minimum_area=12.0)
            zone_view = draw_zone_overlay(current, mask, zones)
            coverage_view = _draw_component_coverage_overlay(current, mask, diagnostic_state, frame_count)
            vector_view = _draw_camera_motion_vectors(current, matrix, transform)
            missing_view = _draw_missing_motion_regions(current, mask)
            write_family_frame(current, raw_view, residual_view, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), zone_view, coverage_view, vector_view, missing_view)
            zone_rows.extend(score_zones(gray, mask, zones, frame_count + 1))
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            missing_region_count += sum(1 for contour in contours if cv2.contourArea(contour) >= 20.0)
            transform_rows.append({"frame_index": frame_count + 1, **transform, "translation_dx": float(matrix[0, 2]), "translation_dy": float(matrix[1, 2])})
            previous = current
            frame_count += 1
    finally:
        capture.release()
        for writer in writers.values():
            writer.release()

    return {
        "status": "PASS" if frame_count > 0 else "FAIL",
        "profile": "03M_motion_truth_family",
        "input_video": str(input_video),
        "output_dir": str(output_dir),
        "output_videos": {key: str(value) for key, value in paths.items()},
        "frame_count": frame_count,
        "fps": fps,
        "resolution": [width, height],
        "zone_count": len(zones),
        "zones": [zone.__dict__ for zone in zones],
        "zone_rows": zone_rows,
        "transform_rows": transform_rows,
        "missing_motion_region_count": missing_region_count,
        "diagnostic_state_manifest": str(diagnostic_state_manifest) if diagnostic_state_manifest else None,
        "component_geometry_used": bool(diagnostic_state_manifest),
        "proxy_boxes_used_as_masks": False,
        "human_review_required": True,
        "final_tracking_proof_claimed": False,
        "unsafe_acceptance_count": 0,
    }


def render_motion_heat_comparison_video(
    truth_video: Path,
    decoded_video: Path,
    output_video: Path,
    *,
    max_frames: int | None = None,
) -> dict[str, Any]:
    """Stream the accepted 08E truth/decoded heat comparison."""
    import cv2
    import numpy as np

    truth_capture = cv2.VideoCapture(str(truth_video))
    decoded_capture = cv2.VideoCapture(str(decoded_video))
    if not truth_capture.isOpened() or not decoded_capture.isOpened():
        truth_capture.release()
        decoded_capture.release()
        raise RuntimeError("could not open both truth and decoded diagnostic videos")
    fps = float(truth_capture.get(cv2.CAP_PROP_FPS) or 30.0)
    writer = None
    frame_count = 0
    try:
        while max_frames is None or frame_count < max_frames:
            truth_ok, truth = truth_capture.read()
            decoded_ok, decoded = decoded_capture.read()
            if not truth_ok or not decoded_ok or truth is None or decoded is None:
                break
            if truth.shape != decoded.shape:
                raise ValueError("truth and decoded diagnostic frames have different shapes")
            if writer is None:
                height, width = truth.shape[:2]
                writer = _open_writer(output_video, fps, width * 5, height)
            if frame_count == 0:
                truth_heat = np.zeros_like(truth)
                decoded_heat = np.zeros_like(decoded)
            else:
                truth_heat = flow_magnitude_heatmap(previous_truth, truth)
                decoded_heat = flow_magnitude_heatmap(previous_decoded, decoded)
            truth_panel = _label_08e(truth, "truth baseline")
            decoded_panel = _label_08e(decoded, "decoded AMCF")
            truth_heat_panel = _label_08e(truth_heat, "truth motion heat")
            decoded_heat_panel = _label_08e(decoded_heat, "decoded motion heat")
            heat_diff = _label_08e(diff_panel(truth_heat, decoded_heat, 2), "motion heat diff")
            writer.write(np.hstack([truth_panel, decoded_panel, truth_heat_panel, decoded_heat_panel, heat_diff]))
            previous_truth = truth
            previous_decoded = decoded
            frame_count += 1
    finally:
        truth_capture.release()
        decoded_capture.release()
        if writer is not None:
            writer.release()
    return {
        "status": "PASS" if frame_count > 0 else "FAIL",
        "profile": "08E_stay_here_for_13_seconds_motion_heat",
        "truth_video": str(truth_video),
        "decoded_video": str(decoded_video),
        "output_video": str(output_video),
        "frame_count": frame_count,
        "fps": fps,
        "contract": "Farneback(0.5,3,15,3,5,1.2,0), per-frame NORM_MINMAX, TURBO, first frame black",
        "human_review_required": False,
        "unsafe_acceptance_count": 0,
    }


def _normalize_proxy_label(label: Any) -> str:
    """Normalize historical 12C/12D/12E proxy taxonomy names."""
    value = str(label or "uncertain").strip().lower()
    for prefix in ("final_", "calibrated_", "proxy_"):
        if value.startswith(prefix):
            value = value[len(prefix) :]
    aliases = {
        "person": "person_or_moving_object",
        "moving_object": "person_or_moving_object",
        "object": "person_or_moving_object",
        "water": "water_or_fluid_motion",
        "fluid": "water_or_fluid_motion",
        "camera_motion": "global_or_camera_motion",
        "global_motion": "global_or_camera_motion",
        "noise": "reject_noise",
    }
    return aliases.get(value, value)


def _proxy_track_id(track: dict[str, Any]) -> str:
    """Return the stable ID across the 12C, 12D, and 12E schemas."""
    for key in ("reviewed_track_id", "calibrated_track_id", "track_id", "original_track_id"):
        value = track.get(key)
        if value not in (None, ""):
            return str(value)
    return "?"


def _proxy_label(track: dict[str, Any]) -> str:
    """Read whichever label field a historical reviewed manifest provides."""
    for key in ("final_label", "final_reviewer_label", "label", "calibrated_label", "original_label"):
        value = track.get(key)
        if value not in (None, ""):
            return _normalize_proxy_label(value)
    return "uncertain"


def _proxy_color(final_label: str) -> tuple[int, int, int] | None:
    final_label = _normalize_proxy_label(final_label)
    return {
        "person_or_moving_object": (0, 255, 255),
        "water_or_fluid_motion": (255, 120, 0),
        "global_or_camera_motion": (255, 0, 255),
        "uncertain": (180, 180, 180),
        "reject_noise": None,
    }.get(final_label, (180, 180, 180))


def _draw_reviewed_proxy_track(frame: Any, track: dict[str, Any], frame_number: int, *, only_track_id: str | None = None) -> None:
    import cv2

    track_id = _proxy_track_id(track)
    if only_track_id is not None and track_id != str(only_track_id):
        return
    if not (int(track.get("frame_start", 0)) <= frame_number <= int(track.get("frame_end", 0))):
        return
    final_label = _proxy_label(track)
    color = _proxy_color(final_label)
    if color is None:
        return
    boxes = track.get("bboxes", [])
    if not boxes:
        return
    offset = frame_number - int(track.get("frame_start", 0))
    x, y, width, height = [int(value) for value in boxes[min(max(offset, 0), len(boxes) - 1)]]
    track_id = _proxy_track_id(track)
    short = {
        "person_or_moving_object": "obj",
        "water_or_fluid_motion": "fluid",
        "global_or_camera_motion": "global",
        "uncertain": "unc",
    }.get(final_label, "track")
    cv2.rectangle(frame, (x, y), (x + width, y + height), color, 1)
    cv2.putText(frame, f"{short}:{track_id}", (x, max(12, y - 3)), cv2.FONT_HERSHEY_SIMPLEX, 0.33, color, 1, cv2.LINE_AA)


def proxy_motion_audit(tracks: Iterable[dict[str, Any]], *, leftward_threshold_px: float = 2.0) -> dict[str, Any]:
    """Measure temporal proxy movement without claiming semantic correctness.

    The audit deliberately reports both all candidate tracks and the final
    reviewed person/object subset. A moving box is not by itself proof that
    the box belongs to a person; that distinction is part of the 12E contract.
    """
    direction_counts = {"leftward": 0, "rightward": 0, "stationary": 0, "insufficient_data": 0}
    by_label: dict[str, dict[str, int]] = {}
    leftward_tracks: list[dict[str, Any]] = []
    confirmed_person_tracks: list[dict[str, Any]] = []
    for track in tracks:
        boxes = track.get("bboxes") or []
        label = _proxy_label(track)
        label_counts = by_label.setdefault(label, {key: 0 for key in direction_counts})
        row = {
            "track_id": _proxy_track_id(track),
            "label": label,
            "frame_start": int(track.get("frame_start", 0)),
            "frame_end": int(track.get("frame_end", 0)),
            "bbox_count": len(boxes),
        }
        if len(boxes) < 2:
            direction = "insufficient_data"
            dx = None
            dy = None
        else:
            first = boxes[0]
            last = boxes[-1]
            dx = float(last[0]) - float(first[0])
            dy = float(last[1]) - float(first[1])
            if dx < -abs(leftward_threshold_px):
                direction = "leftward"
            elif dx > abs(leftward_threshold_px):
                direction = "rightward"
            else:
                direction = "stationary"
        direction_counts[direction] += 1
        label_counts[direction] += 1
        row.update({"direction": direction, "dx_px": dx, "dy_px": dy})
        if direction == "leftward":
            leftward_tracks.append(row)
        has_review_decision = any(
            track.get(key) not in (None, "")
            for key in ("final_label", "final_reviewer_label", "final_review_status")
        )
        if has_review_decision and label == "person_or_moving_object":
            confirmed_person_tracks.append(row)
    leftward_tracks.sort(key=lambda item: (item["dx_px"] is None, item["dx_px"] or 0))
    confirmed_leftward = [row for row in confirmed_person_tracks if row["direction"] == "leftward"]
    return {
        "track_count": sum(direction_counts.values()),
        "direction_counts": direction_counts,
        "by_label": by_label,
        "all_leftward_track_examples": leftward_tracks[:20],
        "reviewed_person_or_moving_object_count": len(confirmed_person_tracks),
        "reviewed_person_or_moving_object_leftward_count": len(confirmed_leftward),
        "right_to_left_person_behavior_proven": bool(confirmed_leftward),
        "boxes_are_temporal": any(row["bbox_count"] > 1 for row in confirmed_person_tracks),
        "semantic_correctness_proven": False,
        "human_review_required": True,
        "unsafe_acceptance_count": 0,
    }


def render_reviewed_proxy_video(
    source_video: Path,
    reviewed_manifest: Path,
    output_video: Path,
    *,
    only_track_id: str | None = None,
    include_labels: Iterable[str] | None = None,
    profile_name: str = "12E_reviewed_timelapse_proxy",
) -> dict[str, Any]:
    """Render the conservative 12E reviewed proxy without claiming masks."""
    import cv2

    tracks = json.loads(reviewed_manifest.read_text(encoding="utf-8"))
    allowed = (
        {_normalize_proxy_label(label) for label in include_labels}
        if include_labels is not None
        else {
        "person_or_moving_object",
        "water_or_fluid_motion",
        "global_or_camera_motion",
        "uncertain",
        }
    )
    capture = cv2.VideoCapture(str(source_video))
    if not capture.isOpened():
        raise RuntimeError(f"could not open proxy source: {source_video}")
    fps = float(capture.get(cv2.CAP_PROP_FPS) or 30.0)
    writer = None
    frame_count = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok or frame is None:
                break
            if writer is None:
                height, width = frame.shape[:2]
                writer = _open_writer(output_video, fps, width, height)
            frame_count += 1
            overlay = frame.copy()
            for track in tracks:
                if _proxy_label(track) in allowed:
                    _draw_reviewed_proxy_track(overlay, track, frame_count, only_track_id=only_track_id)
            writer.write(_label(overlay, "12E reviewed proxy; semantic/object AMCF not claimed"))
    finally:
        capture.release()
        if writer is not None:
            writer.release()
    counts: dict[str, int] = {}
    for track in tracks:
        label = _proxy_label(track)
        counts[label] = counts.get(label, 0) + 1
    motion_audit = proxy_motion_audit(tracks)
    return {
        "status": "PASS" if frame_count > 0 else "FAIL",
        "profile": profile_name,
        "source_video": str(source_video),
        "reviewed_manifest": str(reviewed_manifest),
        "output_video": str(output_video),
        "frame_count": frame_count,
        "fps": fps,
        "track_count": len(tracks),
        "final_label_counts": counts,
        "motion_audit": motion_audit,
        "only_track_id": only_track_id,
        "allowed_labels": sorted(allowed),
        "boxes_are_proxy_tracks": True,
        "pixel_segmentation_masks_used": False,
        "semantic_object_amcf_solved": False,
        "human_review_required": True,
        "unsafe_acceptance_count": 0,
    }
