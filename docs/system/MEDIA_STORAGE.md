# STUDIO MEDIA & STORAGE SYSTEM

## 1. PURPOSE

The Media & Storage System defines how the AI Film Studio stores, organizes, transfers, protects, versions, backs up, archives, and retrieves production media and project data.

It governs:

- raw media
- generated media
- project files
- proxies
- caches
- renders
- masters
- audio
- images
- image sequences
- AI outputs
- metadata
- research material
- documents
- backups
- archives
- delivery packages
- storage locations
- file transfers
- naming
- manifests
- checksums
- recovery

The objective is:

KEEP MEDIA SAFE

KEEP MEDIA FINDABLE

KEEP MEDIA TRACEABLE

KEEP MEDIA USABLE

KEEP MEDIA RECOVERABLE

---

# 2. CORE STORAGE PRINCIPLE

GitHub is primarily a knowledge, code, configuration, documentation, and version-control environment.

It is not automatically the primary storage location for large production media.

The studio should separate:

KNOWLEDGE

CODE

CONFIGURATION

PROJECT DATA

MEDIA

CACHE

BACKUP

ARCHIVE

DELIVERY

Each should have an appropriate storage location.

---

# 3. STORAGE LAYERS

The studio uses the following conceptual layers:

## LAYER 1 — KNOWLEDGE

Examples:

- CLAUDE.md
- SKILL.md
- Command Center
- Data Schema
- Prompt System
- Tool Registry
- templates
- reports
- documentation

Primary location:

GitHub / studio knowledge repository

---

## LAYER 2 — PROJECT DATA

Examples:

- project records
- shot lists
- asset inventories
- task trackers
- schedules
- decision logs
- QC records
- rights records

Location:

GitHub and/or structured project storage

---

## LAYER 3 — ACTIVE MEDIA

Examples:

- source footage
- generated images
- generated video
- audio
- project files
- image sequences
- graphics
- VFX elements

Location:

Working media storage

---

## LAYER 4 — CACHE / TEMPORARY

Examples:

- render cache
- preview files
- temporary exports
- simulation cache
- AI intermediate outputs
- application cache

Location:

Fast temporary storage

These files should not automatically be treated as archival material.

---

## LAYER 5 — BACKUP

Copies of important production information.

Location:

Independent backup storage

---

## LAYER 6 — ARCHIVE

Long-term preservation of completed project information.

---

## LAYER 7 — DELIVERY

Approved outputs prepared for specific destinations.

---

# 4. STORAGE PRINCIPLE

Do not confuse:

WORKING FILE

with

MASTER

with

BACKUP

with

ARCHIVE

with

DELIVERY

They serve different purposes.

---

# 5. STORAGE CLASSES

Classify storage as:

LOCAL

Fast storage directly attached to the workstation.

NETWORK

NAS or shared network storage.

CLOUD

Remote storage service.

HPC

High-performance compute storage.

ARCHIVE

Long-term preservation.

BACKUP

Recovery-oriented copy.

REMOVABLE

Portable storage such as external drives.

TEMPORARY

Disposable working storage.

---

# 6. STORAGE RECORD

Storage ID:
Name:
Type:
Location:
Capacity:
Usable Capacity:
Interface:
Read Speed:
Write Speed:
Network:
Encryption:
Backup:
Redundancy:
Primary Use:
Secondary Use:
Archive Use:
Recovery:
Owner:
Status:
Last Checked:

---

# 7. STORAGE INVENTORY

Maintain a live inventory.

| Storage ID | Name | Type | Capacity | Primary Use | Status |
|---|---|---|---:|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

---

# 8. PROJECT STORAGE ROOT

Every project should have one defined root.

Example:

PROJECT_ROOT

or:

PROJECT_2026_001

All project paths should resolve relative to the project root where practical.

Avoid hard-coding random workstation-specific paths into project documentation.

---

# 9. PROJECT STORAGE STRUCTURE

Recommended structure:

PROJECT_ROOT/

00_admin/

01_research/

02_story/

03_script/

04_director/

05_production-design/

06_casting/

07_storyboard-previs/

08_cinematography/

09_ai-generation/

10_animation/

11_production/

12_edit/

13_vfx-motion/

14_sound/

15_music/

16_color/

17_continuity/

18_technical/

19_legal-rights/

20_qc/

21_distribution/

22_marketing/

23_knowledge/

24_archive/

99_backup/

---

# 10. MEDIA SUBSTRUCTURE

Within relevant production folders, use consistent media subdivisions.

Recommended:

01_source

02_ingest

03_working

04_selects

05_proxies

06_intermediate

07_output

08_approved

09_archive

99_backup

Not every department requires every folder.

---

# 11. SOURCE MEDIA

SOURCE means original or original-equivalent input material.

Examples:

- camera footage
- recorded audio
- original photographs
- supplied graphics
- downloaded licensed media
- original documents
- approved reference files
- source datasets

Source media should be treated as protected.

Do not modify source files destructively unless unavoidable and documented.

---

# 12. SOURCE PRESERVATION

For important source material:

INGEST

→ VERIFY

→ REGISTER

→ BACKUP

→ WORK FROM COPY / PROJECT LINK

Where possible preserve an untouched source copy.

---

# 13. INGEST WORKFLOW

NEW MEDIA

→ COPY / IMPORT

→ VERIFY TRANSFER

→ INSPECT

→ ASSIGN ASSET ID

→ RECORD METADATA

→ CHECKSUM IF REQUIRED

→ BACKUP

→ REGISTER

→ RELEASE TO PRODUCTION

---

# 14. INGEST VERIFICATION

After ingest verify:

□ file exists

□ file opens

□ expected duration

□ expected resolution

□ expected frame rate

□ expected audio

□ expected number of files

□ no obvious corruption

□ transfer completed

□ source location recorded

---

# 15. CHECKSUMS

Important files may use checksums.

Record:

File:
Algorithm:
Checksum:
Date:
Purpose:

Possible algorithms may include:

SHA-256

SHA-512

MD5 where compatibility requires it

For critical archival integrity, use an appropriate modern cryptographic hash.

---

# 16. CHECKSUM PURPOSE

Checksums may verify:

- transfer integrity
- archival integrity
- delivery integrity
- duplicate detection
- source identity

A checksum does not prove creative quality.

It proves file content identity for the chosen algorithm.

---

# 17. MEDIA NAMING STANDARD

Use:

PROJECT_ID

ENTITY_ID

DESCRIPTION

VERSION

EXTENSION

Example:

PROJECT_2026_001_SHOT_014_TRAIN_REVEAL_v003.mp4

---

# 18. MEDIA NAMING RULES

Avoid:

- spaces
- unexplained abbreviations
- random dates without context
- ambiguous numbering
- `final`
- `final2`
- `final_final`
- `latest`
- `new`
- `use_this`

Use explicit identifiers.

---

# 19. FOLDER NAMING

Use stable names.

Recommended:

lowercase

hyphen-separated

numbered project stages where appropriate

Example:

production-design

ai-generation

legal-rights

storyboard-previs

---

# 20. VERSIONING

Important files should use explicit versions.

Examples:

v001

v002

v003

Approved milestone:

v100

Major revision:

v200

Version number should describe production state, not emotional confidence.

---

# 21. MASTER FILES

A master is an approved high-quality source used to create downstream deliverables.

Examples:

- picture master
- audio master
- color master
- VFX master
- subtitle master
- graphics master

Each master should have:

Master ID:
Version:
Approval:
QC:
Rights:
Location:
Checksum:
Date:

---

# 22. APPROVED MASTER PRINCIPLE

There should be a clearly identified authoritative master.

Do not let multiple files be treated as the final master without explicit distinction.

Use:

CURRENT_MASTER

APPROVED_MASTER

ARCHIVED_MASTER

---

# 23. DELIVERY FILES

Delivery files are derived from approved masters.

A delivery file may differ in:

- codec
- resolution
- aspect ratio
- bitrate
- language
- subtitle
- audio configuration

Delivery files must remain traceable to the approved master.

---

# 24. SOURCE → MASTER → DELIVERY

The production lineage should be:

SOURCE

→ WORKING

→ INTERMEDIATE

→ MASTER

→ DELIVERY

Each important transition should remain traceable.

---

# 25. PROXY SYSTEM

Proxies are lower-resource representations used for efficient editing or review.

A proxy should record:

Source Asset:

Proxy Asset:

Resolution:

Codec:

Frame Rate:

Audio:

Creation Date:

Software:

Version:

Relationship:

---

# 26. PROXY RULE

Proxies must remain linked to the original source.

A proxy is not automatically an archival master.

Do not substitute proxy media for source media without explicit authorization.

---

# 27. CACHE SYSTEM

Cache files may include:

- render cache
- preview cache
- shader cache
- simulation cache
- AI intermediate cache
- application cache
- temporary thumbnails

Caches may usually be regenerated.

However, before deletion determine whether a cache contains unique work that cannot easily be reproduced.

---

# 28. TEMPORARY FILES

Temporary files should be clearly identifiable.

Examples:

tmp

preview

cache

scratch

test

temp

Do not allow temporary material to become indistinguishable from final material.

---

# 29. AI MEDIA STORAGE

AI-generated media should be separated into:

01_inputs

02_prompts

03_generation

04_selected

05_rejected

06_post

07_approved

08_archive

This structure may be adapted to the project's needs.

---

# 30. AI GENERATION STORAGE

For each important AI generation preserve where practical:

- input references
- prompt
- model
- model version
- workflow
- settings
- seed where applicable
- generation date
- output
- selected output
- QC
- approval

---

# 31. AI REJECTED OUTPUTS

Rejected outputs may be preserved when they contain useful knowledge.

Use cases:

- failure analysis
- comparison
- prompt development
- future model testing
- creative decision history

Do not preserve every failed generation indefinitely when it provides no useful value.

---

# 32. AI PROVENANCE

Important AI assets should resolve:

ASSET_ID

→ GENERATION_ID

→ PROMPT_ID

→ MODEL_ID

→ INPUT_REFERENCES

→ OUTPUT

This creates traceability.

---

# 33. IMAGE STORAGE

For important image assets record:

Format

Resolution

Color Profile

Bit Depth

Alpha

Source

Version

Asset ID

Rights

QC

Images intended for print, editorial, VFX, or web may require different technical specifications.

---

# 34. VIDEO STORAGE

Record:

Resolution

Frame Rate

Codec

Bit Depth

Color Space

Duration

Audio

Aspect Ratio

Source

Version

Asset ID

QC

---

# 35. AUDIO STORAGE

Record:

Sample Rate

Bit Depth

Channel Layout

Codec

Duration

Source

Version

Asset ID

Rights

QC

---

# 36. IMAGE SEQUENCE STORAGE

For image sequences:

Sequence ID:

First Frame:

Last Frame:

Frame Rate:

Format:

Resolution:

Color:

Bit Depth:

Missing Frames:

Duplicate Frames:

Path:

Version:

QC:

---

# 37. FRAME SEQUENCE VALIDATION

Before using a sequence:

□ first frame exists

□ last frame exists

□ expected range exists

□ no unexpected gaps

□ no duplicate frame numbers

□ consistent resolution

□ consistent format

□ consistent color

□ naming is valid

---

# 38. PROJECT FILE STORAGE

Project files include:

- editing projects
- VFX projects
- audio projects
- color projects
- animation projects
- design files
- 3D scenes
- compositing files
- workflow files

Record application and version.

Example:

APPLICATION:
Premiere Pro

VERSION:
verified installed version

PROJECT:
sequence_edit

PROJECT_VERSION:
v014

---

# 39. SOFTWARE PROJECT COMPATIBILITY

Before upgrading software, consider:

Can the project still open?

Are plugins compatible?

Are media links preserved?

Did color management change?

Did effects change?

Did fonts change?

Did audio behavior change?

Did AI integrations change?

Important projects should not be casually migrated without testing.

---

# 40. MEDIA RELINKING

When moving media:

record:

Old Path:

New Path:

Asset ID:

Project:

Date:

Reason:

Verification:

Update project references where required.

---

# 41. PATH PORTABILITY

Where possible use:

relative paths

project-root variables

environment variables

central configuration

Avoid embedding personal machine paths such as:

C:\Users\Someone\Desktop\film_final\...

unless the path is intentionally machine-specific.

---

# 42. ENVIRONMENT VARIABLES FOR STORAGE

Examples:

PROJECT_ROOT

MEDIA_ROOT

CACHE_ROOT

PROXY_ROOT

ARCHIVE_ROOT

BACKUP_ROOT

DELIVERY_ROOT

Avoid storing secret values in these settings.

---

# 43. CROSS-MACHINE WORKFLOW

For moving a project between machines:

1. identify project root
2. collect project files
3. collect required media
4. collect plugins
5. collect fonts where licensed
6. collect workflow files
7. collect AI configuration where appropriate
8. collect project manifests
9. verify paths
10. test project
11. update environment record

---

# 44. MEDIA MANIFEST

A manifest should contain:

Asset ID

Filename

Path

Size

Checksum

Version

Type

Resolution

Frame Rate

Duration

Source

Rights

QC

Status

A manifest is useful for large projects and archives.

---

# 45. DIRECTORY MANIFEST

For large projects create:

Project:

Generated:

Root:

Folders:

Files:

Total Size:

File Count:

Checksum Policy:

Missing Files:

Unexpected Files:

Status:

---

# 46. DUPLICATE DETECTION

Potential duplicates may be detected using:

- filename
- size
- checksum
- metadata
- visual comparison where appropriate

Do not delete duplicates automatically when provenance is unclear.

Mark:

POSSIBLE_DUPLICATE

until resolved.

---

# 47. STORAGE CAPACITY

Track:

Total Capacity:

Used:

Free:

Reserved:

Projected Growth:

Expected Archive Growth:

Expected AI Generation Growth:

Expected Render Growth:

---

# 48. STORAGE THRESHOLDS

Example operational thresholds:

70%
Monitor.

85%
Action recommended.

95%
Critical.

These values are guidelines and should be adapted to the storage environment.

---

# 49. STORAGE CLEANUP

Before cleanup classify files:

SOURCE

MASTER

APPROVED

WORKING

PROXY

CACHE

TEMP

ARCHIVE

Only clearly disposable categories should be considered for automated deletion.

Never delete source or approved masters merely because storage is low.

---

# 50. CACHE CLEANUP

Safe cleanup candidates may include verified regenerable caches.

Before deleting:

□ cache identified

□ source/work remains available

□ application can regenerate cache

□ no unique data exists

□ active project is not using the cache

---

# 51. BACKUP PRINCIPLE

A backup should protect against:

- accidental deletion
- hardware failure
- corruption
- ransomware
- software failure
- human error
- project mistakes
- storage failure

A backup should not simply be another copy sitting beside the original on the same failure domain.

---

# 52. BACKUP STRATEGY

For important projects consider multiple copies across appropriately independent storage.

Conceptual structure:

PRIMARY

→ BACKUP

→ OFF-SITE / INDEPENDENT COPY

The exact implementation depends on the studio's hardware and infrastructure.

---

# 53. BACKUP PRIORITIES

Highest priority:

- source media
- approved masters
- project files
- research
- rights records
- production databases / records
- important prompts
- generation logs
- delivery masters

Lower priority:

- regenerable cache
- temporary previews
- disposable intermediates

---

# 54. BACKUP RECORD

Backup ID:

Project:

Source:

Destination:

Date:

Size:

Checksum:

Method:

Frequency:

Retention:

Verification:

Status:

---

# 55. BACKUP VERIFICATION

A backup is not considered trusted merely because the copy command succeeded.

Verify:

- files exist
- important files open
- file counts match where appropriate
- size is plausible
- checksums match where required
- restore can be performed

---

# 56. RESTORE TEST

A backup should periodically be tested by restoration.

Restore Test:

Date:

Backup:

Files Tested:

Restore Location:

Result:

Problems:

Recovery Time:

Status:

A backup that has never been tested may contain unknown recovery risk.

---

# 57. BACKUP FREQUENCY

Choose frequency based on production risk.

Possible schedules:

continuous

daily

weekly

milestone-based

manual

For high-change projects, milestone and frequent backups may be appropriate.

---

# 58. VERSIONED BACKUPS

For important project data retain historical versions.

Example:

backup_2026-09-28

backup_2026-09-29

backup_before_picture_lock

backup_before_major_change

This allows recovery from corrupted or unwanted changes.

---

# 59. ARCHIVE PRINCIPLE

Archive is not simply "old files."

An archive should preserve enough information to understand the project later.

Include where appropriate:

- final masters
- source manifests
- project files
- important source media
- prompts
- generation logs
- research
- rights
- QC
- decisions
- changes
- technical environment
- delivery files

---

# 60. ARCHIVE STRUCTURE

Recommended:

24_archive/

project_manifest/

masters/

project_files/

source_manifest/

research/

rights/

qc/

prompts/

ai_generation/

technical/

delivery/

reports/

knowledge/

checksums/

---

# 61. ARCHIVE PACKAGE

A completed project archive may contain:

PROJECT SUMMARY

PROJECT MANIFEST

FINAL MASTER

DELIVERY MASTERS

PROJECT FILES

SOURCE MANIFEST

ASSET INVENTORY

RESEARCH

RIGHTS

QC

DECISIONS

CHANGES

PROMPTS

AI GENERATION LOGS

TECHNICAL ENVIRONMENT

ARCHIVE CHECKSUMS

---

# 62. ARCHIVE MANIFEST

Archive ID:

Project:

Project Version:

Archive Date:

Included:

Excluded:

Total Size:

File Count:

Checksums:

Archive Location:

Backup Location:

Restoration Test:

Status:

---

# 63. ARCHIVE COMPLETENESS

Before archive completion verify:

□ project identity

□ final master

□ project files

□ source manifest

□ important assets

□ research

□ rights

□ QC

□ prompts

□ AI generation information

□ technical environment

□ delivery versions

□ decisions

□ changes

□ archive checksum

□ backup

---

# 64. DELIVERY PACKAGE

A delivery package should contain only approved deliverables.

Example:

DELIVERY_001/

master_video/

audio/

subtitles/

captions/

metadata/

credits/

thumbnail/

poster/

manifest/

checksums/

---

# 65. DELIVERY ISOLATION

Do not mix:

working files

with

approved delivery files

The delivery directory should represent a clean release package.

---

# 66. MEDIA TRANSFER

Before transferring large media:

check:

source

destination

available space

network

integrity method

expected duration

permissions

resume capability

After transfer:

verify

register

log

---

# 67. LARGE FILE TRANSFER

For large files consider:

- resumable transfer
- checksums
- transfer logs
- bandwidth limits
- local caching
- compression where appropriate
- transfer scheduling

Do not compress already-compressed media unless the workflow benefits.

---

# 68. NETWORK STORAGE

For NAS / shared storage record:

Server:

Share:

Protocol:

Permissions:

Capacity:

Available:

Project:

Backup:

Redundancy:

Network Speed:

Known Bottleneck:

---

# 69. CLOUD STORAGE

For cloud storage record:

Provider:

Bucket / Container:

Region where relevant:

Storage Class:

Encryption:

Access:

Lifecycle:

Transfer Cost:

Storage Cost:

Retention:

Backup:

Project:

Rights / Data Considerations:

---

# 70. CLOUD DATA TRANSFER

Before uploading sensitive project material verify:

What is being uploaded?

Where is it stored?

Who can access it?

How long is it retained?

What terms apply?

Is the material permitted to be uploaded?

Do not upload restricted project data merely because a tool accepts the file.

---

# 71. AI CLOUD STORAGE

AI services may process or retain inputs according to their terms.

Before sending sensitive media to an external AI service, verify the applicable service terms and studio requirements.

Record:

Service:

Input:

Purpose:

Retention:

Training / usage terms where relevant:

Rights:

Approval:

Status:

---

# 72. GITHUB STORAGE POLICY

GitHub is appropriate for:

- Markdown
- documentation
- code
- scripts
- prompt templates
- configuration templates
- manifests
- lightweight metadata
- version history

GitHub is generally not the primary storage for:

- massive raw footage
- large render caches
- massive image sequences
- large temporary media
- high-volume generated outputs

Use suitable media storage for those workloads.

---

# 73. GIT LARGE FILE POLICY

Large binary assets should be evaluated before being committed to a Git repository.

Consider:

- repository size
- clone time
- version history growth
- storage limits
- team workflow
- backup requirements

Use an appropriate large-file or external-storage strategy where necessary.

---

# 74. REPOSITORY HYGIENE

Do not commit:

- API keys
- passwords
- tokens
- private keys
- session credentials
- secrets
- massive cache directories
- temporary files
- unnecessary generated batches

---

# 75. PROJECT .GITIGNORE PRINCIPLE

Projects should exclude appropriate regenerable or sensitive files.

Typical candidates may include:

cache/

tmp/

preview/

logs containing secrets

local configuration

machine-specific files

large generated intermediates

The exact exclusions depend on the production workflow.

---

# 76. STORAGE SECURITY

Consider:

- authentication
- permissions
- encryption
- physical security
- backup
- network exposure
- account recovery
- credential rotation
- malware protection

Critical project storage should not be exposed unnecessarily.

---

# 77. LEAST PRIVILEGE

Users and tools should receive only the storage permissions required.

Example:

Read-only research tool

should not automatically receive:

Delete access

Write access to masters

Access to unrelated projects

---

# 78. PROJECT ISOLATION

Where practical separate projects to limit accidental contamination.

Example:

PROJECT_2026_001

should not accidentally modify:

PROJECT_2026_002

unless the relationship is intentional and documented.

---

# 79. MEDIA ACCESS

Track where useful:

Who can access:

- source
- working
- masters
- rights
- archive
- delivery

Use project-specific permissions where practical.

---

# 80. MEDIA LOCKING

When a file is being modified by a process that cannot tolerate simultaneous editing:

mark:

LOCKED

record:

Entity:

Owner:

Date:

Reason:

Expected Release:

This helps prevent conflicting edits.

---

# 81. READ-ONLY MASTERS

Approved masters should preferably be protected from accidental overwrite.

Use:

read-only

write-protected

versioned storage

or equivalent controls where appropriate.

---

# 82. MASTER REPLACEMENT

Never replace an approved master casually.

Process:

CURRENT MASTER

→ NEW VERSION

→ QC

→ APPROVAL

→ PROMOTE

→ ARCHIVE OLD MASTER

---

# 83. MEDIA CORRUPTION

If corruption is suspected:

STOP

→ isolate affected file

→ preserve evidence

→ check checksum

→ compare backup

→ identify source

→ restore if appropriate

→ verify

→ log incident

Do not overwrite the damaged original before understanding what happened.

---

# 84. MEDIA LOSS

If media is missing:

identify:

Asset ID

Last Known Location

Last Known Version

Owner

Backup

Archive

Related Project

Impact

Recovery Option

Do not assume the file was permanently lost before checking manifests and backups.

---

# 85. ORPHAN MEDIA

Orphan media is a file with no clear project or asset relationship.

Examples:

unknown_video.mp4

image_final.png

audio_new.wav

Orphan media should be:

identified

reviewed

assigned

archived

or safely removed after verification

---

# 86. STORAGE AUDIT

Audit:

□ Project root exists

□ Folder structure is correct

□ Source media is preserved

□ Masters are identifiable

□ Delivery is separated

□ Backups exist

□ Important checksums exist

□ Proxies are linked

□ Caches are identified

□ Temporary files are controlled

□ File naming is consistent

□ Permissions are appropriate

□ Storage capacity is known

---

# 87. MEDIA INVENTORY

Maintain:

| Asset ID | Filename | Type | Version | Path | Size | Checksum | Rights | QC | Status |
|---|---|---|---|---|---:|---|---|---|---|
| | | | | | | | | | |

---

# 88. STORAGE HEALTH DASHBOARD

Overall Storage State:

Primary Storage:

Free Space:

Backup State:

Archive State:

Cloud State:

Network State:

Critical Storage Issue:

Latest Backup:

Latest Restore Test:

Current Storage Risk:

---

# 89. STORAGE RISK REGISTER

Typical risks:

- insufficient capacity
- single-point-of-failure storage
- missing backup
- untested backup
- corrupted media
- disconnected media
- lost paths
- obsolete software
- cloud access loss
- credential loss
- accidental deletion
- unauthorized access
- ransomware
- repository growth
- AI generation volume

Record significant risks.

---

# 90. STORAGE GROWTH ESTIMATION

For high-volume projects estimate:

Source Media:

AI Images:

AI Video:

Audio:

VFX:

Animation:

Render Outputs:

Proxies:

Backups:

Archive:

Expected Growth:

Free Capacity:

Projected Limit:

Action Required:

---

# 91. AI STORAGE GROWTH

AI generation may create very large volumes.

Control growth by:

- limiting batch size
- deleting clearly disposable previews
- preserving selected outputs
- archiving useful failures
- separating cache
- using metadata instead of duplicate files
- moving completed media to appropriate storage

Do not preserve every output forever without a purpose.

---

# 92. STORAGE OPTIMIZATION

Possible strategies:

- proxies
- intermediate codecs
- tiered storage
- archive completed projects
- remove verified cache
- deduplicate where safe
- compress documents
- reduce unnecessary duplicates
- move cold data to archive

Do not optimize storage at the expense of source preservation.

---

# 93. COLD STORAGE

Material that is rarely accessed may move to cheaper or slower storage.

Examples:

- completed projects
- old project versions
- historical source material
- old AI experiments

Record location changes.

---

# 94. HOT STORAGE

Fast storage should prioritize:

- active editing
- active VFX
- AI generation
- rendering
- color
- audio production

Do not waste the fastest storage on material that is rarely accessed.

---

# 95. STORAGE TIERING

Example:

HOT
Active production

WARM
Recent projects

COLD
Completed projects

ARCHIVE
Long-term preservation

BACKUP
Recovery copies

The exact implementation depends on the studio infrastructure.

---

# 96. MEDIA LIFECYCLE

MEDIA CREATED

↓

REGISTERED

↓

WORKING

↓

REVIEW

↓

APPROVED

↓

MASTER

↓

DELIVERY

↓

ARCHIVE

At each stage determine whether the previous version should be retained.

---

# 97. MEDIA RETENTION

Retention should depend on:

- rights
- production value
- reproducibility
- legal requirements
- archive strategy
- storage cost
- future reuse

Do not delete historically important data merely because it is old.

---

# 98. MEDIA DELETION

Before deleting:

1. identify file
2. identify owner
3. identify dependencies
4. verify backup
5. verify archive
6. verify rights implications
7. confirm it is safe to delete
8. record deletion where required

Permanent deletion should be rare for important production data.

---

# 99. MEDIA RECOVERY

Recovery workflow:

IDENTIFY

→ FIND MANIFEST

→ FIND BACKUP

→ RESTORE

→ VERIFY

→ REGISTER

→ RELINK

→ TEST

→ DOCUMENT

---

# 100. DISASTER RECOVERY

For critical projects define:

Recovery Point Objective:

Recovery Time Objective:

Primary Failure:

Backup:

Secondary Backup:

Restore Procedure:

Responsible Person:

Validation:

Recovery Status:

---

# 101. DISASTER SCENARIOS

Plan for:

- workstation failure
- GPU failure
- storage failure
- NAS failure
- network failure
- software corruption
- accidental deletion
- repository failure
- cloud outage
- account loss
- malware
- ransomware
- physical damage

---

# 102. RECOVERY PRIORITY

In a major failure prioritize:

1. project identity
2. current project state
3. approved masters
4. project files
5. essential source
6. critical assets
7. rights / research
8. production history
9. lower-priority intermediates

---

# 103. MEDIA TRANSFER LOG

Transfer ID:

Project:

Source:

Destination:

Asset:

Version:

Size:

Start:

End:

Method:

Checksum:

Verification:

Status:

---

# 104. STORAGE CHANGE LOG

Change ID:

Date:

Project:

Old Location:

New Location:

Reason:

Affected Assets:

Affected Projects:

Verification:

Owner:

Status:

---

# 105. STORAGE INCIDENT LOG

Incident ID:

Date:

Project:

Storage:

Problem:

Affected Assets:

Impact:

Root Cause:

Recovery:

Backup Used:

Downtime:

Corrective Action:

Status:

---

# 106. STORAGE AUTOMATION

Safe automation candidates:

- asset indexing
- manifest generation
- metadata extraction
- checksum calculation
- proxy generation
- duplicate detection
- storage monitoring
- archive manifests
- delivery packaging
- cache cleanup with strict rules

Destructive deletion should require stronger controls.

---

# 107. STORAGE AUTOMATION SAFETY

Automations must verify:

- path exists
- target is expected
- file type is expected
- project is correct
- permissions are correct
- operation is reversible where possible

Never run a broad delete command against a production root without safeguards.

---

# 108. STORAGE AND CLAUDE

Claude should be able to reason about:

WHERE something is

WHAT version it is

WHO owns it

WHETHER it is approved

WHETHER it is backed up

WHETHER it is archived

WHETHER it is safe to modify

Claude should not assume filesystem access simply because a path exists in documentation.

Actual tool access must be available.

---

# 109. STORAGE AND AI GENERATION

Before large AI generation:

check:

available storage

expected output volume

working cache

selected outputs

archive policy

backup requirement

Generate within actual storage constraints.

---

# 110. STORAGE AND RENDERING

Before large rendering:

check:

output size estimate

disk capacity

render destination

temporary cache

final output

backup

cleanup policy

Do not fill primary storage with unmanaged render outputs.

---

# 111. STORAGE AND EDITING

Editing systems should use:

source media

proxies where appropriate

project files

cache

preview

approved outputs

Keep those categories distinguishable.

---

# 112. STORAGE AND VFX

VFX may require:

source plates

image sequences

simulation caches

renders

mattes

tracking data

3D scenes

textures

assets

composites

These may grow rapidly.

Track large data families separately.

---

# 113. STORAGE AND SOUND

Sound may require:

production audio

dialogue edits

Foley

SFX

ambience

music

stems

mixes

masters

Keep source recordings separate from processed outputs.

---

# 114. STORAGE AND COLOR

Color workflows may require:

camera originals

RAW

reference exports

graded masters

LUTs

CDLs

color project files

still references

master exports

Preserve color-critical metadata.

---

# 115. STORAGE AND RESEARCH

Research projects may contain:

papers

documents

notes

datasets

references

screenshots

archives

source records

Store them so their provenance remains identifiable.

---

# 116. STORAGE AND RIGHTS

Rights records should remain linked to assets.

Do not separate a cleared asset from the information explaining why it may be used.

---

# 117. STORAGE AND QC

QC records should point to exact:

Asset

Version

Master

Delivery

Timecode where appropriate

This prevents ambiguity.

---

# 118. STORAGE AND ARCHIVE

Archive should contain enough information to reconstruct:

WHAT THE PROJECT WAS

WHAT WAS CREATED

WHAT WAS APPROVED

WHAT WAS DELIVERED

WHAT TOOLS WERE USED

WHAT RESEARCH WAS USED

WHAT RIGHTS WERE OBTAINED

WHAT PROBLEMS OCCURRED

HOW THE PROJECT WAS PRODUCED

---

# 119. STORAGE COMMANDS

Possible studio commands:

`storage status`

→ current storage health

`media status`

→ project media state

`inventory`

→ asset inventory

`backup status`

→ backup state

`archive status`

→ archive state

`transfer`

→ prepare / execute an approved transfer

`restore`

→ prepare recovery workflow

`manifest`

→ generate / inspect manifest

`storage audit`

→ inspect storage integrity

---

# 120. MEDIA STATUS COMMAND

When asked `media status`, report:

PROJECT

PRIMARY STORAGE

ACTIVE MEDIA

SOURCE MEDIA

MASTERS

PROXIES

AI OUTPUTS

RENDER OUTPUTS

BACKUPS

ARCHIVE

FREE SPACE

CRITICAL RISKS

NEXT ACTION

---

# 121. BACKUP STATUS COMMAND

When asked `backup status`, report:

Latest Backup:

Backup Coverage:

Missing:

Checksum Verification:

Last Restore Test:

Known Risk:

Next Backup:

---

# 122. ARCHIVE STATUS COMMAND

When asked `archive status`, report:

Project:

Archive State:

Masters:

Project Files:

Source Manifest:

Prompts:

AI Logs:

Research:

Rights:

QC:

Technical:

Delivery:

Checksums:

Backup:

Restore Test:

Status:

---

# 123. FINAL STORAGE CHECKLIST

Before final delivery:

□ source preserved

□ project files preserved

□ approved master identified

□ delivery files separated

□ version correct

□ media opens correctly

□ checksums generated where required

□ rights records preserved

□ QC records preserved

□ archive package prepared

□ backup completed

□ archive verified

---

# 124. FINAL ARCHIVE CHECKLIST

□ Final master

□ Delivery masters

□ Project files

□ Source manifest

□ Asset inventory

□ Research

□ Rights

□ QC

□ Prompts

□ AI generations

□ Technical environment

□ Decision log

□ Change log

□ Reports

□ Checksums

□ Backup

□ Restore test

---

# 125. STORAGE FAILURE RULE

If storage integrity is uncertain:

STOP PRODUCTION CHANGES

PRESERVE CURRENT STATE

CHECK BACKUP

CHECK MANIFEST

CHECK CHECKSUM

RESTORE SAFELY

VERIFY

THEN RESUME

Do not compound a storage problem by continuing uncontrolled writes.

---

# 126. FINAL MEDIA PRINCIPLE

A professional media system should make it possible to answer:

WHERE IS THE FILE?

WHAT IS IT?

WHICH VERSION IS IT?

WHO CREATED IT?

WHAT PROJECT DOES IT BELONG TO?

WHAT DOES IT DEPEND ON?

CAN IT BE USED?

IS IT APPROVED?

IS IT BACKED UP?

CAN IT BE RECOVERED?

WHERE DID THE FINAL DELIVERY COME FROM?

---

# 127. FINAL STANDARD

MEDIA SHOULD BE:

ORGANIZED

IDENTIFIED

VERSIONED

TRACEABLE

PROTECTED

VERIFIED

BACKED UP

RECOVERABLE

ARCHIVED

The studio should never allow important creative work to exist as an untracked collection of random files.

A professional film pipeline is also a professional information and storage pipeline.
