"""The anime episode pipeline: stages, gates and episode timelines.

Every stage names the skill (department) that owns it, where it runs,
how automated it is, and the gate it must pass. ``status`` inspects the
episode folders to show what is done, so ``python -m studio pipeline
status <series> <n>`` always reflects reality, not memory.

Automation levels:
    auto    runs unattended once inputs exist
    assist  Claude drafts, the owner approves (creative decisions)
    gate    a hard check that blocks the next stage on failure
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.series.shotlist import dialogue_lines, iter_shots


@dataclass(frozen=True)
class Stage:
    key: str
    title: str
    skill: str
    runs_on: str  # laptop | gridshare | claude
    automation: str  # auto | assist | gate
    command: str
    done_when: str  # relative path pattern inside the episode or project


STAGES: List[Stage] = [
    Stage("story", "Episode outline & script", "writer", "claude", "assist", "Claude: writer skill -> episodes/EXX/script.md", "episode:script.md"),
    Stage("direction", "Director's treatment (scene intent, tone, action beats)", "director", "claude", "assist", "Claude: director + action-direction skills", "episode:treatment.md"),
    Stage("shotlist", "Compile shot list from script", "shot-compiler", "claude", "assist", "Claude: shot-compiler skill -> shotlist.json", "episode:shotlist.json"),
    Stage("validate", "Validate shot list against the bible", "continuity", "laptop", "gate", "python -m studio shots check <series> <n>", "project:20_qc/shotlist_check.json"),
    Stage("legal_scan", "Scan script & prompts for third-party IP", "legal-rights", "laptop", "gate", "python -m studio legal scan <series> <n>", "project:19_legal-rights/content_scan.json"),
    Stage("estimate", "GPU budget estimate vs cap", "producer", "laptop", "gate", "python -m studio estimate <series> <n>", "project:00_admin/budget/estimate.json"),
    Stage("voice", "Generate all dialogue (every language)", "sound", "gridshare", "auto", "python -m studio voice <series> <n> --execute", "project:14_sound/dialogue"),
    Stage("voice_qc", "Dialogue QC: speech-to-text vs script, peaks", "qc", "laptop", "gate", "feedback loop: voice_line", "project:20_qc/feedback/journal.jsonl"),
    Stage("timing", "Lock shot timing to recorded dialogue", "editor", "laptop", "auto", "python -m studio timing <series> <n>", "project:12_edit/timeline.json"),
    Stage("layout", "Blender layout / blocking renders", "storyboard-previs", "laptop", "assist", "Blender MCP with Claude, then integrations.blender.adapter", "project:07_storyboard-previs/layout"),
    Stage("keyframes", "Keyframes per shot (checkpoint + LoRA + control)", "ai-generation", "gridshare", "auto", "ComfyUI keyframe workflow via quality loop", "project:09_ai-generation/keyframes"),
    Stage("keyframe_qc", "Identity, palette, provenance QC + owner approval", "continuity", "laptop", "gate", "feedback loop: keyframe; review queue", "project:09_ai-generation/selected"),
    Stage("motion", "Motion: camera moves (CPU) and full AI video (GPU)", "animation", "gridshare", "auto", "edit.camera for hold/camera; ComfyUI video workflow for full", "project:10_animation/clips"),
    Stage("lipsync", "Mouth shapes + Rhubarb timing for talking shots", "performance", "laptop", "auto", "lipsync.rhubarb + lipsync.compose", "project:10_animation/clips"),
    Stage("motion_graphics", "Titles, cards, lower thirds", "vfx-motion", "laptop", "auto", "integrations.motion_graphics.adapter (Remotion)", "project:13_vfx-motion/titles"),
    Stage("music", "Score: theme library + episode cues, SFX", "music", "gridshare", "assist", "integrations.music.adapter", "project:15_music/cues"),
    Stage("edit", "Assemble picture from EDL", "editor", "laptop", "auto", "integrations.edit.assemble", "project:12_edit/picture.mp4"),
    Stage("mix", "Mix per language, -14 LUFS", "sound", "laptop", "auto", "integrations.edit.mix", "project:14_sound/mix"),
    Stage("subtitles", "SRT per language", "distribution", "laptop", "auto", "integrations.edit.subtitles", "project:21_distribution/subtitles"),
    Stage("master_qc", "Master QC (tech, loudness, black frames) + owner viewing", "qc", "laptop", "gate", "feedback loop: master", "project:20_qc/master_qc.json"),
    Stage("release_gate", "Release gate: provenance + licenses + disclosure", "legal-rights", "laptop", "gate", "python -m studio legal release-gate <series> <n>", "project:19_legal-rights/release_gate.json"),
    Stage("package", "Package master (audio tracks, subtitles, metadata)", "distribution", "laptop", "auto", "integrations.edit.package", "project:21_distribution/master"),
    Stage("review", "Episode review: ratings, calibration, lessons", "feedback-loop", "claude", "assist", "python -m studio qc report / calibrate; lessons", "project:23_knowledge/lessons.md"),
]


def _exists(spec: str, episode_dir: Path, project_dir: Optional[Path]) -> bool:
    scope, _, rel = spec.partition(":")
    base = episode_dir if scope == "episode" else project_dir
    if base is None:
        return False
    path = Path(base) / rel
    if path.is_dir():
        return any(p for p in path.rglob("*") if p.is_file() and not p.name.startswith("."))
    if path.is_file():
        if path.name == "shotlist.json":
            return '"visual_prompt": ""' not in path.read_text(encoding="utf-8") and "SC01" in path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            return "TODO" not in path.read_text(encoding="utf-8")
        return path.stat().st_size > 0
    return False


def status(episode_dir: Path, project_dir: Optional[Path]) -> List[Dict[str, Any]]:
    rows = []
    for number, stage in enumerate(STAGES, start=1):
        rows.append(
            {
                "n": number,
                "stage": stage.key,
                "title": stage.title,
                "skill": stage.skill,
                "runs_on": stage.runs_on,
                "automation": stage.automation,
                "done": _exists(stage.done_when, Path(episode_dir), project_dir),
                "command": stage.command,
            }
        )
    return rows


def next_stage(rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for row in rows:
        if not row["done"]:
            return row
    return None


# ------------------------------------------------------------- timeline
def shot_starts(shotlist: Dict[str, Any]) -> Dict[str, float]:
    starts, t = {}, 0.0
    for shot in iter_shots(shotlist):
        starts[shot["id"]] = round(t, 3)
        t += float(shot.get("duration_s") or 0)
    return starts


def dialogue_timeline(shotlist: Dict[str, Any], language: str, line_durations: Dict[str, float], lead_in_s: float = 0.25, gap_s: float = 0.2) -> List[Dict[str, Any]]:
    """Place each recorded line inside its shot.

    ``line_durations``: measured length of each generated line (seconds).
    Lines in a shot play back to back after a short lead-in. If a shot is
    too short for its lines, the overflow is reported so the ``timing``
    stage can lengthen the shot (picture follows dialogue in animation).
    """
    starts = shot_starts(shotlist)
    durations = {shot["id"]: float(shot.get("duration_s") or 0) for shot in iter_shots(shotlist)}
    cursor: Dict[str, float] = {}
    timeline = []
    for line in dialogue_lines(shotlist, language):
        shot_id = line["shot_id"]
        length = float(line_durations.get(line["line_id"], 0.0))
        local = cursor.get(shot_id, lead_in_s)
        start = starts[shot_id] + local
        end = start + length
        overflow = max(0.0, local + length - durations[shot_id])
        timeline.append({**line, "start_s": round(start, 3), "end_s": round(end, 3), "overflow_s": round(overflow, 3)})
        cursor[shot_id] = local + length + gap_s
    return timeline


def retime_shots(shotlist: Dict[str, Any], timeline: List[Dict[str, Any]], tail_s: float = 0.4) -> Dict[str, float]:
    """New duration per shot so every line fits (only ever lengthens)."""
    need: Dict[str, float] = {}
    starts = shot_starts(shotlist)
    for item in timeline:
        local_end = item["end_s"] - starts[item["shot_id"]] + tail_s
        need[item["shot_id"]] = max(need.get(item["shot_id"], 0.0), local_end)
    changes = {}
    for shot in iter_shots(shotlist):
        current = float(shot.get("duration_s") or 0)
        wanted = need.get(shot["id"], 0.0)
        if wanted > current + 1e-6:
            # whole frames at 24 fps, rounded UP so the last syllable is never cut
            changes[shot["id"]] = math.ceil(wanted * 24 - 1e-9) / 24
    return changes


def build_edl(shotlist: Dict[str, Any], clip_for_shot: Dict[str, str], fps: int = 24, resolution: str = "1920x1080") -> Dict[str, Any]:
    clips, missing = [], []
    for shot in iter_shots(shotlist):
        path = clip_for_shot.get(shot["id"])
        if not path:
            missing.append(shot["id"])
            continue
        clips.append({"shot_id": shot["id"], "path": path, "duration_s": float(shot["duration_s"])})
    return {"fps": fps, "resolution": resolution, "clips": clips, "missing": missing}
