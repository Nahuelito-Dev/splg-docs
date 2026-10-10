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
import re, os, subprocess, html, sys, glob

D = os.path.dirname(os.path.abspath(__file__)) + "/"
SAL = D + "lucidchart/"

ANCHO_MIN, ALTO_FILA, ALTO_TITULO = 200, 26, 30

# ---------- lectura del diagrama de clases ----------
def leer(ruta):
    """Devuelve (clases, relaciones) de un diagrama de clases escrito en texto."""
    src = open(ruta, encoding="utf-8").read()
    clases, orden = {}, []

    # `class Id["Etiqueta"] {`: la etiqueta es el nombre que se ve (Map<String, Pedido>)
    for m in re.finditer(r'class\s+(\w+)(?:\["([^"]+)"\])?\s*\{(.*?)\}', src, re.S):
        nom, etiqueta, cuerpo = m.group(1), m.group(2), m.group(3)
        est, filas = "", []
        for l in cuerpo.split("\n"):
            l = l.strip()
            if not l: continue
            e = re.match(r'<<([^>]+)>>', l)
            if e: est = e.group(1); continue
            filas.append(l)
        clases[nom] = {"filas": filas, "est": est, "titulo": etiqueta or nom}
        orden.append(nom)

    for m in re.finditer(r'^\s*class\s+(\w+)(?:\["([^"]+)"\])?\s*$', src, re.M):
        if m.group(1) not in clases:
            clases[m.group(1)] = {"filas": [], "est": "", "titulo": m.group(2) or m.group(1)}
            orden.append(m.group(1))

    rel = []
    patron = re.compile(
        r'^\s*(\w+)\s*(?:"([^"]+)"\s*)?'      # origen y su multiplicidad
        r'(<-->|\*-->|o-->|\.\.\|>|<\|--|--\|>|\*--|--\*|o--|--o|\.\.>|<\.\.|-->|<--|--)'
        r'\s*(?:"([^"]+)"\s*)?(\w+)'          # multiplicidad del destino y destino
        r'\s*(?::\s*(.+))?$', re.M)
    for m in patron.finditer(src):
        a, ma, tipo, mb, b, et = m.groups()
        if a not in clases or b not in clases: continue
        rel.append({"a": a, "b": b, "tipo": tipo,
                    "ma": (ma or "").strip(), "mb": (mb or "").strip(),
                    "et": (et or "").strip()})
    # clase de asociación: «%% asociacion-clase Clase A B» la une con la asociación A–B
    for m in re.finditer(r'^\s*%%\s*asociacion-clase\s+(\w+)\s+(\w+)\s+(\w+)', src, re.M):
        if m.group(1) in clases:
            rel.append({"a": m.group(1), "b": m.group(1), "tipo": "ASOC",
                        "ea": m.group(2), "eb": m.group(3), "ma": "", "mb": "", "et": ""})
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
        if r["tipo"] == "ASOC": continue
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
  "<-->":  "startArrow=open;startSize=10;endArrow=open;endSize=10;",
  "*-->":  "endArrow=diamondThin;endFill=1;endSize=16;",
  "o-->":  "endArrow=diamondThin;endFill=0;endSize=16;",
  "..|>":  "dashed=1;endArrow=block;endFill=0;endSize=14;",
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
INVERTIR = {"*--", "o--", "*-->", "o-->", "<|--", "<.."}   # el simbolo va en el otro extremo

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
        c.append(f'        <mxCell id="{cid}" value="{esc(cl.get("titulo", n))}" style="swimlane;'
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

    ids_rel = {}
    for k, r in enumerate(rel):
        if r["tipo"] != "ASOC":
            ids_rel[frozenset((r["a"], r["b"]))] = f"e{k}"
    for k, r in enumerate(rel):
        if r["tipo"] == "ASOC":
            destino = ids_rel.get(frozenset((r["ea"], r["eb"])))
            if destino:
                c.append(f'        <mxCell id="e{k}" value="" style="edgeStyle=none;dashed=1;'
                         'endArrow=none;html=1;strokeColor=#2C4257;" edge="1" parent="1"'
                         f' source="{ident[r["a"]]}" target="{destino}">')
                c.append('          <mxGeometry relative="1" as="geometry" />')
                c.append('        </mxCell>')
            continue
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
# El modelo conceptual y el diagrama de clases de dominio son fijos. Las vistas por
# módulo salen de los DSD (material-de-trabajo/generar-clases-diseno.py) porque en
# un solo diagrama no entran los controladores, las fabricaciones puras, los puertos
# y las colecciones.
FUENTES = [
    ("SPLG-modelo-conceptual", "Modelo conceptual",
     "diagramas/lucidchart/SPLG-modelo-conceptual.mmd"),
    ("SPLG-diagrama-de-clases-dominio", "Diagrama de clases de diseño — dominio",
     "diagramas/lucidchart/SPLG-clases-diseno-dominio.mmd"),
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

    for viejo in glob.glob(SAL + "clases/*.xml"):
        os.remove(viejo)
    fuentes_servicios = sorted(glob.glob(D + "diagramas/lucidchart/clases/SPLG-clases-*.mmd"))
    os.makedirs(SAL + "clases/", exist_ok=True)
    for ruta in fuentes_servicios:
        modulo = re.match(r'SPLG-clases-(.+)\.mmd$', os.path.basename(ruta)).group(1)
        clases, orden, rel = leer(ruta)
        pos = acomodar(clases, orden, rel)
        destino = SAL + f"clases/SPLG-diagrama-de-clases-{modulo}.xml"
        open(destino, "w", encoding="utf-8").write(
            xml(f"Diagrama de clases — módulo {modulo}", clases, orden, rel, pos))
    if fuentes_servicios:
        print(f"  ✓ {len(fuentes_servicios)} vistas del diagrama de clases de diseño por módulo, en clases/")

    # el modelo de datos entra por otra puerta: Importar datos · ERD. Son dos esquemas: lo que la base
    # tiene hoy, y eso más lo planificado (las tablas de los módulos que todavía no se construyeron).
    import shutil
    for origen, destino, que in (
            ("SPLG-base-de-datos-lucidchart.sql", "SPLG-diagrama-de-base-de-datos.sql", "implementadas"),
            ("SPLG-base-de-datos-completa-lucidchart.sql", "SPLG-diagrama-de-base-de-datos-con-planificadas.sql",
             "implementadas y planificadas")):
        sql = D + "diagramas/base-de-datos/" + origen
        if os.path.exists(sql):
            shutil.copy(sql, SAL + destino)
            n = open(sql, encoding="utf-8").read().count("CREATE TABLE")
            print(f"  ✓ {destino}  ({n} tablas, {que})")

if __name__ == "__main__":
    main()


# ------------------------------------------------- formatos que Lucidchart acepta
# Lucidchart importa la base desde un CSV/TSV: el resultado de su propia consulta de
# PostgreSQL ("Import Data → Entity Relationship → PostgreSQL") corrida contra la base.
# Se corre contra splg_db (lo implementado) y contra una base temporal armada con el SQL
# que incluye lo planificado. Para el MC y las clases, que no son un ERD, quedan las
# fuentes en texto (Mermaid y PlantUML) para "Diagram as code".
import shutil, subprocess as _sp
_CONT = os.environ.get("SPLG_BD_CONTENEDOR", "splg-bd")
_Q = " ".join(open(D + "material-de-trabajo/lucidchart-erd-postgresql.sql", encoding="utf-8").read().split())
def _psql(base, *args, entrada=None):
    return _sp.run(["docker", "exec", "-i", _CONT, "psql", "-U", "postgres", "-d", base, "-q", *args],
                   input=entrada, capture_output=True, text=True)
def _exportar(base, nombre):
    for ext, delim in (("csv", ","), ("tsv", "\t")):
        r = _psql(base, "-c", f"\\copy ({_Q}) to stdout with (format csv, delimiter E'{delim}')")
        if r.returncode:
            print(f"  ✗ {nombre}.{ext}: {r.stderr.strip()[:200]}"); return
        open(D + f"lucidchart/{nombre}.{ext}", "w", encoding="utf-8").write(r.stdout)
    filas = r.stdout.splitlines()
    print(f"  ✓ {nombre}.csv/.tsv  ({len({f.split(chr(9))[3] for f in filas})} tablas)")
_exportar("splg_db", "SPLG-base-de-datos-lucidchart")
_psql("postgres", "-c", "drop database if exists splg_lucid_tmp")
_psql("postgres", "-c", "create database splg_lucid_tmp")
_psql("splg_lucid_tmp", entrada=open(D + "lucidchart/SPLG-diagrama-de-base-de-datos-con-planificadas.sql", encoding="utf-8").read())
_exportar("splg_lucid_tmp", "SPLG-base-de-datos-con-planificadas-lucidchart")
_psql("postgres", "-c", "drop database splg_lucid_tmp")
os.makedirs(D + "lucidchart/texto/clases", exist_ok=True)
for _src, _dst in (("diagramas/lucidchart/SPLG-modelo-conceptual.mmd", "texto/SPLG-modelo-conceptual-mermaid.txt"),
                   ("diagramas/lucidchart/SPLG-clases-diseno-dominio.mmd", "texto/SPLG-clases-diseno-dominio-mermaid.txt"),
                   ("diagramas/modelo-conceptual/MC_General.puml", "texto/SPLG-modelo-conceptual-plantuml.txt"),
                   ("diagramas/clases-diseno/DC_General.puml", "texto/SPLG-clases-diseno-general-plantuml.txt")):
    shutil.copy(D + _src, D + "lucidchart/" + _dst)
for _f in glob.glob(D + "diagramas/lucidchart/clases/SPLG-clases-*.mmd"):
    shutil.copy(_f, D + "lucidchart/texto/clases/" + os.path.basename(_f)[:-4] + "-mermaid.txt")
print("  ✓ texto/: fuentes Mermaid y PlantUML del MC y de las clases")

# La base como código Mermaid (erDiagram), una relación por clave foránea: se pega en
# Lucidchart ("Diagram as code") y entra dibujada y conectada, sin arrastrar tabla por tabla.
_sp.run([sys.executable, D + "material-de-trabajo/der-mermaid-unico.py", "splg_db", "SPLG-base-de-datos-mermaid.txt"])
_psql("postgres", "-c", "drop database if exists splg_lucid_tmp")
_psql("postgres", "-c", "create database splg_lucid_tmp")
_psql("splg_lucid_tmp", entrada=open(D + "lucidchart/SPLG-diagrama-de-base-de-datos-con-planificadas.sql", encoding="utf-8").read())
_sp.run([sys.executable, D + "material-de-trabajo/der-mermaid-unico.py", "splg_lucid_tmp", "SPLG-base-de-datos-con-planificadas-mermaid.txt"])
_psql("postgres", "-c", "drop database splg_lucid_tmp")
