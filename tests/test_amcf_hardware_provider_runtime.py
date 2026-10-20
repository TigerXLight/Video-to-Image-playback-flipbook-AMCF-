from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_hardware_provider_runtime import run_hardware_provider_runtime  # noqa: E402


class AmcfHardwareProviderRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_provider_runtime_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_provider_handshake_is_ready_and_unverified_switch_is_blocked(self) -> None:
        output = self.tmp / "providers"
        result = run_hardware_provider_runtime(PACKAGE, output)
        report = result["report"]
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertEqual(len(report["provider_descriptors"]), 3)
        self.assertEqual(report["scheduled_event_count"], 3)
        self.assertTrue(report["unverified_switch_blocked"])
        self.assertFalse(report["hardware_connected"])
        self.assertFalse(report["real_driver_or_protocol_used"])
        self.assertFalse(report["direct_hardware_transition_authorized"])
        self.assertFalse(report["feedback"]["display_allowed"])
        self.assertFalse(report["feedback"]["transition_allowed"])
        self.assertTrue(all(item["accepted"] for item in report["reader_results"]))
        for name in (
            "hardware_provider_runtime_report.json",
            "hardware_provider_capabilities.json",
            "hardware_provider_status_events.json",
            "hardware_provider_feedback.json",
            "hardware_provider_command_transcript.json",
            "HARDWARE_PROVIDER_RUNTIME_SUMMARY.md",
        ):
            self.assertTrue((output / name).exists(), name)
        saved = json.loads((output / "hardware_provider_runtime_report.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["run_name"], report["run_name"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
