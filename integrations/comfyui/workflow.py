"""Load ComfyUI API-format workflows and inject shot parameters.

A workflow lives as two files in ``integrations/comfyui/workflows/``:

* ``<name>.api.json``      exported from ComfyUI with "Export (API)"
* ``<name>.mapping.json``  which node inputs receive which studio values,
                           and which registry models the workflow uses

Mapping example::

    {
      "models": ["animagine_xl_4"],
      "tools": ["comfyui"],
      "inputs": {
        "prompt":   [{"node": "6", "input": "text"}],
        "negative": [{"node": "7", "input": "text"}],
        "seed":     [{"node": "3", "input": "seed"}],
        "width":    [{"node": "5", "input": "width"}]
      }
    }

Keeping the mapping separate means a better workflow can be dropped in
(re-export from ComfyUI, update node numbers) without touching code.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Dict, List, Tuple

from studio.common import StudioError, load_json

WORKFLOW_DIR = Path(__file__).resolve().parent / "workflows"


def load_workflow(name: str, folder: Path = WORKFLOW_DIR) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    api_path = Path(folder) / f"{name}.api.json"
    map_path = Path(folder) / f"{name}.mapping.json"
    if not api_path.is_file():
        raise StudioError(f"ComfyUI workflow not found: {api_path}. Export it from ComfyUI with 'Export (API)'.")
    if not map_path.is_file():
        raise StudioError(f"Mapping not found: {map_path}")
    workflow, mapping = load_json(api_path), load_json(map_path)
    validate_mapping(workflow, mapping, name)
    return workflow, mapping


def validate_mapping(workflow: Dict[str, Any], mapping: Dict[str, Any], name: str = "workflow") -> None:
    for key, targets in (mapping.get("inputs") or {}).items():
        for target in targets:
            node = workflow.get(str(target.get("node")))
            if node is None:
                raise StudioError(f"{name}: mapping '{key}' points at missing node {target.get('node')}")
            if target.get("input") not in (node.get("inputs") or {}):
                raise StudioError(f"{name}: node {target['node']} ({node.get('class_type')}) has no input '{target.get('input')}'")


def inject(workflow: Dict[str, Any], mapping: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``workflow`` with mapped params written in."""
    filled = copy.deepcopy(workflow)
    for key, targets in (mapping.get("inputs") or {}).items():
        if key not in params or params[key] is None:
            continue
        value = params[key]
        for target in targets:
            transform = target.get("transform")
            final = value
            if transform == "int":
                final = int(value)
            elif transform == "float":
                final = float(value)
            elif transform == "prefix":
                final = f"{target.get('text', '')}{value}"
            filled[str(target["node"])]["inputs"][target["input"]] = final
    return _bypass_optional(filled, mapping, params)


def _bypass_optional(workflow: Dict[str, Any], mapping: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove optional nodes (e.g. a LoRA loader) when their param is absent,
    rewiring every link that pointed at them to the passthrough source."""
    for node_id, rule in (mapping.get("optional_nodes") or {}).items():
        if params.get(rule.get("when_missing")):
            continue
        passthrough = rule.get("passthrough") or {}
        workflow.pop(str(node_id), None)
        for node in workflow.values():
            for name, value in list((node.get("inputs") or {}).items()):
                if isinstance(value, list) and len(value) == 2 and str(value[0]) == str(node_id):
                    replacement = passthrough.get(str(value[1]))
                    if replacement is None:
                        raise StudioError(f"Cannot bypass node {node_id}: no passthrough for output {value[1]}")
                    node["inputs"][name] = list(replacement)
    return workflow


def required_keys(mapping: Dict[str, Any]) -> List[str]:
    return list(mapping.get("required") or [])
