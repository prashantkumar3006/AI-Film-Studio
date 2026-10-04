"""Mix dialogue, music and SFX into a delivery-ready stereo track.

* every clip is placed at its start time (``adelay``)
* music ducks automatically under dialogue (``sidechaincompress``)
* the result is normalised to the configured loudness (default −14 LUFS,
  −1 dBTP true peak) with ``loudnorm``

Tracks::

    {"dialogue": [{"path": "...wav", "start_s": 1.2}, ...],
     "music":    [{"path": "...wav", "start_s": 0.0, "gain_db": -6}],
     "sfx":      [{"path": "...wav", "start_s": 3.4, "gain_db": -3}]}
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from integrations.edit.ffmpeg import ensure_parent, run
from studio.common import StudioError


def _bus(inputs: List[Dict[str, Any]], offset: int, label: str, chains: List[str]) -> str:
    names = []
    for i, item in enumerate(inputs):
        delay = max(0, int(round(float(item.get("start_s", 0)) * 1000)))
        gain = float(item.get("gain_db", 0.0))
        name = f"{label}{i}"
        chains.append(
            f"[{offset + i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"adelay={delay}|{delay},volume={gain}dB[{name}]"
        )
        names.append(f"[{name}]")
    if len(names) == 1:
        chains.append(f"{names[0]}anull[{label}]")
    else:
        chains.append(f"{''.join(names)}amix=inputs={len(names)}:normalize=0:dropout_transition=0[{label}]")
    return f"[{label}]"


def mix(tracks: Dict[str, List[Dict[str, Any]]], out: Path, duration_s: float, loudness_lufs: float = -14.0, true_peak: float = -1.0, duck: bool = True) -> Path:
    dialogue = tracks.get("dialogue") or []
    music = tracks.get("music") or []
    sfx = tracks.get("sfx") or []
    if not (dialogue or music or sfx):
        raise StudioError("Nothing to mix.")
    for item in dialogue + music + sfx:
        if not Path(item["path"]).is_file():
            raise StudioError(f"Missing audio: {item['path']}")

    args: List[str] = []
    for item in dialogue + music + sfx:
        args += ["-i", str(item["path"])]
    chains: List[str] = []
    buses = []
    offset = 0
    dia = mus = None
    if dialogue:
        dia = _bus(dialogue, offset, "dia", chains)
        offset += len(dialogue)
    if music:
        mus = _bus(music, offset, "mus", chains)
        offset += len(music)
    if sfx:
        buses.append(_bus(sfx, offset, "sfx", chains))
    if dia and mus and duck:
        chains.append(f"{dia}asplit=2[diamix][diakey]")
        chains.append(f"{mus}[diakey]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[musduck]")
        buses = ["[diamix]", "[musduck]"] + buses
    else:
        buses = [b for b in (dia, mus) if b] + buses
    if len(buses) == 1:
        chains.append(f"{buses[0]}anull[pre]")
    else:
        chains.append(f"{''.join(buses)}amix=inputs={len(buses)}:normalize=0:dropout_transition=0[pre]")
    chains.append(
        f"[pre]apad,atrim=0:{float(duration_s):.3f},"
        f"loudnorm=I={loudness_lufs}:TP={true_peak}:LRA=11,aresample=48000[out]"
    )
    run(args + ["-filter_complex", ";".join(chains), "-map", "[out]", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", str(ensure_parent(out))])
    return Path(out)
