#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 007b
Correction objets 2D : manipulation, configuration, texte visible.

Constat après PATCH 007 :
- Les objets 2D apparaissent.
- Ils ne sont pas réellement manipulables/configurables.
- Le texte ne s'affiche pas correctement dans certains cas.

Objectif 007b :
- Ajouter sélection fiable des objets 2D.
- Ajouter déplacement clavier des objets 2D.
- Ajouter suppression/copie/duplication simples des objets 2D.
- Ajouter panneau propriétés 2D minimal : calque, couleur, texte, rayon, intention.
- Corriger le rendu texte avec une taille lisible et un clic fiable.
- Ne pas toucher au graphe métier piping V4.8d.
"""

from pathlib import Path
import shutil
import sys
from datetime import datetime

PATCH_ID = "007b"
ROOT = Path(".")
ENGINE = ROOT / "src" / "pdi" / "isometric" / "engine" / "IsometrieModuleV48d.tsx"
REPORT = ROOT / "007b_2d_objects_manipulation_properties_fix_REPORT.md"
HISTORY = ROOT / "docs" / "PATCH_HISTORY.md"
GUARD = "PATCH 007b — 2D manipulation and properties"


def fail(msg: str) -> None:
    print("ABANDON : " + msg)
    sys.exit(2)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def backup_once(path: Path) -> None:
    backup = path.with_name(path.name + f".before{PATCH_ID}")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"Sauvegarde créée : {backup}")


def assert_project() -> None:
    if not ENGINE.exists():
        fail(f"moteur introuvable : {ENGINE}")
    src = read(ENGINE)
    required = ["Cad2dEntity", "cad2dEntities", "selectedCad2dIds", "addCad2dEntity"]
    missing = [x for x in required if x not in src]
    if missing:
        fail("PATCH 007 non détecté ou incomplet : " + ", ".join(missing))
    print("Audit OK : fondation 2D PATCH 007 détectée.")


def patch_engine() -> None:
    src = read(ENGINE)
    if GUARD in src:
        print("Patch 007b déjà appliqué.")
        return

    backup_once(ENGINE)

    # 1) Ajouter helpers manipulation/configuration 2D après prepareCad2dTool.
    anchor = '''  const prepareCad2dTool = (tool: Cad2dEntityType) => {
    setInteractionMode("select");
    setIsoDrawMode("select");
    setCad2dDraftTool(tool);
    setStatusMessage(`${tool.toUpperCase()} 2D prêt · cliquez dans le plan pour poser un objet de base`);
  };'''

    patch = anchor + r'''

  // PATCH 007b — 2D manipulation and properties.
  const selectedCad2dEntity = cad2dEntities.find((entity) => selectedCad2dIds.includes(entity.id)) || null;

  const updateCad2dEntity = (id: string, patch: Partial<Cad2dEntity>) => {
    setCad2dEntities((prev) => prev.map((entity) => entity.id === id ? { ...entity, ...patch } : entity));
  };

  const moveSelectedCad2d = (dx: number, dy: number) => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    setCad2dEntities((prev) => prev.map((entity) => {
      if (!ids.has(entity.id) || entity.locked) return entity;
      return {
        ...entity,
        points: entity.points?.map((point) => ({ x: point.x + dx, y: point.y + dy })),
        center: entity.center ? { x: entity.center.x + dx, y: entity.center.y + dy } : entity.center,
      };
    }));
    setStatusMessage(`Déplacement 2D · ${selectedCad2dIds.length} objet(s)`);
  };

  const duplicateSelectedCad2d = () => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    const clones = cad2dEntities.filter((entity) => ids.has(entity.id)).map((entity) => ({
      ...entity,
      id: makeCad2dId(entity.type),
      points: entity.points?.map((point) => ({ x: point.x + isoSnapStep, y: point.y + isoSnapStep })),
      center: entity.center ? { x: entity.center.x + isoSnapStep, y: entity.center.y + isoSnapStep } : entity.center,
    }));
    setCad2dEntities((prev) => [...prev, ...clones]);
    setSelectedCad2dIds(clones.map((entity) => entity.id));
    setStatusMessage(`${clones.length} objet(s) 2D dupliqué(s) · nouveaux IDs`);
  };

  const deleteSelectedCad2d = () => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    setCad2dEntities((prev) => prev.filter((entity) => !ids.has(entity.id)));
    setSelectedCad2dIds([]);
    setStatusMessage("Objet(s) 2D supprimé(s)");
  };
'''
    if anchor not in src:
        fail("ancre prepareCad2dTool introuvable")
    src = src.replace(anchor, patch, 1)

    # 2) Ajouter raccourcis clavier 2D dans le gestionnaire clavier, avant gestion arrows piping.
    key_anchor = '      if(e.key.startsWith("Arrow") && selectedNodeIds.length && !(e.target as HTMLElement)?.matches("input,textarea,select")){' 
    key_patch = r'''      if(selectedCad2dIds.length && !(e.target as HTMLElement)?.matches("input,textarea,select")){
        if(e.key.startsWith("Arrow")){
          e.preventDefault();
          const step = isoSnapStep * (e.shiftKey ? 4 : 1);
          moveSelectedCad2d(e.key === "ArrowRight" ? step : e.key === "ArrowLeft" ? -step : 0, e.key === "ArrowDown" ? step : e.key === "ArrowUp" ? -step : 0);
          return;
        }
        if((e.ctrlKey||e.metaKey) && e.key.toLowerCase()==="d"){
          e.preventDefault();
          duplicateSelectedCad2d();
          return;
        }
        if(e.key==="Delete" || e.key==="Backspace"){
          e.preventDefault();
          deleteSelectedCad2d();
          return;
        }
      }

      if(e.key.startsWith("Arrow") && selectedNodeIds.length && !(e.target as HTMLElement)?.matches("input,textarea,select")){'''
    if key_anchor in src:
        src = src.replace(key_anchor, key_patch, 1)
    else:
        print("Ancre clavier Arrow non trouvée — raccourcis 2D non injectés automatiquement.")

    # 3) Corriger rendu texte et rendre chaque objet plus cliquable.
    old_text = '<text key={entity.id} x={p.x} y={p.y} fill={stroke} fontSize="12" fontWeight="800" onClick={common.onClick} style={common.style}>{entity.text || "Texte"}</text>'
    new_text = '''<g key={entity.id} onClick={common.onClick} style={common.style} transform={`translate(${p.x} ${p.y}) rotate(${entity.rotation || 0})`}>
                        <rect x="-4" y="-16" width={Math.max(48, (entity.text || "Texte").length * 8)} height="22" rx="3" fill={selected ? "#fbbf24" : "#020617"} fillOpacity={selected ? .18 : .55} stroke={stroke} strokeOpacity=".55" />
                        <text x="0" y="0" fill={stroke} fontSize="14" fontWeight="900" pointerEvents="none">{entity.text || "Texte"}</text>
                      </g>'''
    if old_text in src:
        src = src.replace(old_text, new_text, 1)
    else:
        print("Ancre rendu texte non trouvée — vérifier manuellement.")

    # 4) Ajouter panneau propriétés 2D avant l'inspecteur CAD existant.
    panel_anchor = '        {/* CAD Property Inspector for active selection */}'
    panel = r'''        {/* PATCH 007b — Propriétés objet 2D */}
        {selectedCad2dEntity && (
          <div className="bg-slate-900 border-2 border-cyan-500/70 rounded-2xl p-3 shadow-lg space-y-2.5 text-white">
            <div className="flex items-center justify-between border-b border-slate-700 pb-1.5">
              <h3 className="text-xs font-black uppercase text-cyan-300">Propriétés 2D</h3>
              <span className="text-[10px] font-mono bg-cyan-950 text-cyan-300 px-2 py-0.5 rounded border border-cyan-800 font-bold">{selectedCad2dEntity.type}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-[11px]">
              <div className="col-span-2">
                <label className="text-[9px] font-bold text-slate-400 block mb-0.5">ID</label>
                <div className="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-[10px] font-mono text-slate-300 truncate">{selectedCad2dEntity.id}</div>
              </div>
              <div>
                <label className="text-[9px] font-bold text-slate-400 block mb-0.5">Calque</label>
                <select value={selectedCad2dEntity.layerId} onChange={(e) => updateCad2dEntity(selectedCad2dEntity.id, { layerId: e.target.value })} className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs text-white">
                  {cad2dLayers.map((layer) => <option key={layer.id} value={layer.id}>{layer.name}</option>)}
                </select>
              </div>
              <div>
                <label className="text-[9px] font-bold text-slate-400 block mb-0.5">Couleur</label>
                <input type="color" value={selectedCad2dEntity.color} onChange={(e) => updateCad2dEntity(selectedCad2dEntity.id, { color: e.target.value })} className="w-full h-8 bg-slate-800 border border-slate-700 rounded" />
              </div>
              {(selectedCad2dEntity.type === "circle" || selectedCad2dEntity.type === "arc") && (
                <div>
                  <label className="text-[9px] font-bold text-slate-400 block mb-0.5">Rayon</label>
                  <input type="number" step="0.1" value={selectedCad2dEntity.radius || 1} onChange={(e) => updateCad2dEntity(selectedCad2dEntity.id, { radius: Number(e.target.value) || 1 })} className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs text-white" />
                </div>
              )}
              {selectedCad2dEntity.type === "text" && (
                <div className="col-span-2">
                  <label className="text-[9px] font-bold text-slate-400 block mb-0.5">Texte</label>
                  <input value={selectedCad2dEntity.text || ""} onChange={(e) => updateCad2dEntity(selectedCad2dEntity.id, { text: e.target.value })} className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs text-white" />
                </div>
              )}
              <div>
                <label className="text-[9px] font-bold text-slate-400 block mb-0.5">Intention</label>
                <select value={selectedCad2dEntity.metadata?.intent || "draft"} onChange={(e) => updateCad2dEntity(selectedCad2dEntity.id, { metadata: { ...(selectedCad2dEntity.metadata || {}), intent: e.target.value as any } })} className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs text-white">
                  <option value="draft">Draft</option>
                  <option value="pipe_axis">Axe tuyauterie</option>
                  <option value="equipment">Équipement</option>
                  <option value="annotation">Annotation</option>
                </select>
              </div>
              <div>
                <label className="text-[9px] font-bold text-slate-400 block mb-0.5">Z futur</label>
                <input type="number" step="0.1" value={selectedCad2dEntity.metadata?.elevationZ || 0} onChange={(e) => updateCad2dEntity(selectedCad2dEntity.id, { metadata: { ...(selectedCad2dEntity.metadata || {}), elevationZ: Number(e.target.value) || 0 } })} className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs text-white" />
              </div>
            </div>
            <div className="grid grid-cols-4 gap-1 pt-1 border-t border-slate-800">
              <button type="button" onClick={() => moveSelectedCad2d(-isoSnapStep, 0)} className="rounded bg-slate-800 py-1 text-[10px] font-black">←</button>
              <button type="button" onClick={() => moveSelectedCad2d(isoSnapStep, 0)} className="rounded bg-slate-800 py-1 text-[10px] font-black">→</button>
              <button type="button" onClick={duplicateSelectedCad2d} className="rounded bg-blue-800 py-1 text-[10px] font-black">Dup</button>
              <button type="button" onClick={deleteSelectedCad2d} className="rounded bg-red-800 py-1 text-[10px] font-black">Del</button>
            </div>
          </div>
        )}

        {/* CAD Property Inspector for active selection */}'''
    if panel_anchor in src:
        src = src.replace(panel_anchor, panel, 1)
    else:
        fail("ancre inspecteur propriétés introuvable")

    # 5) Brancher boutons ruban Copy/Delete/Duplicate : si objet 2D sélectionné prioritaire.
    src = src.replace('<button onClick={duplicateSelection}>Duplicate</button>', '<button onClick={() => selectedCad2dIds.length ? duplicateSelectedCad2d() : duplicateSelection()}>Duplicate</button>', 1)
    src = src.replace('<button onClick={deleteSelection}>Delete</button>', '<button onClick={() => selectedCad2dIds.length ? deleteSelectedCad2d() : deleteSelection()}>Delete</button>', 1)

    write(ENGINE, src)
    print("IsometrieModuleV48d.tsx patché : objets 2D manipulables/configurables.")


def write_report() -> None:
    content = f"""# PATCH 007b — Objets 2D manipulables et configurables

Date : {datetime.now().isoformat(timespec='seconds')}

## Problème constaté
- Les objets 2D apparaissaient.
- Ils n'étaient pas manipulables/configurables.
- Le texte ne s'affichait pas correctement.

## Corrections
- Sélection objet 2D fiabilisée.
- Déplacement clavier des objets 2D sélectionnés.
- Duplication / suppression d'objets 2D.
- Panneau propriétés 2D : calque, couleur, texte, rayon, intention, Z futur.
- Rendu texte corrigé avec fond et `pointerEvents` contrôlé.
- Boutons ruban Duplicate/Delete priorisent les objets 2D sélectionnés.

## Fichier modifié
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`

## Protégé
- Graphe piping V4.8d non remplacé.
- Pas de deuxième moteur piping.
- Mapping 2D -> piping toujours reporté au patch suivant.

## Tests attendus
```bash
npm run lint
npm run build
```

## Validation Vercel
- Créer Line / Polyline / Circle / Text.
- Cliquer objet 2D : panneau Propriétés 2D apparaît.
- Modifier couleur / texte / rayon.
- Flèches clavier déplacent l'objet.
- Dup / Del fonctionnent.
- Le texte est visible.
"""
    write(REPORT, content)
    print(f"Rapport écrit : {REPORT}")


def update_history() -> None:
    if not HISTORY.exists():
        print("PATCH_HISTORY.md absent — historique non mis à jour.")
        return
    src = read(HISTORY)
    if "PATCH 007b" in src:
        print("PATCH_HISTORY.md déjà mis à jour.")
        return
    entry = f"""

## PATCH 007b — Objets 2D manipulables et configurables

Date : {datetime.now().strftime('%Y-%m-%d')}

- Correction manipulation/configuration des objets 2D créés par PATCH 007.
- Ajout panneau propriétés 2D : calque, couleur, texte, rayon, intention, Z futur.
- Ajout déplacement clavier, duplication et suppression 2D.
- Correction rendu texte.
- V4.8d reste source of truth piping.
"""
    write(HISTORY, src.rstrip() + "\n" + entry)
    print("PATCH_HISTORY.md mis à jour.")


def main() -> None:
    print("PD&I PATCH 007b — correction objets 2D")
    assert_project()
    patch_engine()
    write_report()
    update_history()
    print("\nPATCH 007b terminé.")
    print("Suite : appliquer dans AI Studio, npm run lint/build, sync GitHub, vérifier Vercel.")


if __name__ == "__main__":
    main()
