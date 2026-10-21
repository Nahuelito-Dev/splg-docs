#!/usr/bin/env python3
"""Muestra cada DSS y DSD de los documentos como imagen, con su código Mermaid plegado debajo.

    python3 incrustar-imagenes-cu.py            cuenta lo que haría
    python3 incrustar-imagenes-cu.py --aplicar  escribe Casos-de-Uso.md, 2-Analisis.md y 3-Diseño.md
    python3 incrustar-imagenes-cu.py --quitar   vuelve al bloque Mermaid suelto (como lo leen los generadores)

Cada bloque ```mermaid cuyo `title` es el de un `diagramas/DS[SD]_*.mmd` queda así:

    ![pie](diagramas/png/<archivo>.png)

    **Figura N — pie**                  (si el documento ya lo traía)

    <details><summary>Ver código del diagrama</summary> … bloque mermaid … </details>

GitHub dibuja el Mermaid; cualquier otro visor (VS Code sin extensión, el explorador, un .md suelto) muestra la
imagen. Los `.mmd` siguen siendo la fuente (`material-de-trabajo/sincronizar-diagramas.py` copia su contenido a los
bloques). Idempotente. El sitio, el Word y los HTML para Drive leen los documentos ya sin la imagen
(`imagenes_cu.desplegar`), así que cada diagrama sale una sola vez. Los modelos de datos y las capturas de
pantalla no se tocan.
"""
import re, sys
import imagenes_cu as ic

aplicar, quitar = "--aplicar" in sys.argv, "--quitar" in sys.argv
for doc in ic.DOCS_CU:
    antes = ic._leer(doc)
    despues = ic.desplegar(antes) if quitar else ic.plegar(antes)
    n = len(ic._PLEGADO.findall(despues))
    print(f"  {doc}: {n} diagramas con imagen" + ("" if despues != antes else " (sin cambios)"))
    if aplicar and despues != antes:
        open(ic.D + doc, "w", encoding="utf-8").write(despues)
print("aplicado" if aplicar else "\nnada se escribió todavía (--aplicar)")
