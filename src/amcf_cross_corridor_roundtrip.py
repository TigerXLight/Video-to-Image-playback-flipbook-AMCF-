from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from amcf_cross_corridor_reporting import build_cross_corridor_report
from amcf_player_pc_runtime import run_simulated_player_session
from amcf_print_layout import build_print_layout_manifest, validate_print_layout
from amcf_reader_recovery import recover_sections_from_fixture
from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS, build_demo_shared_package
from amcf_software_io_fixtures import load_fixture_bundle


RUN_NAME = "AMCF_CROSS_CORRIDOR_ROUNDTRIP_PROTOTYPE_V1"
ROUNDTRIP_VERSION = "amcf_cross_corridor_roundtrip_v1"


@dataclass(frozen=True)
class CrossCorridorRoundtripReport:
    run_name: str
    roundtrip_version: str
    final_passed: bool
    shared_manifest_passed: bool
    print_layout_passed: bool
    reader_recovery_passed: bool
    player_session_passed: bool
    cross_corridor_report_passed: bool
    section_count: int
    recovered_section_count: int
    command_count: int
    claim_boundary_flags: dict[str, bool] = field(default_factory=lambda: dict(CLAIM_BOUNDARY_FLAGS))
    unsafe_acceptance_count: int = 0


def run_cross_corridor_roundtrip(repo_root: str | Path) -> dict[str, Any]:
    bundle = load_fixture_bundle(repo_root)
    package = build_demo_shared_package()
    layout = build_print_layout_manifest(bundle)
    layout_report = validate_print_layout(layout)
    reader_report = recover_sections_from_fixture(bundle)
    player_report = run_simulated_player_session(bundle)
    corridor_report = build_cross_corridor_report(package)
    unsafe_acceptance_count = (
        layout_report["unsafe_acceptance_count"]
        + reader_report.unsafe_acceptance_count
        + player_report.unsafe_acceptance_count
        + corridor_report.unsafe_acceptance_count
    )
    flags = dict(CLAIM_BOUNDARY_FLAGS)
    final_passed = (
        layout_report["final_passed"]
        and reader_report.final_passed
        and player_report.final_passed
        and corridor_report.final_passed
        and unsafe_acceptance_count == 0
        and not any(flags.values())
    )
    report = CrossCorridorRoundtripReport(
        run_name=RUN_NAME,
        roundtrip_version=ROUNDTRIP_VERSION,
        final_passed=final_passed,
        shared_manifest_passed=True,
        print_layout_passed=layout_report["final_passed"],
        reader_recovery_passed=reader_report.final_passed,
        player_session_passed=player_report.final_passed,
        cross_corridor_report_passed=corridor_report.final_passed,
        section_count=len(layout.sections),
        recovered_section_count=len(reader_report.recovered_sections),
        command_count=len(player_report.command_transcript),
        claim_boundary_flags=flags,
        unsafe_acceptance_count=unsafe_acceptance_count,
    )
    return {
        "roundtrip_report": asdict(report),
        "print_layout_report": layout_report,
        "reader_recovery_report": asdict(reader_report),
        "player_session_report": asdict(player_report),
        "cross_corridor_report": asdict(corridor_report),
    }


def write_cross_corridor_roundtrip_demo(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    result = run_cross_corridor_roundtrip(repo_root)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "cross_corridor_roundtrip_report.json").write_text(
        json.dumps(result["roundtrip_report"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "roundtrip_component_reports.json").write_text(
        json.dumps({key: value for key, value in result.items() if key != "roundtrip_report"}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report = result["roundtrip_report"]
    summary = [
        "# AMCF Cross-Corridor Roundtrip Demo",
        "",
        "This no-hardware roundtrip uses shared fixtures across the printer, reader, and player software-control corridors.",
        "",
        f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
        f"- section_count: {report['section_count']}",
        f"- recovered_section_count: {report['recovered_section_count']}",
        f"- command_count: {report['command_count']}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "",
    ]
    (out / "CROSS_CORRIDOR_ROUNDTRIP_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    result["output_dir"] = str(out)
    return result
