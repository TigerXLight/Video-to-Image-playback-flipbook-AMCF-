from __future__ import annotations
import csv, hashlib, html.parser, json, re, shutil, zipfile
from pathlib import Path

FORBIDDEN_PARTS = {".git", "venv", ".venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache"}
FORBIDDEN_SUFFIXES = {".zip", ".amcfv0.zip", ".pt", ".pth", ".ckpt", ".safetensors", ".onnx"}
FORBIDDEN_NAME_CONTAINS = ["checkpoint", "raw_frames", "browser cache", "thumbs.db", ".ds_store"]

class RefParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        for key, val in attrs:
            if key in {"src", "href"} and val:
                self.refs.append((f"{tag}:{key}", val))

def posix_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()

def is_unsafe_rel_name(name: str) -> bool:
    fixed = name.replace("\\", "/")
    parts = [p for p in fixed.split("/") if p]
    lower = [p.lower() for p in parts]
    if fixed.startswith("/") or re.match(r"^[a-zA-Z]:", fixed) or ".." in parts:
        return True
    if any(ord(c) < 32 for c in fixed):
        return True
    if any(part in FORBIDDEN_PARTS for part in lower):
        return True
    low = fixed.lower()
    if any(s in low for s in FORBIDDEN_NAME_CONTAINS):
        return True
    if low.endswith(".amcfv0.zip") or low.endswith(".zip"):
        return True
    if Path(fixed).suffix.lower() in {".pt", ".pth", ".ckpt", ".safetensors", ".onnx"}:
        return True
    return False

def source_files(root: Path):
    rows = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rows.append(p)
    return rows

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))

def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")

def write_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})

def html_refs(path: Path):
    parser = RefParser()
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    parser.feed(text)
    refs = list(parser.refs)
    for m in re.finditer(r"show(?:Video|Image)\('([^']+)'\)", text):
        refs.append(("js:media", m.group(1)))
    return refs

def validate_viewer_links(root: Path):
    viewers = sorted((root / "viewer").glob("OPEN_FIRST*.html")) if (root / "viewer").exists() else []
    rows = []
    missing = []
    external = []
    for viewer in viewers:
        for typ, val in html_refs(viewer):
            if not val or val.startswith(("#", "javascript:", "data:")) or "+src+" in val:
                continue
            if val.startswith(("http://", "https://", "//")):
                row = {"source_file": posix_rel(viewer, root), "reference_type": typ, "reference_value": val, "resolved_path": val, "exists": False, "notes": "external"}
                external.append(row)
            else:
                target = (viewer.parent / val).resolve()
                exists = target.exists() and str(target).startswith(str(root.resolve()))
                row = {"source_file": posix_rel(viewer, root), "reference_type": typ, "reference_value": val, "resolved_path": str(target), "exists": exists, "notes": ""}
                if not exists:
                    missing.append(row)
            rows.append(row)
    return {"viewers_found": [posix_rel(v, root) for v in viewers], "rows": rows, "missing": missing, "external": external, "passed": bool(viewers) and not missing and not external}

def probe_media(root: Path):
    rows = []
    try:
        import cv2
    except Exception:
        cv2 = None
    try:
        from PIL import Image
    except Exception:
        Image = None
    for p in sorted((root / "media").glob("*")) if (root / "media").exists() else []:
        if not p.is_file():
            continue
        row = {"path": posix_rel(p, root), "exists": True, "readable": False, "width": 0, "height": 0, "fps": 0, "frame_count": 0, "notes": ""}
        if p.suffix.lower() in {".png", ".jpg", ".jpeg"} and Image:
            try:
                im = Image.open(p)
                row.update({"readable": True, "width": im.width, "height": im.height, "frame_count": 1, "notes": "image"})
            except Exception as e:
                row["notes"] = str(e)
        elif p.suffix.lower() in {".mp4", ".mkv", ".mov"} and cv2:
            cap = cv2.VideoCapture(str(p))
            if cap.isOpened():
                row.update({
                    "readable": True,
                    "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0),
                    "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0),
                    "fps": round(float(cap.get(cv2.CAP_PROP_FPS) or 0), 6),
                    "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0),
                })
            else:
                row["notes"] = "OpenCV could not decode"
            cap.release()
        rows.append(row)
    required = {"media/original_vs_best_visual_baseline.mp4", "media/candidate_only_best_visual_baseline.mp4"}
    have = {r["path"] for r in rows if r["readable"]}
    return {"rows": rows, "required_media_present": sorted(required & have), "missing_required_media": sorted(required - have), "passed": required.issubset(have)}
