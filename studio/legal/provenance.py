"""Asset provenance: a ``<file>.prov.json`` sidecar for every generated file.

The sidecar answers "where did this come from and may we sell it?":
tools, models, LoRAs, prompt, seed, input assets and a snapshot of the
license state at generation time. The release gate walks every asset in
the final edit and refuses to pass if any sidecar is missing or names
anything that is not cleared.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from studio.common import StudioError, dump_json, load_json, now_iso
from studio.legal.licenses import all_entries, check_entry, load_catalogue

SIDECAR_SUFFIX = ".prov.json"
REQUIRED_FIELDS = ("asset", "kind", "tools", "created")


def sidecar_path(asset: Path) -> Path:
    asset = Path(asset)
    return asset.with_name(asset.name + SIDECAR_SUFFIX)


def write_provenance(asset: Path, record: Dict[str, Any], catalogue=None) -> Path:
    """Write a sidecar, stamping the license state of every tool/model used."""
    asset = Path(asset)
    entries = all_entries(catalogue or load_catalogue())
    data = dict(record)
    data.setdefault("asset", asset.name)
    data.setdefault("created", now_iso())
    data.setdefault("tools", [])
    data.setdefault("models", [])
    data.setdefault("loras", [])
    data.setdefault("inputs", [])
    data["license_snapshot"] = {
        key: check_entry(key, entries.get(key)).as_dict()
        for key in list(data["tools"]) + list(data["models"])
    }
    for field in REQUIRED_FIELDS:
        if not data.get(field):
            raise StudioError(f"Provenance for {asset.name} is missing '{field}'.")
    return dump_json(data, sidecar_path(asset))


def read_provenance(asset: Path) -> Optional[Dict[str, Any]]:
    path = sidecar_path(asset)
    return load_json(path) if path.is_file() else None


def _lora_problems(lora: Dict[str, Any], bible, entries) -> List[str]:
    """A LoRA is only as clean as its base model and its training data."""
    problems: List[str] = []
    owner = lora.get("character")
    spec = None
    if bible is not None and owner in getattr(bible, "characters", {}):
        spec = bible.characters[owner].get("lora") or None
    if not spec:
        return [f"LoRA '{lora.get('file', '?')}' is not registered in the bible (characters/<id>.yaml lora block)"]
    base = spec.get("base_model")
    if not base:
        problems.append(f"LoRA for '{owner}' has no base_model")
    else:
        clearance = check_entry(base, entries.get(base))
        if not clearance.cleared:
            problems.append(f"LoRA for '{owner}' base model '{base}' not cleared: {clearance.reason}")
    if not spec.get("training_data"):
        problems.append(f"LoRA for '{owner}' has no training_data description")
    if not spec.get("training_data_cleared"):
        problems.append(f"LoRA for '{owner}' training data not marked cleared (only own/licensed images allowed)")
    return problems


def release_gate(assets: Iterable[Path], bible=None, catalogue=None) -> Dict[str, Any]:
    """Check every asset going into a release. Returns a report; ``passed``
    is True only when there are zero problems."""
    entries = all_entries(catalogue or load_catalogue())
    report: Dict[str, Any] = {"checked": 0, "problems": [], "passed": False}
    for asset in assets:
        asset = Path(asset)
        report["checked"] += 1
        record = read_provenance(asset)
        if record is None:
            report["problems"].append({"asset": str(asset), "problem": "no provenance sidecar"})
            continue
        for key in list(record.get("tools") or []) + list(record.get("models") or []):
            clearance = check_entry(key, entries.get(key))
            if not clearance.cleared:
                report["problems"].append({"asset": str(asset), "problem": f"{key}: {clearance.reason}"})
        for lora in record.get("loras") or []:
            for problem in _lora_problems(lora, bible, entries):
                report["problems"].append({"asset": str(asset), "problem": problem})
        if record.get("third_party_source") and not record.get("third_party_license"):
            report["problems"].append({"asset": str(asset), "problem": "third-party asset without a recorded license"})
    report["passed"] = report["checked"] > 0 and not report["problems"]
    return report
