"""
Configuration loading for the modular studio.

Loads ``studio/config.yaml`` and ``integrations/registry.yaml``.

No hard dependency: PyYAML is used when it is installed; otherwise a
small built-in parser handles the simple YAML subset these files use
(nested mappings, scalars, inline ``[a, b]`` lists and ``- item`` lists
of scalars). Keep config files within that subset.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "studio" / "config.yaml"
DEFAULT_REGISTRY_PATH = REPO_ROOT / "integrations" / "registry.yaml"

REQUIRED_SECTIONS = ("projects", "assets", "render", "audio", "processing", "integrations")
PROCESSING_PREFERENCES = {"local", "external", "hybrid"}


class ConfigError(ValueError):
    """Raised when a configuration file is missing or invalid."""


# ------------------------------------------------------------
# Minimal YAML subset parser (fallback when PyYAML is absent)
# ------------------------------------------------------------

def _scalar(text: str) -> Any:
    text = text.strip()
    if text == "" or text in {"null", "~", "Null", "NULL"}:
        return None
    if text in {"true", "True", "TRUE"}:
        return True
    if text in {"false", "False", "FALSE"}:
        return False
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [_scalar(part) for part in inner.split(",")] if inner else []
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


def _strip_comment(line: str) -> str:
    in_quote: Optional[str] = None
    for i, ch in enumerate(line):
        if ch in {"'", '"'}:
            in_quote = None if in_quote == ch else (in_quote or ch)
        elif ch == "#" and in_quote is None and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def _simple_yaml(text: str) -> Dict[str, Any]:
    lines: List[Tuple[int, str]] = []
    for raw in text.splitlines():
        stripped = _strip_comment(raw).rstrip()
        if stripped.strip():
            lines.append((len(stripped) - len(stripped.lstrip(" ")), stripped.strip()))

    root: Dict[str, Any] = {}
    # stack of (indent, container, parent, key) — parent/key let an empty
    # mapping placeholder be swapped for a list when "- item" lines follow.
    stack: List[Tuple[int, Any, Any, Optional[str]]] = [(-1, root, None, None)]

    for indent, content in lines:
        while stack[-1][0] >= indent:
            stack.pop()
        _, container, parent, key_in_parent = stack[-1]

        if content.startswith("- "):
            if isinstance(container, dict) and not container and parent is not None:
                container = []
                parent[key_in_parent] = container
                stack[-1] = (stack[-1][0], container, parent, key_in_parent)
            if not isinstance(container, list):
                raise ConfigError(f"Unexpected list item: {content!r}")
            container.append(_scalar(content[2:]))
            continue

        if ":" not in content or not isinstance(container, dict):
            raise ConfigError(f"Unsupported YAML line: {content!r}")

        key, _, value = content.partition(":")
        key = key.strip()
        if value.strip():
            container[key] = _scalar(value)
        else:
            child: Dict[str, Any] = {}
            container[key] = child
            stack.append((indent, child, container, key))

    return root


def load_yaml(path: Path) -> Dict[str, Any]:
    path = Path(path)
    if not path.is_file():
        raise ConfigError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
    except ImportError:
        data = _simple_yaml(text)
    else:
        data = yaml.safe_load(text) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"Top level of {path} must be a mapping.")
    return data


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def load_config(path: Optional[Path] = None) -> Dict[str, Any]:
    """Load and validate studio/config.yaml."""
    config = load_yaml(Path(path) if path else DEFAULT_CONFIG_PATH)

    missing = [s for s in REQUIRED_SECTIONS if s not in config]
    if missing:
        raise ConfigError(f"config.yaml is missing sections: {', '.join(missing)}")

    preference = config["processing"].get("preference", "local")
    if preference not in PROCESSING_PREFERENCES:
        raise ConfigError(
            f"processing.preference must be one of {sorted(PROCESSING_PREFERENCES)}, got {preference!r}"
        )

    for key in ("resolution", "preview_resolution"):
        value = str(config["render"].get(key, ""))
        if value and not _is_resolution(value):
            raise ConfigError(f"render.{key} must look like 1920x1080, got {value!r}")

    return config


def load_registry(path: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """Load integrations/registry.yaml and return {name: entry}."""
    data = load_yaml(Path(path) if path else DEFAULT_REGISTRY_PATH)
    entries = data.get("integrations") or {}
    if not isinstance(entries, dict):
        raise ConfigError("registry.yaml 'integrations' must be a mapping.")

    required = ("name", "type", "enabled", "execution_mode", "repository", "adapter")
    for key, entry in entries.items():
        missing = [f for f in required if f not in (entry or {})]
        if missing:
            raise ConfigError(f"Integration {key!r} is missing: {', '.join(missing)}")
    return entries


def effective_integrations(
    config: Dict[str, Any],
    registry: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """
    Merge machine switches (config.yaml) with the catalogue (registry.yaml).

    An integration is active only when enabled in BOTH places, and an
    external one is further blocked unless processing.allow_external is true.
    """
    switches = config.get("integrations") or {}
    allow_external = bool(config["processing"].get("allow_external", False))
    merged: Dict[str, Dict[str, Any]] = {}

    for key, entry in registry.items():
        item = copy.deepcopy(entry)
        reason = None
        if not entry.get("enabled"):
            reason = "disabled in registry"
        elif not switches.get(key, False):
            reason = "disabled in config"
        elif entry.get("execution_mode") == "external" and not allow_external:
            reason = "external processing not allowed"
        elif not entry.get("adapter"):
            reason = "adapter not implemented"
        item["active"] = reason is None
        item["status"] = "active" if reason is None else reason
        merged[key] = item
    return merged


def parse_resolution(value: str) -> Tuple[int, int]:
    width, _, height = str(value).lower().partition("x")
    return int(width), int(height)


def _is_resolution(value: str) -> bool:
    try:
        w, h = parse_resolution(value)
    except ValueError:
        return False
    return w > 0 and h > 0
