from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_player_pc_runtime import write_player_pc_runtime_demo  # noqa: E402


def main() -> int:
    output_dir = REPO_ROOT / "output" / "amcf_player_pc_runtime_fixture"
    result = write_player_pc_runtime_demo(REPO_ROOT, output_dir)
    report = result["report"]
    print(
        json.dumps(
            {
                "ok": report["final_passed"],
                "output_folder": str(output_dir),
                "package_compatible": report["package_compatible"],
                "command_count": len(report["command_transcript"]),
                "unsafe_acceptance_count": report["unsafe_acceptance_count"],
                "usb_used": report["usb_used"],
                "serial_used": report["serial_used"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
