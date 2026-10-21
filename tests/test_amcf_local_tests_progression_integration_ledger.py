from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amcf_local_tests_progression_integration_ledger import (  # noqa: E402
    build_markdown_summary,
    build_progression_integration_ledger,
    compare_main_exact_mappings,
    compare_public_v2_to_local_14f,
    summary_parts_found,
    write_progression_integration_outputs,
)
from amcf_local_main_strict_parity import default_paths  # noqa: E402


class LocalTestsProgressionIntegrationLedgerTests(unittest.TestCase):
    def test_summary_part_detection(self) -> None:
        text = "_+Part 149_+\nhello\n_+Part 191_+\nbye\n"
        self.assertEqual(summary_parts_found(text, (149, 150, 191)), {"149": True, "150": False, "191": True})

    def test_builds_report_with_claim_boundaries_false(self) -> None:
        report = build_progression_integration_ledger(REPO_ROOT)
        self.assertTrue(report["final_passed"])
        self.assertFalse(report["full_parity_claimed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary_flags"]["hardware_validation_claimed"])
        self.assertFalse(report["claim_boundary_flags"]["physical_level_5_claimed"])
        self.assertFalse(report["claim_boundary_flags"]["manufactured_player_claimed"])
        self.assertIn("AMCF_DIAGNOSTIC_PROFILE_BUNDLE_COMPLETION_V1", report["recommended_next_phase"])

    def test_report_includes_expected_progression_groups(self) -> None:
        report = build_progression_integration_ledger(REPO_ROOT)
        groups = {row["group_id"]: row for row in report["progression_groups"]}
        self.assertIn("test02_latest_diagnostic_archive", groups)
        self.assertIn("v2_14b_14c_14d_14f_package", groups)
        self.assertEqual(groups["test02_latest_diagnostic_archive"]["status"], "NEEDS_TARGETED_DIAGNOSTIC_PARITY_REVIEW")
        self.assertIn("test02_latest_diagnostic_archive", report["diagnostic_gap_groups"])

    def test_public_v2_comparison_is_specific(self) -> None:
        comparison = compare_public_v2_to_local_14f(
            REPO_ROOT.parents[4],
            REPO_ROOT,
        )
        if comparison["available"]:
            self.assertEqual(comparison["local_python_files"], comparison["public_python_files"])
            self.assertIn("decode/decode_pipeline.py", comparison["differing_python_files"])
            self.assertIn("decode/decode_pipeline.py", comparison["public_safe_diffs"])
        else:
            self.assertEqual(comparison["local_python_files"], 0)
            self.assertEqual(comparison["public_python_files"], 0)

    def test_main_exact_mapping_records_exact_and_adapted_files(self) -> None:
        rows = compare_main_exact_mappings(REPO_ROOT.parents[4], REPO_ROOT)
        by_public = {row["public"]: row for row in rows}
        workspace_main = default_paths(REPO_ROOT).local_main_root
        if workspace_main.exists():
            self.assertTrue(by_public["src/amcf_local_main_test02.py"]["hash_match"])
            self.assertTrue(by_public["src/amcf_vnext.py"]["hash_match"])
            self.assertFalse(by_public["src/amcf_local_main_tracking_test03a.py"]["hash_match"])
        else:
            self.assertTrue(all(not row["local_present"] for row in rows))

    def test_writes_generated_outputs_under_output(self) -> None:
        report = build_progression_integration_ledger(REPO_ROOT)
        with tempfile.TemporaryDirectory() as temp:
            outputs = write_progression_integration_outputs(report, Path(temp) / "out")
            self.assertTrue(Path(outputs["report"]).exists())
            self.assertTrue(Path(outputs["summary"]).exists())
            summary = build_markdown_summary(report)
        self.assertIn("AMCF Local Tests Progression Integration Ledger", summary)
        self.assertIn("AMCF_DIAGNOSTIC_PROFILE_BUNDLE_COMPLETION_V1", summary)


if __name__ == "__main__":
    unittest.main()

