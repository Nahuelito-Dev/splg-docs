#!/usr/bin/env python3
"""Genera el Atlas de Casos de Uso: una pagina con los cuatro artefactos de cada caso
(alto nivel, expandido, secuencia del sistema, interaccion de diseño) y el documento
y seccion donde cada uno esta respaldado.

Uso:  python3 generar-atlas.py     ->  atlas-casos-de-uso.html
"""
import re, json, os, glob, base64, sys

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
for c,v in ss.items():
    g = glob.glob(D+f"diagramas/uml/CU_{c}_*.png")
    if g: v["uml"] = b64(g[0])
g = glob.glob(D+"diagramas/uml/CU_Sistema_*.png")
contexto = b64(g[0]) if g else ""

# ---------- markdown -> html, para los bloques que se muestran tal cual ----------
import html as _html
def md2html(md):
    """Convierte un bloque de markdown a HTML y separa los diagramas mermaid."""
    diagramas = []
    def inline(s):
        s = _html.escape(s)
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
        return s
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
                             nombre=_m.group(3).strip(), sec="§6."+_m.group(1))


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
datos = {"cu":{}, "subsistemas":ss, "contexto":contexto, "modulos":mods}
for c in sorted(set(cua) | set(cue)):
    datos["cu"][c] = {"cua":cua.get(c,{}), "cue":cue.get(c,{}), "dss":dss.get(c,[]),
                      "dsd":dsd.get(c,[]), "respaldo":proc.get(c,[]), "modulo":modulo.get(c),
                      "cur":cur.get(c)}

faltan = {k:[a for a in ("cua","cue","dss","dsd") if not v[a]] for k,v in datos["cu"].items()}
faltan = {k:v for k,v in faltan.items() if v}
if faltan:
    print("ATENCION, casos con artefactos faltantes:", faltan, file=sys.stderr)

payload = json.dumps(datos, ensure_ascii=False, separators=(",",":")).replace("</", "<\\/")
html = open(D+"atlas-plantilla.html", encoding="utf-8").read().replace("__DATOS__", payload)
open(D+"atlas-casos-de-uso.html", "w", encoding="utf-8").write(html)

print(f"casos: {len(datos['cu'])} | CU reales: {len(cur)} | modulos: {len(mods)} | subsistemas con UML: {sum(1 for v in ss.values() if 'uml' in v)}")
print(f"diagramas embebidos: {sum(len(v['dss'])+len(v['dsd']) for v in datos['cu'].values())}")
print(f"atlas-casos-de-uso.html: {os.path.getsize(D+'atlas-casos-de-uso.html')/1048576:.2f} MB")
