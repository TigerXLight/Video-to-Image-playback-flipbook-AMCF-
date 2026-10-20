"""Hash and validate one local evidence folder without deciding feature parity."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import zipfile
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "output" / "amcf_tests_folder_evidence"
TEXT_SUFFIXES = {".txt", ".md", ".html", ".css", ".js", ".ts", ".py", ".cmd", ".bat", ".ps1", ".sh"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _inspect(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
        return {"check": "json_parsed", "value_type": type(value).__name__}
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.reader(handle)
            header = next(reader, [])
            rows = sum(1 for _ in reader)
        return {"check": "csv_parsed", "columns": len(header), "rows": rows}
    if suffix in TEXT_SUFFIXES:
        return {"check": "utf8_read", "lines": len(path.read_text(encoding="utf-8").splitlines())}
    if suffix in IMAGE_SUFFIXES:
        try:
            from PIL import Image
        except ImportError:
            return {"check": "image_not_verified_pillow_unavailable"}
        with Image.open(path) as image:
            size = list(image.size)
            format_name = image.format
            image.verify()
        return {"check": "image_verified", "format": format_name, "size": size}
    if suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ValueError("duplicate archive members")
            bad_member = archive.testzip()
            if bad_member is not None:
                raise ValueError(f"archive CRC mismatch: {bad_member}")
        return {"check": "zip_crc_verified", "members": len(names)}
    return {"check": "bytes_hashed_only"}


def scan_folder(folder: Path, output_dir: Path) -> dict:
    folder = folder.resolve()
    output_dir = output_dir.resolve()
    if not folder.is_dir():
        raise FileNotFoundError(folder)
    if output_dir.is_relative_to(folder):
        raise ValueError("output directory must be outside the scanned folder")
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    counts: Counter[str] = Counter()
    failures = []
    def walk_error(error: OSError) -> None:
        failures.append(f"walk: {error}")

    for directory, dirnames, filenames in os.walk(folder, followlinks=False, onerror=walk_error):
        for name in dirnames:
            path = Path(directory) / name
            if path.is_symlink():
                failures.append(f"symlink directory: {path.relative_to(folder).as_posix()}")
        dirnames[:] = sorted((name for name in dirnames if not (Path(directory) / name).is_symlink()), key=str.casefold)
        for name in sorted(filenames, key=str.casefold):
            path = Path(directory) / name
            relative = path.relative_to(folder).as_posix()
            row = {"path": relative, "bytes": path.lstat().st_size, "semantic_disposition": "OPEN"}
            if path.is_symlink():
                row["verification"] = {"check": "symlink_not_followed"}
                failures.append(relative)
            else:
                try:
                    row["sha256"] = _hash_file(path)
                    row["verification"] = _inspect(path)
                except (OSError, UnicodeError, ValueError, csv.Error, zipfile.BadZipFile) as error:
                    row["error"] = f"{type(error).__name__}: {error}"
                    failures.append(relative)
            counts[row["verification"]["check"] if "verification" in row else "error"] += 1
            rows.append(row)

    rows.sort(key=lambda item: item["path"].casefold())
    with (output_dir / "file_evidence.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    summary = {
        "folder_name": folder.name,
        "files_scanned": len(rows),
        "verification_counts": dict(sorted(counts.items())),
        "failures": failures,
        "file_evidence_complete": not failures,
        "semantic_review_complete_by_scanner": False,
        "full_local_to_public_parity_proven": False,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    summary = scan_folder(args.folder, args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["file_evidence_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
