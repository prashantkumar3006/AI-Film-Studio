# AI-Film-Studio

An automated production studio for an original anime series — fantasy, sci-fi
and supernatural, grounded at first — for a general audience on YouTube, in
English and Hindi. Claude handles writing, generation, assembly and QC; the
owner approves at three checkpoints.

**The plan:** [`docs/WORKPLAN.md`](docs/WORKPLAN.md) — decisions, roles, the
episode pipeline, all 37 build steps with their done-tests, tool stack,
licences and risks.

**Current phase:** 1 · Spine. Step 1.1 (the Production Bible schema and
validator) is done; no worker produces media yet.

## Quick start

```bash
pip install -e ".[dev]"                     # adds the `studio` command
studio validate examples/ep00/bible.json    # check a Production Bible
python -m pytest                            # run the tests
```

On Windows without installing: `python -m studio.cli validate examples\ep00\bible.json`.

## How an episode is made

```
Brief → Writer and director (bible.json) → Checkpoint A
      → Voices → Lip sync → Score          (sound)
      → Sets → Keyframes → Checkpoint B → Motion   (picture)
      → Assembly → Finishing and QC → Checkpoint C → Publish
```

A failed QC check sends only the failing shot back to its worker. The full
diagram, with the tool and platform for each stage, is in `docs/WORKPLAN.md`.

## Where things run

| Laptop (Windows, CPU) | GridShare GPU (RTX 4090, per-second billing) |
|---|---|
| Claude Code, Kokoro voices, Rhubarb lip sync, Remotion assembly, FFmpeg QC, Blender scene set-up via BlenderMCP | ComfyUI + Animagine XL 4.0, kohya_ss character models, Wan2.2 motion, ACE-Step score, Real-ESRGAN upscaling, headless Blender renders |

## Repository layout

| Path | Contents |
|---|---|
| `CLAUDE.md` | Short working guide for Claude |
| `docs/WORKPLAN.md` | The plan and every build step |
| `schema/bible.schema.json` | Production Bible contract |
| `studio/bible/`, `studio/cli.py` | Validator and the `studio` command |
| `studio/orchestrator/` | Pipeline skeleton (`--plan-only` prints every stage) |
| `docs/reference/` | Operating system, creative principles, prompt system, media storage |
| `docs/ARCHIVE.md` | What was removed, why, and how to recover it |
| `studio/<department>/SKILL.md` | Department instructions (25 departments) |
| `integrations/registry.yaml` | Every external tool with repository, licences and where it runs |
| `examples/ep00/` | Pipeline test scene (not canon) |
| `scripts/create_project.py` | Project-state engine |
| `projects/` | Real projects (git-ignored) |

Media, model files and secrets never go into Git; `.gitignore` enforces this.
