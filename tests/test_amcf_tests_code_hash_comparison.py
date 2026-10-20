from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "demo" / "run_amcf_tests_code_hash_comparison.py"
SPEC = importlib.util.spec_from_file_location("amcf_tests_code_hash_comparison", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestsCodeHashComparisonTests(unittest.TestCase):
    def test_exact_match_is_not_mistaken_for_semantic_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tests = root / "Tests"
            main = root / "Main"
            public = tests / "Public"
            for directory in (tests / "Run A", main, public):
                directory.mkdir(parents=True, exist_ok=True)
            (tests / "Run A" / "exact.py").write_text("shared = 1\n", encoding="utf-8")
            (tests / "Run A" / "old.py").write_text("old = 1\n", encoding="utf-8")
            (tests / "Run A" / "main.py").write_text("main = 1\n", encoding="utf-8")
            (public / "new.py").write_text("shared = 1\n", encoding="utf-8")
            (main / "main.py").write_text("main = 1\n", encoding="utf-8")
            output = public / "output" / "comparison"
            summary = MODULE.compare_code(tests, main, public, output)
            rows = [json.loads(line) for line in (output / "code_file_comparison.jsonl").read_text(encoding="utf-8").splitlines()]
            statuses = {row["path"]: row["hash_status"] for row in rows}
            self.assertEqual(statuses["Run A/exact.py"], "PUBLIC_EXACT")
            self.assertEqual(statuses["Run A/main.py"], "MAIN_EXACT_ONLY")
            self.assertEqual(statuses["Run A/old.py"], "UNMATCHED_REVIEW_REQUIRED")
            self.assertEqual(statuses["Public/new.py"], "PUBLIC_REPO_SELF")
            self.assertEqual(summary["code_files_hashed"], 4)
            self.assertFalse(summary["full_parity_proven"])
            self.assertEqual(summary["semantic_reviews_completed_by_this_scan"], 0)


if __name__ == "__main__":
    unittest.main()
