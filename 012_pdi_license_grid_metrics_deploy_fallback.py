#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 012
Licences SaaS + correction grille/métrés + stratégie déploiement hors Vercel.

À lancer à la racine du repo : python3 012_pdi_license_grid_metrics_deploy_fallback.py
"""
from pathlib import Path
import shutil, sys, json
from datetime import datetime

ROOT=Path('.')
APP=ROOT/'src/pdi/app/PdiUnifiedApp.tsx'
ENGINE=ROOT/'src/pdi/isometric/engine/IsometrieModuleV48d.tsx'
UXCSS=ROOT/'src/pdiIsoPrecisionUx.css'
HISTORY=ROOT/'docs/PATCH_HISTORY.md'
REPORT=ROOT/'012_license_grid_metrics_deploy_fallback_REPORT.md'
DEPLOY=ROOT/'docs/DEPLOYMENT_ENTERPRISE_FALLBACK.md'

def fail(m): print('ABANDON: '+m); sys.exit(2)
def read(p): return p.read_text(encoding='utf-8')
def write(p,c): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(c, encoding='utf-8')
def backup(p):
    if p.exists():
        b=p.with_name(p.name+'.before012')
        if not b.exists(): shutil.copy2(p,b)
        print('backup', b)

def audit():
    for p in [APP, ENGINE]:
        if not p.exists(): fail(f'fichier introuvable: {p}')
    app=read(APP); eng=read(ENGINE)
    print('Audit PATCH 011:', 'PATCH 011' in app or 'PATCH 011' in eng)
    print('Ancienne grille dynamique:', 'Dynamic Infinite Zoom/Pan-Aware Drafting Grid' in eng)
    print('Cartes métrés détectables:', any(x in eng for x in ['MÈTRE TUBE','VOL. ÉPREUVE','ÉPREUVE','0.0 kg','60.0 bar']))
    print('Status docked:', 'pdi-status-docked' in eng)

def patch_app():
    s=read(APP); backup(APP)
    if 'PATCH 012 — license keys and deployment fallback' not in s:
        s='// PATCH 012 — license keys and deployment fallback\n'+s
    if '"license_keys"' not in s:
        s=s.replace('"super_admin_console";', '"super_admin_console" | "license_keys";', 1)
    if 'licenseKeys, setLicenseKeys' not in s:
        anchor='  const pdiUserProfile = {'
        idx=s.find(anchor)
        if idx!=-1:
            end=s.find('  };', idx)+5
            block=r'''
  const [licenseKeys, setLicenseKeys] = useState<Array<{ id:string; code:string; type:string; plan:string; status:string; email:string; createdAt:string; expiresAt:string }>>(() => {
    try { return JSON.parse(window.localStorage.getItem("pdi.license.keys.v1") || "[]"); } catch { return []; }
  });
  const [licenseDraft, setLicenseDraft] = useState({ type:"TRIAL_30", plan:"PRO", email:"" });
  const persistLicenseKeys = (keys: typeof licenseKeys) => { setLicenseKeys(keys); try { window.localStorage.setItem("pdi.license.keys.v1", JSON.stringify(keys)); } catch {} };
  const generateLicenseKey = () => {
    const id = `lic-${Date.now().toString(36)}`;
    const code = `PDI-${licenseDraft.type}-${Math.random().toString(36).slice(2,6).toUpperCase()}-${Date.now().toString(36).toUpperCase()}`;
    const days = licenseDraft.type.includes("7") ? 7 : licenseDraft.type.includes("30") ? 30 : licenseDraft.type.includes("YEAR") ? 365 : 90;
    const expiresAt = new Date(Date.now()+days*86400000).toISOString().slice(0,10);
    persistLicenseKeys([{ id, code, type:licenseDraft.type, plan:licenseDraft.plan, status:"generated", email:licenseDraft.email, createdAt:new Date().toISOString().slice(0,10), expiresAt }, ...licenseKeys]);
  };
  const revokeLicenseKey = (id:string) => persistLicenseKeys(licenseKeys.map(k=>k.id===id?{...k,status:"revoked"}:k));
'''
            s=s[:end]+block+s[end:]
    marker='<button onClick={()=>{setAuthMode("super_admin"); setActiveModule("super_admin_console")}}>Super Admin</button>'
    if marker in s and 'setActiveModule("license_keys")' not in s:
        s=s.replace(marker, marker+'<button onClick={()=>{setAuthMode("super_admin"); setActiveModule("license_keys")}}>Clés SaaS</button>',1)
    anchor_panel='        {activeModule === "assistant" && <ComingSoonPanel title="Assistant et agents spécialisés"><p>PD&I orchestrera le repo <code>pipeline-design-skill</code> : agents Vision, Croquis, CAO, JSON, ISO, QA. Les agents proposent ; Python calcule.</p></ComingSoonPanel>}'
    if 'Générateur de clés SaaS' not in s and anchor_panel in s:
        panel=r'''
        {activeModule === "license_keys" && <ComingSoonPanel title="Générateur de clés SaaS">
          <div className="pdi-license-panel">
            <section className="pdi-license-form"><h3>Créer une clé</h3><label>Type<select value={licenseDraft.type} onChange={e=>setLicenseDraft({...licenseDraft,type:e.target.value})}><option>TRIAL_7</option><option>TRIAL_30</option><option>GUEST</option><option>SOLO_MONTHLY</option><option>SOLO_YEARLY</option><option>PRO_MONTHLY</option><option>PRO_YEARLY</option><option>TEAM_MONTHLY</option><option>TEAM_YEARLY</option><option>ENTERPRISE</option><option>ADMIN_INVITE</option><option>SUPER_ADMIN</option></select></label><label>Plan<select value={licenseDraft.plan} onChange={e=>setLicenseDraft({...licenseDraft,plan:e.target.value})}><option>DEMO</option><option>GUEST</option><option>SOLO</option><option>PRO</option><option>TEAM</option><option>ENTERPRISE</option></select></label><label>Email assigné<input value={licenseDraft.email} onChange={e=>setLicenseDraft({...licenseDraft,email:e.target.value})} placeholder="client@email.com" /></label><button onClick={generateLicenseKey}>Générer clé</button><small>Flux futur : demande → paiement → génération compte → email activation unique.</small></section>
            <section className="pdi-license-list"><h3>Clés générées</h3>{licenseKeys.length===0?<p>Aucune clé générée.</p>:licenseKeys.map(k=><div key={k.id} className="pdi-license-row"><code>{k.code}</code><span>{k.type}</span><span>{k.plan}</span><span>{k.email || "non assignée"}</span><span>{k.status}</span><span>exp. {k.expiresAt}</span><button onClick={()=>navigator.clipboard?.writeText(k.code)}>Copier</button><button onClick={()=>revokeLicenseKey(k.id)}>Révoquer</button></div>)}</section>
          </div>
        </ComingSoonPanel>}
'''
        s=s.replace(anchor_panel, panel+'\n'+anchor_panel,1)
    if '.pdi-license-panel' not in s:
        s=s.replace('@media(max-width:900px)', '.pdi-license-panel{display:grid;grid-template-columns:minmax(260px,.34fr) 1fr;gap:14px}.pdi-license-form,.pdi-license-list{border:1px solid rgba(103,232,249,.25);background:linear-gradient(180deg,#111827,#0B111A);border-radius:18px;padding:16px}.pdi-license-form h3,.pdi-license-list h3{margin:0 0 12px;color:#67E8F9}.pdi-license-form{display:grid;gap:10px}.pdi-license-form label{display:grid;gap:4px;color:#94A3B8;font-size:11px;font-weight:900;text-transform:uppercase}.pdi-license-form input,.pdi-license-form select{height:36px;border-radius:10px;background:#07111D!important;color:#E6F4FF!important;border:1px solid rgba(148,163,184,.28)!important;padding:0 10px}.pdi-license-form button,.pdi-license-row button{border:1px solid rgba(103,232,249,.35);background:linear-gradient(135deg,#0284C7,#22D3EE);color:white;border-radius:10px;padding:8px 10px;font-weight:1000}.pdi-license-list{display:grid;gap:8px;align-content:start}.pdi-license-row{display:grid;grid-template-columns:1.8fr .8fr .7fr 1.2fr .7fr .8fr auto auto;gap:7px;align-items:center;border:1px solid rgba(148,163,184,.16);background:#0B111A;border-radius:12px;padding:8px;font-size:10px}.pdi-license-row code{color:#A7F3D0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}@media(max-width:900px)',1)
    write(APP,s)

def patch_engine():
    s=read(ENGINE); backup(ENGINE)
    if 'PATCH 012 — grid metrics cleanup' not in s:
        s='// PATCH 012 — grid metrics cleanup\n'+s
    old_start=s.find('              {/* Dynamic Infinite Zoom/Pan-Aware Drafting Grid */}')
    if old_start!=-1:
        old_end=s.find('\n\n              <g>', old_start)
        if old_end!=-1:
            new='''              {/* PATCH 012 — Stable AutoCAD-like infinite grid */}
              <defs>
                <pattern id="pdiGridMinor" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform={`translate(${viewport.panX % 24} ${viewport.panY % 24})`}>
                  <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#334155" strokeWidth="0.45" opacity="0.42" />
                </pattern>
                <pattern id="pdiGridMajor" width="120" height="120" patternUnits="userSpaceOnUse" patternTransform={`translate(${viewport.panX % 120} ${viewport.panY % 120})`}>
                  <rect width="120" height="120" fill="url(#pdiGridMinor)" />
                  <path d="M 120 0 L 0 0 0 120" fill="none" stroke="#64748b" strokeWidth="0.85" opacity="0.42" />
                </pattern>
              </defs>
              {showGrid && <rect x="-5000" y="-5000" width="10000" height="10000" fill="url(#pdiGridMajor)" opacity="0.88" pointerEvents="none" />}
'''
            s=s[:old_start]+new+s[old_end:]
    # Hide status and metric cards from screenshot
    inject='''
        /* PATCH 012 — suppress bottom metric cards/status requested */
        [data-pdi-studio] .pdi-status-docked,
        [data-pdi-studio] .pdi-bottom-meter,
        [data-pdi-studio] [class*="bottom-meter"],
        [data-pdi-studio] [class*="metric"],
        [data-pdi-studio] [class*="meter"]{display:none!important}
'''
    if 'PATCH 012 — suppress bottom metric cards/status requested' not in s:
        pos=s.find('        [data-pdi-studio] .pdi-status-docked{display:none!important}')
        if pos!=-1:
            s=s[:pos]+inject+s[pos:]
        else:
            s=s.replace('</style>', inject+'</style>',1)
    # direct textual hiding for known labels if present
    for label in ['MÈTRE TUBE','VOL. ÉPREUVE','ÉPREUVE']:
        s=s.replace(label, '')
    write(ENGINE,s)

def patch_css():
    if UXCSS.exists():
        s=read(UXCSS); backup(UXCSS)
        if 'PATCH 012 — hide lower metric strip' not in s:
            s += '\n/* PATCH 012 — hide lower metric strip */\n.pdi-bottom-meter,[class*="pdi-bottom-meter"],[data-pdi-studio] [class*="bottom-meter"]{display:none!important}\n'
        write(UXCSS,s)

def docs():
    write(DEPLOY, '''# Déploiement PD&I — réseau entreprise sans Vercel

## Problème constaté
- Vercel ne fonctionne pas sur le réseau entreprise.
- Pas d'accès firewall.
- AI Studio fonctionne mais le quota `europe-west1` est saturé.

## Stratégie recommandée maintenant

### Option A — Build statique exportable ZIP, prioritaire
1. Construire localement ou dans AI Studio : `npm run build`.
2. Récupérer le dossier `dist/`.
3. Ouvrir l'app sur un poste autorisé ou l'héberger sur un serveur interne/NAS/IIS/Apache/Nginx.
4. Avantage : pas besoin Vercel, pas besoin firewall sortant vers Vercel.

### Option B — Google Cloud Run autre région
Si AI Studio/Google Cloud est le seul accès utilisable :
- éviter `europe-west1` saturé.
- essayer : `europe-west2`, `europe-west3`, `europe-west4`, `me-west1`, `us-central1`.
- garder Firebase côté client via variables `VITE_FIREBASE_*`.

### Option C — GitHub Pages pour version statique
- possible si le réseau entreprise ne bloque pas github.io.
- adapté au front React statique.
- moins adapté aux APIs serveur Express.

### Option D — Archive HTML autonome pour démonstration
- créer une build offline limitée.
- utile pour démonstration client/interne.
- pas de backend réel.

## Décision provisoire
Continuer développement via patches + GitHub, mais préparer une sortie `dist/` autonome pour éviter dépendance à Vercel.
''')
    write(REPORT, f'''# PATCH 012 — Audit + licences + grille/métrés + déploiement alternatif

Date: {datetime.now().isoformat(timespec='seconds')}

## Audit version 8
- PATCH 011 présent.
- PATCH 012 non présent dans le ZIP fourni.
- Ancienne grille dynamique encore détectée.
- Barre status masquée, mais les cartes métrés visibles sur capture restent à supprimer/masquer.
- Vercel non adapté au réseau entreprise actuel.

## Patch 012
- Ajoute générateur de clés SaaS local temporaire.
- Remplace grille dynamique par pattern SVG stable.
- Masque status + cartes métrés basses.
- Ajoute document de stratégie déploiement hors Vercel.

## Déploiement recommandé
Priorité : build statique ZIP `dist/`, puis hébergement interne ou Cloud Run autre région si nécessaire.
''')
    if HISTORY.exists() and 'PATCH 012 — Licences, grille, métrés, déploiement fallback' not in read(HISTORY):
        write(HISTORY, read(HISTORY).rstrip()+'''\n\n## PATCH 012 — Licences, grille, métrés, déploiement fallback\n\n- Ajout générateur local de clés SaaS.\n- Correction grille SVG stable type AutoCAD.\n- Masquage cartes métrés/barre basse visibles.\n- Ajout stratégie déploiement hors Vercel pour réseau entreprise.\n''')

def main():
    audit(); patch_app(); patch_engine(); patch_css(); docs(); print('PATCH 012 prêt/appliqué.')
if __name__=='__main__': main()
