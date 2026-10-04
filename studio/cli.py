"""``python -m studio`` — the studio's command line.

Designed to be driven by Claude (Claude Code in this repo) as much as by
hand: every command prints a readable summary and, with ``--json``, a
machine-readable result. Nothing here spends GPU money unless a command
says ``--execute``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from studio.common import StudioError, dump_json, load_json, relpath, today_iso


# ---------------------------------------------------------------- helpers
def _config() -> Dict[str, Any]:
    from studio.orchestrator.config import load_config

    return load_config()


def _out(args, data: Any, text: Optional[str] = None) -> None:
    if getattr(args, "json", False) or text is None:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    else:
        print(text)


def _issues_text(issues) -> str:
    if not issues:
        return "  no issues"
    return "\n".join(f"  [{i.level.upper():7}] {i.where}: {i.message}" for i in issues)


def _episode(slug: str, number: int):
    from studio.series.bible import load_bible
    from studio.series.episode import episode_dir, load_episode, project_root
    from studio.series.shotlist import load_shotlist

    bible = load_bible(slug)
    episode = load_episode(slug, number)
    folder = episode_dir(slug, number)
    shotlist = load_shotlist(folder / "shotlist.json")
    return bible, episode, folder, shotlist, project_root(episode)


def _require_project(project: Optional[Path]) -> Path:
    if project is None:
        raise StudioError("This episode has no engine project (created with --no-project). Re-create it with a project.")
    return project


# --------------------------------------------------------------- commands
def cmd_doctor(args) -> int:
    checks = []

    def add(name, ok, detail, required=True):
        checks.append({"name": name, "ok": bool(ok), "required": required, "detail": detail})

    add("python>=3.9", sys.version_info >= (3, 9), sys.version.split()[0])
    try:
        import yaml  # type: ignore  # noqa: F401

        add("pyyaml", True, "installed")
    except ImportError:
        add("pyyaml", False, "pip install -r requirements.txt")
    for tool, required in (("ffmpeg", True), ("ffprobe", True), ("ssh", False), ("rsync", False), ("blender", False), ("rhubarb", False), ("node", False), ("npx", False)):
        path = shutil.which(tool)
        add(tool, path, path or "not found", required)
    for module, name in (("PIL", "pillow (palette QC)"), ("faster_whisper", "faster-whisper (dialogue QC)"), ("imgutils", "dghs-imgutils (identity QC)")):
        try:
            __import__(module)
            add(name, True, "installed", False)
        except ImportError:
            add(name, False, "optional: pip install -r requirements-qc.txt", False)
    add("GRIDSHARE_SSH_HOST", os.environ.get("GRIDSHARE_SSH_HOST"), "set" if os.environ.get("GRIDSHARE_SSH_HOST") else "not set (only needed for GPU work)", False)
    try:
        _config()
        add("studio/config.yaml", True, "valid")
    except Exception as error:
        add("studio/config.yaml", False, str(error))
    failed = [c for c in checks if c["required"] and not c["ok"]]
    text = "\n".join(f"  {'OK ' if c['ok'] else ('!! ' if c['required'] else '-- ')} {c['name']:30} {c['detail']}" for c in checks)
    _out(args, {"checks": checks, "ok": not failed}, f"Studio doctor\n{text}\n\n{'READY' if not failed else 'MISSING REQUIRED TOOLS'}")
    return 0 if not failed else 1


def cmd_series_new(args) -> int:
    from studio.series.episode import create_series

    languages = [x.strip() for x in args.languages.split(",") if x.strip()]
    path = create_series(args.slug, args.title, languages)
    _out(args, {"created": relpath(path)}, f"Created series at {relpath(path)}\nNext: fill bible/style.yaml and bible/characters/ (copy _character.yaml).")
    return 0


def cmd_series_check(args) -> int:
    from studio.legal.licenses import all_entries, load_catalogue
    from studio.series.bible import load_bible, validate_bible

    bible = load_bible(args.slug)
    issues = validate_bible(bible, all_entries(load_catalogue()))
    errors = [i for i in issues if i.level == "error"]
    summary = {"characters": len(bible.characters), "locations": len(bible.locations), "languages": bible.languages}
    _out(args, {"summary": summary, "issues": [i.as_dict() for i in issues], "ok": not errors}, f"Series '{args.slug}': {summary}\n{_issues_text(issues)}")
    return 0 if not errors else 1


def cmd_episode_new(args) -> int:
    from studio.series.episode import create_episode

    info = create_episode(args.slug, args.number, args.title, with_project=not args.no_project)
    _out(args, info, f"Created episode E{args.number:02d} '{args.title}'" + (f" with project {info.get('project_id')}" if info.get("project_id") else ""))
    return 0


def cmd_shots_check(args) -> int:
    from studio.series.shotlist import summarize, validate_shotlist

    bible, episode, folder, shotlist, project = _episode(args.slug, args.number)
    if "animation_policy" not in bible.series:
        bible.series["animation_policy"] = {"max_full_video_ratio": (_config().get("animation") or {}).get("max_full_video_ratio")}
    issues = validate_shotlist(shotlist, bible)
    errors = [i for i in issues if i.level == "error"]
    report = {"summary": summarize(shotlist), "issues": [i.as_dict() for i in issues], "ok": not errors, "checked": today_iso()}
    if project:
        dump_json(report, project / "20_qc" / "shotlist_check.json")
    s = report["summary"]
    text = (
        f"E{args.number:02d}: {s['shots']} shots, {s['runtime_min']} min, full AI video {s['full_video_ratio']:.0%}\n"
        f"  by motion: " + ", ".join(f"{k} {v['shots']}" for k, v in s["by_motion"].items()) + f"\n{_issues_text(issues)}"
    )
    _out(args, report, text)
    return 0 if not errors else 1


def cmd_estimate(args) -> int:
    from studio.budget.estimate import estimate_episode, estimate_season_setup

    config = _config()
    bible, episode, folder, shotlist, project = _episode(args.slug, args.number)
    result = estimate_episode(shotlist, config, languages=bible.languages, gpu=args.gpu)
    result["season_setup_one_time"] = estimate_season_setup(len(bible.characters), config, args.gpu)
    if project:
        dump_json(result, project / "00_admin" / "budget" / "estimate.json")
    stages = "\n".join(f"    {k:22} {v:6.2f} h" for k, v in result["stages_gpu_hours"].items())
    verdict = "WITHIN CAP" if result["within_cap"] else "OVER CAP - simplify motion or raise the cap deliberately"
    text = (
        f"Estimate E{args.number:02d} on {result['gpu']} (₹{result['rate_ex_gst_per_hour']}/h ex-GST)\n{stages}\n"
        f"  GPU hours {result['gpu_hours']}  ->  ₹{result['cost_inc_gst']} incl. GST, ₹{result['cost_with_margin']} with margin, cap ₹{result['cap']:.0f}: {verdict}\n"
        f"  one-time season LoRA setup ({result['season_setup_one_time']['characters']} characters): ₹{result['season_setup_one_time']['inc_gst']}\n"
        f"  note: {result['assumptions']}"
    )
    _out(args, result, text)
    return 0 if result["within_cap"] in (True, None) else 1


def cmd_legal_check(args) -> int:
    from studio.legal.licenses import all_entries, check_entry, load_catalogue

    entries = all_entries(load_catalogue())
    keys = args.keys or sorted(entries)
    results = [check_entry(k, entries.get(k)).as_dict() for k in keys]
    width = max(len(r["key"]) for r in results)
    text = "\n".join(f"  {'CLEARED' if r['cleared'] else 'BLOCKED':8} {r['key']:{width}}  {r['reason']}" for r in results)
    _out(args, results, text)
    return 0


def _set_license_fields(key: str, updates: Dict[str, str]) -> None:
    """Edit fields inside one entry's license block, keeping comments intact."""
    from studio.legal.licenses import REGISTRY_PATH

    lines = REGISTRY_PATH.read_text(encoding="utf-8").splitlines()
    start = next((i for i, line in enumerate(lines) if re.match(rf"^  {re.escape(key)}:\s*$", line)), None)
    if start is None:
        raise StudioError(f"'{key}' not found in registry.yaml")
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^  \S", lines[i]) or re.match(r"^\S", lines[i])), len(lines))
    lic = next((i for i in range(start, end) if re.match(r"^    license:\s*$", lines[i])), None)
    if lic is None:
        raise StudioError(f"'{key}' has no license block")
    for field, value in updates.items():
        idx = next((i for i in range(lic + 1, end) if re.match(rf"^      {field}:", lines[i])), None)
        rendered = f'      {field}: {value}'
        if idx is None:
            lines.insert(lic + 1, rendered)
            end += 1
        else:
            lines[idx] = rendered
    REGISTRY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_legal_verify(args) -> int:
    updates = {"commercial_use": args.commercial_use, "verified": "true", "verified_on": today_iso(), "source": args.source}
    if args.conditions:
        updates["conditions"] = json.dumps(args.conditions)
    _set_license_fields(args.key, updates)
    from studio.legal.licenses import all_entries, check_entry, load_catalogue

    result = check_entry(args.key, all_entries(load_catalogue()).get(args.key)).as_dict()
    _out(args, result, f"Recorded verification for {args.key}: {result['reason']}")
    return 0


def cmd_legal_acknowledge(args) -> int:
    _set_license_fields(args.key, {"conditions_acknowledged": "true"})
    from studio.legal.licenses import all_entries, check_entry, load_catalogue

    result = check_entry(args.key, all_entries(load_catalogue()).get(args.key)).as_dict()
    _out(args, result, f"{args.key}: {result['reason']}")
    return 0


def cmd_legal_scan(args) -> int:
    from studio.legal.content import scan_episode

    bible, episode, folder, shotlist, project = _episode(args.slug, args.number)
    script = (folder / "script.md").read_text(encoding="utf-8") if (folder / "script.md").is_file() else ""
    report = scan_episode(script, shotlist)
    if project:
        dump_json(report, project / "19_legal-rights" / "content_scan.json")
    lines = [f"  [{h['severity'].upper():6}] {h['where']}: '{h['term']}' ({h['category']})" for h in report["hits"]]
    _out(args, report, f"Content scan E{args.number:02d}: {report['blocking']} blocking, {report['review']} to review\n" + ("\n".join(lines) or "  clean"))
    return 0 if report["passed"] else 1


def cmd_legal_release_gate(args) -> int:
    from studio.legal.provenance import SIDECAR_SUFFIX, release_gate

    bible, episode, folder, shotlist, project = _episode(args.slug, args.number)
    project = _require_project(project)
    roots = [Path(a) for a in args.assets] if args.assets else [project / "09_ai-generation" / "selected", project / "10_animation" / "clips", project / "14_sound" / "dialogue", project / "15_music" / "cues", project / "13_vfx-motion" / "titles"]
    assets = []
    for root in roots:
        if root.is_file():
            assets.append(root)
        elif root.is_dir():
            assets += [p for p in root.rglob("*") if p.is_file() and not p.name.endswith(SIDECAR_SUFFIX) and not p.name.startswith(".")]
    report = release_gate(assets, bible=bible)
    config = _config()
    report["declare_synthetic_content"] = bool((config.get("legal") or {}).get("declare_synthetic_content", True))
    report["upload_checklist"] = [
        "Tick YouTube's altered/synthetic content disclosure (and India IT Rules 2026 SGI declaration where asked)",
        "Description credits: AI tools used, music source, fonts",
        "Owner has watched the full master in every language",
    ]
    dump_json(report, project / "19_legal-rights" / "release_gate.json")
    lines = [f"  - {relpath(Path(p['asset']))}: {p['problem']}" for p in report["problems"][:40]]
    _out(args, report, f"Release gate: {'PASSED' if report['passed'] else 'BLOCKED'} ({report['checked']} assets checked)\n" + "\n".join(lines))
    return 0 if report["passed"] else 1


def cmd_voice(args) -> int:
    from integrations.tts import adapter as tts
    from studio.series.shotlist import dialogue_lines

    config = _config()
    bible, episode, folder, shotlist, project = _episode(args.slug, args.number)
    project = _require_project(project)
    languages = [args.language] if args.language else bible.languages
    lines = [line for lang in languages for line in dialogue_lines(shotlist, lang)]
    planned = tts.plan(bible, lines, project)
    if not args.execute:
        todo = [p for p in planned if not p["exists"]]
        _out(args, planned, f"{len(planned)} lines ({len(todo)} to generate). Engines: {sorted({p['engine'] for p in planned})}\nRe-run with --execute to generate through the quality loop.")
        return 0

    from integrations.stt.whisper import transcriber
    from studio.budget.ledger import Ledger
    from studio.feedback.loop import QualityLoop

    loop = QualityLoop(project, config, Ledger(project, config))
    transcribe = transcriber(config)
    results = []
    for line in lines:
        out = tts.line_path(project, line)
        if out.is_file() and not args.force:
            continue
        voice = tts.voice_for(bible, line["character"], line["language"])

        def generate(params, attempt, line=line, voice=voice, out=out):
            return tts.synthesize_line(line, voice, out, config, params)

        ctx = {"expected_text": line["text"], "language": line["language"], "transcribe": transcribe, "bible": bible, "shot": {"id": line["shot_id"]}}
        verdict = loop.run("voice_line", generate, ctx, params={"speed": voice.get("speed", 1.0)})
        results.append({"line_id": line["line_id"], "decision": verdict.decision, "attempt": verdict.attempt, "reasons": verdict.reasons})
    approved = sum(1 for r in results if r["decision"] == "approve")
    _out(args, results, f"Voice: {approved}/{len(results)} approved automatically; the rest are in 20_qc/feedback/review_queue.json")
    return 0


def cmd_timing(args) -> int:
    from integrations.tts import adapter as tts
    from studio.feedback.media import probe
    from studio.orchestrator.anime import dialogue_timeline, retime_shots

    bible, episode, folder, shotlist, project = _episode(args.slug, args.number)
    project = _require_project(project)
    language = args.language or bible.languages[0]
    from studio.series.shotlist import dialogue_lines

    durations, missing = {}, []
    for line in dialogue_lines(shotlist, language):
        path = tts.line_path(project, line)
        if path.is_file():
            durations[line["line_id"]] = float(probe(path)["duration_s"] or 0)
        else:
            missing.append(line["line_id"])
    timeline = dialogue_timeline(shotlist, language, durations)
    changes = retime_shots(shotlist, timeline)
    result = {"language": language, "lines": len(timeline), "missing_audio": missing, "lengthen_shots": changes}
    if args.apply and changes:
        for scene in shotlist["scenes"]:
            for shot in scene["shots"]:
                if shot["id"] in changes:
                    shot["duration_s"] = changes[shot["id"]]
        dump_json(shotlist, folder / "shotlist.json")
        timeline = dialogue_timeline(shotlist, language, durations)
        result["applied"] = True
    dump_json({"language": language, "timeline": timeline}, project / "12_edit" / "timeline.json")
    _out(args, result, f"Timing ({language}): {len(timeline)} lines placed, {len(missing)} missing audio, {len(changes)} shots need lengthening" + (" (applied)" if result.get("applied") else " (use --apply)"))
    return 0


def cmd_budget(args) -> int:
    from studio.budget.ledger import Ledger

    config = _config()
    _, _, _, _, project = _episode(args.slug, args.number)
    ledger = Ledger(_require_project(project), config)
    if args.action == "report":
        data = ledger.report()
        _out(args, data, f"Spent ₹{data['spent_inc_gst']} of ₹{data['cap']:.0f} (remaining ₹{data['remaining']}); {data['sessions']} GPU sessions, {data['jobs']} jobs")
    elif args.action == "log":
        if args.amount is None or not args.note:
            raise StudioError("budget log needs --amount and --note")
        data = ledger.log_manual(args.amount, args.note)
        _out(args, data, f"Logged ₹{args.amount}: {args.note}")
    elif args.action == "calibrate":
        data = ledger.calibrate()
        _out(args, data, "Measured medians (copy into budget.benchmarks_gpu_s):\n" + json.dumps(data, indent=2))
    return 0


def cmd_compute(args) -> int:
    from studio.compute import gridshare
    from studio.budget.ledger import Ledger

    config = _config()
    if args.action == "tunnel":
        remote = gridshare.Remote.from_env()
        process = remote.open_tunnel(args.port, args.port)
        print(f"Tunnel open: http://127.0.0.1:{args.port} -> GridShare ComfyUI. Ctrl+C to close.")
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
        return 0
    _, _, _, _, project = _episode(args.slug, args.number)
    project = _require_project(project)
    if args.action == "start":
        gpu = args.gpu or os.environ.get("GRIDSHARE_GPU") or (config.get("budget") or {}).get("default_gpu")
        data = gridshare.session_start(project, gpu, args.note or "")
        _out(args, data, f"GPU session started on {gpu}. Stop it (and the instance!) with: python -m studio compute stop {args.slug} {args.number}")
    elif args.action == "stop":
        data = gridshare.session_stop(project, Ledger(project, config))
        _out(args, data, f"Session logged: {data['seconds'] / 3600:.2f} h on {data['gpu']} = ₹{data['cost_inc_gst']} incl. GST. Remember to stop the instance on gridshare.in.")
    elif args.action == "status":
        data = gridshare.session_status(project)
        text = "No open GPU session." if not data["open"] else f"Open session on {data['gpu']} for {data['hours']} h" + ("  << WARNING: still running?" if data["warning"] else "")
        _out(args, data, text)
    return 0


def _qc_context(config, bible, kind, shot_id, shotlist, language):
    from integrations.identity.ccip import scorer
    from integrations.stt.whisper import transcriber
    from studio.series.shotlist import iter_shots

    shot = next((s for s in iter_shots(shotlist) if s["id"] == shot_id), None) if shot_id else None
    characters = [c["id"] if isinstance(c, dict) else c for c in (shot or {}).get("characters") or []]
    palette = []
    for cid in characters:
        palette += list(((bible.characters.get(cid) or {}).get("palette") or {}).values())
    return {
        "config": config,
        "bible": bible,
        "shot": shot,
        "characters": characters,
        "palette": palette,
        "language": language,
        "transcribe": transcriber(config),
        "identity_scorer": scorer(),
    }


def cmd_qc(args) -> int:
    from studio.feedback import review
    from studio.feedback.loop import QualityLoop

    config = _config()
    bible, episode, folder, shotlist, project = _episode(args.slug, args.number)
    project = _require_project(project)
    if args.action == "run":
        if not args.asset or not args.kind:
            raise StudioError("qc run needs --asset and --kind")
        ctx = _qc_context(config, bible, args.kind, args.shot, shotlist, args.language or bible.languages[0])
        if args.expected_text:
            ctx["expected_text"] = args.expected_text
        verdict = QualityLoop(project, config).evaluate(Path(args.asset), args.kind, ctx)
        rows = "\n".join(f"  {r.status.upper():5} {r.name:18} {r.detail}" for r in verdict.results)
        _out(args, verdict.as_dict(), f"{verdict.decision.upper()}: {'; '.join(verdict.reasons)}\n{rows}")
        return 0 if verdict.decision == "approve" else 1
    if args.action == "report":
        data = review.episode_report(project)
        _out(args, data, json.dumps(data, indent=2))
    elif args.action == "rate":
        if not args.asset or args.score is None:
            raise StudioError("qc rate needs --asset and --score 1-5")
        data = review.rate(project, args.asset, args.score, args.note or "")
        _out(args, data, f"Rated {args.asset}: {args.score}/5")
    elif args.action == "calibrate":
        data = review.calibrate_thresholds(project)
        _out(args, data, "Threshold suggestions (from your ratings):\n" + json.dumps(data, indent=2))
    elif args.action == "queue":
        path = project / "20_qc" / "feedback" / "review_queue.json"
        queue = [q for q in (load_json(path) if path.is_file() else []) if q.get("status") == "open"]
        text = "\n".join(f"  {q['decision']:12} {q.get('shot_id') or '-':12} {q['kind']:10} {'; '.join(q['reasons'])[:120]}" for q in queue) or "  review queue is empty"
        _out(args, queue, f"Open review items: {len(queue)}\n{text}")
    return 0


def cmd_lessons(args) -> int:
    from studio.feedback.review import add_lesson

    _, _, _, _, project = _episode(args.slug, args.number)
    path = add_lesson(_require_project(project), args.lesson, args.area, args.action or "")
    _out(args, {"file": relpath(path)}, f"Lesson recorded in {relpath(path)}")
    return 0


def cmd_pipeline(args) -> int:
    from studio.orchestrator.anime import STAGES, next_stage, status

    if args.action == "plan" or not args.slug:
        rows = [{"n": i, "stage": s.key, "title": s.title, "skill": s.skill, "runs_on": s.runs_on, "automation": s.automation, "command": s.command} for i, s in enumerate(STAGES, 1)]
        text = "\n".join(f"  {r['n']:2}. [{r['automation']:6}] {r['title']:58} skill={r['skill']:18} on={r['runs_on']}" for r in rows)
        _out(args, rows, f"Anime episode pipeline\n{text}")
        return 0
    from studio.series.episode import episode_dir, load_episode, project_root

    episode = load_episode(args.slug, args.number)
    rows = status(episode_dir(args.slug, args.number), project_root(episode))
    nxt = next_stage(rows)
    text = "\n".join(f"  {'[x]' if r['done'] else '[ ]'} {r['n']:2}. {r['title']}" for r in rows)
    if nxt:
        text += f"\n\nNext: {nxt['title']}\n  skill: {nxt['skill']}   how: {nxt['command']}"
    _out(args, {"stages": rows, "next": nxt}, text)
    return 0


# ----------------------------------------------------------------- parser
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m studio", description="AI Film Studio command line")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="check tools and configuration").set_defaults(func=cmd_doctor)

    series = sub.add_parser("series", help="create or check a series").add_subparsers(dest="action", required=True)
    p = series.add_parser("new")
    p.add_argument("slug")
    p.add_argument("--title", required=True)
    p.add_argument("--languages", default="en,hi")
    p.set_defaults(func=cmd_series_new)
    p = series.add_parser("check")
    p.add_argument("slug")
    p.set_defaults(func=cmd_series_check)

    episode = sub.add_parser("episode", help="create an episode").add_subparsers(dest="action", required=True)
    p = episode.add_parser("new")
    p.add_argument("slug")
    p.add_argument("number", type=int)
    p.add_argument("--title", required=True)
    p.add_argument("--no-project", action="store_true", help="canon files only, no engine project")
    p.set_defaults(func=cmd_episode_new)

    def ep(name, func, help_text):
        q = sub.add_parser(name, help=help_text)
        q.add_argument("slug")
        q.add_argument("number", type=int)
        q.set_defaults(func=func)
        return q

    shots = sub.add_parser("shots", help="validate the shot list").add_subparsers(dest="action", required=True)
    p = shots.add_parser("check")
    p.add_argument("slug")
    p.add_argument("number", type=int)
    p.set_defaults(func=cmd_shots_check)

    ep("estimate", cmd_estimate, "GPU cost estimate vs budget cap").add_argument("--gpu")

    legal = sub.add_parser("legal", help="licenses, content scan, release gate").add_subparsers(dest="action", required=True)
    p = legal.add_parser("check", help="license clearance for registry entries")
    p.add_argument("keys", nargs="*")
    p.set_defaults(func=cmd_legal_check)
    p = legal.add_parser("verify", help="record that you read a license")
    p.add_argument("key")
    p.add_argument("--source", required=True)
    p.add_argument("--commercial-use", required=True, choices=["allowed", "conditional", "prohibited", "unknown"])
    p.add_argument("--conditions")
    p.set_defaults(func=cmd_legal_verify)
    p = legal.add_parser("acknowledge", help="accept a conditional license's conditions")
    p.add_argument("key")
    p.set_defaults(func=cmd_legal_acknowledge)
    p = legal.add_parser("scan")
    p.add_argument("slug")
    p.add_argument("number", type=int)
    p.set_defaults(func=cmd_legal_scan)
    p = legal.add_parser("release-gate")
    p.add_argument("slug")
    p.add_argument("number", type=int)
    p.add_argument("--assets", nargs="*")
    p.set_defaults(func=cmd_legal_release_gate)

    p = ep("voice", cmd_voice, "plan or generate all dialogue")
    p.add_argument("--language")
    p.add_argument("--execute", action="store_true")
    p.add_argument("--force", action="store_true")

    p = ep("timing", cmd_timing, "fit shot durations to recorded dialogue")
    p.add_argument("--language")
    p.add_argument("--apply", action="store_true")

    p = ep("budget", cmd_budget, "episode spending")
    p.add_argument("action", choices=["report", "log", "calibrate"])
    p.add_argument("--amount", type=float)
    p.add_argument("--note")

    p = sub.add_parser("compute", help="GridShare GPU sessions and tunnel")
    p.add_argument("action", choices=["start", "stop", "status", "tunnel"])
    p.add_argument("slug", nargs="?")
    p.add_argument("number", type=int, nargs="?")
    p.add_argument("--gpu")
    p.add_argument("--note")
    p.add_argument("--port", type=int, default=8188)
    p.set_defaults(func=cmd_compute)

    p = ep("qc", cmd_qc, "quality checks, ratings and calibration")
    p.add_argument("action", choices=["run", "report", "rate", "calibrate", "queue"])
    p.add_argument("--asset")
    p.add_argument("--kind", choices=["keyframe", "video", "voice_line", "music", "master"])
    p.add_argument("--shot")
    p.add_argument("--language")
    p.add_argument("--expected-text")
    p.add_argument("--score", type=int)
    p.add_argument("--note")

    p = ep("lessons", cmd_lessons, "record a lesson learned")
    p.add_argument("--area", required=True)
    p.add_argument("--lesson", required=True)
    p.add_argument("--action")

    p = sub.add_parser("pipeline", help="episode pipeline plan or status")
    p.add_argument("action", choices=["plan", "status"])
    p.add_argument("slug", nargs="?")
    p.add_argument("number", type=int, nargs="?")
    p.set_defaults(func=cmd_pipeline)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "command", None) == "compute" and args.action != "tunnel" and (args.slug is None or args.number is None):
        parser.error("compute start/stop/status need <series> <episode>")
    try:
        return int(args.func(args) or 0)
    except StudioError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
