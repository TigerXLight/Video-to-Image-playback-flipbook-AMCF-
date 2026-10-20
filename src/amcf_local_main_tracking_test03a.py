from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def workspace_root() -> Path:
    env_root = os.environ.get("AMCF_WORKSPACE_ROOT")
    if env_root:
        return Path(env_root).resolve()
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "Test media").exists():
            return parent
    return current.parents[1]


WORKSPACE = workspace_root()
SOURCE_VIDEO = WORKSPACE / "Test media" / "Waterfall" / "Original" / "Free Waterfall 4k Videoclip ¦ Nature Videos ¦ Youstock (1920p_24fps_AV1-128kbit_AAC).mp4"
TEST_ROOT = WORKSPACE / "Tests" / "Test 03A"
EXPECTED_SOURCE = {
    "bytes": 11661942,
    "sha256": "4C44C01E3A82D6246794676B81B31D25EE2E2150B9DD162FFB7AD9642ADAC81D",
    "width": 3840,
    "height": 1920,
    "fps": "24000/1001",
    "frames": 288,
}


@dataclass(frozen=True)
class Seed:
    track_id: str
    target_name: str
    color_bgr: tuple[int, int, int]
    polygon: list[tuple[int, int]]
    notes: str


SEEDS = [
    Seed(
        "WATERFALL_COLUMN",
        "Waterfall column",
        (255, 215, 80),
        [(1340, 430), (1680, 410), (1860, 1885), (1180, 1890), (1230, 860)],
        "manual seed polygon around visible falling water column",
    ),
    Seed(
        "WATER_IMPACT_FOAM",
        "Waterfall impact foam",
        (255, 255, 255),
        [(1080, 1390), (2350, 1350), (2390, 1890), (930, 1890)],
        "manual seed polygon around bright impact foam and turbulent pool",
    ),
    Seed(
        "MIST_SPRAY",
        "Mist/spray region",
        (210, 210, 255),
        [(900, 520), (1460, 420), (2360, 1180), (2120, 1850), (980, 1770), (760, 960)],
        "manual seed polygon around visible spray haze outside main water column",
    ),
    Seed(
        "FOREGROUND_TREE_LEFT",
        "Left tree/trunk and foliage",
        (40, 180, 40),
        [(0, 0), (570, 0), (650, 860), (510, 1550), (0, 1900)],
        "manual seed polygon around left tree/foliage mass",
    ),
    Seed(
        "BRANCH_LEAF_GROUP_LEFT",
        "Left branch/leaf group",
        (40, 255, 100),
        [(0, 640), (860, 600), (910, 1320), (0, 1380)],
        "manual seed polygon around resolvable left branch/leaf group",
    ),
    Seed(
        "BRANCH_LEAF_GROUP_RIGHT",
        "Right branch/leaf group",
        (60, 220, 220),
        [(2760, 620), (3680, 650), (3670, 1440), (2760, 1360)],
        "manual seed polygon around resolvable right branch/leaf group",
    ),
]


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=WORKSPACE, text=True, capture_output=True, check=False)
        return proc.returncode, (proc.stdout + proc.stderr).strip()
    except FileNotFoundError as exc:
        return 127, str(exc)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def source_probe() -> dict[str, Any]:
    info: dict[str, Any] = {
        "path": str(SOURCE_VIDEO),
        "exists": SOURCE_VIDEO.exists(),
    }
    if SOURCE_VIDEO.exists():
        info["bytes"] = SOURCE_VIDEO.stat().st_size
        info["sha256"] = sha256(SOURCE_VIDEO)
        code, out = run([
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,avg_frame_rate,r_frame_rate,nb_frames,duration,codec_name",
            "-of",
            "json",
            str(SOURCE_VIDEO),
        ])
        info["ffprobe_returncode"] = code
        info["ffprobe"] = out
        try:
            parsed = json.loads(out)
            stream = parsed["streams"][0]
            info["width"] = int(stream["width"])
            info["height"] = int(stream["height"])
            info["fps"] = stream.get("avg_frame_rate")
            info["frames"] = int(stream.get("nb_frames", "0"))
            info["codec"] = stream.get("codec_name")
        except Exception as exc:
            info["ffprobe_parse_error"] = repr(exc)
    return info


def source_ok(info: dict[str, Any]) -> bool:
    return (
        info.get("exists")
        and info.get("bytes") == EXPECTED_SOURCE["bytes"]
        and info.get("sha256") == EXPECTED_SOURCE["sha256"]
        and info.get("width") == EXPECTED_SOURCE["width"]
        and info.get("height") == EXPECTED_SOURCE["height"]
        and info.get("fps") == EXPECTED_SOURCE["fps"]
        and info.get("frames") == EXPECTED_SOURCE["frames"]
    )


def environment_report() -> dict[str, Any]:
    py_info = {
        "executable": sys.executable,
        "version": sys.version,
        "platform": platform.platform(),
    }
    packages: dict[str, Any] = {}
    for name in ["numpy", "PIL", "cv2", "skimage"]:
        try:
            mod = __import__(name)
            packages[name] = {"available": True, "version": getattr(mod, "__version__", "unknown")}
        except Exception as exc:
            packages[name] = {"available": False, "error": repr(exc)}
    ffmpeg_code, ffmpeg_out = run(["ffmpeg", "-version"])
    ffprobe_code, ffprobe_out = run(["ffprobe", "-version"])
    nvidia_code, nvidia_out = run(["nvidia-smi"])
    return {
        "python": py_info,
        "packages": packages,
        "ffmpeg": {"returncode": ffmpeg_code, "first_line": ffmpeg_out.splitlines()[0] if ffmpeg_out else ""},
        "ffprobe": {"returncode": ffprobe_code, "first_line": ffprobe_out.splitlines()[0] if ffprobe_out else ""},
        "nvidia_smi": {"returncode": nvidia_code, "output": nvidia_out},
        "large_ml_dependencies_installed_by_test03a": False,
        "cotracker_used": False,
    }


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_failure_outputs(out_dir: Path, reason: str, env: dict[str, Any], src: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "environment_report.json", env)
    write_json(out_dir / "tracking_manifest.json", {
        "test": "AMCF Test 03A",
        "verdict": "FAIL",
        "failure_stage": "dependency/source gate",
        "reason": reason,
        "source": src,
        "tracks": [],
        "static_rectangles_used_as_masks": False,
        "archive_or_reconstruction_built": False,
    })
    with (out_dir / "tracking_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "track_id",
            "target_name",
            "frame_index",
            "timestamp_seconds",
            "state",
            "confidence",
            "flow_median_px_s",
            "flow_p95_px_s",
            "point_survival",
            "method",
            "notes",
        ])
    (out_dir / "PROVENANCE.md").write_text(
        "# AMCF Test 03A Provenance\n\n"
        "- No upstream source code was copied or adapted into AMCF for this run.\n"
        "- OpenCV/scikit-image were attempted as light CPU dependencies only.\n"
        "- CoTracker was not used.\n"
        "- SAM2, Cutie, XMem, RAFT, PyTorch, CUDA packages and model checkpoints were not installed or used.\n"
        "- No AMCF archive or reconstruction was built.\n",
        encoding="utf-8",
    )
    (out_dir / "TEST03A_TRACKING_REPORT.md").write_text(
        "# AMCF Test 03A Tracking Report\n\n"
        f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
        "## Verdict\n\n"
        "FAIL.\n\n"
        f"{reason}\n\n"
        "This is a tracking-only result. No archive, reconstruction, viewer polish, or compression claim was produced.\n\n"
        "## Source Verification\n\n"
        f"- Path: `{src.get('path')}`\n"
        f"- Exists: {src.get('exists')}\n"
        f"- Bytes: {src.get('bytes')}\n"
        f"- SHA256: `{src.get('sha256')}`\n"
        f"- Resolution: {src.get('width')}x{src.get('height')}\n"
        f"- FPS: {src.get('fps')}\n"
        f"- Frames: {src.get('frames')}\n"
        f"- Matches expected source: {source_ok(src)}\n\n"
        "## Dependency Gate\n\n"
        f"- Python: `{env['python']['executable']}`\n"
        f"- Python version: `{env['python']['version'].splitlines()[0]}`\n"
        f"- NumPy: {env['packages'].get('numpy')}\n"
        f"- Pillow: {env['packages'].get('PIL')}\n"
        f"- OpenCV: {env['packages'].get('cv2')}\n"
        f"- scikit-image: {env['packages'].get('skimage')}\n"
        f"- FFmpeg: {env['ffmpeg'].get('first_line')}\n"
        f"- NVIDIA/CUDA probe: {env['nvidia_smi'].get('output')}\n\n"
        "## Required Tracking Evidence\n\n"
        "Not produced. The OpenCV tracking baseline could not run without `cv2`.\n\n"
        "## PASS/FAIL Gate\n\n"
        "FAIL because tracking-only outputs with object-bound moving masks/contours were not generated. "
        "No static rectangles were substituted and no previous masks were silently reused as visible tracking.\n",
        encoding="utf-8",
    )


def zip_outputs(out_dir: Path) -> Path:
    zip_path = out_dir.with_name(out_dir.name + "_EVIDENCE.zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in out_dir.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(out_dir.parent))
    return zip_path


def write_hierarchy(root: Path, out_path: Path) -> None:
    lines: list[str] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part.startswith(".venv-test03a") for part in rel.parts):
            continue
        prefix = "[D]" if path.is_dir() else "[F]"
        size = "" if path.is_dir() else f" {path.stat().st_size} bytes"
        lines.append(f"{prefix} {rel}{size}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_tracking(out_dir: Path, env: dict[str, Any], src: dict[str, Any]) -> str:
    import cv2
    import numpy as np

    out_dir.mkdir(parents=True, exist_ok=True)
    masks_dir = out_dir / "mask_debug"
    contours_dir = out_dir / "contour_debug"
    stills_dir = out_dir / "stills"
    masks_dir.mkdir(exist_ok=True)
    contours_dir.mkdir(exist_ok=True)
    stills_dir.mkdir(exist_ok=True)

    cap = cv2.VideoCapture(str(SOURCE_VIDEO))
    if not cap.isOpened():
        raise RuntimeError("OpenCV could not open the source video")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24000 / 1001
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or EXPECTED_SOURCE["frames"]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    overlay_path = out_dir / "tracking_overlay.mp4"
    writer = cv2.VideoWriter(str(overlay_path), fourcc, fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError("OpenCV could not open tracking_overlay.mp4 writer")

    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("Could not read first video frame")

    masks: dict[str, Any] = {}
    for seed in SEEDS:
        mask = np.zeros((height, width), np.uint8)
        pts = np.array(seed.polygon, np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(mask, [pts], 255)
        masks[seed.track_id] = mask

    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    records: list[dict[str, Any]] = []
    metrics_rows: list[dict[str, Any]] = []
    contour_debug: dict[str, list[dict[str, Any]]] = {seed.track_id: [] for seed in SEEDS}
    sample_frames = {1, 48, 144, 216, 288}
    held_counts = {seed.track_id: 0 for seed in SEEDS}
    lost_counts = {seed.track_id: 0 for seed in SEEDS}

    for frame_no in range(1, total + 1):
        if frame_no > 1:
            ok, frame = cap.read()
            if not ok:
                break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame_no == 1:
            flow = np.zeros((height, width, 2), np.float32)
        else:
            small_prev = cv2.resize(prev_gray, (width // 2, height // 2), interpolation=cv2.INTER_AREA)
            small_gray = cv2.resize(gray, (width // 2, height // 2), interpolation=cv2.INTER_AREA)
            small_flow = cv2.calcOpticalFlowFarneback(small_prev, small_gray, None, 0.5, 3, 21, 3, 5, 1.2, 0)
            flow = cv2.resize(small_flow, (width, height), interpolation=cv2.INTER_LINEAR) * 2.0

        overlay = frame.copy()
        frame_tracks: list[dict[str, Any]] = []
        for seed in SEEDS:
            prev_mask = masks[seed.track_id]
            yy, xx = np.indices(prev_mask.shape, dtype=np.float32)
            map_x = xx - flow[:, :, 0]
            map_y = yy - flow[:, :, 1]
            warped = cv2.remap(prev_mask, map_x, map_y, cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
            kernel = np.ones((7, 7), np.uint8)
            updated = cv2.morphologyEx(warped, cv2.MORPH_CLOSE, kernel)
            updated = cv2.morphologyEx(updated, cv2.MORPH_OPEN, kernel)
            area = int(np.count_nonzero(updated))
            state = "visible"
            method = "manual seed" if frame_no == 1 else "propagated"
            confidence = 0.9 if frame_no == 1 else 0.65
            if area < max(1000, int(np.count_nonzero(prev_mask) * 0.2)):
                held_counts[seed.track_id] += 1
                updated = prev_mask.copy()
                area = int(np.count_nonzero(updated))
                state = "held"
                method = "held"
                confidence = 0.25
                if held_counts[seed.track_id] >= 3:
                    state = "lost"
                    lost_counts[seed.track_id] += 1
                    confidence = 0.0
            else:
                held_counts[seed.track_id] = 0
            masks[seed.track_id] = updated

            contours, _ = cv2.findContours(updated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = [c for c in contours if cv2.contourArea(c) > 128]
            serialized_contours: list[list[list[int]]] = []
            if contours:
                joined = np.vstack(contours)
                x, y, w, h = cv2.boundingRect(joined)
                m = cv2.moments(updated)
                cx = float(m["m10"] / m["m00"]) if m["m00"] else float(x + w / 2)
                cy = float(m["m01"] / m["m00"]) if m["m00"] else float(y + h / 2)
                cv2.drawContours(overlay, contours, -1, seed.color_bgr, 3)
                for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:5]:
                    epsilon = max(2.0, 0.0025 * cv2.arcLength(contour, True))
                    approx = cv2.approxPolyDP(contour, epsilon, True).reshape(-1, 2)
                    serialized_contours.append([[int(px), int(py)] for px, py in approx])
            else:
                x = y = w = h = 0
                cx = cy = 0.0
            inside = updated > 0
            mag_px_s = np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2) * fps
            vals = mag_px_s[inside]
            med = float(np.median(vals)) if vals.size else 0.0
            p95 = float(np.percentile(vals, 95)) if vals.size else 0.0
            label = f"{seed.track_id} {state} conf={confidence:.2f} med={med:.1f}px/s"
            lx = int(min(max(cx + 12, 0), width - 900))
            ly = int(min(max(cy, 24), height - 24))
            cv2.putText(overlay, label, (lx, ly), cv2.FONT_HERSHEY_SIMPLEX, 0.85, seed.color_bgr, 2, cv2.LINE_AA)
            track_record = {
                "track_id": seed.track_id,
                "target_name": seed.target_name,
                "frame_index": frame_no,
                "timestamp_seconds": (frame_no - 1) / fps,
                "state": state,
                "confidence": confidence,
                "centroid": [cx, cy],
                "bbox": [int(x), int(y), int(w), int(h)],
                "area": area,
                "contours": serialized_contours,
                "flow_median_px_s": med,
                "flow_p95_px_s": p95,
                "point_track_survival": None,
                "method": method,
                "notes": seed.notes if frame_no == 1 else "mask propagated by dense optical flow; failure marked held/lost",
            }
            frame_tracks.append(track_record)
            metrics_rows.append(track_record)
            contour_debug[seed.track_id].append(
                {
                    "frame_index": frame_no,
                    "timestamp_seconds": track_record["timestamp_seconds"],
                    "state": state,
                    "confidence": confidence,
                    "area": area,
                    "bbox": track_record["bbox"],
                    "centroid": track_record["centroid"],
                    "contours": serialized_contours,
                    "method": method,
                }
            )
        writer.write(overlay)
        records.append({"frame_index": frame_no, "tracks": frame_tracks})
        if frame_no in sample_frames:
            cv2.imwrite(str(stills_dir / f"frame_{frame_no:03d}.jpg"), overlay)
            for seed in SEEDS:
                cv2.imwrite(str(masks_dir / f"{seed.track_id}_frame_{frame_no:03d}.png"), masks[seed.track_id])
        prev_gray = gray

    cap.release()
    writer.release()
    for track_id, entries in contour_debug.items():
        write_json(contours_dir / f"{track_id}_contours.json", entries)
    manifest = {
        "test": "AMCF Test 03A",
        "verdict": "FAIL",
        "reason": "OpenCV CPU baseline ran, but this seed-and-flow propagation is diagnostic and was not manually reviewed as passing object-bound tracking.",
        "source": src,
        "fps": fps,
        "frames_processed": len(records),
        "tracks": records,
        "static_rectangles_used_as_masks": False,
        "archive_or_reconstruction_built": False,
    }
    write_json(out_dir / "tracking_manifest.json", manifest)
    with (out_dir / "tracking_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        fields = [
            "track_id",
            "target_name",
            "frame_index",
            "timestamp_seconds",
            "state",
            "confidence",
            "centroid",
            "bbox",
            "area",
            "flow_median_px_s",
            "flow_p95_px_s",
            "point_track_survival",
            "method",
            "notes",
        ]
        writer_csv = csv.DictWriter(f, fieldnames=fields)
        writer_csv.writeheader()
        for row in metrics_rows:
            writer_csv.writerow({k: row.get(k) for k in fields})
    write_json(out_dir / "environment_report.json", env)
    state_counts: dict[str, dict[str, int]] = {seed.track_id: {} for seed in SEEDS}
    mean_flow: dict[str, dict[str, float]] = {}
    for seed in SEEDS:
        rows = [row for row in metrics_rows if row["track_id"] == seed.track_id]
        for row in rows:
            state_counts[seed.track_id][row["state"]] = state_counts[seed.track_id].get(row["state"], 0) + 1
        med_values = [float(row["flow_median_px_s"]) for row in rows]
        p95_values = [float(row["flow_p95_px_s"]) for row in rows]
        mean_flow[seed.track_id] = {
            "mean_median_px_s": float(np.mean(med_values)) if med_values else 0.0,
            "mean_p95_px_s": float(np.mean(p95_values)) if p95_values else 0.0,
        }
    write_json(out_dir / "tracking_summary.json", {"state_counts": state_counts, "mean_flow": mean_flow})
    (out_dir / "DEPENDENCY_REPORT.md").write_text(
        "# AMCF Test 03A Dependency Report\n\n"
        "## Runtime Used\n\n"
        f"- Python executable: `{env['python']['executable']}`\n"
        f"- Python version: `{env['python']['version'].splitlines()[0]}`\n"
        f"- NumPy: `{env['packages'].get('numpy')}`\n"
        f"- Pillow: `{env['packages'].get('PIL')}`\n"
        f"- OpenCV: `{env['packages'].get('cv2')}`\n"
        f"- scikit-image: `{env['packages'].get('skimage')}`\n"
        f"- FFmpeg: `{env['ffmpeg'].get('first_line')}`\n"
        f"- FFprobe: `{env['ffprobe'].get('first_line')}`\n\n"
        "## Dependency Scope\n\n"
        "- Used OpenCV/NumPy/Pillow/scikit-image from the approved light CPU stack.\n"
        "- Did not use a venv for this run; used the verified global Python 3.11 route.\n"
        "- Did not install or use PyTorch, SAM2, Cutie, XMem, CoTracker, RAFT, CUDA packages, or checkpoints.\n",
        encoding="utf-8",
    )
    (out_dir / "PROVENANCE.md").write_text(
        "# AMCF Test 03A Provenance\n\n"
        "- OpenCV Python API was used as a light CPU dependency.\n"
        "- No upstream source code was copied or adapted into AMCF.\n"
        "- CoTracker was not used.\n"
        "- SAM2, Cutie, XMem, RAFT, PyTorch, CUDA packages and model checkpoints were not installed or used.\n"
        "- No AMCF archive or reconstruction was built.\n",
        encoding="utf-8",
    )
    (out_dir / "TEST03A_TRACKING_REPORT.md").write_text(
        "# AMCF Test 03A Tracking Report\n\n"
        f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
        "## Verdict\n\n"
        "FAIL.\n\n"
        "The OpenCV CPU baseline produced diagnostic tracking artifacts, but this run does not claim PASS without human review of object-bound contour fidelity. "
        "No archive or reconstruction work was performed.\n\n"
        "## Summary Metrics\n\n"
        f"- Frames processed: {len(records)}\n"
        f"- Targets seeded: {len(SEEDS)}\n"
        f"- Tracking overlay: `{overlay_path.name}`\n"
        f"- State counts: `{state_counts}`\n"
        f"- Mean flow summary: `{mean_flow}`\n"
        "- Static rectangles used as object masks: False\n"
        "- Fake object FPS reported: False\n"
        "- CoTracker used: False\n"
        "- ML dependencies installed: False\n",
        encoding="utf-8",
    )
    return "FAIL"


def main() -> int:
    timestamp = os.environ.get("AMCF_TEST03A_TIMESTAMP") or datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = TEST_ROOT / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)
    env = environment_report()
    src = source_probe()
    if not source_ok(src):
        reason = "Source verification failed; tracking was not run."
        write_failure_outputs(out_dir, reason, env, src)
        write_hierarchy(WORKSPACE, out_dir / "PROJECT_HIERARCHY_03A.txt")
        zip_path = zip_outputs(out_dir)
        print(f"FAIL\noutput_folder={out_dir}\nzip={zip_path}\nreason={reason}")
        return 2
    if not env["packages"]["cv2"]["available"]:
        reason = "OpenCV (`cv2`) is not importable in the active Python environment; tracking was not run."
        write_failure_outputs(out_dir, reason, env, src)
        write_hierarchy(WORKSPACE, out_dir / "PROJECT_HIERARCHY_03A.txt")
        zip_path = zip_outputs(out_dir)
        print(f"FAIL\noutput_folder={out_dir}\nzip={zip_path}\nreason={reason}")
        return 2
    verdict = run_tracking(out_dir, env, src)
    write_hierarchy(WORKSPACE, out_dir / "PROJECT_HIERARCHY_03A.txt")
    zip_path = zip_outputs(out_dir)
    print(f"{verdict}\noutput_folder={out_dir}\nzip={zip_path}")
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
