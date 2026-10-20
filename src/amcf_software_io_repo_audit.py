from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


RUN_NAME = "AMCF_SOFTWARE_IO_REPO_AUDIT_V1"
DOSSIER_PATH = "docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md"
NEXT_RECOMMENDED_PHASE = "shared_amcf_package_manifest_update_event_section_model_foundation"

CLAIM_BOUNDARY_FLAGS = {
    "hardware_validation_claimed": False,
    "physical_level_5_claimed": False,
    "manufactured_player_claimed": False,
    "real_printer_required": False,
    "real_reader_required": False,
    "real_player_required": False,
    "real_scanner_required": False,
    "real_usb_required": False,
}

SEARCH_TERMS = [
    "manifest",
    "package",
    "export",
    "AMCF",
    "frame",
    "frames",
    "component",
    "components",
    "update",
    "update_event",
    "update event",
    "timeline",
    "schedule",
    "timing",
    "playback",
    "section",
    "sections",
    "physical",
    "print",
    "printer",
    "PDF",
    "SVG",
    "PNG",
    "layout",
    "sheet",
    "card",
    "strip",
    "carrier",
    "reader",
    "scanner",
    "scan",
    "capture",
    "image",
    "lane",
    "marker",
    "registration",
    "colour",
    "color",
    "hash",
    "checksum",
    "digest",
    "report",
    "audit",
    "fixture",
    "fixtures",
    "demo",
    "output",
    "metadata",
    "schema",
    "claim_boundary",
    "unsafe_acceptance",
    "final_passed",
    "generated_output",
    "local_path",
    "hardware_claim",
    "fail_closed",
    "reverse",
    "seek",
    "prefetch",
    "view_gate",
    "hidden_gate",
    "mechanism",
    "profile",
    "capability",
    "command",
    "protocol",
    "diagnostic",
    "audio_sync",
]

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "shared_amcf_core": [
        "amcf",
        "package",
        "manifest",
        "schema",
        "update",
        "update_event",
        "update event",
        "timing",
        "schedule",
        "validation",
        "hash",
        "checksum",
        "digest",
        "metadata",
        "report model",
    ],
    "pc_to_printer": [
        "print",
        "printer",
        "pdf",
        "svg",
        "png",
        "layout",
        "sheet",
        "card",
        "strip",
        "registration",
        "timing/index",
        "colour",
        "color",
        "reprint",
        "physical_carrier",
        "carrier package",
    ],
    "pc_reader": [
        "reader",
        "scanner",
        "scan",
        "capture",
        "image",
        "lane",
        "marker",
        "registration",
        "colour",
        "color",
        "recovery",
        "rescan",
        "virtual_reader",
    ],
    "player_pc": [
        "player",
        "capability",
        "command",
        "control",
        "protocol",
        "diagnostic",
        "audio_sync",
        "package transfer",
        "handoff",
        "runtime",
    ],
    "physical_player_simulator_control": [
        "state_machine",
        "fail_closed",
        "reverse",
        "seek",
        "mechanism",
        "profile",
        "prefetch",
        "view_gate",
        "hidden_gate",
        "staging",
        "simulator",
        "mechanical_optical",
    ],
    "reports_logs_audits": [
        "report",
        "audit",
        "summary",
        "final_passed",
        "unsafe_acceptance",
        "claim_boundary",
        "generated_output",
        "local_path",
        "hardware_claim",
        "review",
        "closeout",
        "tag_prep",
    ],
    "tests_fixtures": [
        "test",
        "tests/",
        "fixture",
        "fixtures",
        "expected",
        "sample",
        "example",
        "unittest",
    ],
    "docs_site_release": [
        "docs/",
        "readme",
        "site/",
        "release",
        "package refresh",
        "closeout",
        "github pages",
        "tag prep",
        "license",
        "publication",
    ],
}

SCHEMA_TERMS = [
    "package",
    "manifest",
    "report",
    "section",
    "schema",
    "physicalsection",
    "amcfphysicalmanifest",
    "claim_boundary",
]

SOURCE_SUFFIXES = {".py", ".md", ".json", ".html", ".css", ".svg", ".txt", ".cmd"}
SKIP_PARTS = {".git", "__pycache__"}
GENERATED_PREFIXES = ("output/", "demo/output/")


@dataclass(frozen=True)
class Classification:
    path: str
    categories: list[str]
    scores: dict[str, int]
    matched_terms: list[str]
    is_generated_output: bool
    is_source_truth: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "categories": self.categories,
            "scores": self.scores,
            "matched_terms": self.matched_terms,
            "is_generated_output": self.is_generated_output,
            "is_source_truth": self.is_source_truth,
        }


def repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize_path(path: str | Path) -> str:
    return Path(path).as_posix()


def is_generated_output_path(path: str | Path) -> bool:
    normalized = normalize_path(path).lower()
    return normalized.startswith(GENERATED_PREFIXES) or "/__pycache__/" in normalized or normalized.startswith("__pycache__/")


def is_source_truth_path(path: str | Path) -> bool:
    return not is_generated_output_path(path)


def text_for_matching(path: str | Path, content: str = "") -> str:
    normalized = normalize_path(path).replace("_", " ").replace("-", " ")
    return f"{normalized}\n{content}".lower()


def classify_file(path: str | Path, content: str = "") -> Classification:
    normalized = normalize_path(path)
    haystack = text_for_matching(normalized, content)
    matched_terms = sorted({term for term in SEARCH_TERMS if term.lower() in haystack})
    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in haystack:
                score += 1
        scores[category] = score
    categories = [category for category, score in scores.items() if score > 0]
    if is_generated_output_path(normalized):
        categories = ["generated_output_ignored"]
    elif not categories:
        categories = ["unclear_duplicate_schema_conflict"]
    if any(term in haystack for term in SCHEMA_TERMS) and len([c for c in categories if c != "generated_output_ignored"]) >= 3:
        if "unclear_duplicate_schema_conflict" not in categories:
            categories.append("unclear_duplicate_schema_conflict")
    return Classification(
        path=normalized,
        categories=categories,
        scores=scores,
        matched_terms=matched_terms,
        is_generated_output=is_generated_output_path(normalized),
        is_source_truth=is_source_truth_path(normalized),
    )


def git_lines(repo_root: Path, args: list[str]) -> list[str]:
    try:
        result = subprocess.run(["git", *args], cwd=repo_root, text=True, capture_output=True, check=False)
    except OSError:
        return []
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def git_scalar(repo_root: Path, args: list[str], default: str = "unknown") -> str:
    lines = git_lines(repo_root, args)
    return lines[0] if lines else default


def git_bool(repo_root: Path, args: list[str]) -> bool:
    try:
        result = subprocess.run(["git", *args], cwd=repo_root, text=True, capture_output=True, check=False)
    except OSError:
        return False
    return result.returncode == 0


def tracked_files(repo_root: Path) -> list[str]:
    lines = git_lines(repo_root, ["ls-files"])
    if lines:
        return sorted(line.replace("\\", "/") for line in lines)
    # Main is a maintained source tree but is intentionally not itself a Git checkout.
    # Audit its source-shaped files without treating generated output as source truth.
    fallback: list[str] = []
    for path in repo_root.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.relative_to(repo_root).parts):
            continue
        relative = path.relative_to(repo_root).as_posix()
        if path.suffix.lower() in SOURCE_SUFFIXES and is_source_truth_path(relative):
            fallback.append(relative)
    return sorted(fallback)


def readable_text(repo_root: Path, rel_path: str, max_chars: int = 120_000) -> str:
    path = repo_root / rel_path
    if path.suffix.lower() not in SOURCE_SUFFIXES:
        return ""
    try:
        data = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    return data[:max_chars]


def build_corridor_file_map(classifications: list[Classification]) -> dict[str, list[str]]:
    category_names = [
        "shared_amcf_core",
        "pc_to_printer",
        "pc_reader",
        "player_pc",
        "physical_player_simulator_control",
        "reports_logs_audits",
        "tests_fixtures",
        "docs_site_release",
        "generated_output_ignored",
        "unclear_duplicate_schema_conflict",
    ]
    mapping = {name: [] for name in category_names}
    for item in classifications:
        for category in item.categories:
            mapping.setdefault(category, []).append(item.path)
    return {key: sorted(set(value)) for key, value in mapping.items()}


def build_schema_discovery(classifications: list[Classification]) -> dict[str, Any]:
    candidates = []
    for item in classifications:
        matched_schema_terms = sorted(set(item.matched_terms).intersection(SCHEMA_TERMS))
        if matched_schema_terms:
            candidates.append(
                {
                    "path": item.path,
                    "categories": item.categories,
                    "schema_terms": matched_schema_terms,
                }
            )
    overlapping = [
        item
        for item in candidates
        if len([category for category in item["categories"] if category != "unclear_duplicate_schema_conflict"]) >= 3
    ]
    return {
        "candidate_count": len(candidates),
        "overlap_review_count": len(overlapping),
        "candidates": candidates,
        "overlap_review_candidates": overlapping,
    }


def generated_output_status(repo_root: Path) -> dict[str, Any]:
    tracked = [line for line in git_lines(repo_root, ["ls-files", "output", "demo/output"]) if line]
    staged = [line for line in git_lines(repo_root, ["diff", "--cached", "--name-only", "--", "output", "demo/output"]) if line]
    existing_dirs = []
    for rel in ("output", "demo/output"):
        if (repo_root / rel).exists():
            existing_dirs.append(rel)
    return {
        "existing_generated_output_dirs": existing_dirs,
        "tracked_output_files": tracked,
        "staged_output_files": staged,
        "generated_output_committed": len(tracked) > 0,
        "generated_output_staged": len(staged) > 0,
        "passed": len(tracked) == 0 and len(staged) == 0,
    }


def origin_main_status(repo_root: Path, head_commit: str) -> dict[str, Any]:
    origin_main = git_scalar(repo_root, ["rev-parse", "origin/main"], default="unavailable")
    origin_main_contains_head = False
    head_contains_origin_main = False
    if origin_main != "unavailable":
        origin_main_contains_head = git_bool(repo_root, ["merge-base", "--is-ancestor", head_commit, "origin/main"])
        head_contains_origin_main = git_bool(repo_root, ["merge-base", "--is-ancestor", "origin/main", head_commit])
    note = "origin/main unavailable; no merge, rebase, or base change performed"
    if origin_main != "unavailable":
        if origin_main_contains_head:
            note = "local origin/main contains the audit base/head; no base change performed"
        elif head_contains_origin_main:
            note = "local audit branch is ahead of origin/main; no merge, rebase, or base change performed"
        else:
            note = "local origin/main and audit branch have diverged or local refs are stale; recorded only, no merge, rebase, or base change performed"
    return {
        "origin_main_head": origin_main,
        "origin_main_contains_current_head": origin_main_contains_head,
        "current_head_contains_origin_main": head_contains_origin_main,
        "note": note,
    }


def build_report(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else repo_root_from_here()
    root = root.resolve()
    branch = git_scalar(root, ["branch", "--show-current"])
    head_commit = git_scalar(root, ["rev-parse", "HEAD"])
    files = tracked_files(root)
    classifications: list[Classification] = []
    for rel_path in files:
        if any(part in SKIP_PARTS for part in Path(rel_path).parts):
            continue
        content = readable_text(root, rel_path)
        classifications.append(classify_file(rel_path, content))
    corridor_file_map = build_corridor_file_map(classifications)
    schema_discovery = build_schema_discovery(classifications)
    generated_status = generated_output_status(root)
    unclear_files = corridor_file_map.get("unclear_duplicate_schema_conflict", [])
    summary = {
        "total_tracked_files_audited": len(classifications),
        "shared_core_files": len(corridor_file_map["shared_amcf_core"]),
        "pc_to_printer_files": len(corridor_file_map["pc_to_printer"]),
        "pc_reader_files": len(corridor_file_map["pc_reader"]),
        "player_pc_files": len(corridor_file_map["player_pc"]),
        "physical_player_simulator_control_files": len(corridor_file_map["physical_player_simulator_control"]),
        "reports_logs_audits_files": len(corridor_file_map["reports_logs_audits"]),
        "tests_fixtures_files": len(corridor_file_map["tests_fixtures"]),
        "docs_site_release_files": len(corridor_file_map["docs_site_release"]),
        "unclear_or_overlap_files": len(unclear_files),
    }
    final_passed = (
        (root / DOSSIER_PATH).exists()
        and generated_status["passed"]
        and summary["total_tracked_files_audited"] > 0
        and summary["shared_core_files"] > 0
        and summary["pc_to_printer_files"] > 0
        and summary["pc_reader_files"] > 0
        and summary["player_pc_files"] > 0
        and all(value is False for value in CLAIM_BOUNDARY_FLAGS.values())
    )
    return {
        "run_name": RUN_NAME,
        "created_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "repo_root": str(root),
        "branch": branch,
        "head_commit": head_commit,
        "dossier_path": DOSSIER_PATH,
        "origin_main_status": origin_main_status(root, head_commit),
        "final_passed": final_passed,
        "summary": summary,
        "counts": summary,
        "corridor_file_map": corridor_file_map,
        "schema_discovery": schema_discovery,
        "unclear_files": unclear_files,
        "generated_output_status": generated_status,
        "claim_boundary_flags": dict(CLAIM_BOUNDARY_FLAGS),
        "unsafe_acceptance_count": 0,
        "next_recommended_phase": NEXT_RECOMMENDED_PHASE,
        "phase_boundary": {
            "implemented_later_phase": False,
            "created_package_model": False,
            "created_printer_module": False,
            "created_reader_module": False,
            "created_player_runtime_module": False,
            "hardware_api_added": False,
        },
    }


def build_summary_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    origin = report["origin_main_status"]
    lines = [
        "# AMCF Software I/O Repo Audit Summary",
        "",
        f"- run name: `{report['run_name']}`",
        f"- branch: `{report['branch']}`",
        f"- head commit: `{report['head_commit']}`",
        f"- dossier path: `{report['dossier_path']}`",
        f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
        f"- origin/main note: {origin['note']}",
        "",
        "## Classification Counts",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "- unsafe_acceptance_count: 0",
            "- hardware validation claimed: false",
            "- physical Level 5 claimed: false",
            "- manufactured player claimed: false",
            "- real printer/reader/player/scanner/USB required: false",
            "",
            "## Phase Boundary",
            "",
            "No package-model, manifest-model, printer, reader, player-runtime, GUI, scanner, image-processing, PDF, barcode, USB, serial, or hardware module was implemented by this audit.",
            "",
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_audit_outputs(output_dir: str | Path, repo_root: str | Path | None = None) -> dict[str, Any]:
    out = Path(output_dir)
    report = build_report(repo_root)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "software_io_repo_audit_report.json", report)
    write_json(out / "corridor_file_map.json", report["corridor_file_map"])
    write_json(out / "schema_discovery_report.json", report["schema_discovery"])
    (out / "SOFTWARE_IO_REPO_AUDIT_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    return report
