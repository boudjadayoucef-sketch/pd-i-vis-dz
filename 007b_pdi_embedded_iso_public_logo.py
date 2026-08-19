#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I PATCH 007b — ISO intégré + logo public unique
==================================================

À exécuter depuis la racine du dépôt PD-I :

    python3 007b_pdi_embedded_iso_public_logo.py

Corrige les réserves après 007a :
1) L'ISO ne doit plus s'ouvrir automatiquement en plein écran.
2) Il ne doit plus y avoir deux logos visibles.
3) AI Studio doit utiliser les fichiers logo placés dans /public, pas un logo SVG/fallback généré.

Ce patch :
- force le moteur ISO en mode intégré par défaut : workspaceFullscreen = false ;
- garde le mode focus possible seulement si l'utilisateur clique dessus ;
- réécrit PdiBrandMark pour utiliser uniquement des images servies depuis /public ;
- évite le fallback SVG / dessin CSS comme logo principal ;
- ajoute un rapport patch_007b_report.txt.

IMPORTANT :
Place tes fichiers logo dans /public avant ou après ce patch.
Noms recommandés :
  public/pdi-logo-horizontal.png
  public/pdi-logo-square.png
ou :
  public/logo_pdi_horizontal.png
  public/logo_pdi_square.png
Le script essaie de détecter automatiquement les fichiers image logo existants dans /public.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import shutil
from pathlib import Path

ROOT = Path.cwd()
STAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
PATCH_ID = "007b"
BACKUP_DIR = ROOT / f".patch_backups/{PATCH_ID}_{STAMP}"
REPORT = ROOT / f"patch_{PATCH_ID}_report.txt"

APP = ROOT / "src/pdi/app/PdiApp.tsx"
BRAND = ROOT / "src/pdi/app/PdiBrandMark.tsx"
ENGINE = ROOT / "src/pdi/isometric/engine/IsometrieModuleV48d.tsx"
WRAPPER = ROOT / "src/pdi/isometric/PdiIsometricEditor.tsx"
PUBLIC = ROOT / "public"
DOCS = ROOT / "docs"
PATCH_HISTORY = DOCS / "PATCH_HISTORY.md"
GITIGNORE = ROOT / ".gitignore"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def backup(path: Path) -> None:
    if not path.exists() or not path.is_file():
        return
    dest = BACKUP_DIR / path.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


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


def detect_public_logos(report: list[str]) -> tuple[str, str]:
    """Return browser paths: (horizontal, square)."""
    candidates: list[Path] = []
    if PUBLIC.exists():
        for p in PUBLIC.rglob("*"):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                name = p.name.lower()
                if any(k in name for k in ["pdi", "pd-i", "pd_i", "logo", "pipeline"]):
                    candidates.append(p)

    def web_path(p: Path) -> str:
        return "/" + p.relative_to(PUBLIC).as_posix()

    # Priorités explicites.
    horizontal_keys = ["horizontal", "wide", "header", "landscape", "banner"]
    square_keys = ["square", "icon", "mark", "compact", "app"]

    horizontal = None
    square = None
    for p in candidates:
        n = p.name.lower()
        if horizontal is None and any(k in n for k in horizontal_keys):
            horizontal = p
        if square is None and any(k in n for k in square_keys):
            square = p

    # Noms standards recommandés si présents.
    standards_h = [
        PUBLIC / "pdi-logo-horizontal.png",
        PUBLIC / "pdi-logo-horizontal.jpg",
        PUBLIC / "logo_pdi_horizontal.png",
        PUBLIC / "logo_pdi_horizontal.jpg",
        PUBLIC / "pdi_horizontal.png",
        PUBLIC / "pdi_horizontal.jpg",
    ]
    standards_s = [
        PUBLIC / "pdi-logo-square.png",
        PUBLIC / "pdi-logo-square.jpg",
        PUBLIC / "logo_pdi_square.png",
        PUBLIC / "logo_pdi_square.jpg",
        PUBLIC / "pdi_square.png",
        PUBLIC / "pdi_square.jpg",
    ]
    for p in standards_h:
        if p.exists():
            horizontal = p
            break
    for p in standards_s:
        if p.exists():
            square = p
            break

    # Fallback sur le premier candidat, ou chemins recommandés même si fichiers pas encore copiés.
    if horizontal is None and candidates:
        horizontal = candidates[0]
    if square is None and len(candidates) > 1:
        square = candidates[1]
    if square is None and horizontal is not None:
        square = horizontal

    horizontal_src = web_path(horizontal) if horizontal else "/pdi-logo-horizontal.png"
    square_src = web_path(square) if square else "/pdi-logo-square.png"

    report.append("Logo public detection:")
    report.append(f"- candidates: {len(candidates)}")
    for p in candidates[:20]:
        report.append(f"  - {rel(p)}")
    report.append(f"- horizontal src: {horizontal_src}")
    report.append(f"- square src: {square_src}")
    if not candidates:
        report.append("WARN: aucun logo détecté dans /public. Le composant utilisera /pdi-logo-horizontal.png et /pdi-logo-square.png ; copie ces fichiers dans public/.")
    return horizontal_src, square_src


def rewrite_brand_mark(horizontal_src: str, square_src: str, report: list[str]) -> None:
    content = f'''import React from "react";

// PD&I PATCH 007b — Logo global servi depuis /public.
// Ne pas utiliser de fallback SVG/CSS ici : AI Studio doit servir les vraies images du dossier public.
const PDI_LOGO_HORIZONTAL_PUBLIC = "{horizontal_src}";
const PDI_LOGO_SQUARE_PUBLIC = "{square_src}";

export type PdiBrandMarkProps = {{
  variant?: "horizontal" | "compact";
  size?: "sm" | "md" | "lg";
  className?: string;
}};

export default function PdiBrandMark({{
  variant = "horizontal",
  size = "md",
  className = "",
}}: PdiBrandMarkProps) {{
  const isCompact = variant === "compact";
  const src = isCompact ? PDI_LOGO_SQUARE_PUBLIC : PDI_LOGO_HORIZONTAL_PUBLIC;
  const height = size === "sm" ? 40 : size === "lg" ? 70 : 52;
  const width = isCompact ? height : undefined;

  return (
    <div
      className={{`pdi-brand-mark pdi-brand-mark--${{variant}} ${{className}}`}}
      aria-label="PD&I — Piping Design & Isometrics"
      style={{{{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        minWidth: 0,
        lineHeight: 1,
      }}}}
    >
      <img
        src={{src}}
        alt="PD&I — Piping Design & Isometrics"
        style={{{{
          height,
          width,
          maxWidth: isCompact ? height : "min(320px, 32vw)",
          objectFit: "contain",
          display: "block",
        }}}}
        draggable={{false}}
      />
    </div>
  );
}}
'''
    write_if_changed(BRAND, content, report)


def patch_app_single_logo(report: list[str]) -> None:
    if not APP.exists():
        report.append(f"KO {rel(APP)} absent")
        return
    text = read(APP)
    original = text

    if "PdiBrandMark" not in text:
        lines = text.splitlines()
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith("import "):
                insert_at = i + 1
        lines.insert(insert_at, 'import PdiBrandMark from "./PdiBrandMark";')
        text = "\n".join(lines) + ("\n" if original.endswith("\n") else "")
        report.append("PdiApp: import PdiBrandMark ajouté")

    # Si plusieurs PdiBrandMark ont été insérés par essais, garder le premier seulement.
    count = text.count("<PdiBrandMark")
    if count > 1:
        first = True
        def keep_first(m):
            nonlocal first
            if first:
                first = False
                return m.group(0)
            return ""
        text = re.sub(r"\s*<PdiBrandMark\b[^/]*/>\s*", keep_first, text)
        report.append(f"PdiApp: logos PdiBrandMark dédupliqués ({count} -> 1)")

    # Remplacer les badges texte PD&I seulement si aucun PdiBrandMark n'est dans le JSX.
    if "<PdiBrandMark" not in text:
        patterns = [
            r'<span([^>]*)>\s*PD\s*&\s*I\s*</span>',
            r'<div([^>]*)>\s*PD\s*&\s*I\s*</div>',
            r'<span([^>]*)>\s*PD&I\s*</span>',
            r'<div([^>]*)>\s*PD&I\s*</div>',
        ]
        replaced = False
        for pat in patterns:
            text, n = re.subn(pat, '<PdiBrandMark variant="horizontal" size="sm" />', text, count=1, flags=re.I | re.S)
            if n:
                replaced = True
                report.append("PdiApp: badge texte PD&I remplacé par logo public")
                break
        if not replaced:
            text, n = re.subn(r"(<header[^>]*>)", r"\1\n        <PdiBrandMark variant=\"horizontal\" size=\"sm\" />", text, count=1, flags=re.I)
            if n:
                report.append("PdiApp: logo public inséré dans le premier header")
            else:
                report.append("WARN: aucun emplacement header trouvé pour insérer PdiBrandMark")

    # Ajouter une classe CSS utile si le shell a déjà PdiBrandMark.
    if "pdi-shell-brand-single" not in text and "<PdiBrandMark" in text:
        text = text.replace('<PdiBrandMark ', '<PdiBrandMark className="pdi-shell-brand-single" ', 1)

    if text != original:
        write_if_changed(APP, text, report)
    else:
        report.append(f"UNCHANGED {rel(APP)}")


def patch_engine_embedded(report: list[str]) -> None:
    if not ENGINE.exists():
        report.append(f"KO {rel(ENGINE)} absent")
        return
    text = read(ENGINE)
    original = text

    marker = "// PD&I PATCH 007b — ISO embedded by default, public logo handled by SaaS shell"
    if marker not in text:
        text = marker + "\n" + text

    # Le point principal : ne plus ouvrir l'ISO en plein écran par défaut.
    patterns = [
        (r'const \[workspaceFullscreen, setWorkspaceFullscreen\] = useState\(true\);',
         'const [workspaceFullscreen, setWorkspaceFullscreen] = useState(false);'),
        (r'const \[workspaceFullscreen, setWorkspaceFullscreen\] = useState<boolean>\(true\);',
         'const [workspaceFullscreen, setWorkspaceFullscreen] = useState<boolean>(false);'),
    ]
    changed_fullscreen = False
    for pat, repl in patterns:
        text, n = re.subn(pat, repl, text)
        if n:
            changed_fullscreen = True
    report.append(f"Engine: workspaceFullscreen default false changed={changed_fullscreen}")

    # Libellés cohérents : l'utilisateur entre dans un module interne, pas dans une autre app.
    replacements = {
        "Quitter PD & I": "Retour accueil",
        "Quitter PD&I": "Retour accueil",
        "Quitter plein écran": "Mode intégré",
        "Plein écran": "Mode focus",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)

    # Éviter que l'ancien data-studio reste v4.8d si on a déjà un shell v4.8d1.
    text = text.replace('data-pdi-studio="v4.8c4"', 'data-pdi-studio="v4.8d1"')
    text = text.replace('data-pdi-studio="v4.8d"', 'data-pdi-studio="v4.8d1"')

    # Ne pas masquer le logo interne par CSS global : en mode focus il peut rester utile.
    # Mais comme le mode par défaut est intégré, l'ancienne topbar/logo interne ne sera pas rendue au chargement.

    if text != original:
        write_if_changed(ENGINE, text, report)
    else:
        report.append(f"UNCHANGED {rel(ENGINE)}")


def patch_wrapper_embedded(report: list[str]) -> None:
    if not WRAPPER.exists():
        report.append(f"INFO {rel(WRAPPER)} absent")
        return
    text = read(WRAPPER)
    original = text
    marker = "// PD&I PATCH 007b — wrapper keeps ISO embedded inside SaaS shell"
    if marker not in text:
        text = marker + "\n" + text
    text = text.replace("pdi-v48d-primary-workspace pdi-isometric-embedded pdi-isometric-embedded", "pdi-v48d-primary-workspace pdi-isometric-embedded")
    text = text.replace("pdi-v48d-primary-workspace", "pdi-v48d-primary-workspace pdi-isometric-embedded")
    if text != original:
        write_if_changed(WRAPPER, text, report)
    else:
        report.append(f"UNCHANGED {rel(WRAPPER)}")


def update_docs_and_ignore(report: list[str]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    add = """

## Patch 007b — ISO intégré + logo public unique

Correctifs :
- l'éditeur ISO ne s'ouvre plus automatiquement en plein écran ;
- le logo produit global est servi depuis `/public` via `PdiBrandMark` ;
- éviter les doubles logos entre le shell SaaS et la topbar interne ISO ;
- le mode plein écran devient un mode focus volontaire, pas l'ouverture par défaut.

Règle : PD&I est toute l'application SaaS. L'ISO est un workspace interne.
"""
    old = read(PATCH_HISTORY)
    if "Patch 007b — ISO intégré" not in old:
        write_if_changed(PATCH_HISTORY, old.rstrip() + add + "\n", report)
    else:
        report.append(f"UNCHANGED {rel(PATCH_HISTORY)}")

    git_lines = [
        "",
        "# PD&I generated backups / temporary patch files",
        "*.bak",
        "*.bak_*",
        "*.backup",
        "*.old",
        "*.tmp",
        ".patch_backups/",
    ]
    oldg = read(GITIGNORE)
    lines = oldg.splitlines()
    changed = False
    for line in git_lines:
        if line not in lines:
            lines.append(line)
            changed = True
    if changed:
        write_if_changed(GITIGNORE, "\n".join(lines).rstrip() + "\n", report)
    else:
        report.append(f"UNCHANGED {rel(GITIGNORE)}")


def postcheck(report: list[str]) -> None:
    report.append("\n--- POST-CHECK 007b ---")
    for p in [BRAND, APP, WRAPPER, ENGINE]:
        if not p.exists():
            report.append(f"KO {rel(p)} absent")
            continue
        txt = read(p)
        report.append(f"OK {rel(p)} size={p.stat().st_size}")
        if p == BRAND:
            report.append(f"  public horizontal refs={txt.count('/')} img tags={txt.count('<img')} svg refs={txt.lower().count('<svg')}")
        if p == APP:
            report.append(f"  PdiBrandMark count={txt.count('PdiBrandMark')}")
        if p == ENGINE:
            report.append(f"  workspaceFullscreen true count={txt.count('useState(true)')}")
            report.append(f"  workspaceFullscreen false count={txt.count('workspaceFullscreen, setWorkspaceFullscreen] = useState(false)')}")
            report.append(f"  Retour accueil count={txt.count('Retour accueil')}")
            report.append(f"  fixed inset root count={txt.count('fixed inset-0')}")


def main() -> int:
    report: list[str] = []
    report.append("PD&I PATCH 007b — ISO intégré + logo public unique")
    report.append(f"Date: {dt.datetime.now().isoformat()}")
    report.append(f"Root: {ROOT}")

    if not (ROOT / "package.json").exists():
        report.append("ERREUR: package.json introuvable. Exécute ce patch depuis la racine du dépôt PD-I.")
        REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
        print("\n".join(report))
        return 2

    h, s = detect_public_logos(report)
    rewrite_brand_mark(h, s, report)
    patch_app_single_logo(report)
    patch_engine_embedded(report)
    patch_wrapper_embedded(report)
    update_docs_and_ignore(report)
    postcheck(report)

    report.append("\n--- TESTS À FAIRE ---")
    report.append("1. Copier les vrais logos dans public/ si le rapport indique aucun logo détecté.")
    report.append("2. npm run build")
    report.append("3. Ouvrir PD&I : un seul logo global doit apparaître dans le shell.")
    report.append("4. Cliquer ISO : l'éditeur doit s'ouvrir intégré, pas en plein écran automatique.")
    report.append("5. Le mode focus doit rester volontaire, pas activé au chargement.")
    report.append("6. Vérifier mobile : pas de double header, pas de double logo.")

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"\nRapport écrit: {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
