"""The quality loop: generate -> measure -> decide -> adjust -> repeat.

    attempt 1: generate(params) -> checks -> FAIL identity 0.71 < 0.80
               adjust: new seed, LoRA weight +0.1, reference strength +0.1
    attempt 2: generate(params) -> checks -> all required pass -> APPROVE

Decisions:

* ``approve``      every required check passed (none skipped)
* ``retry``        a retryable check failed and attempts/budget remain
* ``human_review`` required check skipped/errored, a non-retryable check
                   failed (tech/legal = pipeline problem, not bad luck),
                   or attempts/budget ran out
* ``reject``       a legal check failed: never auto-retried

Every attempt goes to ``<project>/20_qc/feedback/journal.jsonl`` and
human-review items to ``review_queue.json``. Human ratings recorded with
``python -m studio qc rate`` feed the threshold calibration in
``studio.feedback.review``.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from studio.common import StudioError, dump_json, load_json, now_iso
from studio.feedback.checks import ERROR, FAIL, SKIP, CheckResult, run_checks

APPROVE, RETRY, HUMAN, REJECT = "approve", "retry", "human_review", "reject"

DEFAULT_REQUIRED = {
    "keyframe": ["tech_image", "provenance", "identity", "palette"],
    "video": ["tech_video", "provenance", "identity", "flicker", "black_frames"],
    "voice_line": ["voice_peak", "dialogue_accuracy", "provenance"],
    "music": ["provenance"],
    "master": ["tech_video", "loudness", "black_frames"],
}
DEFAULT_MAX_ATTEMPTS = {"keyframe": 4, "video": 3, "voice_line": 3, "music": 2, "master": 1}
NON_RETRYABLE = {"tech_video", "tech_image", "loudness"}
LEGAL = {"provenance"}

DEFAULT_ADJUSTMENTS = {
    "identity": {"new_seed": True, "lora_weight": 0.1, "reference_strength": 0.1},
    "palette": {"new_seed": True, "palette_emphasis": 0.1},
    "flicker": {"new_seed": True, "motion_strength": -0.1},
    "dialogue_accuracy": {"new_seed": True, "speed": -0.05},
    "voice_peak": {"gain_db": -3.0},
}
PARAM_LIMITS = {
    "lora_weight": (0.4, 1.3),
    "reference_strength": (0.2, 1.0),
    "palette_emphasis": (0.0, 0.6),
    "motion_strength": (0.2, 1.0),
    "speed": (0.8, 1.2),
    "gain_db": (-12.0, 0.0),
}


@dataclass
class Verdict:
    kind: str
    asset: str
    attempt: int
    decision: str
    reasons: List[str]
    results: List[CheckResult] = field(default_factory=list)

    @property
    def failed(self) -> List[str]:
        return [r.name for r in self.results if r.status == FAIL]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "asset": self.asset,
            "attempt": self.attempt,
            "decision": self.decision,
            "reasons": self.reasons,
            "results": [r.as_dict() for r in self.results],
        }


class QualityLoop:
    def __init__(self, project_root: Path, config: Dict[str, Any], ledger=None):
        self.project_root = Path(project_root)
        self.config = config
        self.ledger = ledger
        feedback = config.get("feedback") or {}
        self.required = {**DEFAULT_REQUIRED, **(feedback.get("required_checks") or {})}
        self.max_attempts = {**DEFAULT_MAX_ATTEMPTS, **(feedback.get("max_attempts") or {})}
        self.adjustments = {**DEFAULT_ADJUSTMENTS, **(feedback.get("retry_adjustments") or {})}
        self.auto_approve = bool(feedback.get("auto_approve", True))
        self.folder = self.project_root / "20_qc" / "feedback"

    # ------------------------------------------------------------ decide
    def evaluate(self, asset: Path, kind: str, ctx: Dict[str, Any], attempt: int = 1) -> Verdict:
        if kind not in self.required:
            raise StudioError(f"Unknown asset kind '{kind}'. Known: {sorted(self.required)}")
        ctx = {"config": self.config, **ctx}
        results = run_checks(list(self.required[kind]), Path(asset), ctx)
        decision, reasons = self._decide(kind, results, attempt)
        verdict = Verdict(kind, str(asset), attempt, decision, reasons, results)
        self._journal(verdict, ctx)
        return verdict

    def _decide(self, kind: str, results: List[CheckResult], attempt: int):
        failed = [r for r in results if r.status == FAIL]
        unmeasured = [r for r in results if r.status in {SKIP, ERROR}]
        if any(r.name in LEGAL for r in failed):
            return REJECT, [f"{r.name}: {r.detail}" for r in failed if r.name in LEGAL]
        if failed:
            reasons = [f"{r.name}: {r.detail}" for r in failed]
            if any(r.name in NON_RETRYABLE for r in failed):
                return HUMAN, reasons + ["technical failure: fix the pipeline, not the seed"]
            if attempt >= int(self.max_attempts.get(kind, 3)):
                return HUMAN, reasons + [f"still failing after {attempt} attempts"]
            return RETRY, reasons
        if unmeasured:
            return HUMAN, [f"{r.name} not measured: {r.detail}" for r in unmeasured]
        if not self.auto_approve:
            return HUMAN, ["auto_approve is off"]
        return APPROVE, ["all required checks passed"]

    # ------------------------------------------------------------ adjust
    def adjust(self, params: Dict[str, Any], verdict: Verdict, rng: Optional[random.Random] = None) -> Dict[str, Any]:
        """Next attempt's parameters, driven by which checks failed."""
        rng = rng or random.Random()
        nxt = dict(params)
        for name in verdict.failed:
            for key, delta in (self.adjustments.get(name) or {}).items():
                if key == "new_seed":
                    if delta:
                        nxt["seed"] = rng.randrange(0, 2**32 - 1)
                    continue
                base = float(nxt.get(key, 1.0 if key in {"lora_weight", "speed", "motion_strength"} else 0.5 if key == "reference_strength" else 0.0))
                low, high = PARAM_LIMITS.get(key, (-1e9, 1e9))
                nxt[key] = round(min(high, max(low, base + float(delta))), 3)
        nxt["_attempt_reason"] = verdict.failed
        return nxt

    # --------------------------------------------------------------- run
    def run(
        self,
        kind: str,
        generate: Callable[[Dict[str, Any], int], Path],
        ctx: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
        cost_per_attempt_inc_gst: float = 0.0,
        rng: Optional[random.Random] = None,
    ) -> Verdict:
        """Generate until approved, rejected or handed to a human."""
        params = dict(params or {})
        params.setdefault("seed", (rng or random.Random()).randrange(0, 2**32 - 1))
        attempt = 0
        while True:
            attempt += 1
            if self.ledger is not None and cost_per_attempt_inc_gst:
                try:
                    self.ledger.guard(cost_per_attempt_inc_gst)
                except StudioError as error:
                    verdict = Verdict(kind, "", attempt, HUMAN, [str(error)])
                    self._queue(verdict, ctx, params)
                    return verdict
            asset = generate(params, attempt)
            verdict = self.evaluate(asset, kind, ctx, attempt)
            if verdict.decision == RETRY:
                params = self.adjust(params, verdict, rng)
                continue
            if verdict.decision in {HUMAN, REJECT}:
                self._queue(verdict, ctx, params)
            return verdict

    # ------------------------------------------------------------ record
    def _journal(self, verdict: Verdict, ctx: Dict[str, Any]) -> None:
        self.folder.mkdir(parents=True, exist_ok=True)
        entry = verdict.as_dict()
        entry["ts"] = now_iso()
        entry["shot_id"] = (ctx.get("shot") or {}).get("id")
        with (self.folder / "journal.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")

    def _queue(self, verdict: Verdict, ctx: Dict[str, Any], params: Dict[str, Any]) -> None:
        path = self.folder / "review_queue.json"
        queue = load_json(path) if path.is_file() else []
        queue.append(
            {
                "ts": now_iso(),
                "status": "open",
                "decision": verdict.decision,
                "kind": verdict.kind,
                "asset": verdict.asset,
                "shot_id": (ctx.get("shot") or {}).get("id"),
                "attempt": verdict.attempt,
                "reasons": verdict.reasons,
                "last_params": {k: v for k, v in params.items() if not k.startswith("_")},
            }
        )
        dump_json(queue, path)


def journal_entries(project_root: Path) -> List[Dict[str, Any]]:
    path = Path(project_root) / "20_qc" / "feedback" / "journal.jsonl"
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
