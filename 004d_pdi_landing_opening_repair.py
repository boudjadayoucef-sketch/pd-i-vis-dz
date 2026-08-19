#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 004d
Réparation de la landing page et de la page d’ouverture.

Workflow : AI Studio d’abord, patch .py idempotent, tests, ZIP synchronisé,
puis GitHub uniquement après validation explicite.
"""

from pathlib import Path
import shutil
import sys
from datetime import datetime

PATCH_ID = "004d"
ROOT = Path(".")
APP = ROOT / "src" / "pdi" / "app" / "PdiUnifiedApp.tsx"
LANDING_DIR = ROOT / "src" / "pdi" / "landing"
LANDING_TSX = LANDING_DIR / "PdiLandingV4.tsx"
LANDING_CSS = LANDING_DIR / "pdiLandingV4.css"
ENGINE = ROOT / "src" / "pdi" / "isometric" / "engine" / "IsometrieModuleV48d.tsx"
REPORT = ROOT / "004d_landing_opening_repair_REPORT.md"
HISTORY = ROOT / "docs" / "PATCH_HISTORY.md"

GUARD_TSX = "PATCH 004d — landing opening repair"
GUARD_CSS = "PATCH 004d — restauration page d'ouverture"


def fail(message: str) -> None:
    print(f"ABANDON : {message}")
    sys.exit(2)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def backup_once(path: Path) -> None:
    if not path.exists():
        return
    backup = path.with_name(path.name + f".before{PATCH_ID}")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"Sauvegarde créée : {backup}")


def assert_project() -> None:
    if not APP.exists():
        fail(f"fichier introuvable : {APP}")
    if not ENGINE.exists():
        fail(f"moteur V4.8d introuvable : {ENGINE}")
    if not LANDING_TSX.exists():
        fail(f"landing introuvable : {LANDING_TSX}")
    if not LANDING_CSS.exists():
        fail(f"CSS landing introuvable : {LANDING_CSS}")

    engine_src = read(ENGINE)
    if "IsometrieModule" not in engine_src:
        fail("le fichier moteur ne semble pas être V4.8d")

    print("Audit initial OK.")


def patch_unified_app() -> None:
    src = read(APP)

    if "const enterApp = React.useCallback((target?: string)" in src and "allowed.includes(target as PdiModule)" in src:
        print("PdiUnifiedApp.tsx déjà compatible avec entrée ciblée.")
        return

    backup_once(APP)

    old = '''const enterApp = React.useCallback(() => {
    try {
      window.sessionStorage.setItem(PDI_STAGE_KEY, "app");
    } catch {
      /* stockage indisponible : l'entree reste valable pour l'affichage courant */
    }
    setStage("app");
    setActiveModule("home");
    window.scrollTo(0, 0);
  }, []);'''

    new = '''const enterApp = React.useCallback((target?: string) => {
    try {
      window.sessionStorage.setItem(PDI_STAGE_KEY, "app");
    } catch {
      /* stockage indisponible : l'entree reste valable pour l'affichage courant */
    }
    setStage("app");

    // PATCH 004d : la landing / page d'ouverture peut maintenant envoyer
    // directement vers le module choisi, sans casser le comportement existant.
    const allowed: PdiModule[] = [
      "home",
      "isometric",
      "vision",
      "sketch",
      "cad",
      "json",
      "pdf",
      "projects",
      "assistant",
    ];

    setActiveModule(allowed.includes(target as PdiModule) ? (target as PdiModule) : "home");
    window.scrollTo(0, 0);
  }, []);'''

    if old not in src:
        fail("ancre enterApp non trouvée dans PdiUnifiedApp.tsx — audit manuel nécessaire")

    write(APP, src.replace(old, new))
    print("PdiUnifiedApp.tsx patché.")


def patch_landing_tsx() -> None:
    src = read(LANDING_TSX)

    if GUARD_TSX in src:
        print("PdiLandingV4.tsx déjà patché 004d.")
        return

    backup_once(LANDING_TSX)

    src = src.replace(
        'import React, { useEffect, useState } from "react";',
        'import React, { useEffect, useMemo, useState } from "react";',
    )

    src = src.replace(
        '''export type PdiLandingV4Props = {
  /** Appele pour entrer dans le logiciel (connexion / demarrage). */
  onEnter: () => void;
};''',
        '''export type PdiLandingV4Props = {
  /** Appele pour entrer dans le logiciel (connexion / demarrage). */
  onEnter: (target?: string) => void;
};''',
    )

    boot_and_entries = r'''
// PATCH 004d — landing opening repair.
// Séquence complète : splash -> accueil -> boot -> launcher -> module.
const BOOT_STEPS = [
  "Authentification de la session PD&I",
  "Chargement du moteur isométrique V4.8d",
  "Initialisation du JSON central",
  "Montage des calculs Python déterministes",
  "Réveil des agents IA spécialisés",
  "Chargement du catalogue tuyauterie",
  "Vérification ISO / ASME B31.3",
  "Espace de travail prêt",
];

const ENTRY_POINTS = [
  { id: "isometric", title: "Nouveau Plan", sub: "Dessin isométrique manuel", badge: "Recommandé", icon: "ISO", color: "#4db8d4", text: "Démarrer un projet vierge : nœuds, tubes, accessoires, cotations et alignements." },
  { id: "cad", title: "CAD to ISO", sub: "DXF / DWG → isométrique", badge: "DXF · DWG", icon: "CAD", color: "#4db8d4", text: "Convertir un dessin CAO en modèle PD&I puis en planche isométrique normée." },
  { id: "vision", title: "Vision AI — Photo to ISO", sub: "Photo réelle → JSON → ISO", badge: "IA", icon: "VIS", color: "#e8a838", text: "Reconnaissance IA de la tuyauterie sur photo de site, validation puis génération ISO." },
  { id: "sketch", title: "Croquis to ISO", sub: "Croquis main → isométrique", badge: "Croquis", icon: "CRQ", color: "#e8a838", text: "Redresser un croquis, détecter lignes et symboles, produire un ISO propre." },
  { id: "json", title: "Importer JSON", sub: "JSON PD&I existant", badge: "Reprise", icon: "{}", color: "#4caf7d", text: "Reprendre un modèle PD&I : graphe, soudures, cotes et métré restaurés à l’identique." },
  { id: "cad", title: "Importer CAD / PDF", sub: "Import de fond de plan", badge: "Import", icon: "PDF", color: "#4db8d4", text: "Charger un DXF/DWG/PDF comme support de tracé avec mapping des calques." },
  { id: "home", title: "Ouvrir un projet", sub: "Projets récents du compte", badge: "Récents", icon: "CLK", color: "#888888", text: "Reprendre un projet existant là où il s’est arrêté, avec son historique." },
  { id: "pdf", title: "Exports & BOM", sub: "PDF / DXF / nomenclature", badge: "Export", icon: "OUT", color: "#4caf7d", text: "Produire planches A4→A1, cartouche, nomenclature matériaux et métré." },
];
'''

    if "const BOOT_STEPS =" not in src:
        src = src.replace("const NAV_LINKS = [", boot_and_entries + "\nconst NAV_LINKS = [")

    start = src.find("export default function PdiLandingV4")
    if start == -1:
        fail("fonction PdiLandingV4 introuvable")

    replacement = r'''export default function PdiLandingV4({ onEnter }: PdiLandingV4Props) {
  const [screen, setScreen] = useState<"landing" | "home" | "loading" | "launcher">("landing");
  const [stuck, setStuck] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [bootIndex, setBootIndex] = useState(0);
  const [selectedEntry, setSelectedEntry] = useState<string | null>("isometric");

  useEffect(() => {
    const onScroll = () => setStuck(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (screen !== "loading") return;
    if (bootIndex >= BOOT_STEPS.length - 1) {
      const done = window.setTimeout(() => setScreen("launcher"), 950);
      return () => window.clearTimeout(done);
    }
    const timer = window.setTimeout(() => setBootIndex((v) => v + 1), 520);
    return () => window.clearTimeout(timer);
  }, [screen, bootIndex]);

  const goto = (id: string) => {
    setMenuOpen(false);
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const begin = () => {
    setMenuOpen(false);
    setBootIndex(0);
    setScreen("loading");
  };

  const openEntry = (id?: string | null) => onEnter(id || "home");
  const progress = useMemo(() => Math.round(((bootIndex + 1) / BOOT_STEPS.length) * 100), [bootIndex]);

  if (screen === "loading") {
    return (
      <div className="pdiL-boot">
        <button className="pdiL-boot-skip" onClick={() => setScreen("launcher")} title="Passer">×</button>
        <div className="pdiL-boot-glow" />
        <div className="pdiL-boot-brand"><span className="pdiL-brand-dot">PD</span><div><b>PD&amp;I</b><small>Pipeline Design &amp; Isometrics</small></div></div>
        <div className="pdiL-boot-steps">
          {BOOT_STEPS.map((step, i) => <div key={step} className={i < bootIndex ? "done" : i === bootIndex ? "now" : "todo"}><span>{i < bootIndex ? "✓" : i === bootIndex ? "◌" : "•"}</span><b>{step}</b></div>)}
        </div>
        <div className="pdiL-bootbar"><i style={{ width: `${progress}%` }} /></div>
        <div className="pdiL-bootpct">{progress}% · ouverture du logiciel</div>
        <div className="pdiL-powered">Powered by DZ-YSB-DEV</div>
      </div>
    );
  }

  if (screen === "launcher") {
    return (
      <div className="pdiL-launcher">
        <header className="pdiL-launcher-head"><div className="pdiL-brand"><span className="pdiL-brand-dot">PD</span><span>PD&amp;I</span></div><span className="pdiL-session"><i /> Session connectée</span><button onClick={() => setScreen("home")}>Retour</button></header>
        <main className="pdiL-launcher-body">
          <span className="pdiL-kicker">Ouverture du logiciel</span>
          <h1>Par où commence votre isométrique&nbsp;?</h1>
          <p>Choisissez un point d’entrée. Toutes les voies aboutissent au même JSON PD&amp;I — la vérité technique du projet.</p>
          <div className="pdiL-entry-grid">
            {ENTRY_POINTS.map((entry) => <button key={`${entry.id}-${entry.title}`} className={selectedEntry === entry.id ? "pdiL-entry selected" : "pdiL-entry"} style={{ "--entry": entry.color } as React.CSSProperties} onClick={() => setSelectedEntry(entry.id)} onDoubleClick={() => openEntry(entry.id)}><span className="pdiL-entry-top"><b>{entry.icon}</b><em>{entry.badge}</em></span><strong>{entry.title}</strong><small>{entry.sub}</small><p>{entry.text}</p><span className="pdiL-entry-go">Choisir →</span></button>)}
          </div>
          <div className="pdiL-launch-actions"><button className="pdiL-btn pdiL-btn-primary pdiL-btn-lg" onClick={() => openEntry(selectedEntry)}>Ouvrir · {ENTRY_POINTS.find((x) => x.id === selectedEntry)?.title || "Accueil"}</button><span>Astuce : double-cliquez une carte pour ouvrir directement</span></div>
        </main>
        <footer className="pdiL-launcher-foot">ISO / ASME B31.3 · Calculs Python déterministes · JSON central · Powered by DZ-YSB-DEV</footer>
      </div>
    );
  }

  if (screen === "home") {
    return (
      <div className="pdiL-root">
        <div className="pdiL-navhost">
          <nav className={stuck ? "pdiL-nav is-stuck" : "pdiL-nav"} aria-label="Navigation PD&I">
            <div className="pdiL-brand"><span className="pdiL-brand-dot">PD</span><span>PD&amp;I</span></div>
            <div className="pdiL-navlinks">{NAV_LINKS.map((link) => <button key={link.id} type="button" className="pdiL-navlink" onClick={() => goto(link.id)}>{link.label}</button>)}</div>
            <div className="pdiL-navactions"><button type="button" className="pdiL-btn pdiL-btn-ghost" onClick={begin}>Connexion</button><button type="button" className="pdiL-btn pdiL-btn-primary" onClick={begin}>Démarrer</button></div>
            <button type="button" className="pdiL-burger" aria-label="Ouvrir le menu" aria-expanded={menuOpen} onClick={() => setMenuOpen((v) => !v)}>{menuOpen ? "×" : "☰"}</button>
          </nav>
          <div className={menuOpen ? "pdiL-mobilemenu is-open" : "pdiL-mobilemenu"}>{NAV_LINKS.map((link) => <button key={link.id} type="button" className="pdiL-navlink" onClick={() => goto(link.id)}>{link.label}</button>)}<button type="button" className="pdiL-btn pdiL-btn-ghost" onClick={begin}>Connexion</button><button type="button" className="pdiL-btn pdiL-btn-primary" onClick={begin}>Démarrer</button></div>
        </div>
        <header className="pdiL-homehero"><div><span className="pdiL-kicker">Accueil PD&amp;I</span><h1>Construire vos plans isométriques depuis toutes vos sources.</h1><p>Le logiciel principal : dessin manuel, Vision PD&amp;I photo/croquis, import CAO/DXF/PDF, JSON central, exports et validation engineering.</p><button className="pdiL-btn pdiL-btn-primary pdiL-btn-lg" onClick={() => setScreen("launcher")}>Nouveau projet isométrique</button></div></header>
        {landingSections(begin)}
      </div>
    );
  }

  return (
    <div className="pdiL-hero-shell">
      <div className="pdiL-hero-bg"><span /><span /><span /><span /><span /><span /></div>
      <div className="pdiL-hero-grid" />
      <section className="pdiL-splash">
        <div className="pdiL-brand pdiL-splash-brand"><span className="pdiL-brand-dot">PD</span><div><b>PD&amp;I</b><small>Pipeline Design &amp; Isometrics</small></div></div>
        <h1>Du croquis à l’isométrique normé,<br /><em>PD&amp;I dessine votre tuyauterie.</em></h1>
        <p>Photo, P&amp;ID ou croquis → reconnaissance IA, topologie, soudures, cotations, métré et BOM. Un seul JSON comme vérité technique, un ISO prêt à signer.</p>
        <button className="pdiL-hero-button" onClick={() => setScreen("home")}>Let’s begin →</button>
        <div className="pdiL-hero-meta"><span>ISO / ASME B31.3</span><i /><span>Calculs Python déterministes</span><i /><span>JSON central</span><i /><span>Agents IA spécialisés</span></div>
      </section>
      <div className="pdiL-powered">Powered by DZ-YSB-DEV</div>
    </div>
  );
}

function landingSections(begin: () => void) {
  return <>
    <div className="pdiL-band" id="fonctions">{BAND.map((cell) => <div key={cell.key} className={"pdiL-bandcell " + cell.cls}><b>{cell.title}</b><span>{cell.text}</span></div>)}</div>
    <section className="pdiL-sec" id="temps"><div className="pdiL-wrap"><div className="pdiL-seclabel">Methode</div><h2>PD&amp;I en 4 temps</h2><p className="pdiL-lead">Une chaine unique, de la source réelle jusqu'au dossier d'exécution.</p><div className="pdiL-steps">{STEPS.map((step) => <div key={step.n} className={"pdiL-step " + step.cls}><div className="pdiL-stepnum">{step.n}</div><h3>{step.title}</h3><p>{step.text}</p></div>)}</div></div></section>
    <section className="pdiL-sec" id="modules"><div className="pdiL-wrap"><div className="pdiL-seclabel">Capacites</div><h2>Ce que fait le logiciel</h2><p className="pdiL-lead">Un moteur isométrique professionnel, et un seul modèle de données.</p><div className="pdiL-bento">{BENTO.map((cell) => <div key={cell.title} className={cell.span ? "pdiL-cell " + cell.span : "pdiL-cell"}><h4>{cell.title}</h4><p>{cell.text}</p></div>)}</div></div></section>
    <footer className="pdiL-foot" id="contact"><div className="pdiL-wrap"><div className="pdiL-footgrid"><div className="pdiL-footbrand"><div className="pdiL-brand"><span className="pdiL-brand-dot">PD</span><span>PD&amp;I</span></div><p>Conception de tuyauterie et isométriques industriels. Un modèle unique, du relevé terrain au dossier de fabrication.</p><small>Powered by DZ-YSB-DEV</small></div>{FOOT_COLS.map((col) => <div key={col.title} className="pdiL-footcol"><b>{col.title}</b>{col.links.map((label) => <a key={label} onClick={begin} role="button" tabIndex={0}>{label}</a>)}</div>)}</div><div className="pdiL-footbar"><span>PD&amp;I — Piping Design &amp; Isometrics</span><span>Tous droits réservés</span></div></div></footer>
  </>;
}
'''

    write(LANDING_TSX, src[:start] + replacement)
    print("PdiLandingV4.tsx patché.")


def patch_landing_css() -> None:
    src = read(LANDING_CSS)
    if GUARD_CSS in src:
        print("pdiLandingV4.css déjà patché 004d.")
        return

    backup_once(LANDING_CSS)

    css_patch = r'''

/* PATCH 004d — restauration page d'ouverture + boot + launcher */
.pdiL-hero-shell{position:relative;width:100vw;height:100vh;overflow:hidden;background:radial-gradient(120% 90% at 50% 42%,#15191c,#0b0c0d 58%,#070708);display:flex;align-items:center;justify-content:center;color:#f0f0f0;font-family:Inter,ui-sans-serif,system-ui,sans-serif}.pdiL-hero-bg span{position:absolute;border-radius:14px;border:1px solid rgba(255,255,255,.08);background:linear-gradient(135deg,rgba(77,184,212,.16),rgba(255,255,255,.035));box-shadow:0 30px 90px rgba(0,0,0,.55);animation:pdiFloat 12s ease-in-out infinite}.pdiL-hero-bg span:nth-child(1){left:2%;top:4%;width:34%;height:22%;transform:rotate(-5deg);filter:blur(2px);opacity:.45}.pdiL-hero-bg span:nth-child(2){right:3%;top:3%;width:33%;height:24%;transform:rotate(5deg);filter:blur(2px);opacity:.52}.pdiL-hero-bg span:nth-child(3){left:12%;bottom:8%;width:30%;height:26%;transform:rotate(4deg);opacity:.72}.pdiL-hero-bg span:nth-child(4){right:8%;bottom:7%;width:31%;height:27%;transform:rotate(-4deg);opacity:.72}.pdiL-hero-bg span:nth-child(5){left:-5%;top:30%;width:27%;height:30%;transform:rotate(-9deg);opacity:.82}.pdiL-hero-bg span:nth-child(6){right:-5%;top:31%;width:27%;height:30%;transform:rotate(9deg);opacity:.82}@keyframes pdiFloat{50%{margin-top:-9px}}.pdiL-hero-grid{position:absolute;inset:0;opacity:.22;background-image:linear-gradient(115deg,rgba(77,184,212,.16) 1px,transparent 1px),linear-gradient(65deg,rgba(77,184,212,.16) 1px,transparent 1px);background-size:78px 45px;mask-image:radial-gradient(60% 55% at 50% 50%,#000 12%,transparent 78%)}.pdiL-splash{position:relative;z-index:2;max-width:880px;text-align:center;padding:0 28px;display:flex;align-items:center;flex-direction:column;gap:18px}.pdiL-splash-brand small,.pdiL-boot-brand small{display:block;color:#777;font-size:10px;text-transform:uppercase;letter-spacing:.12em;margin-top:2px}.pdiL-splash h1{font-size:clamp(34px,5vw,58px);line-height:1.13;margin:0;letter-spacing:-.025em}.pdiL-splash h1 em{font-style:normal;background:linear-gradient(96deg,#4db8d4,#8fe0ef 46%,#cfeef6);-webkit-background-clip:text;background-clip:text;color:transparent}.pdiL-splash p{max-width:630px;color:#a9b0b3;line-height:1.65;margin:0}.pdiL-hero-button{margin-top:8px;padding:13px 28px;border-radius:7px;background:linear-gradient(180deg,#6fd2ea,#4db8d4);border:1px solid #7fdcf1;color:#04171d;font-weight:800;cursor:pointer;box-shadow:0 18px 45px -15px rgba(77,184,212,.85)}.pdiL-hero-meta{display:flex;gap:11px;flex-wrap:wrap;justify-content:center;color:#6d7477;font:9px/1.4 monospace;text-transform:uppercase;letter-spacing:.1em}.pdiL-hero-meta i{width:3px;height:3px;border-radius:50%;background:#3a4145;margin-top:5px}.pdiL-powered{position:absolute;bottom:20px;left:0;right:0;text-align:center;color:#5a6063;font:9px/1 monospace;text-transform:uppercase;letter-spacing:.11em}.pdiL-homehero{padding:70px 24px 34px;text-align:center}.pdiL-homehero>div{max-width:880px;margin:auto}.pdiL-homehero h1{font-size:clamp(32px,5vw,60px);line-height:1.05;margin:12px auto 18px}.pdiL-homehero p{max-width:700px;margin:0 auto 28px;color:#888;line-height:1.65}.pdiL-boot,.pdiL-launcher{width:100vw;height:100vh;background:#08090a;color:#f0f0f0;font-family:Inter,ui-sans-serif,system-ui,sans-serif;overflow:hidden;position:relative}.pdiL-boot{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px}.pdiL-boot-glow{position:absolute;inset:0;background:radial-gradient(46% 40% at 50% 46%,rgba(77,184,212,.13),transparent 72%)}.pdiL-boot-skip{position:absolute;top:16px;right:18px;width:34px;height:34px;border-radius:8px;background:#111;border:1px solid #222;color:#777;z-index:3;cursor:pointer}.pdiL-boot-brand{z-index:2;display:flex;gap:12px;align-items:center}.pdiL-boot-steps{z-index:2;width:min(392px,86vw);display:flex;flex-direction:column;gap:9px}.pdiL-boot-steps div{display:flex;gap:11px;color:#555;transition:.25s}.pdiL-boot-steps div.now{color:#f2f2f2;transform:translateX(3px)}.pdiL-boot-steps div.done{color:#4caf7d;opacity:.55}.pdiL-boot-steps span{width:18px;color:#4db8d4}.pdiL-boot-steps b{font-size:13px;font-weight:600}.pdiL-bootbar{z-index:2;width:min(392px,86vw);height:2px;background:#1a1c1d}.pdiL-bootbar i{display:block;height:100%;background:#4db8d4;transition:width .4s}.pdiL-bootpct{z-index:2;color:#4db8d4;font:10px/1 monospace;text-transform:uppercase;letter-spacing:.13em}.pdiL-launcher{display:flex;flex-direction:column}.pdiL-launcher-head{height:54px;background:#101011;border-bottom:1px solid #1e1f20;display:flex;align-items:center;gap:14px;padding:0 20px}.pdiL-launcher-head button{background:#141516;border:1px solid #232527;border-radius:4px;color:#aaa;padding:7px 13px;cursor:pointer}.pdiL-session{margin-left:auto;color:#4caf7d;background:#121815;border:1px solid #1f3227;border-radius:4px;padding:5px 10px;font:10px monospace}.pdiL-session i{display:inline-block;width:5px;height:5px;background:#4caf7d;border-radius:50%;margin-right:7px}.pdiL-launcher-body{flex:1;overflow:auto;padding:34px 44px}.pdiL-launcher-body h1{font-size:30px;margin:10px 0}.pdiL-launcher-body>p{color:#777;max-width:660px;line-height:1.65}.pdiL-entry-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:24px}.pdiL-entry{text-align:left;background:#111;border:1px solid #1e1f20;border-radius:10px;padding:15px 16px 40px;min-height:190px;position:relative;color:#eee;cursor:pointer;transition:.16s}.pdiL-entry:hover,.pdiL-entry.selected{border-color:var(--entry);background:#12181b;transform:translateY(-2px)}.pdiL-entry-top{display:flex;justify-content:space-between;margin-bottom:12px}.pdiL-entry-top b{color:var(--entry)}.pdiL-entry-top em{font:9px monospace;color:var(--entry);font-style:normal;border:1px solid var(--entry);padding:2px 6px;border-radius:3px}.pdiL-entry strong{display:block;font-size:14px}.pdiL-entry small{display:block;color:#555;text-transform:uppercase;font:9px monospace;margin:6px 0}.pdiL-entry p{font-size:12px;line-height:1.55;color:#777}.pdiL-entry-go{position:absolute;left:16px;bottom:13px;color:var(--entry);font-size:12px;opacity:.8}.pdiL-launch-actions{display:flex;align-items:center;gap:16px;margin-top:24px}.pdiL-launch-actions span{color:#444;font:10px monospace}.pdiL-launcher-foot{height:34px;display:flex;align-items:center;justify-content:center;border-top:1px solid #171819;color:#444;font:9px monospace;text-transform:uppercase;letter-spacing:.16em}@media(max-width:1100px){.pdiL-entry-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:620px){.pdiL-entry-grid{grid-template-columns:1fr}.pdiL-launcher-body{padding:24px 18px}.pdiL-launch-actions{align-items:flex-start;flex-direction:column}.pdiL-session{display:none}}
'''

    write(LANDING_CSS, src.rstrip() + "\n" + css_patch + "\n")
    print("pdiLandingV4.css patché.")


def write_report() -> None:
    content = f"""# PATCH 004d — Réparation landing / page d’ouverture

Date : {datetime.now().isoformat(timespec='seconds')}

## Objectif
Restaurer la séquence complète : splash → accueil → boot → launcher → module.

## Fichiers modifiés
- `src/pdi/landing/PdiLandingV4.tsx`
- `src/pdi/landing/pdiLandingV4.css`
- `src/pdi/app/PdiUnifiedApp.tsx`

## Fichiers protégés
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx` : non modifié.
- `src/pdi/model/index.ts` : non utilisé pour remplacer V4.8d.
- Aucun fichier GitHub distant modifié.

## Validation attendue
```bash
npm install
npm run lint
npm run build
```

## Test visuel
1. Splash “Du croquis à l’isométrique normé…”
2. Clic “Let’s begin”
3. Accueil PD&I
4. Clic “Démarrer”
5. Boot / chargement
6. Launcher
7. Sélection “Nouveau Plan”
8. Ouverture du module isométrique V4.8d

## Rollback
```bash
cp src/pdi/app/PdiUnifiedApp.tsx.before004d src/pdi/app/PdiUnifiedApp.tsx
cp src/pdi/landing/PdiLandingV4.tsx.before004d src/pdi/landing/PdiLandingV4.tsx
cp src/pdi/landing/pdiLandingV4.css.before004d src/pdi/landing/pdiLandingV4.css
```
"""
    write(REPORT, content)
    print(f"Rapport écrit : {REPORT}")


def update_history() -> None:
    if not HISTORY.exists():
        print("PATCH_HISTORY.md absent — historique non mis à jour.")
        return

    src = read(HISTORY)
    if "PATCH 004d" in src:
        print("PATCH_HISTORY.md déjà mis à jour.")
        return

    entry = f"""

## PATCH 004d — Réparation landing / page d’ouverture

Date : {datetime.now().strftime('%Y-%m-%d')}

- Restauration de la séquence complète splash → accueil → boot → launcher → module.
- Ajout d’une entrée ciblée depuis la landing vers les modules existants.
- Moteur V4.8d non modifié.
- Aucun remplacement du modèle métier.
"""
    write(HISTORY, src.rstrip() + "\n" + entry)
    print("PATCH_HISTORY.md mis à jour.")


def main() -> None:
    print("PD&I PATCH 004d — réparation landing / page d’ouverture")
    assert_project()

    engine_before = read(ENGINE)

    patch_unified_app()
    patch_landing_tsx()
    patch_landing_css()
    write_report()
    update_history()

    engine_after = read(ENGINE)
    if engine_before != engine_after:
        fail("sécurité : le moteur V4.8d a été modifié, rollback nécessaire")

    print("\nPATCH 004d appliqué avec succès.")
    print("Moteur V4.8d intact.")
    print("\nProchaines commandes recommandées :")
    print("  npm install")
    print("  npm run lint")
    print("  npm run build")


if __name__ == "__main__":
    main()
