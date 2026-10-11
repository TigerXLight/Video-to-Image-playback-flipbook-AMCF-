from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_digital_encoder import encode_source_frames  # noqa: E402
from amcf_digital_validator import validate_amcf_archive  # noqa: E402
from amcf_mechanical_optical_player import (  # noqa: E402
    MechanicalOpticalPlayerConfig,
    MechanicalOpticalPlayerSimulator,
    simulate_mechanical_optical_playback,
    validate_mechanical_optical_player_timeline,
)
from amcf_physical_carrier import generate_physical_carrier_from_amcf_archive, validate_physical_carrier_package  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class MechanicalOpticalPlayerSimulatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_player_"))
        self.source_root = self.tmp / "source_frames"
        self.archive = self.tmp / "sample_video_source.amcf.zip"
        self.carrier_root = self.tmp / "carrier_package"
        self.sim_root = self.tmp / "simulation"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def make_carrier(self) -> None:
        generate_source_frames(self.source_root)
        encode_source_frames(self.source_root / "source_frames_manifest.json", self.archive)
        self.assertTrue(validate_amcf_archive(self.archive)["ok"])
        generate_physical_carrier_from_amcf_archive(self.archive, self.carrier_root)
        self.assertTrue(validate_physical_carrier_package(self.carrier_root)["ok"])

    def test_source_frames_generate(self) -> None:
        self.assertEqual(generate_source_frames(self.source_root)["frame_count"], 8)

    def test_amcf_archive_creates_and_validates(self) -> None:
        self.make_carrier()
        self.assertTrue(validate_amcf_archive(self.archive)["ok"])

    def test_physical_carrier_package_creates_and_validates(self) -> None:
        self.make_carrier()
        self.assertTrue(validate_physical_carrier_package(self.carrier_root)["ok"])

    def test_player_simulator_loads_valid_carrier_package(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator()
        loaded = player.load_carrier(self.carrier_root)
        self.assertTrue(loaded["ok"], loaded["errors"])
        self.assertEqual(player.state.section_count, 8)

    def test_play_timeline_covers_expected_section_count(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator()
        player.load_carrier(self.carrier_root)
        states = player.play()
        self.assertEqual(len(states), 8)

    def test_pause_produces_stable_view_gate_state(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator()
        player.load_carrier(self.carrier_root)
        state = player.pause()
        self.assertEqual(state.command, "pause")
        self.assertEqual(state.section_index, 0)
        self.assertTrue(state.alignment_ok)

    def test_step_forward_advances_one_section(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator()
        player.load_carrier(self.carrier_root)
        self.assertEqual(player.step_forward().section_index, 1)

    def test_step_backward_moves_back_one_section(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator()
        player.load_carrier(self.carrier_root)
        player.seek_to_section(3)
        self.assertEqual(player.step_backward().section_index, 2)

    def test_seek_to_section_reaches_requested_section(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator()
        player.load_carrier(self.carrier_root)
        self.assertEqual(player.seek_to_section(5).section_index, 5)

    def test_reverse_traverses_in_reverse_order(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator()
        player.load_carrier(self.carrier_root)
        player.seek_to_section(4)
        states = player.reverse()
        self.assertEqual([state.section_index for state in states], [4, 3, 2, 1, 0])

    def test_view_gate_states_include_expected_fields(self) -> None:
        self.make_carrier()
        result = simulate_mechanical_optical_playback(self.carrier_root, self.sim_root)
        self.assertTrue(result["ok"])
        states = json.loads((self.sim_root / "view_gate_states.json").read_text(encoding="utf-8"))
        first = states[0]
        for key in (
            "section_index",
            "update_timestamp_ms",
            "current_gate_section",
            "next_staging_section",
            "preload_queue",
            "view_gate_state",
            "hidden_gate_state",
            "transition_blank_ms",
            "reader_prefetch_ahead_ms",
            "section_verified_before_display",
            "reverse_buffer_depth",
            "alignment_error",
            "alignment_ok",
            "illumination_on",
            "visible_payload_reference",
        ):
            self.assertIn(key, first)
        self.assertEqual(first["current_gate_section"], 0)
        self.assertEqual(first["next_staging_section"], 1)
        self.assertEqual(first["view_gate_state"], "visible_locked")
        self.assertEqual(first["hidden_gate_state"], "preloaded_verified")

    def test_timeline_uses_dynamic_ab_staging_fields(self) -> None:
        self.make_carrier()
        simulate_mechanical_optical_playback(self.carrier_root, self.sim_root)
        timeline = json.loads((self.sim_root / "player_timeline.json").read_text(encoding="utf-8"))
        self.assertEqual(timeline["preferred_future_mechanism"], "dynamic_folded_path_ab_staged_indexed_section_player")
        self.assertTrue(timeline["not_fixed_fps_page_machine"])
        self.assertIn("folded indexed transport", timeline["physical_playback_path"])
        self.assertEqual(timeline["transport_mode"], "dynamic_folded_path_ab_staged_indexed_transport")
        self.assertEqual(len(timeline["dynamic_update_schedule_ms"]), 8)
        self.assertGreater(timeline["transition_blank_ms"], 0)
        self.assertGreater(timeline["reader_prefetch_ahead_ms"], 0)
        self.assertGreater(timeline["reverse_buffer_depth"], 0)
        self.assertTrue(timeline["fail_closed_on_unverified_next_section"])

    def test_validator_passes_valid_playback_timeline(self) -> None:
        self.make_carrier()
        simulate_mechanical_optical_playback(self.carrier_root, self.sim_root)
        result = validate_mechanical_optical_player_timeline(self.sim_root / "player_timeline.json")
        self.assertTrue(result["ok"], result["errors"])

    def test_simulator_rejects_missing_section(self) -> None:
        self.make_carrier()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        (self.carrier_root / manifest["sections"][0]["section_file"]).unlink()
        player = MechanicalOpticalPlayerSimulator()
        loaded = player.load_carrier(self.carrier_root)
        self.assertFalse(loaded["ok"])

    def test_simulator_rejects_tampered_section_hash_mismatch(self) -> None:
        self.make_carrier()
        manifest = json.loads((self.carrier_root / "physical_carrier_manifest.json").read_text(encoding="utf-8"))
        section_path = self.carrier_root / manifest["sections"][0]["section_file"]
        section_path.write_text(section_path.read_text(encoding="utf-8") + "\nTAMPER\n", encoding="utf-8")
        player = MechanicalOpticalPlayerSimulator()
        loaded = player.load_carrier(self.carrier_root)
        self.assertFalse(loaded["ok"])

    def test_simulator_rejects_missing_required_lane(self) -> None:
        self.make_carrier()
        manifest_path = self.carrier_root / "physical_carrier_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["sections"][0]["lanes"].pop("payload_lane")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        player = MechanicalOpticalPlayerSimulator()
        loaded = player.load_carrier(self.carrier_root)
        self.assertFalse(loaded["ok"])

    def test_simulator_rejects_misalignment_beyond_tolerance(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator(MechanicalOpticalPlayerConfig(forced_alignment_errors={0: 1.0}))
        self.assertTrue(player.load_carrier(self.carrier_root)["ok"])
        state = player.pause()
        self.assertEqual(state.decision, "rejected_fail_closed")
        self.assertTrue(player.state.fail_closed)

    def test_simulator_fail_closes_when_next_staging_section_is_unverified(self) -> None:
        self.make_carrier()
        player = MechanicalOpticalPlayerSimulator(MechanicalOpticalPlayerConfig(unverified_sections=[1]))
        self.assertTrue(player.load_carrier(self.carrier_root)["ok"])
        state = player.play()[0]
        self.assertEqual(state.decision, "rejected_fail_closed")
        self.assertIn("next_staging_section_unverified", state.issues)
        self.assertTrue(player.state.fail_closed)

    def test_no_physical_or_hardware_or_screen_claims_are_made(self) -> None:
        self.make_carrier()
        simulate_mechanical_optical_playback(self.carrier_root, self.sim_root)
        timeline = json.loads((self.sim_root / "player_timeline.json").read_text(encoding="utf-8"))
        boundary = timeline["claim_boundary"]
        self.assertFalse(boundary["real_physical_playback_claimed"])
        self.assertFalse(boundary["digital_screen_physical_player_claimed"])
        self.assertFalse(boundary["physical_proof_claimed"])
        self.assertFalse(boundary["hardware_validation_claimed"])
        self.assertFalse(boundary["final_ui_claimed"])
        self.assertFalse(boundary["physical_prototype_built"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
