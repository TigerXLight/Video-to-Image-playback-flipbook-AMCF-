from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_v2.codecs.registry import PayloadCodecRegistry  # noqa: E402
from amcf_v2.codecs.webp_lossless import WebPLosslessPayloadCodec  # noqa: E402
from amcf_v2.container.archive_reader import ArchiveReader  # noqa: E402
from amcf_v2.container.index_loader import IndexLoader  # noqa: E402
from amcf_v2.container.manifest_loader import ManifestLoader  # noqa: E402
from amcf_v2.decode.checksum import ChecksumVerifier  # noqa: E402
from amcf_v2.playback.frame_cache import FrameCache  # noqa: E402
from amcf_v2.playback.playback_loop import PlaybackClock, PlaybackLoop  # noqa: E402
from amcf_v2.playback.seek_controller import SeekController  # noqa: E402


def build_synthetic_v2_archive(path: Path) -> None:
    native_manifest = {
        "amcf_version": "amcf-v2-synthetic",
        "variant_id": "public-test",
        "codec_strategy": "webp_lossless_frames",
        "payload_included": True,
        "frame_count": 2,
        "width": 2,
        "height": 2,
        "exact_lossy_flag": False,
    }
    residual_manifest = {
        "variant_id": "public-test",
        "codec_strategy": "webp_lossless_frames",
        "payload_included": True,
    }
    seek_index = {"frames": [{"frame_index": 0, "payload_entry": "payload/frame_000.webp"}]}
    decode_plan = {"frames": [{"frame_index": 0, "payload_entry": "payload/frame_000.webp"}]}
    dependency_graph = {"frames": [{"frame_index": 0, "dependencies": ["payload/frame_000.webp"]}]}
    payload = b"synthetic-webp-placeholder"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest/native_manifest.json", json.dumps(native_manifest))
        zf.writestr("manifest/residual_manifest.json", json.dumps(residual_manifest))
        zf.writestr("indexes/seek_index.json", json.dumps(seek_index))
        zf.writestr("indexes/decode_plan.json", json.dumps(decode_plan))
        zf.writestr("indexes/frame_dependency_graph.json", json.dumps(dependency_graph))
        zf.writestr("payload/frame_000.webp", payload)


class AmcfV2PublicPackageTests(unittest.TestCase):
    def test_archive_reader_manifest_and_index_loaders(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "synthetic.amcfv2.zip"
            build_synthetic_v2_archive(archive)
            with ArchiveReader(str(archive)) as reader:
                self.assertTrue(reader.has_entry("manifest/native_manifest.json"))
                self.assertEqual(reader.read_json("manifest/native_manifest.json")["frame_count"], 2)
                self.assertEqual(reader.entry_info("payload/frame_000.webp")["path"], "payload/frame_000.webp")
                self.assertEqual(
                    reader.sha256_entry("payload/frame_000.webp"),
                    ChecksumVerifier().sha256_bytes(b"synthetic-webp-placeholder"),
                )
                manifest_summary = ManifestLoader(reader).summarize_manifest()
                index_summary = IndexLoader(reader).summarize_indexes()
        self.assertEqual(manifest_summary["variant_id"], "public-test")
        self.assertTrue(manifest_summary["payload_included"])
        self.assertEqual(index_summary["missing_referenced_entries"], [])
        self.assertIn("payload/frame_000.webp", index_summary["referenced_payload_paths"])

    def test_codec_registry_is_fail_closed_for_unsupported_payloads(self) -> None:
        registry = PayloadCodecRegistry()
        registry.register(WebPLosslessPayloadCodec())
        with self.assertRaises(LookupError):
            registry.choose_decoder({"codec_strategy": "unsupported-local-codec", "extension": ".bin"})

    def test_bounded_cache_and_seek_controller(self) -> None:
        cache = FrameCache(max_items=2)
        cache.put(1, "frame-one")
        cache.put(2, "frame-two")
        self.assertEqual(cache.get(1), "frame-one")
        cache.put(3, "frame-three")
        self.assertFalse(cache.has(2))
        self.assertEqual(cache.stats()["items"], 2)

        seek = SeekController([10, 20, 30])
        self.assertEqual(seek.seek_middle(), 20)
        with self.assertRaises(ValueError):
            seek.seek(99)

    def test_playback_clock_and_loop_are_deterministic(self) -> None:
        clock = PlaybackClock(source_fps=24)
        self.assertAlmostEqual(clock.timestamp_for(12), 0.5)
        loop = PlaybackLoop([0, 1, 2], clock=clock)
        self.assertFalse(loop.paused)
        loop.pause()
        self.assertTrue(loop.paused)
        loop.resume()
        self.assertFalse(loop.paused)


if __name__ == "__main__":
    unittest.main(verbosity=2)
