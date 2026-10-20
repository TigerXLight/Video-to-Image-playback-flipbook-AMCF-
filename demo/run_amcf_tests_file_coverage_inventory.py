"""Inventory every Tests-tree file without mistaking classification for review."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TESTS_ROOT = REPO_ROOT.parents[4] / "Tests"
OUTPUT_DIR = REPO_ROOT / "output" / "amcf_tests_file_coverage_inventory"
MAX_PART_BYTES = 3_500_000

CODE_SUFFIXES = {".py", ".js", ".ts", ".cmd", ".bat", ".ps1", ".sh", ".html", ".css"}
DOC_SUFFIXES = {".md", ".txt", ".pdf", ".docx", ".rtf"}
DATA_SUFFIXES = {".json", ".jsonl", ".csv", ".tsv", ".xml", ".toml", ".ini", ".cfg", ".yml", ".yaml"}
MEDIA_SUFFIXES = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".wav", ".m4a", ".aac", ".mp3", ".ppm"}
ARCHIVE_SUFFIXES = {".zip", ".7z", ".rar", ".tar", ".gz"}


def classify_path(relative_path: str) -> str:
    suffix = Path(relative_path).suffix.lower()
    if suffix in CODE_SUFFIXES:
        return "code_or_runnable"
    if suffix in DOC_SUFFIXES:
        return "document"
    if suffix in DATA_SUFFIXES:
        return "data_or_metadata"
    if suffix in MEDIA_SUFFIXES:
        return "media"
    if suffix in ARCHIVE_SUFFIXES:
        return "archive_unopened"
    return "other"


def inventory_tests(tests_root: Path, output_dir: Path, max_part_bytes: int = MAX_PART_BYTES) -> dict:
    tests_root = tests_root.resolve()
    output_dir = output_dir.resolve()
    if not tests_root.is_dir():
        raise FileNotFoundError(tests_root)
    output_dir.mkdir(parents=True, exist_ok=True)

    counts: Counter[str] = Counter()
    folder_counts: Counter[str] = Counter()
    errors: list[str] = []
    part_names: list[str] = []
    part_file = None
    part_bytes = 0

    def write_row(row: dict) -> None:
        nonlocal part_file, part_bytes
        encoded = (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        if part_file is None or part_bytes + len(encoded) > max_part_bytes:
            if part_file is not None:
                part_file.close()
            part_name = f"file_inventory_part_{len(part_names) + 1:04d}.jsonl"
            part_names.append(part_name)
            part_file = (output_dir / part_name).open("wb")
            part_bytes = 0
        part_file.write(encoded)
        part_bytes += len(encoded)

    try:
        for directory, dirnames, filenames in os.walk(tests_root, followlinks=False, onerror=lambda error: errors.append(str(error))):
            dirnames.sort(key=str.casefold)
            filenames.sort(key=str.casefold)
            base = Path(directory)
            dirnames[:] = [name for name in dirnames if base / name != output_dir]
            symlink_dirs = [name for name in dirnames if (base / name).is_symlink()]
            for name in symlink_dirs:
                dirnames.remove(name)
            for name in filenames + symlink_dirs:
                path = base / name
                relative = path.relative_to(tests_root).as_posix()
                try:
                    size = path.lstat().st_size
                except OSError as error:
                    errors.append(f"{relative}: {error}")
                    continue
                kind = "symlink" if path.is_symlink() else classify_path(relative)
                folder = relative.split("/", 1)[0]
                counts[kind] += 1
                folder_counts[folder] += 1
                write_row({
                    "path": relative,
                    "bytes": size,
                    "kind": kind,
                    "review_status": "UNREVIEWED",
                })
    finally:
        if part_file is not None:
            part_file.close()

    summary = {
        "run_name": "AMCF_TESTS_FILE_LEVEL_COVERAGE_BASELINE_V1",
        "files_inventoried": sum(counts.values()),
        "top_level_folders_with_files": len(folder_counts),
        "kind_counts": dict(sorted(counts.items())),
        "folder_counts": dict(sorted(folder_counts.items())),
        "manual_file_reviews_confirmed_by_inventory": 0,
        "file_level_parity_proven": False,
        "inventory_parts": part_names,
        "self_generated_report_directory_excluded": output_dir.is_relative_to(tests_root),
        "errors": errors,
        "inventory_complete": not errors,
    }
    (output_dir / "inventory_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tests-root", type=Path, default=TESTS_ROOT)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    arguments = parser.parse_args()
    summary = inventory_tests(arguments.tests_root, arguments.output)
    print(json.dumps({key: value for key, value in summary.items() if key != "folder_counts"}, indent=2, sort_keys=True))
    return 0 if summary["inventory_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
