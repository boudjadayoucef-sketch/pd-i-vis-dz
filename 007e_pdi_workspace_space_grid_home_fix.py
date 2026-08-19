#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I PATCH 007e — Optimisation espace ISO + accueil carousel
=============================================================

À exécuter depuis la racine du dépôt PD-I :

    python3 007e_pdi_workspace_space_grid_home_fix.py

Corrige les réserves après tests 007d :
- enlever le bouton Retour / quitter mode plein écran dans le workspace ISO ;
- réduire la taille des compteurs bas : mètre tube, poids acier, volume épreuve, épreuve ;
- remonter "Vue isométrique 30°" dans la barre noire du haut ;
- supprimer la phrase d'aide "MAIN = déplacer..." pour gagner l'espace ;
- compléter la grille de l'éditeur pour couvrir toute la zone ;
- réduire les décalages visuels en recentrant mieux la grille et en gardant un canvas plein espace ;
- corriger le logo accueil avec une détection multi-chemins depuis /public ;
- remplacer le paragraphe "Architecture cible" par un bandeau/carousel à droite avec fonctionnalités PD&I.

Ce patch ne touche pas aux calculs ni au modèle piping.
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
from pathlib import Path

ROOT = Path.cwd()
PATCH_ID = "007e"
STAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT / f".patch_backups/{PATCH_ID}_{STAMP}"
REPORT = ROOT / f"patch_{PATCH_ID}_report.txt"

ENGINE = ROOT / "src/pdi/isometric/engine/IsometrieModuleV48d.tsx"
UNIFIED_APP = ROOT / "src/pdi/app/PdiUnifiedApp.tsx"
BRAND = ROOT / "src/pdi/app/PdiBrandMark.tsx"
DOCS = ROOT / "docs"
PATCH_HISTORY = DOCS / "PATCH_HISTORY.md"
PUBLIC = ROOT / "public"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


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


def detect_public_logo_paths(report: list[str]) -> tuple[list[str], list[str]]:
    candidates: list[Path] = []
    if PUBLIC.exists():
        for p in PUBLIC.rglob("*"):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                n = p.name.lower()
                if any(k in n for k in ["pdi", "pd-i", "pd_i", "logo", "pipeline"]):
                    candidates.append(p)

    def w(p: Path) -> str:
        return "/" + p.relative_to(PUBLIC).as_posix()

    # Priorité fichiers demandés.
    standard_h = ["/pdi-logo-horizontal.png", "/pdi-logo-horizontal.jpg", "/logo_pdi_horizontal.png", "/logo_pdi_horizontal.jpg", "/pdi_horizontal.png", "/pdi_horizontal.jpg"]
    standard_s = ["/pdi-logo-square.png", "/pdi-logo-square.jpg", "/logo_pdi_square.png", "/logo_pdi_square.jpg", "/pdi_square.png", "/pdi_square.jpg"]

    existing = [w(p) for p in candidates]
    h = [x for x in standard_h if (PUBLIC / x.lstrip("/")).exists()]
    s = [x for x in standard_s if (PUBLIC / x.lstrip("/")).exists()]
    h += [x for x in existing if any(k in x.lower() for k in ["horizontal", "wide", "header", "banner"])]
    s += [x for x in existing if any(k in x.lower() for k in ["square", "icon", "mark", "compact"])]
    h += existing
    s += existing

    # Dédupliquer + fallback chemins standards même si pas encore présents.
    def dedupe(xs: list[str], fallback: list[str]) -> list[str]:
        out = []
        for x in xs + fallback:
            if x not in out:
                out.append(x)
        return out

    h = dedupe(h, standard_h)
    s = dedupe(s, standard_s)
    report.append("Public logo candidates:")
    report.append(f"- detected images: {len(existing)}")
    for x in existing[:30]:
        report.append(f"  - {x}")
    report.append(f"- horizontal fallback list: {h[:8]}")
    report.append(f"- square fallback list: {s[:8]}")
    return h[:10], s[:10]


def write_brand(report: list[str]) -> None:
    horizontal, square = detect_public_logo_paths(report)
    content = f'''import React, {{ useState }} from "react";

// PD&I PATCH 007e — Logo robuste depuis /public avec fallbacks.
// Le logo n'est plus un SVG généré : il charge les images placées dans public/.
const HORIZONTAL_LOGOS = {horizontal!r};
const SQUARE_LOGOS = {square!r};

export type PdiBrandMarkProps = {{
  variant?: "horizontal" | "compact";
  size?: "sm" | "md" | "lg";
  className?: string;
}};

export default function PdiBrandMark({{
  variant = "horizontal",
  size = "md",
  className = "",
}}: PdiBrandMarkProps) {{
  const compact = variant === "compact";
  const logos = compact ? SQUARE_LOGOS : HORIZONTAL_LOGOS;
  const [idx, setIdx] = useState(0);
  const height = size === "sm" ? 38 : size === "lg" ? 70 : 52;
  const src = logos[Math.min(idx, logos.length - 1)];

  return (
    <div className={{`pdi-brand-mark ${{className}}`}} aria-label="PD&I — Piping Design & Isometrics">
      <img
        src={{src}}
        alt="PD&I — Piping Design & Isometrics"
        onError={{() => setIdx((value) => Math.min(value + 1, logos.length - 1))}}
        style={{{{
          height,
          width: compact ? height : undefined,
          maxWidth: compact ? height : "min(330px, 34vw)",
          objectFit: "contain",
          display: "block",
        }}}}
        draggable={{false}}
      />
    </div>
  );
}}
'''
    write_if_changed(BRAND, content, report)


def write_unified_app(report: list[str]) -> None:
    if not UNIFIED_APP.exists():
        report.append(f"WARN {rel(UNIFIED_APP)} absent, création d'une version complète")
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

const showcase = [
  { title: "Dessin isométrique", text: "Workspace plein écran, cotations, alignements et bibliothèque piping.", tag: "ISO", color: "#0ea5e9" },
  { title: "Vision PD&I", text: "Photo réelle → JSON piping → validation → ISO.", tag: "VISION", color: "#f97316" },
  { title: "Croquis", text: "Croquis main → reconnaissance → modèle PD&I.", tag: "CROQUIS", color: "#8b5cf6" },
  { title: "CAO / DXF", text: "Importer dessins techniques et convertir vers JSON.", tag: "DXF", color: "#22c55e" },
  { title: "Exports", text: "PDF, DXF, impression A4/A3/A2/A1 et cartouche.", tag: "PDF", color: "#eab308" },
  { title: "Agents spécialisés", text: "pipeline-design-skill branché à PD&I orchestrateur.", tag: "AGENTS", color: "#06b6d4" },
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
  return <section className="pdi-module-panel"><div className="pdi-panel-kicker">Module préparé</div><h1>{title}</h1><div className="pdi-panel-body">{children}</div></section>;
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

  if (activeModule === "isometric") return <PdiIsometricEditor />;

  return (
    <div className="pdi-unified-root">
      <style>{`
        .pdi-unified-root{height:100vh;width:100vw;overflow:hidden;background:#070B12;color:#E5EDF8;font-family:Inter,ui-sans-serif,system-ui,sans-serif;display:grid;grid-template-columns:96px 1fr;grid-template-rows:72px 1fr}.pdi-unified-topbar{grid-column:1/3;display:flex;align-items:center;gap:18px;padding:8px 16px;background:linear-gradient(180deg,#111827,#0B1019);border-bottom:1px solid rgba(148,163,184,.22);box-shadow:0 8px 24px rgba(0,0,0,.28);min-width:0}.pdi-unified-brand{display:flex;align-items:center;gap:14px;min-width:260px}.pdi-project-title{min-width:0;border-left:1px solid rgba(148,163,184,.28);padding-left:14px;line-height:1.1}.pdi-project-title small{display:block;color:#8EA3C2;font-size:10px;text-transform:uppercase;font-weight:900}.pdi-project-title strong{display:block;color:#F8FAFC;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pdi-top-actions{margin-left:auto;display:flex;align-items:center;gap:8px;color:#93A4BD;font-size:12px}.pdi-search{height:36px;width:min(340px,24vw);border:1px solid rgba(148,163,184,.22);background:#0A1220;color:#E5EDF8;border-radius:10px;padding:0 12px;font-weight:800}.pdi-account{height:36px;border:1px solid rgba(34,211,238,.35);background:#0A1220;color:#F8FAFC;border-radius:10px;padding:0 12px;font-weight:900}.pdi-main-nav{grid-row:2;display:flex;flex-direction:column;gap:10px;padding:14px 10px;background:linear-gradient(180deg,#0D1420,#090E17);border-right:1px solid rgba(148,163,184,.18);overflow:auto}.pdi-main-nav button{height:58px;border:1px solid rgba(148,163,184,.16);background:#111827;color:#BBD0EA;border-radius:14px;font-weight:1000;font-size:13px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer}.pdi-main-nav button.active{background:linear-gradient(135deg,#0284C7,#0EA5E9);color:white;border-color:#67E8F9;box-shadow:0 0 0 1px rgba(103,232,249,.55),0 16px 35px rgba(14,165,233,.25)}.pdi-main-nav small{font-size:8px;letter-spacing:.06em;text-transform:uppercase;opacity:.82}.pdi-content{grid-column:2;grid-row:2;min-width:0;min-height:0;overflow:auto;padding:22px;background:radial-gradient(circle at 18% 8%,rgba(14,165,233,.16),transparent 32%),radial-gradient(circle at 86% 12%,rgba(249,115,22,.13),transparent 28%),#070B12}.pdi-home-hero{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(310px,.75fr);gap:20px;align-items:stretch}.pdi-hero-card,.pdi-module-panel,.pdi-launch-card,.pdi-showcase-card{border:1px solid rgba(148,163,184,.18);background:linear-gradient(180deg,rgba(15,23,42,.92),rgba(8,13,24,.96));border-radius:24px;box-shadow:0 24px 70px rgba(0,0,0,.28)}.pdi-hero-card{padding:28px}.pdi-hero-card h1,.pdi-module-panel h1{font-size:clamp(28px,4vw,54px);line-height:.95;margin:0;color:#F8FAFC;letter-spacing:-.04em}.pdi-hero-card p{color:#B9C8DD;font-weight:700;max-width:760px}.pdi-badge-row{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.pdi-badge{border:1px solid rgba(103,232,249,.28);background:rgba(8,145,178,.12);color:#67E8F9;border-radius:999px;padding:7px 10px;font-size:11px;font-weight:1000;text-transform:uppercase}.pdi-launch-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:20px}.pdi-launch-card{padding:18px;text-align:left;color:#E5EDF8;cursor:pointer;transition:.18s transform,.18s border-color}.pdi-launch-card:hover{transform:translateY(-2px);border-color:#38BDF8}.pdi-launch-card .icon{width:54px;height:54px;border-radius:16px;display:grid;place-items:center;background:#0EA5E9;color:white;font-weight:1000;margin-bottom:12px}.pdi-launch-card h3{margin:0 0 8px;font-size:18px}.pdi-launch-card p{margin:0;color:#9FB0C8;font-size:12px;font-weight:700}.pdi-launch-card .badge{display:inline-block;margin-top:12px;color:#FDE68A;font-size:10px;font-weight:1000;text-transform:uppercase}.pdi-showcase{height:calc(100vh - 132px);overflow:hidden;position:relative}.pdi-showcase-track{display:flex;flex-direction:column;gap:14px;animation:pdiShowcaseScroll 22s linear infinite}.pdi-showcase-card{min-height:150px;padding:18px;position:relative;overflow:hidden}.pdi-showcase-card::before{content:"";position:absolute;inset:auto -30px -45px auto;width:150px;height:150px;border-radius:999px;background:var(--accent);opacity:.23;filter:blur(4px)}.pdi-showcase-card .tag{display:inline-grid;place-items:center;min-width:58px;height:38px;border-radius:12px;background:var(--accent);color:white;font-size:11px;font-weight:1000}.pdi-showcase-card h3{margin:16px 0 8px;font-size:21px}.pdi-showcase-card p{margin:0;color:#B9C8DD;font-weight:750;font-size:13px;line-height:1.45}@keyframes pdiShowcaseScroll{0%{transform:translateY(0)}100%{transform:translateY(-50%)}}.pdi-module-panel{padding:28px;min-height:calc(100vh - 128px)}.pdi-panel-kicker{color:#67E8F9;font-size:11px;text-transform:uppercase;font-weight:1000;margin-bottom:10px}.pdi-panel-body{margin-top:20px;color:#B9C8DD;font-weight:750;line-height:1.75;max-width:980px}.pdi-panel-body code{background:#111827;border:1px solid rgba(148,163,184,.18);border-radius:8px;padding:3px 6px;color:#FDE68A}.pdi-start-primary{border:0;background:linear-gradient(135deg,#0284C7,#22D3EE);color:white;border-radius:16px;padding:14px 18px;font-weight:1000;cursor:pointer;box-shadow:0 18px 45px rgba(14,165,233,.28)}@media(max-width:900px){.pdi-unified-root{grid-template-columns:1fr;grid-template-rows:72px auto 1fr}.pdi-unified-topbar{grid-column:1}.pdi-project-title,.pdi-search{display:none}.pdi-main-nav{grid-row:2;flex-direction:row;overflow-x:auto;padding:8px}.pdi-main-nav button{min-width:72px;height:54px}.pdi-content{grid-column:1;grid-row:3;padding:12px}.pdi-home-hero{grid-template-columns:1fr}.pdi-launch-grid{grid-template-columns:1fr}.pdi-showcase{height:360px}}
      `}</style>
      <header className="pdi-unified-topbar"><div className="pdi-unified-brand"><PdiBrandMark variant="horizontal" size="sm" /></div><div className="pdi-project-title"><small>Projet actif</small><strong>{moduleTitle}</strong></div><div className="pdi-top-actions"><input className="pdi-search" placeholder="Rechercher une commande…" /><span>Essai</span><button className="pdi-account">Compte</button></div></header>
      <nav className="pdi-main-nav" aria-label="Navigation PD&I">{navItems.map((item) => <button key={item.id} className={activeModule === item.id ? "active" : ""} onClick={() => setActiveModule(item.id)} title={item.title}><span>{item.icon}</span><small>{item.label}</small></button>)}</nav>
      <main className="pdi-content">
        {activeModule === "home" && <div className="pdi-home-hero"><section className="pdi-hero-card"><div className="pdi-badge-row"><span className="pdi-badge">SaaS autonome</span><span className="pdi-badge">JSON central</span><span className="pdi-badge">Python calculs</span><span className="pdi-badge">Agents spécialisés</span></div><h1>Construire vos plans isométriques depuis toutes vos sources.</h1><p>PD&I devient le logiciel principal : dessin manuel, Vision PD&I photo/croquis, import CAO/DXF/PDF, JSON central, exports et validation engineering.</p><button className="pdi-start-primary" onClick={() => setActiveModule("isometric")}>Nouveau projet isométrique</button><div className="pdi-launch-grid">{launchCards.map((card) => <button key={card.id} className="pdi-launch-card" onClick={() => setActiveModule(card.id)} title={card.title}><div className="icon">{card.icon}</div><h3>{card.title}</h3><p>{card.subtitle}</p><span className="badge">{card.ready ? "Disponible" : card.badge}</span></button>)}</div></section><aside className="pdi-showcase"><div className="pdi-showcase-track">{[...showcase, ...showcase].map((item, index) => <div key={`${item.tag}-${index}`} className="pdi-showcase-card" style={{ "--accent": item.color } as React.CSSProperties}><span className="tag">{item.tag}</span><h3>{item.title}</h3><p>{item.text}</p></div>)}</div></aside></div>}
        {activeModule === "vision" && <ComingSoonPanel title="Vision PD&I"><p><b>Vision PD&I</b> préparera le flux <code>photo réelle → analyse agent → scripts Python → JSON PD&I → validation → ISO</code>. Les images restent en cache local temporaire navigateur.</p></ComingSoonPanel>}
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


def patch_engine(report: list[str]) -> None:
    if not ENGINE.exists():
        report.append(f"KO {rel(ENGINE)} absent")
        return
    text = read(ENGINE)
    original = text
    marker = "// PD&I PATCH 007e — workspace space/grid/home corrections"
    if marker not in text:
        text = marker + "\n" + text

    # Enlever boutons retour/quitter/mode intégré injectés dans les patchs précédents.
    text, n_return_block = re.subn(r'\s*<button\s+[^>]*className="pdi-return-home-007d[\s\S]*?</button>', '', text, flags=re.S)
    text, n_return_block2 = re.subn(r'\s*<button\s+[^>]*title="Retour accueil PD&I"[\s\S]*?</button>', '', text, flags=re.S)
    report.append(f"Engine: return buttons removed={n_return_block+n_return_block2}")

    # ISO mode principal.
    text, n_state = re.subn(
        r'const \[workspaceFullscreen, setWorkspaceFullscreen\] = useState(?:<boolean>)?\((?:true|false)\);',
        'const [workspaceFullscreen, setWorkspaceFullscreen] = useState(true);',
        text,
        count=1,
    )
    report.append(f"Engine: workspaceFullscreen true replacements={n_state}")

    # Masquer le bandeau descriptif et la toolbar claire hors plein écran.
    text = text.replace('className={`${workspaceFullscreen ? "hidden" : ""} bg-slate-950 border border-slate-800 rounded-2xl px-4 py-3 text-white shadow-lg`}', 'className="hidden"')
    text = text.replace('className={`${workspaceFullscreen ? "hidden" : "sticky"} top-2 z-40 bg-white/95 backdrop-blur border border-slate-200 rounded-xl shadow-sm px-2 py-2 flex-wrap items-center justify-between gap-2 ${workspaceFullscreen ? "" : "flex"}`}', 'className="hidden"')

    # Supprimer / masquer la ligne aide MAIN = déplacer...
    text, n_help = re.subn(
        r'<div className="text-\[10px\] text-slate-400 flex flex-wrap items-center gap-2 mb-2">[\s\S]*?<b className="text-amber-300">[\s\S]*?</b>\s*</div>',
        '',
        text,
        count=1,
    )
    report.append(f"Engine: help phrase block removed={n_help}")

    # Compléter la grille : augmenter nombre de lignes et étendre hors viewBox.
    text = text.replace('Array.from({ length: 30 })', 'Array.from({ length: 72 })')
    text = text.replace('x1={i * 35 - 250}', 'x1={i * 35 - 900}')
    text = text.replace('x2={i * 35 + 50}', 'x2={i * 35 + 500}')
    text = text.replace('x1={i * 35 + 250}', 'x1={i * 35 + 900}')
    text = text.replace('x2={i * 35 - 50}', 'x2={i * 35 - 500}')
    text = text.replace('y2="400"', 'y2="520"')

    # Insérer "Vue isométrique 30°" dans topbar noire si absent.
    if "pdi-top-iso-title-007e" not in text:
        # Ajouter après le bloc projet actif si possible, sinon après header.
        insert = '''
              <div className="pdi-top-iso-title-007e hidden lg:flex items-center gap-2 rounded-md border border-slate-700 bg-slate-950/60 px-3 py-1 text-[10px] font-black uppercase text-cyan-200" title="Vue isométrique 30°">
                ↗ Vue isométrique 30° · {Math.round(viewport.zoom * 100)}%
              </div>'''
        anchor = '</div>\n            </div>\n            <nav className="pdi-cad-menubar'
        if anchor in text:
            text = text.replace('</div>\n            </div>\n            <nav className="pdi-cad-menubar', '</div>' + insert + '\n            </div>\n            <nav className="pdi-cad-menubar', 1)
            report.append("Engine: top iso title inserted before menu nav")
        else:
            text, n_top = re.subn(r'(<header className="pdi-studio-topbar[\s\S]*?>)', r'\1' + insert, text, count=1)
            report.append(f"Engine: top iso title inserted fallback={n_top}")

    # Cacher le titre local Vue isométrique dans la carte éditeur pour gagner de la place (gardons les boutons).
    text = text.replace('<Maximize2 className="w-4 h-4 text-blue-400" />', '<Maximize2 className="hidden" />')
    text = text.replace('<span className="text-xs font-black uppercase">\n                  Vue isométrique 30°\n                </span>', '<span className="hidden">Vue isométrique 30°</span>')

    # CSS compact : stats bas + no-scroll + canvas plus haut + tooltips.
    css = '''
        [data-pdi-studio] .pdi-compact-metrics, [data-pdi-studio] .pdi-metric-card{min-height:52px!important;padding:8px 10px!important;border-radius:14px!important}
        [data-pdi-studio] .pdi-compact-metrics h3, [data-pdi-studio] .pdi-metric-card h3{font-size:9px!important;margin:0!important}
        [data-pdi-studio] .pdi-compact-metrics strong, [data-pdi-studio] .pdi-metric-card strong{font-size:18px!important;line-height:1!important}
        [data-pdi-studio] button[title]{position:relative}
        [data-pdi-studio] button[title]:hover::after{content:attr(title);position:absolute;left:50%;top:calc(100% + 8px);transform:translateX(-50%);z-index:10080;min-width:max-content;max-width:260px;padding:6px 8px;border-radius:8px;background:#020617;color:#E6EDF3;border:1px solid rgba(103,232,249,.35);box-shadow:0 14px 35px rgba(0,0,0,.45);font-size:10px;font-weight:900;white-space:nowrap;pointer-events:none}
        [data-pdi-studio] .pdi-status-docked{height:28px!important;min-height:28px!important;padding-top:3px!important;padding-bottom:3px!important}
'''
    if "pdi-compact-metrics" not in text:
        text = text.replace('      `}</style>', css + '      `}</style>', 1)
        report.append("Engine: compact workspace CSS added")

    # Essayer de marquer les cartes métriques existantes avec une classe si on trouve leurs titres.
    metric_words = ["MÈTRE TUBE", "METRE TUBE", "POIDS ACIER", "VOLUME ÉPREUVE", "VOLUME EPREUVE", "ÉPREUVE", "EPREUVE"]
    if "pdi-compact-metrics" not in text:
        for word in metric_words:
            if word in text:
                # CSS globale suffira si structure non connue.
                pass

    # Éviter scroll root.
    text = text.replace('overflow-auto bg-[#0B0F14]', 'overflow-hidden bg-[#0B0F14]')

    if text != original:
        write_if_changed(ENGINE, text, report)
    else:
        report.append(f"UNCHANGED {rel(ENGINE)}")


def write_docs(report: list[str]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    add = '''

## Patch 007e — Optimisation espace ISO + accueil carousel

Correctifs :
- retirer le bouton retour/quitter du workspace ISO ;
- garder l'ISO comme workspace principal plein écran ;
- réduire l'encombrement des compteurs bas ;
- déplacer l'information `Vue isométrique 30°` vers la barre noire du haut ;
- supprimer la phrase d'aide `MAIN = déplacer...` dans le workspace ;
- compléter la grille pour couvrir toute la zone ;
- remplacer le bloc `Architecture cible` de l'accueil par un carousel vertical de fonctionnalités ;
- rendre le logo accueil robuste avec plusieurs chemins `/public`.
'''
    old = read(PATCH_HISTORY)
    if "Patch 007e — Optimisation espace ISO" not in old:
        write_if_changed(PATCH_HISTORY, old.rstrip() + add + "\n", report)
    else:
        report.append(f"UNCHANGED {rel(PATCH_HISTORY)}")


def postcheck(report: list[str]) -> None:
    report.append("\n--- POST-CHECK 007e ---")
    if ENGINE.exists():
        t = read(ENGINE)
        report.append(f"Engine workspaceFullscreen true: {t.count('workspaceFullscreen, setWorkspaceFullscreen] = useState(true)')}")
        report.append(f"Engine return buttons: {t.count('pdi-return-home-007d') + t.count('Retour accueil PD&I')}")
        report.append(f"Engine help phrase MAIN: {t.count('MAIN = déplacer la feuille')}")
        report.append(f"Engine grid length 72: {t.count('Array.from({ length: 72 })')}")
        report.append(f"Engine top iso title: {t.count('pdi-top-iso-title-007e')}")
    if UNIFIED_APP.exists():
        u = read(UNIFIED_APP)
        report.append(f"Unified Architecture cible: {u.count('Architecture cible')}")
        report.append(f"Unified showcase: {u.count('pdi-showcase')}")
    if BRAND.exists():
        b = read(BRAND)
        report.append(f"Brand img tags: {b.count('<img')}")
        report.append(f"Brand fallback arrays: {b.count('HORIZONTAL_LOGOS')}")


def main() -> int:
    report: list[str] = []
    report.append("PD&I PATCH 007e — Optimisation espace ISO + accueil carousel")
    report.append(f"Date: {dt.datetime.now().isoformat()}")
    report.append(f"Root: {ROOT}")

    if not (ROOT / "package.json").exists():
        report.append("ERREUR: package.json introuvable. Exécute ce patch depuis la racine du dépôt PD-I.")
        REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
        print("\n".join(report))
        return 2

    write_brand(report)
    write_unified_app(report)
    patch_engine(report)
    write_docs(report)
    postcheck(report)

    report.append("\n--- TESTS RECOMMANDÉS ---")
    report.append("1. npm run build")
    report.append("2. Accueil : logo visible, plus de bloc Architecture cible, carousel fonctionnalités à droite")
    report.append("3. ISO : pas de bouton retour/quitter, pas de scroll page")
    report.append("4. ISO : barre menus en haut visible, Vue isométrique 30° remonté en topbar")
    report.append("5. ISO : phrase MAIN supprimée")
    report.append("6. ISO : compteurs bas plus petits")
    report.append("7. ISO : grille couvre toute la zone, retester dessin segment/nœuds")

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"\nRapport écrit: {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
