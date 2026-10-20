from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amcf_material_coupon_analysis import analyze_synthetic_coupon  # noqa: E402


def main() -> None:
    result = analyze_synthetic_coupon(ROOT / "output" / "amcf_material_coupon_analysis")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
