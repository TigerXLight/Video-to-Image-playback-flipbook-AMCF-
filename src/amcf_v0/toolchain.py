from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
LOADER_MODULE = "amcf_v0.loader"
BUILDER_MODULE = "amcf_v0.builder"

def run(args):
    p = subprocess.run([PY] + [str(a) for a in args], cwd=str(ROOT.parents[1]), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return {"args": [str(a) for a in args], "returncode": p.returncode, "stdout": p.stdout, "passed": p.returncode == 0}

def component_manifest_ok(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["component_schema_name", "component_schema_version", "source_baseline", "source_fps", "source_frame_count", "components", "update_schedules", "mask_policy", "stream_policy", "compositor_policy", "visual_gate_policy", "limitations"]
    missing = [k for k in required if k not in data]
    ids = [c["component_id"] for c in data.get("components", [])]
    return {"path": str(path), "missing": missing, "component_count": len(ids), "component_ids": ids, "passed": not missing and bool(ids)}

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("validate-archive"); p.add_argument("archive"); p.add_argument("--report", default="")
    p = sub.add_parser("extract-archive"); p.add_argument("archive"); p.add_argument("--out", required=True)
    p = sub.add_parser("open-archive"); p.add_argument("archive"); p.add_argument("--out", required=True); p.add_argument("--no-launch", action="store_true")
    p = sub.add_parser("validate-source"); p.add_argument("source"); p.add_argument("--report", default="")
    p = sub.add_parser("build-source"); p.add_argument("source"); p.add_argument("--out", required=True); p.add_argument("--report", default="")
    p = sub.add_parser("validate-component-stream"); p.add_argument("manifest"); p.add_argument("--report", default="")
    p = sub.add_parser("inspect-manifest"); p.add_argument("manifest")
    p = sub.add_parser("inspect-components"); p.add_argument("manifest")
    p = sub.add_parser("full-check"); p.add_argument("source"); p.add_argument("archive"); p.add_argument("--extract-out", required=True)
    ns = ap.parse_args()
    if ns.cmd == "validate-archive":
        args = ["-m", LOADER_MODULE, "validate", ns.archive]
        if ns.report: args += ["--report", ns.report]
        out = run(args)
    elif ns.cmd == "extract-archive":
        out = run(["-m", LOADER_MODULE, "extract", ns.archive, "--out", ns.out])
    elif ns.cmd == "open-archive":
        args = ["-m", LOADER_MODULE, "open", ns.archive, "--out", ns.out]
        if ns.no_launch: args.append("--no-launch")
        out = run(args)
    elif ns.cmd == "validate-source":
        args = ["-m", BUILDER_MODULE, "validate-source", ns.source]
        if ns.report: args += ["--report", ns.report]
        out = run(args)
    elif ns.cmd == "build-source":
        args = ["-m", BUILDER_MODULE, "build", ns.source, "--out", ns.out]
        if ns.report: args += ["--report", ns.report]
        out = run(args)
    elif ns.cmd == "validate-component-stream":
        out = component_manifest_ok(Path(ns.manifest))
        if ns.report: Path(ns.report).write_text(json.dumps(out, indent=2), encoding="utf-8")
    elif ns.cmd in {"inspect-manifest", "inspect-components"}:
        data = json.loads(Path(ns.manifest).read_text(encoding="utf-8"))
        out = {"manifest": ns.manifest, "keys": sorted(data.keys()), "component_count": len(data.get("components", [])), "components": [c.get("component_id") for c in data.get("components", [])], "passed": True}
    elif ns.cmd == "full-check":
        out = {"validate_source": run(["-m", BUILDER_MODULE, "validate-source", ns.source]), "validate_archive": run(["-m", LOADER_MODULE, "validate", ns.archive]), "extract": run(["-m", LOADER_MODULE, "extract", ns.archive, "--out", ns.extract_out])}
        out["passed"] = all(v.get("passed") for v in out.values())
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out.get("passed") else 1)

if __name__ == "__main__":
    main()
