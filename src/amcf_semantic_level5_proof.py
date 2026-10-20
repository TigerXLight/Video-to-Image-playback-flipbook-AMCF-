from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


CLAIM_BOUNDARY_FLAGS = {
    "hardware_validation_claimed": False,
    "physical_level5_claimed": False,
    "manufactured_player_claimed": False,
    "real_sensor_validation_claimed": False,
    "real_motor_validation_claimed": False,
    "real_cartridge_validation_claimed": False,
    "physical_player_proof_claimed": False,
}


@dataclass(frozen=True)
class SemanticProofRun:
    run_name: str
    evidence_type: str
    frames_processed: int | None
    semantic_level5_claimed: bool
    proof_scope: str
    status: str
    local_run_timestamp: str
    notes: str


def semantic_proof_runs() -> list[SemanticProofRun]:
    return [
        SemanticProofRun(
            run_name="AMCF_TOOL_SEARCH_SEGMENTATION_TRACKING_SURVEY",
            evidence_type="tool_survey",
            frames_processed=None,
            semantic_level5_claimed=False,
            proof_scope="planning_only",
            status="READY_NO_LEVEL5_CLAIM",
            local_run_timestamp="20261009_162708",
            notes="Identified optional segmentation/tracking tools; no packages bundled in public core.",
        ),
        SemanticProofRun(
            run_name="AMCF_LOCAL_DEEP_SEMANTIC_TOOLCHAIN_INTEGRATION",
            evidence_type="toolchain_smoke",
            frames_processed=None,
            semantic_level5_claimed=False,
            proof_scope="local_optional_deep_tools",
            status="SMOKE_READY_NO_LEVEL5_CLAIM",
            local_run_timestamp="20261009_164833",
            notes="SAM2/CoTracker execution is available through the external-runtime deep-inference adapter; this historical row remains a pre-Level-5 smoke record.",
        ),
        SemanticProofRun(
            run_name="AMCF_DEEP_SEMANTIC_OBJECT_LEVEL5_RETRY_WITH_SAM2_COTRACKER",
            evidence_type="deep_bridge_retry",
            frames_processed=60,
            semantic_level5_claimed=False,
            proof_scope="level_4_99_deep_toolchain_bridge",
            status="NOT_LEVEL5",
            local_run_timestamp="20261009_170646",
            notes="Generated masks/tracks but did not pass semantic Level 5.",
        ),
        SemanticProofRun(
            run_name="AMCF_FULL_PROXY_DEEP_MASK_TRACK_BINDING_AND_LEVEL5_CLOSURE",
            evidence_type="full_proxy_mask_track_binding",
            frames_processed=402,
            semantic_level5_claimed=False,
            proof_scope="level_4_99_full_proxy_binding",
            status="NOT_LEVEL5",
            local_run_timestamp="20261009_171735",
            notes="Full proxy coverage and mask-track binding advanced, but Level 5 was not claimed.",
        ),
        SemanticProofRun(
            run_name="AMCF_HIGH_PRECISION_MASK_CLUSTER_AND_OBJECT_IDENTITY_PROMOTION",
            evidence_type="high_precision_cluster_validation",
            frames_processed=None,
            semantic_level5_claimed=False,
            proof_scope="level_4_99_high_precision_cluster_validation",
            status="NOT_LEVEL5",
            local_run_timestamp="20261009_173246",
            notes="High-precision clusters validated; lost/recovered evidence still missing.",
        ),
        SemanticProofRun(
            run_name="AMCF_LOST_RECOVERED_AND_FULL_SEMANTIC_CLOSURE",
            evidence_type="lost_recovered_candidate_review",
            frames_processed=None,
            semantic_level5_claimed=False,
            proof_scope="downgraded_after_visual_review",
            status="NOT_LEVEL5",
            local_run_timestamp="20261009_173643",
            notes="Automatic lost/recovered candidates were downgraded after review.",
        ),
        SemanticProofRun(
            run_name="AMCF_CONTROLLED_LOST_RECOVERED_LEVEL5_PROOF",
            evidence_type="controlled_canonical_semantic_object_proof",
            frames_processed=None,
            semantic_level5_claimed=True,
            proof_scope="controlled_canonical_vector_only",
            status="SEMANTIC_LEVEL5_ACCEPTED",
            local_run_timestamp="20261009_213727",
            notes="Controlled canonical lost/recovered proof accepted as semantic/object Level 5 for that vector.",
        ),
        SemanticProofRun(
            run_name="AMCF_HOOT_REAL_WORLD_LOST_RECOVERED_LEVEL5_SOLVER",
            evidence_type="dataset_annotated_real_world_occlusion_proof",
            frames_processed=54,
            semantic_level5_claimed=True,
            proof_scope="hoot_dataset_annotated_vector_only",
            status="SEMANTIC_LEVEL5_ACCEPTED",
            local_run_timestamp="20261009_220908",
            notes="Dataset-annotated HOOT real-world occlusion proof accepted for that specific vector.",
        ),
        SemanticProofRun(
            run_name="AMCF_LEVEL5_PROMOTION_MAIN_INTEGRATION_RELEASE_REFRESH",
            evidence_type="main_facing_promotion",
            frames_processed=None,
            semantic_level5_claimed=True,
            proof_scope="controlled_and_hoot_vectors_only",
            status="MAIN_AMCF_VNEXT_READY",
            local_run_timestamp="20261009_225757",
            notes="Promoted controlled and HOOT proof vectors into Main-facing vnext tooling.",
        ),
    ]


def accepted_semantic_level5_runs(runs: list[SemanticProofRun] | None = None) -> list[SemanticProofRun]:
    runs = runs or semantic_proof_runs()
    return [run for run in runs if run.semantic_level5_claimed and run.status in {"SEMANTIC_LEVEL5_ACCEPTED", "MAIN_AMCF_VNEXT_READY"}]


def build_semantic_level5_report() -> dict[str, Any]:
    runs = semantic_proof_runs()
    accepted = accepted_semantic_level5_runs(runs)
    rejected_or_parked = [run for run in runs if not run.semantic_level5_claimed]
    accepted_scopes = {run.proof_scope for run in accepted}
    final_passed = (
        len([run for run in accepted if run.status == "SEMANTIC_LEVEL5_ACCEPTED"]) == 2
        and "controlled_canonical_vector_only" in accepted_scopes
        and "hoot_dataset_annotated_vector_only" in accepted_scopes
        and not any(CLAIM_BOUNDARY_FLAGS.values())
    )
    return {
        "run_name": "AMCF_SEMANTIC_LEVEL5_PROOF_PARITY",
        "final_passed": final_passed,
        "semantic_level5_vector_count": 2,
        "accepted_semantic_level5_vectors": [asdict(run) for run in accepted if run.status == "SEMANTIC_LEVEL5_ACCEPTED"],
        "main_promotion_present": any(run.status == "MAIN_AMCF_VNEXT_READY" for run in accepted),
        "rejected_or_parked_pre_level5_runs": [asdict(run) for run in rejected_or_parked],
        "claim_boundary": CLAIM_BOUNDARY_FLAGS.copy(),
        "unsafe_acceptance_count": 0,
        "scope_note": "Semantic/object Level 5 is accepted only for the controlled canonical and HOOT dataset-annotated vectors. This is not physical Level 5, hardware validation, or a manufactured player claim.",
        "next_recommended_step": "Keep semantic proof vectors distinct from physical hardware and from future unapproved videos.",
    }


def write_semantic_level5_report(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_semantic_level5_report()
    (output_dir / "semantic_level5_proof_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# AMCF Semantic Level 5 Proof Summary",
        "",
        f"- final_passed: {report['final_passed']}",
        f"- semantic_level5_vector_count: {report['semantic_level5_vector_count']}",
        f"- main_promotion_present: {report['main_promotion_present']}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "",
        "Accepted semantic/object vectors:",
    ]
    for run in report["accepted_semantic_level5_vectors"]:
        lines.append(f"- {run['run_name']}: {run['proof_scope']}")
    (output_dir / "SEMANTIC_LEVEL5_PROOF_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report
