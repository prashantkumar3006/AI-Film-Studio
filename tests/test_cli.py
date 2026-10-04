"""End-to-end: the real `python -m studio` commands in a throwaway repo copy."""

import json
import unittest

from tests.helpers import HAS_FFMPEG, RepoCopy, make_tone


class CliEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepoCopy(with_demo=True)
        # Give the demo episode an engine project.
        meta = cls.repo.root / "series/demo/episodes/E01/episode.yaml"
        done = cls.repo.run("scripts/create_project.py", "init", "--title", "Demo E01", "--type", "animation", "--fps", "24", check=True)
        location = [l for l in done.stdout.splitlines() if l.strip().startswith("Location")][0].split(":", 1)[1].strip()
        rel = location.split("/repo/", 1)[1]
        meta.write_text(f"series: demo\nnumber: 1\ntitle: The Last Lantern\nstatus: WRITING\nlanguages: [en, hi]\nproject_root: {rel}\n", encoding="utf-8")
        cls.project = cls.repo.root / rel

    @classmethod
    def tearDownClass(cls):
        cls.repo.cleanup()

    def studio_json(self, *args, ok=True):
        done = self.repo.studio("--json", *args)
        if ok:
            self.assertEqual(done.returncode, 0, f"{args}\n{done.stdout}\n{done.stderr}")
        return json.loads(done.stdout) if done.stdout.strip().startswith(("{", "[")) else done

    def test_series_check_and_shots_check(self):
        report = self.studio_json("series", "check", "demo")
        self.assertTrue(report["ok"])
        shots = self.studio_json("shots", "check", "demo", "1")
        self.assertTrue(shots["ok"])
        self.assertTrue((self.project / "20_qc/shotlist_check.json").is_file())

    def test_estimate_writes_budget_file(self):
        result = self.studio_json("estimate", "demo", "1")
        self.assertTrue(result["within_cap"])
        self.assertTrue((self.project / "00_admin/budget/estimate.json").is_file())

    def test_legal_scan_flags_ip_in_prompts(self):
        self.assertTrue(self.studio_json("legal", "scan", "demo", "1")["passed"])
        shotlist = self.repo.root / "series/demo/episodes/E01/shotlist.json"
        original = shotlist.read_text(encoding="utf-8")
        try:
            shotlist.write_text(original.replace("lands on rooftop", "lands like Goku on rooftop"), encoding="utf-8")
            done = self.repo.studio("--json", "legal", "scan", "demo", "1")
            self.assertEqual(done.returncode, 1)
            self.assertIn("Goku", done.stdout)
        finally:
            shotlist.write_text(original, encoding="utf-8")

    def test_legal_check_verify_and_acknowledge(self):
        before = {r["key"]: r for r in self.studio_json("legal", "check")}
        self.assertFalse(before["motion_remotion"]["cleared"])
        self.studio_json("legal", "acknowledge", "motion_remotion")
        after = self.studio_json("legal", "check", "motion_remotion")[0]
        self.assertTrue(after["cleared"])
        self.studio_json("legal", "verify", "edit_ffmpeg", "--source", "https://ffmpeg.org/legal.html", "--commercial-use", "allowed")
        self.assertTrue(self.studio_json("legal", "check", "edit_ffmpeg")[0]["cleared"])
        registry = (self.repo.root / "integrations/registry.yaml").read_text()
        self.assertIn("# AI FILM STUDIO - INTEGRATION & MODEL REGISTRY", registry, "comments survive targeted edits")

    def test_release_gate_blocks_media_without_provenance(self):
        clip = self.project / "10_animation/clips/SC01_SH001.mp4"
        clip.parent.mkdir(parents=True, exist_ok=True)
        clip.write_bytes(b"not really a video")
        done = self.repo.studio("--json", "legal", "release-gate", "demo", "1")
        self.assertEqual(done.returncode, 1)
        report = json.loads(done.stdout)
        self.assertFalse(report["passed"])
        self.assertIn("no provenance sidecar", report["problems"][0]["problem"])
        clip.unlink()

    def test_voice_plan_lists_every_line_per_language(self):
        planned = self.studio_json("voice", "demo", "1")
        self.assertEqual(len(planned), 4)
        self.assertEqual({p["engine"] for p in planned}, {"tts_kokoro", "tts_indic_parler"})

    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
    def test_timing_lengthens_shots_to_fit_recorded_lines(self):
        line = self.project / "14_sound/dialogue/en/SC01_SH003_L01.wav"
        make_tone(line, 6.0)  # longer than the 5 s shot
        result = self.studio_json("timing", "demo", "1", "--language", "en")
        self.assertIn("SC01_SH003", result["lengthen_shots"])
        self.assertIn("SC01_SH002_L01", result["missing_audio"])
        line.unlink()

    def test_pipeline_status_points_to_next_stage(self):
        data = self.studio_json("pipeline", "status", "demo", "1")
        done = {row["stage"]: row["done"] for row in data["stages"]}
        self.assertTrue(done["story"])
        self.assertTrue(done["shotlist"])
        self.assertIsNotNone(data["next"])

    def test_qc_and_compute_session_commands(self):
        self.studio_json("compute", "start", "demo", "1", "--gpu", "rtx_4090")
        self.assertTrue(self.studio_json("compute", "status", "demo", "1")["open"])
        stopped = self.studio_json("compute", "stop", "demo", "1")
        self.assertEqual(stopped["kind"], "session")
        report = self.studio_json("budget", "demo", "1", "report")
        self.assertEqual(report["sessions"], 1)
        self.assertEqual(self.studio_json("qc", "demo", "1", "queue"), [])

    def test_new_series_and_episode_from_template(self):
        self.studio_json("series", "new", "sky-forge", "--title", "Sky Forge")
        info = self.studio_json("episode", "new", "sky-forge", "1", "--title", "Sparks")
        self.assertTrue(info["project_id"].startswith("PROJECT_"))
        self.assertTrue((self.repo.root / "series/sky-forge/episodes/E01/shotlist.json").is_file())
        status = self.studio_json("pipeline", "status", "sky-forge", "1")
        self.assertEqual(status["next"]["stage"], "story", "a fresh template is not 'done'")
        dup = self.repo.studio("series", "new", "sky-forge", "--title", "again")
        self.assertEqual(dup.returncode, 2)
        self.assertIn("already exists", dup.stderr)

    def test_doctor(self):
        done = self.repo.studio("doctor")
        self.assertIn("Studio doctor", done.stdout)


if __name__ == "__main__":
    unittest.main()
