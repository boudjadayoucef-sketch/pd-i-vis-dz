# PATCH 007 — Fondation géométrie 2D réelle

Date : 2026-08-19T18:23:27

## Audit avant patch
- La sélection professionnelle existe déjà : Patch 004 / 004b.
- `selectedNodeIds`, `selectedSegmentIds`, `selectedDimensionIds` présents.
- Copier / couper / coller / dupliquer déjà existants.
- Ce patch ne refait pas la sélection.

## Objectif
Créer une couche 2D réelle, persistante et exportable :
- `Cad2dEntity`
- `Cad2dLayer`
- `cad2dEntities`
- `cad2dLayers`
- `selectedCad2dIds`

## Entités préparées
- line
- polyline
- circle
- arc
- text

## Important
- Pas de deuxième moteur piping.
- Pas de remplacement V4.8d.
- Mapping 2D -> piping graph reporté au patch 008/009.
- Les entités 2D sont des objets projet avec IDs réels, pas seulement SVG.

## Fichier modifié
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`

## Validation attendue
```bash
npm run lint
npm run build
```

## Validation visuelle
- Ruban CAD : Line / Polyline / Circle / Arc / Text créent des objets 2D basiques.
- Les objets apparaissent dans le plan.
- Clic sur objet 2D le sélectionne.
- Export JSON contient `model.cad2d`.
- Import JSON restaure `model.cad2d`.
