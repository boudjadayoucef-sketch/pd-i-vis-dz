#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 006
Ruban CAD universel contrôlé (type AutoCAD) — sans casser la sélection pro existante.

AUDIT 006 confirmé sur ZIP pd-i-vis-dz-main :
- La sélection professionnelle existe déjà : Patch 004 / 004b.
- V4.8d contient déjà selectedNodeIds, selectedSegmentIds, selectedDimensionIds.
- Rectangle de sélection, Shift/Ctrl/Cmd, copier/couper/coller/dupliquer, undo/redo existent.
- Donc ce patch NE refait PAS la sélection.

Objectif 006 :
- Ajouter une couche UI de ruban CAD universel inspirée AutoCAD : Draw / Annotation / Modify / Measure / Output.
- Exposer Line/Polyline/Circle/Arc/Text/Dimension/Measure comme entrées visibles.
- Connecter uniquement les outils déjà sûrs aux fonctions existantes.
- Marquer les outils futurs comme “préparé” sans créer de second moteur 2D.
- Ne pas toucher au moteur métier V4.8d hors UI contrôlée.
"""

from pathlib import Path
import shutil
import sys
from datetime import datetime

PATCH_ID = "006"
ROOT = Path(".")
ENGINE = ROOT / "src" / "pdi" / "isometric" / "engine" / "IsometrieModuleV48d.tsx"
REPORT = ROOT / "006_universal_cad_toolbar_REPORT.md"
HISTORY = ROOT / "docs" / "PATCH_HISTORY.md"
GUARD = "PATCH 006 — universal CAD toolbar"


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
        fail(f"moteur V4.8d introuvable : {ENGINE}")
    src = read(ENGINE)
    required = [
        "selectedNodeIds",
        "selectedSegmentIds",
        "selectedDimensionIds",
        "copySelection",
        "duplicateSelection",
        "selectionSubGraph",
        "selectDimensionV44",
        "setIsoDrawMode",
        "cadMenuGroups",
        "pdi-studio-rail",
    ]
    missing = [x for x in required if x not in src]
    if missing:
        fail("audit sélection / UI incomplet, éléments manquants : " + ", ".join(missing))
    print("Audit OK : sélection pro existante confirmée, rail/menu CAD présents.")


def patch_engine() -> None:
    src = read(ENGINE)
    if GUARD in src:
        print("Patch 006 déjà appliqué.")
        return

    backup_once(ENGINE)

    # 1) Ajouter helper de statut pour outils futurs : pas de logique métier dupliquée.
    anchor = "  const runWorkspaceCommand=(action:()=>void,label:string)=>{action();setCommandPaletteOpen(false);setStatusMessage(label);};"
    helper = """  const runWorkspaceCommand=(action:()=>void,label:string)=>{action();setCommandPaletteOpen(false);setStatusMessage(label);};

  // PATCH 006 — universal CAD toolbar.
  // Outils universels préparés sans créer de second moteur 2D : les actions non
  // encore reliées au graphe V4.8d affichent un état explicite, pas une fausse logique.
  const cadToolPrepared = (label: string) => {
    setInteractionMode("select");
    setIsoDrawMode("select");
    setStatusMessage(`${label} préparé · moteur 2D canonique prévu patch 007`);
  };"""
    if anchor in src:
        src = src.replace(anchor, helper, 1)
    else:
        fail("ancre runWorkspaceCommand introuvable")

    # 2) Enrichir le menu CAD existant si possible.
    old_menu_start = "  const cadMenuGroups: Array<{"
    if old_menu_start not in src:
        fail("ancre cadMenuGroups introuvable")

    # Insertion de groupe universel avant le groupe existant via remplacement léger du premier tableau si ancre disponible.
    # On cherche le début du tableau jusqu'à la première occurrence connue d'un item Sélection.
    menu_anchor = "        { label: \"Sélection (Boîte / Clic)\", hint: \"V\", run: () => { setInteractionMode(\"select\"); setIsoDrawMode(\"select\"); } },"
    universal_items = """        // PATCH 006 : outils CAD universels visibles.
        { label: "Line / Tube", hint: "L/T", run: () => { setInteractionMode("select"); setIsoDrawMode("segment"); } },
        { label: "Polyline", hint: "PL", run: () => cadToolPrepared("Polyline") },
        { label: "Circle", hint: "CIR", run: () => cadToolPrepared("Circle") },
        { label: "Arc", hint: "ARC", run: () => cadToolPrepared("Arc") },
        { label: "Text", hint: "TXT", run: () => cadToolPrepared("Text") },
        { label: "Measure", hint: "ME", run: () => { setRightPanelOpen(true); setRightPanelTab("dimensions"); setStatusMessage("Mesures disponibles via cotations et métrés V4.8d"); } },
"""
    if menu_anchor in src and "Polyline" not in src:
        src = src.replace(menu_anchor, universal_items + menu_anchor, 1)

    # 3) Ajouter un mini-ruban horizontal CAD au-dessus du rail en mode fullscreen.
    rail_anchor = "        <aside className=\"pdi-studio-rail fixed bottom-0 left-0 top-[54px] z-[10005] w-[62px] py-3 flex flex-col items-center gap-2\">"
    ribbon = """        <div className="pdi-cad-ribbon fixed left-[62px] right-0 top-[54px] z-[10004] h-[54px] px-3 flex items-center gap-2 overflow-x-auto">
          <div className="pdi-ribbon-group"><span>Draw</span><button onClick={() => { setInteractionMode("select"); setIsoDrawMode("segment"); setStatusMessage("Line / Tube · V4.8d"); }}>Line</button><button onClick={() => cadToolPrepared("Polyline")}>Polyline</button><button onClick={() => cadToolPrepared("Circle")}>Circle</button><button onClick={() => cadToolPrepared("Arc")}>Arc</button></div>
          <div className="pdi-ribbon-group"><span>Annotation</span><button onClick={() => cadToolPrepared("Text")}>Text</button><button onClick={() => { setInteractionMode("select"); setIsoDrawMode("dimension"); setDimensionPick(null); setRightPanelOpen(true); setRightPanelTab("dimensions"); setStatusMessage("Dimension · 2 ancrages V4.8d"); }}>Dimension</button></div>
          <div className="pdi-ribbon-group"><span>Modify</span><button onClick={copySelection}>Copy</button><button onClick={duplicateSelection}>Duplicate</button><button onClick={() => rotateSelectedEquipment(15)}>Rotate</button><button onClick={deleteSelection}>Delete</button></div>
          <div className="pdi-ribbon-group"><span>Measure</span><button onClick={() => { setRightPanelOpen(true); setRightPanelTab("dimensions"); setStatusMessage("Mesure distance/rayon/angle préparée · cotations actives"); }}>Measure</button><button onClick={() => { setRightPanelOpen(true); setRightPanelTab("bom"); setStatusMessage("Métré / BOM V4.8d"); }}>BOM</button></div>
          <div className="pdi-ribbon-group"><span>Output</span><button onClick={printPlanSheet}>Print</button><button onClick={exportProjectJson}>JSON</button></div>
        </div>
"""
    if rail_anchor in src:
        src = src.replace(rail_anchor, ribbon + rail_anchor, 1)
    else:
        fail("ancre rail introuvable")

    # 4) Ajouter styles du ruban.
    style_anchor = "        [data-pdi-studio] .pdi-rail-button.active{color:white;background:#2563EB;border-color:#60A5FA;box-shadow:0 0 12px rgba(37,99,235,0.4)}"
    style_patch = """        [data-pdi-studio] .pdi-rail-button.active{color:white;background:#2563EB;border-color:#60A5FA;box-shadow:0 0 12px rgba(37,99,235,0.4)}
        [data-pdi-studio] .pdi-cad-ribbon{background:#151B24;border-bottom:1px solid #30363D;box-shadow:0 8px 20px rgba(0,0,0,.25)}
        [data-pdi-studio] .pdi-ribbon-group{height:40px;display:flex;align-items:center;gap:4px;border-right:1px solid #30363D;padding-right:10px;flex-shrink:0}
        [data-pdi-studio] .pdi-ribbon-group span{font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:#7D8590;font-weight:900;margin-right:3px}
        [data-pdi-studio] .pdi-ribbon-group button{height:30px;padding:0 9px;border-radius:6px;border:1px solid #30363D;background:#1F2937;color:#D1D5DB;font-size:10px;font-weight:900;white-space:nowrap}
        [data-pdi-studio] .pdi-ribbon-group button:hover{background:#2563EB;color:white;border-color:#60A5FA}
"""
    if style_anchor in src:
        src = src.replace(style_anchor, style_patch, 1)
    else:
        fail("ancre styles rail introuvable")

    # 5) Ajuster le padding top fullscreen pour laisser place au ruban.
    src = src.replace(
        'pt-[84px]',
        'pt-[116px]',
        1,
    )
    src = src.replace(
        'top-[54px] z-[10005]',
        'top-[108px] z-[10005]',
        1,
    )
    src = src.replace(
        'h-[calc(100vh-118px)]',
        'h-[calc(100vh-146px)]',
        1,
    )

    write(ENGINE, src)
    print("IsometrieModuleV48d.tsx patché UI 006, sélection pro conservée.")


def write_report() -> None:
    content = f"""# PATCH 006 — Ruban CAD universel

Date : {datetime.now().isoformat(timespec='seconds')}

## Audit avant patch
La sélection professionnelle existe déjà et ne doit pas être recréée.
Constats dans `IsometrieModuleV48d.tsx` :
- `selectedNodeIds`, `selectedSegmentIds`, `selectedDimensionIds` présents.
- Rectangle de sélection présent.
- Shift/Ctrl/Cmd additif présents.
- `copySelection`, `duplicateSelection`, `clipboardRef`, undo/redo présents.
- Patch 004 / 004b documentés dans `docs/PATCH_HISTORY.md`.

## Objectif du patch
Ajouter une couche d’interface CAD universelle type AutoCAD :
- Draw : Line, Polyline, Circle, Arc.
- Annotation : Text, Dimension.
- Modify : Copy, Duplicate, Rotate, Delete.
- Measure : Measure, BOM.
- Output : Print, JSON.

## Décision technique
- Les outils déjà sûrs appellent les fonctions V4.8d existantes.
- Les outils futurs affichent un statut “préparé” et attendent le patch 007.
- Aucun second moteur 2D n’est créé.
- Aucun remplacement de V4.8d.

## Fichier modifié
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`

## Fichiers protégés
- `src/pdi/model/index.ts` non utilisé comme moteur.
- Aucune suppression legacy.
- Aucun accès GitHub direct.

## Tests attendus
```bash
npm run lint
npm run build
```

## Validation visuelle Vercel
- Le workspace ISO affiche un ruban CAD horizontal en haut.
- Le rail vertical reste présent.
- Sélection pro toujours active.
- Line/Dimension/Copy/Duplicate/Rotate/Delete fonctionnent via V4.8d.
- Polyline/Circle/Arc/Text indiquent “préparé” sans fausse création.
"""
    write(REPORT, content)
    print(f"Rapport écrit : {REPORT}")


def update_history() -> None:
    if not HISTORY.exists():
        print("PATCH_HISTORY.md absent — historique non mis à jour.")
        return
    src = read(HISTORY)
    if "PATCH 006" in src:
        print("PATCH_HISTORY.md déjà mis à jour.")
        return
    entry = f"""

## PATCH 006 — Ruban CAD universel

Date : {datetime.now().strftime('%Y-%m-%d')}

- Audit confirmé : la sélection professionnelle existe déjà via Patch 004/004b.
- Ajout d’un ruban CAD universel visible : Draw, Annotation, Modify, Measure, Output.
- Les outils sûrs réutilisent V4.8d ; les outils futurs sont marqués préparés.
- Aucun second moteur 2D, aucune duplication de sélection/topologie/projection.
"""
    write(HISTORY, src.rstrip() + "\n" + entry)
    print("PATCH_HISTORY.md mis à jour.")


def main() -> None:
    print("PD&I PATCH 006 — ruban CAD universel")
    assert_project()
    before = read(ENGINE)
    patch_engine()
    after = read(ENGINE)
    if before == after:
        print("Aucune modification moteur nécessaire ou patch déjà appliqué.")
    write_report()
    update_history()
    print("\nPATCH 006 terminé.")
    print("Suite : appliquer dans AI Studio, tester, sync GitHub, vérifier Vercel.")


if __name__ == "__main__":
    main()
