import re

with open("src/components/Calculators.tsx", "r") as f:
    code = f.read()

# 1. Update Imports
code = code.replace(
    'import { ParametricSlab, ParametricAbri, ParametricMassif, ParametricGate, ParametricExtension, SlabType } from "../types";',
    'import { ParametricSlab, ParametricAbri, ParametricMassif, ParametricGate, OuvrageBlock, SlabType } from "../types";'
)

# 2. Update activeCadModal type definition
old_cad_modal_type = '"perimeter" | "slabs" | "gates" | "extension" | "voile" | "gabions" | "shelters" | null'
new_cad_modal_type = '"perimeter" | "slabs" | "gates" | "ouvrages" | "voile" | "gabions" | "shelters" | null'
code = code.replace(old_cad_modal_type, new_cad_modal_type)

print("Imports & Modal Type updated")

# Write code back so far
with open("src/components/Calculators.tsx", "w") as f:
    f.write(code)
