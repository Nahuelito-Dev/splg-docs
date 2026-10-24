#!/usr/bin/env python3
"""Verifica los artefactos UP contra las plantillas de la cátedra (catedra/.catedra-ref/*.txt).
Uso:  python3 docs/verificar-conformidad.py
Devuelve 0 si todo cumple, 1 si hay incumplimientos."""
import re, sys, os, collections

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
FALLAS = []

def ruta_doc(n):
    """README y AGENTS viven en la raíz; los documentos, en documentos/."""
    return D + n if os.path.exists(D + n) else DOC + n

def leer(f): return open(ruta_doc(f), encoding="utf-8").read().split("\n")

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
            bloques(leer(f), ini, fin, r'^#{4}\s+.*?(CU-\d+)\s*[—-]'), CUE)

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
    if not re.search(r'!\[[^\]]*\]\(\.\./diagramas/modelo-conceptual/MC_General\.png\)', d15):
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
_cat = open(DOC + "Casos-de-Uso.md", encoding="utf-8").read()
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
# 249 ya no es un total viejo: es lo que inicia el Administrador (ACT-03).
SUPERADOS = {"104", "108", "115", "131", "159", "166", "174"}
_viejos = set()
for _f in ("README.md", "Casos-de-Uso.md", "0-Plan_Del_Proyecto.md", "1-Requisitos.md",
           "2-Analisis.md", "3-Diseño.md", "GUIA-actualizar-drive.md", "INDICE-IMAGENES.md"):
    if not os.path.exists(ruta_doc(_f)): continue
    _t = open(ruta_doc(_f), encoding="utf-8").read()
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

def geometria(nombre, doc):
    """Ninguna asociación ni relación atraviesa un óvalo que no sea su extremo (0 líneas sobre óvalos ajenos)."""
    errores = []
    ovalos = {}
    for m_ in re.finditer(r'<g class="cu" data-cu="(CU-\d+)"[^>]*><ellipse cx="([\d.]+)" cy="([\d.]+)" rx="([\d.]+)" ry="([\d.]+)"', doc):
        ovalos[m_.group(1)] = tuple(float(x_) for x_ in m_.groups()[1:])
    cubos = collections.defaultdict(list)
    for c_, (cx_, cy_, rx_, ry_) in ovalos.items():
        for b_ in range(int((cy_ - ry_) // 40), int((cy_ + ry_) // 40) + 1): cubos[b_].append(c_)
    def cruza(segs, permitidos):
        malos = set()
        for (x0_, y0_, x1_, y1_) in segs:
            largo = max(abs(x1_ - x0_), abs(y1_ - y0_))
            n_ = int(largo // 3) + 1
            for i_ in range(1, n_):
                x_ = x0_ + (x1_ - x0_) * i_ / n_; y_ = y0_ + (y1_ - y0_) * i_ / n_
                for c_ in cubos.get(int(y_ // 40), ()):
                    if c_ in permitidos: continue
                    cx_, cy_, rx_, ry_ = ovalos[c_]
                    if ((x_ - cx_) / rx_) ** 2 + ((y_ - cy_) / ry_) ** 2 < 0.98: malos.add(c_)
        return malos
    for a_ in _elementos(doc, "asoc"):
        d_ = re.match(r'M([\d.]+) ([\d.]+) L([\d.]+) ([\d.]+)', a_["d"])
        if cruza([tuple(float(x_) for x_ in d_.groups())], {a_.get("data-cu", "")}):
            errores.append(f"{nombre}: la asociación {a_['data-act']}–{a_['data-cu']} atraviesa un óvalo")
    for r_ in _elementos(doc, "rel"):
        toks = re.findall(r'([MHV])([\d.]+)(?: ([\d.]+))?', r_["d"])
        x_, y_ = float(toks[0][1]), float(toks[0][2]); segs = []
        for t_, a1, a2 in toks[1:]:
            nx_, ny_ = (float(a1), y_) if t_ == "H" else (x_, float(a1))
            segs.append((x_, y_, nx_, ny_)); x_, y_ = nx_, ny_
        if cruza(segs, {r_["data-desde"], r_["data-hasta"]}):
            errores.append(f"{nombre}: la relación {r_['data-desde']}→{r_['data-hasta']} atraviesa un óvalo")
    return errores

def verificar_diagrama_cu():
    errores = []
    laminas = sorted(glob.glob(D + "diagramas/uml/CU_Sistema_Completo-Lamina-*.svg"))
    rutam = D + "diagramas/uml/CU_Sistema_Mapa.svg"
    por_ss = sorted(glob.glob(D + "diagramas/uml/CU_SS-*.svg"))
    if not laminas or not os.path.exists(rutam) or not por_ss:
        return ["faltan las láminas, el mapa o los diagramas por subsistema (python3 herramientas/generar-uml.py)"]
    ESP, GEN = "05", "03"
    por_nombre = {"cliente": "01", "chofer": "02", "administrador": "03",
                  "sistema automático": "04", "sistema": "04", "administrador general": "05", "operador técnico": "10"}
    cat_ss = {m.group(1): m.group(2) for m in re.finditer(r'\*\*Código:\*\*\s*(CU-\d+)\s*\|[^\n]*\n(?:\*\*[^\n]*\n)*?\*\*Subsistema:\*\*\s*(SS-\d\d)', _cat[_a:_b])}
    cat = {}
    for m in re.finditer(r'\*\*Código:\*\*\s*(CU-\d+)\s*\|[^\n]*\n\*\*Actor/es:\*\*\s*([^\n]*)', _cat[_a:_b]):
        crudo = m.group(2)
        act = set(re.findall(r'ACT-(\d\d)', crudo))
        if not act:
            act = {por_nombre[x.strip().lower()] for x in re.split(r'\s*[,/]\s*|\s+y\s+', crudo)
                   if x.strip().lower() in por_nombre}
        cat[m.group(1)] = act
    # formato único: actores en una sola columna a la izquierda y fuera del límite del sistema
    def revisar(nombre, doc, con_generalizacion=True):
        actores = [a["data-act"] for a in _elementos(doc, "actor")]
        rep = sorted({k for k in actores if actores.count(k) > 1})
        if rep: errores.append(f"{nombre}: actores dibujados mas de una vez {rep}")
        lim = _elementos(doc, "limite")
        if len(lim) != 1: errores.append(f"{nombre}: falta el limite del sistema"); return actores
        x0 = float(lim[0]["data-x"])
        xs = {float(a["data-x"]) for a in _elementos(doc, "actor")}
        if len(xs) > 1: errores.append(f"{nombre}: los actores no están en una sola columna {sorted(xs)}")
        if any(x >= x0 for x in xs): errores.append(f"{nombre}: actores dentro o a la derecha del limite del sistema")
        if ESP in actores and GEN in actores:
            gen = _elementos(doc, "gen")
            if [(g["data-esp"], g["data-gen"]) for g in gen] != [(ESP, GEN)]:
                errores.append(f"{nombre}: falta la generalizacion ACT-{ESP} -> ACT-{GEN}")
        return actores
    leer = lambda f: open(f, encoding="utf-8").read()
    docs_lam = {os.path.basename(f): leer(f) for f in laminas}
    todos_act = set()
    for n, doc in docs_lam.items(): todos_act |= set(revisar(n, doc))
    mapa = leer(rutam)
    todos_act_mapa = set(revisar("mapa", mapa))
    if todos_act != {"01","02","03","04","05","06","07","08","09","10"}:
        errores.append(f"laminas: los actores dibujados son {sorted(todos_act)}, no los diez")
    if todos_act_mapa != todos_act: errores.append("mapa: no dibuja los mismos actores que las láminas")
    # casos dibujados (con su propio recuadro, no el de referencia) = los del catalogo
    cus = set(); asoc = []; dib = set()
    for n, doc in docs_lam.items():
        cus |= {c["data-cu"] for c in _elementos(doc, "cu") if c["data-cu"].startswith("CU-")}
        asoc += [(a["data-act"], a["data-cu"], a["data-rol"]) for a in _elementos(doc, "asoc")]
        dib |= {(r["data-tipo"], r["data-desde"], r["data-hasta"]) for r in _elementos(doc, "rel")}
    if cus != TODOS:
        errores.append(f"laminas: casos de mas {sorted(cus - TODOS)} / de menos {sorted(TODOS - cus)}")
    rep = sorted({x for x in asoc if asoc.count(x) > 1})
    if rep: errores.append(f"laminas: asociaciones repetidas {rep[:5]}")
    # relaciones: las de las láminas = las de los diagramas por subsistema
    sub = set()
    for f in por_ss:
        d_ = leer(f)
        for r in _elementos(d_, "rel"):
            if r["data-desde"].startswith("F-") or r["data-hasta"].startswith("F-"): continue
            sub.add((r["data-tipo"], r["data-desde"], r["data-hasta"]))
        revisar(os.path.basename(f), d_)
    if dib - sub:
        errores.append(f"laminas: relaciones que los diagramas por subsistema no tienen {sorted(dib - sub)[:4]}")
    # --- los actores de cada caso: el catálogo (todos, también ACT-05 junto a ACT-03) más los sistemas externos ---
    sys.path.insert(0, D + "herramientas")
    from actores_cu import SECUNDARIO as _SEC
    esperado = {c: set(s_) | {k for k, lst in _SEC.items() if c in lst} for c, s_ in cat.items()}
    def conectados(doc):
        d_ = collections.defaultdict(set)
        for a_ in _elementos(doc, "asoc"): d_[a_["data-cu"]].add(a_["data-act"])
        return d_
    def con_entrada(doc):
        return {r["data-hasta"] for r in _elementos(doc, "rel") if r["data-tipo"] == "include"}
    # diagrama único: los 340 casos una vez, cada uno con sus actores exactos, ninguno aislado y todas las relaciones de §7.7
    ruta_u = D + "diagramas/uml/CU_Sistema_Diagrama-Completo.svg"
    if not os.path.exists(ruta_u):
        errores.append("falta el diagrama único de casos de uso")
    else:
        du = leer(ruta_u)
        cu_u = [c["data-cu"] for c in _elementos(du, "cu")]
        if len(cu_u) != len(set(cu_u)) or set(cu_u) != TODOS:
            errores.append(f"único: casos repetidos {sorted(x for x in set(cu_u) if cu_u.count(x) > 1)[:5]} / de más {sorted(set(cu_u) - TODOS)[:5]} / de menos {sorted(TODOS - set(cu_u))[:5]}")
        con = conectados(du); ent = con_entrada(du)
        aisl = sorted(c for c in TODOS if not con.get(c) and c not in ent)
        if aisl: errores.append(f"único: casos aislados {aisl[:8]}")
        dif = sorted(f"{c}: dibuja {sorted(con.get(c, set()))} y el catálogo dice {sorted(esperado[c])}" for c in TODOS if con.get(c, set()) != esperado.get(c, set()))
        if dif: errores.append(f"único: {len(dif)} casos con actores distintos del catálogo, p. ej. {dif[:3]}")
        for _c_ in geometria("único", du): errores.append(_c_)
        d1 = leer(DOC + "1-Requisitos.md")
        i77 = d1.index("### 7.7 Relaciones entre Casos de Uso")
        j77 = d1.find("\n### 7.8", i77)
        if j77 < 0: j77 = d1.index("\n## 8.", i77)
        s77 = d1[i77:j77]
        tabla = set()
        modo = None
        for l_ in s77.split("\n"):
            if "Relaciones `«include»`" in l_: modo = "include"
            elif "Relaciones `«extend»`" in l_: modo = "extend"
            m_ = re.match(r'^\|(?: PE-\d+ \|)? (CU-\d{3}) [^|]+ \| → \| (CU-\d{3}) ', l_)
            if m_ and modo: tabla.add((modo, m_.group(1), m_.group(2)))
        dib_u = {(r["data-tipo"], r["data-desde"], r["data-hasta"]) for r in _elementos(du, "rel")}
        falt = sorted(tabla - dib_u); sob = sorted(dib_u - tabla)
        if falt: errores.append(f"único: relaciones de §7.7 que no se dibujan o van al revés {falt[:5]}")
        if sob: errores.append(f"único: relaciones dibujadas que no están en §7.7 {sob[:5]}")
    # diagramas por subsistema: los actores exactos de sus casos propios y ningún caso aislado
    for f_ in por_ss:
        d_ = leer(f_); ss_ = re.search(r'CU_(SS-\d\d)_', f_).group(1)
        con = conectados(d_); ent = con_entrada(d_)
        errores += geometria(os.path.basename(f_), d_)
        propios = {c for c in re.findall(r'<g class="cu" data-cu="(CU-\d+)"[^>]*><ellipse(?![^>]*stroke-dasharray)', d_) if cat_ss.get(c) == ss_}
        for c in sorted(propios):
            if con.get(c, set()) != esperado.get(c, set()) and not (not esperado.get(c) and c in ent):
                errores.append(f"{os.path.basename(f_)}: {c} dibuja {sorted(con.get(c, set()))} y el catálogo dice {sorted(esperado.get(c, set()))}")
            if not con.get(c) and c not in ent and not any(r["data-desde"] == c or r["data-hasta"] == c for r in _elementos(d_, "rel")):
                errores.append(f"{os.path.basename(f_)}: {c} está aislado")
    # láminas por actor: cada caso propio unido a su actor y ninguno aislado
    for n_, doc_ in docs_lam.items():
        errores += geometria(n_, doc_)
        acs = [a_["data-act"] for a_ in _elementos(doc_, "actor")]
        con = conectados(doc_)
        for c in {c_["data-cu"] for c_ in _elementos(doc_, "cu")}:
            if acs and acs[0] not in con.get(c, set()): continue
        for c, s_ in con.items():
            if len(s_) != 1 or next(iter(s_)) != acs[0]:
                errores.append(f"{n_}: {c} dibuja {sorted(s_)} y la lámina es de ACT-{acs[0]}")
        propios = {c for c in cat if acs and acs[0] in esperado[c]}
        enlam = set(re.findall(r'<g class="cu" data-cu="(CU-\d+)"[^>]*><ellipse(?![^>]*stroke-dasharray)', doc_))
        for c in sorted(enlam & propios):
            if acs[0] not in con.get(c, set()): errores.append(f"{n_}: {c} no está unido a ACT-{acs[0]}")
    # diagrama de casos de uso por subsistemas: un paquete por subsistema con su cantidad de casos y cada actor unido
    # a los subsistemas en los que participa (los de sus casos, principales y secundarios)
    ruta_p = D + "diagramas/uml/CU_Sistema_Diagrama-De-Subsistemas.svg"
    if not os.path.exists(ruta_p):
        errores.append("falta el diagrama de subsistemas (CU_Sistema_Diagrama-De-Subsistemas.svg)")
    else:
        dp = leer(ruta_p)
        revisar("subsistemas (paquetes)", dp)
        cuenta_p = collections.Counter(cat_ss[c] for c in cat_ss)
        paq_p = {p_["data-pq"]: int(p_["data-n"]) for p_ in _elementos(dp, "paquete")}
        if paq_p != dict(cuenta_p): errores.append(f"subsistemas (paquetes): {paq_p} distintos del catálogo {dict(cuenta_p)}")
        esp_p = collections.defaultdict(set)
        for c, s_ in esperado.items(): esp_p[cat_ss[c]] |= s_
        dib_p = collections.defaultdict(set)
        for a_ in _elementos(dp, "asoc"): dib_p[a_["data-pq"]].add(a_["data-act"])
        for ss_p in sorted(esp_p):
            if dib_p.get(ss_p, set()) != esp_p[ss_p]:
                errores.append(f"subsistemas (paquetes): {ss_p} dibuja {sorted(dib_p.get(ss_p, set()))} y sus casos tienen {sorted(esp_p[ss_p])}")
    # los diagramas por subsistema dibujan los mismos casos
    cus_ss = set()
    for f in por_ss:
        cus_ss |= {c["data-cu"] for c in _elementos(leer(f), "cu") if c["data-cu"].startswith("CU-")}
    if cus_ss != TODOS: errores.append(f"subsistemas: casos de mas {sorted(cus_ss - TODOS)} / de menos {sorted(TODOS - cus_ss)}")
    # mapa: los paquetes con su cantidad de casos
    cuenta = collections.Counter()
    for m in re.finditer(r'\*\*Código:\*\*\s*CU-\d+\s*\|[^\n]*\n(?:\*\*[^\n]*\n)*?\*\*Subsistema:\*\*\s*(SS-\d\d)', _cat[_a:_b]):
        cuenta[m.group(1)] += 1
    paq = {p["data-pq"]: int(p["data-n"]) for p in _elementos(mapa, "paquete")}
    if paq != dict(cuenta):
        errores.append(f"mapa: paquetes {paq} distintos del catalogo {dict(cuenta)}")
    import struct
    for f in sorted(glob.glob(D + "diagramas/uml/CU_SS-*.png")):
        with open(f, "rb") as fh:
            cab = fh.read(24)
        ancho, alto = struct.unpack(">II", cab[16:24])
        if 4096 in (ancho, alto):
            errores.append(f"{os.path.basename(f)} mide {ancho}x{alto}: tope de 4096 px")
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
    falt = [f"C-{n:02d}" for n in range(1, 21) if f"C-{n:02d}" not in fila_c]
    if falt: errores.append(f"Doc 0 §3: el hito de Construcción no refleja las iteraciones {falt}")
    cal = seccion(d0, orden[2], orden[3])
    if "### Cronograma (Diagrama de Gantt)" not in cal or "UML_Gantt." not in cal:
        errores.append("Doc 0 §4: falta el Cronograma (Diagrama de Gantt) como figura")
    gantt = open(D + "diagramas/uml/UML_Gantt.puml", encoding="utf-8").read()
    for cod in ["INI", "E01", "C01", "C02", "C03", "C04", "C05", "C06", "T01"] + [f"C{n:02d}" for n in range(7, 21)]:
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
    for cod, titulo in (("C-06", "## Iteración C-06"), ("C-07", "## Iteración C-07"), ("C-20", "## Iteración C-20"), ("T-01", "## Iteración T-01")):
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
    if not re.search(r'\*\*Figura \d+ — Diagrama de casos de uso, lámina', s3) or "CU_Sistema_Completo-Lamina-01_Cliente" not in s3:
        errores.append("Doc 1 §3: falta el Diagrama de Casos de Uso del Sistema como figura numerada")
    s4 = seccion(d1, "## 4. Subsistemas del Proyecto", "## 5. Objetivos de la Iteración")
    if not re.search(r'\*\*Figura \d+ — Diagrama de Subsistemas\*\*', s4) or "CU_Sistema_Subsistemas" not in s4:
        errores.append("Doc 1 §4: falta el Diagrama de Subsistemas como figura numerada")
    desc = set(re.findall(r'^\|\s*\*{0,2}(SS-\d\d)\*{0,2}\s*\|[^|]*\|\s*\S', s4, re.M))
    n_ss = len(set(re.findall(r'\*\*Subsistema:\*\*\s*(SS-\d\d)', _cat[_a:_b])))
    if len(desc) != n_ss: errores.append(f"Doc 1 §4: describe {len(desc)} subsistemas de {n_ss}")
    emb = set(re.findall(r'diagramas/uml/CU_(SS-\d\d)_[^)]*\.png\)', s4))
    if len(emb) != n_ss: errores.append(f"Doc 1 §4.3: embebe {len(emb)} diagramas por subsistema de {n_ss}")
    if "CU_Sistema_Diagrama-De-Contexto.png)" not in s3: errores.append("Doc 1 §3.1: falta el diagrama de contexto")

    # figuras: toda imagen existe y lleva su epígrafe numerado
    for doc in ("0-Plan_Del_Proyecto.md", "1-Requisitos.md", "3-Diseño.md"):
        ls = leer(doc)
        for i, l in enumerate(ls):
            m = re.match(r'^!\[[^\]]*\]\((\.\./diagramas/uml/[^)]+)\)\s*$', l)
            if not m: continue
            if not os.path.exists(DOC + m.group(1)): errores.append(f"{doc}: no existe {m.group(1)}")
            vec = [x for x in ls[max(0, i - 3):i + 4] if re.match(r'^\*\*Figura \d+ — ', x)]
            if not vec: errores.append(f"{doc}: la imagen {m.group(1)} no tiene epígrafe numerado")
    d3 = "\n".join(leer("3-Diseño.md"))
    for img in ("UML_Componentes", "UML_Despliegue", "UML_Estados_Pedido", "UML_Estados_Reclamo", "UML_Estados_Envase",
                "UML_Estados_Reserva", "UML_Estados_TareaFlota", "UML_Estados_OfertaDespacho",
                "UML_Estados_Empleado", "UML_Estados_Licencia", "UML_Estados_Jornada",
                "UML_Actividad_Despacho", "UML_Actividad_CicloPedido"):
        if f"diagramas/uml/{img}.png" not in d3: errores.append(f"Doc 3: falta el diagrama {img}")
    return errores

_errs = verificar_plantillas()
if _errs: FALLAS.append("secciones de la plantilla y figuras")
print(f"[{'OK' if not _errs else 'FALLA':5}] Secciones de la plantilla (Doc 0, 0.1, Doc 1) y figuras de los diagramas UML"
      + (f" | {_errs}" if _errs else ""))

# --- Operaciones del sistema: diagramas de secuencia, catálogo y contratos ---
# El catálogo (catedra/material-de-trabajo/operaciones-sistema.json) es la única fuente de las
# firmas. Los DSS tienen que dibujar al sistema como :Sistema, iniciar con un actor del
# catálogo de actores (ACT-01 a ACT-10), no tener mensajes del sistema a sí mismo, usar un
# mensaje asíncrono con nombre (notificar...) para lo que el sistema le manda a un actor
# sin que lo haya pedido, y llamar a cada operación con la misma firma que el catálogo.
# Cada operación que cambia estado tiene su contrato, con los campos de la plantilla de la
# cátedra en su orden.
import json
CAMPOS_CONTRATO = ["Nombre","Responsabilidades","Tipo","Referencias cruzadas","Notas",
                   "Excepciones","Salida","Precondiciones","Postcondiciones"]

PRE_MAL = re.compile(r'\b(ya valid[oó]|su firma es válida|son válid[oa]s|cumplen|suficiente|alcanzan|coincide|permitid[oa]|no supera|formato)\b', re.I)
POST_MAL = re.compile(r'\b(si falla|si la persistencia|se valida|el sistema (?:verifica|valida|comprueba)|no (?:cambió|cambia|varió|se modificó|se eliminó|se borró)|ningún [^.]*(?:cambió|se modificó|quedó negativo)|dejó de (?:aparecer|listarse|ser visible)|recibieron|S3|Firebase|Redis|HTTP)\b', re.I)

def verificar_operaciones():
    errores = []
    ruta = D + "catedra/material-de-trabajo/operaciones-sistema.json"
    if not os.path.exists(ruta):
        return ["falta catedra/material-de-trabajo/operaciones-sistema.json"]
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
        if f"title DSS — {cu} {nombres.get(cu, '?')}" not in t:
            errores.append(f"{base}: el título no es «DSS — {cu} {nombres.get(cu, '?')}»")
        if not re.search(r'^\s*participant\s+SIS\s+as\s+:Sistema\s*$', t, re.M):
            errores.append(f"{base}: el sistema no es la lifeline :Sistema")
        parts = {}
        for m in re.finditer(r'^\s*actor\s+(\w+)\s+as\s+(.+?)\s*$', t, re.M):
            mm = re.match(r'^(.+) \((ACT-(?:0[1-9]|10))\)$', m.group(2))
            if not mm or mm.group(2) not in actores:
                errores.append(f"{base}: el actor «{m.group(2)}» no lleva un código del catálogo (ACT-01 a ACT-10)")
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
        # Larman: la precondición es lo que se asume (lo que el sistema valida va como excepción)
        # y la postcondición describe sólo los cambios en el modelo conceptual, en pasado y sin
        # ramas de falla, ni efectos que no son del modelo (avisos, almacenamiento, visibilidad).
        pre = re.search(r'^\|\s*\*\*Precondiciones\*\*\s*\|\s*(.*?)\s*\|$', cuerpo, re.M)
        post = re.search(r'^\|\s*\*\*Postcondiciones\*\*\s*\|\s*(.*?)\s*\|$', cuerpo, re.M)
        for hallado in (PRE_MAL.findall(pre.group(1)) if pre else []):
            errores.append(f"contratos: {nom}: la precondición valida en vez de asumir ({hallado!r}); va como excepción")
        for hallado in (POST_MAL.findall(post.group(1)) if post else []):
            errores.append(f"contratos: {nom}: la postcondición no describe un cambio del modelo conceptual ({hallado!r})")
        m = re.search(r'^\|\s*\*\*Nombre\*\*\s*\|\s*`(.+?)`\s*\|', cuerpo, re.M)
        if m and m.group(1) != ops[nom]["firmaConTipos"]:
            errores.append(f"contratos: el nombre de {nom} no es la firma del catálogo ({ops[nom]['firmaConTipos']})")
    return errores

def verificar_tabla_operaciones_doc3():
    """La tabla de operaciones del Documento 3 (§4.24) la genera generar-operaciones.py: sus cifras son las del catálogo."""
    cat = json.load(open(D + "catedra/material-de-trabajo/operaciones-sistema.json", encoding="utf-8"))["operaciones"]
    d3 = "\n".join(leer("3-Diseño.md"))
    m = re.search(r'Son \*\*(\d+) operaciones\*\*\. \*\*(\d+)\*\* tienen su diagrama de interacción y\s+\*\*(\d+)\*\* tienen contrato', d3)
    if not m: return ["no está la tabla de operaciones del sistema (generar-operaciones.py)"]
    esperado = (len(cat), len(cat), sum(1 for o in cat if o["cambiaEstado"]))
    if tuple(map(int, m.groups())) != esperado:
        return [f"la tabla dice {m.groups()} y el catálogo {esperado}: correr generar-operaciones.py"]
    return []

_errs_op = verificar_operaciones() + verificar_tabla_operaciones_doc3()
if _errs_op: FALLAS.append("operaciones del sistema (DSS, catálogo y contratos)")
print(f"[{'OK' if not _errs_op else 'FALLA':5}] Operaciones del sistema: DSS con :Sistema, iniciador del catálogo y sin auto-mensajes; una firma por operación; contrato de cada una que cambia estado"
      + (f" | {len(_errs_op)} errores: {_errs_op[:6]}" if _errs_op else ""))

# --- DSD en estilo Larman (catedra/material-de-trabajo/GUIA-DSD-LARMAN.md) ---
# Un DSD ya rehecho tiene que cumplir las reglas de la guía. Las operaciones del catálogo que
# todavía no tienen su DSD se informan y no fallan el gate hasta que se cierra la reescritura:
# entonces se corre con DSD_ESTRICTO=1 (o se fija el valor por omisión acá).
sys.path.insert(0, D + "herramientas")
import dsd_larman
_estricto = os.environ.get("DSD_ESTRICTO", "1") == "1"  # estricto por omisión: todas las operaciones tienen su DSD
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

# --- Catálogo y calificación: sin CU repetidos y con cuentas que cierran ---
# Un CU duplicado en el catálogo o en las listas por calificación, o un total que no es la cantidad
# de casos únicos, hace fallar el gate (en Casos-de-Uso.md §3 y en el Documento 0 §8).
import re as _re
_err_cal = []
for _doc in ("Casos-de-Uso.md", "0-Plan_Del_Proyecto.md"):
    _t = open(ruta_doc(_doc), encoding="utf-8").read()
    _filas = _re.findall(r'^\| (CU-\d{3}) [^|]+\| SS-\d\d \|[^|]*\| (\w+) \|', _t, _re.M)
    _cods = [c for c, _ in _filas]
    _rep = sorted({c for c in _cods if _cods.count(c) > 1})
    if _rep: _err_cal.append(f"{_doc}: CU repetidos en el catálogo {_rep}")
    _tot = 0
    _en_listas = []
    for _m in _re.finditer(r'^\| \*\*(Crítico|Importante|Secundario|Menor)\*\* \| (\d+) \| ([^\n]*?) \|$', _t, _re.M):
        _l = _m.group(3).split(", ")
        _en_listas += _l
        _tot += len(_l)
        if len(set(_l)) != len(_l): _err_cal.append(f"{_doc}: CU repetidos en la lista {_m.group(1)}")
        if int(_m.group(2)) != len(_l): _err_cal.append(f"{_doc}: {_m.group(1)} dice {_m.group(2)} y lista {len(_l)}")
        _de_cat = {c for c, k in _filas if k == _m.group(1)}
        if _de_cat != set(_l): _err_cal.append(f"{_doc}: la lista {_m.group(1)} no es la del catálogo")
    _mt = _re.search(r'^\| \*\*Total\*\* \| \*\*(\d+)\*\* \| CU-001 a', _t, _re.M)
    if not _mt or int(_mt.group(1)) != len(set(_cods)) or _tot != len(set(_cods)):
        _err_cal.append(f"{_doc}: el total ({_mt.group(1) if _mt else '?'}) no es la cantidad de CU únicos ({len(set(_cods))})")
if _err_cal: FALLAS.append("Catálogo y calificación")
print(f"[{'OK' if not _err_cal else 'FALLA':5}] Catálogo y calificación: sin CU repetidos y con totales que cierran" + (f" | {_err_cal[:4]}" if _err_cal else ""))

# --- Cifras que los documentos repiten: tienen que ser las reales ---
# Cantidad de casos de uso, de diagramas de secuencia (DSS) y de interacción (DSD), de operaciones y
# de contratos: lo que dicen README, GUIA, Casos-de-Uso y los documentos 2 y 3 sale del contenido.
_err_cif = []
_casos_t = open(DOC + "Casos-de-Uso.md", encoding="utf-8").read()
_n_cu = len({c for c, _ in _re.findall(r'^\| (CU-\d{3}) [^|]+\| SS-\d\d \|[^|]*\| (\w+) \|', _casos_t, _re.M)})
_n_dss = len(_re.findall(r'title DSS — ', _casos_t))
_n_dsd = len(_re.findall(r'title DSD — ', _casos_t))
_ana = open(DOC + "2-Analisis.md", encoding="utf-8").read()
_n_contr = len(_re.findall(r'^#### [^\n]*Contrato: `', _ana, _re.M))
_n_ops = len(__import__("json").load(open(D + "catedra/material-de-trabajo/operaciones-sistema.json", encoding="utf-8"))["operaciones"])
_esperado = [
    ("README.md", r'los (\d+) casos de uso de alto nivel', _n_cu), ("README.md", r'los (\d+) diagramas de secuencia', _n_dss),
    ("README.md", r'tiene los \*\*(\d+) casos', _n_cu),
    ("GUIA-DEL-REPOSITORIO.md", r'LOS (\d+) CASOS', _n_cu), ("GUIA-DEL-REPOSITORIO.md", r'los (\d+) diagramas de secuencia', _n_dss),
    ("GUIA-DEL-REPOSITORIO.md", r'las (\d+) operaciones del sistema', _n_ops), ("GUIA-DEL-REPOSITORIO.md", r'los (\d+) contratos', _n_contr),
    ("AGENTS.md", r'reúne los (\d+) CU', _n_cu),
    ("Casos-de-Uso.md", r'Se incluyen (\d+) diagramas, uno por caso', _n_dss),
    ("Casos-de-Uso.md", r'Este documento reúne, para los \*\*(\d+) casos de uso', _n_cu),
    ("3-Diseño.md", r'Los (\d+) diagramas de interacción en la notación', _n_dsd),
    ("3-Diseño.md", r'a partir de los (\d+) diagramas de interacción', _n_dsd),
]
for _f, _pat, _val in _esperado:
    _tx = open(ruta_doc(_f), encoding="utf-8").read()
    for _m in _re.finditer(_pat, _tx):
        if int(_m.group(1)) != _val:
            _err_cif.append(f"{_f}: dice {_m.group(1)} y son {_val} ({_pat[:40]})")
if _err_cif: FALLAS.append("Cifras repetidas en los documentos")
print(f"[{'OK' if not _err_cif else 'FALLA':5}] Cifras repetidas en los documentos: {_n_cu} CU, {_n_dss} DSS, {_n_dsd} DSD, {_n_ops} operaciones, {_n_contr} contratos"
      + (f" | {_err_cif[:5]}" if _err_cif else ""))

# --- Cruce de los DSD contra el código (tablas de implementación y clases de diseño) ---
# Una tabla que cita un método o una función que ya no existe en `src/` es una afirmación falsa:
# `cruzar-dsd-clases.py` sale distinto de 0 si hay una.
import subprocess
_cruce = subprocess.run([sys.executable, D + "herramientas/cruzar-dsd-clases.py"],
                        capture_output=True, text=True)
_lineas_cruce = [l.strip() for l in _cruce.stdout.splitlines() if l.strip().startswith("✗")]
if _cruce.returncode: FALLAS.append("Cruce de los DSD contra el código")
print(f"[{'OK' if not _cruce.returncode else 'FALLA':5}] Cruce de los DSD contra el código (cruzar-dsd-clases.py)"
      + (f" | {len(_lineas_cruce)} diferencias: {_lineas_cruce[:4]}" if _cruce.returncode and _lineas_cruce
         else (f" | {_cruce.stdout.strip()[-200:] or _cruce.stderr.strip()[-200:]}" if _cruce.returncode else "")))

# --- Trazabilidad CU <-> IRQ y matriz de objetivos ---
# Cada IRQ lista los casos que lo citan y cada caso cita sus IRQ: las dos direcciones tienen que cerrar,
# y la fila de cada caso en la matriz del Documento 1 §9 es la de sus objetivos.
import importlib.util as _iu
_sp = _iu.spec_from_file_location("trazabilidad_cu_irq", D + "herramientas/trazabilidad-cu-irq.py")
_tz = _iu.module_from_spec(_sp); _sp.loader.exec_module(_tz)
_err_tz, _n_tz = _tz.verificar()
if _err_tz: FALLAS.append("Trazabilidad CU-IRQ")
print(f"[{'OK' if not _err_tz else 'FALLA':5}] Trazabilidad CU-IRQ-objetivos: {_n_tz} casos, requisitos y matriz en los dos sentidos"
      + (f" | {len(_err_tz)} errores: {_err_tz[:4]}" if _err_tz else ""))

# --- Figuras correlativas, índice de imágenes contra los archivos y nombres del catálogo ---
_err_x = []
for _f in ("0-Plan_Del_Proyecto.md", "0.1-Planificacion_Iteraciones.md", "1-Requisitos.md", "2-Analisis.md", "3-Diseño.md"):
    _t = open(ruta_doc(_f), encoding="utf-8").read()
    _fig = re.findall(r'^\*\*Figura (\S+) — ', _t, re.M)
    _esp = [str(i) for i in range(1, len(_fig) + 1)]
    if _fig != _esp:
        _mal = next((a for a, b in zip(_fig, _esp) if a != b), None)
        _err_x.append(f"{_f}: las figuras no son correlativas desde 1 (primera fuera de lugar: {_mal})")
    _ind = re.findall(r'^- Figura (\S+) — ', _t, re.M)
    if _ind and _ind != _esp:
        _err_x.append(f"{_f}: el índice de figuras no coincide con los epígrafes ({len(_ind)} contra {len(_esp)})")
_spi = _iu.spec_from_file_location("generar_indice_imagenes", D + "herramientas/generar-indice-imagenes.py")
_gi = _iu.module_from_spec(_spi); _spi.loader.exec_module(_gi)
_err_x += [f"INDICE-IMAGENES.md: {e}" for e in _gi.verificar_indice()]
# el nombre de cada caso de uso es el del catálogo en el alto nivel, el expandido y los diagramas
_cat_n = {m_.group(1): m_.group(2).strip() for m_ in re.finditer(r'^\| (CU-\d{3}) ([^|]+?) \| SS-\d\d \|', _cat, re.M)}
for _f in ("Casos-de-Uso.md", "0-Plan_Del_Proyecto.md", "1-Requisitos.md", "2-Analisis.md"):
    _t = open(ruta_doc(_f), encoding="utf-8").read()
    for _m in re.finditer(r'\*\*Código:\*\*\s*(CU-\d+) \| \*\*Caso de Uso:\*\* ([^\n]*?)\s*\n', _t):
        if _cat_n.get(_m.group(1)) != _m.group(2).strip():
            _err_x.append(f"{_f}: {_m.group(1)} se llama «{_m.group(2).strip()}» y el catálogo dice «{_cat_n.get(_m.group(1))}»")
    for _m in re.finditer(r'^#### [^\n]*?(CU-\d+) — ([^\n]*)$', _t, re.M):
        if _cat_n.get(_m.group(1)) != _m.group(2).strip():
            _err_x.append(f"{_f}: el expandido de {_m.group(1)} se llama «{_m.group(2).strip()}» y el catálogo dice «{_cat_n.get(_m.group(1))}»")
if _err_x: FALLAS.append("Figuras, índice de imágenes y nombres")
print(f"[{'OK' if not _err_x else 'FALLA':5}] Figuras correlativas, índice de imágenes contra los archivos y nombres de los casos = catálogo"
      + (f" | {len(_err_x)} errores: {_err_x[:5]}" if _err_x else ""))

# ---------- operaciones del sistema, DSS e imágenes ----------
_err_o = []
_ops_j = json.load(open(D + "catedra/material-de-trabajo/operaciones-sistema.json", encoding="utf-8"))["operaciones"]
# cada operación del sistema pertenece a un solo caso de uso
for _o in _ops_j:
    if len(_o["casosDeUso"]) != 1:
        _err_o.append(f"la operación {_o['nombre']} pertenece a {len(_o['casosDeUso'])} casos de uso: {_o['casosDeUso']}")
# un DSS no repite una operación: un bloque por operación, aunque la inicien varios actores
for _p in sorted(glob.glob(D + "diagramas/DSS_*.mmd")):
    _c = collections.Counter(re.findall(r'(\w+)->>\+?SIS: (\w+)\(', open(_p, encoding="utf-8").read()))
    for (_a_, _n), _k in _c.items():
        if _k > 1: _err_o.append(f"{os.path.basename(_p)}: la operación {_n} está dibujada {_k} veces para el mismo actor")
# toda imagen que cita un documento existe, y todo el índice de imágenes apunta a archivos reales
for _f in ("0-Plan_Del_Proyecto.md", "0.1-Planificacion_Iteraciones.md", "1-Requisitos.md", "2-Analisis.md", "3-Diseño.md",
           "Casos-de-Uso.md", "README.md", "GUIA-DEL-REPOSITORIO.md"):
    _t = re.sub(r'```.*?```', '', open(ruta_doc(_f), encoding="utf-8").read(), flags=re.S)
    for _m in re.finditer(r'!\[[^\]]*\]\(([^)\s]+)\)', _t):
        _r = _m.group(1)
        if not _r.startswith(("http", "data:")) and not os.path.exists(os.path.dirname(ruta_doc(_f)) + "/" + _r):
            _err_o.append(f"{_f}: la imagen {_r} no existe")
_ti = open(DOC + "INDICE-IMAGENES.md", encoding="utf-8").read()
for _r in sorted(set(re.findall(r'`((?:diagramas|modelos|catedra/entregables)/[^`\s]+\.(?:png|svg|drawio|mmd))`', _ti))):
    if not os.path.exists(D + _r):
        _err_o.append(f"INDICE-IMAGENES.md: {_r} no existe")
if _err_o: FALLAS.append("Operaciones, DSS e imágenes")
print(f"[{'OK' if not _err_o else 'FALLA':5}] Cada operación pertenece a un solo CU, ningún DSS repite una operación y toda imagen citada existe"
      + (f" | {len(_err_o)} errores: {_err_o[:6]}" if _err_o else ""))

# ---------- los cuatro artefactos de cada caso de uso, con su diagrama ----------
_err_4 = []
_docs4 = {k: open(ruta_doc(f), encoding="utf-8").read() for k, f in
          (("cua", "0-Plan_Del_Proyecto.md"), ("cue", "1-Requisitos.md"), ("dss", "2-Analisis.md"), ("dsd", "3-Diseño.md"), ("casos", "Casos-de-Uso.md"))}
_pat4 = {"cua": r'\*\*Código:\*\*\s*%s \|', "cue": r'^#{4,5} [^\n]*\b%s — ', "dss": r'^#{4,5} [^\n]*\bDSS — %s: ', "dsd": r'^#{4,5} [^\n]*\bDSD — %s: '}
_nombres4 = {m_.group(1): m_.group(2).strip() for m_ in re.finditer(r'^\| (CU-\d{3}) ([^|]+?) \| SS-\d\d \|', _cat, re.M)}
_mmd = os.listdir(D + "diagramas")
for _cu, _n in sorted(_nombres4.items()):
    for _k in ("cua", "cue"):
        if not re.search(_pat4[_k] % _cu, _docs4[_k], re.M):
            _err_4.append(f"{_cu}: falta el {_k.upper()} en su documento")
    for _k, _t4 in (("dss", r'title DSS — %s\b'), ("dsd", r'title DSD — [^\n]*(?<![\d-])%s(?![\d])')):
        for _doc in (_k, "casos"):
            if not re.search(_t4 % _cu, _docs4[_doc]):
                _err_4.append(f"{_cu}: no hay diagrama {_k.upper()} en {'Casos-de-Uso.md' if _doc == 'casos' else 'su documento'}")
    _dss_f = [x for x in _mmd if x.startswith(f"DSS_{_cu}_") and x.endswith(".mmd")]
    _dsd_f = [x for x in _mmd if x.endswith(".mmd") and x.startswith("DSD_") and re.search(r'(?<![\d-])%s(?![\d])' % _cu, x.split(".mmd")[0])]
    if not _dss_f: _err_4.append(f"{_cu}: no hay archivo del DSS")
    if not _dsd_f: _err_4.append(f"{_cu}: no hay archivo del DSD")
    for _x in _dss_f + _dsd_f:
        if not os.path.exists(D + "diagramas/png/" + _x[:-4] + ".png"):
            _err_4.append(f"{_x}: no está dibujado (png)")
if _err_4: FALLAS.append("Cuatro artefactos por caso de uso")
print(f"[{'OK' if not _err_4 else 'FALLA':5}] Cada CU del catálogo tiene CUA, CUE, DSS y DSD con su diagrama dibujado ({len(_nombres4)} casos)"
      + (f" | {len(_err_4)} errores: {_err_4[:6]}" if _err_4 else ""))

# ---------- los diagramas de los casos de uso se ven como imagen, con su PNG al día ----------
import imagenes_cu
_err_i = imagenes_cu.verificar()
if _err_i: FALLAS.append("Imágenes de los diagramas de los casos de uso")
print(f"[{'OK' if not _err_i else 'FALLA':5}] Cada CU tiene su DSS y su DSD como imagen en Casos-de-Uso.md y en su documento, con el Mermaid plegado, y cada PNG es el de su .mmd vigente"
      + (f" | {len(_err_i)} errores: {_err_i[:6]}" if _err_i else ""))

# ---------- secciones duplicadas, pies de figura con el nombre del catálogo y casos retirados ----------
_err_s = []
for _f in ("2-Analisis.md", "Casos-de-Uso.md"):
    _t = open(ruta_doc(_f), encoding="utf-8").read()
    _c = collections.Counter(re.findall(r'^#{4,5} [^\n]*\bDSS — (CU-\d+): ', _t, re.M))
    for _cu_, _n_ in _c.items():
        if _n_ > 1: _err_s.append(f"{_f}: {_cu_} tiene {_n_} secciones DSS")
    if "no tiene diagrama de secuencia propio" in _t:
        _err_s.append(f"{_f}: queda un caso incluido «sin diagrama de secuencia propio»")
for _f in ("2-Analisis.md", "3-Diseño.md"):
    _t = open(ruta_doc(_f), encoding="utf-8").read()
    for _m in re.finditer(r'^(?:\*\*|- )Figura \d+ — (?:DSS|DSD) (CU-\d+(?: / CU-\d+)*)(?::| ·)? ?([^\n]*?)(?:\*\*)?$', _t, re.M):
        _cus_ = _m.group(1).split(" / ")
        _nom_ = re.split(r' — | · ', _m.group(2))[0]
        if len(_cus_) > 1:
            _err_s.append(f"{_f}: un pie de figura nombra varios casos: {_m.group(1)}")
        elif _cat_n.get(_cus_[0]) != _nom_:
            _err_s.append(f"{_f}: el pie «{_cus_[0]}: {_nom_}» no usa el nombre del catálogo «{_cat_n.get(_cus_[0])}»")
from retirados import CODIGOS as _RET
for _f in ("0-Plan_Del_Proyecto.md", "0.1-Planificacion_Iteraciones.md", "1-Requisitos.md", "2-Analisis.md", "3-Diseño.md", "Casos-de-Uso.md", "README.md", "GUIA-DEL-REPOSITORIO.md"):
    _tf = open(ruta_doc(_f), encoding="utf-8").read()
    _en_retirados = False
    for _l_ in _tf.split("\n"):
        if _l_.startswith("#"): _en_retirados = _l_.strip().endswith("Casos de uso retirados") or "Resumen de Calificación" in _l_
        if _en_retirados or _l_.startswith("| **Total**"): continue
        if any(re.search(rf'{r_}\b', _l_) for r_ in _RET) and not re.search(r'retir|sin CU-021|^- Figura|^\| CU-\d+ \(retirado\)|^\| \d+ \| 2026-', _l_):
            _err_s.append(f"{_f}: menciona un caso retirado fuera de la tabla de retirados: {_l_[:70]}")
# una sola numeración de iteraciones: ningún I-1..I-14 como identificador (solo la columna «Paquete» de la tabla de correspondencia del Documento 0 §4 y las filas de las Listas de Cambios, que son historia)
_rx_i = re.compile(r'(?<![A-Za-z0-9-])I-(?:[1-9]|1[0-4])(?!\d)')
for _f in ("0-Plan_Del_Proyecto.md", "0.1-Planificacion_Iteraciones.md", "1-Requisitos.md", "2-Analisis.md", "3-Diseño.md", "Casos-de-Uso.md", "README.md", "GUIA-DEL-REPOSITORIO.md", "AGENTS.md", "INDICE-IMAGENES.md"):
    for _l_ in open(ruta_doc(_f), encoding="utf-8").read().split("\n"):
        if _rx_i.search(_l_) and not re.match(r'\| \d+ \| 2026-', _l_) and not (_f == "0-Plan_Del_Proyecto.md" and re.match(r'\| \*\*C-\d\d\*\* |El plan agrupa los casos en catorce paquetes', _l_)):
            _err_s.append(f"{_f}: usa la numeración I-n de iteraciones: {_l_[:70]}")
if _err_s: FALLAS.append("Secciones, pies de figura y retirados")
print(f"[{'OK' if not _err_s else 'FALLA':5}] Un solo DSS por CU, pies de figura con el nombre del catálogo y sin menciones de casos retirados ni numeración I-n"
      + (f" | {len(_err_s)} errores: {_err_s[:6]}" if _err_s else ""))

# ---------- actores: la misma tabla en el Documento 0, el Documento 1 y Casos-de-Uso.md; ACT-10 presente ----------
_err_act = []
def _tabla_actores(f, ini):
    _t = open(ruta_doc(f), encoding="utf-8").read()
    _a = _t.index(ini)
    _m = re.search(r'\| Código \| Actor \| Tipo \| Descripción \|\n\|[-| :]+\|\n((?:\| ACT-\d+ \|.*\n)+)', _t[_a:])
    return _m.group(1).strip() if _m else ""
_ta = {"Documento 0 §5": _tabla_actores("0-Plan_Del_Proyecto.md", "## 5. Actores del Sistema"),
       "Documento 1 §7.1": _tabla_actores("1-Requisitos.md", "### 7.1 Definición de Actores"),
       "Casos-de-Uso.md §1": _tabla_actores("Casos-de-Uso.md", "## 1. Actores del Sistema")}
for _k, _v in _ta.items():
    if not _v: _err_act.append(f"{_k}: no encuentro la tabla de actores")
if len(set(_ta.values())) != 1: _err_act.append("las tablas de actores del Documento 0, el Documento 1 y Casos-de-Uso.md no son idénticas")
for _k, _v in _ta.items():
    if _v and (len(re.findall(r'^\| ACT-\d+ ', _v, re.M)) != 10 or "ACT-10" not in _v):
        _err_act.append(f"{_k}: la tabla no tiene los diez actores (con ACT-10 Operador Técnico)")
for _f, _ini in (("0-Plan_Del_Proyecto.md", "## 6. Diagrama de Casos de Uso del Sistema"), ("1-Requisitos.md", "## 3. Diagrama de Casos de Uso del Sistema"),
                 ("Casos-de-Uso.md", "## 2. Diagrama de Casos de Uso del Sistema")):
    _t = open(ruta_doc(_f), encoding="utf-8").read()
    _a = _t.index(_ini)
    _i_sub = _t.find("CU_Sistema_Diagrama-De-Subsistemas.png", _a)
    _i_comp = _t.find("CU_Sistema_Diagrama-Completo.png", _a)
    _i_mapa = _t.find("CU_Sistema_Mapa.png", _a)
    if not (0 < _i_sub < _i_comp < _i_mapa):
        _err_act.append(f"{_f}: el diagrama por subsistemas tiene que ir primero, después el completo con sus láminas y al final el mapa de navegación")
if _err_act: FALLAS.append("Actores y figura principal del diagrama de casos de uso")
print(f"[{'OK' if not _err_act else 'FALLA':5}] Tablas de actores idénticas (10 actores) y diagrama por subsistemas como figura principal" + (f" | {_err_act}" if _err_act else ""))

# ---------- tabla de implementación, catálogo vs CUA, cifras derivadas, pasos del CUE y CU reales ----------
# La «Tabla de implementación por caso de uso» (Casos-de-Uso.md §8) es la fuente de lo técnico de cada caso; el
# Documento 3 §4.25 es su copia. Sus pasos existen en el CUE; el catálogo (§3) y el CUA dicen los mismos actores; las cifras
# de los textos (retirados, casos por actor) salen del catálogo y de retirados.py; los CU reales llevan el nombre del
# catálogo; ningún DSD queda suelto después de la Trazabilidad de Casos-de-Uso.md.
def verificar_tabla_implementacion():
    errores = []
    cas = open(DOC + "Casos-de-Uso.md", encoding="utf-8").read()
    dis = open(DOC + "3-Diseño.md", encoding="utf-8").read()
    plan = open(DOC + "0-Plan_Del_Proyecto.md", encoding="utf-8").read()
    req = open(DOC + "1-Requisitos.md", encoding="utf-8").read()
    i8 = cas.find("## 8. Tabla de implementación por caso de uso")
    if i8 < 0:
        return ["Casos-de-Uso.md: falta la «Tabla de implementación por caso de uso» (§8)"]
    t8 = cas[i8:]
    filas8 = {m.group(1): m.group(0) for m in re.finditer(r'^\| (CU-\d{3})(?: \(retirado\))? [^\n]*$', t8, re.M)}
    # --- B1: existe en el Documento 3 (§4.25), con los mismos renglones que Casos-de-Uso.md §8
    j = dis.find("### 4.25 Tabla de implementación por caso de uso")
    if j < 0:
        errores.append("3-Diseño.md: falta la «Tabla de implementación por caso de uso» (§4.25)")
    else:
        k = min(x for x in (dis.find("\n### ", j + 5), dis.find("\n## ", j + 5), dis.find("\n<!-- ", j + 5)) if x != -1)
        filas3 = {m.group(1): m.group(0) for m in re.finditer(r'^\| (CU-\d{3})(?: \(retirado\))? [^\n]*$', dis[j:k], re.M)}
        if filas3 != filas8:
            errores.append(f"3-Diseño.md §4.25 no es copia de Casos-de-Uso.md §8 ({len(filas3)} y {len(filas8)} renglones): correr generar-tabla-implementacion.py")
    catalogo = {m.group(1): set(re.findall(r'ACT-\d\d', m.group(2)))
                for m in re.finditer(r'^\| (CU-\d{3}) [^|]+\| SS-\d\d \| ([^|]*)\|', cas[cas.index("## 3. Cat"):cas.index("## 4. Casos")], re.M)}
    faltan = sorted(set(catalogo) - set(filas8))
    if faltan:
        errores.append(f"tabla de implementación: sin renglón {faltan[:6]}")
    # --- I5: los pasos que cita la tabla y los de Rendimiento existen en el CUE
    s5 = cas[cas.index("## 5. Casos de Uso Expandidos"):cas.index("## 6. Diagramas")]
    cue = {m.group(1): m.group(2) for m in re.finditer(r'^#### [^\n]*?(CU-\d+) — [^\n]*\n(.*?)(?=^#{1,4} |\Z)', s5, re.M | re.S)}
    for cu, cuerpo in cue.items():
        sec = re.search(r'\*\*Secuencia Normal\*\*(.*?)\*\*Postcondici', cuerpo, re.S)
        pasos = {int(x) for x in re.findall(r'^\| (\d+) \|', sec.group(1), re.M)} if sec else set()
        alt = re.search(r'\*\*Secuencia Alternativa[^\n]*\*\*(.*?)(?=\n\*\*Rendimiento|\Z)', cuerpo, re.S)
        if alt: pasos |= {int(x) for x in re.findall(r'^\| (\d+) \|', alt.group(1), re.M)}
        rend = re.search(r'\*\*Rendimiento\*\*\s*\n(.*?)(?=\n\| Campo|\Z)', cuerpo, re.S)
        for n in {int(x) for x in re.findall(r'^\| (\d+) \|', rend.group(1), re.M)} if rend else set():
            if n not in pasos: errores.append(f"{cu}: el Rendimiento cita el paso {n}, que el CUE no tiene")
        exc = re.search(r'\*\*Excepciones\*\*\s*\n(.*?)(?=\n\*\*|\n\| Campo|\Z)', cuerpo, re.S)
        if exc and re.search(r'^\| — \|', exc.group(1), re.M):
            errores.append(f"{cu}: tiene una excepción sin paso («—»)")
        fila = filas8.get(cu)
        if fila:
            celdas = fila.split(" | ")
            if len(celdas) == 5:
                for lin in celdas[3].split("<br>"):
                    if re.match(r'(Sin paso|Paso —)', lin):
                        errores.append(f"{cu}: la tabla de implementación tiene una respuesta sin paso")
                    m = re.match(r'Paso (\d+(?:, \d+)*):', lin)
                    if m:
                        for n in map(int, m.group(1).split(", ")):
                            if n not in pasos:
                                errores.append(f"{cu}: la tabla de implementación cita el paso {n}, que el CUE no tiene")
    # --- I3: el catálogo de cada documento dice los actores del CUA
    sys.path.insert(0, D + "herramientas")
    from actores_cu import SECUNDARIO
    for nombre, texto, ini, fin in (("Casos-de-Uso.md", cas, "## 3. Cat", "## 4. Casos"),
                                    ("Documento 0", plan, "## 8. Cat", "## 9. ")):
        a_ = texto.find(ini)
        if a_ < 0:
            continue
        b_ = texto.find(fin, a_ + 5)
        cat_ = {m.group(1): set(re.findall(r'ACT-\d\d', m.group(2)))
                for m in re.finditer(r'^\| (CU-\d{3}) [^|]+\| SS-\d\d \| ([^|]*)\|', texto[a_:b_ if b_ > 0 else len(texto)], re.M)}
        cua_ = {m.group(1): set(re.findall(r'ACT-\d\d', m.group(2)))
                for m in re.finditer(r'\*\*Código:\*\* (CU-\d+) \|[^\n]*\n\*\*Actor/es:\*\* ([^\n]*)', texto)}
        malos = []
        for cu, a in cat_.items():
            sec_ = {f"ACT-{k}" for k, lst in SECUNDARIO.items() if cu in lst}
            if cu in cua_ and (a - sec_) != (cua_[cu] - sec_):
                malos.append(f"{cu}: catálogo {sorted(a)} y CUA {sorted(cua_[cu])}")
        if malos:
            errores.append(f"{nombre}: el catálogo y el CUA no dicen los mismos actores en {len(malos)} casos, p. ej. {malos[:3]}")
    # --- I4: cifras derivadas de retirados.py y del catálogo
    from retirados import RETIRADOS
    n_ret, n_cat = len(RETIRADOS), len(catalogo)
    palabra = {9: "Nueve", 10: "Diez", 11: "Once", 12: "Doce"}.get(n_ret, str(n_ret))
    for nombre, texto in (("Casos-de-Uso.md", cas), ("0-Plan_Del_Proyecto.md", plan)):
        m = re.search(r'Los (\d+) casos de la tabla se retiraron', texto)
        if not m or int(m.group(1)) != n_ret:
            errores.append(f"{nombre}: dice {m.group(1) if m else '?'} casos retirados y retirados.py tiene {n_ret}")
        m = re.search(r'hay (\d+) números, (\d+) de casos del catálogo y (\d+) retirados', texto)
        if not m or tuple(map(int, m.groups())) != (n_cat + n_ret, n_cat, n_ret):
            errores.append(f"{nombre}: los recuentos de retirados dicen {m.groups() if m else '?'} y el catálogo {(n_cat + n_ret, n_cat, n_ret)}")
    if f"{palabra} casos fueron retirados del catálogo" not in req:
        errores.append(f"1-Requisitos.md: no dice «{palabra} casos fueron retirados del catálogo»")
    por_actor = {k: sum(1 for a in catalogo.values() if f"ACT-{k}" in a) for k in ("01", "02", "03", "05")}
    for nombre, texto in (("Casos-de-Uso.md", cas), ("0-Plan_Del_Proyecto.md", plan), ("1-Requisitos.md", req)):
        for k, n in por_actor.items():
            m = re.search(r'\| ACT-%s \| \*\*[^|\n]*\| [^|\n]*\| [^|\n]*?(?:Inicia|Participa en) (\d+) casos de uso' % k, texto)
            if not m or int(m.group(1)) != n:
                errores.append(f"{nombre}: la tabla de actores dice {m.group(1) if m else '?'} casos para ACT-{k} y el catálogo {n}")
    # --- I7: CU reales con el nombre del catálogo
    nombres = {m.group(1): m.group(2).strip() for m in re.finditer(r'^\| (CU-\d{3}) ([^|]+?) \| SS-\d\d \|', cas, re.M)}
    s3 = dis[dis.index("## 3. Casos de Uso Reales"):dis.index("## 4. Diagramas de Interacción")]
    for m in re.finditer(r'^### 3\.\d+ (CU-\d+)[^—\n]*— ([^\n]*)$', s3, re.M):
        if nombres.get(m.group(1)) != m.group(2):
            errores.append(f"Documento 3 §3: el encabezado de {m.group(1)} dice «{m.group(2)}» y el catálogo «{nombres.get(m.group(1))}»")
    for m in re.finditer(r'\| \*\*Código\*\* \| (CU-\d+) \|\n\| \*\*Caso de Uso\*\* \| ([^|\n]*?) \|', s3):
        if nombres.get(m.group(1)) != m.group(2):
            errores.append(f"Documento 3 §3: el campo «Caso de Uso» de {m.group(1)} dice «{m.group(2)}» y el catálogo «{nombres.get(m.group(1))}»")
    # --- M11: ningún DSD suelto después de la Trazabilidad y todos con el nombre del catálogo
    z = cas.index("\n## Trazabilidad")
    if re.search(r'^#{3,5} [^\n]*DSD — CU-', cas[z:cas.index("\n## 8. Tabla")], re.M):
        errores.append("Casos-de-Uso.md: hay diagramas DSD después de «Trazabilidad», fuera de su subsistema")
    for m in re.finditer(r'^#{3,5} (?:DSS|DSD) — (CU-\d+): ([^\n]*)$', cas, re.M):
        if nombres.get(m.group(1)) != m.group(2).strip():
            errores.append(f"Casos-de-Uso.md: el encabezado «{m.group(0)[:70]}» no usa el nombre del catálogo")
    return errores

_err_ti = verificar_tabla_implementacion()
if _err_ti: FALLAS.append("Tabla de implementación, catálogo, cifras y CU reales")
print(f"[{'OK' if not _err_ti else 'FALLA':5}] Tabla de implementación en Casos §8 y Documento 3 §4.25 (pasos que existen en el CUE), catálogo = CUA, cifras desde retirados.py y el catálogo, CU reales con el nombre del catálogo"
      + (f" | {len(_err_ti)} errores: {_err_ti[:6]}" if _err_ti else ""))

# ---------- verificadores de herramientas/: se corren y se exige que hayan leído algo ----------
def _correr(nombre, script, lee):
    r = subprocess.run([sys.executable, D + "herramientas/" + script], capture_output=True, text=True)
    salida = (r.stdout + r.stderr).strip()
    vacio = not re.search(lee, salida)
    if r.returncode or vacio:
        FALLAS.append(nombre)
    detalle = ""
    if r.returncode or vacio:
        detalle = " | " + (" ".join(salida.splitlines()[-6:]) if salida else "sin salida")[:600] + (" | leyó 0 elementos" if vacio else "")
    print(f"[{'OK' if not (r.returncode or vacio) else 'FALLA':5}] {nombre}" + detalle)

_correr("Cinco artefactos por caso de uso, diagramas por subsistema y estado uniforme (verificar-artefactos-cu.py)",
        "verificar-artefactos-cu.py", r"Casos de uso en el catálogo: [1-9]\d*")
_correr("Relaciones include/extend: fuente, diagramas, tabla §7.7 y CUE (verificar-relaciones-cu.py)",
        "verificar-relaciones-cu.py", r"«include»: [1-9]\d* en la fuente, [1-9]\d* dibujados, [1-9]\d* en la tabla")
_correr("Lenguaje esencial: ningún CUA ni CUE nombra rutas, códigos, clases ni infraestructura (verificar-lenguaje-esencial.py)",
        "verificar-lenguaje-esencial.py", r"Textos revisados: [1-9]\d*")

# ---------- tablas: cada fila tiene tantas celdas como su encabezado ----------
def _celdas(linea):
    """Celdas de una fila de tabla Markdown. Todo `|` corta una celda, también dentro de un code span
    (generar-sitio.py parte por `|` sin más): en el texto de una celda no puede haber ninguno."""
    l = linea.strip()
    return len(l.strip("|").split("|")) if l.startswith("|") else 0

def verificar_celdas_por_fila():
    """Una fila con una celda de más (un `|` suelto o un texto pegado después del cierre) deja vacío el campo
    en el sitio: se compara cada fila de las tablas de los CUE (Casos y Documento 1), de la tabla de
    implementación (Casos §8 y Documento 3 §4.25) y de los contratos (Documento 2) con su encabezado."""
    malas = []
    for f in ("Casos-de-Uso.md", "1-Requisitos.md", "2-Analisis.md", "3-Diseño.md"):
        ancho, previa = 0, ""
        for n, l in enumerate(open(DOC + f, encoding="utf-8").read().split("\n"), 1):
            if not l.startswith("|"):
                ancho, previa = 0, l
                continue
            if not previa.startswith("|"):
                ancho = _celdas(l)          # encabezado de una tabla nueva
            elif re.match(r"^\|[\s:|-]+\|$", l):
                pass
            elif ancho and _celdas(l) != ancho:
                malas.append(f"{f}:{n} ({_celdas(l)} celdas, la tabla tiene {ancho})")
            elif ancho and not l.rstrip().endswith("|"):
                malas.append(f"{f}:{n} (la fila no cierra con «|»)")
            previa = l
    ok = not malas
    if not ok: FALLAS.append("Tablas: celdas por fila")
    print(f"[{'OK' if ok else 'FALLA':5}] Tablas de los CUE, de la tabla de implementación y de los contratos: cada fila tiene las celdas de su encabezado"
          + ("" if ok else " | " + "; ".join(malas[:8]) + (f" … ({len(malas)})" if len(malas) > 8 else "")))
verificar_celdas_por_fila()

print()
if FALLAS:
    print(f"INCUMPLIMIENTOS: {len(FALLAS)} -> {FALLAS}"); sys.exit(1)
print("Todos los artefactos cumplen la plantilla de la cátedra."); sys.exit(0)
