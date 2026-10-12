from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amcf_video_pipeline import decode_amcf_to_frames, decode_amcf_to_video, encode_video_to_amcf, tool_available  # noqa: E402


OUTPUT = ROOT / "output" / "amcf_video_pipeline_demo"


def make_sample_video(path: Path) -> bool:
    if not tool_available("ffmpeg"):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=96x64:rate=4:duration=1",
        "-f",
        "lavfi",
        "-i",
        "sine=frequency=440:duration=1",
        "-shortest",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        str(path),
    ]
    return subprocess.run(command, check=False).returncode == 0 and path.exists()


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sample_video = OUTPUT / "sample_input.mp4"
    if not make_sample_video(sample_video):
        result = {
            "ok": False,
            "reason": "ffmpeg_unavailable_or_sample_video_generation_failed",
            "hardware_validation_claimed": False,
            "manufactured_player_claimed": False,
            "physical_level_5_claimed": False,
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2

    encode = encode_video_to_amcf(sample_video, OUTPUT / "encoded_amcf", fps=4, max_frames=4, include_audio=True)
    frames = decode_amcf_to_frames(encode["archive_path"], OUTPUT / "decoded_frames")
    video = decode_amcf_to_video(encode["archive_path"], OUTPUT / "decoded_video")
    result = {
        "ok": bool(encode["ok"] and frames["ok"] and video["ok"]),
        "source_video": str(sample_video),
        "archive_path": encode["archive_path"],
        "frame_count": encode["frame_count"],
        "audio_status": encode["audio_status"],
        "decoded_frames_dir": frames["decoded_frames_dir"],
        "decoded_video_path": video["decoded_video_path"],
        "mp4_to_amcf_supported_when_ffmpeg_available": True,
        "decoded_mp4_export_supported_when_ffmpeg_available": True,
        "unsafe_acceptance_count": encode["unsafe_acceptance_count"],
        "hardware_validation_claimed": False,
        "manufactured_player_claimed": False,
        "physical_level_5_claimed": False,
    }
    (OUTPUT / "video_pipeline_demo_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
