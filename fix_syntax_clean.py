import sys

with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix extra </div> in bending tab
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
      )}

      {activeTab === "cavalier" && ('''

code = code.replace(bend_err, bend_fix)

# 2. Fix Carré Orange in croquis mode
# Replace misplaced SVG <g> and IIFE in Carré Orange
orange_err_target = '''            <div className="flex items-center justify-between border-b border-orange-500/30 pb-2 mb-2">
              <span className="text-xs font-black uppercase text-orange-400 tracking-wider flex items-center gap-2">
                <FileText className="w-4 h-4 text-orange-400" />
                <span>Carré Orange — Cartouche Technique Normalisé Sonelgaz (Block 2 d'Impression)</span>
              </span>
              <span className="text-[10px] bg-orange-950 text-orange-300 font-mono font-bold px-2.5 py-0.5 rounded border border-orange-800">
                Plan N° {cartoucheInfo.planNumber || "SONELGAZ-GC-001"}
              </span>
            </div>
{/* ==================== A3 FORMAT TITLE BLOCK / CARTOUCHE ==================== */}
                              <g transform={`translate(${svgW - 460}, ${svgH - 220})`}>'''

orange_fix_replacement = '''            <div className="flex items-center justify-between border-b border-orange-500/30 pb-2 mb-2">
              <span className="text-xs font-black uppercase text-orange-400 tracking-wider flex items-center gap-2">
                <FileText className="w-4 h-4 text-orange-400" />
                <span>Carré Orange — Cartouche Technique Normalisé Sonelgaz (Block 2 d'Impression)</span>
              </span>
              <span className="text-[10px] bg-orange-950 text-orange-300 font-mono font-bold px-2.5 py-0.5 rounded border border-orange-800">
                Plan N° {cartoucheInfo.planNumber || "SONELGAZ-GC-001"}
              </span>
            </div>

            {/* Rendered Normalized Sonelgaz Cartouche Title Block */}
            <div className="w-full bg-slate-950 rounded-2xl p-4 border border-slate-800 flex justify-center items-center overflow-x-auto">
              <svg viewBox="0 0 450 205" className="w-full max-w-lg h-auto">
                <g transform="translate(7, 5)">'''

code = code.replace(orange_err_target, orange_fix_replacement)

# Fix closing of the Cartouche SVG and remove orphaned IIFE lines
orphan_err = '''                              </g>
                            </svg>
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

            
                          );
                        })()}
                      </div>
                    </div>'''

orphan_fix = '''                              </g>
                            </svg>
            </div>'''

code = code.replace(orphan_err, orphan_fix)

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Syntax fix script executed.")
