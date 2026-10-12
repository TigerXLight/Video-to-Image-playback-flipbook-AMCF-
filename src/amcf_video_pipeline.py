from __future__ import annotations

import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Any

from amcf_digital_encoder import encode_source_frames, sha256_file
from amcf_digital_validator import validate_amcf_archive


def tool_available(name: str) -> bool:
    return shutil.which(name) is not None


def require_tool(name: str) -> None:
    if not tool_available(name):
        raise RuntimeError(f"required media tool not found on PATH: {name}")


def _run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=False)
    if completed.returncode:
        detail = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{detail}")
    return completed


def ffprobe_json(video_path: str | Path, *, ffprobe_bin: str = "ffprobe") -> dict[str, Any]:
    require_tool(ffprobe_bin)
    video_path = Path(video_path)
    completed = _run(
        [
            ffprobe_bin,
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(video_path),
        ]
    )
    return json.loads(completed.stdout or "{}")


def _parse_rate(value: str | None, fallback: int = 24) -> int:
    if not value:
        return fallback
    if "/" in value:
        num, den = value.split("/", 1)
        den_value = float(den)
        if den_value == 0:
            return fallback
        return max(1, int(round(float(num) / den_value)))
    return max(1, int(round(float(value))))


def video_metadata(video_path: str | Path, *, ffprobe_bin: str = "ffprobe") -> dict[str, Any]:
    probe = ffprobe_json(video_path, ffprobe_bin=ffprobe_bin)
    streams = probe.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fps = _parse_rate(str(video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate") or "24/1"))
    frame_count_raw = video_stream.get("nb_frames")
    try:
        frame_count = int(frame_count_raw) if frame_count_raw not in (None, "N/A") else None
    except ValueError:
        frame_count = None
    return {
        "width": int(video_stream.get("width", 0) or 0),
        "height": int(video_stream.get("height", 0) or 0),
        "fps": fps,
        "duration_seconds": float(probe.get("format", {}).get("duration", 0.0) or 0.0),
        "frame_count": frame_count,
        "has_audio": audio_stream is not None,
        "video_codec": video_stream.get("codec_name"),
        "audio_codec": audio_stream.get("codec_name") if audio_stream else None,
        "source_bytes": Path(video_path).stat().st_size,
        "source_sha256": sha256_file(Path(video_path)),
    }


def extract_video_frames(
    video_path: str | Path,
    frames_dir: str | Path,
    *,
    fps: int | None = None,
    max_frames: int | None = None,
    ffmpeg_bin: str = "ffmpeg",
) -> list[Path]:
    require_tool(ffmpeg_bin)
    video_path = Path(video_path)
    frames_dir = Path(frames_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old_frame in frames_dir.glob("frame_*.ppm"):
        old_frame.unlink()
    command = [ffmpeg_bin, "-y", "-hide_banner", "-loglevel", "error", "-i", str(video_path)]
    filters: list[str] = []
    if fps:
        filters.append(f"fps={int(fps)}")
    if filters:
        command += ["-vf", ",".join(filters)]
    if max_frames is not None:
        command += ["-frames:v", str(int(max_frames))]
    command += [str(frames_dir / "frame_%03d.ppm")]
    _run(command)
    return sorted(frames_dir.glob("frame_*.ppm"))


def extract_audio(
    video_path: str | Path,
    audio_path: str | Path,
    *,
    ffmpeg_bin: str = "ffmpeg",
) -> bool:
    require_tool(ffmpeg_bin)
    video_path = Path(video_path)
    audio_path = Path(audio_path)
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    if audio_path.exists():
        audio_path.unlink()
    completed = subprocess.run(
        [ffmpeg_bin, "-y", "-hide_banner", "-loglevel", "error", "-i", str(video_path), "-vn", "-c:a", "copy", str(audio_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode == 0 and audio_path.exists() and audio_path.stat().st_size > 0


def write_source_manifest_from_frames(
    *,
    video_path: str | Path,
    frames: list[Path],
    output_path: str | Path,
    metadata: dict[str, Any],
    audio_path: Path | None = None,
) -> dict[str, Any]:
    if not frames:
        raise ValueError("no frames extracted from source video")
    output_path = Path(output_path)
    frame_root = output_path.parent
    frame_entries: list[dict[str, Any]] = []
    for index, frame in enumerate(frames):
        rel = frame.relative_to(frame_root).as_posix()
        frame_entries.append(
            {
                "frame_index": index,
                "file": rel,
                "width": int(metadata["width"]),
                "height": int(metadata["height"]),
                "format": "ppm_p6",
                "bytes": frame.stat().st_size,
                "sha256": sha256_file(frame),
            }
        )
    manifest: dict[str, Any] = {
        "source_type": "mp4_video_extracted_frames",
        "frame_count": len(frame_entries),
        "width": int(metadata["width"]),
        "height": int(metadata["height"]),
        "fps": int(metadata["fps"]),
        "source_video": {
            "path_name": Path(video_path).name,
            "bytes": int(metadata["source_bytes"]),
            "sha256": metadata["source_sha256"],
            "video_codec": metadata.get("video_codec"),
            "audio_codec": metadata.get("audio_codec"),
            "duration_seconds": metadata.get("duration_seconds"),
        },
        "frame_entries": frame_entries,
    }
    if audio_path is not None and audio_path.exists():
        manifest["audio"] = {
            "file": audio_path.relative_to(frame_root).as_posix(),
            "format": audio_path.suffix.lstrip(".") or "audio",
            "bytes": audio_path.stat().st_size,
            "sha256": sha256_file(audio_path),
        }
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def encode_video_to_amcf(
    video_path: str | Path,
    output_dir: str | Path,
    *,
    fps: int | None = None,
    max_frames: int | None = None,
    include_audio: bool = True,
    ffmpeg_bin: str = "ffmpeg",
    ffprobe_bin: str = "ffprobe",
) -> dict[str, Any]:
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    extraction_dir = output_dir / "extracted_source"
    frames_dir = extraction_dir / "frames"
    audio_dir = extraction_dir / "audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = video_metadata(video_path, ffprobe_bin=ffprobe_bin)
    effective_fps = int(fps or metadata["fps"] or 24)
    metadata["fps"] = effective_fps
    frames = extract_video_frames(video_path, frames_dir, fps=effective_fps, max_frames=max_frames, ffmpeg_bin=ffmpeg_bin)
    audio_path: Path | None = None
    audio_status = "not_requested"
    if include_audio and metadata.get("has_audio"):
        candidate = audio_dir / "source_audio.m4a"
        audio_status = "included" if extract_audio(video_path, candidate, ffmpeg_bin=ffmpeg_bin) else "not_exported"
        if audio_status == "included":
            audio_path = candidate
    elif include_audio:
        audio_status = "source_has_no_audio"
    manifest_path = extraction_dir / "source_frames_manifest.json"
    source_manifest = write_source_manifest_from_frames(
        video_path=video_path,
        frames=frames,
        output_path=manifest_path,
        metadata=metadata,
        audio_path=audio_path,
    )
    archive_path = output_dir / f"{video_path.stem}.amcf.zip"
    encode_summary = encode_source_frames(manifest_path, archive_path)
    validation = validate_amcf_archive(archive_path)
    return {
        "ok": bool(validation["ok"]),
        "source_video": str(video_path),
        "archive_path": str(archive_path),
        "source_manifest_path": str(manifest_path),
        "frame_count": source_manifest["frame_count"],
        "fps": effective_fps,
        "audio_status": audio_status,
        "ffmpeg_used": True,
        "encode_summary": encode_summary,
        "validation": validation,
        "unsafe_acceptance_count": validation.get("unsafe_acceptance_count", 0),
    }


def decode_amcf_to_frames(archive_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    archive_path = Path(archive_path)
    output_dir = Path(output_dir)
    frames_dir = output_dir / "decoded_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old_frame in frames_dir.glob("frame_*.ppm"):
        old_frame.unlink()
    with zipfile.ZipFile(archive_path, "r") as zf:
        manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
        entries = sorted(manifest.get("frame_entries", []), key=lambda item: int(item["frame_index"]))
        decoded_entries: list[dict[str, Any]] = []
        for entry in entries:
            payload = zf.read(entry["payload_path"])
            frame_path = frames_dir / f"frame_{int(entry['frame_index']):03d}.ppm"
            frame_path.write_bytes(payload)
            decoded_entries.append({"frame_index": int(entry["frame_index"]), "file": frame_path.name, "sha256": sha256_file(frame_path)})
        audio_manifest = manifest.get("audio")
        decoded_audio: str | None = None
        if isinstance(audio_manifest, dict) and audio_manifest.get("payload_path"):
            audio_dir = output_dir / "audio"
            audio_dir.mkdir(parents=True, exist_ok=True)
            audio_path = audio_dir / Path(str(audio_manifest["payload_path"])).name
            audio_path.write_bytes(zf.read(audio_manifest["payload_path"]))
            decoded_audio = str(audio_path)
    summary = {
        "ok": True,
        "archive_path": str(archive_path),
        "decoded_frames_dir": str(frames_dir),
        "frame_count": len(decoded_entries),
        "fps": int(manifest.get("fps", 24) or 24),
        "decoded_audio_path": decoded_audio,
        "frames": decoded_entries,
    }
    (output_dir / "decoded_frames_manifest.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def decode_amcf_to_video(
    archive_path: str | Path,
    output_dir: str | Path,
    *,
    output_video_path: str | Path | None = None,
    ffmpeg_bin: str = "ffmpeg",
) -> dict[str, Any]:
    require_tool(ffmpeg_bin)
    output_dir = Path(output_dir)
    frame_summary = decode_amcf_to_frames(archive_path, output_dir)
    video_path = Path(output_video_path) if output_video_path else output_dir / "decoded_from_amcf.mp4"
    command = [
        ffmpeg_bin,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-framerate",
        str(frame_summary["fps"]),
        "-i",
        str(Path(frame_summary["decoded_frames_dir"]) / "frame_%03d.ppm"),
    ]
    if frame_summary.get("decoded_audio_path"):
        command += ["-i", str(frame_summary["decoded_audio_path"]), "-map", "0:v", "-map", "1:a?", "-c:a", "copy"]
    command += ["-c:v", "libx264", "-pix_fmt", "yuv420p", str(video_path)]
    _run(command)
    return {
        "ok": video_path.exists() and video_path.stat().st_size > 0,
        "decoded_video_path": str(video_path),
        "decoded_video_bytes": video_path.stat().st_size if video_path.exists() else 0,
        "frame_count": frame_summary["frame_count"],
        "audio_included": bool(frame_summary.get("decoded_audio_path")),
        "ffmpeg_used": True,
    }
