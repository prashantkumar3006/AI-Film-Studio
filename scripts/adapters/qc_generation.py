#!/usr/bin/env python3
"""QC handoff for the engine's AI generation workflow.

Runs the studio feedback checks on every output file in a generation
folder and writes ``<output>/qc_report.json``.

Exit codes: 0 all approved, 3 needs human review, 4 rejected (legal),
2 usage/config error. A non-zero exit stops the engine workflow, which
is the point: nothing unreviewed flows downstream.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from studio.common import StudioError, dump_json  # noqa: E402
from studio.feedback.loop import HUMAN, REJECT, QualityLoop  # noqa: E402
from studio.legal.provenance import SIDECAR_SUFFIX  # noqa: E402
from studio.orchestrator.config import load_config  # noqa: E402

KIND_BY_SUFFIX = {".png": "keyframe", ".jpg": "keyframe", ".jpeg": "keyframe", ".webp": "keyframe", ".mp4": "video", ".mov": "video", ".webm": "video", ".wav": "voice_line"}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--project-slug", required=True)
    parser.add_argument("--shot-id", required=True)
    parser.add_argument("--output", required=True, help="generation folder (absolute or project-relative)")
    args = parser.parse_args(argv)

    try:
        config = load_config()
        project = Path(config["projects"]["root"])
        project = (Path(__file__).resolve().parents[2] / project / args.project_id / args.project_slug)
        out_dir = Path(args.output)
        if not out_dir.is_absolute():
            out_dir = project / out_dir
        files = [p for p in sorted(out_dir.glob("*")) if p.suffix.lower() in KIND_BY_SUFFIX and not p.name.endswith(SIDECAR_SUFFIX)]
        if not files:
            print(f"No generated media found in {out_dir}", file=sys.stderr)
            return 3
        loop = QualityLoop(project, config)
        verdicts = [loop.evaluate(path, KIND_BY_SUFFIX[path.suffix.lower()], {"shot": {"id": args.shot_id}}) for path in files]
        dump_json({"shot_id": args.shot_id, "verdicts": [v.as_dict() for v in verdicts]}, out_dir / "qc_report.json")
        for verdict in verdicts:
            print(f"{verdict.decision.upper():13} {Path(verdict.asset).name}: {'; '.join(verdict.reasons)}")
        if any(v.decision == REJECT for v in verdicts):
            return 4
        if any(v.decision == HUMAN for v in verdicts):
            return 3
        return 0
    except StudioError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
