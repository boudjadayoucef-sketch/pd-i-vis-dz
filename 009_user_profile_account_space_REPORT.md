# PATCH 009 — Profil utilisateur + espace compte

Date: 2026-08-20T10:33:31

## Audit
PATCH 008 détecté : onglets, authMode, menu compte.

## Ajouts
- Module Profil utilisateur.
- Menu compte enrichi : Voir profil, Mes projets, Abonnement, Sécurité, Déconnexion.
- Carte identité et carte compte.
- Page sécurité avec checklist SaaS.
- Préparation future Firebase users/profiles/subscriptions.

## Checklist sécurité conservée
1. clés API dans .env
2. .env dans .gitignore
3. rate limiting login
4. RLS/règles base
5. mots de passe hashés
6. droits serveur
7. clé publique côté client
8. HTTPS partout
9. sessions expirantes
10. inputs validés
11. taille max uploads
12. type fichier vérifié
13. CORS
14. erreurs détaillées coupées
15. console.log clean
16. message d'erreur unique
17. webhooks signés
18. dépendances à jour
19. email confirmé
20. backup automatique

## Note assets
AI Studio n’inclut pas automatiquement les PNG/images. Ajouter manuellement les assets dans public/assets/pdi/ ou src/assets/images avant build/sync GitHub.

## Tests
- npm run lint
- npm run build
- Vercel preview
