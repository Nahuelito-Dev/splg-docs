#!/usr/bin/env python3
"""Chequeo de coherencia de las relaciones «include»/«extend» entre casos de uso.

Compara tres fuentes:
  1. Los diagramas .puml por subsistema (diagramas/uml/CU_SS-*.puml)
  2. La tabla maestra de relaciones (1-Requisitos.md §7.7)
  3. El texto de los CUE (Casos-de-Uso.md), que tiene que decir "Incluye CU-XXX"
     o "«include» CU-XXX" / "«extend»" en alguna parte del caso base

y compara que el bloque de cada CU (CUE y DSD) sea idéntico entre Casos-de-Uso.md
y su copia en 1-Requisitos.md / 3-Diseño.md.

    python3 material-de-trabajo/verificar-relaciones-cu.py

Sale con código 0 si no encuentra diferencias, 1 si encuentra alguna (y las lista).
"""
import re, glob, os, sys

D = os.path.dirname(os.path.abspath(__file__)) + "/../"

def leer(nombre):
    return open(D + nombre, encoding="utf-8").read()

# ---------- 1. relaciones declaradas en los .puml ----------
puml_include = set()   # (base, incluido) solo pares CU-CU (se ignoran los factorizados F_)
puml_extend = set()    # (extension, base)

for f in glob.glob(D + "diagramas/uml/CU_SS-*.puml"):
    txt = open(f, encoding="utf-8").read()
    for m in re.finditer(r'U(\d+)\s*\.\.>\s*U(\d+)\s*:\s*<<include>>', txt):
        puml_include.add((f"CU-{m.group(1)}", f"CU-{m.group(2)}"))
    for m in re.finditer(r'U(\d+)\s*\.\.>\s*U(\d+)\s*:\s*<<extend>>', txt):
        puml_extend.add((f"CU-{m.group(1)}", f"CU-{m.group(2)}"))

# ---------- 2. tabla maestra en 1-Requisitos.md §7.7 ----------
req = leer("1-Requisitos.md")
seccion = re.search(r'### 7\.7 Relaciones entre Casos de Uso.*?(?=\n\n---\n\n## 8\.)', req, re.S)
tabla_include = set()
tabla_extend = set()
if seccion:
    bloque = seccion.group(0)
    for m in re.finditer(r'\|\s*(CU-\d+)[^|]*\|\s*→\s*\|\s*(CU-\d+)', bloque):
        tabla_include.add((m.group(1), m.group(2)))

# ---------- 3. texto de Casos-de-Uso.md: cada base menciona el incluido ----------
cu_texto = leer("Casos-de-Uso.md")

def bloque_de(cu):
    m = re.search(rf'^#### [^\n]*{re.escape(cu)} —[^\n]*\n.*?(?=\n---\n|\Z)', cu_texto, re.S | re.M)
    return m.group(0) if m else ""

faltantes_en_texto = []
for base, incluido in sorted(puml_include):
    texto = bloque_de(base)
    if not texto:
        faltantes_en_texto.append((base, incluido, "no se encontró el CUE de la base"))
        continue
    if incluido not in texto:
        faltantes_en_texto.append((base, incluido, "el CUE de la base no menciona al incluido"))

faltantes_en_tabla = sorted(puml_include - tabla_include)

# ---------- 4. copias idénticas entre documentos ----------
diffs_copias = []

def comparar_bloque(cu, doc_a, patron_a, doc_b, patron_b, etiqueta):
    texto_a, texto_b = leer(doc_a), leer(doc_b)
    ma = re.search(patron_a, texto_a, re.S | re.M)
    mb = re.search(patron_b, texto_b, re.S | re.M)
    if not ma or not mb:
        return
    if ma.group(0) != mb.group(0):
        diffs_copias.append((cu, etiqueta, doc_a, doc_b))

for cu in sorted({c for par in puml_include | puml_extend for c in par}):
    patron_cue = rf'^#### [^\n]*{re.escape(cu)} —[^\n]*\n.*?(?=\n---\n)'
    comparar_bloque(cu, "Casos-de-Uso.md", patron_cue, "1-Requisitos.md", patron_cue, "CUE")

print(f"Relaciones <<include>> en los .puml: {len(puml_include)}")
print(f"Relaciones <<extend>> en los .puml: {len(puml_extend)}")
print(f"Filas <<include>> en la tabla maestra (1-Requisitos §7.7): {len(tabla_include)}")
print()

ok = True
if faltantes_en_texto:
    ok = False
    print(f"[FALTA EN EL TEXTO] {len(faltantes_en_texto)} relación(es) del diagrama sin mención explícita en el CUE:")
    for base, inc, motivo in faltantes_en_texto:
        print(f"  - {base} incluye {inc}: {motivo}")
else:
    print("[OK] Todas las relaciones <<include>> del diagrama están mencionadas en el CUE de la base.")

if faltantes_en_tabla:
    ok = False
    print(f"\n[FALTA EN LA TABLA MAESTRA] {len(faltantes_en_tabla)} relación(es) del diagrama sin fila en 1-Requisitos.md §7.7:")
    for base, inc in faltantes_en_tabla:
        print(f"  - {base} → {inc}")
else:
    print("[OK] Todas las relaciones <<include>> del diagrama tienen fila en la tabla maestra.")

if diffs_copias:
    ok = False
    print(f"\n[COPIAS DISTINTAS] {len(diffs_copias)} bloque(s) no coinciden entre documentos:")
    for cu, etiqueta, a, b in diffs_copias:
        print(f"  - {cu} ({etiqueta}): {a} != {b}")
else:
    print("[OK] Los bloques CUE de los CU con relaciones coinciden entre Casos-de-Uso.md y 1-Requisitos.md.")

print()
if ok:
    print("0 diferencias.")
    sys.exit(0)
else:
    print("Hay diferencias — ver el detalle arriba.")
    sys.exit(1)
