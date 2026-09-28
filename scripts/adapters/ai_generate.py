#!/usr/bin/env python3
"""
AI FILM STUDIO - AI GENERATION ADAPTER

This adapter is the bridge between the Studio Automation Engine
and an actual AI image/video generation system.

It does NOT assume that ComfyUI, Kling, or any other provider
is installed or connected.

Supported execution modes
-------------------------
1. External generator command
2. Environment-configured generator command
3. Request-only mode for creating a generation request
4. Optional HTTP JSON API mode

The adapter:
- validates project / shot / prompt / model information
- creates a generation request
- creates a reproducible job record
- optionally executes an external generator
- captures stdout/stderr
- verifies output existence
- records generation metadata
- calculates checksums for output files
- creates a generation manifest
- never deletes source/reference files

Environment variables
---------------------
STUDIO_AI_GENERATOR_COMMAND

Example:

STUDIO_AI_GENERATOR_COMMAND=
python C:/AI/ComfyUI/studio_generate.py
--request "{request}"
--output "{output}"

The following placeholders are available:

{project_id}
{project_root}
{project_slug}
{shot_id}
{prompt_id}
{model_id}
{output}
{request}
{request_json}

Optional generic HTTP API:

STUDIO_AI_GENERATOR_URL

Optional authentication header:

STUDIO_AI_GENERATOR_TOKEN

Examples
--------
Request-only mode:

    python scripts/adapters/ai_generate.py \
        --project-id PROJECT_2026_001 \
        --project-slug my-film \
        --shot-id SHOT_001 \
        --prompt-id PROMPT_001 \
        --model-id MODEL_001 \
        --output "09_ai-generation/selected/SHOT_001_v001"

Execute configured generator:

    python scripts/adapters/ai_generate.py \
        --project-id PROJECT_2026_001 \
        --project-slug my-film \
        --shot-id SHOT_001 \
        --prompt-id PROMPT_001 \
        --model-id MODEL_001 \
        --output "09_ai-generation/selected/SHOT_001_v001" \
        --execute

Use explicit command:

    python scripts/adapters/ai_generate.py \
        ... \
        --command "python generator.py --request {request} --output {output}"

Important
---------
This adapter is intentionally provider-neutral.

A provider-specific adapter such as:

scripts/adapters/comfyui.py

or:

scripts/adapters/kling.py

can later implement provider-specific behavior while this
adapter remains the stable Studio interface.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


# ============================================================
# CONSTANTS
# ============================================================

ADAPTER_NAME = "AI Generation Adapter"
ADAPTER_VERSION = "1.0.0"

MAX_OUTPUT_FILES_IN_REPORT = 500

MEDIA_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
    ".exr",
    ".dpx",
    ".mp4",
    ".mov",
    ".webm",
    ".mkv",
    ".avi",
    ".wav",
    ".aiff",
    ".aif",
    ".flac",
    ".mp3",
}

IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".studio",
    "cache",
    "temp",
    "tmp",
    "preview",
    "previews",
}


# ============================================================
# UTILITIES
# ============================================================

def now_iso() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).astimezone().isoformat(
        timespec="seconds"
    )


def file_sha256(
    path: Path,
    chunk_size: int = 1024 * 1024,
) -> str:

    digest = hashlib.sha256()

    with path.open("rb") as handle:

        while True:

            chunk = handle.read(
                chunk_size
            )

            if not chunk:
                break

            digest.update(
                chunk
            )

    return digest.hexdigest()


def safe_json_dump(
    value: Any,
    path: Path,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp = path.with_suffix(
        path.suffix + ".tmp"
    )

    temp.write_text(
        json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    temp.replace(
        path
    )


def resolve_relative_path(
    root: Path,
    value: str,
) -> Path:

    path = Path(
        value
    )

    if not path.is_absolute():
        path = root / path

    resolved = path.resolve()
    root_resolved = root.resolve()

    if (
        resolved != root_resolved
        and root_resolved
        not in resolved.parents
    ):
        raise ValueError(
            f"Path escapes project root: {value}"
        )

    return resolved


def load_json(
    path: Path,
) -> Any:

    if not path.exists():
        raise FileNotFoundError(
            f"JSON file not found: {path}"
        )

    try:

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Invalid JSON file {path}: {exc}"
        ) from exc


def find_record(
    records: Iterable[Dict[str, Any]],
    record_id: str,
) -> Dict[str, Any]:

    for record in records:

        if record.get("id") == record_id:
            return record

    raise KeyError(
        f"Record not found: {record_id}"
    )


# ============================================================
# STUDIO STATE
# ============================================================

def find_project_root(
    project_id: str,
    project_slug: str,
) -> Path:

    repo_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    root = (
        repo_root
        / "projects"
        / project_id
        / project_slug
    ).resolve()

    if (
        not root.exists()
        or not root.is_dir()
    ):
        raise FileNotFoundError(
            f"Project does not exist: {root}"
        )

    return root


def state_path(
    project_root: Path,
) -> Path:

    return (
        project_root
        / "00_admin"
        / ".studio"
        / "state.json"
    )


def load_state(
    project_root: Path,
) -> Dict[str, Any]:

    data = load_json(
        state_path(
            project_root
        )
    )

    if not isinstance(
        data,
        dict,
    ):
        raise ValueError(
            "Studio state must be a JSON object."
        )

    return data


def save_state(
    project_root: Path,
    state: Dict[str, Any],
) -> None:

    state.setdefault(
        "metadata",
        {}
    )

    state["metadata"][
        "updated"
    ] = now_iso()

    safe_json_dump(
        state,
        state_path(
            project_root
        ),
    )


def append_event(
    project_root: Path,
    event: str,
    entity: Optional[str],
    details: Dict[str, Any],
) -> None:

    event_dir = (
        project_root
        / "00_admin"
        / ".studio"
    )

    event_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    event_path = (
        event_dir
        / "events.jsonl"
    )

    record = {
        "timestamp":
            now_iso(),
        "event":
            event,
        "entity":
            entity,
        "details":
            details,
    }

    with event_path.open(
        "a",
        encoding="utf-8",
    ) as handle:

        handle.write(
            json.dumps(
                record,
                ensure_ascii=False,
            )
            + "\n"
        )


# ============================================================
# ID GENERATION
# ============================================================

def next_id(
    records: List[Dict[str, Any]],
    prefix: str,
) -> str:

    maximum = 0

    for record in records:

        value = str(
            record.get(
                "id",
                ""
            )
        )

        if not value.startswith(
            prefix + "_"
        ):
            continue

        suffix = value[
            len(prefix) + 1:
        ]

        if suffix.isdigit():

            maximum = max(
                maximum,
                int(suffix),
            )

    return f"{prefix}_{maximum + 1:04d}"


# ============================================================
# REQUEST GENERATION
# ============================================================

def build_request(
    state: Dict[str, Any],
    shot_id: str,
    prompt_id: str,
    model_id: str,
    output: Path,
    project_root: Path,
) -> Dict[str, Any]:

    shot = find_record(
        state.get(
            "shots",
            []
        ),
        shot_id,
    )

    prompt = find_record(
        state.get(
            "prompts",
            []
        ),
        prompt_id,
    )

    model = None

    if model_id:

        try:

            model = find_record(
                state.get(
                    "models",
                    []
                ),
                model_id,
            )

        except KeyError:

            # The current state schema may not yet contain
            # a dedicated models collection.
            model = {
                "id":
                    model_id,
                "status":
                    "UNREGISTERED_REFERENCE",
            }

    request = {
        "adapter": {
            "name":
                ADAPTER_NAME,
            "version":
                ADAPTER_VERSION,
        },
        "request": {
            "request_id":
                None,
            "created":
                now_iso(),
        },
        "project": {
            "id":
                state["project"]["id"],
            "title":
                state["project"]["title"],
            "slug":
                state["project"].get(
                    "slug"
                ),
            "type":
                state["project"].get(
                    "type"
                ),
        },
        "shot": shot,
        "prompt": prompt,
        "model": model,
        "output": {
            "directory":
                str(output),
            "exists":
                output.exists(),
        },
        "requirements": {
            "preserve_source":
                True,
            "register_output":
                True,
            "checksum":
                True,
            "qc_required":
                True,
        },
    }

    return request


# ============================================================
# OUTPUT DISCOVERY
# ============================================================

def discover_outputs(
    output_dir: Path,
) -> List[Dict[str, Any]]:

    if not output_dir.exists():
        return []

    files: List[Dict[str, Any]] = []

    for path in output_dir.rglob("*"):

        if not path.is_file():
            continue

        if any(
            part in IGNORED_DIRECTORIES
            for part in path.parts
        ):
            continue

        if (
            path.suffix.lower()
            not in MEDIA_EXTENSIONS
        ):
            continue

        stat = path.stat()

        files.append(
            {
                "path":
                    str(path),
                "filename":
                    path.name,
                "extension":
                    path.suffix.lower(),
                "size":
                    stat.st_size,
                "modified":
                    dt.datetime
                    .fromtimestamp(
                        stat.st_mtime,
                        tz=dt.timezone.utc,
                    )
                    .astimezone()
                    .isoformat(
                        timespec="seconds"
                    ),
                "sha256":
                    file_sha256(
                        path
                    ),
            }
        )

        if (
            len(files)
            >= MAX_OUTPUT_FILES_IN_REPORT
        ):
            break

    files.sort(
        key=lambda item:
            item["path"]
    )

    return files


# ============================================================
# REQUEST FILE
# ============================================================

def write_request_file(
    project_root: Path,
    request: Dict[str, Any],
    request_id: str,
) -> Path:

    request_dir = (
        project_root
        / "09_ai-generation"
        / "generation-logs"
    )

    request_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    request_path = (
        request_dir
        / f"{request_id}.json"
    )

    request["request"][
        "request_id"
    ] = request_id

    safe_json_dump(
        request,
        request_path,
    )

    return request_path


# ============================================================
# COMMAND EXECUTION
# ============================================================

def build_command(
    template: str,
    *,
    project_id: str,
    project_root: Path,
    project_slug: str,
    shot_id: str,
    prompt_id: str,
    model_id: str,
    output: Path,
    request_path: Path,
) -> str:

    replacements = {
        "{project_id}":
            project_id,
        "{project_root}":
            str(project_root),
        "{project_slug}":
            project_slug,
        "{shot_id}":
            shot_id,
        "{prompt_id}":
            prompt_id,
        "{model_id}":
            model_id,
        "{output}":
            str(output),
        "{request}":
            str(request_path),
        "{request_json}":
            request_path.read_text(
                encoding="utf-8"
            ),
    }

    command = template

    for token, value in (
        replacements.items()
    ):

        command = command.replace(
            token,
            value,
        )

    return command


def execute_command(
    command: str,
    project_root: Path,
    timeout: int,
) -> Dict[str, Any]:

    started = now_iso()

    completed = subprocess.run(
        command,
        cwd=project_root,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    result = {
        "command":
            command,
        "started":
            started,
        "ended":
            now_iso(),
        "returncode":
            completed.returncode,
        "stdout":
            completed.stdout[
                -20000:
            ],
        "stderr":
            completed.stderr[
                -20000:
            ],
        "status":
            (
                "SUCCESS"
                if completed.returncode == 0
                else "FAILED"
            ),
    }

    if completed.returncode != 0:

        raise RuntimeError(
            "AI generator command failed."
        )

    return result


# ============================================================
# OPTIONAL HTTP GENERATOR
# ============================================================

def execute_http_generator(
    url: str,
    token: Optional[str],
    request: Dict[str, Any],
    timeout: int,
) -> Dict[str, Any]:

    payload = json.dumps(
        request
    ).encode(
        "utf-8"
    )

    headers = {
        "Content-Type":
            "application/json",
    }

    if token:

        headers[
            "Authorization"
        ] = f"Bearer {token}"

    http_request = (
        urllib.request.Request(
            url,
            data=payload,
            headers=headers,
            method="POST",
        )
    )

    try:

        with urllib.request.urlopen(
            http_request,
            timeout=timeout,
        ) as response:

            body = (
                response
                .read()
                .decode(
                    "utf-8",
                    errors="replace",
                )
            )

            try:
                parsed = json.loads(
                    body
                )
            except json.JSONDecodeError:
                parsed = {
                    "raw":
                        body[
                            -20000:
                        ]
                }

            return {
                "status":
                    "SUCCESS",
                "http_status":
                    response.status,
                "response":
                    parsed,
                "started":
                    now_iso(),
                "ended":
                    now_iso(),
            }

    except urllib.error.HTTPError as exc:

        body = (
            exc.read()
            .decode(
                "utf-8",
                errors="replace",
            )
        )

        raise RuntimeError(
            f"AI generation API returned HTTP "
            f"{exc.code}: {body[-2000:]}"
        ) from exc

    except urllib.error.URLError as exc:

        raise RuntimeError(
            f"AI generation API connection failed: "
            f"{exc}"
        ) from exc


# ============================================================
# GENERATION REGISTRATION
# ============================================================

def register_generation(
    project_root: Path,
    state: Dict[str, Any],
    request: Dict[str, Any],
    request_id: str,
    output_files: List[Dict[str, Any]],
    execution: Optional[Dict[str, Any]],
) -> Dict[str, Any]:

    generations = state.setdefault(
        "generations",
        []
    )

    generation_id = next_id(
        generations,
        "GEN",
    )

    generation = {
        "id":
            generation_id,
        "request_id":
            request_id,
        "shot_id":
            request["shot"]["id"],
        "prompt_id":
            request["prompt"]["id"],
        "model_id":
            request["model"].get(
                "id"
            )
            if request["model"]
            else None,
        "output_directory":
            request["output"][
                "directory"
            ],
        "outputs":
            output_files,
        "output_count":
            len(output_files),
        "status":
            (
                "GENERATED"
                if output_files
                else "NO_OUTPUT"
            ),
        "selected":
            False,
        "qc":
            "NOT_REVIEWED",
        "execution":
            execution,
        "created":
            now_iso(),
    }

    generations.append(
        generation
    )

    save_state(
        project_root,
        state,
    )

    append_event(
        project_root,
        "AI_GENERATION_REGISTERED",
        generation_id,
        generation,
    )

    return generation


# ============================================================
# GENERATION EXECUTION
# ============================================================

def run_generation(
    project_root: Path,
    state: Dict[str, Any],
    shot_id: str,
    prompt_id: str,
    model_id: str,
    output_path: str,
    execute: bool,
    command_template: Optional[str],
    timeout: int,
) -> Dict[str, Any]:

    output = resolve_relative_path(
        project_root,
        output_path,
    )

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    request_id = next_id(
        state.get(
            "generations",
            []
        ),
        "REQ",
    )

    request = build_request(
        state=state,
        shot_id=shot_id,
        prompt_id=prompt_id,
        model_id=model_id,
        output=output,
        project_root=project_root,
    )

    request_path = write_request_file(
        project_root,
        request,
        request_id,
    )

    execution = None

    if not execute:

        result = {
            "status":
                "DRY_RUN",
            "request_id":
                request_id,
            "request_file":
                str(request_path),
            "output":
                str(output),
            "execution":
                None,
            "outputs":
                discover_outputs(
                    output
                ),
        }

        append_event(
            project_root,
            "AI_GENERATION_DRY_RUN",
            request_id,
            result,
        )

        return result

    if command_template:

        command = build_command(
            command_template,
            project_id=state[
                "project"
            ][
                "id"
            ],
            project_root=project_root,
            project_slug=state[
                "project"
            ].get(
                "slug",
                "",
            ),
            shot_id=shot_id,
            prompt_id=prompt_id,
            model_id=model_id,
            output=output,
            request_path=request_path,
        )

        execution = execute_command(
            command,
            project_root,
            timeout,
        )

    else:

        api_url = os.environ.get(
            "STUDIO_AI_GENERATOR_URL"
        )

        if api_url:

            token = os.environ.get(
                "STUDIO_AI_GENERATOR_TOKEN"
            )

            execution = (
                execute_http_generator(
                    api_url,
                    token,
                    request,
                    timeout,
                )
            )

        else:

            raise RuntimeError(
                "No AI generator is configured. "
                "Set STUDIO_AI_GENERATOR_COMMAND "
                "or STUDIO_AI_GENERATOR_URL, "
                "or run without --execute."
            )

    output_files = discover_outputs(
        output
    )

    result = {
        "status":
            (
                "SUCCESS"
                if output_files
                else "NO_OUTPUT"
            ),
        "request_id":
            request_id,
        "request_file":
            str(request_path),
        "output":
            str(output),
        "execution":
            execution,
        "outputs":
            output_files,
    }

    generation = register_generation(
        project_root,
        state,
        request,
        request_id,
        output_files,
        execution,
    )

    result[
        "generation"
    ] = generation

    if not output_files:

        raise RuntimeError(
            "Generator completed but produced "
            "no recognized media output."
        )

    return result


# ============================================================
# CLI
# ============================================================

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description=(
            "AI Film Studio "
            "AI Generation Adapter"
        )
    )

    parser.add_argument(
        "--project-id",
        required=True,
    )

    parser.add_argument(
        "--project-slug",
        required=True,
    )

    parser.add_argument(
        "--shot-id",
        required=True,
    )

    parser.add_argument(
        "--prompt-id",
        required=True,
    )

    parser.add_argument(
        "--model-id",
        required=True,
    )

    parser.add_argument(
        "--output",
        required=True,
    )

    parser.add_argument(
        "--command",
        help=(
            "Explicit generator command. "
            "Overrides STUDIO_AI_GENERATOR_COMMAND."
        ),
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually execute the external generator.",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Maximum generator runtime in seconds.",
    )

    parser.add_argument(
        "--json-output",
        help="Optional path for adapter result JSON.",
    )

    return parser


# ============================================================
# MAIN
# ============================================================

def main(
    argv: Optional[List[str]] = None,
) -> int:

    parser = build_parser()
    args = parser.parse_args(
        argv
    )

    try:

        project_root = find_project_root(
            args.project_id,
            args.project_slug,
        )

        state = load_state(
            project_root
        )

        if (
            state["project"]["id"]
            != args.project_id
        ):
            raise RuntimeError(
                "Project ID does not match project state."
            )

        if (
            state["project"].get(
                "slug"
            )
            != args.project_slug
        ):
            raise RuntimeError(
                "Project slug does not match project state."
            )

        # Validate shot and prompt before generation.
        find_record(
            state.get(
                "shots",
                []
            ),
            args.shot_id,
        )

        find_record(
            state.get(
                "prompts",
                []
            ),
            args.prompt_id,
        )

        command_template = (
            args.command
            or os.environ.get(
                "STUDIO_AI_GENERATOR_COMMAND"
            )
        )

        result = run_generation(
            project_root=project_root,
            state=state,
            shot_id=args.shot_id,
            prompt_id=args.prompt_id,
            model_id=args.model_id,
            output_path=args.output,
            execute=args.execute,
            command_template=command_template,
            timeout=args.timeout,
        )

        if args.json_output:

            output_path = Path(
                args.json_output
            )

            if not output_path.is_absolute():

                output_path = (
                    project_root
                    / output_path
                )

            safe_json_dump(
                result,
                output_path,
            )

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            )
        )

        return 0

    except KeyboardInterrupt:

        print(
            "Generation interrupted.",
            file=sys.stderr,
        )

        return 130

    except Exception as exc:

        error = {
            "status":
                "FAILED",
            "error":
                str(exc),
            "timestamp":
                now_iso(),
        }

        print(
            json.dumps(
                error,
                indent=2,
            ),
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
