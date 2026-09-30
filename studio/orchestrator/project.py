"""
Project creation and directory management for the modular studio.

The folder layout is NOT redefined here. It is read from the existing
engine, ``scripts/create_project.py`` (FULL/STANDARD/SMALL folder sets
and OPTIONAL_SUBFOLDERS), so both systems always agree on:

    projects/<PROJECT_ID>/<project-slug>/00_admin, 01_research, ...

On top of that, the asset / render directories named in
``studio/config.yaml`` are created inside those numbered folders.

This module only creates directories. It does not write the engine's
``00_admin/.studio/state.json``; run ``create_project.py init`` for a
fully tracked project and pass its ID/slug to the pipeline instead.
"""

from __future__ import annotations

import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional

from .config import REPO_ROOT

ENGINE_PATH = REPO_ROOT / "scripts" / "create_project.py"
_ID_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")
_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Used only if scripts/create_project.py cannot be imported.
_FALLBACK_FOLDERS = [
    "00_admin", "01_research", "02_story", "03_script", "04_director",
    "07_storyboard-previs", "08_cinematography", "09_ai-generation",
    "12_edit", "14_sound", "16_color", "17_continuity", "18_technical",
    "20_qc", "21_distribution", "23_knowledge", "24_archive", "99_backup",
]


def _load_engine() -> Optional[ModuleType]:
    """Import scripts/create_project.py as a module without running it."""
    if not ENGINE_PATH.is_file():
        return None
    spec = importlib.util.spec_from_file_location("studio_engine", ENGINE_PATH)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:  # engine unavailable -> use fallback layout
        return None
    return module


_ENGINE = _load_engine()


def slugify(value: str) -> str:
    if _ENGINE is not None:
        return _ENGINE.slugify(value)
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "untitled"


def engine_folders(complexity: str) -> List[str]:
    """Top-level numbered folders for a complexity, taken from the engine."""
    complexity = complexity.upper()
    if _ENGINE is not None:
        if complexity not in _ENGINE.COMPLEXITIES:
            raise ValueError(f"Unknown complexity {complexity!r}")
        return list(_ENGINE.folders_for(complexity))
    return list(_FALLBACK_FOLDERS)


def engine_subfolders() -> Dict[str, List[str]]:
    if _ENGINE is not None:
        return {k: list(v) for k, v in _ENGINE.OPTIONAL_SUBFOLDERS.items()}
    return {}


@dataclass
class Project:
    project_id: str
    slug: str
    root: Path
    complexity: str
    created: List[Path] = field(default_factory=list)

    def path(self, relative: str) -> Path:
        return self.root / relative


def project_root(config: Dict[str, Any], project_id: str, slug: str) -> Path:
    if not _ID_PATTERN.match(project_id):
        raise ValueError(f"Invalid project ID {project_id!r} (use letters, digits, underscore)")
    if not _SLUG_PATTERN.match(slug):
        raise ValueError(f"Invalid slug {slug!r} (use lowercase words joined by '-')")

    projects_dir = (REPO_ROOT / config["projects"].get("root", "projects")).resolve()
    root = (projects_dir / project_id / slug).resolve()
    if projects_dir not in root.parents:
        raise ValueError(f"Project path escapes the projects directory: {root}")
    return root


def standard_directories(config: Dict[str, Any], complexity: str) -> List[str]:
    """Every project-relative directory the studio expects to exist."""
    folders = engine_folders(complexity)
    dirs: List[str] = list(folders)

    for parent, children in engine_subfolders().items():
        if parent in folders:
            dirs.extend(f"{parent}/{child}" for child in children)

    studio_dirs = list((config.get("assets") or {}).values())
    render = config.get("render") or {}
    studio_dirs += [render.get("output_dir"), render.get("preview_dir")]

    for rel in filter(None, studio_dirs):
        # Include the parent numbered folder even if this complexity omits it.
        top = rel.split("/", 1)[0]
        if top not in dirs:
            dirs.append(top)
        dirs.append(rel)

    seen = set()
    return [d for d in dirs if not (d in seen or seen.add(d))]


def create_project(
    config: Dict[str, Any],
    slug: str,
    project_id: Optional[str] = None,
    complexity: Optional[str] = None,
    dry_run: bool = False,
) -> Project:
    """
    Create (or complete) a project directory tree.

    Existing directories and files are never removed or overwritten,
    so this is safe to run against a project made by create_project.py.
    """
    project_id = project_id or config["projects"].get("default_project_id", "STUDIO_DRAFT")
    complexity = (complexity or config["projects"].get("default_complexity", "SMALL")).upper()
    root = project_root(config, project_id, slug)
    project = Project(project_id=project_id, slug=slug, root=root, complexity=complexity)

    for rel in standard_directories(config, complexity):
        target = root / rel
        if not target.exists():
            if not dry_run:
                target.mkdir(parents=True, exist_ok=True)
            project.created.append(target)
    return project
