from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "demo"))

from run_public_github_pages_final_review import build_final_pages_review_report  # noqa: E402


def read_text(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


class PublicGithubPagesFinalReviewTests(unittest.TestCase):
    def test_final_review_script_exists(self) -> None:
        self.assertTrue((PACKAGE / "demo" / "run_public_github_pages_final_review.py").exists())

    def test_final_review_doc_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md").exists())

    def test_readme_or_docs_map_links_to_final_review_doc(self) -> None:
        joined = read_text("README.md") + "\n" + read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
        self.assertIn("docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md", joined)

    def test_docs_map_links_to_final_review_doc(self) -> None:
        self.assertIn("docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md", read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md"))

    def test_site_index_exists(self) -> None:
        self.assertTrue((PACKAGE / "site" / "index.html").exists())

    def test_site_links_to_docs_map_or_public_summary(self) -> None:
        html = read_text("site/index.html")
        self.assertTrue("AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in html or "AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md" in html)

    def test_site_links_to_release_review_or_package_inventory(self) -> None:
        html = read_text("site/index.html")
        self.assertTrue("AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md" in html or "AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md" in html)

    def test_final_review_script_can_build_report_dict(self) -> None:
        report = build_final_pages_review_report()
        self.assertIsInstance(report, dict)
        self.assertEqual(report["run_name"], "AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1")

    def test_final_review_report_final_passed_true(self) -> None:
        self.assertTrue(build_final_pages_review_report()["final_passed"])

    def test_final_review_report_site_present_true(self) -> None:
        self.assertTrue(build_final_pages_review_report()["site_present"])

    def test_final_review_report_site_links_present_true(self) -> None:
        self.assertTrue(build_final_pages_review_report()["site_links_present"])

    def test_final_review_report_generated_output_tracked_false(self) -> None:
        self.assertFalse(build_final_pages_review_report()["generated_output_tracked"])

    def test_final_review_report_local_path_leak_found_false(self) -> None:
        self.assertFalse(build_final_pages_review_report()["local_path_leak_found"])

    def test_final_review_report_unsafe_hardware_claim_found_false(self) -> None:
        self.assertFalse(build_final_pages_review_report()["unsafe_hardware_claim_found"])

    def test_final_review_report_physical_hardware_claimed_false(self) -> None:
        self.assertFalse(build_final_pages_review_report()["physical_hardware_claimed"])

    def test_final_review_report_hardware_validation_claimed_false(self) -> None:
        self.assertFalse(build_final_pages_review_report()["hardware_validation_claimed"])

    def test_final_review_report_physical_level_5_claimed_false(self) -> None:
        self.assertFalse(build_final_pages_review_report()["physical_level_5_claimed"])

    def test_final_review_report_manufactured_player_claimed_false(self) -> None:
        self.assertFalse(build_final_pages_review_report()["manufactured_player_claimed"])

    def test_development_sequence_mentions_stage_10(self) -> None:
        self.assertIn("Stage 10", read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md"))

    def test_development_sequence_mentions_stage_9_commit(self) -> None:
        self.assertIn(
            "8f76d7528e4f6399ef719a99f15e1b248ce8e2ff",
            read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
