from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS
from amcf_software_io_fixtures import load_fixture_bundle, validate_fixture_bundle, write_fixture_report


RUN_NAME = "AMCF_UNIVERSAL_DEVICE_INTERFACE_CONFORMANCE_V1"
SCHEMA_VERSION = "amcf-universal-device-interface-conformance-v1"

CORRIDORS = {
    "pc_to_printer": "PC -> Printer / carrier output",
    "reader_to_pc": "PC <-> Reader / scanner recovery",
    "pc_to_player": "Player <-> PC / physical player control",
}


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_universal_profile_templates() -> dict[str, Any]:
    """Return transport-neutral profile guidance, not a hardware claim."""
    return {
        "template_schema_version": "amcf-universal-device-interface-template-v1",
        "profile_bundle_schema": "amcf-device-profile-bundle-v1",
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "corridors": [
            {
                "corridor": "pc_to_printer",
                "role": "carrier_output",
                "backend_candidates": ["file", "windows-spooler", "ipp"],
                "required_capabilities": [
                    "carrier_artifact_generation",
                    "manifest_hash_acknowledgement",
                ],
                "configuration_fields": ["printer_name", "media_profile", "artifact_format"],
                "safety_contract": ["hash_check_before_acceptance", "fail_closed_print_gate"],
            },
            {
                "corridor": "reader_to_pc",
                "role": "carrier_recovery",
                "backend_candidates": ["folder", "windows-wia", "twain", "camera"],
                "required_capabilities": [
                    "capture_file_resolution",
                    "registration_feedback",
                    "hash_feedback",
                ],
                "configuration_fields": ["reader_device", "capture_resolution", "colour_profile", "source_root"],
                "safety_contract": ["registration_and_hash_required", "rescan_on_failure", "fail_closed_reader_gate"],
            },
            {
                "corridor": "pc_to_player",
                "role": "physical_player_control",
                "backend_candidates": ["loopback", "serial", "usb", "network"],
                "required_capabilities": [
                    "manifest_load",
                    "prefetch_hidden_staging_gate",
                    "verify_staged_section",
                    "switch_visible_gate",
                ],
                "configuration_fields": ["transport_endpoint", "baudrate_or_link", "player_profile", "audio_clock"],
                "safety_contract": ["verify_before_visible_switch", "sequence_ordering", "fail_closed_player_gate"],
            },
        ],
        "shared_contract": {
            "manifest": "one shared AMCF package manifest",
            "schedule": "timestamped AMCF update events, not fixed-FPS page assumptions",
            "identity": "section, event, payload, and source-reference hashes",
            "feedback": "ordered status, retry/rescan, and fail-closed decisions",
            "hardware_boundary": "transport providers may connect later; this runner authorizes no physical transition",
        },
    }


def _manifest_contract(bundle: dict[str, Any]) -> dict[str, Any]:
    manifest = bundle["package"]["manifest"]
    sections = list(manifest.get("physical_sections", []))
    events = list(manifest.get("update_events", []))
    section_ids = [str(item.get("section_id", "")) for item in sections]
    event_section_ids = [str(item.get("section_id", "")) for item in events]
    timestamps = [int(item.get("timestamp_ms", 0)) for item in events]
    checks = {
        "manifest_present": bool(manifest),
        "section_count_matches": len(sections) == int(manifest.get("section_count", -1)),
        "sections_have_unique_ids": len(section_ids) == len(set(section_ids)) and all(section_ids),
        "sections_have_payload_hashes": all(bool(item.get("payload_hash")) for item in sections),
        "sections_have_required_lanes": all(bool(item.get("lanes")) for item in sections),
        "dynamic_update_events_present": bool(events),
        "events_reference_known_sections": set(event_section_ids).issubset(set(section_ids)),
        "event_timestamps_are_ordered": timestamps == sorted(timestamps),
        "timing_contract_present_for_audio_alignment": all(
            "timestamp_ms" in item and "dwell_ms" in item for item in events
        ),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "manifest_id": manifest.get("manifest_id"),
        "section_count": len(sections),
        "update_event_count": len(events),
        "audio_timing_metadata_present": "audio" in manifest or "audio_timing" in manifest,
        "section_ids": section_ids,
    }


def _run_component(
    name: str,
    output_dir: Path,
    runner: Callable[[Path, Path], Any],
    root: Path,
) -> dict[str, Any]:
    try:
        result = runner(root, output_dir)
        report = result.get("report", result) if isinstance(result, dict) else {}
        passed = bool(report.get("final_passed", report.get("ok", False)))
        unsafe = int(report.get("unsafe_acceptance_count", 0))
        return {
            "name": name,
            "final_passed": passed,
            "unsafe_acceptance_count": unsafe,
            "output_dir": str(output_dir),
            "status": "passed" if passed and unsafe == 0 else "failed",
        }
    except Exception as exc:  # noqa: BLE001 - conformance must report and fail closed.
        return {
            "name": name,
            "final_passed": False,
            "unsafe_acceptance_count": 1,
            "output_dir": str(output_dir),
            "status": "exception_fail_closed",
            "error": f"{type(exc).__name__}: {exc}",
        }


def run_device_interface_conformance(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Exercise legacy and current software corridors behind one universal contract."""
    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    bundle = load_fixture_bundle(root)
    fixture_report = validate_fixture_bundle(bundle)
    manifest_contract = _manifest_contract(bundle)
    templates = build_universal_profile_templates()
    _write_json(out / "universal_device_profile_templates.json", templates)

    from amcf_device_provider_adapters import run_device_provider_discovery
    from amcf_device_profiles import run_device_profile_validation
    from amcf_hardware_adapter_planning import run_hardware_adapter_plan
    from amcf_hardware_provider_runtime import run_hardware_provider_runtime
    from amcf_physical_adapters import run_physical_software_adapter_roundtrip
    from amcf_software_control_protocol import run_software_control_session

    components = [
        _run_component(
            "legacy_fixture_contract",
            out / "01_fixture_baseline",
            lambda repo, target: write_fixture_report(repo, target),
            root,
        ),
        _run_component(
            "legacy_software_adapter_contract",
            out / "02_software_adapter_roundtrip",
            lambda repo, target: run_physical_software_adapter_roundtrip(repo, target),
            root,
        ),
        _run_component(
            "hardware_interface_plan",
            out / "03_hardware_interface_plan",
            lambda repo, target: run_hardware_adapter_plan(repo, target),
            root,
        ),
        _run_component(
            "provider_neutral_runtime",
            out / "04_provider_neutral_runtime",
            lambda repo, target: run_hardware_provider_runtime(repo, target),
            root,
        ),
        _run_component(
            "versioned_software_control",
            out / "05_software_control_protocol",
            lambda repo, target: run_software_control_session(repo, target),
            root,
        ),
        _run_component(
            "concrete_provider_adapters",
            out / "06_device_provider_discovery",
            lambda repo, target: run_device_provider_discovery(repo, target),
            root,
        ),
        _run_component(
            "profile_selected_providers",
            out / "07_device_profile_validation",
            lambda repo, target: run_device_profile_validation(repo, target),
            root,
        ),
    ]
    all_components_passed = all(item["final_passed"] and item["unsafe_acceptance_count"] == 0 for item in components)
    control_report = next(item for item in components if item["name"] == "versioned_software_control")
    provider_report = next(item for item in components if item["name"] == "concrete_provider_adapters")
    fail_closed_checks = {
        "software_control_component_passed": control_report["final_passed"],
        "provider_component_passed": provider_report["final_passed"],
        "physical_transition_authorization_disabled": True,
        "hardware_connection_disabled": True,
        "unsafe_acceptance_count_zero": sum(item["unsafe_acceptance_count"] for item in components) == 0,
    }
    flags = dict(CLAIM_BOUNDARY_FLAGS)
    unsafe_count = sum(item["unsafe_acceptance_count"] for item in components)
    final_passed = (
        fixture_report["final_passed"]
        and manifest_contract["passed"]
        and all_components_passed
        and all(fail_closed_checks.values())
        and unsafe_count == 0
        and not any(flags.values())
    )
    report = {
        "run_name": RUN_NAME,
        "schema_version": SCHEMA_VERSION,
        "repo_root": str(root),
        "output_dir": str(out),
        "corridors": CORRIDORS,
        "profile_template_schema": templates["template_schema_version"],
        "manifest_contract": manifest_contract,
        "fixture_contract": {
            "final_passed": bool(fixture_report["final_passed"]),
            "checks_passed": fixture_report.get("checks_passed", []),
            "checks_failed": fixture_report.get("checks_failed", []),
        },
        "components": components,
        "fail_closed_contract": fail_closed_checks,
        "final_passed": final_passed,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "source_video_required": False,
        "physical_transition_authorized": False,
        "claim_boundary_flags": flags,
        "unsafe_acceptance_count": unsafe_count,
        "feedback": {
            "status": "universal_device_interface_ready" if final_passed else "universal_device_interface_rejected_fail_closed",
            "display_allowed": False,
            "transition_allowed": False,
            "hardware_selection_required": True,
            "recommended_action": (
                "select_hardware_profile_and_bind_a_device_specific_provider"
                if final_passed
                else "inspect_component_reports_and_keep_all_transitions_blocked"
            ),
        },
    }
    _write_json(out / "universal_device_interface_conformance_report.json", report)
    _write_json(out / "universal_device_interface_feedback.json", report["feedback"])
    summary = [
        "# AMCF Universal Device Interface Conformance",
        "",
        "This run combines the legacy fixture/adapter paths with the current provider, profile, and software-control paths.",
        "",
        f"- final_passed: {'yes' if final_passed else 'no'}",
        f"- manifest_contract: {'yes' if manifest_contract['passed'] else 'no'}",
        f"- components_passed: {sum(int(item['final_passed']) for item in components)}/{len(components)}",
        f"- unsafe_acceptance_count: {unsafe_count}",
        "- hardware_connected: no",
        "- physical_transition_authorized: no",
        "- physical_level_5_claimed: no",
        "",
        "The universal contract is transport-neutral. A real device must pass a device-specific profile and provider binding before operation is enabled.",
        "",
    ]
    (out / "UNIVERSAL_DEVICE_INTERFACE_CONFORMANCE_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return {"report": report, "output_dir": str(out)}
