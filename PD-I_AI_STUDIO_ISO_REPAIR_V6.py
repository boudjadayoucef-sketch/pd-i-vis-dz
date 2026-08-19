PD-I — AI STUDIO ISO REPAIR V6

AI STUDIO ONLY. Do not modify GitHub or piping-design-skill.
Inspect the CURRENT local workspace before editing. Preserve V4.8d and all V4/V5 repairs.

PURPOSE: repair the current ISO business logic and ergonomics shown in the latest screenshot.

1. LAYOUT / OLD HORIZONTAL BARS
The screenshot proves the previous migration is incomplete:
- workspace horizontal toolbars still consume drawing space
- BOM & Métré is still at the top
- bottom metric cards still exist

Keep the global application navigation if it is genuinely global, but remove/restructure
obsolete ISO workspace-specific horizontal toolbars. Do not duplicate controls.
The drawing viewport must gain space.

Target:
MAIN DRAWING | RIGHT COLLAPSIBLE VERTICAL BAR

Right bar sections:
Selection | Properties | BOM/Métré | Dimensions | Layers | Snap | Details

2. BOM / MÉTRÉ
Move BOM & Métré completely into the right vertical bar.
No duplicate BOM/Métré button above the drawing.
Do not delete the underlying BOM/calculation model.

3. REMOVE BOTTOM CARDS
Remove persistent bottom cards for:
- MÉTRÉ TUBE
- POIDS ACIER
- VOL. ÉPREUVE
- ÉPREUVE
Keep their underlying calculations. Show useful values in right-bar
BOM/Métré or Properties/Details. Never fabricate weight.

4. SELECTION IS BROKEN
The Selection tool must hit-test ALL real model entities:
nodes, pipes, elbows, tees, valves, reducers, flanges, library components,
dimensions and annotations where selectable.

Selection must use the SAME screen/model transform as rendering, snapping and
insertion. Click -> real model entity selected -> visible highlight.
Inserted library objects MUST become selectable.

Support:
click, hover, Shift+click where compatible, rectangle/marquee selection, Escape,
Delete, Move, Copy, Cut, Duplicate, Rotate.
All model mutations must be undoable.

5. LIBRARY INSERTION — RESTORE PREVIOUS BUSINESS WORKFLOW
This is the highest priority business repair.

Previous expected behavior:
select/target pipe -> choose library component -> component automatically inserts
INTO the tube/segment -> ports connect -> topology updates -> welds W00x are
created/calculated -> BOM/Métré updates -> component is selectable.

Restore for the COMPLETE compatible library, including:
valve, elbow, tee, reducer, flange and every existing compatible component.

Do NOT create floating decorative symbols.
Find and reuse the existing V4.8d insertion/topology functions if they still exist.

DOUBLE CLICK:
1 select pipe segment
2 double-click compatible library component
3 determine valid insertion point
4 snap to segment
5 orient to pipe/ISO direction
6 split/update pipe as existing business rules require
7 connect ports
8 update topology
9 generate/update welds
10 update BOM/Métré
11 make inserted object selectable

DRAG & DROP:
library component -> drag -> pipe segment -> preview -> validate -> drop ->
canonical insertion -> ports/topology -> welds -> BOM.
No model mutation before accepted drop. Preserve X/Y/Z.

6. WELDS
Restore existing weld generation/counting logic.
Use the project's existing W00... numbering convention if present; do not invent
a conflicting convention.
Welds must remain consistent on insert, delete, undo/redo and save/reload.
BOM/Métré updates after insertion.

7. Z / ELEVATION
Never flatten inserted components to Z=0.
Use the existing authoritative Z/elevation representation.
Properties must show X/Y/Z and elevation where available.

8. MAC TRACKPAD
Chrome/macOS two-finger scrolling over the ISO drawing must pan the viewport.
Investigate wheel handling, passive listeners, preventDefault, overflow CSS,
pointer-events, nested containers and React event handling.
Do not break mouse wheel, pinch zoom, selection or drag/drop.
Do not hijack page scrolling outside the ISO viewport.
Test vertical and horizontal two-finger pan and selection after pan.

9. RIGHT TOOL BAR
Use semantic symbols, not letters:
node/point, circle, pipe line, elbow bend, tee T, valve symbol, reducer,
flange, dimension arrows, note, select pointer, pan hand.
Keep tooltips/accessibility labels.
Fix dark opaque pills/pastilles that cover icons/text; inspect CSS/z-index/
pseudo-elements before changing markup.

10. RIGHT BAR
Collapsed = narrow icon rail. Expanded = contextual details.
When one object selected: Properties/Details show that model entity.
When multiple selected: show count/common properties/group actions.
Do not create a second engineering model.
Prefer overlay/controlled width so the drawing remains practical.

11. ROTATION
R rotates selected/active real model entity using the project's existing
rotation convention; inspect it first, do not guess.
Rotation updates orientation/ports, preserves connectivity where possible,
is undoable, and is exposed in menus/shortcut help. Avoid shortcut conflicts.

12. DIMENSIONS
Dimensions are still not visible. Audit tool registration, model data,
renderer, layer visibility, z-order, clipping, scale, contrast and text size.
Minimum: select first reference -> second -> preview -> commit -> visible,
selectable/editable where supported -> save/reload.
Support linear/horizontal/vertical, aligned if supported. Never fake static labels.

13. SNAP
Keep fine snap from V5. Separate screen-pixel tolerance from model-unit
tolerance, grid spacing and zoom. Make it viewport-aware and configurable.
Allow precision below 0.25 model units when the coordinate system permits.
Support grid/endpoint/port/midpoint/intersection/axis and visible feedback.
Never add arbitrary coordinate offsets.

14. POINTER/TRANSFORM INVARIANT
Pointer, selection, snapping, drag preview, drop, insertion, grid and rendering
must share one consistent screen<->viewport<->model transform.
Test after zoom, pan, resize and right-bar open/close.

15. ERGONOMIC AUDIT
Test normal and small Chrome windows, 100% and 200%+ zoom, right bar collapsed/
expanded. Verify no overlap, clipping, redundant toolbars, hidden labels,
bottom cards or dark overlays. Drawing gets maximum practical space.

16. ACCEPTANCE TEST
- ISO has full drawing area
- no obsolete ISO horizontal workspace bars
- BOM/Métré only in right bar
- bottom cards gone
- click selects pipe/fittings/library objects
- right-click Properties works
- double-click valve/elbow/tee/reducer/flange inserts into selected pipe
- drag/drop inserts into valid pipe
- ports/topology update
- weld count/IDs update
- inserted objects selectable
- marquee select works
- move/delete/copy/duplicate/cut work and undo/redo
- R rotates
- Z/elevation preserved
- dimensions visible
- fine snap works
- Mac two-finger pan works
- ISO -> Home hides Retour Accueil on Home
- Home -> ISO restores ISO controls

17. DEVELOPMENT ORDER
1 audit current workspace
2 remove old horizontal ISO toolbars / move BOM
3 remove bottom cards
4 repair selection
5 restore canonical library insertion
6 restore weld generation/BOM update
7 drag/drop
8 Mac trackpad
9 rotation R
10 dimensions
11 fine snap
12 full V4/V5 regression test
13 typecheck/lint/tests/build

18. REQUIRED REPORT
AUDIT: files, current implementation, root causes
REPAIR: files changed, business logic restored
VALIDATION: typecheck, lint, tests, build, manual browser test
BUSINESS: valve/elbow/tee/reducer/flange, welds, BOM, selection, multi-select, R, Z, dimensions
MAC: two-finger vertical/horizontal pan, zoom, selection after pan
REMAINING REGRESSIONS: exact list only

Do not claim completion while insertion, topology, weld generation, selection or
trackpad navigation remains broken.
