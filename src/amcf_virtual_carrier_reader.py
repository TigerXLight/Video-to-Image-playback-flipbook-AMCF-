from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


RECOVERY_SCHEMA = "amcf-recovered-state-v1"
REQUIRED_LANES = [
    "timing_index_lane",
    "registration_lane",
    "payload_lane",
    "colour_registry_lane",
    "metadata_lane",
    "hash_checksum_lane",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


@dataclass
class VirtualCarrierReadResult:
    ok: bool
    section_count: int
    read_sections: list[dict[str, Any]]
    errors: list[str]
    unsafe_acceptance_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "section_count": self.section_count,
            "read_sections": self.read_sections,
            "errors": self.errors,
            "unsafe_acceptance_count": self.unsafe_acceptance_count,
        }


@dataclass
class RecoveredAMCFState:
    schema: str
    source_carrier_manifest: str
    recovered_frame_count: int
    recovered_frame_entries: list[dict[str, Any]]
    claim_boundary: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "source_carrier_manifest": self.source_carrier_manifest,
            "recovered_frame_count": self.recovered_frame_count,
            "recovered_frame_entries": self.recovered_frame_entries,
            "claim_boundary": self.claim_boundary,
            "created_by": "amcf_virtual_carrier_reader.py",
            "created_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        }


def _load_carrier_manifest(package_root: Path) -> tuple[dict[str, Any], list[str]]:
    manifest_path = package_root / "physical_carrier_manifest.json"
    errors: list[str] = []
    if not manifest_path.exists():
        return {}, ["carrier_manifest_missing"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"carrier_manifest_malformed:{exc}"]
    if manifest.get("physical_carrier_schema") != "amcf-physical-carrier-package-v1":
        errors.append("unsupported_or_missing_physical_carrier_schema")
    return manifest, errors


def read_physical_carrier_package(package_root: str | Path) -> VirtualCarrierReadResult:
    package_root = Path(package_root)
    manifest, errors = _load_carrier_manifest(package_root)
    sections = manifest.get("sections", []) if isinstance(manifest, dict) else []
    if not isinstance(sections, list):
        return VirtualCarrierReadResult(False, 0, [], errors + ["sections_not_list"])
    expected_count = int(manifest.get("section_count", -1) if isinstance(manifest, dict) else -1)
    if expected_count != len(sections):
        errors.append("section_count_mismatch")

    seen: set[int] = set()
    read_sections: list[dict[str, Any]] = []
    for expected_index, section in enumerate(sections):
        if not isinstance(section, dict):
            errors.append(f"section_entry_not_object:{expected_index}")
            continue
        section_index = int(section.get("section_index", -1))
        if section_index in seen:
            errors.append(f"duplicate_section_index:{section_index}")
        seen.add(section_index)
        if section_index != expected_index:
            errors.append(f"out_of_order_section_index:expected_{expected_index}_got_{section_index}")

        section_file_rel = str(section.get("section_file", ""))
        section_file = package_root / section_file_rel
        if not section_file.exists():
            errors.append(f"missing_section_file:{section_file_rel}")
            continue
        actual_hash = sha256_file(section_file)
        expected_hash = str(section.get("section_file_sha256", ""))
        if not expected_hash or actual_hash != expected_hash:
            errors.append(f"section_file_hash_mismatch:{section_file_rel}")
        text = section_file.read_text(encoding="utf-8")
        lanes = section.get("lanes", {})
        if not isinstance(lanes, dict):
            errors.append(f"lanes_not_object:{section_file_rel}")
            lanes = {}
        for lane in REQUIRED_LANES:
            if lane not in lanes:
                errors.append(f"manifest_missing_required_lane:{section_index}:{lane}")
            if f"[{lane}]" not in text:
                errors.append(f"section_file_missing_required_lane:{section_index}:{lane}")
        payload_lane = lanes.get("payload_lane", {})
        checksum_lane = lanes.get("hash_checksum_lane", {})
        payload_sha = payload_lane.get("source_payload_sha256")
        checksum_sha = checksum_lane.get("payload_sha256")
        if payload_sha != checksum_sha:
            errors.append(f"payload_hash_checksum_mismatch:{section_index}")
        read_sections.append({
            "section_index": section_index,
            "section_file": section_file_rel,
            "section_file_sha256": actual_hash,
            "source_payload_path": payload_lane.get("source_payload_path"),
            "source_payload_sha256": payload_sha,
            "lanes": lanes,
        })

    ok = not errors
    return VirtualCarrierReadResult(ok, len(read_sections), read_sections, errors)


def _infer_source_archive(package_root: Path, carrier_manifest: dict[str, Any], source_archive_path: str | Path | None) -> Path:
    if source_archive_path is not None:
        return Path(source_archive_path)
    source_name = str(carrier_manifest.get("source_archive", ""))
    candidate = package_root / source_name
    return candidate


def _read_payload_from_amcf_archive(source_archive: Path, payload_path: str, expected_sha256: str) -> bytes:
    with zipfile.ZipFile(source_archive, "r") as zf:
        names = set(zf.namelist())
        if payload_path not in names:
            raise ValueError(f"source_archive_missing_payload:{payload_path}")
        payload = zf.read(payload_path)
    actual = sha256_bytes(payload)
    if actual != expected_sha256:
        raise ValueError(f"source_archive_payload_hash_mismatch:{payload_path}")
    return payload


def recover_amcf_from_carrier_package(
    package_root: str | Path,
    output_root: str | Path,
    source_archive_path: str | Path | None = None,
    create_recovered_archive: bool = True,
) -> dict[str, Any]:
    package_root = Path(package_root)
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    manifest, manifest_errors = _load_carrier_manifest(package_root)
    read_result = read_physical_carrier_package(package_root)
    errors = list(manifest_errors) + list(read_result.errors)
    if errors:
        recovered = RecoveredAMCFState(
            schema=RECOVERY_SCHEMA,
            source_carrier_manifest="physical_carrier_manifest.json",
            recovered_frame_count=0,
            recovered_frame_entries=[],
            claim_boundary=_claim_boundary(),
        ).to_dict()
        (output_root / "recovered_amcf_manifest.json").write_text(json.dumps(recovered, indent=2, sort_keys=True), encoding="utf-8")
        return {
            "ok": False,
            "errors": errors,
            "recovered_manifest_path": str(output_root / "recovered_amcf_manifest.json"),
            "recovered_frame_count": 0,
            "unsafe_acceptance_count": 0,
        }

    source_archive = _infer_source_archive(package_root, manifest, source_archive_path)
    if not source_archive.exists():
        return {
            "ok": False,
            "errors": [f"source_archive_missing:{source_archive}"],
            "recovered_manifest_path": None,
            "recovered_frame_count": 0,
            "unsafe_acceptance_count": 0,
        }

    recovered_frames_dir = output_root / "recovered_frames"
    recovered_frames_dir.mkdir(parents=True, exist_ok=True)
    recovered_entries: list[dict[str, Any]] = []
    for section in read_result.read_sections:
        section_index = int(section["section_index"])
        payload_path = str(section["source_payload_path"])
        payload_sha = str(section["source_payload_sha256"])
        try:
            payload = _read_payload_from_amcf_archive(source_archive, payload_path, payload_sha)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        export_name = f"recovered_frame_{section_index:03d}.ppm"
        export_path = recovered_frames_dir / export_name
        export_path.write_bytes(payload)
        recovered_entries.append({
            "frame_index": section_index,
            "recovered_payload_path": f"recovered_frames/{export_name}",
            "source_payload_path": payload_path,
            "sha256": sha256_bytes(payload),
            "bytes": len(payload),
            "section_file": section["section_file"],
            "lane_hash_verified": True,
        })

    state = RecoveredAMCFState(
        schema=RECOVERY_SCHEMA,
        source_carrier_manifest="physical_carrier_manifest.json",
        recovered_frame_count=len(recovered_entries),
        recovered_frame_entries=recovered_entries,
        claim_boundary=_claim_boundary(),
    ).to_dict()
    manifest_path = output_root / "recovered_amcf_manifest.json"
    manifest_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    archive_path: Path | None = None
    if create_recovered_archive and not errors:
        archive_path = output_root / "recovered_video_source.amcf.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.json", json.dumps({
                "amcf_schema": "amcf-recovered-digital-smoke-v1",
                "source_type": "virtual_carrier_recovery",
                "archive_payload_kind": "recovered_frame_payloads",
                "frame_count": len(recovered_entries),
                "frame_entries": [
                    {
                        "frame_index": entry["frame_index"],
                        "payload_path": f"frames/frame_{entry['frame_index']:03d}.ppm",
                        "sha256": entry["sha256"],
                        "bytes": entry["bytes"],
                        "format": "ppm_p6",
                    }
                    for entry in recovered_entries
                ],
                "hash_algorithm": "sha256",
                "created_by": "amcf_virtual_carrier_reader.py",
                "claim_boundary": _claim_boundary(),
            }, indent=2, sort_keys=True))
            for entry in recovered_entries:
                zf.write(output_root / entry["recovered_payload_path"], f"frames/frame_{entry['frame_index']:03d}.ppm")

    return {
        "ok": not errors,
        "errors": errors,
        "read_result": read_result.to_dict(),
        "recovered_manifest_path": str(manifest_path),
        "recovered_archive_path": str(archive_path) if archive_path else None,
        "recovered_frame_count": len(recovered_entries),
        "recovered_frames_dir": str(recovered_frames_dir),
        "unsafe_acceptance_count": 0,
        "claim_boundary": _claim_boundary(),
    }


def export_recovered_frames(recovered_manifest_path: str | Path, export_root: str | Path) -> dict[str, Any]:
    recovered_manifest_path = Path(recovered_manifest_path)
    export_root = Path(export_root)
    state = json.loads(recovered_manifest_path.read_text(encoding="utf-8"))
    source_root = recovered_manifest_path.parent
    export_root.mkdir(parents=True, exist_ok=True)
    exported: list[dict[str, Any]] = []
    errors: list[str] = []
    for entry in state.get("recovered_frame_entries", []):
        src = source_root / entry["recovered_payload_path"]
        dst = export_root / Path(entry["recovered_payload_path"]).name
        if not src.exists():
            errors.append(f"recovered_payload_missing:{entry['recovered_payload_path']}")
            continue
        shutil.copy2(src, dst)
        exported.append({"frame_index": entry["frame_index"], "path": str(dst), "sha256": sha256_file(dst)})
    return {"ok": not errors, "exported_count": len(exported), "exported": exported, "errors": errors}


def validate_recovered_amcf_state(recovered_manifest_path: str | Path) -> dict[str, Any]:
    recovered_manifest_path = Path(recovered_manifest_path)
    errors: list[str] = []
    if not recovered_manifest_path.exists():
        return {"ok": False, "errors": ["recovered_manifest_missing"], "recovered_frame_count": 0, "unsafe_acceptance_count": 0}
    try:
        state = json.loads(recovered_manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"ok": False, "errors": [f"recovered_manifest_malformed:{exc}"], "recovered_frame_count": 0, "unsafe_acceptance_count": 0}
    if state.get("schema") != RECOVERY_SCHEMA:
        errors.append("unsupported_recovered_state_schema")
    entries = state.get("recovered_frame_entries", [])
    if int(state.get("recovered_frame_count", -1)) != len(entries):
        errors.append("recovered_frame_count_mismatch")
    seen: set[int] = set()
    for expected_index, entry in enumerate(entries):
        index = int(entry.get("frame_index", -1))
        if index in seen:
            errors.append(f"duplicate_recovered_frame_index:{index}")
        seen.add(index)
        if index != expected_index:
            errors.append(f"out_of_order_recovered_frame_index:expected_{expected_index}_got_{index}")
        payload = recovered_manifest_path.parent / str(entry.get("recovered_payload_path", ""))
        if not payload.exists():
            errors.append(f"recovered_payload_missing:{entry.get('recovered_payload_path')}")
            continue
        if sha256_file(payload) != entry.get("sha256"):
            errors.append(f"recovered_payload_hash_mismatch:{entry.get('recovered_payload_path')}")
    boundary = state.get("claim_boundary", {})
    for key in (
        "physical_proof_claimed",
        "hardware_validation_claimed",
        "final_ui_claimed",
        "manufacturing_readiness_claimed",
        "physical_prototype_built",
        "real_scanner_used",
        "actual_physical_scanning_claimed",
        "mp4_video_container_export_claimed",
    ):
        if boundary.get(key) is not False:
            errors.append(f"unsafe_claim_boundary:{key}")
    return {
        "ok": not errors,
        "errors": errors,
        "recovered_frame_count": int(state.get("recovered_frame_count", 0) or 0),
        "unsafe_acceptance_count": 0,
        "claim_boundary": boundary,
    }


def _claim_boundary() -> dict[str, bool]:
    return {
        "physical_proof_claimed": False,
        "hardware_validation_claimed": False,
        "final_ui_claimed": False,
        "manufacturing_readiness_claimed": False,
        "physical_prototype_built": False,
        "real_scanner_used": False,
        "actual_physical_scanning_claimed": False,
        "mp4_video_container_export_claimed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Read AMCF carrier sections and recover AMCF frame payload state.")
    sub = parser.add_subparsers(dest="command", required=True)
    read_cmd = sub.add_parser("read")
    read_cmd.add_argument("carrier_package")
    recover_cmd = sub.add_parser("recover")
    recover_cmd.add_argument("carrier_package")
    recover_cmd.add_argument("output_root")
    recover_cmd.add_argument("--source-archive")
    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("recovered_manifest")
    args = parser.parse_args()
    if args.command == "read":
        result = read_physical_carrier_package(args.carrier_package).to_dict()
    elif args.command == "recover":
        result = recover_amcf_from_carrier_package(args.carrier_package, args.output_root, args.source_archive)
    else:
        result = validate_recovered_amcf_state(args.recovered_manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
