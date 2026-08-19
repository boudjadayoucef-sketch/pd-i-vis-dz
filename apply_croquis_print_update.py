import re

with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add handleDirectPrintCroquis function declaration
handler_code = '''  const handleDirectPrintCroquis = () => {
    if (!printAreaRef.current) return;
    const win = window.open("", "_blank");
    if (!win) return;

    const content = printAreaRef.current.innerHTML;

    win.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <base href="${window.location.origin}/" />
          <meta charset="utf-8" />
          <title>Plan_Technique_Sonelgaz_${cartoucheInfo.planNumber || "GC-001"}</title>
          <style>
            @page {
              size: A4 portrait;
              margin: 10mm;
            }
            body {
              font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
              color: #0f172a;
              margin: 0;
              padding: 0;
              background: #ffffff;
              -webkit-print-color-adjust: exact;
              print-color-adjust: exact;
            }
            .container {
              width: 100%;
              max-width: 800px;
              margin: 0 auto;
              border: 2px solid #0f172a;
              padding: 16px;
              box-sizing: border-box;
            }
            .cartouche {
              width: 100%;
              border-collapse: collapse;
              border: 2px solid #0f172a;
              margin-top: 10px;
            }
            .cartouche td {
              border: 1px solid #0f172a;
              padding: 5px 8px;
              font-size: 8.5px;
              font-family: monospace;
              vertical-align: top;
            }
            .cartouche .label {
              font-weight: bold;
              text-transform: uppercase;
              color: #475569;
            }
            .cartouche .value {
              font-weight: 900;
              font-size: 9.5px;
              color: #000000;
            }
            .quantitatif-grid {
              width: 100%;
              border-collapse: collapse;
              border: 1.5px solid #0f172a;
              margin-top: 10px;
              font-size: 8.5px;
              font-family: monospace;
            }
            .quantitatif-grid td, .quantitatif-grid th {
              border: 1px solid #0f172a;
              padding: 5px 8px;
            }
            .quantitatif-grid th {
              background-color: #f1f5f9;
              font-weight: 900;
              text-align: left;
              text-transform: uppercase;
            }
            svg {
              max-width: 100%;
              height: auto;
            }
            img {
              max-width: 100%;
              height: auto;
            }
          </style>
        </head>
        <body>
          <div class="container">
            ${content}
          </div>
          <script>
            window.onload = function() {
              setTimeout(function() {
                window.print();
              }, 400);
            };
          </script>
        </body>
      </html>
    `);
    win.document.close();
  };
'''

# Place handleDirectPrintCroquis right before return statement of Calculators or after state declarations
code = code.replace('const [showTechnicalReport, setShowTechnicalReport] = useState<boolean>(false);',
                    'const [showTechnicalReport, setShowTechnicalReport] = useState<boolean>(false);\n' + handler_code)

# 2. Update Carré Orange button and add cartouche editor fields inside Carré Orange
old_carre_orange_button = '''                          <div className="flex justify-end pt-2 border-t border-slate-200">
                            <button
                              type="button"
                              onClick={() => setShowTechnicalReport(true)}
                              className="px-5 py-2.5 bg-blue-600 text-white rounded-xl text-xs font-black shadow-md hover:bg-blue-700 transition-all flex items-center gap-2"
                            >
                              <Printer className="w-4 h-4" />
                              <span>Générer le Cartouche Technique & Imprimer</span>
                            </button>
                          </div>'''

new_carre_orange_content = '''                          {/* Form Fields for Cartouche Metadata in Carré Orange */}
                          <div className="bg-slate-900 border border-orange-500/40 p-4 rounded-2xl space-y-3 text-white">
                            <div className="flex items-center gap-2 border-b border-orange-500/30 pb-2">
                              <FileText className="w-4 h-4 text-orange-400" />
                              <span className="text-xs font-black uppercase text-orange-400 tracking-wider">
                                Renseignements du Cartouche Technique (Imprimés sur Plan Sonelgaz)
                              </span>
                            </div>
                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                              <div>
                                <label className="text-[10px] font-bold text-slate-400 block mb-1">Nom du Poste / Ouvrage :</label>
                                <input
                                  type="text"
                                  value={cartoucheInfo.postName}
                                  onChange={(e) => setCartoucheInfo(prev => ({ ...prev, postName: e.target.value }))}
                                  className="w-full text-xs font-bold bg-slate-950 text-white border border-slate-700 rounded-lg px-2.5 py-1.5 focus:border-orange-500 focus:outline-none"
                                />
                              </div>
                              <div>
                                <label className="text-[10px] font-bold text-slate-400 block mb-1">N° du Plan :</label>
                                <input
                                  type="text"
                                  value={cartoucheInfo.planNumber}
                                  onChange={(e) => setCartoucheInfo(prev => ({ ...prev, planNumber: e.target.value }))}
                                  className="w-full text-xs font-bold bg-slate-950 text-white border border-slate-700 rounded-lg px-2.5 py-1.5 focus:border-orange-500 focus:outline-none"
                                />
                              </div>
                              <div>
                                <label className="text-[10px] font-bold text-slate-400 block mb-1">Indice de Révision :</label>
                                <input
                                  type="text"
                                  value={cartoucheInfo.revisionIndex}
                                  onChange={(e) => setCartoucheInfo(prev => ({ ...prev, revisionIndex: e.target.value }))}
                                  className="w-full text-xs font-bold bg-slate-950 text-white border border-slate-700 rounded-lg px-2.5 py-1.5 focus:border-orange-500 focus:outline-none"
                                />
                              </div>
                              <div>
                                <label className="text-[10px] font-bold text-slate-400 block mb-1">Échelle :</label>
                                <input
                                  type="text"
                                  value={cartoucheInfo.scale}
                                  onChange={(e) => setCartoucheInfo(prev => ({ ...prev, scale: e.target.value }))}
                                  className="w-full text-xs font-bold bg-slate-950 text-white border border-slate-700 rounded-lg px-2.5 py-1.5 focus:border-orange-500 focus:outline-none"
                                />
                              </div>
                            </div>

                            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
                              <div>
                                <label className="text-[10px] font-bold text-slate-400 block mb-1">Édité / Établi par :</label>
                                <input
                                  type="text"
                                  value={cartoucheInfo.editorName}
                                  onChange={(e) => setCartoucheInfo(prev => ({ ...prev, editorName: e.target.value }))}
                                  className="w-full text-xs font-bold bg-slate-950 text-amber-300 border border-slate-700 rounded-lg px-2.5 py-1.5 focus:border-orange-500 focus:outline-none"
                                />
                              </div>
                              <div>
                                <label className="text-[10px] font-bold text-slate-400 block mb-1">Vérifié par :</label>
                                <input
                                  type="text"
                                  value={cartoucheInfo.verifierName}
                                  onChange={(e) => setCartoucheInfo(prev => ({ ...prev, verifierName: e.target.value }))}
                                  className="w-full text-xs font-bold bg-slate-950 text-sky-300 border border-slate-700 rounded-lg px-2.5 py-1.5 focus:border-orange-500 focus:outline-none"
                                />
                              </div>
                              <div>
                                <label className="text-[10px] font-bold text-slate-400 block mb-1">Approuvé par (Sonelgaz) :</label>
                                <input
                                  type="text"
                                  value={cartoucheInfo.approverName}
                                  onChange={(e) => setCartoucheInfo(prev => ({ ...prev, approverName: e.target.value }))}
                                  className="w-full text-xs font-bold bg-slate-950 text-emerald-300 border border-slate-700 rounded-lg px-2.5 py-1.5 focus:border-orange-500 focus:outline-none"
                                />
                              </div>
                            </div>
                          </div>

                          {/* Action Button: Direct Print / PDF Export */}
                          <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-3 border-t border-slate-200">
                            <span className="text-[11px] text-slate-500 font-medium">
                              💡 L'impression génère le plan officiel combinant le <strong className="text-blue-600">Bloc Bleu (Schéma CAD 2D)</strong> et le <strong className="text-orange-600">Bloc Orange (Métrage & Cartouche)</strong> avec le logo officiel Sonelgaz.
                            </span>
                            <button
                              type="button"
                              onClick={handleDirectPrintCroquis}
                              className="w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700 text-white rounded-2xl text-xs font-black shadow-lg shadow-orange-500/20 transition-all flex items-center justify-center gap-2 shrink-0 cursor-pointer active:scale-95"
                            >
                              <Printer className="w-4 h-4" />
                              <span>Imprimer / Exporter PDF (Plan CAD & Cartouche Sonelgaz)</span>
                            </button>
                          </div>'''

if old_carre_orange_button in code:
    code = code.replace(old_carre_orange_button, new_carre_orange_content)
    print("Carré Orange button and form fields replaced successfully.")
else:
    print("Could not find old_carre_orange_button string.")

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
