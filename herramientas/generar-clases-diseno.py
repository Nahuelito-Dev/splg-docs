#!/usr/bin/env python3
"""Genera el diagrama de clases de diseño del Documento 3 (sección 3), derivado de los DSD.

    python3 herramientas/generar-clases-diseno.py

Es el procedimiento de Larman: el diagrama de clases de diseño sale de los diagramas de
interacción. Lee los DSD en estilo Larman (`diagramas/DSD_*.mmd`) y el modelo conceptual
(`modelo_conceptual.py`); la lógica de derivación está en `dc_larman.py`:

  - cada mensaje que recibe un objeto es una operación de su clase, con los argumentos y el
    retorno que muestra el DSD;
  - los atributos de las clases de dominio salen del modelo conceptual, con el tipo del código;
  - la asociación del modelo conceptual entre dos objetos que se mandan mensajes queda
    navegable en el sentido del mensaje; sin asociación, el mensaje es una dependencia;
  - los servicios, puertos y colecciones que colaboran quedan asociados con navegabilidad
    (se inyectan como atributo) o en dependencia (el código real no los inyecta);
  - los controladores, las fabricaciones puras y los puertos llevan su estereotipo.

Sale, todo en PlantUML como el modelo conceptual (Mermaid no dibuja la notación completa):

  diagramas/clases-diseno/DC_General.*                  las clases de dominio, sin miembros
  diagramas/clases-diseno/DC_<área>.*                   dominio con atributos y operaciones, por área
  diagramas/clases-diseno/DC_Mod_<vista>.*              una vista por módulo o grupo de módulos
  diagramas/clases-diseno/DC_Paquetes.*                 dependencias entre módulos
  catedra/material-de-trabajo/indice-clases-diseno.md           cifras y vistas, para el Documento 3

No se edita ningún archivo generado: si cambia un DSD, se corre de nuevo.
"""
import collections, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import dc_larman as X
import modelo_conceptual as M

D = X.D
DOC = D + "documentos/"
SAL = D + "diagramas/clases-diseno/"
TINTA = "#2C4257"
ANCHO_LINEA = 58    # un miembro más largo se parte en la coma, para que el diagrama no se ensanche

# ======================================================================== qué va en cada vista
# Las vistas de dominio son las áreas del modelo conceptual (M.VISTAS), con el mismo foco.
# Las vistas por módulo agrupan los módulos del backend; las clases de otros módulos con las que
# colaboran se dibujan de referencia, sin miembros.
VISTAS_MODULOS = [
    ("Acceso, registro y clientes", "Acceso-y-clientes", ["auth", "registro", "firebase", "users", "customer"]),
    ("Pedido: alta, cancelación y entrega", "Pedidos",
     ["=CreateOrderUseCase", "=CancelOrderUseCase", "=OrderService", "=UpdateOrderStatusUseCase",
      "=ConfirmDeliveryUseCase", "=CashCollectionUseCase", "=NotificationPort", "=Map<String, Pedido>",
      "=OrderRepositoryPort", "=CylinderLifecyclePort"]),
    ("Pagos, stock y reclamos", "Pagos-stock-y-reclamos",
     ["payments", "=ConfirmPaymentUseCase", "stock", "truck-load", "claims"]),
    ("Despacho y seguimiento en tiempo real", "Despacho",
     ["=DispatchOrchestratorService", "=DispatchService", "=DispatchOfferRepositoryPort", "=RealtimeDispatchPort",
      "route-batch", "distributor", "delivery", "gateways", "notifications"]),
    ("Flota, recompra y recupero de envases", "Flota-recompra-y-recupero", ["fleet", "repurchase", "repurchase-forecast", "cylinder"]),
]

# Vistas de dominio: el foco lleva atributos y operaciones; la referencia, solo el nombre.
VISTAS_DOMINIO = [
    ("Cuentas, clientes y catálogo", "Cuentas-clientes-y-catalogo",
     ["Usuario", "Distribuidora", "Cliente", "Carrito", "FranjaHoraria", "ZonaCobertura", "Producto", "Envase",
      "InvitacionRecompra", "ItemSugerido"],
     ["Pedido", "Chofer"]),
    ("Pedido, pago y reclamo", "Pedido",
     ["Pedido", "ItemPedido", "CambioEstadoPedido", "Pago", "Reclamo"],
     ["Cliente", "Chofer", "Producto", "Usuario", "Envase"]),
    ("Despacho, flota y recupero de envases", "Despacho-flota-y-recupero",
     ["OfertaDespacho", "LoteRecorrido", "OfertaLote", "ParadaLote", "PropuestaVentanaTaller", "TareaMantenimiento",
      "Chofer", "Vehiculo", "UbicacionGPS", "CasoRecupero", "AvisoRecupero"],
     ["Pedido", "Cliente", "Envase", "Usuario", "Distribuidora"]),
]
_cubiertas = [c for _, _, f, _ in VISTAS_DOMINIO for c in f]

# Áreas de los paquetes del diagrama de dependencias.
AREAS_PAQUETES = [
    ("Acceso", ["auth", "registro", "users", "role", "admin", "firebase", "audit"]),
    ("Negocio", ["order", "payments", "cart", "customer", "user-address", "repurchase", "claims",
                 "incident", "rating", "reports", "time-slot", "coverage-zone", "gascylinder",
                 "cylinder", "distributor"]),
    ("Flota y despacho", ["delivery", "car", "fleet", "fleet-expense", "gateways"]),
    ("Personal", ["employee", "attachment"]),
    ("Soporte", ["notifications", "email", "redis", "s3", "health"]),
    ("Stock y compras", ["stock", "purchase", "truck-load"]),
]

CAB = f"""!include ../estilo-vp.iuml
skinparam nodesep 40
skinparam ranksep 55
skinparam genericDisplay old
skinparam class<<referencia>> {{
  BackgroundColor #F1F1F1
  BorderColor #8A97A3
  FontColor #55616C
}}
skinparam class<<fachada>> {{
  HeaderBackgroundColor #B7CDE8
}}
skinparam class<<controlador>> {{
  HeaderBackgroundColor #B7CDE8
}}
skinparam class<<fabricación pura>> {{
  HeaderBackgroundColor #E4ECF6
}}
skinparam class<<colección>> {{
  HeaderBackgroundColor #E6E6E6
}}
skinparam class<<adaptador>> {{
  HeaderBackgroundColor #D5E3F3
}}
skinparam packageStyle rectangle
hide circle
hide empty members
"""

# ======================================================================== el modelo
dc = X.construir()
if X.FALTAN:
    sys.exit("Faltan tipos en el glosario de dc_larman.py:\n  " + "\n  ".join(sorted(X.FALTAN)))
if dc.sin_resolver:
    sys.exit("\n".join(dc.sin_resolver))


_dom = {n for n, c in dc.clases.items() if c.tipo == "dominio"}
assert _dom == set(_cubiertas), f"las vistas de dominio no cubren las clases de los DSD: {sorted(_dom ^ set(_cubiertas))}"


def ident(nombre):
    """Identificador PlantUML de una clase: `Map<String, Pedido>` -> Map_String_Pedido."""
    return re.sub(r'\W+', '_', nombre).strip("_")


def decl_clase(nombre, miembros=True, referencia=False):
    cl = dc.clases[nombre]
    id_ = ident(nombre)
    est = None if referencia else (cl.estereotipo if cl.tipo != "dominio" else None)
    if referencia:
        est = "referencia"
    marca = f" <<{est}>>" if est else ""
    if cl.tipo == "puerto" and not referencia:
        marca = " <<puerto>>"
    visible = f'"{nombre}" as {id_}' if id_ != nombre else nombre
    if cl.tipo == "puerto" and not referencia:
        tipo = "interface"
    elif cl.abstracta:
        tipo = "abstract class"
    else:
        tipo = "class"
    if referencia or not miembros:
        return [f"{tipo} {visible}{marca}"]
    lin = [f"{tipo} {visible}{marca} {{"]
    for vis, n, t in cl.atributos:
        lin.append(f"  {vis} {n}: {t}")
    for op in ordenar_ops(cl):
        lin.append("  + " + partir(op.firma(nombre)))
    lin.append("}")
    return lin


def ordenar_ops(cl):
    return sorted(cl.ops.values(), key=lambda o: (not o.crea, o.nombre.lower(), len(o.params)))


def partir(firma, ancho=ANCHO_LINEA):
    """Parte una firma larga en la coma de la lista de parámetros (`\\n` es un salto de renglón)."""
    if len(firma) <= ancho:
        return firma
    partes, actual = [], ""
    for tr in re.split(r'(?<=, )', firma):
        if actual and len(actual) + len(tr) > ancho:
            partes.append(actual.rstrip())
            actual = "      "
        actual += tr
    partes.append(actual)
    return "\\n".join(partes)


def flecha_asoc(a):
    """Línea PlantUML de una asociación del DC: navegabilidad, multiplicidad y nombre."""
    ia, ib = ident(a["a"]), ident(a["b"])
    ma = f' "{a["ma"]}"' if a["ma"] else ""
    mb = f' "{a["mb"]}"' if a["mb"] else ""
    nombre = f" : {a['nombre']}" if a["nombre"] else ""
    if a["tipo"] == "comp":
        assert not (a["nav_ba"] and not a["nav_ab"]), f"composición navegada del lado de la parte: {a}"
        # PlantUML no dibuja el rombo con flecha en los dos extremos: sin punta es navegable en ambos
        sig = "*-->" if (a["nav_ab"] and not a["nav_ba"]) else "*--"
    elif a["tipo"] == "agreg":
        sig = "o-->"
    else:
        sig = "<-->" if (a["nav_ab"] and a["nav_ba"]) else "-->" if a["nav_ab"] else "<--" if a["nav_ba"] else "--"
    return f"{ia}{ma} {sig}{mb} {ib}{nombre}"


def flecha_dep(o, d):
    """Dependencia `..>`; la creación lleva «create» pegado al extremo de la clase creada, para que
    la etiqueta no flote en el medio de una línea larga."""
    if (o, d) in dc.creaciones:
        return f'{ident(o)} ..> "<<create>>" {ident(d)}'
    return f"{ident(o)} ..> {ident(d)}"


def lineas_relaciones(en_vista, con_nombre=True, ambos_extremos=True, incluir_dep=True):
    """Relaciones entre las clases `en_vista`. `ambos_extremos`: solo las que tienen ambos
    extremos dentro de la vista; si no, alcanza con uno (las de referencia se dibujan igual)."""
    r = []
    for a in dc.asociaciones:
        if a["a"] in en_vista and a["b"] in en_vista:
            r.append(flecha_asoc(a if con_nombre else dict(a, nombre="")))
    if incluir_dep:
        for o, d in sorted(dc.dependencias):
            if o in en_vista and d in en_vista:
                r.append(flecha_dep(o, d))
    for ad, pu in dc.realizaciones:
        if ad in en_vista and pu in en_vista:
            r.append(f"{ident(ad)} ..|> {ident(pu)}")
    return r


def generalizaciones(en_vista):
    r = []
    por_padre = collections.OrderedDict()
    for p, h in dc.generalizaciones:
        if p in en_vista and h in en_vista:
            por_padre.setdefault(p, []).append(h)
    for p, hs in por_padre.items():
        restr = next(x[2] for x in M.GENERALIZACIONES if x[0] == p)
        for k, h in enumerate(hs):
            r.append(f"{p} <|-- {h}" + (f" : {restr}" if k == 0 else ""))
    return r


# ======================================================================== vistas de dominio
def vista_dominio(titulo, foco, ref):
    foco_s = set(foco)
    # una referencia que no se relaciona con ninguna clase del foco no aporta nada a la vista
    usadas = set()
    for a in dc.asociaciones:
        if a["a"] in foco_s: usadas.add(a["b"])
        if a["b"] in foco_s: usadas.add(a["a"])
    for o, d in dc.dependencias:
        if o in foco_s: usadas.add(d)
        if d in foco_s: usadas.add(o)
    for p, h in dc.generalizaciones:
        if p in foco_s: usadas.add(h)
        if h in foco_s: usadas.add(p)
    ref = [n for n in ref if n in usadas or n in foco_s]
    en_vista = foco_s | set(ref)
    lin = ["@startuml", CAB]
    for n in foco:
        lin += decl_clase(n)
    for n in ref:
        if n not in foco:
            lin += decl_clase(n, referencia=True)
    lin.append("")
    lin += generalizaciones(en_vista)
    # no se dibuja lo que une dos referencias entre sí: es de otra vista
    foco_s = set(foco)
    for a in dc.asociaciones:
        if a["a"] in en_vista and a["b"] in en_vista and (a["a"] in foco_s or a["b"] in foco_s):
            lin.append(flecha_asoc(a))
    for o, d in sorted(dc.dependencias):
        if o in en_vista and d in en_vista and (o in foco_s or d in foco_s):
            lin.append(flecha_dep(o, d))
    c, a_, b_ = M.CLASE_ASOCIACION
    if {c, a_, b_} <= en_vista:
        lin.append(f"({a_}, {b_}) .. {c}")
    if len(en_vista) > len(foco_s):
        lin += ["", "legend bottom right",
                "  Las clases en gris pertenecen a otra vista; se muestran solo como referencia.",
                "endlegend"]
    lin.append("@enduml")
    return "\n".join(lin)


AUTORIA = {"origina", "efectúa", "ejecuta", "resuelve", "reporta", "realiza", "emite", "recibe"}


def vista_general():
    """Todas las clases de dominio, sin miembros, en paquetes por contexto."""
    lin = ["@startuml", CAB, "skinparam nodesep 18", "skinparam ranksep 35"]
    for clave, ttl in M.CONTEXTOS:
        miembros = [n for n, (c, _, _) in M.CLASES.items() if c == clave and n in dc.clases]
        for n in miembros:
            lin += decl_clase(n, miembros=False)
    lin.append("")
    todas = {n for n in M.CLASES if n in dc.clases}
    lin += generalizaciones(todas)
    vistas = [a for a in dc.asociaciones if a["a"] in todas and a["b"] in todas
              and not (a["a"] == "Usuario" and a["nombre"] in AUTORIA and a["b"] != "AsientoAuditoria")]
    # entre un mismo par de clases hay a veces dos asociaciones: solo ésas llevan el nombre, para distinguirlas
    por_par = collections.Counter(frozenset((a["a"], a["b"])) for a in vistas)
    for a in vistas:
        repetida = por_par[frozenset((a["a"], a["b"]))] > 1
        lin.append(flecha_asoc(a if repetida else dict(a, nombre="")))
    c, a_, b_ = M.CLASE_ASOCIACION
    if {c, a_, b_} <= todas:
        lin.append(f"({a_}, {b_}) .. {c}")
    lin += ["", "legend bottom right",
            "  Vista de conjunto: sin miembros; solo llevan nombre las asociaciones que comparten par. La flecha abierta marca",
            "  la navegabilidad que piden los diagramas de interacción; se omiten las asociaciones",
            "  de Usuario que solo registran la autoría de un hecho, que figuran en su área.",
            "endlegend", "@enduml"]
    return "\n".join(lin)


# ======================================================================== vistas por módulo
def clases_de_vista(modulos):
    """Clases de diseño que no son de dominio de la vista: las de los módulos que nombra, y las
    que nombra una a una (`=Clase`)."""
    r = []
    for m in modulos:
        if m.startswith("="):
            if m[1:] in dc.clases:
                r.append(m[1:])
            continue
        r += [n for n, cl in dc.clases.items() if cl.tipo != "dominio" and cl.modulo == m]
    return list(collections.OrderedDict.fromkeys(r))   # una clase nombrada y de su módulo se declara una sola vez


def vista_modulo(titulo, propias):
    propias_s = set(propias)
    refs = []
    for a in dc.asociaciones:
        if a["a"] in propias_s and a["b"] not in propias_s and not a["mc"]:
            refs.append(a["b"])
    for o, d in sorted(dc.dependencias):
        if o in propias_s and d not in propias_s:
            refs.append(d)
    for ad, pu in dc.realizaciones:
        if pu in propias_s and ad not in propias_s:
            refs.append(ad)

    # una clase propia que solo recibe mensajes de clases de otra vista (un puerto, un validador)
    # quedaría suelta: se dibuja con quien la usa, en gris
    def tocadas(extra):
        t = set()
        for a in dc.asociaciones:
            if not a["mc"] and a["a"] in propias_s and (a["b"] in propias_s or a["b"] in extra):
                t |= {a["a"], a["b"]}
        for o, d in dc.dependencias:
            if o in propias_s and (d in propias_s or d in extra):
                t |= {o, d}
        for ad, pu in dc.realizaciones:
            if pu in propias_s:
                t |= {ad, pu}
        return t
    sueltas = [n for n in propias if n not in tocadas(set(refs))]
    entrantes = []
    for n in sueltas:
        for a in dc.asociaciones:
            if a["b"] == n and not a["mc"] and a["a"] not in propias_s:
                entrantes.append((a["a"], n, "asoc", a))
        for o, d in sorted(dc.dependencias):
            if d == n and o not in propias_s:
                entrantes.append((o, n, "dep", None))
    refs = list(collections.OrderedDict.fromkeys(refs + [o for o, _, _, _ in entrantes]))
    en_vista = propias_s | set(refs)
    lin = ["@startuml", CAB, "left to right direction", "skinparam nodesep 25", "skinparam ranksep 90"]
    for n in propias:
        lin += decl_clase(n)
    for n in refs:
        lin += decl_clase(n, referencia=True)
    lin.append("")
    for a in dc.asociaciones:
        if a["a"] in en_vista and a["b"] in en_vista and (a["a"] in propias_s or a["b"] in propias_s):
            if a["mc"] or a["a"] not in propias_s:
                continue        # las asociaciones del dominio están en su vista
            lin.append(flecha_asoc(dict(a, nombre="")))
    for o, d in sorted(dc.dependencias):
        if o in propias_s and d in en_vista:
            lin.append(flecha_dep(o, d))
    for o, d, tipo, a in entrantes:
        lin.append(flecha_asoc(dict(a, nombre="")) if tipo == "asoc" else flecha_dep(o, d))
    for ad, pu in dc.realizaciones:
        if ad in en_vista and pu in en_vista:
            lin.append(f"{ident(ad)} ..|> {ident(pu)}")
    lin += ["", "legend bottom right",
            "  Las clases en gris pertenecen a otra vista o a otro módulo; se muestran solo como referencia.",
            "endlegend", "@enduml"]
    return "\n".join(lin), refs


# ======================================================================== paquetes
def dependencias_de_modulo():
    deps = collections.defaultdict(set)

    def mod(c):
        return dc.clases[c].modulo

    for a in dc.asociaciones:
        if a["nav_ab"]:
            deps[(mod(a["a"]), mod(a["b"]))].add((a["a"], a["b"]))
        if a["nav_ba"]:
            deps[(mod(a["b"]), mod(a["a"]))].add((a["b"], a["a"]))
    for o, d in dc.dependencias:
        deps[(mod(o), mod(d))].add((o, d))
    for ad, pu in dc.realizaciones:
        deps[(mod(ad), mod(pu))].add((ad, pu))
    return {k: v for k, v in deps.items() if k[0] != k[1] and k[0] and k[1]}


def vista_paquetes():
    deps = dependencias_de_modulo()
    usados = {m for k in deps for m in k} | {c.modulo for c in dc.clases.values() if c.modulo}
    lin = ["@startuml", CAB, "skinparam nodesep 30", "skinparam ranksep 70",
           "skinparam package {", "  BackgroundColor #FFFFFF", "}"]
    colores = {"Acceso": "#EEF3F8", "Negocio": "#F7F3E8", "Flota y despacho": "#EEF5EF", "Personal": "#F5EEF3", "Soporte": "#F2F2F2", "Stock y compras": "#F4EEF7"}
    for area, mods in AREAS_PAQUETES:
        lin.append(f'package "{area}" as area_{ident(area)} {colores[area]} {{')
        for m in mods:
            if m in usados:
                n = sum(1 for c in dc.clases.values() if c.modulo == m)
                lin.append(f'  package "{m}" as {ident(m)} {{')
                lin.append("  }")
        lin.append("}")
    for (o, d) in sorted(deps):
        lin.append(f"{ident(o)} ..> {ident(d)}")
    lin += ["", "legend bottom right",
            "  Cada flecha punteada es una dependencia entre módulos: alguna clase del origen le manda",
            "  un mensaje, en algún DSD, a una clase del destino.",
            "endlegend", "@enduml"]
    return "\n".join(lin), deps


# ======================================================================== escritura y render
def escribir(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    open(ruta, "w", encoding="utf-8").write(texto if texto.endswith("\n") else texto + "\n")


def renderizar(nombres):
    entorno = dict(os.environ, PLANTUML_LIMIT_SIZE="32768")
    for n in nombres:
        for fmt in ("png", "svg"):
            r = subprocess.run(["plantuml", "-t" + fmt, "-charset", "UTF-8", SAL + n + ".puml"],
                               capture_output=True, text=True, env=entorno)
            if r.returncode or "Error" in (r.stdout + r.stderr):
                print("  ✗", n, fmt, (r.stderr or r.stdout).strip()[:300])
        if os.path.exists(SAL + n + ".png"):
            print(f"  ✓ {n} ({os.path.getsize(SAL + n + '.png') // 1024} KB)")


def main(render=True):
    nombres, indice = [], []

    escribir(SAL + "DC_General.puml", vista_general())
    nombres.append("DC_General")
    for titulo, archivo, foco, ref in VISTAS_DOMINIO:
        foco = [c for c in foco if c in dc.clases]
        ref = [c for c in ref if c in dc.clases]
        if not foco:
            continue
        nom = "DC_" + archivo
        escribir(SAL + nom + ".puml", vista_dominio(titulo, foco, ref))
        nombres.append(nom)
        indice.append(("dominio", titulo, nom, len(foco),
                       sum(len(dc.clases[c].ops) for c in foco)))
    vistas_mod = []
    for titulo, archivo, modulos in VISTAS_MODULOS:
        propias = clases_de_vista(modulos)
        if not propias:
            continue
        texto, refs = vista_modulo(titulo, propias)
        nom = "DC_Mod_" + archivo
        escribir(SAL + nom + ".puml", texto)
        nombres.append(nom)
        vistas_mod.append((titulo, archivo, propias, refs))
        indice.append(("módulo", titulo, nom, len(propias), sum(len(dc.clases[c].ops) for c in propias)))
    texto, deps = vista_paquetes()
    escribir(SAL + "DC_Paquetes.puml", texto)
    nombres.append("DC_Paquetes")

    # se borra solo lo que ya no tiene fuente: nunca una imagen que se vaya a quedar sin regenerar
    vigentes = set(nombres)
    for viejo in os.listdir(SAL):
        if os.path.splitext(viejo)[0] not in vigentes:
            os.remove(SAL + viejo)
    cifras(indice, deps)
    if "--documento" in sys.argv:
        aplicar_documento(documento(indice, vistas_mod, deps))
        print("  ✓ 3-Diseño.md sección 3 actualizada (corré numerar-figuras.py --aplicar)")
    print(f"  ✓ {len(dc.clases)} clases de diseño, "
          f"{sum(len(c.ops) for c in dc.clases.values())} operaciones, "
          f"{len(dc.asociaciones)} asociaciones, {len(dc.dependencias)} dependencias, "
          f"{len(deps)} dependencias entre módulos")
    if render:
        renderizar(nombres)


def documento(indice, vistas_mod, deps):
    """El texto de 3-Diseño.md sección 3, entre marcadores: cada corrida lo
    vuelve a escribir, así que las cifras y las figuras no se desactualizan."""
    nops = sum(len(c.ops) for c in dc.clases.values())
    roles = collections.defaultdict(list)
    for n, c in dc.clases.items():
        if c.tipo != "dominio":
            roles[c.estereotipo].append(n)
    doms = [n for n, c in dc.clases.items() if c.tipo == "dominio"]
    mc_asoc = sum(1 for a in dc.asociaciones if a["mc"])
    nav = sum(1 for a in dc.asociaciones if a["mc"] and (a["nav_ab"] or a["nav_ba"]))
    L = []
    L += ["<!-- dc:inicio -->", "## 3. Diagrama de Clase", "",
          "El diagrama de clases de diseño **se deriva de los diagramas de interacción** de la "
          "sección 2, como pide Larman en *UML y patrones*: cada mensaje que "
          "recibe un objeto es una operación de su clase, y la visibilidad entre dos objetos que se "
          "mandan mensajes decide la relación que los une. Se construye a partir de los "
          f"{len(X.archivos_dsd())} diagramas de interacción y del modelo "
          "conceptual (Documento 2, sección 1): lleva las clases que aparecen en esos diagramas, y todo lo "
          "que muestra sale de alguno de ellos.", "",
          "**Cómo se deriva.**", "",
          "| Del DSD | Al diagrama de clases |", "|---|---|",
          "| Un mensaje `A->>B: operacion(parametro)` | La operación `+ operacion(parametro: Tipo): Retorno` en la clase de `B`, con el retorno que el DSD muestra. Una operación aparece una sola vez aunque varios DSD la usen |",
          "| `«create»` hacia un objeto | Un constructor `+ «create» Clase(...)` y, si quien crea no es el agregado que lo contiene, una dependencia `«create»` |",
          "| Dos objetos de dominio que se mandan mensajes y tienen asociación en el modelo conceptual | Esa asociación, con su nombre y su multiplicidad, **navegable** en el sentido del mensaje (visibilidad por atributo) |",
          "| Un objeto de dominio que llega por parámetro o variable local (controlador a objeto, objeto a objeto sin asociación) | **Dependencia** (línea punteada) |",
          "| Servicio, puerto o colección que colabora con otro | Asociación navegable de multiplicidad 1: el colaborador se inyecta como atributo. Si el código real no lo inyecta, dependencia |",
          "| Primer receptor del mensaje del actor | `«controlador»` (clase `…UseCase` del módulo) o `«fachada»` (servicio fachada del módulo): el controlador de aplicación |",
          "| Objeto de infraestructura que solo recibe mensajes de otros | `«fabricación pura»` |",
          "| Puerto (`…Port`) | `interface` con `«puerto»`; el adaptador que lo realiza se dibuja con la flecha punteada de punta hueca solo si aparece en un DSD |",
          "| `:Map<String, X>` y `:List<X>` | `«colección»` agregada a su clase `X` (el DSD las usa para buscar por identificador) |", "",
          "**Notación.** Atributos `- nombre: Tipo` (privados; `/` marca un atributo derivado); operaciones "
          "`+ nombre(parametro: Tipo): Retorno`; `X[*]` es una colección de `X`; una línea sin punta no "
          "dice nada de la navegabilidad o es navegable en los dos sentidos (la composición se dibuja así "
          "cuando los DSD la recorren en ambos). Los nombres están en el idioma del DSD: las clases de "
          "dominio son las del modelo conceptual (`Pedido`, `ItemPedido`) y los controladores, "
          "fabricaciones puras y puertos llevan su nombre real (`CreateOrderUseCase`, "
          "`OrderPricingService`, `NotificationPort`). Una operación sin retorno es una "
          "que el DSD no muestra devolviendo nada. Una operación tiene una sola firma por clase y un "
          "solo retorno: cuando el DSD devuelve varios valores, el retorno es un `Registro`; un "
          "argumento que no todas las llamadas pasan se marca opcional (`= ninguno`). Los argumentos "
          "son variables con su tipo, nunca valores literales; los importes son `Moneda` y las horas, "
          "`Hora` o `FechaHora`.", "",
          "**Tipos.** Los primitivos son los de las operaciones del sistema del Documento 2; los de los "
          "atributos de dominio salen de las columnas del backend, y los de los argumentos y retornos, "
          "de esas operaciones o del modelo conceptual.", "",
          "| Tipo | Significado |", "|---|---|"]
    L += [f"| `{k}` | {v} |" for k, v in X.PRIMITIVOS.items()]
    L += ["", "| Enumeración | Enumeración del backend |", "|---|---|"]
    usadas = sorted({t for c in dc.clases.values() for _, _, t in c.atributos} |
                    {t for c in dc.clases.values() for o in c.ops.values() for _, t in o.params})
    L += [f"| `{es}` | `{en}` |" for en, es in sorted(X.ENUMERACIONES.items(), key=lambda x: x[1]) if es in usadas]
    L += ["", f"En total el diagrama tiene **{len(dc.clases)} clases** y **{nops} operaciones**: "
          f"{len(doms)} clases de dominio (las del modelo conceptual que aparecen en los diagramas) y "
          f"{len(dc.clases) - len(doms)} de diseño ("
          + ", ".join(f"{len(v)} {k}" for k, v in sorted(roles.items())) + f"). Las {mc_asoc} asociaciones "
          f"del modelo conceptual están todas; {nav} resultan navegables según los mensajes de los DSD, "
          f"y {len(dc.dependencias)} pares de clases quedan unidos por una dependencia.", "",
          "### 3.1 Clases del Dominio", "",
          "Las clases del modelo conceptual, con sus atributos tipados y las operaciones que reciben en "
          "los DSD. La vista general no lleva miembros; las vistas por área llevan todos y dibujan en "
          "gris, solo como referencia, las clases de otra área. Cada asociación del modelo conceptual "
          "está en alguna vista, con su multiplicidad.", "",
          "![Clases de dominio: vista general](../diagramas/clases-diseno/DC_General.png)", "",
          "**Figura 0 — Diagrama de Clase: dominio, vista general**", ""]
    for tipo, titulo, nom, n, o in indice:
        if tipo != "dominio":
            continue
        L += [f"![Clases de dominio: {titulo.lower()}](../diagramas/clases-diseno/{nom}.png)", "",
              f"**Figura 0 — Diagrama de Clase: dominio, {titulo.lower()}**", ""]
    L += ["### 3.2 Clases de Diseño", "",
          "Los controladores, las fabricaciones puras, los puertos y las colecciones de los DSD, "
          "agrupados por la parte del sistema en la que colaboran. Cada vista "
          "dibuja con todas sus operaciones las clases de su módulo y, en gris, las clases con las que "
          "colabora. Las clases de dominio de cada diagrama están en 3.1.", "",
          "| Papel | Clases |", "|---|---|"]
    for k, v in sorted(roles.items()):
        L.append(f"| `«{k}»` | {', '.join(f'`{x}`' for x in sorted(v))} |")
    L.append("")
    if dc.realizaciones:
        L += ["Realizaciones puerto-adaptador que aparecen en los DSD: " +
              ", ".join(f"`{a}` realiza `{p}`" for a, p in dc.realizaciones) + ".", ""]
    else:
        L += ["Ningún DSD llega hasta un adaptador (los diagramas terminan en el puerto), así que el "
              "diagrama no dibuja realizaciones; cuando un DSD nombre un adaptador, la realización "
              "se dibuja sola.", ""]
    for titulo, archivo, propias, refs in vistas_mod:
        L += [f"![Clases de diseño: {titulo.lower()}](../diagramas/clases-diseno/DC_Mod_{archivo}.png)", "",
              f"**Figura 0 — Diagrama de Clase: diseño, {titulo.lower()}**", ""]
    L += ["", "<!-- dc:fin -->"]
    return "\n".join(L)


def aplicar_documento(texto):
    ruta = DOC + "3-Diseño.md"
    doc = open(ruta, encoding="utf-8").read()
    ini, fin = doc.find("<!-- dc:inicio -->"), doc.find("<!-- dc:fin -->")
    if ini == -1 or fin == -1:
        sys.exit("3-Diseño.md no tiene los marcadores <!-- dc:inicio --> y <!-- dc:fin -->")
    open(ruta, "w", encoding="utf-8").write(doc[:ini] + texto + doc[fin + len("<!-- dc:fin -->"):])


def cifras(indice, deps):
    """Cifras del DC para el documento: se pegan en 3-Diseño.md §5."""
    por_tipo = collections.Counter(c.tipo if c.tipo != "servicio" else c.estereotipo for c in dc.clases.values())
    nops = sum(len(c.ops) for c in dc.clases.values())
    l = ["# Cifras del diagrama de clases de diseño", "",
         "Las genera `generar-clases-diseno.py`; no se editan a mano.", "",
         f"- Clases de diseño: **{len(dc.clases)}**; operaciones: **{nops}**.",
         "- Por papel: " + ", ".join(f"{k}: {v}" for k, v in sorted(por_tipo.items())) + ".",
         f"- Asociaciones: {len(dc.asociaciones)} ({sum(1 for a in dc.asociaciones if a['mc'])} del modelo "
         f"conceptual, {sum(1 for a in dc.asociaciones if not a['mc'])} de colaboración); "
         f"dependencias: {len(dc.dependencias)}; realizaciones: {len(dc.realizaciones)}.",
         f"- Dependencias entre módulos: {len(deps)}.", "",
         "| Vista | Archivo | Clases | Operaciones |", "|---|---|---:|---:|"]
    for tipo, titulo, nom, n, o in indice:
        l.append(f"| {titulo} ({tipo}) | `diagramas/clases-diseno/{nom}.png` | {n} | {o} |")
    escribir(D + "catedra/material-de-trabajo/indice-clases-diseno.md", "\n".join(l))


if __name__ == "__main__":
    main(render="--sin-render" not in sys.argv)
