#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD & I — Patch V4.8d1
Workspace CAO fixe + barre menus professionnelle + boutons compacts.

Usage:
  python3 patch_4_8d1_workspace_cao.py IsometrieModule.tsx IsometrieModule_V4.8d1.tsx

Ce patch est volontairement non destructif : il ne touche pas aux logos PNG/public
ni aux constantes PDI_LOGO éventuelles. Il cible seulement l'ergonomie du shell.
"""
from pathlib import Path
import sys

if len(sys.argv) != 3:
    print("Usage: python3 patch_4_8d1_workspace_cao.py <input.tsx> <output.tsx>")
    raise SystemExit(2)

src = Path(sys.argv[1])
out = Path(sys.argv[2])
s = src.read_text(encoding="utf-8")


def rep(old: str, new: str, label: str, required=True):
    global s
    if old not in s:
        if required:
            raise SystemExit(f"Ancre introuvable: {label}")
        print(f"WARN ancre absente: {label}")
        return False
    s = s.replace(old, new, 1)
    print(f"OK {label}")
    return True

# Version / attribut studio.
s = s.replace('data-pdi-studio="v4.8c4"', 'data-pdi-studio="v4.8d1"')
s = s.replace('data-pdi-studio="v4.8d"', 'data-pdi-studio="v4.8d1"')
# Remplacement version sans doubler le suffixe si le patch est rejoué.
s = s.replace('Version 4.8d1', 'Version 4.8d')
s = s.replace('Version 4.8d', 'Version 4.8d1')

# Body/html verrouillés: pas de scroll de page.
scroll_unminified = '''  useEffect(() => {
    if (!workspaceFullscreen) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previousOverflow;
    };
  }, [workspaceFullscreen]);'''

scroll_minified = '''  useEffect(()=>{
    if(!workspaceFullscreen)return;
    const previousOverflow=document.body.style.overflow;
    document.body.style.overflow="hidden";
    return()=>{document.body.style.overflow=previousOverflow;};
  },[workspaceFullscreen]);'''

new_scroll = '''  useEffect(() => {
    if (!workspaceFullscreen) return;
    // V4.8d1_WORKSPACE_CAO_FIXED : le navigateur ne scrolle plus la page.
    // La molette est réservée au zoom/pan de la zone de travail.
    const previousBodyOverflow = document.body.style.overflow;
    const previousHtmlOverflow = document.documentElement.style.overflow;
    const previousBodyHeight = document.body.style.height;
    const previousHtmlHeight = document.documentElement.style.height;
    const previousOverscroll = document.body.style.overscrollBehavior;
    document.body.style.overflow = "hidden";
    document.documentElement.style.overflow = "hidden";
    document.body.style.height = "100vh";
    document.documentElement.style.height = "100vh";
    document.body.style.overscrollBehavior = "none";
    return () => {
      document.body.style.overflow = previousBodyOverflow;
      document.documentElement.style.overflow = previousHtmlOverflow;
      document.body.style.height = previousBodyHeight;
      document.documentElement.style.height = previousHtmlHeight;
      document.body.style.overscrollBehavior = previousOverscroll;
    };
  }, [workspaceFullscreen]);'''

if scroll_unminified in s:
    rep(scroll_unminified, new_scroll, 'verrouillage scroll global')
elif scroll_minified in s:
    rep(scroll_minified, new_scroll, 'verrouillage scroll global')
else:
    print("WARN: Scroll useEffect already updated or not found")

# Barre menus CAO: insérée juste avant return.
menu_block = r'''  // V4.8d1_WORKSPACE_CAO_MENU : menus type logiciel CAO.
  const cadMenuGroups: Array<{
    title: string;
    items: Array<{ label: string; hint?: string; run: () => void; disabled?: boolean }>;
  }> = [
    {
      title: "Fichier",
      items: [
        { label: "Exemple poste", hint: "charger", run: loadPresetPoste },
        { label: "Exemple gare racleur", hint: "charger", run: loadPresetGare },
        { label: "Ouvrir JSON", hint: "import", run: () => importProjectRef.current?.click() },
        { label: "Sauver JSON", hint: "export", run: exportProjectJson },
      ],
    },
    {
      title: "Édition",
      items: [
        { label: "Annuler", hint: "Ctrl+Z", run: undoGraph },
        { label: "Supprimer sélection", hint: "Suppr", run: deleteSelection, disabled: !selectedCount },
        { label: "Désélectionner", hint: "Esc", run: clearSelection },
      ],
    },
    {
      title: "Affichage",
      items: [
        { label: "Zoom +", hint: "+", run: zoomIn },
        { label: "Zoom -", hint: "-", run: zoomOut },
        { label: "Ajuster/recentrer", hint: "Fit", run: resetView },
        { label: showGrid ? "Masquer grille" : "Afficher grille", hint: "#", run: () => setShowGrid((v) => !v) },
        { label: showPipeLabels ? "Masquer pipelines" : "Afficher pipelines", run: () => setShowPipeLabels((v) => !v) },
        { label: showWelds ? "Masquer soudures" : "Afficher soudures", run: () => setShowWelds((v) => !v) },
      ],
    },
    {
      title: "Dessin",
      items: [
        { label: "Sélection", hint: "V", run: () => { setInteractionMode("select"); setIsoDrawMode("select"); } },
        { label: "Main / Pan", hint: "H", run: () => setInteractionMode("main") },
        { label: "Nœud", hint: "N", run: () => { setInteractionMode("select"); setIsoDrawMode("node"); } },
        { label: "Tube", hint: "T", run: () => { setInteractionMode("select"); setIsoDrawMode("segment"); } },
        { label: "Té", hint: "E", run: () => { setInteractionMode("select"); setIsoDrawMode("te"); } },
        { label: "Coude", hint: "C", run: () => { setInteractionMode("select"); setIsoDrawMode("coude"); } },
      ],
    },
    {
      title: "Cotation",
      items: [
        { label: "Créer cotation", hint: "M", run: () => { setInteractionMode("select"); setIsoDrawMode("dimension"); setDimensionPick(null); } },
        { label: showDimensions ? "Masquer cotations" : "Afficher cotations", hint: "D", run: () => setShowDimensions((v) => !v) },
        { label: "Supprimer dernière cote", hint: "⌫", run: removeSelectedDimensions, disabled: dimensions.length === 0 },
      ],
    },
    {
      title: "Alignement",
      items: [
        { label: "Aligner X", hint: "AX", run: () => alignSelectedNodesAxis("x"), disabled: selectedNodeIds.length < 2 },
        { label: "Aligner Y", hint: "AY", run: () => alignSelectedNodesAxis("y"), disabled: selectedNodeIds.length < 2 },
        { label: "Aligner Z", hint: "AZ", run: () => alignSelectedNodesAxis("z"), disabled: selectedNodeIds.length < 2 },
        { label: "Équipement sur tube", hint: "AT", run: alignSelectedEquipmentOnTube },
        { label: "Rendre parallèle", hint: "//", run: makeSelectedSegmentsParallel, disabled: selectedSegmentIds.length < 2 },
        { label: "Redresser ISO", hint: "ISO", run: redressIsoSelection, disabled: selectedSegmentIds.length < 1 },
      ],
    },
    {
      title: "Insertion",
      items: [
        { label: leftPanelOpen ? "Masquer bibliothèque" : "Afficher bibliothèque", hint: "⧉", run: () => setLeftPanelOpen((v) => !v) },
        { label: "Vanne par défaut", run: () => { setFitType("vanne_passage_total"); setFitLabel(FITTING_LABELS.vanne_passage_total); setLeftPanelOpen(true); } },
      ],
    },
    {
      title: "Impression",
      items: [
        { label: "Planche ISO", hint: "A3", run: () => setIsoMode((v) => (v === "editor" ? "planche" : "editor")) },
        { label: "Imprimer", hint: "⎙", run: printPlanSheet },
      ],
    },
    {
      title: "Export",
      items: [
        { label: "Exporter JSON", hint: "⇩", run: exportProjectJson },
        { label: "PDF / DXF", hint: "V4.8e", run: () => setStatusMessage("PDF/DXF prévu en V4.8e") },
      ],
    },
    {
      title: "Outils",
      items: [
        { label: "Contrôle réseau", hint: graphErrorCount ? `${graphErrorCount} erreur(s)` : "OK", run: () => { setStudioLayout("control"); setLeftPanelOpen(true); } },
        { label: "Palette commandes", hint: "Ctrl+K", run: () => setCommandPaletteOpen(true) },
        { label: "Raccourcis", hint: "?", run: () => setShortcutsOpen(true) },
      ],
    },
  ];

'''

if '  return (\n    <div' in s:
    rep('  return (\n    <div', menu_block + '  return (\n    <div', 'menus CAO avant return')
elif '  return <div' in s:
    rep('  return <div', menu_block + '  return <div', 'menus CAO avant return')

# Racine fullscreen sans overflow page.
s = s.replace(
    'className={`${workspaceFullscreen ? "fixed inset-0 z-[9999] overflow-auto bg-[#0B0F14] px-3 pb-[48px] pt-[66px] pl-[74px]" : "w-full"} pdi-studio-root space-y-3 animate-fade-in`}',
    'className={`${workspaceFullscreen ? "fixed inset-0 z-[9999] overflow-hidden bg-[#0B0F14] px-2 pb-[34px] pt-[84px] pl-[64px]" : "w-full"} pdi-studio-root ${workspaceFullscreen ? "h-screen" : "space-y-3"} animate-fade-in`}'
)

# CSS ergonomie/menu.
s = s.replace(
    '[data-pdi-studio] .pdi-rail-button{width:42px;height:42px;border:1px solid transparent;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#9CA3AF;background:#161B22;font-weight:900;font-size:11px}',
    '''[data-pdi-studio] .pdi-cad-menubar{display:flex;align-items:center;gap:2px;min-width:0;overflow:visible}
        [data-pdi-studio] .pdi-cad-menu{position:relative}
        [data-pdi-studio] .pdi-cad-menu-trigger{height:28px;padding:0 10px;border-radius:6px;color:#D1D5DB;background:transparent;font-size:11px;font-weight:900;white-space:nowrap}
        [data-pdi-studio] .pdi-cad-menu:hover .pdi-cad-menu-trigger{background:#1F2937;color:white}
        [data-pdi-studio] .pdi-cad-menu-panel{display:none;position:absolute;top:30px;left:0;min-width:210px;max-height:70vh;overflow:auto;z-index:10050;background:#0F141B;border:1px solid #30363D;border-radius:10px;padding:6px;box-shadow:0 18px 45px rgba(0,0,0,.45)}
        [data-pdi-studio] .pdi-cad-menu:hover .pdi-cad-menu-panel{display:block}
        [data-pdi-studio] .pdi-cad-menu-item{width:100%;display:flex;align-items:center;justify-content:space-between;gap:12px;border-radius:7px;padding:7px 8px;color:#E5E7EB;background:transparent;text-align:left;font-size:11px;font-weight:800}
        [data-pdi-studio] .pdi-cad-menu-item:hover:not(:disabled){background:#1D4ED8;color:white}
        [data-pdi-studio] .pdi-cad-menu-item:disabled{opacity:.38;cursor:not-allowed}
        [data-pdi-studio] .pdi-cad-menu-hint{font-size:9px;color:#94A3B8;font-weight:900}
        [data-pdi-studio] .pdi-studio-rail{background:#11151B;border-right:1px solid var(--pdi-line);box-shadow:8px 0 24px rgba(0,0,0,.2)}
        [data-pdi-studio] .pdi-rail-button{width:38px;height:38px;border:1px solid transparent;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#9CA3AF;background:#161B22;font-weight:900;font-size:14px}'''
)

s = s.replace(
    '@media(max-width:900px){[data-pdi-studio].pdi-studio-root{padding-left:12px!important;padding-top:60px!important}[data-pdi-studio] .pdi-studio-rail{display:none!important}[data-pdi-studio] .pdi-brand-subtitle{display:none}}',
    '''@media(max-width:900px){[data-pdi-studio].pdi-studio-root{padding-left:8px!important;padding-top:92px!important}[data-pdi-studio] .pdi-studio-rail{display:none!important}[data-pdi-studio] .pdi-brand-subtitle{display:none}[data-pdi-studio] .pdi-cad-menubar{position:absolute;left:8px;right:8px;bottom:6px;overflow-x:auto;padding-bottom:1px}[data-pdi-studio] .pdi-cad-menu-trigger{font-size:10px;padding:0 8px}[data-pdi-studio] .pdi-svg-logo{min-width:170px!important;max-width:210px!important}}
        @media(max-width:1200px){[data-pdi-studio] .pdi-cad-menu-trigger{padding:0 7px;font-size:10px}}'''
)

# Header: remplacer les onglets design/data/control par la barre menus.
new_menubar = '''            <nav className="pdi-cad-menubar hidden md:flex" aria-label="Menus PD & I">
              {cadMenuGroups.map((group) => (
                <div key={group.title} className="pdi-cad-menu">
                  <button type="button" className="pdi-cad-menu-trigger">
                    {group.title}
                  </button>
                  <div className="pdi-cad-menu-panel">
                    {group.items.map((item) => (
                      <button
                        key={`${group.title}-${item.label}`}
                        type="button"
                        disabled={item.disabled}
                        onClick={() => {
                          item.run();
                          setStatusMessage(`${group.title} · ${item.label}`);
                        }}
                        className="pdi-cad-menu-item"
                      >
                        <span>{item.label}</span>
                        {item.hint && <span className="pdi-cad-menu-hint">{item.hint}</span>}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </nav>'''

old_layout_tabs_1 = '''            <div className="hidden md:flex items-center gap-1 rounded-md border border-slate-700 bg-slate-900/70 p-1">
              {(["design", "data", "control"] as const).map((layout) => (
                <button
                  key={layout}
                  onClick={() => {
                    setStudioLayout(layout);
                    setLeftPanelOpen(layout === "design");
                    setStatusMessage(`Disposition ${layout}`);
                  }}
                  className={`h-7 px-3 rounded text-[10px] font-black uppercase ${studioLayout === layout ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"}`}
                >
                  {layout === "design"
                    ? "Conception"
                    : layout === "data"
                      ? "Données"
                      : "Contrôle"}
                </button>
              ))}
            </div>'''

old_layout_tabs_2 = '''          <div className="hidden md:flex items-center gap-1 rounded-md border border-slate-700 bg-slate-900/70 p-1">
            {(["design","data","control"] as const).map(layout=><button key={layout} onClick={()=>{setStudioLayout(layout);setLeftPanelOpen(layout==="design");setStatusMessage(`Disposition ${layout}`)}} className={`h-7 px-3 rounded text-[10px] font-black uppercase ${studioLayout===layout?"bg-blue-600 text-white":"text-slate-400 hover:text-white"}`}>{layout==="design"?"Conception":layout==="data"?"Données":"Contrôle"}</button>)}
          </div>'''

if old_layout_tabs_1 in s:
    s = s.replace(old_layout_tabs_1, new_menubar)
elif old_layout_tabs_2 in s:
    s = s.replace(old_layout_tabs_2, new_menubar)

# Boutons top compacts.
s = s.replace('className="h-8 px-3 rounded-md border border-slate-700 bg-slate-800 text-[10px] font-black">Ctrl+K</button>', 'className="h-8 px-2 rounded-md border border-slate-700 bg-slate-800 text-[10px] font-black" title="Palette commandes">⌘K</button>')
s = s.replace('className="h-8 px-3 rounded-md border border-red-500/40 bg-red-500/10 text-red-300 text-[10px] font-black">Quitter PD & I</button>', 'className="h-8 w-8 rounded-md border border-red-500/40 bg-red-500/10 text-red-300 text-sm font-black" title="Quitter PD & I">×</button>')

# Rail icônes compactes.
s = s.replace('>DIM</button>', '>⇔</button>')
s = s.replace('>LIB</button>', '>⧉</button>')
s = s.replace('>A3</button>', '>▣</button>')
s = s.replace('>PRN</button>', '>⎙</button>')
s = s.replace('>SAV</button>', '>⇩</button>')
s = s.replace('>OPN</button>', '>⇧</button>')

# Grille principale fixe
s = s.replace(
    '<div className="grid grid-cols-1 lg:grid-cols-12 gap-3 items-start">',
    '<div className={`${workspaceFullscreen ? "h-[calc(100vh-118px)] overflow-hidden" : ""} grid grid-cols-1 lg:grid-cols-12 gap-3 items-start`}>'
)
s = s.replace(
    'className={`${leftPanelOpen?"lg:col-span-3":"hidden"} space-y-3 lg:sticky lg:top-16 lg:max-h-[calc(100vh-5rem)] lg:overflow-y-auto lg:pr-1`}',
    'className={`${leftPanelOpen?"lg:col-span-3":"hidden"} ${workspaceFullscreen ? "h-full min-h-0 overflow-y-auto pr-1" : "space-y-3 lg:sticky lg:top-16 lg:max-h-[calc(100vh-5rem)] lg:overflow-y-auto lg:pr-1"} space-y-3`}'
)
s = s.replace(
    'className={`${leftPanelOpen ? "lg:col-span-3" : "hidden"} space-y-3 lg:sticky lg:top-16 lg:max-h-[calc(100vh-5rem)] lg:overflow-y-auto lg:pr-1`}',
    'className={`${leftPanelOpen ? "lg:col-span-3" : "hidden"} ${workspaceFullscreen ? "h-full min-h-0 overflow-y-auto pr-1" : "space-y-3 lg:sticky lg:top-16 lg:max-h-[calc(100vh-5rem)] lg:overflow-y-auto lg:pr-1"} space-y-3`}'
)

s = s.replace(
    '''      <div className={`${leftPanelOpen?"lg:col-span-9":"lg:col-span-12"}`}>
        <div className="bg-slate-900 rounded-3xl border-2 border-slate-800 p-4 shadow-2xl">''',
    '''      <div className={`${leftPanelOpen?"lg:col-span-9":"lg:col-span-12"} ${workspaceFullscreen ? "h-full min-h-0" : ""}`}>
        <div className={`${workspaceFullscreen ? "h-full min-h-0 flex flex-col overflow-hidden" : ""} bg-slate-900 rounded-3xl border-2 border-slate-800 p-3 shadow-2xl`}>'''
)

s = s.replace(
    '''      <div className={`${leftPanelOpen ? "lg:col-span-9" : "lg:col-span-12"}`}
        >
          <div className="bg-slate-900 rounded-3xl border-2 border-slate-800 p-4 shadow-2xl">''',
    '''      <div className={`${leftPanelOpen ? "lg:col-span-9" : "lg:col-span-12"} ${workspaceFullscreen ? "h-full min-h-0" : ""}`}
        >
          <div className={`${workspaceFullscreen ? "h-full min-h-0 flex flex-col overflow-hidden" : ""} bg-slate-900 rounded-3xl border-2 border-slate-800 p-3 shadow-2xl`}>'''
)

s = s.replace(
    '''          <div className="bg-slate-950 rounded-2xl overflow-hidden border border-slate-800">
            <svg ref={svgRef} viewBox="0 0 620 400" className="w-full h-[clamp(520px,70vh,820px)] select-none touch-none cursor-crosshair"''',
    '''          <div className={`${workspaceFullscreen ? "flex-1 min-h-0" : ""} bg-slate-950 rounded-2xl overflow-hidden border border-slate-800`}>
            <svg ref={svgRef} viewBox="0 0 620 400" className={`${workspaceFullscreen ? "h-full min-h-[360px]" : "h-[clamp(520px,70vh,820px)]"} w-full select-none touch-none cursor-crosshair`}'''
)

s = s.replace(
    '''            <div className="bg-slate-950 rounded-2xl overflow-hidden border border-slate-800">
              <svg
                ref={svgRef}
                viewBox="0 0 620 400"
                className="w-full h-[clamp(520px,70vh,820px)] select-none touch-none cursor-crosshair"''',
    '''            <div className={`${workspaceFullscreen ? "flex-1 min-h-0" : ""} bg-slate-950 rounded-2xl overflow-hidden border border-slate-800`}>
              <svg
                ref={svgRef}
                viewBox="0 0 620 400"
                className={`${workspaceFullscreen ? "h-full min-h-[360px]" : "h-[clamp(520px,70vh,820px)]"} w-full select-none touch-none cursor-crosshair`}'''
)

# Libellés de toolbar interne plus compacts (non destructif).
compact = {
    '>Grille ISO</button>': '>#</button>',
    '>+ NŒUD</button>': '>●</button>',
    '>+ TUBE</button>': '>╱</button>',
    '>+ TÉ</button>': '>⊥</button>',
    '>+ COUDE</button>': '>⌒</button>',
    '>Cotations</button>': '>⇔</button>',
    '>Pipelines</button>': '>PL</button>',
    '>Soudures</button>': '>W</button>',
    '>Labels</button>': '>Aa</button>',
    'UNDO</button>': '↶</button>',
    '>CLEAR</button>': '>×</button>',
}
for old, new in compact.items():
    s = s.replace(old, new)

out.write_text(s, encoding="utf-8")
print(f"V4.8d1 appliquée: {out}")
print("Ajouts: no-scroll global, menus Fichier/Édition/Affichage/etc., boutons compacts, canevas plein espace.")
