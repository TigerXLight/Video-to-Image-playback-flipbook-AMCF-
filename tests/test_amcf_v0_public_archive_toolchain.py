from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amcf_v0 import builder, loader, toolchain


class AMCFV0PublicArchiveToolchainTests(unittest.TestCase):
    def _write_archive(self, path: Path) -> None:
        manifest = {
            "archive_schema_name": "AMCF v0 prototype archive",
            "archive_schema_version": "public-port-test",
            "not_final_codec": True,
            "primary_viewer": "viewer/OPEN_FIRST_AMCF_04B_VIEWER.html",
            "primary_video": "media/original_vs_best_visual_baseline.mp4",
            "candidate_only_video": "media/candidate_only_best_visual_baseline.mp4",
        }
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("viewer/OPEN_FIRST_AMCF_04B_VIEWER.html", "<!doctype html><title>AMCF v0</title>")
            z.writestr("viewer/OPEN_FIRST_AMCF_04B_README.md", "# AMCF v0 viewer\n")
            z.writestr("manifest/AMCF_04B_ARCHIVE_MANIFEST.json", json.dumps(manifest))
            z.writestr("media/original_vs_best_visual_baseline.mp4", b"synthetic-video-placeholder")
            z.writestr("media/candidate_only_best_visual_baseline.mp4", b"synthetic-video-placeholder")
            z.writestr("docs/visual_gate_rules.md", "# Visual gate rules\n")

    def test_loader_validates_and_extracts_public_v0_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "sample.amcfv0.zip"
            extract_dir = root / "extract"
            self._write_archive(archive)

            report = loader.cmd_validate(
                type("Args", (), {"archive": str(archive), "out": str(extract_dir), "report": ""})()
            )

            self.assertTrue(report["passed"])
            self.assertFalse(report["unsafe_entries"])
            self.assertTrue((extract_dir / "manifest" / "AMCF_04B_ARCHIVE_MANIFEST.json").exists())

    def test_builder_rejects_unsafe_public_archive_names(self) -> None:
        self.assertTrue(builder.is_unsafe_rel_name("../escape.txt"))
        self.assertTrue(builder.is_unsafe_rel_name("nested/archive.zip"))
        self.assertTrue(builder.is_unsafe_rel_name("models/checkpoint.pt"))
        self.assertFalse(builder.is_unsafe_rel_name("viewer/OPEN_FIRST_AMCF_04B_VIEWER.html"))

    def test_builder_template_and_checksums_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "template"
            template = builder.init_template(root)
            checksums = builder.checksum_source(root)

            self.assertTrue(template["passed"])
            self.assertEqual(checksums["file_count"], 4)
            self.assertTrue(all("sha256" in row for row in checksums["files"]))

    def test_toolchain_component_manifest_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "component_manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "component_schema_name": "AMCF v0 component stream",
                        "component_schema_version": "public-port-test",
                        "source_baseline": "synthetic",
                        "source_fps": 24,
                        "source_frame_count": 2,
                        "components": [{"component_id": "component_0001"}],
                        "update_schedules": [],
                        "mask_policy": {},
                        "stream_policy": {},
                        "compositor_policy": {},
                        "visual_gate_policy": {},
                        "limitations": [],
                    }
                ),
                encoding="utf-8",
            )

            report = toolchain.component_manifest_ok(manifest)

            self.assertTrue(report["passed"])
            self.assertEqual(report["component_ids"], ["component_0001"])


if __name__ == "__main__":
    unittest.main()

