from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
SRC = PACKAGE / "src"
DEMO = PACKAGE / "demo"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(DEMO))

from amcf_physical_player_integrated_demo_reports import build_integrated_simulation_summary  # noqa: E402
from run_physical_player_release_review import scan_claim_boundaries, scan_generated_output, scan_local_paths  # noqa: E402


RUN_NAME = "AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1"
BASE_COMMIT_HINT = "8082f0a1134ea33df330c0508f06cc3ff7130e59"

COMMIT_TRAIL = [
    {
        "stage": "Stage 2",
        "run_name": "AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1",
        "commit": "f8b6e91e1dfd9b57345ee38ac262635d446f47c8",
    },
    {
        "stage": "Stage 3",
        "run_name": "AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1",
        "commit": "4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e",
    },
    {
        "stage": "Stage 4",
        "run_name": "AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1",
        "commit": "802042b5395ac860c437188e0d79031d7dd5f591",
    },
    {
        "stage": "Stage 5",
        "run_name": "AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1",
        "commit": "01093024f9bbd11d10615a0f526b4440e5f8f41b",
    },
    {
        "stage": "Stage 6",
        "run_name": "AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1",
        "commit": "fea00409262dea39d5c9068daac0a206c02d07f5",
    },
    {
        "stage": "Stage 7",
        "run_name": "AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1",
        "commit": "c7c2658877f04d40b94b127c6e44fe30d3597a18",
    },
    {
        "stage": "Stage 8",
        "run_name": "AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1",
        "commit": "659bd3e74a9e4dd254600558aec6e76309ba596f",
    },
    {
        "stage": "Stage 9",
        "run_name": "AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1",
        "commit": "8f76d7528e4f6399ef719a99f15e1b248ce8e2ff",
    },
    {
        "stage": "Stage 10",
        "run_name": "AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1",
        "commit": "8082f0a1134ea33df330c0508f06cc3ff7130e59",
    },
    {
        "stage": "Stage 11",
        "run_name": RUN_NAME,
        "commit": "current run, not committed yet",
    },
]

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
    "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md",
    "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md",
    "docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md",
    "docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md",
    "docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md",
    "docs/AMCF_HARDWARE_SOFTWARE_PATHS.md",
    "CLAIM_BOUNDARIES.md",
]

REQUIRED_SOURCE = [
    "src/amcf_physical_player_state_machine.py",
    "src/amcf_physical_player_state_machine_reports.py",
    "src/amcf_physical_player_mechanism_profiles.py",
    "src/amcf_physical_player_mechanism_profile_reports.py",
    "src/amcf_physical_player_integrated_demo_reports.py",
]

REQUIRED_DEMOS = [
    "demo/run_physical_player_state_machine_demo.py",
    "demo/run_physical_player_fail_closed_demo.py",
    "demo/run_physical_player_reverse_seek_demo.py",
    "demo/run_physical_player_mechanism_profiles_demo.py",
    "demo/run_physical_player_simulator_demo.py",
    "demo/run_physical_player_release_review.py",
    "demo/run_public_release_package_refresh.py",
    "demo/run_public_github_pages_final_review.py",
    "demo/run_public_release_closeout_handoff.py",
]

REQUIRED_TESTS = [
    "tests/test_physical_player_state_machine.py",
    "tests/test_physical_player_fail_closed.py",
    "tests/test_physical_player_reverse_seek.py",
    "tests/test_physical_player_mechanism_profiles.py",
    "tests/test_physical_player_simulator_demo.py",
    "tests/test_physical_player_public_docs_sync.py",
    "tests/test_physical_player_release_review.py",
    "tests/test_public_release_package_refresh.py",
    "tests/test_public_github_pages_final_review.py",
    "tests/test_public_release_closeout_handoff.py",
]

CLAIM_VALUES_FALSE = {
    "physical_hardware_claimed": False,
    "hardware_validation_claimed": False,
    "physical_level_5_claimed": False,
    "real_sensors_required": False,
    "real_motors_required": False,
    "real_cartridges_required": False,
    "real_scans_required": False,
    "manufactured_player_claimed": False,
}


def exists_rel(path: str) -> bool:
    return (PACKAGE / path).exists()


def read_rel(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


def all_exist(paths: list[str]) -> bool:
    return all(exists_rel(path) for path in paths)


def build_commit_trail_summary() -> dict[str, Any]:
    sequence = read_rel("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
    handoff = read_rel("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md") if exists_rel("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md") else ""
    pushed_commits = [item["commit"] for item in COMMIT_TRAIL if item["commit"] != "current run, not committed yet"]
    return {
        "commit_trail": COMMIT_TRAIL,
        "known_pushed_commits": pushed_commits,
        "development_sequence_has_stages_2_to_11": all(f"Stage {number}" in sequence for number in range(2, 12)),
        "development_sequence_has_known_commits_2_to_10": all(commit in sequence for commit in pushed_commits),
        "handoff_doc_has_stages_2_to_11": all(f"Stage {number}" in handoff for number in range(2, 12)),
        "handoff_doc_has_known_commits_2_to_10": all(commit in handoff for commit in pushed_commits),
    }


def build_docs_site_summary() -> dict[str, Any]:
    readme = read_rel("README.md")
    docs_map = read_rel("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
    site_html = read_rel("site/index.html") if exists_rel("site/index.html") else ""
    checks = {
        "site_present": exists_rel("site/index.html"),
        "site_links_present": (
            "AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in site_html
            and ("AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md" in site_html or "AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md" in site_html)
        ),
        "readme_entrypoints_present": (
            "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in readme
            and "docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md" in readme
        ),
        "docs_map_links_closeout": "docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md" in docs_map,
        "release_review_present": exists_rel("docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md"),
        "package_refresh_present": exists_rel("docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md"),
        "final_pages_review_present": exists_rel("docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md"),
        "claim_boundaries_present": exists_rel("CLAIM_BOUNDARIES.md")
        and "Physical Player Software-Control Simulator" in read_rel("CLAIM_BOUNDARIES.md"),
    }
    return {"passed": all(checks.values()), "checks": checks}


def build_closeout_handoff_report() -> dict[str, Any]:
    commit_summary = build_commit_trail_summary()
    docs_site = build_docs_site_summary()
    claim_scan = scan_claim_boundaries()
    local_scan = scan_local_paths()
    output_scan = scan_generated_output()
    integrated = build_integrated_simulation_summary()
    unsafe_count = int(integrated["unsafe_acceptance_audit"]["unsafe_acceptance_count"])
    required_docs_present = all_exist(REQUIRED_DOCS)
    required_source_present = all_exist(REQUIRED_SOURCE)
    required_demos_present = all_exist(REQUIRED_DEMOS)
    required_tests_present = all_exist(REQUIRED_TESTS)
    commit_trail_complete = (
        commit_summary["development_sequence_has_stages_2_to_11"]
        and commit_summary["development_sequence_has_known_commits_2_to_10"]
        and commit_summary["handoff_doc_has_stages_2_to_11"]
        and commit_summary["handoff_doc_has_known_commits_2_to_10"]
    )
    final_passed = (
        exists_rel("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md")
        and commit_trail_complete
        and required_docs_present
        and required_source_present
        and required_demos_present
        and required_tests_present
        and docs_site["passed"]
        and claim_scan["passed"]
        and local_scan["passed"]
        and output_scan["passed"]
        and unsafe_count == 0
        and all(value is False for value in CLAIM_VALUES_FALSE.values())
    )
    return {
        "run_name": RUN_NAME,
        "base_commit_hint": BASE_COMMIT_HINT,
        "closeout_doc_present": exists_rel("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md"),
        "commit_trail_complete": commit_trail_complete,
        "required_docs_present": required_docs_present,
        "required_source_present": required_source_present,
        "required_demos_present": required_demos_present,
        "required_tests_present": required_tests_present,
        "site_present": docs_site["checks"]["site_present"],
        "site_links_present": docs_site["checks"]["site_links_present"],
        "readme_entrypoints_present": docs_site["checks"]["readme_entrypoints_present"],
        "development_sequence_complete": commit_summary["development_sequence_has_stages_2_to_11"],
        "release_review_present": docs_site["checks"]["release_review_present"],
        "package_refresh_present": docs_site["checks"]["package_refresh_present"],
        "final_pages_review_present": docs_site["checks"]["final_pages_review_present"],
        "generated_output_tracked": output_scan["generated_output_committed"] or output_scan["generated_output_staged"],
        "local_path_leak_found": not local_scan["passed"],
        "unsafe_hardware_claim_found": not claim_scan["passed"],
        "unsafe_acceptance_count": unsafe_count,
        **CLAIM_VALUES_FALSE,
        "commit_trail_summary": commit_summary,
        "docs_site_summary": docs_site,
        "claim_boundary_summary": claim_scan,
        "generated_output_scan": output_scan,
        "local_path_scan": local_scan,
        "final_passed": final_passed,
        "recommended_next_step": "push this closeout handoff commit, then verify the public repository and GitHub Pages site in the browser",
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_summary_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# AMCF Public Release Closeout Handoff Summary",
            "",
            "This is a software/public-release handoff record, not hardware proof.",
            "",
            f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
            f"- commit trail complete: {'yes' if report['commit_trail_complete'] else 'no'}",
            f"- required docs/source/demos/tests present: {'yes' if report['required_docs_present'] and report['required_source_present'] and report['required_demos_present'] and report['required_tests_present'] else 'no'}",
            f"- site present: {'yes' if report['site_present'] else 'no'}",
            f"- site links present: {'yes' if report['site_links_present'] else 'no'}",
            f"- generated output tracked: {'yes' if report['generated_output_tracked'] else 'no'}",
            f"- local path leak found: {'yes' if report['local_path_leak_found'] else 'no'}",
            f"- unsafe hardware claim found: {'yes' if report['unsafe_hardware_claim_found'] else 'no'}",
            f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
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
            "- Push the closeout handoff commit after local review.",
            "- Check the public GitHub repository and Pages deployment in the browser.",
            "- Preserve the software/control and no-hardware-validation wording in future public updates.",
            "",
        ]
    )


def write_closeout_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_closeout_handoff_report()
    write_json(output_dir / "closeout_handoff_report.json", report)
    write_json(output_dir / "closeout_commit_trail.json", report["commit_trail_summary"])
    write_json(output_dir / "closeout_validation_summary.json", {"unsafe_acceptance_count": report["unsafe_acceptance_count"], "final_passed": report["final_passed"]})
    write_json(output_dir / "closeout_claim_boundary_summary.json", report["claim_boundary_summary"])
    write_json(output_dir / "closeout_docs_site_summary.json", report["docs_site_summary"])
    write_json(output_dir / "closeout_generated_output_scan.json", report["generated_output_scan"])
    write_json(output_dir / "closeout_local_path_scan.json", report["local_path_scan"])
    (output_dir / "CLOSEOUT_HANDOFF_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    (output_dir / "NEXT_STEPS.md").write_text(build_next_steps_markdown(), encoding="utf-8")
    return report


def main() -> None:
    output_dir = PACKAGE / "output" / "public_release_closeout_handoff"
    report = write_closeout_outputs(output_dir)
    print(
        json.dumps(
            {
                "ok": bool(report["final_passed"]),
                "output_folder": str(output_dir),
                "commit_trail_complete": report["commit_trail_complete"],
                "generated_output_tracked": report["generated_output_tracked"],
                "local_path_leak_found": report["local_path_leak_found"],
                "unsafe_hardware_claim_found": report["unsafe_hardware_claim_found"],
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "physical_hardware_claimed": report["physical_hardware_claimed"],
                "hardware_validation_claimed": report["hardware_validation_claimed"],
                "physical_level_5_claimed": report["physical_level_5_claimed"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
