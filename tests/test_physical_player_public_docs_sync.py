from __future__ import annotations

import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


class PhysicalPlayerPublicDocsSyncTests(unittest.TestCase):
    def test_readme_links_to_docs_map(self) -> None:
        self.assertIn("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md", read_text("README.md"))

    def test_readme_links_to_simulator_demo_doc(self) -> None:
        self.assertIn("docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md", read_text("README.md"))

    def test_readme_contains_no_manufactured_hardware_claim_for_physical_player(self) -> None:
        readme = read_text("README.md").lower()
        self.assertNotIn("manufactured physical player exists", readme)
        self.assertNotIn("hardware validation is complete", readme)

    def test_claim_boundaries_contains_physical_player_software_control_boundary(self) -> None:
        self.assertIn("Physical Player Software-Control Simulator", read_text("CLAIM_BOUNDARIES.md"))

    def test_docs_map_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PHYSICAL_PLAYER_DOCS_MAP.md").exists())

    def test_docs_map_links_all_physical_player_docs(self) -> None:
        docs_map = read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
        for doc in [
            "docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md",
            "docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md",
            "docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md",
            "docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md",
            "docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md",
            "docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md",
            "docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md",
        ]:
            self.assertIn(doc, docs_map)

    def test_docs_map_links_all_five_demo_scripts(self) -> None:
        docs_map = read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
        for demo in [
            "demo/run_physical_player_state_machine_demo.py",
            "demo/run_physical_player_fail_closed_demo.py",
            "demo/run_physical_player_reverse_seek_demo.py",
            "demo/run_physical_player_mechanism_profiles_demo.py",
            "demo/run_physical_player_simulator_demo.py",
        ]:
            self.assertIn(demo, docs_map)

    def test_development_sequence_mentions_stages_two_through_seven(self) -> None:
        sequence = read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
        for stage in ["Stage 2", "Stage 3", "Stage 4", "Stage 5", "Stage 6", "Stage 7"]:
            self.assertIn(stage, sequence)

    def test_development_sequence_mentions_known_commits_for_stages_two_through_six(self) -> None:
        sequence = read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md")
        for commit in [
            "f8b6e91e1dfd9b57345ee38ac262635d446f47c8",
            "4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e",
            "802042b5395ac860c437188e0d79031d7dd5f591",
            "01093024f9bbd11d10615a0f526b4440e5f8f41b",
            "fea00409262dea39d5c9068daac0a206c02d07f5",
        ]:
            self.assertIn(commit, sequence)

    def test_docs_or_readme_mentions_unsafe_acceptance_zero(self) -> None:
        joined = read_text("README.md") + "\n" + read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
        self.assertIn("unsafe_acceptance_count", joined)
        self.assertIn("0", joined)

    def test_docs_or_readme_mentions_hardware_validation_not_claimed(self) -> None:
        joined = read_text("README.md").lower() + "\n" + read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md").lower()
        self.assertIn("hardware validation", joined)
        self.assertIn("not claimed", joined)

    def test_site_links_to_docs_map_or_simulator_demo(self) -> None:
        site = PACKAGE / "site" / "index.html"
        if site.exists():
            html = site.read_text(encoding="utf-8")
            self.assertTrue(
                "AMCF_PHYSICAL_PLAYER_DOCS_MAP.md" in html
                or "AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md" in html
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
