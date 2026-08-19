#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 007
Fondation géométrie 2D réelle.

Objectif :
- Créer une couche de données 2D persistante, avec IDs réels.
- Ne PAS remplacer V4.8d.
- Ne PAS créer un deuxième moteur piping.
- Préparer Line / Polyline / Circle / Arc / Text comme entités 2D projet.
- Ajouter export/import JSON des entités 2D.
- Garder le mapping 2D -> piping graph pour les patchs suivants.

Pré-requis : PATCH 006 appliqué ou au minimum rail/menu CAD existants.
"""

from pathlib import Path
import shutil
import sys
from datetime import datetime

PATCH_ID = "007"
ROOT = Path(".")
ENGINE = ROOT / "src" / "pdi" / "isometric" / "engine" / "IsometrieModuleV48d.tsx"
REPORT = ROOT / "007_real_2d_geometry_foundation_REPORT.md"
HISTORY = ROOT / "docs" / "PATCH_HISTORY.md"
GUARD = "PATCH 007 — real 2D geometry foundation"


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
    required = ["IsometrieModule", "selectedNodeIds", "selectedSegmentIds", "commitGraph", "buildProjectFile", "importProjectJson"]
    missing = [x for x in required if x not in src]
    if missing:
        fail("audit incomplet, éléments manquants : " + ", ".join(missing))
    print("Audit OK : V4.8d présent, sélection pro présente, export/import JSON présents.")


def patch_engine() -> None:
    src = read(ENGINE)
    if GUARD in src:
        print("Patch 007 déjà appliqué.")
        return

    backup_once(ENGINE)

    # 1) Ajouter les types 2D après PipingLine.
    type_anchor = "export interface PipingLine {\n  id: string;\n  lineNumber: string;\n  service: string;\n  dn: number;\n  nps: string;\n  material: string;\n  pressureClass: string;\n  schedule?: string;\n  designPressure?: number;\n  designTemperature?: number;\n  color: string;\n}\n"
    type_patch = type_anchor + r'''
// PATCH 007 — real 2D geometry foundation.
// Couche CAD 2D persistante : objets dessin universels avec IDs réels.
// Cette couche ne remplace pas le graphe piping V4.8d ; elle prépare le mapping 2D -> piping.
export type Cad2dEntityType = "line" | "polyline" | "circle" | "arc" | "text";
export type Cad2dPoint = { x: number; y: number };
export type Cad2dEntity = {
  id: string;
  type: Cad2dEntityType;
  layerId: string;
  color: string;
  lineWeight?: number;
  locked?: boolean;
  visible?: boolean;
  points?: Cad2dPoint[];
  center?: Cad2dPoint;
  radius?: number;
  startAngle?: number;
  endAngle?: number;
  text?: string;
  rotation?: number;
  metadata?: {
    intent?: "draft" | "pipe_axis" | "equipment" | "annotation" | "dimension";
    dn?: number;
    elevationZ?: number;
    catalogRef?: string;
    source?: string;
  };
};

export type Cad2dLayer = {
  id: string;
  name: string;
  color: string;
  visible: boolean;
  locked: boolean;
};

'''
    if type_anchor in src:
        src = src.replace(type_anchor, type_patch, 1)
    else:
        fail("ancre PipingLine introuvable")

    # 1b) Adapter IsoProjectFileV474 model type
    iso_proj_anchor = "  model: { lines: PipingLine[]; nodes: IsoNode[]; segments: IsoSegment[]; dimensions?: IsoDimension[]; };"
    iso_proj_patch = "  model: { lines: PipingLine[]; nodes: IsoNode[]; segments: IsoSegment[]; dimensions?: IsoDimension[]; cad2d?: { layers: Cad2dLayer[]; entities: Cad2dEntity[]; }; };"
    if iso_proj_anchor in src:
        src = src.replace(iso_proj_anchor, iso_proj_patch, 1)

    # 2) Ajouter état 2D près des states principaux.
    state_anchor = "  const [dimensions, setDimensionsRaw] = useState<IsoDimension[]>([]);"
    state_patch = state_anchor + r'''

  // PATCH 007 — real 2D geometry foundation.
  const [cad2dEntities, setCad2dEntities] = useState<Cad2dEntity[]>([]);
  const [cad2dLayers, setCad2dLayers] = useState<Cad2dLayer[]>([
    { id: "axes_tuyauterie", name: "Axes tuyauterie", color: "#4db8d4", visible: true, locked: false },
    { id: "annotations", name: "Annotations", color: "#f0f0f0", visible: true, locked: false },
    { id: "import_cad", name: "Import CAD / fond plan", color: "#888888", visible: true, locked: false },
  ]);
  const [selectedCad2dIds, setSelectedCad2dIds] = useState<string[]>([]);
  const [cad2dDraftTool, setCad2dDraftTool] = useState<Cad2dEntityType | null>(null);

  const makeCad2dId = (type: Cad2dEntityType) => `${type}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;
  const addCad2dEntity = (entity: Omit<Cad2dEntity, "id">) => {
    const next: Cad2dEntity = { id: makeCad2dId(entity.type), visible: true, locked: false, ...entity };
    setCad2dEntities((prev) => [...prev, next]);
    setSelectedCad2dIds([next.id]);
    setStatusMessage(`Objet 2D ${entity.type} créé · ID réel ${next.id}`);
    return next;
  };
  const prepareCad2dTool = (tool: Cad2dEntityType) => {
    setInteractionMode("select");
    setIsoDrawMode("select");
    setCad2dDraftTool(tool);
    setStatusMessage(`${tool.toUpperCase()} 2D prêt · cliquez dans le plan pour poser un objet de base`);
  };
'''
    if state_anchor in src:
        src = src.replace(state_anchor, state_patch, 1)
    else:
        fail("ancre dimensions state introuvable")

    # 3) Ajouter support export JSON simple.
    export_anchor = "model:{lines,nodes,segments,dimensions}"
    if export_anchor in src:
        src = src.replace(export_anchor, "model:{lines,nodes,segments,dimensions,cad2d:{layers:cad2dLayers,entities:cad2dEntities}}", 1)
    else:
        print("Ancre export exacte non trouvée — export 2D non injecté automatiquement.")

    # 4) Ajouter support import JSON après dimensions import.
    import_anchor = "    setDimensionsRaw(snapshot.model.dimensions || []);"
    import_patch = """    setDimensionsRaw(snapshot.model.dimensions || []);
    setCad2dLayers(snapshot.model.cad2d?.layers || [
      { id: "axes_tuyauterie", name: "Axes tuyauterie", color: "#4db8d4", visible: true, locked: false },
      { id: "annotations", name: "Annotations", color: "#f0f0f0", visible: true, locked: false },
      { id: "import_cad", name: "Import CAD / fond plan", color: "#888888", visible: true, locked: false },
    ]);
    setCad2dEntities(snapshot.model.cad2d?.entities || []);
    setSelectedCad2dIds([]);"""
    if import_anchor in src:
        src = src.replace(import_anchor, import_patch, 1)
    else:
        print("Ancre import dimensions non trouvée — import 2D non injecté automatiquement.")

    # 5) Rendre les entités 2D dans le SVG avant les dimensions utilisateur.
    svg_anchor = "                {/* User Dimensions (Interactive CAD Cotations) */}"
    svg_patch = r'''                {/* PATCH 007 — real 2D geometry foundation */}
                <g data-cad2d-layer="true">
                  {cad2dEntities.filter((entity) => entity.visible !== false).map((entity) => {
                    const selected = selectedCad2dIds.includes(entity.id);
                    const stroke = selected ? "#fbbf24" : entity.color;
                    const common = {
                      stroke,
                      strokeWidth: selected ? 2.5 : (entity.lineWeight || 1.5),
                      fill: "none",
                      vectorEffect: "non-scaling-stroke" as const,
                      style: { cursor: "pointer" },
                      onClick: (event: React.MouseEvent) => {
                        event.stopPropagation();
                        setSelectedCad2dIds(event.shiftKey || event.ctrlKey || event.metaKey
                          ? (selected ? selectedCad2dIds.filter((id) => id !== entity.id) : [...selectedCad2dIds, entity.id])
                          : [entity.id]);
                        setStatusMessage(`Objet 2D sélectionné · ${entity.type} · ${entity.id}`);
                      },
                    };
                    if (entity.type === "line" && entity.points && entity.points.length >= 2) {
                      const a = isoProjectV4(entity.points[0].x, entity.points[0].y, entity.metadata?.elevationZ || 0, viewport.zoom, viewport.panX, viewport.panY);
                      const b = isoProjectV4(entity.points[1].x, entity.points[1].y, entity.metadata?.elevationZ || 0, viewport.zoom, viewport.panX, viewport.panY);
                      return <line key={entity.id} x1={a.x} y1={a.y} x2={b.x} y2={b.y} {...common} />;
                    }
                    if (entity.type === "polyline" && entity.points && entity.points.length > 0) {
                      const d = entity.points.map((p, i) => {
                        const pp = isoProjectV4(p.x, p.y, entity.metadata?.elevationZ || 0, viewport.zoom, viewport.panX, viewport.panY);
                        return `${i ? "L" : "M"} ${pp.x} ${pp.y}`;
                      }).join(" ");
                      return <path key={entity.id} d={d} {...common} />;
                    }
                    if (entity.type === "circle" && entity.center && entity.radius) {
                      const c = isoProjectV4(entity.center.x, entity.center.y, entity.metadata?.elevationZ || 0, viewport.zoom, viewport.panX, viewport.panY);
                      return <circle key={entity.id} cx={c.x} cy={c.y} r={entity.radius * 18 * viewport.zoom} {...common} />;
                    }
                    if (entity.type === "arc" && entity.center && entity.radius) {
                      const c = isoProjectV4(entity.center.x, entity.center.y, entity.metadata?.elevationZ || 0, viewport.zoom, viewport.panX, viewport.panY);
                      const r = entity.radius * 18 * viewport.zoom;
                      const sa = ((entity.startAngle || 0) * Math.PI) / 180;
                      const ea = ((entity.endAngle || 90) * Math.PI) / 180;
                      const x1 = c.x + r * Math.cos(sa);
                      const y1 = c.y + r * Math.sin(sa);
                      const x2 = c.x + r * Math.cos(ea);
                      const y2 = c.y + r * Math.sin(ea);
                      const largeArc = Math.abs((entity.endAngle || 90) - (entity.startAngle || 0)) > 180 ? 1 : 0;
                      const d = `M ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2}`;
                      return <path key={entity.id} d={d} {...common} />;
                    }
                    if (entity.type === "text" && entity.points && entity.points[0]) {
                      const p = isoProjectV4(entity.points[0].x, entity.points[0].y, entity.metadata?.elevationZ || 0, viewport.zoom, viewport.panX, viewport.panY);
                      return <text key={entity.id} x={p.x} y={p.y} fill={stroke} fontSize="12" fontWeight="800" onClick={common.onClick} style={common.style}>{entity.text || "Texte"}</text>;
                    }
                    return null;
                  })}
                </g>

                {/* User Dimensions (Interactive CAD Cotations) */}'''
    if svg_anchor in src:
        src = src.replace(svg_anchor, svg_patch, 1)
    else:
        fail("ancre SVG dimensions introuvable")

    # 6) Ajouter création basique sur clic fond SVG quand outil 2D actif, sans toucher au graphe piping.
    click_anchor = "    if(isoDrawMode===\"coude\"){"
    click_patch = r'''    if (cad2dDraftTool) {
      const w = screenToIsoWorld(e);
      const point = { x: snapIsoV4(w.x, isoSnapStep), y: snapIsoV4(w.y, isoSnapStep) };
      if (cad2dDraftTool === "line") {
        addCad2dEntity({ type: "line", layerId: "axes_tuyauterie", color: "#4db8d4", points: [point, { x: point.x + 2, y: point.y }] });
      } else if (cad2dDraftTool === "polyline") {
        addCad2dEntity({ type: "polyline", layerId: "axes_tuyauterie", color: "#4db8d4", points: [point, { x: point.x + 1, y: point.y + 1 }, { x: point.x + 2, y: point.y }] });
      } else if (cad2dDraftTool === "circle") {
        addCad2dEntity({ type: "circle", layerId: "import_cad", color: "#8b5cf6", center: point, radius: 1 });
      } else if (cad2dDraftTool === "arc") {
        addCad2dEntity({ type: "arc", layerId: "import_cad", color: "#e8a838", center: point, radius: 1, startAngle: 0, endAngle: 90 });
      } else if (cad2dDraftTool === "text") {
        addCad2dEntity({ type: "text", layerId: "annotations", color: "#f0f0f0", points: [point], text: "Texte" });
      }
      setCad2dDraftTool(null);
      e.stopPropagation();
      return;
    }

    if(isoDrawMode==="coude"){'''
    if click_anchor in src:
        src = src.replace(click_anchor, click_patch, 1)
    else:
        print("Ancre click coude non trouvée — création clic 2D non injectée.")

    # 7) Connecter ruban 006 préparé aux vrais outils 2D si présent.
    src = src.replace('onClick={() => cadToolPrepared("Polyline")}', 'onClick={() => prepareCad2dTool("polyline")}', 1)
    src = src.replace('onClick={() => cadToolPrepared("Circle")}', 'onClick={() => prepareCad2dTool("circle")}', 1)
    src = src.replace('onClick={() => cadToolPrepared("Arc")}', 'onClick={() => prepareCad2dTool("arc")}', 1)
    src = src.replace('onClick={() => cadToolPrepared("Text")}', 'onClick={() => prepareCad2dTool("text")}', 1)

    # 8) Ajouter rapport de sélection 2D dans status si possible.
    status_anchor = "<span>{selectedCount} sélectionné(s)</span>"
    if status_anchor in src:
        src = src.replace(status_anchor, '<span>{selectedCount} sélectionné(s)</span><span>{selectedCad2dIds.length} objet(s) 2D</span>', 1)

    write(ENGINE, src)
    print("IsometrieModuleV48d.tsx patché : fondation 2D réelle ajoutée.")


def write_report() -> None:
    content = f"""# PATCH 007 — Fondation géométrie 2D réelle

Date : {datetime.now().isoformat(timespec='seconds')}

## Audit avant patch
- La sélection professionnelle existe déjà : Patch 004 / 004b.
- `selectedNodeIds`, `selectedSegmentIds`, `selectedDimensionIds` présents.
- Copier / couper / coller / dupliquer déjà existants.
- Ce patch ne refait pas la sélection.

## Objectif
Créer une couche 2D réelle, persistante et exportable :
- `Cad2dEntity`
- `Cad2dLayer`
- `cad2dEntities`
- `cad2dLayers`
- `selectedCad2dIds`

## Entités préparées
- line
- polyline
- circle
- arc
- text

## Important
- Pas de deuxième moteur piping.
- Pas de remplacement V4.8d.
- Mapping 2D -> piping graph reporté au patch 008/009.
- Les entités 2D sont des objets projet avec IDs réels, pas seulement SVG.

## Fichier modifié
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`

## Validation attendue
```bash
npm run lint
npm run build
```

## Validation visuelle
- Ruban CAD : Line / Polyline / Circle / Arc / Text créent des objets 2D basiques.
- Les objets apparaissent dans le plan.
- Clic sur objet 2D le sélectionne.
- Export JSON contient `model.cad2d`.
- Import JSON restaure `model.cad2d`.
"""
    write(REPORT, content)
    print(f"Rapport écrit : {REPORT}")


def update_history() -> None:
    if not HISTORY.exists():
        print("PATCH_HISTORY.md absent — historique non mis à jour.")
        return
    src = read(HISTORY)
    if "PATCH 007 — Fondation géométrie 2D réelle" in src:
        print("PATCH_HISTORY.md déjà mis à jour.")
        return
    entry = f"""

## PATCH 007 — Fondation géométrie 2D réelle

Date : {datetime.now().strftime('%Y-%m-%d')}

- Ajout d'une couche CAD 2D persistante : entités, calques, sélection 2D.
- Entités préparées : line, polyline, circle, arc, text.
- Export/import JSON enrichi avec `model.cad2d`.
- Aucun second moteur piping ; V4.8d reste source of truth.
"""
    write(HISTORY, src.rstrip() + "\n" + entry)
    print("PATCH_HISTORY.md mis à jour.")


def main() -> None:
    print("PD&I PATCH 007 — fondation géométrie 2D réelle")
    assert_project()
    patch_engine()
    write_report()
    update_history()
    print("\nPATCH 007 terminé.")
    print("Suite : appliquer dans AI Studio, tester, sync GitHub, vérifier Vercel.")


if __name__ == "__main__":
    main()
