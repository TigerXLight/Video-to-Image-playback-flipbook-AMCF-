from __future__ import annotations

"""Run the AMCF deep semantic inference bridge against external tool trees.

This module deliberately does not vendor SAM2, CoTracker, checkpoints, or
datasets.  It loads those user-supplied resources at runtime and writes only
bounded inference evidence.  The output is diagnostic input for AMCF event
generation; it is not itself an AMCF archive and does not make a blanket
Level-5 claim.
"""

import argparse
import csv
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row}) if rows else ["empty"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def add_external_repo(repo: Path) -> None:
    repo = repo.resolve()
    if not repo.is_dir():
        raise FileNotFoundError(f"external repository does not exist: {repo}")
    value = str(repo)
    if value not in sys.path:
        sys.path.insert(0, value)


def parse_bbox(value: str | None, width: int, height: int) -> list[float]:
    if value:
        parts = [float(part.strip()) for part in value.split(",")]
        if len(parts) != 4:
            raise ValueError("bbox must contain x0,y0,x1,y1")
        x0, y0, x1, y1 = parts
    else:
        x0, y0 = width * 0.30, height * 0.25
        x1, y1 = width * 0.70, height * 0.75
    x0 = max(0.0, min(float(width - 1), x0))
    y0 = max(0.0, min(float(height - 1), y0))
    x1 = max(x0 + 1.0, min(float(width), x1))
    y1 = max(y0 + 1.0, min(float(height), y1))
    return [x0, y0, x1, y1]


def _read_image_records(input_path: Path, frame_dir: Path, max_frames: int, frame_step: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    import cv2

    if max_frames < 1 or frame_step < 1:
        raise ValueError("max_frames and frame_step must be positive")
    frame_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    source = {"path": str(input_path), "kind": "frames" if input_path.is_dir() else "video_or_image"}

    def save_record(source_index: int, image) -> None:
        if image is None or image.size == 0 or len(records) >= max_frames:
            return
        output_path = frame_dir / f"frame_{source_index:06d}.png"
        if not cv2.imwrite(str(output_path), image):
            raise RuntimeError(f"failed to write sampled frame: {output_path}")
        records.append(
            {
                "frame_order": len(records),
                "source_index": source_index,
                "path": str(output_path),
                "width": int(image.shape[1]),
                "height": int(image.shape[0]),
                "sha256": sha256(output_path),
            }
        )

    if input_path.is_dir():
        paths = sorted(p for p in input_path.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES)
        for source_index, path in enumerate(paths):
            if source_index % frame_step:
                continue
            image = cv2.imread(str(path), cv2.IMREAD_COLOR)
            save_record(source_index, image)
            if len(records) >= max_frames:
                break
        source.update({"input_file_count": len(paths), "selected_count": len(records)})
    elif input_path.is_file() and input_path.suffix.lower() in IMAGE_SUFFIXES:
        save_record(0, cv2.imread(str(input_path), cv2.IMREAD_COLOR))
        source.update({"input_file_count": 1, "selected_count": len(records)})
    elif input_path.is_file():
        capture = cv2.VideoCapture(str(input_path))
        if not capture.isOpened():
            raise RuntimeError(f"OpenCV could not open input video: {input_path}")
        source.update(
            {
                "fps": float(capture.get(cv2.CAP_PROP_FPS) or 0.0),
                "frame_count_hint": int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0),
            }
        )
        source_index = 0
        while len(records) < max_frames:
            ok, image = capture.read()
            if not ok:
                break
            if source_index % frame_step == 0:
                save_record(source_index, image)
            source_index += 1
        capture.release()
        source.update({"decoded_frame_count": source_index, "selected_count": len(records)})
    else:
        raise FileNotFoundError(f"input does not exist: {input_path}")

    if not records:
        raise RuntimeError(f"no readable frames found in {input_path}")
    return records, source


def run_sam2(
    records: list[dict[str, Any]],
    repo: Path,
    checkpoint: Path,
    output: Path,
    bbox_text: str | None,
    device: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    import cv2
    import numpy as np
    import torch

    add_external_repo(repo)
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

    if not checkpoint.is_file():
        raise FileNotFoundError(f"SAM2 checkpoint does not exist: {checkpoint}")
    first = cv2.imread(records[0]["path"], cv2.IMREAD_COLOR)
    if first is None:
        raise RuntimeError("could not read first sampled frame for SAM2 bbox")
    bbox = parse_bbox(bbox_text, first.shape[1], first.shape[0])
    mask_dir = output / "sam2_masks"
    overlay_dir = output / "sam2_overlays"
    mask_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    model = build_sam2("configs/sam2.1/sam2.1_hiera_t.yaml", str(checkpoint), device=device)
    predictor = SAM2ImagePredictor(model)
    rows: list[dict[str, Any]] = []
    started = time.time()
    with torch.inference_mode():
        for record in records:
            image_bgr = cv2.imread(record["path"], cv2.IMREAD_COLOR)
            if image_bgr is None:
                raise RuntimeError(f"could not read sampled frame: {record['path']}")
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            height, width = image_rgb.shape[:2]
            box = np.array(
                [
                    max(0.0, min(width - 1.0, bbox[0])),
                    max(0.0, min(height - 1.0, bbox[1])),
                    max(1.0, min(width, bbox[2])),
                    max(1.0, min(height, bbox[3])),
                ],
                dtype=np.float32,
            )
            predictor.set_image(image_rgb)
            masks, scores, _ = predictor.predict(box=box, multimask_output=True)
            best = int(np.argmax(scores))
            mask = (masks[best].astype(np.uint8) * 255)
            mask_path = mask_dir / f"frame_{record['frame_order']:06d}.png"
            overlay_path = overlay_dir / f"frame_{record['frame_order']:06d}.jpg"
            cv2.imwrite(str(mask_path), mask)
            overlay = image_bgr.copy()
            overlay[mask > 0] = (
                0.45 * overlay[mask > 0] + 0.55 * np.array([0, 255, 0])
            ).astype(np.uint8)
            cv2.rectangle(
                overlay,
                (int(box[0]), int(box[1])),
                (int(box[2]), int(box[3])),
                (0, 128, 255),
                2,
            )
            cv2.putText(
                overlay,
                f"SAM2 frame {record['frame_order']} score={float(scores[best]):.4f}",
                (8, 24),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2,
            )
            cv2.imwrite(str(overlay_path), overlay)
            rows.append(
                {
                    **record,
                    "bbox": bbox,
                    "sam2_score": float(scores[best]),
                    "mask_area": int((mask > 0).sum()),
                    "mask_path": str(mask_path),
                    "overlay_path": str(overlay_path),
                    "mask_sha256": sha256(mask_path),
                }
            )
    del predictor, model
    return (
        {
            "status": "passed",
            "tool": "sam2",
            "repo": str(repo),
            "checkpoint": str(checkpoint),
            "device": device,
            "frames_processed": len(rows),
            "bbox": bbox,
            "elapsed_seconds": round(time.time() - started, 3),
        },
        rows,
    )


def run_cotracker(
    records: list[dict[str, Any]],
    repo: Path,
    checkpoint: Path,
    output: Path,
    grid_size: int,
    device: str,
    sam2_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    import cv2
    import numpy as np
    import torch

    add_external_repo(repo)
    from cotracker.predictor import CoTrackerPredictor

    if not checkpoint.is_file():
        raise FileNotFoundError(f"CoTracker checkpoint does not exist: {checkpoint}")
    if grid_size < 1:
        raise ValueError("grid_size must be positive")
    images = []
    first = cv2.imread(records[0]["path"], cv2.IMREAD_COLOR)
    if first is None:
        raise RuntimeError("could not read first sampled frame for CoTracker")
    original_height, original_width = first.shape[:2]
    track_width = 160
    track_height = max(2, int(round(original_height * track_width / original_width)))
    for record in records:
        image = cv2.imread(record["path"], cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError(f"could not read sampled frame: {record['path']}")
        image = cv2.resize(image, (track_width, track_height), interpolation=cv2.INTER_AREA)
        images.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    video = torch.from_numpy(np.stack(images)).permute(0, 3, 1, 2)[None].float().to(device)
    started = time.time()
    model = CoTrackerPredictor(checkpoint=str(checkpoint), offline=True, window_len=60).to(device).eval()
    with torch.inference_mode():
        tracks, visibility = model(video, grid_size=grid_size)
    tracks_np = tracks.detach().cpu().numpy()
    visibility_np = visibility.detach().cpu().numpy().astype("float32")
    track_path = output / "cotracker_tracks.npz"
    np.savez_compressed(track_path, tracks=tracks_np, visibility=visibility_np)

    cotracker_overlay_dir = output / "cotracker_overlays"
    diagnostic_overlay_dir = output / "diagnostic_overlays"
    cotracker_overlay_dir.mkdir(parents=True, exist_ok=True)
    diagnostic_overlay_dir.mkdir(parents=True, exist_ok=True)
    sam2_by_order = {int(row["frame_order"]): row for row in sam2_rows}
    track_rows: list[dict[str, Any]] = []
    for frame_order, record in enumerate(records):
        image = cv2.imread(record["path"], cv2.IMREAD_COLOR)
        cotracker_image = image.copy()
        diagnostic_image = image.copy()
        sam2_row = sam2_by_order.get(frame_order)
        if sam2_row and Path(sam2_row["mask_path"]).exists():
            mask = cv2.imread(sam2_row["mask_path"], cv2.IMREAD_GRAYSCALE)
            if mask is not None:
                diagnostic_image[mask > 0] = (
                    0.45 * diagnostic_image[mask > 0] + 0.55 * np.array([0, 255, 0])
                ).astype(np.uint8)
        points = tracks_np[0, frame_order]
        visible = visibility_np[0, frame_order] > 0.5
        scale_x = image.shape[1] / float(track_width)
        scale_y = image.shape[0] / float(track_height)
        for point, is_visible in zip(points, visible):
            x = int(round(float(point[0]) * scale_x))
            y = int(round(float(point[1]) * scale_y))
            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                color = (0, 255, 0) if is_visible else (0, 0, 255)
                cv2.circle(cotracker_image, (x, y), 2, color, -1)
                cv2.circle(diagnostic_image, (x, y), 2, color, -1)
        cotracker_overlay_path = cotracker_overlay_dir / f"frame_{frame_order:06d}.jpg"
        diagnostic_overlay_path = diagnostic_overlay_dir / f"frame_{frame_order:06d}.jpg"
        cv2.putText(
            cotracker_image,
            f"CoTracker frame {frame_order} visible={int(visible.sum())}/{len(visible)}",
            (8, cotracker_image.shape[0] - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            diagnostic_image,
            f"AMCF diagnostic frame {frame_order} visible={int(visible.sum())}/{len(visible)}",
            (8, diagnostic_image.shape[0] - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
        )
        cv2.imwrite(str(cotracker_overlay_path), cotracker_image)
        cv2.imwrite(str(diagnostic_overlay_path), diagnostic_image)
        track_rows.append(
            {
                "frame_order": frame_order,
                "source_index": record["source_index"],
                "track_count": int(len(points)),
                "visible_track_count": int(visible.sum()),
                "mean_x": float(points[:, 0].mean()),
                "mean_y": float(points[:, 1].mean()),
                "cotracker_overlay_path": str(cotracker_overlay_path),
                "diagnostic_overlay_path": str(diagnostic_overlay_path),
            }
        )
    del model, video
    return {
        "status": "passed",
        "tool": "cotracker",
        "repo": str(repo),
        "checkpoint": str(checkpoint),
        "device": device,
        "frames_processed": len(records),
        "grid_size": grid_size,
        "track_shape": list(tracks_np.shape),
        "visibility_shape": list(visibility_np.shape),
        "mean_visibility": float(visibility_np.mean()),
        "tracks_path": str(track_path),
        "tracks_sha256": sha256(track_path),
        "track_rows": track_rows,
        "elapsed_seconds": round(time.time() - started, 3),
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.time()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    input_path = Path(args.input).resolve()
    frame_records, source = _read_image_records(
        input_path,
        output / "sampled_frames",
        args.max_frames,
        args.frame_step,
    )
    first = frame_records[0]
    bbox = parse_bbox(args.bbox, int(first["width"]), int(first["height"]))
    sam2_result: dict[str, Any]
    sam2_rows: list[dict[str, Any]] = []
    if args.skip_sam2:
        sam2_result = {"status": "skipped", "tool": "sam2"}
    else:
        try:
            sam2_result, sam2_rows = run_sam2(
                frame_records,
                Path(args.sam2_repo).resolve(),
                Path(args.sam2_checkpoint).resolve(),
                output,
                ",".join(str(value) for value in bbox),
                args.device,
            )
        except Exception as exc:
            sam2_result = {"status": "failed", "tool": "sam2", "error": repr(exc)}
    if args.skip_cotracker:
        cotracker_result = {"status": "skipped", "tool": "cotracker"}
    else:
        try:
            cotracker_result = run_cotracker(
                frame_records,
                Path(args.cotracker_repo).resolve(),
                Path(args.cotracker_checkpoint).resolve(),
                output,
                args.grid_size,
                args.device,
                sam2_rows,
            )
        except Exception as exc:
            cotracker_result = {"status": "failed", "tool": "cotracker", "error": repr(exc)}

    event_rows = [
        {
            "event_id": f"deep_semantic_frame_{row['frame_order']:06d}",
            "frame_order": row["frame_order"],
            "source_index": row["source_index"],
            "component_id": "deep_semantic_prompted_object",
            "sam2_status": sam2_result["status"],
            "cotracker_status": cotracker_result["status"],
        }
        for row in frame_records
    ]
    manifest = {
        "schema": "amcf_deep_semantic_inference_v1",
        "status": "passed" if sam2_result["status"] == "passed" and cotracker_result["status"] in {"passed", "skipped"} else "failed",
        "source": source,
        "source_video_embedded": False,
        "source_video_required_for_diagnostic_output": False,
        "source_video_used_for_inference": True,
        "complete_video_fallback": False,
        "semantic_level5_claimed": False,
        "main_modified": False,
        "prior_runs_modified": False,
        "license_boundary": {
            "sam2": "External SAM2/SAMURAI repository and checkpoint; retain upstream licence notices.",
            "cotracker": "External CoTracker repository and checkpoint; retain its non-commercial/research licence boundary.",
        },
        "input_frame_count": len(frame_records),
        "bbox": bbox,
        "sam2": sam2_result,
        "cotracker": cotracker_result,
        "events": event_rows,
        "elapsed_seconds": round(time.time() - started, 3),
    }
    write_json(output / "deep_inference_manifest.json", manifest)
    write_csv(output / "deep_inference_events.csv", event_rows)
    write_json(output / "sam2_results.json", {"summary": sam2_result, "frames": sam2_rows})
    write_json(output / "cotracker_results.json", cotracker_result)
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run AMCF external deep semantic inference adapters.")
    parser.add_argument("--input", required=True, help="Input video, image, or directory of frames.")
    parser.add_argument("--output", required=True, help="Output directory for bounded inference evidence.")
    parser.add_argument("--sam2-repo", required=True)
    parser.add_argument("--sam2-checkpoint", required=True)
    parser.add_argument("--cotracker-repo", required=True)
    parser.add_argument("--cotracker-checkpoint", required=True)
    parser.add_argument("--bbox", help="SAM2 box prompt as x0,y0,x1,y1; defaults to a central box.")
    parser.add_argument("--max-frames", type=int, default=8)
    parser.add_argument("--frame-step", type=int, default=1)
    parser.add_argument("--grid-size", type=int, default=4)
    parser.add_argument("--device", default="cpu", choices=("cpu", "cuda"))
    parser.add_argument("--skip-sam2", action="store_true")
    parser.add_argument("--skip-cotracker", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run(args)
    except Exception as exc:
        result = {"status": "failed", "error": repr(exc), "main_modified": False}
        if args.output:
            output = Path(args.output).resolve()
            output.mkdir(parents=True, exist_ok=True)
            write_json(output / "deep_inference_manifest.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
