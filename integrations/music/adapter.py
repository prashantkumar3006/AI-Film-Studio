"""Music cues and SFX through command templates (``tools.music_ace_step``,
``tools.sfx_generator`` in config), with provenance.

Strategy that keeps quality high and cost low: build a **theme library**
once per season (main theme, hero, tension, mystery, sorrow, battle,
comedy, ending) and reuse and re-edit those cues every episode, like a
real anime soundtrack. Generate new cues only when a scene needs one.

ACE-Step code is Apache-2.0; the registry blocks it until the weights'
license for the version you install is verified. MusicGen weights are
CC-BY-NC and stay blocked for a monetised channel.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from integrations.common import ensure_file, run_tool
from studio.legal.licenses import require_cleared
from studio.legal.provenance import write_provenance


def generate_cue(cue_id: str, prompt: str, seconds: float, out: Path, config: Dict[str, Any], tool: str = "music_ace_step", lyrics: str = "[instrumental]", seed: int = 0, catalogue=None, remote=None) -> Path:
    require_cleared([tool], mode=(config.get("legal") or {}).get("mode", "strict"), catalogue=catalogue)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    run_tool(config, tool, {"prompt": prompt, "seconds": seconds, "out": str(out), "lyrics": lyrics, "seed": seed}, remote=remote)
    ensure_file(Path(out), f"Music cue {cue_id}")
    write_provenance(Path(out), {"kind": "music", "tools": [tool], "models": [], "cue_id": cue_id, "prompt": prompt, "lyrics": lyrics, "seed": seed, "seconds": seconds}, catalogue=catalogue)
    return Path(out)
