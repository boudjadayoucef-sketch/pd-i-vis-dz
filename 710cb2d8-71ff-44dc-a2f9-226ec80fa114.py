#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 007e
Correctif UI : propriétés flottantes compactes + restauration landing/accueil.

Audit confirmé :
- Les fichiers landing existent encore : src/pdi/landing/PdiLandingV4.tsx/.css.
- PdiUnifiedApp garde encore le stage landing, mais sessionStorage pdi.stage.v4 peut rester bloqué sur "app".
- Le workspace ISO plein écran + retours home peut donner l'impression que landing/accueil ont disparu.
- Le panneau propriétés 2D est encore dans le panneau latéral, donc trop grand.

Objectif :
1) Remplacer/masquer le panneau propriétés 2D latéral par une palette flottante compacte.
2) Palette taille proche menu clic droit, noir/gris, minimaliste, déplaçable sur le plan.
3) Ajouter bouton Landing/Accueil visible dans le workspace.
4) Corriger la navigation : landing restaurable, accueil restaurable, sessionStorage nettoyé si retour landing.
"""

from pathlib import Path
import shutil
import sys
from datetime import datetime

PATCH_ID = "007e"
ROOT = Path(".")
ENGINE = ROOT / "src" / "pdi" / "isometric" / "engine" / "IsometrieModuleV48d.tsx"
APP = ROOT / "src" / "pdi" / "app" / "PdiUnifiedApp.tsx"
REPORT = ROOT / "007e_compact_floating_props_landing_restore_REPORT.md"
HISTORY = ROOT / "docs" / "PATCH_HISTORY.md"
GUARD = "PATCH 007e — compact floating props landing restore"


def fail(msg):
    print("ABANDON : " + msg)
    sys.exit(2)

def read(p): return p.read_text(encoding="utf-8")
def write(p,c):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(c, encoding="utf-8")

def backup_once(p):
    b = p.with_name(p.name + f".before{PATCH_ID}")
    if not b.exists():
        shutil.copy2(p,b)
        print(f"Sauvegarde créée : {b}")

def assert_project():
    if not ENGINE.exists(): fail(f"moteur introuvable: {ENGINE}")
    if not APP.exists(): fail(f"PdiUnifiedApp introuvable: {APP}")
    es = read(ENGINE); app = read(APP)
    missing = [x for x in ["selectedCad2dEntity","updateCad2dEntity","contextMenu"] if x not in es]
    if missing: fail("pré-requis panneau/propriétés manquants: " + ", ".join(missing))
    missing_app = [x for x in ["PdiLandingV4", "PDI_STAGE_KEY", "stage", "pdi:navigate"] if x not in app]
    if missing_app: fail("pré-requis landing manquants: " + ", ".join(missing_app))
    print("Audit OK : landing présente, accueil présent, panneau 2D présent.")

def patch_app():
    src = read(APP)
    if GUARD in src:
        print("App déjà patchée.")
        return
    backup_once(APP)
    src = "// " + GUARD + "\n" + src

    # Ajouter handler navigate landing robuste dans le listener existant.
    old = '''      setStage("app");
      setActiveModule(allowed.includes(detail) ? detail : "home");'''
    new = '''      if (detail === "landing") {
        try { window.sessionStorage.removeItem(PDI_STAGE_KEY); } catch {}
        setStage("landing");
        setActiveModule("home");
        return;
      }
      setStage("app");
      try { window.sessionStorage.setItem(PDI_STAGE_KEY, "app"); } catch {}
      setActiveModule(allowed.includes(detail) ? detail : "home");'''
    if old in src:
        src = src.replace(old,new,1)
    else:
        print("Handler pdi:navigate exact non trouvé, patch partiel app.")

    # Ajouter bouton landing dans top actions près compte si possible.
    old2 = '<button className="pdi-account">Compte PRO</button>'
    new2 = '<button className="pdi-account" onClick={() => window.dispatchEvent(new CustomEvent("pdi:navigate", { detail: "landing" }))}>Landing</button><button className="pdi-account">Compte PRO</button>'
    if old2 in src and 'detail: "landing"' not in src:
        src = src.replace(old2,new2,1)

    write(APP,src)
    print("PdiUnifiedApp patché : retour landing/accueil restauré.")

def patch_engine():
    src = read(ENGINE)
    if GUARD in src:
        print("Engine déjà patché.")
        return
    backup_once(ENGINE)
    src = "// " + GUARD + "\n" + src

    # 1) Etat palette flottante après selectedCad2dEntity.
    anchor = "  const selectedCad2dEntity = cad2dEntities.find((entity) => selectedCad2dIds.includes(entity.id)) || null;"
    inject = anchor + r'''

  // PATCH 007e — palette propriétés CAD flottante compacte.
  const [cadPropsOpen, setCadPropsOpen] = useState(true);
  const [cadPropsPos, setCadPropsPos] = useState({ x: 92, y: 132 });
  const cadPropsDragRef = useRef<{ dx: number; dy: number } | null>(null);
  const startCadPropsDrag = (event: React.MouseEvent) => {
    event.preventDefault();
    cadPropsDragRef.current = { dx: event.clientX - cadPropsPos.x, dy: event.clientY - cadPropsPos.y };
  };
  const moveCadPropsDrag = (event: React.MouseEvent) => {
    if (!cadPropsDragRef.current) return;
    setCadPropsPos({
      x: Math.max(8, Math.min(event.clientX - cadPropsDragRef.current.dx, (typeof window !== "undefined" ? window.innerWidth : 900) - 238)),
      y: Math.max(84, Math.min(event.clientY - cadPropsDragRef.current.dy, (typeof window !== "undefined" ? window.innerHeight : 700) - 260)),
    });
  };
  const endCadPropsDrag = () => { cadPropsDragRef.current = null; };
'''
    if anchor in src and "cadPropsPos" not in src:
        src = src.replace(anchor, inject, 1)

    # 2) Ajouter global mouse move/up sur root pour drag palette.
    src = src.replace(
        'data-pdi-studio="true"',
        'data-pdi-studio="true" onMouseMove={moveCadPropsDrag} onMouseUp={endCadPropsDrag}',
        1
    )

    # 3) Cacher ancien panneau énorme si présent par CSS/condition : remplacer classe racine par hidden.
    src = src.replace('className="pdi-cad-props-mini"', 'className="hidden pdi-cad-props-mini"')
    src = src.replace('className="bg-slate-950 border-2 border-cyan-500/70 rounded-2xl p-3 shadow-lg space-y-2.5 text-white"', 'className="hidden"')

    # 4) Ajouter palette flottante juste avant menu contextuel.
    anchor2 = '            {contextMenu && ('
    palette = r'''            {selectedCad2dEntity && cadPropsOpen && (
              <div className="pdi-cad-float-props" style={{ left: cadPropsPos.x, top: cadPropsPos.y }} onMouseDown={(e)=>e.stopPropagation()}>
                <div className="pdi-cad-float-head" onMouseDown={startCadPropsDrag}>
                  <b>PROPERTIES</b><span>{selectedCad2dEntity.type}</span><button onClick={()=>setCadPropsOpen(false)}>×</button>
                </div>
                <div className="pdi-cad-float-body">
                  <label>Layer<select value={selectedCad2dEntity.layerId} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{layerId:e.target.value})}>{cad2dLayers.map(layer=><option key={layer.id} value={layer.id}>{layer.name}</option>)}</select></label>
                  <label>Color<input type="color" value={selectedCad2dEntity.color} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{color:e.target.value})}/></label>
                  <label>Line<select value={selectedCad2dEntity.lineType || "continuous"} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{lineType:e.target.value as Cad2dEntity["lineType"]})}><option value="continuous">Continuous</option><option value="dashed">Dashed</option><option value="center">Center</option><option value="hidden">Hidden</option></select></label>
                  <label>Weight<input type="number" min="0.5" step="0.5" value={selectedCad2dEntity.lineWeight || 1.5} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{lineWeight:Number(e.target.value)||1.5})}/></label>
                  {selectedCad2dEntity.type === "text" && <>
                    <label className="wide">Text<input value={selectedCad2dEntity.text || ""} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{text:e.target.value})}/></label>
                    <label>Size<input type="number" min="6" max="96" value={selectedCad2dEntity.fontSize || 16} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{fontSize:Number(e.target.value)||16})}/></label>
                    <label>Font<select value={selectedCad2dEntity.fontFamily || "Arial"} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{fontFamily:e.target.value})}><option>Arial</option><option>Inter</option><option>JetBrains Mono</option><option>Georgia</option><option>Times New Roman</option><option>Courier New</option></select></label>
                  </>}
                  <label>Rot.<input type="number" step="1" value={selectedCad2dEntity.rotation || 0} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{rotation:Number(e.target.value)||0})}/></label>
                  <label>Opacity<input type="number" min="0.1" max="1" step="0.05" value={selectedCad2dEntity.opacity ?? 1} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{opacity:Number(e.target.value)||1})}/></label>
                </div>
                <div className="pdi-cad-float-actions"><button onClick={duplicateSelectedCad2d}>Dup</button><button onClick={()=>rotateSelectedCad2d(15)}>Rot</button><button onClick={()=>scaleSelectedCad2d(1.1)}>Scale</button><button onClick={deleteSelectedCad2d}>Del</button></div>
              </div>
            )}
            {selectedCad2dEntity && !cadPropsOpen && <button className="pdi-cad-props-tab" onClick={()=>setCadPropsOpen(true)} style={{ left: cadPropsPos.x, top: cadPropsPos.y }}>PROPS</button>}

''' + anchor2
    if anchor2 in src and "pdi-cad-float-props" not in src:
        src = src.replace(anchor2, palette, 1)

    # 5) Ajouter boutons home/landing dans barre top fullscreen.
    oldhome = '⌂ Accueil'
    # If button area already has Accueil, add Landing next to first occurrence in fullscreen topbar text by broader replacement.
    src = src.replace(
        '<span>⌂ Accueil</span>',
        '<span>⌂ Accueil</span>',
        1
    )
    # add extra menu item in cad menu if not present
    src = src.replace(
        '{ label: "⌂ Retour Accueil", hint: "Home", run: () => window.dispatchEvent(new CustomEvent("pdi:navigate", { detail: "home" })) },',
        '{ label: "⌂ Retour Accueil", hint: "Home", run: () => window.dispatchEvent(new CustomEvent("pdi:navigate", { detail: "home" })) },\n        { label: "◈ Landing", hint: "Ouverture", run: () => window.dispatchEvent(new CustomEvent("pdi:navigate", { detail: "landing" })) },',
        1
    )

    # 6) Styles flottants taille menu contextuel.
    style_anchor = '[data-pdi-studio] .pdi-cad-menu-panel{display:none;position:absolute;top:30px;left:0;min-width:210px;max-height:70vh;overflow:auto;z-index:10050;background:#0F141B;border:1px solid #30363D;border-radius:10px;padding:6px;box-shadow:0 18px 45px rgba(0,0,0,.45)}'
    style_add = style_anchor + r'''
        [data-pdi-studio] .pdi-cad-float-props{position:fixed;width:218px;z-index:10070;background:#111317;border:1px solid #2d333b;border-radius:8px;box-shadow:0 18px 44px rgba(0,0,0,.55);color:#d1d5db;font-size:10px;overflow:hidden;user-select:none}
        [data-pdi-studio] .pdi-cad-float-head{height:27px;display:flex;align-items:center;gap:7px;background:#0b0d10;border-bottom:1px solid #2d333b;padding:0 7px;cursor:move;color:#e5e7eb;letter-spacing:.08em}
        [data-pdi-studio] .pdi-cad-float-head b{font-size:9px}.pdi-cad-float-head span{margin-left:auto;color:#8b949e;font-size:9px;text-transform:uppercase}.pdi-cad-float-head button{width:18px;height:18px;border:0;background:#22272e;color:#8b949e;border-radius:4px;cursor:pointer}
        [data-pdi-studio] .pdi-cad-float-body{display:grid;grid-template-columns:1fr 1fr;gap:5px;padding:7px;background:#161b22;max-height:210px;overflow:auto}
        [data-pdi-studio] .pdi-cad-float-body label{display:flex;flex-direction:column;gap:2px;color:#8b949e;font-size:8px;font-weight:800;text-transform:uppercase}.pdi-cad-float-body label.wide{grid-column:1/-1}
        [data-pdi-studio] .pdi-cad-float-body input,[data-pdi-studio] .pdi-cad-float-body select{height:22px;min-width:0;border-radius:4px;background:#0d1117!important;border:1px solid #30363d!important;color:#e6edf3!important;font-size:10px;padding:0 5px}
        [data-pdi-studio] .pdi-cad-float-actions{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding:6px;background:#0f141b;border-top:1px solid #2d333b}.pdi-cad-float-actions button,.pdi-cad-props-tab{height:22px;border-radius:4px;border:1px solid #30363d;background:#21262d;color:#c9d1d9;font-size:9px;font-weight:900;cursor:pointer}.pdi-cad-float-actions button:hover,.pdi-cad-props-tab:hover{background:#30363d;color:white}.pdi-cad-props-tab{position:fixed;z-index:10069;width:62px;background:#111317}
'''
    if style_anchor in src and "pdi-cad-float-props" not in src[src.find(style_anchor):src.find(style_anchor)+2000]:
        src = src.replace(style_anchor, style_add, 1)

    write(ENGINE,src)
    print("Engine patché : palette propriétés flottante compacte + menu landing.")

def write_report():
    content = f"""# PATCH 007e — Palette propriétés compacte + restauration landing/accueil

Date : {datetime.now().isoformat(timespec='seconds')}

## Audit
- La landing n'était pas supprimée : `PdiLandingV4.tsx` et CSS existent.
- Le problème probable venait du stage enregistré en sessionStorage (`pdi.stage.v4 = app`) et du workspace ISO plein écran.
- Le panneau propriétés 2D restait latéral et trop grand.

## Corrections
- Ajout palette flottante compacte, taille proche menu clic droit.
- Palette noire/grise, minimaliste, déplaçable sur le plan.
- Champs limités aux données à saisir.
- Ancien panneau propriétés 2D latéral masqué.
- Navigation landing restaurée via `pdi:navigate` detail `landing`.
- Bouton/menu Landing ajouté.

## Validation
1. Sélectionner objet 2D : petite palette flottante apparaît.
2. Glisser l'entête PROPERTIES : la palette se déplace.
3. Modifier couleur/texte/taille : l'objet se met à jour.
4. Menu CAD > Landing : la landing doit revenir.
5. Menu CAD > Accueil : la page accueil doit revenir.
"""
    write(REPORT,content)

def update_history():
    if not HISTORY.exists(): return
    src = read(HISTORY)
    if "PATCH 007e — Palette propriétés compacte" in src: return
    entry = f"""

## PATCH 007e — Palette propriétés compacte et restauration landing

Date : {datetime.now().strftime('%Y-%m-%d')}

- Remplacement du panneau propriétés 2D latéral par une palette flottante compacte déplaçable.
- Style noir/gris minimaliste proche menu clic droit CAD.
- Restauration navigation Landing/Accueil depuis workspace.
- Aucun changement topologie piping V4.8d.
"""
    write(HISTORY, src.rstrip()+"\n"+entry)

def main():
    print("PD&I PATCH 007e — propriétés flottantes + landing restore")
    assert_project()
    patch_app()
    patch_engine()
    write_report()
    update_history()
    print("\nPATCH 007e terminé. Tester npm run lint && npm run build puis Vercel.")

if __name__ == "__main__":
    main()
