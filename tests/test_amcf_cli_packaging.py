from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
PROJECT = tomllib.loads((PACKAGE / "pyproject.toml").read_text(encoding="utf-8"))


class AmcfCliPackagingTests(unittest.TestCase):
    def test_project_declares_existing_console_entrypoint(self) -> None:
        self.assertEqual(PROJECT["project"]["name"], "amcf-public-workflow")
        self.assertEqual(PROJECT["project"]["scripts"]["amcf"], "amcf_cli:main")

    def test_cli_imported_modules_are_packaged(self) -> None:
        modules = set(PROJECT["tool"]["setuptools"]["py-modules"])
        required = {
            "amcf_cli",
            "amcf_component_event_archive",
            "amcf_component_event_viewer",
            "amcf_component_ffv1_temporal",
            "amcf_component_size_ceiling",
            "amcf_deliverable_package",
            "amcf_diagnostic_profiles",
            "amcf_diagnostic_state",
            "amcf_digital_encoder",
            "amcf_digital_validator",
            "amcf_physical_carrier",
            "amcf_physical_adapters",
            "amcf_quality_metrics",
            "amcf_setup",
            "amcf_temporal_component_codec",
            "amcf_video_pipeline",
        }
        self.assertTrue(required.issubset(modules))

    def test_optional_research_extra_is_not_base_runtime_dependency(self) -> None:
        self.assertEqual(PROJECT["project"]["dependencies"], [])
        extra = set(PROJECT["project"]["optional-dependencies"]["research"])
        self.assertIn("opencv-python", extra)
        self.assertIn("Pillow", extra)

    def test_metadata_has_no_private_workspace_paths(self) -> None:
        text = (PACKAGE / "pyproject.toml").read_text(encoding="utf-8")
        self.assertNotIn("T:\\", text)
        self.assertNotIn("C:\\Users\\", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
