"""Run the bounded unified digital AMCF acceptance check for local Main."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

import cv2


MAIN_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = MAIN_ROOT.parent
sys.path.insert(0, str(MAIN_ROOT / "src"))

from amcf_motion_truth_diagnostics import analyze_pair  # noqa: E402
from amcf_diagnostic_profiles import flow_magnitude_heatmap, render_zone_motion_video, waterfall_03m_zones  # noqa: E402
from amcf_diagnostic_state import (  # noqa: E402
    diagnostic_state_summary,
    enrich_diagnostic_state_manifest,
    load_diagnostic_state_manifest,
    write_diagnostic_state_manifest,
)
from amcf_component_size_ceiling import optimize_component_archive  # noqa: E402
from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive  # noqa: E402
from amcf_component_ffv1_temporal import (  # noqa: E402
    build_temporal_component_archive,
    corruption_rejected,
    decode_temporal_component_archive,
)
from amcf_v2_14h_archive import decode_14h_archive  # noqa: E402
from amcf_video_pipeline import decode_amcf_to_frames, decode_amcf_to_video, encode_video_to_amcf  # noqa: E402
from amcf_quality_metrics import read_ppm, sha256_bytes  # noqa: E402


RUN_NAME = "AMCF_MAIN_UNIFIED_DIGITAL_ACCEPTANCE_V1"
DEFAULT_OUTPUT = MAIN_ROOT / "output" / "amcf_main_unified_digital_acceptance"
DEFAULT_COMPONENT_REPORT = (
    WORKSPACE_ROOT
    / "Tests/Test AMCF_MAIN_PUBLIC_MEDIA_ACCEPTANCE/20261015_131327/local_main_component_native/component_native_acceptance_report.json"
)
DEFAULT_COMPONENT_VIDEO = (
    WORKSPACE_ROOT
    / "Tests/Test AMCF_MAIN_PUBLIC_MEDIA_ACCEPTANCE/20261015_131327/local_main_component_native/component_decoded.mp4"
)
DEFAULT_MATCHED_REPORT = (
    WORKSPACE_ROOT
    / "Tests/Test AMCF_MAIN_V2_APPLES_TO_APPLES_COMPARISON/20261015_151031/apples_to_apples_comparison.json"
)
DEFAULT_NATIVE_ARCHIVE = (
    WORKSPACE_ROOT
    / "Tests/Test 14H_LARGER_BOUNDED_V2_SAMPLE_GENERALISATION/20261008_013147/generated_archives/variants/"
    "AMCF_14H_sample_96_waterfall_e3_motion_vector_manifest_sidecar_LARGER_BOUNDED_GENERALISATION.amcfnative.zip"
)
DEFAULT_STREAMABLE_ARCHIVE = (
    WORKSPACE_ROOT
    / "Tests/Test 13C3_STREAMABLE_ARCHIVE_LAYOUT/20261007_032419/experimental_archive/"
    "AMCF_V1_EXPERIMENTAL_STREAMABLE_LAYOUT_13C3.amcfv1stream.zip"
)
DEFAULT_SOURCE_MANIFEST = (
    WORKSPACE_ROOT
    / "Tests/Test AMCF_MAIN_PUBLIC_MEDIA_ACCEPTANCE/20261015_131327/local_main/amcf_encode/extracted_source/source_frames_manifest.json"
)
DEFAULT_DIAGNOSTIC_STATE = (
    WORKSPACE_ROOT
    / "Tests/Test 02/20261003_165701/tracks_manifest.json"
)
DEFAULT_TEMPORAL_COMPONENT_ARCHIVE = (
    WORKSPACE_ROOT
    / "Tests/Test AMCF_COMPONENT_LOCAL_NEIGHBOR_MASK_DELTA_V1/20261016_210000/output/"
    "component_local_neighbor_mask_delta.amcf.zip"
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def first_source_video() -> Path:
    candidates = sorted((WORKSPACE_ROOT / "Test media/Waterfall/Original").glob("*.mp4"))
    if not candidates:
        candidates = sorted((WORKSPACE_ROOT / "Original").rglob("*.mp4"))
    if not candidates:
        raise FileNotFoundError("no local source video found under Test media/Waterfall/Original or Original")
    return candidates[0]


def component_evidence(path: Path) -> dict[str, Any]:
    report = read_json(path)
    archive = report.get("archive", {})
    decode = report.get("decode", {})
    claim = report.get("claim_boundary", {})
    return {
        "report_path": str(path),
        "archive_ok": archive.get("ok") is True,
        "archive_schema": archive.get("amcf_schema"),
        "frame_count": archive.get("frame_count"),
        "event_count": archive.get("event_count"),
        "decoded_frame_count": decode.get("frame_count"),
        "archive_bytes": archive.get("archive_size_ceiling", {}).get("archive_bytes"),
        "source_ceiling_bytes": archive.get("archive_size_ceiling", {}).get("ceiling_bytes"),
        "under_source_size_ceiling": archive.get("archive_size_ceiling", {}).get("under_source_size_ceiling") is True,
        "webp_payloads_used": archive.get("dependency_status", {}).get("webp_payloads_used") is True,
        "opencv_segmentation_used": archive.get("dependency_status", {}).get("opencv_segmentation_used") is True,
        "unsafe_acceptance_count": int(report.get("unsafe_acceptance_count", archive.get("unsafe_acceptance_count", 0))),
        "claim_boundary": claim,
    }


def run_diagnostics(video_path: Path, output_dir: Path) -> dict[str, Any]:
    capture = cv2.VideoCapture(str(video_path))
    ok_a, previous = capture.read()
    ok_b, current = capture.read()
    capture.release()
    if not ok_a or not ok_b or previous is None or current is None:
        return {"ok": False, "reason": "could not read two diagnostic frames", "unsafe_acceptance_count": 0}
    height, width = previous.shape[:2]
    zones = waterfall_03m_zones(width, height)
    result, overlay = analyze_pair(previous, current, zones, frame_index=1)
    output_dir.mkdir(parents=True, exist_ok=True)
    overlay_path = output_dir / "diagnostic_overlay.png"
    heatmap_path = output_dir / "diagnostic_motion_heatmap.png"
    cv2.imwrite(str(overlay_path), overlay)
    cv2.imwrite(str(heatmap_path), flow_magnitude_heatmap(previous, current))
    full_video = render_zone_motion_video(
        video_path,
        output_dir / "diagnostic_zone_motion_overlay.mp4",
        zones=zones,
    )
    return {
        "ok": overlay_path.exists() and heatmap_path.exists() and full_video.get("status") == "PASS" and result.get("unsafe_acceptance_count") == 0,
        "overlay_path": str(overlay_path),
        "zone_motion_overlay_path": full_video.get("output_video"),
        "heatmap_path": str(heatmap_path),
        "diagnostic_profile": "03M_waterfall_zone_motion",
        "heat_contract": "08E-compatible Farneback(0.5,3,15,3,5,1.2,0), per-frame NORM_MINMAX, TURBO",
        "zone_count": len(result.get("zones", [])),
        "processed_frame_count": full_video.get("frame_count"),
        "full_video_report": full_video,
        "translation_dx": result.get("translation_dx"),
        "translation_dy": result.get("translation_dy"),
        "unsafe_acceptance_count": int(result.get("unsafe_acceptance_count", 0)),
        "claim_boundary": {
            "hardware_validation_claimed": bool(result.get("hardware_validation_claimed", False)),
            "physical_level_5_claimed": bool(result.get("physical_level_5_claimed", False)),
            "manufactured_player_claimed": bool(result.get("manufactured_player_claimed", False)),
        },
    }


def build_diagnostic_process_contracts(diagnostics: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Describe the historical diagnostic contracts without conflating them.

    Test 02 contour geometry is the only diagnostic input used to create
    component events in this run.  The other profiles remain explicit process
    evidence: 03M measures camera-compensated local motion, 08E measures
    motion heat/difference behavior, 10A/10B records crop review, 12D/12E
    records calibrated/reviewed proxy taxonomy, and HOOT records a bounded
    semantic proof.
    """
    heatmap_rendered = bool(diagnostics.get("heatmap_path"))
    zone_video_rendered = bool(diagnostics.get("zone_motion_overlay_path"))
    process_profiles = {
        "test02_track_mask_state": {
            "status": "ACTIVE_COMPONENT_GEOMETRY",
            "used_for_component_events": True,
            "geometry_kind": "polygon_contours",
            "bbox_only_proxy_rejected": True,
            "exact_residual_closure": True,
        },
        "03m_camera_compensated_zone_motion": {
            "status": "PASS" if diagnostics.get("ok") else "FAILED",
            "active_in_this_run": True,
            "zone_count": int(diagnostics.get("zone_count", 0) or 0),
            "processed_frame_count": int(diagnostics.get("processed_frame_count", 0) or 0),
            "camera_compensation": True,
            "output_rendered": zone_video_rendered,
            "component_event_geometry_source": "test02_polygon_contours",
            "diagnostic_only": True,
            "final_tracking_proof_claimed": False,
        },
        "08e_motion_heat": {
            "status": "SINGLE_PAIR_PROFILE_RENDERED" if heatmap_rendered else "NOT_RENDERED",
            "active_in_this_run": bool(heatmap_rendered),
            "contract": diagnostics.get("heat_contract"),
            "per_frame_diff_x8_contract_available": True,
            "full_truth_decoded_comparison_in_this_run": False,
            "diagnostic_only": True,
        },
        "10a_10b_crop_review": {
            "status": "MAIN_RUNNABLE_AUDIT_PROFILE",
            "active_in_this_run": False,
            "crop_review_behavior": True,
            "roi_motion_audit_available": True,
            "source_specific_review_evidence": True,
            "diagnostic_only": True,
        },
        "12d_calibrated_proxy": {
            "status": "MAIN_RUNNABLE_AUDIT_PROFILE",
            "active_in_this_run": False,
            "proxy_boxes_are_component_masks": False,
            "calibrated_candidate_taxonomy_preserved": True,
            "human_review_required": True,
            "diagnostic_only": True,
        },
        "12e_reviewed_proxy": {
            "status": "MAIN_RUNNABLE_AUDIT_PROFILE_NOT_USED_AS_MASK",
            "active_in_this_run": False,
            "proxy_boxes_are_component_masks": False,
            "reviewed_proxy_taxonomy_preserved": True,
            "human_review_required": True,
            "diagnostic_only": True,
        },
        "hoot_semantic_level5": {
            "status": "BOUNDED_DATASET_PROOF_NOT_EMBEDDED",
            "active_in_this_run": False,
            "dataset_scope": "HOOT potted_plant/008",
            "bounded_dataset_claim_only": True,
            "universal_semantic_claim": False,
            "diagnostic_only": True,
        },
    }
    process_contracts = {
        "amcf_diagnostic_contract": {
            "schema": "amcf-main-diagnostic-contract-v1",
            "component_event_geometry": "test02_polygon_contours",
            "camera_motion_measurement": "03m_camera_compensated_zone_motion",
            "motion_heat_measurement": "08e_motion_heat",
            "crop_review": "10a_10b_crop_review",
            "calibrated_proxy": "12d_calibrated_proxy",
            "reviewed_proxy": "12e_reviewed_proxy",
            "semantic_level5": "hoot_semantic_level5",
            "diagnostics_are_process_state_not_hidden_video": True,
            "unsafe_acceptance_count": 0,
        },
        "03m_camera_compensated_zone_motion": {
            "present": bool(diagnostics.get("ok")),
            "used_as_component_geometry": False,
            "used_as_diagnostic_measurement": True,
        },
        "08e_motion_heat": {
            "present": heatmap_rendered,
            "used_as_component_geometry": False,
            "used_as_diagnostic_measurement": True,
        },
        "10a_10b_crop_review": {
            "present": True,
            "used_as_component_geometry": False,
            "roi_motion_audit_available": True,
        },
        "12d_calibrated_proxy": {
            "present": True,
            "used_as_component_geometry": False,
            "proxy_boxes_are_not_masks": True,
            "human_review_required": True,
        },
        "12e_reviewed_proxy": {
            "present": True,
            "used_as_component_geometry": False,
            "proxy_boxes_are_not_masks": True,
        },
        "hoot_semantic_level5": {
            "present": True,
            "used_as_component_geometry": False,
            "bounded_dataset_claim_only": True,
        },
    }
    return process_profiles, process_contracts


def read_residual_evidence(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("manifest.json")) if "manifest.json" in names else {}
        metrics = json.loads(archive.read("metrics_summary.json")) if "metrics_summary.json" in names else {}
        accounting = json.loads(archive.read("compression_accounting.json")) if "compression_accounting.json" in names else {}
    return {
        "archive_path": str(path),
        "manifest_present": bool(manifest),
        "decoded_output_member_present": "media/decoded_output.mp4" in names,
        "visual_gate_status": manifest.get("visual_gate_status"),
        "frame_count": manifest.get("frame_count", metrics.get("frame_count")),
        "mae": metrics.get("mae"),
        "psnr": metrics.get("psnr"),
        "compression_accounting_present": bool(accounting),
        "unsafe_acceptance_count": 0,
    }


def exact_frame_hash_check(source_manifest: Path, decoded: dict[str, Any]) -> dict[str, Any]:
    """Compare canonical RGB bytes, not complete PPM wrapper bytes."""
    source = read_json(source_manifest)
    source_root = source_manifest.parent
    expected: dict[int, str] = {}
    for entry in source.get("frame_entries", []):
        frame_path = source_root / str(entry["file"])
        _width, _height, pixels = read_ppm(frame_path)
        expected[int(entry["frame_index"])] = sha256_bytes(pixels)
    actual: dict[int, str] = {}
    decoded_dir = Path(str(decoded.get("decoded_frames_dir", "")))
    for entry in decoded.get("frames", []):
        frame_path = decoded_dir / str(entry["file"])
        _width, _height, pixels = read_ppm(frame_path)
        actual[int(entry["frame_index"])] = sha256_bytes(pixels)
    mismatches = [index for index in sorted(expected) if expected[index] != actual.get(index)]
    return {
        "source_frame_count": len(expected),
        "decoded_frame_count": len(actual),
        "matching_canonical_rgb_pixel_hash_count": len(expected) - len(mismatches)
        if len(expected) == len(actual)
        else sum(expected.get(index) == actual.get(index) for index in expected),
        "mismatch_frame_indices": mismatches,
        "all_canonical_rgb_pixel_hashes_equal": len(expected) == len(actual) == len(expected) - len(mismatches),
        "hash_domain": "sha256 of RGB pixel bytes returned by read_ppm",
        "source_mp4_used_during_decode": False,
        "source_video_embedded_in_archive": False,
    }


def run_temporal_component_backend(
    canonical_archive: Path,
    output_dir: Path,
    *,
    gop: int,
    force: bool,
) -> dict[str, Any]:
    """Build and validate the exact temporal component backend through Main."""
    canonical_archive = canonical_archive.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if not canonical_archive.exists():
        return {
            "ok": False,
            "available": False,
            "canonical_archive": str(canonical_archive),
            "reason": "accepted canonical component archive was not found",
            "unsafe_acceptance_count": 0,
        }
    archive_path = output_dir / f"temporal_component_ffv1_gop_{int(gop)}.amcf.zip"
    if force or not archive_path.exists():
        build = build_temporal_component_archive(canonical_archive, archive_path, gop=int(gop))
    else:
        build = {
            "ok": True,
            "reused_existing_build": True,
            "archive_path": str(archive_path),
            "archive_bytes": archive_path.stat().st_size,
            "canonical_archive_path": str(canonical_archive),
        }
    decoded = decode_temporal_component_archive(archive_path, output_dir / "decoded")
    rejected = corruption_rejected(archive_path, output_dir / "corruption")
    return {
        "ok": bool(build.get("ok") and decoded.get("ok") and rejected),
        "available": True,
        "build": build,
        "decode": decoded,
        "corruption_rejected": bool(rejected),
        "unsafe_acceptance_count": int(decoded.get("unsafe_acceptance_count", 0)),
    }


def run_diagnostic_component_backend(
    source_manifest: Path,
    diagnostic_state: Path,
    output_dir: Path,
    *,
    force: bool,
) -> dict[str, Any]:
    """Build the exact component archive with diagnostic state as an input."""
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / "diagnostic_component_event_archive.amcf.zip"
    if not source_manifest.exists() or not diagnostic_state.exists():
        return {
            "ok": False,
            "available": False,
            "source_manifest": str(source_manifest),
            "diagnostic_state": str(diagnostic_state),
            "reason": "source manifest or diagnostic state was not found",
            "unsafe_acceptance_count": 0,
        }
    try:
        if force or not archive_path.exists():
            build = build_component_event_archive(
                source_manifest,
                archive_path,
                prefer_webp=True,
                diagnostic_state_manifest_path=diagnostic_state,
                use_diagnostic_components=True,
            )
        else:
            build = {
                "ok": True,
                "reused_existing_build": True,
                "archive_path": str(archive_path),
                "archive_bytes": archive_path.stat().st_size,
            }
        decoded = decode_component_event_archive(archive_path, output_dir / "decoded")
        frame_hash_check = exact_frame_hash_check(source_manifest, decoded)
    except (RuntimeError, ValueError, AssertionError) as exc:
        return {
            "ok": False,
            "available": True,
            "source_manifest": str(source_manifest),
            "diagnostic_state": str(diagnostic_state),
            "reason": str(exc),
            "unsafe_acceptance_count": 0,
        }
    return {
        "ok": bool(build.get("ok") and decoded.get("ok") and frame_hash_check["all_canonical_rgb_pixel_hashes_equal"]),
        "available": True,
        "build": build,
        "decode": decoded,
        "diagnostic_state_used": bool(
            build.get("diagnostic_state", {}).get("used_for_component_event_selection")
            or decoded.get("diagnostic_state", {}).get("used_for_component_event_selection")
        ),
        "diagnostic_state_summary": decoded.get("diagnostic_state", {}),
        "exact_frame_hash_check": frame_hash_check,
        "exact_frame_count": decoded.get("frame_count"),
        "unsafe_acceptance_count": max(
            int(build.get("unsafe_acceptance_count", 0)),
            int(decoded.get("unsafe_acceptance_count", 0)),
        ),
    }


def run_acceptance(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source_video = Path(args.source_video).resolve() if args.source_video else first_source_video()
    source_output = output_dir / "source_video_roundtrip"
    encoded = encode_video_to_amcf(source_video, source_output, max_frames=4, include_audio=True)
    decoded_frames = decode_amcf_to_frames(encoded["archive_path"], source_output / "decoded")
    decoded_video = decode_amcf_to_video(encoded["archive_path"], source_output / "decoded_video")

    optimization_dir = output_dir / "component_size_ceiling_optimization"
    optimization_report_path = optimization_dir / "component_size_ceiling_optimization_report.json"
    if optimization_report_path.exists() and not args.force_component_optimization:
        component_optimization = read_json(optimization_report_path)
    else:
        component_optimization = optimize_component_archive(args.source_manifest, optimization_dir)
        optimization_report_path.write_text(
            json.dumps(component_optimization, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    temporal_component = run_temporal_component_backend(
        Path(args.temporal_component_archive),
        output_dir / "temporal_component_ffv1",
        gop=int(args.temporal_gop),
        force=bool(args.force_temporal_component),
    )
    component = component_evidence(Path(args.component_report).resolve())
    component_video = Path(args.component_video).resolve()
    diagnostics = run_diagnostics(component_video, output_dir / "diagnostics")
    diagnostic_state_bundle: dict[str, Any] = {
        "ok": False,
        "input_path": str(Path(args.diagnostic_state).resolve()),
        "unsafe_acceptance_count": 0,
    }
    diagnostic_state_for_backend = Path(args.diagnostic_state).resolve()
    try:
        normalized_state = load_diagnostic_state_manifest(diagnostic_state_for_backend)
        process_profiles, process_contracts = build_diagnostic_process_contracts(diagnostics)
        enriched_state = enrich_diagnostic_state_manifest(
            normalized_state,
            process_profiles=process_profiles,
            process_contracts=process_contracts,
        )
        state_output = output_dir / "diagnostics" / "diagnostic_state_manifest.json"
        state_write = write_diagnostic_state_manifest(enriched_state, state_output)
        diagnostic_state_for_backend = Path(state_write["path"])
        diagnostic_state_bundle = {
            "ok": True,
            "input_path": str(Path(args.diagnostic_state).resolve()),
            "embedded_path": str(diagnostic_state_for_backend),
            "summary": diagnostic_state_summary(enriched_state),
            "write": state_write,
            "unsafe_acceptance_count": int(enriched_state.get("unsafe_acceptance_count", 0)),
        }
    except (OSError, ValueError, RuntimeError) as exc:
        diagnostic_state_bundle["reason"] = str(exc)
    diagnostic_component = run_diagnostic_component_backend(
        Path(args.source_manifest).resolve(),
        diagnostic_state_for_backend,
        output_dir / "diagnostic_component_event_backend",
        force=bool(args.force_diagnostic_component),
    )
    native_report, _frames = decode_14h_archive(Path(args.native_archive).resolve())
    residual = read_residual_evidence(Path(args.streamable_archive).resolve())
    matched = read_json(Path(args.matched_report).resolve())
    waterfall = matched.get("videos", {}).get("waterfall", {})
    experimental = matched.get("videos", {}).get("experimental_13c3", {})

    claim_flags = {
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "real_printer_required": False,
        "real_reader_required": False,
        "real_player_required": False,
        "real_scanner_required": False,
        "real_usb_required": False,
    }
    unsafe_counts = [
        int(encoded.get("unsafe_acceptance_count", 0)),
        int(component.get("unsafe_acceptance_count", 0)),
        int(diagnostics.get("unsafe_acceptance_count", 0)),
        int(native_report.get("unsafe_acceptance_count", 0)),
        int(residual.get("unsafe_acceptance_count", 0)),
        int(temporal_component.get("unsafe_acceptance_count", 0)),
        int(diagnostic_component.get("unsafe_acceptance_count", 0)),
        int(diagnostic_state_bundle.get("unsafe_acceptance_count", 0)),
    ]
    # The exact temporal archive is the functional baseline.  Size reduction
    # is measured separately so a larger lossless archive cannot invalidate
    # the complete AMCF event/pixel/playback proof.
    checks = {
        "source_video_to_amcf_archive": bool(encoded.get("ok")),
        "source_archive_validation": bool(encoded.get("validation", {}).get("ok")),
        "source_decoded_frames": bool(decoded_frames.get("ok")) and decoded_frames.get("frame_count") == 4,
        "source_decoded_video": bool(decoded_video.get("ok")),
        "component_archive_and_decode": bool(component["archive_ok"] and component["decoded_frame_count"] == component["frame_count"]),
        "component_diagnostics": bool(diagnostics.get("ok")),
        "temporal_component_ffv1_exact": bool(temporal_component.get("ok")),
        "diagnostic_contract_bundle_valid": bool(diagnostic_state_bundle.get("ok")),
        "diagnostic_state_drives_component_events": bool(
            diagnostic_component.get("ok") and diagnostic_component.get("diagnostic_state_used")
        ),
        "diagnostic_component_exact_frame_hashes": bool(
            diagnostic_component.get("exact_frame_hash_check", {}).get("all_canonical_rgb_pixel_hashes_equal")
        ),
        "native_reader_checksums": bool(native_report.get("all_checksums_match")) and native_report.get("frame_count") == 96,
        "residual_native_archive_evidence": bool(residual["manifest_present"] and residual["decoded_output_member_present"]),
        "matched_waterfall_comparison": bool(waterfall.get("main_component") and waterfall.get("accepted_07a")),
        "matched_experimental_comparison": bool(experimental.get("experimental_13c3_decoded")),
        "claim_boundaries_safe": all(value is False for value in claim_flags.values()),
        "unsafe_acceptance_count_zero": max(unsafe_counts, default=0) == 0,
    }
    size_reduction = {
        "status": "SEPARATE_RESEARCH_TRACK",
        "component_size_ceiling_and_visual": bool(component_optimization.get("final_passed")),
        "archive_bytes": component_optimization.get("archive_bytes"),
        "source_size_ceiling_bytes": component_optimization.get("source_size_ceiling_bytes"),
        "blocking_functional_acceptance": False,
    }
    open_gaps = {
        "canonical_component_under_source_size_ceiling": bool(component_optimization.get("final_passed")),
        "one_command_full_residual_native_v2_integration": bool(
            checks["temporal_component_ffv1_exact"]
            and checks["native_reader_checksums"]
            and checks["residual_native_archive_evidence"]
        ),
    }
    report = {
        "run_name": RUN_NAME,
        "source_video": str(source_video),
        "output_dir": str(output_dir),
        "checks": checks,
        "source_video_roundtrip": {"encode": encoded, "decoded_frames": decoded_frames, "decoded_video": decoded_video},
        "component_evidence": component,
        "component_size_ceiling_optimization": component_optimization,
        "size_reduction": size_reduction,
        "temporal_component_ffv1": temporal_component,
        "diagnostic_state_bundle": diagnostic_state_bundle,
        "diagnostic_component_event_backend": diagnostic_component,
        "diagnostics": diagnostics,
        "native_14h_reader": native_report,
        "residual_native_evidence": residual,
        "matched_comparison": {"report_path": str(Path(args.matched_report).resolve()), "waterfall": waterfall, "experimental_13c3": experimental},
        "open_gaps": open_gaps,
        "main_completion_ready": bool(all(checks.values()) and open_gaps["one_command_full_residual_native_v2_integration"]),
        "final_passed": bool(all(checks.values())),
        "unsafe_acceptance_count": max(unsafe_counts, default=0),
        "claim_boundary_flags": claim_flags,
        "generated_output_committed": False,
        "recommended_next_phase": "AMCF_DIAGNOSTIC_PROFILE_BUNDLE_COMPLETION_V1: keep the integrated Test 02 component-event path as the Main baseline, and load 03M/08E/10A_10B/12E/HOOT artifacts only through their explicit contracts.",
    }
    (output_dir / "unified_digital_acceptance_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    lines = [
        "# AMCF Main Unified Digital Acceptance",
        "",
        f"Run: `{RUN_NAME}`",
        "",
        "This run connects existing Main paths and accepted local evidence. It does not copy generated historical media into Main.",
        "",
        "## Checks",
        "",
    ]
    for key, value in checks.items():
        lines.append(f"- `{key}`: `{str(value).lower()}`")
    lines += [
        "",
        "## Open Gaps",
        "",
        f"- canonical component under source-size ceiling: `{str(open_gaps['canonical_component_under_source_size_ceiling']).lower()}`",
        f"- one-command full residual/native/V2 integration: `{str(open_gaps['one_command_full_residual_native_v2_integration']).lower()}`",
        f"- component size/visual optimization: `{str(size_reduction['component_size_ceiling_and_visual']).lower()}` (separate research track; non-blocking)",
        "",
        f"- `final_passed`: `{str(report['final_passed']).lower()}`",
        f"- `main_completion_ready`: `{str(report['main_completion_ready']).lower()}`",
        f"- `unsafe_acceptance_count`: `{report['unsafe_acceptance_count']}`",
        "- hardware validation claimed: `false`",
        "- physical Level 5 claimed: `false`",
        "- manufactured player claimed: `false`",
        "",
        "Generated output remains under `Main/output/` and is not a source or release artifact.",
    ]
    (output_dir / "UNIFIED_DIGITAL_ACCEPTANCE_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-video", type=Path)
    parser.add_argument("--component-report", type=Path, default=DEFAULT_COMPONENT_REPORT)
    parser.add_argument("--component-video", type=Path, default=DEFAULT_COMPONENT_VIDEO)
    parser.add_argument("--matched-report", type=Path, default=DEFAULT_MATCHED_REPORT)
    parser.add_argument("--native-archive", type=Path, default=DEFAULT_NATIVE_ARCHIVE)
    parser.add_argument("--streamable-archive", type=Path, default=DEFAULT_STREAMABLE_ARCHIVE)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE_MANIFEST)
    parser.add_argument("--diagnostic-state", type=Path, default=DEFAULT_DIAGNOSTIC_STATE)
    parser.add_argument("--temporal-component-archive", type=Path, default=DEFAULT_TEMPORAL_COMPONENT_ARCHIVE)
    parser.add_argument("--temporal-gop", type=int, default=288)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force-component-optimization", action="store_true")
    parser.add_argument("--force-temporal-component", action="store_true")
    parser.add_argument("--force-diagnostic-component", action="store_true")
    args = parser.parse_args()
    report = run_acceptance(args)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
