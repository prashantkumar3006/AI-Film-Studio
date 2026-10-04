# STUDIO DATA SCHEMA

## 1. PURPOSE

The Studio Data Schema defines the canonical structure used by the AI Film Studio for production information.

It standardizes:

- IDs
- naming
- metadata
- tasks
- shots
- assets
- characters
- locations
- scenes
- sequences
- approvals
- dependencies
- blockers
- risks
- decisions
- changes
- QC issues
- rights
- versions
- handoffs
- deliverables
- archive records

The goal is interoperability.

A Writer, Director, Editor, VFX Supervisor, Sound Designer, AI Generation system, QC system, and Producer must be able to understand the same project records without redefining their meaning.

---

# 2. CORE DATA PRINCIPLES

## 2.1 One Record = One Entity

Each important entity should have one canonical record.

Do not create multiple contradictory records for the same entity.

---

## 2.2 Every Important Entity Gets an ID

IDs must be unique within the project.

Examples:

PROJECT_2026_001
SEQ_001
SCN_001
SHOT_001
CHAR_001
LOC_001
PROP_001
ASSET_001
TASK_001
RISK_001
BLOCK_001
QC_001
DEC_001
CHG_001
APR_001
HANDOFF_001
DEL_001

---

## 2.3 Human-Readable Names

IDs are for systems.

Names are for people.

Example:

SHOT_014
Name: "Train Station Reveal"

Both should be preserved.

---

## 2.4 Stable IDs

Do not change an entity's ID merely because:

- its name changes
- its appearance changes
- its version changes
- its department changes
- its status changes

The identity persists.

---

## 2.5 Version Is Separate From Identity

A shot may remain:

SHOT_014

while its versions become:

SHOT_014_v001
SHOT_014_v002
SHOT_014_v003

The same applies to assets, edits, prompts, renders, graphics, and deliverables.

---

# 3. ID SYSTEM

Recommended formats:

PROJECT_YYYY_NNN

SEQUENCE:
SEQ_NNN

SCENE:
SCN_NNN

SHOT:
SHOT_NNN

CHARACTER:
CHAR_NNN

LOCATION:
LOC_NNN

PROP:
PROP_NNN

SET:
SET_NNN

COSTUME:
COST_NNN

ASSET:
ASSET_NNN

TASK:
TASK_NNN

DEPENDENCY:
DEP_NNN

BLOCKER:
BLOCK_NNN

RISK:
RISK_NNN

DECISION:
DEC_NNN

CHANGE:
CHG_NNN

APPROVAL:
APR_NNN

HANDOFF:
HANDOFF_NNN

QC:
QC_NNN

RIGHTS:
RIGHTS_NNN

DELIVERY:
DEL_NNN

ARCHIVE:
ARCH_NNN

PROMPT:
PROMPT_NNN

MODEL:
MODEL_NNN

RENDER:
RENDER_NNN

MUSIC CUE:
CUE_NNN

SOUND EVENT:
SND_NNN

VFX:
VFX_NNN

GRAPHIC:
GFX_NNN

STORYBOARD:
SB_NNN

PREVIS:
PREVIS_NNN

---

# 4. PROJECT RECORD

Every project must contain a project identity record.

Project ID:
Project Title:
Project Type:
Project Owner:
Studio:
Created Date:
Current Version:
Current State:
Current Phase:
Target Runtime:
Target Resolution:
Target Frame Rate:
Primary Aspect Ratio:
Target Platforms:
Target Languages:
Target Delivery Date:
Current Command Center:
Archive Location:

Project Type values:

- NARRATIVE
- DOCUMENTARY
- SCIENTIFIC_DOCUMENTARY
- EDUCATIONAL
- EXPLAINER
- COMMERCIAL
- PROMO
- MUSIC_VIDEO
- ANIMATION
- AI_FILM
- HYBRID
- SOCIAL
- EXPERIMENTAL

---

# 5. SEQUENCE RECORD

Sequence ID:
Project ID:
Sequence Name:
Sequence Number:
Purpose:
Story Function:
Location:
Time:
Characters:
Scenes:
Estimated Duration:
Editor Status:
Director Status:
Continuity Status:
Approval Status:
Version:

Relationships:

Project
→ contains
Sequence

Sequence
→ contains
Scenes

---

# 6. SCENE RECORD

Scene ID:
Project ID:
Sequence ID:
Scene Number:
Scene Name:
Purpose:
Story Beat:
Location ID:
Time:
Weather:
Characters:
Props:
Costume State:
Emotional State:
Conflict:
Dialogue:
Narration:
Visual Objective:
Sound Objective:
Music Objective:
Required Shots:
Continuity Requirements:
Research Requirements:
Rights Requirements:
Current Version:
Status:
Approval:

A scene should explain why the shots exist.

---

# 7. SHOT RECORD

Shot ID:
Project ID:
Sequence ID:
Scene ID:
Shot Number:
Shot Name:
Shot Purpose:
Story Beat:
Character IDs:
Location ID:
Camera:
Lens:
Camera Height:
Framing:
Movement:
Composition:
Lighting:
Depth:
Focus:
Performance:
Dialogue:
VO:
Sound:
Music:
VFX:
Animation:
AI Generation:
Source Assets:
Reference Assets:
Prompt ID:
Generation Model:
Take / Variant:
Editor Status:
Continuity Status:
Color Status:
QC Status:
Rights Status:
Approval:
Current Version:

Status values:

- PLANNED
- STORYBOARDED
- PREVIS
- READY
- GENERATING
- GENERATED
- SELECTED
- EDITED
- VFX
- COLOR
- QC
- APPROVED
- REJECTED
- FINAL

---

# 8. ASSET RECORD

Asset ID:
Project ID:
Asset Name:
Asset Type:
Department:
Source:
Creator:
Owner:
Parent Asset:
Related Character:
Related Location:
Related Shot:
Related Scene:
File Path:
Format:
Resolution:
Frame Rate:
Duration:
File Size:
Checksum:
Version:
Status:
Rights Status:
Continuity Status:
QC Status:
Approval:
Created Date:
Modified Date:
Notes:

Asset Type values:

- VIDEO
- IMAGE
- AUDIO
- MUSIC
- VOICE
- CHARACTER
- LOCATION
- SET
- PROP
- COSTUME
- ARCHIVAL
- STOCK
- VFX
- ANIMATION
- GRAPHIC
- TITLE
- MAP
- DATA
- AI_GENERATED
- DOCUMENT
- PROJECT_FILE
- MASTER
- DELIVERY

---

# 9. CHARACTER RECORD

Character ID:
Project ID:
Name:
Role:
Story Function:
Age:
Apparent Age:
Gender Presentation:
Appearance:
Body:
Face:
Hair:
Wardrobe:
Accessories:
Voice:
Accent:
Personality:
Motivation:
Goal:
Fear:
Conflict:
Relationships:
Knowledge State:
Emotional Baseline:
Current Emotional State:
Character Arc:
Performance Notes:
Casting Record:
Reference Images:
Reference Video:
AI Reference:
Voice Reference:
Continuity Notes:
Rights / Release:
Version:
Status:

---

# 10. LOCATION RECORD

Location ID:
Project ID:
Name:
Type:
Story Function:
Geography:
Architecture:
Era:
Climate:
Weather:
Time:
Lighting:
Materials:
Colors:
Props:
Background Activity:
Sound Environment:
Reference Images:
Reference Video:
AI Environment Reference:
VFX Requirements:
Continuity Notes:
Rights / Source:
Version:
Status:

---

# 11. PROP RECORD

Prop ID:
Project ID:
Name:
Purpose:
Owner:
Character:
Scene:
Shot:
Physical Description:
Material:
Color:
Age / Condition:
Historical Context:
Source:
Reference:
Continuity Requirement:
Rights:
Version:
Status:

---

# 12. TASK RECORD

Task ID:
Project ID:
Task Name:
Department:
Phase:
Owner:
Priority:
Description:
Input:
Output:
Dependencies:
Blocked By:
Blocks:
Estimated Effort:
Schedule:
Start Date:
Due Date:
Status:
Approval Required:
QC Required:
Version:
Created:
Updated:
Notes:

Priority values:

P0
Critical production blocker.

P1
Critical-path / high priority.

P2
Normal production work.

P3
Optional / enhancement.

Status values:

- NOT STARTED
- READY
- ACTIVE
- WAITING
- BLOCKED
- REVIEW
- APPROVED
- COMPLETE
- CANCELLED

---

# 13. DEPENDENCY RECORD

Dependency ID:
Project ID:
Upstream Entity:
Downstream Entity:
Dependency Type:
Required Input:
Reason:
Status:
Impact:
Resolution:
Owner:

Dependency Type examples:

- TASK_TO_TASK
- ASSET_TO_TASK
- APPROVAL_TO_TASK
- RESEARCH_TO_SCRIPT
- SCRIPT_TO_SHOT
- SHOT_TO_EDIT
- EDIT_TO_VFX
- EDIT_TO_SOUND
- RIGHTS_TO_DELIVERY
- QC_TO_DELIVERY
- CHARACTER_TO_SHOT
- LOCATION_TO_SHOT

Status:

- SATISFIED
- WAITING
- BLOCKED
- INVALID
- NOT_APPLICABLE

---

# 14. BLOCKER RECORD

Blocker ID:
Project ID:
Description:
Category:
Severity:
Created:
Detected By:
Department:
Affected Task:
Affected Shot:
Affected Asset:
Affected Phase:
Root Cause:
Owner:
Missing Input:
Resolution:
Workaround:
Deadline:
Status:
Resolved Date:

Severity:

CRITICAL
HIGH
MEDIUM
LOW

---

# 15. RISK RECORD

Risk ID:
Project ID:
Risk:
Category:
Probability:
Impact:
Severity:
Trigger:
Affected Departments:
Affected Assets:
Affected Schedule:
Mitigation:
Contingency:
Owner:
Status:
Review Date:

Risk categories:

- CREATIVE
- STORY
- SCHEDULE
- BUDGET
- RIGHTS
- AI
- TECHNICAL
- DATA
- TALENT
- CONTINUITY
- QUALITY
- DELIVERY
- STORAGE
- SECURITY

---

# 16. APPROVAL RECORD

Approval ID:
Project ID:
Gate:
Entity:
Entity ID:
Version:
Submitted By:
Reviewer:
Submission Date:
Review Date:
Status:
Conditions:
Comments:
Evidence:
Next Action:

Approval status:

- NOT_READY
- READY_FOR_REVIEW
- IN_REVIEW
- CHANGES_REQUIRED
- APPROVED
- REJECTED

Approval is version-specific.

Approval of:

SHOT_014_v002

does not automatically approve:

SHOT_014_v003

unless the project explicitly defines version inheritance.

---

# 17. DECISION RECORD

Decision ID:
Project ID:
Date:
Decision:
Decision Type:
Decision Owner:
Reason:
Alternatives:
Evidence:
Affected Departments:
Affected Entities:
Expected Consequences:
Version:
Status:

Decision types:

- CREATIVE
- STORY
- TECHNICAL
- PRODUCTION
- AI
- EDITORIAL
- LEGAL
- RIGHTS
- DELIVERY
- MARKETING

---

# 18. CHANGE RECORD

Change ID:
Project ID:
Requester:
Date:
Entity:
Entity ID:
Current Version:
Requested Change:
Reason:
Impact:
Affected Departments:
Affected Tasks:
Affected Shots:
Affected Assets:
Risk:
Approval:
Implementation:
New Version:
Status:

Changes should be traceable from request to final implementation.

---

# 19. QC RECORD

QC ID:
Project ID:
Entity:
Entity ID:
Version:
QC Type:
Reviewer:
Date:
Result:
Severity:
Issue:
Timecode:
Required Fix:
Owner:
Recheck:
Final Status:

QC types:

- CREATIVE
- TECHNICAL
- FACTUAL
- CONTINUITY
- AUDIO
- COLOR
- VFX
- AI
- RIGHTS
- ACCESSIBILITY
- SUBTITLE
- DELIVERY

Results:

- PASS
- PASS_WITH_ISSUES
- FAIL
- NOT_REVIEWED

---

# 20. RIGHTS RECORD

Rights ID:
Project ID:
Asset:
Asset ID:
Material:
Source:
Creator:
License / Permission:
Usage:
Territory:
Duration:
Platform:
Attribution:
Restrictions:
Expiration:
Evidence:
Risk:
Reviewer:
Status:

Rights status:

- UNKNOWN
- RESEARCHING
- RESTRICTED
- CLEARED
- CONDITIONAL
- EXPIRED
- NOT_REQUIRED

Unknown rights must never be silently treated as cleared rights.

---

# 21. PROMPT RECORD

Prompt ID:
Project ID:
Department:
Purpose:
Entity:
Entity ID:
Model:
Model Version:
Prompt:
Negative Constraints:
Reference Assets:
Control Inputs:
Seed:
Generation Settings:
Date:
Creator:
Result:
Selected Output:
Rejected Outputs:
Failure Mode:
Notes:
Version:

Prompt versions should be preserved when they materially affect output.

---

# 22. AI MODEL RECORD

Model ID:
Model Name:
Provider:
Model Version:
Task Type:
Image:
Video:
Audio:
Music:
3D:
Animation:
Known Strengths:
Known Weaknesses:
Input Requirements:
Output Requirements:
Hardware Requirement:
License / Terms:
Safety / Rights Notes:
Approved Uses:
Restricted Uses:
Studio Status:
Last Tested:

---

# 23. GENERATION RECORD

Generation ID:
Project ID:
Prompt ID:
Model ID:
Asset Type:
Target Entity:
Input References:
Prompt Version:
Generation Settings:
Seed:
Batch Size:
Date:
Compute:
Output Files:
Selected Output:
Rejected Outputs:
Reason for Selection:
Known Artifacts:
QC:
Approval:
Final Asset ID:

---

# 24. STORYBOARD RECORD

Storyboard ID:
Project ID:
Sequence:
Scene:
Shot:
Panel Number:
Purpose:
Frame:
Camera:
Character Position:
Blocking:
Action:
Dialogue:
Duration:
Transition:
Continuity:
Notes:
Version:
Approval:

---

# 25. PREVIS RECORD

Previs ID:
Project ID:
Sequence:
Scene:
Shot:
Camera:
Lens:
Movement:
Blocking:
Timing:
Duration:
Environment:
Character Animation:
VFX:
Sound:
Edit Reference:
Version:
Status:
Approval:

---

# 26. EDIT RECORD

Edit ID:
Project ID:
Timeline Name:
Timeline Version:
Runtime:
Editor:
Stage:
Source Version:
Picture Version:
Audio Version:
Music Version:
VFX Version:
Color Version:
Subtitle Version:
Current Status:
Approval:

Stages:

- ASSEMBLY
- ROUGH_CUT
- FINE_CUT
- REVIEW
- PICTURE_LOCK

---

# 27. VFX RECORD

VFX ID:
Project ID:
Shot ID:
Effect:
Purpose:
Source Plate:
Reference:
Tracking:
Roto:
Keying:
Cleanup:
CG:
AI:
Compositing:
Color Integration:
Version:
Status:
QC:
Approval:

---

# 28. SOUND RECORD

Sound Record ID:
Project ID:
Shot / Scene:
Dialogue:
VO:
Room Tone:
Ambience:
Foley:
SFX:
Music:
Sound Design:
Mix:
Channels:
Version:
QC:
Approval:

---

# 29. MUSIC CUE RECORD

Cue ID:
Project ID:
Scene:
Shot Range:
Cue Name:
Purpose:
Theme:
Character:
Emotion:
Tempo:
Duration:
Start Time:
End Time:
Composer / Source:
Version:
Rights:
Stems:
Mix:
Approval:

---

# 30. COLOR RECORD

Color Record ID:
Project ID:
Shot:
Scene:
Source:
Color Space:
Transfer:
Look:
Exposure:
White Balance:
Contrast:
Saturation:
Skin Tone:
VFX Integration:
Grain:
Noise Reduction:
HDR / SDR:
Version:
QC:
Approval:

---

# 31. HANDOFF RECORD

Handoff ID:
Project ID:
From Department:
To Department:
Task:
Entity:
Entity ID:
Version:
Deliverables:
Inputs:
Dependencies:
Known Issues:
QC State:
Rights State:
Continuity State:
Expected Action:
Deadline:
Received By:
Received Date:
Status:

Status:

- PREPARING
- SENT
- RECEIVED
- ACCEPTED
- REJECTED
- COMPLETE

---

# 32. DELIVERY RECORD

Delivery ID:
Project ID:
Destination:
Platform:
Deliverable:
Version:
Resolution:
Frame Rate:
Aspect Ratio:
Codec:
Audio:
Subtitles:
Captions:
Metadata:
Credits:
Thumbnail:
Poster:
Rights:
QC:
Checksum:
File Path:
Delivery Date:
Delivered By:
Status:

Status:

- PREPARING
- READY
- QC
- APPROVED
- DELIVERED
- REJECTED
- REPLACED

---

# 33. ARCHIVE RECORD

Archive ID:
Project ID:
Project Version:
Final Master:
Source Media:
Project Files:
AI Prompts:
AI Generation Logs:
Research:
Rights:
QC:
Decisions:
Changes:
Assets:
Delivery Masters:
Technical Documentation:
Checksums:
Backup:
Archive Location:
Recovery Test:
Archived Date:
Status:

---

# 34. RELATIONSHIP MODEL

The studio should conceptualize information as a connected graph.

PROJECT
→ contains
SEQUENCES

SEQUENCE
→ contains
SCENES

SCENE
→ contains
SHOTS

SHOT
→ uses
CHARACTERS

SHOT
→ uses
LOCATIONS

SHOT
→ uses
PROPS

SHOT
→ uses
ASSETS

SHOT
→ may require
AI GENERATION

SHOT
→ becomes part of
EDIT

EDIT
→ may require
VFX

EDIT
→ requires
SOUND

EDIT
→ requires
MUSIC

EDIT
→ requires
COLOR

FINAL
→ requires
QC

FINAL
→ requires
RIGHTS

FINAL
→ becomes
DELIVERY

DELIVERY
→ becomes
ARCHIVE

---

# 35. CANONICAL ENTITY RULE

When the same entity is mentioned in multiple documents, the ID must identify the same underlying object.

Example:

SHOT_021
may appear in:

- script notes
- storyboard
- previs
- cinematography
- AI generation
- edit
- VFX
- sound
- color
- continuity
- QC
- delivery

All references should resolve to the same Shot ID.

---

# 36. CROSS-REFERENCE RULE

When referencing another entity, use its ID whenever possible.

Prefer:

`SHOT_021 requires ASSET_104`

instead of:

`the train station shot requires the latest background`

Use human-readable names in addition to IDs when helpful.

---

# 37. STATUS INHERITANCE

Status should not automatically propagate unless explicitly defined.

Example:

A shot being `APPROVED` does not automatically mean:

- its audio is approved
- its color is approved
- its rights are approved
- its final delivery is approved

Each approval domain remains independently tracked.

---

# 38. VERSION RELATIONSHIPS

A version can have relationships:

DERIVED_FROM:
SHOT_014_v003

REPLACES:
SHOT_014_v002

SUPERSEDES:
SHOT_014_v001

APPROVED_VERSION:
SHOT_014_v003

CURRENT_VERSION:
SHOT_014_v004

ARCHIVED_VERSION:
SHOT_014_v002

Never destroy historical information merely because a new version exists.

---

# 39. FILE NAMING STANDARD

Recommended naming structure:

PROJECTID_ENTITYID_NAME_VERSION_EXTENSION

Examples:

PROJECT_2026_001_SHOT_014_TRAIN_REVEAL_v003.mp4

PROJECT_2026_001_CHAR_002_MAIN_CHARACTER_v005.png

PROJECT_2026_001_ASSET_087_STATION_BACKGROUND_v004.exr

PROJECT_2026_001_SCN_003_EDIT_v012.prproj

PROJECT_2026_001_QC_009_FINAL_REVIEW_v001.pdf

Use lowercase extensions.

Avoid:

- spaces
- unexplained abbreviations
- inconsistent separators
- random filenames
- `final_final`
- `final_latest`
- `new2`
- `newfinal`
- `use_this_one`

---

# 40. FOLDER NAMING

Project folders should follow the Project Template structure.

Example:

00_admin
01_research
02_story
03_script
04_director
05_production-design
06_casting
07_storyboard-previs
08_cinematography
09_ai-generation
10_animation
11_production
12_edit
13_vfx-motion
14_sound
15_music
16_color
17_continuity
18_technical
19_legal-rights
20_qc
21_distribution
22_marketing
23_knowledge
24_archive
99_backup

---

# 41. MASTER METADATA

Important records may include:

Created:
Created By:
Modified:
Modified By:
Version:
Status:
Owner:
Reviewer:
Approval:
Source:
Evidence:
Dependencies:
Related Entities:
Notes:

Use metadata consistently.

---

# 42. SOURCE TRACEABILITY

Whenever factual or externally sourced information affects production, record:

Source ID:
Source Name:
Source Type:
URL / Location:
Author:
Date:
Access Date:
Claim Supported:
Reliability:
Conflicting Sources:
Notes:

For documentary or research-heavy productions, important claims should be traceable to evidence.

---

# 43. FACTUAL STATUS

Use explicit factual states:

VERIFIED
Supported by appropriate evidence.

SOURCE_REPORTED
Reported by a source but not independently verified.

INTERPRETATION
A reasoned interpretation.

INFERENCE
Derived from available evidence.

RECONSTRUCTION
A representation of an event or environment.

SPECULATION
Not established by available evidence.

FICTIONAL
Intentionally invented.

AI_VISUALIZATION
Generated visual representation rather than original evidence.

Do not present one state as another.

---

# 44. DOCUMENTARY VISUAL RECORD

For documentary projects, visual material should optionally contain:

Visual ID:
Subject:
Source:
Original Date:
Location:
Original Format:
Rights:
Factual Status:
Archival:
Reconstruction:
AI Generated:
Interpretive:
Caption:
Attribution:
Confidence:
Notes:

This prevents generated visualizations from being mistaken for historical footage.

---

# 45. AI CONTENT PROVENANCE

For AI-generated material record:

AI Generated:
Model:
Model Version:
Provider:
Prompt:
Reference Inputs:
Generation Date:
Operator:
Human Editing:
Human Compositing:
Human Selection:
Post-Processing:
Known Artifacts:
Rights / Terms:
Final Usage:
Disclosure Requirement:
Archive Record:

---

# 46. CONFIDENTIALITY

Sensitive project information should be classified when necessary.

Classification:

PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED

Examples of potentially restricted material:

- unreleased footage
- private talent information
- contracts
- rights documents
- private interviews
- credentials
- API keys
- passwords
- private client information
- unreleased scripts
- confidential research

Secrets must never be stored directly in ordinary Markdown files.

---

# 47. SECRET HANDLING

Never store:

- API keys
- passwords
- authentication tokens
- private keys
- access tokens
- browser session data
- secret credentials

inside the repository.

Use secure environment variables or appropriate secret-management systems.

The data schema may reference a secret without storing its value.

Example:

Credential Reference:
`ENV:KLING_API_KEY`

Never:

`KLING_API_KEY=actual-secret`

---

# 48. DATA INTEGRITY RULES

The studio should avoid:

- duplicate IDs
- broken references
- contradictory versions
- missing owners
- undefined statuses
- orphan assets
- orphan shots
- unexplained task completion
- approvals without versions
- QC without target entities
- delivery without master verification

When inconsistencies are detected:

1. identify the conflicting records
2. determine the authoritative record
3. preserve historical information
4. correct references
5. record the correction where necessary

---

# 49. ORPHAN ENTITY DETECTION

An orphan entity is an important record with no meaningful relationship to the production graph.

Examples:

An asset with no project.

A shot with no scene.

A scene with no sequence.

A task with no department.

A delivery with no master.

A QC record with no target.

Claude should identify orphan records during audits.

---

# 50. DUPLICATE DETECTION

Potential duplicates should be detected when two records appear to represent the same thing.

Compare:

- ID
- name
- source
- file
- description
- creation date
- version
- relationships

Never delete a possible duplicate automatically when its historical value is uncertain.

Mark:

`POSSIBLE_DUPLICATE`

until resolved.

---

# 51. DATA RECONCILIATION

When two departments provide conflicting information:

1. identify both records
2. compare timestamps
3. compare versions
4. identify ownership
5. inspect approval state
6. inspect dependencies
7. determine the authoritative state
8. preserve the superseded state
9. update affected references
10. record the resolution when important

---

# 52. DATA AUDIT

A project audit should check:

IDENTITY
□ Project ID exists

STRUCTURE
□ Sequence IDs are valid
□ Scene IDs are valid
□ Shot IDs are valid

TASKS
□ Tasks have owners
□ Tasks have statuses
□ Dependencies are valid

ASSETS
□ Assets have IDs
□ Important assets have paths
□ Versions are identifiable

CHARACTERS
□ Character IDs are stable

LOCATIONS
□ Location IDs are stable

APPROVALS
□ Approvals reference versions

QC
□ QC references real entities

RIGHTS
□ Rights records reference real assets

DELIVERY
□ Delivery records reference actual masters

ARCHIVE
□ Archive records reference actual material

---

# 53. DATA AUDIT STATUS

Use:

AUDIT_PASS

No significant structural problems found.

AUDIT_WARN

Non-critical inconsistencies exist.

AUDIT_FAIL

Important structural problems require correction.

Current Audit State:

Audit Date:

Auditor:

Open Issues:

---

# 54. COMMAND CENTER INTEGRATION

The Command Center should reference canonical IDs from this schema.

Examples:

Current Task:
TASK_032

Current Shot:
SHOT_018

Current Blocker:
BLOCK_004

Current Approval:
APR_007

Current QC:
QC_011

Current Delivery:
DEL_003

Claude should avoid creating alternate naming systems inside the Command Center.

---

# 55. DEPARTMENT INTEGRATION

Each department should use this schema while maintaining its specialist workflow.

Director:
SHOT / SCENE / CHARACTER / LOCATION

Writer:
PROJECT / SEQUENCE / SCENE / CHARACTER

Cinematography:
SHOT / CAMERA / ASSET

Production Design:
LOCATION / SET / PROP / ASSET

Casting:
CHARACTER / TALENT

AI Generation:
PROMPT / MODEL / GENERATION / ASSET / SHOT

Animation:
SHOT / CHARACTER / ASSET

Edit:
SHOT / SCENE / SEQUENCE / EDIT

VFX:
SHOT / VFX / ASSET

Sound:
SHOT / SCENE / SOUND

Music:
SCENE / SHOT / CUE

Color:
SHOT / SCENE / MASTER

Continuity:
SHOT / CHARACTER / LOCATION / PROP

Research:
SOURCE / CLAIM / SCENE / SCRIPT

Legal:
ASSET / SOURCE / RIGHTS

QC:
ENTITY / VERSION / ISSUE

Distribution:
MASTER / DELIVERY

Archive:
PROJECT / ASSET / VERSION

---

# 56. HUMAN-READABLE VS MACHINE-READABLE

Human-readable Markdown is the default studio interface.

The schema is designed so records can later be converted into:

- CSV
- JSON
- databases
- spreadsheets
- APIs
- dashboards
- automation workflows
- analytics systems

Do not design records in a way that prevents later machine processing.

---

# 57. FUTURE DATABASE COMPATIBILITY

The schema should remain compatible with a future relational or graph database.

Potential tables / collections:

projects
sequences
scenes
shots
characters
locations
props
assets
tasks
dependencies
blockers
risks
approvals
decisions
changes
prompts
models
generations
storyboards
previs
edits
vfx
sound
music_cues
color
rights
qc
deliveries
archives
handoffs
sources

Entity IDs should function as primary identifiers.

Relationships should function as foreign-key or graph connections.

---

# 58. RECORD CREATION RULE

Before creating a new record, Claude should ask:

Does this entity already exist?

If yes:
reuse its ID.

If no:
create a new ID.

Do not create duplicate entities simply because a new department is working on them.

---

# 59. RECORD UPDATE RULE

When updating a record:

1. preserve its identity
2. update only the necessary fields
3. preserve important historical information
4. update version when required
5. update modification metadata
6. identify downstream impacts
7. update affected project state

---

# 60. RECORD DELETION RULE

Do not permanently delete an important record merely because it is obsolete.

Prefer:

ARCHIVED
SUPERSEDED
CANCELLED
REJECTED
RETIRED

When deletion is genuinely necessary:

- confirm it is safe
- check dependencies
- preserve required history
- record the deletion where appropriate
- move recoverable information to `99_backup`

---

# 61. BACKUP RULE

Important information should be recoverable.

For significant changes preserve:

- previous versions
- important prompts
- rejected assets when useful
- decision history
- QC history
- rights evidence
- project structure
- final masters

The backup system exists to protect production history, not to replace active project organization.

---

# 62. FINAL DATA STANDARD

The studio data layer is successful when:

- every major entity has a stable ID
- relationships are explicit
- versions are traceable
- approvals are version-aware
- QC is entity-aware
- rights are asset-aware
- tasks are dependency-aware
- shots connect creative departments
- assets can be traced to their use
- decisions can be traced to their consequences
- changes can be traced through downstream work
- final deliverables can be traced back to source material
- archived projects remain understandable

The goal is not bureaucracy.

The goal is to make a complex AI Film Studio behave like one coherent production system.

---

# 63. CORE RULE

IDENTITY
→ determines what something is

VERSION
→ determines which state of it is being used

STATUS
→ determines where it is in the workflow

DEPENDENCY
→ determines what must happen before it can progress

APPROVAL
→ determines whether it is authorized to progress

QC
→ determines whether it meets required quality

RIGHTS
→ determines whether it can legally be used

EVIDENCE
→ determines whether the recorded state can be trusted

ARCHIVE
→ preserves the production history

This is the canonical data language of the Studio.
