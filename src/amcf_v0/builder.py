from __future__ import annotations
import argparse, json, shutil, subprocess, sys, time, zipfile
from datetime import datetime
from pathlib import Path

from .common import (
    is_unsafe_rel_name, source_files, sha256_file, read_json, write_json,
    write_csv, posix_rel, validate_viewer_links, probe_media,
)

REQUIRED_FILES = [
    "media/original_vs_best_visual_baseline.mp4",
    "media/candidate_only_best_visual_baseline.mp4",
    "docs/visual_gate_rules.md",
]

def find_manifest(root: Path) -> Path | None:
    candidates = sorted((root / "manifest").glob("*.json")) if (root / "manifest").exists() else []
    for p in candidates:
        try:
            data = read_json(p)
        except Exception:
            continue
        if "archive_schema_name" in data or "not_final_codec" in data or "primary_viewer" in data:
            return p
    return candidates[0] if candidates else None

def find_viewer(root: Path) -> Path | None:
    viewers = sorted((root / "viewer").glob("OPEN_FIRST*.html")) if (root / "viewer").exists() else []
    return viewers[0] if viewers else None

def inventory(root: Path):
    rows = []
    for p in source_files(root):
        rel = posix_rel(p, root)
        rows.append({"path": rel, "size": p.stat().st_size, "unsafe": is_unsafe_rel_name(rel)})
    return rows

def inspect_source(root: Path):
    rows = inventory(root)
    manifest = find_manifest(root)
    viewer = find_viewer(root)
    report = {
        "source_folder": str(root),
        "exists": root.exists(),
        "file_count": len(rows),
        "total_size": sum(r["size"] for r in rows),
        "manifest": posix_rel(manifest, root) if manifest else None,
        "viewer": posix_rel(viewer, root) if viewer else None,
        "media_count": len([r for r in rows if r["path"].startswith("media/")]),
        "doc_count": len([r for r in rows if r["path"].startswith("docs/")]),
        "unsafe_count": len([r for r in rows if r["unsafe"]]),
        "warnings": [],
    }
    if not manifest:
        report["warnings"].append("No AMCF manifest found")
    if not viewer:
        report["warnings"].append("No OPEN_FIRST viewer found")
    return report

def validate_source(root: Path):
    report = inspect_source(root)
    errors = []
    if not root.exists():
        errors.append("Source folder does not exist")
    unsafe = [r for r in inventory(root) if r["unsafe"]] if root.exists() else []
    if unsafe:
        errors.append("Forbidden or unsafe source entries found")
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"Missing required file: {rel}")
    manifest = find_manifest(root)
    manifest_data = {}
    if not manifest:
        errors.append("Missing manifest JSON")
    else:
        try:
            manifest_data = read_json(manifest)
        except Exception as e:
            errors.append(f"Manifest JSON invalid: {e}")
    viewer = find_viewer(root)
    if not viewer:
        errors.append("Missing OPEN_FIRST viewer")
    viewer_links = validate_viewer_links(root) if root.exists() else {"passed": False, "rows": [], "missing": [], "external": []}
    if not viewer_links["passed"]:
        errors.append("Viewer relative path validation failed")
    media = probe_media(root) if root.exists() else {"passed": False, "rows": []}
    if not media["passed"]:
        errors.append("Required media validation failed")
    docs_ok = (root / "docs" / "visual_gate_rules.md").exists()
    if not docs_ok:
        errors.append("Missing visual gate rules doc")
    report.update({
        "manifest_data_keys": sorted(manifest_data.keys()),
        "viewer_links": viewer_links,
        "media": media,
        "unsafe_entries": unsafe,
        "errors": errors,
        "passed": not errors,
    })
    return report

def checksum_source(root: Path, out_json: Path | None = None, out_tsv: Path | None = None):
    rows = []
    for p in source_files(root):
        rel = posix_rel(p, root)
        if is_unsafe_rel_name(rel):
            continue
        rows.append({"path": rel, "size": p.stat().st_size, "sha256": sha256_file(p)})
    report = {"source_folder": str(root), "file_count": len(rows), "total_size": sum(r["size"] for r in rows), "files": rows, "passed": True}
    if out_json:
        write_json(out_json, report)
    if out_tsv:
        out_tsv.parent.mkdir(parents=True, exist_ok=True)
        with out_tsv.open("w", encoding="utf-8", newline="") as f:
            f.write("path\tsize\tsha256\n")
            for r in rows:
                f.write(f"{r['path']}\t{r['size']}\t{r['sha256']}\n")
    return report

def build_archive(root: Path, out: Path, report_path: Path | None = None):
    val = validate_source(root)
    if not val["passed"]:
        report = {"source_folder": str(root), "output_archive": str(out), "validation": val, "passed": False, "error": "source validation failed"}
        if report_path:
            write_json(report_path, report)
        return report
    out.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "builder": "amcfv0_builder.py",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_folder_name": root.name,
        "not_final_codec": True,
        "notes": "Built by AMCF Test 04E builder. This is a prototype archive, not a final codec.",
    }
    checksums = checksum_source(root)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        seen = set()
        for p in source_files(root):
            rel = posix_rel(p, root)
            if is_unsafe_rel_name(rel):
                continue
            z.write(p, rel)
            seen.add(rel)
        z.writestr("manifest/AMCF_04E_BUILD_METADATA.json", json.dumps(metadata, indent=2))
        z.writestr("manifest/AMCF_04E_CHECKSUMS.json", json.dumps(checksums, indent=2))
        z.writestr("docs/BUILD_REPORT_04E.md", "# AMCF 04E Build Report\n\nBuilt by AMCF v0 builder. This is not a final codec.\n")
    report = {
        "source_folder": str(root),
        "output_archive": str(out),
        "validation": val,
        "archive_size": out.stat().st_size,
        "file_count_packaged": checksums["file_count"],
        "generated_entries": ["manifest/AMCF_04E_BUILD_METADATA.json", "manifest/AMCF_04E_CHECKSUMS.json", "docs/BUILD_REPORT_04E.md"],
        "passed": True,
    }
    if report_path:
        write_json(report_path, report)
    return report

def compare_source_archive(root: Path, archive: Path):
    src = {posix_rel(p, root) for p in source_files(root) if not is_unsafe_rel_name(posix_rel(p, root))}
    with zipfile.ZipFile(archive) as z:
        names = {n for n in z.namelist() if not n.endswith("/")}
    missing = sorted(src - names)
    generated_ok = {"manifest/AMCF_04E_BUILD_METADATA.json", "manifest/AMCF_04E_CHECKSUMS.json", "docs/BUILD_REPORT_04E.md"}
    extra = sorted(names - src - generated_ok)
    required_present = {rel: rel in names for rel in REQUIRED_FILES}
    report = {
        "source_folder": str(root),
        "archive": str(archive),
        "source_file_count": len(src),
        "archive_file_count": len(names),
        "missing_from_archive": missing,
        "extra_unexpected_entries": extra,
        "generated_entries_present": sorted(generated_ok & names),
        "required_entries": required_present,
        "passed": not missing and all(required_present.values()),
    }
    return report

def init_template(root: Path):
    if root.exists():
        shutil.rmtree(root)
    (root / "viewer").mkdir(parents=True)
    (root / "media").mkdir()
    (root / "manifest").mkdir()
    (root / "docs").mkdir()
    (root / "viewer" / "OPEN_FIRST_AMCF_TEMPLATE_VIEWER.html").write_text("""<!doctype html>
<html><head><meta charset=\"utf-8\"><title>AMCF v0 Template</title></head>
<body><h1>AMCF v0 Template Source</h1><p>Add real media before packaging as a visual archive.</p></body></html>
""", encoding="utf-8")
    (root / "manifest" / "AMCF_TEMPLATE_ARCHIVE_MANIFEST.json").write_text(json.dumps({
        "archive_schema_name": "AMCF v0 prototype archive",
        "archive_schema_version": "template",
        "not_final_codec": True,
        "template_only": True,
        "primary_viewer": "viewer/OPEN_FIRST_AMCF_TEMPLATE_VIEWER.html",
        "known_limitations": ["No real media included yet"],
    }, indent=2), encoding="utf-8")
    (root / "docs" / "visual_gate_rules.md").write_text("# Visual Gate Rules\n\nTemplate only. Add real gate docs before production review.\n", encoding="utf-8")
    (root / "docs" / "README_TEMPLATE.md").write_text("# AMCF v0 Template Source\n\nThis is a folder scaffold. It is not a complete visual archive until real media is added.\n", encoding="utf-8")
    return {"template_folder": str(root), "passed": True, "template_only": True}

def run_loader_validate(loader: Path, archive: Path, report: Path):
    py = sys.executable
    p = subprocess.run([py, str(loader), "validate", str(archive), "--report", str(report)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        data = read_json(report)
    except Exception:
        data = {}
    return {"returncode": p.returncode, "stdout": p.stdout, "report": data, "passed": p.returncode == 0 and bool(data.get("passed"))}

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("inspect-source"); p.add_argument("source"); p.add_argument("--out", default="")
    p = sub.add_parser("validate-source"); p.add_argument("source"); p.add_argument("--report", default="")
    p = sub.add_parser("checksum"); p.add_argument("source"); p.add_argument("--out", default=""); p.add_argument("--tsv", default="")
    p = sub.add_parser("build"); p.add_argument("source"); p.add_argument("--out", required=True); p.add_argument("--report", default="")
    p = sub.add_parser("compare-source-archive"); p.add_argument("source"); p.add_argument("archive"); p.add_argument("--report", default="")
    p = sub.add_parser("init-template"); p.add_argument("source"); p.add_argument("--report", default="")
    p = sub.add_parser("verify-built"); p.add_argument("archive"); p.add_argument("--loader", required=True); p.add_argument("--report", default="")
    ns = ap.parse_args()
    code = 0
    if ns.cmd == "inspect-source":
        report = inspect_source(Path(ns.source))
        if ns.out: Path(ns.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
    elif ns.cmd == "validate-source":
        report = validate_source(Path(ns.source))
        if ns.report: write_json(Path(ns.report), report)
        print(json.dumps(report, indent=2))
        code = 0 if report["passed"] else 1
    elif ns.cmd == "checksum":
        report = checksum_source(Path(ns.source), Path(ns.out) if ns.out else None, Path(ns.tsv) if ns.tsv else None)
        print(json.dumps({k:v for k,v in report.items() if k != "files"}, indent=2))
    elif ns.cmd == "build":
        report = build_archive(Path(ns.source), Path(ns.out), Path(ns.report) if ns.report else None)
        print(json.dumps({k:v for k,v in report.items() if k != "validation"}, indent=2))
        code = 0 if report["passed"] else 1
    elif ns.cmd == "compare-source-archive":
        report = compare_source_archive(Path(ns.source), Path(ns.archive))
        if ns.report: write_json(Path(ns.report), report)
        print(json.dumps(report, indent=2))
        code = 0 if report["passed"] else 1
    elif ns.cmd == "init-template":
        report = init_template(Path(ns.source))
        if ns.report: write_json(Path(ns.report), report)
        print(json.dumps(report, indent=2))
    elif ns.cmd == "verify-built":
        report = run_loader_validate(Path(ns.loader), Path(ns.archive), Path(ns.report) if ns.report else Path("loader_verify_report.json"))
        print(json.dumps(report, indent=2))
        code = 0 if report["passed"] else 1
    raise SystemExit(code)

if __name__ == "__main__":
    import argparse
    main()
