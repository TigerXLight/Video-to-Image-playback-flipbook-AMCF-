from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_adapters import run_physical_software_adapter_roundtrip  # noqa: E402


class AmcfPhysicalAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_physical_adapters_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_shared_contract_is_complete_and_fail_closed(self) -> None:
        output = self.tmp / "adapter_layer"
        result = run_physical_software_adapter_roundtrip(PACKAGE, output)
        report = result["report"]
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["hardware_connected"])
        self.assertFalse(report["real_driver_or_protocol_used"])
        self.assertFalse(report["physical_level_5_claimed"])
        self.assertFalse(report["manufactured_player_claimed"])
        self.assertEqual(len(report["adapter_results"]), 4)
        self.assertGreaterEqual(len(report["status_events"]), 8)
        self.assertFalse(report["feedback"]["display_allowed"])
        self.assertFalse(report["feedback"]["transition_allowed"])
        self.assertEqual(
            {item["corridor"] for item in report["adapter_results"]},
            {"shared_core", "pc_to_printer", "reader_to_pc", "pc_to_player"},
        )
        saved = json.loads((output / "physical_software_adapter_report.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["run_name"], report["run_name"])
        self.assertTrue((output / "PHYSICAL_SOFTWARE_ADAPTER_ROUNDTRIP_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
