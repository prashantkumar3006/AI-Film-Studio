"""Generate every dialogue line of an episode with each character's voice.

Voices are defined per character and language in the bible::

    voice:
      en: {engine: tts_kokoro, voice: am_michael, speed: 1.0}
      hi: {engine: tts_indic_parler, speaker: Rohit,
           description: "Rohit speaks in a calm, low voice with clear audio"}

The engine key is a registry entry; its command template comes from
``tools.<engine>`` in ``studio/config.yaml``. Engines are only used once
their license is cleared (F5-TTS and XTTS-v2 weights, for example, are
non-commercial and stay blocked).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from integrations.common import ensure_file, run_tool
from studio.common import StudioError
from studio.legal.licenses import require_cleared
from studio.legal.provenance import write_provenance


def synthesize_line(line: Dict[str, Any], voice: Dict[str, Any], out: Path, config: Dict[str, Any], params: Dict[str, Any] = None, catalogue=None, remote=None) -> Path:
    engine = voice.get("engine")
    if not engine:
        raise StudioError(f"No TTS engine for {line.get('character')} ({line.get('language')}).")
    require_cleared([engine], mode=(config.get("legal") or {}).get("mode", "strict"), catalogue=catalogue)
    params = dict(params or {})
    values = {
        "text": line["text"],
        "out": str(out),
        "voice": voice.get("voice", ""),
        "speaker": voice.get("speaker", ""),
        "description": voice.get("description", ""),
        "language": line.get("language", "en"),
        "speed": params.get("speed", voice.get("speed", 1.0)),
        "seed": params.get("seed", 0),
        "emotion": line.get("emotion", "neutral"),
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    run_tool(config, engine, values, remote=remote)
    ensure_file(Path(out), f"Voice line {line.get('line_id')}")
    write_provenance(
        Path(out),
        {
            "kind": "voice_line",
            "tools": [engine],
            "models": [],
            "line_id": line.get("line_id"),
            "shot_id": line.get("shot_id"),
            "character": line.get("character"),
            "language": line.get("language"),
            "text": line["text"],
            "seed": values["seed"],
            "params": {"speed": values["speed"], "voice": values["voice"], "speaker": values["speaker"]},
            "synthetic_voice": True,
        },
        catalogue=catalogue,
    )
    return Path(out)


def voice_for(bible, character_id: str, language: str) -> Dict[str, Any]:
    if character_id == "narrator":
        spec = ((bible.series.get("narrator") or {}).get("voice") or {}).get(language)
    else:
        spec = (bible.character(character_id).get("voice") or {}).get(language)
    if not spec:
        raise StudioError(f"No {language} voice for '{character_id}' in the bible.")
    return spec


def line_path(project_root: Path, line: Dict[str, Any]) -> Path:
    return Path(project_root) / "14_sound" / "dialogue" / line["language"] / f"{line['line_id']}.wav"


def plan(bible, lines: List[Dict[str, Any]], project_root: Path) -> List[Dict[str, Any]]:
    """What would be generated, without generating (used by dry runs)."""
    out = []
    for line in lines:
        voice = voice_for(bible, line["character"], line["language"])
        out.append({**line, "engine": voice.get("engine"), "path": str(line_path(project_root, line)), "exists": line_path(project_root, line).is_file()})
    return out
