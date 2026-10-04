"""Estimate the GPU cost of an episode from its shot list.

All throughput numbers live in ``studio/config.yaml`` under
``budget.benchmarks_gpu_s``. They start as stated assumptions and are
replaced by measured medians via ``python -m studio budget calibrate``
once real jobs have been logged — that is part of the feedback loop.
"""

from __future__ import annotations

import math
from typing import Any, Dict

from studio.common import StudioError
from studio.series.shotlist import dialogue_lines, iter_shots, summarize

DEFAULTS = {
    "keyframe_image": 20,
    "keyframe_candidates": 4,
    "keyframe_edit": 60,
    "keyframe_edit_fraction": 0.5,
    "video_5s_720p": 540,
    "mouth_variant": 30,
    "mouth_shapes": 6,
    "tts_line": 4,
    "stt_minute": 30,
    "music_minute": 60,
    "music_fraction": 0.6,
    "upscale_interp_minute": 240,
    "identity_check_image": 1,
    "lora_training": 2700,
}


def _budget_config(config: Dict[str, Any]) -> Dict[str, Any]:
    budget = config.get("budget")
    if not budget:
        raise StudioError("studio/config.yaml has no 'budget' section.")
    return budget


def gpu_rate(config: Dict[str, Any], gpu: str = None) -> float:
    budget = _budget_config(config)
    gpu = gpu or budget.get("default_gpu")
    rates = budget.get("gpu_rates_ex_gst") or {}
    if gpu not in rates:
        raise StudioError(f"No hourly rate for GPU '{gpu}' in budget.gpu_rates_ex_gst.")
    return float(rates[gpu])


def money(gpu_seconds: float, config: Dict[str, Any], gpu: str = None) -> Dict[str, float]:
    budget = _budget_config(config)
    rate = gpu_rate(config, gpu)
    ex_gst = gpu_seconds / 3600.0 * rate
    inc_gst = ex_gst * (1.0 + float(budget.get("gst_rate", 0.18)))
    return {"gpu_hours": round(gpu_seconds / 3600.0, 2), "ex_gst": round(ex_gst, 2), "inc_gst": round(inc_gst, 2)}


def estimate_episode(shotlist: Dict[str, Any], config: Dict[str, Any], languages=None, gpu: str = None) -> Dict[str, Any]:
    budget = _budget_config(config)
    bench = dict(DEFAULTS)
    bench.update(budget.get("benchmarks_gpu_s") or {})
    retry_video = float(budget.get("retry_factor_video", 2.5))
    retry_image = float(budget.get("retry_factor_image", 1.5))
    languages = list(languages or ["en"])

    summary = summarize(shotlist)
    shots = list(iter_shots(shotlist))
    lines = {lang: len(dialogue_lines(shotlist, lang)) for lang in languages}

    stages: Dict[str, float] = {}
    stages["keyframes"] = len(shots) * bench["keyframe_candidates"] * bench["keyframe_image"] * retry_image
    stages["keyframe_edits"] = len(shots) * bench["keyframe_edit_fraction"] * bench["keyframe_edit"] * retry_image

    clips = 0
    talking_limited = 0
    for shot in shots:
        seconds = float(shot.get("duration_s") or 0)
        if shot.get("motion") == "full":
            clips += max(1, math.ceil(seconds / 5.0))
        if shot.get("motion") == "limited" and shot.get("dialogue"):
            talking_limited += 1
    stages["video_generation"] = clips * bench["video_5s_720p"] * retry_video
    stages["mouth_shapes"] = talking_limited * bench["mouth_shapes"] * bench["mouth_variant"] * retry_image
    stages["voice_tts"] = sum(lines.values()) * bench["tts_line"] * retry_image
    stages["music"] = summary["runtime_min"] * bench["music_fraction"] * bench["music_minute"]
    full_minutes = summary["by_motion"]["full"]["seconds"] / 60.0
    stages["upscale_interpolate"] = full_minutes * bench["upscale_interp_minute"]
    # QC runs on the laptop CPU (free, but takes wall time): reported, not charged.
    laptop = {
        "dialogue_qc_stt": summary["runtime_min"] * len(languages) * bench["stt_minute"],
        "identity_qc": len(shots) * bench["keyframe_candidates"] * bench["identity_check_image"],
    }
    sessions = int(budget.get("sessions_per_episode", 4))
    stages["session_overhead"] = sessions * float(budget.get("session_overhead_min", 20)) * 60.0

    gpu_seconds = sum(stages.values())
    cost = money(gpu_seconds, config, gpu)
    margin = float(budget.get("safety_margin", 0.15))
    with_margin = round(cost["inc_gst"] * (1.0 + margin), 2)
    cap = float(budget.get("per_episode_cap", 0) or 0)

    return {
        "gpu": gpu or budget.get("default_gpu"),
        "rate_ex_gst_per_hour": gpu_rate(config, gpu),
        "summary": summary,
        "dialogue_lines": lines,
        "video_clips_5s": clips,
        "stages_gpu_hours": {k: round(v / 3600.0, 2) for k, v in stages.items()},
        "laptop_hours_not_charged": {k: round(v / 3600.0, 2) for k, v in laptop.items()},
        "gpu_hours": cost["gpu_hours"],
        "cost_ex_gst": cost["ex_gst"],
        "cost_inc_gst": cost["inc_gst"],
        "cost_with_margin": with_margin,
        "cap": cap,
        "within_cap": (with_margin <= cap) if cap else None,
        "assumptions": "benchmarks are assumptions until calibrated from logged jobs",
    }


def estimate_season_setup(characters: int, config: Dict[str, Any], gpu: str = None) -> Dict[str, Any]:
    """One-time cost: one LoRA per recurring character."""
    bench = dict(DEFAULTS)
    bench.update(_budget_config(config).get("benchmarks_gpu_s") or {})
    seconds = characters * bench["lora_training"]
    result = money(seconds, config, gpu)
    result["characters"] = characters
    return result
