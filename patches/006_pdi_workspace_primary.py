#!/usr/bin/env python3
"""
PATCH 006 — PD&I Workspace Primary

Objectif
--------
Faire du workspace PD&I V4.8d l'interface principale du module
Isométries.

IMPORTANT :
- Ne modifie PAS IsometrieModuleV48d.tsx.
- Ne modifie PAS la logique du moteur V4.8d.
- Supprime uniquement le shell/wrapper intermédiaire.
- Le workspace V4.8d devient directement visible.
- L'interface reste en français.

Architecture :

SaaS PD&I
   |
   +-- Projets
   |
   +-- Isométries
          |
          +-- PdiIsometricEditor
                  |
                  +-- IsometrieModuleV48d
"""

from pathlib import Path
import shutil
import hashlib
import re
import sys
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]

EDITOR_CANDIDATES = [
    ROOT / "src/pdi/isometric/PdiIsometricEditor.tsx",
    ROOT / "src/pdi/isometrics/PdiIsometricEditor.tsx",
    ROOT / "src/components/pdi/PdiIsometricEditor.tsx",
]

ENGINE_CANDIDATES = [
    ROOT / "src/pdi/isometric/engine/IsometrieModuleV48d.tsx",
    ROOT / "src/pdi/isometric/IsometrieModuleV48d.tsx",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_existing(candidates):
    for path in candidates:
        if path.exists():
            return path

    # Recherche de secours
    matches = list(ROOT.glob("src/**/PdiIsometricEditor.tsx"))
    if matches:
        return matches[0]

    return None


def find_engine():
    for path in ENGINE_CANDIDATES:
        if path.exists():
            return path

    matches = list(ROOT.glob("src/**/IsometrieModuleV48d.tsx"))
    if matches:
        return matches[0]

    return None


def backup(path: Path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.with_suffix(path.suffix + f".bak_006_{timestamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def detect_export_name(engine_text: str):
    # export default function IsometrieModuleV48d
    m = re.search(
        r"export\s+default\s+function\s+([A-Za-z0-9_]+)",
        engine_text
    )
    if m:
        return m.group(1)

    # export default IsometrieModuleV48d
    m = re.search(
        r"export\s+default\s+([A-Za-z0-9_]+)\s*;",
        engine_text
    )
    if m:
        return m.group(1)

    # export function ...
    m = re.search(
        r"export\s+function\s+([A-Za-z0-9_]*Isometrie[A-Za-z0-9_]*)",
        engine_text
    )
    if m:
        return m.group(1)

    return "IsometrieModuleV48d"


def build_editor(engine: Path, editor: Path = None):
    engine_text = engine.read_text(encoding="utf-8")
    export_name = detect_export_name(engine_text)

    # Chemin relatif depuis PdiIsometricEditor.tsx vers le moteur.
    editor_dir = editor.parent if editor else engine.parent.parent
    relative = Path(
        __import__("os").path.relpath(engine, editor_dir)
    ).as_posix()

    if relative.endswith(".tsx"):
        relative = relative[:-4]

    if not relative.startswith("."):
        import_path = "./" + relative
    else:
        import_path = relative

    return f'''/**
 * PD&I — Éditeur isométrique principal
 *
 * PATCH 006
 *
 * Le moteur V4.8d est volontairement conservé intact.
 * Ce composant ne fait qu'exposer directement son workspace.
 */

import React from "react";
import {export_name} from "{import_path}";

export default function PdiIsometricEditor() {{
  return (
    <div
      className="pdi-v48d-primary-workspace"
      style={{{{
        width: "100%",
        height: "100%",
        minHeight: "100vh",
        overflow: "hidden",
        position: "relative",
      }}}}
    >
      <{export_name} />
    </div>
  );
}}
'''


def patch_css():
    """
    Ajoute un petit garde-fou CSS sans toucher au moteur.
    Il empêche le wrapper SaaS de recréer un scroll autour du workspace.
    """

    css_candidates = [
        ROOT / "src/index.css",
        ROOT / "src/styles.css",
        ROOT / "src/App.css",
    ]

    css = next((p for p in css_candidates if p.exists()), None)

    if css is None:
        print("INFO: Aucun fichier CSS global trouvé. CSS inline suffisant.")
        return

    marker = "/* PATCH 006 — PD&I WORKSPACE PRIMARY */"

    text = css.read_text(encoding="utf-8")

    if marker in text:
        print("CSS Patch 006 déjà présent.")
        return

    addition = f"""

{marker}

html,
body,
#root {{
  width: 100%;
  min-height: 100%;
}}

.pdi-v48d-primary-workspace {{
  width: 100%;
  height: 100%;
  min-height: 100vh;
  overflow: hidden;
}}

.pdi-v48d-primary-workspace > * {{
  width: 100%;
  height: 100%;
}}
"""

    css.write_text(text + addition, encoding="utf-8")
    print(f"CSS mis à jour : {css}")


def main():
    print("=" * 70)
    print("PATCH 006 — PD&I WORKSPACE PRIMARY")
    print("=" * 70)

    editor = find_existing(EDITOR_CANDIDATES)
    engine = find_engine()

    if editor is None:
        print("ERREUR : PdiIsometricEditor.tsx introuvable.")
        print("Aucune modification effectuée.")
        sys.exit(1)

    if engine is None:
        print("ERREUR : IsometrieModuleV48d.tsx introuvable.")
        print("Aucune modification effectuée.")
        sys.exit(1)

    print(f"Éditeur trouvé : {editor}")
    print(f"Moteur V4.8d trouvé : {engine}")

    engine_hash_before = sha256(engine)

    print(f"SHA256 moteur V4.8d : {engine_hash_before}")

    # Sauvegarde du wrapper actuel.
    backup_path = backup(editor)
    print(f"Sauvegarde wrapper : {backup_path}")

    # Remplacement UNIQUEMENT du wrapper.
    new_editor = build_editor(engine, editor)
    editor.write_text(new_editor, encoding="utf-8")

    patch_css()

    # Vérification : moteur strictement inchangé.
    engine_hash_after = sha256(engine)

    if engine_hash_before != engine_hash_after:
        print("ERREUR CRITIQUE : le moteur V4.8d a été modifié !")
        sys.exit(2)

    print()
    print("✓ Moteur V4.8d intact")
    print("✓ Wrapper PdiIsometricEditor remplacé")
    print("✓ Workspace V4.8d exposé directement")
    print("✓ Scroll global neutralisé")
    print("✓ Backup du wrapper créé")
    print()
    print("Étape suivante :")
    print("  npm run build")
    print()
    print("PATCH 006 TERMINÉ")
    print("=" * 70)


if __name__ == "__main__":
    main()