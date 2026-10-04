---
name: anime-direction
description: Anime-specific direction and animation craft - limited animation, holds, animating on twos and threes, layouts, impact and smear frames, background pans and where to spend the full-motion budget. Use when directing a scene, choosing motion types for shots, or making an episode look like real anime within budget.
---

# ANIME DIRECTION

TV anime looks expensive because it spends motion carefully, not because
everything moves. Copy that discipline: it is also how a ₹5,000 episode
becomes possible.

## 1. The motion budget

Each shot in `shotlist.json` gets one motion type:

| Type | What it is | Use for |
|---|---|---|
| `hold` | a still drawing | reactions, tension, beauty shots, comedic pauses |
| `camera` | still + pan/push/tilt/shake | establishing, reveals, slow dread, impacts |
| `limited` | still + mouth flaps / small loops (hair, cloth, blink) | dialogue |
| `full` | AI image-to-video | action peaks, emotional climaxes, signature moments |

Default distribution for a 20-minute episode: about 25% `full`, 35%
`limited`, 25% `camera`, 15% `hold`. The series policy caps `full`
(usually 30%). Spend `full` where the audience will remember it: the
first big moment, the climax, the final image.

## 2. Timing

- 24 fps. Characters animate on twos (12 drawings/s); slow or heavy
  motion on threes. Mouths change at most every 2 frames.
- Hold a strong pose 12-24 frames before and after fast action so the eye
  can read it.
- Anticipation -> action -> follow-through. A punch needs a wind-up frame.
- Cut on action: the edit point sits inside the motion, not after it.

## 3. Layout and composition

- Every shot has a clear subject and a clear direction of attention.
- Keep screen direction consistent (the 180-degree rule) within a scene.
- Low angle = power, high angle = vulnerability, Dutch angle = unease
  (sparingly).
- Large painted backgrounds plus a slow pan create scale cheaply.

## 4. Anime signatures (cheap and effective)

- Impact frames: 1-3 frames of high-contrast colour inversion or
  silhouette on a hit.
- Smear frames on fast swings.
- Speed lines on a held pose with camera shake.
- Light blooms, lens flares and particles in compositing.
- The held close-up with only the eyes or a single tear moving.

## 5. Directing the generator

- Generate the keyframe first, approve it, then animate from it. Never
  text-to-video a character shot.
- For `full` shots, describe motion in physical terms ("coat flares
  left, she lands on her right knee, dust rises") and keep camera motion
  simple: the model handles one big motion better than three small ones.
- If a full shot fails QC twice, downgrade it to `camera` with an impact
  frame rather than spending a third attempt.

## 6. Checklist per scene

- [ ] Scene intent stated in one line
- [ ] Motion types chosen deliberately (not all `full`)
- [ ] One memorable image per scene
- [ ] Screen direction consistent
- [ ] Holds before and after every action beat
