from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any


REQUIRED_MANIFEST_KEYS = {
    "amcf_schema",
    "source_type",
    "archive_payload_kind",
    "frame_count",
    "width",
    "height",
    "fps",
    "frame_entries",
    "hash_algorithm",
    "created_by",
    "claim_boundary",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_amcf_archive(archive_path: str | Path) -> dict[str, Any]:
    archive_path = Path(archive_path)
    errors: list[str] = []
    warnings: list[str] = []
    manifest: dict[str, Any] = {}
    validated_payloads = 0
    validated_audio_payloads = 0

    if not archive_path.exists():
        return {
            "ok": False,
            "archive_path": str(archive_path),
            "frame_count": 0,
            "validated_payloads": 0,
            "errors": ["archive_missing"],
            "warnings": [],
            "unsafe_acceptance_count": 0,
        }

    try:
        with zipfile.ZipFile(archive_path, "r") as zf:
            names = set(zf.namelist())
            if "manifest.json" not in names:
                errors.append("manifest_missing")
            else:
                manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
                missing_keys = sorted(REQUIRED_MANIFEST_KEYS - set(manifest))
                if missing_keys:
                    errors.append(f"manifest_missing_required_keys:{','.join(missing_keys)}")
                entries = manifest.get("frame_entries", [])
                if not isinstance(entries, list):
                    errors.append("frame_entries_not_list")
                    entries = []
                if int(manifest.get("frame_count", -1)) != len(entries):
                    errors.append("frame_count_mismatch")
                if manifest.get("hash_algorithm") != "sha256":
                    errors.append("unsupported_hash_algorithm")
                boundary = manifest.get("claim_boundary", {})
                for key in (
                    "physical_proof_claimed",
                    "hardware_validation_claimed",
                    "final_ui_claimed",
                    "physical_prototype_built",
                ):
                    if boundary.get(key) is not False:
                        errors.append(f"unsafe_claim_boundary:{key}")
                for entry in entries:
                    payload_path = str(entry.get("payload_path", ""))
                    if not payload_path or payload_path not in names:
                        errors.append(f"missing_payload:{payload_path}")
                        continue
                    payload = zf.read(payload_path)
                    actual_hash = sha256_bytes(payload)
                    if actual_hash != entry.get("sha256"):
                        errors.append(f"hash_mismatch:{payload_path}")
                        continue
                    if len(payload) != int(entry.get("bytes", -1)):
                        errors.append(f"byte_count_mismatch:{payload_path}")
                        continue
                    validated_payloads += 1
                audio = manifest.get("audio")
                if isinstance(audio, dict) and audio.get("payload_path"):
                    audio_path = str(audio.get("payload_path", ""))
                    if audio_path not in names:
                        errors.append(f"missing_audio_payload:{audio_path}")
                    else:
                        payload = zf.read(audio_path)
                        if sha256_bytes(payload) != audio.get("sha256"):
                            errors.append(f"audio_hash_mismatch:{audio_path}")
                        elif len(payload) != int(audio.get("bytes", -1)):
                            errors.append(f"audio_byte_count_mismatch:{audio_path}")
                        else:
                            validated_audio_payloads += 1
    except zipfile.BadZipFile:
        errors.append("bad_zip_file")
    except json.JSONDecodeError as exc:
        errors.append(f"manifest_json_decode_error:{exc}")

    ok = not errors
    return {
        "ok": ok,
        "archive_path": str(archive_path),
        "amcf_schema": manifest.get("amcf_schema"),
        "frame_count": int(manifest.get("frame_count", 0) or 0),
        "validated_payloads": validated_payloads,
        "validated_audio_payloads": validated_audio_payloads,
        "errors": errors,
        "warnings": warnings,
        "unsafe_acceptance_count": 0,
        "claim_boundary": manifest.get("claim_boundary", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a minimal AMCF digital archive.")
    parser.add_argument("archive")
    args = parser.parse_args()
    result = validate_amcf_archive(args.archive)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
