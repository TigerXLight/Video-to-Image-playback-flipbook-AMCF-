from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS
from amcf_software_io_fixtures import load_fixture_bundle


PROVIDER_RUNTIME_VERSION = "amcf-hardware-provider-runtime-v1"
RUN_NAME = "AMCF_HARDWARE_PROVIDER_RUNTIME_V1"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ProviderDescriptor:
    provider_id: str
    corridor: str
    backend: str
    transport: str
    capabilities: tuple[str, ...]
    hardware_connected: bool = False
    real_driver_or_protocol_used: bool = False
    hardware_validation_claimed: bool = False


@dataclass(frozen=True)
class ProviderStatusEvent:
    sequence: int
    provider_id: str
    corridor: str
    state: str
    code: str
    accepted: bool
    severity: str
    message: str
    display_allowed: bool
    transition_allowed: bool
    retry_allowed: bool
    rescan_allowed: bool
    fail_closed: bool
    unsafe_acceptance: bool = False


class PrinterCarrierProvider(ABC):
    @abstractmethod
    def describe(self) -> ProviderDescriptor:
        raise NotImplementedError

    @abstractmethod
    def submit_carrier(self, manifest: dict[str, Any], artifact_hash: str) -> dict[str, Any]:
        raise NotImplementedError


class ReaderCaptureProvider(ABC):
    @abstractmethod
    def describe(self) -> ProviderDescriptor:
        raise NotImplementedError

    @abstractmethod
    def capture_section(self, section: dict[str, Any], capture: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class PlayerControlProvider(ABC):
    @abstractmethod
    def describe(self) -> ProviderDescriptor:
        raise NotImplementedError

    @abstractmethod
    def load_manifest(self, manifest: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def prefetch_section(self, section_id: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def verify_staged_section(self, section_id: str, expected_hash: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def switch_visible(self, section_id: str) -> dict[str, Any]:
        raise NotImplementedError


class SimulatedPrintToFileProvider(PrinterCarrierProvider):
    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id="simulated-print-to-file-provider",
            corridor="pc_to_printer",
            backend="deterministic_print_to_file",
            transport="software_artifact_only",
            capabilities=(
                "carrier_artifact_generation",
                "spooler_job_identity",
                "artifact_hash_acknowledgement",
                "registration_lane_validation",
                "fail_closed_print_gate",
            ),
        )

    def submit_carrier(self, manifest: dict[str, Any], artifact_hash: str) -> dict[str, Any]:
        job_id = "SIM-PRINT-" + _sha256({"manifest": manifest, "artifact_hash": artifact_hash})[:16]
        return {
            "accepted": True,
            "status": "simulated_submission_acknowledged",
            "job_id": job_id,
            "artifact_hash": artifact_hash,
            "hash_acknowledged": True,
            "physical_output_created": False,
            "hardware_connected": False,
            "transition_allowed": False,
        }


class SimulatedReaderCaptureProvider(ReaderCaptureProvider):
    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id="simulated-reader-capture-provider",
            corridor="reader_to_pc",
            backend="fixture_capture_recovery",
            transport="software_fixture_only",
            capabilities=(
                "device_profile_resolution",
                "section_capture",
                "registration_marker_feedback",
                "colour_registry_feedback",
                "section_hash_feedback",
                "rescan_request",
                "fail_closed_reader_gate",
            ),
        )

    def capture_section(self, section: dict[str, Any], capture: dict[str, Any]) -> dict[str, Any]:
        registration_ok = capture.get("registration_status") == "matched"
        hash_ok = capture.get("hash_status") == "matched"
        accepted = registration_ok and hash_ok
        return {
            "accepted": accepted,
            "section_id": section["section_id"],
            "registration_status": capture.get("registration_status", "missing"),
            "hash_status": capture.get("hash_status", "missing"),
            "colour_status": capture.get("colour_status", "missing"),
            "rescan_required": not accepted,
            "hardware_connected": False,
            "real_scan_performed": False,
            "fail_closed": not accepted,
        }


class SimulatedPlayerControlProvider(PlayerControlProvider):
    def __init__(self) -> None:
        self._manifest: dict[str, Any] | None = None
        self._sections: dict[str, dict[str, Any]] = {}
        self._staged_section: str | None = None
        self._verified_section: str | None = None
        self._visible_section: str | None = None

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id="simulated-player-control-provider",
            corridor="pc_to_player",
            backend="folded_ab_optical_player_control_fixture",
            transport="software_fixture_only",
            capabilities=(
                "manifest_load",
                "dynamic_event_schedule_load",
                "prefetch_hidden_staging_gate",
                "verify_staged_section",
                "switch_visible_gate",
                "audio_clock_feedback",
                "bounded_seek_and_reverse",
                "fail_closed_stop",
            ),
        )

    def load_manifest(self, manifest: dict[str, Any]) -> dict[str, Any]:
        sections = manifest.get("physical_sections", [])
        self._manifest = manifest
        self._sections = {str(item["section_id"]): item for item in sections}
        accepted = bool(self._sections) and len(manifest.get("update_events", [])) > 0
        return {
            "accepted": accepted,
            "status": "manifest_loaded" if accepted else "manifest_rejected",
            "section_count": len(self._sections),
            "dynamic_schedule_present": bool(manifest.get("update_events")),
            "hardware_connected": False,
            "transition_allowed": False,
            "fail_closed": not accepted,
        }

    def prefetch_section(self, section_id: str) -> dict[str, Any]:
        accepted = section_id in self._sections
        if accepted:
            self._staged_section = section_id
            self._verified_section = None
        return {
            "accepted": accepted,
            "status": "section_prefetched" if accepted else "section_not_found",
            "section_id": section_id,
            "staging_gate": "hidden" if accepted else "closed",
            "transition_allowed": False,
            "fail_closed": not accepted,
        }

    def verify_staged_section(self, section_id: str, expected_hash: str) -> dict[str, Any]:
        section = self._sections.get(section_id)
        actual_hash = section.get("payload_hash") if section else None
        accepted = self._staged_section == section_id and actual_hash == expected_hash
        if accepted:
            self._verified_section = section_id
        return {
            "accepted": accepted,
            "status": "staged_section_verified" if accepted else "staged_section_rejected",
            "section_id": section_id,
            "expected_hash": expected_hash,
            "actual_hash": actual_hash,
            "transition_allowed": False,
            "fail_closed": not accepted,
        }

    def switch_visible(self, section_id: str) -> dict[str, Any]:
        accepted = self._verified_section == section_id
        if accepted:
            self._visible_section = section_id
        return {
            "accepted": accepted,
            "status": "virtual_view_gate_updated" if accepted else "visible_switch_blocked",
            "section_id": section_id,
            "virtual_visible_section": self._visible_section,
            "physical_transition_authorized": False,
            "display_allowed": False,
            "transition_allowed": False,
            "fail_closed": not accepted,
        }


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# AMCF Hardware Provider Runtime",
        "",
        "This run exercises provider-neutral printer, reader, and player interfaces with deterministic software implementations. It does not open hardware or claim a real driver/protocol.",
        "",
        f"- runtime_version: {report['runtime_version']}",
        f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
        f"- provider_count: {len(report['provider_descriptors'])}",
        f"- scheduled_events: {report['scheduled_event_count']}",
        f"- unverified_switch_blocked: {'yes' if report['unverified_switch_blocked'] else 'no'}",
        f"- hardware_connected: {'yes' if report['hardware_connected'] else 'no'}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "",
        "The interfaces are ready for future device-specific providers. Physical display and transition permissions remain disabled.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def run_hardware_provider_runtime(
    repo_root: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    bundle = load_fixture_bundle(root)
    package = bundle["package"]
    manifest = package["manifest"]
    sections = manifest["physical_sections"]
    captures = {item["section_id"]: item for item in bundle["reader_capture"]["simulated_captures"]}

    printer: PrinterCarrierProvider = SimulatedPrintToFileProvider()
    reader: ReaderCaptureProvider = SimulatedReaderCaptureProvider()
    player: PlayerControlProvider = SimulatedPlayerControlProvider()
    descriptors = [printer.describe(), reader.describe(), player.describe()]
    events: list[ProviderStatusEvent] = []

    def add_event(
        provider_id: str,
        corridor: str,
        state: str,
        code: str,
        accepted: bool,
        message: str,
        severity: str = "info",
        retry_allowed: bool = False,
        rescan_allowed: bool = False,
        fail_closed: bool = False,
        unsafe_acceptance: bool = False,
    ) -> None:
        events.append(
            ProviderStatusEvent(
                sequence=len(events),
                provider_id=provider_id,
                corridor=corridor,
                state=state,
                code=code,
                accepted=accepted,
                severity=severity,
                message=message,
                display_allowed=False,
                transition_allowed=False,
                retry_allowed=retry_allowed,
                rescan_allowed=rescan_allowed,
                fail_closed=fail_closed,
                unsafe_acceptance=unsafe_acceptance,
            )
        )

    for descriptor in descriptors:
        add_event(
            descriptor.provider_id,
            descriptor.corridor,
            "provider_ready",
            "PROVIDER_INTERFACE_READY",
            True,
            f"Provider interface ready in simulated mode: {descriptor.backend}.",
        )

    artifact_hash = _sha256(manifest)
    printer_result = printer.submit_carrier(manifest, artifact_hash)
    add_event(
        printer.describe().provider_id,
        "pc_to_printer",
        "carrier_acknowledged" if printer_result["accepted"] else "carrier_rejected",
        "CARRIER_ARTIFACT_ACKNOWLEDGED" if printer_result["accepted"] else "CARRIER_ARTIFACT_REJECTED",
        bool(printer_result["accepted"]),
        "Carrier artifact identity acknowledged by the simulated print-to-file provider."
        if printer_result["accepted"]
        else "Carrier artifact was rejected; keep the print gate fail-closed.",
        fail_closed=not bool(printer_result["accepted"]),
    )

    reader_results: list[dict[str, Any]] = []
    for section in sections:
        result = reader.capture_section(section, captures.get(section["section_id"], {}))
        reader_results.append(result)
        accepted = bool(result["accepted"])
        add_event(
            reader.describe().provider_id,
            "reader_to_pc",
            "section_recovered" if accepted else "section_rejected",
            "SECTION_CAPTURE_RECOVERED" if accepted else "SECTION_CAPTURE_REJECTED",
            accepted,
            f"Section {section['section_id']} passed registration and hash capture checks."
            if accepted
            else f"Section {section['section_id']} failed capture checks and requires rescan.",
            rescan_allowed=not accepted,
            fail_closed=not accepted,
        )

    player_load = player.load_manifest(manifest)
    add_event(
        player.describe().provider_id,
        "pc_to_player",
        "manifest_loaded" if player_load["accepted"] else "manifest_rejected",
        "PLAYER_MANIFEST_LOADED" if player_load["accepted"] else "PLAYER_MANIFEST_REJECTED",
        bool(player_load["accepted"]),
        "Dynamic AMCF schedule loaded into the simulated player provider."
        if player_load["accepted"]
        else "Player manifest was rejected; keep the player stopped.",
        fail_closed=not bool(player_load["accepted"]),
    )
    player_transcript: list[dict[str, Any]] = []
    for event in manifest["update_events"]:
        section_id = str(event["section_id"])
        section = next(item for item in sections if item["section_id"] == section_id)
        prefetch = player.prefetch_section(section_id)
        verify = player.verify_staged_section(section_id, str(section["payload_hash"]))
        switch = player.switch_visible(section_id)
        row = {
            "event_id": event["event_id"],
            "section_id": section_id,
            "timestamp_ms": event["timestamp_ms"],
            "dwell_ms": event["dwell_ms"],
            "prefetch": prefetch,
            "verify": verify,
            "switch": switch,
            "physical_transition_authorized": False,
        }
        player_transcript.append(row)
        accepted = bool(prefetch["accepted"] and verify["accepted"] and switch["accepted"])
        add_event(
            player.describe().provider_id,
            "pc_to_player",
            "virtual_schedule_applied" if accepted else "schedule_blocked",
            "PLAYER_EVENT_SCHEDULE_APPLIED" if accepted else "PLAYER_EVENT_BLOCKED_FAIL_CLOSED",
            accepted,
            f"Event {event['event_id']} was staged, verified, and applied to the virtual view state."
            if accepted
            else f"Event {event['event_id']} was blocked before virtual view-state application.",
            fail_closed=not accepted,
        )

    safety_probe = SimulatedPlayerControlProvider()
    safety_probe.load_manifest(manifest)
    blocked = safety_probe.switch_visible(str(sections[0]["section_id"]))
    unverified_switch_blocked = not bool(blocked["accepted"]) and bool(blocked["fail_closed"])
    add_event(
        safety_probe.describe().provider_id,
        "pc_to_player",
        "unverified_switch_blocked" if unverified_switch_blocked else "safety_probe_failed",
        "UNVERIFIED_SWITCH_BLOCKED_FAIL_CLOSED" if unverified_switch_blocked else "UNVERIFIED_SWITCH_NOT_BLOCKED",
        unverified_switch_blocked,
        "The provider refused a visible-gate switch without a verified staged section."
        if unverified_switch_blocked
        else "The provider allowed an unverified visible-gate switch.",
        fail_closed=not unverified_switch_blocked,
        unsafe_acceptance=not unverified_switch_blocked,
    )

    unsafe_count = sum(1 for event in events if event.unsafe_acceptance)
    final_passed = (
        bool(printer_result["accepted"])
        and all(bool(item["accepted"]) for item in reader_results)
        and bool(player_load["accepted"])
        and all(
            bool(row["prefetch"]["accepted"] and row["verify"]["accepted"] and row["switch"]["accepted"])
            for row in player_transcript
        )
        and unverified_switch_blocked
        and unsafe_count == 0
    )
    feedback = {
        "status": "provider_runtime_ready" if final_passed else "provider_runtime_rejected_fail_closed",
        "display_allowed": False,
        "transition_allowed": False,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "recommended_action": (
            "implement_a_device_specific_provider_against_the_abstract_interfaces"
            if final_passed
            else "repair_provider_contract_or_keep_all_transitions_blocked"
        ),
        "message": (
            "Provider-neutral interfaces and the fail-closed handshake are ready for future device-specific implementations."
            if final_passed
            else "A provider handshake failed; keep the runtime fail-closed before adding device code."
        ),
    }
    report = {
        "run_name": RUN_NAME,
        "runtime_version": PROVIDER_RUNTIME_VERSION,
        "repo_root": str(root),
        "output_dir": str(out),
        "final_passed": final_passed,
        "provider_descriptors": [asdict(item) for item in descriptors],
        "printer_result": printer_result,
        "reader_results": reader_results,
        "player_manifest_result": player_load,
        "player_event_transcript": player_transcript,
        "scheduled_event_count": len(manifest["update_events"]),
        "unverified_switch_blocked": unverified_switch_blocked,
        "status_events": [asdict(item) for item in events],
        "feedback": feedback,
        "claim_boundary_flags": dict(CLAIM_BOUNDARY_FLAGS),
        "unsafe_acceptance_count": unsafe_count,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "physical_hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "direct_hardware_transition_authorized": False,
        "player_image_path": "physical_optical_primary_path",
        "player_schedule_contract": "dynamic_timestamped_amcf_updates",
    }
    _write_json(out / "hardware_provider_runtime_report.json", report)
    _write_json(out / "hardware_provider_capabilities.json", report["provider_descriptors"])
    _write_json(out / "hardware_provider_status_events.json", report["status_events"])
    _write_json(out / "hardware_provider_feedback.json", feedback)
    _write_json(out / "hardware_provider_command_transcript.json", player_transcript)
    _write_summary(out / "HARDWARE_PROVIDER_RUNTIME_SUMMARY.md", report)
    return {"report": report, "output_dir": str(out)}
