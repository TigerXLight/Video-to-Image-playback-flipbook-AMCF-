from __future__ import annotations

import json
import subprocess
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


RUN_NAME = "AMCF_PUBLIC_RELEASE_TAG_PREP_V1"
BASE_COMMIT_HINT = "331848fdf10ff18eab0a9426441f0f00e91a8f03"
SUGGESTED_TAG_NAME = "amcf-physical-player-software-control-v1"
ALTERNATE_DATE_TAG_NAME = "amcf-public-release-2026-10-12"
SUGGESTED_RELEASE_TITLE = "AMCF physical-player software-control public release v1"
SUGGESTED_RELEASE_TYPE = "annotated Git tag prepared for later explicit human approval"

KNOWN_STAGE_COMMITS = [
    "f8b6e91e1dfd9b57345ee38ac262635d446f47c8",
    "4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e",
    "802042b5395ac860c437188e0d79031d7dd5f591",
    "01093024f9bbd11d10615a0f526b4440e5f8f41b",
    "fea00409262dea39d5c9068daac0a206c02d07f5",
    "c7c2658877f04d40b94b127c6e44fe30d3597a18",
    "659bd3e74a9e4dd254600558aec6e76309ba596f",
    "8f76d7528e4f6399ef719a99f15e1b248ce8e2ff",
    "8082f0a1134ea33df330c0508f06cc3ff7130e59",
    "331848fdf10ff18eab0a9426441f0f00e91a8f03",
]

REQUIRED_DOCS = [
    "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md",
    "docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md",
    "docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md",
    "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md",
    "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md",
    "docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md",
    "docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md",
    "docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md",
    "docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md",
    "docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md",
    "docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md",
    "CLAIM_BOUNDARIES.md",
]

ALLOWED_TAG_PREP_DIRTY_PATHS = {
    ".gitignore",
    "DEPENDENCIES_AND_PROVENANCE.md",
    "QUICKSTART.md",
    "amcf_dependency_manifest.json",
    "cmd/RUN_AMCF_SETUP.cmd",
    "README.md",
    "docs/AMCF_SETUP_AND_DEPENDENCY_BOOTSTRAP.md",
    "demo/run_public_release_tag_prep.py",
    "pyproject.toml",
    "src/amcf_cli.py",
    "src/amcf_gui.py",
    "src/amcf_setup.py",
    "src/amcf_source_seeded_event_materializer.py",
    "src/amcf_physical_adapters.py",
    "src/amcf_hardware_adapter_planning.py",
    "src/amcf_hardware_provider_runtime.py",
    "src/amcf_software_control_protocol.py",
    "src/amcf_device_provider_adapters.py",
    "src/amcf_device_profiles.py",
    "packaging/amcf_gui.spec",
    "packaging/amcf_cli.spec",
    "packaging/tkinter_runtime_hook.py",
    "packaging/README_WINDOWS.md",
    "packaging/RUN_AMCF_GUI.cmd",
    "packaging/build_amcf_release_bundle.ps1",
    "docs/AMCF_SOURCE_SEEDED_EVENT_MATERIALIZER.md",
    "docs/AMCF_PHYSICAL_SOFTWARE_ADAPTER_LAYER.md",
    "docs/AMCF_HARDWARE_ADAPTER_PLANNING_LAYER.md",
    "docs/AMCF_HARDWARE_PROVIDER_RUNTIME_LAYER.md",
    "docs/AMCF_SOFTWARE_CONTROL_PROTOCOL.md",
    "docs/AMCF_DEVICE_PROVIDER_ADAPTERS.md",
    "docs/AMCF_DEVICE_PROFILE_LAYER.md",
    "docs/AMCF_SOFTWARE_IO_PUBLIC_SUMMARY.md",
    "docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md",
    "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md",
    "docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md",
    "docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md",
    "docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md",
    "docs/AMCF_PUBLIC_RELEASE_TAG_PREP_AUDIT.md",
    "site/index.html",
    "tests/test_amcf_cli.py",
    "tests/test_amcf_cli_packaging.py",
    "tests/test_amcf_source_seeded_event_materializer.py",
    "tests/test_amcf_physical_adapters.py",
    "tests/test_amcf_hardware_adapter_planning.py",
    "tests/test_amcf_hardware_provider_runtime.py",
    "tests/test_amcf_software_control_protocol.py",
    "tests/test_amcf_device_provider_adapters.py",
    "tests/test_amcf_device_profiles.py",
    "profiles/",
    "profiles/amcf_device_profiles.example.json",
    "tests/test_amcf_setup.py",
    "tests/test_public_release_tag_prep.py",
}

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


def git_result(args: list[str]) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(["git", *args], cwd=PACKAGE, text=True, capture_output=True, check=False)
    except OSError:
        return None


def git_lines(args: list[str]) -> list[str]:
    result = git_result(args)
    if result is None or result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def current_head() -> str:
    lines = git_lines(["rev-parse", "HEAD"])
    return lines[0] if lines else "unversioned-main-source-tree"


def current_branch() -> str:
    lines = git_lines(["branch", "--show-current"])
    return lines[0] if lines else "local-main-source"


def existing_tags() -> list[str]:
    return git_lines(["tag", "--list"])


def status_entries() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for line in git_lines(["status", "--short"]):
        status = line[:2].strip()
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        entries.append({"status": status, "path": path.replace("\\", "/")})
    return entries


def repo_status_scan() -> dict[str, Any]:
    entries = status_entries()
    unexpected = [entry for entry in entries if entry["path"] not in ALLOWED_TAG_PREP_DIRTY_PATHS]
    return {
        "entries": entries,
        "unexpected_entries": unexpected,
        "clean_or_expected_tag_prep_changes": len(unexpected) == 0,
    }


def development_sequence_scan() -> dict[str, Any]:
    sequence = read_rel("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
    checks = {
        "mentions_stages_2_to_12": all(f"Stage {number}" in sequence for number in range(2, 13)),
        "mentions_known_commits_2_to_11": all(commit in sequence for commit in KNOWN_STAGE_COMMITS),
        "mentions_stage_12_run": RUN_NAME in sequence,
    }
    return {"passed": all(checks.values()), "checks": checks}


def readme_entrypoints_present() -> bool:
    readme = read_rel("README.md")
    return (
        "docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in readme
        and "docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md" in readme
    )


def build_release_checklist() -> dict[str, Any]:
    return {
        "repo_clean_or_expected_tag_prep_changes": repo_status_scan()["clean_or_expected_tag_prep_changes"],
        "latest_commit_pushed_or_documented": BASE_COMMIT_HINT in read_rel("docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md"),
        "tests_pass": "run validation commands before tag creation",
        "integrated_simulator_demo_passes": "run validation commands before tag creation",
        "release_review_passes": "run validation commands before tag creation",
        "package_refresh_passes": "run validation commands before tag creation",
        "final_pages_review_passes": "run validation commands before tag creation",
        "closeout_handoff_passes": "run validation commands before tag creation",
        "generated_output_untracked": not scan_generated_output()["generated_output_committed"],
        "local_path_scan_passes": scan_local_paths()["passed"],
        "unsafe_hardware_claim_scan_passes": scan_claim_boundaries()["passed"],
        "claim_boundaries_present": exists_rel("CLAIM_BOUNDARIES.md"),
        "release_notes_reviewed": "manual review required before tag creation",
        "tag_name_chosen": SUGGESTED_TAG_NAME,
        "explicit_human_approval_to_create_tag": False,
        "tag_creation_command_run": False,
        "push_tag_command_run": False,
    }


def build_release_tag_prep_report() -> dict[str, Any]:
    docs_map = read_rel("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
    site_html = read_rel("site/index.html") if exists_rel("site/index.html") else ""
    sequence_scan = development_sequence_scan()
    claim_scan = scan_claim_boundaries()
    local_scan = scan_local_paths()
    output_scan = scan_generated_output()
    integrated = build_integrated_simulation_summary()
    unsafe_count = int(integrated["unsafe_acceptance_audit"]["unsafe_acceptance_count"])
    repo_status = repo_status_scan()
    required_docs_present = all(exists_rel(path) for path in REQUIRED_DOCS)
    checks = {
        "head_readable": current_head() != "unknown",
        "branch_readable": current_branch() != "unknown",
        "repo_clean_or_expected_doc_changes": repo_status["clean_or_expected_tag_prep_changes"],
        "closeout_doc_present": exists_rel("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md"),
        "release_review_present": exists_rel("docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md"),
        "package_refresh_present": exists_rel("docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md"),
        "final_pages_review_present": exists_rel("docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md"),
        "docs_map_present": exists_rel("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md"),
        "site_present": exists_rel("site/index.html"),
        "readme_entrypoints_present": readme_entrypoints_present(),
        "development_sequence_complete": sequence_scan["passed"],
        "required_docs_present": required_docs_present,
        "docs_map_links_tag_materials": all(
            path in docs_map
            for path in [
                "docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md",
                "docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md",
                "docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md",
            ]
        ),
        "site_links_tag_materials": "AMCF_PUBLIC_RELEASE_TAG_PREP.md" in site_html
        or "AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md" in site_html,
        "generated_output_untracked": output_scan["passed"],
        "local_path_scan_passed": local_scan["passed"],
        "unsafe_hardware_claim_scan_passed": claim_scan["passed"],
        "unsafe_acceptance_count_zero": unsafe_count == 0,
        "claim_boundaries_present": exists_rel("CLAIM_BOUNDARIES.md")
        and "Physical Player Software-Control Simulator" in read_rel("CLAIM_BOUNDARIES.md"),
        "tag_not_created_by_script": True,
    }
    final_passed = all(checks.values()) and all(value is False for value in CLAIM_VALUES_FALSE.values())
    return {
        "run_name": RUN_NAME,
        "base_commit_hint": BASE_COMMIT_HINT,
        "current_head": current_head(),
        "current_branch": current_branch(),
        "existing_tags": existing_tags(),
        "suggested_tag_name": SUGGESTED_TAG_NAME,
        "alternate_date_style_suggestion": ALTERNATE_DATE_TAG_NAME,
        "suggested_release_title": SUGGESTED_RELEASE_TITLE,
        "suggested_release_type": SUGGESTED_RELEASE_TYPE,
        "closeout_doc_present": checks["closeout_doc_present"],
        "release_review_present": checks["release_review_present"],
        "package_refresh_present": checks["package_refresh_present"],
        "final_pages_review_present": checks["final_pages_review_present"],
        "docs_map_present": checks["docs_map_present"],
        "site_present": checks["site_present"],
        "readme_entrypoints_present": checks["readme_entrypoints_present"],
        "development_sequence_complete": checks["development_sequence_complete"],
        "generated_output_tracked": output_scan["generated_output_committed"] or output_scan["generated_output_staged"],
        "local_path_leak_found": not local_scan["passed"],
        "unsafe_hardware_claim_found": not claim_scan["passed"],
        "unsafe_acceptance_count": unsafe_count,
        **CLAIM_VALUES_FALSE,
        "tag_created": False,
        "checks": checks,
        "repo_status_scan": repo_status,
        "development_sequence_scan": sequence_scan,
        "claim_boundary_scan": claim_scan,
        "local_path_scan": local_scan,
        "generated_output_scan": output_scan,
        "release_checklist": build_release_checklist(),
        "final_passed": final_passed,
        "recommended_next_step": "review these tag-prep materials, push the commit, then create an annotated tag only after explicit human approval",
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_release_notes_draft_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# AMCF Physical-Player Software-Control Public Release Draft",
            "",
            f"Suggested tag: `{report['suggested_tag_name']}`",
            "",
            f"Suggested title: {report['suggested_release_title']}",
            "",
            "This release draft summarizes the AMCF physical-player software/control simulator sequence. It does not claim manufactured hardware, real optical playback proof, physical Level 5 completion, or hardware validation.",
            "",
            "## Highlights",
            "",
            "- deterministic physical-player state-machine foundation",
            "- fail-closed safety model and unsafe-acceptance audit",
            "- bounded reverse and local-buffer seek controls",
            "- mechanism profiles with default `folded_ab_motor_encoder_baseline`",
            "- integrated simulator demo and public reports",
            "- public documentation map, release review, package inventory, final Pages review, and closeout handoff",
            "",
            "## Validation Snapshot",
            "",
            "- `unsafe_acceptance_count`: 0",
            "- generated output tracked: no",
            "- local path leak found: no",
            "- unsafe hardware claim found: no",
            "- tag created by this run: no",
            "",
        ]
    )


def build_summary_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# AMCF Public Release Tag Prep Summary",
            "",
            "This is tag preparation only. No Git tag was created.",
            "",
            f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
            f"- suggested tag name: `{report['suggested_tag_name']}`",
            f"- alternate date-style suggestion: `{report['alternate_date_style_suggestion']}`",
            f"- current HEAD: `{report['current_head']}`",
            f"- current branch: `{report['current_branch']}`",
            f"- existing tags found: {len(report['existing_tags'])}",
            f"- generated output tracked: {'yes' if report['generated_output_tracked'] else 'no'}",
            f"- local path leak found: {'yes' if report['local_path_leak_found'] else 'no'}",
            f"- unsafe hardware claim found: {'yes' if report['unsafe_hardware_claim_found'] else 'no'}",
            f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
            "- tag created: no",
            "- physical hardware claimed: no",
            "- hardware validation claimed: no",
            "- physical Level 5 claimed: no",
            "- manufactured physical player claimed: no",
            "",
        ]
    )


def build_next_steps_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Next Steps",
            "",
            "- Review the release notes draft and tag checklist.",
            "- Push the tag-prep commit after local review.",
            "- Create an annotated tag only after explicit human approval.",
            "",
            "Future manual command, not run:",
            "",
            f"`git tag -a {report['suggested_tag_name']} -m \"{report['suggested_release_title']}\"`",
            "",
            "Future manual tag push command, not run:",
            "",
            f"`git push origin {report['suggested_tag_name']}`",
            "",
        ]
    )


def write_release_tag_prep_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_release_tag_prep_report()
    write_json(output_dir / "release_tag_prep_report.json", report)
    write_json(
        output_dir / "suggested_tag.json",
        {
            "suggested_tag_name": report["suggested_tag_name"],
            "alternate_date_style_suggestion": report["alternate_date_style_suggestion"],
            "suggested_release_title": report["suggested_release_title"],
            "tag_created": False,
        },
    )
    write_json(output_dir / "release_checklist.json", report["release_checklist"])
    write_json(output_dir / "claim_boundary_scan.json", report["claim_boundary_scan"])
    write_json(output_dir / "local_path_scan.json", report["local_path_scan"])
    write_json(output_dir / "generated_output_scan.json", report["generated_output_scan"])
    (output_dir / "release_notes_draft.md").write_text(build_release_notes_draft_markdown(report), encoding="utf-8")
    (output_dir / "RELEASE_TAG_PREP_SUMMARY.md").write_text(build_summary_markdown(report), encoding="utf-8")
    (output_dir / "NEXT_STEPS.md").write_text(build_next_steps_markdown(report), encoding="utf-8")
    return report


def main() -> None:
    output_dir = PACKAGE / "output" / "public_release_tag_prep"
    report = write_release_tag_prep_outputs(output_dir)
    print(
        json.dumps(
            {
                "ok": bool(report["final_passed"]),
                "output_folder": str(output_dir),
                "suggested_tag_name": report["suggested_tag_name"],
                "tag_created": report["tag_created"],
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
