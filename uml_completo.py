# -*- coding: utf-8 -*-
"""Diagrama único de casos de uso del sistema, en notación UML y estilo Visual Paradigm, en tres columnas:

1. los actores, cada uno una vez, a la altura del centro de sus casos de uso;
2. todos los casos de uso que tienen actor, agrupados por el conjunto de actores;
3. los casos incluidos que ningún actor inicia, a la altura de sus casos base.
Cada asociación es una recta del actor al punto más a la izquierda del óvalo, dentro del canal izquierdo; cada
relación «include» o «extend» es un trazo ortogonal por el canal derecho, con su propio carril vertical (o un tronco
común, si el caso incluido tiene varios casos base). Todo dentro de un solo límite del sistema.
"""
import math
from uml_lamina import (_texto, _actor, _cabecera, _lineas, BORDE, TINTA, PLAN_RELLENO, PLAN_BORDE, GROSOR,
                        NOMBRES_SISTEMA_EXTERNO)

RX2, RX3 = 175, 165
ANCHO_TXT = 40
GAP = 6
X_ACT = 70
X_LIM = 150
FIG = 108
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


def completo(casos, actores_de, nombres_act, rel, esp, gen, limite_txt, titulo):
    rank = {k: i for i, k in enumerate(ORDEN)}
    col3 = sorted(c for c in casos if not actores_de.get(c))
    col2 = [c for c in casos if actores_de.get(c)]
    def clave(c):
        r_ = sorted(rank[k] for k in actores_de[c])
        return (round(sum(r_) / len(r_), 2), tuple(r_), c)
    col2.sort(key=clave)
    info = {c: _alto_caso(c, casos[c]["nombre"]) for c in casos}
    x2 = X_LIM + 40 + RX2
    pos = {}
    y = 92
    for c in col2:
        ry = info[c][1]; pos[c] = (x2, y + ry); y += 2 * ry + GAP
    y_fin = y
    # --- relaciones: sus tramos verticales y carriles
    for_col3 = lambda r: (r[2] if r[0] == "include" else r[1])
    rels = list(rel)
    def extremos(r):
        t, a, b, p = r
        return a, b
    # ancla de la columna 3: el caso sin actor (incluido)
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
    # unidades de carril: un tronco por caso incluido de la columna 3 con varios casos base; una por relación en los demás casos
    unidades = []        # (clave, [relaciones], y_min, y_max)
    por_destino = {}
    for r in rels:
        t, a, b, p = r
        if t == "include" and b in y3 and a in pos: por_destino.setdefault(b, []).append(r)
    usadas = set()
    for b, rs in por_destino.items():
        if len(rs) >= 3:
            ys = [y3[b]] + [pos[r[1]][1] for r in rs]
            unidades.append((("tronco", b), rs, min(ys), max(ys))); usadas.update(rs)
    for r in rels:
        if r in usadas: continue
        t, a, b, p = r
        unidades.append((("rel", r), [r], min(ypos(a), ypos(b)), max(ypos(a), ypos(b))))
    carril, n_car = _asignar_carriles([(u[2], u[3], 0) for u in unidades])
    x_c0 = x2 + RX2 + 100                       # primer carril: deja sitio a la etiqueta junto al óvalo
    x_c_fin = x_c0 + CARRIL * n_car
    x3 = x_c_fin + 70 + RX3
    # relaciones entre casos de la columna 3: carriles a la derecha de la columna 3
    r33 = [u for u in unidades if len(u[1]) == 1 and u[1][0][1] in y3 and u[1][0][2] in y3]
    x_der3 = x3 + RX3
    x_lim_der = x_der3 + 40 + CARRIL * (len(r33) + 1) + 30
    W = x_lim_der + 36
    # --- actores a la altura del centro de sus casos
    yc = {}
    for k in ORDEN:
        ys = [pos[c][1] for c in col2 if k in actores_de[c]]
        if ys: yc[k] = sum(ys) / len(ys) - 40
    orden_a = [k for k in sorted(yc, key=lambda k: yc[k]) if k != esp]
    if esp in yc:
        i = orden_a.index(gen) + 1 if gen in orden_a else len(orden_a)
        orden_a.insert(i, esp)
    ya = {}; prev = None
    for k in orden_a:
        salto = 170 if (prev == gen and k == esp) else FIG
        ya[k] = max(yc[k], 80 if prev is None else ya[prev] + salto); prev = k
    y_fin = max(y_fin, max(ya.values()) + FIG)
    H = y_fin + 40 + 260
    o = [_cabecera(W, H, titulo)]
    o.append(f'<rect class="limite" data-x="{X_LIM}" data-y="44" data-w="{x_lim_der - X_LIM}" data-h="{y_fin - 44 + 12:.0f}" '
             f'x="{X_LIM}" y="44" width="{x_lim_der - X_LIM}" height="{y_fin - 44 + 12:.0f}" fill="#FFFFFF" stroke="{BORDE}" stroke-width="{GROSOR}"/>')
    o.append(_texto((X_LIM + x_lim_der) / 2, 62, [limite_txt], 12, negrita=True))
    # asociaciones: rectas del actor al punto más a la izquierda del óvalo (un desplazamiento mínimo por actor)
    for k, yk in ya.items():
        for c in col2:
            if k in actores_de[c]:
                cx, cy = pos[c]; ry = info[c][1]
                lst_ = actores_de[c]; n_ = len(lst_); s_ = 0.0
                px, py = cx - RX2 * math.sqrt(max(0.0, 1 - s_ * s_)), cy + s_ * ry
                o.append(f'<path class="asoc" data-act="{k}" data-cu="{c}" data-rol="{"secundario" if k in NOMBRES_SISTEMA_EXTERNO else "principal"}" '
                         f'd="M{X_ACT + 24:.1f} {yk + 30:.1f} L{px:.1f} {py:.1f}" fill="none" stroke="{TINTA}" stroke-width="0.7" opacity="0.9"/>')
    # relaciones ortogonales
    n_pe = [0]; pe_texto = []
    por_borde = {}
    def etiqueta(t, p, a, b, x, yv):
        txt = f"«{t}»"
        if t == "extend":
            n_pe[0] += 1; txt += f" PE-{n_pe[0]}"; pe_texto.append(f"PE-{n_pe[0]}  {a} extiende a {b}: cuando {p}")
        wl = len(txt) * 5.6 + 4
        o.append(f'<g class="etiqueta" data-tipo="{t}" data-desde="{a}" data-hasta="{b}">'
                 + _texto(x, yv, [txt], 10, False, "start", TINTA) + "</g>")
    def borde_der(c):
        return (pos[c][0] + RX2, pos[c][1]) if c in pos else (x3 + RX3, y3[c])
    def borde_izq3(c):
        return (x3 - RX3, y3[c])
    desp_arc = {id(u): i for i, u in enumerate(r33)}
    for u, k in zip(unidades, [carril[i] for i in range(len(unidades))]):
        clave_, rs, ymin, ymax = u
        xl = x_c0 + CARRIL * k
        for r in rs:
            t, a, b, p = r
            xa, ya_ = borde_der(a); xb, yb = (borde_der(b) if b in pos else borde_izq3(b))
            if a in y3 and b in y3:             # entre dos casos de la columna 3: carril a la derecha de la columna
                xl2 = x_der3 + 28 + CARRIL * desp_arc[id(u)]
                d = f"M{xa:.1f} {ya_:.1f} H{xl2:.1f} V{yb:.1f} H{xb:.1f}"
                lx, ly = xa + 6, ya_ - 6
            else:
                d = f"M{xa:.1f} {ya_:.1f} H{xl:.1f} V{yb:.1f} H{xb:.1f}"
                lx, ly = xa + 6, ya_ - 6
            o.append(f'<path class="rel" data-tipo="{t}" data-desde="{a}" data-hasta="{b}" d="{d}" fill="none" stroke="{TINTA}" stroke-width="0.8" '
                     f'stroke-dasharray="6 3" marker-end="url(#abre)"/>')
            n_e = por_borde.get(a, 0); por_borde[a] = n_e + 1
            etiqueta(t, p, a, b, lx, ly - 11 * n_e)
    # óvalos
    for c in col2 + orden3:
        cx, cy = (pos[c] if c in pos else (x3, y3[c])); ry = info[c][1]; rx = RX2 if c in pos else RX3
        plan = casos[c].get("planificado")
        fill, stroke = ("url(#vp)", BORDE) if not plan else (PLAN_RELLENO, PLAN_BORDE)
        o.append(f'<g class="cu" data-cu="{c}" data-x="{cx:.0f}" data-y="{cy:.0f}"><ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry:.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{GROSOR}"/>' + _texto(cx, cy, info[c][0], 11, True) + "</g>")
    for k, yk in ya.items():
        o.append(_actor(X_ACT, yk, k, nombres_act[k], ext=k in NOMBRES_SISTEMA_EXTERNO))
    if esp in ya and gen in ya:
        o.append(f'<path class="gen" data-esp="{esp}" data-gen="{gen}" d="M{X_ACT} {ya[esp] - 10:.1f} V{ya[gen] + 9 + 44 + 14 + 40:.1f}" fill="none" stroke="{TINTA}" stroke-width="1" marker-end="url(#hueco)"/>')
    ly = y_fin + 34
    notas = ["Tres columnas: los actores (cada uno una vez, con una asociación a cada uno de sus casos de uso), los casos de uso que tienen actor y, a la derecha, los casos incluidos que ningún actor inicia.",
             "Asociación actor–caso de uso: línea continua sin punta · «include»: del caso base al incluido · «extend»: del caso que extiende al caso base (línea discontinua, con su punto de extensión PE-n).",
             f"ACT-{esp} especializa a ACT-{gen} (triángulo hueco); además, cada caso lleva la asociación de todos los actores que el catálogo le asigna, también la de ACT-{esp}.",
             "Con relleno rosado, los casos de uso planificados. Cuando varios casos incluyen a uno, sus flechas comparten un carril (tronco)."]
    for tx in notas + pe_texto:
        for lin in _lineas(tx, 150):
            o.append(_texto(X_LIM, ly, [lin], 10, False, "start", TINTA)); ly += 14
        ly += 2
    h_real = max(H - 260 + 40, ly + 20)
    svg = "".join(o)
    svg = svg.replace(f'height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}"', f'height="{h_real:.0f}" viewBox="0 0 {W:.0f} {h_real:.0f}"', 1)
    return svg + "</svg>"
