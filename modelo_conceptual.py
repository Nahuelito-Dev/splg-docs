"""Modelo conceptual de SPLG, en una sola pieza.

Lo leen generar-modelo-conceptual.py (las vistas, el .mmd para Lucidchart y la tabla
de relaciones del Documento 2), generar-modelo-datos.py (el DER conceptual) y
material-de-trabajo/verificar-mc-der.py (la consistencia entre los dos).

Convenciones (Larman, «UML y patrones», cap. 9):
  - las clases conceptuales llevan atributos y nunca operaciones ni tipos de
    implementación ni claves foráneas;
  - cada asociación tiene un nombre en voz activa que se lee de A hacia B
    («Cliente realiza Pedido»); la dirección de lectura se dibuja con `>`;
  - la multiplicidad va en los dos extremos, junto a la clase a la que se refiere;
  - un atributo con `/` adelante es derivado.
"""

# ----------------------------------------------------------------- categorías
PF = "Parte física de"
PL = "Parte lógica de"
LT = "Es una línea de transacción de"
RG = "Es un registro de"
EM = "Es miembro de / empleado de"
UG = "Usa o gestiona"
DE = "Descripción para"
TR = "Está relacionado con una transacción"
PR = "Es propiedad de"
EP = "Es propiedad de / está en poder de"

# ------------------------------------------------------------------ contextos
# clave -> (título, módulo del paquete)
CONTEXTOS = [
    ("OrganizacionYAcceso", "Organización y acceso"),
    ("Clientes", "Clientes"),
    ("CatalogoEInventario", "Catálogo e inventario"),
    ("VentaYPedidos", "Venta y pedidos"),
    ("Pagos", "Pagos"),
    ("DespachoYLogistica", "Despacho y logística"),
    ("FlotaYChoferes", "Flota y choferes"),
    ("Posventa", "Posventa"),
]

# ------------------------------------------------------------------- conceptos
# nombre: (contexto, [atributos], abstracta)
# El orden es el de la lista de conceptos idóneos (Documento 2, §1.2).
_C = {}
def _c(nombre, ctx, atributos=(), abstracta=False):
    _C[nombre] = (ctx, list(atributos), abstracta)

_c("Distribuidora", "OrganizacionYAcceso", ["nombre", "razón social", "CUIT", "estado"])
_c("Usuario", "OrganizacionYAcceso", ["nombre", "correo", "teléfono", "bloqueado"])
_c("Rol", "OrganizacionYAcceso", ["tipo"])
_c("Administrador", "OrganizacionYAcceso")
_c("ConfiguracionModulo", "OrganizacionYAcceso", ["módulo", "parámetros"])
_c("AsientoAuditoria", "OrganizacionYAcceso",
   ["operación", "recurso", "aplicación", "resultado", "cambios", "fecha"])

_c("Cliente", "Clientes", ["consumo mensual declarado", "días de aviso"])
_c("DireccionEntrega", "Clientes",
   ["calle y altura", "piso y departamento", "punto", "precisión", "predeterminada"])
_c("InvitacionRecompra", "Clientes", ["agotamiento estimado"])
_c("ItemSugerido", "Clientes", ["cantidad"])

_c("Producto", "CatalogoEInventario", ["tipo", "peso en kilos", "precio", "stock", "activo"])
_c("Promocion", "CatalogoEInventario", ["cantidad", "descuento"])
_c("Envase", "CatalogoEInventario", ["número de serie", "estado", "depósito", "/vencimiento"])
_c("MovimientoEnvase", "CatalogoEInventario", ["desde", "hacia", "fecha"])
_c("RevisionEnvase", "CatalogoEInventario", ["fecha", "resultado", "próxima revisión"])
_c("CasoRecupero", "CatalogoEInventario",
   ["escalón", "depósito comprometido", "estado", "resolución"])
_c("AvisoRecupero", "CatalogoEInventario", ["escalón", "tipo", "vence"])

_c("Carrito", "VentaYPedidos", ["última modificación"])
_c("ItemCarrito", "VentaYPedidos", ["cantidad", "precio unitario"])
_c("Pedido", "VentaYPedidos",
   ["estado", "/total", "modalidad de entrega", "fecha agendada", "método de pago", "seña",
    "código de entrega", "nombre de quien recibe", "documento de quien recibe",
    "vínculo con quien recibe"])
_c("ItemPedido", "VentaYPedidos", ["cantidad", "precio unitario", "/subtotal"])
_c("CambioEstadoPedido", "VentaYPedidos", ["desde", "hacia", "motivo", "fecha"])
_c("CambioDireccion", "VentaYPedidos", ["motivo", "fecha"])
_c("ZonaCobertura", "VentaYPedidos",
   ["nombre", "área", "recargo", "tipo de recargo", "vigente hasta"])
_c("FranjaHoraria", "VentaYPedidos", ["desde", "hasta", "cupo", "activa"])

_c("Pago", "Pagos", ["importe", "pasarela", "estado", "es seña", "fecha"])

_c("PropuestaConVigencia", "DespachoYLogistica", ["estado", "vence"], abstracta=True)
_c("OfertaDespacho", "DespachoYLogistica")
_c("LoteRecorrido", "DespachoYLogistica", ["estado", "/peso total"])
_c("ParadaLote", "DespachoYLogistica", ["orden"])
_c("OfertaLote", "DespachoYLogistica")

_c("Chofer", "FlotaYChoferes", ["disponible", "habilitado", "validado", "/calificación"])
_c("Vehiculo", "FlotaYChoferes",
   ["patente", "tipo", "carga máxima", "kilometraje", "estado en la flota"])
_c("AsignacionVehiculo", "FlotaYChoferes", ["asignado el", "liberado el", "nota"])
_c("PlanMantenimiento", "FlotaYChoferes",
   ["nombre", "disparo", "intervalo", "anticipación", "criticidad"])
_c("TareaMantenimiento", "FlotaYChoferes",
   ["estado", "vence", "vencimiento proyectado", "prestador", "número", "costo"])
_c("AdjuntoTarea", "FlotaYChoferes", ["nombre original", "tipo de archivo", "fecha de carga"])
_c("PropuestaVentanaTaller", "FlotaYChoferes", ["desde", "hasta"])
_c("UbicacionGPS", "FlotaYChoferes", ["latitud", "longitud"])
_c("RegistroUsoVehiculo", "FlotaYChoferes", ["día", "kilómetros", "pedidos"])

_c("Reclamo", "Posventa", ["motivo", "descripción", "estado", "resolución", "fotografía"])
_c("Incidencia", "Posventa",
   ["tipo", "momento", "descripción", "estado", "resolución", "fotografía"])
_c("Calificacion", "Posventa", ["puntaje", "comentario"])

CLASES = _C

# ------------------------------------------------------------- generalizaciones
# padre, hijos, restricciones (UML 2.5, §9.9.7: conjunto de generalización)
GENERALIZACIONES = [
    ("Usuario", ["Cliente", "Chofer", "Administrador"], "{overlapping, incomplete}"),
    ("PropuestaConVigencia",
     ["OfertaDespacho", "OfertaLote", "PropuestaVentanaTaller", "InvitacionRecompra",
      "AvisoRecupero"], "{disjoint, complete}"),
]

# ------------------------------------------------------------------ asociaciones
# (A, multiplicidad en A, tipo, multiplicidad en B, B, nombre, categoría)
# tipo: "-" asociación, "*" composición (A es el todo). El nombre se lee de A hacia B.
ASOCIACIONES = [
    ("Usuario", "0..*", "-", "0..1", "Rol", "tiene asignado", DE),
    ("Distribuidora", "1", "-", "0..*", "Chofer", "emplea", EM),
    ("Distribuidora", "0..1", "-", "0..*", "Administrador", "emplea", EM),
    ("Distribuidora", "1", "-", "0..*", "Producto", "comercializa", UG),
    ("Distribuidora", "1", "-", "0..*", "Envase", "posee", PR),
    ("Distribuidora", "1", "-", "0..*", "Pedido", "gestiona", UG),
    ("Distribuidora", "1", "*", "0..*", "ZonaCobertura", "define", PL),
    ("Distribuidora", "1", "*", "0..*", "FranjaHoraria", "define", PL),
    ("Distribuidora", "1", "*", "0..*", "ConfiguracionModulo", "parametriza", DE),
    ("Usuario", "0..1", "-", "0..*", "AsientoAuditoria", "origina", RG),

    ("Cliente", "1", "*", "0..*", "DireccionEntrega", "registra", PL),
    ("Cliente", "1", "-", "0..*", "Pedido", "realiza", TR),
    ("Cliente", "1", "*", "0..*", "Carrito", "arma", TR),
    ("Cliente", "1", "-", "0..*", "InvitacionRecompra", "recibe", TR),
    ("Cliente", "0..*", "-", "0..1", "Producto", "usa habitualmente", UG),
    ("InvitacionRecompra", "0..1", "-", "0..1", "Pedido", "se convierte en", TR),
    ("InvitacionRecompra", "1", "*", "1..*", "ItemSugerido", "sugiere", LT),
    ("InvitacionRecompra", "0..*", "-", "0..1", "DireccionEntrega", "sugiere entregar en", TR),
    ("ItemSugerido", "0..*", "-", "1", "Producto", "corresponde a", DE),

    ("Carrito", "1", "*", "0..*", "ItemCarrito", "contiene", LT),
    ("ItemCarrito", "0..*", "-", "1", "Producto", "corresponde a", DE),
    ("Pedido", "1", "*", "1..*", "ItemPedido", "contiene", LT),
    ("ItemPedido", "0..*", "-", "1", "Producto", "corresponde a", DE),
    ("Pedido", "0..*", "-", "1", "DireccionEntrega", "se entrega en", TR),
    ("Pedido", "0..*", "-", "0..1", "FranjaHoraria", "se programa en", TR),
    ("Pedido", "0..*", "-", "0..1", "ZonaCobertura", "aplica el recargo de", TR),
    ("Pedido", "1", "*", "0..*", "CambioEstadoPedido", "registra", RG),
    ("Usuario", "0..1", "-", "0..*", "CambioEstadoPedido", "efectúa", TR),
    ("Pedido", "1", "*", "0..*", "CambioDireccion", "registra", RG),
    ("CambioDireccion", "0..*", "-", "1", "DireccionEntrega", "cambia desde", TR),
    ("CambioDireccion", "0..*", "-", "1", "DireccionEntrega", "cambia hacia", TR),
    ("Usuario", "1", "-", "0..*", "CambioDireccion", "realiza", TR),
    ("Chofer", "0..1", "-", "0..*", "Pedido", "entrega", TR),
    ("Pedido", "1", "-", "0..*", "Pago", "se salda con", TR),

    ("Pedido", "1", "*", "0..*", "OfertaDespacho", "genera", TR),
    ("OfertaDespacho", "0..*", "-", "1", "Chofer", "se dirige a", TR),
    ("LoteRecorrido", "1", "*", "1..*", "ParadaLote", "se compone de", PF),
    ("ParadaLote", "0..*", "-", "1", "Pedido", "atiende", TR),
    ("LoteRecorrido", "1", "*", "0..*", "OfertaLote", "genera", TR),
    ("OfertaLote", "0..*", "-", "1", "Chofer", "se dirige a", TR),
    ("Chofer", "0..1", "-", "0..*", "LoteRecorrido", "acepta", TR),

    ("Chofer", "1", "-", "0..*", "Vehiculo", "tiene registrado", UG),
    ("Chofer", "0..*", "-", "0..*", "Vehiculo", "usa", UG),     # clase de asociación
    ("Chofer", "1", "-", "0..1", "UbicacionGPS", "se ubica en", DE),
    ("PlanMantenimiento", "1", "-", "0..*", "TareaMantenimiento", "genera", RG),
    ("TareaMantenimiento", "0..*", "-", "0..1", "Vehiculo", "habilita", TR),
    ("TareaMantenimiento", "0..*", "-", "0..1", "Chofer", "habilita", TR),
    ("TareaMantenimiento", "1", "*", "0..*", "PropuestaVentanaTaller", "origina", TR),
    ("TareaMantenimiento", "1", "*", "0..*", "AdjuntoTarea", "adjunta", PL),
    ("PropuestaVentanaTaller", "0..*", "-", "1", "Chofer", "se dirige a", TR),
    ("Vehiculo", "1", "*", "0..*", "RegistroUsoVehiculo", "acumula", RG),

    ("Producto", "1", "*", "0..*", "Promocion", "ofrece", DE),
    ("Producto", "0..1", "-", "0..*", "Envase", "describe", DE),
    ("Envase", "1", "*", "0..*", "MovimientoEnvase", "registra", RG),
    ("Envase", "1", "*", "0..*", "RevisionEnvase", "se somete a", RG),
    ("Pedido", "0..1", "-", "0..*", "MovimientoEnvase", "origina", TR),
    ("Usuario", "0..1", "-", "0..*", "MovimientoEnvase", "ejecuta", TR),
    ("Cliente", "0..1", "-", "0..*", "Envase", "tiene en su poder", EP),
    ("Pedido", "0..1", "-", "0..*", "Envase", "despacha", TR),
    ("Envase", "1", "-", "0..*", "CasoRecupero", "motiva", TR),
    ("CasoRecupero", "0..*", "-", "1", "Cliente", "se abre contra", TR),
    ("Usuario", "0..1", "-", "0..*", "CasoRecupero", "resuelve", TR),
    ("CasoRecupero", "1", "*", "0..*", "AvisoRecupero", "emite", RG),

    ("Pedido", "1", "-", "0..*", "Reclamo", "origina", TR),
    ("Cliente", "1", "-", "0..*", "Reclamo", "presenta", TR),
    ("Pedido", "1", "-", "0..*", "Incidencia", "origina", TR),
    ("Usuario", "1", "-", "0..*", "Incidencia", "reporta", TR),
    ("Pedido", "1", "-", "0..2", "Calificacion", "recibe", TR),
    ("Usuario", "1", "-", "0..*", "Calificacion", "emite", TR),
    ("Usuario", "1", "-", "0..*", "Calificacion", "recibe", TR),
]

# Clase de asociación: (clase, extremo A, extremo B). Se dibuja con la línea
# punteada que sale de la clase hacia la asociación Chofer–Vehiculo.
CLASE_ASOCIACION = ("AsignacionVehiculo", "Chofer", "Vehiculo")

# ----------------------------------------------------------------------- vistas
# titulo, archivo, [(clases con atributos)], [(clases de referencia, sin atributos)]
# En cada vista se dibujan las asociaciones cuyos dos extremos están en ella.
VISTAS = [
    ("Usuarios y cuentas", "MC_Usuarios-y-cuentas",
     ["Distribuidora", "Usuario", "Rol", "Administrador", "ConfiguracionModulo",
      "AsientoAuditoria", "Cliente", "DireccionEntrega", "InvitacionRecompra", "ItemSugerido"],
     ["Chofer", "Producto", "Pedido"]),
    ("Pedidos y pagos", "MC_Pedidos",
     ["Pedido", "ItemPedido", "Carrito", "ItemCarrito", "CambioEstadoPedido",
      "CambioDireccion", "ZonaCobertura", "FranjaHoraria", "Pago"],
     ["Cliente", "Chofer", "Producto", "DireccionEntrega", "Usuario", "Distribuidora"]),
    ("Despacho y propuestas con vigencia", "MC_Despacho",
     ["PropuestaConVigencia", "OfertaDespacho", "OfertaLote", "LoteRecorrido", "ParadaLote"],
     ["PropuestaVentanaTaller", "InvitacionRecompra", "AvisoRecupero", "Pedido", "Chofer"]),
    ("Flota y choferes", "MC_Flota",
     ["Chofer", "Vehiculo", "AsignacionVehiculo", "PlanMantenimiento", "TareaMantenimiento",
      "AdjuntoTarea", "PropuestaVentanaTaller", "UbicacionGPS", "RegistroUsoVehiculo"],
     ["Usuario", "Distribuidora"]),
    ("Envases y catálogo", "MC_Envases",
     ["Producto", "Promocion", "Envase", "MovimientoEnvase", "RevisionEnvase", "CasoRecupero",
      "AvisoRecupero"],
     ["Cliente", "Pedido", "Usuario", "Distribuidora"]),
    ("Posventa", "MC_Posventa",
     ["Calificacion", "Incidencia", "Reclamo"],
     ["Usuario", "Pedido", "Cliente"]),
]

# -------------------------------------------------------- correspondencia con la BD
# concepto -> tabla del modelo de datos. None: el concepto no tiene tabla propia y
# se explica en OBSERVACION.
TABLA = {
    "Distribuidora": "distributor", "Usuario": "user", "Rol": "role",
    "Administrador": "admin", "ConfiguracionModulo": "module_config",
    "AsientoAuditoria": "audit_log", "Cliente": "customer",
    "DireccionEntrega": "user_address", "InvitacionRecompra": "repurchase_invitation",
    "ItemSugerido": None, "Producto": "gas_cylinder", "Promocion": "gas_cylinder_promotion",
    "Envase": "cylinder", "MovimientoEnvase": "cylinder_movement",
    "RevisionEnvase": "cylinder_inspection", "CasoRecupero": "cylinder_recovery_case",
    "AvisoRecupero": "cylinder_recovery_notice", "Carrito": "cart", "ItemCarrito": "cart_item",
    "Pedido": "order", "ItemPedido": "order_item", "CambioEstadoPedido": "order_status_history",
    "CambioDireccion": "order_address_change", "ZonaCobertura": "coverage_zone",
    "FranjaHoraria": "time_slot", "Pago": "payment", "PropuestaConVigencia": None,
    "OfertaDespacho": "order_dispatch_offer", "LoteRecorrido": "route_batch",
    "ParadaLote": "route_batch_stop", "OfertaLote": "route_batch_offer",
    "Chofer": "delivery", "Vehiculo": "car", "AsignacionVehiculo": "vehicle_assignment",
    "PlanMantenimiento": "maintenance_plan", "TareaMantenimiento": "maintenance_task",
    "AdjuntoTarea": "maintenance_task_attachment",
    "PropuestaVentanaTaller": "maintenance_window_proposal", "UbicacionGPS": None,
    "RegistroUsoVehiculo": "vehicle_usage_log", "Reclamo": "claims", "Incidencia": "incident",
    "Calificacion": "rating",
}

OBSERVACION = {
    "ItemSugerido": "Sin tabla: las líneas sugeridas se guardan como JSON en "
                    "`repurchase_invitation.suggested_items`.",
    "PropuestaConVigencia": "Concepto abstracto: sin tabla. Sus atributos `estado` y `vence` "
                            "están en cada tabla de sus cinco especializaciones.",
    "UbicacionGPS": "Sin tabla: la posición vigente es la columna `delivery.actual_location`.",
    "Producto": "La base lo llama `gas_cylinder` (tipo de garrafa); el modelo conceptual y los "
                "documentos lo llaman Producto, y esa es la única denominación del dominio.",
    "Vehiculo": "La tabla se llama `car` por historia del proyecto.",
    "Chofer": "La tabla se llama `delivery` por historia del proyecto.",
    "DireccionEntrega": "Pertenece al usuario (`user_id`), no al perfil de cliente.",
    "Carrito": "Pertenece al usuario (`user_id`), no al perfil de cliente.",
}

# concepto -> {atributo: columna}. None: atributo derivado que no se guarda.
ATRIBUTOS = {
    "Distribuidora": {"nombre": "name", "razón social": "legal_name", "CUIT": "tax_id",
                      "estado": "status"},
    "Usuario": {"nombre": "full_name", "correo": "email", "teléfono": "phone_number",
                "bloqueado": "blocked"},
    "Rol": {"tipo": "type"},
    "ConfiguracionModulo": {"módulo": "module", "parámetros": "params"},
    "AsientoAuditoria": {"operación": "http_method", "recurso": "resource",
                         "aplicación": "client_source", "resultado": "result",
                         "cambios": "changes", "fecha": "created_at"},
    "Cliente": {"consumo mensual declarado": "avg_monthly_consumption_kg",
                "días de aviso": "repurchase_notice_days"},
    "DireccionEntrega": {"calle y altura": "street", "piso y departamento": "floor",
                         "punto": "location", "precisión": "geocode_precision",
                         "predeterminada": "isDefault"},
    "InvitacionRecompra": {"agotamiento estimado": "projected_depletion_at"},
    "Producto": {"tipo": "type", "peso en kilos": "weight", "precio": "price",
                 "stock": "stock", "activo": "isActive"},
    "Promocion": {"cantidad": "quantity", "descuento": "discount_percentage"},
    "Envase": {"número de serie": "serial", "estado": "state", "depósito": "deposit",
               "/vencimiento": "expires_at"},
    "MovimientoEnvase": {"desde": "from_state", "hacia": "to_state", "fecha": "createdAt"},
    "RevisionEnvase": {"fecha": "inspected_at", "resultado": "result",
                       "próxima revisión": "next_due_at"},
    "CasoRecupero": {"escalón": "step", "depósito comprometido": "deposit_amount",
                     "estado": "status", "resolución": "resolution_note"},
    "AvisoRecupero": {"escalón": "step", "tipo": "kind", "vence": "expires_at"},
    "Carrito": {"última modificación": "updated_at"},
    "ItemCarrito": {"cantidad": "quantity", "precio unitario": "unit_price"},
    "Pedido": {"estado": "status", "/total": "totalAmount",
               "modalidad de entrega": "delivery_mode", "fecha agendada": "scheduled_date",
               "método de pago": "paymentMethod", "seña": "deposit_amount",
               "código de entrega": "deliveryCode", "nombre de quien recibe": "receiver_name",
               "documento de quien recibe": "receiver_document",
               "vínculo con quien recibe": "receiver_relationship"},
    "ItemPedido": {"cantidad": "quantity", "precio unitario": "unitPrice", "/subtotal": "subtotal"},
    "CambioEstadoPedido": {"desde": "from_status", "hacia": "to_status", "motivo": "reason",
                           "fecha": "changed_at"},
    "CambioDireccion": {"motivo": "reason", "fecha": "changed_at"},
    "ZonaCobertura": {"nombre": "name", "área": "area", "recargo": "surcharge_value",
                      "tipo de recargo": "surcharge_type", "vigente hasta": "valid_until"},
    "FranjaHoraria": {"desde": "startTime", "hasta": "endTime", "cupo": "capacity",
                      "activa": "isActive"},
    "Pago": {"importe": "amount", "pasarela": "gateway", "estado": "status",
             "es seña": "is_deposit", "fecha": "createdAt"},
    "OfertaDespacho": {"estado": "status", "vence": "expiresAt"},
    "LoteRecorrido": {"estado": "status", "/peso total": "total_weight_kg"},
    "ParadaLote": {"orden": "sequence"},
    "OfertaLote": {"estado": "status", "vence": "expires_at"},
    "Chofer": {"disponible": "isAvailable", "habilitado": "isEnabled", "validado": "validated",
               "/calificación": "calification"},
    "Vehiculo": {"patente": "car_patent", "tipo": "type_car", "carga máxima": "max_load_kg",
                 "kilometraje": "odometer_km", "estado en la flota": "fleet_status"},
    "AsignacionVehiculo": {"asignado el": "assigned_at", "liberado el": "released_at",
                           "nota": "note"},
    "PlanMantenimiento": {"nombre": "name", "disparo": "trigger", "intervalo": "interval_km",
                          "anticipación": "lead_time_days", "criticidad": "criticality"},
    "TareaMantenimiento": {"estado": "status", "vence": "due_at",
                           "vencimiento proyectado": "predicted_due_at",
                           "prestador": "provider", "número": "reference_number",
                           "costo": "cost"},
    "AdjuntoTarea": {"nombre original": "original_name", "tipo de archivo": "mime_type",
                     "fecha de carga": "uploaded_at"},
    "PropuestaVentanaTaller": {"estado": "status", "vence": "expires_at",
                               "desde": "window_start", "hasta": "window_end"},
    "RegistroUsoVehiculo": {"día": "day", "kilómetros": "km", "pedidos": "orders"},
    "Reclamo": {"motivo": "reason", "descripción": "description", "estado": "status",
                "resolución": "resolutionNote", "fotografía": "photoUrl"},
    "Incidencia": {"tipo": "type", "momento": "moment", "descripción": "description",
                   "estado": "status", "resolución": "resolution_note",
                   "fotografía": "photo_url"},
    "Calificacion": {"puntaje": "stars", "comentario": "comment"},
}
# Las especializaciones heredan los atributos de su concepto abstracto: en la
# base cada tabla trae su propia columna.
HEREDA_ATRIBUTOS = {"estado": "status", "vence": "expires_at"}

# ------------------------------------------------------ MC <-> modelo de datos
CONCEPTO_DE_TABLA = {t: c for c, t in TABLA.items() if t}

# Los perfiles son especializaciones de Usuario: una relación de la base contra
# `user` puede sostener la asociación de cualquiera de ellos.
ANCESTROS = {"Cliente": {"Cliente", "Usuario"}, "Chofer": {"Chofer", "Usuario"},
             "Administrador": {"Administrador", "Usuario"}}

def _anc(c):
    return ANCESTROS.get(c, {c})

# Dos claves foráneas distintas entre las mismas tablas: el nombre de la
# asociación depende de la columna.
NOMBRE_POR_COLUMNA = {
    ("order_address_change", "from_address_id"): "cambia desde",
    ("order_address_change", "to_address_id"): "cambia hacia",
    ("rating", "from_user_id"): "emite",
    ("rating", "to_user_id"): "recibe",
    ("maintenance_task", "car_id"): "habilita",
    ("maintenance_task", "delivery_id"): "habilita",
    ("cylinder_recovery_case", "user_id"): "se abre contra",
    ("cylinder_recovery_case", "resolved_by_user_id"): "resuelve",
    ("car", "user_id"): "tiene registrado",
    ("vehicle_assignment", "delivery_id"): "usa",
    ("vehicle_assignment", "car_id"): "usa",
}

# Columnas que sólo dicen quién hizo algo: no son asociaciones del dominio.
AUTORIA_TECNICA = {("maintenance_task_attachment", "uploaded_by_user_id"),
                   ("module_config", "updated_by_user_id"),
                   ("vehicle_assignment", "assigned_by_user_id"),
                   ("vehicle_assignment", "released_by_user_id")}

def asociacion_de_fk(tabla, col, destino):
    """La asociación del modelo conceptual que sostiene una clave foránea, o None
    (relación técnica: pertenencia a la distribuidora, autoría de un cambio)."""
    ct, cd = CONCEPTO_DE_TABLA.get(tabla), CONCEPTO_DE_TABLA.get(destino)
    if not ct or not cd or (tabla, col) in AUTORIA_TECNICA:
        return None
    nombre = NOMBRE_POR_COLUMNA.get((tabla, col))
    if tabla == "vehicle_assignment" and col in ("delivery_id", "car_id"):
        # la clase de asociación sostiene la asociación Chofer-Vehiculo «usa»
        return next(a for a in ASOCIACIONES if a[5] == "usa")
    # una columna de perfil hacia `user` es la especialización, no una asociación
    if destino == "user" and tabla in ("admin", "customer", "delivery"):
        return ("ESPECIALIZACION", ct, cd)
    for a, ma, t, mb, b, n, cat in ASOCIACIONES:
        if nombre and n != nombre:
            continue
        if (ct in _anc(a) and cd in _anc(b)) or (ct in _anc(b) and cd in _anc(a)):
            # una asociación entre perfiles se sostiene con la clave del perfil
            # concreto, no con la de `user`
            return (a, ma, t, mb, b, n, cat)
    return None
