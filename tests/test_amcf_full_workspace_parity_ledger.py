from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amcf_full_workspace_parity_ledger import (
    build_full_workspace_parity_ledger,
    build_hierarchy_address_list_text,
    classify_workspace_path,
    write_full_workspace_parity_outputs,
)


class FullWorkspaceParityLedgerTests(unittest.TestCase):
    def test_classifier_marks_amcf_code_as_priority(self) -> None:
        decision, reason = classify_workspace_path("Tests/Test 04F_05A/run_amcf_archive_writer.py")
        self.assertEqual(decision, "INSPECT_PRIORITY")
        self.assertIn("AMCF", reason)

    def test_classifier_marks_generated_output_do_not_copy(self) -> None:
        decision, _reason = classify_workspace_path("Tests/Test 05B/built_archives/sample.amcfv0.zip")
        self.assertEqual(decision, "GENERATED_DO_NOT_COPY")

    def test_classifier_marks_reference_dependency_review(self) -> None:
        decision, _reason = classify_workspace_path("Tests/sam2/modeling/sam2_video_predictor.py")
        self.assertEqual(decision, "THIRD_PARTY_REFERENCE")

    def test_builds_public_safe_ledger_and_hierarchy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            public = root / "Tests" / "A" / "B" / "C" / "D" / "public"
            workspace = root / "workspace"
            public.mkdir(parents=True)
            (workspace / "Tests" / "Test 01").mkdir(parents=True)
            (workspace / "Tests" / "Test 01" / "run_amcf_archive.py").write_text("print('amcf')\n", encoding="utf-8")
            (workspace / "Tests" / "Test 01" / "output").mkdir()
            (workspace / "Tests" / "Test 01" / "output" / "archive.zip").write_bytes(b"zip")

            report = build_full_workspace_parity_ledger(public, workspace)
            outputs = write_full_workspace_parity_outputs(report, root / "out")
            hierarchy = build_hierarchy_address_list_text(report)
            self.assertTrue(Path(outputs["hierarchy_address_list"]).exists())

        self.assertTrue(report["final_passed"])
        self.assertEqual(report["file_count"], 2)
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary_flags"]["hardware_validation_claimed"])
        self.assertIn("<workspace-root>/Tests/Test 01/run_amcf_archive.py", hierarchy)


if __name__ == "__main__":
    unittest.main()

