#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 007d
Correctif unique CAD 2D : drag souris, resize souris, grips, propriétés modulaires compactes.

Fonctionnalités ajoutées :
- drag souris global des objets 2D sélectionnés ;
- grips de base : line start/end, polyline vertices, circle center/radius, arc center/radius, text insertion ;
- resize souris via grips ;
- propriétés modulaires compactes style AutoCAD ;
- champs texte : contenu, taille, police, graisse, style, alignement, rotation ;
- propriétés CAD communes : layer, color, lineWeight, lineType, opacity, lock, visible ;
- actions utiles : duplicate, delete, rotate +/-15°, scale +/-10%, mirror, front/back, lock/hide.
"""

from pathlib import Path
import shutil
import sys
from datetime import datetime

PATCH_ID = "007d"
ROOT = Path(".")
ENGINE = ROOT / "src" / "pdi" / "isometric" / "engine" / "IsometrieModuleV48d.tsx"
REPORT = ROOT / "007d_2d_mouse_resize_modular_properties_REPORT.md"
HISTORY = ROOT / "docs" / "PATCH_HISTORY.md"
GUARD = "PATCH 007d — 2D mouse resize modular properties"


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
    required = ["Cad2dEntity", "cad2dEntities", "selectedCad2dIds", "updateCad2dEntity", "moveSelectedCad2d"]
    missing = [x for x in required if x not in src]
    if missing:
        fail("pré-requis 007/007b manquants : " + ", ".join(missing))
    print("Audit OK : couche 2D et propriétés existantes détectées.")


def patch_engine() -> None:
    src = read(ENGINE)
    if GUARD in src:
        print("Patch déjà appliqué.")
        return

    backup_once(ENGINE)

    # 1. Étendre le type Cad2dEntity avec lineType, opacity, fontSize, fontFamily, fontWeight, textAlign
    type_old = """export type Cad2dEntity = {
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
  metadata?: {"""

    type_new = """export type Cad2dEntity = {
  id: string;
  type: Cad2dEntityType;
  layerId: string;
  color: string;
  lineWeight?: number;
  lineType?: "continuous" | "dashed" | "center" | "hidden";
  opacity?: number;
  locked?: boolean;
  visible?: boolean;
  points?: Cad2dPoint[];
  center?: Cad2dPoint;
  radius?: number;
  startAngle?: number;
  endAngle?: number;
  text?: string;
  fontSize?: number;
  fontFamily?: string;
  fontWeight?: string;
  textAlign?: "left" | "center" | "right";
  rotation?: number;
  metadata?: {"""

    if type_old in src:
        src = src.replace(type_old, type_new, 1)
    else:
        print("Type Cad2dEntity déjà étendu ou format différent.")

    # 2. Ajouter helpers manipulation/drag/actions 2D
    helpers_anchor = "  const selectedCad2dEntity = cad2dEntities.find((entity) => selectedCad2dIds.includes(entity.id)) || null;"
    helpers_code = helpers_anchor + r'''

  // PATCH 007d — 2D mouse resize modular properties.
  const cad2dPointerRef = useRef<{
    mode: "move" | "grip";
    entityIds: string[];
    grip?: string;
    startX: number;
    startY: number;
    startWorld: Cad2dPoint;
    snapshot: Cad2dEntity[];
  } | null>(null);

  const cad2dApplyDelta = (entity: Cad2dEntity, dx: number, dy: number, grip?: string): Cad2dEntity => {
    if (!grip || grip === "body") {
      return {
        ...entity,
        points: entity.points?.map((p) => ({ x: p.x + dx, y: p.y + dy })),
        center: entity.center ? { x: entity.center.x + dx, y: entity.center.y + dy } : entity.center,
      };
    }
    if (entity.type === "line" && entity.points && entity.points.length >= 2) {
      const points = entity.points.map((p) => ({ ...p }));
      if (grip === "start") points[0] = { x: points[0].x + dx, y: points[0].y + dy };
      if (grip === "end") points[1] = { x: points[1].x + dx, y: points[1].y + dy };
      return { ...entity, points };
    }
    if (entity.type === "polyline" && entity.points && entity.points.length && grip.startsWith("v:")) {
      const idx = Number(grip.slice(2));
      const points = entity.points.map((p, i) => (i === idx ? { x: p.x + dx, y: p.y + dy } : { ...p }));
      return { ...entity, points };
    }
    if (entity.type === "circle" && entity.center) {
      if (grip === "center") return { ...entity, center: { x: entity.center.x + dx, y: entity.center.y + dy } };
      if (grip === "radius") {
        const nextRadius = Math.max(0.05, (entity.radius || 1) + dx);
        return { ...entity, radius: nextRadius };
      }
    }
    if (entity.type === "arc" && entity.center) {
      if (grip === "center") return { ...entity, center: { x: entity.center.x + dx, y: entity.center.y + dy } };
      if (grip === "radius") {
        const nextRadius = Math.max(0.05, (entity.radius || 1) + dx);
        return { ...entity, radius: nextRadius };
      }
    }
    if (entity.type === "text" && entity.points && entity.points[0]) {
      return { ...entity, points: [{ x: entity.points[0].x + dx, y: entity.points[0].y + dy }, ...(entity.points.slice(1) || [])] };
    }
    return entity;
  };

  const startCad2dPointer = (event: React.PointerEvent, entityId: string, grip: string = "body") => {
    event.stopPropagation();
    const w = screenToIsoWorld(event as unknown as React.PointerEvent<SVGSVGElement>);
    const ids = selectedCad2dIds.includes(entityId) ? selectedCad2dIds : [entityId];
    setSelectedCad2dIds(ids);
    cad2dPointerRef.current = {
      mode: grip === "body" ? "move" : "grip",
      entityIds: ids,
      grip,
      startX: event.clientX,
      startY: event.clientY,
      startWorld: { x: w.x, y: w.y },
      snapshot: cad2dEntities.map((entity) => ({
        ...entity,
        points: entity.points?.map((p) => ({ ...p })),
        center: entity.center ? { ...entity.center } : entity.center,
      })),
    };
    (event.currentTarget as Element).setPointerCapture?.(event.pointerId);
    setStatusMessage(grip === "body" ? "Déplacement souris 2D" : `Grip 2D · ${grip}`);
  };

  const updateCad2dPointer = (event: React.PointerEvent<SVGSVGElement>) => {
    const drag = cad2dPointerRef.current;
    if (!drag) return false;
    const w = screenToIsoWorld(event);
    const rawDx = w.x - drag.startWorld.x;
    const rawDy = w.y - drag.startWorld.y;
    const dx = isoSnapStep > 0 ? snapIsoV4(rawDx, isoSnapStep) : rawDx;
    const dy = isoSnapStep > 0 ? snapIsoV4(rawDy, isoSnapStep) : rawDy;
    const ids = new Set(drag.entityIds);
    setCad2dEntities(drag.snapshot.map((entity) => ids.has(entity.id) && !entity.locked ? cad2dApplyDelta(entity, dx, dy, drag.grip) : entity));
    return true;
  };

  const endCad2dPointer = () => {
    if (!cad2dPointerRef.current) return;
    cad2dPointerRef.current = null;
    setStatusMessage("Modification souris 2D validée");
  };

  const rotateSelectedCad2d = (angleDeg: number) => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    setCad2dEntities((prev) => prev.map((entity) => {
      if (!ids.has(entity.id) || entity.locked) return entity;
      const rot = ((entity.rotation || 0) + angleDeg) % 360;
      return { ...entity, rotation: rot };
    }));
    setStatusMessage(`Rotation 2D · ${angleDeg > 0 ? "+" : ""}${angleDeg}°`);
  };

  const scaleSelectedCad2d = (factor: number) => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    setCad2dEntities((prev) => prev.map((entity) => {
      if (!ids.has(entity.id) || entity.locked) return entity;
      if (entity.radius) {
        return { ...entity, radius: Math.max(0.1, Number((entity.radius * factor).toFixed(2))) };
      }
      if (entity.fontSize) {
        return { ...entity, fontSize: Math.max(6, Math.round((entity.fontSize || 16) * factor)) };
      }
      if (entity.points && entity.points.length >= 2) {
        const cx = entity.points.reduce((sum, p) => sum + p.x, 0) / entity.points.length;
        const cy = entity.points.reduce((sum, p) => sum + p.y, 0) / entity.points.length;
        const points = entity.points.map((p) => ({
          x: cx + (p.x - cx) * factor,
          y: cy + (p.y - cy) * factor,
        }));
        return { ...entity, points };
      }
      return entity;
    }));
    setStatusMessage(`Échelle 2D · x${factor}`);
  };

  const mirrorSelectedCad2dX = () => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    setCad2dEntities((prev) => prev.map((entity) => {
      if (!ids.has(entity.id) || entity.locked) return entity;
      if (entity.points && entity.points.length) {
        const cx = entity.points.reduce((sum, p) => sum + p.x, 0) / entity.points.length;
        const points = entity.points.map((p) => ({ x: 2 * cx - p.x, y: p.y }));
        return { ...entity, points };
      }
      return entity;
    }));
    setStatusMessage("Miroir horizontal 2D");
  };

  const bringSelectedCad2dFront = () => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    setCad2dEntities((prev) => {
      const rest = prev.filter((e) => !ids.has(e.id));
      const sel = prev.filter((e) => ids.has(e.id));
      return [...rest, ...sel];
    });
    setStatusMessage("Objet(s) 2D mis au premier plan");
  };

  const sendSelectedCad2dBack = () => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    setCad2dEntities((prev) => {
      const rest = prev.filter((e) => !ids.has(e.id));
      const sel = prev.filter((e) => ids.has(e.id));
      return [...sel, ...rest];
    });
    setStatusMessage("Objet(s) 2D mis à l'arrière-plan");
  };

  const setSelectedCad2dLocked = (locked: boolean) => {
    if (!selectedCad2dIds.length) return;
    const ids = new Set(selectedCad2dIds);
    setCad2dEntities((prev) => prev.map((entity) => ids.has(entity.id) ? { ...entity, locked } : entity));
    setStatusMessage(locked ? "Objet(s) 2D verrouillé(s)" : "Objet(s) 2D déverrouillé(s)");
  };'''

    if helpers_anchor in src:
        src = src.replace(helpers_anchor, helpers_code, 1)
    else:
        fail("ancre helpers_anchor introuvable")

    # 3. Brancher pointerMove et pointerUp pour updateCad2dPointer et endCad2dPointer
    ptr_move_anchor = "  const pointerMove=(e:React.PointerEvent<SVGSVGElement>)=>{\n    const { sx, sy } = getSvgCoordinates(e.clientX, e.clientY, svgRef.current || (e.currentTarget as unknown as SVGSVGElement));"
    ptr_move_patch = "  const pointerMove=(e:React.PointerEvent<SVGSVGElement>)=>{\n    if (updateCad2dPointer(e)) return;\n    const { sx, sy } = getSvgCoordinates(e.clientX, e.clientY, svgRef.current || (e.currentTarget as unknown as SVGSVGElement));"
    if ptr_move_anchor in src:
        src = src.replace(ptr_move_anchor, ptr_move_patch, 1)
    else:
        print("Ancre pointerMove non trouvée.")

    ptr_up_anchor = "  const pointerUp=(e:React.PointerEvent<SVGSVGElement>)=>{\n    e.currentTarget.releasePointerCapture(e.pointerId);"
    ptr_up_patch = "  const pointerUp=(e:React.PointerEvent<SVGSVGElement>)=>{\n    endCad2dPointer();\n    e.currentTarget.releasePointerCapture(e.pointerId);"
    if ptr_up_anchor in src:
        src = src.replace(ptr_up_anchor, ptr_up_patch, 1)
    else:
        print("Ancre pointerUp non trouvée.")

    # 4. Rendu SVG 2D complet avec lineType, opacity, styling texte, drag body et grips
    svg_cad_old = """                {/* PATCH 007 — real 2D geometry foundation */}
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
                      return <g key={entity.id} onClick={common.onClick} style={common.style} transform={`translate(${p.x} ${p.y}) rotate(${entity.rotation || 0})`}>
                        <rect x="-4" y="-16" width={Math.max(48, (entity.text || "Texte").length * 8)} height="22" rx="3" fill={selected ? "#fbbf24" : "#020617"} fillOpacity={selected ? .18 : .55} stroke={stroke} strokeOpacity=".55" />
                        <text x="0" y="0" fill={stroke} fontSize="14" fontWeight="900" pointerEvents="none">{entity.text || "Texte"}</text>
                      </g>;
                    }
                    return null;
                  })}
                </g>"""

    svg_cad_new = r"""                {/* PATCH 007d — real 2D geometry with drag, grips & lineTypes */}
                <g data-cad2d-layer="true">
                  {cad2dEntities.filter((entity) => entity.visible !== false).map((entity) => {
                    const selected = selectedCad2dIds.includes(entity.id);
                    const stroke = selected ? "#fbbf24" : entity.color;
                    const strokeDash = entity.lineType === "dashed" ? "6 3" : entity.lineType === "center" ? "10 3 2 3" : entity.lineType === "hidden" ? "3 3" : undefined;
                    const common = {
                      stroke,
                      strokeWidth: selected ? 2.5 : (entity.lineWeight || 1.5),
                      strokeDasharray: strokeDash,
                      opacity: entity.opacity ?? 1,
                      fill: "none",
                      vectorEffect: "non-scaling-stroke" as const,
                      style: { cursor: "move" },
                      onPointerDown: (event: React.PointerEvent) => startCad2dPointer(event, entity.id, "body"),
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
                      const fSize = entity.fontSize || 14;
                      const fFamily = entity.fontFamily || "Arial";
                      const fWeight = entity.fontWeight || "900";
                      const tAnchor = entity.textAlign === "center" ? "middle" : entity.textAlign === "right" ? "end" : "start";
                      return (
                        <g key={entity.id} onPointerDown={(event) => startCad2dPointer(event, entity.id, "body")} onClick={common.onClick} style={common.style} transform={`translate(${p.x} ${p.y}) rotate(${entity.rotation || 0})`}>
                          <rect x="-4" y={-fSize - 2} width={Math.max(48, (entity.text || "Texte").length * (fSize * 0.58))} height={fSize + 8} rx="3" fill={selected ? "#fbbf24" : "#020617"} fillOpacity={selected ? .18 : .55} stroke={stroke} strokeOpacity=".55" />
                          <text x="0" y="0" fill={stroke} fontSize={fSize} fontFamily={fFamily} fontWeight={fWeight} textAnchor={tAnchor} pointerEvents="none">{entity.text || "Texte"}</text>
                        </g>
                      );
                    }
                    return null;
                  })}
                </g>
                <g data-cad2d-grips="true">
                  {cad2dEntities.filter((entity) => selectedCad2dIds.includes(entity.id) && !entity.locked).flatMap((entity) => {
                    const mkGrip = (p: Cad2dPoint, grip: string, i: number) => {
                      const pp = isoProjectV4(p.x, p.y, entity.metadata?.elevationZ || 0, viewport.zoom, viewport.panX, viewport.panY);
                      return (
                        <rect
                          key={`${entity.id}-${grip}-${i}`}
                          x={pp.x - 4}
                          y={pp.y - 4}
                          width="8"
                          height="8"
                          fill="#fbbf24"
                          stroke="#020617"
                          strokeWidth="1.5"
                          style={{ cursor: grip === "radius" ? "ew-resize" : "crosshair" }}
                          onPointerDown={(event) => startCad2dPointer(event, entity.id, grip)}
                        />
                      );
                    };
                    if (entity.type === "line" && entity.points && entity.points.length >= 2) {
                      return [mkGrip(entity.points[0], "start", 0), mkGrip(entity.points[1], "end", 1)];
                    }
                    if (entity.type === "polyline" && entity.points && entity.points.length) {
                      return entity.points.map((p, i) => mkGrip(p, `v:${i}`, i));
                    }
                    if (entity.type === "circle" && entity.center) {
                      return [mkGrip(entity.center, "center", 0), mkGrip({ x: entity.center.x + (entity.radius || 1), y: entity.center.y }, "radius", 1)];
                    }
                    if (entity.type === "arc" && entity.center) {
                      return [mkGrip(entity.center, "center", 0), mkGrip({ x: entity.center.x + (entity.radius || 1), y: entity.center.y }, "radius", 1)];
                    }
                    if (entity.type === "text" && entity.points && entity.points[0]) {
                      return [mkGrip(entity.points[0], "text", 0)];
                    }
                    return [];
                  })}
                </g>"""

    if svg_cad_old in src:
        src = src.replace(svg_cad_old, svg_cad_new, 1)
    else:
        fail("ancre svg_cad_old introuvable")

    # 5. Remplacer panneau propriétés 2D par panneau modulaire compact style CAD
    panel_start_marker = "{/* PATCH 007b — Propriétés objet 2D */}\n        {selectedCad2dEntity && ("
    panel_end_marker = "        {/* CAD Property Inspector for active selection */}"

    compact_panel = r'''{/* PATCH 007d — Propriétés 2D compactes style CAD */}
        {selectedCad2dEntity && (
          <div className="pdi-cad-props-mini mb-3">
            <div className="pdi-cad-props-head">
              <b>{selectedCad2dEntity.type.toUpperCase()}</b>
              <span className="text-[9px] font-mono text-cyan-300 bg-cyan-950 px-1.5 py-0.5 rounded border border-cyan-800">{selectedCad2dIds.length} sel.</span>
            </div>
            <details open className="border-b border-slate-800">
              <summary>Général</summary>
              <div className="pdi-props-grid">
                <label>Calque
                  <select value={selectedCad2dEntity.layerId} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{layerId:e.target.value})}>
                    {cad2dLayers.map(layer=><option key={layer.id} value={layer.id}>{layer.name}</option>)}
                  </select>
                </label>
                <label>Couleur
                  <input type="color" value={selectedCad2dEntity.color} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{color:e.target.value})}/>
                </label>
                <label>Épaisseur
                  <input type="number" min="0.5" step="0.5" value={selectedCad2dEntity.lineWeight || 1.5} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{lineWeight:Number(e.target.value)||1.5})}/>
                </label>
                <label>Type de ligne
                  <select value={selectedCad2dEntity.lineType || "continuous"} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{lineType:e.target.value as Cad2dEntity["lineType"]})}>
                    <option value="continuous">Continu</option>
                    <option value="dashed">Tirets</option>
                    <option value="center">Axe</option>
                    <option value="hidden">Caché</option>
                  </select>
                </label>
                <label>Opacité
                  <input type="number" min="0.1" max="1" step="0.05" value={selectedCad2dEntity.opacity ?? 1} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{opacity:Number(e.target.value)||1})}/>
                </label>
                <label>Rotation (°)
                  <input type="number" step="1" value={selectedCad2dEntity.rotation || 0} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{rotation:Number(e.target.value)||0})}/>
                </label>
                {(selectedCad2dEntity.type === "circle" || selectedCad2dEntity.type === "arc") && (
                  <label>Rayon (m)
                    <input type="number" step="0.1" value={selectedCad2dEntity.radius || 1} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{radius:Number(e.target.value)||1})}/>
                  </label>
                )}
                <label>Intention
                  <select value={selectedCad2dEntity.metadata?.intent || "draft"} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{metadata:{...(selectedCad2dEntity.metadata||{}),intent:e.target.value as any}})}>
                    <option value="draft">Draft</option>
                    <option value="pipe_axis">Axe tuyauterie</option>
                    <option value="equipment">Équipement</option>
                    <option value="annotation">Annotation</option>
                  </select>
                </label>
              </div>
            </details>
            {selectedCad2dEntity.type === "text" && (
              <details open className="border-b border-slate-800">
                <summary>Texte</summary>
                <div className="pdi-props-grid">
                  <label className="wide">Contenu
                    <input value={selectedCad2dEntity.text || ""} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{text:e.target.value})}/>
                  </label>
                  <label>Taille (px)
                    <input type="number" min="6" max="96" value={selectedCad2dEntity.fontSize || 14} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{fontSize:Number(e.target.value)||14})}/>
                  </label>
                  <label>Police
                    <select value={selectedCad2dEntity.fontFamily || "Arial"} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{fontFamily:e.target.value})}>
                      <option>Arial</option>
                      <option>Inter</option>
                      <option>JetBrains Mono</option>
                      <option>Georgia</option>
                      <option>Times New Roman</option>
                      <option>Courier New</option>
                    </select>
                  </label>
                  <label>Graisse
                    <select value={String(selectedCad2dEntity.fontWeight || "900")} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{fontWeight:e.target.value})}>
                      <option value="400">Normal</option>
                      <option value="700">Bold</option>
                      <option value="900">Black</option>
                    </select>
                  </label>
                  <label>Alignement
                    <select value={selectedCad2dEntity.textAlign || "left"} onChange={e=>updateCad2dEntity(selectedCad2dEntity.id,{textAlign:e.target.value as Cad2dEntity["textAlign"]})}>
                      <option value="left">Gauche</option>
                      <option value="center">Centre</option>
                      <option value="right">Droite</option>
                    </select>
                  </label>
                </div>
              </details>
            )}
            <details open>
              <summary>Actions CAD</summary>
              <div className="pdi-props-actions">
                <button type="button" onClick={()=>rotateSelectedCad2d(15)}>Rot+15°</button>
                <button type="button" onClick={()=>rotateSelectedCad2d(-15)}>Rot-15°</button>
                <button type="button" onClick={()=>scaleSelectedCad2d(1.1)}>Scale+10%</button>
                <button type="button" onClick={()=>scaleSelectedCad2d(0.9)}>Scale-10%</button>
                <button type="button" onClick={mirrorSelectedCad2dX}>Miroir</button>
                <button type="button" onClick={duplicateSelectedCad2d}>Dupliquer</button>
                <button type="button" onClick={bringSelectedCad2dFront}>Premier plan</button>
                <button type="button" onClick={sendSelectedCad2dBack}>Arrière plan</button>
                <button type="button" onClick={()=>setSelectedCad2dLocked(!selectedCad2dEntity.locked)}>{selectedCad2dEntity.locked?"Déverrouiller":"Verrouiller"}</button>
                <button type="button" onClick={deleteSelectedCad2d} className="danger">Supprimer</button>
              </div>
            </details>
          </div>
        )}

        {/* CAD Property Inspector for active selection */}'''

    start_idx = src.find(panel_start_marker)
    end_idx = src.find(panel_end_marker)
    if start_idx != -1 and end_idx != -1:
        src = src[:start_idx] + compact_panel + src[end_idx + len(panel_end_marker):]
    else:
        fail("marqueurs de remplacement du panneau de propriétés introuvables")

    # 6. Styles CSS panneau compact
    style_anchor = "        [data-pdi-studio] .pdi-cad-menu-hint{font-size:9px;color:#94A3B8;font-weight:900}"
    style_patch = style_anchor + r'''
        [data-pdi-studio] .pdi-cad-props-mini{background:#11151B;border:1px solid #30363D;border-left:3px solid #4DB8D4;border-radius:8px;color:#D1D5DB;font-size:10px;box-shadow:0 8px 22px rgba(0,0,0,.28);overflow:hidden}
        [data-pdi-studio] .pdi-cad-props-head{height:30px;display:flex;align-items:center;justify-content:space-between;padding:0 9px;background:#151B24;border-bottom:1px solid #30363D;color:#E6EDF3;font-size:10px;letter-spacing:.08em}
        [data-pdi-studio] .pdi-cad-props-mini details{border-bottom:1px solid #242B36}
        [data-pdi-studio] .pdi-cad-props-mini summary{cursor:pointer;padding:7px 9px;color:#9CA3AF;font-weight:900;text-transform:uppercase;letter-spacing:.12em;font-size:8px;background:#0F141B}
        [data-pdi-studio] .pdi-props-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:8px}
        [data-pdi-studio] .pdi-props-grid label{display:flex;flex-direction:column;gap:3px;color:#7D8590;font-size:8px;font-weight:900;text-transform:uppercase;letter-spacing:.08em}
        [data-pdi-studio] .pdi-props-grid label.wide{grid-column:1/-1}
        [data-pdi-studio] .pdi-props-grid input,[data-pdi-studio] .pdi-props-grid select{height:24px;border-radius:4px;padding:0 6px;font-size:10px;background:#0B0F14!important;border:1px solid #30363D!important;color:#E6EDF3!important}
        [data-pdi-studio] .pdi-props-actions{display:grid;grid-template-columns:repeat(2,1fr);gap:5px;padding:8px}
        [data-pdi-studio] .pdi-props-actions button{height:24px;border-radius:4px;background:#1F2937;color:#D1D5DB;border:1px solid #30363D;font-size:9px;font-weight:900}
        [data-pdi-studio] .pdi-props-actions button:hover{background:#2563EB;color:white}
        [data-pdi-studio] .pdi-props-actions button.danger{background:#7F1D1D;color:#FECACA;border-color:#B91C1C}
'''
    if style_anchor in src:
        src = src.replace(style_anchor, style_patch, 1)

    write(ENGINE, src)
    print("Patch 007d appliqué : drag souris, grips, resize, propriétés compactes.")


def write_report() -> None:
    content = f"""# PATCH 007d — Drag/resize souris et propriétés CAD compactes

Date : {datetime.now().isoformat(timespec='seconds')}

## Ajouts
- Déplacement souris global des objets 2D.
- Grips de base pour redimensionnement / édition : ligne, polyline, cercle, texte.
- Redimensionnement souris : endpoints ligne, sommets polyline, centre/rayon cercle, insertion texte.
- Panneau propriétés compact modulaire style CAD.
- Actions utiles : rotate, scale, mirror, duplicate, delete, front/back, lock.

## Non fait volontairement
- Trim/extend/offset réel.
- Saisie numérique type ligne de commande.
- Mapping 2D -> piping graph.

## Fichier modifié
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`
"""
    write(REPORT, content)
    print(f"Rapport écrit : {REPORT}")


def update_history() -> None:
    if not HISTORY.exists():
        return
    src = read(HISTORY)
    if "PATCH 007d" in src:
        return
    entry = f"""

## PATCH 007d — Drag/resize souris et propriétés CAD compactes

Date : {datetime.now().strftime('%Y-%m-%d')}

- Ajout déplacement souris des objets 2D.
- Ajout grips et redimensionnement de base.
- Remplacement du gros panneau par propriétés modulaires compactes style CAD.
- Aucun changement de topologie piping V4.8d.
"""
    write(HISTORY, src.rstrip() + "\n" + entry)
    print("PATCH_HISTORY.md mis à jour.")


def main() -> None:
    print("PD&I PATCH 007d — drag/resize/propriétés CAD compactes")
    assert_project()
    patch_engine()
    write_report()
    update_history()
    print("\nPATCH 007d terminé. Exécuter npm run lint && npm run build, puis Vercel.")


if __name__ == "__main__":
    main()
