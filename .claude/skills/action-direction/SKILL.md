---
name: action-direction
description: Action and fight choreography for anime - beat sheets, spatial geography, escalation, readability, impact moments and how to turn a fight into shots that AI generation can deliver. Use when writing or planning any fight, chase, battle, power display or physical set piece.
---

# ACTION DIRECTION

Action is storytelling with bodies. Every exchange must change something:
who has the advantage, what is at stake, or what a character learns.

## 1. Before any shots: the beat sheet

For each set piece write, in `treatment.md`:

1. **Goal**: what each side wants from this fight.
2. **Geography**: the space (rooftop edge, the lantern, the stairwell) and
   where everyone starts. Draw it once in Blender layout.
3. **Beats**: 5-9 exchanges. Each beat = action -> reaction -> new state.
4. **Turn**: the moment the advantage flips.
5. **Cost**: what the winner loses.
6. **Button**: the final image that ends the sequence.

## 2. Escalation

Start small and readable, end big. Typical shape: probe -> first exchange
-> complication (environment, a power, an injury) -> low point for the
hero -> turn -> climax -> aftermath hold. Do not open with the biggest move.

## 3. Readability rules

- Establish the space with a wide shot before cutting close.
- Keep screen direction: the hero attacks left-to-right until a deliberate
  reversal signals a power shift.
- One idea per shot. If a shot description has "and then" twice, split it.
- Show the impact or its result, not both at length.
- Hold after the big hit (12-24 frames) so it lands.

## 4. Turning beats into shots

| Beat element | Shot treatment | Motion type |
|---|---|---|
| Wind-up | close on eyes/hands, slow push | `camera` |
| Strike | 1 strong full-motion moment | `full` (3-5 s) |
| Impact | impact frame + shake on a held drawing | `camera` (shake) |
| Reaction | held pose, debris, speed lines | `hold`/`camera` |
| Reposition | wide shot showing new geography | `camera` (pan) |

A 60-second fight is usually 14-20 shots with only 4-6 of them `full`.

## 5. Writing motion prompts for full shots

- One main motion, physically specific: direction, weight, timing.
- Fix the camera ("static camera" or "slow push in"); camera plus body
  motion together drifts.
- Name what must NOT change (outfit, hair, weapon in right hand).
- Start from the approved keyframe (image-to-video), end on a pose you can
  cut from.

## 6. Safety and taste

Violence serves story. Avoid gore close-ups (platform and audience
limits for a 13+ channel); show consequence through reaction, sound and
aftermath instead.
