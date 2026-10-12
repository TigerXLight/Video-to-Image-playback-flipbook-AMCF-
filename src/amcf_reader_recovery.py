from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS
from amcf_software_io_fixtures import load_fixture_bundle


RUN_NAME = "AMCF_READER_RECOVERY_FIXTURE_PROTOTYPE_V1"
RECOVERY_VERSION = "amcf_reader_recovery_fixture_v1"


@dataclass(frozen=True)
class RecoveredSectionRecord:
    section_id: str
    recovered: bool
    display_allowed: bool
    registration_status: str
    hash_status: str
    colour_status: str
    diagnostic: str


@dataclass(frozen=True)
class ReaderDiagnosticRequest:
    section_id: str
    request_type: str
    reason: str
    recommended_action: str


@dataclass(frozen=True)
class ReaderRecoveryReport:
    run_name: str
    recovery_version: str
    final_passed: bool
    recovered_sections: list[RecoveredSectionRecord]
    diagnostic_requests: list[ReaderDiagnosticRequest]
    claim_boundary_flags: dict[str, bool] = field(default_factory=lambda: dict(CLAIM_BOUNDARY_FLAGS))
    unsafe_acceptance_count: int = 0
    scanner_api_used: bool = False
    image_processing_used: bool = False
    barcode_decoding_used: bool = False


def recover_sections_from_fixture(bundle: dict[str, Any]) -> ReaderRecoveryReport:
    captures = {capture["section_id"]: capture for capture in bundle["reader_capture"]["simulated_captures"]}
    recovered: list[RecoveredSectionRecord] = []
    diagnostics: list[ReaderDiagnosticRequest] = []
    for section in bundle["package"]["manifest"]["physical_sections"]:
        section_id = section["section_id"]
        capture = captures.get(section_id)
        if capture is None:
            recovered.append(
                RecoveredSectionRecord(section_id, False, False, "missing", "missing", "missing", "capture_missing")
            )
            diagnostics.append(
                ReaderDiagnosticRequest(section_id, "rescan_request", "capture_missing", "rerun_simulated_fixture_capture")
            )
            continue
        registration_status = capture["registration_status"]
        hash_status = capture["hash_status"]
        colour_status = capture["colour_status"]
        critical_ok = registration_status == "matched" and hash_status == "matched"
        display_allowed = critical_ok
        diagnostic = "accepted"
        if colour_status == "degraded_warning" and critical_ok:
            diagnostic = "accepted_with_colour_warning"
        if not critical_ok:
            diagnostic = "rejected_before_display"
            request_type = "reprint_request" if hash_status != "matched" else "rescan_request"
            diagnostics.append(
                ReaderDiagnosticRequest(section_id, request_type, diagnostic, "inspect_fixture_lane_status")
            )
        recovered.append(
            RecoveredSectionRecord(
                section_id=section_id,
                recovered=critical_ok,
                display_allowed=display_allowed,
                registration_status=registration_status,
                hash_status=hash_status,
                colour_status=colour_status,
                diagnostic=diagnostic,
            )
        )
    flags = dict(CLAIM_BOUNDARY_FLAGS)
    unsafe_acceptance_count = sum(
        1 for item in recovered if item.display_allowed and item.hash_status != "matched"
    )
    final_passed = unsafe_acceptance_count == 0 and not any(flags.values()) and all(
        item.recovered or not item.display_allowed for item in recovered
    )
    return ReaderRecoveryReport(
        run_name=RUN_NAME,
        recovery_version=RECOVERY_VERSION,
        final_passed=final_passed,
        recovered_sections=recovered,
        diagnostic_requests=diagnostics,
        claim_boundary_flags=flags,
        unsafe_acceptance_count=unsafe_acceptance_count,
    )


def object_to_dict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, list):
        return [object_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: object_to_dict(item) for key, item in value.items()}
    return value


def write_reader_recovery_demo(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    bundle = load_fixture_bundle(repo_root)
    report = recover_sections_from_fixture(bundle)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    data = object_to_dict(report)
    (out / "reader_recovery_report.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "recovered_sections.json").write_text(
        json.dumps(data["recovered_sections"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "reader_diagnostics.json").write_text(
        json.dumps(data["diagnostic_requests"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = [
        "# AMCF PC Reader Recovery Fixture Demo",
        "",
        "This is a simulated reader recovery fixture. It does not use a scanner, camera, image processing, OCR, barcode decoding, or hardware APIs.",
        "",
        f"- final_passed: {'yes' if report.final_passed else 'no'}",
        f"- recovered_sections: {len(report.recovered_sections)}",
        f"- diagnostic_requests: {len(report.diagnostic_requests)}",
        f"- unsafe_acceptance_count: {report.unsafe_acceptance_count}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "",
    ]
    (out / "READER_RECOVERY_FIXTURE_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return {"report": data, "output_dir": str(out)}
