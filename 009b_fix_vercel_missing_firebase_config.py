#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PD&I — PATCH 009b
Fix Vercel build: firebase-applet-config.json manquant.

Erreur Vercel observée :
Could not resolve "../../firebase-applet-config.json"
src/lib/firebase-admin.ts: import firebaseConfig from '../../firebase-applet-config.json'

Cause :
- Le fichier JSON local n'est pas présent dans le repo/build Vercel.
- Un fichier de config Firebase ne doit pas être une dépendance obligatoire du build.
- En production, utiliser les variables d'environnement Vercel/Firebase.

Correction :
- Remplacer l'import JSON dur par une configuration lue depuis import.meta.env.
- Garder des valeurs demo non secrètes pour éviter crash build.
- Ne pas toucher au moteur V4.8d.
"""
from pathlib import Path
import shutil, sys
from datetime import datetime

ROOT=Path('.')
TARGET=ROOT/'src/lib/firebase-admin.ts'
REPORT=ROOT/'009b_vercel_firebase_config_fix_REPORT.md'
HISTORY=ROOT/'docs/PATCH_HISTORY.md'

def fail(m):
    print('ABANDON: '+m)
    sys.exit(2)

def read(p): return p.read_text(encoding='utf-8')
def write(p,c):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(c,encoding='utf-8')

def backup(p):
    b=p.with_name(p.name+'.before009b')
    if not b.exists():
        shutil.copy2(p,b)
        print('Sauvegarde:',b)

def main():
    print('PD&I PATCH 009b — fix Vercel firebase config')
    if not TARGET.exists():
        fail('src/lib/firebase-admin.ts introuvable')
    src=read(TARGET)
    if 'PATCH 009b — Vercel-safe Firebase config' in src:
        print('Déjà patché')
    else:
        backup(TARGET)
        # Remplacement robuste : on supprime l'import JSON et on injecte une config env-safe.
        src=src.replace("import firebaseConfig from '../../firebase-applet-config.json';\n", '')
        src=src.replace("import firebaseConfig from \"../../firebase-applet-config.json\";\n", '')
        if 'firebaseConfig' not in src:
            fail('firebaseConfig non trouvé après suppression import — vérifier fichier manuellement')
        env_block="""// PATCH 009b — Vercel-safe Firebase config.\n// Ne jamais dépendre d'un JSON local absent du build.\n// Config publique Firebase via variables Vercel VITE_FIREBASE_* ; fallback demo non secret pour build.\nconst firebaseConfig = {\n  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'demo-api-key',\n  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'demo.firebaseapp.com',\n  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'demo-project',\n  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'demo.appspot.com',\n  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '000000000000',\n  appId: import.meta.env.VITE_FIREBASE_APP_ID || 'demo-app-id',\n};\n\n"""
        # Placer après les imports initiaux.
        lines=src.splitlines(True)
        idx=0
        while idx < len(lines) and (lines[idx].startswith('import ') or lines[idx].strip()=='' or lines[idx].startswith('//')):
            idx+=1
        src=''.join(lines[:idx])+env_block+''.join(lines[idx:])
        write(TARGET,src)
        print('firebase-admin.ts corrigé')
    report=f"""# PATCH 009b — Fix Vercel Firebase config\n\nDate: {datetime.now().isoformat(timespec='seconds')}\n\n## Erreur corrigée\nVercel échouait sur :\n\n```text\nCould not resolve \"../../firebase-applet-config.json\"\nsrc/lib/firebase-admin.ts\n```\n\n## Cause\nLe build dépendait d'un fichier JSON local absent du repo/Vercel.\n\n## Correction\n- Suppression de l'import direct `../../firebase-applet-config.json`.\n- Lecture via variables d'environnement `VITE_FIREBASE_*`.\n- Fallback demo non secret pour permettre le build.\n\n## Variables Vercel à ajouter plus tard\n```text\nVITE_FIREBASE_API_KEY\nVITE_FIREBASE_AUTH_DOMAIN\nVITE_FIREBASE_PROJECT_ID\nVITE_FIREBASE_STORAGE_BUCKET\nVITE_FIREBASE_MESSAGING_SENDER_ID\nVITE_FIREBASE_APP_ID\n```\n\n## Sécurité\n- Ne pas commiter de clés privées.\n- `.env` doit rester dans `.gitignore`.\n- Les clés Firebase client sont publiques, mais les droits doivent être protégés par règles serveur/Firebase.\n\n## Tests\n```bash\nnpm run lint\nnpm run build\n```\n"""
    write(REPORT,report)
    if HISTORY.exists() and 'PATCH 009b — Fix Vercel Firebase config' not in read(HISTORY):
        write(HISTORY, read(HISTORY).rstrip()+"\n\n## PATCH 009b — Fix Vercel Firebase config\n\n- Suppression dépendance au fichier local firebase-applet-config.json.\n- Config Firebase lue via variables Vercel VITE_FIREBASE_*.\n- Build Vercel débloqué sans exposer de secrets privés.\n")
    print('PATCH 009b terminé')

if __name__=='__main__':
    main()
