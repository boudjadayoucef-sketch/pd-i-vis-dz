import sys
import re

# Read the clean state before we broke it or read Calculators.tsx
with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix Bending Tab Closing Tag syntax
# Let's inspect bending block around line 2840-2935
bend_err = '''            <p className="text-[10px] text-slate-400 text-center italic">
              Rayon minimal autorisé sans ovalisation nocive ni plissement de génératrice (Fascicule 3).
            </p>
          </div>
        </div>
      )}

        {activeTab === "cavalier" && ('''

bend_fix = '''            <p className="text-[10px] text-slate-400 text-center italic">
              Rayon minimal autorisé sans ovalisation nocive ni plissement de génératrice (Fascicule 3).
            </p>
          </div>
        </div>
      )}

      {activeTab === "cavalier" && ('''

if bend_err in code:
    code = code.replace(bend_err, bend_fix)

# 2. Fix croquisMode === "parametrique"
# Let's locate croquisMode === "parametrique"
pos_mode = code.find('croquisMode === "parametrique" && (')
pos_libre = code.find('croquisMode === "libre" && (')

print("pos_mode:", pos_mode, "pos_libre:", pos_libre)

# Let's construct a clean structure for croquisMode === "parametrique"
# Yellow box at top:
# - Type de projet switcher
# - 7 CAD component cards grid
# Blue box in middle:
# - The complete SVG drawing canvas container
# Orange box at bottom:
# - Cartouche control & editing panel (Block 2) + Quantitatif Estimatif

# Let's check where the SVG canvas starts inside parametrique mode
mode_str = code[pos_mode:pos_libre]

# Find where the SVG canvas wrapper div starts
# It starts around: `{/* Main Drawing Canvas & Interactive SVG */}` or `svgW`
canvas_wrapper_pos = mode_str.find('<div className="relative bg-slate-950')
if canvas_wrapper_pos == -1:
    canvas_wrapper_pos = mode_str.find('svgW')
    canvas_wrapper_pos = mode_str.rfind('<div', 0, canvas_wrapper_pos)

print("canvas_wrapper_pos:", canvas_wrapper_pos)

# Find where the cartouche panel / quantitatif starts after the svg canvas ends
svg_end_pos = mode_str.find('</svg>')
print("svg_end_pos:", svg_end_pos)

# Extract drawing canvas part (including controls and SVG canvas)
canvas_part = mode_str[canvas_wrapper_pos:svg_end_pos + 6]

# Extract remaining part after SVG canvas (Cartouche panel, controls, quantitatif)
after_svg_part = mode_str[svg_end_pos + 6:]
# remove trailing closing tags from after_svg_part
after_svg_part = after_svg_part.rstrip()
if after_svg_part.endswith(')}'):
    after_svg_part = after_svg_part[:-2]
if after_svg_part.endswith('</div>'):
    after_svg_part = after_svg_part[:-6]

# Now assemble the clean 3-box layout
new_croquis_block = '''croquisMode === "parametrique" && (
        <div className="space-y-6 animate-fade-in text-left">
          
          {/* ========================================================================= */}
          {/* CARRÉ JAUNE (YELLOW BOX): TOP HORIZONTAL TOOLBAR & CAD MODULE CARDS        */}
          {/* ========================================================================= */}
          <div className="w-full bg-slate-900 border-2 border-amber-400 rounded-3xl p-4 md:p-5 text-white space-y-4 shadow-xl relative overflow-hidden">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-amber-400/30 pb-3">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-2xl bg-amber-500/20 border border-amber-400 flex items-center justify-center text-amber-400 shrink-0">
                  <SlidersHorizontal className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-xs font-black uppercase text-amber-400 tracking-wider flex items-center gap-2">
                    <span>Carré Jaune — Module de Saisie CAD & Configuration Horizontal</span>
                  </h3>
                  <p className="text-[11px] text-slate-300 mt-0.5">
                    Sélectionnez un composant ci-dessous pour ouvrir sa fenêtre d'édition CAD paramétrique.
                  </p>
                </div>
              </div>

              {/* Config Type de Projet Switcher */}
              <div className="flex items-center gap-2 bg-slate-950 p-1.5 rounded-xl border border-amber-400/30 shrink-0">
                <span className="text-[10px] font-black text-amber-300 uppercase tracking-wider px-2">Type de Projet :</span>
                <button
                  type="button"
                  onClick={() => setConceptionMode("neuf")}
                  className={`px-3 py-1.5 text-xs font-black rounded-lg transition-all cursor-pointer ${
                    conceptionMode === "neuf" ? "bg-blue-600 text-white shadow-xs" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Ouvrage Neuf
                </button>
                <button
                  type="button"
                  onClick={() => setConceptionMode("extension")}
                  className={`px-3 py-1.5 text-xs font-black rounded-lg transition-all cursor-pointer ${
                    conceptionMode === "extension" ? "bg-orange-600 text-white shadow-xs" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Extension
                </button>
              </div>
            </div>

            {/* HORIZONTAL GRID OF 7 CAD COMPONENT EDIT CARDS */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7 gap-3">
              {/* 1. Périmètre & Clôture */}
              <div className="bg-slate-800/90 p-3 rounded-2xl border border-slate-700 hover:border-blue-400 transition-all space-y-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <span className="text-[11px] font-black text-white uppercase flex items-center gap-1.5 truncate">
                      <ShieldAlert className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                      <span className="truncate">Périmètre & Clôture</span>
                    </span>
                  </div>
                  <span className="font-mono text-blue-300 font-extrabold text-[10px] bg-blue-950 px-2 py-0.5 rounded border border-blue-800 inline-block">
                    {fenceA}m x {fenceB}m
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveCadModal("perimeter")}
                  className="w-full py-1.5 px-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Saisir Périmètre ⚙️</span>
                </button>
              </div>

              {/* 2. Abri Télé-exploitation */}
              <div className="bg-slate-800/90 p-3 rounded-2xl border border-slate-700 hover:border-emerald-400 transition-all space-y-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <span className="text-[11px] font-black text-white uppercase flex items-center gap-1.5 truncate">
                      <Building2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span className="truncate">Abri Télé-expl.</span>
                    </span>
                  </div>
                  <span className="font-mono text-emerald-300 font-extrabold text-[10px] bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800 inline-block">
                    {teleShelterLength}m x {teleShelterWidth}m
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveCadModal("shelters")}
                  className="w-full py-1.5 px-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Saisir Abri Télé ⚙️</span>
                </button>
              </div>

              {/* 3. Ouvrages & Blocs */}
              <div className="bg-slate-800/90 p-3 rounded-2xl border border-slate-700 hover:border-amber-400 transition-all space-y-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <span className="text-[11px] font-black text-white uppercase flex items-center gap-1.5 truncate">
                      <Square className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                      <span className="truncate">Ouvrages & Blocs</span>
                    </span>
                  </div>
                  <span className="font-mono text-amber-300 font-extrabold text-[10px] bg-amber-950 px-2 py-0.5 rounded border border-amber-800 inline-block">
                    {ouvrages.length > 1 ? `${ouvrages.length} Blocs` : "Poste Unique"}
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveCadModal("ouvrages")}
                  className="w-full py-1.5 px-2 bg-amber-600 hover:bg-amber-500 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Gérer Blocs ⚙️</span>
                </button>
              </div>

              {/* 4. Voile Béton Armé */}
              <div className="bg-slate-800/90 p-3 rounded-2xl border border-slate-700 hover:border-indigo-400 transition-all space-y-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <span className="text-[11px] font-black text-white uppercase flex items-center gap-1.5 truncate">
                      <Shield className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                      <span className="truncate">Voile Béton Armé</span>
                    </span>
                  </div>
                  <span className={`font-mono text-[10px] font-extrabold px-2 py-0.5 rounded border inline-block ${
                    hasVoilePeripherique ? "bg-indigo-950 text-indigo-300 border-indigo-800" : "bg-slate-900 text-slate-400 border-slate-800"
                  }`}>
                    {hasVoilePeripherique ? `${voileSides.length} Côté(s)` : "Désactivé"}
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveCadModal("voile")}
                  className="w-full py-1.5 px-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Saisir Voile ⚙️</span>
                </button>
              </div>

              {/* 5. Murs en Gabions */}
              <div className="bg-slate-800/90 p-3 rounded-2xl border border-slate-700 hover:border-amber-500 transition-all space-y-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <span className="text-[11px] font-black text-white uppercase flex items-center gap-1.5 truncate">
                      <Construction className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                      <span className="truncate">Murs Gabions</span>
                    </span>
                  </div>
                  <span className={`font-mono text-[10px] font-extrabold px-2 py-0.5 rounded border inline-block ${
                    hasGabions ? "bg-amber-950 text-amber-300 border-amber-800" : "bg-slate-900 text-slate-400 border-slate-800"
                  }`}>
                    {hasGabions ? `${Object.entries(gabionSideConfigs).filter(([_, c]) => c.enabled).length} Côté(s)` : "Désactivés"}
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveCadModal("gabions")}
                  className="w-full py-1.5 px-2 bg-amber-700 hover:bg-amber-600 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Designer Gabions ⚙️</span>
                </button>
              </div>

              {/* 6. Dalles & Socles Béton */}
              <div className="bg-slate-800/90 p-3 rounded-2xl border border-slate-700 hover:border-purple-400 transition-all space-y-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <span className="text-[11px] font-black text-white uppercase flex items-center gap-1.5 truncate">
                      <Layers className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                      <span className="truncate">Dalles & Socles</span>
                    </span>
                  </div>
                  <span className="font-mono text-purple-300 font-extrabold text-[10px] bg-purple-950 px-2 py-0.5 rounded border border-purple-800 inline-block">
                    {slabs.length} Dalles ({totalSlabsArea.toFixed(1)} m²)
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveCadModal("slabs")}
                  className="w-full py-1.5 px-2 bg-purple-600 hover:bg-purple-500 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Gérer Dalles ⚙️</span>
                </button>
              </div>

              {/* 7. Portails & Accès */}
              <div className="bg-slate-800/90 p-3 rounded-2xl border border-slate-700 hover:border-cyan-400 transition-all space-y-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <span className="text-[11px] font-black text-white uppercase flex items-center gap-1.5 truncate">
                      <DoorClosed className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                      <span className="truncate">Portails & Accès</span>
                    </span>
                  </div>
                  <span className="font-mono text-cyan-300 font-extrabold text-[10px] bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800 inline-block">
                    {gates.length} Accès
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveCadModal("gates")}
                  className="w-full py-1.5 px-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-[10px] rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <Maximize2 className="w-3 h-3" />
                  <span className="truncate">Placer Accès ⚙️</span>
                </button>
              </div>
            </div>
          </div>

          {/* ========================================================================= */}
          {/* CARRÉ BLEU (BLUE BOX): SECTION DESSIN ET ÉDITION (FULL WIDTH CANVAS)       */}
          {/* ========================================================================= */}
          <div className="w-full bg-slate-950 border-2 border-blue-500/80 rounded-3xl p-4 md:p-6 text-white space-y-4 shadow-2xl relative">
            <div className="flex items-center justify-between border-b border-blue-500/30 pb-2 mb-2">
              <span className="text-xs font-black uppercase text-cyan-400 tracking-wider flex items-center gap-2">
                <Compass className="w-4 h-4 text-cyan-400" />
                <span>Carré Bleu — Espace de Dessin, Canvas et Édition Technique (Grand Format)</span>
              </span>
              <span className="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-2.5 py-0.5 rounded border border-blue-800">
                Format d'Impression A3 (1189 x 841 mm)
              </span>
            </div>

            ''' + canvas_part + '''
          </div>

          {/* ========================================================================= */}
          {/* CARRÉ ORANGE (ORANGE BOX): SECTION CARTOUCHE TECHNIQUE (BLOCK 2)           */}
          {/* ========================================================================= */}
          <div className="w-full bg-slate-900 border-2 border-orange-500/80 rounded-3xl p-5 text-white space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-orange-500/30 pb-2 mb-2">
              <span className="text-xs font-black uppercase text-orange-400 tracking-wider flex items-center gap-2">
                <FileText className="w-4 h-4 text-orange-400" />
                <span>Carré Orange — Cartouche Technique Normalisé Sonelgaz (Block 2 d'Impression)</span>
              </span>
              <span className="text-[10px] bg-orange-950 text-orange-300 font-mono font-bold px-2.5 py-0.5 rounded border border-orange-800">
                Plan N° {cartoucheInfo.planNumber || "SONELGAZ-GC-001"}
              </span>
            </div>

            ''' + after_svg_part + '''
          </div>
        </div>
      )'''

code = code[:pos_mode] + new_croquis_block + code[pos_libre:]

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Reorganisation script executed successfully.")
