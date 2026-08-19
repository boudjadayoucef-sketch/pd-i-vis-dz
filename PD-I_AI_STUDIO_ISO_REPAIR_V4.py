"""
PD-I — AI STUDIO ISO REPAIR PATCH V4

REPAIR-FIRST PATCH
------------------
AI Studio is the ONLY environment that modifies and compiles PD-I.
Do NOT modify GitHub directly. Do NOT modify piping-design-skill.
The CURRENT LOCAL AI STUDIO WORKSPACE is the source of truth.

A file transfer appears to have corrupted/altered existing ISO business logic.
STOP adding new features until the regressions below are repaired.

REPORTED REGRESSIONS
--------------------
1. Mouse click position != created point position.
2. Tee no longer inserts/connects to pipe as before.
3. Valve no longer inserts/connects to pipe as before.
4. Elbow no longer inserts/connects to pipe as before.
5. Retour Accueil is missing.
6. Z/elevation disappeared.
7. Right-click -> List -> Properties is missing/incomplete.
8. Rectangle/marquee multi-selection is missing.
9. Multi-selection must support move, delete, copy, duplicate, cut.

============================================================
0. AUDIT BEFORE EDITING
============================================================

Inspect the CURRENT local workspace first.

Search for:
- PdiIsometricEditor
- V4.8d
- PdiIsometricModel
- IsoNode / IsoSegment
- pipe insertion/routing
- tee/valve/elbow insertion
- pointer/click handlers
- screen<->model/ISO transforms
- viewport, zoom, pan
- elevation/Z fields
- selection/context menu/properties
- Home routing/navigation
- copy/paste/duplicate/delete
- existing command/undo/redo code

For each relevant file record internally:
FILE / ROLE / CURRENT BEHAVIOR / EXPECTED BEHAVIOR / RISK / REPAIR.

Do not delete code during the audit.

============================================================
1. HIGHEST PRIORITY — POINTER / COORDINATE BUG
============================================================

The created point must appear exactly under the mouse.

Find the existing screen->model and model->screen pipeline. Do NOT add
arbitrary offsets.

Investigate:
- canvas/SVG boundingClientRect
- CSS scaling
- devicePixelRatio
- nested container offsets
- zoom applied twice
- pan applied twice
- stale viewport state
- wrong origin
- projection mismatch
- grid using a different transform

The renderer and pointer insertion must use the SAME viewport/projection.

Required invariant, within rendering tolerance:

    modelToScreen(screenToModel(mouse)) ~= mouse

Test at:
- center
- top-left
- bottom-right
- after zoom
- after pan
- after resize

Use temporary diagnostics only to find the root cause; remove/disable them
after repair.

============================================================
2. RESTORE EXISTING FITTING INSERTION
============================================================

Restore the PREVIOUS business behavior for:
- TEE
- VALVE
- ELBOW

Do NOT implement floating decorative symbols.

Expected:

user selects component
 -> targets pipe/port/segment
 -> snap detects valid target
 -> component orientation calculated
 -> component inserted into canonical model
 -> ports/topology updated
 -> rendering updates

TEE:
- connect to host pipe
- preserve/create branch port
- correct orientation
- update topology

VALVE:
- connect to pipe
- correct axis/flow orientation
- correct port connectivity

ELBOW:
- connect to endpoint/route
- correct ISO orientation
- preserve ports/connectivity

Find and reuse existing insertion/topology functions. Do not replace V4.8d
logic with a simplified implementation.

============================================================
3. RESTORE Z / ELEVATION
============================================================

Z/elevation is an engineering property and must be restored.

Inspect the existing/current model for:
z, elevation, startZ, endZ, node elevation, segment elevation,
coordinate fields and any prior representation.

Restore the SAME authoritative representation; do not create a parallel Z model.

Display where supported:

Node:
    X / Y / Z
    Elevation

Segment:
    Start X/Y/Z
    End X/Y/Z
    Length
    Elevation

Never invent missing values. Show Unknown / Not defined when unavailable.

Z/elevation must survive save/reload.

============================================================
4. RIGHT CLICK -> LIST -> PROPERTIES TABLE
============================================================

Required workflow:

RIGHT CLICK OBJECT
    -> LIST
    -> PROPERTIES
    -> PROPERTY TABLE

The Properties view must be a real table.

Example pipe rows:
    ID
    Type
    Line Number
    DN/NPS
    Spec
    Material
    Start X
    Start Y
    Start Z
    End X
    End Y
    End Z
    Length
    Elevation

Fitting rows may include:
    ID
    Type
    DN
    Rating/Class
    Angle
    Orientation
    Ports
    Connected elements
    X/Y/Z
    Dimensions
    Envelope

Rules:
- read from canonical model
- never fabricate values
- unknown = explicit Unknown/null
- update when selection changes
- edits, when allowed, must use model commands

============================================================
5. RECTANGLE / MARQUEE MULTI-SELECTION
============================================================

Implement CAD-style rectangular selection.

Mouse down in empty drawing area
 -> drag rectangle
 -> select all selectable model objects inside/intersecting the rectangle

Do not select:
- grid
- UI
- non-selectable construction objects

Support:
- click selection
- Shift+click add/remove where compatible
- rectangle selection
- Escape clear/cancel
- Delete

Selected objects need a consistent visual highlight.

Use real model entity IDs/references.

============================================================
6. MULTI-SELECTION OPERATIONS
============================================================

For real multi-selection support:
- MOVE
- DELETE
- COPY
- DUPLICATE
- CUT

Use model commands, not canvas pixels.

Preferred commands if architecture allows:
    MoveSelectionCommand
    DeleteSelectionCommand
    CopySelectionCommand
    DuplicateSelectionCommand
    CutSelectionCommand

All destructive operations must be undoable.

Copy/duplicate:
- preserve internal connectivity where appropriate
- generate new IDs
- never duplicate IDs
- do not mutate the original

Cut:
- copy to clipboard/command state
- remove originals through a model command
- undo restores originals

Inspect existing shortcuts before adding:
Ctrl/Cmd+C copy
Ctrl/Cmd+X cut
Ctrl/Cmd+V paste
Ctrl/Cmd+D duplicate
Delete delete
Ctrl/Cmd+Z undo
Ctrl/Cmd+Shift+Z redo

============================================================
7. RETOUR ACCUEIL
============================================================

Add a visible, working "Retour Accueil" button to ISO.

It must use the existing navigation/router architecture and return to the
existing Home page. Do not create a second Home page.

============================================================
8. GRID / VIEWPORT SAFETY
============================================================

The horizontal/vertical drafting grid must NOT alter engineering coordinates.

Grid, model rendering, snapping and pointer insertion must share the correct
viewport transform.

Fix the ROOT viewport/coordinate problem rather than compensating with offsets.

============================================================
9. V4.8d PROTECTION
============================================================

Treat existing V4.8d business logic as protected.

Before changing related code:
- locate current implementation
- inspect callers
- understand data flow
- preserve public behavior

Do not:
- rewrite the ISO engine
- replace the geometry engine
- remove topology logic
- create a parallel geometry model
- simplify fitting insertion into decorative placement

============================================================
10. REGRESSION TEST MATRIX
============================================================

A POINTER:
- click center/top-left/bottom-right
- after zoom
- after pan
- after resize

B PIPE:
- create/move/delete

C ELBOW:
- insert on pipe
- correct orientation
- connected ports

D TEE:
- insert on pipe
- correct branch
- connected topology

E VALVE:
- insert on pipe
- correct axis
- connected ports

F Z:
- create/edit/display elevation
- save/reload elevation

G PROPERTIES:
- right click
- List
- Properties
- table shows real values

H MULTISELECT:
- rectangle select
- move
- delete
- copy
- duplicate
- cut
- undo/redo

I NAVIGATION:
- ISO -> Retour Accueil
- Home -> ISO

============================================================
11. VALIDATION
============================================================

Run the project's actual:
- typecheck
- lint if configured
- tests if configured
- production build

Then inspect:
- browser console
- runtime errors
- pointer alignment
- fitting insertion
- Z/elevation
- property table
- marquee selection
- move/delete/copy/duplicate/cut
- Home navigation

Report exact commands/results.

============================================================
12. DO NOT CONTINUE NEW FEATURES
============================================================

Do NOT proceed to advanced catalogue work, AI vision, DXF or advanced
clearance until these core regressions are repaired.

============================================================
13. REQUIRED AI STUDIO REPORT
============================================================

REPAIR AUDIT
- files inspected
- regression root causes
- existing behavior found

REPAIRS
- files changed
- functions restored
- minimal new abstractions

VALIDATION
- typecheck
- lint
- tests
- build

MANUAL ISO TEST
- pointer
- elbow
- tee
- valve
- Z/elevation
- right-click/list/properties
- marquee multi-selection
- move/delete/copy/duplicate/cut
- Retour Accueil

REMAINING ISSUES
- exact list only

Do not claim completion while any reported core regression remains.
"""

PATCH_META = {
    "name": "PD-I AI Studio ISO Repair V4",
    "mode": "repair-first",
    "source_of_truth": "AI Studio local workspace",
    "github_direct_modification": False,
    "piping_design_skill_modification": False,
    "preserve_v48d": True,
}
