from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable


RUN_NAME = "AMCF_WORKSPACE_TESTS_FUNCTIONALITY_INVENTORY_V1"

CODE_SUFFIXES = {
    ".py",
    ".cmd",
    ".bat",
    ".ps1",
    ".sh",
    ".toml",
    ".ini",
    ".cfg",
}

EXCLUDED_DIR_NAMES = {
    ".git",
    "__pycache__",
    "output",
    ".venv",
    "venv",
    "AMCF_GITHUB_CLEAN_PACKAGE",
}

LOCAL_PATH_RE = re.compile(
    r"([A-Za-z]:\\|C:\\Users\\|T:\\References\\|AppData\\|codex-runtimes|\\.venv[-\\w]*)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class InventoryRoots:
    public_root: Path
    workspace_tests_root: Path


def default_roots(public_root: str | Path) -> InventoryRoots:
    public_root = Path(public_root).resolve()
    workspace_root = public_root.parents[4]
    return InventoryRoots(
        public_root=public_root,
        workspace_tests_root=workspace_root / "Tests",
    )


def sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _has_excluded_part(path: Path) -> bool:
    return any(part in EXCLUDED_DIR_NAMES for part in path.parts)


def iter_code_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if _has_excluded_part(path):
            continue
        if path.suffix.lower() in CODE_SUFFIXES or path.name.lower() == "requirements.txt":
            yield path


def build_public_file_index(public_root: Path) -> dict[str, Any]:
    by_hash: dict[str, list[str]] = defaultdict(list)
    by_name: dict[str, list[str]] = defaultdict(list)
    for path in iter_code_files(public_root):
        try:
            digest = sha256_file(path)
        except OSError:
            continue
        rel = path.relative_to(public_root).as_posix()
        by_hash[digest].append(rel)
        by_name[path.name].append(rel)
    return {"by_hash": dict(by_hash), "by_name": dict(by_name)}


def read_text_sample(path: Path, limit: int = 65536) -> str:
    try:
        data = path.read_bytes()[:limit]
    except OSError:
        return ""
    return data.decode("utf-8", errors="replace")


def classify_code_file(rel_path: str, content: str, public_matches: dict[str, list[str]]) -> tuple[str, list[str]]:
    lower_path = rel_path.lower().replace("\\", "/")
    lower_content = content.lower()
    reasons: list[str] = []

    if public_matches.get("hash"):
        reasons.append("byte-identical public file exists")
        return "PUBLIC_EXACT_MATCH", reasons

    if lower_path.endswith((".cmd", ".bat", ".ps1")):
        if LOCAL_PATH_RE.search(content):
            reasons.append("command wrapper contains machine-local path or local venv reference")
            return "LOCAL_MACHINE_SPECIFIC_WRAPPER_NEEDS_PORTABLE_EQUIVALENT", reasons
        reasons.append("command wrapper without exact public hash match")
        return "COMMAND_WRAPPER_REVIEW_REQUIRED", reasons

    if "amcf_virtual_hardware_release_refresh" in lower_path or "release_package" in lower_path:
        reasons.append("local release-package candidate")
        if public_matches.get("name"):
            reasons.append("same filename exists in public repo")
            return "PUBLIC_NAME_MATCH_REVIEW_REQUIRED", reasons
        return "LOCAL_RELEASE_PACKAGE_CANDIDATE", reasons

    if any(term in lower_path for term in ("archive_writer", "archive_reader", "amcf_v1_", "minimal_decode_contract", "validate_archive")):
        reasons.append("archive writer/reader or v1 validation tooling")
        if public_matches.get("name"):
            reasons.append("same filename exists in public repo")
            return "PUBLIC_NAME_MATCH_REVIEW_REQUIRED", reasons
        return "CORE_ARCHIVE_TOOL_CANDIDATE", reasons

    if any(term in lower_path or term in lower_content for term in ("samurai", "sam2", "cotracker", "semantic", "manual_roi", "mask_seed", "inspection_guided")):
        reasons.append("deep/semantic/manual-review research surface")
        return "OPTIONAL_DEEP_RESEARCH_OR_DATASET_SPECIFIC", reasons

    if any(term in lower_path for term in ("regression_tests", "acceptance_harness", "quality_gate", "benchmark_validation")):
        reasons.append("local regression, acceptance, gate, or benchmark proof")
        if public_matches.get("name"):
            reasons.append("same filename exists in public repo")
            return "PUBLIC_NAME_MATCH_REVIEW_REQUIRED", reasons
        return "LOCAL_REGRESSION_PROOF_CANDIDATE", reasons

    if any(term in lower_path or term in lower_content for term in ("viewer", "playback", "preview", "review_pack")):
        reasons.append("viewer/preview/review packaging surface")
        if public_matches.get("name"):
            reasons.append("same filename exists in public repo")
            return "PUBLIC_NAME_MATCH_REVIEW_REQUIRED", reasons
        return "VIEWER_OR_REVIEW_PACKAGE_CANDIDATE", reasons

    if any(term in lower_path or term in lower_content for term in ("component", "archive", "decode", "reconstruct", "ffmpeg", "webp", "audio")):
        reasons.append("AMCF archive/component/decode/media behaviour")
        if public_matches.get("name"):
            reasons.append("same filename exists in public repo")
            return "PUBLIC_NAME_MATCH_REVIEW_REQUIRED", reasons
        return "CORE_AMCF_BEHAVIOUR_CANDIDATE", reasons

    if public_matches.get("name"):
        reasons.append("same filename exists in public repo but content differs")
        return "PUBLIC_NAME_MATCH_REVIEW_REQUIRED", reasons

    if LOCAL_PATH_RE.search(content):
        reasons.append("contains local path references")
        return "LOCAL_PATH_REVIEW_REQUIRED", reasons

    reasons.append("no exact or same-name public match found")
    return "NEEDS_MANUAL_REVIEW", reasons


def build_workspace_tests_inventory(public_root: str | Path, tests_root: str | Path | None = None) -> dict[str, Any]:
    roots = default_roots(public_root)
    public_root = roots.public_root
    workspace_tests_root = Path(tests_root).resolve() if tests_root else roots.workspace_tests_root
    public_index = build_public_file_index(public_root)
    files: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()

    for path in sorted(iter_code_files(workspace_tests_root), key=lambda p: str(p).lower()):
        try:
            rel = path.relative_to(workspace_tests_root).as_posix()
        except ValueError:
            rel = path.as_posix()
        digest = sha256_file(path)
        public_hash_matches = public_index["by_hash"].get(digest, [])
        public_name_matches = public_index["by_name"].get(path.name, [])
        content = read_text_sample(path)
        classification, reasons = classify_code_file(
            rel,
            content,
            {"hash": public_hash_matches, "name": public_name_matches},
        )
        row = {
            "local_tests_file": rel,
            "suffix": path.suffix.lower(),
            "bytes": path.stat().st_size,
            "sha256": digest,
            "classification": classification,
            "public_hash_matches": public_hash_matches,
            "public_name_matches": public_name_matches,
            "contains_local_path_reference": bool(LOCAL_PATH_RE.search(content)),
            "reasons": reasons,
        }
        files.append(row)
        counts[classification] += 1

    port_candidate_classes = {
        "CORE_ARCHIVE_TOOL_CANDIDATE",
        "CORE_AMCF_BEHAVIOUR_CANDIDATE",
        "LOCAL_RELEASE_PACKAGE_CANDIDATE",
        "LOCAL_REGRESSION_PROOF_CANDIDATE",
        "VIEWER_OR_REVIEW_PACKAGE_CANDIDATE",
    }
    port_candidates = [row for row in files if row["classification"] in port_candidate_classes]
    already_public = [
        row
        for row in files
        if row["classification"] in {"PUBLIC_EXACT_MATCH", "PUBLIC_NAME_MATCH_REVIEW_REQUIRED"}
    ]
    return {
        "run_name": RUN_NAME,
        "public_root": str(public_root),
        "workspace_tests_root": str(workspace_tests_root),
        "workspace_tests_root_exists": workspace_tests_root.exists(),
        "code_files_checked": len(files),
        "counts": dict(sorted(counts.items())),
        "already_public_or_name_matched_count": len(already_public),
        "port_candidate_count": len(port_candidates),
        "local_machine_specific_wrapper_count": counts.get("LOCAL_MACHINE_SPECIFIC_WRAPPER_NEEDS_PORTABLE_EQUIVALENT", 0),
        "optional_deep_research_count": counts.get("OPTIONAL_DEEP_RESEARCH_OR_DATASET_SPECIFIC", 0),
        "claim_boundary_flags": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
        },
        "unsafe_acceptance_count": 0,
        "files": files,
        "top_port_candidates": port_candidates[:100],
        "final_passed": workspace_tests_root.exists() and len(files) > 0,
    }


def write_inventory_outputs(report: dict[str, Any], output_dir: str | Path) -> dict[str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "workspace_tests_functionality_inventory.json"
    summary_path = output_dir / "WORKSPACE_TESTS_FUNCTIONALITY_INVENTORY_SUMMARY.md"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    summary_path.write_text(build_inventory_markdown(report), encoding="utf-8")
    return {"report": str(report_path), "summary": str(summary_path)}


def build_inventory_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AMCF Workspace Tests Functionality Inventory",
        "",
        f"Run name: `{report['run_name']}`",
        "",
        "This report inventories runnable/code-like files in the broader local workspace `Tests` tree.",
        "It does not claim that every historical experiment should be copied into the public repo.",
        "",
        "## Summary",
        "",
        f"- code files checked: {report['code_files_checked']}",
        f"- port candidate count: {report['port_candidate_count']}",
        f"- already public or same-name match count: {report['already_public_or_name_matched_count']}",
        f"- machine-specific wrapper count: {report['local_machine_specific_wrapper_count']}",
        f"- optional/deep research count: {report['optional_deep_research_count']}",
        "- unsafe_acceptance_count: 0",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "",
        "## Classification Counts",
        "",
    ]
    for key, value in report["counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## First Port Candidates", ""])
    for row in report["top_port_candidates"][:25]:
        lines.append(f"- `{row['classification']}`: `{row['local_tests_file']}`")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The public repo can only honestly claim full broader-workspace parity after the port candidates are reviewed and either ported, superseded by existing public modules, or explicitly marked as historical/generated/research-only.",
            "Generated output, local media, caches, virtual environments, and private machine paths should not be committed.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inventory broader local AMCF Tests code against the public repo.")
    parser.add_argument("--public-root", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--tests-root", default=None)
    parser.add_argument("--output", default="output/amcf_workspace_tests_functionality_inventory")
    args = parser.parse_args(argv)
    report = build_workspace_tests_inventory(args.public_root, args.tests_root)
    outputs = write_inventory_outputs(report, Path(args.public_root) / args.output)
    print(json.dumps({"final_passed": report["final_passed"], "outputs": outputs, "counts": report["counts"]}, indent=2))
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
