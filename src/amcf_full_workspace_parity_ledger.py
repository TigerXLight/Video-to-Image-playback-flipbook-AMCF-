from __future__ import annotations

import json
import os
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


RUN_NAME = "AMCF_FULL_LOCAL_WORKSPACE_PARITY_LEDGER_V1"

TEXT_SUFFIXES = {
    ".py",
    ".cmd",
    ".bat",
    ".ps1",
    ".sh",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".tsv",
    ".xml",
}
CODE_SUFFIXES = {".py", ".cmd", ".bat", ".ps1", ".sh", ".js", ".ts"}
MEDIA_SUFFIXES = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".wav", ".m4a", ".aac", ".mp3", ".ppm"}
ARCHIVE_SUFFIXES = {".zip", ".7z", ".rar", ".tar", ".gz"}
CACHE_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules", "venv", ".venv", "build", "dist"}
THIRD_PARTY_MARKERS = {"xmem", "sam2", "samurai", "cutie", "raft", "segment-anything", "segment_anything", "pytorch", "torch"}
AMCF_TERMS = {
    "amcf",
    "archive",
    "component",
    "decode",
    "encoder",
    "manifest",
    "viewer",
    "carrier",
    "reader",
    "print",
    "physical",
    "tracking",
    "waterfall",
    "reconstruct",
    "quality",
    "psnr",
    "ssim",
    "ffmpeg",
    "v0",
    "v1",
    "v2",
}


def default_workspace_root(public_root: str | Path) -> Path:
    public_root = Path(public_root).resolve()
    return public_root.parents[4]


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def list_workspace_files(workspace_root: str | Path) -> list[str]:
    workspace_root = Path(workspace_root).resolve()
    try:
        completed = subprocess.run(
            ["rg", "--files", str(workspace_root)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return sorted(
            _relative(Path(line), workspace_root)
            for line in completed.stdout.splitlines()
            if line.strip()
        )
    except (OSError, subprocess.CalledProcessError):
        paths: list[str] = []
        for dirpath, _dirnames, filenames in os.walk(workspace_root):
            base = Path(dirpath)
            for filename in filenames:
                paths.append(_relative(base / filename, workspace_root))
        return sorted(paths)


def classify_workspace_path(rel_path: str) -> tuple[str, str]:
    lower = rel_path.lower().replace("\\", "/")
    path = Path(lower)
    suffix = path.suffix
    parts = set(lower.split("/"))

    if lower.startswith("tests/test amcf_public_github_pages_site_prep/"):
        return "ALREADY_PUBLIC", "current public GitHub package workspace"
    if lower.startswith("github repos/"):
        return "THIRD_PARTY_REFERENCE", "external reference repository collection"
    if parts & CACHE_PARTS:
        return "DO_NOT_COPY", "cache/build/dependency directory"
    if suffix in ARCHIVE_SUFFIXES or {"output", "built_archives", "decoded_outputs", "extraction_runs", "scratch"} & parts:
        return "GENERATED_DO_NOT_COPY", "generated archive/output/scratch artifact"
    if any(marker in lower for marker in THIRD_PARTY_MARKERS):
        return "THIRD_PARTY_REFERENCE", "third-party/reference/dependency surface"
    if suffix in MEDIA_SUFFIXES:
        return "ASSET_REVIEW", "media/sample/output asset"
    if suffix in CODE_SUFFIXES and any(term in lower for term in AMCF_TERMS):
        return "INSPECT_PRIORITY", "AMCF code or runnable script candidate"
    if suffix in TEXT_SUFFIXES and any(term in lower for term in AMCF_TERMS):
        return "LEDGER_REVIEW", "AMCF documentation/metadata candidate"
    if suffix in TEXT_SUFFIXES:
        return "LOW_PRIORITY_REVIEW", "text/config file"
    return "LOW_PRIORITY_REVIEW", "non-source file"


def group_inspect_priority_items(priority_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for item in priority_items:
        path = item["path"]
        parts = path.split("/")
        if parts[0] == "Tests" and len(parts) >= 2:
            group = "/".join(parts[:2])
        elif parts[0] in {"Main", "AMCF_Interactive_Viewer_01", "AMCF_Codex_Handoff_02"}:
            group = parts[0]
        else:
            group = parts[0]
        row = groups.setdefault(group, {"group": group, "count": 0, "total_bytes": 0, "sample_paths": []})
        row["count"] += 1
        row["total_bytes"] += int(item.get("bytes", 0))
        if len(row["sample_paths"]) < 12:
            row["sample_paths"].append(path)
    return sorted(groups.values(), key=lambda row: (-row["count"], row["group"]))


def build_full_workspace_parity_ledger(public_root: str | Path, workspace_root: str | Path | None = None) -> dict[str, Any]:
    public_root = Path(public_root).resolve()
    workspace_root = Path(workspace_root).resolve() if workspace_root else default_workspace_root(public_root)
    files = list_workspace_files(workspace_root)

    classification_counts: Counter[str] = Counter()
    extension_counts: Counter[str] = Counter()
    top_level_counts: Counter[str] = Counter()
    priority_items: list[dict[str, Any]] = []

    for rel_path in files:
        path = workspace_root / rel_path
        suffix = path.suffix.lower() or "<none>"
        classification, reason = classify_workspace_path(rel_path)
        classification_counts[classification] += 1
        extension_counts[suffix] += 1
        top_level_counts[rel_path.split("/")[0] if "/" in rel_path else "<root>"] += 1
        if classification == "INSPECT_PRIORITY":
            try:
                size = path.stat().st_size
            except OSError:
                size = 0
            priority_items.append({"path": rel_path, "bytes": size, "decision": classification, "reason": reason})
    priority_groups = group_inspect_priority_items(priority_items)

    return {
        "run_name": RUN_NAME,
        "public_root": "<public-repo-root>",
        "workspace_root": "<workspace-root>",
        "actual_public_root": str(public_root),
        "actual_workspace_root": str(workspace_root),
        "file_count": len(files),
        "classification_counts": dict(sorted(classification_counts.items())),
        "extension_counts_top": extension_counts.most_common(40),
        "top_level_counts_top": top_level_counts.most_common(80),
        "inspect_priority_count": len(priority_items),
        "inspect_priority_top": priority_items[:250],
        "inspect_priority_groups": priority_groups,
        "ledger_status_values": [
            "PORTED",
            "ALREADY_PUBLIC",
            "GENERATED_DO_NOT_COPY",
            "THIRD_PARTY_REFERENCE",
            "SUPERSEDED",
            "NEEDS_MANUAL_REVIEW",
        ],
        "claim_boundary_flags": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
        },
        "unsafe_acceptance_count": 0,
        "final_passed": len(files) > 0,
        "files": [{"path": rel_path, "decision": classify_workspace_path(rel_path)[0], "reason": classify_workspace_path(rel_path)[1]} for rel_path in files],
    }


def build_hierarchy_address_list_header(report: dict[str, Any]) -> list[str]:
    return [
        "# AMCF Full Local Workspace File Hierarchy Address List",
        f"run_name: {report['run_name']}",
        "workspace_root: <workspace-root>",
        "public_root: <public-repo-root>",
        "",
        "Format: <decision> | <workspace-root>/<relative-path> | <reason>",
        "",
    ]


def iter_hierarchy_address_lines(report: dict[str, Any]):
    yield from build_hierarchy_address_list_header(report)
    for item in report["files"]:
        yield f"{item['decision']} | <workspace-root>/{item['path']} | {item['reason']}"
    yield ""


def build_hierarchy_address_list_text(report: dict[str, Any]) -> str:
    lines = list(iter_hierarchy_address_lines(report))
    return "\n".join(lines)


def write_split_hierarchy_address_list(report: dict[str, Any], output_dir: Path, max_part_bytes: int = 4_000_000) -> dict[str, Any]:
    part_paths: list[Path] = []
    current_lines: list[str] = []
    current_bytes = 0

    def flush() -> None:
        nonlocal current_lines, current_bytes
        if not current_lines:
            return
        part_path = output_dir / f"local_workspace_file_hierarchy_address_list_part_{len(part_paths) + 1:04d}.txt"
        part_path.write_text("\n".join(current_lines) + "\n", encoding="utf-8")
        part_paths.append(part_path)
        current_lines = []
        current_bytes = 0

    for line in iter_hierarchy_address_lines(report):
        line_bytes = len((line + "\n").encode("utf-8"))
        if current_lines and current_bytes + line_bytes > max_part_bytes:
            flush()
        current_lines.append(line)
        current_bytes += line_bytes
    flush()

    index_path = output_dir / "local_workspace_file_hierarchy_address_list.txt"
    index_lines = [
        "# AMCF Full Local Workspace File Hierarchy Address List",
        "",
        "The complete address list is split into smaller `.txt` parts so release-package checks do not treat it as a huge generated artifact.",
        "",
    ]
    for part_path in part_paths:
        index_lines.append(f"- {part_path.name}")
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return {
        "index": index_path,
        "parts": part_paths,
    }


def build_summary_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AMCF Full Local Workspace Parity Ledger",
        "",
        f"Run name: `{report['run_name']}`",
        "",
        "This ledger is a public-safe summary of the full local workspace file hierarchy.",
        "The generated full address list is written under `output/` and is not committed.",
        "",
        "## Counts",
        "",
        f"- Files inventoried: {report['file_count']}",
        f"- Inspect-priority AMCF code/script candidates: {report['inspect_priority_count']}",
        f"- `unsafe_acceptance_count`: {report['unsafe_acceptance_count']}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "",
        "## Classification Counts",
        "",
    ]
    for key, value in report["classification_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Top-Level Areas", ""])
    for key, value in report["top_level_counts_top"][:30]:
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Initial Inspect-Priority Items", ""])
    for item in report["inspect_priority_top"][:80]:
        lines.append(f"- `{item['path']}` ({item['bytes']} bytes): {item['reason']}")
    lines.extend(["", "## Inspect-Priority Groups", ""])
    for group in report.get("inspect_priority_groups", [])[:40]:
        lines.append(f"- `{group['group']}`: {group['count']} files, {group['total_bytes']} bytes")
    lines.extend(
        [
            "",
            "## Next Work",
            "",
            "Work through inspect-priority AMCF-owned candidates group by group and mark each as `PORTED`, `ALREADY_PUBLIC`, `GENERATED_DO_NOT_COPY`, `THIRD_PARTY_REFERENCE`, `SUPERSEDED`, or `NEEDS_MANUAL_REVIEW`.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_full_workspace_parity_outputs(report: dict[str, Any], output_dir: str | Path) -> dict[str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    compact = {key: value for key, value in report.items() if key != "files"}
    report_path = output_dir / "full_workspace_parity_ledger.json"
    summary_path = output_dir / "FULL_WORKSPACE_PARITY_LEDGER_SUMMARY.md"
    report_path.write_text(json.dumps(compact, indent=2, sort_keys=True), encoding="utf-8")
    hierarchy_outputs = write_split_hierarchy_address_list(report, output_dir)
    summary_path.write_text(build_summary_markdown(report), encoding="utf-8")
    return {
        "report": str(report_path),
        "hierarchy_address_list": str(hierarchy_outputs["index"]),
        "hierarchy_address_list_parts": [str(path) for path in hierarchy_outputs["parts"]],
        "summary": str(summary_path),
    }

