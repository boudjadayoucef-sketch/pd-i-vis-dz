# PATCH 012 — Audit + licences + grille/métrés + déploiement alternatif

Date: 2026-08-20T13:12:30

## Audit version 8
- PATCH 011 présent.
- PATCH 012 non présent dans le ZIP fourni.
- Ancienne grille dynamique encore détectée.
- Barre status masquée, mais les cartes métrés visibles sur capture restent à supprimer/masquer.
- Vercel non adapté au réseau entreprise actuel.

## Patch 012
- Ajoute générateur de clés SaaS local temporaire.
- Remplace grille dynamique par pattern SVG stable.
- Masque status + cartes métrés basses.
- Ajoute document de stratégie déploiement hors Vercel.

## Déploiement recommandé
Priorité : build statique ZIP `dist/`, puis hébergement interne ou Cloud Run autre région si nécessaire.
