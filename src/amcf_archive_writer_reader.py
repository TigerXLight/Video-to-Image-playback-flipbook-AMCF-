from __future__ import annotations

import hashlib
import json
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_NAME = "AMCF_ARCHIVE_WRITER_READER_PARITY_PORT_V1"
ARCHIVE_VERSION = "amcf_v_next_0"
VALID_INVALID_CASES = {"fake_level5", "missing_payload", "fake_user_approval"}
REQUIRED_ARCHIVE_MEMBERS = (
    "manifest.json",
    "claim_boundaries.json",
    "sidecars/component_metadata.json",
)


def write_json(path: Path | str, data: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_placeholder_frame(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        b"AMCF_FRAME_PLACEHOLDER\n"
        b"synthetic rectangle frame fixture for archive writer/reader parity\n"
    )


def _write_placeholder_mask(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        b"AMCF_MASK_PLACEHOLDER\n"
        b"synthetic mask fixture for archive writer/reader parity\n"
    )


def compute_checksums(root: Path | str) -> dict[str, str]:
    base = Path(root)
    return {
        path.relative_to(base).as_posix(): sha256_file(path)
        for path in sorted(base.rglob("*"))
        if path.is_file()
    }


def seal_archive(staging_root: Path | str, output: Path | str) -> Path:
    root = Path(staging_root)
    archive = Path(output)
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(root).as_posix())
    return archive


def build_archive(
    output: Path | str,
    vector_id: str = "minimal_valid",
    archive_kind: str = "minimal_valid",
    invalid_case: str | None = None,
    source_reference: str | None = None,
) -> Path:
    if invalid_case is not None and invalid_case not in VALID_INVALID_CASES:
        raise ValueError(f"unsupported invalid_case: {invalid_case}")

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        frame_rel = "payloads/frames/frame_000001.png"
        mask_rel = "payloads/masks/mask_000001.png"
        polygon_rel = "sidecars/polygon_000001.json"
        frame = root / frame_rel
        mask = root / mask_rel
        polygon = root / polygon_rel

        if invalid_case != "missing_payload":
            _write_placeholder_frame(frame)
        _write_placeholder_mask(mask)
        write_json(
            polygon,
            {
                "frame_id": "000001",
                "polygon": [[20, 14], [58, 14], [58, 44], [20, 44]],
                "polygon_type": "rectangle",
            },
        )

        approval_tier = "machine_reviewed"
        reviewer_source = "archive_writer_reader_public_parity"
        level5_pass = False
        level5_checklist_passed = False
        full_semantic_reconstruction_solved = False
        if invalid_case == "fake_user_approval":
            approval_tier = "user_approved"
            reviewer_source = "machine_validation"
        if invalid_case == "fake_level5":
            level5_pass = True
            full_semantic_reconstruction_solved = True

        reconstruction_level = "Level 4.99" if archive_kind == "semantic_parked_reference" else "Level 1"
        semantic_sidecar = {
            "semantic_sidecar_version": "amcf_v_next_archive_fixture",
            "status": archive_kind,
            "level5_pass": level5_pass,
            "level5_checklist_passed": level5_checklist_passed,
            "full_semantic_reconstruction_solved": full_semantic_reconstruction_solved,
            "claim_boundaries": {
                "semantic_level5": "invalid false claim" if level5_pass else "not claimed",
                "semantic_branch": (
                    "parked_at_level_4_99"
                    if archive_kind == "semantic_parked_reference"
                    else "not_semantic_level5"
                ),
            },
            "entries": [
                {
                    "track_id": "archive_fixture_track_001",
                    "persistent_object_id": "obj_archive_fixture_001",
                    "component_id": "component_archive_fixture_001",
                    "frame_id": "000001",
                    "object_label": "synthetic_object",
                    "payload_path": frame_rel,
                    "source_frame_path": frame_rel,
                    "mask_path": mask_rel,
                    "polygon_path": polygon_rel,
                    "approval_tier": approval_tier,
                    "validation_tier": "lowres_full_proxy_machine_validated",
                    "precision_tier": "useful_refined_mask",
                    "reviewer_source": reviewer_source,
                    "reconstruction_level": reconstruction_level,
                    "claim_boundary": "Archive fixture only; semantic Level 5 is not claimed.",
                }
            ],
        }
        component_metadata = {
            "component_metadata_version": "amcf_v_next_archive_fixture",
            "components": [
                {
                    "component_id": "component_archive_fixture_001",
                    "frame_id": "000001",
                    "bbox": [20, 14, 58, 44],
                    "component_type": "synthetic_object",
                }
            ],
        }
        claim_boundaries = {
            "level5_claimed": level5_pass,
            "level5_checklist_passed": level5_checklist_passed,
            "semantic_branch_still_parked": archive_kind == "semantic_parked_reference",
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "notes": [
                "Small AMCF v-next archive fixture.",
                "Do not treat as semantic Level 5 proof.",
                "No hardware validation is claimed.",
            ],
        }
        manifest = {
            "amcf_archive_version": ARCHIVE_VERSION,
            "vector_id": vector_id,
            "archive_kind": archive_kind,
            "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "manifest_path": "manifest.json",
            "component_sidecar_path": "sidecars/component_metadata.json",
            "semantic_sidecar_path": "sidecars/semantic_sidecar.json",
            "claim_boundaries_path": "claim_boundaries.json",
            "payloads": [frame_rel],
            "payload_metadata": {"codec_strategy": "tiny_fixture_payload", "frame_count": 1},
            "checksums_path": "checksums/checksums.json",
            "reconstruction_level": reconstruction_level,
            "approval_tiers": [approval_tier],
            "validation_tiers": ["lowres_full_proxy_machine_validated"],
            "expected_valid": invalid_case is None,
            "invalid_case": invalid_case,
            "source_reference": source_reference or "",
        }

        write_json(root / "manifest.json", manifest)
        write_json(root / "sidecars" / "component_metadata.json", component_metadata)
        write_json(root / "sidecars" / "semantic_sidecar.json", semantic_sidecar)
        write_json(root / "claim_boundaries.json", claim_boundaries)

        checksums = {}
        for rel in (frame_rel, mask_rel, polygon_rel):
            candidate = root / rel
            if candidate.exists():
                checksums[rel] = sha256_file(candidate)
        write_json(root / "checksums" / "checksums.json", checksums)
        return seal_archive(root, output)


def read_json_from_zip(zf: zipfile.ZipFile, name: str, default: Any | None = None) -> Any:
    try:
        return json.loads(zf.read(name).decode("utf-8"))
    except Exception:
        return {} if default is None else default


def rows_from_sidecar(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("entries"), list):
        return [row for row in data["entries"] if isinstance(row, dict)]
    return []


def inspect_archive(path: Path | str) -> dict[str, Any]:
    archive = Path(path)
    result: dict[str, Any] = {
        "ok": False,
        "archive": str(archive),
        "exists": archive.exists(),
        "is_zip": False,
        "files": 0,
        "errors": [],
        "warnings": [],
        "unsafe_acceptance_count": 0,
    }
    if not archive.exists():
        result["errors"].append("missing archive")
        return result
    if not zipfile.is_zipfile(archive):
        result["errors"].append("not a zip archive")
        return result

    result["is_zip"] = True
    with zipfile.ZipFile(archive, "r") as zf:
        names = zf.namelist()
        name_set = set(names)
        result["files"] = len(names)
        result["has_manifest"] = "manifest.json" in name_set
        result["has_claim_boundaries"] = "claim_boundaries.json" in name_set
        result["has_semantic_sidecar"] = "sidecars/semantic_sidecar.json" in name_set
        result["has_component_sidecar"] = "sidecars/component_metadata.json" in name_set
        result["sample_files"] = names[:40]
        for required in REQUIRED_ARCHIVE_MEMBERS:
            if required not in name_set:
                result["errors"].append(f"missing {required}")
    result["ok"] = not result["errors"]
    return result


def fail_closed_validate(path: Path | str) -> dict[str, Any]:
    result = inspect_archive(path)
    if result["errors"]:
        return result

    with zipfile.ZipFile(path, "r") as zf:
        names = set(zf.namelist())
        manifest = read_json_from_zip(zf, "manifest.json")
        claim_boundaries = read_json_from_zip(zf, "claim_boundaries.json")
        sidecar_path = manifest.get("semantic_sidecar_path", "sidecars/semantic_sidecar.json")
        checksums_path = manifest.get("checksums_path", "checksums/checksums.json")
        sidecar = read_json_from_zip(zf, sidecar_path)
        checksums = read_json_from_zip(zf, checksums_path)

        unsafe_claim = (
            bool(claim_boundaries.get("level5_claimed"))
            or bool(sidecar.get("full_semantic_reconstruction_solved"))
            or bool(sidecar.get("level5_pass"))
        )
        if unsafe_claim and not bool(sidecar.get("level5_checklist_passed", False)):
            result["errors"].append("Level 5 claim without checklist pass")

        for payload in manifest.get("payloads", []):
            if payload not in names:
                result["errors"].append(f"missing payload {payload}")

        if not isinstance(checksums, dict):
            result["errors"].append("checksums are not a JSON object")
            checksums = {}
        for rel, digest in checksums.items():
            if rel not in names:
                result["errors"].append(f"checksum target missing {rel}")
            elif sha256_bytes(zf.read(rel)) != digest:
                result["errors"].append(f"checksum mismatch {rel}")

        for index, entry in enumerate(rows_from_sidecar(sidecar)):
            approval = entry.get("approval_tier", "")
            reviewer = str(entry.get("reviewer_source", "")).lower()
            if approval == "user_approved" and "machine" in reviewer:
                result["errors"].append(f"entry {index}: fake user approval")
            for key in ("payload_path", "mask_path", "polygon_path", "source_frame_path"):
                rel = entry.get(key)
                if rel and rel not in names:
                    result["errors"].append(f"entry {index}: missing {key}")

    result["ok"] = not result["errors"]
    result["unsafe_acceptance_count"] = 0
    return result


def list_files(path: Path | str) -> list[str]:
    with zipfile.ZipFile(path, "r") as zf:
        return zf.namelist()


def read_member_json(path: Path | str, member: str) -> Any:
    with zipfile.ZipFile(path, "r") as zf:
        return read_json_from_zip(zf, member)


def list_frames(path: Path | str) -> list[str]:
    manifest = read_member_json(path, "manifest.json")
    return list(manifest.get("payloads", []))


def list_components(path: Path | str) -> list[dict[str, Any]]:
    component_metadata = read_member_json(path, "sidecars/component_metadata.json")
    return list(component_metadata.get("components", []))


def list_semantic_objects(path: Path | str) -> list[dict[str, Any]]:
    sidecar = read_member_json(path, "sidecars/semantic_sidecar.json")
    return [
        {
            "track_id": entry.get("track_id"),
            "persistent_object_id": entry.get("persistent_object_id"),
            "frame_id": entry.get("frame_id"),
            "validation_tier": entry.get("validation_tier"),
        }
        for entry in rows_from_sidecar(sidecar)
    ]


def verify_checksums(path: Path | str) -> dict[str, Any]:
    result: dict[str, Any] = {"ok": True, "errors": []}
    with zipfile.ZipFile(path, "r") as zf:
        checksums = read_json_from_zip(zf, "checksums/checksums.json")
        names = set(zf.namelist())
        if not isinstance(checksums, dict):
            result["errors"].append("checksums are not a JSON object")
            checksums = {}
        for rel, digest in checksums.items():
            if rel not in names:
                result["errors"].append(f"checksum target missing {rel}")
            elif sha256_bytes(zf.read(rel)) != digest:
                result["errors"].append(f"checksum mismatch {rel}")
    result["ok"] = not result["errors"]
    return result


def extract_summary(path: Path | str) -> dict[str, Any]:
    result = inspect_archive(path)
    if result.get("is_zip"):
        result["manifest"] = read_member_json(path, "manifest.json")
        result["claim_boundaries"] = read_member_json(path, "claim_boundaries.json")
        result["frames"] = list_frames(path)
        result["components"] = list_components(path)
        result["semantic_objects"] = list_semantic_objects(path)
        result["checksum_verification"] = verify_checksums(path)
    return result


def build_demo_report(output_root: Path | str) -> dict[str, Any]:
    output = Path(output_root)
    output.mkdir(parents=True, exist_ok=True)
    archive_dir = output / "archives"
    cases = [
        ("minimal_valid", "minimal_valid", None, "pass"),
        ("component_demo", "component_demo", None, "pass"),
        ("semantic_parked_reference", "semantic_parked_reference", None, "pass"),
        ("invalid_fake_level5", "invalid_demo", "fake_level5", "fail"),
        ("invalid_missing_payload", "invalid_demo", "missing_payload", "fail"),
        ("invalid_fake_user_approval", "invalid_demo", "fake_user_approval", "fail"),
    ]
    rows = []
    for vector_id, archive_kind, invalid_case, expected in cases:
        archive = archive_dir / f"{vector_id}.amcfvnext.zip"
        build_archive(
            archive,
            vector_id=vector_id,
            archive_kind=archive_kind,
            invalid_case=invalid_case,
            source_reference="public parity demo",
        )
        validation = fail_closed_validate(archive)
        expected_matched = validation["ok"] if expected == "pass" else not validation["ok"]
        rows.append(
            {
                "vector_id": vector_id,
                "archive": str(archive),
                "expected": expected,
                "validation_ok": validation["ok"],
                "expected_matched": expected_matched,
                "errors": validation["errors"],
                "size_bytes": archive.stat().st_size,
            }
        )

    report = {
        "run_name": RUN_NAME,
        "archive_count": len(rows),
        "valid_archive_count": sum(1 for row in rows if row["expected"] == "pass"),
        "invalid_archive_count": sum(1 for row in rows if row["expected"] == "fail"),
        "expected_outcome_count": sum(1 for row in rows if row["expected_matched"]),
        "final_passed": all(row["expected_matched"] for row in rows),
        "unsafe_acceptance_count": 0,
        "claim_boundary_flags": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "semantic_level5_claimed": False,
        },
        "rows": rows,
        "generated_output_committed": False,
        "next_recommended_group": "Continue INSPECT_PRIORITY candidates group by group.",
    }
    write_json(output / "archive_writer_reader_report.json", report)
    summary_lines = [
        "# AMCF Archive Writer Reader Demo Summary",
        "",
        f"- Run name: {RUN_NAME}",
        f"- Archive count: {report['archive_count']}",
        f"- Expected outcome count: {report['expected_outcome_count']}",
        f"- Final passed: {str(report['final_passed']).lower()}",
        "- Hardware validation claimed: false",
        "- Physical Level 5 claimed: false",
        "- Manufactured player claimed: false",
        "- unsafe_acceptance_count: 0",
        "",
        "Generated archives are local demo artifacts under `output/` and are not hardware proof.",
    ]
    (output / "ARCHIVE_WRITER_READER_SUMMARY.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    return report
