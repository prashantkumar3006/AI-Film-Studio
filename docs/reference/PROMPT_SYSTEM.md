# STUDIO PROMPT SYSTEM

## 1. PURPOSE

The Studio Prompt System is the central framework for designing, storing, testing, versioning, and reusing prompts across the AI Film Studio.

It governs prompts for:

- image generation
- video generation
- character generation
- environment generation
- object / prop generation
- animation
- motion graphics
- VFX
- sound
- music
- voice
- research
- writing
- editing
- automation
- analysis
- QC

The purpose is not simply to write longer prompts.

The purpose is to produce:

- predictable outputs
- repeatable workflows
- controllable variation
- continuity
- efficient iteration
- reusable knowledge
- traceable production decisions

---

# 2. CORE PROMPT PRINCIPLE

A prompt is a production instruction.

It should define:

INTENT
→ what must be achieved

SUBJECT
→ what is being created

CONTEXT
→ where and when it exists

APPEARANCE / BEHAVIOR
→ what it should look or behave like

CAMERA / PRESENTATION
→ how it should be observed

STYLE
→ artistic language

CONSTRAINTS
→ what must not change

CONTINUITY
→ what must match previous work

OUTPUT
→ what is required

QUALITY
→ what makes the result acceptable

---

# 3. PROMPT = SPECIFICATION

For important work, treat the prompt as a specification rather than casual prose.

A strong prompt should answer:

WHAT?

WHY?

WHO?

WHERE?

WHEN?

HOW?

UNDER WHAT CONSTRAINTS?

WHAT MUST REMAIN CONSISTENT?

WHAT SHOULD BE AVOIDED?

WHAT OUTPUT IS REQUIRED?

---

# 4. PROMPT LAYERS

The studio uses layered prompts.

## Layer 1 — Production Intent

Why is this generation being performed?

Example:

Create a tense establishing shot that introduces an abandoned research facility.

## Layer 2 — Subject

What is actually being shown?

Example:

A large abandoned scientific research facility surrounded by dense vegetation.

## Layer 3 — Environment

Where does it exist?

Example:

Remote tropical valley, humid atmosphere, overgrown concrete structures, remnants of industrial infrastructure.

## Layer 4 — Time

When?

Example:

Late afternoon, shortly before sunset.

## Layer 5 — Visual Design

How should it appear?

Example:

Weathered concrete, rusted metal, broken glass, moss, wet surfaces.

## Layer 6 — Cinematography

How is it photographed?

Example:

Wide establishing composition, controlled perspective, slow forward movement, deep environmental context.

## Layer 7 — Lighting

What is the light doing?

Example:

Low directional sunlight filtered through clouds and vegetation.

## Layer 8 — Emotion

What should the audience feel?

Example:

Mystery, isolation, unresolved history.

## Layer 9 — Continuity

What must match?

Example:

Architecture must match LOC_004 reference images.

## Layer 10 — Output

What must be delivered?

Example:

16:9 cinematic video suitable for editorial use.

---

# 5. MASTER PROMPT STRUCTURE

Use this general structure:

PROJECT CONTEXT

CREATIVE INTENT

SHOT / TASK PURPOSE

SUBJECT

CHARACTER / OBJECT DETAILS

ENVIRONMENT

TIME / WEATHER

ACTION / BEHAVIOR

CAMERA

LENS / PERSPECTIVE

COMPOSITION

MOVEMENT

LIGHTING

COLOR

MATERIALS / TEXTURES

STYLE

MOOD

AUDIO / PERFORMANCE where relevant

CONTINUITY CONSTRAINTS

REFERENCES

NEGATIVE CONSTRAINTS

TECHNICAL OUTPUT

QUALITY CONTROL

---

# 6. SHOT PROMPT SYSTEM

Visual generation should generally be shot-centric.

Shot Prompt ID:
Project:
Sequence:
Scene:
Shot:
Purpose:
Characters:
Location:
Action:
Emotion:
Camera:
Lens:
Composition:
Movement:
Lighting:
Color:
Atmosphere:
Continuity:
Reference Assets:
Prompt:
Negative Constraints:
Model:
Model Version:
Output:
QC Criteria:

---

# 7. CHARACTER PROMPT SYSTEM

Character prompts should separate identity from temporary scene conditions.

## Permanent Identity

Character ID:
Face:
Body:
Age:
Hair:
Skin:
Distinctive Features:
Wardrobe Baseline:
Accessories:
Voice:
Personality:
Physical Behavior:

## Scene State

Scene:
Location:
Time:
Wardrobe:
Emotion:
Action:
Pose:
Expression:
Lighting:
Camera:
Continuity:

Permanent identity should not be rewritten arbitrarily from shot to shot.

---

# 8. CHARACTER REFERENCE PROMPT

For reference creation define:

Character identity

Facial structure

Body proportions

Hair

Skin characteristics

Age

Distinctive features

Wardrobe

Accessories

Neutral expression

Neutral lighting

Reference framing

Full body / half body / portrait

Clean background where useful

This reference becomes an anchor for later generations.

---

# 9. CHARACTER CONTINUITY PROMPT

When generating a new shot:

Match CHAR_XXX reference.

Preserve:

- face structure
- facial proportions
- hair
- body proportions
- age
- wardrobe unless intentionally changed
- accessories
- distinctive marks
- skin characteristics

Change only:

- expression
- pose
- action
- lighting
- camera
- environment
- scene-specific state

unless the project explicitly requires a permanent change.

---

# 10. LOCATION PROMPT SYSTEM

Location prompts should define:

Location ID:
Architecture:
Geography:
Era:
Materials:
Scale:
Color:
Weather:
Vegetation:
Objects:
Signs:
Lighting:
Atmosphere:
Population:
Sound Context:
Time:
Continuity References:

A location should be treated as a persistent world asset.

---

# 11. ENVIRONMENT CONTINUITY

When returning to a previously established location:

MATCH

- architecture
- major structures
- geography
- distinctive objects
- material palette
- environmental conditions
- visual identity

Allow deliberate changes in:

- time
- weather
- lighting
- activity
- camera position

when motivated by the story.

---

# 12. PROP PROMPT SYSTEM

Props should define:

Prop ID:
Function:
Shape:
Material:
Color:
Age:
Condition:
Wear:
Scale:
Historical Context:
Owner / Character:
Scene:
Continuity Requirement:
Reference:

Important props should maintain consistent:

- shape
- scale
- color
- material
- damage
- markings
- position
- ownership

---

# 13. CINEMATOGRAPHY PROMPT SYSTEM

For visual generation specify:

SHOT SIZE

CAMERA HEIGHT

CAMERA POSITION

LENS / FOCAL LENGTH

PERSPECTIVE

DEPTH OF FIELD

FOCUS

COMPOSITION

MOVEMENT

FRAMING

SCREEN DIRECTION

LIGHTING

EXPOSURE CHARACTER

COLOR

ATMOSPHERE

The prompt should communicate the intended camera language rather than merely saying:

"cinematic."

---

# 14. AVOIDING GENERIC "CINEMATIC"

The word `cinematic` is insufficient by itself.

Instead define:

- lens behavior
- composition
- lighting
- contrast
- texture
- depth
- camera movement
- atmosphere
- production design
- color
- emotional intention

The studio should prefer specific visual language over vague aesthetic labels.

---

# 15. CAMERA MOVEMENT PROMPTS

Use movement only when motivated.

Possible movements:

- static
- slow push-in
- dolly
- tracking
- crane
- orbit
- pan
- tilt
- handheld
- stabilized handheld
- lateral movement
- aerial movement
- follow shot

Specify:

START POSITION

END POSITION

MOVEMENT SPEED

MOVEMENT DIRECTION

SUBJECT RELATIONSHIP

EMOTIONAL PURPOSE

---

# 16. LIGHTING PROMPTS

Specify:

SOURCE

DIRECTION

QUALITY

COLOR TEMPERATURE

INTENSITY

CONTRAST

SHADOW CHARACTER

REFLECTION

ATMOSPHERE

MOTIVATION

Examples of useful lighting descriptions:

soft overcast daylight

hard directional noon sunlight

warm practical interior lighting

cool moonlight entering through a window

flickering industrial sodium lighting

Do not use technical lighting terms without understanding their visual effect.

---

# 17. COLOR PROMPTS

Color prompts may define:

Primary palette:
Secondary palette:
Accent:
Contrast:
Saturation:
Temperature:
Skin-tone behavior:
Environmental palette:
Mood:

Color must support continuity.

Do not randomly change palette between related shots.

---

# 18. MATERIAL AND TEXTURE PROMPTS

Materials may include:

- concrete
- steel
- wood
- glass
- fabric
- stone
- soil
- water
- plastic
- vegetation
- skin
- painted surfaces

Specify condition where relevant:

- new
- worn
- scratched
- oxidized
- wet
- dusty
- cracked
- polished
- weathered
- burned

Material specificity improves world coherence.

---

# 19. MOTION PROMPT SYSTEM

For video generation specify:

START STATE

ACTION

MOVEMENT

TIMING

END STATE

CAMERA MOVEMENT

ENVIRONMENT MOVEMENT

LIGHTING CHANGE

SECONDARY MOTION

PHYSICS

EMOTIONAL BEAT

Avoid describing a single frame when the output is a moving shot.

---

# 20. TEMPORAL CONSISTENCY

Video prompts should control:

- identity
- object permanence
- spatial relationships
- movement direction
- scale
- camera path
- lighting
- environment
- action sequence

Important shots should be checked for:

- identity drift
- object disappearance
- shape deformation
- texture flicker
- inconsistent shadows
- impossible motion
- sudden changes

---

# 21. ACTION SPECIFICATION

Describe action as an ordered sequence.

START

→ ACTION 1

→ ACTION 2

→ REACTION

→ END STATE

Example:

Character stands motionless.

Looks toward the doorway.

Hears an unseen sound.

Slowly turns.

Camera begins a subtle push-in.

Character stops before fully turning toward camera.

This is generally more controllable than simply saying:

"Character reacts dramatically."

---

# 22. PERFORMANCE PROMPTING

Performance prompts should specify:

Objective:
Emotion:
Subtext:
Expression:
Eye Direction:
Posture:
Gesture:
Movement:
Voice:
Tempo:
Reaction:

Avoid generic instructions like:

"act naturally"

when more useful behavioral information can be supplied.

---

# 23. DIALOGUE / LIP SYNC PROMPTS

For talking subjects specify:

Speaker:
Exact dialogue:
Emotion:
Delivery:
Pace:
Eye Direction:
Mouth Visibility:
Camera:
Framing:
Lip Sync Requirement:
Accent:
Voice Reference:
Continuity:

Avoid unnecessary camera movement when lip-sync accuracy is critical.

---

# 24. VOICE GENERATION PROMPTS

Voice prompt elements:

Character:
Age:
Tone:
Accent:
Language:
Pitch:
Texture:
Energy:
Pacing:
Emotion:
Clarity:
Breath:
Performance Style:
Dialogue:
Context:

Do not generate a voice merely from an adjective such as "deep" or "powerful."

Define the actual behavioral qualities.

---

# 25. MUSIC PROMPT SYSTEM

Music prompts may include:

Purpose:
Scene:
Emotion:
Genre:
Instrumentation:
Tempo:
Rhythm:
Harmony:
Texture:
Dynamics:
Structure:
Cultural Context:
Reference:
Duration:
Ending:
Stems Required:

Avoid excessive imitation of a specific living artist's signature style.

Describe musical characteristics and desired function instead.

---

# 26. SOUND DESIGN PROMPT SYSTEM

Define:

Scene:
Location:
Perspective:
Environment:
Ambience:
Foreground Sounds:
Background Sounds:
Movement:
Material:
Intensity:
Dynamic Range:
Silence:
Transitions:
Emotional Purpose:

Sound perspective should support spatial realism.

---

# 27. MOTION GRAPHICS PROMPT SYSTEM

Define:

Graphic ID:
Purpose:
Information:
Hierarchy:
Typography:
Layout:
Animation:
Timing:
Transition:
Color:
Branding:
Data Source:
Output:
Accessibility:

Information should remain readable before decorative complexity is added.

---

# 28. INFOGRAPHIC PROMPTS

Define:

Question:
Data:
Source:
Chart Type:
Units:
Labels:
Comparison:
Highlight:
Animation:
Narrative Purpose:
Color:
Typography:
Citation:
Output:

Never invent data merely to complete an infographic.

---

# 29. SCIENTIFIC VISUALIZATION PROMPTS

Define:

Subject:
Scientific Concept:
Evidence:
Data:
Model:
Scale:
Perspective:
Representation Type:
Variables:
Colors:
Labels:
Motion:
Uncertainty:
Reference:
Restrictions:

Specify whether the visual is:

OBSERVATIONAL

SIMULATED

PREDICTED

CONCEPTUAL

RECONSTRUCTED

AI_VISUALIZATION

Do not imply unsupported scientific certainty.

---

# 30. HISTORICAL RECONSTRUCTION PROMPTS

Define:

Historical Period:
Location:
Date:
Architecture:
Clothing:
Objects:
Technology:
Environment:
Lighting:
Cultural Details:
Evidence:
Known Uncertainties:
Reconstruction Status:

Historical visual generation should be evidence-aware.

---

# 31. DOCUMENTARY AI VISUAL PROMPT

For documentary work, define:

Visual Purpose:
Factual Subject:
Source Evidence:
Representation Type:
AI Generated:
What Is Known:
What Is Estimated:
What Is Reconstructed:
What Must Not Be Invented:
Visual Style:
Disclosure Requirement:
QC Criteria:

---

# 32. RESEARCH PROMPTS

Research prompts should specify:

Question:
Scope:
Time Range:
Geography:
Source Types:
Evidence Standard:
Required Output:
Primary Sources:
Secondary Sources:
Conflicting Evidence:
Citation Requirement:
Uncertainty Requirement:

The prompt should tell the research system what evidence is needed, not simply ask:

"Research this."

---

# 33. WRITING PROMPTS

Writing prompts may specify:

Project:
Format:
Audience:
Purpose:
Genre:
Tone:
Point of View:
Runtime / Length:
Structure:
Characters:
Themes:
Research Requirements:
Restrictions:
Desired Output:
Revision Target:

---

# 34. EDITING PROMPTS

Editing prompts should define:

Source Material:
Scene:
Story Purpose:
Current Problem:
Desired Effect:
Available Shots:
Coverage:
Pacing:
Dialogue:
Music:
Sound:
B-roll:
Transition:
Target Runtime:
Restrictions:
Expected Result:

---

# 35. QC PROMPTS

QC prompts should explicitly define:

Target:
Version:
QC Category:
Specifications:
Known Risks:
Test Conditions:
Inspection Criteria:
Pass Conditions:
Failure Conditions:
Severity:
Required Report:

A QC prompt should describe what counts as failure.

---

# 36. PROMPT VARIABLES

Reusable prompts should use variables.

Example:

PROJECT = PROJECT_2026_001

SHOT = SHOT_014

CHARACTER = CHAR_002

LOCATION = LOC_003

EMOTION = tension

CAMERA = slow push-in

LIGHTING = overcast dusk

OUTPUT = 16:9 cinematic video

Variable-based prompts are easier to reuse and automate.

---

# 37. VARIABLE PRIORITY

When variables conflict, use this priority:

1. Hard constraints
2. Continuity constraints
3. Safety / rights constraints
4. Story requirements
5. Technical requirements
6. Cinematography
7. Style
8. Optional embellishment

Do not sacrifice identity or continuity merely to increase visual novelty.

---

# 38. HARD CONSTRAINTS

Hard constraints are requirements that must not change.

Examples:

- character identity
- architecture
- object geometry
- historical period
- camera orientation
- brand asset
- scientific structure
- screen direction
- exact text
- required dimensions

Use explicit language.

Example:

PRESERVE EXACTLY:
character face structure, building geometry, wardrobe, and prop placement.

---

# 39. SOFT CONSTRAINTS

Soft constraints allow variation.

Examples:

- cloud density
- background activity
- minor vegetation
- secondary extras
- atmospheric density
- subtle color variation

Use these for controlled exploration.

---

# 40. NEGATIVE CONSTRAINTS

Negative prompts or constraints should focus on actual failure modes.

Examples:

avoid identity drift

avoid extra limbs

avoid deformed hands

avoid warped architecture

avoid floating objects

avoid incorrect text

avoid unnatural eye direction

avoid temporal flicker

avoid inconsistent shadows

avoid random camera movement

Avoid enormous generic negative lists unless the model benefits from them.

---

# 41. MODEL-SPECIFIC PROMPTS

Prompt behavior varies by model.

The studio should maintain model-specific knowledge.

For every important model record:

MODEL ID

MODEL NAME

VERSION

BEST USE

WEAKNESS

PROMPT STYLE

CONTROL INPUTS

NEGATIVE PROMPT BEHAVIOR

REFERENCE SUPPORT

VIDEO CONTROL

KNOWN ARTIFACTS

RECOMMENDED SETTINGS

Do not assume one prompt structure works equally well across every model.

---

# 42. MODEL TESTING

Before using a model for major production:

TEST

→ GENERATE

→ INSPECT

→ COMPARE

→ RECORD

Capture:

- prompt
- settings
- output
- failure mode
- strengths
- weaknesses
- continuity performance
- speed
- resource usage

---

# 43. PROMPT EXPERIMENT LOG

Each meaningful experiment should record:

Experiment ID:
Project:
Prompt ID:
Model:
Purpose:
Hypothesis:
Input:
Prompt Version:
Settings:
Output:
Result:
Failure:
Lesson:
Next Test:
Date:

The experiment log should become studio knowledge.

---

# 44. PROMPT VERSIONING

Use:

PROMPT_001_v001

PROMPT_001_v002

PROMPT_001_v003

A new version should be created when the prompt meaning materially changes.

Minor formatting changes need not always create a new version unless reproducibility requires it.

---

# 45. PROMPT LIBRARY

Organize reusable prompts by:

01_character
02_environment
03_prop
04_cinematography
05_video
06_animation
07_vfx
08_sound
09_music
10_voice
11_research
12_writing
13_editing
14_graphics
15_scientific
16_documentary
17_historical
18_qc
19_automation
20_experimental

---

# 46. PROMPT TAGGING

Useful tags include:

#character

#environment

#video

#cinematography

#documentary

#scientific

#historical

#animation

#vfx

#sound

#music

#voice

#research

#editing

#qc

#kling

#comfyui

#image

#continuity

#experimental

Tags should improve retrieval rather than become excessive metadata.

---

# 47. PROMPT SEARCHABILITY

Every reusable prompt should have:

Prompt ID:
Name:
Purpose:
Department:
Use Case:
Model:
Tags:
Version:
Status:

This allows Claude to search the prompt library efficiently.

---

# 48. PROMPT APPROVAL

Important production prompts may require approval.

Approval states:

- DRAFT
- TESTING
- REVIEW
- APPROVED
- REJECTED
- RETIRED

An approved prompt may be reused without rebuilding it from memory.

---

# 49. PROMPT LOCKING

Lock prompts when they become part of a critical pipeline.

Examples:

LOCKED:

Character reference prompt

Approved environment prompt

Final title-generation prompt

Production-critical VFX prompt

Locked prompts should not be altered silently.

Create a new version instead.

---

# 50. PROMPT REUSE

Before creating a new prompt, Claude should search for:

- existing approved prompts
- similar prompts
- project-specific prompt templates
- model-specific templates
- continuity prompts
- department prompt patterns

Reuse stable systems where appropriate.

---

# 51. PROMPT COMPOSITION

Complex work may combine prompt modules.

Example:

BASE CHARACTER
+
SCENE CONTEXT
+
CAMERA
+
ACTION
+
LIGHTING
+
CONTINUITY
+
OUTPUT

This allows a stable identity layer to be reused across many shots.

---

# 52. PROMPT MODULARITY

Recommended modules:

CHARACTER_CORE

LOCATION_CORE

PROP_CORE

VISUAL_STYLE

CAMERA

LIGHTING

ACTION

PERFORMANCE

SOUND

CONTINUITY

NEGATIVE_CONSTRAINTS

TECHNICAL_OUTPUT

Modules may be combined into project-specific prompts.

---

# 53. MASTER CHARACTER MODULE

A reusable character module should contain only relatively stable identity information.

Do not overload it with:

- temporary emotions
- scene-specific poses
- changing camera positions
- temporary weather
- temporary lighting

Those belong to scene or shot modules.

---

# 54. MASTER LOCATION MODULE

A reusable location module should contain:

- architecture
- geography
- materials
- scale
- persistent objects
- visual identity

Scene-specific changes belong elsewhere.

---

# 55. SHOT-SPECIFIC MODULE

Shot-specific information includes:

- action
- performance
- camera
- framing
- movement
- exact lighting
- current emotional state
- temporary environmental conditions

---

# 56. CONTINUITY MODULE

The continuity module should explicitly state what previous approved material must be matched.

Example:

MATCH SHOT_013_v004.

PRESERVE:
character face, wardrobe, architecture, screen direction, time of day.

CHANGE:
character expression and camera distance only.

---

# 57. REFERENCE PRIORITY

When multiple references exist:

1. approved project master
2. latest approved version
3. continuity reference
4. department-approved reference
5. exploratory reference
6. generic visual reference

Do not let a generic reference override an approved project reference.

---

# 58. REFERENCE COLLISION

When references conflict:

Identify:

REFERENCE A

REFERENCE B

CONFLICT

AUTHORITATIVE SOURCE

REQUIRED DECISION

Do not merge conflicting references automatically.

---

# 59. PROMPT CHAINING

Complex generation may use sequential prompts.

Example:

Character creation
→ environment integration
→ blocking
→ camera
→ motion
→ cleanup
→ upscale
→ compositing

Track each stage.

Do not assume the last prompt contains the full production history.

---

# 60. PROMPT-TO-ASSET TRACEABILITY

Every important generated asset should be traceable to:

Asset ID

Prompt ID

Model ID

Generation ID

Reference Assets

Version

QC

Approval

This creates provenance.

---

# 61. PROMPT-TO-SHOT TRACEABILITY

Every major AI-generated shot should trace:

SHOT_ID

→ PROMPT_ID

→ MODEL_ID

→ GENERATION_ID

→ ASSET_ID

→ EDIT_VERSION

This enables reconstruction of how the shot was produced.

---

# 62. FAILURE CATEGORIES

Record common failures using categories:

IDENTITY_DRIFT

ANATOMY

GEOMETRY

TEXT

TEMPORAL

LIGHTING

MATERIAL

PHYSICS

CAMERA

COMPOSITION

PERFORMANCE

LIP_SYNC

AUDIO

COLOR

CONTINUITY

STYLE

COMPLIANCE

TECHNICAL

REPRODUCIBILITY

---

# 63. FAILURE ANALYSIS

When a prompt fails:

DO NOT simply regenerate indefinitely.

Determine:

What failed?

Was the instruction ambiguous?

Was the model incapable?

Was the reference weak?

Was the prompt too complex?

Did constraints conflict?

Was the model setting inappropriate?

Was the shot itself poorly designed?

Should the task be decomposed?

---

# 64. PROMPT OPTIMIZATION

Optimize for:

CONTROL

CLARITY

REPEATABILITY

RELEVANCE

MODEL COMPATIBILITY

Do not optimize merely for prompt length.

A shorter precise prompt may outperform a long ambiguous prompt.

---

# 65. PROMPT COMPLEXITY

When output quality decreases as prompts become longer:

Test:

SHORT VERSION

vs

DETAILED VERSION

vs

MODULAR VERSION

Record the result.

Prompt complexity should be justified by improved control.

---

# 66. GENERATION BATCHING

When exploring:

define a controlled variable.

Example:

KEEP FIXED:
character, location, lighting.

VARY:
camera angle.

Generate a small batch.

Compare outputs.

Do not vary everything simultaneously when trying to discover why one result is better.

---

# 67. A/B PROMPT TESTING

For meaningful comparisons:

Prompt A:
Prompt B:

Keep constant:

- model
- references
- settings
- subject
- output

Change only the variable being tested.

Record:

result
quality
failure
control
continuity
time
resource usage

---

# 68. PROMPT BENCHMARKS

The studio may maintain benchmark tests for important models.

Benchmark categories:

CHARACTER CONSISTENCY

LOCATION CONSISTENCY

MOTION

CAMERA

LIP SYNC

TEXT

PHYSICS

LIGHTING

STYLE

VFX

SCIENTIFIC VISUALIZATION

HISTORICAL RECONSTRUCTION

Benchmarks should use standardized test prompts.

---

# 69. MODEL SELECTION

Choose models according to the task.

Evaluate:

quality
control
consistency
speed
hardware requirements
cost
rights / terms
reference support
workflow integration

Do not select a model solely because it produces impressive isolated examples.

---

# 70. HARDWARE-AWARE PROMPTING

When local generation is used, consider:

GPU VRAM

RAM

resolution

batch size

sampling

upscaling

sequence length

model size

offloading

render time

storage

The prompt system should work within actual compute constraints.

---

# 71. COMFYUI INTEGRATION

For ComfyUI workflows record:

Workflow ID:
Workflow Version:
Model:
Checkpoint:
LoRA:
ControlNet:
VAE:
Sampler:
Steps:
CFG:
Seed:
Resolution:
Upscaler:
Input References:
Output:
Prompt ID:
Generation ID:

The prompt should not be considered the only source of generation state.

The workflow itself is part of the production asset.

---

# 72. AI VIDEO WORKFLOW RECORD

For video generation record:

Video Model:
Version:
Image-to-Video or Text-to-Video:
Input Image:
Prompt:
Motion Description:
Camera:
Duration:
Aspect Ratio:
Resolution:
Seed where supported:
Reference Controls:
Output:
Selected Take:
Failure:
QC:
Version:

---

# 73. IMAGE-TO-VIDEO PRINCIPLE

When a strong keyframe exists:

Use it as an anchor when the model supports reference-based video generation.

Control:

identity
composition
environment
lighting
action
camera motion

Avoid unnecessarily regenerating the entire visual identity.

---

# 74. KEYFRAME PRINCIPLE

Important shots may use:

KEYFRAME A

→ MOTION

→ KEYFRAME B

This can provide better continuity than asking a model to invent the entire sequence without anchors.

---

# 75. SHOT DECOMPOSITION

If a requested generation is too complex, decompose it.

Instead of:

Character walking through a massive crowd while camera circles, weather changes, building collapses, lighting changes, and dialogue occurs.

Consider:

SHOT A
Establish environment.

SHOT B
Character enters.

SHOT C
Crowd interaction.

SHOT D
Camera movement.

SHOT E
Major event.

SHOT F
Reaction.

This improves editorial control.

---

# 76. PROMPT AND EDITORIAL CONTROL

Do not design prompts independently from editing.

Before generating a shot ask:

How long will it likely be used?

What frame begins the shot?

What frame ends the shot?

Where will the cut occur?

What coverage is missing?

What should the editor be able to choose?

Generate editorially useful material rather than isolated spectacle.

---

# 77. PROMPT AND SOUND

For visual prompts, identify relevant sound context when it affects motion or performance.

Examples:

heavy machinery

rain

crowd noise

door slam

distant siren

music-driven movement

Sound context can help define expected action, even when generated separately.

---

# 78. PROMPT AND COLOR

Record intended color direction before generation when continuity matters.

Example:

MATCH SCENE PALETTE:
muted blue-gray environment with restrained warm practical lights.

This helps reduce uncontrolled visual variation.

---

# 79. PROMPT AND PRODUCTION DESIGN

AI environments should use approved:

- location references
- architectural references
- prop references
- material references
- era references

Do not allow AI generation to redefine the world accidentally.

---

# 80. PROMPT AND PERFORMANCE

Performance prompts should be connected to:

Character ID

Scene objective

Emotional state

Relationship

Subtext

Action

Camera

Edit intention

The model should receive enough context to produce useful performance rather than generic animation.

---

# 81. PROMPT AND CONTINUITY

When a prompt creates a continuity-critical output, explicitly identify:

PREVIOUS SHOT

CURRENT SHOT

NEXT EXPECTED STATE

This creates temporal awareness.

---

# 82. PROMPT AND QC

Every important prompt should have predefined QC questions.

Example:

Does the character match CHAR_002?

Does the location match LOC_003?

Does the camera match the approved shot design?

Are there temporal artifacts?

Is the lighting consistent?

Is the output resolution correct?

Does it contain unintended text?

Does the result satisfy the story purpose?

---

# 83. PROMPT REVIEW

Before executing an important prompt, inspect:

PURPOSE

CLARITY

CONSTRAINTS

REFERENCES

CONTINUITY

MODEL

TECHNICAL OUTPUT

QC CRITERIA

If these are incomplete, improve the prompt before generating.

---

# 84. PROMPT APPROVAL WORKFLOW

DRAFT

↓

TEST

↓

COMPARE

↓

REVIEW

↓

REVISE

↓

APPROVE

↓

LOCK

↓

REUSE

↓

AUDIT

↓

UPDATE WHEN NECESSARY

---

# 85. PROMPT LIBRARY ENTRY TEMPLATE

Prompt ID:
Name:
Department:
Purpose:
Project Type:
Use Case:
Model:
Version:
Status:
Tags:
Variables:
Prompt:
Negative Constraints:
Reference Requirements:
Input Requirements:
Output Requirements:
QC Criteria:
Known Failure Modes:
Notes:
Created:
Updated:

---

# 86. MASTER PROMPT TEMPLATE

PROJECT:
PROJECT_ID:

TASK:
TASK_ID:

ENTITY:
ENTITY_ID:

PURPOSE:

SHOT / SCENE CONTEXT:

SUBJECT:

CHARACTER:

LOCATION:

TIME:

WEATHER:

ACTION:

PERFORMANCE:

CAMERA:

LENS:

COMPOSITION:

MOVEMENT:

LIGHTING:

COLOR:

MATERIALS:

ATMOSPHERE:

STYLE:

MOOD:

CONTINUITY:

REFERENCES:

HARD CONSTRAINTS:

SOFT CONSTRAINTS:

NEGATIVE CONSTRAINTS:

MODEL:

MODEL VERSION:

WORKFLOW:

OUTPUT:

QC CRITERIA:

---

# 87. AI IMAGE PROMPT TEMPLATE

Subject:
Environment:
Action:
Composition:
Camera:
Lens:
Lighting:
Color:
Materials:
Atmosphere:
Style:
Mood:
Continuity:
Reference:
Constraints:
Negative Constraints:
Output:

---

# 88. AI VIDEO PROMPT TEMPLATE

Subject:
Starting State:
Action:
Performance:
Movement:
Camera:
Lens:
Composition:
Lighting:
Environment Motion:
Physics:
Emotional Beat:
Ending State:
Continuity:
Reference:
Constraints:
Negative Constraints:
Duration:
Output:

---

# 89. CHARACTER GENERATION TEMPLATE

Character ID:
Identity:
Age:
Face:
Body:
Hair:
Skin:
Wardrobe:
Accessories:
Expression:
Pose:
Environment:
Lighting:
Camera:
Style:
Reference:
Continuity:
Output:

---

# 90. ENVIRONMENT GENERATION TEMPLATE

Location ID:
Architecture:
Geography:
Scale:
Materials:
Objects:
Vegetation:
Weather:
Time:
Lighting:
Color:
Atmosphere:
Human Activity:
Camera:
Reference:
Continuity:
Output:

---

# 91. PROMPT QUALITY CHECKLIST

Before use:

□ Purpose is clear

□ Subject is clear

□ Context is defined

□ Important constraints are explicit

□ References are identified

□ Continuity requirements are included

□ Camera is sufficiently specified

□ Lighting is sufficiently specified

□ Action is sufficiently specified

□ Output requirements are clear

□ Model is appropriate

□ QC criteria exist

---

# 92. GENERATION REVIEW CHECKLIST

After generation:

□ Identity matches

□ Environment matches

□ Composition works

□ Camera behaves correctly

□ Lighting works

□ Materials are plausible

□ Action is coherent

□ Physics are acceptable

□ Temporal consistency is acceptable

□ No major AI artifacts

□ Continuity is preserved

□ Story purpose is served

□ Output specifications are correct

---

# 93. PROMPT EFFICIENCY RULE

Before adding more words, ask:

What exact ambiguity am I trying to remove?

Add information only when it improves control.

---

# 94. PROMPT FAILURE RULE

When repeated generations fail, do not simply add more adjectives.

Instead examine:

- prompt structure
- reference quality
- task complexity
- model capability
- workflow
- settings
- shot design
- decomposition

The solution may be changing the production method rather than making the prompt longer.

---

# 95. PROMPT KNOWLEDGE LOOP

Every major prompt should contribute to studio knowledge:

PROMPT

→ GENERATION

→ RESULT

→ QC

→ FAILURE / SUCCESS

→ LESSON

→ LIBRARY

→ FUTURE PROMPT

This makes the studio improve over time.

---

# 96. PROMPT ARCHIVE

Retain important:

- approved prompts
- benchmark prompts
- failed prompts with useful lessons
- model-specific prompts
- project-critical prompts
- reusable modules

Mark retired prompts rather than silently deleting them.

---

# 97. PROMPT SECURITY

Never include:

- API keys
- passwords
- tokens
- private credentials
- authentication secrets

inside prompts stored in GitHub.

Use references such as:

ENV:MODEL_API_KEY

rather than storing the secret itself.

---

# 98. PROMPT RIGHTS

Consider rights implications for:

- reference images
- reference videos
- voices
- likenesses
- copyrighted material
- logos
- brands
- proprietary assets
- model usage terms

Prompt existence does not establish permission to use the referenced material.

---

# 99. PROMPT GOVERNANCE

Claude should treat:

APPROVED PROMPT
as reusable production knowledge.

DRAFT PROMPT
as experimental.

RETIRED PROMPT
as historical knowledge, not default production material.

REJECTED PROMPT
as unavailable for production unless explicitly reviewed again.

---

# 100. FINAL PROMPT SYSTEM STANDARD

A good studio prompt is:

PURPOSEFUL

SPECIFIC

CONTROLLABLE

REPEATABLE

TRACEABLE

CONTINUITY-AWARE

MODEL-AWARE

TECHNICALLY VALID

EDITORIALLY USEFUL

QC-READY

The objective is not to create the longest prompt.

The objective is to create the clearest production instruction that gives the studio the required control over the result.

PROMPT
→ GENERATE
→ INSPECT
→ SELECT
→ QC
→ APPROVE
→ VERSION
→ REUSE

That is the Studio Prompt System.
