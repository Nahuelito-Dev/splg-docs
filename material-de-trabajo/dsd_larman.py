"""Lectura y reglas de los diagramas de interacción de diseño (DSD) en estilo Larman.

Lo usan `verificar-dsd-larman.py` (las reglas de la guía), `cruzar-dsd-clases.py` (el cruce
contra el código) y `verificar-conformidad.py` (el gate). La guía es
`material-de-trabajo/GUIA-DSD-LARMAN.md`.

Un DSD está en estilo Larman si alguna de sus líneas de vida lleva el formato de objeto
(`:Clase` o `nombre:Clase`). Los anteriores, hechos como traza del código, no lo llevan y
siguen bajo las reglas viejas del cruce hasta que se rehacen.
"""
import glob, json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__)) + "/../"
BACK = os.path.abspath(D + "../splg-app-backend") + "/src/"
sys.path.insert(0, D)

# --------------------------------------------------------------------------- catálogo
def catalogo():
    c = json.load(open(D + "material-de-trabajo/operaciones-sistema.json", encoding="utf-8"))
    return c["actores"], {o["nombre"]: o for o in c["operaciones"]}


def casos_planificados():
    """CU cuyo estado en el catálogo de Casos-de-Uso.md es «Planificado»."""
    t = open(D + "Casos-de-Uso.md", encoding="utf-8").read()
    return {m.group(1) for m in re.finditer(
        r'^\| (CU-\d{3}) [^|]+\| SS-\d\d \|[^|]*\|[^|]*\| Planificado[^|]*\|', t, re.M)}


def nombres_de_casos():
    t = open(D + "Casos-de-Uso.md", encoding="utf-8").read()
    return {m.group(1): m.group(2).strip()
            for m in re.finditer(r'^\| (CU-\d{3}) ([^|]+?) \| SS-\d\d \|', t, re.M)}


# --------------------------------------------------------------------------- el código
def clases_del_codigo():
    """clase -> conjunto de métodos, de todo `src/` (igual criterio que el cruce)."""
    clase = re.compile(r'^(?:export\s+)?(?:default\s+)?(?:abstract\s+)?class\s+(\w+)', re.M)
    metodo = re.compile(
        r'^  (?:(?:public|private|protected|static|async|readonly|override|abstract)\s+)*'
        r'(?:get\s+|set\s+)?([A-Za-z_]\w*)\s*[<(]', re.M)
    r = {}
    for ruta in glob.glob(BACK + "**/*.ts", recursive=True):
        if ruta.endswith(".spec.ts"):
            continue
        txt = open(ruta, encoding="utf-8").read()
        for m in clase.finditer(txt):
            fin = txt.find("\n}\n", m.end())
            cuerpo = txt[m.end(): fin if fin != -1 else len(txt)]
            r.setdefault(m.group(1), set()).update(
                {x.group(1) for x in metodo.finditer(cuerpo)} - {"constructor", "if", "for", "while", "switch", "return", "catch", "super"})
    return r


def funciones_del_codigo():
    r = set()
    f = re.compile(r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)|^(?:export\s+)?const\s+(\w+)\s*[:=]', re.M)
    for ruta in glob.glob(BACK + "**/*.ts", recursive=True):
        if not ruta.endswith(".spec.ts"):
            for m in f.finditer(open(ruta, encoding="utf-8").read()):
                r.add(m.group(1) or m.group(2))
    return r


def manifiesto():
    return json.load(open(D + "material-de-trabajo/clases-codigo.json", encoding="utf-8"))


# Clases del diseño que todavía no existen en el código (módulos planificados del Documento 3).
# Un DSD de un caso planificado puede nombrarlas; en uno implementado, no.
PROPUESTAS_CLASE = {
  # Carrito persistente (I-3)
  "CartController": "CU-122 a CU-126: endpoints del carrito; el módulo cart sólo registra las entidades",
  "CartService": "CU-122 a CU-126: agregar, modificar, quitar, consultar y vaciar el carrito",
  # Consumo declarado y recompra (I-5, I-6): módulo repurchase (D8)
  "ConsumptionService": "CU-143, CU-144: orquesta el consumo declarado fuera de customer, para no crear un ciclo con order",
  "ConsumptionEstimatorService": "CU-143, CU-144, CU-106: estimador de la fecha de recompra (función pura en el módulo repurchase)",
  "RepurchaseController": "CU-144, CU-146: endpoints de consumo y de recompras estimadas, en el módulo repurchase",
  "RepurchaseEstimatesService": "CU-146: listado administrativo de recompras estimadas",
  "RepurchaseForecastService": "CU-106: proceso diario que estima e invita",
  "RepurchaseInvitationRepositoryPort": "CU-106: persistencia de las invitaciones de recompra",
  # Recupero de envases (I-8)
  "CylinderRecoveryService": "CU-108: proceso diario del recupero de envases",
  "DepositLedgerService": "CU-108: registra la liberación y la decisión sobre el depósito, sin cobro por pasarela (D14)",
  "RecoveryCaseRepositoryPort": "CU-108: persistencia de los casos de recupero",
  # Módulos inteligentes de flota y recorrido (I-9, I-10)
  "DemandForecastService": "CU-105: demanda proyectada por franja y zona",
  "FleetAvailabilityPort": "CU-105: puerto que consulta el despacho para saber si un vehículo está apto",
  "FleetCapacityService": "CU-107: capacidad de carga del vehículo en uso",
  "FleetCoverageService": "CU-105: mínimo de vehículos por zona, con la zona derivada de las entregas (D15)",
  "FleetMaintenancePlannerService": "CU-105: proceso diario del planificador de flota",
  "MaintenanceTaskRepositoryPort": "CU-105: persistencia de las tareas con ventana propuesta",
  "MaintenanceWindowProposalRepositoryPort": "CU-105: persistencia de las propuestas de ventana de taller",
  "VehicleUsageRepositoryPort": "CU-105: registro de uso (kilómetros) por vehículo y día",
  "RouteBatchPlannerService": "CU-107: proceso que agrupa pedidos programados en recorridos (D13)",
  "RouteBatchRepositoryPort": "CU-107: persistencia de lotes, paradas y ofertas",
  "RouteSequencerService": "CU-107: orden de las paradas de un lote",
  # Pequeños huecos (I-1)
  "CoverageZoneCronService": "CU-151: barrido que desactiva las zonas vencidas",
  "UpdateTimeSlotDto": "CU-043: validación de la modificación de una franja",
  # Configuración de procesos y tareas (I-1)
  "ModuleConfigController": "CU-171, CU-172, CU-173: endpoints de la configuración de procesos por distribuidora",
  "ModuleConfigService": "CU-171, CU-172, CU-173: lee y valida los parámetros de module_config, con los valores por omisión",
  "DispatchConfigService": "CU-171: entrega al despacho los parámetros de su distribuidora, con una copia en memoria de un minuto",
  "ScheduledTaskGate": "CU-173: decide en cada ciclo qué distribuidoras atiende cada tarea programada, según su intervalo",
  # Historial de estados del pedido (I-4)
  "OrderStatusHistoryService": "CU-169, CU-170: escribe y lee order_status_history, que existe sin servicio",
  # Caja, rendición, cuentas corrientes y comisiones (I-14)
  "CashBoxService": "CU-225 a CU-227, CU-264: cajas y sesiones de caja con arqueo, módulo cash",
  "CashLedgerService": "CU-228, CU-229: punto único de escritura del libro de caja y de los saldos",
  "CashCategoryService": "CU-230, CU-265: categorías de ingresos y gastos de caja",
  "DriverSettlementService": "CU-232, CU-233: presentación, aprobación y reapertura de la rendición del chofer",
  "DriverSettlementCron": "CU-231: proceso diario que abre las rendiciones",
  "SettlementOverdueCron": "CU-234: proceso diario que avisa las rendiciones sin cerrar",
  "CustomerAccountService": "CU-235 a CU-239: cuentas corrientes, cargos, pagos, ajustes y consultas",
  "CommissionService": "CU-240 a CU-244: reglas, comisiones por entrega y liquidaciones",
  "FinanceDashboardService": "CU-245: tablero financiero",
  # Reintegro de pagos (I-7)
  "ReintegroListener": "CU-168: escucha el evento de pedido cancelado",
  "RefundPaymentUseCase": "CU-168: devuelve el pago por la pasarela, fuera de la transacción de la cancelación",
  # Personal y legajos (I-11): módulo employee. Puestos, legajos, egreso y cuenta ya están construidos.
  "AttendanceService": "CU-189, CU-190: jornadas de trabajo, cargadas por el panel o marcadas por el chofer",
  "LeaveService": "CU-191, CU-192: licencias y ausencias, su solicitud y su resolución",
  "PersonnelDashboardService": "CU-194: cifras del tablero de personal",
  "VacationPolicy": "CU-193: función pura de los días de vacaciones por antigüedad, LCT art. 150 (domain/vacaciones.ts)",
  # Flota ampliada (I-12): módulo fleet-expense
  "FuelLoadService": "CU-195, CU-196: cargas de combustible y consumo de un vehículo, en el módulo fleet-expense",
  "FuelConsumptionCalculator": "CU-195, CU-196: función pura del consumo por tramo entre cargas de tanque lleno y de su desvío (domain/consumo.ts)",
  "TrafficFineService": "CU-198 a CU-200: multas de tránsito, su pago y su imputación al chofer",
  "FleetExpenseAlertsCron": "CU-198: aviso diario de las multas por vencer, 08:00 hora argentina",
  "VehicleAccidentService": "CU-201, CU-202: siniestros de los vehículos, su avance y su cierre",
  "FleetCostReportService": "CU-203, CU-204: modelo de lectura del costo por vehículo y de la flota, en el módulo reports",
  "TireService": "CU-205, CU-206: neumáticos y sus movimientos (funcionalidad opcional)",
}


# Clases de bibliotecas que pueden ser participantes de un DSD porque son la única clase de
# aplicación de su operación (no hay una propia en `src/`).
LIBRERIA_PARTICIPANTE = {
    # @nestjs/terminus: CU-104, verificación de salud del sistema.
    "HealthCheckService",
}

# Clases de bibliotecas que la tabla de implementación puede citar sin que existan en `src/`.
EXTERNAS = {"QueryRunner", "EntityManager", "Repository", "DataSource", "Decimal",
            # @nestjs/terminus: es la única clase de aplicación de CU-104 (salud del sistema).
            "HealthCheckService"}

# Casos que sólo se incluyen: ningún actor los inicia ni tienen operación del sistema en el
# catálogo. Su DSD es el fragmento que realiza el caso incluido: el primer mensaje sale del
# controlador del caso base (`controladores`) y lleva la `firma` de acá; una nota «Caso incluido
# desde CU-…» nombra a los casos base. Nombre de archivo: DSD_CU-xxx_<operacion>.mmd.
INCLUIDOS = {
    "crearUsuarioBase": {"casos": ["CU-082"], "bases": ["CU-002", "CU-003", "CU-031", "CU-086", "CU-087"],
                         "controladores": {"RegistroService"},
                         "firma": "registrar(datosPersonales, rol, distribuidoraId)"},
    "almacenarArchivo": {"casos": ["CU-159"], "bases": ["CU-155", "CU-174"],
                         "controladores": {"FleetAttachmentService", "ClaimsService"},
                         "firma": "put(clave, contenido, tipo)"},
    "recuperarArchivo": {"casos": ["CU-160"], "bases": ["CU-157", "CU-175"],
                         "controladores": {"FleetAttachmentService", "ClaimsService"},
                         "firma": "getSignedDownload(clave, nombreDeDescarga)"},
    # No es un caso incluido sino una operación interna: ningún actor la invoca y no es del
    # catálogo; la ejecuta CreateOrderUseCase dentro de crearPedido, crearReserva y
    # realizarCompraExpress. Se la trata igual (primer mensaje desde el controlador del caso base).
    # Planificado (I-11): el gate de despacho ampliado con la situación laboral del chofer.
    "verificarHabilitacionLaboral": {"casos": ["CU-246"], "bases": ["CU-012", "CU-013", "CU-015"],
                                     "controladores": {"OrderService", "DispatchOrchestratorService",
                                                       "UpdateOrderStatusUseCase"},
                                     "firma": "verificarHabilitacionLaboral(chofer)"},
    "verificarCargaDeCamionAbierta": {"casos": ["CU-248"], "bases": ["CU-012", "CU-013", "CU-015", "CU-080"],
                                      "controladores": {"OrderService", "DispatchOrchestratorService",
                                                        "UpdateOrderStatusUseCase"},
                                      "firma": "verificarCargaDeCamionAbierta(chofer)"},
    "aplicarMovimientoDeStock": {"casos": ["CU-250"],
                                 "bases": ["CU-212", "CU-213", "CU-217", "CU-218", "CU-219", "CU-220", "CU-222", "CU-274", "CU-276", "CU-280"],
                                 "controladores": {"StockTransferUseCase", "StockAdjustmentUseCase", "InitialCountUseCase",
                                                   "ReverseBatchUseCase", "StockDeliveryService",
                                                   "ReceivePurchaseUseCase", "VoidPurchaseReceiptUseCase",
                                                   "ReloadTruckLoadUseCase", "DepartTruckLoadUseCase",
                                                   "CloseTruckLoadUseCase"},
                                 "firma": "aplicar(operacion)"},
    "descontarStockDeLaEntrega": {"casos": ["CU-220"], "bases": ["CU-020", "CU-079", "CU-278"],
                                  "controladores": {"UpdateOrderStatusUseCase", "ReapplyDeliveriesUseCase"},
                                  "firma": "registrarEntrega(entrega)"},
    "crearCheckoutDePago": {"casos": ["CU-048"], "bases": ["CU-005", "CU-072", "CU-147"],
                            "controladores": {"CreateOrderUseCase"},
                            "firma": "crearCheckoutDePago(pedidoId, medioDePago)",
                            "frase": "Operación interna invocada desde"},
}

# --------------------------------------------------------------------------- lectura
NOMBRE = re.compile(r'^DSD_((?:CU-\d{3}_)+)(\w+)\.mmd$')
PART = re.compile(r'^\s*(create\s+)?(participant|actor)\s+(\w+)\s+as\s+(.+?)\s*$')
MSG = re.compile(r'^\s*(\w+)\s*(-{1,2}(?:>>|x|\)))\s*([+-]?)\s*(\w+)\s*:\s*(.*?)\s*$')


def es_larman(src):
    return re.search(r'^\s*(?:create\s+)?participant\s+\w+\s+as\s+\w*:', src, re.M) is not None


def leer(ruta):
    src = open(ruta, encoding="utf-8").read()
    d = {"ruta": ruta, "base": os.path.basename(ruta), "src": src, "titulo": None,
         "actores": {}, "participantes": {}, "creados": set(), "mensajes": []}
    for linea in src.split("\n"):
        t = re.match(r'^\s*title\s+(.*)$', linea)
        if t:
            d["titulo"] = t.group(1).strip()
            continue
        p = PART.match(linea)
        if p:
            crea, tipo, ident, etiqueta = p.groups()
            etiqueta = etiqueta.replace("#lt;", "<").replace("#gt;", ">")
            (d["actores"] if tipo == "actor" else d["participantes"])[ident] = etiqueta
            if crea:
                d["creados"].add(ident)
            continue
        m = MSG.match(linea)
        if m:
            org, flecha, _act, dst, texto = m.groups()
            d["mensajes"].append({"de": org, "flecha": flecha, "a": dst, "texto": texto})
    return d


def clase_de(etiqueta):
    """`:Pedido` y `pedido:Pedido` dan `Pedido`; `:Map<String, Reclamo>` da `Map<String, Reclamo>`."""
    return etiqueta.split(":", 1)[1].strip() if ":" in etiqueta else etiqueta


def partes_de_coleccion(clase):
    m = re.fullmatch(r'(Map|List)<(.+)>', clase)
    if not m:
        return None
    return [x.strip() for x in m.group(2).split(",")]


def clase_destino(d, ident):
    return clase_de(d["participantes"][ident]) if ident in d["participantes"] else None


def es_retorno(m):
    return m["flecha"] == "-->>"


def operacion(texto):
    m = re.match(r'^(«create»|[A-Za-z_]\w*)\s*(\(.*\))?', texto)
    return m.group(1) if m else None


def mc():
    import modelo_conceptual as m
    return m


def composiciones():
    """parte -> todo, según las asociaciones de composición del modelo conceptual."""
    return {a[4]: a[0] for a in mc().ASOCIACIONES if a[2] == "*"}


# --------------------------------------------------------------------------- tablas del documento
def bloque_mermaid(md, src):
    """Posición (fin del bloque) del bloque de `md` que tiene exactamente `src`, o None."""
    norm = lambda s: "\n".join(x.rstrip() for x in s.strip().split("\n"))
    for m in re.finditer(r'```mermaid\n(.*?)\n```', md, re.S):
        if norm(m.group(1)) == norm(src):
            return m.end()
    return None


def tabla_de_implementacion(md, src):
    """{(clase, operación): texto de la celda} de la tabla `Operación de diseño | Implementación`
    que sigue a un diagrama `src` dentro de `md` (si el diagrama aparece más de una vez, el
    primero que tenga la tabla); None si no hay diagrama o no hay tabla."""
    norm = lambda x: "\n".join(l.rstrip() for l in x.strip().split("\n"))
    t = None
    for m in re.finditer(r'```mermaid\n(.*?)\n```', md, re.S):
        if norm(m.group(1)) != norm(src):
            continue
        resto = md[m.end():]
        corte = re.search(r'```mermaid|^#{2,4} ', resto, re.M)
        resto = resto[: corte.start()] if corte else resto
        t = re.search(r'^\| Operación de diseño \| Implementación \|\n\|[-| ]+\|\n((?:\|.*\|\n?)+)', resto, re.M)
        if t:
            break
    if not t:
        return None
    filas = {}
    for linea in t.group(1).strip().split("\n"):
        celdas = [c.strip() for c in re.split(r'(?<!\\)\|', linea.strip().strip("|"))]
        k = re.match(r'^`(.+?)\.(«create»|\w+)(?:\(.*\))?`$', celdas[0])
        if k and len(celdas) >= 2:
            filas[(k.group(1), k.group(2))] = celdas[1]
    return filas


# --------------------------------------------------------------------------- reglas
AVISOS = []   # advertencias que no hacen fallar (p. ej. demasiadas líneas de vida)
MAX_LINEAS = 9


def verificar(estricto=False, solo=None):
    """Devuelve (errores, pendientes, hechos). `pendientes` son los pares (CU, operación) del
    catálogo que todavía no tienen un DSD en estilo Larman; en modo estricto son errores."""
    actores, ops = catalogo()
    planificados = casos_planificados()
    nombres = nombres_de_casos()
    M = mc()
    dominio = set(M.CLASES)
    codigo = clases_del_codigo()
    permitidas = dominio | set(codigo) | set(PROPUESTAS_CLASE) | LIBRERIA_PARTICIPANTE
    todo_de = composiciones()
    contratos = _contratos()
    doc3 = open(D + "3-Diseño.md", encoding="utf-8").read()
    casos = open(D + "Casos-de-Uso.md", encoding="utf-8").read()
    errores, hechos, cubiertos = [], [], set()
    incluidos_hechos = set()
    AVISOS.clear()

    archivos = sorted(glob.glob(D + "diagramas/DSD_*.mmd"))
    for ruta in archivos:
        base = os.path.basename(ruta)
        if solo and base not in solo:
            continue
        src = open(ruta, encoding="utf-8").read()
        if not es_larman(src):
            continue
        d = leer(ruta)
        e = lambda msg: errores.append(f"{base}: {msg}")
        nm = NOMBRE.match(base)
        if not nm:
            e("el nombre no es DSD_CU-xxx[_CU-yyy]_<operacion>.mmd")
            continue
        cus = re.findall(r'CU-\d{3}', nm.group(1))
        nombre_op = nm.group(2)
        inc = INCLUIDOS.get(nombre_op)
        o = ops.get(nombre_op)
        if inc and not o:
            o = {"casosDeUso": inc["casos"], "firma": inc["firma"], "actores": [], "cambiaEstado": False}
            incluidos_hechos.add(nombre_op)
        if not o:
            e(f"la operación {nombre_op} no está en el catálogo ni entre los casos incluidos")
            continue
        if cus != o["casosDeUso"]:
            e(f"los casos del nombre {cus} no son los del catálogo para {nombre_op}: {o['casosDeUso']}")
        for cu in cus:
            cubiertos.add((cu, nombre_op))
        planificado = all(cu in planificados for cu in cus)

        # título
        esperado = ("DSD — " + " / ".join(cus) + (" " + nombres.get(cus[0], "?") if len(cus) == 1 else "")
                    + " · " + nombre_op)
        if d["titulo"] != esperado:
            e(f"el título es {d['titulo']!r} y debería ser {esperado!r}")
        if not re.search(r'^\s*autonumber\s*$', src, re.M):
            e("falta autonumber")

        # primer mensaje
        if not d["mensajes"]:
            e("no tiene mensajes")
            continue
        m1 = d["mensajes"][0]
        if m1["texto"] != o["firma"]:
            e(f"el primer mensaje {m1['texto']!r} no es la firma del catálogo {o['firma']!r}")
        et = d["actores"].get(m1["de"])
        if inc:
            # fragmento de un caso incluido: sale del controlador del caso base, no de un actor
            origen = clase_destino(d, m1["de"])
            if origen not in inc["controladores"]:
                e(f"el primer mensaje sale de {origen!r}: tiene que ser el controlador del caso base {sorted(inc['controladores'])}")
            notas_inc = " ".join(re.findall(r'^\s*Note\s+.*?:\s*(.*)$', src, re.M))
            frase = inc.get("frase", "Caso incluido desde")
            if frase not in notas_inc or any(b not in notas_inc for b in inc["bases"]):
                e(f"falta la nota «{frase} …» con los casos base {', '.join(inc['bases'])}")
        elif et is None:
            e("el primer mensaje no sale de un actor")
        else:
            a = re.fullmatch(r'(.+) \((ACT-0[1-9])\)', et)
            if not a or a.group(2) not in actores or actores[a.group(2)] != a.group(1):
                e(f"el actor {et!r} no es del catálogo (nombre y código)")
            elif a.group(2) not in o["actores"]:
                e(f"{a.group(2)} no inicia {nombre_op} en el catálogo")
        ctrl = clase_destino(d, m1["a"])
        if ctrl is None or ctrl.endswith("Controller") or ctrl in dominio:
            e(f"el primer mensaje llega a {ctrl!r}: tiene que ser el controlador de aplicación (UseCase o Service), no el HTTP ni un objeto de dominio")

        # participantes
        clases_dsd = set()
        for ident, et in d["participantes"].items():
            if not re.fullmatch(r'[a-z]\w*:[A-Z][\w<>, ]*|:[A-Z][\w<>, ]*', et):
                e(f"la línea de vida {et!r} no es :Clase ni nombre:Clase")
                continue
            c = clase_de(et)
            partes = partes_de_coleccion(c)
            if partes:
                for x in partes:
                    if x not in ("String", "UUID", "Number") and x not in permitidas:
                        e(f"la colección {c!r} usa {x}, que no es una clase permitida")
                continue
            clases_dsd.add(c)
            if re.search(r'Guard|Pipe|Interceptor|QueryRunner|DataSource|EntityManager|Repository<|Controller$|Dto$|Mapper$', c):
                e(f"{c} no puede ser un participante (infraestructura del framework, HTTP, DTO o mapeo)")
            elif c not in permitidas:
                e(f"{c} no es una clase del modelo conceptual, del código ni de las planificadas")
            elif c in PROPUESTAS_CLASE and not planificado and c not in codigo:
                e(f"{c} es una clase planificada y {'/'.join(cus)} no está planificado")

        n_lineas = len(d["actores"]) + len(d["participantes"])
        if n_lineas > MAX_LINEAS:
            AVISOS.append(f"{base}: {n_lineas} líneas de vida (el tope es {MAX_LINEAS}); "
                          "los subprocesos que son otra operación del catálogo van con «ver DSD de …»")

        # asignaciones como mensaje
        for m in d["mensajes"]:
            if re.search(r'\sigual\s|[^=!<>]=[^=]|:=', m["texto"]):
                e(f"el mensaje {m['texto']!r} es una asignación; va como mensaje al objeto que tiene el dato")

        # creaciones
        destinos_create = set()
        for m in d["mensajes"]:
            if operacion(m["texto"]) == "«create»":
                destinos_create.add(m["a"])
                if m["a"] not in d["creados"]:
                    e(f"«create» a {m['a']}, que no está declarado con create participant")
                cr, cd = clase_destino(d, m["de"]), clase_destino(d, m["a"])
                if cd in todo_de and cr != todo_de[cd]:
                    e(f"{cd} es parte de {todo_de[cd]} (composición): la crea {todo_de[cd]}, no {cr}")
        for ident in d["creados"]:
            if ident not in destinos_create:
                e(f"{ident} se declara con create participant y nadie le manda «create»")

        # estado: al menos un objeto de dominio
        clases_dominio_dsd = {c for c in clases_dsd if c in dominio}
        if o["cambiaEstado"] and not clases_dominio_dsd:
            e("la operación cambia estado y el diagrama no tiene ningún objeto de dominio")

        # contrato: cada instancia creada y cada objeto modificado aparece
        post = contratos.get(nombre_op, "")
        notas = " ".join(re.findall(r'^\s*Note\s+.*?:\s*(.*)$', src, re.M))
        recibe = {clase_destino(d, m["a"]) for m in d["mensajes"]
                  if operacion(m["texto"]) != "«create»" and not es_retorno(m)}
        creados = {clase_destino(d, i) for i in d["creados"]}
        for s in re.split(r'(?<=\.)\s+', post):
            if re.search(r'\bcre(?:ó|aron)\b', s):
                for c in re.findall(r'(?:instancias? de|una|un|sus instancias de)\s+([A-Z]\w+)', s):
                    if c in dominio and c not in creados and not ("ver DSD de" in notas and c in notas):
                        e(f"la postcondición dice que se creó {c} y el diagrama no tiene «create» de {c}")
            elif re.search(r'atributo', s):
                for c in re.findall(r'(?:instancia de|del|de la)\s+([A-Z]\w+)', s):
                    if c in dominio and c not in recibe and c not in creados:
                        e(f"la postcondición modifica {c} y ningún mensaje llega a un {c}")

        # copias en los documentos y tabla de implementación
        for nom, md in (("3-Diseño.md", doc3), ("Casos-de-Uso.md", casos)):
            tab = tabla_de_implementacion(md, src)
            if bloque_mermaid(md, src) is None:
                e(f"el diagrama no está, idéntico, en {nom}")
            elif not planificado and tab is None:
                e(f"falta la tabla «Operación de diseño | Implementación» después del diagrama en {nom}")
        hechos.append(base)

    pendientes = sorted((cu, n) for n, o in ops.items() for cu in o["casosDeUso"] if (cu, n) not in cubiertos)
    pendientes += sorted((i["casos"][0], n) for n, i in INCLUIDOS.items() if (i["casos"][0], n) not in cubiertos)
    if solo:
        pendientes = []
    if estricto:
        errores += [f"{cu} {n}: no tiene DSD en estilo Larman" for cu, n in pendientes]
    return errores, pendientes, hechos


def _contratos():
    """operación -> texto de las postcondiciones del contrato en 2-Analisis.md."""
    t = open(D + "2-Analisis.md", encoding="utf-8").read()
    r = {}
    for m in re.finditer(r'Contrato: `(\w+)\(\)`.*?\*\*Postcondiciones\*\*\s*\|\s*(.*?)\s*\|\n', t, re.S):
        r[m.group(1)] = m.group(2)
    return r
