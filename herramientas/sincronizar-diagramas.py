#!/usr/bin/env python3
"""Copia el contenido de cada `diagramas/DSS_*.mmd` y `diagramas/DSD_*.mmd` al bloque ```mermaid del mismo título en los
documentos (Documento 2, Documento 3 y Casos-de-Uso.md): los `.mmd` son la fuente y los bloques son copias.

    python3 herramientas/sincronizar-diagramas.py            informa qué bloques difieren
    python3 herramientas/sincronizar-diagramas.py --aplicar  los reescribe
"""
import glob, os, re, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
DOCS = ["2-Analisis.md", "3-Diseño.md", "Casos-de-Uso.md"]
TIT = re.compile(r'^\s*title (.+)$', re.M)

fuentes = {}
for f in glob.glob(D + "diagramas/DS[SD]_*.mmd"):
    t = open(f, encoding="utf-8").read()
    m = TIT.search(t)
    if m:
        fuentes[m.group(1).strip()] = t.strip("\n")

total = distintos = 0
for doc in DOCS:
    txt = open(DOC + doc, encoding="utf-8").read()
    def cambiar(m):
        global total, distintos
        cuerpo = m.group(1)
        t = TIT.search(cuerpo)
        if not t or t.group(1).strip() not in fuentes:
            return m.group(0)
        total += 1
        nuevo = fuentes[t.group(1).strip()]
        if cuerpo.strip("\n") != nuevo:
            distintos += 1
            return "```mermaid\n" + nuevo + "\n```"
        return m.group(0)
    nuevo_txt = re.sub(r'```mermaid\n(.*?)\n```', cambiar, txt, flags=re.S)
    if nuevo_txt != txt and "--aplicar" in sys.argv:
        open(DOC + doc, "w", encoding="utf-8").write(nuevo_txt)
print(f"{total} bloques con fuente, {distintos} distintos" + (" (reescritos)" if "--aplicar" in sys.argv else ""))
