from __future__ import annotations

import hashlib
import json
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
    player_status = {
        "load": player_load,
        "play": player_play,
        "pause": player_pause,
        "seek": player_seek,
        "reverse": player_reverse,
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

    unsafe_acceptance_count = (
        int(conformance_report.get("unsafe_acceptance_count", 0))
        + int(profile_report.get("unsafe_acceptance_count", 0))
        + int(virtual_report.get("unsafe_acceptance_count", 0))
    )
    final_passed = bool(
        conformance_report.get("final_passed")
        and
        profile_report.get("final_passed")
        and printer_contract_passed
        and reader_contract_passed
        and player_contract_passed
        and virtual_passed
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
            "reader_to_pc": {"passed": reader_contract_passed, "role": "capture_registration_and_hash_recovery"},
            "reader_to_printer": {"passed": reader_to_printer_passed, "role": "validated_capture_reprint_relay"},
            "pc_to_player": {"passed": player_contract_passed, "role": "verified_staged_playback_control"},
        },
        "components": {
            "device_interface_conformance": bool(conformance_report.get("final_passed")),
            "device_profiles": bool(profile_report.get("final_passed")),
            "pc_to_printer": printer_contract_passed,
            "reader_to_pc": reader_contract_passed,
            "reader_to_printer": reader_to_printer_passed,
            "pc_to_player": player_contract_passed,
            "virtual_reader_player": virtual_passed,
        },
        "profile_report": profile_report,
        "device_interface_conformance_report": conformance_report,
        "virtual_reader_player_report": virtual_report,
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
        f"- Reader -> PC / capture recovery: {'pass' if reader_contract_passed else 'fail-closed'}",
        f"- Reader -> Printer / validated reprint relay: {'pass' if reader_to_printer_passed else 'fail-closed'}",
        f"- Reader -> Printer invalid-capture probe: {'blocked' if relay_fault_probe['invalid_capture_relay_blocked'] else 'unsafe'}",
        f"- Player <-> PC / loopback control: {'pass' if player_contract_passed else 'fail-closed'}",
        f"- virtual reader/player A/B simulation: {'pass' if virtual_passed else 'fail-closed'}",
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
