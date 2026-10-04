"""Run a tool from a command template, locally or on the GridShare GPU.

Templates live in ``studio/config.yaml`` under ``tools.<key>``::

    tools:
      tts_kokoro:
        where: local                 # local | gridshare
        command: "python integrations/tts/runners/kokoro_tts.py --text {text} --voice {voice} --out {out}"

Placeholders are filled with shell-quoted values, so text with spaces,
quotes or Devanagari is safe.
"""

from __future__ import annotations

import shlex
import string
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.common import REPO_ROOT, StudioError


def tool_config(config: Dict[str, Any], key: str) -> Dict[str, Any]:
    tools = config.get("tools") or {}
    spec = tools.get(key)
    if not spec or not spec.get("command"):
        raise StudioError(f"No command configured for tool '{key}' (studio/config.yaml -> tools.{key}.command).")
    return spec


def template_fields(template: str) -> List[str]:
    return [name for _, name, _, _ in string.Formatter().parse(template) if name]


def render_command(template: str, values: Dict[str, Any]) -> str:
    missing = [name for name in template_fields(template) if name not in values]
    if missing:
        raise StudioError(f"Command template needs values for: {', '.join(sorted(set(missing)))}")
    quoted = {key: shlex.quote(str(value)) for key, value in values.items()}
    return template.format(**quoted)


def run_tool(config: Dict[str, Any], key: str, values: Dict[str, Any], timeout: int = 3600, remote=None) -> subprocess.CompletedProcess:
    spec = tool_config(config, key)
    command = render_command(spec["command"], values)
    where = spec.get("where", "local")
    if where == "gridshare":
        if remote is None:
            from studio.compute.gridshare import Remote

            remote = Remote.from_env()
        done = remote.run(command, timeout=timeout)
    elif where == "local":
        done = subprocess.run(command, shell=True, cwd=REPO_ROOT, capture_output=True, text=True, timeout=timeout, check=False)
    else:
        raise StudioError(f"tools.{key}.where must be 'local' or 'gridshare', got {where!r}")
    if done.returncode != 0:
        raise StudioError(f"Tool '{key}' failed (exit {done.returncode}):\n{(done.stderr or done.stdout).strip()[-1500:]}")
    return done


def ensure_file(path: Path, what: str) -> Path:
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        raise StudioError(f"{what} was not produced: {path}")
    return path


def first_existing(paths: List[Optional[Path]]) -> Optional[Path]:
    for path in paths:
        if path and Path(path).exists():
            return Path(path)
    return None
