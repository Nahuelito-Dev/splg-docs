# -*- coding: utf-8 -*-
"""Diagrama de casos de uso del sistema a nivel de subsistemas, en notación UML y estilo Visual Paradigm.

Es la figura principal del diagrama de casos de uso del sistema (Documento 0 §6 y Documento 1 §3): los subsistemas
son paquetes UML apilados en una columna dentro del límite del sistema y los actores, cada uno una vez y fuera
del límite, se asocian a los paquetes en los que participan. El Administrador General especializa al
Administrador. El detalle de cada subsistema —sus casos de uso, uno por uno— está en el diagrama completo y en
sus láminas. Cada elemento lleva atributos data-* para que verificar-conformidad.py compruebe el dibujo.
"""
import math
from uml_lamina import (_texto, _actor, _cabecera, BORDE, TINTA, SUAVE, GROSOR, NOMBRES_SISTEMA_EXTERNO)

ORDEN = ["01", "02", "03", "05", "04", "10", "06", "07", "08", "09"]
X_ACT, X_LIM, Y0 = 85, 235, 52
PW, PH, GAP, TAB = 420, 44, 20, 14


def _anclas(x, y):
    r = 9
    return [(x + r, y), (x + 15, y + r + 8), (x + 6, y + r + 33), (x + 13, y + r + 44)]


def subsistemas(subs, nombres_ss, cuenta, actores_de_ss, nombres_act, esp, gen, limite_txt, titulo, planificados=()):
    """subs [SS-xx]; nombres_ss {SS: nombre}; cuenta {SS: casos}; actores_de_ss {SS: {actores}}."""
    rank = {k: i for i, k in enumerate(ORDEN)}

    def clave(s):
        r_ = sorted(rank[k] for k in actores_de_ss[s])
        return (round(sum(r_) / len(r_), 2) if r_ else 99, tuple(r_), s)
    orden = sorted(subs, key=clave)
    x_p = X_LIM + 60
    pos = {}
    y = Y0 + 46
    for s in orden:
        pos[s] = y
        y += PH + GAP
    y_fin = y
    # actores a la altura media de sus paquetes, sin pisarse
    yc = {}
    for k in ORDEN:
        ys = [pos[s] + PH / 2 for s in orden if k in actores_de_ss[s]]
        if ys:
            yc[k] = sum(ys) / len(ys) - 40
    orden_a = [k for k in sorted(yc, key=lambda k: yc[k]) if k != esp]
    if esp in yc:
        i = orden_a.index(gen) + 1 if gen in orden_a else len(orden_a)
        orden_a.insert(i, esp)
    ya = {}
    prev = None
    for k in orden_a:
        salto = 190 if (prev == gen and k == esp) else 112
        ya[k] = max(yc[k], Y0 + 40 if prev is None else ya[prev] + salto)
        prev = k
    y_fin = max(y_fin, max(ya.values()) + 130)
    W = x_p + PW + 70
    H = y_fin + 90
    o = [_cabecera(W, H, titulo)]
    lim_w, lim_h = W - X_LIM - 24, y_fin - Y0 - 10
    o.append(f'<rect class="limite" data-x="{X_LIM}" data-y="{Y0}" data-w="{lim_w:.0f}" data-h="{lim_h:.0f}" '
             f'x="{X_LIM}" y="{Y0}" width="{lim_w:.0f}" height="{lim_h:.0f}" fill="#FFFFFF" stroke="{BORDE}" stroke-width="{GROSOR}"/>')
    o.append(_texto(X_LIM + lim_w / 2, Y0 + 20, [limite_txt], 12, negrita=True))
    # asociaciones: cada actor una recta a cada paquete en el que participa; sale de varios puntos de su contorno
    for k, yk in ya.items():
        suyos = [s for s in orden if k in actores_de_ss[s]]
        anclas = _anclas(X_ACT, yk)
        for j, s in enumerate(suyos):
            lst = sorted(a_ for a_ in actores_de_ss[s] if a_ in ya)
            n = len(lst)
            dy = ((lst.index(k) - (n - 1) / 2) * 9) if n > 1 else 0
            ax, ay = anclas[min(len(anclas) - 1, j * len(anclas) // max(1, len(suyos)))] if len(suyos) > 6 else anclas[1]
            tx, ty = x_p, pos[s] + PH / 2 + dy
            rol = "secundario" if k in NOMBRES_SISTEMA_EXTERNO and k != "09" else "principal"
            o.append(f'<path class="asoc" data-act="{k}" data-pq="{s}" data-rol="{rol}" '
                     f'd="M{ax:.1f} {ay:.1f} L{tx:.1f} {ty:.1f}" fill="none" stroke="{TINTA}" stroke-width="0.7" opacity="0.9"/>')
    # paquetes
    for s in orden:
        yp = pos[s]
        plan = s in planificados
        o.append(f'<g class="paquete" data-pq="{s}" data-n="{cuenta[s]}">'
                 f'<path d="M{x_p} {yp} h{TAB * 3} v{-TAB} h{-TAB * 3} z" fill="url(#vp)" stroke="{BORDE}" stroke-width="{GROSOR}" transform="translate(0 0)"/>'
                 f'<rect x="{x_p}" y="{yp}" width="{PW}" height="{PH}" fill="url(#vp)" stroke="{BORDE}" stroke-width="{GROSOR}"/>'
                 + _texto(x_p + 12, yp + 16, [f"{s}  {nombres_ss[s]}"], 12, False, "start", "#000000", negrita=True)
                 + _texto(x_p + 12, yp + 33, [f"{cuenta[s]} caso{'s' if cuenta[s] != 1 else ''} de uso"], 10, False, "start", SUAVE)
                 + '</g>')
    for k, yk in ya.items():
        o.append(_actor(X_ACT, yk, k, nombres_act[k], ext=k in NOMBRES_SISTEMA_EXTERNO))
    if esp in ya and gen in ya:
        o.append(f'<path class="gen" data-esp="{esp}" data-gen="{gen}" d="M{X_ACT} {ya[esp] - 10:.1f} V{ya[gen] + 9 + 44 + 14 + 40:.1f}" '
                 f'fill="none" stroke="{TINTA}" stroke-width="1" marker-end="url(#hueco)"/>')
    ly = y_fin + 22
    notas = ["Cada paquete es un subsistema; el número es la cantidad de casos de uso que contiene. Los casos de uso, uno por uno, están en el diagrama completo y en sus láminas.",
             "Asociación actor–subsistema: línea continua sin punta; el actor participa en algún caso de uso del subsistema, ya sea porque lo inicia o porque el sistema lo invoca durante el caso.",
             f"ACT-{esp} especializa a ACT-{gen} (triángulo hueco); como la especialización no reemplaza a las asociaciones, cada actor se une a todos los subsistemas en los que participa."]
    from uml_lamina import _lineas
    for tx in notas:
        for lin in _lineas(tx, max(40, int((W - X_LIM - 20) / 5.3))):
            o.append(_texto(X_LIM, ly, [lin], 10, False, "start", TINTA))
            ly += 14
        ly += 2
    svg = "".join(o)
    h_real = max(H, ly + 16)
    svg = svg.replace(f'height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}"', f'height="{h_real:.0f}" viewBox="0 0 {W:.0f} {h_real:.0f}"', 1)
    return svg + "</svg>"
