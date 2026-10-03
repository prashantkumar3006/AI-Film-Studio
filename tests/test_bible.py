"""
Step 1.1 done-test: the validator accepts the one valid Bible and rejects each
of the five deliberately broken ones for the right reason.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from studio.bible import load_bible, validate_bible
from studio.cli import main as cli_main

REPO = Path(__file__).resolve().parents[1]
VALID = REPO / "examples" / "ep00" / "bible.json"
BROKEN = REPO / "tests" / "fixtures" / "bible_broken"

# fixture file -> words that must appear in one of its errors
EXPECTED = {
    "01_missing_scenes.json": "'scenes' is a required property",
    "02_bad_shot_id.json": "does not match",
    "03_unknown_character.json": "CH_ARJUN is not defined",
    "04_missing_hindi_text.json": "missing text for hi",
    "05_duplicate_shot_id.json": "duplicate id 'EP00_SC01_SH002'",
}


def test_valid_bible_passes():
    report = validate_bible(load_bible(VALID))
    assert report.ok, report.errors


def test_exactly_five_broken_fixtures_exist():
    assert sorted(p.name for p in BROKEN.glob("*.json")) == sorted(EXPECTED)


@pytest.mark.parametrize("name,expected", sorted(EXPECTED.items()))
def test_broken_bible_is_rejected_for_the_right_reason(name, expected):
    report = validate_bible(load_bible(BROKEN / name))
    assert not report.ok, f"{name} should be invalid"
    assert any(expected in e for e in report.errors), report.errors


def test_cli_exit_codes(capsys):
    assert cli_main(["validate", str(VALID)]) == 0
    assert cli_main(["validate", "ep00"]) == 0  # found under examples/
    assert cli_main(["validate", str(BROKEN / "03_unknown_character.json")]) == 1
    assert cli_main(["validate", "no-such-episode"]) == 2
