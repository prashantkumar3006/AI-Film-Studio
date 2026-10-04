"""ffmpeg edit tools and lip-sync composition on synthetic media."""

import shutil
import tempfile
import unittest
from pathlib import Path

from integrations.edit.assemble import assemble
from integrations.edit.camera import MOVES, still_to_clip
from integrations.edit.mix import mix
from integrations.edit.package import package
from integrations.edit.subtitles import write_srt
from integrations.lipsync import compose
from integrations.lipsync.rhubarb import build_command
from studio.common import StudioError
from studio.feedback import media
from studio.orchestrator.anime import build_edl, dialogue_timeline, retime_shots
from tests.helpers import make_color_image, make_image, make_tone, make_video, needs_ffmpeg


@needs_ffmpeg
class EditTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.key = make_image(cls.tmp / "key.png", "1920x1080")
        cls.gen = make_video(cls.tmp / "gen.mp4", 3.0, "1280x720", 16)
        cls.line = make_tone(cls.tmp / "line.wav", 1.5, 300, -3)
        cls.music = make_tone(cls.tmp / "music.wav", 8.0, 500, -3)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_every_camera_move_renders_exact_frames(self):
        for move in MOVES:
            out = still_to_clip(self.key, self.tmp / f"{move}.mp4", 1.0, move)
            info = media.probe(out)["video"]
            self.assertEqual((info["width"], info["height"], info["fps"]), (1920, 1080, 24.0), move)
            self.assertEqual(info["frames"], 24, move)
        with self.assertRaises(StudioError):
            still_to_clip(self.key, self.tmp / "x.mp4", 1.0, "barrel_roll")

    def test_assemble_normalises_and_keeps_exact_duration(self):
        cam = still_to_clip(self.key, self.tmp / "a.mp4", 2.0, "push_in")
        edl = {"fps": 24, "resolution": "1920x1080", "clips": [
            {"shot_id": "SC01_SH001", "path": str(cam), "duration_s": 2.0},
            {"shot_id": "SC01_SH002", "path": str(self.gen), "duration_s": 5.0},  # shorter source: padded
            {"shot_id": "SC01_SH003", "path": str(cam), "duration_s": 1.0},  # longer source: trimmed
        ]}
        out = self.tmp / "picture.mp4"
        assemble(edl, out, self.tmp / "work")
        info = media.probe(out)
        self.assertEqual(info["video"]["frames"], 8 * 24)
        self.assertAlmostEqual(info["duration_s"], 8.0, delta=0.05)
        with self.assertRaises(StudioError):
            assemble({"clips": [{"path": "/nope.mp4", "duration_s": 1}]}, out)

    def test_mix_hits_loudness_target_and_length(self):
        out = mix({"dialogue": [{"path": str(self.line), "start_s": 1.0}], "music": [{"path": str(self.music), "start_s": 0.0, "gain_db": -6}]}, self.tmp / "mix.wav", 7.0)
        loud = media.loudness(out)
        self.assertAlmostEqual(loud["integrated_lufs"], -14.0, delta=1.0)
        self.assertLessEqual(loud["true_peak_dbtp"], -0.9)
        self.assertAlmostEqual(media.probe(out)["duration_s"], 7.0, delta=0.05)

    def test_package_keeps_full_length_and_language_tags(self):
        picture = still_to_clip(self.key, self.tmp / "p.mp4", 6.0, "static")
        audio = mix({"music": [{"path": str(self.music), "start_s": 0}]}, self.tmp / "m.wav", 6.0)
        en = write_srt([{"start_s": 1.0, "end_s": 2.0, "text": "Hello"}], self.tmp / "en.srt")
        hi = write_srt([{"start_s": 1.0, "end_s": 2.0, "text": "नमस्ते"}], self.tmp / "hi.srt")
        out = package(picture, [(audio, "en"), (audio, "hi")], [(en, "en"), (hi, "hi")], self.tmp / "final.mp4")
        info = media.probe(out)
        self.assertAlmostEqual(info["duration_s"], 6.0, delta=0.1)  # not cut at the last subtitle
        self.assertEqual([a["language"] for a in info["audio"]], ["eng", "hin"])

    def test_lipsync_compose_switches_mouth_frames(self):
        frames = {shape: make_color_image(self.tmp / f"mouth_{shape}.png", color, "1920x1080") for shape, color in (("A", "black"), ("C", "gray"), ("D", "white"))}
        cues = [{"start": 0.0, "end": 0.5, "value": "X"}, {"start": 0.5, "end": 1.0, "value": "D"}, {"start": 1.0, "end": 1.5, "value": "G"}]
        segments = compose.timeline(cues, frames, 2.0, fps=24, on=2)
        self.assertEqual(sum(s["frames"] for s in segments), 48)
        self.assertTrue(all(s["frames"] >= 2 for s in segments[:-1]), "mouths animate on twos")
        # X (rest) -> A, D stays D, G (F/V) -> B is missing so closed A, merged with the rest.
        self.assertEqual([s["shape"] for s in segments], ["A", "D", "A"])
        out = compose.render(segments, frames, self.tmp / "talk.mp4")
        self.assertEqual(media.probe(out)["video"]["frames"], 48)


class PureLogic(unittest.TestCase):
    def test_fallback_mouth_shapes(self):
        frames = {k: Path(k) for k in ("A", "B", "C", "D")}
        self.assertEqual(compose.resolve_shape("X", frames), "A")
        self.assertEqual(compose.resolve_shape("G", frames), "B")
        self.assertEqual(compose.resolve_shape("F", frames), "D")  # F -> E -> D
        with self.assertRaises(StudioError):
            compose.resolve_shape("A", {"B": Path("b")})

    def test_rhubarb_uses_phonetic_for_hindi(self):
        en = build_command(Path("a.wav"), Path("o.json"), "en", "hello", dialog_file=Path("d.txt"))
        hi = build_command(Path("a.wav"), Path("o.json"), "hi", "नमस्ते", dialog_file=Path("d.txt"))
        self.assertNotIn("phonetic", en)
        self.assertIn("--dialogFile", en)
        self.assertEqual(hi[hi.index("--recognizer") + 1], "phonetic")
        self.assertNotIn("--dialogFile", hi)

    def test_srt_wrapping_and_timestamps(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            out = write_srt([{"start_s": 3661.5, "end_s": 3663.5, "text": "word " * 30}], tmp / "x.srt", 42, 2)
            text = out.read_text()
            self.assertIn("01:01:01,500 -->", text)
            self.assertTrue(all(len(line) <= 42 for line in text.splitlines()))
        finally:
            shutil.rmtree(tmp)

    def test_dialogue_timeline_and_retiming(self):
        shotlist = {"scenes": [{"id": "SC01", "shots": [
            {"id": "SC01_SH001", "duration_s": 2.0, "dialogue": [{"character": "a", "line": {"en": "one"}}, {"character": "a", "line": {"en": "two"}}]},
            {"id": "SC01_SH002", "duration_s": 3.0, "dialogue": []},
        ]}]}
        timeline = dialogue_timeline(shotlist, "en", {"SC01_SH001_L01": 1.0, "SC01_SH001_L02": 1.5})
        self.assertEqual([t["start_s"] for t in timeline], [0.25, 1.45])
        self.assertGreater(timeline[1]["overflow_s"], 0)
        changes = retime_shots(shotlist, timeline)
        self.assertEqual(list(changes), ["SC01_SH001"])
        self.assertGreaterEqual(changes["SC01_SH001"], 3.35)
        self.assertEqual(round(changes["SC01_SH001"] * 24, 6) % 1, 0)  # whole frames
        edl = build_edl(shotlist, {"SC01_SH001": "a.mp4"})
        self.assertEqual(edl["missing"], ["SC01_SH002"])


if __name__ == "__main__":
    unittest.main()
