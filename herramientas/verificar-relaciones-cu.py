#!/usr/bin/env python3
"""Chequeo de coherencia de las relaciones «include»/«extend» entre casos de uso.

Compara cuatro fuentes y no da OK si alguna está vacía:

  1. La fuente única, `relaciones_cu.py` (INCLUYE, INCLUYE_EXTERNO, EXTIENDE).
  2. Los diagramas por subsistema (`diagramas/uml/CU_SS-*.svg`): cada trazo lleva `data-tipo`,
     `data-desde` y `data-hasta`.
  3. La tabla de relaciones del Documento 1 §7.7, con el identificador PE-n de cada «extend».
  4. El texto de los casos de uso expandidos (Casos-de-Uso.md): el CUE del caso base dice «Incluye CU-xxx»
     y lleva en «Puntos de extensión» el PE-n de cada extensión; el de la extensión nombra al caso base y su PE-n.

y compara que el bloque de cada CUE sea idéntico entre Casos-de-Uso.md y su copia en 1-Requisitos.md.

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

# ---------- 3. tabla del Documento 1 §7.7 ----------
req = leer("1-Requisitos.md")
seccion = re.search(r'### 7\.7 Relaciones entre Casos de Uso.*?(?=\n\n---\n\n### 7\.8)', req, re.S)
tabla_include, tabla_extend, tabla_pe = set(), set(), {}
if seccion:
    bloque = seccion.group(0)
    corte = bloque.index("«extend»` (comportamiento")
    for m in re.finditer(r'\|\s*(CU-\d+)[^|]*\|\s*→\s*\|\s*(CU-\d+)', bloque[:corte]):
        tabla_include.add((m.group(1), m.group(2)))
    for m in re.finditer(r'\|\s*(PE-\d+)\s*\|\s*(CU-\d+)[^|]*\|\s*→\s*\|\s*(CU-\d+)', bloque[corte:]):
        tabla_extend.add((m.group(2), m.group(3)))
        tabla_pe[(m.group(2), m.group(3))] = m.group(1)

# ---------- 4. texto de los CUE ----------
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
                     ("diagramas contra relaciones_cu.py (extend)", dib_extend, fuente_extend),
                     ("tabla §7.7 contra relaciones_cu.py (include)", tabla_include, fuente_include),
                     ("tabla §7.7 contra relaciones_cu.py (extend)", tabla_extend, fuente_extend)):
    if a != b:
        errores.append(f"{nombre}: solo en la primera {sorted(a - b)}; solo en la segunda {sorted(b - a)}")
for par, pe in tabla_pe.items():
    if pe != R.pe_id(*par):
        errores.append(f"la tabla §7.7 numera {par} como {pe} y relaciones_cu.py como {R.pe_id(*par)}")

# ---------- copias idénticas entre documentos ----------
diffs = []
todos = sorted(set(re.findall(r'^#### [^\n]*?(CU-\d{3}) —', cu_texto, re.M)))
for cu in todos:
    a, b = bloque_de(cu_texto, cu), bloque_de(req, cu)
    if a != b:
        diffs.append(cu)
if diffs:
    errores.append(f"el CUE de {len(diffs)} caso(s) difiere entre Casos-de-Uso.md y 1-Requisitos.md: {diffs[:8]}")

# ---------- no se da OK sobre nada vacío ----------
for nombre, n in (("include en la fuente", len(fuente_include)), ("extend en la fuente", len(fuente_extend)),
                  ("include dibujados", len(dib_include)), ("extend dibujados", len(dib_extend)),
                  ("include en la tabla", len(tabla_include)), ("extend en la tabla", len(tabla_extend)),
                  ("CUE comparados", len(todos))):
    if n == 0:
        errores.append(f"0 {nombre}: el chequeo no puede dar OK sobre una lectura vacía")

print(f"«include»: {len(fuente_include)} en la fuente, {len(dib_include)} dibujados, {len(tabla_include)} en la tabla §7.7")
print(f"«extend»: {len(fuente_extend)} en la fuente, {len(dib_extend)} dibujados, {len(tabla_extend)} en la tabla §7.7")
print(f"CUE comparados entre Casos-de-Uso.md y 1-Requisitos.md: {len(todos)}")
if errores:
    print(f"\n{len(errores)} diferencia(s):")
    for e in errores:
        print("  -", e)
    sys.exit(1)
print("\n0 diferencias.")
sys.exit(0)
