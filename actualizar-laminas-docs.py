#!/usr/bin/env python3
"""Rehace en los documentos el bloque del diagrama de casos de uso del sistema: la imagen única con los
340 casos de uso y, como complemento, las láminas por actor (`diagramas/uml/CU_Sistema_Completo-Lamina-*.png`).

    python3 actualizar-laminas-docs.py

El bloque va entre dos marcas (`<!-- cu-completo:inicio -->` y `<!-- cu-completo:fin -->`); la primera vez
reemplaza el bloque anterior de láminas. Después corre `numerar-figuras.py --aplicar` para numerar las figuras.
"""
import glob, os, re

D = os.path.dirname(os.path.abspath(__file__)) + "/"
NOMBRES = {"Cliente": "Cliente (ACT-01)", "Chofer": "Chofer (ACT-02)", "Administrador": "Administrador (ACT-03)",
           "Administrador-General": "Administrador General (ACT-05)", "Sistema-Automatico": "Sistema Automático (ACT-04)",
           "MercadoPago": "MercadoPago (ACT-06)", "Firebase": "Firebase (ACT-07)",
           "Servicio-De-Correo": "Servicio de correo (ACT-08)", "Plataforma-De-Despliegue": "Plataforma de despliegue (ACT-09)", "Operador-Tecnico": "Operador Técnico (ACT-10)",
           "Casos-Incluidos": "casos de uso que ningún actor inicia, incluidos por otros"}
INI, FIN = "<!-- cu-completo:inicio -->", "<!-- cu-completo:fin -->"


def laminas():
    arch = sorted(os.path.basename(p)[:-4] for p in glob.glob(D + "diagramas/uml/CU_Sistema_Completo-Lamina-*.png"))
    partes = {}
    for a in arch:
        m = re.match(r'CU_Sistema_Completo-Lamina-(\d+)_(.+?)(?:_Parte-(\d+))?$', a)
        partes[m.group(2)] = partes.get(m.group(2), 0) + 1
    items = [("CU_Sistema_Actores", "Actores del sistema y generalización de ACT-05 en ACT-03")]
    for a in arch:
        m = re.match(r'CU_Sistema_Completo-Lamina-(\d+)_(.+?)(?:_Parte-(\d+))?$', a)
        n = NOMBRES[m.group(2)]
        items.append((a, n[0].upper() + n[1:] + (f", parte {m.group(3)} de {partes[m.group(2)]}" if m.group(3) else "")))
    return items


def bloque(numerada):
    items = laminas()
    n = len(items)
    fig = "**Figura 1 —" if numerada else "**Figura —"
    out = [INI,
           "> **Diagrama de casos de uso del sistema.** Una sola imagen con los casos de uso del sistema, cada uno una vez: a la "
           "izquierda, los actores, cada uno a la altura del centro de su grupo; dentro del límite del sistema, la columna de casos "
           "de uso, agrupados por su actor principal y, dentro de cada grupo, por subsistema. Las relaciones `«include»` y `«extend»` "
           "dentro de un grupo son arcos; hacia otro grupo, un trazo corto con el código del caso al que remiten. Los casos con "
           "varios actores figuran en el grupo del principal, con un trazo corto por cada otro actor. Los casos planificados van en rosado. "
           "La imagen está también en `entregables/diagramas-cu/` en PNG, SVG y PDF.",
           "",
           f"{fig} Diagrama de casos de uso del sistema (todos los casos de uso)**", "",
           "![Diagrama de casos de uso del sistema (todos los casos de uso)](diagramas/uml/CU_Sistema_Diagrama-Completo.png)", "",
           f"> **Láminas complementarias.** El mismo diagrama, en {n} láminas más cortas: la de los actores con la generalización del "
           "Administrador General en el Administrador y una lámina por actor (el Administrador y el Cliente se parten por subsistema) con "
           "todos sus casos de uso a la derecha. Un caso de otro actor que se incluye o se extiende aparece en una segunda columna, con borde "
           "discontinuo, como referencia.", ""]
    for i, (l, nom) in enumerate(items, 1):
        out += [f"{fig} Diagrama de casos de uso, lámina {i} de {n}: {nom}**", "",
                f"![Diagrama de casos de uso, lámina {i} de {n}: {nom}](diagramas/uml/{l}.png)", ""]
    out.append(FIN)
    return "\n".join(out)


for f, num in (("0-Plan_Del_Proyecto.md", True), ("1-Requisitos.md", True), ("Casos-de-Uso.md", False)):
    t = open(D + f, encoding="utf-8").read()
    if INI in t:
        a, b = t.index(INI), t.index(FIN) + len(FIN)
    else:
        m = re.search(r'> El diagrama completo se presenta en \d+ láminas.*?Completo-Lamina-[^)]*\.png\)', t, re.S)
        if not m:
            raise SystemExit(f"{f}: no encuentro el bloque de láminas")
        a, b = m.start(), m.end()
    open(D + f, "w", encoding="utf-8").write(t[:a] + bloque(num) + t[b:])
    print("ok", f)
