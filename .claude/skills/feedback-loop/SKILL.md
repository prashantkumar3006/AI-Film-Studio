---
name: feedback-loop
description: Run and improve the studio's built-in feedback system - automated asset checks, the approve/retry/human-review loop, the review queue, owner ratings, threshold and cost calibration, and lessons that update the bible and prompts. Use after any generation batch, when reviewing QC results, at the end of every episode, or when quality or consistency is slipping.
---

# FEEDBACK LOOP

Four levels. Each one feeds the next, so the studio gets better every
episode instead of repeating mistakes.

## Level 1 — asset checks (automatic)

| Kind | Required checks |
|---|---|
| keyframe | tech_image, provenance, identity, palette |
| video | tech_video, provenance, identity, flicker, black_frames |
| voice_line | voice_peak, dialogue_accuracy, provenance |
| music | provenance |
| master | tech_video, loudness, black_frames |

A check that cannot run (tool missing, no model sheet) is `skip`. A
skipped required check never counts as a pass: the asset goes to the
owner instead. Install the QC extras (`pip install -r requirements-qc.txt`)
so most assets can be approved automatically.

Run one by hand: `python -m studio qc <series> <n> run --asset <file> --kind keyframe --shot SC01_SH002`.

## Level 2 — the loop (automatic)

approve -> next shot. retry -> new seed plus targeted adjustments (LoRA
weight, reference strength, motion strength, speed). human_review ->
review queue. reject -> legal problem, never retried.
Limits: `feedback.max_attempts` per kind and the episode budget guard.

## Level 3 — episode review (you + owner, end of each episode)

1. `python -m studio qc <series> <n> queue` — resolve every open item.
2. Owner rates a sample: 10 approved keyframes, 5 approved clips, 10
   Hindi lines, 10 English lines (`qc rate --asset ... --score 1-5`).
   Include some the machine rejected: disagreements teach the most.
3. `python -m studio qc <series> <n> report` — first-pass rate, top
   failures, mean attempts.
4. `python -m studio qc <series> <n> calibrate` — threshold suggestions.
   Apply a suggestion only when it says `suggest`; if it says the check
   "does not predict human judgement", the metric itself needs replacing.
5. `python -m studio budget <series> <n> calibrate` — real GPU seconds per
   unit; copy medians into `budget.benchmarks_gpu_s` so the next estimate
   is accurate.

## Level 4 — studio learning

Turn findings into durable changes, each through a reviewed commit:

- Repeated identity failures for one character -> improve the model
  sheet or retrain the LoRA (series-bible change control).
- Repeated palette drift -> add colour words to the outfit prompt.
- Retries concentrated in one shot type -> a better ComfyUI workflow or a
  cheaper motion type for that type.
- Record each lesson: `python -m studio lessons <series> <n> --area continuity --lesson "..." --action "..."`.

## Targets to watch

| Metric | Healthy |
|---|---|
| keyframe first-pass rate | > 50% after episode 3 |
| mean attempts per full clip | < 2.5 |
| owner mean rating | ≥ 4 |
| spend vs cap | ≤ 80% |

Report these at the end of each episode and compare with the previous one.
