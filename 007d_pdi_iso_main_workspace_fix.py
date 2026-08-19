#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I PATCH 007d — ISO plein écran = mode principal
===================================================

À exécuter depuis la racine du dépôt PD-I :

    python3 007d_pdi_iso_main_workspace_fix.py

Correctif suite aux tests 007c :
- le scroll de page est revenu ;
- la barre menus Fichier / Édition / Affichage / Dessin / Cotation / Alignement / ... n'apparaît plus ;
- les boutons n'affichent pas clairement leur fonction au survol ;
- le bouton Retour accueil n'est pas présent/clair ;
- le bandeau "Concepteur & Schéma..." n'a plus lieu d'être ;
- l'ISO doit être le mode principal plein écran, pas un affichage intégré/non-fullscreen.

Ce patch force donc :
- l'éditeur ISO en plein écran principal par défaut ;
- aucun affichage non-fullscreen de l'ancien moteur ;
- retour accueil via événement pdi:navigate ;
- tooltips visibles rapidement via CSS sur les boutons title ;
- wrapper ISO sans scroll de page ;
- docs mises à jour.
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
from pathlib import Path

ROOT = Path.cwd()
PATCH_ID = "007d"
STAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT / f".patch_backups/{PATCH_ID}_{STAMP}"
REPORT = ROOT / f"patch_{PATCH_ID}_report.txt"

ENGINE = ROOT / "src/pdi/isometric/engine/IsometrieModuleV48d.tsx"
WRAPPER = ROOT / "src/pdi/isometric/PdiIsometricEditor.tsx"
UNIFIED_APP = ROOT / "src/pdi/app/PdiUnifiedApp.tsx"
DOCS = ROOT / "docs"
PATCH_HISTORY = DOCS / "PATCH_HISTORY.md"


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def backup(path: Path) -> None:
    if path.exists() and path.is_file():
        dest = BACKUP_DIR / path.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def write_if_changed(path: Path, content: str, report: list[str]) -> bool:
    old = read(path)
    if old == content:
        report.append(f"UNCHANGED {rel(path)}")
        return False
    backup(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    report.append(f"UPDATED {rel(path)}")
    return True


def patch_engine(report: list[str]) -> None:
    if not ENGINE.exists():
        report.append(f"KO {rel(ENGINE)} absent")
        return

    text = read(ENGINE)
    original = text

    marker = "// PD&I PATCH 007d — ISO fullscreen is the main PD&I workspace"
    if marker not in text:
        text = marker + "\n" + text

    # 1) Forcer le mode plein écran comme mode principal.
    text, n_state = re.subn(
        r'const \[workspaceFullscreen, setWorkspaceFullscreen\] = useState(?:<boolean>)?\((?:true|false)\);',
        'const [workspaceFullscreen, setWorkspaceFullscreen] = useState(true);',
        text,
        count=1,
    )
    report.append(f"Engine: workspaceFullscreen forced true replacements={n_state}")

    # 2) Toute sortie du plein écran devient retour accueil, pas retour affichage intégré.
    nav_action = 'window.dispatchEvent(new CustomEvent("pdi:navigate", { detail: "home" }))'
    patterns = [
        r'setWorkspaceFullscreen\(false\)',
        r'setWorkspaceFullscreen\(\(v\) => !v\)',
        r'setWorkspaceFullscreen\(\s*\(v\)\s*=>\s*!v\s*\)',
    ]
    repl_count = 0
    for pat in patterns:
        text, n = re.subn(pat, nav_action, text)
        repl_count += n
    report.append(f"Engine: fullscreen exit/toggle actions redirected={repl_count}")

    # 3) Harmoniser les libellés.
    replacements = {
        "Quitter PD & I": "Retour accueil",
        "Quitter PD&I": "Retour accueil",
        "Quitter plein écran": "Retour accueil",
        "Mode intégré": "Retour accueil",
        "Plein écran": "Mode focus",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)

    # 4) Ajouter un bouton retour clair dans la topbar fullscreen, si non présent.
    if "pdi-return-home-007d" not in text:
        header_pattern = r'(<header\s+className="pdi-studio-topbar[^"]*"[^>]*>)'
        return_button = '''\1
            <button
              type="button"
              onClick={() => window.dispatchEvent(new CustomEvent("pdi:navigate", { detail: "home" }))}
              className="pdi-return-home-007d h-8 px-3 rounded-md border border-cyan-500/40 bg-cyan-500/10 text-cyan-200 text-[10px] font-black"
              title="Retour accueil PD&I"
            >
              ⌂ Retour
            </button>'''
        text, n_ret = re.subn(header_pattern, return_button, text, count=1)
        report.append(f"Engine: return button inserted={n_ret}")

    # 5) Cacher définitivement les anciens blocs non-fullscreen : bandeau Concepteur + toolbar claire.
    # Comme l'ISO est maintenant le workspace principal, ces blocs ne doivent plus apparaître.
    text = text.replace('className={`${workspaceFullscreen ? "hidden" : ""} bg-slate-950 border border-slate-800 rounded-2xl px-4 py-3 text-white shadow-lg`}', 'className="hidden"')
    text = text.replace('className={`${workspaceFullscreen ? "hidden" : "sticky"} top-2 z-40 bg-white/95 backdrop-blur border border-slate-200 rounded-xl shadow-sm px-2 py-2 flex-wrap items-center justify-between gap-2 ${workspaceFullscreen ? "" : "flex"}`}', 'className="hidden"')

    # 6) Root et CSS : no-scroll + tooltips immédiats.
    # Si la classe root a été altérée par des patchs précédents, forcer overflow-hidden côté plein écran.
    text = text.replace('overflow-auto bg-[#0B0F14]', 'overflow-hidden bg-[#0B0F14]')

    tooltip_css = '''
        [data-pdi-studio] button[title]{position:relative}
        [data-pdi-studio] button[title]:hover::after{content:attr(title);position:absolute;left:50%;top:calc(100% + 8px);transform:translateX(-50%);z-index:10080;min-width:max-content;max-width:260px;padding:6px 8px;border-radius:8px;background:#020617;color:#E6EDF3;border:1px solid rgba(103,232,249,.35);box-shadow:0 14px 35px rgba(0,0,0,.45);font-size:10px;font-weight:900;letter-spacing:.01em;white-space:nowrap;pointer-events:none}
        [data-pdi-studio] button[title]:hover::before{content:"";position:absolute;left:50%;top:100%;transform:translateX(-50%);border:5px solid transparent;border-bottom-color:rgba(103,232,249,.35);z-index:10081;pointer-events:none}
'''
    if "button[title]:hover::after" not in text:
        # Insérer avant la règle scrollbar ou avant fin style.
        anchor = '        [data-pdi-studio] ::-webkit-scrollbar{'
        if anchor in text:
            text = text.replace(anchor, tooltip_css + anchor, 1)
        else:
            text = text.replace('      `}</style>', tooltip_css + '      `}</style>', 1)
        report.append("Engine: tooltip CSS added")

    # 7) S'assurer que les menus CAO sont détectables.
    if "cadMenuGroups" not in text or "pdi-cad-menubar" not in text:
        report.append("WARN: cadMenuGroups/pdi-cad-menubar non détectés. La barre Fichier/Édition peut nécessiter restauration depuis le patch 007/4.8d1.")
    else:
        report.append("OK: barre menus CAO détectée")

    # 8) Éviter version accidentelle.
    text = text.replace("Version 4.8d11", "Version 4.8d1")

    if text != original:
        write_if_changed(ENGINE, text, report)
    else:
        report.append(f"UNCHANGED {rel(ENGINE)}")


def patch_wrapper(report: list[str]) -> None:
    if not WRAPPER.exists():
        report.append(f"INFO {rel(WRAPPER)} absent")
        return
    text = read(WRAPPER)
    original = text

    marker = "// PD&I PATCH 007d — wrapper locks ISO as primary fullscreen workspace"
    if marker not in text:
        text = marker + "\n" + text

    # Ajouter style anti-scroll sur wrapper si possible.
    if "pdi-isometric-primary-lock" not in text:
        text = text.replace("pdi-isometric-embedded", "pdi-isometric-embedded pdi-isometric-primary-lock")
        text = text.replace("pdi-v48d-primary-workspace", "pdi-v48d-primary-workspace pdi-isometric-primary-lock")

    # Si le wrapper n'a pas de style, ajouter un petit style global avant le rendu du moteur.
    if "pdi-isometric-primary-lock" not in text:
        report.append("WARN: impossible d'ajouter classe wrapper anti-scroll automatiquement")

    if text != original:
        write_if_changed(WRAPPER, text, report)
    else:
        report.append(f"UNCHANGED {rel(WRAPPER)}")


def patch_unified(report: list[str]) -> None:
    if not UNIFIED_APP.exists():
        report.append(f"INFO {rel(UNIFIED_APP)} absent")
        return
    text = read(UNIFIED_APP)
    original = text

    # En mode ISO, afficher seulement l'éditeur pour éviter deux shells.
    expected = 'if (activeModule === "isometric") {\n    return <PdiIsometricEditor />;\n  }'
    if expected not in text:
        # Corriger les variantes où on aurait gardé le shell autour de l'ISO.
        text, n = re.subn(
            r'if \(activeModule === "isometric"\) \{.*?return\s*<PdiIsometricEditor\s*/>\s*;.*?\}',
            expected,
            text,
            count=1,
            flags=re.S,
        )
        report.append(f"UnifiedApp: isometric direct render normalized={n}")

    # Ajouter title sur boutons si absent (navigation/launch).
    text = text.replace('onClick={() => openModule(card.id)}>', 'onClick={() => openModule(card.id)} title={card.title}>')

    if text != original:
        write_if_changed(UNIFIED_APP, text, report)
    else:
        report.append(f"UNCHANGED {rel(UNIFIED_APP)}")


def write_docs(report: list[str]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    add = '''

## Patch 007d — ISO plein écran = mode principal

Correctif après test utilisateur :
- le mode non-fullscreen de l'ancien ISO est supprimé de l'usage normal ;
- l'ISO doit s'ouvrir comme workspace principal plein écran ;
- la barre menus Fichier / Édition / Affichage / Dessin / Cotation / Alignement / Insertion / Impression / Export / Outils doit rester visible ;
- le bouton de sortie doit être `Retour accueil` ;
- les tooltips doivent être visibles sur les boutons ;
- le bandeau descriptif `Concepteur & Schéma...` ne doit plus apparaître dans le workspace principal.
'''
    old = read(PATCH_HISTORY)
    if "Patch 007d — ISO plein écran" not in old:
        write_if_changed(PATCH_HISTORY, old.rstrip() + add + "\n", report)
    else:
        report.append(f"UNCHANGED {rel(PATCH_HISTORY)}")


def postcheck(report: list[str]) -> None:
    report.append("\n--- POST-CHECK 007d ---")
    if ENGINE.exists():
        t = read(ENGINE)
        report.append(f"workspaceFullscreen true count: {t.count('workspaceFullscreen, setWorkspaceFullscreen] = useState(true)')}")
        report.append(f"workspaceFullscreen false count: {t.count('workspaceFullscreen, setWorkspaceFullscreen] = useState(false)')}")
        report.append(f"cadMenuGroups count: {t.count('cadMenuGroups')}")
        report.append(f"pdi-cad-menubar count: {t.count('pdi-cad-menubar')}")
        report.append(f"Retour accueil count: {t.count('Retour accueil')}")
        report.append(f"pdi:navigate count: {t.count('pdi:navigate')}")
        report.append(f"tooltip CSS count: {t.count('button[title]:hover::after')}")
        hidden_count = t.count('className="hidden"')
        report.append(f"hidden Concepteur block hints: {hidden_count}")
    if UNIFIED_APP.exists():
        u = read(UNIFIED_APP)
        report.append(f"UnifiedApp direct ISO render: {'OK' if 'return <PdiIsometricEditor />' in u else 'KO'}")


def main() -> int:
    report: list[str] = []
    report.append("PD&I PATCH 007d — ISO plein écran = mode principal")
    report.append(f"Date: {dt.datetime.now().isoformat()}")
    report.append(f"Root: {ROOT}")

    if not (ROOT / "package.json").exists():
        report.append("ERREUR: package.json introuvable. Exécuter depuis la racine du dépôt PD-I.")
        REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
        print("\n".join(report))
        return 2

    patch_engine(report)
    patch_wrapper(report)
    patch_unified(report)
    write_docs(report)
    postcheck(report)

    report.append("\n--- TESTS RECOMMANDÉS ---")
    report.append("1. npm run build")
    report.append("2. Ouvrir PD&I : page accueil unique")
    report.append("3. Cliquer ISO / Nouveau projet : l'ISO s'ouvre en workspace plein écran principal")
    report.append("4. Vérifier : plus de scroll de page")
    report.append("5. Vérifier : barre Fichier / Édition / Affichage / Dessin / Cotation / Alignement visible")
    report.append("6. Vérifier : bouton ⌂ Retour visible et fonctionne")
    report.append("7. Vérifier : survol des boutons affiche une info")
    report.append("8. Vérifier : le bandeau Concepteur & Schéma ne s'affiche plus dans le workspace")

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"\nRapport écrit: {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
