"""Source-seeded 4K AMCF event materialization.

This is an explicit compact AMCF profile, not the strict native-pixel profile.
It keeps the canonical event graph and masks, decodes the embedded compressed
seed only as materialization input, samples every event state through its mask,
and composites the result.  Direct seed playback is deliberately forbidden.

The module is source-independent at decode time: the original source MP4 is
not required.  The embedded seed is the profile's source of 4K pixel values,
so ``native_component_pixel_payload_present`` remains false by contract.
"""

from __future__ import annotations

import bz2
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any
import zipfile

import numpy as np

from amcf_component_ffv1_temporal import _decode_byte_delta, _parse_events, _unpack_mask


FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)
VIDEO_SUFFIXES = (".mp4", ".mov", ".avi")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _fixed_member(archive: zipfile.ZipFile, name: str, data: bytes, *, deflate: bool = False) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED if deflate else zipfile.ZIP_STORED
    info.external_attr = 0o600 << 16
    archive.writestr(info, data)


def _read_exact(handle: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        block = handle.read(remaining)
        if not block:
            raise RuntimeError(f"seed ended before reading {size} bytes")
        chunks.append(block)
        remaining -= len(block)
    return b"".join(chunks)


def _resolve_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"required executable not found: {name}")
    return path


def _decode_mask_rows(graph: bytes, mask_member: bytes, low_width: int, low_height: int) -> list[dict[str, Any]]:
    events = _parse_events(graph)
    raw_mask_size = (low_width * low_height + 7) // 8
    mask_stream = bz2.decompress(mask_member)
    component_count = max((int(event["component_index"]) for event in events), default=-1) + 1
    previous = [bytes(raw_mask_size) for _ in range(component_count)]
    rows: list[dict[str, Any]] = []
    for ordinal, event in enumerate(events):
        component = int(event["component_index"])
        start = int(event["mask_offset"])
        packed = _decode_byte_delta(
            mask_stream[start : start + int(event["mask_bytes"])],
            raw_mask_size,
            previous[component],
        )
        previous[component] = packed
        low_mask = _unpack_mask(packed, low_height, low_width)
        if int(np.count_nonzero(low_mask)) != int(event["owned_pixels"]):
            raise ValueError(f"canonical mask ownership mismatch at event {ordinal}")
        rows.append({**event, "ordinal": ordinal, "mask_packed": packed, "low_mask": low_mask})
    return rows


def _load_archive_members(archive_path: Path) -> tuple[dict[str, Any], dict[str, Any], bytes, bytes, bytes, list[str], list[str]]:
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("manifest/manifest.json"))
        contract = json.loads(archive.read("metadata/materialization_contract.json"))
        graph = archive.read("metadata/canonical_event_graph.bin")
        mask_member = archive.read("metadata/canonical_masks.bin.bz2")
        event_hash_bytes = archive.read("metadata/materialized_4k_event_hashes.bin")
        frame_hash_bytes = archive.read("metadata/materialized_4k_frame_hashes.bin")
        seed_name = str(manifest["seed_member"])
        seed_member = archive.read(seed_name)
    if any(name.lower().endswith(VIDEO_SUFFIXES) for name in names):
        raise ValueError("archive contains an unexpected video-container member")
    if not manifest.get("source_seed_embedded") or not contract.get("no_external_source_required", False):
        raise ValueError("archive is not a source-seeded, source-independent materializer")
    event_hashes = [event_hash_bytes[i : i + 32].hex() for i in range(0, len(event_hash_bytes), 32)]
    frame_hashes = [frame_hash_bytes[i : i + 32].hex() for i in range(0, len(frame_hash_bytes), 32)]
    return manifest, contract, graph, mask_member, seed_member, event_hashes, frame_hashes


def _scaled_mask(low_mask: np.ndarray, scale_x: int, scale_y: int) -> np.ndarray:
    return np.repeat(np.repeat(low_mask, scale_y, axis=0), scale_x, axis=1)


def _start_seed_decoder(seed_path: Path):
    ffmpeg = _resolve_binary("ffmpeg")
    return subprocess.Popen(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(seed_path),
            "-map",
            "0:v:0",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "bgr24",
            "-vsync",
            "0",
            "-",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _start_review_encoder(seed_path: Path, output_path: Path, width: int, height: int, fps: str):
    ffmpeg = _resolve_binary("ffmpeg")
    return subprocess.Popen(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "bgr24",
            "-s",
            f"{width}x{height}",
            "-r",
            fps,
            "-i",
            "-",
            "-i",
            str(seed_path),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0?",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            "-shortest",
            str(output_path),
        ],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _materialize_seed(
    seed_path: Path,
    rows: list[dict[str, Any]],
    *,
    width: int,
    height: int,
    frame_count: int,
    scale_x: int,
    scale_y: int,
    fps: str,
    expected_event_hashes: list[str] | None = None,
    expected_frame_hashes: list[str] | None = None,
    review_output: Path | None = None,
) -> dict[str, Any]:
    rows_by_frame: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        rows_by_frame.setdefault(int(row["frame_index"]), []).append(row)
    component_count = max((int(row["component_index"]) for row in rows), default=-1) + 1
    state_arrays = [np.zeros((height * width, 3), dtype=np.uint8) for _ in range(component_count)]
    active_indices = [np.empty(0, dtype=np.int64) for _ in range(component_count)]
    event_hashes: list[str] = []
    frame_hashes: list[str] = []
    coverage_counts: list[int] = []
    ablation_passed = False
    decoder = _start_seed_decoder(seed_path)
    encoder = _start_review_encoder(seed_path, review_output, width, height, fps) if review_output else None
    assert decoder.stdout is not None
    if encoder is not None:
        assert encoder.stdin is not None
    frame_bytes = width * height * 3
    try:
        for frame_index in range(frame_count):
            source_frame = np.frombuffer(_read_exact(decoder.stdout, frame_bytes), dtype=np.uint8).reshape((height, width, 3))
            frame_records = rows_by_frame.get(frame_index, [])
            frame_masks: list[tuple[int, np.ndarray]] = []
            frame_values: dict[int, np.ndarray] = {}
            coverage = np.zeros((height, width), dtype=np.uint8)
            for row in frame_records:
                component = int(row["component_index"])
                high_mask = _scaled_mask(row["low_mask"], scale_x, scale_y)
                flat = np.flatnonzero(high_mask.reshape(-1))
                values = np.ascontiguousarray(source_frame[high_mask], dtype=np.uint8)
                expected_count = int(row["owned_pixels"]) * scale_x * scale_y
                if len(flat) != expected_count or len(values) != expected_count:
                    raise ValueError(f"scaled ownership mismatch at event {row['ordinal']}")
                digest = _sha256(values.tobytes())
                event_hashes.append(digest)
                if expected_event_hashes is not None and digest != expected_event_hashes[int(row["ordinal"])]:
                    raise ValueError(f"4K event hash mismatch at event {row['ordinal']}")
                frame_values[int(row["ordinal"])] = values
                previous = active_indices[component]
                if len(previous):
                    state_arrays[component][previous] = 0
                state_arrays[component][flat] = values
                active_indices[component] = flat
                coverage += high_mask.astype(np.uint8)
                frame_masks.append((component, high_mask))
            if int(np.count_nonzero(coverage)) != width * height or int(coverage.max()) != 1:
                raise ValueError(f"scaled masks do not form a partition at frame {frame_index}")
            coverage_counts.append(int(np.count_nonzero(coverage)))
            composed = np.zeros_like(source_frame)
            for component, high_mask in frame_masks:
                composed[high_mask] = state_arrays[component].reshape((height, width, 3))[high_mask]
            frame_digest = _sha256(composed.tobytes())
            frame_hashes.append(frame_digest)
            if expected_frame_hashes is not None and frame_digest != expected_frame_hashes[frame_index]:
                raise ValueError(f"4K frame hash mismatch at frame {frame_index}")
            if frame_index == 0 and frame_records:
                removed = int(frame_records[0]["ordinal"])
                ablated = np.zeros_like(source_frame)
                for row in frame_records:
                    ordinal = int(row["ordinal"])
                    if ordinal != removed:
                        ablated[_scaled_mask(row["low_mask"], scale_x, scale_y)] = frame_values[ordinal]
                ablation_passed = not np.array_equal(composed, ablated)
            if encoder is not None:
                encoder.stdin.write(composed.tobytes())
    finally:
        if encoder is not None:
            encoder.stdin.close()
            stderr = encoder.stderr.read().decode("utf-8", errors="replace") if encoder.stderr else ""
            if encoder.wait() != 0:
                raise RuntimeError(f"materialized review encode failed: {stderr[-4000:]}")
        if decoder.stdout:
            decoder.stdout.close()
        stderr = decoder.stderr.read().decode("utf-8", errors="replace") if decoder.stderr else ""
        if decoder.wait() != 0:
            raise RuntimeError(f"seed decode failed: {stderr[-4000:]}")
    return {
        "event_hashes": event_hashes,
        "frame_hashes": frame_hashes,
        "event_count": len(event_hashes),
        "frame_count": len(frame_hashes),
        "full_frame_coverage": all(value == width * height for value in coverage_counts),
        "min_covered_pixels": min(coverage_counts),
        "max_covered_pixels": max(coverage_counts),
        "event_ablation_passed": ablation_passed,
        "component_compositor_used": True,
        "direct_seed_playback_used": False,
    }


def validate_source_seeded_archive(archive_path: str | Path, output_dir: str | Path, *, render_video: bool = False) -> dict[str, Any]:
    archive_path = Path(archive_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest, contract, graph, mask_member, seed_member, expected_events, expected_frames = _load_archive_members(archive_path)
    width, height = (int(value) for value in manifest["display_dimensions"])
    low_width, low_height = (int(value) for value in manifest["mask_dimensions"])
    scale_x, scale_y = (int(value) for value in manifest["mask_scale"])
    frame_count = int(manifest["frame_count"])
    rows = _decode_mask_rows(graph, mask_member, low_width, low_height)
    with tempfile.TemporaryDirectory(prefix="amcf_seeded_validate_", dir=str(output_dir)) as temp_name:
        temp = Path(temp_name)
        seed_path = temp / "seed.mkv"
        seed_path.write_bytes(seed_member)
        review = output_dir / "seeded_event_materialized_review.mp4" if render_video else None
        result = _materialize_seed(
            seed_path,
            rows,
            width=width,
            height=height,
            frame_count=frame_count,
            scale_x=scale_x,
            scale_y=scale_y,
            fps=str(manifest.get("fps", "24000/1001")),
            expected_event_hashes=expected_events,
            expected_frame_hashes=expected_frames,
            review_output=review,
        )
    report = {
        "ok": bool(
            result["event_hashes"] == expected_events
            and result["frame_hashes"] == expected_frames
            and result["full_frame_coverage"]
            and result["event_ablation_passed"]
        ),
        "archive_path": str(archive_path),
        "archive_bytes": archive_path.stat().st_size,
        "archive_sha256": _sha256_file(archive_path),
        "classification": manifest.get("classification", "AMCF_SOURCE_SEEDED_EVENT_MATERIALIZER"),
        "logical_event_count": result["event_count"],
        "frame_count": result["frame_count"],
        "display_dimensions": [width, height],
        "mask_dimensions": [low_width, low_height],
        "mask_scale": [scale_x, scale_y],
        "source_seed_embedded": bool(manifest.get("source_seed_embedded")),
        "source_video_required_for_decode": bool(manifest.get("source_video_required_for_decode")),
        "direct_seed_playback_used": bool(result["direct_seed_playback_used"]),
        "component_compositor_used": bool(result["component_compositor_used"]),
        "native_component_pixel_payload_present": bool(contract.get("native_4k_component_pixels_stored_independently")),
        "event_hashes_equal": result["event_hashes"] == expected_events,
        "frame_hashes_equal": result["frame_hashes"] == expected_frames,
        "full_frame_coverage": result["full_frame_coverage"],
        "event_ablation_passed": result["event_ablation_passed"],
        "unsafe_acceptance_count": 0 if result["event_hashes"] == expected_events and result["frame_hashes"] == expected_frames else 1,
        "review_video": str(review) if render_video else None,
    }
    (output_dir / "seeded_materializer_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def build_source_seeded_archive(profile_archive: str | Path, canonical_archive: str | Path, output_archive: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Build the compact profile from an embedded 4K seed and canonical masks."""
    profile_archive = Path(profile_archive).resolve()
    canonical_archive = Path(canonical_archive).resolve()
    output_archive = Path(output_archive).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(profile_archive) as source:
        profile_manifest = json.loads(source.read("manifest/manifest.json"))
        graph = source.read("metadata/canonical_event_graph.bin")
        mask_member = source.read("metadata/canonical_masks.bin.bz2")
        seed_member = source.read("payload/perceptual_4k_av1_q32.mkv")
    with zipfile.ZipFile(canonical_archive) as source:
        canonical_manifest = json.loads(source.read("manifest/manifest.json"))
    display_width = int(profile_manifest["source_reference"]["width"])
    display_height = int(profile_manifest["source_reference"]["height"])
    low_width = int(canonical_manifest["source_reference"]["width"])
    low_height = int(canonical_manifest["source_reference"]["height"])
    rows = _decode_mask_rows(graph, mask_member, low_width, low_height)
    scale_x = display_width // low_width
    scale_y = display_height // low_height
    if display_width % low_width or display_height % low_height:
        raise ValueError("4K display dimensions must be an integer scale of the canonical mask dimensions")
    with tempfile.TemporaryDirectory(prefix="amcf_seeded_build_", dir=str(output_dir)) as temp_name:
        seed = Path(temp_name) / "seed.mkv"
        seed.write_bytes(seed_member)
        result = _materialize_seed(
            seed,
            rows,
            width=display_width,
            height=display_height,
            frame_count=int(profile_manifest["source_reference"]["frames"]),
            scale_x=scale_x,
            scale_y=scale_y,
            fps=str(profile_manifest["source_reference"].get("fps", "24000/1001")),
        )
    manifest = {
        "archive_kind": "amcf_4k_source_seeded_event_materializer",
        "format_version": "1.0.0",
        "classification": "AMCF_SOURCE_SEEDED_EVENT_MATERIALIZER",
        "display_dimensions": [display_width, display_height],
        "mask_dimensions": [low_width, low_height],
        "mask_scale": [scale_x, scale_y],
        "logical_event_count": result["event_count"],
        "frame_count": result["frame_count"],
        "fps": str(profile_manifest["source_reference"].get("fps", "24000/1001")),
        "seed_member": "payload/seed_4k_av1_q32.mkv",
        "source_seed_embedded": True,
        "source_video_required_for_decode": False,
        "direct_seed_playback_allowed": False,
        "component_compositor_required": True,
        "native_component_pixel_payload_present": False,
    }
    contract = {
        "all_logical_events_retained": True,
        "direct_component_state_materialization": True,
        "direct_component_compositing": True,
        "no_external_source_required": True,
        "no_direct_seed_playback": True,
        "complete_video_seed_present": True,
        "native_4k_component_pixels_stored_independently": False,
        "canonical_low_resolution_event_graph_retained": True,
        "scale_rule": "nearest_neighbor_integer_mask_block_replication",
    }
    output_archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_archive, "w") as archive:
        _fixed_member(archive, "manifest/manifest.json", json.dumps(manifest, indent=2, sort_keys=True).encode(), deflate=True)
        _fixed_member(archive, "metadata/materialization_contract.json", json.dumps(contract, indent=2, sort_keys=True).encode(), deflate=True)
        _fixed_member(archive, "metadata/profile_manifest.json", json.dumps(profile_manifest, indent=2, sort_keys=True).encode(), deflate=True)
        _fixed_member(archive, "metadata/canonical_manifest.json", json.dumps(canonical_manifest, indent=2, sort_keys=True).encode(), deflate=True)
        _fixed_member(archive, "metadata/canonical_event_graph.bin", graph)
        _fixed_member(archive, "metadata/canonical_masks.bin.bz2", mask_member)
        _fixed_member(archive, "metadata/materialized_4k_event_hashes.bin", b"".join(bytes.fromhex(item) for item in result["event_hashes"]))
        _fixed_member(archive, "metadata/materialized_4k_frame_hashes.bin", b"".join(bytes.fromhex(item) for item in result["frame_hashes"]))
        _fixed_member(archive, "decoder/DECODER_CONTRACT.md", b"Direct seed playback is forbidden. Decode the embedded seed, materialize every event through its mask, then composite the 4K frame. This is source-seeded, not seed-free native-pixel AMCF.\n", deflate=True)
        _fixed_member(archive, "payload/seed_4k_av1_q32.mkv", seed_member)
    report = validate_source_seeded_archive(output_archive, output_dir)
    report["built_archive"] = True
    return report

