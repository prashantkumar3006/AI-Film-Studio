"""Shot list: the machine-readable contract between script and pipeline.

``series/<slug>/episodes/EXX/shotlist.json`` is compiled from the script
(see the ``shot-compiler`` skill). Every downstream stage reads it:
voice, layout, keyframes, motion, lip sync, edit, QC and the estimator.

Motion types decide cost, so they are explicit per shot:

    hold     still keyframe                      (cheapest)
    camera   still keyframe + camera move        (pan / push / shake)
    limited  keyframe + mouth flaps / small loops (anime limited animation)
    full     AI video generation (image-to-video) (most expensive)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from studio.common import StudioError, load_json
from studio.series.bible import Bible, Issue

MOTION_TYPES = ("hold", "camera", "limited", "full")
CAMERA_MOVES = ("static", "push_in", "pull_out", "pan_left", "pan_right", "tilt_up", "tilt_down", "shake", "tracking", "orbit")
SHOT_ID = re.compile(r"^SC\d{2,3}_SH\d{3}$")
SCENE_ID = re.compile(r"^SC\d{2,3}$")

# Rough speaking rates used only to sanity-check that dialogue fits a shot.
WORDS_PER_SECOND = {"en": 2.6, "hi": 2.4}
MIN_SHOT_S = 0.5
MAX_SHOT_S = 20.0


def load_shotlist(path: Path) -> Dict[str, Any]:
    data = load_json(path)
    if not isinstance(data, dict) or not isinstance(data.get("scenes"), list):
        raise StudioError(f"{path} must be an object with a 'scenes' list.")
    return data


def iter_shots(shotlist: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for scene in shotlist.get("scenes", []):
        for shot in scene.get("shots", []):
            shot.setdefault("_scene", scene.get("id"))
            shot.setdefault("_location", scene.get("location"))
            yield shot


def shot_duration(shot: Dict[str, Any]) -> float:
    return float(shot.get("duration_s") or 0.0)


def dialogue_lines(shotlist: Dict[str, Any], language: str) -> List[Dict[str, Any]]:
    """Flatten dialogue for one language, in shot order, with stable line IDs."""
    lines: List[Dict[str, Any]] = []
    for shot in iter_shots(shotlist):
        for index, item in enumerate(shot.get("dialogue") or [], start=1):
            text = (item.get("line") or {}).get(language)
            if not text:
                continue
            lines.append(
                {
                    "line_id": f"{shot['id']}_L{index:02d}",
                    "shot_id": shot["id"],
                    "character": item.get("character"),
                    "emotion": item.get("emotion", "neutral"),
                    "text": text,
                    "language": language,
                }
            )
    return lines


def _word_count(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def summarize(shotlist: Dict[str, Any]) -> Dict[str, Any]:
    by_motion = {m: {"shots": 0, "seconds": 0.0} for m in MOTION_TYPES}
    total = 0.0
    shots = 0
    for shot in iter_shots(shotlist):
        shots += 1
        seconds = shot_duration(shot)
        total += seconds
        motion = shot.get("motion")
        if motion in by_motion:
            by_motion[motion]["shots"] += 1
            by_motion[motion]["seconds"] += seconds
    full_ratio = (by_motion["full"]["seconds"] / total) if total else 0.0
    return {
        "scenes": len(shotlist.get("scenes", [])),
        "shots": shots,
        "runtime_s": round(total, 2),
        "runtime_min": round(total / 60.0, 2),
        "by_motion": {k: {"shots": v["shots"], "seconds": round(v["seconds"], 2)} for k, v in by_motion.items()},
        "full_video_ratio": round(full_ratio, 3),
    }


def validate_shotlist(shotlist: Dict[str, Any], bible: Optional[Bible] = None) -> List[Issue]:
    issues: List[Issue] = []
    seen_shots = set()
    seen_scenes = set()
    languages = bible.languages if bible else []
    policy = (bible.series.get("animation_policy") or {}) if bible else {}

    for scene in shotlist.get("scenes", []):
        sid = scene.get("id")
        where = f"scene {sid}"
        if not SCENE_ID.match(str(sid or "")):
            issues.append(Issue("error", where, "scene id must look like SC01"))
        if sid in seen_scenes:
            issues.append(Issue("error", where, "duplicate scene id"))
        seen_scenes.add(sid)
        location = scene.get("location")
        if bible is not None:
            if not location:
                issues.append(Issue("error", where, "scene has no location"))
            elif location not in bible.locations:
                issues.append(Issue("error", where, f"location '{location}' is not in the bible"))
        if not scene.get("shots"):
            issues.append(Issue("error", where, "scene has no shots"))

        for shot in scene.get("shots", []):
            shid = shot.get("id")
            where = f"shot {shid}"
            if not SHOT_ID.match(str(shid or "")):
                issues.append(Issue("error", where, "shot id must look like SC01_SH001"))
            elif not str(shid).startswith(f"{sid}_"):
                issues.append(Issue("error", where, f"shot id must start with its scene id {sid}_"))
            if shid in seen_shots:
                issues.append(Issue("error", where, "duplicate shot id"))
            seen_shots.add(shid)

            motion = shot.get("motion")
            if motion not in MOTION_TYPES:
                issues.append(Issue("error", where, f"motion must be one of {MOTION_TYPES}"))

            seconds = shot_duration(shot)
            if not (MIN_SHOT_S <= seconds <= MAX_SHOT_S):
                issues.append(Issue("error", where, f"duration_s={seconds} outside {MIN_SHOT_S}-{MAX_SHOT_S}s"))
            if motion == "full" and seconds > 5.0:
                issues.append(Issue("warning", where, "full-motion shots over 5 s need chained generations (cost x2+)"))

            camera = shot.get("camera") or {}
            move = camera.get("move", "static")
            if move not in CAMERA_MOVES:
                issues.append(Issue("error", where, f"camera.move '{move}' not in {CAMERA_MOVES}"))
            if motion == "camera" and move == "static":
                issues.append(Issue("warning", where, "motion 'camera' with a static camera: use 'hold'"))

            if not shot.get("visual_prompt"):
                issues.append(Issue("error", where, "missing visual_prompt"))

            present = set()
            for char in shot.get("characters") or []:
                cid = char.get("id") if isinstance(char, dict) else char
                present.add(cid)
                if bible is None:
                    continue
                if cid not in bible.characters:
                    issues.append(Issue("error", where, f"character '{cid}' is not in the bible"))
                    continue
                outfit = char.get("outfit", "default") if isinstance(char, dict) else "default"
                if outfit not in (bible.characters[cid].get("outfits") or {}):
                    issues.append(Issue("error", where, f"outfit '{outfit}' not defined for '{cid}'"))

            spoken = 0.0
            for item in shot.get("dialogue") or []:
                speaker = item.get("character")
                if speaker and speaker not in present and speaker != "narrator":
                    issues.append(Issue("warning", where, f"'{speaker}' speaks but is not listed in characters (off-screen?)"))
                line = item.get("line") or {}
                for lang in languages:
                    if not line.get(lang):
                        issues.append(Issue("error", where, f"dialogue missing '{lang}' text"))
                for lang, text in line.items():
                    rate = WORDS_PER_SECOND.get(lang, 2.5)
                    spoken = max(spoken, _word_count(str(text)) / rate)
            if spoken and seconds and spoken > seconds * 1.15:
                issues.append(
                    Issue("warning", where, f"dialogue needs ~{spoken:.1f}s but shot is {seconds:.1f}s: lengthen or split")
                )

    summary = summarize(shotlist)
    target = (bible.format.get("episode_minutes") if bible else None) or shotlist.get("target_minutes")
    if target:
        runtime = summary["runtime_min"]
        if abs(runtime - float(target)) > float(target) * 0.1:
            issues.append(Issue("warning", "episode", f"runtime {runtime} min vs target {target} min (>10% off)"))
    max_full = policy.get("max_full_video_ratio")
    if max_full is not None and summary["full_video_ratio"] > float(max_full):
        issues.append(
            Issue(
                "error",
                "episode",
                f"full AI video is {summary['full_video_ratio']:.0%} of runtime; policy limit is {float(max_full):.0%}",
            )
        )
    return issues
