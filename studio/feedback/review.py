"""Episode-level feedback: human ratings, QC report, threshold calibration
and lessons learned.

The automated checks are only as good as their thresholds. Humans rate a
sample of approved and rejected assets (1-5). Calibration compares the
check scores of assets humans liked with those they did not, and
proposes a threshold between them. Over episodes the machine judgement
converges on the owner's taste — that is the self-improving part.
"""

from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

from studio.common import StudioError, now_iso
from studio.feedback.loop import journal_entries

# Higher score = better for these checks; the rest are "lower is better".
HIGHER_IS_BETTER = {"identity", "palette", "tech_image"}


def ratings_path(project_root: Path) -> Path:
    return Path(project_root) / "20_qc" / "feedback" / "ratings.jsonl"


def rate(project_root: Path, asset: str, score: int, note: str = "", rater: str = "owner") -> Dict[str, Any]:
    if not 1 <= int(score) <= 5:
        raise StudioError("Rating must be 1-5.")
    entry = {"ts": now_iso(), "asset": asset, "score": int(score), "note": note, "rater": rater}
    path = ratings_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def ratings(project_root: Path) -> List[Dict[str, Any]]:
    path = ratings_path(project_root)
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def episode_report(project_root: Path) -> Dict[str, Any]:
    entries = journal_entries(project_root)
    decisions = Counter(e["decision"] for e in entries)
    check_status: Dict[str, Counter] = defaultdict(Counter)
    failures: Counter = Counter()
    attempts_per_shot: Dict[str, int] = defaultdict(int)
    for entry in entries:
        for result in entry.get("results", []):
            check_status[result["name"]][result["status"]] += 1
            if result["status"] == "fail":
                failures[result["name"]] += 1
        if entry.get("shot_id"):
            key = f"{entry['shot_id']}:{entry['kind']}"
            attempts_per_shot[key] = max(attempts_per_shot[key], int(entry.get("attempt", 1)))
    rated = ratings(project_root)
    first_pass = sum(1 for v in attempts_per_shot.values() if v == 1)
    return {
        "attempts": len(entries),
        "decisions": dict(decisions),
        "checks": {name: dict(counter) for name, counter in sorted(check_status.items())},
        "top_failures": failures.most_common(5),
        "assets_tracked": len(attempts_per_shot),
        "first_pass_rate": round(first_pass / len(attempts_per_shot), 3) if attempts_per_shot else None,
        "mean_attempts": round(statistics.mean(attempts_per_shot.values()), 2) if attempts_per_shot else None,
        "human_ratings": len(rated),
        "mean_rating": round(statistics.mean(r["score"] for r in rated), 2) if rated else None,
    }


def calibrate_thresholds(project_root: Path, minimum_each: int = 3) -> Dict[str, Any]:
    """Suggest thresholds from human ratings (good >= 4, bad <= 2).

    Only suggests when there are enough good and bad samples and the two
    groups actually separate; otherwise it says why not.
    """
    scores_by_asset: Dict[str, Dict[str, float]] = defaultdict(dict)
    for entry in journal_entries(project_root):
        for result in entry.get("results", []):
            if result.get("score") is not None:
                scores_by_asset[entry["asset"]][result["name"]] = float(result["score"])
    good: Dict[str, List[float]] = defaultdict(list)
    bad: Dict[str, List[float]] = defaultdict(list)
    for item in ratings(project_root):
        for check, value in scores_by_asset.get(item["asset"], {}).items():
            if item["score"] >= 4:
                good[check].append(value)
            elif item["score"] <= 2:
                bad[check].append(value)
    suggestions: Dict[str, Any] = {}
    for check in sorted(set(good) | set(bad)):
        g, b = good.get(check, []), bad.get(check, [])
        if len(g) < minimum_each or len(b) < minimum_each:
            suggestions[check] = {"status": "need more ratings", "good": len(g), "bad": len(b)}
            continue
        g_med, b_med = statistics.median(g), statistics.median(b)
        separates = g_med > b_med if check in HIGHER_IS_BETTER else g_med < b_med
        if not separates:
            suggestions[check] = {
                "status": "check does not predict human judgement",
                "good_median": g_med,
                "bad_median": b_med,
                "action": "improve or replace this metric",
            }
            continue
        suggestions[check] = {"status": "suggest", "threshold": round((g_med + b_med) / 2.0, 3), "good_median": g_med, "bad_median": b_med}
    return suggestions


def add_lesson(project_root: Path, lesson: str, area: str, action: str = "") -> Path:
    """Append a lesson to the project's knowledge folder (human readable)."""
    path = Path(project_root) / "23_knowledge" / "lessons.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", encoding="utf-8") as handle:
        if new:
            handle.write("# Lessons learned\n\n| Date | Area | Lesson | Action for next episode |\n|---|---|---|---|\n")
        handle.write(f"| {now_iso()[:10]} | {area} | {lesson} | {action} |\n")
    return path
