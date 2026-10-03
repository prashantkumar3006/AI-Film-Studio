# Integrations

External capabilities the studio can use — stock media, maps, vector
graphics, text-to-speech, transcription, image generation and video
generation.

## Principle: adapters, not dependencies

External GitHub repositories and services will be connected **through
adapters**. They do not become part of the core studio:

- The core (`studio/`) never imports an external repository directly.
- Each capability gets one thin adapter in `integrations/<type>/adapter.py`
  that translates between the studio's contract and the external tool.
- Swapping one TTS engine or stock provider for another means rewriting
  one adapter — not touching the orchestrator, config or workflows.
- An external repository's heavy dependencies stay with that repository
  (its own virtual environment, container or install), so the studio
  remains lightweight.
- Cloned or vendored external code goes in `integrations/<type>/vendor/`
  or `repo/`, which are git-ignored.

```
studio/orchestrator ──► integrations/<type>/adapter.py ──► external repo / API / CLI
      (contract)              (translation)                   (implementation)
```

The existing `scripts/adapters/ai_generate.py` already follows this idea for
AI generation; future image/video generation adapters can wrap it.

## Layout

Chosen tools, from the decisions of 3 October 2026 (`docs/WORKPLAN.md`):

| Folder | Capability | Chosen tool | Runs on | Step |
|---|---|---|---|---|
| `tts/` | English and Hindi voices | Kokoro-82M; Hindi from a bake-off | laptop, GridShare if needed | 1.3–1.5 |
| `transcription/` | Round-trip check of every voice line | Whisper | laptop | 1.3 |
| `lipsync/` | Mouth shapes from dialogue | Rhubarb Lip Sync | laptop | 2.7 |
| `layout_3d/` | Location sets, cameras, depth and line-art passes | Blender via BlenderMCP | laptop + GridShare | 2.4 |
| `lora_training/` | One model per main character | kohya_ss | GridShare | 2.3 |
| `image_generation/` | Anime keyframes | ComfyUI + Animagine XL 4.0 | GridShare | 1.10, 2.5 |
| `video_generation/` | Hero-shot motion | Wan2.2 TI2V-5B | GridShare | 2.6 |
| `music/` | Score | ACE-Step 1.5 | GridShare | 2.8 |
| `upscaling/` | Final resolution | Real-ESRGAN anime models | GridShare | 2.9 |
| `assembly/` | Timeline, subtitles, titles | Remotion | laptop | 1.7 |
| `stock/`, `maps/`, `vectors/` | Earlier design | not in the current plan | — | — |

Every entry is disabled until its adapter exists and its workplan step's
done-test passes.

## Registry

`registry.yaml` lists every integration with:

`name`, `type`, `enabled`, `execution_mode` (`local` / `external` / `hybrid`),
`runs_on`, `gpu`, `repository`, `weights`, `licence_code`, `licence_weights`,
`licence_source`, `licence_checked`, `adapter`, `adapter_planned`,
`workplan_step` and `heavy`. Its `blocked:` section lists popular tools that
were rejected because their weights forbid commercial use.

Pin each repository to a tag or commit when its adapter is written.

## Enabling an integration

All of these must be true for it to run:

1. `enabled: true` in `registry.yaml`
2. `true` for that key under `integrations:` in `studio/config.yaml`
3. `adapter:` points to an importable module with `run(stage, context)`
4. if `execution_mode: external`, `processing.allow_external: true`
5. `processing.dry_run: false` to actually call it

Before enabling a new integration, check its licence, rights terms and
hardware requirements (see `studio/legal-rights/` and `studio/technical-post/`).
