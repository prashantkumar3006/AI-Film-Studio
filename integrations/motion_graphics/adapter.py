"""Render Remotion compositions (titles, lower thirds, end cards).

Remotion is free for individuals and teams of up to 3 people; a company
license is required beyond that (remotion.dev/docs/license). Rendering
needs Node.js and downloads a headless Chrome on first run — run it on
the laptop (CPU is fine for titles) or on the GridShare box.

    cd integrations/motion_graphics/remotion && npm install
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.common import StudioError

PROJECT = Path(__file__).resolve().parent / "remotion"


def build_command(composition: str, out: Path, props_file: Path, codec: str = "h264", frames: Optional[int] = None) -> List[str]:
    command = ["npx", "remotion", "render", "src/index.ts", composition, str(out), f"--props={props_file}", f"--codec={codec}"]
    if frames:
        command.append(f"--frames=0-{frames - 1}")
    return command


def render(composition: str, out: Path, props: Dict[str, Any], codec: str = "h264", frames: Optional[int] = None, timeout: int = 1800) -> Path:
    if not shutil.which("npx"):
        raise StudioError("Node.js (npx) is required for Remotion: install Node 18+.")
    if not (PROJECT / "node_modules").is_dir():
        raise StudioError(f"Run 'npm install' in {PROJECT} first.")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(props, handle, ensure_ascii=False)
        props_file = Path(handle.name)
    try:
        done = subprocess.run(build_command(composition, Path(out).resolve(), props_file, codec, frames), cwd=PROJECT, capture_output=True, text=True, timeout=timeout, check=False)
    finally:
        props_file.unlink(missing_ok=True)
    if done.returncode != 0:
        raise StudioError(f"Remotion render failed:\n{(done.stderr or done.stdout)[-1500:]}")
    return Path(out)
