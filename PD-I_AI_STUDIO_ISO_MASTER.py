"""
PD-I / ISO — AI Studio Master Development Brief
================================================

USAGE
-----
Use this file as the single master brief for an AI coding session.
It is intentionally self-contained and provider-neutral.

SCOPE
-----
Develop ONLY the ISO professional drawing experience in PD-I.
Do NOT modify piping-design-skill in this phase.
Do NOT replace the existing ISO V4.8d engine.
Do NOT invent a second geometry engine.

CURRENT REPOSITORY CONTEXT
--------------------------
Repository:
    boudjadayoucef-sketch/PD-I

Working branch:
    feature/saas-iso-foundation

Stack observed:
    React 19
    TypeScript 5.8
    Vite
    Express
    Tailwind CSS
    lucide-react
    @google/genai is present, but AI integration is NOT the priority here.

Current ISO foundation:
    src/pdi/isometric/PdiIsometricEditor.tsx
    src/pdi/isometric/IsoWorkspace.tsx
    src/pdi/isometric/IsoProfessionalWorkspace.tsx
    src/pdi/isometric/isoProjection.ts

IMPORTANT
---------
The existing PdiIsometricEditor / V4.8d implementation is valuable legacy
engineering logic. Preserve it. Refactor around it incrementally.

PRODUCT GOAL
------------
Make PD-I usable as a professional piping isometric drafting application
BEFORE connecting AI reconstruction.

The user must be able to:
    - create/edit a piping isometric drawing
    - navigate naturally
    - select objects precisely
    - snap to meaningful ISO points
    - create/edit pipe segments and fittings
    - edit valves and components
    - place dimensions
    - place annotations/tags
    - manage layers/visibility
    - undo/redo operations
    - save/reopen a drawing without losing state
    - validate the drawing
    - prepare a professional ISO sheet
    - export a clean visual representation

NON-NEGOTIABLE ARCHITECTURE
---------------------------
1. Canonical model remains the source of truth.
2. Geometry calculations remain deterministic.
3. UI does not directly own engineering geometry.
4. AI must never invent exact engineering coordinates.
5. Existing V4.8d engine must not be deleted/replaced.
6. New functionality must be introduced behind small interfaces.
7. Avoid giant components and duplicated state.
8. Every modification must preserve current behavior.
9. Do not modify PD-I main unless explicitly requested.
10. Do not modify piping-design-skill during this ISO maturation phase.

PROFESSIONAL ISO WORKFLOW
-------------------------
SESSION
  |
  +--> Open/Create project
  |
  +--> Select ISO drawing
  |
  +--> Configure sheet
  |
  +--> Draw / edit piping
  |      |
  |      +--> selection
  |      +--> snapping
  |      +--> pipe routing
  |      +--> fittings
  |      +--> valves
  |      +--> components
  |
  +--> Annotate
  |      +--> dimensions
  |      +--> line number
  |      +--> component tags
  |      +--> notes
  |      +--> weld markers
  |
  +--> Validate
  |
  +--> Save revision
  |
  +--> Preview
  |
  +--> Export
         +--> SVG
         +--> PDF
         +--> DXF (when supported)

PHASE PLAN
----------
PHASE 1 — Interaction foundation
    - robust pan/zoom
    - fit drawing
    - selection
    - box selection
    - hover highlighting
    - keyboard shortcuts
    - escape/cancel
    - delete
    - undo/redo

PHASE 2 — ISO snapping
    - endpoint snap
    - port snap
    - midpoint snap
    - intersection snap
    - axis snap
    - grid snap
    - visible snap feedback
    - configurable snap priority

PHASE 3 — Drawing operations
    - create pipe segment
    - extend segment
    - trim segment
    - move segment
    - rotate fitting
    - insert elbow
    - insert tee
    - insert reducer
    - insert valve
    - connect components

PHASE 4 — Professional annotation
    - dimensions
    - leaders
    - component tags
    - line labels
    - notes
    - weld symbols
    - configurable annotation styles

PHASE 5 — Sheet composition
    - title block
    - project metadata
    - drawing number
    - revision
    - scale
    - units
    - north/flow indication where applicable
    - margins
    - paper sizes A4/A3/A2/A1 as appropriate
    - print preview

PHASE 6 — QA
    - disconnected ports
    - dangling segments
    - invalid fittings
    - duplicate IDs
    - invalid dimensions
    - missing required metadata
    - visual overlap warnings
    - export readiness

PHASE 7 — Persistence
    - canonical JSON save
    - reopen exact drawing state
    - revision metadata
    - dirty-state detection
    - autosave strategy

PHASE 8 — Export
    - SVG first
    - PDF
    - DXF after deterministic export contract is stable

UX REQUIREMENTS
---------------
The interface should feel like a professional engineering drawing tool,
not a generic web canvas.

Required interaction principles:
    - keyboard-first where appropriate
    - mouse-first for drawing
    - predictable cursor/tool behavior
    - explicit active tool
    - obvious selection state
    - non-destructive operations
    - undo available after every mutation
    - no hidden modal traps
    - zoom must preserve cursor focus
    - pan must never mutate geometry
    - snap feedback must be visible
    - properties panel reflects selected object
    - no fake buttons that do nothing

Suggested shortcuts:
    V = select
    H = pan
    D = dimension
    G = grid
    Esc = cancel/current tool reset
    Delete/Backspace = delete selection
    Ctrl/Cmd+Z = undo
    Ctrl/Cmd+Shift+Z = redo
    Ctrl/Cmd+S = save

MODEL CONTRACT
--------------
Prefer an explicit service boundary such as:

    IsoDocument
      - metadata
      - model
      - annotations
      - sheet
      - layers
      - revisions

    IsoEditorState
      - activeTool
      - selection
      - hover
      - viewport
      - snap
      - panels

    IsoCommand
      - execute()
      - undo()
      - description

Do NOT create parallel copies of piping geometry in React state.

ENGINEERING SAFETY
------------------
Never infer exact:
    - lengths
    - coordinates
    - angles
    - diameters
    - elevations
    - connectivity

from visual appearance alone.

If an operation requires engineering geometry, call the deterministic
model/geometry layer.

TESTING
-------
For each feature:
    1. TypeScript compile/lint
    2. existing app build
    3. focused unit tests if available
    4. manual interaction check
    5. regression check of V4.8d behavior

ACCEPTANCE CRITERIA
-------------------
ISO is considered mature only when a user can complete this scenario:

    Create project
      -> create/open ISO
      -> draw connected pipe route
      -> add elbow
      -> add tee
      -> add valve
      -> edit properties
      -> use snapping
      -> select/move/delete
      -> undo/redo
      -> add dimensions
      -> add tags/notes
      -> toggle layers
      -> validate
      -> save
      -> reload
      -> preview sheet
      -> export

and the drawing remains geometrically and visually consistent.

DEVELOPMENT RULE
----------------
Before editing a file:
    - inspect its current content
    - inspect imports and consumers
    - identify the current source of truth
    - make the smallest safe change

After editing:
    - run lint/typecheck/build
    - report failures honestly
    - do not hide or bypass errors
    - do not rewrite unrelated files

DO NOT DO
---------
- Do not rewrite the whole ISO editor.
- Do not replace V4.8d with a new canvas library just for convenience.
- Do not introduce AI into geometry calculations.
- Do not add speculative abstractions everywhere.
- Do not modify PD-I files unrelated to ISO.
- Do not modify piping-design-skill.
- Do not claim a feature is implemented if its button is only visual.
- Do not break existing import/export behavior.

NEXT IMPLEMENTATION ORDER
-------------------------
Start with:
    1. audit current editor interaction/state
    2. selection model
    3. command/undo-redo foundation
    4. snapping service
    5. viewport service
    6. real toolbar actions
    7. object properties binding
    8. dimensions
    9. annotations
    10. layers
    11. sheet/cartouche
    12. QA
    13. persistence
    14. export

For every task, first inspect the current repository and reuse existing
functionality before creating new functionality.

FINAL RULE
----------
The goal is not to make a beautiful mockup.

The goal is to make PD-I's ISO module behave like a real professional
piping-isometric drafting application, with deterministic engineering logic,
a stable canonical model, and a clean foundation for future AI integration.
"""

PROJECT = {
    "repo": "boudjadayoucef-sketch/PD-I",
    "branch": "feature/saas-iso-foundation",
    "scope": "ISO professional drafting maturation",
    "do_not_touch": ["main", "piping-design-skill"],
}

if __name__ == "__main__":
    print(__doc__)
