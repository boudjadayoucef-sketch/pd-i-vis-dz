# PATCH 010 — Auth simulée + suppression accès direct + fix boutons noirs

Date: 2026-08-20T12:20:04

## Audit
- PATCH 008/009 détectés.
- Landing et PdiUnifiedApp présents.

## Corrections demandées
- Bouton Commencer/Démarrer renommé et accès direct neutralisé.
- Accès ISO/Vision/CAD bloqué si utilisateur guest/pending_email.
- Ajout gateway Connexion / Créer compte / Activation / Démo.
- Correction renforcée des boutons noirs sur landing et app.

## Flux ajouté
Créer compte → pending_email → token activation simulé → activer compte → client actif.

## Sécurité
- Message d'erreur unique.
- Email confirmé simulé.
- Inputs minimum validés.
- Pas de secret dans le code.
- Variables Firebase via Vercel/env.

## Note assets
AI Studio n’inclut pas automatiquement les PNG/images. Ajouter manuellement les assets dans public/assets/pdi/ ou src/assets/images avant build/sync GitHub.

## Tests
npm run lint
npm run build
Vercel preview
