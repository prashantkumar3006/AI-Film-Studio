"""Shared paths and file helpers for the studio packages.

Standard library only. YAML goes through ``studio.orchestrator.config``
(PyYAML when installed, a small built-in parser otherwise). Series
bibles use richer YAML than the built-in parser supports, so loading
them asks for PyYAML with a clear message instead of failing obscurely.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[1]
SERIES_ROOT = REPO_ROOT / "series"
PROJECTS_ROOT = REPO_ROOT / "projects"
INTEGRATIONS_ROOT = REPO_ROOT / "integrations"
LEGAL_ROOT = REPO_ROOT / "legal"
TEMPLATE_SERIES = SERIES_ROOT / "_template"


class StudioError(RuntimeError):
    """A user-facing error: printed without a traceback by the CLI."""


def now_iso() -> str:
    return dt.datetime.now().astimezone().replace(microsecond=0).isoformat()


def today_iso() -> str:
    return dt.date.today().isoformat()


def load_json(path: Path) -> Any:
    path = Path(path)
    if not path.is_file():
        raise StudioError(f"File not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise StudioError(f"Invalid JSON in {path}: {error}") from error


def dump_json(data: Any, path: Path) -> Path:
    """Write JSON atomically (write temp file, then replace)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return path


def load_yaml(path: Path, rich: bool = False) -> Dict[str, Any]:
    """Load a YAML mapping.

    ``rich=True`` requires PyYAML (lists of mappings, multi-line strings),
    which series bibles need.
    """
    path = Path(path)
    if not path.is_file():
        raise StudioError(f"File not found: {path}")
    try:
        import yaml  # type: ignore
    except ImportError:
        if rich:
            raise StudioError(
                f"Reading {path.name} needs PyYAML. Install it with: pip install -r requirements.txt"
            )
        from studio.orchestrator.config import load_yaml as simple_load

        return simple_load(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise StudioError(f"Top level of {path} must be a mapping.")
    return data


def dump_yaml(data: Dict[str, Any], path: Path) -> Path:
    try:
        import yaml  # type: ignore
    except ImportError as error:
        raise StudioError("Writing YAML needs PyYAML: pip install -r requirements.txt") from error
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def relpath(path: Path) -> str:
    """Path relative to the repo when possible (for readable reports)."""
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)
