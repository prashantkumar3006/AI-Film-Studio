# Archive — removed files

Consolidation of 3 October 2026. These files were removed because they were
superseded by working code, contradicted the Production Bible schema, or
described capabilities the anime plan does not use. About 18,000 lines of
documentation went; nothing that code reads was removed.

Every file is still in Git history. Commit `782303f` is on `main`, so it stays
recoverable whichever way the pull request is merged.

```bash
git show 782303f:studio/DATA_SCHEMA.md > DATA_SCHEMA.md      # read one file
git checkout 782303f -- studio/DATA_SCHEMA.md                 # restore it in place
```

## Removed

| File | Lines | Why it went | What replaces it |
|---|---|---|---|
| `studio/DATA_SCHEMA.md` | 2,080 | Its IDs (`SCN_001`, `SHOT_001`) contradict the stable IDs every stage now uses (`EP01_SC02_SH003`) | `schema/bible.schema.json` and `studio validate` |
| `studio/TOOL_REGISTRY.md` | 2,395 | Prose catalogue of generic tools, most of them outside the plan, with no licence of the weights recorded | `integrations/registry.yaml` |
| `studio/STUDIO_INDEX.md` | 2,232 | Index of documents that no longer exist | "Where things are" in `CLAUDE.md`; layout in `README.md` |
| `studio/COMMAND_CENTER.md` | 1,812 | Hand-kept project dashboard; a second source of project state | `scripts/create_project.py` (state file) and each episode's `bible.json` |
| `studio/TEMPLATE_REGISTRY.md` | 3,354 | Templates for many project types; the series uses one contract | The Production Bible schema; project folders from `create_project.py init` |
| `studio/AUTOMATION.md` | 3,327 | Automation described in general terms | The episode pipeline (`studio/orchestrator/pipeline.py`) and the build steps in `docs/WORKPLAN.md` |
| `studio/workflow/SKILL.md` | 1,563 | Repeated the orchestration rules of the operating system | `CLAUDE.md` and `docs/WORKPLAN.md` |
| `studio/project-template/SKILL.md` | 1,499 | Described the project folder tree by hand | `scripts/create_project.py init`, which creates it |
| `studio/subtitles/` | empty | Placeholder module | Subtitles are made in the assembly stage by Remotion (step 1.7, `studio/render/`) |
| `integrations/stock/`, `maps/`, `vectors/` | empty | Documentary-era capabilities; the series generates its own images | Removed with their entries in `integrations/registry.yaml`, their switches and asset folders in `studio/config.yaml` |

## Moved

| From | To |
|---|---|
| `studio/OPERATING_SYSTEM.md` (the original `CLAUDE.md`) | `docs/reference/OPERATING_SYSTEM.md` |
| `studio/STUDIO_BIBLE.md` | `docs/reference/STUDIO_BIBLE.md` |
| `studio/PROMPT_SYSTEM.md` | `docs/reference/PROMPT_SYSTEM.md` |
| `studio/MEDIA_STORAGE.md` | `docs/reference/MEDIA_STORAGE.md` |

These four stay because upcoming steps draw on them: creative principles for
the series bible (2.1), the prompt system for keyframes (1.10, 2.5) and media
storage for the GridShare round trip (1.9). Where any of them disagrees with
`CLAUDE.md` or `docs/WORKPLAN.md`, the latter win.
