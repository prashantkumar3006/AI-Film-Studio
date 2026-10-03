# Orchestrator

Coordinates a production run. It is currently a **skeleton**: it plans,
validates and creates directories, but does not generate or render media.

## Execution flow

The episode pipeline from `docs/WORKPLAN.md`. Sound and picture run side by
side; the owner approves at three checkpoints.

```
Brief → Workflow → Project → Writer (bible.json) → Checkpoint A
      → Voices → Layout → Lip sync → Keyframes → Checkpoint B
      → Score → Motion → Assembly → Finishing and QC → Checkpoint C → Publish
```

| # | Stage | Owner module | Integrations used |
|---|---|---|---|
| 1 | Brief (owner) | — | — |
| 2 | Workflow | `orchestrator` | — |
| 3 | Project creation | `orchestrator` | — |
| 4 | Writer and director: `bible.json` | `orchestrator` | — |
| 5 | Checkpoint A (owner): script, dialogue, lore | — | — |
| 6 | Voices | `audio` | tts, tts_hindi, transcription |
| 7 | Sets and layout | `asset_manager` | layout_3d |
| 8 | Lip sync | `audio` | lipsync |
| 9 | Keyframes | `asset_manager` | lora_training, image_generation |
| 10 | Checkpoint B (owner): one keyframe per shot | — | — |
| 11 | Score and effects | `audio` | music |
| 12 | Motion | `video` | video_generation |
| 13 | Assembly | `render` | assembly |
| 14 | Finishing and QC | `qc` | upscaling |
| 15 | Checkpoint C (owner): final cut | — | — |
| 16 | Publish (owner): YouTube | — | — |

The stage list lives in `STAGES` in `pipeline.py`. A failed QC check sends
only the failing shot back to its stage.

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
