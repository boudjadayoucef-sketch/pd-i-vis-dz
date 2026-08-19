import sys

with open("src/components/Calculators.tsx", "r") as f:
    code = f.read()

# 1. Update imports
code = code.replace(
    'import { ParametricSlab, ParametricAbri, ParametricMassif, ParametricGate, SlabType } from "../types";',
    'import { ParametricSlab, ParametricAbri, ParametricMassif, ParametricGate, ParametricExtension, SlabType } from "../types";'
)

# 2. Add SonelgazHeader component before main Calculators component
header_code = '''
const SonelgazHeader = () => (
  <div className="w-full bg-white pb-2 mb-3 border-b-2 border-[#007ac3]">
    <div className="flex items-center justify-between gap-4">
      <div className="flex items-center gap-2">
        <div className="bg-[#e67e00] p-2 rounded-xl text-white shadow-xs flex flex-col items-center justify-center min-w-[65px] min-h-[65px]">
          <div className="flex gap-1 items-end mb-0.5">
            <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
              <path d="M6 24L14 8L12 18L20 8L16 26L26 12L20 22L28 14" stroke="#007ac3" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <span className="text-[9px] font-black text-[#007ac3] leading-none uppercase tracking-wider">
            سونلغاز
          </span>
          <span className="text-[8px] font-bold text-white leading-none tracking-widest mt-0.5">
            sonelgaz
          </span>
        </div>
      </div>

      <div className="flex-1 text-right flex flex-col justify-center">
        <h1 className="text-sm md:text-base font-black text-[#007ac3] tracking-tight leading-tight">
          الشركة الجزائرية للكهرباء والغاز - نقل الغاز
        </h1>
        <h2 className="text-[11px] md:text-xs font-bold text-[#007ac3] tracking-normal leading-tight mt-0.5">
          Société algérienne de l'électricité et du gaz – Transport du Gaz
        </h2>
      </div>
    </div>
  </div>
);
'''

if "const SonelgazHeader =" not in code:
    code = code.replace("export default function Calculators() {", header_code + "\nexport default function Calculators() {")

# 3. Add Extension handlers and cartoucheInfo state
ext_state_old = '''  // Extension Génie Civil Périmétrique (Poste en Forme de L)
  const [hasCivilExtension, setHasCivilExtension] = useState<boolean>(false);
  const [extWall, setExtWall] = useState<"est" | "ouest" | "nord" | "sud">("est");
  const [extLength, setExtLength] = useState<number>(8.0); // Longueur extension A' (m)
  const [extWidth, setExtWidth] = useState<number>(6.0); // Largeur extension B' (m)
  const [extOffset, setExtOffset] = useState<number>(2.0); // Position offset m'''

ext_state_new = '''  // Extension Génie Civil Périmétrique (Poste en Forme de L) - Placement Libre et Multiples
  const [extensions, setExtensions] = useState<ParametricExtension[]>([
    {
      id: "ext-1",
      name: "Extension Forme L Côté Est",
      wall: "est",
      length: 8.0,
      width: 6.0,
      xOffset: 35,
      yOffset: 2.0,
      isExtension: true
    }
  ]);

  const primaryExt = extensions[0] || {
    id: "ext-1",
    name: "Extension Forme L",
    wall: "est" as const,
    length: 8.0,
    width: 6.0,
    xOffset: 35,
    yOffset: 2.0,
    isExtension: true
  };
  const hasCivilExtension = extensions.length > 0;
  const extLength = primaryExt.length;
  const extWidth = primaryExt.width;
  const extWall = primaryExt.wall;
  const extOffset = primaryExt.yOffset;

  const handleAddExtension = () => {
    const newId = "ext-" + Date.now();
    const count = extensions.length + 1;
    setExtensions(prev => [
      ...prev,
      {
        id: newId,
        name: `Extension Forme L N°${count}`,
        wall: "est",
        length: 8.0,
        width: 6.0,
        xOffset: fenceA,
        yOffset: 2.0,
        isExtension: true
      }
    ]);
  };

  const handleDuplicateExtension = (id: string) => {
    const target = extensions.find(e => e.id === id);
    if (!target) return;
    const newId = "ext-" + Date.now();
    setExtensions(prev => [
      ...prev,
      {
        ...target,
        id: newId,
        name: `${target.name} (Copie)`,
        xOffset: target.xOffset + 1,
        yOffset: target.yOffset + 1
      }
    ]);
  };

  const handleRemoveExtension = (id: string) => {
    setExtensions(prev => prev.filter(e => e.id !== id));
  };

  const handleUpdateExtension = (id: string, field: keyof ParametricExtension, value: any) => {
    setExtensions(prev => prev.map(e => e.id === id ? { ...e, [field]: value } : e));
  };

  // State for Cartouche Metadata & Verification signatures
  const [cartoucheInfo, setCartoucheInfo] = useState({
    editorName: "Boudjada Youcef",
    verifierName: "Chef de Service Génie Civil",
    approverName: "Directeur Transport Gaz",
    postName: "Poste de Détente & Mesurage Gaz",
    planNumber: "GRTG-GC-2026-001",
    revisionIndex: "Rev 01 (Bon Pour Exécution)",
    date: new Date().toLocaleDateString("fr-FR"),
    scale: "1:100"
  });'''

if ext_state_old in code:
    code = code.replace(ext_state_old, ext_state_new)
    print("Extension and Cartouche state added")
else:
    print("Could not find ext_state_old exact match")

with open("src/components/Calculators.tsx", "w") as f:
    f.write(code)

print("Script execution done")
