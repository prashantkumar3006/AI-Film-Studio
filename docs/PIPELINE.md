# Episode pipeline

`python -m studio pipeline plan` prints the 23 stages; `pipeline status
<series> <n>` shows which are done (read from disk) and the next action.

| # | Stage | Owner skill | Runs on | Type | Gate / output |
|---|---|---|---|---|---|
| 1 | Script | writer | Claude | assist | `script.md` |
| 2 | Director's treatment, action beats | director, action-direction, anime-direction | Claude | assist | `treatment.md` |
| 3 | Shot list | shot-compiler | Claude | assist | `shotlist.json` |
| 4 | Validate vs bible | continuity | laptop | **gate** | `shots check` |
| 5 | IP / real-person scan | legal-rights | laptop | **gate** | `legal scan` |
| 6 | Budget estimate | producer, compute-budget | laptop | **gate** | `estimate` ≤ cap |
| 7 | Voices (EN + HI) | sound, localization-hindi | laptop + GPU | auto | `voice --execute` |
| 8 | Dialogue QC | qc | laptop | **gate** | STT vs script, peaks |
| 9 | Timing lock | editor | laptop | auto | `timing --apply` (picture follows dialogue) |
| 10 | Blender layout | storyboard-previs | laptop | assist | Blender MCP + layout renders |
| 11 | Keyframes | ai-generation, anime-prompting | GPU | auto | ComfyUI via quality loop |
| 12 | Keyframe QC + approval | continuity, qc | laptop | **gate** | identity, palette, provenance, review queue |
| 13 | Motion | animation | laptop + GPU | auto | camera moves (CPU) / Wan2.2 I2V (GPU) |
| 14 | Lip sync | performance | laptop | auto | Rhubarb + mouth frames |
| 15 | Titles & graphics | vfx-motion | laptop | auto | Remotion |
| 16 | Music & SFX | music | GPU | assist | theme library + cues |
| 17 | Edit | editor | laptop | auto | EDL → `picture.mp4` |
| 18 | Mix per language | sound | laptop | auto | −14 LUFS, ducking |
| 19 | Subtitles | distribution | laptop | auto | SRT per language |
| 20 | Master QC | qc | laptop | **gate** | tech, loudness, black frames + owner viewing |
| 21 | Release gate | legal-rights | laptop | **gate** | provenance + licenses + disclosure |
| 22 | Package | distribution | laptop | auto | MP4 with EN/HI audio + subtitles |
| 23 | Review & lessons | feedback-loop | Claude | assist | ratings, calibration, lessons |

## Where the owner's 10 hours go

| Activity | Hours / episode (target) |
|---|---|
| Story decisions and script approval | 2 |
| Character / keyframe approvals (review queue) | 2-3 |
| Hindi listening pass | 1 |
| Final viewing in both languages | 1 |
| Ratings and lessons | 0.5 |

Everything else is Claude and the pipeline. Early episodes will take
longer while the thresholds and workflows are tuned; that is expected.

## Running a stage by hand

```bash
python -m studio shots check my-show 1
python -m studio legal scan my-show 1
python -m studio estimate my-show 1
python -m studio voice my-show 1                 # plan
python -m studio voice my-show 1 --execute       # generate + QC loop
python -m studio timing my-show 1 --apply
python -m studio qc my-show 1 queue
python -m studio legal release-gate my-show 1
```
