from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_hoot_level5_inference import (  # noqa: E402
    bbox_from_annotation,
    build_parser,
    find_lost_recovered_event,
)


class HootLevel5InferenceTests(unittest.TestCase):
    def test_parser_requires_input_output_and_sam2(self) -> None:
        help_text = build_parser().format_help()
        self.assertIn("--input", help_text)
        self.assertIn("--output", help_text)
        self.assertIn("--sam2-repo", help_text)
        self.assertIn("--max-visible-masks", help_text)

    def test_polygon_bbox_is_normalised(self) -> None:
        self.assertEqual(bbox_from_annotation([[10, 20], [30, 20], [30, 50], [10, 50]]), [10.0, 20.0, 30.0, 50.0])

    def test_visible_occluded_visible_event_is_detected(self) -> None:
        rows = [
            {"frame_order": 0, "visible_state": "visible_present", "full_occlusion": False, "absent": False, "image_path": "before.png"},
            {"frame_order": 1, "visible_state": "full_occlusion", "full_occlusion": True, "absent": False, "image_path": "during.png"},
            {"frame_order": 2, "visible_state": "visible_present", "full_occlusion": False, "absent": False, "image_path": "after.png"},
        ]
        event = find_lost_recovered_event(rows)
        self.assertTrue(event["validated"])
        self.assertEqual(event["occlusion_start_frame"], 1)
        self.assertEqual(event["recovered_after_frame"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
