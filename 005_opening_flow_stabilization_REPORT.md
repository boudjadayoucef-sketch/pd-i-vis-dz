# PATCH 005 — Stabilisation du flow d'ouverture

Date : 2026-08-19T15:38:21

## Objectif
Stabiliser la séquence : splash → accueil → boot → launcher → module.

## Modifications
- Navigation externe `pdi:navigate` sécurisée vers modules connus.
- `enterApp(target)` conservé pour ouvrir un module choisi.
- Type d'écran d'ouverture clarifié.
- Entrée par défaut stabilisée sur `isometric`.
- Boot réinitialise toujours la sélection sur Nouveau Plan.
- Focus visible et petits garde-fous responsive ajoutés.

## Fichiers modifiés
- `src/pdi/app/PdiUnifiedApp.tsx`
- `src/pdi/landing/PdiLandingV4.tsx`
- `src/pdi/landing/pdiLandingV4.css`

## Fichiers protégés
- `src/pdi/isometric/engine/IsometrieModuleV48d.tsx` non modifié.
- Aucun second moteur créé.
- Aucun remplacement de modèle métier.

## Tests attendus
```bash
npm install
npm run lint
npm run build
```

## Preview attendue Vercel
- Splash visible au premier chargement.
- Let’s begin → accueil.
- Démarrer → boot.
- Boot → launcher.
- Nouveau Plan → ISO V4.8d.
- Destination inconnue → fallback ISO.
