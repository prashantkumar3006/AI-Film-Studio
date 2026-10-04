# Legal guide: copyright, licenses and commercial use

**Not legal advice.** This is the studio's working rulebook, written to
keep a monetised YouTube anime channel out of trouble. Before you scale
revenue, sign deals or license the series, have an Indian IP lawyer review
it. Facts marked *(checked 2026-10-04)* were verified against the cited
source on that date; everything else should be re-checked when it matters.

---

## 1. The three questions for every asset

1. **May we use this tool or model commercially?** → license gate
   (`integrations/registry.yaml`, `python -m studio legal check`)
2. **Where did this exact file come from?** → provenance sidecar
   (`<file>.prov.json`, written automatically by every adapter)
3. **Does it copy someone else's work, character, name, face or voice?**
   → content scan (`legal/denylist.yaml`, `python -m studio legal scan`)
   plus human judgement

The release gate (`python -m studio legal release-gate <series> <n>`)
refuses to pass an episode unless all three are answered for every file.

---

## 2. Tool and model licenses

The code license and the **weights** license are different things. A
repository can be MIT while its model weights are non-commercial.

| Status in this studio | Examples | Why |
|---|---|---|
| Cleared (verified) | ComfyUI (GPL-3.0 software), Blender ("what you create is your sole property"), FFmpeg, faster-whisper, Kokoro-82M, Indic Parler-TTS, Wan2.2, Qwen-Image-Edit-2509, Rhubarb, Blender MCP | Apache-2.0 / MIT weights or code, checked at source *(2026-10-04)* |
| Conditional: owner must acknowledge | Remotion (free up to 3 people), Animagine XL 4.0 (OpenRAIL++-M use restrictions) | Commercial use allowed with conditions *(2026-10-04)* |
| Blocked: non-commercial | F5-TTS weights (CC-BY-NC), NoobAI-XL (fair-ai-public-license prohibits commercialising generated products), MusicGen weights (CC-BY-NC), XTTS-v2 (CPML) | Would make a monetised episode infringing |
| Blocked until verified | Illustrious-XL and merges, FLUX.1 dev, ACE-Step weights, RIFE / Real-ESRGAN weights, CCIP weights, ComfyUI custom nodes | Not yet checked; versions differ |

How to clear an entry after reading its license:

```bash
python -m studio legal verify ace_step --source <license URL> --commercial-use allowed
python -m studio legal acknowledge motion_remotion      # for conditional licenses
```

Re-verify whenever you change a model version (`pin`). Community
"merges" on model-sharing sites inherit the most restrictive license of
everything merged into them — treat them as blocked unless documented.

**ComfyUI custom nodes** each have their own license. Add every node pack
you install to the registry.

---

## 3. Indian law essentials

**Ownership of what you make.** The Copyright Act, 1957 covers scripts
(literary works), character art (artistic works), music and sound
recordings, and the episode itself (cinematograph film). For
computer-generated works, section 2(d)(vi) names the author as the person
who causes the work to be created, and section 17 makes the author the
first owner unless there is a contract saying otherwise. Whether purely
AI-generated output qualifies for protection is **not settled** in India;
the Copyright Office's handling of the AI-credited painting "Suryast"
(the RAGHAV application) shows the uncertainty. Practical consequence:
keep real human creative control — your scripts, character designs,
selection, editing and direction — and document it. That human authorship
is what you can most confidently claim and register.

**Contracts.** Anyone else who contributes (a voice actor, an artist, a
co-writer) must assign rights in writing (section 19). Verbal agreements
are not enough.

**Registration.** Copyright exists without registration, but registering
scripts and key character art with the Copyright Office gives strong
evidence in a dispute. Consider a trademark for the series name and logo
once it has traction (Trade Marks Act, 1999).

**Personality and voice rights.** Indian courts protect celebrities'
names, likeness and voice against unauthorised commercial use, including
AI voice cloning (for example, Delhi High Court orders for Anil Kapoor and
Amitabh Bachchan, and the Bombay High Court's 2024 order protecting Arijit
Singh's voice from AI cloning). Rule here: **no real person's face, name
or voice**, and no voice cloning of anyone without written consent stored
outside git (`legal/consent/` is git-ignored).

**Synthetic content declarations.** Amendments to the IT Rules notified on
10 February 2026 and in force from 20 February 2026 require users to
declare synthetically generated information when uploading, and require
platforms to label it and keep provenance markers *(checked 2026-10-04,
Hogan Lovells summary)*. This studio's default
`legal.declare_synthetic_content: true` means: always declare.

---

## 4. YouTube rules that affect an automated channel

- **Inauthentic (mass-produced) content.** From 15 July 2025 YouTube's
  Partner Program targets mass-produced, repetitive content without
  meaningful human contribution; AI as a tool remains allowed *(checked
  2026-10-04)*. A fully automated pipeline is exactly what this policy
  watches for. Protection: original stories, consistent characters, real
  creative direction, varied episodes, your own voice in community posts
  and descriptions. Automation must serve quality, not volume.
- **Altered or synthetic content disclosure.** YouTube asks creators to
  disclose realistic synthetic content. Stylised anime is usually outside
  the "realistic" test, but Indian law now expects a declaration anyway,
  so tick it.
- **Content ID.** AI music models can produce melodies close to existing
  songs. Keep the provenance; if a claim appears, you can show your
  generation record. Prefer building your own theme library.
- **Made for kids.** The series is set to a general (13+) audience. If you
  ever mark a video "made for kids", comments and some monetisation are
  disabled; decide per video, honestly.

---

## 5. Style, names and references

- Copyright does not protect a general style, but naming a studio or
  artist in prompts ("in the style of …") invites imitation disputes and
  is flagged by the denylist. Describe qualities instead.
- Never use frames, screenshots or art from existing anime as
  references, LoRA training data or ControlNet inputs.
- Fonts: only fonts whose license allows video use (for example SIL OFL
  fonts such as Noto). Record each font in provenance.
- Third-party assets (Poly Haven, Sketchfab, stock) carry individual
  licenses. Record `third_party_source` and `third_party_license` in
  provenance or the release gate blocks them.

---

## 6. Release checklist (the gate enforces the first four)

- [ ] Every file in the edit has a provenance sidecar
- [ ] Every tool, model and LoRA in those sidecars is cleared
- [ ] Every LoRA's base model and training data is cleared
- [ ] Every third-party asset has a recorded license
- [ ] Content scan has no blocking hits; review hits have a recorded decision
- [ ] Synthetic content declared on upload
- [ ] Description credits the tools, music source and fonts
- [ ] The owner has watched the full master in every language
