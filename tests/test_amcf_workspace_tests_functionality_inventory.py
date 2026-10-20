from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_workspace_tests_functionality_inventory import (  # noqa: E402
    build_workspace_tests_inventory,
    classify_code_file,
)


class WorkspaceTestsFunctionalityInventoryTests(unittest.TestCase):
    def test_classifier_identifies_machine_specific_wrapper(self) -> None:
        classification, reasons = classify_code_file(
            "Test 03K/RUN_TEST03K.cmd",
            'cd /d "T:\\References\\to go\\Media\\tools\\Video to Image"\n',
            {"hash": [], "name": []},
        )
        self.assertEqual(classification, "LOCAL_MACHINE_SPECIFIC_WRAPPER_NEEDS_PORTABLE_EQUIVALENT")
        self.assertTrue(reasons)

    def test_classifier_identifies_archive_tool_candidate(self) -> None:
        classification, _reasons = classify_code_file(
            "Test AMCF_ARCHIVE_WRITER_READER_INTEGRATION/amcf_archive_writer_v_next.py",
            "def write_archive(): pass\n",
            {"hash": [], "name": []},
        )
        self.assertEqual(classification, "CORE_ARCHIVE_TOOL_CANDIDATE")

    def test_classifier_identifies_deep_research_surface(self) -> None:
        classification, _reasons = classify_code_file(
            "Test 03C/run_samurai_microproof_03c.py",
            "SAMURAI microproof\n",
            {"hash": [], "name": []},
        )
        self.assertEqual(classification, "OPTIONAL_DEEP_RESEARCH_OR_DATASET_SPECIFIC")

    def test_inventory_uses_public_hash_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            public = root / "public"
            tests = root / "Tests"
            (public / "src").mkdir(parents=True)
            tests.mkdir()
            (public / "src" / "same.py").write_text("print('same')\n", encoding="utf-8")
            (tests / "same.py").write_text("print('same')\n", encoding="utf-8")
            report = build_workspace_tests_inventory(public, tests)
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["code_files_checked"], 1)
        self.assertEqual(report["files"][0]["classification"], "PUBLIC_EXACT_MATCH")
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary_flags"]["hardware_validation_claimed"])
        self.assertFalse(report["claim_boundary_flags"]["physical_level_5_claimed"])
        self.assertFalse(report["claim_boundary_flags"]["manufactured_player_claimed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
