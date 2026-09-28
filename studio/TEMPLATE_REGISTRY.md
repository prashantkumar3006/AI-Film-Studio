# STUDIO TEMPLATE REGISTRY

## 1. PURPOSE

The Template Registry is the central catalog of reusable templates used throughout the AI Film Studio.

It defines:

- what templates exist
- where they are stored
- what each template is used for
- which departments use them
- what inputs they require
- what outputs they produce
- which templates are approved
- how templates are versioned
- how templates are updated
- how projects inherit templates
- how reusable production knowledge is preserved

The objective is to prevent the studio from rebuilding the same production structure repeatedly.

---

# 2. CORE TEMPLATE PRINCIPLE

A template is a reusable production structure.

It should provide:

STRUCTURE
+
CONSISTENCY
+
SPEED
+
REPEATABILITY

A template should not force identical creative results.

Templates standardize process.

Projects provide creative specificity.

---

# 3. TEMPLATE CATEGORIES

Templates may include:

- PROJECT
- PROJECT_BRIEF
- PROJECT_IDENTITY
- COMMAND_CENTER
- TASK
- SCHEDULE
- MILESTONE
- RISK
- BLOCKER
- DECISION
- CHANGE
- APPROVAL
- HANDOFF
- SEQUENCE
- SCENE
- SHOT
- CHARACTER
- LOCATION
- PROP
- ASSET
- STORYBOARD
- PREVIS
- PROMPT
- AI_GENERATION
- EDIT
- VFX
- SOUND
- MUSIC
- COLOR
- RESEARCH
- CLAIM
- SOURCE
- RIGHTS
- QC
- DELIVERY
- ARCHIVE
- REPORT
- DAILY_STATUS
- WEEKLY_STATUS
- AUTOMATION
- TOOL
- MODEL
- HARDWARE
- SOFTWARE
- SCRIPT
- WORKFLOW

---

# 4. TEMPLATE RECORD

Each important template should have:

Template ID:
Template Name:
Category:
Department:
Purpose:
Description:
Inputs:
Outputs:
Required Fields:
Optional Fields:
Dependencies:
Project Types:
Version:
Status:
Owner:
Created:
Modified:
Source:
Related Templates:
Notes:

---

# 5. TEMPLATE ID SYSTEM

Recommended format:

TPL_PROJECT_001

TPL_BRIEF_001

TPL_SCENE_001

TPL_SHOT_001

TPL_CHARACTER_001

TPL_LOCATION_001

TPL_ASSET_001

TPL_TASK_001

TPL_PROMPT_001

TPL_QC_001

TPL_DELIVERY_001

TPL_ARCHIVE_001

The category should remain recognizable from the ID.

---

# 6. TEMPLATE STATUS

Use:

DRAFT

TESTING

APPROVED

ACTIVE

DEPRECATED

RETIRED

Definitions:

DRAFT
Being designed.

TESTING
Being evaluated.

APPROVED
Validated for intended use.

ACTIVE
Currently recommended.

DEPRECATED
Still preserved but should normally be replaced.

RETIRED
No longer recommended for production.

---

# 7. TEMPLATE VERSIONING

Templates should use explicit versions.

Example:

TPL_SHOT_001_v001

TPL_SHOT_001_v002

TPL_SHOT_001_v003

Major structural revision:

TPL_SHOT_001_v100

Do not silently alter an important production template.

---

# 8. TEMPLATE OWNERSHIP

Every important template should have an owner.

Owner:

Department:

Review Responsibility:

The owner is responsible for:

- validity
- maintenance
- documentation
- compatibility
- review
- deprecation decisions

---

# 9. TEMPLATE SOURCE OF TRUTH

Each template should have one authoritative source.

Possible source:

`studio/...`

or:

approved project template

or:

external tool configuration where appropriate

Do not maintain multiple contradictory copies.

---

# 10. TEMPLATE REGISTRY STRUCTURE

Recommended organization:

templates/

01_project/

02_story/

03_production/

04_shot/

05_asset/

06_ai/

07_post/

08_research/

09_rights/

10_qc/

11_delivery/

12_archive/

13_reports/

14_automation/

---

# 11. PROJECT TEMPLATE

A Project Template should define:

Project ID:
Project Title:
Project Type:
Owner:
Director:
Producer:
Target Runtime:
Target Resolution:
Frame Rate:
Aspect Ratio:
Platforms:
Languages:
Delivery Date:
Current State:
Current Phase:
Version:

---

# 12. PROJECT BRIEF TEMPLATE

Project Name:

Project Type:

Purpose:

Audience:

Logline:

Premise:

Synopsis:

Core Theme:

Tone:

Visual Direction:

Duration:

Distribution:

Research Requirements:

Creative Constraints:

Technical Constraints:

Rights Considerations:

Major Deliverables:

Success Criteria:

---

# 13. PROJECT IDENTITY TEMPLATE

Project ID:

Title:

Type:

Owner:

Studio:

Created:

Version:

State:

Phase:

Runtime:

Aspect Ratio:

Resolution:

Frame Rate:

Target Platform:

Delivery Date:

---

# 14. COMMAND CENTER TEMPLATE

Project:

Project ID:

Current State:

Current Phase:

Current Priority:

Critical Path:

Active Departments:

Completed:

Active:

Blocked:

Waiting:

Approvals:

QC:

Rights:

Delivery:

Next Action:

---

# 15. TASK TEMPLATE

Task ID:

Project:

Task:

Department:

Phase:

Owner:

Priority:

Inputs:

Outputs:

Dependencies:

Blocked By:

Blocks:

Start:

Due:

Status:

Approval:

QC:

Version:

Notes:

---

# 16. SEQUENCE TEMPLATE

Sequence ID:

Project:

Sequence Number:

Name:

Purpose:

Story Function:

Scenes:

Location:

Time:

Characters:

Estimated Duration:

Visual Direction:

Sound Direction:

Music Direction:

Edit Purpose:

Continuity:

Status:

Version:

---

# 17. SCENE TEMPLATE

Scene ID:

Project:

Sequence:

Scene Number:

Name:

Purpose:

Story Beat:

Location:

Time:

Weather:

Characters:

Props:

Costume:

Conflict:

Emotion:

Dialogue:

VO:

Visual Objective:

Sound Objective:

Music Objective:

Required Shots:

Research:

Rights:

Continuity:

Status:

Version:

---

# 18. SHOT TEMPLATE

Shot ID:

Project:

Sequence:

Scene:

Shot Number:

Name:

Purpose:

Story Beat:

Characters:

Location:

Action:

Performance:

Camera:

Lens:

Composition:

Movement:

Lighting:

Color:

Sound:

Music:

VFX:

Animation:

AI:

References:

Prompt ID:

Asset IDs:

Continuity:

Edit:

QC:

Approval:

Version:

Status:

---

# 19. CHARACTER TEMPLATE

Character ID:

Project:

Name:

Role:

Story Function:

Age:

Appearance:

Face:

Body:

Hair:

Wardrobe:

Accessories:

Voice:

Personality:

Motivation:

Goal:

Conflict:

Relationships:

Knowledge:

Emotional State:

Character Arc:

Performance:

Casting:

AI Reference:

Continuity:

Rights:

Version:

Status:

---

# 20. LOCATION TEMPLATE

Location ID:

Project:

Name:

Type:

Purpose:

Geography:

Architecture:

Era:

Materials:

Colors:

Weather:

Time:

Lighting:

Environment:

Props:

Sound:

References:

AI Reference:

VFX:

Continuity:

Rights:

Version:

Status:

---

# 21. PROP TEMPLATE

Prop ID:

Project:

Name:

Purpose:

Character:

Scene:

Shot:

Material:

Color:

Shape:

Scale:

Condition:

Historical Context:

Reference:

Continuity:

Rights:

Version:

Status:

---

# 22. ASSET TEMPLATE

Asset ID:

Project:

Name:

Type:

Department:

Source:

Creator:

Owner:

Parent Asset:

Related Shot:

Related Scene:

Related Character:

Related Location:

File Path:

Format:

Resolution:

Frame Rate:

Duration:

Checksum:

Version:

Rights:

Continuity:

QC:

Approval:

Status:

---

# 23. STORYBOARD TEMPLATE

Storyboard ID:

Project:

Sequence:

Scene:

Shot:

Panel:

Purpose:

Frame:

Camera:

Lens:

Blocking:

Action:

Character Position:

Dialogue:

Duration:

Transition:

Continuity:

Reference:

Version:

Approval:

---

# 24. PREVIS TEMPLATE

Previs ID:

Project:

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

# 25. PROMPT TEMPLATE

Prompt ID:

Project:

Department:

Purpose:

Entity:

Entity ID:

Model:

Model Version:

Prompt:

Negative Constraints:

Reference Assets:

Variables:

Settings:

Seed:

Output:

QC:

Version:

Status:

---

# 26. AI GENERATION TEMPLATE

Generation ID:

Project:

Shot:

Asset:

Prompt ID:

Model ID:

Model Version:

Reference Inputs:

Settings:

Seed:

Batch:

Output:

Selected Output:

Rejected Outputs:

Failure Modes:

QC:

Approval:

Final Asset:

Version:

---

# 27. RESEARCH TEMPLATE

Research ID:

Project:

Question:

Scope:

Time Range:

Geography:

Sources:

Primary Sources:

Secondary Sources:

Claims:

Conflicting Evidence:

Known Uncertainties:

Visual References:

Conclusion:

Confidence:

Reviewer:

Date:

Status:

---

# 28. SOURCE TEMPLATE

Source ID:

Project:

Title:

Author:

Publisher:

Source Type:

Publication Date:

Access Date:

URL / Location:

Claim Supported:

Evidence:

Reliability:

Conflicting Sources:

Notes:

Status:

---

# 29. CLAIM TEMPLATE

Claim ID:

Project:

Claim:

Category:

Source IDs:

Evidence:

Factual Status:

Confidence:

Conflicting Evidence:

Interpretation:

Required Verification:

Used In:

Status:

---

# 30. RIGHTS TEMPLATE

Rights ID:

Project:

Asset:

Asset ID:

Material:

Creator:

Source:

License:

Permission:

Usage:

Territory:

Platform:

Duration:

Attribution:

Restrictions:

Expiration:

Evidence:

Risk:

Status:

Reviewer:

---

# 31. EDIT TEMPLATE

Edit ID:

Project:

Timeline:

Version:

Stage:

Runtime:

Editor:

Source Version:

Picture:

VFX:

Sound:

Music:

Color:

Subtitles:

Current Status:

Approval:

Notes:

---

# 32. VFX TEMPLATE

VFX ID:

Project:

Shot:

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

# 33. SOUND TEMPLATE

Sound ID:

Project:

Scene:

Shot:

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

# 34. MUSIC CUE TEMPLATE

Cue ID:

Project:

Scene:

Shot Range:

Cue Name:

Purpose:

Theme:

Character:

Emotion:

Tempo:

Duration:

Start:

End:

Composer / Source:

Rights:

Stems:

Version:

Approval:

---

# 35. COLOR TEMPLATE

Color ID:

Project:

Scene:

Shot:

Source:

Color Space:

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

# 36. QC TEMPLATE

QC ID:

Project:

Target:

Target ID:

Version:

QC Type:

Reviewer:

Date:

Criteria:

Result:

Severity:

Issue:

Timecode:

Required Fix:

Owner:

Recheck:

Final Status:

---

# 37. DELIVERY TEMPLATE

Delivery ID:

Project:

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

Status:

---

# 38. ARCHIVE TEMPLATE

Archive ID:

Project:

Version:

Final Master:

Source Media:

Project Files:

AI Prompts:

Generation Logs:

Research:

Rights:

QC:

Decisions:

Changes:

Assets:

Delivery Files:

Technical Documentation:

Checksums:

Backup:

Archive Location:

Recovery Test:

Date:

Status:

---

# 39. RISK TEMPLATE

Risk ID:

Project:

Risk:

Category:

Probability:

Impact:

Severity:

Trigger:

Affected Departments:

Affected Tasks:

Affected Assets:

Mitigation:

Contingency:

Owner:

Status:

Review Date:

---

# 40. BLOCKER TEMPLATE

Blocker ID:

Project:

Description:

Category:

Severity:

Department:

Affected Task:

Affected Shot:

Affected Asset:

Affected Phase:

Root Cause:

Owner:

Missing Input:

Workaround:

Resolution:

Deadline:

Status:

---

# 41. DECISION TEMPLATE

Decision ID:

Project:

Date:

Decision:

Type:

Decision Owner:

Reason:

Alternatives:

Evidence:

Affected Departments:

Affected Entities:

Consequences:

Version:

Status:

---

# 42. CHANGE TEMPLATE

Change ID:

Project:

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

---

# 43. APPROVAL TEMPLATE

Approval ID:

Project:

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

---

# 44. HANDOFF TEMPLATE

Handoff ID:

Project:

From:

To:

Task:

Entity:

Entity ID:

Version:

Deliverables:

Inputs:

Dependencies:

Known Issues:

QC:

Rights:

Continuity:

Expected Action:

Deadline:

Received By:

Received Date:

Status:

---

# 45. TOOL TEMPLATE

Tool ID:

Tool Name:

Provider:

Category:

Department:

Purpose:

Platform:

Version:

Access:

Local / Cloud:

Input:

Output:

Formats:

Hardware:

VRAM:

RAM:

Storage:

API:

License:

Cost:

Strengths:

Limitations:

Fallback:

Status:

Last Tested:

---

# 46. AI MODEL TEMPLATE

Model ID:

Model Name:

Provider:

Version:

Modality:

Input:

Output:

Best Uses:

Weaknesses:

Reference Support:

Control Features:

Character Consistency:

Environment Consistency:

Motion:

Resolution:

Local / Cloud:

Hardware:

API:

Cost:

Rights / Terms:

Status:

---

# 47. HARDWARE TEMPLATE

Hardware ID:

Device:

Model:

Category:

CPU:

GPU:

VRAM:

RAM:

Storage:

Network:

Operating System:

Primary Use:

Secondary Use:

Capacity:

Bottlenecks:

Status:

---

# 48. SOFTWARE ENVIRONMENT TEMPLATE

Environment ID:

Name:

Operating System:

Python:

Conda:

CUDA:

Driver:

Libraries:

AI Frameworks:

Creative Applications:

Plugins:

Models:

Scripts:

Storage:

Status:

Last Verified:

---

# 49. AUTOMATION TEMPLATE

Automation ID:

Name:

Purpose:

Category:

Department:

Trigger:

Inputs:

Outputs:

Tools:

Dependencies:

Permissions:

Risk Level:

Approval:

Execution Mode:

Validation:

Error Handling:

Retry:

Rollback:

Logging:

Owner:

Version:

Status:

---

# 50. REPORT TEMPLATE

Report ID:

Project:

Report Type:

Period:

Prepared:

Prepared By:

Overall State:

Completed:

Active:

Blocked:

Waiting:

Approvals:

QC:

Risks:

Technical Issues:

Resources:

Next Actions:

Notes:

---

# 51. DAILY STATUS TEMPLATE

Date:

Project:

Overall State:

Current Phase:

Completed Today:

Currently Active:

Blocked:

Waiting:

Approvals:

Shots:

Assets:

AI Generation:

Edit:

VFX:

Sound:

Music:

Color:

QC:

Rights:

Technical:

Risks:

Next Actions:

---

# 52. WEEKLY STATUS TEMPLATE

Week:

Project:

Overall State:

Phase:

Milestones:

Completed:

Active:

Critical Path:

Blockers:

Risks:

Major Decisions:

Major Changes:

Department Status:

QC:

Rights:

Resources:

Upcoming:

Next Week:

---

# 53. MEETING TEMPLATE

Meeting ID:

Project:

Date:

Participants:

Purpose:

Topics:

Decisions:

Actions:

Owners:

Deadlines:

Risks:

Blockers:

Follow-Up:

Notes:

---

# 54. REVIEW TEMPLATE

Review ID:

Project:

Entity:

Entity ID:

Version:

Reviewer:

Date:

Purpose:

Creative Review:

Story Review:

Technical Review:

Continuity:

Research:

Rights:

QC:

Strengths:

Weaknesses:

Required Fixes:

Recommendations:

Status:

---

# 55. LESSON TEMPLATE

Lesson ID:

Project:

Department:

Date:

Problem:

What Happened:

Root Cause:

Solution:

What Worked:

What Did Not:

Reusable Knowledge:

Recommended Workflow Change:

Related Tools:

Related Prompts:

Status:

---

# 56. FAILURE TEMPLATE

Failure ID:

Project:

Department:

Entity:

Task:

Tool:

Version:

Failure:

Expected:

Actual:

Root Cause:

Impact:

Workaround:

Resolution:

Lesson:

Future Prevention:

Status:

---

# 57. TEMPLATE INHERITANCE

Projects may inherit approved studio templates.

Example:

Studio Template
→ Project Template
→ Sequence Template
→ Scene Template
→ Shot Template

Project-specific modifications should remain traceable.

Do not modify the master studio template merely because one project needs a variation.

Create a project-specific variation when necessary.

---

# 58. TEMPLATE OVERRIDES

A project may override a template.

Record:

Template:

Original Version:

Project Override:

Reason:

Affected Fields:

Approval:

Version:

The override applies only to the specified project unless promoted to the studio template system.

---

# 59. TEMPLATE PROMOTION

A project-specific template may become a studio-wide template when it proves broadly reusable.

Workflow:

PROJECT TEMPLATE

→ TESTED

→ REUSABLE

→ REVIEWED

→ GENERALIZED

→ APPROVED

→ STUDIO TEMPLATE

---

# 60. TEMPLATE DEPRECATION

When a template becomes obsolete:

mark:

DEPRECATED

and provide:

Replacement Template:

Reason:

Migration Notes:

Affected Projects:

Do not silently remove a template used by existing projects.

---

# 61. TEMPLATE MIGRATION

When replacing a template:

1. identify projects using old version
2. identify structural differences
3. create migration mapping
4. test migration
5. preserve old records
6. update project references
7. document migration
8. validate

---

# 62. TEMPLATE VALIDATION

Before approving a template verify:

□ Required fields are defined

□ Optional fields are defined

□ IDs are clear

□ Versioning is clear

□ Status values are valid

□ Dependencies are defined

□ Outputs are clear

□ Relationships are understandable

□ It can be reused

□ It does not create unnecessary bureaucracy

---

# 63. TEMPLATE TESTING

Test:

CREATE

→ POPULATE

→ UPDATE

→ VERSION

→ LINK

→ EXPORT

→ ARCHIVE

The template should remain understandable throughout the workflow.

---

# 64. TEMPLATE MACHINE COMPATIBILITY

Templates should be structured so they can later be processed programmatically.

Avoid unnecessarily ambiguous fields.

Prefer:

Status:
APPROVED

over:

Looks good now.

Prefer:

Version:
v003

over:

latest version

Prefer:

Shot ID:
SHOT_014

over:

the fourth train scene shot

---

# 65. TEMPLATE VARIABLES

Reusable templates may define variables.

Example:

{{PROJECT_ID}}

{{PROJECT_TITLE}}

{{SCENE_ID}}

{{SHOT_ID}}

{{CHARACTER_ID}}

{{LOCATION_ID}}

{{ASSET_ID}}

{{VERSION}}

{{DATE}}

{{OWNER}}

Variables should be replaced during project initialization or record creation.

---

# 66. REQUIRED VS OPTIONAL

Every template should distinguish:

REQUIRED

from

OPTIONAL

Example:

Required:

Project ID

Task ID

Task Name

Department

Status

Optional:

Notes

Reference

Secondary Owner

Do not make fields mandatory merely because they could theoretically be useful.

---

# 67. DEFAULT VALUES

Templates may define defaults.

Example:

Status:
NOT_STARTED

Version:
v001

Project State:
INTAKE

Current Phase:
INTAKE

Defaults should be documented.

---

# 68. TEMPLATE VALIDATION RULES

Where appropriate define:

Allowed values

Field formats

Required fields

ID patterns

Version format

Date format

File path rules

Status rules

Relationship rules

This allows future automation and automated validation.

---

# 69. DATE STANDARD

Use:

YYYY-MM-DD

Example:

2026-09-28

For date-time records use:

YYYY-MM-DD HH:MM

Where timezone matters, record it explicitly.

---

# 70. VERSION STANDARD

Use:

v001

v002

v003

Do not mix:

v1

1.0

final

latest

new

inside version fields unless the project explicitly requires another standard.

---

# 71. STATUS STANDARD

Use a defined vocabulary.

Do not create arbitrary alternatives such as:

working

almost done

nearly complete

finished-ish

Use canonical states from the Studio Data Schema.

---

# 72. TEMPLATE RELATIONSHIPS

Templates may reference:

- parent templates
- child templates
- related templates
- inherited templates
- replacement templates
- project overrides

Example:

TPL_SCENE_001
→ contains
TPL_SHOT_001

---

# 73. TEMPLATE DEPENDENCIES

A template may require another template.

Example:

PROJECT
→ requires
PROJECT_IDENTITY

PROJECT
→ creates
COMMAND_CENTER

SCENE
→ requires
SEQUENCE

SHOT
→ requires
SCENE

AI_GENERATION
→ requires
PROMPT

DELIVERY
→ requires
QC

---

# 74. TEMPLATE BUNDLES

Frequently used templates may be packaged together.

Example:

DOCUMENTARY_BUNDLE

includes:

Project Brief

Research

Source

Claim

Scene

Shot

Asset

Rights

QC

Delivery

Archive

---

# 75. PROJECT-TYPE TEMPLATE BUNDLES

Recommended bundles:

NARRATIVE

DOCUMENTARY

SCIENTIFIC_DOCUMENTARY

EDUCATIONAL

COMMERCIAL

MUSIC_VIDEO

ANIMATION

AI_FILM

HYBRID

SOCIAL

Each bundle should include only the templates normally required by that project type.

---

# 76. DOCUMENTARY TEMPLATE BUNDLE

Recommended:

Project

Brief

Research

Source

Claim

Scene

Shot

Archive

Rights

Interview

Asset

Continuity

QC

Delivery

---

# 77. SCIENTIFIC TEMPLATE BUNDLE

Recommended:

Project

Research

Source

Claim

Scientific Visualization

Data

Scene

Shot

Asset

AI Generation

QC

Rights

Delivery

Archive

---

# 78. AI FILM TEMPLATE BUNDLE

Recommended:

Project

Brief

Character

Location

Prop

Shot

Storyboard

Previs

Prompt

Model

Generation

Asset

Continuity

Edit

VFX

Sound

Music

Color

QC

Delivery

Archive

---

# 79. ANIMATION TEMPLATE BUNDLE

Recommended:

Project

Character

Environment

Story

Scene

Shot

Storyboard

Previs

Animation

Asset

Sound

Music

Edit

VFX

Color

QC

Delivery

Archive

---

# 80. COMMERCIAL TEMPLATE BUNDLE

Recommended:

Project

Brief

Audience

Brand

Concept

Script

Storyboard

Shot

Talent

Asset

Rights

Edit

Sound

Music

Color

QC

Delivery

Marketing

Archive

---

# 81. TEMPLATE DISCOVERY

Claude should search this registry before inventing a new structure.

Ask:

Does an approved template already solve this problem?

If yes:

reuse it.

If nearly:

adapt it carefully.

If fundamentally missing:

create a new template and register it.

---

# 82. NO DUPLICATE TEMPLATE RULE

Do not create:

SHOT_TEMPLATE_A

SHOT_TEMPLATE_B

SHOT_TEMPLATE_FINAL

when one canonical Shot Template can serve the requirement.

Different templates should exist only when their purposes differ meaningfully.

---

# 83. TEMPLATE CUSTOMIZATION

Customization should be minimal.

Prefer adding optional project-specific fields over creating completely new templates.

Create a new template when:

- purpose changes
- data structure changes significantly
- workflow differs materially
- project type requires unique fields

---

# 84. TEMPLATE QUALITY CONTROL

A template should be reviewed for:

- clarity
- completeness
- reusability
- redundancy
- consistency
- machine-readability
- human readability
- relationship integrity
- versioning
- downstream compatibility

---

# 85. TEMPLATE GOVERNANCE

The Studio Director / Operations layer should maintain overall template coherence.

Departments may propose templates.

Production may test them.

Technical Post may validate machine compatibility.

QC may validate quality requirements.

Knowledge / Archive may preserve reusable versions.

---

# 86. TEMPLATE CHANGE REQUEST

Template changes should record:

Template ID:

Current Version:

Requested By:

Date:

Requested Change:

Reason:

Affected Projects:

Compatibility:

Risk:

Test:

Approval:

New Version:

---

# 87. TEMPLATE CHANGE RULE

Do not modify a production-critical template in place when active projects depend on the previous structure.

Prefer:

old version preserved

new version created

migration documented

---

# 88. TEMPLATE ARCHIVE

Retain:

- approved versions
- deprecated versions
- retired versions
- important historical variants
- migration notes

Archived templates help reconstruct older projects.

---

# 89. TEMPLATE REPORT

Each important template may have a short report:

Template:

Current Version:

Purpose:

Used By:

Projects Using It:

Last Updated:

Last Tested:

Known Issues:

Recommended Changes:

Status:

---

# 90. TEMPLATE USAGE STATISTICS

Where practical track:

Usage Count:

Projects:

Departments:

Reused:

Modified:

Failure Rate:

Common Issues:

Last Used:

High-value templates should be prioritized for maintenance.

---

# 91. TEMPLATE PERFORMANCE

Evaluate:

Time Saved:

Error Reduction:

Consistency:

Ease of Use:

Automation Compatibility:

User Feedback:

Downstream Rework:

Template Status:

A template should exist because it provides practical value.

---

# 92. TEMPLATE FAILURE ANALYSIS

When a template causes problems:

What field was missing?

What was ambiguous?

What was unnecessary?

What caused downstream errors?

Was the template too rigid?

Was the template too loose?

Should it be modified?

Should it be retired?

Record the lesson.

---

# 93. TEMPLATE AUTOMATION

Templates may be used to automatically create:

- project files
- folders
- records
- tasks
- trackers
- reports
- checklists
- prompts
- manifests

Automation should instantiate templates without silently changing their meaning.

---

# 94. TEMPLATE GENERATION RULE

When creating an automated output from a template:

1. load template
2. populate variables
3. validate required fields
4. create output
5. assign ID
6. assign version
7. register output
8. validate relationships
9. update project state

---

# 95. TEMPLATE AND DATA SCHEMA

Templates must remain compatible with:

`studio/DATA_SCHEMA.md`

When the Data Schema changes:

review dependent templates.

When a template changes:

check schema compatibility.

These systems should evolve together.

---

# 96. TEMPLATE AND COMMAND CENTER

The Command Center may be created from a template.

Project initialization should populate:

Project identity

State

Phase

Department statuses

Task board

Shot board

Asset board

Blockers

Approvals

QC

Delivery

Archive

The template should not contain project-specific information permanently.

---

# 97. TEMPLATE AND CLAUDE

Claude should use templates to:

- create consistent records
- populate project structure
- generate production documents
- create reports
- prepare department handoffs
- initialize new projects
- construct repeatable workflows

Claude should preserve the semantics of the template.

---

# 98. TEMPLATE AND AI

AI-generated outputs should use appropriate templates for:

- prompts
- generation logs
- model records
- assets
- shots
- continuity
- QC
- rights

This keeps AI production traceable.

---

# 99. TEMPLATE AND ARCHIVE

The archive should preserve:

the template version used

plus

the project-specific populated record.

This allows future reconstruction.

---

# 100. MASTER TEMPLATE REGISTRY

Maintain this live registry:

| Template ID | Name | Category | Department | Version | Status |
|---|---|---|---|---|---|
| TPL_PROJECT_001 | Project | Project | Production | v001 | ACTIVE |
| TPL_BRIEF_001 | Project Brief | Project | Producer | v001 | ACTIVE |
| TPL_SEQUENCE_001 | Sequence | Story | Director | v001 | ACTIVE |
| TPL_SCENE_001 | Scene | Story | Director | v001 | ACTIVE |
| TPL_SHOT_001 | Shot | Shot | Cinematography | v001 | ACTIVE |
| TPL_CHARACTER_001 | Character | Character | Performance | v001 | ACTIVE |
| TPL_LOCATION_001 | Location | Environment | Production Design | v001 | ACTIVE |
| TPL_ASSET_001 | Asset | Asset | Asset Pipeline | v001 | ACTIVE |
| TPL_TASK_001 | Task | Production | Producer | v001 | ACTIVE |
| TPL_PROMPT_001 | Prompt | AI | AI Generation | v001 | ACTIVE |
| TPL_GENERATION_001 | AI Generation | AI | AI Generation | v001 | ACTIVE |
| TPL_RESEARCH_001 | Research | Research | Research | v001 | ACTIVE |
| TPL_SOURCE_001 | Source | Research | Research | v001 | ACTIVE |
| TPL_CLAIM_001 | Claim | Research | Research | v001 | ACTIVE |
| TPL_RIGHTS_001 | Rights | Legal | Legal / Rights | v001 | ACTIVE |
| TPL_QC_001 | QC | Quality | QC | v001 | ACTIVE |
| TPL_DELIVERY_001 | Delivery | Delivery | Distribution | v001 | ACTIVE |
| TPL_ARCHIVE_001 | Archive | Archive | Knowledge / Archive | v001 | ACTIVE |

Update this registry as new approved templates are created.

---

# 101. TEMPLATE AUDIT

Audit:

□ Every active template has an ID

□ Purpose is clear

□ Owner is defined

□ Version is defined

□ Status is defined

□ Required fields are defined

□ Optional fields are defined

□ Relationships are clear

□ Data Schema compatibility checked

□ Duplicate templates removed or merged

□ Deprecated templates identified

□ Project overrides documented

□ Archive versions preserved

---

# 102. FINAL TEMPLATE STANDARD

A good template should make production:

FASTER

CLEARER

MORE CONSISTENT

MORE REUSABLE

MORE TRACEABLE

MORE AUTOMATABLE

without becoming:

RIGID

REDUNDANT

CONFUSING

BUREAUCRATIC

OR UNNECESSARILY COMPLEX.

Templates are the reusable building blocks of the Studio.

The Studio should build once, learn once, and reuse intelligently.
