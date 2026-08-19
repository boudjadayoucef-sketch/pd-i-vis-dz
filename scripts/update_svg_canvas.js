import fs from 'fs';

const filePath = 'src/components/Calculators.tsx';
let content = fs.readFileSync(filePath, 'utf-8').replace(/\r\n/g, '\n');

const startMarker = `                      const tooltipData: { [key: string]: { title: string; desc: string } } = {`;
const endMarker = `                                <div className="flex justify-end pt-2 border-t border-slate-200">
                                  <button
                                    type="button"
                                    onClick={() => setShowTechnicalReport(true)}`;

const startIndex = content.indexOf(startMarker);
const endIndex = content.indexOf(endMarker);

if (startIndex === -1 || endIndex === -1) {
  console.error("Markers not found!", startIndex, endIndex);
  process.exit(1);
}

const replacementCode = `                      const tooltipData: { [key: string]: { title: string; desc: string } } = {
                        fence: {
                          title: "Clôture en Panneaux Profilés (Cornières e=12mm inter-axe)",
                          desc: \`Panneaux profilés électrosoudés de hauteur \${fenceHeight}m constitués de cornières métalliques en L avec un espacement rigoureux de 12 mm inter-axe, fixés sur poteaux Fer H enterrés dans des semelles béton 80cm x 80cm avec fil barbelé supérieur.\`
                        },
                        portail_5m: {
                          title: "Portail 2 Vantaux (Largeur 5.00m)",
                          desc: \`Portail d'accès principal 2 vantaux battants en acier galvanisé profilé de largeur 5.00 ml et hauteur \${fenceHeight}m, équipé de serrure de sécurité, d'arrêt de battant et verrous de sol pour véhicules lourds.\`
                        },
                        portillon_1m: {
                          title: "Portillon Piéton (Largeur 1.00m)",
                          desc: \`Portillon d'accès piéton 1 vantail battant en acier galvanisé profilé de largeur 1.00 ml et hauteur \${fenceHeight}m, pour le passage sécurisé des agents d'exploitation Sonelgaz.\`
                        },
                        tele_shelter: {
                          title: \`Abri de Télé-exploitation (\${teleShelterType === "01_porte" ? "01 Porte" : "02 Portes"})\`,
                          desc: \`Bâtiment maçonné fermé de \${teleShelterLength}m x \${teleShelterWidth}m abritant les armoires de télétransmission, calculateurs de débit gaz et alimentations de secours. Comporte \${teleShelterType === "01_porte" ? "1 porte blindée d'accès" : "2 portes d'accès indépendantes"}.\`
                        },
                        poste_detente: {
                          title: "Dalle Poste de Détente",
                          desc: "Béton armé d'épaisseur 25cm dosé à 350kg/m³ de ciment CPA. Supporte les collecteurs d'entrée (HP), filtres régulateurs et détendeurs de pression."
                        },
                        rechaffeur: {
                          title: "Dalle Réchauffeur de Gaz",
                          desc: "Dalle béton isolée sous réchauffeur de gaz pour prévenir l'effet Joule-Thomson. Résistance thermique et chimique."
                        },
                        gare_racleur_arrivee: {
                          title: "Dalle Gare Racleur (Arrivée)",
                          desc: "Dalle renforcée pour le sas de réception des racleurs (pigs). Dispositifs d'ancrage et bac de rétention des condensats."
                        },
                        gare_racleur_depart: {
                          title: "Dalle Gare Racleur (Départ)",
                          desc: "Dalle renforcée sous le sas de lancement des racleurs. Zone classée ATEX avec prise de terre directe."
                        },
                        epandage_assiette: {
                          title: "Épandage / Assiette Béton",
                          desc: "Zone d'épandage en béton gravillonné / dalle d'assiette pour la rétention et l'évacuation des eaux pluviales et fluides."
                        },
                        abri_tele: {
                          title: "Dalle Bâtiment Télé-exploitation",
                          desc: "Dalle béton armé étanche sous le bâtiment télécom/télétransmission."
                        }
                      };

                      // Helper to render gate openings on the chosen face
                      const renderGates = () => {
                        const gatesList = [];

                        // Gate side parameters
                        let pStartX = fX;
                        let pStartY = fY;
                        let isHorizontal = true;

                        if (gateSide === "sud") {
                          pStartY = fY + fH;
                          pStartX = fX + Math.min(portailOffset, fenceA - 5) * scale;
                        } else if (gateSide === "nord") {
                          pStartY = fY;
                          pStartX = fX + Math.min(portailOffset, fenceA - 5) * scale;
                        } else if (gateSide === "est") {
                          pStartX = fX + fW;
                          pStartY = fY + Math.min(portailOffset, fenceB - 5) * scale;
                          isHorizontal = false;
                        } else if (gateSide === "ouest") {
                          pStartX = fX;
                          pStartY = fY + Math.min(portailOffset, fenceB - 5) * scale;
                          isHorizontal = false;
                        }

                        // Portail 2 Vantaux 5m
                        if (nbPortails5m > 0) {
                          const w5 = 5 * scale;
                          if (isHorizontal) {
                            gatesList.push(
                              <g key="portail-5m" className="cursor-pointer group" onClick={() => setActiveTooltipCroquis("portail_5m")}>
                                {/* Gate opening gap on fence */}
                                <rect x={pStartX} y={pStartY - 3} width={w5} height="6" fill="#0f172a" />
                                {/* Two door leaves 2.5m each */}
                                <line x1={pStartX} y1={pStartY} x2={pStartX + w5 / 2} y2={pStartY + (gateSide === "sud" ? 18 : -18)} stroke="#f59e0b" strokeWidth="2.5" />
                                <line x1={pStartX + w5} y1={pStartY} x2={pStartX + w5 / 2} y2={pStartY + (gateSide === "sud" ? 18 : -18)} stroke="#f59e0b" strokeWidth="2.5" />
                                {/* Opening swing arcs */}
                                <path d={\`M \${pStartX + w5 / 2} \${pStartY + (gateSide === "sud" ? 18 : -18)} A \${w5 / 2} \${w5 / 2} 0 0 1 \${pStartX} \${pStartY}\`} stroke="#f59e0b" strokeDasharray="3 2" fill="none" strokeWidth="1" />
                                <path d={\`M \${pStartX + w5 / 2} \${pStartY + (gateSide === "sud" ? 18 : -18)} A \${w5 / 2} \${w5 / 2} 0 0 0 \${pStartX + w5} \${pStartY}\`} stroke="#f59e0b" strokeDasharray="3 2" fill="none" strokeWidth="1" />
                                {/* Gate posts */}
                                <rect x={pStartX - 3} y={pStartY - 4} width="6" height="8" fill="#f59e0b" rx="1" />
                                <rect x={pStartX + w5 - 3} y={pStartY - 4} width="6" height="8" fill="#f59e0b" rx="1" />
                                <text x={pStartX + w5 / 2} y={pStartY + (gateSide === "sud" ? 28 : -22)} fill="#f59e0b" className="font-mono text-[7px] font-black" textAnchor="middle">
                                  PORTAIL 2 BATTANTS (5.00m x H={fenceHeight}m)
                                </text>
                              </g>
                            );
                          } else {
                            gatesList.push(
                              <g key="portail-5m" className="cursor-pointer group" onClick={() => setActiveTooltipCroquis("portail_5m")}>
                                <rect x={pStartX - 3} y={pStartY} width="6" height={w5} fill="#0f172a" />
                                <line x1={pStartX} y1={pStartY} x2={pStartX + (gateSide === "est" ? 18 : -18)} y2={pStartY + w5 / 2} stroke="#f59e0b" strokeWidth="2.5" />
                                <line x1={pStartX} y1={pStartY + w5} x2={pStartX + (gateSide === "est" ? 18 : -18)} y2={pStartY + w5 / 2} stroke="#f59e0b" strokeWidth="2.5" />
                                <rect x={pStartX - 4} y={pStartY - 3} width="8" height="6" fill="#f59e0b" rx="1" />
                                <rect x={pStartX - 4} y={pStartY + w5 - 3} width="8" height="6" fill="#f59e0b" rx="1" />
                                <text x={pStartX + (gateSide === "est" ? 26 : -26)} y={pStartY + w5 / 2 + 2} fill="#f59e0b" className="font-mono text-[6.5px] font-black" textAnchor="middle">
                                  PORTAIL 5m
                                </text>
                              </g>
                            );
                          }
                        }

                        // Portillon 1m
                        let poStartX = fX;
                        let poStartY = fY;
                        if (gateSide === "sud") {
                          poStartY = fY + fH;
                          poStartX = fX + Math.min(portillonOffset, fenceA - 1) * scale;
                        } else if (gateSide === "nord") {
                          poStartY = fY;
                          poStartX = fX + Math.min(portillonOffset, fenceA - 1) * scale;
                        } else if (gateSide === "est") {
                          poStartX = fX + fW;
                          poStartY = fY + Math.min(portillonOffset, fenceB - 1) * scale;
                        } else if (gateSide === "ouest") {
                          poStartX = fX;
                          poStartY = fY + Math.min(portillonOffset, fenceB - 1) * scale;
                        }

                        if (nbPortillons1m > 0) {
                          const w1 = 1 * scale;
                          if (isHorizontal) {
                            gatesList.push(
                              <g key="portillon-1m" className="cursor-pointer group" onClick={() => setActiveTooltipCroquis("portillon_1m")}>
                                <rect x={poStartX} y={poStartY - 3} width={Math.max(w1, 8)} height="6" fill="#0f172a" />
                                <line x1={poStartX} y1={poStartY} x2={poStartX + Math.max(w1, 8)} y2={poStartY + (gateSide === "sud" ? 12 : -12)} stroke="#06b6d4" strokeWidth="2" />
                                <rect x={poStartX - 2} y={poStartY - 3} width="4" height="6" fill="#06b6d4" rx="1" />
                                <rect x={poStartX + Math.max(w1, 8) - 2} y={poStartY - 3} width="4" height="6" fill="#06b6d4" rx="1" />
                                <text x={poStartX + Math.max(w1, 8) / 2} y={poStartY + (gateSide === "sud" ? 20 : -14)} fill="#06b6d4" className="font-mono text-[6.5px] font-black" textAnchor="middle">
                                  PORTILLON 1m
                                </text>
                              </g>
                            );
                          } else {
                            gatesList.push(
                              <g key="portillon-1m" className="cursor-pointer group" onClick={() => setActiveTooltipCroquis("portillon_1m")}>
                                <rect x={poStartX - 3} y={poStartY} width="6" height={Math.max(w1, 8)} fill="#0f172a" />
                                <line x1={poStartX} y1={poStartY} x2={poStartX + (gateSide === "est" ? 12 : -12)} y2={poStartY + Math.max(w1, 8)} stroke="#06b6d4" strokeWidth="2" />
                                <rect x={poStartX - 3} y={poStartY - 2} width="6" height="4" fill="#06b6d4" rx="1" />
                                <rect x={poStartX - 3} y={poStartY + Math.max(w1, 8) - 2} width="6" height="4" fill="#06b6d4" rx="1" />
                                <text x={poStartX + (gateSide === "est" ? 18 : -18)} y={poStartY + Math.max(w1, 8) / 2 + 2} fill="#06b6d4" className="font-mono text-[6px] font-black" textAnchor="middle">
                                  PORTILLON 1m
                                </text>
                              </g>
                            );
                          }
                        }

                        return gatesList;
                      };

                      return (
                        <div className="space-y-4">
                          {/* Banner for Drag and Drop & Cornière details */}
                          <div className="flex flex-wrap items-center justify-between gap-2 bg-slate-950/90 text-slate-200 px-3.5 py-2 rounded-xl border border-slate-800 text-[10px]">
                            <span className="flex items-center gap-2 font-bold text-cyan-300">
                              <Move className="w-4 h-4 text-cyan-400 animate-pulse" />
                              <span>Déplacement interactif : Glissez-déposez n'importe quelle dalle directement sur le plan!</span>
                            </span>
                            <span className="font-mono text-[9.5px] bg-blue-950 text-blue-300 px-2 py-0.5 rounded border border-blue-800 font-extrabold">
                              Panneaux Profilés : Cornières 12mm inter-axe
                            </span>
                          </div>

                          <div className="bg-slate-900 border border-slate-950 rounded-2xl overflow-hidden shadow-2xl relative select-none">
                            <svg
                              viewBox={\`0 0 \${svgW} \${svgH}\`}
                              className="w-full h-auto touch-none"
                              onPointerMove={(e) => {
                                if (draggingSlabId && dragStartPos) {
                                  const dxPx = e.clientX - dragStartPos.pointerX;
                                  const dyPx = e.clientY - dragStartPos.pointerY;
                                  const dxM = dxPx / scale;
                                  const dyM = dyPx / scale;

                                  const activeSlab = slabs.find(s => s.id === draggingSlabId);
                                  if (activeSlab) {
                                    let newX = Math.round((dragStartPos.initX + dxM) * 10) / 10;
                                    let newY = Math.round((dragStartPos.initY + dyM) * 10) / 10;

                                    newX = Math.max(0, Math.min(fenceA - activeSlab.length, newX));
                                    newY = Math.max(0, Math.min(fenceB - activeSlab.width, newY));

                                    handleUpdateSlab(draggingSlabId, "xOffset", newX);
                                    handleUpdateSlab(draggingSlabId, "yOffset", newY);
                                  }
                                }
                              }}
                              onPointerUp={() => {
                                setDraggingSlabId(null);
                                setDragStartPos(null);
                              }}
                              onPointerCancel={() => {
                                setDraggingSlabId(null);
                                setDragStartPos(null);
                              }}
                            >
                              <defs>
                                <pattern id="blueprint-grid" width="15" height="15" patternUnits="userSpaceOnUse">
                                  <rect width="15" height="15" fill="#0f172a" />
                                  <path d="M 15 0 L 0 0 0 15" fill="none" stroke="#1e293b" strokeWidth="0.5" />
                                </pattern>
                              </defs>
                              <rect width={svgW} height={svgH} fill="url(#blueprint-grid)" />

                              {/* Center grid axes */}
                              <line x1={cX} y1="10" x2={cX} y2={svgH - 10} stroke="#475569" strokeWidth="0.5" strokeDasharray="5 3" />
                              <line x1="10" y1={cY} x2={svgW - 10} y2={cY} stroke="#475569" strokeWidth="0.5" strokeDasharray="5 3" />

                              {/* Fence Panel Mesh Outline */}
                              <rect
                                x={fX}
                                y={fY}
                                width={fW}
                                height={fH}
                                fill="none"
                                stroke="#3b82f6"
                                strokeWidth="2.5"
                                strokeDasharray="6 3"
                                className="cursor-pointer hover:stroke-cyan-400 transition-colors"
                                onClick={() => setActiveTooltipCroquis("fence")}
                              />
                              <text x={fX + 10} y={fY + 16} fill="#38bdf8" className="font-mono text-[8px] uppercase font-black tracking-wider">
                                Clôture Panneaux Profilés H={fenceHeight}m ({fenceA}m x {fenceB}m) - Cornières e=12mm inter-axe + Barbelé
                              </text>

                              {/* Cornière detail callout badge */}
                              <g transform={\`translate(\${fX + fW - 175}, \${fY + 8})\`}>
                                <rect width="170" height="16" fill="#0284c7" fillOpacity="0.85" rx="3" stroke="#38bdf8" strokeWidth="0.8" />
                                <text x="85" y="11" fill="#ffffff" className="font-mono text-[6.5px] font-black" textAnchor="middle">
                                  ÉLÉMENT PROFILÉ : CORNIÈRES 12mm INTER-AXE
                                </text>
                              </g>

                              {/* Render Gates (Portail 5m & Portillon 1m) */}
                              {renderGates()}

                              {/* Fence Posts (Fer H with 80x80cm Footing) */}
                              {fencePosts.map((post, idx) => (
                                <g key={idx} onClick={() => setActiveTooltipCroquis("fence")}>
                                  <rect
                                    x={post.x - 0.4 * scale}
                                    y={post.y - 0.4 * scale}
                                    width={0.8 * scale}
                                    height={0.8 * scale}
                                    fill="#475569"
                                    fillOpacity="0.4"
                                    stroke="#94a3b8"
                                    strokeWidth="0.5"
                                  />
                                  <rect
                                    x={post.x - 2}
                                    y={post.y - 2}
                                    width="4"
                                    height="4"
                                    fill="#38bdf8"
                                  />
                                </g>
                              ))}

                              {/* Abri Télé-exploitation Building */}
                              <g
                                className="cursor-pointer group"
                                onClick={() => setActiveTooltipCroquis("tele_shelter")}
                              >
                                <rect
                                  x={tX}
                                  y={tY}
                                  width={tW}
                                  height={tH}
                                  fill={teleShelterIsExtension ? "#ea580c" : "#10b981"}
                                  fillOpacity={teleShelterIsExtension ? "0.35" : "0.45"}
                                  stroke={teleShelterIsExtension ? "#ea580c" : "#34d399"}
                                  strokeWidth="2"
                                  strokeDasharray={teleShelterIsExtension ? "4 2" : "none"}
                                  className="group-hover:fill-opacity-65 transition-all"
                                />
                                <rect x={tX + 3} y={tY + 3} width={tW - 6} height={tH - 6} fill="none" stroke="#059669" strokeWidth="0.6" strokeDasharray="2 2" />

                                {teleShelterType === "01_porte" ? (
                                  <g>
                                    <rect x={tX + tW / 2 - 5} y={tY + tH - 3} width="10" height="3" fill="#f59e0b" stroke="#fff" strokeWidth="0.5" />
                                    <text x={tX + tW / 2} y={tY + tH + 8} fill="#f59e0b" className="font-mono text-[6px] font-black" textAnchor="middle">1 Porte</text>
                                  </g>
                                ) : (
                                  <g>
                                    <rect x={tX + tW / 3 - 4} y={tY + tH - 3} width="8" height="3" fill="#f59e0b" stroke="#fff" strokeWidth="0.5" />
                                    <rect x={tX + (tW * 2) / 3 - 4} y={tY + tH - 3} width="8" height="3" fill="#f59e0b" stroke="#fff" strokeWidth="0.5" />
                                    <text x={tX + tW / 2} y={tY + tH + 8} fill="#f59e0b" className="font-mono text-[6px] font-black" textAnchor="middle">2 Portes</text>
                                  </g>
                                )}

                                <text x={tX + tW / 2} y={tY + tH / 2 + 2} fill="#ffffff" className="font-sans text-[7px] font-black uppercase" textAnchor="middle">
                                  {teleShelterIsExtension ? "[EXT] Abri Télé" : "Abri Télé-Exploitation"}
                                </text>
                              </g>

                              {/* Dynamic Drag-and-Drop Slabs Render */}
                              {slabs.map((slab) => {
                                const sW = slab.length * scale;
                                const sH = slab.width * scale;
                                const sX = fX + slab.xOffset * scale;
                                const sY = fY + slab.yOffset * scale;
                                const isExt = conceptionMode === "extension" && slab.isExtension;
                                const style = getSlabStyle(slab.type, isExt);
                                const isSelected = selectedSlabId === slab.id;
                                const isDragging = draggingSlabId === slab.id;

                                return (
                                  <g
                                    key={slab.id}
                                    className="cursor-move group"
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      setSelectedSlabId(slab.id);
                                      setActiveTooltipCroquis(slab.type);
                                    }}
                                    onPointerDown={(e) => {
                                      e.stopPropagation();
                                      try {
                                        e.currentTarget.setPointerCapture(e.pointerId);
                                      } catch (_) {}
                                      setSelectedSlabId(slab.id);
                                      setDraggingSlabId(slab.id);
                                      setDragStartPos({
                                        pointerX: e.clientX,
                                        pointerY: e.clientY,
                                        initX: slab.xOffset,
                                        initY: slab.yOffset
                                      });
                                    }}
                                  >
                                    <rect
                                      x={sX}
                                      y={sY}
                                      width={sW}
                                      height={sH}
                                      fill={style.fill}
                                      fillOpacity={isSelected || isDragging ? 0.75 : style.fillOpacity}
                                      stroke={isDragging ? "#38bdf8" : isSelected ? "#ffffff" : style.stroke}
                                      strokeWidth={isSelected || isDragging ? 2.5 : style.strokeWidth}
                                      strokeDasharray={style.dash}
                                      className="transition-all duration-100"
                                    />

                                    {/* Dragging or Selected indicator handles */}
                                    {(isSelected || isDragging) && (
                                      <g>
                                        <rect x={sX - 3} y={sY - 3} width="6" height="6" fill="#38bdf8" />
                                        <rect x={sX + sW - 3} y={sY - 3} width="6" height="6" fill="#38bdf8" />
                                        <rect x={sX - 3} y={sY + sH - 3} width="6" height="6" fill="#38bdf8" />
                                        <rect x={sX + sW - 3} y={sY + sH - 3} width="6" height="6" fill="#38bdf8" />
                                        
                                        {/* Floating position pill */}
                                        <rect x={sX + sW / 2 - 40} y={sY - 18} width="80" height="14" fill="#0284c7" rx="3" stroke="#38bdf8" strokeWidth="0.8" />
                                        <text x={sX + sW / 2} y={sY - 8} fill="#ffffff" className="font-mono text-[7px] font-black" textAnchor="middle">
                                          X:{slab.xOffset}m | Y:{slab.yOffset}m
                                        </text>
                                      </g>
                                    )}

                                    {/* Internal piping/symbol graphics per slab type */}
                                    {slab.type === "poste_detente" && (
                                      <>
                                        <line x1={sX + 8} y1={sY + sH / 2} x2={sX + sW - 8} y2={sY + sH / 2} stroke="#38bdf8" strokeWidth="1.5" />
                                        <circle cx={sX + sW / 3} cy={sY + sH / 2} r="3" fill="#ea580c" />
                                        <circle cx={sX + (sW * 2) / 3} cy={sY + sH / 2} r="3" fill="#10b981" />
                                      </>
                                    )}

                                    {slab.type === "rechaffeur" && (
                                      <path d={\`M \${sX + sW/2} \${sY + sH/2 - 4} L \${sX + sW/2 + 4} \${sY + sH/2 + 4} L \${sX + sW/2 - 4} \${sY + sH/2 + 4} Z\`} fill="#f59e0b" />
                                    )}

                                    {(slab.type === "gare_racleur_arrivee" || slab.type === "gare_racleur_depart") && (
                                      <>
                                        <line x1={sX + 8} y1={sY + sH / 3} x2={sX + sW - 8} y2={sY + sH / 3} stroke="#c084fc" strokeWidth="1.2" />
                                        <line x1={sX + 8} y1={sY + (sH * 2) / 3} x2={sX + sW - 8} y2={sY + (sH * 2) / 3} stroke="#c084fc" strokeWidth="1.2" />
                                        <rect x={sX + 6} y={sY + sH / 3 - 3} width="6" height="6" fill="#eab308" rx="1" />
                                      </>
                                    )}

                                    {/* Dimension Cotes */}
                                    <line x1={sX} y1={sY - 4} x2={sX + sW} y2={sY - 4} stroke="#f59e0b" strokeWidth="0.8" />
                                    <text x={sX + sW / 2} y={sY - 6} fill="#f59e0b" className="font-mono text-[6.5px] font-black" textAnchor="middle">
                                      {slab.length}m
                                    </text>

                                    <line x1={sX - 4} y1={sY} x2={sX - 4} y2={sY + sH} stroke="#f59e0b" strokeWidth="0.8" />
                                    <text x={sX - 6} y={sY + sH / 2 + 2} fill="#f59e0b" className="font-mono text-[6.5px] font-black" textAnchor="end">
                                      {slab.width}m
                                    </text>

                                    {/* Label badge */}
                                    <text x={sX + 5} y={sY + 11} fill="#ffffff" className="font-sans font-black text-[6px] uppercase">
                                      {isExt ? \`[EXT] \${slab.name}\` : slab.name} ({slab.thickness}m)
                                    </text>
                                  </g>
                                );
                              })}
                            </svg>
                          </div>

                          {/* Active Click Hotspot Info Banner */}
                          {activeTooltipCroquis && tooltipData[activeTooltipCroquis] && (
                            <div className="bg-blue-950 border border-blue-800 p-4 rounded-xl text-white space-y-1 animate-fade-in shadow-md">
                              <div className="flex items-center justify-between border-b border-blue-800/80 pb-1.5">
                                <span className="font-black text-xs text-blue-300 uppercase flex items-center gap-1.5">
                                  <Info className="w-4 h-4 text-cyan-400" />
                                  <span>{tooltipData[activeTooltipCroquis].title}</span>
                                </span>
                                <button
                                  type="button"
                                  onClick={() => setActiveTooltipCroquis(null)}
                                  className="text-slate-400 hover:text-white text-xs font-bold"
                                >
                                  ✕
                                </button>
                              </div>
                              <p className="text-xs text-slate-300 leading-relaxed pt-1">
                                {tooltipData[activeTooltipCroquis].desc}
                              </p>
                            </div>
                          )}

                          {/* Total Quantities & Materials Calculations Card */}
                          {(() => {
                            const totalSlabsConcrete = slabs.reduce((acc, s) => acc + (s.length * s.width * s.thickness), 0);
                            const teleShelterConcrete = teleShelterLength * teleShelterWidth * 0.20;
                            const totalFootingsCount = fencePosts.length;
                            const footingsConcrete = totalFootingsCount * (0.80 * 0.80 * 0.80); // 80x80x80cm footings
                            const totalConcrete = totalSlabsConcrete + teleShelterConcrete + footingsConcrete;

                            const totalCementBags = Math.ceil((totalConcrete * 350) / 50);
                            const totalSlabsArea = slabs.reduce((acc, s) => acc + (s.length * s.width), 0);

                            return (
                              <div className="bg-slate-50 border border-slate-200 p-5 rounded-2xl space-y-4">
                                <div className="flex items-center justify-between">
                                  <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider flex items-center gap-1.5">
                                    <Construction className="w-4 h-4 text-orange-600" />
                                    <span>Quantitatif Estimatif du Génie Civil & Équipements</span>
                                  </h4>
                                  <span className="text-[10px] bg-orange-100 text-orange-800 font-extrabold px-2 py-0.5 rounded-full border border-orange-200">
                                    Norme Sonelgaz CPA 350kg/m³
                                  </span>
                                </div>

                                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                  <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
                                    <span className="text-[9px] font-bold text-slate-400 uppercase block">Surface Dalles :</span>
                                    <span className="text-base font-black text-slate-800 font-mono">{totalSlabsArea.toFixed(1)} m²</span>
                                    <span className="text-[9px] text-slate-500 block mt-0.5">{slabs.length} dalle(s) active(s)</span>
                                  </div>

                                  <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
                                    <span className="text-[9px] font-bold text-slate-400 uppercase block">Volume Béton Armé :</span>
                                    <span className="text-base font-black text-blue-700 font-mono">{totalConcrete.toFixed(2)} m³</span>
                                    <span className="text-[9px] text-slate-500 block mt-0.5">Dalles + Semelles 80x80</span>
                                  </div>

                                  <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
                                    <span className="text-[9px] font-bold text-slate-400 uppercase block">Besoins en Ciment :</span>
                                    <span className="text-base font-black text-orange-600 font-mono">{totalCementBags} Sacs</span>
                                    <span className="text-[9px] text-slate-500 block mt-0.5">{(totalCementBags * 50 / 1000).toFixed(2)} Tonnes CPA</span>
                                  </div>

                                  <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
                                    <span className="text-[9px] font-bold text-amber-600 uppercase block">Portails & Accès :</span>
                                    <span className="text-xs font-black text-amber-900 block font-mono">{nbPortails5m}x Portail 5m | {nbPortillons1m}x Portillon 1m</span>
                                    <span className="text-[9px] text-slate-500 block mt-0.5">Façade {gateSide.toUpperCase()} (H={fenceHeight}m)</span>
                                  </div>
                                </div>

                                <div className="flex justify-end pt-2 border-t border-slate-200">
                                  <button
                                    type="button"
                                    onClick={() => setShowTechnicalReport(true)}`;

content = content.substring(0, startIndex) + replacementCode + content.substring(endIndex + endMarker.length);

fs.writeFileSync(filePath, content, 'utf-8');
console.log("Successfully updated SVG canvas!");
