"""Compare all local Tests code files with Main and tracked public code."""

from __future__ import annotations

import json
import os
import subprocess
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TESTS_ROOT = REPO_ROOT.parents[4] / "Tests"
MAIN_ROOT = REPO_ROOT.parents[4] / "Main"
OUTPUT_DIR = REPO_ROOT / "output" / "amcf_tests_code_hash_comparison"
CODE_SUFFIXES = {".py", ".js", ".ts", ".cmd", ".bat", ".ps1", ".sh", ".html", ".css"}


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def code_files(root: Path, excluded_dir: Path | None = None):
    root = root.resolve()
    excluded_dir = excluded_dir.resolve() if excluded_dir else None
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        dirnames[:] = sorted(
            (name for name in dirnames if base / name != excluded_dir),
            key=str.casefold,
        )
        for name in sorted(filenames, key=str.casefold):
            path = base / name
            if path.suffix.lower() in CODE_SUFFIXES and not path.is_symlink():
                yield path


def public_code_files(public_root: Path):
    if (public_root / ".git").exists():
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=public_root, capture_output=True, check=True
        )
        for encoded in result.stdout.split(b"\0"):
            if not encoded:
                continue
            path = public_root / os.fsdecode(encoded)
            if path.suffix.lower() in CODE_SUFFIXES and path.is_file():
                yield path
    else:
        for path in code_files(public_root):
            if not set(path.relative_to(public_root).parts) & {"output", "__pycache__", ".git"}:
                yield path


def index_files(paths, root: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    by_hash: dict[str, list[str]] = defaultdict(list)
    by_name: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        relative = path.relative_to(root).as_posix()
        by_hash[digest(path)].append(relative)
        by_name[path.name.casefold()].append(relative)
    return by_hash, by_name


def compare_code(tests_root: Path, main_root: Path, public_root: Path, output_dir: Path) -> dict:
    tests_root = tests_root.resolve()
    main_root = main_root.resolve()
    public_root = public_root.resolve()
    output_dir = output_dir.resolve()
    public_hashes, public_names = index_files(public_code_files(public_root), public_root)
    main_hashes, main_names = index_files(code_files(main_root), main_root)
    output_dir.mkdir(parents=True, exist_ok=True)

    counts: Counter[str] = Counter()
    folder_counts: dict[str, Counter[str]] = defaultdict(Counter)
    unique_hashes: set[str] = set()
    errors: list[str] = []
    comparison_path = output_dir / "code_file_comparison.jsonl"
    with comparison_path.open("w", encoding="utf-8") as handle:
        for path in code_files(tests_root, excluded_dir=output_dir):
            relative = path.relative_to(tests_root).as_posix()
            try:
                file_hash = digest(path)
            except OSError as error:
                errors.append(f"{relative}: {error}")
                continue
            public_exact = public_hashes.get(file_hash, [])
            main_exact = main_hashes.get(file_hash, [])
            if path.is_relative_to(public_root):
                status = "PUBLIC_REPO_SELF"
            elif public_exact:
                status = "PUBLIC_EXACT"
            elif main_exact:
                status = "MAIN_EXACT_ONLY"
            elif public_names.get(path.name.casefold()):
                status = "PUBLIC_NAME_DIFFERENT_REVIEW"
            elif main_names.get(path.name.casefold()):
                status = "MAIN_NAME_DIFFERENT_REVIEW"
            else:
                status = "UNMATCHED_REVIEW_REQUIRED"
            row = {
                "path": relative,
                "sha256": file_hash,
                "bytes": path.stat().st_size,
                "hash_status": status,
                "public_exact_paths": public_exact,
                "main_exact_paths": main_exact,
                "public_same_name_paths": public_names.get(path.name.casefold(), []),
                "main_same_name_paths": main_names.get(path.name.casefold(), []),
                "semantic_review_complete": False,
            }
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            counts[status] += 1
            folder_counts[relative.split("/", 1)[0]][status] += 1
            unique_hashes.add(file_hash)

    summary = {
        "run_name": "AMCF_TESTS_CODE_HASH_COMPARISON_V1",
        "code_files_hashed": sum(counts.values()),
        "unique_code_hashes": len(unique_hashes),
        "public_code_hashes": len(public_hashes),
        "main_code_hashes": len(main_hashes),
        "hash_status_counts": dict(sorted(counts.items())),
        "folder_hash_status_counts": {
            key: dict(sorted(value.items())) for key, value in sorted(folder_counts.items())
        },
        "semantic_reviews_completed_by_this_scan": 0,
        "full_parity_proven": False,
        "errors": errors,
        "scan_complete": not errors,
    }
    (output_dir / "code_hash_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def main() -> int:
    summary = compare_code(TESTS_ROOT, MAIN_ROOT, REPO_ROOT, OUTPUT_DIR)
    print(json.dumps({key: value for key, value in summary.items() if key != "folder_hash_status_counts"}, indent=2, sort_keys=True))
    return 0 if summary["scan_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
