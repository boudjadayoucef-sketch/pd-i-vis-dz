with open('src/components/Calculators.tsx', 'r') as f:
    code = f.read()

# Locate printAreaRef in Calculators.tsx
start_str = '<div ref={printAreaRef} className="bg-white p-6 border-2 border-slate-900 font-mono text-xs leading-relaxed max-w-4xl mx-auto text-slate-800 space-y-4">'

if start_str in code:
    print("Found printAreaRef start!")

new_print_area = """<div ref={printAreaRef} className="bg-white p-3 border-2 border-slate-900 font-mono text-xs leading-relaxed w-full text-slate-800">
                     <div className="border-2 border-slate-900 p-3 bg-white">
                       {/* ========================================================================= */}
                       {/* IMPRESSION LANDSCAPE (PAYSAGE A3/A4): CARTOUCHE A GAUCHE, DESSIN A DROITE */}
                       {/* ========================================================================= */}
                       <div className="flex flex-row gap-3 items-stretch min-h-[580px]">
                         
                         {/* LEFT COLUMN: SONELGAZ HEADER, CARTOUCHE & METRES TABLES (35% WIDTH) */}
                         <div className="w-[340px] shrink-0 flex flex-col justify-between border-r-2 border-slate-900 pr-3 space-y-2">
                           <div className="space-y-2">
                             {/* Official Sonelgaz Transport du Gaz Header */}
                             <SonelgazHeader />

                             <div className="text-center border border-slate-900 bg-slate-50 py-1.5 px-2">
                               <h2 className="text-[10px] font-black tracking-widest uppercase text-slate-900">
                                 PLAN D'IMPLANTATION & CARTOUCHE TECHNIQUE
                               </h2>
                               <p className="text-[8px] text-slate-600 uppercase mt-0.5">
                                 {conceptionMode === "neuf" ? "Ouvrage Neuf d'Origine" : "Extension sur Ouvrage Existant"} • Plan N° {cartoucheInfo.planNumber || "SONELGAZ-GC-001"}
                               </p>
                             </div>

                             {/* Cartouche Table */}
                             <table className="cartouche">
                               <tbody>
                                 <tr>
                                   <td className="w-1/2">
                                     <span className="label">Ouvrage :</span><br />
                                     <span className="value">{cartoucheInfo.postName}</span>
                                   </td>
                                   <td className="w-1/2">
                                     <span className="label">N° Plan & Rév :</span><br />
                                     <span className="value">{cartoucheInfo.planNumber} | {cartoucheInfo.revisionIndex}</span>
                                   </td>
                                 </tr>
                                 <tr>
                                   <td>
                                     <span className="label">Échelle & Date :</span><br />
                                     <span className="value">{cartoucheInfo.scale} | {cartoucheInfo.date}</span>
                                   </td>
                                   <td>
                                     <span className="label">Projet :</span><br />
                                     <span className="value">{conceptionMode === "neuf" ? "Neuf 100%" : "Extension"}</span>
                                   </td>
                                 </tr>
                                 <tr>
                                   <td>
                                     <span className="label">Dessiné par :</span><br />
                                     <span className="value text-[#007ac3] font-extrabold">{cartoucheInfo.editorName}</span>
                                   </td>
                                   <td>
                                     <span className="label">Vérifié par :</span><br />
                                     <span className="value text-[#007ac3] font-extrabold">{cartoucheInfo.verifierName}</span>
                                   </td>
                                 </tr>
                                 <tr>
                                   <td colSpan={2}>
                                     <span className="label">Approuvé par (Direction) :</span><br />
                                     <span className="value text-[#007ac3] font-extrabold">{cartoucheInfo.approverName}</span>
                                   </td>
                                 </tr>
                               </tbody>
                             </table>

                             {/* Summary Métrés Table */}
                             {(() => {
                               const totalSlabsConcrete = slabs.reduce((acc, s) => acc + (s.length * s.width * s.thickness), 0);
                               const teleShelterConcrete = teleShelterLength * teleShelterWidth * 0.20;
                               const nx = Math.max(2, Math.ceil(fenceA / 3));
                               const ny = Math.max(2, Math.ceil(fenceB / 3));
                               const postsCount = (nx + 1) * 2 + (ny - 1) * 2;
                               const footingsConcrete = postsCount * (0.80 * 0.80 * 0.80);
                               const totalConcrete = totalSlabsConcrete + teleShelterConcrete + footingsConcrete;

                               return (
                                 <div className="space-y-1">
                                   <span className="text-[8.5px] font-black uppercase text-slate-900 block border-b border-slate-900 pb-0.5">
                                     RÉSUMÉ SYNTÉTIQUE DES MÉTRÉS GC :
                                   </span>
                                   <table className="quantitatif-grid">
                                     <thead>
                                       <tr>
                                         <th>Désignation</th>
                                         <th style={{ textAlign: 'right' }}>Quantité</th>
                                       </tr>
                                     </thead>
                                     <tbody>
                                       <tr>
                                         <td>Blocs / Ouvrages GC</td>
                                         <td style={{ textAlign: 'right' }}><strong>{ouvrages.length} U</strong></td>
                                       </tr>
                                       <tr>
                                         <td>Dalles Béton Armé</td>
                                         <td style={{ textAlign: 'right' }}><strong>{slabs.length} U ({slabs.reduce((acc, s) => acc + s.length * s.width, 0).toFixed(1)} m²)</strong></td>
                                       </tr>
                                       <tr>
                                         <td>Volume Béton Total</td>
                                         <td style={{ textAlign: 'right' }}><strong>{totalConcrete.toFixed(2)} m³</strong></td>
                                       </tr>
                                       <tr>
                                         <td>Portails & Portillons</td>
                                         <td style={{ textAlign: 'right' }}><strong>{gates.length} U</strong></td>
                                       </tr>
                                       <tr>
                                         <td>Clôture Périmétrique</td>
                                         <td style={{ textAlign: 'right' }}><strong>{(fenceA * 2 + fenceB * 2).toFixed(1)} ml</strong></td>
                                       </tr>
                                     </tbody>
                                   </table>
                                 </div>
                               );
                             })()}

                             {/* Notes techniques */}
                             <div className="border border-slate-900 p-2 bg-slate-50 text-[7.5px] font-mono leading-tight space-y-1">
                               <p className="font-bold border-b border-slate-900 pb-0.5 text-slate-800">NOTES TECHNIQUES RÉGLEMENTAIRES :</p>
                               <p>1. Clôture H={fenceHeight}m avec fil barbelé et fer H.</p>
                               <p>2. Béton armé dosé à 350 kg/m³ CPA sur gravier compacté.</p>
                               <p>3. En cas d'extension, scellement par goujons résine époxy homologuée.</p>
                             </div>
                           </div>

                           {/* Visas & Signatures */}
                           <div className="border-t-2 border-slate-900 pt-1.5 grid grid-cols-2 gap-2 text-[7px] text-center">
                             <div className="border border-slate-900 p-1 h-12 flex flex-col justify-between">
                               <span className="font-bold uppercase text-slate-700">VISA INGÉNIEUR GC</span>
                               <span className="text-[6px] text-slate-400">Signature / Date</span>
                             </div>
                             <div className="border border-slate-900 p-1 h-12 flex flex-col justify-between">
                               <span className="font-bold uppercase text-slate-700">VISA CHEF DE PROJET</span>
                               <span className="text-[6px] text-slate-400">Signature / Cachet</span>
                             </div>
                           </div>
                         </div>

                         {/* RIGHT COLUMN: TECHNICAL DRAWING BLUEPRINT SVG (65% WIDTH) */}
                         <div className="flex-1 flex flex-col justify-between bg-white border border-slate-900 p-2 overflow-hidden">
                           <div className="text-center border-b border-slate-900 pb-1 mb-1">
                             <span className="text-[9.5px] font-black uppercase tracking-wider text-slate-900">
                               SCHÉMA TECHNIQUE CAD 2D — VUE EN PLAN D'IMPLANTATION
                             </span>
                           </div>

                           {/* Schematic drawing print copy */}
                           <div className="flex-1 flex justify-center items-center p-1 bg-white">"""

# Let's replace the start of printAreaRef up to the drawing container
idx1 = code.find(start_str)
idx2 = code.find('{croquisMode === "libre" ? (', idx1)

if idx1 != -1 and idx2 != -1:
    code = code[:idx1] + new_print_area + "\n" + code[idx2:]
    print("Replaced printAreaRef with Landscape layout (Cartouche left, drawing right)!")

with open('src/components/Calculators.tsx', 'w') as f:
    f.write(code)

print("Finished printAreaRef update!")
