from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS, REQUIRED_SECTION_LANES
from amcf_software_io_fixtures import load_fixture_bundle


RUN_NAME = "AMCF_PC_TO_PRINTER_LAYOUT_PROTOTYPE_V1"
LAYOUT_VERSION = "amcf_print_layout_v1"


@dataclass(frozen=True)
class PrintLaneGeometry:
    lane_type: str
    x_mm: float
    y_mm: float
    width_mm: float
    height_mm: float


@dataclass(frozen=True)
class PrintSectionLayout:
    section_id: str
    section_index: int
    sheet_id: str
    origin_x_mm: float
    origin_y_mm: float
    width_mm: float
    height_mm: float
    lanes: list[PrintLaneGeometry]


@dataclass(frozen=True)
class PrintLayoutManifest:
    run_name: str
    layout_version: str
    source_manifest_id: str
    sheet_size: str
    printer_safe_margin_mm: float
    sections: list[PrintSectionLayout]
    claim_boundary_flags: dict[str, bool] = field(default_factory=lambda: dict(CLAIM_BOUNDARY_FLAGS))
    unsafe_acceptance_count: int = 0


def _lane_geometry(section_x: float, section_y: float, section_width: float, lane_height: float) -> list[PrintLaneGeometry]:
    lanes: list[PrintLaneGeometry] = []
    for index, lane_type in enumerate(REQUIRED_SECTION_LANES):
        lanes.append(
            PrintLaneGeometry(
                lane_type=lane_type,
                x_mm=section_x,
                y_mm=round(section_y + index * lane_height, 2),
                width_mm=section_width,
                height_mm=lane_height,
            )
        )
    return lanes


def build_print_layout_manifest(bundle: dict[str, Any]) -> PrintLayoutManifest:
    package = bundle["package"]
    manifest = package["manifest"]
    sections: list[PrintSectionLayout] = []
    margin = 8.0
    section_width = 58.0
    section_height = 36.0
    lane_height = round(section_height / len(REQUIRED_SECTION_LANES), 2)
    for section in manifest["physical_sections"]:
        index = int(section["section_index"])
        column = index % 3
        row = index // 3
        origin_x = round(margin + column * (section_width + 6.0), 2)
        origin_y = round(margin + row * (section_height + 8.0), 2)
        sections.append(
            PrintSectionLayout(
                section_id=section["section_id"],
                section_index=index,
                sheet_id="sheet-000",
                origin_x_mm=origin_x,
                origin_y_mm=origin_y,
                width_mm=section_width,
                height_mm=section_height,
                lanes=_lane_geometry(origin_x, origin_y, section_width, lane_height),
            )
        )
    return PrintLayoutManifest(
        run_name=RUN_NAME,
        layout_version=LAYOUT_VERSION,
        source_manifest_id=manifest["manifest_id"],
        sheet_size="A4-abstract-mm",
        printer_safe_margin_mm=margin,
        sections=sections,
    )


def validate_print_layout(layout: PrintLayoutManifest) -> dict[str, Any]:
    checks_passed: list[str] = []
    checks_failed: list[str] = []
    if layout.layout_version == LAYOUT_VERSION:
        checks_passed.append("layout_version_supported")
    else:
        checks_failed.append("layout_version_unsupported")
    if layout.printer_safe_margin_mm >= 5.0:
        checks_passed.append("printer_safe_margin_present")
    else:
        checks_failed.append("printer_safe_margin_too_small")
    section_ids = [section.section_id for section in layout.sections]
    if len(section_ids) == len(set(section_ids)):
        checks_passed.append("section_layout_ids_unique")
    else:
        checks_failed.append("duplicate_section_layout_id")
    for section in layout.sections:
        lane_types = {lane.lane_type for lane in section.lanes}
        missing = [lane for lane in REQUIRED_SECTION_LANES if lane not in lane_types]
        if missing:
            checks_failed.append(f"missing_layout_lane:{section.section_id}:{','.join(missing)}")
    flags = dict(layout.claim_boundary_flags)
    final_passed = len(checks_failed) == 0 and layout.unsafe_acceptance_count == 0 and not any(flags.values())
    return {
        "run_name": RUN_NAME,
        "final_passed": final_passed,
        "checks_passed": checks_passed,
        "checks_failed": checks_failed,
        "section_layout_count": len(layout.sections),
        "claim_boundary_flags": flags,
        "unsafe_acceptance_count": layout.unsafe_acceptance_count,
        "no_hardware_printer_driver_used": True,
        "pdf_generation_used": False,
        "image_dependency_used": False,
        "barcode_dependency_used": False,
    }


def object_to_dict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, list):
        return [object_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: object_to_dict(item) for key, item in value.items()}
    return value


def write_print_layout_demo(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    bundle = load_fixture_bundle(repo_root)
    layout = build_print_layout_manifest(bundle)
    report = validate_print_layout(layout)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "print_layout_manifest.json").write_text(json.dumps(object_to_dict(layout), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "print_layout_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = [
        "# AMCF PC to Printer Layout Prototype",
        "",
        "This is a no-hardware abstract print-layout prototype.",
        "",
        f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
        f"- section_layout_count: {report['section_layout_count']}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "- hardware validation claimed: false",
        "- physical Level 5 claimed: false",
        "- manufactured player claimed: false",
        "- real printer driver used: false",
        "- PDF generation used: false",
        "",
    ]
    (out / "PC_TO_PRINTER_LAYOUT_SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    return {"layout": object_to_dict(layout), "report": report, "output_dir": str(out)}
