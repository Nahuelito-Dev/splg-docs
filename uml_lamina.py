# -*- coding: utf-8 -*-
"""Dibuja los diagramas de casos de uso (por subsistema y por lámina) y el mapa de navegación.

Formato único, en el estilo Visual Paradigm de `estilo_vp.py`:

  - los actores, en una sola columna a la izquierda y fuera del límite del sistema;
  - a la derecha, el límite del sistema con el nombre arriba y, adentro, todos los casos de
    uso apilados en una sola columna (un recuadro por subsistema cuando hay más de uno);
  - las relaciones «include» y «extend» entre los casos, a la derecha de la columna, como
    arcos de línea discontinua con el estereotipo entre comillas angulares.

Se componen acá, con una disposición fija, y no con Graphviz: el motor no respeta una
columna de casos ni una de actores. Cada elemento lleva atributos data-* para que
verificar-conformidad.py pueda comprobar el dibujo sin mirarlo: cada actor una sola vez y
fuera del límite, cada caso con su actor y las relaciones iguales a las del catálogo.
"""
import math, re
from html import escape

from estilo_vp import (FUENTE, FONDO, RELLENO, RELLENO_CLARO, BORDE, TINTA, SUAVE,
                       PLAN_RELLENO, PLAN_BORDE, GROSOR)

NOMBRES_SISTEMA_EXTERNO = ("06", "07", "08", "09")


def _lineas(txt, ancho):
    out, l = [], ""
    for w in txt.split():
        if len(l) + len(w) + 1 > ancho and l:
            out.append(l); l = w
        else:
            l = (l + " " + w).strip()
    if l:
        out.append(l)
    return out


def _texto(x, y, lineas, fs, negrita_primera=False, ancla="middle", color="#000000", interlinea=None, negrita=False):
    il = interlinea or fs * 1.2
    y0 = y - il * (len(lineas) - 1) / 2
    partes = []
    for i, t in enumerate(lineas):
        peso = ' font-weight="bold"' if (negrita or (negrita_primera and i == 0)) else ""
        partes.append(f'<text x="{x:.1f}" y="{y0 + i * il:.1f}" font-size="{fs}" text-anchor="{ancla}" '
                      f'dominant-baseline="central" fill="{color}"{peso}>{escape(t)}</text>')
    return "".join(partes)


def _actor(x, y, cod, nombre, ext=False, fs=11):
    """Figura de palito con el nombre debajo. (x, y) es el centro de la cabeza."""
    r = 9
    g = [f'<g class="actor" data-act="{cod}" data-x="{x:.0f}" data-y="{y:.0f}">']
    g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{RELLENO_CLARO}" stroke="{BORDE}" stroke-width="{GROSOR}"/>')
    g.append(f'<path d="M{x:.1f} {y + r:.1f} V{y + r + 24:.1f} M{x - 15:.1f} {y + r + 8:.1f} H{x + 15:.1f} '
             f'M{x:.1f} {y + r + 24:.1f} L{x - 13:.1f} {y + r + 44:.1f} M{x:.1f} {y + r + 24:.1f} L{x + 13:.1f} {y + r + 44:.1f}" '
             f'stroke="{BORDE}" stroke-width="{GROSOR}" fill="none"/>')
    ls = ([f"«sistema externo»"] if ext else []) + _lineas(nombre, 18) + [f"(ACT-{cod})"]
    g.append(_texto(x, y + r + 44 + 14 + (len(ls) - 1) * fs * 0.6, ls, fs))
    g.append("</g>")
    return "".join(g)


def _defs():
    return (f'<defs>'
            f'<marker id="abre" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
            f'<path d="M0 1 L9 5 L0 9" fill="none" stroke="{TINTA}" stroke-width="1"/></marker>'
            f'<marker id="hueco" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto">'
            f'<path d="M1 1 L11 6 L1 11 Z" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1"/></marker>'
            f'<linearGradient id="vp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RELLENO_CLARO}"/>'
            f'<stop offset="1" stop-color="{RELLENO}"/></linearGradient></defs>')


def _cabecera(w, h, titulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'font-family="{FUENTE}">' + _defs() +
            f'<rect width="100%" height="100%" fill="{FONDO}"/>' + _texto(w / 2, 22, [titulo], 14, negrita=True))


def _borde_elipse(cx, cy, rx, ry, hacia_x, hacia_y):
    dx, dy = hacia_x - cx, hacia_y - cy
    if dx == 0 and dy == 0:
        return cx, cy
    t = 1.0 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx * t, cy + dy * t


HUB_MIN = 4                             # cuántos casos tienen que apuntar a uno para dibujar el tronco


def _cruces(orden, arcos):
    """Cantidad de pares de arcos que se cruzan (extremos entrelazados) y largo total, en posiciones."""
    pos = {cu: i for i, cu in enumerate(orden)}
    segs = []
    for a, b in arcos:
        if a in pos and b in pos:
            segs.append(tuple(sorted((pos[a], pos[b]))))
    c = 0
    for i in range(len(segs)):
        a0, a1 = segs[i]
        for j in range(i + 1, len(segs)):
            b0, b1 = segs[j]
            if len({a0, a1, b0, b1}) < 4:
                continue
            if (a0 < b0 < a1 < b1) or (b0 < a0 < b1 < a1):
                c += 1
    return c, sum(b - a for a, b in segs)


def _afinar(casos, clave, rel, paquetes):
    """Reordena los casos de un mismo grupo de actores para que los arcos de «include» y «extend» queden
    cortos y sin cruzarse. El orden entre grupos no cambia: solo se permutan los casos con la misma clave."""
    arcos = [(r[1], r[2]) for r in rel]
    mios = set(casos)
    arcos = [(a, b) for a, b in arcos if a in mios and b in mios]
    if len(arcos) < 2:
        return casos
    grupos, k = [], None
    for cu in casos:
        kk = clave(cu)[:2]
        if kk != k:
            grupos.append([]); k = kk
        grupos[-1].append(cu)
    orden = [cu for g in grupos for cu in g]
    mejor = _cruces(orden, arcos)
    rangos, i = [], 0
    for g in grupos:
        rangos.append((i, i + len(g))); i += len(g)
    mejoro = True
    while mejoro:
        mejoro = False
        for (a, b) in rangos:
            if b - a < 2:
                continue
            for i in range(a, b):
                for j in range(a, b):
                    if i == j:
                        continue
                    cand = orden[:]
                    cu = cand.pop(i); cand.insert(j, cu)
                    v = _cruces(cand, arcos)
                    if (v[0] * 100 + v[1]) < (mejor[0] * 100 + mejor[1]):
                        orden, mejor, mejoro = cand, v, True
    return orden


def columna(casos, paquetes, nombres_act, actores, asoc, rel, esp, gen, limite_txt, titulo,
            secundarios=(), factorizados=None, ref_ss=None, leyenda=None, fuera_de_lamina=False, ref_lateral=False,
            grupo_de=None, centro_actor=None, nota_stub=None, compacto=False, sec_a_la_derecha=False):
    """Un diagrama de dos columnas.

    casos        {cu: {"nombre", "ss", "planificado"?}}
    paquetes     [{"id", "titulo", "casos": [cu...]}] en el orden en que se apilan
    nombres_act  {"01": "Cliente", ...}
    actores      códigos de los actores que se dibujan, en el orden de arriba abajo
    asoc         [(actor, cu, "principal"|"secundario")]
    rel          [(tipo, desde, hasta, punto|None)]
    """
    # fuera_de_lamina: los casos de otras láminas no se dibujan; una relación con ellos termina en un
    # trazo corto con el código del caso y el número de su lámina (como un conector de página)
    stub_rel = []
    if fuera_de_lamina and ref_ss:
        ref_casos = {c for p in paquetes if p["id"] == ref_ss for c in p["casos"]}
        paquetes = [p for p in paquetes if p["id"] != ref_ss]
        asoc = [x for x in asoc if x[1] not in ref_casos]
        stub_rel = [r for r in rel if (r[1] in ref_casos) != (r[2] in ref_casos)]
        rel = [r for r in rel if r[1] not in ref_casos and r[2] not in ref_casos]
        ref_ss = None
    # grupo_de: {caso: grupo}. Una relación entre casos de grupos distintos no se dibuja como arco: termina en
    # un trazo corto con el código del otro caso. centro_actor: {actor: [casos]}, para ubicar cada actor a la
    # altura del centro de su grupo.
    if grupo_de:
        stub_rel = [r for r in rel if grupo_de[r[1]] != grupo_de[r[2]]]
        rel = [r for r in rel if grupo_de[r[1]] == grupo_de[r[2]]]
    # ref_lateral: los casos de referencia van en una segunda columna a la derecha, cada uno a la altura de
    # los casos que lo relacionan, con un recuadro común y un título
    ref_lat = set()
    if ref_lateral and ref_ss:
        ref_lat = {c for p in paquetes if p["id"] == ref_ss for c in p["casos"]}
        paquetes = [p for p in paquetes if p["id"] != ref_ss]
    RX, RYMIN = (200, 17) if compacto else (140, 20)   # semiejes de la elipse (el alto crece con las líneas de texto)
    GAP = 6 if compacto else 9          # entre elipses
    PAD, TIT = 16, 30                   # relleno del recuadro de un subsistema y alto de su título
    SEP = 20                            # entre recuadros
    ANCHO_TXT = 42 if compacto else 28
    X_ACT = 85                          # centro de la columna de actores
    X_LIM = 235                         # borde izquierdo del límite del sistema
    Y0 = 52                             # donde empieza el límite

    # los casos de cada recuadro, agrupados por actor en el orden de la columna de actores: así las
    # asociaciones casi no se cruzan; los que comparten varios actores quedan entre sus grupos
    orden_act = {k: i for i, k in enumerate(actores)}
    por_caso = {}
    for (k, cu, rol) in asoc:
        if k in orden_act: por_caso.setdefault(cu, []).append(orden_act[k])
    def clave(cu):
        ix = por_caso.get(cu)
        if not ix: return (99, 99, cu)
        return (sum(ix) / len(ix), min(ix), cu)
    paquetes = [dict(p, casos=_afinar(sorted(p["casos"], key=clave), clave, rel, paquetes)) for p in paquetes]
    # alto de cada caso según las líneas de su nombre
    info = {}
    for cu, c in casos.items():
        ls = ([cu] if not cu.startswith("F-") else []) + _lineas(c["nombre"], ANCHO_TXT)
        info[cu] = {"ls": ls, "ry": max(RYMIN, 6.2 * len(ls) + 8)}
    pos = {}
    y = Y0 + 34                         # debajo del nombre del sistema
    cajas = []
    for p in paquetes:
        y_ini = y
        y += TIT + 4
        for cu in p["casos"]:
            ry = info[cu]["ry"]
            pos[cu] = (X_LIM + 20 + PAD + RX, y + ry)
            y += 2 * ry + GAP
        y += PAD - GAP + 4
        cajas.append((p, y_ini, y))
        y += SEP
    y_fin = y - SEP

    # arcos de las relaciones, a la derecha de la columna: se reparten en carriles para que
    # los que cubren tramos que se superponen no se monten
    x_der = X_LIM + 20 + PAD + 2 * RX
    rel_ref = [r for r in rel if r[1] in ref_lat or r[2] in ref_lat]
    rel = [r for r in rel if r[1] not in ref_lat and r[2] not in ref_lat] if ref_lat else rel
    rel_num = rel + (rel_ref if ref_lat else []) + (stub_rel if grupo_de else [])   # para numerar los puntos de extensión
    cadenas = sorted(rel, key=lambda r: abs(pos[r[1]][1] - pos[r[2]][1]) if r[1] in pos and r[2] in pos else 0)
    carriles = []                       # cada carril: lista de (y0, y1)
    asigna = {}
    # un caso incluido (o extendido) por muchos otros se dibuja como un tronco: cada caso base llega con un
    # tramo corto a un trazo vertical común, que entra una sola vez en el caso incluido
    entran = {}
    for (t, a, b, _) in rel:
        if a in pos and b in pos:
            entran.setdefault((t, b), []).append(a)
    hubs = {k: v for k, v in entran.items() if len(v) >= HUB_MIN}
    for (t, b), bases in sorted(hubs.items(), key=lambda kv: -len(kv[1])):
        ys = [pos[b][1]] + [pos[a][1] for a in bases]
        y0, y1 = min(ys), max(ys)
        for k, ocupados in enumerate(carriles):
            if all(y1 + 6 < o0 or y0 - 6 > o1 for o0, o1 in ocupados):
                ocupados.append((y0, y1)); asigna[("hub", t, b)] = k; break
        else:
            carriles.append([(y0, y1)]); asigna[("hub", t, b)] = len(carriles) - 1
    for r in cadenas:
        t, a, b, _ = r
        if a not in pos or b not in pos or (t, b) in hubs:
            continue
        y0, y1 = sorted((pos[a][1], pos[b][1]))
        for k, ocupados in enumerate(carriles):
            if all(y1 + 6 < o0 or y0 - 6 > o1 for o0, o1 in ocupados):
                ocupados.append((y0, y1)); asigna[(t, a, b)] = k; break
        else:
            carriles.append([(y0, y1)]); asigna[(t, a, b)] = len(carriles) - 1
    ancho_arcos = 50 + 16 * len(carriles) + 40
    def _etiqueta_fuera(r):
        tt, a_, b_, _p = r
        if grupo_de:
            pe_ = f" PE-{[x for x in rel_num if x[0] == 'extend'].index(r) + 1}" if tt == "extend" else ""
            return f"«{tt}»{pe_} {b_}"
        otro = a_ if a_ not in pos else b_
        m_ = re.search(r"\((lámina \d+)\)", casos[otro]["nombre"])
        return f"«{tt}» {otro}" + (f" ({m_.group(1)})" if m_ else "")
    if sec_a_la_derecha:
        ancho_arcos = max(ancho_arcos, 36 + 16 * len(carriles) + 14 + int(max(len(v) for v in nombres_act.values()) * 5.8) + 40)
    if stub_rel:
        ancho_arcos = max(ancho_arcos, 36 + (16 * len(carriles) if grupo_de else 0) + 14 + int(max(len(_etiqueta_fuera(r)) for r in stub_rel) * 5.4))
    x_ref = None
    if ref_lat:
        x_ref = x_der + ancho_arcos + 40 + RX
        relac = {c: [pos[(r[2] if r[1] == c else r[1])][1] for r in rel_ref if c in (r[1], r[2])] for c in ref_lat}
        orden_ref = sorted(ref_lat, key=lambda c: (sum(relac[c]) / len(relac[c]) if relac[c] else 0, c))
        y_prev = Y0 + 70
        for c in orden_ref:
            ry = info[c]["ry"]
            ideal_y = sum(relac[c]) / len(relac[c]) if relac[c] else y_prev
            yc = max(ideal_y, y_prev + ry)
            pos[c] = (x_ref, yc)
            y_prev = yc + ry + GAP
        y_fin = max(y_fin, y_prev + PAD)
        ancho_arcos = (x_ref + RX + 30) - x_der
    W_LIM = (x_der - X_LIM) + ancho_arcos
    H_LIM = y_fin - Y0 + 24
    LEY = 130 if leyenda is not False else 20
    W = max(X_LIM + W_LIM + 30, 820)

    # posición de los actores: a la altura media de sus asociaciones, sin pisarse
    asoc_de = {k: [pos[c][1] for (a, c, r) in asoc if a == k and c in pos] for k in actores}
    for k_, cs_ in (centro_actor or {}).items():
        if k_ in asoc_de and cs_:
            ys_ = [pos[c][1] for c in cs_ if c in pos]
            asoc_de[k_] = [(min(ys_) + max(ys_)) / 2]
    ideal = {k: (sum(v) / len(v) if v else Y0 + 80) for k, v in asoc_de.items()}
    if sec_a_la_derecha and centro_actor:
        for k_ in actores:
            if k_ not in centro_actor:
                ideal[k_] = y_fin + 40 + actores.index(k_)         # los actores externos sin grupo van al final
    actores = sorted(actores, key=lambda k: ideal[k])
    if esp in actores and gen in actores:
        actores.remove(esp); actores.insert(actores.index(gen) + 1, esp)
    SALTO = 120
    SALTO_GEN = 200                    # entre el actor general y el que lo especializa
    apos = {}
    prev = None
    for k in actores:
        sep = SALTO_GEN if (prev is not None and esp in actores and prev == gen and k == esp) else SALTO
        v = ideal[k] if prev is None else max(ideal[k], apos[prev] + sep)
        apos[k] = v; prev = k
    H = max(Y0 + H_LIM + 30 + LEY, max(apos.values(), default=0) + 120 + LEY)

    o = [_cabecera(W, H, titulo)]
    o.append(f'<rect class="limite" data-x="{X_LIM}" data-y="{Y0}" data-w="{W_LIM:.0f}" data-h="{H_LIM:.0f}" '
             f'x="{X_LIM}" y="{Y0}" width="{W_LIM:.0f}" height="{H_LIM:.0f}" fill="#FFFFFF" stroke="{BORDE}" stroke-width="{GROSOR}"/>')
    o.append(_texto(X_LIM + W_LIM / 2, Y0 + 20, [limite_txt], 12, negrita=True))

    # recuadros de subsistema (si hay más de uno o uno de referencia)
    for p, y0, y1 in cajas:
        ref = p["id"] == ref_ss
        if len([q for q in paquetes if q["id"] != ref_ss]) > 1 or ref or ref_lateral:
            o.append(f'<g class="paquete" data-pq="{p["id"]}" data-n="{len(p["casos"])}">'
                     f'<rect x="{X_LIM + 10}" y="{y0}" width="{x_der - X_LIM - 0 + 10 - 10 + 0:.0f}" height="{y1 - y0:.0f}" '
                     f'fill="{"#FFFFFF" if ref else "#F4F8FC"}" stroke="{SUAVE if ref else BORDE}" '
                     f'stroke-width="{GROSOR}"{" stroke-dasharray=\"5 3\"" if ref else ""}/>'
                     + (_texto(X_LIM + 10 + (x_der - X_LIM) - 10, y0 + 14, [p["titulo"]], 11, False, "end", TINTA, negrita=True) if grupo_de
                        else _texto(X_LIM + 20, y0 + 14, [p["titulo"]], 11, False, "start", SUAVE if ref else TINTA, negrita=True))
                     + "</g>")

    def _a_la_derecha(k, cu, rol):
        return rol == "secundario" or bool(grupo_de and grupo_de.get(cu, "").split("|")[0] != k)
    rol_de = {(k, cu): rol for (k, cu, rol) in asoc}
    # asociaciones actor - caso (línea fina, sin punta: es una asociación)
    for (k, cu, rol) in asoc:
        if k not in apos or cu not in pos:
            continue
        if sec_a_la_derecha and _a_la_derecha(k, cu, rol):
            continue                      # los actores externos y los de otro grupo se indican con un trazo corto a la derecha del caso
        xa, ya = X_ACT + 24, apos[k] + 30
        cx, cy = pos[cu]
        ry = info[cu]["ry"]
        _lst = sorted({a_ for (a_, c_, r_) in asoc if c_ == cu and a_ in apos and not (sec_a_la_derecha and _a_la_derecha(a_, c_, r_))})
        _n = len(_lst); _s = ((_lst.index(k) if k in _lst else 0) - (_n - 1) / 2) * 0.5
        tx, ty = cx - RX * math.sqrt(max(0.0, 1 - _s * _s)), cy + _s * ry          # un punto del borde por actor
        o.append(f'<path class="asoc" data-act="{k}" data-cu="{cu}" data-rol="{rol}" '
                 f'd="M{xa:.1f} {ya:.1f} L{tx:.1f} {ty:.1f}" fill="none" stroke="{TINTA}" stroke-width="0.8" opacity="0.85"/>')

    # relaciones entre casos
    for (t, a, b, punto) in rel:
        if a not in pos or b not in pos:
            continue
        (xa, ya), (xb, yb) = pos[a], pos[b]
        if (t, b) in hubs:
            xt = x_der + 36 + 16 * asigna[("hub", t, b)]
            pa = _borde_elipse(xa, ya, RX, info[a]["ry"], xa + 1000, ya)
            o.append(f'<path class="rel" data-tipo="{t}" data-desde="{a}" data-hasta="{b}" '
                     f'd="M{pa[0]:.1f} {pa[1]:.1f} H{xt:.1f}" fill="none" stroke="{TINTA}" stroke-width="0.8" '
                     f'stroke-dasharray="6 3"/>')
            continue
        k = asigna[(t, a, b)]
        d = 36 + 16 * k
        xs = xa + RX * math.sqrt(max(0.0, 1 - ((0) / 1) ** 2))
        # el arco sale del borde derecho de cada elipse
        pa = _borde_elipse(xa, ya, RX, info[a]["ry"], xa + 1000, ya)
        pb = _borde_elipse(xb, yb, RX, info[b]["ry"], xb + 1000, yb)
        o.append(f'<path class="rel" data-tipo="{t}" data-desde="{a}" data-hasta="{b}" '
                 f'd="M{pa[0]:.1f} {pa[1]:.1f} C{pa[0] + d:.1f} {pa[1]:.1f} {pb[0] + d:.1f} {pb[1]:.1f} {pb[0]:.1f} {pb[1]:.1f}" '
                 f'fill="none" stroke="{TINTA}" stroke-width="0.8" stroke-dasharray="6 3" marker-end="url(#abre)"/>')

    # relaciones con los casos de referencia de la segunda columna
    for (tt, a_, b_, _p) in rel_ref if ref_lat else []:
        (xa_, ya_), (xb_, yb_) = pos[a_], pos[b_]
        if a_ in ref_lat:
            pa_ = _borde_elipse(xa_, ya_, RX, info[a_]["ry"], xa_ - 1000, ya_)
            pb_ = _borde_elipse(xb_, yb_, RX, info[b_]["ry"], xb_ + 1000, yb_)
        else:
            pa_ = _borde_elipse(xa_, ya_, RX, info[a_]["ry"], xa_ + 1000, ya_)
            pb_ = _borde_elipse(xb_, yb_, RX, info[b_]["ry"], xb_ - 1000, yb_)
        dx_ = abs(pb_[0] - pa_[0]) * 0.5
        sg_ = 1 if pb_[0] > pa_[0] else -1
        o.append(f'<path class="rel" data-tipo="{tt}" data-desde="{a_}" data-hasta="{b_}" '
                 f'd="M{pa_[0]:.1f} {pa_[1]:.1f} C{pa_[0] + sg_ * dx_:.1f} {pa_[1]:.1f} {pb_[0] - sg_ * dx_:.1f} {pb_[1]:.1f} '
                 f'{pb_[0]:.1f} {pb_[1]:.1f}" fill="none" stroke="{TINTA}" stroke-width="0.8" stroke-dasharray="6 3" '
                 f'marker-end="url(#abre)"/>')
    if ref_lat:
        y_top = min(pos[c][1] - info[c]["ry"] for c in ref_lat)
        o.append(f'<rect x="{x_ref - RX - 14}" y="{Y0 + 34}" width="{2 * RX + 28}" height="{y_fin - Y0 - 34 - 6:.0f}" fill="none" '
                 f'stroke="{SUAVE}" stroke-width="{GROSOR}" stroke-dasharray="5 3"/>')
        o.append(_texto(x_ref, Y0 + 50, ["Casos de uso de otros actores", "(solo como referencia)"], 11, False, "middle", SUAVE, negrita=True))
        rot = {}
        for (tt, a_, b_, _p) in rel_ref:
            c_ = a_ if a_ in ref_lat else b_
            if (tt, c_) in rot: continue
            rot[(tt, c_)] = True
            k_ = sum(1 for (q, w_) in rot if w_ == c_) - 1
            txt = f"«{tt}»" + (f" PE-{[r for r in rel_num if r[0] == 'extend'].index((tt, a_, b_, _p)) + 1}" if tt == "extend" else "")
            wl = len(txt) * 5.6 + 6
            lx, ly_ = x_ref - RX - 44, pos[c_][1] - 6 + 13 * k_
            o.append(f'<g class="etiqueta" data-tipo="{tt}" data-hasta="{b_}"><rect x="{lx - wl / 2:.1f}" y="{ly_ - 7:.1f}" width="{wl:.1f}" height="14" fill="#FFFFFF"/>'
                     + _texto(lx, ly_, [txt], 10, False, "middle", TINTA) + "</g>")

    # relaciones con casos de otras láminas (o de otro grupo) y, si se pide, los actores externos
    por_caso = {}
    for r in stub_rel:
        por_caso.setdefault(r[1] if r[1] in pos else r[2], []).append(("rel", r))
    if sec_a_la_derecha:
        for (k_, cu_, rol_) in asoc:
            if _a_la_derecha(k_, cu_, rol_) and cu_ in pos and k_ in apos:
                por_caso.setdefault(cu_, []).append(("sec", k_))
    for c_, lst in por_caso.items():
        cx_, cy_ = pos[c_]
        for i_, (tipo_, r) in enumerate(lst):
            y_ = cy_ + (i_ - (len(lst) - 1) / 2) * 14
            bx_ = _borde_elipse(cx_, cy_, RX, info[c_]["ry"], cx_ + 1000, y_)[0]
            x_fin = x_der + 36 + (16 * len(carriles) if grupo_de else 0)
            if tipo_ == "sec":
                o.append(f'<path class="asoc" data-act="{r}" data-cu="{c_}" data-rol="{rol_de.get((r, c_), "secundario")}" '
                         f'd="M{bx_:.1f} {y_:.1f} H{x_fin:.1f}" fill="none" stroke="{TINTA}" stroke-width="0.8"/>')
                o.append(_texto(x_fin + 6, y_ + 3, [f"{nombres_act[r]} (ACT-{r})"], 9, False, "start", TINTA, negrita=True))
                continue
            tt, a_, b_, _p = r
            d_ = f"M{bx_:.1f} {y_:.1f} H{x_fin:.1f}" if a_ in pos else f"M{x_fin:.1f} {y_:.1f} H{bx_:.1f}"
            o.append(f'<path class="rel" data-tipo="{tt}" data-desde="{a_}" data-hasta="{b_}" d="{d_}" fill="none" '
                     f'stroke="{TINTA}" stroke-width="0.8" stroke-dasharray="6 3" marker-end="url(#abre)"/>')
            o.append(_texto(x_fin + 6, y_ + 3, [_etiqueta_fuera(r)], 9, False, "start", TINTA))

    # troncos de los casos incluidos por muchos
    for (t, b), bases in hubs.items():
        xt = x_der + 36 + 16 * asigna[("hub", t, b)]
        yb = pos[b][1]
        pb = _borde_elipse(pos[b][0], yb, RX, info[b]["ry"], pos[b][0] + 1000, yb)
        arriba = [pos[a][1] for a in bases if pos[a][1] < yb]
        abajo = [pos[a][1] for a in bases if pos[a][1] > yb]
        if arriba:
            o.append(f'<path class="troncal" d="M{xt:.1f} {min(arriba):.1f} V{yb:.1f} H{pb[0]:.1f}" fill="none" '
                     f'stroke="{TINTA}" stroke-width="0.8" stroke-dasharray="6 3" marker-end="url(#abre)"/>')
        if abajo:
            fin = f' H{pb[0]:.1f}" marker-end="url(#abre)' if not arriba else ""
            o.append(f'<path class="troncal" d="M{xt:.1f} {max(abajo):.1f} V{yb:.1f}{fin}" fill="none" '
                     f'stroke="{TINTA}" stroke-width="0.8" stroke-dasharray="6 3"/>')

    # casos de uso
    pe = {}
    for i, (t, a, b, punto) in enumerate([r for r in rel_num if r[0] == "extend"], 1):
        pe.setdefault(b, []).append(f"PE-{i}")
    for cu, (cx, cy) in pos.items():
        ry = info[cu]["ry"]
        c = casos[cu]
        ref = c.get("ss") == ref_ss
        if ref:
            fill, stroke, dash = "#FFFFFF", SUAVE, ' stroke-dasharray="5 3"'
        elif c.get("planificado"):
            fill, stroke, dash = PLAN_RELLENO, PLAN_BORDE, ""
        elif cu.startswith("F-"):
            fill, stroke, dash = "#F2F4F6", SUAVE, ""
        else:
            fill, stroke, dash = "url(#vp)", BORDE, ""
        o.append(f'<g class="cu" data-cu="{cu}" data-x="{cx:.0f}" data-y="{cy:.0f}">'
                 f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{RX}" ry="{ry:.1f}" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="{GROSOR}"{dash}/>'
                 + _texto(cx, cy, info[cu]["ls"], 11, bool(not cu.startswith("F-")), color="#000000" if not ref else SUAVE)
                 + "</g>")

    # etiquetas de las relaciones (sobre un fondo blanco, en el ápice del arco)
    puestas = []
    ya_rotulado = set()
    for (t, a, b, punto) in sorted(rel, key=lambda r: asigna.get((r[0], r[1], r[2]), 0)):
        if a not in pos or b not in pos:
            continue
        if (t, b) in hubs:
            if (t, b) in ya_rotulado:
                continue
            ya_rotulado.add((t, b))
            xt = x_der + 36 + 16 * asigna[("hub", t, b)]
            txt = f"«{t}»"
            wl = len(txt) * 5.6 + 6
            my = pos[b][1] + (18 if any(pos[x][1] < pos[b][1] for x in hubs[(t, b)]) else -18)
            r = (xt - wl / 2, my - 7, xt + wl / 2, my + 7)
            puestas.append(r)
            o.append(f'<g class="etiqueta" data-tipo="{t}" data-hasta="{b}">'
                     f'<rect x="{r[0]:.1f}" y="{r[1]:.1f}" width="{wl:.1f}" height="14" fill="#FFFFFF"/>'
                     + _texto(xt, my, [txt], 10, False, "middle", TINTA) + "</g>")
            continue
        k = asigna[(t, a, b)]
        d = 36 + 16 * k
        ya, yb = pos[a][1], pos[b][1]
        xa_ = pos[a][0] + RX
        xb_ = pos[b][0] + RX
        mx = (xa_ + xb_) / 2 + 0.75 * d + (46 if t == "extend" else 0)
        my = (ya + yb) / 2
        txt = f"«{t}»" + (f" PE-{[r for r in rel_num if r[0]=='extend'].index((t, a, b, punto)) + 1}" if t == "extend" else "")
        wl = len(txt) * 5.6 + 6
        r = (mx - wl / 2, my - 7, mx + wl / 2, my + 7)
        for q in puestas:
            if not (r[2] < q[0] - 1 or q[2] + 1 < r[0] or r[3] < q[1] - 1 or q[3] + 1 < r[1]):
                my += 15; r = (mx - wl / 2, my - 7, mx + wl / 2, my + 7)
        puestas.append(r)
        o.append(f'<g class="etiqueta" data-tipo="{t}" data-desde="{a}" data-hasta="{b}">'
                 f'<rect x="{r[0]:.1f}" y="{r[1]:.1f}" width="{wl:.1f}" height="14" fill="#FFFFFF"/>'
                 + _texto(mx, my, [txt], 10, False, "middle", TINTA) + "</g>")

    # actores
    for k in actores:
        o.append(_actor(X_ACT, apos[k], k, nombres_act[k], ext=k in NOMBRES_SISTEMA_EXTERNO))
    if esp in apos and gen in apos:
        o.append(f'<path class="gen" data-esp="{esp}" data-gen="{gen}" '
                 f'd="M{X_ACT} {apos[esp] - 10:.1f} V{apos[gen] + 9 + 44 + 14 + 40:.1f}" '
                 f'fill="none" stroke="{TINTA}" stroke-width="1" marker-end="url(#hueco)"/>')

    # leyenda y puntos de extensión
    ly = max(Y0 + H_LIM, max(apos.values(), default=0) + 120) + 22
    if leyenda is not False:
        o.append('<g class="leyenda">')
        notas = ["Asociación actor–caso de uso: línea continua sin punta · «include»: del caso base al incluido · "
                 "«extend»: de la extensión al caso base (línea discontinua).",
                 f"ACT-{esp} especializa a ACT-{gen} (triángulo hueco); además, cada caso de uso lleva la asociación de todos los actores que el catálogo le asigna, también la de ACT-{esp}."]
        if any(c.get("planificado") for c in casos.values()):
            notas.append("Con relleno rosado, los casos de uso planificados.")
        if ref_ss:
            notas.append("Con borde discontinuo, los casos de uso de otro diagrama, solo como referencia.")
        if stub_rel:
            notas.append(nota_stub or "Una relación con un caso de uso de otra lámina termina en un trazo corto con el código de ese caso y el número de su lámina.")
        for tx in notas:
            for lin in _lineas(tx, int((W - X_LIM - 20) / 5.3)):
                o.append(_texto(X_LIM, ly, [lin], 10, False, "start", TINTA)); ly += 14
            ly += 2
        exts = [r for r in rel_num if r[0] == "extend" and r[1] in pos and r[2] in pos]
        for i, (t, a, b, punto) in enumerate(exts, 1):
            na = (factorizados or {}).get(a) or a
            for lin in _lineas(f"PE-{i}  {na} extiende a {b}: cuando {punto}", int((W - X_LIM - 20) / 5.3)):
                o.append(_texto(X_LIM, ly, [lin], 10, False, "start", TINTA)); ly += 14
            ly += 1
        o.append("</g>")
    H_real = max(H, ly + 16)
    svg = "".join(o)
    svg = svg.replace(f'height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}"', f'height="{H_real:.0f}" viewBox="0 0 {W:.0f} {H_real:.0f}"', 1)
    return svg + "</svg>"


# -------------------------------------------------------------------- mapa

def mapa(casos, subs, SS, nombres_act, actores, directos, secundario, esp, gen, limite_txt):
    """Los subsistemas como paquetes apilados y, a su derecha, una matriz que dice qué actores participan
    en cada uno (un punto por actor y paquete); los actores van en una columna a la izquierda, afuera del
    límite del sistema. No se dibuja una línea por pareja: serían más de cien y ninguna se leería."""
    n = len(subs)
    FH, PW = 40, 520
    X_ACT, X_LIM = 90, 240
    CELDA = 64
    Y0 = 74
    cnt = {s: sum(1 for c in casos if casos[c]["ss"] == s) for s in subs}
    toca = {k: set() for k in actores}
    for c in casos:
        for k in directos(c):
            if k in toca:
                toca[k].add(casos[c]["ss"])
    for k, lst in secundario.items():
        for c in lst:
            if c in casos and k in toca:
                toca[k].add(casos[c]["ss"])
    if esp in actores and gen in actores:
        actores = [k for k in actores if k != esp]
        actores.insert(actores.index(gen) + 1, esp)
    SALTO = 120
    apos, y_a = {}, Y0 + 50
    for k in actores:
        apos[k] = y_a
        y_a += 200 if k == gen else SALTO        # sobre el que especializa cabe la línea de la generalización
    x_m = X_LIM + PW + 40               # primera columna de la matriz
    W = x_m + CELDA * len(actores) + 30
    H_LIM = n * FH + 60
    H = max(Y0 + H_LIM + 110, max(apos.values()) + 120)

    o = [_cabecera(W, H, f"Mapa de navegación (no es un diagrama UML) — SPLG ({n} paquetes · {len(casos)} casos de uso)")]
    o.append(f'<rect class="limite" data-x="{X_LIM}" data-y="{Y0}" data-w="{PW + 20}" data-h="{H_LIM}" '
             f'x="{X_LIM}" y="{Y0}" width="{PW + 20}" height="{H_LIM}" fill="#FFFFFF" stroke="{BORDE}" stroke-width="{GROSOR}"/>')
    o.append(_texto(X_LIM + (PW + 20) / 2, Y0 + 18, [limite_txt], 12, negrita=True))
    # encabezado de la matriz: el código de cada actor
    corto = {"01": "Cliente", "02": "Chofer", "03": "Admin.", "04": "Sist. Autom.", "05": "Admin. Gral.",
             "06": "MercadoPago", "07": "Firebase", "08": "Correo", "09": "Plataforma", "10": "Operador"}
    cols = sorted(actores)
    for j, k in enumerate(cols):
        o.append(_texto(x_m + j * CELDA + CELDA / 2, Y0 + 22, ["ACT-" + k, corto.get(k, "")], 9, False, "middle", "#000000", negrita=True))
    for i, s in enumerate(subs):
        y = Y0 + 40 + i * FH
        if i % 2 == 0:
            o.append(f'<rect x="{x_m - 6}" y="{y + 4}" width="{CELDA * len(actores) + 6}" height="{FH - 8}" fill="#F4F8FC"/>')
        o.append(f'<g class="paquete" data-pq="{s}" data-n="{cnt[s]}">'
                 f'<rect x="{X_LIM + 10}" y="{y + 4}" width="{PW}" height="{FH - 8}" fill="url(#vp)" stroke="{BORDE}" stroke-width="{GROSOR}"/>'
                 + _texto(X_LIM + 22, y + FH / 2, [f"{s}  {SS[s]}"], 11, False, "start", "#000000", negrita=True)
                 + _texto(X_LIM + PW, y + FH / 2, [f"{cnt[s]} CU"], 11, False, "end", TINTA)
                 + "</g>")
        for j, k in enumerate(cols):
            if s in toca[k]:
                o.append(f'<circle class="participa" data-act="{k}" data-pq="{s}" cx="{x_m + j * CELDA + CELDA / 2}" '
                         f'cy="{y + FH / 2}" r="5" fill="{BORDE}"/>')
    for k in actores:
        o.append(_actor(X_ACT, apos[k], k, nombres_act[k], ext=k in NOMBRES_SISTEMA_EXTERNO))
    if esp in apos and gen in apos:
        o.append(f'<path class="gen" data-esp="{esp}" data-gen="{gen}" d="M{X_ACT} {apos[esp] - 10:.1f} V{apos[gen] + 9 + 44 + 14 + 40:.1f}" '
                 f'fill="none" stroke="{TINTA}" stroke-width="1" marker-end="url(#hueco)"/>')
    ly = Y0 + H_LIM + 30
    for t in [f"ACT-{esp} especializa a ACT-{gen}: solo figura en los paquetes con casos exclusivos del Administrador General.",
              "Un punto indica que el actor de esa columna participa en el paquete. CU: cantidad de casos de uso del paquete.",
              "El detalle caso por caso está en las láminas del diagrama de casos de uso y en el diagrama de cada subsistema."]:
        o.append(_texto(X_LIM, ly, [t], 10, False, "start", TINTA)); ly += 16
    return "".join(o) + "</svg>"


def contexto(actores, nombres_act, roles, lineas_ss, esp, gen, limite_txt, titulo):
    """Diagrama de contexto: todos los actores en una columna a la izquierda y el sistema como una sola
    caja a la derecha, con el motivo de cada relación sobre su línea."""
    SALTO = 125
    X_ACT, X_LIM, PW = 80, 330, 470
    Y0 = 52
    apos, y_a = {}, Y0 + 30
    for k in actores:
        apos[k] = y_a
        y_a += SALTO + 75 if k == gen else SALTO
    H_LIM = max(y_a - Y0 - 30, len(lineas_ss) * 16 + 110)
    H = Y0 + H_LIM + 40
    W = X_LIM + PW + 30
    o = [_cabecera(W, H, titulo)]
    o.append(f'<rect class="limite" data-x="{X_LIM}" data-y="{Y0}" data-w="{PW}" data-h="{H_LIM}" x="{X_LIM}" y="{Y0}" '
             f'width="{PW}" height="{H_LIM}" fill="url(#vp)" stroke="{BORDE}" stroke-width="{GROSOR}"/>')
    o.append(_texto(X_LIM + PW / 2, Y0 + 22, [limite_txt], 12, negrita=True))
    y = Y0 + 56
    for t in lineas_ss + ["", "(entre paréntesis, los casos de uso de cada subsistema)"]:
        o.append(_texto(X_LIM + 20, y, [t], 11, False, "start")); y += 16
    for k in actores:
        ya = apos[k] + 19
        o.append(f'<line class="asoc" data-act="{k}" x1="{X_ACT + 20}" y1="{ya:.1f}" x2="{X_LIM}" y2="{ya:.1f}" stroke="{TINTA}" stroke-width="0.8"/>')
        wl_ = min(len(roles[k]) * 5.4 + 10, X_LIM - X_ACT - 50)
        o.append(f'<rect x="{(X_ACT + 20 + X_LIM) / 2 - wl_ / 2:.1f}" y="{ya - 15:.1f}" width="{wl_:.1f}" height="13" fill="#FFFFFF"/>')
        o.append(_texto((X_ACT + 20 + X_LIM) / 2, ya - 8, [roles[k]], 10, False, "middle", TINTA))
        o.append(_actor(X_ACT, apos[k], k, nombres_act[k], ext=k in NOMBRES_SISTEMA_EXTERNO))
    o.append(f'<path class="gen" data-esp="{esp}" data-gen="{gen}" d="M{X_ACT} {apos[esp] - 10:.1f} V{apos[gen] + 9 + 44 + 14 + 40:.1f}" '
             f'fill="none" stroke="{TINTA}" stroke-width="1" marker-end="url(#hueco)"/>')
    return "".join(o) + "</svg>"
