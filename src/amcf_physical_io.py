from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any


STATUS_NOT_STARTED = "not_started"
STATUS_SIMULATED_ONLY = "simulated_only"
STATUS_RECOGNIZED = "recognized"
STATUS_PARTIAL = "partial"
STATUS_VALIDATED = "validated"
STATUS_WARNING = "warning"
STATUS_FAILED = "failed"
STATUS_UNSUPPORTED = "unsupported"
STATUS_UNVERIFIED = "unverified"
STATUS_MEASURED = "measured"

LANE_TIMING = "timing_lane"
LANE_INDEX = "index_lane"
LANE_REGISTRATION = "registration_lane"
LANE_IMAGE_PAYLOAD = "image_payload_lane"
LANE_COLOUR_REGISTRY = "colour_registry_lane"
LANE_METADATA = "metadata_lane"
LANE_CHECKSUM_HASH = "checksum_hash_lane"
LANE_DAMAGE_RECOVERY = "damage_recovery_lane"

REQUIRED_LANE_TYPES = [
    LANE_TIMING,
    LANE_INDEX,
    LANE_REGISTRATION,
    LANE_IMAGE_PAYLOAD,
    LANE_COLOUR_REGISTRY,
    LANE_METADATA,
    LANE_CHECKSUM_HASH,
]

DEVICE_PATH_PRINTER = "printer_output_path"
DEVICE_PATH_READER_PC = "reader_pc_path"
DEVICE_PATH_PLAYER_PC = "player_pc_path"

CARRIER_INDEXED_THIN_SECTION = "indexed_thin_section_carrier"

PHYSICAL_IO_CLAIM_BOUNDARY_TEXT = (
    "This physical I/O module is a software architecture and simulation foundation. "
    "It does not claim manufactured hardware, real print accuracy, real scanner validation, "
    "real physical playback proof, or real device-driver integration."
)


@dataclass
class PhysicalClaimBoundary:
    status: str
    summary: str
    not_claimed: list[str]
    allowed_claims: list[str]


@dataclass
class MaterialProfile:
    material_profile_id: str
    material_family: str
    thickness_um: float
    stiffness_proxy: float
    friction_proxy: float
    curl_risk: str
    humidity_sensitivity: str
    marker_contrast_proxy: float
    colour_stability_proxy: float
    scanner_reflectance_proxy: float
    profile_confidence: str
    claim_boundary: PhysicalClaimBoundary


@dataclass
class AMCFPhysicalLane:
    lane_id: str
    lane_type: str
    required: bool
    layout_mm: dict[str, float]
    encoding: str
    recovery_policy: str


@dataclass
class AMCFPhysicalSection:
    section_id: str
    section_index: int
    timestamp_start_ms: int
    timestamp_end_ms: int
    dwell_ms: int
    layout_mm: dict[str, float]
    lanes: list[AMCFPhysicalLane]
    payload_ref: str
    payload_hash: str
    metadata_ref: str
    required_for_playback: bool
    recovery_policy: str


@dataclass
class AMCFPhysicalManifest:
    manifest_id: str
    source_amcf_id: str
    carrier_id: str
    carrier_format_version: str
    carrier_type: str
    section_count: int
    sections: list[AMCFPhysicalSection]
    material_profile: MaterialProfile
    lane_schema: list[AMCFPhysicalLane]
    printer_requirements: dict[str, Any]
    reader_requirements: dict[str, Any]
    player_requirements: dict[str, Any]
    compression_policy: dict[str, Any]
    claim_boundary: PhysicalClaimBoundary


@dataclass
class PhysicalDeviceProfile:
    device_profile_id: str
    device_name: str
    device_path_type: str
    recognition_mode: str
    connection_type: str
    profile_confidence: str
    capabilities: dict[str, Any]
    claim_boundary: PhysicalClaimBoundary


@dataclass
class PhysicalRecognitionReport:
    report_id: str
    path_type: str
    recognized: bool
    recognition_status: str
    confidence: str
    recognized_ids: list[str]
    warnings: list[str]
    failures: list[str]
    claim_boundary: PhysicalClaimBoundary


@dataclass
class PhysicalCapabilityReport:
    report_id: str
    path_type: str
    device_profile_id: str
    carrier_id: str
    supported: bool
    validation_status: str
    capabilities_checked: list[str]
    warnings: list[str]
    failures: list[str]
    claim_boundary: PhysicalClaimBoundary


@dataclass
class PhysicalValidationReport:
    report_id: str
    validation_target: str
    validation_status: str
    checks_passed: list[str]
    checks_failed: list[str]
    warnings: list[str]
    failures: list[str]
    claim_boundary: PhysicalClaimBoundary


def default_claim_boundary() -> PhysicalClaimBoundary:
    return PhysicalClaimBoundary(
        status=STATUS_SIMULATED_ONLY,
        summary=PHYSICAL_IO_CLAIM_BOUNDARY_TEXT,
        not_claimed=[
            "manufactured_hardware",
            "real_print_accuracy",
            "real_scanner_validation",
            "real_physical_playback_proof",
            "real_device_driver_integration",
            "lcd_oled_screen_playback_as_physical_player",
        ],
        allowed_claims=[
            "software_architecture_foundation",
            "deterministic_demo_manifest",
            "simulated_device_profiles",
            "claim_boundary_documentation",
        ],
    )


def default_material_profile() -> MaterialProfile:
    return MaterialProfile(
        material_profile_id="demo_material_profile_parameterized_001",
        material_family="indexed_thin_section_reference_card",
        thickness_um=180.0,
        stiffness_proxy=0.62,
        friction_proxy=0.34,
        curl_risk=STATUS_UNVERIFIED,
        humidity_sensitivity=STATUS_UNVERIFIED,
        marker_contrast_proxy=0.8,
        colour_stability_proxy=0.74,
        scanner_reflectance_proxy=0.7,
        profile_confidence=STATUS_SIMULATED_ONLY,
        claim_boundary=default_claim_boundary(),
    )


def default_lane_schema() -> list[AMCFPhysicalLane]:
    lane_layouts = {
        LANE_TIMING: {"x": 0.0, "y": 0.0, "width": 8.0, "height": 60.0},
        LANE_INDEX: {"x": 8.0, "y": 0.0, "width": 8.0, "height": 60.0},
        LANE_REGISTRATION: {"x": 16.0, "y": 0.0, "width": 10.0, "height": 60.0},
        LANE_IMAGE_PAYLOAD: {"x": 26.0, "y": 0.0, "width": 90.0, "height": 60.0},
        LANE_COLOUR_REGISTRY: {"x": 116.0, "y": 0.0, "width": 14.0, "height": 60.0},
        LANE_METADATA: {"x": 130.0, "y": 0.0, "width": 22.0, "height": 60.0},
        LANE_CHECKSUM_HASH: {"x": 152.0, "y": 0.0, "width": 20.0, "height": 60.0},
        LANE_DAMAGE_RECOVERY: {"x": 172.0, "y": 0.0, "width": 18.0, "height": 60.0},
    }
    encodings = {
        LANE_IMAGE_PAYLOAD: "payload_reference",
        LANE_COLOUR_REGISTRY: "calibration_swatches",
        LANE_CHECKSUM_HASH: "sha256_digest_reference",
    }
    lanes = []
    for lane_type, layout in lane_layouts.items():
        lanes.append(
            AMCFPhysicalLane(
                lane_id=f"default_{lane_type}",
                lane_type=lane_type,
                required=lane_type in REQUIRED_LANE_TYPES,
                layout_mm=layout,
                encoding=encodings.get(lane_type, "marker_lane_v1"),
                recovery_policy="fail_closed_if_required_lane_unreadable" if lane_type in REQUIRED_LANE_TYPES else "optional_damage_hint",
            )
        )
    return lanes


def _section_lanes(section_index: int) -> list[AMCFPhysicalLane]:
    lanes = []
    for lane in default_lane_schema():
        lane_dict = manifest_to_dict(lane)
        lane_dict["lane_id"] = f"section_{section_index:03d}_{lane.lane_type}"
        lanes.append(AMCFPhysicalLane(**lane_dict))
    return lanes


def build_demo_physical_manifest() -> AMCFPhysicalManifest:
    sections = []
    for index, start_ms in enumerate((0, 120, 300)):
        end_ms = (120, 300, 480)[index]
        sections.append(
            AMCFPhysicalSection(
                section_id=f"amcf_section_{index:03d}",
                section_index=index,
                timestamp_start_ms=start_ms,
                timestamp_end_ms=end_ms,
                dwell_ms=end_ms - start_ms,
                layout_mm={"width": 190.0, "height": 60.0, "safe_margin": 2.0},
                lanes=_section_lanes(index),
                payload_ref=f"payloads/section_{index:03d}.amcfpayload",
                payload_hash=f"demo_sha256_placeholder_{index:03d}",
                metadata_ref=f"metadata/section_{index:03d}.json",
                required_for_playback=True,
                recovery_policy="reader_verifies_required_lanes_before_recovery_or_player_prefetch",
            )
        )
    return AMCFPhysicalManifest(
        manifest_id="demo_amcf_physical_manifest_001",
        source_amcf_id="demo_source_amcf_archive_001",
        carrier_id="demo_indexed_thin_section_carrier_001",
        carrier_format_version="physical_manifest_v1",
        carrier_type=CARRIER_INDEXED_THIN_SECTION,
        section_count=len(sections),
        sections=sections,
        material_profile=default_material_profile(),
        lane_schema=default_lane_schema(),
        printer_requirements={
            "path_type": DEVICE_PATH_PRINTER,
            "role": "creates_or_exports_physical_amcf_carrier_packages",
            "stage": STATUS_SIMULATED_ONLY,
            "no_real_printer_driver": True,
        },
        reader_requirements={
            "path_type": DEVICE_PATH_READER_PC,
            "role": "recovers_or_verifies_physical_amcf_back_into_digital_amcf",
            "stage": STATUS_SIMULATED_ONLY,
            "no_real_scanner_driver": True,
        },
        player_requirements={
            "path_type": DEVICE_PATH_PLAYER_PC,
            "role": "recognizes_controls_supports_future_physical_optical_player",
            "preferred_mechanism": "dynamic A/B staged folded-path physical/optical playback",
            "visible_image_path": "physical_optical_not_lcd_oled_screen_playback",
            "stage": STATUS_SIMULATED_ONLY,
            "no_real_player_driver": True,
        },
        compression_policy={
            "canonical_scan_recovery_images": "lossless_or_original_until_marker_hash_colour_decoding_complete",
            "lossy_before_marker_hash_colour_decoding": "disabled_by_default",
            "compressed_previews_after_validation": "allowed",
            "references_only_not_dependencies": ["CompressorJS", "UPNG.js"],
        },
        claim_boundary=default_claim_boundary(),
    )


def build_demo_printer_device_profile() -> PhysicalDeviceProfile:
    return PhysicalDeviceProfile(
        device_profile_id="demo_printer_export_profile_001",
        device_name="AMCF simulated printer/export path",
        device_path_type=DEVICE_PATH_PRINTER,
        recognition_mode="software_export_profile_only",
        connection_type="none",
        profile_confidence=STATUS_SIMULATED_ONLY,
        capabilities={
            "exports_carrier_package": True,
            "real_printer_hardware_claimed": False,
            "real_print_accuracy_claimed": False,
        },
        claim_boundary=default_claim_boundary(),
    )


def build_demo_reader_device_profile() -> PhysicalDeviceProfile:
    return PhysicalDeviceProfile(
        device_profile_id="demo_reader_pc_profile_001",
        device_name="AMCF simulated reader/PC recovery path",
        device_path_type=DEVICE_PATH_READER_PC,
        recognition_mode="simulated_manifest_lane_check",
        connection_type="none",
        profile_confidence=STATUS_SIMULATED_ONLY,
        capabilities={
            "recovers_digital_amcf_state": "simulated_only",
            "real_scanner_hardware_claimed": False,
            "real_scanner_validation_claimed": False,
        },
        claim_boundary=default_claim_boundary(),
    )


def build_demo_player_device_profile() -> PhysicalDeviceProfile:
    return PhysicalDeviceProfile(
        device_profile_id="demo_player_pc_profile_001",
        device_name="AMCF simulated player recognition/control path",
        device_path_type=DEVICE_PATH_PLAYER_PC,
        recognition_mode="simulated_pc_control_profile",
        connection_type="none",
        profile_confidence=STATUS_SIMULATED_ONLY,
        capabilities={
            "physical_optical_playback_concept": "dynamic_folded_path_ab_staged_indexed_section_player",
            "pc_control_support": ["schedule_execution", "motor_index_control", "audio_sync", "diagnostics", "fail_closed_safety"],
            "visible_image_path": "physical_optical",
            "lcd_oled_screen_playback_as_physical_player": False,
            "real_physical_playback_proof_claimed": False,
        },
        claim_boundary=default_claim_boundary(),
    )


def validate_physical_manifest(manifest: AMCFPhysicalManifest) -> PhysicalValidationReport:
    checks_passed: list[str] = []
    checks_failed: list[str] = []
    warnings: list[str] = []
    failures: list[str] = []

    if manifest.carrier_type == CARRIER_INDEXED_THIN_SECTION:
        checks_passed.append("carrier_type_indexed_thin_section_carrier")
    else:
        checks_failed.append("carrier_type_supported")
        failures.append("unsupported_carrier_type")

    if manifest.section_count == len(manifest.sections):
        checks_passed.append("section_count_matches_sections")
    else:
        checks_failed.append("section_count_matches_sections")
        failures.append("section_count_mismatch")

    for section in manifest.sections:
        section_lanes = {lane.lane_type for lane in section.lanes}
        missing = [lane_type for lane_type in REQUIRED_LANE_TYPES if lane_type not in section_lanes]
        if missing:
            checks_failed.append(f"section_{section.section_index}_required_lanes_present")
            failures.append(f"missing_required_lanes:section_{section.section_index}:{','.join(missing)}")
        else:
            checks_passed.append(f"section_{section.section_index}_required_lanes_present")

    if manifest.material_profile.profile_confidence == STATUS_SIMULATED_ONLY:
        warnings.append("material_profile_simulated_parameterized_not_measured")
    elif manifest.material_profile.profile_confidence == STATUS_MEASURED:
        checks_passed.append("material_profile_measured")
    else:
        warnings.append(f"material_profile_confidence:{manifest.material_profile.profile_confidence}")

    status = STATUS_VALIDATED if not failures else STATUS_FAILED
    if warnings and not failures:
        status = STATUS_WARNING
    return PhysicalValidationReport(
        report_id="demo_physical_manifest_validation_report_001",
        validation_target=manifest.manifest_id,
        validation_status=status,
        checks_passed=checks_passed,
        checks_failed=checks_failed,
        warnings=warnings,
        failures=failures,
        claim_boundary=default_claim_boundary(),
    )


def manifest_to_dict(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, list):
        return [manifest_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {key: manifest_to_dict(value) for key, value in obj.items()}
    return obj


def write_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest_to_dict(data), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_demo_physical_io_package(output_dir: str | Path) -> dict[str, str]:
    output_dir = Path(output_dir)
    shared = output_dir / "shared"
    printer = output_dir / "printer_path"
    reader = output_dir / "reader_path"
    player = output_dir / "player_path"
    manifest = build_demo_physical_manifest()
    validation = validate_physical_manifest(manifest)

    paths = {
        "manifest": str(shared / "amcf_physical_manifest.json"),
        "material_profile": str(shared / "material_profile.json"),
        "lane_schema": str(shared / "lane_schema.json"),
        "claim_boundary": str(shared / "claim_boundary.json"),
        "summary": str(shared / "physical_io_summary.md"),
        "printer_profile": str(printer / "printer_device_profile.json"),
        "reader_profile": str(reader / "reader_device_profile.json"),
        "player_profile": str(player / "player_device_profile.json"),
        "validation_report": str(output_dir / "physical_validation_report.json"),
        "readme": str(output_dir / "README.md"),
    }

    write_json(paths["manifest"], manifest)
    write_json(paths["material_profile"], manifest.material_profile)
    write_json(paths["lane_schema"], manifest.lane_schema)
    write_json(paths["claim_boundary"], manifest.claim_boundary)
    write_json(paths["printer_profile"], build_demo_printer_device_profile())
    write_json(paths["reader_profile"], build_demo_reader_device_profile())
    write_json(paths["player_profile"], build_demo_player_device_profile())
    write_json(paths["validation_report"], validation)

    summary = [
        "# AMCF Physical I/O Architecture Demo",
        "",
        "- Digital AMCF is the canonical representation, scheduler, compositor, and validation model.",
        "- Physical AMCF is the material embodiment, execution, and recovery branch of the same AMCF schedule and section logic.",
        "- Printer path creates or exports physical AMCF carrier packages.",
        "- Reader path recovers or verifies carrier packages back into digital AMCF.",
        "- Player path supports physical/optical execution of the same AMCF schedule.",
        "- No real hardware validation is claimed.",
        "",
        PHYSICAL_IO_CLAIM_BOUNDARY_TEXT,
    ]
    Path(paths["summary"]).parent.mkdir(parents=True, exist_ok=True)
    Path(paths["summary"]).write_text("\n".join(summary) + "\n", encoding="utf-8")

    readme = [
        "# Physical I/O Architecture Demo Output",
        "",
        "This ignored demo output is generated by `demo/run_physical_io_architecture_demo.py`.",
        "It contains a shared AMCF physical manifest, material profile, lane schema, simulated path profiles, and validation report.",
        "",
        PHYSICAL_IO_CLAIM_BOUNDARY_TEXT,
    ]
    Path(paths["readme"]).write_text("\n".join(readme) + "\n", encoding="utf-8")
    return paths
