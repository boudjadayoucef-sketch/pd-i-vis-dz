#!/usr/bin/env python3
"""PD&I Patch 002 — interface SaaS française et navigation.

Exécuter depuis la racine :
    python3 patches/002_saas_dashboard_navigation.py

Portée :
- remplace le shell temporaire PdiApp par un tableau de bord SaaS français ;
- ajoute Tableau de bord, Projets, Isométries, CAO / JSON et IA ;
- ajoute un menu Compte provisoire ;
- conserve le Guide historique intact ;
- n'ajoute ni authentification, ni facturation, ni nouveau backend ;
- ne modifie pas le moteur piping/isométrique.

La version française est la langue principale du produit pour cette phase.
Une couche i18n anglaise sera ajoutée ultérieurement dans un patch dédié.
"""

from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent if (Path(__file__).resolve().parent / "src").exists() else Path(__file__).resolve().parents[1]
PDI_APP = ROOT / "src" / "pdi" / "app" / "PdiApp.tsx"
MARKER = "// PD&I PATCH 002 FR"

if not PDI_APP.exists():
    raise SystemExit("ERREUR : src/pdi/app/PdiApp.tsx introuvable. Patch annulé.")

current = PDI_APP.read_text(encoding="utf-8")
if MARKER in current:
    raise SystemExit("ERREUR : le Patch 002 FR semble déjà appliqué ; aucun fichier modifié.")

content = textwrap.dedent(
    '''\
    // PD&I PATCH 002 FR
    import React, { useState } from "react";
    import type { LicensePlan } from "../saas/types";
    import { getDefaultEntitlements } from "../saas/entitlements";

    type Section = "dashboard" | "projects" | "isometrics" | "cad" | "ai";

    const PLAN_LABELS: Record<LicensePlan, string> = {
      trial: "Essai",
      professional: "Professionnel",
      team: "Équipe",
      enterprise: "Entreprise",
    };

    const NAV_ITEMS: Array<{ id: Section; label: string; description: string }> = [
      { id: "dashboard", label: "Tableau de bord", description: "Vue d’ensemble de l’espace" },
      { id: "projects", label: "Projets", description: "Projets de tuyauterie" },
      { id: "isometrics", label: "Isométries", description: "Plans isométriques" },
      { id: "cad", label: "CAO / JSON", description: "Échanges techniques" },
      { id: "ai", label: "IA", description: "Assistance ingénierie" },
    ];

    function SectionContent({ section }: { section: Section }) {
      if (section === "dashboard") {
        return (
          <>
            <div className="mb-8">
              <p className="mb-2 text-sm font-medium text-cyan-400">PD&I SaaS</p>
              <h1 className="text-3xl font-semibold tracking-tight">Espace de travail ingénierie</h1>
              <p className="mt-2 max-w-2xl text-slate-400">
                Gérez vos projets de tuyauterie, vos isométries, vos échanges CAO et vos flux assistés par IA depuis un espace unique.
              </p>
            </div>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {NAV_ITEMS.slice(1).map((item) => (
                <div key={item.id} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
                  <div className="text-base font-medium">{item.label}</div>
                  <div className="mt-2 text-sm text-slate-400">{item.description}</div>
                  <div className="mt-5 text-xs text-slate-500">Module en préparation</div>
                </div>
              ))}
            </div>
          </>
        );
      }

      const content: Record<Exclude<Section, "dashboard">, { title: string; text: string }> = {
        projects: {
          title: "Projets",
          text: "La gestion des projets sera connectée à la couche de données autonome de PD&I dans un prochain patch.",
        },
        isometrics: {
          title: "Isométries",
          text: "L’éditeur isométrique autonome sera connecté après la stabilisation du modèle de tuyauterie canonique et de l’adaptateur du moteur historique.",
        },
        cad: {
          title: "CAO / JSON",
          text: "L’import/export DXF et les échanges avec le modèle Piping JSON canonique seront connectés dans les prochains patches.",
        },
        ai: {
          title: "Intelligence artificielle",
          text: "Les outils IA utiliseront le modèle de tuyauterie canonique au travers de services explicites et d’outils d’ingénierie déterministes.",
        },
      };

      return (
        <div className="max-w-3xl">
          <p className="mb-2 text-sm font-medium text-cyan-400">PD&I</p>
          <h1 className="text-3xl font-semibold tracking-tight">{content[section].title}</h1>
          <p className="mt-4 text-slate-400">{content[section].text}</p>
          <div className="mt-8 rounded-2xl border border-dashed border-slate-700 bg-slate-900/40 p-6 text-sm text-slate-500">
            Ce module constitue actuellement une base de travail. Aucun code de l’ancien Guide n’est exécuté ici.
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
                  <div className="text-[11px] text-slate-500">Conception de tuyauterie & isométries</div>
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
                  Compte
                </button>
                {accountOpen && (
                  <div className="absolute right-0 top-12 z-10 w-56 rounded-xl border border-slate-800 bg-slate-900 p-2 shadow-xl">
                    <div className="px-3 py-2 text-xs text-slate-500">Mon compte</div>
                    <button className="w-full rounded-lg px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800">
                      Profil
                    </button>
                    <button className="w-full rounded-lg px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800">
                      Organisation
                    </button>
                    <button className="w-full rounded-lg px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800">
                      Licence
                    </button>
                  </div>
                )}
              </div>
            </div>
          </header>

          <div className="flex min-h-[calc(100vh-4rem)]">
            <aside className="hidden w-56 shrink-0 border-r border-slate-800 bg-slate-950/70 p-3 lg:block">
              <div className="mb-3 px-3 py-2 text-[11px] font-medium uppercase tracking-wider text-slate-600">
                Espace de travail
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
                <div className="text-xs font-medium text-slate-400">État de l’espace</div>
                <div className="mt-2 text-xs text-slate-500">
                  {entitlements.isometric ? "Isométrie activée" : "Isométrie verrouillée"}
                </div>
                <div className="mt-1 text-xs text-slate-500">
                  {entitlements.dxfImport ? "Import DXF activé" : "Import DXF verrouillé"}
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
print("Patch 002 FR appliqué avec succès.")
print("Mis à jour : src/pdi/app/PdiApp.tsx")
print("Interface principale : français.")
print("Le Guide historique et la configuration backend ne sont pas modifiés.")
print("Étape suivante : exécuter npm run build et tester toute la navigation dans Preview.")
