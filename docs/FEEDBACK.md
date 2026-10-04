# The feedback system

The requirement: *the full stack keeps producing consistent, high-quality
anime without someone checking every frame.* The design: measure
everything that can be measured, retry intelligently, send only real
problems to a human, and learn the owner's taste from their ratings.

```
            ┌──────────────── Level 4: studio learning ───────────────┐
            │  calibrated thresholds & GPU benchmarks → config.yaml    │
            │  lessons → bible, prompt library, workflows              │
            └───────────────▲──────────────────────────────────────────┘
                            │
   Level 3: episode review — owner ratings, report, calibration, lessons
                            ▲
   Level 2: quality loop — approve │ retry (adjusted) │ human │ reject
                            ▲
   Level 1: checks — tech · loudness · dialogue accuracy · identity ·
                     palette · flicker · black frames · provenance
```

## Level 1: checks (`studio/feedback/checks.py`)

| Check | Measures | Tool | Default threshold |
|---|---|---|---|
| tech_video | resolution, 24 fps, exact shot duration | ffprobe | config `render` |
| tech_image | minimum height | ffprobe | 1024 px |
| loudness | integrated LUFS, true peak | ffmpeg ebur128 | −14 ±1 LU, ≤ −1 dBTP |
| voice_peak | clipping in a voice line | ffmpeg | ≤ −0.5 dBTP |
| dialogue_accuracy | TTS said the script | faster-whisper + WER/CER | EN 0.15, HI 0.25 |
| identity | same character as the model sheet | imgutils CCIP | 0.82 (per character override) |
| palette | bible colours present | Pillow | 60% of colours |
| flicker | frame-to-frame "pops" in a clip | ffmpeg signalstats | spike ≤ 6× median |
| black_frames | unintended black | ffmpeg blackdetect | none ≥ 0.5 s |
| provenance | sidecar exists, all tools/models/LoRAs cleared | license gate | must pass |

Honesty rule: a check that cannot run is **skip**, and a skipped required
check means the asset goes to a human, never auto-approved.

## Level 2: the loop (`studio/feedback/loop.py`)

Each failure maps to a specific adjustment, within limits:

| Failed | Next attempt |
|---|---|
| identity | new seed, LoRA weight +0.1 (≤ 1.3), reference strength +0.1 |
| palette | new seed, palette emphasis +0.1 |
| flicker | new seed, motion strength −0.1 |
| dialogue_accuracy | new seed, speech speed −0.05 |
| voice_peak | gain −3 dB |
| tech_*, loudness | no retry: it is a pipeline bug, goes to a human |
| provenance | **reject**: a legal problem is never "retried away" |

Stops at `feedback.max_attempts` per kind, or when the episode budget
guard says the next attempt would exceed the cap. Everything is logged to
`20_qc/feedback/journal.jsonl`; human items to `review_queue.json`.

## Level 3: episode review (`studio/feedback/review.py`)

The owner rates a sample of assets 1-5. Calibration compares check scores
for liked (≥ 4) and disliked (≤ 2) assets and proposes a threshold
between them, or reports that a check does not predict the owner's
judgement at all (then the metric must change, not the number).

## Level 4: learning

After each episode: apply calibrated thresholds and GPU benchmarks,
record lessons, and turn repeated failures into bible or workflow
changes. The `feedback-loop` skill walks through it.

## What this cannot do (yet)

- Judge story, acting and comedic timing. Those stay with the owner.
- Judge Hindi naturalness beyond "it said the words": the owner's Hindi
  listening pass is part of the process by design.
- Identity of characters that are tiny in frame or heavily occluded:
  CCIP is less reliable there; those shots tend to land in human review.
