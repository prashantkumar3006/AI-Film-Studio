"""License gate, provenance and content scan."""

import shutil
import tempfile
import unittest
from pathlib import Path

from studio.common import StudioError
from studio.legal.content import load_denylist, scan_episode, scan_text
from studio.legal.licenses import all_entries, check_entry, load_catalogue, require_cleared
from studio.legal.provenance import read_provenance, release_gate, sidecar_path, write_provenance
from studio.orchestrator.config import _simple_yaml, load_registry
from studio.series.bible import load_bible
from tests.helpers import FIXTURES, REPO


def lic(**kw):
    base = {"commercial_use": "allowed", "verified": True, "source": "https://example.org"}
    base.update(kw)
    return {"_kind": "model", "license": base}


class LicenseRules(unittest.TestCase):
    def test_allowed_needs_verification_and_source(self):
        self.assertTrue(check_entry("x", lic()).cleared)
        self.assertFalse(check_entry("x", lic(verified=False)).cleared)
        self.assertFalse(check_entry("x", lic(source=None)).cleared)

    def test_prohibited_and_unknown_are_blocked(self):
        self.assertFalse(check_entry("x", lic(commercial_use="prohibited")).cleared)
        self.assertFalse(check_entry("x", lic(commercial_use="unknown")).cleared)
        self.assertFalse(check_entry("x", {"_kind": "model"}).cleared)
        self.assertFalse(check_entry("missing", None).cleared)

    def test_conditional_needs_written_and_acknowledged_conditions(self):
        self.assertFalse(check_entry("x", lic(commercial_use="conditional")).cleared)
        self.assertFalse(check_entry("x", lic(commercial_use="conditional", conditions="max 3 people")).cleared)
        self.assertTrue(check_entry("x", lic(commercial_use="conditional", conditions="max 3 people", conditions_acknowledged=True)).cleared)


class RegistryFacts(unittest.TestCase):
    """The registry encodes license facts verified on 2026-10-04."""

    @classmethod
    def setUpClass(cls):
        cls.entries = all_entries(load_catalogue())

    def test_known_non_commercial_entries_are_blocked(self):
        for key in ("tts_f5", "tts_xtts_v2", "music_musicgen", "noobai_xl", "illustrious_xl", "flux1_dev"):
            self.assertFalse(check_entry(key, self.entries[key]).cleared, key)

    def test_verified_permissive_entries_are_cleared(self):
        for key in ("tts_kokoro", "tts_indic_parler", "lipsync_rhubarb", "wan2_2_ti2v_5b", "wan2_2_i2v_a14b", "qwen_image_edit_2509", "blender_mcp"):
            self.assertTrue(check_entry(key, self.entries[key]).cleared, key)

    def test_conditional_entries_wait_for_owner_acknowledgement(self):
        for key in ("motion_remotion", "animagine_xl_4"):
            result = check_entry(key, self.entries[key])
            self.assertFalse(result.cleared)
            self.assertIn("acknowledged", result.reason)

    def test_require_cleared_blocks_in_strict_and_warns_in_exploration(self):
        with self.assertRaises(StudioError):
            require_cleared(["tts_f5"])
        results = require_cleared(["tts_f5"], mode="exploration")
        self.assertFalse(results[0].cleared)

    def test_registry_parses_without_pyyaml(self):
        text = (REPO / "integrations/registry.yaml").read_text(encoding="utf-8")
        simple = _simple_yaml(text)
        import yaml

        full = yaml.safe_load(text)
        for section in ("integrations", "models"):
            self.assertEqual(sorted(simple[section]), sorted(full[section]))
            for key in full[section]:
                self.assertEqual(simple[section][key]["license"]["commercial_use"], full[section][key]["license"]["commercial_use"], key)
                self.assertEqual(bool(simple[section][key]["license"]["verified"]), bool(full[section][key]["license"]["verified"]), key)
        self.assertIn("comfyui", load_registry())


class Provenance(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.bible = load_bible("demo", FIXTURES / "demo")
        self.catalogue = load_catalogue()
        # Pretend the owner acknowledged Animagine's conditions (copy of catalogue only).
        self.catalogue["models"]["animagine_xl_4"]["license"]["conditions_acknowledged"] = True
        self.catalogue["integrations"]["comfyui"]["license"]["verified"] = True

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _asset(self, name="kf.png", **record):
        path = self.tmp / name
        path.write_bytes(b"x")
        base = {"kind": "keyframe", "tools": ["comfyui"], "models": ["animagine_xl_4"]}
        base.update(record)
        write_provenance(path, base, catalogue=self.catalogue)
        return path

    def test_sidecar_round_trip_records_license_snapshot(self):
        asset = self._asset(prompt="girl", seed=7)
        self.assertTrue(sidecar_path(asset).is_file())
        record = read_provenance(asset)
        self.assertEqual(record["seed"], 7)
        self.assertTrue(record["license_snapshot"]["animagine_xl_4"]["cleared"])

    def test_gate_passes_clean_assets(self):
        report = release_gate([self._asset()], bible=self.bible, catalogue=self.catalogue)
        self.assertTrue(report["passed"], report)

    def test_gate_blocks_missing_sidecar_and_blocked_models(self):
        bare = self.tmp / "bare.png"
        bare.write_bytes(b"x")
        bad = self._asset("bad.png", models=["noobai_xl"])
        report = release_gate([bare, bad], bible=self.bible, catalogue=self.catalogue)
        self.assertFalse(report["passed"])
        problems = " ".join(p["problem"] for p in report["problems"])
        self.assertIn("no provenance sidecar", problems)
        self.assertIn("noobai_xl", problems)

    def test_gate_checks_lora_base_model_and_training_data(self):
        ok = self._asset("lora_ok.png", loras=[{"character": "aria", "file": "aria_v001.safetensors"}])
        unknown = self._asset("lora_unknown.png", loras=[{"character": "kael", "file": "kael.safetensors"}])
        self.assertTrue(release_gate([ok], bible=self.bible, catalogue=self.catalogue)["passed"])
        report = release_gate([unknown], bible=self.bible, catalogue=self.catalogue)
        self.assertFalse(report["passed"])
        self.assertIn("not registered in the bible", report["problems"][0]["problem"])

    def test_third_party_assets_need_a_license(self):
        asset = self._asset("stock.png", third_party_source="https://example.org/img")
        self.assertFalse(release_gate([asset], bible=self.bible, catalogue=self.catalogue)["passed"])


class ContentScan(unittest.TestCase):
    def test_flags_franchises_and_styles(self):
        denylist = load_denylist()
        hits = scan_text("Make it look like Naruto, in the style of Studio Ghibli", "x", denylist)
        severities = {h["term"]: h["severity"] for h in hits}
        self.assertEqual(severities["Naruto"], "block")
        self.assertEqual(severities["Studio Ghibli"], "review")

    def test_whole_words_only_and_unicode_safe(self):
        denylist = {"franchises": ["Bleach"], "characters": ["Gojo"]}
        self.assertEqual(scan_text("bleached hair; गोजो नहीं", "x", denylist), [])
        self.assertEqual(len(scan_text("BLEACH fan art", "x", denylist)), 1)

    def test_episode_scan_covers_prompts_and_dialogue(self):
        shotlist = {"scenes": [{"id": "SC01", "shots": [{"id": "SC01_SH001", "visual_prompt": "Goku pose", "dialogue": [{"line": {"en": "Hi Pikachu"}}]}]}]}
        report = scan_episode("clean script", shotlist)
        self.assertFalse(report["passed"])
        self.assertEqual({h["where"] for h in report["hits"]}, {"SC01_SH001.visual_prompt", "SC01_SH001.dialogue.en"})


if __name__ == "__main__":
    unittest.main()
