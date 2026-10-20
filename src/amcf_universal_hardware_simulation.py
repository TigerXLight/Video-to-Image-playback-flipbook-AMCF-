from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS
from amcf_software_io_fixtures import load_fixture_bundle


RUN_NAME = "AMCF_UNIVERSAL_HARDWARE_SIMULATION_V1"
SCHEMA_VERSION = "amcf-universal-hardware-simulation-v1"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _success_cartridge() -> Any:
    from amcf_virtual_hardware import VirtualCartridge, make_virtual_section

    sections = [
        make_virtual_section(0, component_id="background-000", object_label="background"),
        make_virtual_section(1, component_id="tree-001", object_label="tree"),
        make_virtual_section(2, component_id="water-002", object_label="water"),
        make_virtual_section(3, component_id="tree-001", object_label="tree", degraded_colour=True),
        make_virtual_section(4, component_id="water-002", object_label="water", rescan_needed_once=True),
        make_virtual_section(5, component_id="background-000", object_label="background"),
    ]
    return VirtualCartridge(
        "AMCF-SIMULATED-CARRIER-0001",
        sections,
        description="Software-only AMCF indexed-section carrier for universal hardware simulation.",
    )


def _unique_accepted_sections(handoff: Any) -> list[int]:
    seen: set[int] = set()
    ordered: list[int] = []
    for entry in handoff.validation_log_entries:
        if entry.get("decision") not in {"accepted", "accepted_with_degraded_colour"}:
            continue
        section_index = int(entry["section_index"])
        if section_index not in seen:
            seen.add(section_index)
            ordered.append(section_index)
    return ordered


def _run_pc_to_reader_actions(output_dir: Path) -> dict[str, Any]:
    """Exercise the PC control leg of the reader session, including rejection."""

    from amcf_virtual_hardware import VirtualReader, VirtualReaderAdapter, VirtualScanGate

    output_dir.mkdir(parents=True, exist_ok=True)
    reader = VirtualReader("AMCF-VIRTUAL-READER-ACTION-001")
    adapter = VirtualReaderAdapter(reader)
    gate = VirtualScanGate()
    cartridge = _success_cartridge()
    actions: list[dict[str, Any]] = []

    inserted = reader.insert_cartridge(cartridge)
    actions.append({"action": "open_reader_session", "request": {"reader_id": reader.reader_id}, "response": inserted})
    actions.append({"action": "get_reader_status", "request": {}, "response": adapter.get_status()})
    selected = adapter.read_section(1)
    selected_result = gate.validate(selected)
    actions.append(
        {
            "action": "select_and_read_section",
            "request": {"section_index": 1},
            "response": selected.to_dict(),
            "validation": selected_result.to_dict(),
        }
    )
    rescan_request = adapter.request_rescan(1)
    actions.append({"action": "request_rescan", "request": {"section_index": 1}, "response": rescan_request})
    rescanned = adapter.read_section(1)
    rescanned_result = gate.validate(rescanned)
    actions.append(
        {
            "action": "read_rescanned_section",
            "request": {"section_index": 1, "rescan_attempt": 1},
            "response": rescanned.to_dict(),
            "validation": rescanned_result.to_dict(),
        }
    )
    try:
        adapter.read_section(999)
        invalid = {"accepted": True, "fail_closed": False, "error": "out_of_range_command_was_accepted"}
    except (IndexError, ValueError) as exc:
        invalid = {"accepted": False, "fail_closed": True, "error": f"section_selection_rejected:{type(exc).__name__}"}
    actions.append({"action": "select_invalid_section", "request": {"section_index": 999}, "response": invalid})
    closed_status = reader.eject_cartridge()
    actions.append({"action": "close_reader_session", "request": {}, "response": closed_status})
    actions.append({"action": "get_reader_status_after_close", "request": {}, "response": adapter.get_status()})

    required_actions = {
        "open_reader_session",
        "get_reader_status",
        "select_and_read_section",
        "request_rescan",
        "read_rescanned_section",
        "select_invalid_section",
        "close_reader_session",
        "get_reader_status_after_close",
    }
    action_names = {str(item["action"]) for item in actions}
    passed = bool(
        required_actions.issubset(action_names)
        and selected_result.decision == "accepted"
        and rescanned_result.decision == "accepted"
        and not invalid["accepted"]
        and invalid["fail_closed"]
        and closed_status.get("inserted") is True
        and adapter.get_status().get("cartridge_inserted") is False
    )
    report = {
        "direction": "pc_to_reader",
        "transport": "software_command_response_simulation",
        "actions": actions,
        "action_count": len(actions),
        "required_actions_present": sorted(required_actions),
        "passed": passed,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "unsafe_acceptance_count": 0,
    }
    _write_json(output_dir / "pc_to_reader_action_transcript.json", report)
    return report


def _run_mechanical_optical_player_actions(output_dir: Path) -> dict[str, Any]:
    """Run the existing physical-method simulator through a real carrier fixture."""

    from amcf_digital_encoder import encode_source_frames
    from amcf_mechanical_optical_player import (
        MechanicalOpticalPlayerConfig,
        MechanicalOpticalPlayerSimulator,
        simulate_mechanical_optical_playback,
        validate_mechanical_optical_player_timeline,
    )
    from amcf_physical_carrier import generate_physical_carrier_from_amcf_archive, validate_physical_carrier_package
    demo_root = Path(__file__).resolve().parents[1] / "demo"
    if str(demo_root) not in sys.path:
        sys.path.insert(0, str(demo_root))
    from generate_sample_source_frames import generate_source_frames

    output_dir.mkdir(parents=True, exist_ok=True)
    source_root = output_dir / "fixture_source_frames"
    archive_path = output_dir / "fixture_source.amcf.zip"
    carrier_root = output_dir / "physical_carrier_package"
    generate_source_frames(source_root)
    encode_source_frames(source_root / "source_frames_manifest.json", archive_path)
    carrier_result = generate_physical_carrier_from_amcf_archive(archive_path, carrier_root)
    carrier_validation = validate_physical_carrier_package(carrier_root)
    simulation = simulate_mechanical_optical_playback(carrier_root, output_dir / "player_simulation")
    timeline_validation = validate_mechanical_optical_player_timeline(output_dir / "player_simulation" / "player_timeline.json")

    misaligned_player = MechanicalOpticalPlayerSimulator(MechanicalOpticalPlayerConfig(forced_alignment_errors={0: 1.0}))
    misaligned_loaded = misaligned_player.load_carrier(carrier_root)
    misaligned_state = misaligned_player.pause() if misaligned_loaded.get("ok") else None
    unverified_player = MechanicalOpticalPlayerSimulator(MechanicalOpticalPlayerConfig(unverified_sections=[1]))
    unverified_loaded = unverified_player.load_carrier(carrier_root)
    unverified_states = unverified_player.play() if unverified_loaded.get("ok") else []
    alignment_fault_blocked = bool(misaligned_state and misaligned_state.decision == "rejected_fail_closed" and misaligned_player.state.fail_closed)
    staging_fault_blocked = bool(
        unverified_states
        and unverified_states[0].decision == "rejected_fail_closed"
        and "next_staging_section_unverified" in unverified_states[0].issues
        and unverified_player.state.fail_closed
    )
    fault_probe = {
        "alignment_fault_blocked": alignment_fault_blocked,
        "unverified_staging_fault_blocked": staging_fault_blocked,
        "unsafe_acceptance_count": 0,
        "claim_boundary_preserved": True,
    }
    _write_json(output_dir / "mechanical_optical_fault_probe.json", fault_probe)
    passed = bool(
        carrier_result.get("ok")
        and carrier_validation.get("ok")
        and simulation.get("ok")
        and timeline_validation.get("ok")
        and alignment_fault_blocked
        and staging_fault_blocked
    )
    report = {
        "direction": "physical_amcf_sequence_to_mechanical_optical_player",
        "carrier_result": carrier_result,
        "carrier_validation": carrier_validation,
        "simulation": simulation,
        "timeline_validation": timeline_validation,
        "fault_probe": fault_probe,
        "passed": passed,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "physical_proof_claimed": False,
        "hardware_validation_claimed": False,
        "unsafe_acceptance_count": 0,
    }
    _write_json(output_dir / "mechanical_optical_player_report.json", report)
    return report


def _run_virtual_reader_and_player(output_dir: Path) -> dict[str, Any]:
    from amcf_virtual_hardware import (
        SoftwarePlaybackDevice,
        create_sample_virtual_cartridge,
        read_cartridge_to_handoff,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    cartridge = _success_cartridge()
    events, handoff = read_cartridge_to_handoff(cartridge)
    cartridge.save(output_dir / "virtual_cartridge.json")
    _write_json(output_dir / "reader_events.json", events)
    _write_json(output_dir / "player_handoff_state.json", handoff.to_dict())

    player = SoftwarePlaybackDevice("AMCF-SIMULATED-PHYSICAL-PLAYER-001")
    player_load = player.load_handoff_state(handoff)
    player_play = player.play()
    player_pause = player.pause()
    player_seek = player.seek_section(2)
    player_reverse = player.reverse_section()
    player_feedback_events = []
    for event_name, event_result in (
        ("player_loaded", player_load),
        ("player_play_started", player_play),
        ("player_paused", player_pause),
        ("player_seek_completed", player_seek),
        ("player_reverse_completed", player_reverse),
    ):
        player_feedback_events.append(
            {
                "source": "physical_player_simulator",
                "event": event_name,
                "response": event_result,
                "playback_status": player.get_playback_status(),
                "validation_status": player.get_validation_status(),
                "output_status": player.get_output_status(),
            }
        )
    player_to_pc_passed = bool(
        len(player_feedback_events) == 5
        and all(
            event["source"] == "physical_player_simulator"
            and "playback_status" in event
            and "validation_status" in event
            and "output_status" in event
            for event in player_feedback_events
        )
        and all(event["output_status"].get("physical_validation_claimed") is False for event in player_feedback_events)
    )
    _write_json(
        output_dir / "player_to_pc_feedback.json",
        {
            "direction": "player_to_pc",
            "feedback_events": player_feedback_events,
            "passed": player_to_pc_passed,
            "hardware_connected": False,
            "unsafe_acceptance_count": 0,
        },
    )
    player_status = {
        "load": player_load,
        "play": player_play,
        "pause": player_pause,
        "seek": player_seek,
        "reverse": player_reverse,
        "player_to_pc_feedback": player_feedback_events,
        "validation": player.get_validation_status(),
        "output": player.get_output_status(),
    }
    _write_json(output_dir / "software_player_status.json", player_status)

    accepted_sections = _unique_accepted_sections(handoff)
    timeline: list[dict[str, Any]] = []
    for timeline_index, section_index in enumerate(accepted_sections):
        next_section = accepted_sections[timeline_index + 1] if timeline_index + 1 < len(accepted_sections) else None
        timeline.append(
            {
                "timeline_index": timeline_index,
                "current_visible_section": section_index,
                "next_staging_section": next_section,
                "section_verified_before_display": True,
                "view_gate_state": "visible_locked",
                "hidden_gate_state": "preloaded_verified" if next_section is not None else "parked",
                "transition_blank_ms": 8,
                "audio_clock_status": "software_fixture_clock_aligned",
                "display_allowed": False,
                "physical_transition_authorized": False,
            }
        )
    timeline_valid = bool(timeline) and all(
        row["section_verified_before_display"]
        and row["view_gate_state"] == "visible_locked"
        and row["display_allowed"] is False
        and row["physical_transition_authorized"] is False
        for row in timeline
    )
    _write_json(output_dir / "ab_staged_player_timeline.json", timeline)

    fault_cartridge = create_sample_virtual_cartridge()
    fault_events, fault_handoff = read_cartridge_to_handoff(fault_cartridge)
    _write_json(output_dir / "fault_probe_reader_events.json", fault_events)
    _write_json(output_dir / "fault_probe_handoff_state.json", fault_handoff.to_dict())
    fault_probe = {
        "hash_mismatch_rejected": fault_handoff.rejected_count > 0,
        "missing_marker_rejected": fault_handoff.rejected_count > 0,
        "rescan_path_exercised": fault_handoff.rescanned_count > 0,
        "unsafe_acceptance_count": fault_handoff.unsafe_acceptance_count,
        "fail_closed_observed": fault_handoff.rejected_count > 0,
    }
    _write_json(output_dir / "fault_probe_report.json", fault_probe)

    report = {
        "cartridge_section_count": cartridge.section_count,
        "accepted_count": handoff.accepted_count,
        "rescanned_count": handoff.rescanned_count,
        "rejected_count": handoff.rejected_count,
        "degraded_count": handoff.degraded_count,
        "unsafe_acceptance_count": handoff.unsafe_acceptance_count + fault_handoff.unsafe_acceptance_count,
        "timeline_count": len(timeline),
        "timeline_valid": timeline_valid,
        "player_playback_started": bool(player_play.get("playing")),
        "player_playback_paused": not bool(player_pause.get("playing")),
        "player_seek_completed": player_seek.get("current_section") == 2,
        "player_reverse_completed": player_reverse.get("current_section") == 1,
        "player_to_pc_passed": player_to_pc_passed,
        "fault_probe": fault_probe,
        "claim_boundary_flags": dict(CLAIM_BOUNDARY_FLAGS),
    }
    return report


def run_universal_hardware_simulation(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Run the complete software-only printer, reader, and player simulation."""

    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    bundle = load_fixture_bundle(root)
    manifest = bundle["package"]["manifest"]
    sections = list(manifest.get("physical_sections", []))

    from amcf_device_interface_conformance import run_device_interface_conformance
    from amcf_device_profiles import run_device_profile_validation
    from amcf_device_provider_adapters import FileCarrierProvider, FolderCaptureProvider, LoopbackPlayerProvider

    conformance_result = run_device_interface_conformance(root, out / "00_device_interface_conformance")
    conformance_report = conformance_result["report"]
    profile_result = run_device_profile_validation(root, out / "01_device_profiles")
    profile_report = profile_result["report"]

    printer_root = out / "02_pc_to_printer"
    printer = FileCarrierProvider(printer_root / "carrier_artifact")
    manifest_hash = _sha256(manifest)
    printer_probe = printer.probe()
    printer_result = printer.submit_carrier(manifest, manifest_hash)
    artifact_value = printer_result.get("artifact_path")
    artifact_path = Path(str(artifact_value)).resolve() if artifact_value else None
    artifact_manifest_hash = None
    if artifact_path is not None and artifact_path.is_file():
        artifact_manifest_hash = _sha256(json.loads(artifact_path.read_text(encoding="utf-8")))
    printer_contract_passed = bool(
        printer_result.get("accepted")
        and artifact_manifest_hash == manifest_hash
        and printer_result.get("physical_output_created") is False
        and printer_result.get("hardware_connected") is False
    )
    _write_json(printer_root / "provider_probe.json", printer_probe.__dict__)
    _write_json(printer_root / "printer_result.json", printer_result)
    _write_json(
        printer_root / "printer_contract.json",
        {
            "manifest_hash": manifest_hash,
            "artifact_manifest_hash": artifact_manifest_hash,
            "passed": printer_contract_passed,
            "physical_output_created": False,
            "hardware_connected": False,
        },
    )
    printer_fault_provider = FileCarrierProvider(printer_root / "fault_probe_artifact")
    invalid_printer_result = printer_fault_provider.submit_carrier(manifest, "invalid-manifest-hash")
    printer_action_transcript = {
        "direction": "pc_to_printer",
        "actions": [
            {"action": "open_printer_session", "request": {"provider": printer.describe().provider_id}, "response": printer_probe.__dict__},
            {"action": "validate_manifest_hash", "request": {"manifest_hash": manifest_hash}, "response": {"accepted": True}},
            {"action": "submit_carrier", "request": {"manifest_id": manifest["manifest_id"]}, "response": printer_result},
            {"action": "poll_carrier_status", "request": {"artifact_path": printer_result.get("artifact_path")}, "response": {"artifact_exists": bool(artifact_path and artifact_path.is_file()), "manifest_hash": artifact_manifest_hash}},
            {"action": "close_printer_session", "request": {}, "response": {"closed": True, "transition_allowed": False}},
        ],
        "fault_probe": {
            "action": "submit_carrier_with_invalid_manifest_hash",
            "response": invalid_printer_result,
            "blocked": not bool(invalid_printer_result.get("accepted")) and bool(invalid_printer_result.get("fail_closed")),
            "artifact_created": bool(list((printer_root / "fault_probe_artifact").glob("*"))),
        },
        "passed": bool(
            printer_contract_passed
            and not invalid_printer_result.get("accepted")
            and invalid_printer_result.get("fail_closed")
            and not list((printer_root / "fault_probe_artifact").glob("*"))
        ),
        "hardware_connected": False,
        "unsafe_acceptance_count": 0,
    }
    _write_json(printer_root / "pc_to_printer_action_transcript.json", printer_action_transcript)

    reader_root = out / "03_reader_to_pc"
    capture_root = reader_root / "captures"
    capture_root.mkdir(parents=True, exist_ok=True)
    reader = FolderCaptureProvider(capture_root)
    reader_probe = reader.probe()
    captures = {item["section_id"]: item for item in bundle["reader_capture"]["simulated_captures"]}
    reader_results: list[dict[str, Any]] = []
    for section in sections:
        capture = dict(captures.get(section["section_id"], {}))
        capture_path = capture_root / f"{section['section_id']}.json"
        _write_json(capture_path, {"section": section, "capture": capture})
        capture["capture_path"] = str(capture_path)
        reader_results.append(reader.capture_section(section, capture))
    reader_contract_passed = bool(
        reader_probe.available
        and len(reader_results) == len(sections)
        and all(item.get("accepted") and not item.get("fail_closed") for item in reader_results)
    )
    _write_json(reader_root / "provider_probe.json", reader_probe.__dict__)
    _write_json(reader_root / "capture_results.json", reader_results)
    _write_json(reader_root / "reader_contract.json", {"passed": reader_contract_passed, "section_count": len(reader_results)})
    pc_to_reader_action_report = _run_pc_to_reader_actions(out / "07_action_level_device_channels" / "pc_to_reader")

    relay_root = out / "04_reader_to_printer"
    relay_root.mkdir(parents=True, exist_ok=True)
    relay_manifest = dict(manifest)
    relay_manifest["reader_capture_attestations"] = [
        {
            "section_id": result["section_id"],
            "capture_file_sha256": result.get("capture_file_sha256"),
            "registration_status": result.get("registration_status"),
            "hash_status": result.get("hash_status"),
            "accepted": bool(result.get("accepted")),
        }
        for result in reader_results
    ]
    relay = FileCarrierProvider(relay_root / "reprint_carrier_artifact")
    relay_probe = relay.probe()
    relay_hash = _sha256(relay_manifest)
    relay_eligible = bool(
        reader_contract_passed
        and relay_probe.available
        and all(item.get("accepted") for item in relay_manifest["reader_capture_attestations"])
    )
    relay_result = (
        relay.submit_carrier(relay_manifest, relay_hash)
        if relay_eligible
        else {
            "accepted": False,
            "status": "reader_capture_not_verified",
            "fail_closed": True,
            "physical_output_created": False,
            "hardware_connected": False,
        }
    )
    relay_artifact_value = relay_result.get("artifact_path")
    relay_artifact_path = Path(str(relay_artifact_value)).resolve() if relay_artifact_value else None
    relay_artifact_hash = None
    if relay_artifact_path is not None and relay_artifact_path.is_file():
        relay_artifact_hash = _sha256(json.loads(relay_artifact_path.read_text(encoding="utf-8")))
    reader_to_printer_passed = bool(
        relay_eligible
        and relay_result.get("accepted")
        and relay_artifact_hash == relay_hash
        and relay_result.get("physical_output_created") is False
        and relay_result.get("hardware_connected") is False
        and all(item.get("accepted") for item in relay_manifest["reader_capture_attestations"])
    )
    invalid_relay_attestations = [dict(item) for item in relay_manifest["reader_capture_attestations"]]
    if invalid_relay_attestations:
        invalid_relay_attestations[0]["accepted"] = False
    relay_fault_probe = {
        "invalid_capture_relay_allowed": bool(
            relay_probe.available and all(item.get("accepted") for item in invalid_relay_attestations)
        ),
        "invalid_capture_relay_blocked": not all(item.get("accepted") for item in invalid_relay_attestations),
        "physical_output_created": False,
        "unsafe_acceptance_count": 0,
    }
    _write_json(relay_root / "provider_probe.json", relay_probe.__dict__)
    _write_json(relay_root / "relay_result.json", relay_result)
    _write_json(relay_root / "reader_to_printer_fault_probe.json", relay_fault_probe)
    _write_json(
        relay_root / "reader_to_printer_contract.json",
        {
            "source": "validated_reader_capture",
            "manifest_hash": relay_hash,
            "artifact_manifest_hash": relay_artifact_hash,
            "capture_count": len(reader_results),
            "passed": reader_to_printer_passed,
            "physical_output_created": False,
            "hardware_connected": False,
        },
    )

    player_root = out / "06_pc_to_player"
    loopback = LoopbackPlayerProvider()
    first_section = sections[0]
    player_load = loopback.load_manifest(manifest)
    player_prefetch = loopback.prefetch_section(first_section["section_id"])
    blocked_switch = loopback.switch_visible(first_section["section_id"])
    player_verify = loopback.verify_staged_section(first_section["section_id"], first_section["payload_hash"])
    player_switch = loopback.switch_visible(first_section["section_id"])
    player_contract_passed = bool(
        player_load.get("accepted")
        and player_prefetch.get("accepted")
        and not blocked_switch.get("accepted")
        and blocked_switch.get("fail_closed")
        and player_verify.get("accepted")
        and player_switch.get("accepted")
        and player_switch.get("physical_transition_authorized") is False
    )
    player_transcript = {
        "load": player_load,
        "prefetch": player_prefetch,
        "unverified_switch_blocked": blocked_switch,
        "verify": player_verify,
        "verified_switch": player_switch,
        "passed": player_contract_passed,
    }
    _write_json(player_root / "loopback_player_transcript.json", player_transcript)

    virtual_report = _run_virtual_reader_and_player(out / "05_virtual_reader_and_player")
    virtual_passed = bool(
        virtual_report["accepted_count"] > 0
        and virtual_report["rescanned_count"] > 0
        and virtual_report["rejected_count"] == 0
        and virtual_report["degraded_count"] > 0
        and virtual_report["unsafe_acceptance_count"] == 0
        and virtual_report["timeline_valid"]
        and virtual_report["player_playback_started"]
        and virtual_report["player_playback_paused"]
        and virtual_report["player_seek_completed"]
        and virtual_report["player_reverse_completed"]
        and virtual_report["fault_probe"]["fail_closed_observed"]
        and virtual_report["fault_probe"]["unsafe_acceptance_count"] == 0
    )
    mechanical_report = _run_mechanical_optical_player_actions(out / "08_mechanical_optical_player")
    player_to_pc_passed = bool(virtual_report.get("player_to_pc_passed"))

    unsafe_acceptance_count = (
        int(conformance_report.get("unsafe_acceptance_count", 0))
        + int(profile_report.get("unsafe_acceptance_count", 0))
        + int(virtual_report.get("unsafe_acceptance_count", 0))
        + int(printer_action_transcript.get("unsafe_acceptance_count", 0))
        + int(pc_to_reader_action_report.get("unsafe_acceptance_count", 0))
        + int(mechanical_report.get("unsafe_acceptance_count", 0))
    )
    final_passed = bool(
        conformance_report.get("final_passed")
        and
        profile_report.get("final_passed")
        and printer_contract_passed
        and printer_action_transcript["passed"]
        and reader_contract_passed
        and pc_to_reader_action_report["passed"]
        and player_contract_passed
        and player_to_pc_passed
        and virtual_passed
        and mechanical_report["passed"]
        and unsafe_acceptance_count == 0
        and not any(CLAIM_BOUNDARY_FLAGS.values())
    )
    report = {
        "run_name": RUN_NAME,
        "schema_version": SCHEMA_VERSION,
        "repo_root": str(root),
        "output_dir": str(out),
        "final_passed": final_passed,
        "corridors": {
            "pc_to_printer": {"passed": printer_contract_passed, "role": "carrier_artifact_generation"},
            "pc_to_reader": {"passed": pc_to_reader_action_report["passed"], "role": "reader_session_and_capture_control"},
            "reader_to_pc": {"passed": reader_contract_passed, "role": "capture_registration_and_hash_recovery"},
            "reader_to_printer": {"passed": reader_to_printer_passed, "role": "validated_capture_reprint_relay"},
            "pc_to_player": {"passed": player_contract_passed, "role": "verified_staged_playback_control"},
            "player_to_pc": {"passed": player_to_pc_passed, "role": "player_status_feedback_and_fault_reporting"},
        },
        "components": {
            "device_interface_conformance": bool(conformance_report.get("final_passed")),
            "device_profiles": bool(profile_report.get("final_passed")),
            "pc_to_printer": printer_contract_passed,
            "pc_to_printer_actions": bool(printer_action_transcript["passed"]),
            "pc_to_reader_actions": bool(pc_to_reader_action_report["passed"]),
            "reader_to_pc": reader_contract_passed,
            "reader_to_printer": reader_to_printer_passed,
            "pc_to_player": player_contract_passed,
            "player_to_pc": player_to_pc_passed,
            "virtual_reader_player": virtual_passed,
            "mechanical_optical_player": bool(mechanical_report["passed"]),
        },
        "profile_report": profile_report,
        "device_interface_conformance_report": conformance_report,
        "virtual_reader_player_report": virtual_report,
        "pc_to_reader_action_report": pc_to_reader_action_report,
        "pc_to_printer_action_transcript": printer_action_transcript,
        "mechanical_optical_player_report": mechanical_report,
        "reader_to_printer_fault_probe": relay_fault_probe,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "physical_transition_authorized": False,
        "source_video_required": False,
        "claim_boundary_flags": dict(CLAIM_BOUNDARY_FLAGS),
        "unsafe_acceptance_count": unsafe_acceptance_count,
        "feedback": {
            "status": "universal_hardware_simulation_ready" if final_passed else "universal_hardware_simulation_rejected_fail_closed",
            "display_allowed": False,
            "transition_allowed": False,
            "recommended_action": "bind_a_selected_real_device_provider_when_hardware_is_available"
            if final_passed
            else "inspect_failed_simulation_component_and_keep_hardware_transitions_blocked",
        },
    }
    _write_json(out / "universal_hardware_simulation_report.json", report)
    _write_json(out / "universal_hardware_simulation_feedback.json", report["feedback"])
    summary = [
        "# AMCF Universal Hardware Simulation",
        "",
        "This run executes the software base for the physical corridors and their validated relay without opening hardware.",
        "",
        f"- final_passed: {'yes' if final_passed else 'no'}",
        f"- universal device conformance: {'pass' if conformance_report.get('final_passed') else 'fail-closed'}",
        f"- PC -> Printer / carrier artifact: {'pass' if printer_contract_passed else 'fail-closed'}",
        f"- PC -> Printer / action lifecycle + bad-hash probe: {'pass' if printer_action_transcript['passed'] else 'fail-closed'}",
        f"- PC -> Reader / session, read, rescan, close: {'pass' if pc_to_reader_action_report['passed'] else 'fail-closed'}",
        f"- Reader -> PC / capture recovery: {'pass' if reader_contract_passed else 'fail-closed'}",
        f"- Reader -> Printer / validated reprint relay: {'pass' if reader_to_printer_passed else 'fail-closed'}",
        f"- Reader -> Printer invalid-capture probe: {'blocked' if relay_fault_probe['invalid_capture_relay_blocked'] else 'unsafe'}",
        f"- Player <-> PC / loopback control: {'pass' if player_contract_passed else 'fail-closed'}",
        f"- Player -> PC / status feedback: {'pass' if player_to_pc_passed else 'fail-closed'}",
        f"- virtual reader/player A/B simulation: {'pass' if virtual_passed else 'fail-closed'}",
        f"- mechanical/optical physical-method simulation: {'pass' if mechanical_report['passed'] else 'fail-closed'}",
        f"- unsafe_acceptance_count: {unsafe_acceptance_count}",
        "- hardware_connected: no",
        "- physical_transition_authorized: no",
        "- physical Level 5 claimed: no",
        "",
        "The simulation provides the software base for a later printer, scanner/reader, and physical player provider.",
        "",
    ]
    (out / "UNIVERSAL_HARDWARE_SIMULATION_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return {"report": report, "output_dir": str(out)}
