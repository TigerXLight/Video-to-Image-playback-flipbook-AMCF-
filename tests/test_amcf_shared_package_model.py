from __future__ import annotations

import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_shared_package_model import (  # noqa: E402
    CLAIM_BOUNDARY_FLAGS,
    REQUIRED_SECTION_LANES,
    AMCFManifest,
    AMCFPackage,
    build_demo_shared_package,
    validate_shared_package,
    write_demo_shared_package,
)


class AMCFSharedPackageModelTests(unittest.TestCase):
    def test_demo_package_has_required_sections(self) -> None:
        package = build_demo_shared_package()
        self.assertEqual(package.manifest.section_count, 3)
        self.assertEqual(len(package.manifest.update_events), 3)

    def test_each_section_has_required_lanes(self) -> None:
        package = build_demo_shared_package()
        for section in package.manifest.physical_sections:
            self.assertEqual(set(REQUIRED_SECTION_LANES).issubset(section.lanes), True)

    def test_validation_passes_demo_package(self) -> None:
        report = validate_shared_package(build_demo_shared_package())
        self.assertTrue(report.final_passed)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_validation_fails_duplicate_section_id(self) -> None:
        package = build_demo_shared_package()
        first = package.manifest.physical_sections[0]
        duplicate = replace(package.manifest.physical_sections[1], section_id=first.section_id)
        manifest = replace(package.manifest, physical_sections=[first, duplicate, package.manifest.physical_sections[2]])
        report = validate_shared_package(replace(package, manifest=manifest))
        self.assertFalse(report.final_passed)
        self.assertIn("duplicate_section_id", report.checks_failed)

    def test_validation_fails_missing_lane(self) -> None:
        package = build_demo_shared_package()
        section = package.manifest.physical_sections[0]
        lanes = dict(section.lanes)
        lanes.pop("checksum_hash_lane")
        changed = replace(section, lanes=lanes)
        manifest = replace(package.manifest, physical_sections=[changed, *package.manifest.physical_sections[1:]])
        report = validate_shared_package(replace(package, manifest=manifest))
        self.assertFalse(report.final_passed)
        self.assertTrue(any(item.startswith("missing_required_lanes") for item in report.checks_failed))

    def test_claim_boundary_flags_false(self) -> None:
        report = validate_shared_package(build_demo_shared_package())
        self.assertEqual(report.claim_boundary_flags, CLAIM_BOUNDARY_FLAGS)
        self.assertFalse(report.claim_boundary_flags["hardware_validation_claimed"])
        self.assertFalse(report.claim_boundary_flags["physical_level_5_claimed"])
        self.assertFalse(report.claim_boundary_flags["manufactured_player_claimed"])

    def test_demo_outputs_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = write_demo_shared_package(tmp)
            self.assertTrue(result["validation_report"]["final_passed"])
            root = Path(tmp)
            self.assertTrue((root / "amcf_shared_package.json").exists())
            self.assertTrue((root / "amcf_shared_manifest.json").exists())
            self.assertTrue((root / "amcf_shared_package_validation_report.json").exists())
            self.assertTrue((root / "AMCF_SHARED_PACKAGE_MODEL_SUMMARY.md").exists())

    def test_no_printer_reader_player_runtime_types_created(self) -> None:
        self.assertNotIn("Printer", AMCFPackage.__name__)
        self.assertNotIn("Reader", AMCFManifest.__name__)


if __name__ == "__main__":
    unittest.main(verbosity=2)
