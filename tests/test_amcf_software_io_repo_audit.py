from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

import amcf_software_io_repo_audit as audit  # noqa: E402


class AMCFSoftwareIORepoAuditTests(unittest.TestCase):
    def test_audit_module_imports(self) -> None:
        self.assertEqual(audit.RUN_NAME, "AMCF_SOFTWARE_IO_REPO_AUDIT_V1")

    def test_classifier_recognises_shared_core_terms(self) -> None:
        item = audit.classify_file("src/amcf_manifest_schema.py", "AMCF package manifest update_event timing checksum report")
        self.assertIn("shared_amcf_core", item.categories)

    def test_classifier_recognises_printer_terms(self) -> None:
        item = audit.classify_file("docs/print_layout.md", "printer PDF SVG PNG sheet card strip registration colour hash")
        self.assertIn("pc_to_printer", item.categories)

    def test_classifier_recognises_reader_terms(self) -> None:
        item = audit.classify_file("src/reader_capture.py", "scanner scan capture lane marker registration recovery rescan")
        self.assertIn("pc_reader", item.categories)

    def test_classifier_recognises_player_terms(self) -> None:
        item = audit.classify_file("src/player_control.py", "player command capability protocol diagnostic audio_sync")
        self.assertIn("player_pc", item.categories)

    def test_classifier_recognises_physical_player_simulator_terms(self) -> None:
        item = audit.classify_file("src/amcf_physical_player_state_machine.py", "fail_closed reverse seek prefetch view_gate hidden_gate mechanism profile")
        self.assertIn("physical_player_simulator_control", item.categories)

    def test_classifier_recognises_report_audit_terms(self) -> None:
        item = audit.classify_file("demo/run_release_review.py", "final_passed unsafe_acceptance claim_boundary local_path generated_output hardware_claim")
        self.assertIn("reports_logs_audits", item.categories)

    def test_generated_output_paths_are_marked_generated(self) -> None:
        item = audit.classify_file("output/amcf_software_io_repo_audit/report.json", "manifest package report")
        self.assertTrue(item.is_generated_output)
        self.assertFalse(item.is_source_truth)
        self.assertEqual(item.categories, ["generated_output_ignored"])

    def test_output_is_not_source_truth(self) -> None:
        self.assertFalse(audit.is_source_truth_path("output/example.json"))

    def test_report_includes_final_passed(self) -> None:
        report = audit.build_report(PACKAGE)
        self.assertIn("final_passed", report)
        self.assertTrue(report["final_passed"])

    def test_report_includes_unsafe_acceptance_count_zero(self) -> None:
        report = audit.build_report(PACKAGE)
        self.assertEqual(report["unsafe_acceptance_count"], 0)

    def test_claim_boundary_flags_present_and_false(self) -> None:
        flags = audit.build_report(PACKAGE)["claim_boundary_flags"]
        for key in (
            "hardware_validation_claimed",
            "physical_level_5_claimed",
            "manufactured_player_claimed",
            "real_printer_required",
            "real_reader_required",
            "real_player_required",
            "real_scanner_required",
            "real_usb_required",
        ):
            self.assertIn(key, flags)
            self.assertFalse(flags[key])

    def test_no_hardware_validation_claimed(self) -> None:
        self.assertFalse(audit.build_report(PACKAGE)["claim_boundary_flags"]["hardware_validation_claimed"])

    def test_no_physical_level_5_claimed(self) -> None:
        self.assertFalse(audit.build_report(PACKAGE)["claim_boundary_flags"]["physical_level_5_claimed"])

    def test_no_manufactured_player_claimed(self) -> None:
        self.assertFalse(audit.build_report(PACKAGE)["claim_boundary_flags"]["manufactured_player_claimed"])

    def test_write_outputs_creates_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = audit.write_audit_outputs(tmp, PACKAGE)
            self.assertTrue(report["final_passed"])
            out = Path(tmp)
            self.assertTrue((out / "software_io_repo_audit_report.json").exists())
            self.assertTrue((out / "corridor_file_map.json").exists())
            self.assertTrue((out / "schema_discovery_report.json").exists())
            self.assertTrue((out / "SOFTWARE_IO_REPO_AUDIT_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
