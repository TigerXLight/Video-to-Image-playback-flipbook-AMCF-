from __future__ import annotations

"""Reproducible AMCF dependency and external-tool bootstrap.

The maintained AMCF package is intentionally source-first.  This module does
not vendor research repositories, model checkpoints, datasets, or FFmpeg
builds into the repository.  It can, when explicitly requested, install the
declared Python dependencies, clone pinned external repositories into a local
runtime directory, download checksummed checkpoints, and emit a runtime
config that the deep-inference adapters can consume.
"""

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any


MODULE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_PATH = MODULE_ROOT / "amcf_dependency_manifest.json"
SCHEMA = "amcf_dependency_manifest_v1"


DEFAULT_MANIFEST: dict[str, Any] = {
    "schema": SCHEMA,
    "base_requirements": "requirements.txt",
    "deep_python_packages": [
        "torch>=2.3.1",
        "torchvision>=0.18.1",
        "hydra-core>=1.3.2",
        "iopath>=0.1.10",
        "tqdm>=4.66.1",
    ],
    "external_tools": {
        "ffmpeg": {
            "executables": ["ffmpeg", "ffprobe"],
            "required_for": ["MP4 input", "MP4 export", "video diagnostics"],
            "automatic_download": False,
            "reason": "Use a user-selected Windows build and preserve its LGPL/GPL notices.",
        }
    },
    "resources": [
        {
            "id": "samurai_sam2",
            "kind": "repository",
            "url": "https://github.com/yangchris11/samurai.git",
            "ref": "76ba195984892b0d1e3db5d9c9f90bb62175680a",
            "relative_path": "repositories/SAMURAI",
            "adapter_path": "sam2",
            "license": "Apache-2.0; retain upstream notices and embedded SAM2 notices",
            "requires_noncommercial_acceptance": False,
            "install_paths": ["sam2"],
        },
        {
            "id": "cotracker",
            "kind": "repository",
            "url": "https://github.com/facebookresearch/co-tracker.git",
            "ref": "82e02e8029753ad4ef13cf06be7f4fc5facdda4d",
            "relative_path": "repositories/co-tracker",
            "adapter_path": ".",
            "license": "CC-BY-NC-4.0 for the majority of the repository; inspect per-file notices",
            "requires_noncommercial_acceptance": True,
            "install_paths": ["."],
        },
        {
            "id": "sam2_tiny_checkpoint",
            "kind": "checkpoint",
            "url": "https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_tiny.pt",
            "relative_path": "checkpoints/sam2.1_hiera_tiny.pt",
            "sha256": "7402E0D864FA82708A20FBD15BC84245C2F26DFF0EB43A4B5B93452DEB34BE69",
            "license": "Upstream SAM2/SAMURAI checkpoint terms; retain attribution and notices",
            "requires_noncommercial_acceptance": False,
        },
        {
            "id": "cotracker_baseline_offline_checkpoint",
            "kind": "checkpoint",
            "url": "https://huggingface.co/facebook/cotracker3/resolve/main/baseline_offline.pth",
            "relative_path": "checkpoints/baseline_offline.pth",
            "sha256": "DA09BBAC871F7398E5B29C4DE5213652658949737BC158840B101678BA8AD1DF",
            "license": "CC-BY-NC-4.0 / upstream model terms; research and non-commercial boundary",
            "requires_noncommercial_acceptance": True,
        },
    ],
    "claim_boundary": {
        "core_archive": "Deep tools are not required for source-independent AMCF archive playback.",
        "deep_inference": "SAM2/CoTracker are optional external research adapters and must retain upstream terms.",
        "hoot": "HOOT data and checkpoints are user-supplied; no dataset is silently downloaded or redistributed.",
        "physical": "No hardware, printer, reader, scanner, or manufactured-player validation is claimed.",
    },
}


def _json_load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        raise ValueError(f"invalid AMCF dependency manifest: {path}")
    return value


def load_manifest(path: str | Path | None = None) -> dict[str, Any]:
    manifest_path = Path(path).resolve() if path else DEFAULT_MANIFEST_PATH
    if manifest_path.exists():
        return _json_load(manifest_path)
    return json.loads(json.dumps(DEFAULT_MANIFEST))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _run(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout[-4000:].strip(),
        "stderr": completed.stderr[-4000:].strip(),
    }


def _module_status(name: str) -> dict[str, Any]:
    return {"module": name, "available": importlib.util.find_spec(name) is not None}


def _resource_path(dependency_root: Path, resource: dict[str, Any]) -> Path:
    return dependency_root / str(resource["relative_path"])


def _repo_status(path: Path, expected_ref: str, expected_url: str) -> dict[str, Any]:
    row: dict[str, Any] = {
        "path": str(path),
        "exists": path.is_dir(),
        "git_repository": (path / ".git").exists(),
        "expected_ref": expected_ref,
        "expected_url": expected_url,
        "ref_match": False,
        "remote_match": False,
    }
    if not row["git_repository"]:
        return row
    head = _run(["git", "-C", str(path), "rev-parse", "HEAD"])
    remote = _run(["git", "-C", str(path), "remote", "get-url", "origin"])
    actual_head = head["stdout"].splitlines()[-1] if head["stdout"] else ""
    actual_url = remote["stdout"].splitlines()[-1] if remote["stdout"] else ""
    row.update(
        {
            "actual_ref": actual_head,
            "actual_url": actual_url,
            "ref_match": actual_head.lower() == expected_ref.lower(),
            "remote_match": actual_url.rstrip("/").lower() == expected_url.removesuffix(".git").rstrip("/").lower(),
        }
    )
    return row


def _checkpoint_status(path: Path, expected_hash: str | None) -> dict[str, Any]:
    row: dict[str, Any] = {
        "path": str(path),
        "exists": path.is_file(),
        "bytes": path.stat().st_size if path.is_file() else 0,
        "expected_sha256": expected_hash or "",
        "sha256": "",
        "checksum_match": False,
    }
    if path.is_file():
        row["sha256"] = sha256(path)
        row["checksum_match"] = not expected_hash or row["sha256"].lower() == expected_hash.lower()
    return row


def check_setup(
    manifest: dict[str, Any],
    project_root: Path,
    dependency_root: Path,
    python_executable: Path | None = None,
    existing_config: Path | None = None,
) -> dict[str, Any]:
    python_executable = (python_executable or Path(sys.executable)).resolve()
    modules = [_module_status(name) for name in ("numpy", "PIL", "cv2", "torch", "sam2", "cotracker")]
    ffmpeg_spec = manifest.get("external_tools", {}).get("ffmpeg", {})
    ffmpeg = [
        {"executable": name, "path": shutil.which(name), "available": shutil.which(name) is not None}
        for name in ffmpeg_spec.get("executables", ["ffmpeg", "ffprobe"])
    ]
    resources: list[dict[str, Any]] = []
    for resource in manifest.get("resources", []):
        kind = resource.get("kind")
        root_path = _resource_path(dependency_root, resource)
        if kind == "repository":
            row = _repo_status(root_path, str(resource.get("ref", "")), str(resource.get("url", "")))
            adapter_path = str(resource.get("adapter_path", "."))
            row["adapter_path"] = str((root_path / adapter_path).resolve())
        else:
            row = _checkpoint_status(root_path, resource.get("sha256"))
        row.update(
            {
                "id": resource.get("id", ""),
                "kind": kind,
                "license": resource.get("license", ""),
                "requires_noncommercial_acceptance": bool(resource.get("requires_noncommercial_acceptance")),
            }
        )
        resources.append(row)

    existing = None
    if existing_config and existing_config.is_file():
        try:
            existing = json.loads(existing_config.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            existing = {"error": repr(exc)}

    deep_ready = True
    for row in resources:
        if row.get("kind") == "repository":
            deep_ready = deep_ready and bool(row.get("exists") and row.get("ref_match") and row.get("remote_match"))
        else:
            deep_ready = deep_ready and bool(row.get("exists") and row.get("checksum_match"))

    return {
        "schema": "amcf_setup_status_v1",
        "project_root": str(project_root),
        "dependency_root": str(dependency_root),
        "python": {"path": str(python_executable), "exists": python_executable.exists(), "version": sys.version},
        "python_modules": modules,
        "external_tools": ffmpeg,
        "resources": resources,
        "existing_config": str(existing_config) if existing_config else "",
        "existing_config_read": existing,
        "core_playback_requires_deep_tools": False,
        "deep_inference_ready": deep_ready,
    }


def _license_gate(resources: list[dict[str, Any]], upstream: bool, noncommercial: bool) -> list[str]:
    errors: list[str] = []
    if not upstream:
        errors.append("upstream licence acceptance is required for external repositories/checkpoints")
    if any(resource.get("requires_noncommercial_acceptance") for resource in resources) and not noncommercial:
        errors.append("--accept-noncommercial is required before preparing CoTracker resources")
    return errors


def _clone_repo(resource: dict[str, Any], target: Path) -> dict[str, Any]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not (target / ".git").exists():
        return {"id": resource["id"], "ok": False, "error": f"target exists but is not a git repository: {target}"}
    if not target.exists():
        clone = _run(["git", "clone", "--depth", "1", resource["url"], str(target)])
        if clone["returncode"] != 0:
            return {"id": resource["id"], "ok": False, "stage": "clone", **clone}
    fetch = _run(["git", "-C", str(target), "fetch", "--depth", "1", "origin", resource["ref"]])
    checkout = _run(["git", "-C", str(target), "checkout", "--force", resource["ref"]])
    ok = checkout["returncode"] == 0
    return {"id": resource["id"], "ok": ok, "stage": "checkout", "fetch": fetch, "checkout": checkout}


def _download_checkpoint(resource: dict[str, Any], target: Path, force: bool) -> dict[str, Any]:
    if target.exists() and not force:
        current = _checkpoint_status(target, resource.get("sha256"))
        return {"id": resource["id"], "ok": bool(current["checksum_match"]), "stage": "existing", "status": current}
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".part")
    try:
        with urllib.request.urlopen(resource["url"], timeout=60) as response, partial.open("wb") as handle:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                handle.write(block)
        partial.replace(target)
    except Exception as exc:
        partial.unlink(missing_ok=True)
        return {"id": resource["id"], "ok": False, "stage": "download", "error": repr(exc)}
    status = _checkpoint_status(target, resource.get("sha256"))
    return {"id": resource["id"], "ok": bool(status["checksum_match"]), "stage": "download", "status": status}


def _install_packages(packages: list[str], python_executable: Path, label: str) -> dict[str, Any]:
    if not packages:
        return {"label": label, "ok": True, "skipped": True}
    result = _run([str(python_executable), "-m", "pip", "install", *packages])
    return {"label": label, "ok": result["returncode"] == 0, **result}


def _install_repo(repo_root: Path, relative_paths: list[str], python_executable: Path, env: dict[str, str]) -> list[dict[str, Any]]:
    results = []
    for relative in relative_paths:
        path = (repo_root / relative).resolve()
        result = _run([str(python_executable), "-m", "pip", "install", "-e", str(path)], cwd=path, env=env)
        results.append({"path": str(path), "ok": result["returncode"] == 0, **result})
    return results


def write_runtime_config(path: Path, project_root: Path, dependency_root: Path, python_executable: Path) -> dict[str, Any]:
    def relative(value: Path) -> str:
        try:
            return os.path.relpath(value, project_root).replace("\\", "/")
        except ValueError:
            # Windows cannot express a relative path across drive letters.
            # Keep the runtime executable usable rather than writing a broken
            # path; repository-local dependency paths remain relative.
            return str(value)
    values = {
        "workspace_root": ".",
        "optional_deep_tools": {
            "deep_python": relative(python_executable),
            "sam2_repo": relative(dependency_root / "repositories" / "SAMURAI" / "sam2"),
            "sam2_checkpoint": relative(dependency_root / "checkpoints" / "sam2.1_hiera_tiny.pt"),
            "cotracker_repo": relative(dependency_root / "repositories" / "co-tracker"),
            "cotracker_checkpoint": relative(dependency_root / "checkpoints" / "baseline_offline.pth"),
        },
        "setup": {
            "dependency_root": relative(dependency_root),
            "source_video_required_for_deep_inference": True,
            "source_video_required_for_core_archive_playback": False,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(values, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return values


def run_setup(
    *,
    manifest_path: str | Path | None = None,
    project_root: str | Path | None = None,
    dependency_root: str | Path | None = None,
    python_executable: str | Path | None = None,
    existing_config: str | Path | None = None,
    install_research: bool = False,
    install_deep: bool = False,
    clone_repositories: bool = False,
    download_checkpoints: bool = False,
    accept_upstream_licenses: bool = False,
    accept_noncommercial: bool = False,
    force: bool = False,
    config_output: str | Path | None = None,
    report_output: str | Path | None = None,
) -> dict[str, Any]:
    project = Path(project_root).resolve() if project_root else Path.cwd().resolve()
    deps = Path(dependency_root).resolve() if dependency_root else project / ".amcf-runtime"
    python = Path(python_executable).resolve() if python_executable else Path(sys.executable).resolve()
    manifest = load_manifest(manifest_path)
    resources = list(manifest.get("resources", []))
    actions: list[dict[str, Any]] = []
    errors: list[str] = []

    prepare_repos = clone_repositories or install_deep
    prepare_checkpoints = download_checkpoints or install_deep
    if prepare_repos or prepare_checkpoints:
        errors.extend(_license_gate(resources, accept_upstream_licenses, accept_noncommercial))
    if not python.exists():
        errors.append(f"Python executable does not exist: {python}")

    if install_research and not errors:
        requirements = project / str(manifest.get("base_requirements", "requirements.txt"))
        if not requirements.is_file():
            errors.append(f"missing base requirements file: {requirements}")
        else:
            actions.append(_run([str(python), "-m", "pip", "install", "-r", str(requirements)], cwd=project))
            actions[-1]["label"] = "research_requirements"
            actions[-1]["ok"] = actions[-1]["returncode"] == 0

    if install_deep and not errors:
        actions.append(_install_packages(list(manifest.get("deep_python_packages", [])), python, "deep_python_packages"))

    repo_resources = [resource for resource in resources if resource.get("kind") == "repository"]
    if prepare_repos and not errors:
        for resource in repo_resources:
            actions.append(_clone_repo(resource, _resource_path(deps, resource)))
        if install_deep:
            install_env = dict(os.environ)
            install_env["SAM2_BUILD_CUDA"] = "0"
            install_env["SAM2_BUILD_ALLOW_ERRORS"] = "1"
            for resource in repo_resources:
                actions.extend(
                    _install_repo(
                        _resource_path(deps, resource),
                        list(resource.get("install_paths", [])),
                        python,
                        install_env,
                    )
                )

    checkpoint_resources = [resource for resource in resources if resource.get("kind") == "checkpoint"]
    if prepare_checkpoints and not errors:
        for resource in checkpoint_resources:
            actions.append(_download_checkpoint(resource, _resource_path(deps, resource), force))

    config_path = Path(config_output).resolve() if config_output else project / "amcf_runtime_config.json"
    config_data = write_runtime_config(config_path, project, deps, python)
    status = check_setup(
        manifest,
        project,
        deps,
        python,
        Path(existing_config).resolve() if existing_config else None,
    )
    errors.extend(str(action.get("error")) for action in actions if action.get("ok") is False and action.get("error"))
    result = {
        "schema": "amcf_setup_report_v1",
        "ok": not errors and all(action.get("ok", True) for action in actions),
        "project_root": str(project),
        "dependency_root": str(deps),
        "manifest": str(Path(manifest_path).resolve()) if manifest_path else str(DEFAULT_MANIFEST_PATH),
        "runtime_config": str(config_path),
        "runtime_config_values": config_data,
        "actions": actions,
        "errors": errors,
        "status": status,
        "claim_boundary": manifest.get("claim_boundary", {}),
        "notes": [
            "Core source-independent AMCF archive playback does not require the deep runtime.",
            "Deep inference requires the external repositories, compatible Python runtime, and checkpoints.",
            "Checkpoint bytes are never copied into the AMCF repository by this command.",
            "HOOT datasets remain user-supplied and are not downloaded implicitly.",
        ],
    }
    if report_output:
        report = Path(report_output).resolve()
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def build_setup_parser(parser: Any) -> Any:
    parser.add_argument("--manifest", help=f"Dependency manifest JSON (default: {DEFAULT_MANIFEST_PATH}).")
    parser.add_argument("--project-root", help="Repository root receiving the generated runtime config.")
    parser.add_argument("--dependency-root", help="External runtime directory; defaults to <project>/.amcf-runtime.")
    parser.add_argument("--python", dest="python_executable", help="Python executable used for pip and runtime config.")
    parser.add_argument("--existing-config", help="Optional existing AMCF config to include in the status report.")
    parser.add_argument("--install-research", action="store_true", help="Install the pinned base research requirements.txt.")
    parser.add_argument(
        "--install-deep",
        action="store_true",
        help="Install deep Python packages, clone pinned SAMURAI/CoTracker trees, and download their checkpoints.",
    )
    parser.add_argument("--clone-repositories", action="store_true", help="Clone/update pinned external research repositories.")
    parser.add_argument("--download-checkpoints", action="store_true", help="Download and checksum declared checkpoints.")
    parser.add_argument("--accept-upstream-licenses", action="store_true", help="Confirm that upstream repository/checkpoint terms were reviewed.")
    parser.add_argument("--accept-noncommercial", action="store_true", help="Confirm the CoTracker non-commercial/research boundary.")
    parser.add_argument("--force", action="store_true", help="Redownload an existing checkpoint after checksum verification is bypassed.")
    parser.add_argument("--config-output", help="Generated runtime config path.")
    parser.add_argument("--report-output", help="Optional JSON setup report path.")
    parser.add_argument("--check", action="store_true", help="Perform an availability check; this is the default when no action flag is used.")
    return parser


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Prepare and inspect AMCF external dependencies.")
    build_setup_parser(parser)
    args = parser.parse_args(argv)
    action_flags = any(
        getattr(args, name)
        for name in ("install_research", "install_deep", "clone_repositories", "download_checkpoints")
    )
    result = run_setup(
        manifest_path=args.manifest,
        project_root=args.project_root,
        dependency_root=args.dependency_root,
        python_executable=args.python_executable,
        existing_config=args.existing_config,
        install_research=args.install_research,
        install_deep=args.install_deep,
        clone_repositories=args.clone_repositories,
        download_checkpoints=args.download_checkpoints,
        accept_upstream_licenses=args.accept_upstream_licenses,
        accept_noncommercial=args.accept_noncommercial,
        force=args.force,
        config_output=args.config_output,
        report_output=args.report_output,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not action_flags:
        return 0
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
