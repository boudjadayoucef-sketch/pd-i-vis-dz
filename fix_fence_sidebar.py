file_path = "src/components/Calculators.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """                    {/* Clôture Panneaux Profilés */}
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

replacement = """                    {/* Clôture Panneaux Profilés & Dimensionnement du Poste */}
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

if target in content:
    content = content.replace(target, replacement)
    print("Replaced successfully!")
else:
    print("Target still not matched!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
