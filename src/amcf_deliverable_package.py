from __future__ import annotations

import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Any

from amcf_quality_metrics import read_ppm, sha256_bytes, write_ppm


FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


TRACK_TAXONOMY = [
    {
        "track_id": "WATERFALL_COLUMN",
        "label": "Waterfall Column",
        "parent_id": None,
        "color_rgb": [0, 220, 255],
        "min_interval_frames": 4,
        "motion_threshold_px_s": 28.0,
    },
    {
        "track_id": "WATER_IMPACT_FOAM",
        "label": "Water Impact Foam",
        "parent_id": "WATERFALL_COLUMN",
        "color_rgb": [255, 255, 0],
        "min_interval_frames": 3,
        "motion_threshold_px_s": 24.0,
    },
    {
        "track_id": "MIST_SPRAY",
        "label": "Mist Spray",
        "parent_id": "WATERFALL_COLUMN",
        "color_rgb": [230, 160, 255],
        "min_interval_frames": 6,
        "motion_threshold_px_s": 18.0,
    },
    {
        "track_id": "FOREGROUND_TREE_LEFT",
        "label": "Foreground Tree Left",
        "parent_id": None,
        "color_rgb": [80, 255, 80],
        "min_interval_frames": 18,
        "motion_threshold_px_s": 10.0,
    },
    {
        "track_id": "FOREGROUND_TREE_RIGHT",
        "label": "Foreground Tree Right",
        "parent_id": None,
        "color_rgb": [80, 180, 255],
        "min_interval_frames": 18,
        "motion_threshold_px_s": 10.0,
    },
    {
        "track_id": "MIDGROUND_TREE",
        "label": "Midground Tree",
        "parent_id": None,
        "color_rgb": [255, 160, 80],
        "min_interval_frames": 18,
        "motion_threshold_px_s": 10.0,
    },
    {
        "track_id": "BRANCH_LEAF_GROUP_LEFT",
        "label": "Branch Leaf Group Left",
        "parent_id": "FOREGROUND_TREE_LEFT",
        "color_rgb": [120, 255, 160],
        "min_interval_frames": 10,
        "motion_threshold_px_s": 12.0,
    },
    {
        "track_id": "BRANCH_LEAF_GROUP_RIGHT",
        "label": "Branch Leaf Group Right",
        "parent_id": "FOREGROUND_TREE_RIGHT",
        "color_rgb": [255, 120, 160],
        "min_interval_frames": 10,
        "motion_threshold_px_s": 12.0,
    },
]


def build_track_taxonomy_report() -> dict[str, Any]:
    return {
        "ok": True,
        "schema": "amcf-local-main-track-taxonomy-v1",
        "taxonomy_source": "clean public data model derived from local Main track categories",
        "track_count": len(TRACK_TAXONOMY),
        "tracks": TRACK_TAXONOMY,
        "claim_boundary": _claim_boundary(),
        "unsafe_acceptance_count": 0,
    }


def build_deliverable_package(
    *,
    archive_path: str | Path,
    source_frames_dir: str | Path,
    decoded_frames_dir: str | Path,
    quality_report: dict[str, Any],
    viewer_dir: str | Path | None,
    output_dir: str | Path,
    fps: int = 6,
) -> dict[str, Any]:
    archive_path = Path(archive_path)
    source_frames_dir = Path(source_frames_dir)
    decoded_frames_dir = Path(decoded_frames_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    package_dir = output_dir / "deliverable"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    archive_target = package_dir / archive_path.name
    shutil.copy2(archive_path, archive_target)

    comparison_dir = package_dir / "comparison_frames"
    comparison_entries = build_comparison_frames(source_frames_dir, decoded_frames_dir, comparison_dir)
    taxonomy_report = build_track_taxonomy_report()
    (package_dir / "track_taxonomy.json").write_text(json.dumps(taxonomy_report, indent=2, sort_keys=True), encoding="utf-8")
    (package_dir / "quality_report.json").write_text(json.dumps(quality_report, indent=2, sort_keys=True), encoding="utf-8")

    viewer_manifest_path = None
    if viewer_dir is not None:
        viewer_dir = Path(viewer_dir)
        if viewer_dir.exists():
            shutil.copytree(viewer_dir, package_dir / "viewer")
            viewer_manifest_path = "viewer/viewer_manifest.json"

    comparison_video = _build_comparison_video(comparison_dir, package_dir / "comparison_sync.mp4", fps=fps)

    manifest = {
        "schema": "amcf-public-deliverable-package-v1",
        "archive": archive_target.name,
        "comparison_frame_count": len(comparison_entries),
        "comparison_frames": comparison_entries,
        "comparison_video": comparison_video,
        "viewer_manifest": viewer_manifest_path,
        "track_taxonomy": "track_taxonomy.json",
        "quality_report": "quality_report.json",
        "claim_boundary": _claim_boundary(),
        "unsafe_acceptance_count": 0,
    }
    manifest_path = package_dir / "deliverable_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    summary_path = package_dir / "DELIVERABLE_SUMMARY.md"
    summary_path.write_text(_summary_markdown(manifest), encoding="utf-8")
    zip_path = output_dir / "amcf_public_deliverable_package.zip"
    _zip_directory(package_dir, zip_path)

    return {
        "ok": True,
        "deliverable_dir": str(package_dir),
        "deliverable_manifest": str(manifest_path),
        "zip_path": str(zip_path),
        "zip_sha256": sha256_bytes(zip_path.read_bytes()),
        "comparison_frame_count": len(comparison_entries),
        "comparison_video_created": bool(comparison_video["created"]),
        "track_taxonomy_count": taxonomy_report["track_count"],
        "claim_boundary": manifest["claim_boundary"],
        "unsafe_acceptance_count": 0,
    }


def build_comparison_frames(source_frames_dir: str | Path, decoded_frames_dir: str | Path, output_dir: str | Path) -> list[dict[str, Any]]:
    source_frames = sorted(Path(source_frames_dir).glob("frame_*.ppm"))
    decoded_frames = sorted(Path(decoded_frames_dir).glob("frame_*.ppm"))
    if len(source_frames) != len(decoded_frames):
        raise ValueError("source and decoded frame counts differ")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    for index, (source_path, decoded_path) in enumerate(zip(source_frames, decoded_frames)):
        src_w, src_h, source_pixels = read_ppm(source_path)
        dec_w, dec_h, decoded_pixels = read_ppm(decoded_path)
        if (src_w, src_h) != (dec_w, dec_h):
            raise ValueError("source and decoded frame dimensions differ")
        comparison_pixels = _comparison_pixels(source_pixels, decoded_pixels)
        output_path = output_dir / f"comparison_frame_{index:03d}.ppm"
        write_ppm(output_path, src_w * 3, src_h, comparison_pixels)
        entries.append(
            {
                "frame_index": index,
                "file": f"comparison_frames/{output_path.name}",
                "sha256": sha256_bytes(comparison_pixels),
            }
        )
    return entries


def _comparison_pixels(source: bytes, decoded: bytes) -> bytes:
    if len(source) != len(decoded):
        raise ValueError("source and decoded payload lengths differ")
    out = bytearray()
    for offset in range(0, len(source), 3):
        src = source[offset:offset + 3]
        dec = decoded[offset:offset + 3]
        diff = bytes(min(255, abs(src[channel] - dec[channel]) * 5) for channel in range(3))
        out.extend(src)
        out.extend(dec)
        out.extend(diff)
    return bytes(out)


def _build_comparison_video(frames_dir: Path, output_video: Path, *, fps: int) -> dict[str, Any]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return {"created": False, "reason": "ffmpeg_not_found", "path": str(output_video)}
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-framerate",
        str(fps),
        "-i",
        str(frames_dir / "comparison_frame_%03d.ppm"),
        "-pix_fmt",
        "yuv420p",
        str(output_video),
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        return {
            "created": False,
            "reason": "ffmpeg_failed",
            "path": str(output_video),
            "stderr": completed.stderr.strip(),
        }
    return {"created": True, "path": str(output_video), "bytes": output_video.stat().st_size}


def _zip_directory(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(source_dir).as_posix(), FIXED_ZIP_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, path.read_bytes())


def _summary_markdown(manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# AMCF Public Deliverable Package",
            "",
            "This package is a software AMCF deliverable bundle for inspection and parity testing.",
            "",
            f"- Archive: `{manifest['archive']}`",
            f"- Comparison frames: {manifest['comparison_frame_count']}",
            f"- Comparison video created: {str(manifest['comparison_video']['created']).lower()}",
            f"- unsafe_acceptance_count: {manifest['unsafe_acceptance_count']}",
            "- hardware_validation_claimed: false",
            "- physical_level_5_claimed: false",
            "- manufactured_player_claimed: false",
            "",
            "This is not a GUI, EXE, hardware validation result, or manufactured-player claim.",
            "",
        ]
    )


def _claim_boundary() -> dict[str, bool]:
    return {
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "real_printer_required": False,
        "real_reader_required": False,
        "real_player_required": False,
        "real_scanner_required": False,
        "real_usb_required": False,
        "viewer_is_final_ui": False,
    }
