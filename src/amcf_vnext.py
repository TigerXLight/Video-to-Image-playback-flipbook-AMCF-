from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
MAIN = Path(__file__).resolve().parent
TESTS = WORKSPACE / "Tests"
DEFAULT_CONFIG = MAIN / "amcf_config.example.json"

CONTROLLED_LEVEL5_RUN = TESTS / "Test AMCF_CONTROLLED_LOST_RECOVERED_LEVEL5_PROOF" / "20261009_213727"
HOOT_LEVEL5_RUN = TESTS / "Test AMCF_HOOT_REAL_WORLD_LOST_RECOVERED_LEVEL5_SOLVER" / "20261009_220908"
ACCEPTANCE_RUN = TESTS / "Test AMCF_ACCEPTANCE_HARNESS_AND_CI_STYLE_REGRESSION" / "20261009_144608"
ARCHIVE_RUN = TESTS / "Test AMCF_ARCHIVE_WRITER_READER_INTEGRATION" / "20261009_150115"
RELEASE_SIGNOFF_RUN = TESTS / "Test AMCF_RELEASE_CANDIDATE_REVIEW_AND_SIGNOFF" / "20261009_153000"

DEFAULT_CONFIG_DATA: dict[str, Any] = {
    "workspace_root": "..",
    "proof_runs": {
        "controlled_level5": str(CONTROLLED_LEVEL5_RUN.relative_to(WORKSPACE)).replace("\\", "/"),
        "hoot_level5": str(HOOT_LEVEL5_RUN.relative_to(WORKSPACE)).replace("\\", "/"),
        "acceptance": str(ACCEPTANCE_RUN.relative_to(WORKSPACE)).replace("\\", "/"),
        "archive_writer_reader": str(ARCHIVE_RUN.relative_to(WORKSPACE)).replace("\\", "/"),
    },
    "optional_deep_tools": {
        "sam2_repo": "Github repos/SAMURAI/sam2",
        "sam2_checkpoint": "Tests/Test AMCF_LOCAL_DEEP_SEMANTIC_TOOLCHAIN_INTEGRATION/20261009_164833/02_CHECKPOINT_ACQUISITION/models/sam2.1_hiera_tiny.pt",
        "cotracker_repo": "Github repos/co-tracker",
        "cotracker_checkpoint": "Tests/Test AMCF_LOCAL_DEEP_SEMANTIC_TOOLCHAIN_INTEGRATION/20261009_164833/02_CHECKPOINT_ACQUISITION/models/baseline_offline.pth",
    },
    "adapters": {
        "primary_semantic_adapters": {
            "sam2": {
                "role": "high_precision_object_segmentation",
                "repo_key": "sam2_repo",
                "checkpoint_key": "sam2_checkpoint",
                "required_for_core_archive_playback": False,
                "required_for_semantic_level5_runs": True,
            },
            "cotracker": {
                "role": "persistent_point_and_identity_tracking",
                "repo_key": "cotracker_repo",
                "checkpoint_key": "cotracker_checkpoint",
                "required_for_core_archive_playback": False,
                "required_for_semantic_level5_runs": True,
            },
        },
        "future_optional_adapters": {
            "aot": "temporal_mask_propagation_candidate",
            "cutie": "temporal_mask_propagation_candidate",
            "xmem": "memory_based_video_object_segmentation_candidate",
            "xmem2": "memory_based_video_object_segmentation_candidate",
            "deva": "detection_plus_tracking_candidate",
            "raft": "dense_optical_flow_candidate",
            "tapnet": "point_tracking_candidate",
            "track_anything": "sam_track_integration_candidate",
        },
    },
    "claim_boundary": {
        "level5_scope": "Level 5 is claimed for controlled canonical and HOOT dataset-annotated proof vectors only.",
        "new_video_policy": "New videos must pass the same gates before receiving Level 5.",
    },
}

APPROVAL_TIERS = {
    "user_approved",
    "machine_validated",
    "machine_validated_controlled_ground_truth",
    "machine_validated_dataset_annotation",
    "machine_validated_not_user_approved",
    "machine_reviewed",
    "machine_reviewed_low_confidence",
    "candidate",
    "uncertain",
    "rejected",
    "",
}

VALIDATION_TIERS = {
    "lost_recovered_validated",
    "controlled_canonical_validated",
    "visible_absence_validated",
    "source_roi_semantic_identity_validated",
    "source_roi_persistent_motion_validated",
    "lowres_full_proxy_machine_validated",
    "identity_expanded_machine_validated",
    "long_range_identity_candidate",
    "medium_range_identity_candidate",
    "high_precision_candidate",
    "high_precision_machine_validated",
    "candidate",
    "uncertain",
    "rejected",
    "",
}


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {} if default is None else default


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({k for row in rows for k in row}) if rows else ["empty"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve_path(value: str | Path, base: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (base / path).resolve()


def load_config(config_path: str | None = None) -> dict[str, Any]:
    path = Path(config_path) if config_path else DEFAULT_CONFIG
    path = path.resolve()
    raw = read_json(path, DEFAULT_CONFIG_DATA) if path.exists() else dict(DEFAULT_CONFIG_DATA)
    if not isinstance(raw, dict):
        raw = dict(DEFAULT_CONFIG_DATA)
    workspace_raw = raw.get("workspace_root", "..")
    workspace = resolve_path(workspace_raw, path.parent if path.exists() else MAIN)
    config = dict(raw)
    config["_config_path"] = str(path)
    config["_config_exists"] = path.exists()
    config["_workspace"] = str(workspace)
    return config


def config_workspace(config: dict[str, Any]) -> Path:
    return Path(config.get("_workspace") or WORKSPACE).resolve()


def config_run(config: dict[str, Any], key: str, fallback: Path) -> Path:
    proof_runs = config.get("proof_runs") if isinstance(config.get("proof_runs"), dict) else {}
    value = proof_runs.get(key)
    if not value:
        return fallback
    return resolve_path(str(value), config_workspace(config))


def config_optional_path(config: dict[str, Any], key: str) -> Path | None:
    tools = config.get("optional_deep_tools") if isinstance(config.get("optional_deep_tools"), dict) else {}
    value = tools.get(key)
    if not value:
        return None
    return resolve_path(str(value), config_workspace(config))


def config_deep_python(config: dict[str, Any]) -> Path:
    configured = config_optional_path(config, "deep_python")
    if configured:
        return configured
    return Path(sys.executable).resolve()


def deep_runner_path() -> Path:
    installed_path = MAIN / "amcf_deep_semantic_inference.py"
    if installed_path.exists():
        return installed_path
    return MAIN / "src" / "amcf_deep_semantic_inference.py"


def hoot_runner_path() -> Path:
    installed_path = MAIN / "amcf_hoot_level5_inference.py"
    if installed_path.exists():
        return installed_path
    return MAIN / "src" / "amcf_hoot_level5_inference.py"


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", help=f"Path to AMCF config JSON. Default: {DEFAULT_CONFIG}")


def sidecar_rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [r for r in value if isinstance(r, dict)]
    if isinstance(value, dict):
        for key in ("entries", "semantic_entries", "objects", "frames", "rows"):
            rows = value.get(key)
            if isinstance(rows, list):
                return [r for r in rows if isinstance(r, dict)]
    return []


def proof_paths(config: dict[str, Any]) -> dict[str, dict[str, Path]]:
    controlled = config_run(config, "controlled_level5", CONTROLLED_LEVEL5_RUN)
    hoot = config_run(config, "hoot_level5", HOOT_LEVEL5_RUN)
    return {
        "controlled": {
            "root": controlled,
            "status": controlled / "04_FINAL_STATUS" / "final_status.json",
            "sidecar": controlled / "03_FULL_SEMANTIC_RECONSTRUCTION" / "semantic_sidecar_controlled_level5.json",
            "sheet": controlled / "03_FULL_SEMANTIC_RECONSTRUCTION" / "controlled_level5_reconstruction_sheet.jpg",
        },
        "hoot": {
            "root": hoot,
            "status": hoot / "07_FINAL_STATUS" / "final_status.json",
            "sidecar": hoot / "06_SEMANTIC_RECONSTRUCTION" / "semantic_sidecar_hoot_level5_candidate.json",
            "sheet": hoot / "03_EVENT_WINDOW_EVIDENCE" / "lost_recovered_real_world_event_sheet.jpg",
        },
    }


def validate_level5_status(name: str, status: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_true = [
        "general_semantic_object_amcf_solved",
        "high_precision_segmentation_solved",
        "lost_recovered_tracking_solved",
        "full_semantic_reconstruction_solved",
        "level5_claimed",
    ]
    for key in required_true:
        if status.get(key) is not True:
            errors.append(f"{name}: {key} is not true")
    boundary = str(status.get("claim_boundary") or status.get("level5_claim_boundary") or "")
    if name == "controlled" and "controlled" not in boundary.lower():
        errors.append("controlled: missing controlled claim boundary")
    if name == "hoot":
        if "hoot" not in boundary.lower() and "dataset" not in boundary.lower():
            errors.append("hoot: missing dataset/HOOT claim boundary")
    return errors


def validate_sidecar(path: Path) -> list[str]:
    errors: list[str] = []
    data = read_json(path, {})
    rows = sidecar_rows(data)
    if not rows:
        errors.append(f"{path}: no sidecar rows")
    for i, row in enumerate(rows[:5000]):
        approval = str(row.get("approval_tier", ""))
        validation = str(row.get("validation_tier", ""))
        if approval not in APPROVAL_TIERS:
            errors.append(f"{path}: row {i} invalid approval_tier {approval}")
        if validation not in VALIDATION_TIERS:
            errors.append(f"{path}: row {i} invalid validation_tier {validation}")
        if approval == "user_approved" and "machine" in str(row.get("reviewer_source", "")).lower():
            errors.append(f"{path}: row {i} fake user approval risk")
        for key in ("source_frame_path", "mask_path", "overlay_path"):
            value = row.get(key)
            if value and not Path(value).exists():
                errors.append(f"{path}: row {i} missing {key}: {value}")
    return errors


def cmd_status(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    paths = proof_paths(config)
    result = {
        "amcf_vnext_main_cli": True,
        "config_path": config["_config_path"],
        "config_exists": config["_config_exists"],
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "workspace": str(config_workspace(config)),
        "proofs": {},
        "acceptance_badge": "",
        "level5_claim_boundary": (config.get("claim_boundary") or {}).get(
            "level5_scope",
            "Level 5 is claimed for controlled canonical and HOOT dataset-annotated proof vectors only.",
        ),
    }
    for name, item in paths.items():
        status = read_json(item["status"], {})
        result["proofs"][name] = {
            "root": str(item["root"]),
            "status_path": str(item["status"]),
            "status_exists": item["status"].exists(),
            "sidecar_path": str(item["sidecar"]),
            "sidecar_exists": item["sidecar"].exists(),
            "sheet_path": str(item["sheet"]),
            "sheet_exists": item["sheet"].exists(),
            "level5_claimed": status.get("level5_claimed"),
            "highest_reconstruction_level": status.get("highest_reconstruction_level"),
        }
    acceptance_run = config_run(config, "acceptance", ACCEPTANCE_RUN)
    acc = acceptance_run / "04_ACCEPTANCE_STATUS" / "acceptance_badge.txt"
    if acc.exists():
        result["acceptance_badge"] = acc.read_text(encoding="utf-8", errors="ignore").strip()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_validate_level5(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for name, item in proof_paths(config).items():
        status = read_json(item["status"], {})
        proof_errors = validate_level5_status(name, status)
        sidecar_errors = validate_sidecar(item["sidecar"]) if item["sidecar"].exists() else [f"{name}: missing sidecar"]
        errors.extend(proof_errors)
        errors.extend(sidecar_errors)
        rows.append(
            {
                "proof": name,
                "status_exists": item["status"].exists(),
                "sidecar_exists": item["sidecar"].exists(),
                "level5_claimed": status.get("level5_claimed"),
                "highest_reconstruction_level": status.get("highest_reconstruction_level"),
                "errors": len(proof_errors) + len(sidecar_errors),
            }
        )
    result = {
        "ok": not errors,
        "proofs_checked": len(rows),
        "errors": errors[:100],
        "proof_rows": rows,
    }
    if args.output:
        out = Path(args.output)
        write_json(out / "main_level5_validation.json", result)
        write_csv(out / "main_level5_validation.csv", rows)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 2


def cmd_inspect_archive(args: argparse.Namespace) -> int:
    path = Path(args.archive)
    result: dict[str, Any] = {"archive": str(path), "exists": path.exists(), "ok": False, "errors": []}
    if not path.exists():
        result["errors"].append("missing archive")
    elif not zipfile.is_zipfile(path):
        result["errors"].append("not a zip archive")
    else:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            result.update(
                {
                    "ok": True,
                    "file_count": len(names),
                    "sample": names[:40],
                    "has_manifest": any(n.endswith("manifest.json") for n in names),
                    "has_claim_boundaries": any("claim" in n.lower() and n.endswith(".json") for n in names),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 2


def cmd_toolchain_status(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    adapters = config.get("adapters") if isinstance(config.get("adapters"), dict) else {}
    primary = adapters.get("primary_semantic_adapters") if isinstance(adapters.get("primary_semantic_adapters"), dict) else {}
    tools = []
    for key in ("sam2_repo", "sam2_checkpoint", "cotracker_repo", "cotracker_checkpoint"):
        path = config_optional_path(config, key)
        adapter_name = ""
        adapter_role = ""
        for name, spec in primary.items():
            if isinstance(spec, dict) and key in {spec.get("repo_key"), spec.get("checkpoint_key")}:
                adapter_name = str(name)
                adapter_role = str(spec.get("role", ""))
        tools.append(
            {
                "key": key,
                "path": str(path) if path else "",
                "exists": bool(path and path.exists()),
                "kind": "checkpoint" if "checkpoint" in key else "repo",
                "adapter_name": adapter_name,
                "adapter_role": adapter_role,
                "adapter_tier": "primary_semantic_adapter" if adapter_name else "configured_tool",
            }
        )
    deep_python = config_deep_python(config)
    modules = []
    for module in ("sam2", "cotracker", "cv2", "PIL"):
        modules.append({"module": module, "import_resolvable": importlib.util.find_spec(module) is not None})
    deep_runtime = {"path": str(deep_python), "exists": deep_python.exists(), "modules": [], "error": ""}
    if deep_python.exists():
        probe = subprocess.run(
            [
                str(deep_python),
                "-c",
                "import importlib.util; print({m: bool(importlib.util.find_spec(m)) for m in ('torch','sam2','cotracker','cv2','PIL')})",
            ],
            cwd=str(config_workspace(config)),
            capture_output=True,
            text=True,
            check=False,
        )
        deep_runtime["returncode"] = probe.returncode
        deep_runtime["stdout"] = probe.stdout.strip()
        deep_runtime["stderr"] = probe.stderr[-2000:].strip()
    else:
        deep_runtime["error"] = "configured deep Python does not exist"
    result = {
        "config_path": config["_config_path"],
        "optional_deep_tools_checked": True,
        "deep_tools_run": False,
        "deep_inference_entrypoint": str(deep_runner_path()),
        "deep_runtime": deep_runtime,
        "primary_semantic_adapters": primary,
        "future_optional_adapters": adapters.get("future_optional_adapters", {}),
        "tool_paths": tools,
        "python_modules": modules,
        "notes": [
            "This command checks path/import availability only.",
            "Use deep-inference to execute the configured external adapters.",
        ],
    }
    if args.output:
        out = Path(args.output)
        write_json(out / "toolchain_status.json", result)
        write_csv(out / "toolchain_paths.csv", tools)
        write_csv(out / "toolchain_modules.csv", modules)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_deep_inference(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    runner = deep_runner_path()
    deep_python = Path(args.deep_python).resolve() if args.deep_python else config_deep_python(config)
    if not runner.exists():
        print(json.dumps({"status": "failed", "error": f"missing deep inference runner: {runner}"}, indent=2))
        return 2
    if not deep_python.exists():
        print(json.dumps({"status": "failed", "error": f"missing deep inference Python: {deep_python}"}, indent=2))
        return 2
    values = {
        "sam2_repo": config_optional_path(config, "sam2_repo"),
        "sam2_checkpoint": config_optional_path(config, "sam2_checkpoint"),
        "cotracker_repo": config_optional_path(config, "cotracker_repo"),
        "cotracker_checkpoint": config_optional_path(config, "cotracker_checkpoint"),
    }
    missing = [key for key, value in values.items() if value is None or not value.exists()]
    if missing and not (args.skip_sam2 and args.skip_cotracker):
        print(json.dumps({"status": "failed", "error": "missing configured deep resources", "missing": missing}, indent=2))
        return 2
    command = [
        str(deep_python),
        str(runner),
        "--input",
        str(Path(args.input).resolve()),
        "--output",
        str(Path(args.output).resolve()),
        "--sam2-repo",
        str(values["sam2_repo"] or ""),
        "--sam2-checkpoint",
        str(values["sam2_checkpoint"] or ""),
        "--cotracker-repo",
        str(values["cotracker_repo"] or ""),
        "--cotracker-checkpoint",
        str(values["cotracker_checkpoint"] or ""),
        "--max-frames",
        str(args.max_frames),
        "--frame-step",
        str(args.frame_step),
        "--grid-size",
        str(args.grid_size),
        "--device",
        args.device,
    ]
    if args.bbox:
        command.extend(["--bbox", args.bbox])
    if args.skip_sam2:
        command.append("--skip-sam2")
    if args.skip_cotracker:
        command.append("--skip-cotracker")
    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    completed = subprocess.run(command, cwd=str(config_workspace(config)), env=env, text=True, check=False)
    return int(completed.returncode)


def cmd_hoot_level5(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    runner = hoot_runner_path()
    deep_python = Path(args.deep_python).resolve() if args.deep_python else config_deep_python(config)
    sam2_repo = config_optional_path(config, "sam2_repo")
    sam2_checkpoint = config_optional_path(config, "sam2_checkpoint")
    missing = [
        name
        for name, value in {
            "runner": runner,
            "deep_python": deep_python,
            "sam2_repo": sam2_repo,
            "sam2_checkpoint": sam2_checkpoint,
            "input": Path(args.input).resolve(),
        }.items()
        if value is None or not value.exists()
    ]
    if missing:
        print(json.dumps({"status": "failed", "error": "missing HOOT inference resource", "missing": missing}, indent=2))
        return 2
    command = [
        str(deep_python),
        str(runner),
        "--input",
        str(Path(args.input).resolve()),
        "--output",
        str(Path(args.output).resolve()),
        "--sam2-repo",
        str(sam2_repo),
        "--sam2-checkpoint",
        str(sam2_checkpoint),
        "--max-visible-masks",
        str(args.max_visible_masks),
        "--device",
        args.device,
    ]
    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    completed = subprocess.run(command, cwd=str(config_workspace(config)), env=env, text=True, check=False)
    return int(completed.returncode)


def cmd_config(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    result = {
        "config_path": config["_config_path"],
        "config_exists": config["_config_exists"],
        "workspace": str(config_workspace(config)),
        "proof_runs": {
            "controlled_level5": str(config_run(config, "controlled_level5", CONTROLLED_LEVEL5_RUN)),
            "hoot_level5": str(config_run(config, "hoot_level5", HOOT_LEVEL5_RUN)),
            "acceptance": str(config_run(config, "acceptance", ACCEPTANCE_RUN)),
            "archive_writer_reader": str(config_run(config, "archive_writer_reader", ARCHIVE_RUN)),
        },
        "optional_deep_tools": {
            key: str(config_optional_path(config, key) or "")
            for key in ("sam2_repo", "sam2_checkpoint", "cotracker_repo", "cotracker_checkpoint")
        },
        "deep_python": str(config_deep_python(config)),
        "claim_boundary": config.get("claim_boundary", {}),
    }
    if args.output:
        out = Path(args.output)
        write_json(out / "resolved_config.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_run_legacy(args: argparse.Namespace) -> int:
    scripts = {
        "test02": MAIN / "amcf_test02.py",
        "tracking-test03a": MAIN / "amcf_tracking_test03a.py",
        "decode-test": MAIN / "test_archive_decode.py",
    }
    script = scripts[args.target]
    if not script.exists():
        print(json.dumps({"ok": False, "error": f"missing script: {script}"}, indent=2))
        return 2
    if args.dry_run:
        print(json.dumps({"ok": True, "dry_run": True, "command": [sys.executable, str(script)]}, indent=2))
        return 0
    completed = subprocess.run([sys.executable, str(script)], cwd=str(WORKSPACE), check=False)
    return int(completed.returncode)


def cmd_github_manifest(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    include = [
        "Main/amcf_vnext.py",
        "Main/amcf_config.example.json",
        "Main/amcf_test02.py",
        "Main/amcf_tracking_test03a.py",
        "Main/test_archive_decode.py",
        "Main/README.md",
        "Main/DEPENDENCIES_AND_PROVENANCE.md",
        "Main/requirements.txt",
        "Main/RUN_AMCF_VNEXT.cmd",
        "Main/RUN_TEST02.cmd",
        "Main/RUN_TRACKING_TEST03A.cmd",
    ]
    optional_lightweight = [
        "Tests/Test AMCF_RELEASE_CANDIDATE_LIGHTWEIGHT_PACKAGE/20261009_152539/02_RELEASE_CANDIDATE_FOLDER/AMCF_RELEASE_CANDIDATE_LIGHTWEIGHT",
        "Tests/Test AMCF_CONTROLLED_LOST_RECOVERED_LEVEL5_PROOF/20261009_213727/04_FINAL_STATUS/final_status.json",
        "Tests/Test AMCF_HOOT_REAL_WORLD_LOST_RECOVERED_LEVEL5_SOLVER/20261009_220908/07_FINAL_STATUS/final_status.json",
    ]
    exclude = [
        ".venv*",
        "Github repos/",
        "Original/",
        "Test media/",
        "Tests/**/frames/",
        "Tests/**/masks/",
        "Tests/**/overlays/",
        "Tests/**/roi_frames/",
        "Tests/**/proxy_frames/",
        "Tests/**/01_HOOT_DOWNLOAD/*.zip",
        "Tests/**/02_HOOT_EXTRACTED/",
        "*.mp4",
        "*.avi",
        "*.zip",
        "__pycache__/",
    ]
    result = {
        "config_path": config["_config_path"],
        "include_core": include,
        "include_optional_lightweight_references": optional_lightweight,
        "exclude_from_github": exclude,
        "notes": [
            "Do not commit model checkpoints, source videos, downloaded datasets, generated frame floods, or venvs.",
            "Keep SAM2/CoTracker as optional external/local dependencies unless their licenses and distribution plan are explicitly accepted.",
        ],
    }
    if args.output:
        out = Path(args.output)
        write_json(out / "github_upload_manifest.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_smoke(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    output = Path(args.output) if args.output else None
    status_code = cmd_validate_level5(argparse.Namespace(output=str(output) if output else None, config=args.config))
    archive_run = config_run(config, "archive_writer_reader", ARCHIVE_RUN)
    archives = sorted((archive_run / "03_SMALL_TEST_ARCHIVES").glob("*.amcfvnext.zip"))
    archive_rows = []
    for archive in archives[:6]:
        archive_rows.append({"archive": str(archive), "exists": archive.exists(), "is_zip": zipfile.is_zipfile(archive), "bytes": archive.stat().st_size})
    result = {"level5_validation_exit": status_code, "archives_seen": len(archives), "archive_rows": archive_rows, "ok": status_code == 0 and all(r["is_zip"] for r in archive_rows)}
    if output:
        write_json(output / "main_smoke_results.json", result)
        write_csv(output / "main_smoke_archives.csv", archive_rows)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AMCF v-next Main integration CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("status", help="Show AMCF v-next proof/runtime status.")
    add_common_args(p)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("config", help="Resolve and print AMCF v-next config paths.")
    add_common_args(p)
    p.add_argument("--output", help="Optional output directory for resolved config JSON.")
    p.set_defaults(func=cmd_config)

    p = sub.add_parser("validate-level5", help="Validate controlled and HOOT Level 5 proof artifacts.")
    add_common_args(p)
    p.add_argument("--output", help="Optional output directory for JSON/CSV validation results.")
    p.set_defaults(func=cmd_validate_level5)

    p = sub.add_parser("inspect-archive", help="Inspect a small AMCF v-next zip archive.")
    p.add_argument("archive")
    p.set_defaults(func=cmd_inspect_archive)

    p = sub.add_parser("toolchain-status", help="Check configured SAM2/CoTracker path/import availability without running inference.")
    add_common_args(p)
    p.add_argument("--output", help="Optional output directory for toolchain status JSON/CSV.")
    p.set_defaults(func=cmd_toolchain_status)

    p = sub.add_parser("deep-inference", help="Run external SAM2/CoTracker inference and write bounded AMCF diagnostic evidence.")
    add_common_args(p)
    p.add_argument("--input", required=True, help="Input video, image, or frame directory.")
    p.add_argument("--output", required=True, help="Output directory for inference evidence.")
    p.add_argument("--deep-python", help="Override configured Python runtime for deep inference.")
    p.add_argument("--bbox", help="SAM2 box prompt x0,y0,x1,y1; defaults to a central box.")
    p.add_argument("--max-frames", type=int, default=8)
    p.add_argument("--frame-step", type=int, default=1)
    p.add_argument("--grid-size", type=int, default=4)
    p.add_argument("--device", default="cpu", choices=("cpu", "cuda"))
    p.add_argument("--skip-sam2", action="store_true")
    p.add_argument("--skip-cotracker", action="store_true")
    p.set_defaults(func=cmd_deep_inference)

    p = sub.add_parser("hoot-level5", help="Run the bounded HOOT annotated lost/recovered semantic proof with real SAM2 inference.")
    add_common_args(p)
    p.add_argument("--input", required=True, help="Extracted HOOT sequence directory or explicit HOOT zip archive.")
    p.add_argument("--output", required=True, help="Output directory for reproducible HOOT evidence.")
    p.add_argument("--deep-python", help="Override configured Python runtime for deep inference.")
    p.add_argument("--max-visible-masks", type=int, default=36)
    p.add_argument("--device", default="cpu", choices=("cpu", "cuda"))
    p.set_defaults(func=cmd_hoot_level5)

    p = sub.add_parser("github-manifest", help="Emit recommended GitHub include/exclude lists.")
    add_common_args(p)
    p.add_argument("--output", help="Optional output directory for manifest JSON.")
    p.set_defaults(func=cmd_github_manifest)

    p = sub.add_parser("run-legacy", help="Route legacy Main scripts through this single app entrypoint.")
    p.add_argument("target", choices=["test02", "tracking-test03a", "decode-test"])
    p.add_argument("--dry-run", action="store_true", help="Print the delegated command without running it.")
    p.set_defaults(func=cmd_run_legacy)

    p = sub.add_parser("smoke", help="Run a local Main-facing smoke test.")
    add_common_args(p)
    p.add_argument("--output", help="Optional output directory for smoke artifacts.")
    p.set_defaults(func=cmd_smoke)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
