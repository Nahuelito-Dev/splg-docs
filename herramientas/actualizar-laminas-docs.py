#!/usr/bin/env python3
"""Rehace en los documentos el bloque del diagrama de casos de uso del sistema: la imagen única con los
338 casos de uso y, como complemento, las láminas por actor (`diagramas/uml/CU_Sistema_Completo-Lamina-*.png`).

    python3 herramientas/actualizar-laminas-docs.py

El bloque va entre dos marcas (`<!-- cu-completo:inicio -->` y `<!-- cu-completo:fin -->`); la primera vez
reemplaza el bloque anterior de láminas. Después corre `numerar-figuras.py --aplicar` para numerar las figuras.
"""
import glob, os, re

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
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
           "> **Diagrama completo de casos de uso del sistema (anexo).** Una sola imagen con los casos de uso del sistema, cada uno una vez, "
           "en tres columnas: a la izquierda, los actores, cada uno a la altura del centro de sus casos de uso; en la columna del medio, "
           "dentro del límite del sistema, los casos de uso que esos actores inician; y a la derecha, los casos incluidos que ningún actor "
           "inicia. Cada relación `«include»` y `«extend»` tiene su propio trazo ortogonal, con el estereotipo junto al trazo; la base de una "
           "extensión lleva el compartimiento de puntos de extensión con su identificador PE-n. Los casos planificados van en rosado. "
           "La imagen está también en `catedra/entregables/diagramas-cu/` en PNG, SVG y PDF.",
           "",
           f"{fig} Diagrama de casos de uso del sistema (todos los casos de uso)**", "",
           "![Diagrama de casos de uso del sistema (todos los casos de uso)](../diagramas/uml/CU_Sistema_Diagrama-Completo.png)", "",
           f"> **Láminas complementarias.** El mismo diagrama, en {n} láminas más cortas, con la misma grilla de tres columnas: la de los "
           "actores con la generalización del Administrador General en el Administrador y, por cada actor, sus casos de uso en la columna del "
           "medio (el Administrador y el Cliente se parten en varias partes) y, a la derecha, los casos relacionados con ellos por `«include»` "
           "o `«extend»`; un caso que inicia otro actor o que es de otro subsistema figura con borde discontinuo, solo como referencia. "
           "Los diagramas de cada subsistema (Documento 1 §4.3) usan la misma grilla.", ""]
    for i, (l, nom) in enumerate(items, 1):
        out += [f"{fig} Diagrama de casos de uso, lámina {i} de {n}: {nom}**", "",
                f"![Diagrama de casos de uso, lámina {i} de {n}: {nom}](../diagramas/uml/{l}.png)", ""]
    out.append(FIN)
    return "\n".join(out)


SUBS_TXT = ("Con {n} casos de uso, el diagrama de casos de uso del sistema se presenta en dos niveles, ambos en notación UML. La figura principal es el "
            "**diagrama por subsistemas**: los {s} subsistemas dibujados como paquetes dentro del límite del sistema y los actores fuera de él, cada uno "
            "unido a los subsistemas en los que participa; el Administrador General especializa al Administrador. El detalle —los {n} casos de uso, uno por "
            "uno, con sus relaciones «include» y «extend»— está en el **diagrama completo** y en sus **láminas** (anexo `catedra/entregables/diagramas-cu/`), "
            "que siguen a esta figura. Después, el **mapa de navegación** (que no es un diagrama UML) resume los paquetes y los actores en una página, "
            "como ayuda para ubicarse.")


def figura_subs(numerada):
    fig = "**Figura 1 —" if numerada else "**Figura —"
    return [f"{fig} Diagrama de casos de uso del sistema por subsistemas**", "",
            "![Diagrama de casos de uso del sistema por subsistemas](../diagramas/uml/CU_Sistema_Diagrama-De-Subsistemas.png)", ""]


def reestructurar(t, numerada, f):
    """Deja, en este orden: el diagrama por subsistemas, el completo con sus láminas y, al final, el mapa de navegación."""
    if "CU_Sistema_Diagrama-De-Subsistemas.png" in t:
        return t
    fig = "**Figura 1 —" if numerada else "**Figura —"
    m = re.search(r'\*\*Figura (?:\d+ )?— Mapa de navegación[^\n]*\*\*\n\n!\[[^\n]*\]\([^)]*CU_Sistema_Mapa\.png\)\n\n(?:> [^\n]*\n)*', t)
    mapa = m.group(0).rstrip("\n") if m else ""
    if m: t = t[:m.start()] + t[m.end():]
    n_ss = 21
    intro = SUBS_TXT.format(n=338, s=n_ss)
    if f == "0-Plan_Del_Proyecto.md":
        a = t.index("## 6. Diagrama de Casos de Uso del Sistema") + len("## 6. Diagrama de Casos de Uso del Sistema")
        b = t.index(INI)
        t = t[:a] + "\n\n" + intro + "\n\n" + "\n".join(figura_subs(numerada)) + "\n" + t[b:]
    elif f == "1-Requisitos.md":
        a = t.index("## 3. Diagrama de Casos de Uso del Sistema") + len("## 3. Diagrama de Casos de Uso del Sistema")
        b = t.index("### 3.1 Fronteras del Sistema")
        t = t[:a] + "\n\n" + intro.replace("Después, el **mapa de navegación**", "Después del diagrama completo, el **mapa de navegación**") + \
            " La sección 3.1 delimita el sistema con el **diagrama de contexto**, y el detalle de cada subsistema está en la sección 4.3.\n\n" + "\n".join(figura_subs(numerada)) + "\n" + t[b:]
    else:
        a = t.index("## 2. Diagrama de Casos de Uso del Sistema") + len("## 2. Diagrama de Casos de Uso del Sistema")
        b = t.index("**Figura — Diagrama de contexto")
        t = t[:a] + "\n\n" + intro + "\n\n" + "\n".join(figura_subs(numerada)) + "\n" + t[b:]
    if mapa:
        k = t.index(FIN) + len(FIN)
        t = t[:k] + "\n\n" + mapa + "\n" + t[k:]
    return t


# el Documento 1 lleva sólo el diagrama por subsistemas (la plantilla pide un diagrama del sistema): sin láminas
for f, num in (("0-Plan_Del_Proyecto.md", True), ("Casos-de-Uso.md", False)):
    t = open(DOC + f, encoding="utf-8").read()
    t = reestructurar(t, num, f)
    if INI in t:
        a, b = t.index(INI), t.index(FIN) + len(FIN)
    else:
        m = re.search(r'> El diagrama completo se presenta en \d+ láminas.*?Completo-Lamina-[^)]*\.png\)', t, re.S)
        if not m:
            raise SystemExit(f"{f}: no encuentro el bloque de láminas")
        a, b = m.start(), m.end()
    open(DOC + f, "w", encoding="utf-8").write(t[:a] + bloque(num) + t[b:])
    print("ok", f)
