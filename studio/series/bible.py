"""Load and validate a series bible.

Layout (see ``series/_template``)::

    series/<slug>/
        series.yaml
        bible/style.yaml
        bible/characters/<id>.yaml
        bible/locations/<id>.yaml
        bible/props/<id>.yaml          (optional)
        bible/refs/...                 model sheets and reference images
        episodes/E01/...

The bible is the single source of truth for consistency. Every check in
the feedback loop compares generated output against it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from studio.common import SERIES_ROOT, StudioError, load_yaml

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

CHARACTER_REQUIRED = ("id", "name", "role", "appearance", "palette", "outfits", "voice")
LOCATION_REQUIRED = ("id", "name", "description")
STATUSES = {"draft", "review", "approved", "retired"}


@dataclass
class Issue:
    level: str  # "error" | "warning"
    where: str
    message: str

    def as_dict(self) -> Dict[str, str]:
        return {"level": self.level, "where": self.where, "message": self.message}


@dataclass
class Bible:
    slug: str
    root: Path
    series: Dict[str, Any]
    style: Dict[str, Any]
    characters: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    locations: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    props: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @property
    def languages(self) -> List[str]:
        return list(self.series.get("languages") or ["en"])

    @property
    def format(self) -> Dict[str, Any]:
        return self.series.get("format") or {}

    def character(self, character_id: str) -> Dict[str, Any]:
        if character_id not in self.characters:
            raise StudioError(f"Unknown character '{character_id}' in series '{self.slug}'.")
        return self.characters[character_id]

    def reference_path(self, relative: str) -> Path:
        return (self.root / "bible" / relative).resolve()


def series_dir(slug: str) -> Path:
    if not SLUG_PATTERN.match(slug or ""):
        raise StudioError(f"Invalid series slug '{slug}': use lowercase letters, digits and hyphens.")
    return SERIES_ROOT / slug


def _load_folder(folder: Path) -> Dict[str, Dict[str, Any]]:
    items: Dict[str, Dict[str, Any]] = {}
    if not folder.is_dir():
        return items
    for path in sorted(folder.glob("*.yaml")):
        if path.name.startswith("_"):
            continue  # templates
        data = load_yaml(path, rich=True)
        data.setdefault("id", path.stem)
        data["_file"] = str(path)
        items[str(data["id"])] = data
    return items


def load_bible(slug: str, root: Path = None) -> Bible:
    root = Path(root) if root else series_dir(slug)
    if not (root / "series.yaml").is_file():
        raise StudioError(f"No series.yaml in {root}. Create one with: python -m studio series new {slug}")
    bible_dir = root / "bible"
    style_path = bible_dir / "style.yaml"
    return Bible(
        slug=slug,
        root=root,
        series=load_yaml(root / "series.yaml", rich=True),
        style=load_yaml(style_path, rich=True) if style_path.is_file() else {},
        characters=_load_folder(bible_dir / "characters"),
        locations=_load_folder(bible_dir / "locations"),
        props=_load_folder(bible_dir / "props"),
    )


def _check_palette(where: str, palette: Any, issues: List[Issue]) -> None:
    if not isinstance(palette, dict) or not palette:
        issues.append(Issue("error", where, "palette must map part names to #RRGGBB colours"))
        return
    for part, colour in palette.items():
        if not HEX_COLOR.match(str(colour)):
            issues.append(Issue("error", where, f"palette.{part} = {colour!r} is not #RRGGBB"))


def validate_bible(bible: Bible, registry_tools: Dict[str, Any] = None) -> List[Issue]:
    """Return a list of issues. Errors block production; warnings do not."""
    issues: List[Issue] = []
    series = bible.series

    for key in ("title", "languages", "format"):
        if key not in series:
            issues.append(Issue("error", "series.yaml", f"missing '{key}'"))
    fmt = bible.format
    fps = fmt.get("fps")
    if fps not in (None, 24, 23.976, 25, 30):
        issues.append(Issue("warning", "series.yaml", f"format.fps={fps}; anime is normally 24"))

    if not bible.characters:
        issues.append(Issue("warning", "bible/characters", "no characters defined yet"))

    for cid, char in bible.characters.items():
        where = f"characters/{cid}"
        if not ID_PATTERN.match(cid):
            issues.append(Issue("error", where, "id must be lowercase letters, digits, underscores"))
        for key in CHARACTER_REQUIRED:
            if key not in char:
                issues.append(Issue("error", where, f"missing '{key}'"))
        _check_palette(where, char.get("palette"), issues)

        outfits = char.get("outfits") or {}
        if not isinstance(outfits, dict) or "default" not in outfits:
            issues.append(Issue("error", where, "outfits must include a 'default' outfit"))

        voice = char.get("voice") or {}
        for lang in bible.languages:
            spec = voice.get(lang) if isinstance(voice, dict) else None
            if not spec:
                issues.append(Issue("error", where, f"no voice defined for language '{lang}'"))
                continue
            engine = spec.get("engine")
            if registry_tools is not None and engine and engine not in registry_tools:
                issues.append(Issue("error", where, f"voice.{lang}.engine '{engine}' is not in integrations/registry.yaml"))
            if spec.get("clone_of_real_person"):
                if not spec.get("consent_record"):
                    issues.append(Issue("error", where, f"voice.{lang} clones a real person but has no consent_record"))

        status = char.get("status", "draft")
        if status not in STATUSES:
            issues.append(Issue("error", where, f"status '{status}' not in {sorted(STATUSES)}"))
        elif status != "approved":
            issues.append(Issue("warning", where, f"status is '{status}': approve the model sheet before production"))

        refs = char.get("references") or {}
        sheet = refs.get("model_sheet") if isinstance(refs, dict) else None
        if not sheet:
            issues.append(Issue("warning", where, "no references.model_sheet: identity QC cannot run"))
        elif not bible.reference_path(sheet).is_file():
            issues.append(Issue("warning", where, f"model sheet not found: bible/{sheet}"))

        lora = char.get("lora") or {}
        if lora and not lora.get("trigger"):
            issues.append(Issue("warning", where, "lora has no trigger word"))

    for lid, loc in bible.locations.items():
        where = f"locations/{lid}"
        if not ID_PATTERN.match(lid):
            issues.append(Issue("error", where, "id must be lowercase letters, digits, underscores"))
        for key in LOCATION_REQUIRED:
            if key not in loc:
                issues.append(Issue("error", where, f"missing '{key}'"))
        if "palette" in loc:
            _check_palette(where, loc["palette"], issues)

    style = bible.style
    if not style:
        issues.append(Issue("warning", "bible/style.yaml", "no style guide yet"))
    elif "palette" in style:
        _check_palette("bible/style.yaml", style["palette"], issues)

    return issues
