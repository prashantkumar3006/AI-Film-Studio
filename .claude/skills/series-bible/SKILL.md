---
name: series-bible
description: Create and maintain the series bible - world rules, art direction style guide, character sheets with exact palettes, outfits, voices per language, LoRA records and approved reference images - under change control. Use when creating a series, designing or changing a character, location or style, or training a character LoRA.
---

# SERIES BIBLE

Consistency is measured against the bible. If the bible is vague, QC
cannot catch drift, and the series will not look like one show.

## 1. What a character needs before production

- `appearance`: concrete, visible traits (hair length and style, eye
  shape and colour, scars, accessories). Avoid adjectives like "pretty".
- `palette`: exact `#RRGGBB` for hair, eyes, skin, outfit primary and
  accent. The palette check compares frames against these.
- `outfits`: at least `default`, each with a short prompt fragment.
- `voice`: one per language, with a cleared engine (`tts_kokoro` for
  English, `tts_indic_parler` for Hindi). No real-person clones without
  a consent record.
- `references.model_sheet`: an approved image under `bible/refs/`.
- `status: approved` only after the owner approves the model sheet.

Validate: `python -m studio series check <slug>`.

## 2. Making the model sheet

1. Write the appearance and palette first.
2. Generate many candidates with a cleared checkpoint (for example
   `animagine_xl_4` once its conditions are acknowledged), front view,
   neutral expression, plain background.
3. The owner picks one. Then generate side, back and 6-8 expressions with
   reference editing (`qwen_image_edit_2509`) from that pick, so they
   share one identity.
4. Assemble into `refs/<id>/model_sheet_v001.png`; record it in the
   character file; set status to `approved`.

## 3. Character LoRA

- Train only on your own approved images (20-40), varied pose and
  expression, consistent outfit. No screenshots or art from anywhere else.
- Record `base_model`, `training_data` and set `training_data_cleared: true`
  only when every training image came from cleared models or your own art.
  The release gate checks this.
- Trigger word: short and unusual (`ar1a`). Typical weight 0.7-0.9.
- Version files (`aria_v001.safetensors`); keep them on the GridShare
  disk and a backup, not in git.

## 4. Change control

Changing a palette, outfit or model sheet after episodes exist:

1. Record the change and reason (decision log).
2. Bump versions (`model_sheet_v002`, `lora v002`).
3. Decide: does it apply from the next episode only, or retroactively?
4. Re-run identity QC on affected shots if retroactive.
Never silently edit an approved character.

## 5. Locations and style

- Locations: palette, lighting by time of day, ambience sound, and a
  Blender layout file with named cameras for recurring sets.
- `style.yaml`: medium, line, shading, palette, prompt prefix/negative,
  and motion rules. Describe qualities, never cite a studio or artist.
