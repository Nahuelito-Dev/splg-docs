# -*- coding: utf-8 -*-
"""Dibuja el diagrama completo de casos de uso y el mapa de una pagina.

Graphviz no da abasto con 166 casos de uso, ocho actores y mas de trescientas
relaciones: el motor ubica mal a los actores que quedan fuera del limite del
sistema y superpone los paquetes. Estas dos laminas se componen aca, con una
disposicion fija, y se escriben como SVG; generar-uml.py las convierte a PNG.

Cada elemento lleva atributos data-* para que verificar-conformidad.py pueda
comprobar el dibujo sin mirarlo: que cada actor aparezca una sola vez y fuera
del limite, que cada caso tenga un actor y que las relaciones sean las de los
diagramas por subsistema.
"""
import math
from html import escape

FUENTE = "Helvetica, Arial, sans-serif"
TINTA = "#2C4257"


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


def _texto(x, y, lineas, fs, negrita_primera=False, ancla="middle", color=TINTA, interlinea=None):
    il = interlinea or fs * 1.18
    y0 = y - il * (len(lineas) - 1) / 2
    partes = []
    for i, t in enumerate(lineas):
        peso = ' font-weight="bold"' if (negrita_primera and i == 0) else ""
        partes.append(f'<text x="{x:.1f}" y="{y0 + i * il:.1f}" font-size="{fs}" text-anchor="{ancla}" '
                      f'dominant-baseline="central" fill="{color}"{peso}>{escape(t)}</text>')
    return "".join(partes)


def _borde_elipse(cx, cy, rx, ry, hacia_x, hacia_y):
    """Punto del borde de la elipse en la direccion de (hacia_x, hacia_y)."""
    dx, dy = hacia_x - cx, hacia_y - cy
    if dx == 0 and dy == 0:
        return cx, cy
    t = 1.0 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx * t, cy + dy * t


def _actor(x, y, cod, nombre, color, esc=1.0, fs=15, ext=False):
    """Monigote UML con su nombre debajo. (x, y) es el centro de la cabeza."""
    r = 11 * esc
    g = [f'<g class="actor" data-act="{cod}" data-x="{x:.0f}" data-y="{y:.0f}">']
    g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#E8EDF2" stroke="{TINTA}" stroke-width="1.6"/>')
    g.append(f'<path d="M{x:.1f} {y + r:.1f} V{y + r + 28 * esc:.1f} M{x - 17 * esc:.1f} {y + r + 8 * esc:.1f} '
             f'H{x + 17 * esc:.1f} M{x:.1f} {y + r + 28 * esc:.1f} L{x - 15 * esc:.1f} {y + r + 52 * esc:.1f} '
             f'M{x:.1f} {y + r + 28 * esc:.1f} L{x + 15 * esc:.1f} {y + r + 52 * esc:.1f}" '
             f'stroke="{TINTA}" stroke-width="1.6" fill="none"/>')
    ls = ([f"«sistema externo»"] if ext else []) + [nombre, f"(ACT-{cod})"]
    g.append(_texto(x, y + r + 52 * esc + 18 * esc + (len(ls) - 1) * fs * 0.6, ls, fs, False))
    g.append(f'<rect x="{x - 3:.1f}" y="{y - 3:.1f}" width="6" height="6" fill="{color}" stroke="none"/>')
    g.append("</g>")
    return "".join(g)


def _flecha(id_, color):
    return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
            f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10" fill="none" stroke="{color}" stroke-width="1.4"/></marker>')


def _cabecera(w, h, titulo, fs_titulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'font-family="{FUENTE}">'
            f'<defs>{_flecha("abre", "#2C4257")}'
            f'<marker id="hueco" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" '
            f'orient="auto"><path d="M1 1 L11 6 L1 11 Z" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1.4"/></marker>'
            f'</defs><rect width="100%" height="100%" fill="#FFFFFF"/>'
            + _texto(w / 2, 34, [titulo], fs_titulo, True))


# ---------------------------------------------------------------- completo

def _rect_toca_elipse(x0, y0, x1, y1, cx, cy, rx, ry, margen=3):
    px = min(max(cx, x0), x1)
    py = min(max(cy, y0), y1)
    return ((px - cx) / (rx + margen)) ** 2 + ((py - cy) / (ry + margen)) ** 2 < 1


def completo(casos, subs, SS, TINTE, BORDE, COLOR_ACT, NOMBRE_ACT, IZQ, DER, directos,
             secundario, factorizado, inc, ext, esp, gen, limite_txt, tintes_ss,
             titulo=None, columnas=4, ref_ss=None, compacto=False):
    import random
    # la celda deja entre ovalos un canal de 56x22: ahi entran las etiquetas de las relaciones
    CW, CH, RX, RY = 350, 114, 140, 42
    PAD, CAB = 22, 64
    FS = 12.5
    # Las láminas del completo se miran a pantalla completa: letra más grande y menos aire.
    SALTO_ACT = 330
    ANCHO_TXT, FS_REL, FS_PAQ, FS_ACT = 27, 10, 15, 17
    if compacto:
        CW, CH, RX, RY = 330, 112, 152, 50
        PAD, CAB = 18, 58
        FS = 16
        SALTO_ACT = 235
        ANCHO_TXT, FS_REL, FS_PAQ, FS_ACT = 26, 13, 19, 20
    META = columnas
    GAP = 40 if compacto else 56
    ZONA = 240 if compacto else 300
    MARCO = 50
    SEP = 28                                    # entre paquetes de una columna

    ids_inc = {b for _, b in inc}
    paq = []
    for s in subs:
        cs = sorted(c for c in casos if casos[c]["ss"] == s)
        # las bases a la izquierda y los casos incluidos a la derecha
        cs = [c for c in cs if c not in ids_inc] + [c for c in cs if c in ids_inc]
        paq.append({"id": s, "titulo": SS[s] if s == ref_ss else f"{s} — {SS[s]}", "casos": cs, "ss": s})
    if factorizado:
        paq.append({"id": "FACT", "titulo": "Casos de uso factorizados", "casos": list(factorizado), "ss": None})
    for p in paq:
        n = len(p["casos"])
        p["cols"] = 1 if n <= 4 else (2 if n <= 12 else (3 if n <= 30 else 4))
        p["filas"] = math.ceil(n / p["cols"])
        p["w"] = p["cols"] * CW + 2 * PAD
        p["h"] = p["filas"] * CH + CAB + PAD

    # cuantas asociaciones tiene cada actor con cada paquete
    cu_paq = {}
    for p in paq:
        for c in p["casos"]:
            cu_paq[c] = p["id"]
    peso = {}
    for c in casos:
        for k in directos(c):
            peso[(k, cu_paq[c])] = peso.get((k, cu_paq[c]), 0) + 1
    for k, lst in secundario.items():
        for c in lst:
            peso[(k, cu_paq[c])] = peso.get((k, cu_paq[c]), 0) + 1
    ACT = IZQ + DER

    def disponer(cols):
        """Columnas de paquetes -> posicion de cada paquete y de cada caso."""
        ancho = [max(p["w"] for p in c) if c else 0 for c in cols]
        cajas, pos, alt = {}, {}, []
        x0 = MARCO
        for m, c in enumerate(cols):
            y = 80
            for p in c:
                cajas[p["id"]] = (p, x0, y)
                for i, cu in enumerate(p["casos"]):
                    f, k = i % p["filas"], i // p["filas"]
                    pos[cu] = (x0 + PAD + k * CW + CW / 2, y + CAB + f * CH + CH / 2)
                y += p["h"] + SEP
            alt.append(y - SEP - 80 if c else 0)
            x0 += ancho[m] + GAP
        return cajas, pos, ancho, alt, x0 - GAP + MARCO

    def ubicar_actores(cajas, ancho_total, alt_max):
        """Cada actor a la altura media de sus asociaciones, sin que se pisen."""
        cy = {k: [0.0, 0.0] for k in ACT}
        for (k, pid), n in peso.items():
            p, x, y = cajas[pid]
            cy[k][0] += n * (y + p["h"] / 2); cy[k][1] += n
        ideal = {k: cy[k][0] / cy[k][1] if cy[k][1] else alt_max / 2 for k in ACT}
        res = {}
        for grupo, orden in ((IZQ, IZQ), (DER, sorted(DER, key=lambda k: ideal[k]))):
            y = None
            for k in orden:
                v = ideal[k] if y is None else max(ideal[k], y + SALTO_ACT)
                res[k] = v; y = v
        # 05 va debajo de 03 (la flecha de la generalizacion)
        res[esp] = max(res[esp], res[gen] + SALTO_ACT)
        return res

    def costo(cols):
        cajas, pos, ancho, alt, ancho_t = disponer(cols)
        ymax = max(alt) + 160
        ay = ubicar_actores(cajas, ancho_t, ymax)
        total = 0.0
        for (k, pid), n in peso.items():
            p, x, y = cajas[pid]
            cx, cyp = x + p["w"] / 2, y + p["h"] / 2
            axp = -ZONA / 2 if k in IZQ else ancho_t + ZONA / 2
            total += n * math.hypot(cx - axp, cyp - ay[k])
        return total, alt

    # busqueda local: se mueven y se intercambian paquetes entre columnas y se
    # queda la disposicion de menor largo total de asociaciones
    rnd = random.Random(7)
    ini = [[] for _ in range(META)]
    altc = [0] * META
    for p in sorted(paq, key=lambda p: -p["h"]):
        m = altc.index(min(altc)); ini[m].append(p); altc[m] += p["h"] + SEP
    hmax = max(max(altc) * 1.06, max(p["h"] for p in paq))
    def valida(cols):
        return all((sum(p["h"] + SEP for p in c) - SEP if c else 0) <= hmax for c in cols) and all(cols)
    mejor, c_mejor = [list(c) for c in ini], costo(ini)[0]
    actual, c_act = [list(c) for c in mejor], c_mejor
    temp = c_mejor * 0.02
    for it in range(30000):
        cand = [list(c) for c in actual]
        if rnd.random() < 0.5:
            c1, c2 = rnd.randrange(META), rnd.randrange(META)
            if not cand[c1] or not cand[c2]: continue
            i, j = rnd.randrange(len(cand[c1])), rnd.randrange(len(cand[c2]))
            cand[c1][i], cand[c2][j] = cand[c2][j], cand[c1][i]
        else:
            c1, c2 = rnd.randrange(META), rnd.randrange(META)
            if not cand[c1]: continue
            pq = cand[c1].pop(rnd.randrange(len(cand[c1])))
            cand[c2].insert(rnd.randrange(len(cand[c2]) + 1), pq)
        if not valida(cand): continue
        c_nuevo = costo(cand)[0]
        if c_nuevo < c_act or rnd.random() < math.exp((c_act - c_nuevo) / max(temp, 1e-9)):
            actual, c_act = cand, c_nuevo
            if c_act < c_mejor: mejor, c_mejor = [list(c) for c in actual], c_act
        temp *= 0.9998
    col = mejor
    cajas_d, pos_rel, ancho_col, alt, ancho_lim = disponer(col)

    Y_lim = 90
    X_lim = ZONA
    H_lim = max(alt) + 80 + 60
    W_lim = ancho_lim
    W = X_lim + W_lim + ZONA
    ay_rel = ubicar_actores(cajas_d, ancho_lim, max(alt) + 160)
    # el limite tiene que alcanzar a todos los actores
    off_y = Y_lim
    pos = {c: (x + X_lim, y + off_y) for c, (x, y) in pos_rel.items()}
    cajas = {k: (p, x + X_lim, y + off_y) for k, (p, x, y) in cajas_d.items()}
    ax_i = X_lim - ZONA / 2
    ax_d = X_lim + W_lim + ZONA / 2
    apos = {k: ((ax_i if k in IZQ else ax_d), ay_rel[k] + off_y) for k in ACT}
    lo = min(y for _, y in apos.values()) - 40
    hi = max(y for _, y in apos.values()) + 220
    H_lim = max(H_lim, int(hi - Y_lim), 0)
    LEY = 300
    H = Y_lim + H_lim + LEY

    o = [_cabecera(W, H, titulo or f"Diagrama Completo de Casos de Uso — SPLG ({len(casos)} casos de uso)", 30)]
    o.append(f'<rect class="limite" data-x="{X_lim:.0f}" data-y="{Y_lim:.0f}" data-w="{W_lim:.0f}" data-h="{H_lim:.0f}" '
             f'x="{X_lim}" y="{Y_lim}" width="{W_lim:.0f}" height="{H_lim:.0f}" fill="#FFFFFF" stroke="#6B7683" stroke-width="2.4"/>')
    o.append(_texto(X_lim + W_lim / 2, Y_lim + 28, [limite_txt], 20, True))

    # 1. asociaciones, en haz hasta el borde del paquete y de ahi a cada caso
    def haz(k, pid, cu, rol):
        p, px_, py_ = cajas[pid]
        izq = k in IZQ
        xa, ya = apos[k]
        sx, sy = (xa + 18, ya + 30) if izq else (xa - 18, ya + 30)
        ex = px_ if izq else px_ + p["w"]
        # altura de entrada: la media de los casos de este actor en el paquete
        ys = [pos[c][1] for c in p["casos"] if (k in directos(c) if c in casos else False)
              or (c in secundario.get(k, []))]
        ey = min(max(sum(ys) / len(ys), py_ + CAB), py_ + p["h"] - 10) if ys else py_ + p["h"] / 2
        cx, cy = pos[cu]
        tx = cx - RX if izq else cx + RX
        d1 = max(60, abs(ex - sx) * 0.5)
        d2 = max(30, abs(tx - ex) * 0.5)
        s = 1 if izq else -1
        return (f"M{sx:.1f} {sy:.1f} C{sx + s * d1:.1f} {sy:.1f} {ex - s * d1:.1f} {ey:.1f} {ex:.1f} {ey:.1f} "
                f"C{ex + s * d2:.1f} {ey:.1f} {tx - s * d2:.1f} {cy:.1f} {tx:.1f} {cy:.1f}")
    for cu in sorted(casos):
        for k in directos(cu):
            o.append(f'<path class="asoc" data-act="{k}" data-cu="{cu}" data-rol="principal" '
                     f'd="{haz(k, cu_paq[cu], cu, "p")}" fill="none" stroke="{COLOR_ACT[k]}" '
                     f'stroke-width="1.5" opacity=".7"/>')
    for k in sorted(secundario):
        for cu in secundario[k]:
            o.append(f'<path class="asoc" data-act="{k}" data-cu="{cu}" data-rol="secundario" '
                     f'd="{haz(k, cu_paq[cu], cu, "s")}" fill="none" stroke="{COLOR_ACT[k]}" '
                     f'stroke-width="1.7" opacity=".8"/>')

    # 2. paquetes con fondo semitransparente
    titulos = []
    for pid, (p, x, y) in cajas.items():
        if p["ss"]:
            i = subs.index(p["ss"])
            fondo, borde = TINTE[i % len(TINTE)], BORDE[i % len(BORDE)]
            sub = (f'({len(p["casos"])} casos de uso)' if p["ss"] != ref_ss else
                   "(sólo como referencia)")
        else:
            fondo, borde = "#F2F4F6", "#6B7683"
            sub = "(comportamiento común, sin código propio)"
        o.append(f'<g class="paquete" data-pq="{p["id"]}" data-n="{len(p["casos"])}">'
                 f'<path d="M{x} {y} h{min(p["w"] * 0.55, 480):.0f} v26 H{x + p["w"]} V{y + p["h"]} H{x} Z" '
                 f'fill="{fondo}" fill-opacity=".45" stroke="{borde}" stroke-width="2"/>'
                 f'<path d="M{x} {y + 26} H{x + p["w"]}" stroke="{borde}" stroke-width="1" opacity=".5"/></g>')
        titulos.append(f'<rect x="{x + 2}" y="{y + 2}" width="{min(p["w"] * 0.55, 480) - 4:.0f}" height="24" fill="{fondo}"/>'
                       + _texto(x + 12, y + 13, [p["titulo"]], FS_PAQ, True, "start", borde)
                       + _texto(x + 14, y + 44, [sub], 12, False, "start", borde))
    o += titulos

    # 3. include / extend
    rel = [(a, b, "include", None) for a, b in inc]
    for i, (a, b, punto) in enumerate(ext, 1):
        rel.append((a, b, "extend", i))

    def bezier(p0, c1, c2, p3, n=36):
        pts = []
        for i in range(n + 1):
            t = i / n; u = 1 - t
            pts.append((u**3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * p3[0],
                        u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p3[1]))
        return pts

    zonas_titulo = [(x, y, x + min(p["w"] * 0.55, 480), y + 54) for (p, x, y) in cajas.values()]

    def ruta(a, b, tipo="include"):
        """Curva de a hacia b que no pasa por debajo de ningun otro ovalo: se prueban
        desvios cada vez mas grandes hacia un lado y hacia el otro y se toma el primero
        que no toca ninguna elipse ajena."""
        (xa, ya), (xb, yb) = pos[a], pos[b]
        dx, dy = xb - xa, yb - ya
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        ajenos = [p_ for k_, p_ in pos.items() if k_ not in (a, b)]
        mejor = None
        # entre dos ovalos pegados la flecha de un <<extend>> quedaria tan corta que no se
        # ve la punta: se la obliga a describir un arco
        p_a = _borde_elipse(xa, ya, RX, RY, xb, yb)
        p_b = _borde_elipse(xb, yb, RX, RY, xa, ya)
        corta = tipo == "extend" and math.hypot(p_a[0] - p_b[0], p_a[1] - p_b[1]) < 100
        offsets = (0, 70, -70, 140, -140, 220, -220, 320, -320, 440, -440, 600, -600)
        if corta:
            offsets = (150, -150, 220, -220, 320, -320, 440, -440, 600, -600)
        for off in offsets:
            c1 = (xa + dx / 3 + nx * off, ya + dy / 3 + ny * off)
            c2 = (xa + 2 * dx / 3 + nx * off, ya + 2 * dy / 3 + ny * off)
            p1 = _borde_elipse(xa, ya, RX, RY, c1[0], c1[1])
            p2 = _borde_elipse(xb, yb, RX, RY, c2[0], c2[1])
            pts = bezier(p1, c1, c2, p2)
            choques = sum(1 for (px, py) in pts[1:-1] for (cx, cy) in ajenos
                          if ((px - cx) / (RX + 5)) ** 2 + ((py - cy) / (RY + 5)) ** 2 < 1)
            # la curva tiene que quedar dentro del limite y por debajo de su titulo
            choques += 50 * sum(1 for (px, py) in pts
                                if py < Y_lim + 60 or py > Y_lim + H_lim - 20
                                or px < X_lim + 10 or px > X_lim + W_lim - 10)
            # y que no pase por encima del titulo de ningun paquete
            choques += 50 * sum(1 for (px, py) in pts for (zx0, zy0, zx1, zy1) in zonas_titulo
                                if zx0 - 4 <= px <= zx1 + 4 and zy0 - 4 <= py <= zy1 + 4)
            if mejor is None or choques < mejor[0]:
                mejor = (choques, p1, c1, c2, p2, pts)
            if choques == 0: break
        return mejor[1:]

    rutas = {}
    for a, b, tipo, n in rel:
        p1, c1, c2, p2, pts = ruta(a, b, tipo)
        rutas[(a, b, tipo)] = pts
        o.append(f'<path class="rel" data-tipo="{tipo}" data-desde="{a}" data-hasta="{b}" '
                 f'd="M{p1[0]:.1f} {p1[1]:.1f} C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}" '
                 f'fill="none" stroke="{TINTA}" stroke-width="1.4" stroke-dasharray="7 4" marker-end="url(#abre)"/>')

    # 4. ovalos y, encima de todo, las etiquetas de las relaciones
    elipses = list(pos.values())
    pe_de = {}
    for i, (a, b, punto) in enumerate(ext, 1):
        pe_de.setdefault(b, []).append(f"PE-{i}")
    for cu, (cx, cy) in pos.items():
        if cu.startswith("F-"):
            borde, nombre, cod = "#6B7683", factorizado[cu], ""
        else:
            borde = BORDE[subs.index(casos[cu]["ss"]) % len(BORDE)]
            nombre, cod = casos[cu]["nombre"], cu
        ls = ([cod] if cod else []) + _lineas(nombre, ANCHO_TXT)
        # compartimento "extension points" del caso base de un <<extend>>
        pes = pe_de.get(cu)
        extra = ""
        dy = 0
        if pes:
            # el compartimento va debajo del nombre: con letra grande se corre más
            dy, yl, yt, fe = (-14, 18, 32, 12) if compacto else (-9, 12, 23, 10)
            extra = (f'<line x1="{cx - 118:.1f}" y1="{cy + yl:.1f}" x2="{cx + 118:.1f}" y2="{cy + yl:.1f}" stroke="{borde}" stroke-width="1"/>'
                     + _texto(cx, cy + yt, ["extension points: " + ", ".join(pes)], fe, False, "middle", TINTA))
        o.append(f'<g class="cu" data-cu="{cu}" data-x="{cx:.0f}" data-y="{cy:.0f}">'
                 f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{RX}" ry="{RY}" fill="#FFFFFF" stroke="{borde}" stroke-width="1.8"/>'
                 + _texto(cx, cy + dy, ls, FS, bool(cod)) + extra + "</g>")
    puestas = []
    sin_lugar = 0
    for a, b, tipo, n in sorted(rel, key=lambda r: -math.hypot(pos[r[0]][0] - pos[r[1]][0], pos[r[0]][1] - pos[r[1]][1])):
        pts = rutas[(a, b, tipo)]
        txt = f"«{tipo}»" + (f" PE-{n}" if n else "")
        wl, hl_ = len(txt) * FS_REL * 0.58 + 6, FS_REL + 3
        elegido, mejor_c = None, None
        orden_t = sorted(range(2, len(pts) - 2), key=lambda i: abs(i - len(pts) / 2))
        for i in orden_t:
            mx, my = pts[i]
            r = (mx - wl / 2, my - hl_ / 2, mx + wl / 2, my + hl_ / 2)
            choques = sum(1 for (cx, cy) in elipses if _rect_toca_elipse(*r, cx, cy, RX, RY, 1))
            choques += sum(1 for q in puestas if not (r[2] < q[0] - 2 or q[2] + 2 < r[0] or r[3] < q[1] - 2 or q[3] + 2 < r[1]))
            if mejor_c is None or choques < mejor_c:
                elegido, mejor_c = (mx, my, r), choques
            if choques == 0: break
        if mejor_c: sin_lugar += 1
        mx, my, r = elegido
        puestas.append(r)
        o.append(f'<g class="etiqueta" data-tipo="{tipo}" data-desde="{a}" data-hasta="{b}">'
                 f'<rect x="{r[0]:.1f}" y="{r[1]:.1f}" width="{wl:.1f}" height="{hl_}" fill="#FFFFFF"/>'
                 + _texto(mx, my, [txt], FS_REL, False, "middle", TINTA) + "</g>")
    completo.etiquetas_sin_lugar = sin_lugar

    # actores
    for k in ACT:
        x, y = apos[k]
        o.append(_actor(x, y, k, NOMBRE_ACT[k], COLOR_ACT[k], 1.45, FS_ACT, ext=k in ("06", "07", "08", "09")))
    xe, ye = apos[esp]
    xg, yg = apos[gen]
    o.append(f'<path class="gen" data-esp="{esp}" data-gen="{gen}" d="M{xe:.1f} {ye - 24:.1f} V{yg + 168:.1f}" '
             f'fill="none" stroke="{TINTA}" stroke-width="2" marker-end="url(#hueco)"/>')

    # leyenda
    ly = Y_lim + H_lim + 40
    o.append('<g class="leyenda">')
    o.append(_texto(X_lim, ly, ["Convenciones"], 16, True, "start"))
    x = X_lim
    ly += 34
    for k in ACT:
        o.append(f'<line x1="{x}" y1="{ly}" x2="{x + 34}" y2="{ly}" stroke="{COLOR_ACT[k]}" stroke-width="3"/>')
        o.append(_texto(x + 42, ly, [f"ACT-{k} {NOMBRE_ACT[k]}"], 13, False, "start"))
        x += 330 if k != "05" else 380
        if k == "05": x = X_lim; ly += 26
    ly += 40
    notas = ["Cada actor se dibuja una sola vez y fuera del límite del sistema; los humanos a la izquierda, el Sistema Automático y los sistemas externos a la derecha.",
             f"ACT-{esp} especializa a ACT-{gen} (flecha con triángulo hueco): hereda todas sus asociaciones y sólo se asocia a los casos que son exclusivos suyos.",
             "ACT-06, ACT-07 y ACT-08 son actores secundarios: el sistema los invoca. ACT-09 es un sistema externo que inicia CU-104.",
             "Las líneas de cada actor se juntan en un haz hasta el borde del paquete y de ahí se abren a cada caso.",
             "Las flechas punteadas son relaciones entre casos de uso: «include» va del caso base al incluido; «extend» va de la extensión al caso base."]
    if compacto:
        notas = ["Actores fuera del límite del sistema · asociación actor–caso sin punta · «include»: del caso base al incluido · "
                 "«extend»: de la extensión al caso base · en gris, casos de uso de otra lámina."]
    for tx_ in notas:
        o.append(_texto(X_lim, ly, [tx_], 15 if compacto else 13, False, "start")); ly += 26 if compacto else 22
    ly += 10
    if ext:
        o.append(_texto(X_lim, ly, ["Puntos de extensión (PE) de las relaciones «extend»"], 14, True, "start")); ly += 24
    mitad = (len(ext) + 1) // 2
    for i, (a, b, punto) in enumerate(ext, 1):
        na = factorizado.get(a) or a
        xx = X_lim + (0 if i <= mitad else 1100)
        yy = ly + ((i - 1) % mitad) * 20
        o.append(_texto(xx, yy, [f"PE-{i}  {na} extiende a {b}: cuando {punto}"], 12.5, False, "start"))
    ly += mitad * 20
    o.append("</g>")
    H_real = ly + 30
    svg = "".join(o).replace(f'height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}"', f'height="{H_real:.0f}" viewBox="0 0 {W:.0f} {H_real:.0f}"', 1)
    return svg + "</svg>"


# -------------------------------------------------------------------- mapa

def mapa(casos, subs, SS, TINTE, BORDE, COLOR_ACT, NOMBRE_ACT, IZQ, DER, directos,
         secundario, esp, gen, limite_txt):
    """Una pagina A4 apaisada: los 18 paquetes en una columna, los actores a los
    costados y una linea por actor hacia cada paquete en el que participa."""
    n = len(subs)
    FH, PW = 52, 560
    W, H = 1800, 1380
    xl, yl = 620, 150
    hl = n * FH + 76
    px = xl + (560 - PW) / 2 + 280 - PW / 2 + 0
    px = (W - PW) / 2
    top = yl + 56
    y_pq = {s: top + i * FH + FH / 2 for i, s in enumerate(subs)}
    cnt = {s: sum(1 for c in casos if casos[c]["ss"] == s) for s in subs}
    xi, xd = 130, W - 150
    cyl = yl + hl / 2
    yi = {"01": cyl - 400, "02": cyl - 150, "03": cyl + 100, "05": cyl + 400}
    yd = {"04": cyl - 400, "06": cyl - 200, "07": cyl, "08": cyl + 200, "09": cyl + 400}
    apos = {k: (xi, yi[k]) for k in IZQ}
    apos.update({k: (xd, yd[k]) for k in DER})

    o = [_cabecera(W, H, f"Mapa de navegación (no es un diagrama UML) — SPLG ({n} paquetes · {len(casos)} casos de uso)", 28)]
    lx = px - 60
    o.append(f'<rect class="limite" data-x="{lx:.0f}" data-y="{yl}" data-w="{PW + 120}" data-h="{hl}" '
             f'x="{lx}" y="{yl}" width="{PW + 120}" height="{hl}" fill="#FFFFFF" stroke="#6B7683" stroke-width="2.4"/>')
    o.append(_texto(W / 2, yl + 26, [limite_txt], 17, True))

    # que paquetes toca cada actor (sin las asociaciones que hereda)
    toca = {k: set() for k in IZQ + DER}
    for c in casos:
        for k in directos(c):
            toca[k].add(casos[c]["ss"])
    for k, lst in secundario.items():
        for c in lst:
            if c in casos:
                toca[k].add(casos[c]["ss"])
    # por cada paquete, el orden de los actores que le llegan por cada lado: asi cada linea
    # entra a una altura propia y no se montan
    for lado, ks in (("i", IZQ), ("d", DER)):
        for s in subs:
            quienes = [k for k in ks if s in toca[k]]
            for j, k in enumerate(quienes):
                dy = (j - (len(quienes) - 1) / 2) * 9
                xa, ya = apos[k]
                xe = px if lado == "i" else px + PW
                ye = y_pq[s] + dy
                o.append(f'<line class="asoc" data-act="{k}" data-pq="{s}" x1="{xa + (24 if lado == "i" else -24):.1f}" '
                         f'y1="{ya + 40:.1f}" x2="{xe:.1f}" y2="{ye:.1f}" stroke="{COLOR_ACT[k]}" stroke-width="1.5" opacity=".75"/>')
    for i, s in enumerate(subs):
        y = top + i * FH
        o.append(f'<g class="paquete" data-pq="{s}" data-n="{cnt[s]}">'
                 f'<rect x="{px}" y="{y + 5}" width="{PW}" height="{FH - 10}" fill="{TINTE[i % len(TINTE)]}" '
                 f'stroke="{BORDE[i % len(BORDE)]}" stroke-width="2"/>'
                 f'<rect x="{px}" y="{y + 5}" width="86" height="{FH - 10}" fill="{BORDE[i % len(BORDE)]}"/>'
                 + _texto(px + 43, y + FH / 2, [s], 16, True, "middle", "#FFFFFF")
                 + _texto(px + 98, y + FH / 2, [SS[s]], 16, False, "start", TINTA)
                 + _texto(px + PW - 12, y + FH / 2, [f"{cnt[s]} CU"], 16, True, "end", BORDE[i % len(BORDE)])
                 + "</g>")
    for k in IZQ + DER:
        x, y = apos[k]
        o.append(_actor(x, y, k, NOMBRE_ACT[k], COLOR_ACT[k], 1.45, 17, ext=k in ("06", "07", "08", "09")))
    xe, ye = apos[esp]; xg, yg = apos[gen]
    o.append(f'<path class="gen" data-esp="{esp}" data-gen="{gen}" d="M{xe:.1f} {ye - 24:.1f} V{yg + 168:.1f}" '
             f'fill="none" stroke="{TINTA}" stroke-width="2" marker-end="url(#hueco)"/>')
    o.append(_texto(xe + 14, (ye + yg) / 2 + 40, ["especializa a"], 13, False, "start"))
    ly = yl + hl + 95
    notas = [f"ACT-{esp} especializa a ACT-{gen}: hereda todo lo suyo y la línea sólo llega a los paquetes con casos exclusivos del Administrador General.",
             "Una línea por actor hacia cada paquete en el que participa. ACT-06, ACT-07 y ACT-08 son actores secundarios; ACT-09 es un sistema externo que inicia CU-104.",
             "CU: cantidad de casos de uso del paquete. El detalle caso por caso está en el Diagrama Completo."]
    for t in notas:
        o.append(_texto(60, ly, [t], 15, False, "start")); ly += 26
    return "".join(o) + "</svg>"
