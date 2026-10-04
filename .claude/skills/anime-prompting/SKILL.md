---
name: anime-prompting
description: Write and debug prompts and ComfyUI parameters for consistent anime keyframes and image-to-video clips - prompt structure, LoRA triggers and weights, negatives, control and reference strength, seeds and the prompt library. Use when writing visual prompts, when a generated image or clip is off-model, or when the feedback loop keeps retrying a shot.
---

# ANIME PROMPTING

## 1. Keyframe prompt structure (SDXL-family anime checkpoints)

Order matters: earlier tokens weigh more.

```
<style prefix from style.yaml>, <LoRA trigger>, <subject + count>,
<outfit prompt from bible>, <expression>, <pose/action>,
<framing + angle>, <location + time of day>, <lighting>, <mood>
```

Example: `masterpiece, anime screencap style, cel shading, ar1a, 1girl,
short silver bob, amber eyes, navy coat with brass buttons, determined
expression, gripping the lantern, medium close-up, low angle, observatory
rooftop at night, warm lantern rim light, wind`.

Negative comes from `style.yaml`; add shot-specific negatives only when a
problem repeats (for example `extra lantern`).

## 2. Consistency levers, strongest first

1. **Reference editing** (`qwen_image_edit_2509`) from the approved model
   sheet: best for identity across angles and expressions.
2. **Character LoRA** at 0.7-0.9. Above 1.0 it bakes in artefacts.
3. **Layout control** from the Blender render (depth/lineart ControlNet,
   strength 0.4-0.7): locks composition and perspective.
4. **Palette words** for drift-prone colours ("navy coat", "silver hair").
5. **Seed**: only reuse a seed for near-identical shots; seeds do not
   carry identity across different prompts.

## 3. When the feedback loop retries

| Failing check | What to change |
|---|---|
| identity | +0.1 LoRA weight, +0.1 reference strength, new seed; if it still fails, regenerate the shot from a reference edit |
| palette | add the drifting colour words, lower CFG slightly, new seed |
| flicker (video) | lower motion strength, shorter clip, simpler camera |
| tech | it is a workflow problem (size, fps): fix the workflow, do not reroll |

The loop applies the numeric changes automatically; you handle wording.

## 4. Image-to-video (Wan2.2) prompts

- Start from the approved keyframe.
- Describe one physical motion, its direction and weight; state the
  camera explicitly ("static camera").
- 3-5 s per clip at 16-24 fps source; the edit retimes to 24 fps.
- Name what must not change ("outfit unchanged, hair silver").

## 5. Prompt library

When a prompt produces an approved result, save it under
`series/<slug>/bible/prompts/` with the shot type ("lantern close-up,
night, rim light"). Reuse beats reinvention: consistency is mostly
repetition of what already worked.

## 6. Never

Names of existing anime, characters, studios, artists or real people;
"in the style of <studio>". Describe the qualities instead.
