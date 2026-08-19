#!/usr/bin/env python3
"""PD&I Patch 002 — add the autonomous SaaS dashboard shell and navigation.

Run from repository root:
    python3 patches/002_saas_dashboard_navigation.py

Scope:
- replaces the temporary PdiApp shell with a small client-side SaaS dashboard;
- adds Dashboard, Projects, Isometrics, CAD / JSON and AI sections;
- adds a simple account menu placeholder;
- keeps the legacy Guide untouched;
- does not add authentication, routing libraries, backend services, billing,
  or modify the piping/isometric engine.

The patch is intentionally reversible and idempotent.
"""

from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent if (Path(__file__).resolve().parent / "src").exists() else Path(__file__).resolve().parents[1]
PDI_APP = ROOT / "src" / "pdi" / "app" / "PdiApp.tsx"
MARKER = "// PD&I PATCH 002"

if not PDI_APP.exists():
    raise SystemExit("ERROR: src/pdi/app/PdiApp.tsx not found. Patch aborted.")

current = PDI_APP.read_text(encoding="utf-8")
if MARKER in current:
    raise SystemExit("ERROR: Patch 002 appears to be already applied; no files changed.")

content = textwrap.dedent(
    '''\
    // PD&I PATCH 002
    import React, { useState } from "react";
    import type { LicensePlan } from "../saas/types";
    import { getDefaultEntitlements } from "../saas/entitlements";

    type Section = "dashboard" | "projects" | "isometrics" | "cad" | "ai";

    const PLAN_LABELS: Record<LicensePlan, string> = {
      trial: "Trial",
      professional: "Professional",
      team: "Team",
      enterprise: "Enterprise",
    };

    const NAV_ITEMS: Array<{ id: Section; label: string; description: string }> = [
      { id: "dashboard", label: "Dashboard", description: "Workspace overview" },
      { id: "projects", label: "Projects", description: "Piping projects" },
      { id: "isometrics", label: "Isometrics", description: "Isometric drawings" },
      { id: "cad", label: "CAD / JSON", description: "Engineering exchange" },
      { id: "ai", label: "AI", description: "Engineering assistance" },
    ];

    function SectionContent({ section }: { section: Section }) {
      if (section === "dashboard") {
        return (
          <>
            <div className="mb-8">
              <p className="mb-2 text-sm font-medium text-cyan-400">PD&I SaaS</p>
              <h1 className="text-3xl font-semibold tracking-tight">Engineering workspace</h1>
              <p className="mt-2 max-w-2xl text-slate-400">
                Manage piping projects, isometrics, CAD exchange and AI-assisted workflows from one workspace.
              </p>
            </div>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {NAV_ITEMS.slice(1).map((item) => (
                <div key={item.id} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
                  <div className="text-base font-medium">{item.label}</div>
                  <div className="mt-2 text-sm text-slate-400">{item.description}</div>
                  <div className="mt-5 text-xs text-slate-500">Module foundation ready</div>
                </div>
              ))}
            </div>
          </>
        );
      }

      const content: Record<Exclude<Section, "dashboard">, { title: string; text: string }> = {
        projects: {
          title: "Projects",
          text: "Project management will be connected to the autonomous PD&I data layer in a later patch.",
        },
        isometrics: {
          title: "Isometrics",
          text: "The standalone isometric editor will be connected after the canonical piping model and legacy engine adapter are ready.",
        },
        cad: {
          title: "CAD / JSON",
          text: "DXF import/export and canonical Piping JSON exchange will be connected in later patches.",
        },
        ai: {
          title: "AI",
          text: "AI tools will consume the canonical piping model through explicit services and deterministic engineering tools.",
        },
      };

      return (
        <div className="max-w-3xl">
          <p className="mb-2 text-sm font-medium text-cyan-400">PD&I</p>
          <h1 className="text-3xl font-semibold tracking-tight">{content[section].title}</h1>
          <p className="mt-4 text-slate-400">{content[section].text}</p>
          <div className="mt-8 rounded-2xl border border-dashed border-slate-700 bg-slate-900/40 p-6 text-sm text-slate-500">
            This module is intentionally a foundation placeholder. No legacy Guide code is executed here.
          </div>
        </div>
      );
    }

    export default function PdiApp() {
      const [plan] = useState<LicensePlan>("trial");
      const [section, setSection] = useState<Section>("dashboard");
      const [accountOpen, setAccountOpen] = useState(false);
      const entitlements = getDefaultEntitlements(plan);

      return (
        <div className="min-h-screen bg-slate-950 text-slate-100">
          <header className="border-b border-slate-800 bg-slate-950/95">
            <div className="flex h-16 items-center justify-between px-5">
              <div className="flex items-center gap-8">
                <button onClick={() => setSection("dashboard")} className="text-left">
                  <div className="text-xl font-semibold tracking-tight">PD&I</div>
                  <div className="text-[11px] text-slate-500">Piping Design & Isometrics</div>
                </button>
                <nav className="hidden items-center gap-1 md:flex">
                  {NAV_ITEMS.map((item) => (
                    <button
                      key={item.id}
                      onClick={() => setSection(item.id)}
                      className={`rounded-lg px-3 py-2 text-sm transition ${
                        section === item.id
                          ? "bg-slate-800 text-white"
                          : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
                      }`}
                    >
                      {item.label}
                    </button>
                  ))}
                </nav>
              </div>

              <div className="relative flex items-center gap-3 text-sm">
                <span className="rounded-full border border-slate-700 px-3 py-1 text-slate-300">
                  {PLAN_LABELS[plan]}
                </span>
                <button
                  onClick={() => setAccountOpen((value) => !value)}
                  className="rounded-lg border border-slate-700 px-3 py-2 hover:bg-slate-900"
                >
                  Account
                </button>
                {accountOpen && (
                  <div className="absolute right-0 top-12 z-10 w-52 rounded-xl border border-slate-800 bg-slate-900 p-2 shadow-xl">
                    <div className="px-3 py-2 text-xs text-slate-500">Current account</div>
                    <button className="w-full rounded-lg px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800">
                      Profile
                    </button>
                    <button className="w-full rounded-lg px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800">
                      Organization
                    </button>
                    <button className="w-full rounded-lg px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800">
                      License
                    </button>
                  </div>
                )}
              </div>
            </div>
          </header>

          <div className="flex min-h-[calc(100vh-4rem)]">
            <aside className="hidden w-56 shrink-0 border-r border-slate-800 bg-slate-950/70 p-3 lg:block">
              <div className="mb-3 px-3 py-2 text-[11px] font-medium uppercase tracking-wider text-slate-600">
                Workspace
              </div>
              <div className="space-y-1">
                {NAV_ITEMS.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setSection(item.id)}
                    className={`w-full rounded-lg px-3 py-2.5 text-left transition ${
                      section === item.id
                        ? "bg-slate-800 text-white"
                        : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
                    }`}
                  >
                    <div className="text-sm">{item.label}</div>
                    <div className="mt-0.5 text-[11px] text-slate-600">{item.description}</div>
                  </button>
                ))}
              </div>

              <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900/50 p-3">
                <div className="text-xs font-medium text-slate-400">Workspace status</div>
                <div className="mt-2 text-xs text-slate-500">
                  {entitlements.isometric ? "Isometric enabled" : "Isometric locked"}
                </div>
                <div className="mt-1 text-xs text-slate-500">
                  {entitlements.dxfImport ? "DXF import enabled" : "DXF import locked"}
                </div>
              </div>
            </aside>

            <main className="min-w-0 flex-1 px-5 py-8 md:px-8">
              <SectionContent section={section} />
            </main>
          </div>
        </div>
      );
    }
    '''
)

PDI_APP.write_text(content, encoding="utf-8")
print("PD&I Patch 002 applied successfully.")
print("Updated: src/pdi/app/PdiApp.tsx")
print("Added: dashboard shell, workspace navigation and account placeholder.")
print("Legacy Guide and backend configuration were not modified.")
print("Next: run npm run build and verify all navigation sections in Preview.")
