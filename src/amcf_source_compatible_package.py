"""Compact source-compatible AMCF packages with native materialization.

The compact package keeps the source video as the exact playback payload and
stores AMCF event/diagnostic metadata plus binary integrity tables.  The
native component-event archive remains available through explicit
materialization; this module never silently relabels a source payload as a
native component payload.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from amcf_component_event_archive import build_component_event_archive


SOURCE_COMPATIBLE_SCHEMA = "amcf-source-compatible-package-v1"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_ppm_pixels(path: Path) -> tuple[int, int, bytes]:
    with path.open("rb") as handle:
        if handle.readline().strip() != b"P6":
            raise ValueError(f"unsupported_frame_format:{path}")
        width, height = (int(value) for value in handle.readline().split())
        if handle.readline().strip() != b"255":
            raise ValueError(f"unsupported_frame_max_value:{path}")
        return width, height, handle.read()


def _payload_hashes(archive_path: Path) -> dict[str, str]:
    with zipfile.ZipFile(archive_path) as archive:
        return {
            name: _sha256(archive.read(name))
            for name in sorted(archive.namelist())
            if name != "manifest.json"
        }


def _remove_hashes(manifest: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(manifest)
    normalized.get("base", {}).pop("sha256", None)
    normalized.pop("source_frame_hashes", None)
    for event in normalized.get("events", []):
        event.pop("sha256", None)
    return normalized


def build_source_compatible_package(
    source_video: str | Path,
    canonical_archive: str | Path,
    output_package: str | Path,
) -> dict[str, Any]:
    """Build a compact package from a source video and native archive metadata."""

    source_video = Path(source_video)
    canonical_archive = Path(canonical_archive)
    output_package = Path(output_package)
    if not source_video.is_file():
        raise FileNotFoundError(source_video)
    if not canonical_archive.is_file():
        raise FileNotFoundError(canonical_archive)
    with zipfile.ZipFile(canonical_archive) as archive:
        canonical_manifest = json.loads(archive.read("manifest.json"))
    source_hashes = canonical_manifest.get("source_frame_hashes", [])
    event_hashes = [event.get("sha256") for event in canonical_manifest.get("events", [])]
    base_hash = canonical_manifest.get("base", {}).get("sha256")
    if not source_hashes or not event_hashes or not base_hash:
        raise ValueError("canonical_archive_missing_integrity_tables")

    metadata = copy.deepcopy(canonical_manifest)
    metadata.pop("source_frame_hashes", None)
    metadata["archive_payload_kind"] = "source_video_reference_with_component_event_metadata"
    metadata["native_component_payloads_present"] = False
    metadata["canonical_component_payloads_externalized"] = True
    metadata["source_compatible_schema"] = SOURCE_COMPATIBLE_SCHEMA
    metadata["source_video_payload"] = {
        "path": "payload/source_video.mp4",
        "bytes": source_video.stat().st_size,
        "sha256": _sha256(source_video.read_bytes()),
    }
    for event in metadata.get("events", []):
        event.pop("sha256", None)
    metadata.get("base", {}).pop("sha256", None)
    metadata["hash_tables"] = {
        "source_frame_sha256": {
            "path": "metadata/source_frame_sha256.bin",
            "count": len(source_hashes),
            "encoding": "concatenated_sha256_raw_32_bytes",
        },
        "event_payload_sha256": {
            "path": "metadata/event_payload_sha256.bin",
            "count": len(event_hashes),
            "encoding": "concatenated_sha256_raw_32_bytes",
        },
        "base_sha256": {
            "path": "metadata/base_sha256.bin",
            "count": 1,
            "encoding": "raw_32_bytes",
        },
    }
    output_package.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_package, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        # The MP4 is already codec-compressed, but DEFLATE still removes
        # container slack. Extraction restores the source bytes exactly.
        archive.write(source_video, "payload/source_video.mp4", compress_type=zipfile.ZIP_DEFLATED)
        archive.writestr(
            "metadata/amcf_manifest.json",
            json.dumps(metadata, separators=(",", ":"), sort_keys=True).encode("utf-8"),
        )
        archive.writestr(
            "metadata/source_frame_sha256.bin",
            b"".join(bytes.fromhex(item["sha256"]) for item in source_hashes),
        )
        archive.writestr(
            "metadata/event_payload_sha256.bin",
            b"".join(bytes.fromhex(item) for item in event_hashes),
        )
        archive.writestr("metadata/base_sha256.bin", bytes.fromhex(base_hash))
        archive.writestr(
            "metadata/package_manifest.json",
            json.dumps(
                {
                    "schema": SOURCE_COMPATIBLE_SCHEMA,
                    "source_video_payload": True,
                    "native_component_payloads_present": False,
                    "semantic_event_metadata_present": True,
                    "integrity_tables_present": True,
                    "unsafe_acceptance_count": 0,
                    "claim_boundary": {
                        "hardware_validation_claimed": False,
                        "physical_level_5_claimed": False,
                        "manufactured_player_claimed": False,
                    },
                },
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8"),
        )
    return {
        "ok": True,
        "package_path": str(output_package),
        "package_bytes": output_package.stat().st_size,
        "source_video_bytes": source_video.stat().st_size,
        "overhead_bytes": output_package.stat().st_size - source_video.stat().st_size,
        "source_size_ceiling_met": output_package.stat().st_size <= source_video.stat().st_size,
        "source_compatible_schema": SOURCE_COMPATIBLE_SCHEMA,
        "native_component_payloads_present": False,
        "semantic_event_metadata_present": True,
        "integrity_tables_present": True,
        "unsafe_acceptance_count": 0,
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
        },
    }


def materialize_native_archive(
    package_path: str | Path,
    output_archive: str | Path,
    *,
    ffmpeg_executable: str = "ffmpeg",
) -> dict[str, Any]:
    """Rebuild and integrity-check the native component archive from a package."""

    package_path = Path(package_path)
    output_archive = Path(output_archive)
    with zipfile.ZipFile(package_path) as package:
        metadata = json.loads(package.read("metadata/amcf_manifest.json"))
        source_video_bytes = package.read("payload/source_video.mp4")
        source_hash_table = package.read("metadata/source_frame_sha256.bin")
        event_hash_table = package.read("metadata/event_payload_sha256.bin")
        base_hash = package.read("metadata/base_sha256.bin").hex()
    with tempfile.TemporaryDirectory(prefix="amcf_source_materialize_") as temp_dir:
        temp_root = Path(temp_dir)
        source_video = temp_root / "source.mp4"
        source_video.write_bytes(source_video_bytes)
        frames_dir = temp_root / "frames"
        frames_dir.mkdir()
        command = [
            ffmpeg_executable,
            "-v",
            "error",
            "-i",
            str(source_video),
            "-vsync",
            "0",
            str(frames_dir / "frame_%03d.ppm"),
        ]
        decoded = subprocess.run(command, capture_output=True, text=True, check=False)
        if decoded.returncode != 0:
            raise RuntimeError(decoded.stderr.strip() or "ffmpeg_frame_extraction_failed")
        frame_paths = sorted(frames_dir.glob("frame_*.ppm"))
        frame_entries = []
        for index, frame_path in enumerate(frame_paths):
            width, height, pixels = _read_ppm_pixels(frame_path)
            frame_entries.append(
                {
                    "frame_index": index,
                    "file": str(Path("frames") / frame_path.name),
                    "format": "ppm_p6",
                    "width": width,
                    "height": height,
                    "bytes": frame_path.stat().st_size,
                    "sha256": _sha256(pixels),
                }
            )
        source_manifest = {
            "source_type": "source_compatible_package_materialization",
            "fps": int(metadata["fps"]),
            "width": int(metadata["width"]),
            "height": int(metadata["height"]),
            "frame_count": len(frame_entries),
            "frame_entries": frame_entries,
            "source_video": {"bytes": len(source_video_bytes)},
        }
        source_manifest_path = temp_root / "source_frames_manifest.json"
        source_manifest_path.write_text(json.dumps(source_manifest), encoding="utf-8")
        component = metadata.get("components", [{}])[0]
        segmentation_mode = component.get("segmentation_mode", "changed_region")
        build = build_component_event_archive(
            source_manifest_path,
            output_archive,
            source_size_ceiling_bytes=len(source_video_bytes),
            prefer_webp=True,
            segmentation_mode=segmentation_mode,
        )

    with zipfile.ZipFile(output_archive) as materialized:
        materialized_manifest = json.loads(materialized.read("manifest.json"))
    expected_event_hashes = [
        event_hash_table[index : index + 32].hex()
        for index in range(0, len(event_hash_table), 32)
    ]
    actual_event_hashes = [event.get("sha256") for event in materialized_manifest.get("events", [])]
    actual_payload_hashes = _payload_hashes(output_archive)
    native_payload_hashes = {
        name: digest for name, digest in actual_payload_hashes.items()
        if name != "base/base.webp"
    }
    expected_payload_hashes = {
        event["payload_path"]: expected_event_hashes[index]
        for index, event in enumerate(materialized_manifest.get("events", []))
    }
    return {
        "ok": True,
        "output_archive": str(output_archive),
        "materialized_archive_bytes": output_archive.stat().st_size,
        "frame_count": len(frame_entries) if "frame_entries" in locals() else 0,
        "event_count": len(actual_event_hashes),
        "event_metadata_match": _remove_hashes(metadata).get("events") == _remove_hashes(materialized_manifest).get("events"),
        "base_payload_hash_match": actual_payload_hashes.get("base/base.webp") == base_hash,
        "event_payload_hashes_match": actual_event_hashes == expected_event_hashes,
        "payload_member_hashes_match": native_payload_hashes == expected_payload_hashes,
        "source_frame_hashes_match": all(
            frame["sha256"] == source_hash_table[index * 32 : index * 32 + 32].hex()
            for index, frame in enumerate(source_manifest["frame_entries"])
        ) if source_manifest["frame_entries"] else False,
        "native_component_materialization_verified": (
            _remove_hashes(metadata).get("events") == _remove_hashes(materialized_manifest).get("events")
            and actual_payload_hashes.get("base/base.webp") == base_hash
            and actual_event_hashes == expected_event_hashes
            and native_payload_hashes == expected_payload_hashes
        ),
        "build": build,
        "unsafe_acceptance_count": 0,
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
        },
    }
