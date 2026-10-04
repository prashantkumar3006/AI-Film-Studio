# Integrations

External tools are reached only through adapters here. The studio never
imports an external project directly, so any tool can be swapped by
rewriting one adapter.

| Folder | Tool | Contract |
|---|---|---|
| `comfyui/` | ComfyUI HTTP API (on GridShare) | `adapter.generate(workflow, params, out_dir, config, provenance=...)` |
| `blender/` | Blender headless + Blender MCP notes | `adapter.render_layout(blend, out, camera, frame)` |
| `tts/` | Kokoro (EN), Indic Parler-TTS (HI) via runner scripts | `adapter.synthesize_line(line, voice, out, config)` |
| `stt/` | faster-whisper | `whisper.transcribe(path, language)`, `word_timings(...)` |
| `lipsync/` | Rhubarb + frame compositor | `rhubarb.mouth_cues(audio, language)`, `compose.timeline/render` |
| `music/` | ACE-Step or any command | `adapter.generate_cue(...)` |
| `motion_graphics/` | Remotion project + renderer | `adapter.render(composition, out, props)` |
| `edit/` | FFmpeg | `camera.still_to_clip`, `assemble.assemble`, `mix.mix`, `subtitles.write_srt`, `package.package` |
| `identity/` | imgutils CCIP | `ccip.scorer()` for the identity check |
| `common.py` | command templates, local or over SSH | `run_tool(config, key, values)` |
| `registry.yaml` | **every tool and model with its license state** | read by the license gate |

## Adding a tool

1. Add it to `registry.yaml` with a `license` block. Read the license and
   run `python -m studio legal verify <key> --source <url> --commercial-use ...`.
2. Write the adapter. Call `studio.legal.licenses.require_cleared([...])`
   before doing any paid work, and `studio.legal.provenance.write_provenance`
   for every file it produces.
3. If it is a command-line tool, put its command template in
   `studio/config.yaml` under `tools.<key>` (with `where: local` or
   `where: gridshare`) and use `integrations.common.run_tool`.
4. Add tests (fake the external tool; see `tests/test_comfyui.py`).
5. Enable it in both `registry.yaml` and `studio/config.yaml` → `integrations`.

Cloned or vendored external code goes in `integrations/<type>/vendor/`
or `repo/`, which are git-ignored.
