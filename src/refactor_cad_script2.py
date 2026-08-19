with open("src/components/Calculators.tsx", "r") as f:
    code = f.read()

target_block = '''  // Extension Génie Civil Périmétrique (Poste en Forme de L) - Placement Libre et Multiples
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
  };'''

replacement_block = '''  // Multi-Ouvrages & Blocs du Croquis (Gestion des Postes & Extensions Multiples)
  const [ouvrages, setOuvrages] = useState<OuvrageBlock[]>([
    {
      id: "ouvrage-1",
      name: "Poste Principal (Bloc A)",
      status: "nouveau",
      xOffset: 0,
      yOffset: 0,
      length: 35,
      width: 21,
      fenceHeight: 2.8,
      hasFence: true,
      hasVoile: false,
      hasGabions: false,
      voileSides: ["nord", "sud", "est", "ouest"],
      voileHeight: 2.5,
      voileThickness: 0.20,
      gabionSides: {
        nord: { enabled: false, etages: 1, length: 12, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
        sud: { enabled: false, etages: 2, length: 12, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
        est: { enabled: false, etages: 3, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
        ouest: { enabled: false, etages: 2, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
      }
    }
  ]);

  const [selectedOuvrageId, setSelectedOuvrageId] = useState<string | null>("ouvrage-1");
  const [draggingOuvrageId, setDraggingOuvrageId] = useState<string | null>(null);

  const primaryOuvrage = ouvrages[0] || {
    id: "ouvrage-1",
    name: "Poste Principal (Bloc A)",
    status: "nouveau" as const,
    xOffset: 0,
    yOffset: 0,
    length: fenceA,
    width: fenceB,
    fenceHeight: fenceHeight,
    hasFence: true,
    hasVoile: false,
    hasGabions: false
  };

  const handleAddOuvrage = () => {
    const newId = "ouvrage-" + Date.now();
    const count = ouvrages.length + 1;
    const refOv = ouvrages[0] || { length: 35, width: 21, xOffset: 0, yOffset: 0 };
    setOuvrages(prev => [
      ...prev,
      {
        id: newId,
        name: `Ouvrage / Bloc N°${count} (Extension)`,
        status: "nouveau",
        xOffset: refOv.xOffset + refOv.length + 4,
        yOffset: 0,
        length: 16,
        width: 12,
        fenceHeight: 2.8,
        hasFence: true,
        hasVoile: false,
        hasGabions: false,
        voileSides: ["nord", "sud", "est", "ouest"],
        voileHeight: 2.5,
        voileThickness: 0.20,
        gabionSides: {
          nord: { enabled: false, etages: 1, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
          sud: { enabled: false, etages: 1, length: 10, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
          est: { enabled: false, etages: 1, length: 8, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
          ouest: { enabled: false, etages: 1, length: 8, width: 1.0, height: 1.0, offset: 2.0, gap: 0.5, status: "nouveau" },
        }
      }
    ]);
    setSelectedOuvrageId(newId);
  };

  const handleDuplicateOuvrage = (id: string) => {
    const target = ouvrages.find(o => o.id === id);
    if (!target) return;
    const newId = "ouvrage-" + Date.now();
    setOuvrages(prev => [
      ...prev,
      {
        ...target,
        id: newId,
        name: `${target.name} (Copie)`,
        xOffset: target.xOffset + target.length + 3,
        yOffset: target.yOffset
      }
    ]);
    setSelectedOuvrageId(newId);
  };

  const handleRemoveOuvrage = (id: string) => {
    if (ouvrages.length <= 1) return;
    setOuvrages(prev => prev.filter(o => o.id !== id));
    if (selectedOuvrageId === id) setSelectedOuvrageId(null);
  };

  const handleUpdateOuvrage = (id: string, field: keyof OuvrageBlock, value: any) => {
    setOuvrages(prev => prev.map(o => {
      if (o.id !== id) return o;
      const updated = { ...o, [field]: value };
      if (id === ouvrages[0]?.id) {
        if (field === "length") setFenceA(Number(value) || 10);
        if (field === "width") setFenceB(Number(value) || 10);
      }
      return updated;
    }));
  };'''

if target_block in code:
    code = code.replace(target_block, replacement_block)
    print("State replaced successfully")
else:
    print("Could not find target_block")

with open("src/components/Calculators.tsx", "w") as f:
    f.write(code)
