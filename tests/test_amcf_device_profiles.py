from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_device_profiles import (  # noqa: E402
    PROFILE_SCHEMA_VERSION,
    default_device_profile_bundle,
    load_device_profile_bundle,
    provider_selection_from_bundle,
    run_device_profile_validation,
    validate_device_profile_bundle,
)


class DeviceProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = PACKAGE

    def test_default_bundle_is_complete_and_safe(self) -> None:
        bundle = default_device_profile_bundle()
        report = validate_device_profile_bundle(bundle)
        self.assertEqual(bundle["schema_version"], PROFILE_SCHEMA_VERSION)
        self.assertTrue(report["final_passed"])
        self.assertEqual({item["corridor"] for item in report["profiles"]}, {"pc_to_printer", "reader_to_pc", "pc_to_player"})
        self.assertFalse(report["claim_boundary_flags"].get("hardware_validation_claimed", False))

    def test_default_profile_validation_runs_provider_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_device_profile_validation(self.repo_root, directory)
            report = result["report"]
            self.assertTrue(report["final_passed"])
            self.assertTrue(report["profile_validation"]["final_passed"])
            self.assertTrue(report["provider_discovery"]["final_passed"])
            self.assertFalse(report["hardware_connected"])
            self.assertEqual(report["unsafe_acceptance_count"], 0)
            self.assertTrue((Path(directory) / "device_profile_validation_report.json").exists())

    def test_example_bundle_loads_and_resolves_backends(self) -> None:
        path = self.repo_root / "profiles" / "amcf_device_profiles.example.json"
        bundle = load_device_profile_bundle(path)
        selection = provider_selection_from_bundle(bundle, self.repo_root)
        self.assertEqual(selection["printer_backend"], "file")
        self.assertEqual(selection["reader_backend"], "folder")
        self.assertEqual(selection["player_backend"], "loopback")
        self.assertFalse(selection["hardware_requested"])

    def test_hardware_profile_requires_explicit_cli_enable(self) -> None:
        bundle = default_device_profile_bundle()
        bundle["profiles"][0]["backend"] = "windows-spooler"
        bundle["profiles"][0]["hardware_requested"] = True
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "hardware_profile.json"
            profile_path.write_text(json.dumps(bundle), encoding="utf-8")
            result = run_device_profile_validation(self.repo_root, Path(directory) / "run", profile_path=profile_path)
            report = result["report"]
            self.assertFalse(report["final_passed"])
            self.assertFalse(report["hardware_connected"])
            self.assertEqual(report["unsafe_acceptance_count"], 0)
            reasons = {item["reason"] for item in report["provider_discovery"]["provider_probes"]}
            self.assertIn("hardware_not_enabled", reasons)

    def test_invalid_profile_is_rejected_before_provider_operation(self) -> None:
        bundle = default_device_profile_bundle()
        capabilities = list(bundle["profiles"][1]["capabilities"])
        capabilities.remove("hash_feedback")
        bundle["profiles"][1]["capabilities"] = capabilities
        report = validate_device_profile_bundle(bundle)
        self.assertFalse(report["final_passed"])
        self.assertIn("amcf-folder-reader-profile-v1:required_capabilities_missing", report["checks_failed"])

    def test_incomplete_profile_bundle_fails_closed_without_provider_resolution(self) -> None:
        bundle = default_device_profile_bundle()
        bundle["profiles"] = bundle["profiles"][:2]
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "incomplete_profile.json"
            profile_path.write_text(json.dumps(bundle), encoding="utf-8")
            result = run_device_profile_validation(self.repo_root, Path(directory) / "run", profile_path=profile_path)
            report = result["report"]
            self.assertFalse(report["final_passed"])
            self.assertIsNone(report["provider_discovery"])
            self.assertEqual(report["unsafe_acceptance_count"], 0)


if __name__ == "__main__":
    unittest.main()
