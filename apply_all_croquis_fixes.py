import re

with open('src/components/Calculators.tsx', 'r') as f:
    code = f.read()

print("Applying Croquis fixes...")

# -----------------------------------------------------------------------------
# 1. Update handleDirectPrintCroquis to use A4 landscape page setup
# -----------------------------------------------------------------------------
old_page_style = """            @page {
              size: A4 portrait;
              margin: 10mm;
            }"""

new_page_style = """            @page {
              size: A4 landscape;
              margin: 6mm;
            }
            @media print {
              body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
              .container { max-width: 100% !important; width: 100% !important; border: none !important; padding: 0 !important; }
            }"""

if old_page_style in code:
    code = code.replace(old_page_style, new_page_style, 1)
    print("Updated handleDirectPrintCroquis page style to A4 landscape!")

# -----------------------------------------------------------------------------
# 2. Add Floating Zoom Controls & MouseWheel zoom handler to Parametric Canvas
# -----------------------------------------------------------------------------
old_canvas_container = """            <div 
                        className="relative w-full overflow-hidden bg-slate-950 rounded-b-xl border border-slate-800 shadow-2xl min-h-[580px] flex items-center justify-center p-2 select-none"
                        onMouseMove={(e) => {"""

new_canvas_container = """            <div 
                        className="relative w-full overflow-hidden bg-slate-950 rounded-b-xl border border-slate-800 shadow-2xl min-h-[580px] flex items-center justify-center p-2 select-none"
                        onWheel={(e) => {
                          e.preventDefault();
                          if (e.deltaY < 0) {
                            handleZoomIn();
                          } else {
                            handleZoomOut();
                          }
                        }}
                        onMouseMove={(e) => {"""

if old_canvas_container in code:
    code = code.replace(old_canvas_container, new_canvas_container, 1)
    print("Added onWheel zoom to Parametric Canvas container!")

# Add Floating Zoom Controls Bar overlaid on the top right of the Parametric Canvas
old_canvas_header = """            <div className="flex items-center justify-between border-b border-blue-500/30 pb-2 mb-2">
              <span className="text-xs font-black uppercase text-cyan-400 tracking-wider flex items-center gap-2">
                <Compass className="w-4 h-4 text-cyan-400" />
                <span>Carré Bleu — Espace de Dessin, Canvas et Édition Technique (Grand Format)</span>
              </span>
              <span className="text-[10px] bg-blue-950 text-blue-300 font-mono font-bold px-2.5 py-0.5 rounded border border-blue-800">
                Format d'Impression A3 (1189 x 841 mm)
              </span>
            </div>"""

new_canvas_header = """            <div className="flex flex-wrap items-center justify-between border-b border-blue-500/30 pb-2 mb-2 gap-2">
              <span className="text-xs font-black uppercase text-cyan-400 tracking-wider flex items-center gap-2">
                <Compass className="w-4 h-4 text-cyan-400" />
                <span>Carré Bleu — Espace de Dessin, Canvas et Édition Technique (Grand Format)</span>
              </span>

              {/* Floating Toolbar: Zoom + Wheel Scroll + Impression Paysage */}
              <div className="flex items-center gap-1.5 bg-slate-900/90 border border-cyan-500/40 p-1.5 rounded-2xl shadow-lg">
                <button
                  type="button"
                  onClick={handleZoomOut}
                  title="Zoom Arrière (-)"
                  className="w-7 h-7 flex items-center justify-center bg-slate-800 hover:bg-slate-700 text-cyan-300 rounded-xl font-bold transition-all border border-slate-700 cursor-pointer"
                >
                  <ZoomOut className="w-3.5 h-3.5" />
                </button>
                <span className="text-[11px] font-mono font-black text-cyan-300 px-1.5 min-w-[45px] text-center">
                  {Math.round(croquisZoom * 100)}%
                </span>
                <button
                  type="button"
                  onClick={handleZoomIn}
                  title="Zoom Avant (+)"
                  className="w-7 h-7 flex items-center justify-center bg-slate-800 hover:bg-slate-700 text-cyan-300 rounded-xl font-bold transition-all border border-slate-700 cursor-pointer"
                >
                  <ZoomIn className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={handleZoomReset}
                  title="Réinitialiser Zoom 100%"
                  className="px-2 py-1 text-[10px] font-mono font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl transition-all border border-slate-700 cursor-pointer flex items-center gap-1"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>100%</span>
                </button>
                <span className="text-[10px] font-mono text-slate-400 hidden sm:inline px-1">
                  (Molette 🖱️ Zoom)
                </span>
                <button
                  type="button"
                  onClick={handleDirectPrintCroquis}
                  title="Imprimer au format paysage (Cartouche à gauche, Dessin à droite)"
                  className="px-3 py-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white rounded-xl text-[10px] font-black shadow-sm transition-all flex items-center gap-1 cursor-pointer"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>🖨️ Imprimer (Paysage)</span>
                </button>
              </div>
            </div>"""

if old_canvas_header in code:
    code = code.replace(old_canvas_header, new_canvas_header, 1)
    print("Added Floating Zoom & Print Controls Header!")

# -----------------------------------------------------------------------------
# 3. Add Gates & Global Gabions Rendering inside Parametric SVG Canvas
# -----------------------------------------------------------------------------
target_svg_end = """                              {massifs.map((m) => {
                                const mW = m.length * scale;
                                const mH = m.width * scale;
                                const mX = cX + (m.xOffset * scale) - (mW / 2);
                                const mY = cY + (m.yOffset * scale) - (mH / 2);

                                return (
                                  <g key={m.id}>
                                    <rect
                                      x={mX}
                                      y={mY}
                                      width={mW}
                                      height={mH}
                                      fill="#451a03"
                                      stroke="#d97706"
                                      strokeWidth="1.5"
                                      rx="1"
                                    />
                                    <text x={mX + mW / 2} y={mY + mH / 2 + 3} fill="#fef3c7" fontSize="8" fontWeight="bold" textAnchor="middle">
                                      {m.name}
                                    </text>
                                  </g>
                                );
                              })}"""

replacement_svg_end = """                              {massifs.map((m) => {
                                const mW = m.length * scale;
                                const mH = m.width * scale;
                                const mX = cX + (m.xOffset * scale) - (mW / 2);
                                const mY = cY + (m.yOffset * scale) - (mH / 2);

                                return (
                                  <g key={m.id}>
                                    <rect
                                      x={mX}
                                      y={mY}
                                      width={mW}
                                      height={mH}
                                      fill="#451a03"
                                      stroke="#d97706"
                                      strokeWidth="1.5"
                                      rx="1"
                                    />
                                    <text x={mX + mW / 2} y={mY + mH / 2 + 3} fill="#fef3c7" fontSize="8" fontWeight="bold" textAnchor="middle">
                                      {m.name}
                                    </text>
                                  </g>
                                );
                              })}

                              {/* ==================== RENDERING PARAMETRIC GATES & PORTILLONS ==================== */}
                              {gates.map((g) => {
                                const isSelected = selectedGateId === g.id;
                                const isSmall = g.type === "portillon";
                                const mainOv = ouvrages[0] || { length: 35, width: 21, xOffset: 0, yOffset: 0 };
                                const ovW = mainOv.length * scale;
                                const ovH = mainOv.width * scale;
                                const ovX = cX + (mainOv.xOffset * scale) - (ovW / 2);
                                const ovY = cY + (mainOv.yOffset * scale) - (ovH / 2);

                                const gWidthPx = g.width * scale;
                                let px = ovX;
                                let py = ovY;

                                if (g.wall === "sud") {
                                  px = ovX + Math.min(ovW - gWidthPx, Math.max(0, g.offset * scale));
                                  py = ovY + ovH;
                                } else if (g.wall === "nord") {
                                  px = ovX + Math.min(ovW - gWidthPx, Math.max(0, g.offset * scale));
                                  py = ovY;
                                } else if (g.wall === "ouest") {
                                  px = ovX;
                                  py = ovY + Math.min(ovH - gWidthPx, Math.max(0, g.offset * scale));
                                } else if (g.wall === "est") {
                                  px = ovX + ovW;
                                  py = ovY + Math.min(ovH - gWidthPx, Math.max(0, g.offset * scale));
                                }

                                const isHoriz = g.wall === "sud" || g.wall === "nord";

                                return (
                                  <g
                                    key={g.id}
                                    className="cursor-pointer"
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      setSelectedGateId(g.id);
                                    }}
                                  >
                                    {isHoriz ? (
                                      <>
                                        <line x1={px} y1={py} x2={px + gWidthPx} y2={py} stroke="#090d16" strokeWidth="6" />
                                        <line x1={px} y1={py} x2={px + gWidthPx} y2={py} stroke={isSmall ? "#38bdf8" : "#0284c7"} strokeWidth="3" strokeDasharray="3 2" />
                                        <rect x={px - 4} y={py - 6} width="8" height="12" fill={isSmall ? "#38bdf8" : "#0284c7"} stroke="#ffffff" strokeWidth="1" rx="2" />
                                        <rect x={px + gWidthPx - 4} y={py - 6} width="8" height="12" fill={isSmall ? "#38bdf8" : "#0284c7"} stroke="#ffffff" strokeWidth="1" rx="2" />
                                        <path d={`M ${px} ${py} A ${gWidthPx/2} ${gWidthPx/2} 0 0 1 ${px + gWidthPx/2} ${py + 15}`} fill="none" stroke={isSmall ? "#38bdf8" : "#0284c7"} strokeWidth="1.2" strokeDasharray="2 2" />
                                        {!isSmall && (
                                          <path d={`M ${px + gWidthPx} ${py} A ${gWidthPx/2} ${gWidthPx/2} 0 0 0 ${px + gWidthPx/2} ${py + 15}`} fill="none" stroke="#0284c7" strokeWidth="1.2" strokeDasharray="2 2" />
                                        )}
                                        <rect x={px + gWidthPx/2 - 45} y={py + (g.wall === "nord" ? -22 : 18)} width="90" height="16" fill={isSelected ? "#0284c7" : "#0f172a"} stroke={isSelected ? "#38bdf8" : "#334155"} rx="4" />
                                        <text x={px + gWidthPx/2} y={py + (g.wall === "nord" ? -10 : 30)} fill="#38bdf8" fontSize="8" fontWeight="black" textAnchor="middle">
                                          {g.name} ({g.width}m)
                                        </text>
                                      </>
                                    ) : (
                                      <>
                                        <line x1={px} y1={py} x2={px} y2={py + gWidthPx} stroke="#090d16" strokeWidth="6" />
                                        <line x1={px} y1={py} x2={px} y2={py + gWidthPx} stroke={isSmall ? "#38bdf8" : "#0284c7"} strokeWidth="3" strokeDasharray="3 2" />
                                        <rect x={px - 6} y={py - 4} width="12" height="8" fill={isSmall ? "#38bdf8" : "#0284c7"} stroke="#ffffff" strokeWidth="1" rx="2" />
                                        <rect x={px - 6} y={py + gWidthPx - 4} width="12" height="8" fill={isSmall ? "#38bdf8" : "#0284c7"} stroke="#ffffff" strokeWidth="1" rx="2" />
                                        <rect x={px + (g.wall === "ouest" ? -95 : 10)} y={py + gWidthPx/2 - 8} width="85" height="16" fill={isSelected ? "#0284c7" : "#0f172a"} stroke={isSelected ? "#38bdf8" : "#334155"} rx="4" />
                                        <text x={px + (g.wall === "ouest" ? -52.5 : 52.5)} y={py + gWidthPx/2 + 3} fill="#38bdf8" fontSize="8" fontWeight="black" textAnchor="middle">
                                          {g.name} ({g.width}m)
                                        </text>
                                      </>
                                    )}
                                  </g>
                                );
                              })}

                              {/* ==================== RENDERING PARAMETRIC GLOBAL GABIONS ==================== */}
                              {hasGabions && (
                                <g>
                                  {(["nord", "sud", "est", "ouest"] as const).map((side) => {
                                    const gConf = gabionSideConfigs[side];
                                    if (!gConf || !gConf.enabled) return null;

                                    const mainOv = ouvrages[0] || { length: 35, width: 21, xOffset: 0, yOffset: 0 };
                                    const ovW = mainOv.length * scale;
                                    const ovH = mainOv.width * scale;
                                    const ovX = cX + (mainOv.xOffset * scale) - (ovW / 2);
                                    const ovY = cY + (mainOv.yOffset * scale) - (ovH / 2);

                                    const gDepth = (gConf.width || 1) * scale;
                                    const gLen = Math.min(side === "nord" || side === "sud" ? ovW : ovH, (gConf.length || 10) * scale);
                                    let gx = ovX, gy = ovY, gw = ovW, gh = ovH;

                                    if (side === "nord") { gy = ovY - gDepth - (gConf.offset * scale || 4); gh = gDepth; gw = gLen; }
                                    else if (side === "sud") { gy = ovY + ovH + (gConf.offset * scale || 4); gh = gDepth; gw = gLen; }
                                    else if (side === "ouest") { gx = ovX - gDepth - (gConf.offset * scale || 4); gw = gDepth; gh = gLen; }
                                    else if (side === "est") { gx = ovX + ovW + (gConf.offset * scale || 4); gw = gDepth; gh = gLen; }

                                    return (
                                      <g key={`global-gabion-${side}`}>
                                        <rect
                                          x={gx}
                                          y={gy}
                                          width={gw}
                                          height={gh}
                                          fill="url(#hatchGabion)"
                                          stroke="#f59e0b"
                                          strokeWidth="1.5"
                                          rx="2"
                                        />
                                        <text
                                          x={gx + gw / 2}
                                          y={gy + gh / 2 + 3}
                                          fill="#fbbf24"
                                          fontSize="8.5"
                                          fontWeight="black"
                                          textAnchor="middle"
                                        >
                                          Mur Gabion {side.toUpperCase()} ({gConf.etages} ET)
                                        </text>
                                      </g>
                                    );
                                  })}
                                </g>
                              )}"""

if target_svg_end in code:
    code = code.replace(target_svg_end, replacement_svg_end, 1)
    print("Added Gates and Global Gabions SVG rendering to Parametric mode!")

with open('src/components/Calculators.tsx', 'w') as f:
    f.write(code)

print("Finished script step 1!")
