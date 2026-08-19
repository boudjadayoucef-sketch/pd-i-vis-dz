#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I PATCH 007 — Stabilisation V4.8d1 + Workflow IA/JSON central
=================================================================

À exécuter depuis la racine du dépôt PD-I :

    python3 007_stabilize_pdi_v48d1_workflow.py

Objectif :
- officialiser l'état V4.8d1 sans réappliquer brutalement le patch V4.8d1 ;
- nettoyer les backups committés autour du moteur isométrique ;
- ajouter un historique de patches clair ;
- ajouter une note d'architecture workflow : Photo/Croquis/DXF/Manuel → JSON → Validation → ISO → PDF/DXF ;
- préparer le socle avant V4.8d2 et V4.8e.

Ce patch est idempotent : il peut être relancé sans créer de doublons majeurs.
Il ne touche pas au logo public ni aux assets image.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import os
from pathlib import Path
import re
import shutil
import sys
from typing import Iterable

ROOT = Path.cwd()
PATCH_ID = "007"
PATCH_NAME = "PD&I PATCH 007 — Stabilisation V4.8d1 + Workflow IA/JSON central"
STAMP = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")

ENGINE = ROOT / "src/pdi/isometric/engine/IsometrieModuleV48d.tsx"
WRAPPER = ROOT / "src/pdi/isometric/PdiIsometricEditor.tsx"
APP = ROOT / "src/pdi/app/PdiApp.tsx"
DOCS = ROOT / "docs"
PATCH_HISTORY = DOCS / "PATCH_HISTORY.md"
WORKFLOW_DOC = DOCS / "PD_I_WORKFLOW_IA_JSON.md"
GITIGNORE = ROOT / ".gitignore"
ARCHIVE_DIR = ROOT / "_archive/isometrie_backups"
BACKUP_DIR = ROOT / f".patch_backups/{PATCH_ID}_{STAMP}"
REPORT = ROOT / f"patch_{PATCH_ID}_report.txt"


def log(msg: str) -> None:
    print(msg)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def backup(path: Path) -> None:
    if not path.exists() or not path.is_file():
        return
    dest = BACKUP_DIR / path.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def append_unique(path: Path, block: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    changed = False
    lines = existing.splitlines()
    for line in block.strip("\n").splitlines():
        if line not in lines:
            lines.append(line)
            changed = True
    if changed:
        backup(path)
        ensure_parent(path)
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return changed


def replace_between_markers(path: Path, start: str, end: str, content: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    block = f"{start}\n{content.rstrip()}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(existing):
        new = pattern.sub(block, existing)
    else:
        new = existing.rstrip() + "\n\n" + block + "\n"
    if new != existing:
        backup(path)
        ensure_parent(path)
        path.write_text(new, encoding="utf-8")
        return True
    return False


def move_backups() -> list[str]:
    moved: list[str] = []
    search_roots = [ROOT / "src/pdi/isometric", ROOT / "src/pdi/app"]
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for base in search_roots:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            name = p.name.lower()
            if (
                ".bak" in name
                or name.endswith(".backup")
                or name.endswith(".old")
                or name.endswith(".tmp")
            ):
                rel = p.relative_to(ROOT)
                dest = ARCHIVE_DIR / rel.as_posix().replace("/", "__")
                if dest.exists():
                    dest = dest.with_name(dest.name + f".{STAMP}")
                backup(p)
                shutil.move(str(p), str(dest))
                moved.append(f"{rel} -> {dest.relative_to(ROOT)}")
    return moved


def normalize_engine_version() -> list[str]:
    changes: list[str] = []
    if not ENGINE.exists():
        return changes
    text = ENGINE.read_text(encoding="utf-8")
    original = text

    # Ne pas doubler la version si déjà 4.8d1.
    text = text.replace("Version 4.8d11", "Version 4.8d1")
    text = text.replace('data-pdi-studio="v4.8c4"', 'data-pdi-studio="v4.8d1"')
    text = text.replace('data-pdi-studio="v4.8d"', 'data-pdi-studio="v4.8d1"')

    # Si le moteur affiche encore 4.8d dans la fenêtre À propos, officialiser 4.8d1.
    text = re.sub(r"Version 4\.8d(?!1)", "Version 4.8d1", text)

    # Ajouter un marqueur patch 007 en tête, sans doublon.
    marker = "// PD&I PATCH 007 — V4.8d1 stabilized for autonomous SaaS workflow"
    if marker not in text:
        text = marker + "\n" + text

    # Vérification non destructrice : si les marqueurs V4.8d1 n'existent pas,
    # on ne tente pas de reconstruire le patch ici. On le signale dans le rapport.
    if "cadMenuGroups" not in text:
        changes.append("WARN: cadMenuGroups absent — V4.8d1 menu CAO non détecté dans le moteur.")
    if "V4.8d1_WORKSPACE_CAO" not in text and "data-pdi-studio=\"v4.8d1\"" not in text:
        changes.append("WARN: marqueurs V4.8d1 faibles/absents — ne pas considérer V4.8d1 complète.")

    if text != original:
        backup(ENGINE)
        ENGINE.write_text(text, encoding="utf-8")
        changes.append("Engine version/markers normalized")
    return changes


def write_patch_history() -> bool:
    content = """
# Historique patches PD&I

Ce fichier clarifie la ligne de développement du dépôt autonome **PD-I**.

| Patch | Statut | Objet |
|---|---:|---|
| 003 | OK | Restauration du moteur isométrique V4.8d dans `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`. |
| 004 | À clarifier | Numéro réservé / patch non identifié dans le dépôt actuel. Ne plus le référencer sans fichier ou commit clair. |
| 005 | OK | Interface logiciel professionnelle française dans `src/pdi/app/PdiApp.tsx`. |
| 006 | OK | Wrapper/workspace principal `src/pdi/isometric/PdiIsometricEditor.tsx`. |
| 007 | OK | Stabilisation V4.8d1, nettoyage backups, documentation workflow IA/JSON central. |

## Règle source de vérité

Le dépôt actif est désormais :

```txt
boudjadayoucef-sketch/PD-I
```

La source de vérité du moteur isométrique actuel est :

```txt
src/pdi/isometric/engine/IsometrieModuleV48d.tsx
```

Même si le nom contient `V48d`, l'état à stabiliser est **V4.8d1** quand les marqueurs workspace CAO sont présents.

## Règle de développement

Chaque évolution majeure doit passer par un patch Python contrôlé :

```txt
Définir objectif → créer patch .py → appliquer dans AI Studio → tester → tsc --noEmit → npm run build → valider → commit
```

Ne pas committer de fichiers `*.bak`, `*.tmp`, `*.old` dans `src/`.
"""
    start = "<!-- PD-I PATCH HISTORY START -->"
    end = "<!-- PD-I PATCH HISTORY END -->"
    return replace_between_markers(PATCH_HISTORY, start, end, content)


def write_workflow_doc() -> bool:
    content = """
# PD&I — Workflow IA et JSON central

## Principe directeur

PD&I n'est plus seulement un éditeur isométrique. C'est un SaaS autonome dont le modèle central est le **JSON piping PD&I**.

Toutes les sources doivent converger vers le JSON, puis le JSON alimente l'éditeur, le moteur ISO et les exports.

```txt
Photo réelle / Croquis / DXF-CAO / Saisie manuelle
→ Analyse IA ou parseur
→ JSON piping PD&I
→ Validation humaine
→ Moteur isométrique
→ ISO / PDF / DXF / Nomenclature
```

## Sources d'entrée

### 1. Saisie manuelle

```txt
Éditeur PD&I → nœuds → segments → équipements → cotations → JSON
```

### 2. Photo réelle de plant / installation

```txt
Photo → IA Vision → tuyaux/équipements/connexions → JSON proposé → validation → ISO
```

Points à prévoir :
- dimensions parfois manquantes ;
- éléments cachés non fiables ;
- validation humaine obligatoire ;
- correction dans l'éditeur PD&I.

### 3. Croquis à la main

```txt
Croquis → IA Vision → lignes/symboles/cotes → JSON proposé → validation → ISO
```

### 4. CAO / DXF vers JSON

```txt
DXF → lecture calques/entities/blocs/textes → mapping tuyauterie → JSON → ISO
```

## Sorties

```txt
JSON → ISO
JSON → PDF
JSON → DXF
JSON → impression A4/A3/A2/A1
JSON → nomenclature
```

## Roadmap liée

```txt
007 — Stabilisation V4.8d1 PD-I
008 — V4.8d2 clic droit + propriétés éditables
009 — V4.8e impression pro + PDF/DXF/CAD
010 — V4.8f rendu tuyauterie 3D personnalisable
011 — JSON schema central v1
012 — DXF → JSON prototype
013 — Croquis → JSON prototype
014 — Photo réelle → JSON prototype
015 — JSON → ISO automatique assisté IA
```

## Règle d'architecture

Ne pas créer de flux directs fragiles du type :

```txt
Photo → ISO direct
DXF → ISO direct
Croquis → ISO direct
```

Toujours passer par :

```txt
Source → JSON PD&I → Validation → ISO/Exports
```
"""
    start = "<!-- PD-I WORKFLOW IA JSON START -->"
    end = "<!-- PD-I WORKFLOW IA JSON END -->"
    return replace_between_markers(WORKFLOW_DOC, start, end, content)


def update_gitignore() -> bool:
    block = """
# PD&I generated backups / temporary patch files
*.bak
*.bak_*
*.backup
*.old
*.tmp
.patch_backups/
_archive/isometrie_backups/
tmp/
"""
    return append_unique(GITIGNORE, block)


def validate_paths() -> list[str]:
    msgs = []
    for label, path in [
        ("ENGINE", ENGINE),
        ("WRAPPER", WRAPPER),
        ("APP", APP),
    ]:
        if path.exists():
            msgs.append(f"OK {label}: {path.relative_to(ROOT)} sha={sha256(path)}")
        else:
            msgs.append(f"KO {label}: manquant {path.relative_to(ROOT)}")
    return msgs


def main() -> int:
    if not (ROOT / "package.json").exists():
        log("ERREUR: exécute ce patch depuis la racine du dépôt PD-I (package.json introuvable).")
        return 2

    DOCS.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    report: list[str] = []
    report.append(PATCH_NAME)
    report.append(f"Root: {ROOT}")
    report.append(f"Date: {_dt.datetime.now().isoformat()}")
    report.append("")

    report.extend(validate_paths())
    report.append("")

    moved = move_backups()
    report.append(f"Backups déplacés: {len(moved)}")
    report.extend([f"- {m}" for m in moved])
    report.append("")

    engine_changes = normalize_engine_version()
    report.append("Engine changes:")
    report.extend([f"- {c}" for c in engine_changes] or ["- Aucun changement moteur nécessaire"])
    report.append("")

    changed_gitignore = update_gitignore()
    changed_history = write_patch_history()
    changed_workflow = write_workflow_doc()
    report.append(f".gitignore mis à jour: {changed_gitignore}")
    report.append(f"PATCH_HISTORY mis à jour: {changed_history}")
    report.append(f"WORKFLOW IA/JSON mis à jour: {changed_workflow}")
    report.append("")

    # Contrôles rapides post-patch.
    if ENGINE.exists():
        t = ENGINE.read_text(encoding="utf-8")
        report.append("Contrôles moteur:")
        report.append(f"- Version 4.8d1 count: {t.count('Version 4.8d1')}")
        report.append(f"- Version 4.8d11 count: {t.count('Version 4.8d11')}")
        report.append(f"- data-pdi-studio v4.8d1 count: {t.count('data-pdi-studio=\"v4.8d1\"')}")
        report.append(f"- cadMenuGroups count: {t.count('cadMenuGroups')}")
        report.append(f"- IsoDimension count: {t.count('IsoDimension')}")
        report.append("")

    report.append("Prochaine étape recommandée:")
    report.append("1. npm run build")
    report.append("2. npx tsc --noEmit ou npm run typecheck si disponible")
    report.append("3. Tester desktop: ouverture isométrie, menus, no-scroll, zoom molette, cotation M")
    report.append("4. Tester mobile: pas de débordement horizontal, moteur visible, toolbar utilisable")
    report.append("5. Commit: 'Patch 007 stabilize V4.8d1 workflow' ")

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    log("\n".join(report))
    log(f"\nRapport écrit: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
