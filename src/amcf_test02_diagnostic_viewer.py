from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from typing import Any


DIAGNOSTIC_VIEWER_SCHEMA = "amcf-test02-diagnostic-viewer-v1"


def load_tracks_manifest(path: str | Path) -> dict[str, Any]:
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    if "frames" not in manifest or not isinstance(manifest["frames"], list):
        raise ValueError("tracks manifest missing frames list")
    for frame in manifest["frames"]:
        if "frame_index" not in frame or "tracks" not in frame:
            raise ValueError("track frame missing frame_index or tracks")
        if not isinstance(frame["tracks"], list):
            raise ValueError("track frame tracks must be a list")
    return manifest


def build_track_taxonomy(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for frame in manifest["frames"]:
        for track in frame.get("tracks", []):
            track_id = str(track["track_id"])
            row = by_id.setdefault(
                track_id,
                {
                    "track_id": track_id,
                    "parent_id": track.get("parent_id"),
                    "label": track.get("label", track_id),
                    "frames_visible": 0,
                    "component_update_count": 0,
                    "contour_frame_count": 0,
                    "max_motion_p95_px_s": 0.0,
                    "update_reasons": {},
                },
            )
            row["frames_visible"] += 1
            if track.get("component_update"):
                row["component_update_count"] += 1
            if track.get("contours"):
                row["contour_frame_count"] += 1
            row["max_motion_p95_px_s"] = max(
                float(row["max_motion_p95_px_s"]),
                float(track.get("motion_p95_px_s", 0.0) or 0.0),
            )
            reason = str(track.get("update_reason", "unknown"))
            row["update_reasons"][reason] = int(row["update_reasons"].get(reason, 0)) + 1
    return [by_id[key] for key in sorted(by_id)]


def summarize_tracks_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    taxonomy = build_track_taxonomy(manifest)
    frame_count = len(manifest["frames"])
    contour_frames = 0
    update_events = 0
    for frame in manifest["frames"]:
        for track in frame.get("tracks", []):
            if track.get("contours"):
                contour_frames += 1
            if track.get("component_update"):
                update_events += 1
    return {
        "schema": DIAGNOSTIC_VIEWER_SCHEMA,
        "frame_count": frame_count,
        "track_count": len(taxonomy),
        "taxonomy": taxonomy,
        "contour_track_frames": contour_frames,
        "component_update_events": update_events,
        "has_parent_child_taxonomy": any(row.get("parent_id") for row in taxonomy),
        "has_motion_metrics": any(row["max_motion_p95_px_s"] > 0 for row in taxonomy),
        "claim_boundary": {
            "hardware_validation_claimed": False,
            "physical_level_5_claimed": False,
            "manufactured_player_claimed": False,
            "final_ui_claimed": False,
        },
        "unsafe_acceptance_count": 0,
    }


def build_test02_diagnostic_viewer(
    *,
    tracks_manifest_path: str | Path,
    output_dir: str | Path,
    comparison_video_path: str | Path | None = None,
    difference_video_path: str | Path | None = None,
) -> dict[str, Any]:
    tracks_manifest_path = Path(tracks_manifest_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = load_tracks_manifest(tracks_manifest_path)
    summary = summarize_tracks_manifest(manifest)

    copied_tracks = output_dir / "tracks_manifest.json"
    copied_tracks.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    assets: dict[str, str | None] = {"comparison_video": None, "difference_video": None}
    if comparison_video_path is not None:
        source = Path(comparison_video_path)
        if source.exists():
            target = output_dir / "comparison_sync.mp4"
            shutil.copy2(source, target)
            assets["comparison_video"] = target.name
    if difference_video_path is not None:
        source = Path(difference_video_path)
        if source.exists():
            target = output_dir / "comparison_difference.mp4"
            shutil.copy2(source, target)
            assets["difference_video"] = target.name

    report = {
        "ok": True,
        "schema": DIAGNOSTIC_VIEWER_SCHEMA,
        "viewer_dir": str(output_dir),
        "viewer_html": str(output_dir / "index.html"),
        "tracks_manifest": str(copied_tracks),
        "assets": assets,
        **summary,
    }
    (output_dir / "diagnostic_viewer_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "index.html").write_text(_diagnostic_viewer_html(summary, assets), encoding="utf-8")
    return report


def _diagnostic_viewer_html(summary: dict[str, Any], assets: dict[str, str | None]) -> str:
    comparison_src = html.escape(assets.get("comparison_video") or "")
    difference_src = html.escape(assets.get("difference_video") or "")
    fallback_note = (
        "No comparison video asset was packaged; load a compatible same-clock comparison video next to this viewer."
        if not comparison_src else
        "Comparison video packaged."
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AMCF Test 02 Diagnostic Viewer</title>
<style>
body{{margin:0;background:#101214;color:#e8ecef;font-family:Segoe UI,Arial,sans-serif}}
main{{max-width:1500px;margin:0 auto;padding:16px}}
.stage{{position:relative;background:#050607;aspect-ratio:4/1;border:1px solid #343a40}}
video,canvas{{position:absolute;inset:0;width:100%;height:100%}}
.bar{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:12px 0}}
button,select,input{{background:#1e252b;color:#eef3f6;border:1px solid #59636c;border-radius:4px;padding:7px 9px}}
input[type=range]{{flex:1;min-width:220px}}
.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px}}
.metric{{background:#171c20;border:1px solid #333b42;border-radius:6px;padding:8px;font-size:13px}}
.labels{{display:flex;justify-content:space-between;font-size:13px;color:#b9c2c9;margin-bottom:4px}}
.boundary{{border-left:4px solid #5f6b75;padding-left:12px;color:#c9d1d8}}
</style>
</head>
<body>
<main>
<h1>AMCF Test 02 Diagnostic Viewer</h1>
<p>This viewer preserves the Test 02 diagnostic surface for frame-indexed contours, object track taxonomy, update reasons, and motion metrics. It is not a final UI or hardware validation.</p>
<div class="boundary">hardware_validation_claimed: false<br>physical_level_5_claimed: false<br>manufactured_player_claimed: false<br>unsafe_acceptance_count: {int(summary["unsafe_acceptance_count"])}</div>
<p>{html.escape(fallback_note)}</p>
<div class="labels"><span>Source / comparison</span><span>AMCF reconstruction / difference view</span></div>
<div class="stage"><video id="v" src="{comparison_src}" muted playsinline></video><canvas id="c"></canvas></div>
<div class="bar">
<button id="play">Play</button><button id="back">-1 frame</button><button id="fwd">+1 frame</button>
<select id="speed"><option>0.25</option><option>0.5</option><option selected>1</option><option>2</option></select>
<label><input id="loop" type="checkbox" checked> loop</label>
<label><input id="overlay" type="checkbox" checked> contours</label>
<label><input id="vectors" type="checkbox" checked> metrics</label>
<label><input id="diff" type="checkbox"> difference</label>
<select id="focus"><option value="">all objects</option></select>
<input id="seek" type="range" min="0" max="{max(0, int(summary["frame_count"]) - 1)}" value="0">
<button id="export">Export frame data</button>
</div>
<div id="readout"></div>
<div class="metrics" id="metrics"></div>
</main>
<script>
const fallbackFps = 24000/1001;
const differenceSrc = "{difference_src}";
let data = null;
const video = document.getElementById('v');
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const seek = document.getElementById('seek');
const focus = document.getElementById('focus');
fetch('tracks_manifest.json').then(r=>r.json()).then(j=>{{data=j; init(); draw();}});
function fps(){{ return data && data.fps ? Number(data.fps) : fallbackFps; }}
function init(){{
  const seen = new Set();
  for(const fr of data.frames){{ for(const t of fr.tracks){{ seen.add(t.track_id); }} }}
  for(const id of [...seen].sort()){{ const o=document.createElement('option'); o.value=id; o.textContent=id; focus.appendChild(o); }}
}}
function frameIndex(){{ return Math.max(0, Math.min(data.frames.length-1, Math.round((video.currentTime || 0)*fps()))); }}
function scalePoint(p, rect, sideOffset){{
  const source = data.source_size || [3840, 1920];
  const display = data.display_size || [source[0], source[1]];
  const halfWidth = rect.width / 2;
  const sx = halfWidth / display[0];
  const sy = rect.height / display[1];
  const downX = source[0] / display[0];
  const downY = source[1] / display[1];
  return [sideOffset + (p[0] / downX) * sx, (p[1] / downY) * sy];
}}
function draw(){{
  requestAnimationFrame(draw);
  if(!data) return;
  const rect = canvas.getBoundingClientRect();
  const dpr = devicePixelRatio || 1;
  canvas.width = Math.round(rect.width*dpr); canvas.height = Math.round(rect.height*dpr);
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,rect.width,rect.height);
  const i = frameIndex();
  seek.value = i;
  const fr = data.frames[i];
  document.getElementById('readout').textContent = `frame ${{i+1}}/${{data.frames.length}}  pts ${{Number(fr.pts_seconds || 0).toFixed(3)}}s  speed ${{video.playbackRate || 1}}x`;
  const showOverlay = document.getElementById('overlay').checked;
  const showMetrics = document.getElementById('vectors').checked;
  const selected = focus.value;
  let metricHtml = '';
  for(const t of fr.tracks){{
    if(selected && t.track_id !== selected) continue;
    const color = t.color_bgr ? `rgb(${{t.color_bgr[2]}},${{t.color_bgr[1]}},${{t.color_bgr[0]}})` : '#75d7ff';
    if(showOverlay && t.contours){{
      ctx.lineWidth = 2; ctx.strokeStyle = color; ctx.fillStyle = color;
      for(const contour of t.contours){{
        for(const side of [0, rect.width/2]){{
          ctx.beginPath();
          contour.forEach((p,k)=>{{ const q=scalePoint(p, rect, side); if(k) ctx.lineTo(q[0], q[1]); else ctx.moveTo(q[0], q[1]); }});
          ctx.closePath(); ctx.stroke();
        }}
      }}
    }}
    if(showMetrics){{
      const update = t.component_update ? (t.update_reason || 'update') : 'held';
      metricHtml += `<div class="metric"><b>${{t.track_id}}</b><br>parent: ${{t.parent_id || 'none'}}<br>update: ${{update}}<br>motion median: ${{Number(t.motion_median_px_s || 0).toFixed(1)}} px/s<br>confidence: ${{Number(t.confidence || 0).toFixed(2)}}</div>`;
    }}
  }}
  document.getElementById('metrics').innerHTML = metricHtml;
}}
document.getElementById('play').onclick=()=>{{ if(video.paused){{video.play(); play.textContent='Pause'}} else {{video.pause(); play.textContent='Play'}} }};
document.getElementById('back').onclick=()=>{{ video.pause(); video.currentTime=Math.max(0,(frameIndex()-1)/fps()); }};
document.getElementById('fwd').onclick=()=>{{ video.pause(); video.currentTime=Math.min(video.duration || 0,(frameIndex()+1)/fps()); }};
document.getElementById('speed').onchange=e=>video.playbackRate=parseFloat(e.target.value);
document.getElementById('loop').onchange=e=>video.loop=e.target.checked; video.loop=true;
seek.oninput=e=>{{ video.pause(); video.currentTime=parseInt(e.target.value,10)/fps(); }};
document.getElementById('diff').onchange=e=>{{ if(!differenceSrc) return; const t=video.currentTime; const was=!video.paused; video.src=e.target.checked?differenceSrc:'{comparison_src}'; video.currentTime=t; if(was) video.play(); }};
document.getElementById('export').onclick=()=>{{ const fr=data.frames[frameIndex()]; const blob=new Blob([JSON.stringify(fr,null,2)],{{type:'application/json'}}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=`amcf_frame_${{fr.frame_index+1}}.json`; a.click(); }};
</script>
</body>
</html>
"""
