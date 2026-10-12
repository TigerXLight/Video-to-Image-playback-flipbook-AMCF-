from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS, REQUIRED_SECTION_LANES, stable_hash


RUN_NAME = "AMCF_SOFTWARE_IO_FIXTURE_REGRESSION_BASELINE_V1"
FIXTURE_VERSION = "amcf_software_io_fixtures_v1"


def fixture_root(repo_root: str | Path) -> Path:
    return Path(repo_root) / "tests" / "fixtures" / "amcf_software_io"


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_fixture_bundle(repo_root: str | Path) -> dict[str, Any]:
    root = fixture_root(repo_root)
    return {
        "package": load_json(root / "shared_package_fixture.json"),
        "reader_capture": load_json(root / "reader_capture_fixture.json"),
        "player_profile": load_json(root / "player_profile_fixture.json"),
    }


def validate_fixture_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    checks_passed: list[str] = []
    checks_failed: list[str] = []
    package = bundle["package"]
    reader_capture = bundle["reader_capture"]
    player_profile = bundle["player_profile"]
    sections = package["manifest"]["physical_sections"]
    if package["fixture_version"] == FIXTURE_VERSION:
        checks_passed.append("fixture_version_supported")
    else:
        checks_failed.append("fixture_version_unsupported")
    if len(sections) == package["manifest"]["section_count"]:
        checks_passed.append("section_count_matches")
    else:
        checks_failed.append("section_count_mismatch")
    for section in sections:
        missing = [lane for lane in REQUIRED_SECTION_LANES if lane not in section["lanes"]]
        if missing:
            checks_failed.append(f"missing_required_lanes:{section['section_id']}")
        expected_hash = stable_hash(section["payload_seed"])
        if section["payload_hash"] != expected_hash:
            checks_failed.append(f"payload_hash_mismatch:{section['section_id']}")
    capture_ids = {item["section_id"] for item in reader_capture["simulated_captures"]}
    section_ids = {section["section_id"] for section in sections}
    if section_ids.issubset(capture_ids):
        checks_passed.append("reader_capture_sections_present")
    else:
        checks_failed.append("reader_capture_missing_section")
    if player_profile["seek_model"] == "local_buffer_seek_only":
        checks_passed.append("player_profile_seek_is_bounded")
    else:
        checks_failed.append("player_profile_seek_unbounded")
    flags = dict(CLAIM_BOUNDARY_FLAGS)
    final_passed = len(checks_failed) == 0 and not any(flags.values())
    return {
        "run_name": RUN_NAME,
        "fixture_version": FIXTURE_VERSION,
        "final_passed": final_passed,
        "checks_passed": checks_passed,
        "checks_failed": checks_failed,
        "fixture_files": sorted(bundle.keys()),
        "claim_boundary_flags": flags,
        "unsafe_acceptance_count": 0,
    }


def write_fixture_report(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    bundle = load_fixture_bundle(repo_root)
    report = validate_fixture_bundle(bundle)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "fixture_regression_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "fixture_bundle_index.json").write_text(
        json.dumps({"fixtures": report["fixture_files"], "source": "tests/fixtures/amcf_software_io/"}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = [
        "# AMCF Software I/O Fixture Regression Baseline",
        "",
        "These are deterministic no-hardware fixtures for later AMCF software I/O phases.",
        "",
        f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "",
    ]
    (out / "SOFTWARE_IO_FIXTURE_BASELINE_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return report
