from __future__ import annotations

import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_reader_recovery import recover_sections_from_fixture, write_reader_recovery_demo  # noqa: E402
from amcf_software_io_fixtures import load_fixture_bundle  # noqa: E402


class AMCFReaderRecoveryFixtureTests(unittest.TestCase):
    def test_fixture_recovery_passes(self) -> None:
        report = recover_sections_from_fixture(load_fixture_bundle(PACKAGE))
        self.assertTrue(report.final_passed)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_degraded_colour_warns_but_allows_display(self) -> None:
        report = recover_sections_from_fixture(load_fixture_bundle(PACKAGE))
        degraded = [item for item in report.recovered_sections if item.colour_status == "degraded_warning"]
        self.assertEqual(len(degraded), 1)
        self.assertTrue(degraded[0].display_allowed)
        self.assertEqual(degraded[0].diagnostic, "accepted_with_colour_warning")

    def test_hash_mismatch_creates_reprint_request(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        changed = deepcopy(bundle)
        changed["reader_capture"]["simulated_captures"][0]["hash_status"] = "mismatch"
        report = recover_sections_from_fixture(changed)
        self.assertTrue(report.final_passed)
        self.assertEqual(report.unsafe_acceptance_count, 0)
        self.assertFalse(report.recovered_sections[0].display_allowed)
        self.assertEqual(report.diagnostic_requests[0].request_type, "reprint_request")

    def test_registration_failure_creates_rescan_request(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        changed = deepcopy(bundle)
        changed["reader_capture"]["simulated_captures"][0]["registration_status"] = "mismatch"
        report = recover_sections_from_fixture(changed)
        self.assertTrue(report.final_passed)
        self.assertFalse(report.recovered_sections[0].display_allowed)
        self.assertEqual(report.diagnostic_requests[0].request_type, "rescan_request")

    def test_no_scanner_or_image_processing_used(self) -> None:
        report = recover_sections_from_fixture(load_fixture_bundle(PACKAGE))
        self.assertFalse(report.scanner_api_used)
        self.assertFalse(report.image_processing_used)
        self.assertFalse(report.barcode_decoding_used)

    def test_demo_outputs_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = write_reader_recovery_demo(PACKAGE, tmp)
            self.assertTrue(result["report"]["final_passed"])
            root = Path(tmp)
            self.assertTrue((root / "reader_recovery_report.json").exists())
            self.assertTrue((root / "recovered_sections.json").exists())
            self.assertTrue((root / "reader_diagnostics.json").exists())
            self.assertTrue((root / "READER_RECOVERY_FIXTURE_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
