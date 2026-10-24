#!/usr/bin/env python3
"""Verifica los diagramas de draw.io (`modelos/drawio/*.drawio`) contra su fuente.

    python3 herramientas/verificar-drawio.py

Para cada archivo cuenta las aristas que tienen `source` y `target` válidos (que no quedan flotando) y compara las
relaciones dibujadas contra la fuente:

  SPLG-DBD.drawio   las claves foráneas de la base `splg_db` (leídas en vivo) y sus 63 tablas
  SPLG-DER.drawio   las relaciones de las láminas del DER conceptual (`modelos/base-de-datos/conceptual/*.puml`)
  SPLG-MC.drawio    las asociaciones y generalizaciones de `modelo_conceptual.py`
  SPLG-DC.drawio    las relaciones del diagrama de clases de diseño (`herramientas/dc_larman.py`)

Sale 0 si no falta ninguna relación, no sobra ninguna y no hay ninguna arista suelta; si no, 1 y el detalle.
"""
import collections, glob, os, re, subprocess, sys
import xml.etree.ElementTree as ET

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
sys.path.insert(0, D + "herramientas")
sys.path.insert(0, D + "herramientas")
fallas = []


def leer(nombre):
    """(vértices, aristas) de la única página del archivo: {id: celda} y [(id, atributos, source, target)]."""
    raiz = ET.parse(D + "modelos/drawio/" + nombre + ".drawio").getroot()
    paginas = raiz.findall("diagram")
    if len(paginas) != 1:
        fallas.append(f"{nombre}: tiene {len(paginas)} páginas y tiene que tener una")
    modelo = paginas[0].find("mxGraphModel/root")
    celdas, aristas = {}, []
    for el in modelo:
        if el.tag == "object":
            c = el.find("mxCell")
            if c is not None and c.get("edge") == "1":
                aristas.append((el.get("id"), dict(el.attrib), c.get("source"), c.get("target")))
            continue
        if el.tag == "mxCell":
            if el.get("edge") == "1":
                aristas.append((el.get("id"), {}, el.get("source"), el.get("target")))
            else:
                celdas[el.get("id")] = el
    return celdas, aristas


def comparar(titulo, dibujado, esperado):
    """Compara dos Counter de relaciones; informa lo que falta y lo que sobra."""
    faltan = esperado - dibujado
    sobran = dibujado - esperado
    print(f"  {titulo}: esperadas {sum(esperado.values())} · dibujadas {sum(dibujado.values())} · "
          f"faltan {sum(faltan.values())} · sobran {sum(sobran.values())}")
    for k in list(faltan)[:8]:
        print("     falta:", k)
    for k in list(sobran)[:8]:
        print("     sobra:", k)
    if faltan or sobran:
        fallas.append(f"{titulo}: faltan {sum(faltan.values())}, sobran {sum(sobran.values())}")


def sueltas(nombre, celdas, aristas):
    """Aristas sin `source` o `target`, o que apuntan a algo que no existe."""
    ids = set(celdas) | {a[0] for a in aristas}
    malas = [a[0] for a in aristas if not a[2] or not a[3] or a[2] not in ids or a[3] not in ids]
    print(f"  aristas: {len(aristas)} · sueltas: {len(malas)}")
    if malas:
        fallas.append(f"{nombre}: {len(malas)} aristas sueltas {malas[:5]}")
    return len(malas)


def psql(sql):
    env = {}
    for l in open(D + "../splg-app-backend/.env", encoding="utf-8"):
        m = re.match(r'\s*([A-Z_]+)\s*=\s*(.*)', l)
        if m:
            env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    r = subprocess.run(["docker", "exec", os.environ.get("SPLG_BD_CONTENEDOR", "splg-bd"), "psql", "-U",
                        env.get("DB_USERNAME", "postgres"), "-d", env.get("DB_NAME", "postgres"), "-At", "-F", "\x1f", "-c", sql],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("psql: " + r.stderr.strip())
    return [l.split("\x1f") for l in r.stdout.strip("\n").split("\n") if l]


# ------------------------------------------------------------------ DBD
def verificar_dbd():
    print("SPLG-DBD.drawio")
    celdas, aristas = leer("SPLG-DBD")
    sueltas("SPLG-DBD", celdas, aristas)
    saltar = "('migrations','spatial_ref_sys','geography_columns','geometry_columns')"
    tablas = {t[0] for t in psql(f"select table_name from information_schema.tables where table_schema='public' "
                                 f"and table_type='BASE TABLE' and table_name not in {saltar}")}
    fks = collections.Counter(tuple(f) for f in psql(f"""
      select tc.table_name, kcu.column_name, ccu.table_name, ccu.column_name
      from information_schema.table_constraints tc
      join information_schema.key_column_usage kcu on kcu.constraint_name=tc.constraint_name
      join information_schema.constraint_column_usage ccu on ccu.constraint_name=tc.constraint_name
      where tc.constraint_type='FOREIGN KEY' and tc.table_schema='public' and tc.table_name not in {saltar}"""))
    dib = collections.Counter()
    for _id, at, o, d in aristas:
        co, cd = celdas.get(o), celdas.get(d)
        if co is None or cd is None:
            continue
        # el origen es la fila de la columna FK y el destino, la fila de la clave primaria destino
        fila_o, fila_d = (co.get("value") or "").split(), (cd.get("value") or "").split()
        t_o, t_d = celdas[co.get("parent")].get("value"), celdas[cd.get("parent")].get("value")
        col_o = fila_o[1] if len(fila_o) > 1 else ""
        col_d = fila_d[1] if len(fila_d) > 1 else ""
        if fila_o[:1] != ["FK"] and not (fila_o[:1] == ["PK"]):
            fallas.append(f"SPLG-DBD: la arista {_id} no sale de una fila de clave foránea ({fila_o[:2]})")
        if (at.get("tabla"), at.get("columna"), at.get("destino_tabla"), at.get("destino_columna")) != (t_o, col_o, t_d, col_d):
            fallas.append(f"SPLG-DBD: la arista {_id} dice {at.get('tabla')}.{at.get('columna')} -> "
                          f"{at.get('destino_tabla')}.{at.get('destino_columna')} pero conecta {t_o}.{col_o} -> {t_d}.{col_d}")
        dib[(t_o, col_o, t_d, col_d)] += 1
    # las tablas dibujadas: los swimlane de primer nivel que tienen filas
    padres = {c.get("parent") for c in celdas.values()}
    dibujadas = {c.get("value") for i, c in celdas.items() if i in padres and "swimlane" in (c.get("style") or "")}
    print(f"  tablas: esperadas {len(tablas)} · dibujadas {len(dibujadas)}")
    if tablas != dibujadas:
        fallas.append(f"SPLG-DBD: faltan tablas {sorted(tablas - dibujadas)} · sobran {sorted(dibujadas - tablas)}")
    fondos = [c for c in celdas.values() if "container=1" in (c.get("style") or "")]
    if fondos:
        fallas.append(f"SPLG-DBD: tiene {len(fondos)} contenedores de fondo y no tiene que tener ninguno")
    comparar("claves foráneas", dib, fks)


# ------------------------------------------------------------------ DER
def verificar_der():
    print("SPLG-DER.drawio")
    celdas, aristas = leer("SPLG-DER")
    sueltas("SPLG-DER", celdas, aristas)
    esperado = collections.Counter()
    for ruta in sorted(glob.glob(D + "modelos/base-de-datos/conceptual/SPLG-der-[0-9][0-9]-*.puml")):
        if "-00-" in ruta:
            continue                # la general reetiqueta las relaciones de Usuario con su perfil
        vistas = set()
        for l in open(ruta, encoding="utf-8"):
            m = re.match(r'^(\w+) [|}o{]+--[|}o{]+ (\w+) : (.+?)(?: \[[^\]]*\])? >$', l.strip())
            if m:
                vistas.add((m.group(1), m.group(2), m.group(3)))
        for k in vistas:
            esperado[k] += 0
        for k in vistas:
            esperado[k] = 1
    dib = collections.Counter((a["origen_nombre"], a["destino_nombre"], a["nombre"]) for _, a, _, _ in aristas)
    # las aristas deben unir las entidades que dicen
    for _id, at, o, d in aristas:
        no, nd = (celdas[o].get("value") or ""), (celdas[d].get("value") or "")
        if f"<b>{at['origen_nombre']}</b>" not in no or f"<b>{at['destino_nombre']}</b>" not in nd:
            fallas.append(f"SPLG-DER: la arista {_id} no conecta {at['origen_nombre']} con {at['destino_nombre']}")
    comparar("relaciones del DER", dib, esperado)
    ent = [c for c in celdas.values() if "<b>" in (c.get("value") or "")]
    print(f"  entidades: {len(ent)}")


# ------------------------------------------------------------------ MC
def verificar_mc():
    print("SPLG-MC.drawio")
    import modelo_conceptual as M
    celdas, aristas = leer("SPLG-MC")
    sueltas("SPLG-MC", celdas, aristas)
    esperado = collections.Counter()
    for a, ma, tipo, mb, b, nombre, _ in M.ASOCIACIONES:
        esperado[("asociacion", a, b, nombre, ma, mb)] += 1
    for padre, hijos, restr in M.GENERALIZACIONES:
        for h in hijos:
            esperado[("generalizacion", h, padre, restr, "", "")] += 1
    ca, c1, c2 = M.CLASE_ASOCIACION
    esperado[("clase_de_asociacion", ca, f"{c1}-{c2}", "clase de asociación", "", "")] += 1
    dib = collections.Counter()
    for _id, at, o, d in aristas:
        dib[(at["tipo"], at["origen_nombre"], at["destino_nombre"], at["nombre"], at.get("mult_origen", ""),
             at.get("mult_destino", ""))] += 1
        if at["tipo"] != "clase_de_asociacion":
            for ext, nombre in ((o, at["origen_nombre"]), (d, at["destino_nombre"])):
                if f"<b>{nombre}</b>" not in (celdas[ext].get("value") or ""):
                    fallas.append(f"SPLG-MC: la arista {_id} no está conectada a {nombre}")
    comparar("asociaciones, generalizaciones y clase de asociación", dib, esperado)
    print(f"  conceptos: {sum(1 for c in celdas.values() if '<b>' in (c.get('value') or ''))} de {len(M.CLASES)}")


# ------------------------------------------------------------------ DC
def verificar_dc():
    print("SPLG-DC.drawio")
    import dc_larman as X
    celdas, aristas = leer("SPLG-DC")
    sueltas("SPLG-DC", celdas, aristas)
    dc = X.construir()
    esperado = collections.Counter()
    for a in dc.asociaciones:
        esperado[("asoc_" + a["tipo"], a["a"], a["b"], a["nombre"] or "", a["ma"] or "", a["mb"] or "")] += 1
    for o, d in sorted(dc.dependencias):
        esperado[("dependencia", o, d, "«create»" if (o, d) in dc.creaciones else "", "", "")] += 1
    for ad, pu in dc.realizaciones:
        esperado[("realizacion", ad, pu, "", "", "")] += 1
    import modelo_conceptual as M
    for p, h in dc.generalizaciones:
        esperado[("generalizacion", h, p, next(x[2] for x in M.GENERALIZACIONES if x[0] == p), "", "")] += 1
    dib = collections.Counter()
    for _id, at, o, d in aristas:
        dib[(at["tipo"], at["origen_nombre"], at["destino_nombre"], at["nombre"], at.get("mult_origen", ""),
             at.get("mult_destino", ""))] += 1
        for ext, nombre in ((o, at["origen_nombre"]), (d, at["destino_nombre"])):
            if f"<b>{nombre.replace('<', '&lt;').replace('>', '&gt;')}</b>" not in (celdas[ext].get("value") or ""):
                fallas.append(f"SPLG-DC: la arista {_id} no está conectada a {nombre}")
    comparar("relaciones del diagrama de clases", dib, esperado)
    clases = [c for c in celdas.values() if "<b>" in (c.get("value") or "")]
    print(f"  clases: {len(clases)} de {len(dc.clases)}")
    if len(clases) != len(dc.clases):
        fallas.append("SPLG-DC: la cantidad de clases dibujadas no es la del diagrama de clases de diseño")


def main():
    for f in (verificar_mc, verificar_der, verificar_dbd, verificar_dc):
        f()
    print()
    if fallas:
        print("FALLAS:")
        for x in dict.fromkeys(fallas):
            print(" -", x)
        sys.exit(1)
    print("0 relaciones faltantes y 0 aristas sueltas en los cuatro diagramas.")


if __name__ == "__main__":
    main()
