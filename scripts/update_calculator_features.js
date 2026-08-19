import fs from 'fs';

const filePath = 'src/components/Calculators.tsx';
let content = fs.readFileSync(filePath, 'utf-8');

// 1. Update lucide-react imports to include Move, DoorOpen
content = content.replace(
  '  DoorClosed,\n  ShieldAlert,',
  '  DoorClosed,\n  Move,\n  DoorOpen,\n  ShieldAlert,'
);

// 2. Add new state variables right after fenceHeight
const fenceStateMarker = 'const [fenceHeight, setFenceHeight] = useState<number>(2.8); // Hauteur panneaux profilés (2.5 à 3.0m)';
const newStateCode = `const [fenceHeight, setFenceHeight] = useState<number>(2.8); // Hauteur panneaux profilés (2.5 à 3.0m)

  // Clôture Gates / Portails & Portillons State
  const [nbPortails5m, setNbPortails5m] = useState<number>(1); // Portail 2 vantaux de 5.00 ml (H = fenceHeight)
  const [nbPortillons1m, setNbPortillons1m] = useState<number>(1); // Portillon piéton de 1.00 ml (H = fenceHeight)
  const [gateSide, setGateSide] = useState<"sud" | "nord" | "est" | "ouest">("sud"); // Façade d'accès
  const [portailOffset, setPortailOffset] = useState<number>(5); // Pos en mètres sur la façade
  const [portillonOffset, setPortillonOffset] = useState<number>(15); // Pos en mètres sur la façade

  // Interactive Drag & Drop state for Slabs
  const [selectedSlabId, setSelectedSlabId] = useState<string | null>("slab-1");
  const [draggingSlabId, setDraggingSlabId] = useState<string | null>(null);
  const [dragStartPos, setDragStartPos] = useState<{ pointerX: number; pointerY: number; initX: number; initY: number } | null>(null);`;

content = content.replace(fenceStateMarker, newStateCode);

fs.writeFileSync(filePath, content, 'utf-8');
console.log("Updated state & imports successfully!");
