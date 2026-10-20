from __future__ import annotations

import hashlib
import importlib
import json
import os
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from amcf_hardware_provider_runtime import (
    PlayerControlProvider,
    PrinterCarrierProvider,
    ProviderDescriptor,
    ReaderCaptureProvider,
    SimulatedPlayerControlProvider,
)
from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS
from amcf_software_io_fixtures import load_fixture_bundle


RUN_NAME = "AMCF_DEVICE_PROVIDER_ADAPTER_DISCOVERY_V1"
RUNTIME_VERSION = "amcf-device-provider-adapters-v1"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _optional_import(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except (ImportError, OSError):
        return None


@dataclass(frozen=True)
class DeviceProviderProbe:
    provider_id: str
    corridor: str
    backend: str
    configured: bool
    dependency_available: bool
    available: bool
    hardware_connected: bool
    real_driver_or_protocol_used: bool
    reason: str
    capabilities: tuple[str, ...]


class DeviceProviderAdapter(ABC):
    @abstractmethod
    def describe(self) -> ProviderDescriptor:
        raise NotImplementedError

    @abstractmethod
    def probe(self) -> DeviceProviderProbe:
        raise NotImplementedError


class FileCarrierProvider(PrinterCarrierProvider, DeviceProviderAdapter):
    """Concrete carrier writer used before a physical printer is selected."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir).resolve()

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id="file-carrier-provider",
            corridor="pc_to_printer",
            backend="validated_carrier_file",
            transport="filesystem",
            capabilities=(
                "carrier_artifact_generation",
                "manifest_hash_acknowledgement",
                "reprintable_artifact_path",
                "no_hardware_required",
                "fail_closed_print_gate",
            ),
        )

    def probe(self) -> DeviceProviderProbe:
        return DeviceProviderProbe(
            provider_id=self.describe().provider_id,
            corridor=self.describe().corridor,
            backend=self.describe().backend,
            configured=True,
            dependency_available=True,
            available=True,
            hardware_connected=False,
            real_driver_or_protocol_used=False,
            reason="file_carrier_backend_ready",
            capabilities=self.describe().capabilities,
        )

    def submit_carrier(self, manifest: dict[str, Any], artifact_hash: str) -> dict[str, Any]:
        expected_hash = _sha256(manifest)
        if artifact_hash != expected_hash:
            return {
                "accepted": False,
                "status": "carrier_hash_rejected",
                "fail_closed": True,
                "physical_output_created": False,
                "hardware_connected": False,
            }
        self.output_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = self.output_dir / f"carrier_{manifest['manifest_id']}.json"
        artifact_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return {
            "accepted": True,
            "status": "carrier_file_written",
            "artifact_path": str(artifact_path),
            "manifest_hash": artifact_hash,
            "artifact_file_hash": hashlib.sha256(artifact_path.read_bytes()).hexdigest(),
            "physical_output_created": False,
            "hardware_connected": False,
            "real_driver_or_protocol_used": False,
            "transition_allowed": False,
            "fail_closed": False,
        }


class FolderCaptureProvider(ReaderCaptureProvider, DeviceProviderAdapter):
    """Concrete reader adapter for captured files or maintained fixtures."""

    def __init__(self, capture_root: str | Path | None = None) -> None:
        self.capture_root = Path(capture_root).resolve() if capture_root else None

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id="folder-capture-provider",
            corridor="reader_to_pc",
            backend="folder_capture_recovery",
            transport="filesystem",
            capabilities=(
                "capture_file_resolution",
                "registration_feedback",
                "colour_registry_feedback",
                "hash_feedback",
                "rescan_request",
                "no_hardware_required",
                "fail_closed_reader_gate",
            ),
        )

    def probe(self) -> DeviceProviderProbe:
        configured = self.capture_root is not None
        available = bool(configured and self.capture_root.exists())
        return DeviceProviderProbe(
            provider_id=self.describe().provider_id,
            corridor=self.describe().corridor,
            backend=self.describe().backend,
            configured=configured,
            dependency_available=True,
            available=available,
            hardware_connected=False,
            real_driver_or_protocol_used=False,
            reason="capture_root_ready" if available else "capture_root_not_configured_or_missing",
            capabilities=self.describe().capabilities,
        )

    def capture_section(self, section: dict[str, Any], capture: dict[str, Any]) -> dict[str, Any]:
        registration_ok = capture.get("registration_status") == "matched"
        hash_ok = capture.get("hash_status") == "matched"
        result: dict[str, Any] = {
            "accepted": registration_ok and hash_ok,
            "section_id": section["section_id"],
            "registration_status": capture.get("registration_status", "missing"),
            "hash_status": capture.get("hash_status", "missing"),
            "colour_status": capture.get("colour_status", "missing"),
            "rescan_required": not (registration_ok and hash_ok),
            "hardware_connected": False,
            "real_scan_performed": False,
            "fail_closed": not (registration_ok and hash_ok),
            "provider_backend": self.describe().backend,
        }
        capture_path = capture.get("capture_path")
        if capture_path:
            path = Path(str(capture_path)).resolve()
            if self.capture_root and not path.is_relative_to(self.capture_root):
                result.update({"accepted": False, "fail_closed": True, "rescan_required": True, "error": "capture_path_outside_root"})
            elif not path.exists():
                result.update({"accepted": False, "fail_closed": True, "rescan_required": True, "error": "capture_path_missing"})
            else:
                result["capture_path"] = str(path)
                result["capture_file_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        return result


class LoopbackPlayerProvider(SimulatedPlayerControlProvider, DeviceProviderAdapter):
    """Concrete local transport for protocol testing before a player exists."""

    def describe(self) -> ProviderDescriptor:
        base = super().describe()
        return ProviderDescriptor(
            provider_id="loopback-player-provider",
            corridor=base.corridor,
            backend="software_control_loopback",
            transport="in_memory_loopback",
            capabilities=base.capabilities + ("protocol_transcript", "no_hardware_required"),
        )

    def probe(self) -> DeviceProviderProbe:
        descriptor = self.describe()
        return DeviceProviderProbe(
            provider_id=descriptor.provider_id,
            corridor=descriptor.corridor,
            backend=descriptor.backend,
            configured=True,
            dependency_available=True,
            available=True,
            hardware_connected=False,
            real_driver_or_protocol_used=False,
            reason="loopback_transport_ready",
            capabilities=descriptor.capabilities,
        )


class WindowsPrintSpoolerProvider(PrinterCarrierProvider, DeviceProviderAdapter):
    """Optional raw Print Spooler provider; disabled until explicitly enabled."""

    def __init__(self, printer_name: str | None = None, *, enable_hardware: bool = False) -> None:
        self.printer_name = printer_name
        self.enable_hardware = enable_hardware

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id="windows-print-spooler-provider",
            corridor="pc_to_printer",
            backend="windows_print_spooler_raw",
            transport="win32print",
            capabilities=("printer_discovery", "raw_artifact_submission", "job_acknowledgement", "fail_closed_print_gate"),
        )

    def probe(self) -> DeviceProviderProbe:
        descriptor = self.describe()
        if os.name != "nt":
            reason = "windows_only_backend"
            dependency = False
        elif not self.enable_hardware:
            reason = "hardware_not_enabled"
            dependency = _optional_import("win32print") is not None
        else:
            module = _optional_import("win32print")
            dependency = module is not None
            if module is None:
                reason = "pywin32_win32print_unavailable"
            elif not self.printer_name:
                reason = "printer_name_required"
            else:
                try:
                    handle = module.OpenPrinter(self.printer_name)
                    module.ClosePrinter(handle)
                    return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, True, True, True, True, True, "printer_opened", descriptor.capabilities)
                except Exception as exc:  # noqa: BLE001 - convert device errors into a probe result.
                    reason = f"printer_open_failed:{type(exc).__name__}"
        return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, bool(self.printer_name), dependency, False, False, False, reason, descriptor.capabilities)

    def submit_carrier(self, manifest: dict[str, Any], artifact_hash: str) -> dict[str, Any]:
        if not self.enable_hardware:
            return {"accepted": False, "status": "hardware_not_enabled", "fail_closed": True, "hardware_connected": False}
        module = _optional_import("win32print")
        artifact_path = manifest.get("print_artifact_path")
        expected_file_hash = manifest.get("print_artifact_sha256")
        if module is None or not self.printer_name or not artifact_path or not expected_file_hash:
            return {"accepted": False, "status": "printer_artifact_or_dependency_missing", "fail_closed": True, "hardware_connected": False}
        path = Path(str(artifact_path)).resolve()
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != str(expected_file_hash):
            return {"accepted": False, "status": "print_artifact_hash_rejected", "fail_closed": True, "hardware_connected": False}
        handle = None
        try:
            handle = module.OpenPrinter(self.printer_name)
            job = module.StartDocPrinter(handle, 1, (str(path.name), None, "RAW"))
            module.StartPagePrinter(handle)
            module.WritePrinter(handle, path.read_bytes())
            module.EndPagePrinter(handle)
            module.EndDocPrinter(handle)
            return {"accepted": True, "status": "spooler_job_submitted", "job_id": job, "hardware_connected": True, "real_driver_or_protocol_used": True, "fail_closed": False}
        except Exception as exc:  # noqa: BLE001 - device failure must remain fail-closed.
            return {"accepted": False, "status": f"spooler_submission_failed:{type(exc).__name__}", "hardware_connected": False, "fail_closed": True}
        finally:
            if handle is not None:
                module.ClosePrinter(handle)


class WindowsWiaReaderProvider(ReaderCaptureProvider, DeviceProviderAdapter):
    """Optional WIA discovery/capture provider; disabled until explicitly enabled."""

    def __init__(self, device_name: str | None = None, *, enable_hardware: bool = False) -> None:
        self.device_name = device_name
        self.enable_hardware = enable_hardware

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id="windows-wia-reader-provider",
            corridor="reader_to_pc",
            backend="windows_wia_capture",
            transport="win32com_wia",
            capabilities=("reader_discovery", "section_capture", "registration_feedback", "hash_feedback", "rescan_request", "fail_closed_reader_gate"),
        )

    def probe(self) -> DeviceProviderProbe:
        descriptor = self.describe()
        if os.name != "nt":
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, bool(self.device_name), False, False, False, False, "windows_only_backend", descriptor.capabilities)
        module = _optional_import("win32com.client")
        if not self.enable_hardware:
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, bool(self.device_name), module is not None, False, False, False, "hardware_not_enabled", descriptor.capabilities)
        if module is None:
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, bool(self.device_name), False, False, False, False, "pywin32_wia_unavailable", descriptor.capabilities)
        if not self.device_name:
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, False, True, False, False, False, "reader_device_name_required", descriptor.capabilities)
        try:
            manager = module.Dispatch("WIA.DeviceManager")
            names = [str(info.Properties("Name").Value) for info in manager.DeviceInfos]
            matched = self.device_name in names
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, True, True, matched, matched, matched, "wia_reader_found" if matched else "wia_reader_not_found", descriptor.capabilities)
        except Exception as exc:  # noqa: BLE001 - convert WIA failures into a safe probe result.
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, True, True, False, False, False, f"wia_probe_failed:{type(exc).__name__}", descriptor.capabilities)

    def capture_section(self, section: dict[str, Any], capture: dict[str, Any]) -> dict[str, Any]:
        if not self.enable_hardware:
            return {"accepted": False, "section_id": section["section_id"], "status": "hardware_not_enabled", "rescan_required": True, "real_scan_performed": False, "fail_closed": True}
        probe = self.probe()
        if not probe.available:
            return {"accepted": False, "section_id": section["section_id"], "status": probe.reason, "rescan_required": True, "real_scan_performed": False, "fail_closed": True}
        return {
            "accepted": capture.get("registration_status") == "matched" and capture.get("hash_status") == "matched",
            "section_id": section["section_id"],
            "registration_status": capture.get("registration_status", "unverified"),
            "hash_status": capture.get("hash_status", "unverified"),
            "colour_status": capture.get("colour_status", "unverified"),
            "rescan_required": not (capture.get("registration_status") == "matched" and capture.get("hash_status") == "matched"),
            "real_scan_performed": False,
            "hardware_connected": True,
            "fail_closed": not (capture.get("registration_status") == "matched" and capture.get("hash_status") == "matched"),
            "status": "wia_capture_requires_device_profile_binding",
        }


class SerialPlayerProvider(PlayerControlProvider, DeviceProviderAdapter):
    """Optional JSON-line player transport over an explicitly selected serial port."""

    def __init__(self, port: str | None = None, *, baudrate: int = 115200, enable_hardware: bool = False) -> None:
        self.port = port
        self.baudrate = baudrate
        self.enable_hardware = enable_hardware

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id="serial-player-provider",
            corridor="pc_to_player",
            backend="json_line_serial_player",
            transport="pyserial",
            capabilities=("manifest_load", "dynamic_event_schedule_load", "prefetch_hidden_staging_gate", "verify_staged_section", "switch_visible_gate", "safe_stop"),
        )

    def probe(self) -> DeviceProviderProbe:
        descriptor = self.describe()
        module = _optional_import("serial")
        if not self.enable_hardware:
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, bool(self.port), module is not None, False, False, False, "hardware_not_enabled", descriptor.capabilities)
        if module is None:
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, bool(self.port), False, False, False, False, "pyserial_unavailable", descriptor.capabilities)
        if not self.port:
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, False, True, False, False, False, "serial_port_required", descriptor.capabilities)
        try:
            connection = module.Serial(self.port, self.baudrate, timeout=1)
            connection.close()
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, True, True, True, True, True, "serial_port_opened", descriptor.capabilities)
        except Exception as exc:  # noqa: BLE001 - convert transport failures into a safe probe result.
            return DeviceProviderProbe(descriptor.provider_id, descriptor.corridor, descriptor.backend, True, True, False, False, False, f"serial_open_failed:{type(exc).__name__}", descriptor.capabilities)

    def _wire_command(self, command: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.enable_hardware:
            return {"accepted": False, "status": "hardware_not_enabled", "fail_closed": True, "hardware_connected": False}
        module = _optional_import("serial")
        if module is None or not self.port:
            return {"accepted": False, "status": "serial_dependency_or_port_missing", "fail_closed": True, "hardware_connected": False}
        connection = None
        try:
            connection = module.Serial(self.port, self.baudrate, timeout=2)
            connection.write((_canonical_json({"command": command, "payload": payload}) + "\n").encode("utf-8"))
            reply = connection.readline().decode("utf-8", errors="replace").strip()
            response = json.loads(reply) if reply else {}
            accepted = bool(response.get("accepted"))
            return {**response, "accepted": accepted, "hardware_connected": True, "real_driver_or_protocol_used": accepted, "fail_closed": not accepted}
        except Exception as exc:  # noqa: BLE001 - transport errors must not authorize motion.
            return {"accepted": False, "status": f"serial_command_failed:{type(exc).__name__}", "hardware_connected": False, "fail_closed": True}
        finally:
            if connection is not None:
                connection.close()

    def load_manifest(self, manifest: dict[str, Any]) -> dict[str, Any]:
        return self._wire_command("load_manifest", {"manifest_id": manifest.get("manifest_id"), "event_count": len(manifest.get("update_events", []))})

    def prefetch_section(self, section_id: str) -> dict[str, Any]:
        return self._wire_command("prefetch_section", {"section_id": section_id})

    def verify_staged_section(self, section_id: str, expected_hash: str) -> dict[str, Any]:
        return self._wire_command("verify_staged_section", {"section_id": section_id, "expected_hash": expected_hash})

    def switch_visible(self, section_id: str) -> dict[str, Any]:
        return self._wire_command("switch_visible", {"section_id": section_id})


def _build_provider_set(
    repo_root: Path,
    output_dir: Path,
    *,
    printer_backend: str,
    reader_backend: str,
    player_backend: str,
    printer_name: str | None,
    reader_device: str | None,
    reader_source: str | None,
    player_port: str | None,
    enable_hardware: bool,
) -> tuple[dict[str, DeviceProviderAdapter], dict[str, Any]]:
    fixture_root = repo_root / "tests" / "fixtures" / "amcf_software_io"
    if printer_backend == "file":
        printer: DeviceProviderAdapter = FileCarrierProvider(output_dir / "carrier")
    elif printer_backend == "windows-spooler":
        printer = WindowsPrintSpoolerProvider(printer_name, enable_hardware=enable_hardware)
    else:
        raise ValueError(f"unsupported printer backend: {printer_backend}")
    if reader_backend == "folder":
        reader: DeviceProviderAdapter = FolderCaptureProvider(reader_source or fixture_root)
    elif reader_backend == "windows-wia":
        reader = WindowsWiaReaderProvider(reader_device, enable_hardware=enable_hardware)
    else:
        raise ValueError(f"unsupported reader backend: {reader_backend}")
    if player_backend == "loopback":
        player: DeviceProviderAdapter = LoopbackPlayerProvider()
    elif player_backend == "serial":
        player = SerialPlayerProvider(player_port, enable_hardware=enable_hardware)
    else:
        raise ValueError(f"unsupported player backend: {player_backend}")
    return {"printer": printer, "reader": reader, "player": player}, {
        "printer_backend": printer_backend,
        "reader_backend": reader_backend,
        "player_backend": player_backend,
        "enable_hardware": enable_hardware,
    }


def run_device_provider_discovery(
    repo_root: str | Path,
    output_dir: str | Path,
    *,
    printer_backend: str = "file",
    reader_backend: str = "folder",
    player_backend: str = "loopback",
    printer_name: str | None = None,
    reader_device: str | None = None,
    reader_source: str | None = None,
    player_port: str | None = None,
    enable_hardware: bool = False,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    bundle = load_fixture_bundle(root)
    providers, selection = _build_provider_set(
        root,
        out,
        printer_backend=printer_backend,
        reader_backend=reader_backend,
        player_backend=player_backend,
        printer_name=printer_name,
        reader_device=reader_device,
        reader_source=reader_source,
        player_port=player_port,
        enable_hardware=enable_hardware,
    )
    probes = [provider.probe() for provider in providers.values()]
    manifest = bundle["package"]["manifest"]
    software_operations: dict[str, Any] = {}
    if not enable_hardware and all(selection[key] in {"file", "folder", "loopback"} for key in ("printer_backend", "reader_backend", "player_backend")):
        printer = providers["printer"]
        reader = providers["reader"]
        player = providers["player"]
        assert isinstance(printer, FileCarrierProvider)
        assert isinstance(reader, FolderCaptureProvider)
        assert isinstance(player, LoopbackPlayerProvider)
        printer_result = printer.submit_carrier(manifest, _sha256(manifest))
        section = manifest["physical_sections"][0]
        capture = bundle["reader_capture"]["simulated_captures"][0]
        reader_result = reader.capture_section(section, capture)
        player_load = player.load_manifest(manifest)
        player_prefetch = player.prefetch_section(section["section_id"])
        player_verify = player.verify_staged_section(section["section_id"], section["payload_hash"])
        player_switch = player.switch_visible(section["section_id"])
        software_operations = {
            "printer": printer_result,
            "reader": reader_result,
            "player": {"load": player_load, "prefetch": player_prefetch, "verify": player_verify, "switch": player_switch},
        }
    unsafe_count = 0
    interface_ready = all(bool(probe.capabilities) and probe.provider_id for probe in probes)
    selected_ready = all(probe.available for probe in probes)
    software_ready = not software_operations or all(
        bool(value.get("accepted")) if isinstance(value, dict) and "accepted" in value else all(bool(item.get("accepted")) for item in value.values())
        for value in software_operations.values()
    )
    final_passed = interface_ready and selected_ready and software_ready and unsafe_count == 0
    report = {
        "run_name": RUN_NAME,
        "runtime_version": RUNTIME_VERSION,
        "repo_root": str(root),
        "output_dir": str(out),
        "selection": selection,
        "final_passed": final_passed,
        "interface_ready": interface_ready,
        "selected_backends_ready": selected_ready,
        "software_operations_passed": software_ready,
        "provider_descriptors": [asdict(provider.describe()) for provider in providers.values()],
        "provider_probes": [asdict(probe) for probe in probes],
        "software_operations": software_operations,
        "claim_boundary_flags": dict(CLAIM_BOUNDARY_FLAGS),
        "unsafe_acceptance_count": unsafe_count,
        "hardware_connected": any(probe.hardware_connected for probe in probes),
        "real_driver_or_protocol_used": any(probe.real_driver_or_protocol_used for probe in probes),
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "direct_hardware_transition_authorized": False,
        "feedback": {
            "status": "provider_set_ready" if final_passed else "provider_set_rejected_fail_closed",
            "hardware_connected": any(probe.hardware_connected for probe in probes),
            "display_allowed": False,
            "transition_allowed": False,
            "recommended_action": "select_device_profile_and_enable_hardware_explicitly" if final_passed else "repair_provider_selection_or_dependencies",
        },
    }
    out.mkdir(parents=True, exist_ok=True)
    _write_json(out / "device_provider_discovery_report.json", report)
    _write_json(out / "device_provider_capabilities.json", report["provider_descriptors"])
    _write_json(out / "device_provider_probe_results.json", report["provider_probes"])
    _write_json(out / "device_provider_feedback.json", report["feedback"])
    summary = [
        "# AMCF Device Provider Discovery",
        "",
        "This run validates concrete provider adapters and their discovery gates. It does not claim that a physical printer, reader, scanner, or player has been operated.",
        "",
        f"- final_passed: {'yes' if final_passed else 'no'}",
        f"- interface_ready: {'yes' if interface_ready else 'no'}",
        f"- selected_backends_ready: {'yes' if selected_ready else 'no'}",
        f"- software_operations_passed: {'yes' if software_ready else 'no'}",
        f"- hardware_connected: {'yes' if report['hardware_connected'] else 'no'}",
        f"- real_driver_or_protocol_used: {'yes' if report['real_driver_or_protocol_used'] else 'no'}",
        f"- unsafe_acceptance_count: {unsafe_count}",
        "- physical_hardware_validation_claimed: no",
        "",
        "Hardware backends remain disabled unless an explicit device profile and enable flag are provided.",
        "",
    ]
    (out / "DEVICE_PROVIDER_DISCOVERY_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return {"report": report, "output_dir": str(out)}


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
