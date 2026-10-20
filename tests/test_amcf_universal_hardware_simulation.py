from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_universal_hardware_simulation import run_universal_hardware_simulation  # noqa: E402


class AmcfUniversalHardwareSimulationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_universal_hardware_simulation_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_complete_software_only_simulation_passes(self) -> None:
        result = run_universal_hardware_simulation(PACKAGE, self.tmp / "run")
        report = result["report"]
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertTrue(all(item["passed"] for item in report["corridors"].values()))
        self.assertTrue(all(report["components"].values()))
        self.assertTrue(report["device_interface_conformance_report"]["final_passed"])
        self.assertTrue(report["reader_to_printer_fault_probe"]["invalid_capture_relay_blocked"])
        self.assertTrue(report["pc_to_reader_action_report"]["passed"])
        self.assertTrue(report["pc_to_printer_action_transcript"]["passed"])
        self.assertTrue(report["virtual_reader_player_report"]["player_to_pc_passed"])
        self.assertTrue(report["mechanical_optical_player_report"]["passed"])
        self.assertTrue(report["mechanical_optical_player_report"]["fault_probe"]["alignment_fault_blocked"])
        self.assertTrue(report["mechanical_optical_player_report"]["fault_probe"]["unverified_staging_fault_blocked"])
        self.assertFalse(report["hardware_connected"])
        self.assertFalse(report["real_driver_or_protocol_used"])
        self.assertFalse(report["physical_transition_authorized"])
        self.assertFalse(report["physical_level_5_claimed"])
        self.assertTrue(report["virtual_reader_player_report"]["fault_probe"]["fail_closed_observed"])

    def test_report_and_contract_artifacts_are_reopenable(self) -> None:
        output = self.tmp / "run"
        run_universal_hardware_simulation(PACKAGE, output)
        report = json.loads((output / "universal_hardware_simulation_report.json").read_text(encoding="utf-8"))
        relay = json.loads((output / "04_reader_to_printer" / "reader_to_printer_contract.json").read_text(encoding="utf-8"))
        timeline = json.loads((output / "05_virtual_reader_and_player" / "ab_staged_player_timeline.json").read_text(encoding="utf-8"))
        self.assertTrue(report["final_passed"])
        self.assertTrue((output / "00_device_interface_conformance" / "universal_device_interface_conformance_report.json").exists())
        self.assertTrue(relay["passed"])
        self.assertTrue((output / "04_reader_to_printer" / "reader_to_printer_fault_probe.json").exists())
        self.assertTrue((output / "07_action_level_device_channels" / "pc_to_reader" / "pc_to_reader_action_transcript.json").exists())
        self.assertTrue((output / "02_pc_to_printer" / "pc_to_printer_action_transcript.json").exists())
        self.assertTrue((output / "05_virtual_reader_and_player" / "player_to_pc_feedback.json").exists())
        self.assertTrue((output / "08_mechanical_optical_player" / "mechanical_optical_player_report.json").exists())
        self.assertEqual(relay["capture_count"], 3)
        self.assertTrue(timeline)
        self.assertTrue(all(row["section_verified_before_display"] for row in timeline))
        self.assertTrue(all(row["physical_transition_authorized"] is False for row in timeline))


if __name__ == "__main__":
    unittest.main(verbosity=2)
