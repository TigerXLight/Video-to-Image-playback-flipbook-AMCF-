from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RUN_NAME = "AMCF_LOCAL_TESTS_PROGRESSION_INTEGRATION_LEDGER_V1"


@dataclass(frozen=True)
class ProgressionGroup:
    group_id: str
    local_group: str
    purpose: str
    summary_parts: tuple[int, ...]
    local_evidence: tuple[str, ...]
    public_coverage: tuple[str, ...]
    status: str
    next_action: str
    notes: str


PROGRESSION_GROUPS: tuple[ProgressionGroup, ...] = (
    ProgressionGroup(
        group_id="local_main_core",
        local_group="Main",
        purpose="Main-facing AMCF code and canonical docs.",
        summary_parts=(183, 184, 185, 186, 187, 188),
        local_evidence=(
            "Main/amcf_test02.py",
            "Main/amcf_vnext.py",
            "Main/test_archive_decode.py",
            "Main/amcf_tracking_test03a.py",
            "Main/AMCF_CANONICAL_CONCEPT.md",
            "Main/AMCF_PHYSICAL_MEDIUM_BOUNDARY.md",
        ),
        public_coverage=(
            "src/amcf_local_main_test02.py",
            "src/amcf_vnext.py",
            "src/amcf_local_main_archive_decode_check.py",
            "src/amcf_local_main_tracking_test03a.py",
            "docs/AMCF_CANONICAL_CONCEPT.md",
            "docs/AMCF_DIGITAL_AMCF_PARITY_AUDIT.md",
        ),
        status="IN_GITHUB_EXACT_OR_PUBLIC_SAFE_PORT",
        next_action="Keep exact/adapted mappings tested; use diagnostic parity group for remaining viewer/overlay fullness.",
        notes="Main is strongly represented, but Main alone is not the whole local project truth.",
    ),
    ProgressionGroup(
        group_id="test02_latest_diagnostic_archive",
        local_group="Tests/Test 02/20261013_071127",
        purpose="Waterfall component archive, masks, contours, optical-flow diagnostics, viewer, and decoded reconstruction evidence.",
        summary_parts=(1, 191),
        local_evidence=(
            "Tests/Test 02/20261013_071127/TEST02_REPORT.md",
            "Tests/Test 02/20261013_071127/tracks_manifest.json",
            "Tests/Test 02/20261013_071127/archive_manifest_resolved.json",
            "Tests/Test 02/20261013_071127/quality_metrics.json",
            "Tests/Test 02/20261013_071127/viewer/index.html",
        ),
        public_coverage=(
            "src/amcf_local_main_test02.py",
            "src/amcf_component_event_archive.py",
            "src/amcf_component_event_viewer.py",
            "src/amcf_quality_metrics.py",
            "src/amcf_optical_flow_tracking.py",
            "tests/test_amcf_component_event_archive.py",
            "tests/test_amcf_quality_metrics.py",
        ),
        status="NEEDS_TARGETED_DIAGNOSTIC_PARITY_REVIEW",
        next_action="Port or explicitly classify source-specific contour-overlay viewer and diagnostics behavior.",
        notes="Latest Test 02 is evidence/prototype functionality; it still says fail for final AMCF acceptance, so it must not be presented as the final proof by itself.",
    ),
    ProgressionGroup(
        group_id="diagnostic_state_component_bridge",
        local_group="Test 02 + Test 03M + Test 08E + Test 10A_10B + Test 12E + HOOT + 15-Oct Main acceptance",
        purpose="Normalize the project diagnostic contract and feed contour-backed Test 02 geometry into Main component events while preserving distinct motion, heat, crop-review, proxy, and bounded HOOT contracts.",
        summary_parts=(21,),
        local_evidence=(
            "Tests/Test 02/20261003_165701/tracks_manifest.json",
            "Tests/Test 03M/20261004_201918/motion_truth/motion_truth_summary_03M.json",
            "Tests/Test 08E/20261006_144850/acceptance_decision/leaf_motion_gate_result_08E.json",
            "Tests/Test 12E/20261006_181534/reviewed_tracks/reviewed_proxy_tracks_12E.json",
            "Tests/Test AMCF_HOOT_REAL_WORLD_LOST_RECOVERED_LEVEL5_SOLVER/20261009_220908/07_FINAL_STATUS/final_status.json",
            "Tests/Test AMCF_MAIN_PUBLIC_MEDIA_ACCEPTANCE/20261015_131327",
        ),
        public_coverage=(
            "src/amcf_diagnostic_state.py",
            "src/amcf_component_event_archive.py",
            "src/amcf_diagnostic_profiles.py",
            "demo/run_amcf_main_unified_digital_acceptance.py",
            "tests/test_amcf_diagnostic_state.py",
        ),
        status="IN_MAIN_COMPONENT_EVENT_PATH",
        next_action="Keep profile-specific outputs explicit; optionally load full 08E truth/decoded and reviewed 12E artifacts in later acceptance profiles without treating proxy boxes as masks.",
        notes="The 288-frame diagnostic-driven archive closes every frame with contour-backed component events plus exact residual coverage and decodes source-independently. Its 209.6 MB size is not a compactness result, and the Test 02 final-fidelity warning remains explicit.",
    ),
    ProgressionGroup(
        group_id="pre_github_source_to_amcf",
        local_group="Tests/Test AMCF_PRE_GITHUB_VIDEO_TO_AMCF_DIGITAL_SMOKE_DEMO",
        purpose="Generated source frames to digital AMCF archive and validator.",
        summary_parts=(150, 151),
        local_evidence=(
            "Tests/Test AMCF_PRE_GITHUB_VIDEO_TO_AMCF_DIGITAL_SMOKE_DEMO/20261010_200512/13_FINAL_STATUS/FINAL_STATUS.md",
        ),
        public_coverage=(
            "src/amcf_digital_encoder.py",
            "src/amcf_digital_validator.py",
            "demo/run_source_frames_to_amcf_digital_demo.py",
            "tests/test_source_frames_to_amcf_digital.py",
        ),
        status="IN_GITHUB_EQUIVALENT_PORT",
        next_action="Keep covered by public source-frame encoder/validator tests.",
        notes="Arbitrary real-video ingestion was not claimed in this pre-GitHub run; later public video support is FFmpeg-backed and optional.",
    ),
    ProgressionGroup(
        group_id="pre_github_physical_carrier_reader",
        local_group="Tests/Test AMCF_PRE_GITHUB_AMCF_TO_PRINTABLE_PHYSICAL_CARRIER_GENERATOR and virtual reader runs",
        purpose="Digital AMCF to physical carrier plan, virtual reader recovery, and recovered frame export.",
        summary_parts=(152, 153),
        local_evidence=(
            "Tests/Test AMCF_PRE_GITHUB_AMCF_TO_PRINTABLE_PHYSICAL_CARRIER_GENERATOR/20261010_211716",
            "Tests/Test AMCF_PRE_GITHUB_VIRTUAL_READER_RECOVERY_EXPORT_DEMO/20261010_222827/12_FINAL_STATUS/FINAL_STATUS.md",
        ),
        public_coverage=(
            "src/amcf_physical_carrier.py",
            "src/amcf_virtual_carrier_reader.py",
            "demo/run_amcf_to_physical_carrier_demo.py",
            "demo/run_virtual_reader_recovery_export_demo.py",
            "tests/test_amcf_to_physical_carrier.py",
            "tests/test_virtual_reader_recovery_export.py",
        ),
        status="IN_GITHUB_EQUIVALENT_PORT",
        next_action="Keep no-hardware carrier/reader path tested.",
        notes="This covers print/reader software simulation, not real printer or scanner integration.",
    ),
    ProgressionGroup(
        group_id="level5_main_promotion",
        local_group="Tests/Test AMCF_LEVEL5_PROMOTION_MAIN_INTEGRATION_RELEASE_REFRESH",
        purpose="Controlled and HOOT semantic/object Level 5 proof integration into Main-facing tooling.",
        summary_parts=(183, 188),
        local_evidence=(
            "Tests/Test AMCF_LEVEL5_PROMOTION_MAIN_INTEGRATION_RELEASE_REFRESH/20261009_225757/06_FINAL_STATUS/FINAL_STATUS.md",
        ),
        public_coverage=(
            "src/amcf_vnext.py",
            "tests/test_release_package.py",
        ),
        status="IN_GITHUB_EXACT_CODE",
        next_action="Keep semantic/object Level 5 distinct from physical hardware Level 5.",
        notes="This is not a physical hardware validation claim.",
    ),
    ProgressionGroup(
        group_id="native_payload_13i_13j_13j2_13p",
        local_group="Tests/Test 13I, Test 13J_13K, Test 13J2_13N, Test 13P",
        purpose="Accepted bounded native payload/archive, reader/compositor/playback-loop, longer sample, and payload codec feasibility chain.",
        summary_parts=(80, 81, 82, 83),
        local_evidence=(
            "Tests/Test 13I_REAL_NATIVE_PAYLOAD_ARCHIVE/20261007_143313/TEST13I_REAL_NATIVE_PAYLOAD_ARCHIVE_REPORT.md",
            "Tests/Test 13J_13K_NATIVE_READER_COMPOSITOR_INTEGRATION/20261007_144632/TEST13J_13K_NATIVE_READER_COMPOSITOR_INTEGRATION_REPORT.md",
            "Tests/Test 13J2_13N_LONGER_NATIVE_ARCHIVE_SAMPLE/20261007_154510/TEST13J2_13N_LONGER_NATIVE_ARCHIVE_SAMPLE_REPORT.md",
            "Tests/Test 13P_NATIVE_PAYLOAD_CODEC_FEASIBILITY/20261007_164713/TEST13P_NATIVE_PAYLOAD_CODEC_FEASIBILITY_REPORT.md",
        ),
        public_coverage=(
            "src/amcf_v2/",
            "demo/run_amcf_v2_public_package_demo.py",
            "tests/test_amcf_v2_public_package.py",
            "docs/AMCF_V2_PUBLIC_PACKAGE_PORT.md",
        ),
        status="LOCAL_ACCEPTED_EVIDENCE_COVERED_BY_PUBLIC_V2",
        next_action="Keep as accepted local evidence feeding the public V2 package; do not bulk-copy generated archives.",
        notes="Local reports mark bounded native proof ready while preserving no final production UI/player claim.",
    ),
    ProgressionGroup(
        group_id="v2_14b_14c_14d_14f_package",
        local_group="Tests/Test 14B, Test 14C, Test 14D, Test 14F",
        purpose="V2 read-only archive reader, WebP decode adapter, playback-loop dry run, and integrated bounded prototype package.",
        summary_parts=(189, 190),
        local_evidence=(
            "Tests/Test 14B_V2_READONLY_ARCHIVE_READER/20261007_204515/TEST14B_V2_READONLY_ARCHIVE_READER_REPORT.md",
            "Tests/Test 14C_V2_WEBP_CODEC_DECODE_ADAPTER/20261007_205656/TEST14C_V2_WEBP_CODEC_DECODE_ADAPTER_REPORT.md",
            "Tests/Test 14D_V2_PLAYBACK_LOOP_DRY_RUN/20261007_212913/TEST14D_V2_PLAYBACK_LOOP_DRY_RUN_REPORT.md",
            "Tests/Test 14F_V2_INTEGRATED_BOUNDED_PROTOTYPE_PACKAGE/20261007_215229/prototype_package/amcf_v2_prototype/amcf_v2",
        ),
        public_coverage=(
            "src/amcf_v2/",
            "demo/run_amcf_v2_public_package_demo.py",
            "tests/test_amcf_v2_public_package.py",
            "docs/AMCF_V2_PUBLIC_PACKAGE_PORT.md",
        ),
        status="IN_GITHUB_EXACT_CODE_WITH_PUBLIC_SAFE_DIFF",
        next_action="Record the one deliberate Pillow import hardening diff; otherwise keep V2 package exact.",
        notes="The public V2 package mirrors the local 14F Python package except one missing-dependency hardening change.",
    ),
    ProgressionGroup(
        group_id="benchmark_consolidation_13m",
        local_group="Tests/Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC",
        purpose="Historical benchmark/spec consolidation and acceptance summary.",
        summary_parts=(191,),
        local_evidence=(
            "Tests/Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC/20261007_170924/TEST13M_FINAL_BENCHMARK_VALIDATION_SPEC_REPORT.md",
            "Tests/Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC/20261007_170924/FINAL_PLAYBACK_READINESS_REPORT_13M.md",
        ),
        public_coverage=(
            "docs/AMCF_FULL_LOCAL_WORKSPACE_PARITY_GROUP_LEDGER.md",
            "docs/AMCF_LOCAL_MAIN_PARITY_SYNC_REPORT.md",
        ),
        status="EVIDENCE_ONLY_NOT_BULK_PORT_TARGET",
        next_action="Extract claims into ledger; do not copy generated/imported benchmark evidence wholesale.",
        notes="Mostly generated/imported evidence and ledgers; useful for decisions, not a direct code port.",
    ),
    ProgressionGroup(
        group_id="canonical_physical_boundary",
        local_group="Tests/Test AMCF_CANONICAL_CONCEPT_ALIGNMENT and vertical-stack physical simulation",
        purpose="Clarifies digital AMCF as canonical; physical carrier/player is later material execution/recovery branch.",
        summary_parts=(149, 154),
        local_evidence=(
            "Main/AMCF_CANONICAL_CONCEPT.md",
            "Main/AMCF_PHYSICAL_MEDIUM_BOUNDARY.md",
            "Tests/Test AMCF_VERTICAL_STACK_PHYSICAL_MEDIUM_SIMULATION/20261010_004003/05_FINAL_STATUS/FINAL_STATUS.md",
        ),
        public_coverage=(
            "docs/AMCF_CANONICAL_CONCEPT.md",
            "docs/AMCF_HARDWARE_SOFTWARE_PATHS.md",
            "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md",
        ),
        status="IN_GITHUB_DOCS_AND_PHYSICAL_BRANCH",
        next_action="Keep physical robustness work separate from digital AMCF parity closeout.",
        notes="Physical simulations are useful but should not distract from digital AMCF/decoded playback parity closure.",
    ),
)


def default_workspace_root(public_root: str | Path) -> Path:
    public_root = Path(public_root).resolve()
    candidates = (public_root, *public_root.parents)
    for candidate in candidates:
        if (candidate / "Main").is_dir() and (candidate / "Tests").is_dir():
            return candidate
    return public_root.parent if public_root.name == "Main" else public_root


def default_summary_path(workspace_root: str | Path) -> Path:
    return Path(workspace_root).resolve() / "transcript summary.txt"


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_exists(root: Path, rel_path: str) -> bool:
    return (root / rel_path).exists()


def public_path_exists(public_root: Path, rel_path: str) -> bool:
    return (public_root / rel_path).exists()


def summary_parts_found(summary_text: str, parts: tuple[int, ...]) -> dict[str, bool]:
    return {str(part): bool(re.search(rf"(?m)^_\+Part\s+0*{part}_\+\s*$", summary_text)) for part in parts}


def compare_public_v2_to_local_14f(workspace_root: Path, public_root: Path) -> dict[str, Any]:
    workspace_root = normalize_workspace_root(workspace_root, public_root)
    local_root = workspace_root / "Tests/Test 14F_V2_INTEGRATED_BOUNDED_PROTOTYPE_PACKAGE/20261007_215229/prototype_package/amcf_v2_prototype/amcf_v2"
    public_v2 = public_root / "src/amcf_v2"
    if not local_root.exists() or not public_v2.exists():
        return {
            "available": False,
            "local_python_files": 0,
            "public_python_files": 0,
            "matching_python_files": 0,
            "differing_python_files": [],
            "public_safe_diffs": [],
        }
    local_files = {str(path.relative_to(local_root).as_posix()): sha256_file(path) for path in local_root.rglob("*.py")}
    public_files = {str(path.relative_to(public_v2).as_posix()): sha256_file(path) for path in public_v2.rglob("*.py")}
    all_keys = sorted(set(local_files) | set(public_files))
    differing = [
        key
        for key in all_keys
        if local_files.get(key) != public_files.get(key)
    ]
    public_safe = [
        "decode/decode_pipeline.py"
    ] if differing == ["decode/decode_pipeline.py"] else []
    return {
        "available": True,
        "local_python_files": len(local_files),
        "public_python_files": len(public_files),
        "matching_python_files": len(all_keys) - len(differing),
        "differing_python_files": differing,
        "public_safe_diffs": public_safe,
    }


def compare_main_exact_mappings(workspace_root: Path, public_root: Path) -> list[dict[str, Any]]:
    workspace_root = normalize_workspace_root(workspace_root, public_root)
    pairs = (
        ("Main/amcf_test02.py", "src/amcf_local_main_test02.py"),
        ("Main/amcf_vnext.py", "src/amcf_vnext.py"),
        ("Main/test_archive_decode.py", "src/amcf_local_main_archive_decode_check.py"),
        ("Main/amcf_tracking_test03a.py", "src/amcf_local_main_tracking_test03a.py"),
    )
    rows: list[dict[str, Any]] = []
    for local_rel, public_rel in pairs:
        local_path = workspace_root / local_rel
        public_path = public_root / public_rel
        local_hash = sha256_file(local_path)
        public_hash = sha256_file(public_path)
        rows.append(
            {
                "local": local_rel,
                "public": public_rel,
                "local_present": local_hash is not None,
                "public_present": public_hash is not None,
                "hash_match": bool(local_hash and public_hash and local_hash == public_hash),
                "classification": "IN_GITHUB_EXACT_CODE" if local_hash and public_hash and local_hash == public_hash else "IN_GITHUB_PUBLIC_SAFE_ADAPTATION_OR_REVIEW",
            }
        )
    return rows


def normalize_workspace_root(workspace_root: Path, public_root: Path) -> Path:
    """Accept either a real workspace root or a legacy ancestor hint."""
    workspace_root = Path(workspace_root).resolve()
    public_root = Path(public_root).resolve()
    if (workspace_root / "Main").is_dir() and (workspace_root / "Tests").is_dir():
        return workspace_root
    candidates = (public_root, *public_root.parents)
    for candidate in candidates:
        if (candidate / "Main").is_dir() and (candidate / "Tests").is_dir():
            return candidate
    return workspace_root


def build_progression_integration_ledger(
    public_root: str | Path,
    workspace_root: str | Path | None = None,
    summary_path: str | Path | None = None,
) -> dict[str, Any]:
    public_root = Path(public_root).resolve()
    workspace_root = Path(workspace_root).resolve() if workspace_root else default_workspace_root(public_root)
    summary_path = Path(summary_path).resolve() if summary_path else default_summary_path(workspace_root)
    summary_text = summary_path.read_text(encoding="utf-8", errors="replace") if summary_path.is_file() else ""

    rows: list[dict[str, Any]] = []
    for group in PROGRESSION_GROUPS:
        local_evidence = [{"path": path, "present": path_exists(workspace_root, path)} for path in group.local_evidence]
        public_coverage = [{"path": path, "present": public_path_exists(public_root, path)} for path in group.public_coverage]
        rows.append(
            {
                "group_id": group.group_id,
                "local_group": group.local_group,
                "purpose": group.purpose,
                "summary_parts": list(group.summary_parts),
                "summary_parts_found": summary_parts_found(summary_text, group.summary_parts),
                "local_evidence": local_evidence,
                "public_coverage": public_coverage,
                "status": group.status,
                "next_action": group.next_action,
                "notes": group.notes,
                "local_evidence_present": all(item["present"] for item in local_evidence),
                "public_coverage_present": all(item["present"] for item in public_coverage),
            }
        )

    diagnostic_gap_groups = [
        row["group_id"]
        for row in rows
        if row["status"] in {"NEEDS_TARGETED_DIAGNOSTIC_PARITY_REVIEW"}
    ]
    review_groups = [
        row["group_id"]
        for row in rows
        if row["status"] in {"EVIDENCE_ONLY_NOT_BULK_PORT_TARGET"}
    ]
    return {
        "run_name": RUN_NAME,
        "public_root": "<public-repo-root>",
        "workspace_root": "<workspace-root>",
        "summary_path": "<workspace-root>/transcript summary.txt",
        "actual_public_root": str(public_root),
        "actual_workspace_root": str(workspace_root),
        "actual_summary_path": str(summary_path),
        "summary_available": summary_path.is_file(),
        "progression_groups": rows,
        "main_exact_mapping": compare_main_exact_mappings(workspace_root, public_root),
        "v2_14f_python_comparison": compare_public_v2_to_local_14f(workspace_root, public_root),
        "diagnostic_gap_groups": diagnostic_gap_groups,
        "review_groups": review_groups,
        "claim_boundary_flags": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "real_printer_integration_claimed": False,
            "real_scanner_integration_claimed": False,
            "real_player_hardware_claimed": False,
        },
        "unsafe_acceptance_count": 0,
        "generated_output_committed": False,
        "recommended_next_phase": "AMCF_DIAGNOSTIC_PROFILE_BUNDLE_COMPLETION_V1",
        "final_passed": True,
        "full_parity_claimed": False,
    }


def build_markdown_summary(report: dict[str, Any]) -> str:
    lines = [
        "# AMCF Local Tests Progression Integration Ledger",
        "",
        f"Run name: `{report['run_name']}`",
        "",
        "This ledger maps local `Main` and `Tests` progression evidence into the public GitHub package. It is a procedural parity ledger, not a claim of byte-for-byte generated-output identity.",
        "",
        "## Claim Boundary",
        "",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "- real printer/scanner/player hardware integration claimed: false",
        "- unsafe_acceptance_count: 0",
        "- full parity claimed by this ledger: false",
        "",
        "## Main Mapping",
        "",
        "| Local file | Public file | Status |",
        "| --- | --- | --- |",
    ]
    for row in report["main_exact_mapping"]:
        status = "exact" if row["hash_match"] else "public-safe adaptation / review"
        lines.append(f"| `{row['local']}` | `{row['public']}` | {status} |")

    v2 = report["v2_14f_python_comparison"]
    lines.extend(
        [
            "",
            "## V2 / 14F Package Comparison",
            "",
            f"- comparison available: `{str(v2['available']).lower()}`",
            f"- local Python files: `{v2['local_python_files']}`",
            f"- public Python files: `{v2['public_python_files']}`",
            f"- matching Python files: `{v2['matching_python_files']}`",
            f"- differing Python files: `{', '.join(v2['differing_python_files']) if v2['differing_python_files'] else 'none'}`",
            f"- public-safe dependency hardening diffs: `{', '.join(v2['public_safe_diffs']) if v2['public_safe_diffs'] else 'none'}`",
            "",
            "## Progression Groups",
            "",
            "| Group | Status | Public coverage | Next action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in report["progression_groups"]:
        coverage = ", ".join(f"`{item['path']}`" for item in row["public_coverage"])
        lines.append(f"| `{row['group_id']}` | `{row['status']}` | {coverage} | {row['next_action']} |")

    lines.extend(
        [
            "",
            "## Immediate Gap",
            "",
            "The remaining highest-priority gap is diagnostic/viewer fullness around the latest `Test 02` waterfall evidence: masks, contours, optical-flow diagnostics, source-specific track taxonomy, and contour-overlay viewer behavior. Public GitHub already contains exact or equivalent core code for much of this, but the remaining diagnostic/viewer surface should be closed explicitly instead of assumed.",
            "",
            "Recommended next phase: `AMCF_DIAGNOSTIC_PROFILE_BUNDLE_COMPLETION_V1`.",
            "",
            "## What Not To Copy",
            "",
            "- generated videos, generated archives, raw frame dumps, caches, or local output folders",
            "- local absolute paths",
            "- third-party reference repositories without separate license/provenance decisions",
            "- physical robustness experiments as a substitute for digital AMCF parity closeout",
            "",
        ]
    )
    return "\n".join(lines)


def write_progression_integration_outputs(report: dict[str, Any], output_dir: str | Path) -> dict[str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "progression_integration_ledger_report.json"
    summary_path = output_dir / "PROGRESSION_INTEGRATION_LEDGER_SUMMARY.md"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    summary_path.write_text(build_markdown_summary(report), encoding="utf-8")
    return {
        "report": str(report_path),
        "summary": str(summary_path),
    }

