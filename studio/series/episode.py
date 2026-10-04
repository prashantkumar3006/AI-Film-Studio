"""Create series and episodes from the templates in ``series/_template``.

An episode has two homes:

* ``series/<slug>/episodes/EXX/`` — small, version-controlled canon
  (episode.yaml, script.md, shotlist.json, continuity.json).
* ``projects/<PROJECT_ID>/<slug>/`` — the engine project with numbered
  folders for heavy media, QC reports and state. Git-ignored.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from studio.common import REPO_ROOT, TEMPLATE_SERIES, StudioError, dump_yaml, load_yaml
from studio.series.bible import series_dir


def create_series(slug: str, title: str, languages=None) -> Path:
    target = series_dir(slug)
    if target.exists():
        raise StudioError(f"Series already exists: {target}")
    if not TEMPLATE_SERIES.is_dir():
        raise StudioError(f"Template missing: {TEMPLATE_SERIES}")
    shutil.copytree(TEMPLATE_SERIES, target, ignore=shutil.ignore_patterns("episodes"))
    (target / "episodes").mkdir(exist_ok=True)
    meta = load_yaml(target / "series.yaml", rich=True)
    meta["slug"] = slug
    meta["title"] = title
    if languages:
        meta["languages"] = list(languages)
    dump_yaml(meta, target / "series.yaml")
    return target


def episode_dir(slug: str, number: int) -> Path:
    return series_dir(slug) / "episodes" / f"E{int(number):02d}"


def _engine_init(title: str, fps: int, resolution: str) -> Dict[str, str]:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "create_project.py"),
        "init",
        "--title",
        title,
        "--type",
        "animation",
        "--fps",
        str(fps),
        "--resolution",
        resolution,
        "--complexity",
        "FULL",
    ]
    done = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True)
    if done.returncode != 0:
        raise StudioError(f"Engine init failed:\n{done.stderr or done.stdout}")
    match = re.search(r"Location\s*:\s*(.+)", done.stdout)
    if not match:
        raise StudioError(f"Could not read project location from engine output:\n{done.stdout}")
    location = Path(match.group(1).strip())
    return {"project_id": location.parent.name, "project_slug": location.name, "project_root": str(location)}


def create_episode(slug: str, number: int, title: str, with_project: bool = True) -> Dict[str, Any]:
    series_root = series_dir(slug)
    if not (series_root / "series.yaml").is_file():
        raise StudioError(f"Unknown series '{slug}'. Create it first: python -m studio series new {slug}")
    target = episode_dir(slug, number)
    if target.exists():
        raise StudioError(f"Episode already exists: {target}")
    template = TEMPLATE_SERIES / "episodes" / "E00"
    shutil.copytree(template, target)

    series_meta = load_yaml(series_root / "series.yaml", rich=True)
    fmt = series_meta.get("format") or {}
    info: Dict[str, Any] = {
        "series": slug,
        "number": int(number),
        "title": title,
        "status": "WRITING",
        "languages": series_meta.get("languages") or ["en"],
    }
    if with_project:
        project = _engine_init(
            f"{series_meta.get('title', slug)} E{int(number):02d} {title}",
            int(fmt.get("fps", 24)),
            str(fmt.get("resolution", "1920x1080")),
        )
        info.update(project)
        info["project_root"] = str(Path(project["project_root"]).relative_to(REPO_ROOT))
    dump_yaml(info, target / "episode.yaml")

    shotlist = target / "shotlist.json"
    text = shotlist.read_text(encoding="utf-8")
    text = text.replace('"series": "_template"', f'"series": "{slug}"').replace('"episode": 0', f'"episode": {int(number)}')
    shotlist.write_text(text, encoding="utf-8")
    return info


def load_episode(slug: str, number: int) -> Dict[str, Any]:
    folder = episode_dir(slug, number)
    meta_path = folder / "episode.yaml"
    if not meta_path.is_file():
        raise StudioError(f"No episode E{int(number):02d} in series '{slug}'.")
    meta = load_yaml(meta_path, rich=True)
    meta["_dir"] = str(folder)
    return meta


def project_root(episode: Dict[str, Any]) -> Optional[Path]:
    root = episode.get("project_root")
    return (REPO_ROOT / root) if root else None
