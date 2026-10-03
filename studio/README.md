# Studio — Modular Architecture

`studio/` now holds two layers that live side by side:

| Layer | What it is | Where |
|---|---|---|
| **Department knowledge** | How each department thinks and works (the existing `SKILL.md` files, `STUDIO_BIBLE.md`, `COMMAND_CENTER.md`, …) | `studio/<department>/SKILL.md`, `studio/*.md` |
| **Execution modules** | Python code that plans and (later) runs production steps | `studio/orchestrator/`, `asset_manager/`, `render/`, `audio/`, `video/`, `subtitles/`, `qc/` |

The knowledge layer decides *what should happen*. The execution layer
makes it happen repeatably. Nothing in the execution layer replaces a
department's ownership of its decisions (see `studio/OPERATING_SYSTEM.md`, §8).

The existing engine, `scripts/create_project.py`, remains the source of
truth for project state, tasks, approvals and workflow step execution.
The modules below build on it rather than duplicating it.

---

## Modules

### `orchestrator/`
Entry point and coordination.

- `config.py` — loads `studio/config.yaml` and `integrations/registry.yaml`
  (PyYAML if installed, otherwise a built-in parser — no required dependency).
- `project.py` — creates `projects/<PROJECT_ID>/<slug>/`, reusing the engine's
  numbered folder layout (`00_admin` … `99_backup`) so both tools agree.
- `pipeline.py` — loads and validates a workflow, creates the project,
  prints the stage plan, and dispatches stages to adapters.

See [`orchestrator/README.md`](orchestrator/README.md) for the execution flow.

### `integrations` (repository root)
External capabilities — stock media, maps, vectors, TTS, transcription,
image and video generation — connected through adapters. Catalogued in
`integrations/registry.yaml`. See [`../integrations/README.md`](../integrations/README.md).

### `asset_manager/`
*Planned.* Acquires assets through integration adapters, registers them,
normalises formats, and places them in the project's asset directories
(`assets:` in `config.yaml`). Pairs with the `asset-pipeline` department.

### `render/`
*Planned.* Assembles timelines and renders previews and masters using the
`render:` settings (1920×1080 @ 30 fps by default, 1280×720 previews).
Output goes to `18_technical/renders`, which is git-ignored.

### `audio/`
*Planned.* Voice, SFX and music handling, TTS / transcription via adapters,
and loudness normalisation to the `audio:` targets (48 kHz, −14 LUFS).
Pairs with the `sound` and `music` departments.

### `video/`
*Planned.* Animation, motion and clip-level processing ahead of rendering.
Pairs with `animation` and `vfx-motion`.

### `subtitles/`
*Planned.* Caption generation (from transcription) and formatting to the
`subtitles:` rules (SRT, 42 chars/line, 2 lines).

### `qc/`
Already contains the QC department `SKILL.md`. *Planned* automated checks
(resolution, frame rate, loudness, missing assets, subtitle timing) will live
alongside it and write reports to `20_qc/`.

---

## Design rules

1. **Lightweight first.** Defaults must run on a laptop with no GPU.
2. **Heavy AI is opt-in.** Disabled in both config and registry by default.
3. **Local by default.** `processing.allow_external: false` blocks external
   services until you explicitly allow them.
4. **Adapters, not coupling.** Core code never imports an external repo directly.
5. **One layout.** Project folders come from `scripts/create_project.py`.
6. **Generated media is never committed.** `projects/*` and render output are ignored.
