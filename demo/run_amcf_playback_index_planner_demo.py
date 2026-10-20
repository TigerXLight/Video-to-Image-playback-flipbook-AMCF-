from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_playback_index_planner import build_playback_index_report  # noqa: E402


RUN_NAME = "AMCF_PLAYBACK_INDEX_PLANNER_DEMO_V1"


def build_demo_archive(path: Path) -> tuple[dict[str, object], dict[str, object]]:
    path.parent.mkdir(parents=True, exist_ok=True)
    members = {
        "manifest/native_manifest.json": b'{"variant_id":"planner-demo","frame_count":2}',
        "contracts/decoder_contract.json": b'{"decoder":"bounded-demo"}',
        "metrics/quality.json": b'{"mean_mae":0.0}',
        "media/decoded_preview.mp4": b"synthetic-decoded-output",
        "payload/residual_000.bin": b"synthetic-residual",
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    with zipfile.ZipFile(path) as zf:
        info_by_name = {info.filename: info for info in zf.infolist()}
    fingerprints = [
        {
            "entry_name": name,
            "crc": int(info_by_name[name].CRC),
            "uncompressed_size": int(info_by_name[name].file_size),
        }
        for name in sorted(members)
    ]
    decode_index = {
        "quick_lookup_maps": {
            "by_role": {
                "manifest": ["manifest/native_manifest.json"],
                "decoder_contract": ["contracts/decoder_contract.json"],
                "metrics": ["metrics/quality.json"],
                "decoded_output": ["media/decoded_preview.mp4"],
                "residual_payload": ["payload/residual_000.bin"],
            }
        },
        "validation_fingerprints": fingerprints,
    }
    seek_index = {"frames": [{"frame_index": 0, "entry": "media/decoded_preview.mp4"}]}
    return decode_index, seek_index


def run_demo(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / "playback_index_demo.amcf.zip"
    decode_index, seek_index = build_demo_archive(archive)
    report = build_playback_index_report(archive, decode_index, seek_index)
    report = {
        "run_name": RUN_NAME,
        **report,
        "generated_output_committed": False,
    }
    (output_dir / "playback_index_planner_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "PLAYBACK_INDEX_PLANNER_SUMMARY.md").write_text(
        "\n".join(
            [
                "# AMCF Playback Index Planner Demo Summary",
                "",
                f"- run_name: {RUN_NAME}",
                f"- final_passed: {str(report['final_passed']).lower()}",
                f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
                "- hardware_validation_claimed: false",
                "- physical_level_5_claimed: false",
                "- manufactured_player_claimed: false",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return report


def main() -> int:
    report = run_demo(REPO_ROOT / "output" / "amcf_playback_index_planner_demo")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
