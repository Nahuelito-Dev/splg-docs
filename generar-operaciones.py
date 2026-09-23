#!/usr/bin/env python3
"""Rehace la sección de Operaciones del documento de Diseño (§4.15).

    python3 generar-operaciones.py

La plantilla de la cátedra pide, junto al diagrama de interacción, la lista de
operaciones del sistema con su firma. Sale de los diagramas de secuencia del
Documento 2, así que no se escribe a mano: cada vez que un diagrama declara una
operación nueva, se vuelve a correr esto.
"""
import re, glob, os

D = os.path.dirname(os.path.abspath(__file__)) + "/"

a = open(D + "2-Analisis.md", encoding="utf-8").read()
bloques = re.findall(
    r'^#{4,5}\s*DSS\s*[—-]\s*(CU-[\d\s/CU-]+?):\s*(.+?)$\s*\n+\*\*Actor:\*\*\s*(.+?)\n'
    r'\*\*Operaciones del sistema:\*\*\s*(.+?)\n', a, re.M)
contratos = {c.strip() for c in re.findall(r'####\s*.*Contrato:\s*`([^`]+?)\(', a)}
con_dsd = {cu for f in glob.glob(D + "diagramas/DSD_*.mmd")
           for cu in re.findall(r'CU-\d+', os.path.basename(f))}

def actor_corto(s):
    s = re.sub(r'\s*\(.*?\)', '', s).split(",")[0].split(" con ")[0].strip()
    return s or "—"

filas, vistas = [], set()
for cu, nom, act, ops in bloques:
    cus = re.findall(r'CU-\d+', cu)
    for firma in re.findall(r'`([^`]+)`', ops):
        if firma in vistas: continue
        vistas.add(firma)
        filas.append((firma, " / ".join(cus), actor_corto(act),
                      "sí" if all(c in con_dsd for c in cus) else "—",
                      "sí" if firma.split("(")[0] in contratos else "—"))
filas.sort(key=lambda f: f[0].lower())
c_con = sum(1 for f in filas if f[4] == "sí")
c_dsd = sum(1 for f in filas if f[3] == "sí")

s = ["### 4.15 Operaciones", "",
 "Cada operación del sistema con su firma. Una operación del sistema es un mensaje que",
 "un actor le manda al sistema y que aparece como tal en el diagrama de secuencia del",
 "Documento 2. El contrato de las que lo tienen, con precondiciones y postcondiciones,",
 "está en el Documento 2 · §2.2; el diagrama de interacción que muestra cómo se resuelve",
 "por dentro está en §4 de este documento.", "",
 f"Son **{len(filas)} operaciones**. **{c_dsd}** tienen su diagrama de interacción y",
 f"**{c_con}** tienen contrato escrito.", "",
 "| Operación | Caso de uso | Actor que la invoca | Diagrama de interacción | Contrato |",
 "|---|---|---|---|---|"]
s += [f"| `{f[0]}` | {f[1]} | {f[2]} | {f[3]} | {f[4]} |" for f in filas]
s.append("")
texto = "\n".join(s)

d = open(D + "3-Diseño.md", encoding="utf-8").read()
ini = d.index("### 4.15 Operaciones")
fin = d.index("\n## 5. Diagrama de Clases de Diseño")
open(D + "3-Diseño.md", "w", encoding="utf-8").write(d[:ini] + texto + d[fin:])
print(f"§4.15: {len(filas)} operaciones | {c_dsd} con diagrama | {c_con} con contrato")
