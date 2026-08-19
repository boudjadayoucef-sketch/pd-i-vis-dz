import sys
import re

file_path = "src/components/Calculators.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. ADD NEW STATE VARIABLES & HANDLERS
state_target = """  // Clôture Gates / Portails & Portillons State
  const [nbPortails5m, setNbPortails5m] = useState<number>(1); // Portail 2 vantaux de 5.00 ml (H = fenceHeight)
  const [nbPortillons1m, setNbPortillons1m] = useState<number>(1); // Portillon piéton de 1.00 ml (H = fenceHeight)
  const [gateSide, setGateSide] = useState<"sud" | "nord" | "est" | "ouest">("sud"); // Façade d'accès
  const [portailOffset, setPortailOffset] = useState<number>(5); // Pos en mètres sur la façade
  const [portillonOffset, setPortillonOffset] = useState<number>(15); // Pos en mètres sur la façade"""

state_replacement = """  // Fence Post Type & Concrete Section Inputs
  const [postType, setPostType] = useState<"metal_heb" | "beton_arme">("metal_heb");
  const [postConcreteWidth, setPostConcreteWidth] = useState<number>(0.25); // 25 cm = 0.25m
  const [postConcreteDepth, setPostConcreteDepth] = useState<number>(0.25); // 25 cm = 0.25m
  const [postConcreteHeight, setPostConcreteHeight] = useState<number>(2.8); // 2.8m

  // Dynamic Clôture Gates / Portails & Portillons State
  const [gates, setGates] = useState<ParametricGate[]>([
    {
      id: "gate-1",
      name: "Portail Véhicules Principal",
      type: "portail_5m",
      wall: "sud",
      offset: 5,
      width: 5,
      height: 2.8
    },
    {
      id: "gate-2",
      name: "Portillon Piéton",
      type: "portillon",
      wall: "sud",
      offset: 15,
      width: 1,
      height: 2.8
    }
  ]);
  const [selectedGateId, setSelectedGateId] = useState<string | null>(null);
  const [draggingGateId, setDraggingGateId] = useState<string | null>(null);

  const handleAddGate = (type: "portail_5m" | "portail_custom" | "portillon" = "portail_5m") => {
    const newId = "gate-" + Date.now();
    const width = type === "portail_5m" ? 5 : type === "portillon" ? 1 : 4;
    const name = type === "portillon" ? `Portillon Piéton ${gates.length + 1}` : `Portail Véhicules ${gates.length + 1}`;
    setGates(prev => [
      ...prev,
      {
        id: newId,
        name,
        type,
        wall: "sud",
        offset: Math.min(2 + prev.length * 3, Math.max(0, fenceA - width)),
        width,
        height: fenceHeight
      }
    ]);
    setSelectedGateId(newId);
  };

  const handleRemoveGate = (id: string) => {
    setGates(prev => prev.filter(g => g.id !== id));
    if (selectedGateId === id) setSelectedGateId(null);
  };

  const handleUpdateGate = (id: string, field: keyof ParametricGate, value: any) => {
    setGates(prev => prev.map(g => g.id === id ? { ...g, [field]: value } : g));
  };

  const handleDuplicateGate = (id: string) => {
    const target = gates.find(g => g.id === id);
    if (!target) return;
    const newId = "gate-" + Date.now();
    const maxWallLen = (target.wall === "sud" || target.wall === "nord") ? fenceA : fenceB;
    const newOffset = Math.min(Math.max(0, maxWallLen - target.width), target.offset + 2);
    setGates(prev => [
      ...prev,
      {
        ...target,
        id: newId,
        name: `${target.name} (Copie)`,
        offset: newOffset
      }
    ]);
    setSelectedGateId(newId);
  };

  // Dynamic Concrete Massifs (Fondations / Pylônes / Équipements) State
  const [massifs, setMassifs] = useState<ParametricMassif[]>([
    {
      id: "massif-1",
      name: "Massif Ancrage Filtre",
      length: 1.5,
      width: 1.5,
      height: 1.0,
      xOffset: 12,
      yOffset: 4,
      isExtension: false
    },
    {
      id: "massif-2",
      name: "Massif Pylône / Équipement",
      length: 1.2,
      width: 1.2,
      height: 0.8,
      xOffset: 25,
      yOffset: 14,
      isExtension: false
    }
  ]);
  const [selectedMassifId, setSelectedMassifId] = useState<string | null>(null);
  const [draggingMassifId, setDraggingMassifId] = useState<string | null>(null);

  const handleAddMassif = () => {
    const newId = "massif-" + Date.now();
    setMassifs(prev => [
      ...prev,
      {
        id: newId,
        name: `Massif Béton N°${prev.length + 1}`,
        length: 1.2,
        width: 1.2,
        height: 1.0,
        xOffset: Math.min(Math.max(0, fenceA - 1.2), 5 + (prev.length * 3) % 15),
        yOffset: Math.min(Math.max(0, fenceB - 1.2), 5 + (prev.length * 2) % 10),
        isExtension: false
      }
    ]);
    setSelectedMassifId(newId);
  };

  const handleRemoveMassif = (id: string) => {
    setMassifs(prev => prev.filter(m => m.id !== id));
    if (selectedMassifId === id) setSelectedMassifId(null);
  };

  const handleUpdateMassif = (id: string, field: keyof ParametricMassif, value: any) => {
    setMassifs(prev => prev.map(m => m.id === id ? { ...m, [field]: value } : m));
  };

  const handleDuplicateMassif = (id: string) => {
    const target = massifs.find(m => m.id === id);
    if (!target) return;
    const newId = "massif-" + Date.now();
    setMassifs(prev => [
      ...prev,
      {
        ...target,
        id: newId,
        name: `${target.name} (Copie)`,
        xOffset: Math.min(Math.max(0, fenceA - target.length), target.xOffset + 1.5),
        yOffset: Math.min(Math.max(0, fenceB - target.width), target.yOffset + 1.5)
      }
    ]);
    setSelectedMassifId(newId);
  };"""

if state_target in content:
    content = content.replace(state_target, state_replacement)
    print("State variables replacement successful!")
else:
    print("State variables target not found!")

# 2. UPDATE DEFAULT NAMES IN handleAddSlab
slab_names_target = """    const defaultNames: Record<SlabType, string> = {
      poste_detente: "Dalle Poste de Détente",
      rechaffeur: "Dalle Réchauffeur",
      gare_racleur_arrivee: "Dalle Gare Racleur (Arrivée)",
      gare_racleur_depart: "Dalle Gare Racleur (Départ)",
      epandage_assiette: "Épandage Assiette",
      abri_tele: "Dalle Abri Téléexploitation"
    };
    const defaultThickness: Record<SlabType, number> = {
      poste_detente: 0.25,
      rechaffeur: 0.25,
      gare_racleur_arrivee: 0.25,
      gare_racleur_depart: 0.25,
      epandage_assiette: 0.20,
      abri_tele: 0.20
    };"""

slab_names_replacement = """    const defaultNames: Record<SlabType, string> = {
      poste_detente: "Dalle Poste de Détente",
      rechaffeur: "Dalle Réchauffeur",
      gare_racleur_arrivee: "Dalle Gare Racleur (Arrivée)",
      gare_racleur_depart: "Dalle Gare Racleur (Départ)",
      epandage_assiette: "Épandage Assiette",
      abri_tele: "Dalle Abri Téléexploitation",
      dalle_custom: "Dalle Béton Personnalisée"
    };
    const defaultThickness: Record<SlabType, number> = {
      poste_detente: 0.25,
      rechaffeur: 0.25,
      gare_racleur_arrivee: 0.25,
      gare_racleur_depart: 0.25,
      epandage_assiette: 0.20,
      abri_tele: 0.20,
      dalle_custom: 0.25
    };"""

if slab_names_target in content:
    content = content.replace(slab_names_target, slab_names_replacement)
    print("Slab names replacement successful!")
else:
    print("Slab names target not found!")

# 3. UPDATE KEYBOARD LISTENER FOR ESCAPE, DELETE & DUPLICATE (Slab, Abri, Massif, Gate)
key_target = """      if (e.key === "Escape") {
        if (selectedSlabId) setSelectedSlabId(null);
        if (selectedAbriId) setSelectedAbriId(null);
        if (selectedShapeId) setSelectedShapeId(null);
        if (isFullscreenCroquis) setIsFullscreenCroquis(false);
      }

      if (!isInput) {
        if (croquisMode === "parametrique") {
          // Delete or Backspace
          if (e.key === "Delete" || e.key === "Backspace") {
            if (selectedSlabId) {
              e.preventDefault();
              setSlabs(prev => prev.filter(s => s.id !== selectedSlabId));
              setSelectedSlabId(null);
            } else if (selectedAbriId) {
              e.preventDefault();
              setAbris(prev => prev.filter(a => a.id !== selectedAbriId));
              setSelectedAbriId(null);
            }
          }

          // Duplicate: Ctrl+D, Cmd+D, or 'd' key
          const isD = e.key.toLowerCase() === "d";
          if (isD) {
            if (selectedSlabId) {
              e.preventDefault();
              const target = slabs.find(s => s.id === selectedSlabId);
              if (target) {
                const newId = "slab-" + Date.now();
                const dup: ParametricSlab = {
                  ...target,
                  id: newId,
                  name: `${target.name} (Copie)`,
                  xOffset: Math.min(Math.max(0, fenceA - target.length), target.xOffset + 1),
                  yOffset: Math.min(Math.max(0, fenceB - target.width), target.yOffset + 1)
                };
                setSlabs(prev => [...prev, dup]);
                setSelectedSlabId(newId);
                setSelectedAbriId(null);
              }
            } else if (selectedAbriId) {
              e.preventDefault();
              const target = abris.find(a => a.id === selectedAbriId);
              if (target) {
                const newId = "abri-" + Date.now();
                const dup: ParametricAbri = {
                  ...target,
                  id: newId,
                  name: `${target.name} (Copie)`,
                  xOffset: Math.min(Math.max(0, fenceA - target.length), target.xOffset + 1),
                  yOffset: Math.min(Math.max(0, fenceB - target.width), target.yOffset + 1)
                };
                setAbris(prev => [...prev, dup]);
                setSelectedAbriId(newId);
                setSelectedSlabId(null);
              }
            }
          }
        }"""

key_replacement = """      if (e.key === "Escape") {
        if (selectedSlabId) setSelectedSlabId(null);
        if (selectedAbriId) setSelectedAbriId(null);
        if (selectedMassifId) setSelectedMassifId(null);
        if (selectedGateId) setSelectedGateId(null);
        if (selectedShapeId) setSelectedShapeId(null);
        if (isFullscreenCroquis) setIsFullscreenCroquis(false);
      }

      if (!isInput) {
        if (croquisMode === "parametrique") {
          // Delete or Backspace shortcut for selected element
          if (e.key === "Delete" || e.key === "Backspace") {
            if (selectedSlabId) {
              e.preventDefault();
              handleRemoveSlab(selectedSlabId);
            } else if (selectedAbriId) {
              e.preventDefault();
              handleRemoveAbri(selectedAbriId);
            } else if (selectedMassifId) {
              e.preventDefault();
              handleRemoveMassif(selectedMassifId);
            } else if (selectedGateId) {
              e.preventDefault();
              handleRemoveGate(selectedGateId);
            }
          }

          // Duplicate shortcut: Ctrl+D, Cmd+D, or 'd' / 'D' key for selected element
          const isD = e.key.toLowerCase() === "d";
          if (isD) {
            if (selectedSlabId) {
              e.preventDefault();
              handleDuplicateSlab(selectedSlabId);
            } else if (selectedAbriId) {
              e.preventDefault();
              handleDuplicateAbri(selectedAbriId);
            } else if (selectedMassifId) {
              e.preventDefault();
              handleDuplicateMassif(selectedMassifId);
            } else if (selectedGateId) {
              e.preventDefault();
              handleDuplicateGate(selectedGateId);
            }
          }
        }"""

if key_target in content:
    content = content.replace(key_target, key_replacement)
    print("Keyboard listener replacement successful!")
else:
    print("Keyboard listener target not found!")

# Helper functions for duplicating slabs/abris
dup_helpers = """  const handleDuplicateSlab = (id: string) => {
    const target = slabs.find(s => s.id === id);
    if (!target) return;
    const newId = "slab-" + Date.now();
    setSlabs(prev => [
      ...prev,
      {
        ...target,
        id: newId,
        name: `${target.name} (Copie)`,
        xOffset: Math.min(Math.max(0, fenceA - target.length), target.xOffset + 1),
        yOffset: Math.min(Math.max(0, fenceB - target.width), target.yOffset + 1)
      }
    ]);
    setSelectedSlabId(newId);
  };

  const handleDuplicateAbri = (id: string) => {
    const target = abris.find(a => a.id === id);
    if (!target) return;
    const newId = "abri-" + Date.now();
    setAbris(prev => [
      ...prev,
      {
        ...target,
        id: newId,
        name: `${target.name} (Copie)`,
        xOffset: Math.min(Math.max(0, fenceA - target.length), target.xOffset + 1),
        yOffset: Math.min(Math.max(0, fenceB - target.width), target.yOffset + 1)
      }
    ]);
    setSelectedAbriId(newId);
  };
"""

# Insert duplicate helpers before handleAddAbri
if "const handleAddAbri = () => {" in content:
    content = content.replace("const handleAddAbri = () => {", dup_helpers + "\n  const handleAddAbri = () => {")
    print("Duplicate helpers inserted successfully!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Part 1 applied!")
