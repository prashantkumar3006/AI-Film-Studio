# AI FILM STUDIO INDEX

## 1. PURPOSE

This file is the master navigation map for the AI Film Studio repository.

It tells Claude:

- where each system lives
- which file controls which responsibility
- which department should handle a request
- where project information should be stored
- where templates and schemas are defined
- how the studio documentation is connected
- which document should be consulted first

This is an index and routing layer.

It is not intended to duplicate the detailed content of other files.

---

# 2. MASTER STUDIO ARCHITECTURE

The studio is organized into five layers:

LAYER 1
MASTER OPERATING SYSTEM

LAYER 2
SPECIALIST DEPARTMENTS

LAYER 3
STUDIO CONTROL SYSTEMS

LAYER 4
PROJECT SYSTEMS

LAYER 5
TOOLS / EXECUTION / MEDIA

The conceptual hierarchy is:

CLAUDE.md

↓

DEPARTMENT SKILLS

↓

CONTROL SYSTEMS

↓

PROJECT SYSTEM

↓

TOOLS

↓

MEDIA / OUTPUT

---

# 3. ROOT FILES

## CLAUDE.md

Primary role:

Master Studio Operating System.

Defines:

- Claude's studio role
- orchestration
- production pipeline
- department routing
- decision ownership
- project coordination
- change control
- dependencies
- AI generation control
- knowledge management
- security
- command behavior

Claude should consult this first when determining how the studio operates.

---

## README.md

Primary role:

Repository overview.

Should explain:

- studio purpose
- repository structure
- basic navigation
- major systems
- project workflow
- how to start a project

README should remain concise compared with the operating system.

---

# 4. STUDIO CONTROL SYSTEMS

## studio/COMMAND_CENTER.md

Primary role:

Current production-state control.

Use for:

- current project
- phase
- active tasks
- blockers
- approvals
- risks
- shots
- assets
- QC
- delivery
- next action

This is the operational dashboard.

---

## studio/DATA_SCHEMA.md

Primary role:

Canonical data language.

Defines:

- IDs
- entities
- relationships
- statuses
- versions
- tasks
- shots
- assets
- characters
- locations
- approvals
- QC
- rights
- deliveries
- archives

Use this when creating or interpreting structured project records.

---

## studio/STUDIO_BIBLE.md

Primary role:

Permanent creative philosophy.

Defines:

- studio identity
- storytelling principles
- cinematic philosophy
- AI philosophy
- visual language
- sound philosophy
- color philosophy
- quality standards
- documentary principles
- creative critique

Use this when making studio-level creative decisions.

---

## studio/PROMPT_SYSTEM.md

Primary role:

Prompt engineering and generation framework.

Defines:

- prompt architecture
- shot prompts
- character prompts
- environment prompts
- AI video prompts
- voice prompts
- music prompts
- research prompts
- QC prompts
- prompt versioning
- prompt library
- model-aware prompting

Use whenever a production prompt must be created, revised, tested, or reused.

---

## studio/TOOL_REGISTRY.md

Primary role:

Inventory and evaluation of production tools.

Defines:

- software
- AI models
- hardware
- plugins
- APIs
- MCP tools
- Adobe applications
- local/cloud/HPC workflows
- capabilities
- limitations
- licensing
- security
- tool selection
- benchmarking

Use this before selecting production technology.

---

## studio/AUTOMATION.md

Primary role:

Automation architecture.

Defines:

- triggers
- workflows
- queues
- scripts
- batch generation
- rendering
- QC automation
- reports
- error handling
- retry
- rollback
- security
- automation approval

Use when designing or executing repeatable automated production work.

---

## studio/TEMPLATE_REGISTRY.md

Primary role:

Reusable production structures.

Defines:

- project templates
- scene templates
- shot templates
- asset templates
- prompt templates
- research templates
- QC templates
- delivery templates
- archive templates
- project-type bundles
- template versioning

Use before creating a new recurring document structure.

---

## studio/MEDIA_STORAGE.md

Primary role:

Media and storage architecture.

Defines:

- project storage
- source media
- proxies
- working media
- masters
- delivery
- archive
- backup
- checksums
- naming
- manifests
- storage health
- disaster recovery

Use when deciding where media and project files belong.

---

# 5. DIRECTORIAL DEPARTMENTS

## studio/director/SKILL.md

Primary role:

Direction and creative vision.

Use for:

- visual storytelling
- scene interpretation
- shot purpose
- blocking
- camera intent
- performance direction
- cinematic language
- AI-directed imagery
- documentary visual distinctions

---

## studio/writer/SKILL.md

Primary role:

Story and writing.

Use for:

- concept
- logline
- premise
- synopsis
- treatment
- script
- dialogue
- narration
- documentary writing
- structure
- character arcs
- pacing
- revision

---

## studio/performance/SKILL.md

Primary role:

Character and performance.

Use for:

- character objectives
- motivation
- emotional state
- performance beats
- body language
- face / eyes
- voice
- subtext
- relationships
- AI character performance
- lipsync

---

## studio/casting-talent/SKILL.md

Primary role:

Casting and talent coordination.

Use for:

- character casting
- voice casting
- narrators
- documentary participants
- auditions
- talent records
- AI character references
- synthetic voice
- releases

---

# 6. VISUAL DEVELOPMENT DEPARTMENTS

## studio/production-design/SKILL.md

Primary role:

World and visual environment design.

Use for:

- locations
- sets
- architecture
- props
- materials
- environments
- historical design
- cultural design
- documentary reconstruction
- visual world-building

---

## studio/storyboard-previs/SKILL.md

Primary role:

Previsualization.

Use for:

- storyboards
- shot planning
- blocking
- camera planning
- screen direction
- animatics
- previs
- VFX planning
- motion planning

---

## studio/cinematography/SKILL.md

Primary role:

Camera and image design.

Use for:

- framing
- lens
- camera placement
- movement
- composition
- lighting
- depth
- visual continuity
- AI cinematography

---

## studio/ai-generation/SKILL.md

Primary role:

AI image / video / visual generation.

Use for:

- image generation
- video generation
- character generation
- environment generation
- object generation
- AI animation
- generation logs
- prompt/model selection
- reference systems
- batch generation

---

## studio/animation/SKILL.md

Primary role:

Animation.

Use for:

- 2D
- 3D
- character animation
- facial animation
- lip sync
- mechanical animation
- environment animation
- scientific animation
- motion timing

---

## studio/vfx-motion/SKILL.md

Primary role:

VFX and motion graphics.

Use for:

- compositing
- tracking
- roto
- keying
- cleanup
- screen replacement
- motion graphics
- titles
- lower thirds
- maps
- infographics
- AI VFX

---

# 7. EDITORIAL DEPARTMENTS

## studio/editor/SKILL.md

Primary role:

Editorial construction.

Use for:

- selects
- assembly
- rough cut
- fine cut
- picture lock
- pacing
- transitions
- montage
- dialogue editing
- B-roll
- documentary editing

---

## studio/sound/SKILL.md

Primary role:

Complete sound department.

Use for:

- dialogue
- VO
- ambience
- room tone
- Foley
- SFX
- sound design
- mixing
- audio QC

---

## studio/music/SKILL.md

Primary role:

Music and score.

Use for:

- score
- music supervision
- themes
- leitmotifs
- cue sheets
- music editing
- stems
- AI music
- music rights

---

## studio/color/SKILL.md

Primary role:

Color and image finishing.

Use for:

- technical normalization
- look development
- shot matching
- scene matching
- skin tone
- VFX integration
- grain
- HDR
- SDR
- final color master

---

# 8. PRODUCTION OPERATIONS

## studio/producer/SKILL.md

Primary role:

Producer and production management.

Use for:

- scope
- planning
- WBS
- scheduling
- resources
- dependencies
- approvals
- risk
- delivery
- project coordination

---

## studio/production-management/SKILL.md

Primary role:

Detailed production execution and assistant-director functions.

Use for:

- daily planning
- execution
- schedules
- milestones
- blockers
- production readiness
- critical path
- coordination
- picture lock readiness

---

## studio/workflow/SKILL.md

Primary role:

Workflow orchestration.

Use for:

- master pipeline
- phases
- task states
- approvals
- change control
- parallel work
- dependencies
- project state
- production communication

---

## studio/asset-pipeline/SKILL.md

Primary role:

Asset and pipeline management.

Use for:

- asset IDs
- metadata
- naming
- versions
- ingest
- asset inventory
- asset relationships
- storage organization
- handoffs
- archive

---

# 9. RESEARCH / FACTUAL INTEGRITY

## studio/research/SKILL.md

Primary role:

Research and evidence management.

Use for:

- research questions
- source discovery
- source evaluation
- evidence
- fact checking
- historical research
- scientific research
- technical research
- documentary research
- source traceability

---

## studio/legal-rights/SKILL.md

Primary role:

Rights and legal compliance.

Use for:

- copyright
- stock
- music
- archival material
- talent rights
- voice
- likeness
- AI content
- trademarks
- fonts
- data
- attribution
- permissions

---

## studio/continuity/SKILL.md

Primary role:

Consistency management.

Use for:

- characters
- props
- wardrobe
- locations
- time
- geography
- lighting
- camera
- screen direction
- sound
- VFX
- AI consistency

---

# 10. TECHNICAL / ENGINEERING

## studio/technical-post/SKILL.md

Primary role:

Technical post-production engineering.

Use for:

- codecs
- media pipelines
- render systems
- AI infrastructure
- GPU environments
- scripts
- Python
- plugins
- storage
- cache
- logs
- troubleshooting
- reproducibility
- file integrity

---

# 11. QUALITY / DELIVERY

## studio/qc/SKILL.md

Primary role:

Quality control.

Use for:

- creative QC
- technical QC
- factual QC
- continuity QC
- audio QC
- color QC
- AI artifact QC
- subtitle QC
- accessibility QC
- delivery QC

---

## studio/distribution/SKILL.md

Primary role:

Distribution and delivery.

Use for:

- platform versions
- aspect ratios
- subtitles
- captions
- audio deliverables
- masters
- metadata
- credits
- thumbnails
- posters
- packaging
- final delivery

---

## studio/marketing-promotion/SKILL.md

Primary role:

Marketing and promotional material.

Use for:

- audience
- positioning
- trailers
- teasers
- short-form
- social
- thumbnails
- key art
- campaign messaging
- promotional assets

---

# 12. KNOWLEDGE / ARCHIVE

## studio/knowledge-archive/SKILL.md

Primary role:

Long-term studio knowledge and archive.

Use for:

- project memory
- lessons
- decisions
- reusable knowledge
- prompt history
- workflow history
- source traceability
- asset traceability
- project archive
- backup strategy

---

# 13. PROJECT INITIALIZATION

## studio/project-template/SKILL.md

Primary role:

Project creation system.

Use when starting a new project.

It defines:

- Project ID
- project folders
- core project files
- task system
- shot system
- asset system
- risk system
- blocker system
- decision system
- approval system
- QC system
- rights system
- delivery system
- archive system
- project complexity levels

---

# 14. DEPARTMENT ROUTING MATRIX

Use this matrix when deciding where a request belongs.

| Request | Primary Department | Supporting Departments |
|---|---|---|
| Story idea | Writer | Director |
| Script | Writer | Director, Research |
| Scene direction | Director | Writer, Cinematography |
| Character | Performance | Casting, Director |
| Casting | Casting | Director, Performance |
| Location design | Production Design | Director, Cinematography |
| Shot design | Cinematography | Director, Storyboard |
| Storyboard | Storyboard / Previs | Director, Cinematography |
| Previs | Storyboard / Previs | Director, Animation |
| AI image | AI Generation | Cinematography, Production Design |
| AI video | AI Generation | Director, Cinematography, Performance |
| Character consistency | Continuity | Performance, AI Generation |
| Editing | Editor | Director, Sound, Music |
| VFX | VFX / Motion | Director, Cinematography, AI Generation |
| Animation | Animation | Director, VFX |
| Sound | Sound | Editor, Music |
| Music | Music | Director, Editor |
| Color | Color | Cinematography, VFX |
| Research | Research | Writer, Director |
| Rights | Legal / Rights | Research, Distribution |
| QC | QC | All departments |
| Delivery | Distribution | QC, Technical Post |
| Storage | Media Storage | Asset Pipeline, Technical Post |
| Automation | Automation | Technical Post, relevant department |
| Tool choice | Tool Registry | Technical Post, relevant department |
| Project setup | Project Template | Producer, Workflow |
| Current project state | Command Center | All departments |
| Data structure | Data Schema | All departments |
| Studio philosophy | Studio Bible | Director |
| Prompt design | Prompt System | AI Generation, relevant department |
| Archive | Knowledge / Archive | Asset Pipeline, Technical Post |

---

# 15. REQUEST ROUTING RULE

When a request arrives:

1. Identify the production objective.
2. Identify the entity involved.
3. Identify the responsible department.
4. Read the relevant department skill.
5. Check Command Center state.
6. Check Data Schema requirements.
7. Check dependencies.
8. Check applicable templates.
9. Check Tool Registry if execution requires software.
10. Check Prompt System if AI generation is involved.
11. Execute or prepare the required work.
12. Update project state.

---

# 16. CROSS-DEPARTMENT REQUESTS

Some requests require multiple departments.

Examples:

"Create a cinematic scene."

Use:

Writer
→ Director
→ Production Design
→ Performance
→ Storyboard / Previs
→ Cinematography
→ AI Generation
→ Edit
→ Sound
→ Music
→ Color
→ QC

---

# 17. RESEARCH-HEAVY REQUESTS

For factual projects:

Research
→ Writer
→ Director
→ Production Design / Visuals
→ Editorial
→ QC
→ Legal where required

Research must remain traceable.

---

# 18. AI VIDEO REQUEST

For:

"Create this shot."

Use:

Director

→ Shot definition

→ Cinematography

→ Performance / Character

→ Production Design

→ AI Generation

→ Continuity

→ Editorial

→ QC

---

# 19. DOCUMENTARY REQUEST

For:

"Make a documentary about X."

Use:

Producer
→ Research
→ Writer
→ Director
→ Storyboard / Previs where useful
→ Production / AI / Archive
→ Editor
→ Sound
→ Music
→ Color
→ QC
→ Rights
→ Distribution
→ Archive

---

# 20. COMMERCIAL REQUEST

For:

"Create an advertisement."

Use:

Producer
→ Audience / Marketing
→ Writer
→ Director
→ Production Design
→ Casting
→ Cinematography
→ AI / Production
→ Edit
→ VFX
→ Sound
→ Music
→ Color
→ QC
→ Legal
→ Delivery

---

# 21. SCIENTIFIC VISUALIZATION REQUEST

Use:

Research
→ scientific evidence

Writer
→ explanation

Director
→ narrative purpose

Production Design
→ visual language

AI / Animation
→ visualization

Cinematography
→ presentation

Editorial
→ pacing

QC
→ factual + technical validation

---

# 22. CURRENT PROJECT INFORMATION

The active project's detailed information should NOT be duplicated permanently in this index.

Use:

Project Command Center

for current state.

Use:

Project files

for project-specific information.

The index only tells Claude where to look.

---

# 23. PROJECT FILE ROUTING

Project-level operational information:

→ Command Center

Project structured entities:

→ Data Schema

Project templates:

→ Project Template System

Project creative philosophy:

→ Project-specific creative files + Studio Bible

Project prompts:

→ Prompt System + project prompt library

Project tools:

→ Tool Registry + project tool snapshot

Project media:

→ Media Storage System

Project knowledge:

→ Knowledge / Archive

---

# 24. DEFAULT CONSULTATION ORDER

For an unfamiliar production request, consult:

1. `CLAUDE.md`
2. `studio/COMMAND_CENTER.md`
3. relevant `SKILL.md`
4. `studio/DATA_SCHEMA.md`
5. `studio/TEMPLATE_REGISTRY.md`
6. `studio/PROMPT_SYSTEM.md` if AI generation is involved
7. `studio/TOOL_REGISTRY.md` if a tool is required
8. `studio/MEDIA_STORAGE.md` if files/media are involved
9. project-specific files

Do not read every document unnecessarily.

Read what is relevant to the task.

---

# 25. DEPARTMENT SKILL LOADING

When a task belongs primarily to one department:

Load that department's `SKILL.md`.

Then load supporting departments only when necessary.

Example:

AI video generation

Primary:
`ai-generation/SKILL.md`

Supporting:
`director/SKILL.md`
`cinematography/SKILL.md`
`performance/SKILL.md`
`continuity/SKILL.md`

---

# 26. CREATIVE REQUEST LOADING

For creative tasks:

Consult:

Studio Bible

+

Director

+

relevant specialist

+

Project creative brief

This maintains studio-level consistency while preserving project-specific direction.

---

# 27. OPERATIONAL REQUEST LOADING

For operational tasks:

Consult:

Command Center

+

Workflow

+

Producer / Production Management

+

Data Schema

+

relevant department

---

# 28. TECHNICAL REQUEST LOADING

For technical tasks:

Consult:

Technical Post

+

Tool Registry

+

Media Storage

+

Automation where applicable

+

Data Schema

---

# 29. AI REQUEST LOADING

For AI tasks:

Consult:

AI Generation

+

Prompt System

+

Tool Registry

+

Director

+

Cinematography / Performance / Production Design as required

+

Continuity

+

QC

---

# 30. DELIVERY REQUEST LOADING

For delivery:

Distribution

+

QC

+

Technical Post

+

Legal / Rights

+

Media Storage

---

# 31. ARCHIVE REQUEST LOADING

For archive:

Knowledge / Archive

+

Media Storage

+

Asset Pipeline

+

Technical Post

+

QC

+

Distribution

---

# 32. STATUS REQUEST LOADING

For:

`status`

Primary:

Command Center

Supporting:

Workflow

Production Management

QC

Distribution

Archive

Do not construct status from memory when project records exist.

---

# 33. NEXT REQUEST LOADING

For:

`next`

Use:

Command Center

+

Task system

+

Dependency system

+

Blockers

+

Approvals

+

Critical path

Then consult the responsible department's skill.

---

# 34. BLOCKED REQUEST LOADING

For:

`blocked`

Use:

Command Center

+

Blocker Register

+

Dependency System

+

Production Management

+

relevant department

---

# 35. REVIEW REQUEST LOADING

For:

`review`

Use:

appropriate department skill

+

QC

+

Continuity

+

Research where relevant

+

Rights where relevant

The scope of review should be explicit.

---

# 36. MAKE IT REQUEST

For:

`make it`

Use:

Command Center

→ identify approved task

→ identify required department

→ load department skill

→ load relevant template

→ verify tools

→ create execution plan

→ execute if authorized

→ verify

→ update state

---

# 37. PASTABLE REQUEST

For:

`pastable`

Return the requested file or artifact as one complete pasteable block.

Avoid splitting a requested file into multiple blocks unless explicitly requested.

Do not introduce nested fenced code blocks that break the single pasteable structure.

Use indented examples inside the document where needed.

---

# 38. FILE CREATION PRINCIPLE

When creating a new studio system file:

1. identify correct directory
2. check whether the file already exists
3. check for overlapping responsibility
4. determine purpose
5. create complete content
6. preserve naming convention
7. register it in this index
8. update related systems if necessary

Do not create duplicate systems unnecessarily.

---

# 39. NEW DEPARTMENT PRINCIPLE

Before creating a new department:

ask:

Does an existing department already own this responsibility?

Can the capability be added to an existing department?

Would a new department materially improve the system?

Only create a separate department when the responsibility is sufficiently distinct.

---

# 40. NEW SYSTEM PRINCIPLE

Before creating a new control document:

check:

Command Center

Data Schema

Template Registry

Automation

Tool Registry

Media Storage

Studio Bible

Prompt System

If the requested function already belongs there, extend the appropriate system instead of creating unnecessary fragmentation.

---

# 41. DOCUMENT HIERARCHY

The studio documentation hierarchy is:

MASTER RULES
`CLAUDE.md`

CREATIVE CONSTITUTION
`STUDIO_BIBLE.md`

OPERATIONAL STATE
`COMMAND_CENTER.md`

DATA STRUCTURE
`DATA_SCHEMA.md`

TOOLS
`TOOL_REGISTRY.md`

PROMPTS
`PROMPT_SYSTEM.md`

AUTOMATION
`AUTOMATION.md`

TEMPLATES
`TEMPLATE_REGISTRY.md`

MEDIA
`MEDIA_STORAGE.md`

SPECIALIST EXECUTION
department `SKILL.md`

PROJECT IMPLEMENTATION
project files

---

# 42. CONFLICT RESOLUTION

If documents conflict:

1. identify conflict
2. determine scope
3. determine whether one document governs the other
4. check project-specific override
5. check version
6. preserve historical information
7. resolve explicitly
8. update the appropriate canonical source

Do not silently choose one document.

---

# 43. AUTHORITY MODEL

Recommended authority:

Studio-wide operating rules:

`CLAUDE.md`

Studio creative philosophy:

`STUDIO_BIBLE.md`

Studio data definitions:

`DATA_SCHEMA.md`

Current project state:

`COMMAND_CENTER.md`

Department execution:

department `SKILL.md`

Project-specific facts:

project records

Project-specific approved decisions:

project decision / approval records

Current tool capability:

`TOOL_REGISTRY.md`

Current prompt methodology:

`PROMPT_SYSTEM.md`

---

# 44. PROJECT OVERRIDES

A project may intentionally differ from studio defaults.

Examples:

- unique visual language
- special aspect ratio
- unique workflow
- custom department requirement
- alternative delivery target
- unusual documentation requirements

Project overrides must be documented within the project.

Do not alter the Studio-wide rule merely for one project.

---

# 45. VERSION AWARENESS

When a studio document changes:

record its version where appropriate.

When a project depends on a particular system version:

record that dependency.

Important production work should remain reconstructible.

---

# 46. INDEX MAINTENANCE

Update this index when:

- a new core system is created
- a department is added
- a department is renamed
- a system is retired
- responsibility changes
- routing changes materially
- repository structure changes

Do not update it for every small content revision.

---

# 47. INDEX AUDIT

Audit:

□ every core system is listed

□ every department is listed

□ paths are correct

□ responsibilities are clear

□ no major system is duplicated

□ routing matrix is current

□ authority model is clear

□ command routing is defined

□ project routing is defined

---

# 48. STUDIO FILE MAP

Current core systems:

CLAUDE.md

README.md

studio/COMMAND_CENTER.md

studio/DATA_SCHEMA.md

studio/STUDIO_BIBLE.md

studio/PROMPT_SYSTEM.md

studio/TOOL_REGISTRY.md

studio/AUTOMATION.md

studio/TEMPLATE_REGISTRY.md

studio/MEDIA_STORAGE.md

studio/STUDIO_INDEX.md

---

# 49. DEPARTMENT FILE MAP

studio/director/SKILL.md

studio/producer/SKILL.md

studio/writer/SKILL.md

studio/cinematography/SKILL.md

studio/editor/SKILL.md

studio/sound/SKILL.md

studio/vfx-motion/SKILL.md

studio/color/SKILL.md

studio/research/SKILL.md

studio/qc/SKILL.md

studio/workflow/SKILL.md

studio/production-design/SKILL.md

studio/continuity/SKILL.md

studio/legal-rights/SKILL.md

studio/distribution/SKILL.md

studio/marketing-promotion/SKILL.md

studio/performance/SKILL.md

studio/music/SKILL.md

studio/casting-talent/SKILL.md

studio/production-management/SKILL.md

studio/asset-pipeline/SKILL.md

studio/animation/SKILL.md

studio/technical-post/SKILL.md

studio/knowledge-archive/SKILL.md

studio/storyboard-previs/SKILL.md

studio/ai-generation/SKILL.md

studio/project-template/SKILL.md

---

# 50. STUDIO NAVIGATION MAP

START

↓

`CLAUDE.md`

↓

WHAT IS THE USER ASKING?

↓

CREATIVE
→ Studio Bible
→ Department Skill

OPERATIONAL
→ Command Center
→ Workflow / Production

DATA
→ Data Schema

AI
→ Prompt System
→ AI Generation
→ Tool Registry

AUTOMATION
→ Automation

TEMPLATES
→ Template Registry

MEDIA
→ Media Storage

RESEARCH
→ Research

RIGHTS
→ Legal / Rights

QUALITY
→ QC

DELIVERY
→ Distribution

ARCHIVE
→ Knowledge / Archive

↓

PROJECT FILES

↓

EXECUTION

↓

VERIFICATION

↓

UPDATE COMMAND CENTER

---

# 51. MASTER ROUTING LOGIC

For every task Claude should internally determine:

PURPOSE

→ ENTITY

→ DEPARTMENT

→ REQUIRED KNOWLEDGE

→ REQUIRED TEMPLATE

→ REQUIRED TOOL

→ DEPENDENCIES

→ APPROVAL

→ EXECUTION

→ VALIDATION

→ STATE UPDATE

This is the basic routing algorithm of the Studio.

---

# 52. NO RANDOM ROUTING

Claude should not select departments arbitrarily.

Route according to responsibility.

Example:

Camera question
→ Cinematography

Story structure question
→ Writer / Director

Storage question
→ Media Storage / Asset Pipeline

AI model selection
→ Tool Registry + AI Generation

Prompt design
→ Prompt System + relevant department

Final technical validation
→ QC + Technical Post

Rights question
→ Legal / Rights

---

# 53. MULTI-DEPARTMENT ORCHESTRATION

For complex tasks, assign:

PRIMARY DEPARTMENT

+

SUPPORTING DEPARTMENTS

Example:

Primary:
Director

Supporting:
Writer
Cinematography
Production Design
Performance
Storyboard
AI Generation
Continuity

This prevents all departments from attempting to own the same task.

---

# 54. DEPARTMENT OWNERSHIP

Each task should have one primary owner.

Supporting departments contribute inputs.

Example:

SHOT DESIGN

Primary:
Cinematography

Supporting:
Director
Storyboard / Previs
Performance
Production Design
Continuity

---

# 55. DECISION OWNERSHIP

Suggested default ownership:

Story:
Writer + Director

Creative Vision:
Director

Production:
Producer / Production Management

Camera:
Cinematography

Performance:
Director / Performance

World:
Production Design

AI Generation:
AI Generation + Director

Editorial:
Editor + Director

Sound:
Sound

Music:
Music

Color:
Color

Continuity:
Continuity

Research:
Research

Rights:
Legal / Rights

Technical:
Technical Post

QC:
QC

Delivery:
Distribution

Project State:
Command Center / Production Management

---

# 56. FINAL SOURCE-OF-TRUTH MAP

WHAT IS HAPPENING NOW?

→ Command Center

WHAT SHOULD THE STUDIO DO?

→ CLAUDE.md

HOW SHOULD THE SPECIALIST WORK?

→ Department Skill

WHAT DOES THE DATA MEAN?

→ Data Schema

WHAT IS THE CREATIVE PHILOSOPHY?

→ Studio Bible

WHAT PROMPT SYSTEM SHOULD BE USED?

→ Prompt System

WHAT TOOLS EXIST?

→ Tool Registry

WHAT CAN BE AUTOMATED?

→ Automation

WHAT TEMPLATES EXIST?

→ Template Registry

WHERE DOES MEDIA LIVE?

→ Media Storage

WHAT HAPPENED BEFORE?

→ Knowledge / Archive

---

# 57. STUDIO INDEX PRINCIPLE

The Index should reduce search time.

Claude should not repeatedly inspect the entire repository when the appropriate file is already known.

Use the index to route quickly.

Then inspect only the relevant systems.

---

# 58. FINAL STANDARD

The AI Film Studio should feel like one integrated organization, not a collection of disconnected Markdown files.

The architecture is:

MASTER OPERATING SYSTEM

↓

CREATIVE PHILOSOPHY

↓

CONTROL SYSTEMS

↓

DEPARTMENTS

↓

PROJECT SYSTEM

↓

TOOLS

↓

MEDIA

↓

QC

↓

DELIVERY

↓

ARCHIVE

The Studio Index connects these layers.

Its purpose is simple:

KNOW WHERE TO LOOK.

KNOW WHO SHOULD ACT.

KNOW WHAT SYSTEM GOVERNS THE DECISION.

KNOW WHAT THE CURRENT STATE IS.

KNOW WHAT HAPPENS NEXT.
