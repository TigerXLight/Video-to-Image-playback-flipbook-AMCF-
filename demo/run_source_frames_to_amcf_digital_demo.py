from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_digital_encoder import encode_source_frames  # noqa: E402
from amcf_digital_validator import validate_amcf_archive  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


def main() -> None:
    out = PACKAGE / "demo" / "output" / "source_to_amcf"
    frames_root = out / "generated_source_frames"
    if out.exists():
        shutil.rmtree(out)
    frames_root.mkdir(parents=True, exist_ok=True)

    source_manifest = generate_source_frames(frames_root)
    source_manifest_path = frames_root / "source_frames_manifest.json"
    archive_path = out / "sample_video_source.amcf.zip"
    encode_summary = encode_source_frames(source_manifest_path, archive_path)
    validation = validate_amcf_archive(archive_path)

    summary_manifest_path = out / "sample_source_frames_manifest.json"
    summary_manifest_path.write_text(json.dumps(source_manifest, indent=2, sort_keys=True), encoding="utf-8")
    validation_path = out / "sample_video_source_validation.json"
    validation_path.write_text(json.dumps(validation, indent=2, sort_keys=True), encoding="utf-8")

    result_lines = [
        "# Source Frames to AMCF Digital Demo Result",
        "",
        f"- actual AMCF archive created: {'yes' if archive_path.exists() else 'no'}",
        f"- archive: `{archive_path.relative_to(PACKAGE).as_posix()}`",
        f"- frame count: {validation.get('frame_count', 0)}",
        f"- validation pass: {'yes' if validation.get('ok') else 'no'}",
        f"- validated payloads: {validation.get('validated_payloads', 0)}",
        f"- unsafe acceptance count: {validation.get('unsafe_acceptance_count', 0)}",
        f"- physical proof claimed: no",
        f"- hardware validation claimed: no",
        f"- final UI claimed: no",
        f"- arbitrary real video support claimed: no",
        "",
        "This is a standard-library smoke demo for generated source frames. It creates an actual AMCF digital archive and validates payload integrity, but it does not claim arbitrary video ingestion.",
    ]
    result_path = out / "SOURCE_TO_AMCF_DEMO_RESULT.md"
    result_path.write_text("\n".join(result_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "ok": bool(validation.get("ok")),
        "archive_created": archive_path.exists(),
        "archive_path": str(archive_path),
        "frame_count": validation.get("frame_count", 0),
        "validated_payloads": validation.get("validated_payloads", 0),
        "unsafe_acceptance_count": validation.get("unsafe_acceptance_count", 0),
        "encode_summary": encode_summary,
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if validation.get("ok") and archive_path.exists() else 1)


if __name__ == "__main__":
    main()
