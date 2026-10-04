"""Thin, testable wrapper around the ffmpeg binary."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import List, Sequence

from studio.common import StudioError


def ffmpeg_bin() -> str:
    path = shutil.which("ffmpeg")
    if not path:
        raise StudioError("ffmpeg is not installed or not on PATH.")
    return path


def run(args: Sequence[str], timeout: int = 3600) -> subprocess.CompletedProcess:
    command: List[str] = [ffmpeg_bin(), "-hide_banner", "-loglevel", "error", "-y", *map(str, args)]
    done = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    if done.returncode != 0:
        raise StudioError(f"ffmpeg failed: {done.stderr.strip()[-1500:]}\ncommand: {' '.join(command)}")
    return done


def parse_resolution(value: str):
    width, _, height = str(value).lower().partition("x")
    return int(width), int(height)


def ensure_parent(path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
