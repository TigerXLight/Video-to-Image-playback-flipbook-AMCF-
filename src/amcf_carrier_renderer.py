from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any, Iterable

from amcf_physical_carrier import REQUIRED_LANES, sha256_file, validate_physical_carrier_package


SWATCHES: list[tuple[str, tuple[int, int, int]]] = [
    ("black", (0, 0, 0)),
    ("white", (255, 255, 255)),
    ("red", (220, 40, 40)),
    ("green", (40, 170, 70)),
    ("blue", (45, 95, 220)),
    ("cyan", (30, 190, 205)),
    ("magenta", (205, 55, 185)),
    ("yellow", (230, 190, 35)),
]


@dataclass(frozen=True)
class CarrierRenderConfig:
    width_px: int = 1600
    height_px: int = 1000
    margin_px: int = 52
    marker_px: int = 34
    dpi: int = 300


def _rgb_hex(rgb: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % rgb


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def _lane_geometry(config: CarrierRenderConfig) -> list[dict[str, Any]]:
    left = config.margin_px * 2
    top = 205
    width = config.width_px - (config.margin_px * 4)
    height = 520
    gap = 12
    lane_width = (width - gap * (len(REQUIRED_LANES) - 1)) / len(REQUIRED_LANES)
    lanes: list[dict[str, Any]] = []
    for index, name in enumerate(REQUIRED_LANES):
        lanes.append({
            "name": name,
            "x": int(round(left + index * (lane_width + gap))),
            "y": top,
            "width": int(round(lane_width)),
            "height": height,
        })
    return lanes


def _metadata_for_section(
    section: dict[str, Any],
    config: CarrierRenderConfig,
    section_count: int,
) -> dict[str, Any]:
    markers = [
        {"name": "top_left", "x": config.margin_px, "y": config.margin_px},
        {"name": "top_right", "x": config.width_px - config.margin_px - config.marker_px, "y": config.margin_px},
        {"name": "bottom_left", "x": config.margin_px, "y": config.height_px - config.margin_px - config.marker_px},
        {"name": "bottom_right", "x": config.width_px - config.margin_px - config.marker_px, "y": config.height_px - config.margin_px - config.marker_px},
    ]
    return {
        "schema": "amcf-carrier-render-v1",
        "width_px": config.width_px,
        "height_px": config.height_px,
        "dpi": config.dpi,
        "section_index": int(section.get("section_index", 0)),
        "section_count": int(section_count),
        "section_file": str(section.get("section_file", "")),
        "section_file_sha256": str(section.get("section_file_sha256", "")),
        "markers": markers,
        "marker_size_px": config.marker_px,
        "lanes": _lane_geometry(config),
        "swatches": [
            {"name": name, "rgb": list(rgb)} for name, rgb in SWATCHES
        ],
        "pixel_recovery_contract": {
            "registration": "black_corner_squares",
            "lane_presence": "non-white_lane_area",
            "colour_registry": "bottom_swatch_row",
            "source_payload_pixels_embedded": False,
        },
    }


def _lane_summary(section: dict[str, Any], lane_name: str) -> str:
    value = section.get("lanes", {}).get(lane_name, {})
    text = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return text[:170]


def _svg_for_section(section: dict[str, Any], metadata: dict[str, Any]) -> str:
    w = int(metadata["width_px"])
    h = int(metadata["height_px"])
    index = int(metadata["section_index"])
    count = int(metadata["section_count"])
    section_id = f"section_{index:04d}"
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" data-amcf-section="{section_id}">',
        '<rect width="100%" height="100%" fill="#f7f7f3"/>',
        f'<text x="120" y="92" font-family="Arial, sans-serif" font-size="34" fill="#111">AMCF PHYSICAL CARRIER / {index:04d} of {count:04d}</text>',
        f'<text x="120" y="135" font-family="monospace" font-size="18" fill="#333">TIMING-{index:04d} | indexed upright section | scan/recovery surface</text>',
    ]
    for marker in metadata["markers"]:
        lines.append(
            f'<rect x="{marker["x"]}" y="{marker["y"]}" width="{metadata["marker_size_px"]}" height="{metadata["marker_size_px"]}" fill="#000" data-registration="{marker["name"]}"/>'
        )
    lane_colors = ["#d8e8f5", "#e4e4e4", "#dcefdc", "#f7e8b4", "#eadcf3", "#f2d8d8"]
    for lane_index, lane in enumerate(metadata["lanes"]):
        color = lane_colors[lane_index % len(lane_colors)]
        x, y, lw, lh = lane["x"], lane["y"], lane["width"], lane["height"]
        name = str(lane["name"])
        summary = _lane_summary(section, name)
        lines.extend([
            f'<rect x="{x}" y="{y}" width="{lw}" height="{lh}" rx="6" fill="{color}" stroke="#333" stroke-width="3" data-lane="{escape(name)}"/>',
            f'<text x="{x + 16}" y="{y + 38}" font-family="Arial, sans-serif" font-size="20" fill="#111">{escape(name)}</text>',
            f'<text x="{x + 16}" y="{y + 75}" font-family="monospace" font-size="13" fill="#333">{escape(summary[:48])}</text>',
            f'<text x="{x + 16}" y="{y + 106}" font-family="monospace" font-size="13" fill="#333">{escape(summary[48:96])}</text>',
        ])
        for line_index in range(5):
            yy = y + 145 + line_index * 58
            lines.append(f'<line x1="{x + 14}" y1="{yy}" x2="{x + lw - 14}" y2="{yy}" stroke="#ffffff" stroke-opacity="0.72" stroke-width="2"/>')
    swatch_y = h - 112
    lines.append(f'<text x="{120}" y="{swatch_y - 18}" font-family="Arial, sans-serif" font-size="18" fill="#111">COLOUR REGISTRY / scan calibration row</text>')
    for swatch_index, (name, rgb) in enumerate(SWATCHES):
        x = 120 + swatch_index * 112
        lines.extend([
            f'<rect x="{x}" y="{swatch_y}" width="76" height="48" fill="{_rgb_hex(rgb)}" stroke="#111" stroke-width="2" data-swatch="{name}"/>',
            f'<text x="{x}" y="{swatch_y + 68}" font-family="monospace" font-size="13" fill="#111">{name}</text>',
        ])
    lines.append(f'<text x="{w - 620}" y="{h - 35}" font-family="monospace" font-size="14" fill="#222">sha256:{escape(str(section.get("section_file_sha256", ""))[:32])}</text>')
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def _draw_png(section: dict[str, Any], metadata: dict[str, Any], output_path: Path) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:  # pragma: no cover - exercised on minimal installations
        raise RuntimeError("Pillow is required for PNG/PDF carrier rendering") from exc

    width = int(metadata["width_px"])
    height = int(metadata["height_px"])
    image = Image.new("RGB", (width, height), (247, 247, 243))
    draw = ImageDraw.Draw(image)
    try:
        title_font = ImageFont.truetype("arial.ttf", 34)
        body_font = ImageFont.truetype("arial.ttf", 20)
        mono_font = ImageFont.truetype("consola.ttf", 13)
    except OSError:
        title_font = body_font = mono_font = ImageFont.load_default()
    index = int(metadata["section_index"])
    count = int(metadata["section_count"])
    draw.text((120, 48), f"AMCF PHYSICAL CARRIER / {index:04d} of {count:04d}", fill=(17, 17, 17), font=title_font)
    draw.text((120, 112), f"TIMING-{index:04d} | indexed upright section | scan/recovery surface", fill=(51, 51, 51), font=mono_font)
    for marker in metadata["markers"]:
        x, y = int(marker["x"]), int(marker["y"])
        size = int(metadata["marker_size_px"])
        draw.rectangle((x, y, x + size, y + size), fill=(0, 0, 0))
    lane_colors = [(216, 232, 245), (228, 228, 228), (220, 239, 220), (247, 232, 180), (234, 220, 243), (242, 216, 216)]
    for lane_index, lane in enumerate(metadata["lanes"]):
        x, y = int(lane["x"]), int(lane["y"])
        lw, lh = int(lane["width"]), int(lane["height"])
        draw.rectangle((x, y, x + lw, y + lh), fill=lane_colors[lane_index % len(lane_colors)], outline=(51, 51, 51), width=3)
        name = str(lane["name"])
        draw.text((x + 16, y + 20), name, fill=(17, 17, 17), font=body_font)
        summary = _lane_summary(section, name)
        draw.text((x + 16, y + 64), summary[:34], fill=(51, 51, 51), font=mono_font)
        draw.text((x + 16, y + 84), summary[34:68], fill=(51, 51, 51), font=mono_font)
        for line_index in range(5):
            yy = y + 145 + line_index * 58
            draw.line((x + 14, yy, x + lw - 14, yy), fill=(255, 255, 255), width=2)
    swatch_y = height - 112
    draw.text((120, swatch_y - 28), "COLOUR REGISTRY / scan calibration row", fill=(17, 17, 17), font=body_font)
    for swatch_index, (name, rgb) in enumerate(SWATCHES):
        x = 120 + swatch_index * 112
        draw.rectangle((x, swatch_y, x + 76, swatch_y + 48), fill=rgb, outline=(17, 17, 17), width=2)
        draw.text((x, swatch_y + 56), name, fill=(17, 17, 17), font=mono_font)
    draw.text((width - 620, height - 35), f"sha256:{str(section.get('section_file_sha256', ''))[:32]}", fill=(34, 34, 34), font=mono_font)
    image.save(output_path, format="PNG", optimize=True)


def render_carrier_package(
    carrier_root: str | Path,
    output_dir: str | Path,
    formats: Iterable[str] = ("svg", "png", "pdf"),
    config: CarrierRenderConfig | None = None,
) -> dict[str, Any]:
    carrier_root = Path(carrier_root).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    config = config or CarrierRenderConfig()
    requested = {str(item).lower().lstrip(".") for item in formats}
    if "pdf" in requested:
        requested.add("png")
    validation = validate_physical_carrier_package(carrier_root)
    if not validation.get("ok"):
        return {"ok": False, "error": "carrier_package_invalid", "validation": validation, "unsafe_acceptance_count": 0}
    manifest_path = carrier_root / "physical_carrier_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sections = list(manifest.get("sections", []))
    section_outputs: list[dict[str, Any]] = []
    rendered_pngs: list[Path] = []
    for section in sections:
        index = int(section.get("section_index", len(section_outputs)))
        metadata = _metadata_for_section(section, config, len(sections))
        stem = f"section_{index:04d}"
        outputs: dict[str, str] = {}
        if "svg" in requested:
            svg_path = output_dir / f"{stem}.svg"
            svg_path.write_text(_svg_for_section(section, metadata), encoding="utf-8")
            outputs["svg"] = str(svg_path)
        if "png" in requested:
            png_path = output_dir / f"{stem}.png"
            _draw_png(section, metadata, png_path)
            rendered_pngs.append(png_path)
            outputs["png"] = str(png_path)
        metadata_path = output_dir / f"{stem}.render.json"
        metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        outputs["metadata"] = str(metadata_path)
        outputs["section_file_sha256"] = str(section.get("section_file_sha256", ""))
        section_outputs.append({"section_index": index, "outputs": outputs, "metadata": metadata})

    pdf_path: Path | None = None
    if "pdf" in requested:
        try:
            from PIL import Image
            images = [Image.open(path).convert("RGB") for path in rendered_pngs]
            if images:
                pdf_path = output_dir / "amcf_carrier_sections.pdf"
                images[0].save(pdf_path, "PDF", resolution=config.dpi, save_all=True, append_images=images[1:])
        except ImportError:
            pdf_path = None
    if pdf_path is not None and pdf_path.exists():
        for item in section_outputs:
            item["outputs"]["pdf"] = str(pdf_path)
    render_manifest = {
        "schema": "amcf-carrier-render-package-v1",
        "carrier_manifest": str(manifest_path),
        "carrier_id": manifest.get("carrier_id"),
        "section_count": len(sections),
        "formats_requested": sorted(requested),
        "sections": section_outputs,
        "pdf_path": str(pdf_path) if pdf_path else None,
        "render_config": config.__dict__,
        "source_payload_pixels_embedded": False,
        "real_printing_performed": False,
        "hardware_validation_claimed": False,
        "unsafe_acceptance_count": 0,
    }
    render_manifest_path = output_dir / "carrier_render_manifest.json"
    render_manifest_path.write_text(json.dumps(render_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    hashes = {path.name: sha256_file(path) for path in output_dir.iterdir() if path.is_file() and path.name != render_manifest_path.name}
    render_manifest["output_sha256"] = hashes
    render_manifest_path.write_text(json.dumps(render_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "ok": bool(section_outputs) and all((output_dir / f"section_{int(item['section_index']):04d}.svg").exists() for item in section_outputs if "svg" in requested),
        "render_manifest_path": str(render_manifest_path),
        "section_count": len(section_outputs),
        "formats": sorted(requested),
        "sections": section_outputs,
        "pdf_path": str(pdf_path) if pdf_path else None,
        "real_printing_performed": False,
        "hardware_validation_claimed": False,
        "unsafe_acceptance_count": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Render AMCF carrier sections as SVG, PNG, and PDF.")
    parser.add_argument("carrier_root")
    parser.add_argument("output_dir")
    parser.add_argument("--formats", default="svg,png,pdf")
    args = parser.parse_args()
    result = render_carrier_package(args.carrier_root, args.output_dir, args.formats.split(","))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
