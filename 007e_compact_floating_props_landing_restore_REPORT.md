# PATCH 007e — Palette propriétés compacte + restauration landing/accueil

Date : 2026-08-20T06:41:08

## Audit
- La landing n'était pas supprimée : `PdiLandingV4.tsx` et CSS existent.
- Le problème probable venait du stage enregistré en sessionStorage (`pdi.stage.v4 = app`) et du workspace ISO plein écran.
- Le panneau propriétés 2D restait latéral et trop grand.

## Corrections
- Ajout palette flottante compacte, taille proche menu clic droit.
- Palette noire/grise, minimaliste, déplaçable sur le plan.
- Champs limités aux données à saisir.
- Ancien panneau propriétés 2D latéral masqué.
- Navigation landing restaurée via `pdi:navigate` detail `landing`.
- Bouton/menu Landing ajouté.

## Validation
1. Sélectionner objet 2D : petite palette flottante apparaît.
2. Glisser l'entête PROPERTIES : la palette se déplace.
3. Modifier couleur/texte/taille : l'objet se met à jour.
4. Menu CAD > Landing : la landing doit revenir.
5. Menu CAD > Accueil : la page accueil doit revenir.
