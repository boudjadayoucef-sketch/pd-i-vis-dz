// PATCH 004c — PD&I landing v4.
// Page publicitaire publique : AUCUNE barre laterale (la coquille applicative
// n'est montee qu'apres l'entree dans le logiciel), banniere d'information
// pleine largeur, "PD&I en 4 temps", bento minimaliste, pied de page minimaliste.
//
// Ce composant est purement presentationnel : il ne connait ni le moteur V4.8d,
// ni le graphe, ni la topologie. Il expose une seule sortie : onEnter().

import React, { useEffect, useState } from "react";
import "./pdiLandingV4.css";

export type PdiLandingV4Props = {
  /** Appele pour entrer dans le logiciel (connexion / demarrage). */
  onEnter: () => void;
};

const NAV_LINKS = [
  { id: "fonctions", label: "Fonctions" },
  { id: "temps", label: "4 temps" },
  { id: "modules", label: "Modules" },
  { id: "contact", label: "Contact" },
];

const BAND = [
  { key: "iso", cls: "pdiL-band-iso", title: "Isometrique", text: "Noeuds, tubes DN, organes, cotations, elevations Z et soudures W00x." },
  { key: "vision", cls: "pdiL-band-vision", title: "Vision IA", text: "Photo, scan ou plan 2D reconnu, puis converti en JSON piping verifiable." },
  { key: "sketch", cls: "pdiL-band-sketch", title: "Croquis", text: "Un dessin a la main devient un reseau topologique exploitable." },
  { key: "json", cls: "pdiL-band-json", title: "JSON central", text: "Un seul modele de reference pour le 2D, le 3D, l'ISO et le metre." },
];

const STEPS = [
  { n: "01", cls: "pdiL-step-1", title: "Capturer", text: "Photo, scan, PDF, plan 2D ou donnees CAO : toute source devient un point de depart." },
  { n: "02", cls: "pdiL-step-2", title: "Reconnaitre", text: "La vision IA identifie la tuyauterie et produit un JSON piping structure." },
  { n: "03", cls: "pdiL-step-3", title: "Construire", text: "Modele topologique, 2D et 3D synchronises, edition professionnelle temps reel." },
  { n: "04", cls: "pdiL-step-4", title: "Livrer", text: "ISO, cotations, DN, W00x, BOM, metre, QA engineering et export documentaire." },
];

const BENTO = [
  { span: "pdiL-sp2", title: "Editeur isometrique professionnel", text: "Clic droit, proprietes reelles X / Y / Z, copier-coller a nouveaux IDs, undo par operation logique." },
  { span: "", title: "Cotations", text: "Selection multiple, unites m / mm, ancrage sur noeud ou sur port." },
  { span: "", title: "Soudures W00x", text: "Numerotation automatique et recalcul apres chaque modification." },
  { span: "", title: "Metre & BOM", text: "Longueurs, poids, volumes et nomenclature toujours a jour." },
  { span: "pdiL-sp2", title: "2D et 3D synchronises", text: "Le plan tuyauterie et l'isometrique partagent le meme graphe : aucune double saisie." },
  { span: "", title: "QA engineering", text: "Controle du reseau, ports orphelins, incoherences DN signalees." },
  { span: "", title: "Trackpad & raccourcis", text: "Pan et pincement Mac, raccourcis Cmd et Ctrl, rotation R / Shift+R." },
  { span: "pdiL-sp3", title: "Export documentaire", text: "Planches A4 a A1, cartouche, PDF, DXF et dossier de fabrication." },
];

const FOOT_COLS = [
  { title: "Produit", links: ["Editeur isometrique", "Vision IA", "Croquis vers ISO", "Import CAO"] },
  { title: "Ingenierie", links: ["Modele JSON", "Soudures W00x", "Metre & BOM", "QA engineering"] },
  { title: "Ressources", links: ["Documentation", "Historique des patchs", "Regles de l'art", "Journal des versions"] },
  { title: "Societe", links: ["A propos", "Contact", "Mentions legales", "Confidentialite"] },
];

export default function PdiLandingV4({ onEnter }: PdiLandingV4Props) {
  const [stuck, setStuck] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setStuck(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const goto = (id: string) => {
    setMenuOpen(false);
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const enter = () => {
    setMenuOpen(false);
    onEnter();
  };

  return (
    <div className="pdiL-root">
      <div className="pdiL-navhost">
        <nav className={stuck ? "pdiL-nav is-stuck" : "pdiL-nav"} aria-label="Navigation PD&I">
          <div className="pdiL-brand">
            <span className="pdiL-brand-dot">PD</span>
            <span>PD&amp;I</span>
          </div>
          <div className="pdiL-navlinks">
            {NAV_LINKS.map((link) => (
              <button key={link.id} type="button" className="pdiL-navlink" onClick={() => goto(link.id)}>
                {link.label}
              </button>
            ))}
          </div>
          <div className="pdiL-navactions">
            <button type="button" className="pdiL-btn pdiL-btn-ghost" onClick={enter}>Connexion</button>
            <button type="button" className="pdiL-btn pdiL-btn-primary" onClick={enter}>Demarrer</button>
          </div>
          <button
            type="button"
            className="pdiL-burger"
            aria-label="Ouvrir le menu"
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((v) => !v)}
          >
            {menuOpen ? "\u2715" : "\u2630"}
          </button>
        </nav>
        <div className={menuOpen ? "pdiL-mobilemenu is-open" : "pdiL-mobilemenu"}>
          {NAV_LINKS.map((link) => (
            <button key={link.id} type="button" className="pdiL-navlink" onClick={() => goto(link.id)}>
              {link.label}
            </button>
          ))}
          <button type="button" className="pdiL-btn pdiL-btn-ghost" onClick={enter}>Connexion</button>
          <button type="button" className="pdiL-btn pdiL-btn-primary" onClick={enter}>Demarrer</button>
        </div>
      </div>

      <header className="pdiL-hero">
        <div className="pdiL-wrap">
          <span className="pdiL-kicker">Piping Design &amp; Isometrics</span>
          <h1>
            De la photo au plan isometrique, <em>sans ressaisie</em>.
          </h1>
          <p>
            PD&amp;I lit vos sources reelles, reconnait la tuyauterie, construit un modele
            topologique unique et produit l'isometrique, les cotations, les soudures et le metre.
          </p>
          <div className="pdiL-herocta">
            <button type="button" className="pdiL-btn pdiL-btn-primary pdiL-btn-lg" onClick={enter}>
              Commencer un isometrique
            </button>
            <button type="button" className="pdiL-btn pdiL-btn-ghost pdiL-btn-lg" onClick={() => goto("temps")}>
              Voir la methode
            </button>
          </div>
        </div>
      </header>

      <div className="pdiL-band" id="fonctions">
        {BAND.map((cell) => (
          <div key={cell.key} className={"pdiL-bandcell " + cell.cls}>
            <b>{cell.title}</b>
            <span>{cell.text}</span>
          </div>
        ))}
      </div>

      <section className="pdiL-sec" id="temps">
        <div className="pdiL-wrap">
          <div className="pdiL-seclabel">Methode</div>
          <h2>PD&amp;I en 4 temps</h2>
          <p className="pdiL-lead">
            Une chaine unique, de la source reelle jusqu'au dossier d'execution.
          </p>
          <div className="pdiL-steps">
            {STEPS.map((step) => (
              <div key={step.n} className={"pdiL-step " + step.cls}>
                <div className="pdiL-stepnum">{step.n}</div>
                <h3>{step.title}</h3>
                <p>{step.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="pdiL-sec" id="modules">
        <div className="pdiL-wrap">
          <div className="pdiL-seclabel">Capacites</div>
          <h2>Ce que fait le logiciel</h2>
          <p className="pdiL-lead">
            Un moteur isometrique professionnel, et un seul modele de donnees.
          </p>
          <div className="pdiL-bento">
            {BENTO.map((cell) => (
              <div key={cell.title} className={cell.span ? "pdiL-cell " + cell.span : "pdiL-cell"}>
                <h4>{cell.title}</h4>
                <p>{cell.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="pdiL-foot" id="contact">
        <div className="pdiL-wrap">
          <div className="pdiL-footgrid">
            <div className="pdiL-footbrand">
              <div className="pdiL-brand">
                <span className="pdiL-brand-dot">PD</span>
                <span>PD&amp;I</span>
              </div>
              <p>
                Conception de tuyauterie et isometriques industriels. Un modele unique,
                du releve terrain au dossier de fabrication.
              </p>
              <small>Powered by DZ-YSB-DEV</small>
            </div>
            {FOOT_COLS.map((col) => (
              <div key={col.title} className="pdiL-footcol">
                <b>{col.title}</b>
                {col.links.map((label) => (
                  <a key={label} onClick={enter} role="button" tabIndex={0}
                     onKeyDown={(e) => { if (e.key === "Enter") enter(); }}>
                    {label}
                  </a>
                ))}
              </div>
            ))}
          </div>
          <div className="pdiL-footbar">
            <span>PD&amp;I — Piping Design &amp; Isometrics</span>
            <span>Tous droits reserves</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
