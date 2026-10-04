"""Build a talking ``limited`` shot from mouth-shape frames + Rhubarb cues.

Inputs per shot: one full frame per mouth shape (the approved keyframe
with the mouth region inpainted into shapes A–F, optionally G/H/X —
generated once in ComfyUI). Output: a video that switches frames on the
cue times, snapped to the animation grid (anime usually animates mouths
"on twos": a new drawing at most every 2 frames at 24 fps).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from integrations.edit.ffmpeg import ensure_parent, parse_resolution, run
from studio.common import StudioError

# Nearest available drawing for each shape, best first. "A" (closed) is
# the one shape every character must have.
PREFERENCES = {
    "A": [],
    "B": ["C", "A"],
    "C": ["D", "B", "A"],
    "D": ["C", "B", "A"],
    "E": ["D", "C", "B", "A"],
    "F": ["E", "D", "B", "A"],
    "G": ["B", "A"],
    "H": ["C", "B", "A"],
    "X": ["A"],
}


def resolve_shape(value: str, frames: Dict[str, Path]) -> str:
    if "A" not in frames:
        raise StudioError(f"Mouth set needs at least shape 'A' (closed); have {sorted(frames)}.")
    if value in frames:
        return value
    for candidate in PREFERENCES.get(value, ["A"]):
        if candidate in frames:
            return candidate
    raise StudioError(f"No mouth frame for shape '{value}' (have {sorted(frames)}).")


def timeline(cues: List[Dict[str, Any]], frames: Dict[str, Path], duration_s: float, fps: int = 24, on: int = 2, offset_s: float = 0.0) -> List[Dict[str, Any]]:
    """Snap cues to the frame grid and merge repeats. Returns [{shape, frames}]."""
    rest = resolve_shape("X", frames)
    total = max(1, round(duration_s * fps))
    grid = [rest] * total
    for cue in cues:
        shape = resolve_shape(str(cue["value"]), frames)
        start = round((float(cue["start"]) + offset_s) * fps)
        end = round((float(cue["end"]) + offset_s) * fps)
        for f in range(max(0, start), min(total, end)):
            grid[f] = shape
    # hold each drawing at least `on` frames (animating on twos)
    for f in range(0, total, on):
        for k in range(f, min(f + on, total)):
            grid[k] = grid[f]
    segments: List[Dict[str, Any]] = []
    for shape in grid:
        if segments and segments[-1]["shape"] == shape:
            segments[-1]["frames"] += 1
        else:
            segments.append({"shape": shape, "frames": 1})
    return segments


def render(segments: List[Dict[str, Any]], frames: Dict[str, Path], out: Path, fps: int = 24, resolution: str = "1920x1080") -> Path:
    width, height = parse_resolution(resolution)
    listing = Path(out).with_suffix(".concat.txt")
    lines = []
    for seg in segments:
        lines.append(f"file '{Path(frames[seg['shape']]).resolve().as_posix()}'")
        lines.append(f"duration {seg['frames'] / fps:.6f}")
    lines.append(f"file '{Path(frames[segments[-1]['shape']]).resolve().as_posix()}'")  # concat demuxer needs the last file twice
    ensure_parent(listing).write_text("\n".join(lines) + "\n", encoding="utf-8")
    total_frames = sum(seg["frames"] for seg in segments)
    run(
        [
            "-f", "concat", "-safe", "0", "-i", str(listing),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,fps={fps},setsar=1,format=yuv420p",
            "-frames:v", str(total_frames), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", str(out),
        ]
    )
    listing.unlink(missing_ok=True)
    return Path(out)
