# -*- coding: utf-8 -*-
"""Diagrama único de casos de uso del sistema, en notación UML y estilo Visual Paradigm, en tres columnas:

1. los actores, cada uno una vez, a la altura del centro de sus casos de uso;
2. todos los casos de uso que tienen actor, agrupados por el conjunto de actores;
3. los casos incluidos que ningún actor inicia, a la altura de sus casos base.
Cada asociación es una recta del actor al punto más a la izquierda del óvalo, dentro del canal izquierdo; un actor con
muchos casos reparte sus rectas entre varios puntos del contorno de su figura. Cada relación «include» o «extend» es un
trazo ortogonal por el canal derecho con su propio carril vertical y su rótulo pegado al arranque del trazo; nunca
dos relaciones comparten un tramo: cada una sale y entra por su propio punto del contorno del óvalo (que crece si
tiene muchas). La base de una extensión lleva el compartimiento «puntos de extensión» con los PE-n. Todo dentro de un
solo límite del sistema.
"""
import math, collections
from estilo_vp import SUAVE
from uml_lamina import (_texto, _actor, _cabecera, _lineas, BORDE, TINTA, PLAN_RELLENO, PLAN_BORDE, GROSOR,
                        NOMBRES_SISTEMA_EXTERNO, texto_ovalo, pe_de_base)
from relaciones_cu import pe_id

RX2, RX3 = 175, 165
ANCHO_TXT = 40
GAP = 6
X_ACT = 70
X_LIM = 150
FIG = 134
SALTO_BLOQUE = 700      # salto vertical entre casos de un mismo actor a partir del cual se abre otra copia
CARRIL = 14            # separación entre carriles verticales
ORDEN = ["01", "02", "03", "05", "04", "10", "06", "07", "08", "09"]


def _alto_caso(c, nombre, ancho=ANCHO_TXT):
    ls = [c] + _lineas(nombre, ancho)
    return ls, max(16, 6.2 * len(ls) + 7)


def _asignar_carriles(spans):
    """spans [(y0, y1, largo)]: los más cortos, al carril más cercano; dos tramos que se solapan no comparten carril."""
    orden = sorted(range(len(spans)), key=lambda i: (spans[i][1] - spans[i][0], spans[i][0]))
    carriles, res = [], {}
    for i in orden:
        y0, y1 = spans[i][0], spans[i][1]
        for k, oc in enumerate(carriles):
            if all(y1 + 10 < a0 or y0 - 10 > a1 for a0, a1 in oc): oc.append((y0, y1)); res[i] = k; break
        else:
            carriles.append([(y0, y1)]); res[i] = len(carriles) - 1
    return res, len(carriles)


def _slots(c_y, otros_y, paso, ry):
    """Desplazamientos verticales (sobre el contorno del óvalo) de cada trazo que toca al caso, de arriba abajo,
    ordenados por la altura del otro extremo para que los trazos no se crucen."""
    n = len(otros_y)
    idx = sorted(range(n), key=lambda i: otros_y[i])
    res = [0.0] * n
    for rango, i in enumerate(idx):
        res[i] = (rango - (n - 1) / 2) * paso
    return res


def completo(casos, actores_de, nombres_act, rel, esp, gen, limite_txt, titulo, ref=(), orden=None, notas=None, pie_pe=True, copias=None):
    rank = {k: i for i, k in enumerate(ORDEN)}
    col3 = sorted(c for c in casos if not actores_de.get(c))
    col2 = [c for c in casos if actores_de.get(c)]
    def clave(c):
        r_ = sorted(rank[k] for k in actores_de[c])
        return (round(sum(r_) / len(r_), 2), tuple(r_), c)
    col2.sort(key=orden or clave)
    ref = set(ref)
    rels = list(rel)
    pe_base = pe_de_base(rels)
    info = {}
    n_out = {c: 0 for c in casos}; n_in = {c: 0 for c in casos}
    for (t, a, b, p) in rels:
        n_out[a] += 1; n_in[b] += 1
    paso_de = {c: (12 if n_out[c] >= 2 else 8) for c in casos}
    for c in casos:
        ls = [c] + _lineas(casos[c]["nombre"], ANCHO_TXT)
        n_ls = len(ls) + (3 if c in pe_base else 0)
        ry = max(16, 6.2 * n_ls + 7)
        n_t = n_out[c] + n_in[c]
        ry = max(ry, (n_t - 1) * paso_de[c] / 1.6 + 8)          # el óvalo crece para que cada trazo tenga su punto
        info[c] = (ls, ry)
    x2 = X_LIM + 40 + RX2
    pos = {}
    y = 92
    for c in col2:
        ry = info[c][1]; pos[c] = (x2, y + ry); y += 2 * ry + GAP
    y_fin = y
    # ancla de la columna 3: el caso sin actor (incluido), a la altura media de sus casos base
    vec3 = {c: [] for c in col3}
    for (t, a, b, p) in rels:
        if t == "include" and b in vec3 and a in pos: vec3[b].append(a)
    ide = {}
    for c in col3:
        ys = [pos[v][1] for v in vec3[c]]
        ide[c] = sum(ys) / len(ys) if ys else None
    for _ in range(3):
        for c in col3:
            if ide[c] is None:
                ys = [ide[v] for (t, a, b, p) in rels for v in (a,) if b == c and ide.get(a) is not None]
                ide[c] = sum(ys) / len(ys) if ys else None
    for c in col3:
        if ide[c] is None: ide[c] = 200
    orden3 = sorted(col3, key=lambda c: (ide[c], c))
    cur = 92; y3 = {}
    for c in orden3:
        ry = info[c][1]; cy = max(ide[c], cur + ry); y3[c] = cy; cur = cy + ry + GAP
    y_fin = max(y_fin, cur)
    ypos = lambda c: pos[c][1] if c in pos else y3[c]
    rx_de = lambda c: RX2 if c in pos else RX3
    # puntos de salida y de entrada de cada trazo sobre el contorno de su óvalo: uno por trazo
    inc_de = {c: [] for c in casos}                  # trazos que tocan al caso: (índice de la relación, otro extremo)
    for i, (t, a, b, p) in enumerate(rels):
        inc_de[a].append((i, b)); inc_de[b].append((i, a))
    # --- relaciones: sus tramos verticales y carriles (cada relación su carril; dos tramos solo comparten carril si no se tocan)
    desp = {}
    for c, lst in inc_de.items():
        if not lst: continue
        off = _slots(ypos(c), [ypos(o) for _, o in lst], paso_de[c], info[c][1])
        for (i, o_), d in zip(lst, off):
            desp[(i, c)] = d
    unidades = []        # (clave, [relación], y_min, y_max)
    for i, r in enumerate(rels):
        t, a, b, p = r
        ya_, yb_ = ypos(a) + desp[(i, a)], ypos(b) + desp[(i, b)]
        unidades.append((("rel", i), [r], min(ya_, yb_), max(ya_, yb_)))
    carril, n_car = _asignar_carriles([(u[2], u[3], 0) for u in unidades])
    x_c0 = x2 + RX2 + 100                       # primer carril: deja sitio al rótulo junto al óvalo
    x_c_fin = x_c0 + CARRIL * n_car
    x3 = x_c_fin + 70 + RX3
    r33 = [u for u in unidades if u[1][0][1] in y3 and u[1][0][2] in y3]
    x_der3 = x3 + RX3
    x_lim_der = x_der3 + 40 + CARRIL * (len(r33) + 1) + 30
    W = x_lim_der + 36
    def contorno(c, dy, derecha=True):
        cx = pos[c][0] if c in pos else x3
        rx = rx_de(c); ry = info[c][1]
        dy = max(-ry * 0.92, min(ry * 0.92, dy))
        return (cx + (1 if derecha else -1) * rx * math.sqrt(max(0.0, 1 - (dy / ry) ** 2)), ypos(c) + dy)
    # --- actores a la altura del centro de sus casos; con `copias`, un actor con muchos casos se repite
    # (UML permite repetir la figura del mismo actor) en bloques de casos contiguos, cada copia a la altura de su bloque
    suyos_de = {k: sorted((c for c in col2 if k in actores_de[c]), key=lambda c: pos[c][1]) for k in ORDEN}
    bloque_de = {}                      # (actor, caso) -> número de copia
    yc = {}                             # (actor, copia) -> altura deseada
    def _copias(k, tramos):
        for j, tramo in enumerate(tramos):
            if not tramo: continue
            for c in tramo: bloque_de[(k, c)] = j
            yc[(k, j)] = sum(pos[c][1] for c in tramo) / len(tramo) - 40
    for k in ORDEN:
        su = suyos_de[k]
        if not su or k == esp: continue
        if not copias:
            _copias(k, [su]); continue
        # bloques de casos contiguos: se corta cuando el bloque llega a `copias` casos o cuando el salto al
        # caso siguiente del actor es largo (así ninguna asociación cruza media figura)
        tramos = [[su[0]]]
        for c in su[1:]:
            if len(tramos[-1]) >= copias or pos[c][1] - pos[tramos[-1][-1]][1] > SALTO_BLOQUE: tramos.append([c])
            else: tramos[-1].append(c)
        _copias(k, tramos)
    if suyos_de[esp]:
        # el especializado sigue los bloques del general: cada copia queda junto a la copia de ACT-gen que especializa
        centros = {j: yc[(gen, j)] for (k, j) in yc if k == gen}
        tr = collections.defaultdict(list)
        for c in suyos_de[esp]:
            jg = bloque_de.get((gen, c))
            if jg is None: jg = min(centros, key=lambda j_: abs(centros[j_] - (pos[c][1] - 40))) if centros else 0
            tr[jg].append(c)
        _copias(esp, [tr.get(j, []) for j in range(max(tr) + 1)])
    orden_a = [it for it in sorted(yc, key=lambda it: yc[it]) if it[0] != esp]
    for it in sorted(k_ for k_ in yc if k_[0] == esp):
        ant = [i_ for i_, x_ in enumerate(orden_a) if x_ == (gen, it[1])]
        orden_a.insert(ant[0] + 1 if ant else len(orden_a), it)
    ya = {}; prev = None
    for it in orden_a:
        salto = 215 if (prev is not None and prev[0] == gen and it[0] == esp) else FIG
        ya[it] = max(yc[it], 80 if prev is None else ya[prev] + salto); prev = it
    y_fin = max(y_fin, max(ya.values()) + FIG)
    H = y_fin + 40 + 260
    o = [_cabecera(W, H, titulo)]
    o.append(f'<rect class="limite" data-x="{X_LIM}" data-y="44" data-w="{x_lim_der - X_LIM}" data-h="{y_fin - 44 + 12:.0f}" '
             f'x="{X_LIM}" y="44" width="{x_lim_der - X_LIM}" height="{y_fin - 44 + 12:.0f}" fill="#FFFFFF" stroke="{BORDE}" stroke-width="{GROSOR}"/>')
    o.append(_texto((X_LIM + x_lim_der) / 2, 62, [limite_txt], 12, negrita=True))
    # asociaciones: rectas del actor al punto más a la izquierda del óvalo; el actor las reparte entre varios puntos de su contorno
    for (k, nb_), yk in ya.items():
        suyos = [c for c in suyos_de[k] if bloque_de[(k, c)] == nb_]
        n_s = len(suyos)
        anclas = _anclas_muchas(X_ACT, yk) if n_s > 12 else _anclas(X_ACT, yk)
        for j, c in enumerate(suyos):
            cx, cy = pos[c]; ry = info[c][1]
            ax, ay = anclas[min(len(anclas) - 1, j * len(anclas) // max(1, n_s))] if n_s > 6 else anclas[1]
            o.append(f'<path class="asoc" data-act="{k}" data-cu="{c}" data-rol="{"secundario" if k in NOMBRES_SISTEMA_EXTERNO else "principal"}" '
                     f'd="M{ax:.1f} {ay:.1f} L{cx - RX2:.1f} {cy:.1f}" fill="none" stroke="{TINTA}" stroke-width="0.7" opacity="0.9"/>')
    # relaciones ortogonales: cada una por su carril, con su rótulo pegado al arranque del trazo
    for u, k in zip(unidades, [carril[i] for i in range(len(unidades))]):
        (_, i_rel), rs, ymin, ymax = u
        xl = x_c0 + CARRIL * k
        t, a, b, p = rs[0]
        xa, ya_ = contorno(a, desp[(i_rel, a)], True)
        if b in pos:
            xb, yb = contorno(b, desp[(i_rel, b)], True)
        else:
            xb, yb = contorno(b, desp[(i_rel, b)], False)
        if a in y3 and b in y3:             # entre dos casos de la columna 3: carril a la derecha de la columna
            xa, ya_ = contorno(a, desp[(i_rel, a)], True); xb, yb = contorno(b, desp[(i_rel, b)], True)
            xl2 = x_der3 + 28 + CARRIL * [id(x) for x in r33].index(id(u))
            d = f"M{xa:.1f} {ya_:.1f} H{xl2:.1f} V{yb:.1f} H{xb:.1f}"
        else:
            d = f"M{xa:.1f} {ya_:.1f} H{xl:.1f} V{yb:.1f} H{xb:.1f}"
        o.append(f'<path class="rel" data-tipo="{t}" data-desde="{a}" data-hasta="{b}" d="{d}" fill="none" stroke="{TINTA}" stroke-width="0.8" '
                 f'stroke-dasharray="6 3" marker-end="url(#abre)"/>')
        txt = f"«{t}»" + (f" {pe_id(a, b)}" if t == "extend" else "")
        o.append(f'<g class="etiqueta" data-tipo="{t}" data-desde="{a}" data-hasta="{b}">'
                 + _texto(xa + 6, ya_ - 6, [txt], 10, False, "start", TINTA) + "</g>")
    # óvalos
    for c in col2 + orden3:
        cx, cy = (pos[c] if c in pos else (x3, y3[c])); ry = info[c][1]; rx = RX2 if c in pos else RX3
        plan = casos[c].get("planificado")
        fill, stroke = ("url(#vp)", BORDE) if not plan else (PLAN_RELLENO, PLAN_BORDE)
        dash = ""
        if c in ref:
            fill, stroke, dash = "#FFFFFF", SUAVE, ' stroke-dasharray="5 3"'
        o.append(f'<g class="cu" data-cu="{c}" data-x="{cx:.0f}" data-y="{cy:.0f}"><ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry:.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{GROSOR}"{dash}/>'
                 + texto_ovalo(cx, cy, rx, ry, info[c][0], pe_base.get(c), 11, True, color=SUAVE if c in ref else "#000000") + "</g>")
    for (k, _nb), yk in ya.items():
        o.append(_actor(X_ACT, yk, k, nombres_act[k], ext=k in NOMBRES_SISTEMA_EXTERNO))
    for (k, j_), y_e in ya.items():
        if k == esp and (gen, j_) in ya:
            o.append(f'<path class="gen" data-esp="{esp}" data-gen="{gen}" d="M{X_ACT} {y_e - 10:.1f} V{ya[(gen, j_)] + 9 + 44 + 14 + 40:.1f}" fill="none" stroke="{TINTA}" stroke-width="1" marker-end="url(#hueco)"/>')
    ly = y_fin + 34
    pe_texto = [f"{pe_id(a, b)}  {a} extiende a {b}: cuando {p}" for (t, a, b, p) in rels if t == "extend"]
    pe_texto.sort()
    notas = notas or ["Tres columnas: los actores (cada uno una vez, con una asociación a cada uno de sus casos de uso), los casos de uso que tienen actor y, a la derecha, los casos incluidos que ningún actor inicia.",
             "Asociación actor–caso de uso: línea continua sin punta · «include»: del caso base al incluido · «extend»: del caso que extiende al caso base (línea discontinua, con su punto de extensión PE-n, que figura también en el compartimiento «puntos de extensión» del caso base).",
             f"ACT-{esp} especializa a ACT-{gen} (triángulo hueco); además, cada caso lleva la asociación de todos los actores que el catálogo le asigna, también la de ACT-{esp}.",
             "Con relleno rosado, los casos de uso planificados. Cada «include» y cada «extend» tiene su propio trazo, con el rótulo junto a su arranque."]
    repetidos = sorted({k for (k, j) in ya if j > 0})
    if repetidos:
        notas = notas + [f"Para que se lea, la figura de {', '.join(f'{nombres_act[k]} (ACT-{k})' for k in repetidos)} se repite a lo alto del diagrama (notación UML: es el mismo actor); "
                         "cada copia se une solo a los casos de uso de su bloque, y entre todas cubren la totalidad de sus casos."]
    for tx in notas + (pe_texto if pie_pe else []):
        for lin in _lineas(tx, max(40, int((W - X_LIM - 20) / 5.3))):
            o.append(_texto(X_LIM, ly, [lin], 10, False, "start", TINTA)); ly += 14
        ly += 2
    h_real = max(H - 260 + 40, ly + 20)
    svg = "".join(o)
    svg = svg.replace(f'height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}"', f'height="{h_real:.0f}" viewBox="0 0 {W:.0f} {h_real:.0f}"', 1)
    return svg + "</svg>"


def _anclas(x, y):
    """Puntos del contorno de la figura del actor (centro de la cabeza en (x, y)) desde donde salen las asociaciones:
    la cabeza, la mano, la rodilla y el pie del lado de los casos de uso."""
    r = 9
    return [(x + r, y), (x + 15, y + r + 8), (x + 6, y + r + 33), (x + 13, y + r + 44)]


def _anclas_muchas(x, y, n=14):
    """n puntos repartidos a lo largo del contorno del lado derecho de la figura (cabeza, brazo, tronco, pierna)."""
    return [(x + (9 if i < 2 else 15 if i < 6 else 12), y + i * 53 / (n - 1)) for i in range(n)]
