from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ACCEPTED = "accepted"
ACCEPTED_WITH_DEGRADED_COLOUR = "accepted_with_degraded_colour"
RESCAN_REQUIRED = "rescan_required"
REJECTED_FAIL_CLOSED = "rejected_fail_closed"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def checksum_for_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass
class VirtualCartridgeSection:
    section_index: int
    section_payload: dict[str, Any]
    timing_index_lane: dict[str, Any]
    registration_lane: dict[str, Any]
    component_payload_lane: dict[str, Any]
    alpha_object_mask_lane: dict[str, Any]
    colour_registry_lane: dict[str, Any]
    metadata_transform_lane: dict[str, Any]
    hash_checksum_lane: dict[str, Any]
    read_hint: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "section_index": self.section_index,
            "section_payload": self.section_payload,
            "timing_index_lane": self.timing_index_lane,
            "registration_lane": self.registration_lane,
            "component_payload_lane": self.component_payload_lane,
            "alpha_object_mask_lane": self.alpha_object_mask_lane,
            "colour_registry_lane": self.colour_registry_lane,
            "metadata_transform_lane": self.metadata_transform_lane,
            "hash_checksum_lane": self.hash_checksum_lane,
            "read_hint": self.read_hint,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VirtualCartridgeSection":
        return cls(
            section_index=int(data["section_index"]),
            section_payload=dict(data.get("section_payload", {})),
            timing_index_lane=dict(data.get("timing_index_lane", {})),
            registration_lane=dict(data.get("registration_lane", {})),
            component_payload_lane=dict(data.get("component_payload_lane", {})),
            alpha_object_mask_lane=dict(data.get("alpha_object_mask_lane", {})),
            colour_registry_lane=dict(data.get("colour_registry_lane", {})),
            metadata_transform_lane=dict(data.get("metadata_transform_lane", {})),
            hash_checksum_lane=dict(data.get("hash_checksum_lane", {})),
            read_hint=dict(data.get("read_hint", {})),
        )


@dataclass
class VirtualCartridge:
    cartridge_id: str
    sections: list[VirtualCartridgeSection]
    schema_version: str = "amcf-virtual-hardware-v1"
    description: str = "software-only virtual AMCF cartridge"

    @property
    def section_count(self) -> int:
        return len(self.sections)

    def get_section(self, section_index: int) -> VirtualCartridgeSection:
        if section_index < 0 or section_index >= self.section_count:
            raise IndexError(f"section_index out of range: {section_index}")
        return self.sections[section_index]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "cartridge_id": self.cartridge_id,
            "description": self.description,
            "section_count": self.section_count,
            "sections": [section.to_dict() for section in self.sections],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VirtualCartridge":
        return cls(
            cartridge_id=str(data.get("cartridge_id", "virtual-cartridge")),
            sections=[VirtualCartridgeSection.from_dict(item) for item in data.get("sections", [])],
            schema_version=str(data.get("schema_version", "amcf-virtual-hardware-v1")),
            description=str(data.get("description", "software-only virtual AMCF cartridge")),
        )

    @classmethod
    def load(cls, path: str | Path) -> "VirtualCartridge":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


@dataclass
class LaneReadResult:
    section_index: int
    decision: str
    issues: list[str]
    unsafe_acceptance: bool = False
    colour_degraded: bool = False
    component_payload_state: str = "present"

    def to_dict(self) -> dict[str, Any]:
        return {
            "section_index": self.section_index,
            "decision": self.decision,
            "issues": self.issues,
            "unsafe_acceptance": self.unsafe_acceptance,
            "colour_degraded": self.colour_degraded,
            "component_payload_state": self.component_payload_state,
        }


@dataclass
class ReaderEvent:
    reader_id: str
    cartridge_id: str
    section_index: int
    rescan_attempt: int
    lanes: dict[str, Any]
    reader_status: dict[str, Any]
    cartridge_status: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "reader_id": self.reader_id,
            "cartridge_id": self.cartridge_id,
            "section_index": self.section_index,
            "rescan_attempt": self.rescan_attempt,
            "lanes": self.lanes,
            "reader_status": self.reader_status,
            "cartridge_status": self.cartridge_status,
        }


class VirtualReader:
    def __init__(self, reader_id: str = "AMCF-VIRTUAL-READER-001") -> None:
        self.reader_id = reader_id
        self.cartridge: VirtualCartridge | None = None
        self.current_section = 0
        self.rescan_requests = 0

    def insert_cartridge(self, cartridge: VirtualCartridge) -> dict[str, Any]:
        self.cartridge = cartridge
        self.current_section = 0
        self.rescan_requests = 0
        return self.get_cartridge_status()

    def eject_cartridge(self) -> dict[str, Any]:
        previous = self.get_cartridge_status()
        self.cartridge = None
        self.current_section = 0
        self.rescan_requests = 0
        return previous

    def _require_cartridge(self) -> VirtualCartridge:
        if self.cartridge is None:
            raise RuntimeError("no virtual cartridge inserted")
        return self.cartridge

    def seek_section(self, section_index: int) -> dict[str, Any]:
        cartridge = self._require_cartridge()
        cartridge.get_section(section_index)
        self.current_section = section_index
        return self.get_reader_status()

    def advance_section(self) -> dict[str, Any]:
        cartridge = self._require_cartridge()
        self.current_section = min(self.current_section + 1, cartridge.section_count - 1)
        return self.get_reader_status()

    def reverse_section(self) -> dict[str, Any]:
        self._require_cartridge()
        self.current_section = max(self.current_section - 1, 0)
        return self.get_reader_status()

    def read_current_section(self, rescan_attempt: int = 0) -> ReaderEvent:
        cartridge = self._require_cartridge()
        section = cartridge.get_section(self.current_section)
        return ReaderEvent(
            reader_id=self.reader_id,
            cartridge_id=cartridge.cartridge_id,
            section_index=self.current_section,
            rescan_attempt=rescan_attempt,
            lanes=self.read_lanes(section),
            reader_status=self.get_reader_status(),
            cartridge_status=self.get_cartridge_status(),
        )

    def read_lanes(self, section: VirtualCartridgeSection) -> dict[str, Any]:
        data = section.to_dict()
        return {
            "timing_index_lane": data["timing_index_lane"],
            "registration_lane": data["registration_lane"],
            "component_payload_lane": data["component_payload_lane"],
            "alpha_object_mask_lane": data["alpha_object_mask_lane"],
            "colour_registry_lane": data["colour_registry_lane"],
            "metadata_transform_lane": data["metadata_transform_lane"],
            "hash_checksum_lane": data["hash_checksum_lane"],
            "section_payload": data["section_payload"],
            "read_hint": data.get("read_hint", {}),
        }

    def request_rescan(self) -> dict[str, Any]:
        self.rescan_requests += 1
        return {"reader_id": self.reader_id, "section_index": self.current_section, "rescan_requests": self.rescan_requests}

    def get_reader_status(self) -> dict[str, Any]:
        return {
            "reader_id": self.reader_id,
            "cartridge_inserted": self.cartridge is not None,
            "current_section": self.current_section,
            "rescan_requests": self.rescan_requests,
            "mode": "virtual_software_reader",
        }

    def get_cartridge_status(self) -> dict[str, Any]:
        if self.cartridge is None:
            return {"inserted": False, "cartridge_id": None, "section_count": 0}
        return {"inserted": True, "cartridge_id": self.cartridge.cartridge_id, "section_count": self.cartridge.section_count}


class VirtualScanGate:
    def validate(self, event: ReaderEvent | dict[str, Any]) -> LaneReadResult:
        data = event.to_dict() if isinstance(event, ReaderEvent) else event
        lanes = data["lanes"]
        issues: list[str] = []
        section_index = int(data["section_index"])
        rescan_attempt = int(data.get("rescan_attempt", 0))

        timing = lanes["timing_index_lane"]
        registration = lanes["registration_lane"]
        alpha = lanes["alpha_object_mask_lane"]
        colour = lanes["colour_registry_lane"]
        metadata = lanes["metadata_transform_lane"]
        checksum = lanes["hash_checksum_lane"]
        component = lanes["component_payload_lane"]
        read_hint = lanes.get("read_hint", {})

        timing_valid = bool(timing.get("valid")) and bool(timing.get("marker_present"))
        registration_valid = bool(registration.get("valid"))
        alpha_valid = bool(alpha.get("valid"))
        colour_valid = bool(colour.get("valid"))
        colour_degraded = bool(colour.get("degraded"))
        metadata_valid = bool(metadata.get("valid"))
        checksum_valid = bool(checksum.get("valid"))
        transparent = component.get("state") == "transparent_no_op"
        rescan_needed_once = bool(read_hint.get("rescan_needed_once"))

        if not timing_valid:
            issues.append("timing_index_marker_invalid_or_missing")
        if not registration_valid:
            issues.append("registration_invalid")
        if not alpha_valid:
            issues.append("alpha_object_mask_invalid")
        if not colour_valid:
            issues.append("colour_registry_invalid")
        if not metadata_valid:
            issues.append("metadata_transform_invalid")
        if not checksum_valid:
            issues.append("hash_checksum_mismatch")
        if rescan_needed_once and rescan_attempt == 0:
            issues.append("transient_reader_rescan_needed")

        critical_failure = any(issue in issues for issue in {
            "timing_index_marker_invalid_or_missing",
            "registration_invalid",
            "alpha_object_mask_invalid",
            "metadata_transform_invalid",
            "hash_checksum_mismatch",
        })

        if critical_failure:
            decision = RESCAN_REQUIRED if rescan_attempt == 0 else REJECTED_FAIL_CLOSED
        elif rescan_needed_once and rescan_attempt == 0:
            decision = RESCAN_REQUIRED
        elif colour_degraded:
            decision = ACCEPTED_WITH_DEGRADED_COLOUR
        elif not colour_valid:
            decision = RESCAN_REQUIRED if rescan_attempt == 0 else REJECTED_FAIL_CLOSED
        else:
            decision = ACCEPTED

        unsafe = decision in {ACCEPTED, ACCEPTED_WITH_DEGRADED_COLOUR} and critical_failure
        return LaneReadResult(
            section_index=section_index,
            decision=decision,
            issues=issues,
            unsafe_acceptance=unsafe,
            colour_degraded=colour_degraded,
            component_payload_state="transparent_no_op" if transparent else "present",
        )


@dataclass
class PlayerHandoffState:
    reconstructed_playback_status: str = "idle"
    current_section: int | None = None
    accepted_count: int = 0
    rescanned_count: int = 0
    rejected_count: int = 0
    degraded_count: int = 0
    unsafe_acceptance_count: int = 0
    reader_status: dict[str, Any] = field(default_factory=dict)
    cartridge_status: dict[str, Any] = field(default_factory=dict)
    component_payload_list: list[dict[str, Any]] = field(default_factory=list)
    validation_log_entries: list[dict[str, Any]] = field(default_factory=list)

    def apply(self, event: ReaderEvent, result: LaneReadResult) -> None:
        self.current_section = result.section_index
        self.reader_status = event.reader_status
        self.cartridge_status = event.cartridge_status
        if result.decision == ACCEPTED:
            self.accepted_count += 1
            self.reconstructed_playback_status = "playing_reconstructed_amcf"
        elif result.decision == ACCEPTED_WITH_DEGRADED_COLOUR:
            self.accepted_count += 1
            self.degraded_count += 1
            self.reconstructed_playback_status = "playing_with_degraded_colour_flag"
        elif result.decision == RESCAN_REQUIRED:
            self.rescanned_count += 1
            self.reconstructed_playback_status = "rescan_requested"
        elif result.decision == REJECTED_FAIL_CLOSED:
            self.rejected_count += 1
            self.reconstructed_playback_status = "fail_closed_rejection"
        if result.unsafe_acceptance:
            self.unsafe_acceptance_count += 1

        payload = event.lanes.get("section_payload", {})
        self.component_payload_list.append({
            "section_index": result.section_index,
            "component_id": payload.get("component_id"),
            "object_label": payload.get("object_label"),
            "payload_state": payload.get("payload_state"),
            "component_payload_state": result.component_payload_state,
            "alpha_object_mask_status": event.lanes["alpha_object_mask_lane"].get("mask_state"),
            "transform_metadata": event.lanes["metadata_transform_lane"].get("transform"),
            "residual_tile_payload_status": "transparent_no_op" if result.component_payload_state == "transparent_no_op" else "valid",
        })
        self.validation_log_entries.append({
            "section_index": result.section_index,
            "rescan_attempt": event.rescan_attempt,
            "decision": result.decision,
            "issues": ";".join(result.issues),
            "unsafe_acceptance": result.unsafe_acceptance,
        })

    def to_dict(self) -> dict[str, Any]:
        return {
            "reconstructed_playback_status": self.reconstructed_playback_status,
            "current_section": self.current_section,
            "accepted_count": self.accepted_count,
            "rescanned_count": self.rescanned_count,
            "rejected_count": self.rejected_count,
            "degraded_count": self.degraded_count,
            "unsafe_acceptance_count": self.unsafe_acceptance_count,
            "reader_status": self.reader_status,
            "cartridge_status": self.cartridge_status,
            "component_payload_list": self.component_payload_list,
            "validation_log_entries": self.validation_log_entries,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlayerHandoffState":
        return cls(
            reconstructed_playback_status=str(data.get("reconstructed_playback_status", "idle")),
            current_section=data.get("current_section"),
            accepted_count=int(data.get("accepted_count", 0)),
            rescanned_count=int(data.get("rescanned_count", 0)),
            rejected_count=int(data.get("rejected_count", 0)),
            degraded_count=int(data.get("degraded_count", 0)),
            unsafe_acceptance_count=int(data.get("unsafe_acceptance_count", 0)),
            reader_status=dict(data.get("reader_status", {})),
            cartridge_status=dict(data.get("cartridge_status", {})),
            component_payload_list=list(data.get("component_payload_list", [])),
            validation_log_entries=list(data.get("validation_log_entries", [])),
        )


class ReaderAdapter(ABC):
    @abstractmethod
    def read_section(self, section_index: int | None = None) -> ReaderEvent:
        raise NotImplementedError

    @abstractmethod
    def read_lane_data(self, section_index: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def request_rescan(self, section_index: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def fail_closed(self, reason: str) -> dict[str, Any]:
        raise NotImplementedError


class VirtualReaderAdapter(ReaderAdapter):
    def __init__(self, reader: VirtualReader) -> None:
        self.reader = reader

    def read_section(self, section_index: int | None = None) -> ReaderEvent:
        if section_index is not None:
            self.reader.seek_section(section_index)
        return self.reader.read_current_section()

    def read_lane_data(self, section_index: int) -> dict[str, Any]:
        return self.read_section(section_index).lanes

    def get_status(self) -> dict[str, Any]:
        return self.reader.get_reader_status()

    def request_rescan(self, section_index: int) -> dict[str, Any]:
        self.reader.seek_section(section_index)
        return self.reader.request_rescan()

    def fail_closed(self, reason: str) -> dict[str, Any]:
        return {"decision": REJECTED_FAIL_CLOSED, "reason": reason, "unsafe_acceptance": False}


class FuturePhysicalReaderAdapter(ReaderAdapter):
    def read_section(self, section_index: int | None = None) -> ReaderEvent:
        raise NotImplementedError("future physical reader adapter placeholder only")

    def read_lane_data(self, section_index: int) -> dict[str, Any]:
        raise NotImplementedError("future physical reader adapter placeholder only")

    def get_status(self) -> dict[str, Any]:
        return {"adapter": "future_physical_reader", "implemented": False, "placeholder_only": True}

    def request_rescan(self, section_index: int) -> dict[str, Any]:
        raise NotImplementedError("future physical reader adapter placeholder only")

    def fail_closed(self, reason: str) -> dict[str, Any]:
        return {"decision": REJECTED_FAIL_CLOSED, "reason": reason, "unsafe_acceptance": False}


class PlaybackDevice(ABC):
    @abstractmethod
    def load_handoff_state(self, handoff: PlayerHandoffState | dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def play(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def pause(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def seek_section(self, section_index: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def reverse_section(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_playback_status(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_validation_status(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_output_status(self) -> dict[str, Any]:
        raise NotImplementedError


class SoftwarePlaybackDevice(PlaybackDevice):
    def __init__(self, device_id: str = "AMCF-SOFTWARE-PLAYER-001") -> None:
        self.device_id = device_id
        self.handoff = PlayerHandoffState()
        self.playing = False

    def load_handoff_state(self, handoff: PlayerHandoffState | dict[str, Any]) -> dict[str, Any]:
        self.handoff = handoff if isinstance(handoff, PlayerHandoffState) else PlayerHandoffState.from_dict(handoff)
        return self.get_playback_status()

    def play(self) -> dict[str, Any]:
        self.playing = True
        return self.get_playback_status()

    def pause(self) -> dict[str, Any]:
        self.playing = False
        return self.get_playback_status()

    def seek_section(self, section_index: int) -> dict[str, Any]:
        self.handoff.current_section = section_index
        return self.get_playback_status()

    def reverse_section(self) -> dict[str, Any]:
        current = self.handoff.current_section or 0
        self.handoff.current_section = max(0, current - 1)
        return self.get_playback_status()

    def get_playback_status(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "device_type": "software_playback",
            "playing": self.playing,
            "current_section": self.handoff.current_section,
            "reconstructed_playback_status": self.handoff.reconstructed_playback_status,
        }

    def get_validation_status(self) -> dict[str, Any]:
        return {
            "accepted_count": self.handoff.accepted_count,
            "rescanned_count": self.handoff.rescanned_count,
            "rejected_count": self.handoff.rejected_count,
            "degraded_count": self.handoff.degraded_count,
            "unsafe_acceptance_count": self.handoff.unsafe_acceptance_count,
            "fail_closed_enabled": True,
        }

    def get_output_status(self) -> dict[str, Any]:
        return {
            "output_layer": "desktop_software",
            "display_or_hardware_output_required": False,
            "physical_validation_claimed": False,
        }


class FuturePhysicalPlaybackDevice(PlaybackDevice):
    def load_handoff_state(self, handoff: PlayerHandoffState | dict[str, Any]) -> dict[str, Any]:
        return self.get_playback_status()

    def play(self) -> dict[str, Any]:
        return self.get_playback_status()

    def pause(self) -> dict[str, Any]:
        return self.get_playback_status()

    def seek_section(self, section_index: int) -> dict[str, Any]:
        return self.get_playback_status()

    def reverse_section(self) -> dict[str, Any]:
        return self.get_playback_status()

    def get_playback_status(self) -> dict[str, Any]:
        return {"device_type": "future_physical_playback_device", "implemented": False, "placeholder_only": True}

    def get_validation_status(self) -> dict[str, Any]:
        return {"implemented": False, "placeholder_only": True, "hardware_validation_claimed": False}

    def get_output_status(self) -> dict[str, Any]:
        return {"implemented": False, "placeholder_only": True, "physical_output_validated": False}


class ReaderPlayerApplianceAdapter:
    """Placeholder for a future combined cartridge reader + playback appliance."""

    def __init__(self) -> None:
        self.placeholder_only = True

    def get_status(self) -> dict[str, Any]:
        return {
            "adapter": "reader_player_appliance",
            "implemented": False,
            "placeholder_only": True,
            "hardware_validation_claimed": False,
        }

    def fail_closed(self, reason: str) -> dict[str, Any]:
        return {"decision": REJECTED_FAIL_CLOSED, "reason": reason, "unsafe_acceptance": False}


def make_virtual_section(
    section_index: int,
    *,
    component_id: str = "tree-001",
    object_label: str = "tree object",
    transparent: bool = False,
    degraded_colour: bool = False,
    hash_mismatch: bool = False,
    missing_marker: bool = False,
    rescan_needed_once: bool = False,
) -> VirtualCartridgeSection:
    section_payload = {
        "component_id": component_id,
        "object_label": object_label,
        "payload_state": "transparent_no_op" if transparent else "component_payload",
        "bbox": None if transparent else [220, 120, 620, 720],
        "data_ref": None if transparent else f"synthetic://component/{component_id}/section/{section_index}",
    }
    expected = checksum_for_payload(section_payload)
    observed = "mismatch-" + expected[:16] if hash_mismatch else expected
    return VirtualCartridgeSection(
        section_index=section_index,
        section_payload=section_payload,
        timing_index_lane={"section_index": section_index, "marker_present": not missing_marker, "timing_tick": section_index * 1000, "valid": not missing_marker},
        registration_lane={"corner_markers_present": True, "skew_px": 0.0, "valid": True},
        component_payload_lane={"present": not transparent, "state": "transparent_no_op" if transparent else "present", "component_id": None if transparent else component_id, "object_label": None if transparent else object_label},
        alpha_object_mask_lane={"present": not transparent, "mask_state": "transparent_no_op" if transparent else "valid_mask", "valid": True},
        colour_registry_lane={"profile": "AMCF-Rec709-virtual", "degraded": degraded_colour, "delta_e_proxy": 9.5 if degraded_colour else 1.2, "valid": True},
        metadata_transform_lane={"timestamp_ms": section_index * 41.708, "transform": {"x": 0, "y": 0, "scale": 1.0, "rotation": 0.0}, "valid": True},
        hash_checksum_lane={"algorithm": "sha256", "expected": expected, "observed": observed, "valid": expected == observed},
        read_hint={"rescan_needed_once": rescan_needed_once},
    )


def create_sample_virtual_cartridge() -> VirtualCartridge:
    sections = [
        make_virtual_section(0),
        make_virtual_section(1),
        make_virtual_section(2, component_id="noop-002", object_label="transparent no-op", transparent=True),
        make_virtual_section(3, degraded_colour=True),
        make_virtual_section(4, hash_mismatch=True),
        make_virtual_section(5, missing_marker=True),
        make_virtual_section(6, rescan_needed_once=True),
        make_virtual_section(7),
    ]
    return VirtualCartridge("AMCF-VIRTUAL-CART-0001", sections, description="Synthetic virtual AMCF cartridge for reader/player abstraction tests.")


def read_cartridge_to_handoff(cartridge: VirtualCartridge) -> tuple[list[dict[str, Any]], PlayerHandoffState]:
    reader = VirtualReader()
    gate = VirtualScanGate()
    handoff = PlayerHandoffState()
    reader.insert_cartridge(cartridge)
    events: list[dict[str, Any]] = []
    for section_index in range(cartridge.section_count):
        reader.seek_section(section_index)
        event = reader.read_current_section(rescan_attempt=0)
        result = gate.validate(event)
        handoff.apply(event, result)
        events.append({"event": event.to_dict(), "validation": result.to_dict()})
        if result.decision == RESCAN_REQUIRED:
            reader.request_rescan()
            retry = reader.read_current_section(rescan_attempt=1)
            retry_result = gate.validate(retry)
            handoff.apply(retry, retry_result)
            events.append({"event": retry.to_dict(), "validation": retry_result.to_dict()})
    return events, handoff
