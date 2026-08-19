with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Locate massifs mapping end in Carré Bleu
target = '''                                     <text x={mX + mW / 2} y={mY + mH / 2 + 3} fill="#fef3c7" fontSize="8" fontWeight="bold" textAnchor="middle">
                                       {m.name}
                                     </text>
                                   </g>
                                 );
                               })}'''

replacement = '''                                     <text x={mX + mW / 2} y={mY + mH / 2 + 3} fill="#fef3c7" fontSize="8" fontWeight="bold" textAnchor="middle">
                                       {m.name}
                                     </text>
                                   </g>
                                 );
                               })}
                             </svg>
                           );
                         })()}
                       </div>
                     </div>'''

if target in code:
    code = code.replace(target, replacement)
    with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Carré Bleu closing tags added successfully.")
else:
    print("Target not found. Let's inspect target string.")
