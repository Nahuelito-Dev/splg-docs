"""Diagrama de clases de diseño derivado de los DSD (Larman, «UML y patrones», caps. 16 y 17).

Lo usan `generar-clases-diseno.py` (que dibuja) y `verificar-conformidad.py` (que comprueba
que lo dibujado sigue siendo lo que dicen los DSD). Acá está todo lo que *decide* algo:

  - cada mensaje que recibe un objeto en un DSD es una operación de su clase;
  - la visibilidad entre dos objetos da la relación: atributo (asociación navegable) o
    parámetro y variable local (dependencia);
  - los atributos de las clases de dominio salen del modelo conceptual, con el tipo del
    código;
  - los controladores, las fabricaciones puras y los puertos se reconocen por el papel que
    cumplen en los diagramas.

No se edita ningún dato a mano en los diagramas: si un DSD cambia, se vuelve a generar.
"""
import collections, glob, os, re, sys, unicodedata

import dsd_larman as L

D = L.D
sys.path.insert(0, D)
import modelo_conceptual as M

# =============================================================================== vocabulario
# Tipos primitivos: son los del catálogo de operaciones del Documento 2 (operaciones-sistema.json).
PRIMITIVOS = {
    "Cadena": "texto",
    "Identificador": "identificador único de un objeto (UUID)",
    "Entero": "número sin decimales",
    "Decimal": "número con decimales",
    "Moneda": "importe en pesos",
    "Booleano": "verdadero o falso",
    "Fecha": "día calendario",
    "Hora": "hora del día",
    "FechaHora": "instante: día y hora",
    "Coordenada": "punto geográfico (latitud y longitud)",
    "Poligono": "área geográfica cerrada",
    "Archivo": "contenido binario con su tipo",
    "Registro": "conjunto de campos con nombre",
}
CAT_A_PRIM = {"cadena": "Cadena", "identificador": "Identificador", "entero": "Entero",
              "decimal": "Decimal", "moneda": "Moneda", "booleano": "Booleano", "fecha": "Fecha",
              "hora": "Hora", "fechaHora": "FechaHora", "coordenada": "Coordenada",
              "poligono": "Poligono", "archivo": "Archivo", "registro": "Registro", "lista": "Lista"}

# Enumeraciones: el nombre en castellano del tipo y la enumeración del código que lo respalda.
ENUMERACIONES = {
    "OrderStatus": "EstadoPedido", "PaymentMethod": "MetodoDePago", "PaymentType": "TipoDePago",
    "PaymentStatus": "EstadoDelPago", "OrderDeliveryMode": "ModalidadDeEntrega",
    "ProposalStatus": "EstadoDePropuesta", "CylinderState": "EstadoDelEnvase",
    "CylinderInspectionResult": "ResultadoDeRevision", "RecoveryCaseStatus": "EstadoDelCasoDeRecupero",
    "RecoveryNoticeKind": "TipoDeAviso", "CoverageZoneSurchargeType": "TipoDeRecargo",
    "AuditResult": "ResultadoDeAuditoria", "FleetStatus": "EstadoEnLaFlota",
    "ClaimStatus": "EstadoDelReclamo", "DistributorStatus": "EstadoDeDistribuidora",
    "ConfigurableProcess": "ProcesoConfigurable", "MaintenanceTrigger": "DisparoDeMantenimiento",
    "MaintenanceCriticality": "Criticidad", "MaintenanceTaskStatus": "EstadoDeLaTarea",
    "MaintenanceSubject": "SujetoDeMantenimiento", "IncidentType": "TipoDeIncidencia",
    "IncidentStatus": "EstadoDeIncidencia", "IncidentMoment": "MomentoDeIncidencia",
    "RouteBatchStatus": "EstadoDelLote", "PrecisionDeGeocodificacion": "PrecisionDeGeocodificacion",
    "RoleType": "TipoDeRol", "PaymentGateway": "Pasarela", "LedgerPaymentStatus": "EstadoDelCobroEnPasarela", "RaterRole": "RolDelCalificador",
    # Flota ampliada (C-18): enumeraciones planificadas
    "FuelType": "TipoDeCombustible", "FuelPaymentMethod": "MedioDePagoDeCombustible",
    "TrafficFineStatus": "EstadoDeLaMulta", "VehicleAccidentStatus": "EstadoDelSiniestro",
    "TireStatus": "EstadoDelNeumatico", "TireEventType": "TipoDeMovimientoDeNeumatico",
    "RefundKind": "TipoDeReintegro", "RefundStatus": "EstadoDelReintegro",
}

# Atributos del modelo conceptual que el código no tiene como columna propia o que el modelo
# nombra distinto: (concepto, atributo) -> tipo.
TIPO_ATRIBUTO_SIN_COLUMNA = {
    ("Cliente", "consumo mensual declarado"): "Decimal",
    ("Cliente", "días de aviso"): "Entero",
    ("Distribuidora", "razón social"): "Cadena",
    ("Chofer", "/calificación"): "Decimal",
    ("Envase", "/vencimiento"): "Fecha",
    ("Pedido", "/total"): "Moneda",
    ("LoteRecorrido", "/peso total"): "Decimal",
    ("ItemSugerido", "cantidad"): "Entero",
    ("UbicacionGPS", "latitud"): "Decimal",
    ("UbicacionGPS", "longitud"): "Decimal",
    ("PropuestaConVigencia", "estado"): "EstadoDePropuesta",
    ("PropuestaConVigencia", "vence"): "FechaHora",
    ("DireccionEntrega", "punto"): "Coordenada",
    ("DireccionEntrega", "precisión"): "PrecisionDeGeocodificacion",
    ("Pedido", "modalidad de entrega"): "ModalidadDeEntrega",
    # Stock y compras (planificado, C-09): conceptos sin entidad en el código
    ("Deposito", "nombre"): "Cadena",
    ("Deposito", "código"): "Cadena",
    ("Deposito", "tipo"): "Cadena",
    ("Deposito", "dirección"): "Cadena",
    ("Deposito", "predeterminado"): "Booleano",
    ("Deposito", "activo"): "Booleano",
    ("UbicacionDeStock", "tipo"): "Cadena",
    ("SaldoDeStock", "condición"): "Cadena",
    ("SaldoDeStock", "cantidad"): "Entero",
    ("MovimientoDeStock", "cantidad"): "Entero",
    ("MovimientoDeStock", "condición de origen"): "Cadena",
    ("MovimientoDeStock", "condición de destino"): "Cadena",
    ("MovimientoDeStock", "motivo"): "Cadena",
    ("MovimientoDeStock", "fecha"): "FechaHora",
    ("UmbralDeStock", "mínimo de llenas"): "Entero",
    ("UmbralDeStock", "avisado el"): "FechaHora",
    ("AjusteDeStock", "número"): "Entero",
    ("AjusteDeStock", "motivo"): "Cadena",
    ("AjusteDeStock", "nota"): "Cadena",
    ("AjusteDeStock", "fecha"): "FechaHora",
    ("ItemAjusteDeStock", "condición"): "Cadena",
    ("ItemAjusteDeStock", "diferencia"): "Entero",
    ("CargaDeCamion", "número"): "Entero",
    ("CargaDeCamion", "día"): "Fecha",
    ("CargaDeCamion", "estado"): "Cadena",
    ("CargaDeCamion", "abierta el"): "FechaHora",
    ("CargaDeCamion", "salió el"): "FechaHora",
    ("CargaDeCamion", "regresó el"): "FechaHora",
    ("CargaDeCamion", "cerrada el"): "FechaHora",
    ("CargaDeCamion", "nota de diferencia"): "Cadena",
    ("CargaDeCamion", "motivo de cancelación"): "Cadena",
    ("CargaDeCamion", "notas"): "Cadena",
    ("ItemCarga", "llenas cargadas"): "Entero",
    ("ItemCarga", "llenas repuestas"): "Entero",
    ("ItemCarga", "vacías cargadas"): "Entero",
    ("ItemCarga", "llenas declaradas al regreso"): "Entero",
    ("ItemCarga", "vacías declaradas al regreso"): "Entero",
    ("ItemCarga", "llenas entregadas"): "Entero",
    ("ItemCarga", "vacías recolectadas"): "Entero",
    ("ItemCarga", "/llenas esperadas"): "Entero",
    ("ItemCarga", "/vacías esperadas"): "Entero",
    ("ItemCarga", "diferencia de llenas"): "Entero",
    ("ItemCarga", "diferencia de vacías"): "Entero",
    ("Proveedor", "razón social"): "Cadena",
    ("Proveedor", "CUIT"): "Cadena",
    ("Proveedor", "tipo"): "Cadena",
    ("Proveedor", "contacto"): "Cadena",
    ("Proveedor", "teléfono"): "Cadena",
    ("Proveedor", "correo"): "Cadena",
    ("Proveedor", "dirección"): "Cadena",
    ("Proveedor", "plazo de pago"): "Entero",
    ("Proveedor", "activo"): "Booleano",
    ("OrdenDeCompra", "número"): "Entero",
    ("OrdenDeCompra", "estado"): "Cadena",
    ("OrdenDeCompra", "emitida el"): "FechaHora",
    ("OrdenDeCompra", "fecha esperada"): "Fecha",
    ("OrdenDeCompra", "total"): "Moneda",
    ("OrdenDeCompra", "motivo de cancelación"): "Cadena",
    ("OrdenDeCompra", "notas"): "Cadena",
    ("ItemOrdenDeCompra", "cantidad"): "Entero",
    ("ItemOrdenDeCompra", "costo unitario"): "Moneda",
    ("ItemOrdenDeCompra", "vacíos a canjear"): "Entero",
    ("ItemOrdenDeCompra", "cantidad recibida"): "Entero",
    ("RecepcionDeCompra", "número"): "Entero",
    ("RecepcionDeCompra", "tipo de comprobante"): "Cadena",
    ("RecepcionDeCompra", "número de comprobante"): "Cadena",
    ("RecepcionDeCompra", "recibida el"): "FechaHora",
    ("RecepcionDeCompra", "total"): "Moneda",
    ("RecepcionDeCompra", "estado de pago"): "Cadena",
    ("RecepcionDeCompra", "estado"): "Cadena",
    ("RecepcionDeCompra", "motivo de anulación"): "Cadena",
    ("ItemRecepcion", "llenas recibidas"): "Entero",
    ("ItemRecepcion", "vacías entregadas"): "Entero",
    ("ItemRecepcion", "costo unitario"): "Moneda",
    ("Producto", "costo promedio"): "Moneda",
    ("Caja", "nombre"): "Cadena",
    ("Empleado", "nombre"): "Cadena",
    ("Caja", "tipo"): "TipoDeCaja",
    ("Caja", "saldo"): "Moneda",
    ("Caja", "requiere sesión"): "Booleano",
    ("Caja", "activa"): "Booleano",
    ("SesionDeCaja", "estado"): "EstadoDeLaSesion",
    ("SesionDeCaja", "abierta el"): "FechaHora",
    ("SesionDeCaja", "monto inicial"): "Moneda",
    ("SesionDeCaja", "cerrada el"): "FechaHora",
    ("SesionDeCaja", "/monto esperado"): "Moneda",
    ("SesionDeCaja", "monto contado"): "Moneda",
    ("SesionDeCaja", "/diferencia"): "Moneda",
    ("SesionDeCaja", "observaciones"): "Cadena",
    ("CategoriaDeCaja", "nombre"): "Cadena",
    ("CategoriaDeCaja", "sentido"): "SentidoDeCaja",
    ("CategoriaDeCaja", "código de sistema"): "CodigoDeSistema",
    ("CategoriaDeCaja", "activa"): "Booleano",
    ("MovimientoDeCaja", "sentido"): "SentidoDeCaja",
    ("MovimientoDeCaja", "importe"): "Moneda",
    ("MovimientoDeCaja", "medio"): "MedioDeCaja",
    ("MovimientoDeCaja", "fecha"): "FechaHora",
    ("MovimientoDeCaja", "descripción"): "Cadena",
    ("MovimientoDeCaja", "origen"): "OrigenDelMovimiento",
    ("RendicionChofer", "número"): "Entero",
    ("RendicionChofer", "fecha de negocio"): "Fecha",
    ("RendicionChofer", "estado"): "EstadoDeLaRendicion",
    ("RendicionChofer", "efectivo esperado"): "Moneda",
    ("RendicionChofer", "efectivo declarado"): "Moneda",
    ("RendicionChofer", "/gastos del chofer"): "Moneda",
    ("RendicionChofer", "/diferencia"): "Moneda",
    ("RendicionChofer", "resolución de la diferencia"): "ResolucionDeDiferencia",
    ("RendicionChofer", "presentada el"): "FechaHora",
    ("RendicionChofer", "aprobada el"): "FechaHora",
    ("RendicionChofer", "observaciones"): "Cadena",
    ("RendicionChofer", "aviso enviado el"): "FechaHora",
    ("PedidoRendido", "importe"): "Moneda",
    ("CobroDeRendicion", "importe"): "Moneda",
    ("ReintegroDePago", "tipo"): "TipoDeReintegro", ("ReintegroDePago", "estado"): "EstadoDelReintegro",
    ("ReintegroDePago", "importe"): "Moneda", ("ReintegroDePago", "intentos"): "Entero",
    ("ReintegroDePago", "devuelto antes del intento"): "Moneda",
    ("PedidoRendido", "medio de pago"): "MetodoDePago",
    ("GastoDeRendicion", "importe"): "Moneda",
    ("GastoDeRendicion", "descripción"): "Cadena",
    ("CuentaCorriente", "razón social"): "Cadena",
    ("CuentaCorriente", "CUIT"): "Cadena",
    ("CuentaCorriente", "condición fiscal"): "CondicionFiscal",
    ("CuentaCorriente", "límite de crédito"): "Moneda",
    ("CuentaCorriente", "plazo de pago en días"): "Entero",
    ("CuentaCorriente", "estado"): "EstadoDeLaCuenta",
    ("CuentaCorriente", "saldo"): "Moneda",
    ("AsientoCuentaCorriente", "tipo"): "TipoDeAsiento",
    ("AsientoCuentaCorriente", "importe"): "Moneda",
    ("AsientoCuentaCorriente", "vence"): "Fecha",
    ("AsientoCuentaCorriente", "medio de pago"): "MedioDeCaja",
    ("AsientoCuentaCorriente", "fecha"): "FechaHora",
    ("AsientoCuentaCorriente", "descripción"): "Cadena",
    ("ImputacionCuentaCorriente", "importe"): "Moneda",
    ("ReglaComision", "base"): "BaseDeComision",
    ("ReglaComision", "valor"): "Decimal",
    ("ReglaComision", "vigente desde"): "Fecha",
    ("ReglaComision", "vigente hasta"): "Fecha",
    ("ReglaComision", "activa"): "Booleano",
    ("AsientoComision", "tipo"): "TipoDeAsientoDeComision",
    ("AsientoComision", "importe"): "Moneda",
    ("AsientoComision", "fecha"): "FechaHora",
    ("AsientoComision", "descripción"): "Cadena",
    ("LiquidacionComisiones", "número"): "Entero",
    ("LiquidacionComisiones", "período desde"): "Fecha",
    ("LiquidacionComisiones", "período hasta"): "Fecha",
    ("LiquidacionComisiones", "bruto"): "Moneda",
    ("LiquidacionComisiones", "deducciones"): "Moneda",
    ("LiquidacionComisiones", "neto"): "Moneda",
    ("LiquidacionComisiones", "estado"): "EstadoDeLaLiquidacion",
    ("LiquidacionComisiones", "aprobada el"): "FechaHora",
    ("LiquidacionComisiones", "pagada el"): "FechaHora",
}
# Los atributos de los conceptos planificados no tienen todavía una columna en el código.
TIPO_ATRIBUTO_SIN_COLUMNA.update(getattr(M, "TIPOS_PLANIFICADOS", {}))
MONEDA = {"precio", "importe", "seña", "recargo", "costo", "depósito", "monto del depósito", "depósito comprometido",
          "precio unitario", "descuento_", "/subtotal"}

# =============================================================================== utilidades
def sin_acentos(t):
    t = t.replace("ñ", "ni").replace("Ñ", "Ni")
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def camel(t):
    """«calle y altura» -> calleYAltura; «número de serie» -> numeroDeSerie."""
    t = sin_acentos(t).lstrip("/")
    if t.isupper():
        t = t.lower()
    partes = re.split(r'[^A-Za-z0-9]+', t.strip())
    partes = [p for p in partes if p]
    if not partes:
        return t
    return partes[0][0].lower() + partes[0][1:] + "".join(p[0].upper() + p[1:] for p in partes[1:])


def minuscula(clase):
    return clase[0].lower() + clase[1:]


def snake_a_camel(s):
    p = s.split("_")
    return p[0] + "".join(x[:1].upper() + x[1:] for x in p[1:])


# =============================================================================== el código
_MAN = None
def manifiesto():
    global _MAN
    if _MAN is None:
        _MAN = L.manifiesto()
    return _MAN


def _archivos_del_codigo():
    """clase -> módulo, de todo `src/` (incluye lo que el manifiesto no extrae, como los cron)."""
    r = {}
    clase = re.compile(r'^(?:export\s+)?(?:default\s+)?(?:abstract\s+)?class\s+(\w+)', re.M)
    for ruta in glob.glob(L.BACK + "**/*.ts", recursive=True):
        if ruta.endswith(".spec.ts"):
            continue
        rel = os.path.relpath(ruta, L.BACK)
        txt = open(ruta, encoding="utf-8").read()
        for m in clase.finditer(txt):
            r.setdefault(m.group(1), rel)
    return r


_ARCH = None
def archivo_de(clase):
    global _ARCH
    if _ARCH is None:
        _ARCH = _archivos_del_codigo()
    return _ARCH.get(clase)


# Módulo de las clases que todavía no existen en el código (las planificadas del Documento 3) y de
# las que vienen de una biblioteca. Para las demás, el módulo es la carpeta de `src/` que las define.
MODULO_PLANIFICADA = {
    "CartService": "cart", "CartController": "cart",
    "ConsumptionService": "repurchase", "ConsumptionEstimatorService": "repurchase",
    "RepurchaseController": "repurchase", "RepurchaseEstimatesService": "repurchase",
    "RepurchaseForecastService": "repurchase",
    "CylinderRecoveryService": "cylinder", "DepositLedgerService": "cylinder",
    "DemandForecastService": "fleet", "FleetCoverageService": "fleet",
    "FleetMaintenancePlannerService": "fleet", "FleetAvailabilityPort": "fleet",
    "ProcessConfigService": "distributor",
    "RouteBatchPlannerService": "order",
    "RouteSequencerService": "order",
    "RefundPaymentUseCase": "payments", "ReintegroListener": "payments",
    "JobPositionService": "employee", "EmployeeService": "employee", "TerminateEmployeeUseCase": "employee",
    "GrantEmployeeAccountUseCase": "employee", "AttendanceService": "employee", "LeaveService": "employee",
    "PersonnelDashboardService": "employee", "AttachmentsService": "attachment",
    "CuilValidator": "employee",
    "CoverageZoneExpiryCron": "coverage-zone", "RefundsService": "payments",
    "HealthCheckService": "health",
    "FuelLoadService": "fleet-expense",
    "TrafficFineService": "fleet-expense", "FineDueAlertsCron": "fleet-expense",
    "VehicleAccidentService": "fleet-expense", "TireService": "fleet-expense",
    "FleetCostService": "fleet-expense",
    "WarehouseService": "stock", "StockService": "stock", "StockLedgerService": "stock",
    "StockAdjustmentService": "stock", "StockLowCron": "stock", "StockDeliveryListener": "stock",
    "StockReconciliationCron": "stock", "StockReconciliationService": "stock",
    "SupplierService": "purchase", "PurchaseOrderService": "purchase",
    "PurchaseReceiptService": "purchase", "TruckLoadService": "truck-load",
    "CashBoxService": "cash", "CashLedgerService": "cash", "CashCategoryService": "cash",
    "FinanceService": "finance",
    "DriverSettlementService": "driver-settlement", "DriverSettlementCron": "driver-settlement",
    "CustomerAccountService": "customer-account", "CommissionRuleService": "commission",
    "CommissionLedgerService": "commission", "DriverLiquidationService": "commission",
    "CommissionQueryService": "commission",
}


def modulo_de_clase(clase):
    if clase in MODULO_PLANIFICADA:
        return MODULO_PLANIFICADA[clase]
    m = manifiesto().get(clase)
    if m:
        return m["file"].split("/")[0]
    f = archivo_de(clase)
    if f:
        return f.split("/")[0]
    return None


def adaptadores_del_codigo():
    """puerto -> [adaptadores] según `class X extends YPort` de `src/`."""
    r = collections.defaultdict(list)
    pat = re.compile(r'^export\s+class\s+(\w+)\s+extends\s+(\w+Port)\b', re.M)
    for ruta in glob.glob(L.BACK + "**/*.ts", recursive=True):
        if ruta.endswith(".spec.ts"):
            continue
        for m in pat.finditer(open(ruta, encoding="utf-8").read()):
            r[m.group(2)].append(m.group(1))
    return r


# =============================================================================== tipos
def tipo_ts(ts, nombre_col="", nulo=False):
    """Tipo de un atributo de entidad TypeORM -> tipo del diseño."""
    t = re.sub(r'\s*\|\s*null', '', ts).strip()
    if t in ENUMERACIONES:
        return ENUMERACIONES[t]
    return {"string": "Cadena", "number": "Decimal", "boolean": "Booleano", "Date": "FechaHora",
            "Point": "Coordenada", "PoligonoGeoJson": "Poligono"}.get(t, "Registro")


def tipo_de_atributo(concepto, atributo):
    """Tipo de un atributo del modelo conceptual: del código si hay columna, del glosario si no."""
    if (concepto, atributo) in TIPO_ATRIBUTO_SIN_COLUMNA:
        return TIPO_ATRIBUTO_SIN_COLUMNA[(concepto, atributo)]
    col = M.ATRIBUTOS.get(concepto, {}).get(atributo)
    if col is None and concepto in ("OfertaDespacho", "OfertaLote", "PropuestaVentanaTaller",
                                    "InvitacionRecompra", "AvisoRecupero"):
        col = M.HEREDA_ATRIBUTOS.get(atributo)
    tabla = M.TABLA.get(concepto)
    ent = next((v for v in manifiesto().values() if v["kind"] == "entity" and v.get("tabla") == tabla), None) if tabla else None
    if ent and col:
        a = next((x for x in ent["atributos"] if x["nombre"] == snake_a_camel(col)), None)
        if a:
            t = tipo_ts(a["tipo"], col, a["nulo"])
            n = camel(atributo)
            if t == "Decimal":
                if atributo in MONEDA or "precio" in atributo or "costo" in atributo:
                    return "Moneda"
                if re.search(r'quantity|stock|capacity|sequence|orders|km|stars|step|days|interval|lead', col):
                    return "Entero"
                return "Decimal"
            if t == "Cadena":
                if "fecha" in atributo and col.endswith(("date", "_at")) or atributo in ("día",):
                    return "Fecha"
                if re.search(r'(^|_)(start|end)Time$|^(start|end)Time$', col):
                    return "Hora"
                if col in ("startTime", "endTime"):
                    return "Hora"
                if atributo in ("día",):
                    return "Fecha"
            return t
    t = _tipo_planificado(concepto, atributo)
    if t:
        return t
    raise KeyError(f"sin tipo para {concepto}.{atributo}")


# Tipos de las columnas planificadas (módulo Personal, C-08): salen de `propuesto_personal.py`.
ENUM_PLANIFICADO = {
    "job_position_category_enum": "CategoriaDePuesto", "employee_status_enum": "EstadoDelEmpleado",
    "employee_termination_reason_enum": "MotivoDeEgreso", "employment_type_enum": "ModalidadDeContratacion",
    "attendance_source_enum": "OrigenDeLaJornada", "employee_leave_type_enum": "TipoDeLicencia",
    "employee_leave_status_enum": "EstadoDeLaLicencia", "maintenance_document_kind_enum": "DocumentoControlado",
    "employee_document_type_enum": "TipoDeDocumento", "attachment_owner_type_enum": "TipoDeDuenio",
}


def _tipo_planificado(concepto, atributo):
    import propuesto_personal as PP
    col = M.ATRIBUTOS.get(concepto, {}).get(atributo)
    tabla = M.TABLA.get(concepto)
    for ag in PP.AGREGADOS:
        defs = [c for tb in ag["tablas"] if tb["nombre"] == tabla for c in tb["columnas"]]
        defs += ag["columnas"].get(tabla, [])
        for c in defs:
            if c["nombre"] != col:
                continue
            sql = c["tipo"]
            lista = sql.endswith("[]")
            sql = sql.rstrip("[]")
            if sql in ENUM_PLANIFICADO:
                t = ENUM_PLANIFICADO[sql]
            else:
                base = re.sub(r'\(.*\)', '', sql)
                t = {"uuid": "Identificador", "varchar": "Cadena", "text": "Cadena", "date": "Fecha",
                     "timestamptz": "FechaHora", "integer": "Entero", "boolean": "Booleano",
                     "jsonb": "Registro"}.get(base)
            return t and (t + "[*]" if lista else t)
    return None


def nombre_de_atributo(a):
    return ("/" if a.startswith("/") else "") + camel(a)


# -------------------------------------------------------------------- parámetros y retornos
# Las tablas de abajo dicen qué tipo tiene el argumento o el retorno que un DSD nombra. El
# nombre es el que escribe el DSD; el tipo sale de: (1) el catálogo de operaciones del Documento 2,
# para los parámetros del primer mensaje; (2) el modelo conceptual (una clase, un atributo); (3) este
# glosario, para lo demás.
ALIAS_CLASE = {
    "direccion": "DireccionEntrega", "direccionNueva": "DireccionEntrega",
    "direccionOrigen": "DireccionEntrega", "direcciones": "DireccionEntrega",
    "franja": "FranjaHoraria", "franjas": "FranjaHoraria", "zona": "ZonaCobertura", "zonas": "ZonaCobertura",
    "cambio": "CambioEstadoPedido",
    "adjunto": "AdjuntoTarea", "adjuntos": "AdjuntoTarea", "tarea": "TareaMantenimiento",
    "tareas": "TareaMantenimiento", "plan": "PlanMantenimiento", "ventana": "PropuestaVentanaTaller",
    "ventanas": "PropuestaVentanaTaller", "ventanaElegida": "PropuestaVentanaTaller",
    "propuesta": "PropuestaVentanaTaller", "oferta": "OfertaDespacho", "ofertas": "OfertaDespacho",
    "recorrido": "LoteRecorrido", "invitacion": "InvitacionRecompra", "recompras": "InvitacionRecompra",
    "caso": "CasoRecupero", "asignacion": "AsignacionVehiculo",
    "asignaciones": "AsignacionVehiculo", "asientos": "AsientoAuditoria", "calificacion": "Calificacion",
    "auditorias": "Auditoria", "detalles": "DetalleAuditoria",
    "calificaciones": "Calificacion", "configuracion": "ConfiguracionModulo", "ubicacion": "UbicacionGPS",
    "posicion": "UbicacionGPS", "carrito": "Carrito", "reserva": "Pedido", "reservas": "Pedido",
    "administrador": "Administrador", "administradores": "Administrador", "movimientos": "MovimientoEnvase",
    "envase": "Envase", "envases": "Envase", "usuarios": "Usuario",
    "distribuidoras": "Distribuidora", "choferes": "Chofer", "clientes": "Cliente", "reclamos": "Reclamo",
    "carga": "CargaCombustible", "cargas": "CargaCombustible", "multa": "MultaTransito",
    "multas": "MultaTransito", "siniestros": "Siniestro", "neumaticos": "Neumatico",
    "incidencias": "Incidencia", "productos": "Producto", "vehiculos": "Vehiculo", "pedidos": "Pedido",
    "pago": "Pago", "pagos": "Pago", "roles": "Rol", "rol": "Rol", "tareas": "TareaMantenimiento",
    "aviso": "AvisoRecupero", "cercanos": "Chofer", "contactados": "Chofer", "aceptados": "Chofer", "libres": "Chofer",
    "activos": "Chofer", "habilitados": "Chofer", "solicitante": "Usuario", "autor": "Usuario",
    "usuario": "Usuario", "chofer": "Chofer", "choferAnterior": "Chofer", "choferConOferta": "Chofer", "administrador": "Usuario", "cliente": "Cliente",
    "vehiculo": "Vehiculo", "producto": "Producto", "pedido": "Pedido", "reclamo": "Reclamo",
    "incidencia": "Incidencia", "distribuidora": "Distribuidora", "item": "ItemPedido", "items": "ItemPedido",
    "itemsDelCarrito": "ItemCarrito", "promociones": "Promocion",
    "adjuntoNuevo": "Adjunto",     "puesto": "PuestoDeTrabajo", "puestos": "PuestoDeTrabajo", "licencia": "LicenciaLaboral",
    "licencias": "LicenciaLaboral", "jornada": "JornadaDeTrabajo", "jornadas": "JornadaDeTrabajo",
    "empleado": "Empleado", "empleados": "Empleado", "planes": "PlanMantenimiento",
    "movimiento": "MovimientoDeCaja", "movimientoDelPago": "MovimientoDeCaja", "movimientos": "MovimientoDeCaja", "contraasiento": "MovimientoDeCaja",
    "salida": "MovimientoDeCaja", "entrada": "MovimientoDeCaja", "sesion": "SesionDeCaja",
    "origen_": "Caja", "caja": "Caja", "cajas": "Caja", "categoria": "CategoriaDeCaja",
    "rendicion": "RendicionChofer", "rendiciones": "RendicionChofer", "gasto": "GastoDeRendicion",
    "cuenta": "CuentaCorriente", "cuentas": "CuentaCorriente", "asiento": "AsientoCuentaCorriente",
    "asientosDeLaCuenta": "AsientoCuentaCorriente", "cargo": "AsientoCuentaCorriente",
    "regla": "ReglaComision", "liquidacion": "LiquidacionComisiones",
    "comisiones": "AsientoComision", "sesionDeCaja": "SesionDeCaja", "cuentaCorriente": "CuentaCorriente",
    "asientoDeComision": "AsientoComision", "asientosDeComision": "AsientoComision",
    "categoria_": "CategoriaDeCaja", "cobro": "AsientoCuentaCorriente", "cobros": "AsientoCuentaCorriente"
}
_PLURALES = {"cargas", "multas", "siniestros", "neumaticos", "cercanos", "contactados", "aceptados", "libres", "activos", "habilitados", "vencidas",
             "recompras", "direcciones", "franjas", "zonas", "cambios", "adjuntos", "tareas", "ventanas",
             "ofertas", "asignaciones", "asientos", "auditorias", "detalles", "cobros", "empleados", "asientosDeLaCuenta", "asientosDeComision", "cajas", "rendiciones", "cuentas", "comisiones", "calificaciones", "movimientos", "envases", "usuarios",
             "distribuidoras", "choferes", "clientes", "reclamos", "incidencias", "productos", "vehiculos",
             "pedidos", "pagos", "roles", "administradores", "reservas", "items", "promociones",
             "puestos", "licencias", "jornadas", "empleados", "planes"}

# nombre -> tipo, para lo que no es una clase ni un atributo del modelo.
GLOSARIO = {
    # parámetros
    "clave": "Cadena", "claveAnterior": "Cadena", "direccionExterna": "Cadena", "nombreDeDescarga": "Cadena",
    "entidad": "Cadena", "registro": "Cadena", "ip": "Cadena", "tipoDeAccion": "Entero", "contrasena": "Cadena", "correoActual": "Cadena",
    "correoNuevo": "Cadena", "correoDePrueba": "Cadena", "correoDeRecuperacion": "Cadena",
    "verificacionDeCorreo": "Registro", "destinatario": "Cadena", "ajustes": "Registro",
    "firma": "Cadena", "tipoDeNotificacion": "Cadena", "identificadorDelPago": "Identificador",
    "referenciaExterna": "Cadena", "identificadorCorto": "Cadena", "cuit": "Cadena",
    "razonSocial": "Cadena", "nombreCompleto": "Cadena", "nombre": "Cadena", "telefono": "Cadena",
    "correo": "Cadena", "color": "Cadena", "marca": "Cadena", "modelo": "Cadena", "patente": "Cadena",
    "motivo": "Cadena", "descripcion": "Cadena", "comentario": "Cadena", "observacion": "Cadena",
    "nota": "Cadena", "notaDeResolucion": "Cadena", "resolucion": "Cadena", "mensaje": "Cadena",
    "titulo": "Cadena", "token": "Cadena", "plataforma": "Cadena", "operacion": "Cadena",
    "recurso": "Cadena", "tipoDeRecurso": "Cadena", "tipoGarrafa": "Cadena", "tipoDeProducto": "Cadena",
    "decision": "Cadena", "escalon": "Entero", "proceso": "ProcesoConfigurable", "numeroDeSerie": "Cadena",
    "serie": "Cadena", "series": "Cadena", "numerosDeSerie": "Cadena", "codigo": "Cadena",
    "documento": "Cadena", "destinatarioNombre": "Cadena", "textoDeBusqueda": "Cadena", "termino": "Cadena",
    "evidencia": "Archivo", "foto": "Archivo", "imagen": "Archivo", "archivo": "Archivo", "logo": "Archivo",
    "contenido": "Archivo", "contentType": "Cadena", "tamano": "Entero", "ubicacionDescriptiva": "Cadena",
    "pagina": "Entero", "limite": "Entero", "anio": "Entero", "variacion": "Entero", "stockInicial": "Entero",
    "desplazamiento": "Entero", "dias": "Entero", "estrellas": "Entero", "capacidad": "Entero",
    "cantidad": "Entero", "kilometraje": "Entero", "kilometrajeDiario": "Entero", "peso": "Decimal",
    "cantidadPorMes": "Decimal", "latitud": "Decimal", "longitud": "Decimal", "radioKm": "Decimal",
    "radioExpressKm": "Decimal", "radiosKm": "Decimal", "plazo": "Entero", "plazoDeTolerancia": "Entero",
    "ventanaDeAceptacion": "Entero", "venceEn": "Entero", "enfriamiento": "Entero", "granularidad": "Cadena", "periodo": "Cadena",
    "monto": "Moneda", "montoDeLaSenia": "Moneda", "importe": "Moneda", "precio": "Moneda",
    "precioUnitario": "Moneda", "subtotal": "Moneda", "subtotalItems": "Moneda", "recargo": "Moneda",
    "costo": "Moneda", "gastoEstimado": "Moneda", "total": "Moneda", "saldo": "Moneda", "ajustes_": "Moneda",
    "deposito": "Moneda", "descuento": "Decimal",
    "fecha": "Fecha", "fechaAgendada": "Fecha", "fechaDesde": "Fecha", "fechaHasta": "Fecha",
    "fechaEstimada": "Fecha", "fechaDeRegistro": "Fecha", "ultimaCompra": "Fecha", "vencimiento": "Fecha",
    "ahora": "FechaHora", "inicioDelDia": "FechaHora", "hoy": "Fecha", "desde": "FechaHora", "hasta": "FechaHora", "llegada": "FechaHora",
    "vigencia": "FechaHora", "vigenteHasta": "FechaHora", "horaInicio": "Hora", "horaFin": "Hora",
    "activa": "Booleano", "activo": "Booleano", "disponible": "Booleano", "bloquear": "Booleano", "verdadero": "Booleano", "falso": "Booleano",
    "deshabilitada": "Booleano", "express": "Booleano", "esSenia": "Booleano", "predeterminada": "Booleano",
    "coordenadas": "Coordenada", "punto": "Coordenada", "origen": "Coordenada", "destino": "Coordenada",
    "poligono": "Poligono", "precision": "PrecisionDeGeocodificacion", "latLng": "Coordenada",
    "datos": "Registro", "cuenta": "Registro", "datosDelChofer": "Registro", "datosDelCliente": "Registro",
    "datosPersonales": "Registro", "detalle": "Registro", "parametros": "Registro", "intervalos": "Registro",
    "evento": "Registro", "notificacion": "Registro", "confirmacion": "Registro", "body": "Registro",
    "manager": "Registro", "conexion": "Registro", "redis": "Registro", "pagador": "Cadena",
    "metodoDePago": "MetodoDePago", "medioDePago": "MetodoDePago", "paymentMethod": "MetodoDePago",
    "estado": "Cadena", "estadoAnterior": "Cadena", "estadoNuevo": "Cadena", "estadoFinal": "Cadena",
    "estadoOrigen": "Cadena", "estadoDestino": "Cadena",
    "origenDeJornada": "OrigenDeLaJornada", "estadoNuevoDeLicencia": "EstadoDeLaLicencia",
    "tipoDeLicencia": "TipoDeLicencia", "motivoDeEgreso": "MotivoDeEgreso", "motivoDeRechazo": "Cadena",
    "saldoDeVacaciones": "Entero", "fechaDesde": "Fecha", "fechaHasta": "Fecha", "habilitado": "Booleano",
    "activo": "Booleano",
    "aprobada": "EstadoDeLaLicencia", "rechazada_": "EstadoDeLaLicencia", "cancelada": "EstadoDeLaLicencia",
    "filtros": "Registro", "confirmación": "Cadena", "confirmacion": "Cadena",
    "correspondientes": "Entero", "tomados": "Entero", "presentes": "Entero",
        "calificado": "Usuario", "despacho": "ProcesoConfigurable", "tareasProgramadas": "ProcesoConfigurable",
    "devuelto": "Booleano", "nombreDelChofer": "Cadena", "usuarioActual": "Usuario", "asignado": "Booleano",
    "pendientes": "Pedido[*]", "reservados": "Pedido[*]", "retiro": "Envase", "tokens": "Cadena[*]",
    "corren": "Distribuidora[*]", "conOfertas": "Distribuidora[*]", "conPendientes": "Distribuidora[*]",
    "generacion": "Entero", "marcaDeLaGeneracionAnterior": "Cadena", "tareaProgramada": "Cadena",
    "marcasDeUltimaEjecucion": "Registro", "bloqueado": "Booleano", "habilitado": "Booleano",
    "tipo": "Cadena", "esSena": "Booleano", "orden": "Entero", "relacion": "Cadena", "usuario_": "Usuario",
    "rolCliente": "TipoDeRol", "rolChofer": "TipoDeRol", "rolAdministradorGeneral": "TipoDeRol",
    "destinatarioDelAviso": "Cadena", "vencimientos": "Registro", "ventasDelDia": "Registro",
    "ventasPorDia": "Registro", "entregadosDelDia": "Entero", "cantidadDeItems": "Entero",
    "kilometros": "Entero", "resultado": "Cadena", "pendiente": "EstadoPedido",
    "cancelado": "EstadoPedido", "aceptado": "EstadoPedido", "enCamino": "Booleano",
    "entregado": "EstadoPedido", "enProceso": "EstadoDelReclamo", "despachado": "EstadoDelEnvase",
    "enDeposito": "EstadoDelEnvase", "gasCylinderId": "Identificador",
    # Stock y compras (C-09)
    "minimos": "Registro", "minimoDeLlenos": "Entero", "condicion": "Cadena", "items": "Registro",
    "devueltos": "Registro", "datosDeContacto": "Registro", "plazoDePago": "Entero",
    "tipoDeComprobante": "Cadena", "numeroDeComprobante": "Cadena", "estadoDePago": "Cadena",
    "vaciosACanjear": "Entero", "llenosCargados": "Entero", "vaciosCargados": "Entero",
    "llenosRepuestos": "Entero", "llenosDevueltos": "Entero", "vaciosDevueltos": "Entero",
    "llenosRecibidos": "Entero", "vaciosEntregados": "Entero", "llenosFisicos": "Entero",
    "reservado": "Entero", "faltante": "Entero", "diferencia": "Entero", "diferencias": "Registro",
    "stockBajo": "Registro", "conSaldo": "Booleano", "bajo": "Booleano", "esperado": "Entero",
    "conciliacion": "Registro", "resultado_": "Registro", "costoUnitario": "Moneda",
    "fechaEsperada": "Fecha", "codigo_": "Cadena", "ubicacionDeOrigen": "UbicacionDeStock",
    "ayudanteId": "Identificador",
    # retornos
    "cubierta": "Booleano", "firmaValida": "Booleano", "sesionValida": "Booleano", "valido": "Booleano", "hayDiferencia": "Booleano", "recibida": "Booleano", "hayStock": "Booleano",
    "existe": "Booleano", "elegible": "Booleano", "reofertable": "Booleano", "rechazada": "Booleano",
    "recibido": "Booleano", "reintegrado": "Booleano", "efectivo": "Booleano", "booked": "Booleano",
    "correoUsado": "Booleano", "telefonoUsado": "Booleano", "inhabilitado": "Booleano",
    "vigente": "Booleano", "guardado": "Booleano", "sinPagar": "Booleano", "cambios": "Registro", "mercadoPago": "Booleano",
    "enlaceDePago": "Cadena", "enlace": "Cadena", "url": "Cadena", "propio": "Booleano",
    "stream": "Archivo", "credencial": "Registro", "identidad": "Registro", "sesion": "Registro",
    "resumen": "Registro", "evolucion": "Registro", "ventas": "Registro", "ventasPorChofer": "Registro",
    "ventasPorProducto": "Registro", "ventasPorMetodoDePago": "Registro", "disponibilidad": "Registro",
    "promedio": "Decimal", "modalidades": "ModalidadDeEntrega[*]", "mediosDePago": "MetodoDePago[*]",
    "motivos": "Cadena[*]", "estadoDelPago": "EstadoDelPago", "confirmada": "Booleano",
    "sentido": "SentidoDeCaja", "medio": "MedioDeCaja", "referencia": "OrigenDelMovimiento",
    "codigoDeSistema": "CodigoDeSistema", "montoInicial": "Moneda", "montoContado": "Moneda",
    "efectivoDeclarado": "Moneda", "gastos": "GastoDeRendicion[*]", "resolucionDeDiferencia": "ResolucionDeDiferencia",
    "condicionFiscal": "CondicionFiscal", "limiteDeCredito": "Moneda", "plazoEnDias": "Entero",
    "razonSocial": "Cadena", "base": "BaseDeComision", "valor": "Decimal",
    "vigenteDesde": "Fecha", "saldoInicial": "Moneda", "antiguedad": "Registro", "tablero": "Registro",
    "vencimiento": "Fecha", "pagoDeCuenta": "AsientoCuentaCorriente", "importe_": "Moneda",
    "cajaOrigenId": "Identificador", "cajaDestinoId": "Identificador", "tipo": "Cadena",
    "tipoDeCaja": "TipoDeCaja", "tipoDeAsiento": "TipoDeAsiento", "tipoDeAsientoDeComision": "TipoDeAsientoDeComision",
    "neto": "Moneda", "saldoDeudor": "Moneda", "choferId": "Identificador", "administradores": "Administrador[*]", "movimientoId": "Identificador",
}

GLOSARIO.update({
    # Flota ampliada (C-18)
    "litros": "Decimal", "desvio": "Decimal", "consumo": "Registro", "fechaYHora": "FechaHora",
    "claveDelPlan": "Cadena", "vigenteDesde": "Fecha", "numero": "Cadena", "prestador": "Cadena",
    "claveDeActa": "Cadena", "jurisdiccion": "Cadena", "numeroDeActa": "Cadena",
    "fechaDePago": "FechaHora", "importePagado": "Moneda", "costoDeReparacion": "Moneda",
    "reintegroDelSeguro": "Moneda", "franquicia": "Moneda", "filtros": "Registro",
    "costos": "Registro", "costoDelVehiculo": "Registro", "movimientoNeumatico": "MovimientoNeumatico",
})

# El DSD a veces pasa un valor literal o un estado como argumento: se lo reemplaza por el parámetro
# que lo recibe en el diseño (nombre, tipo). Se busca por (clase, nombre) y después por nombre.
ALIAS_PARAMETRO = {
    "1": ("cantidad", "Entero"),
    # Carga del camión
    ("TruckLoadGateService", "elegibles"): ("choferes", "Chofer[*]"),
    ("StockLedgerService", "renglones"): ("renglones", "MovimientoDeStock[*]"),
    ("ItemCarga", "vaciasDeclaradas"): ("vaciasDeclaradas", "Entero"),
    # Personal: ingreso y egreso de una jornada son instantes (en Caja, los mismos nombres son el sentido del movimiento)
    ("Empleado", "ingreso"): ("ingreso", "FechaHora"), ("Empleado", "egreso"): ("egreso", "FechaHora"),
    ("JornadaDeTrabajo", "ingreso"): ("ingreso", "FechaHora"), ("JornadaDeTrabajo", "egreso"): ("egreso", "FechaHora"),
    ("CargaDeCamion", "vehiculoEnUso"): ("vehiculoEnUso", "Vehiculo"),
    ("Pedido", "pendiente"): ("estadoDestino", "EstadoPedido"),
    ("Pedido", "cancelado"): ("estadoDestino", "EstadoPedido"),
    ("Pedido", "aceptado"): ("estadoDestino", "EstadoPedido"),
    ("Pedido", "enCamino"): ("estadoDestino", "EstadoPedido"),
    ("Pedido", "entregado"): ("estadoDestino", "EstadoPedido"),
    ("Reclamo", "enProceso"): ("estadoDestino", "EstadoDelReclamo"),
    ("Reclamo", "estadoFinal"): ("estadoDestino", "EstadoDelReclamo"),
    ("Envase", "despachado"): ("estadoDestino", "EstadoDelEnvase"),
    ("Envase", "estadoDestino"): ("estadoDestino", "EstadoDelEnvase"),
    ("Envase", "enDeposito"): ("estadoDestino", "EstadoDelEnvase"),
    ("MovimientoEnvase", "enDeposito"): ("estadoDestino", "EstadoDelEnvase"),
    ("MovimientoEnvase", "estadoOrigen"): ("estadoOrigen", "EstadoDelEnvase"),
    ("MovimientoEnvase", "estadoDestino"): ("estadoDestino", "EstadoDelEnvase"),
    "medioDePago": ("metodoDePago", "MetodoDePago"),
    "direccionNueva": ("direccion", "DireccionEntrega"),
    "direccionOrigen": ("direccion", "DireccionEntrega"),
    "clienteId": ("cliente", "Cliente"),
    "usuarioId": ("usuario", "Usuario"),
    ("Distribuidora", "plan"): ("plan", "Cadena"),
    ("AsientoAuditoria", "origen"): ("origen", "Cadena"),
    ("AsientoAuditoria", "codigo"): ("codigo", "Entero"),
    ("Usuario", "cuenta"): ("cuenta", "Registro"),
    # Flota ampliada (C-18): el estado destino es del tipo enumerado de cada concepto
    ("MultaTransito", "estadoDestino"): ("estadoDestino", "EstadoDeLaMulta"),
    ("Siniestro", "estadoDestino"): ("estadoDestino", "EstadoDelSiniestro"),
    ("Neumatico", "estadoDestino"): ("estadoDestino", "EstadoDelNeumatico"),
    # Las fachadas del módulo reciben identificadores y valores tipados, no objetos
    ("CustomerAccountService", "clienteId"): ("clienteId", "Identificador"),
    ("CashBoxService", "tipo"): ("tipo", "TipoDeCaja"),
    ("CashCategoryService", "sentido"): ("sentido", "SentidoDeCaja"),
    ("CashLedgerService", "sentido"): ("sentido", "SentidoDeCaja"),
    ("CashLedgerService", "medio"): ("medio", "MedioDeCaja"),
    ("DriverSettlementService", "gastos"): ("gastos", "GastoDeRendicion[*]"),
    ("DriverSettlementService", "resolucionDeDiferencia"): ("resolucionDeDiferencia", "ResolucionDeDiferencia"),
    ("CustomerAccountService", "condicionFiscal"): ("condicionFiscal", "CondicionFiscal"),
    ("CustomerAccountService", "tipo"): ("tipo", "TipoDeAsiento"),
    ("CustomerAccountService", "medio"): ("medio", "MedioDeCaja"),
    ("CommissionRuleService", "base"): ("base", "BaseDeComision"),
}


# Stock y compras (C-09): nombres de los DSD que resuelven a una clase del módulo.
ALIAS_CLASE.update({
    "carga": "CargaDeCamion", "cargas": "CargaDeCamion", "ajuste": "AjusteDeStock", "ajustes": "AjusteDeStock",
    "depositoDeStock": "Deposito", "depositos": "Deposito", "orden": "OrdenDeCompra", "ordenes": "OrdenDeCompra",
    "proveedor": "Proveedor", "proveedores": "Proveedor", "recepcion": "RecepcionDeCompra",
    "recepciones": "RecepcionDeCompra", "saldos": "SaldoDeStock", "umbrales": "UmbralDeStock",
    "movimientosDeStock": "MovimientoDeStock", "ubicacionDeStock": "UbicacionDeStock",
    "ubicacionOrigen": "UbicacionDeStock", "ubicacionDestino": "UbicacionDeStock",
})
_PLURALES |= {"cargas", "ajustes", "depositos", "ordenes", "proveedores", "recepciones", "saldos", "umbrales",
              "movimientosDeStock"}
GLOSARIO.update({"lote": "Identificador", "llenos": "Entero", "domicilio": "Cadena"})
# Enumeraciones del módulo de stock y compras (C-09): todavía no existen en el código.
ENUMERACIONES.update({
    "StockCondition": "CondicionDeStock", "StockMovementReason": "MotivoDeMovimiento",
    "StockAdjustmentReason": "MotivoDeAjuste", "WarehouseKind": "TipoDeDeposito",
    "StockLocationKind": "TipoDeUbicacion", "SupplierKind": "TipoDeProveedor",
    "PurchaseOrderStatus": "EstadoDeLaOrden", "PurchaseDocumentType": "TipoDeComprobante",
    "PurchasePaymentStatus": "EstadoDePagoDeCompra", "PurchaseReceiptStatus": "EstadoDeLaRecepcion",
    "TruckLoadStatus": "EstadoDeLaCarga",
})
TIPO_ATRIBUTO_SIN_COLUMNA.update({
    ("Deposito", "tipo"): "TipoDeDeposito", ("UbicacionDeStock", "tipo"): "TipoDeUbicacion",
    ("SaldoDeStock", "condición"): "CondicionDeStock",
    ("MovimientoDeStock", "condición de origen"): "CondicionDeStock",
    ("MovimientoDeStock", "condición de destino"): "CondicionDeStock",
    ("MovimientoDeStock", "motivo"): "MotivoDeMovimiento", ("AjusteDeStock", "motivo"): "MotivoDeAjuste",
    ("ItemAjusteDeStock", "condición"): "CondicionDeStock", ("CargaDeCamion", "estado"): "EstadoDeLaCarga",
    ("Proveedor", "tipo"): "TipoDeProveedor", ("OrdenDeCompra", "estado"): "EstadoDeLaOrden",
    ("RecepcionDeCompra", "tipo de comprobante"): "TipoDeComprobante",
    ("RecepcionDeCompra", "estado de pago"): "EstadoDePagoDeCompra",
    ("RecepcionDeCompra", "estado"): "EstadoDeLaRecepcion",
    ("ConfiguracionModulo", "exigir carga de camión abierta"): "Booleano",
})
GLOSARIO.update({
    "condicionDeStock": "CondicionDeStock", "condicionOrigen": "CondicionDeStock",
    "condicionDestino": "CondicionDeStock", "motivoDeMovimiento": "MotivoDeMovimiento",
    "motivoDeAjuste": "MotivoDeAjuste", "tipoDeComprobante": "TipoDeComprobante",
    "estadoDeLaOrden": "EstadoDeLaOrden", "estadoDePagoDeCompra": "EstadoDePagoDeCompra",
    "controlDeStock": "ProcesoConfigurable", "exigirCargaDeCamionAbierta": "Booleano",
    "exigida": "Booleano", "aplicado": "Booleano", "descontado": "Booleano", "existe": "Booleano",
    "rechazado": "Booleano", "saldoInsuficiente": "Booleano", "vendibleInsuficiente": "Booleano",
    "solicitudInvalida": "Booleano", "conflicto": "Booleano", "nadaQueHacer": "Booleano",
    "acumulado": "Booleano", "ordenNoAdmiteRecepciones": "Booleano", "ajustado": "Booleano",
    "esLaMisma": "Booleano", "restado": "Booleano", "sumado": "Booleano", "habilitado": "Booleano",
    "hayCupo": "Booleano", "eliminable": "Booleano", "traslado": "MotivoDeMovimiento",
    "anulacionDeCompra": "MotivoDeMovimiento", "cancelacionDeCarga": "MotivoDeMovimiento",
    "compra": "MotivoDeMovimiento", "entrega": "MotivoDeMovimiento", "reposicion": "MotivoDeMovimiento",
    "cargaDelCamion": "MotivoDeMovimiento", "cierreDeRendicion": "MotivoDeMovimiento",
    "ajusteManual": "MotivoDeMovimiento", "llenas": "CondicionDeStock", "nula": "UbicacionDeStock",
    "llenasDeclaradas": "Entero", "recargoExpress": "Moneda", "tieneZonas": "Booleano",
    "cobroDeCuentaCorriente": "CategoriaDeCaja", "diferenciaDeCaja": "CategoriaDeCaja",
    "pagoDeComisiones": "CategoriaDeCaja", "cobroDePedido": "CategoriaDeCaja", "saldoACobrar": "Moneda", "enEfectivo": "MedioDeCaja",
    "ingreso": "SentidoDeCaja", "egreso": "SentidoDeCaja",
    "llenasCargadas": "Entero", "vaciasCargadas": "Entero", "llenasRepuestas": "Entero",
    "llenasDevueltas": "Entero", "vaciasDevueltas": "Entero", "llenasRecibidas": "Entero",
    "vaciasEntregadas": "Entero", "llenasFisicas": "Entero", "vaciasACanjear": "Entero",
    "minimoDeLlenas": "Entero",
})
# Stock físico (implementado): nombres propios de sus DSD, sin colisión con otros módulos.
ALIAS_CLASE.update({"renglonesDeAjuste": "ItemAjusteDeStock", "ubicacionesDeStock": "UbicacionDeStock",
                    "saldosEnDepositosYVehiculos": "SaldoDeStock", "depositoCreado": "Deposito",
                    "depositoPredeterminado": "Deposito", "depositoElegido": "Deposito",
                    "ubicacionPredeterminada": "UbicacionDeStock",
                    "itemsSinDescuento": "ItemPedido", "ubicacionDelCamion": "UbicacionDeStock",
                    "ubicacionDelDeposito": "UbicacionDeStock"})
_PLURALES |= {"renglonesDeAjuste", "ubicacionesDeStock", "saldosEnDepositosYVehiculos",
              "itemsSinDescuento"}
GLOSARIO.update({
    "motivoConteoInicial": "MotivoDeAjuste", "motivoRecuento": "MotivoDeAjuste",
    "motivoConciliacion": "MotivoDeAjuste", "correccionDeVendible": "Entero", "diferenciaEsperada": "Entero",
    "minimoDeStock": "Entero", "incluirInactivos": "Booleano", "alcanzaElSaldo": "Booleano",
    "esUnaTransferencia": "Booleano", "sinConteoInicial": "Booleano", "transferenciaValida": "Booleano",
    "avisoRepetido": "Booleano", "predeterminadoQuitado": "Booleano", "nadaQueDescontar": "Booleano",
    "resumenDeReaplicacion": "Registro", "cobrosPendientes": "Registro", "cotizacion": "Registro", "totales": "Registro", "renglon": "Registro", "renglonesActuales": "Registro", "ruta": "Registro", "reintegros": "Registro", "cantidadDeAjustes": "Entero", "cantidadDeMovimientos": "Entero",
})
# Compras (implementado): nombres propios de sus DSD, sin colisión con otros módulos.
ALIAS_CLASE.update({"itemsRecibidos": "ItemRecepcion", "proveedorDadoDeBaja": "Proveedor",
                    "ordenActualizada": "OrdenDeCompra"})
_PLURALES |= {"itemsRecibidos"}
GLOSARIO.update({
    "enviada": "Cadena", "cerradaConFaltante": "Cadena", "costoPrevio": "Moneda",
    "loteDeLaRecepcion": "Identificador", "loteDelContraasiento": "Identificador",
    "anulable": "Booleano", "recibible": "Booleano", "comprobanteLibre": "Booleano",
    "dentroDeLoPedido": "Booleano", "historial": "Registro",
})
ALIAS_PARAMETRO.update({("Distribuidora", "direccion"): ("direccion", "Cadena"),
                        ("Deposito", "direccion"): ("direccion", "Cadena"),
                        ("OrdenDeCompra", "cancelada"): ("estadoDestino", "EstadoDeLaOrden"),
                        ("OrdenDeCompra", "enviada"): ("estadoDestino", "EstadoDeLaOrden"),
                        ("OrdenDeCompra", "cerradaConFaltante"): ("estadoDestino", "EstadoDeLaOrden")})

# El mismo nombre de argumento significa cosas distintas según la clase que lo recibe: el glosario
# da el sentido más común y esta tabla da el de cada clase.
#  - `deposito` es el Deposito físico donde se carga el camión; en el envase y en el caso de
#    recupero es el importe de la garantía (columna `deposit`, numérica), o sea Moneda.
#  - `categoria` de un puesto de trabajo es la CategoriaDePuesto, no la categoría de la caja.
#  - `diferencia` es en unidades (Entero) salvo en la sesión de caja, donde es un importe.
#  - `cargas` de la flota son cargas de combustible, no cargas del camión.
ALIAS_PARAMETRO.update({
    ("CargaDeCamion", "deposito"): ("deposito", "Deposito"),
    ("Vehiculo", "deposito"): ("deposito", "Deposito"),
    ("CylinderService", "deposito"): ("deposito", "Moneda"),
    ("CylinderService", "estadoDestino"): ("estadoDestino", "EstadoDelEnvase"),
    ("Distribuidora", "categoria"): ("categoria", "CategoriaDePuesto"),
    ("PuestoDeTrabajo", "categoria"): ("categoria", "CategoriaDePuesto"),
    ("JobPositionService", "categoria"): ("categoria", "CategoriaDePuesto"),
    ("FleetExpirationsService", "categoria"): ("categoria", "CategoriaDePuesto"),
    ("List<TareaMantenimiento>", "categoria"): ("categoria", "CategoriaDePuesto"),
    ("SesionDeCaja", "diferencia"): ("diferencia", "Moneda"),
    ("FuelConsumptionCalculator", "cargas"): ("cargas", "CargaCombustible[*]"),
    ("S3Service", "imagen"): ("archivo", "Archivo"),
    # La configuración de un proceso se crea y se actualiza con el proceso y sus parámetros: cada
    # DSD nombra los parámetros propios de su proceso, pero es una sola operación.
    **{(c, n): ("parametros", "Registro") for c in ("Distribuidora", "ConfiguracionModulo")
       for n in ("radiosKm", "ventanaDeAceptacion", "exigirCargaDeCamionAbierta", "intervalos")},
    **{(c, n): ("proceso", "ProcesoConfigurable") for c in ("Distribuidora", "ConfiguracionModulo")
       for n in ("despacho", "controlDeStock", "tareasProgramadas")},
    ("S3Service", "contenido"): ("archivo", "Archivo"),
})


def _tipo_clase_del_nombre(n):
    c = ALIAS_CLASE.get(n)
    if c:
        return c + ("[*]" if n in _PLURALES else "")
    cap = n[0].upper() + n[1:]
    if cap in M.CLASES:
        return cap
    return None


def tipo_de_nombre(n):
    """Tipo de un argumento o un retorno nombrado en un DSD; None si no se sabe."""
    if n in GLOSARIO:
        return GLOSARIO[n]
    c = _tipo_clase_del_nombre(n)
    if c:
        return c
    if n.endswith("Id") and len(n) > 2:
        return "Identificador"
    for conc, attrs in M.ATRIBUTOS.items():
        for a in attrs:
            if camel(a) == n:
                try:
                    return tipo_de_atributo(conc, a)
                except KeyError:
                    pass
    return None


# =============================================================================== lectura de los DSD
class Op:
    """Una operación de diseño: lo que recibe un objeto en un DSD."""
    def __init__(self, nombre, params, retorno, crea=False, salidas=()):
        self.nombre, self.params, self.retorno, self.crea = nombre, params, retorno, crea
        self.salidas = list(salidas)   # parámetros de salida: lo que el DSD devuelve además del retorno

    def clave(self):
        return (self.nombre, tuple(n for n, _ in self.params))

    def firma(self, clase=None):
        ps = ", ".join([f"{n}: {t}" for n, t in self.params] + [f"out {n}: {t}" for n, t in self.salidas])
        if self.crea:
            return f"«create» {clase}({ps})"
        r = f": {self.retorno}" if self.retorno else ""
        return f"{self.nombre}({ps}){r}"


# Operaciones de una colección que reciben la clave con la que se busca: sea lo que sea que
# cada DSD use para buscar (un id, un correo, una patente), la clave de un Map es una cadena.
OPS_POR_CLAVE = {"get", "contiene", "containsKey", "remove"}

FALTAN = set()   # nombres de argumentos o retornos que ningún glosario resuelve


def _limpiar_param(p):
    p = p.strip()
    p = re.sub(r'\.manager$', '', p)
    if " " in p:
        p = camel(p)
    return p.split(".")[0]


def _parametros(texto):
    m = re.match(r'^(«create»|[A-Za-z_]\w*)\s*\((.*)\)\s*$', texto)
    if not m:
        return None, []
    ps = [x for x in (_limpiar_param(p) for p in re.split(r',\s*', m.group(2))) if x]
    return m.group(1), ps


# Retornos que son un acuse y no un valor: el DSD los muestra, el diseño no los tipa.
RETORNO_ACUSE = {"confirmacion", "recibido", "guardado"}

# El retorno de una operación concreta, cuando el nombre que usa el DSD es ambiguo:
# (clase, operación) -> tipo.
RETORNO_ESPECIFICO = {
    ("Pedido", "getCambiosDeEstado"): "CambioEstadoPedido[*]",
    ("OrderService", "consultarHistorialDeEstados"): "CambioEstadoPedido[*]",
    ("OrderService", "avisarLlegada"): None,
    ("CylinderService", "verificarVigenciaAlAsignar"): "Envase[*]",
    ("Pedido", "estaSinPagar"): "Booleano",
    ("Siniestro", "getCostoNeto"): "Moneda",
    # El DSD devuelve varios valores que son partes de un mismo resultado (conteos, cupos,
    # tablero): el diseño los tipa como un solo Registro, no como un retorno y sus `out`.
    ("List<Pedido>", "contarPorEstado"): "Registro",
    ("List<Pedido>", "contarEntregadosDelMesPorMetodo"): "Registro",
    ("List<Chofer>", "contarEnLinea"): "Entero",
    ("List<Chofer>", "contarHabilitados"): "Entero",
    ("FranjaHoraria", "cuposLibres"): "Registro",
    ("PersonnelDashboardService", "consultarTableroDePersonal"): "Registro",
    # `carga` y `movimientos` nombran dos cosas en el sistema: el contexto decide
    ("Vehiculo", "getCargas"): "CargaCombustible[*]",
    ("List<CargaCombustible>", "getVigentes"): "CargaCombustible[*]",
    ("FuelLoadService", "consultarCargasDeCombustible"): "CargaCombustible[*]",
    ("Caja", "calcularDiferencia"): "Moneda",
    ("Envase", "getMovimientos"): "MovimientoEnvase[*]",
    ("CylinderService", "consultarHistorialDelEnvase"): "MovimientoEnvase[*]",
    # Carga del camión: las validaciones no devuelven un valor, y los conteos y las preguntas sí
    ("Vehiculo", "validarEnUsoPor"): None,
    ("Vehiculo", "validarSinCargaAbierta"): None,
    ("Chofer", "validarSinCargaAbierta"): None,
    ("UbicacionDeStock", "validarVacia"): None,
    ("CargaDeCamion", "validarQuePuedeSalir"): None,
    ("CargaDeCamion", "validarQueEstaEnRuta"): None,
    ("CargaDeCamion", "validarQueEstaDevuelta"): None,
    ("CargaDeCamion", "validarQuePuedeDeclararElRegreso"): None,
    ("CargaDeCamion", "validarNotaDeDiferencia"): None,
    ("CargaDeCamion", "getEntregasPosterioresALaDeclaracion"): "Entero",
    ("CargaDeCamion", "estaEnRutaCon"): "Booleano",
    ("Chofer", "getPedidosEnCurso"): "Entero",
    # lo pendiente de recibir: por renglón es una cantidad, y de toda la orden, el detalle de cada renglón
    ("OrdenDeCompra", "getPendiente"): "Registro",
}

# Consultas y cálculos que el DSD llama sin mostrar qué devuelven (o que devuelven una prosa que
# no es un nombre): el retorno sale del propio nombre y del código. (clase, operación) -> tipo.
# Solo se aplica si el DSD no dio un retorno.
RETORNO_DE_CONSULTA = {
    ("Usuario", "calcularPromedio"): "Decimal",
    ("Cliente", "getFechaEstimadaDeRecompra"): "Fecha",
    ("Envase", "getResumen"): "Registro",
    ("Envase", "diasHastaElVencimiento"): "Entero",
    ("Carrito", "getItem"): "ItemCarrito",
    ("ItemCarrito", "getDiferenciaDePrecio"): "Moneda",
    ("Pedido", "getFechaDeEntrega"): "Fecha",
    ("Pedido", "getItems"): "ItemPedido[*]",
    ("Pedido", "generarCodigoDeEntrega"): "Cadena",
    ("ItemPedido", "getProducto"): "Producto",
    ("ZonaCobertura", "calcularRecargo"): "Moneda",
    ("Vehiculo", "proyectarVencimientos"): "TareaMantenimiento[*]",
    ("Vehiculo", "estimarKilometrajeDiario"): "Entero",
    ("TareaMantenimiento", "getEstadoDeVencimiento"): "Cadena",
    ("TareaMantenimiento", "proyectarVencimiento"): "Fecha",
    ("PuestoDeTrabajo", "contarEmpleadosActivos"): "Entero",
    ("Empleado", "getPeorVencimiento"): "Cadena",
    ("JornadaDeTrabajo", "getDuracion"): "Decimal",
    ("Reclamo", "getResumen"): "Registro",
    ("Incidencia", "getResumen"): "Registro",
    ("Calificacion", "getEstrellas"): "Entero",
    ("Deposito", "getUmbral"): "UmbralDeStock",

    ("Deposito", "getOrden"): "OrdenDeCompra",
    ("CargaDeCamion", "getItems"): "ItemCarga[*]",
    ("ItemCarga", "calcularEsperado"): "Entero",
    ("ItemCarga", "calcularDiferencia"): "Entero",
    ("ItemCarga", "getEsperado"): "Entero",
    ("OrdenDeCompra", "calcularTotal"): "Moneda",
    ("ItemOrdenDeCompra", "getPendiente"): "Entero",
    ("RendicionChofer", "calcularEfectivoEsperado"): "Moneda",
    ("RendicionChofer", "calcularDiferencia"): "Moneda",
    ("RendicionChofer", "recalcularEfectivoEsperado"): "Moneda",
    ("CuentaCorriente", "calcularDisponible"): "Moneda",
    ("CuentaCorriente", "calcularAntiguedad"): "Registro",
    ("Producto", "calcularDiferencia"): "Entero",
    ("OrderService", "completarDiasSinVentas"): "Registro",
    ("OrderService", "calcularValorPromedio"): "Moneda",
    ("List<Pedido>", "getReservado"): "Entero",
    ("ReportsService", "agruparPorChofer"): "Registro",
    ("ReportsService", "agruparPorProducto"): "Registro",
    ("ReportsService", "agruparPorMetodoDePago"): "Registro",
    ("ReportsService", "agruparPorPeriodo"): "Registro",
    ("RouteBatchPlannerService", "agruparPorProximidad"): "LoteRecorrido[*]",
    ("HealthCheckService", "verificarSalud"): "Registro",
    ("HealthCheckService", "verificarDisponibilidad"): "Registro",
    ("HealthCheckService", "verificarVida"): "Registro",
    ("DemandForecastService", "demandaProyectada"): "Registro",
    ("FleetCoverageService", "ventanasFactibles"): "PropuestaVentanaTaller[*]",
    ("FleetExpirationsService", "consultarVencimientosDeLaFlota"): "Registro",
    ("FleetExpirationsService", "consultarVencimientosDelPersonal"): "Registro",
    ("List<TareaMantenimiento>", "getAbiertasDeEmpleadosPorEstado"): "TareaMantenimiento[*]",
    ("JobPositionService", "consultarPuestosDeTrabajo"): "PuestoDeTrabajo[*]",
    ("EmployeeService", "consultarEmpleado"): "Empleado",
    ("EmployeeService", "consultarEmpleados"): "Empleado[*]",
    ("List<Empleado>", "getActivosPorPuesto"): "Empleado[*]",
    ("AttendanceService", "consultarAsistencias"): "JornadaDeTrabajo[*]",
    ("List<JornadaDeTrabajo>", "getAbiertasDeHoy"): "JornadaDeTrabajo[*]",
    ("LeaveService", "consultarLicencias"): "LicenciaLaboral[*]",
    ("List<LicenciaLaboral>", "getAprobadasQueCubren"): "LicenciaLaboral[*]",
    ("FleetCostService", "ordenarPorCostoPorKilometro"): "Registro",
    ("List<UbicacionDeStock>", "getCantidadPorCondicion"): "Entero",
    ("List<UbicacionDeStock>", "getLlenas"): "Entero",
    ("List<UmbralDeStock>", "getMinimoDeLlenas"): "Entero",
    ("Map<String, Usuario>", "verificarDisponibilidad"): "Booleano",
    ("OrderService", "verificarCoberturaExpress"): "Booleano",
}
# Los predicados se reconocen por el nombre: `estaActivo`, `tieneCupo`, `esValido`, `cubre`...
PREDICADO = re.compile(r'^(es[A-Z]|esta[A-Z]|tiene[A-Z]|is[A-Z]|existe|cubre$|coincideCon$)')


def _tipo_de_retorno(texto, clase=None, op=None):
    """(retorno, salidas) de un mensaje de retorno: el primer valor que devuelve es el retorno
    de la operación; cuando el DSD devuelve varios valores el retorno es un Registro: una operación
    tiene un solo retorno y ningún parámetro de salida. Retorno None si el DSD no lo precisa (códigos de error, prosa, acuses)."""
    if (clase, op) in RETORNO_ESPECIFICO:
        r = RETORNO_ESPECIFICO[(clase, op)]
        return (r, []) if r is None or isinstance(r, str) else r
    tipos = []
    nombres = []
    tokens = [x.strip() for x in re.split(r',\s*|\s+y\s+', texto.strip())]
    hay_coleccion = any((tipo_de_nombre(x) or "").endswith("[*]") for x in tokens)
    for tk in tokens:
        if not tk or tk == "void" or tk in RETORNO_ACUSE:
            continue
        if re.match(r'^\d', tk) or "Exception" in tk or " " in tk or tk in ("null",):
            continue
        t = "Entero" if (tk == "total" and hay_coleccion) else tipo_de_nombre(tk)
        if t is None:
            FALTAN.add(f"retorno {tk!r}")
            t = "?"
        if t not in tipos:
            tipos.append(t)
            nombres.append(camel(tk) if " " in tk else tk)
    if not tipos:
        return None, []
    if len(tipos) > 1 and not all(t == "Moneda" for t in tipos[1:]) and tipos[0] != "Registro":
        # varios valores devueltos son partes de un mismo resultado: la operación tiene un solo retorno, un Registro
        return "Registro", []
    return tipos[0], []


def leer_dsd():
    """Los DSD en estilo Larman, con sus llamadas y el retorno de cada una."""
    out = []
    for ruta in sorted(glob.glob(D + "diagramas/DSD_*.mmd")):
        if not L.es_larman(open(ruta, encoding="utf-8").read()):
            continue
        d = L.leer(ruta)
        llamadas, abiertas = [], []
        for m in d["mensajes"]:
            if L.es_retorno(m):
                for i in range(len(abiertas) - 1, -1, -1):
                    c = abiertas[i]
                    if c["a"] == m["de"] and c["de"] == m["a"]:
                        c["retorno"] = m["texto"]
                        del abiertas[i]
                        break
                continue
            nombre, ps = _parametros(m["texto"])
            if nombre is None:
                continue
            c = {"de": m["de"], "a": m["a"], "nombre": nombre, "params": ps, "retorno": None,
                 "asincrono": m["flecha"] == "--)"}
            llamadas.append(c)
            abiertas.append(c)
        d["llamadas"] = llamadas
        out.append(d)
    return out


def _tipos_del_catalogo():
    _, ops = L.catalogo()
    return {n: {p["nombre"]: CAT_A_PRIM[p["tipo"]] for p in o["parametros"]} for n, o in ops.items()}


# =============================================================================== el modelo
ESTEREOTIPO = {"use case": "controlador", "fachada": "fachada", "pura": "fabricación pura",
               "puerto": "puerto", "adaptador": "adaptador", "coleccion": "colección",
               "externa": "biblioteca"}


class Clase:
    def __init__(self, nombre, tipo):
        self.nombre, self.tipo = nombre, tipo      # tipo: dominio | servicio | puerto | adaptador | coleccion
        self.estereotipo = None
        self.modulo = None
        self.atributos = []                        # (visibilidad, nombre, tipo)
        self.ops = collections.OrderedDict()       # clave -> Op
        self.abstracta = False
        self.planificada = False

    def agregar_op(self, op):
        k = op.clave()
        if k not in self.ops:
            self.ops[k] = op
        elif not self.ops[k].retorno and op.retorno:
            self.ops[k].retorno = op.retorno
            self.ops[k].salidas = op.salidas


class DC:
    """El diagrama de clases de diseño, entero."""
    def __init__(self):
        self.clases = collections.OrderedDict()
        self.asociaciones = []      # dicts: a, b, nombre, ma, mb, composicion, nav_ab, nav_ba
        self.dependencias = set()   # (origen, destino)
        self.realizaciones = []     # (adaptador, puerto)
        self.generalizaciones = []  # (padre, hijo)
        self.sin_resolver = []


def _tipo_de_participante(clase, controladores):
    if clase in M.CLASES:
        return "dominio"
    if re.fullmatch(r'(Map|List)<.+>', clase):
        return "coleccion"
    if clase.endswith("Port"):
        return "puerto"
    if clase.endswith("Adapter"):
        return "adaptador"
    return "servicio"


def _normalizar_params(clase, op, ps, tipos_cat):
    """[(nombre, tipo)] con el literal reemplazado por el parámetro que lo recibe."""
    r, vistos = [], set()
    for p in ps:
        alias = ALIAS_PARAMETRO.get((clase, p)) or ALIAS_PARAMETRO.get(p)
        if alias:
            n, t = alias
        else:
            n, t = p, tipos_cat.get(p) or tipo_de_nombre(p)
            if t is None:
                FALTAN.add(f"argumento {p!r} (en {clase}.{op})")
                t = "?"
        if n in vistos:
            continue
        vistos.add(n)
        r.append((n, t))
    return r


def construir():
    """Arma el DC desde los DSD y el modelo conceptual."""
    dsds = leer_dsd()
    tipos_cat = _tipos_del_catalogo()
    dc = DC()
    man = manifiesto()

    # --- las clases de dominio: las del modelo conceptual, todas
    for nombre, (ctx, atrs, abstracta) in M.CLASES.items():
        c = Clase(nombre, "dominio")
        c.abstracta = abstracta
        c.modulo = _modulo_de_dominio(nombre)
        for a in atrs:
            c.atributos.append(("-", nombre_de_atributo(a), tipo_de_atributo(nombre, a)))
        dc.clases[nombre] = c
    for padre, hijos, _ in M.GENERALIZACIONES:
        for h in hijos:
            dc.generalizaciones.append((padre, h))

    # --- clases de los DSD, operaciones y mensajes entre objetos
    primeros = set()          # clases que reciben el primer mensaje de algún DSD
    mensajes = set()          # (origen, destino) entre clases distintas
    creaciones = set()
    for d in dsds:
        cat = {}
        _, ops = L.catalogo()
        ids = {i: L.clase_de(t) for i, t in d["participantes"].items()}
        primero = d["llamadas"][0] if d["llamadas"] else None
        for i, c in enumerate(d["llamadas"]):
            org, dst = ids.get(c["de"]), ids.get(c["a"])
            if dst is None:
                continue
            if dst not in dc.clases:
                k = _tipo_de_participante(dst, primeros)
                cl = Clase(dst, k)
                cl.planificada = dst in L.PROPUESTAS_CLASE and dst not in man and archivo_de(dst) is None
                dc.clases[dst] = cl
            cl = dc.clases[dst]
            if i == 0:
                primeros.add(dst)
            if c["nombre"] == "«create»":
                ps = _normalizar_params(dst, "«create»", c["params"], {})
                cl.agregar_op(Op("«create»", ps, None, crea=True))
                if org and org != dst:
                    creaciones.add((org, dst))
            else:
                tc = tipos_cat.get(L.operacion(c["nombre"])) if i == 0 else None
                ps = _normalizar_params(dst, c["nombre"], c["params"], tc or {})
                if cl.tipo == "coleccion" and c["nombre"] in OPS_POR_CLAVE and len(ps) == 1:
                    ps = [("clave", "Cadena")]
                try:
                    ret, sal = _tipo_de_retorno(c["retorno"], dst, c["nombre"]) if c["retorno"] else (None, [])
                except KeyError as e:
                    dc.sin_resolver.append(f"{d['base']}: {dst}.{c['nombre']}: {e.args[0]}")
                    ret, sal = None, []
                cl.agregar_op(Op(c["nombre"], ps, ret, salidas=sal))
            if org and org != dst and ids.get(c["de"]) is not None:
                mensajes.add((org, dst))
    # las clases de los DSD que son colecciones o de servicio reciben módulo y papel
    for nombre, cl in dc.clases.items():
        if cl.tipo == "dominio":
            continue
        _asignar_modulo_y_papel(dc, cl, primeros)
    _fusionar_sobrecargas(dc)
    _deduplicar_firmas(dc)
    _unificar_firmas_en_conflicto(dc)
    _tipar_getters(dc)
    _tipar_consultas(dc)
    _relaciones(dc, mensajes, creaciones)
    _realizaciones(dc)
    return dc


def _modulo_de_dominio(concepto):
    tabla = M.TABLA.get(concepto)
    ent = next((v for v in manifiesto().values() if v["kind"] == "entity" and v.get("tabla") == tabla), None) if tabla else None
    if ent:
        return ent["file"].split("/")[0]
    if concepto in getattr(M, "MODULO_PLANIFICADO", {}):
        return M.MODULO_PLANIFICADO[concepto]
    return {"ItemSugerido": "customer", "PropuestaConVigencia": "order", "UbicacionGPS": "delivery"}[concepto]


# Clientes de un servicio externo: reciben el primer mensaje de los casos incluidos (CU-159 y CU-160),
# pero no son el controlador de nada: son fabricación pura.
INFRAESTRUCTURA = {"S3Service"}


def _asignar_modulo_y_papel(dc, cl, primeros):
    if cl.tipo == "coleccion":
        m = re.fullmatch(r'(?:Map|List)<(?:String,\s*)?(\w+)>', cl.nombre)
        elem = m.group(1) if m else None
        cl.modulo = dc.clases[elem].modulo if elem in dc.clases else None
        cl.estereotipo = "colección"
        return
    cl.modulo = modulo_de_clase(cl.nombre)
    if cl.tipo == "puerto":
        cl.estereotipo = "puerto"
    elif cl.tipo == "adaptador":
        cl.estereotipo = "adaptador"
    elif cl.nombre in primeros and cl.nombre not in INFRAESTRUCTURA:
        cl.estereotipo = "controlador" if cl.nombre.endswith("UseCase") else "fachada"
    else:
        cl.estereotipo = "fabricación pura"


def _fusionar_sobrecargas(dc):
    """Un DSD muestra la operación con los argumentos que importan a su caso. Si una variante es
    prefijo de otra (cancelar() y cancelar(motivo)), es la misma operación: queda la más completa."""
    for cl in dc.clases.values():
        por_nombre = collections.defaultdict(list)
        for k, op in cl.ops.items():
            por_nombre[op.nombre].append(k)
        for nombre, claves in por_nombre.items():
            if len(claves) < 2:
                continue
            ordenadas = sorted(claves, key=lambda k: -len(k[1]))
            for k in ordenadas:
                if k not in cl.ops:
                    continue
                for j in ordenadas:
                    if j == k or j not in cl.ops:
                        continue
                    if len(j[1]) < len(k[1]) and k[1][: len(j[1])] == j[1]:
                        if not cl.ops[k].retorno and cl.ops[j].retorno:
                            cl.ops[k].retorno = cl.ops[j].retorno
                            cl.ops[k].salidas = cl.ops[j].salidas
                        del cl.ops[j]


# Nombre del argumento cuando varios DSD pasan lo mismo con nombres distintos y la operación es una
# sola: (operación, tipos de los argumentos) -> nombres.
NOMBRE_UNIFICADO = {
    ("send", ("Cadena",)): ["destinatario"],
    ("send", ("Administrador", "Registro")): ["administrador", "detalle"],
    ("restarStock", ("Entero",)): ["cantidad"],
}
GENERICOS = {"proceso", "parametros", "cantidad", "correo", "archivo", "destinatario", "detalle"}


def _elegir_nombre(candidatos, tipo):
    """El nombre que representa a varios argumentos del mismo tipo: el del tipo (`tipoDeRol`
    para un TipoDeRol), uno genérico del glosario, o el más corto."""
    if len(candidatos) == 1:
        return candidatos[0]
    por_tipo = minuscula(tipo.rstrip("[*]"))
    if por_tipo in candidatos:
        return por_tipo
    gen = sorted(c for c in candidatos if c in GENERICOS)
    if gen:
        return gen[0]
    if tipo in PRIMITIVOS or tipo.rstrip("[*]") in PRIMITIVOS or tipo in CAT_A_PRIM.values():
        return sorted(candidatos, key=lambda c: (len(c), c))[0]
    if tipo in ENUMERACIONES.values() or tipo.rstrip("[*]") not in M.CLASES:
        return por_tipo
    return sorted(candidatos, key=lambda c: (len(c), c))[0]


def _deduplicar_firmas(dc):
    """Dos operaciones de una clase con el mismo nombre y los mismos tipos de argumento son la misma
    operación: los DSD solo le ponen nombres distintos al argumento (`getConfiguracion(despacho)`,
    `getConfiguracion(controlDeStock)`). Queda una, con un nombre que sirve a todas."""
    for cl in dc.clases.values():
        grupos = collections.OrderedDict()
        for k, op in cl.ops.items():
            clave = (op.crea, op.nombre, tuple(t for _, t in op.params), tuple(t for _, t in op.salidas))
            grupos.setdefault(clave, []).append(op)
        if all(len(v) == 1 for v in grupos.values()):
            continue
        nuevas = collections.OrderedDict()
        for (crea, nombre, tipos, tsal), ops in grupos.items():
            op = ops[0]
            if len(ops) > 1:
                fijo = NOMBRE_UNIFICADO.get((nombre, tipos))
                nombres = fijo or [_elegir_nombre(sorted({o.params[i][0] for o in ops}), tipos[i])
                                   for i in range(len(tipos))]
                op = Op(nombre, list(zip(nombres, tipos)), next((o.retorno for o in ops if o.retorno), None),
                        crea=crea, salidas=op.salidas)
            nuevas[op.clave()] = op
        cl.ops = nuevas


def _unificar_firmas_en_conflicto(dc):
    """Una operación tiene una sola firma por clase. Si los DSD la llaman con argumentos distintos (la variante con y la
    variante sin franja, el pedido o su identificador), queda una sola operación con todos los argumentos; los que no
    pasan todas las variantes se marcan opcionales (`= ninguno`, la notación UML de un valor por omisión) y se
    ordenan después de los obligatorios."""
    for cl in dc.clases.values():
        por = collections.OrderedDict()
        for k, op in cl.ops.items():
            por.setdefault((op.crea, op.nombre), []).append(op)
        if all(len(v) == 1 for v in por.values()):
            continue
        nuevas = collections.OrderedDict()
        for (crea, nombre), ops in por.items():
            if len(ops) == 1:
                nuevas[ops[0].clave()] = ops[0]
                continue
            todos = []
            for o in ops:
                for n, t in o.params:
                    if n not in [x for x, _ in todos]:
                        todos.append((n, t))
            en_todas = [n for n, _ in todos if all(n in [x for x, _ in o.params] for o in ops)]
            oblig = [(n, t) for n, t in todos if n in en_todas]
            opcion = [(n, t + " = ninguno") for n, t in todos if n not in en_todas]
            op = Op(nombre, oblig + opcion, next((o.retorno for o in ops if o.retorno), None), crea=crea)
            nuevas[op.clave()] = op
        cl.ops = nuevas


def _tipar_consultas(dc):
    """Una consulta o un cálculo que el DSD no muestra devolviendo nada: su retorno sale de
    `RETORNO_DE_CONSULTA` o, si es un predicado (`estaActivo`, `tieneCupo`), es Booleano."""
    for nombre, cl in dc.clases.items():
        for op in cl.ops.values():
            if op.crea or op.retorno:
                continue
            t = RETORNO_DE_CONSULTA.get((nombre, op.nombre))
            if t is None and PREDICADO.match(op.nombre):
                t = "Booleano"
            if t:
                op.retorno = t


def _tipar_getters(dc):
    """`getTotal()` sin retorno en el DSD devuelve lo que dice el modelo conceptual: el atributo
    `total` del Pedido, o la clase asociada (`getCliente()`)."""
    for nombre, cl in dc.clases.items():
        if cl.tipo != "dominio":
            continue
        vecinos = {a["b"] for a in dc.asociaciones if a["a"] == nombre} | \
                  {a["a"] for a in dc.asociaciones if a["b"] == nombre}
        atrs = {a[1].lstrip("/").lower(): a[2] for a in cl.atributos}
        for op in cl.ops.values():
            if op.crea or op.retorno or not op.nombre.startswith("get") or op.params:
                continue
            resto = op.nombre[3:]
            if resto.lower() in atrs:
                op.retorno = atrs[resto.lower()]
            elif resto in vecinos or (resto in M.CLASES and any(resto in M._anc(v) for v in vecinos)):
                op.retorno = resto


# ------------------------------------------------------------------ relaciones
def _indices_mc(o, d):
    """Índices de ASOCIACIONES entre `o` y `d`, contando que un perfil es un Usuario."""
    r = []
    ao, ad = M._anc(o), M._anc(d)
    for i, (x, ma, t, mb, y, n, cat) in enumerate(M.ASOCIACIONES):
        if (x in ao and y in ad) or (x in ad and y in ao):
            r.append(i)
    return r


def _relaciones(dc, mensajes, creaciones):
    """La visibilidad entre dos objetos dice la relación (Larman, cap. 18):

      - dominio -> dominio con asociación en el modelo conceptual: la asociación, navegable de
        quien manda el mensaje hacia quien lo recibe (visibilidad por atributo);
      - cualquier otro mensaje que llega a un objeto de dominio, o entre dos de dominio sin
        asociación: dependencia (el objeto llega por parámetro o variable local);
      - servicio, puerto o colección -> servicio, puerto o colección: asociación navegable de
        multiplicidad 1 (el colaborador se inyecta como atributo), salvo que el código real diga
        que no se inyecta, en cuyo caso es dependencia.
    """
    man = manifiesto()
    nav = collections.defaultdict(lambda: [False, False])
    for (o, d) in mensajes:
        if o in M.CLASES and d in M.CLASES:
            ao, ad = M._anc(o), M._anc(d)
            for i in _indices_mc(o, d):
                x, _, _, _, y, _, _ = M.ASOCIACIONES[i]
                if x in ao and y in ad:
                    nav[i][0] = True
                if y in ao and x in ad:
                    nav[i][1] = True
    for i, (a, ma, t, mb, b, n, cat) in enumerate(M.ASOCIACIONES):
        dc.asociaciones.append({"a": a, "b": b, "nombre": n, "ma": ma, "mb": mb,
                                "tipo": "comp" if t == "*" else "asoc",
                                "nav_ab": nav[i][0], "nav_ba": nav[i][1], "mc": True})
    # una colección contiene objetos de su clase
    for nombre, cl in dc.clases.items():
        if cl.tipo == "coleccion":
            m = re.fullmatch(r'(?:Map|List)<(?:String,\s*)?(\w+)>', nombre)
            if m and m.group(1) in dc.clases:
                dc.asociaciones.append({"a": nombre, "b": m.group(1), "nombre": "elementos", "ma": "1",
                                        "mb": "0..*", "tipo": "agreg", "nav_ab": True, "nav_ba": False,
                                        "mc": False})
    inyectado = {}
    for (o, d) in sorted(mensajes):
        o_dom, d_dom = o in M.CLASES, d in M.CLASES
        if o_dom and d_dom:
            emparentadas = d in M._anc(o) or o in M._anc(d)
            if not _indices_mc(o, d) and not emparentadas:
                dc.dependencias.add((o, d))
            continue
        if o_dom or d_dom:
            dc.dependencias.add((o, d))
            continue
        if dc.clases[o].tipo == "coleccion":
            dc.dependencias.add((o, d))
            continue
        # colaboradores que no son de dominio: ¿los inyecta el código real?
        if o in man and d in man and d not in man[o].get("dependencias", []):
            dc.dependencias.add((o, d))
            continue
        dc.asociaciones.append({"a": o, "b": d, "nombre": minuscula(d), "ma": "", "mb": "1",
                                "tipo": "asoc", "nav_ab": True, "nav_ba": False, "mc": False})
    dc.creaciones = set(creaciones)


def _realizaciones(dc):
    ads = adaptadores_del_codigo()
    for puerto, lista in ads.items():
        if puerto not in dc.clases:
            continue
        for a in lista:
            if a in dc.clases:
                dc.realizaciones.append((a, puerto))


# =============================================================================== comprobación
SAL_DC = D + "diagramas/clases-diseno/"
_NO_DOMINIO = ("DC_Mod_", "DC_General", "DC_Paquetes")


def _leer_puml():
    """Lo que dicen los diagramas dibujados: clases con miembros, y sus relaciones."""
    clases, rels = {}, []
    for ruta in sorted(glob.glob(SAL_DC + "DC_*.puml")):
        base = os.path.basename(ruta)[:-5]
        dominio = not base.startswith(_NO_DOMINIO)
        lineas = open(ruta, encoding="utf-8").read().split("\n")
        actual = None
        for ln in lineas:
            m = re.match(r'^(?:abstract class|class|interface)\s+(?:"([^"]+)" as \w+|(\w+))(?:\s+<<.*?>>)*\s*(\{)?\s*$', ln)
            if m:
                nombre = m.group(1) or m.group(2)
                actual = nombre if m.group(3) else None
                if actual:
                    clases.setdefault(nombre, {"ops": [], "attrs": [], "vistas": set(), "dominio": False})
                    clases[nombre]["vistas"].add(base)
                    clases[nombre]["dominio"] |= dominio
                continue
            if ln.strip() == "}":
                actual = None
                continue
            if actual:
                mm = re.match(r'^\s+([+-])\s+(.*)$', ln)
                if mm:
                    txt = re.sub(r'\\n\s*', ' ', mm.group(2))
                    (clases[actual]["ops"] if mm.group(1) == "+" else clases[actual]["attrs"]).append(txt)
                continue
            r = re.match(r'^(\w+)(?: "([^"]*)")? (<-->|\*-->|\*--|o-->|-->|<--|--|\.\.>|\.\.\|>|<\|--) (?:"([^"]*)" )?(\w+)(?: : (.*))?$', ln)
            if r:
                rels.append({"vista": base, "dominio": dominio, "a": r.group(1), "ma": r.group(2) or "",
                             "sig": r.group(3), "mb": r.group(4) or "", "b": r.group(5), "nombre": r.group(6) or ""})
    return clases, rels


def verificar_dc():
    """Coherencia entre los DSD, el modelo conceptual y el diagrama de clases de diseño dibujado.
    Devuelve (errores, cifras). Lee los `.puml` generados, no el modelo en memoria: si un DSD
    cambió y el diagrama no se regeneró, falla."""
    errores = []
    clases, rels = _leer_puml()
    if not clases:
        return ["no hay diagramas de clases de diseño en diagramas/clases-diseno/ (correr generar-clases-diseno.py)"], {}
    ident = lambda n: re.sub(r'\W+', '_', n).strip("_")
    ops_de = {c: {re.match(r'^(?:«create» )?(\w+)', o).group(1) if not o.startswith("«create»") else "«create»"
                  for o in v["ops"]} for c, v in clases.items()}
    # una clase se declara una sola vez por diagrama: dos declaraciones duplican sus miembros en la imagen
    for ruta in sorted(glob.glob(D + "diagramas/clases-diseno/*.puml")):
        decl = re.findall(r'^(?:abstract class|class|interface) (.+?) (?:<<|\{|$)', open(ruta, encoding="utf-8").read(), re.M)
        rep = sorted({x for x in decl if decl.count(x) > 1})
        if rep:
            errores.append(f"{os.path.basename(ruta)}: clases declaradas más de una vez {rep[:3]}")
    # 1 y 2: operaciones y clases de los DSD
    n_ops = 0
    for ruta in sorted(glob.glob(D + "diagramas/DSD_*.mmd")):
        if not L.es_larman(open(ruta, encoding="utf-8").read()):
            continue
        d = L.leer(ruta)
        base = os.path.basename(ruta)
        for i, t in d["participantes"].items():
            c = L.clase_de(t)
            if c not in clases:
                errores.append(f"{base}: la clase {c} no está en el diagrama de clases de diseño")
        for m in d["mensajes"]:
            if L.es_retorno(m):
                continue
            op = L.operacion(m["texto"])
            if op is None or m["a"] not in d["participantes"]:
                continue
            c = L.clase_destino(d, m["a"])
            n_ops += 1
            if c in clases and op not in ops_de[c]:
                errores.append(f"{base}: {c}.{op} no está entre las operaciones de {c} en el diagrama de clases")
    # 3: las clases de dominio del DC son las del MC
    dom = {c for c, v in clases.items() if v["dominio"]}
    mc = set(M.CLASES)
    for c in sorted(mc - dom):
        errores.append(f"la clase del modelo conceptual {c} no está en las vistas de dominio del diagrama de clases")
    for c in sorted(dom - mc):
        errores.append(f"{c} está en las vistas de dominio y no es una clase del modelo conceptual")
    for c in sorted(mc & dom):
        esperados = [("-", camel(a)) for a in M.CLASES[c][1]]
        propios = [x.split(":")[0].strip().lstrip("/") for x in clases[c]["attrs"]]
        for _, a in esperados:
            if a not in propios:
                errores.append(f"{c}: falta el atributo {a} del modelo conceptual")
    # 3b: las asociaciones del MC, con su multiplicidad, y la navegabilidad que piden los mensajes
    por_par = collections.defaultdict(list)
    for r in rels:
        if r["dominio"] and r["a"] in mc and r["b"] in mc and r["sig"] in ("<-->", "*-->", "*--", "-->", "<--", "--"):
            por_par[(r["a"], r["b"], r["nombre"])].append(r)
    for a, ma, t, mb, b, n, _ in M.ASOCIACIONES:
        rs = por_par.get((a, b, n), [])
        if not rs:
            errores.append(f"falta la asociación {a} {n} {b} del modelo conceptual")
        elif not any(r["ma"] == ma and r["mb"] == mb for r in rs):
            errores.append(f"la asociación {a} {n} {b} no tiene la multiplicidad {ma} / {mb} del modelo conceptual")
    sentidos = collections.defaultdict(set)      # (a, b, nombre) -> {"ab", "ba"}
    for ruta in sorted(glob.glob(D + "diagramas/DSD_*.mmd")):
        if not L.es_larman(open(ruta, encoding="utf-8").read()):
            continue
        d = L.leer(ruta)
        base = os.path.basename(ruta)
        for m in d["mensajes"]:
            if L.es_retorno(m) or m["de"] not in d["participantes"] or m["a"] not in d["participantes"]:
                continue
            o, de = L.clase_destino(d, m["de"]), L.clase_destino(d, m["a"])
            if o not in mc or de not in mc or o == de:
                continue
            ao, ad = M._anc(o), M._anc(de)
            asoc = [x for x in M.ASOCIACIONES if (x[0] in ao and x[4] in ad) or (x[0] in ad and x[4] in ao)]
            if asoc:
                for x in asoc:
                    if x[0] in ao and x[4] in ad:
                        sentidos[(x[0], x[4], x[5])].add("ab")
                    if x[0] in ad and x[4] in ao:
                        sentidos[(x[0], x[4], x[5])].add("ba")
            elif de not in ao and o not in ad:
                if not any(r["a"] == ident(o) and r["b"] == ident(de) and r["sig"] == "..>" for r in rels):
                    errores.append(f"{base}: {o} le manda un mensaje a {de}, sin asociación en el modelo conceptual, y falta la dependencia")
    for (a, b, n), dirs in sentidos.items():
        rs = por_par.get((a, b, n), [])
        if not rs:
            continue
        for sentido in dirs:
            ok = any((sentido == "ab" and r["sig"] in ("-->", "<-->", "*-->")) or
                     (sentido == "ba" and r["sig"] in ("<--", "<-->")) or
                     (r["sig"] == "*--" and dirs == {"ab", "ba"}) for r in rs)
            if not ok:
                errores.append(f"un DSD manda mensajes de {a if sentido == 'ab' else b} a {b if sentido == 'ab' else a} "
                               f"y la asociación {a} {n} {b} no es navegable en ese sentido")
    # 4: notación UML, sin sintaxis del código
    for c, v in clases.items():
        for o in v["ops"]:
            if not re.match(r'^(?:«create» )?\w+\((?:\w+: [\wáéíóú\[\]*]+(?: = ninguno)?(?:, \w+: [\wáéíóú\[\]*]+(?: = ninguno)?)*)?\)(?:: [\w\[\]*]+)?$', o):
                errores.append(f"{c}: la operación «{o}» no está en notación UML (+ nombre(parámetro: Tipo): Retorno)")
        firmas = collections.defaultdict(set)
        for o in v["ops"]:
            if re.search(r'\bout \w+:', o):
                errores.append(f"{c}: la operación «{o}» tiene un parámetro de salida (`out`): una operación tiene un solo retorno")
            m_ = re.match(r'^(?:«create» )?(\w+)\((.*)\)', o)
            if m_:
                firmas[m_.group(1)].add(m_.group(2))
        for nombre_, fs_ in firmas.items():
            if len(fs_) > 1:
                errores.append(f"{c}: la operación {nombre_} tiene {len(fs_)} firmas distintas (sobrecarga en conflicto)")
        for a in v["attrs"]:
            if not re.match(r'^/?\w+: [\w\[\]*]+$', a):
                errores.append(f"{c}: el atributo «{a}» no está en notación UML (- nombre: Tipo)")
    return errores, {"clases": len(clases), "operaciones": n_ops}
