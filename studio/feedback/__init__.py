"""Built-in feedback system.

Four levels, each feeding the next:

1. **Asset checks** (``checks``): technical, audio, dialogue accuracy,
   identity, palette, temporal stability, provenance.
2. **Quality loop** (``loop``): approve / retry with adjusted parameters /
   human review / reject, within attempt and budget limits.
3. **Episode review** (``review``): pass rates, retries, human ratings,
   threshold calibration, lessons learned.
4. **Studio learning**: calibrated thresholds and benchmarks go back into
   ``studio/config.yaml``; lessons update the bible and prompt library
   (the ``feedback-loop`` skill drives this step).
"""
