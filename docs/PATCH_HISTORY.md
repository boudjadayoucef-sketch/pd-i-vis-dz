

## Patch 007a — Branding global + workspace intégré

Objectif :
- PD&I devient le branding de toute l'application SaaS, pas seulement l'interface ISO ;
- ajout du composant global `PdiBrandMark` ;
- correction des libellés de plein écran interne vers une logique `mode focus` / `retour accueil` ;
- documentation du rôle du dépôt `pipeline-design-skill` ;
- rappel : les calculs techniques sont réalisés par Python/règles déterministes, pas par IA générative.

## Patch 007b — ISO intégré + logo public unique

Correctifs :
- l'éditeur ISO ne s'ouvre plus automatiquement en plein écran ;
- le logo produit global est servi depuis `/public` via `PdiBrandMark` ;
- éviter les doubles logos entre le shell SaaS et la topbar interne ISO ;
- le mode plein écran devient un mode focus volontaire, pas l'ouverture par défaut.

Règle : PD&I est toute l'application SaaS. L'ISO est un workspace interne.

## Patch 007c — Shell unifié + accueil + ISO principal

Décision : arrêter la coexistence de deux logiciels (shell SaaS + ancien ISO intégré).

- PD&I devient un seul logiciel.
- La page d'accueil propose : nouveau projet, Vision PD&I, croquis, import DXF/PDF/JSON, exports.
- Le module ISO devient le workspace principal plein écran lorsqu'on le lance.
- Le bouton de sortie ISO devient `Retour accueil`.
- Le dépôt `pipeline-design-skill` est prévu comme équipe d'agents spécialisés.
- PD&I est l'orchestrateur ; les calculs techniques sont faits par Python.

## Patch 007d — ISO plein écran = mode principal

Correctif après test utilisateur :
- le mode non-fullscreen de l'ancien ISO est supprimé de l'usage normal ;
- l'ISO doit s'ouvrir comme workspace principal plein écran ;
- la barre menus Fichier / Édition / Affichage / Dessin / Cotation / Alignement / Insertion / Impression / Export / Outils doit rester visible ;
- le bouton de sortie doit être `Retour accueil` ;
- les tooltips doivent être visibles sur les boutons ;
- le bandeau descriptif `Concepteur & Schéma...` ne doit plus apparaître dans le workspace principal.

## Patch 007e — Optimisation espace ISO + accueil carousel

Correctifs :
- retirer le bouton retour/quitter du workspace ISO ;
- garder l'ISO comme workspace principal plein écran ;
- réduire l'encombrement des compteurs bas ;
- déplacer l'information `Vue isométrique 30°` vers la barre noire du haut ;
- supprimer la phrase d'aide `MAIN = déplacer...` dans le workspace ;
- compléter la grille pour couvrir toute la zone ;
- remplacer le bloc `Architecture cible` de l'accueil par un carousel vertical de fonctionnalités ;
- rendre le logo accueil robuste avec plusieurs chemins `/public`.


## Patch 004 — Edition professionnelle (clic droit, proprietes, presse-papiers)

- Menu contextuel ISO : Proprietes, Copier, Couper, Coller, Dupliquer, Rotation, Retourner, Supprimer.
- Panneau de proprietes reel : X / Y / Z, elevation, DN, type, tag, rotation, ports, connexions, soudures W00x.
- Proprietes multi-selection sans residu d'un objet precedent.
- Presse-papiers copier / couper / coller / dupliquer avec NOUVEAUX IDs
  (ports et lineId canonises par normalizedGraphPorts, positions calees par snapIsoV4).
- Deplacement clavier (fleches, Alt = Z, Shift = pas x4).
- Undo par operation logique + Redo (Ctrl/Cmd+Shift+Z, Ctrl/Cmd+Y).
- Suppression sans topologie orpheline (purge des cotations support).
- Raccourcis Cmd (macOS) et Ctrl (Windows/Linux). Conflit de la touche F leve.
- Rectangle de selection (fenetre et traversee) sur noeuds et tronçons.
- Aucune regression du trackpad Mac : le gestionnaire wheel n'a pas ete touche.

## Patch 004b — Cotations, selection et correctif du chemin de suppression

- CORRECTIF : la suppression d'une cotation passait par setDimensions() puis
  commitGraph() avec l'etat "dimensions" non rafraichi, ce qui reintroduisait la
  cotation supprimee et creait deux entrees d'historique pour une seule operation.
  La suppression suit desormais un chemin logique unique (commitGraph).
- CORRECTIF : le message des cotations orphelines etait ecrase immediatement.
- Selection multiple de cotations (selectedDimensionIds), Shift+clic additif.
- Le rectangle de selection capture aussi les cotations (fenetre et traversee),
  via resolveDimensionAnchor + isoProjectV4 + lineSegmentIntersectsBox.
- Presse-papiers : les cotations entierement contenues dans la selection sont
  copiees, coupees, collees et dupliquees avec NOUVEAUX IDs et ancres remappees.
  Une cotation dont une seule ancre est selectionnee n'est jamais clonee.
- Aucune nouvelle logique metier, aucun offset arbitraire, aucun second modele.

## Patch 004c — Interface publique (landing v4) portee en composants React

- Nouveaux fichiers : `src/pdi/landing/PdiLandingV4.tsx` et `src/pdi/landing/pdiLandingV4.css`.
- La page d'accueil publique est desormais un composant React reel, plus un bundle HTML injecte :
  une seule source de verite d'interface.
- Aucune barre laterale sur la page publicitaire : la coquille applicative
  (barre superieure + navigation) n'est montee qu'apres l'entree dans le logiciel.
- Banniere d'information pleine largeur en quatre couleurs (ISO, Vision, Croquis, JSON).
- Barre de navigation flottante minimaliste, avec menu burger mobile.
- Section "PD&I en 4 temps" conservee : Capturer, Reconnaitre, Construire, Livrer.
- Bento minimaliste des capacites, et pied de page minimaliste a cinq colonnes.
- Flux : landing -> entree -> accueil -> "Nouveau projet isometrique" -> editeur V4.8d.
- Etape memorisee en sessionStorage (`pdi.stage.v4`) : aucune interference avec les
  cles localStorage d'autosauvegarde du moteur.
- Hygiene : la sauvegarde `.before004b` est sortie de `src/` vers `backups/`.
- Garde-fou verifie par le script : le moteur `IsometrieModuleV48d.tsx` est
  STRICTEMENT inchange (comparaison octet a octet avant/apres).


## PATCH 004d — Réparation landing / page d’ouverture

Date : 2026-08-19

- Restauration de la séquence complète splash → accueil → boot → launcher → module.
- Ajout d’une entrée ciblée depuis la landing vers les modules existants.
- Moteur V4.8d non modifié.
- Aucun remplacement du modèle métier.


## PATCH 005 — Stabilisation du flow d'ouverture

Date : 2026-08-19

- Séquence splash → accueil → boot → launcher → module stabilisée.
- Navigation cible sécurisée.
- Entrée par défaut ISO conservée.
- Moteur V4.8d non modifié.


## PATCH 006 — Ruban CAD universel

Date : 2026-08-19

- Audit confirmé : la sélection professionnelle existe déjà via Patch 004/004b.
- Ajout d’un ruban CAD universel visible : Draw, Annotation, Modify, Measure, Output.
- Les outils sûrs réutilisent V4.8d ; les outils futurs sont marqués préparés.
- Aucun second moteur 2D, aucune duplication de sélection/topologie/projection.
