from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any


CLAIM_STATUS_SOFTWARE_PROFILE = "software_control_profile_not_physical_validation"


@dataclass(frozen=True)
class AMCFMechanismProfile:
    profile_id: str
    display_name: str
    profile_family: str
    carrier_layout: str
    staging_model: str
    actuator_family: str
    gate_model: str
    prefetch_model: str
    reverse_model: str
    seek_model: str
    guide_model: str
    energy_support_model: str
    material_profile_model: str
    safety_model: str
    primary_use: str
    ranking_tier: str
    simulator_default: bool = False
    research_candidate: bool = False
    support_layer_only: bool = False
    hardware_validated: bool = False
    physical_level_5_claimed: bool = False
    claim_status: str = CLAIM_STATUS_SOFTWARE_PROFILE
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class AMCFMechanismProfileCapability:
    profile_id: str
    amcf_schedule_fit: int
    ab_staging_fit: int
    view_gate_stability_fit: int
    reader_prefetch_fit: int
    reverse_fit: int
    seek_fit: int
    fail_closed_fit: int
    tablet_form_factor_fit: int
    simulator_readiness: int
    hardware_uncertainty: int
    overall_score: int
    recommendation: str


@dataclass(frozen=True)
class AMCFMechanismProfileRanking:
    profiles_ranked: list[str]
    default_profile_id: str
    recommended_first_simulator_profile: str
    research_profiles: list[str]
    support_layer_profiles: list[str]
    experimental_profiles: list[str]
    hardware_validated_profiles: list[str]
    physical_level_5_claimed_profiles: list[str]
    warnings: list[str]


@dataclass(frozen=True)
class AMCFMechanismProfileClaimBoundary:
    software_control_profiles_only: bool = True
    physical_hardware_claimed: bool = False
    hardware_validation_claimed: bool = False
    physical_level_5_claimed: bool = False
    real_motor_validation_claimed: bool = False
    real_piezo_validation_claimed: bool = False
    real_carrier_validation_claimed: bool = False
    real_reverse_seek_hardware_claimed: bool = False
    manufacturing_readiness_claimed: bool = False
    energy_self_powering_claimed: bool = False


@dataclass(frozen=True)
class AMCFMechanismProfileComparisonReport:
    profile_count: int
    default_profile_id: str
    capabilities: list[AMCFMechanismProfileCapability]
    ranking: AMCFMechanismProfileRanking
    claim_boundary: AMCFMechanismProfileClaimBoundary
    claim_boundary_passed: bool


def _profile(**kwargs: Any) -> AMCFMechanismProfile:
    defaults = {
        "energy_support_model": "none",
        "material_profile_model": "parameterized_thin_section_carrier",
        "safety_model": "fail_closed_required",
        "primary_use": "mechanism_profile_comparison",
        "notes": (),
    }
    defaults.update(kwargs)
    return AMCFMechanismProfile(**defaults)


def folded_ab_motor_encoder_baseline() -> AMCFMechanismProfile:
    return _profile(
        profile_id="folded_ab_motor_encoder_baseline",
        display_name="Folded A/B Motor Encoder Baseline",
        profile_family="primary_baseline",
        carrier_layout="folded_indexed_carrier",
        staging_model="abstract_ab_staging",
        actuator_family="motor_encoder",
        gate_model="single_visible_gate_plus_hidden_staging",
        prefetch_model="reader_prefetch_ahead",
        reverse_model="limited_reverse_buffer",
        seek_model="local_buffer_seek_only",
        guide_model="edge_guides_and_stop_gates",
        primary_use="default_simulator_control_profile",
        ranking_tier="rank_1_primary",
        simulator_default=True,
        claim_status=CLAIM_STATUS_SOFTWARE_PROFILE,
    )


def folded_ab_inchworm_research() -> AMCFMechanismProfile:
    return _profile(
        profile_id="folded_ab_inchworm_research",
        display_name="Folded A/B Inchworm Research Candidate",
        profile_family="research_actuator_candidate",
        carrier_layout="folded_indexed_carrier",
        staging_model="abstract_ab_staging",
        actuator_family="piezo_electrostatic_inchworm",
        gate_model="single_visible_gate_plus_hidden_staging_or_dual_gate_candidate",
        prefetch_model="reader_prefetch_ahead",
        reverse_model="limited_reverse_buffer",
        seek_model="local_buffer_seek_only",
        guide_model="clamp_step_release_guides",
        energy_support_model="piezo_charge_recovery_optional_support_only",
        primary_use="amcf_index_like_research_profile",
        ranking_tier="rank_2_research",
        research_candidate=True,
        claim_status="research_candidate_not_physical_validation",
    )


def two_track_ab_shuttle_candidate() -> AMCFMechanismProfile:
    return _profile(
        profile_id="two_track_ab_shuttle_candidate",
        display_name="Two-Track A/B Shuttle Candidate",
        profile_family="layout_candidate",
        carrier_layout="two_track_shuttle",
        staging_model="ab_double_buffered_tracks",
        actuator_family="motor_encoder_or_piezo_candidate",
        gate_model="dual_track_visible_hidden_candidate",
        prefetch_model="reader_prefetch_ahead",
        reverse_model="limited_reverse_buffer",
        seek_model="local_buffer_seek_only",
        guide_model="track_guides_and_stop_gates",
        ranking_tier="rank_3_secondary",
        research_candidate=True,
        claim_status="layout_candidate_not_physical_validation",
    )


def cartridge_stack_shuttle_candidate() -> AMCFMechanismProfile:
    return _profile(
        profile_id="cartridge_stack_shuttle_candidate",
        display_name="Cartridge Stack Shuttle Candidate",
        profile_family="layout_candidate",
        carrier_layout="indexed_section_stack",
        staging_model="stack_to_hidden_staging_shuttle",
        actuator_family="motor_encoder_shuttle",
        gate_model="single_visible_gate_plus_hidden_staging",
        prefetch_model="reader_prefetch_ahead",
        reverse_model="limited_reverse_or_reselect_required",
        seek_model="local_buffer_or_reselect_future",
        guide_model="stack_guides_and_stop_gates",
        ranking_tier="rank_4_secondary_prototype",
        research_candidate=True,
        claim_status="prototype_candidate_not_physical_validation",
    )


def chain_indexed_carrier_research() -> AMCFMechanismProfile:
    return _profile(
        profile_id="chain_indexed_carrier_research",
        display_name="Chain Indexed Carrier Research Candidate",
        profile_family="research_layout_candidate",
        carrier_layout="chain_indexed_carrier",
        staging_model="chain_positioned_ab_staging",
        actuator_family="motor_encoder_chain_drive",
        gate_model="view_gate_with_chain_flattening_requirement",
        prefetch_model="reader_prefetch_ahead",
        reverse_model="limited_chain_reverse_candidate",
        seek_model="local_buffer_seek_only",
        guide_model="chain_guides_stop_gates_and_flattening",
        ranking_tier="rank_5_research",
        research_candidate=True,
        claim_status="research_candidate_not_physical_validation",
    )


def spring_governor_brake_comparison() -> AMCFMechanismProfile:
    return _profile(
        profile_id="spring_governor_brake_comparison",
        display_name="Spring Governor Brake Comparison",
        profile_family="mechanical_comparison",
        carrier_layout="folded_indexed_carrier_or_cartridge_stack",
        staging_model="latched_indexed_staging",
        actuator_family="constant_force_spring_governor_brake",
        gate_model="single_visible_gate_plus_hidden_staging",
        prefetch_model="reader_prefetch_ahead",
        reverse_model="limited_reverse_only",
        seek_model="not_default",
        guide_model="brake_latch_stop_gate_support",
        ranking_tier="rank_6_comparison",
        research_candidate=True,
        claim_status="mechanical_comparison_not_physical_validation",
    )


def magnetic_guided_clamp_support() -> AMCFMechanismProfile:
    return _profile(
        profile_id="magnetic_guided_clamp_support",
        display_name="Magnetic Guided Clamp Support",
        profile_family="support_layer",
        carrier_layout="not_primary_transport",
        staging_model="supports_ab_staging",
        actuator_family="not_primary_actuator",
        gate_model="guide_clamp_stop_gate_support",
        prefetch_model="supports_reader_prefetch_alignment",
        reverse_model="supports_limited_reverse_alignment",
        seek_model="support_only",
        guide_model="magnetic_electrostatic_or_mechanical_guides",
        material_profile_model="not_primary_material_profile",
        primary_use="support_layer_only",
        ranking_tier="support_layer",
        support_layer_only=True,
        claim_status="support_layer_not_physical_validation",
    )


def energy_recovery_support_layer() -> AMCFMechanismProfile:
    return _profile(
        profile_id="energy_recovery_support_layer",
        display_name="Energy Recovery Support Layer",
        profile_family="support_layer",
        carrier_layout="not_primary_transport",
        staging_model="not_primary_staging",
        actuator_family="not_primary_actuator",
        gate_model="not_primary_gate",
        prefetch_model="none",
        reverse_model="none",
        seek_model="none",
        guide_model="none",
        energy_support_model="electret_triboelectric_piezo_or_regenerative_recovery_support_only",
        material_profile_model="not_primary_material_profile",
        primary_use="support_layer_only",
        ranking_tier="support_layer",
        support_layer_only=True,
        claim_status="energy_support_only_not_power_solution_not_validation",
        notes=("Energy recovery is a support comparison only, not a transport and not a power-sufficiency claim.",),
    )


def soft_actuator_experimental_branch() -> AMCFMechanismProfile:
    return _profile(
        profile_id="soft_actuator_experimental_branch",
        display_name="Soft Actuator Experimental Branch",
        profile_family="experimental_research",
        carrier_layout="future_material_integrated_candidate",
        staging_model="experimental",
        actuator_family="dielectric_elastomer_hasel_electroactive_paper",
        gate_model="experimental",
        prefetch_model="reader_prefetch_required_if_ever_used",
        reverse_model="unresolved",
        seek_model="unresolved",
        guide_model="unresolved",
        ranking_tier="rank_9_experimental",
        research_candidate=True,
        claim_status="experimental_branch_not_physical_validation",
    )


def material_aligned_carrier_branch() -> AMCFMechanismProfile:
    return _profile(
        profile_id="material_aligned_carrier_branch",
        display_name="Material-Aligned Carrier Branch",
        profile_family="material_profile_branch",
        carrier_layout="thin_section_carrier_material_branch",
        staging_model="supports_future_folded_carrier_if_validated",
        actuator_family="not_actuator",
        gate_model="material_support_for_view_gate",
        prefetch_model="marker_colour_lane_support",
        reverse_model="material_dependent",
        seek_model="material_dependent",
        guide_model="material_dependent",
        material_profile_model="nanocellulose_bacterial_cellulose_cnc_or_hybrid_laminate_candidate",
        primary_use="material_profile_comparison",
        ranking_tier="rank_10_material_branch",
        research_candidate=True,
        claim_status="material_branch_not_physical_validation",
    )


def all_mechanism_profiles() -> list[AMCFMechanismProfile]:
    return [
        folded_ab_motor_encoder_baseline(),
        folded_ab_inchworm_research(),
        two_track_ab_shuttle_candidate(),
        cartridge_stack_shuttle_candidate(),
        chain_indexed_carrier_research(),
        spring_governor_brake_comparison(),
        magnetic_guided_clamp_support(),
        energy_recovery_support_layer(),
        soft_actuator_experimental_branch(),
        material_aligned_carrier_branch(),
    ]


def default_mechanism_profile() -> AMCFMechanismProfile:
    return folded_ab_motor_encoder_baseline()


def profile_by_id(profile_id: str) -> AMCFMechanismProfile:
    for profile in all_mechanism_profiles():
        if profile.profile_id == profile_id:
            return profile
    raise KeyError(profile_id)


def score_profile_capability(profile: AMCFMechanismProfile) -> AMCFMechanismProfileCapability:
    table = {
        "folded_ab_motor_encoder_baseline": (5, 5, 5, 5, 4, 3, 5, 5, 5, 2, "recommended first simulator profile"),
        "folded_ab_inchworm_research": (5, 5, 4, 5, 4, 3, 5, 5, 3, 4, "research candidate only; actuator uncertainty remains"),
        "two_track_ab_shuttle_candidate": (4, 5, 4, 4, 3, 3, 5, 4, 3, 4, "layout candidate, not default"),
        "cartridge_stack_shuttle_candidate": (4, 4, 4, 4, 2, 2, 5, 4, 3, 4, "secondary prototype candidate"),
        "chain_indexed_carrier_research": (4, 3, 3, 4, 3, 2, 4, 2, 2, 5, "research candidate with flattening uncertainty"),
        "spring_governor_brake_comparison": (3, 3, 4, 3, 2, 1, 4, 4, 2, 5, "comparison profile only"),
        "magnetic_guided_clamp_support": (2, 3, 4, 3, 3, 1, 4, 4, 2, 3, "support layer only"),
        "energy_recovery_support_layer": (1, 1, 1, 1, 0, 0, 2, 3, 1, 5, "support layer only; not a transport or power-sufficiency claim"),
        "soft_actuator_experimental_branch": (2, 2, 2, 2, 1, 1, 3, 3, 1, 5, "experimental only"),
        "material_aligned_carrier_branch": (3, 2, 4, 3, 2, 1, 3, 4, 2, 4, "material branch only; not an actuator/default"),
    }
    values = table[profile.profile_id]
    raw_score = sum(values[:9]) - values[9]
    if profile.support_layer_only:
        raw_score = min(raw_score, 18)
    return AMCFMechanismProfileCapability(
        profile_id=profile.profile_id,
        amcf_schedule_fit=values[0],
        ab_staging_fit=values[1],
        view_gate_stability_fit=values[2],
        reader_prefetch_fit=values[3],
        reverse_fit=values[4],
        seek_fit=values[5],
        fail_closed_fit=values[6],
        tablet_form_factor_fit=values[7],
        simulator_readiness=values[8],
        hardware_uncertainty=values[9],
        overall_score=raw_score,
        recommendation=values[10],
    )


def rank_mechanism_profiles(profiles: list[AMCFMechanismProfile]) -> AMCFMechanismProfileRanking:
    capabilities = {cap.profile_id: cap for cap in [score_profile_capability(profile) for profile in profiles]}
    ordered = sorted(profiles, key=lambda item: (-capabilities[item.profile_id].overall_score, item.ranking_tier, item.profile_id))
    default_profiles = [profile.profile_id for profile in profiles if profile.simulator_default]
    hardware_validated = [profile.profile_id for profile in profiles if profile.hardware_validated]
    level5 = [profile.profile_id for profile in profiles if profile.physical_level_5_claimed]
    support_layers = [profile.profile_id for profile in profiles if profile.support_layer_only]
    warnings: list[str] = []
    if default_profiles != ["folded_ab_motor_encoder_baseline"]:
        warnings.append("default_profile_must_be_folded_ab_motor_encoder_baseline")
    if hardware_validated:
        warnings.append("hardware_validated_profiles_must_remain_empty")
    if level5:
        warnings.append("physical_level_5_claimed_profiles_must_remain_empty")
    if any(profile.simulator_default for profile in profiles if profile.support_layer_only):
        warnings.append("support_layers_must_not_be_simulator_default")
    return AMCFMechanismProfileRanking(
        profiles_ranked=[profile.profile_id for profile in ordered],
        default_profile_id=default_profiles[0] if default_profiles else "",
        recommended_first_simulator_profile="folded_ab_motor_encoder_baseline",
        research_profiles=[profile.profile_id for profile in profiles if profile.research_candidate],
        support_layer_profiles=support_layers,
        experimental_profiles=[profile.profile_id for profile in profiles if profile.profile_family == "experimental_research"],
        hardware_validated_profiles=hardware_validated,
        physical_level_5_claimed_profiles=level5,
        warnings=warnings,
    )


def default_mechanism_profile_claim_boundary() -> AMCFMechanismProfileClaimBoundary:
    return AMCFMechanismProfileClaimBoundary()


def validate_mechanism_claim_boundaries(profiles: list[AMCFMechanismProfile]) -> dict[str, Any]:
    failures: list[str] = []
    for profile in profiles:
        if profile.hardware_validated:
            failures.append(f"{profile.profile_id}:hardware_validated_true")
        if profile.physical_level_5_claimed:
            failures.append(f"{profile.profile_id}:physical_level_5_claimed_true")
    return {
        "software_control_profiles_only": True,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "physical_hardware_claimed": False,
        "energy_self_powering_claimed": False,
        "passed": not failures,
        "failures": failures,
    }


def build_mechanism_comparison_report(profiles: list[AMCFMechanismProfile]) -> AMCFMechanismProfileComparisonReport:
    return AMCFMechanismProfileComparisonReport(
        profile_count=len(profiles),
        default_profile_id=default_mechanism_profile().profile_id,
        capabilities=[score_profile_capability(profile) for profile in profiles],
        ranking=rank_mechanism_profiles(profiles),
        claim_boundary=default_mechanism_profile_claim_boundary(),
        claim_boundary_passed=validate_mechanism_claim_boundaries(profiles)["passed"],
    )


def mechanism_profile_to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, list):
        return [mechanism_profile_to_plain(item) for item in value]
    if isinstance(value, tuple):
        return [mechanism_profile_to_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: mechanism_profile_to_plain(item) for key, item in value.items()}
    return value
