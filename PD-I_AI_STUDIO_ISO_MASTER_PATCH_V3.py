"""
PD-I — AI STUDIO MASTER PATCH V3

Use this file as the SINGLE master brief for the current PD-I workspace.

IMPORTANT WORKFLOW:
- AI Studio is the ONLY environment that applies code changes and compiles/tests.
- Do NOT modify GitHub directly.
- Do NOT create a second PD-I implementation.
- Do NOT modify piping-design-skill during this ISO maturation phase.
- The AI Studio LOCAL WORKSPACE is the source of truth.
- GitHub is reference/audit only.
- Before every change, inspect the CURRENT files, imports, consumers and source of truth.
- Preserve the existing ISO V4.8d engine. Do not rewrite or replace it.

PRODUCT GOAL
------------
Mature PD-I ISO into a professional piping-isometric drafting environment BEFORE
connecting AI vision/reconstruction.

The user must be able to:
create/open project, create/open ISO, configure sheet, draw piping, connect
components, snap, edit properties, dimension, annotate, manage layers,
undo/redo, validate, save/reload, prepare title block, preview and export.

CURRENT TECHNICAL CONTEXT
-------------------------
Historically observed:
- React + TypeScript + Vite
- Tailwind CSS
- lucide-react
- existing PdiIsometricEditor / V4.8d family
- existing PdiIsometricModel and ISO node/segment structures

BUT AI STUDIO MUST inspect package.json and the actual local tree first.
Do not assume paths or branch names are unchanged.

NON-NEGOTIABLE RULES
--------------------
1. Canonical piping/ISO model is the source of truth.
2. React state must not become a second engineering model.
3. Geometry is deterministic.
4. AI must never invent exact lengths, coordinates, angles, elevations,
   clearances or component dimensions.
5. Do not rewrite the V4.8d engine.
6. Do not introduce a second canvas/geometry engine.
7. Prefer small, reversible patches.
8. Do not modify unrelated modules.
9. No fake buttons/features.
10. After each coherent patch: typecheck, lint if configured, tests, build,
    and inspect runtime/console errors.
11. Report failures honestly.

IMMEDIATE PATCH PRIORITY
------------------------
Implement and stabilize in this order:
    1. Horizontal/vertical drafting grid
    2. Real selection + hover
    3. Right-click context menu
    4. Real Properties panel bound to selected model entity
    5. Command-based Undo/Redo
    6. Professional snapping

1 — GRID
--------
Replace any defective work-plane grid with a clean 2D drafting grid:

    |       |       |       |
    +-------+-------+-------+
    |       |       |       |
    +-------+-------+-------+
    |       |       |       |

Requirements:
- vertical lines
- horizontal lines
- consistent spacing
- zoom/pan aware
- visually subordinate to piping
- no pointer-event interception
- toggleable
- crisp while zooming
- prepared for snapping
- does not mutate the canonical model

Design settings for future:
- major/minor spacing
- grid origin
- visible
- snap enabled
- snap spacing

The grid is a drafting reference, not automatically an engineering coordinate
system.

2 — SELECTION
-------------
Implement real model-backed selection:
- click selection
- hover highlight
- selected highlight
- multi-selection where supported
- box selection if compatible
- Escape cancels/clears
- Delete through a model command
- selection references real model IDs/entities

3 — RIGHT CLICK / PROPERTIES
----------------------------
Right-click an ISO object:

    Properties
    Select
    Hide/Show (if supported)
    Delete
    Cancel

Properties MUST be bound to the actual selected model entity.

For a pipe, expose where available:
- id
- line number
- DN/NPS
- spec
- material
- start/end
- length
- elevation

For elbow:
- id
- type
- DN
- angle
- radius/class
- connected ports

For valve:
- id
- type
- DN
- rating/class
- orientation
- connected ports

Never invent missing values. Use null/unknown/unavailable explicitly.

4 — UNDO / REDO
---------------
Use or create a command architecture:

    command.execute()
    command.undo()
    command.description

Examples:
AddPipeCommand
DeleteObjectCommand
MoveObjectCommand
UpdatePropertyCommand
AddDimensionCommand
DeleteDimensionCommand

Undo/redo must restore the canonical model exactly.

Shortcuts:
Ctrl/Cmd+Z
Ctrl/Cmd+Shift+Z

5 — SNAPPING
------------
Create a dedicated snapping service/utility.

Targets:
GRID
ENDPOINT
PORT
MIDPOINT
INTERSECTION
AXIS

Requirements:
- visible feedback
- deterministic priority
- configurable enable/disable
- viewport-scale-aware tolerance
- no accidental mutation

Suggested priority:
PORT > ENDPOINT > INTERSECTION > MIDPOINT > AXIS > GRID

Inspect existing behavior before implementing.

6 — PROFESSIONAL DRAWING TOOLS
------------------------------
Mature progressively:
Select, Pan, Pipe, Elbow, Tee, Reducer, Flange, Valve,
Dimension, Leader, Note, Weld, Measure.

Never expose a tool that only looks functional.

7 — DIMENSIONS
--------------
Dimensions are core model data, not decoration.

Progressively support:
- linear
- horizontal
- vertical
- aligned
- angle where appropriate
- text editing
- movement
- style
- units
- precision
- extension/witness lines

Persist dimensions in the drawing/document model.
Do not flatten them into pixels.

8 — ANNOTATIONS
---------------
Support:
- line number
- component tag
- notes
- leaders
- weld markers
- flow direction
- service information
- revision notes

Annotations must be document/model data.

9 — LAYERS
----------
Real layers, for example:
PIPE, FITTINGS, VALVES, DIMENSIONS, ANNOTATIONS, WELDS,
EQUIPMENT, GRID, CONSTRUCTION, TITLE_BLOCK.

Support visibility, active layer and optional lock/filtering.
Do not duplicate geometry per layer.

10 — SHEET / CARTOUCHE
----------------------
Support progressively:
A4, A3, A2, A1.

Metadata:
project, client, drawing number, title, revision, date,
drawn by, checked by, approved by, scale, units.

Title block is persistent data.
Preview/export must use the same sheet model.

11 — TROUVAY & CAUVIN / INDUSTRIAL COMPONENT LIBRARY
-----------------------------------------------------
Strategic requirement: create a PARAMETRIC component library, not decorative
symbols.

A component definition should eventually contain:
- manufacturer/source
- catalogue reference
- component type
- DN/NPS
- rating/class
- material
- dimensions
- connection types
- port definitions
- orientation rules
- ISO representation
- bounding/envelope dimensions
- mass where available
- evidence/source
- revision/version

Only use dimensions explicitly available from a trusted source.
Never fabricate catalogue data.

Architecture target:

ComponentDefinition
    metadata
    ports
    dimensions
    envelope
    isoRepresentation
    source

The library must be independent from the renderer and allow multiple suppliers.

12 — DIMENSIONS + ENCOMBREMENT / CLEARANCE
------------------------------------------
For parametric components, prepare:
- nominal dimensions
- connection positions
- overall envelope/bounding box
- required installation clearance where known

Then deterministic checks can detect:
- collision
- overlap
- insufficient clearance
- impossible connection
- invalid orientation

Never call a visual approximation an engineering clearance.

13 — QA
-------
Deterministic checks:
- disconnected ports
- dangling ends
- invalid connections
- duplicate IDs
- missing required properties
- invalid orientation
- invalid dimensions
- overlaps/collisions
- missing title block data
- export readiness

Severity:
INFO / WARNING / ERROR

Return structured QA results.

14 — SAVE / RELOAD
------------------
Persist:
- model
- dimensions
- annotations
- layers
- sheet
- revision
- metadata
- viewport only if appropriate

Support dirty-state detection.
Never save only a screenshot.

15 — EXPORT
-----------
Order:
SVG -> PDF -> DXF

Exports derive from canonical document/model.
Never use a screenshot as engineering source.

16 — HOME / NAVIGATION
----------------------
Add a clear "Retour Accueil" action in ISO.
Apply the same navigation principle to all modules.

The Home page is a hub:
    Projects
    ISO
    CAD / JSON
    AI
    Settings

Do not reproduce every module toolbar on Home.

17 — HOME PAGE CLEANUP
----------------------
Audit and remove:
- overlapping controls
- duplicated functions
- excessive cards
- competing navigation
- unclear hierarchy
- fake/duplicate actions

Home launches workspaces; workspaces contain their own tools.

18 — 8-PHASE ROADMAP
--------------------
PHASE 1: interaction foundation
selection, hover, pan/zoom, fit, shortcuts, Escape, delete, undo/redo

PHASE 2: grid and snapping
horizontal/vertical grid, zoom-aware rendering, grid settings,
grid snapping, endpoint/port/intersection snapping

PHASE 3: professional drawing
pipe, elbow, tee, reducer, flange, valve, connect, edit, move, rotate

PHASE 4: dimensions and annotations
dimensions, leaders, tags, notes, welds, line/service information

PHASE 5: components and sheet
parametric library, trusted source metadata, real dimensions, envelopes,
layers, title block, revisions

PHASE 6: QA and engineering checks
connectivity, collisions, clearances, required metadata, export readiness

PHASE 7: persistence and export
JSON document, save/reload, SVG, PDF, DXF

PHASE 8: AI readiness
stable canonical model, component library, geometry, evidence/source metadata,
QA; only then connect piping-design-skill

19 — PROFESSIONAL ACCEPTANCE TEST
---------------------------------
AI Studio must eventually verify:
1. Open PD-I
2. Go to ISO
3. See clean professional workspace
4. Toggle horizontal/vertical grid
5. Zoom/pan
6. Create pipe
7. Snap endpoint
8. Add elbow
9. Add tee
10. Add valve
11. Connect components
12. Select object
13. Right-click
14. Open Properties
15. Modify valid property
16. Undo
17. Redo
18. Add dimensions
19. Add line number/tag
20. Toggle layers
21. Run QA
22. Configure title block
23. Save
24. Reload
25. Verify identical model
26. Preview
27. Export SVG/PDF when implemented

No step may depend on fake UI state.

20 — EXACT DEVELOPMENT ORDER
----------------------------
STEP 0: audit local workspace and produce a file map.
STEP 1: audit current ISO editor, model, workspace, routing, grid and Home.
STEP 2: fix horizontal/vertical grid.
STEP 3: create/clean viewport/grid abstraction.
STEP 4: real selection/hover.
STEP 5: right-click context menu.
STEP 6: real Properties binding.
STEP 7: command Undo/Redo.
STEP 8: snapping service.
STEP 9: pipe/fitting manipulation.
STEP 10: persistent dimensions.
STEP 11: annotations.
STEP 12: layers.
STEP 13: Home navigation.
STEP 14: Home hierarchy cleanup.
STEP 15: parametric component-library interfaces.
STEP 16: trusted catalogue/source model.
STEP 17: dimensions/envelopes/clearance.
STEP 18: deterministic QA.
STEP 19: sheet/title block/revision.
STEP 20: persistence/reload.
STEP 21: SVG/PDF.
STEP 22: DXF.
STEP 23: final regression.
STEP 24: only then prepare piping-design-skill integration.

21 — AI STUDIO OPERATING FORMAT
-------------------------------
For every task report:

AUDIT
- files inspected
- current implementation
- source of truth
- risks

PATCH
- files changed
- exact reason
- compatibility impact

VALIDATION
- typecheck
- lint
- tests
- build
- runtime/console check

RESULT
- implemented
- pending
- regressions

Never claim success without validation.

22 — FUTURE AI VISION
---------------------
Future pipeline:

PHOTO / P&ID
    -> Vision
    -> Observation
    -> Topology
    -> Reconstruction
    -> Canonical Piping Model
    -> PD-I ISO

The future AI must rely on:
- real component definitions
- real ports
- real dimensions
- real envelopes
- real connectivity
- evidence/confidence

This is why current ISO geometry and component data must be real,
parametric and deterministic.

FINAL INSTRUCTION
-----------------
Start by inspecting the CURRENT LOCAL AI STUDIO WORKSPACE.

Do NOT assume branch names, paths, component names or file contents from this
brief are still correct.

Do NOT modify GitHub.
Do NOT modify piping-design-skill.
Do NOT create a second PD-I implementation.
Preserve V4.8d.

Apply the smallest safe patch for the CURRENT step only.
Compile and test it.
Fix regressions before moving forward.

Immediate priority:
GRID -> SELECTION -> RIGHT CLICK -> PROPERTIES -> UNDO/REDO -> SNAPPING

Then continue through the roadmap.
"""

PATCH_META = {
    "name": "PD-I AI Studio ISO Master Patch V3",
    "source_of_truth": "AI Studio local workspace",
    "github_direct_modification": False,
    "piping_design_skill_modification": False,
    "preserve_v48d": True,
    "priority": [
        "grid",
        "selection",
        "right_click_properties",
        "undo_redo",
        "snapping",
    ],
}

if __name__ == "__main__":
    print(__doc__)
