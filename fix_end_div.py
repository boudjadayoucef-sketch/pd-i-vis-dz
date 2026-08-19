with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# At end of file before `); \n }`, ensure there are two closing </div> tags
target = '''            {/* Modal Footer */}
            <div className="bg-slate-50 p-4 border-t border-slate-200 flex justify-end">
              <button
                type="button"
                onClick={() => setActiveCadModal(null)}
                className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-extrabold text-xs rounded-xl shadow-md transition-all active:scale-95 flex items-center gap-2 cursor-pointer"
              >
                <Check className="w-4 h-4 text-emerald-400" />
                <span>Valider & Appliquer au Plan 2D</span>
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}'''

replacement = '''            {/* Modal Footer */}
            <div className="bg-slate-50 p-4 border-t border-slate-200 flex justify-end">
              <button
                type="button"
                onClick={() => setActiveCadModal(null)}
                className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-extrabold text-xs rounded-xl shadow-md transition-all active:scale-95 flex items-center gap-2 cursor-pointer"
              >
                <Check className="w-4 h-4 text-emerald-400" />
                <span>Valider & Appliquer au Plan 2D</span>
              </button>
            </div>
          </div>
        </div>
      )}

      </div>
    </div>
  );
}'''

if target in code:
    code = code.replace(target, replacement)
    with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Added missing outer </div> successfully.")
else:
    print("Target not found.")
