# 008e_pdi_iso_precision_ux_workspace_fix

Patch appliqué le 20260816_180654

## Fichiers ajoutés

- `src/pdiIsoPrecisionUx.css`
- `src/pdiIsoUxRuntimePatch.js`
- `src/components/usePdiIsoPrecisionViewport.js`

## Tests

1. `npm run build`
2. Accueil → ISO
3. Vérifier bouton `← Accueil`
4. Vérifier header sans superposition
5. Tester zoom souris/touchpad
6. Tester dessin nœud + tube
7. Vérifier précision point/souris après zoom

## Note importante

La correction durable de précision doit centraliser les coordonnées avec :

```js
const rect = canvas.getBoundingClientRect();
const screenX = event.clientX - rect.left;
const screenY = event.clientY - rect.top;
const worldX = (screenX - pan.x) / zoom;
const worldY = (screenY - pan.y) / zoom;
```
