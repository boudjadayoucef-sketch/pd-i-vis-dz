import sys
import re

with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update BENDING Section
bend_target = '''            <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100 flex flex-col justify-between">
              <div className="space-y-4">
                <span className="text-[10px] font-black uppercase text-slate-400 tracking-wider">Spécifications de Cintrage</span>
                
                <div>
                  <p className="text-xs text-slate-500">Plaque de gabarit de vérification minimale :</p>
                  <p className="text-lg font-bold text-slate-800 mt-1">{currentBending.gaugePlateDiameter} mm</p>
                </div>

                <div>
                  <p className="text-xs text-slate-500 font-semibold text-slate-600">Rayon minimal de cintrage réglementaire à froid :</p>
                  <p className="text-4xl font-black text-blue-600 mt-1 flex items-baseline gap-1">
                    <span>{currentBendingRadius}</span>
                    <span className="text-sm font-normal text-slate-500">Mètres</span>
                  </p>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-200 text-[10px] text-slate-400">
                Conforme à l'Annexe 12, Fascicule 7, Page 138.
              </div>
            </div>
          </div>
        )}'''

bend_replacement = '''            <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100 flex flex-col justify-between">
              <div className="space-y-4">
                <span className="text-[10px] font-black uppercase text-slate-400 tracking-wider">Spécifications de Cintrage</span>
                
                <div>
                  <p className="text-xs text-slate-500">Plaque de gabarit de vérification minimale :</p>
                  <p className="text-lg font-bold text-slate-800 mt-1">{currentBending.gaugePlateDiameter} mm</p>
                </div>

                <div>
                  <p className="text-xs text-slate-500 font-semibold text-slate-600">Rayon minimal de cintrage réglementaire à froid :</p>
                  <p className="text-4xl font-black text-blue-600 mt-1 flex items-baseline gap-1">
                    <span>{currentBendingRadius}</span>
                    <span className="text-sm font-normal text-slate-500">Mètres</span>
                  </p>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-200 text-[10px] text-slate-400">
                Conforme à l'Annexe 12, Fascicule 7, Page 138.
              </div>
            </div>
          </div>

          {/* SCHÉMA TECHNIQUE DESSIN INTERACTIF — CINTRAGE À FROID (FASC. 3) */}
          <div className="bg-slate-900 rounded-2xl p-5 text-white border border-slate-800 space-y-4 shadow-xl">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-amber-400" />
                <h4 className="text-xs font-black uppercase tracking-wider text-amber-400">
                  Schéma Cinématique & Machine — Cintrage à Froid sur Chantier (Fasc. 3)
                </h4>
              </div>
              <span className="text-[10px] bg-amber-950 text-amber-300 font-mono font-bold px-3 py-1 rounded-full border border-amber-800/80 self-start sm:self-auto">
                DN {currentBending.diameterInches} | e = {selectedThickness} mm | Gabarit Ø {currentBending.gaugePlateDiameter} mm
              </span>
            </div>

            <div className="w-full bg-slate-950 rounded-xl p-4 border border-slate-800/80 flex justify-center items-center overflow-x-auto">
              <svg viewBox="0 0 840 320" className="w-full max-w-4xl h-auto">
                <defs>
                  <pattern id="gridBending" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" strokeWidth="0.5"/>
                  </pattern>
                  <linearGradient id="pipeArcGrad" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#38bdf8"/>
                    <stop offset="50%" stopColor="#fbbf24"/>
                    <stop offset="100%" stopColor="#38bdf8"/>
                  </linearGradient>
                </defs>
                <rect width="840" height="320" fill="url(#gridBending)" />

                {/* Machine Frame / Base */}
                <rect x="60" y="250" width="720" height="20" fill="#334155" rx="4"/>
                <text x="420" y="265" fill="#94a3b8" fontSize="10" fontWeight="bold" textAnchor="middle">
                  BANC DE CINTRAGE HYDRAULIQUE SUR CHANTIER
                </text>

                {/* Left Support Die */}
                <path d="M 120 250 L 140 200 L 180 200 L 200 250 Z" fill="#475569" stroke="#94a3b8" strokeWidth="1.5"/>
                <circle cx="160" cy="200" r="12" fill="#64748b"/>

                {/* Right Support Die */}
                <path d="M 640 250 L 660 200 L 700 200 L 720 250 Z" fill="#475569" stroke="#94a3b8" strokeWidth="1.5"/>
                <circle cx="680" cy="200" r="12" fill="#64748b"/>

                {/* Curved Bent Pipe Arc */}
                <path d="M 100 220 Q 420 80 740 220" stroke="url(#pipeArcGrad)" strokeWidth="18" fill="none" strokeLinecap="round"/>
                <path d="M 100 220 Q 420 80 740 220" stroke="#0284c7" strokeWidth="10" fill="none" strokeLinecap="round"/>

                {/* Center Hydraulic Bending Ram */}
                <rect x="390" y="20" width="60" height="50" rx="4" fill="#0284c7" stroke="#38bdf8" strokeWidth="2"/>
                <text x="420" y="42" fill="#ffffff" fontSize="9" fontWeight="900" textAnchor="middle">VÉRIN</text>
                
                {/* Piston Rod pushing down */}
                <rect x="412" y="70" width="16" height="50" fill="#cbd5e1"/>
                <polygon points="420,130 405,115 435,115" fill="#ef4444"/>
                <text x="450" y="95" fill="#ef4444" fontSize="10" fontWeight="bold">Effort F (kN)</text>

                {/* Curvature Radius Line to Center */}
                <line x1="420" y1="280" x2="420" y2="135" stroke="#f59e0b" strokeWidth="2" strokeDasharray="4 2"/>
                <polygon points="420,135 414,145 426,145" fill="#f59e0b"/>
                
                <rect x="300" y="165" width="240" height="30" rx="8" fill="#0f172a" stroke="#f59e0b" strokeWidth="2"/>
                <text x="420" y="184" fill="#f59e0b" fontSize="13" fontWeight="900" textAnchor="middle">
                  RAYON R MIN = {currentBendingRadius} MÈTRES
                </text>

                {/* Gauge Plate Verification Badge */}
                <g transform="translate(620, 40)">
                  <rect x="0" y="0" width="170" height="60" rx="8" fill="#1e1b4b" stroke="#818cf8" strokeWidth="1.5"/>
                  <text x="85" y="22" fill="#a5b4fc" fontSize="9" fontWeight="bold" textAnchor="middle">PLAQUE DE GABARIT</text>
                  <text x="85" y="44" fill="#ffffff" fontSize="14" fontWeight="900" textAnchor="middle">Ø {currentBending.gaugePlateDiameter} mm</text>
                </g>
              </svg>
            </div>
            <p className="text-[10px] text-slate-400 text-center italic">
              Rayon minimal autorisé sans ovalisation nocive ni plissement de génératrice (Fascicule 3).
            </p>
          </div>
        </div>
      )}'''

code = code.replace(bend_target, bend_replacement)
print("Bending schematic replaced.")

# 2. Update CAVALIER Section
cav_target = '''                <div className="text-[10px] text-slate-400 leading-relaxed bg-white p-2.5 rounded-lg border border-slate-200">
                  <span className="font-bold">Note de calcul (p. 152) :</span> Le lestage doit garantir une flottabilité négative d'au moins 10% par rapport au volume déplacé.
                </div>
              </div>
            </div>
          </div>
        )}'''

cav_replacement = '''                <div className="text-[10px] text-slate-400 leading-relaxed bg-white p-2.5 rounded-lg border border-slate-200">
                  <span className="font-bold">Note de calcul (p. 152) :</span> Le lestage doit garantir une flottabilité négative d'au moins 10% par rapport au volume déplacé.
                </div>
              </div>
            </div>
          </div>

          {/* SCHÉMA TECHNIQUE DESSIN INTERACTIF — LESTAGE & CAVALIER (FASC. 7) */}
          <div className="bg-slate-900 rounded-2xl p-5 text-white border border-slate-800 space-y-4 shadow-xl">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Waves className="w-5 h-5 text-blue-400" />
                <h4 className="text-xs font-black uppercase tracking-wider text-blue-400">
                  Schéma de Principe & Coupe — Lestage par Cavaliers en Béton Armé (Fasc. 7)
                </h4>
              </div>
              <span className="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-3 py-1 rounded-full border border-blue-800/80 self-start sm:self-auto">
                Spacement Max X = {maxSpacingX > 0 ? `${maxSpacingX.toFixed(2)} m` : "Calcul N/A"} | K = {K_factor}
              </span>
            </div>

            <div className="w-full bg-slate-950 rounded-xl p-4 border border-slate-800/80 flex justify-center items-center overflow-x-auto">
              <svg viewBox="0 0 840 340" className="w-full max-w-4xl h-auto">
                <defs>
                  <pattern id="gridCavalier" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" strokeWidth="0.5"/>
                  </pattern>
                  <linearGradient id="waterGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#0284c7" stopOpacity="0.4"/>
                    <stop offset="100%" stopColor="#075985" stopOpacity="0.8"/>
                  </linearGradient>
                </defs>
                <rect width="840" height="340" fill="url(#gridCavalier)" />

                {/* Water Table Submerged Layer */}
                <rect x="40" y="60" width="760" height="210" fill="url(#waterGrad)" rx="8"/>
                <line x1="40" y1="75" x2="800" y2="75" stroke="#38bdf8" strokeWidth="2" strokeDasharray="8 4"/>
                <text x="60" y="68" fill="#38bdf8" fontSize="10" fontWeight="bold">NIVEAU DE LA NAPPE PHRÉATIQUE / OUED EN CRUE</text>

                {/* Pipeline Longitudinal Axis */}
                <rect x="40" y="160" width="760" height="36" fill="#334155" stroke="#94a3b8" strokeWidth="2.5" rx="4"/>
                <line x1="40" y1="178" x2="800" y2="178" stroke="#38bdf8" strokeWidth="1.5" strokeDasharray="6 3"/>
                <text x="420" y="182" fill="#ffffff" fontSize="11" fontWeight="900" textAnchor="middle">
                  GAZODUC REVÊTU Ø {pipeDiameterWithCoating} m
                </text>

                {/* Concrete Saddle 1 (Left) */}
                <g transform="translate(180, 115)">
                  <path d="M 0 0 L 70 0 L 70 110 L 52 110 L 52 75 L 18 75 L 18 110 L 0 110 Z" fill="#78716c" stroke="#f59e0b" strokeWidth="2"/>
                  <text x="35" y="-10" fill="#fef08a" fontSize="10" fontWeight="bold" textAnchor="middle">Cavalier 1</text>
                  <text x="35" y="45" fill="#ffffff" fontSize="9" fontWeight="bold" textAnchor="middle">{cavalierVolume} m³</text>
                </g>

                {/* Concrete Saddle 2 (Right) */}
                <g transform="translate(590, 115)">
                  <path d="M 0 0 L 70 0 L 70 110 L 52 110 L 52 75 L 18 75 L 18 110 L 0 110 Z" fill="#78716c" stroke="#f59e0b" strokeWidth="2"/>
                  <text x="35" y="-10" fill="#fef08a" fontSize="10" fontWeight="bold" textAnchor="middle">Cavalier 2</text>
                  <text x="35" y="45" fill="#ffffff" fontSize="9" fontWeight="bold" textAnchor="middle">{cavalierVolume} m³</text>
                </g>

                {/* Upward Archimedes Buoyancy Force Arrow */}
                <g transform="translate(420, 210)">
                  <line x1="0" y1="35" x2="0" y2="5" stroke="#06b6d4" strokeWidth="3"/>
                  <polygon points="0,0 -6,10 6,10" fill="#06b6d4"/>
                  <text x="0" y="50" fill="#6ee7b7" fontSize="10" fontWeight="extrabold" textAnchor="middle">Poussée d'Archimède (Fa)</text>
                </g>

                {/* Downward Gravity Force Arrows */}
                <g transform="translate(215, 230)">
                  <line x1="0" y1="0" x2="0" y2="25" stroke="#ef4444" strokeWidth="2.5"/>
                  <polygon points="0,30 -5,20 5,20" fill="#ef4444"/>
                  <text x="0" y="42" fill="#fca5a5" fontSize="9" textAnchor="middle">Poids (P1)</text>
                </g>
                <g transform="translate(625, 230)">
                  <line x1="0" y1="0" x2="0" y2="25" stroke="#ef4444" strokeWidth="2.5"/>
                  <polygon points="0,30 -5,20 5,20" fill="#ef4444"/>
                  <text x="0" y="42" fill="#fca5a5" fontSize="9" textAnchor="middle">Poids (P2)</text>
                </g>

                {/* Max Distance Spacing Arrow X */}
                <line x1="215" y1="295" x2="625" y2="295" stroke="#f59e0b" strokeWidth="2.5"/>
                <polygon points="215,295 225,290 225,300" fill="#f59e0b"/>
                <polygon points="625,295 615,290 615,300" fill="#f59e0b"/>
                
                <rect x="300" y="280" width="240" height="28" rx="8" fill="#0f172a" stroke="#f59e0b" strokeWidth="2"/>
                <text x="420" y="299" fill="#f59e0b" fontSize="12" fontWeight="900" textAnchor="middle">
                  DISTANCE MAX X = {maxSpacingX > 0 ? `${maxSpacingX.toFixed(2)} MÈTRES` : "N/A"}
                </text>
              </svg>
            </div>
            <p className="text-[10px] text-slate-400 text-center italic">
              Équilibre de stabilité sous coefficient de sécurité K = {K_factor} (Annexe Fascicule 7 Sonelgaz).
            </p>
          </div>
        </div>
      )}'''

code = code.replace(cav_target, cav_replacement)
print("Cavalier schematic replaced.")

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
