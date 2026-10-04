"""Write SRT subtitles from timed dialogue (one file per language)."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any, Dict, List

from integrations.edit.ffmpeg import ensure_parent


def _stamp(seconds: float) -> str:
    millis = int(round(max(0.0, seconds) * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def wrap(text: str, max_chars: int = 42, max_lines: int = 2) -> List[List[str]]:
    """Split a line into subtitle cards of at most ``max_lines`` lines."""
    lines = textwrap.wrap(" ".join(text.split()), width=max_chars) or [""]
    return [lines[i : i + max_lines] for i in range(0, len(lines), max_lines)]


def write_srt(items: List[Dict[str, Any]], out: Path, max_chars: int = 42, max_lines: int = 2) -> Path:
    """``items``: [{"start_s", "end_s", "text"}], already in time order."""
    blocks = []
    index = 1
    for item in items:
        start, end = float(item["start_s"]), float(item["end_s"])
        cards = wrap(str(item["text"]), max_chars, max_lines)
        span = (end - start) / len(cards)
        for n, card in enumerate(cards):
            card_start = start + n * span
            blocks.append(f"{index}\n{_stamp(card_start)} --> {_stamp(card_start + span)}\n" + "\n".join(card) + "\n")
            index += 1
    ensure_parent(out).write_text("\n".join(blocks), encoding="utf-8")
    return Path(out)
