from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS


PROFILE_SCHEMA_VERSION = "amcf-device-profile-bundle-v1"
RUN_NAME = "AMCF_DEVICE_PROFILE_VALIDATION_V1"

CORRIDORS = ("pc_to_printer", "reader_to_pc", "pc_to_player")
BACKENDS_BY_CORRIDOR = {
    "pc_to_printer": ("file", "windows-spooler"),
    "reader_to_pc": ("folder", "windows-wia"),
    "pc_to_player": ("loopback", "serial"),
}
REQUIRED_CAPABILITIES = {
    "pc_to_printer": ("carrier_artifact_generation", "manifest_hash_acknowledgement"),
    "reader_to_pc": ("capture_file_resolution", "registration_feedback", "hash_feedback"),
    "pc_to_player": ("manifest_load", "prefetch_hidden_staging_gate", "verify_staged_section", "switch_visible_gate"),
}
SOFTWARE_BACKENDS = {"file", "folder", "loopback"}


@dataclass(frozen=True)
class DeviceProfile:
    profile_id: str
    corridor: str
    backend: str
    device_name: str
    transport: str
    connection: str
    capabilities: tuple[str, ...]
    safety_contract: tuple[str, ...]
    configuration: dict[str, Any]
    hardware_requested: bool = False
    hardware_validation_claimed: bool = False
    physical_level_5_claimed: bool = False

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "DeviceProfile":
        return cls(
            profile_id=str(value["profile_id"]),
            corridor=str(value["corridor"]),
            backend=str(value["backend"]),
            device_name=str(value["device_name"]),
            transport=str(value["transport"]),
            connection=str(value.get("connection", "none")),
            capabilities=tuple(str(item) for item in value.get("capabilities", [])),
            safety_contract=tuple(str(item) for item in value.get("safety_contract", [])),
            configuration=dict(value.get("configuration", {})),
            hardware_requested=bool(value.get("hardware_requested", False)),
            hardware_validation_claimed=bool(value.get("hardware_validation_claimed", False)),
            physical_level_5_claimed=bool(value.get("physical_level_5_claimed", False)),
        )

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_device_profile_bundle() -> dict[str, Any]:
    profiles = [
        DeviceProfile(
            profile_id="amcf-file-carrier-profile-v1",
            corridor="pc_to_printer",
            backend="file",
            device_name="AMCF software carrier artifact",
            transport="filesystem",
            connection="none",
            capabilities=(
                "carrier_artifact_generation",
                "manifest_hash_acknowledgement",
                "reprintable_artifact_path",
                "fail_closed_print_gate",
            ),
            safety_contract=("hash_check_before_acceptance", "fail_closed_on_mismatch", "no_physical_output_claim"),
            configuration={},
        ),
        DeviceProfile(
            profile_id="amcf-folder-reader-profile-v1",
            corridor="reader_to_pc",
            backend="folder",
            device_name="AMCF software capture folder",
            transport="filesystem",
            connection="none",
            capabilities=(
                "capture_file_resolution",
                "registration_feedback",
                "colour_registry_feedback",
                "hash_feedback",
                "rescan_request",
                "fail_closed_reader_gate",
            ),
            safety_contract=("registration_and_hash_required", "rescan_on_failure", "fail_closed_reader_gate"),
            configuration={},
        ),
        DeviceProfile(
            profile_id="amcf-loopback-player-profile-v1",
            corridor="pc_to_player",
            backend="loopback",
            device_name="AMCF software control loopback",
            transport="in_memory_loopback",
            connection="none",
            capabilities=(
                "manifest_load",
                "prefetch_hidden_staging_gate",
                "verify_staged_section",
                "switch_visible_gate",
                "bounded_seek_and_reverse",
                "fail_closed_stop",
            ),
            safety_contract=("verify_before_visible_switch", "sequence_ordering", "fail_closed_player_gate"),
            configuration={},
        ),
    ]
    return {
        "schema_version": PROFILE_SCHEMA_VERSION,
        "bundle_id": "amcf-device-profiles-software-default-v1",
        "profiles": [profile.as_dict() for profile in profiles],
        "hardware_enable_policy": "requires_profile_request_and_explicit_cli_flag",
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
    }


def load_device_profile_bundle(path: str | Path | None = None) -> dict[str, Any]:
    if path is None:
        return default_device_profile_bundle()
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_device_profile_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[str] = []
    profiles: list[DeviceProfile] = []
    if bundle.get("schema_version") != PROFILE_SCHEMA_VERSION:
        errors.append("schema_version_unsupported")
    else:
        checks.append("schema_version_supported")
    raw_profiles = bundle.get("profiles")
    if not isinstance(raw_profiles, list):
        errors.append("profiles_must_be_a_list")
        raw_profiles = []
    for index, raw in enumerate(raw_profiles):
        if not isinstance(raw, dict):
            errors.append(f"profile_{index}_must_be_an_object")
            continue
        try:
            profile = DeviceProfile.from_mapping(raw)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"profile_{index}_malformed:{type(exc).__name__}")
            continue
        profiles.append(profile)
        if profile.corridor not in CORRIDORS:
            errors.append(f"{profile.profile_id}:unknown_corridor")
        elif profile.backend not in BACKENDS_BY_CORRIDOR[profile.corridor]:
            errors.append(f"{profile.profile_id}:backend_not_supported_for_corridor")
        else:
            checks.append(f"{profile.profile_id}:corridor_backend_supported")
            if set(REQUIRED_CAPABILITIES[profile.corridor]).issubset(profile.capabilities):
                checks.append(f"{profile.profile_id}:required_capabilities_present")
            else:
                errors.append(f"{profile.profile_id}:required_capabilities_missing")
        if not profile.profile_id or not profile.device_name or not profile.transport:
            errors.append(f"{profile.profile_id or index}:identity_incomplete")
        if "fail_closed" not in " ".join(profile.safety_contract) and not any(
            "fail_closed" in item for item in profile.safety_contract
        ):
            errors.append(f"{profile.profile_id}:fail_closed_safety_contract_missing")
        if profile.backend not in SOFTWARE_BACKENDS and not profile.hardware_requested:
            errors.append(f"{profile.profile_id}:hardware_profile_requires_hardware_requested_true")
        if profile.hardware_validation_claimed:
            errors.append(f"{profile.profile_id}:hardware_validation_claimed_true")
        if profile.physical_level_5_claimed:
            errors.append(f"{profile.profile_id}:physical_level_5_claimed_true")
    ids = [profile.profile_id for profile in profiles]
    corridors = [profile.corridor for profile in profiles]
    if len(ids) != len(set(ids)):
        errors.append("duplicate_profile_id")
    if sorted(corridors) != sorted(CORRIDORS):
        errors.append("exactly_one_profile_per_corridor_required")
    else:
        checks.append("all_required_corridors_present")
    if bool(bundle.get("hardware_validation_claimed", False)):
        errors.append("bundle_hardware_validation_claimed_true")
    if bool(bundle.get("physical_level_5_claimed", False)):
        errors.append("bundle_physical_level_5_claimed_true")
    if any(profile.hardware_requested for profile in profiles):
        warnings.append("explicit_hardware_enable_flag_required")
    flags = dict(CLAIM_BOUNDARY_FLAGS)
    final_passed = not errors and not any(flags.values())
    return {
        "run_name": RUN_NAME,
        "schema_version": PROFILE_SCHEMA_VERSION,
        "bundle_id": str(bundle.get("bundle_id", "")),
        "final_passed": final_passed,
        "checks_passed": checks,
        "checks_failed": errors,
        "warnings": warnings,
        "profiles": [profile.as_dict() for profile in profiles],
        "claim_boundary_flags": flags,
        "unsafe_acceptance_count": 0,
    }


def _profile_by_corridor(bundle: dict[str, Any]) -> dict[str, DeviceProfile]:
    return {
        profile.corridor: profile
        for profile in (DeviceProfile.from_mapping(item) for item in bundle["profiles"])
    }


def _relative_or_absolute_path(root: Path, value: Any) -> str | None:
    if value in (None, ""):
        return None
    path = Path(str(value))
    return str(path if path.is_absolute() else root / path)


def provider_selection_from_bundle(bundle: dict[str, Any], root: str | Path) -> dict[str, Any]:
    profiles = _profile_by_corridor(bundle)
    printer = profiles["pc_to_printer"]
    reader = profiles["reader_to_pc"]
    player = profiles["pc_to_player"]
    return {
        "printer_backend": printer.backend,
        "reader_backend": reader.backend,
        "player_backend": player.backend,
        "printer_name": printer.configuration.get("printer_name"),
        "reader_device": reader.configuration.get("reader_device"),
        "reader_source": _relative_or_absolute_path(Path(root).resolve(), reader.configuration.get("reader_source")),
        "player_port": player.configuration.get("player_port"),
        "profile_ids": {
            "pc_to_printer": printer.profile_id,
            "reader_to_pc": reader.profile_id,
            "pc_to_player": player.profile_id,
        },
        "hardware_requested": any(profile.hardware_requested for profile in profiles.values()),
    }


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_summary(path: Path, report: dict[str, Any]) -> None:
    validation = report["profile_validation"]
    provider = report.get("provider_discovery") or {}
    lines = [
        "# AMCF Device Profile Validation",
        "",
        "This run validates the selected printer/carrier, reader/scanner, and player profiles before adapter operation.",
        "",
        f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
        f"- profile_validation: {'yes' if validation['final_passed'] else 'no'}",
        f"- provider_discovery: {'yes' if provider.get('final_passed') else 'no'}",
        f"- hardware_enable_requested: {'yes' if report['hardware_enable_requested'] else 'no'}",
        f"- hardware_connected: {'yes' if report['hardware_connected'] else 'no'}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "- physical_hardware_validation_claimed: no",
        "- physical_level_5_claimed: no",
        "",
        "A hardware profile requires both profile intent and the explicit CLI enable flag. Missing or failed device checks remain fail-closed.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def run_device_profile_validation(
    repo_root: str | Path,
    output_dir: str | Path,
    *,
    profile_path: str | Path | None = None,
    enable_hardware: bool = False,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    source = str(Path(profile_path).resolve()) if profile_path else "built_in_software_default"
    try:
        bundle = load_device_profile_bundle(profile_path)
        validation = validate_device_profile_bundle(bundle)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        validation = {
            "run_name": RUN_NAME,
            "schema_version": PROFILE_SCHEMA_VERSION,
            "bundle_id": "",
            "final_passed": False,
            "checks_passed": [],
            "checks_failed": [f"profile_load_failed:{type(exc).__name__}"],
            "warnings": [],
            "profiles": [],
            "claim_boundary_flags": dict(CLAIM_BOUNDARY_FLAGS),
            "unsafe_acceptance_count": 0,
        }
        bundle = default_device_profile_bundle()
    # Reject malformed profiles before resolving corridor-specific provider arguments.
    # This keeps custom configuration failures fail-closed instead of raising a KeyError.
    selection = provider_selection_from_bundle(bundle, root) if validation["final_passed"] else {}
    provider_result: dict[str, Any] | None = None
    if validation["final_passed"]:
        from amcf_device_provider_adapters import run_device_provider_discovery

        hardware_active = bool(enable_hardware and selection.get("hardware_requested", False))
        provider_result = run_device_provider_discovery(
            root,
            out / "provider_discovery",
            printer_backend=selection["printer_backend"],
            reader_backend=selection["reader_backend"],
            player_backend=selection["player_backend"],
            printer_name=selection.get("printer_name"),
            reader_device=selection.get("reader_device"),
            reader_source=selection.get("reader_source"),
            player_port=selection.get("player_port"),
            enable_hardware=hardware_active,
        )
    provider_report = provider_result["report"] if provider_result else None
    provider_passed = bool(provider_report and provider_report.get("final_passed"))
    unsafe_count = int(validation.get("unsafe_acceptance_count", 0)) + int(
        provider_report.get("unsafe_acceptance_count", 0) if provider_report else 0
    )
    final_passed = bool(validation["final_passed"] and provider_passed and unsafe_count == 0)
    report = {
        "run_name": RUN_NAME,
        "profile_schema_version": PROFILE_SCHEMA_VERSION,
        "repo_root": str(root),
        "output_dir": str(out),
        "profile_source": source,
        "profile_validation": validation,
        "provider_selection": selection,
        "provider_discovery": provider_report,
        "hardware_enable_requested": bool(enable_hardware),
        "hardware_connected": bool(provider_report and provider_report.get("hardware_connected")),
        "final_passed": final_passed,
        "claim_boundary_flags": dict(CLAIM_BOUNDARY_FLAGS),
        "unsafe_acceptance_count": unsafe_count,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "feedback": {
            "status": "device_profiles_ready" if final_passed else "device_profiles_rejected_fail_closed",
            "display_allowed": False,
            "transition_allowed": False,
            "recommended_action": (
                "select_exact_hardware_profile_and_run_with_enable_hardware"
                if final_passed and selection.get("hardware_requested")
                else "repair_profile_or_provider_selection"
                if not final_passed
                else "software_profile_ready_for_adapter_use"
            ),
        },
    }
    _write_json(out / "device_profile_bundle.json", bundle)
    _write_json(out / "device_profile_validation_report.json", report)
    _write_json(out / "device_profile_feedback.json", report["feedback"])
    _write_summary(out / "DEVICE_PROFILE_VALIDATION_SUMMARY.md", report)
    return {"report": report, "output_dir": str(out)}
