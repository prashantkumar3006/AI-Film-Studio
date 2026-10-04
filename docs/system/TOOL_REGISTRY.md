# STUDIO TOOL REGISTRY

## 1. PURPOSE

The Tool Registry is the authoritative inventory of software, AI models, services, plugins, APIs, hardware, and production tools available to the AI Film Studio.

It tells Claude:

- what tools exist
- what each tool is for
- which department owns it
- what inputs it accepts
- what outputs it produces
- where it fits in the pipeline
- what hardware it requires
- what limitations it has
- whether it is approved for production
- what alternatives exist
- how the tool should be used safely and efficiently

The registry prevents random tool selection and helps Claude choose the appropriate production technology for each task.

---

# 2. CORE PRINCIPLE

A tool is selected because it solves a production problem.

Do not select a tool merely because:

- it is new
- it is popular
- it is expensive
- it produces impressive demos
- another creator uses it
- it is available

Evaluate:

PURPOSE
→ CAPABILITY
→ CONTROL
→ QUALITY
→ COMPATIBILITY
→ COST
→ SPEED
→ RESOURCE REQUIREMENTS
→ RIGHTS / TERMS
→ RELIABILITY

---

# 3. TOOL CATEGORIES

The studio may classify tools as:

- AI
- VIDEO_GENERATION
- IMAGE_GENERATION
- AUDIO_GENERATION
- MUSIC_GENERATION
- VOICE
- EDITING
- COLOR
- VFX
- MOTION_GRAPHICS
- ANIMATION
- 3D
- COMPOSITING
- STORYBOARD
- PREVIS
- SCREENWRITING
- RESEARCH
- SCRIPTING
- AUTOMATION
- FILE_MANAGEMENT
- STORAGE
- COLLABORATION
- QC
- DELIVERY
- TRANSCRIPTION
- SUBTITLING
- CAPTIONING
- DOCUMENTATION
- PROJECT_MANAGEMENT
- HARDWARE
- HPC
- LOCAL_AI
- CLOUD_AI
- API
- PLUGIN
- MCP
- SECURITY

---

# 4. TOOL RECORD

Every important tool should have a canonical record.

Tool ID:
Tool Name:
Provider:
Category:
Subcategory:
Department:
Primary Purpose:
Secondary Uses:
Platform:
Operating System:
Version:
Access Method:
License:
Subscription:
API Available:
Local / Cloud:
Input:
Output:
Supported Formats:
Hardware Requirement:
VRAM Requirement:
RAM Requirement:
Storage Requirement:
Network Requirement:
Typical Runtime:
Estimated Cost:
Production Status:
Reliability:
Known Limitations:
Known Failure Modes:
Alternatives:
Documentation:
Last Tested:
Tested By:
Notes:

---

# 5. TOOL STATUS

Use:

NOT_TESTED

EXPERIMENTAL

TESTING

APPROVED

LIMITED

DEPRECATED

RETIRED

Explanation:

NOT_TESTED
The studio has not evaluated the tool.

EXPERIMENTAL
The tool is being explored.

TESTING
The tool is under structured evaluation.

APPROVED
Suitable for the specified production uses.

LIMITED
Usable only under specified conditions.

DEPRECATED
Existing projects may still use it, but new work should normally use another tool.

RETIRED
Do not use for new production.

---

# 6. ACCESS TYPES

A tool may be accessed through:

LOCAL
Installed directly on studio hardware.

CLOUD
Remote web-based service.

API
Programmatic service.

PLUGIN
Integrated into another application.

MCP
Connected through a Model Context Protocol server.

CLI
Command-line application.

HPC
Runs through high-performance computing infrastructure.

HYBRID
Multiple access methods.

---

# 7. PRODUCTION ROLE

For every approved tool define:

PRIMARY ROLE

SECONDARY ROLE

WHEN TO USE

WHEN NOT TO USE

Example:

Primary:
Video generation

Use when:
A shot requires AI-generated motion.

Do not use when:
Existing footage already satisfies the shot.

---

# 8. TOOL SELECTION LOGIC

When a task requires a tool, Claude should ask:

1. What problem needs solving?
2. What output is required?
3. What tools can produce that output?
4. Which tools satisfy the project's technical requirements?
5. Which tools preserve continuity?
6. Which tools fit available hardware?
7. Which tools fit the schedule?
8. Which tools fit budget/resource constraints?
9. Which tools have acceptable rights/terms?
10. Which tool provides sufficient control?

Then select an appropriate tool or present alternatives when uncertainty is significant.

---

# 9. TOOL DECISION RECORD

For important tool selections record:

Decision ID:
Task:
Project:
Required Capability:
Candidates:
Selected Tool:
Reason:
Alternative:
Hardware:
Cost:
Expected Runtime:
Limitations:
Rights / Terms:
Decision Owner:
Date:
Version:

---

# 10. AI TOOL REGISTRY

AI tools should additionally record:

Model:
Model Version:
Provider:
Modality:
Input Modalities:
Output Modalities:
Context / Prompt Capability:
Reference Support:
Control Features:
Generation Length:
Resolution:
Consistency:
Character Consistency:
Environment Consistency:
Motion Quality:
Audio Quality:
Editing Capability:
Local Execution:
Cloud Execution:
API:
Workflow Integration:
Known Artifacts:
Safety / Rights Notes:
Benchmark Status:

---

# 11. IMAGE GENERATION RECORD

Tool:
Model:
Version:
Provider:
Text-to-Image:
Image-to-Image:
Reference Image:
Character Reference:
ControlNet / Control Inputs:
Masking:
Inpainting:
Outpainting:
Upscaling:
Resolution:
Aspect Ratios:
Seed:
Batch:
Style Control:
Consistency:
Local / Cloud:
API:
Cost:
Limitations:

---

# 12. VIDEO GENERATION RECORD

Tool:
Model:
Version:
Provider:
Text-to-Video:
Image-to-Video:
Video-to-Video:
Reference Support:
Character Consistency:
Camera Control:
Motion Control:
Duration:
Resolution:
Frame Rate:
Aspect Ratios:
Seed:
Prompt Control:
First / Last Frame Control:
Editing Controls:
Audio:
API:
Local Execution:
Hardware:
Cost:
Limitations:

---

# 13. AUDIO / VOICE TOOL RECORD

Tool:
Model:
Version:
Provider:
Speech Synthesis:
Voice Cloning:
Voice Design:
Language:
Accent:
Emotion:
Prosody:
Lip Sync:
Audio Editing:
Noise Reduction:
Dialogue Cleanup:
Sample Rate:
Export:
API:
Rights / Consent Requirements:
Known Limitations:

---

# 14. MUSIC TOOL RECORD

Tool:
Model:
Version:
Provider:
Text-to-Music:
Instrument Control:
Genre Control:
Tempo:
Duration:
Vocals:
Stems:
MIDI:
Editing:
Looping:
Reference Input:
Export:
Commercial Usage:
Rights / Terms:
Known Limitations:

---

# 15. EDITING SOFTWARE RECORD

Software:
Version:
Platform:
Primary Function:
Supported Codecs:
Image Sequences:
Proxy Workflow:
Multicam:
Color Integration:
Audio Integration:
VFX Integration:
AI Integration:
Scripting:
Automation:
Collaboration:
Hardware:
Known Limitations:
Project File Format:
Archive Considerations:

---

# 16. COLOR SOFTWARE RECORD

Software:
Version:
Color Management:
RAW Support:
HDR:
SDR:
Scopes:
Secondary Corrections:
Tracking:
Power Windows:
Film Emulation:
Noise Reduction:
Grain:
VFX Integration:
Export:
Hardware:
Known Limitations:

---

# 17. VFX SOFTWARE RECORD

Software:
Version:
Compositing:
Roto:
Tracking:
Keying:
Cleanup:
3D:
Particles:
Motion Graphics:
AI Integration:
Scripting:
GPU Acceleration:
Render Management:
Supported Formats:
Hardware:
Known Limitations:

---

# 18. ANIMATION TOOL RECORD

Software:
Version:
2D:
3D:
Character Animation:
Facial Animation:
Rigging:
Lip Sync:
Motion Capture:
Procedural Animation:
Physics:
Camera:
Rendering:
AI Integration:
Export:
Hardware:
Known Limitations:

---

# 19. 3D TOOL RECORD

Software:
Version:
Modeling:
Sculpting:
Texturing:
Rigging:
Animation:
Simulation:
Lighting:
Rendering:
USD:
Alembic:
FBX:
OBJ:
GLTF:
Python:
GPU:
Cloud Rendering:
Known Limitations:

---

# 20. RESEARCH TOOL RECORD

Tool:
Version:
Research Type:
Web Search:
Academic Search:
PDF:
Citation Management:
Database Access:
Semantic Search:
Local Knowledge:
AI Assistance:
Export:
API:
Automation:
Source Traceability:
Known Limitations:

Research tools must not be treated as evidence themselves.

The underlying sources remain the evidence.

---

# 21. TRANSCRIPTION TOOL RECORD

Tool:
Model:
Languages:
Speaker Diarization:
Timestamp Accuracy:
Punctuation:
Translation:
Export:
Subtitle:
Caption:
API:
Cost:
Known Limitations:

---

# 22. SUBTITLE / CAPTION TOOL RECORD

Tool:
Input:
Output:
SRT:
VTT:
ASS:
Burn-In:
Positioning:
Styling:
Speaker Labels:
Timing:
Translation:
QC:
Accessibility:
Known Limitations:

---

# 23. AUTOMATION TOOL RECORD

Tool:
Type:
Trigger:
Inputs:
Outputs:
APIs:
Webhooks:
File Access:
GitHub:
Adobe:
Cloud:
Local:
Scheduling:
Logging:
Error Handling:
Retry:
Security:
Permissions:
Known Limitations:

---

# 24. SCRIPTING TOOL RECORD

Language:
Version:
Environment:
Libraries:
Purpose:
Input:
Output:
Dependencies:
Execution Method:
OS:
GPU:
CPU:
Memory:
Logging:
Error Handling:
Version Control:
Reproducibility:
Known Limitations:

---

# 25. STORAGE TOOL RECORD

Storage:
Type:
Capacity:
Usable Capacity:
Connection:
Read Speed:
Write Speed:
Backup:
Redundancy:
Encryption:
Access:
Location:
Project Use:
Archive Use:
Recovery:
Known Limitations:

---

# 26. HARDWARE RECORD

Hardware ID:
Device:
Category:
Manufacturer:
Model:
CPU:
GPU:
VRAM:
RAM:
Storage:
Network:
Operating System:
Cooling:
Power:
Primary Use:
Secondary Use:
Available Capacity:
Known Bottlenecks:
Maintenance:
Status:

Hardware categories:

- WORKSTATION
- LAPTOP
- SERVER
- GPU_SERVER
- NAS
- STORAGE
- HPC
- RENDER_NODE
- MOBILE
- CAPTURE_DEVICE
- AUDIO_INTERFACE
- CAMERA
- PERIPHERAL

---

# 27. GPU RECORD

GPU:
VRAM:
Architecture:
Driver:
CUDA / Compute:
Recommended Tasks:
Maximum Tested Resolution:
Typical AI Models:
Batch Capability:
Known Memory Limits:
Temperature:
Power:
Performance Notes:

Track VRAM limitations explicitly because AI workflows are highly memory-sensitive.

---

# 28. SOFTWARE ENVIRONMENT RECORD

Environment ID:
Name:
Operating System:
Python:
Conda:
CUDA:
Drivers:
Packages:
AI Frameworks:
VFX Software:
Editing Software:
Plugins:
Environment Variables:
Storage:
Status:
Last Verified:

Production environments should be documented for reproducibility.

---

# 29. PYTHON ENVIRONMENT

Environment:

materials_ml

Example fields:

Python Version:
Conda Environment:
NumPy:
Pandas:
Scikit-Learn:
XGBoost:
PyTorch:
Transformers:
OpenCV:
Pillow:
ASE:
pymatgen:

Only record packages that are actually installed and verified.

---

# 30. PLUGIN RECORD

Plugin ID:
Plugin Name:
Host Application:
Version:
Provider:
Purpose:
Department:
Installation:
License:
Compatibility:
Dependencies:
Permissions:
Security Notes:
Status:
Last Tested:

---

# 31. MCP TOOL RECORD

MCP ID:
MCP Name:
Server:
Version:
Provider:
Application:
Capabilities:
Read:
Write:
Search:
Create:
Edit:
Delete:
Authentication:
Permissions:
Data Access:
Local / Remote:
Status:
Known Limitations:

MCP connections should be treated as operational tools, not automatically trusted sources of truth.

---

# 32. CONNECTOR RECORD

Connector:
Service:
Account Type:
Capabilities:
Read:
Write:
Search:
Create:
Update:
Delete:
Authentication:
Permissions:
Rate Limits:
Data Scope:
Status:
Notes:

---

# 33. ADOBE TOOL FAMILY

Record each Adobe application separately.

Examples:

Premiere Pro

After Effects

Photoshop

Illustrator

Audition

Media Encoder

Lightroom where relevant

Substance 3D tools where relevant

For each record:

Application:
Version:
Primary Use:
AI Features:
API / Automation:
Plugin Support:
Supported Formats:
Integration:
Hardware:
Known Limitations:
Studio Status:

Do not assume capability based only on the Adobe product family.

Record the specific application's tested capability.

---

# 34. GITHUB ROLE

GitHub should primarily store:

- studio operating system
- skills
- Markdown documentation
- prompts
- templates
- scripts
- configuration examples
- metadata
- workflow definitions
- project records where appropriate
- version history
- automation code

GitHub should generally NOT be treated as the primary home for:

- massive raw video
- large image sequences
- heavy cache files
- render caches
- large temporary files

unless the workflow explicitly requires it.

---

# 35. GITHUB TOOL RECORD

Service:
GitHub

Role:
Studio knowledge and code repository

Typical contents:

- CLAUDE.md
- SKILL.md files
- project documentation
- prompts
- scripts
- templates
- manifests
- automation
- versioned knowledge

Security:

Never commit:

- API keys
- passwords
- tokens
- credentials
- private keys
- session data

---

# 36. CLAUDE ROLE

Claude is the studio's orchestration and intelligence layer.

Potential functions:

- planning
- research
- writing
- production coordination
- tool selection
- task generation
- prompt generation
- critique
- QC reasoning
- documentation
- knowledge management
- workflow orchestration
- connected-tool interaction

Claude should use the Tool Registry to determine which actual production tools are available.

---

# 37. ADOBE + CLAUDE WORKFLOW

Where an appropriate connection exists:

Claude
→ plans task
→ prepares structured instructions
→ invokes available tool / connector
→ monitors or interprets result
→ records output
→ updates project state

Do not assume that having an Adobe subscription automatically means every Adobe operation is callable directly from Claude.

Capabilities must be verified through the actual connected integration.

---

# 38. AI MODEL REGISTRY

The studio should maintain a dedicated model table.

| Model ID | Model | Provider | Modality | Primary Use | Access | Hardware | Status |
|---|---|---|---|---|---|---|---|
| MODEL_001 | | | | | | | |
| MODEL_002 | | | | | | | |
| MODEL_003 | | | | | | | |

---

# 39. TOOL CAPABILITY MATRIX

Maintain a high-level capability matrix.

| Tool | Image | Video | Audio | Music | Voice | Edit | VFX | Color | Animation | Research | Automation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

Values:

YES
NO
LIMITED
TESTING

Do not fill a cell from assumption.

Use verified tool capability.

---

# 40. DEPARTMENT TOOL MATRIX

| Department | Primary Tool | Secondary Tool | AI Tool | Automation | Status |
|---|---|---|---|---|---|
| Director | | | | | |
| Writer | | | | | |
| Research | | | | | |
| Production Design | | | | | |
| Casting | | | | | |
| Storyboard / Previs | | | | | |
| Cinematography | | | | | |
| AI Generation | | | | | |
| Animation | | | | | |
| Production | | | | | |
| Edit | | | | | |
| VFX / Motion | | | | | |
| Sound | | | | | |
| Music | | | | | |
| Color | | | | | |
| Continuity | | | | | |
| Technical Post | | | | | |
| QC | | | | | |
| Distribution | | | | | |
| Marketing | | | | | |
| Archive | | | | | |

---

# 41. TASK-TO-TOOL MAPPING

A task may specify:

Task:
Required Capability:
Preferred Tool:
Fallback Tool:
Why:
Hardware:
Time:
Cost:
Rights:
Status:

Example:

Task:
Generate environment concept

Required Capability:
High-quality concept image generation

Preferred:
Approved image model

Fallback:
Alternative approved image model

---

# 42. FALLBACK SYSTEM

Important workflows should identify fallback tools.

Primary Tool:
Fallback 1:
Fallback 2:

Trigger:

- service unavailable
- API failure
- insufficient quality
- hardware limitation
- unexpected cost
- rights restriction
- model limitation

Do not switch tools without checking compatibility and downstream impact.

---

# 43. TOOL FAILURE RECORD

Failure ID:
Tool:
Version:
Task:
Project:
Date:
Failure:
Error:
Impact:
Workaround:
Resolution:
Root Cause:
New Limitation:
Recommended Fallback:
Lessons:
Status:

Repeated failures should become studio knowledge.

---

# 44. TOOL BENCHMARK

For important tools test:

QUALITY

CONSISTENCY

CONTROL

SPEED

RESOURCE USAGE

REPRODUCIBILITY

INTEGRATION

RELIABILITY

COST

RIGHTS / TERMS

Record the results.

Do not treat marketing claims as benchmark results.

---

# 45. TOOL BENCHMARK RECORD

Benchmark ID:
Tool:
Version:
Task:
Test Input:
Settings:
Hardware:
Runtime:
Output:
Quality:
Consistency:
Failures:
Resource Usage:
Cost:
Result:
Notes:

---

# 46. TOOL COMPARISON

When comparing tools, use task-specific criteria.

Example:

Task:
Generate a 6-second cinematic environment shot.

Compare:

- visual quality
- temporal consistency
- camera control
- reference adherence
- render time
- VRAM / compute
- cost
- workflow compatibility

Do not declare one tool universally superior.

A tool may be better suited to one task and less suitable to another.

---

# 47. TOOL VERSION CONTROL

Record:

Tool:
Old Version:
New Version:
Change Date:
Reason:
Compatibility:
Known Changes:
Regression Test:
Result:
Affected Projects:
Action:

Do not silently update production-critical tools without checking compatibility.

---

# 48. VERSION PINNING

For reproducible workflows, pin critical versions.

Examples:

MODEL_VERSION

SOFTWARE_VERSION

PLUGIN_VERSION

PYTHON_VERSION

CUDA_VERSION

DRIVER_VERSION

WORKFLOW_VERSION

A production pipeline may fail when one of these changes unexpectedly.

---

# 49. ENVIRONMENT SNAPSHOT

For major production environments record:

OS:
GPU:
Driver:
CUDA:
Python:
Conda:
AI Framework:
Editing Software:
VFX Software:
Plugins:
Model Versions:
Workflow Versions:

This allows technical post to reconstruct the environment.

---

# 50. LICENSE RECORD

Tool:
License:
Subscription:
Owner:
Seats:
Expiration:
Commercial Use:
API Terms:
Usage Restrictions:
Redistribution:
Training / Data Terms:
Project Restrictions:
Renewal:
Status:

Never assume that a paid subscription means unrestricted commercial rights.

Check the applicable terms.

---

# 51. COST RECORD

Tool:
Pricing Model:
Subscription:
Per Generation:
Per Minute:
Per Render:
Per API Call:
Storage:
Compute:
Additional Charges:
Expected Monthly Usage:
Estimated Project Cost:

Costs may change.

When current pricing matters, verify current provider information before making a production decision.

---

# 52. RESOURCE ESTIMATION

Before large generation batches estimate:

Number of outputs:
Resolution:
Duration:
Model:
Batch size:
Expected render time:
GPU:
VRAM:
Storage generated:
Network transfer:
Cost:

Then decide whether to:

- run locally
- run in cloud
- reduce resolution
- batch
- prototype first
- change model
- change workflow

---

# 53. TOOL SECURITY

Before connecting a tool, evaluate:

What data does it access?

What credentials does it require?

Where does data go?

Does it upload source material?

What permissions are granted?

Can access be limited?

Can credentials be rotated?

Are project secrets exposed?

Does the tool connect to external services?

Record important security considerations.

---

# 54. PERMISSION PRINCIPLE

Use least privilege.

A tool should receive only the access required for its production task.

Do not grant broad access merely for convenience.

---

# 55. DATA CLASSIFICATION

When relevant classify tool-accessed data:

PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED

Tools receiving RESTRICTED material require additional scrutiny.

---

# 56. LOCAL VS CLOUD DECISION

Use local workflows when appropriate for:

- privacy
- repeatability
- offline operation
- predictable compute
- large-volume workloads
- existing hardware capability

Use cloud workflows when appropriate for:

- models unavailable locally
- burst compute
- specialized infrastructure
- managed services
- rapid experimentation

Evaluate each workflow independently.

---

# 57. HYBRID PIPELINE

A production may use:

Claude
→ GitHub
→ local workstation
→ Adobe
→ AI cloud service
→ local post-production
→ archive

Every transfer between systems should be understood.

Track:

INPUT

PROCESS

OUTPUT

TRANSFER

STORAGE

OWNERSHIP

RIGHTS

---

# 58. TOOL INTEGRATION GRAPH

Example:

Claude
↔ GitHub

Claude
↔ Connected MCP / Plugins

GitHub
↔ Scripts

Scripts
↔ Local AI

Local AI
↔ Asset Pipeline

Adobe
↔ Editorial / VFX / Audio

Storage
↔ All Media

QC
↔ Final Outputs

The actual studio graph should be maintained as integrations are added.

---

# 59. TOOL DEPENDENCIES

A tool may depend on:

- operating system
- GPU driver
- CUDA
- Python
- libraries
- plugins
- APIs
- credentials
- storage
- network
- other software

Record important dependencies.

---

# 60. DEPENDENCY FAILURE

When a tool fails because of dependency issues:

Record:

Tool:
Dependency:
Expected Version:
Installed Version:
Error:
Resolution:
Environment:
Date:

Do not randomly upgrade packages in a production environment without considering downstream compatibility.

---

# 61. TOOL INSTALLATION RECORD

Tool:
Version:
Installer / Source:
Date:
Environment:
Dependencies:
Configuration:
License:
Credentials:
Test:
Result:
Status:

Do not store credentials in the installation record.

---

# 62. TOOL REMOVAL / RETIREMENT

Before retiring a production-critical tool:

1. identify projects using it
2. identify dependencies
3. identify replacement
4. test replacement
5. preserve necessary project files
6. document migration
7. mark the tool DEPRECATED or RETIRED

Do not remove an important tool blindly.

---

# 63. TOOL DISCOVERY

When discovering a new tool:

Record:

Name:
Provider:
What it claims to do:
Relevant capability:
Potential use:
Potential problems:
License:
Cost:
Integration:
Security:
Test Plan:

Do not add it to the approved production list until evaluated.

---

# 64. TOOL EVALUATION WORKFLOW

DISCOVER

↓

DOCUMENT

↓

TEST

↓

BENCHMARK

↓

CHECK RIGHTS

↓

CHECK SECURITY

↓

CHECK HARDWARE

↓

CHECK INTEGRATION

↓

REVIEW

↓

APPROVE / LIMIT / REJECT

↓

REGISTER

---

# 65. APPROVED TOOL LIST

Maintain an explicit approved list.

| Tool ID | Tool | Department | Use | Version | Status |
|---|---|---|---|---|---|
| | | | | | APPROVED |

Approval should be task-specific where necessary.

---

# 66. TOOL RESTRICTIONS

A tool may be approved only for certain uses.

Example:

Tool:
Approved for:
Concept art

Not approved for:
Final documentary reconstruction

Reason:
Insufficient provenance / factual control

Restrictions must be explicit.

---

# 67. TOOL RECOMMENDATION PROTOCOL

When Claude needs to recommend a tool internally, provide:

REQUIRED CAPABILITY:

AVAILABLE TOOLS:

PRIMARY CANDIDATE:

WHY:

LIMITATIONS:

FALLBACK:

RESOURCE IMPACT:

RIGHTS / TERMS:

CONFIDENCE:

Do not hide important limitations.

---

# 68. TOOL SWITCH PROTOCOL

When switching tools mid-project:

CURRENT TOOL:

REASON FOR SWITCH:

NEW TOOL:

COMPATIBILITY:

ASSET IMPACT:

PROMPT IMPACT:

VERSION IMPACT:

EDIT IMPACT:

COLOR IMPACT:

SOUND IMPACT:

QC IMPACT:

RIGHTS IMPACT:

APPROVAL:

MIGRATION TASKS:

---

# 69. TOOLCHAIN DESIGN

Do not choose tools independently.

Design the toolchain.

Example:

Research
→ Writer

Writer
→ Storyboard

Storyboard
→ AI Generation

AI Generation
→ Asset Pipeline

Asset Pipeline
→ Edit

Edit
→ VFX

Edit
→ Sound

VFX
→ Color

Color
→ QC

QC
→ Delivery

Each tool should exchange usable outputs with the next stage.

---

# 70. FORMAT COMPATIBILITY

For important tools record:

Input Formats:

Output Formats:

Intermediate Formats:

Preferred Master Formats:

Potential Loss:

Potential Metadata Loss:

Potential Color Shift:

Potential Audio Issue:

Potential Frame Rate Issue:

Never assume that "export completed" means the transfer was lossless or correct.

---

# 71. COLOR PIPELINE COMPATIBILITY

Track:

Color Space:

Transfer Function:

Bit Depth:

HDR / SDR:

RAW:

Image Sequence:

LUT:

Metadata:

VFX Compatibility:

Editing Compatibility:

Delivery Compatibility:

---

# 72. AUDIO PIPELINE COMPATIBILITY

Track:

Sample Rate:

Bit Depth:

Channel Layout:

Codec:

Stems:

Metadata:

DAW Compatibility:

Video Editor Compatibility:

Delivery Requirements:

---

# 73. AI OUTPUT COMPATIBILITY

For generated media track:

Resolution:

Frame Rate:

Duration:

Codec:

Color:

Alpha:

Audio:

Metadata:

File Format:

Editor Compatibility:

VFX Compatibility:

Color Compatibility:

---

# 74. AUTOMATION COMPATIBILITY

Before automating a tool, determine:

API available?

CLI available?

File-based workflow?

Webhook?

Plugin?

MCP?

Manual-only?

Automation should use documented interfaces where possible.

---

# 75. MANUAL-ONLY TOOL

Some tools may be manual-only.

Record:

Manual Steps:
Operator:
Required Inputs:
Expected Output:
Verification:
Estimated Time:

Do not pretend a tool is automated merely because another AI can provide instructions for using it.

---

# 76. TOOL LOGGING

Important tool executions should record:

Tool:
Version:
Project:
Task:
Input:
Output:
Date:
Operator / Automation:
Result:
Error:
Notes:

This is especially useful for:

- AI generation
- rendering
- transcoding
- batch processing
- automated QC
- data processing

---

# 77. TOOL PERFORMANCE

Track where useful:

Runtime:
CPU:
GPU:
VRAM:
RAM:
Storage:
Network:
Failure Rate:
Throughput:

Performance should be measured on actual studio hardware where practical.

---

# 78. HUMBLE HARDWARE MODE

The studio should remain capable of working on constrained hardware.

When resources are limited:

1. reduce unnecessary resolution
2. use proxies
3. test short sequences
4. batch intelligently
5. offload appropriate tasks
6. use lighter models
7. avoid unnecessarily large contexts
8. schedule heavy jobs
9. preserve intermediate files
10. scale only after proving the workflow

The workflow should degrade gracefully rather than collapse completely.

---

# 79. WORKSTATION SCALING

The same production system should support:

SMALL LAPTOP

→ LOW RESOURCE MODE

WORKSTATION

→ STANDARD MODE

HIGH-END GPU WORKSTATION

→ HIGH PERFORMANCE MODE

GPU SERVER / CLOUD

→ LARGE SCALE MODE

The project data model should remain the same across these environments.

---

# 80. HARDWARE-AWARE WORKFLOW

Before executing a heavy task determine:

Required VRAM:
Available VRAM:
Estimated runtime:
Expected storage:
Can it fit locally?
Can it be tiled / chunked?
Can it use proxies?
Can it be batched?
Should it be cloud-rendered?

---

# 81. TOOL COST VS VALUE

When a tool costs money, evaluate:

Required capability:

Current alternative:

Time saved:

Quality gained:

Reliability gained:

Integration gained:

Project volume:

Recurring cost:

One-time cost:

Do not optimize purely for price.

Do not pay for capability the project does not require.

---

# 82. TOOL RETIREMENT KNOWLEDGE

When a tool is retired, preserve:

- version used
- reason for retirement
- workflows affected
- replacement
- migration instructions
- important compatibility notes

The studio should learn from tool transitions.

---

# 83. STUDIO TOOL DIRECTORY

Maintain this directory:

## AI

Image:
Video:
Voice:
Music:
Research:
Writing:
Animation:

## CREATIVE

Editing:
Color:
VFX:
Motion:
3D:
Audio:
Storyboard:

## PRODUCTION

Project Management:
Asset Management:
Storage:
Collaboration:

## ENGINEERING

Python:
Git:
Automation:
HPC:
Rendering:
Monitoring:

## DELIVERY

Encoding:
Subtitles:
QC:
Distribution:

Populate with actual approved tools.

---

# 84. CURRENT TOOL INVENTORY

Use this section as the live registry.

| Tool ID | Name | Category | Department | Access | Version | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

Update this table whenever a production-critical tool is added, removed, or materially changed.

---

# 85. CURRENT HARDWARE INVENTORY

| Hardware ID | Device | GPU | VRAM | RAM | Storage | Primary Use | Status |
|---|---|---|---:|---:|---:|---|---|
| | | | | | | | |

---

# 86. CURRENT AI MODEL INVENTORY

| Model ID | Model | Modality | Provider | Local/Cloud | Primary Use | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

---

# 87. CURRENT SOFTWARE INVENTORY

| Software ID | Application | Version | Primary Use | Platform | Status |
|---|---|---|---|---|---|
| | | | | | |

---

# 88. TOOL HEALTH

For each critical production tool track:

AVAILABLE

WORKING

DEGRADED

UNAVAILABLE

UNKNOWN

When a production-critical tool is unavailable, identify fallback options.

---

# 89. TOOL HEALTH CHECK

Tool:

Version:

Date:

Test:

Expected:

Actual:

Result:

Error:

Impact:

Action:

---

# 90. TOOL SECURITY REVIEW

For critical tools review:

□ Authentication understood

□ Permissions understood

□ External data transfer understood

□ Credentials securely stored

□ Project secrets protected

□ Access scope minimized

□ License reviewed

□ Data retention understood where relevant

□ Backup implications understood

□ Integration risks understood

---

# 91. TOOL REGISTRY AUDIT

Audit:

□ Important tools have IDs

□ Versions are recorded

□ Status is current

□ Departments are assigned

□ Capabilities are documented

□ Hardware requirements are documented

□ Major limitations are documented

□ Critical dependencies are documented

□ Production approvals are documented

□ Retired tools are marked

□ Fallbacks exist for critical workflows

□ Secrets are not stored

---

# 92. TOOL SELECTION FAILURE RULE

Do not recommend a tool solely because:

"it can do it."

The relevant question is:

"Can it do it reliably, at the required quality, within this project's technical, creative, rights, time, and resource constraints?"

---

# 93. NO UNVERIFIED CAPABILITY

If a capability has not been tested or verified:

mark it:

`UNVERIFIED`

Do not convert assumptions into registry facts.

---

# 94. TOOL KNOWLEDGE LOOP

DISCOVER

→ TEST

→ BENCHMARK

→ DOCUMENT

→ USE

→ OBSERVE

→ RECORD FAILURE / SUCCESS

→ UPDATE REGISTRY

→ IMPROVE TOOLCHAIN

The Tool Registry should become more accurate over time.

---

# 95. TOOLCHAIN REVIEW

For major projects, review:

Does each department have the required tools?

Are any tools redundant?

Are any critical capabilities missing?

Are there unnecessary subscriptions?

Are any tools causing bottlenecks?

Are format conversions creating quality loss?

Are hardware limits affecting production?

Are cloud dependencies creating risks?

Are fallback tools available?

---

# 96. PROJECT-SPECIFIC TOOL LOCK

A project may define:

Approved Toolchain:

Tool:
Version:
Model:
Version:
Workflow:
Version:

Once production begins, major changes should be documented through Change Control.

---

# 97. TOOLCHAIN SNAPSHOT

For a production milestone record:

Project:

Date:

OS:

Hardware:

Software:

AI Models:

Plugins:

Scripts:

Workflows:

Storage:

External Services:

Versions:

This snapshot supports reproducibility.

---

# 98. FINAL TOOL REGISTRY PRINCIPLE

THE RIGHT TOOL

is not necessarily:

the newest

the biggest

the most expensive

the most famous

or the most visually impressive.

The right tool is the one that reliably satisfies the production requirement within the project's constraints.

The Studio Tool Registry exists to make that decision explicit, repeatable, testable, and traceable.

---

# 99. FINAL STANDARD

Every important production tool should be:

IDENTIFIED

CLASSIFIED

TESTED

VERSIONED

DOCUMENTED

SECURED

CONNECTED APPROPRIATELY

MONITORED

AND REPLACED WHEN NECESSARY

The toolchain should serve the film.

The film should never become a demonstration of the toolchain.
