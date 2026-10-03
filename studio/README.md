# Studio — package layout

`studio/` holds two layers side by side:

| Layer | What it is | Where |
|---|---|---|
| **Department knowledge** | How each department thinks and works | `studio/<department>/SKILL.md` |
| **Execution code** | Python that validates, plans and (later) runs production steps | `studio/bible/`, `studio/cli.py`, `studio/orchestrator/`, and the planned `asset_manager/`, `audio/`, `video/`, `render/` |

The knowledge layer decides *what should happen*; the code makes it happen
repeatably. Code never takes a decision away from the department that owns
it (`docs/reference/OPERATING_SYSTEM.md`, §8).

Studio-wide reference documents (operating system, creative principles,
prompt system, media storage) live in `docs/reference/`.

`scripts/create_project.py` remains the source of truth for project state,
tasks, approvals and workflow step execution. The modules below build on it.

---

## Modules

### `bible/` and `cli.py`
The Production Bible validator (workplan step 1.1). `studio validate <target>`
checks a `bible.json` against `schema/bible.schema.json`, then checks IDs,
references and that every line has English and Hindi text. Exit codes:
`0` valid, `1` invalid, `2` file or set-up error.

### `orchestrator/`
Entry point and coordination.

- `config.py` — loads `studio/config.yaml` and `integrations/registry.yaml`
  (PyYAML if installed, otherwise a built-in parser).
- `project.py` — creates `projects/<PROJECT_ID>/<slug>/`, reusing the engine's
  numbered folder layout (`00_admin` … `99_backup`) so both tools agree.
- `pipeline.py` — loads and validates a workflow, creates the project, prints
  the episode stages and dispatches them to adapters.

See [`orchestrator/README.md`](orchestrator/README.md).

### `integrations` (repository root)
The external tools — Kokoro and the Hindi voice, Whisper, Rhubarb, Blender,
kohya_ss, ComfyUI, Wan2.2, ACE-Step, Real-ESRGAN, Remotion — each reached
through one adapter and catalogued with licences in
`integrations/registry.yaml`. See [`../integrations/README.md`](../integrations/README.md).

### `asset_manager/`
*Planned.* Registers every generated asset in the Bible (path, version,
checksum, tool, model, seed, licence) and places it in the project's asset
folders (`assets:` in `config.yaml`). Owns the layout and keyframe stages.

### `audio/`
*Planned.* Voices, lip sync, score and effects through adapters, and loudness
normalisation to the `audio:` targets (48 kHz, −14 LUFS).

### `video/`
*Planned.* Hero-shot motion (Wan2.2) and clip-level processing.

### `render/`
*Planned.* Assembly through Remotion — timeline, mouth shapes, subtitles
(to the `subtitles:` rules) and titles — using the `render:` settings.
Output goes to `18_technical/renders`, which is git-ignored.

### `qc/`
Holds the QC department `SKILL.md`. *Planned* automated checks (resolution,
frame rate, loudness, Whisper round-trip, missing assets, subtitle timing)
will live alongside it and write reports to `20_qc/`.

---

## Design rules

1. **Laptop first.** Light work runs on a Windows laptop with no GPU; heavy
   work runs on a rented GridShare GPU and is stopped after each batch.
2. **Everything heavy is opt-in.** Disabled in both config and registry until
   its adapter exists and its workplan step's done-test passes.
3. **Local by default.** `processing.allow_external: false` blocks external
   services until you allow them.
4. **Adapters, not coupling.** Core code never imports an external repo.
5. **One layout.** Project folders come from `scripts/create_project.py`.
6. **Generated media is never committed.** `projects/*` and render output are ignored.
