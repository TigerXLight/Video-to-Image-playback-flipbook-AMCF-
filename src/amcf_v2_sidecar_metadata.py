from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path
from typing import Any


AMCF_V2_SIDECAR_SCHEMA = "amcf-v2-webp-demo-component-sidecar-v1"
FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)

REQUIRED_ENTRIES = (
    "manifest/native_manifest_14J.json",
    "manifest/payload_manifest_14J.json",
    "manifest/component_metadata_sidecar_14J.json",
    "manifest/region_table_14J.csv",
    "indexes/seek_index_14J.json",
)

SAFE_CLAIM_FLAGS = {
    "hardware_validation_claimed": False,
    "physical_level_5_claimed": False,
    "manufactured_player_claimed": False,
    "full_native_playback_solved": False,
    "final_playback_engine_solved": False,
    "custom_component_codec_solved": False,
    "proxy_regions_are_semantic_objects": False,
    "motion_vectors_are_object_tracking": False,
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_zip_member(zf: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, payload)


def _json_bytes(data: Any) -> bytes:
    return json.dumps(data, indent=2, sort_keys=True).encode("utf-8")


def _csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue().encode("utf-8")


def build_demo_sidecar_archive(archive_path: str | Path, *, frame_count: int = 4) -> dict[str, Any]:
    """Build a small deterministic 14J-style sidecar archive for tests and demos.

    The payload bytes are placeholders. This function validates the metadata
    contract and sidecar reader behavior; it does not claim WebP decoding or
    full native playback.
    """
    if frame_count < 1:
        raise ValueError("frame_count must be positive")
    archive_path = Path(archive_path)
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    payload_manifest: list[dict[str, Any]] = []
    seek_frames: list[dict[str, Any]] = []
    regions: list[dict[str, Any]] = []
    region_rows: list[dict[str, Any]] = []
    payloads: dict[str, bytes] = {}

    for index in range(frame_count):
        payload_path = f"payload/frame_{index:03d}.webp"
        payload = f"synthetic-webp-demo-payload-{index}".encode("utf-8")
        payloads[payload_path] = payload
        payload_manifest.append(
            {
                "frame_id": index,
                "payload_path": payload_path,
                "codec_strategy": "webp_lossless_frames",
                "payload_sha256": sha256_bytes(payload),
                "metadata_sidecar_required": True,
            }
        )
        seek_frames.append({"frame_id": index, "payload_entry": payload_path, "sidecar_required": True})
        region_id = "proxy_region_a" if index < max(2, frame_count - 1) else "proxy_region_b"
        bbox = [index, index % 2, 2, 2]
        regions.append(
            {
                "frame_id": index,
                "proxy_region_id": region_id,
                "track_id": region_id,
                "bbox": bbox,
                "update_reason": "keyframe" if index == 0 else "changed_region",
                "is_semantic_object": False,
            }
        )
        region_rows.append(
            {
                "frame_id": index,
                "proxy_region_id": region_id,
                "x": bbox[0],
                "y": bbox[1],
                "w": bbox[2],
                "h": bbox[3],
                "update_reason": "keyframe" if index == 0 else "changed_region",
            }
        )

    native_manifest = {
        "schema": AMCF_V2_SIDECAR_SCHEMA,
        "variant_id": "public-14j-sidecar-demo",
        "codec_strategy": "webp_lossless_frames",
        "frame_count": frame_count,
        "component_metadata_sidecar": True,
        "payload_included": True,
        "claim_flags": dict(SAFE_CLAIM_FLAGS),
    }
    sidecar = {
        "schema": AMCF_V2_SIDECAR_SCHEMA,
        "description": "Component metadata sidecar for WebP demo payload archives.",
        "regions": regions,
        "claim_flags": dict(SAFE_CLAIM_FLAGS),
        "unsafe_acceptance_count": 0,
    }

    with zipfile.ZipFile(archive_path, "w") as zf:
        _write_zip_member(zf, "manifest/native_manifest_14J.json", _json_bytes(native_manifest))
        _write_zip_member(zf, "manifest/payload_manifest_14J.json", _json_bytes(payload_manifest))
        _write_zip_member(zf, "manifest/component_metadata_sidecar_14J.json", _json_bytes(sidecar))
        _write_zip_member(zf, "manifest/region_table_14J.csv", _csv_bytes(region_rows))
        _write_zip_member(zf, "indexes/seek_index_14J.json", _json_bytes({"frames": seek_frames}))
        for payload_path, payload in payloads.items():
            _write_zip_member(zf, payload_path, payload)

    report = validate_sidecar_archive(archive_path)
    report["archive_path"] = str(archive_path)
    return report


class V2SidecarArchiveReader:
    """Read the public-safe subset of the accepted 14J sidecar archive shape."""

    def __init__(self, archive_path: str | Path):
        self.archive_path = Path(archive_path)
        self._zip: zipfile.ZipFile | None = None

    def __enter__(self) -> "V2SidecarArchiveReader":
        self.open()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def open(self) -> "V2SidecarArchiveReader":
        self._zip = zipfile.ZipFile(self.archive_path, "r")
        return self

    def close(self) -> None:
        if self._zip is not None:
            self._zip.close()
            self._zip = None

    def entries(self) -> list[str]:
        if self._zip is None:
            raise RuntimeError("archive not open")
        return sorted(self._zip.namelist())

    def missing_required_entries(self) -> list[str]:
        available = set(self.entries())
        return [entry for entry in REQUIRED_ENTRIES if entry not in available]

    def _json(self, entry: str) -> Any:
        if self._zip is None:
            raise RuntimeError("archive not open")
        try:
            return json.loads(self._zip.read(entry).decode("utf-8"))
        except KeyError as exc:
            raise RuntimeError(f"required entry missing: {entry}") from exc

    def native_manifest(self) -> dict[str, Any]:
        return self._json("manifest/native_manifest_14J.json")

    def payload_manifest(self) -> list[dict[str, Any]]:
        payload = self._json("manifest/payload_manifest_14J.json")
        if not isinstance(payload, list):
            raise RuntimeError("payload manifest must be a list")
        return payload

    def sidecar(self) -> dict[str, Any]:
        return self._json("manifest/component_metadata_sidecar_14J.json")

    def seek_index(self) -> dict[str, Any]:
        return self._json("indexes/seek_index_14J.json")

    def region_table(self) -> list[dict[str, str]]:
        if self._zip is None:
            raise RuntimeError("archive not open")
        try:
            text = self._zip.read("manifest/region_table_14J.csv").decode("utf-8")
        except KeyError as exc:
            raise RuntimeError("required entry missing: manifest/region_table_14J.csv") from exc
        return list(csv.DictReader(io.StringIO(text)))

    def list_frames(self) -> list[int]:
        return [int(row["frame_id"]) for row in self.payload_manifest()]

    def regions_for_frame(self, frame_id: int) -> list[dict[str, Any]]:
        return [row for row in self.sidecar().get("regions", []) if int(row.get("frame_id", -1)) == int(frame_id)]

    def proxy_region_lifespan(self) -> dict[str, dict[str, int]]:
        spans: dict[str, list[int]] = {}
        for region in self.sidecar().get("regions", []):
            spans.setdefault(str(region["proxy_region_id"]), []).append(int(region["frame_id"]))
        return {
            region_id: {"first": min(frames), "last": max(frames), "count": len(frames)}
            for region_id, frames in sorted(spans.items())
        }

    def verify_claim_flags_false(self) -> bool:
        sidecar_flags = self.sidecar().get("claim_flags", {})
        manifest_flags = self.native_manifest().get("claim_flags", {})
        flags = {**manifest_flags, **sidecar_flags}
        return bool(flags) and all(value is False for value in flags.values())

    def payload_hashes_match(self) -> bool:
        if self._zip is None:
            raise RuntimeError("archive not open")
        for row in self.payload_manifest():
            expected = str(row.get("payload_sha256", ""))
            payload_path = str(row.get("payload_path", ""))
            if sha256_bytes(self._zip.read(payload_path)) != expected:
                return False
        return True

    def summarize(self) -> dict[str, Any]:
        missing = self.missing_required_entries()
        sidecar = self.sidecar() if not missing else {}
        frames = self.list_frames() if not missing else []
        lifespans = self.proxy_region_lifespan() if not missing else {}
        claim_flags_false = self.verify_claim_flags_false() if not missing else False
        unsafe_acceptance_count = int(sidecar.get("unsafe_acceptance_count", 1))
        return {
            "schema": sidecar.get("schema"),
            "archive_path": str(self.archive_path),
            "required_entries_present": not missing,
            "missing_required_entries": missing,
            "frame_count": len(frames),
            "frames": frames,
            "proxy_region_count": len(lifespans),
            "proxy_region_lifespan": lifespans,
            "region_table_rows": len(self.region_table()) if not missing else 0,
            "claim_flags_false": claim_flags_false,
            "unsafe_acceptance_count": unsafe_acceptance_count,
            "payload_hashes_match": self.payload_hashes_match() if not missing else False,
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "final_passed": (
                not missing
                and claim_flags_false
                and unsafe_acceptance_count == 0
                and self.payload_hashes_match()
            ),
        }


def validate_sidecar_archive(archive_path: str | Path) -> dict[str, Any]:
    with V2SidecarArchiveReader(archive_path) as reader:
        return reader.summarize()
