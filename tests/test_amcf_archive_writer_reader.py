from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_archive_writer_reader import (  # noqa: E402
    build_archive,
    build_demo_report,
    extract_summary,
    fail_closed_validate,
    list_components,
    list_files,
    list_frames,
    list_semantic_objects,
    read_member_json,
    verify_checksums,
)


class AMCFArchiveWriterReaderTests(unittest.TestCase):
    def test_valid_archive_contains_manifest_sidecars_claims_and_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "minimal_valid.amcfvnext.zip"
            build_archive(archive, "minimal_valid", "minimal_valid")
            files = list_files(archive)

            self.assertIn("manifest.json", files)
            self.assertIn("claim_boundaries.json", files)
            self.assertIn("sidecars/component_metadata.json", files)
            self.assertIn("sidecars/semantic_sidecar.json", files)
            self.assertIn("payloads/frames/frame_000001.png", files)

            manifest = read_member_json(archive, "manifest.json")
            claims = read_member_json(archive, "claim_boundaries.json")
            self.assertEqual(manifest["vector_id"], "minimal_valid")
            self.assertFalse(claims["level5_claimed"])
            self.assertFalse(claims["hardware_validation_claimed"])
            self.assertFalse(claims["physical_level_5_claimed"])
            self.assertFalse(claims["manufactured_player_claimed"])

    def test_reader_lists_frames_components_and_semantic_objects(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "component_demo.amcfvnext.zip"
            build_archive(archive, "component_demo", "component_demo")

            self.assertEqual(list_frames(archive), ["payloads/frames/frame_000001.png"])
            components = list_components(archive)
            objects = list_semantic_objects(archive)
            self.assertEqual(components[0]["component_id"], "component_archive_fixture_001")
            self.assertEqual(objects[0]["persistent_object_id"], "obj_archive_fixture_001")

    def test_fail_closed_validation_accepts_only_safe_valid_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "safe.amcfvnext.zip"
            build_archive(archive, "safe", "minimal_valid")

            validation = fail_closed_validate(archive)
            self.assertTrue(validation["ok"], validation["errors"])
            self.assertEqual(validation["unsafe_acceptance_count"], 0)
            self.assertTrue(verify_checksums(archive)["ok"])

    def test_fail_closed_rejects_fake_level5_missing_payload_and_fake_user_approval(self) -> None:
        cases = {
            "fake_level5": "Level 5 claim without checklist pass",
            "missing_payload": "missing payload payloads/frames/frame_000001.png",
            "fake_user_approval": "entry 0: fake user approval",
        }
        with tempfile.TemporaryDirectory() as temp:
            for invalid_case, expected_error in cases.items():
                archive = Path(temp) / f"{invalid_case}.amcfvnext.zip"
                build_archive(archive, f"invalid_{invalid_case}", "invalid_demo", invalid_case=invalid_case)

                validation = fail_closed_validate(archive)
                self.assertFalse(validation["ok"], invalid_case)
                self.assertIn(expected_error, validation["errors"])
                self.assertEqual(validation["unsafe_acceptance_count"], 0)

    def test_extract_summary_includes_manifest_claims_components_and_checksum_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "summary.amcfvnext.zip"
            build_archive(archive, "summary", "semantic_parked_reference")

            summary = extract_summary(archive)
            self.assertTrue(summary["ok"], summary["errors"])
            self.assertEqual(summary["manifest"]["reconstruction_level"], "Level 4.99")
            self.assertTrue(summary["claim_boundaries"]["semantic_branch_still_parked"])
            self.assertTrue(summary["checksum_verification"]["ok"])
            self.assertEqual(summary["semantic_objects"][0]["track_id"], "archive_fixture_track_001")

    def test_demo_report_records_expected_invalid_rejections_and_claim_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = build_demo_report(Path(temp) / "demo")

            self.assertTrue(report["final_passed"])
            self.assertEqual(report["archive_count"], 6)
            self.assertEqual(report["expected_outcome_count"], 6)
            self.assertEqual(report["unsafe_acceptance_count"], 0)
            self.assertFalse(report["claim_boundary_flags"]["hardware_validation_claimed"])
            self.assertFalse(report["claim_boundary_flags"]["physical_level_5_claimed"])
            self.assertFalse(report["claim_boundary_flags"]["manufactured_player_claimed"])
            self.assertFalse(report["generated_output_committed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
