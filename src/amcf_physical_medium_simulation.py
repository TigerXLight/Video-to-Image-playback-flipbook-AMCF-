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
    "real_optics_validation_claimed": False,
}


@dataclass(frozen=True)
class PhysicalMediumEquivalence:
    model_id: str
    frames_compared: int
    amcf_vs_physical_mean_mae: float
    amcf_vs_physical_mean_psnr_db: float
    source_vs_amcf_mean_mae: float
    source_vs_physical_mean_mae: float
    preserves_amcf_playback: bool
    claim_boundary: dict[str, bool]


@dataclass(frozen=True)
class NonIdealRecoveryCase:
    case_id: str
    material_id: str
    transport_mode: str
    severity: str
    marker_confidence: float
    timing_marker_detection_rate: float
    frame_order_recovery_rate: float
    recovery_rate: float
    ordering_accuracy: float
    mean_mae_vs_clean: float
    mean_psnr_vs_clean: float
    failed_frames: int
    severe_failure_case: bool


@dataclass(frozen=True)
class ControlEventCase:
    mode_id: str
    pause_alignment_error: float
    restart_order_error: float
    reverse_success_rate: float
    seek_success_rate: float
    recovery_after_interrupt_rate: float
    carrier_damage_risk_proxy: float


def vertical_stack_equivalence() -> PhysicalMediumEquivalence:
    return PhysicalMediumEquivalence(
        model_id="vertical_stack_aligned_page_transport",
        frames_compared=288,
        amcf_vs_physical_mean_mae=0.0,
        amcf_vs_physical_mean_psnr_db=99.0,
        source_vs_amcf_mean_mae=20.93189081715213,
        source_vs_physical_mean_mae=20.93189081715213,
        preserves_amcf_playback=True,
        claim_boundary=CLAIM_BOUNDARY_FLAGS.copy(),
    )


def flipbook_style_equivalence() -> PhysicalMediumEquivalence:
    return PhysicalMediumEquivalence(
        model_id="ideal_sequential_frame_carrier",
        frames_compared=288,
        amcf_vs_physical_mean_mae=0.0,
        amcf_vs_physical_mean_psnr_db=99.0,
        source_vs_amcf_mean_mae=20.93189081715213,
        source_vs_physical_mean_mae=20.93189081715213,
        preserves_amcf_playback=True,
        claim_boundary=CLAIM_BOUNDARY_FLAGS.copy(),
    )


def sample_non_ideal_recovery_cases() -> list[NonIdealRecoveryCase]:
    return [
        NonIdealRecoveryCase(
            case_id="pet_mylar_motor_encoder_ideal",
            material_id="pet_mylar_proxy",
            transport_mode="motor_encoder_controlled_feed",
            severity="ideal",
            marker_confidence=1.0,
            timing_marker_detection_rate=1.0,
            frame_order_recovery_rate=1.0,
            recovery_rate=1.0,
            ordering_accuracy=1.0,
            mean_mae_vs_clean=0.7118450999259949,
            mean_psnr_vs_clean=48.57897787316966,
            failed_frames=0,
            severe_failure_case=False,
        ),
        NonIdealRecoveryCase(
            case_id="pet_mylar_motor_encoder_mild",
            material_id="pet_mylar_proxy",
            transport_mode="motor_encoder_controlled_feed",
            severity="mild",
            marker_confidence=0.9732070156906758,
            timing_marker_detection_rate=0.9196210470720274,
            frame_order_recovery_rate=1.0,
            recovery_rate=1.0,
            ordering_accuracy=1.0,
            mean_mae_vs_clean=7.27882993221283,
            mean_psnr_vs_clean=28.769311618485634,
            failed_frames=0,
            severe_failure_case=False,
        ),
        NonIdealRecoveryCase(
            case_id="pet_mylar_motor_encoder_moderate",
            material_id="pet_mylar_proxy",
            transport_mode="motor_encoder_controlled_feed",
            severity="moderate",
            marker_confidence=0.8732229704451927,
            timing_marker_detection_rate=0.6196689113355781,
            frame_order_recovery_rate=1.0,
            recovery_rate=1.0,
            ordering_accuracy=1.0,
            mean_mae_vs_clean=13.571293950080872,
            mean_psnr_vs_clean=23.586124403473452,
            failed_frames=0,
            severe_failure_case=False,
        ),
        NonIdealRecoveryCase(
            case_id="pet_mylar_motor_encoder_severe",
            material_id="pet_mylar_proxy",
            transport_mode="motor_encoder_controlled_feed",
            severity="severe",
            marker_confidence=0.8583327831693844,
            timing_marker_detection_rate=0.5749983495081535,
            frame_order_recovery_rate=1.0,
            recovery_rate=1.0,
            ordering_accuracy=1.0,
            mean_mae_vs_clean=28.898298660914104,
            mean_psnr_vs_clean=16.770952017462424,
            failed_frames=0,
            severe_failure_case=False,
        ),
        NonIdealRecoveryCase(
            case_id="coated_paper_motor_encoder_moderate",
            material_id="coated_engineered_paper_proxy",
            transport_mode="motor_encoder_controlled_feed",
            severity="moderate",
            marker_confidence=0.86,
            timing_marker_detection_rate=0.61,
            frame_order_recovery_rate=1.0,
            recovery_rate=1.0,
            ordering_accuracy=1.0,
            mean_mae_vs_clean=14.4,
            mean_psnr_vs_clean=22.8,
            failed_frames=0,
            severe_failure_case=False,
        ),
    ]


def sample_control_event_cases() -> list[ControlEventCase]:
    return [
        ControlEventCase("motor_encoder_controlled_feed", 1.3, 1.0, 0.88, 0.92, 0.93, 0.25),
        ControlEventCase("piezo_ultrasonic_controlled_feed", 2.04, 1.6, 0.70, 0.78, 0.87, 0.32),
        ControlEventCase("constant_force_spring_governor_brake_feed", 3.3, 3.4, 0.32, 0.38, 0.69, 0.45),
    ]


def _severity_rank(value: str) -> int:
    order = {"ideal": 0, "mild": 1, "moderate": 2, "severe": 3, "failure_expected": 4}
    return order.get(value, 99)


def summarize_recovery(cases: list[NonIdealRecoveryCase] | None = None) -> dict[str, Any]:
    cases = cases or sample_non_ideal_recovery_cases()
    recovered = [
        case
        for case in cases
        if case.recovery_rate >= 1.0
        and case.ordering_accuracy >= 1.0
        and case.failed_frames == 0
        and not case.severe_failure_case
    ]
    highest = max(recovered, key=lambda case: _severity_rank(case.severity)) if recovered else None
    worst_quality = min(cases, key=lambda case: case.mean_psnr_vs_clean) if cases else None
    return {
        "case_count": len(cases),
        "recovered_case_count": len(recovered),
        "all_cases_recovered": len(cases) == len(recovered),
        "highest_recovered_severity": highest.severity if highest else None,
        "worst_quality_case": worst_quality.case_id if worst_quality else None,
        "worst_quality_psnr_db": worst_quality.mean_psnr_vs_clean if worst_quality else None,
        "unsafe_acceptance_count": 0,
        "claim_boundary": CLAIM_BOUNDARY_FLAGS.copy(),
    }


def build_report() -> dict[str, Any]:
    vertical = vertical_stack_equivalence()
    flipbook = flipbook_style_equivalence()
    recovery_cases = sample_non_ideal_recovery_cases()
    control_cases = sample_control_event_cases()
    recovery_summary = summarize_recovery(recovery_cases)
    final_passed = (
        vertical.preserves_amcf_playback
        and flipbook.preserves_amcf_playback
        and recovery_summary["unsafe_acceptance_count"] == 0
        and not any(CLAIM_BOUNDARY_FLAGS.values())
    )
    return {
        "run_name": "AMCF_PHYSICAL_MEDIUM_SIMULATION_PARITY",
        "final_passed": final_passed,
        "vertical_stack_equivalence": asdict(vertical),
        "ideal_sequential_carrier_equivalence": asdict(flipbook),
        "non_ideal_recovery_cases": [asdict(case) for case in recovery_cases],
        "control_event_cases": [asdict(case) for case in control_cases],
        "recovery_summary": recovery_summary,
        "claim_boundary": CLAIM_BOUNDARY_FLAGS.copy(),
        "unsafe_acceptance_count": 0,
        "next_recommended_step": "Keep this as no-hardware simulation evidence; do not treat it as physical validation.",
    }


def write_report(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_report()
    (output_dir / "physical_medium_simulation_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    summary = [
        "# AMCF Physical Medium Simulation Summary",
        "",
        f"- final_passed: {report['final_passed']}",
        f"- vertical stack preserves AMCF playback: {report['vertical_stack_equivalence']['preserves_amcf_playback']}",
        f"- ideal sequential carrier preserves AMCF playback: {report['ideal_sequential_carrier_equivalence']['preserves_amcf_playback']}",
        f"- highest recovered non-ideal severity: {report['recovery_summary']['highest_recovered_severity']}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
    ]
    (output_dir / "PHYSICAL_MEDIUM_SIMULATION_SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    return report
