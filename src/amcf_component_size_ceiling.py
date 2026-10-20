"""Deterministic component-archive size/quality search."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive
from amcf_quality_metrics import compare_ppm_frame_folders


RUN_NAME = "AMCF_COMPONENT_SIZE_CEILING_OPTIMIZATION_V1"


def optimize_component_archive(
    source_manifest_path: str | Path,
    output_dir: str | Path,
    *,
    source_size_ceiling_bytes: int | None = None,
    quality_candidates: Iterable[int] = (35, 25, 15, 8, 4),
    max_mae: float = 12.0,
    min_ssim: float = 0.85,
    segmentation_mode: str = "opencv_changed_region",
) -> dict[str, Any]:
    source_manifest_path = Path(source_manifest_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    source_root = source_manifest_path.parent
    ceiling = source_size_ceiling_bytes
    if ceiling is None:
        source_video = source_manifest.get("source_video", {})
        ceiling = int(source_video.get("bytes") or 0) or None
    if ceiling is None:
        ceiling = sum((source_root / str(entry["file"])).stat().st_size for entry in source_manifest["frame_entries"])

    candidates: list[dict[str, Any]] = []
    for quality in quality_candidates:
        quality = int(quality)
        candidate_dir = output_dir / f"quality_{quality:03d}"
        archive_path = candidate_dir / "component_event_archive.amcf.zip"
        decoded_dir = candidate_dir / "decoded"
        result = build_component_event_archive(
            source_manifest_path,
            archive_path,
            source_size_ceiling_bytes=ceiling,
            prefer_webp=True,
            segmentation_mode=segmentation_mode,
            webp_quality=quality,
        )
        decoded = decode_component_event_archive(archive_path, decoded_dir)
        quality_report = compare_ppm_frame_folders(source_root / "frames", decoded_dir / "decoded_frames")
        mean_mae = quality_report.get("mean_absolute_error")
        mean_ssim = quality_report.get("mean_ssim")
        visual_passed = (
            quality_report.get("expected_frame_count") == quality_report.get("actual_frame_count")
            and mean_mae is not None
            and float(mean_mae) <= max_mae
            and mean_ssim is not None
            and float(mean_ssim) >= min_ssim
        )
        candidates.append(
            {
                "quality": quality,
                "archive_path": str(archive_path),
                "archive_bytes": int(result["archive_size_ceiling"]["archive_bytes"]),
                "ceiling_bytes": int(ceiling),
                "under_source_size_ceiling": bool(result["archive_size_ceiling"]["under_source_size_ceiling"]),
                "frame_count": int(result["frame_count"]),
                "event_count": int(result["event_count"]),
                "payload_format": result["payload_format"],
                "visual": {
                    "passed": bool(visual_passed),
                    "mean_mae": mean_mae,
                    "mean_ssim": mean_ssim,
                    "max_mae": max_mae,
                    "min_ssim": min_ssim,
                    "decoded_frame_count": quality_report.get("actual_frame_count"),
                },
                "unsafe_acceptance_count": 0,
            }
        )

    accepted = [
        item for item in candidates
        if item["under_source_size_ceiling"] and item["visual"]["passed"]
    ]
    selected = max(accepted, key=lambda item: item["quality"]) if accepted else None
    return {
        "run_name": RUN_NAME,
        "source_manifest": str(source_manifest_path),
        "source_size_ceiling_bytes": int(ceiling),
        "quality_candidates": [int(value) for value in quality_candidates],
        "visual_thresholds": {"max_mae": max_mae, "min_ssim": min_ssim},
        "candidates": candidates,
        "selected": selected,
        "final_passed": selected is not None,
        "unsafe_acceptance_count": 0,
        "claim_boundary_flags": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
        },
    }
