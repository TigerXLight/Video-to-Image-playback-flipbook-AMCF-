from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from amcf_physical_carrier import REQUIRED_LANES, validate_physical_carrier_package


TIMELINE_SCHEMA = "amcf-mechanical-optical-player-timeline-v1"


def _claim_boundary() -> dict[str, bool]:
    return {
        "real_physical_playback_claimed": False,
        "digital_screen_physical_player_claimed": False,
        "physical_proof_claimed": False,
        "hardware_validation_claimed": False,
        "final_ui_claimed": False,
        "manufacturing_readiness_claimed": False,
        "physical_prototype_built": False,
        "real_optical_hardware_used": False,
    }


@dataclass
class MechanicalOpticalPlayerConfig:
    fps: int = 12
    alignment_tolerance: float = 0.25
    illumination_enabled: bool = True
    view_gate_id: str = "fixed_view_gate_001"
    transport_mode: str = "indexed_section_transport"
    forced_alignment_errors: dict[int, float] = field(default_factory=dict)


@dataclass
class ViewGateState:
    timeline_index: int
    command: str
    section_index: int
    alignment_error: float
    alignment_ok: bool
    illumination_on: bool
    visible_payload_reference: str
    section_file: str
    decision: str
    issues: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "timeline_index": self.timeline_index,
            "command": self.command,
            "section_index": self.section_index,
            "alignment_error": self.alignment_error,
            "alignment_ok": self.alignment_ok,
            "illumination_on": self.illumination_on,
            "visible_payload_reference": self.visible_payload_reference,
            "section_file": self.section_file,
            "decision": self.decision,
            "issues": self.issues,
        }


@dataclass
class MechanicalOpticalPlayerState:
    loaded: bool = False
    current_section: int = 0
    section_count: int = 0
    playing: bool = False
    direction: str = "forward"
    fail_closed: bool = False
    issues: list[str] = field(default_factory=list)
    timeline: list[ViewGateState] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "loaded": self.loaded,
            "current_section": self.current_section,
            "section_count": self.section_count,
            "playing": self.playing,
            "direction": self.direction,
            "fail_closed": self.fail_closed,
            "issues": self.issues,
            "timeline": [state.to_dict() for state in self.timeline],
        }


def load_carrier_for_physical_player(package_root: str | Path) -> dict[str, Any]:
    package_root = Path(package_root)
    validation = validate_physical_carrier_package(package_root)
    if not validation.get("ok"):
        return {
            "ok": False,
            "errors": validation.get("errors", []),
            "sections": [],
            "manifest": {},
            "unsafe_acceptance_count": 0,
        }
    manifest_path = package_root / "physical_carrier_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sections = sorted(manifest.get("sections", []), key=lambda item: int(item.get("section_index", -1)))
    errors: list[str] = []
    expected_indices = list(range(len(sections)))
    actual_indices = [int(section.get("section_index", -1)) for section in sections]
    if actual_indices != expected_indices:
        errors.append("carrier_sections_not_contiguous_or_ordered")
    for section in sections:
        lanes = section.get("lanes", {})
        for lane in REQUIRED_LANES:
            if lane not in lanes:
                errors.append(f"missing_lane:{section.get('section_index')}:{lane}")
    return {
        "ok": not errors,
        "errors": errors,
        "sections": sections if not errors else [],
        "manifest": manifest,
        "unsafe_acceptance_count": 0,
    }


class MechanicalOpticalPlayerSimulator:
    def __init__(self, config: MechanicalOpticalPlayerConfig | None = None) -> None:
        self.config = config or MechanicalOpticalPlayerConfig()
        self.state = MechanicalOpticalPlayerState()
        self.sections: list[dict[str, Any]] = []

    def load_carrier(self, package_root: str | Path) -> dict[str, Any]:
        loaded = load_carrier_for_physical_player(package_root)
        if not loaded["ok"]:
            self.state.fail_closed = True
            self.state.issues.extend(loaded["errors"])
            return loaded
        self.sections = loaded["sections"]
        self.state = MechanicalOpticalPlayerState(loaded=True, current_section=0, section_count=len(self.sections))
        return loaded

    def _require_loaded(self) -> None:
        if not self.state.loaded or not self.sections:
            raise RuntimeError("no carrier loaded")
        if self.state.fail_closed:
            raise RuntimeError("player is fail-closed")

    def _emit_view_gate_state(self, command: str, section_index: int) -> ViewGateState:
        self._require_loaded()
        if section_index < 0 or section_index >= len(self.sections):
            self.state.fail_closed = True
            raise IndexError(f"section_index out of range: {section_index}")
        section = self.sections[section_index]
        lanes = section["lanes"]
        payload = lanes["payload_lane"]
        alignment_error = float(self.config.forced_alignment_errors.get(section_index, 0.0))
        issues: list[str] = []
        alignment_ok = abs(alignment_error) <= self.config.alignment_tolerance
        if not alignment_ok:
            issues.append("view_gate_misalignment_beyond_tolerance")
        if not self.config.illumination_enabled:
            issues.append("illumination_off")
        decision = "presented" if not issues else "rejected_fail_closed"
        if issues:
            self.state.fail_closed = True
            self.state.issues.extend(issues)
        view_state = ViewGateState(
            timeline_index=len(self.state.timeline),
            command=command,
            section_index=section_index,
            alignment_error=alignment_error,
            alignment_ok=alignment_ok,
            illumination_on=self.config.illumination_enabled,
            visible_payload_reference=str(payload.get("source_payload_path")),
            section_file=str(section.get("section_file")),
            decision=decision,
            issues=issues,
        )
        self.state.timeline.append(view_state)
        self.state.current_section = section_index
        return view_state

    def play(self) -> list[ViewGateState]:
        self._require_loaded()
        self.state.playing = True
        self.state.direction = "forward"
        states = []
        for index in range(self.state.current_section, self.state.section_count):
            states.append(self._emit_view_gate_state("play", index))
            if self.state.fail_closed:
                break
        self.state.playing = False
        return states

    def pause(self) -> ViewGateState:
        self._require_loaded()
        self.state.playing = False
        return self._emit_view_gate_state("pause", self.state.current_section)

    def step_forward(self) -> ViewGateState:
        self._require_loaded()
        return self._emit_view_gate_state("step_forward", min(self.state.current_section + 1, self.state.section_count - 1))

    def step_backward(self) -> ViewGateState:
        self._require_loaded()
        return self._emit_view_gate_state("step_backward", max(self.state.current_section - 1, 0))

    def seek_to_section(self, section_index: int) -> ViewGateState:
        self._require_loaded()
        return self._emit_view_gate_state("seek_to_section", section_index)

    def reverse(self) -> list[ViewGateState]:
        self._require_loaded()
        self.state.playing = True
        self.state.direction = "reverse"
        states = []
        for index in range(self.state.current_section, -1, -1):
            states.append(self._emit_view_gate_state("reverse", index))
            if self.state.fail_closed:
                break
        self.state.playing = False
        return states


def validate_mechanical_optical_player_timeline(timeline_path: str | Path) -> dict[str, Any]:
    timeline_path = Path(timeline_path)
    errors: list[str] = []
    if not timeline_path.exists():
        return {"ok": False, "errors": ["timeline_missing"], "unsafe_acceptance_count": 0}
    data = json.loads(timeline_path.read_text(encoding="utf-8"))
    if data.get("schema") != TIMELINE_SCHEMA:
        errors.append("unsupported_timeline_schema")
    states = data.get("view_gate_states", [])
    if not isinstance(states, list) or not states:
        errors.append("view_gate_states_missing_or_empty")
        states = []
    commands = {state.get("command") for state in states if isinstance(state, dict)}
    for command in ("play", "pause", "step_forward", "step_backward", "seek_to_section", "reverse"):
        if command not in commands:
            errors.append(f"missing_command:{command}")
    for expected_timeline_index, state in enumerate(states):
        for key in ("section_index", "alignment_error", "alignment_ok", "illumination_on", "visible_payload_reference", "decision"):
            if key not in state:
                errors.append(f"view_gate_state_missing:{expected_timeline_index}:{key}")
        if state.get("timeline_index") != expected_timeline_index:
            errors.append(f"timeline_index_mismatch:{expected_timeline_index}")
        if state.get("decision") == "presented" and not state.get("alignment_ok"):
            errors.append(f"unsafe_presented_misaligned_section:{expected_timeline_index}")
        if state.get("decision") == "presented" and not state.get("illumination_on"):
            errors.append(f"unsafe_presented_without_illumination:{expected_timeline_index}")
    boundary = data.get("claim_boundary", {})
    for key in _claim_boundary():
        if boundary.get(key) is not False:
            errors.append(f"unsafe_claim_boundary:{key}")
    return {
        "ok": not errors,
        "errors": errors,
        "timeline_count": len(states),
        "commands_seen": sorted(str(command) for command in commands),
        "unsafe_acceptance_count": 0,
        "claim_boundary": boundary,
    }


def simulate_mechanical_optical_playback(package_root: str | Path, output_root: str | Path) -> dict[str, Any]:
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    simulator = MechanicalOpticalPlayerSimulator()
    loaded = simulator.load_carrier(package_root)
    if not loaded["ok"]:
        validation = {"ok": False, "errors": loaded["errors"], "unsafe_acceptance_count": 0}
        (output_root / "player_validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True), encoding="utf-8")
        return {"ok": False, "loaded": False, "errors": loaded["errors"], "unsafe_acceptance_count": 0}
    simulator.play()
    simulator.pause()
    simulator.step_forward()
    simulator.step_backward()
    simulator.seek_to_section(min(3, simulator.state.section_count - 1))
    simulator.reverse()

    view_states = [state.to_dict() for state in simulator.state.timeline]
    timeline = {
        "schema": TIMELINE_SCHEMA,
        "player_kind": "software_simulated_mechanical_optical_physical_player",
        "physical_playback_path": "AMCF physical media -> indexed transport -> fixed physical view gate -> illumination/optical presentation -> direct human viewing",
        "transport_mode": simulator.config.transport_mode,
        "view_gate_id": simulator.config.view_gate_id,
        "fps": simulator.config.fps,
        "section_count": simulator.state.section_count,
        "view_gate_states": view_states,
        "claim_boundary": _claim_boundary(),
    }
    (output_root / "player_timeline.json").write_text(json.dumps(timeline, indent=2, sort_keys=True), encoding="utf-8")
    (output_root / "view_gate_states.json").write_text(json.dumps(view_states, indent=2, sort_keys=True), encoding="utf-8")
    validation = validate_mechanical_optical_player_timeline(output_root / "player_timeline.json")
    (output_root / "player_validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True), encoding="utf-8")
    summary = [
        "# Mechanical / Optical Player Simulation Summary",
        "",
        f"- player simulator loaded carrier: {'yes' if loaded.get('ok') else 'no'}",
        f"- view-gate states generated: {'yes' if bool(view_states) else 'no'}",
        f"- timeline generated: yes",
        f"- play/pause/step/reverse/seek simulated: {'yes' if validation.get('ok') else 'no'}",
        f"- validation pass: {'yes' if validation.get('ok') else 'no'}",
        f"- unsafe acceptance count: {validation.get('unsafe_acceptance_count', 0)}",
        "- real physical playback performed: no",
        "- digital-screen playback claimed: no",
        "- physical proof claimed: no",
        "- hardware validation claimed: no",
        "- final UI claimed: no",
        "",
        "This is software simulation of future mechanical/optical physical playback behaviour. It is not a real optical device and not physical validation.",
    ]
    (output_root / "mechanical_optical_player_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    return {
        "ok": bool(validation.get("ok")),
        "loaded": bool(loaded.get("ok")),
        "timeline_path": str(output_root / "player_timeline.json"),
        "view_gate_states_path": str(output_root / "view_gate_states.json"),
        "validation_path": str(output_root / "player_validation.json"),
        "timeline_count": validation.get("timeline_count", 0),
        "unsafe_acceptance_count": validation.get("unsafe_acceptance_count", 0),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate AMCF mechanical/optical physical-player behaviour.")
    sub = parser.add_subparsers(dest="command", required=True)
    sim = sub.add_parser("simulate")
    sim.add_argument("carrier_package")
    sim.add_argument("output_root")
    val = sub.add_parser("validate")
    val.add_argument("timeline")
    args = parser.parse_args()
    if args.command == "simulate":
        result = simulate_mechanical_optical_playback(args.carrier_package, args.output_root)
    else:
        result = validate_mechanical_optical_player_timeline(args.timeline)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
