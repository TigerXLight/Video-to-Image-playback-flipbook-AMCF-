from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from dataclasses import replace
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_player_pc_runtime import build_player_profile, check_package_compatibility, run_simulated_player_session  # noqa: E402
from amcf_print_layout import build_print_layout_manifest, validate_print_layout  # noqa: E402
from amcf_reader_recovery import recover_sections_from_fixture  # noqa: E402
from amcf_shared_package_model import build_demo_shared_package, validate_shared_package  # noqa: E402
from amcf_software_io_fixtures import load_fixture_bundle, validate_fixture_bundle  # noqa: E402


class AMCFCrossCorridorMutationSafetyTests(unittest.TestCase):
    def test_duplicate_section_id_rejected(self) -> None:
        package = build_demo_shared_package()
        first = package.manifest.physical_sections[0]
        duplicate = replace(package.manifest.physical_sections[1], section_id=first.section_id)
        manifest = replace(package.manifest, physical_sections=[first, duplicate, package.manifest.physical_sections[2]])
        report = validate_shared_package(replace(package, manifest=manifest))
        self.assertFalse(report.final_passed)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_missing_hash_lane_rejected(self) -> None:
        package = build_demo_shared_package()
        section = package.manifest.physical_sections[0]
        lanes = dict(section.lanes)
        lanes.pop("checksum_hash_lane")
        changed = replace(section, lanes=lanes)
        manifest = replace(package.manifest, physical_sections=[changed, *package.manifest.physical_sections[1:]])
        report = validate_shared_package(replace(package, manifest=manifest))
        self.assertFalse(report.final_passed)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_fixture_hash_mismatch_rejected(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        changed = deepcopy(bundle)
        changed["package"]["manifest"]["physical_sections"][0]["payload_hash"] = "bad-hash"
        report = validate_fixture_bundle(changed)
        self.assertFalse(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)

    def test_reader_hash_mismatch_not_displayed(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        changed = deepcopy(bundle)
        changed["reader_capture"]["simulated_captures"][0]["hash_status"] = "mismatch"
        report = recover_sections_from_fixture(changed)
        self.assertFalse(report.recovered_sections[0].display_allowed)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_reader_wrong_section_missing_capture_not_displayed(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        changed = deepcopy(bundle)
        changed["reader_capture"]["simulated_captures"] = changed["reader_capture"]["simulated_captures"][1:]
        report = recover_sections_from_fixture(changed)
        self.assertFalse(report.recovered_sections[0].display_allowed)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_unsupported_arbitrary_seek_denied(self) -> None:
        report = run_simulated_player_session(load_fixture_bundle(PACKAGE))
        arbitrary = [item for item in report.command_transcript if item.command == "arbitrary_seek"][0]
        self.assertFalse(arbitrary.accepted)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_manifest_mismatch_rejected_by_player_compatibility(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        changed = deepcopy(bundle)
        changed["package"]["manifest"]["section_count"] = 0
        compatible, diagnostics = check_package_compatibility(changed, build_player_profile(changed))
        self.assertFalse(compatible)
        self.assertIn("empty_manifest", diagnostics)

    def test_invalid_print_layout_rejected(self) -> None:
        layout = build_print_layout_manifest(load_fixture_bundle(PACKAGE))
        invalid = replace(layout, printer_safe_margin_mm=1.0)
        report = validate_print_layout(invalid)
        self.assertFalse(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
