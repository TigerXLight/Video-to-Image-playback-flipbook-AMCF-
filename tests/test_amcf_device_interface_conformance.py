from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_device_interface_conformance import (  # noqa: E402
    build_universal_profile_templates,
    run_device_interface_conformance,
)


class DeviceInterfaceConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_device_conformance_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_templates_cover_all_universal_corridors(self) -> None:
        templates = build_universal_profile_templates()
        self.assertEqual(
            {item["corridor"] for item in templates["corridors"]},
            {"pc_to_printer", "reader_to_pc", "pc_to_player"},
        )
        self.assertFalse(templates["hardware_validation_claimed"])
        self.assertFalse(templates["physical_level_5_claimed"])

    def test_universal_conformance_passes_legacy_and_current_paths(self) -> None:
        output = self.tmp / "conformance"
        result = run_device_interface_conformance(PACKAGE, output)
        report = result["report"]
        self.assertTrue(report["final_passed"])
        self.assertTrue(report["manifest_contract"]["passed"])
        self.assertEqual(len(report["components"]), 7)
        self.assertTrue(all(item["final_passed"] for item in report["components"]))
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["hardware_connected"])
        self.assertFalse(report["physical_transition_authorized"])
        self.assertTrue((output / "universal_device_interface_conformance_report.json").exists())
        self.assertTrue((output / "universal_device_profile_templates.json").exists())

    def test_report_is_json_reopenable(self) -> None:
        output = self.tmp / "reopen"
        run_device_interface_conformance(PACKAGE, output)
        report = json.loads((output / "universal_device_interface_conformance_report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["run_name"], "AMCF_UNIVERSAL_DEVICE_INTERFACE_CONFORMANCE_V1")
        self.assertEqual(report["schema_version"], "amcf-universal-device-interface-conformance-v1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
