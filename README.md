# AI-Film-Studio
AI-powered film and documentary production studio: directing, writing, cinematography, editing, VFX, sound, color, and production workflows.

## Modular architecture

The repository is being prepared as a modular, automated video-production studio:

- **`studio/`** — department knowledge (`<department>/SKILL.md`) plus execution modules:
  `orchestrator/`, `asset_manager/`, `render/`, `audio/`, `video/`, `subtitles/`, `qc/`.
  Settings live in `studio/config.yaml` (lightweight defaults: 1920×1080 @ 30 fps, local processing).
- **`integrations/`** — external tools (stock, maps, vectors, TTS, transcription, image/video
  generation) connected through adapters and catalogued in `integrations/registry.yaml`.
  All heavy AI integrations are disabled by default.
- **`projects/`** — generated project folders (git-ignored).
- **`scripts/create_project.py`** — the existing engine; still owns project state and workflow execution.

Try the orchestration skeleton (standard library only):

```bash
python studio/orchestrator/pipeline.py --workflow scripts/workflows/production_pipeline.json --slug my-first-film --plan-only
```

See [`studio/README.md`](studio/README.md) and [`integrations/README.md`](integrations/README.md).
