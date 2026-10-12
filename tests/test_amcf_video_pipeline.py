from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


THIS = Path(__file__).resolve()
PACKAGE = THIS.parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from amcf_digital_validator import validate_amcf_archive  # noqa: E402
from amcf_video_pipeline import decode_amcf_to_frames, decode_amcf_to_video, encode_video_to_amcf, require_tool, tool_available  # noqa: E402


def make_sample_video(path: Path) -> None:
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=80x60:rate=4:duration=1",
        "-f",
        "lavfi",
        "-i",
        "sine=frequency=330:duration=1",
        "-shortest",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        str(path),
    ]
    completed = subprocess.run(command, check=False, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(completed.stderr or completed.stdout)


@unittest.skipUnless(tool_available("ffmpeg") and tool_available("ffprobe"), "ffmpeg/ffprobe not available")
class AmcfVideoPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_video_pipeline_"))
        self.video = self.tmp / "input.mp4"
        make_sample_video(self.video)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_encode_video_to_amcf_creates_archive(self) -> None:
        result = encode_video_to_amcf(self.video, self.tmp / "encoded", fps=4, max_frames=4)
        self.assertTrue(result["ok"], result)
        archive = Path(result["archive_path"])
        self.assertTrue(archive.exists())
        self.assertEqual(result["frame_count"], 4)
        self.assertEqual(result["audio_status"], "included")

    def test_video_archive_validates_audio_and_frames(self) -> None:
        result = encode_video_to_amcf(self.video, self.tmp / "encoded", fps=4, max_frames=4)
        validation = validate_amcf_archive(result["archive_path"])
        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(validation["validated_payloads"], 4)
        self.assertEqual(validation["validated_audio_payloads"], 1)
        self.assertEqual(validation["unsafe_acceptance_count"], 0)

    def test_manifest_marks_video_adapter_without_hardware_claims(self) -> None:
        result = encode_video_to_amcf(self.video, self.tmp / "encoded", fps=4, max_frames=4)
        with zipfile.ZipFile(result["archive_path"], "r") as zf:
            manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
        self.assertEqual(manifest["source_type"], "mp4_video_extracted_frames")
        self.assertTrue(manifest["capabilities"]["mp4_video_input_adapter_used"])
        self.assertTrue(manifest["capabilities"]["audio_payload_included"])
        boundary = manifest["claim_boundary"]
        self.assertFalse(boundary["hardware_validation_claimed"])
        self.assertFalse(boundary["physical_proof_claimed"])
        self.assertFalse(boundary["physical_prototype_built"])
        self.assertFalse(boundary["decoded_video_export_claimed"])

    def test_decode_amcf_to_frames_exports_frames(self) -> None:
        result = encode_video_to_amcf(self.video, self.tmp / "encoded", fps=4, max_frames=4)
        decoded = decode_amcf_to_frames(result["archive_path"], self.tmp / "decoded_frames")
        self.assertTrue(decoded["ok"])
        self.assertEqual(decoded["frame_count"], 4)
        self.assertEqual(len(list(Path(decoded["decoded_frames_dir"]).glob("*.ppm"))), 4)

    def test_decode_amcf_to_video_exports_mp4(self) -> None:
        result = encode_video_to_amcf(self.video, self.tmp / "encoded", fps=4, max_frames=4)
        decoded = decode_amcf_to_video(result["archive_path"], self.tmp / "decoded_video")
        self.assertTrue(decoded["ok"], decoded)
        self.assertTrue(Path(decoded["decoded_video_path"]).exists())
        self.assertGreater(decoded["decoded_video_bytes"], 0)
        self.assertTrue(decoded["audio_included"])


class AmcfVideoPipelineDependencyTests(unittest.TestCase):
    def test_missing_tool_reports_clear_error(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "required media tool not found"):
            require_tool("__definitely_missing_amcf_tool__")


if __name__ == "__main__":
    unittest.main(verbosity=2)
