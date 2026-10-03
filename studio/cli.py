"""
`studio` command line.

    studio validate <bible.json | episode folder | episode name>

Install once with ``pip install -e .`` to get the ``studio`` command, or run
``python -m studio.cli validate ...`` from the repository root.

Exit codes: 0 = valid, 1 = invalid, 2 = file or setup problem.
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from studio.bible.validate import BibleLoadError, load_bible, resolve_target, summary, validate_bible


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        path = resolve_target(args.target)
        bible = load_bible(path)
        report = validate_bible(bible)
    except (BibleLoadError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"Bible   : {path}")
    for warning in report.warnings:
        print(f"warning : {warning}")
    for error in report.errors:
        print(f"error   : {error}", file=sys.stderr)
    if report.ok:
        print(f"valid   : {summary(bible)}")
        return 0
    print(f"invalid : {len(report.errors)} error(s)", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="studio", description="AI Film Studio command line.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="Check a Production Bible against the schema and its own references.")
    p.add_argument("target", help="Path to bible.json, a folder containing it, or an episode name such as ep00.")
    p.set_defaults(func=cmd_validate)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
