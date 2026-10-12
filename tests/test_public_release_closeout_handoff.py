from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "demo"))

from run_public_release_closeout_handoff import COMMIT_TRAIL, build_closeout_handoff_report  # noqa: E402


def read_text(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


class PublicReleaseCloseoutHandoffTests(unittest.TestCase):
    def test_closeout_handoff_script_exists(self) -> None:
        self.assertTrue((PACKAGE / "demo" / "run_public_release_closeout_handoff.py").exists())

    def test_closeout_handoff_doc_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md").exists())

    def test_readme_or_docs_map_links_to_closeout_handoff_doc(self) -> None:
        joined = read_text("README.md") + "\n" + read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
        self.assertIn("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md", joined)

    def test_docs_map_links_to_closeout_handoff_doc(self) -> None:
        self.assertIn("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md", read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md"))

    def test_site_links_to_closeout_or_docs_map(self) -> None:
        html = read_text("site/index.html")
        self.assertTrue("AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md" in html or "AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in html)

    def test_closeout_script_can_build_report_dict(self) -> None:
        report = build_closeout_handoff_report()
        self.assertIsInstance(report, dict)
        self.assertEqual(report["run_name"], "AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1")

    def test_closeout_report_final_passed_true(self) -> None:
        self.assertTrue(build_closeout_handoff_report()["final_passed"])

    def test_closeout_report_commit_trail_complete_true(self) -> None:
        self.assertTrue(build_closeout_handoff_report()["commit_trail_complete"])

    def test_closeout_report_generated_output_tracked_false(self) -> None:
        self.assertFalse(build_closeout_handoff_report()["generated_output_tracked"])

    def test_closeout_report_local_path_leak_found_false(self) -> None:
        self.assertFalse(build_closeout_handoff_report()["local_path_leak_found"])

    def test_closeout_report_unsafe_hardware_claim_found_false(self) -> None:
        self.assertFalse(build_closeout_handoff_report()["unsafe_hardware_claim_found"])

    def test_closeout_report_physical_hardware_claimed_false(self) -> None:
        self.assertFalse(build_closeout_handoff_report()["physical_hardware_claimed"])

    def test_closeout_report_hardware_validation_claimed_false(self) -> None:
        self.assertFalse(build_closeout_handoff_report()["hardware_validation_claimed"])

    def test_closeout_report_physical_level_5_claimed_false(self) -> None:
        self.assertFalse(build_closeout_handoff_report()["physical_level_5_claimed"])

    def test_closeout_report_manufactured_player_claimed_false(self) -> None:
        self.assertFalse(build_closeout_handoff_report()["manufactured_player_claimed"])

    def test_closeout_handoff_doc_mentions_stages_two_through_eleven(self) -> None:
        handoff = read_text("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md")
        for number in range(2, 12):
            self.assertIn(f"Stage {number}", handoff)

    def test_closeout_handoff_doc_includes_commits_for_stages_two_through_ten(self) -> None:
        handoff = read_text("docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md")
        for item in COMMIT_TRAIL:
            if item["commit"] != "current run, not committed yet":
                self.assertIn(item["commit"], handoff)

    def test_development_sequence_mentions_stage_11(self) -> None:
        self.assertIn("Stage 11", read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md"))

    def test_development_sequence_mentions_stage_10_commit(self) -> None:
        self.assertIn(
            "8082f0a1134ea33df330c0508f06cc3ff7130e59",
            read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
