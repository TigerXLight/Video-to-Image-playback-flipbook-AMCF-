from __future__ import annotations

import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_player_pc_runtime import (  # noqa: E402
    build_player_profile,
    check_package_compatibility,
    run_simulated_player_session,
    write_player_pc_runtime_demo,
)
from amcf_software_io_fixtures import load_fixture_bundle  # noqa: E402


class AMCFPlayerPCRuntimeFixtureTests(unittest.TestCase):
    def test_profile_uses_folded_indexed_carrier(self) -> None:
        profile = build_player_profile(load_fixture_bundle(PACKAGE))
        self.assertEqual(profile.carrier_layout, "folded_indexed_carrier")
        self.assertEqual(profile.seek_model, "local_buffer_seek_only")

    def test_package_compatibility_passes(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        compatible, diagnostics = check_package_compatibility(bundle, build_player_profile(bundle))
        self.assertTrue(compatible)
        self.assertEqual(diagnostics, [])

    def test_unsupported_seek_model_fails_compatibility(self) -> None:
        bundle = load_fixture_bundle(PACKAGE)
        changed = deepcopy(bundle)
        changed["player_profile"]["seek_model"] = "arbitrary_physical_seek"
        compatible, diagnostics = check_package_compatibility(changed, build_player_profile(changed))
        self.assertFalse(compatible)
        self.assertIn("unsupported_seek_model", diagnostics)

    def test_session_denies_arbitrary_seek(self) -> None:
        report = run_simulated_player_session(load_fixture_bundle(PACKAGE))
        arbitrary = [item for item in report.command_transcript if item.command == "arbitrary_seek"][0]
        self.assertFalse(arbitrary.accepted)
        self.assertEqual(report.unsafe_acceptance_count, 0)

    def test_session_uses_no_real_transport(self) -> None:
        report = run_simulated_player_session(load_fixture_bundle(PACKAGE))
        self.assertFalse(report.usb_used)
        self.assertFalse(report.serial_used)
        self.assertFalse(report.firmware_protocol_used)
        self.assertFalse(report.hardware_detection_used)

    def test_demo_outputs_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = write_player_pc_runtime_demo(PACKAGE, tmp)
            self.assertTrue(result["report"]["final_passed"])
            root = Path(tmp)
            self.assertTrue((root / "player_pc_session_report.json").exists())
            self.assertTrue((root / "player_command_transcript.json").exists())
            self.assertTrue((root / "player_capability_profile.json").exists())
            self.assertTrue((root / "PLAYER_PC_RUNTIME_FIXTURE_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
