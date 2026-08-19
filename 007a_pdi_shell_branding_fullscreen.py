#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I PATCH 007a — Branding global + workspace intégré
======================================================

À exécuter depuis la racine du dépôt PD-I :

    python3 007a_pdi_shell_branding_fullscreen.py

Objectif :
- faire de PD&I le branding de toute l'application SaaS, pas seulement l'éditeur ISO ;
- ajouter un composant global PdiBrandMark utilisé par le shell principal ;
- corriger les libellés incohérents du plein écran interne : "Quitter PD&I" → retour/dashboard/mode focus ;
- documenter l'architecture pipeline-design-skill + calculs Python déterministes ;
- préparer le patch 007 de stabilisation workflow IA/JSON.

Ce patch est prudent et idempotent : il évite les doublons et génère un rapport.
Il ne modifie pas les fichiers de logo public eux-mêmes.
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
from pathlib import Path

ROOT = Path.cwd()
STAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
PATCH_ID = "007a"
BACKUP_DIR = ROOT / f".patch_backups/{PATCH_ID}_{STAMP}"
REPORT = ROOT / f"patch_{PATCH_ID}_report.txt"

APP = ROOT / "src/pdi/app/PdiApp.tsx"
BRAND = ROOT / "src/pdi/app/PdiBrandMark.tsx"
ENGINE = ROOT / "src/pdi/isometric/engine/IsometrieModuleV48d.tsx"
WRAPPER = ROOT / "src/pdi/isometric/PdiIsometricEditor.tsx"
INDEX_HTML = ROOT / "index.html"
DOCS = ROOT / "docs"
PATCH_HISTORY = DOCS / "PATCH_HISTORY.md"
SKILLS_DOC = DOCS / "PD_I_AGENTS_SKILLS_PYTHON.md"
GITIGNORE = ROOT / ".gitignore"


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


def append_unique_lines(path: Path, lines: list[str], report: list[str]) -> None:
    old = read(path)
    existing = old.splitlines()
    changed = False
    for line in lines:
        if line not in existing:
            existing.append(line)
            changed = True
    if changed:
        write_if_changed(path, "\n".join(existing).rstrip() + "\n", report)
    else:
        report.append(f"UNCHANGED {rel(path)}")


def detect_logo_import() -> tuple[str, str]:
    """Return (import_line, usage_jsx_source)."""
    candidates = [
        ROOT / "src/pdi/assets/pdiLogos.ts",
        ROOT / "src/pdi/assets/pdiLogos.tsx",
        ROOT / "src/pdi/assets/pdiLogos/index.ts",
        ROOT / "src/pdi/assets/pdiLogos/index.tsx",
    ]
    if any(p.exists() for p in candidates):
        return (
            'import { PDI_LOGO_HORIZONTAL_SRC, PDI_LOGO_SQUARE_SRC } from "../assets/pdiLogos";',
            "assets",
        )
    # Fallback safe: no static asset import if the module does not exist.
    return ("", "fallback")


def create_brand_component(report: list[str]) -> None:
    import_line, mode = detect_logo_import()
    if mode == "assets":
        body = f'''import React from "react";
{import_line}

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
  const logoSrc = isCompact ? PDI_LOGO_SQUARE_SRC : PDI_LOGO_HORIZONTAL_SRC;
  const height = size === "sm" ? 36 : size === "lg" ? 64 : 46;
  return (
    <div
      className={{`pdi-brand-mark ${{className}}`}}
      aria-label="PD&I — Piping Design & Isometrics"
      style={{{{ display: "inline-flex", alignItems: "center", gap: 10, minWidth: 0 }}}}
    >
      <img
        src={{logoSrc}}
        alt="PD&I"
        style={{{{ height, width: isCompact ? height : "auto", objectFit: "contain", display: "block" }}}}
      />
      {{isCompact ? null : (
        <div style={{{{ minWidth: 0, lineHeight: 1.05 }}}}>
          <div style={{{{ fontWeight: 1000, letterSpacing: ".02em", color: "#f8fafc", fontSize: size === "lg" ? 22 : 16 }}}}>PD&I</div>
          <div style={{{{ fontWeight: 800, letterSpacing: ".06em", color: "#67e8f9", fontSize: 9, textTransform: "uppercase", whiteSpace: "nowrap" }}}}>Piping Design & Isometrics</div>
        </div>
      )}}
    </div>
  );
}}
'''
    else:
        body = '''import React from "react";

export type PdiBrandMarkProps = {
  variant?: "horizontal" | "compact";
  size?: "sm" | "md" | "lg";
  className?: string;
};

export default function PdiBrandMark({
  variant = "horizontal",
  size = "md",
  className = "",
}: PdiBrandMarkProps) {
  const box = size === "sm" ? 34 : size === "lg" ? 58 : 44;
  const font = size === "sm" ? 14 : size === "lg" ? 22 : 17;
  const compact = variant === "compact";
  return (
    <div
      className={`pdi-brand-mark ${className}`}
      aria-label="PD&I — Piping Design & Isometrics"
      style={{ display: "inline-flex", alignItems: "center", gap: 10, minWidth: 0 }}
    >
      <div
        style={{
          width: box,
          height: box,
          borderRadius: 12,
          display: "grid",
          placeItems: "center",
          color: "#fff",
          fontWeight: 1000,
          letterSpacing: "-.08em",
          background: "radial-gradient(circle at 30% 20%, #22d3ee, #1d4ed8 55%, #020617)",
          boxShadow: "inset 0 0 0 1px rgba(255,255,255,.18), 0 10px 28px rgba(14,165,233,.22)",
          border: "1px solid rgba(103,232,249,.35)",
          fontSize: font,
        }}
      >
        P&I
      </div>
      {compact ? null : (
        <div style={{ minWidth: 0, lineHeight: 1.05 }}>
          <div style={{ fontWeight: 1000, letterSpacing: ".02em", color: "#f8fafc", fontSize: size === "lg" ? 22 : 16 }}>PD&I</div>
          <div style={{ fontWeight: 800, letterSpacing: ".06em", color: "#67e8f9", fontSize: 9, textTransform: "uppercase", whiteSpace: "nowrap" }}>Piping Design & Isometrics</div>
        </div>
      )}
    </div>
  );
}
'''
    write_if_changed(BRAND, body, report)
    report.append(f"Brand component mode: {mode}")


def patch_pdi_app(report: list[str]) -> None:
    if not APP.exists():
        report.append(f"KO {rel(APP)} absent")
        return
    text = read(APP)
    original = text

    # Import du composant global.
    if "PdiBrandMark" not in text:
        # Placer après les imports React / premiers imports.
        lines = text.splitlines()
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith("import "):
                insert_at = i + 1
        lines.insert(insert_at, 'import PdiBrandMark from "./PdiBrandMark";')
        text = "\n".join(lines) + ("\n" if original.endswith("\n") else "")
        report.append("PdiApp: import PdiBrandMark ajouté")

    # Remplacer badge texte PD&I simple par logo global, si structure reconnaissable.
    replacements = 0
    patterns = [
        r'<span([^>]*)>\s*PD\s*&\s*I\s*</span>',
        r'<div([^>]*)>\s*PD\s*&\s*I\s*</div>',
        r'<span([^>]*)>\s*PD&I\s*</span>',
        r'<div([^>]*)>\s*PD&I\s*</div>',
    ]
    for pat in patterns:
        text, n = re.subn(pat, '<PdiBrandMark variant="horizontal" size="sm" />', text, count=1, flags=re.I | re.S)
        replacements += n
        if n:
            break

    if replacements:
        report.append("PdiApp: badge texte PD&I remplacé par PdiBrandMark")
    else:
        # Insertion safe : juste après la première balise <header ...> si aucune substitution.
        if "<PdiBrandMark" not in text:
            text, n = re.subn(r"(<header[^>]*>)", r"\1\n        <PdiBrandMark variant=\"horizontal\" size=\"sm\" />", text, count=1, flags=re.I)
            if n:
                report.append("PdiApp: PdiBrandMark inséré dans le premier <header>")
            else:
                report.append("WARN PdiApp: emplacement logo non trouvé — composant créé mais non inséré automatiquement")

    # Harmoniser wording produit.
    text = text.replace("Guide Travaux Gaz", "PD&I")
    text = text.replace("Guide Sonelgaz", "PD&I")
    text = text.replace("STG.GTDev", "PD&I")

    if text != original:
        write_if_changed(APP, text, report)
    else:
        report.append(f"UNCHANGED {rel(APP)}")


def patch_engine_fullscreen(report: list[str]) -> None:
    if not ENGINE.exists():
        report.append(f"KO {rel(ENGINE)} absent")
        return
    text = read(ENGINE)
    original = text

    marker = "// PD&I PATCH 007a — shell SaaS branding/fullscreen wording reviewed"
    if marker not in text:
        text = marker + "\n" + text

    replacements = {
        "Quitter PD & I": "Retour accueil",
        "Quitter PD&I": "Retour accueil",
        "Quitter plein écran": "Mode intégré",
        "Plein écran": "Mode focus",
        "À propos de PD & I": "À propos de PD&I",
        "PD & I — Pipeline Design & Isometrics": "PD&I — Piping Design & Isometrics",
        "Pipeline Design & Isometrics": "Piping Design & Isometrics",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)

    # Ne pas supprimer le no-scroll : demandé pour workspace CAO, mais documenter la séparation.
    note = "// 007a: le shell PD-I est la source de vérité produit ; ce plein écran est un mode focus du workspace ISO."
    if note not in text and "workspaceFullscreen" in text:
        text = text.replace("const [workspaceFullscreen", note + "\n  const [workspaceFullscreen", 1)

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
    marker = "// PD&I PATCH 007a — ISO workspace embedded in global SaaS shell"
    if marker not in text:
        text = marker + "\n" + text

    # Ajouter une classe/conteneur reconnaissable si possible sans casser le wrapper.
    text = text.replace("pdi-v48d-primary-workspace", "pdi-v48d-primary-workspace pdi-isometric-embedded")

    if text != original:
        write_if_changed(WRAPPER, text, report)
    else:
        report.append(f"UNCHANGED {rel(WRAPPER)}")


def patch_index(report: list[str]) -> None:
    if not INDEX_HTML.exists():
        report.append(f"INFO {rel(INDEX_HTML)} absent")
        return
    text = read(INDEX_HTML)
    original = text
    text = re.sub(r"<title>.*?</title>", "<title>PD&I — Piping Design & Isometrics</title>", text, flags=re.I | re.S)
    text = text.replace("Guide Travaux Gaz", "PD&I")
    text = text.replace("STG.GTDev", "PD&I")
    if text != original:
        write_if_changed(INDEX_HTML, text, report)
    else:
        report.append(f"UNCHANGED {rel(INDEX_HTML)}")


def write_docs(report: list[str]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    skills_doc = '''# PD&I — Agents spécialisés, pipeline-design-skill et calculs Python

## Principe

Le dépôt **PD-I** contient l'application SaaS, le workspace, le modèle JSON central, les imports/exports et l'interface.

Le dépôt **pipeline-design-skill** servira aux agents spécialisés : reconnaissance croquis, analyse photo, piping JSON, DXF, validation, QA engineering.

## Règle importante

Les agents IA ne doivent pas faire les calculs techniques finaux.

```txt
IA = reconnaissance, extraction, assistance, orchestration
Python = calculs techniques déterministes et vérifiables
```

## Calculs à faire par Python

- longueurs et cumuls ;
- coordonnées ISO ;
- pentes et niveaux Z ;
- DN/NPS, unités, conversions ;
- nomenclature/BOM ;
- poids estimatifs ;
- validation réseau, ports, soudures ;
- parsing DXF → JSON ;
- génération JSON → DXF ;
- génération PDF/DXF/rapports.

## Workflow cible

```txt
Photo réelle / Croquis / DXF / Manuel
→ agent spécialisé + script Python
→ JSON PD&I
→ validation humaine
→ ISO
→ PDF / DXF / impression
```

## Règle d'intégration

Chaque skill doit produire ou valider des données structurées, jamais seulement du texte libre.
'''
    write_if_changed(SKILLS_DOC, skills_doc, report)

    history_add = '''

## Patch 007a — Branding global + workspace intégré

Objectif :
- PD&I devient le branding de toute l'application SaaS, pas seulement l'interface ISO ;
- ajout du composant global `PdiBrandMark` ;
- correction des libellés de plein écran interne vers une logique `mode focus` / `retour accueil` ;
- documentation du rôle du dépôt `pipeline-design-skill` ;
- rappel : les calculs techniques sont réalisés par Python/règles déterministes, pas par IA générative.
'''
    old = read(PATCH_HISTORY)
    if "Patch 007a — Branding global" not in old:
        write_if_changed(PATCH_HISTORY, old.rstrip() + history_add + "\n", report)
    else:
        report.append(f"UNCHANGED {rel(PATCH_HISTORY)}")


def patch_gitignore(report: list[str]) -> None:
    append_unique_lines(GITIGNORE, [
        "",
        "# PD&I patch backups / temporary files",
        "*.bak",
        "*.bak_*",
        "*.backup",
        "*.old",
        "*.tmp",
        ".patch_backups/",
        "_archive/isometrie_backups/",
    ], report)


def scan(report: list[str]) -> None:
    report.append("\n--- POST-CHECK ---")
    for p in [APP, BRAND, WRAPPER, ENGINE, INDEX_HTML, SKILLS_DOC]:
        if p.exists():
            txt = read(p)
            report.append(f"OK {rel(p)} size={p.stat().st_size}")
            if p == ENGINE:
                report.append(f"  Version 4.8d1 count={txt.count('Version 4.8d1')}")
                report.append(f"  Retour accueil count={txt.count('Retour accueil')}")
                report.append(f"  workspaceFullscreen count={txt.count('workspaceFullscreen')}")
            if p == APP:
                report.append(f"  PdiBrandMark count={txt.count('PdiBrandMark')}")
        else:
            report.append(f"KO {rel(p)} absent")


def main() -> int:
    report: list[str] = []
    report.append("PD&I PATCH 007a — Branding global + workspace intégré")
    report.append(f"Date: {dt.datetime.now().isoformat()}")
    report.append(f"Root: {ROOT}")

    if not (ROOT / "package.json").exists():
        report.append("ERREUR: package.json introuvable. Exécuter depuis la racine du dépôt PD-I.")
        REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
        print("\n".join(report))
        return 2

    create_brand_component(report)
    patch_pdi_app(report)
    patch_engine_fullscreen(report)
    patch_wrapper(report)
    patch_index(report)
    write_docs(report)
    patch_gitignore(report)
    scan(report)

    report.append("\n--- TESTS RECOMMANDÉS ---")
    report.append("1. npm run build")
    report.append("2. npx tsc --noEmit si disponible")
    report.append("3. Vérifier logo visible dès l'accueil PD&I")
    report.append("4. Vérifier menu Isométrie / workspace ISO")
    report.append("5. Vérifier que le bouton ancien plein écran n'affiche plus une logique 'Quitter PD&I' incohérente")
    report.append("6. Vérifier mobile : pas de débordement horizontal")

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"\nRapport écrit: {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
