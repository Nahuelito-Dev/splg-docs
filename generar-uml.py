#!/usr/bin/env python3
"""Genera los diagramas UML de nivel sistema a partir de Casos-de-Uso.md y renderiza los UML_*.puml.

    python3 generar-uml.py

Produce, en diagramas/uml/, el .puml y sus .png/.svg de:

  CU_Sistema_Actores               los cinco actores y el canal por el que operan
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
         "09": "Plataforma de despliegue"}
# el campo Actor/es esta escrito de varias formas ("ACT-03 Administrador",
# "Administrador (ACT-03)", "Sistema (ACT-04)", o el nombre solo)
POR_NOMBRE = {"cliente": "01", "chofer": "02", "administrador": "03",
              "sistema automático": "04", "sistema": "04",
              "administrador general": "05",
              "plataforma de despliegue": "09"}

casos = {}
for m in re.finditer(r'\*\*Código:\*\*\s*(CU-\d+)\s*\|\s*\*\*Caso de Uso:\*\*\s*(.+?)\s*\n(.*?)(?=\*\*Código:\*\*|\Z)', blk, re.S):
    cod, nom, resto = m.group(1), m.group(2).strip(), m.group(3)
    def campo(n):
        mm = re.search(rf'\*\*{n}:\*\*\s*(.*?)(?=\n\s*\*\*|\n\s*---|\Z)', resto, re.S)
        return re.sub(r'\s+', ' ', mm.group(1)).strip() if mm else ""
    crudo = campo("Actor/es")
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
INCLUYE = {
  # Toda alta de usuario crea la identidad por el mismo camino (CU-082).
  "SS-01": [("CU-002","CU-082"), ("CU-003","CU-082"),
            ("CU-050","CU-083"), ("CU-085","CU-083"),
            # ABM de usuarios y de perfil: cada operación parte de su consulta
            ("CU-270","CU-083"), ("CU-251","CU-004")],
  "SS-02": [("CU-147","CU-121"), ("CU-144","CU-146"), ("CU-170","CU-006"),
            ("CU-008","CU-006"), ("CU-009","CU-006"), ("CU-010","CU-006"),
            ("CU-118","CU-117"), ("CU-119","CU-117"), ("CU-120","CU-117"),
            ("CU-123","CU-125"), ("CU-124","CU-125"), ("CU-126","CU-125"),
            ("CU-127","CU-046"), ("CU-127","CU-006"), ("CU-128","CU-006")],
  "SS-05": [("CU-025","CU-024")],
  "SS-07": [("CU-136","CU-113"), ("CU-137","CU-113"), ("CU-140","CU-113"),
            ("CU-138","CU-110"), ("CU-105","CU-139"), ("CU-142","CU-139"),
            ("CU-096","CU-110"), ("CU-097","CU-110"), ("CU-109","CU-110"),
            ("CU-032","CU-110"), ("CU-033","CU-110"), ("CU-034","CU-110"),
            ("CU-267","CU-110"), ("CU-271","CU-110"),
            ("CU-111","CU-113"), ("CU-112","CU-113"), ("CU-105","CU-051"),
            ("CU-155","CU-159"), ("CU-157","CU-156"), ("CU-157","CU-160"),
            ("CU-158","CU-156"),
            # flota ampliada (I-12): cada alta o consulta parte de la ficha del vehículo
            ("CU-195","CU-113"), ("CU-196","CU-113"), ("CU-197","CU-113"), ("CU-198","CU-113"),
            ("CU-201","CU-113"), ("CU-203","CU-113")],
  "SS-08": [("CU-037","CU-041"), ("CU-038","CU-041"),
            ("CU-039","CU-041"), ("CU-040","CU-041"),
            ("CU-210","CU-208"), ("CU-212","CU-208"), ("CU-213","CU-208"),
            ("CU-212","CU-250"), ("CU-213","CU-250"), ("CU-218","CU-250"), ("CU-220","CU-250"),
            ("CU-222","CU-250"),
            # depósitos: modificar o dar de baja parte del listado; reactivar parte de los productos inactivos
            ("CU-259","CU-207"), ("CU-260","CU-207"), ("CU-268","CU-269")],
  "SS-09": [("CU-044","CU-045"), ("CU-043","CU-154"), ("CU-103","CU-154")],
  "SS-10": [("CU-054","CU-053"), ("CU-055","CU-053")],
  "SS-11": [("CU-059","CU-057")],
  "SS-12": [("CU-063","CU-061")],
  "SS-13": [("CU-135","CU-133"), ("CU-068","CU-135"), ("CU-134","CU-133"),
            ("CU-108","CU-071")],
  "SS-16": [("CU-094","CU-129"), ("CU-095","CU-129"),
            ("CU-131","CU-129"), ("CU-129","CU-130"),
            # roles: modificar o eliminar un rol parte del listado
            ("CU-253","CU-089"), ("CU-254","CU-089")],
  "SS-03": [("CU-149","CU-015")],
  "SS-19": [("CU-178","CU-179"), ("CU-181","CU-179"), ("CU-182","CU-179"), ("CU-183","CU-179"),
            ("CU-184","CU-179"), ("CU-185","CU-179"), ("CU-186","CU-179"), ("CU-191","CU-179"),
            ("CU-193","CU-179"), ("CU-187","CU-179"), ("CU-188","CU-187"),
            # puestos de trabajo: modificar o eliminar un puesto parte del listado
            ("CU-256","CU-176"), ("CU-257","CU-176")],
  "SS-21": [("CU-227","CU-228"), ("CU-233","CU-228"), ("CU-237","CU-228"), ("CU-243","CU-228")],
  # proveedores: modificar o dar de baja parte del listado
  "SS-20": [("CU-262","CU-214"), ("CU-263","CU-214")],
}

# Casos de uso factorizados: comportamiento comun que otros casos reutilizan
# (<<include>>) o que se agrega solo si se cumple una condicion (<<extend>>).
# No llevan codigo CU-XXX porque no son algo que el actor pida por separado:
# son parte de otro caso. Se dibujan igual porque la tabla 7.7 del Doc 1 los
# declara y la catedra pide ver la relacion en el diagrama.
FACTORIZADO = {
  "F-STOCK": "Reservar Stock",
  "F-AVISO": "Notificar Cliente",
  "F-PROMO": "Aplicar Promoción",
  "F-RECAR": "Aplicar Recargo por Pago en Línea",
  "F-TERM":  "Filtrar por Término",
  "F-FILTRO": "Filtrar Pedidos",
}

# Inclusiones entre subsistemas distintos: el caso incluido vive en otro
# subsistema y se dibuja fuera del limite del que lo incluye, con su codigo.
INCLUYE_EXTERNO = [("CU-031","CU-082"), ("CU-086","CU-082"), ("CU-087","CU-082"),
                   ("CU-174","CU-159"), ("CU-175","CU-160"),
                   ("CU-003","CU-177"), ("CU-012","CU-246"), ("CU-013","CU-246"), ("CU-015","CU-246"),
                   ("CU-217","CU-250"), ("CU-012","CU-248"), ("CU-013","CU-248"), ("CU-015","CU-248"),
                   ("CU-236","CU-005")]

# base -> incluido factorizado
INCLUYE_FACTOR = {
  "SS-02": [("CU-005","F-STOCK")],
  "SS-03": [("CU-015","F-AVISO")],
  "SS-04": [("CU-018","F-AVISO"), ("CU-020","F-AVISO")],
}

# extension -> base, con su punto de extension. La flecha de <<extend>> va
# SIEMPRE desde el caso opcional hacia el caso base, al reves que <<include>>.
EXTIENDE = {
  "SS-02": [("F-PROMO","CU-005","la cantidad de un ítem alcanza el umbral de promoción por volumen"),
            ("F-RECAR","CU-005","el medio de pago elegido es MercadoPago o Transferencia"),
            ("F-FILTRO","CU-011","se indica status, from/to o term sobre el listado")],
  "SS-03": [("CU-014","CU-013","no hay choferes disponibles en el radio")],
  "SS-04": [("CU-019","CU-018","el chofer se encuentra cerca del destino")],
  "SS-05": [("CU-174","CU-023","el cliente adjunta evidencia fotográfica")],
  "SS-14": [("CU-168","CU-008","el pedido cancelado tiene un pago aprobado por una pasarela"),
            ("CU-168","CU-010","el pedido cancelado tiene un pago aprobado por una pasarela"),
            ("CU-168","CU-149","el pedido express pasa a reparto común y ya estaba pagado en linea")],
  "SS-07": [("F-TERM","CU-035","se indica el parámetro term sobre el listado")],
  "SS-08": [("F-TERM","CU-041","se indica el parámetro term sobre el listado")],
  "SS-16": [("F-TERM","CU-092","se indica el parámetro term sobre el listado")],
}

# ---------- actores secundarios y generalizacion ----------
# Los tres actores externos no estan en el campo Actor/es de los casos: ese campo
# nombra al actor principal, el que inicia el caso. Estos son secundarios: el
# sistema los invoca. Cada lista sale de los adaptadores del backend:
#   ACT-06  payments/infrastructure/mercadopago.adapter.ts  (checkout y webhook)
#   ACT-07  firebase/infrastructure/firebase-auth.adapter.ts (identidad) y
#           fcm.adapter.ts (push)
#   ACT-08  email/infrastructure/resend-email.adapter.ts
ACTOR_EXT = {"06": "MercadoPago", "07": "Firebase", "08": "Servicio de correo"}
SECUNDARIO = {
  "06": ["CU-005", "CU-048", "CU-072", "CU-147"],
  "07": ["CU-001", "CU-004", "CU-005", "CU-013", "CU-014", "CU-015", "CU-016", "CU-019",
         "CU-018", "CU-020", "CU-021", "CU-047", "CU-072", "CU-079", "CU-082", "CU-085",
         "CU-091", "CU-100", "CU-101", "CU-147"],
  "08": ["CU-002", "CU-047", "CU-102", "CU-142", "CU-188", "CU-211", "CU-224"],
}
# El Administrador General hace todo lo que hace el Administrador y ademas lo que
# es exclusivo suyo: ACT-05 especializa a ACT-03.
GENERALIZA = ("05", "03")
ESP, GEN = GENERALIZA

def directos(cu):
    """Los actores principales que se dibujan contra el caso. Como ACT-05
    especializa a ACT-03, si el caso es de los dos la asociacion de ACT-05 sobra:
    la hereda."""
    a = list(casos[cu]["actores"])
    if ESP in a and GEN in a: a.remove(ESP)
    return a


CABECERA = """skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam defaultFontName Helvetica
skinparam defaultFontSize 13
skinparam dpi 150
skinparam ArrowColor #2C4257
skinparam ArrowThickness 1.1
skinparam actor {
  BorderColor #2C4257
  BackgroundColor #E8EDF2
  FontSize 13
  FontStyle bold
}
skinparam usecase {
  BorderColor #2C4257
  BackgroundColor #FFFFFF
  FontSize 12
}
skinparam rectangle {
  BorderColor #6B7683
  FontSize 14
  FontStyle bold
}
"""

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
  "05": ["CU-052", "CU-087"],
  "04": ["CU-014", "CU-075"],
}
EXT_REPRESENTATIVO = {"06": "CU-048", "07": "CU-001", "08": "CU-047"}
PRIMARIO_EXT = {"09": "CU-104"}
PRIMARIO_EXT_ACT = set(PRIMARIO_EXT)
act = ["@startuml", "title Actores del Sistema — SPLG", "left to right direction", CABECERA]
for k in ["01", "02", "03", "05", "04"]:
    act.append(f'actor "{ACTOR[k]}\\n(ACT-{k})" as A{k}')
for k in sorted(ACTOR_EXT):
    act.append(f'actor "{ACTOR_EXT[k]}\\n(ACT-{k})" as A{k} <<sistema externo>>')
act.append(f'actor "{ACTOR["09"]}\\n(ACT-09)" as A09 <<sistema externo>>')
act += ["", f'rectangle "{ "Sistema de Pedidos y Logística de Garrafas de Gas (SPLG)" }" ' + "{"]
usados = sorted({c for v in REPRESENTATIVOS.values() for c in v} | set(EXT_REPRESENTATIVO.values()) | set(PRIMARIO_EXT.values()))
for c in usados:
    act.append(f'  usecase "{c}\\n{parte(casos[c]["nombre"], 28)}" as {eid(c)} #back:FFFFFF;line:2C4257')
act += ["}", ""]
for k, lista in REPRESENTATIVOS.items():
    for c in lista:
        act.append(f'A{k} -[{COLOR_ACT[k]}]- {eid(c)}')
for k, c in EXT_REPRESENTATIVO.items():
    act.append(f'{eid(c)} -[#6B7683]- A{k}')
for k, c in PRIMARIO_EXT.items():
    act.append(f'A{k} -[{COLOR_ACT[k]}]- {eid(c)}')
act += ["", f"A{ESP} -right-|> A{GEN}", "", "@enduml"]
escribir("CU_Sistema_Actores", "\n".join(act))

# ---------- 2. contexto ----------
# Un subsistema NO es un caso de uso: la elipse esta reservada para el caso de
# uso. Un subsistema se dibuja como paquete. Y un diagrama de contexto muestra
# ademas con que sistemas externos habla el nuestro, que es lo que faltaba.
cnt = collections.Counter(v["ss"] for v in casos.values())
ctx = ["@startuml", "title Diagrama de Contexto del Sistema — SPLG",
       CABECERA,
       "skinparam nodesep 14", "skinparam ranksep 90",
       "skinparam rectangle {", "  BorderColor #2C4257", "  FontSize 12", "}", ""]
for k in ["01", "02", "03", "05", "04"]:
    ctx.append(f'actor "{ACTOR[k]}\\n(ACT-{k})" as A{k}')
for k in sorted(ACTOR_EXT):
    ctx.append(f'actor "{ACTOR_EXT[k]}\\n(ACT-{k})" as A{k} <<sistema externo>>')
ctx.append(f'actor "{ACTOR["09"]}\\n(ACT-09)" as A09 <<sistema externo>>')
lineas = "\\n".join(f'{s_}  {SS[s_]}  ({cnt[s_]})' for s_ in subs)
ctx += ["", f'rectangle "**Sistema de Pedidos y Logística de Garrafas de Gas (SPLG)**\\n\\n{lineas}\\n\\n(entre paréntesis, los casos de uso de cada subsistema)" as LIMITE #back:F4F7FA;line:2C4257', ""]
# En un diagrama de contexto el sistema es una sola caja: lo que se dibuja es con
# quien habla y para que. El detalle por subsistema esta en el mapa y en los
# diagramas de cada subsistema.
ROL = {"01": "pide, sigue y reclama sus pedidos", "02": "recibe ofertas y entrega",
       "03": "gestiona su distribuidora", "05": "gestiona todas las distribuidoras",
       "04": "ejecuta los procesos programados"}
for k in ["01", "02", "03", "05", "04"]:
    ctx.append(f'A{k} -[{COLOR_ACT[k]}]down- LIMITE : {ROL[k]}')
ctx += ["",
        f'LIMITE -[#6B7683]down- A06 : cobra y recibe el aviso de pago',
        f'LIMITE -[#6B7683]down- A07 : identidad y avisos push',
        f'LIMITE -[#6B7683]down- A08 : correos de bienvenida, recuperación y vencimientos',
        f'LIMITE -[{COLOR_ACT["09"]}]down- A09 : sondea la salud del sistema',
        "", f"A{ESP} -down-|> A{GEN}", "", "@enduml"]
escribir("CU_Sistema_Diagrama-De-Contexto", "\n".join(ctx))

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

# Graphviz no resuelve bien un diagrama de este tamano con los actores fuera del
# limite; el completo y el mapa se componen en uml_lamina.py y salen como SVG.
import uml_lamina
inc, ext = relaciones()
# Los casos factorizados no son casos de uso del catalogo (no llevan codigo): se
# dibujan en los diagramas de cada subsistema, que declaran sus relaciones, y no en
# la lamina completa, que muestra solo los casos numerados.
inc = [(a, b) for a, b in inc if not (a.startswith("F-") or b.startswith("F-"))]
ext = [(a, b, p) for a, b, p in ext if not (a.startswith("F-") or b.startswith("F-"))]
LAMINAS = {}
LAMINAS["CU_Sistema_Diagrama-Completo"] = uml_lamina.completo(
    casos, subs, SS, TINTE, BORDE, COLOR_ACT, NOMBRE_ACT, IZQ, DER, directos,
    SECUNDARIO, {}, inc, ext, ESP, GEN, LIMITE_TXT, None)
# El completo en una sola lámina tiene 271 casos y entero no se lee: se parte en seis
# láminas con la misma notación (límite del sistema, subsistemas como paquetes, actores
# afuera, «include»/«extend»). Juntas son el diagrama completo. Si un caso incluye o
# extiende a uno de otra lámina, ese otro se dibuja en un paquete gris de referencia
# que dice en qué lámina está, para que cada lámina se entienda sola.
PARTES_COMPLETO = [
    ("Usuarios y pedidos", ["SS-01", "SS-02"]),
    ("Despacho, entrega y posventa", ["SS-03", "SS-04", "SS-05", "SS-09", "SS-12", "SS-14", "SS-15"]),
    ("Choferes y flota", ["SS-07"]),
    ("Productos, envases y compras", ["SS-08", "SS-13", "SS-20"]),
    ("Personal y caja", ["SS-19", "SS-21"]),
    ("Administración y plataforma", ["SS-06", "SS-10", "SS-11", "SS-16", "SS-17", "SS-18"]),
]
_en_parte = {s: k for k, (_, ss_) in enumerate(PARTES_COMPLETO, 1) for s in ss_}
assert set(_en_parte) == set(subs), f"subsistemas sin lámina: {set(subs) - set(_en_parte)}"
REF = "REF"
LAMINAS_COMPLETO = []
for _k, (_tit, _ss) in enumerate(PARTES_COMPLETO, 1):
    _propios = {c for c in casos if casos[c]["ss"] in _ss}
    _ajenos = set()
    for a, b in inc:
        if (a in _propios) != (b in _propios): _ajenos.add(b if a in _propios else a)
    for a, b, _p in ext:
        if (a in _propios) != (b in _propios): _ajenos.add(b if a in _propios else a)
    _casos = {c: casos[c] for c in _propios}
    for c in _ajenos:
        _casos[c] = {**casos[c], "ss": REF,
                     "nombre": f'{casos[c]["nombre"]} (lámina {_en_parte[casos[c]["ss"]]})'}
    _subs = [s for s in subs if s in _ss] + ([REF] if _ajenos else [])
    _SS = {**{s: SS[s] for s in _ss}, REF: "De otras láminas"}
    _tinte = [TINTE[subs.index(s) % len(TINTE)] for s in _subs if s != REF] + ["#EEF0F2"]
    _borde = [BORDE[subs.index(s) % len(BORDE)] for s in _subs if s != REF] + ["#8A97A3"]
    _dir = (lambda prop: (lambda c: directos(c) if c in prop else []))(_propios)
    _sec = {k: [c for c in v if c in _propios] for k, v in SECUNDARIO.items()}
    _sec = {k: v for k, v in _sec.items() if v}
    _act = {k for c in _propios for k in directos(c)} | set(_sec)
    if ESP in _act or GEN in _act: _act |= {ESP, GEN}
    _inc = [(a, b) for a, b in inc if a in _casos and b in _casos and (a in _propios or b in _propios)]
    _ext = [(a, b, p) for a, b, p in ext if a in _casos and b in _casos and (a in _propios or b in _propios)]
    _n = f"CU_Sistema_Completo-Lamina-{_k}"
    LAMINAS[_n] = uml_lamina.completo(
        _casos, _subs, _SS, _tinte, _borde, COLOR_ACT, NOMBRE_ACT,
        [k for k in IZQ if k in _act], [k for k in DER if k in _act], _dir,
        _sec, {}, _inc, _ext, ESP, GEN, LIMITE_TXT, None,
        titulo=f"Diagrama Completo de Casos de Uso — lámina {_k} de {len(PARTES_COMPLETO)}: "
               f"{_tit} ({len(_propios)} casos de uso)",
        columnas=min(2, len(_subs)), ref_ss=REF, compacto=True)
    LAMINAS_COMPLETO.append(_n)

LAMINAS["CU_Sistema_Mapa"] = uml_lamina.mapa(
    casos, subs, SS, TINTE, BORDE, COLOR_ACT, NOMBRE_ACT, IZQ, DER, directos,
    SECUNDARIO, ESP, GEN, LIMITE_TXT)
for _n, _svg in LAMINAS.items():
    open(UML + _n + ".svg", "w", encoding="utf-8").write(_svg)
    # el .puml del completo de antes ya no es la fuente de nada
    if os.path.exists(UML + _n + ".puml"): os.remove(UML + _n + ".puml")


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
        "skinparam package {", "  BorderColor #2C4257", "  FontSize 12", "}",
        "", "left to right direction", ""]
def paquete(s, sangria):
    i = subs.index(s); n = cnt[s]
    return (f'{sangria}package "{s} {SS[s]}\\n({n} caso{"s" if n != 1 else ""} de uso)" as M{s.replace("-","")} '
            f'<<subsystem>> #back:{TINTE[i % len(TINTE)][1:]};line:{BORDE[i % len(BORDE)][1:]} ' + "{")
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
# Estaban escritos a mano y se quedaron cortos: SS-02 mostraba once casos cuando ya
# eran veinticuatro. Se generan del catalogo para que ninguno quede incompleto.
unidades = []
for i, s in enumerate(subs):
    todos = sorted(c for c in casos if casos[c]["ss"] == s)
    if s in PARTES:
        asignados = set().union(*[m for _, _, m in PARTES[s] if m])
        for suf, tit, m in PARTES[s]:
            miembros = set(m) if m else {c for c in todos if c not in asignados}
            miembros |= {b for a, b in INCLUYE.get(s, []) if a in miembros and b in casos and casos[b]["ss"] == s}
            unidades.append((i, s, f"CU_{s}_{suf}", tit, sorted(miembros)))
    else:
        g = glob.glob(UML + f"CU_{s}_*.puml")
        if g: unidades.append((i, s, os.path.basename(g[0])[:-5], None, todos))
for i, s, nombre, tit, cs in unidades:
    quienes = {k for c in cs for k in casos[c]["actores"]}
    # el Administrador General especializa al Administrador: si participa uno de los
    # dos, se dibujan ambos y la generalizacion, para que se lea por que ACT-05 no
    # repite las asociaciones que hereda
    if ESP in quienes or GEN in quienes:
        quienes |= {ESP, GEN}
    quienes = sorted(quienes)
    borde = BORDE[i % len(BORDE)][1:]
    d = ["@startuml", f"title {s} — {SS[s]}{': ' + tit if tit else ''} ({len(cs)} casos de uso)",
         "left to right direction", CABECERA, "skinparam nodesep 18", "skinparam ranksep 70",
         "skinparam usecase {", "  BorderColor<<planificado>> #9C4436",
         "  BackgroundColor<<planificado>> #F6E4E1",
         "  BorderColor<<factorizado>> #6B7683",
         "  BackgroundColor<<factorizado>> #F2F4F6", "}", ""]
    for k in quienes:
        est_ac = " <<sistema externo>>" if k in PRIMARIO_EXT_ACT else ""
        d.append(f'actor "{ACTOR[k]}\\n(ACT-{k})" as A{k}{est_ac}')
    # actores secundarios: el sistema los invoca durante el caso (los mismos del
    # diagrama de actores y del completo)
    sec = {k: [c for c in SECUNDARIO[k] if c in cs] for k in sorted(SECUNDARIO)}
    sec = {k: v for k, v in sec.items() if v}
    for k in sec:
        d.append(f'actor "{ACTOR_EXT[k]}\\n(ACT-{k})" as A{k} <<sistema externo>>')
    d.append("")
    d.append(f'rectangle "{s} {SS[s]}{chr(92) + "n" + tit if tit else ""}" ' + "{")
    for c in cs:
        est = " <<planificado>>" if casos[c].get("planificado") else ""
        # el estereotipo va antes del color; al reves plantuml no lo toma
        d.append(f'  usecase "{c}\\n{parte(casos[c]["nombre"], 30)}" as {eid(c)}{est}'
                 f' #back:FFFFFF;line:{borde}')
    # los factorizados que participen de alguna relacion de este subsistema
    ext_s = [(a, b, p_) for a, b, p_ in EXTIENDE.get(s, []) if b in cs or b not in casos or casos[b]["ss"] != s]
    inc_f = [(a, b) for a, b in INCLUYE_FACTOR.get(s, []) if b in cs or b not in casos]
    usados = sorted({x for a, b in inc_f for x in (a, b) if x.startswith("F-")}
                  | {a for a, b, _ in ext_s if a.startswith("F-")})
    for fc in usados:
        d.append(f'  usecase "{parte(FACTORIZADO[fc], 30)}" as {eid(fc)} <<factorizado>>'
                 f' #back:FFFFFF;line:{borde}')
    d += ["}", ""]
    # casos de otro subsistema que alguno de este incluye: fuera del rectangulo
    externos = [(a, b) for a, b in INCLUYE_EXTERNO
                if a in cs and b in casos and casos[b]["ss"] != s]
    # la base de un <<extend>> que vive en otro subsistema se dibuja igual, fuera del limite
    bases_ext = [b for a, b, _ in ext_s if b in casos and casos[b]["ss"] != s]
    # los casos de otro subsistema que incluyen a uno de éste: se muestran como referencia externa,
    # con su flecha «include», para que el caso incluido no quede suelto
    entrantes = [(a, b) for a, b in INCLUYE_EXTERNO
                 if a in casos and b in cs and casos[a]["ss"] != s]
    ajenos = sorted({b for _, b in externos} | set(bases_ext) | {a for a, _ in entrantes})
    if ajenos:
        # los casos de otros subsistemas van juntos en su propio limite, no sueltos
        d.append('rectangle "Casos de uso de otros subsistemas\\n(sólo como referencia)" as OTROS '
                 '#back:FFFFFF;line:6B7683;line.dashed {')
    for b in ajenos:
        est = " <<planificado>>" if casos[b].get("planificado") else ""
        d.append(f'  usecase "{b}\\n{parte(casos[b]["nombre"], 30)}\\n({casos[b]["ss"]})" as {eid(b)}{est}'
                 f' #back:FFFFFF;line:6B7683')
    if ajenos: d += ["}", ""]
    # La asociacion actor-caso de uso es una asociacion, no una dependencia:
    # en UML va sin punta de flecha. La flecha significaria navegabilidad, que
    # es una decision de diseno y no corresponde a un diagrama de requisitos.
    for k in quienes:
        for c in cs:
            if k in directos(c):
                d.append(f'A{k} -[{COLOR_ACT[k]}]- {eid(c)}')
    for k, v in sec.items():
        for c in v:
            d.append(f'{eid(c)} -[#6B7683]- A{k}')
    if ESP in quienes:
        # la punta del triangulo va sobre la cabeza del Administrador, no sobre su rotulo
        d.append(f'A{ESP} -right-|> A{GEN}')
    rel = [(a, b) for a, b in INCLUYE.get(s, []) if a in cs and b in cs]
    rel += inc_f
    rel += externos + entrantes
    if rel:
        d.append("")
        d.append("' escribir sobre algo exige leerlo antes: la busqueda entra por <<include>>")
        for a, b in rel:
            d.append(f'{eid(a)} ..> {eid(b)} : <<include>>')
        # Un caso incluido que ademas tiene actor propio recibe dos lineas por el mismo
        # lado: la asociacion (solida) y la flecha de <<include>>, y la primera se lee
        # como si terminara en la punta. Se lo ubica antes que sus bases: la flecha le
        # llega por la derecha y la asociacion por la izquierda.
        for b in sorted({b for _, b in rel}):
            bases = sorted({a for a, bb in rel if bb == b})
            if (s in SEPARAR_ACTOR_DE_INCLUIDO and b in casos and casos[b]["ss"] == s and any(k in quienes for k in directos(b))
                    and len(bases) <= BASES_MAX_POR_SS.get(s, BASES_MAX_SEPARAR)):
                for a in bases:
                    d.append(f'{eid(b)} -[hidden]-> {eid(a)}')
    ext = ext_s
    if ext:
        d.append("")
        d.append("' <<extend>>: comportamiento opcional. La flecha va de la extension al caso base.")
        for a, b, punto in ext:
            # el punto de extension va en el rotulo de la propia relacion
            d.append(f'{eid(a)} ..> {eid(b)} : <<extend>>\\n(punto de extensión:\\n{parte(punto, 34)})')
    d += ["", "@enduml"]
    escribir(nombre, "\n".join(d))
    SUBSISTEMAS.append(nombre)

# ---------- render ----------
objetivo = sys.argv[1:] or (["CU_Sistema_Actores", "CU_Sistema_Diagrama-De-Contexto"]
                            + list(LAMINAS) + SUBSISTEMAS)
for n in objetivo:
    if n in LAMINAS:
        # el SVG ya esta escrito; el PNG sale al doble de tamano para poder imprimirlo
        r = subprocess.run(["rsvg-convert", "-z", "1.5", "-o", UML + n + ".png", UML + n + ".svg"],
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
