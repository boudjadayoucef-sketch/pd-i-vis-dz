import sys

with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Cavalier tab wrapping fix
cavalier_old = '''      {activeTab === "cavalier" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in">'''

cavalier_new = '''      {activeTab === "cavalier" && (
        <div className="space-y-6 animate-fade-in">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">'''

code = code.replace(cavalier_old, cavalier_new)

# 2. Carré Bleu closing before Carré Orange
blue_end_old = '''                                     <text x={mX + mW / 2} y={mY + mH / 2 + 3} fill="#fef3c7" fontSize="8" fontWeight="bold" textAnchor="middle">
                                       {m.name}
                                     </text>
                                   </g>
                                 );
                               })}

                               
          </div>

          {/* ========================================================================= */}
          {/* CARRÉ ORANGE (ORANGE BOX): SECTION CARTOUCHE TECHNIQUE (BLOCK 2)           */}'''

blue_end_new = '''                                     <text x={mX + mW / 2} y={mY + mH / 2 + 3} fill="#fef3c7" fontSize="8" fontWeight="bold" textAnchor="middle">
                                       {m.name}
                                     </text>
                                   </g>
                                 );
                               })}
                             </svg>
                           );
                         })()}
                       </div>
                     </div>
          </div>

          {/* ========================================================================= */}
          {/* CARRÉ ORANGE (ORANGE BOX): SECTION CARTOUCHE TECHNIQUE (BLOCK 2)           */}'''

code = code.replace(blue_end_old, blue_end_new)

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fix script completed.")
