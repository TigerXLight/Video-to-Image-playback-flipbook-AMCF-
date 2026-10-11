from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_io import (  # noqa: E402
    CARRIER_INDEXED_THIN_SECTION,
    DEVICE_PATH_PRINTER,
    DEVICE_PATH_READER_PC,
    LANE_CHECKSUM_HASH,
    LANE_COLOUR_REGISTRY,
    LANE_IMAGE_PAYLOAD,
    LANE_INDEX,
    LANE_METADATA,
    LANE_REGISTRATION,
    LANE_TIMING,
    REQUIRED_LANE_TYPES,
    STATUS_FAILED,
    STATUS_SIMULATED_ONLY,
    STATUS_WARNING,
    build_demo_physical_manifest,
    build_demo_player_device_profile,
    build_demo_printer_device_profile,
    build_demo_reader_device_profile,
    default_claim_boundary,
    default_lane_schema,
    default_material_profile,
    validate_physical_manifest,
    write_demo_physical_io_package,
)


class PhysicalIOArchitectureTests(unittest.TestCase):
    def test_default_material_profile_is_parameterized(self) -> None:
        profile = default_material_profile()
        self.assertEqual(profile.profile_confidence, STATUS_SIMULATED_ONLY)
        self.assertGreater(profile.thickness_um, 0)
        self.assertEqual(profile.claim_boundary.status, STATUS_SIMULATED_ONLY)

    def test_default_lane_schema_contains_required_lanes(self) -> None:
        lanes = {lane.lane_type for lane in default_lane_schema()}
        for lane_type in (
            LANE_TIMING,
            LANE_INDEX,
            LANE_REGISTRATION,
            LANE_IMAGE_PAYLOAD,
            LANE_COLOUR_REGISTRY,
            LANE_METADATA,
            LANE_CHECKSUM_HASH,
        ):
            self.assertIn(lane_type, lanes)

    def test_demo_manifest_uses_indexed_thin_section_carrier(self) -> None:
        manifest = build_demo_physical_manifest()
        self.assertEqual(manifest.carrier_type, CARRIER_INDEXED_THIN_SECTION)

    def test_demo_manifest_has_minimum_sections(self) -> None:
        manifest = build_demo_physical_manifest()
        self.assertGreaterEqual(len(manifest.sections), 3)

    def test_each_section_contains_required_lanes(self) -> None:
        manifest = build_demo_physical_manifest()
        for section in manifest.sections:
            lane_types = {lane.lane_type for lane in section.lanes}
            for lane_type in REQUIRED_LANE_TYPES:
                self.assertIn(lane_type, lane_types)

    def test_validation_passes_default_manifest_with_simulated_warning(self) -> None:
        report = validate_physical_manifest(build_demo_physical_manifest())
        self.assertEqual(report.validation_status, STATUS_WARNING)
        self.assertIn("material_profile_simulated_parameterized_not_measured", report.warnings)
        self.assertFalse(report.failures)

    def test_validation_fails_missing_required_lane(self) -> None:
        manifest = build_demo_physical_manifest()
        manifest.sections[0].lanes = [lane for lane in manifest.sections[0].lanes if lane.lane_type != LANE_TIMING]
        report = validate_physical_manifest(manifest)
        self.assertEqual(report.validation_status, STATUS_FAILED)
        self.assertTrue(any("missing_required_lanes" in failure for failure in report.failures))

    def test_validation_fails_section_count_mismatch(self) -> None:
        manifest = build_demo_physical_manifest()
        manifest.section_count = 999
        report = validate_physical_manifest(manifest)
        self.assertEqual(report.validation_status, STATUS_FAILED)
        self.assertIn("section_count_mismatch", report.failures)

    def test_printer_profile_is_export_only(self) -> None:
        profile = build_demo_printer_device_profile()
        self.assertEqual(profile.device_path_type, DEVICE_PATH_PRINTER)
        self.assertEqual(profile.profile_confidence, STATUS_SIMULATED_ONLY)
        self.assertFalse(profile.capabilities["real_printer_hardware_claimed"])
        self.assertFalse(profile.capabilities["real_print_accuracy_claimed"])

    def test_reader_profile_is_simulated(self) -> None:
        profile = build_demo_reader_device_profile()
        self.assertEqual(profile.device_path_type, DEVICE_PATH_READER_PC)
        self.assertEqual(profile.profile_confidence, STATUS_SIMULATED_ONLY)
        self.assertFalse(profile.capabilities["real_scanner_hardware_claimed"])
        self.assertFalse(profile.capabilities["real_scanner_validation_claimed"])

    def test_player_profile_is_folded_path_physical_optical(self) -> None:
        profile = build_demo_player_device_profile()
        self.assertIn("dynamic_folded_path_ab_staged", profile.capabilities["physical_optical_playback_concept"])
        self.assertEqual(profile.capabilities["visible_image_path"], "physical_optical")

    def test_player_profile_not_lcd_oled_playback_claim(self) -> None:
        profile = build_demo_player_device_profile()
        self.assertFalse(profile.capabilities["lcd_oled_screen_playback_as_physical_player"])

    def test_compression_policy_references_optional_tools_only(self) -> None:
        manifest = build_demo_physical_manifest()
        references = manifest.compression_policy["references_only_not_dependencies"]
        self.assertIn("CompressorJS", references)
        self.assertIn("UPNG.js", references)
        self.assertEqual(manifest.compression_policy["lossy_before_marker_hash_colour_decoding"], "disabled_by_default")

    def test_claim_boundary_no_hardware_validation(self) -> None:
        boundary = default_claim_boundary()
        self.assertIn("real_scanner_validation", boundary.not_claimed)
        self.assertIn("real_physical_playback_proof", boundary.not_claimed)
        self.assertIn("real_device_driver_integration", boundary.not_claimed)

    def test_demo_outputs_expected_files(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="amcf_physical_io_"))
        try:
            paths = write_demo_physical_io_package(tmp)
            for path in paths.values():
                self.assertTrue(Path(path).exists(), path)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_demo_script_creates_expected_output_files(self) -> None:
        output_dir = PACKAGE / "output" / "physical_io_architecture_demo"
        shutil.rmtree(output_dir, ignore_errors=True)
        result = subprocess.run(
            [sys.executable, str(PACKAGE / "demo" / "run_physical_io_architecture_demo.py")],
            cwd=PACKAGE,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for relative in (
            "shared/amcf_physical_manifest.json",
            "shared/material_profile.json",
            "shared/lane_schema.json",
            "shared/claim_boundary.json",
            "shared/physical_io_summary.md",
            "printer_path/printer_device_profile.json",
            "reader_path/reader_device_profile.json",
            "player_path/player_device_profile.json",
            "physical_validation_report.json",
            "README.md",
        ):
            self.assertTrue((output_dir / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main(verbosity=2)
