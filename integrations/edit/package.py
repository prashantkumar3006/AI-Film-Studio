"""Mux the final deliverable: picture + one audio track per language +
soft subtitles, each tagged with its language.

YouTube accepts separate audio language tracks only through its own
upload flow (where available to the channel), so the package also keeps
one fully mixed MP4 per language as a fallback.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from integrations.edit.ffmpeg import ensure_parent, run

ISO_639_2 = {"en": "eng", "hi": "hin", "ta": "tam", "te": "tel", "bn": "ben", "mr": "mar", "ja": "jpn"}


def package(video: Path, audio_tracks: List[Tuple[Path, str]], subtitles: List[Tuple[Path, str]], out: Path, aac_bitrate: str = "192k") -> Path:
    args: List[str] = ["-i", str(video)]
    for path, _ in audio_tracks:
        args += ["-i", str(path)]
    for path, _ in subtitles:
        args += ["-i", str(path)]
    args += ["-map", "0:v:0"]
    for i in range(len(audio_tracks)):
        args += ["-map", f"{1 + i}:a:0"]
    for i in range(len(subtitles)):
        args += ["-map", f"{1 + len(audio_tracks) + i}:s:0"]
    args += ["-c:v", "copy", "-c:a", "aac", "-b:a", aac_bitrate]
    if subtitles:
        args += ["-c:s", "mov_text"]
    for i, (_, lang) in enumerate(audio_tracks):
        args += [f"-metadata:s:a:{i}", f"language={ISO_639_2.get(lang, lang)}"]
        args += [f"-disposition:a:{i}", "default" if i == 0 else "0"]
    for i, (_, lang) in enumerate(subtitles):
        args += [f"-metadata:s:s:{i}", f"language={ISO_639_2.get(lang, lang)}"]
    # No -shortest: it would end the file at the last subtitle cue.
    # Audio mixes are already trimmed to the picture length.
    args += ["-movflags", "+faststart", str(ensure_parent(out))]
    run(args)
    return Path(out)
