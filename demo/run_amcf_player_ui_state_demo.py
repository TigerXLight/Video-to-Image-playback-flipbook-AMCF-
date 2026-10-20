from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amcf_player_ui_state import build_player_ui_state_outputs  # noqa: E402


def main() -> None:
    output_root = ROOT / "output" / "amcf_player_ui_state"
    result = build_player_ui_state_outputs(
        ROOT / "examples" / "sample_player_ui_state.json",
        output_root,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
