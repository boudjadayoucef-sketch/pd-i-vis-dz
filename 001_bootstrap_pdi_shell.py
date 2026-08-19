#!/usr/bin/env python3
"""PD&I Patch 001 — isolate the legacy Guide shell and install a standalone PD&I shell.

Run from the repository root:
    python3 patches/001_bootstrap_pdi_shell.py

The patch is intentionally conservative:
- preserves the existing Guide App as src/GuideLegacyApp.tsx;
- replaces src/App.tsx with the autonomous PD&I entry point;
- creates a dependency-free PD&I shell under src/pdi/app/;
- does not delete legacy files or modify Firebase configuration.

The script is idempotent: it refuses to overwrite the legacy snapshot or the
new App entry point if they already exist, so a second run cannot destroy work.
"""

from pathlib import Path
import shutil
import textwrap

ROOT = Path(__file__).resolve().parent if (Path(__file__).resolve().parent / "src").exists() else Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
APP = SRC / "App.tsx"
LEGACY = SRC / "GuideLegacyApp.tsx"
PDI_APP = SRC / "pdi" / "app" / "PdiApp.tsx"
PDI_INDEX = SRC / "pdi" / "app" / "index.ts"

if not APP.exists():
    raise SystemExit("ERROR: src/App.tsx not found. Patch aborted.")

if LEGACY.exists():
    raise SystemExit(
        "ERROR: src/GuideLegacyApp.tsx already exists. "
        "Patch appears to have been applied already; no files changed."
    )

if PDI_APP.exists() or PDI_INDEX.exists():
    raise SystemExit(
        "ERROR: PD&I shell files already exist. Patch aborted to avoid overwriting work."
    )

PDI_APP.parent.mkdir(parents=True, exist_ok=True)

# Preserve the current Guide application without moving it, so all of its
# existing relative imports remain valid for later migration/reference work.
shutil.copy2(APP, LEGACY)

PDI_APP.write_text(
    textwrap.dedent(
        '''\
        import React, { useState } from "react";
        import type { LicensePlan } from "../saas/types";
        import { getDefaultEntitlements } from "../saas/entitlements";

        const PLAN_LABELS: Record<LicensePlan, string> = {
          trial: "Trial",
          professional: "Professional",
          team: "Team",
          enterprise: "Enterprise",
        };

        export default function PdiApp() {
          const [plan] = useState<LicensePlan>("trial");
          const entitlements = getDefaultEntitlements(plan);

          return (
            <div className="min-h-screen bg-slate-950 text-slate-100">
              <header className="border-b border-slate-800 bg-slate-950/95">
                <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
                  <div>
                    <div className="text-xl font-semibold tracking-tight">PD&I</div>
                    <div className="text-xs text-slate-400">Piping Design & Isometrics</div>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <span className="rounded-full border border-slate-700 px-3 py-1 text-slate-300">
                      {PLAN_LABELS[plan]}
                    </span>
                    <button className="rounded-lg border border-slate-700 px-3 py-2 hover:bg-slate-900">
                      Account
                    </button>
                  </div>
                </div>
              </header>

              <main className="mx-auto max-w-7xl px-6 py-10">
                <section className="mb-10">
                  <p className="mb-3 text-sm font-medium text-cyan-400">PD&I SaaS</p>
                  <h1 className="max-w-3xl text-4xl font-semibold tracking-tight">
                    Piping design and isometric engineering in one workspace.
                  </h1>
                  <p className="mt-4 max-w-2xl text-slate-400">
                    This is the autonomous PD&I application shell. The legacy Guide remains
                    preserved separately while the piping model, isometric engine, CAD and AI
                    services are migrated into this product boundary.
                  </p>
                </section>

                <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                  {[
                    ["Projects", "Create and manage piping projects."],
                    ["Isometrics", "Open the future standalone isometric editor."],
                    ["CAD / JSON", "Exchange the canonical piping model."],
                    ["AI", "Assist recognition and engineering workflows."],
                  ].map(([title, description]) => (
                    <button
                      key={title}
                      className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5 text-left transition hover:border-slate-600 hover:bg-slate-900"
                    >
                      <div className="text-base font-medium">{title}</div>
                      <div className="mt-2 text-sm text-slate-400">{description}</div>
                    </button>
                  ))}
                </section>

                <section className="mt-8 rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
                  <div className="flex flex-wrap items-center justify-between gap-4">
                    <div>
                      <h2 className="font-medium">Current workspace</h2>
                      <p className="mt-1 text-sm text-slate-400">
                        SaaS boundary is active; authorization and licensing remain server-authoritative.
                      </p>
                    </div>
                    <div className="text-right text-sm text-slate-400">
                      <div>{entitlements.isometric ? "Isometric enabled" : "Isometric locked"}</div>
                      <div>{entitlements.dxfImport ? "DXF import enabled" : "DXF import locked"}</div>
                    </div>
                  </div>
                </section>
              </main>
            </div>
          );
        }
        '''
    ),
    encoding="utf-8",
)

PDI_INDEX.write_text(
    'export { default as PdiApp } from "./PdiApp";\n',
    encoding="utf-8",
)

APP.write_text(
    textwrap.dedent(
        '''\
        /**
         * PD&I autonomous SaaS entry point.
         *
         * The former PLAN-SONELGAZ-TG-GUIDE application is preserved in
         * GuideLegacyApp.tsx for controlled extraction and regression reference.
         */
        import React from "react";
        import { PdiApp } from "./pdi/app";

        export default function App() {
          return <PdiApp />;
        }
        '''
    ),
    encoding="utf-8",
)

print("PD&I Patch 001 applied successfully.")
print("Preserved: src/GuideLegacyApp.tsx")
print("Created:  src/pdi/app/PdiApp.tsx")
print("Created:  src/pdi/app/index.ts")
print("Replaced: src/App.tsx with autonomous PD&I entry point")
print("Next: run npm run build and verify the Preview before any further migration.")
