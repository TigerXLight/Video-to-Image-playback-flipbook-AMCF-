from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from amcf_physical_adapters import run_physical_software_adapter_roundtrip
from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS


PLAN_VERSION = "amcf-hardware-adapter-plan-v1"
RUN_NAME = "AMCF_HARDWARE_ADAPTER_PLANNING_V1"


@dataclass(frozen=True)
class HardwareAdapterInterfaceSpec:
    adapter_id: str
    corridor: str
    interface_name: str
    provider: str
    transport: str
    direction: str
    capabilities: tuple[str, ...]
    required_inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    safety_requirements: tuple[str, ...]
    physical_player_alignment: tuple[str, ...] = ()
    planned_only: bool = True
    hardware_validation_claimed: bool = False


@dataclass(frozen=True)
class HardwarePlanStatusEvent:
    sequence: int
    state: str
    code: str
    accepted: bool
    severity: str
    message: str
    display_allowed: bool
    transition_allowed: bool
    retry_allowed: bool
    fail_closed: bool
    unsafe_acceptance: bool = False


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _interface_specs() -> tuple[HardwareAdapterInterfaceSpec, ...]:
    return (
        HardwareAdapterInterfaceSpec(
            adapter_id="windows-print-carrier-planner",
            corridor="pc_to_printer",
            interface_name="Windows print spooler or deterministic carrier-artifact submission",
            provider="Windows Print Spooler API or a print-to-file provider",
            transport="windows_print_spooler_or_print_to_file",
            direction="pc_to_printer_or_carrier",
            capabilities=(
                "carrier_artifact_generation",
                "spooler_job_submission",
                "job_identity_feedback",
                "artifact_hash_feedback",
                "registration_lane_validation",
                "fail_closed_print_gate",
            ),
            required_inputs=(
                "validated_physical_manifest",
                "lane_layout_and_timing_metadata",
                "printer_profile_and_safe_margins",
                "artifact_sha256",
            ),
            outputs=(
                "carrier_artifact_or_spooler_job",
                "job_id",
                "artifact_sha256",
                "status_events",
                "print_gate_decision",
            ),
            safety_requirements=(
                "never acknowledge physical output before device acknowledgement",
                "fail closed when the artifact hash or registration lanes are missing",
                "retain a recoverable carrier artifact and immutable job record",
            ),
        ),
        HardwareAdapterInterfaceSpec(
            adapter_id="windows-reader-capture-planner",
            corridor="reader_to_pc",
            interface_name="Windows reader and scanner capture",
            provider="Windows Image Acquisition (WIA) or TWAIN; OpenCV remains an offline capture fallback",
            transport="wia_twain_or_opencv_capture",
            direction="reader_or_scanner_to_pc",
            capabilities=(
                "device_enumeration",
                "frame_capture",
                "registration_marker_recovery",
                "colour_registry_calibration",
                "frame_hash_feedback",
                "rescan_request",
                "fail_closed_reader_gate",
            ),
            required_inputs=(
                "reader_profile",
                "capture_resolution_and_timing",
                "registration_and_colour_registry",
                "expected_section_hashes",
            ),
            outputs=(
                "captured_sections",
                "recovery_records",
                "marker_and_colour_diagnostics",
                "rescan_feedback",
                "capture_hashes",
            ),
            safety_requirements=(
                "do not mark a section recovered without registration and hash checks",
                "request rescan on missing markers, unreadable lanes, or timing ambiguity",
                "never authorize player display from an unverified capture",
            ),
        ),
        HardwareAdapterInterfaceSpec(
            adapter_id="amcf-player-control-planner",
            corridor="pc_to_player",
            interface_name="AMCF Player Control Protocol v1",
            provider="AMCF player firmware endpoint over USB or serial",
            transport="usb_or_serial_control",
            direction="pc_to_player",
            capabilities=(
                "manifest_load",
                "event_schedule_load",
                "prefetch_hidden_staging_gate",
                "verify_staged_section",
                "switch_visible_gate",
                "blank_transition",
                "pause_and_fail_closed_stop",
                "bounded_seek_and_reverse",
                "audio_clock_feedback",
                "status_feedback",
            ),
            required_inputs=(
                "validated_amcf_manifest",
                "dynamic_timestamped_event_schedule",
                "a_b_section_index",
                "timing_and_audio_clock",
                "player_safety_profile",
            ),
            outputs=(
                "player_commands",
                "acknowledgements",
                "view_gate_state",
                "staging_gate_state",
                "timing_feedback",
                "fault_and_recovery_events",
            ),
            safety_requirements=(
                "only switch the visible gate after the staged section is verified",
                "drive updates from the AMCF timestamped schedule rather than fixed-FPS page flipping",
                "stop and blank on feedback timeout, checksum failure, or gate disagreement",
                "keep the primary displayed image path physical and optical rather than an LCD replacement",
            ),
            physical_player_alignment=(
                "folded indexed-media path",
                "visible view gate",
                "hidden staging gate",
                "dynamic AMCF update schedule",
                "timing and index feedback",
            ),
        ),
    )


def _validate_spec(spec: HardwareAdapterInterfaceSpec) -> dict[str, Any]:
    checks = {
        "identity_present": bool(spec.adapter_id and spec.corridor and spec.interface_name),
        "provider_present": bool(spec.provider and spec.transport and spec.direction),
        "capabilities_present": len(spec.capabilities) >= 4,
        "input_contract_present": len(spec.required_inputs) >= 3,
        "output_contract_present": len(spec.outputs) >= 3,
        "safety_contract_present": len(spec.safety_requirements) >= 3,
        "planned_only": spec.planned_only,
        "hardware_validation_not_claimed": not spec.hardware_validation_claimed,
    }
    return {
        "adapter_id": spec.adapter_id,
        "corridor": spec.corridor,
        "passed": all(checks.values()),
        "checks": checks,
    }


def _write_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# AMCF Hardware Adapter Planning",
        "",
        "This is an offline device-interface plan. It does not connect to a printer, scanner, camera, USB endpoint, serial endpoint, firmware, motor, sensor, or manufactured player.",
        "",
        f"- plan_version: {report['plan_version']}",
        f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
        f"- status: {report['feedback']['status']}",
        f"- hardware_connected: {'yes' if report['hardware_connected'] else 'no'}",
        f"- real_driver_or_protocol_used: {'yes' if report['real_driver_or_protocol_used'] else 'no'}",
        f"- display_allowed: {'yes' if report['feedback']['display_allowed'] else 'no'}",
        f"- transition_allowed: {'yes' if report['feedback']['transition_allowed'] else 'no'}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "",
        "## Planned interfaces",
        "",
    ]
    for spec in report["interface_specs"]:
        lines.append(
            f"- {spec['adapter_id']} ({spec['corridor']}): {spec['interface_name']} "
            f"via {spec['transport']}"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            report["feedback"]["message"],
            "",
            "The next implementation step is a separately reviewed device adapter for each selected Windows provider. Until then, all display and physical-transition permissions remain disabled.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_hardware_adapter_plan(
    repo_root: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    specs = _interface_specs()
    spec_checks = [_validate_spec(spec) for spec in specs]
    events: list[HardwarePlanStatusEvent] = []

    def add_event(
        state: str,
        code: str,
        accepted: bool,
        severity: str,
        message: str,
        retry_allowed: bool = False,
        fail_closed: bool = False,
        unsafe_acceptance: bool = False,
    ) -> None:
        events.append(
            HardwarePlanStatusEvent(
                sequence=len(events),
                state=state,
                code=code,
                accepted=accepted,
                severity=severity,
                message=message,
                display_allowed=False,
                transition_allowed=False,
                retry_allowed=retry_allowed,
                fail_closed=fail_closed,
                unsafe_acceptance=unsafe_acceptance,
            )
        )

    add_event(
        "planning_only",
        "HARDWARE_ADAPTER_PLANNING_ONLY",
        True,
        "info",
        "The run validates interface contracts without opening a device.",
    )

    software_output = out / "software_baseline"
    try:
        software_result = run_physical_software_adapter_roundtrip(root, software_output)
        software_report = software_result["report"]
        software_passed = bool(software_report.get("final_passed")) and int(
            software_report.get("unsafe_acceptance_count", 0)
        ) == 0
        software_baseline = {
            "final_passed": software_passed,
            "unsafe_acceptance_count": int(software_report.get("unsafe_acceptance_count", 0)),
            "output_dir": str(software_output),
        }
    except Exception as exc:  # noqa: BLE001 - convert planning dependency faults into a report.
        software_passed = False
        software_baseline = {
            "final_passed": False,
            "unsafe_acceptance_count": 1,
            "output_dir": str(software_output),
            "error": f"{type(exc).__name__}: {exc}",
        }

    add_event(
        "software_baseline_checked" if software_passed else "software_baseline_rejected",
        "SOFTWARE_ADAPTER_BASELINE_ACCEPTED" if software_passed else "SOFTWARE_ADAPTER_BASELINE_REJECTED",
        software_passed,
        "info" if software_passed else "error",
        "The existing software-only adapter contract passed before hardware planning."
        if software_passed
        else "The existing software-only adapter contract failed; hardware planning remains fail-closed.",
        retry_allowed=not software_passed,
        fail_closed=not software_passed,
        unsafe_acceptance=not software_passed,
    )

    for check in spec_checks:
        accepted = bool(check["passed"])
        add_event(
            "interface_specified" if accepted else "interface_rejected",
            "HARDWARE_INTERFACE_SPECIFIED" if accepted else "HARDWARE_INTERFACE_REJECTED",
            accepted,
            "info" if accepted else "error",
            f"Interface contract {'is complete' if accepted else 'is incomplete'} for {check['adapter_id']}.",
            retry_allowed=not accepted,
            fail_closed=not accepted,
            unsafe_acceptance=not accepted,
        )

    final_passed = software_passed and all(bool(item["passed"]) for item in spec_checks)
    add_event(
        "plan_ready" if final_passed else "plan_rejected",
        "HARDWARE_ADAPTER_PLAN_READY" if final_passed else "HARDWARE_ADAPTER_PLAN_REJECTED",
        final_passed,
        "info" if final_passed else "error",
        "Printer, reader, and player interface plans are ready for separately implemented device adapters."
        if final_passed
        else "The plan is incomplete; keep all physical transitions fail-closed.",
        retry_allowed=not final_passed,
        fail_closed=not final_passed,
        unsafe_acceptance=not final_passed,
    )

    unsafe_count = int(software_baseline["unsafe_acceptance_count"]) + sum(
        1 for event in events if event.unsafe_acceptance
    )
    feedback = {
        "status": "hardware_adapter_plan_ready" if final_passed else "hardware_adapter_plan_rejected",
        "display_allowed": False,
        "transition_allowed": False,
        "retry_allowed": not final_passed,
        "device_selection_required": True,
        "recommended_action": (
            "select_windows_device_profiles_and_implement_device_specific_adapters"
            if final_passed
            else "repair_software_baseline_or_interface_contract_before_device_work"
        ),
        "message": (
            "The Windows printer/carrier, reader/scanner, and physical-player control boundaries are specified. No device is connected and no physical transition is authorized."
            if final_passed
            else "Hardware planning is blocked by an incomplete software baseline or interface contract. Keep the system fail-closed."
        ),
    }
    claim_flags = dict(CLAIM_BOUNDARY_FLAGS)
    report = {
        "run_name": RUN_NAME,
        "plan_version": PLAN_VERSION,
        "repo_root": str(root),
        "output_dir": str(out),
        "final_passed": final_passed,
        "software_baseline": software_baseline,
        "interface_specs": [asdict(spec) for spec in specs],
        "interface_checks": spec_checks,
        "status_events": [asdict(event) for event in events],
        "feedback": feedback,
        "claim_boundary_flags": claim_flags,
        "unsafe_acceptance_count": unsafe_count,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "physical_hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "direct_hardware_transition_authorized": False,
        "source_video_required": False,
        "player_image_path": "physical_optical_primary_path",
        "player_schedule_contract": "dynamic_timestamped_amcf_updates",
    }
    capability_matrix = {
        "plan_version": PLAN_VERSION,
        "shared_safety_contract": [
            "all device acknowledgements are explicit",
            "hash and registration failures remain fail-closed",
            "display and transition permissions are disabled until device-specific validation",
            "AMCF timestamps and event ordering remain authoritative",
        ],
        "interfaces": {
            spec.adapter_id: {
                "corridor": spec.corridor,
                "provider": spec.provider,
                "transport": spec.transport,
                "direction": spec.direction,
                "capabilities": list(spec.capabilities),
                "planned_only": spec.planned_only,
            }
            for spec in specs
        },
    }
    _write_json(out / "hardware_adapter_plan_report.json", report)
    _write_json(out / "hardware_adapter_interface_specs.json", report["interface_specs"])
    _write_json(out / "hardware_adapter_capability_matrix.json", capability_matrix)
    _write_json(out / "hardware_adapter_status_events.json", report["status_events"])
    _write_json(out / "hardware_adapter_feedback.json", feedback)
    _write_summary(out / "HARDWARE_ADAPTER_PLANNING_SUMMARY.md", report)
    return {"report": report, "capability_matrix": capability_matrix, "output_dir": str(out)}
