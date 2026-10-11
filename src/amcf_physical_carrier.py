from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PHYSICAL_CARRIER_SCHEMA = "amcf-physical-carrier-package-v1"
SECTION_FILE_SUFFIX = ".amcfsection.txt"
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


def _read_amcf_manifest(archive_path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(archive_path, "r") as zf:
        if "manifest.json" not in zf.namelist():
            raise ValueError("AMCF archive missing manifest.json")
        manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
    if "frame_entries" not in manifest:
        raise ValueError("AMCF archive manifest missing frame_entries")
    return manifest


@dataclass
class PhysicalCarrierSection:
    section_index: int
    source_payload_path: str
    source_payload_sha256: str
    section_file: str
    lanes: dict[str, Any]
    section_file_sha256: str = ""

    def to_manifest_entry(self) -> dict[str, Any]:
        return {
            "section_index": self.section_index,
            "source_payload_path": self.source_payload_path,
            "source_payload_sha256": self.source_payload_sha256,
            "section_file": self.section_file,
            "section_file_sha256": self.section_file_sha256,
            "lanes": self.lanes,
        }


@dataclass
class PhysicalCarrierManifest:
    carrier_id: str
    source_archive: str
    source_archive_sha256: str
    section_count: int
    sections: list[PhysicalCarrierSection]

    def to_dict(self) -> dict[str, Any]:
        return {
            "physical_carrier_schema": PHYSICAL_CARRIER_SCHEMA,
            "carrier_id": self.carrier_id,
            "source_archive": self.source_archive,
            "source_archive_sha256": self.source_archive_sha256,
            "layout_mode": "vertical_stack_indexed_section_physical_medium",
            "default_notation": "indexed sections, not left-to-right flipbook and not continuous ribbon",
            "section_count": self.section_count,
            "lane_schema": REQUIRED_LANES,
            "sections": [section.to_manifest_entry() for section in self.sections],
            "claim_boundary": {
                "physical_proof_claimed": False,
                "hardware_validation_claimed": False,
                "final_ui_claimed": False,
                "manufacturing_readiness_claimed": False,
                "physical_prototype_built": False,
                "real_printing_performed": False,
            },
            "created_by": "amcf_physical_carrier.py",
            "created_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        }


def _lane_metadata(frame_entry: dict[str, Any], section_index: int, frame_count: int) -> dict[str, Any]:
    frame_sha = str(frame_entry["sha256"])
    return {
        "timing_index_lane": {
            "section_index": section_index,
            "section_count": frame_count,
            "marker": f"TIMING-{section_index:04d}",
            "index_code": f"{section_index:04d}/{frame_count:04d}",
        },
        "registration_lane": {
            "corner_marks": ["top_left", "top_right", "bottom_left", "bottom_right"],
            "orientation": "indexed_section_upright",
            "datum": "top_left_registration_origin",
        },
        "payload_lane": {
            "payload_kind": "frame_reference_payload",
            "source_payload_path": str(frame_entry["payload_path"]),
            "source_payload_sha256": frame_sha,
            "format": str(frame_entry.get("format", "ppm_p6")),
            "width": int(frame_entry.get("width", 0)),
            "height": int(frame_entry.get("height", 0)),
        },
        "colour_registry_lane": {
            "swatches": ["black", "white", "red", "green", "blue", "cyan", "magenta", "yellow"],
            "profile": "amcf_smoke_reference_swatches",
            "degraded": False,
        },
        "metadata_lane": {
            "source_frame_index": int(frame_entry["frame_index"]),
            "fps_reference": "from_amcf_manifest",
            "transform": {"x": 0, "y": 0, "scale_x": 1.0, "scale_y": 1.0, "rotation_degrees": 0.0},
        },
        "hash_checksum_lane": {
            "hash_algorithm": "sha256",
            "payload_sha256": frame_sha,
            "section_index_sha256": hashlib.sha256(f"{section_index}:{frame_sha}".encode("utf-8")).hexdigest(),
        },
    }


def _section_text(section_index: int, lanes: dict[str, Any]) -> str:
    lines = [
        "AMCF PHYSICAL CARRIER SECTION",
        f"section_index: {section_index:04d}",
        "layout_mode: vertical_stack_indexed_section_physical_medium",
        "default_notation: indexed sections, not left-to-right flipbook and not continuous ribbon",
        "",
    ]
    for lane_name in REQUIRED_LANES:
        lines.append(f"[{lane_name}]")
        lines.append(json.dumps(lanes[lane_name], sort_keys=True))
        lines.append("")
    lines.extend([
        "[claim_boundary]",
        json.dumps({
            "physical_proof_claimed": False,
            "hardware_validation_claimed": False,
            "real_printing_performed": False,
            "manufacturing_readiness_claimed": False,
        }, sort_keys=True),
        "",
    ])
    return "\n".join(lines)


def generate_physical_carrier_from_amcf_archive(
    amcf_archive_path: str | Path,
    output_root: str | Path,
    carrier_id: str = "AMCF-CARRIER-SMOKE-001",
) -> dict[str, Any]:
    amcf_archive_path = Path(amcf_archive_path)
    output_root = Path(output_root)
    sections_dir = output_root / "carrier_sections"
    sections_dir.mkdir(parents=True, exist_ok=True)
    amcf_manifest = _read_amcf_manifest(amcf_archive_path)
    frame_entries = list(amcf_manifest["frame_entries"])
    sections: list[PhysicalCarrierSection] = []
    frame_count = len(frame_entries)

    for index, frame_entry in enumerate(frame_entries):
        lanes = _lane_metadata(frame_entry, index, frame_count)
        section_file = sections_dir / f"section_{index:04d}{SECTION_FILE_SUFFIX}"
        section_file.write_text(_section_text(index, lanes), encoding="utf-8")
        sections.append(
            PhysicalCarrierSection(
                section_index=index,
                source_payload_path=str(frame_entry["payload_path"]),
                source_payload_sha256=str(frame_entry["sha256"]),
                section_file=f"carrier_sections/{section_file.name}",
                lanes=lanes,
                section_file_sha256=sha256_file(section_file),
            )
        )

    manifest = PhysicalCarrierManifest(
        carrier_id=carrier_id,
        source_archive=amcf_archive_path.name,
        source_archive_sha256=sha256_file(amcf_archive_path),
        section_count=frame_count,
        sections=sections,
    ).to_dict()
    manifest_path = output_root / "physical_carrier_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return {
        "ok": True,
        "carrier_manifest_path": str(manifest_path),
        "section_count": frame_count,
        "lane_layout_present": True,
        "section_files": [section.section_file for section in sections],
        "claim_boundary": manifest["claim_boundary"],
    }


def validate_physical_carrier_package(package_root: str | Path) -> dict[str, Any]:
    package_root = Path(package_root)
    manifest_path = package_root / "physical_carrier_manifest.json"
    errors: list[str] = []
    warnings: list[str] = []
    manifest: dict[str, Any] = {}
    validated_sections = 0

    if not manifest_path.exists():
        return {
            "ok": False,
            "manifest_exists": False,
            "section_count": 0,
            "validated_sections": 0,
            "lane_layout_present": False,
            "errors": ["carrier_manifest_missing"],
            "warnings": [],
            "unsafe_acceptance_count": 0,
        }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("physical_carrier_schema") != PHYSICAL_CARRIER_SCHEMA:
        errors.append("unsupported_or_missing_physical_carrier_schema")
    if manifest.get("layout_mode") != "vertical_stack_indexed_section_physical_medium":
        errors.append("layout_mode_not_vertical_stack_indexed_section")
    lane_schema = manifest.get("lane_schema", [])
    for lane in REQUIRED_LANES:
        if lane not in lane_schema:
            errors.append(f"lane_schema_missing:{lane}")
    sections = manifest.get("sections", [])
    if int(manifest.get("section_count", -1)) != len(sections):
        errors.append("section_count_mismatch")
    boundary = manifest.get("claim_boundary", {})
    for key in (
        "physical_proof_claimed",
        "hardware_validation_claimed",
        "final_ui_claimed",
        "manufacturing_readiness_claimed",
        "physical_prototype_built",
        "real_printing_performed",
    ):
        if boundary.get(key) is not False:
            errors.append(f"unsafe_claim_boundary:{key}")

    for section in sections:
        section_file = package_root / str(section.get("section_file", ""))
        if not section_file.exists():
            errors.append(f"missing_section:{section.get('section_file')}")
            continue
        text = section_file.read_text(encoding="utf-8")
        for lane in REQUIRED_LANES:
            if f"[{lane}]" not in text:
                errors.append(f"section_missing_lane:{section_file.name}:{lane}")
            if lane not in section.get("lanes", {}):
                errors.append(f"manifest_section_missing_lane:{section_file.name}:{lane}")
        expected_hash = str(section.get("section_file_sha256", ""))
        actual_hash = sha256_file(section_file)
        if not expected_hash or expected_hash != actual_hash:
            errors.append(f"section_file_hash_mismatch:{section_file.name}")
        payload_lane = section.get("lanes", {}).get("payload_lane", {})
        checksum_lane = section.get("lanes", {}).get("hash_checksum_lane", {})
        if payload_lane.get("source_payload_sha256") != checksum_lane.get("payload_sha256"):
            errors.append(f"payload_checksum_lane_mismatch:{section_file.name}")
        validated_sections += 1

    return {
        "ok": not errors,
        "manifest_exists": True,
        "physical_carrier_schema": manifest.get("physical_carrier_schema"),
        "section_count": int(manifest.get("section_count", 0) or 0),
        "validated_sections": validated_sections,
        "lane_layout_present": all(lane in manifest.get("lane_schema", []) for lane in REQUIRED_LANES),
        "errors": errors,
        "warnings": warnings,
        "unsafe_acceptance_count": 0,
        "claim_boundary": manifest.get("claim_boundary", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or validate an AMCF printable/indexed physical carrier package.")
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate")
    gen.add_argument("amcf_archive")
    gen.add_argument("output_root")
    val = sub.add_parser("validate")
    val.add_argument("package_root")
    args = parser.parse_args()
    if args.command == "generate":
        result = generate_physical_carrier_from_amcf_archive(args.amcf_archive, args.output_root)
    else:
        result = validate_physical_carrier_package(args.package_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
