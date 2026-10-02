#!/usr/bin/env python3
"""Verifica que cada caso de uso del catálogo tenga sus cinco artefactos y un estado uniforme.

    python3 material-de-trabajo/verificar-artefactos-cu.py

Por cada CU de `Casos-de-Uso.md` §3 comprueba:

  1. CU     aparece en el diagrama de casos de uso de su subsistema (`diagramas/uml/CU_SS-xx_*.puml`)
  2. CUA    alto nivel en el Documento 0 §7 y en `Casos-de-Uso.md` §4
  3. CUE    expandido en el Documento 1 §7 y en `Casos-de-Uso.md` §5, con su campo Estado
  4. DSS    diagrama de secuencia del sistema en el Documento 2 y en `Casos-de-Uso.md` §6,
            con su `.mmd`, su PNG y su SVG. Un caso incluido (ningún actor lo inicia) no tiene
            diagrama propio: en los dos documentos lleva la nota que remite a su caso base
  5. DSD    diagrama de interacción de diseño en el Documento 3 y en `Casos-de-Uso.md` §7,
            con su `.mmd`, su PNG y su SVG

y el estado: el campo Estado del CUE es «Implementado», «Implementado, con funcionalidad
planificada…» o «Planificado (I-n)…», con la misma redacción en todos los planificados, y la
columna Estado de los dos catálogos coincide con él. Sale 0 si todo cierra, 1 y el detalle si no.
"""
import re, os, glob, sys

D = os.path.dirname(os.path.abspath(__file__)) + "/../"


def leer(f):
    return open(D + f, encoding="utf-8").read()


def seccion(t, ini, fin):
    a = re.search(ini, t, re.M).start()
    m = re.search(fin, t[a + 1:], re.M) if fin else None
    return t[a: a + 1 + m.start() if m else len(t)]


cas, plan, req, ana, dis = (leer(f) for f in ("Casos-de-Uso.md", "0-Plan_Del_Proyecto.md",
                                              "1-Requisitos.md", "2-Analisis.md", "3-Diseño.md"))

# ---- catálogo (Casos-de-Uso §3 y Documento 0 §8)
FILA = re.compile(r'^\| (CU-\d{3}) ([^|]+?) \| (SS-\d\d) \| ([^|]*?) \| (\w+)\s*\| ([^|]+?) \|$', re.M)
cat_cas = {m.group(1): m for m in FILA.finditer(seccion(cas, r'^## 3\. ', r'^## 4\. '))}
cat_plan = {m.group(1): m for m in FILA.finditer(seccion(plan, r'^## 8\. ', r'^## 9\. |\Z'))}
codigos = sorted(cat_cas)

# ---- secciones de cada documento
CUA_CAS = seccion(cas, r'^## 4\. ', r'^## 5\. ')
CUE_CAS = seccion(cas, r'^## 5\. ', r'^## 6\. ')
DSS_CAS = seccion(cas, r'^## 6\. ', r'^## 7\. ')
DSD_CAS = seccion(cas, r'^## 7\. ', None)
CUA_PLAN = seccion(plan, r'^## 7\. ', r'^## 8\. ')
CUE_REQ = seccion(req, r'^## 7\. ', r'^## 8\. ')
DSS_ANA = seccion(ana, r'^## 2\. ', r'^## 3\. ')
DSD_DIS = seccion(dis, r'^## 3\. ', r'^## 5\. ')

fallas = []


def falta(cu, que):
    fallas.append(f"{cu}: {que}")


def tiene_cua(t, cu):
    return re.search(rf'\*\*Código:\*\*\s*{cu}\s*\|', t) is not None


def tiene_cue(t, cu):
    return re.search(rf'^####\s+[^\n]*?{cu}\s+—', t, re.M) is not None


def es_incluido(cu):
    """Un caso incluido no lo inicia ningún actor: su catálogo dice «caso incluido» o «Ninguno directo»."""
    m = re.search(rf'\*\*Código:\*\*\s*{cu}\s*\|[^\n]*\n\*\*Actor/es:\*\*\s*([^\n]*)', CUA_CAS)
    return bool(m) and ("caso incluido" in m.group(1).lower() or "ninguno directo" in m.group(1).lower())


def tiene_nota_de_incluido(t, cu):
    m = re.search(rf'^#{{3,5}}\s+[^\n]*DSS\s+—\s+{cu}:[^\n]*\n(.*?)(?=^#{{3,5}}\s|^---\s*$|\Z)', t, re.M | re.S)
    return bool(m) and "Caso incluido" in m.group(1) and "```mermaid" not in m.group(1)


def tiene_dia(t, tipo, cu):
    # el título del diagrama o el encabezado nombran el caso, solo o junto con otros (CU-015 / CU-016)
    pat = rf'^#{{3,5}}\s+[^\n]*{tipo}\s+—\s+[^\n]*{cu}\b'
    return re.search(pat, t, re.M) is not None or re.search(rf'^\s*title {tipo} — {cu}\b', t, re.M) is not None


# ---- diagramas de casos de uso por subsistema
puml = {}
for f in glob.glob(D + "diagramas/uml/CU_SS-*.puml"):
    txt = open(f, encoding="utf-8").read()
    for n in re.findall(r'usecase "CU-(\d{3})\\n', txt):
        puml.setdefault(f"CU-{n}", set()).add(os.path.basename(f))
puml_ss = {}
for f in glob.glob(D + "diagramas/uml/CU_SS-*.puml"):
    ss = re.match(r'CU_(SS-\d\d)_', os.path.basename(f)).group(1)
    puml_ss[os.path.basename(f)] = ss

# ---- imágenes
def imagenes(tipo, cu):
    mmd = [f for f in glob.glob(D + f"diagramas/{tipo}_*.mmd")
           if re.search(rf'(?:_|^){cu}(?:_|\.)', os.path.basename(f)) or f"_{cu}_" in os.path.basename(f)]
    res = []
    for f in mmd:
        b = os.path.basename(f)[:-4]
        res.append((b, os.path.exists(D + f"diagramas/png/{b}.png"), os.path.exists(D + f"diagramas/svg/{b}.svg")))
    return res


ESTADO_PLAN = re.compile(r'^Planificado \((I-\d+)\)\. Registrado en el Documento 0, plan de construcción de los casos de uso planificados\.$')
ESTADO_PARCIAL = re.compile(r'^Implementado, con funcionalidad planificada(?: \((I-\d+(?:, I-\d+)*)\))?: .+\.$')

n_plan = n_parcial = 0
for cu in codigos:
    m = cat_cas[cu]
    ss = m.group(3)
    # 1. diagrama del subsistema
    if not any(puml_ss.get(a) == ss for a in puml.get(cu, ())):
        falta(cu, f"no está en el diagrama de casos de uso de {ss}")
    # 2. CUA
    if not tiene_cua(CUA_PLAN, cu):
        falta(cu, "sin CUA en el Documento 0")
    if not tiene_cua(CUA_CAS, cu):
        falta(cu, "sin CUA en Casos-de-Uso.md")
    # 3. CUE
    if not tiene_cue(CUE_REQ, cu):
        falta(cu, "sin CUE en el Documento 1")
    if not tiene_cue(CUE_CAS, cu):
        falta(cu, "sin CUE en Casos-de-Uso.md")
    # 4. DSS (un caso incluido no tiene diagrama propio, pero sí su nota)
    incluido = es_incluido(cu)
    if incluido:
        if not tiene_nota_de_incluido(DSS_ANA, cu):
            falta(cu, "caso incluido sin la nota que remite a su caso base en el Documento 2")
        if not tiene_nota_de_incluido(DSS_CAS, cu):
            falta(cu, "caso incluido sin la nota que remite a su caso base en Casos-de-Uso.md")
        if imagenes("DSS", cu):
            falta(cu, "caso incluido con diagrama de secuencia propio")
    else:
        if not tiene_dia(DSS_ANA, "DSS", cu):
            falta(cu, "sin DSS en el Documento 2")
        if not tiene_dia(DSS_CAS, "DSS", cu):
            falta(cu, "sin DSS en Casos-de-Uso.md")
    # 5. DSD
    if not tiene_dia(DSD_DIS, "DSD", cu):
        falta(cu, "sin DSD en el Documento 3")
    if not tiene_dia(DSD_CAS, "DSD", cu):
        falta(cu, "sin DSD en Casos-de-Uso.md")
    for tipo in ("DSS", "DSD"):
        if tipo == "DSS" and incluido:
            continue
        ims = imagenes(tipo, cu)
        if not ims:
            falta(cu, f"sin .mmd de {tipo}")
        for b, png, svg in ims:
            if not png:
                falta(cu, f"{b}: sin PNG")
            if not svg:
                falta(cu, f"{b}: sin SVG")
    # estado
    mc = re.search(rf'^####\s+[^\n]*?{cu}\s+—.*?\|\s*\*\*Estado\*\*\s*\|\s*([^\n]*?)\s*\|\n', CUE_REQ, re.S | re.M)
    estado = mc.group(1) if mc else ""
    if estado == "Implementado" or estado.startswith("Implementado. Ver ") or estado.startswith("Implementado, con el adaptador"):
        cat = "Implementado"
    elif ESTADO_PLAN.match(estado):
        cat = f"Planificado ({ESTADO_PLAN.match(estado).group(1)})"
        n_plan += 1
    elif ESTADO_PARCIAL.match(estado):
        mm = ESTADO_PARCIAL.match(estado)
        cat = "Implementado, con funcionalidad planificada" + (f" ({mm.group(1)})" if mm.group(1) else "")
        n_parcial += 1
    else:
        falta(cu, f"estado fuera de convención: {estado[:80]!r}")
        continue
    for nombre, cat_doc in (("Casos-de-Uso.md", cat_cas), ("Documento 0", cat_plan)):
        fila = cat_doc.get(cu)
        if not fila:
            falta(cu, f"sin fila en el catálogo de {nombre}")
        elif fila.group(6).strip() != cat:
            falta(cu, f"el catálogo de {nombre} dice {fila.group(6).strip()!r} y el CUE {cat!r}")

# ---- que el catálogo del Documento 0 y el de Casos-de-Uso sean el mismo conjunto
if set(cat_cas) != set(cat_plan):
    falta("catálogos", f"difieren: {sorted(set(cat_cas) ^ set(cat_plan))}")

print(f"Casos de uso en el catálogo: {len(codigos)}")
print(f"  planificados: {n_plan} · implementados con funcionalidad planificada: {n_parcial} · implementados: {len(codigos) - n_plan - n_parcial}")
print("  artefactos por caso: diagrama del subsistema, CUA (Doc 0 y Casos), CUE (Doc 1 y Casos), "
      "DSS (Doc 2 y Casos; los casos incluidos, con su nota) con .mmd, PNG y SVG, DSD (Doc 3 y Casos) con .mmd, PNG y SVG")
if fallas:
    print(f"\n{len(fallas)} falla(s):")
    for f in fallas:
        print("  -", f)
    sys.exit(1)
print("\nTodos los casos de uso tienen sus cinco artefactos y un estado uniforme.")
sys.exit(0)
