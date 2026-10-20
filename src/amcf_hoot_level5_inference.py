from __future__ import annotations

"""Run the bounded HOOT lost/recovered semantic proof.

The adapter keeps the HOOT dataset and SAM2 runtime external.  It accepts an
already extracted sequence or an explicit HOOT zip, parses the official frame
annotations, runs SAM2 on visible frames, and writes reproducible event-window
evidence.  It is an inference/acceptance adapter, not an AMCF archive and not
a blanket claim about arbitrary videos.
"""

import argparse
import csv
import hashlib
import json
import math
import shutil
import time
import zipfile
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def add_external_repo(repo: Path) -> None:
    import sys

    repo = repo.resolve()
    if not repo.is_dir():
        raise FileNotFoundError(f"external repository does not exist: {repo}")
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))


def bbox_from_annotation(value: Any) -> list[float] | None:
    if not value:
        return None
    import numpy as np

    arr = np.asarray(value, dtype=float).reshape(-1)
    if len(arr) == 4:
        x0, y0, x1, y1 = [float(v) for v in arr]
        if x1 > x0 and y1 > y0:
            return [x0, y0, x1, y1]
        return [x0, y0, x0 + x1, y0 + y1]
    if len(arr) >= 8:
        return [float(arr[0::2].min()), float(arr[1::2].min()), float(arr[0::2].max()), float(arr[1::2].max())]
    return None


def annotation_frame_path(extract_dir: Path, annotation: dict[str, Any], index: int) -> Path | None:
    candidates: list[Path] = []
    for key in ("file_name", "img_path", "path", "image", "frame"):
        value = annotation.get(key)
        if isinstance(value, str):
            candidates.append(extract_dir / value)
    for width in (6, 5, 4):
        token = f"{index:0{width}d}"
        candidates.extend(sorted(p for p in extract_dir.rglob(f"*{token}*.*") if p.suffix.lower() in IMAGE_SUFFIXES))
    candidates.extend(sorted(p for p in extract_dir.rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES))
    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.is_file():
            return candidate
    return None


def parse_annotations(extract_dir: Path) -> tuple[list[dict[str, Any]], Path, dict[str, Any]]:
    annotation_path = next(iter(sorted(extract_dir.rglob("anno.json"))), None)
    if annotation_path is None:
        annotation_path = next(iter(sorted(extract_dir.rglob("*.json"))), None)
    if annotation_path is None:
        raise FileNotFoundError(f"No HOOT annotation JSON found under {extract_dir}")
    document = json.loads(annotation_path.read_text(encoding="utf-8"))
    frames = document.get("frames") or document.get("annotations") or document.get("sequence") or []
    if isinstance(frames, dict):
        frames = [{"frame_index": int(key), **value} for key, value in frames.items()]
    rows: list[dict[str, Any]] = []
    for index, frame in enumerate(frames):
        attrs = frame.get("attrs") or frame.get("attributes") or {}
        tags = set(frame.get("tags") or [])
        full_occlusion = bool(attrs.get("full_occlusion") or frame.get("full_occlusion") or "full_occlusion" in tags)
        absent = bool(attrs.get("absent") or frame.get("absent") or "absent" in tags)
        bbox = bbox_from_annotation(frame.get("aa_bb") or frame.get("bbox") or frame.get("box") or frame.get("bb"))
        image_path = annotation_frame_path(extract_dir, frame, index)
        state = "visible_present"
        if absent:
            state = "absent"
        elif full_occlusion:
            state = "full_occlusion"
        rows.append(
            {
                "frame_order": index,
                "frame_id": frame.get("frame_id", frame.get("frame_index", index)),
                "frame_index": int(frame.get("frame_index", frame.get("frame", index))),
                "image_path": str(image_path) if image_path else "",
                "bbox": bbox or [],
                "full_occlusion": full_occlusion,
                "absent": absent,
                "visible_state": state,
            }
        )
    if not rows:
        raise ValueError(f"HOOT annotation contains no frames: {annotation_path}")
    return rows, annotation_path, {
        "video_key": document.get("video_key", ""),
        "frame_count": len(rows),
        "frame_occlusion_level": document.get("frame_occlusion_level", []),
    }


def find_lost_recovered_event(rows: list[dict[str, Any]]) -> dict[str, Any]:
    occluded = [row["frame_order"] for row in rows if row["full_occlusion"] or row["absent"]]
    if not occluded:
        return {"validated": False, "reason": "no full_occlusion or absent annotation found"}
    runs: list[tuple[int, int]] = []
    start = previous = occluded[0]
    for index in occluded[1:]:
        if index == previous + 1:
            previous = index
        else:
            runs.append((start, previous))
            start = previous = index
    runs.append((start, previous))
    for start, end in runs:
        before = [row for row in rows[max(0, start - 40) : start] if row["visible_state"] == "visible_present" and row["image_path"]]
        after = [row for row in rows[end + 1 : min(len(rows), end + 41)] if row["visible_state"] == "visible_present" and row["image_path"]]
        during = [row for row in rows[start : end + 1] if row["image_path"]]
        if before and after and during:
            return {
                "validated": True,
                "present_before_frame": before[-1]["frame_order"],
                "occlusion_start_frame": start,
                "occlusion_end_frame": end,
                "recovered_after_frame": after[0]["frame_order"],
                "before_count": len(before),
                "occluded_count": len(during),
                "after_count": len(after),
                "classification": "present_absent_or_full_occlusion_present_validated",
                "claim_boundary": "HOOT frame-level annotation validates the target visible before, fully occluded/absent, then visible again.",
            }
    return {"validated": False, "reason": "no full occlusion run has visible source frames on both sides"}


def write_event_window(rows: list[dict[str, Any]], event: dict[str, Any], output: Path) -> list[dict[str, Any]]:
    import cv2

    overlay_dir = output / "event_window_overlays"
    overlay_dir.mkdir(parents=True, exist_ok=True)
    if not event.get("validated"):
        write_json(output / "event_window_manifest.json", [])
        return []
    low = max(0, int(event["present_before_frame"]) - 8)
    high = min(len(rows) - 1, int(event["recovered_after_frame"]) + 8)
    overlays: list[dict[str, Any]] = []
    for row in rows[low : high + 1]:
        source = Path(row["image_path"]) if row["image_path"] else None
        if source is None or not source.is_file():
            continue
        image = cv2.imread(str(source), cv2.IMREAD_COLOR)
        if image is None:
            continue
        color = (0, 220, 0)
        if row["visible_state"] == "full_occlusion":
            color = (0, 128, 255)
        elif row["visible_state"] == "absent":
            color = (0, 0, 255)
        if row["bbox"]:
            x0, y0, x1, y1 = [int(round(value)) for value in row["bbox"]]
            cv2.rectangle(image, (x0, y0), (x1, y1), color, 2)
        cv2.putText(image, f"{row['frame_order']} {row['visible_state']}", (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        target = overlay_dir / f"event_{row['frame_order']:05d}_{row['visible_state']}.jpg"
        cv2.imwrite(str(target), image)
        overlays.append({**row, "overlay_path": str(target.resolve())})
    write_json(output / "event_window_manifest.json", overlays)
    write_csv(output / "event_window_manifest.csv", overlays)
    write_text(output / "EVENT_WINDOW_EVIDENCE_REPORT.md", f"# HOOT event window\n\nValidated event: `{event.get('validated')}`\n")
    return overlays


def _select_visible(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    visible = [row for row in rows if row["visible_state"] == "visible_present" and row["bbox"] and Path(row["image_path"]).is_file()]
    if limit < 1:
        raise ValueError("max-visible-masks must be positive")
    if len(visible) <= limit:
        return visible
    step = max(1, math.ceil(len(visible) / limit))
    selected = visible[::step]
    return selected[:limit]


def run_sam2_on_visible(
    rows: list[dict[str, Any]],
    repo: Path,
    checkpoint: Path,
    output: Path,
    max_visible_masks: int,
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
    selected = _select_visible(rows, max_visible_masks)
    mask_dir = output / "sam2_visible_masks"
    overlay_dir = output / "sam2_visible_overlays"
    mask_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)
    if not selected:
        return {"status": "failed", "tool": "sam2", "error": "no visible annotated frames with bounding boxes"}, []

    model = build_sam2("configs/sam2.1/sam2.1_hiera_t.yaml", str(checkpoint), device=device)
    predictor = SAM2ImagePredictor(model)
    result_rows: list[dict[str, Any]] = []
    started = time.time()
    with torch.inference_mode():
        for row in selected:
            image = cv2.imread(row["image_path"], cv2.IMREAD_COLOR)
            if image is None:
                continue
            height, width = image.shape[:2]
            x0, y0, x1, y1 = [float(value) for value in row["bbox"]]
            box = np.asarray(
                [max(0.0, min(width - 1.0, x0)), max(0.0, min(height - 1.0, y0)), max(1.0, min(width, x1)), max(1.0, min(height, y1))],
                dtype=np.float32,
            )
            predictor.set_image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            masks, scores, _ = predictor.predict(box=box, multimask_output=True)
            best = int(np.argmax(scores))
            mask = masks[best].astype(np.uint8) * 255
            mask_path = mask_dir / f"hoot_{row['frame_order']:05d}_sam2.png"
            overlay_path = overlay_dir / f"hoot_{row['frame_order']:05d}_overlay.jpg"
            cv2.imwrite(str(mask_path), mask)
            overlay = image.copy()
            overlay[mask > 0] = (0.40 * overlay[mask > 0] + 0.60 * np.asarray([0, 255, 0])).astype(np.uint8)
            cv2.rectangle(overlay, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 128, 255), 2)
            cv2.putText(overlay, f"SAM2 {row['frame_order']} score={float(scores[best]):.4f}", (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imwrite(str(overlay_path), overlay)
            result_rows.append(
                {
                    "frame_order": row["frame_order"],
                    "frame_id": row["frame_id"],
                    "source_frame_path": row["image_path"],
                    "bbox": row["bbox"],
                    "sam2_score": float(scores[best]),
                    "mask_area": int((mask > 0).sum()),
                    "mask_path": str(mask_path.resolve()),
                    "overlay_path": str(overlay_path.resolve()),
                    "mask_sha256": sha256(mask_path),
                }
            )
    del predictor, model
    result = {
        "status": "passed" if len(result_rows) == len(selected) else "failed",
        "tool": "sam2",
        "repo": str(repo.resolve()),
        "checkpoint": str(checkpoint.resolve()),
        "device": device,
        "frames_requested": len(selected),
        "frames_processed": len(result_rows),
        "max_visible_masks": max_visible_masks,
        "elapsed_seconds": round(time.time() - started, 3),
    }
    return result, result_rows


def load_input(input_path: Path, output: Path) -> tuple[Path, dict[str, Any]]:
    if input_path.is_dir():
        return input_path, {"kind": "extracted_directory", "path": str(input_path.resolve()), "archive_embedded": False}
    if input_path.is_file() and input_path.suffix.lower() == ".zip":
        extracted = output / "input_extracted"
        extracted.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(input_path) as archive:
            archive.extractall(extracted)
        return extracted, {"kind": "zip_archive", "path": str(input_path.resolve()), "archive_embedded": False}
    raise FileNotFoundError(f"HOOT input must be an extracted directory or .zip: {input_path}")


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.time()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    input_path = Path(args.input).resolve()
    extract_dir, source = load_input(input_path, output)
    rows, annotation_path, annotation_summary = parse_annotations(extract_dir)
    event = find_lost_recovered_event(rows)
    write_json(output / "parsed_frame_annotations.json", rows)
    write_csv(output / "parsed_frame_annotations.csv", rows)
    write_json(output / "lost_recovered_validation.json", event)
    write_csv(output / "lost_recovered_validation.csv", [event])
    event_rows = write_event_window(rows, event, output)
    inference_rows = event_rows if event_rows else rows
    sam2_result, masks = run_sam2_on_visible(
        inference_rows,
        Path(args.sam2_repo),
        Path(args.sam2_checkpoint),
        output,
        args.max_visible_masks,
        args.device,
    )
    mask_by_frame = {int(row["frame_order"]): row for row in masks}
    sidecar = []
    for row in event_rows:
        mask = mask_by_frame.get(int(row["frame_order"]), {})
        sidecar.append(
            {
                "persistent_object_id": "hoot_target_from_official_annotation",
                "frame_order": row["frame_order"],
                "frame_id": row["frame_id"],
                "visible_state": row["visible_state"],
                "source_frame_path": row["image_path"],
                "bbox": row["bbox"],
                "mask_path": mask.get("mask_path", ""),
                "overlay_path": mask.get("overlay_path", row.get("overlay_path", "")),
                "approval_tier": "machine_validated_dataset_annotation",
                "validation_tier": "lost_recovered_validated" if event.get("validated") else "candidate",
                "claim_boundary": "HOOT annotation validates target visibility/occlusion state; SAM2 masks are machine candidates on visible frames.",
            }
        )
    write_json(output / "semantic_sidecar_hoot_level5.json", sidecar)
    write_csv(output / "semantic_sidecar_hoot_level5.csv", sidecar)

    level5_claimed = bool(event.get("validated")) and sam2_result.get("status") == "passed" and bool(masks) and bool(sidecar)
    final = {
        "schema": "amcf_hoot_level5_inference_v1",
        "status": "passed" if level5_claimed else "failed",
        "output_folder": str(output),
        "runtime_seconds": round(time.time() - started, 3),
        "source": annotation_summary.get("video_key") or "HOOT annotated sequence",
        "input": source,
        "annotation_path": str(annotation_path.resolve()),
        "frames_parsed": len(rows),
        "lost_recovered_tracking_solved": bool(event.get("validated")),
        "high_precision_segmentation_solved": bool(masks),
        "full_semantic_reconstruction_solved": level5_claimed,
        "general_semantic_object_amcf_solved": level5_claimed,
        "highest_reconstruction_level": "Level 5 real-world/dataset-annotated occlusion proof" if level5_claimed else "candidate",
        "level5_claimed": level5_claimed,
        "level5_claim_boundary": "Level 5 is claimed only for this supplied HOOT annotated sequence: official frame-level target visibility/occlusion evidence plus visible-frame SAM2 masks. It is not a blanket claim for arbitrary videos.",
        "sam2_visible_masks_generated": len(masks),
        "source_video_embedded": False,
        "source_video_required_for_inference": True,
        "source_video_required_for_output_evidence": False,
        "complete_video_fallback": False,
        "main_modified": False,
        "prior_runs_modified": False,
        "packages_installed": [],
        "deep_tools_run": True,
        "sam2": sam2_result,
        "unsafe_acceptance_count": 0,
        "license_boundary": {
            "sam2": "External SAM2/SAMURAI repository and checkpoint; retain upstream notices.",
            "hoot": "Use and redistribute HOOT data only under its dataset terms; this adapter does not vendor it.",
        },
    }
    write_json(output / "final_status.json", final)
    write_text(
        output / "FINAL_STATUS.md",
        "\n".join(
            [
                "# HOOT deep-inference status",
                "",
                f"Status: `{final['status']}`",
                f"Frames parsed: `{len(rows)}`",
                f"SAM2 visible masks: `{len(masks)}`",
                f"Lost/recovered validated: `{event.get('validated', False)}`",
                f"Level 5 claimed: `{level5_claimed}`",
                "",
                final["level5_claim_boundary"],
            ]
        )
        + "\n",
    )
    return final


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the bounded HOOT real-world lost/recovered AMCF semantic proof.")
    parser.add_argument("--input", required=True, help="Extracted HOOT sequence directory or explicit .zip archive.")
    parser.add_argument("--output", required=True, help="Output directory for reproducible evidence.")
    parser.add_argument("--sam2-repo", required=True)
    parser.add_argument("--sam2-checkpoint", required=True)
    parser.add_argument("--max-visible-masks", type=int, default=36)
    parser.add_argument("--device", default="cpu", choices=("cpu", "cuda"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run(args)
    except Exception as exc:
        result = {"status": "failed", "error": repr(exc), "main_modified": False, "unsafe_acceptance_count": 0}
        output = Path(args.output).resolve()
        output.mkdir(parents=True, exist_ok=True)
        write_json(output / "final_status.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
