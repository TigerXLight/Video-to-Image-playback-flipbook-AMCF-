from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from typing import Any


def build_component_event_viewer(
    *,
    archive_report: dict[str, Any],
    decoded_report: dict[str, Any],
    quality_report: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Any]:
    output_dir = Path(output_dir)
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    decoded_frames_dir = Path(str(decoded_report["decoded_frames_dir"]))
    copied_frames: list[dict[str, Any]] = []
    for frame_path in sorted(decoded_frames_dir.glob("frame_*.ppm")):
        target = frames_dir / frame_path.name
        shutil.copy2(frame_path, target)
        copied_frames.append({"file": f"frames/{target.name}", "bytes": target.stat().st_size})

    viewer_manifest = {
        "schema": "amcf-component-event-viewer-v1",
        "archive_path_name": Path(str(archive_report["archive_path"])).name,
        "frame_count": int(decoded_report["frame_count"]),
        "event_count": int(decoded_report["event_count"]),
        "frames": copied_frames,
        "quality": {
            "mean_absolute_error": quality_report.get("mean_absolute_error"),
            "mean_ssim": quality_report.get("mean_ssim"),
            "ssim_available": quality_report.get("ssim_available", False),
        },
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "viewer_is_final_ui": False,
        },
        "unsafe_acceptance_count": int(decoded_report.get("unsafe_acceptance_count", 0)),
    }
    manifest_path = output_dir / "viewer_manifest.json"
    manifest_path.write_text(json.dumps(viewer_manifest, indent=2, sort_keys=True), encoding="utf-8")
    html_path = output_dir / "index.html"
    html_path.write_text(_viewer_html(viewer_manifest), encoding="utf-8")
    return {
        "ok": True,
        "viewer_dir": str(output_dir),
        "viewer_manifest": str(manifest_path),
        "viewer_html": str(html_path),
        "frame_count": len(copied_frames),
        "claim_boundary": viewer_manifest["claim_boundary"],
        "unsafe_acceptance_count": viewer_manifest["unsafe_acceptance_count"],
    }


def _viewer_html(manifest: dict[str, Any]) -> str:
    frame_items = "\n".join(
        f'<li><code>{html.escape(frame["file"])}</code> ({int(frame["bytes"])} bytes)</li>'
        for frame in manifest["frames"]
    )
    quality = manifest["quality"]
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>AMCF Component Event Viewer</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.45; }}
    code {{ background: #f2f2f2; padding: 0.1rem 0.25rem; }}
    .boundary {{ border-left: 4px solid #444; padding-left: 1rem; }}
  </style>
</head>
<body>
  <h1>AMCF Component Event Viewer</h1>
  <p>This is a static software inspection viewer for a component-event archive demo. It is not a final UI, not hardware validation, and not physical playback proof.</p>
  <dl>
    <dt>Archive</dt><dd><code>{html.escape(str(manifest["archive_path_name"]))}</code></dd>
    <dt>Frames</dt><dd>{int(manifest["frame_count"])}</dd>
    <dt>Events</dt><dd>{int(manifest["event_count"])}</dd>
    <dt>Mean absolute error</dt><dd>{html.escape(str(quality.get("mean_absolute_error")))}</dd>
    <dt>Mean SSIM</dt><dd>{html.escape(str(quality.get("mean_ssim")))}</dd>
  </dl>
  <section class=\"boundary\">
    <h2>Claim Boundary</h2>
    <p>hardware_validation_claimed: false<br>
    physical_level_5_claimed: false<br>
    manufactured_player_claimed: false<br>
    unsafe_acceptance_count: {int(manifest["unsafe_acceptance_count"])}</p>
  </section>
  <h2>Decoded Frame Payloads</h2>
  <ul>
    {frame_items}
  </ul>
</body>
</html>
"""
