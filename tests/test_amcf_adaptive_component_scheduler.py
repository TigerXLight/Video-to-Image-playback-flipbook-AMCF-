from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_adaptive_component_scheduler import ComponentUpdatePolicy, build_update_schedule, decide_component_update  # noqa: E402


class AmcfAdaptiveComponentSchedulerTests(unittest.TestCase):
    def test_first_frame_can_be_forced_to_update(self) -> None:
        decision = decide_component_update(
            frame_index=0,
            last_update_frame=None,
            changed_pixels=0,
            total_pixels=100,
            force_first=True,
        )
        self.assertTrue(decision.should_update)
        self.assertEqual(decision.reason, "initial_component_state")

    def test_min_interval_blocks_update(self) -> None:
        decision = decide_component_update(
            frame_index=2,
            last_update_frame=1,
            changed_pixels=50,
            total_pixels=100,
            policy=ComponentUpdatePolicy(min_interval_frames=3),
        )
        self.assertFalse(decision.should_update)
        self.assertEqual(decision.reason, "min_interval_not_met")

    def test_changed_region_triggers_update(self) -> None:
        decision = decide_component_update(
            frame_index=4,
            last_update_frame=1,
            changed_pixels=20,
            total_pixels=100,
            policy=ComponentUpdatePolicy(min_interval_frames=1, changed_pixel_threshold=5, changed_ratio_threshold=0.1),
        )
        self.assertTrue(decision.should_update)
        self.assertEqual(decision.reason, "changed_region")

    def test_build_update_schedule_records_decisions(self) -> None:
        schedule = build_update_schedule(
            [0, 2, 20],
            total_pixels=100,
            policy=ComponentUpdatePolicy(min_interval_frames=1, changed_pixel_threshold=5),
        )
        self.assertTrue(schedule[0]["should_update"])
        self.assertFalse(schedule[1]["should_update"])
        self.assertTrue(schedule[2]["should_update"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
