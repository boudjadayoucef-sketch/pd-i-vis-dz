with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Locate old modal start and replace with clean hidden printAreaRef container
old_modal_start = '''              {/* Print Blueprint Modal */}
              {showTechnicalReport && (
                <div className="bg-white rounded-3xl border border-slate-200 p-6 space-y-4 animate-fade-in relative shadow-xl max-w-4xl mx-auto z-40">
                   <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                     <div className="flex items-center gap-2">
                       <Compass className="w-5 h-5 text-orange-500" />
                       <span className="font-extrabold text-sm text-slate-800">Aperçu du Plan d'Implantation Technique & Cartouche</span>
                     </div>
                     <div className="flex gap-2">
                       <button
                         type="button"
                         onClick={() => {
                           const win = window.open("", "_blank");
                           if (win && printAreaRef.current) {
                             win.document.write(`
                               <html>
                                 <head>
                                   <title>Plan de Conception de Poste de Détente - SONELGAZ</title>
                                   <style>
                                     body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; padding: 30px; color: #0f172a; line-height: 1.4; }
                                     .container { width: 100%; max-width: 800px; margin: 0 auto; border: 2px solid #000; padding: 20px; box-sizing: border-box; }
                                     .header { display: flex; justify-content: space-between; align-items: center; border-b: 2px solid #000; padding-bottom: 12px; margin-bottom: 15px; }
                                     .header h1 { font-size: 14px; font-weight: 900; margin: 0; text-transform: uppercase; }
                                     .title-block { text-align: center; border: 1.5px solid #000; padding: 10px; font-weight: bold; background-color: #f1f5f9; text-transform: uppercase; font-size: 11px; margin-bottom: 15px; }
                                     .drawing-area { text-align: center; border: 1.5px solid #000; padding: 15px; background-color: #fff; margin-bottom: 15px; min-height: 250px; }
                                     .drawing-area svg { width: 100%; height: auto; max-height: 280px; }
                                     .notes-block { border: 1.5px solid #000; padding: 10px; font-size: 8px; font-family: monospace; line-height: 1.3; margin-bottom: 15px; background-color: #fafafa; }
                                     .cartouche { width: 100%; border-collapse: collapse; border: 2px solid #000; margin-top: 15px; }
                                     .cartouche td { border: 1px solid #000; padding: 6px; font-size: 8px; font-family: monospace; vertical-align: top; }
                                     .cartouche .label { font-weight: bold; text-transform: uppercase; color: #475569; }
                                     .cartouche .value { font-weight: 900; font-size: 9px; color: #000; }
                                   </style>
                                 </head>
                                 <body>
                                   <div class="container">${printAreaRef.current.innerHTML}</div>
                                   <script>window.print();</script>
                                 </body>
                               </html>
                             `);
                             win.document.close();
                           }
                         }}
                         className="px-3 py-1.5 bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5"
                       >
                         <Printer className="w-3.5 h-3.5" />
                         <span>Imprimer le Plan</span>
                       </button>
                       <button
                         type="button"
                         onClick={() => setShowTechnicalReport(false)}
                         className="px-3 py-1.5 bg-slate-100 text-slate-700 hover:bg-slate-200 rounded-lg text-xs font-bold transition-all"
                       >
                         Fermer
                       </button>
                     </div>
                   </div>

                   {/* Intervenants & Cartouche Metadata Editor */}
                   <div className="bg-slate-100 p-4 rounded-xl border border-slate-300 space-y-3 font-sans max-w-4xl mx-auto">
                     <h4 className="text-xs font-black uppercase text-blue-900 tracking-wider flex items-center gap-1.5">
                       <FileText className="w-4 h-4 text-blue-700" />
                       <span>Renseignements du Cartouche Technique & Intervenants Plan</span>
                     </h4>
                     <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                       <div>
                         <label className="text-[10px] font-bold text-slate-600 block mb-1">Éditeur / Établi par :</label>
                         <input
                           type="text"
                           value={cartoucheInfo.editorName}
                           onChange={(e) => setCartoucheInfo(prev => ({ ...prev, editorName: e.target.value }))}
                           className="w-full text-xs font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                         />
                       </div>
                       <div>
                         <label className="text-[10px] font-bold text-slate-600 block mb-1">Vérificateur / Vérifié par :</label>
                         <input
                           type="text"
                           value={cartoucheInfo.verifierName}
                           onChange={(e) => setCartoucheInfo(prev => ({ ...prev, verifierName: e.target.value }))}
                           className="w-full text-xs font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                         />
                       </div>
                       <div>
                         <label className="text-[10px] font-bold text-slate-600 block mb-1">Approuvé par :</label>
                         <input
                           type="text"
                           value={cartoucheInfo.approverName}
                           onChange={(e) => setCartoucheInfo(prev => ({ ...prev, approverName: e.target.value }))}
                           className="w-full text-xs font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                         />
                       </div>
                     </div>
                     <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                       <div>
                         <label className="text-[10px] font-bold text-slate-600 block mb-1">Nom du Poste / Ouvrage :</label>
                         <input
                           type="text"
                           value={cartoucheInfo.postName}
                           onChange={(e) => setCartoucheInfo(prev => ({ ...prev, postName: e.target.value }))}
                           className="w-full text-xs font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                         />
                       </div>
                       <div>
                         <label className="text-[10px] font-bold text-slate-600 block mb-1">N° du Plan :</label>
                         <input
                           type="text"
                           value={cartoucheInfo.planNumber}
                           onChange={(e) => setCartoucheInfo(prev => ({ ...prev, planNumber: e.target.value }))}
                           className="w-full text-xs font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                         />
                       </div>
                       <div>
                         <label className="text-[10px] font-bold text-slate-600 block mb-1">Indice de Révision :</label>
                         <input
                           type="text"
                           value={cartoucheInfo.revisionIndex}
                           onChange={(e) => setCartoucheInfo(prev => ({ ...prev, revisionIndex: e.target.value }))}
                           className="w-full text-xs font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                         />
                       </div>
                       <div>
                         <label className="text-[10px] font-bold text-slate-600 block mb-1">Échelle :</label>
                         <input
                           type="text"
                           value={cartoucheInfo.scale}
                           onChange={(e) => setCartoucheInfo(prev => ({ ...prev, scale: e.target.value }))}
                           className="w-full text-xs font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1.5"
                         />
                       </div>
                     </div>
                   </div>

                   {/* Printable Area Wrapper */}
                   <div ref={printAreaRef} className="bg-slate-50/55 rounded-2xl p-6 border border-slate-150 font-mono text-xs leading-relaxed max-w-4xl mx-auto text-slate-800">'''

new_printable_start = '''              {/* Hidden Printable Area Container (Targeted by Direct Print / Export PDF) */}
              <div className="hidden">
                <div ref={printAreaRef} className="bg-white p-6 border-2 border-slate-900 font-mono text-xs leading-relaxed max-w-4xl mx-auto text-slate-800 space-y-4">'''

if old_modal_start in code:
    code = code.replace(old_modal_start, new_printable_start)
    print("Replaced modal start with clean hidden printAreaRef container.")
else:
    print("Could not match old_modal_start precisely.")

# Also remove the ending </div> </div> )} around line 7038
old_modal_end = '''                  </div>
               </div>
             )}
          </div>
        )}'''

new_modal_end = '''                  </div>
              </div>
          </div>
        )}'''

if old_modal_end in code:
    code = code.replace(old_modal_end, new_modal_end)
    print("Replaced modal end successfully.")
else:
    print("Could not match old_modal_end precisely.")

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
