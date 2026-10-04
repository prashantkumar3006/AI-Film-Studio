"""Minimal ComfyUI HTTP API client (standard library only).

ComfyUI runs on the GridShare GPU (one-click template). Reach it through
an SSH tunnel (``python -m studio compute tunnel``) at
``http://127.0.0.1:8188``; never expose the port publicly.

Endpoints used: POST /prompt, GET /history/{id}, GET /view,
POST /upload/image, GET /system_stats.
"""

from __future__ import annotations

import json
import mimetypes
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.common import StudioError


class ComfyClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8188", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client_id = str(uuid.uuid4())

    # ---------------------------------------------------------- http
    def _request(self, method: str, path: str, body: Optional[bytes] = None, headers=None) -> bytes:
        request = urllib.request.Request(self.base_url + path, data=body, method=method, headers=headers or {})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")[:800]
            raise StudioError(f"ComfyUI {method} {path} -> HTTP {error.code}: {detail}") from error
        except urllib.error.URLError as error:
            raise StudioError(
                f"Cannot reach ComfyUI at {self.base_url} ({error.reason}). Is the GridShare instance running and the tunnel open?"
            ) from error

    def _json(self, method: str, path: str, payload: Any = None) -> Any:
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        raw = self._request(method, path, body, headers)
        return json.loads(raw.decode("utf-8")) if raw else {}

    # ------------------------------------------------------------ api
    def system_stats(self) -> Dict[str, Any]:
        return self._json("GET", "/system_stats")

    def queue(self, workflow: Dict[str, Any]) -> str:
        result = self._json("POST", "/prompt", {"prompt": workflow, "client_id": self.client_id})
        if result.get("node_errors"):
            raise StudioError(f"ComfyUI rejected the workflow: {json.dumps(result['node_errors'])[:800]}")
        prompt_id = result.get("prompt_id")
        if not prompt_id:
            raise StudioError(f"ComfyUI returned no prompt_id: {result}")
        return prompt_id

    def history(self, prompt_id: str) -> Dict[str, Any]:
        return self._json("GET", f"/history/{urllib.parse.quote(prompt_id)}")

    def wait(self, prompt_id: str, timeout: int = 3600, poll: float = 2.0) -> Dict[str, Any]:
        deadline = time.time() + timeout
        while time.time() < deadline:
            entry = self.history(prompt_id).get(prompt_id)
            if entry:
                status = entry.get("status") or {}
                if status.get("status_str") == "error":
                    raise StudioError(f"ComfyUI job {prompt_id} failed: {json.dumps(status.get('messages'))[:800]}")
                if status.get("completed", True) and entry.get("outputs"):
                    return entry
            time.sleep(poll)
        raise StudioError(f"ComfyUI job {prompt_id} did not finish within {timeout}s.")

    @staticmethod
    def output_files(entry: Dict[str, Any]) -> List[Dict[str, str]]:
        files = []
        for node_id, output in (entry.get("outputs") or {}).items():
            for key in ("images", "gifs", "videos", "audio"):
                for item in output.get(key) or []:
                    if item.get("type", "output") == "output":
                        files.append({"node": node_id, **item})
        return files

    def download(self, item: Dict[str, str], dest_dir: Path) -> Path:
        query = urllib.parse.urlencode({"filename": item["filename"], "subfolder": item.get("subfolder", ""), "type": item.get("type", "output")})
        data = self._request("GET", f"/view?{query}")
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        path = dest_dir / Path(item["filename"]).name
        path.write_bytes(data)
        return path

    def upload_image(self, path: Path, overwrite: bool = True) -> str:
        """Upload a reference/keyframe image; returns the name to use in LoadImage."""
        path = Path(path)
        boundary = uuid.uuid4().hex
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        parts = [
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{path.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode(),
            path.read_bytes(),
            f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\n{'true' if overwrite else 'false'}\r\n--{boundary}--\r\n".encode(),
        ]
        raw = self._request("POST", "/upload/image", b"".join(parts), {"Content-Type": f"multipart/form-data; boundary={boundary}"})
        result = json.loads(raw.decode("utf-8"))
        name = result.get("name")
        if not name:
            raise StudioError(f"Upload failed: {result}")
        return f"{result['subfolder']}/{name}" if result.get("subfolder") else name
