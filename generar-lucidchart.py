#!/usr/bin/env python3
"""Convierte los diagramas de clases a archivos que Lucidchart importa directo.

    python3 generar-lucidchart.py

Lucidchart no importa PlantUML ni lee los .mmd como archivo: lo que si importa,
desde Archivo · Importar, son los diagramas de draw.io en .xml. Este script toma
los diagramas de clases escritos en el repositorio y emite ese .xml, con las
formas UML puestas donde van —el acomodo lo calcula graphviz, no queda todo
amontonado en una esquina— y con la notacion que corresponde a cada relacion:
rombo relleno para la composicion, rombo hueco para la agregacion, punta hueca
para la generalizacion, linea punteada para la dependencia y linea sin punta
para la asociacion.

El modelo de datos no pasa por aca: ese va por Importar datos · ERD con el .sql.
"""
import re, os, subprocess, html, sys

D = os.path.dirname(os.path.abspath(__file__)) + "/"
SAL = D + "lucidchart/"

ANCHO_MIN, ALTO_FILA, ALTO_TITULO = 200, 26, 30

# ---------- lectura del diagrama de clases ----------
def leer(ruta):
    """Devuelve (clases, relaciones) de un diagrama de clases escrito en texto."""
    src = open(ruta, encoding="utf-8").read()
    clases, orden = {}, []

    for m in re.finditer(r'class\s+(\w+)\s*\{(.*?)\}', src, re.S):
        nom, cuerpo = m.group(1), m.group(2)
        est, filas = "", []
        for l in cuerpo.split("\n"):
            l = l.strip()
            if not l: continue
            e = re.match(r'<<(\w+)>>', l)
            if e: est = e.group(1); continue
            filas.append(l)
        clases[nom] = {"filas": filas, "est": est}
        orden.append(nom)

    for m in re.finditer(r'^\s*class\s+(\w+)\s*$', src, re.M):
        if m.group(1) not in clases:
            clases[m.group(1)] = {"filas": [], "est": ""}
            orden.append(m.group(1))

    rel = []
    patron = re.compile(
        r'^\s*(\w+)\s*(?:"([^"]+)"\s*)?'      # origen y su multiplicidad
        r'(<\|--|--\|>|\*--|--\*|o--|--o|\.\.>|<\.\.|-->|<--|--)'
        r'\s*(?:"([^"]+)"\s*)?(\w+)'          # multiplicidad del destino y destino
        r'\s*(?::\s*(.+))?$', re.M)
    for m in patron.finditer(src):
        a, ma, tipo, mb, b, et = m.groups()
        if a not in clases or b not in clases: continue
        rel.append({"a": a, "b": b, "tipo": tipo,
                    "ma": (ma or "").strip(), "mb": (mb or "").strip(),
                    "et": (et or "").strip()})
    return clases, orden, rel

def medida(c):
    ancho = max([ANCHO_MIN] + [int(len(f) * 6.6) + 24 for f in c["filas"]]
                            + ([int(len(c["est"]) * 7) + 40] if c["est"] else []))
    alto = ALTO_TITULO + ALTO_FILA * (len(c["filas"]) + (1 if c["est"] else 0))
    return min(ancho, 460), max(alto, ALTO_TITULO + 10)

# ---------- acomodo ----------
def acomodar(clases, orden, rel):
    """Posiciones calculadas por graphviz. Sin esto Lucidchart recibe el diagrama
    con todas las cajas encimadas y hay que reacomodarlo a mano."""
    lin = ['digraph G { rankdir=TB; splines=ortho; nodesep=0.6; ranksep=1.1;',
           '  node [shape=box];']
    for n in orden:
        w, h = medida(clases[n])
        lin.append(f'  {n} [width={w/72:.3f}, height={h/72:.3f}, fixedsize=true];')
    for r in rel:
        lin.append(f'  {r["a"]} -> {r["b"]};')
    lin.append("}")
    try:
        out = subprocess.run(["dot", "-Tplain"], input="\n".join(lin),
                             capture_output=True, text=True, check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print("  ! graphviz no respondio, se acomoda en grilla:", e)
        pos, x, y, alto = {}, 40, 40, 0
        for i, n in enumerate(orden):
            w, h = medida(clases[n])
            if i and i % 5 == 0: x, y, alto = 40, y + alto + 70, 0
            pos[n] = (x, y); x += w + 60; alto = max(alto, h)
        return pos

    pos, escala, altura = {}, 90.0, 0.0
    for l in out.split("\n"):
        p = l.split()
        if p and p[0] == "graph": altura = float(p[3])
        if p and p[0] == "node" and p[1] in clases:
            w, h = medida(clases[p[1]])
            # graphviz da el centro y crece hacia arriba; draw.io usa la esquina
            # y crece hacia abajo.
            pos[p[1]] = (float(p[2]) * escala - w / 2,
                         (altura - float(p[3])) * escala - h / 2)
    if not pos: return acomodar(clases, orden, [])
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    return {n: (x - minx + 40, y - miny + 40) for n, (x, y) in pos.items()}

# ---------- estilos UML ----------
# La punta la pone draw.io del lado del destino de la arista, asi que la
# composicion y la agregacion se emiten al reves: de la parte hacia el todo.
ESTILO = {
  "--":    "endArrow=none;",
  "-->":   "endArrow=open;endSize=10;",
  "<--":   "endArrow=open;endSize=10;",
  "..>":   "dashed=1;endArrow=open;endSize=10;",
  "<..":   "dashed=1;endArrow=open;endSize=10;",
  "<|--":  "endArrow=block;endFill=0;endSize=14;",
  "--|>":  "endArrow=block;endFill=0;endSize=14;",
  "*--":   "endArrow=diamondThin;endFill=1;endSize=16;",
  "--*":   "endArrow=diamondThin;endFill=1;endSize=16;",
  "o--":   "endArrow=diamondThin;endFill=0;endSize=16;",
  "--o":   "endArrow=diamondThin;endFill=0;endSize=16;",
}
INVERTIR = {"*--", "o--", "<|--", "<.."}   # el simbolo va en el otro extremo

def esc(s): return html.escape(s, quote=True)

def xml(nombre, clases, orden, rel, pos):
    c = ['<mxfile host="app.diagrams.net" type="device">',
         f'  <diagram name="{esc(nombre)}" id="d1">',
         '    <mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1"'
         ' tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1"'
         ' pageWidth="1654" pageHeight="1169" math="0" shadow="0">',
         '      <root>',
         '        <mxCell id="0" />',
         '        <mxCell id="1" parent="0" />']
    ident = {}
    for i, n in enumerate(orden):
        cl, (x, y) = clases[n], pos.get(n, (40, 40))
        w, h = medida(cl); cid = f"c{i}"; ident[n] = cid
        c.append(f'        <mxCell id="{cid}" value="{esc(n)}" style="swimlane;'
                 'fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;'
                 'horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;'
                 'resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;'
                 'html=1;fillColor=#FFFFFF;strokeColor=#2C4257;" vertex="1" parent="1">')
        c.append(f'          <mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" as="geometry" />')
        c.append('        </mxCell>')
        fy = ALTO_TITULO
        filas = ([f"«{cl['est']}»"] if cl["est"] else []) + cl["filas"]
        for j, f in enumerate(filas):
            centrado = j == 0 and cl["est"]
            c.append(f'        <mxCell id="{cid}f{j}" value="{esc(f)}" style="text;'
                     'strokeColor=none;fillColor=none;'
                     f'align={"center" if centrado else "left"};verticalAlign=middle;'
                     'spacingLeft=6;spacingRight=6;overflow=hidden;rotatable=0;'
                     f'html=1;{"fontStyle=2;" if centrado else ""}" vertex="1" parent="{cid}">')
            c.append(f'          <mxGeometry y="{fy}" width="{w}" height="{ALTO_FILA}" as="geometry" />')
            c.append('        </mxCell>'); fy += ALTO_FILA

    for k, r in enumerate(rel):
        org, dst, ma, mb = r["a"], r["b"], r["ma"], r["mb"]
        if r["tipo"] in INVERTIR:
            org, dst, ma, mb = dst, org, mb, ma
        eid = f"e{k}"
        c.append(f'        <mxCell id="{eid}" value="{esc(r["et"])}" style="edgeStyle=orthogonalEdgeStyle;'
                 f'rounded=0;html=1;startArrow=none;startFill=0;{ESTILO[r["tipo"]]}'
                 'strokeColor=#2C4257;fontSize=11;" edge="1" parent="1"'
                 f' source="{ident[org]}" target="{ident[dst]}">')
        c.append('          <mxGeometry relative="1" as="geometry" />')
        c.append('        </mxCell>')
        for lado, txt, x in (("s", ma, -1), ("t", mb, 1)):
            if not txt: continue
            c.append(f'        <mxCell id="{eid}{lado}" value="{esc(txt)}" style="edgeLabel;'
                     'html=1;align=center;verticalAlign=middle;fontSize=11;"'
                     f' vertex="1" connectable="0" parent="{eid}">')
            c.append(f'          <mxGeometry x="{x * 0.82}" relative="1" as="geometry">'
                     '<mxPoint as="offset" /></mxGeometry>')
            c.append('        </mxCell>')

    c += ['      </root>', '    </mxGraphModel>', '  </diagram>', '</mxfile>']
    return "\n".join(c) + "\n"

# ---------- que se convierte ----------
FUENTES = [
    ("SPLG-modelo-conceptual", "Modelo conceptual",
     "diagramas/lucidchart/SPLG-modelo-conceptual.mmd"),
    ("SPLG-diagrama-de-clases-dominio", "Diagrama de clases — dominio",
     "diagramas/lucidchart/SPLG-clases-dominio.mmd"),
    ("SPLG-diagrama-de-clases-servicios", "Diagrama de clases — servicios",
     "diagramas/lucidchart/SPLG-clases-servicios.mmd"),
]

def main():
    os.makedirs(SAL, exist_ok=True)
    for archivo, titulo, fuente in FUENTES:
        ruta = D + fuente
        if not os.path.exists(ruta):
            print(f"  ! falta {fuente}"); continue
        clases, orden, rel = leer(ruta)
        pos = acomodar(clases, orden, rel)
        destino = SAL + archivo + ".xml"
        open(destino, "w", encoding="utf-8").write(xml(titulo, clases, orden, rel, pos))
        print(f"  ✓ {archivo}.xml  ({len(orden)} clases, {len(rel)} relaciones)")

    # el modelo de datos entra por otra puerta: Importar datos · ERD
    sql = D + "diagramas/base-de-datos/SPLG-base-de-datos-completa-lucidchart.sql"
    if os.path.exists(sql):
        import shutil
        shutil.copy(sql, SAL + "SPLG-diagrama-de-base-de-datos.sql")
        n = open(sql, encoding="utf-8").read().count("CREATE TABLE")
        print(f"  ✓ SPLG-diagrama-de-base-de-datos.sql  ({n} tablas)")

if __name__ == "__main__":
    main()
