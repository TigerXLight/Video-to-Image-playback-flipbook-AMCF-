from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

from amcf_component_event_archive import load_source_frame_manifest
from amcf_quality_metrics import read_ppm


def optical_flow_dependency_status() -> dict[str, bool]:
    return {
        "opencv_available": importlib.util.find_spec("cv2") is not None,
        "numpy_available": importlib.util.find_spec("numpy") is not None,
    }


def _require_optical_flow_dependencies() -> None:
    status = optical_flow_dependency_status()
    if not status["opencv_available"] or not status["numpy_available"]:
        raise RuntimeError("OpenCV optical flow requested but cv2/numpy are not importable")


def _bbox_from_mask(mask: Any) -> list[int]:
    import numpy as np

    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return [0, 0, 0, 0]
    x0 = int(xs.min())
    y0 = int(ys.min())
    x1 = int(xs.max()) + 1
    y1 = int(ys.max()) + 1
    return [x0, y0, x1 - x0, y1 - y0]


def build_optical_flow_track_report(source_manifest_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    _require_optical_flow_dependencies()
    import cv2
    import numpy as np

    source_manifest_path = Path(source_manifest_path)
    source_root = source_manifest_path.parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = load_source_frame_manifest(source_manifest_path)
    fps = float(manifest["fps"])
    entries = sorted(manifest["frame_entries"], key=lambda entry: int(entry["frame_index"]))
    frames: list[dict[str, Any]] = []
    previous_gray: Any | None = None
    previous_pixels: bytes | None = None
    width = int(manifest["width"])
    height = int(manifest["height"])

    for entry in entries:
        frame_index = int(entry["frame_index"])
        frame_path = source_root / str(entry["file"])
        frame_width, frame_height, pixels = read_ppm(frame_path)
        if frame_width != width or frame_height != height:
            raise ValueError("source frame dimensions do not match manifest")
        rgb = np.frombuffer(pixels, dtype=np.uint8).reshape((height, width, 3))
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        if previous_gray is None or previous_pixels is None:
            frames.append(
                {
                    "frame_index": frame_index,
                    "pts_seconds": frame_index / fps,
                    "track_id": "global_changed_region",
                    "bbox": [0, 0, width, height],
                    "component_update": True,
                    "update_reason": "initial_state",
                    "motion_median_px_s": 0.0,
                    "motion_p95_px_s": 0.0,
                    "motion_direction_deg": 0.0,
                    "flow_sample_count": 0,
                }
            )
            previous_gray = gray
            previous_pixels = pixels
            continue
        prev_rgb = np.frombuffer(previous_pixels, dtype=np.uint8).reshape((height, width, 3))
        diff = cv2.absdiff(prev_rgb, rgb)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(diff_gray, 0, 255, cv2.THRESH_BINARY)
        flow = cv2.calcOpticalFlowFarneback(previous_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        active = mask > 0
        sample_count = int(np.count_nonzero(active))
        if sample_count:
            local = flow[active, :].astype(np.float32)
            vx = local[:, 0]
            vy = local[:, 1]
            mags = np.sqrt(vx * vx + vy * vy) * fps
            med_vx = float(np.median(vx) * fps)
            med_vy = float(np.median(vy) * fps)
            median_px_s = float(np.median(mags))
            p95_px_s = float(np.percentile(mags, 95))
            direction_deg = float(math.degrees(math.atan2(med_vy, med_vx))) if med_vx or med_vy else 0.0
        else:
            median_px_s = 0.0
            p95_px_s = 0.0
            direction_deg = 0.0
        frames.append(
            {
                "frame_index": frame_index,
                "pts_seconds": frame_index / fps,
                "track_id": "global_changed_region",
                "bbox": _bbox_from_mask(active),
                "component_update": sample_count > 0,
                "update_reason": "motion" if sample_count > 0 else "held_state",
                "motion_median_px_s": median_px_s,
                "motion_p95_px_s": p95_px_s,
                "motion_direction_deg": direction_deg,
                "flow_sample_count": sample_count,
            }
        )
        previous_gray = gray
        previous_pixels = pixels

    report = {
        "schema": "amcf-optical-flow-track-report-v1",
        "ok": True,
        "source_manifest": str(source_manifest_path),
        "frame_count": len(frames),
        "track_count": 1,
        "dependency_status": optical_flow_dependency_status(),
        "frames": frames,
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "real_camera_required": False,
            "real_scanner_required": False,
        },
        "unsafe_acceptance_count": 0,
    }
    (output_dir / "optical_flow_track_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "optical_flow_track_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["frame_index", "track_id", "bbox_x", "bbox_y", "bbox_w", "bbox_h", "motion_median_px_s", "motion_p95_px_s", "update_reason"])
        for frame in frames:
            writer.writerow(
                [
                    frame["frame_index"],
                    frame["track_id"],
                    *frame["bbox"],
                    f"{frame['motion_median_px_s']:.6f}",
                    f"{frame['motion_p95_px_s']:.6f}",
                    frame["update_reason"],
                ]
            )
    return report
