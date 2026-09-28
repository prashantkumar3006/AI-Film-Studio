# STUDIO COMMAND CENTER

## 1. PURPOSE

The Studio Command Center is the operational control layer for the entire AI Film Studio.

It gives Claude one place to determine:

- what project is active
- what phase the project is in
- what has been completed
- what is currently being worked on
- what is blocked
- what requires approval
- which departments are active
- which assets and shots are ready
- what dependencies exist
- what should happen next
- whether the project is actually ready for delivery

This file is a control dashboard, not a narrative description.

Claude MUST use this file together with:

- `CLAUDE.md`
- relevant department `SKILL.md` files
- the active project files
- project trackers
- asset records
- shot records
- research records
- continuity records
- legal/rights records
- QC records
- delivery records

---

# 2. COMMAND CENTER PRINCIPLE

The Studio operates as a dependency-driven production system.

The next action is determined by:

1. project phase
2. story requirements
3. production dependencies
4. blocked work
5. approvals
6. available assets
7. technical readiness
8. QC results
9. delivery requirements

Claude MUST NOT choose the next action simply because it is convenient.

Claude should choose the next valid production action that moves the project forward without violating dependencies, approvals, rights, continuity, or QC requirements.

---

# 3. ACTIVE PROJECT

Update this section whenever the active project changes.

Project ID:
Project Title:
Project Type:
Project Owner:
Studio Director:
Producer:
Current Version:
Project State:
Current Phase:
Target Runtime:
Target Resolution:
Primary Aspect Ratio:
Target Platforms:
Target Delivery Date:
Last Updated:
Last Updated By:

Possible Project States:

- INTAKE
- ACTIVE
- ON HOLD
- BLOCKED
- REVIEW
- APPROVED
- PICTURE LOCK
- FINISHING
- DELIVERY
- COMPLETED
- ARCHIVED
- CANCELLED

---

# 4. MASTER PRODUCTION STATE

Overall Production State:
Overall Health:
Current Priority:
Current Critical Path:
Current Blocker:
Next Approval:
Next Milestone:
Estimated Completion State:
Last QC State:

Allowed Health Values:

- GREEN
- YELLOW
- RED

Health meanings:

GREEN
Production is proceeding normally.

YELLOW
Production can continue, but one or more risks, dependencies, quality issues, or approvals require attention.

RED
Production is materially blocked, unsafe to proceed, or unable to advance without intervention.

Claude MUST NOT mark production GREEN when a critical blocker exists.

---

# 5. MASTER PIPELINE

The standard studio pipeline is:

INTAKE
→ RESEARCH
→ CONCEPT
→ STORY
→ SCRIPT
→ DIRECTOR DEVELOPMENT
→ PRODUCTION DESIGN
→ CASTING / TALENT
→ STORYBOARD / PREVIS
→ CINEMATOGRAPHY PLAN
→ AI GENERATION / PRODUCTION
→ ANIMATION
→ EDIT
→ VFX / MOTION
→ SOUND
→ MUSIC
→ COLOR
→ CONTINUITY
→ TECHNICAL POST
→ QC
→ LEGAL / RIGHTS CHECK
→ DELIVERY
→ MARKETING
→ ARCHIVE

Not every project requires every stage.

Claude MUST activate only the departments required by the project.

Claude MUST NOT skip a required dependency merely to reach a later phase.

---

# 6. CURRENT PHASE CONTROL

Current Phase:

Phase Objective:

Phase Start:

Phase Target Completion:

Required Inputs:

Required Outputs:

Current Phase Status:

Phase Owner:

Dependencies:

Blockers:

Approval Required:

Approval Status:

Next Phase:

Phase Transition Rule:

A phase may advance only when its required deliverables and approval conditions have been satisfied.

---

# 7. DEPARTMENT DASHBOARD

Use this table as the master department status board.

| Department | Status | Current Task | Owner | Dependency | Blocker | Approval | Version |
|---|---|---|---|---|---|---|---|
| Director | NOT STARTED | | | | | | |
| Producer | NOT STARTED | | | | | | |
| Writer | NOT STARTED | | | | | | |
| Production Design | NOT STARTED | | | | | | |
| Casting & Talent | NOT STARTED | | | | | | |
| Storyboard / Previs | NOT STARTED | | | | | | |
| Cinematography | NOT STARTED | | | | | | |
| Research | NOT STARTED | | | | | | |
| AI Generation | NOT STARTED | | | | | | |
| Animation | NOT STARTED | | | | | | |
| Production Management | NOT STARTED | | | | | | |
| Asset Pipeline | NOT STARTED | | | | | | |
| Edit | NOT STARTED | | | | | | |
| VFX / Motion | NOT STARTED | | | | | | |
| Sound | NOT STARTED | | | | | | |
| Music | NOT STARTED | | | | | | |
| Color | NOT STARTED | | | | | | |
| Continuity | NOT STARTED | | | | | | |
| Technical Post | NOT STARTED | | | | | | |
| Legal / Rights | NOT STARTED | | | | | | |
| QC | NOT STARTED | | | | | | |
| Distribution | NOT STARTED | | | | | | |
| Marketing | NOT STARTED | | | | | | |
| Knowledge / Archive | NOT STARTED | | | | | | |

Allowed department statuses:

- NOT STARTED
- READY
- ACTIVE
- WAITING
- BLOCKED
- REVIEW
- APPROVED
- COMPLETE
- ON HOLD

---

# 8. PRIORITY QUEUE

Claude MUST maintain a short operational priority queue.

## P0 — Critical

Tasks that block the project or threaten final delivery.

## P1 — High

Tasks on the critical path or required for the current phase.

## P2 — Normal

Important tasks that can proceed without blocking major production.

## P3 — Optional

Useful improvements that do not affect core completion.

Current Priority Queue:

| Priority | Task ID | Task | Department | Dependency | Status |
|---|---|---|---|---|---|
| P0 | | | | | |
| P1 | | | | | |
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

Claude should not spend substantial effort on P3 work while P0 blockers remain unresolved.

---

# 9. MASTER TASK BOARD

All important production tasks should have unique IDs.

Task ID:
Task Name:
Department:
Phase:
Priority:
Owner:
Inputs:
Expected Output:
Dependencies:
Status:
Version:
Created:
Updated:
Approval Required:
Approval State:
QC Required:
QC State:
Notes:

Allowed task statuses:

- NOT STARTED
- READY
- ACTIVE
- WAITING
- BLOCKED
- REVIEW
- APPROVED
- COMPLETE
- CANCELLED

Completion requires evidence.

A task is NOT COMPLETE merely because Claude generated instructions for it.

---

# 10. SHOT BOARD

The shot is the primary production unit for visual work.

Each significant shot should have a unique Shot ID.

Shot ID:
Sequence:
Scene:
Shot Number:
Purpose:
Story Beat:
Characters:
Location:
Time:
Camera:
Lens:
Movement:
Lighting:
Composition:
Performance:
Dialogue / VO:
Sound:
Music:
VFX:
AI Generation:
Animation:
Continuity Requirement:
Source Asset:
Current Version:
Status:
Approval:
QC:
Notes:

Allowed shot statuses:

- PLANNED
- STORYBOARD
- PREVIS
- READY_TO_GENERATE
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

Claude MUST avoid generating shots without sufficient shot context.

---

# 11. ASSET BOARD

Every major asset should have an Asset ID.

Asset ID:
Asset Type:
Asset Name:
Project:
Source:
Department:
Owner:
Version:
File Location:
Format:
Resolution:
Dependencies:
Rights Status:
Continuity Status:
QC Status:
Approval:
Usage:
Current State:

Major asset categories:

- CHARACTER
- LOCATION
- SET
- PROP
- COSTUME
- VEHICLE
- ENVIRONMENT
- ARCHIVAL
- IMAGE
- VIDEO
- AUDIO
- MUSIC
- VOICE
- VFX
- ANIMATION
- GRAPHICS
- TITLE
- MAP
- DATA VISUALIZATION
- DOCUMENT
- AI GENERATED
- EDIT MASTER
- AUDIO MASTER
- COLOR MASTER
- DELIVERY MASTER

---

# 12. CHARACTER STATE

For each important character:

Character ID:
Name:
Role:
Age / Apparent Age:
Appearance:
Wardrobe:
Hair:
Makeup:
Physical Traits:
Personality:
Motivation:
Current Emotional State:
Character Arc:
Relationships:
Voice:
Reference Assets:
AI Character Reference:
Continuity Status:
Casting Status:
Performance Status:
Current Version:

Claude MUST maintain character consistency across:

- face
- body
- age
- clothing
- hair
- accessories
- voice
- behavior
- emotional state
- physical environment
- lighting context
- time period

---

# 13. LOCATION STATE

Location ID:
Location Name:
Type:
Description:
Architecture:
Geography:
Era:
Weather:
Time:
Lighting:
Color Palette:
Materials:
Props:
Environmental Details:
Reference Images:
Generated Assets:
Continuity Status:
Current Version:

Locations must remain visually consistent unless a deliberate story change is documented.

---

# 14. CONTINUITY STATE

Continuity categories:

- CHARACTER
- COSTUME
- HAIR / MAKEUP
- PROP
- LOCATION
- GEOGRAPHY
- TIME
- WEATHER
- LIGHTING
- CAMERA
- SCREEN DIRECTION
- PERFORMANCE
- SOUND
- MUSIC
- VFX
- COLOR
- AI APPEARANCE
- STORY INFORMATION

Current Continuity State:

Overall Status:

Open Continuity Issues:

| Issue ID | Category | Description | Shot / Scene | Severity | Owner | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

No final approval should occur while unresolved critical continuity errors remain.

---

# 15. DEPENDENCY GRAPH

Every major task should identify what it requires and what depends on it.

Format:

Task A
→ requires
Task B
→ enables
Task C

Dependency Record:

Dependency ID:
Upstream Task:
Downstream Task:
Required Asset:
Required Decision:
Required Approval:
Status:
Impact:

Dependency states:

- SATISFIED
- WAITING
- BLOCKED
- NOT APPLICABLE

Claude MUST inspect dependencies before starting downstream work.

---

# 16. BLOCKER BOARD

A blocker is anything preventing valid progress.

| Blocker ID | Description | Department | Severity | Blocking Task | Owner | Action | Status |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Severity:

CRITICAL
Stops major production.

HIGH
Stops an important workflow.

MEDIUM
Slows production but allows partial progress.

LOW
Minor inconvenience.

For each blocker Claude should determine:

What is blocked?

Why is it blocked?

Who owns the resolution?

What input is missing?

Can parallel work continue?

What is the minimum action required to unblock it?

---

# 17. APPROVAL GATES

Approvals must be explicit.

Possible approval gates:

1. Project Brief Approval
2. Research Approval
3. Story Approval
4. Script Approval
5. Director Treatment Approval
6. Production Design Approval
7. Casting Approval
8. Storyboard Approval
9. Previs Approval
10. AI Reference Approval
11. Production Readiness Approval
12. Rough Cut Approval
13. Fine Cut Approval
14. Picture Lock
15. VFX Approval
16. Sound Approval
17. Music Approval
18. Color Approval
19. Technical Approval
20. Legal / Rights Approval
21. Final QC Approval
22. Delivery Approval
23. Archive Approval

Approval Record:

Gate ID:
Gate Name:
Required By:
Submitted Version:
Reviewer:
Status:
Comments:
Date:
Next Action:

Allowed states:

- NOT READY
- READY FOR REVIEW
- IN REVIEW
- CHANGES REQUIRED
- APPROVED
- REJECTED

Claude must never silently convert `READY FOR REVIEW` into `APPROVED`.

---

# 18. DECISION CONTROL

Important creative and production decisions should be recorded.

Decision ID:
Date:
Decision:
Reason:
Alternatives Considered:
Decision Owner:
Departments Affected:
Assets Affected:
Shots Affected:
Version:
Consequences:

Examples of decisions:

- visual style
- camera language
- aspect ratio
- narration style
- AI model
- character design
- location design
- music direction
- edit structure
- color grade
- distribution format

Major decisions should not be repeatedly reconsidered without a documented reason.

---

# 19. CHANGE CONTROL

Every significant change should be traceable.

Change ID:
Requested By:
Date:
Original State:
Requested Change:
Reason:
Affected Departments:
Affected Shots:
Affected Assets:
Dependencies:
Risk:
Approved By:
Implementation Status:
New Version:

Potential change impact categories:

- STORY
- SCRIPT
- CHARACTER
- LOCATION
- SHOT
- ASSET
- EDIT
- SOUND
- MUSIC
- VFX
- COLOR
- RIGHTS
- TECHNICAL
- DELIVERY
- MARKETING

Claude should identify downstream consequences before accepting major changes.

---

# 20. RESEARCH STATE

Research Status:
Research Question:
Current Evidence Level:
Open Questions:
Important Sources:
Conflicting Sources:
Claims Requiring Verification:
Visual References:
Historical Accuracy Status:
Technical Accuracy Status:

For documentary, scientific, educational, historical, or factual projects, research state is mandatory.

Claims should be traceable to sources.

Claude must distinguish:

- verified fact
- source-reported claim
- interpretation
- reconstruction
- inference
- speculation
- fictionalization

---

# 21. RIGHTS STATE

Rights Status:

Required rights categories:

- MUSIC
- FOOTAGE
- PHOTOGRAPHS
- ARCHIVAL MATERIAL
- STOCK
- FONTS
- LOGOS
- TRADEMARKS
- TALENT
- INTERVIEWS
- VOICES
- AI-GENERATED MATERIAL
- MODEL / SOFTWARE TERMS
- DATA
- MAPS
- QUOTATIONS
- SCREENSHOTS
- THIRD-PARTY MATERIAL

Open Rights Issues:

| Rights ID | Asset | Right Needed | Source | Status | Restriction |
|---|---|---|---|---|---|
| | | | | | |

No asset should be treated as legally cleared merely because it is technically usable.

---

# 22. AI GENERATION STATE

AI Generation Status:

Active Model(s):
Purpose:
Generation Type:
Prompt Version:
Reference Version:
Control Inputs:
Generation Count:
Selected Assets:
Rejected Assets:
Known Failure Modes:
Current Model Limitations:
Human Review:
Continuity Review:
Rights Review:

AI assets should record:

- model/tool
- model version where available
- prompt
- negative constraints where applicable
- reference assets
- generation settings where available
- seed or reproducibility information where available
- date
- selected output
- rejected output
- approval state

AI generation is a production process, not random asset creation.

---

# 23. EDIT STATE

Edit Version:
Edit Stage:
Timeline Length:
Scenes Complete:
Shots Complete:
Missing Shots:
Placeholder Assets:
Dialogue Status:
Music Status:
Sound Status:
VFX Status:
Color Status:
Continuity Status:
Editorial Issues:
Current Approval:

Edit stages:

- ASSEMBLY
- ROUGH CUT
- FINE CUT
- REVIEW
- PICTURE LOCK

A picture cannot be considered locked while unresolved structural edit changes remain.

---

# 24. VFX / MOTION STATE

VFX Status:
Shots Requiring VFX:
Shots In Progress:
Shots Complete:
Motion Graphics Status:
Titles Status:
Lower Thirds:
Maps:
Infographics:
Tracking:
Roto:
Cleanup:
Compositing:
AI Artifact Review:
VFX Approval:

---

# 25. SOUND STATE

Dialogue Status:
Voice-Over Status:
Room Tone:
Ambience:
Foley:
SFX:
Music:
Sound Design:
Mix:
Spatial / Stereo:
Audio QC:
Final Audio Master:

Sound must be evaluated in relation to the picture, pacing, dialogue, and emotional structure.

---

# 26. MUSIC STATE

Score Status:
Music Direction:
Themes:
Leitmotifs:
Open Cues:
Temp Music:
Original Score:
Licensed Music:
Music Rights:
Music Edit:
Stems:
Final Music:

Music should be tracked as both a creative and rights-managed asset.

---

# 27. COLOR STATE

Color Status:
Technical Normalization:
Color Space:
Look Development:
Scene Matching:
Skin Tone Review:
VFX Integration:
Archival Treatment:
Grain / Texture:
HDR / SDR:
Color QC:
Master Version:

---

# 28. TECHNICAL POST STATE

Technical Environment:
Editing Software:
VFX Software:
Color Software:
Audio Software:
AI Tools:
GPU / Compute:
Storage:
Working Drive:
Cache:
Proxy State:
Render State:
Codec:
Frame Rate:
Resolution:
Color Management:
Audio Sample Rate:
Backup State:

Technical blockers:

| Issue | Impact | Severity | Workaround | Owner | Status |
|---|---|---|---|---|---|

---

# 29. QC STATE

Overall QC Status:

Creative QC:
Technical QC:
Continuity QC:
Factual QC:
Rights QC:
Audio QC:
Color QC:
Subtitle QC:
Caption QC:
Accessibility QC:
Delivery QC:

Open QC Issues:

| QC ID | Category | Severity | Timecode / Asset | Problem | Required Fix | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

Severity:

CRITICAL
Must be fixed before delivery.

HIGH
Should be fixed before approval.

MEDIUM
Requires review.

LOW
Minor issue.

QC must be re-run after significant fixes.

---

# 30. DELIVERY STATE

Delivery Status:

Master:
Master Version:
Resolution:
Frame Rate:
Aspect Ratio:
Codec:
Audio:
Subtitles:
Captions:
Languages:
Credits:
Metadata:
Thumbnail:
Poster:
Trailer:
Legal Clearance:
Final QC:
Checksum / Integrity:
Destination:

Delivery targets:

| Platform / Destination | Format | Aspect | Resolution | Audio | Subtitle | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

---

# 31. MARKETING STATE

Marketing Status:
Audience:
Positioning:
Core Message:
Trailer:
Teaser:
Short Clips:
Social Assets:
Thumbnail:
Poster / Key Art:
Description:
Tags / Keywords:
Credits:
Campaign Assets:
Rights Review:
Approval:
Distribution Schedule:

Marketing claims must remain consistent with the actual project.

---

# 32. ARCHIVE STATE

Archive Status:
Project Archive:
Source Media:
Masters:
Project Files:
Scripts:
Research:
Prompts:
AI Generation Logs:
Asset Manifest:
Rights Records:
QC Reports:
Decision Logs:
Change Logs:
Delivery Files:
Documentation:
Backup:
Recovery Test:

Archive should preserve sufficient information to understand and reproduce the project pipeline where technically possible.

---

# 33. DAILY PRODUCTION STATUS

Date:

Overall Status:

Completed Today:

Currently Active:

Blocked:

Waiting For Approval:

New Risks:

New Decisions:

New Changes:

Assets Created:

Shots Created:

Shots Approved:

Shots Rejected:

QC Issues:

Technical Issues:

Next Priority:

Tomorrow / Next Session Plan:

---

# 34. NEXT-ACTION ENGINE

When asked `next`, Claude should determine the next action using this order:

1. Resolve CRITICAL blockers.
2. Complete required approval gates.
3. Complete P0 critical-path tasks.
4. Satisfy missing dependencies.
5. Complete the current production phase.
6. Protect continuity and rights requirements.
7. Address critical QC issues.
8. Advance downstream work that is now unblocked.
9. Complete P1 tasks.
10. Perform useful P2 work.
11. Defer P3 improvements unless the core pipeline is stable.

Claude should return:

NEXT ACTION:
REASON:
DEPARTMENT:
TASK ID:
INPUTS REQUIRED:
EXPECTED OUTPUT:
DEPENDENCIES:
BLOCKERS:
APPROVAL REQUIRED:
SUCCESS CONDITION:

Claude should not answer `next` with a random creative suggestion when an operational dependency is more important.

---

# 35. STATUS COMMAND

When asked `status`, provide the current state of:

PROJECT
PHASE
PRIORITY
ACTIVE DEPARTMENTS
COMPLETED WORK
ACTIVE WORK
BLOCKERS
WAITING ITEMS
APPROVALS
QC
DELIVERY
NEXT ACTION

Do not claim a state that is not supported by project records.

---

# 36. BLOCKED COMMAND

When asked `blocked`, identify:

BLOCKER:
WHY IT EXISTS:
WHAT IT BLOCKS:
OWNER:
MISSING INPUT:
DEPENDENCIES:
AVAILABLE PARALLEL WORK:
RECOMMENDED UNBLOCK ACTION:

Do not simply report the blocker.

Determine the operational path toward resolution.

---

# 37. REVIEW COMMAND

When asked `review`, inspect the relevant project state and evaluate:

- creative quality
- technical integrity
- story clarity
- continuity
- factual accuracy where applicable
- AI artifacts
- rights status
- QC status
- delivery readiness

Separate:

PASS
ISSUE
RISK
RECOMMENDATION
REQUIRED FIX

Do not confuse a recommendation with a completed fix.

---

# 38. APPROVE COMMAND

When asked to approve something, Claude must first verify:

1. Required inputs exist.
2. Required dependencies are satisfied.
3. Required QC is complete.
4. Rights requirements are satisfied where applicable.
5. The correct version is being reviewed.
6. No known critical blocker invalidates the approval.

Then record:

Approval Gate:
Item:
Version:
Evidence:
Reviewer:
Decision:
Conditions:
Next Action:

---

# 39. HANDOFF COMMAND

When one department hands work to another, create a handoff record.

HANDOFF ID:
FROM:
TO:
PROJECT:
TASK:
ASSET:
VERSION:
DELIVERABLE:
INPUTS:
KNOWN LIMITATIONS:
OPEN ISSUES:
QC STATE:
RIGHTS STATE:
CONTINUITY STATE:
EXPECTED NEXT ACTION:

The receiving department should not have to reconstruct missing context unnecessarily.

---

# 40. ARCHIVE COMMAND

When asked to archive, confirm:

- final master exists
- project files exist
- source assets are preserved
- important AI generation information is preserved
- rights records are preserved
- QC reports are preserved
- decision/change records are preserved
- delivery versions are preserved
- archive integrity is checked
- backup state is known

Archive only after the project state is accurately recorded.

---

# 41. FALSE-COMPLETION PREVENTION

Claude MUST NOT claim:

- generated when only a prompt was written
- edited when only editing instructions were provided
- rendered when no render exists
- approved when no approval occurred
- QC-passed when QC was not performed
- rights-cleared when rights were not verified
- delivered when the actual delivery did not occur
- backed up when backup has not been confirmed
- archived when archive integrity has not been confirmed

Use explicit language:

PLANNED
INSTRUCTION CREATED
READY
IN PROGRESS
GENERATED
REVIEWED
APPROVED
VERIFIED
DELIVERED
ARCHIVED

These states are not interchangeable.

---

# 42. EVIDENCE RULE

Important production state should be evidence-based.

Evidence may include:

- project files
- actual assets
- timeline versions
- render outputs
- QC reports
- approvals
- source records
- rights records
- logs
- manifests
- screenshots
- technical reports

When evidence is missing, state:

`STATUS UNVERIFIED`

Do not silently assume completion.

---

# 43. VERSION CONTROL

All meaningful deliverables should use versions.

Recommended format:

v001
v002
v003

For major locked milestones:

v100 = first approved milestone
v200 = major revision milestone

Do not overwrite an important historical state without preserving it.

The Command Center must always identify the currently authoritative version.

---

# 44. PROJECT MEMORY

The Command Center should preserve the current operational truth.

Important information should be copied or linked to the appropriate permanent project document rather than existing only in a chat message.

Permanent project knowledge should include:

- decisions
- lessons learned
- important prompts
- workflows
- recurring problems
- successful methods
- technical settings
- creative rules
- research discoveries
- asset relationships
- production history

---

# 45. CROSS-DEPARTMENT ORCHESTRATION

Claude acts as the coordination layer.

Example:

Writer changes a scene
→ Director reevaluates visual intent
→ Production Design checks environment
→ Casting / Performance checks character requirement
→ Storyboard / Previs updates shots
→ Cinematography updates camera plan
→ AI Generation updates prompts
→ Animation / VFX evaluate consequences
→ Editor checks pacing
→ Sound / Music evaluate timing
→ Continuity checks consistency
→ QC checks affected areas

A major change should propagate through affected departments.

---

# 46. PARALLEL WORK

Claude should identify work that can safely happen in parallel.

Example:

While waiting for final script approval:

- research can continue
- visual references can be collected
- production design can prepare alternatives
- asset pipeline can prepare structure
- legal can review known third-party material
- technical post can prepare the environment
- AI experiments can test non-final visual directions

Parallel work must not create expensive downstream rework unnecessarily.

---

# 47. CRITICAL PATH

The Command Center should maintain an approximate critical path.

Critical Path:

Task 1:
↓
Task 2:
↓
Task 3:
↓
Task 4:
↓
Task 5:
↓
Delivery

A task belongs to the critical path when delay in that task materially delays the project.

Claude should prioritize critical-path visibility over raw task count.

---

# 48. RISK REGISTER

| Risk ID | Risk | Probability | Impact | Severity | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Risk categories:

- STORY
- CREATIVE
- SCHEDULE
- BUDGET
- AI
- TECHNICAL
- RIGHTS
- TALENT
- DATA
- CONTINUITY
- QUALITY
- DELIVERY
- STORAGE
- SECURITY

Claude should identify major risks early rather than after failure.

---

# 49. RESOURCE STATE

Compute:
GPU:
CPU:
RAM:
Storage:
Network:
Cloud:
AI Credits:
Software:
Licenses:
Human Contributors:
External Vendors:

Resource Constraints:

Resource bottlenecks should be connected to scheduling decisions.

---

# 50. AUTOMATION STATE

Automation opportunities:

- project initialization
- task generation
- folder creation
- asset naming
- metadata generation
- prompt logging
- render queues
- file validation
- checksum generation
- proxy generation
- QC checklists
- report generation
- archive preparation
- delivery packaging

Automation must not bypass approval, rights, continuity, or QC controls.

---

# 51. COMMUNICATION PROTOCOL

Claude should communicate operational states using explicit labels.

Use:

`STATE`
`TASK`
`BLOCKER`
`DEPENDENCY`
`DECISION`
`APPROVAL`
`CHANGE`
`RISK`
`QC`
`HANDOFF`
`NEXT ACTION`

Example:

STATE
Production is in storyboard/previs.

BLOCKER
Final location design is not approved.

DEPENDENCY
Shot 021 requires the final location design.

NEXT ACTION
Complete location design review before finalizing Shot 021.

---

# 52. COMMAND PROTOCOL

Supported studio commands include:

`status`
Show current production state.

`next`
Determine the next valid production action.

`blocked`
Show blockers and resolution paths.

`review`
Review the specified project, sequence, scene, shot, asset, or department.

`approve`
Process an approval gate.

`handoff`
Create a department handoff.

`archive`
Prepare and verify project archiving.

`make it`
Convert an approved plan into execution-ready tasks.

`pastable`
Return the requested artifact as one complete pasteable file/block.

`update command center`
Reconcile the dashboard with the latest project state.

---

# 53. UPDATE RULES

The Command Center should be updated whenever there is a meaningful:

- task completion
- blocker
- approval
- rejection
- version change
- major asset creation
- script change
- shot change
- production phase transition
- QC result
- rights decision
- delivery result
- technical failure
- major creative decision

Do not update only at the end of the project.

The Command Center should remain an accurate current-state representation.

---

# 54. INITIALIZATION

For a new project:

1. Create a Project ID.
2. Create the project structure from `studio/project-template/SKILL.md`.
3. Populate project identity.
4. Populate project brief.
5. Set the project state to `INTAKE`.
6. Identify project type.
7. Identify required departments.
8. Create initial task board.
9. Create initial dependency map.
10. Create risk register.
11. Create blocker register.
12. Create decision log.
13. Create approval gates.
14. Create asset inventory.
15. Create shot system if visual production is required.
16. Create continuity system.
17. Create rights tracker.
18. Create QC tracker.
19. Create delivery matrix.
20. Move to `ACTIVE` only when production is actually ready to begin.

---

# 55. MINIMUM PROJECT RECORD

Every active project must have:

- project identity
- project brief
- production status
- task tracker
- schedule
- milestone tracker
- decision log
- change log
- blocker register
- risk register
- asset inventory
- shot list where applicable
- continuity record
- rights record where applicable
- QC record
- delivery record
- archive record

---

# 56. COMPLETION TEST

Before marking a project `COMPLETED`, verify:

PROJECT
□ Final approved master exists

STORY
□ Final story/script state is recorded

EDIT
□ Picture lock or equivalent final edit state exists

VFX
□ Required VFX is approved

SOUND
□ Final sound master exists

MUSIC
□ Music is finalized and rights are recorded

COLOR
□ Final color/mastering is approved

CONTINUITY
□ Major continuity issues are resolved

RESEARCH
□ Required factual verification is complete

RIGHTS
□ Required rights are verified

QC
□ Final QC is complete

TECHNICAL
□ Delivery files are technically valid

DISTRIBUTION
□ Required deliverables are created

MARKETING
□ Required marketing assets are complete

ARCHIVE
□ Project archive exists

BACKUP
□ Required backup state is confirmed

KNOWLEDGE
□ Important lessons and reusable knowledge are preserved

Only then should the project state become:

`COMPLETED`

---

# 57. COMMAND CENTER CORE LOOP

Claude should continuously reason through this loop:

OBSERVE
↓
UNDERSTAND CURRENT STATE
↓
IDENTIFY MISSING INFORMATION
↓
CHECK DEPENDENCIES
↓
CHECK BLOCKERS
↓
CHECK APPROVALS
↓
IDENTIFY CRITICAL PATH
↓
SELECT NEXT VALID ACTION
↓
EXECUTE OR DELEGATE
↓
VERIFY RESULT
↓
UPDATE STATE
↓
REPEAT

---

# 58. STUDIO CONTROL PRINCIPLE

The Studio Command Center is the source of operational truth for the active production state.

Department files define how work should be performed.

Project files define what the project contains.

The Command Center defines what is happening now.

Claude must use all three layers together:

STUDIO OPERATING SYSTEM
→ how the studio operates

DEPARTMENT SKILLS
→ how specialist work is performed

PROJECT COMMAND CENTER
→ what is currently happening

PROJECT FILES
→ the actual project evidence

---

# 59. FINAL COMMAND CENTER STANDARD

The Command Center must always answer five questions:

1. WHERE ARE WE?
2. WHAT IS DONE?
3. WHAT IS BLOCKED?
4. WHAT NEEDS TO HAPPEN NEXT?
5. WHAT EVIDENCE PROVES THE CURRENT STATE?

If any of these cannot be answered confidently, Claude should identify the missing information rather than inventing it.

The Command Center exists to keep the entire AI Film Studio aligned, traceable, dependency-aware, and execution-ready from the first idea to the final archive.
