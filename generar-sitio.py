#!/usr/bin/env python3
"""Genera el sitio de documentación: una pagina con los cuatro artefactos de cada caso
(alto nivel, expandido, secuencia del sistema, interaccion de diseño) y el documento
y seccion donde cada uno esta respaldado.

Uso:  python3 generar-sitio.py     ->  splg-documentacion.html
"""
import re, json, os, glob, base64, hashlib, sys, datetime
from paleta import css_subsistemas

# Los casos de uso que intervienen en cada modulo sin pertenecerle. Salen de las
# entradas y salidas de la especificacion del documento 3, seccion 6. La catedra
# revisa esta trazabilidad, y el catalogo por si solo no la tiene.
USA = {
 "M1": [("Lo dispara", ["CU-005"]),
        ("Se alimenta de", ["CU-058", "CU-035", "CU-109"]),
        ("Alternativa manual", ["CU-012"]),
        ("Desemboca en", ["CU-081", "CU-017", "CU-018"]),
        ("Comparte mecánica con", ["CU-149"])],
 "M2": [("Se alimenta de", ["CU-136", "CU-137", "CU-138", "CU-141", "CU-051", "CU-113"]),
        ("Consulta", ["CU-139"]),
        ("Desemboca en", ["CU-140"]),
        ("Condiciona", ["CU-013"]),
        ("Convive con", ["CU-142"])],
 "M3": [("Se alimenta de", ["CU-143", "CU-144", "CU-007", "CU-041"]),
        ("Respeta", ["CU-145"]),
        ("Se consulta por", ["CU-146"]),
        ("Desemboca en", ["CU-005"])],
 "M4": [("Se alimenta de", ["CU-011", "CU-045", "CU-057", "CU-051", "CU-113"]),
        ("Comparte mecánica con", ["CU-015", "CU-016"]),
        ("Devuelve a", ["CU-013"])],
 "M5": [("Se alimenta de", ["CU-067", "CU-068", "CU-070", "CU-071", "CU-069"]),
        ("Ofrece la devolución en", ["CU-081"]),
        ("Escala a", ["CU-011"])],
}


D = os.path.dirname(os.path.abspath(__file__)) + "/"
lin = open(D+"Casos-de-Uso.md", encoding="utf-8").read().split("\n")

def rango(ini, fin):
    return (next(i for i,x in enumerate(lin) if re.match(ini,x)),
            next(i for i,x in enumerate(lin) if re.match(fin,x)))

# ---------- casos de uso de alto nivel ----------
a,b = rango(r'^## 4\. ', r'^## 5\. ')
blk = "\n".join(lin[a:b]); cua = {}
for m in re.finditer(r'\*\*Código:\*\*\s*(CU-\d+)\s*\|\s*\*\*Caso de Uso:\*\*\s*(.+?)\s*\n(.*?)(?=\*\*Código:\*\*|\Z)', blk, re.S):
    cod, nom, resto = m.group(1), m.group(2).strip(), m.group(3)
    def campo(n):
        mm = re.search(rf'\*\*{n}:\*\*\s*(.*?)(?=\n\s*\*\*|\n\s*---|\Z)', resto, re.S)
        return re.sub(r'\s+',' ',mm.group(1)).strip() if mm else ""
    cua[cod] = {"nombre":nom, "actores":campo("Actor/es"), "subsistema":campo("Subsistema"),
                "calificacion":campo("Calificación"), "descripcion":campo("Descripción")}

# ---------- casos de uso expandidos ----------
a,b = rango(r'^## 5\. ', r'^## 6\. ')
sub = lin[a:b]
idx = [(i,m) for i,x in enumerate(sub) if (m:=re.match(r'^#{4}\s+(.*?)\s*(CU-\d+)\s*[—-]\s*(.+)$',x))]
cue = {}
for n,(i,m) in enumerate(idx):
    fin = idx[n+1][0] if n+1 < len(idx) else len(sub)
    cuerpo = "\n".join(sub[i+1:fin])
    def fila(nom):
        mm = re.search(rf'\|\s*\*\*{re.escape(nom)}\*\*\s*\|\s*(.*?)\s*\|\s*$', cuerpo, re.M)
        return mm.group(1).strip() if mm else ""
    def tabla(titulo):
        mm = re.search(rf'\*\*{titulo}\*\*\s*\n\n\|[^\n]*\|\s*\n\|[-\s|]+\|\s*\n((?:\|.*\|\s*\n)+)', cuerpo)
        if not mm: return []
        out = []
        for f in mm.group(1).strip().split("\n"):
            c = [x.strip() for x in f.strip().strip("|").split("|")]
            if len(c) < 2: continue
            if c[0] == "Campo" or set(c[0]) <= set("-: "): break
            out.append({"paso":c[0], "accion":c[1]})
        return out
    post = re.search(r'\*\*Postcondición:\*\*\s*(.+?)(?=\n\n|\Z)', cuerpo, re.S)
    cue[m.group(2)] = {"prioridad":m.group(1).strip(), "nombre":m.group(3).strip(),
      "objetivos":fila("Objetivos asociados"), "requisitos":fila("Requisitos asociados"),
      "descripcion":fila("Descripción"), "precondicion":fila("Precondición"),
      "estado":fila("Estado"), "secuencia":tabla("Secuencia Normal"),
      "postcondicion":re.sub(r'\s+',' ',post.group(1)).strip() if post else "",
      "excepciones":tabla("Excepciones"), "rendimiento":fila("Rendimiento"),
      "frecuencia":fila("Frecuencia"), "estabilidad":fila("Estabilidad"),
      "comentarios":fila("Comentarios"), "especificacion":fila("Especificación expandida")}

# ---------- diagramas ----------
def cargar(prefijo):
    o = {}
    for f in glob.glob(D+f"diagramas/{prefijo}_CU-*.mmd"):
        base = os.path.basename(f)
        m = re.match(rf'{prefijo}_((?:CU-\d+_)+)(.+)\.mmd$', base)
        if not m: continue
        codes = re.findall(r'CU-\d+', m.group(1))
        src = re.sub(r'^```mermaid\s*|\s*```$', '', open(f,encoding="utf-8").read().strip()).strip()
        titulo = m.group(2).replace("-", " ")
        if prefijo == "DSD":
            # estilo Larman: el diagrama es una operación del sistema y su título es la firma
            fm = re.search(r'^\s*\w+\s*-{1,2}>>\+?\s*\w+\s*:\s*(\w+\(.*\))\s*$', src, re.M)
            if fm and re.search(r'^\s*(?:create\s+)?participant\s+\w+\s+as\s+\w*:', src, re.M):
                titulo = "Operación: " + fm.group(1)
        if prefijo == "DSS":
            # el nombre del caso, con sus tildes, está en el título del propio diagrama
            tm = re.search(r'^\s*title DSS — CU-\d+(?:\s*/\s*CU-\d+)*:?\s+(.+)$', src, re.M)
            if tm: titulo = tm.group(1).strip()
        for c in codes:
            o.setdefault(c, []).append({"titulo":titulo, "src":src,
                                        "comparte": codes if len(codes) > 1 else []})
    return o
dss, dsd = cargar("DSS"), cargar("DSD")

# ---------- subsistemas y diagramas UML ----------
d1 = open(D+"1-Requisitos.md", encoding="utf-8").read()
ss = {}
for m in re.finditer(r'^\|\s*\*?\*?(SS-\d+)\*?\*?\s*\|\s*\*?\*?([^|*]+?)\*?\*?\s*\|\s*([^|]+)\|', d1, re.M):
    ss.setdefault(m.group(1), {"nombre":m.group(2).strip(), "descripcion":m.group(3).strip()})
def b64(p):
    return "data:image/png;base64," + base64.b64encode(open(p,"rb").read()).decode() if os.path.exists(p) else ""
def imagen(p):
    """El .svg del mismo diagrama, si existe: pesa una fraccion del png y no se
    pixela al ampliarlo. El diagrama completo son 4 MB en png contra 200 KB en svg."""
    s = p if p.endswith(".svg") else re.sub(r'\.png$', '.svg', p)
    if os.path.exists(s):
        return "data:image/svg+xml;base64," + base64.b64encode(open(s,"rb").read()).decode()
    return b64(p)
for c,v in ss.items():
    g = glob.glob(D+f"diagramas/uml/CU_{c}_*.png")
    if g: v["uml"] = imagen(g[0])

# diagramas de nivel sistema. Antes esto era un glob de CU_Sistema_*.png del que se
# tomaba el primero; al sumar el de actores y el completo, cual salia dependia del
# orden del directorio.
UMLSIS = {
  "contexto": ("CU_Sistema_Diagrama-De-Contexto",
               "Diagrama de contexto",
               "Actores contra subsistemas: define el límite del sistema"),
  "completo": ("CU_Sistema_Diagrama-Completo",
               "Diagrama completo de casos de uso",
               "Los %d casos de uso, uno por uno, dentro de su paquete, con los actores afuera del límite"),
  "mapa": ("CU_Sistema_Mapa",
               "Mapa del sistema",
               "Una página: los 18 paquetes con su cantidad de casos y qué actor participa en cada uno"),
  "subsistemas": ("CU_Sistema_Subsistemas",
               "Subsistemas del proyecto",
               "Los 18 subsistemas, su agrupamiento y de quién depende cada uno"),
  "despliegue": ("SPLG_Arquitectura",
               "Despliegue y entornos",
               "Dónde corre cada pieza y cómo llega el código a producción"),
  "actores":  ("CU_Sistema_Actores",
               "Actores del sistema",
               "Los actores, el canal por el que operan y los sistemas externos"),
}
umlsis = {}
for _k,(_f,_n,_d) in UMLSIS.items():
    _p = D+"diagramas/uml/"+_f+(".svg" if os.path.exists(D+"diagramas/uml/"+_f+".svg")
                                and not os.path.exists(D+"diagramas/uml/"+_f+".png") else ".png")
    if os.path.exists(_p): umlsis[_k] = {"img":imagen(_p), "nombre":_n, "descripcion":_d}
contexto = umlsis.get("contexto",{}).get("img","")

# ---------- markdown -> html, para los bloques que se muestran tal cual ----------
import html as _html

# Los codigos que aparecen en el texto se marcan con su color: el subsistema con
# el mismo tinte que su caja en los diagramas, el caso de uso y el actor con su
# propia marca. Con 149 casos y 18 subsistemas, encontrar uno en una tabla de
# texto plano era leer renglon por renglon.
def marcar(s):
    s = re.sub(r'\b(SS-\d\d)\b', r'<span class="marca-ss" data-ss="\1">\1</span>', s)
    s = re.sub(r'\b(CU-\d{3})\b', r'<span class="marca-cu">\1</span>', s)
    s = re.sub(r'\b(ACT-0\d)\b', r'<span class="marca-act" data-act="\1">\1</span>', s)
    return s

def md2html(md):
    """Convierte un bloque de markdown a HTML y separa los diagramas mermaid."""
    diagramas = []
    def inline(s):
        s = _html.escape(s)
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
        return marcar(s)
    out, i, L = [], 0, md.split("\n")
    while i < len(L):
        l = L[i]
        if l.strip().startswith("```"):
            leng = l.strip().strip("`"); i += 1; buf = []
            while i < len(L) and not L[i].strip().startswith("```"): buf.append(L[i]); i += 1
            i += 1
            if leng == "mermaid":
                out.append('<div class="diagram" data-mer="%d"></div>' % len(diagramas))
                diagramas.append("\n".join(buf))
            else:
                out.append("<pre>" + _html.escape("\n".join(buf)) + "</pre>")
            continue
        m = re.match(r'^!\[(.*?)\]\(([^)]+)\)\s*$', l.strip())
        if m:
            # las figuras del markdown se embeben; sin esto salian como texto
            src = imagen(D + m.group(2))
            out.append('<div class="figura"><img class="umlimg" alt="%s" src="%s">'
                       '<span class="ampliar">CLIC PARA AMPLIAR</span></div>'
                       % (_html.escape(m.group(1)), src) if src else "")
            i += 1; continue
        if re.match(r'^\|', l) and i+1 < len(L) and re.match(r'^\|[\s:\-|]+\|\s*$', L[i+1]):
            cab = [c.strip() for c in l.strip().strip("|").split("|")]
            i += 2; filas = []
            while i < len(L) and L[i].strip().startswith("|"):
                filas.append([c.strip() for c in L[i].strip().strip("|").split("|")]); i += 1
            th = "".join("<th>%s</th>" % inline(c) for c in cab)
            tb = "".join("<tr>" + "".join("<td>%s</td>" % inline(c) for c in f) + "</tr>" for f in filas)
            out.append('<div class="scroller"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, tb))
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', l)
        if m:
            out.append('<h4 class="sub">%s</h4>' % inline(m.group(2))); i += 1; continue
        if re.match(r'^---+\s*$', l): i += 1; continue
        if l.strip().startswith(">"):
            buf = []
            while i < len(L) and L[i].strip().startswith(">"):
                buf.append(L[i].strip().lstrip(">").strip()); i += 1
            out.append('<div class="note">' + inline(" ".join(buf)) + "</div>"); continue
        if re.match(r'^\s*[-*]\s+', l) or re.match(r'^\s*\d+\.\s+', l):
            tag = "ol" if re.match(r'^\s*\d+\.\s+', l) else "ul"; buf = []
            while i < len(L) and (re.match(r'^\s*[-*]\s+', L[i]) or re.match(r'^\s*\d+\.\s+', L[i])):
                buf.append(re.sub(r'^\s*(?:[-*]|\d+\.)\s+', '', L[i])); i += 1
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in buf), tag)); continue
        if l.strip():
            buf = []
            while i < len(L) and L[i].strip() and not re.match(r'^(#{1,6}\s|\||>|```|---+\s*$|\s*[-*]\s|\s*\d+\.\s)', L[i]):
                buf.append(L[i].rstrip()); i += 1
            if not buf: buf = [L[i].rstrip()]; i += 1
            out.append("<p>" + inline(" ".join(buf)) + "</p>"); continue
        i += 1
    return {"html": "".join(out), "mermaid": diagramas}

# ---------- casos de uso reales (documento 3, seccion 3) ----------
_l3 = open(D+"3-Diseño.md", encoding="utf-8").read().split("\n")
_s = next(i for i,x in enumerate(_l3) if re.match(r'^## 3\. Casos de Uso Reales', x))
_e = next(i for i,x in enumerate(_l3) if re.match(r'^## 4\. ', x))
_ix = [(i,m) for i in range(_s,_e) if (m:=re.match(r'^### 3\.(\d+) (CU-\d+)', _l3[i]))]
cur = {}
for _n,(_i,_m) in enumerate(_ix):
    _f = _ix[_n+1][0] if _n+1 < len(_ix) else _e
    cur[_m.group(2)] = dict(md2html("\n".join(_l3[_i+1:_f])), sec="§3."+_m.group(1))

# ---------- modulos inteligentes (documento 3, seccion 6) ----------
_s6 = next(i for i,x in enumerate(_l3) if re.match(r'^## 6\. Módulos', x))
_e6 = next(i for i,x in enumerate(_l3) if re.match(r'^## 7\. ', x))
_ix6 = [(i,m) for i in range(_s6,_e6) if (m:=re.match(r'^### 6\.(\d+) Módulo (M\d) — (.+)$', _l3[i]))]
mods = {}
for _n,(_i,_m) in enumerate(_ix6):
    _f = _ix6[_n+1][0] if _n+1 < len(_ix6) else _e6
    mods[_m.group(2)] = dict(md2html("\n".join(_l3[_i+1:_f])),
                             nombre=_m.group(3).strip(), sec="§6."+_m.group(1),
                             usa=USA.get(_m.group(2), []))



# ---------- vista de sistema: actores, contexto, subsistemas, catalogo ----------
def _seccion(archivo, ini, fin):
    ls = open(D+archivo, encoding="utf-8").read().split("\n")
    a = next(i for i,x in enumerate(ls) if re.match(ini, x))
    b = next(i for i,x in enumerate(ls) if re.match(fin, x))
    return "\n".join(ls[a+1:b]).strip()

sistema = {
  "actores":  dict(md2html(_seccion("Casos-de-Uso.md", r'^## 1\. Actores', r'^## 2\. ')),
                   titulo="Actores del sistema", sec="Doc 1 · §7.1"),
  "contexto": dict(md2html(_seccion("Casos-de-Uso.md", r'^## 2\. Diagrama', r'^## 3\. ')),
                   titulo="Diagrama de casos de uso del sistema", sec="Doc 0 · §6 · Doc 1 · §3"),
  "catalogo": dict(md2html(_seccion("Casos-de-Uso.md", r'^## 3\. Catálogo', r'^## 4\. ')),
                   titulo="Catálogo y calificación de los casos", sec="Doc 0 · §8"),
}
# el diagrama de subsistemas vive en el documento 1
_d1 = open(D+"1-Requisitos.md", encoding="utf-8").read().split("\n")
_a = next(i for i,x in enumerate(_d1) if x.startswith("## 4. Subsistemas"))
_b = next(i for i,x in enumerate(_d1) if x.startswith("## 5. "))
sistema["subsistemas"] = dict(md2html("\n".join(_d1[_a+1:_b])),
                              titulo="Subsistemas del proyecto", sec="Doc 1 · §4")

# ---------- respaldo documental ----------
proc = {}
def add(cod, doc, sec, que):
    e = {"doc":doc, "sec":sec, "que":que}
    if e not in proc.setdefault(cod, []): proc[cod].append(e)

d0 = open(D+"0-Plan_Del_Proyecto.md", encoding="utf-8").read()
for c in cua: add(c, "0 — Plan del Proyecto", "§7 Casos de Uso de Alto Nivel", "Descripción de alto nivel")
for m in re.finditer(r'^\|\s*(CU-\d+)[^|]*\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|', d0, re.M):
    add(m.group(1), "0 — Plan del Proyecto", "§8 Calificación de los Casos de Uso", f"Calificado como {m.group(2).strip()}")

d01 = open(D+"0.1-Planificacion_Iteraciones.md", encoding="utf-8").read()
it = None
for linea in d01.split("\n"):
    mm = re.match(r'^## (Fase de Inicio|Iteración [\w-]+.*)$', linea)
    if mm: it = mm.group(1).strip()
    for c in set(re.findall(r'CU-\d+', linea)):
        if it: add(c, "0.1 — Planificación de Iteraciones", it, "Planificado en esta iteración")

for c,v in cue.items():
    add(c, "1 — Requisitos", "§7 Requisitos Funcionales", "Caso de uso expandido")
    if v["objetivos"]: add(c, "1 — Requisitos", "§2 Objetivos del Sistema", f"Realiza {v['objetivos']}")
    if v["requisitos"]: add(c, "1 — Requisitos", "§6 Requisitos de Información", f"Usa {v['requisitos']}")
    add(c, "1 — Requisitos", "§9 Matriz de Rastreabilidad", "Fila de la matriz")

for c in dss: add(c, "2 — Análisis", "§2.1 Diagramas de Secuencia del Sistema", "Diagrama de secuencia")
d2 = open(D+"2-Analisis.md", encoding="utf-8").read()
for m in re.finditer(r'Contrato: `(\w+)\(', d2):
    ref = re.search(r'\*\*Referencias cruzadas\*\*\s*\|\s*([^|]+)\|', d2[m.start():m.start()+2000])
    if ref:
        for c in re.findall(r'CU-\d+', ref.group(1)):
            add(c, "2 — Análisis", "§2.2 Contratos de Operaciones", f"Contrato `{m.group(1)}()`")

d3 = open(D+"3-Diseño.md", encoding="utf-8").read()
for m in re.finditer(r'^### 3\.(\d+) (CU-\d+)', d3, re.M):
    add(m.group(2), "3 — Diseño", f"§3.{m.group(1)} Casos de Uso Reales", "Caso de uso real, con pantalla")
for c in dsd: add(c, "3 — Diseño", "§4 Diagramas de Interacción", "Diagrama de interacción de diseño")

MOD = {"M1":["CU-013","CU-014","CU-015","CU-016"], "M2":["CU-105"], "M3":["CU-106"],
       "M4":["CU-107"], "M5":["CU-108"]}
NOM = {"M1":"Negociación secuencial de asignación", "M2":"Mantenimiento predictivo de flota",
       "M3":"Anticipación de recompra", "M4":"Agrupación por recorrido",
       "M5":"Recuperación de envases"}
modulo = {}
for mo,cs in MOD.items():
    for c in cs:
        modulo[c] = {"codigo":mo, "nombre":NOM[mo]}
        add(c, "2 — Análisis", "§3 Módulos Inteligentes", f"Proceso automatizado {mo}")
        add(c, "3 — Diseño", "§6 Módulos Inteligentes", f"Especificación de {mo}")

# ---------- armado ----------
datos = {"cu":{}, "subsistemas":ss, "contexto":contexto, "umlsis":umlsis,
         "modulos":mods, "sistema":sistema}
for c in sorted(set(cua) | set(cue)):
    datos["cu"][c] = {"cua":cua.get(c,{}), "cue":cue.get(c,{}), "dss":dss.get(c,[]),
                      "dsd":dsd.get(c,[]), "respaldo":proc.get(c,[]), "modulo":modulo.get(c),
                      "cur":cur.get(c)}

if "completo" in umlsis:
    umlsis["completo"]["descripcion"] = umlsis["completo"]["descripcion"] % len(datos["cu"])

# un caso incluido no lo inicia ningún actor: su operación forma parte del diagrama del caso base
incluidos = {c for c,v in cua.items() if "caso incluido" in v["actores"].lower() or "ninguno directo" in v["actores"].lower()}
faltan = {k:[a for a in ("cua","cue","dss","dsd") if not v[a] and not (a == "dss" and k in incluidos)] for k,v in datos["cu"].items()}
faltan = {k:v for k,v in faltan.items() if v}
if faltan:
    print("ATENCION, casos con artefactos faltantes:", faltan, file=sys.stderr)

# ---------- version de los archivos compartidos ----------
# El visor vive en visor.js y visor.css. Sin una marca en el enlace, el
# navegador se queda con la copia vieja despues de publicar y la pagina queda a
# medias. La marca sale del contenido: cambia sola cuando el archivo cambia.
def marca_de(archivo):
    return hashlib.sha1(open(D + archivo, "rb").read()).hexdigest()[:8]

# ---------- las paginas hermanas, embebidas ----------
# Ramas, versionado y agentes son secciones del mismo sitio, no destinos
# aparte: el menu las muestra en la misma vista. Se toma el cuerpo de cada
# archivo —de la introduccion hasta el pie— y se guarda con los datos, asi la
# pagina sigue existiendo por separado para enlazarla directo.
def cuerpo_de(archivo):
    txt = open(D + archivo, encoding="utf-8").read()
    desde = txt.index('<div class="intro">')
    hasta = txt.rindex('<div class="pie">')
    cuerpo = txt[desde:hasta].strip()
    # La pagina de asistentes define sus iconos en un <svg> con <defs> antes del
    # contenido: sin el, los <use> de la version embebida no dibujan nada.
    if '<svg class="sprite"' in txt:
        i = txt.index('<svg class="sprite"')
        cuerpo = txt[i:txt.index("</svg>", i) + 6] + "\n" + cuerpo
    return cuerpo

# La arquitectura y el despliegue vivían sólo en el documento de Diseño: el sitio no
# mostraba la sección 2 en ningún lado, así que el diagrama de entornos y los criterios
# de la API no se veían. Entra como sección propia del menú.
_arq = _seccion("3-Diseño.md", r'^## 2\. Arquitectura', r'^## 3\. ')
_arq_html = md2html(_arq)["html"]

# ---------- los archivos para Lucidchart ----------
# El modelo conceptual, los dos diagramas de clases y el modelo de datos se
# trabajan en Lucidchart. Los archivos viven en lucidchart/ y se generan con
# generar-lucidchart.py; acá se muestran dibujados y se dejan para descargar,
# para no tener que ir al repositorio a buscarlos.
sys.path.insert(0, D)
from modelo_conceptual import VISTAS as _vistas_mc

def _lucid():
    fuentes = [
      ("Modelo conceptual", "SPLG-modelo-conceptual.xml",
       "diagramas/lucidchart/SPLG-modelo-conceptual.mmd",
       "Los conceptos del dominio con sus asociaciones y multiplicidades. "
       "Es el modelo de análisis: sin métodos, sin claves foráneas y sin navegabilidad."),
      ("Diagrama de clases de diseño — dominio", "SPLG-diagrama-de-clases-dominio.xml",
       "diagramas/lucidchart/SPLG-clases-diseno-dominio.mmd",
       "Las clases del modelo conceptual con sus atributos tipados y las operaciones que reciben "
       "en los diagramas de interacción, con la navegabilidad que esos mensajes piden. Se deriva "
       "de los DSD: no se escribe a mano."),
    ]
    # Las clases de servicios, casos de uso, puertos y controladores no entran en un
    # solo diagrama (126 clases): generar-clases-diseno.py las parte por módulo del
    # backend. Se agregan todas acá, en orden alfabético del módulo.
    for ruta_mmd in sorted(glob.glob(D + "diagramas/lucidchart/clases/SPLG-clases-*.mmd")):
        modulo = re.match(r'SPLG-clases-(.+)\.mmd$', os.path.basename(ruta_mmd)).group(1)
        fuentes.append((
          f"Diagrama de clases — servicios · módulo {modulo}",
          f"SPLG-diagrama-de-clases-{modulo}.xml",
          f"diagramas/lucidchart/clases/SPLG-clases-{modulo}.mmd",
          f"Vista `{modulo}` del diagrama de clases de diseño: controladores, fabricaciones "
          f"puras, puertos y colecciones con las operaciones que reciben en los DSD."))
    mer, secc = [], []
    for titulo, xml, fuente, desc in fuentes:
        ruta = D + fuente
        if not os.path.exists(ruta): continue
        mer.append(open(ruta, encoding="utf-8").read().strip())
        xml_ruta = (D + "lucidchart/clases/" + xml if "/clases/" in fuente
                   else D + "lucidchart/" + xml)
        if not os.path.exists(xml_ruta): continue
        b64 = base64.b64encode(open(xml_ruta, "rb").read()).decode()
        cuerpo = f'<div class="diagram" data-mer="{len(mer)-1}"></div>'
        if "clases-diseno-dominio" in fuente or re.search(r'lucidchart/clases/SPLG-clases-', fuente):
            # el diagrama de clases de diseño se dibuja con PlantUML (estereotipos, interfaces,
            # navegabilidad, realización): se muestran sus imágenes y no el Mermaid, que sólo es
            # la fuente del draw.io
            mer.pop()
            cuerpo = ""
            if "clases-diseno-dominio" in fuente:
                nombres_img = ["DC_General"] + sorted(
                    os.path.basename(f)[:-5] for f in glob.glob(D + "diagramas/clases-diseno/DC_*.puml")
                    if not os.path.basename(f).startswith(("DC_Mod_", "DC_General", "DC_Paquetes")))
            else:
                nombres_img = ["DC_Mod_" + re.search(r'SPLG-clases-(.+)\.mmd$', fuente).group(1)]
            for img in nombres_img:
                for ext in (".svg", ".png"):
                    ruta_img = D + "diagramas/clases-diseno/" + img + ext
                    if os.path.exists(ruta_img):
                        cuerpo += ('<div class="figura"><img class="umlimg" alt="Diagrama de clases de diseño: '
                                   f'{img}" src="{imagen(ruta_img)}"></div>')
                        break
        if xml == "SPLG-modelo-conceptual.xml":
            # el modelo conceptual se dibuja con PlantUML (dirección de lectura, clase de
            # asociación y restricciones de generalización): se muestran sus imágenes y no
            # el Mermaid, que es sólo la fuente del draw.io
            mer.pop()
            cuerpo = ""
            for img in ["MC_General"] + [v[1] for v in _vistas_mc]:
                for ext in (".svg", ".png"):
                    ruta_img = D + "diagramas/modelo-conceptual/" + img + ext
                    if os.path.exists(ruta_img):
                        cuerpo += ('<div class="figura"><img class="umlimg" alt="Modelo conceptual: '
                                   f'{img}" src="{imagen(ruta_img)}"></div>')
                        break
        secc.append(
          f'<h2>{titulo}</h2><p>{desc}</p>'
          f'{cuerpo}'
          f'<p class="bajar"><a download="{xml}" href="data:application/xml;base64,{b64}">'
          f'DESCARGAR {xml}</a> <span class="comollega">Lucidchart · Archivo · Importar · Draw.io</span></p>')

    sql = D + "lucidchart/SPLG-diagrama-de-base-de-datos.sql"
    if os.path.exists(sql):
        crudo = open(sql, encoding="utf-8").read()
        b64 = base64.b64encode(crudo.encode()).decode()
        img = ""
        for ruta_img in sorted(glob.glob(D + "diagramas/base-de-datos/fisico/SPLG-fisico-*.svg")):
            img += (f'<div class="figura"><img class="umlimg" alt="Modelo físico: '
                    f'{os.path.basename(ruta_img)[12:-4]}" src="{imagen(ruta_img)}"></div>')
        secc.append(
          f'<h2>Diagrama de base de datos</h2>'
          f'<p>Las {crudo.count("CREATE TABLE")} tablas con sus columnas y sus claves foráneas. '
          f'Entra por otra puerta que los anteriores: no es un diagrama sino el esquema, '
          f'y Lucidchart lo arma solo a partir del SQL.</p>{img}'
          f'<p class="bajar"><a download="SPLG-diagrama-de-base-de-datos.sql" '
          f'href="data:text/plain;base64,{b64}">DESCARGAR SPLG-diagrama-de-base-de-datos.sql</a> '
          f'<span class="comollega">Lucidchart · Importar datos · ERD · PostgreSQL</span></p>')

    intro = ('<div class="intro"><h1>Modelos para Lucidchart</h1>'
             '<p>Los cuatro diagramas que se trabajan en Lucidchart, dibujados acá y '
             'listos para bajar. Los tres primeros son archivos de draw.io, que es uno de '
             'los formatos que Lucidchart importa de fábrica; el cuarto es el esquema de '
             'la base. Se generan con <code>generar-lucidchart.py</code>.</p></div>')
    return {"titulo": "Modelos para Lucidchart", "html": intro + "".join(secc), "mermaid": mer}

datos["paginas"] = {
    "modelos": _lucid(),
    "arquitectura": {"titulo": "Arquitectura y despliegue",
                     "html": '<div class="intro"><h1>Arquitectura y despliegue</h1>'
                             '<p>Cómo está armado el sistema, dónde corre cada pieza y con qué '
                             'criterios está diseñada su interfaz HTTP. Documento 3 · §2.</p></div>'
                             + _arq_html},
    "ramas":      {"titulo": "Ramas y commits",     "html": cuerpo_de("branching.html")},
    "versionado": {"titulo": "Versionado automatico", "html": cuerpo_de("versionado.html")},
}

marcas = {a: marca_de(a) for a in ("visor.js", "visor.css")}

payload = json.dumps(datos, ensure_ascii=False, separators=(",",":")).replace("</", "<\\/")

# Los numeros que la pagina dice de si misma salen de los datos, no escritos a
# mano: el pie decia 221 diagramas de mermaid cuando ya eran 223.
n_mermaid = sum(len(v["dss"]) + len(v["dsd"]) +
                len((v["cur"] or {}).get("mermaid", [])) for v in datos["cu"].values())
n_mermaid += sum(len(m.get("mermaid", [])) for m in mods.values())
n_uml = sum(1 for v in ss.values() if "uml" in v) + len(umlsis)

version = ""
try:
    version = open(D+"VERSION", encoding="utf-8").read().strip()
except OSError:
    version = ""
generado = datetime.date.today().strftime("%d/%m/%Y")

html = (open(D+"splg-plantilla.html", encoding="utf-8").read()
        .replace("__DATOS__", payload)
        .replace("__VERSION__", version)
        .replace("__GENERADO__", generado)
        .replace("__N_MERMAID__", str(n_mermaid))
        .replace("__N_UML__", str(n_uml))
        .replace("__N_CASOS__", str(len(datos["cu"])))
        .replace("__COLORES_SS__", css_subsistemas(ss.keys()))
        .replace('href="visor.css"', f'href="visor.css?v={marcas["visor.css"]}"')
        .replace('src="visor.js"', f'src="visor.js?v={marcas["visor.js"]}"'))
open(D+"splg-documentacion.html", "w", encoding="utf-8").write(html)

print(f"casos: {len(datos['cu'])} | CU reales: {len(cur)} | modulos: {len(mods)} | subsistemas con UML: {sum(1 for v in ss.values() if 'uml' in v)}")
print(f"diagramas embebidos: {sum(len(v['dss'])+len(v['dsd']) for v in datos['cu'].values())}")
print(f"splg-documentacion.html: {os.path.getsize(D+'splg-documentacion.html')/1048576:.2f} MB")
