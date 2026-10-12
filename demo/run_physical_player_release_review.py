from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
SRC = PACKAGE / "src"
sys.path.insert(0, str(SRC))

from amcf_physical_player_integrated_demo_reports import build_integrated_simulation_summary  # noqa: E402


RUN_NAME = "AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1"
BASE_COMMIT_HINT = "c7c2658877f04d40b94b127c6e44fe30d3597a18"

REQUIRED_DOCS = [
    "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md",
    "docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md",
    "docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md",
    "docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md",
    "docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md",
    "docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md",
    "docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md",
    "docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md",
    "docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md",
    "docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md",
    "docs/AMCF_HARDWARE_SOFTWARE_PATHS.md",
    "CLAIM_BOUNDARIES.md",
]

REQUIRED_DEMOS = [
    "demo/run_physical_player_state_machine_demo.py",
    "demo/run_physical_player_fail_closed_demo.py",
    "demo/run_physical_player_reverse_seek_demo.py",
    "demo/run_physical_player_mechanism_profiles_demo.py",
    "demo/run_physical_player_simulator_demo.py",
]

REQUIRED_TESTS = [
    "tests/test_physical_player_state_machine.py",
    "tests/test_physical_player_fail_closed.py",
    "tests/test_physical_player_reverse_seek.py",
    "tests/test_physical_player_mechanism_profiles.py",
    "tests/test_physical_player_simulator_demo.py",
    "tests/test_physical_player_public_docs_sync.py",
    "tests/test_physical_player_release_review.py",
]

KNOWN_STAGE_COMMITS = [
    "f8b6e91e1dfd9b57345ee38ac262635d446f47c8",
    "4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e",
    "802042b5395ac860c437188e0d79031d7dd5f591",
    "01093024f9bbd11d10615a0f526b4440e5f8f41b",
    "fea00409262dea39d5c9068daac0a206c02d07f5",
    "c7c2658877f04d40b94b127c6e44fe30d3597a18",
]

GENERATED_OUTPUT_DIRS = [
    "output/physical_player_state_machine_demo/",
    "output/physical_player_fail_closed_demo/",
    "output/physical_player_reverse_seek_demo/",
    "output/physical_player_mechanism_profiles_demo/",
    "output/physical_player_simulator_demo/",
    "output/physical_player_release_review/",
]

LOCAL_PATH_PATTERNS = [
    "T:\\",
    "C:\\Users\\",
    "AppData\\",
    "Tests\\Test AMCF_PUBLIC",
    "AMCF_GITHUB_CLEAN_PACKAGE",
    "codex-runtimes",
]

DANGEROUS_PHRASES = [
    "manufactured physical player exists",
    "real physical player exists",
    "physical level 5 complete",
    "hardware validated",
    "real motor validated",
    "real sensor validated",
    "real cartridge validated",
    "real optical playback proven",
    "no-gap physically proven",
    "arbitrary physical seek proven",
    "reverse hardware proven",
    "energy recovery powers the system",
]

NEGATIVE_BOUNDARY_MARKERS = [
    "no ",
    "not ",
    "does not",
    "do not",
    "false",
    "not claimed",
    "until real hardware",
    "without claiming",
]


def read_rel(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


def rel_exists(path: str) -> bool:
    return (PACKAGE / path).exists()


def public_files() -> list[Path]:
    files = [PACKAGE / "README.md", PACKAGE / "CLAIM_BOUNDARIES.md"]
    files.extend(sorted((PACKAGE / "docs").glob("*.md")))
    site_index = PACKAGE / "site" / "index.html"
    if site_index.exists():
        files.append(site_index)
    return files


def rel_path(path: Path) -> str:
    return path.relative_to(PACKAGE).as_posix()


def is_negative_boundary(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in NEGATIVE_BOUNDARY_MARKERS)


def scan_claim_boundaries() -> dict[str, Any]:
    matches: list[dict[str, Any]] = []
    unsafe: list[dict[str, Any]] = []
    for path in public_files():
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            lowered = line.lower()
            for phrase in DANGEROUS_PHRASES:
                if phrase in lowered:
                    item = {
                        "file": rel_path(path),
                        "line": line_number,
                        "phrase": phrase,
                        "negative_boundary": is_negative_boundary(line),
                        "text": line.strip(),
                    }
                    matches.append(item)
                    if not item["negative_boundary"]:
                        unsafe.append(item)
    return {
        "passed": len(unsafe) == 0,
        "match_count": len(matches),
        "unsafe_affirmative_overclaim_count": len(unsafe),
        "matches": matches,
        "unsafe_matches": unsafe,
    }


def scan_local_paths() -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    for path in public_files():
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern in LOCAL_PATH_PATTERNS:
                if pattern in line:
                    hits.append({"file": rel_path(path), "line": line_number, "pattern": pattern, "text": line.strip()})
    return {"passed": len(hits) == 0, "hit_count": len(hits), "hits": hits}


def git_lines(args: list[str]) -> list[str]:
    try:
        result = subprocess.run(["git", *args], cwd=PACKAGE, text=True, capture_output=True, check=False)
    except OSError as exc:
        return [f"git_unavailable:{exc}"]
    if result.returncode != 0:
        return [f"git_error:{result.stderr.strip()}"]
    return [line for line in result.stdout.splitlines() if line.strip()]


def scan_generated_output() -> dict[str, Any]:
    tracked = git_lines(["ls-files", "output"])
    staged = [line for line in git_lines(["diff", "--cached", "--name-only", "--", "output"]) if not line.startswith("git_")]
    existing = [folder for folder in GENERATED_OUTPUT_DIRS if (PACKAGE / folder).exists()]
    tracked_outputs = [line for line in tracked if not line.startswith("git_")]
    return {
        "passed": len(tracked_outputs) == 0 and len(staged) == 0,
        "generated_output_folders_found": existing,
        "tracked_output_files": tracked_outputs,
        "staged_output_files": staged,
        "generated_output_committed": len(tracked_outputs) > 0,
        "generated_output_staged": len(staged) > 0,
    }


def build_docs_link_scan() -> dict[str, Any]:
    readme = read_rel("README.md")
    docs_map = read_rel("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
    claim_boundaries = read_rel("CLAIM_BOUNDARIES.md")
    sequence = read_rel("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
    site_path = PACKAGE / "site" / "index.html"
    site_html = site_path.read_text(encoding="utf-8") if site_path.exists() else ""
    checks = {
        "required_docs_exist": all(rel_exists(path) for path in REQUIRED_DOCS),
        "required_demos_exist": all(rel_exists(path) for path in REQUIRED_DEMOS),
        "required_tests_exist": all(rel_exists(path) for path in REQUIRED_TESTS),
        "readme_links_docs_map": "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in readme,
        "readme_links_simulator_demo_doc": "docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md" in readme,
        "claim_boundaries_has_physical_player_boundary": "Physical Player Software-Control Simulator" in claim_boundaries,
        "docs_map_links_all_physical_player_docs": all(path in docs_map for path in REQUIRED_DOCS if path.startswith("docs/AMCF_PHYSICAL_PLAYER")),
        "docs_map_links_all_five_demo_scripts": all(path in docs_map for path in REQUIRED_DEMOS),
        "site_links_physical_player_docs": (not site_path.exists()) or ("AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in site_html and "AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md" in site_html),
        "development_sequence_mentions_stages_2_to_7": all(f"Stage {number}" in sequence for number in range(2, 8)),
        "development_sequence_mentions_known_commits_2_to_6": all(commit in sequence for commit in KNOWN_STAGE_COMMITS[:5]),
    }
    return {"passed": all(checks.values()), "checks": checks}


def build_release_review_report() -> dict[str, Any]:
    docs_scan = build_docs_link_scan()
    claim_scan = scan_claim_boundaries()
    local_scan = scan_local_paths()
    output_scan = scan_generated_output()
    integrated_summary = build_integrated_simulation_summary()
    unsafe_count = int(integrated_summary["unsafe_acceptance_audit"]["unsafe_acceptance_count"])
    claim_values = {
        "physical_hardware_claimed": False,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "real_sensors_required": False,
        "real_motors_required": False,
        "real_cartridges_required": False,
        "real_scans_required": False,
        "manufactured_player_claimed": False,
    }
    final_passed = (
        docs_scan["passed"]
        and claim_scan["passed"]
        and local_scan["passed"]
        and output_scan["passed"]
        and integrated_summary["final_passed"]
        and unsafe_count == 0
        and all(value is False for value in claim_values.values())
    )
    return {
        "run_name": RUN_NAME,
        "base_commit_hint": BASE_COMMIT_HINT,
        "software_control_release_review_only": True,
        **claim_values,
        "docs_link_scan": docs_scan,
        "claim_boundary_scan": claim_scan,
        "local_path_scan": local_scan,
        "generated_output_scan": output_scan,
        "integrated_simulator_summary": {
            "default_mechanism_profile_id": integrated_summary["default_mechanism_profile_id"],
            "profile_count": integrated_summary["mechanism_profile_phase"]["profile_count"],
            "forward_transition_count": integrated_summary["forward_playback_phase"]["forward_transition_count"],
            "fail_closed_scenario_count": integrated_summary["fail_closed_phase"]["scenario_count"],
            "fail_closed_event_count": integrated_summary["fail_closed_phase"]["fail_closed_event_count"],
            "reverse_attempts": integrated_summary["reverse_seek_phase"]["reverse_attempts"],
            "reverse_successes": integrated_summary["reverse_seek_phase"]["reverse_successes"],
            "reverse_denials": integrated_summary["reverse_seek_phase"]["reverse_denials"],
            "seek_attempts": integrated_summary["reverse_seek_phase"]["seek_attempts"],
            "seek_successes": integrated_summary["reverse_seek_phase"]["seek_successes"],
            "seek_denials": integrated_summary["reverse_seek_phase"]["seek_denials"],
            "arbitrary_seek_denied_count": integrated_summary["reverse_seek_phase"]["arbitrary_seek_denied_count"],
            "unsafe_acceptance_count": unsafe_count,
            "integrated_report_passed": integrated_summary["final_passed"],
        },
        "unsafe_acceptance_count": unsafe_count,
        "final_passed": final_passed,
        "recommended_next_stage": "push this release-review commit, then continue future hardware-adapter alignment without hardware validation claims",
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_summary_markdown(report: dict[str, Any]) -> str:
    sim = report["integrated_simulator_summary"]
    return "\n".join(
        [
            "# AMCF Physical Player Release Review Summary",
            "",
            "This is a software/control release-review artifact, not hardware proof.",
            "",
            f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
            f"- default mechanism profile: {sim['default_mechanism_profile_id']}",
            f"- profile count: {sim['profile_count']}",
            f"- forward transitions: {sim['forward_transition_count']}",
            f"- fail-closed scenarios/events: {sim['fail_closed_scenario_count']} / {sim['fail_closed_event_count']}",
            f"- reverse attempts/successes/denials: {sim['reverse_attempts']} / {sim['reverse_successes']} / {sim['reverse_denials']}",
            f"- seek attempts/successes/denials: {sim['seek_attempts']} / {sim['seek_successes']} / {sim['seek_denials']}",
            f"- arbitrary seek denied count: {sim['arbitrary_seek_denied_count']}",
            f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
            f"- generated output committed: {'yes' if report['generated_output_scan']['generated_output_committed'] else 'no'}",
            f"- local path leak found: {'yes' if not report['local_path_scan']['passed'] else 'no'}",
            f"- unsafe hardware claim found: {'yes' if not report['claim_boundary_scan']['passed'] else 'no'}",
            "- physical hardware claimed: no",
            "- hardware validation claimed: no",
            "- physical Level 5 claimed: no",
            "- manufactured physical player claimed: no",
            "",
        ]
    )


def build_next_steps_markdown() -> str:
    return "\n".join(
        [
            "# Next Steps",
            "",
            "- Push the release-review commit after local review.",
            "- Keep generated output folders ignored and uncommitted.",
            "- Continue future hardware-adapter alignment without claiming real hardware validation.",
            "",
        ]
    )


def write_release_review_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_release_review_report()
    write_json(output_dir / "release_review_report.json", report)
    write_json(output_dir / "claim_boundary_scan.json", report["claim_boundary_scan"])
    write_json(output_dir / "docs_link_scan.json", report["docs_link_scan"])
    write_json(output_dir / "generated_output_scan.json", report["generated_output_scan"])
    write_json(output_dir / "local_path_scan.json", report["local_path_scan"])
    (output_dir / "RELEASE_REVIEW_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    (output_dir / "next_steps.md").write_text(build_next_steps_markdown(), encoding="utf-8")
    return report


def main() -> None:
    out = PACKAGE / "output" / "physical_player_release_review"
    report = write_release_review_outputs(out)
    sim = report["integrated_simulator_summary"]
    print(
        json.dumps(
            {
                "ok": bool(report["final_passed"]),
                "output_folder": str(out),
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "generated_output_committed": report["generated_output_scan"]["generated_output_committed"],
                "local_path_leak_found": not report["local_path_scan"]["passed"],
                "unsafe_hardware_claim_found": not report["claim_boundary_scan"]["passed"],
                "physical_hardware_claimed": report["physical_hardware_claimed"],
                "hardware_validation_claimed": report["hardware_validation_claimed"],
                "physical_level_5_claimed": report["physical_level_5_claimed"],
                "default_mechanism_profile_id": sim["default_mechanism_profile_id"],
                "profile_count": sim["profile_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
