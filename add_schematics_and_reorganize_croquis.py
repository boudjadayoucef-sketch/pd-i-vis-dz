import sys
import re

with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update EMPRISE Section to include Interactive SVG Schema
emp_old = '''activeTab === "emprise" && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-fade-in">'''

emp_new = '''activeTab === "emprise" && (
          <div className="space-y-6 animate-fade-in">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">'''

code = code.replace(emp_old, emp_new)

# Locate end of emprise section to append schematic
emp_end_target = '''              <div className="mt-6 pt-4 border-t border-slate-200">
                <p className="text-xs text-slate-500">Largeur totale d'emprise de la piste :</p>
                <p className="text-3xl font-black text-blue-600 mt-1">{RIGHT_OF_WAY_TABLE[selectedRowIndex].total} mètres</p>
              </div>
            </div>
          </div>
        )}'''

emp_end_replacement = '''              <div className="mt-6 pt-4 border-t border-slate-200">
                <p className="text-xs text-slate-500">Largeur totale d'emprise de la piste :</p>
                <p className="text-3xl font-black text-blue-600 mt-1">{RIGHT_OF_WAY_TABLE[selectedRowIndex].total} mètres</p>
              </div>
            </div>
          </div>

          {/* SCHÉMA TECHNIQUE DESSIN INTERACTIF — EMPRISE DE PISTE (FASC. 2) */}
          <div className="bg-slate-900 rounded-2xl p-5 text-white border border-slate-800 space-y-4 shadow-xl">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Sliders className="w-5 h-5 text-cyan-400" />
                <h4 className="text-xs font-black uppercase tracking-wider text-cyan-400">
                  Schéma & Dessin Technique de Profil — Emprise de Piste (Fasc. 2)
                </h4>
              </div>
              <span className="text-[10px] bg-cyan-950 text-cyan-300 font-mono font-bold px-3 py-1 rounded-full border border-cyan-800/80 self-start sm:self-auto">
                Tube Ø {RIGHT_OF_WAY_TABLE[selectedRowIndex].diameterInches} ({RIGHT_OF_WAY_TABLE[selectedRowIndex].diameterMm} mm)
              </span>
            </div>

            <div className="w-full bg-slate-950 rounded-xl p-4 border border-slate-800/80 flex justify-center items-center overflow-x-auto">
              <svg viewBox="0 0 840 340" className="w-full max-w-4xl h-auto">
                <defs>
                  <pattern id="gridEmprise" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" strokeWidth="0.5"/>
                  </pattern>
                  <linearGradient id="groundGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#334155"/>
                    <stop offset="100%" stopColor="#0f172a"/>
                  </linearGradient>
                  <linearGradient id="pipeMetalGrad" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stopColor="#38bdf8"/>
                    <stop offset="50%" stopColor="#0284c7"/>
                    <stop offset="100%" stopColor="#0369a1"/>
                  </linearGradient>
                  <linearGradient id="spoilGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#d97706"/>
                    <stop offset="100%" stopColor="#78350f"/>
                  </linearGradient>
                </defs>
                
                {/* Background Grid */}
                <rect width="840" height="340" fill="url(#gridEmprise)" />

                {/* Sky / Air label */}
                <text x="50" y="30" fill="#64748b" fontSize="10" fontWeight="bold">SURFACE DU SOL NATUREL</text>

                {/* Natural Ground Surface line */}
                <path d="M 40 180 L 260 180 Q 280 180 290 180 M 470 180 L 800 180" stroke="#94a3b8" strokeWidth="2.5" fill="none" strokeDasharray="6 3"/>
                <rect x="40" y="180" width="760" height="100" fill="url(#groundGrad)" opacity="0.35"/>

                {/* Excavated Trench (Tranchée au centre) */}
                <polygon points="290,180 310,245 450,245 470,180" fill="#020617" stroke="#38bdf8" strokeWidth="2.5"/>
                
                {/* Trench Sand Bedding */}
                <rect x="315" y="235" width="130" height="10" fill="#f59e0b" opacity="0.4" rx="2"/>

                {/* Pipeline inside Trench */}
                <circle cx="380" cy="210" r="23" fill="url(#pipeMetalGrad)" stroke="#ffffff" strokeWidth="2"/>
                <circle cx="380" cy="210" r="16" fill="none" stroke="#0f172a" strokeWidth="2"/>
                <text x="380" y="214" fill="#ffffff" fontSize="9" fontWeight="900" textAnchor="middle">
                  {RIGHT_OF_WAY_TABLE[selectedRowIndex].diameterInches}
                </text>

                {/* Spoil Heap / Merlon de déblais (Cordon D) on the left */}
                <path d="M 80 180 Q 150 100 220 180 Z" fill="url(#spoilGrad)" opacity="0.8" stroke="#f59e0b" strokeWidth="2"/>
                <text x="150" y="145" fill="#fef08a" fontSize="11" fontWeight="bold" textAnchor="middle">
                  Déblais (D) = {RIGHT_OF_WAY_TABLE[selectedRowIndex].d}m
                </text>
                <text x="150" y="162" fill="#fde68a" fontSize="9" textAnchor="middle">Stockage terre meuble</text>

                {/* Working Track (Bande B) on the right */}
                <rect x="490" y="175" width="290" height="10" fill="#10b981" rx="2"/>
                <text x="635" y="162" fill="#6ee7b7" fontSize="11" fontWeight="bold" textAnchor="middle">
                  Piste de Travail (B) = {RIGHT_OF_WAY_TABLE[selectedRowIndex].b}m
                </text>
                <text x="635" y="145" fill="#a7f3d0" fontSize="9" textAnchor="middle">Passage engins & bardage</text>

                {/* Left Servitude (C) */}
                <line x1="220" y1="170" x2="290" y2="170" stroke="#93c5fd" strokeWidth="1.5" strokeDasharray="3 2"/>
                <text x="255" y="162" fill="#93c5fd" fontSize="10" fontWeight="bold" textAnchor="middle">
                  C = {RIGHT_OF_WAY_TABLE[selectedRowIndex].c}m
                </text>

                {/* Trench Depth Indicator */}
                <line x1="475" y1="180" x2="475" y2="245" stroke="#a855f7" strokeWidth="1.5" strokeDasharray="2 2"/>
                <text x="490" y="215" fill="#c084fc" fontSize="9" fontWeight="bold">H ≥ 1.0 m</text>

                {/* Boundary Safety Fence Left & Right */}
                <line x1="40" y1="140" x2="40" y2="180" stroke="#ef4444" strokeWidth="3"/>
                <circle cx="40" cy="140" r="4" fill="#ef4444"/>
                <text x="40" y="130" fill="#fca5a5" fontSize="9" textAnchor="middle" fontWeight="bold">Limite Emprise</text>

                <line x1="800" y1="140" x2="800" y2="180" stroke="#ef4444" strokeWidth="3"/>
                <circle cx="800" cy="140" r="4" fill="#ef4444"/>
                <text x="800" y="130" fill="#fca5a5" fontSize="9" textAnchor="middle" fontWeight="bold">Limite Emprise</text>

                {/* Dimension Line Total A */}
                <line x1="40" y1="290" x2="800" y2="290" stroke="#38bdf8" strokeWidth="2.5"/>
                <polygon points="40,290 50,285 50,295" fill="#38bdf8"/>
                <polygon points="800,290 790,285 790,295" fill="#38bdf8"/>
                
                <rect x="290" y="276" width="260" height="28" rx="8" fill="#0f172a" stroke="#38bdf8" strokeWidth="2"/>
                <text x="420" y="295" fill="#38bdf8" fontSize="13" fontWeight="900" textAnchor="middle">
                  LARGEUR TOTALE (A) = {RIGHT_OF_WAY_TABLE[selectedRowIndex].total} MÈTRES
                </text>
              </svg>
            </div>
            <p className="text-[10px] text-slate-400 text-center italic">
              Conforme à l'Abaque Réglementaire Fascicule 2 — Pistes de Travail et Servitudes Gazoducs Sonelgaz.
            </p>
          </div>
        </div>
      )}'''

code = code.replace(emp_end_target, emp_end_replacement)

print("Emprise schematic updated.")

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
