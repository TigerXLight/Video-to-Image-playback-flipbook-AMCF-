
from __future__ import annotations
import argparse, csv, html.parser, json, os, re, shutil, sys, zipfile, subprocess
from pathlib import Path

FORBIDDEN_PARTS = {"venv", ".venv", "node_modules", ".git", "__pycache__"}
EXPECTED = [
    "viewer/OPEN_FIRST_AMCF_04B_VIEWER.html",
    "viewer/OPEN_FIRST_AMCF_04B_README.md",
    "manifest/AMCF_04B_ARCHIVE_MANIFEST.json",
    "media/original_vs_best_visual_baseline.mp4",
    "media/candidate_only_best_visual_baseline.mp4",
    "docs/visual_gate_rules.md",
]

class RefParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]
    def handle_starttag(self, tag, attrs):
        for k,v in attrs:
            if k in {"src","href"} and v:
                self.refs.append((f"{tag}:{k}", v))

def is_unsafe_zip_name(name: str) -> bool:
    p = Path(name)
    parts = [x.lower() for x in p.parts]
    if Path(name).is_absolute() or ".." in p.parts or re.match(r"^[a-zA-Z]:", name):
        return True
    if any(ord(c) < 32 for c in name):
        return True
    if any(part in FORBIDDEN_PARTS for part in parts):
        return True
    if "checkpoint" in name.lower() or "raw_frames" in name.lower():
        return True
    return False

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

def archive_names(path: Path):
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        return z.namelist(), bad

def validate_viewer(root: Path):
    viewer = root / "viewer" / "OPEN_FIRST_AMCF_04B_VIEWER.html"
    txt = read_text(viewer)
    parser = RefParser(); parser.feed(txt)
    refs = parser.refs
    for m in re.finditer(r"show(?:Video|Image)\('([^']+)'\)", txt):
        refs.append(("js:media", m.group(1)))
    rows=[]; missing=[]; external=[]
    for typ,val in refs:
        if not val or val.startswith(("#","javascript:","data:")) or "+src+" in val:
            continue
        if val.startswith(("http://","https://","//")):
            exists=False; resolved=val; external.append(val); notes="external"
        else:
            rp=(viewer.parent / val).resolve(); exists=rp.exists(); resolved=str(rp); notes=""
        row={"reference_type":typ,"reference_value":val,"resolved_path":resolved,"exists":exists,"notes":notes}
        rows.append(row)
        if not exists: missing.append(row)
    return {"viewer_exists": viewer.exists(), "references_checked": len(rows), "missing_references": missing, "external_urls": external, "passed": viewer.exists() and not missing and not external, "rows": rows}

def media_probe(root: Path):
    targets=["media/original_vs_best_visual_baseline.mp4","media/candidate_only_best_visual_baseline.mp4","media/original_vs_best_visual_baseline_2x.mp4","media/trunk_parallax_texture_audit.mp4","media/right_foreground_trunk_contact_sheet.png","media/waterfall_fidelity_contact_sheet.png"]
    rows=[]
    try:
        import cv2
        from PIL import Image
    except Exception:
        cv2=None; Image=None
    for rel in targets:
        p=root/rel
        if not p.exists(): continue
        row={"path":rel,"exists":True,"readable":False,"width":0,"height":0,"fps":0,"frame_count":0,"notes":""}
        if p.suffix.lower() in {".png",".jpg",".jpeg"} and Image:
            try:
                im=Image.open(p); row.update({"readable":True,"width":im.width,"height":im.height,"frame_count":1,"notes":"image"})
            except Exception as e: row["notes"]=str(e)
        elif cv2:
            cap=cv2.VideoCapture(str(p))
            if cap.isOpened():
                fps=float(cap.get(cv2.CAP_PROP_FPS) or 0); fc=int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
                row.update({"readable":True,"width":int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0),"height":int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0),"fps":round(fps,6),"frame_count":fc})
            else:
                row["notes"]="OpenCV could not decode"
            cap.release()
        rows.append(row)
    required = {r["path"]: r for r in rows}
    passed = "media/original_vs_best_visual_baseline.mp4" in required and "media/candidate_only_best_visual_baseline.mp4" in required
    return {"rows": rows, "passed": passed and all(required[k]["exists"] for k in ["media/original_vs_best_visual_baseline.mp4","media/candidate_only_best_visual_baseline.mp4"])}

def validate_extracted(root: Path):
    manifest_path=root/"manifest"/"AMCF_04B_ARCHIVE_MANIFEST.json"
    try: manifest=json.loads(read_text(manifest_path)); manifest_ok=True
    except Exception: manifest={}; manifest_ok=False
    viewer=validate_viewer(root)
    media=media_probe(root)
    docs_ok=(root/"docs"/"visual_gate_rules.md").exists()
    return {"root":str(root),"manifest_status":manifest_ok,"manifest":manifest,"viewer_status":viewer["passed"],"media_status":media["passed"],"docs_status":docs_ok,"viewer_path":str((root/"viewer"/"OPEN_FIRST_AMCF_04B_VIEWER.html").resolve()),"passed":manifest_ok and viewer["passed"] and media["passed"] and docs_ok,"viewer_links":viewer["rows"],"media_rows":media["rows"]}

def cmd_info(args):
    path=Path(args.archive)
    names,bad=archive_names(path)
    manifest={}
    with zipfile.ZipFile(path) as z:
        if "manifest/AMCF_04B_ARCHIVE_MANIFEST.json" in names:
            manifest=json.loads(z.read("manifest/AMCF_04B_ARCHIVE_MANIFEST.json").decode("utf-8","replace"))
    print("AMCF v0 archive")
    print("not final codec:", manifest.get("not_final_codec"))
    print("primary viewer:", manifest.get("primary_viewer"))
    print("primary video:", manifest.get("primary_video"))
    print("candidate video:", manifest.get("candidate_only_video"))
    print("entries:", len(names))
    return {"archive":str(path),"zip_test_ok":bad is None,"entry_count":len(names),"manifest":manifest,"passed":bad is None}

def safe_extract(archive: Path, out: Path):
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    skipped=[]
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            if is_unsafe_zip_name(info.filename):
                skipped.append(info.filename); continue
            target=(out/info.filename).resolve()
            if not str(target).startswith(str(out.resolve())):
                skipped.append(info.filename); continue
            if info.is_dir(): target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src,dst)
    return skipped

def cmd_extract(args):
    archive=Path(args.archive); out=Path(args.out)
    skipped=safe_extract(archive,out)
    val=validate_extracted(out)
    report={"archive":str(archive),"output_folder":str(out),"skipped_entries":skipped,"validation":val,"viewer_path":val["viewer_path"],"passed":val["passed"] and not skipped}
    print("viewer:", val["viewer_path"])
    return report

def cmd_validate(args):
    archive=Path(args.archive)
    names,bad=archive_names(archive)
    unsafe=[n for n in names if is_unsafe_zip_name(n)]
    expected={e:e in names for e in EXPECTED}
    temp=Path(args.out) if args.out else archive.parent/"_amcfv0_validate_extract"
    skipped=safe_extract(archive,temp)
    val=validate_extracted(temp)
    report={"archive":str(archive),"zip_test_ok":bad is None,"unsafe_entries":unsafe,"expected_entries":expected,"skipped_entries":skipped,"extracted_validation":val,"passed":bad is None and not unsafe and all(expected.values()) and val["passed"]}
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("VALID" if report["passed"] else "INVALID")
    return report

def cmd_open(args):
    report=cmd_extract(args)
    viewer=report["viewer_path"]
    opened=False
    if not args.no_launch:
        try:
            os.startfile(viewer); opened=True
        except Exception:
            opened=False
    report["browser_launch_attempted"]=not args.no_launch
    report["browser_launch_success"]=opened
    report["open_path_exists"]=Path(viewer).exists()
    return report

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd", required=True)
    for c in ["info","validate","extract","open"]:
        p=sub.add_parser(c); p.add_argument("archive")
        if c in {"validate","extract","open"}: p.add_argument("--out", default="")
        if c=="validate": p.add_argument("--report", default="")
        if c=="open": p.add_argument("--no-launch", action="store_true")
    ns=ap.parse_args()
    if ns.cmd=="info": report=cmd_info(ns)
    elif ns.cmd=="validate": report=cmd_validate(ns)
    elif ns.cmd=="extract": report=cmd_extract(ns)
    elif ns.cmd=="open": report=cmd_open(ns)
    else: raise SystemExit(2)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
