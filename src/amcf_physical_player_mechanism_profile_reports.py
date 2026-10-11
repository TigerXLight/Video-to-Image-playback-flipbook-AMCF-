from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from amcf_physical_player_mechanism_profiles import (
    AMCFMechanismProfile,
    AMCFMechanismProfileRanking,
    build_mechanism_comparison_report as _build_mechanism_comparison_report,
    default_mechanism_profile_claim_boundary,
    mechanism_profile_to_plain,
    rank_mechanism_profiles,
    score_profile_capability,
    validate_mechanism_claim_boundaries,
)


def mechanism_profile_to_dict(profile: AMCFMechanismProfile) -> dict[str, Any]:
    return mechanism_profile_to_plain(profile)


def mechanism_profiles_to_dict(profiles: list[AMCFMechanismProfile]) -> list[dict[str, Any]]:
    return [mechanism_profile_to_dict(profile) for profile in profiles]


def build_mechanism_profile_ranking(profiles: list[AMCFMechanismProfile]) -> AMCFMechanismProfileRanking:
    return rank_mechanism_profiles(profiles)


def build_mechanism_claim_boundary_report(profiles: list[AMCFMechanismProfile]) -> dict[str, Any]:
    validation = validate_mechanism_claim_boundaries(profiles)
    boundary = default_mechanism_profile_claim_boundary()
    return {
        "software_control_profiles_only": boundary.software_control_profiles_only,
        "hardware_validation_claimed": boundary.hardware_validation_claimed,
        "physical_level_5_claimed": boundary.physical_level_5_claimed,
        "physical_hardware_claimed": boundary.physical_hardware_claimed,
        "real_motor_validation_claimed": boundary.real_motor_validation_claimed,
        "real_piezo_validation_claimed": boundary.real_piezo_validation_claimed,
        "real_carrier_validation_claimed": boundary.real_carrier_validation_claimed,
        "real_reverse_seek_hardware_claimed": boundary.real_reverse_seek_hardware_claimed,
        "manufacturing_readiness_claimed": boundary.manufacturing_readiness_claimed,
        "energy_self_powering_claimed": boundary.energy_self_powering_claimed,
        "hardware_validated_profiles": [profile.profile_id for profile in profiles if profile.hardware_validated],
        "physical_level_5_claimed_profiles": [profile.profile_id for profile in profiles if profile.physical_level_5_claimed],
        "passed": validation["passed"],
        "failures": validation["failures"],
    }


def build_mechanism_comparison_report(profiles: list[AMCFMechanismProfile]) -> dict[str, Any]:
    return mechanism_profile_to_plain(_build_mechanism_comparison_report(profiles))


def write_mechanism_profiles_json(profiles: list[AMCFMechanismProfile], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(mechanism_profiles_to_dict(profiles), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_mechanism_ranking_report(ranking: AMCFMechanismProfileRanking, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(mechanism_profile_to_plain(ranking), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_mechanism_claim_boundary_report(profiles: list[AMCFMechanismProfile], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_mechanism_claim_boundary_report(profiles), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_mechanism_comparison_markdown(profiles: list[AMCFMechanismProfile], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ranking = rank_mechanism_profiles(profiles)
    capability_by_id = {cap.profile_id: cap for cap in [score_profile_capability(profile) for profile in profiles]}
    lines = [
        "# AMCF Physical Player Mechanism Profile Comparison",
        "",
        "These are software/control mechanism profiles only. They are not physical validation and not manufactured hardware proof.",
        "",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- default profile: folded_ab_motor_encoder_baseline",
        "- piezo/inchworm: research candidate only",
        "- energy recovery: support layer only",
        "- soft actuators: experimental only",
        "- no profile is a manufactured hardware proof",
        "",
        "## Ranked Profiles",
        "",
    ]
    for profile_id in ranking.profiles_ranked:
        cap = capability_by_id[profile_id]
        lines.append(f"- `{profile_id}`: score {cap.overall_score}; {cap.recommendation}")
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "All profiles remain software/control contracts for future hardware comparison. No profile claims real motor validation, piezo validation, chain carrier validation, cartridge shuttle validation, folded-path validation, random-access physical seek, no-gap optical switching proof, or hardware validation.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
