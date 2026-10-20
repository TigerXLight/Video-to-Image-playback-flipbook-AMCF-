from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_v2.container.archive_reader import ArchiveReader  # noqa: E402
from amcf_v2.container.index_loader import IndexLoader  # noqa: E402
from amcf_v2.container.manifest_loader import ManifestLoader  # noqa: E402
from amcf_v2.playback.frame_cache import FrameCache  # noqa: E402
from amcf_v2.playback.seek_controller import SeekController  # noqa: E402


RUN_NAME = "AMCF_V2_PUBLIC_PACKAGE_DEMO_V1"


def build_demo_archive(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "manifest/native_manifest.json",
            json.dumps(
                {
                    "amcf_version": "amcf-v2-public-demo",
                    "variant_id": "public-v2-demo",
                    "codec_strategy": "webp_lossless_frames",
                    "payload_included": True,
                    "frame_count": 3,
                    "width": 2,
                    "height": 2,
                    "exact_lossy_flag": False,
                }
            ),
        )
        zf.writestr(
            "manifest/residual_manifest.json",
            json.dumps({"variant_id": "public-v2-demo", "codec_strategy": "webp_lossless_frames", "payload_included": True}),
        )
        zf.writestr("indexes/seek_index.json", json.dumps({"frames": [{"frame_index": i, "payload_entry": f"payload/frame_{i:03d}.webp"} for i in range(3)]}))
        zf.writestr("indexes/decode_plan.json", json.dumps({"frames": [{"frame_index": i, "payload_entry": f"payload/frame_{i:03d}.webp"} for i in range(3)]}))
        zf.writestr("indexes/frame_dependency_graph.json", json.dumps({"frames": [{"frame_index": i, "dependencies": [f"payload/frame_{i:03d}.webp"]} for i in range(3)]}))
        for index in range(3):
            zf.writestr(f"payload/frame_{index:03d}.webp", f"synthetic-payload-{index}".encode("utf-8"))


def run_demo(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / "synthetic_v2_archive.amcfv2.zip"
    build_demo_archive(archive)
    with ArchiveReader(str(archive)) as reader:
        manifest_summary = ManifestLoader(reader).summarize_manifest()
        index_summary = IndexLoader(reader).summarize_indexes()
    seek = SeekController([0, 1, 2])
    cache = FrameCache(max_items=2)
    cache.put(0, "frame-zero")
    cache.put(1, "frame-one")
    cache.put(2, "frame-two")
    report = {
        "run_name": RUN_NAME,
        "archive_path": str(archive),
        "archive_entries_checked": True,
        "manifest_summary": manifest_summary,
        "index_summary": index_summary,
        "seek_middle": seek.seek_middle(),
        "cache_stats": cache.stats(),
        "unsafe_acceptance_count": 0,
        "hardware_validation_claimed": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "final_passed": manifest_summary["payload_included"] and not index_summary["missing_referenced_entries"],
    }
    (output_dir / "amcf_v2_public_package_demo_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> int:
    report = run_demo(REPO_ROOT / "output" / "amcf_v2_public_package_demo")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
