#!/usr/bin/env python3
"""Verifica que el modelo conceptual (Documento 2, §1) y el modelo entidad-relación
(Documento 3, §7.4) cuenten lo mismo: los mismos conceptos, las mismas relaciones y
las cardinalidades que impone la base.

    python3 material-de-trabajo/verificar-mc-der.py

Fuente del modelo conceptual: modelo_conceptual.py. Sale 0 si todo coincide.
"""
import subprocess, os, re, sys, collections

D = os.path.dirname(os.path.abspath(__file__)) + "/../"
sys.path.insert(0, D)
import modelo_conceptual as MC
import propuesto_personal as PP
import propuesto_flota as PF
AGREGADOS = PP.AGREGADOS + PF.AGREGADOS

BACK = os.path.abspath(D + "../splg-app-backend") + "/"
env = {}
for l in open(BACK + ".env", encoding="utf-8"):
    m = re.match(r'\s*([A-Z_]+)\s*=\s*(.*)', l)
    if m: env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
USR, BD = env.get("DB_USERNAME", "postgres"), env.get("DB_NAME", "postgres")

def psql(sql):
    r = subprocess.run(["docker", "exec", os.environ.get("SPLG_BD_CONTENEDOR", "splg-bd"), "psql", "-U", USR, "-d", BD,
                        "-At", "-F", "\x1f", "-c", sql], capture_output=True, text=True)
    if r.returncode:
        sys.exit("psql: " + r.stderr.strip())
    return [l.split("\x1f") for l in r.stdout.strip("\n").split("\n") if l]

def leer(ruta):
    return open(D + ruta, encoding="utf-8").read()

PLAN = set(getattr(MC, "PLANIFICADOS", ()))   # conceptos cuya tabla todavía no está en la base
fallas = []
def check(titulo, ok, detalle=""):
    print(f"[{'OK   ' if ok else 'FALLA'}] {titulo}")
    if not ok:
        fallas.append(titulo)
        for l in detalle if isinstance(detalle, list) else [detalle]:
            print("         " + str(l))

SALTAR = "('migrations','spatial_ref_sys','geography_columns','geometry_columns')"
tablas = {t[0] for t in psql(f"select table_name from information_schema.tables where "
                             f"table_schema='public' and table_type='BASE TABLE' "
                             f"and table_name not in {SALTAR}")}
columnas = collections.defaultdict(set)
for t, c in psql("select table_name, column_name from information_schema.columns "
                 "where table_schema='public'"):
    columnas[t].add(c)
fks = [(t, c, d) for t, c, d in psql(
    "select tc.table_name, kcu.column_name, ccu.table_name "
    "from information_schema.table_constraints tc "
    "join information_schema.key_column_usage kcu on kcu.constraint_name=tc.constraint_name "
    "join information_schema.constraint_column_usage ccu on ccu.constraint_name=tc.constraint_name "
    "where tc.constraint_type='FOREIGN KEY' and tc.table_schema='public' "
    f"and tc.table_name not in {SALTAR} and ccu.table_name not in {SALTAR}")]

# Lo planificado (conceptos de MC.PLANIFICADOS): sus tablas todavía no están en la base. Se las
# lee de la propuesta que genera generar-modelo-datos.py (SQL portable del modelo completo).
sql = leer("diagramas/base-de-datos/SPLG-base-de-datos-completa-lucidchart.sql")
plan_cols, plan_fks = {}, []
for m in re.finditer(r'-- tabla propuesta\nCREATE TABLE "(\w+)" \((.*?)\n\);', sql, re.S):
    tabla = m.group(1)
    plan_cols[tabla] = set(re.findall(r'^  "(\w+)" ', m.group(2), re.M))
    plan_fks += [(tabla, c, d) for c, d in re.findall(r'FOREIGN KEY \("(\w+)"\) REFERENCES "(\w+)"', m.group(2))]
for t_, cs in plan_cols.items():
    columnas[t_] |= cs
fks += plan_fks
tablas_reales = set(tablas)
tablas |= set(plan_cols)
check("Planificados: cada concepto planificado tiene su tabla en la propuesta, y viceversa (%d)" % len(plan_cols),
      {MC.TABLA[c] for c in MC.PLANIFICADOS} == set(plan_cols),
      sorted({MC.TABLA[c] for c in MC.PLANIFICADOS} ^ set(plan_cols)))

# Las tablas planificadas ya se leyeron arriba del SQL propuesto. Faltan las columnas que los módulos
# suman a tablas que ya existen (están en los agregados) y sus claves foráneas, que el SQL declara
# dentro de la tabla existente; se agregan una sola vez, sin repetir las ya contadas.
planificadas = set(plan_cols)
for ag in AGREGADOS:
    for t, cs in ag["columnas"].items():
        for c in cs:
            columnas[t].add(c["nombre"])
fks_vistas = set(fks)
# `cylinder_recovery_notice.order_id` (módulo de recupero, planificado) no tiene todavía una asociación
# en el modelo conceptual: no es de estos módulos y no se cuenta acá.
cols_agregadas = {(t, c["nombre"]) for ag in AGREGADOS for t, cs in ag["columnas"].items() for c in cs}
for m in re.finditer(r'CREATE TABLE "(\w+)" \((.*?)\n\);', sql, re.S):
    for c, d in re.findall(r'FOREIGN KEY \("(\w+)"\) REFERENCES "(\w+)"', m.group(2)):
        if (m.group(1), c) in cols_agregadas and (m.group(1), c, d) not in fks_vistas:
            fks.append((m.group(1), c, d)); fks_vistas.add((m.group(1), c, d))

# ------------------------------------------------------------------ conceptos
analisis = leer("2-Analisis.md")
sec = analisis[analisis.index("### 1.2 Lista de Conceptos Idóneos"):analisis.index("### 1.3 Relaciones entre los Conceptos")]
en_doc = set(re.findall(r'^\|\s*\d+\s*\|\s*\*\*(\w+)\*\*', sec, re.M))
check("Conceptos: Documento 2 §1.2 = modelo conceptual (%d)" % len(MC.CLASES),
      en_doc == set(MC.CLASES),
      [f"sólo en el documento: {sorted(en_doc - set(MC.CLASES))}",
       f"sólo en el modelo: {sorted(set(MC.CLASES) - en_doc)}"])

mmd = set(re.findall(r'^\s*class (\w+)', leer("diagramas/lucidchart/SPLG-modelo-conceptual.mmd"), re.M))
check("Conceptos: el .mmd para Lucidchart tiene los mismos", mmd == set(MC.CLASES),
      sorted(mmd ^ set(MC.CLASES)))

con_tabla = {c for c, t in MC.TABLA.items() if t}
con_tabla_todos = con_tabla
tecnicas = set(MC.TABLAS_TECNICAS)
check("Tablas técnicas: existen en la base y no tienen concepto (%s)" % ", ".join(sorted(tecnicas)),
      tecnicas <= tablas and not tecnicas & {MC.TABLA[c] for c in con_tabla},
      sorted(tecnicas - tablas))
check("Conceptos con tabla: todas las tablas tienen concepto y viceversa (%d, de las cuales %d planificadas y %d técnicas)"
      % (len(tablas), len(plan_cols), len(tecnicas)),
      {MC.TABLA[c] for c in con_tabla} == tablas - tecnicas,
      [f"tablas sin concepto: {sorted(tablas - tecnicas - {MC.TABLA[c] for c in con_tabla})}",
       f"concepto sin tabla: {sorted({MC.TABLA[c] for c in con_tabla} - tablas)}"])

sin_tabla = sorted(c for c, t in MC.TABLA.items() if not t)
check("Conceptos sin tabla propia están explicados (%s)" % ", ".join(sin_tabla),
      all(c in MC.OBSERVACION for c in sin_tabla), sin_tabla)

# el DER conceptual dibuja una entidad por concepto con tabla
import glob
puml = "".join(open(f, encoding="utf-8").read()
               for f in glob.glob(D + "diagramas/base-de-datos/conceptual/SPLG-der-00-general.puml"))
ents = set(re.findall(r'^entity (\w+)', puml, re.M))
check("DER conceptual: una entidad por concepto con tabla, con el mismo nombre",
      ents == con_tabla_todos, [sorted(ents ^ con_tabla_todos)])

# ------------------------------------------------------------------- atributos
mal = []
for c, (_, atrs, _) in MC.CLASES.items():
    t = MC.TABLA[c]
    if not t or c in PLAN: continue
    for a in atrs + ([x for x in MC.CLASES["PropuestaConVigencia"][1]]
                     if any(c in h for p, h, _ in MC.GENERALIZACIONES if p == "PropuestaConVigencia") else []):
        if (c, a) in MC.ATRIBUTOS_PLANIFICADOS: continue
        col = MC.ATRIBUTOS.get(c, {}).get(a) or MC.HEREDA_ATRIBUTOS.get(a)
        if (c, a) in getattr(MC, "ATRIBUTOS_PLANIFICADOS", ()): continue
        if col not in columnas[t]:
            mal.append(f"{c}.{a} -> {t}.{col}")
check("Atributos: cada atributo del concepto tiene su columna en la base", not mal, mal)

# ------------------------------------------------------------------ relaciones
sin_asoc, sostenidas = [], collections.defaultdict(list)
for t, c, d in fks:
    a = MC.asociacion_de_fk(t, c, d)
    if a is None:
        if d == "distributor" or (t, c) in MC.AUTORIA_TECNICA:
            continue
        sin_asoc.append(f"{t}.{c} -> {d}")
    elif a[0] != "ESPECIALIZACION":
        sostenidas[(a[0], a[4], a[5])].append((t, c))
check("Relaciones: toda clave foránea es una asociación del modelo, la pertenencia a la "
      "distribuidora o una columna de autoría", not sin_asoc, sin_asoc)

sin_fk = []
for a, ma, t, mb, b, n, _ in MC.ASOCIACIONES:
    if (a, b, n) in sostenidas or (a, b, n) in MC.POLIMORFICAS: continue
    # las asociaciones de un concepto sin tabla propia se sostienen en otra tabla
    if MC.TABLA[a] is None or MC.TABLA[b] is None: continue
    # las de un concepto planificado se sostienen en tablas que todavía no existen
    if a in PLAN or b in PLAN: continue
    sin_fk.append(f"{a} {n} {b}")
check("Relaciones: toda asociación entre conceptos con tabla tiene su clave foránea",
      not sin_fk, sin_fk)

# la distribuidora: cada relación dibujada en el MC existe en la base
dist = [(a, b, n) for a, ma, t, mb, b, n, _ in MC.ASOCIACIONES if a == "Distribuidora" and b not in PLAN]
check("Distribuidora: %d asociaciones del MC, todas con clave foránea" % len(dist),
      all(k in sostenidas for k in dist), [k for k in dist if k not in sostenidas])

# ---------------------------------------------------------------- cardinalidades
unicas = {(t, c) for t, c in psql(
    "select i.indrelid::regclass::text, a.attname from pg_index i "
    "join pg_attribute a on a.attrelid=i.indrelid and a.attnum = any(i.indkey) "
    "where i.indisunique and not i.indisprimary and i.indpred is null and i.indnatts = 1")}
perfiles = [("admin", "user_id"), ("customer", "user_id"), ("delivery", "user_id")]
check("Cardinalidad: user -> admin, customer, delivery es 1 a 0..1 (clave única en la base)",
      all(p in unicas for p in perfiles), [p for p in perfiles if p not in unicas])

mer = leer("diagramas/base-de-datos/SPLG-der-mermaid.md")
malas = [l.strip() for l in mer.split("\n")
         if re.match(r'\s+(ADMIN|CUSTOMER|DELIVERY) ', l) and ' : "user_id"' in l and "|o--" not in l]
check("Cardinalidad: el DER físico dibuja los tres perfiles como 0..1", not malas, malas)
conc = "".join(open(f, encoding="utf-8").read() for f in glob.glob(D + "diagramas/base-de-datos/conceptual/*.puml"))
malas = [l for l in conc.split("\n") if re.match(r'(Administrador|Cliente|Chofer) ', l)
         and " Usuario" in l and not l.startswith(("Administrador |o--||", "Cliente |o--||", "Chofer |o--||"))]
check("Cardinalidad: el DER conceptual dibuja los tres perfiles como 0..1", not malas, malas)

# ------------------------------------------------- tabla del Documento 2 §1.3
gen = leer("diagramas/modelo-conceptual/relaciones.md").strip()
i = analisis.index("| Relación | Concepto A")
j = analisis.index("**Nota sobre Producto y Envase")
check("Relaciones: la tabla del Documento 2 §1.3 es la que sale del modelo",
      analisis[i:j].strip() == gen, "regenerar con generar-modelo-conceptual.py y pegar la tabla")

print()
n_aso = len(MC.ASOCIACIONES)
n_esp = sum(len(h) for _, h, _ in MC.GENERALIZACIONES)
print(f"{len(MC.CLASES)} conceptos · {n_aso} asociaciones · {n_esp} especializaciones · "
      f"{len(fks)} claves foráneas · {len(tablas)} tablas")
if fallas:
    print(f"\n{len(fallas)} verificación(es) fallida(s).")
    sys.exit(1)
print("Modelo conceptual y modelo entidad-relación coinciden.")
