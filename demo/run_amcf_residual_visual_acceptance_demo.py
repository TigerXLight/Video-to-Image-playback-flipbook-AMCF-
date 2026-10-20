"""Exercise the 07E residual accounting and visual gate with bounded values."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amcf_residual_visual_acceptance import assess_candidate  # noqa: E402


def main() -> None:
    metric = {"frame_count_match": True, "fps_match": True, "resolution_match": True,
              "mae": 2.062966, "psnr": 40.11, "temporal_difference_similarity": 0.997505}
    result = assess_candidate(metric, metric, compressed_bytes=97246316,
                              fullrate_component_bytes=621084672, source_video_bytes=6097016,
                              artifact_warning=True)
    output = ROOT / "output" / "amcf_residual_visual_acceptance_demo"
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (output / "SUMMARY.md").write_text(
        "# Residual visual acceptance\n\n"
        f"Visual gate: {result['visual_gate']['status']}\n\n"
        f"Residual stream reduction: {result['compression_accounting']['reduction_vs_fullrate_component_stream_percent']}%\n\n"
        "This is an accounting and review-gate demo, not a decoded-video or hardware proof.\n",
        encoding="utf-8",
    )
    print(json.dumps({"visual_gate": result["visual_gate"]["status"],
                      "unsafe_acceptance_count": result["unsafe_acceptance_count"],
                      "output": str(output)}))


if __name__ == "__main__":
    main()
