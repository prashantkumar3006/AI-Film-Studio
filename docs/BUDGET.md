# Budget: ₹5,000 per 20-minute episode

## Prices used

GridShare India, listed hourly prices ex-GST *(gridshare.in, checked
2026-10-04)*: RTX 3090 ₹30, RTX 4080 ₹42, **RTX 4090 ₹48**, RTX 5090 ₹51.
GST 18% added. Update `budget.gpu_rates_ex_gst` when prices change.

## What an episode costs (estimator, RTX 4090)

Model: 240 shots × 5 s; voices in English and Hindi; starting throughput
assumptions; retries ×2.5 for video and ×1.5 for images; 4 sessions with
20 min overhead each; 15% safety margin.

| Full AI video share of runtime | GPU hours | Cost incl. GST | With margin | Within ₹5,000? |
|---|---|---|---|---|
| 0% | 21.9 | ₹1,242 | ₹1,429 | yes |
| 25% (recommended) | 42.4 | ₹2,402 | ₹2,763 | yes |
| 30% (series policy cap) | 46.5 | ₹2,635 | ₹3,030 | yes |
| 50% | 62.9 | ₹3,563 | ₹4,097 | yes, little headroom |
| 100% | 103.9 | ₹5,883 | ₹6,765 | **no** |

At 25%, the largest costs are video generation (~22.5 h), keyframes
(~8 h) and mouth shapes (~6.8 h). Laptop-side QC is free and not charged.

**One-time per season**: one LoRA per recurring character, about 45 min
each by assumption — for 6 characters roughly ₹300 incl. GST.

## Honest caveats

- The throughput numbers are **assumptions**, except Wan2.2 TI2V-5B's
  ~9 minutes per 5 s 720p clip on a single consumer GPU, which comes from
  its README. Episode 1 will probably cost more than the table: retries are
  higher while prompts and workflows are new.
- Calibrate after every episode: `python -m studio budget <series> <n> calibrate`.
- Session overhead (boot, model loading) and forgotten instances are the
  usual budget leaks. The session commands and `compute status` warning
  exist for this reason.

## Levers when over budget (in order)

1. `full` → `limited` or `camera` for low-importance shots
2. One 5 s generation per `full` shot, not chained clips
3. 2 keyframe candidates instead of 4 for simple shots
4. Reuse the music theme library
5. Raise the cap (owner decision only)
