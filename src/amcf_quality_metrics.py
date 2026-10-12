from __future__ import annotations

import hashlib
import importlib.util
import math
from pathlib import Path
from typing import Any


def optional_quality_dependency_status() -> dict[str, bool]:
    return {
        "skimage_available": importlib.util.find_spec("skimage") is not None,
        "numpy_available": importlib.util.find_spec("numpy") is not None,
    }


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_ppm(path: str | Path) -> tuple[int, int, bytes]:
    data = Path(path).read_bytes()
    tokens: list[bytes] = []
    index = 0
    while len(tokens) < 4:
        while index < len(data) and data[index:index + 1].isspace():
            index += 1
        if index < len(data) and data[index:index + 1] == b"#":
            while index < len(data) and data[index:index + 1] not in (b"\n", b"\r"):
                index += 1
            continue
        start = index
        while index < len(data) and not data[index:index + 1].isspace():
            index += 1
        tokens.append(data[start:index])
    if tokens[0] != b"P6":
        raise ValueError("only binary PPM P6 frames are supported")
    width = int(tokens[1])
    height = int(tokens[2])
    max_value = int(tokens[3])
    if max_value != 255:
        raise ValueError("only 8-bit PPM frames are supported")
    if index < len(data) and data[index:index + 1].isspace():
        index += 1
    pixels = data[index:]
    expected = width * height * 3
    if len(pixels) != expected:
        raise ValueError(f"PPM payload length mismatch: expected {expected}, got {len(pixels)}")
    return width, height, pixels


def ppm_bytes(width: int, height: int, pixels: bytes) -> bytes:
    if len(pixels) != width * height * 3:
        raise ValueError("pixel payload does not match width and height")
    return f"P6\n{width} {height}\n255\n".encode("ascii") + pixels


def write_ppm(path: str | Path, width: int, height: int, pixels: bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(ppm_bytes(width, height, pixels))


def mean_absolute_error_rgb(expected: bytes, actual: bytes) -> float:
    if len(expected) != len(actual):
        raise ValueError("payload lengths differ")
    if not expected:
        return 0.0
    total = sum(abs(a - b) for a, b in zip(expected, actual))
    return total / len(expected)


def psnr_db(expected: bytes, actual: bytes) -> float | None:
    if len(expected) != len(actual):
        raise ValueError("payload lengths differ")
    if not expected:
        return None
    mse = sum((a - b) ** 2 for a, b in zip(expected, actual)) / len(expected)
    if mse == 0:
        return None
    return 20.0 * math.log10(255.0 / math.sqrt(mse))


def compare_ppm_frames(expected_path: str | Path, actual_path: str | Path) -> dict[str, Any]:
    expected_width, expected_height, expected_pixels = read_ppm(expected_path)
    actual_width, actual_height, actual_pixels = read_ppm(actual_path)
    same_dimensions = expected_width == actual_width and expected_height == actual_height
    if not same_dimensions:
        return {
            "ok": False,
            "same_dimensions": False,
            "expected_size": [expected_width, expected_height],
            "actual_size": [actual_width, actual_height],
            "mean_absolute_error": None,
            "psnr_db": None,
            "ssim": None,
            "ssim_available": False,
        }
    mae = mean_absolute_error_rgb(expected_pixels, actual_pixels)
    return {
        "ok": mae == 0.0,
        "same_dimensions": True,
        "expected_size": [expected_width, expected_height],
        "actual_size": [actual_width, actual_height],
        "mean_absolute_error": mae,
        "psnr_db": psnr_db(expected_pixels, actual_pixels),
        "ssim": None,
        "ssim_available": False,
        "dependency_status": optional_quality_dependency_status(),
    }


def compare_ppm_frame_folders(expected_dir: str | Path, actual_dir: str | Path) -> dict[str, Any]:
    expected = sorted(Path(expected_dir).glob("frame_*.ppm"))
    actual = sorted(Path(actual_dir).glob("frame_*.ppm"))
    pairs = list(zip(expected, actual))
    comparisons = [compare_ppm_frames(left, right) for left, right in pairs]
    mae_values = [float(item["mean_absolute_error"]) for item in comparisons if item["mean_absolute_error"] is not None]
    return {
        "ok": len(expected) == len(actual) and all(item["ok"] for item in comparisons),
        "expected_frame_count": len(expected),
        "actual_frame_count": len(actual),
        "compared_frame_count": len(comparisons),
        "mean_absolute_error": sum(mae_values) / len(mae_values) if mae_values else None,
        "frames": comparisons,
        "ssim_available": False,
        "dependency_status": optional_quality_dependency_status(),
    }
