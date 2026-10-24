#!/usr/bin/env python3
"""Escribe en `diagramas/` el `.mmd` de los bloques Mermaid de los documentos que no son un DSS ni un DSD: el
modelo entidad-relación por contexto (`ER_<nn>_<contexto>.mmd`) y los diagramas de módulo (`MOD_<Mn>_<nombre>.mmd`).

    python3 herramientas/extraer-mmd-modelos.py            informa
    python3 herramientas/extraer-mmd-modelos.py --aplicar  escribe los .mmd

El nombre sale del pie «Figura N — …» que lleva cada bloque. Después se dibujan con `renderizar-dsd.py` y
`incrustar-imagenes-cu.py --aplicar` los muestra como imagen. Idempotente.
"""
import os, re, sys, unicodedata
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
sys.path.insert(0, D + "herramientas")
import imagenes_cu as ic


def slug(t):
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'-+', '-', re.sub(r'[^A-Za-z0-9]+', '-', t)).strip("-")


def bloques():
    t = ic.desplegar(ic._leer("3-Diseño.md"))
    conocidos = ic.fuentes()
    n_er = 0
    for m in re.finditer(r'```mermaid\n(.*?)\n```\n\n(' + ic._PIE + ')', t, re.S):
        cuerpo, pie = m.group(1), re.sub(r'^\*\*Figura \d+ — |\*\*$', '', m.group(2))
        ti = ic._TITULO.search(cuerpo)
        if ti and ti.group(1).strip() in conocidos:
            continue
        if cuerpo.startswith("erDiagram"):
            n_er += 1
            yield f"ER_{n_er:02d}_{slug(pie)}", cuerpo
        else:
            mm = re.match(r'Módulo (M\d) — (.+?) — Diagrama de secuencia$', pie)
            if mm:
                yield f"MOD_{mm.group(1)}_{slug(mm.group(2))}", cuerpo


if __name__ == "__main__":
    n = 0
    for nombre, cuerpo in bloques():
        n += 1
        ruta = D + f"diagramas/{nombre}.mmd"
        if "--aplicar" in sys.argv:
            open(ruta, "w", encoding="utf-8").write(cuerpo + "\n")
        print("  " + nombre)
    print(f"{n} diagramas" + ("" if "--aplicar" in sys.argv else " (nada se escribió; --aplicar)"))
