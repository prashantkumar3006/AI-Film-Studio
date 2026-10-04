"""Generate keyframes / video clips through ComfyUI, with provenance.

Flow per call:

1. license gate: every model/tool named in the workflow mapping must be
   cleared before any GPU time is spent (``legal.mode`` in config)
2. upload input images (keyframe for image-to-video, references)
3. inject params, queue, wait, download outputs
4. write a ``.prov.json`` sidecar next to every output

The quality loop (``studio.feedback.loop``) calls ``generate`` once per
attempt, so retries automatically get new seeds and adjusted weights.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.comfyui.client import ComfyClient
from integrations.comfyui.workflow import inject, load_workflow, required_keys
from studio.common import StudioError
from studio.legal.licenses import require_cleared
from studio.legal.provenance import write_provenance


def generate(
    workflow_name: str,
    params: Dict[str, Any],
    out_dir: Path,
    config: Dict[str, Any],
    client: Optional[ComfyClient] = None,
    provenance: Optional[Dict[str, Any]] = None,
    upload: Optional[Dict[str, Path]] = None,
    catalogue=None,
    timeout: int = 3600,
) -> List[Path]:
    workflow, mapping = load_workflow(workflow_name)
    mode = (config.get("legal") or {}).get("mode", "strict")
    require_cleared(list(mapping.get("tools") or []) + list(mapping.get("models") or []), mode=mode, catalogue=catalogue)

    missing = [key for key in required_keys(mapping) if params.get(key) in (None, "")]
    if missing:
        raise StudioError(f"Workflow '{workflow_name}' needs params: {', '.join(missing)}")

    comfy_cfg = config.get("comfyui") or {}
    client = client or ComfyClient(comfy_cfg.get("url", "http://127.0.0.1:8188"))
    params = dict(params)
    for key, path in (upload or {}).items():
        params[key] = client.upload_image(Path(path))

    started = time.time()
    prompt_id = client.queue(inject(workflow, mapping, params))
    entry = client.wait(prompt_id, timeout=timeout)
    elapsed = time.time() - started

    outputs = [client.download(item, out_dir) for item in client.output_files(entry)]
    if not outputs:
        raise StudioError(f"ComfyUI job {prompt_id} finished without output files.")

    base = dict(provenance or {})
    for path in outputs:
        record = dict(base)
        record.update(
            {
                "asset": path.name,
                "kind": base.get("kind", "image"),
                "tools": list(mapping.get("tools") or ["comfyui"]),
                "models": list(mapping.get("models") or []),
                "workflow": workflow_name,
                "prompt": params.get("prompt"),
                "negative_prompt": params.get("negative"),
                "seed": params.get("seed"),
                "params": {k: v for k, v in params.items() if not k.startswith("_") and k not in {"prompt", "negative"}},
                "job_id": prompt_id,
                "gpu_seconds_wall": round(elapsed, 1),
            }
        )
        write_provenance(path, record, catalogue=catalogue)
    return outputs
