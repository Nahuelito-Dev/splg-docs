#!/usr/bin/env python3
"""Genera los diagramas UML de nivel sistema a partir de Casos-de-Uso.md.

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
         "04": "Sistema Automático", "05": "Administrador General"}
# el campo Actor/es esta escrito de varias formas ("ACT-03 Administrador",
# "Administrador (ACT-03)", "Sistema (ACT-04)", o el nombre solo)
POR_NOMBRE = {"cliente": "01", "chofer": "02", "administrador": "03",
              "sistema automático": "04", "sistema": "04",
              "administrador general": "05"}

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

# estado de cada caso, del artefacto expandido: los que todavia no estan
# construidos se dibujan con otro color en el diagrama de su subsistema
a2 = next(i for i, x in enumerate(lin) if re.match(r'^## 5\. ', x))
b2 = next(i for i, x in enumerate(lin) if re.match(r'^## 6\. ', x))
blk2 = "\n".join(lin[a2:b2])
# El encabezado puede traer uno o dos marcadores antes del codigo
# ("Importante · automático CU-105"): con \S+ se salteaban esos casos y los
# cuatro modulos inteligentes salian dibujados como si estuvieran construidos.
for m in re.finditer(r'^####\s+.*?(CU-\d+)\s+—.*?\|\s*\*\*Estado\*\*\s*\|\s*([^|]+)\|', blk2, re.S | re.M):
    if m.group(1) in casos:
        casos[m.group(1)]["pendiente"] = not m.group(2).strip().lower().startswith("implementado")

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
  "SS-01": [("CU-002","CU-082"), ("CU-003","CU-082")],
  "SS-02": [("CU-005","CU-125"), ("CU-005","CU-121"), ("CU-005","CU-148"),
            ("CU-147","CU-121"), ("CU-147","CU-148"), ("CU-144","CU-146"),
            ("CU-008","CU-006"), ("CU-009","CU-006"), ("CU-010","CU-006"),
            ("CU-118","CU-117"), ("CU-119","CU-117"), ("CU-120","CU-117"),
            ("CU-123","CU-125"), ("CU-124","CU-125"), ("CU-126","CU-125"),
            ("CU-127","CU-046"), ("CU-127","CU-006"), ("CU-128","CU-006")],
  "SS-07": [("CU-136","CU-113"), ("CU-137","CU-113"), ("CU-140","CU-113"),
            ("CU-138","CU-109"), ("CU-105","CU-139"), ("CU-142","CU-139"),
            ("CU-096","CU-110"), ("CU-097","CU-110"), ("CU-109","CU-110"),
            ("CU-032","CU-110"), ("CU-033","CU-110"), ("CU-034","CU-110"),
            ("CU-111","CU-113"), ("CU-112","CU-113"), ("CU-105","CU-051")],
  "SS-16": [("CU-094","CU-129"), ("CU-095","CU-129"),
            ("CU-131","CU-129"), ("CU-129","CU-130")],
  "SS-13": [("CU-135","CU-133"), ("CU-068","CU-135"), ("CU-134","CU-133"),
            ("CU-108","CU-071")],
  "SS-03": [("CU-149","CU-015")],
  "SS-09": [("CU-044","CU-045")],
}

# Casos de uso factorizados: comportamiento comun que otros casos reutilizan
# (<<include>>) o que se agrega solo si se cumple una condicion (<<extend>>).
# No llevan codigo CU-XXX porque no son algo que el actor pida por separado:
# son parte de otro caso. Se dibujan igual porque la tabla 7.7 del Doc 1 los
# declara y la catedra pide ver la relacion en el diagrama.
FACTORIZADO = {
  "F-STOCK": "Reservar Stock",
  "F-AVISO": "Notificar Cliente",
  "F-PROMO": "Aplicar Promocion",
  "F-RECAR": "Recargo por Transferencia",
  "F-FOTO":  "Adjuntar Foto",
}

# Inclusiones entre subsistemas distintos: el caso incluido vive en otro
# subsistema y se dibuja fuera del limite del que lo incluye, con su codigo.
INCLUYE_EXTERNO = [("CU-031","CU-082"), ("CU-086","CU-082"), ("CU-087","CU-082")]

# base -> incluido factorizado
INCLUYE_FACTOR = {
  "SS-02": [("CU-005","F-STOCK")],
  "SS-03": [("CU-015","F-AVISO")],
  "SS-04": [("CU-018","F-AVISO"), ("CU-020","F-AVISO")],
}

# extension -> base, con su punto de extension. La flecha de <<extend>> va
# SIEMPRE desde el caso opcional hacia el caso base, al reves que <<include>>.
EXTIENDE = {
  "SS-02": [("F-PROMO","CU-005","la cantidad de un item alcanza el umbral de promocion por volumen"),
            ("F-RECAR","CU-005","el medio de pago elegido es Transferencia")],
  "SS-03": [("CU-014","CU-013","no hay choferes disponibles en el radio")],
  "SS-04": [("CU-019","CU-018","el chofer se encuentra cerca del destino")],
  "SS-05": [("F-FOTO","CU-023","el cliente adjunta evidencia fotografica")],
}

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

# ---------- 1. actores ----------
act = ["@startuml", "title Actores del Sistema — SPLG", "left to right direction", CABECERA]
for k in sorted(ACTOR):
    act.append(f'actor "{ACTOR[k]}\\n(ACT-{k})" as A{k}')
act += ["",
  'rectangle "Sistema de Pedidos y Logística de Garrafas de Gas (SPLG)" {',
  '  rectangle "App Cliente\\n(Flutter)" as APPC',
  '  rectangle "App Chofer\\n(Flutter)" as APPD',
  '  rectangle "Panel Web\\n(React / Vite)" as PANEL',
  '  rectangle "Procesos programados\\n(sin interfaz)" as PROC',
  '  rectangle "Backend\\n(NestJS + PostgreSQL/PostGIS)" as BACK',
  "}", ""]
canal = [("01", "APPC", ""), ("02", "APPD", ""),
         ("03", "PANEL", "alcance: su distribuidora"),
         ("05", "PANEL", "alcance: todas las distribuidoras"),
         ("04", "PROC", "sin intervención humana")]
for k, destino, etiqueta in canal:
    et = f" : {etiqueta}" if etiqueta else ""
    act.append(f'A{k} -[{COLOR_ACT[k]}]- {destino}{et}')
act += ["", "APPC --> BACK", "APPD --> BACK", "PANEL --> BACK", "PROC --> BACK",
        "", "@enduml"]
escribir("CU_Sistema_Actores", "\n".join(act))

# ---------- 2. contexto ----------
# Un subsistema NO es un caso de uso: la elipse esta reservada para el caso de
# uso. Un subsistema se dibuja como paquete. Y un diagrama de contexto muestra
# ademas con que sistemas externos habla el nuestro, que es lo que faltaba.
cnt = collections.Counter(v["ss"] for v in casos.values())
ctx = ["@startuml", "title Diagrama de Contexto del Sistema — SPLG",
       "left to right direction", CABECERA,
       "skinparam nodesep 14", "skinparam ranksep 45",
       "skinparam package {", "  BorderColor #2C4257", "  FontSize 12", "}", ""]
for k in sorted(ACTOR):
    ctx.append(f'actor "{ACTOR[k]}\\n(ACT-{k})" as A{k}')
ctx += ["", 'rectangle "Sistema de Pedidos y Logística de Garrafas de Gas (SPLG)" as LIMITE {']
for i, s in enumerate(subs):
    n = cnt[s]
    ctx.append(f'  package "{s}\\n{SS[s]}\\n({n} caso{"s" if n != 1 else ""} de uso)" as {s.replace("-","")} '
               f'<<subsystem>> #back:{TINTE[i % len(TINTE)][1:]};line:{BORDE[i % len(BORDE)][1:]}')
# Los 18 paquetes en una sola tira dan una lamina de 5400 px de ancho o de
# 4000 de alto, segun la direccion. La cadena invisible los reparte en columnas
# y deja el diagrama en una proporcion que entra en una hoja. Es el mismo
# recurso que usa el diagrama completo.
PORCOL = 6
ids = [s.replace("-", "") for s in subs]
for c in range(0, len(ids), PORCOL):
    col = ids[c:c + PORCOL]
    for a, b in zip(col, col[1:]):
        ctx.append(f'  {a} -[hidden]- {b}')
ctx += ["}", ""]
por_ss = collections.defaultdict(set)
for v in casos.values():
    for k in v["actores"]:
        por_ss[k].add(v["ss"])
for k in sorted(ACTOR):
    for s in sorted(por_ss[k]):
        ctx.append(f'A{k} -[{COLOR_ACT[k]}]- {s.replace("-","")}')
# Los servicios de terceros son parte del contexto: el sistema depende de ellos
# y estan fuera de su limite.
ctx += ["", 'actor "Firebase\\nidentidad y avisos" as XFB <<external>>',
        'actor "MercadoPago\\npasarela de cobro" as XMP <<external>>',
        'actor "Servicio de correo" as XML <<external>>', "",
        "LIMITE ..> XFB : autentica y notifica",
        "LIMITE ..> XMP : cobra y concilia",
        "LIMITE ..> XML : envía comprobantes"]
ctx += ["", "@enduml"]
escribir("CU_Sistema_Diagrama-De-Contexto", "\n".join(ctx))

# ---------- 3. completo ----------
def eid(c): return c.replace("-", "_") if c.startswith("F-") else "U" + c.replace("CU-", "")
def parte(txt, ancho=26):
    """Corta el nombre en lineas para que la elipse no salga apaisada."""
    out, l = [], ""
    for w in txt.split():
        if len(l) + len(w) + 1 > ancho and l: out.append(l); l = w
        else: l = (l + " " + w).strip()
    if l: out.append(l)
    return "\\n".join(out)

# Los actores se dibujan una vez por subsistema. UML admite que un mismo
# clasificador aparezca con mas de un simbolo en el diagrama, y con 115 casos es
# la diferencia entre un diagrama legible y una maraña: con un unico juego de
# actores a la izquierda las ~250 asociaciones cruzan el lienzo entero.
POR_COLUMNA = 4   # subsistemas por columna; 4 es lo que menos hueco deja

com = ["@startuml", f"title Diagrama Completo de Casos de Uso — SPLG ({len(casos)} casos de uso)",
       "left to right direction", CABECERA,
       "skinparam nodesep 14", "skinparam ranksep 60", ""]
com.append('rectangle "Sistema de Pedidos y Logística de Garrafas de Gas (SPLG)" {')
primeros, flechas = [], []
for i, s in enumerate(subs):
    cs = sorted(c for c in casos if casos[c]["ss"] == s)
    primeros.append(eid(cs[0]))
    quienes = sorted({k for c in cs for k in casos[c]["actores"]})
    tinte, borde = TINTE[i % len(TINTE)][1:], BORDE[i % len(BORDE)][1:]
    com.append(f'  rectangle "{s} — {SS[s]}" as R{s.replace("-","")} #back:{tinte};line:{borde} ' + "{")
    for k in quienes:
        com.append(f'    actor "{ACTOR[k]}\\n(ACT-{k})" as A{k}{s.replace("-","")}')
    for c in cs:
        com.append(f'    usecase "{c}\\n{parte(casos[c]["nombre"])}" as {eid(c)} #back:FFFFFF;line:{borde}')
        for k in casos[c]["actores"]:
            flechas.append(f'A{k}{s.replace("-","")} -[{COLOR_ACT[k]}]- {eid(c)}')
    com.append("  }")
com += ["}", ""] + flechas
com += ["", "' sin esta cadena invisible graphviz apila los 18 subsistemas en una sola tira"]
com += [f'{primeros[i-POR_COLUMNA]} -[hidden]-> {primeros[i]}' for i in range(POR_COLUMNA, len(primeros))]
com += ["", "legend right",
        "  Un color de linea por actor:",
        "  " + "  ".join(f"<color:{COLOR_ACT[k]}>■</color> {ACTOR[k]} (ACT-{k})" for k in sorted(ACTOR)),
        "  Cada actor se dibuja una vez por subsistema; son los mismos cinco actores.",
        "endlegend", "", "@enduml"]
escribir("CU_Sistema_Diagrama-Completo", "\n".join(com))


# ---------- 4. mapa de subsistemas ----------
# La catedra dijo que el de subsistemas se veia mal. Era un flowchart de cajas sueltas
# dentro de dos marcos: no mostraba ninguna relacion, y sin relaciones no es un diagrama
# sino una lista dibujada. Este dice quien depende de quien.
NEGOCIO = ["SS-01","SS-02","SS-03","SS-04","SS-05","SS-06","SS-07","SS-08","SS-09",
           "SS-11","SS-12","SS-13","SS-14","SS-15"]
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
  ("SS-16","SS-01","administra las cuentas"), ("SS-17","SS-01","avisa a los usuarios"),
  ("SS-18","SS-10","vigila la instancia"),
]
mapa = ["@startuml", f"title Subsistemas del Proyecto — SPLG ({len(subs)} subsistemas · {len(casos)} casos de uso)",
        CABECERA, "skinparam nodesep 25", "skinparam ranksep 55",
        "skinparam package {", "  BorderColor #2C4257", "  FontSize 12", "}",
        "", "left to right direction", "",
        'rectangle "SS-10 Multi-Distribuidora — restricción transversal:'
        '\\ntodo subsistema de negocio opera acotado a la distribuidora del usuario" as R10 '
        '#back:F3F1E4;line:7A7340 {']
for alias, grupo, titulo, borde in (("GNEG", NEGOCIO, "Subsistemas de negocio", "3C6E8F"),
                                    ("GSOP", [s for s in subs if s not in NEGOCIO and s != "SS-10"],
                                     "Subsistemas de soporte", "5A5896")):
    mapa.append(f'  package "{titulo}" as {alias} #back:FFFFFF;line:{borde} ' + "{")
    for s in grupo:
        i = subs.index(s)
        n = cnt[s]
        mapa.append(f'    package "**{s}**\\n{SS[s]}\\n({n} caso{"s" if n != 1 else ""})" as M{s.replace("-","")} '
                    f'<<subsystem>> #back:{TINTE[i % len(TINTE)][1:]};line:{BORDE[i % len(BORDE)][1:]}')
    mapa.append("  }")
mapa += ["}", ""]
def nodo(s):
    # SS-10 no es una caja mas: es el rectangulo que envuelve a todos
    return "R10" if s == "SS-10" else "M" + s.replace("-", "")
for a, b, que in DEPENDE:
    if a in SS and b in SS:
        mapa.append(f'{nodo(a)} ..> {nodo(b)} : {que}')
mapa += ["", "@enduml"]
escribir("CU_Sistema_Subsistemas", "\n".join(mapa))
SUBSISTEMAS.append("CU_Sistema_Subsistemas")


# ---------- 5. despliegue y entornos ----------
# No habia ningun diagrama que mostrara donde corre cada cosa ni como llega el codigo
# de la maquina de desarrollo a produccion. Sale de la configuracion real: los
# docker-compose de cada repo y los flujos de trabajo de GitHub Actions.
des = ["@startuml", "title Despliegue y Entornos — SPLG", CABECERA,
       "skinparam nodesep 20", "skinparam ranksep 60", "skinparam componentStyle rectangle", "",
 'node "Máquina de desarrollo" as DEV #back:E7F0F6;line:3C6E8F {',
 '  component "splg-app-backend\\n(NestJS)" as B',
 '  component "splg-app-admin\\n(React + Vite)" as P',
 '  component "splg-app-cliente\\nsplg-app-chofer\\n(Flutter)" as A',
 '  component "splg-lib\\n(contratos compartidos)" as L',
 '  database "splg-bd\\nPostGIS 14-3.4 · 5432" as BD',
 '  database "splg-redis\\nRedis · 6379" as RD',
 "}", "",
 'node "GitHub" as GH #back:F3F1E4;line:7A7340 {',
 '  component "6 repositorios splg-*\\nGitFlow: develop → release → main" as REPO',
 '  component "checks.yml\\nverificación en cada cambio" as CI',
 '  component "release.yml\\netiqueta y publica la versión" as REL',
 '  component "deploy.yml\\ndespliega al integrar en main" as DEP',
 "}", "",
 'node "Producción" as PROD #back:E9F4EA;line:3F7A50 {',
 '  component "Render\\nbackend + base de datos" as REN',
 '  component "Netlify\\npanel de administración" as NET',
 '  component "Netlify\\ndocumentación del sistema" as DOC',
 "}", "",
 'cloud "Servicios externos" as EXT #back:F7ECEF;line:8E5566 {',
 '  component "Firebase\\nidentidad y avisos al dispositivo" as FB',
 '  component "MercadoPago\\npasarela de cobro" as MP',
 '  component "Slack\\naviso de cada despliegue" as SL',
 "}", "",
 "B --> BD", "B --> RD", "P --> B", "A --> B", "L ..> B : tipos", "L ..> P : tipos",
 "", "DEV --> REPO : push a develop",
 "REPO --> CI : en cada cambio", "REPO --> REL : al integrar en main",
 "REPO --> DEP : al integrar en main",
 "DEP --> REN : dispara la construcción", "DEP --> NET : dispara la construcción",
 "DEP --> SL : avisa inicio, éxito o falla",
 "DOC <.. DEV : se publica a mano con publicar.sh",
 "", "B ..> FB", "B ..> MP", "A ..> FB",
 "", "legend right",
 "  Lo que corre en cada lugar y cómo llega el código de una máquina a la otra.",
 "  La documentación es la única pieza que todavía se publica a mano.",
 "endlegend", "", "@enduml"]
escribir("CU_Sistema_Despliegue", "\n".join(des))
SUBSISTEMAS.append("CU_Sistema_Despliegue")

# ---------- 6. un diagrama por subsistema ----------
# Estaban escritos a mano y se quedaron cortos: SS-02 mostraba once casos cuando ya
# eran veinticuatro. Se generan del catalogo para que ninguno quede incompleto.
for i, s in enumerate(subs):
    g = glob.glob(UML + f"CU_{s}_*.puml")
    if not g: continue
    cs = sorted(c for c in casos if casos[c]["ss"] == s)
    quienes = sorted({k for c in cs for k in casos[c]["actores"]})
    borde = BORDE[i % len(BORDE)][1:]
    d = ["@startuml", f"title {s} — {SS[s]} ({len(cs)} casos de uso)",
         "left to right direction", CABECERA, "skinparam nodesep 18", "skinparam ranksep 70",
         "skinparam usecase {", "  BorderColor<<pendiente>> #9C4436",
         "  BackgroundColor<<pendiente>> #F6E4E1",
         "  BorderColor<<factorizado>> #6B7683",
         "  BackgroundColor<<factorizado>> #F2F4F6", "}", ""]
    for k in quienes:
        d.append(f'actor "{ACTOR[k]}\\n(ACT-{k})" as A{k}')
    d.append("")
    d.append(f'rectangle "{s} {SS[s]}" ' + "{")
    for c in cs:
        est = " <<pendiente>>" if casos[c].get("pendiente") else ""
        # el estereotipo va antes del color; al reves plantuml no lo toma
        d.append(f'  usecase "{c}\\n{parte(casos[c]["nombre"], 30)}" as {eid(c)}{est}'
                 f' #back:FFFFFF;line:{borde}')
    # los factorizados que participen de alguna relacion de este subsistema
    usados = sorted({x for a, b in INCLUYE_FACTOR.get(s, []) for x in (a, b)
                     if x.startswith("F-")}
                  | {a for a, b, _ in EXTIENDE.get(s, []) if a.startswith("F-")})
    for fc in usados:
        d.append(f'  usecase "{parte(FACTORIZADO[fc], 30)}" as {eid(fc)} <<factorizado>>'
                 f' #back:FFFFFF;line:{borde}')
    d += ["}", ""]
    # casos de otro subsistema que alguno de este incluye: fuera del rectangulo
    externos = [(a, b) for a, b in INCLUYE_EXTERNO
                if a in casos and b in casos and casos[a]["ss"] == s and casos[b]["ss"] != s]
    for b in sorted({b for _, b in externos}):
        d.append(f'usecase "{b}\\n{parte(casos[b]["nombre"], 30)}\\n({casos[b]["ss"]})" as {eid(b)}'
                 f' #back:FFFFFF;line:6B7683')
    if externos: d.append("")
    # La asociacion actor-caso de uso es una asociacion, no una dependencia:
    # en UML va sin punta de flecha. La flecha significaria navegabilidad, que
    # es una decision de diseno y no corresponde a un diagrama de requisitos.
    for k in quienes:
        for c in cs:
            if k in casos[c]["actores"]:
                d.append(f'A{k} -[{COLOR_ACT[k]}]- {eid(c)}')
    rel = [(a, b) for a, b in INCLUYE.get(s, [])
           if a in casos and b in casos and casos[a]["ss"] == s and casos[b]["ss"] == s]
    rel += [(a, b) for a, b in INCLUYE_FACTOR.get(s, [])]
    rel += externos
    if rel:
        d.append("")
        d.append("' escribir sobre algo exige leerlo antes: la busqueda entra por <<include>>")
        for a, b in rel:
            d.append(f'{eid(a)} ..> {eid(b)} : <<include>>')
    ext = EXTIENDE.get(s, [])
    if ext:
        d.append("")
        d.append("' <<extend>>: comportamiento opcional. La flecha va de la extension al caso base.")
        for a, b, punto in ext:
            d.append(f'{eid(a)} ..> {eid(b)} : <<extend>>')
            d.append("note on link")
            d.append(f'  Punto de extension: {punto}')
            d.append("end note")
    d += ["", "@enduml"]
    nombre = os.path.basename(g[0])[:-5]
    escribir(nombre, "\n".join(d))
    SUBSISTEMAS.append(nombre)

# ---------- render ----------
objetivo = sys.argv[1:] or (["CU_Sistema_Actores", "CU_Sistema_Diagrama-De-Contexto",
                             "CU_Sistema_Diagrama-Completo"] + SUBSISTEMAS)
for n in objetivo:
    for fmt in ("png", "svg"):
        # sin el limite, plantuml recorta el diagrama completo a 4096 px de alto
        entorno = dict(os.environ, PLANTUML_LIMIT_SIZE="32768")
        r = subprocess.run(["plantuml", "-t" + fmt, "-charset", "UTF-8", UML + n + ".puml"],
                           capture_output=True, text=True, env=entorno)
        if r.returncode:
            print(f"  ✗ {n}.{fmt}: {r.stderr.strip()[:300]}"); continue
    p = UML + n + ".png"
    if os.path.exists(p):
        print(f"  ✓ {n}  ({os.path.getsize(p)//1024} KB)")
print(f"catalogo: {len(casos)} casos · {len(subs)} subsistemas · {len(ACTOR)} actores")
