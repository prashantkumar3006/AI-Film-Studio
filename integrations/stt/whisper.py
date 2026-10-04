"""Speech-to-text with faster-whisper (MIT): dialogue QC and subtitle timing.

Note: Whisper *listens*; it does not speak. It is not a voice generator.
(Wispr Flow is a separate dictation app for typing by voice — useful for
writing scripts hands-free, not part of this pipeline.)

Two uses here:

1. ``transcribe`` — the dialogue_accuracy check compares what the TTS
   actually said with the script (catches skipped/garbled words).
2. ``word_timings`` — precise subtitle timing for each line.

Install where it runs: ``pip install faster-whisper``. The ``small``
model runs on a laptop CPU for short lines; use ``large-v3`` on the GPU
for Hindi accuracy.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.common import StudioError


@lru_cache(maxsize=2)
def _model(size: str, device: str, compute_type: str):
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except ImportError as error:
        raise StudioError("faster-whisper is not installed: pip install faster-whisper") from error
    return WhisperModel(size, device=device, compute_type=compute_type)


def available() -> bool:
    try:
        import faster_whisper  # type: ignore  # noqa: F401
    except ImportError:
        return False
    return True


def transcribe(audio: Path, language: str = "en", size: str = "small", device: str = "auto", compute_type: str = "int8") -> str:
    model = _model(size, device, compute_type)
    segments, _ = model.transcribe(str(audio), language=language, beam_size=5, vad_filter=False)
    return " ".join(segment.text.strip() for segment in segments).strip()


def word_timings(audio: Path, language: str = "en", size: str = "small", device: str = "auto", compute_type: str = "int8") -> List[Dict[str, Any]]:
    model = _model(size, device, compute_type)
    segments, _ = model.transcribe(str(audio), language=language, word_timestamps=True)
    words: List[Dict[str, Any]] = []
    for segment in segments:
        for word in segment.words or []:
            words.append({"word": word.word.strip(), "start": round(word.start, 3), "end": round(word.end, 3)})
    return words


def transcriber(config: Dict[str, Any]) -> Optional[Any]:
    """A callable(path) -> text for the QC context, or None if unavailable."""
    if not available():
        return None
    stt = (config.get("tools") or {}).get("stt_faster_whisper") or {}
    size = stt.get("model", "small")

    def run(path: Path, language: str = "en") -> str:
        return transcribe(path, language=language, size=size)

    return run
