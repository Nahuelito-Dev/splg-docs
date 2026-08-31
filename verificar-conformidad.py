#!/usr/bin/env python3
"""Verifica los artefactos UP contra las plantillas de la cátedra (.catedra-ref/*.txt).
Uso:  python3 docs/verificar-conformidad.py
Devuelve 0 si todo cumple, 1 si hay incumplimientos."""
import re, sys, os, collections

D = os.path.dirname(os.path.abspath(__file__)) + "/"
FALLAS = []

def leer(f): return open(D+f, encoding="utf-8").read().split("\n")

def bloques(lineas, ini, fin, item):
    s = next(i for i,x in enumerate(lineas) if re.match(ini,x))
    e = next(i for i,x in enumerate(lineas) if re.match(fin,x))
    idx = [(i,m) for i in range(s,e) if (m:=re.match(item, lineas[i]))]
    out = {}
    for n,(i,m) in enumerate(idx):
        out[m.group(1)] = "\n".join(lineas[i : (idx[n+1][0] if n+1<len(idx) else e)])
    return out

def revisar(nombre, bl, campos, excepciones=()):
    falt = collections.Counter(); vac = collections.Counter()
    for cod, body in bl.items():
        if cod in excepciones: continue
        for c in campos:
            if f"**{c}" not in body: falt[c] += 1
        for m in re.finditer(r'\|\s*\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|', body):
            if m.group(1) in campos and m.group(2).strip() in ("","—","-","–","N/A"):
                vac[m.group(1)] += 1
    estado = "OK" if not falt and not vac else "FALLA"
    if estado == "FALLA": FALLAS.append(nombre)
    print(f"[{estado:5}] {nombre}: {len(bl)} artefactos"
          + (f" | ausentes {dict(falt)}" if falt else "")
          + (f" | en blanco {dict(vac)}" if vac else ""))

CUE = ["Objetivos asociados","Requisitos asociados","Descripción","Precondición","Secuencia Normal",
       "Postcondición","Excepciones","Rendimiento","Frecuencia","Estabilidad","Comentarios"]

# --- CU expandidos (plantilla 1-Requisitos.txt) ---
for f, ini, fin in [("Casos-de-Uso.md", r'^## 5\. ', r'^## 6\. '),
                    ("1-Requisitos.md",  r'^## 7\. ', r'^## 8\. ')]:
    revisar(f"CU expandidos — {f}",
            bloques(leer(f), ini, fin, r'^#{4}\s+.*?(CU-\d+)\s*[—-]'), CUE, excepciones=("CU-003",))

# --- CU de alto nivel (plantilla 0-Plan_Del_Proyecto.txt) ---
for f, ini, fin in [("Casos-de-Uso.md", r'^## 4\. ', r'^## 5\. '),
                    ("0-Plan_Del_Proyecto.md", r'^## 7\. ', r'^## 8\. ')]:
    l = leer(f)
    s = next(i for i,x in enumerate(l) if re.match(ini,x)); e = next(i for i,x in enumerate(l) if re.match(fin,x))
    blk = "\n".join(l[s:e]); n = len(re.findall(r'\*\*Código:\*\*\s*CU-\d+', blk))
    falt = [c for c in ["Caso de Uso","Actor/es","Descripción"] if blk.count(f"**{c}:**") < n]
    if falt: FALLAS.append(f"CUA {f}")
    print(f"[{'OK' if not falt else 'FALLA':5}] CU alto nivel — {f}: {n} artefactos"
          + (f" | campos incompletos {falt}" if falt else ""))

# --- Contratos (plantilla 2.-Análisis.txt) ---
revisar("Contratos de operación — 2-Analisis.md",
        bloques(leer("2-Analisis.md"), r'^## 2\. ', r'^## 3\. ', r'^#{4} .*Contrato: `(.+?)\('),
        ["Nombre","Responsabilidades","Tipo","Referencias cruzadas","Notas","Excepciones",
         "Salida","Precondiciones","Postcondiciones"])

# --- CU reales (plantilla 3.-Diseño.txt) ---
revisar("CU reales — 3-Diseño.md",
        bloques(leer("3-Diseño.md"), r'^## 3\. ', r'^## 4\. ', r'^### 3\.\d+ (CU-\d+)'),
        [c if c != "Secuencia Normal" else "Secuencia normal" for c in CUE])

# --- Requisitos no funcionales (plantilla 1-Requisitos.txt) ---
revisar("Requisitos no funcionales — 1-Requisitos.md",
        bloques(leer("1-Requisitos.md"), r'^## 8\. ', r'^## 9\. ', r'^### .*?(NFR-\d+)'),
        ["Objetivos asociados","Requisitos asociados","Descripción","Comentarios"])

# --- Jerarquía de encabezados (para que el índice de Word/Docs salga bien) ---
malos = [f for f in ["0-Plan_Del_Proyecto.md","0.1-Planificacion_Iteraciones.md","1-Requisitos.md",
                     "2-Analisis.md","3-Diseño.md","Casos-de-Uso.md"]
         if sum(1 for x in leer(f) if x.startswith("# ")) != 1]
if malos: FALLAS.append("jerarquía de encabezados")
print(f"[{'OK' if not malos else 'FALLA':5}] Un solo H1 por documento"
      + (f" | incumplen {malos}" if malos else ""))

# --- Coherencia con el sistema real (no debe reaparecer la ficción previa a la auditoría) ---
resid = []
for f in ["0-Plan_Del_Proyecto.md","0.1-Planificacion_Iteraciones.md","1-Requisitos.md",
          "2-Analisis.md","3-Diseño.md","Casos-de-Uso.md"]:
    for i,x in enumerate(leer(f),1):
        if re.search(r'HS256|JwtAuthGuard|OwnershipGuard|JwtService|JWT propio', x):
            resid.append(f"{f}:{i}")
if resid: FALLAS.append("afirmaciones contradictorias con el código")
print(f"[{'OK' if not resid else 'FALLA':5}] Sin afirmaciones refutadas por la auditoría"
      + (f" | {resid}" if resid else ""))

# --- Módulos inteligentes (criterios de la cátedra) ---
revisar_mod = ["Casos de uso","Descripción","Entradas","Salidas","Parámetros",
               "Por qué no es una consulta","Decisión humana","Precondiciones",
               "Postcondiciones","Diagrama de secuencia"]
l3 = leer("3-Diseño.md")
s3 = next(i for i,x in enumerate(l3) if re.match(r'^## 6\. Módulos', x))
e3 = next(i for i,x in enumerate(l3) if re.match(r'^## 7\. ', x))
mods = [(i,m) for i in range(s3,e3) if (m:=re.match(r'^### 6\.\d+ Módulo (M\d)', l3[i]))]
faltan_mod = {}
for n,(i,m) in enumerate(mods):
    fin = mods[n+1][0] if n+1 < len(mods) else e3
    cuerpo = "\n".join(l3[i:fin]).lower()
    f = [c for c in revisar_mod if c.lower() not in cuerpo]
    if "#### algoritmo" not in cuerpo and "#### proceso" not in cuerpo:
        f.append("Algoritmo o Proceso")
    if f: faltan_mod[m.group(1)] = f
if faltan_mod: FALLAS.append("módulos inteligentes")
print(f"[{'OK' if not faltan_mod else 'FALLA':5}] Módulos inteligentes: {len(mods)} artefactos"
      + (f" | {faltan_mod}" if faltan_mod else ""))

# --- Cobertura de los cuatro artefactos para los 108 CU ---
TODOS = {f"CU-{n:03d}" for n in range(1,109)}
def codigos(f, ini, fin, pat):
    ls = leer(f)
    s = next(i for i,x in enumerate(ls) if re.match(ini,x)); e = next(i for i,x in enumerate(ls) if re.match(fin,x))
    o = set()
    for i in range(s,e):
        if re.search(pat, ls[i]): o.update(re.findall(r'CU-\d+', ls[i]))
    return o & TODOS
cobertura = {
  "CUA (doc 0)": codigos("0-Plan_Del_Proyecto.md", r'^## 7\. ', r'^## 8\. ', r'\*\*Código:\*\*'),
  "CUE (doc 1)": codigos("1-Requisitos.md",        r'^## 7\. ', r'^## 8\. ', r'^#{4}\s+.*CU-\d+'),
  "DSS (doc 2)": codigos("2-Analisis.md",          r'^## 2\. ', r'^## 3\. ', r'^#{3,5}.*CU-\d+'),
  "DSD (doc 3)": codigos("3-Diseño.md",            r'^## 3\. ', r'^## 5\. ', r'^#{3,4}.*CU-\d+'),
}
inc = {k: sorted(TODOS-v) for k,v in cobertura.items() if v != TODOS}
if inc: FALLAS.append("cobertura de artefactos por caso de uso")
print(f"[{'OK' if not inc else 'FALLA':5}] Los 4 artefactos para los 108 casos de uso"
      + (f" | {inc}" if inc else ""))

print()
if FALLAS:
    print(f"INCUMPLIMIENTOS: {len(FALLAS)} -> {FALLAS}"); sys.exit(1)
print("Todos los artefactos cumplen la plantilla de la cátedra."); sys.exit(0)
