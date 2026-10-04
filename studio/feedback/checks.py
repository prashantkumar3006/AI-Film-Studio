"""Automated QC checks.

Each check takes an asset path and a context dict and returns a
``CheckResult``. Status meanings:

* ``pass``  — measured and within threshold
* ``fail``  — measured and outside threshold (retry or fix)
* ``skip``  — could not be measured here (tool not installed, no
  reference). A skipped *required* check never counts as a pass: the
  asset goes to human review instead of being auto-approved.
* ``error`` — the check itself crashed (treated like skip, and logged)

Context keys used (all optional): ``config``, ``bible``, ``shot``,
``characters`` (ids), ``expected_text``, ``language``, ``transcribe``
(callable path -> text), ``identity_scorer`` (callable image, reference
-> similarity 0..1), ``palette`` (list of #RRGGBB), ``catalogue``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from studio.feedback import media
from studio.feedback.text import dialogue_error

PASS, FAIL, SKIP, ERROR = "pass", "fail", "skip", "error"


@dataclass
class CheckResult:
    name: str
    status: str
    score: Optional[float] = None
    threshold: Optional[float] = None
    detail: str = ""
    data: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "score": self.score,
            "threshold": self.threshold,
            "detail": self.detail,
            "data": self.data,
        }


def _thresholds(ctx: Dict[str, Any]) -> Dict[str, Any]:
    return ((ctx.get("config") or {}).get("feedback") or {}).get("thresholds") or {}


def _render(ctx: Dict[str, Any]) -> Dict[str, Any]:
    return (ctx.get("config") or {}).get("render") or {}


# ---------------------------------------------------------------- technical
def check_tech_video(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    info = media.probe(asset)
    video = info.get("video")
    if not video:
        return CheckResult("tech_video", FAIL, detail="no video stream")
    problems = []
    want = str(_render(ctx).get("resolution", "1920x1080"))
    allowed = {want} | set(str(r) for r in (_thresholds(ctx).get("allowed_intermediate_resolutions") or []))
    got = f"{video['width']}x{video['height']}"
    if got not in allowed:
        problems.append(f"resolution {got} not in {sorted(allowed)}")
    fps = float(_render(ctx).get("fps", 24))
    if video.get("fps") and abs(video["fps"] - fps) > 0.01:
        problems.append(f"fps {video['fps']} != {fps}")
    shot = ctx.get("shot") or {}
    expected = shot.get("duration_s")
    tolerance = float(_thresholds(ctx).get("duration_tolerance_s", 0.1))
    if expected and info.get("duration_s") is not None and abs(info["duration_s"] - float(expected)) > tolerance:
        problems.append(f"duration {info['duration_s']}s vs shot {expected}s")
    return CheckResult("tech_video", FAIL if problems else PASS, detail="; ".join(problems) or "ok", data=info)


def check_tech_image(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    info = media.probe(asset)
    video = info.get("video")
    if not video:
        return CheckResult("tech_image", FAIL, detail="not a readable image")
    min_h = int(_thresholds(ctx).get("min_image_height", 1024))
    ok = (video.get("height") or 0) >= min_h
    return CheckResult(
        "tech_image",
        PASS if ok else FAIL,
        score=video.get("height"),
        threshold=min_h,
        detail=f"{video['width']}x{video['height']}",
        data=info,
    )


# ------------------------------------------------------------------- audio
def check_loudness(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    audio_cfg = (ctx.get("config") or {}).get("audio") or {}
    target = float(audio_cfg.get("loudness_target_lufs", -14))
    max_peak = float(audio_cfg.get("true_peak_dbtp", -1.0))
    tolerance = float(_thresholds(ctx).get("loudness_tolerance_lu", 1.0))
    meas = media.loudness(asset)
    lufs, peak = meas.get("integrated_lufs"), meas.get("true_peak_dbtp")
    if lufs is None:
        return CheckResult("loudness", ERROR, detail="could not measure loudness", data=meas)
    problems = []
    if abs(lufs - target) > tolerance:
        problems.append(f"{lufs} LUFS vs target {target}±{tolerance}")
    if peak is not None and peak > max_peak + 0.1:
        problems.append(f"true peak {peak} dBTP > {max_peak}")
    return CheckResult("loudness", FAIL if problems else PASS, score=lufs, threshold=target, detail="; ".join(problems) or "ok", data=meas)


def check_voice_peak(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    """Individual voice lines: no clipping. Loudness is normalised later in the mix."""
    meas = media.loudness(asset)
    peak = meas.get("true_peak_dbtp")
    if peak is None:
        return CheckResult("voice_peak", ERROR, detail="could not measure peak", data=meas)
    limit = float(_thresholds(ctx).get("voice_max_peak_dbtp", -0.5))
    return CheckResult("voice_peak", PASS if peak <= limit else FAIL, score=peak, threshold=limit, detail=f"peak {peak} dBTP", data=meas)


def check_dialogue_accuracy(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    transcribe: Optional[Callable[[Path], str]] = ctx.get("transcribe")
    expected = ctx.get("expected_text")
    if not expected:
        return CheckResult("dialogue_accuracy", SKIP, detail="no expected text in context")
    if transcribe is None:
        return CheckResult("dialogue_accuracy", SKIP, detail="no speech-to-text configured (integrations: stt_faster_whisper)")
    language = ctx.get("language", "en")
    heard = transcribe(Path(asset), language)
    scores = dialogue_error(expected, heard, language)
    limits = _thresholds(ctx).get("dialogue_max_error") or {}
    limit = float(limits.get(language, 0.15 if language == "en" else 0.25))
    status = PASS if scores["error"] <= limit else FAIL
    return CheckResult("dialogue_accuracy", status, score=scores["error"], threshold=limit, detail=f"heard: {heard!r}", data=scores)


# ------------------------------------------------------------- consistency
def check_identity(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    scorer = ctx.get("identity_scorer")
    bible = ctx.get("bible")
    characters = ctx.get("characters") or []
    if not characters:
        return CheckResult("identity", PASS, detail="no characters in shot")
    if scorer is None:
        return CheckResult("identity", SKIP, detail="no identity scorer configured (integrations: identity_ccip)")
    if bible is None:
        return CheckResult("identity", SKIP, detail="no bible in context")
    default = float(_thresholds(ctx).get("identity_min_similarity", 0.80))
    worst, details, data = 1.0, [], {}
    for cid in characters:
        char = bible.characters.get(cid) or {}
        sheet = (char.get("references") or {}).get("model_sheet")
        if not sheet or not bible.reference_path(sheet).is_file():
            return CheckResult("identity", SKIP, detail=f"no model sheet for '{cid}'")
        similarity = float(scorer(Path(asset), bible.reference_path(sheet), cid))
        limit = float(char.get("identity_threshold", default))
        data[cid] = {"similarity": round(similarity, 3), "threshold": limit}
        details.append(f"{cid} {similarity:.2f}/{limit:.2f}")
        worst = min(worst, similarity - limit)
    return CheckResult("identity", PASS if worst >= 0 else FAIL, score=round(worst, 3), threshold=0.0, detail=", ".join(details), data=data)


def _hex_to_rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def check_palette(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    palette = ctx.get("palette") or []
    if not palette:
        return CheckResult("palette", SKIP, detail="no palette in context")
    try:
        from PIL import Image  # type: ignore
    except ImportError:
        return CheckResult("palette", SKIP, detail="Pillow not installed")
    image = Image.open(asset).convert("RGB")
    image.thumbnail((256, 256))
    quantized = image.quantize(colors=24)
    flat = quantized.getpalette() or []
    total = image.width * image.height
    min_share = float(_thresholds(ctx).get("palette_min_coverage", 0.005))
    # Only colours that actually cover part of the frame count; unused
    # palette slots would otherwise "match" anything.
    colors = [tuple(flat[i * 3 : i * 3 + 3]) for count, i in (quantized.getcolors() or []) if count / total >= min_share]
    if not colors:
        return CheckResult("palette", ERROR, detail="could not extract colours")
    tolerance = float(_thresholds(ctx).get("palette_max_distance", 48))
    matched = 0
    for hex_value in palette:
        target = _hex_to_rgb(hex_value)
        best = min(sum((a - b) ** 2 for a, b in zip(target, c)) ** 0.5 for c in colors)
        matched += best <= tolerance
    score = matched / len(palette)
    limit = float(_thresholds(ctx).get("palette_min_match", 0.6))
    return CheckResult("palette", PASS if score >= limit else FAIL, score=round(score, 3), threshold=limit, detail=f"{matched}/{len(palette)} palette colours present")


def check_flicker(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    """Per generated clip only: a single shot should not contain hard 'pops'.
    (On an edited master every cut is a legitimate spike, so masters use
    ``black_frames`` instead.)"""
    flick = media.flicker_score(asset)
    limit = float(_thresholds(ctx).get("flicker_max_spike_ratio", 6.0))
    bad = bool(flick["spike_ratio"]) and flick["spike_ratio"] > limit
    detail = f"frame-change spike {flick['spike_ratio']}x median" if bad else "ok"
    return CheckResult("flicker", FAIL if bad else PASS, score=flick["spike_ratio"], threshold=limit, detail=detail, data=flick)


def check_black_frames(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    blacks = media.black_segments(asset, float(_thresholds(ctx).get("black_min_seconds", 0.5)))
    allowed = (ctx.get("shot") or {}).get("allow_black") or ctx.get("allow_black")
    bad = bool(blacks) and not allowed
    return CheckResult("black_frames", FAIL if bad else PASS, score=float(len(blacks)), threshold=0.0, detail=f"{len(blacks)} black segment(s)" if blacks else "ok", data={"segments": blacks})


# ------------------------------------------------------------------- legal
def check_provenance(asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    from studio.legal.provenance import release_gate

    report = release_gate([asset], bible=ctx.get("bible"), catalogue=ctx.get("catalogue"))
    if report["passed"]:
        return CheckResult("provenance", PASS, detail="provenance recorded and every tool/model cleared")
    return CheckResult("provenance", FAIL, detail="; ".join(p["problem"] for p in report["problems"]), data=report)


CHECKS: Dict[str, Callable[[Path, Dict[str, Any]], CheckResult]] = {
    "tech_video": check_tech_video,
    "tech_image": check_tech_image,
    "loudness": check_loudness,
    "voice_peak": check_voice_peak,
    "dialogue_accuracy": check_dialogue_accuracy,
    "identity": check_identity,
    "palette": check_palette,
    "flicker": check_flicker,
    "black_frames": check_black_frames,
    "provenance": check_provenance,
}


def run_check(name: str, asset: Path, ctx: Dict[str, Any]) -> CheckResult:
    if name not in CHECKS:
        return CheckResult(name, ERROR, detail="unknown check")
    try:
        return CHECKS[name](Path(asset), ctx)
    except Exception as error:  # a crashing check must not crash the pipeline
        return CheckResult(name, ERROR, detail=f"{type(error).__name__}: {error}")


def run_checks(names: List[str], asset: Path, ctx: Dict[str, Any]) -> List[CheckResult]:
    return [run_check(name, asset, ctx) for name in names]
