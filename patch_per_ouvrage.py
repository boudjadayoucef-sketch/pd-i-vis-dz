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
# STEP 0 — New state: which ouvrage the Gabion Designer targets.
# ---------------------------------------------------------------------------

do_replace(
    "0. add activeGabionOuvrageId state",
    '''  const [activeGabionTab, setActiveGabionTab] = useState<"nord" | "sud" | "est" | "ouest">("nord");''',
    '''  const [activeGabionTab, setActiveGabionTab] = useState<"nord" | "sud" | "est" | "ouest">("nord");
  const [activeGabionOuvrageId, setActiveGabionOuvrageId] = useState<string | null>(null);''',
)


# ---------------------------------------------------------------------------
# STEP 1 — Gates: tag each gate with the ouvrage it belongs to.
# ---------------------------------------------------------------------------

do_replace(
    "1. initial gates: tag default gates with ouvrageId",
    '''  const [gates, setGates] = useState<ParametricGate[]>([
    {
      id: "gate-1",
      name: "Portail Véhicules Principal",
      type: "portail_5m",
      wall: "sud",
      offset: 5,
      width: 5,
      height: 2.8
    },
    {
      id: "gate-2",
      name: "Portillon Piéton",
      type: "portillon",
      wall: "sud",
      offset: 15,
      width: 1,
      height: 2.8
    }
  ]);''',
    '''  const [gates, setGates] = useState<ParametricGate[]>([
    {
      id: "gate-1",
      name: "Portail Véhicules Principal",
      type: "portail_5m",
      wall: "sud",
      offset: 5,
      width: 5,
      height: 2.8,
      ouvrageId: "ouvrage-1"
    },
    {
      id: "gate-2",
      name: "Portillon Piéton",
      type: "portillon",
      wall: "sud",
      offset: 15,
      width: 1,
      height: 2.8,
      ouvrageId: "ouvrage-1"
    }
  ]);''',
)

do_replace(
    "2. handleAddGate: default the new gate to the selected ouvrage, size it off that ouvrage's own dimensions",
    '''  const handleAddGate = (type: "portail_5m" | "portail_custom" | "portillon" = "portail_5m") => {
    const newId = "gate-" + Date.now();
    const width = type === "portail_5m" ? 5 : type === "portillon" ? 1 : 4;
    const name = type === "portillon" ? `Portillon Piéton ${gates.length + 1}` : `Portail Véhicules ${gates.length + 1}`;
    setGates(prev => [
      ...prev,
      {
        id: newId,
        name,
        type,
        wall: "sud",
        offset: Math.min(2 + prev.length * 3, Math.max(0, fenceA - width)),
        width,
        height: fenceHeight
      }
    ]);
    setSelectedGateId(newId);
  };''',
    '''  const handleAddGate = (type: "portail_5m" | "portail_custom" | "portillon" = "portail_5m", targetOuvrageId?: string) => {
    const newId = "gate-" + Date.now();
    const width = type === "portail_5m" ? 5 : type === "portillon" ? 1 : 4;
    const ouvrageId = targetOuvrageId || selectedOuvrageId || ouvrages[0]?.id || "ouvrage-1";
    const targetOv = ouvrages.find(o => o.id === ouvrageId);
    const wallLen = targetOv ? targetOv.length : fenceA;
    const gateHeight = targetOv ? targetOv.fenceHeight : fenceHeight;
    const existingOnOuvrage = gates.filter(g => g.ouvrageId === ouvrageId).length;
    const name = type === "portillon" ? `Portillon Piéton ${existingOnOuvrage + 1}` : `Portail Véhicules ${existingOnOuvrage + 1}`;
    setGates(prev => [
      ...prev,
      {
        id: newId,
        name,
        type,
        wall: "sud",
        offset: Math.min(2 + existingOnOuvrage * 3, Math.max(0, wallLen - width)),
        width,
        height: gateHeight,
        ouvrageId
      }
    ]);
    setSelectedGateId(newId);
  };''',
)

do_replace(
    "3. handleUpdateGate: clamp offset against the gate's OWN ouvrage, not the global fence",
    '''  const handleUpdateGate = (id: string, field: keyof ParametricGate, value: any) => {
    setGates(prev => prev.map(g => {
      if (g.id !== id) return g;
      const updated = { ...g, [field]: value };
      if (field === "wall") {
        const maxWallLen = (value === "sud" || value === "nord") ? fenceA : fenceB;
        updated.offset = Math.min(Math.max(0, maxWallLen - updated.width), updated.offset);
      }
      return updated;
    }));
  };''',
    '''  const handleUpdateGate = (id: string, field: keyof ParametricGate, value: any) => {
    setGates(prev => prev.map(g => {
      if (g.id !== id) return g;
      const updated = { ...g, [field]: value };
      if (field === "wall" || field === "ouvrageId") {
        const targetOv = ouvrages.find(o => o.id === updated.ouvrageId) || ouvrages[0];
        const maxWallLen = (updated.wall === "sud" || updated.wall === "nord") ? (targetOv?.length ?? fenceA) : (targetOv?.width ?? fenceB);
        updated.offset = Math.min(Math.max(0, maxWallLen - updated.width), updated.offset);
      }
      return updated;
    }));
  };''',
)

do_replace(
    "4. gates render: look up the gate's own ouvrage instead of ouvrages[0]",
    '''                              {gates.map((g) => {
                                const isSelected = selectedGateId === g.id;
                                const isSmall = g.type === "portillon";
                                const mainOv = ouvrages[0] || { length: 35, width: 21, xOffset: 0, yOffset: 0 };
                                const ovW = mainOv.length * scale;
                                const ovH = mainOv.width * scale;
                                const ovX = cX + (mainOv.xOffset * scale) - (ovW / 2);
                                const ovY = cY + (mainOv.yOffset * scale) - (ovH / 2);''',
    '''                              {gates.map((g) => {
                                const isSelected = selectedGateId === g.id;
                                const isSmall = g.type === "portillon";
                                const mainOv = ouvrages.find(o => o.id === g.ouvrageId) || ouvrages[0] || { length: 35, width: 21, xOffset: 0, yOffset: 0 };
                                const ovW = mainOv.length * scale;
                                const ovH = mainOv.width * scale;
                                const ovX = cX + (mainOv.xOffset * scale) - (ovW / 2);
                                const ovY = cY + (mainOv.yOffset * scale) - (ovH / 2);''',
)

do_replace(
    "5. gates modal: add an Ouvrage selector per gate row",
    '''                      <div key={g.id} className="bg-slate-50 p-3 rounded-xl border border-slate-200 flex items-center justify-between gap-3 text-xs">
                        <div className="grid grid-cols-3 gap-2 flex-1">
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Type d'Accès :</label>''',
    '''                      <div key={g.id} className="bg-slate-50 p-3 rounded-xl border border-slate-200 flex items-center justify-between gap-3 text-xs">
                        <div className="grid grid-cols-4 gap-2 flex-1">
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Ouvrage :</label>
                            <select
                              value={g.ouvrageId || ouvrages[0]?.id || ""}
                              onChange={(e) => handleUpdateGate(g.id, "ouvrageId", e.target.value)}
                              className="w-full font-bold bg-white border border-slate-300 rounded px-2 py-1 text-xs"
                            >
                              {ouvrages.map((o) => (
                                <option key={o.id} value={o.id}>{o.name}</option>
                              ))}
                            </select>
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Type d'Accès :</label>''',
)


# ---------------------------------------------------------------------------
# STEP 2 — Gabions: retarget the two modal-opening buttons, and rewrite the
# modal body to edit the SELECTED ouvrage's own gabionSides instead of the
# global (ouvrage[0]-only) gabionSideConfigs.
# ---------------------------------------------------------------------------

do_replace(
    "6. toolbar quick-add button: default gabion target to the selected ouvrage",
    '''                <button
                  type="button"
                  onClick={() => setActiveCadModal("gabions")}
                  className="px-3 py-1.5 bg-amber-700 hover:bg-amber-600 text-white rounded-xl text-xs font-black transition-all flex items-center gap-1.5 shadow-sm cursor-pointer"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>+ Murs de Gabions</span>
                </button>''',
    '''                <button
                  type="button"
                  onClick={() => {
                    setActiveGabionOuvrageId(selectedOuvrageId || ouvrages[0]?.id || null);
                    setActiveCadModal("gabions");
                  }}
                  className="px-3 py-1.5 bg-amber-700 hover:bg-amber-600 text-white rounded-xl text-xs font-black transition-all flex items-center gap-1.5 shadow-sm cursor-pointer"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>+ Murs de Gabions</span>
                </button>''',
)

do_replace(
    "7. card button: default gabion target to the selected ouvrage",
    '''                <button
                  type="button"
                  onClick={() => setActiveCadModal("gabions")}
                  className="w-full py-1.5 px-2 bg-amber-700 hover:bg-amber-600 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Designer Gabions ⚙️</span>
                </button>''',
    '''                <button
                  type="button"
                  onClick={() => {
                    setActiveGabionOuvrageId(selectedOuvrageId || ouvrages[0]?.id || null);
                    setActiveCadModal("gabions");
                  }}
                  className="w-full py-1.5 px-2 bg-amber-700 hover:bg-amber-600 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Designer Gabions ⚙️</span>
                </button>''',
)

GABIONS_MODAL_OLD = '''              {/* 1. GABIONS CAD MODAL */}
              {activeCadModal === "gabions" && (
                <div className="space-y-5">
                  <div className="flex items-center justify-between bg-amber-50 p-3 rounded-xl border border-amber-200">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={hasGabions}
                        onChange={(e) => setHasGabions(e.target.checked)}
                        className="rounded text-amber-700 focus:ring-amber-600 w-4 h-4"
                      />
                      <span className="text-xs font-black text-amber-950 uppercase tracking-wider">
                        Activer la Protection par Murs en Gabions (Terrain Dénivelé)
                      </span>
                    </label>
                  </div>

                  {hasGabions && (
                    <div className="space-y-4">
                      {/* Side Tabs Selector */}
                      <div className="space-y-1">
                        <label className="text-[10px] font-black text-slate-500 uppercase block">Côté du Mur à Configurer :</label>
                        <div className="grid grid-cols-4 gap-2">
                          {(["nord", "sud", "est", "ouest"] as const).map((side) => {
                            const conf = gabionSideConfigs[side];
                            const isTabActive = activeGabionTab === side;
                            return (
                              <button
                                key={side}
                                type="button"
                                onClick={() => setActiveGabionTab(side)}
                                className={`py-2 px-3 rounded-xl font-black text-xs capitalize flex flex-col items-center justify-center border transition-all ${
                                  isTabActive
                                    ? "bg-amber-600 text-white border-amber-600 shadow-md scale-[1.02]"
                                    : conf.enabled
                                    ? "bg-amber-50 text-amber-900 border-amber-200 hover:bg-amber-100"
                                    : "bg-slate-100 text-slate-400 border-slate-200 hover:bg-slate-200"
                                }`}
                              >
                                <span className="uppercase">{side}</span>
                                <span className="text-[9px] font-mono opacity-80">
                                  {conf.enabled ? `${conf.etages} Étage${conf.etages > 1 ? "s" : ""}` : "Inactif"}
                                </span>
                              </button>
                            );
                          })}
                        </div>
                      </div>

                      {/* Active Gabion Side Parameters Panel */}
                      {(() => {
                        const side = activeGabionTab;
                        const conf = gabionSideConfigs[side];

                        const updateConf = (partial: Partial<typeof conf>) => {
                          setGabionSideConfigs((prev) => ({
                            ...prev,
                            [side]: { ...prev[side], ...partial }
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
                      })()}
                    </div>
                  )}
                </div>
              )}'''

GABIONS_MODAL_NEW = '''              {/* 1. GABIONS CAD MODAL (par ouvrage / bloc cible) */}
              {activeCadModal === "gabions" && (() => {
                const defaultGabionSide = { enabled: false, etages: 1, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5 };
                const targetOuvrage = ouvrages.find(o => o.id === activeGabionOuvrageId) || ouvrages[0];
                const sides = targetOuvrage?.gabionSides || {
                  nord: defaultGabionSide, sud: defaultGabionSide, est: defaultGabionSide, ouest: defaultGabionSide
                };

                return (
                <div className="space-y-5">
                  <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5">
                    <label className="text-[10px] font-black text-slate-500 uppercase block">Ouvrage / Bloc Cible :</label>
                    <select
                      value={targetOuvrage?.id || ""}
                      onChange={(e) => setActiveGabionOuvrageId(e.target.value)}
                      className="w-full font-bold text-sm bg-white border border-slate-300 rounded-xl px-3 py-2"
                    >
                      {ouvrages.map((o) => (
                        <option key={o.id} value={o.id}>{o.name}</option>
                      ))}
                    </select>
                  </div>

                  <div className="flex items-center justify-between bg-amber-50 p-3 rounded-xl border border-amber-200">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={!!targetOuvrage?.hasGabions}
                        onChange={(e) => targetOuvrage && handleUpdateOuvrage(targetOuvrage.id, "hasGabions", e.target.checked)}
                        className="rounded text-amber-700 focus:ring-amber-600 w-4 h-4"
                      />
                      <span className="text-xs font-black text-amber-950 uppercase tracking-wider">
                        Activer la Protection par Murs en Gabions (Terrain Dénivelé)
                      </span>
                    </label>
                  </div>

                  {targetOuvrage?.hasGabions && (
                    <div className="space-y-4">
                      {/* Side Tabs Selector */}
                      <div className="space-y-1">
                        <label className="text-[10px] font-black text-slate-500 uppercase block">Côté du Mur à Configurer :</label>
                        <div className="grid grid-cols-4 gap-2">
                          {(["nord", "sud", "est", "ouest"] as const).map((side) => {
                            const conf = sides[side] || defaultGabionSide;
                            const isTabActive = activeGabionTab === side;
                            return (
                              <button
                                key={side}
                                type="button"
                                onClick={() => setActiveGabionTab(side)}
                                className={`py-2 px-3 rounded-xl font-black text-xs capitalize flex flex-col items-center justify-center border transition-all ${
                                  isTabActive
                                    ? "bg-amber-600 text-white border-amber-600 shadow-md scale-[1.02]"
                                    : conf.enabled
                                    ? "bg-amber-50 text-amber-900 border-amber-200 hover:bg-amber-100"
                                    : "bg-slate-100 text-slate-400 border-slate-200 hover:bg-slate-200"
                                }`}
                              >
                                <span className="uppercase">{side}</span>
                                <span className="text-[9px] font-mono opacity-80">
                                  {conf.enabled ? `${conf.etages} Étage${conf.etages > 1 ? "s" : ""}` : "Inactif"}
                                </span>
                              </button>
                            );
                          })}
                        </div>
                      </div>

                      {/* Active Gabion Side Parameters Panel */}
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
                      })()}
                    </div>
                  )}
                </div>
                );
              })()}'''

do_replace("8. rewrite the Gabions modal body to be per-ouvrage", GABIONS_MODAL_OLD, GABIONS_MODAL_NEW)

do_replace(
    "9. remove the global (ouvrage[0]-only) gabion render, per-ouvrage rendering already exists inside ouvrages.map",
    '''                              {/* ==================== RENDERING PARAMETRIC GLOBAL GABIONS ==================== */}
                              {hasGabions && (
                                <g>
                                  {(["nord", "sud", "est", "ouest"] as const).map((side) => {
                                    const gConf = gabionSideConfigs[side];
                                    if (!gConf || !gConf.enabled) return null;

                                    const mainOv = ouvrages[0] || { length: 35, width: 21, xOffset: 0, yOffset: 0 };
                                    const ovW = mainOv.length * scale;
                                    const ovH = mainOv.width * scale;
                                    const ovX = cX + (mainOv.xOffset * scale) - (ovW / 2);
                                    const ovY = cY + (mainOv.yOffset * scale) - (ovH / 2);

                                    const gDepth = (gConf.width || 1) * scale;
                                    const gLen = Math.min(side === "nord" || side === "sud" ? ovW : ovH, (gConf.length || 10) * scale);
                                    let gx = ovX, gy = ovY, gw = ovW, gh = ovH;

                                    if (side === "nord") { gy = ovY - gDepth - (gConf.offset * scale || 4); gh = gDepth; gw = gLen; }
                                    else if (side === "sud") { gy = ovY + ovH + (gConf.offset * scale || 4); gh = gDepth; gw = gLen; }
                                    else if (side === "ouest") { gx = ovX - gDepth - (gConf.offset * scale || 4); gw = gDepth; gh = gLen; }
                                    else if (side === "est") { gx = ovX + ovW + (gConf.offset * scale || 4); gw = gDepth; gh = gLen; }

                                    return (
                                      <g key={`global-gabion-${side}`}>
                                        <rect
                                          x={gx}
                                          y={gy}
                                          width={gw}
                                          height={gh}
                                          fill="url(#hatchGabion)"
                                          stroke="#f59e0b"
                                          strokeWidth="1.5"
                                          rx="2"
                                        />
                                        <text
                                          x={gx + gw / 2}
                                          y={gy + gh / 2 + 3}
                                          fill="#fbbf24"
                                          fontSize="8.5"
                                          fontWeight="black"
                                          textAnchor="middle"
                                        >
                                          Mur Gabion {side.toUpperCase()} ({gConf.etages} ET)
                                        </text>
                                      </g>
                                    );
                                  })}
                                </g>
                              )}''',
    '''                              {/* Gabions are rendered per-ouvrage above, inside the ouvrages.map loop
                                  (see "Gabions Protection Walls around Ouvrage" — ov.hasGabions / ov.gabionSides).
                                  The old global hasGabions/gabionSideConfigs (ouvrage[0]-only) is no longer rendered. */}''',
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
