"""Run the motion-referenced temporal component codec on the canonical source frames."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from amcf_temporal_component_codec import assess_temporal_component_archive, build_temporal_component_archive  # noqa: E402


DEFAULT_MANIFEST = WORKSPACE / "Tests/Test AMCF_MAIN_PUBLIC_MEDIA_ACCEPTANCE/20261015_131327/local_main/amcf_encode/extracted_source/source_frames_manifest.json"
DEFAULT_OUTPUT = ROOT / "output" / "amcf_temporal_component_codec"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--keyframe-interval", type=int, default=24)
    parser.add_argument("--tile-size", type=int, default=64)
    parser.add_argument("--keyframe-quality", type=int, default=90)
    parser.add_argument("--residual-codec", choices=("packed_motion_xor_zlib", "quantized_residual_webp", "quantized_residual_webp_lossy"), default="packed_motion_xor_zlib")
    parser.add_argument("--residual-step", type=int, default=4)
    parser.add_argument("--residual-quality", type=int, default=55)
    parser.add_argument("--no-local-motion", action="store_true", help="disable per-tile motion search for comparison")
    parser.add_argument("--motion-search-radius", type=int, default=1)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / "temporal_component_archive.amcf.zip"
    build = build_temporal_component_archive(
        args.source_manifest,
        archive,
        keyframe_interval=args.keyframe_interval,
        tile_size=args.tile_size,
        keyframe_quality=args.keyframe_quality,
        residual_codec=args.residual_codec,
        residual_step=args.residual_step,
        residual_quality=args.residual_quality,
        local_motion=not args.no_local_motion,
        motion_search_radius=args.motion_search_radius,
    )
    assessment = assess_temporal_component_archive(args.source_manifest, archive, args.output / "decoded")
    report = {"build": build, "assessment": assessment, "unsafe_acceptance_count": 0}
    (args.output / "temporal_component_codec_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    summary = [
        "# AMCF Temporal Component Codec",
        "",
        f"- archive bytes: `{build['archive_bytes']}`",
        f"- source ceiling bytes: `{build['source_size_ceiling_bytes']}`",
        f"- under source ceiling: `{str(build['under_source_size_ceiling']).lower()}`",
        f"- keyframes: `{build['keyframe_count']}`",
        f"- delta frames: `{build['delta_frame_count']}`",
        f"- residual raw bytes: `{build['residual_raw_bytes']}`",
        f"- residual compressed bytes: `{build['residual_compressed_bytes']}`",
        f"- mean MAE: `{assessment['quality']['mean_absolute_error']}`",
        f"- mean SSIM: `{assessment['quality']['mean_ssim']}`",
        f"- visual gate: `{str(assessment['visual_passed']).lower()}`",
        "- unsafe_acceptance_count: `0`",
        "- hardware validation claimed: `false`",
        "- physical Level 5 claimed: `false`",
        "- manufactured player claimed: `false`",
    ]
    (args.output / "TEMPORAL_COMPONENT_CODEC_SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if bool(build["under_source_size_ceiling"] and assessment["visual_passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
