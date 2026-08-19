#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I PATCH 007c — Shell unifié + accueil + ISO module principal
================================================================

À exécuter depuis la racine du dépôt PD-I :

    python3 007c_pdi_unified_shell_home_orchestrator.py

Direction validée :
- arrêter d'avoir deux logiciels concurrents : shell SaaS + ancien ISO ;
- garder une page d'accueil PD&I, puis ouvrir l'ISO comme module principal plein écran ;
- utiliser le bandeau vertical gauche de l'accueil comme navigation vers les grands modules ;
- réserver les menus du haut aux commandes du module actif ;
- ajouter "Vision PD&I" comme module Photo/Croquis → JSON/ISO ;
- préparer le branchement futur vers le repo piping-design-skill : équipe d'agents spécialisés,
  avec PD&I comme orchestrateur ;
- rappeler : les calculs techniques se font par Python/règles déterministes, pas par IA générative.

Le patch crée un shell PdiUnifiedApp, bascule src/App.tsx vers ce shell,
force l'ancien moteur ISO à rester en mode plein écran/principal par défaut,
et transforme le bouton de sortie ISO en "Retour accueil" via événement navigateur pdi:navigate.
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
from pathlib import Path

ROOT = Path.cwd()
PATCH_ID = "007c"
STAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT / f".patch_backups/{PATCH_ID}_{STAMP}"
REPORT = ROOT / f"patch_{PATCH_ID}_report.txt"

SRC_APP = ROOT / "src/App.tsx"
UNIFIED_APP = ROOT / "src/pdi/app/PdiUnifiedApp.tsx"
BRAND = ROOT / "src/pdi/app/PdiBrandMark.tsx"
ENGINE = ROOT / "src/pdi/isometric/engine/IsometrieModuleV48d.tsx"
WRAPPER = ROOT / "src/pdi/isometric/PdiIsometricEditor.tsx"
DOCS = ROOT / "docs"
PATCH_HISTORY = DOCS / "PATCH_HISTORY.md"
ORCHESTRATOR_DOC = DOCS / "PD_I_ORCHESTRATOR_PIPELINE_SKILLS.md"
GITIGNORE = ROOT / ".gitignore"


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def backup(path: Path) -> None:
    if path.exists() and path.is_file():
        dest = BACKUP_DIR / path.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def write_if_changed(path: Path, content: str, report: list[str]) -> bool:
    old = read(path)
    if old == content:
        report.append(f"UNCHANGED {rel(path)}")
        return False
    backup(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    report.append(f"UPDATED {rel(path)}")
    return True


def ensure_brand(report: list[str]) -> None:
    # Toujours utiliser /public, pas un SVG/fallback.
    content = '''import React from "react";

// PD&I PATCH 007c — Branding global depuis /public.
// Placer les vrais logos ici :
// public/pdi-logo-horizontal.png
// public/pdi-logo-square.png
const PDI_LOGO_HORIZONTAL_PUBLIC = "/pdi-logo-horizontal.png";
const PDI_LOGO_SQUARE_PUBLIC = "/pdi-logo-square.png";

export type PdiBrandMarkProps = {
  variant?: "horizontal" | "compact";
  size?: "sm" | "md" | "lg";
  className?: string;
};

export default function PdiBrandMark({
  variant = "horizontal",
  size = "md",
  className = "",
}: PdiBrandMarkProps) {
  const compact = variant === "compact";
  const height = size === "sm" ? 38 : size === "lg" ? 70 : 52;
  return (
    <div className={`pdi-brand-mark ${className}`} aria-label="PD&I — Piping Design & Isometrics">
      <img
        src={compact ? PDI_LOGO_SQUARE_PUBLIC : PDI_LOGO_HORIZONTAL_PUBLIC}
        alt="PD&I — Piping Design & Isometrics"
        style={{
          height,
          width: compact ? height : undefined,
          maxWidth: compact ? height : "min(320px, 34vw)",
          objectFit: "contain",
          display: "block",
        }}
        draggable={false}
      />
    </div>
  );
}
'''
    write_if_changed(BRAND, content, report)


def write_unified_app(report: list[str]) -> None:
    content = '''import React, { useEffect, useMemo, useState } from "react";
import PdiBrandMark from "./PdiBrandMark";
import PdiIsometricEditor from "../isometric/PdiIsometricEditor";

type PdiModule = "home" | "isometric" | "vision" | "sketch" | "cad" | "json" | "pdf" | "projects" | "assistant";

type LaunchCard = {
  id: PdiModule;
  title: string;
  subtitle: string;
  badge: string;
  icon: string;
  ready?: boolean;
};

const launchCards: LaunchCard[] = [
  { id: "isometric", title: "Dessin isométrique", subtitle: "Créer un projet manuel avec nœuds, tubes, équipements, cotations et alignements.", badge: "V4.8d1", icon: "ISO", ready: true },
  { id: "vision", title: "Vision PD&I", subtitle: "Transformer une photo de plant réel en JSON piping puis en ISO après validation.", badge: "Photo → ISO", icon: "VIS" },
  { id: "sketch", title: "Croquis → ISO", subtitle: "Importer un dessin à la main, extraire le réseau, valider le JSON puis générer l’ISO.", badge: "Croquis", icon: "CRQ" },
  { id: "cad", title: "Importer CAO / DXF", subtitle: "Lire un DXF/PDF, extraire calques/lignes/blocs et convertir vers JSON PD&I.", badge: "DXF/PDF", icon: "DX" },
  { id: "json", title: "Ouvrir JSON PD&I", subtitle: "Charger ou vérifier le modèle central : lignes, nœuds, équipements, soudures, cotations.", badge: "JSON", icon: "{}" },
  { id: "pdf", title: "Impression / exports", subtitle: "Préparer PDF, DXF, planches A4/A3/A2/A1, cartouche et nomenclature.", badge: "PDF/DXF", icon: "OUT" },
];

const navItems: Array<{ id: PdiModule; label: string; icon: string; title: string }> = [
  { id: "home", label: "Accueil", icon: "⌂", title: "Accueil PD&I" },
  { id: "isometric", label: "ISO", icon: "ISO", title: "Dessin isométrique" },
  { id: "vision", label: "Vision", icon: "VIS", title: "Vision PD&I — Photo vers ISO" },
  { id: "sketch", label: "Croquis", icon: "CRQ", title: "Croquis vers JSON/ISO" },
  { id: "cad", label: "CAO", icon: "DX", title: "Import CAD/DXF/PDF" },
  { id: "json", label: "JSON", icon: "{}", title: "Modèle JSON PD&I" },
  { id: "pdf", label: "Export", icon: "PDF", title: "PDF / DXF / Impression" },
  { id: "assistant", label: "IA", icon: "AI", title: "Assistant et agents spécialisés" },
];

function ComingSoonPanel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="pdi-module-panel">
      <div className="pdi-panel-kicker">Module préparé</div>
      <h1>{title}</h1>
      <div className="pdi-panel-body">{children}</div>
    </section>
  );
}

export default function PdiUnifiedApp() {
  const [activeModule, setActiveModule] = useState<PdiModule>("home");

  useEffect(() => {
    const onNavigate = (event: Event) => {
      const detail = (event as CustomEvent<PdiModule>).detail;
      setActiveModule(detail || "home");
    };
    window.addEventListener("pdi:navigate", onNavigate as EventListener);
    return () => window.removeEventListener("pdi:navigate", onNavigate as EventListener);
  }, []);

  const moduleTitle = useMemo(() => navItems.find((x) => x.id === activeModule)?.title || "PD&I", [activeModule]);

  // ISO devient le module principal : quand il est actif, on affiche uniquement son workspace.
  // On évite ainsi deux logiciels concurrents à l’écran.
  if (activeModule === "isometric") {
    return <PdiIsometricEditor />;
  }

  return (
    <div className="pdi-unified-root">
      <style>{`
        .pdi-unified-root{height:100vh;width:100vw;overflow:hidden;background:#070B12;color:#E5EDF8;font-family:Inter,ui-sans-serif,system-ui,sans-serif;display:grid;grid-template-columns:96px 1fr;grid-template-rows:72px 1fr}
        .pdi-unified-topbar{grid-column:1/3;display:flex;align-items:center;gap:18px;padding:8px 16px;background:linear-gradient(180deg,#111827,#0B1019);border-bottom:1px solid rgba(148,163,184,.22);box-shadow:0 8px 24px rgba(0,0,0,.28);min-width:0}
        .pdi-unified-brand{display:flex;align-items:center;gap:14px;min-width:260px}
        .pdi-project-title{min-width:0;border-left:1px solid rgba(148,163,184,.28);padding-left:14px;line-height:1.1}.pdi-project-title small{display:block;color:#8EA3C2;font-size:10px;text-transform:uppercase;font-weight:900}.pdi-project-title strong{display:block;color:#F8FAFC;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
        .pdi-top-actions{margin-left:auto;display:flex;align-items:center;gap:8px;color:#93A4BD;font-size:12px}.pdi-search{height:36px;width:min(340px,24vw);border:1px solid rgba(148,163,184,.22);background:#0A1220;color:#E5EDF8;border-radius:10px;padding:0 12px;font-weight:800}.pdi-account{height:36px;border:1px solid rgba(34,211,238,.35);background:#0A1220;color:#F8FAFC;border-radius:10px;padding:0 12px;font-weight:900}
        .pdi-main-nav{grid-row:2;display:flex;flex-direction:column;gap:10px;padding:14px 10px;background:linear-gradient(180deg,#0D1420,#090E17);border-right:1px solid rgba(148,163,184,.18);overflow:auto}.pdi-main-nav button{height:58px;border:1px solid rgba(148,163,184,.16);background:#111827;color:#BBD0EA;border-radius:14px;font-weight:1000;font-size:13px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer}.pdi-main-nav button.active{background:linear-gradient(135deg,#0284C7,#0EA5E9);color:white;border-color:#67E8F9;box-shadow:0 0 0 1px rgba(103,232,249,.55),0 16px 35px rgba(14,165,233,.25)}.pdi-main-nav small{font-size:8px;letter-spacing:.06em;text-transform:uppercase;opacity:.82}
        .pdi-content{grid-column:2;grid-row:2;min-width:0;min-height:0;overflow:auto;padding:22px;background:radial-gradient(circle at 18% 8%,rgba(14,165,233,.16),transparent 32%),radial-gradient(circle at 86% 12%,rgba(249,115,22,.13),transparent 28%),#070B12}.pdi-home-hero{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(320px,.8fr);gap:20px;align-items:stretch}.pdi-hero-card,.pdi-module-panel,.pdi-launch-card{border:1px solid rgba(148,163,184,.18);background:linear-gradient(180deg,rgba(15,23,42,.92),rgba(8,13,24,.96));border-radius:24px;box-shadow:0 24px 70px rgba(0,0,0,.28)}.pdi-hero-card{padding:28px}.pdi-hero-card h1,.pdi-module-panel h1{font-size:clamp(28px,4vw,54px);line-height:.95;margin:0;color:#F8FAFC;letter-spacing:-.04em}.pdi-hero-card p{color:#B9C8DD;font-weight:700;max-width:760px}.pdi-badge-row{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.pdi-badge{border:1px solid rgba(103,232,249,.28);background:rgba(8,145,178,.12);color:#67E8F9;border-radius:999px;padding:7px 10px;font-size:11px;font-weight:1000;text-transform:uppercase}.pdi-launch-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:20px}.pdi-launch-card{padding:18px;text-align:left;color:#E5EDF8;cursor:pointer;transition:.18s transform,.18s border-color}.pdi-launch-card:hover{transform:translateY(-2px);border-color:#38BDF8}.pdi-launch-card .icon{width:54px;height:54px;border-radius:16px;display:grid;place-items:center;background:#0EA5E9;color:white;font-weight:1000;margin-bottom:12px}.pdi-launch-card h3{margin:0 0 8px;font-size:18px}.pdi-launch-card p{margin:0;color:#9FB0C8;font-size:12px;font-weight:700}.pdi-launch-card .badge{display:inline-block;margin-top:12px;color:#FDE68A;font-size:10px;font-weight:1000;text-transform:uppercase}.pdi-side-card{padding:22px}.pdi-side-card h2{margin:0 0 12px}.pdi-side-card ul{margin:0;padding-left:18px;color:#B9C8DD;font-weight:700;line-height:1.8}.pdi-module-panel{padding:28px;min-height:calc(100vh - 128px)}.pdi-panel-kicker{color:#67E8F9;font-size:11px;text-transform:uppercase;font-weight:1000;margin-bottom:10px}.pdi-panel-body{margin-top:20px;color:#B9C8DD;font-weight:750;line-height:1.75;max-width:980px}.pdi-panel-body code{background:#111827;border:1px solid rgba(148,163,184,.18);border-radius:8px;padding:3px 6px;color:#FDE68A}.pdi-start-primary{border:0;background:linear-gradient(135deg,#0284C7,#22D3EE);color:white;border-radius:16px;padding:14px 18px;font-weight:1000;cursor:pointer;box-shadow:0 18px 45px rgba(14,165,233,.28)}
        @media(max-width:900px){.pdi-unified-root{grid-template-columns:1fr;grid-template-rows:72px auto 1fr}.pdi-unified-topbar{grid-column:1}.pdi-project-title,.pdi-search{display:none}.pdi-main-nav{grid-row:2;flex-direction:row;overflow-x:auto;padding:8px}.pdi-main-nav button{min-width:72px;height:54px}.pdi-content{grid-column:1;grid-row:3;padding:12px}.pdi-home-hero{grid-template-columns:1fr}.pdi-launch-grid{grid-template-columns:1fr}}
      `}</style>

      <header className="pdi-unified-topbar">
        <div className="pdi-unified-brand"><PdiBrandMark variant="horizontal" size="sm" /></div>
        <div className="pdi-project-title"><small>Projet actif</small><strong>{moduleTitle}</strong></div>
        <div className="pdi-top-actions">
          <input className="pdi-search" placeholder="Rechercher une commande…" />
          <span>Essai</span>
          <button className="pdi-account">Compte</button>
        </div>
      </header>

      <nav className="pdi-main-nav" aria-label="Navigation PD&I">
        {navItems.map((item) => (
          <button key={item.id} className={activeModule === item.id ? "active" : ""} onClick={() => setActiveModule(item.id)} title={item.title}>
            <span>{item.icon}</span><small>{item.label}</small>
          </button>
        ))}
      </nav>

      <main className="pdi-content">
        {activeModule === "home" && (
          <div className="pdi-home-hero">
            <section className="pdi-hero-card">
              <div className="pdi-badge-row"><span className="pdi-badge">SaaS autonome</span><span className="pdi-badge">JSON central</span><span className="pdi-badge">Python calculs</span><span className="pdi-badge">Agents spécialisés</span></div>
              <h1>Construire vos plans isométriques depuis toutes vos sources.</h1>
              <p>PD&I devient le logiciel principal : dessin manuel, Vision PD&I photo/croquis, import CAO/DXF/PDF, JSON central, exports et validation engineering.</p>
              <button className="pdi-start-primary" onClick={() => openModule("isometric")}>Nouveau projet isométrique</button>
              <div className="pdi-launch-grid">
                {launchCards.map((card) => (
                  <button key={card.id} className="pdi-launch-card" onClick={() => openModule(card.id)}>
                    <div className="icon">{card.icon}</div><h3>{card.title}</h3><p>{card.subtitle}</p><span className="badge">{card.ready ? "Disponible" : card.badge}</span>
                  </button>
                ))}
              </div>
            </section>
            <aside className="pdi-side-card">
              <h2>Architecture cible</h2>
              <ul>
                <li>Source → JSON PD&I → validation → ISO.</li>
                <li>Photo/croquis en cache local temporaire.</li>
                <li>Seul le JSON est conservé durablement.</li>
                <li>Calculs par Python, pas par IA générative.</li>
                <li>pipeline-design-skill = équipe d’agents spécialisés.</li>
                <li>PD&I = orchestrateur du workflow.</li>
              </ul>
            </aside>
          </div>
        )}

        {activeModule === "vision" && <ComingSoonPanel title="Vision PD&I"><p><b>Vision PD&I</b> préparera le flux <code>photo réelle → analyse agent → scripts Python → JSON PD&I → validation → ISO</code>. Les images restent en cache local temporaire navigateur et ne saturent pas le cloud.</p></ComingSoonPanel>}
        {activeModule === "sketch" && <ComingSoonPanel title="Croquis → JSON / ISO"><p>Import croquis main, reconnaissance lignes/symboles, conversion vers JSON central, validation humaine, puis génération ISO.</p></ComingSoonPanel>}
        {activeModule === "cad" && <ComingSoonPanel title="Import CAO / DXF / PDF"><p>Import DXF/PDF, lecture des calques et entités, conversion déterministe Python vers JSON PD&I.</p></ComingSoonPanel>}
        {activeModule === "json" && <ComingSoonPanel title="Modèle JSON PD&I"><p>Le JSON devient la source de vérité : lignes, nœuds, équipements, ports, soudures, cotations, niveaux Z, massifs, dalle, exports.</p></ComingSoonPanel>}
        {activeModule === "pdf" && <ComingSoonPanel title="Impression / Exports"><p>Préparation V4.8e : A4/A3/A2/A1, portrait/paysage, PDF, DXF/CAD, cartouche, nomenclature.</p></ComingSoonPanel>}
        {activeModule === "assistant" && <ComingSoonPanel title="Assistant et agents spécialisés"><p>PD&I orchestrera le repo <code>pipeline-design-skill</code> : agents Vision, Croquis, CAO, JSON, ISO, QA. Les agents proposent ; Python calcule.</p></ComingSoonPanel>}
      </main>
    </div>
  );
}
'''
    write_if_changed(UNIFIED_APP, content, report)


def patch_src_app(report: list[str]) -> None:
    if not SRC_APP.exists():
        report.append(f"KO {rel(SRC_APP)} absent")
        return
    content = '''import React from "react";
import PdiUnifiedApp from "./pdi/app/PdiUnifiedApp";

export default function App() {
  return <PdiUnifiedApp />;
}
'''
    write_if_changed(SRC_APP, content, report)


def patch_engine_main_mode(report: list[str]) -> None:
    if not ENGINE.exists():
        report.append(f"KO {rel(ENGINE)} absent")
        return
    text = read(ENGINE)
    original = text
    marker = "// PD&I PATCH 007c — ISO is the main workspace; home is handled by PdiUnifiedApp"
    if marker not in text:
        text = marker + "\n" + text

    # ISO doit redevenir le mode principal lorsqu'on y entre : pas d'affichage hors plein écran.
    text = re.sub(
        r'const \[workspaceFullscreen, setWorkspaceFullscreen\] = useState(?:<boolean>)?\((?:false|true)\);',
        'const [workspaceFullscreen, setWorkspaceFullscreen] = useState(true);',
        text,
        count=1,
    )

    # Transformer les libellés.
    text = text.replace("Quitter PD & I", "Retour accueil")
    text = text.replace("Quitter PD&I", "Retour accueil")
    text = text.replace("Quitter plein écran", "Retour accueil")
    text = text.replace("Mode intégré", "Retour accueil")
    text = text.replace("Plein écran", "Mode focus")

    # Remplacer l'action de sortie vers l'ancien affichage non fullscreen par navigation accueil.
    # Plusieurs variantes possibles selon patchs précédents.
    patterns = [
        r'onClick=\{\(\) => setWorkspaceFullscreen\(false\)\}',
        r'onClick=\{\(\) => \{\s*setWorkspaceFullscreen\(false\);?\s*\}\}',
    ]
    nav_action = 'onClick={() => window.dispatchEvent(new CustomEvent("pdi:navigate", { detail: "home" }))}'
    replaced = 0
    for pat in patterns:
        text, n = re.subn(pat, nav_action, text)
        replaced += n
    report.append(f"Engine: exit actions replaced={replaced}")

    # Si un bouton Retour accueil n'a pas été capturé, au moins l'état false n'est plus la sortie préférée.
    # On garde setWorkspaceFullscreen pour d'éventuels usages internes, mais l'entrée reste true.

    if text != original:
        write_if_changed(ENGINE, text, report)
    else:
        report.append(f"UNCHANGED {rel(ENGINE)}")


def patch_wrapper(report: list[str]) -> None:
    if not WRAPPER.exists():
        report.append(f"INFO {rel(WRAPPER)} absent")
        return
    text = read(WRAPPER)
    original = text
    marker = "// PD&I PATCH 007c — wrapper used as primary ISO workspace by unified shell"
    if marker not in text:
        text = marker + "\n" + text
    if text != original:
        write_if_changed(WRAPPER, text, report)
    else:
        report.append(f"UNCHANGED {rel(WRAPPER)}")


def write_docs(report: list[str]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    orchestrator = '''# PD&I — Orchestrateur et pipeline-design-skill

## Décision d'architecture

PD&I est l'application SaaS principale et l'orchestrateur du workflow piping.

Le dépôt `pipeline-design-skill` sera utilisé comme base d'agents spécialisés et de procédures techniques.
AS-DE-PIQUE pourra le consulter pour aider à auditer, orienter et préparer les intégrations.

## Rôle des agents

Les agents spécialisés facilitent le travail :

- Agent Vision PD&I : photo réelle → observations structurées ;
- Agent Croquis : croquis main → lignes/symboles/cotes ;
- Agent CAO : DXF/PDF → entités exploitables ;
- Agent JSON : consolidation du modèle PD&I ;
- Agent ISO : génération/validation isométrique ;
- Agent QA Engineering : contrôle règles métier.

## Règle calculs

Les calculs techniques ne sont pas faits par IA générative.

```txt
IA = reconnaissance, extraction, assistance, orchestration
Python = calculs déterministes, vérifiables, versionnés
```

Calculs Python : longueurs, cotes, pentes, coordonnées ISO, DN/NPS, BOM, poids, validation ports/soudures, DXF/PDF.

## Flux cible

```txt
Photo / Croquis / DXF / Manuel
→ agent spécialisé
→ script Python
→ JSON PD&I
→ validation humaine
→ ISO / PDF / DXF
```

## Stockage

Les photos/croquis/scans sont temporaires dans le navigateur.
Seul le JSON PD&I est conservé durablement par défaut.
'''
    write_if_changed(ORCHESTRATOR_DOC, orchestrator, report)

    history_add = '''

## Patch 007c — Shell unifié + accueil + ISO principal

Décision : arrêter la coexistence de deux logiciels (shell SaaS + ancien ISO intégré).

- PD&I devient un seul logiciel.
- La page d'accueil propose : nouveau projet, Vision PD&I, croquis, import DXF/PDF/JSON, exports.
- Le module ISO devient le workspace principal plein écran lorsqu'on le lance.
- Le bouton de sortie ISO devient `Retour accueil`.
- Le dépôt `pipeline-design-skill` est prévu comme équipe d'agents spécialisés.
- PD&I est l'orchestrateur ; les calculs techniques sont faits par Python.
'''
    old = read(PATCH_HISTORY)
    if "Patch 007c — Shell unifié" not in old:
        write_if_changed(PATCH_HISTORY, old.rstrip() + history_add + "\n", report)
    else:
        report.append(f"UNCHANGED {rel(PATCH_HISTORY)}")


def update_gitignore(report: list[str]) -> None:
    old = read(GITIGNORE)
    lines = old.splitlines()
    add = ["", "# PD&I patch backups", ".patch_backups/", "*.bak", "*.bak_*", "*.tmp", "*.old"]
    changed = False
    for line in add:
        if line not in lines:
            lines.append(line)
            changed = True
    if changed:
        write_if_changed(GITIGNORE, "\n".join(lines).rstrip() + "\n", report)
    else:
        report.append(f"UNCHANGED {rel(GITIGNORE)}")


def postcheck(report: list[str]) -> None:
    report.append("\n--- POST-CHECK 007c ---")
    for p in [SRC_APP, UNIFIED_APP, BRAND, WRAPPER, ENGINE, ORCHESTRATOR_DOC]:
        if p.exists():
            txt = read(p)
            report.append(f"OK {rel(p)} size={p.stat().st_size}")
            if p == ENGINE:
                report.append(f"  workspaceFullscreen true marker={txt.count('workspaceFullscreen, setWorkspaceFullscreen] = useState(true)')}")
                report.append(f"  Retour accueil count={txt.count('Retour accueil')}")
                report.append(f"  pdi:navigate count={txt.count('pdi:navigate')}")
            if p == UNIFIED_APP:
                report.append(f"  Vision PD&I count={txt.count('Vision PD&I')}")
                report.append(f"  PdiIsometricEditor count={txt.count('PdiIsometricEditor')}")
        else:
            report.append(f"KO {rel(p)} absent")


def main() -> int:
    report: list[str] = []
    report.append("PD&I PATCH 007c — Shell unifié + accueil + ISO principal")
    report.append(f"Date: {dt.datetime.now().isoformat()}")
    report.append(f"Root: {ROOT}")

    if not (ROOT / "package.json").exists():
        report.append("ERREUR: package.json introuvable. Exécuter depuis la racine du dépôt PD-I.")
        REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
        print("\n".join(report))
        return 2

    ensure_brand(report)
    write_unified_app(report)
    patch_src_app(report)
    patch_engine_main_mode(report)
    patch_wrapper(report)
    write_docs(report)
    update_gitignore(report)
    postcheck(report)

    report.append("\n--- TESTS RECOMMANDÉS ---")
    report.append("1. npm run build")
    report.append("2. npx tsc --noEmit si disponible")
    report.append("3. Ouvrir PD&I : voir l'accueil unique avec les cartes Nouveau projet / Vision / Croquis / DXF / JSON")
    report.append("4. Cliquer Dessin isométrique : l'ISO devient le workspace principal plein écran")
    report.append("5. Cliquer Retour accueil dans ISO : revenir à l'accueil")
    report.append("6. Vérifier : un seul logo global sur l'accueil ; plus deux logiciels visibles en même temps")
    report.append("7. Vérifier mobile : navigation horizontale et pas de double header")

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"\nRapport écrit: {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
