from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "demo"))

from amcf_playback_index_planner import (  # noqa: E402
    build_playback_index_report,
    build_playback_plan,
    build_startup_plan,
    entries_for_roles,
    validate_fingerprints,
)
from run_amcf_playback_index_planner_demo import build_demo_archive  # noqa: E402


class AmcfPlaybackIndexPlannerTests(unittest.TestCase):
    def test_entries_for_roles_preserves_order_and_uniqueness(self) -> None:
        index = {"quick_lookup_maps": {"by_role": {"manifest": ["a.json", "b.json"], "metadata": ["b.json", "c.json"]}}}
        self.assertEqual(entries_for_roles(index, ("manifest", "metadata")), ["a.json", "b.json", "c.json"])

    def test_startup_and_playback_plans_classify_entries(self) -> None:
        index = {
            "quick_lookup_maps": {
                "by_role": {
                    "manifest": ["manifest/native_manifest.json"],
                    "decoder_contract": ["contracts/decoder_contract.json"],
                    "decoded_output": ["media/decoded_preview.mp4"],
                    "residual_payload": ["payload/residual_000.bin"],
                }
            }
        }
        startup = build_startup_plan(index, {"frames": [{"frame_index": 0}]})
        playback = build_playback_plan(index)
        self.assertIn("manifest/native_manifest.json", startup["eager_metadata_reads"])
        self.assertTrue(playback["fallback_decoded_output_available"])
        self.assertTrue(playback["native_components_present"])

    def test_report_passes_for_synthetic_indexed_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "archive.amcf.zip"
            decode_index, seek_index = build_demo_archive(archive)
            report = build_playback_index_report(archive, decode_index, seek_index)

        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(report["claim_boundary"]["physical_level_5_claimed"])
        self.assertFalse(report["claim_boundary"]["manufactured_player_claimed"])

    def test_fingerprint_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "archive.amcf.zip"
            decode_index, _seek_index = build_demo_archive(archive)
            decode_index["validation_fingerprints"][0]["crc"] = -1
            validation = validate_fingerprints(archive, decode_index)

        self.assertFalse(validation["ok"])
        self.assertEqual(validation["fingerprint_mismatch_count"], 1)


if __name__ == "__main__":
    unittest.main()
