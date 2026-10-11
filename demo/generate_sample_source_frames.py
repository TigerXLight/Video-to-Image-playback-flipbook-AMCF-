from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_FRAME_COUNT = 8
DEFAULT_WIDTH = 128
DEFAULT_HEIGHT = 72
DEFAULT_FPS = 12


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def frame_pixels(index: int, width: int, height: int) -> bytes:
    data = bytearray()
    box_size = max(8, min(width, height) // 5)
    box_x = (index * 11) % max(1, width - box_size)
    box_y = height // 2 - box_size // 2
    for y in range(height):
        for x in range(width):
            r = (x * 3 + index * 17) % 256
            g = (y * 4 + index * 23) % 256
            b = ((x + y) * 2 + index * 31) % 256
            if box_x <= x < box_x + box_size and box_y <= y < box_y + box_size:
                r, g, b = 235, 245, 255
            data.extend((r, g, b))
    return bytes(data)


def write_ppm(path: Path, width: int, height: int, pixels: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = f"P6\n{width} {height}\n255\n".encode("ascii")
    path.write_bytes(header + pixels)


def generate_source_frames(
    output_root: str | Path,
    frame_count: int = DEFAULT_FRAME_COUNT,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    fps: int = DEFAULT_FPS,
) -> dict[str, Any]:
    root = Path(output_root)
    frames_dir = root / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_entries: list[dict[str, Any]] = []
    for index in range(frame_count):
        frame_name = f"frame_{index:03d}.ppm"
        frame_path = frames_dir / frame_name
        write_ppm(frame_path, width, height, frame_pixels(index, width, height))
        frame_entries.append(
            {
                "frame_index": index,
                "file": f"frames/{frame_name}",
                "width": width,
                "height": height,
                "fps": fps,
                "format": "ppm_p6",
                "bytes": frame_path.stat().st_size,
                "sha256": sha256_file(frame_path),
            }
        )
    manifest = {
        "schema": "amcf-source-frames-smoke-v1",
        "source_type": "generated_source_frames",
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "fps": fps,
        "frame_entries": frame_entries,
        "claim_boundary": {
            "physical_proof_claimed": False,
            "hardware_validation_claimed": False,
            "final_ui_claimed": False,
            "physical_prototype_built": False,
        },
    }
    (root / "source_frames_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic AMCF smoke-test source frames.")
    parser.add_argument("--output-root", default=str(Path(__file__).resolve().parents[1] / "examples" / "source_frames"))
    parser.add_argument("--frame-count", type=int, default=DEFAULT_FRAME_COUNT)
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS)
    args = parser.parse_args()
    manifest = generate_source_frames(args.output_root, args.frame_count, args.width, args.height, args.fps)
    print(json.dumps({"ok": True, "frame_count": manifest["frame_count"], "manifest": str(Path(args.output_root) / "source_frames_manifest.json")}, indent=2))


if __name__ == "__main__":
    main()
