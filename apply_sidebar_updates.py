import sys

file_path = "src/components/Calculators.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. REPLACE FENCE & POSTS SIDEBAR INPUTS
old_fence_sidebar = """                    {/* Clôture Panneaux Profilés */}
                    <div className="space-y-3 pt-4 border-t border-slate-200">
                      <div className="flex justify-between items-center">
                        <span className="text-[11px] font-black text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                          <ShieldAlert className="w-4 h-4 text-slate-600" />
                          <span>Clôture Panneaux Profilés</span>
                        </span>
                        <span className="font-mono text-blue-600 font-extrabold text-xs bg-blue-50 px-2 py-0.5 rounded border border-blue-100">
                          {fenceA}m x {fenceB}m (H={fenceHeight}m)
                        </span>
                      </div>

                      <div className="bg-blue-50/70 p-2.5 rounded-xl border border-blue-100 text-[10px] text-slate-600 leading-relaxed">
                        Panneaux profilés électrosoudés (long. 3m) avec fil barbelé supérieur. Poteaux Fer H scellés dans semelles béton <strong>80x80cm</strong>.
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div className="space-y-1">
                          <span className="text-[9px] text-slate-500 font-bold block">Longueur A ({fenceA}m) :</span>
                          <input
                            type="range"
                            min="15"
                            max="80"
                            value={fenceA}
                            onChange={(e) => setFenceA(parseInt(e.target.value))}
                            className="w-full accent-blue-600"
                          />
                        </div>
                        <div className="space-y-1">
                          <span className="text-[9px] text-slate-500 font-bold block">Largeur B ({fenceB}m) :</span>
                          <input
                            type="range"
                            min="10"
                            max="50"
                            value={fenceB}
                            onChange={(e) => setFenceB(parseInt(e.target.value))}
                            className="w-full accent-blue-600"
                          />
                        </div>
                      </div>

                      <div className="space-y-1">
                        <span className="text-[9px] text-slate-500 font-bold block">Hauteur des Panneaux :</span>
                        <div className="grid grid-cols-3 gap-1.5">
                          {[2.5, 2.8, 3.0].map((h) => (
                            <button
                              key={h}
                              type="button"
                              onClick={() => setFenceHeight(h)}
                              className={`py-1 text-center text-xs font-bold rounded border transition-all ${
                                fenceHeight === h
                                  ? "bg-blue-600 text-white border-blue-600"
                                  : "bg-white text-slate-700 border-slate-200 hover:bg-slate-100"
                              }`}
                            >
                              {h} m
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>"""

new_fence_sidebar = """                    {/* Clôture Panneaux Profilés & Dimensionnement du Poste */}
                    <div className="space-y-3 pt-4 border-t border-slate-200">
                      <div className="flex justify-between items-center">
                        <span className="text-[11px] font-black text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                          <ShieldAlert className="w-4 h-4 text-blue-600" />
                          <span>Périmètre & Poteaux du Poste</span>
                        </span>
                        <span className="font-mono text-blue-600 font-extrabold text-xs bg-blue-50 px-2 py-0.5 rounded border border-blue-100">
                          {fenceA}m x {fenceB}m
                        </span>
                      </div>

                      {/* Libération de la Saisie Directe Longueur & Largeur du Poste */}
                      <div className="grid grid-cols-2 gap-3 bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
                        <div className="space-y-1">
                          <label className="text-[9px] text-slate-600 font-extrabold uppercase block">
                            Longueur A (m) :
                          </label>
                          <input
                            type="number"
                            min="5"
                            max="500"
                            step="0.5"
                            value={fenceA}
                            onChange={(e) => setFenceA(Math.max(5, parseFloat(e.target.value) || 35))}
                            className="w-full text-xs font-mono font-bold bg-slate-50 border border-slate-300 rounded px-2 py-1 focus:ring-1 focus:ring-blue-500"
                          />
                        </div>
                        <div className="space-y-1">
                          <label className="text-[9px] text-slate-600 font-extrabold uppercase block">
                            Largeur B (m) :
                          </label>
                          <input
                            type="number"
                            min="5"
                            max="500"
                            step="0.5"
                            value={fenceB}
                            onChange={(e) => setFenceB(Math.max(5, parseFloat(e.target.value) || 21))}
                            className="w-full text-xs font-mono font-bold bg-slate-50 border border-slate-300 rounded px-2 py-1 focus:ring-1 focus:ring-blue-500"
                          />
                        </div>
                      </div>

                      {/* Type de Poteaux : Fer H vs Béton Armé */}
                      <div className="space-y-2 bg-slate-100/80 p-2.5 rounded-xl border border-slate-200">
                        <label className="text-[10px] font-extrabold text-slate-700 uppercase block">
                          Matériau & Type de Poteaux :
                        </label>
                        <div className="grid grid-cols-2 gap-1.5">
                          <button
                            type="button"
                            onClick={() => setPostType("metal_heb")}
                            className={`py-1.5 px-2 text-[10px] font-black rounded-lg border transition-all ${
                              postType === "metal_heb"
                                ? "bg-slate-800 text-cyan-300 border-slate-800 shadow-2xs"
                                : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                            }`}
                          >
                            Poteaux Métalliques HEB
                          </button>
                          <button
                            type="button"
                            onClick={() => setPostType("beton_arme")}
                            className={`py-1.5 px-2 text-[10px] font-black rounded-lg border transition-all ${
                              postType === "beton_arme"
                                ? "bg-emerald-700 text-white border-emerald-700 shadow-2xs"
                                : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                            }`}
                          >
                            Poteaux Béton Armé
                          </button>
                        </div>

                        {postType === "beton_arme" && (
                          <div className="pt-2 border-t border-slate-200 space-y-2 bg-white p-2 rounded-lg border border-emerald-200">
                            <span className="text-[9px] font-extrabold text-emerald-800 uppercase block">
                              Section & Dimensions Poteau Béton :
                            </span>
                            <div className="grid grid-cols-3 gap-1.5 text-[9px]">
                              <div>
                                <label className="text-slate-500 font-bold block mb-0.5">Largeur (m) :</label>
                                <input
                                  type="number"
                                  min="0.15"
                                  max="1.0"
                                  step="0.05"
                                  value={postConcreteWidth}
                                  onChange={(e) => setPostConcreteWidth(Math.max(0.1, parseFloat(e.target.value) || 0.25))}
                                  className="w-full text-xs font-mono font-bold bg-slate-50 border border-slate-200 rounded px-1.5 py-0.5"
                                />
                              </div>
                              <div>
                                <label className="text-slate-500 font-bold block mb-0.5">Profondeur (m) :</label>
                                <input
                                  type="number"
                                  min="0.15"
                                  max="1.0"
                                  step="0.05"
                                  value={postConcreteDepth}
                                  onChange={(e) => setPostConcreteDepth(Math.max(0.1, parseFloat(e.target.value) || 0.25))}
                                  className="w-full text-xs font-mono font-bold bg-slate-50 border border-slate-200 rounded px-1.5 py-0.5"
                                />
                              </div>
                              <div>
                                <label className="text-slate-500 font-bold block mb-0.5">Hauteur (m) :</label>
                                <input
                                  type="number"
                                  min="1.5"
                                  max="5.0"
                                  step="0.1"
                                  value={postConcreteHeight}
                                  onChange={(e) => setPostConcreteHeight(Math.max(1, parseFloat(e.target.value) || 2.8))}
                                  className="w-full text-xs font-mono font-bold bg-slate-50 border border-slate-200 rounded px-1.5 py-0.5"
                                />
                              </div>
                            </div>
                          </div>
                        )}
                      </div>

                      <div className="space-y-1">
                        <span className="text-[9px] text-slate-500 font-bold block">Hauteur des Panneaux Clôture :</span>
                        <div className="grid grid-cols-3 gap-1.5">
                          {[2.5, 2.8, 3.0].map((h) => (
                            <button
                              key={h}
                              type="button"
                              onClick={() => setFenceHeight(h)}
                              className={`py-1 text-center text-xs font-bold rounded border transition-all ${
                                fenceHeight === h
                                  ? "bg-blue-600 text-white border-blue-600"
                                  : "bg-white text-slate-700 border-slate-200 hover:bg-slate-100"
                              }`}
                            >
                              {h} m
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>"""

if old_fence_sidebar in content:
    content = content.replace(old_fence_sidebar, new_fence_sidebar)
    print("Fence sidebar replacement successful!")
else:
    print("Fence sidebar target not found!")

# 2. ADD SIDEBAR SECTION FOR GATES & PORTILLONS MANAGEMENT
gates_sidebar = """                    {/* Dynamic Portails & Portillons Management */}
                    <div className="space-y-3 pt-4 border-t border-slate-200">
                      <div className="flex justify-between items-center">
                        <span className="text-[11px] font-black text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                          <DoorClosed className="w-4 h-4 text-amber-600" />
                          <span>Portails & Portillons ({gates.length})</span>
                        </span>
                        <div className="flex gap-1">
                          <button
                            type="button"
                            onClick={() => handleAddGate("portail_5m")}
                            className="text-[9px] bg-amber-600 hover:bg-amber-700 text-white font-extrabold py-1 px-2 rounded-lg flex items-center gap-1 transition-all"
                          >
                            <Plus className="w-3 h-3" />
                            <span>Portail 5m</span>
                          </button>
                          <button
                            type="button"
                            onClick={() => handleAddGate("portillon")}
                            className="text-[9px] bg-cyan-600 hover:bg-cyan-700 text-white font-extrabold py-1 px-2 rounded-lg flex items-center gap-1 transition-all"
                          >
                            <Plus className="w-3 h-3" />
                            <span>Portillon</span>
                          </button>
                        </div>
                      </div>

                      <div className="space-y-3 max-h-[280px] overflow-y-auto pr-1">
                        {gates.map((gate, index) => (
                          <div
                            key={gate.id}
                            className={`p-3 rounded-xl border transition-all space-y-2 ${
                              selectedGateId === gate.id
                                ? "bg-amber-50/70 border-amber-300 shadow-xs"
                                : "bg-white border-slate-200"
                            }`}
                          >
                            <div className="flex items-center justify-between border-b border-slate-100 pb-1.5">
                              <span className="text-[10px] font-extrabold text-amber-900 uppercase flex items-center gap-1">
                                <span className="w-4 h-4 rounded-full bg-amber-200 text-amber-900 flex items-center justify-center text-[9px]">
                                  {index + 1}
                                </span>
                                <span>{gate.name}</span>
                              </span>
                              <div className="flex items-center gap-1">
                                <button
                                  type="button"
                                  onClick={() => handleDuplicateGate(gate.id)}
                                  className="p-1 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded transition-all"
                                  title="Dupliquer (Raccourci: Clavier D / Ctrl+D)"
                                >
                                  <Copy className="w-3 h-3" />
                                </button>
                                {gates.length > 1 && (
                                  <button
                                    type="button"
                                    onClick={() => handleRemoveGate(gate.id)}
                                    className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded transition-all"
                                    title="Supprimer (Raccourci: Clavier Suppr)"
                                  >
                                    <Trash2 className="w-3.5 h-3.5" />
                                  </button>
                                )}
                              </div>
                            </div>

                            <div>
                              <label className="text-[8.5px] font-bold text-slate-400 block mb-0.5">Libellé :</label>
                              <input
                                type="text"
                                value={gate.name}
                                onChange={(e) => handleUpdateGate(gate.id, "name", e.target.value)}
                                className="w-full text-xs font-bold bg-white border border-slate-200 rounded px-2 py-1 focus:ring-1 focus:ring-amber-500"
                              />
                            </div>

                            <div className="grid grid-cols-3 gap-1.5 text-[10px]">
                              <div>
                                <label className="text-[8px] font-bold text-slate-500 block mb-0.5">Façade :</label>
                                <select
                                  value={gate.wall}
                                  onChange={(e) => handleUpdateGate(gate.id, "wall", e.target.value as any)}
                                  className="w-full text-xs font-extrabold bg-white border border-slate-200 rounded px-1 py-1 focus:ring-1 focus:ring-amber-500"
                                >
                                  <option value="sud">Sud (Bas)</option>
                                  <option value="nord">Nord (Haut)</option>
                                  <option value="est">Est (Droite)</option>
                                  <option value="ouest">Ouest (Gauche)</option>
                                </select>
                              </div>
                              <div>
                                <label className="text-[8px] font-bold text-slate-500 block mb-0.5">Position (m) :</label>
                                <input
                                  type="number"
                                  min="0"
                                  max={Math.max(0, (gate.wall === "sud" || gate.wall === "nord" ? fenceA : fenceB) - gate.width)}
                                  step="0.5"
                                  value={gate.offset}
                                  onChange={(e) => handleUpdateGate(gate.id, "offset", Math.max(0, parseFloat(e.target.value) || 0))}
                                  className="w-full text-xs font-mono font-bold bg-white border border-slate-200 rounded px-1 py-1"
                                />
                              </div>
                              <div>
                                <label className="text-[8px] font-bold text-slate-500 block mb-0.5">Largeur (m) :</label>
                                <input
                                  type="number"
                                  min="0.8"
                                  max="12"
                                  step="0.5"
                                  value={gate.width}
                                  onChange={(e) => handleUpdateGate(gate.id, "width", Math.max(0.5, parseFloat(e.target.value) || 1))}
                                  className="w-full text-xs font-mono font-bold bg-white border border-slate-200 rounded px-1 py-1"
                                />
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>"""

# Insert gates management before Dynamic Abris de Télé-exploitation
if "{/* Dynamic Abris de Télé-exploitation Management List */}" in content:
    content = content.replace("{/* Dynamic Abris de Télé-exploitation Management List */}", gates_sidebar + "\n\n                    {/* Dynamic Abris de Télé-exploitation Management List */}")
    print("Gates sidebar inserted successfully!")

# 3. ADD SIDEBAR SECTION FOR CONCRETE MASSIFS MANAGEMENT
massifs_sidebar = """                    {/* Dynamic Massifs Béton Management */}
                    <div className="space-y-3 pt-4 border-t border-slate-200">
                      <div className="flex justify-between items-center">
                        <span className="text-[11px] font-black text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                          <Box className="w-4 h-4 text-purple-600" />
                          <span>Massifs Béton ({massifs.length})</span>
                        </span>
                        <button
                          type="button"
                          onClick={handleAddMassif}
                          className="text-[10px] bg-purple-600 hover:bg-purple-700 text-white font-extrabold py-1 px-2.5 rounded-lg flex items-center gap-1 shadow-xs transition-all"
                        >
                          <Plus className="w-3 h-3" />
                          <span>Ajouter Massif</span>
                        </button>
                      </div>

                      <div className="space-y-3 max-h-[280px] overflow-y-auto pr-1">
                        {massifs.map((massif, index) => (
                          <div
                            key={massif.id}
                            className={`p-3 rounded-xl border transition-all space-y-2 ${
                              selectedMassifId === massif.id
                                ? "bg-purple-50/70 border-purple-300 shadow-xs"
                                : "bg-white border-slate-200"
                            }`}
                          >
                            <div className="flex items-center justify-between border-b border-slate-100 pb-1.5">
                              <span className="text-[10px] font-extrabold text-purple-900 uppercase flex items-center gap-1">
                                <span className="w-4 h-4 rounded-full bg-purple-200 text-purple-900 flex items-center justify-center text-[9px]">
                                  {index + 1}
                                </span>
                                <span>{massif.name}</span>
                              </span>
                              <div className="flex items-center gap-1">
                                <button
                                  type="button"
                                  onClick={() => handleDuplicateMassif(massif.id)}
                                  className="p-1 text-slate-400 hover:text-purple-600 hover:bg-purple-50 rounded transition-all"
                                  title="Dupliquer (Raccourci: Clavier D / Ctrl+D)"
                                >
                                  <Copy className="w-3 h-3" />
                                </button>
                                <button
                                  type="button"
                                  onClick={() => handleRemoveMassif(massif.id)}
                                  className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded transition-all"
                                  title="Supprimer (Raccourci: Clavier Suppr)"
                                >
                                  <Trash2 className="w-3.5 h-3.5" />
                                </button>
                              </div>
                            </div>

                            <div>
                              <label className="text-[8.5px] font-bold text-slate-400 block mb-0.5">Désignation Massif :</label>
                              <input
                                type="text"
                                value={massif.name}
                                onChange={(e) => handleUpdateMassif(massif.id, "name", e.target.value)}
                                className="w-full text-xs font-bold bg-white border border-slate-200 rounded px-2 py-1 focus:ring-1 focus:ring-purple-500"
                              />
                            </div>

                            <div className="grid grid-cols-3 gap-1.5 text-[10px]">
                              <div>
                                <label className="text-[8px] font-bold text-slate-500 block mb-0.5">Long. (m) :</label>
                                <input
                                  type="number"
                                  min="0.3"
                                  max="15"
                                  step="0.1"
                                  value={massif.length}
                                  onChange={(e) => handleUpdateMassif(massif.id, "length", Math.max(0.1, parseFloat(e.target.value) || 1))}
                                  className="w-full text-xs font-mono font-bold bg-white border border-slate-200 rounded px-1 py-0.5"
                                />
                              </div>
                              <div>
                                <label className="text-[8px] font-bold text-slate-500 block mb-0.5">Larg. (m) :</label>
                                <input
                                  type="number"
                                  min="0.3"
                                  max="15"
                                  step="0.1"
                                  value={massif.width}
                                  onChange={(e) => handleUpdateMassif(massif.id, "width", Math.max(0.1, parseFloat(e.target.value) || 1))}
                                  className="w-full text-xs font-mono font-bold bg-white border border-slate-200 rounded px-1 py-0.5"
                                />
                              </div>
                              <div>
                                <label className="text-[8px] font-bold text-slate-500 block mb-0.5">Haut. (m) :</label>
                                <input
                                  type="number"
                                  min="0.2"
                                  max="5"
                                  step="0.1"
                                  value={massif.height}
                                  onChange={(e) => handleUpdateMassif(massif.id, "height", Math.max(0.1, parseFloat(e.target.value) || 0.8))}
                                  className="w-full text-xs font-mono font-bold bg-white border border-slate-200 rounded px-1 py-0.5"
                                />
                              </div>
                            </div>

                            <div className="grid grid-cols-2 gap-2 text-[10px]">
                              <div>
                                <label className="text-[8px] font-bold text-slate-500 block mb-0.5">Pos X (m) :</label>
                                <input
                                  type="number"
                                  min="0"
                                  max={Math.max(0, fenceA - massif.length)}
                                  value={massif.xOffset}
                                  onChange={(e) => handleUpdateMassif(massif.id, "xOffset", Math.max(0, parseFloat(e.target.value) || 0))}
                                  className="w-full text-xs font-mono font-bold bg-white border border-slate-200 rounded px-1.5 py-0.5"
                                />
                              </div>
                              <div>
                                <label className="text-[8px] font-bold text-slate-500 block mb-0.5">Pos Y (m) :</label>
                                <input
                                  type="number"
                                  min="0"
                                  max={Math.max(0, fenceB - massif.width)}
                                  value={massif.yOffset}
                                  onChange={(e) => handleUpdateMassif(massif.id, "yOffset", Math.max(0, parseFloat(e.target.value) || 0))}
                                  className="w-full text-xs font-mono font-bold bg-white border border-slate-200 rounded px-1.5 py-0.5"
                                />
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>"""

# Insert massifs sidebar before Slabs List
if "{/* Dynamic Slabs List */}" in content or "<span>Liste des Dalles" in content:
    content = content.replace("{/* Dynamic Slabs List */}", massifs_sidebar + "\n\n                    {/* Dynamic Slabs List */}")
    print("Massifs sidebar inserted successfully!")

# 4. ADD CUSTOM SLAB OPTION TO DROPDOWN
old_slab_option = '<option value="abri_tele" className="bg-white text-slate-800">Dalle Abri Télé-exploitation</option>'
new_slab_option = '<option value="abri_tele" className="bg-white text-slate-800">Dalle Abri Télé-exploitation</option>\n                          <option value="dalle_custom" className="bg-white text-slate-800">+ Dalle Béton Sur-Mesure</option>'

if old_slab_option in content:
    content = content.replace(old_slab_option, new_slab_option)
    print("Slab option inserted successfully!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Part 2 sidebar updates applied!")
