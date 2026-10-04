"""License clearance for every tool and model in ``integrations/registry.yaml``.

Each catalogue entry carries a ``license`` block::

    license:
      code: Apache-2.0
      weights: Apache-2.0
      commercial_use: allowed      # allowed | conditional | prohibited | unknown
      conditions: null             # required text when conditional
      conditions_acknowledged: false
      verified: true               # someone read the license at `source`
      verified_on: 2026-10-04
      source: https://...

Clearance rule (deliberately strict):

* ``allowed``      -> cleared only if ``verified``
* ``conditional``  -> cleared only if ``verified`` and ``conditions_acknowledged``
* ``prohibited`` / ``unknown`` / missing -> blocked

Unknown is treated exactly like prohibited. "Probably fine" is how
channels get demonetised or sued.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from studio.common import INTEGRATIONS_ROOT, StudioError, load_yaml

COMMERCIAL_VALUES = {"allowed", "conditional", "prohibited", "unknown"}
REGISTRY_PATH = INTEGRATIONS_ROOT / "registry.yaml"


@dataclass
class Clearance:
    key: str
    kind: str  # "integration" | "model"
    cleared: bool
    reason: str
    commercial_use: str
    verified: bool

    def as_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "kind": self.kind,
            "cleared": self.cleared,
            "reason": self.reason,
            "commercial_use": self.commercial_use,
            "verified": self.verified,
        }


def load_catalogue(path: Optional[Path] = None) -> Dict[str, Dict[str, Dict[str, Any]]]:
    data = load_yaml(Path(path) if path else REGISTRY_PATH)
    return {
        "integrations": data.get("integrations") or {},
        "models": data.get("models") or {},
    }


def all_entries(catalogue: Dict[str, Dict[str, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
    """Flatten integrations and models into one {key: entry} map."""
    merged: Dict[str, Dict[str, Any]] = {}
    for kind in ("integrations", "models"):
        for key, entry in (catalogue.get(kind) or {}).items():
            if key in merged:
                raise StudioError(f"Registry key '{key}' is used for both an integration and a model.")
            item = dict(entry or {})
            item["_kind"] = "integration" if kind == "integrations" else "model"
            merged[key] = item
    return merged


def check_entry(key: str, entry: Optional[Dict[str, Any]]) -> Clearance:
    if entry is None:
        return Clearance(key, "unknown", False, "not in integrations/registry.yaml", "unknown", False)
    kind = entry.get("_kind", "integration")
    lic = entry.get("license") or {}
    use = str(lic.get("commercial_use") or "unknown").lower()
    verified = bool(lic.get("verified"))
    if use not in COMMERCIAL_VALUES:
        return Clearance(key, kind, False, f"commercial_use '{use}' is not a known value", use, verified)
    if use == "prohibited":
        return Clearance(key, kind, False, "license prohibits commercial use", use, verified)
    if use == "unknown":
        return Clearance(key, kind, False, "commercial use not established", use, verified)
    if not verified:
        return Clearance(key, kind, False, "license not yet verified against its source", use, verified)
    if not lic.get("source"):
        return Clearance(key, kind, False, "verified but no license source URL recorded", use, verified)
    if use == "conditional":
        if not lic.get("conditions"):
            return Clearance(key, kind, False, "conditional but conditions are not written down", use, verified)
        if not lic.get("conditions_acknowledged"):
            return Clearance(key, kind, False, "conditions not acknowledged by the owner", use, verified)
        return Clearance(key, kind, True, f"cleared with conditions: {lic['conditions']}", use, verified)
    return Clearance(key, kind, True, "cleared", use, verified)


def check_keys(keys: Iterable[str], catalogue=None) -> List[Clearance]:
    entries = all_entries(catalogue or load_catalogue())
    return [check_entry(key, entries.get(key)) for key in keys]


def require_cleared(keys: Iterable[str], mode: str = "strict", catalogue=None) -> List[Clearance]:
    """Raise unless every key is cleared. ``exploration`` mode only warns.

    Used before spending GPU money: there is no point generating footage
    that can never be released.
    """
    results = check_keys(keys, catalogue)
    blocked = [r for r in results if not r.cleared]
    if blocked and mode != "exploration":
        details = "; ".join(f"{r.key}: {r.reason}" for r in blocked)
        raise StudioError(f"License gate blocked: {details}")
    return results
