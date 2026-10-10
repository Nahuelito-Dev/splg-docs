#!/usr/bin/env python3
"""Arma un solo erDiagram de Mermaid con la base entera, leída de Postgres, para pegar en
Lucidchart ("Diagram as code") y que se dibuje ya conectado: cada tabla con sus columnas
(tipo, PK, FK, UK) y una relación por cada clave foránea, con su cardinalidad real
(obligatoria u opcional según admita NULL; 1 a 1 si la columna es única).

    python3 material-de-trabajo/der-mermaid-unico.py [base]   (por omisión splg_db)

Deja lucidchart/texto/SPLG-base-de-datos-mermaid.txt.
"""
import os, sys, subprocess
D = os.path.dirname(os.path.abspath(__file__)) + "/../"
BASE = sys.argv[1] if len(sys.argv) > 1 else "splg_db"
SALIDA = sys.argv[2] if len(sys.argv) > 2 else "SPLG-base-de-datos-mermaid.txt"
CONT = os.environ.get("SPLG_BD_CONTENEDOR", "splg-bd")
SALTAR = "('migrations','spatial_ref_sys','geography_columns','geometry_columns')"

def q(sql):
    r = subprocess.run(["docker", "exec", CONT, "psql", "-U", "postgres", "-d", BASE, "-At", "-F", "\t", "-c", sql],
                       capture_output=True, text=True, check=True)
    return [l.split("\t") for l in r.stdout.splitlines() if l]

cols = q(f"""select table_name, column_name, coalesce(nullif(udt_name,''), data_type), is_nullable
  from information_schema.columns where table_schema='public' and table_name not in {SALTAR}
  order by table_name, ordinal_position""")
pk = {(t, c) for t, c in q("""select tc.table_name, kcu.column_name from information_schema.table_constraints tc
  join information_schema.key_column_usage kcu using (constraint_schema, constraint_name)
  where tc.constraint_type='PRIMARY KEY' and tc.table_schema='public'""")}
fks = q("""select tc.table_name, kcu.column_name, ccu.table_name
  from information_schema.table_constraints tc
  join information_schema.key_column_usage kcu using (constraint_schema, constraint_name)
  join information_schema.constraint_column_usage ccu using (constraint_schema, constraint_name)
  where tc.constraint_type='FOREIGN KEY' and tc.table_schema='public'""")
# columnas únicas por sí solas (constraint o índice único de una columna)
uni = {(t, c) for t, c in q("""select t.relname, a.attname from pg_index i join pg_class t on t.oid=i.indrelid
  join pg_namespace n on n.oid=t.relnamespace join pg_attribute a on a.attrelid=t.oid and a.attnum=i.indkey[0]
  where n.nspname='public' and i.indisunique and i.indnkeyatts=1 and i.indpred is null""")}
fkset = {(t, c) for t, c, _ in fks}
nulo = {(t, c): n == "YES" for t, c, _ty, n in cols}

def ident(t): return t.upper()
def tipo(ty): return ty.replace(" ", "_").replace("character_varying", "varchar")
sal = ["erDiagram"]
for t, c, dest in sorted(fks):
    hijo = "|o" if (t, c) in uni else "}o"          # muchos (o uno si la FK es única) del lado de la tabla hija
    padre = "o|" if nulo[(t, c)] else "||"          # el padre es opcional si la FK admite NULL
    sal.append(f'    {ident(t)} {hijo}--{padre} {ident(dest)} : "{c}"')
sal.append("")
tablas = sorted({t for t, *_ in cols})
for t in tablas:
    sal.append(f"    {ident(t)} {{")
    for tt, c, ty, n in cols:
        if tt != t: continue
        marcas = [m for m, ok in (("PK", (t, c) in pk), ("FK", (t, c) in fkset), ("UK", (t, c) in uni and (t, c) not in pk)) if ok]
        sal.append(f"        {tipo(ty)} {c}" + (" " + ",".join(marcas) if marcas else "") + (' "nullable"' if n == "YES" else ""))
    sal.append("    }")
os.makedirs(D + "lucidchart/texto", exist_ok=True)
open(D + "lucidchart/texto/" + SALIDA, "w", encoding="utf-8").write("\n".join(sal) + "\n")
print(f"  ✓ texto/{SALIDA}  ({len(tablas)} tablas, {len(fks)} relaciones)")
