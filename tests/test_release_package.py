from __future__ import annotations

import json
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_virtual_hardware import (  # noqa: E402
    FuturePhysicalPlaybackDevice,
    FuturePhysicalReaderAdapter,
)


class ReleasePackageTests(unittest.TestCase):
    def test_src_modules_compile(self) -> None:
        src = PACKAGE / "src"
        files = [str(path) for path in src.glob("*.py")]
        result = subprocess.run([sys.executable, "-m", "py_compile", *files], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_virtual_hardware_demo_runs(self) -> None:
        result = subprocess.run([sys.executable, str(PACKAGE / "demo" / "run_virtual_hardware_demo.py")], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["unsafe_acceptance_count"], 0)

    def test_viewer_html_exists(self) -> None:
        self.assertTrue((PACKAGE / "viewer" / "amcf_player_ui_state_viewer.html").exists())

    def test_viewer_boundary_text_exists(self) -> None:
        html = (PACKAGE / "viewer" / "amcf_player_ui_state_viewer.html").read_text(encoding="utf-8")
        self.assertIn("Viewer stub only", html)
        self.assertIn("not physical proof", html)

    def test_claim_boundaries_exist(self) -> None:
        text = (PACKAGE / "CLAIM_BOUNDARIES.md").read_text(encoding="utf-8")
        self.assertIn("No physical proof", text)
        self.assertIn("No hardware validation", text)

    def test_unsafe_acceptance_zero(self) -> None:
        data = json.loads((PACKAGE / "examples" / "sample_player_ui_state.json").read_text(encoding="utf-8"))
        self.assertEqual(data["unsafe_acceptance_count"], 0)

    def test_future_reader_placeholder_only(self) -> None:
        status = FuturePhysicalReaderAdapter().get_status()
        self.assertFalse(status["implemented"])
        self.assertTrue(status["placeholder_only"])

    def test_future_playback_placeholder_only(self) -> None:
        status = FuturePhysicalPlaybackDevice().get_playback_status()
        self.assertFalse(status["implemented"])
        self.assertTrue(status["placeholder_only"])

    def test_package_contains_no_huge_generated_artifacts(self) -> None:
        for path in PACKAGE.rglob("*"):
            if ".git" in path.parts or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            if path.is_file():
                self.assertLess(path.stat().st_size, 5_000_000, str(path))
                self.assertNotIn("Tests", path.relative_to(PACKAGE).parts)


if __name__ == "__main__":
    unittest.main(verbosity=2)
