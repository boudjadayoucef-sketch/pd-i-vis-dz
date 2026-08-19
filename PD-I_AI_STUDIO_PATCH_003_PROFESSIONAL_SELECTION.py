PD&I — PATCH 003 — PROFESSIONAL SELECTION

AI STUDIO ONLY — LOCAL WORKSPACE
DO NOT MODIFY GITHUB DIRECTLY.
DO NOT MODIFY piping-design-skill.
DO NOT MERGE / REBASE / CHERRY-PICK.
DO NOT REPLACE V4.8d.
DO NOT CREATE A SECOND MODEL, PROJECTION, TOPOLOGY, WELD OR BOM ENGINE.

MISSION
-------
Stabilize professional CAD-style selection using the existing V4.8d model
and selection states. This is an interaction patch, not an architecture
migration.

SOURCE OF TRUTH
---------------
src/pdi/isometric/engine/IsometrieModuleV48d.tsx

Active editor:
src/pdi/isometric/PdiIsometricEditor.tsx

Existing selection state previously identified:
- selectedNodeId
- selectedNodeIds
- selectedSegmentId
- selectedSegmentIds
- selectedFitting
- selectedDimensionId

FIRST inspect the actual current files and usages. Do not rely on old line
numbers or assumptions.

REQUIRED SELECTION
------------------
1. Single click:
   - node → select node
   - pipe segment → select segment
   - fitting/equipment → select real model entity
   - dimension → select dimension if safely supported
   - empty canvas → clear selection

2. Shift+click:
   - add unselected entity
   - remove already selected entity
   - preserve unrelated selections

3. Rectangle/window selection:
   - mouse drag on empty workspace
   - temporary visual rectangle only
   - on release select eligible real model IDs
   - MUST use the same coordinate/projection contract stabilized in Patch 002
   - MUST NOT modify engineering geometry

4. Drag-vs-click:
   - small movement threshold distinguishes click from rectangle
   - dragging a selected entity must continue using existing move behavior
   - do not steal entity dragging for rectangle selection

5. Selection mode:
   - reuse existing selection tool if present
   - do not create a second selection mode
   - ESC cancels transient rectangle interaction

MODEL IDS ONLY
--------------
Never select by screen coordinate, SVG child index, array index or visual
approximation. Use stable model IDs.

Keep node IDs, segment IDs, fittings and dimensions type-safe according to
the existing architecture. Do not invent a generic parallel selection model.

RECTANGLE RULE
--------------
Prefer:
- node/fitting: projected anchor/center inside rectangle
- segment: projected geometry intersects/contained by rectangle
- dimension: only if current implementation supports safe hit testing

If left-to-right / right-to-left CAD semantics can be added safely:
- left→right = fully contained
- right→left = intersecting

If that is risky, implement deterministic intersection/containment first
and report the limitation.

COORDINATE SAFETY
-----------------
Reuse the Patch 002 chain:
Pointer
→ getSvgCoordinates()
→ SVG viewBox
→ isoUnprojectV4()/existing projection helpers
→ snapIsoV4() where appropriate
→ model

For rectangle hit testing, projected geometry may be preferable; do not
invent a second screen/world transform.

Selection-only operations MUST NOT change:
- node x/y/z
- segment geometry
- ports
- topology
- welds
- BOM
- dimensions

PROPERTIES
----------
After single selection, the existing right sidebar Properties must show
the same real selected object.

After multi-selection, show a safe multi-selection state/summary.
Never display stale properties from a previously selected object.

SIDEBAR / TRACKPAD
------------------
Selection must work with the right sidebar open or closed.
Do not reintroduce old horizontal BOM/Métré UI.

Do not regress Patch 002:
- two-finger Mac trackpad pan
- pinch/mouse zoom
- selection after pan/zoom

OPERATIONS
----------
Reuse existing handlers for:
- Move
- Delete
- Copy
- Duplicate
- Cut
- Rotate R

Do not rewrite topology or business logic inside selection.

If group movement is already supported safely, selection must feed it.
If it is not, do NOT rewrite the move/topology engine in this patch.
Report group movement as deferred.

For multi-selection, only enable group rotation if the current architecture
already has a safe path. Otherwise preserve single-object R and report that
group rotation is deferred.

UNDO / REDO
-----------
Selection and rectangle selection create NO engineering history entries.

Engineering operations remain undoable:
- move
- delete
- copy/duplicate
- cut
- rotation
- dimension edits

TOPOLOGY PROTECTION
-------------------
If an engineering operation follows selection, use the existing canonical
mutation path (for example commitGraph/current equivalent).

Do not directly mutate graph data from the selection layer.

After fitting/equipment selection and operations verify:
- ports
- topology
- W00x weld generation
- BOM/Métré
- X/Y/Z
remain valid.

TEST MATRIX
-----------
A. Single node: click → highlight → Properties → correct model ID.
B. Single pipe: click → segment selection → Properties.
C. Shift: select A → Shift+B → both → Shift+B → only A.
D. Rectangle: select several entities → expected IDs → no geometry change.
E. Rectangle after zoom/pan: alignment remains exact.
F. Insert valve: immediate selection → rectangle can select it → Properties.
G. Move: test existing multi-move if available; verify topology/X/Y/Z/weld/BOM.
H. Delete/Undo/Redo.
I. R rotation on fitting; selection remains valid.
J. Sidebar open/close; no coordinate offset.
K. Trackpad pan/zoom then selection and rectangle selection.

VALIDATION
----------
Run:
npx tsc --noEmit
npm run lint
npm run build

All must pass before claiming completion.

REGRESSION CHECK
----------------
For selection-only actions compare before/after:
nodes, segments, X/Y/Z, ports, topology, welds, dimensions, BOM.
Expected: ZERO engineering-model changes.

FILE SCOPE
----------
Inspect first. Prefer the smallest number of files.
Likely active file:
src/pdi/isometric/engine/IsometrieModuleV48d.tsx

Modify other files only if inspection proves necessary.

Do NOT create:
- SelectionEngine.ts
- SelectionModel.ts
- second coordinate system
- second graph/model
unless absolutely required by the existing architecture; if so STOP and
report before proceeding.

STOP CONDITIONS
---------------
Stop and report instead of improvising if:
- selection is duplicated in another component
- group movement requires topology rewrite
- rectangle selection cannot safely use current projection
- runtime patch conflicts with selection
- fix would alter V4.8d business rules
- a new model or projection engine would be required.

FINAL REPORT
------------
Return:
1. Files changed
2. Functions/symbols changed
3. Single selection
4. Shift multi-selection
5. Rectangle selection
6. Selection after zoom/pan
7. Properties
8. Move/Delete/Copy/Duplicate/Cut
9. Rotation R
10. Trackpad
11. Undo/Redo
12. Topology regression
13. W00x regression
14. BOM/Métré regression
15. X/Y/Z regression
16. TypeScript
17. Lint
18. Build
19. Remaining issues
20. Recommended Patch 004

For every remaining issue give:
file, symbol/function, observed behavior, root cause, safest next patch.

FINAL RULE
----------
Patch 003 is ONLY professional selection stabilization.
Do not redesign PD&I.
Do not replace V4.8d.
Do not migrate the canonical model.
Do not touch GitHub.
Protect the existing engineering model first.
