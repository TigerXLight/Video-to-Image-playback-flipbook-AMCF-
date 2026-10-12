from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, is_dataclass
from pathlib import Path
from typing import Any

from amcf_shared_package_model import (
    CLAIM_BOUNDARY_FLAGS,
    AMCFPackage,
    build_demo_shared_package,
    object_to_dict,
    validate_shared_package,
)


RUN_NAME = "AMCF_CROSS_CORRIDOR_REPORTING_BASELINE_V1"
REPORT_VERSION = "amcf_cross_corridor_reporting_v1"
CORRIDORS = (
    "shared_core",
    "pc_to_printer",
    "pc_reader",
    "player_pc",
)


@dataclass(frozen=True)
class AMCFClaimBoundaryReport:
    hardware_validation_claimed: bool = False
    physical_level_5_claimed: bool = False
    manufactured_player_claimed: bool = False
    real_printer_required: bool = False
    real_reader_required: bool = False
    real_player_required: bool = False
    real_scanner_required: bool = False
    real_usb_required: bool = False
    summary: str = "software/no-hardware cross-corridor report baseline"


@dataclass(frozen=True)
class AMCFSafetyDecision:
    decision_id: str
    corridor: str
    decision: str
    reason: str
    display_allowed: bool
    transition_allowed: bool
    retry_allowed: bool
    rescan_allowed: bool
    unsafe_acceptance: bool
    recommended_action: str


@dataclass(frozen=True)
class AMCFCorridorCheck:
    corridor: str
    passed: bool
    checks: list[str]
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AMCFCrossCorridorReport:
    run_name: str
    report_version: str
    final_passed: bool
    package_id: str
    manifest_id: str
    corridor_checks: list[AMCFCorridorCheck]
    safety_decisions: list[AMCFSafetyDecision]
    claim_boundary_flags: dict[str, bool]
    unsafe_acceptance_count: int
    summary: str


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    return object_to_dict(value)


def write_json(path: str | Path, data: Any) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(_to_jsonable(data), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_claim_boundary_report() -> AMCFClaimBoundaryReport:
    return AMCFClaimBoundaryReport(**CLAIM_BOUNDARY_FLAGS)


def build_safety_decision(
    decision_id: str,
    corridor: str,
    decision: str,
    reason: str,
    *,
    display_allowed: bool = False,
    transition_allowed: bool = False,
    retry_allowed: bool = False,
    rescan_allowed: bool = False,
    recommended_action: str = "continue_software_fixture_validation",
) -> AMCFSafetyDecision:
    unsafe_acceptance = decision in {"accepted", "accepted_with_warning"} and not display_allowed
    return AMCFSafetyDecision(
        decision_id=decision_id,
        corridor=corridor,
        decision=decision,
        reason=reason,
        display_allowed=display_allowed,
        transition_allowed=transition_allowed,
        retry_allowed=retry_allowed,
        rescan_allowed=rescan_allowed,
        unsafe_acceptance=unsafe_acceptance,
        recommended_action=recommended_action,
    )


def build_cross_corridor_report(package: AMCFPackage | None = None) -> AMCFCrossCorridorReport:
    package = package or build_demo_shared_package()
    validation = validate_shared_package(package)
    shared_ok = validation.final_passed
    section_count = package.manifest.section_count
    lane_ready = all(section.lanes for section in package.manifest.physical_sections)
    corridor_checks = [
        AMCFCorridorCheck(
            "shared_core",
            shared_ok,
            ["package_model_present", "manifest_present", "update_events_present", "physical_sections_present"],
            validation.warnings,
        ),
        AMCFCorridorCheck(
            "pc_to_printer",
            shared_ok and lane_ready,
            ["shared_manifest_available", "section_lanes_available", "print_runtime_not_implemented"],
            ["no_hardware_printer_driver_claimed"],
        ),
        AMCFCorridorCheck(
            "pc_reader",
            shared_ok and section_count > 0,
            ["shared_manifest_available", "hash_lanes_available", "reader_runtime_not_implemented"],
            ["no_scanner_or_image_capture_claimed"],
        ),
        AMCFCorridorCheck(
            "player_pc",
            shared_ok and section_count > 0,
            ["shared_manifest_available", "update_events_available", "player_runtime_not_implemented"],
            ["no_usb_serial_or_hardware_player_claimed"],
        ),
    ]
    safety_decisions = [
        build_safety_decision(
            "decision-shared-package-valid",
            "shared_core",
            "accepted",
            "shared_package_validation_passed",
            display_allowed=True,
            transition_allowed=True,
        )
        if validation.final_passed
        else build_safety_decision(
            "decision-shared-package-invalid",
            "shared_core",
            "rejected_fail_closed",
            "shared_package_validation_failed",
            recommended_action="fix_shared_package_before_corridor_use",
        )
    ]
    unsafe_acceptance_count = sum(1 for decision in safety_decisions if decision.unsafe_acceptance)
    flags = dict(CLAIM_BOUNDARY_FLAGS)
    final_passed = (
        all(check.passed for check in corridor_checks)
        and validation.final_passed
        and unsafe_acceptance_count == 0
        and not any(flags.values())
    )
    return AMCFCrossCorridorReport(
        run_name=RUN_NAME,
        report_version=REPORT_VERSION,
        final_passed=final_passed,
        package_id=package.package_id,
        manifest_id=package.manifest.manifest_id,
        corridor_checks=corridor_checks,
        safety_decisions=safety_decisions,
        claim_boundary_flags=flags,
        unsafe_acceptance_count=unsafe_acceptance_count,
        summary="software/no-hardware cross-corridor reporting baseline",
    )


def build_summary_markdown(report: AMCFCrossCorridorReport) -> str:
    lines = [
        "# AMCF Cross-Corridor Reporting Demo",
        "",
        "This is a software/no-hardware report baseline for AMCF software I/O corridors.",
        "",
        f"- final_passed: {'yes' if report.final_passed else 'no'}",
        f"- package_id: `{report.package_id}`",
        f"- manifest_id: `{report.manifest_id}`",
        f"- unsafe_acceptance_count: {report.unsafe_acceptance_count}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "",
        "## Corridor Checks",
        "",
    ]
    for check in report.corridor_checks:
        lines.append(f"- `{check.corridor}`: {'pass' if check.passed else 'fail'}")
    lines.extend(
        [
            "",
            "No printer driver, scanner, image-processing, USB, serial, firmware, GUI, PDF, or barcode support is implemented here.",
            "",
        ]
    )
    return "\n".join(lines)


def write_demo_cross_corridor_report(output_dir: str | Path) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    package = build_demo_shared_package()
    report = build_cross_corridor_report(package)
    claim_report = build_claim_boundary_report()
    write_json(out / "cross_corridor_report.json", report)
    write_json(out / "claim_boundary_report.json", claim_report)
    write_json(out / "safety_decisions.json", report.safety_decisions)
    (out / "CROSS_CORRIDOR_REPORTING_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    return {
        "report": _to_jsonable(report),
        "claim_boundary_report": _to_jsonable(claim_report),
        "output_dir": str(out),
    }
