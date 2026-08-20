# PATCH 007d — Drag/resize souris et propriétés CAD compactes

Date : 2026-08-19T20:40:17

## Ajouts
- Déplacement souris global des objets 2D.
- Grips de base pour redimensionnement / édition : ligne, polyline, cercle, texte.
- Redimensionnement souris : endpoints ligne, sommets polyline, centre/rayon cercle, insertion texte.
- Panneau propriétés compact modulaire style CAD.
- Actions utiles : rotate, scale, mirror, duplicate, delete, front/back, lock.

## Non fait volontairement
- Trim/extend/offset réel.
- Saisie numérique type ligne de commande.
- Mapping 2D -> piping graph.

## Fichier modifié
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`
