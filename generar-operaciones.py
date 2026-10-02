#!/usr/bin/env python3
"""Rehace la sección de Operaciones del documento de Diseño (§4.15).

    python3 generar-operaciones.py

La plantilla de la cátedra pide, junto al diagrama de interacción, la lista de
operaciones del sistema con su firma. La fuente es el catálogo canónico de
`material-de-trabajo/operaciones-sistema.json`, el mismo que el Documento 2 §2.2
publica y que `verificar-conformidad.py` cruza contra los diagramas de secuencia y
los contratos: no se escribe a mano.
"""
import re, glob, os, json

D = os.path.dirname(os.path.abspath(__file__)) + "/"

cat = json.load(open(D + "material-de-trabajo/operaciones-sistema.json", encoding="utf-8"))
actores, ops = cat["actores"], cat["operaciones"]
con_dsd = {cu for f in glob.glob(D + "diagramas/DSD_*.mmd")
           for cu in re.findall(r'CU-\d+', os.path.basename(f))}

def quien(o):
    return ", ".join(f"{actores[a]} ({a})" for a in o["actores"])

filas = []
for o in sorted(ops, key=lambda o: o["nombre"].lower()):
    dsd = "sí" if all(c in con_dsd for c in o["casosDeUso"]) else "—"
    filas.append((o, dsd))
c_con = sum(1 for o, _ in filas if o["cambiaEstado"])
c_dsd = sum(1 for _, d in filas if d == "sí")

s = ["### 4.15 Operaciones", "",
 "Cada operación del sistema con su firma. Una operación del sistema es un mensaje que",
 "un actor le manda al sistema y que aparece como tal en el diagrama de secuencia del",
 "Documento 2. El catálogo, con una sola firma por operación, y el contrato de las que",
 "modifican el modelo conceptual, con precondiciones y postcondiciones, están en el",
 "Documento 2 · §2.2; el diagrama de interacción que muestra cómo se resuelve por dentro",
 "está en §4 de este documento.", "",
 f"Son **{len(filas)} operaciones**. **{c_dsd}** tienen su diagrama de interacción y",
 f"**{c_con}** tienen contrato: son las que cambian el estado del sistema.", "",
 "| Operación | Caso de uso | Actor que la invoca | Diagrama de interacción | Contrato |",
 "|---|---|---|---|---|"]
s += [f"| `{o['firmaConTipos']}` | {' / '.join(o['casosDeUso'])} | {quien(o)} | {d} | "
      f"{'sí' if o['cambiaEstado'] else '—'} |" for o, d in filas]
s.append("")
texto = "\n".join(s)

d = open(D + "3-Diseño.md", encoding="utf-8").read()
ini = d.index("### 4.15 Operaciones")
fin = d.index("\n## 5. Diagrama de Clases de Diseño")
open(D + "3-Diseño.md", "w", encoding="utf-8").write(d[:ini] + texto + d[fin:])
print(f"§4.15: {len(filas)} operaciones | {c_dsd} con diagrama | {c_con} con contrato")
