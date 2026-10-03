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
    "RoleType": "TipoDeRol", "PaymentGateway": "Pasarela", "LedgerPaymentStatus": "EstadoDelPago", "RaterRole": "RolDelCalificador",
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
}
MONEDA = {"precio", "importe", "seña", "recargo", "costo", "depósito", "depósito comprometido",
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
    "ModuleConfigService": "distributor", "DispatchConfigService": "distributor",
    "ScheduledTaskGate": "distributor", "ModuleConfigController": "distributor",
    "OrderStatusHistoryService": "order", "RouteBatchPlannerService": "order",
    "RouteSequencerService": "order",
    "RefundPaymentUseCase": "payments", "ReintegroListener": "payments",
    "CoverageZoneCronService": "coverage-zone",
    "HealthCheckService": "health",
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
    raise KeyError(f"sin tipo para {concepto}.{atributo}")


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
    "calificaciones": "Calificacion", "configuracion": "ConfiguracionModulo", "ubicacion": "UbicacionGPS",
    "posicion": "UbicacionGPS", "carrito": "Carrito", "reserva": "Pedido", "reservas": "Pedido",
    "administrador": "Administrador", "administradores": "Administrador", "movimientos": "MovimientoEnvase",
    "envase": "Envase", "envases": "Envase", "usuarios": "Usuario",
    "distribuidoras": "Distribuidora", "choferes": "Chofer", "clientes": "Cliente", "reclamos": "Reclamo",
    "incidencias": "Incidencia", "productos": "Producto", "vehiculos": "Vehiculo", "pedidos": "Pedido",
    "pago": "Pago", "pagos": "Pago", "roles": "Rol", "rol": "Rol", "tareas": "TareaMantenimiento",
    "aviso": "AvisoRecupero", "cercanos": "Chofer", "contactados": "Chofer", "aceptados": "Chofer", "libres": "Chofer",
    "activos": "Chofer", "habilitados": "Chofer", "solicitante": "Usuario", "autor": "Usuario",
    "usuario": "Usuario", "chofer": "Chofer", "choferAnterior": "Chofer", "cliente": "Cliente",
    "vehiculo": "Vehiculo", "producto": "Producto", "pedido": "Pedido", "reclamo": "Reclamo",
    "incidencia": "Incidencia", "distribuidora": "Distribuidora", "item": "ItemPedido", "items": "ItemPedido",
    "itemsDelCarrito": "ItemCarrito", "promociones": "Promocion", 
}
_PLURALES = {"cercanos", "contactados", "aceptados", "libres", "activos", "habilitados", "vencidas",
             "recompras", "direcciones", "franjas", "zonas", "cambios", "adjuntos", "tareas", "ventanas",
             "ofertas", "asignaciones", "asientos", "calificaciones", "movimientos", "envases", "usuarios",
             "distribuidoras", "choferes", "clientes", "reclamos", "incidencias", "productos", "vehiculos",
             "pedidos", "pagos", "roles", "administradores", "reservas", "items", "promociones"}

# nombre -> tipo, para lo que no es una clase ni un atributo del modelo.
GLOSARIO = {
    # parámetros
    "clave": "Cadena", "claveAnterior": "Cadena", "contrasena": "Cadena", "correoActual": "Cadena",
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
    "ventanaDeAceptacion": "Entero", "venceEn": "Entero", "granularidad": "Cadena", "periodo": "Cadena",
    "monto": "Moneda", "montoDeLaSenia": "Moneda", "importe": "Moneda", "precio": "Moneda",
    "precioUnitario": "Moneda", "subtotal": "Moneda", "subtotalItems": "Moneda", "recargo": "Moneda",
    "costo": "Moneda", "gastoEstimado": "Moneda", "total": "Moneda", "saldo": "Moneda", "ajustes_": "Moneda",
    "deposito": "Moneda", "descuento": "Decimal",
    "fecha": "Fecha", "fechaAgendada": "Fecha", "fechaDesde": "Fecha", "fechaHasta": "Fecha",
    "fechaEstimada": "Fecha", "fechaDeRegistro": "Fecha", "ultimaCompra": "Fecha", "vencimiento": "Fecha",
    "ahora": "FechaHora", "hoy": "Fecha", "desde": "FechaHora", "hasta": "FechaHora", "llegada": "FechaHora",
    "vigencia": "FechaHora", "vigenteHasta": "FechaHora", "horaInicio": "Hora", "horaFin": "Hora",
    "activa": "Booleano", "activo": "Booleano", "disponible": "Booleano", "bloquear": "Booleano",
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
    "calificado": "Usuario", "despacho": "ProcesoConfigurable", "tareasProgramadas": "ProcesoConfigurable",
    "devuelto": "Booleano", "nombreDelChofer": "Cadena", "usuarioActual": "Usuario", "asignado": "Booleano",
    "pendientes": "Pedido[*]", "reservados": "Pedido[*]", "retiro": "Envase", "tokens": "Cadena[*]",
    "marcasDeUltimaEjecucion": "Registro", "bloqueado": "Booleano", "habilitado": "Booleano",
    "tipo": "Cadena", "esSena": "Booleano", "orden": "Entero", "relacion": "Cadena", "usuario_": "Usuario",
    "rolCliente": "TipoDeRol", "rolChofer": "TipoDeRol", "rolAdministradorGeneral": "TipoDeRol",
    "destinatarioDelAviso": "Cadena", "vencimientos": "Registro", "ventasDelDia": "Registro",
    "ventasPorDia": "Registro", "entregadosDelDia": "Entero", "cantidadDeItems": "Entero",
    "kilometros": "Entero", "resultado": "Cadena", "pendiente": "EstadoPedido",
    "cancelado": "EstadoPedido", "aceptado": "EstadoPedido", "enCamino": "Booleano",
    "entregado": "EstadoPedido", "enProceso": "EstadoDelReclamo", "despachado": "EstadoDelEnvase",
    "enDeposito": "EstadoDelEnvase", "gasCylinderId": "Identificador",
    # retornos
    "cubierta": "Booleano", "firmaValida": "Booleano", "sesionValida": "Booleano", "valido": "Booleano",
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
}

# El DSD a veces pasa un valor literal o un estado como argumento: se lo reemplaza por el parámetro
# que lo recibe en el diseño (nombre, tipo). Se busca por (clase, nombre) y después por nombre.
ALIAS_PARAMETRO = {
    "1": ("cantidad", "Entero"),
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
}


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
    ("OrderStatusHistoryService", "consultarHistorialDeEstados"): "CambioEstadoPedido[*]",
    ("OrderService", "avisarLlegada"): None,
    ("CylinderService", "verificarVigenciaAlAsignar"): "Envase[*]",
    ("Pedido", "estaSinPagar"): "Booleano",
}


def _tipo_de_retorno(texto, clase=None, op=None):
    """(retorno, salidas) de un mensaje de retorno: el primer valor que devuelve es el retorno
    de la operación y los demás son parámetros de salida (`out`); una operación nunca tiene
    dos retornos. Retorno None si el DSD no lo precisa (códigos de error, prosa, acuses)."""
    if (clase, op) in RETORNO_ESPECIFICO:
        return RETORNO_ESPECIFICO[(clase, op)], []
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
    return tipos[0], list(zip(nombres[1:], tipos[1:]))


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
    _tipar_getters(dc)
    _relaciones(dc, mensajes, creaciones)
    _realizaciones(dc)
    return dc


def _modulo_de_dominio(concepto):
    tabla = M.TABLA.get(concepto)
    ent = next((v for v in manifiesto().values() if v["kind"] == "entity" and v.get("tabla") == tabla), None) if tabla else None
    if ent:
        return ent["file"].split("/")[0]
    return {"ItemSugerido": "customer", "PropuestaConVigencia": "order", "UbicacionGPS": "delivery"}[concepto]


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
    elif cl.nombre in primeros:
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
            if not re.match(r'^(?:«create» )?\w+\((?:(?:out )?\w+: [\wáéíóú\[\]*]+(?:, (?:out )?\w+: [\wáéíóú\[\]*]+)*)?\)(?:: [\w\[\]*]+)?$', o):
                errores.append(f"{c}: la operación «{o}» no está en notación UML (+ nombre(parámetro: Tipo): Retorno)")
        for a in v["attrs"]:
            if not re.match(r'^/?\w+: [\w\[\]*]+$', a):
                errores.append(f"{c}: el atributo «{a}» no está en notación UML (- nombre: Tipo)")
    return errores, {"clases": len(clases), "operaciones": n_ops}
