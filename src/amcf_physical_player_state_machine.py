from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any


STATE_NO_CARTRIDGE = "no_cartridge"
STATE_CARTRIDGE_INSERTED = "cartridge_inserted"
STATE_MANIFEST_RECOGNIZED = "manifest_recognized"
STATE_PREFETCH_CURRENT = "prefetch_current"
STATE_VERIFY_CURRENT = "verify_current"
STATE_LOAD_VIEW_GATE = "load_view_gate"
STATE_VIEW_GATE_LOCKED = "view_gate_locked"
STATE_PLAYBACK_READY = "playback_ready"
STATE_PREFETCH_NEXT = "prefetch_next"
STATE_VERIFY_NEXT = "verify_next"
STATE_STAGE_NEXT = "stage_next"
STATE_WAIT_UPDATE_TIMESTAMP = "wait_update_timestamp"
STATE_TRANSITION_BLANK = "transition_blank"
STATE_SWITCH_VISIBLE_SECTION = "switch_visible_section"
STATE_PARK_OLD_SECTION = "park_old_section"
STATE_PAUSED_SAFE = "paused_safe"
STATE_RESCAN_REQUIRED = "rescan_required"
STATE_RETRY_ALLOWED = "retry_allowed"
STATE_FAIL_CLOSED = "fail_closed"
STATE_MECHANICAL_STOP = "mechanical_stop"
STATE_PLAYBACK_COMPLETE = "playback_complete"

FAIL_CLOSED_UNVERIFIED_SECTION = "fail_closed_unverified_section"
FAIL_CLOSED_WRONG_SECTION = "fail_closed_wrong_section"
FAIL_CLOSED_HASH_MISMATCH = "fail_closed_hash_mismatch"
FAIL_CLOSED_REGISTRATION_FAILURE = "fail_closed_registration_failure"
FAIL_CLOSED_GATE_UNLOCKED = "fail_closed_gate_unlocked"
FAIL_CLOSED_PREFETCH_TIMEOUT = "fail_closed_prefetch_timeout"
FAIL_CLOSED_SHUTTER_FAILURE = "fail_closed_shutter_failure"
FAIL_CLOSED_ILLUMINATION_FAILURE = "fail_closed_illumination_failure"
FAIL_CLOSED_JAM = "fail_closed_jam"
FAIL_CLOSED_MANIFEST_MISMATCH = "fail_closed_manifest_mismatch"
FAIL_CLOSED_UNSUPPORTED_CARRIER = "fail_closed_unsupported_carrier"
FAIL_CLOSED_AUDIO_SYNC_LIMIT = "fail_closed_audio_sync_limit"


@dataclass
class PlayerProfile:
    profile_id: str = "amcf_software_control_player_profile_v1"
    claim_status: str = "software_control_simulator_not_physical_validation"
    hardware_validation_claimed: bool = False
    manufactured_hardware_claimed: bool = False
    visible_image_path: str = "physical_optical"


@dataclass
class MechanismProfile:
    carrier_layout: str = "folded_indexed_carrier"
    staging_model: str = "abstract_ab_staging"
    actuator_family: str = "motor_encoder"
    gate_model: str = "single_visible_gate_plus_hidden_staging"
    prefetch_model: str = "reader_prefetch_ahead"
    reverse_model: str = "limited_reverse_buffer"
    claim_status: str = "software_control_simulator_not_physical_validation"


@dataclass
class PhysicalPlayerSection:
    section_id: str
    update_timestamp_ms: int
    playback_required: bool = True
    timing_index_read: bool = True
    registration_read: bool = True
    metadata_read: bool = True
    hash_read: bool = True
    hash_ok: bool = True
    registration_ok: bool = True
    colour_ok: bool = True
    display_allowed_hint: bool = True


@dataclass
class PhysicalPlayerCartridge:
    cartridge_id: str
    manifest_id: str
    recognized: bool = True
    manifest_matched: bool = True
    carrier_supported: bool = True
    sections: list[PhysicalPlayerSection] = field(default_factory=list)

    def playback_sections(self) -> list[PhysicalPlayerSection]:
        return [section for section in self.sections if section.playback_required]

    def get_section(self, section_id: str | None) -> PhysicalPlayerSection | None:
        if section_id is None:
            return None
        for section in self.sections:
            if section.section_id == section_id:
                return section
        return None


@dataclass
class VerificationState:
    section_id: str | None = None
    display_allowed: bool = False
    decision: str = "not_started"
    reason: str = ""
    warnings: list[str] = field(default_factory=list)
    lanes_read: dict[str, bool] = field(default_factory=dict)


@dataclass
class GateState:
    section_id: str | None = None
    state: str = "empty"
    locked: bool = False
    aligned: bool = False
    illumination_allowed: bool = False
    ready_for_switch: bool = False
    visible: bool = False


@dataclass
class ABGateState:
    visible_section_id: str | None = None
    hidden_section_id: str | None = None
    blanking_active: bool = False
    old_section_id: str | None = None


@dataclass
class ReaderPrefetchState:
    expected_section_id: str | None = None
    prefetched_section_id: str | None = None
    lanes_read: dict[str, bool] = field(default_factory=dict)
    queue: list[str] = field(default_factory=list)


@dataclass
class ReverseBufferState:
    enabled: bool = True
    depth: int = 3
    section_ids: list[str] = field(default_factory=list)


@dataclass
class SeekRequestState:
    requested_timestamp_ms: int | None = None
    requested_section_id: str | None = None
    seek_available: bool = False
    denial_reason: str = ""


@dataclass
class AudioSyncState:
    state: str = "not_started"
    drift_ms: int = 0
    within_limit: bool = True


@dataclass
class SafetyState:
    state: str = "safe_idle"
    playback_allowed: bool = False
    display_allowed: bool = False
    motion_allowed: bool = False
    transition_allowed: bool = False


@dataclass
class FailClosedDecision:
    timestamp_ms: int
    reason: str
    recommended_action: str
    current_section_id: str | None
    next_section_id: str | None
    unsafe_acceptance_count: int = 0


def _to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, list):
        return [_to_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_plain(item) for key, item in value.items()}
    return value


def build_sample_cartridge(kind: str = "valid") -> PhysicalPlayerCartridge:
    sections = [
        PhysicalPlayerSection("section_000", 0),
        PhysicalPlayerSection("section_001", 120),
        PhysicalPlayerSection("section_002", 260),
        PhysicalPlayerSection("section_003_degraded_colour", 420, colour_ok=False),
    ]
    if kind == "hash_mismatch":
        sections[1].hash_ok = False
    if kind == "registration_failure":
        sections[1].registration_ok = False
    return PhysicalPlayerCartridge(
        cartridge_id=f"demo_cartridge_{kind}",
        manifest_id="demo_manifest_state_machine_v1",
        recognized=kind != "unrecognized",
        manifest_matched=kind != "manifest_mismatch",
        carrier_supported=kind != "unsupported_carrier",
        sections=sections,
    )


def verify_physical_section(section: PhysicalPlayerSection | None) -> VerificationState:
    if section is None:
        return VerificationState(display_allowed=False, decision="rejected_fail_closed", reason=FAIL_CLOSED_WRONG_SECTION)
    lanes_read = {
        "timing_index": section.timing_index_read,
        "registration": section.registration_read,
        "metadata": section.metadata_read,
        "hash": section.hash_read,
    }
    if not all(lanes_read.values()):
        return VerificationState(
            section_id=section.section_id,
            display_allowed=False,
            decision="rescan_required",
            reason="required_lane_not_read",
            lanes_read=lanes_read,
        )
    if not section.hash_ok:
        return VerificationState(
            section_id=section.section_id,
            display_allowed=False,
            decision="rejected_fail_closed",
            reason=FAIL_CLOSED_HASH_MISMATCH,
            lanes_read=lanes_read,
        )
    if not section.registration_ok:
        return VerificationState(
            section_id=section.section_id,
            display_allowed=False,
            decision="rescan_required",
            reason=FAIL_CLOSED_REGISTRATION_FAILURE,
            lanes_read=lanes_read,
        )
    warnings = [] if section.colour_ok else ["colour_degraded_but_hash_and_registration_passed"]
    return VerificationState(
        section_id=section.section_id,
        display_allowed=section.display_allowed_hint,
        decision="display_allowed" if section.display_allowed_hint else "rejected_fail_closed",
        reason="" if section.display_allowed_hint else FAIL_CLOSED_UNVERIFIED_SECTION,
        warnings=warnings,
        lanes_read=lanes_read,
    )


class AMCFPhysicalPlayerStateMachine:
    def __init__(
        self,
        player_profile: PlayerProfile | None = None,
        mechanism_profile: MechanismProfile | None = None,
        cartridge: PhysicalPlayerCartridge | None = None,
    ) -> None:
        self.player_profile = player_profile or PlayerProfile()
        self.mechanism_profile = mechanism_profile or MechanismProfile()
        self.cartridge: PhysicalPlayerCartridge | None = None
        self.current_time_ms = 0
        self.current_section_id: str | None = None
        self.next_section_id: str | None = None
        self.old_section_id: str | None = None
        self.playback_state = STATE_NO_CARTRIDGE
        self.reader_prefetch_state = ReaderPrefetchState()
        self.current_verification_state = VerificationState()
        self.next_verification_state = VerificationState()
        self.ab_gate_state = ABGateState()
        self.view_gate_state = GateState()
        self.hidden_gate_state = GateState()
        self.transition_state = "idle"
        self.reverse_buffer_state = ReverseBufferState()
        self.seek_request_state = SeekRequestState()
        self.audio_sync_state = AudioSyncState()
        self.safety_state = SafetyState()
        self.event_log: list[dict[str, Any]] = []
        self.fail_closed_events: list[FailClosedDecision] = []
        self.unsafe_acceptance_count = 0
        if cartridge is not None:
            self.insert_cartridge(cartridge)

    def _record_event(self, event_type: str, from_state: str, to_state: str, detail: str = "") -> None:
        self.event_log.append(
            {
                "timestamp_ms": self.current_time_ms,
                "event_type": event_type,
                "from_state": from_state,
                "to_state": to_state,
                "current_section_id": self.current_section_id,
                "next_section_id": self.next_section_id,
                "detail": detail,
                "safety_state": self.safety_state.state,
                "display_allowed": self.safety_state.display_allowed,
            }
        )

    def _set_state(self, state: str, event_type: str, detail: str = "") -> None:
        previous = self.playback_state
        self.playback_state = state
        self._record_event(event_type, previous, state, detail)

    def _section_by_id(self, section_id: str | None) -> PhysicalPlayerSection | None:
        return self.cartridge.get_section(section_id) if self.cartridge else None

    def _playback_sections(self) -> list[PhysicalPlayerSection]:
        return self.cartridge.playback_sections() if self.cartridge else []

    def insert_cartridge(self, cartridge: PhysicalPlayerCartridge) -> None:
        self.cartridge = cartridge
        self.safety_state = SafetyState(state="cartridge_inserted")
        self._set_state(STATE_CARTRIDGE_INSERTED, "insert_cartridge", f"cartridge_id={cartridge.cartridge_id}")

    def recognize_manifest(self) -> bool:
        if self.cartridge is None:
            self.fail_closed(FAIL_CLOSED_MANIFEST_MISMATCH, "insert a cartridge before recognition")
            return False
        if not self.cartridge.carrier_supported:
            self.fail_closed(FAIL_CLOSED_UNSUPPORTED_CARRIER, "use indexed thin-section carrier")
            return False
        if not self.cartridge.recognized or not self.cartridge.manifest_matched:
            self.fail_closed(FAIL_CLOSED_MANIFEST_MISMATCH, "rescan or replace cartridge manifest")
            return False
        self._set_state(STATE_MANIFEST_RECOGNIZED, "recognize_manifest", self.cartridge.manifest_id)
        return True

    def prefetch_current(self) -> bool:
        sections = self._playback_sections()
        if not sections:
            self.fail_closed(FAIL_CLOSED_UNVERIFIED_SECTION, "no playback-required sections available")
            return False
        section = sections[0]
        self.current_section_id = section.section_id
        self.reader_prefetch_state = ReaderPrefetchState(
            expected_section_id=section.section_id,
            prefetched_section_id=section.section_id,
            lanes_read={"timing_index": section.timing_index_read, "registration": section.registration_read, "metadata": section.metadata_read, "hash": section.hash_read},
            queue=[item.section_id for item in sections[1:]],
        )
        self._set_state(STATE_PREFETCH_CURRENT, "prefetch_current", section.section_id)
        return True

    def verify_current(self) -> bool:
        verification = verify_physical_section(self._section_by_id(self.current_section_id))
        self.current_verification_state = verification
        if verification.display_allowed:
            self._set_state(STATE_VERIFY_CURRENT, "verify_current", verification.section_id or "")
            return True
        if verification.decision == "rescan_required":
            self._set_state(STATE_RESCAN_REQUIRED, "verify_current_rescan_required", verification.reason)
            return False
        self.fail_closed(verification.reason or FAIL_CLOSED_UNVERIFIED_SECTION, "do not display current section")
        return False

    def load_view_gate(self) -> bool:
        if not self.current_verification_state.display_allowed:
            self.fail_closed(FAIL_CLOSED_UNVERIFIED_SECTION, "verify current section before loading view gate")
            return False
        self.view_gate_state = GateState(section_id=self.current_section_id, state="loading", aligned=False, illumination_allowed=False)
        self._set_state(STATE_LOAD_VIEW_GATE, "load_view_gate", self.current_section_id or "")
        return True

    def lock_view_gate(self) -> bool:
        if self.view_gate_state.section_id != self.current_section_id:
            self.fail_closed(FAIL_CLOSED_WRONG_SECTION, "load expected current section into view gate")
            return False
        self.view_gate_state.state = "fine_aligned"
        self.view_gate_state.locked = True
        self.view_gate_state.aligned = True
        self.view_gate_state.illumination_allowed = bool(self.current_verification_state.display_allowed)
        self._set_state(STATE_VIEW_GATE_LOCKED, "lock_view_gate", self.current_section_id or "")
        return True

    def enter_playback_ready(self) -> bool:
        if not self.view_gate_state.locked or not self.current_verification_state.display_allowed:
            self.fail_closed(FAIL_CLOSED_GATE_UNLOCKED, "lock verified view gate before playback")
            return False
        self.view_gate_state.visible = True
        self.ab_gate_state.visible_section_id = self.current_section_id
        self.safety_state = SafetyState(
            state="playback_allowed",
            playback_allowed=True,
            display_allowed=True,
            motion_allowed=True,
            transition_allowed=True,
        )
        self.audio_sync_state = AudioSyncState(state="ready", drift_ms=0, within_limit=True)
        self._set_state(STATE_PLAYBACK_READY, "enter_playback_ready", self.current_section_id or "")
        return True

    def prefetch_next(self) -> bool:
        sections = self._playback_sections()
        if not self.current_section_id:
            self.fail_closed(FAIL_CLOSED_WRONG_SECTION, "current section missing before next prefetch")
            return False
        current_index = next((index for index, section in enumerate(sections) if section.section_id == self.current_section_id), -1)
        if current_index < 0 or current_index + 1 >= len(sections):
            self.next_section_id = None
            self._set_state(STATE_PLAYBACK_COMPLETE, "prefetch_next_complete", "no next section")
            return False
        section = sections[current_index + 1]
        self.next_section_id = section.section_id
        self.reader_prefetch_state.expected_section_id = section.section_id
        self.reader_prefetch_state.prefetched_section_id = section.section_id
        self.reader_prefetch_state.lanes_read = {
            "timing_index": section.timing_index_read,
            "registration": section.registration_read,
            "metadata": section.metadata_read,
            "hash": section.hash_read,
        }
        self.reader_prefetch_state.queue = [item.section_id for item in sections[current_index + 2 :]]
        self._set_state(STATE_PREFETCH_NEXT, "prefetch_next", section.section_id)
        return True

    def verify_next(self) -> bool:
        verification = verify_physical_section(self._section_by_id(self.next_section_id))
        self.next_verification_state = verification
        if verification.display_allowed:
            self._set_state(STATE_VERIFY_NEXT, "verify_next", verification.section_id or "")
            return True
        if verification.decision == "rescan_required":
            self._set_state(STATE_RESCAN_REQUIRED, "verify_next_rescan_required", verification.reason)
            return False
        self.fail_closed(verification.reason or FAIL_CLOSED_UNVERIFIED_SECTION, "do not stage next section")
        return False

    def stage_next(self) -> bool:
        if not self.next_verification_state.display_allowed:
            self.fail_closed(FAIL_CLOSED_UNVERIFIED_SECTION, "verify next section before hidden staging")
            return False
        self.hidden_gate_state = GateState(
            section_id=self.next_section_id,
            state="staged_hidden",
            locked=True,
            aligned=True,
            illumination_allowed=False,
            ready_for_switch=True,
        )
        self.ab_gate_state.hidden_section_id = self.next_section_id
        self._set_state(STATE_STAGE_NEXT, "stage_next", self.next_section_id or "")
        return True

    def wait_until_update_timestamp(self, target_timestamp_ms: int) -> bool:
        if not self.hidden_gate_state.ready_for_switch or not self.next_verification_state.display_allowed:
            self.fail_closed(FAIL_CLOSED_PREFETCH_TIMEOUT, "next section not verified and staged by update timestamp")
            return False
        if target_timestamp_ms > self.current_time_ms:
            self.current_time_ms = target_timestamp_ms
        self._set_state(STATE_WAIT_UPDATE_TIMESTAMP, "wait_until_update_timestamp", str(target_timestamp_ms))
        return True

    def begin_transition_blank(self) -> bool:
        if not self.hidden_gate_state.ready_for_switch:
            self.fail_closed(FAIL_CLOSED_SHUTTER_FAILURE, "hidden gate not ready for blanked transition")
            return False
        self.ab_gate_state.blanking_active = True
        self.transition_state = "blanking_active"
        self.view_gate_state.illumination_allowed = False
        self._set_state(STATE_TRANSITION_BLANK, "begin_transition_blank", "shutter_closed")
        return True

    def switch_visible_section(self) -> bool:
        if not self.ab_gate_state.blanking_active:
            self.fail_closed(FAIL_CLOSED_SHUTTER_FAILURE, "transition blanking must be active before switch")
            return False
        if not self.hidden_gate_state.ready_for_switch or not self.next_verification_state.display_allowed:
            self.fail_closed(FAIL_CLOSED_UNVERIFIED_SECTION, "hidden staged section is not verified")
            return False
        self.old_section_id = self.current_section_id
        self.current_section_id = self.hidden_gate_state.section_id
        self.next_section_id = None
        self.current_verification_state = self.next_verification_state
        self.next_verification_state = VerificationState()
        self.view_gate_state = GateState(
            section_id=self.current_section_id,
            state="visible_locked",
            locked=True,
            aligned=True,
            illumination_allowed=False,
            ready_for_switch=False,
            visible=True,
        )
        self.hidden_gate_state = GateState()
        self.ab_gate_state.visible_section_id = self.current_section_id
        self.ab_gate_state.hidden_section_id = None
        self.ab_gate_state.old_section_id = self.old_section_id
        self._set_state(STATE_SWITCH_VISIBLE_SECTION, "switch_visible_section", self.current_section_id or "")
        return True

    def park_old_section(self) -> bool:
        if self.old_section_id and self.reverse_buffer_state.enabled:
            self.reverse_buffer_state.section_ids.append(self.old_section_id)
            self.reverse_buffer_state.section_ids = self.reverse_buffer_state.section_ids[-self.reverse_buffer_state.depth :]
        self.old_section_id = None
        self.ab_gate_state.old_section_id = None
        self.ab_gate_state.blanking_active = False
        self.transition_state = "idle"
        self.view_gate_state.illumination_allowed = True
        self._set_state(STATE_PARK_OLD_SECTION, "park_old_section", "old section parked")
        return True

    def tick(self, delta_ms: int) -> None:
        self.current_time_ms += max(0, int(delta_ms))
        self._record_event("tick", self.playback_state, self.playback_state, f"delta_ms={delta_ms}")

    def pause(self) -> bool:
        safe_visible = self.view_gate_state.visible and self.current_verification_state.display_allowed
        self.safety_state.motion_allowed = False
        self.safety_state.transition_allowed = False
        self.safety_state.display_allowed = safe_visible
        self.safety_state.playback_allowed = False
        self.safety_state.state = "paused_safe"
        self._set_state(STATE_PAUSED_SAFE, "pause", "safe visible hold" if safe_visible else "paused without display")
        return True

    def resume(self) -> bool:
        if self.current_verification_state.display_allowed and self.view_gate_state.locked:
            self.safety_state = SafetyState("playback_allowed", True, True, True, True)
            self._set_state(STATE_PLAYBACK_READY, "resume", self.current_section_id or "")
            return True
        self._set_state(STATE_RESCAN_REQUIRED, "resume_rescan_required", "current section not verified or gate unlocked")
        return False

    def step_forward(self) -> bool:
        if not self.prefetch_next():
            return self.playback_state == STATE_PLAYBACK_COMPLETE
        if not self.verify_next():
            return False
        if not self.stage_next():
            return False
        section = self._section_by_id(self.next_section_id)
        timestamp = section.update_timestamp_ms if section else self.current_time_ms
        return (
            self.wait_until_update_timestamp(timestamp)
            and self.begin_transition_blank()
            and self.switch_visible_section()
            and self.park_old_section()
        )

    def step_reverse(self) -> bool:
        if not self.reverse_buffer_state.enabled or not self.reverse_buffer_state.section_ids:
            self._record_event("step_reverse_denied", self.playback_state, self.playback_state, "reverse buffer unavailable")
            return False
        previous_section_id = self.reverse_buffer_state.section_ids.pop()
        section = self._section_by_id(previous_section_id)
        verification = verify_physical_section(section)
        if not verification.display_allowed:
            self.fail_closed(verification.reason or FAIL_CLOSED_UNVERIFIED_SECTION, "do not reverse to unverified section")
            return False
        self.next_section_id = previous_section_id
        self.next_verification_state = verification
        if not self.stage_next():
            return False
        return self.begin_transition_blank() and self.switch_visible_section() and self.park_old_section()

    def request_seek(self, timestamp_ms: int | None = None, section_id: str | None = None) -> bool:
        requested_section_id = section_id
        if requested_section_id is None and timestamp_ms is not None and self.cartridge is not None:
            for section in self._playback_sections():
                if section.update_timestamp_ms == timestamp_ms:
                    requested_section_id = section.section_id
                    break
        local = set(self.reverse_buffer_state.section_ids) | set(self.reader_prefetch_state.queue)
        if requested_section_id in local:
            self.seek_request_state = SeekRequestState(timestamp_ms, requested_section_id, True, "")
            self._record_event("seek_allowed_local_buffer", self.playback_state, self.playback_state, requested_section_id or "")
            return True
        self.seek_request_state = SeekRequestState(timestamp_ms, requested_section_id, False, "unsupported_or_not_in_local_buffer")
        self._record_event("seek_denied", self.playback_state, self.playback_state, self.seek_request_state.denial_reason)
        return False

    def fail_closed(self, reason: str, recommended_action: str) -> FailClosedDecision:
        decision = FailClosedDecision(
            timestamp_ms=self.current_time_ms,
            reason=reason,
            recommended_action=recommended_action,
            current_section_id=self.current_section_id,
            next_section_id=self.next_section_id,
            unsafe_acceptance_count=self.unsafe_acceptance_count,
        )
        self.fail_closed_events.append(decision)
        previous = self.playback_state
        self.playback_state = STATE_FAIL_CLOSED
        self.safety_state = SafetyState(
            state=STATE_FAIL_CLOSED,
            playback_allowed=False,
            display_allowed=bool(self.view_gate_state.visible and self.current_verification_state.display_allowed),
            motion_allowed=False,
            transition_allowed=False,
        )
        self._record_event("fail_closed", previous, STATE_FAIL_CLOSED, f"{reason}:{recommended_action}")
        return decision

    def build_timeline(self) -> list[dict[str, Any]]:
        return list(self.event_log)

    def build_summary(self) -> dict[str, Any]:
        return {
            "software_control_simulator_only": True,
            "hardware_validation_claimed": False,
            "physical_level5_claimed": False,
            "real_sensors_motors_cartridges_scans_required": False,
            "final_playback_state": self.playback_state,
            "final_safety_state": self.safety_state.state,
            "event_count": len(self.event_log),
            "fail_closed_event_count": len(self.fail_closed_events),
            "unsafe_acceptance_count": self.unsafe_acceptance_count,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "player_profile": _to_plain(self.player_profile),
            "mechanism_profile": _to_plain(self.mechanism_profile),
            "cartridge": _to_plain(self.cartridge),
            "current_time_ms": self.current_time_ms,
            "current_section_id": self.current_section_id,
            "next_section_id": self.next_section_id,
            "playback_state": self.playback_state,
            "reader_prefetch_state": _to_plain(self.reader_prefetch_state),
            "current_verification_state": _to_plain(self.current_verification_state),
            "next_verification_state": _to_plain(self.next_verification_state),
            "ab_gate_state": _to_plain(self.ab_gate_state),
            "view_gate_state": _to_plain(self.view_gate_state),
            "hidden_gate_state": _to_plain(self.hidden_gate_state),
            "transition_state": self.transition_state,
            "reverse_buffer_state": _to_plain(self.reverse_buffer_state),
            "seek_request_state": _to_plain(self.seek_request_state),
            "audio_sync_state": _to_plain(self.audio_sync_state),
            "safety_state": _to_plain(self.safety_state),
            "event_log": self.build_timeline(),
            "fail_closed_events": _to_plain(self.fail_closed_events),
            "unsafe_acceptance_count": self.unsafe_acceptance_count,
            "summary": self.build_summary(),
        }
