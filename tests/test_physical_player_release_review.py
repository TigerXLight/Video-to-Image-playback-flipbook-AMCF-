from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "demo"))

from run_physical_player_release_review import build_release_review_report  # noqa: E402


def read_text(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


class PhysicalPlayerReleaseReviewTests(unittest.TestCase):
    def test_docs_map_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PHYSICAL_PLAYER_DOCS_MAP.md").exists())

    def test_public_summary_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md").exists())

    def test_simulator_demo_doc_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md").exists())

    def test_readme_links_to_docs_map(self) -> None:
        self.assertIn("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md", read_text("README.md"))

    def test_readme_links_to_simulator_demo_doc(self) -> None:
        self.assertIn("docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md", read_text("README.md"))

    def test_claim_boundaries_contains_physical_player_boundary(self) -> None:
        self.assertIn("Physical Player Software-Control Simulator", read_text("CLAIM_BOUNDARIES.md"))

    def test_development_sequence_mentions_stages_two_through_seven(self) -> None:
        sequence = read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
        for stage in ["Stage 2", "Stage 3", "Stage 4", "Stage 5", "Stage 6", "Stage 7"]:
            self.assertIn(stage, sequence)

    def test_development_sequence_contains_known_commits(self) -> None:
        sequence = read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
        for commit in [
            "f8b6e91e1dfd9b57345ee38ac262635d446f47c8",
            "4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e",
            "802042b5395ac860c437188e0d79031d7dd5f591",
            "01093024f9bbd11d10615a0f526b4440e5f8f41b",
            "fea00409262dea39d5c9068daac0a206c02d07f5",
        ]:
            self.assertIn(commit, sequence)

    def test_site_links_to_physical_player_docs(self) -> None:
        site = PACKAGE / "site" / "index.html"
        if site.exists():
            html = site.read_text(encoding="utf-8")
            self.assertIn("AMCF_PHYSICAL_PLAYER_DOCS_MAP.md", html)
            self.assertIn("AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md", html)

    def test_public_docs_contain_no_local_windows_workspace_paths(self) -> None:
        report = build_release_review_report()
        self.assertTrue(report["local_path_scan"]["passed"], report["local_path_scan"]["hits"])

    def test_public_docs_contain_no_unsafe_affirmative_hardware_claims(self) -> None:
        report = build_release_review_report()
        self.assertTrue(report["claim_boundary_scan"]["passed"], report["claim_boundary_scan"]["unsafe_matches"])

    def test_release_review_script_can_build_report_dict(self) -> None:
        report = build_release_review_report()
        self.assertIsInstance(report, dict)
        self.assertEqual(report["run_name"], "AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1")

    def test_release_review_report_physical_hardware_claimed_false(self) -> None:
        self.assertFalse(build_release_review_report()["physical_hardware_claimed"])

    def test_release_review_report_hardware_validation_claimed_false(self) -> None:
        self.assertFalse(build_release_review_report()["hardware_validation_claimed"])

    def test_release_review_report_physical_level_5_claimed_false(self) -> None:
        self.assertFalse(build_release_review_report()["physical_level_5_claimed"])

    def test_release_review_report_unsafe_acceptance_count_zero(self) -> None:
        self.assertEqual(build_release_review_report()["unsafe_acceptance_count"], 0)

    def test_release_review_report_final_passed_true(self) -> None:
        self.assertTrue(build_release_review_report()["final_passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
