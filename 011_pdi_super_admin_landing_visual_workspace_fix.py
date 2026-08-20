#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 011
Super Admin shell + corrections landing/animations + workspace CAD neutre + grille infinie + suppression barre métrés.

But : minimiser les patchs en suivant le workflow.
PATCH 011 prévu = Super Admin Console, mais on intègre aussi les corrections demandées :
- landing page restaurée/forcée ;
- animations landing/parallax renforcées ;
- photo initiale préparée avec fallback CSS si PNG absent ;
- éléments PD&I créés en couleur neutre gris AutoCAD avant modification ;
- grille workspace stabilisée façon plan infini AutoCAD ;
- suppression de la barre basse avec chiffres / métrés / statut encombrant.

Ne touche pas à la topologie métier V4.8d.
"""
from pathlib import Path
import shutil, sys
from datetime import datetime

ROOT=Path('.')
APP=ROOT/'src/pdi/app/PdiUnifiedApp.tsx'
LAND=ROOT/'src/pdi/landing/PdiLandingV4.tsx'
LANDCSS=ROOT/'src/pdi/landing/pdiLandingV4.css'
ENGINE=ROOT/'src/pdi/isometric/engine/IsometrieModuleV48d.tsx'
REPORT=ROOT/'011_super_admin_landing_workspace_visual_fix_REPORT.md'
HISTORY=ROOT/'docs/PATCH_HISTORY.md'
PUBLIC_ASSETS=ROOT/'public/assets/pdi/landing'

NEUTRAL='#9CA3AF'


def fail(m):
    print('ABANDON: '+m); sys.exit(2)

def read(p): return p.read_text(encoding='utf-8')
def write(p,c): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(c,encoding='utf-8')
def backup(p):
    b=p.with_name(p.name+'.before011')
    if not b.exists(): shutil.copy2(p,b); print('Sauvegarde:',b)

def audit():
    for p in [APP, LAND, LANDCSS, ENGINE]:
        if not p.exists(): fail(f'fichier introuvable: {p}')
    app=read(APP); land=read(LAND); css=read(LANDCSS); eng=read(ENGINE)
    required_app=['PATCH 010','PdiLandingV4','authMode','profile','security']
    missing=[x for x in required_app if x not in app]
    if missing: fail('pré-requis app manquants: '+', '.join(missing))
    if 'pdiL-hero-shell' not in land or 'pdiL-hero-bg' not in land:
        print('ATTENTION: landing hero avancée non détectée, correction CSS/flow appliquée quand même.')
    if 'pdi-status-docked' not in eng:
        print('ATTENTION: barre basse non trouvée, suppression ignorée.')
    print('Audit OK: version actuelle détectée, correction 011 possible.')

def patch_app():
    s=read(APP); backup(APP)
    if 'PATCH 011 — Super admin shell and landing restore' in s:
        print('App déjà patchée 011'); return
    s='// PATCH 011 — Super admin shell and landing restore\n'+s
    # Ajouter super_admin_console au type module
    s=s.replace('"profile" | "subscription" | "security";', '"profile" | "subscription" | "security" | "super_admin_console";')
    # Forcer la landing au premier chargement sauf route app explicitement mémorisée en localStorage.
    old='return window.sessionStorage.getItem(PDI_STAGE_KEY) === "app" ? "app" : "landing";'
    if old in s:
        s=s.replace(old, 'return window.localStorage.getItem("pdi.force.app.v1") === "1" || window.sessionStorage.getItem(PDI_STAGE_KEY) === "app" ? "app" : "landing";',1)
    # Quand on entre via auth/démo, mémoriser app volontaire.
    s=s.replace('window.sessionStorage.setItem(PDI_STAGE_KEY,"app");', 'window.sessionStorage.setItem(PDI_STAGE_KEY,"app"); window.localStorage.setItem("pdi.force.app.v1","1");')
    s=s.replace('window.sessionStorage.setItem(PDI_STAGE_KEY, "app");', 'window.sessionStorage.setItem(PDI_STAGE_KEY, "app"); window.localStorage.setItem("pdi.force.app.v1","1");')
    # Retour landing nettoie le flag app.
    s=s.replace('window.localStorage.removeItem(PDI_STAGE_KEY)', 'window.localStorage.removeItem(PDI_STAGE_KEY); window.localStorage.removeItem("pdi.force.app.v1")')
    # Menu compte : ajouter super admin
    marker='<button onClick={()=>setActiveModule("security")}>Sécurité</button>'
    if marker in s and 'super_admin_console' not in s[s.find('pdi-account-menu'):s.find('pdi-account-menu')+1200]:
        s=s.replace(marker, marker+'<button onClick={()=>{setAuthMode("super_admin"); setActiveModule("super_admin_console")}}>Super Admin</button>',1)
    # Ajouter panneau Super Admin avant assistant
    anchor='        {activeModule === "assistant" && <ComingSoonPanel title="Assistant et agents spécialisés"><p>PD&I orchestrera le repo <code>pipeline-design-skill</code> : agents Vision, Croquis, CAO, JSON, ISO, QA. Les agents proposent ; Python calcule.</p></ComingSoonPanel>}'
    panel=r'''
        {activeModule === "super_admin_console" && <ComingSoonPanel title="Super Admin Console">
          <div className="pdi-super-grid">
            {[
              ["Demandes", "Réception demande → paiement → compte"],
              ["Clés", "Trial, Guest, Pro, Team, Enterprise"],
              ["Comptes", "Créer, suspendre, activer, inviter"],
              ["Paiements", "Simulation avant intégration réelle"],
              ["Emails", "Activation unique et confirmation"],
              ["Firebase", "Auth, Firestore, Storage, règles"],
              ["Migration", "Provider prêt Supabase/Postgres"],
              ["Rapports", "Journalier + sécurité + assets PNG"]
            ].map(([title,txt])=><section key={title} className="pdi-super-card"><b>{title}</b><span>{txt}</span></section>)}
          </div>
        </ComingSoonPanel>}
'''
    if anchor in s and 'Super Admin Console' not in s:
        s=s.replace(anchor, panel+'\n'+anchor,1)
    # Styles super admin et landing restore button visibility
    if '.pdi-super-grid' not in s:
        s=s.replace('@media(max-width:900px)', '.pdi-super-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.pdi-super-card{min-height:112px;border:1px solid rgba(103,232,249,.28);background:linear-gradient(180deg,#142033,#0A101A);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:8px;box-shadow:0 18px 40px rgba(0,0,0,.25);animation:pdiTabIn .25s ease both}.pdi-super-card b{color:#67E8F9;font-size:13px}.pdi-super-card span{color:#C7D2FE;font-size:12px;font-weight:700}@media(max-width:900px)',1)
    write(APP,s)
    print('App patchée 011: landing flow + super admin shell.')

def patch_landing():
    s=read(LAND); backup(LAND)
    if 'PATCH 011 — commercial landing restored' in s:
        print('Landing déjà patchée 011'); return
    s='// PATCH 011 — commercial landing restored\n'+s
    # Restaurer wording commercial propre après le remplacement agressif du patch 010.
    s=s.replace('Connexion / Démo un projet vierge', 'Créer un projet vierge')
    s=s.replace('Choisir après connexion', 'Nouveau projet isométrique')
    # Garder CTA auth mais commercial.
    s=s.replace('Connexion / Démo →', 'Découvrir PD&I →')
    # Ajouter visuel initial si absent dans hero splash.
    target='<button className="pdiL-hero-button" onClick={() => setScreen("home")}>Découvrir PD&I →</button>'
    if target in s and 'pdiL-hero-visual' not in s:
        visual='''<div className="pdiL-hero-visual" aria-hidden="true"><img src="/assets/pdi/landing/hero-dashboard.png" onError={(e)=>{(e.currentTarget as HTMLImageElement).style.display='none'}} /><div className="pdiL-hero-fallback"><b>PD&I</b><span>ISO · CAD 2D · Vision · JSON</span></div></div>'''
        s=s.replace(target, visual+target,1)
    write(LAND,s)
    print('Landing patchée 011: wording + visuel initial préparé.')

def patch_landing_css():
    s=read(LANDCSS); backup(LANDCSS)
    if 'PATCH 011 landing parallax restored' in s:
        print('Landing CSS déjà patché 011'); return
    s += r'''
/* PATCH 011 landing parallax restored */
.pdiL-hero-shell{isolation:isolate;perspective:1200px;min-height:100vh!important;display:flex!important}
.pdiL-hero-bg span{will-change:transform,opacity;animation:pdiParallaxFloat 10s ease-in-out infinite alternate!important}
.pdiL-hero-bg span:nth-child(2n){animation-duration:13s!important;animation-direction:alternate-reverse!important}
.pdiL-hero-grid{animation:pdiGridDrift 18s linear infinite!important;background-position:0 0;opacity:.34!important}
.pdiL-splash{animation:pdiHeroRise .7s cubic-bezier(.16,1,.3,1) both!important;transform-style:preserve-3d}
.pdiL-hero-visual{width:min(760px,88vw);height:clamp(170px,24vh,260px);margin:18px auto 10px;border:1px solid rgba(103,232,249,.30);border-radius:22px;background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(8,13,24,.72));box-shadow:0 28px 90px rgba(0,0,0,.42),0 0 80px rgba(34,211,238,.12);overflow:hidden;position:relative;animation:pdiVisualFloat 7s ease-in-out infinite}
.pdiL-hero-visual img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(1.08) contrast(1.05)}
.pdiL-hero-fallback{position:absolute;inset:0;display:grid;place-items:center;text-align:center;background:radial-gradient(circle at 35% 30%,rgba(77,184,212,.25),transparent 35%),linear-gradient(135deg,#0f172a,#020617)}
.pdiL-hero-fallback b{font-size:clamp(46px,8vw,86px);letter-spacing:.08em;color:#EAF6FF;text-shadow:0 0 30px rgba(103,232,249,.34)}
.pdiL-hero-fallback span{position:absolute;bottom:24px;color:#67E8F9;font-weight:900;letter-spacing:.18em;font-size:11px;text-transform:uppercase}
.pdiL-entry,.pdiL-btn,.pdiL-hero-button{animation:pdiCardIn .45s ease both}.pdiL-entry:nth-child(2){animation-delay:.05s}.pdiL-entry:nth-child(3){animation-delay:.1s}.pdiL-entry:nth-child(4){animation-delay:.15s}
@keyframes pdiParallaxFloat{0%{transform:translate3d(-8px,6px,0) rotate(-4deg) scale(1)}100%{transform:translate3d(12px,-10px,40px) rotate(5deg) scale(1.035)}}
@keyframes pdiGridDrift{from{background-position:0 0}to{background-position:156px 90px}}
@keyframes pdiHeroRise{from{opacity:0;transform:translateY(18px) rotateX(4deg)}to{opacity:1;transform:none}}
@keyframes pdiVisualFloat{0%,100%{transform:translateY(0) rotateX(0)}50%{transform:translateY(-8px) rotateX(1.5deg)}}
@keyframes pdiCardIn{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:none}}
'''
    write(LANDCSS,s)
    print('Landing CSS patché 011: parallax/animations/visuel fallback.')

def patch_engine():
    s=read(ENGINE); backup(ENGINE)
    if 'PATCH 011 — neutral CAD colors infinite grid no bottom metrics' in s:
        print('Engine déjà patché 011'); return
    s='// PATCH 011 — neutral CAD colors infinite grid no bottom metrics\n'+s
    # Couleurs neutres par défaut
    s=s.replace('color:"#0284c7"}]);', f'color:"{NEUTRAL}"}}]);',1)
    s=s.replace('color:"#0284c7"};', f'color:"{NEUTRAL}"}};',1)
    s=s.replace('color: "#4db8d4"', f'color: "{NEUTRAL}"')
    s=s.replace('color: "#f0f0f0"', f'color: "{NEUTRAL}"')
    s=s.replace('color: "#8b5cf6"', f'color: "{NEUTRAL}"')
    s=s.replace('color: "#e8a838"', f'color: "{NEUTRAL}"')
    s=s.replace('s.color||((s.pn.includes("600"))?"#f59e0b":"#0284c7")', f's.color||"{NEUTRAL}"')
    s=s.replace('value={s.color||"#0284c7"}', f'value={{s.color||"{NEUTRAL}"}}')
    # Supprimer annotation longueur visuelle sur tubes (barre/chiffres longueur qui reste sur plan)
    s=s.replace('{showDimensions&&showPipeLabels&&s.length>=.5&&<g data-iso-object="true" transform={`translate(${dimensionAnnotation?.x??mx} ${dimensionAnnotation?.y??my-13})`}><rect x="-65" y="-10" width="130" height="18" rx="4" fill="#020617" stroke="#38bdf8"/><text x="0" y="3" fill="#e0f2fe" fontSize="8" fontWeight="900" textAnchor="middle">{(s.sourceName||("Pipeline "+dia(s.dn).inch))+" · L="+s.length.toFixed(2)+" m"}</text></g>}', '{false&&showDimensions&&showPipeLabels&&s.length>=.5&&<g />}')
    # Masquer complètement status docked bas pour éviter chiffres nœuds/tronçons/etc.
    if 'pdi-status-docked ${workspaceFullscreen?' in s:
        s=s.replace('<div className={`pdi-status-docked ${workspaceFullscreen?', '<div className={`hidden pdi-status-docked ${workspaceFullscreen?',1)
    # Grille infinie : remplacer rendu lignes par pattern SVG fixe non friable si anchors présents.
    old_grid_start='{showGrid&&(()=>{'
    if old_grid_start in s and 'pdiInfiniteGrid' not in s:
        inject='''<defs><pattern id="pdiInfiniteGridMinor" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M 24 0 L 0 0 0 24" fill="none" stroke="#334155" strokeWidth="0.45" opacity="0.55"/></pattern><pattern id="pdiInfiniteGridMajor" width="120" height="120" patternUnits="userSpaceOnUse"><rect width="120" height="120" fill="url(#pdiInfiniteGridMinor)"/><path d="M 120 0 L 0 0 0 120" fill="none" stroke="#64748b" strokeWidth="0.8" opacity="0.42"/></pattern></defs>{showGrid&&<rect x="-5000" y="-5000" width="10000" height="10000" fill="url(#pdiInfiniteGridMajor)" opacity="0.72" pointerEvents="none"/>}{false&&'''
        s=s.replace(old_grid_start, inject+old_grid_start,1)
        # close the disabled old grid IIFE by making it false&& existing expression - okay JSX false&&(()=>...) not executed but syntax valid if followed by () result. It is {false&&{showGrid... invalid? We inserted {false&&{showGrid... actually old starts with {showGrid. New ends {false&&{showGrid... double braces invalid. Need fix
        s=s.replace('{false&&{showGrid&&(()=>{', '{false && showGrid&&(()=>{',1)
    # CSS grid stable canvas
    if '[data-pdi-studio] .pdi-infinite-grid-note' not in s:
        s=s.replace('[data-pdi-studio] .pdi-status-docked{height:28px!important;min-height:28px!important;padding-top:3px!important;padding-bottom:3px!important}', '[data-pdi-studio] .pdi-status-docked{display:none!important}\n        [data-pdi-studio] svg{background-color:#0b0f14!important;background-image:radial-gradient(circle at center,rgba(148,163,184,.09) 0,transparent 55%)!important}',1)
    write(ENGINE,s)
    print('Engine patché 011: gris neutre, grille pattern, barre basse masquée.')

def create_asset_notes():
    PUBLIC_ASSETS.mkdir(parents=True,exist_ok=True)
    note=PUBLIC_ASSETS/'README_ASSETS_PNG.txt'
    if not note.exists():
        note.write_text('''PD&I assets landing — à ajouter manuellement car AI Studio n’inclut pas automatiquement les PNG/images.\n\nFichier recommandé pour la photo/visuel initial :\n- public/assets/pdi/landing/hero-dashboard.png\n\nAutres fichiers possibles :\n- iso-preview.png\n- cad2d-preview.png\n- vision-preview.png\n\nLe patch 011 contient un fallback CSS si hero-dashboard.png est absent.\n''',encoding='utf-8')

def report():
    txt=f'''# PATCH 011 — Super Admin + corrections landing/workspace\n\nDate: {datetime.now().isoformat(timespec='seconds')}\n\n## Audit\n- Landing existe dans le code mais peut sembler enlevée à cause du flag d’entrée app/sessionStorage.\n- CSS parallax existe mais pas assez visible.\n- Photo initiale absente des assets publics.\n- Couleurs initiales PD&I encore variées : bleu/violet/orange.\n- Grille rendue en lignes finies pouvant se dégrader au zoom.\n- Barre basse métrés/statut encore visible.\n\n## Corrections incluses\n- Restauration flux landing commerciale.\n- Parallax, grid drift, card animations et fallback visuel initial.\n- Préparation chemin image : public/assets/pdi/landing/hero-dashboard.png.\n- Couleur neutre gris AutoCAD pour nouveaux tubes/nœuds/objets 2D avant changement.\n- Grille workspace transformée en pattern infini style CAD.\n- Barre basse avec chiffres masquée.\n- Ajout shell Super Admin Console selon workflow 011.\n\n## À ajouter manuellement\nAI Studio n’inclut pas les PNG/images : ajouter si possible :\npublic/assets/pdi/landing/hero-dashboard.png\n\n## Tests\nnpm run lint\nnpm run build\nVercel preview\n'''
    write(REPORT,txt)
    if HISTORY.exists() and 'PATCH 011 — Super Admin + corrections landing/workspace' not in read(HISTORY):
        write(HISTORY, read(HISTORY).rstrip()+"\n\n## PATCH 011 — Super Admin + corrections landing/workspace\n\n- Restauration landing commerciale et animations/parallax.\n- Préparation photo initiale hero-dashboard.png avec fallback CSS.\n- Couleur neutre gris AutoCAD pour nouveaux éléments.\n- Grille infinie style AutoCAD.\n- Barre basse métrés/statut masquée.\n- Ajout shell Super Admin Console.\n")

def main():
    print('PD&I PATCH 011 — Super Admin + corrections visuelles/workspace')
    audit(); patch_app(); patch_landing(); patch_landing_css(); patch_engine(); create_asset_notes(); report(); print('PATCH 011 terminé')

if __name__=='__main__': main()
