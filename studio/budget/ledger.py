"""Append-only spending ledger per episode project.

Stored at ``<project>/00_admin/budget/ledger.jsonl`` (one JSON object per
line, never rewritten). Entries:

* ``session`` — a rented GPU session: start/end, GPU type -> money
* ``job``     — one generation job: stage, GPU seconds, shot, attempt
* ``manual``  — anything else paid for (stock, a font, a service)

Money is derived from sessions and manual entries (that is what you are
billed for). Job entries measure throughput for calibration.
"""

from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.budget.estimate import money
from studio.common import StudioError, now_iso


class Ledger:
    def __init__(self, project_root: Path, config: Dict[str, Any]):
        self.project_root = Path(project_root)
        self.config = config
        self.path = self.project_root / "00_admin" / "budget" / "ledger.jsonl"

    # ---------------------------------------------------------------- io
    def entries(self) -> List[Dict[str, Any]]:
        if not self.path.is_file():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
        return out

    def _append(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        entry = dict(entry)
        entry.setdefault("ts", now_iso())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    # ----------------------------------------------------------- record
    def log_session(self, gpu: str, seconds: float, note: str = "") -> Dict[str, Any]:
        if seconds <= 0:
            raise StudioError("Session length must be positive.")
        cost = money(seconds, self.config, gpu)
        return self._append({"kind": "session", "gpu": gpu, "seconds": round(seconds, 1), "cost_inc_gst": cost["inc_gst"], "note": note})

    def log_job(self, stage: str, gpu_seconds: float, gpu: str = None, shot_id: str = None, attempt: int = 1, unit: str = None, units: float = 1.0, note: str = "") -> Dict[str, Any]:
        return self._append(
            {
                "kind": "job",
                "stage": stage,
                "unit": unit or stage,
                "units": units,
                "gpu": gpu or self.config.get("budget", {}).get("default_gpu"),
                "gpu_seconds": round(gpu_seconds, 2),
                "shot_id": shot_id,
                "attempt": attempt,
                "note": note,
            }
        )

    def log_manual(self, amount_inc_gst: float, note: str) -> Dict[str, Any]:
        return self._append({"kind": "manual", "cost_inc_gst": round(float(amount_inc_gst), 2), "note": note})

    # ----------------------------------------------------------- report
    def spent(self) -> float:
        return round(sum(float(e.get("cost_inc_gst", 0)) for e in self.entries() if e.get("kind") in {"session", "manual"}), 2)

    def cap(self) -> float:
        return float(self.config.get("budget", {}).get("per_episode_cap", 0) or 0)

    def remaining(self) -> float:
        return round(self.cap() - self.spent(), 2)

    def guard(self, projected_inc_gst: float) -> None:
        """Raise if the next spend would exceed the episode cap."""
        cap = self.cap()
        if cap and self.spent() + projected_inc_gst > cap:
            raise StudioError(
                f"Budget guard: spent ₹{self.spent():.0f} + next ₹{projected_inc_gst:.0f} exceeds the episode cap ₹{cap:.0f}. "
                "Simplify shots (hold/camera instead of full motion), or raise budget.per_episode_cap deliberately."
            )

    def report(self) -> Dict[str, Any]:
        entries = self.entries()
        by_stage: Dict[str, float] = defaultdict(float)
        for entry in entries:
            if entry.get("kind") == "job":
                by_stage[entry["stage"]] += float(entry.get("gpu_seconds", 0))
        return {
            "spent_inc_gst": self.spent(),
            "cap": self.cap(),
            "remaining": self.remaining(),
            "sessions": sum(1 for e in entries if e.get("kind") == "session"),
            "jobs": sum(1 for e in entries if e.get("kind") == "job"),
            "job_gpu_hours_by_stage": {k: round(v / 3600.0, 2) for k, v in sorted(by_stage.items())},
        }

    def calibrate(self, minimum_samples: int = 5) -> Dict[str, Any]:
        """Median measured GPU seconds per unit, per benchmark key.

        Only units with enough samples are reported; copy the result into
        ``budget.benchmarks_gpu_s`` so the next estimate uses reality.
        """
        samples: Dict[str, List[float]] = defaultdict(list)
        attempts: Dict[str, List[int]] = defaultdict(list)
        for entry in self.entries():
            if entry.get("kind") != "job":
                continue
            units = float(entry.get("units") or 1.0)
            if units > 0:
                samples[entry.get("unit") or entry["stage"]].append(float(entry["gpu_seconds"]) / units)
            if entry.get("shot_id"):
                attempts[entry["stage"]].append(int(entry.get("attempt") or 1))
        result: Dict[str, Any] = {"benchmarks_gpu_s": {}, "samples": {}, "max_attempt_by_stage": {}}
        for unit, values in samples.items():
            result["samples"][unit] = len(values)
            if len(values) >= minimum_samples:
                result["benchmarks_gpu_s"][unit] = round(statistics.median(values), 1)
        for stage, values in attempts.items():
            result["max_attempt_by_stage"][stage] = max(values)
        return result

    def latest(self, kind: Optional[str] = None) -> Optional[Dict[str, Any]]:
        for entry in reversed(self.entries()):
            if kind is None or entry.get("kind") == kind:
                return entry
        return None
