from __future__ import annotations

import json
import time
import zipfile
from pathlib import Path
from typing import Any


STARTUP_ROLES = (
    "manifest",
    "decoder_contract",
    "provenance",
    "metrics",
    "metadata",
    "residual_manifest",
)

PLAYBACK_ROLES = (
    "truth_baseline",
    "decoded_output",
    "selected_candidate",
    "fullrate_control",
    "media",
    "residual_payload",
)


def unique_entries(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def entries_for_roles(index: dict[str, Any], roles: tuple[str, ...] = STARTUP_ROLES) -> list[str]:
    by_role = index.get("quick_lookup_maps", {}).get("by_role", {})
    entries: list[str] = []
    for role in roles:
        entries.extend(str(entry) for entry in by_role.get(role, []))
    return unique_entries(entries)


def validate_fingerprints(
    archive_path: str | Path,
    decode_index: dict[str, Any],
    *,
    limit: int = 100,
) -> dict[str, Any]:
    archive_path = Path(archive_path)
    start = time.perf_counter()
    mismatches: list[str] = []
    checked = 0
    with zipfile.ZipFile(archive_path) as zf:
        info_by_name = {info.filename: info for info in zf.infolist()}
        for fingerprint in decode_index.get("validation_fingerprints", [])[:limit]:
            checked += 1
            entry_name = str(fingerprint["entry_name"])
            info = info_by_name.get(entry_name)
            if (
                info is None
                or int(info.CRC) != int(fingerprint.get("crc", -1))
                or int(info.file_size) != int(fingerprint.get("uncompressed_size", -1))
            ):
                mismatches.append(entry_name)
    return {
        "checked_count": checked,
        "fingerprint_mismatch_count": len(mismatches),
        "fingerprint_mismatches": mismatches,
        "seconds": round(time.perf_counter() - start, 8),
        "ok": not mismatches,
    }


def build_startup_plan(decode_index: dict[str, Any], seek_index: dict[str, Any] | None = None) -> dict[str, Any]:
    by_role = decode_index.get("quick_lookup_maps", {}).get("by_role", {})
    entries = entries_for_roles(decode_index, STARTUP_ROLES)
    return {
        "archive_validation_steps": [
            "open_zip",
            "validate_archive_size_if_available",
            "validate_selected_fingerprints",
        ],
        "index_validation_steps": [
            "load_decode_index",
            "load_seek_index",
            "match_archive_id_if_available",
        ],
        "eager_metadata_reads": entries,
        "required_manifest_entries": by_role.get("manifest", []),
        "required_decoder_contract_entries": by_role.get("decoder_contract", []),
        "optional_entries": by_role.get("metrics", []) + by_role.get("provenance", []),
        "seek_index_frame_count": len((seek_index or {}).get("frames", [])),
        "cache_recommendations": {
            "startup_metadata": "eager",
            "media_payloads": "stream",
            "unknown": "lazy",
        },
    }


def build_playback_plan(decode_index: dict[str, Any]) -> dict[str, Any]:
    by_role = decode_index.get("quick_lookup_maps", {}).get("by_role", {})
    media_entries: list[dict[str, str]] = []
    for role in PLAYBACK_ROLES:
        for entry in by_role.get(role, []):
            media_entries.append({"role": role, "entry": str(entry)})
    decoded = by_role.get("decoded_output", [])
    native_components = by_role.get("residual_payload", []) + by_role.get("residual_manifest", [])
    if decoded:
        playback_path = "fallback_decoded_output_available"
    elif native_components:
        playback_path = "native_component_planning_ready_decoder_required"
    else:
        playback_path = "playback_media_not_identified"
    return {
        "media_entries": media_entries,
        "playback_path": playback_path,
        "fallback_decoded_output_available": bool(decoded),
        "native_components_present": bool(native_components),
        "cache_prefetch_hints": {
            "decoded_output": "stream",
            "truth_baseline": "lazy",
            "selected_candidate": "lazy",
            "metadata": "eager",
        },
        "actions": [
            {"step": 1, "action": "validate_archive_and_indexes"},
            {"step": 2, "action": "load_manifest"},
            {"step": 3, "action": "load_decoder_contract_provenance_metrics"},
            {"step": 4, "action": "identify_decoded_output_if_available"},
            {"step": 5, "action": "identify_truth_control_candidate_media"},
            {"step": 6, "action": "identify_native_components_or_residuals"},
            {"step": 7, "action": playback_path},
        ],
    }


def read_startup_entries(archive_path: str | Path, startup_plan: dict[str, Any], *, max_bytes: int | None = None) -> dict[str, Any]:
    start = time.perf_counter()
    rows: list[dict[str, Any]] = []
    total = 0
    with zipfile.ZipFile(archive_path) as zf:
        for entry in startup_plan.get("eager_metadata_reads", []):
            try:
                data = zf.read(entry)
                if max_bytes is not None:
                    data = data[:max_bytes]
                total += len(data)
                rows.append({"entry": entry, "bytes_read": len(data), "ok": True})
            except Exception as exc:  # pragma: no cover - exercised through summary path
                rows.append({"entry": entry, "bytes_read": 0, "ok": False, "error": repr(exc)})
    return {
        "seconds": round(time.perf_counter() - start, 8),
        "bytes_read": total,
        "entries": rows,
        "ok": all(row["ok"] for row in rows),
    }


def build_playback_index_report(
    archive_path: str | Path,
    decode_index: dict[str, Any],
    seek_index: dict[str, Any],
) -> dict[str, Any]:
    start = time.perf_counter()
    startup_plan = build_startup_plan(decode_index, seek_index)
    playback_plan = build_playback_plan(decode_index)
    validation = validate_fingerprints(archive_path, decode_index)
    startup_read = read_startup_entries(archive_path, startup_plan)
    final_passed = validation["ok"] and startup_read["ok"]
    return {
        "archive_path": str(archive_path),
        "startup_plan": startup_plan,
        "playback_plan": playback_plan,
        "fingerprint_validation": validation,
        "startup_read": startup_read,
        "role_counts": {
            role: len(entries)
            for role, entries in decode_index.get("quick_lookup_maps", {}).get("by_role", {}).items()
        },
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "final_playback_engine_claimed": False,
        },
        "unsafe_acceptance_count": 0,
        "final_passed": final_passed,
        "total_seconds": round(time.perf_counter() - start, 8),
    }


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
