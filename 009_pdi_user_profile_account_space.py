#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 009
Espace profil utilisateur + menu compte structuré.

Pré-requis : PATCH 008 appliqué.
Objectif : ajouter un vrai espace profil utilisateur sans toucher au moteur V4.8d.

Ajouts :
- module/profile dans l'état UI ;
- page profil utilisateur ;
- menu compte : Voir profil, Mes projets, Abonnement, Sécurité, Déconnexion ;
- carte identité : nom, email, rôle, mode, abonnement, activation email ;
- base future Firebase : users/profiles/subscriptions ;
- checklist sécurité visible dans profil/sécurité ;
- rapport journalier avec note assets PNG.
"""
from pathlib import Path
import shutil, sys
from datetime import datetime

ROOT=Path('.')
APP=ROOT/'src/pdi/app/PdiUnifiedApp.tsx'
REPORT=ROOT/'009_user_profile_account_space_REPORT.md'
HISTORY=ROOT/'docs/PATCH_HISTORY.md'
PATCH='009'
SECURITY=[
 'clés API dans .env', '.env dans .gitignore', 'rate limiting login', 'RLS/règles base',
 'mots de passe hashés', 'droits serveur', 'clé publique côté client', 'HTTPS partout',
 'sessions expirantes', 'inputs validés', 'taille max uploads', 'type fichier vérifié', 'CORS',
 'erreurs détaillées coupées', 'console.log clean', "message d'erreur unique", 'webhooks signés',
 'dépendances à jour', 'email confirmé', 'backup automatique'
]

def fail(m): print('ABANDON: '+m); sys.exit(2)
def read(p): return p.read_text(encoding='utf-8')
def write(p,c): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(c,encoding='utf-8')
def backup(p):
    b=p.with_name(p.name+'.before009')
    if not b.exists(): shutil.copy2(p,b); print('Sauvegarde:',b)

def audit():
    if not APP.exists(): fail('PdiUnifiedApp.tsx introuvable')
    s=read(APP)
    req=['PATCH 008','PdiWorkspaceTab','pdi-account-menu','authMode','workspaceTabs']
    missing=[x for x in req if x not in s]
    if missing: fail('PATCH 008 incomplet/manquant: '+', '.join(missing))
    print('Audit OK: PATCH 008 détecté. Passage PATCH 009 possible.')

def patch_app():
    s=read(APP); backup(APP)
    if 'PATCH 009 — User profile account space' in s:
        print('PdiUnifiedApp déjà patché 009'); return
    s='// PATCH 009 — User profile account space\n'+s
    # Etendre PdiModule avec profile/subscription/security si pas fait
    old='type PdiModule = "home" | "isometric" | "vision" | "sketch" | "cad" | "json" | "pdf" | "projects" | "assistant";'
    new='type PdiModule = "home" | "isometric" | "vision" | "sketch" | "cad" | "json" | "pdf" | "projects" | "assistant" | "profile" | "subscription" | "security";'
    if old in s: s=s.replace(old,new,1)
    # Ajouter profile state après authMode state
    anchor='  const [accountMenuOpen, setAccountMenuOpen] = useState(false);'
    if anchor in s and 'pdiUserProfile' not in s:
        s=s.replace(anchor, anchor+r'''
  const pdiUserProfile = {
    name: "Youcef Seif Eddine Boudjada",
    email: "boudjada.youcef@gmail.com",
    role: authMode,
    company: "PD&I Vision DZ",
    country: "Algérie",
    plan: authMode === "guest" ? "Guest" : authMode === "demo" ? "Demo" : "Pro",
    emailStatus: "confirmé",
    createdAt: "2026-08-20",
  };
''',1)
    # Menu account remplacer boutons simples
    s=s.replace('<button>Voir profil</button><button>Abonnement</button>', '<button onClick={()=>setActiveModule("profile")}>Voir profil</button><button onClick={()=>setActiveModule("projects")}>Mes projets</button><button onClick={()=>setActiveModule("subscription")}>Abonnement</button><button onClick={()=>setActiveModule("security")}>Sécurité</button>')
    # Ajouter panels avant assistant ou avant fin modules
    anchor_panel='        {activeModule === "assistant" && <ComingSoonPanel title="Assistant et agents spécialisés"><p>PD&I orchestrera le repo <code>pipeline-design-skill</code> : agents Vision, Croquis, CAO, JSON, ISO, QA. Les agents proposent ; Python calcule.</p></ComingSoonPanel>}'
    profile_panel=r'''
        {activeModule === "profile" && <ComingSoonPanel title="Profil utilisateur">
          <div className="pdi-profile-grid">
            <section className="pdi-profile-card"><h3>Identité</h3><p><b>Nom</b><span>{pdiUserProfile.name}</span></p><p><b>Email</b><span>{pdiUserProfile.email}</span></p><p><b>Entreprise</b><span>{pdiUserProfile.company}</span></p><p><b>Pays</b><span>{pdiUserProfile.country}</span></p></section>
            <section className="pdi-profile-card"><h3>Compte</h3><p><b>Rôle</b><span>{String(pdiUserProfile.role).toUpperCase()}</span></p><p><b>Plan</b><span>{pdiUserProfile.plan}</span></p><p><b>Email</b><span>{pdiUserProfile.emailStatus}</span></p><p><b>Créé le</b><span>{pdiUserProfile.createdAt}</span></p></section>
            <section className="pdi-profile-card wide"><h3>Actions</h3><div className="pdi-profile-actions"><button onClick={()=>setActiveModule("projects")}>Mes projets</button><button onClick={()=>setActiveModule("subscription")}>Mon abonnement</button><button onClick={()=>setActiveModule("security")}>Sécurité</button><button onClick={()=>{setAuthMode("guest"); setStage("landing");}}>Déconnexion</button></div></section>
          </div>
        </ComingSoonPanel>}
        {activeModule === "subscription" && <ComingSoonPanel title="Abonnement"><p>Plan actuel : <b>{pdiUserProfile.plan}</b>. Les clés SaaS, paiements et renouvellements seront reliés au Super Admin dans les patchs 011 à 016.</p></ComingSoonPanel>}
        {activeModule === "security" && <ComingSoonPanel title="Sécurité du compte"><div className="pdi-security-list">{['clés API dans .env','.env dans .gitignore','rate limiting login','règles sécurité base','mots de passe hashés','droits serveur','HTTPS','sessions expirantes','inputs validés','uploads limités','type fichier vérifié','CORS','erreurs détaillées coupées','console.log clean','message erreur unique','webhooks signés','dépendances à jour','email confirmé','backup auto'].map((item,i)=><span key={item}>{i+1}. {item}</span>)}</div></ComingSoonPanel>}
'''
    if anchor_panel in s and 'Profil utilisateur' not in s:
        s=s.replace(anchor_panel, profile_panel+'\n'+anchor_panel,1)
    # Styles
    if '.pdi-profile-grid' not in s:
        s=s.replace('@media(max-width:900px)', '.pdi-profile-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.pdi-profile-card{border:1px solid rgba(148,163,184,.22);background:linear-gradient(180deg,#111827,#0B111A);border-radius:18px;padding:16px}.pdi-profile-card.wide{grid-column:1/-1}.pdi-profile-card h3{margin:0 0 12px;color:#67E8F9}.pdi-profile-card p{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid rgba(148,163,184,.12);padding:8px 0;margin:0}.pdi-profile-card b{color:#94A3B8}.pdi-profile-card span{color:#F8FAFC;font-weight:900}.pdi-profile-actions{display:flex;flex-wrap:wrap;gap:8px}.pdi-profile-actions button{border:1px solid rgba(103,232,249,.35);background:#0A1824;color:#E0F2FE;border-radius:10px;padding:9px 12px;font-weight:900}.pdi-security-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.pdi-security-list span{border:1px solid rgba(148,163,184,.18);background:#0B111A;border-radius:10px;padding:9px;color:#D1E7F8;font-weight:800;font-size:12px}@media(max-width:900px)',1)
    write(APP,s)
    print('PdiUnifiedApp patché 009')

def report():
    txt='# PATCH 009 — Profil utilisateur + espace compte\n\nDate: '+datetime.now().isoformat(timespec='seconds')+'\n\n## Audit\nPATCH 008 détecté : onglets, authMode, menu compte.\n\n## Ajouts\n- Module Profil utilisateur.\n- Menu compte enrichi : Voir profil, Mes projets, Abonnement, Sécurité, Déconnexion.\n- Carte identité et carte compte.\n- Page sécurité avec checklist SaaS.\n- Préparation future Firebase users/profiles/subscriptions.\n\n## Checklist sécurité conservée\n'+'\n'.join(f'{i+1}. {x}' for i,x in enumerate(SECURITY))+'\n\n## Note assets\nAI Studio n’inclut pas automatiquement les PNG/images. Ajouter manuellement les assets dans public/assets/pdi/ ou src/assets/images avant build/sync GitHub.\n\n## Tests\n- npm run lint\n- npm run build\n- Vercel preview\n'
    write(REPORT,txt)
    if HISTORY.exists() and 'PATCH 009 — Profil utilisateur' not in read(HISTORY):
        write(HISTORY, read(HISTORY).rstrip()+'\n\n## PATCH 009 — Profil utilisateur + espace compte\n\n- Ajout module Profil utilisateur.\n- Menu compte enrichi.\n- Page sécurité avec checklist SaaS.\n- Préparation Firebase users/profiles/subscriptions.\n')

def main():
    print('PD&I PATCH 009 — Profil utilisateur')
    audit(); patch_app(); report(); print('PATCH 009 terminé')
if __name__=='__main__': main()
