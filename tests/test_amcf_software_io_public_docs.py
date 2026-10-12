from __future__ import annotations

import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


class AMCFSoftwareIOPublicDocsTests(unittest.TestCase):
    def test_software_io_docs_map_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_SOFTWARE_IO_DOCS_MAP.md").exists())

    def test_public_summary_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_SOFTWARE_IO_PUBLIC_SUMMARY.md").exists())

    def test_release_review_refresh_exists(self) -> None:
        self.assertTrue((PACKAGE / "docs" / "AMCF_SOFTWARE_IO_RELEASE_REVIEW_REFRESH.md").exists())

    def test_readme_links_to_software_io_docs_map(self) -> None:
        readme = (PACKAGE / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/AMCF_SOFTWARE_IO_DOCS_MAP.md", readme)

    def test_docs_map_links_all_corridor_docs(self) -> None:
        docs_map = (PACKAGE / "docs" / "AMCF_SOFTWARE_IO_DOCS_MAP.md").read_text(encoding="utf-8")
        for path in (
            "docs/AMCF_SHARED_PACKAGE_MANIFEST_MODEL.md",
            "docs/AMCF_CROSS_CORRIDOR_REPORTING_MODEL.md",
            "docs/AMCF_PC_TO_PRINTER_SOFTWARE_PATH.md",
            "docs/AMCF_PC_READER_SOFTWARE_PATH.md",
            "docs/AMCF_PLAYER_PC_SOFTWARE_PATH.md",
            "docs/AMCF_CROSS_CORRIDOR_ROUNDTRIP.md",
            "docs/AMCF_CROSS_CORRIDOR_MUTATION_SAFETY.md",
        ):
            self.assertIn(path, docs_map)

    def test_public_summary_keeps_claim_flags_false(self) -> None:
        summary = (PACKAGE / "docs" / "AMCF_SOFTWARE_IO_PUBLIC_SUMMARY.md").read_text(encoding="utf-8")
        self.assertIn("hardware validation claimed: false", summary)
        self.assertIn("physical Level 5 claimed: false", summary)
        self.assertIn("manufactured player claimed: false", summary)

    def test_site_links_to_software_io_docs(self) -> None:
        site = (PACKAGE / "site" / "index.html").read_text(encoding="utf-8")
        self.assertIn("AMCF_SOFTWARE_IO_DOCS_MAP.md", site)
        self.assertIn("AMCF_SOFTWARE_IO_PUBLIC_SUMMARY.md", site)

    def test_no_hardware_overclaim_in_new_docs(self) -> None:
        for name in (
            "AMCF_SOFTWARE_IO_DOCS_MAP.md",
            "AMCF_SOFTWARE_IO_PUBLIC_SUMMARY.md",
            "AMCF_SOFTWARE_IO_RELEASE_REVIEW_REFRESH.md",
        ):
            text = (PACKAGE / "docs" / name).read_text(encoding="utf-8").lower()
            self.assertNotIn("hardware validation claimed: true", text)
            self.assertNotIn("physical level 5 claimed: true", text)
            self.assertNotIn("manufactured player claimed: true", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
