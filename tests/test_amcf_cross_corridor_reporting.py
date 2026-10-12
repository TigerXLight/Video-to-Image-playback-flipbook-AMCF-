from __future__ import annotations

import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_cross_corridor_reporting import (  # noqa: E402
    CORRIDORS,
    build_claim_boundary_report,
    build_cross_corridor_report,
    build_safety_decision,
    write_demo_cross_corridor_report,
)
from amcf_shared_package_model import build_demo_shared_package  # noqa: E402


class AMCFCrossCorridorReportingTests(unittest.TestCase):
    def test_report_contains_all_corridors(self) -> None:
        report = build_cross_corridor_report()
        self.assertEqual([check.corridor for check in report.corridor_checks], list(CORRIDORS))

    def test_report_final_passed_for_demo_package(self) -> None:
        report = build_cross_corridor_report()
        self.assertTrue(report.final_passed)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_claim_boundary_flags_false(self) -> None:
        report = build_cross_corridor_report()
        for value in report.claim_boundary_flags.values():
            self.assertFalse(value)

    def test_claim_boundary_report_is_no_hardware(self) -> None:
        boundary = build_claim_boundary_report()
        self.assertFalse(boundary.hardware_validation_claimed)
        self.assertFalse(boundary.physical_level_5_claimed)
        self.assertFalse(boundary.manufactured_player_claimed)

    def test_safety_decision_does_not_create_unsafe_acceptance_for_safe_accept(self) -> None:
        decision = build_safety_decision(
            "decision-valid",
            "shared_core",
            "accepted",
            "valid_fixture",
            display_allowed=True,
            transition_allowed=True,
        )
        self.assertFalse(decision.unsafe_acceptance)

    def test_report_fails_for_invalid_shared_package(self) -> None:
        package = build_demo_shared_package()
        manifest = replace(package.manifest, section_count=99)
        report = build_cross_corridor_report(replace(package, manifest=manifest))
        self.assertFalse(report.final_passed)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_demo_outputs_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = write_demo_cross_corridor_report(tmp)
            self.assertTrue(result["report"]["final_passed"])
            root = Path(tmp)
            self.assertTrue((root / "cross_corridor_report.json").exists())
            self.assertTrue((root / "claim_boundary_report.json").exists())
            self.assertTrue((root / "safety_decisions.json").exists())
            self.assertTrue((root / "CROSS_CORRIDOR_REPORTING_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
