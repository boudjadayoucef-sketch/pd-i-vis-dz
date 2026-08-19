import sys
import re

with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

print("File loaded. Length:", len(code))

# 1. REPLACE TOP SUB-NAV BAR (remove horizontal scroll, show all buttons in grid)
nav_old_pattern = r'\{/\* Horizontal Navigation Bar for Calculators & Tools \*/\}.*?\{/\* Content Pane - Full Width \*/\}'

nav_new_code = '''{/* Horizontal Navigation Bar for Calculators & Tools */}
      <div className="bg-slate-50/90 rounded-2xl border border-slate-200 p-3 space-y-2 mb-4 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-200/80 pb-2 px-1">
          <h3 className="text-xs font-black uppercase tracking-wider text-slate-600 flex items-center gap-1.5">
            <Calculator className="w-4 h-4 text-orange-500" />
            <span>Calculateurs & Outils Réglementaires</span>
          </h3>
          <span className="text-[10px] font-bold text-slate-500 hidden sm:inline">
            {activeTab === "spare" && "Fascicule 1 — Pièces de Rechange"}
            {activeTab === "emprise" && "Fascicule 2 — Emprise de Piste"}
            {activeTab === "bending" && "Fascicule 3 — Cintrage à Froid"}
            {activeTab === "cavalier" && "Fascicule 7 — Lestage & Cavalier"}
            {activeTab === "gauvin" && "Fascicule 5 — Test GAUVIN & Profil Hydrostatique"}
            {activeTab === "poste_gc" && "Génie Civil Poste de Gaz"}
            {activeTab === "reception_usine" && "Réception Tube Usine"}
            {activeTab === "poste_croquis" && "Concepteur de Croquis Génie Civil"}
            {activeTab === "bordereau" && "Bordereau des Prix Unitaires (BPU)"}
          </span>
        </div>
        
        {/* Sleek Grid Navigation — No Horizontal Scroll, All 9 Tabs Visible */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-9 gap-1.5">
          <button
            type="button"
            onClick={() => setActiveTab("spare")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "spare"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <Layers className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">Pièces (Fasc. 1)</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("emprise")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "emprise"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <Sliders className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">Emprise (Fasc. 2)</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("bending")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "bending"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <Zap className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">Cintrage (Fasc. 3)</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("cavalier")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "cavalier"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <Waves className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">Lestage (Fasc. 7)</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("gauvin")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "gauvin"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <Flame className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">GAUVIN (Fasc. 5)</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("poste_gc")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "poste_gc"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <Construction className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">Génie Civil Poste</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("reception_usine")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "reception_usine"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <Truck className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">Réception Tube</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("poste_croquis")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "poste_croquis"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <Compass className="w-3.5 h-3.5 shrink-0 text-amber-300 animate-pulse" />
            <span className="truncate">Croquis & CAD</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("bordereau")}
            className={`flex items-center justify-center gap-1.5 px-2 py-2 rounded-xl text-[11px] font-black transition-all border text-center cursor-pointer ${
              activeTab === "bordereau"
                ? "bg-gradient-to-r from-orange-600 to-orange-700 text-white border-orange-800 shadow-md shadow-orange-500/20 ring-2 ring-orange-500/30 scale-[1.02]"
                : "bg-white hover:bg-slate-100 border-slate-200 text-slate-700 hover:border-slate-300"
            }`}
          >
            <FileText className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">BPU & Prix</span>
          </button>
        </div>
      </div>

      {/* Content Pane - Full Width */}'''

code = re.sub(nav_old_pattern, nav_new_code, code, flags=re.DOTALL)
print("Nav bar replaced.")

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
print("File updated with sub-nav bar changes.")
