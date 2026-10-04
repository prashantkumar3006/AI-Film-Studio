"""Text metrics for dialogue QC: does the generated voice say the script?

TTS engines skip words, repeat words and mispronounce names. Running
speech-to-text on every generated line and comparing it to the script
catches that automatically. Hindi uses character error rate as well,
because transcribers split and join Devanagari words inconsistently.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Dict, List

_SPACE = re.compile(r"\s+")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text or "").lower()
    text = text.replace("।", " ").replace("॥", " ")
    # \w keeps Devanagari letters, but combining vowel signs (matras) are
    # category Mn/Mc, so strip punctuation without touching marks.
    text = "".join(ch if (ch.isalnum() or ch.isspace() or unicodedata.category(ch).startswith("M")) else " " for ch in text)
    return _SPACE.sub(" ", text).strip()


def _edit_distance(a: List[str], b: List[str]) -> int:
    previous = list(range(len(b) + 1))
    for i, x in enumerate(a, start=1):
        current = [i] + [0] * len(b)
        for j, y in enumerate(b, start=1):
            current[j] = min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (x != y))
        previous = current
    return previous[-1]


def word_error_rate(reference: str, hypothesis: str) -> float:
    ref = normalize(reference).split()
    hyp = normalize(hypothesis).split()
    if not ref:
        return 0.0 if not hyp else 1.0
    return _edit_distance(ref, hyp) / len(ref)


def char_error_rate(reference: str, hypothesis: str) -> float:
    ref = list(normalize(reference).replace(" ", ""))
    hyp = list(normalize(hypothesis).replace(" ", ""))
    if not ref:
        return 0.0 if not hyp else 1.0
    return _edit_distance(ref, hyp) / len(ref)


def dialogue_error(reference: str, hypothesis: str, language: str) -> Dict[str, float]:
    """The score the QC check uses: WER for English, the lower of WER/CER for Hindi."""
    wer = word_error_rate(reference, hypothesis)
    cer = char_error_rate(reference, hypothesis)
    score = min(wer, cer) if language == "hi" else wer
    return {"wer": round(wer, 3), "cer": round(cer, 3), "error": round(score, 3)}
