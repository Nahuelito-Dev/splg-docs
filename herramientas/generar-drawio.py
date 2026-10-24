#!/usr/bin/env python3
"""Genera los modelos de SPLG como archivos de draw.io (`modelos/drawio/*.drawio`).

    python3 herramientas/generar-drawio.py

Salen cuatro archivos, cada uno con **una sola página** y el diagrama completo:

  SPLG-MC.drawio    modelo conceptual: conceptos, asociaciones con nombre y multiplicidades en los dos
                    extremos, composiciones, generalizaciones y la clase de asociación
  SPLG-DER.drawio   DER conceptual: una entidad por concepto con tabla, con el vocabulario del modelo
                    conceptual y las relaciones con su cardinalidad (pata de gallo)
  SPLG-DBD.drawio   diagrama de base de datos físico: las tablas reales de `splg_db` con columnas, tipos,
                    claves, únicos e índices, y cada clave foránea simple como una arista de la columna FK a la
                    clave primaria de la tabla destino (las compuestas por distribuidora se marcan en `distributor_id`)
  SPLG-DC.drawio    diagrama de clases de diseño: asociaciones con navegabilidad y multiplicidades,
                    composición y agregación, generalización y dependencias

Todo sale de las mismas fuentes que el resto de la documentación; al cambiar los modelos se regenera a mano (necesita graphviz: si falta, termina con error):
`modelo_conceptual.py` (MC), `modelos/base-de-datos/SPLG-modelo.json` (que escribe `generar-modelo-datos.py`
a partir de la base) y `herramientas/dc_larman.py` (el diagrama de clases derivado de los DSD).

Cada elemento es una celda de draw.io y cada relación una arista con `source` y `target` reales: se mueve una
tabla y la arista la sigue. Las aristas llevan sus datos (`tipo`, `origen`, `destino`, `nombre`) como propiedades,
y `verificar-drawio.py` las compara contra la fuente.
"""
import collections, html, json, math, os, re, subprocess, sys, time

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
SAL = D + "modelos/drawio/"
sys.path.insert(0, D + "herramientas")
sys.path.insert(0, D + "herramientas")

# ------------------------------------------------------------------ medidas y colores
FUENTE = 11
ANCHO_CHAR = 6.15
ALTO_LINEA = 15
MARGEN_GRUPO = 36
TITULO_GRUPO = 38
SEP_GRUPOS = 70
from estilo_vp import TINTA, BORDE as GRIS, RELLENO, RELLENO_CLARO   # estilo Visual Paradigm, centralizado
COLOR = {"dominio": RELLENO, "controlador": "#B7CDE8", "fachada": "#B7CDE8", "fabricación pura": "#E4ECF6",
         "colección": "#E6E6E6", "puerto": "#D5E3F3", "adaptador": "#D5E3F3", "planificado": "#FFF6D9"}
FONDOS_GRUPO = ["#FFFFFF", "#F7FAFD", "#FFFFFF", "#F7FAFD", "#FFFFFF", "#F7FAFD"]


def esc(s):
    return html.escape(str(s), quote=True)


# ------------------------------------------------------------------ el lienzo
class Lienzo:
    """Las celdas de una página de draw.io, con ids propios y geometría absoluta de cada vértice.
    Las aristas se guardan como especificación y se escriben al final, cuando el enrutador ya les calculó el
    recorrido."""

    def __init__(self, grilla=10):
        self.celdas = []          # texto XML de los vértices
        self.n = 0
        self.abs = {}             # id -> (x, y, w, h) absolutos
        self.nodos = []           # ids de las tablas, clases o entidades: son los obstáculos del enrutador
        self.obst = {}            # terminal -> id del nodo que lo contiene (una fila pertenece a su tabla)
        self.aristas = []         # especificación de cada arista
        self.grilla = grilla

    def id(self, prefijo):
        self.n += 1
        return f"{prefijo}{self.n}"

    def vertice(self, valor, estilo, x, y, w, h, padre="1", id_=None, abs_=None, nodo=False, de_nodo=None):
        id_ = id_ or self.id("v")
        self.celdas.append(
            f'<mxCell id="{id_}" value="{esc(valor)}" style="{estilo}" vertex="1" parent="{padre}">'
            f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')
        self.abs[id_] = abs_ or (x, y, w, h)
        if nodo:
            self.nodos.append(id_)
            self.obst[id_] = id_
        if de_nodo:
            self.obst[id_] = de_nodo
        return id_

    def arista(self, origen, destino, estilo, tipo, datos, etiqueta="", extremos=("", ""), id_=None):
        """Una arista entre dos celdas (o hacia otra arista). `extremos` son las multiplicidades en el
        extremo de origen y en el de destino."""
        id_ = id_ or self.id("e")
        e = {"id": id_, "origen": origen, "destino": destino, "tipo": tipo, "estilo": estilo, "datos": datos,
             "etiqueta": etiqueta, "extremos": extremos, "puntos": None, "puertos": ""}
        self.aristas.append(e)
        return id_

    def _xml_arista(self, e):
        attrs = " ".join(f'{k}="{esc(v)}"' for k, v in e["datos"].items())
        pts = ""
        if e["puntos"]:
            pts = "<Array as=\"points\">" + "".join(f'<mxPoint x="{x:.0f}" y="{y:.0f}"/>' for x, y in e["puntos"]) + "</Array>"
        estilo = e["puertos"] + e["estilo"]
        out = [f'<object label="{esc(e["etiqueta"])}" id="{e["id"]}" tipo="{esc(e["tipo"])}" {attrs}>'
               f'<mxCell style="{estilo}" edge="1" parent="1" source="{e["origen"]}" target="{e["destino"]}">'
               f'<mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell></object>']
        for texto, x in ((e["extremos"][0], -0.80), (e["extremos"][1], 0.80)):
            if texto:
                out.append(
                    f'<mxCell id="{self.id("m")}" value="{esc(texto)}" '
                    f'style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];'
                    f'fontSize=10;fontColor={TINTA};labelBackgroundColor=#FFFFFF;" vertex="1" connectable="0" parent="{e["id"]}">'
                    f'<mxGeometry x="{x}" relative="1" as="geometry"><mxPoint y="-9" as="offset"/></mxGeometry></mxCell>')
        return "\n".join(out)

    def xml(self, nombre):
        ancho = max((x + w for x, y, w, h in self.abs.values()), default=800) + 80
        alto = max((y + h for x, y, w, h in self.abs.values()), default=600) + 80
        cuerpo = "\n".join(self.celdas + [self._xml_arista(e) for e in self.aristas])
        return (f'<mxfile host="app.diagrams.net" agent="generar-drawio.py" version="24.0.0">\n'
                f' <diagram id="splg" name="{esc(nombre)}">\n'
                f'  <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
                f'arrows="1" fold="1" page="0" pageScale="1" pageWidth="{ancho:.0f}" pageHeight="{alto:.0f}" math="0" shadow="0">\n'
                f'   <root>\n<mxCell id="0"/>\n<mxCell id="1" parent="0"/>\n{cuerpo}\n   </root>\n'
                f'  </mxGraphModel>\n </diagram>\n</mxfile>\n')


# ------------------------------------------------------------------ acomodo
def dot_local(nodos, aristas, dir_="TB", sep=(0.35, 0.55), motor="dot", extra=""):
    """Posiciones relativas de los nodos de un grupo, calculadas por graphviz (centros, en puntos).
    nodos: {id: (w, h)}; aristas: [(a, b)] internas del grupo. Devuelve ({id: (x, y)}, ancho, alto)
    con (x, y) la esquina superior izquierda."""
    if not nodos:
        return {}, 0, 0
    lin = [f'digraph G {{ rankdir={dir_}; nodesep={sep[0]}; ranksep={sep[1]}; splines=false; {extra} '
           'node [shape=box, fixedsize=true, label=""];']
    for i, (w, h) in nodos.items():
        lin.append(f'  "{i}" [width={w / 72:.3f}, height={h / 72:.3f}];')
    for a, b in aristas:
        if a != b and a in nodos and b in nodos:
            lin.append(f'  "{a}" -> "{b}";')
    lin.append("}")
    try:
        out = subprocess.run([motor, "-Tplain"], input="\n".join(lin), capture_output=True, text=True,
                             check=True).stdout
    except FileNotFoundError:
        sys.exit(f"graphviz ({motor}) no está instalado: instalalo (brew install graphviz) para generar los diagramas de draw.io")
    except subprocess.CalledProcessError as e:
        sys.exit(f"graphviz ({motor}) falló: {e.stderr.strip()[:300]}")
    pos, alto_g = {}, 0.0
    for l in out.split("\n"):
        p = re.findall(r'"[^"]*"|\S+', l)
        if p and p[0] == "graph":
            alto_g = float(p[3])
        elif p and p[0] == "node":
            pos[p[1].strip('"')] = (float(p[2]) * 72, (alto_g - float(p[3])) * 72)
    if len(pos) != len(nodos):
        sys.exit(f"graphviz ({motor}) no devolvió la posición de todos los nodos ({len(pos)} de {len(nodos)})")
    esq = {i: (cx - nodos[i][0] / 2, cy - nodos[i][1] / 2) for i, (cx, cy) in pos.items()}
    minx = min(x for x, _ in esq.values())
    miny = min(y for _, y in esq.values())
    esq = {i: (x - minx, y - miny) for i, (x, y) in esq.items()}
    ancho = max(esq[i][0] + nodos[i][0] for i in esq)
    alto = max(esq[i][1] + nodos[i][1] for i in esq)
    return esq, ancho, alto


def empaquetar(grupos, ancho_objetivo=None):
    """Coloca las cajas de los grupos en filas (estantes). grupos: [(clave, w, h)] en el orden dado.
    Devuelve ({clave: (x, y)}, ancho_total, alto_total)."""
    area = sum((w + SEP_GRUPOS) * (h + SEP_GRUPOS) for _, w, h in grupos)
    objetivo = ancho_objetivo or max(max(w for _, w, _ in grupos) + SEP_GRUPOS, math.sqrt(area) * 1.35)
    pos, x, y, fila_h, total_w = {}, 0.0, 0.0, 0.0, 0.0
    for clave, w, h in grupos:
        if x and x + w > objetivo:
            x, y, fila_h = 0.0, y + fila_h + SEP_GRUPOS, 0.0
        pos[clave] = (x, y)
        x += w + SEP_GRUPOS
        fila_h = max(fila_h, h)
        total_w = max(total_w, x - SEP_GRUPOS)
    return pos, total_w, y + fila_h


def acomodar(lienzo, grupos, aristas_layout, estilo_nodo, dir_="TB", sep=(0.35, 0.55), contenedor=True, motor="dot", extra=""):
    """Coloca los nodos de cada grupo (graphviz) y los grupos en filas, todo alineado a la grilla del enrutador.
    grupos: [(clave, titulo, [(id, w, h)])]. `estilo_nodo(id, padre, x, y, abs_x, abs_y)` dibuja cada nodo.
    Con `contenedor=True` cada grupo es un recuadro con título y sus nodos son hijos suyos; con `False` los nodos
    quedan sueltos en el lienzo (coordenadas absolutas) y el nombre del grupo es un texto sin fondo ni borde."""
    g = lienzo.grilla
    arriba = lambda v: int(math.ceil(v / g)) * g
    margen, titulo_h = arriba(MARGEN_GRUPO), arriba(TITULO_GRUPO)
    if not any(t for _, t, _ in grupos):          # un solo conjunto sin nombre: no hay franja de título
        titulo_h = 0
    tamanos, locales = [], {}
    for clave, titulo, nodos in grupos:
        dim = {i: (w, h) for i, w, h in nodos}
        internas = [(a, b) for a, b in aristas_layout if a in dim and b in dim]
        esq, w, h = dot_local(dim, internas, dir_, sep, motor, extra)
        esq = {i: (arriba(x), arriba(y)) for i, (x, y) in esq.items()}
        w = max((esq[i][0] + dim[i][0] for i in esq), default=0)
        h = max((esq[i][1] + dim[i][1] for i in esq), default=0)
        locales[clave] = (esq, dim)
        ancho_t = arriba(max(w + 2 * margen, len(titulo) * 9 + 2 * margen))
        tamanos.append((clave, ancho_t, arriba(h + titulo_h + margen)))
    pos, tw, th = empaquetar(tamanos)
    contenedores = {}
    for k, (clave, titulo, nodos) in enumerate(grupos):
        gx, gy = arriba(pos[clave][0]), arriba(pos[clave][1])
        _, gw, gh = next(t for t in tamanos if t[0] == clave)
        esq, dim = locales[clave]
        if contenedor:
            fondo = FONDOS_GRUPO[k % len(FONDOS_GRUPO)]
            cid = lienzo.vertice(
                titulo,
                f"rounded=1;arcSize=2;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;"
                f"fillColor={fondo};strokeColor={GRIS};strokeWidth=1.5;dashed=0;verticalAlign=top;align=left;"
                f"spacingLeft=14;spacingTop=6;fontStyle=1;fontSize=16;fontColor={TINTA};",
                gx, gy, gw, gh)
            ox, oy = 0, 0
        else:
            cid = "1"
            ox, oy = gx, gy
            if titulo:
                lienzo.vertice(titulo, f"text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;"
                                       f"fontStyle=1;fontSize=18;fontColor={TINTA};whiteSpace=nowrap;",
                               gx + 6, gy + 6, max(len(titulo) * 10, 120), 28)
        contenedores[clave] = (cid, gx, gy)
        for i, w, h in nodos:
            x, y = esq[i]
            x += margen
            y += titulo_h
            estilo_nodo(i, cid, ox + x, oy + y, gx + x, gy + y)
    return contenedores, tw, th


# ------------------------------------------------------------------ enrutador ortogonal
def estilo_arista(base, extra=""):
    return ("rounded=1;arcSize=8;html=1;jumpStyle=arc;jumpSize=7;"
            f"strokeColor={TINTA};strokeWidth=1;fontSize=10;fontColor={TINTA};" + base + extra)


class Enrutador:
    """Rutas ortogonales sobre una grilla, con A*: esquiva las tablas o clases, penaliza los giros y el
    solaparse con las rutas ya trazadas (así las aristas paralelas se reparten en pistas distintas) y deja
    los cruces como último recurso."""
    PASO, GIRO, SOLAPE, CRUCE = 10, 30, 26, 5

    def __init__(self, ancho, alto, g):
        self.g = g
        self.cols = int(ancho // g) + 3
        self.filas = int(alto // g) + 3
        n = self.cols * self.filas
        self.bloq = bytearray(n)
        self.uh = bytearray(n)
        self.uv = bytearray(n)
        self.libres = set()

    def bloquear(self, x0, y0, x1, y1):
        g = self.g
        for j in range(max(0, int(math.ceil(y0 / g))), min(self.filas, int(y1 // g) + 1)):
            base = j * self.cols
            for i in range(max(0, int(math.ceil(x0 / g))), min(self.cols, int(x1 // g) + 1)):
                self.bloq[base + i] = 1

    def buscar(self, s, t, dir0, caja):
        cols = self.cols
        ti, tj = t
        i_min, j_min, i_max, j_max = caja
        s_idx, t_idx = s[1] * cols + s[0], t[1] * cols + t[0]
        bloq, uh, uv, libres = self.bloq, self.uh, self.uv, self.libres
        DI = (1, 0, -1, 0)
        DJ = (0, 1, 0, -1)
        PASO, GIRO, SOLAPE, CRUCE = self.PASO, self.GIRO, self.SOLAPE, self.CRUCE
        import heapq
        h0 = (abs(s[0] - ti) + abs(s[1] - tj)) * PASO
        heap = [(h0, 0, s_idx, dir0)]
        mejor = {s_idx * 4 + dir0: 0}
        padre = {}
        while heap:
            f, c, idx, d = heapq.heappop(heap)
            if idx == t_idx:
                ruta = [idx]
                k = idx * 4 + d
                while k in padre:
                    k = padre[k]
                    ruta.append(k // 4)
                ruta.reverse()
                return [(r % cols, r // cols) for r in ruta]
            if c > mejor.get(idx * 4 + d, 1 << 60):
                continue
            i, j = idx % cols, idx // cols
            for nd in (d, (d + 1) & 3, (d + 3) & 3):
                ni, nj = i + DI[nd], j + DJ[nd]
                if ni < i_min or ni > i_max or nj < j_min or nj > j_max:
                    continue
                n_idx = nj * cols + ni
                if bloq[n_idx] and n_idx not in libres:
                    continue
                coste = c + PASO + (GIRO if nd != d else 0)
                if nd & 1:      # vertical
                    coste += SOLAPE * min(uv[n_idx], 2) + CRUCE * min(uh[n_idx], 2)
                else:
                    coste += SOLAPE * min(uh[n_idx], 2) + CRUCE * min(uv[n_idx], 2)
                k = n_idx * 4 + nd
                if coste < mejor.get(k, 1 << 60):
                    mejor[k] = coste
                    padre[k] = idx * 4 + d
                    heapq.heappush(heap, (coste + (abs(ni - ti) + abs(nj - tj)) * PASO, coste, n_idx, nd))
        return None

    def marcar(self, ruta):
        cols = self.cols
        for (i0, j0), (i1, j1) in zip(ruta, ruta[1:]):
            arr = self.uh if j0 == j1 else self.uv
            for (i, j) in ((i0, j0), (i1, j1)):
                if arr[j * cols + i] < 250:
                    arr[j * cols + i] += 1


def _snap(v, g):
    return int(round(v / g)) * g


def enrutar(L, solo_lr=False, stub=None):
    """Calcula puertos de salida y de entrada y el recorrido ortogonal de cada arista. Las que no tienen ruta
    (o unen un elemento consigo mismo) quedan con el enrutado automático de draw.io."""
    g = L.grilla
    stub = stub or 2 * g
    margen = g * 0.9
    ancho = max(x + w for x, y, w, h in L.abs.values()) + 6 * g
    alto = max(y + h for x, y, w, h in L.abs.values()) + 6 * g
    rt = Enrutador(ancho, alto, g)
    for n in L.nodos:
        x, y, w, h = L.abs[n]
        rt.bloquear(x - margen, y - margen, x + w + margen, y + h + margen)

    def rect_nodo(t):
        return L.abs[L.obst.get(t, t)]

    # 1) lados
    plan = {}
    usos = collections.defaultdict(list)
    for e in L.aristas:
        o, d = e["origen"], e["destino"]
        if o in L.abs and d in L.abs and L.obst.get(o, o) == L.obst.get(d, d):
            # una relación del elemento consigo mismo: sale por la derecha, da la vuelta y vuelve a entrar
            nx_, ny_, nw_, nh_ = rect_nodo(o)
            to_ = L.abs[o]
            td_ = L.abs[d]
            if L.obst.get(o, o) == o:             # clase o entidad: dos alturas distintas del mismo lado
                yo, yd = ny_ + nh_ * 0.35, ny_ + nh_ * 0.7
            else:                                  # fila de una tabla: el centro de cada fila
                yo, yd = to_[1] + to_[3] / 2, td_[1] + td_[3] / 2
            yo, yd = _snap(yo, g), _snap(yd, g)
            xf = _snap(nx_ + nw_ + 3 * g, g)
            e["puertos"] = (f"exitX=1;exitY={(yo - to_[1]) / to_[3]:.4f};exitDx=0;exitDy=0;exitPerimeter=0;"
                            f"entryX=1;entryY={(yd - td_[1]) / td_[3]:.4f};entryDx=0;entryDy=0;entryPerimeter=0;")
            e["puntos"] = [(xf, yo), (xf, yd)]
            continue
        if o not in L.abs or d not in L.abs:
            e["estilo"] = "edgeStyle=orthogonalEdgeStyle;" + e["estilo"]
            continue
        ro, rd = rect_nodo(o), rect_nodo(d)
        cxo, cyo, cxd, cyd = ro[0] + ro[2] / 2, ro[1] + ro[3] / 2, rd[0] + rd[2] / 2, rd[1] + rd[3] / 2
        ddx, ddy = cxd - cxo, cyd - cyo
        if solo_lr:
            if ro[0] + ro[2] < rd[0] - 2 * g:
                lo, ld = "E", "W"
            elif rd[0] + rd[2] < ro[0] - 2 * g:
                lo, ld = "W", "E"
            else:
                lo = ld = "E" if cxo + cxd >= 2 * (max(ro[0], rd[0])) else "W"
                lo = ld = "E" if (ro[0] + ro[2] / 2 + rd[0] + rd[2] / 2) / 2 > max(ro[0], rd[0]) + 40 else "W"
        elif abs(ddx) * 0.55 >= abs(ddy):
            lo, ld = ("E", "W") if ddx > 0 else ("W", "E")
        else:
            lo, ld = ("S", "N") if ddy > 0 else ("N", "S")
        plan[e["id"]] = (lo, ld)
        usos[(L.obst.get(o, o), lo, o if o != L.obst.get(o, o) else None)].append((cyd if lo in "EW" else cxd, e["id"], True))
        usos[(L.obst.get(d, d), ld, d if d != L.obst.get(d, d) else None)].append((cyo if ld in "EW" else cxo, e["id"], False))
    # 2) puntos sobre cada lado (en la grilla)
    frac = {}
    for (nodo, lado, fila), lst in usos.items():
        lst.sort()
        n = len(lst)
        for i, (_, e, es_o) in enumerate(lst):
            frac[(e, es_o)] = (i + 1) / (n + 1)
    puertos = {}
    for e in L.aristas:
        if e["id"] not in plan:
            continue
        lo, ld = plan[e["id"]]
        res = []
        for term, lado, es_o in ((e["origen"], lo, True), (e["destino"], ld, False)):
            nodo = L.obst.get(term, term)
            ox, oy, ow, oh = L.abs[nodo]
            tx, ty, tw, th = L.abs[term]
            if term != nodo:          # una fila de una tabla: el punto va en el centro de la fila
                py = ty + th / 2
                px = ox + ow if lado == "E" else ox
            elif lado in "EW":
                py = _snap(oy + 6 + (oh - 12) * frac[(e["id"], es_o)], g)
                py = min(max(py, oy + 4), oy + oh - 4)
                px = ox + ow if lado == "E" else ox
            else:
                px = _snap(ox + 6 + (ow - 12) * frac[(e["id"], es_o)], g)
                px = min(max(px, ox + 4), ox + ow - 4)
                py = oy + oh if lado == "S" else oy
            if lado == "E":
                sx, sy = math.ceil((px + stub) / g) * g, _snap(py, g)
            elif lado == "W":
                sx, sy = math.floor((px - stub) / g) * g, _snap(py, g)
            elif lado == "S":
                sx, sy = _snap(px, g), math.ceil((py + stub) / g) * g
            else:
                sx, sy = _snap(px, g), math.floor((py - stub) / g) * g
            res.append(((px, py), (sx, sy), lado, (tx, ty, tw, th)))
        puertos[e["id"]] = res
    # 3) rutas, de las más cortas a las más largas
    orden = sorted((e for e in L.aristas if e["id"] in puertos),
                   key=lambda e: abs(puertos[e["id"]][0][1][0] - puertos[e["id"]][1][1][0]) +
                                 abs(puertos[e["id"]][0][1][1] - puertos[e["id"]][1][1][1]))
    sin_ruta = 0
    DIR = {"E": 0, "S": 1, "W": 2, "N": 3}
    for e in orden:
        (p0, s0, l0, r0), (p1, s1, l1, r1) = puertos[e["id"]]
        a = (int(round(s0[0] / g)), int(round(s0[1] / g)))
        b = (int(round(s1[0] / g)), int(round(s1[1] / g)))
        rt.libres |= {a[1] * rt.cols + a[0], b[1] * rt.cols + b[0]}
        ruta = None
        for ext in (30, 90, 10 ** 6):
            caja = (max(0, min(a[0], b[0]) - ext), max(0, min(a[1], b[1]) - ext),
                    min(rt.cols - 1, max(a[0], b[0]) + ext), min(rt.filas - 1, max(a[1], b[1]) + ext))
            ruta = rt.buscar(a, b, DIR[l0], caja)
            if ruta:
                break
        # fracciones respecto del terminal
        def fr(p, r):
            return (min(max((p[0] - r[0]) / r[2], 0), 1), min(max((p[1] - r[1]) / r[3], 0), 1))
        (ex, ey), (nx, ny) = fr(p0, r0), fr(p1, r1)
        e["puertos"] = (f"exitX={ex:.4f};exitY={ey:.4f};exitDx=0;exitDy=0;exitPerimeter=0;"
                        f"entryX={nx:.4f};entryY={ny:.4f};entryDx=0;entryDy=0;entryPerimeter=0;")
        if not ruta:
            sin_ruta += 1
            e["estilo"] = "edgeStyle=orthogonalEdgeStyle;" + e["estilo"]
            continue
        rt.marcar(ruta)
        pts = [(i * g, j * g) for i, j in ruta]
        comp = [pts[0]]
        for k in range(1, len(pts) - 1):
            (x0, y0), (x1, y1), (x2, y2) = pts[k - 1], pts[k], pts[k + 1]
            if (x0 == x1 == x2) or (y0 == y1 == y2):
                continue
            comp.append(pts[k])
        if len(pts) > 1:
            comp.append(pts[-1])
        e["puntos"] = comp
    return sin_ruta


# ------------------------------------------------------------------ texto de las cajas
def ancho_de(lineas, minimo=150, maximo=620):
    return max(minimo, min(maximo, max((len(l) for l in lineas), default=0) * ANCHO_CHAR + 22))


def caja_html(titulo, estereotipo, secciones):
    """HTML del rótulo de una clase o entidad: estereotipo, nombre y secciones separadas por línea."""
    cab = ""
    if estereotipo:
        cab += f'<i style="font-size:10px">{esc(estereotipo)}</i><br>'
    cab += f"<b>{esc(titulo)}</b>"
    h = f'<div style="text-align:center">{cab}</div>'
    for s in secciones:
        if s:
            h += '<hr size="1" style="margin:2px 0">' + "<br>".join(esc(x) for x in s)
    return h


def estilo_caja(fondo, planificado=False, extra=""):
    borde = "dashed=1;dashPattern=6 3;" if planificado else ""
    return (f"rounded=0;whiteSpace=nowrap;html=1;align=left;verticalAlign=top;spacingLeft=6;spacingRight=4;spacingTop=3;"
            f"fontSize={FUENTE};fontFamily=Arial;fillColor={fondo};strokeColor={TINTA};strokeWidth=1;"
            f"overflow=hidden;{borde}{extra}")


# ================================================================== MC
def generar_mc():
    import modelo_conceptual as M
    L = Lienzo(10)
    plan = getattr(M, "PLANIFICADOS", {})
    ids = {}
    grupos = []
    for clave, titulo in M.CONTEXTOS:
        nodos = []
        for nombre, (ctx, atrs, abstracta) in M.CLASES.items():
            if ctx != clave:
                continue
            lineas = ["- " + a if not a.startswith("/") else "/ " + a[1:] for a in atrs]
            w = ancho_de([nombre] + lineas, 150)
            h = 26 + (len(atrs) * ALTO_LINEA + 8 if atrs else 6) + (14 if nombre in plan else 0)
            nodos.append((nombre, w, h))
        grupos.append((clave, titulo, nodos))
    aristas_layout = [(a[0], a[4]) for a in M.ASOCIACIONES] + [(p, h) for p, hs, _ in M.GENERALIZACIONES for h in hs]

    def dibujar(nombre, padre, x, y, ax, ay):
        ctx, atrs, abstracta = M.CLASES[nombre]
        lineas = ["- " + a if not a.startswith("/") else "/ " + a[1:] for a in atrs]
        w = ancho_de([nombre] + lineas, 150)
        h = 26 + (len(atrs) * ALTO_LINEA + 8 if atrs else 6) + (14 if nombre in plan else 0)
        est = "planificado (" + plan[nombre] + ")" if nombre in plan else ("{abstracta}" if abstracta else "")
        fondo = COLOR["planificado"] if nombre in plan else COLOR["dominio"]
        v = L.vertice(caja_html(nombre, est, [lineas] if lineas else []), estilo_caja(fondo, nombre in plan),
                      x, y, w, h, padre, abs_=(ax, ay, w, h), nodo=True)
        ids[nombre] = v

    grupos = [("todo", "", [n for _, _, ns in grupos for n in ns])]
    cont, tw, th = acomodar(L, grupos, aristas_layout, dibujar, dir_="TB", sep=(0.6, 0.9), contenedor=False,
             motor="fdp", extra='overlap=prism; sep="+40"; K=3; start=1;')
    # asociaciones
    for a, ma, tipo, mb, b, nombre, cat in M.ASOCIACIONES:
        base = "endArrow=none;startArrow=none;"
        if tipo == "*":
            base = "startArrow=diamondThin;startFill=1;startSize=14;endArrow=none;"
        L.arista(ids[a], ids[b], estilo_arista(base, ""), "asociacion",
                 {"origen_nombre": a, "destino_nombre": b, "nombre": nombre, "mult_origen": ma, "mult_destino": mb,
                  "composicion": "si" if tipo == "*" else "no"}, etiqueta=nombre, extremos=(ma, mb))
    for padre, hijos, restr in M.GENERALIZACIONES:
        for h in hijos:
            L.arista(ids[h], ids[padre], estilo_arista("endArrow=block;endFill=0;endSize=12;startArrow=none;", ""),
                     "generalizacion", {"origen_nombre": h, "destino_nombre": padre, "nombre": restr},
                     etiqueta=restr if h == hijos[0] else "")
    # clase de asociación: línea punteada de la clase a la asociación que completa
    ca, c1, c2 = M.CLASE_ASOCIACION
    asoc = next(e for e in L.aristas if e["tipo"] == "asociacion" and
                {e["datos"]["origen_nombre"], e["datos"]["destino_nombre"]} == {c1, c2} and e["datos"]["nombre"] == "usa")
    L.arista(ids[ca], asoc["id"], estilo_arista("dashed=1;endArrow=none;startArrow=none;", ""), "clase_de_asociacion",
             {"origen_nombre": ca, "destino_nombre": f"{c1}-{c2}", "nombre": "clase de asociación"})
    # los puertos solo para aristas entre vértices
    enrutar(L)
    return L


# ================================================================== DER
SIMBOLO_ER = {"1": "ERmandOne", "0..1": "ERzeroToOne", "0..*": "ERzeroToMany", "*": "ERzeroToMany",
              "1..*": "ERoneToMany", "uno": "ERmandOne", "cero_uno": "ERzeroToOne", "muchos": "ERzeroToMany"}


def aprox_er(m):
    if m in SIMBOLO_ER:
        return m
    return "1..*" if m.split("..")[0] not in ("0", "") else "0..*"


def generar_der(modelo):
    import modelo_conceptual as M
    der = modelo["der"]
    L = Lienzo(10)
    ents = der["entidades"]
    plan = getattr(M, "PLANIFICADOS", {})
    ids = {}

    def lineas_de(c):
        return ["* identificador"] + ["– " + a for a in ents[c]["atributos"]]

    grupos = []
    for clave, titulo in M.CONTEXTOS:
        nodos = []
        for c, e in ents.items():
            if e["contexto"] != clave:
                continue
            ls = lineas_de(c)
            nodos.append((c, ancho_de([c] + ls, 150), 28 + len(ls) * ALTO_LINEA + 8))
        if nodos:
            grupos.append((clave, titulo, nodos))
    rels = der["relaciones"]
    aristas_layout = [(r["izq"], r["der"]) for r in rels]

    def dibujar(c, padre, x, y, ax, ay):
        ls = lineas_de(c)
        w, h = ancho_de([c] + ls, 150), 28 + len(ls) * ALTO_LINEA + 8
        pl = c in plan
        v = L.vertice(caja_html(c, "planificado (" + plan[c] + ")" if pl else "", [ls]),
                      estilo_caja(COLOR["planificado"] if pl else COLOR["dominio"], pl), x, y, w, h, padre,
                      abs_=(ax, ay, w, h), nodo=True)
        ids[c] = v

    grupos = [("todo", "", [n for _, _, ns in grupos for n in ns])]
    acomodar(L, grupos, aristas_layout, dibujar, dir_="TB", sep=(0.6, 0.9), contenedor=False,
             motor="fdp", extra='overlap=prism; sep="+40"; K=3; start=1;')
    for r in rels:
        ci, cd = aprox_er(r["card_izq"]), aprox_er(r["card_der"])
        exactas = [m for m in (r["card_izq"], r["card_der"]) if m not in SIMBOLO_ER]
        etiqueta = r["nombre"] + (" [" + " / ".join(exactas) + "]" if exactas else "")
        base = f"startArrow={SIMBOLO_ER[ci]};startFill=0;endArrow={SIMBOLO_ER[cd]};endFill=0;startSize=12;endSize=12;"
        L.arista(ids[r["izq"]], ids[r["der"]], estilo_arista(base, ""), "relacion",
                 {"origen_nombre": r["izq"], "destino_nombre": r["der"], "nombre": r["nombre"],
                  "mult_origen": r["card_izq"], "mult_destino": r["card_der"]}, etiqueta=etiqueta)
    enrutar(L)
    return L


# ================================================================== DBD
ER_DBD = {"muchos": "ERzeroToMany", "cero_uno": "ERzeroToOne", "uno": "ERmandOne"}
ALTO_FILA = 18


def indices_cortos(t):
    """Únicos compuestos e índices de una tabla, en una línea cada uno."""
    out = []
    for g in t["unicos"]:
        if len(g) > 1:
            out.append("UQ (" + ", ".join(g) + ")")
    for nombre, defi in t["indices"]:
        m = re.search(r'CREATE (UNIQUE )?INDEX (\S+) ON \S+ USING \w+ \((.*?)\)(?: WHERE (.*))?$', defi)
        if not m:
            continue
        cols = m.group(3).replace('"', "")
        unico, parcial = bool(m.group(1)), m.group(4)
        if unico and not parcial and len(cols.split(",")) == 1 and cols in {c["nombre"] for c in t["columnas"] if c["unico"]}:
            continue            # ya figura como columna única
        if unico and not parcial and [c.strip() for c in cols.split(",")] in t["unicos"]:
            continue
        txt = ("UQ " if unico else "IX ") + "(" + cols + ")"
        if parcial:
            txt += " parcial"
        if txt not in out:
            out.append(txt)
    return out


def generar_dbd(modelo):
    dbd = modelo["dbd"]
    L = Lienzo(6)
    tablas = dbd["tablas"]
    filas = {}                       # (tabla, columna) -> id de la fila
    tabla_id = {}

    def textos(t):
        d = tablas[t]
        out = []
        for c in d["columnas"]:
            marca = "PK" if c["pk"] else ("FK" if c["fk"] else ("UQ" if c["unico"] else "  "))
            comp = ""
            if c.get("fk_compuesta"):
                dest = sorted({g["destino"] for g in c["fk_compuesta"]})
                comp = f"  · FK compuesta: {', '.join(dest[:3])}{f' +{len(dest) - 3}' if len(dest) > 3 else ''}"
            out.append((c, f"{marca}  {c['nombre']} : {c['tipo']}{'' if c['nulo'] else ' *'}{comp}"))
        return out

    def medidas(t):
        tx = textos(t)
        ix = indices_cortos(tablas[t])
        w = ancho_de([t] + [s for _, s in tx] + ix, 190, 560) + 26
        h = 27 + len(tx) * ALTO_FILA + (len(ix) * 12 + 8 if ix else 0)
        return w, h, tx, ix

    # un DBD clásico: sin módulos ni agrupación visual. Un solo conjunto con todas las tablas, que graphviz
    # acomoda de forma orgánica a partir de las claves foráneas (las tablas relacionadas quedan cerca).
    grupos = [("todo", "", [(t, *medidas(t)[:2]) for t in tablas])]
    aristas_layout = [(t, c["fk"]["destino"]) for t in tablas for c in tablas[t]["columnas"]
                      if c["fk"] and c["fk"]["destino"] != "distributor"]

    def dibujar(t, padre, x, y, ax, ay):
        w, h, tx, ix = medidas(t)
        tid = L.vertice(t, (f"swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=27;fillColor=#C6DAF0;"
                            f"horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;"
                            f"swimlaneFillColor=#FFFFFF;strokeColor={TINTA};strokeWidth=1;fontSize=12;fontColor={TINTA};"
                            f"align=center;"), x, y, w, h, padre, abs_=(ax, ay, w, h), nodo=True)
        tabla_id[t] = tid
        yy = 27
        for c, s in tx:
            rid = L.vertice(s, (f"text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=6;"
                                f"spacingRight=4;overflow=hidden;rotatable=0;whiteSpace=nowrap;html=1;fontSize={FUENTE};"
                                f"fontFamily=Arial;fontColor={TINTA};" + ("fontStyle=1;" if c["pk"] else "")),
                            0, yy, w, ALTO_FILA, tid, abs_=(ax, ay + yy, w, ALTO_FILA), de_nodo=tid)
            filas[(t, c["nombre"])] = rid
            yy += ALTO_FILA
        if ix:
            L.vertice("<br>".join(esc(s) for s in ix), (f"text;strokeColor=none;fillColor=#F4F6F8;align=left;verticalAlign=top;"
                      f"spacingLeft=6;spacingTop=3;overflow=hidden;whiteSpace=nowrap;html=1;fontSize=9;fontColor=#55616C;"
                      f"fontStyle=2;rotatable=0;lineHeight=1;"), 0, yy, w, len(ix) * 12 + 8, tid,
                      abs_=(ax, ay + yy, w, len(ix) * 12 + 8))

    acomodar(L, grupos, aristas_layout, dibujar, dir_="TB", sep=(0.6, 0.9), contenedor=False,
             motor="fdp", extra='overlap=prism; sep="+40"; K=3; start=1;')
    # una arista por clave foránea: de la columna FK a la clave primaria de la tabla destino
    for t, d in tablas.items():
        for c in d["columnas"]:
            f = c["fk"]
            if not f:
                continue
            base = (f"startArrow={ER_DBD[f['card_hijo']]};startFill=0;endArrow={ER_DBD[f['card_padre']]};endFill=0;"
                    "startSize=11;endSize=11;")
            L.arista(filas[(t, c["nombre"])], filas[(f["destino"], f["destcol"])],
                     estilo_arista(base, "strokeColor=#7FA3C4;strokeWidth=1;" if f["destino"] == "distributor" else ""), "fk",
                     {"tabla": t, "columna": c["nombre"], "destino_tabla": f["destino"], "destino_columna": f["destcol"],
                      "card_hijo": f["card_hijo"], "card_padre": f["card_padre"], "borrado": f["borrado"]})
    enrutar(L, solo_lr=True)
    return L


# ================================================================== DC
def firma_lineas(texto, ancho=58):
    """Una firma partida en la coma de sus parámetros, como en las láminas de PlantUML."""
    if len(texto) <= ancho:
        return [texto]
    partes, actual = [], ""
    for tr in re.split(r'(?<=, )', texto):
        if actual and len(actual) + len(tr) > ancho:
            partes.append(actual.rstrip())
            actual = "      "
        actual += tr
    partes.append(actual)
    return partes


MODULOS = {
    "order": "Pedidos (order)", "stock": "Stock (stock)", "purchase": "Compras (purchase)",
    "truck-load": "Carga del camión (truck-load)", "employee": "Personal (employee)", "fleet": "Flota (fleet)",
    "fleet-expense": "Flota: gastos (fleet-expense)", "cash": "Caja (cash)", "cylinder": "Envases (cylinder)",
    "audit": "Auditoría (audit)", "distributor": "Distribuidoras (distributor)", "customer": "Clientes (customer)",
    "driver-settlement": "Rendición del chofer (driver-settlement)", "commission": "Comisiones (commission)",
    "car": "Vehículos (car)", "customer-account": "Cuentas corrientes (customer-account)",
    "gascylinder": "Productos (gascylinder)", "coverage-zone": "Cobertura (coverage-zone)", "delivery": "Choferes (delivery)",
    "users": "Usuarios (users)", "role": "Roles (role)", "admin": "Administradores (admin)", "payments": "Pagos (payments)",
    "gateways": "Tiempo real (gateways)", "repurchase": "Recompra (repurchase)", "user-address": "Direcciones (user-address)",
    "cart": "Carrito (cart)", "time-slot": "Franjas (time-slot)", "claims": "Reclamos (claims)",
    "incident": "Incidencias (incident)", "attachment": "Adjuntos (attachment)", "rating": "Calificaciones (rating)",
    "firebase": "Firebase", "reports": "Reportes (reports)", "email": "Correo (email)", "health": "Salud (health)",
    "s3": "Archivos (s3)", "auth": "Sesión (auth)", "registro": "Registro", "notifications": "Notificaciones",
    "redis": "Redis",
}
ORDEN_MODULOS = ["auth", "registro", "firebase", "users", "role", "admin", "audit", "distributor", "customer", "user-address",
                 "cart", "repurchase", "gascylinder", "time-slot", "coverage-zone", "order", "payments", "gateways",
                 "delivery", "car", "fleet", "fleet-expense", "cylinder", "claims", "incident", "rating", "reports",
                 "employee", "attachment", "stock", "purchase", "truck-load", "cash", "driver-settlement",
                 "customer-account", "commission", "notifications", "email", "health", "redis", "s3"]


def generar_dc():
    import dc_larman as X
    import modelo_conceptual as M
    dc = X.construir()
    if X.FALTAN or dc.sin_resolver:
        sys.exit("dc_larman no resuelve todos los tipos: corré herramientas/generar-clases-diseno.py")
    L = Lienzo(12)
    ids = {}
    plan = getattr(M, "PLANIFICADOS", {})

    def contenido(nombre):
        cl = dc.clases[nombre]
        attrs = [f"{v} {n}: {t}" for v, n, t in cl.atributos]
        ops = []
        for op in sorted(cl.ops.values(), key=lambda o: (not o.crea, o.nombre.lower(), len(o.params))):
            ops += ["+ " + firma_lineas(op.firma(nombre))[0]] + firma_lineas(op.firma(nombre))[1:]
        return cl, attrs, ops

    def medidas(nombre):
        cl, attrs, ops = contenido(nombre)
        est = cl.estereotipo if cl.tipo != "dominio" else ("{abstracta}" if cl.abstracta else "")
        if nombre in plan:
            est = "planificado (" + plan[nombre] + ")"
        lineas = [nombre] + attrs + ops
        w = ancho_de(lineas, 150, 600)
        n_lineas = len(attrs) + len(ops)
        h = 28 + (14 if est else 0) + n_lineas * ALTO_LINEA + (10 if attrs and ops else 0) + 8
        return w, h, est

    por_modulo = collections.defaultdict(list)
    for n, cl in dc.clases.items():
        por_modulo[cl.modulo or "otros"].append(n)
    orden = [m for m in ORDEN_MODULOS if m in por_modulo] + sorted(m for m in por_modulo if m not in ORDEN_MODULOS)
    grupos = [(m, MODULOS.get(m, m), [(n, *medidas(n)[:2]) for n in sorted(por_modulo[m])]) for m in orden]

    aristas_layout = [(a["a"], a["b"]) for a in dc.asociaciones] + sorted(dc.dependencias) + \
                     [(p, h) for p, h in dc.generalizaciones]

    def dibujar(nombre, padre, x, y, ax, ay):
        cl, attrs, ops = contenido(nombre)
        w, h, est = medidas(nombre)
        fondo = COLOR["planificado"] if nombre in plan else COLOR.get(cl.estereotipo if cl.tipo != "dominio" else "dominio", COLOR["dominio"])
        v = L.vertice(caja_html(nombre, est, [attrs, ops]), estilo_caja(fondo, nombre in plan or getattr(cl, "planificada", False)),
                      x, y, w, h, padre, abs_=(ax, ay, w, h), nodo=True)
        ids[nombre] = v

    grupos = [("todo", "", [n for _, _, ns in grupos for n in ns])]
    acomodar(L, grupos, aristas_layout, dibujar, dir_="TB", sep=(0.6, 0.9), contenedor=False,
             motor="fdp", extra='overlap=prism; sep="+40"; K=3; start=1;')

    for a in dc.asociaciones:
        tipo = a["tipo"]
        if tipo == "comp":
            base = "startArrow=diamondThin;startFill=1;startSize=14;" + ("endArrow=open;endSize=9;" if a["nav_ab"] and not a["nav_ba"] else "endArrow=none;")
        elif tipo == "agreg":
            base = "startArrow=diamondThin;startFill=0;startSize=14;endArrow=open;endSize=9;"
        else:
            s = "startArrow=open;startSize=9;" if a["nav_ba"] else "startArrow=none;"
            e = "endArrow=open;endSize=9;" if a["nav_ab"] else "endArrow=none;"
            base = s + e
        L.arista(ids[a["a"]], ids[a["b"]], estilo_arista(base, ""), "asoc_" + tipo,
                 {"origen_nombre": a["a"], "destino_nombre": a["b"], "nombre": a["nombre"] or "",
                  "mult_origen": a["ma"] or "", "mult_destino": a["mb"] or "",
                  "navega_ab": "si" if a["nav_ab"] else "no", "navega_ba": "si" if a["nav_ba"] else "no"},
                 etiqueta=a["nombre"] or "", extremos=(a["ma"] or "", a["mb"] or ""))
    for o, d in sorted(dc.dependencias):
        crea = (o, d) in dc.creaciones
        L.arista(ids[o], ids[d], estilo_arista("dashed=1;endArrow=open;endSize=9;startArrow=none;", ""), "dependencia",
                 {"origen_nombre": o, "destino_nombre": d, "nombre": "«create»" if crea else ""},
                 etiqueta="«create»" if crea else "")
    for ad, pu in dc.realizaciones:
        L.arista(ids[ad], ids[pu], estilo_arista("dashed=1;endArrow=block;endFill=0;endSize=12;startArrow=none;", ""),
                 "realizacion", {"origen_nombre": ad, "destino_nombre": pu, "nombre": ""})
    for p, h in dc.generalizaciones:
        restr = next(x[2] for x in M.GENERALIZACIONES if x[0] == p)
        L.arista(ids[h], ids[p], estilo_arista("endArrow=block;endFill=0;endSize=12;startArrow=none;", ""),
                 "generalizacion", {"origen_nombre": h, "destino_nombre": p, "nombre": restr})
    enrutar(L)
    return L


# ================================================================== principal
LEEME = """# Diagramas en draw.io

Los modelos de SPLG como archivos de draw.io, con cada relación dibujada como una arista conectada a sus dos
elementos (si se mueve una tabla o una clase, la línea la sigue). Los genera `generar-drawio.py`; no se editan a mano.

| Archivo | Qué es | Origen |
|---|---|---|
| `SPLG-MC.drawio` | Modelo conceptual: conceptos con atributos, asociaciones con nombre y multiplicidades en los dos extremos, composición, generalización y la clase de asociación | `modelo_conceptual.py` |
| `SPLG-DER.drawio` | DER conceptual: una entidad por concepto con tabla, con el vocabulario del modelo conceptual y las relaciones en pata de gallo | `modelos/base-de-datos/SPLG-modelo.json` |
| `SPLG-DBD.drawio` | Diagrama de base de datos físico: las {tablas} tablas de la base con columnas, tipos, claves, únicos e índices, y cada una de las {fks} claves foráneas simples como una arista de la columna FK a la clave primaria destino; las {fks_comp} compuestas `(id, distributor_id)` repiten esa relación y se marcan en la columna `distributor_id` («FK compuesta») | `modelos/base-de-datos/SPLG-modelo.json` (leído de la base) |
| `SPLG-DC.drawio` | Diagrama de clases de diseño: {clases} clases con atributos y operaciones, asociaciones con navegabilidad y multiplicidades, composición, agregación, generalización y dependencias | `herramientas/dc_larman.py` (derivado de los DSD) |

Cada archivo tiene **una sola página** con el diagrama completo, sin módulos ni recuadros de agrupación: los
elementos van sueltos y graphviz los acomoda a partir de sus relaciones, de modo que los relacionados quedan cerca.

## Cómo se abren

- **draw.io de escritorio** (`/Applications/draw.io.app`): Archivo → Abrir, o `open -a draw.io modelos/drawio/SPLG-DBD.drawio`.
- **Web**: https://app.diagrams.net → Abrir desde → Dispositivo.

Al seleccionar una arista se ven sus dos extremos conectados.

## Exportar a imagen

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png --scale 2 -o salida.png modelos/drawio/SPLG-DBD.drawio
```

## Regenerar y verificar

```bash
python3 herramientas/generar-drawio.py      # reescribe los cuatro .drawio
python3 herramientas/verificar-drawio.py    # 0 relaciones faltantes y 0 aristas sueltas, contra la base, el MC, el DER y el DC
```

Los `.drawio` se regeneran solo a mano con `generar-drawio.py` (el diagrama de clases tarda unos minutos); `generar-sitio.py` no los regenera y avisa si están desactualizados. Hace falta graphviz (`dot`, `fdp`): sin él, `generar-drawio.py` termina con error.
"""


def main():
    solo = {a.upper() for a in sys.argv[1:] if not a.startswith("-")}      # p. ej.: `generar-drawio.py dbd`
    os.makedirs(SAL, exist_ok=True)
    modelo = json.load(open(D + "modelos/base-de-datos/SPLG-modelo.json", encoding="utf-8"))
    resultados = {}
    for nombre, f in (("SPLG-MC", lambda: generar_mc()), ("SPLG-DER", lambda: generar_der(modelo)),
                      ("SPLG-DBD", lambda: generar_dbd(modelo)), ("SPLG-DC", lambda: generar_dc())):
        if solo and nombre.split("-")[1] not in solo:
            continue
        t0 = time.time()
        L = f()
        titulos = {"SPLG-MC": "Modelo conceptual", "SPLG-DER": "DER conceptual", "SPLG-DBD": "Diagrama de base de datos",
                   "SPLG-DC": "Diagrama de clases de diseño"}
        open(SAL + nombre + ".drawio", "w", encoding="utf-8").write(L.xml(titulos[nombre]))
        resultados[nombre] = L
        print(f"  ✓ {nombre}.drawio · {len(L.nodos)} elementos · {len(L.aristas)} aristas · "
              f"{sum(1 for e in L.aristas if e['puntos'] is None)} sin ruta propia · {time.time() - t0:.0f} s", flush=True)
    if len(resultados) < 4:
        return
    dbd = resultados["SPLG-DBD"]
    dc_cl = len([1 for c in resultados["SPLG-DC"].celdas if 'vertex="1"' in c and "container=1" not in c])
    open(SAL + "LEEME.md", "w", encoding="utf-8").write(
        LEEME.replace("{tablas}", str(len(modelo["dbd"]["tablas"])))
             .replace("{fks}", str(len(dbd.aristas))).replace("{fks_comp}", str(sum(1 for t in modelo["dbd"]["tablas"].values() for c in t["columnas"] if c.get("fk_compuesta") for _ in c["fk_compuesta"]))).replace("{clases}", str(dc_cl)))


if __name__ == "__main__":
    main()
