"""Mouth-shape timing from dialogue audio with Rhubarb Lip Sync (MIT).

https://github.com/DanielSWolf/rhubarb-lip-sync — a CPU command-line tool,
fine on a laptop. English uses the default recognizer; Hindi and other
languages use ``--recognizer phonetic`` (language independent).

Mouth shapes (Rhubarb / Hanna-Barbera convention):

    A  closed (M, B, P)         D  wide open (AA)
    B  slightly open (K, S, T)  E  rounded (AO, ER)
    C  open (EH, AE)            F  puckered (UW, OW, W)
    G  F/V (teeth on lip)       H  L (tongue)        X  idle / rest
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.common import StudioError, load_json

BASIC = ("A", "B", "C", "D", "E", "F")
EXTENDED = ("G", "H", "X")


def rhubarb_bin(explicit: Optional[str] = None) -> str:
    path = explicit or shutil.which("rhubarb")
    if not path:
        raise StudioError("Rhubarb Lip Sync not found. Download a release from github.com/DanielSWolf/rhubarb-lip-sync and put 'rhubarb' on PATH.")
    return path


def build_command(audio: Path, out_json: Path, language: str = "en", dialog_text: Optional[str] = None, extended: str = "GHX", binary: str = "rhubarb", dialog_file: Optional[Path] = None) -> List[str]:
    command = [binary, "-f", "json", "-o", str(out_json), "--extendedShapes", extended]
    if language != "en":
        command += ["--recognizer", "phonetic"]
    if dialog_text and dialog_file is not None and language == "en":
        command += ["--dialogFile", str(dialog_file)]
    return command + [str(audio)]


def mouth_cues(audio: Path, language: str = "en", dialog_text: Optional[str] = None, extended: str = "GHX", binary: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return [{"start": s, "end": s, "value": "A"}...]."""
    binary = rhubarb_bin(binary)
    with tempfile.TemporaryDirectory() as tmp:
        out_json = Path(tmp) / "cues.json"
        dialog_file = Path(tmp) / "dialog.txt"
        if dialog_text:
            dialog_file.write_text(dialog_text, encoding="utf-8")
        command = build_command(Path(audio), out_json, language, dialog_text, extended, binary, dialog_file)
        done = subprocess.run(command, capture_output=True, text=True, check=False)
        if done.returncode != 0:
            raise StudioError(f"Rhubarb failed: {done.stderr.strip()[-800:]}")
        return load_json(out_json).get("mouthCues") or []
