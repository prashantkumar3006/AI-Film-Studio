"""Anime character identity scoring with CCIP from deepghs/imgutils (MIT code).

CCIP (Contrastive Character Image Pretraining) is trained specifically
to tell whether two anime images show the same character, which generic
face recognition cannot do on stylised faces. It runs on CPU via ONNX,
so identity QC works on a laptop.

Install: ``pip install dghs-imgutils``. The CCIP model weights download
from Hugging Face on first use; their license is recorded separately in
the registry (``identity_ccip``) — check it before relying on it.

Score returned is a similarity in 0..1 (``1 - ccip_difference``).
imgutils treats two images as the same character when the difference is
below about 0.18, i.e. a similarity above about 0.82.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional


def available() -> bool:
    try:
        import imgutils.metrics  # type: ignore  # noqa: F401
    except ImportError:
        return False
    return True


def _crops(image: Path):
    """Person crops when several characters share a frame, else the image."""
    try:
        from imgutils.detect import detect_person  # type: ignore
        from PIL import Image  # type: ignore
    except ImportError:
        return [str(image)]
    picture = Image.open(image).convert("RGB")
    boxes = [box for box, _, score in detect_person(picture) if score >= 0.4]
    if len(boxes) <= 1:
        return [picture]
    return [picture.crop(tuple(int(v) for v in box)) for box in boxes]


def similarity(image: Path, reference: Path, character_id: str = "") -> float:
    from imgutils.metrics import ccip_difference  # type: ignore

    best = 0.0
    for crop in _crops(Path(image)):
        diff = float(ccip_difference(crop, str(reference)))
        best = max(best, 1.0 - diff)
    return round(best, 4)


def scorer() -> Optional[Callable[[Path, Path, str], float]]:
    return similarity if available() else None
