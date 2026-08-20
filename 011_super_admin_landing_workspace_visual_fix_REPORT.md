# PATCH 011 — Super Admin + corrections landing/workspace

Date: 2026-08-20T12:38:33

## Audit
- Landing existe dans le code mais peut sembler enlevée à cause du flag d’entrée app/sessionStorage.
- CSS parallax existe mais pas assez visible.
- Photo initiale absente des assets publics.
- Couleurs initiales PD&I encore variées : bleu/violet/orange.
- Grille rendue en lignes finies pouvant se dégrader au zoom.
- Barre basse métrés/statut encore visible.

## Corrections incluses
- Restauration flux landing commerciale.
- Parallax, grid drift, card animations et fallback visuel initial.
- Préparation chemin image : public/assets/pdi/landing/hero-dashboard.png.
- Couleur neutre gris AutoCAD pour nouveaux tubes/nœuds/objets 2D avant changement.
- Grille workspace transformée en pattern infini style CAD.
- Barre basse avec chiffres masquée.
- Ajout shell Super Admin Console selon workflow 011.

## À ajouter manuellement
AI Studio n’inclut pas les PNG/images : ajouter si possible :
public/assets/pdi/landing/hero-dashboard.png

## Tests
npm run lint
npm run build
Vercel preview
