PD&I — PATCH 001 / SOURCE OF TRUTH FOUNDATION
AI STUDIO ONLY — READ / MAP / VERIFY / DOCUMENT

IMPORTANT:
- Work only in the local AI Studio workspace.
- Do NOT modify GitHub.
- Do NOT modify piping-design-skill.
- Do NOT merge/rebase/cherry-pick branches.
- Do NOT rewrite or replace V4.8d.
- Do NOT change runtime behavior in this first patch.
- Do NOT delete or rename production files.

OBJECTIVE
Establish one verified Source of Truth before any further ISO repair.

KNOWN AUDIT FACTS
- Repository default branch is main.
- src/pdi/model/index.ts declares a canonical model boundary.
- src/pdi/isometric/PdiIsometricEditor.tsx delegates directly to the V4.8d engine.
- V4.8d still contains a much richer internal engineering model.
- Therefore the declared canonical model and active runtime model may be split.
This patch must measure and document that split, not solve it.

PHASE 1 — INSPECT CURRENT WORKSPACE
Inspect the actual local workspace first. Do not trust old patch notes.

Report:
1. current branch
2. HEAD commit
3. repository root
4. dirty/uncommitted state if available
5. package manager
6. build/dev commands
7. actual application entry point
8. actual route/component rendering ISO
9. actual ISO engine
10. actual renderer

Trace:
App
-> unified shell/router
-> ISO route
-> PdiIsometricEditor
-> active ISO engine
-> rendering surface

PHASE 2 — IDENTIFY ACTIVE RUNTIME MODEL
Locate the authoritative runtime storage for:
- nodes
- pipe segments
- fittings
- equipment
- ports
- topology
- joints/welds
- dimensions
- annotations
- layers
- X/Y/Z
- selection
- viewport
- BOM
- persistence

For each item report:
- exact file
- symbol/function/class
- caller
- data direction
- canonical / legacy / duplicated / unknown

PHASE 3 — COMPARE THE TWO MODEL WORLDS
Compare:
A) src/pdi/model/index.ts and consumers
B) active V4.8d internal model

Create a table:
Concern | Canonical model | V4.8d runtime | Actual source of truth | Risk

Concerns:
node, segment, fitting, equipment, port, topology, weld,
dimension, annotation, layer, X, Y, Z, selection, viewport,
BOM, persistence, JSON serialization.

DO NOT merge them yet.

PHASE 4 — FIND DUPLICATES
Search for duplicate implementations of:
- screenToWorld
- worldToScreen
- snapping
- selection
- insertion
- topology
- weld numbering
- BOM calculation
- dimensions
- save/load
- model serialization
- ISO workspace
- home navigation

Classify each:
CANONICAL / LEGACY / ACTIVE BUT DUPLICATED / UNUSED / UNKNOWN

Do not delete anything.

PHASE 5 — COORDINATE DIAGNOSTIC
The user reported pointer positions appearing away from the click.

Trace:
pointer event
-> DOM coordinates
-> viewport coordinates
-> model coordinates
-> snap coordinates
-> stored coordinates
-> rendering coordinates

Inspect all:
- getBoundingClientRect
- clientX/clientY
- offsetX/offsetY
- CSS transform
- translate
- scale
- canvas/SVG transforms
- zoom
- pan

Do NOT modify them.
Document the single transformation that should become canonical.

PHASE 6 — LIBRARY / ENGINEERING FLOW
Locate the real current flow for:
library selection
-> placement
-> insertion
-> ports
-> topology
-> weld W00x
-> BOM
-> selection
-> render
-> save

Also locate:
- double-click insertion
- drag/drop insertion
- rotation
- Z/elevation handling
- property panel
- dimensions

Do not repair yet.

PHASE 7 — SAFETY
Do not:
- switch branches silently
- cherry-pick
- merge
- rebase
- delete files
- rename production files
- replace V4.8d
- replace the active model
- modify Firestore rules
- modify GitHub

If local workspace differs from main, report it.

PHASE 8 — CREATE ONLY DOCUMENTATION
Create locally:
docs/architecture/PD_I_SOURCE_OF_TRUTH.md
docs/architecture/PD_I_RUNTIME_MAP.json

These are diagnostic artifacts only.

The Markdown must contain:
- branch
- entry point
- active ISO editor
- active engine
- renderer
- runtime model
- viewport
- selection
- snap
- library
- topology
- weld
- BOM
- dimensions
- persistence
- JSON serializer
- router/home

The JSON must represent the same map without inventing unknown values.

PHASE 9 — ACCEPTANCE
The patch is successful only if AI Studio can answer:
1. Which branch is being compiled?
2. Which component renders ISO?
3. Which engine renders ISO?
4. Which model stores real piping objects?
5. Which model is serialized?
6. Where does insertion happen?
7. Where are ports created?
8. Where is topology updated?
9. Where are W00x welds generated?
10. Where is selection stored?
11. Where is snap calculated?
12. Where is screen->world calculated?
13. Where are X/Y/Z stored?
14. Where are dimensions stored?
15. Where is BOM calculated?
16. Which code is legacy?
17. Which code is active?
18. Which code is duplicated?
19. What is the authoritative Source of Truth?

If unknown, write UNKNOWN. Never guess.

FINAL REPORT
Produce:
A. Source of Truth Report
B. Architecture Conflict Report
C. Coordinate Report
D. Actual ISO Business Flow
E. Smallest SAFE next patch recommendation

STRICT RULE
DO NOT FIX ANYTHING IN PATCH 001.
This patch establishes facts only.
The next patch will be based on this report and will repair the highest-risk
architectural issue without breaking V4.8d.
