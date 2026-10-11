from __future__ import annotations

import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_physical_io import write_demo_physical_io_package  # noqa: E402


def main() -> None:
    output_dir = PACKAGE / "output" / "physical_io_architecture_demo"
    paths = write_demo_physical_io_package(output_dir)
    expected = {key: Path(value).exists() for key, value in paths.items()}
    result = {
        "ok": all(expected.values()),
        "output_dir": str(output_dir),
        "expected_outputs": expected,
        "hardware_validation_claimed": False,
        "manufactured_hardware_claimed": False,
        "real_physical_playback_proof_claimed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
