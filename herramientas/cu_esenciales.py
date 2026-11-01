"""Los casos de uso esenciales: los únicos que llevan su caso de uso expandido en el Documento 1.

Decisión de nahue (31/10/2026): la cátedra no pide los artefactos de todos los casos; quedan los 21 del
circuito del pedido, los cinco módulos inteligentes y la auditoría. Los demás casos siguen en la lista
con su importancia (Documento 1 §4) y en el diagrama de su subsistema.
"""

ESENCIALES = (
    "CU-001", "CU-002", "CU-005", "CU-008", "CU-022", "CU-013", "CU-014", "CU-015", "CU-017",
    "CU-078", "CU-079", "CU-292", "CU-301", "CU-048", "CU-023", "CU-025",
    "CU-105", "CU-106", "CU-107", "CU-108", "CU-152",
)

# Retirados del alcance (el chofer cobra un sueldo mensual, sin comisiones por entrega): siguen en el catálogo
# de Casos-de-Uso.md y en el Documento 0, pero el Documento 1 los lista como retirados y no los cuenta en los
# IRQ ni en la matriz. Las ganancias del chofer y las comisiones con su liquidación (decisión de nahue, 31/10/2026).
RETIRADOS_ALCANCE = ("CU-049", "CU-240", "CU-241", "CU-242", "CU-243", "CU-244",
                     "CU-333", "CU-334", "CU-335", "CU-347")

# Documento 2 (Análisis): sólo los casos donde el actor interviene y el sistema reacciona según lo que ingresa o
# decide llevan diagrama de secuencia (DSS) y contrato; el resto se nombra en una tabla con el motivo (decisión de
# nahue, 01/11/2026, según los apuntes de la cátedra).
CON_DSS = ("CU-001", "CU-002", "CU-005", "CU-008", "CU-015", "CU-078", "CU-079", "CU-301", "CU-048", "CU-025")

# Operaciones de consulta de los casos con DSS: no cambian el estado del sistema, así que no llevan contrato
# (Larman: el contrato describe cambios del modelo conceptual). Decisión de nahue, 01/11/2026.
CONSULTAS_SIN_CONTRATO = ("iniciarSesion", "obtenerCodigoDeEntrega")

SIN_DSS = {
    "CU-022": ("Lineal", "el chofer sólo cambia su disponibilidad: una única secuencia, sin decisiones del actor."),
    "CU-292": ("Lineal", "el chofer confirma que cobró; la secuencia es única y el sistema no reacciona distinto según lo que ingrese."),
    "CU-023": ("Lineal", "el cliente completa un formulario y el sistema crea el reclamo; no hay variantes del comportamiento."),
    "CU-013": ("Automático", "lo dispara la creación del pedido, sin eventos del actor."),
    "CU-014": ("Automático", "proceso periódico del sistema, sin eventos del actor."),
    "CU-017": ("Estático", "el sistema sólo registra la posición informada por el dispositivo; lo resuelve una sola clase."),
    "CU-105": ("Automático", "proceso diario del sistema; las respuestas del chofer y del administrador son decisiones sobre propuestas ya emitidas."),
    "CU-106": ("Automático", "proceso diario del sistema, sin eventos del actor."),
    "CU-107": ("Automático", "proceso periódico del sistema, sin eventos del actor."),
    "CU-108": ("Automático", "proceso periódico del sistema, sin eventos del actor."),
    "CU-152": ("Estático", "es una consulta que no modifica nada: la resuelve una sola clase."),
}

# Conceptos del modelo conceptual del Documento 2: los que aparecen en los 21 casos de uso esenciales.
CONCEPTOS_ESENCIALES = (
    "Distribuidora", "Usuario", "Rol", "Administrador", "ConfiguracionModulo", "AsientoAuditoria", "Auditoria",
    "DetalleAuditoria", "TipoAccionAuditoria", "Cliente", "DireccionEntrega", "InvitacionRecompra", "ItemSugerido",
    "Producto", "Promocion", "Envase", "MovimientoEnvase", "CasoRecupero", "AvisoRecupero", "Carrito", "ItemCarrito",
    "Pedido", "ItemPedido", "CambioEstadoPedido", "ZonaCobertura", "FranjaHoraria", "Pago", "ReintegroDePago",
    "PropuestaConVigencia", "OfertaDespacho", "LoteRecorrido", "ParadaLote", "OfertaLote", "Chofer", "Vehiculo",
    "AsignacionVehiculo", "PlanMantenimiento", "TareaMantenimiento", "PropuestaVentanaTaller", "UbicacionGPS",
    "RegistroUsoVehiculo", "Empleado", "Reclamo", "Deposito", "UbicacionDeStock", "SaldoDeStock", "MovimientoDeStock",
    "CargaDeCamion",
)
