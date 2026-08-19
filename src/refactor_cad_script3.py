with open("src/components/Calculators.tsx", "r") as f:
    code = f.read()

# Replace Card 3 in left menu
old_card_3 = '''                      {/* 3. Carte Extension L Génie Civil */}
                      <div className="bg-white p-3 rounded-xl border border-slate-200 hover:border-amber-400 transition-all shadow-2xs space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-[11px] font-black text-slate-800 uppercase flex items-center gap-1.5">
                            <Square className="w-4 h-4 text-amber-600" />
                            <span>Extension Poste (Forme L)</span>
                          </span>
                          <span className={`font-mono text-xs font-extrabold px-2 py-0.5 rounded border ${
                            hasCivilExtension ? "bg-amber-50 text-amber-800 border-amber-200" : "bg-slate-100 text-slate-400 border-slate-200"
                          }`}>
                            {hasCivilExtension ? `${extLength}m x ${extWidth}m` : "Désactivée"}
                          </span>
                        </div>
                        {hasCivilExtension && (
                          <div className="text-[10px] text-slate-500 flex items-center justify-between">
                            <span>Côté: <strong className="uppercase">{extWall}</strong></span>
                            <span>Offset: {extOffset}m</span>
                          </div>
                        )}
                        <button
                          type="button"
                          onClick={() => setActiveCadModal("extension")}
                          className="w-full py-1.5 px-3 bg-amber-50 hover:bg-amber-100 text-amber-800 font-bold text-[10px] rounded-lg border border-amber-200 flex items-center justify-center gap-1.5 transition-all shadow-2xs"
                        >
                          <Maximize2 className="w-3.5 h-3.5" />
                          <span>Configurer Extension Forme L (Fenêtre CAD) ⚙️</span>
                        </button>
                      </div>'''

new_card_3 = '''                      {/* 3. Carte Gestion des Ouvrages & Blocs Multiples */}
                      <div className="bg-white p-3 rounded-xl border border-slate-200 hover:border-amber-400 transition-all shadow-2xs space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-[11px] font-black text-slate-800 uppercase flex items-center gap-1.5">
                            <Square className="w-4 h-4 text-amber-600" />
                            <span>Ouvrages & Blocs ({ouvrages.length})</span>
                          </span>
                          <span className="font-mono text-xs font-extrabold px-2 py-0.5 rounded border bg-amber-50 text-amber-800 border-amber-200">
                            {ouvrages.length > 1 ? `${ouvrages.length} Blocs` : "Poste Unique"}
                          </span>
                        </div>
                        <div className="text-[10px] text-slate-500 flex items-center justify-between">
                          <span>Positions & Dimensions Libres</span>
                          <span className="font-bold text-amber-800">Nouveau / Ancien</span>
                        </div>
                        <button
                          type="button"
                          onClick={() => setActiveCadModal("ouvrages")}
                          className="w-full py-1.5 px-3 bg-amber-50 hover:bg-amber-100 text-amber-800 font-bold text-[10px] rounded-lg border border-amber-200 flex items-center justify-center gap-1.5 transition-all shadow-2xs"
                        >
                          <Maximize2 className="w-3.5 h-3.5" />
                          <span>Gérer les Ouvrages & Blocs (Fenêtre CAD) ⚙️</span>
                        </button>
                      </div>'''

if old_card_3 in code:
    code = code.replace(old_card_3, new_card_3)
    print("Card 3 replaced successfully")
else:
    print("Could not find old_card_3")

# Replace header text in Modal
old_modal_header = '{activeCadModal === "extension" && "Extension Génie Civil (Forme L)"}'
new_modal_header = '{activeCadModal === "ouvrages" && "Gestion des Ouvrages & Blocs (Multi-Postes / Extensions)"}'
code = code.replace(old_modal_header, new_modal_header)

# Replace Modal Body
old_modal_body = '''              {/* 4. EXTENSION CAD MODAL - Multi-Extension L Placement Libre */}
              {activeCadModal === "extension" && (
                <div className="space-y-4">
                  <div className="flex justify-between items-center bg-amber-50 p-3 rounded-xl border border-amber-200">
                    <span className="text-xs font-black text-amber-950 uppercase">
                      Extensions Génie Civil en Forme L ({extensions.length})
                    </span>
                    <button
                      type="button"
                      onClick={() => handleAddExtension()}
                      className="px-3 py-1.5 bg-amber-700 hover:bg-amber-800 text-white rounded-lg text-xs font-black flex items-center gap-1 shadow-xs cursor-pointer"
                    >
                      <Plus className="w-3.5 h-3.5" />
                      <span>Ajouter Extension L</span>
                    </button>
                  </div>

                  <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
                    {extensions.map((ext) => (
                      <div key={ext.id} className="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-3">
                        <div className="flex justify-between items-center">
                          <input
                            type="text"
                            value={ext.name}
                            onChange={(e) => handleUpdateExtension(ext.id, "name", e.target.value)}
                            className="font-bold text-xs bg-white border border-slate-300 rounded px-2 py-1 text-slate-800 w-2/3"
                          />
                          <div className="flex items-center gap-1">
                            <button
                              type="button"
                              onClick={() => handleDuplicateExtension(ext.id)}
                              className="p-1 bg-white border border-slate-200 text-slate-600 hover:bg-slate-100 rounded"
                              title="Dupliquer"
                            >
                              <Copy className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() => handleRemoveExtension(ext.id)}
                              className="p-1 bg-white border border-red-200 text-red-600 hover:bg-red-50 rounded"
                              title="Supprimer"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-2">
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Position / Mur :</label>
                            <select
                              value={ext.wall}
                              onChange={(e) => handleUpdateExtension(ext.id, "wall", e.target.value)}
                              className="w-full font-bold bg-white border border-slate-300 rounded px-2 py-1 text-xs capitalize"
                            >
                              <option value="est">Est</option>
                              <option value="ouest">Ouest</option>
                              <option value="nord">Nord</option>
                              <option value="sud">Sud</option>
                              <option value="libre">Libre (Placement X,Y)</option>
                            </select>
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Désignation :</label>
                            <span className="text-xs font-mono font-bold text-amber-800 bg-amber-50 px-2 py-1 block rounded border border-amber-200">
                              Extension L ({ext.length}m x {ext.width}m)
                            </span>
                          </div>
                        </div>

                        <div className="grid grid-cols-4 gap-2">
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Longueur A\' (m) :</label>
                            <input
                              type="number"
                              step="0.1"
                              value={ext.length}
                              onChange={(e) => handleUpdateExtension(ext.id, "length", parseFloat(e.target.value) || 0)}
                              className="w-full font-mono font-bold bg-white border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Largeur B\' (m) :</label>
                            <input
                              type="number"
                              step="0.1"
                              value={ext.width}
                              onChange={(e) => handleUpdateExtension(ext.id, "width", parseFloat(e.target.value) || 0)}
                              className="w-full font-mono font-bold bg-white border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Pos X (m / Ml) :</label>
                            <input
                              type="number"
                              step="0.1"
                              value={ext.xOffset}
                              onChange={(e) => handleUpdateExtension(ext.id, "xOffset", parseFloat(e.target.value) || 0)}
                              className="w-full font-mono font-bold bg-white border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Pos Y (m / Ml) :</label>
                            <input
                              type="number"
                              step="0.1"
                              value={ext.yOffset}
                              onChange={(e) => handleUpdateExtension(ext.id, "yOffset", parseFloat(e.target.value) || 0)}
                              className="w-full font-mono font-bold bg-white border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}'''

new_modal_body = '''              {/* 4. OUVRAGES CAD MODAL - Multi-Ouvrages / Blocs Placement Libre */}
              {activeCadModal === "ouvrages" && (
                <div className="space-y-4">
                  <div className="flex justify-between items-center bg-amber-50 p-3 rounded-xl border border-amber-200">
                    <div>
                      <span className="text-xs font-black text-amber-950 uppercase block">
                        Gestion des Blocs & Ouvrages du Croquis ({ouvrages.length})
                      </span>
                      <span className="text-[10px] text-amber-800">
                        Chaque bloc peut être configuré en Nouveau (Projet/Extension) ou Ancien (Existant) et positionné librement (X,Y).
                      </span>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleAddOuvrage()}
                      className="px-3 py-1.5 bg-amber-700 hover:bg-amber-800 text-white rounded-lg text-xs font-black flex items-center gap-1 shadow-xs cursor-pointer"
                    >
                      <Plus className="w-3.5 h-3.5" />
                      <span>Ajouter un Ouvrage / Bloc</span>
                    </button>
                  </div>

                  <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1">
                    {ouvrages.map((ov, idx) => (
                      <div key={ov.id} className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-3 shadow-2xs">
                        <div className="flex justify-between items-center gap-2">
                          <div className="flex items-center gap-2 flex-1">
                            <span className="text-xs font-mono font-black text-slate-500 bg-slate-200 px-2 py-0.5 rounded">
                              #{idx + 1}
                            </span>
                            <input
                              type="text"
                              value={ov.name}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "name", e.target.value)}
                              className="font-bold text-xs bg-white border border-slate-300 rounded px-2 py-1 text-slate-800 w-full"
                              placeholder="Nom de l'ouvrage..."
                            />
                          </div>

                          {/* Statut Nouveau vs Ancien */}
                          <div className="flex items-center gap-1">
                            <select
                              value={ov.status}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "status", e.target.value as "nouveau" | "ancien")}
                              className={`font-mono font-bold text-xs rounded px-2 py-1 border ${
                                ov.status === "nouveau"
                                  ? "bg-sky-100 text-sky-800 border-sky-300"
                                  : "bg-slate-200 text-slate-700 border-slate-300"
                              }`}
                            >
                              <option value="nouveau">🆕 NOUVEAU / EXTENSION</option>
                              <option value="ancien">🏛️ ANCIEN / EXISTANT</option>
                            </select>

                            <button
                              type="button"
                              onClick={() => handleDuplicateOuvrage(ov.id)}
                              className="p-1.5 bg-white border border-slate-200 text-slate-600 hover:bg-slate-100 rounded"
                              title="Dupliquer"
                            >
                              <Copy className="w-3.5 h-3.5" />
                            </button>
                            {ouvrages.length > 1 && (
                              <button
                                type="button"
                                onClick={() => handleRemoveOuvrage(ov.id)}
                                className="p-1.5 bg-white border border-red-200 text-red-600 hover:bg-red-50 rounded"
                                title="Supprimer"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            )}
                          </div>
                        </div>

                        {/* Coordonnées & Dimensions */}
                        <div className="grid grid-cols-5 gap-2 bg-white p-2 rounded-lg border border-slate-200">
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Long. A (m):</label>
                            <input
                              type="number"
                              step="0.5"
                              value={ov.length}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "length", parseFloat(e.target.value) || 1)}
                              className="w-full font-mono font-bold bg-slate-50 border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Larg. B (m):</label>
                            <input
                              type="number"
                              step="0.5"
                              value={ov.width}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "width", parseFloat(e.target.value) || 1)}
                              className="w-full font-mono font-bold bg-slate-50 border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Pos X (m):</label>
                            <input
                              type="number"
                              step="0.5"
                              value={ov.xOffset}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "xOffset", parseFloat(e.target.value) || 0)}
                              className="w-full font-mono font-bold bg-slate-50 border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">Pos Y (m):</label>
                            <input
                              type="number"
                              step="0.5"
                              value={ov.yOffset}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "yOffset", parseFloat(e.target.value) || 0)}
                              className="w-full font-mono font-bold bg-slate-50 border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                          <div>
                            <label className="text-[9px] font-bold text-slate-500 block">H Clôture (m):</label>
                            <input
                              type="number"
                              step="0.1"
                              value={ov.fenceHeight}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "fenceHeight", parseFloat(e.target.value) || 2.5)}
                              className="w-full font-mono font-bold bg-slate-50 border border-slate-300 rounded px-1.5 py-1 text-xs"
                            />
                          </div>
                        </div>

                        {/* Éléments de l'Ouvrage */}
                        <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-slate-200 text-[10px]">
                          <label className="flex items-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={ov.hasFence}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "hasFence", e.target.checked)}
                              className="rounded text-amber-600"
                            />
                            <span>Clôture Périmétrique</span>
                          </label>
                          <label className="flex items-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={ov.hasVoile}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "hasVoile", e.target.checked)}
                              className="rounded text-indigo-600"
                            />
                            <span>Voile Béton Armé</span>
                          </label>
                          <label className="flex items-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={ov.hasGabions}
                              onChange={(e) => handleUpdateOuvrage(ov.id, "hasGabions", e.target.checked)}
                              className="rounded text-amber-700"
                            />
                            <span>Gabions de Protection</span>
                          </label>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}'''

if old_modal_body in code:
    code = code.replace(old_modal_body, new_modal_body)
    print("Modal body replaced successfully")
else:
    print("Could not find old_modal_body")

with open("src/components/Calculators.tsx", "w") as f:
    f.write(code)
