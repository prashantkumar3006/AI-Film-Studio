"""GridShare SSH command construction and tool templates (no network)."""

import unittest
from unittest import mock

from integrations.common import render_command, run_tool
from studio.common import StudioError
from studio.compute.gridshare import Remote


class RemoteCommands(unittest.TestCase):
    def setUp(self):
        self.remote = Remote.from_env({"GRIDSHARE_SSH_HOST": "203.0.113.5", "GRIDSHARE_SSH_PORT": "2222", "GRIDSHARE_SSH_KEY": "/k/id", "GRIDSHARE_REMOTE_DIR": "/workspace/s"})

    def test_requires_host(self):
        with self.assertRaises(StudioError):
            Remote.from_env({})

    def test_ssh_command_runs_in_remote_dir(self):
        command = self.remote.ssh_command("nvidia-smi")
        self.assertEqual(command[:3], ["ssh", "-p", "2222"])
        self.assertIn("-i", command)
        self.assertEqual(command[-2], "root@203.0.113.5")
        self.assertEqual(command[-1], "mkdir -p /workspace/s && cd /workspace/s && nvidia-smi")

    def test_tunnel_binds_localhost_only(self):
        command = self.remote.tunnel_command(8188, 8188)
        self.assertIn("8188:127.0.0.1:8188", command)
        self.assertIn("-N", command)

    def test_push_and_pull_targets(self):
        self.assertTrue(self.remote.push_command("/tmp/x", "inputs")[-1].endswith(":/workspace/s/inputs/"))
        self.assertTrue(self.remote.pull_command("out/a.png", "/tmp/a.png")[-2].endswith(":/workspace/s/out/a.png"))


class ToolTemplates(unittest.TestCase):
    def test_values_are_shell_quoted(self):
        command = render_command("tts --text {text} --out {out}", {"text": "it's \"fine\"; rm -rf /", "out": "a b.wav"})
        self.assertIn("'it'\"'\"'s \"fine\"; rm -rf /'", command)
        self.assertIn("'a b.wav'", command)

    def test_missing_values_are_reported(self):
        with self.assertRaises(StudioError) as caught:
            render_command("x {text} {voice}", {"text": "a"})
        self.assertIn("voice", str(caught.exception))

    def test_gridshare_tools_run_over_ssh(self):
        config = {"tools": {"tts_indic_parler": {"where": "gridshare", "command": "python run.py --text {text}"}}}
        fake = mock.Mock()
        fake.run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
        run_tool(config, "tts_indic_parler", {"text": "नमस्ते"}, remote=fake)
        fake.run.assert_called_once()
        self.assertIn("नमस्ते", fake.run.call_args[0][0])

    def test_unconfigured_tool(self):
        with self.assertRaises(StudioError):
            run_tool({"tools": {"music_ace_step": {"command": None}}}, "music_ace_step", {})


if __name__ == "__main__":
    unittest.main()
