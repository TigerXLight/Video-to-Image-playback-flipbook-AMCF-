from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amcf_player_ui_state import (  # noqa: E402
    REQUIRED_PLAYER_UI_STATE_KEYS,
    build_player_ui_state_outputs,
    normalize_player_ui_state,
    render_player_ui_state_report,
)


class PlayerUiStateTests(unittest.TestCase):
    def sample_state(self) -> dict:
        return json.loads((ROOT / "examples" / "sample_player_ui_state.json").read_text(encoding="utf-8"))

    def test_sample_contains_required_keys(self) -> None:
        state = self.sample_state()
        for key in REQUIRED_PLAYER_UI_STATE_KEYS:
            self.assertIn(key, state)

    def test_normalize_player_ui_state_adds_counts_and_boundaries(self) -> None:
        normalized = normalize_player_ui_state(self.sample_state())
        self.assertEqual(normalized["viewer_schema"], "amcf-player-ui-state-viewer-v1")
        self.assertEqual(normalized["counts"]["accepted"], 6)
        self.assertEqual(normalized["counts"]["rescanned"], 3)
        self.assertEqual(normalized["counts"]["rejected"], 2)
        self.assertEqual(normalized["counts"]["unsafe_acceptance"], 0)
        self.assertFalse(normalized["claim_boundary"]["final_ui_claimed"])
        self.assertFalse(normalized["claim_boundary"]["hardware_validation_claimed"])
        self.assertFalse(normalized["claim_boundary"]["physical_level_5_claimed"])
        self.assertFalse(normalized["claim_boundary"]["manufactured_player_claimed"])

    def test_normalize_rejects_missing_required_key(self) -> None:
        state = self.sample_state()
        state.pop("validation_log_rows")
        with self.assertRaises(ValueError):
            normalize_player_ui_state(state)

    def test_normalize_rejects_unsafe_acceptance(self) -> None:
        state = self.sample_state()
        state["unsafe_acceptance_count"] = 1
        with self.assertRaises(ValueError):
            normalize_player_ui_state(state)

    def test_render_report_contains_diagnostics(self) -> None:
        report = render_player_ui_state_report(normalize_player_ui_state(self.sample_state()))
        self.assertIn("AMCF Player UI State Report", report)
        self.assertIn("unsafe acceptance policy: zero tolerated", report)
        self.assertIn("Viewer stub only", report)
        self.assertIn("Component Payloads", report)

    def test_build_outputs_writes_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = build_player_ui_state_outputs(ROOT / "examples" / "sample_player_ui_state.json", tmp)
            self.assertTrue(result["ok"])
            self.assertEqual(result["unsafe_acceptance_count"], 0)
            self.assertTrue(Path(result["normalized_state_path"]).exists())
            self.assertTrue(Path(result["report_path"]).exists())

    def test_demo_runs(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "demo" / "run_amcf_player_ui_state_demo.py")],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["ok"])
        self.assertEqual(data["unsafe_acceptance_count"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
