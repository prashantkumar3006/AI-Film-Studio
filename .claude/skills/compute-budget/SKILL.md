---
name: compute-budget
description: Plan and control GPU spending on GridShare India within the per-episode cap - estimates, batching work into sessions, choosing GPUs, session logging, the budget guard and calibration from measured jobs. Use before renting any GPU, when an estimate is over cap, or when reviewing what an episode cost.
---

# COMPUTE BUDGET

## 1. The money model

- GridShare bills per instance hour. Listed prices (ex-GST, checked
  2026-10-04): RTX 3090 ₹30/h, 4080 ₹42/h, 4090 ₹48/h, 5090 ₹51/h. GST 18%
  on top. Re-check prices; update `budget.gpu_rates_ex_gst`.
- Cap: ₹5,000 per episode including GST (`budget.per_episode_cap`).
- Idle time costs the same as work. A forgotten instance is the biggest risk.

## 2. Estimate before renting

`python -m studio estimate <series> <n>` prices every stage from the shot
list. With the starting assumptions, a 20-minute episode costs roughly
(with 15% margin):

| Full AI video share | Est. cost |
|---|---|
| 0% | ≈ ₹1,430 |
| 25% | ≈ ₹2,760 |
| 30% | ≈ ₹3,030 |
| 50% | ≈ ₹4,100 |
| 100% | ≈ ₹6,770 (over cap) |

These are assumptions until calibrated: a first real episode may cost
more because retries are higher while the pipeline is new.

## 3. Choosing a GPU

- RTX 4090 (24 GB): default. Fits Wan2.2 TI2V-5B, SDXL + ControlNet,
  Qwen-Image-Edit with offloading, Indic Parler-TTS, LoRA training.
- RTX 5090 (32 GB): when 14B video models need more memory; check
  speed per rupee with a timed test first.
- Never rent bigger "just in case"; measure.

## 4. Session discipline

1. Prepare everything first (see studio-manager §3).
2. `python -m studio compute start <series> <n> --gpu rtx_4090`
3. Open the tunnel for ComfyUI: `python -m studio compute tunnel`
4. Run the whole batch.
5. Pull outputs, then `python -m studio compute stop <series> <n>` and
   stop the instance on gridshare.in.
6. Keep models on a persistent volume if GridShare offers one, so each
   session does not re-download 20+ GB (session overhead is budgeted at
   20 minutes; measure it).

## 5. When over budget

In order: convert `full` shots to `limited`/`camera`, shorten long `full`
shots to one 5 s generation, reduce keyframe candidates from 4 to 2 for
simple shots, reuse music cues. Raising the cap is the owner's decision.

## 6. Calibrate

After each episode: `python -m studio budget <series> <n> calibrate` and
copy the measured medians into `budget.benchmarks_gpu_s`.
