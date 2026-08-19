import fs from 'fs';

const filePath = 'src/components/Calculators.tsx';
let content = fs.readFileSync(filePath, 'utf-8').replace(/\r\n/g, '\n');

const targetStr = `<span className="label">Abri Télé & Clôture :</span><br />
                                  <span className="value">ABRI {teleShelterType === "01_porte" ? "01 PORTE" : "02 PORTES"} | PANNEAUX H={fenceHeight}m</span>`;

const replacementStr = `<span className="label">Abri Télé, Clôture & Accès :</span><br />
                                  <span className="value">ABRI {teleShelterType === "01_porte" ? "01 PORTE" : "02 PORTES"} | CLÔTURE PROFILÉE (e=12mm) | {nbPortails5m}x PORTAIL 5m | {nbPortillons1m}x PORTILLON 1m</span>`;

content = content.replace(targetStr, replacementStr);

fs.writeFileSync(filePath, content, 'utf-8');
console.log("Updated cartouche!");
