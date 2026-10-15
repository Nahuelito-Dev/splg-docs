#!/usr/bin/env python3
"""Cruza los diagramas de secuencia de diseño (DSD) con el código real: por cada
mensaje `Origen->>Destino: operacion(args)` de cada `diagramas/DSD_*.mmd`, verifica
que la clase del destino (resuelta por su alias de `participant`) exista en
`material-de-trabajo/clases-codigo.json` y que tenga un método con ese nombre.

    python3 material-de-trabajo/extraer-clases-codigo.py   # primero, si el código cambió
    python3 material-de-trabajo/cruzar-dsd-clases.py

Una diferencia puede quedar justificada en las tablas de excepciones de este archivo
(`MODULOS`, `PROPUESTAS_CLASE`, `EXCEPCIONES_OP`): cada entrada lleva su motivo y el
script la verifica contra el código en cada corrida, así que una excepción que deja de
ser cierta (la función se movió, lo propuesto ya se construyó) también hace fallar.

Sale 0 si no queda ninguna diferencia sin justificar, o 1 y el detalle si queda alguna.
Es aproximado (depende de cómo esté escrito cada mensaje, igual que advierte la
auditoría de los cuatro modelos), pero determinista: corriendo dos veces da el
mismo resultado, así que sirve para no reabrir lo mismo dos veces.
"""
import re, os, glob, json, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dsd_larman

D = os.path.dirname(os.path.abspath(__file__)) + "/../"
DSD_DIR = D + "diagramas/"
MANIFIESTO = D + "material-de-trabajo/clases-codigo.json"

if not os.path.exists(MANIFIESTO):
    sys.exit("Falta clases-codigo.json: corré primero extraer-clases-codigo.py")
manifest = json.load(open(MANIFIESTO, encoding="utf-8"))
metodos_por_clase = {c: {m["nombre"] for m in v.get("metodos", [])} for c, v in manifest.items()}

# Actores humanos o del sistema externo (no son clases del backend: no se
# modelan en el diagrama de clases de diseño) y bibliotecas/infraestructura
# de terceros que los DSD nombran como si fueran una clase propia. Cruzarlas
# contra el código no aporta nada: TypeORM, Nest y MercadoPago no son nuestras.
EXCLUIR = {
  "Administrador", "App", "Chofer", "Cliente", "Cualquiera", "Controlador",
  "Panel", "SuperAdmin", "Usuario", "CTRL",
  "ConfigService", "DataSource", "EntityManager", "QueryRunner", "Reflector",
  "EventEmitter2", "Decimal", "ValidationPipe", "ScheduleRegistry",
  "FirebaseAuthClientSDK", "MercadoPago", "HealthCheckService",
  "MemoryHealthIndicator", "DiskHealthIndicator", "TypeOrmHealthIndicator",
  "Load",
  # Marcador de lugar de los DSD de CU-159 y CU-160: «el caso de uso que incluye».
  "Caso",
}
EXCLUIR_PREFIJOS = ("Repository", "SelectQueryBuilder")

PARTICIPANTE = re.compile(r'^\s*(?:actor|participant)\s+(\w+)\s+as\s+(\w+)', re.M)
PARTICIPANTE_SIN_AS = re.compile(r'^\s*(?:actor|participant)\s+(\w+)\s*$', re.M)
MENSAJE = re.compile(
    r'^\s*(\w+)\s*(-+>>?|-\)|--\))\s*(\w+)\s*:\s*(.*)$', re.M)
OPERACION = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*\(')

def alias_de(ruta):
    src = open(ruta, encoding="utf-8").read()
    alias = {m.group(1): m.group(2) for m in PARTICIPANTE.finditer(src)}
    for m in PARTICIPANTE_SIN_AS.finditer(src):
        alias.setdefault(m.group(1), m.group(1))
    return alias, src


# ---------------------------------------------------------------- indice del codigo
# El manifiesto solo lleva las clases que entran al diagrama de clases de diseño.
# Para decidir si algo "existe en el código" se mira todo `src/`: clases (con sus
# métodos de 2 espacios de sangría, como deja Prettier) y funciones de módulo.
BACK = os.path.abspath(D + "../splg-app-backend") + "/src/"
if not os.path.isdir(BACK):
    sys.exit(f"No se encuentra el backend en {BACK}")

CLASE = re.compile(r'^(?:export\s+)?(?:default\s+)?(?:abstract\s+)?class\s+(\w+)', re.M)
METODO = re.compile(
    r'^  (?:(?:public|private|protected|static|async|readonly|override|abstract)\s+)*'
    r'(?:get\s+|set\s+)?([A-Za-z_]\w*)\s*[<(]', re.M)
FUNCION = re.compile(
    r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)|^(?:export\s+)?const\s+(\w+)\s*[:=]', re.M)
PALABRAS = {"constructor", "if", "for", "while", "switch", "return", "catch", "super"}

codigo_clases = {}                      # clase -> {"metodos": set, "archivo": str}
codigo_funciones = collections.defaultdict(set)   # nombre -> {archivos}
codigo_texto = {}
for ruta in glob.glob(BACK + "**/*.ts", recursive=True):
    if ruta.endswith(".spec.ts"):
        continue
    rel = os.path.relpath(ruta, BACK)
    txt = open(ruta, encoding="utf-8").read()
    codigo_texto[rel] = txt
    for m in FUNCION.finditer(txt):
        codigo_funciones[m.group(1) or m.group(2)].add(rel)
    cs = list(CLASE.finditer(txt))
    for i, m in enumerate(cs):
        fin = txt.find("\n}\n", m.end())
        cuerpo = txt[m.end(): fin if fin != -1 else len(txt)]
        info = codigo_clases.setdefault(m.group(1), {"metodos": set(), "archivo": rel})
        info["metodos"] |= {x.group(1) for x in METODO.finditer(cuerpo)} - PALABRAS

def existe_funcion(nombre, archivo):
    return archivo in codigo_funciones.get(nombre, ())

# ---------------------------------------------------------------- excepciones
# Participantes de un DSD que no son una clase del backend sino un módulo de
# funciones, un script o una abstracción: nombre -> (tipo, archivo o motivo).
# "modulo": cada operación que reciba tiene que ser una función exportada de ese archivo.
MODULOS = {
  "OrderStatusMachine": ("modulo", "order/domain/order-status.machine.ts"),
  "CylinderStateMachine": ("modulo", "cylinder/domain/cylinder-state.machine.ts"),
  "DeliveryCodeUtil": ("modulo", "order/domain/delivery-code.util.ts"),
  "PoliticaDeRegistro": ("modulo", "registro/politica-de-registro.ts"),
  "depurarCambios": ("modulo", "audit/depurar-cambios.ts"),
  "CurrentDistributor": ("modulo", "common/decorators/current-distributor.decorator.ts"),
  "ComandoCrearSuperAdmin": ("modulo", "cli/crear-superadmin.ts"),
}
# ServicioDelPerfil es la abstracción de CustomersService, DeliveryService y AdminService
# (el propio DSD de CU-082 lo aclara en una nota): cada operación tiene que existir en los tres.
ABSTRACCIONES = {"ServicioDelPerfil": ("CustomersService", "DeliveryService", "AdminService")}

# Colaboración propuesta: la clase todavía no existe en el código (el Documento 3 la
# marca como propuesta). Cada entrada dice a qué caso de uso responde y por qué; el
# script verifica que siga sin existir y falla si se construye sin sacarla de acá.
PROPUESTAS_CLASE = dsd_larman.PROPUESTAS_CLASE   # compartida con verificar-dsd-larman.py

def _propuestas(clase, motivo, *ops):
    return {(clase, op): ("propuesta", motivo) for op in ops}

# (clase, operación) -> (tipo, dónde o motivo). Tipos:
#   funcion     función de módulo en ese archivo (no un método de la clase)
#   local       función local dentro de un método de ese archivo
#   adaptador   método privado de la clase que implementa el puerto
#   biblioteca  función de una biblioteca de terceros
#   propuesta   operación todavía inexistente en esa clase; se verifica que siga así
EXCEPCIONES_OP = {
  ("OrderController", "mapRoleToCancelActor"): ("funcion", "order/application/cancel-order.use-case.ts"),
  ("CarAssignmentsController", "informarTotal"): ("funcion", "common/http/total.ts"),
  ("DeliveryVehicleController", "informarTotal"): ("funcion", "common/http/total.ts"),
  ("ClaimsService", "assertClaimTransition"): ("funcion", "claims/claim-status.machine.ts"),
  ("CreateOrderUseCase", "coordenadasDePunto"): ("funcion", "common/geo/punto.ts"),
  ("FleetExpirationsService", "calcularEstadoDeVencimiento"): ("funcion", "fleet/domain/expiration-status.ts"),
  ("FleetExpirationsService", "estaInhabilitado"): ("funcion", "fleet/domain/fleet-lock.util.ts"),
  ("GasCylinderService", "assertPromocionesSinRepetir"): ("funcion", "gascylinder/gascylinder.service.ts"),
  ("OrderService", "delivered"): ("local", "order/order.service.ts"),
  ("OrderRepositoryPort", "scoped"): ("adaptador", "OrderTypeormRepository"),
  ("AdminService", "isUUID"): ("biblioteca", "class-validator"),
  # Consumo declarado y recompra: CustomersService es dueño de los campos (D8)
  **_propuestas("CustomersService", "CU-143 a CU-146: validar el rango, persistir el consumo y la estimación, y buscar por ventana",
                "aKilosPorMes", "configurarAviso", "findByEstimateWindow", "guardarConsumo", "guardarEstimacion"),
  **_propuestas("CylinderLifecyclePort", "CU-108: el recupero lee quién retiene cada envase y su último movimiento",
                "findHeldByCustomer", "findLastMovement"),
  **_propuestas("CylinderService", "CU-132 a CU-135: vigencia de los envases",
                "consultarVigencia", "diasHastaElVencimiento", "proximosAVencer", "registrarRevision"),
  **_propuestas("NotificationsService", "CU-105 a CU-108: avisos de los módulos inteligentes",
                "escalateToAdmin", "sendBatchOffer", "sendRecoveryStep",
                "sendRepurchaseInvitation", "sendWindowProposal"),
  **_propuestas("OrderRepositoryPort", "CU-106, CU-107, CU-108, CU-144, CU-146: consultas que necesitan los módulos",
                "assignBatch", "findDeliveredHistory", "findNextScheduledDelivery", "findScheduled",
                "hasActiveOrder"),
  **_propuestas("OrderService", "CU-127, CU-128, CU-147, CU-148: dirección, quién recibe y modalidad",
                "cambiarDireccion", "compraExpress", "direccionPredeterminada",
                "indicarQuienRecibe", "modalidadesDisponibles", "verificarCobertura",
                "verificarCoberturaExpress"),
  **_propuestas("GasCylinderService", "CU-268, CU-269: reactivar un producto y listar los dados de baja", "findInactive", "reactivate"),
  **_propuestas("ClaimsService", "CU-174, CU-175: la fotografía del reclamo", "assertEsDelCliente", "attachPhoto", "getPhoto"),
  **_propuestas("PaymentsService", "CU-168: reintegro de un pago aprobado", "findApprovedByOrder", "markRefunded"),
  **_propuestas("PaymentGatewayPort", "CU-168: devolución por la pasarela; MercadoPago la implementa y otra pasarela agrega un adaptador", "refundPayment"),
  **_propuestas("RealtimeDispatchPort", "CU-127: aviso al chofer del cambio de dirección", "notifyDriverOrderAddressChanged"),
}

def metodos_de(clase):
    return metodos_por_clase.get(clase, set()) | codigo_clases.get(clase, {}).get("metodos", set())

def existe_clase(clase):
    return clase in manifest or clase in codigo_clases

referencias = collections.defaultdict(set)   # clase -> {operaciones}
origen_de = collections.defaultdict(set)      # (clase, operacion) -> {archivos}
clases_en_dsd = set()

# Los DSD en estilo Larman se cruzan más abajo, contra su tabla de implementación.
archivos = sorted(f for f in glob.glob(DSD_DIR + "DSD_*.mmd")
                  if not dsd_larman.es_larman(open(f, encoding="utf-8").read()))
for ruta in archivos:
    alias, src = alias_de(ruta)
    for m in MENSAJE.finditer(src):
        origen, _flecha, destino, texto = m.groups()
        clase = alias.get(destino, destino)
        if clase in EXCLUIR or clase.startswith(EXCLUIR_PREFIJOS):
            continue
        clases_en_dsd.add(clase)
        om = OPERACION.match(texto.strip())
        if not om:
            continue
        op = om.group(1)
        # Palabras que no son metodos de una clase de diseno (verbos de HTTP,
        # eventos de dominio en el texto del mensaje).
        if op in ("POST", "GET", "PUT", "PATCH", "DELETE", "if", "for", "while"):
            continue
        referencias[clase].add(op)
        origen_de[(clase, op)].add(os.path.basename(ruta))

faltan = []              # (clase, op) sin justificar
clases_faltantes = []    # clases sin justificar
justificadas = collections.defaultdict(list)   # tipo -> [(clase, op o None, donde)]
obsoletas = []           # excepciones que dejaron de ser ciertas
coinciden = 0
ops_en_clases_justificadas = 0

def justificar(tipo, clase, op, donde):
    justificadas[tipo].append((clase, op, donde))

for clase in sorted(clases_en_dsd):
    ops = sorted(referencias.get(clase, ()))
    if clase in PROPUESTAS_CLASE:
        if existe_clase(clase):
            obsoletas.append(f"{clase}: figura como propuesta pero ya existe en el código")
        justificar("propuesta", clase, None, PROPUESTAS_CLASE[clase])
        ops_en_clases_justificadas += len(ops)
        continue
    if clase in MODULOS:
        _t, archivo = MODULOS[clase]
        if archivo not in codigo_texto:
            obsoletas.append(f"{clase}: no existe {archivo}")
        for op in ops:
            if op != clase and not existe_funcion(op, archivo):
                faltan.append((clase, op))
        justificar("modulo", clase, None, archivo)
        ops_en_clases_justificadas += len(ops)
        continue
    if clase in ABSTRACCIONES:
        for op in ops:
            for real in ABSTRACCIONES[clase]:
                if op not in metodos_de(real):
                    faltan.append((real, op))
        justificar("abstraccion", clase, None, ", ".join(ABSTRACCIONES[clase]))
        ops_en_clases_justificadas += len(ops)
        continue
    if not existe_clase(clase):
        clases_faltantes.append(clase)
        continue
    for op in ops:
        if op in metodos_de(clase):
            coinciden += 1
            continue
        exc = EXCEPCIONES_OP.get((clase, op))
        if not exc:
            faltan.append((clase, op))
            continue
        tipo, donde = exc
        if tipo in ("funcion",) and not existe_funcion(op, donde):
            obsoletas.append(f"{clase}.{op}: ya no es una función de {donde}")
        elif tipo == "local" and not re.search(r'\bconst\s+' + op + r'\b', codigo_texto.get(donde, "")):
            obsoletas.append(f"{clase}.{op}: no hay una función local con ese nombre en {donde}")
        elif tipo == "adaptador" and op not in codigo_clases.get(donde, {}).get("metodos", set()):
            obsoletas.append(f"{clase}.{op}: no es un método de {donde}")
        elif tipo == "propuesta" and (op in metodos_de(clase)):
            obsoletas.append(f"{clase}.{op}: figura como propuesta pero ya existe")
        justificar(tipo, clase, op, donde)

total_pares = sum(len(v) for v in referencias.values())
n_just_op = sum(1 for t, v in justificadas.items() for (c, o, d) in v if o)
print(f"DSD analizados: {len(archivos)}")
print(f"Clases referenciadas en DSD: {len(clases_en_dsd)} · con operación reconocible: {len(referencias)}")
print(f"Pares clase.operación referenciados: {total_pares}")
print(f"  coinciden con un método real: {coinciden}")
print(f"  justificados por la excepción de la operación: {n_just_op}")
print(f"  justificados por la excepción de su clase (propuesta, módulo o abstracción): {ops_en_clases_justificadas}")
for tipo in ("propuesta", "modulo", "abstraccion", "funcion", "local", "adaptador", "biblioteca"):
    items = justificadas.get(tipo, [])
    if items:
        n_cl = sum(1 for (c, o, d) in items if not o)
        n_op = sum(1 for (c, o, d) in items if o)
        print(f"    {tipo}: {n_cl} clases, {n_op} operaciones")
print(f"Clases referenciadas sin justificar: {len(clases_faltantes)}")
for c in clases_faltantes:
    print(f"  ✗ clase {c}")
print(f"Operaciones sin justificar: {len(faltan)}")
for c, op in faltan:
    archivos_de = sorted(origen_de[(c, op)])[:3]
    print(f"  ✗ {c}.{op}()  —  {', '.join(archivos_de)}")
print(f"Excepciones que ya no son ciertas: {len(obsoletas)}")
for o in obsoletas:
    print(f"  ✗ {o}")


# ---------------------------------------------------------------- DSD en estilo Larman
# El cruce pasa a ser DSD <-> clases de diseño (las que salen de los propios DSD) <-> código.
# Cada mensaje `:Clase` -> `operacion()` tiene que cumplir una de dos: la clase del código tiene
# un método con ese nombre, o la tabla «Operación de diseño | Implementación» que sigue al
# diagrama en Casos-de-Uso.md dice con qué código se implementa. Cada símbolo que cita la tabla
# (`Clase.metodo`, `Clase.atributo` o `funcion()`) se verifica contra `src/`. Un caso
# planificado no tiene tabla: sus clases todavía no existen.
def cruce_larman():
    errores, dc = [], collections.defaultdict(set)
    codigo = dsd_larman.clases_del_codigo()
    funciones = dsd_larman.funciones_del_codigo()
    dominio = set(dsd_larman.mc().CLASES)
    planificados = dsd_larman.casos_planificados()
    casos = open(D + "Casos-de-Uso.md", encoding="utf-8").read()
    n = 0
    for ruta in sorted(glob.glob(DSD_DIR + "DSD_*.mmd")):
        src = open(ruta, encoding="utf-8").read()
        if not dsd_larman.es_larman(src):
            continue
        n += 1
        d = dsd_larman.leer(ruta)
        base = d["base"]
        cus = re.findall(r'CU-\d{3}', base)
        d["mensajes"] = [m for m in d["mensajes"] if not dsd_larman.es_retorno(m)]
        for m in d["mensajes"]:
            c = dsd_larman.clase_destino(d, m["a"])
            if c:
                dc[c].add(dsd_larman.operacion(m["texto"]))
        if all(cu in planificados for cu in cus):
            continue
        tabla = dsd_larman.tabla_de_implementacion(casos, src) or {}
        usadas = set()
        for m in d["mensajes"]:
            c = dsd_larman.clase_destino(d, m["a"])
            op = dsd_larman.operacion(m["texto"])
            if c is None or op is None:
                continue
            clave = (c, op)
            if clave in tabla:
                usadas.add(clave)
                continue
            if c in codigo and op in codigo[c]:
                continue
            errores.append(f"{base}: {c}.{op} no es un método del código y la tabla de implementación no lo dice")
        for clave in tabla:
            if clave not in usadas and not any(
                    (dsd_larman.clase_destino(d, m["a"]), dsd_larman.operacion(m["texto"])) == clave
                    for m in d["mensajes"]):
                errores.append(f"{base}: la tabla trae {clave[0]}.{clave[1]}, que no es un mensaje del diagrama")
        manifest_attrs = {k: {a["nombre"] for a in v.get("atributos", [])} | {r["campo"] for r in v.get("relaciones", [])}
                          for k, v in manifest.items()}
        for clave, celda in tabla.items():
            for tok in re.findall(r'`([^`]+)`', celda):
                if "." in tok and re.fullmatch(r'[A-Z]\w*\.\w+(?:\(\))?', tok):
                    cl, mt = tok.split(".")
                    mt = mt.replace("()", "")
                    if cl in dsd_larman.EXTERNAS:
                        continue
                    if mt not in codigo.get(cl, set()) and mt not in manifest_attrs.get(cl, set()):
                        errores.append(f"{base}: la tabla cita `{tok}` y no existe en el código")
                elif re.fullmatch(r'[a-z]\w*\(\)', tok):
                    if tok[:-2] not in funciones:
                        errores.append(f"{base}: la tabla cita `{tok}` y no existe en el código")
    return n, dc, errores

n_larman, dc_diseno, errores_larman = cruce_larman()
print(f"DSD en estilo Larman cruzados: {n_larman} · clases de diseño derivadas: {len(dc_diseno)} "
      f"({sum(1 for c in dc_diseno if c in dsd_larman.mc().CLASES)} del modelo conceptual) · "
      f"operaciones: {sum(len(v) for v in dc_diseno.values())}")
print(f"Diferencias en los DSD Larman: {len(errores_larman)}")
for e in errores_larman:
    print("  ✗", e)

if os.environ.get("CRUZAR_JSON"):
    json.dump({"clases_faltantes": clases_faltantes,
              "operaciones_faltantes": [{"clase": c, "operacion": op,
                                         "archivos": sorted(origen_de[(c, op)])}
                                        for c, op in faltan]},
             open(D + "material-de-trabajo/cruce-dsd-clases.json", "w", encoding="utf-8"),
             ensure_ascii=False, indent=1)

sys.exit(1 if (faltan or clases_faltantes or obsoletas or errores_larman) else 0)
