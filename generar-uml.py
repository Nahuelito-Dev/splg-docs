#!/usr/bin/env python3
"""Genera los diagramas UML de nivel sistema a partir de Casos-de-Uso.md y renderiza los UML_*.puml.

    python3 generar-uml.py

Produce, en diagramas/uml/, el .puml y sus .png/.svg de:

  CU_Sistema_Actores               los cinco actores y el canal por el que operan
  CU_Sistema_Diagrama-De-Subsistemas  los subsistemas como paquetes, con los actores y el límite del sistema
  CU_Sistema_Diagrama-De-Contexto  actores contra subsistemas (limite del sistema)
  CU_Sistema_Diagrama-Completo     los N casos de uso, uno por uno, en su subsistema

Se generan y no se escriben a mano porque los tres dependen del catalogo: cada caso
nuevo cambia los conteos del contexto y agrega una elipse al completo.
"""
import re, os, glob, subprocess, sys, collections

D = os.path.dirname(os.path.abspath(__file__)) + "/"
UML = D + "diagramas/uml/"

# ---------- catalogo ----------
lin = open(D + "Casos-de-Uso.md", encoding="utf-8").read().split("\n")
a = next(i for i, x in enumerate(lin) if re.match(r'^## 4\. ', x))
b = next(i for i, x in enumerate(lin) if re.match(r'^## 5\. ', x))
blk = "\n".join(lin[a:b])

ACTOR = {"01": "Cliente", "02": "Chofer", "03": "Administrador",
         "04": "Sistema Automático", "05": "Administrador General",
         "09": "Plataforma de despliegue", "10": "Operador Técnico"}
# el campo Actor/es esta escrito de varias formas ("ACT-03 Administrador",
# "Administrador (ACT-03)", "Sistema (ACT-04)", o el nombre solo)
POR_NOMBRE = {"cliente": "01", "chofer": "02", "administrador": "03",
              "sistema automático": "04", "sistema": "04",
              "administrador general": "05",
              "plataforma de despliegue": "09", "operador técnico": "10"}

casos = {}
for m in re.finditer(r'\*\*Código:\*\*\s*(CU-\d+)\s*\|\s*\*\*Caso de Uso:\*\*\s*(.+?)\s*\n(.*?)(?=\*\*Código:\*\*|\Z)', blk, re.S):
    cod, nom, resto = m.group(1), m.group(2).strip(), m.group(3)
    def campo(n):
        mm = re.search(rf'\*\*{n}:\*\*\s*(.*?)(?=\n\s*\*\*|\n\s*---|\Z)', resto, re.S)
        return re.sub(r'\s+', ' ', mm.group(1)).strip() if mm else ""
    crudo = campo("Actor/es").split("; actores secundarios")[0]     # los secundarios salen de actores_cu.py
    act = set(re.findall(r'ACT-(\d\d)', crudo))
    if not act:
        for trozo in re.split(r'\s*[,/]\s*|\s+y\s+', crudo):
            k = POR_NOMBRE.get(trozo.strip().lower())
            if k: act.add(k)
    ss = re.match(r'(SS-\d\d)\s+(.*)', campo("Subsistema"))
    casos[cod] = {"nombre": nom, "actores": sorted(act),
                  "ss": ss.group(1) if ss else "SS-00",
                  "ssnom": ss.group(2) if ss else "Sin subsistema"}

# estado de cada caso, del artefacto expandido: los planificados (no construidos)
# se dibujan con otro color en el diagrama de su subsistema
a2 = next(i for i, x in enumerate(lin) if re.match(r'^## 5\. ', x))
b2 = next(i for i, x in enumerate(lin) if re.match(r'^## 6\. ', x))
blk2 = "\n".join(lin[a2:b2])
# El encabezado puede traer uno o dos marcadores antes del codigo
# ("Importante · automático CU-105"): con \S+ se salteaban esos casos y los
# cuatro modulos inteligentes salian dibujados como si estuvieran construidos.
for m in re.finditer(r'^####\s+.*?(CU-\d+)\s+—.*?\|\s*\*\*Estado\*\*\s*\|\s*([^|]+)\|', blk2, re.S | re.M):
    if m.group(1) in casos:
        casos[m.group(1)]["planificado"] = not m.group(2).strip().lower().startswith("implementado")

SS = {}
for v in casos.values():
    SS.setdefault(v["ss"], v["ssnom"])
subs = sorted(SS)

# los colores viven en paleta.py: los usa tambien el generador del sitio
from paleta import TINTE, BORDE, COLOR_ACT

# Relaciones entre casos de uso. El catalogo no las tiene: dicen que una operacion
# necesita de otra —tipicamente, escribir sobre algo exige leerlo antes—, y son lo
# que la catedra pidio que se viera en los diagramas de cada ABM.
from relaciones_cu import INCLUYE, INCLUYE_EXTERNO, EXTIENDE, extensiones, pe_id

# Casos de uso factorizados: comportamiento comun que otros casos reutilizan
# (<<include>>) o que se agrega solo si se cumple una condicion (<<extend>>).
# No llevan codigo CU-XXX porque no son algo que el actor pida por separado:
# son parte de otro caso. Se dibujan igual porque la tabla 7.7 del Doc 1 los
# declara y la catedra pide ver la relacion en el diagrama.
FACTORIZADO = {}   # no hay casos de uso factorizados: un caso incluido o una extensión tiene código propio

INCLUYE_FACTOR = {}

# ---------- actores secundarios y generalizacion ----------
# Los tres actores externos no estan en el campo Actor/es de los casos: ese campo
# nombra al actor principal, el que inicia el caso. Estos son secundarios: el
# sistema los invoca. Cada lista sale de los adaptadores del backend:
#   ACT-06  payments/infrastructure/mercadopago.adapter.ts  (checkout y webhook)
#   ACT-07  firebase/infrastructure/firebase-auth.adapter.ts (identidad) y
#           fcm.adapter.ts (push)
#   ACT-08  email/infrastructure/resend-email.adapter.ts
ACTOR_EXT = {"06": "MercadoPago", "07": "Firebase", "08": "Servicio de correo"}
from actores_cu import SECUNDARIO
# El Administrador General hace todo lo que hace el Administrador y ademas lo que
# es exclusivo suyo: ACT-05 especializa a ACT-03.
GENERALIZA = ("05", "03")
ESP, GEN = GENERALIZA

def directos(cu):
    """Los actores que el catálogo asigna al caso, todos: la asociación de ACT-05 se dibuja aunque ACT-03 también
    esté, porque la generalización no reemplaza a las líneas."""
    return list(casos[cu]["actores"])


CABECERA = "!include ../estilo-vp.iuml"

def escribir(nombre, texto):
    p = UML + nombre + ".puml"
    open(p, "w", encoding="utf-8").write(texto)
    return p

SUBSISTEMAS = []
# hasta cuantas bases puede tener un caso incluido para separarlo de su actor (ver seccion 6)
BASES_MAX_SEPARAR = 8
BASES_MAX_POR_SS = {"SS-07": 16}
# Un subsistema con ~50 casos y ~45 asociaciones de un mismo actor no se lee en una sola
# lamina: se parte en varios diagramas, cada uno con su limite, sus actores y sus
# <<include>> completos. La ultima parte (None) toma todo el resto; un caso incluido por
# casos de dos partes se dibuja en cada una, para que la flecha nunca quede sin destino.
PARTES = {
  "SS-07": [("Choferes", "Choferes",
             {"CU-031", "CU-032", "CU-033", "CU-034", "CU-035", "CU-049", "CU-096", "CU-097",
              "CU-109", "CU-110", "CU-115", "CU-138", "CU-267", "CU-271"}),
            ("Vehiculos", "Vehículos y vencimientos",
             {"CU-051", "CU-105", "CU-111", "CU-112", "CU-113", "CU-114", "CU-136", "CU-137",
              "CU-139", "CU-140", "CU-141", "CU-142", "CU-161", "CU-162", "CU-163", "CU-164",
              "CU-165", "CU-247"}),
            ("Costos-Siniestros-Y-Adjuntos", "Costos, siniestros y adjuntos de flota", None)],
}
SEPARAR_ACTOR_DE_INCLUIDO = {"SS-02", "SS-07", "SS-19", "SS-21"}

def eid(c): return c.replace("-", "_") if c.startswith("F-") else "U" + c.replace("CU-", "")
def parte(txt, ancho=26):
    """Corta el nombre en lineas para que la elipse no salga apaisada."""
    out, l = [], ""
    for w in txt.split():
        if len(l) + len(w) + 1 > ancho and l: out.append(l); l = w
        else: l = (l + " " + w).strip()
    if l: out.append(l)
    return "\\n".join(out)

# ---------- 1. actores ----------
# Los actores se asocian a casos de uso (no a componentes del sistema): cada uno con
# los casos que mejor lo representan. Los tres externos son secundarios: no inician
# nada, el sistema los invoca durante el caso.
REPRESENTATIVOS = {
  "01": ["CU-005", "CU-023", "CU-072"],
  "02": ["CU-015", "CU-018", "CU-020"],
  "03": ["CU-012", "CU-025", "CU-026"],
  "05": ["CU-052"],
  "04": ["CU-014", "CU-075"],
  "10": ["CU-087"],
}
EXT_REPRESENTATIVO = {"07": "CU-001", "08": "CU-047"}
PRIMARIO_EXT = {"09": "CU-104", "06": "CU-048"}
PRIMARIO_EXT_ACT = set(PRIMARIO_EXT)
# Se dibuja con el mismo formato que los diagramas de casos de uso (actores a la izquierda, casos a la
# derecha), así que se compone en uml_lamina.py una vez que están calculadas las relaciones (sección 3).
usados = sorted({c for v in REPRESENTATIVOS.values() for c in v} | set(EXT_REPRESENTATIVO.values()) | set(PRIMARIO_EXT.values()))

# ---------- 2. contexto ----------
# Un subsistema NO es un caso de uso: la elipse esta reservada para el caso de
# uso. Un subsistema se dibuja como paquete. Y un diagrama de contexto muestra
# ademas con que sistemas externos habla el nuestro, que es lo que faltaba.
cnt = collections.Counter(v["ss"] for v in casos.values())
_orden_ctx = ["01", "02", "03", "05", "04", "10", "06", "07", "08", "09"]
_lineas_ss = [f'{s_}  {SS[s_]}  ({cnt[s_]})' for s_ in subs]
ROL = {"01": "pide, sigue y reclama sus pedidos", "02": "recibe ofertas y entrega",
       "03": "gestiona su distribuidora", "05": "gestiona todas las distribuidoras",
       "04": "ejecuta los procesos programados", "10": "pone en marcha el sistema desde el servidor",
       "06": "cobra y recibe el aviso de pago", "07": "identidad y avisos push",
       "08": "correos transaccionales", "09": "sondea la salud del sistema"}

# ---------- 3. completo ----------
def relaciones():
    """<<include>> y <<extend>> de todos los subsistemas, sin repetir. Es la misma
    lista que dibujan los diagramas por subsistema (seccion 6)."""
    inc, ext = [], []
    for s in subs:
        for a, b in INCLUYE.get(s, []):
            if a in casos and b in casos and casos[a]["ss"] == s and casos[b]["ss"] == s:
                inc.append((a, b))
        inc += INCLUYE_FACTOR.get(s, [])
        ext += EXTIENDE.get(s, [])
    inc += [(a, b) for a, b in INCLUYE_EXTERNO
            if a in casos and b in casos and casos[a]["ss"] != casos[b]["ss"]]
    visto = set()
    inc = [x for x in inc if not (x in visto or visto.add(x))]
    return inc, ext

# El actor es externo al sistema: va afuera del limite y una sola vez. Los
# humanos a la izquierda; a la derecha, el Sistema Automatico y los tres
# sistemas externos.
IZQ = ["01", "02", "03", "05"]
DER = ["04", "06", "07", "08", "09"]
NOMBRE_ACT = {**ACTOR, **ACTOR_EXT}
LIMITE_TXT = "Sistema de Pedidos y Logística de Garrafas de Gas (SPLG)"

# Los diagramas de casos de uso se componen en uml_lamina.py, con el mismo formato en todos:
# los actores en una columna a la izquierda y, dentro del límite del sistema, los casos de uso
# apilados en una columna con sus relaciones «include» y «extend» a la derecha. Salen como SVG.
import uml_lamina, json
inc, ext = relaciones()
# Los casos factorizados no son casos de uso del catalogo (no llevan codigo): se
# dibujan en los diagramas de cada subsistema, que declaran sus relaciones, y no en
# las laminas, que muestran solo los casos numerados.
inc = [(a, b) for a, b in inc if not (a.startswith("F-") or b.startswith("F-"))]
ext = [(a, b, p) for a, b, p in ext if not (a.startswith("F-") or b.startswith("F-"))]
LAMINAS = {}
# El diagrama completo se dibuja con una lámina por actor: a la izquierda ese único actor, y a la derecha,
# dentro del límite del sistema, una columna con todos sus casos de uso agrupados por subsistema, con los
# «include» y «extend» a su derecha. Un caso incluido o extendido que no es de ese actor se dibuja como
# referencia (borde discontinuo) en un recuadro aparte. Un actor con muchos casos se parte por subsistema.
REF = "REF"
MAX_POR_LAMINA = 22
LAMINAS_COMPLETO = []
RELACIONES_JSON = {"laminas": {}, "subsistemas": {}}
ORDEN_ACT = ["01", "02", "03", "05", "04", "10", "06", "07", "08", "09"]
ORDEN_LAMINAS = ["01", "02", "03", "05", "04", "10", "06", "07", "08", "09"]

def _asociaciones(cs, quienes):
    a = [(k, c, "principal") for c in cs for k in directos(c) if k in quienes]
    for k, v in SECUNDARIO.items():
        a += [(k, c, "secundario") for c in v if c in cs and k in quienes]
    return a

def _slug(txt):
    import unicodedata
    s = unicodedata.normalize("NFD", txt)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return "-".join(w[0].upper() + w[1:] for w in s.replace("/", " ").split())

ALTO_MAX = 1600                 # alto máximo de una lámina (en unidades del SVG; el PNG sale al doble)
_lam_n = 0
_plan_lam = []          # (actor, parte, partes, casos)

import uml_completo
NOTAS_3COL = ["Tres columnas: el actor, los casos de uso que inicia y, a la derecha, los casos relacionados con ellos por «include» o «extend».",
              "Asociación actor–caso de uso: línea continua sin punta · «include»: del caso base al incluido · «extend»: del caso que extiende al caso base "
              "(línea discontinua, con su punto de extensión PE-n, que figura también en el compartimiento «puntos de extensión» del caso base).",
              "Cada «include» y cada «extend» tiene su propio trazo, con el rótulo junto a su arranque. Con relleno rosado, los casos de uso planificados; "
              "con borde discontinuo, los casos de uso que no inicia el actor de este diagrama o que son de otro subsistema, solo como referencia."]

def _svg_lamina(_k, _i, _np, _propios):
    _ajenos = set()
    for a, b in inc:
        if (a in _propios) != (b in _propios): _ajenos.add(b if a in _propios else a)
    for a, b, _p in ext:
        if (a in _propios) != (b in _propios): _ajenos.add(b if a in _propios else a)
    _casos = {c: dict(casos[c]) for c in _propios}
    for c in _ajenos:
        _casos[c] = {**casos[c], "nombre": f'{casos[c]["nombre"]} ({casos[c]["ss"]})'}
    _rel = [("include", a, b, None) for a, b in inc if a in _casos and b in _casos and (a in _propios or b in _propios)]
    _rel += [("extend", a, b, p) for a, b, p in ext if a in _casos and b in _casos and (a in _propios or b in _propios)]
    _nom = NOMBRE_ACT[_k]
    _parte = f" — parte {_i} de {_np}" if _np > 1 else ""
    _act = {c: [_k] for c in _propios}
    for c in _ajenos: _act[c] = []
    return uml_completo.completo(
        _casos, _act, NOMBRE_ACT, _rel, ESP, GEN, LIMITE_TXT,
        f"Diagrama de casos de uso — {_nom} (ACT-{_k}){_parte} · {len(_propios)} casos de uso",
        ref=_ajenos, orden=lambda c: (casos[c]["ss"], c), notas=NOTAS_3COL)

def _alto(svg_txt):
    return float(re.search(r'height="([\d.]+)"', svg_txt[:600]).group(1))

def _grupos_por_ss(bloques, n):
    m = len(bloques); pref = [0]
    for b_ in bloques: pref.append(pref[-1] + len(b_))
    INF = 10 ** 9
    dp = [[(INF, None)] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = (0, None)
    for p in range(1, n + 1):
        for j in range(1, m + 1):
            for i2 in range(p - 1, j):
                v = max(dp[p - 1][i2][0], pref[j] - pref[i2])
                if v < dp[p][j][0]: dp[p][j] = (v, i2)
    cortes, j = [], m
    for p in range(n, 0, -1):
        i2 = dp[p][j][1]; cortes.append((i2, j)); j = i2
    cortes.reverse()
    return [[c for blq in bloques[i2:j2] for c in blq] for i2, j2 in cortes]

for _k in ORDEN_LAMINAS:
    _suyos = {c for c in casos if _k in directos(c)} | set(SECUNDARIO.get(_k, []))
    # los bloques por subsistema; uno muy grande se corta en trozos de a lo sumo 18 casos
    _bloques = []
    for s in subs:
        v = sorted(c for c in _suyos if casos[c]["ss"] == s)
        for i0 in range(0, len(v), 22):
            if v[i0:i0 + 22]: _bloques.append(v[i0:i0 + 22])
    _elegido = None
    for _n_partes in range(max(1, -(-len(_suyos) // 30)), len(_bloques) + 1):
        _gs = _grupos_por_ss(_bloques, _n_partes)
        _elegido = _gs
        if all(_alto(_svg_lamina(_k, i_, len(_gs), set(g_))) <= ALTO_MAX for i_, g_ in enumerate(_gs, 1)):
            break
    for _i, _g in enumerate(_elegido, 1):
        _plan_lam.append((_k, _i, len(_elegido), set(_g)))

# los casos incluidos (que ningún actor inicia) no tienen lámina propia: figuran en el diagrama único y como referencia
for _k, _i, _np, _propios in _plan_lam:
    _lam_n += 1
    _n = f"CU_Sistema_Completo-Lamina-{_lam_n:02d}_{_slug(NOMBRE_ACT[_k])}" + (f"_Parte-{_i}" if _np > 1 else "")
    LAMINAS[_n] = _svg_lamina(_k, _i, _np, _propios)
    LAMINAS_COMPLETO.append(_n)

# ---- el diagrama de casos de uso del sistema, completo, en una sola imagen ----
# Un bloque por subsistema; a su izquierda, la figura de cada actor que participa en él, unida a todos sus casos.
import uml_completo
_actores_de = {c: sorted(set(directos(c)) | {k for k, v in SECUNDARIO.items() if c in v}) for c in casos}
_rel_c = [("include", a, b, None) for a, b in inc] + [("extend", a, b, p) for a, b, p in ext]
LAMINAS["CU_Sistema_Diagrama-Completo"] = uml_completo.completo(
    {c: dict(casos[c]) for c in casos}, _actores_de, NOMBRE_ACT, _rel_c, ESP, GEN,
    LIMITE_TXT, f"Diagrama de casos de uso del sistema — SPLG ({len(casos)} casos de uso)", copias=26)

_casos_act = {c: dict(casos[c]) for c in usados}
_asoc_act = [(k, c, "principal") for k, lst in REPRESENTATIVOS.items() for c in lst]
_asoc_act += [(k, c, "secundario") for k, c in EXT_REPRESENTATIVO.items()]
_asoc_act += [(k, c, "principal") for k, c in PRIMARIO_EXT.items()]
LAMINAS["CU_Sistema_Actores"] = uml_lamina.columna(
    _casos_act, [{"id": "ACT", "titulo": "Casos de uso representativos", "casos": usados}], NOMBRE_ACT,
    ["01", "02", "03", "05", "04", "10", "06", "07", "08", "09"], _asoc_act, [], ESP, GEN, LIMITE_TXT,
    "Actores del sistema y el canal por el que operan — SPLG", leyenda=False)
LAMINAS["CU_Sistema_Diagrama-De-Contexto"] = uml_lamina.contexto(
    _orden_ctx, NOMBRE_ACT, ROL, _lineas_ss, ESP, GEN, "Sistema de Pedidos y Logística de Garrafas de Gas (SPLG)",
    "Diagrama de Contexto del Sistema — SPLG")
import uml_subsistemas
_ad_ss = {s_: set() for s_ in subs}
for _c_ in casos:
    _ad_ss[casos[_c_]["ss"]] |= set(directos(_c_)) | {k_ for k_, v_ in SECUNDARIO.items() if _c_ in v_}
LAMINAS["CU_Sistema_Diagrama-De-Subsistemas"] = uml_subsistemas.subsistemas(
    subs, SS, cnt, _ad_ss, NOMBRE_ACT, ESP, GEN, LIMITE_TXT,
    f"Diagrama de casos de uso del sistema por subsistemas — SPLG ({len(subs)} subsistemas · {len(casos)} casos de uso)")
LAMINAS["CU_Sistema_Mapa"] = uml_lamina.mapa(
    casos, subs, SS, NOMBRE_ACT, ORDEN_ACT, directos, SECUNDARIO, ESP, GEN, LIMITE_TXT)
for _n, _svg in LAMINAS.items():
    open(UML + _n + ".svg", "w", encoding="utf-8").write(_svg)
    if os.path.exists(UML + _n + ".puml"): os.remove(UML + _n + ".puml")
# el completo en una sola imagen ya no existe: lo reemplazan las seis láminas



# ---------- 4. mapa de subsistemas ----------
# La catedra dijo que el de subsistemas se veia mal. Era un flowchart de cajas sueltas
# dentro de dos marcos: no mostraba ninguna relacion, y sin relaciones no es un diagrama
# sino una lista dibujada. Este dice quien depende de quien.
NEGOCIO = ["SS-01","SS-02","SS-03","SS-04","SS-05","SS-06","SS-07","SS-08","SS-09",
           "SS-11","SS-12","SS-13","SS-14","SS-15","SS-19","SS-20","SS-21"]
DEPENDE = [
  ("SS-02","SS-01","el pedido es de un cliente"), ("SS-02","SS-08","toma precio y stock"),
  ("SS-02","SS-09","reserva cupo de franja"), ("SS-02","SS-11","valida cobertura"),
  ("SS-02","SS-14","cobra"),
  ("SS-03","SS-02","despacha pedidos"), ("SS-03","SS-07","ofrece a los choferes"),
  ("SS-04","SS-03","sigue al chofer asignado"), ("SS-04","SS-17","avisa cada cambio"),
  ("SS-05","SS-02","reclama sobre un pedido"),
  ("SS-06","SS-02","mide ventas"), ("SS-06","SS-14","concilia cobros"),
  ("SS-12","SS-02","registra sobre la entrega"), ("SS-12","SS-07","califica al chofer"),
  ("SS-13","SS-02","asigna envases al pedido"), ("SS-13","SS-08","el envase es de un tipo"),
  ("SS-15","SS-02","la reserva se convierte en pedido"), ("SS-15","SS-14","toma la seña"),
  ("SS-19","SS-01","otorga cuentas de acceso"), ("SS-19","SS-07","comparte vencimientos y bloqueo de despacho"),
  ("SS-20","SS-08","la recepción acredita el stock"), ("SS-08","SS-02","descuenta lo entregado"),
  ("SS-08","SS-07","carga el camión del chofer"),
  ("SS-16","SS-01","administra las cuentas"), ("SS-17","SS-01","avisa a los usuarios"),
  ("SS-21","SS-02","rinde y cobra a cuenta los pedidos"), ("SS-21","SS-07","rinde y liquida a los choferes"),
]
mapa = ["@startuml", f"title Subsistemas del Proyecto — SPLG ({len(subs)} subsistemas · {len(casos)} casos de uso)",
        CABECERA, "skinparam nodesep 25", "skinparam ranksep 55",
        "", "left to right direction", ""]
def paquete(s, sangria):
    i = subs.index(s); n = cnt[s]
    return (f'{sangria}package "{s} {SS[s]}\\n({n} caso{"s" if n != 1 else ""} de uso)" as M{s.replace("-","")} '
            '<<subsystem>> #back:C6DAF0;line:3C5F8F ' + "{")
for alias, grupo, titulo, borde in (("GNEG", NEGOCIO, "Subsistemas de negocio", "3C6E8F"),
                                    ("GSOP", [s for s in subs if s not in NEGOCIO],
                                     "Subsistemas de soporte", "5A5896")):
    mapa.append(f'package "{titulo}" as {alias} #back:FFFFFF;line:{borde} ' + "{")
    for s in grupo:
        mapa.append(paquete(s, "  ")); mapa.append("  }")
    mapa.append("}")
mapa.append("")
def nodo(s):
    return "M" + s.replace("-", "")
for a, b, que in DEPENDE:
    if a in SS and b in SS:
        mapa.append(f'{nodo(a)} ..> {nodo(b)} : {que}')
# SS-10 es un subsistema como los demas; lo que lo distingue es que acota a todos los de negocio
mapa.append('GNEG ..> MSS10 : acotados a la distribuidora del usuario')
mapa += ["", "@enduml"]
escribir("CU_Sistema_Subsistemas", "\n".join(mapa))
SUBSISTEMAS.append("CU_Sistema_Subsistemas")


# ---------- 6. un diagrama por subsistema ----------
NOMBRE_SS = {"SS-01": "CU_SS-01_Autenticacion-Y-Usuarios", "SS-02": "CU_SS-02_Gestion-De-Pedidos",
             "SS-03": "CU_SS-03_Despacho-Y-Asignacion", "SS-04": "CU_SS-04_Seguimiento-En-Tiempo-Real",
             "SS-05": "CU_SS-05_Reclamos", "SS-06": "CU_SS-06_Reportes-Y-Dashboard",
             "SS-08": "CU_SS-08_Gestion-De-Productos", "SS-09": "CU_SS-09_Franjas-Horarias",
             "SS-10": "CU_SS-10_Multi-Distribuidora", "SS-11": "CU_SS-11_Cobertura-Geografica",
             "SS-12": "CU_SS-12_Incidencias-Y-Calidad-De-Servicio", "SS-13": "CU_SS-13_Trazabilidad-De-Envases",
             "SS-14": "CU_SS-14_Pagos-Y-Conciliacion", "SS-15": "CU_SS-15_Reservas-Programadas",
             "SS-16": "CU_SS-16_Administracion-De-Cuentas-Y-Roles", "SS-17": "CU_SS-17_Notificaciones-Y-Mensajeria",
             "SS-18": "CU_SS-18_Observabilidad-Y-Operacion", "SS-19": "CU_SS-19_Personal-Y-Legajos",
             "SS-20": "CU_SS-20_Compras", "SS-21": "CU_SS-21_Caja-Rendiciones-Y-Cuentas-Corrientes"}
# Estaban escritos a mano y se quedaron cortos: SS-02 mostraba once casos cuando ya
# eran veinticuatro. Se generan del catalogo para que ninguno quede incompleto.
unidades = []
MAX_CASOS = 32          # más casos que éstos no se leen en una imagen: el subsistema se parte en partes

def _partir(s, todos):
    """Parte un subsistema grande en grupos de a lo sumo MAX_CASOS casos, sin separar un caso de los
    que se relacionan con él (include/extend dentro del subsistema) más de lo necesario."""
    padre = {c: c for c in todos}
    def raiz(c):
        while padre[c] != c:
            padre[c] = padre[padre[c]]; c = padre[c]
        return c
    for a_, b_ in INCLUYE.get(s, []):
        if a_ in padre and b_ in padre: padre[raiz(a_)] = raiz(b_)
    for a_, b_, _p in EXTIENDE.get(s, []):
        if a_ in padre and b_ in padre: padre[raiz(a_)] = raiz(b_)
    comp = collections.defaultdict(list)
    for c in todos: comp[raiz(c)].append(c)
    comps = sorted((sorted(v) for v in comp.values()), key=lambda v: v[0])
    partes_n = -(-len(todos) // MAX_CASOS)
    for tope in range(-(-len(todos) // partes_n), MAX_CASOS + 1):   # lo más parejas que se pueda, sin pasar de MAX_CASOS
        grupos, actual = [], []
        for v in comps:
            if actual and len(actual) + len(v) > tope:
                grupos.append(actual); actual = []
            actual += v
        if actual: grupos.append(actual)
        if len(grupos) <= partes_n:
            break
    return [sorted(g_) for g_ in grupos]

for i, s in enumerate(subs):
    todos = sorted(c for c in casos if casos[c]["ss"] == s)
    if s in PARTES:
        asignados = set().union(*[m for _, _, m in PARTES[s] if m])
        for suf, tit, m in PARTES[s]:
            miembros = set(m) if m else {c for c in todos if c not in asignados}
            miembros |= {b for a, b in INCLUYE.get(s, []) if a in miembros and b in casos and casos[b]["ss"] == s}
            unidades.append((i, s, f"CU_{s}_{suf}", tit, sorted(miembros)))
    elif len(todos) > MAX_CASOS:
        gs = _partir(s, todos)
        for k, g_ in enumerate(gs, 1):
            unidades.append((i, s, f"{NOMBRE_SS[s]}_Parte-{k}", f"parte {k} de {len(gs)}", g_))
    else:
        unidades.append((i, s, NOMBRE_SS[s], None, todos))
for i, s, nombre, tit, cs in unidades:
    quienes = {k for c in cs for k in casos[c]["actores"]}
    # el Administrador General especializa al Administrador: si participa uno de los
    # dos, se dibujan ambos y la generalizacion, para que se lea por que ACT-05 no
    # repite las asociaciones que hereda
    if ESP in quienes or GEN in quienes:
        quienes |= {ESP, GEN}
    # actores secundarios: el sistema los invoca durante el caso
    sec = {k: [c for c in SECUNDARIO[k] if c in cs] for k in sorted(SECUNDARIO)}
    sec = {k: v for k, v in sec.items() if v}
    quienes |= set(sec)
    ext_s = [(a, b, p_) for a, b, p_ in EXTIENDE.get(s, []) if a in cs or (b in cs and casos[b]["ss"] == s)]
    inc_f = [(a, b) for a, b in INCLUYE_FACTOR.get(s, []) if b in cs or b not in casos]
    usados_f = sorted({x for a, b in inc_f for x in (a, b) if x.startswith("F-")}
                      | {a for a, b, _ in ext_s if a.startswith("F-")})
    # casos de otro subsistema que alguno de este incluye, o que incluyen a uno de este: referencia
    externos = [(a, b) for a, b in INCLUYE_EXTERNO if a in cs and b in casos and casos[b]["ss"] != s]
    bases_ext = [b for a, b, _ in ext_s if b in casos and casos[b]["ss"] != s]
    entrantes = [(a, b) for a, b in INCLUYE_EXTERNO if a in casos and b in cs and casos[a]["ss"] != s]
    # las relaciones del mismo subsistema que cruzan a otra parte: el otro extremo va de referencia
    mismas = [(a, b) for a, b in INCLUYE.get(s, []) if a in casos and b in casos and casos[a]["ss"] == s
              and casos[b]["ss"] == s and ((a in cs) != (b in cs))]
    mismas_ext = [(a, b, p_) for a, b, p_ in ext_s if a in casos and b in casos and casos[a]["ss"] == s
                  and casos[b]["ss"] == s and ((a in cs) != (b in cs))]
    ajenos = sorted({b for _, b in externos} | set(bases_ext) | {a for a, _ in entrantes}
                    | {x for a, b in mismas for x in (a, b) if x not in cs}
                    | {x for a, b, _ in mismas_ext for x in (a, b) if x not in cs})
    _c = {c: dict(casos[c]) for c in cs}
    for b_ in ajenos:
        _c[b_] = {**casos[b_], "nombre": f'{casos[b_]["nombre"]} ({casos[b_]["ss"]})'}
    rel = [("include", a, b, None) for a, b in INCLUYE.get(s, []) if a in cs and b in cs]
    rel += [("include", a, b, None) for a, b in externos + entrantes + mismas]
    rel += [("extend", a, b, p_) for a, b, p_ in ext_s if not ((a in casos and b in casos and casos[a]["ss"] == s and casos[b]["ss"] == s and (a in cs) != (b in cs)))]
    rel += [("extend", a, b, p_) for a, b, p_ in mismas_ext]
    rel = [r for r in rel if r[1] in _c and r[2] in _c]
    _act = {c: sorted(set(directos(c)) | {k for k, v in SECUNDARIO.items() if c in v}) for c in cs}
    for c in ajenos: _act[c] = []
    LAMINAS[nombre] = uml_completo.completo(
        _c, _act, NOMBRE_ACT, rel, ESP, GEN, LIMITE_TXT,
        f"{s} — {SS[s]}{': ' + tit if tit else ''} ({len(cs)} {'caso' if len(cs) == 1 else 'casos'} de uso)",
        ref=set(ajenos), notas=NOTAS_3COL)
    open(UML + nombre + ".svg", "w", encoding="utf-8").write(LAMINAS[nombre])
    if os.path.exists(UML + nombre + ".puml"): os.remove(UML + nombre + ".puml")
    SUBSISTEMAS.append(nombre)

# ---------- render ----------
objetivo = sys.argv[1:] or (list(dict.fromkeys(list(LAMINAS) + SUBSISTEMAS)))
for n in objetivo:
    if n in LAMINAS:
        # el SVG ya esta escrito; el PNG sale al doble de tamano para poder imprimirlo
        _h = float(re.search(r'height="([\d.]+)"', open(UML + n + ".svg", encoding="utf-8").read(2000)).group(1))
        _z = min(2.0, 32000 / _h)       # rsvg-convert no pasa de 32767 px: el diagrama completo sale a la escala que entra
        r = subprocess.run(["rsvg-convert", "-z", f"{_z:.3f}", "-o", UML + n + ".png", UML + n + ".svg"],
                           capture_output=True, text=True)
        if r.returncode: print(f"  ✗ {n}.png: {r.stderr.strip()[:300]}")
    else:
        for fmt in ("png", "svg"):
            # PlantUML corta la imagen a 4096 px: un subsistema grande se pierde sin avisar
            r = subprocess.run(["plantuml", "-t" + fmt, "-charset", "UTF-8", UML + n + ".puml"],
                               capture_output=True, text=True,
                               env={**os.environ, "PLANTUML_LIMIT_SIZE": "16384"})
            if r.returncode:
                print(f"  ✗ {n}.{fmt}: {r.stderr.strip()[:300]}"); continue
    p = UML + n + ".png"
    if os.path.exists(p):
        print(f"  ✓ {n}  ({os.path.getsize(p)//1024} KB)")
# ---------- diagramas de comportamiento y arquitectura ----------
# Estados, actividad, componentes, despliegue y Gantt: se escriben a mano en
# diagramas/uml/UML_*.puml porque salen del codigo y del plan, no del catalogo.
if not sys.argv[1:]:
    for p in sorted(glob.glob(UML + "UML_*.puml")):
        n = os.path.basename(p)[:-5]
        for fmt in ("png", "svg"):
            r = subprocess.run(["plantuml", "-t" + fmt, "-charset", "UTF-8", p],
                               capture_output=True, text=True)
            if r.returncode: print(f"  ✗ {n}.{fmt}: {r.stderr.strip()[:300]}")
        print(f"  ✓ {n}")
print(f"catalogo: {len(casos)} casos · {len(subs)} subsistemas · {len(ACTOR)} actores")
