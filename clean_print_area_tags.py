with open('src/components/Calculators.tsx', 'r') as f:
    code = f.read()

target_block_start = '                      {/* Technical Regulatory Notes */}'
target_block_end = '                          </table>\n                        );\n                      })()}\n                    </div>\n                  </div>\n              </div>'

idx1 = code.find(target_block_start)
idx2 = code.find('</div>\n          </div>\n        )}\n\n        {activeTab === "bordereau"', idx1)

if idx1 != -1 and idx2 != -1:
    print(f"Found trailing block between {idx1} and {idx2}")
    code = code[:idx1] + "                     </div>\n                   </div>\n                 </div>\n               </div>" + code[idx2:]

with open('src/components/Calculators.tsx', 'w') as f:
    f.write(code)

print("Cleaned up printAreaRef closing tags!")
