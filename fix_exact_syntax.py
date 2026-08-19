import sys

with open('src/components/Calculators.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Clean up mess at end of croquisMode parametrique before croquisMode libre
bad_end = '''                  </div>
                </div>
               )}

               {
           </div>
         </div>
       )
           </div>
         </div>
       )croquisMode === "libre" && ('''

good_end = '''          </div>
        </div>
      )}

      {croquisMode === "libre" && ('''

code = code.replace(bad_end, good_end)

# Also check for variations
bad_end_alt = '''                  </div>
                </div>
               )}

               {croquisMode === "libre" && ('''

code = code.replace(bad_end_alt, good_end)

with open('src/components/Calculators.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Exact syntax fix applied.")
