#!/usr/bin/env python3
"""
Modular studio pipeline — orchestration skeleton.

This is NOT a video generator. It:

1. loads a workflow JSON (same format as scripts/workflows/*.json),
2. validates it against the engine's rules,
3. creates the project directory,
4. creates the standard subdirectories,
5. prints the pipeline stages and which integrations each would use,
6. dispatches each stage to adapters — which are placeholders for now.

Workflow *steps* are still executed by the existing engine:

    python scripts/create_project.py workflow-run <ID> <slug> --workflow <file> [--execute]

Usage:

    python studio/orchestrator/pipeline.py \\
        --workflow scripts/workflows/production_pipeline.json \\
        --slug my-first-film

Only the standard library is required.
"""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

if __package__ in (None, ""):
    # Allow `python studio/orchestrator/pipeline.py` as well as `-m`.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "studio.orchestrator"

from studio.orchestrator.config import (  # noqa: E402
    REPO_ROOT,
    ConfigError,
    effective_integrations,
    load_config,
    load_registry,
)
from studio.orchestrator import project as project_mod  # noqa: E402


# ------------------------------------------------------------
# Stages
# ------------------------------------------------------------

@dataclass(frozen=True)
class Stage:
    key: str
    title: str
    integrations: Sequence[str] = ()
    module: Optional[str] = None  # studio package that will own this stage


STAGES: List[Stage] = [
    Stage("input", "Input"),
    Stage("workflow", "Workflow", module="orchestrator"),
    Stage("project", "Project creation", module="orchestrator"),
    Stage("asset_acquisition", "Asset acquisition",
          ("stock", "maps", "vectors", "blender", "comfyui"),
          module="integrations"),
    Stage("asset_processing", "Asset processing", ("post_realesrgan", "post_rife"), module="integrations"),
    Stage("audio", "Audio",
          ("tts_kokoro", "tts_indic_parler", "stt_faster_whisper", "music_ace_step"),
          module="integrations"),
    Stage("animation", "Animation", ("lipsync_rhubarb", "motion_remotion"), module="integrations"),
    Stage("rendering", "Rendering", ("edit_ffmpeg",), module="integrations.edit"),
    Stage("qc", "QC", ("identity_ccip",), module="studio.feedback"),
    Stage("final_output", "Final output", ("edit_ffmpeg",), module="integrations.edit"),
]
# The anime episode pipeline (with legal, budget and feedback gates)
# lives in studio/orchestrator/anime.py: python -m studio pipeline plan


# ------------------------------------------------------------
# Workflow loading / validation
# ------------------------------------------------------------

_ENGINE_TOKENS = {"PROJECT_ROOT", "REPO_ROOT", "PROJECT_ID", "PROJECT_TITLE",
                  "PROJECT_SLUG", "DATE", "NOW"}
_TOKEN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


@dataclass
class ValidationReport:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_workflow(path: Path) -> Dict[str, Any]:
    path = Path(path)
    if not path.is_absolute():
        path = (Path.cwd() / path) if (Path.cwd() / path).exists() else REPO_ROOT / path
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _supported_step_types() -> set:
    engine = project_mod._ENGINE
    if engine is not None:
        return set(engine.WORKFLOW_STEP_TYPES)
    return {"mkdir", "write_text", "copy", "move", "checksum", "manifest",
            "http", "python", "command", "shell", "sleep"}


def _tokens(value: Any) -> set:
    return set(_TOKEN.findall(json.dumps(value)))


def validate_workflow(workflow: Any) -> ValidationReport:
    """Same hard rules as the engine, plus advisory checks."""
    report = ValidationReport()

    if not isinstance(workflow, dict):
        report.errors.append("Workflow must be a JSON object.")
        return report
    for key in ("id", "name"):
        if not workflow.get(key):
            report.warnings.append(f"Workflow has no {key!r}.")
    steps = workflow.get("steps")
    if not isinstance(steps, list) or not steps:
        report.errors.append("Workflow must contain a non-empty 'steps' list.")
        return report

    supported = _supported_step_types()
    names: set = set()
    for i, step in enumerate(steps, 1):
        label = f"step {i}"
        if not isinstance(step, dict):
            report.errors.append(f"{label} is not an object.")
            continue
        name = step.get("name")
        label = f"step {i} ({name or 'unnamed'})"
        if not name:
            report.warnings.append(f"{label} has no name.")
        elif name in names:
            report.errors.append(f"Duplicate step name {name!r}.")
        names.add(name)

        stype = step.get("type")
        if stype not in supported:
            report.errors.append(f"{label}: unsupported step type {stype!r}.")
        if stype == "command" and not isinstance(step.get("args"), list):
            report.errors.append(f"{label}: 'command' steps need an 'args' list.")
        if stype == "mkdir" and not step.get("path"):
            report.errors.append(f"{label}: 'mkdir' steps need a 'path'.")

        # Advisory: referenced repo scripts that do not exist yet.
        for arg in step.get("args") or []:
            if isinstance(arg, str) and arg.startswith("{{REPO_ROOT}}/"):
                target = REPO_ROOT / arg[len("{{REPO_ROOT}}/"):]
                if not target.exists():
                    report.warnings.append(f"{label}: references missing file {target.relative_to(REPO_ROOT)}")

    known = _ENGINE_TOKENS | set((workflow.get("variables") or {}).keys())
    unknown = _tokens(workflow) - known
    if unknown:
        report.warnings.append(
            "Placeholders not provided by the engine or 'variables' "
            f"(must come from the environment): {', '.join(sorted(unknown))}"
        )
    return report


# ------------------------------------------------------------
# Adapter dispatch (placeholder)
# ------------------------------------------------------------
#
# Adapter contract (to be implemented per integration):
#
#   integrations/<type>/adapter.py
#       def run(stage: str, context: dict) -> dict: ...
#
# and set `adapter: integrations.<type>.adapter` in registry.yaml.

def call_adapter(integration: Dict[str, Any], stage: Stage,
                 context: Dict[str, Any], dry_run: bool) -> Dict[str, Any]:
    if not integration["active"]:
        return {"status": "skipped", "reason": integration["status"]}
    if dry_run:
        return {"status": "planned", "adapter": integration["adapter"]}

    module = importlib.import_module(integration["adapter"])
    run = getattr(module, "run", None)
    if run is None:
        raise NotImplementedError(f"{integration['adapter']} has no run(stage, context)")
    return run(stage.key, context)


def run_stages(integrations: Dict[str, Dict[str, Any]],
               context: Dict[str, Any], dry_run: bool) -> None:
    print("\nPipeline stages")
    print("-" * 60)
    for n, stage in enumerate(STAGES, 1):
        owner = f"  [{stage.module if '.' in stage.module or stage.module == 'integrations' else 'studio/' + stage.module}]" if stage.module else ""
        print(f"{n:>2}. {stage.title}{owner}")
        for key in stage.integrations:
            entry = integrations.get(key)
            if entry is None:
                print(f"      - {key}: not in registry")
                continue
            result = call_adapter(entry, stage, context, dry_run)
            detail = result.get("reason") or result.get("adapter") or ""
            print(f"      - {key}: {result['status']}" + (f" ({detail})" if detail else ""))
        if n < len(STAGES):
            print("      ↓")


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Modular studio pipeline skeleton.")
    p.add_argument("--workflow", required=True, help="Path to a workflow JSON file.")
    p.add_argument("--slug", help="Project slug (default: derived from the workflow name).")
    p.add_argument("--project-id", help="Project ID (default: projects.default_project_id).")
    p.add_argument("--complexity", choices=["SMALL", "STANDARD", "FULL"])
    p.add_argument("--config", help="Alternative config.yaml.")
    p.add_argument("--registry", help="Alternative registry.yaml.")
    p.add_argument("--plan-only", action="store_true",
                   help="Validate and print, but do not create directories.")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        config = load_config(Path(args.config) if args.config else None)
        registry = load_registry(Path(args.registry) if args.registry else None)
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return 2

    # 1. Load
    try:
        workflow = load_workflow(Path(args.workflow))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not load workflow: {exc}", file=sys.stderr)
        return 2
    print(f"Workflow : {workflow.get('name', '?')} ({workflow.get('id', '?')}, {workflow.get('version', '?')})")
    print(f"Risk     : {workflow.get('risk_level', '?')}   approval required: {workflow.get('approval_required', '?')}")

    # 2. Validate
    report = validate_workflow(workflow)
    for w in report.warnings:
        print(f"  warning: {w}")
    for e in report.errors:
        print(f"  error:   {e}", file=sys.stderr)
    if not report.ok:
        print("Workflow is invalid; stopping.", file=sys.stderr)
        return 1
    print(f"Valid    : {len(workflow['steps'])} steps")

    # 3 + 4. Project directory and standard subdirectories
    slug = args.slug or project_mod.slugify(workflow.get("name", "untitled"))
    try:
        proj = project_mod.create_project(
            config, slug=slug, project_id=args.project_id,
            complexity=args.complexity, dry_run=args.plan_only,
        )
    except ValueError as exc:
        print(f"Project error: {exc}", file=sys.stderr)
        return 2
    verb = "Would create" if args.plan_only else "Created"
    print(f"\nProject  : {proj.root.relative_to(REPO_ROOT)}  ({proj.complexity})")
    print(f"{verb} {len(proj.created)} directories"
          + (" (project already complete)" if not proj.created else ""))

    # 5 + 6. Stages and adapter dispatch
    processing = config["processing"]
    print(f"\nProcessing: preference={processing.get('preference')} "
          f"allow_external={processing.get('allow_external')} dry_run={processing.get('dry_run')}")
    render = config["render"]
    print(f"Render    : {render.get('resolution')} @ {render.get('fps')} fps "
          f"(preview {render.get('preview_resolution')})")

    context = {"workflow": workflow, "project": proj, "config": config}
    run_stages(effective_integrations(config, registry), context,
               dry_run=bool(processing.get("dry_run", True)))

    print("\nWorkflow steps (executed by the engine, not by this skeleton):")
    for i, step in enumerate(workflow["steps"], 1):
        print(f"  {i:>2}. {step.get('name')}  [{step.get('type')}]")
    print("\nTo run them on an engine-tracked project (made with `create_project.py init`):")
    print(f"  python scripts/create_project.py workflow-run <PROJECT_ID> <slug> --workflow {args.workflow}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
