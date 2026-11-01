#!/usr/bin/env python3
"""Chequeo de coherencia de las relaciones «include»/«extend» entre casos de uso.

Compara tres fuentes y no da OK si alguna está vacía:

  1. La fuente única, `relaciones_cu.py` (INCLUYE, INCLUYE_EXTERNO, EXTIENDE).
  2. Los diagramas por subsistema (`diagramas/uml/CU_SS-*.svg`): cada trazo lleva `data-tipo`,
     `data-desde` y `data-hasta`.
  3. El texto de los casos de uso expandidos (Casos-de-Uso.md): el CUE del caso base dice «Incluye CU-xxx»
     y lleva en «Puntos de extensión» el PE-n de cada extensión; el de la extensión nombra al caso base y su PE-n.

El Documento 1 ya no lleva la tabla de relaciones (la plantilla no la pide: las relaciones se ven en el
diagrama de cada subsistema) y expande sólo los casos esenciales (`cu_esenciales.py`), con los pasos que
incluían un caso sin expandir reescritos dentro del caso. De él se controla que expanda exactamente esos
casos y que ningún paso diga «Incluye» un caso que el documento no expande.

    python3 herramientas/verificar-relaciones-cu.py

Sale con código 0 si no encuentra diferencias, 1 si encuentra alguna (y las lista).
"""
import re, glob, os, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
sys.path.insert(0, D + "herramientas")
import relaciones_cu as R


def leer(nombre):
    return open(DOC + nombre, encoding="utf-8").read()


# ---------- 1. fuente única ----------
fuente_include = set()
for v in R.INCLUYE.values():
    fuente_include |= set(v)
fuente_include |= set(R.INCLUYE_EXTERNO)
fuente_extend = {(e, b) for e, b, _ in R.extensiones()}

# ---------- 2. relaciones dibujadas ----------
dib_include, dib_extend = set(), set()
for f in glob.glob(D + "diagramas/uml/CU_SS-*.svg"):
    txt = open(f, encoding="utf-8").read()
    for m in re.finditer(r'<path class="rel" data-tipo="(include|extend)" data-desde="(CU-\d+)" data-hasta="(CU-\d+)"', txt):
        (dib_include if m.group(1) == "include" else dib_extend).add((m.group(2), m.group(3)))

req = leer("1-Requisitos.md")
from cu_esenciales import ESENCIALES

# ---------- 3. texto de los CUE ----------
cu_texto = leer("Casos-de-Uso.md")


def bloque_de(texto, cu):
    m = re.search(rf'^#### [^\n]*{re.escape(cu)} —[^\n]*\n.*?(?=\n---\n|\Z)', texto, re.S | re.M)
    return m.group(0) if m else ""


errores = []
for base, inc in sorted(fuente_include):
    b = bloque_de(cu_texto, base)
    if not b:
        errores.append(f"{base}: no se encontró su CUE en Casos-de-Uso.md")
    elif inc not in b:
        errores.append(f"{base} incluye {inc}, pero su CUE no lo menciona")
for ext, base in sorted(fuente_extend):
    pe = R.pe_id(ext, base)
    be, bb = bloque_de(cu_texto, ext), bloque_de(cu_texto, base)
    if base not in be or pe not in be:
        errores.append(f"{ext} extiende {base} ({pe}), pero su CUE no nombra al caso base y al {pe}")
    if pe not in bb or ext not in bb:
        errores.append(f"{base} tiene la extensión {ext} ({pe}), pero su CUE no la lista en «Puntos de extensión»")

# ---------- comparaciones ----------
for nombre, a, b in (("diagramas contra relaciones_cu.py (include)", dib_include, fuente_include),
                     ("diagramas contra relaciones_cu.py (extend)", dib_extend, fuente_extend)):
    if a != b:
        errores.append(f"{nombre}: solo en la primera {sorted(a - b)}; solo en la segunda {sorted(b - a)}")

# ---------- Documento 1: sólo los esenciales, y ningún «Incluye» a un caso sin expandir ----------
todos = sorted(set(re.findall(r'^#### [^\n]*?(CU-\d{3}) —', req, re.M)))
if set(todos) != set(ESENCIALES):
    errores.append(f"el Documento 1 expande {sorted(set(todos) - set(ESENCIALES))} de más y le faltan {sorted(set(ESENCIALES) - set(todos))}")
for cu in todos:
    for inc in re.findall(r'^\| \d+ \|[^\n]*?Incluye (CU-\d{3})', bloque_de(req, cu), re.M):
        if inc not in ESENCIALES:
            errores.append(f"Documento 1, {cu}: un paso incluye {inc}, que el documento no expande (reescribir el paso dentro del caso)")

# ---------- no se da OK sobre nada vacío ----------
for nombre, n in (("include en la fuente", len(fuente_include)), ("extend en la fuente", len(fuente_extend)),
                  ("include dibujados", len(dib_include)), ("extend dibujados", len(dib_extend)),
                  ("CUE del Documento 1", len(todos))):
    if n == 0:
        errores.append(f"0 {nombre}: el chequeo no puede dar OK sobre una lectura vacía")

print(f"«include»: {len(fuente_include)} en la fuente, {len(dib_include)} dibujados")
print(f"«extend»: {len(fuente_extend)} en la fuente, {len(dib_extend)} dibujados")
print(f"CUE del Documento 1 (casos esenciales): {len(todos)}")
if errores:
    print(f"\n{len(errores)} diferencia(s):")
    for e in errores:
        print("  -", e)
    sys.exit(1)
print("\n0 diferencias.")
sys.exit(0)
