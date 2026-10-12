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
from run_physical_player_release_review import (  # noqa: E402
    scan_claim_boundaries,
    scan_generated_output,
    scan_local_paths,
)


RUN_NAME = "AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1"
BASE_COMMIT_HINT = "659bd3e74a9e4dd254600558aec6e76309ba596f"

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
    "docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md",
    "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md",
    "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md",
]

CORE_REPO_FILES = [
    "README.md",
    "CLAIM_BOUNDARIES.md",
    "PUBLICATION_STATUS.md",
    "LICENSE_MAP.md",
    "THIRD_PARTY_NOTICES.md",
    "RELEASE_MANIFEST.json",
    ".gitignore",
]

SITE_FILES = [
    "site/index.html",
    "site/styles.css",
    "site/README.md",
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


def exists_all(paths: list[str]) -> bool:
    return all((PACKAGE / path).exists() for path in paths)


def read_rel(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


def build_package_inventory() -> dict[str, Any]:
    return {
        "core_repo_files": {path: (PACKAGE / path).exists() for path in CORE_REPO_FILES},
        "physical_player_source_modules": {path: (PACKAGE / path).exists() for path in REQUIRED_SOURCE},
        "physical_player_demos": {path: (PACKAGE / path).exists() for path in REQUIRED_DEMOS},
        "physical_player_tests": {path: (PACKAGE / path).exists() for path in REQUIRED_TESTS},
        "physical_player_docs": {path: (PACKAGE / path).exists() for path in REQUIRED_DOCS},
        "site_public_pages": {path: (PACKAGE / path).exists() for path in SITE_FILES},
        "claim_boundary_files": {
            "CLAIM_BOUNDARIES.md": (PACKAGE / "CLAIM_BOUNDARIES.md").exists(),
            "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md": (PACKAGE / "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md").exists(),
            "docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md": (PACKAGE / "docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md").exists(),
        },
        "generated_output_policy": {
            "output/": "ignored demo/report artifacts, not committed",
            "demo/output/": "ignored demo artifacts, not committed",
        },
        "excluded_files_folders": [
            "output/",
            "demo/output/",
            "__pycache__/",
            "*.pyc",
            "checkpoints/",
            "models/",
            "weights/",
            "Tests/",
        ],
    }


def build_docs_and_site_checks() -> dict[str, Any]:
    readme = read_rel("README.md")
    docs_map = read_rel("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
    sequence = read_rel("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
    site_path = PACKAGE / "site" / "index.html"
    site_html = site_path.read_text(encoding="utf-8") if site_path.exists() else ""
    checks = {
        "readme_links_docs_map": "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in readme,
        "readme_links_package_refresh_or_inventory": (
            "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md" in readme
            or "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md" in readme
        ),
        "readme_links_release_review_doc": "docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md" in readme,
        "claim_boundaries_has_physical_player_boundary": "Physical Player Software-Control Simulator" in read_rel("CLAIM_BOUNDARIES.md"),
        "docs_map_includes_release_review_and_public_summary": (
            "docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md" in docs_map
            and "docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md" in docs_map
        ),
        "docs_map_links_package_refresh_or_inventory": (
            "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md" in docs_map
            or "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md" in docs_map
        ),
        "development_sequence_mentions_stages_2_to_8": all(f"Stage {number}" in sequence for number in range(2, 9)),
        "development_sequence_mentions_stage_9": "Stage 9" in sequence,
        "development_sequence_mentions_stage_8_commit": BASE_COMMIT_HINT in sequence,
        "release_review_doc_exists": (PACKAGE / "docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md").exists(),
        "release_review_script_exists": (PACKAGE / "demo/run_physical_player_release_review.py").exists(),
        "site_present": site_path.exists(),
        "site_links_present": (not site_path.exists())
        or ("AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in site_html and "AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md" in site_html),
    }
    return {"passed": all(checks.values()), "checks": checks}


def build_package_refresh_report() -> dict[str, Any]:
    inventory = build_package_inventory()
    docs_site = build_docs_and_site_checks()
    claim_scan = scan_claim_boundaries()
    local_scan = scan_local_paths()
    output_scan = scan_generated_output()
    integrated = build_integrated_simulation_summary()
    unsafe_count = int(integrated["unsafe_acceptance_audit"]["unsafe_acceptance_count"])
    required_source_present = exists_all(REQUIRED_SOURCE)
    required_demos_present = exists_all(REQUIRED_DEMOS)
    required_tests_present = exists_all(REQUIRED_TESTS)
    required_docs_present = exists_all(REQUIRED_DOCS)
    inventory_complete = (
        all(inventory["physical_player_source_modules"].values())
        and all(inventory["physical_player_demos"].values())
        and all(inventory["physical_player_tests"].values())
        and all(inventory["physical_player_docs"].values())
    )
    final_passed = (
        required_source_present
        and required_demos_present
        and required_tests_present
        and required_docs_present
        and docs_site["passed"]
        and not output_scan["generated_output_committed"]
        and not output_scan["generated_output_staged"]
        and local_scan["passed"]
        and claim_scan["passed"]
        and inventory_complete
        and unsafe_count == 0
        and all(value is False for value in CLAIM_VALUES_FALSE.values())
    )
    return {
        "run_name": RUN_NAME,
        "base_commit_hint": BASE_COMMIT_HINT,
        "required_docs_present": required_docs_present,
        "required_source_present": required_source_present,
        "required_demos_present": required_demos_present,
        "required_tests_present": required_tests_present,
        "site_present": docs_site["checks"]["site_present"],
        "site_links_present": docs_site["checks"]["site_links_present"],
        "generated_output_tracked": output_scan["generated_output_committed"] or output_scan["generated_output_staged"],
        "local_path_leak_found": not local_scan["passed"],
        "unsafe_hardware_claim_found": not claim_scan["passed"],
        "unsafe_acceptance_count": unsafe_count,
        **CLAIM_VALUES_FALSE,
        "docs_and_site_checks": docs_site,
        "package_inventory": inventory,
        "package_claim_boundary_scan": claim_scan,
        "package_local_path_scan": local_scan,
        "package_generated_output_scan": output_scan,
        "final_passed": final_passed,
        "recommended_next_step": "push this package-refresh commit, then continue future hardware-adapter alignment without hardware validation claims",
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_summary_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# AMCF Public Release Package Refresh Summary",
            "",
            "This is a software release/package refresh artifact, not hardware proof.",
            "",
            f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
            f"- required docs present: {'yes' if report['required_docs_present'] else 'no'}",
            f"- required source present: {'yes' if report['required_source_present'] else 'no'}",
            f"- required demos present: {'yes' if report['required_demos_present'] else 'no'}",
            f"- required tests present: {'yes' if report['required_tests_present'] else 'no'}",
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
            "- Push the package-refresh commit after local review.",
            "- Keep generated output folders and local package artifacts uncommitted.",
            "- Continue future hardware-adapter alignment without claiming manufactured hardware or hardware validation.",
            "",
        ]
    )


def write_package_refresh_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_package_refresh_report()
    write_json(output_dir / "package_refresh_report.json", report)
    write_json(output_dir / "package_inventory.json", report["package_inventory"])
    write_json(output_dir / "package_claim_boundary_scan.json", report["package_claim_boundary_scan"])
    write_json(output_dir / "package_local_path_scan.json", report["package_local_path_scan"])
    write_json(output_dir / "package_generated_output_scan.json", report["package_generated_output_scan"])
    (output_dir / "PACKAGE_REFRESH_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    (output_dir / "NEXT_STEPS.md").write_text(build_next_steps_markdown(), encoding="utf-8")
    return report


def main() -> None:
    output_dir = PACKAGE / "output" / "public_release_package_refresh"
    report = write_package_refresh_outputs(output_dir)
    print(
        json.dumps(
            {
                "ok": bool(report["final_passed"]),
                "output_folder": str(output_dir),
                "required_docs_present": report["required_docs_present"],
                "required_source_present": report["required_source_present"],
                "required_demos_present": report["required_demos_present"],
                "required_tests_present": report["required_tests_present"],
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
