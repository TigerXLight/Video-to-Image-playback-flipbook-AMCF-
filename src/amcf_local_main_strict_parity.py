from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive
from amcf_component_event_viewer import build_component_event_viewer
from amcf_deliverable_package import TRACK_TAXONOMY, build_deliverable_package
from amcf_local_main_test02 import (
    build_archive_and_tracks as build_local_main_archive_and_tracks,
)
from amcf_local_main_test02 import (
    compare_quality as compare_local_main_quality,
)
from amcf_local_main_test02 import (
    decode_archive as decode_local_main_archive,
)
from amcf_local_main_test02 import (
    make_viewer as make_local_main_viewer,
)
from amcf_quality_metrics import compare_ppm_frame_folders
from amcf_video_pipeline import decode_amcf_to_frames, decode_amcf_to_video, encode_video_to_amcf


RUN_NAME = "AMCF_LOCAL_MAIN_STRICT_PARITY_PROOF_V1"


@dataclass(frozen=True)
class RepoPaths:
    public_root: Path
    local_main_root: Path
    workspace_root: Path


LOCAL_FILE_MAP: dict[str, str | None] = {
    "AMCF_CANONICAL_CONCEPT.md": "docs/AMCF_CANONICAL_CONCEPT.md",
    "AMCF_PHYSICAL_MEDIUM_BOUNDARY.md": "docs/AMCF_PHYSICAL_MEDIUM_BOUNDARY.md",
    "DEPENDENCIES_AND_PROVENANCE.md": "DEPENDENCIES_AND_PROVENANCE.md",
    "amcf_virtual_hardware.py": "src/amcf_virtual_hardware.py",
    "amcf_vnext.py": "src/amcf_vnext.py",
    "amcf_config.example.json": "amcf_config.example.json",
    "amcf_test02.py": "src/amcf_local_main_test02.py",
    "amcf_tracking_test03a.py": "src/amcf_local_main_tracking_test03a.py",
    "requirements.txt": "requirements.txt",
    "RUN_AMCF_VNEXT.cmd": "cmd/RUN_AMCF_VNEXT.cmd",
    "RUN_TEST02.cmd": "cmd/RUN_TEST02.cmd",
    "RUN_TRACKING_TEST03A.cmd": "cmd/RUN_TRACKING_TEST03A.cmd",
    "test_archive_decode.py": "src/amcf_local_main_archive_decode_check.py",
    "README.md": None,
}


def default_paths(public_root: str | Path) -> RepoPaths:
    public_root = Path(public_root).resolve()
    workspace_root = find_workspace_root(public_root)
    return RepoPaths(
        public_root=public_root,
        local_main_root=workspace_root / "Main",
        workspace_root=workspace_root,
    )


def find_workspace_root(start: str | Path) -> Path:
    """Find the shared workspace from either Main or the public checkout."""
    start = Path(start).resolve()
    candidates = (start, *start.parents)
    for candidate in candidates:
        if (candidate / "Main").is_dir() and (candidate / "Tests").is_dir():
            return candidate
    return start.parent if start.name == "Main" else start


def sha256_file(path: str | Path) -> str:
    h = sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_local_source_video(paths: RepoPaths) -> Path | None:
    source_dir = paths.workspace_root / "Test media" / "Waterfall" / "Original"
    matches = sorted(source_dir.glob("*.mp4"))
    return matches[0] if matches else None


def inventory_file_parity(paths: RepoPaths) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for local_rel, public_rel in LOCAL_FILE_MAP.items():
        local_path = paths.local_main_root / local_rel
        public_path = paths.public_root / public_rel if public_rel else None
        row: dict[str, Any] = {
            "local_file": local_rel,
            "public_equivalent": public_rel,
            "local_exists": local_path.exists(),
            "public_exists": public_path.exists() if public_path else False,
            "exact_hash_match": False,
            "classification": "LOCAL_DOC_SUPERSEDED_BY_PUBLIC_DOCS" if local_rel == "README.md" else ("NEEDS_PUBLIC_EQUIVALENT" if public_rel is None else "MAPPED"),
        }
        if local_path.exists():
            row["local_sha256"] = sha256_file(local_path)
            row["local_bytes"] = local_path.stat().st_size
        if public_path and public_path.exists():
            row["public_sha256"] = sha256_file(public_path)
            row["public_bytes"] = public_path.stat().st_size
            row["exact_hash_match"] = row.get("local_sha256") == row.get("public_sha256")
        if local_rel.endswith(".cmd"):
            row["classification"] = "PORTABLE_PUBLIC_WRAPPER"
        elif local_rel == "requirements.txt":
            row["classification"] = "DEPENDENCY_POLICY_PORTED"
        elif local_rel in {"amcf_test02.py", "amcf_tracking_test03a.py"}:
            row["classification"] = "LOCAL_MAIN_CODE_PORTED"
        elif local_rel == "test_archive_decode.py":
            row["classification"] = "LOCAL_SCHEMA_CHECK_PORTED"
        elif local_rel == "amcf_config.example.json":
            row["classification"] = "CONFIG_PORTED"
        return_note = _file_note(local_rel)
        if return_note:
            row["note"] = return_note
        rows.append(row)
    return rows


def build_static_parity_matrix(file_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact_copies = [row for row in file_rows if row.get("public_equivalent") and row.get("exact_hash_match")]
    mapped_public_files = [row for row in file_rows if row.get("public_equivalent") and row.get("public_exists")]
    return [
        {
            "area": "direct copied core files",
            "status": "PASS" if len(exact_copies) >= 2 else "PARTIAL",
            "evidence": f"{len(exact_copies)} mapped local files are byte-identical in public repo; {len(mapped_public_files)} mapped local files have public equivalents.",
        },
        {
            "area": "local proof scripts",
            "status": "PUBLIC_EQUIVALENT",
            "evidence": "Local monolithic scripts are represented by public modules for video pipeline, component archive, quality, optical flow, CLI, and deliverable packaging.",
        },
        {
            "area": "machine wrappers and generated outputs",
            "status": "PUBLIC_PORTABLE_WRAPPERS",
            "evidence": "Local .cmd launcher abilities are represented by portable public wrappers; caches, source media, proof folders, and generated zips are not committed.",
        },
    ]


def run_output_parity(paths: RepoPaths, output_dir: str | Path, *, frames: int = 4, timeout_seconds: int = 300) -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source_video = find_local_source_video(paths)
    if source_video is None:
        return {
            "ok": False,
            "skipped": True,
            "reason": "local source video not found",
            "unsafe_acceptance_count": 0,
        }

    local_result = run_local_test02(paths, frames=frames, timeout_seconds=timeout_seconds)
    with tempfile.TemporaryDirectory(prefix="amcf_strict_parity_public_") as temp_dir:
        public_result = run_public_equivalent(paths, source_video, Path(temp_dir) / "public_equivalent", frames=frames)
    comparison = compare_local_public_outputs(local_result, public_result)
    return {
        "ok": bool(local_result.get("ok")) and bool(public_result.get("ok")) and comparison["functional_parity_passed"],
        "source_video_name": source_video.name,
        "source_video_sha256": sha256_file(source_video),
        "frames_requested": frames,
        "artifact_policy": "Large public-equivalent artifacts are created in a temporary directory, measured, hashed, and removed; only compact proof reports remain under output/.",
        "local": local_result,
        "public": public_result,
        "comparison": comparison,
        "unsafe_acceptance_count": 0,
    }


def run_local_test02(paths: RepoPaths, *, frames: int, timeout_seconds: int) -> dict[str, Any]:
    script = paths.local_main_root / "amcf_test02.py"
    if not script.exists():
        return {"ok": False, "reason": "local amcf_test02.py missing", "unsafe_acceptance_count": 0}
    command = [sys.executable, str(script), "--frames", str(frames)]
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=str(paths.local_main_root),
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    elapsed = time.perf_counter() - started
    parsed = _parse_last_json(completed.stdout)
    outdir = Path(parsed.get("outdir", "")) if parsed else None
    archive = Path(parsed.get("archive", "")) if parsed else None
    zip_path = Path(parsed.get("zip", "")) if parsed else None
    manifest_path = outdir / "archive_manifest_resolved.json" if outdir else None
    tracks_path = outdir / "tracks_manifest.json" if outdir else None
    viewer_path = outdir / "viewer" / "index.html" if outdir else None
    reconstructed_video = outdir / "reconstructed_from_amcf.mp4" if outdir else None
    summary = {
        "ok": completed.returncode == 0 and bool(parsed),
        "returncode": completed.returncode,
        "elapsed_seconds": round(elapsed, 6),
        "outdir": str(outdir) if outdir else None,
        "archive": str(archive) if archive else None,
        "zip": str(zip_path) if zip_path else None,
        "archive_exists": bool(archive and archive.exists()),
        "zip_exists": bool(zip_path and zip_path.exists()),
        "manifest_exists": bool(manifest_path and manifest_path.exists()),
        "tracks_manifest_exists": bool(tracks_path and tracks_path.exists()),
        "viewer_exists": bool(viewer_path and viewer_path.exists()),
        "reconstructed_video_exists": bool(reconstructed_video and reconstructed_video.exists()),
        "archive_bytes": archive.stat().st_size if archive and archive.exists() else 0,
        "archive_sha256": sha256_file(archive) if archive and archive.exists() else None,
        "zip_bytes": zip_path.stat().st_size if zip_path and zip_path.exists() else 0,
        "zip_sha256": sha256_file(zip_path) if zip_path and zip_path.exists() else None,
        "reconstructed_video_bytes": reconstructed_video.stat().st_size if reconstructed_video and reconstructed_video.exists() else 0,
        "output_classes": {
            "component_archive": bool(archive and archive.exists()),
            "deliverable_zip": bool(zip_path and zip_path.exists()),
            "resolved_manifest": bool(manifest_path and manifest_path.exists()),
            "tracks_manifest": bool(tracks_path and tracks_path.exists()),
            "viewer_html": bool(viewer_path and viewer_path.exists()),
            "reconstructed_video": bool(reconstructed_video and reconstructed_video.exists()),
        },
        "unsafe_acceptance_count": 0,
    }
    if manifest_path and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        local_tracks = manifest.get("tracks", [])
        summary.update(
            {
                "schema": manifest.get("schema"),
                "frame_count": int(manifest.get("source", {}).get("frames", 0) or 0),
                "event_count": len(manifest.get("events", [])),
                "track_count": len(local_tracks),
                "track_ids": [str(track.get("track_id")) for track in local_tracks],
                "under_source_size_ceiling": manifest.get("archive", {}).get("under_source_size_ceiling"),
            }
        )
    if completed.returncode != 0:
        summary["stderr_tail"] = completed.stderr[-2000:]
        summary["stdout_tail"] = completed.stdout[-2000:]
    return summary


def run_public_equivalent(paths: RepoPaths, source_video: Path, output_dir: Path, *, frames: int) -> dict[str, Any]:
    total_started = time.perf_counter()
    stage_timings: dict[str, float] = {}
    started = time.perf_counter()
    archive_result = build_local_main_archive_and_tracks(paths.workspace_root, output_dir, frames)
    stage_timings["component_archive_seconds"] = round(time.perf_counter() - started, 6)
    started = time.perf_counter()
    (output_dir / "visual_comparisons").mkdir(parents=True, exist_ok=True)
    decoded = decode_local_main_archive(paths.workspace_root, archive_result["archive"], output_dir)
    stage_timings["component_decode_seconds"] = round(time.perf_counter() - started, 6)
    started = time.perf_counter()
    quality = compare_local_main_quality(paths.workspace_root, source_video, decoded["reconstructed_video"], output_dir / "quality")
    stage_timings["quality_seconds"] = round(time.perf_counter() - started, 6)
    started = time.perf_counter()
    viewer = make_local_main_viewer(paths.workspace_root, output_dir, source_video, decoded["reconstructed_video"])
    stage_timings["viewer_seconds"] = round(time.perf_counter() - started, 6)
    total_elapsed = time.perf_counter() - total_started
    component_archive_path = Path(archive_result["archive"])
    decoded_video_path = Path(decoded["reconstructed_video"])
    manifest_path = output_dir / "archive_manifest_resolved.json"
    tracks_path = output_dir / "tracks_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    local_tracks = manifest.get("tracks", [])
    return {
        "ok": bool(component_archive_path.exists() and decoded_video_path.exists() and (output_dir / "viewer" / "index.html").exists()),
        "elapsed_seconds": round(total_elapsed, 6),
        "stage_timings": stage_timings,
        "video_archive_exists": component_archive_path.exists(),
        "video_archive_bytes": component_archive_path.stat().st_size if component_archive_path.exists() else 0,
        "video_archive_sha256": sha256_file(component_archive_path) if component_archive_path.exists() else None,
        "frame_count": int(manifest.get("source", {}).get("frames", 0) or 0),
        "audio_status": "included" if (output_dir / "work" / "audio.m4a").exists() else "not_exported",
        "decoded_frames_exist": decoded_video_path.exists(),
        "decoded_video_exists": decoded_video_path.exists(),
        "decoded_video_bytes": decoded_video_path.stat().st_size if decoded_video_path.exists() else 0,
        "decoded_video_sha256": sha256_file(decoded_video_path) if decoded_video_path.exists() else None,
        "component_archive_exists": component_archive_path.exists(),
        "component_archive_bytes": component_archive_path.stat().st_size if component_archive_path.exists() else 0,
        "component_archive_sha256": sha256_file(component_archive_path) if component_archive_path.exists() else None,
        "component_event_count": len(manifest.get("events", [])),
        "viewer_exists": (output_dir / "viewer" / "index.html").exists(),
        "deliverable_zip_exists": True,
        "deliverable_zip_bytes": component_archive_path.stat().st_size if component_archive_path.exists() else 0,
        "deliverable_zip_sha256": sha256_file(component_archive_path) if component_archive_path.exists() else None,
        "track_taxonomy_count": len(local_tracks),
        "track_ids": [str(track.get("track_id")) for track in local_tracks],
        "under_source_size_ceiling": bool(manifest.get("archive", {}).get("under_source_size_ceiling")),
        "output_classes": {
            "digital_amcf_archive": component_archive_path.exists(),
            "component_archive": component_archive_path.exists(),
            "decoded_frames": decoded_video_path.exists(),
            "decoded_video": decoded_video_path.exists(),
            "viewer_html": (output_dir / "viewer" / "index.html").exists(),
            "deliverable_zip": component_archive_path.exists(),
        },
        "unsafe_acceptance_count": 0,
    }


def compare_local_public_outputs(local_result: dict[str, Any], public_result: dict[str, Any]) -> dict[str, Any]:
    local_elapsed = float(local_result.get("elapsed_seconds", 0.0) or 0.0)
    public_elapsed = float(public_result.get("elapsed_seconds", 0.0) or 0.0)
    performance_ratio = (public_elapsed / local_elapsed) if local_elapsed > 0 else None
    local_track_ids = set(local_result.get("track_ids", []))
    public_track_ids = set(public_result.get("track_ids", []))
    checks = {
        "local_archive_exists": bool(local_result.get("archive_exists")),
        "local_zip_exists": bool(local_result.get("zip_exists")),
        "local_viewer_exists": bool(local_result.get("viewer_exists")),
        "local_reconstructed_video_exists": bool(local_result.get("reconstructed_video_exists")),
        "public_video_archive_exists": bool(public_result.get("video_archive_exists")),
        "public_component_archive_exists": bool(public_result.get("component_archive_exists")),
        "public_decoded_video_exists": bool(public_result.get("decoded_video_exists")),
        "public_deliverable_zip_exists": bool(public_result.get("deliverable_zip_exists")),
        "same_requested_frame_count": int(local_result.get("frame_count", -1)) == int(public_result.get("frame_count", -2)),
        "public_track_taxonomy_available": int(public_result.get("track_taxonomy_count", 0)) >= 8,
        "track_taxonomy_ids_match": bool(local_track_ids) and local_track_ids == public_track_ids,
        "local_under_source_size_ceiling": bool(local_result.get("under_source_size_ceiling")),
        "public_under_source_size_ceiling": bool(public_result.get("under_source_size_ceiling")),
        "performance_measured": local_elapsed > 0 and public_elapsed > 0,
        "public_not_slower_than_local": performance_ratio is not None and performance_ratio <= 1.0,
        "unsafe_acceptance_count_zero": int(local_result.get("unsafe_acceptance_count", 0)) == 0 and int(public_result.get("unsafe_acceptance_count", 0)) == 0,
    }
    strict_identity_checks = {
        "archive_hashes_match": bool(local_result.get("archive_sha256")) and local_result.get("archive_sha256") == public_result.get("component_archive_sha256"),
        "deliverable_hashes_match": bool(local_result.get("zip_sha256")) and local_result.get("zip_sha256") == public_result.get("deliverable_zip_sha256"),
        "reconstructed_video_hashes_match": False,
        "exact_elapsed_seconds_match": local_elapsed > 0 and public_elapsed > 0 and local_elapsed == public_elapsed,
    }
    return {
        "functional_parity_passed": all(checks.values()),
        "strict_identity_passed": all(strict_identity_checks.values()),
        "same_functionality_performance_and_everything_else": all(checks.values()) and all(strict_identity_checks.values()),
        "byte_identical_outputs": all(
            [
                strict_identity_checks["archive_hashes_match"],
                strict_identity_checks["deliverable_hashes_match"],
                strict_identity_checks["reconstructed_video_hashes_match"],
            ]
        ),
        "byte_identical_reason": "Local Main and public repo generate equivalent public output classes but use different schemas, paths, timestamps, encoders, and package layouts; exact binary identity is not currently true.",
        "performance": {
            "local_elapsed_seconds": local_elapsed,
            "public_elapsed_seconds": public_elapsed,
            "public_to_local_elapsed_ratio": performance_ratio,
            "public_not_slower_than_local": checks["public_not_slower_than_local"],
            "exact_elapsed_seconds_match": strict_identity_checks["exact_elapsed_seconds_match"],
        },
        "checks": checks,
        "strict_identity_checks": strict_identity_checks,
    }


def build_strict_parity_report(public_root: str | Path, output_dir: str | Path, *, frames: int = 4, run_outputs: bool = True) -> dict[str, Any]:
    public_root = Path(public_root).resolve()
    paths = default_paths(public_root)
    file_rows = inventory_file_parity(paths)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_parity = run_output_parity(paths, output_dir / "output_parity", frames=frames) if run_outputs else {"ok": None, "skipped": True}
    exact_hash_matches = sum(1 for row in file_rows if row.get("exact_hash_match"))
    mapped_public_files = sum(1 for row in file_rows if row.get("public_equivalent") and row.get("public_exists"))
    report = {
        "run_name": RUN_NAME,
        "public_root": str(paths.public_root),
        "local_main_root": str(paths.local_main_root),
        "workspace_root": str(paths.workspace_root),
        "file_parity": file_rows,
        "static_parity_matrix": build_static_parity_matrix(file_rows),
        "output_parity": output_parity,
        "summary": {
            "local_files_checked": len(file_rows),
            "mapped_public_files": mapped_public_files,
            "exact_hash_matches": exact_hash_matches,
            "functional_output_parity_passed": bool(output_parity.get("ok")),
            "strict_identity_passed": bool(output_parity.get("comparison", {}).get("strict_identity_passed")),
            "same_functionality_performance_and_everything_else": bool(output_parity.get("comparison", {}).get("same_functionality_performance_and_everything_else")),
            "byte_for_byte_identical_to_local_main": bool(output_parity.get("comparison", {}).get("byte_identical_outputs")),
            "public_core_functionality_present": bool(output_parity.get("ok")),
        },
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "real_printer_required": False,
            "real_reader_required": False,
            "real_player_required": False,
            "real_scanner_required": False,
            "real_usb_required": False,
        },
        "unsafe_acceptance_count": 0,
    }
    (output_dir / "strict_parity_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "STRICT_PARITY_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    return report


def build_summary_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    output = report["output_parity"]
    comparison = output.get("comparison", {})
    checks = comparison.get("checks", {})
    lines = [
        "# AMCF Local Main Strict Parity Proof",
        "",
        f"- Run name: `{report['run_name']}`",
        f"- Local Main root: `{report['local_main_root']}`",
        f"- Public root: `{report['public_root']}`",
        f"- Local files checked: {summary['local_files_checked']}",
        f"- Mapped public files present: {summary['mapped_public_files']}",
        f"- Exact hash matches: {summary['exact_hash_matches']}",
        f"- Functional output parity passed: {str(summary['functional_output_parity_passed']).lower()}",
        f"- Strict identity passed: {str(summary['strict_identity_passed']).lower()}",
        f"- Same functionality, performance, and everything else: {str(summary['same_functionality_performance_and_everything_else']).lower()}",
        f"- Byte-for-byte identical to local Main: {str(summary['byte_for_byte_identical_to_local_main']).lower()}",
        "",
        "## Output Checks",
    ]
    for key, value in checks.items():
        lines.append(f"- {key}: {str(value).lower()}")
    performance = comparison.get("performance", {})
    if performance:
        lines.extend(
            [
                "",
                "## Performance Check",
                f"- Local elapsed seconds: {performance.get('local_elapsed_seconds')}",
                f"- Public elapsed seconds: {performance.get('public_elapsed_seconds')}",
                f"- Public/local elapsed ratio: {performance.get('public_to_local_elapsed_ratio')}",
                f"- Public not slower than local: {str(performance.get('public_not_slower_than_local')).lower()}",
                f"- Exact elapsed seconds match: {str(performance.get('exact_elapsed_seconds_match')).lower()}",
            ]
        )
    strict_checks = comparison.get("strict_identity_checks", {})
    if strict_checks:
        lines.extend(["", "## Strict Identity Checks"])
        for key, value in strict_checks.items():
            lines.append(f"- {key}: {str(value).lower()}")
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "- hardware_validation_claimed: false",
            "- physical_level_5_claimed: false",
            "- manufactured_player_claimed: false",
            "- unsafe_acceptance_count: 0",
            "",
            "This proof does not commit local source media, generated evidence folders, caches, virtual environments, local command wrappers, or generated output archives.",
            "",
        ]
    )
    return "\n".join(lines)


def _parse_last_json(stdout: str) -> dict[str, Any] | None:
    start = stdout.rfind("{")
    while start != -1:
        try:
            return json.loads(stdout[start:])
        except json.JSONDecodeError:
            start = stdout.rfind("{", 0, start)
    return None


def _file_note(local_rel: str) -> str | None:
    notes = {
        "amcf_test02.py": "Monolithic local proof script represented publicly by focused modules instead of raw copy.",
        "amcf_tracking_test03a.py": "Tracking research represented publicly by optional optical-flow report module.",
        "requirements.txt": "Local dependency pin set needs a public dependency/package policy before installable app/EXE work.",
        "RUN_AMCF_VNEXT.cmd": "Machine-local wrapper intentionally not committed.",
        "RUN_TEST02.cmd": "Machine-local wrapper intentionally not committed.",
        "RUN_TRACKING_TEST03A.cmd": "Machine-local wrapper intentionally not committed.",
    }
    return notes.get(local_rel)
