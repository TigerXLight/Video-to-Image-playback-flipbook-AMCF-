from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from amcf_hardware_provider_runtime import (
    PlayerControlProvider,
    PrinterCarrierProvider,
    ReaderCaptureProvider,
    SimulatedPlayerControlProvider,
    SimulatedPrintToFileProvider,
    SimulatedReaderCaptureProvider,
)
from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS
from amcf_software_io_fixtures import load_fixture_bundle


PROTOCOL_VERSION = "amcf-software-control-protocol-v1"
RUN_NAME = "AMCF_SOFTWARE_CONTROL_PROTOCOL_RUNTIME_V1"

COMMAND_HELLO = "HELLO"
COMMAND_SUBMIT_CARRIER = "SUBMIT_CARRIER"
COMMAND_CAPTURE_SECTION = "CAPTURE_SECTION"
COMMAND_PLAYER_LOAD_MANIFEST = "PLAYER_LOAD_MANIFEST"
COMMAND_PLAYER_PREFETCH = "PLAYER_PREFETCH_SECTION"
COMMAND_PLAYER_VERIFY = "PLAYER_VERIFY_SECTION"
COMMAND_PLAYER_SWITCH = "PLAYER_SWITCH_VISIBLE"
COMMAND_PLAYER_SEEK = "PLAYER_SEEK_LOCAL_BUFFER"
COMMAND_PLAYER_REVERSE = "PLAYER_REVERSE_LOCAL_BUFFER"
COMMAND_PLAYER_STOP = "PLAYER_STOP"
COMMAND_CLOSE = "CLOSE_SESSION"

SUPPORTED_COMMANDS = (
    COMMAND_HELLO,
    COMMAND_SUBMIT_CARRIER,
    COMMAND_CAPTURE_SECTION,
    COMMAND_PLAYER_LOAD_MANIFEST,
    COMMAND_PLAYER_PREFETCH,
    COMMAND_PLAYER_VERIFY,
    COMMAND_PLAYER_SWITCH,
    COMMAND_PLAYER_SEEK,
    COMMAND_PLAYER_REVERSE,
    COMMAND_PLAYER_STOP,
    COMMAND_CLOSE,
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SoftwareCapabilityProfile:
    profile_id: str
    protocol_version: str
    corridors: tuple[str, ...]
    commands: tuple[str, ...]
    carrier_layout: str
    staging_model: str
    gate_model: str
    seek_model: str
    reverse_model: str
    safety_model: str
    hardware_validation_claimed: bool = False


@dataclass(frozen=True)
class ProtocolEnvelope:
    session_id: str
    sequence: int
    command_id: str
    corridor: str
    command: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProtocolResponse:
    session_id: str
    sequence: int
    command_id: str
    command: str
    accepted: bool
    state: str
    code: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    display_allowed: bool = False
    transition_allowed: bool = False
    retry_allowed: bool = False
    rescan_allowed: bool = False
    fail_closed: bool = False
    unsafe_acceptance: bool = False


def _plain(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: _plain(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    return value


def build_capability_profile(bundle: dict[str, Any]) -> SoftwareCapabilityProfile:
    profile = bundle["player_profile"]
    return SoftwareCapabilityProfile(
        profile_id="amcf-software-control-profile-v1",
        protocol_version=PROTOCOL_VERSION,
        corridors=("pc_to_printer", "reader_to_pc", "pc_to_player"),
        commands=SUPPORTED_COMMANDS,
        carrier_layout=str(profile["carrier_layout"]),
        staging_model=str(profile["staging_model"]),
        gate_model=str(profile["gate_model"]),
        seek_model=str(profile["seek_model"]),
        reverse_model=str(profile["reverse_model"]),
        safety_model=str(profile["safety_model"]),
        hardware_validation_claimed=bool(profile.get("hardware_validation_claimed", False)),
    )


class SoftwareControlSession:
    """Deterministic command/session layer shared by future device providers.

    The session owns protocol ordering and safety decisions. Providers only
    perform corridor-specific operations and never authorize physical output.
    """

    def __init__(
        self,
        bundle: dict[str, Any],
        *,
        printer: PrinterCarrierProvider | None = None,
        reader: ReaderCaptureProvider | None = None,
        player: PlayerControlProvider | None = None,
    ) -> None:
        self.bundle = bundle
        self.manifest = bundle["package"]["manifest"]
        self.profile = build_capability_profile(bundle)
        self.session_id = "AMCF-SESSION-" + _sha256(
            {"protocol": PROTOCOL_VERSION, "manifest_id": self.manifest["manifest_id"]}
        )[:20]
        self.printer = printer or SimulatedPrintToFileProvider()
        self.reader = reader or SimulatedReaderCaptureProvider()
        self.player = player or SimulatedPlayerControlProvider()
        self._sections = {str(item["section_id"]): item for item in self.manifest["physical_sections"]}
        self._captures = {
            str(item["section_id"]): item for item in bundle["reader_capture"]["simulated_captures"]
        }
        self._next_sequence = 0
        self._negotiated = False
        self._manifest_loaded = False
        self._closed = False
        self._verified_sections: list[str] = []
        self._visible_section: str | None = None
        self._transcript: list[dict[str, Any]] = []

    @property
    def transcript(self) -> list[dict[str, Any]]:
        return list(self._transcript)

    def send(self, command: str, corridor: str, payload: dict[str, Any] | None = None) -> ProtocolResponse:
        envelope = ProtocolEnvelope(
            session_id=self.session_id,
            sequence=self._next_sequence,
            command_id=f"cmd-{self._next_sequence:04d}",
            corridor=corridor,
            command=command,
            payload=dict(payload or {}),
        )
        return self.dispatch(envelope)

    def dispatch(self, envelope: ProtocolEnvelope) -> ProtocolResponse:
        if self._closed:
            return self._record(envelope, False, "session_closed", "SESSION_CLOSED", "Session is closed.", fail_closed=True)
        if envelope.session_id != self.session_id:
            return self._record(envelope, False, "session_rejected", "SESSION_ID_MISMATCH", "Session identity does not match.", fail_closed=True)
        if envelope.sequence != self._next_sequence:
            self._closed = True
            return self._record(
                envelope,
                False,
                "fail_closed",
                "SEQUENCE_REJECTED_FAIL_CLOSED",
                f"Expected sequence {self._next_sequence}, received {envelope.sequence}.",
                fail_closed=True,
            )
        if envelope.command != COMMAND_HELLO and not self._negotiated:
            return self._record(
                envelope,
                False,
                "fail_closed",
                "NEGOTIATION_REQUIRED",
                "Capability negotiation must pass before corridor commands.",
                fail_closed=True,
            )

        handlers = {
            COMMAND_HELLO: self._hello,
            COMMAND_SUBMIT_CARRIER: self._submit_carrier,
            COMMAND_CAPTURE_SECTION: self._capture_section,
            COMMAND_PLAYER_LOAD_MANIFEST: self._player_load_manifest,
            COMMAND_PLAYER_PREFETCH: self._player_prefetch,
            COMMAND_PLAYER_VERIFY: self._player_verify,
            COMMAND_PLAYER_SWITCH: self._player_switch,
            COMMAND_PLAYER_SEEK: self._player_seek,
            COMMAND_PLAYER_REVERSE: self._player_reverse,
            COMMAND_PLAYER_STOP: self._player_stop,
            COMMAND_CLOSE: self._close_session,
        }
        handler = handlers.get(envelope.command)
        if handler is None:
            return self._record(
                envelope,
                False,
                "fail_closed",
                "UNKNOWN_COMMAND_REJECTED",
                f"Unsupported command: {envelope.command}.",
                fail_closed=True,
            )
        try:
            accepted, state, code, message, payload, retry, rescan, fail_closed = handler(envelope)
        except (KeyError, TypeError, ValueError) as exc:
            accepted, state, code, message, payload, retry, rescan, fail_closed = (
                False,
                "fail_closed",
                "MALFORMED_COMMAND_REJECTED",
                f"Malformed command payload: {exc}.",
                {},
                False,
                False,
                True,
            )
        return self._record(
            envelope,
            accepted,
            state,
            code,
            message,
            payload=payload,
            retry_allowed=retry,
            rescan_allowed=rescan,
            fail_closed=fail_closed,
        )

    def _record(
        self,
        envelope: ProtocolEnvelope,
        accepted: bool,
        state: str,
        code: str,
        message: str,
        *,
        payload: dict[str, Any] | None = None,
        retry_allowed: bool = False,
        rescan_allowed: bool = False,
        fail_closed: bool = False,
    ) -> ProtocolResponse:
        response = ProtocolResponse(
            session_id=self.session_id,
            sequence=envelope.sequence,
            command_id=envelope.command_id,
            command=envelope.command,
            accepted=accepted,
            state=state,
            code=code,
            message=message,
            payload=dict(payload or {}),
            display_allowed=False,
            transition_allowed=False,
            retry_allowed=retry_allowed,
            rescan_allowed=rescan_allowed,
            fail_closed=fail_closed,
            unsafe_acceptance=False,
        )
        self._transcript.append({"envelope": _plain(envelope), "response": _plain(response)})
        if envelope.sequence == self._next_sequence:
            self._next_sequence += 1
        return response

    def _hello(self, envelope: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        requested = str(envelope.payload.get("protocol_version", ""))
        required = [str(item) for item in envelope.payload.get("required_capabilities", [])]
        available = set(self.profile.commands)
        missing = [item for item in required if item not in available]
        accepted = requested == PROTOCOL_VERSION and not missing
        if accepted:
            self._negotiated = True
        return (
            accepted,
            "negotiated" if accepted else "fail_closed",
            "CAPABILITIES_NEGOTIATED" if accepted else "CAPABILITY_NEGOTIATION_REJECTED",
            "Software control capabilities negotiated." if accepted else "Protocol version or required capability mismatch.",
            {"protocol_version": PROTOCOL_VERSION, "missing_capabilities": missing, "profile_id": self.profile.profile_id},
            False,
            False,
            not accepted,
        )

    def _submit_carrier(self, envelope: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        artifact_hash = str(envelope.payload["artifact_hash"])
        expected_hash = _sha256(self.manifest)
        if artifact_hash != expected_hash:
            return False, "fail_closed", "CARRIER_HASH_REJECTED", "Carrier manifest hash does not match the session manifest.", {}, False, False, True
        result = self.printer.submit_carrier(self.manifest, artifact_hash)
        accepted = bool(result.get("accepted"))
        return accepted, "carrier_acknowledged" if accepted else "fail_closed", "CARRIER_ACKNOWLEDGED" if accepted else "CARRIER_REJECTED", "Carrier artifact was acknowledged by the provider." if accepted else "Carrier artifact was rejected.", result, False, False, not accepted

    def _capture_section(self, envelope: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        section_id = str(envelope.payload["section_id"])
        section = self._sections[section_id]
        capture = dict(envelope.payload.get("capture") or self._captures.get(section_id, {}))
        result = self.reader.capture_section(section, capture)
        accepted = bool(result.get("accepted"))
        return accepted, "section_recovered" if accepted else "rescan_required", "SECTION_CAPTURE_ACCEPTED" if accepted else "SECTION_CAPTURE_REJECTED", "Section capture checks passed." if accepted else "Section capture requires rescan.", result, False, not accepted, not accepted

    def _player_load_manifest(self, _: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        result = self.player.load_manifest(self.manifest)
        accepted = bool(result.get("accepted"))
        self._manifest_loaded = accepted
        return accepted, "manifest_loaded" if accepted else "fail_closed", "PLAYER_MANIFEST_ACCEPTED" if accepted else "PLAYER_MANIFEST_REJECTED", "Player manifest loaded." if accepted else "Player manifest rejected.", result, False, False, not accepted

    def _player_prefetch(self, envelope: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        section_id = str(envelope.payload["section_id"])
        if not self._manifest_loaded:
            return False, "fail_closed", "MANIFEST_REQUIRED", "Player manifest must be loaded first.", {}, False, False, True
        result = self.player.prefetch_section(section_id)
        accepted = bool(result.get("accepted"))
        return accepted, "section_prefetched" if accepted else "fail_closed", "SECTION_PREFETCHED" if accepted else "SECTION_PREFETCH_REJECTED", "Section prefetched into hidden staging." if accepted else "Section was not available for staging.", result, False, False, not accepted

    def _player_verify(self, envelope: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        section_id = str(envelope.payload["section_id"])
        expected_hash = str(envelope.payload["expected_hash"])
        result = self.player.verify_staged_section(section_id, expected_hash)
        accepted = bool(result.get("accepted"))
        if accepted and section_id not in self._verified_sections:
            self._verified_sections.append(section_id)
        return accepted, "section_verified" if accepted else "fail_closed", "SECTION_VERIFIED" if accepted else "SECTION_VERIFICATION_REJECTED", "Staged section verified." if accepted else "Staged section verification failed.", result, False, True, not accepted

    def _player_switch(self, envelope: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        section_id = str(envelope.payload["section_id"])
        result = self.player.switch_visible(section_id)
        accepted = bool(result.get("accepted"))
        if accepted:
            self._visible_section = section_id
        return accepted, "visible_state_updated" if accepted else "hold_previous_safe_state", "VISIBLE_STATE_UPDATED" if accepted else "VISIBLE_SWITCH_BLOCKED", "Virtual visible state updated." if accepted else "Visible switch blocked until the section is verified.", result, False, False, not accepted

    def _player_seek(self, envelope: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        target = str(envelope.payload["section_id"])
        if target not in self._verified_sections or str(envelope.payload.get("mode", "")) != "local_buffer":
            return False, "hold_previous_safe_state", "LOCAL_SEEK_DENIED", "Only verified sections in the local buffer may be selected.", {"target_section_id": target}, False, False, True
        self._visible_section = target
        return True, "local_seek_resolved", "LOCAL_SEEK_RESOLVED", "Local verified-buffer seek resolved.", {"target_section_id": target, "resolved_from_buffer": True}, False, False, False

    def _player_reverse(self, envelope: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        target = str(envelope.payload["section_id"])
        if target not in self._verified_sections or str(envelope.payload.get("mode", "")) != "local_buffer":
            return False, "hold_previous_safe_state", "LOCAL_REVERSE_DENIED", "Only verified sections in the local buffer may be reversed to.", {"target_section_id": target}, False, False, True
        self._visible_section = target
        return True, "local_reverse_resolved", "LOCAL_REVERSE_RESOLVED", "Local verified-buffer reverse resolved.", {"target_section_id": target, "resolved_from_buffer": True}, False, False, False

    def _player_stop(self, _: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        return True, "safe_stopped", "PLAYER_STOPPED_SAFE", "Player command path entered a safe stopped state.", {"display_allowed": False, "transition_allowed": False}, False, False, False

    def _close_session(self, _: ProtocolEnvelope) -> tuple[bool, str, str, str, dict[str, Any], bool, bool, bool]:
        self._closed = True
        return True, "closed", "SESSION_CLOSED", "Software control session closed cleanly.", {}, False, False, False


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_plain(value), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_software_control_session(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    bundle = load_fixture_bundle(root)
    session = SoftwareControlSession(bundle)
    manifest = bundle["package"]["manifest"]
    sections = manifest["physical_sections"]
    expected_capabilities = [COMMAND_SUBMIT_CARRIER, COMMAND_CAPTURE_SECTION, COMMAND_PLAYER_SWITCH]
    responses: list[ProtocolResponse] = []

    def send(command: str, corridor: str, payload: dict[str, Any] | None = None) -> ProtocolResponse:
        response = session.send(command, corridor, payload)
        responses.append(response)
        return response

    send(COMMAND_HELLO, "shared_core", {"protocol_version": PROTOCOL_VERSION, "required_capabilities": expected_capabilities})
    send(COMMAND_SUBMIT_CARRIER, "pc_to_printer", {"artifact_hash": _sha256(manifest)})
    for section in sections:
        send(COMMAND_CAPTURE_SECTION, "reader_to_pc", {"section_id": section["section_id"]})
    send(COMMAND_PLAYER_LOAD_MANIFEST, "pc_to_player")
    for event in manifest["update_events"]:
        section_id = str(event["section_id"])
        section = next(item for item in sections if item["section_id"] == section_id)
        send(COMMAND_PLAYER_PREFETCH, "pc_to_player", {"section_id": section_id})
        send(COMMAND_PLAYER_VERIFY, "pc_to_player", {"section_id": section_id, "expected_hash": section["payload_hash"]})
        send(COMMAND_PLAYER_SWITCH, "pc_to_player", {"section_id": section_id})
    send(COMMAND_PLAYER_SEEK, "pc_to_player", {"section_id": sections[1]["section_id"], "mode": "local_buffer"})
    send(COMMAND_PLAYER_REVERSE, "pc_to_player", {"section_id": sections[0]["section_id"], "mode": "local_buffer"})
    send(COMMAND_PLAYER_STOP, "pc_to_player")
    send(COMMAND_CLOSE, "shared_core")

    safety_session = SoftwareControlSession(bundle)
    safety_session.send(COMMAND_HELLO, "shared_core", {"protocol_version": PROTOCOL_VERSION, "required_capabilities": []})
    safety_session.send(COMMAND_PLAYER_LOAD_MANIFEST, "pc_to_player")
    unverified = safety_session.send(COMMAND_PLAYER_SWITCH, "pc_to_player", {"section_id": sections[0]["section_id"]})

    ordering_session = SoftwareControlSession(bundle)
    ordering_session.send(COMMAND_HELLO, "shared_core", {"protocol_version": PROTOCOL_VERSION, "required_capabilities": []})
    out_of_order = ordering_session.dispatch(
        ProtocolEnvelope(
            session_id=ordering_session.session_id,
            sequence=4,
            command_id="probe-sequence-gap",
            corridor="pc_to_player",
            command=COMMAND_PLAYER_STOP,
        )
    )
    expected_pass = all(item.accepted for item in responses)
    safety_pass = not unverified.accepted and unverified.fail_closed and not unverified.unsafe_acceptance
    ordering_pass = not out_of_order.accepted and out_of_order.fail_closed and not out_of_order.unsafe_acceptance
    unsafe_count = sum(int(item.unsafe_acceptance) for item in responses + [unverified, out_of_order])
    flags = dict(CLAIM_BOUNDARY_FLAGS)
    final_passed = expected_pass and safety_pass and ordering_pass and unsafe_count == 0 and not any(flags.values())
    report = {
        "run_name": RUN_NAME,
        "protocol_version": PROTOCOL_VERSION,
        "repo_root": str(root),
        "output_dir": str(out),
        "session_id": session.session_id,
        "final_passed": final_passed,
        "capability_profile": _plain(session.profile),
        "command_count": len(session.transcript),
        "accepted_command_count": sum(int(item["response"]["accepted"]) for item in session.transcript),
        "corridor_counts": {
            corridor: sum(1 for item in session.transcript if item["envelope"]["corridor"] == corridor)
            for corridor in ("pc_to_printer", "reader_to_pc", "pc_to_player", "shared_core")
        },
        "safety_probes": {
            "unverified_visible_switch_blocked": safety_pass,
            "sequence_gap_blocked": ordering_pass,
            "unverified_response": _plain(unverified),
            "sequence_gap_response": _plain(out_of_order),
        },
        "provider_ids": [
            session.printer.describe().provider_id,
            session.reader.describe().provider_id,
            session.player.describe().provider_id,
        ],
        "command_transcript": session.transcript,
        "claim_boundary_flags": flags,
        "unsafe_acceptance_count": unsafe_count,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "direct_hardware_transition_authorized": False,
        "source_video_required": False,
        "status": "software_control_protocol_ready" if final_passed else "software_control_protocol_rejected_fail_closed",
        "feedback": {
            "status": "accepted_software_only" if final_passed else "rejected_fail_closed",
            "display_allowed": False,
            "transition_allowed": False,
            "recommended_action": "implement_selected_device_provider_against_protocol" if final_passed else "repair_protocol_before_device_integration",
        },
    }
    _write_json(out / "software_control_protocol_report.json", report)
    _write_json(out / "software_control_capabilities.json", report["capability_profile"])
    _write_json(out / "software_control_command_transcript.json", report["command_transcript"])
    _write_json(out / "software_control_feedback.json", report["feedback"])
    summary = [
        "# AMCF Software Control Protocol",
        "",
        "This deterministic session exercises capability negotiation and command ordering across the printer, reader, and player software corridors. It does not open hardware or claim a real device protocol.",
        "",
        f"- protocol_version: {PROTOCOL_VERSION}",
        f"- final_passed: {'yes' if final_passed else 'no'}",
        f"- command_count: {report['command_count']}",
        f"- accepted_command_count: {report['accepted_command_count']}",
        f"- unverified_visible_switch_blocked: {'yes' if safety_pass else 'no'}",
        f"- sequence_gap_blocked: {'yes' if ordering_pass else 'no'}",
        f"- unsafe_acceptance_count: {unsafe_count}",
        "- hardware_connected: no",
        "- physical_hardware_validation_claimed: no",
        "",
        "Future device providers can map their transport to these envelopes while retaining the same capability, ordering, transcript, and fail-closed rules.",
        "",
    ]
    out.mkdir(parents=True, exist_ok=True)
    (out / "SOFTWARE_CONTROL_PROTOCOL_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return {"report": report, "output_dir": str(out)}
