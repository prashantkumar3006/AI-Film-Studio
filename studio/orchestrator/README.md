# Orchestrator

> The **anime episode pipeline** (23 stages with legal, budget and QC gates)
> is `anime.py`: `python -m studio pipeline plan`. This file describes the
> general workflow planner used for any project type.

Coordinates a production run. It is currently a **skeleton**: it plans,
validates and creates directories, but does not generate or render media.

## Execution flow

```
Input
  → Workflow
  → Project creation
  → Asset acquisition
  → Asset processing
  → Audio
  → Animation
  → Rendering
  → QC
  → Final output
```

| # | Stage | Owner module | Integrations used |
|---|---|---|---|
| 1 | Input | — | — |
| 2 | Workflow | `orchestrator` | — |
| 3 | Project creation | `orchestrator` | — |
| 4 | Asset acquisition | `integrations` | stock, maps, vectors, blender, comfyui |
| 5 | Asset processing | `integrations` | post_realesrgan, post_rife |
| 6 | Audio | `integrations` | tts_kokoro, tts_indic_parler, stt_faster_whisper, music_ace_step |
| 7 | Animation | `integrations` | lipsync_rhubarb, motion_remotion |
| 8 | Rendering | `integrations.edit` | edit_ffmpeg |
| 9 | QC | `studio.feedback` | identity_ccip |
| 10 | Final output | `integrations.edit` | edit_ffmpeg |

The stage list lives in `STAGES` in `pipeline.py`.

## What `pipeline.py` does today

1. **Loads** a workflow JSON in the existing `scripts/workflows/` format.
2. **Validates** it with the engine's rules (supported step types from
   `create_project.py`), plus checks for duplicate step names, missing
   `args`/`path`, referenced scripts that don't exist, and placeholders
   that must come from the environment.
3. **Creates** `projects/<PROJECT_ID>/<slug>/` (never deletes or overwrites).
4. **Creates** the engine's standard folders plus the asset/render
   directories from `studio/config.yaml`.
5. **Prints** each stage and the status of its integrations.
6. **Dispatches** each stage to adapters via `call_adapter()` — every adapter
   is currently skipped (disabled / not implemented).

It does **not** execute workflow steps. The engine still does that:

```bash
python scripts/create_project.py workflow-run <PROJECT_ID> <slug> \
    --workflow scripts/workflows/production_pipeline.json [--execute]
```

## Usage

```bash
# Validate and preview, create nothing
python studio/orchestrator/pipeline.py \
    --workflow scripts/workflows/production_pipeline.json \
    --slug my-first-film --plan-only

# Create the project directories
python studio/orchestrator/pipeline.py \
    --workflow scripts/workflows/production_pipeline.json \
    --slug my-first-film

# Complete the folders of a project made by `create_project.py init`
python -m studio.orchestrator.pipeline \
    --workflow scripts/workflows/ai_generation_pipeline.json \
    --project-id PROJECT_2026_001 --slug my-documentary --complexity FULL
```

Without `--project-id`, projects go under `STUDIO_DRAFT/`, which is kept
separate from the engine's `PROJECT_<YEAR>_<NNN>` numbering. Those draft
projects have folders but no engine state file; for full tracking, create the
project with `create_project.py init` first and pass its ID and slug here.

Exit codes: `0` ok, `1` invalid workflow, `2` config / input error.

## Adapter contract

An integration runs only when it is enabled in **both**
`integrations/registry.yaml` and `studio/config.yaml`, has an `adapter`
set, and — if external — `processing.allow_external` is `true`. With
`processing.dry_run: true` (the default) active adapters are listed as
*planned* but not called.

```python
# integrations/<type>/adapter.py
def run(stage: str, context: dict) -> dict:
    """context: {"workflow": ..., "project": Project, "config": ...}"""
    return {"status": "ok", "outputs": [...]}
```
