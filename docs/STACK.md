# The stack: what each tool does and why it was chosen

Chosen for: commercial-use licenses, quality for anime, running on a
CPU-only laptop plus a rented 24 GB GPU, and automation from code.
License status is enforced by `integrations/registry.yaml`, not by this page.

| Job | Tool | Runs on | Why this one | License state |
|---|---|---|---|---|
| Studio brain: script, direction, prompts, management | **Claude** (Claude Code in this repo + the skills in `.claude/skills/`) | laptop | Writes, plans, compiles shot lists, drives every command | — |
| 3D sets, props, blocking | **Blender** + **Blender MCP** (ahujasid/blender-mcp) | laptop | Claude edits scenes interactively; headless Workbench renders give layout guides on CPU | GPL / MIT ✔ |
| Generation runner | **ComfyUI** | GridShare (one-click template) | Node graphs for keyframes, reference editing and video; HTTP API for automation | GPL (software) |
| Anime keyframes | **Animagine XL 4.0** (SDXL) | GridShare | Strong anime base with a commercial-use license (OpenRAIL++-M conditions) | conditional ✔ |
| Character consistency | **Qwen-Image-Edit-2509** + character **LoRAs** (kohya-ss sd-scripts) | GridShare | Multi-reference editing preserves identity; LoRA locks a character | Apache-2.0 ✔ / verify |
| Image-to-video | **Wan2.2 TI2V-5B** (fits 24 GB), **I2V-A14B** for hero shots | GridShare | Best open video model family with Apache-2.0 weights | Apache-2.0 ✔ |
| English voices | **Kokoro-82M** | laptop CPU | Small, fast, Apache-2.0, good quality | Apache-2.0 ✔ |
| Hindi voices | **AI4Bharat Indic Parler-TTS** | GridShare | Hindi + 20 Indian languages, named speakers, Apache-2.0 | Apache-2.0 ✔ |
| Speech-to-text (QC, subtitles) | **faster-whisper** | laptop | Checks every TTS line against the script; word timings | MIT (verify) |
| Lip sync | **Rhubarb Lip Sync** | laptop | Mouth shapes from audio, the way 2D animation does it; phonetic mode for Hindi | MIT ✔ |
| Music | **ACE-Step** (code Apache-2.0) | GridShare | Open music model; weights license to verify per version | blocked until verified |
| Motion graphics | **Remotion** | laptop | React-based titles, cards, lower thirds rendered from code | free ≤ 3 people |
| Edit, mix, subtitles, packaging | **FFmpeg** | laptop | Camera moves, assembly, ducking, −14 LUFS, multi-language tracks | LGPL |
| Manual polish (optional) | **DaVinci Resolve** (free) via OpenTimelineIO | laptop | Human touch-ups without After Effects | free / Apache-2.0 |
| Identity QC | **imgutils CCIP** | laptop CPU | Trained to tell whether two anime images show the same character | MIT code, verify weights |
| GPU compute | **GridShare India** | — | SSH, JupyterLab, REST API, ComfyUI template, RTX 4090 at ₹48/h ex-GST *(gridshare.in, 2026-10-04)* | read their ToS |

## Corrections to the original plan

- **Whisper is speech-to-text, not voice generation.** It listens. (Wispr
  Flow is a dictation app for typing by voice — handy for writing scripts,
  not part of the pipeline.) Voices come from Kokoro and Indic Parler-TTS;
  Whisper checks them.
- **After Effects** is proprietary, subscription-based and hard to automate
  from scripts. Remotion + FFmpeg + Blender's compositor cover titles,
  overlays and effects in code. Keep After Effects optional for hand-made
  hero effects only.
- **Popular community anime checkpoints (NoobAI, many Illustrious merges)
  are non-commercial.** They are blocked in the registry even though they
  are common in tutorials.

## Recommended additions (not in the original list)

| Need | Tool | Status |
|---|---|---|
| Frame interpolation for generated clips | Practical-RIFE | registry, disabled until verified |
| Upscaling 720p generations to 1080p | Real-ESRGAN (anime model) | registry, disabled until verified |
| Scheduling uploads | Postiz (available as a Claude plugin skill) | optional |
| Timeline export to Resolve | OpenTimelineIO | registry, disabled |

## Claude skills, connectors and extensions to use

| What | Why | When |
|---|---|---|
| **Claude Code** in this repo | Runs `python -m studio …`, edits shot lists, writes adapters | always |
| **Claude desktop app + Blender MCP** | Lets Claude build Blender scenes on your laptop | layout stage |
| **The 36 skills in `.claude/skills/`** | Department expertise loaded on demand | always |
| **GitHub connector** (already attached) | Commits, branches, pull requests for every change | always |
| **Google Drive or similar** (optional) | Backing up approved model sheets and masters outside git | after episode 1 |
| **YouTube Data API via Zapier/Postiz** (optional) | Uploads and analytics for the audience feedback loop | after the channel launches |
