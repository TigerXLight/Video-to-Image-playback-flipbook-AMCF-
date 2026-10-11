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
from amcf_physical_carrier import (  # noqa: E402
    generate_physical_carrier_from_amcf_archive,
    validate_physical_carrier_package,
)
from amcf_virtual_carrier_reader import (  # noqa: E402
    read_physical_carrier_package,
    recover_amcf_from_carrier_package,
    validate_recovered_amcf_state,
)
from generate_sample_source_frames import generate_source_frames  # noqa: E402


def main() -> None:
    out = PACKAGE / "demo" / "output" / "virtual_reader_recovery"
    frames_root = out / "generated_source_frames"
    if out.exists():
        shutil.rmtree(out)
    frames_root.mkdir(parents=True, exist_ok=True)

    source_manifest = generate_source_frames(frames_root)
    source_manifest_path = frames_root / "source_frames_manifest.json"
    archive_path = out / "sample_video_source.amcf.zip"
    encode_source_frames(source_manifest_path, archive_path)
    amcf_validation = validate_amcf_archive(archive_path)
    generate_physical_carrier_from_amcf_archive(archive_path, out)
    carrier_validation = validate_physical_carrier_package(out)
    read_result = read_physical_carrier_package(out)
    recovery = recover_amcf_from_carrier_package(out, out, archive_path)
    recovered_validation = validate_recovered_amcf_state(out / "recovered_amcf_manifest.json")

    (out / "source_frames_manifest.json").write_text(json.dumps(source_manifest, indent=2, sort_keys=True), encoding="utf-8")
    (out / "recovered_validation.json").write_text(json.dumps(recovered_validation, indent=2, sort_keys=True), encoding="utf-8")
    result_lines = [
        "# Virtual Reader Recovery Export Demo Result",
        "",
        f"- source AMCF archive created: {'yes' if archive_path.exists() else 'no'}",
        f"- source AMCF archive validation pass: {'yes' if amcf_validation.get('ok') else 'no'}",
        f"- physical carrier package created: {'yes' if (out / 'physical_carrier_manifest.json').exists() else 'no'}",
        f"- physical carrier package validation pass: {'yes' if carrier_validation.get('ok') else 'no'}",
        f"- virtual reader read sections: {'yes' if read_result.ok else 'no'}",
        f"- recovered AMCF state created: {'yes' if (out / 'recovered_amcf_manifest.json').exists() else 'no'}",
        f"- recovered frame export created: {'yes' if (out / 'recovered_frames').exists() else 'no'}",
        f"- recovered frame count: {recovered_validation.get('recovered_frame_count', 0)}",
        f"- validation pass: {'yes' if recovered_validation.get('ok') else 'no'}",
        f"- unsafe acceptance count: {recovered_validation.get('unsafe_acceptance_count', 0)}",
        f"- real scanner used: no",
        f"- physical proof claimed: no",
        f"- hardware validation claimed: no",
        f"- MP4/video-container export claimed: no",
        "",
        "This is a virtual reader/recovery demo over software-generated carrier sections. It exports recovered PPM frame payloads and a recovered AMCF state manifest; it does not use real scanner hardware.",
    ]
    (out / "VIRTUAL_READER_RECOVERY_EXPORT_DEMO_RESULT.md").write_text("\n".join(result_lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "ok": bool(amcf_validation.get("ok") and carrier_validation.get("ok") and read_result.ok and recovery.get("ok") and recovered_validation.get("ok")),
        "source_amcf_archive_created": archive_path.exists(),
        "physical_carrier_package_created": (out / "physical_carrier_manifest.json").exists(),
        "virtual_reader_read_sections": read_result.ok,
        "recovered_amcf_state_created": (out / "recovered_amcf_manifest.json").exists(),
        "recovered_frame_export_created": (out / "recovered_frames").exists(),
        "recovered_frame_count": recovered_validation.get("recovered_frame_count", 0),
        "unsafe_acceptance_count": recovered_validation.get("unsafe_acceptance_count", 0),
        "mp4_video_container_export_claimed": False,
        "recovery": recovery,
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if amcf_validation.get("ok") and carrier_validation.get("ok") and read_result.ok and recovery.get("ok") and recovered_validation.get("ok") else 1)


if __name__ == "__main__":
    main()
