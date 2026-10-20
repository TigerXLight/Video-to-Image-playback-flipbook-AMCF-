from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_component_size_ceiling import optimize_component_archive  # noqa: E402
from amcf_quality_metrics import ppm_bytes  # noqa: E402


class ComponentSizeCeilingTests(unittest.TestCase):
    def test_optimizer_reports_candidate_and_claim_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            frames = root / "frames"
            frames.mkdir()
            entries = []
            for index in range(3):
                pixels = bytes([index * 20, 100, 180]) * (16 * 8)
                path = frames / f"frame_{index:03d}.ppm"
                path.write_bytes(ppm_bytes(16, 8, pixels))
                entries.append({"frame_index": index, "file": f"frames/{path.name}", "width": 16, "height": 8, "format": "ppm_p6"})
            manifest = root / "source_frames_manifest.json"
            manifest.write_text(json.dumps({
                "source_type": "test_frames",
                "frame_count": 3,
                "width": 16,
                "height": 8,
                "fps": 3,
                "source_video": {"bytes": 100000},
                "frame_entries": entries,
            }), encoding="utf-8")
            report = optimize_component_archive(manifest, root / "output", quality_candidates=(35,))
            self.assertEqual(report["unsafe_acceptance_count"], 0)
            self.assertFalse(report["claim_boundary_flags"]["hardware_validation_claimed"])
            self.assertEqual(len(report["candidates"]), 1)
            self.assertIn("visual", report["candidates"][0])


if __name__ == "__main__":
    unittest.main()
