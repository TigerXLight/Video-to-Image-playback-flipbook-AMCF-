from __future__ import annotations

import json
from pathlib import Path
from typing import Any


VIEWER_SCHEMA = "amcf-player-ui-state-viewer-v1"
BOUNDARY_NOTE = "Viewer stub only - not final UI, not physical proof, not hardware validation."

REQUIRED_PLAYER_UI_STATE_KEYS = [
    "reconstructed_playback_status",
    "current_section",
    "timeline_sections",
    "accepted_count",
    "rescanned_count",
    "rejected_count",
    "degraded_count",
    "unsafe_acceptance_count",
    "reader_status",
    "cartridge_status",
    "marker_index_lock",
    "scan_lock",
    "colour_calibration_status",
    "hash_checksum_status",
    "fail_closed_status",
    "component_payload_list",
    "alpha_object_mask_status",
    "transform_metadata_summary",
    "residual_tile_payload_summary",
    "validation_log_rows",
]


def normalize_player_ui_state(raw: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in REQUIRED_PLAYER_UI_STATE_KEYS if key not in raw]
    if missing:
        raise ValueError(f"missing required player UI state keys: {missing}")

    unsafe_count = int(raw.get("unsafe_acceptance_count", 0))
    if unsafe_count != 0:
        raise ValueError("unsafe acceptance count is non-zero; viewer refuses to normalize unsafe state")

    normalized = dict(raw)
    normalized.setdefault("boundary_note", BOUNDARY_NOTE)
    normalized.setdefault("degraded_output_flags", [])
    normalized.setdefault("rejected_section_flags", [])
    normalized.setdefault("viewer_schema", VIEWER_SCHEMA)
    normalized.setdefault("hash_checksum_validation", raw.get("hash_checksum_status") in {"valid", "fail_closed_for_mismatch"})
    normalized["counts"] = {
        "accepted": int(raw.get("accepted_count", 0)),
        "rescanned": int(raw.get("rescanned_count", 0)),
        "rejected": int(raw.get("rejected_count", 0)),
        "degraded": int(raw.get("degraded_count", 0)),
        "unsafe_acceptance": unsafe_count,
    }
    normalized["validation_status"] = {
        "marker_index_lock": raw.get("marker_index_lock", "unknown"),
        "scan_lock": raw.get("scan_lock", "unknown"),
        "colour_calibration_status": raw.get("colour_calibration_status", "unknown"),
        "hash_checksum_status": raw.get("hash_checksum_status", "unknown"),
        "fail_closed_status": raw.get("fail_closed_status", "unknown"),
    }
    normalized["claim_boundary"] = {
        "final_ui_claimed": False,
        "physical_proof_claimed": False,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
    }
    normalized["unsafe_acceptance_count"] = unsafe_count
    return normalized


def load_player_ui_state(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_player_ui_state(state: dict[str, Any], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def render_player_ui_state_report(state: dict[str, Any]) -> str:
    counts = state.get("counts", {})
    validation = state.get("validation_status", {})
    components = state.get("component_payload_list", [])
    log_rows = state.get("validation_log_rows", [])

    component_lines = [
        f"- section `{item.get('section_index')}`: `{item.get('object_label')}` / `{item.get('payload_state')}` / mask `{item.get('alpha_object_mask_status')}`"
        for item in components
    ]
    log_lines = [
        f"- section `{row.get('section_index')}` attempt `{row.get('rescan_attempt')}`: `{row.get('decision')}` issues `{row.get('issues')}` unsafe `{row.get('unsafe_acceptance')}`"
        for row in log_rows
    ]

    return "\n".join(
        [
            "# AMCF Player UI State Report",
            "",
            f"- `playback_status`: {state.get('reconstructed_playback_status')}",
            f"- `current_section`: {state.get('current_section')}",
            f"- `accepted_count`: {counts.get('accepted')}",
            f"- `rescanned_count`: {counts.get('rescanned')}",
            f"- `rejected_count`: {counts.get('rejected')}",
            f"- `degraded_count`: {counts.get('degraded')}",
            f"- `unsafe_acceptance_count`: {counts.get('unsafe_acceptance')}",
            "",
            "## Validation Status",
            "",
            f"- `marker_index_lock`: {validation.get('marker_index_lock')}",
            f"- `scan_lock`: {validation.get('scan_lock')}",
            f"- `colour_calibration_status`: {validation.get('colour_calibration_status')}",
            f"- `hash_checksum_status`: {validation.get('hash_checksum_status')}",
            f"- `fail_closed_status`: {validation.get('fail_closed_status')}",
            "",
            "## Component Payloads",
            "",
            *(component_lines or ["- no components"]),
            "",
            "## Fail-Closed Summary",
            "",
            f"- rejected sections: {counts.get('rejected')}",
            f"- unsafe acceptance count: {counts.get('unsafe_acceptance')}",
            "- unsafe acceptance policy: zero tolerated",
            "",
            "## Validation Log",
            "",
            *(log_lines or ["- no validation log rows"]),
            "",
            "## Boundary Note",
            "",
            str(state.get("boundary_note", BOUNDARY_NOTE)),
        ]
    ) + "\n"


def write_player_ui_state_report(state: dict[str, Any], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_player_ui_state_report(state), encoding="utf-8")


def build_player_ui_state_outputs(input_path: str | Path, output_root: str | Path) -> dict[str, Any]:
    output_root = Path(output_root)
    normalized = normalize_player_ui_state(load_player_ui_state(input_path))
    normalized_path = output_root / "normalised_player_ui_state.json"
    report_path = output_root / "PLAYER_UI_STATE_REPORT.md"
    write_player_ui_state(normalized, normalized_path)
    write_player_ui_state_report(normalized, report_path)
    return {
        "ok": True,
        "viewer_schema": normalized["viewer_schema"],
        "normalized_state_path": str(normalized_path),
        "report_path": str(report_path),
        "unsafe_acceptance_count": normalized["unsafe_acceptance_count"],
        "claim_boundary": normalized["claim_boundary"],
        "counts": normalized["counts"],
    }
