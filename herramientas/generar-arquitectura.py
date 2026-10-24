#!/usr/bin/env python3
"""Dibuja la lamina de entornos y recorrido del codigo (vista de entrega, complementaria
del diagrama de despliegue UML de diagramas/uml/UML_Despliegue.puml).

    python3 herramientas/generar-arquitectura.py  ->  diagramas/uml/SPLG_Arquitectura.svg

Se escribe a mano y no con plantuml. El de entornos no es un diagrama UML sino una
lamina de lectura, y graphviz lo resolvia con cajas sueltas y flechas cruzadas. El
armado es por filas: a la izquierda el rotulo sobre fondo oscuro, a la derecha el
contenido, una fila por tema. El recorrido del codigo se anima, que es lo que hace
entender de una que el flujo tiene un sentido.
"""
import os
from estilo_vp import FUENTE, RELLENO, RELLENO_CLARO, BORDE, TINTA as TINTA_VP, SUAVE as SUAVE_VP

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"

ROTULO_W = 210          # columna oscura de la izquierda
MARGEN   = 30
W        = 1180
CAB      = 96

# Estilo Visual Paradigm (estilo_vp.py): fondo blanco, relleno celeste, borde azul oscuro de línea fina
TINTA  = "#000000"
SUAVE  = SUAVE_VP
OSCURO = RELLENO_CLARO          # columna de rótulos de cada fila
PAPEL  = "#FFFFFF"
LINEA  = BORDE

AZUL = VERDE = VIOLETA = OCRE = ROJO = TEAL = BORDE

ICONOS = {
 "laptop": "M3 5h18v11H3z M1 18h22l-2 2H3z",
 "github": ("M12 1.5a10.5 10.5 0 00-3.32 20.47c.53.1.72-.23.72-.5v-1.94c-2.92.63-3.54-1.4-3.54-1.4"
            "-.48-1.22-1.17-1.55-1.17-1.55-.96-.65.07-.64.07-.64 1.06.08 1.62 1.09 1.62 1.09.94 1.62 2.47 1.15 3.07.88"
            ".1-.68.37-1.15.67-1.41-2.33-.27-4.78-1.17-4.78-5.19 0-1.15.41-2.09 1.08-2.83-.11-.27-.47-1.34.1-2.79 0 0 .88-.28 2.88 1.08"
            "a9.9 9.9 0 015.24 0c2-1.36 2.88-1.08 2.88-1.08.57 1.45.21 2.52.1 2.79.67.74 1.08 1.68 1.08 2.83 0 4.03-2.46 4.92-4.8 5.18"
            ".38.33.71.97.71 1.96v2.9c0 .28.19.61.73.5A10.5 10.5 0 0012 1.5z"),
 "base":   "M12 3c4.4 0 8 1.1 8 2.5S16.4 8 12 8 4 6.9 4 5.5 7.6 3 12 3z M4 5.5v13C4 19.9 7.6 21 12 21s8-1.1 8-2.5v-13 M4 12c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5",
 "nube":   "M7 18h10a4 4 0 000-8 6 6 0 00-11.6 2A3.5 3.5 0 007 18z",
 "celu":   "M7 2h10v20H7z M10.5 19h3",
 "engra":  "M12 8.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7z M12 2v3 M12 19v3 M2 12h3 M19 12h3 M5.2 5.2l2.1 2.1 M16.7 16.7l2.1 2.1 M18.8 5.2l-2.1 2.1 M7.3 16.7l-2.1 2.1",
 "web":    "M3 5h18v14H3z M3 9h18 M5.6 7h.01 M8 7h.01",
 "cohete": "M12 2c3.4 3 5.4 7 5.4 11l-2.9 3h-5l-2.9-3C6.6 9 8.6 5 12 2z M9.6 19l-2 3 M14.4 19l2 3 M12 9.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3z",
 "escudo": "M12 2l8 3v6c0 5-3.4 9.4-8 11-4.6-1.6-8-6-8-11V5z M9 12l2 2 4-4",
 "check":  "M20 6L9 17l-5-5",
 "reloj":  "M12 2a10 10 0 100 20 10 10 0 000-20z M12 6v6l4 2",
}

svg = []
def ico(n, x, y, c, e=1.0, ancho=1.6):
    return (f'<g transform="translate({x},{y}) scale({e})" fill="none" stroke="{c}" stroke-width="{ancho}" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{ICONOS[n]}"/></g>')

def caja(x, y, w, h, t, s, color, i=None, relleno=None):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{relleno or RELLENO}" '
         f'stroke="{color}" stroke-width="1"/>']
    tx = x + (40 if i else 14)
    if i: o.append(ico(i, x + 11, y + (h - 24) / 2, color))
    if s:
        o.append(f'<text x="{tx}" y="{y+h/2-3}" class="t-cja" fill="{TINTA}">{t}</text>')
        o.append(f'<text x="{tx}" y="{y+h/2+14}" class="t-sub" fill="{SUAVE}">{s}</text>')
    else:
        o.append(f'<text x="{tx}" y="{y+h/2+4.5}" class="t-cja" fill="{TINTA}">{t}</text>')
    return "".join(o)

def chip(x, y, w, t, color, tinte):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{RELLENO_CLARO}" stroke="{color}" stroke-width="1"/>'
            f'<text x="{x+w/2}" y="{y+17.5}" class="t-chip" fill="{color}" text-anchor="middle">{t}</text>')

def fle(x1, y1, x2, y2, c, t="", anim=True):
    o = [f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{c}" stroke-width="1.1" '
         f'stroke-dasharray="6 3" class="{"flujo" if anim else ""}" marker-end="url(#p{c[1:]})"/>']
    if t:
        o.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 9}" class="t-eti" fill="{SUAVE}" text-anchor="middle">{t}</text>')
    return "".join(o)

FILAS = [
  ("Máquina de\ndesarrollo", 158),
  ("GitHub", 150),
  ("Despliegue", 158),
  ("Documentación", 118),
  ("Servicios\nexternos", 122),
]
H = CAB + sum(a for _, a in FILAS) + MARGEN

colores = {AZUL, VERDE, VIOLETA, OCRE, ROJO, TEAL, SUAVE}
defs = "".join(f'<marker id="p{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
               f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>' for c in colores)

svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
  aria-label="Entornos y recorrido del código de SPLG">
<defs>{defs}</defs>
<style>
  text{{font-family:Arial,Helvetica,sans-serif}}
  .t-tit{{font-size:18px;font-weight:700}}
  .t-baj{{font-size:11px}}
  .t-rot{{font-size:13px;font-weight:700;fill:#000000}}
  .t-cja{{font-size:12px;font-weight:700}}
  .t-sub{{font-size:10.5px}}
  .t-chip{{font-size:11px;font-weight:600}}
  .t-eti{{font-size:11px;font-weight:600}}
  /* El recorrido del codigo se anima. Sin el movimiento hay que leer las
     etiquetas para saber hacia donde va cada linea. */
  .flujo{{animation:correr 1.1s linear infinite}}
  @keyframes correr{{to{{stroke-dashoffset:-26}}}}
  @media (prefers-reduced-motion:reduce){{.flujo{{animation:none}}}}
</style>
<rect width="{W}" height="{H}" fill="{PAPEL}"/>
<text x="{MARGEN}" y="{MARGEN+22}" class="t-tit" fill="{TINTA}">Entornos y recorrido del código — SPLG</text>
<text x="{MARGEN}" y="{MARGEN+42}" class="t-baj" fill="{SUAVE}">Dónde corre cada pieza y cómo llega el código de una máquina a la otra</text>''')

y = CAB
X = MARGEN
PANEL_X = X + ROTULO_W
PANEL_W = W - PANEL_X - MARGEN

for nombre, alto in FILAS:
    svg.append(f'<rect x="{X}" y="{y}" width="{ROTULO_W}" height="{alto}" fill="{OSCURO}" stroke="{LINEA}" stroke-width="1"/>')
    lineas = nombre.split("\n")
    y0 = y + alto/2 - (len(lineas)-1)*10 + 5
    for i, l in enumerate(lineas):
        svg.append(f'<text x="{X+ROTULO_W/2}" y="{y0 + i*20}" class="t-rot" text-anchor="middle">{l}</text>')
    svg.append(f'<rect x="{PANEL_X}" y="{y}" width="{PANEL_W}" height="{alto}" fill="{PAPEL}" '
               f'stroke="{LINEA}" stroke-width="1"/>')
    y += alto

# ---------- fila 1: máquina de desarrollo ----------
y = CAB; px = PANEL_X + 22
svg.append(ico("laptop", px, y + 58, AZUL, 1.6, 1.3))
svg.append(caja(px + 78, y + 20,  250, 42, "splg-app-backend", "NestJS · API REST", AZUL, "engra"))
svg.append(caja(px + 78, y + 70,  250, 42, "splg-app-admin", "React + Vite", AZUL, "web"))
svg.append(caja(px + 78, y + 120, 250, 30, "splg-lib · contratos", None, AZUL))
svg.append(caja(px + 348, y + 20, 210, 42, "splg-app-cliente", "Flutter", AZUL, "celu"))
svg.append(caja(px + 348, y + 70, 210, 42, "splg-app-chofer", "Flutter", AZUL, "celu"))
svg.append(caja(px + 588, y + 20, 190, 42, "splg-bd", "PostGIS · 5432", AZUL, "base"))
svg.append(caja(px + 588, y + 70, 190, 42, "splg-redis", "Redis · 6379", AZUL, "base"))
svg.append(fle(px + 578, y + 41, px + 586, y + 41, SUAVE, "", False))
svg.append(f'<text x="{px+588}" y="{y+134}" class="t-sub" fill="{SUAVE}">Los dos motores corren en contenedores, con splg-dev.sh</text>')

# ---------- fila 2: github ----------
y += FILAS[0][1]
svg.append(ico("github", px, y + 55, OCRE, 1.6, 1.3))
svg.append(caja(px + 78, y + 22, 250, 46, "6 repositorios splg-*", "GitFlow: develop → release → main", OCRE, "github"))
svg.append(chip(px + 78,  y + 84, 118, "develop", OCRE, RELLENO_CLARO))
svg.append(chip(px + 210, y + 84, 118, "release", OCRE, RELLENO_CLARO))
svg.append(chip(px + 342, y + 84, 118, "main", OCRE, RELLENO_CLARO))
svg.append(caja(px + 500, y + 18, 278, 34, "checks.yml", None, VERDE, "check"))
svg.append(caja(px + 500, y + 58, 278, 34, "release.yml", None, VIOLETA, "reloj"))
svg.append(caja(px + 500, y + 98, 278, 34, "deploy.yml", None, ROJO, "cohete"))
svg.append(f'<text x="{px+470}" y="{y+16}" class="t-eti" fill="{SUAVE}">GitHub Actions</text>')

# ---------- fila 3: despliegue ----------
y += FILAS[1][1]
svg.append(ico("cohete", px, y + 58, ROJO, 1.6, 1.3))
svg.append(caja(px + 78, y + 55, 168, 42, "deploy.yml", "al integrar en main", ROJO, "cohete"))
svg.append(caja(px + 400, y + 18, 250, 42, "Servidor virtual (VPS)", "backend, base y caché en Docker", VERDE, "engra"))
svg.append(caja(px + 400, y + 68, 250, 42, "Servidor virtual (VPS)", "panel de administración estático", VERDE, "web"))
svg.append(fle(px + 250, y + 70, px + 396, y + 40, ROJO, "construye"))
svg.append(fle(px + 250, y + 82, px + 396, y + 89, ROJO, ""))
svg.append(caja(px + 668, y + 43, 110, 42, "Slack", "avisa", TEAL, "nube"))
svg.append(fle(px + 654, y + 64, px + 664, y + 64, TEAL, "", False))
svg.append(f'<text x="{px+78}" y="{y+120}" class="t-sub" fill="{SUAVE}">Nada llega a producción sin pasar antes por checks.yml</text>')

# ---------- fila 4: documentación ----------
y += FILAS[2][1]
svg.append(ico("web", px, y + 42, VIOLETA, 1.6, 1.3))
svg.append(caja(px + 78, y + 34, 218, 42, "publicar.sh", "se corre a mano", VIOLETA, "engra"))
svg.append(caja(px + 460, y + 34, 250, 42, "Netlify", "documentación del sistema", VERDE, "web"))
svg.append(fle(px + 300, y + 55, px + 456, y + 55, VIOLETA, "única pieza manual"))
svg.append(f'<text x="{px+78}" y="{y+96}" class="t-sub" fill="{SUAVE}">Regenera el sitio, valida el script y despliega; el resto del circuito es automático</text>')

# ---------- fila 5: servicios externos ----------
y += FILAS[3][1]
svg.append(ico("nube", px, y + 44, TEAL, 1.6, 1.3))
svg.append(caja(px + 78,  y + 36, 218, 44, "Firebase", "identidad y avisos al dispositivo", TEAL, "escudo"))
svg.append(caja(px + 310, y + 36, 218, 44, "MercadoPago", "pasarela de cobro y webhook", TEAL, "nube"))
svg.append(caja(px + 542, y + 36, 236, 44, "Slack", "aviso de cada despliegue", TEAL, "nube"))

svg.append("</svg>")
destino = D + "diagramas/uml/SPLG_Arquitectura.svg"
open(destino, "w", encoding="utf-8").write("\n".join(svg))
print(f"  ✓ SPLG_Arquitectura.svg ({os.path.getsize(destino)//1024} KB)")
