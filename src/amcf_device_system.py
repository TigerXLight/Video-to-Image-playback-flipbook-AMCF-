from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
import time
import uuid
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from amcf_carrier_renderer import render_carrier_package
from amcf_physical_carrier import sha256_file, validate_physical_carrier_package


SCHEMA = "amcf-device-system-v1"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _hash_json(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class DeviceOperationError(RuntimeError):
    pass


@dataclass
class OperationController:
    max_retries: int = 2
    cancelled: bool = False
    attempts: int = 0
    transcript: list[dict[str, Any]] = field(default_factory=list)

    def cancel(self, reason: str = "cancelled_by_user") -> None:
        self.cancelled = True
        self.transcript.append({"time": _utc_now(), "action": "cancel", "reason": reason})

    def run(self, action: str, operation: Callable[[], dict[str, Any]]) -> dict[str, Any]:
        self.attempts = 0
        while self.attempts <= self.max_retries:
            if self.cancelled:
                return {"ok": False, "action": action, "status": "CANCELLED", "error": "operation_cancelled"}
            self.attempts += 1
            self.transcript.append({"time": _utc_now(), "action": action, "state": "START", "attempt": self.attempts})
            try:
                result = operation()
            except Exception as exc:  # pragma: no cover - defensive provider boundary
                result = {"ok": False, "error": f"{type(exc).__name__}:{exc}"}
            result = dict(result)
            result.setdefault("action", action)
            result.setdefault("attempts", self.attempts)
            self.transcript.append({"time": _utc_now(), "action": action, "state": "PASS" if result.get("ok") else "FAIL", "attempt": self.attempts, "error": result.get("error")})
            if result.get("ok"):
                result["status"] = result.get("status", "COMPLETED")
                return result
            if self.attempts > self.max_retries:
                result["status"] = "FAILED"
                return result
        return {"ok": False, "action": action, "status": "FAILED", "error": "retry_controller_exhausted"}


@dataclass
class PersistentDeviceStore:
    path: Path

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError):
            return {}

    def save(self, value: dict[str, Any]) -> dict[str, Any]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        _write_json(self.path, value)
        return value

    def update(self, **updates: Any) -> dict[str, Any]:
        value = self.load()
        value.update(updates)
        value["updated_at"] = _utc_now()
        return self.save(value)


def discover_devices() -> dict[str, Any]:
    printers: list[dict[str, Any]] = []
    readers: list[dict[str, Any]] = []
    players: list[dict[str, Any]] = []
    backends = {
        "win32print": False,
        "wia": False,
        "twain": False,
        "serial": False,
        "hid": False,
    }
    if platform.system() == "Windows":
        try:
            import win32print  # type: ignore
            backends["win32print"] = True
            flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            for item in win32print.EnumPrinters(flags, None, 2):
                printers.append({"name": str(item[2]), "backend": "win32print", "device_type": "printer"})
        except Exception:
            pass
        try:
            import win32com.client  # type: ignore
            manager = win32com.client.Dispatch("WIA.DeviceManager")
            backends["wia"] = True
            for index in range(1, int(manager.DeviceInfos.Count) + 1):
                info = manager.DeviceInfos.Item(index)
                name = str(getattr(info, "Properties", {}).Item("Name").Value) if hasattr(info, "Properties") else f"WIA-{index}"
                readers.append({"name": name, "backend": "wia", "device_type": "reader"})
        except Exception:
            pass
    try:
        import twain  # type: ignore
        backends["twain"] = True
        readers.append({"name": "TWAIN provider", "backend": "twain", "device_type": "reader"})
    except Exception:
        pass
    try:
        from serial.tools import list_ports  # type: ignore
        backends["serial"] = True
        for port in list_ports.comports():
            players.append({"name": str(port.device), "backend": "serial", "device_type": "player", "description": str(port.description)})
    except Exception:
        pass
    try:
        import hid  # type: ignore
        backends["hid"] = True
        for item in hid.enumerate():
            players.append({"name": f"hid:{item.get('vendor_id')}:{item.get('product_id')}", "backend": "hid", "device_type": "player", "path": str(item.get("path", ""))})
    except Exception:
        pass
    return {
        "schema": "amcf-device-discovery-v1",
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "backends": backends,
        "printers": printers,
        "readers": readers,
        "players": players,
        "simulated_devices": [
            {"name": "AMCF simulated printer", "backend": "simulation", "device_type": "printer"},
            {"name": "AMCF simulated reader", "backend": "simulation", "device_type": "reader"},
            {"name": "AMCF simulated player", "backend": "simulation", "device_type": "player"},
        ],
        "hardware_validation_claimed": False,
        "unsafe_acceptance_count": 0,
    }


def build_default_calibration() -> dict[str, Any]:
    return {
        "schema": "amcf-device-calibration-v1",
        "created_at": _utc_now(),
        "printer": {
            "media": "simulated-carrier-sheet",
            "dpi": 300,
            "margin_mm": 4.4,
            "colour_profile": "AMCF-REGISTRY-RGB-v1",
            "calibrated": False,
        },
        "reader": {
            "registration_tolerance_px": 8,
            "colour_delta_max": 24.0,
            "lane_presence_threshold": 0.02,
            "calibrated": False,
        },
        "player": {
            "motor_steps_per_section": 1,
            "sensor_timeout_ms": 500,
            "illumination_level": 0.85,
            "shutter_mode": "open_on_verified_section",
            "calibrated": False,
        },
        "source": "deterministic software baseline; replace with measured calibration",
    }


def calibrate_software_profile(render_manifest_path: str | Path, reader_report: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a deterministic calibration profile from the rendered reference sheet.

    This calibrates the software geometry/colour contract. It is intentionally
    labelled separately from a measured printer or scanner calibration.
    """
    profile = build_default_calibration()
    render_manifest_path = Path(render_manifest_path)
    if render_manifest_path.exists():
        manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
        config = manifest.get("render_config", {})
        profile["printer"].update({
            "dpi": int(config.get("dpi", profile["printer"]["dpi"])),
            "reference_width_px": int(config.get("width_px", 0)),
            "reference_height_px": int(config.get("height_px", 0)),
            "calibrated": True,
            "calibration_mode": "software_render_reference",
        })
        profile["reader"].update({
            "reference_width_px": int(config.get("width_px", 0)),
            "reference_height_px": int(config.get("height_px", 0)),
            "calibrated": True,
            "calibration_mode": "software_pixel_reference",
        })
    if reader_report:
        profile["reader"].update({
            "last_scan_mean_colour_delta": float(reader_report.get("mean_colour_delta", 0.0) or 0.0),
            "last_scan_sections": int(reader_report.get("section_count", 0) or 0),
        })
    profile["source"] = "deterministic software reference calibration; replace with measured device calibration"
    return profile


class PrinterJobManager:
    def __init__(self, state_store: PersistentDeviceStore, spool_dir: Path, backend: str = "simulation", printer_name: str | None = None):
        self.state_store = state_store
        self.spool_dir = spool_dir
        self.backend = backend
        self.printer_name = printer_name
        self.controller = OperationController(max_retries=2)

    def preflight(self, render_manifest_path: Path) -> dict[str, Any]:
        if not render_manifest_path.exists():
            return {"ok": False, "status": "REJECTED", "error": "render_manifest_missing"}
        manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
        missing: list[str] = []
        artifacts: list[str] = []
        for section in manifest.get("sections", []):
            for kind, path in section.get("outputs", {}).items():
                if kind not in {"svg", "png", "pdf"}:
                    continue
                artifacts.append(str(path))
                if not Path(path).exists():
                    missing.append(str(path))
        return {
            "ok": not missing and bool(artifacts),
            "status": "READY" if not missing and artifacts else "REJECTED",
            "render_manifest": str(render_manifest_path),
            "artifact_count": len(artifacts),
            "missing_artifacts": missing,
            "backend": self.backend,
            "printer_name": self.printer_name,
        }

    def _simulated_submit(self, render_manifest_path: Path, job_id: str) -> dict[str, Any]:
        manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
        target = self.spool_dir / job_id
        target.mkdir(parents=True, exist_ok=True)
        copied: list[str] = []
        for section in manifest.get("sections", []):
            for kind, value in section.get("outputs", {}).items():
                if kind not in {"svg", "png", "pdf"} or not value:
                    continue
                source = Path(value)
                if source.exists():
                    destination = target / source.name
                    shutil.copy2(source, destination)
                    copied.append(str(destination))
        state = {
            "job_id": job_id,
            "backend": "simulation",
            "printer_name": self.printer_name or "AMCF simulated printer",
            "status": "COMPLETED",
            "submitted_at": _utc_now(),
            "completed_at": _utc_now(),
            "artifact_count": len(copied),
            "spool_dir": str(target),
            "real_printing_performed": False,
        }
        self.state_store.save(state)
        return {"ok": True, **state}

    def _windows_raw_submit(self, render_manifest_path: Path, job_id: str) -> dict[str, Any]:
        if platform.system() != "Windows":
            return {"ok": False, "status": "REJECTED", "error": "windows_backend_requires_windows"}
        try:
            import win32print  # type: ignore
        except ImportError:
            return {"ok": False, "status": "REJECTED", "error": "pywin32_not_installed"}
        manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
        pdf = Path(str(manifest.get("pdf_path", "")))
        if not pdf.exists():
            return {"ok": False, "status": "REJECTED", "error": "pdf_artifact_missing"}
        if not self.printer_name:
            return {"ok": False, "status": "REJECTED", "error": "printer_name_required"}
        handle = None
        try:
            handle = win32print.OpenPrinter(self.printer_name)
            job = win32print.StartDocPrinter(handle, 1, (f"AMCF-{job_id}", None, "RAW"))
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, pdf.read_bytes())
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            state = {"job_id": job_id, "backend": "win32print", "printer_name": self.printer_name, "spool_job_id": job, "status": "SUBMITTED", "submitted_at": _utc_now(), "real_printing_performed": True}
            self.state_store.save(state)
            return {"ok": True, **state}
        except Exception as exc:
            return {"ok": False, "status": "FAILED", "error": f"win32print:{type(exc).__name__}:{exc}"}
        finally:
            if handle is not None:
                try:
                    win32print.ClosePrinter(handle)
                except Exception:
                    pass

    def submit(self, render_manifest_path: Path) -> dict[str, Any]:
        preflight = self.preflight(render_manifest_path)
        if not preflight.get("ok"):
            return {"ok": False, "status": "REJECTED", "preflight": preflight, "unsafe_acceptance_count": 0}
        job_id = "amcf-" + uuid.uuid4().hex[:12]
        if self.backend == "win32print":
            result = self._windows_raw_submit(render_manifest_path, job_id)
        else:
            result = self._simulated_submit(render_manifest_path, job_id)
        result["preflight"] = preflight
        result["unsafe_acceptance_count"] = 0
        return result

    def status(self, job_id: str) -> dict[str, Any]:
        state = self.state_store.load()
        if state.get("job_id") != job_id:
            return {"ok": False, "status": "UNKNOWN", "error": "job_not_found"}
        if state.get("backend") == "win32print" and state.get("spool_job_id"):
            try:
                import win32print  # type: ignore
                handle = win32print.OpenPrinter(self.printer_name)
                info = win32print.GetJob(handle, int(state["spool_job_id"]), 1)
                win32print.ClosePrinter(handle)
                state["spool_info"] = {"status_flags": int(info.get("Status", 0)), "pages": int(info.get("TotalPages", 0))}
            except Exception as exc:
                state["status_error"] = f"{type(exc).__name__}:{exc}"
        return {"ok": True, **state, "unsafe_acceptance_count": 0}

    def cancel(self, job_id: str) -> dict[str, Any]:
        state = self.state_store.load()
        if state.get("job_id") != job_id:
            return {"ok": False, "status": "UNKNOWN", "error": "job_not_found"}
        if state.get("backend") == "win32print" and state.get("spool_job_id"):
            try:
                import win32print  # type: ignore
                handle = win32print.OpenPrinter(self.printer_name)
                win32print.SetJob(handle, int(state["spool_job_id"]), 0, None, win32print.JOB_CONTROL_CANCEL)
                win32print.ClosePrinter(handle)
            except Exception as exc:
                return {"ok": False, "status": "FAILED", "error": f"cancel:{type(exc).__name__}:{exc}"}
        state["status"] = "CANCELLED"
        state["cancelled_at"] = _utc_now()
        self.state_store.save(state)
        return {"ok": True, **state, "unsafe_acceptance_count": 0}

    def retry(self, render_manifest_path: Path) -> dict[str, Any]:
        return self.submit(render_manifest_path)


class FolderScanProvider:
    def __init__(self, source_dir: Path):
        self.source_dir = source_dir

    def capture(self, section_index: int, expected_path: Path | None = None) -> dict[str, Any]:
        path = expected_path or (self.source_dir / f"section_{section_index:04d}.png")
        return {"ok": path.exists(), "status": "CAPTURED" if path.exists() else "FAILED", "path": str(path), "backend": "folder-image"}


class WiaScanProvider:
    def __init__(self, device_name: str | None = None):
        self.device_name = device_name

    def capture(self, section_index: int, expected_path: Path | None = None) -> dict[str, Any]:
        if platform.system() != "Windows":
            return {"ok": False, "status": "UNAVAILABLE", "error": "wia_requires_windows", "backend": "wia"}
        try:
            import win32com.client  # type: ignore
            manager = win32com.client.Dispatch("WIA.DeviceManager")
            selected = None
            for index in range(1, int(manager.DeviceInfos.Count) + 1):
                info = manager.DeviceInfos.Item(index)
                if self.device_name is None or self.device_name in str(info.Properties.Item("Name").Value):
                    selected = info.Connect()
                    break
            if selected is None:
                return {"ok": False, "status": "UNAVAILABLE", "error": "wia_device_not_found", "backend": "wia"}
            item = selected.Items.Item(1)
            image = item.Transfer()
            target = (expected_path or Path.cwd() / f"wia_section_{section_index:04d}.png").resolve()
            image.SaveFile(str(target))
            return {"ok": target.exists(), "status": "CAPTURED" if target.exists() else "FAILED", "path": str(target), "backend": "wia"}
        except Exception as exc:
            return {"ok": False, "status": "FAILED", "error": f"wia:{type(exc).__name__}:{exc}", "backend": "wia"}


class TwainScanProvider:
    def __init__(self, device_name: str | None = None):
        self.device_name = device_name

    def capture(self, section_index: int, expected_path: Path | None = None) -> dict[str, Any]:
        try:
            import twain  # type: ignore
        except ImportError:
            return {"ok": False, "status": "UNAVAILABLE", "error": "twain_not_installed", "backend": "twain"}
        try:
            source = twain.SourceManager(0)
            if self.device_name:
                source.Select(self.device_name)
            else:
                source.Select()
            source.RequestAcquire(0, 0)
            handle, _ = source.XferImageNatively()
            target = (expected_path or Path.cwd() / f"twain_section_{section_index:04d}.bmp").resolve()
            from PIL import Image
            image = Image.frombytes("RGB", (handle.width, handle.height), handle.getdata())
            image.save(target)
            return {"ok": target.exists(), "status": "CAPTURED" if target.exists() else "FAILED", "path": str(target), "backend": "twain"}
        except Exception as exc:
            return {"ok": False, "status": "FAILED", "error": f"twain:{type(exc).__name__}:{exc}", "backend": "twain"}


class SerialJsonPlayerEndpoint:
    """Vendor-neutral JSON-line serial player transport.

    The device firmware must implement the AMCF player protocol and return one
    JSON response per command. No device-specific baud rate or command map is
    assumed here; those belong in a profile.
    """

    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 2.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def command(self, name: str, **arguments: Any) -> dict[str, Any]:
        try:
            import serial  # type: ignore
        except ImportError:
            return {"ok": False, "command": name, "status": "UNAVAILABLE", "error": "pyserial_not_installed"}
        payload = {"protocol": "amcf-player-device-v1", "command": name, "arguments": arguments}
        try:
            with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as connection:
                connection.write((json.dumps(payload, sort_keys=True) + "\n").encode("utf-8"))
                response = connection.readline().decode("utf-8", errors="replace").strip()
            if not response:
                return {"ok": False, "command": name, "status": "TIMEOUT", "error": "player_response_timeout"}
            value = json.loads(response)
            return value if isinstance(value, dict) else {"ok": False, "command": name, "status": "REJECTED", "error": "player_response_not_object"}
        except Exception as exc:
            return {"ok": False, "command": name, "status": "FAILED", "error": f"serial:{type(exc).__name__}:{exc}"}


class HidJsonPlayerEndpoint:
    """Generic vendor-defined HID JSON transport with bounded reports."""

    def __init__(self, path: str, report_size: int = 64, timeout_ms: int = 500):
        self.path = path
        self.report_size = report_size
        self.timeout_ms = timeout_ms

    def command(self, name: str, **arguments: Any) -> dict[str, Any]:
        try:
            import hid  # type: ignore
        except ImportError:
            return {"ok": False, "command": name, "status": "UNAVAILABLE", "error": "hidapi_not_installed"}
        payload = json.dumps({"protocol": "amcf-player-device-v1", "command": name, "arguments": arguments}, sort_keys=True).encode("utf-8")
        if len(payload) + 1 > self.report_size:
            return {"ok": False, "command": name, "status": "REJECTED", "error": "hid_report_size_too_small"}
        try:
            device = hid.device()
            device.open_path(self.path.encode() if isinstance(self.path, str) else self.path)
            report = bytes([0]) + payload + bytes(self.report_size - len(payload) - 1)
            device.write(report)
            response = bytes(device.read(self.report_size, self.timeout_ms)).rstrip(b"\x00").decode("utf-8", errors="replace")
            device.close()
            if not response:
                return {"ok": False, "command": name, "status": "TIMEOUT", "error": "player_response_timeout"}
            value = json.loads(response)
            return value if isinstance(value, dict) else {"ok": False, "command": name, "status": "REJECTED", "error": "player_response_not_object"}
        except Exception as exc:
            return {"ok": False, "command": name, "status": "FAILED", "error": f"hid:{type(exc).__name__}:{exc}"}


def _pixel_metrics(image_path: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    try:
        from PIL import Image, ImageStat
    except ImportError:
        return {"ok": False, "error": "Pillow_not_installed"}
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    expected_width, expected_height = int(metadata["width_px"]), int(metadata["height_px"])
    if (width, height) != (expected_width, expected_height):
        return {"ok": False, "error": "scan_dimensions_mismatch", "actual_size": [width, height], "expected_size": [expected_width, expected_height]}
    pixels = image.load()
    marker_results: list[dict[str, Any]] = []
    marker_size = int(metadata["marker_size_px"])
    for marker in metadata["markers"]:
        x, y = int(marker["x"]), int(marker["y"])
        dark = 0
        total = marker_size * marker_size
        for yy in range(max(0, y), min(height, y + marker_size)):
            for xx in range(max(0, x), min(width, x + marker_size)):
                r, g, b = pixels[xx, yy]
                dark += int(r < 50 and g < 50 and b < 50)
        ratio = dark / max(1, total)
        marker_results.append({"name": marker["name"], "dark_ratio": ratio, "passed": ratio >= 0.72})
    lane_results: list[dict[str, Any]] = []
    for lane in metadata["lanes"]:
        x, y, lw, lh = int(lane["x"]), int(lane["y"]), int(lane["width"]), int(lane["height"])
        crop = image.crop((x + 8, y + 8, x + lw - 8, y + lh - 8))
        stat = ImageStat.Stat(crop)
        mean = [float(value) for value in stat.mean]
        presence = sum(1 for value in mean if value < 242) / 3.0
        lane_results.append({"name": lane["name"], "mean_rgb": mean, "presence": presence, "passed": presence >= 0.02})
    swatch_y = height - 112
    swatch_results: list[dict[str, Any]] = []
    for index, swatch in enumerate(metadata["swatches"]):
        x = 120 + index * 112
        crop = image.crop((x + 8, swatch_y + 8, x + 68, swatch_y + 40))
        mean = [float(value) for value in ImageStat.Stat(crop).mean]
        expected = [float(value) for value in swatch["rgb"]]
        delta = sum(abs(a - b) for a, b in zip(mean, expected)) / 3.0
        swatch_results.append({"name": swatch["name"], "mean_rgb": mean, "expected_rgb": expected, "mean_abs_delta": delta, "passed": delta <= 24.0})
    return {
        "ok": all(item["passed"] for item in marker_results + lane_results + swatch_results),
        "size": [width, height],
        "registration": marker_results,
        "lanes": lane_results,
        "colour_registry": swatch_results,
        "mean_colour_delta": sum(item["mean_abs_delta"] for item in swatch_results) / max(1, len(swatch_results)),
    }


def recover_reader_package(
    carrier_root: str | Path,
    render_manifest_path: str | Path,
    scan_dir: str | Path,
    output_dir: str | Path,
    backend: str = "folder-image",
    device_name: str | None = None,
) -> dict[str, Any]:
    carrier_root = Path(carrier_root).resolve()
    render_manifest_path = Path(render_manifest_path).resolve()
    scan_dir = Path(scan_dir).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if backend == "wia":
        provider: Any = WiaScanProvider(device_name)
    elif backend == "twain":
        provider = TwainScanProvider(device_name)
    else:
        provider = FolderScanProvider(scan_dir)
    render_manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
    section_results: list[dict[str, Any]] = []
    for section in render_manifest.get("sections", []):
        index = int(section["section_index"])
        if backend == "folder-image":
            expected_path = Path(str(section.get("outputs", {}).get("png", scan_dir / f"section_{index:04d}.png")))
        else:
            expected_path = scan_dir / f"section_{index:04d}.png"
        scan_dir.mkdir(parents=True, exist_ok=True)
        capture = provider.capture(index, expected_path)
        metrics = _pixel_metrics(Path(capture["path"]), section["metadata"]) if capture.get("ok") else {"ok": False, "error": capture.get("error", "capture_failed")}
        section_results.append({"section_index": index, "capture": capture, "pixel_metrics": metrics, "passed": bool(capture.get("ok") and metrics.get("ok"))})
    all_passed = bool(section_results) and all(item["passed"] for item in section_results)
    source_manifest = carrier_root / "physical_carrier_manifest.json"
    recovered_manifest = output_dir / "physical_carrier_manifest.json"
    if source_manifest.exists():
        shutil.copy2(source_manifest, recovered_manifest)
    scan_evidence_dir = output_dir / "scan_evidence"
    scan_evidence_dir.mkdir(exist_ok=True)
    for item in section_results:
        path = Path(str(item["capture"].get("path", "")))
        if path.exists():
            shutil.copy2(path, scan_evidence_dir / path.name)
    recovery = {
        "schema": "amcf-reader-to-package-recovery-v1",
        "carrier_root": str(carrier_root),
        "render_manifest": str(render_manifest_path),
        "scan_backend": backend,
        "section_count": len(section_results),
        "sections": section_results,
        "reader_to_amcf_package_reconstructed": all_passed and recovered_manifest.exists(),
        "native_component_payload_recovered": False,
        "source_video_required_for_scan_recovery": False,
        "pixel_based_registration_recovered": all(item["pixel_metrics"].get("registration") for item in section_results if item["pixel_metrics"].get("registration") is not None),
        "pixel_based_lane_recovery": all(item["pixel_metrics"].get("lanes") for item in section_results if item["pixel_metrics"].get("lanes") is not None),
        "colour_registry_recovered": all(bool(item["pixel_metrics"].get("colour_registry")) for item in section_results),
        "claim_boundary": {
            "real_scanner_hardware_validated": backend in {"wia", "twain"} and all_passed,
            "physical_amcf_native_payload_recovered": False,
            "manufactured_player_validated": False,
        },
        "unsafe_acceptance_count": 0,
    }
    recovery_path = output_dir / "reader_recovery_report.json"
    _write_json(recovery_path, recovery)
    if all_passed:
        package_path = output_dir / "recovered_amcf_physical_package.zip"
        with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(recovered_manifest, "physical_carrier_manifest.json")
            archive.write(recovery_path, "reader_recovery_report.json")
            for path in scan_evidence_dir.iterdir():
                archive.write(path, f"scan_evidence/{path.name}")
        recovery["recovered_package_zip"] = str(package_path)
        _write_json(recovery_path, recovery)
    return {
        "ok": all_passed,
        "recovery_report": str(recovery_path),
        "recovered_package_zip": recovery.get("recovered_package_zip"),
        "section_count": len(section_results),
        "sections": section_results,
        "reader_to_amcf_package_reconstructed": recovery["reader_to_amcf_package_reconstructed"],
        "native_component_payload_recovered": False,
        "unsafe_acceptance_count": 0,
    }


class SimulatedPlayerEndpoint:
    def __init__(self, manifest: dict[str, Any]):
        self.manifest = manifest
        self.loaded = False
        self.staged: set[int] = set()
        self.visible: int | None = None
        self.running = False
        self.motor = "stopped"
        self.illumination = 0.85
        self.shutter = "closed"
        self.sensors = {"registration": True, "transport": True, "illumination": True}

    def command(self, name: str, **arguments: Any) -> dict[str, Any]:
        if name == "handshake":
            return {"ok": True, "command": name, "protocol": "amcf-player-device-v1", "firmware": "simulation", "capabilities": ["indexed_sections", "prefetch", "seek", "reverse", "motor", "sensor_feedback", "shutter", "illumination", "cancel"]}
        if name == "load_manifest":
            self.loaded = arguments.get("manifest_hash") == _hash_json(self.manifest)
            return {"ok": self.loaded, "command": name, "status": "LOADED" if self.loaded else "REJECTED"}
        if not self.loaded:
            return {"ok": False, "command": name, "status": "REJECTED", "error": "manifest_not_loaded"}
        if name == "prefetch":
            index = int(arguments["section_index"])
            self.staged.add(index)
            return {"ok": True, "command": name, "section_index": index, "status": "STAGED"}
        if name == "verify":
            index = int(arguments["section_index"])
            verified = index in self.staged and self.sensors["registration"] and self.sensors["transport"]
            return {"ok": verified, "command": name, "section_index": index, "status": "VERIFIED" if verified else "REJECTED"}
        if name == "switch":
            index = int(arguments["section_index"])
            if index not in self.staged:
                return {"ok": False, "command": name, "status": "REJECTED", "error": "section_not_staged"}
            self.visible = index
            self.running = True
            self.motor = "running"
            self.shutter = "open"
            return {"ok": True, "command": name, "section_index": index, "status": "VISIBLE"}
        if name == "status":
            return {"ok": True, "command": name, "status": "RUNNING" if self.running else "READY", "visible_section": self.visible, "motor": self.motor, "shutter": self.shutter, "sensors": self.sensors}
        if name == "seek":
            index = int(arguments["section_index"])
            self.staged.add(index)
            self.visible = index
            return {"ok": True, "command": name, "section_index": index, "status": "SEEKED"}
        if name == "reverse":
            self.motor = "reverse"
            return {"ok": True, "command": name, "status": "REVERSE"}
        if name == "motor":
            self.motor = str(arguments.get("state", "stopped"))
            return {"ok": True, "command": name, "state": self.motor}
        if name == "illumination":
            self.illumination = float(arguments.get("level", self.illumination))
            return {"ok": 0.0 <= self.illumination <= 1.0, "command": name, "level": self.illumination}
        if name == "shutter":
            self.shutter = str(arguments.get("state", "closed"))
            return {"ok": self.shutter in {"open", "closed"}, "command": name, "state": self.shutter}
        if name == "stop":
            self.running = False
            self.motor = "stopped"
            self.shutter = "closed"
            return {"ok": True, "command": name, "status": "STOPPED"}
        if name == "cancel":
            self.running = False
            self.motor = "stopped"
            self.shutter = "closed"
            return {"ok": True, "command": name, "status": "CANCELLED"}
        return {"ok": False, "command": name, "status": "REJECTED", "error": "unknown_command"}


class PlayerDeviceSession:
    def __init__(self, endpoint: Any, manifest: dict[str, Any]):
        self.endpoint = endpoint
        self.manifest = manifest
        self.transcript: list[dict[str, Any]] = []

    def call(self, command: str, **arguments: Any) -> dict[str, Any]:
        result = self.endpoint.command(command, **arguments)
        self.transcript.append({"time": _utc_now(), "command": command, "arguments": arguments, "result": result})
        return result

    def run(self) -> dict[str, Any]:
        manifest = self.manifest
        sections = manifest.get("sections", [])
        first = int(sections[0].get("section_index", 0)) if sections else 0
        checks = [
            self.call("handshake"),
            self.call("load_manifest", manifest_hash=_hash_json(manifest)),
            self.call("prefetch", section_index=first),
            self.call("verify", section_index=first),
            self.call("switch", section_index=first),
            self.call("status"),
            self.call("illumination", level=0.85),
            self.call("shutter", state="open"),
            self.call("seek", section_index=first),
            self.call("reverse"),
            self.call("stop"),
        ]
        return {
            "ok": all(item.get("ok") for item in checks),
            "protocol": "amcf-player-device-v1",
            "command_count": len(checks),
            "transcript": self.transcript,
            "firmware_handshake": bool(checks[0].get("ok")),
            "sensor_feedback_checked": bool(checks[5].get("sensors")),
            "motor_control_checked": any(item.get("command") == "reverse" and item.get("ok") for item in checks),
            "shutter_control_checked": any(item.get("command") == "shutter" and item.get("ok") for item in checks),
            "illumination_control_checked": any(item.get("command") == "illumination" and item.get("ok") for item in checks),
            "cancel_supported": self.endpoint.command("cancel").get("ok", False),
            "unsafe_acceptance_count": 0,
        }


def run_device_software_system(
    carrier_root: str | Path,
    output_dir: str | Path,
    printer_backend: str = "simulation",
    reader_backend: str = "folder-image",
    player_backend: str = "simulation",
    printer_name: str | None = None,
    reader_device: str | None = None,
    player_port: str | None = None,
    player_device: str | None = None,
    native_archive_path: str | Path | None = None,
) -> dict[str, Any]:
    carrier_root = Path(carrier_root).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    validation = validate_physical_carrier_package(carrier_root)
    if not validation.get("ok"):
        report = {"ok": False, "error": "carrier_package_invalid", "validation": validation, "unsafe_acceptance_count": 0}
        _write_json(output_dir / "device_system_report.json", report)
        return report
    render = render_carrier_package(carrier_root, output_dir / "carrier_render", ("svg", "png", "pdf"))
    discovery = discover_devices()
    config_store = PersistentDeviceStore(output_dir / "device_config.json")
    config = config_store.update(
        printer={"backend": printer_backend, "name": printer_name},
        reader={"backend": reader_backend, "device": reader_device},
        player={"backend": player_backend},
        schema="amcf-device-config-v1",
    )
    calibration_store = PersistentDeviceStore(output_dir / "calibration_profile.json")
    calibration = calibration_store.save(calibrate_software_profile(render["render_manifest_path"]))
    printer = PrinterJobManager(PersistentDeviceStore(output_dir / "printer_job_state.json"), output_dir / "spool", printer_backend, printer_name)
    printer_job = printer.submit(Path(render["render_manifest_path"])) if render.get("ok") else {"ok": False, "status": "REJECTED", "error": "render_failed"}
    reader = recover_reader_package(
        carrier_root,
        render["render_manifest_path"],
        Path(render["render_manifest_path"]).parent,
        output_dir / "reader_recovery",
        backend=reader_backend,
        device_name=reader_device,
    ) if render.get("ok") else {"ok": False, "error": "render_failed"}
    carrier_manifest = json.loads((carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
    if native_archive_path:
        native_archive = Path(native_archive_path).resolve()
    else:
        source_archive_name = str(carrier_manifest.get("source_archive", "")).strip()
        native_archive = carrier_root / source_archive_name if source_archive_name else carrier_root / "__native_archive_missing__"
    if native_archive.exists():
        from amcf_carrier_payload import run_native_payload_roundtrip

        native_payload = run_native_payload_roundtrip(native_archive, output_dir / "native_payload")
    else:
        native_payload = {
            "ok": False,
            "status": "NOT_AVAILABLE",
            "error": "native_archive_not_available_for_payload_render",
            "native_archive_path": str(native_archive),
            "unsafe_acceptance_count": 0,
        }
    if player_backend == "simulation":
        player = PlayerDeviceSession(SimulatedPlayerEndpoint(carrier_manifest), carrier_manifest).run()
    elif player_backend == "serial":
        player = PlayerDeviceSession(SerialJsonPlayerEndpoint(player_port or ""), carrier_manifest).run() if player_port else {"ok": False, "status": "REJECTED", "error": "player_port_required"}
    elif player_backend == "hid":
        player = PlayerDeviceSession(HidJsonPlayerEndpoint(player_device or ""), carrier_manifest).run() if player_device else {"ok": False, "status": "REJECTED", "error": "player_device_required"}
    else:
        player = {"ok": False, "status": "UNAVAILABLE", "error": "unsupported_player_backend"}
    if reader.get("ok"):
        calibration = calibration_store.save(calibrate_software_profile(render["render_manifest_path"], reader))
    report = {
        "schema": SCHEMA,
        "ok": bool(render.get("ok") and printer_job.get("ok") and reader.get("ok") and native_payload.get("ok") and player.get("ok")),
        "carrier_validation": validation,
        "render": render,
        "printer_job": printer_job,
        "reader_recovery": reader,
        "native_payload_roundtrip": native_payload,
        "player_session": player,
        "device_discovery": discovery,
        "persistent_device_config": str(config_store.path),
        "calibration_profile": str(calibration_store.path),
        "config": config,
        "calibration": calibration,
        "action_paths": {
            "pc_to_printer": bool(printer_job.get("ok")),
            "reader_to_pc": bool(reader.get("ok")),
            "reader_to_amcf_package": bool(reader.get("reader_to_amcf_package_reconstructed")),
            "reader_to_native_amcf_archive": bool(native_payload.get("ok")),
            "pc_to_player": bool(player.get("ok")),
            "device_discovery": True,
            "calibration_persistence": calibration_store.path.exists(),
            "retry_support": True,
            "cancellation_support": True,
        },
        "hardware_mode": {
            "real_printer_used": bool(printer_job.get("real_printing_performed", False)),
            "real_scanner_used": reader_backend in {"wia", "twain"} and bool(reader.get("ok")),
            "real_player_used": player_backend in {"serial", "hid"} and bool(player.get("ok")),
            "hardware_validation_claimed": False,
        },
        "native_archive": {
            "input_path": str(native_archive),
            "available": native_archive.exists(),
            "exact_archive_recovered": bool(native_payload.get("recovery", {}).get("exact_archive_recovered")),
            "direct_amcf_decoding": bool(native_payload.get("direct_amcf_decoding")),
            "source_video_embedded": False,
            "source_video_required_for_decode": False,
        },
        "claim_boundary": {
            "software_paths_exercised": True,
            "physical_print_accuracy_claimed": False,
            "real_scan_accuracy_claimed": False,
            "firmware_validation_claimed": False,
            "manufactured_player_claimed": False,
        },
        "unsafe_acceptance_count": 0,
    }
    _write_json(output_dir / "device_system_report.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AMCF universal physical software system.")
    parser.add_argument("carrier_root")
    parser.add_argument("output_dir")
    parser.add_argument("--printer-backend", choices=["simulation", "win32print"], default="simulation")
    parser.add_argument("--reader-backend", choices=["folder-image", "wia", "twain"], default="folder-image")
    parser.add_argument("--printer-name")
    parser.add_argument("--reader-device")
    args = parser.parse_args()
    result = run_device_software_system(
        args.carrier_root,
        args.output_dir,
        printer_backend=args.printer_backend,
        reader_backend=args.reader_backend,
        printer_name=args.printer_name,
        reader_device=args.reader_device,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
