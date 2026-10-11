from __future__ import annotations

import sys
import unittest
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_mechanism_profile_reports import (  # noqa: E402
    build_mechanism_claim_boundary_report,
    build_mechanism_profile_ranking,
)
from amcf_physical_player_mechanism_profiles import (  # noqa: E402
    all_mechanism_profiles,
    default_mechanism_profile,
    profile_by_id,
    score_profile_capability,
)


REQUIRED_PROFILE_IDS = {
    "folded_ab_motor_encoder_baseline",
    "folded_ab_inchworm_research",
    "two_track_ab_shuttle_candidate",
    "cartridge_stack_shuttle_candidate",
    "chain_indexed_carrier_research",
    "spring_governor_brake_comparison",
    "magnetic_guided_clamp_support",
    "energy_recovery_support_layer",
    "soft_actuator_experimental_branch",
    "material_aligned_carrier_branch",
}


class PhysicalPlayerMechanismProfilesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profiles = all_mechanism_profiles()
        self.by_id = {profile.profile_id: profile for profile in self.profiles}

    def test_all_required_profile_ids_exist(self) -> None:
        self.assertEqual(set(self.by_id), REQUIRED_PROFILE_IDS)

    def test_exactly_one_profile_is_simulator_default_true(self) -> None:
        self.assertEqual([profile.profile_id for profile in self.profiles if profile.simulator_default], ["folded_ab_motor_encoder_baseline"])

    def test_default_profile_is_folded_ab_motor_encoder_baseline(self) -> None:
        self.assertEqual(default_mechanism_profile().profile_id, "folded_ab_motor_encoder_baseline")

    def test_default_profile_uses_folded_indexed_carrier(self) -> None:
        self.assertEqual(default_mechanism_profile().carrier_layout, "folded_indexed_carrier")

    def test_default_profile_uses_abstract_ab_staging(self) -> None:
        self.assertEqual(default_mechanism_profile().staging_model, "abstract_ab_staging")

    def test_default_profile_uses_motor_encoder(self) -> None:
        self.assertEqual(default_mechanism_profile().actuator_family, "motor_encoder")

    def test_default_profile_has_hardware_validated_false(self) -> None:
        self.assertFalse(default_mechanism_profile().hardware_validated)

    def test_default_profile_has_physical_level_5_claimed_false(self) -> None:
        self.assertFalse(default_mechanism_profile().physical_level_5_claimed)

    def test_piezo_inchworm_profile_is_research_candidate_true(self) -> None:
        self.assertTrue(profile_by_id("folded_ab_inchworm_research").research_candidate)

    def test_piezo_inchworm_profile_is_simulator_default_false(self) -> None:
        self.assertFalse(profile_by_id("folded_ab_inchworm_research").simulator_default)

    def test_two_track_shuttle_profile_is_candidate_not_default(self) -> None:
        profile = profile_by_id("two_track_ab_shuttle_candidate")
        self.assertTrue(profile.research_candidate)
        self.assertFalse(profile.simulator_default)

    def test_cartridge_stack_shuttle_profile_is_candidate_not_default(self) -> None:
        profile = profile_by_id("cartridge_stack_shuttle_candidate")
        self.assertTrue(profile.research_candidate)
        self.assertFalse(profile.simulator_default)

    def test_chain_indexed_carrier_profile_is_research_candidate_not_default(self) -> None:
        profile = profile_by_id("chain_indexed_carrier_research")
        self.assertTrue(profile.research_candidate)
        self.assertFalse(profile.simulator_default)

    def test_magnetic_guided_clamp_profile_is_support_layer_only_true(self) -> None:
        self.assertTrue(profile_by_id("magnetic_guided_clamp_support").support_layer_only)

    def test_energy_recovery_profile_is_support_layer_only_true(self) -> None:
        self.assertTrue(profile_by_id("energy_recovery_support_layer").support_layer_only)

    def test_energy_recovery_profile_is_not_a_transport_default(self) -> None:
        profile = profile_by_id("energy_recovery_support_layer")
        self.assertEqual(profile.carrier_layout, "not_primary_transport")
        self.assertFalse(profile.simulator_default)

    def test_soft_actuator_branch_is_experimental_research_and_not_default(self) -> None:
        profile = profile_by_id("soft_actuator_experimental_branch")
        self.assertEqual(profile.profile_family, "experimental_research")
        self.assertTrue(profile.research_candidate)
        self.assertFalse(profile.simulator_default)

    def test_material_branch_is_not_actuator_default(self) -> None:
        profile = profile_by_id("material_aligned_carrier_branch")
        self.assertEqual(profile.actuator_family, "not_actuator")
        self.assertFalse(profile.simulator_default)

    def test_hardware_validated_profiles_is_empty(self) -> None:
        ranking = build_mechanism_profile_ranking(self.profiles)
        self.assertEqual(ranking.hardware_validated_profiles, [])

    def test_physical_level_5_claimed_profiles_is_empty(self) -> None:
        ranking = build_mechanism_profile_ranking(self.profiles)
        self.assertEqual(ranking.physical_level_5_claimed_profiles, [])

    def test_claim_boundary_says_hardware_validation_claimed_false(self) -> None:
        report = build_mechanism_claim_boundary_report(self.profiles)
        self.assertFalse(report["hardware_validation_claimed"])

    def test_claim_boundary_says_energy_self_powering_claimed_false(self) -> None:
        report = build_mechanism_claim_boundary_report(self.profiles)
        self.assertFalse(report["energy_self_powering_claimed"])

    def test_ranking_recommends_folded_ab_motor_encoder_baseline_first(self) -> None:
        ranking = build_mechanism_profile_ranking(self.profiles)
        self.assertEqual(ranking.recommended_first_simulator_profile, "folded_ab_motor_encoder_baseline")
        self.assertEqual(ranking.profiles_ranked[0], "folded_ab_motor_encoder_baseline")

    def test_support_layers_do_not_outrank_primary_transport_profile(self) -> None:
        default_score = score_profile_capability(profile_by_id("folded_ab_motor_encoder_baseline")).overall_score
        for profile_id in ["magnetic_guided_clamp_support", "energy_recovery_support_layer"]:
            self.assertLess(score_profile_capability(profile_by_id(profile_id)).overall_score, default_score)


if __name__ == "__main__":
    unittest.main(verbosity=2)
