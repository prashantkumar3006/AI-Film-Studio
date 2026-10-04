"""Shared test helpers: synthetic media and throwaway repo copies.

Tests never touch real projects: anything that writes state runs in a
temporary copy of the repository.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))

needs_ffmpeg = unittest.skipUnless(HAS_FFMPEG, "ffmpeg/ffprobe not installed")


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def make_image(path: Path, size: str = "1920x1080", source: str = "testsrc2") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg("-f", "lavfi", "-i", f"{source}=size={size}", "-frames:v", "1", str(path))
    return path


def make_color_image(path: Path, color: str, size: str = "512x512") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg("-f", "lavfi", "-i", f"color=c={color}:size={size}", "-frames:v", "1", str(path))
    return path


def make_video(path: Path, seconds: float = 2.0, size: str = "1920x1080", fps: int = 24, source: str = "testsrc2") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    joiner = ":" if "=" in source else "="
    ffmpeg("-f", "lavfi", "-i", f"{source}{joiner}size={size}:rate={fps}", "-t", str(seconds), "-pix_fmt", "yuv420p", str(path))
    return path


def make_tone(path: Path, seconds: float = 1.0, freq: int = 440, volume_db: float = -6.0) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg("-f", "lavfi", "-i", f"sine=frequency={freq}:duration={seconds}", "-af", f"volume={volume_db}dB", "-ar", "48000", str(path))
    return path


class RepoCopy:
    """A disposable copy of the repo (without .git) for state-writing tests."""

    def __init__(self, with_demo: bool = False):
        self.tmp = Path(tempfile.mkdtemp(prefix="studio-test-"))
        self.root = self.tmp / "repo"
        shutil.copytree(
            REPO,
            self.root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules", "projects"),
        )
        (self.root / "projects").mkdir(exist_ok=True)
        if with_demo:
            shutil.copytree(FIXTURES / "demo", self.root / "series" / "demo")
            make_color_image(self.root / "series" / "demo" / "bible" / "refs" / "aria" / "model_sheet_v001.png", "0x3D6E8C")

    def run(self, *args: str, env=None, check: bool = False) -> subprocess.CompletedProcess:
        environment = dict(os.environ)
        environment.update(env or {})
        done = subprocess.run([sys.executable, *args], cwd=self.root, capture_output=True, text=True, env=environment)
        if check and done.returncode != 0:
            raise AssertionError(f"{args} failed ({done.returncode}):\n{done.stdout}\n{done.stderr}")
        return done

    def studio(self, *args: str, **kwargs) -> subprocess.CompletedProcess:
        return self.run("-m", "studio", *args, **kwargs)

    def cleanup(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)
