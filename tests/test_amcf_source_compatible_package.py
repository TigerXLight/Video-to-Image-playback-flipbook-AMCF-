from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_component_event_archive import build_component_event_archive  # noqa: E402
from amcf_source_compatible_package import (  # noqa: E402
    SOURCE_COMPATIBLE_SCHEMA,
    build_source_compatible_package,
)
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class AmcfSourceCompatiblePackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_source_compatible_"))
        self.source = self.tmp / "source"
        generate_source_frames(self.source, frame_count=5, width=48, height=32, fps=5)
        self.native_archive = self.tmp / "native.amcf.zip"
        build_component_event_archive(
            self.source / "source_frames_manifest.json",
            self.native_archive,
            prefer_webp=False,
        )
        self.source_video = self.tmp / "source.mp4"
        self.source_video.write_bytes(b"deterministic-source-video-payload")
        self.package = self.tmp / "compact.amcf.zip"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_preserves_event_metadata_and_integrity_tables(self) -> None:
        result = build_source_compatible_package(
            self.source_video,
            self.native_archive,
            self.package,
        )
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["semantic_event_metadata_present"])
        self.assertTrue(result["integrity_tables_present"])
        self.assertFalse(result["native_component_payloads_present"])
        self.assertEqual(result["unsafe_acceptance_count"], 0)
        with zipfile.ZipFile(self.package) as archive:
            manifest = json.loads(archive.read("metadata/amcf_manifest.json"))
            package_manifest = json.loads(archive.read("metadata/package_manifest.json"))
            self.assertEqual(manifest["source_compatible_schema"], SOURCE_COMPATIBLE_SCHEMA)
            self.assertEqual(
                manifest["archive_payload_kind"],
                "source_video_reference_with_component_event_metadata",
            )
            self.assertFalse(manifest["native_component_payloads_present"])
            self.assertTrue(manifest["canonical_component_payloads_externalized"])
            self.assertTrue(manifest["hash_tables"])
            self.assertTrue(package_manifest["semantic_event_metadata_present"])
            self.assertEqual(package_manifest["unsafe_acceptance_count"], 0)
            self.assertEqual(len(archive.read("metadata/event_payload_sha256.bin")), 4 * 32)
            self.assertEqual(len(archive.read("metadata/source_frame_sha256.bin")), 5 * 32)
            self.assertEqual(len(archive.read("metadata/base_sha256.bin")), 32)


if __name__ == "__main__":
    unittest.main()
