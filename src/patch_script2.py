import sys

TARGET = "src/components/Calculators.tsx"

with open(TARGET, "r", encoding="utf-8") as f:
    code = f.read()

applied = []
skipped = []

def do_replace(label, old, new):
    global code
    if old in code:
        code = code.replace(old, new, 1)
        applied.append(label)
    else:
        skipped.append(label)


# ---------------------------------------------------------------------------
# STEP 1 — Data model: gabionSides[side] moves from a single etages/width/
# height/gap tuple to a `tiers` list, one entry per étage, each with its own
# height, depth, and redan (fixed meters OR % of the tier below).
# ---------------------------------------------------------------------------

do_replace(
    "1a. initial ouvrage-1: gabionSides becomes tier-based",
    '''      gabionSides: {
        nord: { enabled: false, etages: 1, length: 12, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
        sud: { enabled: false, etages: 2, length: 12, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
        est: { enabled: false, etages: 3, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
        ouest: { enabled: false, etages: 2, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
      }''',
    '''      gabionSides: {
        nord: { enabled: false, length: 12, offset: 0, tiers: [{ height: 1, depth: 1, redanMode: "fixe", redanValue: 0 }] },
        sud: { enabled: false, length: 12, offset: 0, tiers: [
          { height: 1, depth: 1.2, redanMode: "fixe", redanValue: 0 },
          { height: 0.8, depth: 1.0, redanMode: "fixe", redanValue: 0.4 }
        ] },
        est: { enabled: false, length: 10, offset: 0, tiers: [
          { height: 1, depth: 1.2, redanMode: "fixe", redanValue: 0 },
          { height: 0.8, depth: 1.0, redanMode: "fixe", redanValue: 0.4 },
          { height: 0.6, depth: 0.8, redanMode: "pourcentage", redanValue: 30 }
        ] },
        ouest: { enabled: false, length: 10, offset: 0, tiers: [
          { height: 1, depth: 1.2, redanMode: "fixe", redanValue: 0 },
          { height: 0.8, depth: 1.0, redanMode: "fixe", redanValue: 0.4 }
        ] },
      }''',
)

do_replace(
    "1b. handleAddOuvrage: gabionSides becomes tier-based for new ouvrages too",
    '''        gabionSides: {
          nord: { enabled: false, etages: 1, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
          sud: { enabled: false, etages: 1, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
          est: { enabled: false, etages: 1, length: 8, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
          ouest: { enabled: false, etages: 1, length: 8, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
        }''',
    '''        gabionSides: {
          nord: { enabled: false, length: 10, offset: 0, tiers: [{ height: 1, depth: 1, redanMode: "fixe", redanValue: 0 }] },
          sud: { enabled: false, length: 10, offset: 0, tiers: [{ height: 1, depth: 1, redanMode: "fixe", redanValue: 0 }] },
          est: { enabled: false, length: 8, offset: 0, tiers: [{ height: 1, depth: 1, redanMode: "fixe", redanValue: 0 }] },
          ouest: { enabled: false, length: 8, offset: 0, tiers: [{ height: 1, depth: 1, redanMode: "fixe", redanValue: 0 }] },
        }''',
)


# ---------------------------------------------------------------------------
# STEP 2 — Render: one line per tier, offset by the cumulative redan, still
# draggable as a single whole-wall group (offset stays at the side level).
# ---------------------------------------------------------------------------

do_replace(
    "2. gabions render: iterate tiers, draw N lines with cumulative redan",
    '''                                    {/* Gabions Protection Walls around Ouvrage (longueur + position réglables sur le côté) */}
                                    {ov.hasGabions && ov.gabionSides && (
                                      <g>
                                        {(Object.keys(ov.gabionSides) as Array<"nord" | "sud" | "est" | "ouest">).map((side) => {
                                          const gConf = ov.gabionSides?.[side];
                                          if (!gConf || !gConf.enabled) return null;
                                          const gDepth = Math.max(2, (gConf.width || 1) * scale);
                                          const wallLen = (side === "nord" || side === "sud") ? fW : fH;
                                          const gSpan = Math.min(wallLen, Math.max(4, (gConf.length || 10) * scale));
                                          const clampedOffset = Math.min(Math.max(0, (gConf.offset || 0) * scale), Math.max(0, wallLen - gSpan));
                                          let gx = fX, gy = fY, gw = gSpan, gh = gDepth;
                                          if (side === "nord") { gx = fX + clampedOffset; gy = fY - gDepth - 4; }
                                          else if (side === "sud") { gx = fX + clampedOffset; gy = fY + fH + 4; }
                                          else if (side === "ouest") { gx = fX - gDepth - 4; gw = gDepth; gh = gSpan; }
                                          else if (side === "est") { gx = fX + fW + 4; gy = fY + clampedOffset; gw = gDepth; gh = gSpan; }

                                          return (
                                            <g
                                              key={`gabion-${ov.id}-${side}`}
                                              className="cursor-move"
                                              onMouseDown={(e) => {
                                                e.stopPropagation();
                                                setDraggingGabionKey(`${ov.id}:${side}`);
                                                const svgRect = e.currentTarget.ownerSVGElement?.getBoundingClientRect();
                                                if (svgRect) {
                                                  setDragStartPos({
                                                    pointerX: e.clientX - svgRect.left,
                                                    pointerY: e.clientY - svgRect.top,
                                                    initX: gConf.offset || 0,
                                                    initY: 0
                                                  });
                                                }
                                              }}
                                            >
                                              <rect
                                                x={gx}
                                                y={gy}
                                                width={gw}
                                                height={gh}
                                                fill="url(#hatchGabion)"
                                                stroke="#f59e0b"
                                                strokeWidth="1.2"
                                                rx="1"
                                              />
                                              <text x={gx + gw / 2} y={gy + gh / 2 + 3} fill="#fbbf24" fontSize="8" fontWeight="bold" textAnchor="middle">
                                                Gabion ({gConf.etages} ET)
                                              </text>
                                            </g>
                                          );
                                        })}
                                      </g>
                                    )}''',
    '''                                    {/* Gabions Protection Walls around Ouvrage (1 ligne par étage, retrait cumulé) */}
                                    {ov.hasGabions && ov.gabionSides && (
                                      <g>
                                        {(Object.keys(ov.gabionSides) as Array<"nord" | "sud" | "est" | "ouest">).map((side) => {
                                          const gConf = ov.gabionSides?.[side];
                                          if (!gConf || !gConf.enabled || !gConf.tiers || gConf.tiers.length === 0) return null;
                                          const wallLen = (side === "nord" || side === "sud") ? fW : fH;
                                          const gSpan = Math.min(wallLen, Math.max(4, (gConf.length || 10) * scale));
                                          const clampedOffset = Math.min(Math.max(0, (gConf.offset || 0) * scale), Math.max(0, wallLen - gSpan));

                                          let cumulative = 0;
                                          const tierPositions = gConf.tiers.map((t, idx) => {
                                            if (idx > 0) {
                                              const prevDepth = gConf.tiers[idx - 1].depth || 1;
                                              const redan = t.redanMode === "pourcentage" ? (prevDepth * (t.redanValue || 0)) / 100 : (t.redanValue || 0);
                                              cumulative += redan;
                                            }
                                            return cumulative;
                                          });
                                          const tierColors = ["#f59e0b", "#fbbf24", "#fcd34d", "#fde68a", "#fef3c7"];

                                          return (
                                            <g
                                              key={`gabion-${ov.id}-${side}`}
                                              className="cursor-move"
                                              onMouseDown={(e) => {
                                                e.stopPropagation();
                                                setDraggingGabionKey(`${ov.id}:${side}`);
                                                const svgRect = e.currentTarget.ownerSVGElement?.getBoundingClientRect();
                                                if (svgRect) {
                                                  setDragStartPos({
                                                    pointerX: e.clientX - svgRect.left,
                                                    pointerY: e.clientY - svgRect.top,
                                                    initX: gConf.offset || 0,
                                                    initY: 0
                                                  });
                                                }
                                              }}
                                            >
                                              {gConf.tiers.map((t, idx) => {
                                                const perpOffset = 4 + tierPositions[idx] * scale;
                                                let x1 = fX, y1 = fY, x2 = fX, y2 = fY;
                                                if (side === "nord") { x1 = fX + clampedOffset; x2 = x1 + gSpan; y1 = y2 = fY - perpOffset; }
                                                else if (side === "sud") { x1 = fX + clampedOffset; x2 = x1 + gSpan; y1 = y2 = fY + fH + perpOffset; }
                                                else if (side === "ouest") { y1 = fY + clampedOffset; y2 = y1 + gSpan; x1 = x2 = fX - perpOffset; }
                                                else if (side === "est") { y1 = fY + clampedOffset; y2 = y1 + gSpan; x1 = x2 = fX + fW + perpOffset; }
                                                return (
                                                  <line
                                                    key={`gtier-${ov.id}-${side}-${idx}`}
                                                    x1={x1} y1={y1} x2={x2} y2={y2}
                                                    stroke={tierColors[idx % tierColors.length]}
                                                    strokeWidth={Math.max(1, 2.5 - idx * 0.3)}
                                                  />
                                                );
                                              })}
                                              <text
                                                x={side === "nord" || side === "sud" ? fX + clampedOffset + gSpan / 2 : (side === "ouest" ? fX - 8 - tierPositions[tierPositions.length - 1] * scale : fX + fW + 8 + tierPositions[tierPositions.length - 1] * scale)}
                                                y={side === "nord" ? fY - 8 - tierPositions[tierPositions.length - 1] * scale : side === "sud" ? fY + fH + 14 + tierPositions[tierPositions.length - 1] * scale : fY + clampedOffset + gSpan / 2}
                                                fill="#fbbf24"
                                                fontSize="7.5"
                                                fontWeight="bold"
                                                textAnchor="middle"
                                              >
                                                Gabion ({gConf.tiers.length} ét.)
                                              </text>
                                            </g>
                                          );
                                        })}
                                      </g>
                                    )}''',
)


# ---------------------------------------------------------------------------
# STEP 3 — Modal: default shape, side-tab subtitle, and the whole detail
# panel become tier-based (list of étages + live elevation preview),
# replacing the old "Nombre d'Étages" buttons / single width+gap fields.
# ---------------------------------------------------------------------------

do_replace(
    "3. modal: defaultGabionSide becomes tier-based",
    '''                const defaultGabionSide = { enabled: false, etages: 1, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5 };''',
    '''                const defaultGabionSide = { enabled: false, length: 10, offset: 0, tiers: [{ height: 1, depth: 1, redanMode: "fixe" as const, redanValue: 0.3 }] };''',
)

do_replace(
    "4. modal: side-tab subtitle now shows étage count from tiers.length",
    '''                                <span className="text-[9px] font-mono opacity-80">
                                  {conf.enabled ? `${conf.etages} Étage${conf.etages > 1 ? "s" : ""}` : "Inactif"}
                                </span>''',
    '''                                <span className="text-[9px] font-mono opacity-80">
                                  {conf.enabled ? `${(conf.tiers || []).length} Étage${(conf.tiers || []).length > 1 ? "s" : ""}` : "Inactif"}
                                </span>''',
)

GABION_PANEL_OLD = '''                      {/* Active Gabion Side Parameters Panel */}
                      {(() => {
                        const side = activeGabionTab;
                        const conf = sides[side] || defaultGabionSide;

                        const updateConf = (partial: Partial<typeof conf>) => {
                          if (!targetOuvrage) return;
                          setOuvrages(prev => prev.map(o => {
                            if (o.id !== targetOuvrage.id) return o;
                            const currentSides = o.gabionSides || { nord: defaultGabionSide, sud: defaultGabionSide, est: defaultGabionSide, ouest: defaultGabionSide };
                            return {
                              ...o,
                              gabionSides: {
                                ...currentSides,
                                [side]: { ...(currentSides[side] || defaultGabionSide), ...partial }
                              }
                            };
                          }));
                        };

                        return (
                          <div className="bg-amber-50/60 p-4 rounded-2xl border border-amber-300 space-y-4">
                            <div className="flex items-center justify-between border-b border-amber-200 pb-3">
                              <label className="flex items-center gap-2 cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={conf.enabled}
                                  onChange={(e) => updateConf({ enabled: e.target.checked })}
                                  className="rounded text-amber-700 focus:ring-amber-600 w-4 h-4"
                                />
                                <span className="text-xs font-black text-slate-800 uppercase">
                                  Mur Gabion Côté <strong className="text-amber-800 uppercase">{side}</strong>
                                </span>
                              </label>
                              {conf.enabled && (
                                <span className="text-[10px] font-mono bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded">
                                  {conf.length}m x {conf.width}m | {conf.etages} Étage(s)
                                </span>
                              )}
                            </div>

                            {conf.enabled && (
                              <div className="space-y-4">
                                {/* Nombre d'Étages (1 à 4) */}
                                <div>
                                  <label className="text-[10px] font-bold text-slate-600 block mb-1">
                                    Nombre d'Étages de Casiers (Terrain Dénivelé) :
                                  </label>
                                  <div className="grid grid-cols-4 gap-2">
                                    {[1, 2, 3, 4].map((n) => (
                                      <button
                                        key={n}
                                        type="button"
                                        onClick={() => updateConf({ etages: n })}
                                        className={`py-2 text-center text-xs font-black rounded-lg border transition-all ${
                                          conf.etages === n
                                            ? "bg-amber-700 text-white border-amber-700 shadow-xs"
                                            : "bg-white text-slate-700 border-slate-200 hover:bg-amber-100"
                                        }`}
                                      >
                                        {n} Étage{n > 1 ? "s" : ""}
                                      </button>
                                    ))}
                                  </div>
                                </div>

                                {/* Dimensions du mur & Offset */}
                                <div className="grid grid-cols-3 gap-3">
                                  <div>
                                    <label className="text-[10px] font-bold text-slate-600 block mb-1">Longueur du Mur (m) :</label>
                                    <input
                                      type="number"
                                      min="2"
                                      max="100"
                                      step="1"
                                      value={conf.length}
                                      onChange={(e) => updateConf({ length: Math.max(1, parseFloat(e.target.value) || 5) })}
                                      className="w-full text-xs font-mono font-bold bg-white border border-amber-300 rounded-lg px-2.5 py-1.5"
                                    />
                                  </div>
                                  <div>
                                    <label className="text-[10px] font-bold text-slate-600 block mb-1">Largeur Casier (m) :</label>
                                    <input
                                      type="number"
                                      min="0.5"
                                      max="3"
                                      step="0.5"
                                      value={conf.width}
                                      onChange={(e) => updateConf({ width: Math.max(0.5, parseFloat(e.target.value) || 1) })}
                                      className="w-full text-xs font-mono font-bold bg-white border border-amber-300 rounded-lg px-2.5 py-1.5"
                                    />
                                  </div>
                                  <div>
                                    <label className="text-[10px] font-bold text-slate-600 block mb-1">Offset / Distance (m) :</label>
                                    <input
                                      type="number"
                                      min="0"
                                      max="20"
                                      step="0.5"
                                      value={conf.offset}
                                      onChange={(e) => updateConf({ offset: Math.max(0, parseFloat(e.target.value) || 0) })}
                                      className="w-full text-xs font-mono font-bold bg-white border border-amber-300 rounded-lg px-2.5 py-1.5"
                                    />
                                  </div>
                                </div>

                                {/* Espace entre casiers & angles (Non jointifs) */}
                                <div className="p-3 bg-white rounded-xl border border-amber-200 space-y-1">
                                  <label className="text-[10px] font-black text-amber-900 block">
                                    Espacement Inter-Casiers & Angles (Terrain en Dénivelé - Non Jointifs) :
                                  </label>
                                  <div className="flex items-center gap-3">
                                    <input
                                      type="range"
                                      min="0.2"
                                      max="2.0"
                                      step="0.1"
                                      value={conf.gap}
                                      onChange={(e) => updateConf({ gap: Math.max(0.1, parseFloat(e.target.value) || 0.4) })}
                                      className="w-full accent-amber-600"
                                    />
                                    <span className="font-mono font-bold text-xs bg-amber-100 text-amber-900 px-2 py-1 rounded">
                                      {conf.gap} m
                                    </span>
                                  </div>
                                  <p className="text-[9px] text-slate-500">
                                    L'espace libre évite le chevauchement aux angles et garantit la stabilité sur terrain pente.
                                  </p>
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })()}'''

GABION_PANEL_NEW = '''                      {/* Active Gabion Side Parameters Panel — étages paramétriques individuels */}
                      {(() => {
                        const side = activeGabionTab;
                        const conf = sides[side] || defaultGabionSide;
                        const tiers = conf.tiers || [];

                        const updateConf = (partial: Partial<typeof conf>) => {
                          if (!targetOuvrage) return;
                          setOuvrages(prev => prev.map(o => {
                            if (o.id !== targetOuvrage.id) return o;
                            const currentSides = o.gabionSides || { nord: defaultGabionSide, sud: defaultGabionSide, est: defaultGabionSide, ouest: defaultGabionSide };
                            return {
                              ...o,
                              gabionSides: {
                                ...currentSides,
                                [side]: { ...(currentSides[side] || defaultGabionSide), ...partial }
                              }
                            };
                          }));
                        };

                        const updateTier = (idx: number, partial: any) => {
                          const newTiers = tiers.map((t, i) => i === idx ? { ...t, ...partial } : t);
                          updateConf({ tiers: newTiers } as any);
                        };
                        const addTier = () => {
                          updateConf({ tiers: [...tiers, { height: 0.8, depth: 0.8, redanMode: "fixe", redanValue: 0.3 }] } as any);
                        };
                        const removeTier = (idx: number) => {
                          updateConf({ tiers: tiers.filter((_, i) => i !== idx) } as any);
                        };

                        const totalHeight = tiers.reduce((s, t) => s + (t.height || 0), 0);

                        return (
                          <div className="bg-amber-50/60 p-4 rounded-2xl border border-amber-300 space-y-4">
                            <div className="flex items-center justify-between border-b border-amber-200 pb-3">
                              <label className="flex items-center gap-2 cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={conf.enabled}
                                  onChange={(e) => updateConf({ enabled: e.target.checked })}
                                  className="rounded text-amber-700 focus:ring-amber-600 w-4 h-4"
                                />
                                <span className="text-xs font-black text-slate-800 uppercase">
                                  Mur Gabion Côté <strong className="text-amber-800 uppercase">{side}</strong>
                                </span>
                              </label>
                              {conf.enabled && (
                                <span className="text-[10px] font-mono bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded">
                                  {conf.length}m | {tiers.length} Étage(s) | H≈{totalHeight.toFixed(2)}m
                                </span>
                              )}
                            </div>

                            {conf.enabled && (
                              <div className="space-y-4">
                                <div className="grid grid-cols-2 gap-3">
                                  <div>
                                    <label className="text-[10px] font-bold text-slate-600 block mb-1">Longueur du Mur (m) :</label>
                                    <input
                                      type="number"
                                      min="2"
                                      max="100"
                                      step="1"
                                      value={conf.length}
                                      onChange={(e) => updateConf({ length: Math.max(1, parseFloat(e.target.value) || 5) })}
                                      className="w-full text-xs font-mono font-bold bg-white border border-amber-300 rounded-lg px-2.5 py-1.5"
                                    />
                                  </div>
                                  <div>
                                    <label className="text-[10px] font-bold text-slate-600 block mb-1">Position le long du mur, depuis le coin (m) :</label>
                                    <input
                                      type="number"
                                      min="0"
                                      max="20"
                                      step="0.5"
                                      value={conf.offset}
                                      onChange={(e) => updateConf({ offset: Math.max(0, parseFloat(e.target.value) || 0) })}
                                      className="w-full text-xs font-mono font-bold bg-white border border-amber-300 rounded-lg px-2.5 py-1.5"
                                    />
                                  </div>
                                </div>

                                {/* Aperçu élévation (coupe) */}
                                <div className="bg-slate-950 rounded-xl p-3 border border-slate-700">
                                  <span className="text-[10px] font-black text-slate-400 uppercase block mb-2">Aperçu Élévation (Coupe)</span>
                                  <svg viewBox="0 0 400 220" className="w-full h-auto bg-slate-900 rounded">
                                    {tiers.length === 0 ? (
                                      <text x="200" y="110" fill="#64748b" fontSize="11" textAnchor="middle">Aucun étage configuré</text>
                                    ) : (() => {
                                      const PX_PER_M = 40;
                                      let cumH = 0, cumD = 0;
                                      const rects = tiers.map((t, idx) => {
                                        const h = (t.height || 0.5) * PX_PER_M;
                                        const d = (t.depth || 0.5) * PX_PER_M;
                                        if (idx > 0) {
                                          const prevDepth = tiers[idx - 1].depth || 1;
                                          const redanM = t.redanMode === "pourcentage" ? (prevDepth * (t.redanValue || 0)) / 100 : (t.redanValue || 0);
                                          cumD += redanM * PX_PER_M;
                                        }
                                        const y = 190 - cumH - h;
                                        const x = 30 + cumD;
                                        cumH += h;
                                        const color = idx % 2 === 0 ? "#92400e" : "#b45309";
                                        return (
                                          <g key={idx}>
                                            <rect x={x} y={y} width={d} height={h} fill={color} stroke="#f59e0b" strokeWidth="1.5" />
                                            <text x={x + d / 2} y={y + h / 2 + 3} fill="#fef3c7" fontSize="8" fontWeight="bold" textAnchor="middle">Ét.{idx + 1}</text>
                                          </g>
                                        );
                                      });
                                      return (
                                        <>
                                          <line x1="10" y1="190" x2="390" y2="190" stroke="#475569" strokeWidth="1.5" strokeDasharray="4 3" />
                                          {rects}
                                          <text x="200" y="210" fill="#64748b" fontSize="9" textAnchor="middle">Hauteur totale ≈ {totalHeight.toFixed(2)} m</text>
                                        </>
                                      );
                                    })()}
                                  </svg>
                                </div>

                                {/* Liste des étages */}
                                <div className="space-y-2">
                                  <div className="flex items-center justify-between">
                                    <label className="text-[10px] font-black text-slate-600 uppercase">Étages ({tiers.length}) :</label>
                                    <button type="button" onClick={addTier} className="text-[10px] font-bold text-amber-700 underline">+ Ajouter un étage</button>
                                  </div>
                                  {tiers.map((t, idx) => (
                                    <div key={idx} className="bg-white p-2.5 rounded-lg border border-amber-200 space-y-2">
                                      <div className="flex items-center justify-between">
                                        <span className="text-[10px] font-black text-amber-800">Étage {idx + 1} {idx === 0 ? "(base)" : ""}</span>
                                        {tiers.length > 1 && (
                                          <button type="button" onClick={() => removeTier(idx)} className="text-red-500 hover:text-red-700">
                                            <Trash2 className="w-3.5 h-3.5" />
                                          </button>
                                        )}
                                      </div>
                                      <div className="grid grid-cols-2 gap-2">
                                        <div>
                                          <label className="text-[9px] font-bold text-slate-500 block">Hauteur (m) :</label>
                                          <input
                                            type="number" min="0.2" step="0.1" value={t.height}
                                            onChange={(e) => updateTier(idx, { height: Math.max(0.2, parseFloat(e.target.value) || 0.5) })}
                                            className="w-full text-xs font-mono font-bold bg-slate-50 border border-slate-300 rounded px-2 py-1"
                                          />
                                        </div>
                                        <div>
                                          <label className="text-[9px] font-bold text-slate-500 block">Profondeur (m) :</label>
                                          <input
                                            type="number" min="0.3" step="0.1" value={t.depth}
                                            onChange={(e) => updateTier(idx, { depth: Math.max(0.3, parseFloat(e.target.value) || 0.5) })}
                                            className="w-full text-xs font-mono font-bold bg-slate-50 border border-slate-300 rounded px-2 py-1"
                                          />
                                        </div>
                                      </div>
                                      {idx > 0 && (
                                        <div className="grid grid-cols-2 gap-2 pt-1 border-t border-amber-100">
                                          <div>
                                            <label className="text-[9px] font-bold text-slate-500 block">Mode du retrait :</label>
                                            <select
                                              value={t.redanMode}
                                              onChange={(e) => updateTier(idx, { redanMode: e.target.value })}
                                              className="w-full text-xs font-bold bg-slate-50 border border-slate-300 rounded px-2 py-1"
                                            >
                                              <option value="fixe">Fixe (m)</option>
                                              <option value="pourcentage">% de la profondeur du dessous</option>
                                            </select>
                                          </div>
                                          <div>
                                            <label className="text-[9px] font-bold text-slate-500 block">{t.redanMode === "pourcentage" ? "Retrait (%) :" : "Retrait (m) :"}</label>
                                            <input
                                              type="number" min="0" step={t.redanMode === "pourcentage" ? "5" : "0.1"} value={t.redanValue}
                                              onChange={(e) => updateTier(idx, { redanValue: Math.max(0, parseFloat(e.target.value) || 0) })}
                                              className="w-full text-xs font-mono font-bold bg-slate-50 border border-slate-300 rounded px-2 py-1"
                                            />
                                          </div>
                                        </div>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })()}'''

do_replace("5. rewrite the gabion side detail panel to a tier list + elevation preview", GABION_PANEL_OLD, GABION_PANEL_NEW)


# ---------------------------------------------------------------------------
# STEP 4 — Keep the drag fallback shape consistent (drag only reads/writes
# `.offset`, so this is cosmetic/type-consistency, not a functional fix).
# ---------------------------------------------------------------------------

do_replace(
    "6. drag handler: fallback default shape for gabion sides becomes tier-based",
    '''                            const defaultSide = { enabled: false, etages: 1, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5 };''',
    '''                            const defaultSide = { enabled: false, length: 10, offset: 0, tiers: [{ height: 1, depth: 1, redanMode: "fixe", redanValue: 0 }] };''',
)

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Applied {len(applied)}/{len(applied) + len(skipped)} patches:")
for a in applied:
    print(f"  OK   - {a}")
for s in skipped:
    print(f"  SKIP - {s}  (anchor not found — file may already differ; check manually)")

if skipped:
    sys.exit(1)
