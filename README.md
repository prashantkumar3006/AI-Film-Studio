# AI-Film-Studio

A private, automated, license-safe studio for producing an original
**anime series in English and Hindi** — and, because the studio is
general, any future film or video project.

Claude writes, directs and manages; Blender (with Blender MCP) builds sets
and layouts; ComfyUI on a rented GridShare GPU generates keyframes and
motion; Kokoro and Indic Parler-TTS voice the characters; Rhubarb drives
mouth shapes; Remotion makes titles; FFmpeg edits, mixes and packages.
A built-in feedback system checks every asset, retries what it can fix
and sends only real problems to you.

```
script → shot list → [gates: bible · IP scan · budget] → voices → timing
→ Blender layout → keyframes → [QC + approval] → motion · lip sync · titles
→ music → edit → mix → subtitles → [master QC] → [release gate] → package
→ review & lessons (thresholds and costs recalibrate)
```

## Quick start

```bash
python -m pip install -r requirements.txt     # + requirements-qc.txt for QC extras
python -m studio doctor
python -m unittest discover -s tests
python -m studio pipeline plan
```

Then in Claude Code: *"studio status for <series> <episode>"*.

| Command | What it does |
|---|---|
| `series new / check` | create a series from the template; validate its bible |
| `episode new` | episode canon files + engine project |
| `shots check` | shot list vs bible, runtime, motion policy |
| `legal check / verify / acknowledge / scan / release-gate` | license gate, IP scan, final provenance gate |
| `estimate` | GPU cost vs the ₹5,000 cap |
| `voice`, `timing` | dialogue through the QC loop; fit shots to dialogue |
| `compute start / stop / status / tunnel` | GridShare sessions and ComfyUI tunnel |
| `qc run / queue / rate / report / calibrate` | the feedback system |
| `budget report / log / calibrate` | spending and measured costs |
| `pipeline plan / status` | the 23 stages and what to do next |

## Layout

```
.claude/skills/     36 department skills (Claude loads them automatically)
CLAUDE.md           studio operating system: rules, routing, gates
series/             canon per series: bible, scripts, shot lists (_template/)
studio/             Python: series, legal, budget, feedback, compute, CLI, orchestrator
integrations/       adapters + registry.yaml (every tool/model with license state)
scripts/            project engine (create_project.py), workflows, legacy adapters
legal/              denylist; consent records stay outside git
docs/               SETUP · PIPELINE · STACK · FEEDBACK · BUDGET · LEGAL · system/
tests/              unittest suite (runs in CI on every push)
projects/           engine projects with heavy media (git-ignored)
```

## Rules that keep the channel safe

Nothing is generated with a tool or model that is not cleared for
commercial use, every generated file carries a provenance record, and an
episode cannot pass the release gate unless all of it checks out. See
[docs/LEGAL.md](docs/LEGAL.md). Not legal advice.

This repository is private. Keep it that way: it holds unreleased scripts
and character designs.
