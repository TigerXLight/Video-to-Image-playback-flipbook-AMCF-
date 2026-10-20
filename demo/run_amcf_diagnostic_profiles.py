"""Run one of the maintained AMCF diagnostic profiles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


MAIN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MAIN_ROOT / "src"))

from amcf_diagnostic_profiles import (  # noqa: E402
    render_03m_motion_truth_family,
    render_roi_comparison_video,
    render_motion_heat_comparison_video,
    render_reviewed_proxy_video,
    render_zone_motion_video,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "profile",
        choices=("03m-motion-truth-family", "03m-zone-motion", "08e-motion-heat", "10ab-roi-audit", "12d-calibrated-proxy", "12e-reviewed-proxy"),
    )
    parser.add_argument("--input-video", type=Path, help="source video for the 03M or 12E profile")
    parser.add_argument("--truth-video", type=Path, help="truth video for the 08E profile")
    parser.add_argument("--decoded-video", type=Path, help="decoded video for the 08E profile")
    parser.add_argument("--selected-video", type=Path, help="selected AMCF video for the 10A/10B profile")
    parser.add_argument("--fullrate-video", type=Path, help="optional full-rate control for the 10A/10B profile")
    parser.add_argument("--roi-profile", default="fourth-people", help="10A/10B ROI profile: third-water or fourth-people")
    parser.add_argument("--manifest", type=Path, help="reviewed 12E proxy manifest")
    parser.add_argument("--diagnostic-state", type=Path, help="normalized Test 02 state for the 03M coverage view")
    parser.add_argument("--output-video", type=Path, required=True)
    parser.add_argument("--only-track-id")
    args = parser.parse_args()

    if args.profile == "03m-motion-truth-family":
        if args.input_video is None:
            parser.error("03m-motion-truth-family requires --input-video")
        report = render_03m_motion_truth_family(
            args.input_video,
            args.output_video,
            diagnostic_state_manifest=args.diagnostic_state,
        )
    elif args.profile == "03m-zone-motion":
        if args.input_video is None:
            parser.error("03m-zone-motion requires --input-video")
        report = render_zone_motion_video(args.input_video, args.output_video)
    elif args.profile == "08e-motion-heat":
        if args.truth_video is None or args.decoded_video is None:
            parser.error("08e-motion-heat requires --truth-video and --decoded-video")
        report = render_motion_heat_comparison_video(args.truth_video, args.decoded_video, args.output_video)
    elif args.profile == "10ab-roi-audit":
        if args.truth_video is None or args.selected_video is None:
            parser.error("10ab-roi-audit requires --truth-video and --selected-video")
        report = render_roi_comparison_video(
            args.truth_video,
            args.selected_video,
            args.output_video,
            roi_profile=args.roi_profile,
            fullrate_video=args.fullrate_video,
        )
    else:
        if args.input_video is None or args.manifest is None:
            parser.error(f"{args.profile} requires --input-video and --manifest")
        report = render_reviewed_proxy_video(
            args.input_video,
            args.manifest,
            args.output_video,
            only_track_id=args.only_track_id,
            profile_name=(
                "12D_calibrated_semantic_proxy"
                if args.profile == "12d-calibrated-proxy"
                else "12E_reviewed_timelapse_proxy"
            ),
        )

    report_path = (
        args.output_video / "03m_motion_truth_family.json"
        if args.profile == "03m-motion-truth-family"
        else args.output_video.with_suffix(args.output_video.suffix + ".json")
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("status") == "PASS" and report.get("unsafe_acceptance_count") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
