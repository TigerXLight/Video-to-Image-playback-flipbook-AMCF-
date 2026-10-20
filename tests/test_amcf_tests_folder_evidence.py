from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "demo" / "run_amcf_tests_folder_evidence.py"
SPEC = importlib.util.spec_from_file_location("amcf_tests_folder_evidence", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FolderEvidenceTests(unittest.TestCase):
    def test_every_file_is_hashed_and_parity_remains_open(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            (root / "manifest.json").write_text('{"frames": 2}', encoding="utf-8")
            (root / "measurements.csv").write_text("frame,value\n0,1\n1,2\n", encoding="utf-8")
            (root / "notes.md").write_text("# Not accepted\n", encoding="utf-8")
            with zipfile.ZipFile(root / "archive.zip", "w") as archive:
                archive.writestr("payload.txt", "data")
            output = Path(temporary) / "output"
            summary = MODULE.scan_folder(root, output)
            rows = [json.loads(line) for line in (output / "file_evidence.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(summary["files_scanned"], 4)
            self.assertTrue(summary["file_evidence_complete"])
            self.assertFalse(summary["semantic_review_complete_by_scanner"])
            self.assertFalse(summary["full_local_to_public_parity_proven"])
            self.assertTrue(all(row["sha256"] and row["semantic_disposition"] == "OPEN" for row in rows))
            checks = {row["path"]: row["verification"]["check"] for row in rows}
            self.assertEqual(checks["archive.zip"], "zip_crc_verified")
            self.assertEqual(checks["manifest.json"], "json_parsed")
            self.assertEqual(checks["measurements.csv"], "csv_parsed")

    def test_rejects_self_inventory_and_bad_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            with self.assertRaisesRegex(ValueError, "outside"):
                MODULE.scan_folder(root, root / "output")
            (root / "bad.json").write_text("{broken", encoding="utf-8")
            summary = MODULE.scan_folder(root, Path(temporary) / "output")
            self.assertFalse(summary["file_evidence_complete"])
            self.assertEqual(summary["failures"], ["bad.json"])

    def test_corrupt_archive_does_not_pass_file_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            (root / "broken.zip").write_bytes(b"not an archive")
            summary = MODULE.scan_folder(root, Path(temporary) / "output")
            self.assertFalse(summary["file_evidence_complete"])
            self.assertEqual(summary["failures"], ["broken.zip"])


if __name__ == "__main__":
    unittest.main()
