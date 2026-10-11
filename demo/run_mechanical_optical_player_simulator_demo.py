from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_digital_encoder import encode_source_frames  # noqa: E402
from amcf_digital_validator import validate_amcf_archive  # noqa: E402
from amcf_mechanical_optical_player import simulate_mechanical_optical_playback, validate_mechanical_optical_player_timeline  # noqa: E402
from amcf_physical_carrier import generate_physical_carrier_from_amcf_archive, validate_physical_carrier_package  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


def main() -> None:
    out = PACKAGE / "demo" / "output" / "mechanical_optical_player"
    frames_root = out / "generated_source_frames"
    if out.exists():
        shutil.rmtree(out)
    frames_root.mkdir(parents=True, exist_ok=True)

    source_manifest = generate_source_frames(frames_root)
    source_manifest_path = frames_root / "source_frames_manifest.json"
    archive_path = out / "sample_video_source.amcf.zip"
    encode_source_frames(source_manifest_path, archive_path)
    amcf_validation = validate_amcf_archive(archive_path)
    generate_physical_carrier_from_amcf_archive(archive_path, out)
    carrier_validation = validate_physical_carrier_package(out)
    simulation = simulate_mechanical_optical_playback(out, out)
    timeline_validation = validate_mechanical_optical_player_timeline(out / "player_timeline.json")

    (out / "source_frames_manifest.json").write_text(json.dumps(source_manifest, indent=2, sort_keys=True), encoding="utf-8")
    result_lines = [
        "# Mechanical / Optical Player Simulator Demo Result",
        "",
        f"- source AMCF archive created: {'yes' if archive_path.exists() else 'no'}",
        f"- source AMCF archive validation pass: {'yes' if amcf_validation.get('ok') else 'no'}",
        f"- physical carrier package created: {'yes' if (out / 'physical_carrier_manifest.json').exists() else 'no'}",
        f"- physical carrier package validation pass: {'yes' if carrier_validation.get('ok') else 'no'}",
        f"- player simulator loaded carrier: {'yes' if simulation.get('loaded') else 'no'}",
        f"- view-gate states generated: {'yes' if (out / 'view_gate_states.json').exists() else 'no'}",
        f"- timeline generated: {'yes' if (out / 'player_timeline.json').exists() else 'no'}",
        f"- play/pause/step/reverse/seek simulated: {'yes' if timeline_validation.get('ok') else 'no'}",
        f"- validation pass: {'yes' if timeline_validation.get('ok') else 'no'}",
        f"- unsafe acceptance count: {timeline_validation.get('unsafe_acceptance_count', 0)}",
        "- real physical playback performed: no",
        "- digital-screen playback claimed: no",
        "- physical proof claimed: no",
        "- hardware validation claimed: no",
        "- final UI claimed: no",
        "",
        "This is a software simulator for the future mechanical/optical physical-player path. It does not use real optical hardware or define the physical player as a digital-screen device.",
    ]
    (out / "MECHANICAL_OPTICAL_PLAYER_SIMULATOR_DEMO_RESULT.md").write_text("\n".join(result_lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "ok": bool(amcf_validation.get("ok") and carrier_validation.get("ok") and simulation.get("ok") and timeline_validation.get("ok")),
        "source_amcf_archive_created": archive_path.exists(),
        "physical_carrier_package_created": (out / "physical_carrier_manifest.json").exists(),
        "player_simulator_loaded_carrier": simulation.get("loaded", False),
        "view_gate_states_generated": (out / "view_gate_states.json").exists(),
        "timeline_generated": (out / "player_timeline.json").exists(),
        "controls_simulated": bool(timeline_validation.get("ok")),
        "unsafe_acceptance_count": timeline_validation.get("unsafe_acceptance_count", 0),
        "digital_screen_playback_claimed": False,
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if amcf_validation.get("ok") and carrier_validation.get("ok") and simulation.get("ok") and timeline_validation.get("ok") else 1)


if __name__ == "__main__":
    main()
