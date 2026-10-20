import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.amcf_semantic_sidecar_overlay import (
    build_demo_sidecar,
    build_semantic_overlay_report,
    list_semantic_objects,
    semantic_frames,
    validate_semantic_sidecar,
    write_semantic_overlay_report,
)


class SemanticSidecarOverlayTests(unittest.TestCase):
    def test_demo_sidecar_lists_approved_frames_and_object(self):
        sidecar = build_demo_sidecar()
        frames = semantic_frames(sidecar)
        self.assertEqual(len(frames), 3)
        self.assertTrue(all(frame.reviewer_approved for frame in frames))
        objects = list_semantic_objects(sidecar)
        self.assertEqual(objects[0]["persistent_object_id"], "obj_people_cal12c_0117")

    def test_validate_rejects_fake_solved_claim_and_unapproved_frame(self):
        sidecar = build_demo_sidecar()
        sidecar["claim_flags"]["semantic_object_amcf_solved"] = True
        sidecar["objects"][0]["frames"][0]["reviewer_approved"] = False
        validation = validate_semantic_sidecar(sidecar)
        self.assertFalse(validation["valid"])
        self.assertIn("semantic_object_amcf_solved must remain false for this micro-sidecar diagnostic", validation["errors"])
        self.assertIn("unapproved frame: 0", validation["errors"])
        self.assertEqual(validation["unsafe_acceptance_count"], 0)

    def test_report_preserves_claim_boundaries(self):
        report = build_semantic_overlay_report()
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(report["claim_boundary"]["physical_level5_claimed"])
        self.assertFalse(report["claim_boundary"]["manufactured_player_claimed"])
        self.assertFalse(report["claim_boundary"]["semantic_object_amcf_solved_by_micro_sidecar"])

    def test_write_report_outputs_json_and_summary(self):
        with TemporaryDirectory() as tmp:
            report = write_semantic_overlay_report(Path(tmp))
            self.assertTrue(report["final_passed"])
            self.assertTrue((Path(tmp) / "semantic_sidecar_overlay_report.json").exists())
            self.assertTrue((Path(tmp) / "SEMANTIC_SIDECAR_OVERLAY_SUMMARY.md").exists())


if __name__ == "__main__":
    unittest.main()
