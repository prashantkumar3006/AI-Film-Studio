"""Measure media with ffprobe / ffmpeg (the only required external tools).

Every function returns plain dicts so results can go straight into QC
reports. Nothing here modifies media.
"""

from __future__ import annotations

import json
import re
import shutil
import statistics
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.common import StudioError


def require(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        raise StudioError(f"'{tool}' is not installed or not on PATH (needed for QC).")
    return path


def _run(args: List[str], timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)


def probe(path: Path) -> Dict[str, Any]:
    """Basic stream facts for an image, video or audio file."""
    path = Path(path)
    if not path.is_file():
        raise StudioError(f"File not found: {path}")
    done = _run([require("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    if done.returncode != 0:
        raise StudioError(f"ffprobe could not read {path.name}: {done.stderr.strip()[:300]}")
    data = json.loads(done.stdout or "{}")
    info: Dict[str, Any] = {"path": str(path), "video": None, "audio": [], "duration_s": None}
    fmt = data.get("format") or {}
    if fmt.get("duration"):
        info["duration_s"] = round(float(fmt["duration"]), 3)
    for stream in data.get("streams", []):
        kind = stream.get("codec_type")
        if kind == "video" and info["video"] is None:
            fps = None
            rate = stream.get("avg_frame_rate") or stream.get("r_frame_rate")
            if rate and rate not in {"0/0", "0"}:
                fps = round(float(Fraction(rate)), 3)
            info["video"] = {
                "codec": stream.get("codec_name"),
                "width": stream.get("width"),
                "height": stream.get("height"),
                "fps": fps,
                "pix_fmt": stream.get("pix_fmt"),
                "frames": int(stream["nb_frames"]) if str(stream.get("nb_frames", "")).isdigit() else None,
            }
        elif kind == "audio":
            info["audio"].append(
                {
                    "codec": stream.get("codec_name"),
                    "sample_rate": int(stream.get("sample_rate") or 0),
                    "channels": stream.get("channels"),
                    "language": (stream.get("tags") or {}).get("language"),
                }
            )
    return info


def loudness(path: Path) -> Dict[str, Optional[float]]:
    """Integrated loudness (LUFS), loudness range and true peak (dBTP)."""
    done = _run(
        [require("ffmpeg"), "-hide_banner", "-nostats", "-i", str(path), "-filter_complex", "ebur128=peak=true", "-f", "null", "-"]
    )
    text = done.stderr
    summary = text[text.rfind("Summary:"):] if "Summary:" in text else text

    def grab(pattern: str) -> Optional[float]:
        match = re.search(pattern, summary)
        return float(match.group(1)) if match else None

    return {
        "integrated_lufs": grab(r"I:\s+(-?[\d.]+|-inf)\s+LUFS"),
        "range_lu": grab(r"LRA:\s+(-?[\d.]+)\s+LU"),
        "true_peak_dbtp": grab(r"Peak:\s+(-?[\d.]+)\s+dBFS"),
    }


def frame_differences(path: Path, max_frames: int = 2000) -> List[float]:
    """Mean luma difference between consecutive frames (ffmpeg signalstats YDIF)."""
    done = _run(
        [
            require("ffmpeg"),
            "-hide_banner",
            "-i",
            str(path),
            "-frames:v",
            str(max_frames),
            "-vf",
            "signalstats,metadata=print:key=lavfi.signalstats.YDIF:file=-",
            "-f",
            "null",
            "-",
        ]
    )
    values = [float(v) for v in re.findall(r"lavfi\.signalstats\.YDIF=([\d.]+)", done.stdout)]
    return values[1:]  # the first frame has nothing to compare against


def flicker_score(path: Path) -> Dict[str, Any]:
    """Spikes in frame-to-frame change relative to the clip's own baseline.

    AI video often 'pops' (identity flicker, sudden lighting jumps). A
    spike ratio well above the median signals a frame worth inspecting.
    """
    diffs = frame_differences(path)
    if len(diffs) < 3:
        return {"frames": len(diffs), "spike_ratio": 0.0, "median": None, "max": None}
    median = statistics.median(diffs)
    peak = max(diffs)
    ratio = peak / median if median > 0.05 else (0.0 if peak < 1.0 else peak)
    return {"frames": len(diffs) + 1, "median": round(median, 3), "max": round(peak, 3), "spike_ratio": round(ratio, 2)}


def black_segments(path: Path, min_seconds: float = 0.5) -> List[Dict[str, float]]:
    done = _run(
        [require("ffmpeg"), "-hide_banner", "-i", str(path), "-vf", f"blackdetect=d={min_seconds}:pix_th=0.10", "-an", "-f", "null", "-"]
    )
    segments = []
    for start, end in re.findall(r"black_start:([\d.]+)\s+black_end:([\d.]+)", done.stderr):
        segments.append({"start": float(start), "end": float(end)})
    return segments
