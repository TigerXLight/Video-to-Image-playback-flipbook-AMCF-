"""Fail-closed residual-stream accounting and visual gate from the 07E/07I trials."""

from __future__ import annotations

import math
from typing import Any


def _number(row: dict[str, Any], key: str) -> float:
    value = row[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"invalid {key}")
    return float(value)


def visual_gate(metric: dict[str, Any], fullrate_metric: dict[str, Any]) -> dict[str, Any]:
    """Apply the 07E thresholds; missing/invalid evidence is rejected."""
    reasons: list[str] = []
    required = ("frame_count_match", "fps_match", "resolution_match")
    if any(metric.get(key) is not True for key in required):
        reasons.append("technical mismatch")
    try:
        mae = _number(metric, "mae")
        psnr = _number(metric, "psnr")
        control_mae = _number(fullrate_metric, "mae")
        control_psnr = _number(fullrate_metric, "psnr")
        temporal = _number(metric, "temporal_difference_similarity")
        if min(mae, control_mae, temporal) < 0 or min(psnr, control_psnr) < 0:
            raise ValueError("negative metric")
    except (KeyError, ValueError):
        return {"status": "REJECTED", "human_review_required": False, "reasons": reasons + ["missing or invalid metric"]}

    if mae > max(4.0, control_mae + 1.5) or psnr < 36.0:
        reasons.append("metric regression")
    if reasons:
        return {"status": "REJECTED", "human_review_required": False, "reasons": reasons}
    if mae > control_mae + 0.5 or psnr < control_psnr - 1.0:
        reasons.append("near visual uncertainty")
    if abs(temporal - 1.0) > 0.05:
        reasons.append("temporal similarity uncertain")
    return {
        "status": "NEEDS_HUMAN_REVIEW" if reasons else "PASS",
        "human_review_required": bool(reasons),
        "reasons": reasons,
    }


def residual_accounting(compressed_bytes: int, fullrate_component_bytes: int, source_video_bytes: int) -> dict[str, Any]:
    """Keep residual-stream evidence distinct from final video/container size."""
    if any(isinstance(value, bool) or not isinstance(value, int) or value <= 0 for value in
           (compressed_bytes, fullrate_component_bytes, source_video_bytes)):
        raise ValueError("sizes must be positive integers")
    return {
        "residual_stream_compressed_bytes": compressed_bytes,
        "fullrate_component_stream_estimate_bytes": fullrate_component_bytes,
        "source_video_bytes": source_video_bytes,
        "reduction_vs_fullrate_component_stream_percent": round(
            100 * (1 - compressed_bytes / fullrate_component_bytes), 6
        ),
        "residual_stream_smaller_than_fullrate": compressed_bytes < fullrate_component_bytes,
        "residual_stream_smaller_than_source_video": compressed_bytes < source_video_bytes,
        "proof_scope": "residual_stream_vs_fullrate_component_estimate_only",
    }


def assess_candidate(
    metric: dict[str, Any],
    fullrate_metric: dict[str, Any],
    *,
    compressed_bytes: int,
    fullrate_component_bytes: int,
    source_video_bytes: int,
    artifact_warning: bool = False,
) -> dict[str, Any]:
    gate = visual_gate(metric, fullrate_metric)
    accounting = residual_accounting(compressed_bytes, fullrate_component_bytes, source_video_bytes)
    compression_evidence = accounting["residual_stream_smaller_than_fullrate"]
    if artifact_warning and gate["status"] == "PASS":
        gate = {"status": "NEEDS_HUMAN_REVIEW", "human_review_required": True,
                "reasons": ["suspected visual artifact"]}
    accepted_automatically = gate["status"] == "PASS" and compression_evidence
    return {
        "visual_gate": gate,
        "compression_accounting": accounting,
        "compression_proof_claimed": compression_evidence and gate["status"] != "REJECTED",
        "accepted_automatically": accepted_automatically,
        "human_review_required": gate["human_review_required"],
        "final_passed": accepted_automatically,
        "unsafe_acceptance_count": 0,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
    }
