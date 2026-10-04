---
name: localization-hindi
description: Hindi adaptation and dubbing for the series - writing natural Hindi dialogue (adaptation, not literal translation), register and code-mixing, voice casting with Indic Parler-TTS speakers, timing to picture, Hindi QC and subtitles. Use when writing or reviewing Hindi lines, generating Hindi voices, or preparing the Hindi version of an episode.
---

# HINDI LOCALIZATION

The Hindi version is a first-class release, not a subtitle track. The
owner judges Hindi quality; your job is to give them lines worth judging.

## 1. Adapt, don't translate

- Keep intent, emotion and character voice; change words freely.
- Match the line's length within about 15% so timing still fits.
- Idioms: replace with natural Hindi equivalents, not literal ones.
- Register by character: formal (`आप`) vs informal (`तुम`, `तू`) is a
  character decision; record it in the character file and keep it.
- Everyday spoken Hindi accepts some English words (mission, plan, okay).
  Use them where a real speaker would; avoid heavy Sanskritised Hindi
  unless it is the character's voice (a priest, an ancient being).
- Names and invented terms: transliterate once in the bible glossary
  (`world.md`) and reuse exactly.

## 2. Writing in the shot list

Both languages live in each dialogue item:
`"line": {"en": "We leave tonight.", "hi": "हम आज रात निकलेंगे।"}`.
Use Devanagari, standard punctuation, and `।` for full stops.

## 3. Voices

- Engine: `tts_indic_parler` (Apache-2.0). Named Hindi speakers include
  Rohit and Divya (recommended), Aman and Rani.
- One speaker plus one fixed description per character, recorded in the
  character's `voice.hi`. Changing either changes the character.
- Emotion comes mostly from the description and punctuation; keep
  descriptions consistent and vary only intensity words.
- Generate all Hindi lines in one GPU session (`python -m studio voice
  <series> <n> --language hi --execute`).

## 4. QC

- Dialogue accuracy: speech-to-text on every line, error threshold 0.25
  for Hindi (lower of word/character error).
- The owner listens to every Hindi line flagged by the loop, plus a sample
  of passed ones, and rates them (`qc rate`). Ratings calibrate the
  threshold over time.
- Mouth timing: Hindi uses Rhubarb's phonetic recognizer; it is
  language-independent, so it works on Hindi audio.

## 5. Subtitles and delivery

- Hindi SRT from the Hindi timeline; 42 characters per line, 2 lines.
- Deliver either a separate Hindi upload or a second audio track if the
  channel has YouTube multi-language audio available; keep a fully mixed
  Hindi MP4 regardless.
