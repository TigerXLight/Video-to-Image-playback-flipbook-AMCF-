from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_cross_corridor_roundtrip import (  # noqa: E402
    run_cross_corridor_roundtrip,
    write_cross_corridor_roundtrip_demo,
)


class AMCFCrossCorridorRoundtripTests(unittest.TestCase):
    def test_roundtrip_final_passed(self) -> None:
        report = run_cross_corridor_roundtrip(PACKAGE)["roundtrip_report"]
        self.assertTrue(report["final_passed"])

    def test_roundtrip_exercises_all_corridors(self) -> None:
        report = run_cross_corridor_roundtrip(PACKAGE)["roundtrip_report"]
        self.assertTrue(report["print_layout_passed"])
        self.assertTrue(report["reader_recovery_passed"])
        self.assertTrue(report["player_session_passed"])
        self.assertTrue(report["cross_corridor_report_passed"])

    def test_roundtrip_unsafe_acceptance_zero(self) -> None:
        report = run_cross_corridor_roundtrip(PACKAGE)["roundtrip_report"]
        self.assertEqual(report["unsafe_acceptance_count"], 0)

    def test_roundtrip_claim_flags_false(self) -> None:
        report = run_cross_corridor_roundtrip(PACKAGE)["roundtrip_report"]
        for value in report["claim_boundary_flags"].values():
            self.assertFalse(value)

    def test_demo_outputs_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = write_cross_corridor_roundtrip_demo(PACKAGE, tmp)
            self.assertTrue(result["roundtrip_report"]["final_passed"])
            root = Path(tmp)
            self.assertTrue((root / "cross_corridor_roundtrip_report.json").exists())
            self.assertTrue((root / "roundtrip_component_reports.json").exists())
            self.assertTrue((root / "CROSS_CORRIDOR_ROUNDTRIP_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
