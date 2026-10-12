from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "demo"))

from run_public_release_package_refresh import (  # noqa: E402
    REQUIRED_DEMOS,
    REQUIRED_DOCS,
    REQUIRED_TESTS,
    build_package_refresh_report,
)


def read_text(path: str) -> str:
    return (PACKAGE / path).read_text(encoding="utf-8")


class PublicReleasePackageRefreshTests(unittest.TestCase):
    def test_package_refresh_script_exists(self) -> None:
        self.assertTrue((PACKAGE / "demo" / "run_public_release_package_refresh.py").exists())

    def test_package_refresh_doc_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md").exists())

    def test_package_inventory_doc_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md").exists())

    def test_readme_links_to_package_refresh_or_inventory_doc(self) -> None:
        readme = read_text("README.md")
        self.assertTrue(
            "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md" in readme
            or "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md" in readme
        )

    def test_docs_map_links_to_package_refresh_or_inventory_doc(self) -> None:
        docs_map = read_text("docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md")
        self.assertTrue(
            "docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md" in docs_map
            or "docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md" in docs_map
        )

    def test_package_refresh_script_can_build_report_dict(self) -> None:
        report = build_package_refresh_report()
        self.assertIsInstance(report, dict)
        self.assertEqual(report["run_name"], "AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1")

    def test_package_refresh_report_final_passed_true(self) -> None:
        self.assertTrue(build_package_refresh_report()["final_passed"])

    def test_package_refresh_report_generated_output_tracked_false(self) -> None:
        self.assertFalse(build_package_refresh_report()["generated_output_tracked"])

    def test_package_refresh_report_local_path_leak_found_false(self) -> None:
        self.assertFalse(build_package_refresh_report()["local_path_leak_found"])

    def test_package_refresh_report_unsafe_hardware_claim_found_false(self) -> None:
        self.assertFalse(build_package_refresh_report()["unsafe_hardware_claim_found"])

    def test_package_refresh_report_physical_hardware_claimed_false(self) -> None:
        self.assertFalse(build_package_refresh_report()["physical_hardware_claimed"])

    def test_package_refresh_report_hardware_validation_claimed_false(self) -> None:
        self.assertFalse(build_package_refresh_report()["hardware_validation_claimed"])

    def test_package_refresh_report_physical_level_5_claimed_false(self) -> None:
        self.assertFalse(build_package_refresh_report()["physical_level_5_claimed"])

    def test_package_refresh_report_manufactured_player_claimed_false(self) -> None:
        self.assertFalse(build_package_refresh_report()["manufactured_player_claimed"])

    def test_package_inventory_lists_all_physical_player_demos(self) -> None:
        inventory = read_text("docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md")
        for path in REQUIRED_DEMOS:
            self.assertIn(path, inventory)

    def test_package_inventory_lists_all_physical_player_tests(self) -> None:
        inventory = read_text("docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md")
        for path in REQUIRED_TESTS:
            self.assertIn(path, inventory)

    def test_package_inventory_lists_all_physical_player_docs(self) -> None:
        inventory = read_text("docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md")
        for path in REQUIRED_DOCS:
            self.assertIn(path, inventory)

    def test_development_sequence_mentions_stage_9(self) -> None:
        self.assertIn("Stage 9", read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md"))

    def test_development_sequence_mentions_stage_8_commit(self) -> None:
        self.assertIn(
            "659bd3e74a9e4dd254600558aec6e76309ba596f",
            read_text("docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
