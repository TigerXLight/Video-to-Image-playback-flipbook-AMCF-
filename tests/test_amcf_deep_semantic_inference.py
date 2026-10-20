from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_deep_semantic_inference import build_parser, parse_bbox  # noqa: E402


class DeepSemanticInferenceTests(unittest.TestCase):
    def test_parser_requires_explicit_input_and_output(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        self.assertIn("--input", help_text)
        self.assertIn("--output", help_text)
        self.assertIn("--sam2-repo", help_text)
        self.assertIn("--cotracker-checkpoint", help_text)

    def test_default_bbox_is_central_and_deterministic(self) -> None:
        self.assertEqual(parse_bbox(None, 100, 80), [30.0, 20.0, 70.0, 60.0])

    def test_bbox_is_clamped_to_frame(self) -> None:
        self.assertEqual(parse_bbox("-10,-5,120,90", 100, 80), [0.0, 0.0, 100.0, 80.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
