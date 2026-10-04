"""Bible and shot-list validation."""

import copy
import json
import unittest

from studio.legal.licenses import all_entries, load_catalogue
from studio.series.bible import load_bible, validate_bible
from studio.series.shotlist import dialogue_lines, summarize, validate_shotlist
from tests.helpers import FIXTURES


def errors(issues):
    return [i for i in issues if i.level == "error"]


class BibleValidation(unittest.TestCase):
    def setUp(self):
        self.bible = load_bible("demo", FIXTURES / "demo")

    def test_demo_bible_has_no_errors(self):
        issues = validate_bible(self.bible, all_entries(load_catalogue()))
        self.assertEqual(errors(issues), [], [i.as_dict() for i in issues])
        warnings = " ".join(i.message for i in issues)
        self.assertIn("status is 'draft'", warnings)  # kael is not approved yet

    def test_bad_palette_and_missing_voice_are_errors(self):
        self.bible.characters["aria"]["palette"]["hair"] = "silver"
        del self.bible.characters["kael"]["voice"]["hi"]
        messages = " ".join(i.message for i in errors(validate_bible(self.bible)))
        self.assertIn("is not #RRGGBB", messages)
        self.assertIn("no voice defined for language 'hi'", messages)

    def test_unknown_engine_and_unconsented_clone_are_errors(self):
        self.bible.characters["aria"]["voice"]["en"] = {"engine": "nope", "clone_of_real_person": True}
        messages = " ".join(i.message for i in errors(validate_bible(self.bible, all_entries(load_catalogue()))))
        self.assertIn("'nope' is not in integrations/registry.yaml", messages)
        self.assertIn("no consent_record", messages)


class ShotlistValidation(unittest.TestCase):
    def setUp(self):
        self.bible = load_bible("demo", FIXTURES / "demo")
        self.shotlist = json.loads((FIXTURES / "demo/episodes/E01/shotlist.json").read_text())

    def test_demo_shotlist_is_valid(self):
        issues = validate_shotlist(self.shotlist, self.bible)
        self.assertEqual(errors(issues), [], [i.as_dict() for i in issues])

    def test_summary(self):
        s = summarize(self.shotlist)
        self.assertEqual(s["shots"], 4)
        self.assertEqual(s["runtime_s"], 57.0)
        self.assertEqual(s["by_motion"]["full"]["shots"], 1)
        self.assertAlmostEqual(s["full_video_ratio"], 5 / 57, places=3)

    def test_dialogue_lines_have_stable_ids_per_language(self):
        en = dialogue_lines(self.shotlist, "en")
        hi = dialogue_lines(self.shotlist, "hi")
        self.assertEqual([l["line_id"] for l in en], ["SC01_SH002_L01", "SC01_SH003_L01"])
        self.assertEqual([l["line_id"] for l in en], [l["line_id"] for l in hi])
        self.assertIn("जल रहा", hi[0]["text"])

    def test_catches_continuity_errors(self):
        bad = copy.deepcopy(self.shotlist)
        shot = bad["scenes"][0]["shots"][1]
        shot["characters"] = [{"id": "aria", "outfit": "swimsuit"}, {"id": "ghost"}]
        shot["dialogue"][0]["line"].pop("hi")
        bad["scenes"][0]["location"] = "moon"
        bad["scenes"][0]["shots"][2]["id"] = "SC02_SH003"
        messages = " ".join(i.message for i in errors(validate_shotlist(bad, self.bible)))
        for expected in ("outfit 'swimsuit'", "'ghost' is not in the bible", "missing 'hi' text", "location 'moon'", "must start with its scene id"):
            self.assertIn(expected, messages)

    def test_full_motion_policy_limit(self):
        heavy = copy.deepcopy(self.shotlist)
        for shot in heavy["scenes"][0]["shots"]:
            shot["motion"] = "full"
        messages = " ".join(i.message for i in errors(validate_shotlist(heavy, self.bible)))
        self.assertIn("policy limit is 30%", messages)

    def test_dialogue_too_long_for_shot_warns(self):
        tight = copy.deepcopy(self.shotlist)
        tight["scenes"][0]["shots"][2]["duration_s"] = 0.6
        warnings = " ".join(i.message for i in validate_shotlist(tight, self.bible) if i.level == "warning")
        self.assertIn("lengthen or split", warnings)


if __name__ == "__main__":
    unittest.main()
