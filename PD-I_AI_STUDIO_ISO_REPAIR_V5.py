PD-I — AI STUDIO ISO REPAIR / UX PATCH V5

AI STUDIO ONLY:
- Modify/compile only the current local AI Studio workspace.
- Do not modify GitHub directly.
- Do not modify piping-design-skill.
- Inspect current files before every change.
- Preserve V4.8d and all V4 repairs.

PURPOSE
-------
Fix the current ISO UX issues without breaking business logic.

1) HOME BUTTON CONTEXT
----------------------
Bug: after returning Home, the ISO "Retour Accueil" button remains visible.

Required:
- ISO: show Retour Accueil.
- Home: hide it completely.
- Use the existing router/workspace state.
- Do not create a second Home page.

Acceptance:
ISO -> Home = no ISO button.
Home -> ISO = button visible again.

2) GRID FULL WORKSPACE
----------------------
The horizontal/vertical grid is currently too small.

Make it cover the ENTIRE drawing viewport dynamically:
- full available editor area
- resize with container/window
- correct after sidebar open/close
- correct after zoom/pan
- horizontal + vertical lines
- no hard-coded small rectangle
- no pointer-event interception
- same viewport transform as geometry

Do NOT fix coordinate errors with arbitrary offsets.

3) RECENTER / FIT
-----------------
Current top editor buttons reduce the useful drawing area.

Audit them. Recenter/Fit must change VIEWPORT only:
- never resize the model/drawing area as a side effect
- do not shrink the canvas
- keep the drawing workspace maximized

4) RIGHT COLLAPSIBLE DETAIL BAR
------------------------------
Create/use a vertical right-side collapsible detail bar.

Collapsed:
- narrow icon/handle.

Expanded:
- Properties
- BOM
- Selection
- Element details
- Dimensions
- Snap options
- Layer information where useful

Prefer overlay/floating or controlled width so the drawing remains usable.

Selected model entity drives contextual information.
No duplicate engineering model.

5) REMOVE USELESS BOTTOM DETAILS
---------------------------------
Remove the current bottom display of weight/length IF it is only redundant UI.
Do NOT delete underlying model data.

Move useful information to:
Right Detail Bar -> Properties / Element Information.

Never invent weight.

6) MOVE BOM / PROPERTIES
------------------------
Move the current BOM/Properties button from the top horizontal area into
the new right vertical bar.

Target:
Right Bar
  - Properties
  - BOM
  - Selection
  - Details

Avoid duplicate controls.

7) RIGHT PALETTE SYMBOLS
------------------------
Replace text letters in the vertical right tool palette with semantic icons.

Examples:
- Node: node/point-node symbol
- Point: circle
- Tube/Pipe: line/pipe icon
- Elbow: bent-line icon
- Tee: T-shaped line
- Valve: valve symbol
- Reducer: tapered pipe
- Flange: flange icon
- Dimension: dimension-line icon
- Note: annotation/text icon

Keep full tooltips and accessibility labels.
Do not use arbitrary decorative symbols.

8) PALETTE DARK OVERLAY
-----------------------
Buttons are covered by dark circular/pill overlays.

Inspect CSS, pseudo-elements, z-index and badge layers.
Fix so icon/text is clearly visible.
Keep useful active/hover state.
Do not remove accessibility/status indicators unnecessarily.

9) LIBRARY DOUBLE-CLICK INSERTION
---------------------------------
All compatible library components must support:

select pipe segment
 -> double-click library component
 -> insertion mode or immediate insertion
 -> snap to valid segment location
 -> orient to pipe/ISO axis
 -> update ports/topology
 -> canonical model

Must work for compatible:
tee, valve, elbow, reducer, flange and other existing library components.

Do NOT create disconnected decorative symbols.

10) LIBRARY DRAG & DROP
-----------------------
Support:
Library component -> drag -> ISO segment -> preview -> drop -> validate
-> insert/connect -> update topology.

During drag:
- preview
- valid/invalid target feedback
- no model mutation until accepted

On drop:
- use canonical insertion logic
- valid IDs
- connect ports
- preserve Z/elevation
- preserve existing geometry conventions

11) ROTATION — KEY R
--------------------
Implement/use a real model rotation command.

R = rotate selected/active element using the project's existing rotation
increment/convention. Inspect existing convention first; do not guess.

Rotation must:
- operate on real model entities
- preserve connectivity where possible
- update orientation/ports
- be undoable
- work during insertion when appropriate

Expose rotation in:
- context menus
- relevant tool menus
- shortcut help
- keyboard shortcut R

Do not conflict with existing shortcuts.

12) COTATIONS / DIMENSIONS
--------------------------
User reports cotations are not visible.

Audit:
- dimension tool registration
- dimension model
- renderer
- layer visibility
- z-order
- clipping
- scale/text size
- contrast
- creation interaction

Minimum:
- Dimension tool visible
- select first reference
- select second reference
- preview
- commit
- persistent visible dimension
- save/reload persistence

Support at minimum:
linear, horizontal, vertical; aligned if current engine supports it.

Do not fake dimensions as static labels.

13) SNAP BELOW 0.25
-------------------
Investigate current snap tolerance.

Do NOT blindly set an engineering tolerance of 0.25.
Separate:
- screen-pixel tolerance
- model-unit tolerance
- grid spacing
- zoom factor

Make snap tolerance configurable and viewport-scale aware, allowing precision
below 0.25 model units when the current coordinate system permits.

Expose where architecture permits:
- Snap enabled
- Snap tolerance
- Grid snap
- Endpoint snap
- Port snap
- Intersection snap
- Midpoint snap

Show snap feedback near cursor.
Never snap outside configured tolerance.
Do not alter canonical coordinates to make snapping look correct.

14) PRESERVE V4 REPAIRS
-----------------------
Before touching shared viewport/insertion functions, verify:
- pointer alignment
- tee insertion
- valve insertion
- elbow insertion
- Z/elevation
- right-click properties
- property table
- marquee selection
- multi-selection operations
- Retour Accueil

15) ACCEPTANCE TESTS
--------------------
HOME:
- ISO shows Retour Accueil
- Home does not

GRID:
- fills entire drawing area
- resize works
- zoom/pan works
- no clipping

VIEW:
- recenter/fit changes only view
- does not shrink workspace

RIGHT BAR:
- collapse/expand
- Properties
- BOM
- details
- drawing remains usable

PALETTE:
- semantic symbols visible
- no dark overlay hiding icons
- tooltips work

INSERTION:
- double-click library component on segment
- drag/drop onto segment
- tee/valve/elbow connect correctly
- reducer/flange compatible insertion
- topology valid
- Z preserved

ROTATION:
- R rotates selected/active object
- menu exposes rotation
- undo/redo works

DIMENSIONS:
- tool visible
- create dimension
- dimension visible
- dimension persists

SNAP:
- fine snap below 0.25 when coordinate system allows
- feedback visible
- no false snapping outside tolerance

16) VALIDATION
--------------
Run the project's actual:
- typecheck
- lint if configured
- tests
- build
Then browser/manual validation.

Report:
AUDIT
PATCH
VALIDATION
REGRESSIONS
REMAINING ISSUES

Do not claim completion if an acceptance test fails.

17) EXACT DEVELOPMENT ORDER
---------------------------
1. Audit workspace.
2. Fix Home context visibility.
3. Fix full-viewport grid.
4. Fix recenter/fit.
5. Build right detail bar.
6. Move Properties/BOM.
7. Remove bottom weight/length display.
8. Fix palette icons/overlays.
9. Restore double-click insertion.
10. Add drag/drop insertion.
11. Add R rotation.
12. Restore dimension rendering.
13. Fine-tune configurable snap.
14. Run V4 + V5 regression tests.
15. Build and report.

Do not proceed to new AI/catalogue features until this passes.
