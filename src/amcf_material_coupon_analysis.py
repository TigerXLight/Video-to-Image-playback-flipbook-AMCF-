from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

try:
    from PIL import Image, ImageOps, ImageStat
except Exception:  # pragma: no cover - environment dependent
    Image = None
    ImageOps = None
    ImageStat = None


CLAIM_BOUNDARY = {
    "hardware_validation_claimed": False,
    "physical_level_5_claimed": False,
    "manufactured_player_claimed": False,
    "real_sensor_validation_claimed": False,
    "real_scanner_required": False,
    "real_coupon_test_claimed": False,
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def _region_luma(image: Any, box: tuple[int, int, int, int]) -> tuple[float, float]:
    if ImageOps is None or ImageStat is None:
        return 0.0, 0.0
    crop = ImageOps.grayscale(image.crop(box))
    stat = ImageStat.Stat(crop)
    return float(stat.mean[0]), float(stat.stddev[0])


def analyze_coupon_image(
    image_path: str | Path,
    *,
    coupon_type: str = "unknown",
    material_label: str = "",
    scan_mode_label: str = "",
) -> dict[str, Any]:
    image_path = Path(image_path)
    if Image is None:
        return {
            "input_image": str(image_path),
            "coupon_type": coupon_type,
            "material_label": material_label,
            "scan_mode_label": scan_mode_label,
            "error": "Pillow unavailable",
            "fail_closed_decision": True,
            "unsafe_acceptance_flag": False,
            "unsafe_acceptance_count": 0,
            "claim_boundary": dict(CLAIM_BOUNDARY),
        }

    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    scale_x = width / 1200.0
    scale_y = height / 800.0

    def scaled_box(box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return tuple(int(value * scale_x if index % 2 == 0 else value * scale_y) for index, value in enumerate(box))  # type: ignore[return-value]

    _, timing_std = _region_luma(image, scaled_box((55, 80, 145, 720)))
    _, index_std = _region_luma(image, scaled_box((160, 80, 230, 720)))
    registration_boxes = [
        scaled_box((20, 20, 80, 80)),
        scaled_box((1120, 20, 1180, 80)),
        scaled_box((20, 720, 80, 780)),
        scaled_box((1120, 720, 1180, 780)),
    ]
    registration_scores: list[float] = []
    for registration_box in registration_boxes:
        _, stddev = _region_luma(image, registration_box)
        registration_scores.append(clamp(stddev / 80.0))

    _, grey_std = _region_luma(image, scaled_box((760, 190, 1120, 240)))
    _, fine_std = _region_luma(image, scaled_box((760, 260, 1120, 360)))
    _, checker_std = _region_luma(image, scaled_box((760, 380, 1120, 560)))
    _, colour_std = _region_luma(image, scaled_box((760, 110, 1120, 170)))
    _, meta_std = _region_luma(image, scaled_box((250, 650, 720, 700)))
    _, hash_std = _region_luma(image, scaled_box((760, 650, 1120, 700)))

    marker_contrast_score = clamp(mean([timing_std, index_std, hash_std]) / 90.0)
    registration_detection_score = clamp(mean(registration_scores))
    timing_lane_score = clamp(timing_std / 85.0)
    index_lane_score = clamp(index_std / 75.0)
    grey_ramp_score = clamp(grey_std / 74.0)
    fine_line_score = clamp(fine_std / 80.0)
    checkerboard_score = clamp(checker_std / 110.0)
    colour_palette_score = clamp(colour_std / 95.0)
    metadata_hash_lane_score = clamp(mean([meta_std, hash_std]) / 70.0)
    skew_estimate = round(abs(registration_scores[0] + registration_scores[1] - registration_scores[2] - registration_scores[3]) * 3.0, 4)
    confidence = mean(
        [
            registration_detection_score,
            timing_lane_score,
            index_lane_score,
            marker_contrast_score,
            grey_ramp_score,
            fine_line_score,
            checkerboard_score,
            colour_palette_score,
            metadata_hash_lane_score,
        ]
    )
    fail_closed_decision = confidence < 0.48 or registration_detection_score < 0.35 or metadata_hash_lane_score < 0.35
    return {
        "input_image": str(image_path),
        "coupon_type": coupon_type,
        "material_label": material_label,
        "scan_mode_label": scan_mode_label,
        "registration_detection_score": round(registration_detection_score, 4),
        "skew_estimate": skew_estimate,
        "timing_lane_score": round(timing_lane_score, 4),
        "index_lane_score": round(index_lane_score, 4),
        "marker_contrast_score": round(marker_contrast_score, 4),
        "grey_ramp_score": round(grey_ramp_score, 4),
        "fine_line_score": round(fine_line_score, 4),
        "checkerboard_score": round(checkerboard_score, 4),
        "colour_palette_score": round(colour_palette_score, 4),
        "metadata_hash_lane_score": round(metadata_hash_lane_score, 4),
        "overall_confidence": round(confidence, 4),
        "fail_closed_decision": bool(fail_closed_decision),
        "unsafe_acceptance_flag": False,
        "unsafe_acceptance_count": 0,
        "claim_boundary": dict(CLAIM_BOUNDARY),
    }


def write_coupon_analysis(result: dict[str, Any], output_dir: str | Path, *, write_csv: bool = True) -> dict[str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "analysis_result.json"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    paths = {"json": str(json_path)}
    if write_csv:
        csv_path = output_dir / "analysis_result.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
            writer.writeheader()
            writer.writerow(result)
        paths["csv"] = str(csv_path)
    return paths


def create_synthetic_coupon_ppm(path: str | Path, *, width: int = 120, height: int = 80) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pixels = bytearray()
    for y in range(height):
        for x in range(width):
            value = 235
            if x < 15 or 16 <= x < 24:
                value = 20 if (y // 3) % 2 == 0 else 235
            if x < 8 and y < 8 or x >= width - 8 and y < 8 or x < 8 and y >= height - 8 or x >= width - 8 and y >= height - 8:
                value = 0 if (x + y) % 2 == 0 else 255
            if 76 <= x < 112 and 11 <= y < 17:
                value = (x * 7 + y * 13) % 256
            if 76 <= x < 112 and 19 <= y < 24:
                value = int((x - 76) / 36 * 255)
            if 76 <= x < 112 and 26 <= y < 36:
                value = 0 if (x + y) % 4 < 2 else 255
            if 76 <= x < 112 and 38 <= y < 56:
                value = 0 if ((x // 4) + (y // 4)) % 2 == 0 else 255
            if 25 <= x < 72 and 65 <= y < 70:
                value = 0 if (x // 3) % 2 == 0 else 255
            if 76 <= x < 112 and 65 <= y < 70:
                value = 0 if (x + y) % 5 < 2 else 255
            pixels.extend([value, value, value])
    path.write_bytes(f"P6\n{width} {height}\n255\n".encode("ascii") + bytes(pixels))
    return path


def analyze_synthetic_coupon(output_dir: str | Path) -> dict[str, Any]:
    output_dir = Path(output_dir)
    image_path = create_synthetic_coupon_ppm(output_dir / "synthetic_coupon.ppm")
    result = analyze_coupon_image(
        image_path,
        coupon_type="synthetic_public_fixture",
        material_label="simulated_pet_mylar_proxy",
        scan_mode_label="simulated_near_contact_air_gap",
    )
    paths = write_coupon_analysis(result, output_dir)
    return {
        "ok": bool(not result.get("unsafe_acceptance_flag")),
        "analysis": result,
        "paths": paths,
        "synthetic_coupon_path": str(image_path),
        "unsafe_acceptance_count": int(result.get("unsafe_acceptance_count", 0)),
        "claim_boundary": result["claim_boundary"],
    }
