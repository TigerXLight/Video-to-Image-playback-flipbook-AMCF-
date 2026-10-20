from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_hardware_adapter_planning import run_hardware_adapter_plan  # noqa: E402


class AmcfHardwareAdapterPlanningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_hardware_plan_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_plan_is_complete_but_keeps_hardware_fail_closed(self) -> None:
        output = self.tmp / "hardware_plan"
        result = run_hardware_adapter_plan(PACKAGE, output)
        report = result["report"]
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertEqual(len(report["interface_specs"]), 3)
        self.assertTrue(report["software_baseline"]["final_passed"])
        self.assertFalse(report["hardware_connected"])
        self.assertFalse(report["real_driver_or_protocol_used"])
        self.assertFalse(report["physical_hardware_validation_claimed"])
        self.assertFalse(report["direct_hardware_transition_authorized"])
        self.assertFalse(report["feedback"]["display_allowed"])
        self.assertFalse(report["feedback"]["transition_allowed"])
        self.assertEqual(
            {spec["corridor"] for spec in report["interface_specs"]},
            {"pc_to_printer", "reader_to_pc", "pc_to_player"},
        )
        self.assertGreaterEqual(len(report["status_events"]), 6)
        for name in (
            "hardware_adapter_plan_report.json",
            "hardware_adapter_interface_specs.json",
            "hardware_adapter_capability_matrix.json",
            "hardware_adapter_status_events.json",
            "hardware_adapter_feedback.json",
            "HARDWARE_ADAPTER_PLANNING_SUMMARY.md",
        ):
            self.assertTrue((output / name).exists(), name)
        saved = json.loads((output / "hardware_adapter_plan_report.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["run_name"], report["run_name"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
