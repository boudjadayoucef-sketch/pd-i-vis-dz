# PATCH 008 — Flux SaaS + onglets + sécurité

Date: 2026-08-20T10:04:56

## Checklist sécurité photos
1. clés API dans .env
2. .env dans .gitignore
3. rate limiting sur le login
4. RLS/règles sécurité activées
5. mots de passe hashés
6. droits vérifiés côté serveur
7. clé publique côté client seulement
8. HTTPS partout
9. sessions qui expirent
10. inputs validés
11. taille max des uploads
12. type de fichier vérifié
13. CORS configuré
14. erreurs détaillées coupées
15. console.log clean
16. message d'erreur unique
17. webhooks signés
18. dépendances à jour
19. email confirmé
20. backup auto

## Note assets
AI Studio n’inclut pas automatiquement les PNG/images. Ajouter manuellement les assets dans public/assets/pdi/ ou src/assets/images avant build/sync GitHub.

## Tests
- npm run lint
- npm run build
- Vercel preview
