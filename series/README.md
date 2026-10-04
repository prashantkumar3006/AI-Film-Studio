# Series canon

Each series lives in `series/<slug>/` and is version-controlled text plus
approved reference images. Heavy media never goes here; it lives in the
episode's engine project under `projects/` (git-ignored).

```
series/<slug>/
  series.yaml            format, languages, animation policy, narrator
  bible/
    world.md             rules of the world
    style.yaml           art direction, palette, prompt prefix/negative
    characters/<id>.yaml appearance, palette, outfits, voices, LoRA, refs
    locations/<id>.yaml
    refs/                approved model sheets and location art
  episodes/EXX/
    episode.yaml         status and link to its engine project
    script.md            writer
    treatment.md         director + action direction
    shotlist.json        the machine contract for every stage
    continuity.json      state at the end of the episode
```

Create one: `python -m studio series new <slug> --title "..."`, then
`python -m studio episode new <slug> 1 --title "..."`.
`_template/` is the starting point for both.
