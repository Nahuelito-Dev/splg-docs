#!/usr/bin/env python3
"""Arma `catedra/entregables/diagramas-cu/`: los diagramas de casos de uso como imágenes sueltas, para mandarlas
sin el documento. Cada PNG se lee solo (título, nombre del sistema en el límite y leyenda de la notación).

    python3 herramientas/generar-entregables.py

00 es el diagrama único con todos los casos de uso (PNG, SVG y PDF vectoriales); después, la lámina de
actores, una lámina por actor y un diagrama por subsistema. Todo sale de `diagramas/uml/`.
"""
import glob, os, re, shutil, subprocess

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
UML = D + "diagramas/uml/"
OUT = D + "catedra/entregables/diagramas-cu/"
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(OUT + "*"):
    os.remove(f)

ACTORES = {"Cliente": "Cliente", "Chofer": "Chofer", "Administrador": "Administrador",
           "Administrador-General": "Administrador-General", "Sistema-Automatico": "Sistema-Automatico",
           "MercadoPago": "MercadoPago", "Firebase": "Firebase", "Servicio-De-Correo": "Servicio-de-correo",
           "Plataforma-De-Despliegue": "Plataforma-de-despliegue", "Operador-Tecnico": "Operador-tecnico", "Casos-Incluidos": "Casos-incluidos"}
MINUS = {"-Y-": "-y-", "-De-": "-de-", "-En-": "-en-", "-Del-": "-del-", "-Al-": "-al-"}
indice = []


def pdf(svg, destino, alto_pagina=2800):
    """PDF vectorial de varias páginas: el diagrama completo mide más de 20.000 puntos de alto y los visores no
    abren una página así. Se corta entre un recuadro de subsistema y el siguiente, sin partir ningún caso."""
    import tempfile
    txt = open(svg, encoding="utf-8").read()
    w, h = (float(x) for x in re.search(r'width="([\d.]+)" height="([\d.]+)"', txt).groups())
    ivs = sorted((float(m.group(1)) - float(m.group(2)), float(m.group(1)) + float(m.group(2))) for m in
                 re.finditer(r'<ellipse cx="[\d.]+" cy="([\d.]+)" rx="[\d.]+" ry="([\d.]+)"', txt))
    finales = []                       # puntos de corte: huecos entre óvalos (nunca a través de un caso de uso)
    for (a0, a1), (b0, b1) in zip(ivs, ivs[1:]):
        if b0 > a1 + 2: finales.append((a1 + b0) / 2 - 6)
    cortes, y0 = [0.0], 0.0
    while h - y0 > alto_pagina:
        c = [f for f in finales if y0 + alto_pagina * 0.6 < f <= y0 + alto_pagina]
        y0 = max(c) + 6 if c else y0 + alto_pagina
        cortes.append(y0)
    cortes.append(h)
    paginas = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (a, b) in enumerate(zip(cortes, cortes[1:])):
            s = re.sub(r'width="[\d.]+" height="[\d.]+" viewBox="[^"]+"',
                       f'width="{w}" height="{b - a}" viewBox="0 {a} {w} {b - a}"', txt, count=1)
            s = s.replace('<rect width="100%" height="100%" fill="#FFFFFF"/>',
                          f'<rect x="0" y="0" width="{w}" height="{h}" fill="#FFFFFF"/>', 1)
            p = f"{tmp}/p{i:03d}.pdf"
            open(f"{tmp}/p{i:03d}.svg", "w", encoding="utf-8").write(s)
            subprocess.run(["rsvg-convert", "-f", "pdf", "-o", p, f"{tmp}/p{i:03d}.svg"], check=True)
            paginas.append(p)
        subprocess.run(["pdfunite"] + paginas + [destino], check=True)


def copiar(origen, nombre, descripcion, vectorial=False):
    shutil.copy(UML + origen + ".png", OUT + nombre + ".png")
    if vectorial:
        shutil.copy(UML + origen + ".svg", OUT + nombre + ".svg")
        pdf(UML + origen + ".svg", OUT + nombre + ".pdf")
    indice.append((nombre, descripcion, vectorial))


n = 0
copiar("CU_Sistema_Diagrama-Completo", "00-Diagrama-de-Casos-de-Uso-Completo",
       "Diagrama de casos de uso del sistema: los 338 casos de uso en una sola imagen, en tres columnas (también SVG y PDF vectoriales)", True)
n += 1
copiar("CU_Sistema_Diagrama-De-Subsistemas", f"{n:02d}-Diagrama-por-subsistemas", "Diagrama de casos de uso del sistema por subsistemas: los paquetes con los actores y el límite del sistema")
n += 1
copiar("CU_Sistema_Actores", f"{n:02d}-Actores", "Los actores del sistema y la generalización del Administrador General en el Administrador")
for p in sorted(glob.glob(UML + "CU_Sistema_Completo-Lamina-*.png")):
    o = os.path.basename(p)[:-4]
    m = re.match(r'CU_Sistema_Completo-Lamina-\d+_(.+?)(?:_Parte-(\d+))?$', o)
    n += 1
    nombre = f"{n:02d}-{ACTORES[m.group(1)]}" + (f"-parte-{m.group(2)}" if m.group(2) else "")
    copiar(o, nombre, "Casos de uso de " + ACTORES[m.group(1)].replace("-", " ") + (f", parte {m.group(2)}" if m.group(2) else ""))
for o in ("CU_Sistema_Diagrama-De-Contexto", "CU_Sistema_Mapa"):
    n += 1
    copiar(o, f"{n:02d}-" + ("Diagrama-de-contexto" if "Contexto" in o else "Mapa-de-navegacion"),
           "Diagrama de contexto del sistema" if "Contexto" in o else "Mapa de navegación: qué actores participan en cada subsistema")
for p in sorted(glob.glob(UML + "CU_SS-*.png")):
    o = os.path.basename(p)[:-4]
    m = re.match(r'CU_(SS-\d+)_(.+?)(?:_Parte-(\d+))?$', o)
    tit = m.group(2).replace("Dashboard", "Tablero")
    for a, b in MINUS.items():
        tit = tit.replace(a, b)
    n += 1
    nombre = f"{n:02d}-{m.group(1)}-{tit}" + (f"-parte-{m.group(3)}" if m.group(3) else "")
    copiar(o, nombre, f"Subsistema {m.group(1)}: {tit.replace('-', ' ')}" + (f", parte {m.group(3)}" if m.group(3) else ""))

txt = ["DIAGRAMAS DE CASOS DE USO — SPLG (Sistema de Pedidos y Logística de Garrafas de Gas)", "",
       "Cada imagen se lee sola: lleva su título, el nombre del sistema en el límite y la leyenda de la notación.",
       "Los PNG están exportados al doble de tamaño (el diagrama 00, a la escala máxima que admite un PNG: 32.000 px de alto);",
       "para ampliar o imprimir en A4 sin perder nitidez, usar el SVG o el PDF de la imagen 00.", "",
       "Notación: UML 2.5. Rosado = caso de uso planificado. Cada «include» y cada «extend» tiene su propio trazo discontinuo, con",
       "el estereotipo junto al trazo; un caso de otro actor o de otro subsistema figura con borde discontinuo, solo como referencia.", "", "ÍNDICE", ""]
for nombre, desc, vec in indice:
    txt.append(f"  {nombre}.png" + (" (+ .svg, .pdf)" if vec else ""))
    txt.append(f"      {desc}")
open(OUT + "LEEME.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")
print(f"{len(indice)} diagramas en {OUT}")
