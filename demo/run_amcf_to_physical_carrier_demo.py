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
from generate_sample_source_frames import generate_source_frames  # noqa: E402


def main() -> None:
    out = PACKAGE / "demo" / "output" / "amcf_to_physical_carrier"
    frames_root = out / "generated_source_frames"
    carrier_root = out
    if out.exists():
        shutil.rmtree(out)
    frames_root.mkdir(parents=True, exist_ok=True)

    source_manifest = generate_source_frames(frames_root)
    source_manifest_path = frames_root / "source_frames_manifest.json"
    archive_path = out / "sample_video_source.amcf.zip"
    encode_source_frames(source_manifest_path, archive_path)
    amcf_validation = validate_amcf_archive(archive_path)
    carrier_generation = generate_physical_carrier_from_amcf_archive(archive_path, carrier_root)
    carrier_validation = validate_physical_carrier_package(carrier_root)

    (out / "physical_carrier_validation.json").write_text(json.dumps(carrier_validation, indent=2, sort_keys=True), encoding="utf-8")
    result_lines = [
        "# AMCF Digital to Physical Carrier Demo Result",
        "",
        f"- AMCF archive created: {'yes' if archive_path.exists() else 'no'}",
        f"- AMCF archive validation pass: {'yes' if amcf_validation.get('ok') else 'no'}",
        f"- physical carrier package created: {'yes' if (out / 'physical_carrier_manifest.json').exists() else 'no'}",
        f"- section count: {carrier_validation.get('section_count', 0)}",
        f"- lane layout present: {'yes' if carrier_validation.get('lane_layout_present') else 'no'}",
        f"- validation pass: {'yes' if carrier_validation.get('ok') else 'no'}",
        f"- unsafe acceptance count: {carrier_validation.get('unsafe_acceptance_count', 0)}",
        f"- physical proof claimed: no",
        f"- hardware validation claimed: no",
        f"- real printing performed: no",
        f"- final UI claimed: no",
        "",
        "This is a software-generated indexed physical-carrier output package. It is not real printing, manufacturing readiness, hardware validation, or physical proof.",
    ]
    (out / "AMCF_TO_PHYSICAL_CARRIER_DEMO_RESULT.md").write_text("\n".join(result_lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "ok": bool(amcf_validation.get("ok") and carrier_validation.get("ok")),
        "amcf_archive_created": archive_path.exists(),
        "physical_carrier_package_created": (out / "physical_carrier_manifest.json").exists(),
        "section_count": carrier_validation.get("section_count", 0),
        "lane_layout_present": carrier_validation.get("lane_layout_present", False),
        "unsafe_acceptance_count": carrier_validation.get("unsafe_acceptance_count", 0),
        "carrier_generation": carrier_generation,
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if amcf_validation.get("ok") and carrier_validation.get("ok") else 1)


if __name__ == "__main__":
    main()
