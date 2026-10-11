from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any


AMCF_SCHEMA = "amcf-digital-smoke-v1"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_source_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = ["frame_count", "width", "height", "fps", "frame_entries"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"source frame manifest missing required keys: {missing}")
    if len(data.get("frame_entries", [])) != int(data["frame_count"]):
        raise ValueError("source frame manifest frame_count does not match frame_entries")
    return data


def encode_source_frames(source_manifest_path: str | Path, output_archive_path: str | Path) -> dict[str, Any]:
    source_manifest_path = Path(source_manifest_path)
    source_root = source_manifest_path.parent
    source_manifest = load_source_manifest(source_manifest_path)
    output_archive_path = Path(output_archive_path)
    output_archive_path.parent.mkdir(parents=True, exist_ok=True)

    frame_entries: list[dict[str, Any]] = []
    payloads: list[tuple[Path, str]] = []
    for entry in source_manifest["frame_entries"]:
        source_rel = str(entry["file"])
        source_path = source_root / source_rel
        if not source_path.exists():
            raise FileNotFoundError(f"missing source frame payload: {source_rel}")
        actual_hash = sha256_file(source_path)
        expected_hash = str(entry.get("sha256", ""))
        if expected_hash and actual_hash != expected_hash:
            raise ValueError(f"source frame hash mismatch before encoding: {source_rel}")
        archive_path = f"frames/frame_{int(entry['frame_index']):03d}.ppm"
        payloads.append((source_path, archive_path))
        frame_entries.append(
            {
                "frame_index": int(entry["frame_index"]),
                "payload_path": archive_path,
                "source_path": source_rel,
                "width": int(entry.get("width", source_manifest["width"])),
                "height": int(entry.get("height", source_manifest["height"])),
                "format": str(entry.get("format", "ppm_p6")),
                "bytes": source_path.stat().st_size,
                "sha256": actual_hash,
            }
        )

    manifest = {
        "amcf_schema": AMCF_SCHEMA,
        "source_type": source_manifest.get("source_type", "generated_source_frames"),
        "archive_payload_kind": "source_frame_payloads",
        "frame_count": int(source_manifest["frame_count"]),
        "width": int(source_manifest["width"]),
        "height": int(source_manifest["height"]),
        "fps": int(source_manifest["fps"]),
        "frame_entries": frame_entries,
        "hash_algorithm": "sha256",
        "created_by": "amcf_digital_encoder.py",
        "created_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "claim_boundary": {
            "physical_proof_claimed": False,
            "hardware_validation_claimed": False,
            "final_ui_claimed": False,
            "manufacturing_readiness_claimed": False,
            "physical_prototype_built": False,
            "arbitrary_real_video_support_claimed": False,
        },
    }

    with zipfile.ZipFile(output_archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
        for source_path, archive_path in payloads:
            zf.write(source_path, archive_path)

    return {
        "ok": True,
        "archive_path": str(output_archive_path),
        "amcf_schema": AMCF_SCHEMA,
        "frame_count": manifest["frame_count"],
        "archive_sha256": sha256_file(output_archive_path),
        "claim_boundary": manifest["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Encode source frames into a minimal AMCF digital archive.")
    parser.add_argument("source_manifest")
    parser.add_argument("output_archive")
    args = parser.parse_args()
    print(json.dumps(encode_source_frames(args.source_manifest, args.output_archive), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
