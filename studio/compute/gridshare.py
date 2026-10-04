"""Run heavy jobs on a rented GridShare GPU over plain SSH.

GridShare (gridshare.in) gives SSH, JupyterLab, a REST API and one-click
images including ComfyUI. This module only relies on SSH, which works
with every instance type. Connection details come from environment
variables (put them in ``.env``, which is git-ignored — never commit
them)::

    GRIDSHARE_SSH_HOST     e.g. 203.0.113.10
    GRIDSHARE_SSH_PORT     e.g. 22
    GRIDSHARE_SSH_USER     e.g. root
    GRIDSHARE_SSH_KEY      path to your private key (optional)
    GRIDSHARE_REMOTE_DIR   working dir on the instance, e.g. /workspace/studio
    GRIDSHARE_GPU          the GPU you rented, e.g. rtx_4090 (for cost)

Money is spent per hour of instance time, not per job. ``session start``
and ``session stop`` record that time into the episode ledger, and
``session status`` warns when an instance has been left running.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.common import StudioError, dump_json, load_json, now_iso


@dataclass
class Remote:
    host: str
    user: str = "root"
    port: int = 22
    key: Optional[str] = None
    remote_dir: str = "/workspace/studio"
    gpu: str = "rtx_4090"

    @classmethod
    def from_env(cls, env: Dict[str, str] = None) -> "Remote":
        env = env if env is not None else os.environ
        host = env.get("GRIDSHARE_SSH_HOST")
        if not host:
            raise StudioError("GRIDSHARE_SSH_HOST is not set. Copy .env.example to .env and fill in your instance details.")
        return cls(
            host=host,
            user=env.get("GRIDSHARE_SSH_USER", "root"),
            port=int(env.get("GRIDSHARE_SSH_PORT", "22")),
            key=env.get("GRIDSHARE_SSH_KEY") or None,
            remote_dir=env.get("GRIDSHARE_REMOTE_DIR", "/workspace/studio"),
            gpu=env.get("GRIDSHARE_GPU", "rtx_4090"),
        )

    # ------------------------------------------------------- commands
    def _ssh_base(self) -> List[str]:
        args = ["ssh", "-p", str(self.port), "-o", "StrictHostKeyChecking=accept-new", "-o", "ServerAliveInterval=30"]
        if self.key:
            args += ["-i", self.key]
        return args

    @property
    def target(self) -> str:
        return f"{self.user}@{self.host}"

    def ssh_command(self, command: str) -> List[str]:
        remote = f"mkdir -p {shlex.quote(self.remote_dir)} && cd {shlex.quote(self.remote_dir)} && {command}"
        return self._ssh_base() + [self.target, remote]

    def push_command(self, local: Path, remote_subdir: str = "") -> List[str]:
        dest = f"{self.target}:{self.remote_dir.rstrip('/')}/{remote_subdir}".rstrip("/") + "/"
        ssh = " ".join(shlex.quote(a) for a in self._ssh_base())
        if shutil.which("rsync"):
            return ["rsync", "-az", "--partial", "-e", ssh, str(local), dest]
        args = ["scp", "-r", "-P", str(self.port)] + (["-i", self.key] if self.key else [])
        return args + [str(local), dest]

    def pull_command(self, remote_path: str, local: Path) -> List[str]:
        source = f"{self.target}:{remote_path if remote_path.startswith('/') else self.remote_dir.rstrip('/') + '/' + remote_path}"
        ssh = " ".join(shlex.quote(a) for a in self._ssh_base())
        if shutil.which("rsync"):
            return ["rsync", "-az", "--partial", "-e", ssh, source, str(local)]
        args = ["scp", "-r", "-P", str(self.port)] + (["-i", self.key] if self.key else [])
        return args + [source, str(local)]

    def tunnel_command(self, local_port: int = 8188, remote_port: int = 8188) -> List[str]:
        """Forward the instance's ComfyUI API to localhost (no public port needed)."""
        return self._ssh_base() + ["-N", "-L", f"{local_port}:127.0.0.1:{remote_port}", self.target]

    # -------------------------------------------------------- execute
    def run(self, command: str, timeout: int = 6 * 3600) -> subprocess.CompletedProcess:
        return subprocess.run(self.ssh_command(command), capture_output=True, text=True, timeout=timeout, check=False)

    def push(self, local: Path, remote_subdir: str = "") -> None:
        done = subprocess.run(self.push_command(local, remote_subdir), capture_output=True, text=True, check=False)
        if done.returncode != 0:
            raise StudioError(f"Upload failed: {done.stderr.strip()[:500]}")

    def pull(self, remote_path: str, local: Path) -> None:
        Path(local).parent.mkdir(parents=True, exist_ok=True)
        done = subprocess.run(self.pull_command(remote_path, local), capture_output=True, text=True, check=False)
        if done.returncode != 0:
            raise StudioError(f"Download failed: {done.stderr.strip()[:500]}")

    def open_tunnel(self, local_port: int = 8188, remote_port: int = 8188) -> subprocess.Popen:
        process = subprocess.Popen(self.tunnel_command(local_port, remote_port))
        time.sleep(2)
        if process.poll() is not None:
            raise StudioError("SSH tunnel exited immediately: check host, port and key.")
        return process


# ---------------------------------------------------------- sessions
def _session_file(project_root: Path) -> Path:
    return Path(project_root) / "00_admin" / "budget" / "open_session.json"


def session_start(project_root: Path, gpu: str, note: str = "") -> Dict[str, Any]:
    path = _session_file(project_root)
    if path.is_file():
        raise StudioError("A GPU session is already open. Stop it first: python -m studio compute stop ...")
    data = {"gpu": gpu, "started_epoch": time.time(), "started": now_iso(), "note": note}
    dump_json(data, path)
    return data


def session_stop(project_root: Path, ledger, now_epoch: float = None) -> Dict[str, Any]:
    path = _session_file(project_root)
    if not path.is_file():
        raise StudioError("No open GPU session.")
    data = load_json(path)
    seconds = (now_epoch or time.time()) - float(data["started_epoch"])
    entry = ledger.log_session(data["gpu"], max(seconds, 1.0), note=data.get("note", ""))
    path.unlink()
    return entry


def session_status(project_root: Path, warn_hours: float = 3.0, now_epoch: float = None) -> Dict[str, Any]:
    path = _session_file(project_root)
    if not path.is_file():
        return {"open": False}
    data = load_json(path)
    hours = ((now_epoch or time.time()) - float(data["started_epoch"])) / 3600.0
    return {"open": True, "gpu": data["gpu"], "hours": round(hours, 2), "warning": hours >= warn_hours, "started": data["started"]}
