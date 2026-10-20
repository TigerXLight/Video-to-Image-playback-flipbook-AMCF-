from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import math
import os
import shutil
import subprocess
import sys
import time
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


FPS_NUM = 24000
FPS_DEN = 1001
FPS = FPS_NUM / FPS_DEN
ANALYSIS_W = 960
ANALYSIS_H = 480
SOURCE_W = 3840
SOURCE_H = 1920
SIZE_CEILING = 11_661_942
TRACK_ORDER = [
    "WATERFALL_COLUMN",
    "WATER_IMPACT_FOAM",
    "MIST_SPRAY",
    "FOREGROUND_TREE_LEFT",
    "FOREGROUND_TREE_RIGHT",
    "MIDGROUND_TREE",
    "BRANCH_LEAF_GROUP_LEFT",
    "BRANCH_LEAF_GROUP_RIGHT",
]


@dataclass
class TrackState:
    track_id: str
    parent_id: str | None
    label: str
    color: tuple[int, int, int]
    min_interval: int
    motion_threshold_px_s: float
    error_threshold: float
    last_update_frame: int = -10_000
    last_area: float = 0.0
    last_centroid: tuple[float, float] = (0.0, 0.0)
    last_mask: np.ndarray | None = None
    update_times: list[float] = field(default_factory=list)
    patch_events: int = 0
    reseeds: int = 0
    lost_frames: int = 0


def root_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def source_video_path(root: Path) -> Path:
    original = root / "Test media" / "Waterfall" / "Original"
    matches = sorted(original.glob("*.mp4"))
    if not matches:
        raise FileNotFoundError(f"No .mp4 source found under {original}")
    return matches[0]


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("RUN", " ".join(f'"{c}"' if " " in c else c for c in cmd), flush=True)
    cp = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    if check and cp.returncode:
        if cp.stdout:
            print(cp.stdout, flush=True)
        if cp.stderr:
            print(cp.stderr, flush=True)
        cp.check_returncode()
    return cp


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def ffprobe_json(path: Path, cwd: Path) -> dict[str, Any]:
    cp = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-print_format",
            "json",
            str(path),
        ],
        cwd,
    )
    return json.loads(cp.stdout)


def ensure_clean_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def bgr_to_rgb(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def resize_analysis(frame_bgr: np.ndarray) -> np.ndarray:
    return cv2.resize(frame_bgr, (ANALYSIS_W, ANALYSIS_H), interpolation=cv2.INTER_AREA)


def morph(mask: np.ndarray, open_k: int = 3, close_k: int = 7) -> np.ndarray:
    mask = mask.astype(np.uint8)
    if open_k:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_k, open_k))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
    if close_k:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close_k, close_k))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    return (mask > 0).astype(np.uint8)


def roi_mask(x0: int, y0: int, x1: int, y1: int) -> np.ndarray:
    m = np.zeros((ANALYSIS_H, ANALYSIS_W), np.uint8)
    m[max(0, y0) : min(ANALYSIS_H, y1), max(0, x0) : min(ANALYSIS_W, x1)] = 1
    return m


def keep_largest(mask: np.ndarray, min_area: int = 50) -> np.ndarray:
    labels, stats = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)[1:3]
    if stats.shape[0] <= 1:
        return np.zeros_like(mask)
    areas = stats[1:, cv2.CC_STAT_AREA]
    idx = int(np.argmax(areas)) + 1
    if stats[idx, cv2.CC_STAT_AREA] < min_area:
        return np.zeros_like(mask)
    return (labels == idx).astype(np.uint8)


def keep_components(mask: np.ndarray, min_area: int = 50, max_components: int = 4) -> np.ndarray:
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    out = np.zeros_like(mask)
    comps = []
    for i in range(1, n):
        area = int(stats[i, cv2.CC_STAT_AREA])
        if area >= min_area:
            comps.append((area, i))
    for _, idx in sorted(comps, reverse=True)[:max_components]:
        out[labels == idx] = 1
    return out


def segment_frame(frame_small: np.ndarray, prev: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    hsv = cv2.cvtColor(frame_small, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
    h, s, v = cv2.split(hsv)
    green = ((h >= 28) & (h <= 98) & (s >= 35) & (v >= 24)).astype(np.uint8)
    bright_low_sat = ((v >= 145) & (s <= 78)).astype(np.uint8)
    pale_mist = ((v >= 112) & (s <= 58)).astype(np.uint8)

    masks: dict[str, np.ndarray] = {}

    water_roi = roi_mask(330, 118, 548, 478)
    water = bright_low_sat & water_roi
    water = morph(water, 5, 15)
    water = keep_largest(water, 500)
    masks["WATERFALL_COLUMN"] = water

    foam_roi = roi_mask(300, 335, 595, 480)
    foam = bright_low_sat & foam_roi
    foam = morph(foam, 3, 11)
    foam = keep_components(foam, 100, 3)
    masks["WATER_IMPACT_FOAM"] = foam

    spray_roi = roi_mask(250, 140, 625, 470)
    spray = pale_mist & spray_roi
    spray = spray & (cv2.dilate(water, np.ones((17, 17), np.uint8)) == 0)
    spray = morph(spray, 5, 17)
    spray = keep_components(spray, 120, 5)
    masks["MIST_SPRAY"] = spray

    left_tree = green & roi_mask(0, 0, 170, 480)
    left_tree = morph(left_tree, 5, 15)
    masks["FOREGROUND_TREE_LEFT"] = keep_components(left_tree, 300, 4)

    right_tree = green & roi_mask(742, 0, 960, 480)
    right_tree = morph(right_tree, 5, 17)
    masks["FOREGROUND_TREE_RIGHT"] = keep_components(right_tree, 300, 5)

    mid_tree = green & roi_mask(610, 0, 748, 480)
    mid_tree = morph(mid_tree, 5, 13)
    masks["MIDGROUND_TREE"] = keep_components(mid_tree, 180, 4)

    left_leaf = green & roi_mask(0, 160, 248, 345)
    edge_boost = (cv2.Canny(gray, 40, 120) > 0).astype(np.uint8)
    left_leaf = left_leaf & cv2.dilate(edge_boost, np.ones((3, 3), np.uint8))
    left_leaf = morph(left_leaf, 3, 7)
    masks["BRANCH_LEAF_GROUP_LEFT"] = keep_components(left_leaf, 40, 8)

    right_leaf = green & roi_mask(705, 170, 920, 370)
    right_leaf = right_leaf & cv2.dilate(edge_boost, np.ones((3, 3), np.uint8))
    right_leaf = morph(right_leaf, 3, 7)
    masks["BRANCH_LEAF_GROUP_RIGHT"] = keep_components(right_leaf, 40, 8)

    for key, mask in list(masks.items()):
        if mask.sum() == 0 and key in prev:
            masks[key] = prev[key].copy()
    return masks


def contours_for(mask: np.ndarray) -> list[list[list[int]]]:
    cs, _ = cv2.findContours((mask * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out: list[list[list[int]]] = []
    for c in cs:
        if cv2.contourArea(c) < 16:
            continue
        eps = max(1.0, 0.003 * cv2.arcLength(c, True))
        approx = cv2.approxPolyDP(c, eps, True)
        pts = approx.reshape(-1, 2)
        if len(pts) >= 3:
            out.append([[int(x * 4), int(y * 4)] for x, y in pts])
    return out


def mask_stats(mask: np.ndarray) -> dict[str, Any]:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return {
            "area": 0,
            "centroid": [0.0, 0.0],
            "bbox": [0, 0, 0, 0],
        }
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    return {
        "area": int(len(xs) * 16),
        "centroid": [float(xs.mean() * 4), float(ys.mean() * 4)],
        "bbox": [x0 * 4, y0 * 4, (x1 - x0) * 4, (y1 - y0) * 4],
    }


def flow_stats(flow: np.ndarray, global_flow: tuple[float, float], mask: np.ndarray) -> dict[str, Any]:
    ys, xs = np.nonzero(mask)
    if len(xs) < 10:
        return {
            "median_px_s": 0.0,
            "p95_px_s": 0.0,
            "direction_deg": 0.0,
            "sample_count": int(len(xs)),
        }
    local = flow[ys, xs, :].astype(np.float32)
    local[:, 0] -= global_flow[0]
    local[:, 1] -= global_flow[1]
    mags = np.sqrt(local[:, 0] ** 2 + local[:, 1] ** 2) * FPS * 4.0
    med_vx = float(np.median(local[:, 0]) * FPS * 4.0)
    med_vy = float(np.median(local[:, 1]) * FPS * 4.0)
    return {
        "median_px_s": float(np.median(mags)),
        "p95_px_s": float(np.percentile(mags, 95)),
        "direction_deg": float(math.degrees(math.atan2(med_vy, med_vx))) if med_vx or med_vy else 0.0,
        "sample_count": int(len(xs)),
    }


def full_mask_from_small(mask: np.ndarray) -> np.ndarray:
    return cv2.resize(mask, (SOURCE_W, SOURCE_H), interpolation=cv2.INTER_NEAREST).astype(np.uint8)


def rgba_patch(frame_bgr: np.ndarray, mask_small: np.ndarray) -> tuple[Image.Image, list[int]]:
    full_mask = full_mask_from_small(mask_small)
    ys, xs = np.nonzero(full_mask)
    if len(xs) == 0:
        raise ValueError("empty mask")
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    rgb = bgr_to_rgb(frame_bgr[y0:y1, x0:x1])
    alpha = (full_mask[y0:y1, x0:x1] * 255).astype(np.uint8)
    rgba = np.dstack([rgb, alpha])
    return Image.fromarray(rgba, "RGBA"), [x0, y0, x1 - x0, y1 - y0]


def save_webp_bytes(image: Image.Image, quality: int) -> bytes:
    bio = io.BytesIO()
    image.save(bio, "WEBP", quality=quality, method=4, lossless=False)
    return bio.getvalue()


def source_capture(source: Path) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise RuntimeError(f"OpenCV could not open {source}")
    return cap


def make_tracks() -> dict[str, TrackState]:
    colors = {
        "WATERFALL_COLUMN": (0, 220, 255),
        "WATER_IMPACT_FOAM": (255, 255, 0),
        "MIST_SPRAY": (230, 160, 255),
        "FOREGROUND_TREE_LEFT": (80, 255, 80),
        "FOREGROUND_TREE_RIGHT": (80, 180, 255),
        "MIDGROUND_TREE": (255, 160, 80),
        "BRANCH_LEAF_GROUP_LEFT": (120, 255, 160),
        "BRANCH_LEAF_GROUP_RIGHT": (255, 120, 160),
    }
    parent = {
        "WATER_IMPACT_FOAM": "WATERFALL_COLUMN",
        "MIST_SPRAY": "WATERFALL_COLUMN",
        "BRANCH_LEAF_GROUP_LEFT": "FOREGROUND_TREE_LEFT",
        "BRANCH_LEAF_GROUP_RIGHT": "FOREGROUND_TREE_RIGHT",
    }
    min_intervals = {
        "WATERFALL_COLUMN": 4,
        "WATER_IMPACT_FOAM": 3,
        "MIST_SPRAY": 6,
        "FOREGROUND_TREE_LEFT": 18,
        "FOREGROUND_TREE_RIGHT": 18,
        "MIDGROUND_TREE": 18,
        "BRANCH_LEAF_GROUP_LEFT": 10,
        "BRANCH_LEAF_GROUP_RIGHT": 10,
    }
    motion_thresholds = {
        "WATERFALL_COLUMN": 28.0,
        "WATER_IMPACT_FOAM": 24.0,
        "MIST_SPRAY": 18.0,
        "FOREGROUND_TREE_LEFT": 10.0,
        "FOREGROUND_TREE_RIGHT": 10.0,
        "MIDGROUND_TREE": 10.0,
        "BRANCH_LEAF_GROUP_LEFT": 12.0,
        "BRANCH_LEAF_GROUP_RIGHT": 12.0,
    }
    return {
        tid: TrackState(
            track_id=tid,
            parent_id=parent.get(tid),
            label=tid.replace("_", " ").title(),
            color=colors[tid],
            min_interval=min_intervals[tid],
            motion_threshold_px_s=motion_thresholds[tid],
            error_threshold=11.0,
        )
        for tid in TRACK_ORDER
    }


def draw_overlay(frame_small: np.ndarray, records: list[dict[str, Any]]) -> np.ndarray:
    out = frame_small.copy()
    for rec in records:
        color = tuple(int(c) for c in rec["color_bgr"])
        small_contours = []
        for contour in rec["contours"]:
            pts = np.array([[p[0] // 4, p[1] // 4] for p in contour], np.int32).reshape((-1, 1, 2))
            small_contours.append(pts)
        cv2.drawContours(out, small_contours, -1, color, 2)
        cx, cy = rec["centroid"]
        x, y = int(cx // 4), int(cy // 4)
        label = f"{rec['track_id']} {rec['motion_median_px_s']:.0f}px/s c={rec['confidence']:.2f}"
        cv2.circle(out, (x, y), 4, color, -1)
        cv2.putText(out, label, (min(x + 8, ANALYSIS_W - 260), max(18, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 3)
        cv2.putText(out, label, (min(x + 8, ANALYSIS_W - 260), max(18, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.42, color, 1)
    return out


def extract_audio(source: Path, audio_path: Path, cwd: Path) -> None:
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(source), "-vn", "-c:a", "copy", str(audio_path)], cwd)


def build_archive_and_tracks(root: Path, outdir: Path, max_frames: int = 288) -> dict[str, Any]:
    source = source_video_path(root)
    ensure_clean_dir(outdir)
    work = outdir / "work"
    ensure_clean_dir(work)
    diag = outdir / "tracking_diagnostics"
    ensure_clean_dir(diag)
    event_dir = work / "events"
    ensure_clean_dir(event_dir)
    audio_path = work / "audio.m4a"
    extract_audio(source, audio_path, root)

    cap = source_capture(source)
    tracks = make_tracks()
    prev_small: np.ndarray | None = None
    prev_gray: np.ndarray | None = None
    prev_masks: dict[str, np.ndarray] = {}
    frame_records: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    source_hash_samples: dict[str, str] = {}
    base_bytes: bytes | None = None
    global_flow_series: list[list[float]] = []

    frame_count = 0
    t0 = time.time()
    while frame_count < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        if frame.shape[1] != SOURCE_W or frame.shape[0] != SOURCE_H:
            raise RuntimeError(f"Expected {SOURCE_W}x{SOURCE_H}, got {frame.shape[1]}x{frame.shape[0]}")
        small = resize_analysis(frame)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        masks = segment_frame(small, prev_masks)

        if frame_count == 0:
            base_img = Image.fromarray(bgr_to_rgb(frame))
            base_bytes = save_webp_bytes(base_img, quality=58)
            flow = np.zeros((ANALYSIS_H, ANALYSIS_W, 2), np.float32)
            global_flow = (0.0, 0.0)
        else:
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag = np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2)
            low_motion = mag < np.percentile(mag, 60)
            if np.any(low_motion):
                global_flow = (float(np.median(flow[:, :, 0][low_motion])), float(np.median(flow[:, :, 1][low_motion])))
            else:
                global_flow = (float(np.median(flow[:, :, 0])), float(np.median(flow[:, :, 1])))
        global_flow_series.append([global_flow[0] * FPS * 4.0, global_flow[1] * FPS * 4.0])

        per_frame: list[dict[str, Any]] = []
        for tid in TRACK_ORDER:
            st = tracks[tid]
            mask = masks[tid]
            stats = mask_stats(mask)
            fstats = flow_stats(flow, global_flow, mask)
            area = float(stats["area"])
            previous_area = st.last_area
            area_delta = abs(area - previous_area) / max(area, previous_area, 1.0)
            visible = area > 0
            if not visible:
                st.lost_frames += 1
            confidence = 0.0 if not visible else float(max(0.15, min(0.99, 1.0 - area_delta * 0.75)))
            if frame_count == 0:
                reason = "initial_state"
                do_update = True
            else:
                interval_ok = (frame_count - st.last_update_frame) >= st.min_interval
                motion_ok = fstats["median_px_s"] >= st.motion_threshold_px_s
                shape_ok = area_delta >= 0.035
                do_update = interval_ok and (motion_ok or shape_ok)
                if do_update:
                    reason = "motion" if motion_ok else "shape_change"
                else:
                    reason = "held_state"

            contours = contours_for(mask)
            if visible and not contours:
                st.reseeds += 1
                confidence *= 0.35
            rec = {
                "frame_index": frame_count,
                "pts_seconds": frame_count / FPS,
                "track_id": tid,
                "parent_id": st.parent_id,
                "label": st.label,
                "visible_state": "visible" if visible else "lost",
                "occluded_state": "none",
                "confidence": confidence,
                "centroid": stats["centroid"],
                "area": stats["area"],
                "bbox": stats["bbox"],
                "contours": contours,
                "motion_median_px_s": fstats["median_px_s"],
                "motion_p95_px_s": fstats["p95_px_s"],
                "motion_direction_deg": fstats["direction_deg"],
                "flow_sample_count": fstats["sample_count"],
                "global_compensation_px_s": [global_flow[0] * FPS * 4.0, global_flow[1] * FPS * 4.0],
                "component_update": bool(do_update),
                "update_reason": reason,
                "color_bgr": list(st.color),
            }
            if do_update and visible:
                patch, bbox = rgba_patch(frame, mask)
                patch_bytes = save_webp_bytes(patch, quality=48 if "WATER" in tid or "MIST" in tid else 42)
                event_name = f"events/{frame_count:04d}_{tid}.webp"
                (work / event_name).parent.mkdir(parents=True, exist_ok=True)
                (work / event_name).write_bytes(patch_bytes)
                ev = {
                    "frame_index": frame_count,
                    "pts_seconds": frame_count / FPS,
                    "track_id": tid,
                    "bbox": bbox,
                    "path": event_name,
                    "bytes": len(patch_bytes),
                    "reason": reason,
                }
                events.append(ev)
                rec["archive_event"] = ev
                st.last_update_frame = frame_count
                st.update_times.append(frame_count / FPS)
                st.patch_events += 1

            st.last_area = area
            st.last_centroid = tuple(stats["centroid"])
            st.last_mask = mask
            per_frame.append(rec)

        if frame_count in {0, 47, 143, 215, 287}:
            overlay = draw_overlay(small, per_frame)
            cv2.imwrite(str(diag / f"source_tracking_frame_{frame_count + 1:03d}.jpg"), overlay)
            source_hash_samples[str(frame_count)] = hashlib.sha256(bgr_to_rgb(frame).tobytes()).hexdigest().upper()

        frame_records.append(
            {
                "frame_index": frame_count,
                "pts_seconds": frame_count / FPS,
                "tracks": per_frame,
            }
        )
        prev_small = small
        prev_gray = gray
        prev_masks = masks
        frame_count += 1

        if frame_count % 24 == 0:
            print(f"tracked {frame_count}/{max_frames} frames in {time.time() - t0:.1f}s", flush=True)

    cap.release()
    if base_bytes is None:
        raise RuntimeError("No frames decoded from source")
    (work / "base.webp").write_bytes(base_bytes)

    manifest = {
        "schema": "amcf-test02-component-archive-v1",
        "created_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "source": {
            "path": str(source),
            "sha256": sha256_file(source),
            "bytes": source.stat().st_size,
            "width": SOURCE_W,
            "height": SOURCE_H,
            "fps": f"{FPS_NUM}/{FPS_DEN}",
            "frames": frame_count,
        },
        "analysis_resolution": [ANALYSIS_W, ANALYSIS_H],
        "archive_resolution": [SOURCE_W, SOURCE_H],
        "synthetic_interpolation": False,
        "base": {"path": "base.webp", "bytes": len(base_bytes), "frame_index": 0},
        "audio": {"path": "audio.m4a", "bytes": audio_path.stat().st_size},
        "tracks": [
            {
                "track_id": st.track_id,
                "parent_id": st.parent_id,
                "label": st.label,
                "min_interval_frames": st.min_interval,
                "motion_threshold_px_s": st.motion_threshold_px_s,
                "patch_events": st.patch_events,
                "lost_frames": st.lost_frames,
                "reseeds": st.reseeds,
                "update_moments_per_second": sliding_rate(st.update_times, frame_count / FPS),
            }
            for st in tracks.values()
        ],
        "events": events,
        "global_flow_px_s": global_flow_series,
        "source_hash_samples": source_hash_samples,
    }
    (work / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    tracks_json = {
        "schema": "amcf-test02-tracks-v1",
        "fps": FPS,
        "source_size": [SOURCE_W, SOURCE_H],
        "display_size": [ANALYSIS_W, ANALYSIS_H],
        "synthetic_interpolation": False,
        "frames": frame_records,
    }
    tracks_path = outdir / "tracks_manifest.json"
    tracks_path.write_text(json.dumps(tracks_json), encoding="utf-8")

    csv_path = outdir / "track_metrics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "frame_index",
                "pts_seconds",
                "track_id",
                "parent_id",
                "centroid_x",
                "centroid_y",
                "area",
                "bbox_x",
                "bbox_y",
                "bbox_w",
                "bbox_h",
                "confidence",
                "motion_median_px_s",
                "motion_p95_px_s",
                "component_update",
                "update_reason",
            ]
        )
        for fr in frame_records:
            for rec in fr["tracks"]:
                writer.writerow(
                    [
                        rec["frame_index"],
                        f"{rec['pts_seconds']:.6f}",
                        rec["track_id"],
                        rec["parent_id"] or "",
                        f"{rec['centroid'][0]:.2f}",
                        f"{rec['centroid'][1]:.2f}",
                        rec["area"],
                        *rec["bbox"],
                        f"{rec['confidence']:.4f}",
                        f"{rec['motion_median_px_s']:.4f}",
                        f"{rec['motion_p95_px_s']:.4f}",
                        int(rec["component_update"]),
                        rec["update_reason"],
                    ]
                )

    archive = outdir / "waterfall_test02.amcf.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for p in sorted(work.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(work).as_posix())
    manifest["archive"] = {
        "path": str(archive),
        "bytes": archive.stat().st_size,
        "sha256": sha256_file(archive),
        "under_source_size_ceiling": archive.stat().st_size <= SIZE_CEILING,
    }
    (outdir / "archive_manifest_resolved.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"manifest": manifest, "tracks_path": tracks_path, "archive": archive}


def sliding_rate(times: list[float], duration: float) -> float:
    if duration <= 0:
        return 0.0
    return len(times) / duration


def decode_archive(root: Path, archive: Path, outdir: Path) -> dict[str, Any]:
    decode_dir = outdir / "decoded_frames"
    ensure_clean_dir(decode_dir)
    with zipfile.ZipFile(archive, "r") as zf:
        manifest = json.loads(zf.read("manifest.json"))
        base = Image.open(io.BytesIO(zf.read(manifest["base"]["path"]))).convert("RGBA")
        frame_count = int(manifest["source"]["frames"])
        events = sorted(manifest["events"], key=lambda e: (e["frame_index"], e["track_id"]))
        audio_bytes = zf.read(manifest["audio"]["path"])

        audio_path = outdir / "archive_audio.m4a"
        audio_path.write_bytes(audio_bytes)
        frame = base.copy()
        event_idx = 0
        hashes: list[str] = []
        raw_cmd = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{SOURCE_W}x{SOURCE_H}",
            "-r",
            f"{FPS_NUM}/{FPS_DEN}",
            "-i",
            "-",
            "-i",
            str(audio_path),
            "-map",
            "0:v",
            "-map",
            "1:a?",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            str(outdir / "reconstructed_from_amcf.mp4"),
        ]
        proc = subprocess.Popen(raw_cmd, cwd=str(root), stdin=subprocess.PIPE)
        if proc.stdin is None:
            raise RuntimeError("ffmpeg pipe did not open")
        sample_indices = {0, 47, 143, 215, 287}
        for frame_index in range(frame_count):
            while event_idx < len(events) and int(events[event_idx]["frame_index"]) <= frame_index:
                ev = events[event_idx]
                patch = Image.open(io.BytesIO(zf.read(ev["path"]))).convert("RGBA")
                frame.alpha_composite(patch, tuple(ev["bbox"][:2]))
                event_idx += 1
            rgb = frame.convert("RGB")
            arr = np.asarray(rgb)
            hashes.append(hashlib.sha256(arr.tobytes()).hexdigest().upper())
            if frame_index in sample_indices:
                rgb.resize((ANALYSIS_W, ANALYSIS_H), Image.Resampling.LANCZOS).save(
                    outdir / "visual_comparisons" / f"reconstructed_frame_{frame_index + 1:03d}.jpg",
                    quality=92,
                )
            proc.stdin.write(arr.tobytes())
        proc.stdin.close()
        rc = proc.wait()
        if rc:
            raise RuntimeError(f"ffmpeg reconstruction encode failed with exit code {rc}")
    decoded_hash_path = outdir / "decoded_state_hashes.txt"
    decoded_hash_path.write_text("\n".join(f"{i:04d}\t{h}" for i, h in enumerate(hashes)), encoding="utf-8")
    return {
        "reconstructed_video": outdir / "reconstructed_from_amcf.mp4",
        "decoded_hashes": decoded_hash_path,
        "decoded_frames": len(hashes),
    }


def compare_quality(root: Path, source: Path, recon: Path, outdir: Path, sample_step: int = 24) -> dict[str, Any]:
    src_cap = source_capture(source)
    rec_cap = source_capture(recon)
    metrics = []
    ensure_clean_dir(outdir / "visual_comparisons")
    frame_index = 0
    while True:
        ok1, s = src_cap.read()
        ok2, r = rec_cap.read()
        if not ok1 or not ok2:
            break
        if frame_index % sample_step == 0 or frame_index in {47, 143, 215, 287}:
            if r.shape[:2] != s.shape[:2]:
                r = cv2.resize(r, (s.shape[1], s.shape[0]), interpolation=cv2.INTER_LINEAR)
            s_rgb = bgr_to_rgb(s)
            r_rgb = bgr_to_rgb(r)
            mae = float(np.mean(np.abs(s_rgb.astype(np.int16) - r_rgb.astype(np.int16))))
            psnr = float(peak_signal_noise_ratio(s_rgb, r_rgb, data_range=255))
            small_s = cv2.resize(s_rgb, (960, 480), interpolation=cv2.INTER_AREA)
            small_r = cv2.resize(r_rgb, (960, 480), interpolation=cv2.INTER_AREA)
            ssim = float(structural_similarity(small_s, small_r, channel_axis=2, data_range=255))
            metrics.append({"frame_index": frame_index, "mae": mae, "psnr_db": psnr, "ssim_960": ssim})
            if frame_index in {0, 47, 143, 215, 287}:
                diff = np.clip(np.abs(small_s.astype(np.int16) - small_r.astype(np.int16)) * 5, 0, 255).astype(np.uint8)
                Image.fromarray(small_s).save(outdir / "visual_comparisons" / f"source_frame_{frame_index + 1:03d}.jpg", quality=92)
                Image.fromarray(small_r).save(outdir / "visual_comparisons" / f"recon_frame_{frame_index + 1:03d}.jpg", quality=92)
                Image.fromarray(diff).save(outdir / "visual_comparisons" / f"diff_x5_frame_{frame_index + 1:03d}.jpg", quality=92)
        frame_index += 1
    src_cap.release()
    rec_cap.release()
    summary = {
        "frames_compared": frame_index,
        "sample_step": sample_step,
        "mean_mae": float(np.mean([m["mae"] for m in metrics])) if metrics else None,
        "mean_psnr_db": float(np.mean([m["psnr_db"] for m in metrics])) if metrics else None,
        "mean_ssim_960": float(np.mean([m["ssim_960"] for m in metrics])) if metrics else None,
        "samples": metrics,
    }
    (outdir / "quality_metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def make_viewer(root: Path, outdir: Path, source: Path, recon: Path) -> dict[str, Any]:
    comparison = outdir / "viewer" / "comparison_sync.mp4"
    diff = outdir / "viewer" / "comparison_difference.mp4"
    ensure_clean_dir(comparison.parent)
    tracks_src = outdir / "tracks_manifest.json"
    shutil.copy2(tracks_src, comparison.parent / "tracks_manifest.json")
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-i",
            str(recon),
            "-filter_complex",
            "[0:v]scale=960:480,setpts=PTS-STARTPTS[left];[1:v]scale=960:480,setpts=PTS-STARTPTS[right];[left][right]hstack=inputs=2[v]",
            "-map",
            "[v]",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "21",
            "-pix_fmt",
            "yuv420p",
            str(comparison),
        ],
        root,
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-i",
            str(recon),
            "-filter_complex",
            "[0:v]scale=960:480,format=rgb24,setpts=PTS-STARTPTS,split=2[left][leftdiff];[1:v]scale=960:480,format=rgb24,setpts=PTS-STARTPTS[r];[leftdiff][r]blend=all_mode=difference,eq=contrast=7:brightness=0.08,format=rgb24[d];[left][d]hstack=inputs=2[v]",
            "-map",
            "[v]",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "21",
            "-pix_fmt",
            "yuv420p",
            str(diff),
        ],
        root,
    )
    (comparison.parent / "index.html").write_text(viewer_html(), encoding="utf-8")
    return {"comparison": comparison, "difference": diff, "index": comparison.parent / "index.html"}


def viewer_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AMCF Test 02 Viewer</title>
<style>
body{margin:0;background:#101214;color:#e8ecef;font-family:Segoe UI,Arial,sans-serif}
main{max-width:1500px;margin:0 auto;padding:16px}
.stage{position:relative;background:#050607;aspect-ratio:4/1;border:1px solid #343a40}
video,canvas{position:absolute;inset:0;width:100%;height:100%}
.bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:12px 0}
button,select,input{background:#1e252b;color:#eef3f6;border:1px solid #59636c;border-radius:4px;padding:7px 9px}
input[type=range]{flex:1;min-width:220px}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px}
.metric{background:#171c20;border:1px solid #333b42;border-radius:6px;padding:8px;font-size:13px}
.labels{display:flex;justify-content:space-between;font-size:13px;color:#b9c2c9;margin-bottom:4px}
</style>
</head>
<body>
<main>
<div class="labels"><span>Source</span><span>AMCF reconstruction / difference view</span></div>
<div class="stage"><video id="v" src="comparison_sync.mp4" muted playsinline></video><canvas id="c"></canvas></div>
<div class="bar">
<button id="play">Play</button><button id="back">-1 frame</button><button id="fwd">+1 frame</button>
<select id="speed"><option>0.25</option><option>0.5</option><option selected>1</option><option>2</option></select>
<label><input id="loop" type="checkbox" checked> loop</label>
<label><input id="overlay" type="checkbox" checked> contours</label>
<label><input id="vectors" type="checkbox" checked> metrics</label>
<label><input id="diff" type="checkbox"> difference</label>
<select id="focus"><option value="">all objects</option></select>
<input id="seek" type="range" min="0" max="287" value="0">
<button id="export">Export frame data</button>
</div>
<div id="readout"></div>
<div class="metrics" id="metrics"></div>
</main>
<script>
const fps = 24000/1001;
let data = null;
const video = document.getElementById('v');
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const seek = document.getElementById('seek');
const focus = document.getElementById('focus');
fetch('tracks_manifest.json').then(r=>r.json()).then(j=>{data=j; init(); draw();});
function init(){
  const ids = data.frames[0].tracks.map(t=>t.track_id);
  for(const id of ids){ const o=document.createElement('option'); o.value=id; o.textContent=id; focus.appendChild(o); }
}
function frameIndex(){ return Math.max(0, Math.min(data.frames.length-1, Math.round(video.currentTime*fps))); }
function draw(){
  requestAnimationFrame(draw);
  if(!data) return;
  const rect = canvas.getBoundingClientRect();
  const dpr = devicePixelRatio || 1;
  canvas.width = Math.round(rect.width*dpr); canvas.height = Math.round(rect.height*dpr);
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,rect.width,rect.height);
  const i = frameIndex();
  seek.value = i;
  const fr = data.frames[i];
  document.getElementById('readout').textContent = `frame ${i+1}/${data.frames.length}  pts ${fr.pts_seconds.toFixed(3)}s  speed ${video.playbackRate}x`;
  const sx = rect.width / 1920, sy = rect.height / 480;
  const showOverlay = document.getElementById('overlay').checked;
  const showMetrics = document.getElementById('vectors').checked;
  const selected = focus.value;
  let html = '';
  for(const t of fr.tracks){
    if(selected && t.track_id !== selected) continue;
    const color = `rgb(${t.color_bgr[2]},${t.color_bgr[1]},${t.color_bgr[0]})`;
    if(showOverlay){
      ctx.lineWidth = 2; ctx.strokeStyle = color; ctx.fillStyle = color;
      for(const contour of t.contours){
        ctx.beginPath();
        contour.forEach((p,k)=>{ const x=p[0]/4*sx; const y=p[1]/4*sy; if(k) ctx.lineTo(x,y); else ctx.moveTo(x,y); });
        ctx.closePath(); ctx.stroke();
        ctx.beginPath();
        contour.forEach((p,k)=>{ const x=(p[0]/4+960)*sx; const y=p[1]/4*sy; if(k) ctx.lineTo(x,y); else ctx.moveTo(x,y); });
        ctx.closePath(); ctx.stroke();
      }
      const cx=t.centroid[0]/4*sx, cy=t.centroid[1]/4*sy;
      ctx.beginPath(); ctx.arc(cx,cy,4,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(cx+960*sx,cy,4,0,Math.PI*2); ctx.fill();
    }
    if(showMetrics){
      html += `<div class="metric"><b>${t.track_id}</b><br>update: ${t.component_update ? t.update_reason : 'held'}<br>motion median: ${t.motion_median_px_s.toFixed(1)} px/s<br>confidence: ${t.confidence.toFixed(2)}<br>centroid: ${t.centroid.map(v=>v.toFixed(0)).join(', ')}</div>`;
    }
  }
  document.getElementById('metrics').innerHTML = html;
}
document.getElementById('play').onclick=()=>{ if(video.paused){video.play(); play.textContent='Pause'} else {video.pause(); play.textContent='Play'} };
document.getElementById('back').onclick=()=>{ video.pause(); video.currentTime=Math.max(0,(frameIndex()-1)/fps); };
document.getElementById('fwd').onclick=()=>{ video.pause(); video.currentTime=Math.min(video.duration,(frameIndex()+1)/fps); };
document.getElementById('speed').onchange=e=>video.playbackRate=parseFloat(e.target.value);
document.getElementById('loop').onchange=e=>video.loop=e.target.checked; video.loop=true;
seek.oninput=e=>{ video.pause(); video.currentTime=parseInt(e.target.value,10)/fps; };
document.getElementById('diff').onchange=e=>{ const t=video.currentTime; const was=!video.paused; video.src=e.target.checked?'comparison_difference.mp4':'comparison_sync.mp4'; video.currentTime=t; if(was) video.play(); };
document.getElementById('export').onclick=()=>{ const fr=data.frames[frameIndex()]; const blob=new Blob([JSON.stringify(fr,null,2)],{type:'application/json'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=`amcf_frame_${fr.frame_index+1}.json`; a.click(); };
</script>
</body>
</html>
"""


def make_av1_baseline(root: Path, source: Path, outdir: Path) -> dict[str, Any]:
    baseline = outdir / "baseline_conventional_av1_crf32.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-c:v",
            "libsvtav1",
            "-preset",
            "10",
            "-crf",
            "32",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            str(baseline),
        ],
        root,
        check=False,
    )
    if not baseline.exists() or baseline.stat().st_size == 0:
        baseline = outdir / "baseline_conventional_av1_libaom_crf32.mkv"
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(source),
                "-c:v",
                "libaom-av1",
                "-cpu-used",
                "8",
                "-crf",
                "32",
                "-b:v",
                "0",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "copy",
                str(baseline),
            ],
            root,
        )
    return {
        "path": baseline,
        "bytes": baseline.stat().st_size,
        "sha256": sha256_file(baseline),
    }


def write_report(root: Path, outdir: Path, audit: dict[str, Any]) -> None:
    manifest = json.loads((outdir / "archive_manifest_resolved.json").read_text(encoding="utf-8"))
    quality = json.loads((outdir / "quality_metrics.json").read_text(encoding="utf-8"))
    lines = [
        "# AMCF Test 02 Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Verdict",
        "",
        "FAIL for final AMCF acceptance. Test 02 does demonstrate persistent per-frame object-bound masks, contours, track IDs, object-relative labels, optical-flow motion metrics and a self-contained component archive/decoder. It does not meet acceptable native-resolution reconstruction fidelity, and it should not be represented as a successful replacement for conventional AV1.",
        "",
        "## Source",
        "",
        f"- Path: `{manifest['source']['path']}`",
        f"- SHA256: `{manifest['source']['sha256']}`",
        f"- Bytes: {manifest['source']['bytes']:,}",
        f"- Video: {manifest['source']['width']}x{manifest['source']['height']} at {manifest['source']['fps']}, {manifest['source']['frames']} frames",
        f"- Synthetic interpolation: {manifest['synthetic_interpolation']}",
        "",
        "## Tracking Evidence",
        "",
        "Per-frame masks are regenerated from source-visible image content and recorded as contours in `tracks_manifest.json`; no static tile grid is used. Optical flow is measured inside each current mask in pixels per second, after subtracting a simple whole-image median-flow compensation estimate.",
        "",
        "| Track | Parent | Events | Mean update moments/s | Lost frames | Reseeds |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for tr in manifest["tracks"]:
        lines.append(
            f"| {tr['track_id']} | {tr['parent_id'] or ''} | {tr['patch_events']} | {tr['update_moments_per_second']:.2f} | {tr['lost_frames']} | {tr['reseeds']} |"
        )
    lines += [
        "",
        "Diagnostic overlays: `tracking_diagnostics/source_tracking_frame_001.jpg`, `048`, `144`, `216`, `288`.",
        "",
        "## Archive And Decode",
        "",
        f"- Archive: `{Path(manifest['archive']['path']).name}`",
        f"- Archive bytes: {manifest['archive']['bytes']:,}",
        f"- Original byte ceiling: {SIZE_CEILING:,}",
        f"- Under ceiling: {manifest['archive']['under_source_size_ceiling']}",
        f"- Base image bytes: {manifest['base']['bytes']:,}",
        f"- Audio bytes: {manifest['audio']['bytes']:,}",
        f"- Component patch events: {len(manifest['events']):,}",
        "- Decoder reads only the `.amcf.zip` archive and does not read source video pixels.",
        "",
        "## Reconstruction Quality",
        "",
        f"- Frames compared: {quality['frames_compared']}",
        f"- Sampled mean MAE: {quality['mean_mae']:.3f}",
        f"- Sampled mean PSNR: {quality['mean_psnr_db']:.3f} dB",
        f"- Sampled mean SSIM at 960x480 analysis scale: {quality['mean_ssim_960']:.4f}",
        "",
        "The low score is expected for this CPU-only component prototype: held component states preserve independent scheduling, but the compressed base plus sparse object updates lose substantial detail. This is evidence, not a pass claim.",
        "",
        "## Conventional AV1 Control",
        "",
        f"- Baseline path: `{Path(audit['baseline']['path']).name}`",
        f"- Baseline bytes: {audit['baseline']['bytes']:,}",
        f"- Baseline SHA256: `{audit['baseline']['sha256']}`",
        f"- Baseline sampled mean SSIM: {audit['baseline_quality']['mean_ssim_960']:.4f}",
        f"- Baseline sampled mean PSNR: {audit['baseline_quality']['mean_psnr_db']:.3f} dB",
        "",
        "## Viewer",
        "",
        "The viewer uses one HTML video element for the side-by-side comparison, so playback, seeking, stepping and speed derive from one clock. Canvas overlays use frame-indexed `tracks_manifest.json`; the difference checkbox switches to a same-clock source/difference encode.",
        "",
        "## Provenance",
        "",
        "No code was copied from the staged third-party repositories into `Main`. Test 02 uses installed package APIs from OpenCV, scikit-image, NumPy, Pillow and FFmpeg.",
    ]
    (outdir / "TEST02_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_docs(root: Path, outdir: Path, baseline: dict[str, Any]) -> None:
    main = root / "Main"
    (main / "README.md").write_text(
        f"""# AMCF Test 02

Run:

```cmd
Main\\RUN_TEST02.cmd
```

The script writes a dated evidence folder under `Tests\\Test 02`, decodes the AMCF archive without rereading source pixels, creates a synchronized browser viewer, and writes `TEST02_REPORT.md`.

Source asset:

`{source_video_path(root)}`

Current evidence folder:

`{outdir}`

Viewer:

```cmd
cd /d "{outdir / 'viewer'}"
"C:\\Users\\fahad\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m http.server 8022
```

Open `http://127.0.0.1:8022/`.
""",
        encoding="utf-8",
    )
    (main / "DEPENDENCIES_AND_PROVENANCE.md").write_text(
        f"""# AMCF Test 02 Dependencies And Provenance

Generated: {datetime.now().isoformat(timespec='seconds')}

## Local application code

All Test 02 application code in `Main` was newly written for this workspace. No files or functions were copied from `Github repos`.

## Runtime dependencies

| Component | Version / source | Licence note | Use |
|---|---|---|---|
| Python | 3.11.4 at `C:\\Users\\fahad\\AppData\\Local\\Programs\\Python\\Python311\\python.exe` | PSF | scripts |
| FFmpeg | local `ffmpeg` on PATH, GPL-enabled build per `ffmpeg -L` | GPLv3+ build notice applies | video/audio decode, encode, mux |
| NumPy | 2.4.6 | BSD-style | arrays |
| Pillow | 12.3.0 | HPND | WebP image IO |
| OpenCV Python | 5.0.0.93 | Apache-2.0 package/source family | masks, contours, optical flow |
| scikit-image | 0.26.0 | BSD-3-Clause + notices | PSNR/SSIM metrics |

## Reference repositories inspected

See `Github repos\\REPOSITORY_MANIFEST.tsv`. OpenCV and scikit-image are used through installed package APIs only. FFmpeg is used as an installed executable. SAM 2, RAFT, PySceneDetect, Cutie, XMem and CoTracker remain research references only; CoTracker is explicitly not copied because its majority licence is CC-BY-NC.

## Media

The source video is `Free Waterfall 4k Videoclip | Nature Videos | Youstock`, URL recorded in the handoff as https://www.youtube.com/watch?v=w6uX9jamcwQ. This test does not grant redistribution rights beyond the local experiment.
""",
        encoding="utf-8",
    )
    (main / "requirements.txt").write_text(
        "numpy==2.4.6\nPillow==12.3.0\nopencv-python==5.0.0.93\nscikit-image==0.26.0\nscipy==1.17.1\nimageio==2.38.0\nnetworkx==3.6.1\ntifffile==2026.3.3\nlazy-loader==0.6\n",
        encoding="utf-8",
    )


def write_hierarchy(root: Path, outdir: Path) -> None:
    wanted_roots = [root / "Main", outdir]
    lines: list[str] = []
    for base in wanted_roots:
        lines.append(str(base))
        for p in sorted(base.rglob("*")):
            if ".git" in p.parts:
                continue
            rel = p.relative_to(base)
            depth = len(rel.parts)
            size = f" ({p.stat().st_size} bytes)" if p.is_file() else ""
            lines.append("  " * depth + rel.name + size)
    (root / f"PROJECT_HIERARCHY_TEST02_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt").write_text("\n".join(lines), encoding="utf-8")


def package_deliverables(root: Path, outdir: Path) -> Path:
    zip_path = root / f"AMCF_Test02_Deliverables_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    include_roots = [root / "Main", outdir]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for base in include_roots:
            for p in base.rglob("*"):
                if not p.is_file() or ".git" in p.parts:
                    continue
                zf.write(p, p.relative_to(root).as_posix())
    return zip_path


def run_pipeline(args: argparse.Namespace) -> None:
    root = root_dir()
    source = source_video_path(root)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = root / "Tests" / "Test 02" / stamp
    ensure_clean_dir(outdir / "visual_comparisons")
    probe = ffprobe_json(source, root)
    (outdir / "source_ffprobe.json").write_text(json.dumps(probe, indent=2), encoding="utf-8")
    result = build_archive_and_tracks(root, outdir, args.frames)
    decode = decode_archive(root, result["archive"], outdir)
    quality = compare_quality(root, source, decode["reconstructed_video"], outdir)
    viewer = make_viewer(root, outdir, source, decode["reconstructed_video"])
    baseline = make_av1_baseline(root, source, outdir)
    baseline_quality = compare_quality(root, source, baseline["path"], outdir / "baseline_quality")
    write_report(root, outdir, {"baseline": baseline, "baseline_quality": baseline_quality})
    write_docs(root, outdir, baseline)
    write_hierarchy(root, outdir)
    zip_path = package_deliverables(root, outdir)
    (outdir / "ARTIFACT_SHA256SUMS.txt").write_text(
        "\n".join(
            f"{sha256_file(p)}  {p.name}"
            for p in [
                result["archive"],
                decode["reconstructed_video"],
                viewer["comparison"],
                viewer["difference"],
                baseline["path"],
                zip_path,
            ]
            if p.exists()
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"outdir": str(outdir), "archive": str(result["archive"]), "zip": str(zip_path)}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", type=int, default=288)
    args = parser.parse_args()
    run_pipeline(args)


if __name__ == "__main__":
    main()
