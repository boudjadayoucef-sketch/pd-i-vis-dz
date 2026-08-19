PD&I — PATCH 002
INTERACTION / COORDINATE CONTRACT + V4.8d PROTECTION

AI STUDIO ONLY — LOCAL WORKSPACE.
DO NOT MODIFY GITHUB DIRECTLY.
DO NOT MODIFY piping-design-skill.
DO NOT MERGE / REBASE / CHERRY-PICK.
DO NOT REPLACE V4.8d.
DO NOT REPLACE THE ACTIVE ENGINEERING MODEL.
DO NOT REBUILD EXISTING BUSINESS LOGIC FROM SCRATCH.

MISSION
Patch 001 established that the active Source of Truth is:
src/pdi/isometric/engine/IsometrieModuleV48d.tsx

Patch 002 stabilizes the interaction contract without architectural migration.

The protected chains are:

POINTER → SCREEN → SVG VIEWBOX → ISO WORLD → SNAP → MODEL

LIBRARY INSERTION → MODEL ENTITY → SELECTION

TRACKPAD → VIEWPORT PAN / ZOOM

PHASE 0 — INSPECT FIRST
Read the current versions of:
- src/pdi/isometric/engine/IsometrieModuleV48d.tsx
- src/pdi/isometric/PdiIsometricEditor.tsx
- src/pdiIsoUxRuntimePatch.js
- docs/architecture/PD_I_SOURCE_OF_TRUTH.md
- docs/architecture/PD_I_RUNTIME_MAP.json

Locate current implementations of:
getSvgCoordinates, isoUnprojectV4, isoProjectV4, snapIsoV4,
pointerDown, pointerMove, pointerUp, wheel/onWheel,
panX/panY, viewport zoom, insertEquipmentNode, insertTeeNode,
insertBendNode, dropEquipmentOnCanvas,
selectedNodeId, selectedNodeIds, selectedSegmentId,
selectedSegmentIds, selectedFitting, undo/redo.

Do not trust old line numbers.

PHASE 1 — SINGLE COORDINATE CONTRACT
Use ONE authoritative chain:
Pointer event
→ getSvgCoordinates(clientX, clientY, SVG)
→ SVG viewBox coordinates
→ isoUnprojectV4()
→ model world coordinates
→ snapIsoV4()
→ model mutation

Rendering remains:
model world coordinates
→ isoProjectV4()
→ SVG viewBox coordinates
→ SVG rendering

Do not introduce a second screen/world transform.
Do not add arbitrary offsets or magic constants.
Do not use fixed canvas dimensions as an engineering transform.
Selection, snapping, insertion and drawing must share the same transform.

PHASE 2 — POINTER OFFSET REGRESSION
Trace clientX/clientY → DOM/SVG transform → viewBox → isoUnprojectV4
→ snap → stored x/y/z → isoProjectV4 → rendered position.

Verify that clicking the visible projection of a world point recovers
that point within the engine's existing tolerance.

Test after:
- zoom
- pan
- sidebar collapsed/expanded
- browser resize
- trackpad pan
- mouse pan
- reset/recenter

Do not change geometry to compensate for UI transforms.

PHASE 3 — CSS / RUNTIME TRANSFORM SAFETY
Inspect:
- CSS transform/translate/scale
- nested transforms
- runtime DOM injections
- CSS zoom
- SVG/canvas transforms
- duplicated viewport offsets

SVG viewBox / CTM must remain the authoritative drawing coordinate system.
CSS may position the container but must not redefine engineering coordinates.

If src/pdiIsoUxRuntimePatch.js changes engineering coordinates, isolate only
that behavior. Preserve harmless layout behavior.

PHASE 4 — INSERTION → SELECTION
Keep canonical insertion functions:
insertEquipmentNode
insertTeeNode
insertBendNode
dropEquipmentOnCanvas
or their current equivalents.

After successful insertion:
real entity ID known
→ selectedNodeId or selectedNodeIds updated
→ visible highlight
→ Properties targets same entity
→ Move/Delete/Rotate target same entity.

Never select by screen coordinates or array index.
Use stable model IDs.
If insertion fails, do not leave a stale selected ID.

PHASE 5 — BUSINESS INVARIANTS
Do not rewrite topology/weld logic.

After successful elbow, tee, valve, reducer, flange and another existing
library component insertion verify:
1. parent segment remains valid
2. inserted object exists
3. ports exist
4. port orientation remains valid
5. canonical splitting remains
6. graph validation succeeds
7. weld derivation succeeds
8. W00x numbering remains canonical
9. BOM/Métré recalculates
10. inserted entity is selectable
11. undo restores previous graph
12. redo restores insertion

Reuse deriveProjectJoints() or the active equivalent.
Do not invent weld rules.

PHASE 6 — MAC TRACKPAD
Fix only interaction handling.

Mac:
- two-finger vertical scroll → pan Y
- two-finger horizontal scroll → pan X
- pinch zoom only if already supported by the event path

Mouse behavior must remain intact.

Use non-passive wheel handling only where necessary.
Do not prevent page scrolling outside the ISO viewport.
Do not break drag/drop or selection.
Do not create a second viewport state.

PHASE 7 — PAN / ZOOM INVARIANT
Pan, zoom, recenter and sidebar changes may change viewport/camera state,
but MUST NOT mutate node.x/y/z, segment geometry, fittings, topology or welds.

PHASE 8 — RIGHT SIDEBAR
Opening/closing the sidebar must not mutate engineering coordinates.
After open/close:
- selection remains on same entity
- hit testing remains aligned
- snap remains aligned

PHASE 9 — RESET / RECENTER
Keep the existing dynamic bounding-box resetView() if active.
Verify it changes camera only, preserves all model geometry and selection,
and does not introduce pointer offsets.

PHASE 10 — UNDO/REDO
Viewport-only actions (pan, zoom, sidebar, hover, selection) must NOT create
engineering undo entries.

Engineering mutations (insert, delete, move, rotate, split, dimension edit)
remain undoable. Do not rewrite the history engine.

PHASE 11 — VALIDATION
Run:
- npm run lint
- npx tsc --noEmit
- npm run build

Manual checks:
A) Coordinate: place → zoom → pan → click visible point → no offset.
B) Selection: insert valve → immediate selection → click → properties → delete/undo/redo.
C) Insertion: elbow, tee, valve, reducer, flange → ports/topology/weld/BOM.
D) Trackpad: vertical/horizontal pan → zoom → selection → insertion.
E) Sidebar: open/close → selection and coordinates unchanged.
F) Recenter: geometry unchanged.

PHASE 12 — REGRESSION GUARD
Compare before/after viewport-only actions:
- nodes
- segments
- fittings/equipment
- welds
- dimensions
- X/Y/Z

Viewport operations MUST produce zero engineering-model changes.

STRICT FILE RULE
Modify the smallest existing interaction code necessary.
Do not create a new ISO engine, model, topology engine, weld engine,
BOM engine or projection engine.
Do not duplicate existing functions.

If a behavior cannot be repaired safely without architectural refactoring,
STOP and report the exact blocker. Do not invent a parallel system.

FINAL REPORT
Return:
1. FILES CHANGED
2. EXACT FUNCTIONS CHANGED
3. COORDINATE CONTRACT RESULT
4. INSERTION → SELECTION RESULT
5. TOPOLOGY/WELD/BOM REGRESSION
6. TRACKPAD RESULT
7. PAN/ZOOM RESULT
8. SIDEBAR RESULT
9. UNDO/REDO RESULT
10. LINT RESULT
11. TYPESCRIPT RESULT
12. BUILD RESULT
13. REMAINING ISSUES

For remaining issues give exact file, symbol, behavior, root cause and safest next patch.

ABSOLUTE RULE:
PATCH 002 IS STABILIZATION ONLY.
Do not add product features.
Do not redesign architecture.
Do not replace V4.8d.
Do not migrate the canonical model yet.
Protect existing engineering behavior first.
