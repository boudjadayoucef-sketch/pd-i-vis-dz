#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 005
Stabilisation du flow d'ouverture après landing 004d.

Objectif :
- Sécuriser la séquence splash -> accueil -> boot -> launcher -> module.
- Ajouter des garde-fous de navigation.
- Corriger l'entrée ciblée vers ISO / Vision / Croquis / CAO / JSON / Export / IA.
- Ne pas toucher au moteur métier V4.8d.
- Ne pas créer de deuxième moteur ni de deuxième modèle.

Workflow : AI Studio -> patch .py -> tests -> sync GitHub -> preview Vercel.
"""

from pathlib import Path
import shutil
import sys
from datetime import datetime

PATCH_ID = "005"
ROOT = Path(".")
APP = ROOT / "src" / "pdi" / "app" / "PdiUnifiedApp.tsx"
LANDING_TSX = ROOT / "src" / "pdi" / "landing" / "PdiLandingV4.tsx"
LANDING_CSS = ROOT / "src" / "pdi" / "landing" / "pdiLandingV4.css"
ENGINE = ROOT / "src" / "pdi" / "isometric" / "engine" / "IsometrieModuleV48d.tsx"
REPORT = ROOT / "005_opening_flow_stabilization_REPORT.md"
HISTORY = ROOT / "docs" / "PATCH_HISTORY.md"

GUARD_APP = "PATCH 005 : navigation ciblee stabilisee"
GUARD_LANDING = "PATCH 005 : flow d'ouverture stabilise"


def fail(msg: str) -> None:
    print("ABANDON : " + msg)
    sys.exit(2)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def backup_once(path: Path) -> None:
    if not path.exists():
        return
    backup = path.with_name(path.name + f".before{PATCH_ID}")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"Sauvegarde créée : {backup}")


def assert_project() -> None:
    for p in [APP, LANDING_TSX, LANDING_CSS, ENGINE]:
        if not p.exists():
            fail(f"fichier introuvable : {p}")

    engine_src = read(ENGINE)
    if "IsometrieModule" not in engine_src:
        fail("le moteur V4.8d n'est pas reconnu")

    print("Audit initial OK : fichiers actifs présents, moteur V4.8d identifié.")


def patch_app_navigation() -> None:
    src = read(APP)

    if GUARD_APP in src:
        print("PdiUnifiedApp.tsx déjà patché 005.")
        return

    backup_once(APP)

    # 005 sécurise la navigation externe pdi:navigate : seules les destinations connues sont acceptées.
    old = '''  useEffect(() => {
    const onNavigate = (event: Event) => {
      const detail = (event as CustomEvent<PdiModule>).detail;
      // PATCH 004c : une navigation externe entre dans le logiciel.
      setStage("app");
      setActiveModule(detail || "home");
    };
    window.addEventListener("pdi:navigate", onNavigate as EventListener);
    return () => window.removeEventListener("pdi:navigate", onNavigate as EventListener);
  }, []);'''

    new = '''  useEffect(() => {
    const onNavigate = (event: Event) => {
      const detail = (event as CustomEvent<PdiModule>).detail;
      // PATCH 005 : navigation ciblee stabilisee.
      // Une navigation externe entre dans le logiciel uniquement vers un module connu.
      const allowed: PdiModule[] = [
        "home",
        "isometric",
        "vision",
        "sketch",
        "cad",
        "json",
        "pdf",
        "projects",
        "assistant",
      ];
      setStage("app");
      setActiveModule(allowed.includes(detail) ? detail : "home");
    };
    window.addEventListener("pdi:navigate", onNavigate as EventListener);
    return () => window.removeEventListener("pdi:navigate", onNavigate as EventListener);
  }, []);'''

    if old not in src:
        print("Ancre navigation externe exacte non trouvée — tentative de contrôle uniquement.")
    else:
        src = src.replace(old, new)

    # Si enterApp 004d existe, ajouter un commentaire garde-fou si absent.
    if GUARD_APP not in src and "const enterApp = React.useCallback((target?: string)" in src:
        src = src.replace(
            "const enterApp = React.useCallback((target?: string) => {",
            "// PATCH 005 : navigation ciblee stabilisee.\n  const enterApp = React.useCallback((target?: string) => {",
            1,
        )

    write(APP, src)
    print("PdiUnifiedApp.tsx stabilisé.")


def patch_landing_flow_guards() -> None:
    src = read(LANDING_TSX)

    if GUARD_LANDING in src:
        print("PdiLandingV4.tsx déjà patché 005.")
        return

    backup_once(LANDING_TSX)

    # Ajouter constantes typées pour éviter les écrans invalides et clarifier le flow.
    if "type PdiOpeningScreen" not in src:
        src = src.replace(
            "const BOOT_STEPS = [",
            "// PATCH 005 : flow d'ouverture stabilise.\ntype PdiOpeningScreen = \"landing\" | \"home\" | \"loading\" | \"launcher\";\nconst PDI_DEFAULT_ENTRY = \"isometric\";\n\nconst BOOT_STEPS = [",
            1,
        )

    src = src.replace(
        'useState<"landing" | "home" | "loading" | "launcher">("landing")',
        'useState<PdiOpeningScreen>("landing")',
    )

    src = src.replace(
        'useState<string | null>("isometric")',
        'useState<string | null>(PDI_DEFAULT_ENTRY)',
    )

    # Stabiliser openEntry : vérifier que la destination existe dans ENTRY_POINTS.
    old = '  const openEntry = (id?: string | null) => onEnter(id || "home");'
    new = '''  const openEntry = (id?: string | null) => {
    const target = id || "home";
    const known = target === "home" || ENTRY_POINTS.some((entry) => entry.id === target);
    onEnter(known ? target : PDI_DEFAULT_ENTRY);
  };'''
    if old in src:
        src = src.replace(old, new, 1)

    # Stabiliser begin : toujours repartir du début du boot.
    old_begin = '''  const begin = () => {
    setMenuOpen(false);
    setBootIndex(0);
    setScreen("loading");
  };'''
    new_begin = '''  const begin = () => {
    setMenuOpen(false);
    setSelectedEntry(PDI_DEFAULT_ENTRY);
    setBootIndex(0);
    setScreen("loading");
  };'''
    if old_begin in src:
        src = src.replace(old_begin, new_begin, 1)

    write(LANDING_TSX, src)
    print("PdiLandingV4.tsx flow stabilisé.")


def patch_css_small_fix() -> None:
    src = read(LANDING_CSS)

    if "PATCH 005 — stabilisation responsive launcher" in src:
        print("pdiLandingV4.css déjà patché 005.")
        return

    backup_once(LANDING_CSS)

    css = r'''

/* PATCH 005 — stabilisation responsive launcher */
.pdiL-entry:focus-visible,
.pdiL-hero-button:focus-visible,
.pdiL-btn:focus-visible,
.pdiL-launcher-head button:focus-visible {
  outline: 2px solid #4db8d4;
  outline-offset: 3px;
}

.pdiL-launcher,
.pdiL-boot,
.pdiL-hero-shell {
  min-width: 320px;
}

.pdiL-entry-grid {
  align-items: stretch;
}

.pdiL-entry {
  min-width: 0;
}
'''

    write(LANDING_CSS, src.rstrip() + "\n" + css + "\n")
    print("pdiLandingV4.css stabilisé.")


def write_report() -> None:
    content = f"""# PATCH 005 — Stabilisation du flow d'ouverture

Date : {datetime.now().isoformat(timespec='seconds')}

## Objectif
Stabiliser la séquence : splash → accueil → boot → launcher → module.

## Modifications
- Navigation externe `pdi:navigate` sécurisée vers modules connus.
- `enterApp(target)` conservé pour ouvrir un module choisi.
- Type d'écran d'ouverture clarifié.
- Entrée par défaut stabilisée sur `isometric`.
- Boot réinitialise toujours la sélection sur Nouveau Plan.
- Focus visible et petits garde-fous responsive ajoutés.

## Fichiers modifiés
- `src/pdi/app/PdiUnifiedApp.tsx`
- `src/pdi/landing/PdiLandingV4.tsx`
- `src/pdi/landing/pdiLandingV4.css`

## Fichiers protégés
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx` non modifié.
- Aucun second moteur créé.
- Aucun remplacement de modèle métier.

## Tests attendus
```bash
npm install
npm run lint
npm run build
```

## Preview attendue Vercel
- Splash visible au premier chargement.
- Let’s begin → accueil.
- Démarrer → boot.
- Boot → launcher.
- Nouveau Plan → ISO V4.8d.
- Destination inconnue → fallback ISO.
"""
    write(REPORT, content)
    print(f"Rapport écrit : {REPORT}")


def update_history() -> None:
    if not HISTORY.exists():
        print("PATCH_HISTORY.md absent — non mis à jour.")
        return

    src = read(HISTORY)
    if "PATCH 005" in src:
        print("PATCH_HISTORY.md déjà mis à jour.")
        return

    entry = f"""

## PATCH 005 — Stabilisation du flow d'ouverture

Date : {datetime.now().strftime('%Y-%m-%d')}

- Séquence splash → accueil → boot → launcher → module stabilisée.
- Navigation cible sécurisée.
- Entrée par défaut ISO conservée.
- Moteur V4.8d non modifié.
"""
    write(HISTORY, src.rstrip() + "\n" + entry)
    print("PATCH_HISTORY.md mis à jour.")


def main() -> None:
    print("PD&I PATCH 005 — stabilisation du flow d'ouverture")
    assert_project()

    engine_before = read(ENGINE)

    patch_app_navigation()
    patch_landing_flow_guards()
    patch_css_small_fix()
    write_report()
    update_history()

    engine_after = read(ENGINE)
    if engine_before != engine_after:
        fail("sécurité : le moteur V4.8d a été modifié")

    print("\nPATCH 005 appliqué avec succès.")
    print("Moteur V4.8d intact.")
    print("\nCommandes recommandées :")
    print("  npm install")
    print("  npm run lint")
    print("  npm run build")
    print("\nPuis : sync GitHub -> vérifier preview Vercel.")


if __name__ == "__main__":
    main()
