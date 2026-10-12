from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS
from amcf_software_io_fixtures import load_fixture_bundle


RUN_NAME = "AMCF_PLAYER_PC_RUNTIME_FIXTURE_PROTOTYPE_V1"
RUNTIME_VERSION = "amcf_player_pc_runtime_fixture_v1"


@dataclass(frozen=True)
class PlayerCapabilityProfile:
    profile_id: str
    carrier_layout: str
    staging_model: str
    gate_model: str
    prefetch_model: str
    reverse_model: str
    seek_model: str
    safety_model: str
    hardware_validation_claimed: bool = False


@dataclass(frozen=True)
class PlayerCommandRecord:
    command_id: str
    command: str
    accepted: bool
    reason: str
    section_id: str | None = None


@dataclass(frozen=True)
class PlayerSessionReport:
    run_name: str
    runtime_version: str
    final_passed: bool
    profile: PlayerCapabilityProfile
    package_compatible: bool
    command_transcript: list[PlayerCommandRecord]
    diagnostics: list[str]
    claim_boundary_flags: dict[str, bool] = field(default_factory=lambda: dict(CLAIM_BOUNDARY_FLAGS))
    unsafe_acceptance_count: int = 0
    usb_used: bool = False
    serial_used: bool = False
    firmware_protocol_used: bool = False
    hardware_detection_used: bool = False


def build_player_profile(bundle: dict[str, Any]) -> PlayerCapabilityProfile:
    profile = bundle["player_profile"]
    return PlayerCapabilityProfile(
        profile_id=profile["profile_id"],
        carrier_layout=profile["carrier_layout"],
        staging_model=profile["staging_model"],
        gate_model=profile["gate_model"],
        prefetch_model=profile["prefetch_model"],
        reverse_model=profile["reverse_model"],
        seek_model=profile["seek_model"],
        safety_model=profile["safety_model"],
        hardware_validation_claimed=bool(profile.get("hardware_validation_claimed", False)),
    )


def check_package_compatibility(bundle: dict[str, Any], profile: PlayerCapabilityProfile) -> tuple[bool, list[str]]:
    diagnostics: list[str] = []
    package = bundle["package"]
    section_count = package["manifest"]["section_count"]
    if profile.carrier_layout != "folded_indexed_carrier":
        diagnostics.append("unsupported_carrier_layout")
    if profile.seek_model != "local_buffer_seek_only":
        diagnostics.append("unsupported_seek_model")
    if section_count <= 0:
        diagnostics.append("empty_manifest")
    return len(diagnostics) == 0, diagnostics


def run_simulated_player_session(bundle: dict[str, Any]) -> PlayerSessionReport:
    profile = build_player_profile(bundle)
    compatible, diagnostics = check_package_compatibility(bundle, profile)
    sections = bundle["package"]["manifest"]["physical_sections"]
    transcript: list[PlayerCommandRecord] = [
        PlayerCommandRecord("cmd-000", "load_manifest", compatible, "package_compatible" if compatible else "package_incompatible"),
    ]
    if compatible:
        first = sections[0]["section_id"]
        second = sections[1]["section_id"] if len(sections) > 1 else first
        transcript.extend(
            [
                PlayerCommandRecord("cmd-001", "prefetch_section", True, "fixture_section_prefetched", first),
                PlayerCommandRecord("cmd-002", "stage_section", True, "fixture_section_staged", first),
                PlayerCommandRecord("cmd-003", "switch_visible", True, "verified_section_visible", first),
                PlayerCommandRecord("cmd-004", "bounded_reverse", True, "local_reverse_buffer_allowed", first),
                PlayerCommandRecord("cmd-005", "local_buffer_seek", True, "local_buffer_seek_allowed", second),
                PlayerCommandRecord("cmd-006", "arbitrary_seek", False, "arbitrary_physical_seek_not_supported", "fixture-section-999"),
            ]
        )
    unsafe_acceptance_count = sum(1 for item in transcript if item.command == "arbitrary_seek" and item.accepted)
    flags = dict(CLAIM_BOUNDARY_FLAGS)
    final_passed = compatible and unsafe_acceptance_count == 0 and not any(flags.values()) and not profile.hardware_validation_claimed
    return PlayerSessionReport(
        run_name=RUN_NAME,
        runtime_version=RUNTIME_VERSION,
        final_passed=final_passed,
        profile=profile,
        package_compatible=compatible,
        command_transcript=transcript,
        diagnostics=diagnostics,
        claim_boundary_flags=flags,
        unsafe_acceptance_count=unsafe_acceptance_count,
    )


def object_to_dict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, list):
        return [object_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: object_to_dict(item) for key, item in value.items()}
    return value


def write_player_pc_runtime_demo(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    bundle = load_fixture_bundle(repo_root)
    report = run_simulated_player_session(bundle)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    data = object_to_dict(report)
    (out / "player_pc_session_report.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "player_command_transcript.json").write_text(
        json.dumps(data["command_transcript"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "player_capability_profile.json").write_text(
        json.dumps(data["profile"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = [
        "# AMCF Player PC Runtime Fixture Demo",
        "",
        "This is a simulated Player <-> PC control bridge. It does not use USB, serial, firmware protocol, hardware detection, motors, sensors, or cartridges.",
        "",
        f"- final_passed: {'yes' if report.final_passed else 'no'}",
        f"- package_compatible: {'yes' if report.package_compatible else 'no'}",
        f"- command_count: {len(report.command_transcript)}",
        f"- unsafe_acceptance_count: {report.unsafe_acceptance_count}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "",
    ]
    (out / "PLAYER_PC_RUNTIME_FIXTURE_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return {"report": data, "output_dir": str(out)}
