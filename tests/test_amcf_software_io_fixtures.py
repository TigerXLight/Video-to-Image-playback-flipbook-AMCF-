from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_software_io_fixtures import (  # noqa: E402
    FIXTURE_VERSION,
    fixture_root,
    load_fixture_bundle,
    validate_fixture_bundle,
    write_fixture_report,
)


class AMCFSoftwareIOFixtureTests(unittest.TestCase):
    def test_fixture_root_exists(self) -> None:
        self.assertTrue(fixture_root(PACKAGE).exists())

    def test_fixture_bundle_loads(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        self.assertEqual(bundle["package"]["fixture_version"], FIXTURE_VERSION)
        self.assertEqual(bundle["reader_capture"]["fixture_version"], FIXTURE_VERSION)
        self.assertEqual(bundle["player_profile"]["fixture_version"], FIXTURE_VERSION)

    def test_fixture_bundle_validates(self) -> None:
        report = validate_fixture_bundle(load_fixture_bundle(PACKAGE))
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)

    def test_fixture_claim_flags_false(self) -> None:
        report = validate_fixture_bundle(load_fixture_bundle(PACKAGE))
        for value in report["claim_boundary_flags"].values():
            self.assertFalse(value)

    def test_reader_fixture_has_degraded_colour_warning_case(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        statuses = {capture["colour_status"] for capture in bundle["reader_capture"]["simulated_captures"]}
        self.assertIn("degraded_warning", statuses)

    def test_player_fixture_keeps_seek_bounded(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        self.assertEqual(bundle["player_profile"]["seek_model"], "local_buffer_seek_only")

    def test_demo_outputs_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = write_fixture_report(PACKAGE, tmp)
            self.assertTrue(report["final_passed"])
            root = Path(tmp)
            self.assertTrue((root / "fixture_regression_report.json").exists())
            self.assertTrue((root / "fixture_bundle_index.json").exists())
            self.assertTrue((root / "SOFTWARE_IO_FIXTURE_BASELINE_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
