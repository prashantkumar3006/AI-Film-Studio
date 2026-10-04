"""Scan scripts, prompts and dialogue for third-party IP and real people.

The deny list (``legal/denylist.yaml``) is a tripwire, not a lawyer: it
catches the obvious mistakes (a prompt that says "Naruto", "Studio
Ghibli style", or a real actor's name) before money is spent on them.
Anything it flags needs a human decision recorded in the episode.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from studio.common import LEGAL_ROOT, load_yaml
from studio.series.shotlist import iter_shots

DENYLIST_PATH = LEGAL_ROOT / "denylist.yaml"

# Category -> severity. "block" stops the pipeline; "review" needs sign-off.
DEFAULT_SEVERITY = {
    "franchises": "block",
    "characters": "block",
    "real_people": "block",
    "brands": "review",
    "styles": "review",
}


def load_denylist(path: Optional[Path] = None) -> Dict[str, List[str]]:
    data = load_yaml(Path(path) if path else DENYLIST_PATH)
    return {key: [str(t) for t in (value or [])] for key, value in data.items() if isinstance(value, list)}


def _compile(terms: Iterable[str]) -> List[Tuple[str, "re.Pattern[str]"]]:
    compiled = []
    for term in terms:
        term = term.strip()
        if term:
            compiled.append((term, re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE)))
    return compiled


def scan_text(text: str, where: str, denylist: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    for category, terms in denylist.items():
        severity = DEFAULT_SEVERITY.get(category, "review")
        for term, pattern in _compile(terms):
            if pattern.search(text or ""):
                hits.append({"where": where, "category": category, "term": term, "severity": severity})
    return hits


def scan_episode(script_text: str, shotlist: Dict[str, Any], denylist=None) -> Dict[str, Any]:
    denylist = denylist if denylist is not None else load_denylist()
    hits = scan_text(script_text, "script.md", denylist)
    for shot in iter_shots(shotlist):
        sid = shot.get("id")
        for field in ("visual_prompt", "negative_prompt", "action"):
            hits.extend(scan_text(str(shot.get(field) or ""), f"{sid}.{field}", denylist))
        for item in shot.get("dialogue") or []:
            for lang, text in (item.get("line") or {}).items():
                hits.extend(scan_text(str(text), f"{sid}.dialogue.{lang}", denylist))
    blocking = [h for h in hits if h["severity"] == "block"]
    return {"hits": hits, "blocking": len(blocking), "review": len(hits) - len(blocking), "passed": not blocking}
