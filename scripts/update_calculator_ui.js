import fs from 'fs';

const filePath = 'src/components/Calculators.tsx';
let content = fs.readFileSync(filePath, 'utf-8');

// 1. Update Clôture Panneaux Profilés sidebar section + Add Portails & Portillons Section
const oldFenceSidebar = `<div className="bg-blue-50/70 p-2.5 rounded-xl border border-blue-100 text-[10px] text-slate-600 leading-relaxed">
                        Panneaux profilés électrosoudés (long. 3m) avec fil barbelé supérieur. Poteaux Fer H scellés dans semelles béton <strong>80x80cm</strong>.
                      </div>`;

const newFenceSidebar = `<div className="bg-slate-900 text-blue-300 p-2.5 rounded-xl border border-blue-900 text-[10px] space-y-1">
                        <div className="flex items-center justify-between font-black text-white">
                          <span>Structure Panneau Profilé</span>
                          <span className="bg-blue-600 text-white font-mono text-[9px] px-1.5 py-0.5 rounded font-extrabold">12 mm inter-axe</span>
                        </div>
                        <p className="text-[9.5px] leading-relaxed text-slate-300">
                          Panneaux profilés électrosoudés (long. 3m) constitués de cornières métalliques en L avec un espacement rigoureux de <strong>12 mm inter-axe</strong> entre 2 cornières. Poteaux Fer H scellés dans semelles béton <strong>80x80cm</strong>.
                        </p>
                      </div>`;

content = content.replace(oldFenceSidebar, newFenceSidebar);

// Add Gates/Portails section right after fence section and before Abri Télé-exploitation
const fenceEndMarker = `                      </div>
                    </div>

                    {/* Abri de Télé-exploitation */}`;

const gatesSidebarCode = `                      </div>
                    </div>

                    {/* Portails & Portillons d'Accès Clôture */}
                    <div className="space-y-3 pt-4 border-t border-slate-200">
                      <div className="flex justify-between items-center">
                        <span className="text-[11px] font-black text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                          <DoorOpen className="w-4 h-4 text-amber-600" />
                          <span>Portails & Portillons (H={fenceHeight}m)</span>
                        </span>
                        <span className="font-mono text-amber-700 font-extrabold text-xs bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                          {nbPortails5m}x 5m | {nbPortillons1m}x 1m
                        </span>
                      </div>

                      {/* Façade Selection */}
                      <div className="space-y-1">
                        <label className="block text-[9.5px] font-bold text-slate-500">Façade d'installation des accès :</label>
                        <div className="grid grid-cols-4 gap-1">
                          {(["sud", "nord", "est", "ouest"] as const).map((side) => (
                            <button
                              key={side}
                              type="button"
                              onClick={() => setGateSide(side)}
                              className={\`py-1 text-center text-[10px] font-extrabold uppercase rounded border transition-all \${
                                gateSide === side
                                  ? "bg-amber-600 text-white border-amber-600 shadow-xs"
                                  : "bg-white text-slate-700 border-slate-200 hover:bg-slate-100"
                              }\`}
                            >
                              {side}
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Portail 2 vantaux 5m */}
                      <div className="bg-amber-50/70 p-2.5 rounded-xl border border-amber-200 space-y-2">
                        <div className="flex items-center justify-between">
                          <div>
                            <span className="text-xs font-black text-amber-900 block">Portail 2 Vantaux (5.00 ml)</span>
                            <span className="text-[9px] text-amber-700">Largeur = 5.00m | Hauteur = {fenceHeight}m</span>
                          </div>
                          <div className="flex items-center gap-1.5">
                            <button
                              type="button"
                              onClick={() => setNbPortails5m(prev => Math.max(0, prev - 1))}
                              className="w-6 h-6 rounded bg-amber-200 hover:bg-amber-300 font-bold text-amber-900 text-xs flex items-center justify-center"
                            >
                              -
                            </button>
                            <span className="font-mono font-black text-xs w-4 text-center">{nbPortails5m}</span>
                            <button
                              type="button"
                              onClick={() => setNbPortails5m(prev => prev + 1)}
                              className="w-6 h-6 rounded bg-amber-200 hover:bg-amber-300 font-bold text-amber-900 text-xs flex items-center justify-center"
                            >
                              +
                            </button>
                          </div>
                        </div>
                        {nbPortails5m > 0 && (
                          <div className="space-y-1 pt-1 border-t border-amber-200/60">
                            <div className="flex justify-between text-[9px] text-amber-800 font-bold">
                              <span>Position sur façade ({portailOffset} m) :</span>
                            </div>
                            <input
                              type="range"
                              min="1"
                              max={Math.max(2, (gateSide === "sud" || gateSide === "nord" ? fenceA : fenceB) - 6)}
                              value={portailOffset}
                              onChange={(e) => setPortailOffset(parseFloat(e.target.value))}
                              className="w-full accent-amber-600"
                            />
                          </div>
                        )}
                      </div>

                      {/* Portillon piéton 1m */}
                      <div className="bg-cyan-50/70 p-2.5 rounded-xl border border-cyan-200 space-y-2">
                        <div className="flex items-center justify-between">
                          <div>
                            <span className="text-xs font-black text-cyan-900 block">Portillon Piéton (1.00 ml)</span>
                            <span className="text-[9px] text-cyan-700">Largeur = 1.00m | Hauteur = {fenceHeight}m</span>
                          </div>
                          <div className="flex items-center gap-1.5">
                            <button
                              type="button"
                              onClick={() => setNbPortillons1m(prev => Math.max(0, prev - 1))}
                              className="w-6 h-6 rounded bg-cyan-200 hover:bg-cyan-300 font-bold text-cyan-900 text-xs flex items-center justify-center"
                            >
                              -
                            </button>
                            <span className="font-mono font-black text-xs w-4 text-center">{nbPortillons1m}</span>
                            <button
                              type="button"
                              onClick={() => setNbPortillons1m(prev => prev + 1)}
                              className="w-6 h-6 rounded bg-cyan-200 hover:bg-cyan-300 font-bold text-cyan-900 text-xs flex items-center justify-center"
                            >
                              +
                            </button>
                          </div>
                        </div>
                        {nbPortillons1m > 0 && (
                          <div className="space-y-1 pt-1 border-t border-cyan-200/60">
                            <div className="flex justify-between text-[9px] text-cyan-800 font-bold">
                              <span>Position sur façade ({portillonOffset} m) :</span>
                            </div>
                            <input
                              type="range"
                              min="0"
                              max={Math.max(1, (gateSide === "sud" || gateSide === "nord" ? fenceA : fenceB) - 2)}
                              value={portillonOffset}
                              onChange={(e) => setPortillonOffset(parseFloat(e.target.value))}
                              className="w-full accent-cyan-600"
                            />
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Abri de Télé-exploitation */}`;

content = content.replace(fenceEndMarker, gatesSidebarCode);

fs.writeFileSync(filePath, content, 'utf-8');
console.log("Updated sidebar controls!");
