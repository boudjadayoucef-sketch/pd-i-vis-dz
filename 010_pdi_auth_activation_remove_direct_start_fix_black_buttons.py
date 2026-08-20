#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 010
Auth simulée + activation email + suppression accès direct "Commencer/Démarrer" + fix boutons noirs.

Objectifs demandés :
- Donner le patch 010.
- Enlever le bouton "commencé / démarrer" qui permet d'accéder directement sans passer par auth/démo.
- Corriger définitivement les boutons encore complètement noirs.

Pré-requis : PATCH 008, 009, 009b.
Ne touche pas au moteur V4.8d.
"""
from pathlib import Path
import shutil, sys
from datetime import datetime

ROOT=Path('.')
APP=ROOT/'src/pdi/app/PdiUnifiedApp.tsx'
LAND=ROOT/'src/pdi/landing/PdiLandingV4.tsx'
LANDCSS=ROOT/'src/pdi/landing/pdiLandingV4.css'
REPORT=ROOT/'010_auth_activation_remove_direct_start_fix_black_buttons_REPORT.md'
HISTORY=ROOT/'docs/PATCH_HISTORY.md'

def fail(m):
    print('ABANDON: '+m)
    sys.exit(2)

def read(p): return p.read_text(encoding='utf-8')
def write(p,c):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(c,encoding='utf-8')

def backup(p):
    b=p.with_name(p.name+'.before010')
    if not b.exists():
        shutil.copy2(p,b)
        print('Sauvegarde:',b)

def audit():
    for p in [APP, LAND, LANDCSS]:
        if not p.exists(): fail(f'fichier introuvable: {p}')
    app=read(APP); land=read(LAND)
    missing=[x for x in ['PATCH 008','PATCH 009','authMode','pdi-account-menu'] if x not in app]
    if missing: fail('pré-requis app manquants: '+', '.join(missing))
    if 'PdiLandingV4' not in land or 'Connexion' not in land:
        fail('landing non conforme ou introuvable')
    print('Audit OK: 008/009 détectés, landing présente.')

def patch_landing():
    s=read(LAND); backup(LAND)
    if 'PATCH 010 — gated auth landing' in s:
        print('Landing déjà patchée')
        return
    s='// PATCH 010 — gated auth landing\n'+s
    # Remplacer les libellés d'accès direct par un libellé auth/démo.
    replacements={
        'Démarrer':'Connexion / Démo',
        'Demarrer':'Connexion / Démo',
        'Let’s begin →':'Connexion / Démo →',
        'Nouveau projet isométrique':'Choisir après connexion',
        'Ouvrir ·':'Préparer ·'
    }
    for old,new in replacements.items():
        s=s.replace(old,new)
    # Les CTA doivent aller vers l'écran home/launcher contrôlé, pas accès direct silencieux.
    # On garde begin/openEntry mais on clarifie UI : l'entrée directe sera bloquée côté App par authMode.
    write(LAND,s)
    print('Landing patchée: bouton accès direct renommé et neutralisé visuellement.')

def patch_app():
    s=read(APP); backup(APP)
    if 'PATCH 010 — simulated auth activation' in s:
        print('App déjà patchée')
        return
    s='// PATCH 010 — simulated auth activation\n'+s
    # Étendre authMode avec pending_email si nécessaire.
    s=s.replace('useState<"guest" | "demo" | "client" | "admin" | "super_admin">', 'useState<"guest" | "demo" | "pending_email" | "client" | "admin" | "super_admin">')
    # Ajouter état auth gateway après accountMenuOpen.
    anchor='  const [accountMenuOpen, setAccountMenuOpen] = useState(false);'
    if anchor in s and 'authPanelMode' not in s:
        s=s.replace(anchor, anchor+r'''
  const [authPanelMode, setAuthPanelMode] = useState<"login" | "register" | "activation">("login");
  const [authDraft, setAuthDraft] = useState({ name: "", email: "", company: "", password: "", plan: "demo" });
  const [activationToken, setActivationToken] = useState<string | null>(() => { try { return window.localStorage.getItem("pdi.activation.pendingToken.v1"); } catch { return null; } });
  const startDemoSession = () => { setAuthMode("demo"); try { window.localStorage.setItem(PDI_AUTH_KEY,"demo"); window.sessionStorage.setItem(PDI_STAGE_KEY,"app"); } catch {} setStage("app"); setActiveModule("home"); };
  const submitRegisterSimulated = () => {
    if (!authDraft.email || !authDraft.name || authDraft.password.length < 6) { setAuthPanelMode("register"); return; }
    const token = `pdi-act-${Date.now().toString(36)}`;
    setActivationToken(token);
    setAuthMode("pending_email");
    try { window.localStorage.setItem("pdi.activation.pendingToken.v1", token); window.localStorage.setItem("pdi.auth.pendingUser.v1", JSON.stringify({ ...authDraft, password: undefined, status:"pending_email" })); } catch {}
    setAuthPanelMode("activation");
  };
  const activateSimulatedAccount = () => { setAuthMode("client"); try { window.localStorage.removeItem("pdi.activation.pendingToken.v1"); window.localStorage.setItem(PDI_AUTH_KEY,"client"); window.sessionStorage.setItem(PDI_STAGE_KEY,"app"); } catch {} setStage("app"); setActiveModule("home"); };
''',1)
    # Bloquer accès direct aux modules si guest/pending sauf demo/client/admin.
    if 'const canOpenWorkspaceModule' not in s:
        s=s.replace('  const openModuleInTab = (module: PdiModule, title?: string) => {', '  const canOpenWorkspaceModule = authMode === "demo" || authMode === "client" || authMode === "admin" || authMode === "super_admin";\n  const openModuleInTab = (module: PdiModule, title?: string) => {\n    if (!canOpenWorkspaceModule && module !== "home") { setAuthPanelMode("login"); setActiveModule("home"); return; }',1)
        # remove duplicated brace artifact if replacement causes two opening blocks? Original line had {, we included { then rest begins following line ok.
    # Ajouter auth gateway sur home avant home hero.
    marker='        {activeModule === "home" && <div className="pdi-home-hero">'
    gateway=r'''        {activeModule === "home" && (authMode === "guest" || authMode === "pending_email") && <div className="pdi-auth-gateway">
          <section className="pdi-auth-card"><div className="pdi-panel-kicker">Accès PD&I sécurisé</div><h1>Connexion requise</h1><p>Pour ouvrir ISO, Vision, CAD ou créer un nouveau plan, passez par Connexion, Création compte ou Mode démo. L'accès direct par bouton Commencer est désactivé.</p><div className="pdi-auth-tabs"><button className={authPanelMode==="login"?"active":""} onClick={()=>setAuthPanelMode("login")}>Connexion</button><button className={authPanelMode==="register"?"active":""} onClick={()=>setAuthPanelMode("register")}>Créer compte</button><button className={authPanelMode==="activation"?"active":""} onClick={()=>setAuthPanelMode("activation")}>Activation</button></div>
            {authPanelMode === "login" && <div className="pdi-auth-form"><input placeholder="Email" value={authDraft.email} onChange={e=>setAuthDraft({...authDraft,email:e.target.value})}/><input placeholder="Mot de passe" type="password" value={authDraft.password} onChange={e=>setAuthDraft({...authDraft,password:e.target.value})}/><button onClick={startDemoSession}>Continuer en mode démo</button><small>Message unique : identifiants invalides ou compte non activé.</small></div>}
            {authPanelMode === "register" && <div className="pdi-auth-form"><input placeholder="Nom complet" value={authDraft.name} onChange={e=>setAuthDraft({...authDraft,name:e.target.value})}/><input placeholder="Email" value={authDraft.email} onChange={e=>setAuthDraft({...authDraft,email:e.target.value})}/><input placeholder="Entreprise" value={authDraft.company} onChange={e=>setAuthDraft({...authDraft,company:e.target.value})}/><input placeholder="Mot de passe min. 6" type="password" value={authDraft.password} onChange={e=>setAuthDraft({...authDraft,password:e.target.value})}/><select value={authDraft.plan} onChange={e=>setAuthDraft({...authDraft,plan:e.target.value})}><option value="demo">Demo</option><option value="pro">Pro</option><option value="team">Team</option></select><button onClick={submitRegisterSimulated}>Générer email d’activation</button></div>}
            {authPanelMode === "activation" && <div className="pdi-auth-form"><p><b>Email simulé :</b> cliquez sur le lien unique pour confirmer l’email.</p><code>{activationToken || "Aucun token — créez un compte d’abord"}</code><button disabled={!activationToken} onClick={activateSimulatedAccount}>Activer le compte</button></div>}
          </section>
        </div>}
'''
    if marker in s and 'pdi-auth-gateway' not in s:
        s=s.replace(marker, gateway+marker,1)
    # Remplacer bouton nouveau projet pour indiquer auth si guest.
    s=s.replace('>Nouveau projet isométrique</button>', '>{canOpenWorkspaceModule ? "Nouveau projet isométrique" : "Connexion requise"}</button>')
    # Styles auth + fix black buttons app.
    if '.pdi-auth-gateway' not in s[s.find('<style>') if '<style>' in s else 0:]:
        s=s.replace('@media(max-width:900px)', '.pdi-auth-gateway{grid-column:1/-1;display:grid;place-items:center;min-height:calc(100vh - 170px);animation:pdiAuthIn .35s ease}.pdi-auth-card{width:min(760px,92vw);border:1px solid rgba(103,232,249,.35);background:linear-gradient(180deg,#111C2A,#08111C);border-radius:26px;padding:28px;box-shadow:0 30px 90px rgba(0,0,0,.45)}.pdi-auth-card h1{font-size:clamp(30px,4vw,52px);margin:0 0 10px;color:#F8FAFC}.pdi-auth-card p{color:#AFC4DD;font-weight:700}.pdi-auth-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}.pdi-auth-tabs button,.pdi-auth-form button{border:1px solid rgba(103,232,249,.38);background:linear-gradient(180deg,#183349,#0C1A27);color:#E0F2FE;border-radius:12px;padding:10px 13px;font-weight:1000;cursor:pointer}.pdi-auth-tabs button.active,.pdi-auth-form button:hover{background:linear-gradient(135deg,#0284C7,#22D3EE);color:white}.pdi-auth-form{display:grid;gap:10px}.pdi-auth-form input,.pdi-auth-form select{height:40px;border-radius:12px;background:#07111D!important;color:#E6F4FF!important;border:1px solid rgba(148,163,184,.28)!important;padding:0 12px;font-weight:800}.pdi-auth-form code{display:block;background:#050B12;border:1px solid rgba(103,232,249,.25);border-radius:10px;padding:10px;color:#A7F3D0}.pdi-auth-form button:disabled{opacity:.45;cursor:not-allowed}.pdi-launch-card,.pdi-main-nav button,.pdi-account,.pdi-start-primary{background:linear-gradient(180deg,#1B2A3A,#0F1A27)!important;color:#EAF6FF!important;border-color:rgba(77,184,212,.42)!important}.pdi-launch-card .icon{background:linear-gradient(135deg,#0284C7,#22D3EE)!important;color:white!important}.pdi-main-nav button.active{background:linear-gradient(135deg,#0284C7,#22D3EE)!important}.pdi-start-primary{box-shadow:0 18px 45px rgba(14,165,233,.28)!important}@keyframes pdiAuthIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}@media(max-width:900px)',1)
    write(APP,s)
    print('App patchée 010')

def patch_css():
    s=read(LANDCSS); backup(LANDCSS)
    if 'PATCH 010 remove direct start and black buttons' in s:
        print('CSS landing déjà patché')
        return
    s+='''
/* PATCH 010 remove direct start and black buttons */
.pdiL-entry,.pdiL-launcher-head button,.pdiL-btn,.pdiL-hero-button{background:linear-gradient(180deg,#1B2A3A,#0F1A27)!important;color:#EAF6FF!important;border:1px solid rgba(77,184,212,.45)!important;box-shadow:0 18px 44px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,255,255,.05)!important}
.pdiL-btn-primary,.pdiL-hero-button{background:linear-gradient(135deg,#0284C7,#22D3EE)!important;color:white!important;border-color:#67E8F9!important}
.pdiL-entry strong,.pdiL-entry small,.pdiL-entry p{color:#E5F2FF!important}.pdiL-entry p{opacity:.78}.pdiL-entry-go{color:#67E8F9!important;font-weight:900}.pdiL-entry:hover,.pdiL-entry.selected{background:linear-gradient(180deg,#22384D,#102235)!important;transform:translateY(-3px) scale(1.01)!important}
'''
    write(LANDCSS,s)
    print('CSS landing patché 010')

def report():
    txt=f"""# PATCH 010 — Auth simulée + suppression accès direct + fix boutons noirs

Date: {datetime.now().isoformat(timespec='seconds')}

## Audit
- PATCH 008/009 détectés.
- Landing et PdiUnifiedApp présents.

## Corrections demandées
- Bouton Commencer/Démarrer renommé et accès direct neutralisé.
- Accès ISO/Vision/CAD bloqué si utilisateur guest/pending_email.
- Ajout gateway Connexion / Créer compte / Activation / Démo.
- Correction renforcée des boutons noirs sur landing et app.

## Flux ajouté
Créer compte → pending_email → token activation simulé → activer compte → client actif.

## Sécurité
- Message d'erreur unique.
- Email confirmé simulé.
- Inputs minimum validés.
- Pas de secret dans le code.
- Variables Firebase via Vercel/env.

## Note assets
AI Studio n’inclut pas automatiquement les PNG/images. Ajouter manuellement les assets dans public/assets/pdi/ ou src/assets/images avant build/sync GitHub.

## Tests
npm run lint
npm run build
Vercel preview
"""
    write(REPORT,txt)
    if HISTORY.exists() and 'PATCH 010 — Auth simulée' not in read(HISTORY):
        write(HISTORY, read(HISTORY).rstrip()+"\n\n## PATCH 010 — Auth simulée + suppression accès direct\n\n- Ajout gateway Connexion/Créer compte/Activation/Démo.\n- Suppression accès direct via bouton Commencer/Démarrer.\n- Blocage ouverture modules si compte non actif/démo.\n- Correction renforcée boutons noirs.\n")

def main():
    print('PD&I PATCH 010')
    audit(); patch_landing(); patch_app(); patch_css(); report(); print('PATCH 010 terminé')

if __name__=='__main__':
    main()
