# PATCH 009b — Fix Vercel Firebase config

Date: 2026-08-20T10:50:01

## Erreur corrigée
Vercel échouait sur :

```text
Could not resolve "../../firebase-applet-config.json"
src/lib/firebase-admin.ts
```

## Cause
Le build dépendait d'un fichier JSON local absent du repo/Vercel.

## Correction
- Suppression de l'import direct `../../firebase-applet-config.json`.
- Lecture via variables d'environnement `VITE_FIREBASE_*`.
- Fallback demo non secret pour permettre le build.

## Variables Vercel à ajouter plus tard
```text
VITE_FIREBASE_API_KEY
VITE_FIREBASE_AUTH_DOMAIN
VITE_FIREBASE_PROJECT_ID
VITE_FIREBASE_STORAGE_BUCKET
VITE_FIREBASE_MESSAGING_SENDER_ID
VITE_FIREBASE_APP_ID
```

## Sécurité
- Ne pas commiter de clés privées.
- `.env` doit rester dans `.gitignore`.
- Les clés Firebase client sont publiques, mais les droits doivent être protégés par règles serveur/Firebase.

## Tests
```bash
npm run lint
npm run build
```
