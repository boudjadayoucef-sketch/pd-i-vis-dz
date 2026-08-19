# PATCH 006 — Ruban CAD universel

Date : 2026-08-19T18:05:45

## Audit avant patch
La sélection professionnelle existe déjà et ne doit pas être recréée.
Constats dans `IsometrieModuleV48d.tsx` :
- `selectedNodeIds`, `selectedSegmentIds`, `selectedDimensionIds` présents.
- Rectangle de sélection présent.
- Shift/Ctrl/Cmd additif présents.
- `copySelection`, `duplicateSelection`, `clipboardRef`, undo/redo présents.
- Patch 004 / 004b documentés dans `docs/PATCH_HISTORY.md`.

## Objectif du patch
Ajouter une couche d’interface CAD universelle type AutoCAD :
- Draw : Line, Polyline, Circle, Arc.
- Annotation : Text, Dimension.
- Modify : Copy, Duplicate, Rotate, Delete.
- Measure : Measure, BOM.
- Output : Print, JSON.

## Décision technique
- Les outils déjà sûrs appellent les fonctions V4.8d existantes.
- Les outils futurs affichent un statut “préparé” et attendent le patch 007.
- Aucun second moteur 2D n’est créé.
- Aucun remplacement de V4.8d.

## Fichier modifié
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`

## Fichiers protégés
- `src/pdi/model/index.ts` non utilisé comme moteur.
- Aucune suppression legacy.
- Aucun accès GitHub direct.

## Tests attendus
```bash
npm run lint
npm run build
```

## Validation visuelle Vercel
- Le workspace ISO affiche un ruban CAD horizontal en haut.
- Le rail vertical reste présent.
- Sélection pro toujours active.
- Line/Dimension/Copy/Duplicate/Rotate/Delete fonctionnent via V4.8d.
- Polyline/Circle/Arc/Text indiquent “préparé” sans fausse création.
