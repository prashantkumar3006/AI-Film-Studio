#!/usr/bin/env python3
"""
AI FILM STUDIO - COMPLETE AUTOMATION ENGINE

Standard-library-only production orchestrator for the AI Film Studio.

Capabilities
------------
- Project initialization and standardized folder creation
- Persistent operational state in JSON
- Command Center synchronization
- Task / dependency / blocker / approval management
- Shot / asset / prompt / generation records
- Next-action engine
- Workflow execution from JSON workflow files
- Local command / Python / shell / file / HTTP automation steps
- Queue management
- File manifests and optional SHA-256 checksums
- Project reports and audits
- Backup and archive packaging
- Storage / environment diagnostics
- Dry-run by default for execution actions
- Event logging
- Version-aware production records

Important
---------
This engine does not magically control Adobe, Kling, ComfyUI, Premiere,
After Effects, or other applications.

For external tools, define an explicit adapter through:
- a CLI
- a local script
- an API
- an MCP / connector integration
- a workflow step

The engine orchestrates those components.

Repository layout
-----------------
AI-Film-Studio/
├── CLAUDE.md
├── README.md
├── .gitignore
├── scripts/
│   ├── create_project.py
│   └── workflows/
└── studio/
    └── ...

Examples
--------
Create project:

    python scripts/create_project.py init \
        --title "My Documentary" \
        --type documentary

Show status:

    python scripts/create_project.py status \
        PROJECT_2026_001 \
        my-documentary

Get next action:

    python scripts/create_project.py next \
        PROJECT_2026_001 \
        my-documentary

Add task:

    python scripts/create_project.py task-add \
        PROJECT_2026_001 \
        my-documentary \
        --name "Research primary sources" \
        --department Research \
        --priority P1

Register shot:

    python scripts/create_project.py shot-add \
        PROJECT_2026_001 \
        my-documentary \
        --name "Station Reveal" \
        --sequence SEQ_001 \
        --scene SCN_001 \
        --purpose "Reveal the abandoned station"

Run workflow safely:

    python scripts/create_project.py workflow-run \
        PROJECT_2026_001 \
        my-documentary \
        --workflow scripts/workflows/example.json

Actually execute:

    python scripts/create_project.py workflow-run \
        PROJECT_2026_001 \
        my-documentary \
        --workflow scripts/workflows/example.json \
        --execute

Diagnostics:

    python scripts/create_project.py doctor
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


# ============================================================
# ENGINE CONSTANTS
# ============================================================

ENGINE_VERSION = "3.0.0"

DEFAULT_VERSION = "v001"
DEFAULT_PROJECT_STATE = "INTAKE"
DEFAULT_PHASE = "INTAKE"
DEFAULT_HEALTH = "GREEN"

PROJECT_TYPES = {
    "narrative",
    "documentary",
    "scientific_documentary",
    "educational",
    "explainer",
    "commercial",
    "promo",
    "music_video",
    "animation",
    "ai_film",
    "hybrid",
    "social",
    "experimental",
}

PROJECT_TYPE_ALIASES = {
    "ai": "ai_film",
    "aifilm": "ai_film",
    "science": "scientific_documentary",
    "scientific": "scientific_documentary",
    "scientific-doc": "scientific_documentary",
    "musicvideo": "music_video",
    "music-video": "music_video",
}

COMPLEXITIES = {
    "SMALL",
    "STANDARD",
    "FULL",
}

TASK_STATUSES = {
    "NOT STARTED",
    "READY",
    "ACTIVE",
    "WAITING",
    "BLOCKED",
    "REVIEW",
    "APPROVED",
    "COMPLETE",
    "CANCELLED",
}

APPROVAL_STATES = {
    "NOT_READY",
    "READY_FOR_REVIEW",
    "IN_REVIEW",
    "CHANGES_REQUIRED",
    "APPROVED",
    "REJECTED",
}

PROJECT_STATES = {
    "INTAKE",
    "ACTIVE",
    "ON HOLD",
    "BLOCKED",
    "REVIEW",
    "APPROVED",
    "PICTURE LOCK",
    "FINISHING",
    "DELIVERY",
    "COMPLETED",
    "ARCHIVED",
    "CANCELLED",
}

PRIORITIES = {
    "P0",
    "P1",
    "P2",
    "P3",
}

SEVERITIES = {
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
}

DEPARTMENT_NAMES = [
    "Director",
    "Producer",
    "Writer",
    "Production Design",
    "Casting & Talent",
    "Storyboard / Previs",
    "Cinematography",
    "Research",
    "AI Generation",
    "Animation",
    "Production Management",
    "Asset Pipeline",
    "Edit",
    "VFX / Motion",
    "Sound",
    "Music",
    "Color",
    "Continuity",
    "Technical Post",
    "Legal / Rights",
    "QC",
    "Distribution",
    "Marketing",
    "Knowledge / Archive",
]

FULL_FOLDERS = [
    "00_admin",
    "01_research",
    "02_story",
    "03_script",
    "04_director",
    "05_production-design",
    "06_casting",
    "07_storyboard-previs",
    "08_cinematography",
    "09_ai-generation",
    "10_animation",
    "11_production",
    "12_edit",
    "13_vfx-motion",
    "14_sound",
    "15_music",
    "16_color",
    "17_continuity",
    "18_technical",
    "19_legal-rights",
    "20_qc",
    "21_distribution",
    "22_marketing",
    "23_knowledge",
    "24_archive",
    "99_backup",
]

STANDARD_FOLDERS = [
    "00_admin",
    "01_research",
    "02_story",
    "03_script",
    "04_director",
    "05_production-design",
    "07_storyboard-previs",
    "08_cinematography",
    "09_ai-generation",
    "11_production",
    "12_edit",
    "13_vfx-motion",
    "14_sound",
    "15_music",
    "16_color",
    "17_continuity",
    "18_technical",
    "19_legal-rights",
    "20_qc",
    "21_distribution",
    "22_marketing",
    "23_knowledge",
    "24_archive",
    "99_backup",
]

SMALL_FOLDERS = [
    "00_admin",
    "01_research",
    "02_story",
    "03_script",
    "04_director",
    "07_storyboard-previs",
    "08_cinematography",
    "09_ai-generation",
    "12_edit",
    "14_sound",
    "16_color",
    "17_continuity",
    "18_technical",
    "20_qc",
    "21_distribution",
    "23_knowledge",
    "24_archive",
    "99_backup",
]

OPTIONAL_SUBFOLDERS = {
    "01_research": [
        "sources",
        "notes",
        "references",
        "visual-research",
    ],
    "03_script": [
        "drafts",
        "approved",
    ],
    "07_storyboard-previs": [
        "storyboards",
        "previs",
        "animatics",
    ],
    "09_ai-generation": [
        "prompts",
        "references",
        "generation-logs",
        "selected",
        "rejected",
    ],
    "12_edit": [
        "projects",
        "exports",
        "selects",
        "proxies",
    ],
    "13_vfx-motion": [
        "shots",
        "motion-graphics",
        "renders",
    ],
    "14_sound": [
        "dialogue",
        "foley",
        "sfx",
        "ambience",
        "mix",
    ],
    "15_music": [
        "score",
        "cues",
        "stems",
    ],
    "19_legal-rights": [
        "rights-records",
        "releases",
        "licenses",
    ],
    "20_qc": [
        "reviews",
        "reports",
        "issues",
    ],
    "21_distribution": [
        "masters",
        "deliverables",
        "metadata",
    ],
    "22_marketing": [
        "trailers",
        "social",
        "thumbnails",
        "key-art",
    ],
    "24_archive": [
        "masters",
        "project-files",
        "research",
        "rights",
        "qc",
        "delivery",
        "checksums",
    ],
}

WORKFLOW_STEP_TYPES = {
    "mkdir",
    "write_text",
    "copy",
    "move",
    "checksum",
    "manifest",
    "http",
    "python",
    "command",
    "shell",
    "sleep",
}

LARGE_MEDIA_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mxf",
    ".avi",
    ".mkv",
    ".webm",
    ".wav",
    ".aiff",
    ".aif",
    ".flac",
    ".psd",
    ".psb",
    ".exr",
    ".dpx",
    ".tif",
    ".tiff",
    ".braw",
    ".r3d",
    ".ari",
    ".dng",
}


# ============================================================
# BASIC UTILITIES
# ============================================================

def now_iso() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).astimezone().isoformat(timespec="seconds")


def today_iso() -> str:
    return dt.date.today().isoformat()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "untitled-project"


def normalize_project_type(value: str) -> str:
    normalized = (
        value.strip()
        .lower()
        .replace(" ", "_")
    )
    return PROJECT_TYPE_ALIASES.get(
        normalized,
        normalized,
    )


def validate_project_type(value: str) -> str:
    project_type = normalize_project_type(value)

    if project_type not in PROJECT_TYPES:
        valid = ", ".join(sorted(PROJECT_TYPES))
        raise ValueError(
            f"Unsupported project type '{value}'. "
            f"Valid values: {valid}"
        )

    return project_type


def choose_complexity(
    project_type: str,
    requested: Optional[str],
) -> str:

    if requested:
        complexity = requested.upper()

        if complexity not in COMPLEXITIES:
            raise ValueError(
                "Complexity must be SMALL, STANDARD, or FULL."
            )

        return complexity

    if project_type in {
        "documentary",
        "scientific_documentary",
        "commercial",
        "music_video",
        "animation",
        "ai_film",
        "hybrid",
    }:
        return "FULL"

    return "STANDARD"


def folders_for(complexity: str) -> List[str]:
    if complexity == "SMALL":
        return SMALL_FOLDERS

    if complexity == "FULL":
        return FULL_FOLDERS

    return STANDARD_FOLDERS


def parse_csv(value: Optional[str]) -> List[str]:
    if not value:
        return []

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def json_load(
    path: Path,
    default: Any = None,
) -> Any:

    if not path.exists():
        return default

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Invalid JSON in {path}: {exc}"
        ) from exc


def json_dump(
    data: Any,
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
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    temp.replace(path)


def write_text(
    path: Path,
    content: str,
    overwrite: bool = False,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if path.exists() and not overwrite:
        raise FileExistsError(
            f"File already exists: {path}"
        )

    path.write_text(
        content,
        encoding="utf-8",
    )


def safe_rel(
    path: Path,
    root: Path,
) -> str:

    try:
        return str(
            path.resolve().relative_to(
                root.resolve()
            )
        ).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def file_sha256(
    path: Path,
    chunk_size: int = 1024 * 1024,
) -> str:

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


# ============================================================
# STUDIO ENGINE
# ============================================================

class StudioEngine:
    """
    Core AI Film Studio orchestration engine.
    """

    def __init__(
        self,
        repo_root: Optional[Path] = None,
    ):

        self.repo_root = (
            repo_root
            or Path(__file__).resolve().parents[1]
        ).resolve()

        self.projects_root = (
            self.repo_root / "projects"
        )

        self.scripts_root = (
            self.repo_root / "scripts"
        )

        self.workflows_root = (
            self.scripts_root / "workflows"
        )

        self.projects_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.workflows_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ========================================================
    # PROJECT PATH / STATE
    # ========================================================

    def project_path(
        self,
        project_id: str,
        slug: str,
    ) -> Path:

        path = (
            self.projects_root
            / project_id
            / slug
        ).resolve()

        if self.repo_root not in path.parents:
            raise RuntimeError(
                "Project path escapes repository root."
            )

        return path

    def require_project(
        self,
        project_id: str,
        slug: str,
    ) -> Path:

        root = self.project_path(
            project_id,
            slug,
        )

        if not root.exists():
            raise FileNotFoundError(
                f"Project not found: {root}"
            )

        if not (
            root / "00_admin"
        ).exists():
            raise RuntimeError(
                f"Invalid studio project: {root}"
            )

        if not (
            root
            / "00_admin"
            / ".studio"
            / "state.json"
        ).exists():
            raise RuntimeError(
                "Project operational state is missing: "
                f"{root / '00_admin' / '.studio' / 'state.json'}"
            )

        return root

    def state_dir(
        self,
        project_root: Path,
    ) -> Path:

        return (
            project_root
            / "00_admin"
            / ".studio"
        )

    def state_path(
        self,
        project_root: Path,
    ) -> Path:

        return (
            self.state_dir(project_root)
            / "state.json"
        )

    def events_path(
        self,
        project_root: Path,
    ) -> Path:

        return (
            self.state_dir(project_root)
            / "events.jsonl"
        )

    def queue_path(
        self,
        project_root: Path,
    ) -> Path:

        return (
            self.state_dir(project_root)
            / "queue.json"
        )

    def load_state(
        self,
        project_root: Path,
    ) -> Dict[str, Any]:

        state = json_load(
            self.state_path(project_root)
        )

        if not isinstance(state, dict):
            raise RuntimeError(
                "Project state must be a JSON object."
            )

        return state

    def save_state(
        self,
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

        json_dump(
            state,
            self.state_path(project_root),
        )

    def log_event(
        self,
        project_root: Path,
        event: str,
        entity: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:

        record = {
            "timestamp": now_iso(),
            "event": event,
            "entity": entity,
            "details": details or {},
        }

        self.events_path(
            project_root
        ).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.events_path(
            project_root
        ).open(
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

    # ========================================================
    # INITIAL STATE
    # ========================================================

    def create_initial_state(
        self,
        project_id: str,
        title: str,
        project_type: str,
        complexity: str,
        runtime: str,
        aspect: str,
        resolution: str,
        fps: str,
    ) -> Dict[str, Any]:

        departments = {}

        for department in DEPARTMENT_NAMES:
            departments[department] = {
                "status": "NOT STARTED",
                "current_task": None,
                "owner": None,
                "blocker": None,
                "approval": None,
                "version": DEFAULT_VERSION,
            }

        return {
            "engine": {
                "name": (
                    "AI Film Studio "
                    "Automation Engine"
                ),
                "version": ENGINE_VERSION,
            },
            "metadata": {
                "created": now_iso(),
                "updated": now_iso(),
            },
            "project": {
                "id": project_id,
                "title": title,
                "slug": slugify(title),
                "type": project_type,
                "complexity": complexity,
                "owner": None,
                "director": None,
                "producer": None,
                "runtime": runtime,
                "resolution": resolution,
                "aspect_ratio": aspect,
                "fps": fps,
                "delivery_date": None,
            },
            "state": {
                "project_state": DEFAULT_PROJECT_STATE,
                "phase": DEFAULT_PHASE,
                "health": DEFAULT_HEALTH,
                "priority": "P1",
                "critical_path": [],
                "current_blocker": None,
                "next_approval": None,
                "next_milestone": None,
                "next_action": (
                    "Complete project brief "
                    "and establish production direction."
                ),
            },
            "departments": departments,
            "tasks": [],
            "shots": [],
            "assets": [],
            "characters": [],
            "locations": [],
            "dependencies": [],
            "blockers": [],
            "risks": [],
            "approvals": [],
            "decisions": [],
            "changes": [],
            "prompts": [],
            "generations": [],
            "deliveries": [],
            "handoffs": [],
            "workflow_runs": [],
        }

    # ========================================================
    # PROJECT INITIALIZATION
    # ========================================================

    def create_project(
        self,
        title: str,
        project_type: str,
        runtime: str = "",
        aspect: str = "16:9",
        resolution: str = "1920x1080",
        fps: str = "24",
        complexity: Optional[str] = None,
        year: Optional[int] = None,
        number: Optional[str] = None,
    ) -> Path:

        if not title.strip():
            raise ValueError(
                "Project title cannot be empty."
            )

        project_type = validate_project_type(
            project_type
        )

        year = (
            year
            or dt.date.today().year
        )

        complexity = choose_complexity(
            project_type,
            complexity,
        )

        project_id = (
            f"PROJECT_{year}_"
            f"{self.next_project_number(year, number):03d}"
        )

        slug = slugify(title)

        root = self.project_path(
            project_id,
            slug,
        )

        if root.exists():
            raise FileExistsError(
                f"Project already exists: {root}"
            )

        root.mkdir(
            parents=True,
            exist_ok=False,
        )

        folders = folders_for(
            complexity
        )

        for folder in folders:
            (
                root / folder
            ).mkdir(
                parents=True,
                exist_ok=True,
            )

        for parent, children in (
            OPTIONAL_SUBFOLDERS.items()
        ):

            if parent not in folders:
                continue

            for child in children:
                (
                    root
                    / parent
                    / child
                ).mkdir(
                    parents=True,
                    exist_ok=True,
                )

        state = self.create_initial_state(
            project_id=project_id,
            title=title,
            project_type=project_type,
            complexity=complexity,
            runtime=runtime,
            aspect=aspect,
            resolution=resolution,
            fps=fps,
        )

        self.state_dir(root).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.save_state(
            root,
            state,
        )

        self.write_initial_project_files(
            root,
            state,
        )

        self.log_event(
            root,
            "PROJECT_CREATED",
            project_id,
            {
                "title": title,
                "type": project_type,
                "complexity": complexity,
            },
        )

        self.sync_all(
            root,
            state,
        )

        return root

    def next_project_number(
        self,
        year: int,
        requested: Optional[str],
    ) -> int:

        if requested:
            digits = re.sub(
                r"\D",
                "",
                requested,
            )

            if not digits:
                raise ValueError(
                    "Project number must contain digits."
                )

            number = int(digits)

            if number <= 0:
                raise ValueError(
                    "Project number must be greater than zero."
                )

            return number

        max_number = 0

        if self.projects_root.exists():

            pattern = re.compile(
                rf"^PROJECT_{year}_(\d+)$"
            )

            for item in (
                self.projects_root.iterdir()
            ):

                if not item.is_dir():
                    continue

                match = pattern.match(
                    item.name
                )

                if match:
                    max_number = max(
                        max_number,
                        int(match.group(1)),
                    )

        return max_number + 1

    def write_initial_project_files(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        project = state["project"]

        files = {}

        files[
            "README.md"
        ] = f"""# {project['title']}

Project ID:
{project['id']}

Project Type:
{project['type']}

Complexity:
{project['complexity']}

Created by:
AI Film Studio Automation Engine {ENGINE_VERSION}

Operational state:
`00_admin/.studio/state.json`

Project Command Center:
`00_admin/command_center.md`

Studio-wide systems:
`../../studio/`
"""

        files[
            "00_admin/project_brief.md"
        ] = f"""# PROJECT BRIEF

Project ID:
{project['id']}

Project Title:
{project['title']}

Project Type:
{project['type']}

## PURPOSE

## AUDIENCE

## LOGLINE

## PREMISE

## SYNOPSIS

## CORE THEME

## TONE

## VISUAL DIRECTION

## EMOTIONAL EXPERIENCE

## RESEARCH REQUIREMENTS

## CREATIVE CONSTRAINTS

## TECHNICAL CONSTRAINTS

## RIGHTS CONSIDERATIONS

## MAJOR DELIVERABLES

## SUCCESS CRITERIA

## OPEN QUESTIONS
"""

        files[
            "00_admin/schedule.md"
        ] = """# SCHEDULE

## PROJECT START

## TARGET COMPLETION

## TARGET DELIVERY

## MILESTONES
"""

        files[
            "00_admin/milestone_tracker.md"
        ] = """# MILESTONE TRACKER

| Milestone ID | Milestone | Phase | Owner | Status |
|---|---|---|---|---|
| MILESTONE_001 | Project Brief | INTAKE | Producer | NOT STARTED |
| MILESTONE_002 | Story / Script | STORY | Writer / Director | NOT STARTED |
| MILESTONE_003 | Production Ready | PRODUCTION | Production Management | NOT STARTED |
| MILESTONE_004 | Picture Lock | EDIT | Editor / Director | NOT STARTED |
| MILESTONE_005 | Final QC | QC | QC | NOT STARTED |
| MILESTONE_006 | Delivery | DELIVERY | Distribution | NOT STARTED |
"""

        files[
            "00_admin/delivery_matrix.md"
        ] = """# DELIVERY MATRIX

| Destination | Deliverable | Resolution | Aspect Ratio | Frame Rate | Codec | Audio | Subtitle | QC | Rights | Status |
|---|---|---|---|---|---|---|---|---|---|---|
"""

        files[
            "00_admin/master_continuity.md"
        ] = """# MASTER CONTINUITY

## CHARACTER CONTINUITY

## COSTUME CONTINUITY

## PROP CONTINUITY

## LOCATION CONTINUITY

## TIME CONTINUITY

## WEATHER CONTINUITY

## LIGHTING CONTINUITY

## SCREEN DIRECTION

## PERFORMANCE CONTINUITY

## SOUND CONTINUITY

## MUSIC CONTINUITY

## VFX CONTINUITY

## AI VISUAL CONTINUITY

## OPEN CONTINUITY ISSUES
"""

        for relative, content in (
            files.items()
        ):

            write_text(
                root / relative,
                content,
            )

        self.sync_all(
            root,
            state,
        )

        self.create_project_workflow_examples(
            root,
        )

    def create_project_workflow_examples(
        self,
        root: Path,
    ) -> None:

        workflow_dir = (
            root
            / "18_technical"
            / "workflows"
        )

        workflow_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        example = {
            "id": "WF_PROJECT_HEALTH",
            "name": "Project Health Audit",
            "version": "v001",
            "description": (
                "Run an audit and generate "
                "a project manifest."
            ),
            "steps": [
                {
                    "name": "audit",
                    "type": "command",
                    "args": [
                        sys.executable,
                        str(
                            self.repo_root
                            / "scripts"
                            / "create_project.py"
                        ),
                        "audit",
                        "{{PROJECT_ID}}",
                        "{{PROJECT_SLUG}}",
                    ],
                },
                {
                    "name": "manifest",
                    "type": "command",
                    "args": [
                        sys.executable,
                        str(
                            self.repo_root
                            / "scripts"
                            / "create_project.py"
                        ),
                        "manifest",
                        "{{PROJECT_ID}}",
                        "{{PROJECT_SLUG}}",
                    ],
                },
            ],
        }

        write_text(
            workflow_dir
            / "project_health.json",
            json.dumps(
                example,
                indent=2,
            )
            + "\n",
        )

    # ========================================================
    # MARKDOWN SYNCHRONIZATION
    # ========================================================

    def sync_all(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        self.sync_project_identity(
            root,
            state,
        )

        self.sync_production_status(
            root,
            state,
        )

        self.sync_task_tracker(
            root,
            state,
        )

        self.sync_shot_list(
            root,
            state,
        )

        self.sync_asset_inventory(
            root,
            state,
        )

        self.sync_blockers(
            root,
            state,
        )

        self.sync_risks(
            root,
            state,
        )

        self.sync_decisions(
            root,
            state,
        )

        self.sync_changes(
            root,
            state,
        )

        self.sync_approvals(
            root,
            state,
        )

        self.sync_deliveries(
            root,
            state,
        )

        self.sync_command_center(
            root,
            state,
        )

    def sync_project_identity(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        p = state["project"]
        s = state["state"]

        content = f"""# PROJECT IDENTITY

Project ID:
{p['id']}

Project Title:
{p['title']}

Project Type:
{p['type']}

Project Complexity:
{p['complexity']}

Current Version:
{DEFAULT_VERSION}

Project State:
{s['project_state']}

Current Phase:
{s['phase']}

Target Runtime:
{p['runtime']}

Target Resolution:
{p['resolution']}

Frame Rate:
{p['fps']}

Primary Aspect Ratio:
{p['aspect_ratio']}

Project Owner:
{p['owner'] or ''}

Director:
{p['director'] or ''}

Producer:
{p['producer'] or ''}

Created:
{state['metadata']['created']}

Last Updated:
{state['metadata']['updated']}

Automation Engine:
{ENGINE_VERSION}
"""

        write_text(
            root
            / "00_admin"
            / "project_identity.md",
            content,
            overwrite=True,
        )

    def sync_production_status(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        s = state["state"]

        active = [
            task
            for task in state["tasks"]
            if task["status"] == "ACTIVE"
        ]

        blocked = [
            task
            for task in state["tasks"]
            if task["status"] == "BLOCKED"
        ]

        waiting = [
            task
            for task in state["tasks"]
            if task["status"] == "WAITING"
        ]

        lines = [
            "# PRODUCTION STATUS",
            "",
            f"Project ID:\n{state['project']['id']}",
            "",
            f"Last Updated:\n{state['metadata']['updated']}",
            "",
            f"Overall State:\n{s['project_state']}",
            "",
            f"Overall Health:\n{s['health']}",
            "",
            f"Current Phase:\n{s['phase']}",
            "",
            f"Current Priority:\n{s['priority']}",
            "",
            f"Critical Path:\n{', '.join(s['critical_path']) or 'Not defined'}",
            "",
            f"Current Blocker:\n{s['current_blocker'] or 'None'}",
            "",
            f"Next Approval:\n{s['next_approval'] or 'None'}",
            "",
            f"Next Milestone:\n{s['next_milestone'] or 'None'}",
            "",
            "## ACTIVE",
        ]

        lines.extend(
            [
                f"- {task['id']}: "
                f"{task['name']} "
                f"({task['department']})"
                for task in active
            ]
            or ["- None"]
        )

        lines.append("")
        lines.append("## BLOCKED")

        lines.extend(
            [
                f"- {task['id']}: "
                f"{task['name']}"
                for task in blocked
            ]
            or ["- None"]
        )

        lines.append("")
        lines.append("## WAITING")

        lines.extend(
            [
                f"- {task['id']}: "
                f"{task['name']}"
                for task in waiting
            ]
            or ["- None"]
        )

        lines.append("")
        lines.append("## NEXT ACTION")
        lines.append(
            s["next_action"]
        )

        write_text(
            root
            / "00_admin"
            / "production_status.md",
            "\n".join(lines)
            + "\n",
            overwrite=True,
        )

    def sync_task_tracker(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# TASK TRACKER",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Task ID | Task | Department | Phase | Priority | Owner | Dependencies | Status | Version |",
            "|---|---|---|---|---|---|---|---|---|",
        ]

        for task in state["tasks"]:

            dependencies = ", ".join(
                task.get("dependencies", [])
            )

            rows.append(
                f"| {task['id']} | "
                f"{task['name']} | "
                f"{task['department']} | "
                f"{task.get('phase', '')} | "
                f"{task['priority']} | "
                f"{task.get('owner') or ''} | "
                f"{dependencies} | "
                f"{task['status']} | "
                f"{task['version']} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "task_tracker.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_shot_list(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# SHOT LIST",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Shot ID | Sequence | Scene | Shot Name | Purpose | Characters | Location | Camera | AI | VFX | Status | Version |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]

        for shot in state["shots"]:

            rows.append(
                f"| {shot['id']} | "
                f"{shot.get('sequence', '')} | "
                f"{shot.get('scene', '')} | "
                f"{shot['name']} | "
                f"{shot.get('purpose', '')} | "
                f"{', '.join(shot.get('characters', []))} | "
                f"{shot.get('location', '')} | "
                f"{shot.get('camera', '')} | "
                f"{shot.get('ai', False)} | "
                f"{shot.get('vfx', False)} | "
                f"{shot['status']} | "
                f"{shot['version']} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "shot_list.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_asset_inventory(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# ASSET INVENTORY",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Asset ID | Asset Name | Type | Department | Version | Path | Rights | QC | Status |",
            "|---|---|---|---|---|---|---|---|---|",
        ]

        for asset in state["assets"]:

            rows.append(
                f"| {asset['id']} | "
                f"{asset['name']} | "
                f"{asset['type']} | "
                f"{asset['department']} | "
                f"{asset['version']} | "
                f"{asset.get('path', '')} | "
                f"{asset.get('rights', '')} | "
                f"{asset.get('qc', '')} | "
                f"{asset['status']} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "asset_inventory.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_blockers(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# BLOCKER REGISTER",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Blocker ID | Description | Department | Severity | Affected Task | Owner | Resolution | Status |",
            "|---|---|---|---|---|---|---|---|",
        ]

        for blocker in state["blockers"]:

            rows.append(
                f"| {blocker['id']} | "
                f"{blocker['description']} | "
                f"{blocker['department']} | "
                f"{blocker['severity']} | "
                f"{blocker.get('task_id', '')} | "
                f"{blocker.get('owner', '')} | "
                f"{blocker.get('resolution', '')} | "
                f"{blocker['status']} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "blocker_register.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_risks(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# RISK REGISTER",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Risk ID | Risk | Category | Probability | Impact | Severity | Mitigation | Owner | Status |",
            "|---|---|---|---|---|---|---|---|---|",
        ]

        for risk in state["risks"]:

            rows.append(
                f"| {risk['id']} | "
                f"{risk['risk']} | "
                f"{risk.get('category', '')} | "
                f"{risk.get('probability', '')} | "
                f"{risk.get('impact', '')} | "
                f"{risk.get('severity', '')} | "
                f"{risk.get('mitigation', '')} | "
                f"{risk.get('owner', '')} | "
                f"{risk['status']} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "risk_register.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_decisions(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# DECISION LOG",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Decision ID | Date | Decision | Owner | Reason | Affected Areas | Version |",
            "|---|---|---|---|---|---|---|",
        ]

        for item in state["decisions"]:

            rows.append(
                f"| {item['id']} | "
                f"{item['date']} | "
                f"{item['decision']} | "
                f"{item.get('owner', '')} | "
                f"{item.get('reason', '')} | "
                f"{', '.join(item.get('affected', []))} | "
                f"{item['version']} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "decision_log.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_changes(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# CHANGE LOG",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Change ID | Date | Entity | Current Version | Requested Change | Impact | Approval | Status |",
            "|---|---|---|---|---|---|---|---|",
        ]

        for item in state["changes"]:

            rows.append(
                f"| {item['id']} | "
                f"{item['date']} | "
                f"{item['entity']} | "
                f"{item['version']} | "
                f"{item['change']} | "
                f"{item.get('impact', '')} | "
                f"{item.get('approval', '')} | "
                f"{item['status']} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "change_log.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_approvals(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# APPROVAL LOG",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Approval ID | Gate | Entity | Version | Reviewer | Status | Date | Comments |",
            "|---|---|---|---|---|---|---|---|",
        ]

        for item in state["approvals"]:

            rows.append(
                f"| {item['id']} | "
                f"{item['gate']} | "
                f"{item.get('entity', '')} | "
                f"{item['version']} | "
                f"{item.get('reviewer', '')} | "
                f"{item['status']} | "
                f"{item.get('date', '')} | "
                f"{item.get('comments', '')} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "approval_log.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_deliveries(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        rows = [
            "# DELIVERY LOG",
            "",
            f"Project ID: {state['project']['id']}",
            "",
            "| Delivery ID | Destination | Deliverable | Version | QC | Rights | Date | Status |",
            "|---|---|---|---|---|---|---|---|",
        ]

        for item in state["deliveries"]:

            rows.append(
                f"| {item['id']} | "
                f"{item.get('destination', '')} | "
                f"{item.get('deliverable', '')} | "
                f"{item['version']} | "
                f"{item.get('qc', '')} | "
                f"{item.get('rights', '')} | "
                f"{item.get('date', '')} | "
                f"{item['status']} |"
            )

        if len(rows) == 6:
            rows.append(
                "| | | | | | | |"
            )

        write_text(
            root
            / "00_admin"
            / "delivery_log.md",
            "\n".join(rows)
            + "\n",
            overwrite=True,
        )

    def sync_command_center(
        self,
        root: Path,
        state: Dict[str, Any],
    ) -> None:

        p = state["project"]
        s = state["state"]

        active_departments = [
            name
            for name, data
            in state["departments"].items()
            if data["status"] == "ACTIVE"
        ]

        open_blockers = [
            b
            for b in state["blockers"]
            if b["status"] != "RESOLVED"
        ]

        pending_approvals = [
            a
            for a in state["approvals"]
            if a["status"] in {
                "READY_FOR_REVIEW",
                "IN_REVIEW",
                "CHANGES_REQUIRED",
            }
        ]

        lines = [
            "# PROJECT COMMAND CENTER",
            "",
            f"Project: {p['title']}",
            "",
            f"Project ID: {p['id']}",
            "",
            f"Project Type: {p['type']}",
            "",
            f"Current State: {s['project_state']}",
            "",
            f"Current Phase: {s['phase']}",
            "",
            f"Health: {s['health']}",
            "",
            f"Priority: {s['priority']}",
            "",
            "## ACTIVE DEPARTMENTS",
        ]

        lines.extend(
            [f"- {d}" for d in active_departments]
            or ["- None"]
        )

        lines.extend(
            [
                "",
                "## CRITICAL PATH",
                ", ".join(
                    s["critical_path"]
                )
                or "Not defined",
                "",
                "## BLOCKERS",
            ]
        )

        lines.extend(
            [
                f"- {b['id']}: "
                f"{b['description']} "
                f"({b['severity']})"
                for b in open_blockers
            ]
            or ["- None"]
        )

        lines.extend(
            [
                "",
                "## APPROVALS",
            ]
        )

        lines.extend(
            [
                f"- {a['id']}: "
                f"{a['gate']} "
                f"({a['status']})"
                for a in pending_approvals
            ]
            or ["- None"]
        )

        lines.extend(
            [
                "",
                "## NEXT ACTION",
                s["next_action"],
                "",
                "## NEXT APPROVAL",
                s["next_approval"] or "None",
                "",
                "## NEXT MILESTONE",
                s["next_milestone"] or "None",
                "",
                "## LAST UPDATED",
                state["metadata"]["updated"],
            ]
        )

        write_text(
            root
            / "00_admin"
            / "command_center.md",
            "\n".join(lines)
            + "\n",
            overwrite=True,
        )

    # ========================================================
    # ENTITY HELPERS
    # ========================================================

    @staticmethod
    def next_entity_id(
        records: Iterable[Dict[str, Any]],
        prefix: str,
    ) -> str:

        highest = 0

        pattern = re.compile(
            rf"^{re.escape(prefix)}_(\d+)$"
        )

        for record in records:

            match = pattern.match(
                str(record.get("id", ""))
            )

            if match:
                highest = max(
                    highest,
                    int(match.group(1)),
                )

        return (
            f"{prefix}_{highest + 1:03d}"
        )

    @staticmethod
    def find_record(
        records: List[Dict[str, Any]],
        entity_id: str,
    ) -> Dict[str, Any]:

        for record in records:

            if record.get("id") == entity_id:
                return record

        raise KeyError(
            f"Entity not found: {entity_id}"
        )

    # ========================================================
    # TASK ENGINE
    # ========================================================

    def add_task(
        self,
        root: Path,
        name: str,
        department: str,
        priority: str,
        phase: str,
        owner: Optional[str],
        dependencies: List[str],
        description: str,
    ) -> Dict[str, Any]:

        priority = priority.upper()

        if priority not in PRIORITIES:
            raise ValueError(
                "Priority must be P0, P1, P2, or P3."
            )

        state = self.load_state(
            root
        )

        for dependency in dependencies:

            self.find_record(
                state["tasks"],
                dependency,
            )

        task_id = self.next_entity_id(
            state["tasks"],
            "TASK",
        )

        task = {
            "id": task_id,
            "name": name,
            "department": department,
            "phase": (
                phase
                or state["state"]["phase"]
            ),
            "priority": priority,
            "owner": owner,
            "description": description,
            "inputs": [],
            "outputs": [],
            "dependencies": dependencies,
            "blocked_by": [],
            "status": "NOT STARTED",
            "approval_required": False,
            "approval_state": None,
            "qc_required": False,
            "qc_state": None,
            "version": DEFAULT_VERSION,
            "created": now_iso(),
            "updated": now_iso(),
        }

        state["tasks"].append(
            task
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "TASK_CREATED",
            task_id,
            task,
        )

        self.recalculate_state(
            root,
            state,
        )

        self.sync_all(
            root,
            state,
        )

        return task

    def update_task(
        self,
        root: Path,
        task_id: str,
        **updates: Any,
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        task = self.find_record(
            state["tasks"],
            task_id,
        )

        allowed = {
            "name",
            "department",
            "phase",
            "priority",
            "owner",
            "description",
            "status",
            "approval_required",
            "approval_state",
            "qc_required",
            "qc_state",
            "version",
            "blocked_by",
        }

        for key, value in updates.items():

            if key in allowed and value is not None:

                if key == "status":
                    value = value.upper()

                    if value not in TASK_STATUSES:
                        raise ValueError(
                            f"Invalid task status: {value}"
                        )

                if key == "priority":

                    value = value.upper()

                    if value not in PRIORITIES:
                        raise ValueError(
                            f"Invalid priority: {value}"
                        )

                task[key] = value

        task["updated"] = now_iso()

        if task["status"] == "COMPLETE":
            task["completed"] = now_iso()

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "TASK_UPDATED",
            task_id,
            updates,
        )

        self.recalculate_state(
            root,
            state,
        )

        self.sync_all(
            root,
            state,
        )

        return task

    # ========================================================
    # SHOT ENGINE
    # ========================================================

    def add_shot(
        self,
        root: Path,
        name: str,
        sequence: str,
        scene: str,
        purpose: str,
        location: str,
        camera: str,
        characters: List[str],
        ai: bool,
        vfx: bool,
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        shot_id = self.next_entity_id(
            state["shots"],
            "SHOT",
        )

        shot = {
            "id": shot_id,
            "name": name,
            "sequence": sequence,
            "scene": scene,
            "purpose": purpose,
            "location": location,
            "camera": camera,
            "characters": characters,
            "ai": ai,
            "vfx": vfx,
            "status": "PLANNED",
            "version": DEFAULT_VERSION,
            "created": now_iso(),
            "updated": now_iso(),
        }

        state["shots"].append(
            shot
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "SHOT_CREATED",
            shot_id,
            shot,
        )

        self.sync_all(
            root,
            state,
        )

        return shot

    # ========================================================
    # ASSET ENGINE
    # ========================================================

    def add_asset(
        self,
        root: Path,
        name: str,
        asset_type: str,
        department: str,
        path: str,
        status: str,
        rights: str,
        qc: str,
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        asset_id = self.next_entity_id(
            state["assets"],
            "ASSET",
        )

        asset = {
            "id": asset_id,
            "name": name,
            "type": asset_type,
            "department": department,
            "path": path,
            "status": status,
            "rights": rights,
            "qc": qc,
            "version": DEFAULT_VERSION,
            "created": now_iso(),
            "updated": now_iso(),
        }

        state["assets"].append(
            asset
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "ASSET_REGISTERED",
            asset_id,
            asset,
        )

        self.sync_all(
            root,
            state,
        )

        return asset

    # ========================================================
    # PROMPT ENGINE
    # ========================================================

    def add_prompt(
        self,
        root: Path,
        purpose: str,
        prompt_text: str,
        department: str,
        model: str,
        entity_id: Optional[str],
        negative: str,
        references: List[str],
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        prompt_id = self.next_entity_id(
            state["prompts"],
            "PROMPT",
        )

        prompt = {
            "id": prompt_id,
            "purpose": purpose,
            "department": department,
            "model": model,
            "entity_id": entity_id,
            "prompt": prompt_text,
            "negative_constraints": negative,
            "references": references,
            "version": DEFAULT_VERSION,
            "status": "DRAFT",
            "created": now_iso(),
            "updated": now_iso(),
        }

        state["prompts"].append(
            prompt
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "PROMPT_CREATED",
            prompt_id,
            prompt,
        )

        return prompt

    # ========================================================
    # GENERATION ENGINE
    # ========================================================

    def add_generation(
        self,
        root: Path,
        prompt_id: str,
        model: str,
        output: str,
        selected: bool,
        qc: str,
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        self.find_record(
            state["prompts"],
            prompt_id,
        )

        generation_id = self.next_entity_id(
            state["generations"],
            "GEN",
        )

        generation = {
            "id": generation_id,
            "prompt_id": prompt_id,
            "model": model,
            "output": output,
            "selected": selected,
            "qc": qc,
            "status": "GENERATED",
            "created": now_iso(),
        }

        state["generations"].append(
            generation
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "GENERATION_REGISTERED",
            generation_id,
            generation,
        )

        return generation

    # ========================================================
    # BLOCKER ENGINE
    # ========================================================

    def add_blocker(
        self,
        root: Path,
        description: str,
        department: str,
        severity: str,
        task_id: Optional[str],
        owner: Optional[str],
        resolution: str,
    ) -> Dict[str, Any]:

        severity = severity.upper()

        if severity not in SEVERITIES:
            raise ValueError(
                "Severity must be CRITICAL, HIGH, MEDIUM, or LOW."
            )

        state = self.load_state(
            root
        )

        if task_id:
            self.find_record(
                state["tasks"],
                task_id,
            )

        blocker_id = self.next_entity_id(
            state["blockers"],
            "BLOCK",
        )

        blocker = {
            "id": blocker_id,
            "description": description,
            "department": department,
            "severity": severity,
            "task_id": task_id,
            "owner": owner,
            "resolution": resolution,
            "status": "OPEN",
            "created": now_iso(),
            "resolved": None,
        }

        state["blockers"].append(
            blocker
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "BLOCKER_CREATED",
            blocker_id,
            blocker,
        )

        self.recalculate_state(
            root,
            state,
        )

        self.sync_all(
            root,
            state,
        )

        return blocker

    def resolve_blocker(
        self,
        root: Path,
        blocker_id: str,
        note: str,
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        blocker = self.find_record(
            state["blockers"],
            blocker_id,
        )

        blocker["status"] = "RESOLVED"
        blocker["resolved"] = now_iso()

        if note:
            blocker["resolution"] = note

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "BLOCKER_RESOLVED",
            blocker_id,
            blocker,
        )

        self.recalculate_state(
            root,
            state,
        )

        self.sync_all(
            root,
            state,
        )

        return blocker

    # ========================================================
    # APPROVAL ENGINE
    # ========================================================

    def add_approval(
        self,
        root: Path,
        gate: str,
        entity: str,
        version: str,
        reviewer: Optional[str],
        status: str,
        comments: str,
    ) -> Dict[str, Any]:

        status = status.upper()

        if status not in APPROVAL_STATES:
            raise ValueError(
                "Invalid approval state."
            )

        state = self.load_state(
            root
        )

        approval_id = self.next_entity_id(
            state["approvals"],
            "APR",
        )

        approval = {
            "id": approval_id,
            "gate": gate,
            "entity": entity,
            "version": version,
            "reviewer": reviewer,
            "status": status,
            "date": today_iso(),
            "comments": comments,
        }

        state["approvals"].append(
            approval
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "APPROVAL_CREATED",
            approval_id,
            approval,
        )

        self.recalculate_state(
            root,
            state,
        )

        self.sync_all(
            root,
            state,
        )

        return approval

    def set_approval(
        self,
        root: Path,
        approval_id: str,
        status: str,
        comments: str,
    ) -> Dict[str, Any]:

        status = status.upper()

        if status not in APPROVAL_STATES:
            raise ValueError(
                "Invalid approval state."
            )

        state = self.load_state(
            root
        )

        approval = self.find_record(
            state["approvals"],
            approval_id,
        )

        approval["status"] = status
        approval["date"] = today_iso()

        if comments:
            approval["comments"] = comments

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "APPROVAL_UPDATED",
            approval_id,
            approval,
        )

        self.recalculate_state(
            root,
            state,
        )

        self.sync_all(
            root,
            state,
        )

        return approval

    # ========================================================
    # DECISION ENGINE
    # ========================================================

    def add_decision(
        self,
        root: Path,
        decision: str,
        reason: str,
        owner: Optional[str],
        affected: List[str],
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        decision_id = self.next_entity_id(
            state["decisions"],
            "DEC",
        )

        item = {
            "id": decision_id,
            "date": today_iso(),
            "decision": decision,
            "reason": reason,
            "owner": owner,
            "affected": affected,
            "version": DEFAULT_VERSION,
        }

        state["decisions"].append(
            item
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "DECISION_CREATED",
            decision_id,
            item,
        )

        self.sync_all(
            root,
            state,
        )

        return item

    # ========================================================
    # CHANGE ENGINE
    # ========================================================

    def add_change(
        self,
        root: Path,
        entity: str,
        change: str,
        impact: str,
        approval: str,
        status: str,
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        change_id = self.next_entity_id(
            state["changes"],
            "CHG",
        )

        item = {
            "id": change_id,
            "date": today_iso(),
            "entity": entity,
            "version": DEFAULT_VERSION,
            "change": change,
            "impact": impact,
            "approval": approval,
            "status": status,
        }

        state["changes"].append(
            item
        )

        self.save_state(
            root,
            state,
        )

        self.log_event(
            root,
            "CHANGE_CREATED",
            change_id,
            item,
        )

        self.sync_all(
            root,
            state,
        )

        return item

    # ========================================================
    # NEXT-ACTION ENGINE
    # ========================================================

    def task_ready(
        self,
        state: Dict[str, Any],
        task: Dict[str, Any],
    ) -> bool:

        if task["status"] in {
            "COMPLETE",
            "CANCELLED",
            "BLOCKED",
        }:
            return False

        if task.get("blocked_by"):

            unresolved_blockers = [
                blocker
                for blocker
                in state["blockers"]
                if blocker["id"]
                in task["blocked_by"]
                and blocker["status"]
                != "RESOLVED"
            ]

            if unresolved_blockers:
                return False

        for dependency in (
            task.get("dependencies", [])
        ):

            dependency_task = next(
                (
                    item
                    for item
                    in state["tasks"]
                    if item["id"] == dependency
                ),
                None,
            )

            if (
                dependency_task is None
                or dependency_task["status"]
                != "COMPLETE"
            ):
                return False

        if task.get("approval_required"):

            if task.get(
                "approval_state"
            ) != "APPROVED":
                return False

        return True

    def calculate_next_task(
        self,
        state: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:

        open_blockers = [
            blocker
            for blocker
            in state["blockers"]
            if blocker["status"]
            != "RESOLVED"
        ]

        critical = [
            blocker
            for blocker
            in open_blockers
            if blocker["severity"]
            == "CRITICAL"
        ]

        if critical:

            critical_id = critical[0]["id"]

            blocked_tasks = [
                task
                for task
                in state["tasks"]
                if critical_id
                in task.get("blocked_by", [])
                and task["status"]
                not in {
                    "COMPLETE",
                    "CANCELLED",
                }
            ]

            if blocked_tasks:
                return blocked_tasks[0]

        candidates = [
            task
            for task
            in state["tasks"]
            if self.task_ready(
                state,
                task,
            )
        ]

        if not candidates:
            return None

        priority_rank = {
            "P0": 0,
            "P1": 1,
            "P2": 2,
            "P3": 3,
        }

        candidates.sort(
            key=lambda item: (
                priority_rank.get(
                    item["priority"],
                    9,
                ),
                0
                if item["status"]
                == "ACTIVE"
                else 1,
                item.get(
                    "created",
                    "",
                ),
            )
        )

        return candidates[0]

    def critical_path(
        self,
        state: Dict[str, Any],
    ) -> List[str]:

        tasks = {
            task["id"]: task
            for task
            in state["tasks"]
        }

        memo: Dict[
            str,
            List[str],
        ] = {}

        visiting: set[str] = set()

        def walk(
            task_id: str,
        ) -> List[str]:

            if task_id in memo:
                return memo[task_id]

            if task_id in visiting:
                return [task_id]

            visiting.add(task_id)

            task = tasks.get(
                task_id
            )

            if not task:
                visiting.remove(task_id)
                return []

            best: List[str] = []

            for dependency in (
                task.get(
                    "dependencies",
                    [],
                )
            ):

                candidate = walk(
                    dependency
                )

                if len(candidate) > len(best):
                    best = candidate

            visiting.remove(task_id)

            result = (
                best
                + [task_id]
            )

            memo[
                task_id
            ] = result

            return result

        incomplete = [
            task
            for task
            in state["tasks"]
            if task["status"]
            not in {
                "COMPLETE",
                "CANCELLED",
            }
        ]

        best: List[str] = []

        for task in incomplete:

            chain = walk(
                task["id"]
            )

            if len(chain) > len(best):
                best = chain

        return best

    def recalculate_state(
        self,
        root: Path,
        state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        state = (
            state
            or self.load_state(root)
        )

        open_blockers = [
            blocker
            for blocker
            in state["blockers"]
            if blocker["status"]
            != "RESOLVED"
        ]

        critical_blockers = [
            blocker
            for blocker
            in open_blockers
            if blocker["severity"]
            == "CRITICAL"
        ]

        if critical_blockers:

            state["state"][
                "health"
            ] = "RED"

        elif (
            open_blockers
            or any(
                task["status"]
                == "BLOCKED"
                for task
                in state["tasks"]
            )
        ):

            state["state"][
                "health"
            ] = "YELLOW"

        else:

            state["state"][
                "health"
            ] = "GREEN"

        if critical_blockers:

            state["state"][
                "project_state"
            ] = "BLOCKED"

        state["state"][
            "current_blocker"
        ] = (
            critical_blockers[0]["id"]
            if critical_blockers
            else (
                open_blockers[0]["id"]
                if open_blockers
                else None
            )
        )

        pending_approvals = [
            approval
            for approval
            in state["approvals"]
            if approval["status"]
            in {
                "READY_FOR_REVIEW",
                "IN_REVIEW",
                "CHANGES_REQUIRED",
            }
        ]

        state["state"][
            "next_approval"
        ] = (
            pending_approvals[0]["id"]
            if pending_approvals
            else None
        )

        next_task = (
            self.calculate_next_task(
                state
            )
        )

        incomplete = [
            task
            for task
            in state["tasks"]
            if task["status"]
            not in {
                "COMPLETE",
                "CANCELLED",
            }
        ]

        if next_task:

            state["state"][
                "next_action"
            ] = (
                f"{next_task['id']} — "
                f"{next_task['name']} "
                f"({next_task['department']}, "
                f"{next_task['priority']})"
            )

            state["state"][
                "priority"
            ] = next_task[
                "priority"
            ]

        elif not incomplete:

            state["state"][
                "next_action"
            ] = (
                "No incomplete tasks remain; "
                "run final QC and delivery-readiness checks."
            )

        else:

            state["state"][
                "next_action"
            ] = (
                "Review dependency, "
                "blocker, and approval state."
            )

        state["state"][
            "critical_path"
        ] = self.critical_path(
            state
        )

        self.save_state(
            root,
            state,
        )

        return state

    # ========================================================
    # STATUS / REPORT
    # ========================================================

    def status_report(
        self,
        root: Path,
    ) -> Dict[str, Any]:

        state = (
            self.recalculate_state(
                root
            )
        )

        return {
            "engine": ENGINE_VERSION,
            "project": state["project"],
            "state": state["state"],
            "department_summary": {
                "ACTIVE": sum(
                    1
                    for data
                    in state["departments"].values()
                    if data["status"]
                    == "ACTIVE"
                ),
                "BLOCKED": sum(
                    1
                    for data
                    in state["departments"].values()
                    if data["status"]
                    == "BLOCKED"
                ),
                "COMPLETE": sum(
                    1
                    for data
                    in state["departments"].values()
                    if data["status"]
                    == "COMPLETE"
                ),
            },
            "tasks": {
                "total": len(
                    state["tasks"]
                ),
                "complete": sum(
                    1
                    for task
                    in state["tasks"]
                    if task["status"]
                    == "COMPLETE"
                ),
                "active": sum(
                    1
                    for task
                    in state["tasks"]
                    if task["status"]
                    == "ACTIVE"
                ),
                "blocked": sum(
                    1
                    for task
                    in state["tasks"]
                    if task["status"]
                    == "BLOCKED"
                ),
                "waiting": sum(
                    1
                    for task
                    in state["tasks"]
                    if task["status"]
                    == "WAITING"
                ),
            },
            "shots": {
                "total": len(
                    state["shots"]
                ),
                "final": sum(
                    1
                    for shot
                    in state["shots"]
                    if shot["status"]
                    == "FINAL"
                ),
                "approved": sum(
                    1
                    for shot
                    in state["shots"]
                    if shot["status"]
                    == "APPROVED"
                ),
            },
            "assets": {
                "total": len(
                    state["assets"]
                ),
                "approved": sum(
                    1
                    for asset
                    in state["assets"]
                    if asset["status"]
                    == "APPROVED"
                ),
            },
            "open_blockers": [
                blocker
                for blocker
                in state["blockers"]
                if blocker["status"]
                != "RESOLVED"
            ],
            "pending_approvals": [
                approval
                for approval
                in state["approvals"]
                if approval["status"]
                != "APPROVED"
            ],
        }

    # ========================================================
    # AUDIT
    # ========================================================

    def audit_project(
        self,
        root: Path,
    ) -> Dict[str, Any]:

        state = self.load_state(
            root
        )

        issues = []
        warnings = []

        expected_folders = folders_for(
            state["project"][
                "complexity"
            ]
        )

        for folder in expected_folders:

            if not (
                root / folder
            ).exists():

                issues.append(
                    {
                        "type":
                            "MISSING_FOLDER",
                        "path":
                            folder,
                    }
                )

        collections = [
            "tasks",
            "shots",
            "assets",
            "characters",
            "locations",
            "dependencies",
            "blockers",
            "risks",
            "approvals",
            "decisions",
            "changes",
            "prompts",
            "generations",
        ]

        for collection in collections:

            seen = set()

            for item in (
                state.get(
                    collection,
                    [],
                )
            ):

                entity_id = item.get(
                    "id"
                )

                if entity_id in seen:

                    issues.append(
                        {
                            "type":
                                "DUPLICATE_ID",
                            "collection":
                                collection,
                            "id":
                                entity_id,
                        }
                    )

                seen.add(
                    entity_id
                )

        task_ids = {
            task["id"]
            for task
            in state["tasks"]
        }

        for task in state["tasks"]:

            for dependency in (
                task.get(
                    "dependencies",
                    [],
                )
            ):

                if dependency not in task_ids:

                    issues.append(
                        {
                            "type":
                                "BROKEN_DEPENDENCY",
                            "task":
                                task["id"],
                            "dependency":
                                dependency,
                        }
                    )

            if not task.get(
                "department"
            ):

                warnings.append(
                    {
                        "type":
                            "TASK_WITHOUT_DEPARTMENT",
                        "task":
                            task["id"],
                    }
                )

            if (
                task["status"]
                == "COMPLETE"
                and not task.get(
                    "completed"
                )
            ):

                warnings.append(
                    {
                        "type":
                            "COMPLETE_WITHOUT_TIMESTAMP",
                        "task":
                            task["id"],
                    }
                )

        for asset in state["assets"]:

            asset_path = asset.get(
                "path"
            )

            if not asset_path:
                continue

            candidate = Path(
                asset_path
            )

            if not candidate.is_absolute():
                candidate = (
                    root / candidate
                )

            if not candidate.exists():

                warnings.append(
                    {
                        "type":
                            "MISSING_ASSET_PATH",
                        "asset":
                            asset["id"],
                        "path":
                            asset_path,
                    }
                )

        result = {
            "engine_version":
                ENGINE_VERSION,
            "project":
                state["project"],
            "audit":
                (
                    "AUDIT_PASS"
                    if not issues
                    else
                    "AUDIT_FAIL"
                ),
            "issues":
                issues,
            "warnings":
                warnings,
            "timestamp":
                now_iso(),
        }

        report_path = (
            root
            / "20_qc"
            / "reports"
            / "automation_audit.json"
        )

        json_dump(
            result,
            report_path,
        )

        self.log_event(
            root,
            "PROJECT_AUDIT",
            state["project"]["id"],
            result,
        )

        return result

    # ========================================================
    # MANIFEST
    # ========================================================

    def build_manifest(
        self,
        root: Path,
        checksums: bool = False,
        max_checksum_mb: int = 100,
    ) -> Dict[str, Any]:

        excluded_dirs = {
            ".studio",
            "cache",
            "caches",
            "temp",
            "tmp",
            "preview",
            "previews",
            "proxies",
        }

        files = []

        max_checksum_bytes = (
            max_checksum_mb
            * 1024
            * 1024
        )

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            relative = Path(
                safe_rel(
                    path,
                    root,
                )
            )

            if (
                relative.parts
                and any(
                    part in excluded_dirs
                    for part
                    in relative.parts
                )
            ):
                continue

            item = {
                "path":
                    safe_rel(
                        path,
                        root,
                    ),
                "size":
                    path.stat().st_size,
                "modified":
                    dt.datetime.fromtimestamp(
                        path.stat().st_mtime,
                        tz=dt.timezone.utc,
                    ).astimezone().isoformat(
                        timespec="seconds"
                    ),
            }

            if (
                checksums
                and path.stat().st_size
                <= max_checksum_bytes
            ):

                item[
                    "sha256"
                ] = file_sha256(
                    path
                )

            files.append(
                item
            )

        files.sort(
            key=lambda item:
                item["path"]
        )

        manifest = {
            "project":
                root.parent.name,
            "generated":
                now_iso(),
            "engine_version":
                ENGINE_VERSION,
            "file_count":
                len(files),
            "total_bytes":
                sum(
                    item["size"]
                    for item
                    in files
                ),
            "checksums":
                checksums,
            "files":
                files,
        }

        archive_dir = (
            root
            / "24_archive"
            / "checksums"
        )

        archive_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        json_dump(
            manifest,
            archive_dir
            / "manifest.json",
        )

        self.log_event(
            root,
            "MANIFEST_CREATED",
            "manifest.json",
            {
                "file_count":
                    len(files),
            },
        )

        return manifest

    # ========================================================
    # BACKUP
    # ========================================================

    def backup_admin_state(
        self,
        root: Path,
    ) -> Path:

        timestamp = (
            dt.datetime.now()
            .strftime(
                "%Y%m%d_%H%M%S"
            )
        )

        destination = (
            root
            / "99_backup"
            / f"automation_backup_{timestamp}"
        )

        destination.mkdir(
            parents=True,
            exist_ok=False,
        )

        source = (
            root / "00_admin"
        )

        for path in source.rglob("*"):

            if not path.is_file():
                continue

            relative = path.relative_to(
                source
            )

            target = (
                destination
                / relative
            )

            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                path,
                target,
            )

        self.log_event(
            root,
            "ADMIN_BACKUP_CREATED",
            safe_rel(
                destination,
                root,
            ),
            {},
        )

        return destination

    # ========================================================
    # ARCHIVE
    # ========================================================

    def archive_project(
        self,
        root: Path,
        include_media: bool = False,
    ) -> Path:

        project_id = (
            root.parent.name
        )

        archive_dir = (
            root
            / "24_archive"
        )

        archive_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = (
            dt.datetime.now()
            .strftime(
                "%Y%m%d_%H%M%S"
            )
        )

        archive_path = (
            archive_dir
            / (
                f"{project_id}_archive_"
                f"{timestamp}.zip"
            )
        )

        excluded_dirs = {
            ".studio",
            "cache",
            "caches",
            "temp",
            "tmp",
            "preview",
            "previews",
            "proxies",
        }

        with zipfile.ZipFile(
            archive_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=6,
        ) as archive:

            for path in root.rglob("*"):

                if not path.is_file():
                    continue

                if (
                    path.resolve()
                    == archive_path.resolve()
                ):
                    continue

                relative = Path(
                    safe_rel(
                        path,
                        root,
                    )
                )

                if any(
                    part in excluded_dirs
                    for part
                    in relative.parts
                ):
                    continue

                if (
                    not include_media
                    and path.suffix.lower()
                    in LARGE_MEDIA_EXTENSIONS
                ):
                    continue

                archive.write(
                    path,
                    arcname=str(
                        relative
                    ).replace(
                        "\\",
                        "/",
                    ),
                )

        self.log_event(
            root,
            "ARCHIVE_CREATED",
            safe_rel(
                archive_path,
                root,
            ),
            {
                "include_media":
                    include_media,
            },
        )

        return archive_path

    # ========================================================
    # WORKFLOW ENGINE
    # ========================================================

    def resolve_env(
        self,
        value: Any,
    ) -> Any:

        if isinstance(
            value,
            str,
        ):

            pattern = re.compile(
                r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"
            )

            return pattern.sub(
                lambda match:
                    os.environ.get(
                        match.group(1),
                        match.group(0),
                    ),
                value,
            )

        if isinstance(
            value,
            list,
        ):

            return [
                self.resolve_env(
                    item
                )
                for item
                in value
            ]

        if isinstance(
            value,
            dict,
        ):

            return {
                key:
                    self.resolve_env(
                        value
                    )
                for key,
                value
                in value.items()
            }

        return value

    def resolve_workflow_value(
        self,
        value: Any,
        root: Path,
        state: Dict[str, Any],
    ) -> Any:

        value = self.resolve_env(
            value
        )

        if isinstance(
            value,
            str,
        ):

            replacements = {
                "{{PROJECT_ROOT}}":
                    str(root),
                "{{REPO_ROOT}}":
                    str(self.repo_root),
                "{{PROJECT_ID}}":
                    state["project"]["id"],
                "{{PROJECT_TITLE}}":
                    state["project"]["title"],
                "{{PROJECT_SLUG}}":
                    state["project"]["slug"],
                "{{DATE}}":
                    today_iso(),
                "{{NOW}}":
                    now_iso(),
            }

            for token, replacement in (
                replacements.items()
            ):

                value = value.replace(
                    token,
                    replacement,
                )

        elif isinstance(
            value,
            list,
        ):

            value = [
                self.resolve_workflow_value(
                    item,
                    root,
                    state,
                )
                for item
                in value
            ]

        elif isinstance(
            value,
            dict,
        ):

            value = {
                key:
                    self.resolve_workflow_value(
                        item,
                        root,
                        state,
                    )
                for key, item
                in value.items()
            }

        return value

    def load_workflow(
        self,
        path: Path,
    ) -> Dict[str, Any]:

        workflow = json_load(
            path
        )

        if not isinstance(
            workflow,
            dict,
        ):
            raise ValueError(
                "Workflow must be a JSON object."
            )

        if not isinstance(
            workflow.get("steps"),
            list,
        ):
            raise ValueError(
                "Workflow must contain a steps list."
            )

        for step in workflow["steps"]:

            step_type = step.get(
                "type"
            )

            if step_type not in (
                WORKFLOW_STEP_TYPES
            ):
                raise ValueError(
                    f"Unsupported workflow step type: "
                    f"{step_type}"
                )

        return workflow

    def execute_step(
        self,
        root: Path,
        state: Dict[str, Any],
        step: Dict[str, Any],
        execute: bool,
        allow_shell: bool,
    ) -> Dict[str, Any]:

        step_type = step.get(
            "type"
        )

        name = step.get(
            "name",
            step_type,
        )

        if step_type == "mkdir":

            raw_path = (
                self.resolve_workflow_value(
                    step["path"],
                    root,
                    state,
                )
            )

            path = Path(
                raw_path
            )

            result = {
                "type":
                    step_type,
                "path":
                    str(path),
                "status":
                    "DRY_RUN",
            }

            if execute:

                path.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                result[
                    "status"
                ] = "SUCCESS"

            return result

        if step_type == "write_text":

            raw_path = (
                self.resolve_workflow_value(
                    step["path"],
                    root,
                    state,
                )
            )

            path = Path(
                raw_path
            )

            if not path.is_absolute():
                path = (
                    root / path
                )

            content = (
                self.resolve_workflow_value(
                    step.get(
                        "content",
                        "",
                    ),
                    root,
                    state,
                )
            )

            result = {
                "type":
                    step_type,
                "path":
                    str(path),
                "status":
                    "DRY_RUN",
            }

            if execute:

                write_text(
                    path,
                    str(content),
                    overwrite=bool(
                        step.get(
                            "overwrite",
                            False,
                        )
                    ),
                )

                result[
                    "status"
                ] = "SUCCESS"

            return result

        if step_type in {
            "copy",
            "move",
        }:

            source = Path(
                self.resolve_workflow_value(
                    step["source"],
                    root,
                    state,
                )
            )

            destination = Path(
                self.resolve_workflow_value(
                    step["destination"],
                    root,
                    state,
                )
            )

            if not source.is_absolute():
                source = (
                    root / source
                )

            if not destination.is_absolute():
                destination = (
                    root / destination
                )

            result = {
                "type":
                    step_type,
                "source":
                    str(source),
                "destination":
                    str(destination),
                "status":
                    "DRY_RUN",
            }

            if execute:

                if not source.exists():
                    raise FileNotFoundError(
                        f"Source not found: {source}"
                    )

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                if step_type == "copy":

                    shutil.copy2(
                        source,
                        destination,
                    )

                else:

                    shutil.move(
                        str(source),
                        str(destination),
                    )

                result[
                    "status"
                ] = "SUCCESS"

            return result

        if step_type == "checksum":

            path = Path(
                self.resolve_workflow_value(
                    step["path"],
                    root,
                    state,
                )
            )

            if not path.is_absolute():
                path = root / path

            result = {
                "type":
                    step_type,
                "path":
                    str(path),
                "status":
                    "DRY_RUN",
            }

            if execute:

                if not path.exists():
                    raise FileNotFoundError(
                        f"File not found: {path}"
                    )

                result[
                    "sha256"
                ] = file_sha256(
                    path
                )

                result[
                    "status"
                ] = "SUCCESS"

            return result

        if step_type == "manifest":

            result = {
                "type":
                    step_type,
                "status":
                    "DRY_RUN",
            }

            if execute:

                manifest = (
                    self.build_manifest(
                        root,
                        checksums=bool(
                            step.get(
                                "checksums",
                                False,
                            )
                        ),
                        max_checksum_mb=int(
                            step.get(
                                "max_checksum_mb",
                                100,
                            )
                        ),
                    )
                )

                result.update(
                    {
                        "status":
                            "SUCCESS",
                        "file_count":
                            manifest[
                                "file_count"
                            ],
                    }
                )

            return result

        if step_type in {
            "command",
            "python",
        }:

            args = (
                self.resolve_workflow_value(
                    step.get(
                        "args",
                        [],
                    ),
                    root,
                    state,
                )
            )

            if not isinstance(
                args,
                list,
            ) or not args:

                raise ValueError(
                    f"Step '{name}' requires an args list."
                )

            if step_type == "python":

                args = [
                    sys.executable
                ] + [
                    str(item)
                    for item
                    in args
                ]

            else:

                args = [
                    str(item)
                    for item
                    in args
                ]

            result = {
                "type":
                    step_type,
                "command":
                    args,
                "status":
                    "DRY_RUN",
            }

            if not execute:
                return result

            completed = subprocess.run(
                args,
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

            result.update(
                {
                    "status":
                        (
                            "SUCCESS"
                            if completed.returncode
                            == 0
                            else "FAILED"
                        ),
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
                }
            )

            if completed.returncode != 0:
                raise RuntimeError(
                    "Command failed: "
                    + " ".join(args)
                )

            return result

        if step_type == "shell":

            if not allow_shell:
                raise RuntimeError(
                    "Shell steps require "
                    "--allow-shell."
                )

            command = (
                self.resolve_workflow_value(
                    step.get(
                        "command",
                        "",
                    ),
                    root,
                    state,
                )
            )

            if not command:
                raise ValueError(
                    "Shell step requires a command."
                )

            result = {
                "type":
                    "shell",
                "command":
                    command,
                "status":
                    "DRY_RUN",
            }

            if not execute:
                return result

            completed = subprocess.run(
                command,
                cwd=root,
                shell=True,
                capture_output=True,
                text=True,
                check=False,
            )

            result.update(
                {
                    "status":
                        (
                            "SUCCESS"
                            if completed.returncode
                            == 0
                            else "FAILED"
                        ),
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
                }
            )

            if completed.returncode != 0:
                raise RuntimeError(
                    f"Shell workflow failed: {command}"
                )

            return result

        if step_type == "http":

            url = (
                self.resolve_workflow_value(
                    step["url"],
                    root,
                    state,
                )
            )

            method = (
                str(
                    step.get(
                        "method",
                        "GET",
                    )
                )
                .upper()
            )

            headers = (
                self.resolve_workflow_value(
                    step.get(
                        "headers",
                        {},
                    ),
                    root,
                    state,
                )
            )

            body = (
                self.resolve_workflow_value(
                    step.get(
                        "body"
                    ),
                    root,
                    state,
                )
            )

            result = {
                "type":
                    "http",
                "method":
                    method,
                "url":
                    url,
                "status":
                    "DRY_RUN",
            }

            if not execute:
                return result

            data = None

            if body is not None:

                if isinstance(
                    body,
                    (
                        dict,
                        list,
                    ),
                ):

                    data = json.dumps(
                        body
                    ).encode(
                        "utf-8"
                    )

                    headers = {
                        "Content-Type":
                            "application/json",
                        **headers,
                    }

                else:

                    data = str(
                        body
                    ).encode(
                        "utf-8"
                    )

            request = urllib.request.Request(
                url,
                data=data,
                headers=headers,
                method=method,
            )

            timeout = float(
                step.get(
                    "timeout",
                    60,
                )
            )

            try:

                with urllib.request.urlopen(
                    request,
                    timeout=timeout,
                ) as response:

                    payload = (
                        response
                        .read()
                        .decode(
                            "utf-8",
                            errors="replace",
                        )
                    )

                    result.update(
                        {
                            "status":
                                "SUCCESS",
                            "http_status":
                                response.status,
                            "response":
                                payload[
                                    -20000:
                                ],
                        }
                    )

            except urllib.error.HTTPError as exc:

                payload = (
                    exc.read()
                    .decode(
                        "utf-8",
                        errors="replace",
                    )
                )

                raise RuntimeError(
                    f"HTTP error {exc.code}: "
                    f"{payload[-2000:]}"
                ) from exc

            return result

        if step_type == "sleep":

            seconds = float(
                step.get(
                    "seconds",
                    1,
                )
            )

            result = {
                "type":
                    "sleep",
                "seconds":
                    seconds,
                "status":
                    "DRY_RUN",
            }

            if execute:

                time.sleep(
                    seconds
                )

                result[
                    "status"
                ] = "SUCCESS"

            return result

        raise ValueError(
            f"Unhandled workflow step: "
            f"{step_type}"
        )

    def run_workflow(
        self,
        root: Path,
        workflow_path: Path,
        execute: bool,
        allow_shell: bool,
    ) -> Dict[str, Any]:

        workflow = self.load_workflow(
            workflow_path
        )

        state = self.load_state(
            root
        )

        run_id = self.next_entity_id(
            state["workflow_runs"],
            "RUN",
        )

        started = now_iso()

        results = []

        for index, step in enumerate(
            workflow["steps"],
            start=1,
        ):

            result = (
                self.execute_step(
                    root,
                    state,
                    step,
                    execute,
                    allow_shell,
                )
            )

            result["index"] = index

            result["name"] = step.get(
                "name",
                f"step-{index}",
            )

            results.append(
                result
            )

        report = {
            "run_id":
                run_id,
            "workflow_id":
                workflow.get(
                    "id"
                ),
            "workflow_name":
                workflow.get(
                    "name"
                ),
            "workflow_version":
                workflow.get(
                    "version"
                ),
            "project":
                state["project"]["id"],
            "started":
                started,
            "ended":
                now_iso(),
            "mode":
                (
                    "EXECUTE"
                    if execute
                    else "DRY_RUN"
                ),
            "results":
                results,
        }

        state["workflow_runs"].append(
            {
                "id":
                    run_id,
                "workflow_id":
                    workflow.get(
                        "id"
                    ),
                "mode":
                    report["mode"],
                "started":
                    started,
                "ended":
                    report["ended"],
                "status":
                    "COMPLETE",
            }
        )

        self.save_state(
            root,
            state,
        )

        run_dir = (
            self.state_dir(root)
            / "workflow_runs"
        )

        run_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        json_dump(
            report,
            run_dir
            / f"{run_id}.json",
        )

        self.log_event(
            root,
            "WORKFLOW_RUN",
            workflow.get(
                "id"
            ),
            {
                "run_id":
                    run_id,
                "mode":
                    report["mode"],
            },
        )

        return report

    # ========================================================
    # QUEUE ENGINE
    # ========================================================

    def load_queue(
        self,
        root: Path,
    ) -> List[Dict[str, Any]]:

        queue = json_load(
            self.queue_path(root),
            [],
        )

        if not isinstance(
            queue,
            list,
        ):
            raise RuntimeError(
                "Queue must be a JSON list."
            )

        return queue

    def save_queue(
        self,
        root: Path,
        queue: List[Dict[str, Any]],
    ) -> None:

        json_dump(
            queue,
            self.queue_path(root),
        )

    def queue_add(
        self,
        root: Path,
        action: str,
        payload: Dict[str, Any],
        priority: str,
    ) -> Dict[str, Any]:

        priority = priority.upper()

        if priority not in PRIORITIES:
            raise ValueError(
                "Invalid queue priority."
            )

        queue = self.load_queue(
            root
        )

        job_number = (
            len(queue)
            + 1
        )

        job_id = (
            f"JOB_{job_number:05d}"
        )

        job = {
            "id": job_id,
            "action": action,
            "payload": payload,
            "priority": priority,
            "status": "QUEUED",
            "created": now_iso(),
            "started": None,
            "completed": None,
            "error": None,
        }

        queue.append(
            job
        )

        self.save_queue(
            root,
            queue,
        )

        self.log_event(
            root,
            "JOB_QUEUED",
            job_id,
            job,
        )

        return job

    def queue_run(
        self,
        root: Path,
        execute: bool,
        allow_shell: bool,
    ) -> List[Dict[str, Any]]:

        queue = self.load_queue(
            root
        )

        rank = {
            "P0": 0,
            "P1": 1,
            "P2": 2,
            "P3": 3,
        }

        queue.sort(
            key=lambda job: (
                rank.get(
                    job.get(
                        "priority",
                        "P3",
                    ),
                    9,
                ),
                job.get(
                    "created",
                    "",
                ),
            )
        )

        results = []

        for job in queue:

            if job["status"] not in {
                "QUEUED",
                "FAILED",
            }:
                continue

            if not execute:

                results.append(
                    {
                        **job,
                        "preview":
                            True,
                    }
                )

                continue

            job["started"] = now_iso()
            job["status"] = "RUNNING"

            self.save_queue(
                root,
                queue,
            )

            try:

                action = job["action"]
                payload = job["payload"]

                if action == "workflow":

                    workflow_path = Path(
                        payload[
                            "workflow"
                        ]
                    )

                    if not workflow_path.is_absolute():

                        workflow_path = (
                            self.repo_root
                            / workflow_path
                        )

                    result = (
                        self.run_workflow(
                            root,
                            workflow_path,
                            execute=True,
                            allow_shell=allow_shell,
                        )
                    )

                elif action == "manifest":

                    result = (
                        self.build_manifest(
                            root,
                            checksums=bool(
                                payload.get(
                                    "checksums",
                                    False,
                                )
                            ),
                        )
                    )

                elif action == "audit":

                    result = (
                        self.audit_project(
                            root
                        )
                    )

                elif action == "backup":

                    result = {
                        "path":
                            str(
                                self.backup_admin_state(
                                    root
                                )
                            )
                    }

                elif action == "archive":

                    result = {
                        "path":
                            str(
                                self.archive_project(
                                    root,
                                    include_media=bool(
                                        payload.get(
                                            "include_media",
                                            False,
                                        )
                                    ),
                                )
                            )
                    }

                else:

                    raise ValueError(
                        f"Unknown queue action: "
                        f"{action}"
                    )

                job[
                    "status"
                ] = "COMPLETE"

                job[
                    "completed"
                ] = now_iso()

                job[
                    "result"
                ] = result

            except Exception as exc:

                job[
                    "status"
                ] = "FAILED"

                job[
                    "error"
                ] = str(exc)

            results.append(
                dict(job)
            )

            self.save_queue(
                root,
                queue,
            )

        return results

    # ========================================================
    # DIAGNOSTICS
    # ========================================================

    def doctor(
        self,
    ) -> Dict[str, Any]:

        checks = []

        def add_check(
            name: str,
            ok: bool,
            detail: str,
        ):

            checks.append(
                {
                    "name":
                        name,
                    "ok":
                        ok,
                    "detail":
                        detail,
                }
            )

        add_check(
            "Python",
            sys.version_info
            >= (3, 10),
            sys.version.split()[0],
        )

        add_check(
            "Repository Root",
            self.repo_root.exists(),
            str(
                self.repo_root
            ),
        )

        add_check(
            "Studio Directory",
            (
                self.repo_root
                / "studio"
            ).exists(),
            str(
                self.repo_root
                / "studio"
            ),
        )

        add_check(
            "Scripts Directory",
            self.scripts_root.exists(),
            str(
                self.scripts_root
            ),
        )

        add_check(
            "Projects Directory",
            self.projects_root.exists(),
            str(
                self.projects_root
            ),
        )

        add_check(
            "Git",
            shutil.which(
                "git"
            )
            is not None,
            (
                shutil.which(
                    "git"
                )
                or "not found"
            ),
        )

        add_check(
            "FFmpeg",
            shutil.which(
                "ffmpeg"
            )
            is not None,
            (
                shutil.which(
                    "ffmpeg"
                )
                or "not found (optional)"
            ),
        )

        add_check(
            "FFprobe",
            shutil.which(
                "ffprobe"
            )
            is not None,
            (
                shutil.which(
                    "ffprobe"
                )
                or "not found (optional)"
            ),
        )

        return {
            "engine_version":
                ENGINE_VERSION,
            "timestamp":
                now_iso(),
            "checks":
                checks,
            "status":
                (
                    "PASS"
                    if all(
                        item["ok"]
                        for item
                        in checks[:5]
                    )
                    else "FAIL"
                ),
        }


# ============================================================
# CLI
# ============================================================

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="create_project.py",
        description=(
            "AI Film Studio "
            "Complete Automation Engine"
        ),
    )

    sub = (
        parser.add_subparsers(
            dest="command",
            required=True,
        )
    )

    # --------------------------------------------------------
    # INIT
    # --------------------------------------------------------

    p = sub.add_parser(
        "init",
        help="Create a new project.",
    )

    p.add_argument(
        "--title",
        required=True,
    )

    p.add_argument(
        "--type",
        dest="project_type",
        required=True,
    )

    p.add_argument(
        "--runtime",
        default="",
    )

    p.add_argument(
        "--aspect",
        default="16:9",
    )

    p.add_argument(
        "--resolution",
        default="1920x1080",
    )

    p.add_argument(
        "--fps",
        default="24",
    )

    p.add_argument(
        "--complexity",
        choices=sorted(
            COMPLEXITIES
        ),
    )

    p.add_argument(
        "--year",
        type=int,
    )

    p.add_argument(
        "--number",
    )

    # --------------------------------------------------------
    # SIMPLE PROJECT COMMANDS
    # --------------------------------------------------------

    for command in [
        "status",
        "next",
        "audit",
        "report",
        "manifest",
        "backup",
        "archive",
    ]:

        p = sub.add_parser(
            command
        )

        p.add_argument(
            "project_id"
        )

        p.add_argument(
            "slug"
        )

        if command == "manifest":

            p.add_argument(
                "--checksums",
                action="store_true",
            )

            p.add_argument(
                "--max-checksum-mb",
                type=int,
                default=100,
            )

        if command in {
            "backup",
            "archive",
        }:

            p.add_argument(
                "--execute",
                action="store_true",
            )

        if command == "archive":

            p.add_argument(
                "--include-media",
                action="store_true",
            )

        if command == "report":

            p.add_argument(
                "--output"
            )

    # --------------------------------------------------------
    # TASK ADD
    # --------------------------------------------------------

    p = sub.add_parser(
        "task-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--name",
        required=True,
    )

    p.add_argument(
        "--department",
        required=True,
    )

    p.add_argument(
        "--priority",
        default="P2",
    )

    p.add_argument(
        "--phase",
        default="",
    )

    p.add_argument(
        "--owner",
    )

    p.add_argument(
        "--depends-on",
        default="",
    )

    p.add_argument(
        "--description",
        default="",
    )

    # --------------------------------------------------------
    # TASK UPDATE
    # --------------------------------------------------------

    p = sub.add_parser(
        "task-update"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "task_id"
    )

    p.add_argument(
        "--status"
    )

    p.add_argument(
        "--owner"
    )

    p.add_argument(
        "--priority"
    )

    p.add_argument(
        "--department"
    )

    p.add_argument(
        "--phase"
    )

    p.add_argument(
        "--name"
    )

    p.add_argument(
        "--version"
    )

    # --------------------------------------------------------
    # SHOT
    # --------------------------------------------------------

    p = sub.add_parser(
        "shot-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--name",
        required=True,
    )

    p.add_argument(
        "--sequence",
        default="",
    )

    p.add_argument(
        "--scene",
        default="",
    )

    p.add_argument(
        "--purpose",
        default="",
    )

    p.add_argument(
        "--location",
        default="",
    )

    p.add_argument(
        "--camera",
        default="",
    )

    p.add_argument(
        "--characters",
        default="",
    )

    p.add_argument(
        "--ai",
        action="store_true",
    )

    p.add_argument(
        "--vfx",
        action="store_true",
    )

    # --------------------------------------------------------
    # ASSET
    # --------------------------------------------------------

    p = sub.add_parser(
        "asset-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--name",
        required=True,
    )

    p.add_argument(
        "--type",
        dest="asset_type",
        required=True,
    )

    p.add_argument(
        "--department",
        required=True,
    )

    p.add_argument(
        "--path",
        required=True,
    )

    p.add_argument(
        "--status",
        default="PLANNED",
    )

    p.add_argument(
        "--rights",
        default="UNKNOWN",
    )

    p.add_argument(
        "--qc",
        default="NOT_REVIEWED",
    )

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    p = sub.add_parser(
        "prompt-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--purpose",
        required=True,
    )

    p.add_argument(
        "--prompt",
        dest="prompt_text",
        required=True,
    )

    p.add_argument(
        "--department",
        default="AI Generation",
    )

    p.add_argument(
        "--model",
        default="",
    )

    p.add_argument(
        "--entity-id"
    )

    p.add_argument(
        "--negative",
        default="",
    )

    p.add_argument(
        "--references",
        default="",
    )

    # --------------------------------------------------------
    # GENERATION
    # --------------------------------------------------------

    p = sub.add_parser(
        "generation-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--prompt-id",
        required=True,
    )

    p.add_argument(
        "--model",
        required=True,
    )

    p.add_argument(
        "--output",
        required=True,
    )

    p.add_argument(
        "--selected",
        action="store_true",
    )

    p.add_argument(
        "--qc",
        default="NOT_REVIEWED",
    )

    # --------------------------------------------------------
    # BLOCKER
    # --------------------------------------------------------

    p = sub.add_parser(
        "blocker-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--description",
        required=True,
    )

    p.add_argument(
        "--department",
        required=True,
    )

    p.add_argument(
        "--severity",
        default="HIGH",
    )

    p.add_argument(
        "--task-id",
    )

    p.add_argument(
        "--owner",
    )

    p.add_argument(
        "--resolution",
        default="",
    )

    # --------------------------------------------------------
    # BLOCKER RESOLVE
    # --------------------------------------------------------

    p = sub.add_parser(
        "blocker-resolve"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "blocker_id"
    )

    p.add_argument(
        "--note",
        default="",
    )

    # --------------------------------------------------------
    # APPROVAL
    # --------------------------------------------------------

    p = sub.add_parser(
        "approval-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--gate",
        required=True,
    )

    p.add_argument(
        "--entity",
        default="",
    )

    p.add_argument(
        "--version",
        default=DEFAULT_VERSION,
    )

    p.add_argument(
        "--reviewer"
    )

    p.add_argument(
        "--status",
        default="READY_FOR_REVIEW",
    )

    p.add_argument(
        "--comments",
        default="",
    )

    p = sub.add_parser(
        "approval-update"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "approval_id"
    )

    p.add_argument(
        "--status",
        required=True,
    )

    p.add_argument(
        "--comments",
        default="",
    )

    # --------------------------------------------------------
    # DECISION
    # --------------------------------------------------------

    p = sub.add_parser(
        "decision-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--decision",
        required=True,
    )

    p.add_argument(
        "--reason",
        required=True,
    )

    p.add_argument(
        "--owner",
    )

    p.add_argument(
        "--affected",
        default="",
    )

    # --------------------------------------------------------
    # CHANGE
    # --------------------------------------------------------

    p = sub.add_parser(
        "change-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--entity",
        required=True,
    )

    p.add_argument(
        "--change",
        required=True,
    )

    p.add_argument(
        "--impact",
        default="",
    )

    p.add_argument(
        "--approval",
        default="PENDING",
    )

    p.add_argument(
        "--status",
        default="REQUESTED",
    )

    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    p = sub.add_parser(
        "workflow-run"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--workflow",
        required=True,
    )

    p.add_argument(
        "--execute",
        action="store_true",
    )

    p.add_argument(
        "--allow-shell",
        action="store_true",
    )

    # --------------------------------------------------------
    # QUEUE ADD
    # --------------------------------------------------------

    p = sub.add_parser(
        "queue-add"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--action",
        required=True,
        choices=[
            "workflow",
            "manifest",
            "audit",
            "backup",
            "archive",
        ],
    )

    p.add_argument(
        "--workflow"
    )

    p.add_argument(
        "--priority",
        default="P2",
    )

    p.add_argument(
        "--checksums",
        action="store_true",
    )

    p.add_argument(
        "--include-media",
        action="store_true",
    )

    # --------------------------------------------------------
    # QUEUE RUN
    # --------------------------------------------------------

    p = sub.add_parser(
        "queue-run"
    )

    p.add_argument(
        "project_id"
    )

    p.add_argument(
        "slug"
    )

    p.add_argument(
        "--execute",
        action="store_true",
    )

    p.add_argument(
        "--allow-shell",
        action="store_true",
    )

    # --------------------------------------------------------
    # DOCTOR
    # --------------------------------------------------------

    sub.add_parser(
        "doctor"
    )

    return parser


# ============================================================
# CLI EXECUTION
# ============================================================

def main(
    argv: Optional[List[str]] = None,
) -> int:

    parser = build_parser()

    args = parser.parse_args(
        argv
    )

    engine = StudioEngine()

    try:

        # ----------------------------------------------------
        # INIT
        # ----------------------------------------------------

        if args.command == "init":

            root = (
                engine.create_project(
                    title=args.title,
                    project_type=args.project_type,
                    runtime=args.runtime,
                    aspect=args.aspect,
                    resolution=args.resolution,
                    fps=args.fps,
                    complexity=args.complexity,
                    year=args.year,
                    number=args.number,
                )
            )

            state = (
                engine.load_state(root)
            )

            print()
            print(
                "=" * 60
            )
            print(
                "AI FILM STUDIO PROJECT CREATED"
            )
            print(
                "=" * 60
            )
            print(
                f"Project ID : "
                f"{state['project']['id']}"
            )
            print(
                f"Title      : "
                f"{state['project']['title']}"
            )
            print(
                f"Type       : "
                f"{state['project']['type']}"
            )
            print(
                f"Complexity : "
                f"{state['project']['complexity']}"
            )
            print(
                f"Location   : "
                f"{root}"
            )
            print(
                "=" * 60
            )
            print()

            return 0

        # ----------------------------------------------------
        # DOCTOR
        # ----------------------------------------------------

        if args.command == "doctor":

            print(
                json.dumps(
                    engine.doctor(),
                    indent=2,
                )
            )

            return 0

        # ----------------------------------------------------
        # PROJECT LOAD
        # ----------------------------------------------------

        root = (
            engine.require_project(
                args.project_id,
                args.slug,
            )
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if args.command == "status":

            print(
                json.dumps(
                    engine.status_report(
                        root
                    ),
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # NEXT
        # ----------------------------------------------------

        if args.command == "next":

            state = (
                engine.recalculate_state(
                    root
                )
            )

            next_task = (
                engine.calculate_next_task(
                    state
                )
            )

            result = {
                "project":
                    state["project"],
                "current_state":
                    state["state"],
                "next_task":
                    next_task,
                "reason":
                    state["state"][
                        "next_action"
                    ],
            }

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # AUDIT
        # ----------------------------------------------------

        if args.command == "audit":

            print(
                json.dumps(
                    engine.audit_project(
                        root
                    ),
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # REPORT
        # ----------------------------------------------------

        if args.command == "report":

            report = (
                engine.status_report(
                    root
                )
            )

            state = (
                engine.load_state(
                    root
                )
            )

            engine.sync_all(
                root,
                state,
            )

            if args.output:

                output = Path(
                    args.output
                )

                if not output.is_absolute():
                    output = (
                        root / output
                    )

                json_dump(
                    report,
                    output,
                )

                print(
                    f"REPORT WRITTEN: {output}"
                )

            else:

                print(
                    json.dumps(
                        report,
                        indent=2,
                        ensure_ascii=False,
                    )
                )

            return 0

        # ----------------------------------------------------
        # MANIFEST
        # ----------------------------------------------------

        if args.command == "manifest":

            print(
                json.dumps(
                    engine.build_manifest(
                        root,
                        checksums=args.checksums,
                        max_checksum_mb=(
                            args.max_checksum_mb
                        ),
                    ),
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # BACKUP
        # ----------------------------------------------------

        if args.command == "backup":

            if not args.execute:

                print(
                    json.dumps(
                        {
                            "status":
                                "DRY_RUN",
                            "action":
                                "backup admin state",
                        },
                        indent=2,
                    )
                )

            else:

                print(
                    "BACKUP: "
                    + str(
                        engine.backup_admin_state(
                            root
                        )
                    )
                )

            return 0

        # ----------------------------------------------------
        # ARCHIVE
        # ----------------------------------------------------

        if args.command == "archive":

            if not args.execute:

                print(
                    json.dumps(
                        {
                            "status":
                                "DRY_RUN",
                            "action":
                                "archive project",
                            "include_media":
                                args.include_media,
                        },
                        indent=2,
                    )
                )

            else:

                print(
                    "ARCHIVE: "
                    + str(
                        engine.archive_project(
                            root,
                            include_media=(
                                args.include_media
                            ),
                        )
                    )
                )

            return 0

        # ----------------------------------------------------
        # TASK ADD
        # ----------------------------------------------------

        if args.command == "task-add":

            result = (
                engine.add_task(
                    root,
                    name=args.name,
                    department=args.department,
                    priority=args.priority,
                    phase=args.phase,
                    owner=args.owner,
                    dependencies=parse_csv(
                        args.depends_on
                    ),
                    description=args.description,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # TASK UPDATE
        # ----------------------------------------------------

        if args.command == "task-update":

            updates = {
                "status":
                    (
                        args.status.upper()
                        if args.status
                        else None
                    ),
                "owner":
                    args.owner,
                "priority":
                    (
                        args.priority.upper()
                        if args.priority
                        else None
                    ),
                "department":
                    args.department,
                "phase":
                    args.phase,
                "name":
                    args.name,
                "version":
                    args.version,
            }

            result = (
                engine.update_task(
                    root,
                    args.task_id,
                    **updates,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # SHOT ADD
        # ----------------------------------------------------

        if args.command == "shot-add":

            result = (
                engine.add_shot(
                    root,
                    name=args.name,
                    sequence=args.sequence,
                    scene=args.scene,
                    purpose=args.purpose,
                    location=args.location,
                    camera=args.camera,
                    characters=parse_csv(
                        args.characters
                    ),
                    ai=args.ai,
                    vfx=args.vfx,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # ASSET ADD
        # ----------------------------------------------------

        if args.command == "asset-add":

            result = (
                engine.add_asset(
                    root,
                    name=args.name,
                    asset_type=args.asset_type,
                    department=args.department,
                    path=args.path,
                    status=args.status,
                    rights=args.rights,
                    qc=args.qc,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # PROMPT ADD
        # ----------------------------------------------------

        if args.command == "prompt-add":

            result = (
                engine.add_prompt(
                    root,
                    purpose=args.purpose,
                    prompt_text=args.prompt_text,
                    department=args.department,
                    model=args.model,
                    entity_id=args.entity_id,
                    negative=args.negative,
                    references=parse_csv(
                        args.references
                    ),
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # GENERATION ADD
        # ----------------------------------------------------

        if args.command == "generation-add":

            result = (
                engine.add_generation(
                    root,
                    prompt_id=args.prompt_id,
                    model=args.model,
                    output=args.output,
                    selected=args.selected,
                    qc=args.qc,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # BLOCKER ADD
        # ----------------------------------------------------

        if args.command == "blocker-add":

            result = (
                engine.add_blocker(
                    root,
                    description=args.description,
                    department=args.department,
                    severity=args.severity,
                    task_id=args.task_id,
                    owner=args.owner,
                    resolution=args.resolution,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # BLOCKER RESOLVE
        # ----------------------------------------------------

        if args.command == "blocker-resolve":

            result = (
                engine.resolve_blocker(
                    root,
                    args.blocker_id,
                    args.note,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # APPROVAL ADD
        # ----------------------------------------------------

        if args.command == "approval-add":

            result = (
                engine.add_approval(
                    root,
                    gate=args.gate,
                    entity=args.entity,
                    version=args.version,
                    reviewer=args.reviewer,
                    status=args.status,
                    comments=args.comments,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # APPROVAL UPDATE
        # ----------------------------------------------------

        if args.command == "approval-update":

            result = (
                engine.set_approval(
                    root,
                    args.approval_id,
                    args.status,
                    args.comments,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # DECISION
        # ----------------------------------------------------

        if args.command == "decision-add":

            result = (
                engine.add_decision(
                    root,
                    decision=args.decision,
                    reason=args.reason,
                    owner=args.owner,
                    affected=parse_csv(
                        args.affected
                    ),
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # CHANGE
        # ----------------------------------------------------

        if args.command == "change-add":

            result = (
                engine.add_change(
                    root,
                    entity=args.entity,
                    change=args.change,
                    impact=args.impact,
                    approval=args.approval,
                    status=args.status,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # WORKFLOW RUN
        # ----------------------------------------------------

        if args.command == "workflow-run":

            workflow_path = Path(
                args.workflow
            )

            if not workflow_path.is_absolute():

                workflow_path = (
                    engine.repo_root
                    / workflow_path
                )

            result = (
                engine.run_workflow(
                    root,
                    workflow_path,
                    execute=args.execute,
                    allow_shell=args.allow_shell,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # QUEUE ADD
        # ----------------------------------------------------

        if args.command == "queue-add":

            payload = {}

            if args.action == "workflow":

                if not args.workflow:
                    raise ValueError(
                        "--workflow is required "
                        "for workflow queue jobs."
                    )

                payload[
                    "workflow"
                ] = args.workflow

            elif args.action == "manifest":

                payload[
                    "checksums"
                ] = args.checksums

            elif args.action == "archive":

                payload[
                    "include_media"
                ] = args.include_media

            result = (
                engine.queue_add(
                    root,
                    action=args.action,
                    payload=payload,
                    priority=args.priority,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        # ----------------------------------------------------
        # QUEUE RUN
        # ----------------------------------------------------

        if args.command == "queue-run":

            result = (
                engine.queue_run(
                    root,
                    execute=args.execute,
                    allow_shell=args.allow_shell,
                )
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            return 0

        parser.error(
            "Unknown command."
        )

        return 2

    except KeyboardInterrupt:

        print(
            "Interrupted.",
            file=sys.stderr,
        )

        return 130

    except Exception as exc:

        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )

        if os.environ.get(
            "STUDIO_DEBUG"
        ) == "1":

            traceback.print_exc()

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
