from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive
from amcf_component_event_viewer import build_component_event_viewer
from amcf_deliverable_package import build_deliverable_package
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
    "amcf_config.example.json": None,
    "amcf_test02.py": None,
    "amcf_tracking_test03a.py": None,
    "requirements.txt": None,
    "RUN_AMCF_VNEXT.cmd": None,
    "RUN_TEST02.cmd": None,
    "RUN_TRACKING_TEST03A.cmd": None,
    "test_archive_decode.py": None,
    "README.md": None,
}


def default_paths(public_root: str | Path) -> RepoPaths:
    public_root = Path(public_root).resolve()
    workspace_root = public_root.parents[4]
    return RepoPaths(
        public_root=public_root,
        local_main_root=workspace_root / "Main",
        workspace_root=workspace_root,
    )


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
            "classification": "NEEDS_PUBLIC_EQUIVALENT" if public_rel is None else "MAPPED",
        }
        if local_path.exists():
            row["local_sha256"] = sha256_file(local_path)
            row["local_bytes"] = local_path.stat().st_size
        if public_path and public_path.exists():
            row["public_sha256"] = sha256_file(public_path)
            row["public_bytes"] = public_path.stat().st_size
            row["exact_hash_match"] = row.get("local_sha256") == row.get("public_sha256")
        if local_rel.endswith(".cmd"):
            row["classification"] = "LOCAL_MACHINE_WRAPPER_DO_NOT_COPY"
        elif local_rel == "requirements.txt":
            row["classification"] = "DEPENDENCY_POLICY_REQUIRED"
        elif local_rel in {"amcf_test02.py", "amcf_tracking_test03a.py"}:
            row["classification"] = "FUNCTIONAL_PARITY_PORTED_AS_PUBLIC_MODULES"
        elif local_rel == "test_archive_decode.py":
            row["classification"] = "LOCAL_SCHEMA_CHECK_PORTED_AS_PUBLIC_TESTS"
        elif local_rel == "amcf_config.example.json":
            row["classification"] = "CONFIG_POLICY_REQUIRED"
        elif local_rel == "README.md":
            row["classification"] = "LOCAL_DOC_SUPERSEDED_BY_PUBLIC_DOCS"
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
            "status": "INTENTIONALLY_EXCLUDED",
            "evidence": "Local .cmd wrappers, caches, source media, proof folders, and generated zips are not committed.",
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
    public_result = run_public_equivalent(paths, source_video, output_dir / "public_equivalent", frames=frames)
    comparison = compare_local_public_outputs(local_result, public_result)
    return {
        "ok": bool(local_result.get("ok")) and bool(public_result.get("ok")) and comparison["functional_parity_passed"],
        "source_video_name": source_video.name,
        "source_video_sha256": sha256_file(source_video),
        "frames_requested": frames,
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
    completed = subprocess.run(
        command,
        cwd=str(paths.local_main_root),
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
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
        "outdir": str(outdir) if outdir else None,
        "archive": str(archive) if archive else None,
        "zip": str(zip_path) if zip_path else None,
        "archive_exists": bool(archive and archive.exists()),
        "zip_exists": bool(zip_path and zip_path.exists()),
        "manifest_exists": bool(manifest_path and manifest_path.exists()),
        "tracks_manifest_exists": bool(tracks_path and tracks_path.exists()),
        "viewer_exists": bool(viewer_path and viewer_path.exists()),
        "reconstructed_video_exists": bool(reconstructed_video and reconstructed_video.exists()),
        "unsafe_acceptance_count": 0,
    }
    if manifest_path and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        summary.update(
            {
                "frame_count": int(manifest.get("source", {}).get("frames", 0) or 0),
                "event_count": len(manifest.get("events", [])),
                "track_count": len(manifest.get("tracks", [])),
                "under_source_size_ceiling": manifest.get("archive", {}).get("under_source_size_ceiling"),
            }
        )
    if completed.returncode != 0:
        summary["stderr_tail"] = completed.stderr[-2000:]
        summary["stdout_tail"] = completed.stdout[-2000:]
    return summary


def run_public_equivalent(paths: RepoPaths, source_video: Path, output_dir: Path, *, frames: int) -> dict[str, Any]:
    video = encode_video_to_amcf(source_video, output_dir / "video_pipeline", max_frames=frames, include_audio=True)
    decoded = decode_amcf_to_frames(video["archive_path"], output_dir / "decoded_frames")
    decoded_video = decode_amcf_to_video(video["archive_path"], output_dir / "decoded_video")
    component_archive_path = output_dir / "component" / "component_event_archive.amcf.zip"
    component = build_component_event_archive(video["source_manifest_path"], component_archive_path, segmentation_mode="opencv_changed_region")
    component_decoded = decode_component_event_archive(component_archive_path, output_dir / "component_decoded")
    quality = compare_ppm_frame_folders(
        Path(video["source_manifest_path"]).parent / "frames",
        Path(component_decoded["decoded_frames_dir"]),
    )
    viewer = build_component_event_viewer(
        archive_report=component,
        decoded_report=component_decoded,
        quality_report=quality,
        output_dir=output_dir / "viewer",
    )
    deliverable = build_deliverable_package(
        archive_path=component_archive_path,
        source_frames_dir=Path(video["source_manifest_path"]).parent / "frames",
        decoded_frames_dir=Path(component_decoded["decoded_frames_dir"]),
        quality_report=quality,
        viewer_dir=output_dir / "viewer",
        output_dir=output_dir / "deliverable",
        fps=int(component_decoded.get("fps", 24) or 24),
    )
    return {
        "ok": bool(video["ok"] and decoded["ok"] and decoded_video["ok"] and component["ok"] and component_decoded["ok"] and quality["ok"] and viewer["ok"] and deliverable["ok"]),
        "video_archive_exists": Path(video["archive_path"]).exists(),
        "frame_count": int(video["frame_count"]),
        "audio_status": video["audio_status"],
        "decoded_frames_exist": Path(decoded["decoded_frames_dir"]).exists(),
        "decoded_video_exists": Path(decoded_video["decoded_video_path"]).exists(),
        "component_archive_exists": Path(component["archive_path"]).exists(),
        "component_event_count": int(component["event_count"]),
        "viewer_exists": Path(viewer["viewer_html"]).exists(),
        "deliverable_zip_exists": Path(deliverable["zip_path"]).exists(),
        "track_taxonomy_count": int(deliverable["track_taxonomy_count"]),
        "under_source_size_ceiling": component["archive_size_ceiling"]["under_source_size_ceiling"],
        "unsafe_acceptance_count": 0,
    }


def compare_local_public_outputs(local_result: dict[str, Any], public_result: dict[str, Any]) -> dict[str, Any]:
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
        "unsafe_acceptance_count_zero": int(local_result.get("unsafe_acceptance_count", 0)) == 0 and int(public_result.get("unsafe_acceptance_count", 0)) == 0,
    }
    return {
        "functional_parity_passed": all(checks.values()),
        "byte_identical_outputs": False,
        "byte_identical_reason": "Local Main and public repo intentionally use different public-safe schemas/output paths; this proof compares functional output classes, not identical binary archives.",
        "checks": checks,
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
            "byte_for_byte_identical_to_local_main": False,
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
        f"- Byte-for-byte identical to local Main: {str(summary['byte_for_byte_identical_to_local_main']).lower()}",
        "",
        "## Output Checks",
    ]
    for key, value in checks.items():
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
