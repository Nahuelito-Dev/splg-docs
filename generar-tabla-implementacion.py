#!/usr/bin/env python3
"""Arma la «Tabla de implementación por caso de uso» del Documento 3 (§4.25) desde la de Casos-de-Uso.md (§8).

    python3 generar-tabla-implementacion.py

La tabla de Casos-de-Uso.md §8 es la fuente: lo técnico de cada caso de uso (operación del sistema, ruta de la API,
respuestas con sus códigos y notas) que los casos de uso esenciales no mencionan. El Documento 3 §4.25 es su copia, con
los mismos renglones; no se edita a mano. Se corre después de generar-operaciones.py.
"""
import os, re

D = os.path.dirname(os.path.abspath(__file__)) + "/"
TITULO = "### 4.25 Tabla de implementación por caso de uso"
INTRO = ("Los casos de uso esenciales (Documento 1 §7) describen qué hace el actor y qué responde el sistema, sin nombrar "
         "tecnología. Lo técnico de cada caso —la operación del sistema que lo resuelve, la ruta de la API, las respuestas con "
         "sus códigos y las notas de implementación— está en esta tabla, un renglón por caso de uso, agrupado por subsistema. "
         "Los casos planificados todavía no tienen ruta. Es la misma tabla que la sección 8 de Casos-de-Uso.md.")

cas = open(D + "Casos-de-Uso.md", encoding="utf-8").read()
ini = cas.index("## 8. Tabla de implementación por caso de uso")
fin = cas.find("\n## ", ini + 5)
fuente = cas[ini: fin if fin != -1 else len(cas)]
cuerpo = fuente[fuente.index("\n### SS-"):].strip("\n")
cuerpo = re.sub(r"^### ", "#### ", cuerpo, flags=re.M)
texto = TITULO + "\n\n" + INTRO + "\n\n" + cuerpo + "\n"

d = open(D + "3-Diseño.md", encoding="utf-8").read()
if TITULO in d:
    a = d.index(TITULO)
else:
    a = d.index("\n<!-- dc:inicio -->") + 1
fin_d = min(x for x in (d.find("\n### ", a + 5), d.find("\n## ", a + 5), d.find("\n<!-- ", a + 5)) if x != -1)
if TITULO not in d:
    nuevo = d[:a] + texto + "\n" + d[a:]
else:
    nuevo = d[:a] + texto + d[fin_d:]
open(D + "3-Diseño.md", "w", encoding="utf-8").write(nuevo)
filas = len(re.findall(r"^\| CU-\d{3}", texto, re.M))
print(f"§4.25: {filas} renglones de la tabla de implementación")
