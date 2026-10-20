from __future__ import annotations

import tempfile
import sys
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_device_provider_adapters import (
    FileCarrierProvider,
    FolderCaptureProvider,
    LoopbackPlayerProvider,
    _sha256,
    run_device_provider_discovery,
)
from amcf_software_io_fixtures import load_fixture_bundle


class DeviceProviderAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_default_provider_set_passes_without_hardware(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_device_provider_discovery(self.repo_root, directory)
            report = result["report"]
            self.assertTrue(report["final_passed"])
            self.assertTrue(report["interface_ready"])
            self.assertTrue(report["selected_backends_ready"])
            self.assertTrue(report["software_operations_passed"])
            self.assertFalse(report["hardware_connected"])
            self.assertEqual(report["unsafe_acceptance_count"], 0)
            self.assertEqual(len(report["provider_probes"]), 3)
            self.assertTrue((Path(directory) / "device_provider_discovery_report.json").exists())
            self.assertTrue((Path(directory) / "carrier").exists())

    def test_file_carrier_provider_requires_manifest_hash_and_writes_artifact(self) -> None:
        bundle = load_fixture_bundle(self.repo_root)
        manifest = bundle["package"]["manifest"]
        with tempfile.TemporaryDirectory() as directory:
            provider = FileCarrierProvider(directory)
            rejected = provider.submit_carrier(manifest, "wrong")
            self.assertFalse(rejected["accepted"])
            self.assertTrue(rejected["fail_closed"])
            accepted = provider.submit_carrier(manifest, _sha256(manifest))
            self.assertTrue(accepted["accepted"])
            self.assertTrue(Path(accepted["artifact_path"]).exists())
            self.assertFalse(accepted["hardware_connected"])

    def test_explicit_hardware_backends_remain_disabled_without_enable_flag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_device_provider_discovery(
                self.repo_root,
                directory,
                printer_backend="windows-spooler",
                reader_backend="windows-wia",
                player_backend="serial",
                printer_name="AMCF-test-printer",
                reader_device="AMCF-test-reader",
                player_port="COM999",
                enable_hardware=False,
            )
            report = result["report"]
            self.assertFalse(report["final_passed"])
            self.assertFalse(report["hardware_connected"])
            self.assertEqual(report["unsafe_acceptance_count"], 0)
            self.assertTrue(all(not probe["available"] for probe in report["provider_probes"]))
            self.assertTrue(all(probe["reason"] == "hardware_not_enabled" for probe in report["provider_probes"]))

    def test_loopback_rejects_unverified_visible_switch(self) -> None:
        bundle = load_fixture_bundle(self.repo_root)
        manifest = bundle["package"]["manifest"]
        section_id = manifest["physical_sections"][0]["section_id"]
        player = LoopbackPlayerProvider()
        self.assertTrue(player.load_manifest(manifest)["accepted"])
        result = player.switch_visible(section_id)
        self.assertFalse(result["accepted"])
        self.assertTrue(result["fail_closed"])
        self.assertFalse(result["transition_allowed"])

    def test_adapters_run_behind_versioned_control_protocol(self) -> None:
        from amcf_software_control_protocol import (
            COMMAND_CAPTURE_SECTION,
            COMMAND_CLOSE,
            COMMAND_HELLO,
            COMMAND_PLAYER_LOAD_MANIFEST,
            COMMAND_PLAYER_PREFETCH,
            COMMAND_PLAYER_SWITCH,
            COMMAND_PLAYER_VERIFY,
            COMMAND_SUBMIT_CARRIER,
            PROTOCOL_VERSION,
            SoftwareControlSession,
        )

        bundle = load_fixture_bundle(self.repo_root)
        manifest = bundle["package"]["manifest"]
        with tempfile.TemporaryDirectory() as directory:
            printer = FileCarrierProvider(Path(directory) / "carrier")
            reader = FolderCaptureProvider(self.repo_root / "tests" / "fixtures" / "amcf_software_io")
            player = LoopbackPlayerProvider()
            session = SoftwareControlSession(bundle, printer=printer, reader=reader, player=player)
            responses = [
                session.send(COMMAND_HELLO, "shared_core", {"protocol_version": PROTOCOL_VERSION, "required_capabilities": []}),
                session.send(COMMAND_SUBMIT_CARRIER, "pc_to_printer", {"artifact_hash": _sha256(manifest)}),
            ]
            for section in manifest["physical_sections"]:
                responses.append(session.send(COMMAND_CAPTURE_SECTION, "reader_to_pc", {"section_id": section["section_id"]}))
            responses.append(session.send(COMMAND_PLAYER_LOAD_MANIFEST, "pc_to_player"))
            for event in manifest["update_events"]:
                section_id = str(event["section_id"])
                section = next(item for item in manifest["physical_sections"] if item["section_id"] == section_id)
                responses.append(session.send(COMMAND_PLAYER_PREFETCH, "pc_to_player", {"section_id": section_id}))
                responses.append(session.send(COMMAND_PLAYER_VERIFY, "pc_to_player", {"section_id": section_id, "expected_hash": section["payload_hash"]}))
                responses.append(session.send(COMMAND_PLAYER_SWITCH, "pc_to_player", {"section_id": section_id}))
            responses.append(session.send(COMMAND_CLOSE, "shared_core"))
            self.assertTrue(all(response.accepted for response in responses))
            self.assertTrue(all(not response.unsafe_acceptance for response in responses))


if __name__ == "__main__":
    unittest.main()
