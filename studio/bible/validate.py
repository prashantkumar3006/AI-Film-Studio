"""
Validate a Production Bible.

Two layers:

1. ``schema/bible.schema.json`` (JSON Schema 2020-12): shapes, required
   fields, ID patterns and allowed values.
2. Cross-reference checks the schema cannot express: unique IDs, IDs nested
   under their parents, references that resolve, and text present for every
   project language.

Usage from code::

    from studio.bible import validate_bible, load_bible
    report = validate_bible(load_bible("examples/ep00/bible.json"))
    report.ok        # True / False
    report.errors    # list[str]
    report.warnings  # list[str]
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schema" / "bible.schema.json"
SEARCH_DIRS = ("projects", "examples")


@dataclass
class Report:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


class BibleLoadError(ValueError):
    """The Bible file could not be found or parsed."""


# ------------------------------------------------------------
# Loading
# ------------------------------------------------------------

def resolve_target(target: Union[str, Path]) -> Path:
    """
    Accept a path to a bible.json, a directory containing one, or an episode
    name such as ``ep00`` looked up under projects/ and then examples/.
    """
    path = Path(target)
    candidates = [path, path / "bible.json"]
    for root in SEARCH_DIRS:
        candidates.append(REPO_ROOT / root / str(target) / "bible.json")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise BibleLoadError(
        f"No Bible found for {str(target)!r}. Give a path to bible.json, "
        "a folder that contains one, or an episode folder name under projects/ or examples/."
    )


def load_bible(target: Union[str, Path]) -> Dict[str, Any]:
    path = resolve_target(target)
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise BibleLoadError(f"{path}: not valid JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise BibleLoadError(f"{path}: top level must be a JSON object")
    return data


def load_schema() -> Dict[str, Any]:
    with SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


# ------------------------------------------------------------
# Layer 1: JSON Schema
# ------------------------------------------------------------

def _schema_errors(bible: Dict[str, Any]) -> List[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - environment problem
        raise RuntimeError(
            "The 'jsonschema' package is required: pip install -e .  (or pip install jsonschema)"
        ) from exc

    validator = Draft202012Validator(load_schema())
    messages = []
    for err in sorted(validator.iter_errors(bible), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(p) for p in err.absolute_path) or "(root)"
        messages.append(f"schema: {where}: {err.message}")
    return messages


# ------------------------------------------------------------
# Layer 2: cross-reference checks
# ------------------------------------------------------------

def _iter_shots(bible: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for scene in bible.get("scenes", []):
        for shot in scene.get("shots", []):
            yield scene, shot


def _check_languages(label: str, text: Any, languages: List[str], report: Report) -> None:
    if not isinstance(text, dict):
        return
    missing = [lang for lang in languages if lang not in text]
    extra = [lang for lang in text if lang not in languages]
    if missing:
        report.errors.append(f"{label}: missing text for {', '.join(missing)}")
    if extra:
        report.errors.append(f"{label}: text for {', '.join(extra)}, which is not a project language")


def _cross_reference_errors(bible: Dict[str, Any]) -> Report:
    report = Report()
    project = bible.get("project", {})
    episode = project.get("id", "")
    languages = list(project.get("languages", []))

    primary = project.get("primary_language")
    if primary and primary not in languages:
        report.errors.append(f"project.primary_language {primary!r} is not in project.languages")
    if project.get("audience", {}).get("made_for_kids") is True:
        report.warnings.append("project.audience.made_for_kids is true; the plan sets every upload to 'not made for kids'")

    # Unique IDs across the whole Bible.
    seen: Dict[str, str] = {}

    def claim(item_id: Optional[str], where: str) -> None:
        if not item_id:
            return
        if item_id in seen:
            report.errors.append(f"duplicate id {item_id!r} ({where} and {seen[item_id]})")
        else:
            seen[item_id] = where

    characters = {c.get("id") for c in bible.get("characters", [])}
    for c in bible.get("characters", []):
        claim(c.get("id"), "characters")
        _check_languages(f"character {c.get('id')} name", c.get("name"), languages, report)
        voices = c.get("voices", {})
        missing = [lang for lang in languages if lang not in voices]
        if missing:
            report.errors.append(f"character {c.get('id')}: no voice for {', '.join(missing)}")

    locations = {loc.get("id") for loc in bible.get("locations", [])}
    for loc in bible.get("locations", []):
        claim(loc.get("id"), "locations")

    shots = set()
    lines = set()
    for scene in bible.get("scenes", []):
        sid = scene.get("id", "")
        claim(sid, "scenes")
        if episode and sid and not sid.startswith(episode + "_"):
            report.errors.append(f"scene {sid}: id does not start with the episode id {episode}")
        loc = scene.get("location")
        if loc and loc not in locations:
            report.errors.append(f"scene {sid}: location {loc} is not defined in locations")

        for shot in scene.get("shots", []):
            shid = shot.get("id", "")
            claim(shid, f"scene {sid}")
            shots.add(shid)
            if sid and shid and not shid.startswith(sid + "_"):
                report.errors.append(f"shot {shid}: id is not under its scene {sid}")
            on_screen = set(shot.get("characters", []))
            for cid in on_screen - characters:
                report.errors.append(f"shot {shid}: character {cid} is not defined in characters")

            for line in shot.get("lines", []):
                lid = line.get("id", "")
                claim(lid, f"shot {shid}")
                lines.add(lid)
                if shid and lid and not lid.startswith(shid + "_"):
                    report.errors.append(f"line {lid}: id is not under its shot {shid}")
                speaker = line.get("character")
                if speaker and speaker not in characters:
                    report.errors.append(f"line {lid}: character {speaker} is not defined in characters")
                elif speaker and speaker not in on_screen:
                    report.warnings.append(f"line {lid}: {speaker} speaks but is not listed in the shot's characters (off-screen?)")
                _check_languages(f"line {lid}", line.get("text"), languages, report)

    for asset in bible.get("assets", []):
        aid = asset.get("id")
        claim(aid, "assets")
        if asset.get("shot") and asset["shot"] not in shots:
            report.errors.append(f"asset {aid}: shot {asset['shot']} does not exist")
        if asset.get("line") and asset["line"] not in lines:
            report.errors.append(f"asset {aid}: line {asset['line']} does not exist")
        if asset.get("language") and asset["language"] not in languages:
            report.errors.append(f"asset {aid}: language {asset['language']} is not a project language")

    jobs = {j.get("id") for j in bible.get("jobs", [])}
    for job in bible.get("jobs", []):
        jid = job.get("id")
        claim(jid, "jobs")
        if job.get("shot") and job["shot"] not in shots:
            report.errors.append(f"job {jid}: shot {job['shot']} does not exist")
        for dep in job.get("depends_on", []):
            if dep not in jobs:
                report.errors.append(f"job {jid}: depends on unknown job {dep}")

    return report


# ------------------------------------------------------------
# Public entry point
# ------------------------------------------------------------

def validate_bible(bible: Dict[str, Any]) -> Report:
    """Run both layers. Cross-reference checks run only if the schema passes."""
    report = Report(errors=_schema_errors(bible))
    if report.errors:
        return report
    xref = _cross_reference_errors(bible)
    report.errors.extend(xref.errors)
    report.warnings.extend(xref.warnings)
    return report


def summary(bible: Dict[str, Any]) -> str:
    """One line describing what the Bible contains."""
    scenes = bible.get("scenes", [])
    shots = [shot for _, shot in _iter_shots(bible)]
    n_lines = sum(len(s.get("lines", [])) for s in shots)
    runtime = sum(float(s.get("duration_s", 0)) for s in shots)
    project = bible.get("project", {})

    def count(n: int, word: str) -> str:
        return f"{n} {word}{'' if n == 1 else 's'}"

    return (
        f"{project.get('id', '?')} \"{project.get('title', '?')}\": "
        f"{count(len(bible.get('characters', [])), 'character')}, {count(len(scenes), 'scene')}, "
        f"{count(len(shots), 'shot')}, {count(n_lines, 'line')}, {runtime:.0f} s, "
        f"languages {', '.join(project.get('languages', []))}"
    )
