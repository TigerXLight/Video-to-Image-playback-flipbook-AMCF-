"""Run the maintained AMCF diagnostic profiles as one coverage audit.

This is an evidence/audit runner, not an archive encoder. It keeps the
historical diagnostic classes together while preserving their boundaries:
Test 02 contours are component geometry; zones, heat, crops, and proxy boxes
remain process diagnostics.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Callable


MAIN_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = MAIN_ROOT.parent
sys.path.insert(0, str(MAIN_ROOT / "src"))

from amcf_diagnostic_profiles import (  # noqa: E402
    render_03m_motion_truth_family,
    render_motion_heat_comparison_video,
    render_12b_water_object_candidate_video,
    render_reviewed_proxy_video,
    render_roi_comparison_video,
)


def _path(root: Path, value: str) -> Path:
    candidate = Path(value)
    return candidate if candidate.is_absolute() else root / candidate


def _run_profile(name: str, callback: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    try:
        report = callback()
        return {"name": name, **report}
    except Exception as exc:  # pragma: no cover - defensive campaign boundary
        return {
            "name": name,
            "status": "ERROR",
            "error": f"{type(exc).__name__}: {exc}",
            "unsafe_acceptance_count": 0,
        }


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# AMCF Diagnostic Coverage Audit",
        "",
        "This report runs the maintained diagnostic profiles against the local accepted evidence. It does not copy generated media into source or release files.",
        "",
        "## Result",
        "",
        f"- Profile renders pass: `{report['profile_renders_pass']}`",
        f"- Core diagnostic classes runnable from Main: `{report['core_diagnostic_classes_runnable']}`",
        f"- Confirmed right-to-left person behaviour: `{report['proxy_question']['confirmed_right_to_left_person_behaviour']}`",
        f"- 12B leftward person/object candidates: `{report['proxy_question']['12b_leftward_person_object_candidates']}`",
        f"- 12D leftward candidate tracks: `{report['proxy_question']['calibrated_leftward_candidate_tracks']}`",
        f"- 12E reviewed leftward person tracks: `{report['proxy_question']['reviewed_leftward_person_tracks']}`",
        f"- Semantic correctness claimed: `{report['proxy_question']['semantic_correctness_claimed']}`",
        f"- `unsafe_acceptance_count`: `{report['unsafe_acceptance_count']}`",
        "",
        "## Profile Matrix",
        "",
        "| Profile | Status | Human review | Diagnostic boundary |",
        "|---|---|---:|---|",
    ]
    for row in report["profiles"]:
        name = row["name"]
        status = row.get("status", "UNKNOWN")
        review = row.get("human_review_required", "n/a")
        boundary = {
            "03M_motion_truth_family": "raw motion, camera compensation, residual mask, zones, coverage, vectors, missing regions",
            "08E_motion_heat": "Farneback/TURBO heat and diff x8; not a mask",
            "10A_third_water_roi": "truth/fullrate/selected/diff crop and motion audit",
            "10B_fourth_people_roi": "truth/fullrate/selected/diff crop and motion audit",
            "12B_semantic_proxy_candidates": "original green object/orange fluid proxy boxes; not semantic truth or masks",
            "12D_calibrated_proxy": "candidate proxy boxes; not semantic truth or masks",
            "12E_reviewed_proxy": "human-reviewed proxy taxonomy; boxes are not masks",
        }.get(name, "process diagnostic")
        lines.append(f"| `{name}` | `{status}` | `{review}` | {boundary} |")
    lines.extend(
        [
            "",
            "## What Is Covered",
            "",
            "- Test 02 track/mask/contour/optical-flow state is the only diagnostic geometry allowed to drive component events.",
            "- 03M raw screen motion, camera registration, green residual zone motion, residual mask, component coverage, camera vectors, and missing-region views are rendered from Main.",
            "- 08E motion heat, optical-flow comparison, and `diff x8` behavior are rendered from Main.",
            "- 10A/10B crop review and ROI motion ratios are now rendered from Main.",
            "- 12B green object/orange fluid proxy behavior is rendered from the original 12B manifest; boxes remain diagnostic candidates, not masks.",
            "- 12D calibrated proxy labels and 12E reviewed proxy labels are both accepted as schema inputs and rendered without treating boxes as masks.",
            "- HOOT remains a bounded semantic evidence profile; it is not silently upgraded to universal semantic tracking.",
            "",
            "## Still Open",
            "",
            "- 12B has leftward person/object candidates, but its own contract calls them proxy IDs; 12E review does not confirm a right-to-left person track.",
            "- Historical 03A-03Z videos remain source-specific evidence, not one byte-identical Main renderer for every old experiment.",
            "- Physical PC-to-reader/player diagnostics remain a separate physical/software branch and do not replace digital AMCF acceptance.",
            "- The installable CLI is validated separately; the Windows EXE and GitHub parity remain subsequent packaging steps.",
            "",
            "## Claim Boundary",
            "",
            "The audit proves that the diagnostic classes can be run and measured through Main. It does not claim semantic object correctness for every candidate, physical hardware validation, or compact archive size.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=MAIN_ROOT / "output" / "amcf_diagnostic_coverage_audit_20261020")
    parser.add_argument(
        "--component-video",
        type=Path,
        default=WORKSPACE_ROOT / "Tests/Test AMCF_MAIN_PUBLIC_MEDIA_ACCEPTANCE/20261015_131327/local_main_component_native/component_decoded.mp4",
    )
    parser.add_argument(
        "--truth-video",
        type=Path,
        default=WORKSPACE_ROOT / "Tests/Test 07A/20261006_021146/baseline_downscale/ORIGINAL_TRUTH_640x320_23p976.mp4",
    )
    parser.add_argument(
        "--timelapse-video",
        type=Path,
        default=WORKSPACE_ROOT / "Original/River side boat ride timelapse stock video clip no copyright/River side boat ride timelapse stock video clip no copyright (720p_30fps_H264-128kbit_AAC).mp4",
    )
    parser.add_argument(
        "--diagnostic-state",
        type=Path,
        default=MAIN_ROOT / "output/amcf_diagnostic_state_component_archive_288_v2/diagnostics/diagnostic_state_manifest.json",
        help="Optional normalized Test 02 state used only for component-coverage rendering.",
    )
    parser.add_argument("--force", action="store_true", help="overwrite the audit output files")
    args = parser.parse_args()

    output_dir = args.output_dir if args.output_dir.is_absolute() else WORKSPACE_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    component_video = args.component_video if args.component_video.is_absolute() else WORKSPACE_ROOT / args.component_video
    truth_video = args.truth_video if args.truth_video.is_absolute() else WORKSPACE_ROOT / args.truth_video
    timelapse_video = args.timelapse_video if args.timelapse_video.is_absolute() else WORKSPACE_ROOT / args.timelapse_video
    diagnostic_state = args.diagnostic_state if args.diagnostic_state.is_absolute() else WORKSPACE_ROOT / args.diagnostic_state
    if not diagnostic_state.exists():
        diagnostic_state = None

    third_root = WORKSPACE_ROOT / "Tests/Test 10A_10B/20261006_152506"
    third_truth = third_root / "third_truth_baseline/THIRD_TRUTH_640x360_OR_MATCHED_10A.mp4"
    third_selected = third_root / "third_candidates/iteration_01_accepted_07G_tile_residual_keyframe_interval_long/candidate.mp4"
    third_fullrate = third_root / "third_fullrate_control/third_fullrate_microcomponent_control_10A.mp4"
    fourth_truth = third_root / "fourth_truth_baseline/FOURTH_TRUTH_640x360_OR_MATCHED_10B.mp4"
    fourth_selected = third_root / "fourth_candidates/iteration_01_accepted_07G_tile_residual_keyframe_interval_long/candidate.mp4"
    fourth_fullrate = third_root / "fourth_fullrate_control/fourth_fullrate_microcomponent_control_10B.mp4"
    manifest_12d = WORKSPACE_ROOT / "Tests/Test 12D/20261006_172244/imported_12c/calibrated_proxy_tracks_12C.json"
    manifest_12e = WORKSPACE_ROOT / "Tests/Test 12E/20261006_181534/reviewed_tracks/reviewed_proxy_tracks_12E.json"
    manifest_12b = WORKSPACE_ROOT / "Tests/Test 12B/20261006_164238/proxy_tracks/proxy_tracks_12B.json"
    proposals_12b = WORKSPACE_ROOT / "Tests/Test 12B/20261006_164238/region_proposals/region_proposals_12B.json"
    source_12b = WORKSPACE_ROOT / "Tests/Test 12B/20261006_164238/semantic_inputs/FOURTH_TRUTH_BASELINE_INPUT_12B.mp4"

    profiles = [
        _run_profile(
            "03M_motion_truth_family",
            lambda: render_03m_motion_truth_family(
                component_video,
                output_dir,
                diagnostic_state_manifest=diagnostic_state,
            ),
        ),
        _run_profile(
            "08E_motion_heat",
            lambda: render_motion_heat_comparison_video(truth_video, component_video, output_dir / "08e_motion_heat.mp4"),
        ),
        _run_profile(
            "10A_third_water_roi",
            lambda: render_roi_comparison_video(
                third_truth,
                third_selected,
                output_dir / "10a_third_water_roi.mp4",
                roi_profile="third-water",
                fullrate_video=third_fullrate,
            ),
        ),
        _run_profile(
            "10B_fourth_people_roi",
            lambda: render_roi_comparison_video(
                fourth_truth,
                fourth_selected,
                output_dir / "10b_fourth_people_roi.mp4",
                roi_profile="fourth-people",
                fullrate_video=fourth_fullrate,
            ),
        ),
        _run_profile(
            "12B_semantic_proxy_candidates",
            lambda: render_12b_water_object_candidate_video(
                source_12b,
                proposals_12b,
                manifest_12b,
                output_dir / "12b_semantic_proxy_candidates.mp4",
            ),
        ),
        _run_profile(
            "12D_calibrated_proxy",
            lambda: render_reviewed_proxy_video(
                timelapse_video,
                manifest_12d,
                output_dir / "12d_calibrated_proxy.mp4",
                profile_name="12D_calibrated_semantic_proxy",
            ),
        ),
        _run_profile(
            "12E_reviewed_proxy",
            lambda: render_reviewed_proxy_video(
                timelapse_video,
                manifest_12e,
                output_dir / "12e_reviewed_proxy.mp4",
                profile_name="12E_reviewed_timelapse_proxy",
            ),
        ),
    ]
    profile_renders_pass = all(row.get("status") == "PASS" for row in profiles)
    proxy_12d = next(row for row in profiles if row["name"] == "12D_calibrated_proxy")
    proxy_12e = next(row for row in profiles if row["name"] == "12E_reviewed_proxy")
    proxy_12b = next(row for row in profiles if row["name"] == "12B_semantic_proxy_candidates")
    audit_12b = proxy_12b.get("motion_audit", {})
    audit_12d = proxy_12d.get("motion_audit", {})
    audit_12e = proxy_12e.get("motion_audit", {})
    report = {
        "schema": "amcf-diagnostic-coverage-audit-v1",
        "output_dir": str(output_dir),
        "profiles": profiles,
        "profile_renders_pass": profile_renders_pass,
        "core_diagnostic_classes_runnable": profile_renders_pass,
        "proxy_question": {
            "12b_leftward_person_object_candidates": int(
                audit_12b.get("by_label", {}).get("person_or_moving_object", {}).get("leftward", 0)
            ),
            "calibrated_leftward_candidate_tracks": int(
                audit_12d.get("by_label", {}).get("person_or_moving_object", {}).get("leftward", 0)
            ),
            "reviewed_leftward_person_tracks": int(audit_12e.get("reviewed_person_or_moving_object_leftward_count", 0)),
            "confirmed_right_to_left_person_behaviour": bool(
                audit_12e.get("right_to_left_person_behavior_proven", False)
            ),
            "semantic_correctness_claimed": bool(audit_12d.get("semantic_correctness_proven", False))
            or bool(audit_12e.get("semantic_correctness_proven", False)),
            "interpretation": "12B contains leftward person/object proxy candidates; 03M designates camera-compensated motion zones; 12E reviewed evidence does not confirm a right-to-left person identity.",
        },
        "component_geometry_boundary": "Test 02 polygon contours only; 03M/08E/10A_10B/12B/12D/12E remain diagnostics, not masks.",
        "hoot_status": "BOUNDED_DATASET_EVIDENCE_ONLY",
        "physical_branch_status": "SEPARATE_NO_HARDWARE_CLAIM",
        "unsafe_acceptance_count": max(int(row.get("unsafe_acceptance_count", 0)) for row in profiles),
    }
    json_path = output_dir / "diagnostic_coverage_report.json"
    md_path = output_dir / "DIAGNOSTIC_COVERAGE_REPORT.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_markdown(md_path, report)
    print(json.dumps({"ok": profile_renders_pass, "json": str(json_path), "markdown": str(md_path)}, indent=2))
    return 0 if profile_renders_pass and report["unsafe_acceptance_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
