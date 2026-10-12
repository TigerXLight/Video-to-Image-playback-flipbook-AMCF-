from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field, is_dataclass
from pathlib import Path
from typing import Any


MODEL_VERSION = "amcf_shared_package_model_v1"
REQUIRED_SECTION_LANES = (
    "timing_lane",
    "index_lane",
    "registration_lane",
    "image_payload_lane",
    "colour_registry_lane",
    "metadata_lane",
    "checksum_hash_lane",
)
CLAIM_BOUNDARY_FLAGS = {
    "hardware_validation_claimed": False,
    "physical_level_5_claimed": False,
    "manufactured_player_claimed": False,
    "real_printer_required": False,
    "real_reader_required": False,
    "real_player_required": False,
    "real_scanner_required": False,
    "real_usb_required": False,
}


@dataclass(frozen=True)
class AMCFClaimBoundary:
    hardware_validation_claimed: bool = False
    physical_level_5_claimed: bool = False
    manufactured_player_claimed: bool = False
    real_printer_required: bool = False
    real_reader_required: bool = False
    real_player_required: bool = False
    real_scanner_required: bool = False
    real_usb_required: bool = False
    summary: str = "software/no-hardware shared AMCF package baseline"


@dataclass(frozen=True)
class AMCFUpdateEvent:
    event_id: str
    section_id: str
    timestamp_ms: int
    dwell_ms: int
    update_reason: str
    source_frame_ref: str | None = None


@dataclass(frozen=True)
class AMCFPhysicalSection:
    section_id: str
    section_index: int
    timestamp_start_ms: int
    timestamp_end_ms: int
    update_event_id: str
    lanes: dict[str, str]
    payload_ref: str
    payload_hash: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AMCFManifest:
    manifest_id: str
    source_amcf_id: str
    schedule_id: str
    section_count: int
    update_events: list[AMCFUpdateEvent]
    physical_sections: list[AMCFPhysicalSection]
    claim_boundary: AMCFClaimBoundary = field(default_factory=AMCFClaimBoundary)


@dataclass(frozen=True)
class AMCFPackage:
    package_id: str
    model_version: str
    manifest: AMCFManifest
    package_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AMCFPackageValidationReport:
    final_passed: bool
    checks_passed: list[str]
    checks_failed: list[str]
    warnings: list[str]
    unsafe_acceptance_count: int
    claim_boundary_flags: dict[str, bool]


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def object_to_dict(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, list):
        return [object_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {key: object_to_dict(value) for key, value in obj.items()}
    return obj


def write_json(path: str | Path, data: Any) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(object_to_dict(data), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def default_lanes(section_id: str) -> dict[str, str]:
    return {lane: f"{section_id}:{lane}" for lane in REQUIRED_SECTION_LANES}


def build_demo_shared_package() -> AMCFPackage:
    events = [
        AMCFUpdateEvent("update-000", "section-000", 0, 120, "initial_visible_state", "frame-000"),
        AMCFUpdateEvent("update-001", "section-001", 120, 180, "component_state_changed", "frame-003"),
        AMCFUpdateEvent("update-002", "section-002", 300, 160, "component_state_changed", "frame-006"),
    ]
    sections: list[AMCFPhysicalSection] = []
    for index, event in enumerate(events):
        payload_ref = f"payloads/{event.section_id}.json"
        payload_hash = stable_hash(f"{event.event_id}:{event.section_id}:{event.timestamp_ms}")
        sections.append(
            AMCFPhysicalSection(
                section_id=event.section_id,
                section_index=index,
                timestamp_start_ms=event.timestamp_ms,
                timestamp_end_ms=event.timestamp_ms + event.dwell_ms,
                update_event_id=event.event_id,
                lanes=default_lanes(event.section_id),
                payload_ref=payload_ref,
                payload_hash=payload_hash,
                metadata={"source_frame_ref": event.source_frame_ref, "fixture": True},
            )
        )
    manifest = AMCFManifest(
        manifest_id="manifest-demo-software-io-v1",
        source_amcf_id="amcf-demo-source",
        schedule_id="schedule-demo-update-events",
        section_count=len(sections),
        update_events=events,
        physical_sections=sections,
    )
    return AMCFPackage(
        package_id="package-demo-software-io-v1",
        model_version=MODEL_VERSION,
        manifest=manifest,
        package_metadata={"software_control_only": True, "fixture": True},
    )


def validate_shared_package(package: AMCFPackage) -> AMCFPackageValidationReport:
    passed: list[str] = []
    failed: list[str] = []
    warnings: list[str] = []
    manifest = package.manifest
    if package.model_version == MODEL_VERSION:
        passed.append("model_version_supported")
    else:
        failed.append("model_version_unsupported")
    if manifest.section_count == len(manifest.physical_sections):
        passed.append("section_count_matches")
    else:
        failed.append("section_count_mismatch")
    section_ids = [section.section_id for section in manifest.physical_sections]
    if len(section_ids) == len(set(section_ids)):
        passed.append("section_ids_unique")
    else:
        failed.append("duplicate_section_id")
    event_ids = {event.event_id for event in manifest.update_events}
    event_section_ids = {event.section_id for event in manifest.update_events}
    if set(section_ids).issubset(event_section_ids):
        passed.append("sections_have_update_events")
    else:
        failed.append("section_without_update_event")
    for section in manifest.physical_sections:
        missing = [lane for lane in REQUIRED_SECTION_LANES if lane not in section.lanes]
        if missing:
            failed.append(f"missing_required_lanes:{section.section_id}:{','.join(missing)}")
        if section.update_event_id not in event_ids:
            failed.append(f"unknown_update_event:{section.section_id}:{section.update_event_id}")
        if not section.payload_hash:
            failed.append(f"missing_payload_hash:{section.section_id}")
    if not failed:
        passed.append("required_lanes_and_hashes_present")
    boundary = object_to_dict(manifest.claim_boundary)
    for key, expected in CLAIM_BOUNDARY_FLAGS.items():
        if boundary.get(key) is not expected:
            failed.append(f"unsafe_claim_boundary:{key}")
    if not warnings:
        warnings.append("software_fixture_only_no_hardware_validation")
    return AMCFPackageValidationReport(
        final_passed=len(failed) == 0,
        checks_passed=passed,
        checks_failed=failed,
        warnings=warnings,
        unsafe_acceptance_count=0,
        claim_boundary_flags=dict(CLAIM_BOUNDARY_FLAGS),
    )


def write_demo_shared_package(output_dir: str | Path) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    package = build_demo_shared_package()
    report = validate_shared_package(package)
    write_json(out / "amcf_shared_package.json", package)
    write_json(out / "amcf_shared_manifest.json", package.manifest)
    write_json(out / "amcf_shared_package_validation_report.json", report)
    summary = [
        "# AMCF Shared Package Model Demo",
        "",
        "This is a software/no-hardware shared model fixture.",
        "",
        f"- final_passed: {'yes' if report.final_passed else 'no'}",
        f"- section_count: {package.manifest.section_count}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        f"- unsafe_acceptance_count: {report.unsafe_acceptance_count}",
        "",
    ]
    (out / "AMCF_SHARED_PACKAGE_MODEL_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return {
        "package": object_to_dict(package),
        "validation_report": object_to_dict(report),
        "output_dir": str(out),
    }
