"""Run the Test 03M motion-zone diagnostic on deterministic synthetic frames."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amcf_motion_truth_diagnostics import Zone, analyze_pair  # noqa: E402


def main() -> None:
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise SystemExit("Optional OpenCV and NumPy are required for this demo") from exc
    rng = np.random.default_rng(3)
    previous = rng.integers(0, 80, (64, 96, 3), dtype=np.uint8)
    current = previous.copy()
    cv2.rectangle(current, (42, 20), (55, 36), (245, 245, 245), -1)
    zones = [Zone("active_zone", "high_local_motion", (36, 14, 26, 28)),
             Zone("static_zone", "camera_motion_only_or_static", (2, 2, 22, 22))]
    report, overlay = analyze_pair(previous, current, zones)
    output = ROOT / "output" / "amcf_motion_truth_diagnostics_demo"
    output.mkdir(parents=True, exist_ok=True)
    (output / "motion_truth_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if not cv2.imwrite(str(output / "zone_motion_overlay.png"), overlay):
        raise RuntimeError("could not write diagnostic overlay")
    print(json.dumps({"motion_mask_pixels": report["motion_mask_pixels"],
                      "human_review_required": report["human_review_required"],
                      "unsafe_acceptance_count": report["unsafe_acceptance_count"]}))


if __name__ == "__main__":
    main()
