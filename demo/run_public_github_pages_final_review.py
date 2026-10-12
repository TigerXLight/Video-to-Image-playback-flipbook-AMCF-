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


RUN_NAME = "AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1"
BASE_COMMIT_HINT = "8f76d7528e4f6399ef719a99f15e1b248ce8e2ff"

PHYSICAL_PLAYER_DOC_CHAIN = [
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
    "docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md",
    "CLAIM_BOUNDARIES.md",
    "docs/AMCF_HARDWARE_SOFTWARE_PATHS.md",
]

KNOWN_STAGE_COMMITS = [
    "f8b6e91e1dfd9b57345ee38ac262635d446f47c8",
    "4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e",
    "802042b5395ac860c437188e0d79031d7dd5f591",
    "01093024f9bbd11d10615a0f526b4440e5f8f41b",
    "fea00409262dea39d5c9068daac0a206c02d07f5",
    "c7c2658877f04d40b94b127c6e44fe30d3597a18",
    "659bd3e74a9e4dd254600558aec6e76309ba596f",
    "8f76d7528e4f6399ef719a99f15e1b248ce8e2ff",
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


def read_rel(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


def exists_rel(path: str) -> bool:
    return (PACKAGE / path).exists()


def build_readme_entrypoint_scan() -> dict[str, Any]:
    readme = read_rel("README.md") if exists_rel("README.md") else ""
    checks = {
        "readme_exists": exists_rel("README.md"),
        "links_docs_map": "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in readme,
        "links_public_summary_or_simulator_docs": (
            "docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md" in readme
            or "docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md" in readme
        ),
        "links_package_refresh_or_inventory": (
            "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md" in readme
            or "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md" in readme
        ),
        "links_final_review": "docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md" in readme,
    }
    return {"passed": all(checks.values()), "checks": checks}


def build_docs_map_scan() -> dict[str, Any]:
    docs_map_path = "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md"
    docs_map = read_rel(docs_map_path) if exists_rel(docs_map_path) else ""
    checks = {
        "docs_map_present": exists_rel(docs_map_path),
        "links_full_physical_player_doc_chain": all(path in docs_map for path in PHYSICAL_PLAYER_DOC_CHAIN if path.startswith("docs/") or path == "CLAIM_BOUNDARIES.md"),
        "links_release_review": "docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md" in docs_map,
        "links_package_refresh": "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md" in docs_map,
        "links_package_inventory": "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md" in docs_map,
        "links_final_pages_review": "docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md" in docs_map,
    }
    return {"passed": all(checks.values()), "checks": checks}


def build_site_link_scan() -> dict[str, Any]:
    site_path = PACKAGE / "site" / "index.html"
    html = site_path.read_text(encoding="utf-8") if site_path.exists() else ""
    checks = {
        "site_present": site_path.exists(),
        "links_docs_map_or_public_summary": (
            "AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in html
            or "AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md" in html
        ),
        "links_simulator_or_release_package_docs": (
            "AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md" in html
            or "AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md" in html
            or "AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md" in html
            or "AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md" in html
        ),
        "links_claim_boundaries": "CLAIM_BOUNDARIES.md" in html,
    }
    return {"passed": all(checks.values()), "checks": checks}


def build_public_navigation_scan() -> dict[str, Any]:
    readme_scan = build_readme_entrypoint_scan()
    docs_map_scan = build_docs_map_scan()
    site_scan = build_site_link_scan()
    checks = {
        "readme_entrypoints_present": readme_scan["passed"],
        "docs_map_present": docs_map_scan["checks"]["docs_map_present"],
        "docs_map_complete": docs_map_scan["passed"],
        "public_summary_present": exists_rel("docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md"),
        "release_review_linked": docs_map_scan["checks"]["links_release_review"],
        "package_inventory_linked": docs_map_scan["checks"]["links_package_inventory"],
        "package_refresh_linked": docs_map_scan["checks"]["links_package_refresh"],
        "site_present": site_scan["checks"]["site_present"],
        "site_links_present": site_scan["passed"],
        "release_review_script_exists": exists_rel("demo/run_physical_player_release_review.py"),
        "package_refresh_script_exists": exists_rel("demo/run_public_release_package_refresh.py"),
        "integrated_simulator_demo_script_exists": exists_rel("demo/run_physical_player_simulator_demo.py"),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "readme_entrypoint_scan": readme_scan,
        "docs_map_scan": docs_map_scan,
        "site_link_scan": site_scan,
    }


def build_development_sequence_scan() -> dict[str, Any]:
    sequence = read_rel("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
    checks = {
        "mentions_stages_2_to_9": all(f"Stage {number}" in sequence for number in range(2, 10)),
        "mentions_stage_10": "Stage 10" in sequence,
        "mentions_known_commits_2_to_9": all(commit in sequence for commit in KNOWN_STAGE_COMMITS),
    }
    return {"passed": all(checks.values()), "checks": checks}


def build_final_pages_review_report() -> dict[str, Any]:
    navigation = build_public_navigation_scan()
    sequence_scan = build_development_sequence_scan()
    claim_scan = scan_claim_boundaries()
    local_scan = scan_local_paths()
    output_scan = scan_generated_output()
    integrated = build_integrated_simulation_summary()
    unsafe_count = int(integrated["unsafe_acceptance_audit"]["unsafe_acceptance_count"])
    final_passed = (
        navigation["passed"]
        and sequence_scan["passed"]
        and claim_scan["passed"]
        and local_scan["passed"]
        and output_scan["passed"]
        and unsafe_count == 0
        and all(value is False for value in CLAIM_VALUES_FALSE.values())
    )
    return {
        "run_name": RUN_NAME,
        "base_commit_hint": BASE_COMMIT_HINT,
        "site_present": navigation["checks"]["site_present"],
        "site_links_present": navigation["checks"]["site_links_present"],
        "readme_entrypoints_present": navigation["checks"]["readme_entrypoints_present"],
        "docs_map_present": navigation["checks"]["docs_map_present"],
        "docs_map_complete": navigation["checks"]["docs_map_complete"],
        "public_summary_present": navigation["checks"]["public_summary_present"],
        "release_review_linked": navigation["checks"]["release_review_linked"],
        "package_inventory_linked": navigation["checks"]["package_inventory_linked"],
        "package_refresh_linked": navigation["checks"]["package_refresh_linked"],
        "claim_boundaries_present": exists_rel("CLAIM_BOUNDARIES.md") and "Physical Player Software-Control Simulator" in read_rel("CLAIM_BOUNDARIES.md"),
        "generated_output_tracked": output_scan["generated_output_committed"] or output_scan["generated_output_staged"],
        "local_path_leak_found": not local_scan["passed"],
        "unsafe_hardware_claim_found": not claim_scan["passed"],
        "unsafe_acceptance_count": unsafe_count,
        **CLAIM_VALUES_FALSE,
        "public_navigation_scan": navigation,
        "development_sequence_scan": sequence_scan,
        "claim_boundary_scan": claim_scan,
        "local_path_scan": local_scan,
        "generated_output_scan": output_scan,
        "final_passed": final_passed,
        "recommended_next_step": "push this final public Pages review commit, then verify the published GitHub Pages action output in the browser",
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_summary_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# AMCF Public GitHub Pages Final Review Summary",
            "",
            "This is a public documentation/release-readiness artifact, not hardware proof.",
            "",
            f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
            f"- site present: {'yes' if report['site_present'] else 'no'}",
            f"- site links present: {'yes' if report['site_links_present'] else 'no'}",
            f"- README entry points present: {'yes' if report['readme_entrypoints_present'] else 'no'}",
            f"- docs map complete: {'yes' if report['docs_map_complete'] else 'no'}",
            f"- release review linked: {'yes' if report['release_review_linked'] else 'no'}",
            f"- package inventory linked: {'yes' if report['package_inventory_linked'] else 'no'}",
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
            "- Push the final Pages review commit after local review.",
            "- Confirm the GitHub Pages workflow publishes the updated site.",
            "- Keep future public wording within the same software/control and no-hardware-validation boundary.",
            "",
        ]
    )


def write_final_pages_review_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_final_pages_review_report()
    write_json(output_dir / "github_pages_final_review_report.json", report)
    write_json(output_dir / "public_navigation_scan.json", report["public_navigation_scan"])
    write_json(output_dir / "readme_entrypoint_scan.json", report["public_navigation_scan"]["readme_entrypoint_scan"])
    write_json(output_dir / "docs_map_scan.json", report["public_navigation_scan"]["docs_map_scan"])
    write_json(output_dir / "site_link_scan.json", report["public_navigation_scan"]["site_link_scan"])
    write_json(output_dir / "claim_boundary_scan.json", report["claim_boundary_scan"])
    write_json(output_dir / "local_path_scan.json", report["local_path_scan"])
    write_json(output_dir / "generated_output_scan.json", report["generated_output_scan"])
    (output_dir / "GITHUB_PAGES_FINAL_REVIEW_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    (output_dir / "NEXT_STEPS.md").write_text(build_next_steps_markdown(), encoding="utf-8")
    return report


def main() -> None:
    output_dir = PACKAGE / "output" / "public_github_pages_final_review"
    report = write_final_pages_review_outputs(output_dir)
    print(
        json.dumps(
            {
                "ok": bool(report["final_passed"]),
                "output_folder": str(output_dir),
                "site_present": report["site_present"],
                "site_links_present": report["site_links_present"],
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
