#!/usr/bin/env python3
"""Verifica que las cifras de la base que citan los documentos coincidan con la
base en ejecución: tablas, claves foráneas y tipos enumerados del dominio, y la
cantidad de conceptos idóneos del modelo conceptual (§1.2 del Documento 2) y de
clases del diagrama de dominio (§5.1 del Documento 3).

    python3 material-de-trabajo/verificar-cifras-bd.py

Sale 0 si las cifras coinciden, 1 y el detalle si alguna quedó desactualizada.
"""
import subprocess, os, re, sys

D = os.path.dirname(os.path.abspath(__file__)) + "/../"
BACK = os.path.abspath(D + "../splg-app-backend") + "/"
CONTENEDOR = "splg-bd"
env = {}
for l in open(BACK + ".env", encoding="utf-8"):
    m = re.match(r'\s*([A-Z_]+)\s*=\s*(.*)', l)
    if m: env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
USR, BD = env.get("DB_USERNAME", "postgres"), env.get("DB_NAME", "postgres")

def psql(sql):
    r = subprocess.run(["docker", "exec", CONTENEDOR, "psql", "-U", USR, "-d", BD,
                        "-At", "-c", sql], capture_output=True, text=True)
    if r.returncode:
        sys.exit("psql: " + r.stderr.strip())
    return r.stdout.strip()

SALTAR = "('migrations','spatial_ref_sys','geography_columns','geometry_columns')"
n_tablas = int(psql(f"select count(*) from information_schema.tables "
                    f"where table_schema='public' and table_type='BASE TABLE' "
                    f"and table_name not in {SALTAR};"))
n_fk = int(psql(f"select count(*) from information_schema.table_constraints "
                f"where constraint_type='FOREIGN KEY' and table_schema='public';"))
n_enum = int(psql("select count(distinct t.typname) from pg_type t "
                  "join pg_enum e on e.enumtypid=t.oid "
                  "join pg_namespace n on n.oid=t.typnamespace and n.nspname='public';"))

def contar(ruta, patron):
    return len(re.findall(patron, open(D + ruta, encoding="utf-8").read(), re.MULTILINE))

n_conceptos_conceptual = contar("diagramas/lucidchart/SPLG-modelo-conceptual.mmd", r'^\s*class \w+')
n_entidades_diseno = contar("diagramas/lucidchart/SPLG-clases-diseno-dominio.mmd", r'^\s*class \w+')

fallas = []
def check(nombre, esperado, real):
    ok = esperado == real
    print(f"[{'OK' if ok else 'FALLA':5}] {nombre}: documento dice {esperado}, la base/el código tiene {real}")
    if not ok: fallas.append(nombre)

# Lo que dicen los documentos (se transcribe la afirmación central de cada uno;
# si el texto cambia de redacción, hay que actualizar esta constante también).
DOC_TABLAS, DOC_FK, DOC_ENUM = 40, 93, 34
DOC_CONCEPTOS = 43       # 2-Analisis.md §1.2 y 1.5, material-de-trabajo/MODELO-DE-DOMINIO.md
DOC_ENTIDADES_DISENO = 43  # 3-Diseño.md §5.1: las clases del modelo conceptual, con sus operaciones

check("Tablas de dominio", DOC_TABLAS, n_tablas)
check("Claves foráneas", DOC_FK, n_fk)
check("Tipos enumerados", DOC_ENUM, n_enum)
check("Conceptos del modelo conceptual (§1.2/§1.5 Doc 2)", DOC_CONCEPTOS, n_conceptos_conceptual)
check("Clases del diagrama de clases de dominio (§5.1 Doc 3)", DOC_ENTIDADES_DISENO, n_entidades_diseno)

sys.exit(1 if fallas else 0)
