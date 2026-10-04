"""Feedback system: text metrics, media checks, the quality loop, review."""

import copy
import random
import shutil
import tempfile
import unittest
from pathlib import Path

from studio.budget.ledger import Ledger
from studio.common import load_json
from studio.feedback import review
from studio.feedback.checks import FAIL, PASS, SKIP, run_check
from studio.feedback.loop import APPROVE, HUMAN, REJECT, RETRY, QualityLoop, journal_entries
from studio.feedback.text import char_error_rate, dialogue_error, normalize, word_error_rate
from studio.legal.licenses import load_catalogue
from studio.legal.provenance import write_provenance
from studio.orchestrator.config import load_config
from studio.series.bible import load_bible
from tests.helpers import FIXTURES, make_color_image, make_image, make_tone, make_video, needs_ffmpeg


class TextMetrics(unittest.TestCase):
    def test_normalize_keeps_devanagari_marks(self):
        self.assertEqual(normalize("यह अभी भी जल रहा है।"), "यह अभी भी जल रहा है")
        self.assertEqual(normalize("It's still burning, GOOD!"), "it s still burning good")

    def test_wer_and_cer(self):
        self.assertEqual(word_error_rate("it is still burning", "it is still burning"), 0.0)
        self.assertEqual(word_error_rate("it is still burning", "it is burning"), 0.25)
        self.assertLess(char_error_rate("जल रहा है", "जलरहा है"), 0.01)

    def test_hindi_uses_the_kinder_metric(self):
        scores = dialogue_error("यह अभी भी जल रहा है", "यह अभीभी जल रहा है", "hi")
        self.assertGreater(scores["wer"], 0.3)
        self.assertEqual(scores["error"], scores["cer"])


@needs_ffmpeg
class MediaChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.config = load_config()
        cls.good = make_video(cls.tmp / "good.mp4", 2.0, "1920x1080", 24)
        cls.wrong = make_video(cls.tmp / "wrong.mp4", 2.0, "640x360", 30)
        cls.black = make_video(cls.tmp / "black.mp4", 2.0, "1920x1080", 24, source="color=c=black")
        cls.tone = make_tone(cls.tmp / "tone.wav", 3.0, volume_db=-3)
        cls.hot = make_tone(cls.tmp / "hot.wav", 1.0, volume_db=24)  # lavfi sine is -18 dBFS; +24 dB clips
        cls.image = make_image(cls.tmp / "kf.png", "1344x768")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def ctx(self, **kw):
        base = {"config": self.config}
        base.update(kw)
        return base

    def test_tech_video(self):
        self.assertEqual(run_check("tech_video", self.good, self.ctx(shot={"duration_s": 2.0})).status, PASS)
        result = run_check("tech_video", self.wrong, self.ctx(shot={"duration_s": 4.0}))
        self.assertEqual(result.status, FAIL)
        for part in ("resolution 640x360", "fps 30", "duration"):
            self.assertIn(part, result.detail)

    def test_tech_image_minimum_height(self):
        self.assertEqual(run_check("tech_image", self.image, self.ctx()).status, FAIL)  # 768 < 1024
        cfg = copy.deepcopy(self.config)
        cfg["feedback"]["thresholds"]["min_image_height"] = 720
        self.assertEqual(run_check("tech_image", self.image, {"config": cfg}).status, PASS)

    def test_black_frames(self):
        self.assertEqual(run_check("black_frames", self.black, self.ctx()).status, FAIL)
        self.assertEqual(run_check("black_frames", self.good, self.ctx()).status, PASS)

    def test_voice_peak(self):
        self.assertEqual(run_check("voice_peak", self.tone, self.ctx()).status, PASS)
        self.assertEqual(run_check("voice_peak", self.hot, self.ctx()).status, FAIL)

    def test_loudness_against_target(self):
        result = run_check("loudness", self.tone, self.ctx())
        self.assertEqual(result.status, FAIL)  # a raw -3 dB tone is far louder than -14 LUFS
        self.assertIsNotNone(result.score)

    def test_dialogue_accuracy_with_fake_transcriber(self):
        hear = lambda path, language: "it is still burning good"  # noqa: E731
        ok = run_check("dialogue_accuracy", self.tone, self.ctx(expected_text="It is still burning. Good.", transcribe=hear, language="en"))
        self.assertEqual(ok.status, PASS)
        bad = run_check("dialogue_accuracy", self.tone, self.ctx(expected_text="It is still burning. Good.", transcribe=lambda p, l: "it burning", language="en"))
        self.assertEqual(bad.status, FAIL)
        self.assertEqual(run_check("dialogue_accuracy", self.tone, self.ctx(expected_text="x")).status, SKIP)

    def test_palette_with_pillow(self):
        try:
            import PIL  # noqa: F401
        except ImportError:
            self.skipTest("Pillow not installed")
        blue = make_color_image(self.tmp / "blue.png", "0x3D6E8C")
        self.assertEqual(run_check("palette", blue, self.ctx(palette=["#3D6E8C"])).status, PASS)
        self.assertEqual(run_check("palette", blue, self.ctx(palette=["#E3A13B"])).status, FAIL)

    def test_identity_uses_scorer_and_per_character_threshold(self):
        bible = load_bible("demo", FIXTURES / "demo")
        sheet = bible.reference_path("refs/aria/model_sheet_v001.png")
        sheet.parent.mkdir(parents=True, exist_ok=True)
        created = not sheet.exists()
        if created:
            make_color_image(sheet, "0x3D6E8C")
        try:
            high = run_check("identity", self.image, self.ctx(bible=bible, characters=["aria"], identity_scorer=lambda a, r, c: 0.9))
            low = run_check("identity", self.image, self.ctx(bible=bible, characters=["aria"], identity_scorer=lambda a, r, c: 0.7))
            none = run_check("identity", self.image, self.ctx(bible=bible, characters=["aria"]))
        finally:
            if created:
                shutil.rmtree(sheet.parent)
        self.assertEqual(high.status, PASS)
        self.assertEqual(low.status, FAIL)
        self.assertEqual(none.status, SKIP)

    def test_a_crashing_check_is_contained(self):
        result = run_check("identity", self.image, self.ctx(bible=load_bible("demo", FIXTURES / "demo"), characters=["aria"], identity_scorer=lambda *a: 1 / 0))
        self.assertIn(result.status, {"error", "skip"})


class Loop(unittest.TestCase):
    """The loop is tested with fake checks so it is fast and deterministic."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.config = copy.deepcopy(load_config())
        self.config["feedback"]["required_checks"] = {"keyframe": ["identity", "provenance"]}
        self.catalogue = load_catalogue()
        self.catalogue["integrations"]["comfyui"]["license"]["verified"] = True
        self.catalogue["models"]["animagine_xl_4"]["license"]["conditions_acknowledged"] = True
        self.bible = load_bible("demo", FIXTURES / "demo")
        self.sheet = self.tmp / "sheet.png"
        self.sheet.write_bytes(b"ref")
        self.bible.reference_path = lambda rel: self.sheet  # point every model sheet at a temp file

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def generator(self, models=("animagine_xl_4",)):
        def generate(params, attempt):
            path = self.tmp / f"kf_{attempt}.png"
            path.write_bytes(b"img")
            write_provenance(path, {"kind": "keyframe", "tools": ["comfyui"], "models": list(models), "seed": params["seed"]}, catalogue=self.catalogue)
            return path

        return generate

    def ctx(self, scores):
        it = iter(scores)
        return {"bible": self.bible, "characters": ["aria"], "identity_scorer": lambda a, r, c: next(it), "catalogue": self.catalogue, "shot": {"id": "SC01_SH002"}}

    def test_retry_then_approve_with_adjusted_params(self):
        loop = QualityLoop(self.tmp, self.config)
        verdict = loop.run("keyframe", self.generator(), self.ctx([0.70, 0.86]), params={"lora_weight": 0.8, "seed": 1}, rng=random.Random(0))
        self.assertEqual(verdict.decision, APPROVE)
        self.assertEqual(verdict.attempt, 2)
        attempts = journal_entries(self.tmp)
        self.assertEqual([a["decision"] for a in attempts], [RETRY, APPROVE])
        record = load_json(self.tmp / "kf_2.png.prov.json")
        self.assertNotEqual(record["seed"], 1, "a retry must use a new seed")

    def test_adjust_raises_lora_weight_within_limits(self):
        loop = QualityLoop(self.tmp, self.config)
        verdict = loop.evaluate(self.generator()({"seed": 1}, 1), "keyframe", self.ctx([0.5]))
        nxt = loop.adjust({"lora_weight": 1.25, "reference_strength": 0.5, "seed": 1}, verdict, random.Random(1))
        self.assertEqual(nxt["lora_weight"], 1.3)  # clamped
        self.assertEqual(nxt["reference_strength"], 0.6)

    def test_gives_up_to_human_after_max_attempts(self):
        self.config["feedback"]["max_attempts"]["keyframe"] = 3
        loop = QualityLoop(self.tmp, self.config)
        verdict = loop.run("keyframe", self.generator(), self.ctx([0.5, 0.5, 0.5]), rng=random.Random(0))
        self.assertEqual((verdict.decision, verdict.attempt), (HUMAN, 3))
        queue = load_json(self.tmp / "20_qc/feedback/review_queue.json")
        self.assertEqual(queue[-1]["decision"], HUMAN)

    def test_blocked_model_is_rejected_not_retried(self):
        loop = QualityLoop(self.tmp, self.config)
        verdict = loop.run("keyframe", self.generator(models=("noobai_xl",)), self.ctx([0.95]), rng=random.Random(0))
        self.assertEqual((verdict.decision, verdict.attempt), (REJECT, 1))

    def test_unmeasured_required_check_goes_to_human(self):
        loop = QualityLoop(self.tmp, self.config)
        ctx = self.ctx([0.9])
        ctx.pop("identity_scorer")
        verdict = loop.run("keyframe", self.generator(), ctx, rng=random.Random(0))
        self.assertEqual(verdict.decision, HUMAN)
        self.assertIn("not measured", verdict.reasons[0])

    def test_budget_guard_stops_the_loop(self):
        ledger = Ledger(self.tmp, self.config)
        ledger.log_manual(4995, "spent")
        loop = QualityLoop(self.tmp, self.config, ledger)
        verdict = loop.run("keyframe", self.generator(), self.ctx([0.9]), cost_per_attempt_inc_gst=20, rng=random.Random(0))
        self.assertEqual(verdict.decision, HUMAN)
        self.assertIn("Budget guard", verdict.reasons[0])


class Review(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _journal(self, asset, score):
        import json

        folder = self.tmp / "20_qc/feedback"
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / "journal.jsonl").open("a") as handle:
            handle.write(json.dumps({"asset": asset, "kind": "keyframe", "decision": "approve", "attempt": 1, "shot_id": asset, "results": [{"name": "identity", "status": "pass", "score": score}]}) + "\n")

    def test_calibration_proposes_threshold_between_liked_and_disliked(self):
        for i, (score, rating) in enumerate([(0.95, 5), (0.92, 4), (0.90, 5), (0.84, 2), (0.83, 1), (0.85, 2)]):
            self._journal(f"a{i}", score)
            review.rate(self.tmp, f"a{i}", rating)
        suggestion = review.calibrate_thresholds(self.tmp)["identity"]
        self.assertEqual(suggestion["status"], "suggest")
        self.assertAlmostEqual(suggestion["threshold"], (0.92 + 0.84) / 2, places=3)

    def test_calibration_detects_useless_metric(self):
        for i, (score, rating) in enumerate([(0.80, 5), (0.81, 5), (0.82, 4), (0.95, 1), (0.94, 2), (0.96, 1)]):
            self._journal(f"b{i}", score)
            review.rate(self.tmp, f"b{i}", rating)
        self.assertEqual(review.calibrate_thresholds(self.tmp)["identity"]["status"], "check does not predict human judgement")

    def test_report_and_lessons(self):
        self._journal("x", 0.9)
        report = review.episode_report(self.tmp)
        self.assertEqual(report["first_pass_rate"], 1.0)
        path = review.add_lesson(self.tmp, "Kael's coat drifts red-orange", "continuity", "add palette emphasis for kael")
        self.assertIn("Kael's coat", path.read_text())


if __name__ == "__main__":
    unittest.main()
