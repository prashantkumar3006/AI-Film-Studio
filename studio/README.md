# studio/ — the studio's Python packages

Standard library plus PyYAML. Run everything through `python -m studio`.

| Package | Responsibility |
|---|---|
| `cli.py` | The command line (`python -m studio --help`) |
| `common.py` | Paths, JSON/YAML helpers, `StudioError` |
| `series/` | Bible loading and validation, shot lists, series/episode creation |
| `legal/` | License gate (`licenses`), provenance sidecars and the release gate (`provenance`), IP/real-person scan (`content`) |
| `budget/` | Episode cost estimate and the append-only spending ledger with budget guard and calibration |
| `feedback/` | Media measurements, QC checks, the quality loop, episode review and calibration |
| `compute/` | GridShare over SSH: remote runs, file transfer, ComfyUI tunnel, GPU session tracking |
| `orchestrator/` | Config loading, the general workflow planner (`pipeline.py`) and the anime episode pipeline (`anime.py`) |
| `config.yaml` | All tunable settings: render, audio, legal mode, budget, feedback thresholds, tool commands |

Design rules:

1. **Laptop first.** Anything that can run on a CPU does.
2. **Adapters, not coupling.** External tools are reached only through
   `integrations/`.
3. **Gates are code.** Legal, budget and QC rules live in functions with
   tests, not in documents alone.
4. **Honest state.** Status is read from files on disk; unmeasured never
   means passed.
5. **Generated media is never committed.** It lives in `projects/`.
