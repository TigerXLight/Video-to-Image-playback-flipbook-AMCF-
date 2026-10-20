from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_quality_metrics import compare_ppm_frame_folders, ppm_bytes  # noqa: E402
from amcf_temporal_component_codec import (  # noqa: E402
    SCHEMA,
    assess_temporal_component_archive,
    build_temporal_component_archive,
    decode_temporal_component_archive,
)


class TemporalComponentCodecTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_temporal_codec_"))
        self.frames = self.tmp / "frames"
        self.frames.mkdir()
        width, height = 32, 16
        entries = []
        for index in range(6):
            pixels = bytearray(width * height * 3)
            for y in range(height):
                for x in range(width):
                    position = (y * width + x) * 3
                    pixels[position:position + 3] = bytes(((x + index * 2) % 256, (y * 8) % 256, 120))
            path = self.frames / f"frame_{index:03d}.ppm"
            path.write_bytes(ppm_bytes(width, height, bytes(pixels)))
            entries.append({
                "frame_index": index,
                "file": f"frames/{path.name}",
                "width": width,
                "height": height,
                "format": "ppm_p6",
            })
        self.manifest = self.tmp / "source_frames_manifest.json"
        self.manifest.write_text(json.dumps({
            "source_type": "synthetic_temporal_test",
            "frame_count": len(entries),
            "width": width,
            "height": height,
            "fps": 6,
            "source_video": {"bytes": 100000},
            "frame_entries": entries,
        }), encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_decode_and_manifest_are_fail_closed(self) -> None:
        archive = self.tmp / "temporal.amcf.zip"
        result = build_temporal_component_archive(
            self.manifest,
            archive,
            keyframe_interval=3,
            tile_size=16,
            keyframe_quality=100,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["amcf_schema"], SCHEMA)
        self.assertEqual(result["frame_count"], 6)
        self.assertGreater(result["delta_frame_count"], 0)
        self.assertEqual(result["manifest"]["preservation_mode"], "lossless_exact_residual")
        self.assertEqual(result["unsafe_acceptance_count"], 0)
        self.assertFalse(result["claim_boundary"]["hardware_validation_claimed"])

        decoded = decode_temporal_component_archive(archive, self.tmp / "decoded")
        self.assertTrue(decoded["ok"])
        self.assertEqual(decoded["frame_count"], 6)
        quality = compare_ppm_frame_folders(self.frames, Path(decoded["decoded_frames_dir"]))
        self.assertEqual(quality["expected_frame_count"], 6)
        self.assertEqual(quality["actual_frame_count"], 6)
        self.assertEqual(quality["mean_absolute_error"], 0.0)
        self.assertEqual(quality["mean_ssim"], 1.0)

    def test_assessment_contains_visual_gate_and_claim_boundary(self) -> None:
        archive = self.tmp / "temporal_assessed.amcf.zip"
        build_temporal_component_archive(
            self.manifest,
            archive,
            keyframe_interval=6,
            keyframe_quality=90,
            residual_codec="quantized_residual_webp",
            residual_step=4,
        )
        report = assess_temporal_component_archive(self.manifest, archive, self.tmp / "assessed")
        self.assertIn("visual_thresholds", report)
        self.assertIn("visual_passed", report)
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary"]["physical_level_5_claimed"])


if __name__ == "__main__":
    unittest.main()
