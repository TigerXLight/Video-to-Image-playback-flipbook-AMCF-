from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys
import zipfile


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_source_seeded_event_materializer import validate_source_seeded_archive  # noqa: E402


class SourceSeededMaterializerContractTests(unittest.TestCase):
    def test_rejects_non_materializer_archive_before_decoding(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            archive_path = root / "not_materializer.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("manifest/manifest.json", json.dumps({"source_seed_embedded": False}))
                archive.writestr("metadata/materialization_contract.json", json.dumps({}))
            with self.assertRaises((KeyError, ValueError, zipfile.BadZipFile)):
                validate_source_seeded_archive(archive_path, root / "out")


if __name__ == "__main__":
    unittest.main(verbosity=2)

