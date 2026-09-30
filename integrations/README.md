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

| Folder | Capability | Default |
|---|---|---|
| `stock/` | Stock footage, photos, audio | disabled |
| `maps/` | Maps and geographic data | disabled |
| `vectors/` | Vector graphics / illustration | disabled |
| `tts/` | Text-to-speech | disabled (heavy) |
| `transcription/` | Speech-to-text | disabled (heavy) |
| `image_generation/` | AI image generation | disabled (heavy) |
| `video_generation/` | AI video generation | disabled (heavy) |

## Registry

`registry.yaml` lists every integration with:

`name`, `type`, `enabled`, `execution_mode` (`local` / `external` / `hybrid`),
`repository`, `adapter`, and `heavy`.

`repository` and `adapter` are `null` on purpose. Fill them in only when a
specific repository has been chosen and evaluated, and pin it to a tag or
commit for reproducibility.

## Enabling an integration

All of these must be true for it to run:

1. `enabled: true` in `registry.yaml`
2. `true` for that key under `integrations:` in `studio/config.yaml`
3. `adapter:` points to an importable module with `run(stage, context)`
4. if `execution_mode: external`, `processing.allow_external: true`
5. `processing.dry_run: false` to actually call it

Before enabling a new integration, check its licence, rights terms and
hardware requirements (see `studio/legal-rights/` and `studio/technical-post/`).
