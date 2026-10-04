"""ComfyUI client and adapter against a fake ComfyUI HTTP server."""

import copy
import json
import shutil
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from integrations.comfyui import adapter
from integrations.comfyui.client import ComfyClient
from integrations.comfyui.workflow import inject, load_workflow, validate_mapping
from studio.common import StudioError
from studio.legal.licenses import load_catalogue
from studio.legal.provenance import read_provenance
from studio.orchestrator.config import load_config

PNG = bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010806000000" "1f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082")


class FakeComfy(BaseHTTPRequestHandler):
    queued = []
    uploads = []

    def log_message(self, *args):
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        if self.path == "/prompt":
            payload = json.loads(body)
            FakeComfy.queued.append(payload["prompt"])
            self._send(200, {"prompt_id": f"p{len(FakeComfy.queued)}", "number": 1, "node_errors": {}})
        elif self.path == "/upload/image":
            FakeComfy.uploads.append(len(body))
            self._send(200, {"name": "ref.png", "subfolder": "", "type": "input"})
        else:
            self._send(404, {"error": "no"})

    def do_GET(self):
        url = urlparse(self.path)
        if url.path.startswith("/history/"):
            pid = url.path.rsplit("/", 1)[-1]
            self._send(200, {pid: {"status": {"status_str": "success", "completed": True}, "outputs": {"9": {"images": [{"filename": f"{pid}_00001_.png", "subfolder": "", "type": "output"}]}}}})
        elif url.path == "/view":
            self.assertion_name = parse_qs(url.query)["filename"][0]
            self._send(200, PNG, "image/png")
        elif url.path == "/system_stats":
            self._send(200, {"system": {"comfyui_version": "fake"}})
        else:
            self._send(404, {"error": "no"})


class ComfyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), FakeComfy)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.config = copy.deepcopy(load_config())
        self.config["comfyui"]["url"] = self.url
        self.catalogue = load_catalogue()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def cleared(self):
        cat = copy.deepcopy(self.catalogue)
        cat["integrations"]["comfyui"]["license"]["verified"] = True
        cat["models"]["animagine_xl_4"]["license"]["conditions_acknowledged"] = True
        return cat

    def test_mapping_matches_the_shipped_workflow(self):
        workflow, mapping = load_workflow("keyframe_sdxl")
        validate_mapping(workflow, mapping)
        broken = copy.deepcopy(mapping)
        broken["inputs"]["prompt"] = [{"node": "6", "input": "nope"}]
        with self.assertRaises(StudioError):
            validate_mapping(workflow, broken)

    def test_inject_with_and_without_lora(self):
        workflow, mapping = load_workflow("keyframe_sdxl")
        with_lora = inject(workflow, mapping, {"prompt": "ar1a, girl", "seed": "42", "lora_file": "aria.safetensors", "lora_weight": 0.9})
        self.assertEqual(with_lora["6"]["inputs"]["text"], "ar1a, girl")
        self.assertEqual(with_lora["3"]["inputs"]["seed"], 42)
        self.assertEqual(with_lora["10"]["inputs"]["strength_model"], 0.9)
        without = inject(workflow, mapping, {"prompt": "x", "seed": 1})
        self.assertNotIn("10", without, "unused LoRA loader is removed")
        self.assertEqual(without["3"]["inputs"]["model"], ["4", 0])
        self.assertEqual(without["6"]["inputs"]["clip"], ["4", 1])
        self.assertIn("10", workflow, "the template itself is not modified")

    def test_generate_writes_outputs_with_provenance(self):
        outputs = adapter.generate("keyframe_sdxl", {"prompt": "girl on rooftop", "negative": "lowres", "seed": 7}, self.tmp, self.config, catalogue=self.cleared(), provenance={"kind": "keyframe", "shot_id": "SC01_SH002"})
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0].read_bytes()[:4], b"\x89PNG")
        record = read_provenance(outputs[0])
        self.assertEqual((record["seed"], record["shot_id"], record["models"]), (7, "SC01_SH002", ["animagine_xl_4"]))
        self.assertTrue(record["license_snapshot"]["animagine_xl_4"]["cleared"])
        self.assertEqual(FakeComfy.queued[-1]["6"]["inputs"]["text"], "girl on rooftop")

    def test_license_gate_runs_before_any_gpu_time(self):
        before = len(FakeComfy.queued)
        with self.assertRaises(StudioError) as caught:
            adapter.generate("keyframe_sdxl", {"prompt": "x", "seed": 1}, self.tmp, self.config, catalogue=self.catalogue)
        self.assertIn("License gate blocked", str(caught.exception))
        self.assertEqual(len(FakeComfy.queued), before, "nothing was queued")

    def test_required_params_and_upload(self):
        with self.assertRaises(StudioError):
            adapter.generate("keyframe_sdxl", {"seed": 1}, self.tmp, self.config, catalogue=self.cleared())
        image = self.tmp / "ref.png"
        image.write_bytes(PNG)
        self.assertEqual(ComfyClient(self.url).upload_image(image), "ref.png")

    def test_unreachable_server_message(self):
        with self.assertRaises(StudioError) as caught:
            ComfyClient("http://127.0.0.1:9", timeout=2).system_stats()
        self.assertIn("Is the GridShare instance running", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
