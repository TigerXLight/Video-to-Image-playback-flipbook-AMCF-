from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_virtual_hardware import (  # noqa: E402
    FuturePhysicalPlaybackDevice,
    FuturePhysicalReaderAdapter,
    ReaderPlayerApplianceAdapter,
    SoftwarePlaybackDevice,
    VirtualCartridge,
    read_cartridge_to_handoff,
)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    out = PACKAGE / "output"
    out.mkdir(parents=True, exist_ok=True)
    cartridge = VirtualCartridge.load(PACKAGE / "examples" / "sample_virtual_cartridge.json")
    events, handoff = read_cartridge_to_handoff(cartridge)
    player = SoftwarePlaybackDevice()
    player.load_handoff_state(handoff)
    player.play()
    player.pause()
    player.seek_section(3)
    player.reverse_section()
    playback_status = {
        "software_playback": player.get_playback_status(),
        "validation": player.get_validation_status(),
        "output": player.get_output_status(),
        "future_physical_reader_adapter": FuturePhysicalReaderAdapter().get_status(),
        "future_physical_playback_device": FuturePhysicalPlaybackDevice().get_playback_status(),
        "reader_player_appliance_adapter": ReaderPlayerApplianceAdapter().get_status(),
    }

    (out / "demo_reader_events.json").write_text(json.dumps(events, indent=2), encoding="utf-8")
    (out / "demo_player_handoff_state.json").write_text(json.dumps(handoff.to_dict(), indent=2), encoding="utf-8")
    write_csv(out / "demo_validation_log.csv", handoff.validation_log_entries)
    summary = [
        "# Virtual Hardware Demo Summary",
        "",
        f"- `accepted_count`: {handoff.accepted_count}",
        f"- `rescanned_count`: {handoff.rescanned_count}",
        f"- `rejected_count`: {handoff.rejected_count}",
        f"- `degraded_count`: {handoff.degraded_count}",
        f"- `unsafe_acceptance_count`: {handoff.unsafe_acceptance_count}",
        f"- `future_physical_reader_placeholder_only`: {playback_status['future_physical_reader_adapter']['placeholder_only']}",
        f"- `future_physical_playback_placeholder_only`: {playback_status['future_physical_playback_device']['placeholder_only']}",
        f"- `reader_player_appliance_placeholder_only`: {playback_status['reader_player_appliance_adapter']['placeholder_only']}",
        "",
        "Software-only demo. No physical proof, physical Level 5, hardware validation, manufacturing readiness, real scans, or built prototype are claimed.",
    ]
    (out / "demo_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps({
        "accepted_count": handoff.accepted_count,
        "rescanned_count": handoff.rescanned_count,
        "rejected_count": handoff.rejected_count,
        "degraded_count": handoff.degraded_count,
        "unsafe_acceptance_count": handoff.unsafe_acceptance_count,
    }, indent=2))


if __name__ == "__main__":
    main()
