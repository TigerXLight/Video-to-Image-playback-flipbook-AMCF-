from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_cli import build_parser, main as cli_main  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


class AmcfCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_cli_"))
        self.source = self.tmp / "source"
        generate_source_frames(self.source, frame_count=4, width=48, height=32, fps=4)
        self.manifest = self.source / "source_frames_manifest.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_parser_exposes_user_workflow_commands(self) -> None:
        help_text = build_parser().format_help()
        self.assertIn("encode", help_text)
        self.assertIn("decode", help_text)
        self.assertIn("print-plan", help_text)
        self.assertIn("component-archive", help_text)
        self.assertIn("setup", help_text)

    def test_status_command_passes(self) -> None:
        self.assertEqual(cli_main(["status"]), 0)

    def test_encode_decode_and_print_plan_commands(self) -> None:
        package_dir = self.tmp / "package"
        decoded_dir = self.tmp / "decoded"
        print_dir = self.tmp / "print"
        self.assertEqual(cli_main(["encode", "--input-frames-manifest", str(self.manifest), "--output", str(package_dir)]), 0)
        self.assertTrue((package_dir / "package.amcf.zip").exists())
        self.assertEqual(cli_main(["decode", "--input", str(package_dir / "package.amcf.zip"), "--output", str(decoded_dir)]), 0)
        self.assertTrue((decoded_dir / "decoded_frames").exists())
        self.assertEqual(cli_main(["print-plan", "--input", str(package_dir / "package.amcf.zip"), "--output", str(print_dir)]), 0)
        self.assertTrue((print_dir / "physical_carrier_manifest.json").exists())

    def test_component_archive_command(self) -> None:
        output = self.tmp / "component"
        self.assertEqual(cli_main(["component-archive", "--input-frames-manifest", str(self.manifest), "--output", str(output)]), 0)
        self.assertTrue((output / "component_event_archive.amcf.zip").exists())
        self.assertTrue((output / "viewer" / "index.html").exists())
        self.assertTrue((output / "deliverable_package" / "amcf_public_deliverable_package.zip").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
