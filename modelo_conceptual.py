"""Modelo conceptual de SPLG, en una sola pieza.

Lo leen generar-modelo-conceptual.py (las vistas y la tabla de relaciones del
Documento 2), generar-drawio.py (el modelo conceptual en draw.io), generar-modelo-datos.py (el DER conceptual) y
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
    ("Personal", "Personal"),
    ("GastosDeFlota", "Gastos de la flota"),
    ("StockFisico", "Stock físico y carga del camión"),
    ("Compras", "Compras"),
    ("CajaYFinanzas", "Caja y finanzas"),
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
_c("ConfiguracionModulo", "OrganizacionYAcceso",
   ["módulo", "parámetros", "exigir carga de camión abierta"])
_c("AsientoAuditoria", "OrganizacionYAcceso",
   ["operación", "recurso", "aplicación", "resultado", "cambios", "fecha"])
_c("Auditoria", "OrganizacionYAcceso",
   ["entidad afectada", "fecha y hora"])
_c("DetalleAuditoria", "OrganizacionYAcceso", ["campo", "valor anterior", "valor nuevo"])
_c("TipoAccionAuditoria", "OrganizacionYAcceso", ["nombre"])

_c("Cliente", "Clientes", ["consumo mensual declarado", "días de aviso"])
_c("DireccionEntrega", "Clientes",
   ["calle y altura", "piso y departamento", "punto", "precisión", "predeterminada"])
_c("InvitacionRecompra", "Clientes", ["agotamiento estimado"])
_c("ItemSugerido", "Clientes", ["cantidad"])

_c("Producto", "CatalogoEInventario",
   ["tipo", "peso en kilos", "precio", "stock", "activo", "costo promedio", "déficit de reservas"])
_c("Promocion", "CatalogoEInventario", ["cantidad", "descuento"])
_c("Envase", "CatalogoEInventario", ["número de serie", "estado", "monto del depósito", "/vencimiento"])
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
    "vínculo con quien recibe", "estado del cobro", "cobro confirmado el",
    "cobro resuelto el", "nota de resolución del cobro"])
_c("ItemPedido", "VentaYPedidos", ["cantidad", "precio unitario", "/subtotal"])
_c("CambioEstadoPedido", "VentaYPedidos", ["desde", "hacia", "motivo", "fecha"])
_c("CambioDireccion", "VentaYPedidos", ["motivo", "fecha"])
_c("ZonaCobertura", "VentaYPedidos",
   ["nombre", "área", "recargo", "tipo de recargo", "prioridad", "vigente desde", "vigente hasta", "activa"])
_c("FranjaHoraria", "VentaYPedidos", ["desde", "hasta", "cupo", "activa"])

_c("Pago", "Pagos", ["importe", "pasarela", "estado", "es seña", "fecha"])

_c("PropuestaConVigencia", "DespachoYLogistica", ["estado", "vence"], abstracta=True)
_c("OfertaDespacho", "DespachoYLogistica")
_c("LoteRecorrido", "DespachoYLogistica", ["estado", "/peso total"])
_c("ParadaLote", "DespachoYLogistica", ["orden"])
_c("OfertaLote", "DespachoYLogistica")

_c("Chofer", "FlotaYChoferes", ["disponible", "habilitado", "validado", "/calificación"])
_c("Vehiculo", "FlotaYChoferes",
   ["patente", "tipo", "carga máxima", "kilometraje", "estado en la flota", "tipo de combustible",
    "capacidad del tanque"])
_c("AsignacionVehiculo", "FlotaYChoferes", ["asignado el", "liberado el", "nota"])
_c("PlanMantenimiento", "FlotaYChoferes",
   ["nombre", "disparo", "intervalo", "anticipación", "criticidad", "documento que controla", "aplica a"])
_c("TareaMantenimiento", "FlotaYChoferes",
   ["estado", "vence", "vencimiento proyectado", "prestador", "número", "costo", "vigente desde", "detalle"])
_c("AdjuntoTarea", "FlotaYChoferes", ["nombre original", "tipo de archivo", "fecha de carga"])
_c("PropuestaVentanaTaller", "FlotaYChoferes", ["desde", "hasta"])
_c("UbicacionGPS", "FlotaYChoferes", ["latitud", "longitud"])
_c("RegistroUsoVehiculo", "FlotaYChoferes", ["día", "kilómetros", "pedidos"])

_c("PuestoDeTrabajo", "Personal", ["nombre", "categoría", "activo"])
_c("Empleado", "Personal",
   ["legajo", "nombre", "apellido", "documento", "CUIL", "fecha de nacimiento", "domicilio", "teléfono",
    "contacto de emergencia", "fecha de ingreso", "fecha de egreso", "motivo de egreso",
    "modalidad de contratación", "estado"])
_c("JornadaDeTrabajo", "Personal", ["día", "ingreso", "egreso", "origen", "observación"])
_c("LicenciaLaboral", "Personal", ["tipo", "desde", "hasta", "/días", "estado", "motivo", "motivo de rechazo", "resuelta el"])
_c("Adjunto", "Personal", ["nombre original", "tipo de archivo", "etiqueta", "fecha de carga"])

_c("CargaCombustible", "GastosDeFlota",
   ["fecha y hora", "tipo de combustible", "litros", "precio por litro", "importe", "kilometraje",
    "tanque lleno", "estación", "medio de pago", "comprobante", "anómala", "observación", "anulada el"])
_c("MultaTransito", "GastosDeFlota",
   ["fecha de la infracción", "jurisdicción", "número de acta", "infracción", "importe",
    "importe con pago voluntario", "vencimiento", "estado", "pagada el", "importe pagado",
    "imputada al chofer", "avisada el", "motivo de anulación"])
_c("Siniestro", "GastosDeFlota",
   ["fecha", "ubicación", "domicilio", "descripción", "hubo heridos", "hubo terceros", "derrame de GLP",
    "denuncia policial", "reclamo al seguro", "estado", "vehículo inutilizable", "costo de reparación",
    "reintegro del seguro", "franquicia", "cerrado el"])
_c("Neumatico", "GastosDeFlota",
   ["número de serie", "marca", "medida", "costo", "estado", "posición", "kilometraje de montaje"])
_c("MovimientoNeumatico", "GastosDeFlota", ["tipo", "kilometraje", "fecha"])

_c("Reclamo", "Posventa", ["motivo", "descripción", "estado", "resolución", "fotografía"])
_c("Incidencia", "Posventa",
   ["tipo", "momento", "descripción", "estado", "resolución", "fotografía"])
_c("Calificacion", "Posventa", ["puntaje", "comentario"])

# Stock físico, compras y carga del camión (implementados).
_c("Deposito", "StockFisico", ["nombre", "código", "tipo", "dirección", "predeterminado", "activo"])
_c("UbicacionDeStock", "StockFisico", ["tipo"])
_c("SaldoDeStock", "StockFisico", ["condición", "cantidad"])
_c("MovimientoDeStock", "StockFisico",
   ["cantidad", "condición de origen", "condición de destino", "motivo", "documento de origen",
    "observación", "fecha"])
_c("UmbralDeStock", "StockFisico", ["mínimo de llenas", "avisado el"])
_c("AjusteDeStock", "StockFisico", ["número", "motivo", "nota", "fecha"])
_c("ItemAjusteDeStock", "StockFisico", ["condición", "diferencia"])
_c("CargaDeCamion", "StockFisico",
   ["número", "día", "estado", "abierta el", "salió el", "regresó el", "cerrada el",
    "nota de diferencia", "motivo de cancelación", "notas"])
_c("ItemCarga", "StockFisico",
   ["llenas cargadas", "llenas repuestas", "vacías cargadas", "llenas declaradas al regreso",
    "vacías declaradas al regreso", "llenas entregadas", "vacías recolectadas",
    "/llenas esperadas", "/vacías esperadas", "diferencia de llenas", "diferencia de vacías"])

_c("Proveedor", "Compras",
   ["razón social", "CUIT", "tipo", "contacto", "teléfono", "correo", "dirección",
    "plazo de pago", "activo"])
_c("OrdenDeCompra", "Compras",
   ["número", "estado", "emitida el", "fecha esperada", "total", "motivo de cancelación",
    "motivo de cierre", "notas"])
_c("ItemOrdenDeCompra", "Compras",
   ["cantidad", "costo unitario", "vacíos a canjear", "cantidad recibida"])
_c("RecepcionDeCompra", "Compras",
   ["número", "tipo de comprobante", "número de comprobante", "recibida el", "total",
    "estado de pago", "estado", "motivo de anulación", "anulada el", "notas"])
_c("ItemRecepcion", "Compras",
   ["llenas recibidas", "vacías entregadas", "costo unitario", "costo promedio previo",
    "existencia previa", "existencia previa leída el"])
_c("Caja", "CajaYFinanzas", ["nombre", "tipo", "saldo", "requiere sesión", "activa"])
_c("SesionDeCaja", "CajaYFinanzas",
   ["estado", "abierta el", "monto inicial", "cerrada el", "monto esperado", "monto contado",
    "diferencia", "observaciones"])
_c("CategoriaDeCaja", "CajaYFinanzas", ["nombre", "sentido", "código de sistema", "activa"])
_c("MovimientoDeCaja", "CajaYFinanzas",
   ["sentido", "importe", "medio", "fecha", "descripción", "origen"])
_c("RendicionChofer", "CajaYFinanzas",
   ["número", "fecha de negocio", "estado", "efectivo esperado", "efectivo declarado",
    "/gastos del chofer", "/diferencia", "resolución de la diferencia", "presentada el",
    "aprobada el", "observaciones", "aviso enviado el"])
_c("PedidoRendido", "CajaYFinanzas", ["importe", "medio de pago"])
_c("GastoDeRendicion", "CajaYFinanzas", ["importe", "descripción"])
_c("CuentaCorriente", "CajaYFinanzas",
   ["razón social", "CUIT", "condición fiscal", "límite de crédito", "plazo de pago en días",
    "estado", "saldo"])
_c("AsientoCuentaCorriente", "CajaYFinanzas",
   ["tipo", "importe", "vence", "medio de pago", "fecha", "descripción"])
_c("ImputacionCuentaCorriente", "CajaYFinanzas", ["importe"])
_c("ReglaComision", "CajaYFinanzas", ["base", "valor", "vigente desde", "vigente hasta", "activa"])
_c("AsientoComision", "CajaYFinanzas", ["tipo", "importe", "fecha", "descripción"])
_c("LiquidacionComisiones", "CajaYFinanzas",
   ["número", "período desde", "período hasta", "bruto", "deducciones", "neto", "estado",
    "aprobada el", "pagada el"])

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
    ("Distribuidora", "1", "-", "0..*", "Empleado", "emplea", EM),
    ("Distribuidora", "1", "*", "0..*", "PuestoDeTrabajo", "define", PL),
    ("Distribuidora", "1", "-", "0..*", "Producto", "comercializa", UG),
    ("Distribuidora", "1", "-", "0..*", "Envase", "posee", PR),
    ("Distribuidora", "1", "-", "0..*", "Pedido", "gestiona", UG),
    ("Distribuidora", "1", "*", "0..*", "ZonaCobertura", "define", PL),
    ("Distribuidora", "1", "*", "0..*", "FranjaHoraria", "define", PL),
    ("Distribuidora", "1", "*", "0..*", "ConfiguracionModulo", "parametriza", DE),
    ("Usuario", "0..1", "-", "0..*", "AsientoAuditoria", "origina", RG),
    ("Usuario", "0..1", "-", "0..*", "Auditoria", "realiza", RG),
    ("Distribuidora", "0..1", "-", "0..*", "Auditoria", "delimita", RG),
    ("Auditoria", "1", "*", "0..*", "DetalleAuditoria", "detalla con", LT),
    ("TipoAccionAuditoria", "1", "-", "0..*", "Auditoria", "clasifica", DE),

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
    ("Usuario", "0..1", "-", "0..*", "Pedido", "confirmó el cobro de", TR),
    ("Usuario", "0..1", "-", "0..*", "Pedido", "resolvió el cobro de", TR),
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

    ("Empleado", "0..*", "-", "1", "PuestoDeTrabajo", "ocupa", DE),
    ("Empleado", "0..1", "-", "0..1", "Usuario", "accede con", UG),
    ("Empleado", "1", "*", "0..*", "JornadaDeTrabajo", "registra", RG),
    ("Empleado", "1", "*", "0..*", "LicenciaLaboral", "solicita", TR),
    ("Usuario", "0..1", "-", "0..*", "LicenciaLaboral", "resuelve", TR),
    ("Empleado", "1", "*", "0..*", "Adjunto", "conserva", PL),
    ("TareaMantenimiento", "0..*", "-", "0..1", "Empleado", "habilita", TR),
    ("Vehiculo", "1", "*", "0..*", "CargaCombustible", "registra", RG),
    ("Vehiculo", "1", "*", "0..*", "MultaTransito", "acumula", RG),
    ("Vehiculo", "1", "*", "0..*", "Siniestro", "sufre", RG),
    ("Vehiculo", "0..1", "-", "0..*", "Neumatico", "monta", UG),
    ("Distribuidora", "1", "*", "0..*", "Neumatico", "posee", PR),
    ("Neumatico", "1", "*", "0..*", "MovimientoNeumatico", "registra", RG),
    ("MovimientoNeumatico", "0..*", "-", "0..1", "Vehiculo", "ocurre en", TR),
    ("Empleado", "0..1", "-", "0..*", "CargaCombustible", "carga", TR),
    ("Empleado", "0..1", "-", "0..*", "MultaTransito", "responde por", TR),
    ("Empleado", "0..1", "-", "0..*", "Siniestro", "interviene en", TR),

    ("Pedido", "1", "-", "0..*", "Reclamo", "origina", TR),
    ("Cliente", "1", "-", "0..*", "Reclamo", "presenta", TR),
    ("Pedido", "1", "-", "0..*", "Incidencia", "origina", TR),
    ("Usuario", "1", "-", "0..*", "Incidencia", "reporta", TR),
    ("Pedido", "1", "-", "0..2", "Calificacion", "recibe", TR),
    ("Usuario", "1", "-", "0..*", "Calificacion", "emite", TR),
    ("Usuario", "1", "-", "0..*", "Calificacion", "recibe", TR),

    # Stock físico, compras y carga del camión (implementados)
    ("Distribuidora", "1", "-", "0..*", "Deposito", "dispone de", PR),
    ("Distribuidora", "1", "-", "0..*", "Proveedor", "compra a", UG),
    ("Deposito", "1", "-", "0..1", "UbicacionDeStock", "se registra como {xor}", DE),
    ("Vehiculo", "1", "-", "0..1", "UbicacionDeStock", "se registra como {xor}", DE),
    ("UbicacionDeStock", "1", "*", "0..*", "SaldoDeStock", "acumula", RG),
    ("SaldoDeStock", "0..*", "-", "1", "Producto", "corresponde a", DE),
    ("MovimientoDeStock", "0..*", "-", "1", "Producto", "corresponde a", DE),
    ("MovimientoDeStock", "0..*", "-", "0..1", "UbicacionDeStock", "sale de", TR),
    ("MovimientoDeStock", "0..*", "-", "0..1", "UbicacionDeStock", "entra en", TR),
    ("Usuario", "0..1", "-", "0..*", "MovimientoDeStock", "ejecuta", TR),
    ("Deposito", "1", "*", "0..*", "UmbralDeStock", "fija", PL),
    ("UmbralDeStock", "0..*", "-", "1", "Producto", "controla", DE),
    ("UbicacionDeStock", "1", "-", "0..*", "AjusteDeStock", "se corrige con", TR),
    ("AjusteDeStock", "1", "*", "1..*", "ItemAjusteDeStock", "contiene", LT),
    ("ItemAjusteDeStock", "0..*", "-", "1", "Producto", "corresponde a", DE),
    ("Usuario", "1", "-", "0..*", "AjusteDeStock", "registra", TR),
    ("MovimientoDeStock", "0..1", "-", "0..1", "MovimientoDeStock", "corrige a", TR),
    ("Proveedor", "1", "-", "0..*", "OrdenDeCompra", "recibe", TR),
    ("OrdenDeCompra", "0..*", "-", "1", "Deposito", "se destina a", TR),
    ("OrdenDeCompra", "1", "*", "1..*", "ItemOrdenDeCompra", "contiene", LT),
    ("ItemOrdenDeCompra", "0..*", "-", "1", "Producto", "corresponde a", DE),
    ("Usuario", "1", "-", "0..*", "OrdenDeCompra", "emite", TR),
    ("Proveedor", "1", "-", "0..*", "RecepcionDeCompra", "entrega", TR),
    ("OrdenDeCompra", "0..1", "-", "0..*", "RecepcionDeCompra", "se cumple con", TR),
    ("RecepcionDeCompra", "0..*", "-", "1", "Deposito", "ingresa en", TR),
    ("RecepcionDeCompra", "1", "*", "1..*", "ItemRecepcion", "contiene", LT),
    ("ItemRecepcion", "0..*", "-", "1", "Producto", "corresponde a", DE),
    ("Usuario", "1", "-", "0..*", "RecepcionDeCompra", "registra", TR),
    ("Vehiculo", "1", "-", "0..*", "CargaDeCamion", "transporta", TR),
    ("Chofer", "1", "-", "0..*", "CargaDeCamion", "reparte con", TR),
    ("CargaDeCamion", "0..*", "-", "1", "UbicacionDeStock", "parte de", TR),
    ("CargaDeCamion", "1", "*", "1..*", "ItemCarga", "contiene", LT),
    ("ItemCarga", "0..*", "-", "1", "Producto", "corresponde a", DE),
    ("Usuario", "1", "-", "0..*", "CargaDeCamion", "abre", TR),
    ("Usuario", "0..1", "-", "0..*", "CargaDeCamion", "cierra", TR),
    ("Empleado", "0..1", "-", "0..*", "CargaDeCamion", "ayuda en", TR),
    # Caja y finanzas (módulo planificado, iteración I-14)
    ("Distribuidora", "1", "*", "0..*", "Caja", "define", PL),
    ("Distribuidora", "1", "*", "0..*", "CategoriaDeCaja", "define", PL),
    ("Distribuidora", "1", "*", "0..*", "CuentaCorriente", "lleva", PL),
    ("Distribuidora", "1", "*", "0..*", "ReglaComision", "define", PL),
    ("Caja", "1", "*", "0..*", "SesionDeCaja", "registra", RG),
    ("Caja", "1", "*", "0..*", "MovimientoDeCaja", "asienta", RG),
    ("SesionDeCaja", "0..1", "-", "0..*", "MovimientoDeCaja", "agrupa", TR),
    ("CategoriaDeCaja", "1", "-", "0..*", "MovimientoDeCaja", "clasifica", DE),
    ("MovimientoDeCaja", "0..1", "-", "0..1", "MovimientoDeCaja", "anula a", TR),
    ("Usuario", "1", "-", "0..*", "MovimientoDeCaja", "registró", TR),
    ("Chofer", "1", "*", "0..*", "RendicionChofer", "presenta", TR),
    ("RendicionChofer", "0..*", "-", "0..1", "Caja", "ingresa en", TR),
    ("RendicionChofer", "0..1", "-", "0..1", "MovimientoDeCaja", "genera", TR),
    ("RendicionChofer", "1", "*", "0..*", "PedidoRendido", "rinde", LT),
    ("PedidoRendido", "0..1", "-", "1", "Pedido", "corresponde a", DE),
    ("RendicionChofer", "1", "*", "0..*", "GastoDeRendicion", "declara", LT),
    ("GastoDeRendicion", "0..*", "-", "1", "CategoriaDeCaja", "se clasifica en", DE),
    ("Cliente", "1", "-", "0..*", "CuentaCorriente", "tiene habilitada", UG),
    ("CuentaCorriente", "1", "*", "0..*", "AsientoCuentaCorriente", "registra", RG),
    ("Pedido", "0..1", "-", "0..*", "AsientoCuentaCorriente", "origina", TR),
    ("AsientoCuentaCorriente", "0..1", "-", "0..1", "MovimientoDeCaja", "se asienta en", TR),
    ("Chofer", "0..1", "-", "0..*", "AsientoCuentaCorriente", "cobra", TR),
    ("RendicionChofer", "0..1", "-", "0..*", "AsientoCuentaCorriente", "incluye", TR),
    ("AsientoCuentaCorriente", "0..1", "-", "0..1", "AsientoCuentaCorriente", "anula a", TR),
    ("ImputacionCuentaCorriente", "0..*", "-", "1", "AsientoCuentaCorriente", "salda", TR),
    ("ImputacionCuentaCorriente", "0..*", "-", "1", "AsientoCuentaCorriente", "se aplica con", TR),
    ("ReglaComision", "0..*", "-", "0..1", "Empleado", "se aplica a", DE),
    ("ReglaComision", "0..*", "-", "0..1", "Producto", "se aplica a", DE),
    ("Empleado", "1", "*", "0..*", "AsientoComision", "devenga", RG),
    ("Empleado", "1", "*", "0..*", "LiquidacionComisiones", "percibe", TR),
    ("Empleado", "0..1", "-", "0..1", "Chofer", "actúa como", UG),
    ("AsientoComision", "0..*", "-", "0..1", "Pedido", "corresponde a", DE),
    ("ReglaComision", "0..1", "-", "0..*", "AsientoComision", "determina", TR),
    ("LiquidacionComisiones", "0..1", "-", "0..*", "AsientoComision", "incluye", TR),
    ("RendicionChofer", "0..1", "-", "0..*", "AsientoComision", "origina", TR),
    ("LiquidacionComisiones", "0..1", "-", "0..1", "MovimientoDeCaja", "se paga con", TR),
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
      "AsientoAuditoria", "Auditoria", "DetalleAuditoria", "TipoAccionAuditoria",
      "Cliente", "DireccionEntrega", "InvitacionRecompra", "ItemSugerido"],
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
    ("Personal", "MC_Personal",
     ["PuestoDeTrabajo", "Empleado", "JornadaDeTrabajo", "LicenciaLaboral", "Adjunto"],
     ["Distribuidora", "Usuario", "TareaMantenimiento"]),
    ("Posventa", "MC_Posventa",
     ["Calificacion", "Incidencia", "Reclamo"],
     ["Usuario", "Pedido", "Cliente"]),
    ("Gastos de la flota", "MC_Gastos-de-flota",
     ["CargaCombustible", "MultaTransito", "Siniestro", "Neumatico", "MovimientoNeumatico"],
     ["Vehiculo", "Empleado", "Distribuidora"]),
    ("Stock físico", "MC_Stock",
     ["Deposito", "UbicacionDeStock", "SaldoDeStock", "MovimientoDeStock", "UmbralDeStock",
      "AjusteDeStock", "ItemAjusteDeStock"],
     ["Producto", "Vehiculo", "Usuario", "Distribuidora"]),
    ("Carga del camión", "MC_Carga-del-camion",
     ["CargaDeCamion", "ItemCarga"],
     ["Vehiculo", "Chofer", "UbicacionDeStock", "Producto", "Usuario"]),
    ("Compras", "MC_Compras",
     ["Proveedor", "OrdenDeCompra", "ItemOrdenDeCompra", "RecepcionDeCompra", "ItemRecepcion"],
     ["Deposito", "Producto", "Usuario", "Distribuidora"]),
    ("Caja y movimientos", "MC_Caja",
     ["Caja", "SesionDeCaja", "CategoriaDeCaja", "MovimientoDeCaja"],
     ["Distribuidora", "Usuario", "RendicionChofer", "AsientoCuentaCorriente", "LiquidacionComisiones"]),
    ("Rendiciones de choferes", "MC_Rendiciones",
     ["RendicionChofer", "PedidoRendido", "GastoDeRendicion"],
     ["Chofer", "Pedido", "Caja", "MovimientoDeCaja", "CategoriaDeCaja", "AsientoCuentaCorriente",
      "AsientoComision"]),
    ("Cuentas corrientes", "MC_Cuentas-corrientes",
     ["CuentaCorriente", "AsientoCuentaCorriente", "ImputacionCuentaCorriente"],
     ["Cliente", "Distribuidora", "Pedido", "MovimientoDeCaja", "Chofer", "RendicionChofer"]),
    ("Comisiones y liquidaciones", "MC_Comisiones",
     ["Empleado", "ReglaComision", "AsientoComision", "LiquidacionComisiones"],
     ["Chofer", "Producto", "Pedido", "MovimientoDeCaja", "Distribuidora", "RendicionChofer"]),
]

# -------------------------------------------------------- correspondencia con la BD
# concepto -> tabla del modelo de datos. None: el concepto no tiene tabla propia y
# se explica en OBSERVACION.
TABLA = {
    "Distribuidora": "distributor", "Usuario": "user", "Rol": "role",
    "Administrador": "admin", "ConfiguracionModulo": "module_config",
    "AsientoAuditoria": "audit_log", "Auditoria": "audit", "DetalleAuditoria": "audit_detail",
    "TipoAccionAuditoria": "audit_action_type", "Cliente": "customer",
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
    "PuestoDeTrabajo": "job_position", "Empleado": "employee", "JornadaDeTrabajo": "employee_attendance",
    "LicenciaLaboral": "employee_leave", "Adjunto": "attachment",
    "CargaCombustible": "fuel_load", "MultaTransito": "traffic_fine",
    "Siniestro": "vehicle_accident", "Neumatico": "tire", "MovimientoNeumatico": "tire_event",
    # Stock físico, compras y carga del camión (implementados)
    "Deposito": "warehouse", "UbicacionDeStock": "stock_location",
    "SaldoDeStock": "stock_balance", "MovimientoDeStock": "stock_movement",
    "UmbralDeStock": "stock_threshold", "AjusteDeStock": "stock_adjustment",
    "ItemAjusteDeStock": "stock_adjustment_item",
    "CargaDeCamion": "truck_load",
    "ItemCarga": "truck_load_item", "Proveedor": "supplier", "OrdenDeCompra": "purchase_order",
    "ItemOrdenDeCompra": "purchase_order_item", "RecepcionDeCompra": "purchase_receipt",
    "ItemRecepcion": "purchase_receipt_item",
    # Caja y rendición (planificado, I-14)
    "Caja": "cash_box", "SesionDeCaja": "cash_session", "CategoriaDeCaja": "cash_category",
    "MovimientoDeCaja": "cash_movement", "RendicionChofer": "driver_settlement",
    "PedidoRendido": "driver_settlement_order", "GastoDeRendicion": "driver_settlement_expense",
    "CuentaCorriente": "customer_account", "AsientoCuentaCorriente": "customer_account_entry",
    "ImputacionCuentaCorriente": "customer_account_allocation",
    "ReglaComision": "commission_rule", "AsientoComision": "commission_entry",
    "LiquidacionComisiones": "driver_liquidation",
}


# Conceptos de los módulos de gestión de la distribuidora que todavía no tienen tabla en la base
# (concepto -> iteración en que se construyen): las jornadas y licencias del personal (I-11; los puestos y los
# legajos ya están construidos), la flota ampliada (I-12), el stock y
# las compras (I-13) y la caja y rendición (I-14). Sus tablas están en `propuesto_personal.py`, `propuesto_flota.py` y la constante
# PROPUESTO de `generar-modelo-datos.py`. Todo lo que contrasta el modelo con la base los trata aparte.
PLANIFICADOS = {c: "I-11" for c in ("JornadaDeTrabajo", "LicenciaLaboral")}
PLANIFICADOS.update({c: "I-12" for c in ("CargaCombustible", "MultaTransito", "Siniestro", "Neumatico",
                                         "MovimientoNeumatico")})
PLANIFICADOS.update({c: "I-14" for c in (
    "Caja", "SesionDeCaja", "CategoriaDeCaja", "MovimientoDeCaja", "RendicionChofer",
    "PedidoRendido", "GastoDeRendicion", "CuentaCorriente", "AsientoCuentaCorriente",
    "ImputacionCuentaCorriente", "ReglaComision", "AsientoComision", "LiquidacionComisiones")})
# Atributos planificados de conceptos que ya existen: (concepto, atributo).
ATRIBUTOS_PLANIFICADOS = {("PlanMantenimiento", "documento que controla"): "I-11",
                          ("PlanMantenimiento", "aplica a"): "I-11",
                          ("TareaMantenimiento", "vigente desde"): "I-11", ("TareaMantenimiento", "detalle"): "I-11",
                          ("Vehiculo", "tipo de combustible"): "I-12", ("Vehiculo", "capacidad del tanque"): "I-12"}
# Módulo del backend de cada concepto planificado (y del Adjunto, que ya está implementado).
MODULO_PLANIFICADO = {"JornadaDeTrabajo": "employee", "LicenciaLaboral": "employee", "Adjunto": "attachment",
                      "CargaCombustible": "fleet-expense", "MultaTransito": "fleet-expense",
                      "Siniestro": "fleet-expense", "Neumatico": "fleet-expense",
                      "MovimientoNeumatico": "fleet-expense",
                      "Deposito": "stock", "UbicacionDeStock": "stock", "SaldoDeStock": "stock",
                      "MovimientoDeStock": "stock", "UmbralDeStock": "stock", "AjusteDeStock": "stock",
                      "ItemAjusteDeStock": "stock", "CargaDeCamion": "truck-load", "ItemCarga": "truck-load",
                      "Caja": "cash", "SesionDeCaja": "cash", "CategoriaDeCaja": "cash", "MovimientoDeCaja": "cash",
                      "RendicionChofer": "driver-settlement", "PedidoRendido": "driver-settlement",
                      "GastoDeRendicion": "driver-settlement", "CuentaCorriente": "customer-account",
                      "AsientoCuentaCorriente": "customer-account", "ImputacionCuentaCorriente": "customer-account",
                      "ReglaComision": "commission", "AsientoComision": "commission",
                      "LiquidacionComisiones": "commission"}
# Tipo de cada atributo planificado, para el diagrama de clases de diseño: el código no lo tiene todavía.
TIPOS_PLANIFICADOS = {
    ("Vehiculo", "tipo de combustible"): "TipoDeCombustible",
    ("Vehiculo", "capacidad del tanque"): "Decimal",
    ("TareaMantenimiento", "vigente desde"): "Fecha", ("TareaMantenimiento", "detalle"): "Registro",
    ("TareaMantenimiento", "vence"): "Fecha",
    ("MultaTransito", "motivo de anulación"): "Cadena",
    ("CargaCombustible", "fecha y hora"): "FechaHora",
    ("CargaCombustible", "tipo de combustible"): "TipoDeCombustible",
    ("CargaCombustible", "litros"): "Decimal", ("CargaCombustible", "precio por litro"): "Moneda",
    ("CargaCombustible", "importe"): "Moneda", ("CargaCombustible", "kilometraje"): "Entero",
    ("CargaCombustible", "tanque lleno"): "Booleano", ("CargaCombustible", "estación"): "Cadena",
    ("CargaCombustible", "medio de pago"): "MedioDePagoDeCombustible",
    ("CargaCombustible", "comprobante"): "Cadena", ("CargaCombustible", "anómala"): "Booleano",
    ("CargaCombustible", "observación"): "Cadena", ("CargaCombustible", "anulada el"): "FechaHora",
    ("MultaTransito", "fecha de la infracción"): "FechaHora", ("MultaTransito", "jurisdicción"): "Cadena",
    ("MultaTransito", "número de acta"): "Cadena", ("MultaTransito", "infracción"): "Cadena",
    ("MultaTransito", "importe"): "Moneda", ("MultaTransito", "importe con pago voluntario"): "Moneda",
    ("MultaTransito", "vencimiento"): "Fecha", ("MultaTransito", "estado"): "EstadoDeLaMulta",
    ("MultaTransito", "pagada el"): "FechaHora", ("MultaTransito", "importe pagado"): "Moneda",
    ("MultaTransito", "imputada al chofer"): "Booleano", ("MultaTransito", "avisada el"): "FechaHora",
    ("Siniestro", "fecha"): "FechaHora", ("Siniestro", "ubicación"): "Coordenada",
    ("Siniestro", "domicilio"): "Cadena", ("Siniestro", "descripción"): "Cadena",
    ("Siniestro", "hubo heridos"): "Booleano", ("Siniestro", "hubo terceros"): "Booleano",
    ("Siniestro", "derrame de GLP"): "Booleano", ("Siniestro", "denuncia policial"): "Cadena",
    ("Siniestro", "reclamo al seguro"): "Cadena", ("Siniestro", "estado"): "EstadoDelSiniestro",
    ("Siniestro", "vehículo inutilizable"): "Booleano", ("Siniestro", "costo de reparación"): "Moneda",
    ("Siniestro", "reintegro del seguro"): "Moneda", ("Siniestro", "franquicia"): "Moneda",
    ("Siniestro", "cerrado el"): "FechaHora",
    ("Neumatico", "número de serie"): "Cadena", ("Neumatico", "marca"): "Cadena",
    ("Neumatico", "medida"): "Cadena", ("Neumatico", "costo"): "Moneda",
    ("Neumatico", "estado"): "EstadoDelNeumatico", ("Neumatico", "posición"): "Cadena",
    ("Neumatico", "kilometraje de montaje"): "Entero",
    ("MovimientoNeumatico", "tipo"): "TipoDeMovimientoDeNeumatico",
    ("MovimientoNeumatico", "kilometraje"): "Entero", ("MovimientoNeumatico", "fecha"): "FechaHora",
}

# Asociaciones sin clave foránea propia que las sostenga (A, B, nombre): el dueño del adjunto es
# polimórfico (D3), y el empleado es un chofer a través del usuario que comparten (`employee.user_id` y
# `delivery.user_id`), no por una columna.
POLIMORFICAS = {("Empleado", "Adjunto", "conserva"), ("Empleado", "Chofer", "actúa como"),
                # `order.payment_confirmed_by` y `order.payment_resolved_by` guardan el usuario (uuid) sin
                # clave foránea declarada en la base
                ("Usuario", "Pedido", "confirmó el cobro de"), ("Usuario", "Pedido", "resolvió el cobro de")}

# Tablas que la base tiene y que no son un concepto del dominio: las usa la infraestructura del sistema.
# Se dibujan en el modelo físico (contexto «Tablas técnicas») y no entran en el modelo conceptual.
# nombre de la tabla -> (qué es, por qué no es un concepto).
TABLAS_TECNICAS = {
    "document_sequence": ("Secuencia de documentos",
                          "Último número asignado a cada tipo de documento, por distribuidora: un contador "
                          "para numerar comprobantes correlativos sin repetir ni saltear. Es un mecanismo, "
                          "no algo del negocio con identidad propia."),
    "stock_reconciliation_alert": ("Aviso de conciliación de stock",
                                   "Firma de la última diferencia de conciliación que se avisó a cada distribuidora, "
                                   "para no repetir el correo de la noche siguiente. Es un mecanismo del proceso "
                                   "nocturno, no algo del negocio con identidad propia."),
    "storage_orphan": ("Archivo pendiente de borrado",
                       "Cola de reintento del almacenamiento: la clave de un archivo que se subió o se "
                       "reemplazó y todavía hay que borrar del almacenamiento externo. Es una tarea de "
                       "mantenimiento del sistema, no un concepto del dominio."),
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
    "ConfiguracionModulo": {"módulo": "module", "parámetros": "params",
                            "exigir carga de camión abierta": "params"},
    "AsientoAuditoria": {"operación": "http_method", "recurso": "resource",
                         "aplicación": "client_source", "resultado": "result",
                         "cambios": "changes", "fecha": "created_at"},
    "Auditoria": {"entidad afectada": "entity", "fecha y hora": "created_at"},
    "DetalleAuditoria": {"campo": "field", "valor anterior": "old_value", "valor nuevo": "new_value"},
    "TipoAccionAuditoria": {"nombre": "name"},
    "Cliente": {"consumo mensual declarado": "avg_monthly_consumption_kg",
                "días de aviso": "repurchase_notice_days"},
    "DireccionEntrega": {"calle y altura": "street", "piso y departamento": "floor",
                         "punto": "location", "precisión": "geocode_precision",
                         "predeterminada": "isDefault"},
    "InvitacionRecompra": {"agotamiento estimado": "projected_depletion_at"},
    "Producto": {"tipo": "type", "peso en kilos": "weight", "precio": "price",
                 "stock": "stock", "activo": "isActive", "costo promedio": "average_unit_cost",
                 "déficit de reservas": "reservation_deficit"},
    "Promocion": {"cantidad": "quantity", "descuento": "discount_percentage"},
    "Envase": {"número de serie": "serial", "estado": "state", "monto del depósito": "deposit",
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
               "vínculo con quien recibe": "receiver_relationship",
               "estado del cobro": "paymentStatus", "cobro confirmado el": "payment_confirmed_at",
               "cobro resuelto el": "payment_resolved_at",
               "nota de resolución del cobro": "payment_resolution_note"},
    "ItemPedido": {"cantidad": "quantity", "precio unitario": "unitPrice", "/subtotal": "subtotal"},
    "CambioEstadoPedido": {"desde": "from_status", "hacia": "to_status", "motivo": "reason",
                           "fecha": "changed_at"},
    "CambioDireccion": {"motivo": "reason", "fecha": "changed_at"},
    "ZonaCobertura": {"nombre": "name", "área": "area", "recargo": "surcharge_value",
                      "tipo de recargo": "surcharge_type", "prioridad": "priority",
                      "vigente desde": "valid_from", "vigente hasta": "valid_until", "activa": "isActive"},
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
    "PuestoDeTrabajo": {"nombre": "name", "categoría": "category", "activo": "is_active"},
    "Empleado": {"legajo": "file_number", "nombre": "first_name", "apellido": "last_name",
                 "documento": "document_number", "CUIL": "cuil", "fecha de nacimiento": "birth_date",
                 "domicilio": "address_line", "teléfono": "phone",
                 "contacto de emergencia": "emergency_contact_name", "fecha de ingreso": "hire_date",
                 "fecha de egreso": "termination_date", "motivo de egreso": "termination_reason",
                 "modalidad de contratación": "employment_type", "estado": "status"},
    "JornadaDeTrabajo": {"día": "work_date", "ingreso": "check_in_at", "egreso": "check_out_at",
                         "origen": "source", "observación": "notes"},
    "LicenciaLaboral": {"tipo": "type", "desde": "start_date", "hasta": "end_date", "/días": "days",
                        "estado": "status", "motivo": "reason", "motivo de rechazo": "rejection_reason",
                        "resuelta el": "decided_at"},
    "Adjunto": {"nombre original": "original_name", "tipo de archivo": "mime_type", "etiqueta": "label",
                "fecha de carga": "uploaded_at"},
    "CargaCombustible": {"fecha y hora": "loaded_at", "tipo de combustible": "fuel_type",
                         "litros": "liters", "precio por litro": "unit_price", "importe": "total_amount",
                         "kilometraje": "odometer_km", "tanque lleno": "is_full_tank",
                         "estación": "station", "medio de pago": "payment_method",
                         "comprobante": "receipt_number", "anómala": "anomaly",
                         "observación": "notes", "anulada el": "deletedAt"},
    "MultaTransito": {"fecha de la infracción": "occurred_at", "jurisdicción": "jurisdiction",
                      "número de acta": "act_number", "infracción": "infraction", "importe": "amount",
                      "importe con pago voluntario": "voluntary_payment_amount",
                      "vencimiento": "due_date", "estado": "status", "pagada el": "paid_at",
                      "importe pagado": "paid_amount", "imputada al chofer": "charged_to_employee",
                      "avisada el": "alerted_at", "motivo de anulación": "void_reason"},
    "Siniestro": {"fecha": "occurred_at", "ubicación": "location", "domicilio": "address",
                  "descripción": "description", "hubo heridos": "injuries",
                  "hubo terceros": "third_parties_involved", "derrame de GLP": "hazmat_release",
                  "denuncia policial": "police_report_number",
                  "reclamo al seguro": "insurer_claim_number", "estado": "status",
                  "vehículo inutilizable": "vehicle_unusable", "costo de reparación": "repair_cost",
                  "reintegro del seguro": "insurer_reimbursement", "franquicia": "deductible_amount",
                  "cerrado el": "closed_at"},
    "Neumatico": {"número de serie": "serial", "marca": "brand", "medida": "size", "costo": "cost",
                  "estado": "status", "posición": "position",
                  "kilometraje de montaje": "mounted_odometer_km"},
    "MovimientoNeumatico": {"tipo": "event_type", "kilometraje": "odometer_km", "fecha": "occurred_at"},
    # Stock físico, compras y carga del camión (implementados)
    "Deposito": {"nombre": "name", "código": "code", "tipo": "kind", "dirección": "address",
                 "predeterminado": "is_default", "activo": "is_active"},
    "UbicacionDeStock": {"tipo": "kind"},
    "SaldoDeStock": {"condición": "condition", "cantidad": "quantity"},
    "MovimientoDeStock": {"cantidad": "quantity", "condición de origen": "from_condition",
                          "condición de destino": "to_condition", "motivo": "reason",
                          "documento de origen": "reference_type", "observación": "notes",
                          "fecha": "occurred_at"},
    "UmbralDeStock": {"mínimo de llenas": "min_full", "avisado el": "alerted_at"},
    "AjusteDeStock": {"número": "number", "motivo": "reason", "nota": "notes", "fecha": "createdAt"},
    "ItemAjusteDeStock": {"condición": "condition", "diferencia": "quantity_delta"},
    "CargaDeCamion": {"número": "number", "día": "business_date", "estado": "status",
                      "abierta el": "opened_at", "salió el": "departed_at",
                      "regresó el": "returned_at", "cerrada el": "closed_at",
                      "nota de diferencia": "difference_note",
                      "motivo de cancelación": "cancel_reason", "notas": "notes"},
    "ItemCarga": {"llenas cargadas": "loaded_full", "llenas repuestas": "reloaded_full",
                  "vacías cargadas": "loaded_empty",
                  "llenas declaradas al regreso": "declared_return_full",
                  "vacías declaradas al regreso": "declared_return_empty",
                  "llenas entregadas": "delivered_full", "vacías recolectadas": "collected_empty",
                  "/llenas esperadas": "expected_full", "/vacías esperadas": "expected_empty",
                  "diferencia de llenas": "difference_full",
                  "diferencia de vacías": "difference_empty"},
    "Proveedor": {"razón social": "business_name", "CUIT": "cuit", "tipo": "kind",
                  "contacto": "contact_name", "teléfono": "phone", "correo": "email",
                  "dirección": "address", "plazo de pago": "payment_terms_days",
                  "activo": "is_active"},
    "OrdenDeCompra": {"número": "number", "estado": "status", "emitida el": "issued_at",
                      "fecha esperada": "expected_date", "total": "total_amount",
                      "motivo de cancelación": "cancel_reason", "motivo de cierre": "close_reason",
                      "notas": "notes"},
    "ItemOrdenDeCompra": {"cantidad": "quantity", "costo unitario": "unit_cost",
                          "vacíos a canjear": "empties_to_exchange",
                          "cantidad recibida": "received_quantity"},
    "RecepcionDeCompra": {"número": "number", "tipo de comprobante": "supplier_document_type",
                          "número de comprobante": "supplier_document_number",
                          "recibida el": "received_at", "total": "total_amount",
                          "estado de pago": "payment_status", "estado": "status",
                          "motivo de anulación": "void_reason", "anulada el": "voided_at",
                          "notas": "notes"},
    "ItemRecepcion": {"llenas recibidas": "quantity_full", "vacías entregadas": "quantity_empty_out",
                      "costo unitario": "unit_cost", "costo promedio previo": "previous_average_cost",
                      "existencia previa": "previous_on_hand",
                     "existencia previa leída el": "previous_on_hand_at"},
    "Caja": {"nombre": "name", "tipo": "kind", "saldo": "balance",
             "requiere sesión": "requires_session", "activa": "is_active"},
    "SesionDeCaja": {"estado": "status", "abierta el": "opened_at", "monto inicial": "opening_amount",
                     "cerrada el": "closed_at", "monto esperado": "expected_amount",
                     "monto contado": "counted_amount", "diferencia": "difference",
                     "observaciones": "notes"},
    "CategoriaDeCaja": {"nombre": "name", "sentido": "direction", "código de sistema": "system_code",
                        "activa": "is_active"},
    "MovimientoDeCaja": {"sentido": "direction", "importe": "amount", "medio": "method",
                         "fecha": "occurred_at", "descripción": "description",
                         "origen": "reference_type"},
    "RendicionChofer": {"número": "number", "fecha de negocio": "business_date", "estado": "status",
                        "efectivo esperado": "expected_cash", "efectivo declarado": "declared_cash",
                        "/gastos del chofer": "driver_expenses", "/diferencia": "difference",
                        "resolución de la diferencia": "difference_resolution",
                        "presentada el": "submitted_at", "aprobada el": "approved_at",
                        "observaciones": "notes", "aviso enviado el": "alerted_at"},
    "PedidoRendido": {"importe": "amount", "medio de pago": "payment_method"},
    "GastoDeRendicion": {"importe": "amount", "descripción": "description"},
    "CuentaCorriente": {"razón social": "business_name", "CUIT": "tax_id",
                        "condición fiscal": "tax_condition", "límite de crédito": "credit_limit",
                        "plazo de pago en días": "payment_terms_days", "estado": "status",
                        "saldo": "balance"},
    "AsientoCuentaCorriente": {"tipo": "type", "importe": "amount", "vence": "due_date",
                               "medio de pago": "payment_method", "fecha": "occurred_at",
                               "descripción": "description"},
    "ImputacionCuentaCorriente": {"importe": "amount"},
    "ReglaComision": {"base": "basis", "valor": "value", "vigente desde": "valid_from",
                      "vigente hasta": "valid_to", "activa": "is_active"},
    "AsientoComision": {"tipo": "type", "importe": "amount", "fecha": "occurred_at",
                        "descripción": "description"},
    "LiquidacionComisiones": {"número": "number", "período desde": "period_from",
                              "período hasta": "period_to", "bruto": "gross",
                              "deducciones": "deductions", "neto": "net", "estado": "status",
                              "aprobada el": "approved_at", "pagada el": "paid_at"},
}
ATRIBUTOS["PlanMantenimiento"].update({"documento que controla": "document_kind", "aplica a": "applies_to_categories"})
ATRIBUTOS["TareaMantenimiento"].update({"vigente desde": "valid_from", "detalle": "details"})
ATRIBUTOS["Vehiculo"].update({"tipo de combustible": "fuel_type",
                              "capacidad del tanque": "tank_capacity_liters"})
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
    ("maintenance_task", "employee_id"): "habilita",
    ("employee_leave", "decided_by_user_id"): "resuelve",
    ("stock_movement", "from_location_id"): "sale de",
    ("stock_movement", "to_location_id"): "entra en",
    ("stock_movement", "reversed_movement_id"): "corrige a",
    ("truck_load", "opened_by_user_id"): "abre",
    ("truck_load", "closed_by_user_id"): "cierra",
    ("truck_load", "helper_employee_id"): "ayuda en",
    ("customer_account_allocation", "debit_entry_id"): "salda",
    ("customer_account_allocation", "credit_entry_id"): "se aplica con",
    ("cash_movement", "reverses_movement_id"): "anula a",
    ("customer_account_entry", "reverses_entry_id"): "anula a",
}

# Columnas que solo dicen quién hizo algo: no son asociaciones del dominio.
AUTORIA_TECNICA = {("maintenance_task_attachment", "uploaded_by_user_id"),
                   ("module_config", "updated_by_user_id"),
                   ("vehicle_assignment", "assigned_by_user_id"),
                   ("vehicle_assignment", "released_by_user_id"),
                   ("attachment", "uploaded_by_user_id"), ("employee_leave", "requested_by_user_id"),
                   ("employee_attendance", "recorded_by_user_id"),
                   ("fuel_load", "created_by_user_id"), ("tire_event", "created_by_user_id"),
                   ("cash_session", "opened_by_user_id"), ("cash_session", "closed_by_user_id"),
                   ("cash_movement", "created_by_user_id"), ("driver_settlement", "submitted_by_user_id"),
                   ("driver_settlement", "approved_by_user_id"),
                   ("customer_account_entry", "created_by_user_id"), ("commission_entry", "created_by_user_id"),
                   ("driver_liquidation", "approved_by_user_id")}

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
