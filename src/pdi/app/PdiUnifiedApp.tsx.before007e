import React, { useEffect, useMemo, useState } from "react";
import PdiBrandMark from "./PdiBrandMark";
import PdiIsometricEditor from "../isometric/PdiIsometricEditor";
// PATCH 004c : page publicitaire publique, montee AVANT la coquille applicative.
import PdiLandingV4 from "../landing/PdiLandingV4";
import isoPiping3D from "../../assets/images/pdi_iso_piping_3d_1787006532562.jpg";
import valve3D from "../../assets/images/pdi_valve_3d_1787006543831.jpg";
import plantScan3D from "../../assets/images/pdi_plant_scan_3d_1787006555680.jpg";
import cadSpool3D from "../../assets/images/pdi_cad_spool_3d_1787006567003.jpg";

type PdiModule = "home" | "isometric" | "vision" | "sketch" | "cad" | "json" | "pdf" | "projects" | "assistant";

// PATCH 004c : cle de session de l'etape publique.
const PDI_STAGE_KEY = "pdi.stage.v4";

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
  {
    title: "Dessin isométrique 3D",
    text: "Moteur vectoriel temps-réel, tubes DN, robinetterie, cotations automatiques et alignements spatiaux.",
    tag: "ISO 3D",
    color: "#0ea5e9",
    image: isoPiping3D,
    caption: "Réseau tuyauterie inox & collecteurs haute fidélité",
  },
  {
    title: "Vision PD&I Réelle",
    text: "Photo d'installation réelle → segmentation 3D → JSON piping → validation industrielle.",
    tag: "VISION 3D",
    color: "#f97316",
    image: plantScan3D,
    caption: "Scan & détection des composants de tuyauterie",
  },
  {
    title: "Croquis & Modèle CAO",
    text: "Reconnaissance de tracés main, génération instantanée du spool 3D et cotations.",
    tag: "CROQUIS 3D",
    color: "#8b5cf6",
    image: cadSpool3D,
    caption: "Spool préfabriqué avec cotes isométriques",
  },
  {
    title: "Organes & Robinets 3D",
    text: "Vannes à passage direct, papillons, brides et by-pass intégrés en bibliothèque standard.",
    tag: "EQUIP 3D",
    color: "#22c55e",
    image: valve3D,
    caption: "Robinetterie industrielle & instrumentation",
  },
  {
    title: "Plans & Cartouches ISO",
    text: "Exportation PDF/DXF normalisée A4/A3/A2/A1 avec nomenclature automatique (BOM).",
    tag: "EXPORT",
    color: "#eab308",
    image: isoPiping3D,
    caption: "Planche d'exécution et dossier de fabrication",
  },
  {
    title: "Jumeau Numérique & IA",
    text: "Agents spécialisés pipeline-design-skill pour l'assistance et la vérification des règles de l'art.",
    tag: "DIGITAL TWIN",
    color: "#06b6d4",
    image: plantScan3D,
    caption: "Modélisation intelligente assistée par IA",
  },
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
  // PATCH 004c : etape "landing" (page publicitaire, sans barre laterale) puis
  // "app" (coquille + modules). Memorise pour la session uniquement : aucune
  // interference avec les cles localStorage d'autosauvegarde du moteur V4.8d.
  const [stage, setStage] = useState<"landing" | "app">(() => {
    try {
      return window.sessionStorage.getItem(PDI_STAGE_KEY) === "app" ? "app" : "landing";
    } catch {
      return "landing";
    }
  });

  const enterApp = React.useCallback((target?: string) => {
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
  }, []);

  useEffect(() => {
    const onNavigate = (event: Event) => {
      const detail = (event as CustomEvent<PdiModule>).detail;
      // PATCH 005 : navigation ciblee stabilisee.
      // Une navigation externe entre dans le logiciel uniquement vers un module connu.
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
      setStage("app");
      setActiveModule(allowed.includes(detail) ? detail : "home");
    };
    window.addEventListener("pdi:navigate", onNavigate as EventListener);
    return () => window.removeEventListener("pdi:navigate", onNavigate as EventListener);
  }, []);

  const moduleTitle = useMemo(() => navItems.find((x) => x.id === activeModule)?.title || "PD&I", [activeModule]);

  // PATCH 004c : la page publicitaire est rendue seule, sans barre laterale ni
  // barre superieure. Une navigation externe (pdi:navigate) entre directement
  // dans le logiciel, ce qui preserve le comportement existant.
  if (stage === "landing") return <PdiLandingV4 onEnter={enterApp} />;

  if (activeModule === "isometric") return <PdiIsometricEditor />;

  return (
    <div className="pdi-unified-root">
      <style>{`
        .pdi-unified-root{height:100vh;width:100vw;overflow:hidden;background:#070B12;color:#E5EDF8;font-family:Inter,ui-sans-serif,system-ui,sans-serif;display:grid;grid-template-columns:96px 1fr;grid-template-rows:72px 1fr}.pdi-unified-topbar{grid-column:1/3;display:flex;align-items:center;gap:18px;padding:8px 16px;background:linear-gradient(180deg,#111827,#0B1019);border-bottom:1px solid rgba(148,163,184,.22);box-shadow:0 8px 24px rgba(0,0,0,.28);min-width:0}.pdi-unified-brand{display:flex;align-items:center;gap:14px;min-width:260px}.pdi-project-title{min-width:0;border-left:1px solid rgba(148,163,184,.28);padding-left:14px;line-height:1.1}.pdi-project-title small{display:block;color:#8EA3C2;font-size:10px;text-transform:uppercase;font-weight:900}.pdi-project-title strong{display:block;color:#F8FAFC;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pdi-top-actions{margin-left:auto;display:flex;align-items:center;gap:8px;color:#93A4BD;font-size:12px}.pdi-search{height:36px;width:min(340px,24vw);border:1px solid rgba(148,163,184,.22);background:#0A1220;color:#E5EDF8;border-radius:10px;padding:0 12px;font-weight:800}.pdi-account{height:36px;border:1px solid rgba(34,211,238,.35);background:#0A1220;color:#F8FAFC;border-radius:10px;padding:0 12px;font-weight:900}.pdi-main-nav{grid-row:2;display:flex;flex-direction:column;gap:10px;padding:14px 10px;background:linear-gradient(180deg,#0D1420,#090E17);border-right:1px solid rgba(148,163,184,.18);overflow:auto}.pdi-main-nav button{height:58px;border:1px solid rgba(148,163,184,.16);background:#111827;color:#BBD0EA;border-radius:14px;font-weight:1000;font-size:13px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer}.pdi-main-nav button.active{background:linear-gradient(135deg,#0284C7,#0EA5E9);color:white;border-color:#67E8F9;box-shadow:0 0 0 1px rgba(103,232,249,.55),0 16px 35px rgba(14,165,233,.25)}.pdi-main-nav small{font-size:8px;letter-spacing:.06em;text-transform:uppercase;opacity:.82}.pdi-content{grid-column:2;grid-row:2;min-width:0;min-height:0;overflow:auto;padding:22px;background:radial-gradient(circle at 18% 8%,rgba(14,165,233,.16),transparent 32%),radial-gradient(circle at 86% 12%,rgba(249,115,22,.13),transparent 28%),#070B12}.pdi-home-hero{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(330px,.8fr);gap:20px;align-items:stretch}.pdi-hero-card,.pdi-module-panel,.pdi-launch-card,.pdi-showcase-card{border:1px solid rgba(148,163,184,.18);background:linear-gradient(180deg,rgba(15,23,42,.94),rgba(8,13,24,.98));border-radius:24px;box-shadow:0 24px 70px rgba(0,0,0,.28)}.pdi-hero-card{padding:28px}.pdi-hero-card h1,.pdi-module-panel h1{font-size:clamp(28px,4vw,54px);line-height:.95;margin:0;color:#F8FAFC;letter-spacing:-.04em}.pdi-hero-card p{color:#B9C8DD;font-weight:700;max-width:760px}.pdi-badge-row{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.pdi-badge{border:1px solid rgba(103,232,249,.28);background:rgba(8,145,178,.12);color:#67E8F9;border-radius:999px;padding:7px 10px;font-size:11px;font-weight:1000;text-transform:uppercase}.pdi-launch-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:20px}.pdi-launch-card{padding:18px;text-align:left;color:#E5EDF8;cursor:pointer;transition:.18s transform,.18s border-color}.pdi-launch-card:hover{transform:translateY(-2px);border-color:#38BDF8}.pdi-launch-card .icon{width:54px;height:54px;border-radius:16px;display:grid;place-items:center;background:#0EA5E9;color:white;font-weight:1000;margin-bottom:12px}.pdi-launch-card h3{margin:0 0 8px;font-size:18px}.pdi-launch-card p{margin:0;color:#9FB0C8;font-size:12px;font-weight:700}.pdi-launch-card .badge{display:inline-block;margin-top:12px;color:#FDE68A;font-size:10px;font-weight:1000;text-transform:uppercase}.pdi-showcase{height:calc(100vh - 132px);overflow:hidden;position:relative;border-radius:24px;border:1px solid rgba(148,163,184,.14);background:rgba(10,18,32,.5);padding:10px}.pdi-showcase:hover .pdi-showcase-track{animation-play-state:paused}.pdi-showcase-track{display:flex;flex-direction:column;gap:16px;animation:pdiShowcaseScroll 32s linear infinite}.pdi-showcase-card{padding:14px;position:relative;overflow:hidden;transition:transform .2s ease,border-color .2s ease;border:1px solid rgba(148,163,184,.2)}.pdi-showcase-card:hover{transform:translateY(-3px);border-color:var(--accent)}.pdi-showcase-card::before{content:"";position:absolute;inset:auto -30px -45px auto;width:140px;height:140px;border-radius:999px;background:var(--accent);opacity:.2;filter:blur(10px);pointer-events:none}.pdi-showcase-img-box{position:relative;width:100%;height:140px;border-radius:14px;overflow:hidden;border:1px solid rgba(148,163,184,.22);background:#070C15;margin-bottom:12px}.pdi-showcase-img{width:100%;height:100%;object-fit:cover;transition:transform .4s cubic-bezier(0.16,1,0.3,1)}.pdi-showcase-card:hover .pdi-showcase-img{transform:scale(1.06)}.pdi-showcase-img-overlay{position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(7,11,18,.85) 100%)}.pdi-showcase-img-caption{position:absolute;bottom:6px;left:8px;right:8px;font-size:10px;font-weight:800;color:#F1F5F9;text-shadow:0 1px 3px rgba(0,0,0,.9);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pdi-showcase-card .tag{display:inline-grid;place-items:center;min-width:64px;padding:0 8px;height:24px;border-radius:8px;background:var(--accent);color:white;font-size:10px;font-weight:900;letter-spacing:.04em;text-transform:uppercase}.pdi-showcase-card h3{margin:0 0 6px;font-size:16px;color:#F8FAFC;font-weight:800}.pdi-showcase-card p{margin:0;color:#94A3B8;font-weight:600;font-size:12px;line-height:1.45}@keyframes pdiShowcaseScroll{0%{transform:translateY(0)}100%{transform:translateY(-50%)}}.pdi-module-panel{padding:28px;min-height:calc(100vh - 128px)}.pdi-panel-kicker{color:#67E8F9;font-size:11px;text-transform:uppercase;font-weight:1000;margin-bottom:10px}.pdi-panel-body{margin-top:20px;color:#B9C8DD;font-weight:750;line-height:1.75;max-width:980px}.pdi-panel-body code{background:#111827;border:1px solid rgba(148,163,184,.18);border-radius:8px;padding:3px 6px;color:#FDE68A}.pdi-start-primary{border:0;background:linear-gradient(135deg,#0284C7,#22D3EE);color:white;border-radius:16px;padding:14px 18px;font-weight:1000;cursor:pointer;box-shadow:0 18px 45px rgba(14,165,233,.28)}@media(max-width:900px){.pdi-unified-root{grid-template-columns:1fr;grid-template-rows:72px auto 1fr}.pdi-unified-topbar{grid-column:1}.pdi-project-title,.pdi-search{display:none}.pdi-main-nav{grid-row:2;flex-direction:row;overflow-x:auto;padding:8px}.pdi-main-nav button{min-width:72px;height:54px}.pdi-content{grid-column:1;grid-row:3;padding:12px}.pdi-home-hero{grid-template-columns:1fr}.pdi-launch-grid{grid-template-columns:1fr}.pdi-showcase{height:420px}}
      `}</style>
      <header className="pdi-unified-topbar"><div className="pdi-unified-brand"><PdiBrandMark variant="horizontal" size="sm" /></div><div className="pdi-project-title"><small>Projet actif</small><strong>{moduleTitle}</strong></div><div className="pdi-top-actions"><input className="pdi-search" placeholder="Rechercher une commande…" /><span>Essai</span><button className="pdi-account">Compte</button></div></header>
      <nav className="pdi-main-nav" aria-label="Navigation PD&I">{navItems.map((item) => <button key={item.id} className={activeModule === item.id ? "active" : ""} onClick={() => setActiveModule(item.id)} title={item.title}><span>{item.icon}</span><small>{item.label}</small></button>)}</nav>
      <main className="pdi-content">
        {activeModule === "home" && <div className="pdi-home-hero">
          <section className="pdi-hero-card">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-4">
              <div className="pdi-badge-row my-0"><span className="pdi-badge">SaaS autonome</span><span className="pdi-badge">JSON central</span><span className="pdi-badge">Python calculs</span><span className="pdi-badge">Agents spécialisés</span></div>
              <div className="hidden sm:block shrink-0 rounded-2xl overflow-hidden border border-slate-700/60 shadow-lg bg-black/40 p-1.5">
                <img src="/pdi-logo-square.png" alt="PD&I — Pipeline Design & Isometrics" className="h-16 w-16 object-contain rounded-xl" />
              </div>
            </div>
            <h1>Construire vos plans isométriques depuis toutes vos sources.</h1>
            <p>PD&I devient le logiciel principal : dessin manuel, Vision PD&I photo/croquis, import CAO/DXF/PDF, JSON central, exports et validation engineering.</p>
            <button className="pdi-start-primary" onClick={() => setActiveModule("isometric")}>Nouveau projet isométrique</button>
            <div className="pdi-launch-grid">
              {launchCards.map((card) => (
                <button key={card.id} className="pdi-launch-card" onClick={() => setActiveModule(card.id)} title={card.title}>
                  <div className="icon">{card.icon}</div>
                  <h3>{card.title}</h3>
                  <p>{card.subtitle}</p>
                  <span className="badge">{card.ready ? "Disponible" : card.badge}</span>
                </button>
              ))}
            </div>
          </section>
          <aside className="pdi-showcase">
            <div className="pdi-showcase-track">
              {[...showcase, ...showcase].map((item, index) => (
                <div key={`${item.tag}-${index}`} className="pdi-showcase-card" style={{ "--accent": item.color } as React.CSSProperties}>
                  <div className="pdi-showcase-img-box">
                    <img
                      src={item.image}
                      alt={item.title}
                      className="pdi-showcase-img"
                      referrerPolicy="no-referrer"
                      loading="lazy"
                    />
                    <div className="pdi-showcase-img-overlay" />
                    <div className="pdi-showcase-img-caption">{item.caption}</div>
                  </div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="tag">{item.tag}</span>
                    <span className="text-[10px] font-mono text-slate-400 font-bold">3D CAD ENGINE</span>
                  </div>
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                </div>
              ))}
            </div>
          </aside>
        </div>}
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
