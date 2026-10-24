#!/usr/bin/env python3
"""Rehace el catálogo de operaciones del Documento 2 (§2.2) y la sección de Operaciones del
documento de Diseño (§4.24).

    python3 herramientas/generar-operaciones.py

La plantilla de la cátedra pide, junto al diagrama de interacción, la lista de
operaciones del sistema con su firma. La fuente es el catálogo canónico de
`catedra/material-de-trabajo/operaciones-sistema.json`, el mismo que el Documento 2 §2.2
publica y que `verificar-conformidad.py` cruza contra los diagramas de secuencia y
los contratos: no se escribe a mano.
"""
import re, glob, os, json

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"

cat = json.load(open(D + "catedra/material-de-trabajo/operaciones-sistema.json", encoding="utf-8"))
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

s = ["### 4.24 Operaciones del sistema", "",
 "Cada operación del sistema con su firma. Una operación del sistema es un mensaje que",
 "un actor le manda al sistema y que aparece como tal en el diagrama de secuencia del",
 "Documento 2. El catálogo, con una sola firma por operación, y el contrato de las que",
 "modifican el modelo conceptual, con precondiciones y postcondiciones, están en el",
 "Documento 2 · §2.2; el diagrama de interacción que muestra cómo se resuelve por dentro",
 "está en las secciones 4.1 a 4.23 de este documento.", "",
 f"Son **{len(filas)} operaciones**. **{c_dsd}** tienen su diagrama de interacción y",
 f"**{c_con}** tienen contrato: son las que cambian el estado del sistema.", "",
 "| Operación | Caso de uso | Actor que la invoca | Diagrama de interacción | Contrato |",
 "|---|---|---|---|---|"]
s += [f"| `{o['firmaConTipos']}` | {' / '.join(o['casosDeUso'])} | {quien(o)} | {d} | "
      f"{'sí' if o['cambiaEstado'] else '—'} |" for o, d in filas]
s.append("")
texto = "\n".join(s)

d = open(DOC + "3-Diseño.md", encoding="utf-8").read()
ini = d.index("### 4.24 Operaciones del sistema")
# también corta en un marcador: después de esta sección viene el del §5 (<!-- dc:inicio -->)
fin = min(x for x in (d.find("\n### ", ini + 5), d.find("\n## ", ini + 5), d.find("\n<!-- ", ini + 5)) if x != -1)
open(DOC + "3-Diseño.md", "w", encoding="utf-8").write(d[:ini] + texto + d[fin:])
print(f"§4.24: {len(filas)} operaciones | {c_dsd} con diagrama | {c_con} con contrato")

# Documento 2 §2.2: el catálogo, con el recuento de operaciones y de contratos
c_con2 = sum(1 for o in ops if o["cambiaEstado"])
a2 = open(DOC + "2-Analisis.md", encoding="utf-8").read()
ini2 = a2.index("#### Catálogo de operaciones del sistema")
frase = re.compile(r"Son \*\*\d+ operaciones\*\*\. \*\*\d+\*\* modifican el modelo conceptual y tienen contrato; las \*\*\d+\*\* restantes")
m = frase.search(a2, ini2)
tabla_ini = a2.index("| Operación | Casos de uso | Actor iniciador | Cambia estado |", ini2)
tabla_fin = a2.index("\n\n", tabla_ini)
filas2 = ["| Operación | Casos de uso | Actor iniciador | Cambia estado |", "|---|---|---|---|"]
filas2 += [f"| `{o['firmaConTipos']}` | {', '.join(o['casosDeUso'])} | {quien(o)} | "
           f"{'Sí' if o['cambiaEstado'] else 'No'} |" for o, _ in filas]
nueva = (f"Son **{len(ops)} operaciones**. **{c_con2}** modifican el modelo conceptual y tienen contrato; "
         f"las **{len(ops) - c_con2}** restantes")
a2 = a2[:m.start()] + nueva + a2[m.end():tabla_ini] + "\n".join(filas2) + a2[tabla_fin:]
open(DOC + "2-Analisis.md", "w", encoding="utf-8").write(a2)
print(f"Doc 2 §2.2: {len(ops)} operaciones | {c_con2} con contrato")
