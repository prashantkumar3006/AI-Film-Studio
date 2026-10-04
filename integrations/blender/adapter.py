"""Render layout (blocking) frames from Blender for ControlNet guidance.

Two ways Blender is used in this studio:

1. **Interactive, with Claude** — Blender MCP (github.com/ahujasid/blender-mcp,
   MIT) lets Claude build and edit 3D sets, props and blocking inside your
   Blender through the Claude desktop app. Setup is in ``README.md``.
2. **Headless, in the pipeline** — this adapter renders a shot's camera
   from a ``.blend`` layout file with the fast Workbench engine (works on
   CPU). ComfyUI then extracts depth / lineart from that frame
   (preprocessor nodes) to lock composition and perspective, while the
   anime look comes from the checkpoint + LoRA.

    blender -b layout.blend --python integrations/blender/scripts/render_layout.py -- \
        --camera CAM_SC01_SH001 --frame 1 --out .../layout/SC01_SH001.png
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

from studio.common import StudioError

SCRIPT = Path(__file__).resolve().parent / "scripts" / "render_layout.py"


def blender_bin(explicit: Optional[str] = None) -> str:
    path = explicit or shutil.which("blender")
    if not path:
        raise StudioError("Blender not found on PATH. Install Blender (blender.org) or set tools.blender.binary in config.")
    return path


def build_command(blend: Path, out: Path, camera: Optional[str] = None, frame: int = 1, end_frame: Optional[int] = None, resolution: str = "1920x1080", binary: str = "blender") -> List[str]:
    command = [binary, "-b", str(blend), "--python", str(SCRIPT), "--", "--out", str(out), "--frame", str(frame), "--resolution", resolution]
    if camera:
        command += ["--camera", camera]
    if end_frame:
        command += ["--end-frame", str(end_frame)]
    return command


def render_layout(blend: Path, out: Path, camera: Optional[str] = None, frame: int = 1, end_frame: Optional[int] = None, resolution: str = "1920x1080", binary: Optional[str] = None, timeout: int = 1800) -> Path:
    if not Path(blend).is_file():
        raise StudioError(f"Layout file not found: {blend}")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    done = subprocess.run(build_command(blend, out, camera, frame, end_frame, resolution, blender_bin(binary)), capture_output=True, text=True, timeout=timeout, check=False)
    if done.returncode != 0 or "STUDIO_RENDER_OK" not in done.stdout:
        raise StudioError(f"Blender render failed:\n{(done.stderr or done.stdout)[-1500:]}")
    return Path(out)
