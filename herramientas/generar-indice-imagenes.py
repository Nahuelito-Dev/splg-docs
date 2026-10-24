#!/usr/bin/env python3
"""Rehace INDICE-IMAGENES.md (la sección «Diagramas UML» y «Por caso de uso») desde los archivos reales.

    python3 herramientas/generar-indice-imagenes.py

Cada DSS y cada DSD de `diagramas/png/` aparece en el caso de uso que nombra su archivo; los diagramas de
casos de uso, de `diagramas/uml/CU_*.png`. Nada se escribe a mano: un nombre que ya no existe no puede quedar.
`verificar-conformidad.py` controla el índice contra los archivos con `verificar_indice()`.
"""
import glob, os, re

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"


def nombres_de_casos():
    t = open(DOC + "Casos-de-Uso.md", encoding="utf-8").read()
    return {m.group(1): m.group(2).strip()
            for m in re.finditer(r'^\| (CU-\d{3}) ([^|]+?) \| SS-\d\d \|', t, re.M)}


def construir():
    idx = open(DOC + "INDICE-IMAGENES.md", encoding="utf-8").read()
    a = idx.index("## Diagramas en notación UML")
    b = idx.index("## Módulos de gestión planificados")
    cabecera, cola = idx[:a], idx[b:]
    uml = sorted(os.path.basename(p) for p in glob.glob(D + "diagramas/uml/CU_*.png"))
    out = ["## Diagramas en notación UML", "", "| Archivo |", "|---|"] + [f"| `{n}` |" for n in uml] + [""]
    out += ["## Por caso de uso", "", "| CU | Caso de uso | DSS | DSD |", "|---|---|---|---|"]
    dss = sorted(os.path.basename(p) for p in glob.glob(D + "diagramas/png/DSS_*.png"))
    dsd = sorted(os.path.basename(p) for p in glob.glob(D + "diagramas/png/DSD_*.png"))
    for cu, nombre in sorted(nombres_de_casos().items()):
        s = [f"`{n}`" for n in dss if f"_{cu}_" in n]
        d = [f"`{n}`" for n in dsd if re.search(r'(?<![\d-])%s(?![\d])' % cu, n.split(".png")[0])]
        out.append(f"| {cu} | {nombre} | {' · '.join(s) or '—'} | {' · '.join(d) or '—'} |")
    out.append("")
    return cabecera + "\n".join(out) + "\n" + cola


def verificar_indice():
    """Errores del índice contra los archivos: nombres que no existen y diagramas sin entrada."""
    t = open(DOC + "INDICE-IMAGENES.md", encoding="utf-8").read()
    errores = []
    citados = set(re.findall(r'`((?:DSS|DSD|CU)_[^`]+\.png)`', t))
    for n in sorted(citados):
        carpeta = "diagramas/uml/" if n.startswith("CU_") else "diagramas/png/"
        if not os.path.exists(D + carpeta + n):
            errores.append(f"el índice cita {n} y no existe")
    for p in glob.glob(D + "diagramas/png/D*_*.png"):
        if os.path.basename(p) not in citados:
            errores.append(f"{os.path.basename(p)} no está en el índice")
    for p in glob.glob(D + "diagramas/uml/CU_*.png"):
        if os.path.basename(p) not in citados:
            errores.append(f"{os.path.basename(p)} no está en el índice")
    return errores


if __name__ == "__main__":
    texto = construir()
    open(DOC + "INDICE-IMAGENES.md", "w", encoding="utf-8").write(texto)
    e = verificar_indice()
    print(f"índice rehecho; {len(e)} diferencias")
    for x in e[:10]: print("  ✗", x)
