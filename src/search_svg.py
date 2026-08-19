with open("src/components/Calculators.tsx", "r") as f:
    code = f.read()

import re
matches1 = [m.start() for m in re.finditer(r"SVG Blueprint Canvas", code)]
matches2 = [m.start() for m in re.finditer(r"Detailed Bounding Coordinates", code)]

print("Matches 1 (SVG):", matches1)
print("Matches 2 (Bounding):", matches2)
