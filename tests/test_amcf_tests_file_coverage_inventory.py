from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "demo" / "run_amcf_tests_file_coverage_inventory.py"
SPEC = importlib.util.spec_from_file_location("amcf_tests_file_coverage_inventory", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestsFileCoverageInventoryTests(unittest.TestCase):
    def test_classification_is_not_a_parity_decision(self) -> None:
        self.assertEqual(MODULE.classify_path("Test 02/run.py"), "code_or_runnable")
        self.assertEqual(MODULE.classify_path("Test 02/archive.zip"), "archive_unopened")

    def test_nested_and_hidden_files_are_inventoried_without_claiming_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "Tests"
            (root / "Test A" / "nested").mkdir(parents=True)
            (root / "Test A" / "nested" / "run.py").write_text("pass\n", encoding="utf-8")
            (root / "Test A" / ".hidden.txt").write_text("note\n", encoding="utf-8")
            (root / "Test B").mkdir()
            (root / "Test B" / "archive.zip").write_bytes(b"fixture")
            output = Path(temporary) / "output"
            summary = MODULE.inventory_tests(root, output, max_part_bytes=220)
            rows = [json.loads(line) for name in summary["inventory_parts"] for line in (output / name).read_text(encoding="utf-8").splitlines()]
            self.assertEqual(summary["files_inventoried"], 3)
            self.assertEqual(summary["top_level_folders_with_files"], 2)
            self.assertGreater(len(summary["inventory_parts"]), 1)
            self.assertEqual({row["path"] for row in rows}, {"Test A/nested/run.py", "Test A/.hidden.txt", "Test B/archive.zip"})
            self.assertTrue(all(row["review_status"] == "UNREVIEWED" for row in rows))
            self.assertFalse(summary["file_level_parity_proven"])
            self.assertEqual(summary["manual_file_reviews_confirmed_by_inventory"], 0)

    def test_report_files_do_not_inventory_themselves(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "Tests"
            root.mkdir()
            (root / "run.py").write_text("pass\n", encoding="utf-8")
            output = root / "output" / "inventory"
            first = MODULE.inventory_tests(root, output)
            second = MODULE.inventory_tests(root, output)
            self.assertEqual(first["files_inventoried"], 1)
            self.assertEqual(second["files_inventoried"], 1)
            self.assertTrue(second["self_generated_report_directory_excluded"])


if __name__ == "__main__":
    unittest.main()
