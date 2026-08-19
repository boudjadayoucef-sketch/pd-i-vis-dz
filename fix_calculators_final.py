import re

with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# ==============================================================================
# FIX 1: activeTab === "bending" JSX structure
# ==============================================================================
bend_old = '''      {activeTab === "bending" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-fade-in">'''

bend_new = '''      {activeTab === "bending" && (
        <div className="space-y-6 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">'''

code = code.replace(bend_old, bend_new)

# Close the extra wrapping div for bending before cavalier tab
bend_close_old = '''            <p className="text-[10px] text-slate-400 text-center italic">
              Rayon minimal autorisé sans ovalisation nocive ni plissement de génératrice (Fascicule 3).
            </p>
          </div>
        </div>
      )}

      {activeTab === "cavalier" && ('''

bend_close_new = '''            <p className="text-[10px] text-slate-400 text-center italic">
              Rayon minimal autorisé sans ovalisation nocive ni plissement de génératrice (Fascicule 3).
            </p>
          </div>
        </div>
      )}

      {activeTab === "cavalier" && ('''

# If bend_close_old wasn't exact because of div count, let's locate line "Rayon minimal autorisé sans ovalisation nocive"
pos_rayon = code.find('Rayon minimal autorisé sans ovalisation nocive')
pos_cavalier = code.find('{activeTab === "cavalier" && (')

print("pos_rayon:", pos_rayon, "pos_cavalier:", pos_cavalier)

if pos_rayon != -1 and pos_cavalier != -1:
    bend_middle = code[pos_rayon:pos_cavalier]
    print("bend_middle original:\n", repr(bend_middle))
    # Replace bend_middle with clean closing:
    # </p> \n </div> \n </div> \n )} \n \n
    new_bend_middle = '''Rayon minimal autorisé sans ovalisation nocive ni plissement de génératrice (Fascicule 3).
            </p>
          </div>
        </div>
      )}

      '''
    code = code[:pos_rayon] + new_bend_middle + code[pos_cavalier:]

# ==============================================================================
# FIX 2: Carré Bleu closing (line 5340 area) & Carré Orange & Croquis Mode closing
# ==============================================================================
# Find Carré Bleu end before Carré Orange header
pos_carre_orange = code.find('Carré Orange — Cartouche Technique Normalisé Sonelgaz')
print("pos_carre_orange:", pos_carre_orange)

pos_massif_map_end = code.rfind('</g>', 0, pos_carre_orange)
print("pos_massif_map_end:", pos_massif_map_end)

# Let's inspect text between pos_massif_map_end and pos_carre_orange
print("Between massif end and carre orange:\n", repr(code[pos_massif_map_end:pos_carre_orange]))

# We want massif end to transition cleanly to Carré Orange:
clean_blue_to_orange = '''</g>
                                 );
                               })}
                             </svg>
                           );
                         })()}
                       </div>
                     </div>
          </div>

          {/* ========================================================================= */}
          {/* CARRÉ ORANGE (ORANGE BOX): SECTION CARTOUCHE TECHNIQUE (BLOCK 2)           */}
          {/* ========================================================================= */}
          <div className="w-full bg-slate-900 border-2 border-orange-500/80 rounded-3xl p-5 text-white space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-orange-500/30 pb-2 mb-2">
              <span className="text-xs font-black uppercase text-orange-400 tracking-wider flex items-center gap-2">
                <FileText className="w-4 h-4 text-orange-400" />
                <span>Carré Orange — Cartouche Technique Normalisé Sonelgaz (Block 2 d'Impression)</span>'''

# Replace from massif end to end of Carré Orange header span
end_orange_span = code.find('<span>Carré Orange — Cartouche Technique Normalisé Sonelgaz', pos_carre_orange) + len('<span>Carré Orange — Cartouche Technique Normalisé Sonelgaz')
code = code[:pos_massif_map_end] + clean_blue_to_orange + code[end_orange_span:]

# ==============================================================================
# FIX 3: End of Carré Orange before croquisMode === "libre"
# ==============================================================================
pos_libre = code.find('croquisMode === "libre" && (')
print("pos_libre:", pos_libre)

# Look backwards from pos_libre to find where Quantitatif Estimatif ends
pos_quant = code.rfind('Générer le Cartouche Technique & Imprimer', 0, pos_libre)
print("pos_quant:", pos_quant)

# Between pos_quant and pos_libre, make sure divs and braces close cleanly
clean_quant_to_libre = '''Générer le Cartouche Technique & Imprimer</span>
                            </button>
                          </div>
                        </div>
                      );
                    })()}
          </div>
        </div>
      )}

      {croquisMode === "libre" && ('''

code = code[:pos_quant] + clean_quant_to_libre + code[pos_libre + len('croquisMode === "libre" && ('):]

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fix script applied successfully.")
