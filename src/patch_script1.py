import sys

TARGET = "src/components/Calculators.tsx"

with open(TARGET, "r", encoding="utf-8") as f:
    code = f.read()

applied = []
skipped = []

def do_replace(label, old, new):
    global code
    if old in code:
        code = code.replace(old, new, 1)
        applied.append(label)
    else:
        skipped.append(label)


# ---------------------------------------------------------------------------
# STEP 1 — Replace the now-stale "(Molette Zoom)" hint (wheel-zoom was
# removed earlier in favor of click-drag panning) with a Cotations toggle,
# finally giving the existing showCotations/cotationFilter state a real UI.
# ---------------------------------------------------------------------------

do_replace(
    "1. swap the stale wheel-zoom hint for a Cotations toggle button",
    '''                <span className="text-[10px] font-mono text-slate-400 hidden sm:inline px-1">
                  (Molette 🖱️ Zoom)
                </span>''',
    '''                <button
                  type="button"
                  onClick={() => setShowCotations(prev => !prev)}
                  title="Afficher/Masquer les cotations automatiques"
                  className={`px-2 py-1 text-[10px] font-mono font-bold rounded-xl transition-all border flex items-center gap-1 cursor-pointer ${
                    showCotations ? "bg-cyan-950 text-cyan-300 border-cyan-700" : "bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-700"
                  }`}
                >
                  <Ruler className="w-3 h-3" />
                  <span>Cotations</span>
                </button>''',
)

# ---------------------------------------------------------------------------
# STEP 2 — The auto-cotation layer itself: for every slab/abri, a dimension
# to its nearest fence side (X and Y), plus a dimension to its single
# nearest neighbouring element (if close enough to be meaningful). Gated by
# showCotations; respects cotationFilter ("all" vs "selected" element only).
# Inserted right before the gates render, so it sits under gates/gabions but
# above slabs/abris in the drawing order.
# ---------------------------------------------------------------------------

do_replace(
    "2. insert the auto-cotation render block before gates",
    '''                              {/* ==================== RENDERING PARAMETRIC GATES & PORTILLONS ==================== */}
                              {gates.map((g) => {''',
    '''                              {/* ==================== AUTO-COTATIONS (dalles / abri / clôture / voisin le plus proche) ==================== */}
                              {showCotations && (() => {
                                const mainOv = ouvrages[0];
                                if (!mainOv) return null;
                                const fenceX1 = cX + (mainOv.xOffset * scale) - (mainOv.length * scale) / 2;
                                const fenceY1 = cY + (mainOv.yOffset * scale) - (mainOv.width * scale) / 2;
                                const fenceX2 = fenceX1 + mainOv.length * scale;
                                const fenceY2 = fenceY1 + mainOv.width * scale;

                                type FurnitureBox = { id: string; x1: number; y1: number; x2: number; y2: number };
                                const boxes: FurnitureBox[] = [
                                  ...slabs.map(s => {
                                    const w = s.length * scale, h = s.width * scale;
                                    const x = cX + s.xOffset * scale - w / 2, y = cY + s.yOffset * scale - h / 2;
                                    return { id: s.id, x1: x, y1: y, x2: x + w, y2: y + h };
                                  }),
                                  ...abris.map(a => {
                                    const w = a.length * scale, h = a.width * scale;
                                    const x = cX + a.xOffset * scale - w / 2, y = cY + a.yOffset * scale - h / 2;
                                    return { id: a.id, x1: x, y1: y, x2: x + w, y2: y + h };
                                  })
                                ];

                                const filteredBoxes = cotationFilter === "selected"
                                  ? boxes.filter(b => b.id === selectedSlabId || b.id === selectedAbriId)
                                  : boxes;

                                const dimLine = (key: string, lx1: number, ly1: number, lx2: number, ly2: number, label: string, color: string) => {
                                  const horiz = Math.abs(lx2 - lx1) >= Math.abs(ly2 - ly1);
                                  const midX = (lx1 + lx2) / 2, midY = (ly1 + ly2) / 2;
                                  return (
                                    <g key={key}>
                                      <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke={color} strokeWidth="1.2" strokeDasharray="3 2" />
                                      <line x1={lx1} y1={ly1 - 3} x2={lx1} y2={ly1 + 3} stroke={color} strokeWidth="1.2" />
                                      <line x1={lx2} y1={ly2 - 3} x2={lx2} y2={ly2 + 3} stroke={color} strokeWidth="1.2" />
                                      <rect x={midX - (horiz ? 16 : 22)} y={midY - 7} width={horiz ? 32 : 44} height="14" rx="3" fill="#0f172a" stroke={color} strokeWidth="0.8" />
                                      <text x={midX} y={midY + 3} fill={color} fontSize="7.5" fontWeight="bold" textAnchor="middle">{label}</text>
                                    </g>
                                  );
                                };

                                const clearanceLines: any[] = [];
                                filteredBoxes.forEach((b) => {
                                  const cyMid = b.y1 + (b.y2 - b.y1) / 2;
                                  const cxMid = b.x1 + (b.x2 - b.x1) / 2;
                                  const distWest = (b.x1 - fenceX1) / scale;
                                  const distEast = (fenceX2 - b.x2) / scale;
                                  if (distWest <= distEast) {
                                    clearanceLines.push(dimLine(`cl-w-${b.id}`, fenceX1, cyMid, b.x1, cyMid, `${distWest.toFixed(1)}m`, "#94a3b8"));
                                  } else {
                                    clearanceLines.push(dimLine(`cl-e-${b.id}`, b.x2, cyMid, fenceX2, cyMid, `${distEast.toFixed(1)}m`, "#94a3b8"));
                                  }
                                  const distNord = (b.y1 - fenceY1) / scale;
                                  const distSud = (fenceY2 - b.y2) / scale;
                                  if (distNord <= distSud) {
                                    clearanceLines.push(dimLine(`cl-n-${b.id}`, cxMid, fenceY1, cxMid, b.y1, `${distNord.toFixed(1)}m`, "#94a3b8"));
                                  } else {
                                    clearanceLines.push(dimLine(`cl-s-${b.id}`, cxMid, b.y2, cxMid, fenceY2, `${distSud.toFixed(1)}m`, "#94a3b8"));
                                  }
                                });

                                const GAP_THRESHOLD = 20 * scale;
                                const usedPairs = new Set<string>();
                                const neighborLines: any[] = [];
                                filteredBoxes.forEach((a) => {
                                  let best: { b: FurnitureBox; gap: number; horiz: boolean } | null = null;
                                  boxes.forEach((b) => {
                                    if (a.id === b.id) return;
                                    const vOverlap = Math.min(a.y2, b.y2) - Math.max(a.y1, b.y1);
                                    const hOverlap = Math.min(a.x2, b.x2) - Math.max(a.x1, b.x1);
                                    let gap: number | null = null;
                                    let horiz = true;
                                    if (vOverlap > 0 && b.x1 >= a.x2) { gap = b.x1 - a.x2; horiz = true; }
                                    else if (vOverlap > 0 && a.x1 >= b.x2) { gap = a.x1 - b.x2; horiz = true; }
                                    else if (hOverlap > 0 && b.y1 >= a.y2) { gap = b.y1 - a.y2; horiz = false; }
                                    else if (hOverlap > 0 && a.y1 >= b.y2) { gap = a.y1 - b.y2; horiz = false; }
                                    if (gap !== null && gap >= 0 && gap < GAP_THRESHOLD && (!best || gap < best.gap)) {
                                      best = { b, gap, horiz };
                                    }
                                  });
                                  if (best) {
                                    const pairKey = [a.id, best.b.id].sort().join("|");
                                    if (!usedPairs.has(pairKey)) {
                                      usedPairs.add(pairKey);
                                      const gapM = (best.gap / scale).toFixed(1);
                                      if (best.horiz) {
                                        const midY = (Math.max(a.y1, best.b.y1) + Math.min(a.y2, best.b.y2)) / 2;
                                        const [lx, rx] = a.x2 <= best.b.x1 ? [a.x2, best.b.x1] : [best.b.x2, a.x1];
                                        neighborLines.push(dimLine(`nb-${pairKey}`, lx, midY, rx, midY, `${gapM}m`, "#38bdf8"));
                                      } else {
                                        const midX = (Math.max(a.x1, best.b.x1) + Math.min(a.x2, best.b.x2)) / 2;
                                        const [ty, by] = a.y2 <= best.b.y1 ? [a.y2, best.b.y1] : [best.b.y2, a.y1];
                                        neighborLines.push(dimLine(`nb-${pairKey}`, midX, ty, midX, by, `${gapM}m`, "#38bdf8"));
                                      }
                                    }
                                  }
                                });

                                return (
                                  <g opacity="0.95">
                                    {clearanceLines}
                                    {neighborLines}
                                  </g>
                                );
                              })()}

                              {/* ==================== RENDERING PARAMETRIC GATES & PORTILLONS ==================== */}
                              {gates.map((g) => {''',
)

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Applied {len(applied)}/{len(applied) + len(skipped)} patches:")
for a in applied:
    print(f"  OK   - {a}")
for s in skipped:
    print(f"  SKIP - {s}  (anchor not found — file may already differ; check manually)")

if skipped:
    sys.exit(1)
