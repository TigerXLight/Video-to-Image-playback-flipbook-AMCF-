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
from amcf_source_seeded_event_materializer import build_source_seeded_archive, validate_source_seeded_archive


def _print_result(result: dict[str, Any]) -> int:
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok", False) else 1


def cmd_status(_: argparse.Namespace) -> int:
    return _print_result(
        {
            "ok": True,
            "app": "AMCF public workflow CLI",
            "commands": [
                "status",
                "encode",
                "component-archive",
                "decode",
                "seeded-materializer",
                "diagnostics",
                "print-plan",
                "physical-roundtrip",
                "adapter-roundtrip",
                "hardware-plan",
                "hardware-providers",
                "software-control",
                "device-providers",
                "device-profiles",
                "device-conformance",
                "hardware-simulation",
                "carrier-render",
                "carrier-payload",
                "device-system",
                "device-discover",
                "setup",
            ],
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


def cmd_seeded_materializer(args: argparse.Namespace) -> int:
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    if args.profile_archive:
        if not args.canonical_archive:
            return _print_result({"ok": False, "error": "--canonical-archive is required with --profile-archive", "unsafe_acceptance_count": 1})
        archive_path = output / "amcf_4k_source_seeded_event_materializer.amcf.zip"
        result = build_source_seeded_archive(args.profile_archive, args.canonical_archive, archive_path, output)
    else:
        result = validate_source_seeded_archive(args.input_archive, output, render_video=args.render_video)
    return _print_result(result)


def cmd_diagnostics(args: argparse.Namespace) -> int:
    """Render the maintained 03M zone-motion and 08E heat diagnostics."""
    import cv2

    from amcf_diagnostic_profiles import flow_magnitude_heatmap, render_zone_motion_video, waterfall_03m_zones
    from amcf_motion_truth_diagnostics import analyze_pair

    input_video = Path(args.input_video)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(input_video))
    ok_a, previous = capture.read()
    ok_b, current = capture.read()
    capture.release()
    if not ok_a or not ok_b or previous is None or current is None:
        return _print_result({"ok": False, "error": "could not read two frames from the input video", "unsafe_acceptance_count": 0})

    height, width = previous.shape[:2]
    zones = waterfall_03m_zones(width, height)
    pair_result, overlay = analyze_pair(previous, current, zones, frame_index=1)
    overlay_path = output / "diagnostic_overlay.png"
    heatmap_path = output / "diagnostic_motion_heatmap.png"
    cv2.imwrite(str(overlay_path), overlay)
    cv2.imwrite(str(heatmap_path), flow_magnitude_heatmap(previous, current))
    zone_video = render_zone_motion_video(input_video, output / "diagnostic_zone_motion_overlay.mp4", zones=zones)
    unsafe = int(pair_result.get("unsafe_acceptance_count", 0))
    report = {
        "ok": bool(overlay_path.exists() and heatmap_path.exists() and zone_video.get("status") == "PASS" and unsafe == 0),
        "input_video": str(input_video.resolve()),
        "diagnostic_profile": "03M_waterfall_zone_motion",
        "heat_contract": "08E-compatible Farneback(0.5,3,15,3,5,1.2,0), per-frame NORM_MINMAX, TURBO",
        "overlay_path": str(overlay_path),
        "heatmap_path": str(heatmap_path),
        "zone_motion_overlay_path": str(zone_video.get("output_video", "")),
        "zone_count": len(pair_result.get("zones", [])),
        "processed_frame_count": zone_video.get("frame_count"),
        "translation_dx": pair_result.get("translation_dx"),
        "translation_dy": pair_result.get("translation_dy"),
        "unsafe_acceptance_count": unsafe,
        "claim_boundary": {
            "diagnostic_only": True,
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
        },
    }
    (output / "diagnostics_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return _print_result(report)


def cmd_physical_roundtrip(args: argparse.Namespace) -> int:
    """Run the deterministic software-only printer/reader/player corridor fixture."""
    from amcf_cross_corridor_roundtrip import write_cross_corridor_roundtrip_demo

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = write_cross_corridor_roundtrip_demo(project_root, Path(args.output))
    report = result["roundtrip_report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_adapter_roundtrip(args: argparse.Namespace) -> int:
    """Run the shared software-only physical adapter contract."""
    from amcf_physical_adapters import run_physical_software_adapter_roundtrip

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = run_physical_software_adapter_roundtrip(project_root, Path(args.output))
    report = result["report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_hardware_plan(args: argparse.Namespace) -> int:
    """Create the offline Windows printer, reader, and player adapter plan."""
    from amcf_hardware_adapter_planning import run_hardware_adapter_plan

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = run_hardware_adapter_plan(project_root, Path(args.output))
    report = result["report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_hardware_providers(args: argparse.Namespace) -> int:
    """Run the provider-neutral simulated hardware handshake."""
    from amcf_hardware_provider_runtime import run_hardware_provider_runtime

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = run_hardware_provider_runtime(project_root, Path(args.output))
    report = result["report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_software_control(args: argparse.Namespace) -> int:
    """Run the versioned software-only control protocol session."""
    from amcf_software_control_protocol import run_software_control_session

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = run_software_control_session(project_root, Path(args.output))
    report = result["report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_device_providers(args: argparse.Namespace) -> int:
    """Discover and exercise selected software or explicitly enabled device adapters."""
    from amcf_device_provider_adapters import run_device_provider_discovery

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = run_device_provider_discovery(
        project_root,
        Path(args.output),
        printer_backend=args.printer_backend,
        reader_backend=args.reader_backend,
        player_backend=args.player_backend,
        printer_name=args.printer_name,
        reader_device=args.reader_device,
        reader_source=args.reader_source,
        player_port=args.player_port,
        enable_hardware=args.enable_hardware,
    )
    report = result["report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_device_profiles(args: argparse.Namespace) -> int:
    """Validate a device-profile bundle and run its selected provider set."""
    from amcf_device_profiles import run_device_profile_validation

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = run_device_profile_validation(
        project_root,
        Path(args.output),
        profile_path=args.profile,
        enable_hardware=args.enable_hardware,
    )
    report = result["report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_device_conformance(args: argparse.Namespace) -> int:
    """Run the universal legacy/current printer-reader-player conformance contract."""
    from amcf_device_interface_conformance import run_device_interface_conformance

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = run_device_interface_conformance(project_root, Path(args.output))
    report = result["report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_hardware_simulation(args: argparse.Namespace) -> int:
    """Run the complete no-hardware printer, reader, and player simulation."""
    from amcf_universal_hardware_simulation import run_universal_hardware_simulation

    project_root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[1]
    result = run_universal_hardware_simulation(project_root, Path(args.output))
    report = result["report"]
    return _print_result(
        {
            "ok": bool(report.get("final_passed")),
            "project_root": str(project_root),
            "output_dir": result.get("output_dir", str(Path(args.output).resolve())),
            **result,
        }
    )


def cmd_carrier_render(args: argparse.Namespace) -> int:
    """Render a generated physical carrier package as scan/print artifacts."""
    from amcf_carrier_renderer import render_carrier_package

    result = render_carrier_package(args.carrier_root, args.output, args.formats.split(","))
    return _print_result(result)


def cmd_carrier_payload(args: argparse.Namespace) -> int:
    """Render, recover, and natively decode an exact AMCF archive carrier payload."""
    from amcf_carrier_payload import run_native_payload_roundtrip

    result = run_native_payload_roundtrip(
        args.input_archive,
        args.output,
        page_bytes=args.page_bytes,
        write_pdf=not args.no_pdf,
    )
    return _print_result(result)


def cmd_device_system(args: argparse.Namespace) -> int:
    """Run rendering, printer job, scan recovery, discovery, calibration, and player control."""
    from amcf_device_system import run_device_software_system

    result = run_device_software_system(
        args.carrier_package,
        args.output,
        printer_backend=args.printer_backend,
        reader_backend=args.reader_backend,
        player_backend=args.player_backend,
        printer_name=args.printer_name,
        reader_device=args.reader_device,
        player_port=args.player_port,
        player_device=args.player_device,
        native_archive_path=args.native_archive,
    )
    return _print_result(result)


def cmd_device_discover(args: argparse.Namespace) -> int:
    """Enumerate available Windows providers and always include simulation devices."""
    from amcf_device_system import discover_devices

    result = discover_devices()
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result["output"] = str(output.resolve())
    return _print_result({"ok": True, **result})


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

    seeded = sub.add_parser(
        "seeded-materializer",
        help="Validate or build the compact source-seeded 4K AMCF event-materializer profile.",
    )
    seeded_source = seeded.add_mutually_exclusive_group(required=True)
    seeded_source.add_argument("--input-archive", help="Existing source-seeded materializer archive to validate/decode.")
    seeded_source.add_argument("--profile-archive", help="4K compressed-seed profile archive used to build a materializer archive.")
    seeded.add_argument("--canonical-archive", help="Canonical low-resolution event/mask archive required with --profile-archive.")
    seeded.add_argument("--output", required=True, help="Output directory for the report, archive, and optional review video.")
    seeded.add_argument("--render-video", action="store_true", help="Render the materialized component-composited review MP4.")
    seeded.set_defaults(func=cmd_seeded_materializer)

    diagnostics = sub.add_parser(
        "diagnostics",
        help="Render the maintained 03M zone-motion overlay and 08E motion-heat diagnostics for a video.",
    )
    diagnostics.add_argument("--input-video", required=True)
    diagnostics.add_argument("--output", required=True)
    diagnostics.set_defaults(func=cmd_diagnostics)

    print_plan = sub.add_parser("print-plan", help="Create a no-hardware physical carrier / print-plan package.")
    print_plan.add_argument("--input", required=True)
    print_plan.add_argument("--output", required=True)
    print_plan.set_defaults(func=cmd_print_plan)

    physical = sub.add_parser(
        "physical-roundtrip",
        help="Run the no-hardware PC-to-printer, reader-to-PC, and player-to-PC software corridor fixture.",
    )
    physical.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    physical.add_argument("--output", required=True)
    physical.set_defaults(func=cmd_physical_roundtrip)

    adapter = sub.add_parser(
        "adapter-roundtrip",
        help="Run the shared fail-closed software adapter contract across all physical corridors.",
    )
    adapter.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    adapter.add_argument("--output", required=True)
    adapter.set_defaults(func=cmd_adapter_roundtrip)

    hardware_plan = sub.add_parser(
        "hardware-plan",
        help="Validate the offline Windows printer, reader, and physical-player adapter plan.",
    )
    hardware_plan.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    hardware_plan.add_argument("--output", required=True)
    hardware_plan.set_defaults(func=cmd_hardware_plan)

    providers = sub.add_parser(
        "hardware-providers",
        help="Run provider-neutral printer, reader, and player handshakes with simulated implementations.",
    )
    providers.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    providers.add_argument("--output", required=True)
    providers.set_defaults(func=cmd_hardware_providers)

    software_control = sub.add_parser(
        "software-control",
        help="Run the versioned software-only control protocol across printer, reader, and player corridors.",
    )
    software_control.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    software_control.add_argument("--output", required=True)
    software_control.set_defaults(func=cmd_software_control)

    device = sub.add_parser(
        "device-providers",
        help="Discover and exercise concrete printer, reader, and player provider adapters.",
    )
    device.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    device.add_argument("--output", required=True)
    device.add_argument("--printer-backend", choices=["file", "windows-spooler"], default="file")
    device.add_argument("--reader-backend", choices=["folder", "windows-wia"], default="folder")
    device.add_argument("--player-backend", choices=["loopback", "serial"], default="loopback")
    device.add_argument("--printer-name", help="Windows Print Spooler printer name when that backend is selected.")
    device.add_argument("--reader-device", help="Windows WIA device name when that backend is selected.")
    device.add_argument("--reader-source", help="Folder containing captured sections for the folder reader backend.")
    device.add_argument("--player-port", help="Serial port for the JSON-line player backend.")
    device.add_argument(
        "--enable-hardware",
        action="store_true",
        help="Explicitly enable the selected hardware transport; failures remain fail-closed.",
    )
    device.set_defaults(func=cmd_device_providers)

    profiles = sub.add_parser(
        "device-profiles",
        help="Validate a printer, reader, and player profile bundle before provider operation.",
    )
    profiles.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    profiles.add_argument("--profile", help="JSON device-profile bundle; built-in software defaults are used when omitted.")
    profiles.add_argument("--output", required=True)
    profiles.add_argument(
        "--enable-hardware",
        action="store_true",
        help="Allow a profile that requests hardware to reach its selected transport; failures remain fail-closed.",
    )
    profiles.set_defaults(func=cmd_device_profiles)

    conformance = sub.add_parser(
        "device-conformance",
        help="Run one universal conformance report across legacy and current device-interface software paths.",
    )
    conformance.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    conformance.add_argument("--output", required=True)
    conformance.set_defaults(func=cmd_device_conformance)

    simulation = sub.add_parser(
        "hardware-simulation",
        help="Run the complete software-only printer, reader, virtual carrier, and player simulation.",
    )
    simulation.add_argument("--project-root", help="Repository or bundle root containing tests/fixtures/amcf_software_io.")
    simulation.add_argument("--output", required=True)
    simulation.set_defaults(func=cmd_hardware_simulation)

    carrier_render = sub.add_parser(
        "carrier-render",
        help="Render a physical carrier package as printable SVG, PNG, and PDF artifacts.",
    )
    carrier_render.add_argument("--carrier-root", required=True)
    carrier_render.add_argument("--output", required=True)
    carrier_render.add_argument("--formats", default="svg,png,pdf", help="Comma-separated formats: svg,png,pdf.")
    carrier_render.set_defaults(func=cmd_carrier_render)

    carrier_payload = sub.add_parser(
        "carrier-payload",
        help="Render and recover exact native AMCF archive bytes through printable payload pages.",
    )
    carrier_payload.add_argument("--input-archive", required=True)
    carrier_payload.add_argument("--output", required=True)
    carrier_payload.add_argument("--page-bytes", type=int, default=16 * 1024)
    carrier_payload.add_argument("--no-pdf", action="store_true", help="Skip the optional multi-page PDF output.")
    carrier_payload.set_defaults(func=cmd_carrier_payload)

    device_system = sub.add_parser(
        "device-system",
        help="Run the complete universal physical software layer with rendering, printer, reader, and player simulation.",
    )
    device_system.add_argument("--carrier-package", required=True, help="Generated physical carrier package root.")
    device_system.add_argument("--output", required=True)
    device_system.add_argument("--printer-backend", choices=["simulation", "win32print"], default="simulation")
    device_system.add_argument("--reader-backend", choices=["folder-image", "wia", "twain"], default="folder-image")
    device_system.add_argument("--player-backend", choices=["simulation", "serial", "hid"], default="simulation")
    device_system.add_argument("--printer-name", help="Windows printer name for --printer-backend win32print.")
    device_system.add_argument("--reader-device", help="WIA/TWAIN device name when a real reader backend is selected.")
    device_system.add_argument("--player-port", help="Serial player port when --player-backend serial is selected.")
    device_system.add_argument("--player-device", help="HID player path when --player-backend hid is selected.")
    device_system.add_argument(
        "--native-archive",
        help="Native AMCF archive to encode into the physical payload lane; defaults to the carrier package's source archive when present.",
    )
    device_system.set_defaults(func=cmd_device_system)

    discover = sub.add_parser(
        "device-discover",
        help="Discover available Windows printer, WIA/TWAIN reader, serial/HID player, and simulation providers.",
    )
    discover.add_argument("--output", help="Optional JSON output path.")
    discover.set_defaults(func=cmd_device_discover)

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
