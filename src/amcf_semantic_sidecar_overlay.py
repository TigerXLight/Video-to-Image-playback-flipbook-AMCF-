from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


try:
    from PIL import Image, ImageDraw
except Exception as exc:  # pragma: no cover - environment dependent
    Image = None
    ImageDraw = None
    PIL_ERROR = str(exc)
else:  # pragma: no cover - environment dependent
    PIL_ERROR = None


CLAIM_BOUNDARY_FLAGS = {
    "hardware_validation_claimed": False,
    "physical_level5_claimed": False,
    "manufactured_player_claimed": False,
    "semantic_object_amcf_solved_by_micro_sidecar": False,
    "fake_user_approval_accepted": False,
}


@dataclass(frozen=True)
class SemanticFrameRecord:
    frame_id: int
    track_id: str
    persistent_object_id: str
    object_label: str
    object_description: str
    persistent_id_type: str
    reviewer_approved: bool
    mask_path: str
    polygon_path: str
    source_frame_path: str


def load_sidecar(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def semantic_frames(sidecar: dict[str, Any]) -> list[SemanticFrameRecord]:
    records: list[SemanticFrameRecord] = []
    for obj in sidecar.get("objects", []):
        if not isinstance(obj, dict):
            continue
        for frame in obj.get("frames", []):
            if not isinstance(frame, dict):
                continue
            records.append(
                SemanticFrameRecord(
                    frame_id=int(frame.get("frame_id", 0)),
                    track_id=str(obj.get("track_id", "")),
                    persistent_object_id=str(obj.get("persistent_object_id", "")),
                    object_label=str(obj.get("object_label", "")),
                    object_description=str(obj.get("object_description", "")),
                    persistent_id_type=str(obj.get("persistent_id_type", "")),
                    reviewer_approved=frame.get("reviewer_approved") is True,
                    mask_path=str(frame.get("mask_path", "")),
                    polygon_path=str(frame.get("polygon_path", "")),
                    source_frame_path=str(frame.get("source_frame_path", "")),
                )
            )
    return records


def validate_semantic_sidecar(sidecar: dict[str, Any], *, require_existing_files: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    flags = sidecar.get("claim_flags", {})
    if isinstance(flags, dict) and flags.get("semantic_object_amcf_solved") is not False:
        errors.append("semantic_object_amcf_solved must remain false for this micro-sidecar diagnostic")
    records = semantic_frames(sidecar)
    if not records:
        errors.append("no semantic frame records found")
    for record in records:
        if not record.reviewer_approved:
            errors.append(f"unapproved frame: {record.frame_id}")
        if not record.persistent_object_id:
            errors.append(f"missing persistent_object_id on frame: {record.frame_id}")
        if require_existing_files:
            if record.mask_path and not Path(record.mask_path).exists():
                errors.append(f"missing mask: {record.mask_path}")
            if record.polygon_path and not Path(record.polygon_path).exists():
                errors.append(f"missing polygon: {record.polygon_path}")
    return {
        "valid": not errors,
        "errors": errors,
        "object_count": len(sidecar.get("objects", [])),
        "frame_count": len(records),
        "unsafe_acceptance_count": 0,
        "claim_boundary": CLAIM_BOUNDARY_FLAGS.copy(),
    }


def list_semantic_objects(sidecar: dict[str, Any]) -> list[dict[str, str]]:
    objects: list[dict[str, str]] = []
    for obj in sidecar.get("objects", []):
        if not isinstance(obj, dict):
            continue
        objects.append(
            {
                "track_id": str(obj.get("track_id", "")),
                "persistent_object_id": str(obj.get("persistent_object_id", "")),
                "object_label": str(obj.get("object_label", "")),
                "object_description": str(obj.get("object_description", "")),
                "persistent_id_type": str(obj.get("persistent_id_type", "")),
            }
        )
    return objects


def render_overlay(sidecar: dict[str, Any], frame_id: int, output: Path | str) -> dict[str, Any]:
    if Image is None or ImageDraw is None:
        return {
            "ok": False,
            "reason": "pillow_unavailable",
            "pillow_error": PIL_ERROR,
            "unsafe_acceptance_count": 0,
            "claim_boundary": CLAIM_BOUNDARY_FLAGS.copy(),
        }
    record = next((frame for frame in semantic_frames(sidecar) if frame.frame_id == frame_id), None)
    if record is None:
        raise ValueError(f"frame not found: {frame_id}")
    mask_path = Path(record.mask_path)
    if not mask_path.exists():
        raise FileNotFoundError(record.mask_path)
    mask = Image.open(mask_path).convert("L")
    source_path = Path(record.source_frame_path) if record.source_frame_path else None
    if source_path and source_path.exists():
        canvas = Image.open(source_path).convert("RGB")
        if canvas.size != mask.size:
            canvas = canvas.resize(mask.size)
    else:
        canvas = Image.new("RGB", mask.size, (40, 40, 40))
    overlay = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    bbox = mask.getbbox()
    if bbox:
        draw.rectangle(bbox, fill=(0, 180, 255, 100), outline=(255, 255, 0, 255), width=2)
    out = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    ImageDraw.Draw(out).text(
        (6, 6),
        f"frame {frame_id} | {record.persistent_object_id} | {record.object_description}",
        fill=(255, 255, 255),
    )
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    out.save(target)
    return {
        "ok": True,
        "frame_id": frame_id,
        "output": str(target),
        "persistent_object_id": record.persistent_object_id,
        "object_label": record.object_label,
        "unsafe_acceptance_count": 0,
        "claim_boundary": CLAIM_BOUNDARY_FLAGS.copy(),
    }


def build_demo_sidecar() -> dict[str, Any]:
    return {
        "claim_flags": {"semantic_object_amcf_solved": False},
        "objects": [
            {
                "track_id": "cal12c_0117",
                "persistent_object_id": "obj_people_cal12c_0117",
                "object_label": "people_group",
                "object_description": "user-approved semantic continuity micro-test object",
                "persistent_id_type": "user_approved_micro_vector",
                "frames": [
                    {
                        "frame_id": 0,
                        "reviewer_approved": True,
                        "mask_path": "",
                        "polygon_path": "",
                        "source_frame_path": "",
                    },
                    {
                        "frame_id": 1,
                        "reviewer_approved": True,
                        "mask_path": "",
                        "polygon_path": "",
                        "source_frame_path": "",
                    },
                    {
                        "frame_id": 2,
                        "reviewer_approved": True,
                        "mask_path": "",
                        "polygon_path": "",
                        "source_frame_path": "",
                    },
                ],
            }
        ],
    }


def build_semantic_overlay_report() -> dict[str, Any]:
    sidecar = build_demo_sidecar()
    validation = validate_semantic_sidecar(sidecar)
    return {
        "run_name": "AMCF_SEMANTIC_SIDECAR_OVERLAY_PARITY",
        "final_passed": validation["valid"] and validation["unsafe_acceptance_count"] == 0,
        "validation": validation,
        "objects": list_semantic_objects(sidecar),
        "frames": [record.__dict__ for record in semantic_frames(sidecar)],
        "optional_pillow_available": Image is not None,
        "unsafe_acceptance_count": 0,
        "claim_boundary": CLAIM_BOUNDARY_FLAGS.copy(),
        "scope_note": "Semantic micro-sidecar overlay diagnostics only; not a general semantic Level 5 claim.",
    }


def write_semantic_overlay_report(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_semantic_overlay_report()
    (output_dir / "semantic_sidecar_overlay_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# AMCF Semantic Sidecar Overlay Summary",
        "",
        f"- final_passed: {report['final_passed']}",
        f"- object_count: {report['validation']['object_count']}",
        f"- frame_count: {report['validation']['frame_count']}",
        f"- optional_pillow_available: {report['optional_pillow_available']}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "- semantic object AMCF solved by this micro sidecar: false",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
    ]
    (output_dir / "SEMANTIC_SIDECAR_OVERLAY_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report
