"""Assemble a picture edit from an EDL (edit decision list).

EDL JSON (written by ``studio.orchestrator.anime.build_edl`` or by hand)::

    {
      "fps": 24, "resolution": "1920x1080",
      "clips": [
        {"shot_id": "SC01_SH001", "path": "…/SC01_SH001.mp4", "duration_s": 4.0},
        ...
      ]
    }

Each clip is normalised (size, fps, pixel format) and trimmed or padded
to its exact shot duration, so audio timing derived from the shot list
stays in sync. Then all clips are concatenated without re-timing.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, Dict, List

from integrations.edit.ffmpeg import ensure_parent, parse_resolution, run
from studio.common import StudioError, load_json


def normalize_clip(source: Path, out: Path, duration_s: float, resolution: str, fps: int) -> Path:
    width, height = parse_resolution(resolution)
    frames = max(1, round(float(duration_s) * fps))
    vf = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
        f"fps={fps},setsar=1,format=yuv420p,"
        f"tpad=stop_mode=clone:stop_duration={float(duration_s):.3f}"
    )
    run(["-i", str(source), "-an", "-vf", vf, "-frames:v", str(frames), "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", str(ensure_parent(out))])
    return Path(out)


def assemble(edl: Dict[str, Any], out: Path, workdir: Path = None) -> Dict[str, Any]:
    fps = int(edl.get("fps", 24))
    resolution = str(edl.get("resolution", "1920x1080"))
    clips: List[Dict[str, Any]] = edl.get("clips") or []
    if not clips:
        raise StudioError("EDL has no clips.")
    missing = [c.get("path") for c in clips if not Path(c.get("path", "")).is_file()]
    if missing:
        raise StudioError(f"EDL references missing files: {missing[:5]}{' ...' if len(missing) > 5 else ''}")

    workdir = Path(workdir or tempfile.mkdtemp(prefix="assemble-"))
    workdir.mkdir(parents=True, exist_ok=True)
    normalized = []
    for index, clip in enumerate(clips):
        target = workdir / f"{index:04d}_{clip.get('shot_id', 'clip')}.mp4"
        normalize_clip(Path(clip["path"]), target, float(clip["duration_s"]), resolution, fps)
        normalized.append(target)

    listing = workdir / "concat.txt"
    listing.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in normalized), encoding="utf-8")
    run(["-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(ensure_parent(out))])
    total = sum(float(c["duration_s"]) for c in clips)
    return {"output": str(out), "clips": len(clips), "duration_s": round(total, 3), "fps": fps, "resolution": resolution}


def assemble_file(edl_path: Path, out: Path) -> Dict[str, Any]:
    return assemble(load_json(edl_path), out)
