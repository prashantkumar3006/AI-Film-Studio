---
name: shot-compiler
description: Compile an episode script and treatment into shotlist.json - the machine contract every pipeline stage reads - with valid IDs, durations, motion types, camera, bible characters and outfits, prompts and bilingual dialogue. Use after a script is approved or whenever the shot list must be created, revised or fixed after shots check errors.
---

# SHOT COMPILER

`series/<slug>/episodes/EXX/shotlist.json` drives voice, layout,
keyframes, motion, lip sync, edit, QC and the budget. Precision here saves
GPU money later.

## 1. Inputs

- `script.md` (approved) and `treatment.md` (director + action direction)
- The bible: `series.yaml`, `bible/style.yaml`, `bible/characters/*.yaml`,
  `bible/locations/*.yaml`
- Previous episode `continuity.json` (outfits, injuries, props)

## 2. Schema (per shot)

```json
{
  "id": "SC03_SH012",
  "duration_s": 4.0,
  "purpose": "Kael realises the lantern is fake.",
  "motion": "hold | camera | limited | full",
  "camera": {"framing": "ECU|CU|MCU|MS|WS|EWS", "angle": "eye|low|high|dutch", "move": "static|push_in|pull_out|pan_left|pan_right|tilt_up|tilt_down|shake|tracking|orbit", "lens_mm": 35},
  "characters": [{"id": "kael", "outfit": "default", "expression": "shocked"}],
  "action": "physical description for animation",
  "visual_prompt": "what the keyframe shows (no IP names, no studio styles)",
  "negative_prompt": "",
  "dialogue": [{"character": "kael", "emotion": "quiet", "line": {"en": "...", "hi": "..."}}],
  "sfx": ["glass crack"],
  "music_cue": "theme_mystery",
  "notes": ""
}
```

Scene: `{"id": "SC03", "location": "<bible location id>", "time_of_day": "night", "summary": "...", "shots": [...]}`.

## 3. Rules (the validator enforces them)

- IDs: `SC01`, `SC01_SH001`; shot IDs start with their scene ID; unique.
- `duration_s` 0.5-20 s; `full` shots ideally ≤ 5 s (one generation).
- Every character and outfit exists in the bible; every scene location too.
- Every dialogue line has every series language (`en` and `hi`).
- Dialogue must fit: about 2.6 words/s English, 2.4 Hindi, plus 0.25 s
  lead-in. The `timing` stage lengthens shots to fit recorded lines.
- `full` share of runtime under the series policy (default 30%).
- Total runtime within 10% of the target (20 min).

## 4. Writing visual prompts

Start with the character's LoRA trigger and outfit prompt from the bible,
then pose, expression, framing, location, light. The style prefix and
negative come from `style.yaml` automatically; do not repeat them.
Never name existing anime, characters, studios or real people (the legal
scan blocks them).

## 5. After writing

```bash
python -m studio shots check <series> <n>
python -m studio legal scan <series> <n>
python -m studio estimate <series> <n>
```

Fix every error. If the estimate is over cap, convert the least important
`full` shots to `camera` or `limited` and re-run.
