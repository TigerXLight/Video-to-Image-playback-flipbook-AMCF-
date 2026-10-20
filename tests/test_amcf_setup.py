from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_setup import load_manifest, run_setup, write_runtime_config  # noqa: E402


class AmcfSetupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_setup_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_manifest_has_pinned_external_resources_and_claim_boundaries(self) -> None:
        manifest = load_manifest(PACKAGE / "amcf_dependency_manifest.json")
        self.assertEqual(manifest["schema"], "amcf_dependency_manifest_v1")
        resources = {row["id"]: row for row in manifest["resources"]}
        self.assertEqual(resources["samurai_sam2"]["ref"], "76ba195984892b0d1e3db5d9c9f90bb62175680a")
        self.assertTrue(resources["cotracker"]["requires_noncommercial_acceptance"])
        self.assertTrue(manifest["claim_boundary"]["core_archive"])

    def test_runtime_config_is_relative_and_points_at_external_resources(self) -> None:
        path = self.tmp / "amcf_runtime_config.json"
        values = write_runtime_config(path, self.tmp, self.tmp / ".amcf-runtime", Path(sys.executable))
        self.assertEqual(values["workspace_root"], ".")
        self.assertTrue(values["optional_deep_tools"]["sam2_repo"].startswith(".amcf-runtime/"))
        parsed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(parsed["setup"]["source_video_required_for_core_archive_playback"], False)

    def test_check_mode_is_safe_when_external_resources_are_absent(self) -> None:
        report = run_setup(
            manifest_path=PACKAGE / "amcf_dependency_manifest.json",
            project_root=self.tmp,
            dependency_root=self.tmp / ".amcf-runtime",
            config_output=self.tmp / "runtime.json",
            report_output=self.tmp / "report.json",
        )
        self.assertTrue(report["ok"])
        self.assertFalse(report["status"]["deep_inference_ready"])
        self.assertTrue((self.tmp / "runtime.json").is_file())
        self.assertTrue((self.tmp / "report.json").is_file())
        self.assertFalse(report["actions"])

    def test_noncommercial_gate_blocks_external_prepare_without_mutating_resources(self) -> None:
        report = run_setup(
            manifest_path=PACKAGE / "amcf_dependency_manifest.json",
            project_root=self.tmp,
            dependency_root=self.tmp / ".amcf-runtime",
            clone_repositories=True,
            accept_upstream_licenses=True,
        )
        self.assertFalse(report["ok"])
        self.assertIn("--accept-noncommercial", " ".join(report["errors"]))
        self.assertFalse((self.tmp / ".amcf-runtime" / "repositories").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
