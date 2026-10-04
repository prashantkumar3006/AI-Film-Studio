"""Camera moves on a still keyframe (motion types ``hold`` and ``camera``).

Classic anime uses pans across large backgrounds, slow push-ins on a
held drawing and camera shake on impacts. These cost seconds of CPU
instead of minutes of GPU video generation.
"""

from __future__ import annotations

from pathlib import Path

from integrations.edit.ffmpeg import ensure_parent, parse_resolution, run
from studio.common import StudioError

MOVES = ("static", "push_in", "pull_out", "pan_left", "pan_right", "tilt_up", "tilt_down", "shake")


def _zoompan(move: str, frames: int, width: int, height: int, fps: int, strength: float) -> str:
    n = max(frames - 1, 1)
    zoom_end = 1.0 + 0.25 * strength
    pan_zoom = 1.0 + 0.2 * max(strength, 0.25)
    center_x, center_y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if move == "static":
        z, x, y = "1", "0", "0"
    elif move == "push_in":
        z, x, y = f"1+{zoom_end - 1:.4f}*on/{n}", center_x, center_y
    elif move == "pull_out":
        z, x, y = f"{zoom_end:.4f}-{zoom_end - 1:.4f}*on/{n}", center_x, center_y
    elif move in {"pan_left", "pan_right"}:
        travel = f"(iw-iw/zoom)*on/{n}"
        z, y = f"{pan_zoom:.4f}", center_y
        x = f"(iw-iw/zoom)-{travel}" if move == "pan_left" else travel
    elif move in {"tilt_up", "tilt_down"}:
        travel = f"(ih-ih/zoom)*on/{n}"
        z, x = f"{pan_zoom:.4f}", center_x
        y = f"(ih-ih/zoom)-{travel}" if move == "tilt_up" else travel
    elif move == "shake":
        amp = 6.0 * max(strength, 0.25)
        z = "1.06"
        x = f"{center_x}+{amp:.2f}*sin(on*2.1)"
        y = f"{center_y}+{amp:.2f}*cos(on*2.7)"
    else:
        raise StudioError(f"Unknown camera move '{move}'. Use one of {MOVES}.")
    # Upscale first so sub-pixel moves do not jitter.
    return (
        f"scale={width * 2}:{height * 2}:force_original_aspect_ratio=increase,"
        f"crop={width * 2}:{height * 2},"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={width}x{height}:fps={fps},"
        f"setsar=1,format=yuv420p"
    )


def still_to_clip(image: Path, out: Path, duration_s: float, move: str = "static", resolution: str = "1920x1080", fps: int = 24, strength: float = 1.0) -> Path:
    width, height = parse_resolution(resolution)
    frames = max(1, round(float(duration_s) * fps))
    run(
        [
            "-loop", "1", "-framerate", str(fps), "-i", str(image),
            "-vf", _zoompan(move, frames, width, height, fps, strength),
            "-frames:v", str(frames), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
            str(ensure_parent(out)),
        ]
    )
    return Path(out)
