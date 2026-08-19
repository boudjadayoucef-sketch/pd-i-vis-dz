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
# STEP 0 — New state: which ouvrage the Voile Designer targets.
# ---------------------------------------------------------------------------

do_replace(
    "0. add activeVoileOuvrageId state",
    '''  const [activeGabionOuvrageId, setActiveGabionOuvrageId] = useState<string | null>(null);''',
    '''  const [activeGabionOuvrageId, setActiveGabionOuvrageId] = useState<string | null>(null);
  const [activeVoileOuvrageId, setActiveVoileOuvrageId] = useState<string | null>(null);''',
)

# ---------------------------------------------------------------------------
# STEP 1 — Retarget the "Saisir Voile" button to default to the selected
# ouvrage before opening the modal.
# ---------------------------------------------------------------------------

do_replace(
    "1. retarget the Saisir Voile button",
    '''                <button
                  type="button"
                  onClick={() => setActiveCadModal("voile")}
                  className="w-full py-1.5 px-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Saisir Voile ⚙️</span>
                </button>''',
    '''                <button
                  type="button"
                  onClick={() => {
                    setActiveVoileOuvrageId(selectedOuvrageId || ouvrages[0]?.id || null);
                    setActiveCadModal("voile");
                  }}
                  className="w-full py-1.5 px-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Saisir Voile ⚙️</span>
                </button>''',
)

# ---------------------------------------------------------------------------
# STEP 2 — Rewrite the Voile modal body to edit the target ouvrage's own
# hasVoile / voileSides / voileHeight / voileThickness (these fields already
# existed on OuvrageBlock, they just had no UI wired to them).
# ---------------------------------------------------------------------------

VOILE_MODAL_OLD = '''              {/* 5. VOILE CAD MODAL */}
              {activeCadModal === "voile" && (
                <div className="space-y-4">
                  <label className="flex items-center gap-2 cursor-pointer bg-indigo-50 p-3 rounded-xl border border-indigo-200">
                    <input
                      type="checkbox"
                      checked={hasVoilePeripherique}
                      onChange={(e) => setHasVoilePeripherique(e.target.checked)}
                      className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4"
                    />
                    <span className="text-xs font-black text-indigo-950 uppercase">
                      Activer le Voile Périmétrique en Béton Armé
                    </span>
                  </label>

                  {hasVoilePeripherique && (
                    <div className="space-y-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <label className="text-[10px] font-black text-slate-600 uppercase">Côtés du Voile :</label>
                          <button
                            type="button"
                            onClick={() => setVoileSides(["nord", "sud", "est", "ouest"])}
                            className="text-[10px] font-bold text-indigo-600 underline"
                          >
                            Tous les 4 côtés
                          </button>
                        </div>
                        <div className="grid grid-cols-4 gap-2">
                          {(["nord", "sud", "est", "ouest"] as const).map((s) => {
                            const active = voileSides.includes(s);
                            return (
                              <button
                                key={s}
                                type="button"
                                onClick={() => {
                                  setVoileSides(prev => active ? prev.filter(x => x !== s) : [...prev, s]);
                                }}
                                className={`py-2 text-center font-extrabold capitalize rounded-lg border text-xs transition-all ${
                                  active ? "bg-indigo-600 text-white border-indigo-600" : "bg-white text-slate-700 border-slate-200"
                                }`}
                              >
                                {s} {active ? "✓" : ""}
                              </button>
                            );
                          })}
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-[10px] font-bold text-slate-600 block mb-1">Hauteur Voile (m) :</label>
                          <input
                            type="number"
                            value={voileHeight}
                            onChange={(e) => setVoileHeight(parseFloat(e.target.value) || 2.5)}
                            className="w-full text-xs font-mono font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                          />
                        </div>
                        <div>
                          <label className="text-[10px] font-bold text-slate-600 block mb-1">Épaisseur Voile (m) :</label>
                          <input
                            type="number"
                            value={voileThickness}
                            onChange={(e) => setVoileThickness(parseFloat(e.target.value) || 0.2)}
                            className="w-full text-xs font-mono font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}'''

VOILE_MODAL_NEW = '''              {/* 5. VOILE CAD MODAL (par ouvrage / bloc cible) */}
              {activeCadModal === "voile" && (() => {
                const targetOuvrage = ouvrages.find(o => o.id === activeVoileOuvrageId) || ouvrages[0];
                const tSides = targetOuvrage?.voileSides || [];

                return (
                <div className="space-y-4">
                  <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5">
                    <label className="text-[10px] font-black text-slate-500 uppercase block">Ouvrage / Bloc Cible :</label>
                    <select
                      value={targetOuvrage?.id || ""}
                      onChange={(e) => setActiveVoileOuvrageId(e.target.value)}
                      className="w-full font-bold text-sm bg-white border border-slate-300 rounded-xl px-3 py-2"
                    >
                      {ouvrages.map((o) => (
                        <option key={o.id} value={o.id}>{o.name}</option>
                      ))}
                    </select>
                  </div>

                  <label className="flex items-center gap-2 cursor-pointer bg-indigo-50 p-3 rounded-xl border border-indigo-200">
                    <input
                      type="checkbox"
                      checked={!!targetOuvrage?.hasVoile}
                      onChange={(e) => targetOuvrage && handleUpdateOuvrage(targetOuvrage.id, "hasVoile", e.target.checked)}
                      className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4"
                    />
                    <span className="text-xs font-black text-indigo-950 uppercase">
                      Activer le Voile Périmétrique en Béton Armé
                    </span>
                  </label>

                  {targetOuvrage?.hasVoile && (
                    <div className="space-y-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <label className="text-[10px] font-black text-slate-600 uppercase">Côtés du Voile :</label>
                          <button
                            type="button"
                            onClick={() => targetOuvrage && handleUpdateOuvrage(targetOuvrage.id, "voileSides", ["nord", "sud", "est", "ouest"])}
                            className="text-[10px] font-bold text-indigo-600 underline"
                          >
                            Tous les 4 côtés
                          </button>
                        </div>
                        <div className="grid grid-cols-4 gap-2">
                          {(["nord", "sud", "est", "ouest"] as const).map((s) => {
                            const active = tSides.includes(s);
                            return (
                              <button
                                key={s}
                                type="button"
                                onClick={() => {
                                  if (!targetOuvrage) return;
                                  const next = active ? tSides.filter(x => x !== s) : [...tSides, s];
                                  handleUpdateOuvrage(targetOuvrage.id, "voileSides", next);
                                }}
                                className={`py-2 text-center font-extrabold capitalize rounded-lg border text-xs transition-all ${
                                  active ? "bg-indigo-600 text-white border-indigo-600" : "bg-white text-slate-700 border-slate-200"
                                }`}
                              >
                                {s} {active ? "✓" : ""}
                              </button>
                            );
                          })}
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-[10px] font-bold text-slate-600 block mb-1">Hauteur Voile (m) :</label>
                          <input
                            type="number"
                            value={targetOuvrage?.voileHeight ?? 2.5}
                            onChange={(e) => targetOuvrage && handleUpdateOuvrage(targetOuvrage.id, "voileHeight", parseFloat(e.target.value) || 2.5)}
                            className="w-full text-xs font-mono font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                          />
                        </div>
                        <div>
                          <label className="text-[10px] font-bold text-slate-600 block mb-1">Épaisseur Voile (m) :</label>
                          <input
                            type="number"
                            value={targetOuvrage?.voileThickness ?? 0.2}
                            onChange={(e) => targetOuvrage && handleUpdateOuvrage(targetOuvrage.id, "voileThickness", parseFloat(e.target.value) || 0.2)}
                            className="w-full text-xs font-mono font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                );
              })()}'''

do_replace("2. rewrite the Voile modal body to be per-ouvrage", VOILE_MODAL_OLD, VOILE_MODAL_NEW)

# ---------------------------------------------------------------------------
# STEP 3 — Render voile per selected side (and thickness), instead of always
# drawing a generic dashed border around the whole perimeter.
# ---------------------------------------------------------------------------

do_replace(
    "3. render voile per side, using voileSides/voileThickness",
    '''                                    {/* Voile Béton Armé Périmétrique */}
                                    {ov.hasVoile && (
                                      <rect
                                        x={fX - 3}
                                        y={fY - 3}
                                        width={fW + 6}
                                        height={fH + 6}
                                        fill="none"
                                        stroke="#0ea5e9"
                                        strokeWidth="2.5"
                                        strokeDasharray="2 2"
                                      />
                                    )}''',
    '''                                    {/* Voile Béton Armé Périmétrique (par côté sélectionné) */}
                                    {ov.hasVoile && ov.voileSides && ov.voileSides.length > 0 && (
                                      <g>
                                        {ov.voileSides.map((side) => {
                                          const vThick = Math.max(2, (ov.voileThickness || 0.2) * scale);
                                          let vx = fX, vy = fY, vw = fW, vh = fH;
                                          if (side === "nord") { vy = fY - vThick; vh = vThick; }
                                          else if (side === "sud") { vy = fY + fH; vh = vThick; }
                                          else if (side === "ouest") { vx = fX - vThick; vw = vThick; }
                                          else if (side === "est") { vx = fX + fW; vw = vThick; }
                                          return (
                                            <rect
                                              key={`voile-${ov.id}-${side}`}
                                              x={vx}
                                              y={vy}
                                              width={vw}
                                              height={vh}
                                              fill="#0ea5e9"
                                              fillOpacity="0.35"
                                              stroke="#0ea5e9"
                                              strokeWidth="1.5"
                                            />
                                          );
                                        })}
                                      </g>
                                    )}''',
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
