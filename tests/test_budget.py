"""Budget estimate, ledger, guard, calibration and GPU sessions."""

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from studio.budget.estimate import estimate_episode, money
from studio.budget.ledger import Ledger
from studio.common import StudioError
from studio.compute.gridshare import session_start, session_status, session_stop
from studio.orchestrator.config import load_config
from tests.helpers import FIXTURES


def twenty_minute_episode(full_ratio: float):
    """240 five-second shots; a share of them full AI video, half the rest talking."""
    shots = []
    n_full = round(240 * full_ratio)
    for i in range(240):
        motion = "full" if i < n_full else ("limited" if i % 2 else "camera")
        shot = {"id": f"SC01_SH{i + 1:03d}", "duration_s": 5.0, "motion": motion, "visual_prompt": "x"}
        if motion == "limited":
            shot["dialogue"] = [{"character": "aria", "line": {"en": "line", "hi": "पंक्ति"}}]
        shots.append(shot)
    return {"scenes": [{"id": "SC01", "shots": shots}]}


class Estimate(unittest.TestCase):
    def setUp(self):
        self.config = load_config()

    def test_money_includes_gst(self):
        result = money(3600, self.config, "rtx_4090")
        self.assertEqual(result["ex_gst"], 48.0)
        self.assertEqual(result["inc_gst"], 56.64)

    def test_limited_animation_fits_the_5000_cap(self):
        result = estimate_episode(twenty_minute_episode(0.25), self.config, ["en", "hi"])
        self.assertEqual(result["summary"]["runtime_min"], 20.0)
        self.assertTrue(result["within_cap"], result)

    def test_all_full_motion_breaks_the_cap(self):
        result = estimate_episode(twenty_minute_episode(1.0), self.config, ["en", "hi"])
        self.assertFalse(result["within_cap"], result)
        self.assertGreater(result["cost_with_margin"], 5000)

    def test_demo_episode_estimate_shape(self):
        shotlist = json.loads((FIXTURES / "demo/episodes/E01/shotlist.json").read_text())
        result = estimate_episode(shotlist, self.config, ["en", "hi"])
        self.assertEqual(result["video_clips_5s"], 1)
        self.assertEqual(result["dialogue_lines"], {"en": 2, "hi": 2})
        self.assertIn("video_generation", result["stages_gpu_hours"])


class LedgerAndSessions(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.config = copy.deepcopy(load_config())
        self.ledger = Ledger(self.tmp, self.config)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_sessions_and_manual_spend(self):
        self.ledger.log_session("rtx_4090", 2 * 3600)
        self.ledger.log_manual(100, "font license")
        self.assertEqual(self.ledger.spent(), round(2 * 56.64 + 100, 2))
        self.assertEqual(self.ledger.remaining(), round(5000 - 2 * 56.64 - 100, 2))

    def test_guard_stops_overspend(self):
        self.ledger.log_manual(4900, "big spend")
        self.ledger.guard(50)
        with self.assertRaises(StudioError):
            self.ledger.guard(150)

    def test_calibrate_uses_medians_with_enough_samples(self):
        for seconds in (500, 520, 600, 540, 10_000):
            self.ledger.log_job("video", seconds, unit="video_5s_720p", shot_id="SC01_SH001")
        self.ledger.log_job("keyframe", 30, unit="keyframe_image")
        result = self.ledger.calibrate(minimum_samples=5)
        self.assertEqual(result["benchmarks_gpu_s"], {"video_5s_720p": 540.0})
        self.assertEqual(result["samples"]["keyframe_image"], 1)

    def test_gpu_session_tracking(self):
        start = session_start(self.tmp, "rtx_4090")
        status = session_status(self.tmp, warn_hours=3, now_epoch=start["started_epoch"] + 4 * 3600)
        self.assertTrue(status["warning"])
        with self.assertRaises(StudioError):
            session_start(self.tmp, "rtx_4090")
        entry = session_stop(self.tmp, self.ledger, now_epoch=start["started_epoch"] + 1800)
        self.assertEqual(entry["cost_inc_gst"], 28.32)
        self.assertFalse(session_status(self.tmp)["open"])


if __name__ == "__main__":
    unittest.main()
