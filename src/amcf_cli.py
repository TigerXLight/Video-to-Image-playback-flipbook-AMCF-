from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive
from amcf_component_event_viewer import build_component_event_viewer
from amcf_physical_carrier import generate_physical_carrier_from_amcf_archive
from amcf_quality_metrics import compare_ppm_frame_folders
from amcf_video_pipeline import decode_amcf_to_frames, decode_amcf_to_video, encode_video_to_amcf
from amcf_digital_encoder import encode_source_frames
from amcf_digital_validator import validate_amcf_archive


def _print_result(result: dict[str, Any]) -> int:
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok", False) else 1


def cmd_status(_: argparse.Namespace) -> int:
    return _print_result(
        {
            "ok": True,
            "app": "AMCF public workflow CLI",
            "commands": ["status", "encode", "component-archive", "decode", "print-plan"],
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "unsafe_acceptance_count": 0,
        }
    )


def cmd_encode(args: argparse.Namespace) -> int:
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    if args.input_video:
        result = encode_video_to_amcf(args.input_video, output, fps=args.fps, max_frames=args.max_frames, include_audio=not args.no_audio)
    else:
        archive = output / "package.amcf.zip"
        encode = encode_source_frames(args.input_frames_manifest, archive)
        validation = validate_amcf_archive(archive)
        result = {
            "ok": bool(validation["ok"]),
            "archive_path": str(archive),
            "encode_summary": encode,
            "validation": validation,
            "unsafe_acceptance_count": validation.get("unsafe_acceptance_count", 0),
        }
    return _print_result(result)


def cmd_component_archive(args: argparse.Namespace) -> int:
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    archive_path = output / "component_event_archive.amcf.zip"
    archive = build_component_event_archive(
        args.input_frames_manifest,
        archive_path,
        prefer_webp=not args.no_webp,
        segmentation_mode=args.segmentation_mode,
    )
    decoded = decode_component_event_archive(archive_path, output / "decoded")
    quality = compare_ppm_frame_folders(Path(args.input_frames_manifest).parent / "frames", Path(decoded["decoded_frames_dir"]))
    viewer = build_component_event_viewer(
        archive_report=archive,
        decoded_report=decoded,
        quality_report=quality,
        output_dir=output / "viewer",
    )
    result = {
        "ok": archive["ok"] and decoded["ok"] and quality["ok"] and viewer["ok"],
        "archive": archive,
        "decode": decoded,
        "quality": quality,
        "viewer": viewer,
        "unsafe_acceptance_count": archive.get("unsafe_acceptance_count", 0),
    }
    return _print_result(result)


def cmd_decode(args: argparse.Namespace) -> int:
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    if args.component_event:
        result = decode_component_event_archive(args.input, output)
    elif args.video:
        result = decode_amcf_to_video(args.input, output)
    else:
        result = decode_amcf_to_frames(args.input, output)
    return _print_result(result)


def cmd_print_plan(args: argparse.Namespace) -> int:
    result = generate_physical_carrier_from_amcf_archive(args.input, args.output)
    result["unsafe_acceptance_count"] = 0
    return _print_result(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AMCF public workflow CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="Show public CLI status and claim boundaries.")
    status.set_defaults(func=cmd_status)

    encode = sub.add_parser("encode", help="Encode source frames or source video to AMCF.")
    source = encode.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-video")
    source.add_argument("--input-frames-manifest")
    encode.add_argument("--output", required=True)
    encode.add_argument("--fps", type=int)
    encode.add_argument("--max-frames", type=int)
    encode.add_argument("--no-audio", action="store_true")
    encode.set_defaults(func=cmd_encode)

    component = sub.add_parser("component-archive", help="Build and inspect a component-event AMCF archive from source frames.")
    component.add_argument("--input-frames-manifest", required=True)
    component.add_argument("--output", required=True)
    component.add_argument("--segmentation-mode", choices=["changed_region", "opencv_changed_region"], default="changed_region")
    component.add_argument("--no-webp", action="store_true")
    component.set_defaults(func=cmd_component_archive)

    decode = sub.add_parser("decode", help="Decode an AMCF archive.")
    decode.add_argument("--input", required=True)
    decode.add_argument("--output", required=True)
    decode.add_argument("--component-event", action="store_true")
    decode.add_argument("--video", action="store_true")
    decode.set_defaults(func=cmd_decode)

    print_plan = sub.add_parser("print-plan", help="Create a no-hardware physical carrier / print-plan package.")
    print_plan.add_argument("--input", required=True)
    print_plan.add_argument("--output", required=True)
    print_plan.set_defaults(func=cmd_print_plan)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
