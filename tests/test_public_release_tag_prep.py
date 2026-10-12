from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "demo"))

from run_public_release_tag_prep import build_release_tag_prep_report  # noqa: E402


def read_text(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


class PublicReleaseTagPrepTests(unittest.TestCase):
    def test_tag_prep_script_exists(self) -> None:
        self.assertTrue((PACKAGE / "demo" / "run_public_release_tag_prep.py").exists())

    def test_tag_prep_doc_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PUBLIC_RELEASE_TAG_PREP.md").exists())

    def test_release_notes_draft_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md").exists())

    def test_tag_checklist_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md").exists())

    def test_readme_or_docs_map_links_tag_prep_doc(self) -> None:
        joined = read_text("README.md") + "\n" + read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
        self.assertIn("docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md", joined)

    def test_docs_map_links_tag_prep_doc(self) -> None:
        self.assertIn("docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md", read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md"))

    def test_docs_map_links_release_notes_draft(self) -> None:
        self.assertIn("docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md", read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md"))

    def test_docs_map_links_tag_checklist(self) -> None:
        self.assertIn("docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md", read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md"))

    def test_site_links_tag_prep_or_release_notes_or_docs_map(self) -> None:
        html = read_text("site/index.html")
        self.assertTrue(
            "AMCF_PUBLIC_RELEASE_TAG_PREP.md" in html
            or "AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md" in html
            or "AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in html
        )

    def test_tag_prep_script_can_build_report_dict(self) -> None:
        report = build_release_tag_prep_report()
        self.assertIsInstance(report, dict)
        self.assertEqual(report["run_name"], "AMCF_PUBLIC_RELEASE_TAG_PREP_V1")

    def test_tag_prep_report_final_passed_true(self) -> None:
        self.assertTrue(build_release_tag_prep_report()["final_passed"])

    def test_tag_prep_report_tag_created_false(self) -> None:
        self.assertFalse(build_release_tag_prep_report()["tag_created"])

    def test_tag_prep_report_generated_output_tracked_false(self) -> None:
        self.assertFalse(build_release_tag_prep_report()["generated_output_tracked"])

    def test_tag_prep_report_local_path_leak_found_false(self) -> None:
        self.assertFalse(build_release_tag_prep_report()["local_path_leak_found"])

    def test_tag_prep_report_unsafe_hardware_claim_found_false(self) -> None:
        self.assertFalse(build_release_tag_prep_report()["unsafe_hardware_claim_found"])

    def test_tag_prep_report_physical_hardware_claimed_false(self) -> None:
        self.assertFalse(build_release_tag_prep_report()["physical_hardware_claimed"])

    def test_tag_prep_report_hardware_validation_claimed_false(self) -> None:
        self.assertFalse(build_release_tag_prep_report()["hardware_validation_claimed"])

    def test_tag_prep_report_physical_level_5_claimed_false(self) -> None:
        self.assertFalse(build_release_tag_prep_report()["physical_level_5_claimed"])

    def test_tag_prep_report_manufactured_player_claimed_false(self) -> None:
        self.assertFalse(build_release_tag_prep_report()["manufactured_player_claimed"])

    def test_release_notes_draft_includes_stage_11_commit(self) -> None:
        self.assertIn("331848fdf10ff18eab0a9426441f0f00e91a8f03", read_text("docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md"))

    def test_development_sequence_mentions_stage_12(self) -> None:
        self.assertIn("Stage 12", read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md"))

    def test_development_sequence_mentions_stage_11_commit(self) -> None:
        self.assertIn("331848fdf10ff18eab0a9426441f0f00e91a8f03", read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
