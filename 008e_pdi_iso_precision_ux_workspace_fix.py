#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
008e_pdi_iso_precision_ux_workspace_fix.py

Patch PD&I — Workspace ISO précision UX

À lancer depuis la racine du repo PD-I :
    python 008e_pdi_iso_precision_ux_workspace_fix.py
    npm run build

Ce patch :
- remet un bouton "← Accueil" si absent dans le workspace ISO ;
- améliore le header ISO pour éviter la superposition de la ligne haute ;
- ajoute un CSS UX premium pour le workspace ISO ;
- ajoute un runtime de secours pour bloquer le scroll navigateur sur la grille ;
- prépare un hook React propre pour corriger durablement zoom/pan/souris/DPR ;
- remplace quelques usages simples de offsetX/offsetY dans les fichiers ISO/canvas probables.
"""

from pathlib import Path
import re
import shutil
from datetime import datetime

ROOT = Path.cwd()
SRC = ROOT / "src"
PATCH_NAME = "008e_pdi_iso_precision_ux_workspace_fix"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def log(msg: str):
    print(f"[{PATCH_NAME}] {msg}")


def backup(path: Path):
    if path.exists():
        b = path.with_suffix(path.suffix + f".bak_{PATCH_NAME}_{STAMP}")
        shutil.copy2(path, b)
        log(f"Backup: {b}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    backup(path)
    path.write_text(content, encoding="utf-8")
    log(f"Écrit: {path}")


def all_src_files():
    if not SRC.exists():
        raise SystemExit("Erreur : dossier src introuvable. Lance ce patch depuis la racine du repo PD-I.")
    return [p for p in SRC.rglob("*") if p.is_file() and p.suffix in {".js", ".jsx", ".ts", ".tsx", ".css"}]


def ensure_imports(files):
    names = ["main.jsx", "main.tsx", "main.js", "main.ts", "App.jsx", "App.tsx", "App.js", "App.ts"]
    candidates = []
    for n in names:
        candidates.extend([p for p in files if p.name == n])
    if not candidates:
        log("Aucun fichier d'entrée trouvé pour importer le CSS/runtime. Import manuel possible.")
        return

    entry = candidates[0]
    txt = read(entry)
    imports = [
        'import "./pdiIsoPrecisionUx.css";',
        'import "./pdiIsoUxRuntimePatch.js";',
    ]
    changed = False
    for imp in reversed(imports):
        marker = imp.split("./", 1)[1].split("\"", 1)[0]
        if marker not in txt:
            txt = imp + "\n" + txt
            changed = True
    if changed:
        write(entry, txt)
        log(f"Imports ajoutés dans {entry}")
    else:
        log("Imports déjà présents")


def create_css():
    css = r'''
/* =========================================================
   008e — PD&I ISO Precision UX Workspace Fix
   ========================================================= */

:root {
  --pdi-bg-deep: #030812;
  --pdi-bg-panel: #07111f;
  --pdi-bg-panel-2: #0a1728;
  --pdi-border: rgba(0, 216, 255, 0.22);
  --pdi-border-strong: rgba(0, 216, 255, 0.48);
  --pdi-cyan: #00d9ff;
  --pdi-cyan-soft: rgba(0, 217, 255, 0.16);
  --pdi-text: #e8f7ff;
  --pdi-muted: #7ea8c4;
  --pdi-green: #00e676;
  --pdi-orange: #ff9f1a;
  --pdi-red: #ff4d5e;
}

body:has(.pdi-iso-workspace),
body:has(.iso-workspace),
body:has(.pdi-iso-canvas),
body:has(canvas) {
  overscroll-behavior: none;
}

/* Header ISO : plus haut et respirant pour éviter la superposition */
.pdi-iso-header,
.iso-header,
.pdi-workspace-header,
.iso-topbar,
[class*="iso"][class*="header"],
[class*="workspace"][class*="header"] {
  min-height: 92px !important;
  height: auto !important;
  position: relative !important;
  z-index: 50 !important;
  background: linear-gradient(180deg, rgba(3, 8, 18, 0.98), rgba(5, 12, 24, 0.98)) !important;
  border-bottom: 1px solid var(--pdi-border) !important;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.32) !important;
  overflow: visible !important;
}

.pdi-iso-header > *,
.iso-header > *,
.pdi-workspace-header > *,
.iso-topbar > * {
  position: relative;
  z-index: 2;
}

/* Ligne menus descendue : Fichier / Édition / Affichage / etc. */
.pdi-iso-menu-row,
.iso-menu-row,
.pdi-iso-menu,
.iso-menu,
.top-menu-bar,
[class*="menu-row"],
[class*="top-menu"] {
  min-height: 36px !important;
  display: flex !important;
  align-items: center !important;
  gap: 18px !important;
  padding-top: 4px !important;
  padding-bottom: 7px !important;
  border-top: 1px solid rgba(0, 217, 255, 0.08) !important;
}

/* Bouton retour */
.pdi-iso-back-btn,
.pdi-runtime-back-home {
  height: 34px !important;
  min-width: 88px !important;
  padding: 0 14px !important;
  border-radius: 10px !important;
  border: 1px solid rgba(0, 210, 255, 0.46) !important;
  background: rgba(0, 180, 255, 0.10) !important;
  color: #dffaff !important;
  font-size: 12px !important;
  font-weight: 800 !important;
  letter-spacing: 0.02em !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  transition: background 160ms ease, border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease !important;
}

.pdi-iso-back-btn:hover,
.pdi-runtime-back-home:hover {
  background: rgba(0, 210, 255, 0.22) !important;
  border-color: rgba(0, 230, 255, 0.82) !important;
  box-shadow: 0 0 16px rgba(0, 210, 255, 0.26) !important;
  transform: translateY(-1px) !important;
}

.pdi-iso-logo,
.iso-logo,
.pdi-logo,
[class*="logo"] img,
img[src*="pdi-logo"] {
  object-fit: contain !important;
}

/* Canvas / grille : pas de scroll navigateur, meilleure sensation CAO */
.pdi-iso-canvas,
.iso-canvas,
canvas {
  touch-action: none !important;
  user-select: none !important;
}

.pdi-iso-drawing-area,
.iso-drawing-area,
.pdi-iso-grid,
.iso-grid,
.pdi-canvas-wrap,
.iso-canvas-wrap,
[class*="canvas"],
[class*="grid"] {
  overscroll-behavior: none !important;
}

.pdi-cursor-crosshair,
.pdi-iso-canvas,
.iso-canvas {
  cursor: crosshair !important;
}

.pdi-pan-mode,
.pdi-pan-mode canvas,
.pdi-pan-mode .pdi-iso-canvas {
  cursor: grab !important;
}

.pdi-panning,
.pdi-panning canvas,
.pdi-panning .pdi-iso-canvas {
  cursor: grabbing !important;
}

.pdi-iso-toolbar button,
.iso-toolbar button,
[class*="toolbar"] button {
  transition: border-color 140ms ease, background 140ms ease, box-shadow 140ms ease, transform 140ms ease !important;
}

.pdi-iso-toolbar button:hover,
.iso-toolbar button:hover,
[class*="toolbar"] button:hover {
  border-color: rgba(0, 217, 255, 0.65) !important;
  box-shadow: 0 0 12px rgba(0, 217, 255, 0.18) !important;
}

.pdi-meter-panel,
.iso-meter-panel,
.pdi-bottom-meter,
[class*="meter"],
[class*="counter"] {
  min-height: 42px !important;
}

.pdi-meter-panel strong,
.iso-meter-panel strong,
.pdi-bottom-meter strong,
[class*="meter"] strong,
[class*="counter"] strong {
  font-size: 14px !important;
  line-height: 1.05 !important;
}

.pdi-runtime-zoom-badge {
  position: fixed;
  right: 22px;
  bottom: 52px;
  z-index: 9999;
  padding: 7px 10px;
  border-radius: 10px;
  background: rgba(3, 9, 18, 0.88);
  border: 1px solid rgba(0, 217, 255, 0.35);
  color: #dffaff;
  font: 700 12px/1.1 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  box-shadow: 0 0 18px rgba(0, 217, 255, 0.16);
  pointer-events: none;
  opacity: 0;
  transform: translateY(6px);
  transition: opacity 140ms ease, transform 140ms ease;
}

.pdi-runtime-zoom-badge.is-visible {
  opacity: 1;
  transform: translateY(0);
}
'''
    write(SRC / "pdiIsoPrecisionUx.css", css.strip() + "\n")


def create_runtime():
    js = r'''
/**
 * 008e — PD&I ISO Precision UX Runtime Patch
 * Ajoute un bouton retour si absent et bloque le scroll navigateur sur la zone ISO.
 */
(function pdiIsoUxRuntimePatch() {
  if (typeof window === "undefined" || typeof document === "undefined") return;
  if (window.__PDI_ISO_UX_RUNTIME_008E__) return;
  window.__PDI_ISO_UX_RUNTIME_008E__ = true;

  const STATE = { zoom: 1, panX: 0, panY: 0, isPanning: false, lastX: 0, lastY: 0, timer: null };
  const clamp = (v, min, max) => Math.max(min, Math.min(max, v));
  const textOf = (el) => (el && el.textContent ? el.textContent : "").trim();

  function isIsoScreen() {
    const txt = document.body ? document.body.innerText || "" : "";
    return /Vue isométrique|Schéma isométrique|Branche ISO|Graphe valide/i.test(txt);
  }

  function findHomeButton() {
    return Array.from(document.querySelectorAll("button, a, [role='button']")).find((el) => /Accueil/i.test(textOf(el)));
  }

  function goHome() {
    const existing = findHomeButton();
    if (existing && !existing.classList.contains("pdi-runtime-back-home")) {
      existing.click();
      return;
    }
    window.dispatchEvent(new CustomEvent("pdi:navigate-home", { detail: { source: "008e-runtime" } }));
    if (window.location.hash && window.location.hash !== "#/") window.location.hash = "#/";
  }

  function findIsoHeader() {
    return Array.from(document.querySelectorAll("header, nav, div")).find((el) => {
      const t = textOf(el);
      return /Vue isométrique|Schéma isométrique|Projet actif/i.test(t) && /Fichier/i.test(t) && /Affichage/i.test(t);
    });
  }

  function ensureBackButton() {
    if (!isIsoScreen()) return;
    if (document.querySelector(".pdi-runtime-back-home, .pdi-iso-back-btn")) return;
    const header = findIsoHeader();
    if (!header) return;

    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "pdi-runtime-back-home";
    btn.title = "Retour à l’accueil PD&I";
    btn.textContent = "← Accueil";
    btn.addEventListener("click", goHome);
    header.insertBefore(btn, header.firstChild);
  }

  function findCanvasOrWorkspace() {
    return document.querySelector("canvas") || Array.from(document.querySelectorAll("div, section, main")).find((el) => {
      const cls = String(el.className || "");
      return /canvas|grid|workspace|drawing|iso/i.test(cls) && el.clientWidth > 600;
    });
  }

  function badge() {
    let b = document.querySelector(".pdi-runtime-zoom-badge");
    if (!b) {
      b = document.createElement("div");
      b.className = "pdi-runtime-zoom-badge";
      document.body.appendChild(b);
    }
    return b;
  }

  function showZoom() {
    const b = badge();
    b.textContent = `Zoom ${Math.round(STATE.zoom * 100)}%`;
    b.classList.add("is-visible");
    clearTimeout(STATE.timer);
    STATE.timer = setTimeout(() => b.classList.remove("is-visible"), 650);
  }

  function attachWheelPrecision() {
    if (!isIsoScreen()) return;
    const target = findCanvasOrWorkspace();
    if (!target || target.__PDI_WHEEL_PATCHED_008E__) return;
    target.__PDI_WHEEL_PATCHED_008E__ = true;
    target.style.touchAction = "none";
    target.style.userSelect = "none";

    target.addEventListener("wheel", function (event) {
      event.preventDefault();
      event.stopPropagation();

      window.dispatchEvent(new CustomEvent("pdi:iso-wheel", {
        detail: { clientX: event.clientX, clientY: event.clientY, deltaY: event.deltaY }
      }));

      // Fallback visuel seulement si aucun label Zoom n'est détecté.
      const bodyText = document.body ? document.body.innerText || "" : "";
      if (/Zoom\s*\d+%/i.test(bodyText) && !window.__PDI_FORCE_FALLBACK_ZOOM__) return;

      const rect = target.getBoundingClientRect();
      const mx = event.clientX - rect.left;
      const my = event.clientY - rect.top;
      const before = { x: (mx - STATE.panX) / STATE.zoom, y: (my - STATE.panY) / STATE.zoom };
      const nextZoom = clamp(STATE.zoom * (event.deltaY > 0 ? 0.92 : 1.08), 0.25, 4);
      STATE.panX = mx - before.x * nextZoom;
      STATE.panY = my - before.y * nextZoom;
      STATE.zoom = nextZoom;
      target.style.transformOrigin = "0 0";
      target.style.transform = `translate(${STATE.panX}px, ${STATE.panY}px) scale(${STATE.zoom})`;
      showZoom();
    }, { passive: false });

    target.addEventListener("mousedown", function (event) {
      if (event.button !== 1 && !event.altKey) return;
      event.preventDefault();
      STATE.isPanning = true;
      STATE.lastX = event.clientX;
      STATE.lastY = event.clientY;
      document.body.classList.add("pdi-panning");
    });

    window.addEventListener("mousemove", function (event) {
      if (!STATE.isPanning) return;
      STATE.panX += event.clientX - STATE.lastX;
      STATE.panY += event.clientY - STATE.lastY;
      STATE.lastX = event.clientX;
      STATE.lastY = event.clientY;
      target.style.transformOrigin = "0 0";
      target.style.transform = `translate(${STATE.panX}px, ${STATE.panY}px) scale(${STATE.zoom})`;
    });

    window.addEventListener("mouseup", function () {
      STATE.isPanning = false;
      document.body.classList.remove("pdi-panning");
    });
  }

  function markCanvas() {
    document.querySelectorAll("canvas").forEach((c) => {
      c.style.touchAction = "none";
      c.style.userSelect = "none";
      c.dataset.pdiPrecisionPatch = "008e";
    });
  }

  function run() {
    ensureBackButton();
    attachWheelPrecision();
    markCanvas();
  }

  const observer = new MutationObserver(run);
  function start() {
    run();
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    window.addEventListener("resize", run);
    window.addEventListener("hashchange", run);
    window.addEventListener("popstate", run);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
'''
    write(SRC / "pdiIsoUxRuntimePatch.js", js.strip() + "\n")


def create_hook():
    hook = r'''
import { useCallback, useEffect, useRef, useState } from "react";

/**
 * Hook durable pour précision canvas CAO :
 * - getBoundingClientRect()
 * - screenToWorld / worldToScreen
 * - zoom centré curseur
 * - pan
 * - devicePixelRatio
 */
export function usePdiIsoPrecisionViewport(canvasRef, options = {}) {
  const minZoom = options.minZoom ?? 0.25;
  const maxZoom = options.maxZoom ?? 4;
  const initialZoom = options.initialZoom ?? 1;

  const [zoom, setZoom] = useState(initialZoom);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [cursorWorld, setCursorWorld] = useState({ x: 0, y: 0 });
  const stateRef = useRef({ zoom: initialZoom, pan: { x: 0, y: 0 }, isPanning: false, last: { x: 0, y: 0 } });

  useEffect(() => {
    stateRef.current.zoom = zoom;
    stateRef.current.pan = pan;
  }, [zoom, pan]);

  const clamp = useCallback((v, min, max) => Math.max(min, Math.min(max, v)), []);

  const resizeCanvasForDpr = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return null;
    const parent = canvas.parentElement || canvas;
    const rect = parent.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.style.width = `${rect.width}px`;
    canvas.style.height = `${rect.height}px`;
    canvas.width = Math.round(rect.width * dpr);
    canvas.height = Math.round(rect.height * dpr);
    const ctx = canvas.getContext("2d");
    if (ctx) {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = "high";
    }
    return { canvas, ctx, rect, dpr };
  }, [canvasRef]);

  const screenToWorld = useCallback((clientX, clientY) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    const sx = clientX - rect.left;
    const sy = clientY - rect.top;
    const s = stateRef.current;
    return { x: (sx - s.pan.x) / s.zoom, y: (sy - s.pan.y) / s.zoom };
  }, [canvasRef]);

  const worldToScreen = useCallback((x, y) => {
    const s = stateRef.current;
    return { x: x * s.zoom + s.pan.x, y: y * s.zoom + s.pan.y };
  }, []);

  const snapPoint = useCallback((point, step = 25) => ({
    x: Math.round(point.x / step) * step,
    y: Math.round(point.y / step) * step,
  }), []);

  const handleWheel = useCallback((event) => {
    event.preventDefault();
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const mx = event.clientX - rect.left;
    const my = event.clientY - rect.top;
    const s = stateRef.current;
    const before = { x: (mx - s.pan.x) / s.zoom, y: (my - s.pan.y) / s.zoom };
    const nextZoom = clamp(s.zoom * (event.deltaY > 0 ? 0.92 : 1.08), minZoom, maxZoom);
    const nextPan = { x: mx - before.x * nextZoom, y: my - before.y * nextZoom };
    stateRef.current.zoom = nextZoom;
    stateRef.current.pan = nextPan;
    setZoom(nextZoom);
    setPan(nextPan);
  }, [canvasRef, clamp, minZoom, maxZoom]);

  const handlePointerMove = useCallback((event) => {
    const s = stateRef.current;
    if (s.isPanning) {
      const dx = event.clientX - s.last.x;
      const dy = event.clientY - s.last.y;
      const nextPan = { x: s.pan.x + dx, y: s.pan.y + dy };
      s.pan = nextPan;
      s.last = { x: event.clientX, y: event.clientY };
      setPan(nextPan);
      return;
    }
    setCursorWorld(screenToWorld(event.clientX, event.clientY));
  }, [screenToWorld]);

  const startPan = useCallback((event) => {
    stateRef.current.isPanning = true;
    stateRef.current.last = { x: event.clientX, y: event.clientY };
  }, []);

  const stopPan = useCallback(() => {
    stateRef.current.isPanning = false;
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.addEventListener("wheel", handleWheel, { passive: false });
    return () => canvas.removeEventListener("wheel", handleWheel);
  }, [canvasRef, handleWheel]);

  useEffect(() => {
    resizeCanvasForDpr();
    window.addEventListener("resize", resizeCanvasForDpr);
    return () => window.removeEventListener("resize", resizeCanvasForDpr);
  }, [resizeCanvasForDpr]);

  return { zoom, pan, cursorWorld, setZoom, setPan, resizeCanvasForDpr, screenToWorld, worldToScreen, snapPoint, handleWheel, handlePointerMove, startPan, stopPan };
}
'''
    write(SRC / "components" / "usePdiIsoPrecisionViewport.js", hook.strip() + "\n")


def patch_offset_usage(files):
    helper = """
/* 008e PD&I precision helper — utiliser clientX/clientY + getBoundingClientRect, pas offsetX/offsetY */
function pdiGetCanvasLocalPoint008e(event, canvas) {
  const rect = canvas.getBoundingClientRect();
  return { x: event.clientX - rect.left, y: event.clientY - rect.top };
}
"""
    for p in files:
        if p.suffix not in {".js", ".jsx", ".ts", ".tsx"}:
            continue
        txt = read(p)
        low = txt.lower()
        if not (("offsetx" in low or "offsety" in low) and ("iso" in low or "canvas" in low or "isométrique" in low or "isometrique" in low)):
            continue
        original = txt
        if "pdiGetCanvasLocalPoint008e" not in txt:
            imports = list(re.finditer(r"^import .*?;\s*$", txt, flags=re.MULTILINE))
            if imports:
                i = imports[-1].end()
                txt = txt[:i] + "\n" + helper + "\n" + txt[i:]
            else:
                txt = helper + "\n" + txt
        txt = txt.replace("event.offsetX", "(pdiGetCanvasLocalPoint008e(event, event.currentTarget).x)")
        txt = txt.replace("event.offsetY", "(pdiGetCanvasLocalPoint008e(event, event.currentTarget).y)")
        txt = txt.replace("e.offsetX", "(pdiGetCanvasLocalPoint008e(e, e.currentTarget).x)")
        txt = txt.replace("e.offsetY", "(pdiGetCanvasLocalPoint008e(e, e.currentTarget).y)")
        if txt != original:
            write(p, txt)
            log(f"offsetX/offsetY corrigés dans {p}")


def create_report():
    report = f"""# {PATCH_NAME}

Patch appliqué le {STAMP}

## Fichiers ajoutés

- `src/pdiIsoPrecisionUx.css`
- `src/pdiIsoUxRuntimePatch.js`
- `src/components/usePdiIsoPrecisionViewport.js`

## Tests

1. `npm run build`
2. Accueil → ISO
3. Vérifier bouton `← Accueil`
4. Vérifier header sans superposition
5. Tester zoom souris/touchpad
6. Tester dessin nœud + tube
7. Vérifier précision point/souris après zoom

## Note importante

La correction durable de précision doit centraliser les coordonnées avec :

```js
const rect = canvas.getBoundingClientRect();
const screenX = event.clientX - rect.left;
const screenY = event.clientY - rect.top;
const worldX = (screenX - pan.x) / zoom;
const worldY = (screenY - pan.y) / zoom;
```
"""
    write(ROOT / f"{PATCH_NAME}_REPORT.md", report)


def main():
    log("Démarrage...")
    files = all_src_files()
    create_css()
    create_runtime()
    create_hook()
    ensure_imports(files)
    patch_offset_usage(files)
    create_report()
    log("Terminé.")
    print("\nCommandes suivantes :")
    print("  npm run build")
    print("  puis tester Accueil → ISO, bouton retour, zoom, points souris")


if __name__ == "__main__":
    main()
