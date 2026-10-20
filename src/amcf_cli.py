from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from amcf_component_event_archive import build_component_event_archive, decode_component_event_archive
from amcf_component_event_viewer import build_component_event_viewer
from amcf_deliverable_package import build_deliverable_package
from amcf_physical_carrier import generate_physical_carrier_from_amcf_archive
from amcf_quality_metrics import compare_ppm_frame_folders
from amcf_video_pipeline import decode_amcf_to_frames, decode_amcf_to_video, encode_video_to_amcf
from amcf_digital_encoder import encode_source_frames
from amcf_digital_validator import validate_amcf_archive
from amcf_setup import run_setup


def _print_result(result: dict[str, Any]) -> int:
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok", False) else 1


def cmd_status(_: argparse.Namespace) -> int:
    return _print_result(
        {
            "ok": True,
            "app": "AMCF public workflow CLI",
            "commands": ["status", "encode", "component-archive", "decode", "print-plan", "setup"],
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
        diagnostic_state_manifest_path=args.diagnostic_state,
        use_diagnostic_components=args.use_diagnostic_components,
    )
    decoded = decode_component_event_archive(archive_path, output / "decoded")
    quality = compare_ppm_frame_folders(Path(args.input_frames_manifest).parent / "frames", Path(decoded["decoded_frames_dir"]))
    viewer = build_component_event_viewer(
        archive_report=archive,
        decoded_report=decoded,
        quality_report=quality,
        output_dir=output / "viewer",
    )
    deliverable = build_deliverable_package(
        archive_path=archive_path,
        source_frames_dir=Path(args.input_frames_manifest).parent / "frames",
        decoded_frames_dir=Path(decoded["decoded_frames_dir"]),
        quality_report=quality,
        viewer_dir=output / "viewer",
        output_dir=output / "deliverable_package",
        fps=int(decoded.get("fps", 24) or 24),
    )
    result = {
        "ok": archive["ok"] and decoded["ok"] and quality["ok"] and viewer["ok"] and deliverable["ok"],
        "archive": archive,
        "decode": decoded,
        "quality": quality,
        "viewer": viewer,
        "deliverable": deliverable,
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


def cmd_setup(args: argparse.Namespace) -> int:
    result = run_setup(
        manifest_path=args.manifest,
        project_root=args.project_root,
        dependency_root=args.dependency_root,
        python_executable=args.python_executable,
        existing_config=args.existing_config,
        install_research=args.install_research,
        install_deep=args.install_deep,
        clone_repositories=args.clone_repositories,
        download_checkpoints=args.download_checkpoints,
        download_hoot=args.download_hoot,
        accept_upstream_licenses=args.accept_upstream_licenses,
        accept_noncommercial=args.accept_noncommercial,
        accept_hoot_terms=args.accept_hoot_terms,
        force=args.force,
        config_output=args.config_output,
        report_output=args.report_output,
    )
    action_requested = any(
        getattr(args, name)
        for name in ("install_research", "install_deep", "clone_repositories", "download_checkpoints", "download_hoot")
    )
    if not action_requested:
        result = {**result, "ok": True, "check_only": True}
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
    component.add_argument(
        "--diagnostic-state",
        type=Path,
        help="Normalized AMCF diagnostic state or a historical Test 02 tracks_manifest.json.",
    )
    component.add_argument(
        "--use-diagnostic-components",
        action="store_true",
        help="Use contour-backed diagnostic tracks for component events and close uncovered pixels exactly.",
    )
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

    setup = sub.add_parser("setup", help="Check or prepare Python, FFmpeg, SAM2, CoTracker, checkpoints, and the optional HOOT proof dataset.")
    setup.add_argument("--manifest", help="Dependency manifest JSON.")
    setup.add_argument("--project-root", help="Repository root receiving the generated runtime config.")
    setup.add_argument("--dependency-root", help="External runtime directory; defaults to <project>/.amcf-runtime.")
    setup.add_argument("--python", dest="python_executable", help="Python executable used for pip and runtime config.")
    setup.add_argument("--existing-config", help="Optional existing AMCF config to include in the status report.")
    setup.add_argument("--install-research", action="store_true", help="Install the pinned base research requirements.txt.")
    setup.add_argument(
        "--install-deep",
        action="store_true",
        help="Install deep Python packages, clone pinned SAMURAI/CoTracker trees, and download their checkpoints.",
    )
    setup.add_argument("--clone-repositories", action="store_true", help="Clone/update pinned external research repositories.")
    setup.add_argument("--download-checkpoints", action="store_true", help="Download and checksum declared checkpoints.")
    setup.add_argument("--download-hoot", action="store_true", help="Download and checksum the declared HOOT proof vector dataset.")
    setup.add_argument("--accept-upstream-licenses", action="store_true", help="Confirm that upstream repository/checkpoint terms were reviewed.")
    setup.add_argument("--accept-noncommercial", action="store_true", help="Confirm the CoTracker non-commercial/research boundary.")
    setup.add_argument("--accept-hoot-terms", action="store_true", help="Confirm that the HOOT dataset terms were reviewed and permit the intended use.")
    setup.add_argument("--force", action="store_true", help="Redownload an existing checkpoint after checksum verification is bypassed.")
    setup.add_argument("--config-output", help="Generated runtime config path.")
    setup.add_argument("--report-output", help="Optional JSON setup report path.")
    setup.add_argument("--check", action="store_true", help="Perform an availability check; this is the default when no action flag is used.")
    setup.set_defaults(func=cmd_setup)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
