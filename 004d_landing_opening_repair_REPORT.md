# PATCH 004d — Réparation landing / page d’ouverture

Date : 2026-08-19T14:27:30

## Objectif
Restaurer la séquence complète : splash → accueil → boot → launcher → module.

## Fichiers modifiés
- `src/pdi/landing/PdiLandingV4.tsx`
- `src/pdi/landing/pdiLandingV4.css`
- `src/pdi/app/PdiUnifiedApp.tsx`

## Fichiers protégés
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx` : non modifié.
- `src/pdi/model/index.ts` : non utilisé pour remplacer V4.8d.
- Aucun fichier GitHub distant modifié.

## Validation attendue
```bash
npm install
npm run lint
npm run build
```

## Test visuel
1. Splash “Du croquis à l’isométrique normé…”
2. Clic “Let’s begin”
3. Accueil PD&I
4. Clic “Démarrer”
5. Boot / chargement
6. Launcher
7. Sélection “Nouveau Plan”
8. Ouverture du module isométrique V4.8d

## Rollback
```bash
cp src/pdi/app/PdiUnifiedApp.tsx.before004d src/pdi/app/PdiUnifiedApp.tsx
cp src/pdi/landing/PdiLandingV4.tsx.before004d src/pdi/landing/PdiLandingV4.tsx
cp src/pdi/landing/pdiLandingV4.css.before004d src/pdi/landing/pdiLandingV4.css
```
