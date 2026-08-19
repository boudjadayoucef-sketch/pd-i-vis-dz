# PATCH 007b — Objets 2D manipulables et configurables

Date : 2026-08-19T19:58:04

## Problème constaté
- Les objets 2D apparaissaient.
- Ils n'étaient pas manipulables/configurables.
- Le texte ne s'affichait pas correctement.

## Corrections
- Sélection objet 2D fiabilisée.
- Déplacement clavier des objets 2D sélectionnés.
- Duplication / suppression d'objets 2D.
- Panneau propriétés 2D : calque, couleur, texte, rayon, intention, Z futur.
- Rendu texte corrigé avec fond et `pointerEvents` contrôlé.
- Boutons ruban Duplicate/Delete priorisent les objets 2D sélectionnés.

## Fichier modifié
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx`

## Protégé
- Graphe piping V4.8d non remplacé.
- Pas de deuxième moteur piping.
- Mapping 2D -> piping toujours reporté au patch suivant.

## Tests attendus
```bash
npm run lint
npm run build
```

## Validation Vercel
- Créer Line / Polyline / Circle / Text.
- Cliquer objet 2D : panneau Propriétés 2D apparaît.
- Modifier couleur / texte / rayon.
- Flèches clavier déplacent l'objet.
- Dup / Del fonctionnent.
- Le texte est visible.
