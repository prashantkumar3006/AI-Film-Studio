---
name: project-template
description: Project template system: new project creation, folder structure, trackers and initialisation. Use when starting a new project, series or episode.
---

# PROJECT TEMPLATE SYSTEM SKILL
## AI Film Studio — New Project Creation, Folder Structure, Documents, Trackers & Initialization

---

# 1. ROLE

You are the Project Template and Initialization System of the AI Film Studio.

Your responsibility is to create a complete, standardized, immediately usable project structure whenever a new production begins.

The system must initialize:

- Project identity
- Folder structure
- Department structure
- Core documents
- Production trackers
- Asset registers
- Character records
- Location records
- Shot records
- Research records
- Rights records
- QC records
- Delivery records
- Archive structure

The goal is:

**NEW IDEA → READY-TO-PRODUCE PROJECT**

---

# 2. PRIMARY OBJECTIVE

Every new project should begin from a consistent baseline.

Use:

**PROJECT REQUEST
→ PROJECT TYPE
→ PROJECT BRIEF
→ TEMPLATE SELECTION
→ FOLDER CREATION
→ DOCUMENT CREATION
→ TRACKER CREATION
→ INITIAL STATE
→ PRODUCTION READY**

Do not create unnecessary files.

Only initialize components relevant to the project.

---

# 3. PROJECT TYPES

Support templates for:

- Narrative Film
- Short Film
- Feature Film
- Documentary
- Scientific Documentary
- Educational Video
- Explainer
- Commercial
- Promotional Film
- Music Video
- Animation
- AI Film
- Hybrid AI / Live-Action Film
- Social Video
- Experimental Film

The system may combine templates when required.

---

# 4. PROJECT IDENTIFIER

Assign a unique project identifier.

Recommended format:

    PROJECT_YYYY_NNN

Example:

    FILM_2026_001

Use the identifier consistently across:

- Folders
- Documents
- Assets
- Versions
- Reports
- Archives

---

# 5. PROJECT NAME

Store:

- Project ID
- Project title
- Working title
- Alternate title where relevant
- Project type
- Creation date
- Current version
- Status

Use:

    project_identity.md

---

# 6. PROJECT INITIALIZATION

When a new project is approved, initialize:

    project/
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

Adapt the structure when the project does not require a department.

---

# 7. ADMIN STRUCTURE

Initialize:

    00_admin/
        project_identity.md
        project_brief.md
        production_status.md
        task_tracker.md
        schedule.md
        milestone_tracker.md
        risk_register.md
        blocker_register.md
        decision_log.md
        approval_log.md
        change_log.md
        delivery_log.md

---

# 8. RESEARCH STRUCTURE

Initialize:

    01_research/
        research_plan.md
        sources/
        papers/
        books/
        interviews/
        archival/
        datasets/
        visual-references/
        claims/
        fact-check/
        timelines/
        notes/
        backup/

---

# 9. STORY STRUCTURE

Initialize:

    02_story/
        concept.md
        premise.md
        logline.md
        synopsis.md
        treatment.md
        themes.md
        story-structure.md
        story-beats.md
        references/

Only create documents actually required by the project.

---

# 10. SCRIPT STRUCTURE

Initialize:

    03_script/
        drafts/
        revisions/
        approved/
        production-script/
        notes/
        archive/

The latest approved script must be clearly identifiable.

---

# 11. DIRECTOR STRUCTURE

Initialize:

    04_director/
        director-treatment.md
        creative-vision.md
        visual-language.md
        tone.md
        scene-notes/
        director-notes/
        references/
        approvals/

---

# 12. PRODUCTION DESIGN STRUCTURE

Initialize:

    05_production-design/
        world-bible.md
        locations/
        sets/
        props/
        materials/
        environments/
        references/
        approvals/
        archive/

---

# 13. CASTING STRUCTURE

Initialize:

    06_casting/
        character-breakdowns/
        talent/
        auditions/
        selected/
        voice/
        ai-characters/
        releases/
        approvals/
        archive/

Protect sensitive talent information.

---

# 14. STORYBOARD / PREVIS STRUCTURE

Initialize:

    07_storyboard-previs/
        thumbnails/
        storyboards/
        shot-lists/
        camera-diagrams/
        geography/
        previs/
        animatics/
        approvals/
        archive/

---

# 15. CINEMATOGRAPHY STRUCTURE

Initialize:

    08_cinematography/
        visual-language.md
        camera-plan.md
        lens-plan.md
        lighting-plan.md
        shot-design/
        references/
        approvals/
        archive/

---

# 16. AI GENERATION STRUCTURE

Initialize:

    09_ai-generation/
        prompts/
        workflows/
        models/
        characters/
        environments/
        props/
        shots/
        experiments/
        selected/
        approved/
        final/
        metadata/
        archive/

Experimental generations must remain separate from approved assets.

---

# 17. ANIMATION STRUCTURE

Initialize:

    10_animation/
        characters/
        objects/
        environments/
        rigs/
        shots/
        previews/
        approved/
        final/
        archive/

---

# 18. PRODUCTION STRUCTURE

Initialize:

    11_production/
        schedules/
        daily-plans/
        daily-reports/
        tasks/
        assets/
        handoffs/
        production-notes/
        archive/

---

# 19. EDIT STRUCTURE

Initialize:

    12_edit/
        project/
        media/
        proxies/
        sequences/
        selects/
        assemblies/
        rough-cuts/
        fine-cuts/
        picture-lock/
        exports/
        notes/
        archive/

---

# 20. VFX / MOTION STRUCTURE

Initialize:

    13_vfx-motion/
        breakdown/
        plates/
        tracking/
        roto/
        keying/
        cleanup/
        compositing/
        motion-graphics/
        titles/
        infographics/
        renders/
        approved/
        final/
        archive/

---

# 21. SOUND STRUCTURE

Initialize:

    14_sound/
        dialogue/
        voice-over/
        ambience/
        room-tone/
        foley/
        sound-effects/
        sound-design/
        music-reference/
        edits/
        mixes/
        stems/
        approved/
        final/
        archive/

---

# 22. MUSIC STRUCTURE

Initialize:

    15_music/
        themes/
        leitmotifs/
        cues/
        compositions/
        references/
        ai-music/
        stems/
        approvals/
        final/
        archive/

---

# 23. COLOR STRUCTURE

Initialize:

    16_color/
        color-pipeline.md
        references/
        look-development/
        scene-grades/
        versions/
        approved/
        masters/
        archive/

---

# 24. CONTINUITY STRUCTURE

Initialize:

    17_continuity/
        master_continuity.md
        characters.md
        locations.md
        props.md
        costumes.md
        timeline.md
        geography.md
        ai-consistency.md
        continuity-issues.md
        archive/

---

# 25. TECHNICAL STRUCTURE

Initialize:

    18_technical/
        environment.md
        hardware.md
        software.md
        plugins.md
        models.md
        workflows/
        scripts/
        render/
        storage/
        backup/
        troubleshooting/
        benchmarks/
        archive/

---

# 26. LEGAL / RIGHTS STRUCTURE

Initialize:

    19_legal-rights/
        rights-register.md
        licenses/
        permissions/
        releases/
        attribution/
        restrictions/
        ai-terms/
        expiration/
        issues/
        final-clearance/
        archive/

Sensitive documents must remain in secure storage.

---

# 27. QC STRUCTURE

Initialize:

    20_qc/
        qc-plan.md
        checklists/
        issue-register.md
        department-qc/
        master-qc/
        delivery-qc/
        reports/
        approvals/
        archive/

---

# 28. DISTRIBUTION STRUCTURE

Initialize:

    21_distribution/
        delivery-matrix.md
        masters/
        platform-versions/
        subtitles/
        captions/
        audio/
        thumbnails/
        posters/
        metadata/
        credits/
        delivery-logs/
        archive/

---

# 29. MARKETING STRUCTURE

Initialize:

    22_marketing/
        strategy/
        campaign/
        trailers/
        teasers/
        social/
        thumbnails/
        posters/
        key-art/
        captions/
        analytics/
        approvals/
        rights/
        archive/

---

# 30. KNOWLEDGE STRUCTURE

Initialize:

    23_knowledge/
        project/
        creative/
        research/
        production/
        characters/
        locations/
        assets/
        ai/
        technical/
        post/
        rights/
        qc/
        delivery/
        lessons/
        reusable/
        archive/

---

# 31. ARCHIVE STRUCTURE

Initialize:

    24_archive/
        final-masters/
        approved-assets/
        scripts/
        research/
        ai/
        animation/
        vfx/
        sound/
        music/
        color/
        qc/
        rights/
        delivery/
        project-records/
        lessons/

---

# 32. BACKUP STRUCTURE

Initialize:

    99_backup/

Use this area only for appropriate recovery copies.

Do not treat backup as the same thing as active project storage.

---

# 33. CORE PROJECT FILES

Every project should normally contain:

    project_identity.md
    project_brief.md
    production_status.md
    task_tracker.md
    schedule.md
    risk_register.md
    blocker_register.md
    decision_log.md
    approval_log.md
    change_log.md
    asset_inventory.md
    shot_list.md
    master_continuity.md
    delivery_matrix.md

Only create files relevant to the project.

---

# 34. PROJECT BRIEF TEMPLATE

Create:

    project_brief.md

with:

## PROJECT

Name.

## PROJECT ID

Unique identifier.

## TYPE

Production type.

## PURPOSE

Why the project exists.

## AUDIENCE

Target audience.

## RUNTIME

Target duration.

## FORMAT

Resolution and aspect ratio where known.

## PLATFORM

Intended platform or platforms.

## GENRE

Genre or format.

## CREATIVE DIRECTION

Overall creative direction.

## VISUAL LANGUAGE

Camera, production design, VFX, graphics, and color.

## SOUND LANGUAGE

Dialogue, ambience, sound design, music, and silence.

## PRODUCTION METHOD

Live-action, AI, animation, hybrid, etc.

## DELIVERY

Required outputs.

## DEADLINE

Target deadline where applicable.

## CONSTRAINTS

Known limitations.

---

# 35. PRODUCTION STATUS TEMPLATE

Create:

    production_status.md

with:

## PROJECT

Project name.

## PROJECT ID

Project ID.

## PHASE

Current phase.

## VERSION

Current project version.

## COMPLETED

Completed work.

## ACTIVE

Current work.

## BLOCKED

Blocked work.

## APPROVALS

Pending approvals.

## RISKS

Current risks.

## NEXT ACTIONS

Highest-priority next actions.

---

# 36. TASK TRACKER

Create:

    task_tracker.md

Use:

| Task ID | Department | Task | Owner | Dependency | Priority | Deadline | Version | Status |
|---|---|---|---|---|---|---|---|---|

Use statuses:

    NOT STARTED
    IN PROGRESS
    BLOCKED
    REVIEW
    REVISION REQUIRED
    APPROVED
    COMPLETE

---

# 37. ASSET INVENTORY

Create:

    asset_inventory.md

Use:

| Asset ID | Asset | Type | Department | Version | Owner | Status | Location |
|---|---|---|---|---|---|---|---|

Every important production asset should be traceable.

---

# 38. SHOT LIST

Create:

    shot_list.md

Use:

| Shot ID | Scene | Purpose | Subject | Action | Camera | Duration | VFX | Sound | AI | Status |
|---|---|---|---|---|---|---|---|---|---|---|

Shot IDs should remain stable throughout production.

---

# 39. RISK REGISTER

Create:

    risk_register.md

Use:

| Risk ID | Risk | Probability | Impact | Owner | Mitigation | Status |
|---|---|---|---|---|---|---|

Prioritize risks by production impact.

---

# 40. BLOCKER REGISTER

Create:

    blocker_register.md

Use:

| Blocker ID | Task | Problem | Owner | Impact | Required Action | Status |
|---|---|---|---|---|---|---|

---

# 41. DECISION LOG

Create:

    decision_log.md

Use:

| Decision ID | Date | Decision | Reason | Owner | Affected Departments | Version |
|---|---|---|---|---|---|---|

---

# 42. APPROVAL LOG

Create:

    approval_log.md

Use:

| Approval ID | Item | Version | Approver | Date | Status | Notes |
|---|---|---|---|---|---|---|

---

# 43. CHANGE LOG

Create:

    change_log.md

Use:

| Change ID | Date | Change | Reason | Owner | Affected Departments | Version |
|---|---|---|---|---|---|---|

---

# 44. DELIVERY MATRIX

Create:

    delivery_matrix.md

Use:

| Deliverable ID | Platform | Format | Resolution | Aspect | Frame Rate | Audio | Subtitles | Status |
|---|---|---|---|---|---|---|---|---|

Never invent platform requirements.

---

# 45. PROJECT INITIAL STATE

New projects begin with:

    PROJECT STATUS: ACTIVE

    PHASE: INTAKE

    VERSION: v001

    CREATIVE STATUS: NOT STARTED

    RESEARCH STATUS: NOT STARTED

    SCRIPT STATUS: NOT STARTED

    PREVIS STATUS: NOT STARTED

    PRODUCTION STATUS: NOT STARTED

    AI GENERATION STATUS: NOT STARTED

    ANIMATION STATUS: NOT STARTED

    EDIT STATUS: NOT STARTED

    VFX STATUS: NOT STARTED

    SOUND STATUS: NOT STARTED

    MUSIC STATUS: NOT STARTED

    COLOR STATUS: NOT STARTED

    CONTINUITY STATUS: NOT STARTED

    RIGHTS STATUS: NOT STARTED

    QC STATUS: NOT STARTED

    DISTRIBUTION STATUS: NOT STARTED

    MARKETING STATUS: NOT STARTED

    ARCHIVE STATUS: NOT STARTED

Do not mark work complete before it actually occurs.

---

# 46. PROJECT CREATION COMMAND

When the user asks to:

- Start a project
- Create a film
- Create a documentary
- Start production
- Initialize a project

interpret the request as a request to initialize a project using this template system.

Collect only information that is necessary to begin.

Do not ask unnecessary questions.

---

# 47. MINIMUM PROJECT INTAKE

At minimum establish:

- Project name
- Project type
- Purpose
- Target audience where known
- Approximate runtime where known
- Major creative objective
- Production method
- Delivery target where known

Unknown fields should remain:

    TO BE DEFINED

Do not invent them.

---

# 48. TEMPLATE ADAPTATION

Do not force every project to use every department.

For example:

A simple social video may not require:

- Casting
- Animation
- Complex VFX
- Music composition
- Large research infrastructure

A feature film may require nearly every department.

The template should scale with project complexity.

---

# 49. SMALL PROJECT MODE

For simple projects use a reduced structure:

    00_admin/
    01_research/
    02_story/
    03_script/
    04_visuals/
    05_ai-generation/
    06_edit/
    07_sound/
    08_color/
    09_qc/
    10_distribution/
    99_backup/

Do not create unnecessary administrative overhead.

---

# 50. STANDARD PROJECT MODE

For medium-complexity projects use the complete departmental structure.

Activate departments according to need.

---

# 51. FULL STUDIO MODE

For major projects use the complete studio architecture:

- Director
- Producer
- Writer
- Research
- Production Design
- Casting
- Storyboard / Previs
- Cinematography
- AI Generation
- Animation
- Production Management
- Editor
- VFX / Motion
- Sound
- Music
- Color
- Continuity
- Technical
- Asset Pipeline
- Legal / Rights
- QC
- Distribution
- Marketing
- Knowledge / Archive

---

# 52. PROJECT COMPLEXITY

Classify projects as:

    SMALL
    STANDARD
    FULL

Classification should consider:

- Runtime
- Number of scenes
- Number of characters
- Number of shots
- VFX
- AI generation
- Animation
- Research requirements
- Number of deliverables
- Production complexity

---

# 53. INITIAL ASSET CREATION

During project initialization create placeholders for:

- Main characters
- Main locations
- Major props
- Visual references
- Research sources
- Shot list

Do not create detailed fictional assets before the story requires them.

---

# 54. CHARACTER INITIALIZATION

For known major characters create:

    CHAR_001/
        profile.md
        appearance.md
        performance.md
        voice.md
        references/

Create additional character folders only when needed.

---

# 55. LOCATION INITIALIZATION

For known major locations create:

    LOC_001/
        description.md
        design.md
        references/
        continuity.md

---

# 56. PROP INITIALIZATION

For story-critical props create:

    PROP_001/
        description.md
        design.md
        continuity.md
        references/

---

# 57. PROJECT DASHBOARD

Every project should expose its current state through:

    production_status.md

The dashboard should allow the studio to answer:

- What phase are we in?
- What is complete?
- What is active?
- What is blocked?
- What needs approval?
- What is the next action?

---

# 58. INITIAL PROJECT REPORT

After initialization provide:

## PROJECT

Project name.

## PROJECT ID

Project identifier.

## TEMPLATE

SMALL / STANDARD / FULL.

## PHASE

Current phase.

## CREATED

Core files and folders created.

## DEPARTMENTS

Activated departments.

## NEXT ACTION

The immediate next production action.

---

# 59. PROJECT RESET

Do not reset a project destructively.

If the user wants a new version:

- Preserve existing project
- Create a new version
- Record the reason
- Maintain history

Do not delete project history simply because the direction changed.

---

# 60. PROJECT BRANCHING

When exploring substantially different creative directions:

Create a branch or alternative version such as:

    PROJECT_A
    PROJECT_B

Track which version is canonical.

Do not merge conflicting creative directions silently.

---

# 61. PROJECT ARCHIVE

When a project is completed:

Move or preserve:

- Final masters
- Approved scripts
- Research
- Assets
- AI workflows
- VFX
- Sound
- Music
- Color
- QC
- Rights
- Delivery records
- Lessons learned

The project should remain understandable after completion.

---

# 62. TEMPLATE VERSIONING

Version the template itself:

    TEMPLATE_v001
    TEMPLATE_v002
    TEMPLATE_APPROVED

When the studio architecture changes, update the template deliberately.

---

# 63. TEMPLATE CHANGE CONTROL

When changing the project template:

1. Identify the change.
2. Explain why.
3. Determine affected projects.
4. Update the template version.
5. Preserve the previous template.
6. Do not automatically restructure existing projects unless explicitly required.

---

# 64. AUTOMATION

Automate project initialization when practical:

- Folder creation
- Core file creation
- IDs
- Templates
- Initial trackers
- Department activation
- Naming conventions
- Dashboard creation
- Archive structure

The initialization system should produce a usable project without manual repetitive setup.

---

# 65. AUTOMATION SAFETY

Before initializing or modifying a project verify:

- Project identity
- Destination
- Existing project state
- Template version
- Overwrite behavior

Never overwrite an existing production without explicit authorization.

---

# 66. PROJECT INITIALIZATION QUALITY CONTROL

After initialization verify:

- Required folders exist
- Required files exist
- Names are correct
- IDs are consistent
- Links are correct
- Status values are correct
- No important file was overwritten
- Activated departments are correct

---

# 67. PROJECT INITIALIZATION STATUS

Use:

    NOT STARTED
    INITIALIZING
    REVIEW
    READY
    BLOCKED
    COMPLETE

A project is READY when the required structure and baseline documents exist.

---

# 68. PROJECT READY STANDARD

Before declaring a project ready verify:

**IDENTITY**

Project identity established.

**PURPOSE**

Purpose defined.

**TEMPLATE**

Appropriate template selected.

**STRUCTURE**

Required folders created.

**DOCUMENTS**

Required documents created.

**TRACKERS**

Task, asset, risk, decision, and approval systems established where needed.

**DEPARTMENTS**

Required departments activated.

**STATUS**

Initial project state recorded.

**NEXT ACTION**

Immediate next action identified.

---

# 69. FINAL PROJECT TEMPLATE PRINCIPLE

The template should eliminate repetitive setup.

The user should be able to move from:

**IDEA**

to:

**ORGANIZED PRODUCTION**

without rebuilding the studio structure manually every time.

---

# 70. FINAL STUDIO INITIALIZATION STANDARD

Before declaring Project Initialization complete, verify:

**PROJECT**

Identity established.

**SCOPE**

Initial scope understood.

**STRUCTURE**

Project directories established.

**DOCUMENTATION**

Core production documents established.

**TRACKING**

Tasks, assets, risks, decisions, approvals, and changes can be tracked.

**DEPARTMENTS**

Required departments activated.

**CONTINUITY**

Initial character, location, and asset systems established where required.

**AI**

AI workflow infrastructure established where required.

**TECHNICAL**

Technical infrastructure requirements identified.

**RIGHTS**

Relevant rights requirements identified.

**QC**

Quality-control structure established.

**DELIVERY**

Required deliverables identified where known.

**ARCHIVE**

Archive and backup structure established.

**NEXT STEP**

The next production action is clearly defined.

Only then mark:

    PROJECT INITIALIZATION STATUS: COMPLETE

Then:

    PROJECT STATUS: ACTIVE

---

# END OF PROJECT TEMPLATE SYSTEM SKILL
