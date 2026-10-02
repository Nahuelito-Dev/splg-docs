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

# --- Modelo conceptual (plantilla 2.-Análisis.txt) ---
# La plantilla pide, en este orden: lista de conceptos candidatos (por categoría, con
# ejemplos), lista de conceptos idóneos (descripción, símbolo, intención, extensión),
# relaciones entre los conceptos (por categoría, con ejemplos), descripción de los
# atributos (concepto, atributo – descripción) y el diagrama conceptual.
def _modelo_conceptual():
    txt = "\n".join(leer("2-Analisis.md"))
    ini = txt.index("## 1. Modelo Conceptual"); fin = txt.index("## 2. Comportamiento del Sistema")
    sec = txt[ini:fin]
    falt = []
    orden = [r"### 1\.1 Lista de Conceptos Candidatos", r"### 1\.2 Lista de Conceptos Idóneos",
             r"### 1\.3 Relaciones entre los Conceptos", r"### 1\.4 Descripción de los Atributos",
             r"### 1\.5 Diagrama Conceptual"]
    pos = []
    for o in orden:
        m = re.search(o, sec)
        if not m: falt.append(o.replace("\\", ""))
        else: pos.append(m.start())
    if pos != sorted(pos): falt.append("las cinco secciones no están en el orden de la plantilla")
    celdas = [{c.strip() for c in l.strip().strip("|").split("|")}
              for l in sec.split("\n") if l.startswith("|")]
    for cab in (("Categoría del Concepto", "Ejemplos"),
                ("Descripción del Concepto", "Símbolo", "Intención", "Extensión"),
                ("Categoría de la relación", "Ejemplos"),
                ("Concepto", "Atributo – Descripción")):
        if not any(set(cab) <= fila for fila in celdas):
            falt.append("encabezado de tabla: " + " | ".join(cab))
    d15 = sec[sec.index("### 1.5 Diagrama Conceptual"):]
    if not re.search(r'!\[[^\]]*\]\(diagramas/modelo-conceptual/MC_General\.png\)', d15):
        falt.append("1.5 no embebe la vista general del diagrama conceptual")
    if falt: FALLAS.append("Modelo conceptual")
    print(f"[{'OK' if not falt else 'FALLA':5}] Modelo conceptual — 2-Analisis.md §1: estructura de la plantilla"
          + (f" | {falt}" if falt else ""))
_modelo_conceptual()

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
        if re.search(r'HS256|JwtAuthGuard|OwnershipGuard|JwtService|JWT propio|JWT custom'
                     r'|SIN_COBERTURA|validated === true|hasta 15 km|cada minuto|45 CU'
                     r'|ACT-01 a ACT-04', x):
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

# --- Cobertura de los cuatro artefactos ---
# El total sale del catalogo y no de un numero escrito aca: al pasar de 108 a 149
# casos hubo que tocar este archivo a mano y los documentos siguieron diciendo 108.
_cat = open(D+"Casos-de-Uso.md", encoding="utf-8").read()
_a = _cat.index("\n## 4. "); _b = _cat.index("\n## 5. ")
TODOS = set(re.findall(r'\*\*Código:\*\*\s*(CU-\d+)', _cat[_a:_b]))
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
print(f"[{'OK' if not inc else 'FALLA':5}] Los 4 artefactos para los {len(TODOS)} casos de uso"
      + (f" | {inc}" if inc else ""))

# --- Los conteos que los documentos dicen de si mismos ---
# Cada vez que se suman casos hay frases que quedan diciendo el numero viejo.
_n = str(len(TODOS))
# Se buscan los totales que el catalogo dejo atras, no cualquier numero: hay frases
# legitimas que cuentan una parte ("25 casos de uso reales", "45 casos" del relevamiento
# inicial), y marcarlas seria ruido.
SUPERADOS = {"104", "108", "115", "131", "159", "166"}
_viejos = set()
for _f in ("README.md", "Casos-de-Uso.md", "0-Plan_Del_Proyecto.md", "1-Requisitos.md",
           "2-Analisis.md", "3-Diseño.md", "GUIA-actualizar-drive.md", "INDICE-IMAGENES.md"):
    if not os.path.exists(D+_f): continue
    _t = open(D+_f, encoding="utf-8").read()
    for _m in re.finditer(r'(?<![\d:.-])(\d{2,4})\s+(?:casos de uso|casos\b|diagramas)', _t):
        if _m.group(1) in SUPERADOS and _m.group(1) != _n:
            _viejos.add(f'{_f}: "{_m.group(0)}"')
if _viejos: FALLAS.append("conteos desactualizados en el texto")
print(f"[{'OK' if not _viejos else 'FALLA':5}] Los documentos dicen {_n} casos de uso"
      + (f" | {sorted(_viejos)}" if _viejos else ""))

# --- Diagrama completo de casos de uso y mapa (diagramas/uml/CU_Sistema_*.svg) ---
# Se comprueba el dibujo por sus atributos data-*, no por como se ve: cada actor una
# sola vez y fuera del limite, cada caso con un actor (propio, heredado o por un caso
# que lo incluye), las relaciones iguales a las de los diagramas por subsistema y
# ninguna asociacion que la generalizacion ACT-05 -> ACT-03 vuelva redundante.
import glob
def _attrs(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def _elementos(svg, clase):
    return [_attrs(m) for m in re.findall(r'<(?:g|path|line|rect)\s[^>]*class="%s"[^>]*>' % clase, svg)]

def verificar_diagrama_cu():
    errores = []
    ruta = D + "diagramas/uml/CU_Sistema_Diagrama-Completo.svg"
    rutam = D + "diagramas/uml/CU_Sistema_Mapa.svg"
    if not (os.path.exists(ruta) and os.path.exists(rutam)):
        return ["falta CU_Sistema_Diagrama-Completo.svg o CU_Sistema_Mapa.svg (python3 generar-uml.py)"]
    svg = open(ruta, encoding="utf-8").read()
    mapa = open(rutam, encoding="utf-8").read()
    ESP, GEN = "05", "03"
    # catalogo: actor/es de cada caso
    por_nombre = {"cliente": "01", "chofer": "02", "administrador": "03",
                  "sistema automático": "04", "sistema": "04", "administrador general": "05"}
    cat = {}
    for m in re.finditer(r'\*\*Código:\*\*\s*(CU-\d+)\s*\|[^\n]*\n\*\*Actor/es:\*\*\s*([^\n]*)', _cat[_a:_b]):
        crudo = m.group(2)
        act = set(re.findall(r'ACT-(\d\d)', crudo))
        if not act:
            act = {por_nombre[x.strip().lower()] for x in re.split(r'\s*[,/]\s*|\s+y\s+', crudo)
                   if x.strip().lower() in por_nombre}
        cat[m.group(1)] = act
    for nombre, doc in (("completo", svg), ("mapa", mapa)):
        actores = [a["data-act"] for a in _elementos(doc, "actor")]
        rep = sorted({k for k in actores if actores.count(k) > 1})
        if rep: errores.append(f"{nombre}: actores dibujados mas de una vez {rep}")
        if sorted(actores) != ["01","02","03","04","05","06","07","08"]:
            errores.append(f"{nombre}: los actores dibujados son {sorted(actores)}, no los ocho")
        lim = _elementos(doc, "limite")
        if len(lim) != 1: errores.append(f"{nombre}: falta el limite del sistema"); continue
        x0, x1 = float(lim[0]["data-x"]), float(lim[0]["data-x"]) + float(lim[0]["data-w"])
        dentro = [a["data-act"] for a in _elementos(doc, "actor") if x0 <= float(a["data-x"]) <= x1]
        if dentro: errores.append(f"{nombre}: actores dentro del limite del sistema {dentro}")
        gen = _elementos(doc, "gen")
        if [(g["data-esp"], g["data-gen"]) for g in gen] != [(ESP, GEN)]:
            errores.append(f"{nombre}: falta la generalizacion ACT-{ESP} -> ACT-{GEN}")
    # casos dibujados = los del catalogo
    cus = {c["data-cu"] for c in _elementos(svg, "cu") if c["data-cu"].startswith("CU-")}
    if cus != TODOS:
        errores.append(f"completo: casos de mas {sorted(cus - TODOS)} / de menos {sorted(TODOS - cus)}")
    asoc = [(a["data-act"], a["data-cu"], a["data-rol"]) for a in _elementos(svg, "asoc")]
    # ninguna asociacion repetida ni redundante por la generalizacion
    rep = sorted({x for x in asoc if asoc.count(x) > 1})
    if rep: errores.append(f"completo: asociaciones repetidas {rep[:5]}")
    ppal = {(a, c) for a, c, r in asoc if r == "principal"}
    red = sorted(c for a, c in ppal if a == ESP and (GEN, c) in ppal)
    if red: errores.append(f"completo: ACT-{ESP} repite lo que hereda de ACT-{GEN} en {red[:5]}")
    # relaciones: igual a la union de los diagramas por subsistema
    dib = {(r["data-tipo"], r["data-desde"], r["data-hasta"]) for r in _elementos(svg, "rel")}
    def cod(x): return "F-" + x[2:] if x.startswith("F_") else "CU-" + x[1:]
    sub = set()
    for f in glob.glob(D + "diagramas/uml/CU_SS-*.puml"):
        for m in re.finditer(r'(\w+)\s*\.\.>\s*(\w+)\s*:\s*<<(include|extend)>>', open(f, encoding="utf-8").read()):
            sub.add((m.group(3), cod(m.group(1)), cod(m.group(2))))
    if dib != sub:
        errores.append(f"completo: relaciones de mas {sorted(dib - sub)[:4]} / de menos {sorted(sub - dib)[:4]}")
    # cada caso tiene actor: propio, heredado de ACT-03 por ACT-05, o por un caso que lo incluye
    efec = {c: {a for a, cc in ppal if cc == c} for c in cus}
    for c, s in efec.items():
        if GEN in s: s.add(ESP)
    incl = [(d, h) for t_, d, h in dib if t_ == "include"]
    cambio = True
    while cambio:
        cambio = False
        for base, inc_ in incl:
            if base in efec and inc_ in efec and not efec[inc_] >= efec[base]:
                efec[inc_] |= efec[base]; cambio = True
    sin = sorted(c for c, s in efec.items() if not s)
    if sin: errores.append(f"completo: casos sin actor {sin}")
    falta = sorted(f"{c} sin ACT-{a}" for c, s in cat.items() if c in efec for a in s - efec[c])
    if falta: errores.append(f"completo: el catalogo dice mas actores que el dibujo {falta[:5]}")
    # mapa: los 18 paquetes con su cantidad de casos
    cuenta = collections.Counter()
    for m in re.finditer(r'\*\*Código:\*\*\s*CU-\d+\s*\|[^\n]*\n(?:\*\*[^\n]*\n)*?\*\*Subsistema:\*\*\s*(SS-\d\d)', _cat[_a:_b]):
        cuenta[m.group(1)] += 1
    paq = {p["data-pq"]: int(p["data-n"]) for p in _elementos(mapa, "paquete")}
    if paq != dict(cuenta):
        errores.append(f"mapa: paquetes {paq} distintos del catalogo {dict(cuenta)}")
    return errores

_errs = verificar_diagrama_cu()
if _errs: FALLAS.append("diagrama completo de casos de uso")
print(f"[{'OK' if not _errs else 'FALLA':5}] Diagrama completo y mapa de casos de uso: actores una vez y afuera, generalizacion, relaciones = subsistemas"
      + (f" | {_errs}" if _errs else ""))

# --- Secciones que pide la plantilla para el Doc 0, el 0.1 y el Doc 1, y figuras de los documentos ---
def seccion(texto, ini, fin=None):
    a = texto.index(ini)
    b = texto.index(fin, a + len(ini)) if fin else len(texto)
    return texto[a:b]

def tabla_con(texto, columnas):
    """True si hay una tabla markdown cuya cabecera contiene todas esas columnas."""
    for l in texto.split("\n"):
        if l.startswith("|"):
            cab = [c.strip() for c in l.strip().strip("|").split("|")]
            if all(c in cab for c in columnas): return True
    return False

def verificar_plantillas():
    errores = []
    d0 = "\n".join(leer("0-Plan_Del_Proyecto.md"))
    # orden de la plantilla del Plan del Proyecto
    orden = ["## 2. Plan de las Fases", "## 3. Hitos por Fase", "## 4. Calendario del Proyecto",
             "## 5. Actores del Sistema", "## 6. Diagrama de Casos de Uso del Sistema",
             "## 7. Casos de Uso de Alto Nivel", "## 8. Calificación de los Casos de Uso"]
    pos = [d0.find(t) for t in orden]
    if -1 in pos or pos != sorted(pos):
        errores.append("Doc 0: las secciones no están en el orden de la plantilla")
        return errores
    fases = seccion(d0, orden[0], orden[1])
    if not tabla_con(fases, ["Fase", "Nro. Iteraciones", "Duración"]):
        errores.append("Doc 0 §2: falta la tabla Fase · Nro. Iteraciones · Duración")
    for fase in ("Inicio", "Elaboración", "Construcción", "Transición"):
        if f"| Fase de {fase} |" not in fases: errores.append(f"Doc 0 §2: falta la fila de la Fase de {fase}")
    hitos = seccion(d0, orden[1], orden[2])
    if not tabla_con(hitos, ["Descripción", "Hito"]):
        errores.append("Doc 0 §3: falta la tabla Descripción · Hito")
    fila_c = next((l for l in hitos.split("\n") if l.startswith("| Fase de Construcción")), "")
    falt = [f"I-{n}" for n in range(1, 11) if f"(I-{n})" not in fila_c]
    if falt: errores.append(f"Doc 0 §3: el hito de Construcción no refleja las iteraciones {falt}")
    cal = seccion(d0, orden[2], orden[3])
    if "### Cronograma (Diagrama de Gantt)" not in cal or "UML_Gantt." not in cal:
        errores.append("Doc 0 §4: falta el Cronograma (Diagrama de Gantt) como figura")
    gantt = open(D + "diagramas/uml/UML_Gantt.puml", encoding="utf-8").read()
    for cod in ["INI", "E01", "C01", "C02", "C03", "C04", "C05", "C06", "T01"] + [f"I{n}" for n in range(1, 11)]:
        if f"[{cod}]" not in gantt: errores.append(f"Gantt: falta la barra {cod}")
    if gantt.count("happens") < 5: errores.append("Gantt: faltan los hitos de cierre")
    if not tabla_con(seccion(d0, orden[3], orden[4]), ["Actor", "Descripción"]):
        errores.append("Doc 0 §5: falta la tabla Actor · Descripción")
    if not tabla_con(seccion(d0, orden[6]), ["Caso de Uso", "Calificación"]):
        errores.append("Doc 0 §8: falta la tabla Caso de Uso · Calificación")

    # Plan de Iteración (0.1)
    d01 = "\n".join(leer("0.1-Planificacion_Iteraciones.md"))
    cab = d01[:d01.index("\n## ")]
    for campo in ("Proyecto", "Título", "Generado por", "Aprobado por", "Alcance de la distribución"):
        if f"**{campo}:**" not in cab: errores.append(f"0.1: falta «{campo}» en la cabecera")
    for t in ("## Lista de Cambios", "## Sobre este Documento", "### Configuración de la Iteración"):
        if t not in d01: errores.append(f"0.1: falta «{t.lstrip('# ')}»")
    for cod, titulo in (("C-06", "## Iteración C-06"), ("I-1", "## Iteración I-1"), ("T-01", "## Iteración T-01")):
        try:
            a = d01.index(titulo); b = d01.find("\n## ", a + 5)
            blq = d01[a:b if b != -1 else len(d01)]
        except ValueError:
            errores.append(f"0.1: falta el plan de la iteración {cod}"); continue
        for h in ("### Identificación", "### Metas", "### Requisitos de la Iteración", "### Artefactos Nuevos",
                  "### Artefactos Actualizados", "### Requisitos Suplementarios", "### Problemas a Resolver"):
            if h not in blq: errores.append(f"0.1 {cod}: falta «{h.lstrip('# ')}»")
        for campo in ("Código de la Iteración", "Fase a la que pertenece", "Fecha de Inicio", "Fecha de Cierre", "Comentarios"):
            if f"| {campo} |" not in blq: errores.append(f"0.1 {cod}: la identificación no tiene «{campo}»")
        nuevos = seccion(blq, "### Artefactos Nuevos", "### Artefactos Actualizados") if "### Artefactos Actualizados" in blq else ""
        if not tabla_con(nuevos, ["Artefacto", "Meta", "Comentarios"]):
            errores.append(f"0.1 {cod}: Artefactos Nuevos no es Artefacto · Meta · Comentarios")
        act = seccion(blq, "### Artefactos Actualizados", "### Requisitos Suplementarios") if "### Requisitos Suplementarios" in blq else ""
        if not tabla_con(act, ["Artefacto", "Actual", "Meta", "Objetivo de la Actualización"]):
            errores.append(f"0.1 {cod}: Artefactos Actualizados no es Artefacto · Actual · Meta · Objetivo")
        if "### Requisitos de la Iteración" in blq:
            req = seccion(blq, "### Requisitos de la Iteración", "### Artefactos Nuevos")
            for p in ("entradas", "salidas", "contexto"):
                if f"({p})" not in req: errores.append(f"0.1 {cod}: Requisitos de la Iteración sin el punto de vista «{p}»")

    # Doc 1: Diagrama de Casos de Uso y Subsistemas del Proyecto
    d1 = "\n".join(leer("1-Requisitos.md"))
    s3 = seccion(d1, "## 3. Diagrama de Casos de Uso del Sistema", "## 4. Subsistemas del Proyecto")
    if not re.search(r'\*\*Figura \d+ — Diagrama de Casos de Uso del Sistema\*\*', s3) or "CU_Sistema_Diagrama-Completo" not in s3:
        errores.append("Doc 1 §3: falta el Diagrama de Casos de Uso del Sistema como figura numerada")
    s4 = seccion(d1, "## 4. Subsistemas del Proyecto", "## 5. Objetivos de la Iteración")
    if not re.search(r'\*\*Figura \d+ — Diagrama de Subsistemas\*\*', s4) or "CU_Sistema_Subsistemas" not in s4:
        errores.append("Doc 1 §4: falta el Diagrama de Subsistemas como figura numerada")
    desc = set(re.findall(r'^\|\s*\*{0,2}(SS-\d\d)\*{0,2}\s*\|[^|]*\|\s*\S', s4, re.M))
    if len(desc) != 18: errores.append(f"Doc 1 §4: describe {len(desc)} subsistemas de 18")
    emb = set(re.findall(r'diagramas/uml/CU_(SS-\d\d)_[^)]*\.png\)', s4))
    if len(emb) != 18: errores.append(f"Doc 1 §4.3: embebe {len(emb)} diagramas por subsistema de 18")
    if "CU_Sistema_Diagrama-De-Contexto.png)" not in s4: errores.append("Doc 1 §4.3: falta el diagrama de contexto")

    # figuras: toda imagen existe y lleva su epígrafe numerado
    for doc in ("0-Plan_Del_Proyecto.md", "1-Requisitos.md", "3-Diseño.md"):
        ls = leer(doc)
        for i, l in enumerate(ls):
            m = re.match(r'^!\[[^\]]*\]\((diagramas/uml/[^)]+)\)\s*$', l)
            if not m: continue
            if not os.path.exists(D + m.group(1)): errores.append(f"{doc}: no existe {m.group(1)}")
            vec = [x for x in ls[max(0, i - 3):i + 4] if re.match(r'^\*\*Figura \d+ — ', x)]
            if not vec: errores.append(f"{doc}: la imagen {m.group(1)} no tiene epígrafe numerado")
    d3 = "\n".join(leer("3-Diseño.md"))
    for img in ("UML_Componentes", "UML_Despliegue", "UML_Estados_Pedido", "UML_Estados_Reclamo", "UML_Estados_Envase",
                "UML_Estados_Reserva", "UML_Estados_TareaFlota", "UML_Estados_OfertaDespacho",
                "UML_Actividad_Despacho", "UML_Actividad_CicloPedido"):
        if f"diagramas/uml/{img}.png" not in d3: errores.append(f"Doc 3: falta el diagrama {img}")
    return errores

_errs = verificar_plantillas()
if _errs: FALLAS.append("secciones de la plantilla y figuras")
print(f"[{'OK' if not _errs else 'FALLA':5}] Secciones de la plantilla (Doc 0, 0.1, Doc 1) y figuras de los diagramas UML"
      + (f" | {_errs}" if _errs else ""))

# --- Operaciones del sistema: diagramas de secuencia, catálogo y contratos ---
# El catálogo (material-de-trabajo/operaciones-sistema.json) es la única fuente de las
# firmas. Los DSS tienen que dibujar al sistema como :Sistema, iniciar con un actor del
# catálogo de actores (ACT-01 a ACT-08), no tener mensajes del sistema a sí mismo, usar un
# mensaje asíncrono con nombre (notificar...) para lo que el sistema le manda a un actor
# sin que lo haya pedido, y llamar a cada operación con la misma firma que el catálogo.
# Cada operación que cambia estado tiene su contrato, con los campos de la plantilla de la
# cátedra en su orden.
import json
CAMPOS_CONTRATO = ["Nombre","Responsabilidades","Tipo","Referencias cruzadas","Notas",
                   "Excepciones","Salida","Precondiciones","Postcondiciones"]

def verificar_operaciones():
    errores = []
    ruta = D + "material-de-trabajo/operaciones-sistema.json"
    if not os.path.exists(ruta):
        return ["falta material-de-trabajo/operaciones-sistema.json"]
    cat = json.load(open(ruta, encoding="utf-8"))
    actores = cat["actores"]
    ops = {o["nombre"]: o for o in cat["operaciones"]}
    nombres = {m.group(1): m.group(2).strip()
               for m in re.finditer(r'^\| (CU-\d{3}) ([^|]+?) \| SS-\d\d \|', _cat, re.M)}
    # un caso incluido no lo inicia ningún actor: no tiene diagrama de secuencia propio
    incluidos = {m.group(1) for m in re.finditer(
        r'\*\*Código:\*\*\s*(CU-\d+)\s*\|[^\n]*\n\*\*Actor/es:\*\*\s*([^\n]*)', _cat[_a:_b])
        if "caso incluido" in m.group(2).lower() or "ninguno directo" in m.group(2).lower()}
    vistas = {}
    for f in sorted(glob.glob(D + "diagramas/DSS_*.mmd")):
        base = os.path.basename(f)
        cu = re.search(r'CU-\d+', base).group(0)
        t = open(f, encoding="utf-8").read()
        if cu in incluidos:
            errores.append(f"{base}: {cu} es un caso incluido y no lleva diagrama de secuencia propio")
        if f"title DSS — {cu} {nombres.get(cu, '?')}" not in t:
            errores.append(f"{base}: el título no es «DSS — {cu} {nombres.get(cu, '?')}»")
        if not re.search(r'^\s*participant\s+SIS\s+as\s+:Sistema\s*$', t, re.M):
            errores.append(f"{base}: el sistema no es la lifeline :Sistema")
        parts = {}
        for m in re.finditer(r'^\s*actor\s+(\w+)\s+as\s+(.+?)\s*$', t, re.M):
            mm = re.match(r'^(.+) \((ACT-0[1-8])\)$', m.group(2))
            if not mm or mm.group(2) not in actores:
                errores.append(f"{base}: el actor «{m.group(2)}» no lleva un código del catálogo (ACT-01 a ACT-08)")
            else:
                parts[m.group(1)] = (mm.group(1), mm.group(2))
        if re.search(r'^\s*SIS\s*-{1,2}[>)]{1,2}\s*SIS\b', t, re.M):
            errores.append(f"{base}: el sistema se manda mensajes a sí mismo (va como Note)")
        iniciadores = set()
        for m in re.finditer(r'^\s*(\w+)\s*(-{1,2}[>)]{1,2})\s*(\w+):\s*(.*?)\s*$', t, re.M):
            org, flecha, dst, txt = m.groups()
            if dst == "SIS" and org != "SIS":
                iniciadores.add(org)
                if org not in parts:
                    continue
                if parts[org][0] != actores[parts[org][1]]:
                    errores.append(f"{base}: el iniciador «{parts[org][0]}» no se llama como en el catálogo ({actores[parts[org][1]]})")
                nom = txt.split("(")[0]
                o = ops.get(nom)
                if not o:
                    errores.append(f"{base}: la operación {txt!r} no está en el catálogo")
                    continue
                if o["firma"] != txt:
                    errores.append(f"{base}: {txt!r} no es la firma del catálogo {o['firma']!r}")
                vistas.setdefault(nom, set()).add(cu)
                if parts[org][1] not in o["actores"]:
                    errores.append(f"{base}: {nom} la inicia {parts[org][1]} y el catálogo no la lista")
        for m in re.finditer(r'^\s*SIS\s*(-{1,2}[>)]{1,2})\s*(\w+):\s*(.*?)\s*$', t, re.M):
            flecha, dst, txt = m.groups()
            if dst == "SIS": continue
            noti = re.match(r'notificar\w+\(', txt) is not None
            if dst not in iniciadores and not (flecha == "-)" and noti):
                errores.append(f"{base}: lo que el sistema le manda a un actor que no lo pidió debe ser un mensaje asíncrono notificar...(): {txt!r}")
            if flecha == "-)" and not noti:
                errores.append(f"{base}: el mensaje asíncrono {txt!r} no es una notificación con nombre")
    for nom, o in ops.items():
        if nom not in vistas:
            errores.append(f"catálogo: {nom} no aparece en ningún diagrama de secuencia")
        elif sorted(vistas[nom]) != o["casosDeUso"]:
            errores.append(f"catálogo: {nom} dice {o['casosDeUso']} y los diagramas {sorted(vistas[nom])}")
    # contratos
    l2 = leer("2-Analisis.md")
    s2 = next(i for i,x in enumerate(l2) if re.match(r'^## 2\. ', x))
    e2 = next(i for i,x in enumerate(l2) if re.match(r'^## 3\. ', x))
    contratos = bloques(l2, r'^## 2\. ', r'^## 3\. ', r'^#{4} .*Contrato: `(.+?)\(')
    for nom, o in ops.items():
        if o["cambiaEstado"] and nom not in contratos:
            errores.append(f"contratos: {nom} cambia estado y no tiene contrato")
        if not o["cambiaEstado"] and nom in contratos:
            errores.append(f"contratos: {nom} no cambia estado y tiene contrato")
    for nom, cuerpo in contratos.items():
        if nom not in ops:
            errores.append(f"contratos: {nom} no está en el catálogo")
            continue
        campos = re.findall(r'^\|\s*\*\*(.+?)\*\*\s*\|', cuerpo, re.M)
        if campos != CAMPOS_CONTRATO:
            errores.append(f"contratos: {nom} tiene los campos {campos}, la plantilla pide {CAMPOS_CONTRATO}")
        m = re.search(r'^\|\s*\*\*Nombre\*\*\s*\|\s*`(.+?)`\s*\|', cuerpo, re.M)
        if m and m.group(1) != ops[nom]["firmaConTipos"]:
            errores.append(f"contratos: el nombre de {nom} no es la firma del catálogo ({ops[nom]['firmaConTipos']})")
    return errores

_errs_op = verificar_operaciones()
if _errs_op: FALLAS.append("operaciones del sistema (DSS, catálogo y contratos)")
print(f"[{'OK' if not _errs_op else 'FALLA':5}] Operaciones del sistema: DSS con :Sistema, iniciador del catálogo y sin auto-mensajes; una firma por operación; contrato de cada una que cambia estado"
      + (f" | {len(_errs_op)} errores: {_errs_op[:6]}" if _errs_op else ""))

# --- DSD en estilo Larman (material-de-trabajo/GUIA-DSD-LARMAN.md) ---
# Un DSD ya rehecho tiene que cumplir las reglas de la guía. Las operaciones del catálogo que
# todavía no tienen su DSD se informan y no fallan el gate hasta que se cierra la reescritura:
# entonces se corre con DSD_ESTRICTO=1 (o se fija el valor por omisión acá).
sys.path.insert(0, D + "material-de-trabajo")
import dsd_larman
_estricto = os.environ.get("DSD_ESTRICTO", "1") == "1"  # estricto por omisión: las 195 operaciones tienen su DSD
_errs_dsd, _pend_dsd, _hechos_dsd = dsd_larman.verificar(estricto=_estricto)
if _errs_dsd: FALLAS.append("DSD en estilo Larman")
print(f"[{'OK' if not _errs_dsd else 'FALLA':5}] DSD en estilo Larman: {len(_hechos_dsd)} hechos, {len(_pend_dsd)} operaciones del catálogo todavía sin DSD, {len(dsd_larman.AVISOS)} avisos"
      + (" (modo estricto)" if _estricto else " (se informan; DSD_ESTRICTO=1 las hace fallar)")
      + (f" | {len(_errs_dsd)} errores: {_errs_dsd[:6]}" if _errs_dsd else ""))

# --- Diagrama de clases de diseño derivado de los DSD (Doc 3 §5) ---
# Se lee lo que está dibujado (diagramas/clases-diseno/*.puml) y se contrasta con los DSD y con el
# modelo conceptual: toda operación y toda clase de un DSD está en el diagrama; las clases de dominio
# son las del modelo conceptual, con sus atributos, sus asociaciones, su multiplicidad y la
# navegabilidad que piden los mensajes; todo en notación UML y sin sintaxis del código.
import dc_larman
_errs_dc, _cif_dc = dc_larman.verificar_dc()
if _errs_dc: FALLAS.append("Diagrama de clases de diseño")
print(f"[{'OK' if not _errs_dc else 'FALLA':5}] Diagrama de clases de diseño: "
      f"{_cif_dc.get('clases', 0)} clases, {_cif_dc.get('operaciones', 0)} mensajes de los DSD con su operación"
      + (f" | {len(_errs_dc)} errores: {_errs_dc[:6]}" if _errs_dc else ""))

print()
if FALLAS:
    print(f"INCUMPLIMIENTOS: {len(FALLAS)} -> {FALLAS}"); sys.exit(1)
print("Todos los artefactos cumplen la plantilla de la cátedra."); sys.exit(0)
