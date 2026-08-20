#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 008
Flux SaaS + onglets projet + UI compte + checklist sécurité.

À appliquer à la racine du projet.
Ne touche pas au moteur métier V4.8d : patch interface PdiUnifiedApp + landing CSS.
"""
from pathlib import Path
import shutil, sys
from datetime import datetime

ROOT=Path('.')
APP=ROOT/'src/pdi/app/PdiUnifiedApp.tsx'
LANDCSS=ROOT/'src/pdi/landing/pdiLandingV4.css'
REPORT=ROOT/'008_saas_tabs_security_ui_flow_REPORT.md'
HISTORY=ROOT/'docs/PATCH_HISTORY.md'
PATCH='008'
SECURITY=[
 'clés API dans .env', '.env dans .gitignore', 'rate limiting sur le login', 'RLS/règles sécurité activées',
 'mots de passe hashés', 'droits vérifiés côté serveur', 'clé publique côté client seulement', 'HTTPS partout',
 'sessions qui expirent', 'inputs validés', 'taille max des uploads', 'type de fichier vérifié', 'CORS configuré',
 'erreurs détaillées coupées', 'console.log clean', "message d'erreur unique", 'webhooks signés', 'dépendances à jour',
 'email confirmé', 'backup auto'
]

def fail(m): print('ABANDON: '+m); sys.exit(2)
def read(p): return p.read_text(encoding='utf-8')
def write(p,c): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(c,encoding='utf-8')
def backup(p):
    b=p.with_name(p.name+'.before008')
    if not b.exists(): shutil.copy2(p,b); print('Sauvegarde:',b)

def audit():
    if not APP.exists(): fail('PdiUnifiedApp.tsx introuvable')
    if not LANDCSS.exists(): fail('pdiLandingV4.css introuvable')
    s=read(APP)
    missing=[x for x in ['PdiLandingV4','PdiIsometricEditor','activeModule','pdi.stage.v4','pdi-account'] if x not in s]
    if missing: fail('audit incomplet: '+', '.join(missing))
    print('Audit OK: landing/app présentes, patch 008 prêt.')

def patch_app():
    s=read(APP); backup(APP)
    if 'PATCH 008 — SaaS tabs flow' in s:
        print('PdiUnifiedApp déjà patché'); return
    s='// PATCH 008 — SaaS tabs flow\n'+s
    s=s.replace('const PDI_STAGE_KEY = "pdi.stage.v4";', 'const PDI_STAGE_KEY = "pdi.stage.v4";\nconst PDI_TABS_KEY = "pdi.tabs.v1";\nconst PDI_ACTIVE_TAB_KEY = "pdi.activeTabId.v1";\nconst PDI_AUTH_KEY = "pdi.auth.mode.v1";',1)
    s=s.replace('type PdiModule = "home" | "isometric" | "vision" | "sketch" | "cad" | "json" | "pdf" | "projects" | "assistant";', 'type PdiModule = "home" | "isometric" | "vision" | "sketch" | "cad" | "json" | "pdf" | "projects" | "assistant";\ntype PdiWorkspaceTab = { id: string; title: string; module: PdiModule; projectId: string; dirty?: boolean; createdAt: string };',1)
    anchor='  const [activeModule, setActiveModule] = useState<PdiModule>("home");'
    if anchor in s:
        s=s.replace(anchor, anchor+r'''
  const [authMode, setAuthMode] = useState<"guest" | "demo" | "client" | "admin" | "super_admin">(() => { try { return (window.localStorage.getItem(PDI_AUTH_KEY) as any) || "demo"; } catch { return "demo"; } });
  const [accountMenuOpen, setAccountMenuOpen] = useState(false);
  const [workspaceTabs, setWorkspaceTabs] = useState<PdiWorkspaceTab[]>(() => { try { return JSON.parse(window.localStorage.getItem(PDI_TABS_KEY) || "[]"); } catch { return []; } });
  const [activeTabId, setActiveTabId] = useState<string | null>(() => { try { return window.localStorage.getItem(PDI_ACTIVE_TAB_KEY); } catch { return null; } });
  const persistTabs = (tabs: PdiWorkspaceTab[], id: string | null) => { try { window.localStorage.setItem(PDI_TABS_KEY, JSON.stringify(tabs)); if(id) window.localStorage.setItem(PDI_ACTIVE_TAB_KEY,id); } catch {} };
  const openModuleInTab = (module: PdiModule, title?: string) => {
    if (module === "home") { setActiveModule("home"); return; }
    const id = `tab-${Date.now().toString(36)}`;
    const next: PdiWorkspaceTab = { id, title: title || navItems.find(x=>x.id===module)?.title || "Projet PD&I", module, projectId: `project-${Date.now().toString(36)}`, dirty: false, createdAt: new Date().toISOString() };
    const tabs = [...workspaceTabs, next]; setWorkspaceTabs(tabs); setActiveTabId(id); setActiveModule(module); persistTabs(tabs,id);
  };
  const switchTab = (id: string) => { const tab = workspaceTabs.find(t=>t.id===id); if(!tab) return; setActiveTabId(id); setActiveModule(tab.module); persistTabs(workspaceTabs,id); };
  const closeTab = (id: string) => { const tabs = workspaceTabs.filter(t=>t.id!==id); const next = tabs[tabs.length-1] || null; setWorkspaceTabs(tabs); setActiveTabId(next?.id || null); setActiveModule(next?.module || "home"); persistTabs(tabs,next?.id || null); };
''',1)
    s=s.replace('  const moduleTitle = useMemo', '  useEffect(() => { try { window.localStorage.setItem(PDI_AUTH_KEY, authMode); } catch {} }, [authMode]);\n  useEffect(() => { const tab = workspaceTabs.find(t=>t.id===activeTabId); if(tab && activeModule === "home") setActiveModule(tab.module); }, []);\n\n  const moduleTitle = useMemo',1)
    s=s.replace('onClick={() => setActiveModule("isometric")}>Nouveau projet isométrique</button>', 'onClick={() => openModuleInTab("isometric", "Nouveau plan ISO")}>Nouveau projet isométrique</button>')
    s=s.replace('onClick={() => setActiveModule(card.id)} title={card.title}', 'onClick={() => openModuleInTab(card.id, card.title)} title={card.title}')
    s=s.replace('onClick={() => setActiveModule(item.id)} title={item.title}', 'onClick={() => item.id === "home" ? setActiveModule("home") : openModuleInTab(item.id, item.title)} title={item.title}')
    old='<div className="pdi-top-actions"><input className="pdi-search" placeholder="Rechercher une commande…" /><span>Essai</span><button className="pdi-account">Compte</button></div>'
    new='<div className="pdi-top-actions"><input className="pdi-search" placeholder="Rechercher une commande…" /><span className="pdi-auth-badge">{authMode.toUpperCase()}</span><button className="pdi-account" onClick={() => setAccountMenuOpen(v=>!v)}>Youcef ▾</button>{accountMenuOpen && <div className="pdi-account-menu"><button onClick={()=>setActiveModule("home")}>Accueil</button><button>Voir profil</button><button>Abonnement</button><button onClick={()=>setAuthMode("guest")}>Mode guest</button><button onClick={()=>{try{window.localStorage.removeItem(PDI_STAGE_KEY)}catch{}; setStage("landing");}}>Landing</button><button onClick={()=>{setAuthMode("guest"); setStage("landing");}}>Déconnexion</button></div>}</div>'
    if old in s: s=s.replace(old,new,1)
    nav='</nav>\n      <main className="pdi-content">'
    if nav in s:
        s=s.replace(nav, '</nav>\n      {workspaceTabs.length>0 && <div className="pdi-tabsbar">{workspaceTabs.map(tab=><button key={tab.id} className={activeTabId===tab.id?"active":""} onClick={()=>switchTab(tab.id)}>{tab.title}<span onClick={(e)=>{e.stopPropagation(); closeTab(tab.id)}}>×</span></button>)}<button className="plus" onClick={()=>openModuleInTab("isometric","Nouveau plan ISO")}>+</button></div>}\n      <main className="pdi-content">',1)
    if '.pdi-tabsbar' not in s:
        s=s.replace('@media(max-width:900px)', '.pdi-auth-badge{border:1px solid rgba(103,232,249,.35);background:rgba(14,165,233,.14);color:#67E8F9;border-radius:999px;padding:6px 10px;font-size:10px;font-weight:1000}.pdi-account{position:relative;background:linear-gradient(180deg,#123044,#0A1824)!important;border-color:#38BDF8!important}.pdi-account-menu{position:absolute;right:12px;top:58px;z-index:80;width:190px;background:#0B111A;border:1px solid rgba(103,232,249,.32);border-radius:14px;padding:7px;box-shadow:0 24px 60px rgba(0,0,0,.5)}.pdi-account-menu button{display:block;width:100%;height:34px;text-align:left;border:0;background:transparent;color:#DCEBFA;border-radius:8px;padding:0 10px;font-weight:800}.pdi-account-menu button:hover{background:#123044;color:white}.pdi-tabsbar{grid-column:2;grid-row:2;align-self:start;z-index:8;display:flex;gap:6px;padding:8px 14px;background:#080D14;border-bottom:1px solid rgba(148,163,184,.18);overflow:auto}.pdi-tabsbar button{height:30px;border-radius:8px;border:1px solid #263241;background:linear-gradient(180deg,#1E293B,#111827);color:#CBD5E1;font-size:11px;font-weight:900;padding:0 9px;display:flex;align-items:center;gap:8px;animation:pdiTabIn .2s ease}.pdi-tabsbar button.active{background:linear-gradient(135deg,#0284C7,#22D3EE);color:white;border-color:#67E8F9}.pdi-tabsbar button span{opacity:.65}.pdi-tabsbar .plus{min-width:34px;justify-content:center}.pdi-launch-card{background:linear-gradient(180deg,#1B2430,#101722)!important;border-color:rgba(77,184,212,.36)!important;box-shadow:0 16px 38px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.04)!important}.pdi-launch-card:hover{transform:translateY(-3px) scale(1.01);border-color:#67E8F9!important;box-shadow:0 24px 50px rgba(14,165,233,.18)!important}@keyframes pdiTabIn{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}@media(max-width:900px)',1)
    write(APP,s)

def patch_css():
    s=read(LANDCSS); backup(LANDCSS)
    if 'PATCH 008 buttons animations' in s: return
    s+='''\n/* PATCH 008 buttons animations */\n.pdiL-entry{background:linear-gradient(180deg,#1B2430,#101722)!important;border-color:rgba(77,184,212,.36)!important;box-shadow:0 16px 38px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.04)!important}\n.pdiL-entry:hover,.pdiL-entry.selected{transform:translateY(-3px) scale(1.01)!important;border-color:var(--entry,#67E8F9)!important;box-shadow:0 24px 55px rgba(77,184,212,.18)!important}\n.pdiL-launcher-head button,.pdiL-btn{box-shadow:0 10px 28px rgba(0,0,0,.25)}\n.pdiL-splash,.pdiL-entry,.pdiL-homehero{animation:pdiFadeUp .45s ease both}\n@keyframes pdiFadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}\n'''
    write(LANDCSS,s)

def report():
    txt='# PATCH 008 — Flux SaaS + onglets + sécurité\n\nDate: '+datetime.now().isoformat(timespec='seconds')+'\n\n## Checklist sécurité photos\n'+'\n'.join(f'{i+1}. {x}' for i,x in enumerate(SECURITY))+'\n\n## Note assets\nAI Studio n’inclut pas automatiquement les PNG/images. Ajouter manuellement les assets dans public/assets/pdi/ ou src/assets/images avant build/sync GitHub.\n\n## Tests\n- npm run lint\n- npm run build\n- Vercel preview\n'
    write(REPORT,txt)
    if HISTORY.exists() and 'PATCH 008 — Flux SaaS' not in read(HISTORY):
        write(HISTORY, read(HISTORY).rstrip()+'\n\n## PATCH 008 — Flux SaaS + onglets + sécurité\n\n- Onglets projet persistants.\n- Menu compte/profil.\n- Boutons noirs corrigés.\n- Checklist sécurité SaaS ajoutée.\n- Note assets PNG ajoutée.\n')

def main():
    print('PD&I PATCH 008')
    audit(); patch_app(); patch_css(); report(); print('PATCH 008 terminé')
if __name__=='__main__': main()
