from __future__ import annotations

import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_print_layout import (  # noqa: E402
    build_print_layout_manifest,
    validate_print_layout,
    write_print_layout_demo,
)
from amcf_shared_package_model import REQUIRED_SECTION_LANES  # noqa: E402
from amcf_software_io_fixtures import load_fixture_bundle  # noqa: E402


class AMCFPCToPrinterLayoutTests(unittest.TestCase):
    def test_layout_builds_from_fixture(self) -> None:
        layout = build_print_layout_manifest(load_fixture_bundle(PACKAGE))
        self.assertEqual(len(layout.sections), 3)
        self.assertEqual(layout.sheet_size, "A4-abstract-mm")

    def test_each_section_has_all_lane_geometry(self) -> None:
        layout = build_print_layout_manifest(load_fixture_bundle(PACKAGE))
        for section in layout.sections:
            self.assertEqual({lane.lane_type for lane in section.lanes}, set(REQUIRED_SECTION_LANES))

    def test_layout_validation_passes(self) -> None:
        report = validate_print_layout(build_print_layout_manifest(load_fixture_bundle(PACKAGE)))
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)

    def test_layout_validation_fails_missing_lane(self) -> None:
        layout = build_print_layout_manifest(load_fixture_bundle(PACKAGE))
        first = layout.sections[0]
        changed = replace(first, lanes=first.lanes[:-1])
        report = validate_print_layout(replace(layout, sections=[changed, *layout.sections[1:]]))
        self.assertFalse(report["final_passed"])
        self.assertTrue(any(item.startswith("missing_layout_lane") for item in report["checks_failed"]))

    def test_no_real_printer_or_pdf_dependency_claimed(self) -> None:
        report = validate_print_layout(build_print_layout_manifest(load_fixture_bundle(PACKAGE)))
        self.assertTrue(report["no_hardware_printer_driver_used"])
        self.assertFalse(report["pdf_generation_used"])
        self.assertFalse(report["image_dependency_used"])
        self.assertFalse(report["barcode_dependency_used"])

    def test_demo_outputs_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = write_print_layout_demo(PACKAGE, tmp)
            self.assertTrue(result["report"]["final_passed"])
            root = Path(tmp)
            self.assertTrue((root / "print_layout_manifest.json").exists())
            self.assertTrue((root / "print_layout_report.json").exists())
            self.assertTrue((root / "PC_TO_PRINTER_LAYOUT_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
