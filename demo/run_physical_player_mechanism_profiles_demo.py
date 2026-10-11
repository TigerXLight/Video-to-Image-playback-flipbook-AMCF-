from __future__ import annotations

import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_player_mechanism_profile_reports import (  # noqa: E402
    build_mechanism_claim_boundary_report,
    build_mechanism_comparison_report,
    build_mechanism_profile_ranking,
    mechanism_profile_to_plain,
    write_mechanism_claim_boundary_report,
    write_mechanism_comparison_markdown,
    write_mechanism_profiles_json,
    write_mechanism_ranking_report,
)
from amcf_physical_player_mechanism_profiles import (  # noqa: E402
    all_mechanism_profiles,
    default_mechanism_profile,
    score_profile_capability,
)


def main() -> None:
    out = PACKAGE / "output" / "physical_player_mechanism_profiles_demo"
    out.mkdir(parents=True, exist_ok=True)

    profiles = all_mechanism_profiles()
    default_profile = default_mechanism_profile()
    ranking = build_mechanism_profile_ranking(profiles)
    capabilities = [score_profile_capability(profile) for profile in profiles]
    claim_report = build_mechanism_claim_boundary_report(profiles)
    comparison = build_mechanism_comparison_report(profiles)

    write_mechanism_profiles_json(profiles, out / "mechanism_profiles.json")
    (out / "mechanism_capability_scores.json").write_text(json.dumps(mechanism_profile_to_plain(capabilities), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_mechanism_ranking_report(ranking, out / "mechanism_ranking_report.json")
    write_mechanism_claim_boundary_report(profiles, out / "mechanism_claim_boundary_report.json")
    write_mechanism_comparison_markdown(profiles, out / "MECHANISM_PROFILE_COMPARISON.md")
    (out / "MECHANISM_PROFILE_SUMMARY.md").write_text(
        "\n".join(
            [
                "# AMCF Physical Player Mechanism Profile Summary",
                "",
                "These are deterministic software/control mechanism profiles for future physical-player comparison.",
                "",
                f"- profile count: {len(profiles)}",
                f"- default profile: {default_profile.profile_id}",
                f"- hardware_validated_profiles: {ranking.hardware_validated_profiles}",
                f"- physical_level_5_claimed_profiles: {ranking.physical_level_5_claimed_profiles}",
                f"- energy recovery support layer only: {str('energy_recovery_support_layer' in ranking.support_layer_profiles).lower()}",
                f"- piezo/inchworm research candidate only: {str('folded_ab_inchworm_research' in ranking.research_profiles).lower()}",
                "- hardware validation claimed: false",
                "- physical Level 5 claimed: false",
                "- manufactured hardware claimed: false",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "ok": True,
                "output_folder": str(out),
                "profile_count": len(profiles),
                "default_profile_id": default_profile.profile_id,
                "hardware_validated_profiles": ranking.hardware_validated_profiles,
                "physical_level_5_claimed_profiles": ranking.physical_level_5_claimed_profiles,
                "energy_recovery_support_layer_only": "energy_recovery_support_layer" in ranking.support_layer_profiles,
                "piezo_inchworm_research_candidate_only": "folded_ab_inchworm_research" in ranking.research_profiles,
                "mechanism_profile_report_passed": bool(claim_report["passed"] and comparison["claim_boundary_passed"]),
                "hardware_validation_claimed": False,
                "physical_level5_claimed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
