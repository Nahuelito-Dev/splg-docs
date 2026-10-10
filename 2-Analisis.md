# Documento de Análisis — Fase II
**Proyecto:** SPLG – Sistema de Pedidos y Logística de Garrafas de Gas
**Versión:** 1.3
**Fecha:** 2026-10-03
**Realizado por:** Nahuel Wagner

---


## Índice de Figuras

- Figura 1 — Diagrama Conceptual
- Figura 1.1 — Modelo conceptual: usuarios y cuentas
- Figura 1.2 — Modelo conceptual: pedidos y pagos
- Figura 1.3 — Modelo conceptual: despacho y propuestas con vigencia
- Figura 1.4 — Modelo conceptual: flota y choferes
- Figura 1.5 — Modelo conceptual: envases y catálogo
- Figura 1.6 — Modelo conceptual: personal (puestos y legajos construidos; jornadas y licencias planificadas, I-11)
- Figura 1.7 — Modelo conceptual: posventa
- Figura 1.8 — Modelo conceptual: gastos de la flota (planificado, I-12)
- Figura 1.9 — Modelo conceptual: stock físico (planificado, I-13)
- Figura 1.10 — Modelo conceptual: carga del camión (planificado, I-13)
- Figura 1.11 — Modelo conceptual: compras (planificado, I-13)
- Figura 1.12 — Modelo conceptual: caja y movimientos (planificado, I-14)
- Figura 1.13 — Modelo conceptual: rendiciones de choferes (planificado, I-14)
- Figura 1.14 — Modelo conceptual: cuentas corrientes (planificado, I-14)
- Figura 1.15 — Modelo conceptual: comisiones y liquidaciones (planificado, I-14)
- Figura 2 — DSS CU-001: Iniciar Sesión
- Figura 3 — DSS CU-005: Crear Pedido
- Figura 4 — DSS CU-013: Asignar Pedido Automáticamente por Proximidad
- Figura 5 — DSS CU-014: Reintentar Asignación con Radio Expandido (Cron)
- Figura 6 — DSS CU-171: Configurar los Parámetros de Despacho de la Distribuidora
- Figura 7 — DSS CU-015: Aceptar Pedido
- Figura 8 — DSS CU-017: Actualizar Ubicación GPS del Chofer
- Figura 9 — DSS CU-020: Confirmar Entrega
- Figura 10 — DSS CU-023: Registrar Reclamo
- Figura 11 — DSS CU-002: Registrarse como Cliente
- Figura 12 — DSS CU-003: Registrar Chofer
- Figura 13 — DSS CU-004: Consultar el Perfil de Usuario
- Figura 14 — DSS CU-251: Modificar el Perfil de Usuario
- Figura 15 — DSS CU-047: Recuperar Contraseña
- Figura 16 — DSS CU-050: Bloquear un Usuario
- Figura 17 — DSS CU-270: Desbloquear un Usuario
- Figura 18 — DSS CU-083: Listar los Usuarios
- Figura 19 — DSS CU-272: Buscar un Usuario
- Figura 20 — DSS CU-084: Verificar Existencia de Usuario (pre-registro)
- Figura 21 — DSS CU-085: Eliminar Usuario (baja lógica)
- Figura 22 — DSS CU-091: Validar Vigencia del Token de Sesión
- Figura 23 — DSS CU-006: Consultar Detalle de Pedido
- Figura 24 — DSS CU-007: Consultar Historial de Pedidos
- Figura 25 — DSS CU-169: Registrar el Cambio de Estado de un Pedido
- Figura 26 — DSS CU-170: Consultar el Historial de Estados de un Pedido
- Figura 27 — DSS CU-143: Declarar el Consumo Promedio al Registrarse
- Figura 28 — DSS CU-144: Actualizar el Consumo Promedio Declarado
- Figura 29 — DSS CU-145: Configurar los Días de Aviso Previo a la Recompra
- Figura 30 — DSS CU-146: Consultar la Fecha Estimada de Recompra
- Figura 31 — DSS CU-147: Realizar una Compra Express
- Figura 32 — DSS CU-148: Elegir la Modalidad de Entrega del Pedido
- Figura 33 — DSS CU-008: Cancelar Pedido (Cliente)
- Figura 34 — DSS CU-009: Cancelar Pedido (Chofer)
- Figura 35 — DSS CU-010: Cancelar Pedido (Administrador)
- Figura 36 — DSS CU-011: Listar Todos los Pedidos
- Figura 37 — DSS CU-012: Asignar Chofer Manualmente
- Figura 38 — DSS CU-149: Despachar un Pedido Express a un Chofer en Moto
- Figura 39 — DSS CU-046: Consultar Direcciones de Entrega del Cliente
- Figura 40 — DSS CU-116: Registrar Dirección de Entrega
- Figura 41 — DSS CU-117: Consultar Detalle de una Dirección de Entrega
- Figura 42 — DSS CU-118: Editar Dirección de Entrega
- Figura 43 — DSS CU-119: Eliminar Dirección de Entrega
- Figura 44 — DSS CU-120: Marcar una Dirección como Predeterminada
- Figura 45 — DSS CU-121: Consultar la Dirección Predeterminada
- Figura 46 — DSS CU-122: Agregar Ítem al Carrito
- Figura 47 — DSS CU-123: Modificar la Cantidad de un Ítem del Carrito
- Figura 48 — DSS CU-124: Quitar Ítem del Carrito
- Figura 49 — DSS CU-125: Consultar el Carrito
- Figura 50 — DSS CU-126: Vaciar el Carrito
- Figura 51 — DSS CU-127: Cambiar la Dirección de Entrega del Pedido
- Figura 52 — DSS CU-128: Indicar Quién Recibe el Pedido
- Figura 53 — DSS CU-080: Consultar el Pool de Pedidos Disponibles
- Figura 54 — DSS CU-081: Consultar los Pedidos Asignados al Chofer
- Figura 55 — DSS CU-016: Rechazar / Ignorar Pedido
- Figura 56 — DSS CU-018: Marcar Pedido "En Camino"
- Figura 57 — DSS CU-019: Avisar Llegada al Cliente
- Figura 58 — DSS CU-021: Recibir Notificaciones en Tiempo Real
- Figura 59 — DSS CU-022: Activar la Disponibilidad
- Figura 60 — DSS CU-266: Desactivar la Disponibilidad
- Figura 61 — DSS CU-078: Obtener el Código de Entrega (QR del chofer)
- Figura 62 — DSS CU-079: Confirmar Entrega Escaneando el QR (cliente)
- Figura 63 — DSS CU-024: Listar Reclamos
- Figura 64 — DSS CU-025: Resolver Reclamo
- Figura 65 — DSS CU-166: Tomar un Reclamo Pendiente
- Figura 66 — DSS CU-167: Reabrir un Reclamo
- Figura 67 — DSS CU-174: Adjuntar la Fotografía de un Reclamo
- Figura 68 — DSS CU-175: Consultar la Fotografía de un Reclamo
- Figura 69 — DSS CU-026: Ver Dashboard General
- Figura 70 — DSS CU-027: Ver Reporte de Ventas por Chofer
- Figura 71 — DSS CU-028: Ver Reporte de Ventas por Producto
- Figura 72 — DSS CU-029: Ver Reporte por Método de Pago
- Figura 73 — DSS CU-030: Ver Gráfico de Ventas (últimos 7 días)
- Figura 74 — DSS CU-031: Registrar Chofer
- Figura 75 — DSS CU-032: Validar un Chofer
- Figura 76 — DSS CU-271: Invalidar un Chofer
- Figura 77 — DSS CU-033: Activar un Chofer
- Figura 78 — DSS CU-267: Desactivar un Chofer
- Figura 79 — DSS CU-034: Registrar Vehículo del Chofer
- Figura 80 — DSS CU-035: Consultar Listado de Choferes
- Figura 81 — DSS CU-049: Consultar Balance / Ganancias del Chofer
- Figura 82 — DSS CU-051: Consultar Listado de Vehículos
- Figura 83 — DSS CU-096: Actualizar Perfil del Chofer
- Figura 84 — DSS CU-097: Eliminar Chofer (baja lógica)
- Figura 85 — DSS CU-109: Consultar Detalle del Chofer
- Figura 86 — DSS CU-110: Buscar Chofer por Usuario
- Figura 87 — DSS CU-111: Editar Vehículo
- Figura 88 — DSS CU-112: Eliminar Vehículo
- Figura 89 — DSS CU-113: Consultar Detalle del Vehículo
- Figura 90 — DSS CU-114: Buscar Vehículo por Patente
- Figura 91 — DSS CU-115: Consultar Vehículos de un Chofer
- Figura 92 — DSS CU-136: Registrar el Seguro del Vehículo
- Figura 93 — DSS CU-137: Registrar la Verificación Técnica Vehicular
- Figura 94 — DSS CU-138: Registrar la Licencia de Conducir del Chofer
- Figura 95 — DSS CU-139: Consultar los Vencimientos de la Flota
- Figura 96 — DSS CU-140: Programar un Mantenimiento de Vehículo
- Figura 97 — DSS CU-141: Registrar un Mantenimiento Realizado
- Figura 98 — DSS CU-142: Avisar los Vencimientos Próximos de la Flota
- Figura 99 — DSS CU-155: Adjuntar Archivo a una Tarea de Flota
- Figura 100 — DSS CU-156: Consultar Adjuntos de una Tarea de Flota
- Figura 101 — DSS CU-157: Descargar un Adjunto de Flota
- Figura 102 — DSS CU-158: Eliminar un Adjunto de Flota
- Figura 103 — DSS CU-161: Poner un Vehículo en Uso para un Chofer
- Figura 104 — DSS CU-162: Liberar el Vehículo en Uso de un Chofer
- Figura 105 — DSS CU-163: Consultar el Vehículo en Uso de un Chofer
- Figura 106 — DSS CU-164: Consultar el Historial de Vehículos de un Chofer
- Figura 107 — DSS CU-165: Consultar el Historial de Choferes de un Vehículo
- Figura 108 — DSS CU-195: Registrar una Carga de Combustible
- Figura 109 — DSS CU-196: Consultar el Consumo de Combustible de un Vehículo
- Figura 110 — DSS CU-197: Registrar la Habilitación para Transportar Mercancías Peligrosas
- Figura 111 — DSS CU-198: Registrar una Multa de Tránsito
- Figura 112 — DSS CU-199: Registrar el Pago de una Multa
- Figura 113 — DSS CU-200: Imputar una Multa al Chofer
- Figura 114 — DSS CU-201: Registrar un Siniestro
- Figura 115 — DSS CU-202: Cerrar un Siniestro
- Figura 116 — DSS CU-203: Consultar el Costo Total de un Vehículo
- Figura 117 — DSS CU-204: Consultar el Tablero de Costos de la Flota
- Figura 118 — DSS CU-205: Registrar un Neumático
- Figura 119 — DSS CU-206: Registrar un Movimiento de Neumático
- Figura 120 — DSS CU-247: Reactivar un Vehículo
- Figura 121 — DSS CU-036: Crear Producto (Garrafa)
- Figura 122 — DSS CU-037: Actualizar Precio de Producto
- Figura 123 — DSS CU-038: Actualizar Stock de Producto
- Figura 124 — DSS CU-039: Configurar Promociones por Cantidad
- Figura 125 — DSS CU-040: Desactivar un Producto
- Figura 126 — DSS CU-268: Reactivar un Producto
- Figura 127 — DSS CU-269: Consultar los Productos Inactivos
- Figura 128 — DSS CU-041: Consultar Catálogo de Productos
- Figura 129 — DSS CU-042: Crear Franja Horaria
- Figura 130 — DSS CU-044: Seleccionar Franja Horaria al Crear Pedido
- Figura 131 — DSS CU-045: Consultar Franjas Horarias Disponibles
- Figura 132 — DSS CU-103: Eliminar Franja Horaria
- Figura 133 — DSS CU-154: Consultar Listado de Franjas Horarias
- Figura 134 — DSS CU-052: Registrar Distribuidora
- Figura 135 — DSS CU-053: Consultar Distribuidoras
- Figura 136 — DSS CU-054: Modificar Datos de la Distribuidora
- Figura 137 — DSS CU-055: Dar de Baja una Distribuidora
- Figura 138 — DSS CU-056: Definir Zona de Cobertura
- Figura 139 — DSS CU-057: Consultar Zonas de Cobertura
- Figura 140 — DSS CU-058: Validar Cobertura de una Dirección
- Figura 141 — DSS CU-059: Eliminar Zona de Cobertura
- Figura 142 — DSS CU-150: Programar la Vigencia de una Zona de Cobertura
- Figura 143 — DSS CU-151: Desactivar las Zonas de Cobertura Vencidas
- Figura 144 — DSS CU-060: Registrar Incidencia de Entrega
- Figura 145 — DSS CU-061: Listar Incidencias
- Figura 146 — DSS CU-062: Consultar Incidencias de un Pedido
- Figura 147 — DSS CU-063: Resolver Incidencia
- Figura 148 — DSS CU-064: Calificar Pedido (cliente↔chofer)
- Figura 149 — DSS CU-065: Consultar Promedio de Calificaciones de un Usuario
- Figura 150 — DSS CU-066: Consultar Historial de Calificaciones Recibidas
- Figura 151 — DSS CU-067: Dar de Alta un Envase Físico
- Figura 152 — DSS CU-068: Asignar Envases a un Pedido
- Figura 153 — DSS CU-069: Consultar el Parque de Envases
- Figura 154 — DSS CU-070: Registrar Movimiento de Envase (cambio de estado)
- Figura 155 — DSS CU-071: Consultar Historial de Movimientos de un Envase
- Figura 156 — DSS CU-132: Registrar la Revisión Periódica de un Envase
- Figura 157 — DSS CU-133: Consultar la Vigencia de un Envase
- Figura 158 — DSS CU-134: Consultar los Envases Próximos a Vencer
- Figura 159 — DSS CU-135: Bloquear el Despacho de un Envase Vencido
- Figura 160 — DSS CU-048: Procesar Pago con MercadoPago
- Figura 161 — DSS CU-168: Reintegrar el Pago de un Pedido
- Figura 162 — DSS CU-072: Crear Reserva Programada con Seña
- Figura 163 — DSS CU-073: Listar Reservas y Estado de la Seña
- Figura 164 — DSS CU-074: Confirmar Seña Cobrada en Efectivo
- Figura 165 — DSS CU-075: Activar Reservas Vencidas Automaticamente (Cron)
- Figura 166 — DSS CU-076: Expirar Reservas sin Seña Pagada (Cron)
- Figura 167 — DSS CU-077: Expirar Pedidos de MercadoPago sin Pagar (Cron)
- Figura 168 — DSS CU-086: Registrar Administrador
- Figura 169 — DSS CU-087: Crear el Primer Super Administrador (bootstrap)
- Figura 170 — DSS CU-088: Consultar Administradores
- Figura 171 — DSS CU-089: Consultar los Roles
- Figura 172 — DSS CU-252: Crear un Rol
- Figura 173 — DSS CU-253: Modificar un Rol
- Figura 174 — DSS CU-254: Eliminar un Rol
- Figura 175 — DSS CU-090: Sembrar los Roles Iniciales
- Figura 176 — DSS CU-092: Consultar Listado de Clientes
- Figura 177 — DSS CU-094: Actualizar Ubicación del Cliente
- Figura 178 — DSS CU-095: Eliminar Cliente (baja lógica)
- Figura 179 — DSS CU-129: Consultar Detalle del Cliente
- Figura 180 — DSS CU-130: Buscar Cliente por Usuario
- Figura 181 — DSS CU-131: Editar Datos del Cliente
- Figura 182 — DSS CU-098: Registrar el Token de Notificaciones del Dispositivo
- Figura 183 — DSS CU-099: Consultar los Tokens de un Usuario
- Figura 184 — DSS CU-100: Enviar Notificación de Prueba
- Figura 185 — DSS CU-101: Reenviar Notificación de Confirmación de Pedido
- Figura 186 — DSS CU-102: Probar el Servicio de Correo
- Figura 187 — DSS CU-104: Verificar la Salud del Sistema (liveness / readiness)
- Figura 188 — DSS CU-152: Consultar el Registro de Auditoría
- Figura 189 — DSS CU-153: Registrar Toda Operación de Escritura
- Figura 190 — DSS CU-172: Configurar los Parámetros de un Proceso Automático
- Figura 191 — DSS CU-173: Configurar la Frecuencia de las Tareas Programadas
- Figura 192 — DSS CU-176: Consultar los Puestos de Trabajo
- Figura 193 — DSS CU-255: Crear un Puesto de Trabajo
- Figura 194 — DSS CU-256: Modificar un Puesto de Trabajo
- Figura 195 — DSS CU-257: Eliminar un Puesto de Trabajo
- Figura 195.1 — DSS CU-177: Registrar el Legajo de un Empleado
- Figura 195.2 — DSS CU-178: Modificar el Legajo de un Empleado
- Figura 195.3 — DSS CU-179: Consultar el Legajo de un Empleado
- Figura 195.4 — DSS CU-180: Consultar el Listado de Empleados
- Figura 195.5 — DSS CU-181: Registrar el Egreso de un Empleado
- Figura 195.6 — DSS CU-182: Otorgar una Cuenta de Acceso a un Empleado
- Figura 195.7 — DSS CU-183: Registrar el Curso de Transporte de Mercancías Peligrosas del Empleado
- Figura 195.8 — DSS CU-184: Registrar el Examen Psicofísico del Empleado
- Figura 195.9 — DSS CU-185: Registrar el Alta en la ART del Empleado
- Figura 195.10 — DSS CU-186: Adjuntar un Archivo al Legajo
- Figura 195.11 — DSS CU-187: Consultar los Vencimientos del Personal
- Figura 195.12 — DSS CU-188: Avisar los Vencimientos Próximos del Personal
- Figura 195.13 — DSS CU-189: Registrar la Asistencia de un Empleado
- Figura 195.14 — DSS CU-190: Registrar el Inicio y el Fin de la Jornada
- Figura 195.15 — DSS CU-191: Registrar una Licencia o Ausencia
- Figura 195.16 — DSS CU-192: Resolver una Solicitud de Licencia
- Figura 195.17 — DSS CU-193: Consultar el Saldo de Vacaciones de un Empleado
- Figura 195.18 — DSS CU-194: Consultar el Tablero de Personal
- Figura 196 — DSS CU-207: Consultar los Depósitos
- Figura 197 — DSS CU-258: Registrar un Depósito
- Figura 198 — DSS CU-259: Modificar un Depósito
- Figura 199 — DSS CU-260: Dar de Baja un Depósito
- Figura 200 — DSS CU-208: Consultar el Stock por Ubicación
- Figura 201 — DSS CU-209: Consultar los Movimientos de Stock
- Figura 202 — DSS CU-210: Configurar el Stock Mínimo
- Figura 203 — DSS CU-211: Avisar el Stock Bajo
- Figura 204 — DSS CU-212: Transferir Stock entre Depósitos
- Figura 205 — DSS CU-213: Registrar un Ajuste o una Merma de Stock
- Figura 206 — DSS CU-218: Registrar la Carga del Camión
- Figura 207 — DSS CU-219: Registrar la Salida del Camión
- Figura 208 — DSS CU-220: Descontar del Camión lo Entregado
- Figura 209 — DSS CU-221: Registrar el Regreso del Camión
- Figura 210 — DSS CU-222: Cerrar la Rendición de Stock del Camión
- Figura 211 — DSS CU-223: Consultar la Carga Actual del Camión
- Figura 212 — DSS CU-224: Conciliar el Stock Vendible con el Físico
- Figura 213 — DSS CU-249: Configurar el Control de Carga de Camión Abierta
- Figura 214 — DSS CU-214: Consultar los Proveedores
- Figura 215 — DSS CU-261: Registrar un Proveedor
- Figura 216 — DSS CU-262: Modificar un Proveedor
- Figura 217 — DSS CU-263: Dar de Baja un Proveedor
- Figura 218 — DSS CU-215: Emitir una Orden de Compra
- Figura 219 — DSS CU-216: Cancelar una Orden de Compra
- Figura 220 — DSS CU-217: Registrar la Recepción de una Compra
- Figura 221 — DSS CU-225: Crear una Caja
- Figura 222 — DSS CU-264: Modificar una Caja
- Figura 223 — DSS CU-226: Abrir la Caja
- Figura 224 — DSS CU-227: Cerrar la Caja con Arqueo
- Figura 225 — DSS CU-228: Registrar un Ingreso o Egreso de Caja
- Figura 226 — DSS CU-229: Anular un Movimiento de Caja
- Figura 227 — DSS CU-230: Crear una Categoría de Ingresos y Gastos
- Figura 228 — DSS CU-265: Modificar una Categoría de Ingresos y Gastos
- Figura 229 — DSS CU-231: Generar la Rendición Diaria del Chofer
- Figura 230 — DSS CU-232: Declarar el Efectivo Rendido
- Figura 231 — DSS CU-233: Aprobar la Rendición del Chofer
- Figura 232 — DSS CU-234: Avisar las Rendiciones sin Cerrar
- Figura 233 — DSS CU-235: Habilitar la Cuenta Corriente de un Cliente
- Figura 234 — DSS CU-236: Vender a Cuenta Corriente
- Figura 235 — DSS CU-237: Registrar un Pago de Cuenta Corriente
- Figura 236 — DSS CU-238: Consultar el Estado de Cuenta de un Cliente
- Figura 237 — DSS CU-239: Consultar la Antigüedad de la Deuda
- Figura 238 — DSS CU-240: Configurar las Comisiones por Entrega
- Figura 239 — DSS CU-241: Registrar la Comisión de una Entrega
- Figura 240 — DSS CU-242: Liquidar las Comisiones de un Chofer
- Figura 241 — DSS CU-243: Registrar el Pago de una Liquidación
- Figura 242 — DSS CU-244: Consultar Mis Comisiones
- Figura 243 — DSS CU-245: Consultar el Tablero Financiero
- Figura 244 — DSS CU-105: Planificar el mantenimiento y las habilitaciones de la flota
- Figura 245 — DSS CU-106: Anticipar la recompra por consumo estimado
- Figura 246 — DSS CU-107: Agrupar pedidos por recorrido
- Figura 247 — DSS CU-108: Recuperar envases no devueltos
- Figura 248 — DSS CU-043: Modificar Capacidad de Franja Horaria

---

## Lista de Cambios

| Nro | Fecha | Descripción | Autor |
|-----|-------|-------------|-------|
| 0 | 2026-04-17 | Versión inicial | Nahuel Wagner |
| 1 | 2026-08-30 | Verificación de la documentación contra el código. Contratos de operación completados con los campos Notas y Salida que exige la plantilla. | Nahuel Wagner |
| 2 | 2026-09-24 | Reconstrucción del modelo conceptual para que contenga los ocho contextos y los 152 casos de uso, incluidos los planificados. | Nahuel Wagner |
| 3 | 2026-09-30 | Revisión de conformidad del modelo conceptual y de los contratos: notación de multiplicidad UML, asociaciones y atributos verificados contra la base, lista de candidatos por categoría, formato de relaciones de la plantilla y contratos reescritos en términos del modelo conceptual. | Nahuel Wagner |
| 4 | 2026-10-01 | Casos de uso CU-161 a CU-167: vehículo en uso por chofer (asignación, liberación, consulta e historiales) y reclamos (tomar y reabrir), con sus diagramas de secuencia y los contratos de las operaciones que modifican datos. | Nahuel Wagner |
| 5 | 2026-10-01 | Diagramas de secuencia del sistema de CU-168 a CU-175 y los contratos de sus operaciones. Diagramas de CU-008, CU-010, CU-040, CU-043, CU-125, CU-127, CU-135, CU-148 y CU-149 ajustados a las decisiones de diseño. | Nahuel Wagner |
| 6 | 2026-10-01 | Diagramas de secuencia del sistema en notación de Larman: lifeline `:Sistema`, actores del catálogo, salidas al actor como mensajes asíncronos con nombre y casos incluidos sin diagrama propio. Catálogo de operaciones del sistema, con una sola firma por operación, y contratos de todas las operaciones que modifican el modelo conceptual. | Nahuel Wagner |
| 7 | 2026-10-01 | Cierre de la documentación: modelo conceptual, diagramas de secuencia del sistema en notación de Larman, catálogo de 194 operaciones y 110 contratos de operación coherentes con el código; firmas corregidas de crearRol, actualizarUbicacionDelCliente y enviarNotificacionDePrueba; actor de probarServicioDeCorreo; comportamiento de crearCheckoutDePago, notificarResultadoDePago, editarVehiculo, eliminarUsuario y cambiarDisponibilidad. | Nahuel Wagner |
| 8 | 2026-10-01 | Revisión final: CU-048 pasa a operación interna de crearPedido (catálogo de 194 operaciones y 110 contratos), notificaciones fuera de las postcondiciones de los contratos, contratos de confirmarEntrega, ofrecerAlSiguienteChofer, crearPedido y agregarItemAlCarrito ajustados, actor ACT-09 en CU-104. | Nahuel Wagner |
| 9 | 2026-10-03 | Versión 1.1 del sistema (versión del software, back y panel, distinta de la versión de este documento): ItemPedido con precio unitario y subtotal guardados en el renglón, y contrato de crearPedido ajustado. | Nahuel Wagner |
| 10 | 2026-10-03 | Módulo de Personal (CU-176 a CU-194; el caso incluido CU-246, con su nota): cinco conceptos nuevos y sus asociaciones en el modelo conceptual, diagramas de secuencia del sistema, 29 operaciones nuevas en el catálogo y 20 contratos nuevos. | Nahuel Wagner |
| 11 | 2026-10-03 | Módulo de flota ampliada (CU-195 a CU-206 y CU-247): cinco conceptos nuevos en el modelo conceptual, diagramas de secuencia del sistema y 21 operaciones nuevas en el catálogo. | Nahuel Wagner |
| 12 | 2026-10-03 | Módulo de stock y compras (CU-207 a CU-224 y CU-249; los casos incluidos CU-248 y CU-250, con su nota): catorce conceptos nuevos en el modelo conceptual, diagramas de secuencia del sistema, 35 operaciones nuevas en el catálogo y 24 contratos. | Nahuel Wagner |
| 13 | 2026-10-03 | Módulo de caja y rendición (CU-225 a CU-245): trece conceptos nuevos en el modelo conceptual, diagramas de secuencia del sistema y 27 contratos nuevos. El adjunto pasa a ser un concepto implementado (tabla `attachment`) y el catálogo queda en 310 operaciones y 196 contratos. | Nahuel Wagner |
| 14 | 2026-10-06 | Auditoría de datos (CU-152 y CU-153): tres conceptos nuevos en el modelo conceptual —Auditoria, DetalleAuditoria y TipoAccionAuditoria—, dos operaciones nuevas en el catálogo y un contrato nuevo; el catálogo queda en 312 operaciones y 197 contratos. | Nahuel Wagner |
| 15 | 2026-10-07 | Los casos de uso que agrupaban varias operaciones de un ABM se parten en uno por operación (CU-251 a CU-272): un diagrama de secuencia del sistema por caso, con su propia operación, y los contratos de las operaciones referidos al caso que corresponde. | Nahuel Wagner |
| 16 | 2026-10-07 | Personal construido en el backend: puestos de trabajo y legajos (CU-176 a CU-182, CU-186 y CU-255 a CU-257) pasan a «Implementado» —CU-178, CU-180 y CU-181 con funcionalidad planificada—, con sus diagramas, contratos y tablas verificados contra el código y la API; las jornadas, las licencias y el resto de SS-19 siguen planificados. | Nahuel Wagner |

---

## Leyenda

| Indicador | Significado |
|:---------:|-------------|
| C | Concepto / operación crítica |
| I | Concepto / operación importante |
| A | Proceso automático sin intervención humana |

---

## 1. Modelo Conceptual (Modelo de Dominio)

En Larman y en el Proceso Unificado, modelo conceptual y modelo de dominio son el mismo
artefacto: la cátedra, siguiendo la bibliografía en castellano, lo llama «Modelo
Conceptual». Esta sección es la única fuente de ese modelo; no hay una segunda versión en
ningún otro documento. Lo que sí existe por separado, y es un artefacto distinto, es el
**modelo entidad-relación** (nivel conceptual del diseño de la base de datos), en el
Documento 3 (§7.4) y en `diagramas/base-de-datos/conceptual/`.

### 1.1 Lista de Conceptos Candidatos

La lista de categorías es la de Larman (*UML y Patrones*, lista de categorías de conceptos
candidatos). Cada categoría trae los conceptos que terminaron siendo idóneos (§1.2): esta
lista es la fuente de esa otra, no un conjunto aparte de ejemplos sueltos.

| Categoría del Concepto | Ejemplos |
|-----------|----------------------|
| Organizaciones | Distribuidora |
| Personas | Usuario |
| Roles de las personas | Cliente, Chofer, Administrador, Empleado § |
| Descripciones o catálogos de especificación | Producto, Rol, TipoAccionAuditoria ¶, PlanMantenimiento, Proveedor §, PuestoDeTrabajo §, CategoriaDeCaja §, CuentaCorriente § |
| Objetos físicos o tangibles | Envase, Vehiculo, UbicacionGPS, Neumatico §, Deposito §, Caja § |
| Transacciones | Pedido, Carrito, Pago, OrdenDeCompra §, RecepcionDeCompra §, AjusteDeStock §, CargaDeCamion §, RendicionChofer §, LiquidacionComisiones § |
| Líneas de transacción | ItemPedido, ItemCarrito, ItemSugerido, ParadaLote, DetalleAuditoria ¶, ItemOrdenDeCompra §, ItemRecepcion §, ItemAjusteDeStock §, ItemCarga §, PedidoRendido §, GastoDeRendicion §, ImputacionCuentaCorriente § |
| Registros de transacciones o eventos | MovimientoEnvase, CambioEstadoPedido, CambioDireccion, AsientoAuditoria, Auditoria ¶, RevisionEnvase, RegistroUsoVehiculo, AdjuntoTarea, CargaCombustible §, MovimientoNeumatico §, MovimientoDeStock §, JornadaDeTrabajo §, Adjunto, MovimientoDeCaja §, AsientoCuentaCorriente §, AsientoComision §, SaldoDeStock § |
| Lugares | DireccionEntrega, ZonaCobertura, UbicacionDeStock § |
| Reglas y políticas | Promocion, ConfiguracionModulo, FranjaHoraria, UmbralDeStock §, ReglaComision § |
| Eventos | Incidencia, Reclamo, Calificacion, MultaTransito §, Siniestro §, LicenciaLaboral §, SesionDeCaja § |
| Procesos que se negocian por propuestas con vigencia | PropuestaConVigencia, OfertaDespacho, OfertaLote, PropuestaVentanaTaller, InvitacionRecompra, AvisoRecupero, CasoRecupero, LoteRecorrido, TareaMantenimiento |
| Otros sistemas externos al sistema | Pasarela de pago (MercadoPago), Firebase (autenticación) — candidatos, no idóneos: actúan desde afuera y no se modelan como concepto propio. |

**Candidatos descartados**, con el motivo:

| Candidato | Descartado porque |
|---|---|
| Garrafa | Ambiguo entre dos idóneos distintos: **Envase** (el botellón físico con número de serie) y **Producto** (el tipo comercializado). Ver «Nota sobre Producto y Envase» en §1.3. |
| Entrega | No agrega información propia: es uno de los valores del atributo `estado` de **Pedido** (`en_camino`, `entregado`). |
| Catálogo | Es el conjunto de **Producto** de una **Distribuidora** en un momento dado; no tiene identidad ni atributos propios. |
| Stock | El stock **vendible** es el atributo `stock` de **Producto**. El stock **físico** por ubicación y condición sí es un concepto, con su propia identidad: **SaldoDeStock** y el libro **MovimientoDeStock** (planificados, I-13). |
| Reporte | Es una consulta sobre datos existentes (pedidos, pagos, calificaciones), no algo que el sistema cree, modifique o dé de baja. |

---

### 1.2 Lista de Conceptos Idóneos

El sistema opera bajo un modelo **multi-distribuidora**: una única instancia atiende a
varias empresas comercializadoras manteniendo sus datos aislados entre sí. Por eso el
concepto **Distribuidora** encabeza el modelo y actúa como unidad de aislamiento de la
mayoría de los demás conceptos.

Los conceptos se organizan en **trece contextos**, que son las áreas del negocio que los
definen y los modifican. Los marcados con † se incorporaron el 24/09/2026 para que el
modelo contenga los 271 casos de uso, incluidos los planificados.
Los marcados con ‡ se agregaron el 30/09/2026, al contrastar el modelo con la base de
datos. Los marcados con ¶ se incorporaron el 06/10/2026 con la auditoría de datos del modelo de la cátedra (Auditoria, DetalleAuditoria y TipoAccionAuditoria), ya implementada.
Los marcados con § se incorporaron el 03/10/2026 con los módulos de gestión de la distribuidora
—personal (I-11), flota ampliada (I-12), stock y compras (I-13) y caja y rendición (I-14)—: sus tablas todavía no
están en la base, salvo las de puestos y legajos del personal, que ya están construidas. El Símbolo repite siempre el nombre del Concepto, salvo que se indique lo contrario.

| # | Descripción del Concepto | Símbolo | Intención | Extensión | Contexto |
|---|----------|---------|-----------|-----------|----------|
| 1 | **Distribuidora** | Distribuidora | Empresa comercializadora de garrafas que opera dentro del sistema. Unidad de aislamiento de los datos. | Cada empresa dada de alta en la plataforma. | Organización y acceso |
| 2 | **Usuario** | Usuario | Persona registrada en el sistema con un rol asignado. | Todos los clientes, choferes y administradores. | Organización y acceso |
| 3 | **Rol** | Rol | Conjunto de permisos que determina qué puede hacer un usuario. | Cliente, chofer, administrador y administrador general, además de un rol técnico de pruebas (`qa_pruebas`) que sólo existe en los ambientes de prueba. | Organización y acceso |
| 4 | **Administrador** | Administrador | Perfil extendido de un Usuario que gestiona la operación. | Operadores internos con acceso al Panel Web. | Organización y acceso |
| 5 | **ConfiguracionModulo** † | ConfiguracionModulo | Parámetros con que una distribuidora ajusta un proceso automático. | Una por módulo inteligente y distribuidora. | Organización y acceso |
| 6 | **AsientoAuditoria** † | AsientoAuditoria | Constancia inmutable de una operación que modificó datos: quién, qué, cuándo, desde dónde y con qué resultado. | Cada alta, modificación o baja, exitosa o fallida. | Organización y acceso |
| 7 | **Auditoria** ¶ | Auditoria | Constancia inmutable de que un registro de una entidad de negocio se dio de alta, se modificó, se dio de baja o se reactivó: sobre qué registro, quién, cuándo y desde dónde. | Cada registro de negocio afectado por una escritura confirmada. | Organización y acceso |
| 8 | **DetalleAuditoria** ¶ | DetalleAuditoria | Un campo que cambió dentro de una Auditoria, con su valor anterior y el nuevo. | Cada campo modificado en cada auditoría; en un alta, cada campo con valor. | Organización y acceso |
| 9 | **TipoAccionAuditoria** ¶ | TipoAccionAuditoria | Catálogo fijo de las acciones que se auditan: alta, modificación, baja lógica, reactivación y baja física. | Las cinco acciones. | Organización y acceso |
| 10 | **Cliente** | Cliente | Perfil extendido de un Usuario que realiza pedidos. | Toda persona que se registra en la App Cliente. | Clientes |
| 11 | **DireccionEntrega** | DireccionEntrega | Domicilio del cliente guardado para futuras entregas, resuelto contra el mapa. | Cada dirección registrada por un cliente. | Clientes |
| 12 | **InvitacionRecompra** † | InvitacionRecompra | Oferta de reposición que el sistema le hace a un cliente antes de que se le acabe el gas, con el pedido armado. | Cada invitación emitida por el módulo de recompra. | Clientes |
| 13 | **ItemSugerido** ‡ | ItemSugerido | Producto y cantidad que el módulo de recompra sugiere dentro de una invitación. | Cada línea del pedido sugerido por una invitación. | Clientes |
| 14 | **Producto** | Producto | Tipo de garrafa comercializado, con precio, stock y promociones. | Los formatos ofrecidos: 10 kg, 15 kg, 45 kg. | Catálogo e inventario |
| 15 | **Promocion** | Promocion | Descuento por volumen aplicable a un producto al superar una cantidad mínima. | Cada regla de descuento configurada. | Catálogo e inventario |
| 16 | **Envase** | Envase | Garrafa **física** individual, identificable y rastreable por su número de serie. | Cada botellón que la distribuidora posee o tiene en poder de un cliente. | Catálogo e inventario |
| 17 | **MovimientoEnvase** | MovimientoEnvase | Registro inmutable de cada cambio de estado de un envase físico. | La traza completa del ciclo de vida de cada envase. | Catálogo e inventario |
| 18 | **RevisionEnvase** † | RevisionEnvase | Prueba técnica periódica que renueva la vigencia de un envase. | Cada revisión asentada. | Catálogo e inventario |
| 19 | **CasoRecupero** † | CasoRecupero | Gestión escalonada de un envase que un cliente retiene por encima del plazo. | Cada envase retenido en gestión. | Catálogo e inventario |
| 20 | **AvisoRecupero** † | AvisoRecupero | Recordatorio, oferta de retiro o aviso de depósito enviado dentro de un caso de recupero. | Cada aviso emitido. | Catálogo e inventario |
| 21 | **Carrito** † | Carrito | Pedido en armado que el cliente deja guardado antes de confirmarlo. | Uno por cliente y distribuidora. | Venta y pedidos |
| 22 | **ItemCarrito** † | ItemCarrito | Producto cargado en el carrito, con su cantidad. | Cada línea del carrito. | Venta y pedidos |
| 23 | **Pedido** | Pedido | Solicitud formal de compra realizada por un cliente. Tiene un ciclo de vida de estados. | Cada transacción de compra registrada. | Venta y pedidos |
| 24 | **ItemPedido** | ItemPedido | Línea individual dentro de un pedido: un producto y su cantidad. | Cada garrafa solicitada dentro de un pedido. | Venta y pedidos |
| 25 | **CambioEstadoPedido** † | CambioEstadoPedido | Transición del pedido de un estado a otro, con su autor y su motivo. | Cada cambio de estado de cada pedido. | Venta y pedidos |
| 26 | **CambioDireccion** † | CambioDireccion | Cambio de la dirección de entrega de un pedido ya hecho, con su autor y las direcciones de origen y destino. | Cada cambio registrado. | Venta y pedidos |
| 27 | **ZonaCobertura** | ZonaCobertura | Área geográfica dentro de la cual una distribuidora acepta pedidos, con su recargo y su vigencia. | Los polígonos de cobertura definidos por cada distribuidora. | Venta y pedidos |
| 28 | **FranjaHoraria** | FranjaHoraria | Rango de horas del día habilitado para entregas, con capacidad máxima. | Franjas configuradas por cada distribuidora. | Venta y pedidos |
| 29 | **Pago** | Pago | Transacción económica asociada a un pedido, ejecutada por una pasarela. | Cada cobro intentado o concretado. | Pagos |
| 30 | **PropuestaConVigencia** † | PropuestaConVigencia | Algo que el sistema le propone a alguien por un tiempo acotado y que puede ser aceptado, rechazado o vencer. Concepto abstracto. | Se realiza en las cinco propuestas concretas. | Despacho y logística |
| 31 | **OfertaDespacho** | OfertaDespacho | Propuesta de un pedido a un chofer determinado, con vigencia limitada. | Cada intento de asignación del proceso de despacho. | Despacho y logística |
| 32 | **LoteRecorrido** † | LoteRecorrido | Grupo de pedidos que se entregan en un mismo viaje. | Cada lote armado por el módulo de agrupación. | Despacho y logística |
| 33 | **ParadaLote** † | ParadaLote | Pedido dentro de un lote, en su orden de entrega. | Cada parada de cada lote. | Despacho y logística |
| 34 | **OfertaLote** † | OfertaLote | Propuesta de un lote completo a un chofer. | Cada intento de asignación de un lote. | Despacho y logística |
| 35 | **Chofer** | Chofer | Perfil extendido de un Usuario que ejecuta las entregas. | Repartidores habilitados por una distribuidora. | Flota y choferes |
| 36 | **Vehiculo** | Vehiculo | Medio de transporte de la flota de una distribuidora. | Cada unidad de la flota de una distribuidora. | Flota y choferes |
| 37 | **AsignacionVehiculo** ‡ | AsignacionVehiculo | Clase de asociación entre Chofer y Vehiculo: qué chofer tiene en uso un vehículo de la flota en un momento dado, con historial. | Cada período de uso de un vehículo por un chofer. | Flota y choferes |
| 38 | **PlanMantenimiento** † | PlanMantenimiento | Regla que dice qué se controla de un vehículo o chofer, cada cuánto y si inhabilita al vencer. | Seguro, verificación técnica, licencia, services. | Flota y choferes |
| 39 | **TareaMantenimiento** † | TareaMantenimiento | Vencimiento concreto que genera un plan: una póliza, una verificación, un service. | Cada vencimiento proyectado, programado o cumplido. | Flota y choferes |
| 40 | **AdjuntoTarea** ‡ | AdjuntoTarea | Comprobante —foto o documento— que respalda una tarea de mantenimiento: la póliza, la oblea de la VTV, la licencia escaneada. | Cada archivo adjuntado a una tarea de mantenimiento. | Flota y choferes |
| 41 | **PropuestaVentanaTaller** † | PropuestaVentanaTaller | Ventana de taller ofrecida al chofer para cumplir una tarea. | Cada ventana ofrecida. | Flota y choferes |
| 42 | **UbicacionGPS** | UbicacionGPS | Posición geográfica del chofer mientras está conectado; es efímera y deja de existir en cuanto se desconecta. | La posición actual de cada chofer conectado. | Flota y choferes |
| 43 | **RegistroUsoVehiculo** † | RegistroUsoVehiculo | Uso diario de un vehículo: kilómetros, pedidos y horas en ruta. | Un registro por vehículo y día. | Flota y choferes |
| 44 | **PuestoDeTrabajo** § | PuestoDeTrabajo | Puesto que ocupa el personal de una distribuidora, con una categoría que gobierna las reglas que se le aplican; el nombre es libre. | Cada puesto definido por una distribuidora: chofer, ayudante, depósito, administración, vendedor y los que agregue. | Personal |
| 45 | **Empleado** § | Empleado | Persona que trabaja en una distribuidora, con su legajo, su puesto y su vínculo laboral; tenga o no cuenta de acceso. Un chofer es un empleado cuya cuenta tiene el perfil de reparto. | Cada persona con legajo, activa o egresada. | Personal |
| 46 | **JornadaDeTrabajo** § | JornadaDeTrabajo | Período de presencia de un empleado, con su ingreso y su egreso, cargado por el panel o marcado por el chofer. | Cada jornada abierta o cerrada de cada empleado. | Personal |
| 47 | **LicenciaLaboral** § | LicenciaLaboral | Ausencia justificada o no de un empleado durante un período —vacaciones, enfermedad, estudio, suspensión— que se solicita y un administrador aprueba o rechaza. | Cada licencia o ausencia solicitada, aprobada, rechazada o cancelada. | Personal |
| 48 | **Adjunto** | Adjunto | Archivo adjunto a un dueño, hoy el legajo de un empleado, con una etiqueta que dice qué es. Es genérico: otros módulos lo reutilizan. | Cada archivo adjuntado a un legajo. | Personal |
| 49 | **CargaCombustible** § | CargaCombustible | Carga de combustible de un vehículo, con su kilometraje y su importe; es la base del consumo y del costo por kilómetro. | Cada carga que registra el administrador o el chofer. | Gastos de la flota |
| 50 | **MultaTransito** § | MultaTransito | Multa de tránsito de un vehículo, con su ciclo de pendiente a pagada o anulada y, opcionalmente, imputada a un empleado. | Cada acta de infracción recibida por la distribuidora. | Gastos de la flota |
| 51 | **Siniestro** § | Siniestro | Hecho que daña a un vehículo o a terceros, con su ciclo de denunciado a cerrado y sus costos. No es una incidencia, que es un contratiempo de un pedido. | Cada accidente de un vehículo de la flota. | Gastos de la flota |
| 52 | **Neumatico** § | Neumatico | Neumático de la distribuidora, que está en depósito, montado en un vehículo o dado de baja. Funcionalidad opcional. | Cada neumático comprado por la distribuidora. | Gastos de la flota |
| 53 | **MovimientoNeumatico** § | MovimientoNeumatico | Asiento que no se modifica de un cambio de un neumático: montaje, desmontaje, rotación, recapado o baja. Funcionalidad opcional. | Cada movimiento de cada neumático. | Gastos de la flota |
| 54 | **Reclamo** | Reclamo | Queja formal del cliente sobre un pedido entregado, con evidencia opcional. | Cada reclamo registrado. | Posventa |
| 55 | **Incidencia** | Incidencia | Evento que interrumpe o altera el curso normal de una entrega. | Cada contratiempo reportado durante el reparto. | Posventa |
| 56 | **Calificacion** | Calificacion | Valoración que un cliente o un chofer asigna a la otra parte al cierre de un pedido. | Hasta dos por pedido: una del cliente al chofer y otra del chofer al cliente. | Posventa |
| 57 | **Deposito** § | Deposito | Lugar de la distribuidora —depósito o sucursal— donde se guarda el stock físico. | Cada depósito o sucursal dado de alta. | Stock físico y carga del camión |
| 58 | **UbicacionDeStock** § | UbicacionDeStock | Lugar donde puede haber stock: un depósito o un camión. Concentra los saldos y los movimientos de ambos. | Una por depósito y una por vehículo que se carga. | Stock físico y carga del camión |
| 59 | **SaldoDeStock** § | SaldoDeStock | Cantidad de un tipo de garrafa, en una condición (llena, vacía o defectuosa), dentro de una ubicación. | Un saldo por ubicación, tipo de garrafa y condición. | Stock físico y carga del camión |
| 60 | **MovimientoDeStock** § | MovimientoDeStock | Registro inmutable de un cambio de stock entre ubicaciones o con el exterior, con su motivo y el documento que lo originó. | Cada entrada, salida o traslado de garrafas. | Stock físico y carga del camión |
| 61 | **UmbralDeStock** § | UmbralDeStock | Mínimo de garrafas llenas de un tipo que debe tener un depósito, para avisar cuando baja. | Un umbral por depósito y tipo de garrafa controlado. | Stock físico y carga del camión |
| 62 | **AjusteDeStock** § | AjusteDeStock | Corrección del stock de una ubicación, con su motivo y una nota obligatoria. | Cada recuento corregido, merma, pérdida o hallazgo. | Stock físico y carga del camión |
| 63 | **ItemAjusteDeStock** § | ItemAjusteDeStock | Diferencia de un tipo de garrafa y condición dentro de un ajuste. | Cada renglón de cada ajuste. | Stock físico y carga del camión |
| 64 | **CargaDeCamion** § | CargaDeCamion | Hoja de carga: el turno de un camión, desde que sale cargado del depósito hasta que se rinde. | Una por camión y jornada. | Stock físico y carga del camión |
| 65 | **ItemCarga** § | ItemCarga | Por tipo de garrafa, lo que se cargó, repuso, entregó, declaró al regreso y la diferencia. | Cada renglón de cada hoja de carga. | Stock físico y carga del camión |
| 66 | **Proveedor** § | Proveedor | Empresa a la que la distribuidora le compra, principalmente una planta de llenado. | Cada proveedor dado de alta. | Compras |
| 67 | **OrdenDeCompra** § | OrdenDeCompra | Pedido de garrafas a un proveedor para un depósito destino, con su ciclo de estados. | Cada orden emitida. | Compras |
| 68 | **ItemOrdenDeCompra** § | ItemOrdenDeCompra | Tipo de garrafa pedido en una orden, con su costo y los vacíos que se entregan en canje. | Cada renglón de cada orden. | Compras |
| 69 | **RecepcionDeCompra** § | RecepcionDeCompra | Remito de ingreso de una compra, con o sin orden, que hace entrar garrafas llenas al stock. | Cada recepción registrada. | Compras |
| 70 | **ItemRecepcion** § | ItemRecepcion | Tipo de garrafa recibido en un remito, con los vacíos que se llevó la planta y el costo real. | Cada renglón de cada recepción. | Compras |
| 71 | **Caja** § | Caja | Cuenta de fondos de la distribuidora —efectivo, banco o billetera— con su saldo. | Cada caja que la distribuidora lleva, empezando por la «Caja central». | Caja y finanzas |
| 72 | **SesionDeCaja** § | SesionDeCaja | Período de trabajo de una caja entre una apertura y un cierre con arqueo. | Cada apertura y cierre de una caja de efectivo. | Caja y finanzas |
| 73 | **CategoriaDeCaja** § | CategoriaDeCaja | Clasificación de los ingresos y de los gastos de caja, propia o de sistema. | Las categorías de sistema sembradas y las que define cada distribuidora. | Caja y finanzas |
| 74 | **MovimientoDeCaja** § | MovimientoDeCaja | Asiento inmutable del libro de una caja: una entrada o una salida de dinero. | Cada ingreso, egreso, transferencia o anulación asentado en una caja. | Caja y finanzas |
| 75 | **RendicionChofer** § | RendicionChofer | Rendición diaria del efectivo que cobró un chofer, con lo esperado, lo declarado y la diferencia. | Una por chofer y por día con efectivo para rendir. | Caja y finanzas |
| 76 | **PedidoRendido** § | PedidoRendido | Pedido cobrado en efectivo que integra una rendición; un pedido se rinde una sola vez. | Cada pedido incluido en una rendición. | Caja y finanzas |
| 77 | **GastoDeRendicion** § | GastoDeRendicion | Gasto que el chofer pagó con la cobranza y declara al rendir. | Cada gasto declarado en una rendición. | Caja y finanzas |
| 78 | **CuentaCorriente** § | CuentaCorriente | Cuenta de un cliente en una distribuidora, con su límite de crédito, su plazo de pago y su saldo. | Una por cliente y distribuidora con crédito habilitado. | Caja y finanzas |
| 79 | **AsientoCuentaCorriente** § | AsientoCuentaCorriente | Asiento inmutable del libro de una cuenta corriente: cargo, pago, nota de crédito o de débito. | Cada cargo por venta, cobro y ajuste de cada cuenta. | Caja y finanzas |
| 80 | **ImputacionCuentaCorriente** § | ImputacionCuentaCorriente | Aplicación de un pago o una nota de crédito a un cargo, por orden de antigüedad. | Cada porción de un pago aplicada a un cargo. | Caja y finanzas |
| 81 | **ReglaComision** § | ReglaComision | Regla que dice cuánto gana un chofer por entrega, con su alcance y su vigencia. | Cada regla definida por la distribuidora. | Caja y finanzas |
| 82 | **AsientoComision** § | AsientoComision | Asiento inmutable del libro de comisiones de un chofer: una comisión o una deducción. | Cada comisión devengada y cada descuento de cada chofer. | Caja y finanzas |
| 83 | **LiquidacionComisiones** § | LiquidacionComisiones | Liquidación de las comisiones y las deducciones de un chofer en un período, con su neto a pagar. | Cada liquidación de cada chofer. | Caja y finanzas |

**La propuesta con vigencia.** Cinco conceptos comparten un mismo comportamiento: el
sistema le propone algo a alguien por un tiempo acotado —un pedido, un lote, una ventana
de taller, una reposición, el retiro de un envase— y espera que lo acepte, lo rechace o lo
deje vencer; si no prospera, pasa a la alternativa siguiente. Se modelan como
especializaciones de **PropuestaConVigencia**. Es el mecanismo que el despacho automático
ya usaba con la OfertaDespacho y sobre el que se construyen los módulos inteligentes.

---

### 1.3 Relaciones entre los Conceptos

La multiplicidad usa la notación UML (`1`, `0..1`, `0..*`, `1..*`, `0..2`): nunca `N`, que
no distingue «cero o más» de «uno o más». Cada multiplicidad se contrasta con la
nulabilidad o la unicidad de la columna real cuando es posible; donde la base es más laxa que la
regla de negocio, se explica en la nota que sigue a la tabla.

**Categorías de asociación (Larman).** Las relaciones se agrupan por categoría, con el
formato «A es una parte física de B — ejemplo». Un ejemplo por categoría, tomado del
modelo:

| Categoría de la relación | Ejemplos |
|---|---|
| A es parte física de B | ParadaLote – LoteRecorrido |
| A es parte lógica de B | AdjuntoTarea – TareaMantenimiento |
| A es una línea de transacción de B | ItemPedido – Pedido |
| A es un registro de B | MovimientoEnvase – Envase |
| A es miembro de / empleado de B | Chofer – Distribuidora |
| A usa o gestiona B | Cliente – Producto |
| A es una descripción para B | Producto – Envase (patrón descripción de artículo) |
| A está relacionado con una transacción B | ZonaCobertura – Pedido (el recargo que aplicó) |
| A es propiedad de / está en poder de B | Envase – Cliente |

La tabla completa (158 asociaciones y 8 especializaciones) queda con la categoría de cada una
en su columna. El nombre de cada asociación se lee de izquierda a derecha, del Concepto A al
Concepto B, en voz activa («Cliente realiza Pedido»); la multiplicidad se da en el mismo orden
(la del extremo A, «a», la del extremo B). Chofer y Vehiculo se relacionan de dos maneras
distintas: **tiene registrado** es el vehículo que figura a nombre del chofer y es permanente
(cada vehículo tiene exactamente un chofer titular), mientras que **usa** es el uso efectivo
en un momento dado y es una asociación con clase de asociación, AsignacionVehiculo, que guarda
el período de cada uso; a lo sumo un chofer tiene en uso un vehículo abierto y a lo sumo un
vehículo está abierto para un chofer.

| Relación | Concepto A | Concepto B | Tipo | Multiplicidad | Categoría (Larman) |
|----------|-----------|-----------|------|---------------|---------------------|
| Es un tipo de | Cliente | Usuario | Especialización | — | — |
| Es un tipo de | Chofer | Usuario | Especialización | — | — |
| Es un tipo de | Administrador | Usuario | Especialización | — | — |
| Es un tipo de | OfertaDespacho | PropuestaConVigencia | Especialización | — | — |
| Es un tipo de | OfertaLote | PropuestaConVigencia | Especialización | — | — |
| Es un tipo de | PropuestaVentanaTaller | PropuestaConVigencia | Especialización | — | — |
| Es un tipo de | InvitacionRecompra | PropuestaConVigencia | Especialización | — | — |
| Es un tipo de | AvisoRecupero | PropuestaConVigencia | Especialización | — | — |
| Tiene asignado | Usuario | Rol | Asociación | 0..* a 0..1 | Descripción para |
| Emplea | Distribuidora | Chofer | Asociación | 1 a 0..* | Es miembro de / empleado de |
| Emplea | Distribuidora | Administrador | Asociación | 0..1 a 0..* | Es miembro de / empleado de |
| Emplea | Distribuidora | Empleado | Asociación | 1 a 0..* | Es miembro de / empleado de |
| Define | Distribuidora | PuestoDeTrabajo | Composición | 1 a 0..* | Parte lógica de |
| Comercializa | Distribuidora | Producto | Asociación | 1 a 0..* | Usa o gestiona |
| Posee | Distribuidora | Envase | Asociación | 1 a 0..* | Es propiedad de |
| Gestiona | Distribuidora | Pedido | Asociación | 1 a 0..* | Usa o gestiona |
| Define | Distribuidora | ZonaCobertura | Composición | 1 a 0..* | Parte lógica de |
| Define | Distribuidora | FranjaHoraria | Composición | 1 a 0..* | Parte lógica de |
| Parametriza | Distribuidora | ConfiguracionModulo | Composición | 1 a 0..* | Descripción para |
| Origina | Usuario | AsientoAuditoria | Asociación | 0..1 a 0..* | Es un registro de |
| Realiza | Usuario | Auditoria | Asociación | 0..1 a 0..* | Es un registro de |
| Delimita | Distribuidora | Auditoria | Asociación | 0..1 a 0..* | Es un registro de |
| Detalla con | Auditoria | DetalleAuditoria | Composición | 1 a 0..* | Es una línea de transacción de |
| Clasifica | TipoAccionAuditoria | Auditoria | Asociación | 1 a 0..* | Descripción para |
| Registra | Cliente | DireccionEntrega | Composición | 1 a 0..* | Parte lógica de |
| Realiza | Cliente | Pedido | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Arma | Cliente | Carrito | Composición | 1 a 0..* | Está relacionado con una transacción |
| Recibe | Cliente | InvitacionRecompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Usa habitualmente | Cliente | Producto | Asociación | 0..* a 0..1 | Usa o gestiona |
| Se convierte en | InvitacionRecompra | Pedido | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Sugiere | InvitacionRecompra | ItemSugerido | Composición | 1 a 1..* | Es una línea de transacción de |
| Sugiere entregar en | InvitacionRecompra | DireccionEntrega | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Corresponde a | ItemSugerido | Producto | Asociación | 0..* a 1 | Descripción para |
| Contiene | Carrito | ItemCarrito | Composición | 1 a 0..* | Es una línea de transacción de |
| Corresponde a | ItemCarrito | Producto | Asociación | 0..* a 1 | Descripción para |
| Contiene | Pedido | ItemPedido | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemPedido | Producto | Asociación | 0..* a 1 | Descripción para |
| Se entrega en | Pedido | DireccionEntrega | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Se programa en | Pedido | FranjaHoraria | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Aplica el recargo de | Pedido | ZonaCobertura | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Registra | Pedido | CambioEstadoPedido | Composición | 1 a 0..* | Es un registro de |
| Efectúa | Usuario | CambioEstadoPedido | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Registra | Pedido | CambioDireccion | Composición | 1 a 0..* | Es un registro de |
| Cambia desde | CambioDireccion | DireccionEntrega | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Cambia hacia | CambioDireccion | DireccionEntrega | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Realiza | Usuario | CambioDireccion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Entrega | Chofer | Pedido | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Se salda con | Pedido | Pago | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Genera | Pedido | OfertaDespacho | Composición | 1 a 0..* | Está relacionado con una transacción |
| Se dirige a | OfertaDespacho | Chofer | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Se compone de | LoteRecorrido | ParadaLote | Composición | 1 a 1..* | Parte física de |
| Atiende | ParadaLote | Pedido | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Genera | LoteRecorrido | OfertaLote | Composición | 1 a 0..* | Está relacionado con una transacción |
| Se dirige a | OfertaLote | Chofer | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Acepta | Chofer | LoteRecorrido | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Tiene registrado | Chofer | Vehiculo | Asociación (clase de asociación AsignacionVehiculo) | 1 a 0..* | Usa o gestiona |
| Usa | Chofer | Vehiculo | Asociación (clase de asociación AsignacionVehiculo) | 0..* a 0..* | Usa o gestiona |
| Se ubica en | Chofer | UbicacionGPS | Asociación | 1 a 0..1 | Descripción para |
| Genera | PlanMantenimiento | TareaMantenimiento | Asociación | 1 a 0..* | Es un registro de |
| Habilita | TareaMantenimiento | Vehiculo | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Habilita | TareaMantenimiento | Chofer | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Origina | TareaMantenimiento | PropuestaVentanaTaller | Composición | 1 a 0..* | Está relacionado con una transacción |
| Adjunta | TareaMantenimiento | AdjuntoTarea | Composición | 1 a 0..* | Parte lógica de |
| Se dirige a | PropuestaVentanaTaller | Chofer | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Acumula | Vehiculo | RegistroUsoVehiculo | Composición | 1 a 0..* | Es un registro de |
| Ofrece | Producto | Promocion | Composición | 1 a 0..* | Descripción para |
| Describe | Producto | Envase | Asociación | 0..1 a 0..* | Descripción para |
| Registra | Envase | MovimientoEnvase | Composición | 1 a 0..* | Es un registro de |
| Se somete a | Envase | RevisionEnvase | Composición | 1 a 0..* | Es un registro de |
| Origina | Pedido | MovimientoEnvase | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Ejecuta | Usuario | MovimientoEnvase | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Tiene en su poder | Cliente | Envase | Asociación | 0..1 a 0..* | Es propiedad de / está en poder de |
| Despacha | Pedido | Envase | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Motiva | Envase | CasoRecupero | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Se abre contra | CasoRecupero | Cliente | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Resuelve | Usuario | CasoRecupero | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Emite | CasoRecupero | AvisoRecupero | Composición | 1 a 0..* | Es un registro de |
| Ocupa | Empleado | PuestoDeTrabajo | Asociación | 0..* a 1 | Descripción para |
| Accede con | Empleado | Usuario | Asociación | 0..1 a 0..1 | Usa o gestiona |
| Registra | Empleado | JornadaDeTrabajo | Composición | 1 a 0..* | Es un registro de |
| Solicita | Empleado | LicenciaLaboral | Composición | 1 a 0..* | Está relacionado con una transacción |
| Resuelve | Usuario | LicenciaLaboral | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Conserva | Empleado | Adjunto | Composición | 1 a 0..* | Parte lógica de |
| Habilita | TareaMantenimiento | Empleado | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Registra | Vehiculo | CargaCombustible | Composición | 1 a 0..* | Es un registro de |
| Acumula | Vehiculo | MultaTransito | Composición | 1 a 0..* | Es un registro de |
| Sufre | Vehiculo | Siniestro | Composición | 1 a 0..* | Es un registro de |
| Monta | Vehiculo | Neumatico | Asociación | 0..1 a 0..* | Usa o gestiona |
| Posee | Distribuidora | Neumatico | Composición | 1 a 0..* | Es propiedad de |
| Registra | Neumatico | MovimientoNeumatico | Composición | 1 a 0..* | Es un registro de |
| Ocurre en | MovimientoNeumatico | Vehiculo | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Carga | Empleado | CargaCombustible | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Responde por | Empleado | MultaTransito | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Interviene en | Empleado | Siniestro | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Origina | Pedido | Reclamo | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Presenta | Cliente | Reclamo | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Origina | Pedido | Incidencia | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Reporta | Usuario | Incidencia | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Recibe | Pedido | Calificacion | Asociación | 1 a 0..2 | Está relacionado con una transacción |
| Emite | Usuario | Calificacion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Recibe | Usuario | Calificacion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Dispone de | Distribuidora | Deposito | Asociación | 1 a 0..* | Es propiedad de |
| Compra a | Distribuidora | Proveedor | Asociación | 1 a 0..* | Usa o gestiona |
| Se registra como {xor} | Deposito | UbicacionDeStock | Asociación | 1 a 0..1 | Descripción para |
| Se registra como {xor} | Vehiculo | UbicacionDeStock | Asociación | 1 a 0..1 | Descripción para |
| Acumula | UbicacionDeStock | SaldoDeStock | Composición | 1 a 0..* | Es un registro de |
| Corresponde a | SaldoDeStock | Producto | Asociación | 0..* a 1 | Descripción para |
| Corresponde a | MovimientoDeStock | Producto | Asociación | 0..* a 1 | Descripción para |
| Sale de | MovimientoDeStock | UbicacionDeStock | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Entra en | MovimientoDeStock | UbicacionDeStock | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Ejecuta | Usuario | MovimientoDeStock | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Fija | Deposito | UmbralDeStock | Composición | 1 a 0..* | Parte lógica de |
| Controla | UmbralDeStock | Producto | Asociación | 0..* a 1 | Descripción para |
| Se corrige con | UbicacionDeStock | AjusteDeStock | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Contiene | AjusteDeStock | ItemAjusteDeStock | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemAjusteDeStock | Producto | Asociación | 0..* a 1 | Descripción para |
| Registra | Usuario | AjusteDeStock | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Recibe | Proveedor | OrdenDeCompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Se destina a | OrdenDeCompra | Deposito | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Contiene | OrdenDeCompra | ItemOrdenDeCompra | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemOrdenDeCompra | Producto | Asociación | 0..* a 1 | Descripción para |
| Emite | Usuario | OrdenDeCompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Entrega | Proveedor | RecepcionDeCompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Se cumple con | OrdenDeCompra | RecepcionDeCompra | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Ingresa en | RecepcionDeCompra | Deposito | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Contiene | RecepcionDeCompra | ItemRecepcion | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemRecepcion | Producto | Asociación | 0..* a 1 | Descripción para |
| Registra | Usuario | RecepcionDeCompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Transporta | Vehiculo | CargaDeCamion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Reparte con | Chofer | CargaDeCamion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Parte de | CargaDeCamion | UbicacionDeStock | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Contiene | CargaDeCamion | ItemCarga | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemCarga | Producto | Asociación | 0..* a 1 | Descripción para |
| Abre | Usuario | CargaDeCamion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Cierra | Usuario | CargaDeCamion | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Define | Distribuidora | Caja | Composición | 1 a 0..* | Parte lógica de |
| Define | Distribuidora | CategoriaDeCaja | Composición | 1 a 0..* | Parte lógica de |
| Lleva | Distribuidora | CuentaCorriente | Composición | 1 a 0..* | Parte lógica de |
| Define | Distribuidora | ReglaComision | Composición | 1 a 0..* | Parte lógica de |
| Registra | Caja | SesionDeCaja | Composición | 1 a 0..* | Es un registro de |
| Asienta | Caja | MovimientoDeCaja | Composición | 1 a 0..* | Es un registro de |
| Agrupa | SesionDeCaja | MovimientoDeCaja | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Clasifica | CategoriaDeCaja | MovimientoDeCaja | Asociación | 1 a 0..* | Descripción para |
| Anula a | MovimientoDeCaja | MovimientoDeCaja | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Presenta | Chofer | RendicionChofer | Composición | 1 a 0..* | Está relacionado con una transacción |
| Ingresa en | RendicionChofer | Caja | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Genera | RendicionChofer | MovimientoDeCaja | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Rinde | RendicionChofer | PedidoRendido | Composición | 1 a 0..* | Es una línea de transacción de |
| Corresponde a | PedidoRendido | Pedido | Asociación | 0..1 a 1 | Descripción para |
| Declara | RendicionChofer | GastoDeRendicion | Composición | 1 a 0..* | Es una línea de transacción de |
| Se clasifica en | GastoDeRendicion | CategoriaDeCaja | Asociación | 0..* a 1 | Descripción para |
| Tiene habilitada | Cliente | CuentaCorriente | Asociación | 1 a 0..* | Usa o gestiona |
| Registra | CuentaCorriente | AsientoCuentaCorriente | Composición | 1 a 0..* | Es un registro de |
| Origina | Pedido | AsientoCuentaCorriente | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Se asienta en | AsientoCuentaCorriente | MovimientoDeCaja | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Cobra | Chofer | AsientoCuentaCorriente | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Incluye | RendicionChofer | AsientoCuentaCorriente | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Anula a | AsientoCuentaCorriente | AsientoCuentaCorriente | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Salda | ImputacionCuentaCorriente | AsientoCuentaCorriente | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Se aplica con | ImputacionCuentaCorriente | AsientoCuentaCorriente | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Se aplica a | ReglaComision | Empleado | Asociación | 0..* a 0..1 | Descripción para |
| Se aplica a | ReglaComision | Producto | Asociación | 0..* a 0..1 | Descripción para |
| Devenga | Empleado | AsientoComision | Composición | 1 a 0..* | Es un registro de |
| Percibe | Empleado | LiquidacionComisiones | Composición | 1 a 0..* | Está relacionado con una transacción |
| Actúa como | Empleado | Chofer | Asociación | 0..1 a 0..1 | Usa o gestiona |
| Corresponde a | AsientoComision | Pedido | Asociación | 0..* a 0..1 | Descripción para |
| Determina | ReglaComision | AsientoComision | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Incluye | LiquidacionComisiones | AsientoComision | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Origina | RendicionChofer | AsientoComision | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Se paga con | LiquidacionComisiones | MovimientoDeCaja | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |

**Nota sobre Producto y Envase.** El modelo distingue deliberadamente dos conceptos que
en el lenguaje corriente se confunden. **Producto** es el *tipo* de garrafa que se
comercializa —"garrafa de 10 kg", con su precio y su stock agregado—; **Envase** es el
*botellón físico* individual, con número de serie, que la distribuidora entrega y espera
recuperar. El cliente compra un Producto pero recibe un Envase, y es ese envase concreto
—no el tipo— el que hay que rastrear y recuperar.

**Nota sobre el personal.** Todo empleado existe como legajo, tenga o no cuenta de acceso: el vínculo con el usuario (asociación «accede con») es opcional, y un chofer es el empleado cuya cuenta tiene el perfil de reparto. Por eso no hay una asociación directa entre Empleado y Chofer: se llega por el Usuario. La licencia de conducir, el curso de mercancías peligrosas, el examen psicofísico y el alta en la ART no son conceptos nuevos: son TareaMantenimiento de un PlanMantenimiento cuyo sujeto es el empleado, y por eso la tarea se asocia a un vehículo, a un chofer (asociación heredada que el módulo reemplaza) o a un empleado. Los adjuntos se asocian a su dueño sin clave foránea, porque el dueño es polimórfico; el modelo conceptual los une al Empleado por «conserva».

**Nota sobre el mantenimiento de la flota.** El seguro, la verificación técnica, la
licencia del chofer y los services no son conceptos distintos: son **PlanMantenimiento**
con distinto disparo y distinta criticidad, y cada vencimiento concreto es una
**TareaMantenimiento**. La licencia es del chofer y no del vehículo, por eso la tarea se
asocia a uno o al otro.

**Nota sobre la multiplicidad de Envase–Producto.** La regla de negocio podría exigir
que todo envase tenga siempre un tipo de garrafa asociado (multiplicidad `1`), pero la
base modela la relación como opcional (`0..1`, con `ON DELETE SET NULL`): un envase puede
quedar sin tipo si el producto que lo originó se da de baja. El modelo adopta la
multiplicidad de la base porque es la que efectivamente se cumple; si en algún momento se
decide que un envase sin tipo es un estado inválido, corresponde agregar una restricción
en el backend antes de endurecer esta multiplicidad.

---

### 1.4 Descripción de los Atributos

Los nombres de atributo van en lenguaje natural, sin `snake_case`: la notación de
identificador de columna es del modelo de datos (Documento 3), no del modelo conceptual.
Los atributos derivados —los que se calculan a partir de otros datos del sistema y no se
piden ni se guardan por separado— llevan `/` adelante, como indica la notación UML.

| Concepto | Atributo – Descripción |
|----------|------------------------|
| **Distribuidora** | nombre: Nombre comercial, el que ve el cliente. |
| **Distribuidora** | razón social: Nombre legal de la empresa comercializadora. |
| **Distribuidora** | CUIT: Identificación tributaria de la empresa. No funciona como clave —hay distribuidoras con el mismo valor—; corregirlo es una tarea del modelo de datos, no del dominio. |
| **Distribuidora** | estado: Si la distribuidora puede operar en la plataforma o está suspendida. |
| **Usuario** | nombre: Nombre completo. |
| **Usuario** | correo: Correo único. Identifica al usuario en la autenticación. |
| **Usuario** | teléfono: Teléfono de contacto. |
| **Usuario** | bloqueado: Si la cuenta está suspendida y no puede operar. |
| **Rol** | tipo: Cliente, chofer, administrador o administrador general. |
| **ConfiguracionModulo** | módulo: Proceso automático al que corresponden los parámetros. |
| **ConfiguracionModulo** | parámetros: Valores con que la distribuidora ajusta el proceso. |
| **AsientoAuditoria** | operación: Alta, modificación o baja. |
| **AsientoAuditoria** | recurso: Sobre qué tipo de dato se operó. |
| **AsientoAuditoria** | aplicación: Desde qué aplicación: panel, app de cliente o app de chofer. |
| **AsientoAuditoria** | resultado: Si la operación fue exitosa o fallida. |
| **AsientoAuditoria** | cambios: Qué cambió, con las credenciales depuradas. |
| **AsientoAuditoria** | fecha: Cuándo ocurrió. |
| **Auditoria** | entidad afectada: Nombre de la entidad de dominio cuyo registro cambió, por ejemplo Pedido. |
| **Auditoria** | fecha y hora: Cuándo se confirmó el cambio. |
| **DetalleAuditoria** | campo: Propiedad de la entidad que cambió. |
| **DetalleAuditoria** | valor anterior: Valor antes del cambio; vacío en un alta. |
| **DetalleAuditoria** | valor nuevo: Valor después del cambio; vacío en una baja. |
| **TipoAccionAuditoria** | nombre: Alta, Modificación, Baja lógica, Reactivación o Baja física. |
| **Cliente** | consumo mensual declarado: Kilos de gas por mes que el cliente declara consumir. |
| **Cliente** | días de aviso: Con cuántos días de anticipación quiere que se le avise la recompra. |
| **DireccionEntrega** | calle y altura: Domicilio de entrega. |
| **DireccionEntrega** | piso y departamento: Unidad dentro del edificio, si corresponde. |
| **DireccionEntrega** | punto: Ubicación geográfica resuelta contra el servicio de mapas. |
| **DireccionEntrega** | precisión: Con qué exactitud quedó resuelto el punto: exacta, aproximada o sin resolver. |
| **DireccionEntrega** | predeterminada: Si es la que se propone por defecto al armar un pedido. |
| **InvitacionRecompra** | agotamiento estimado: Cuándo se estima que al cliente se le termina el gas. |
| **ItemSugerido** | cantidad: Unidades sugeridas de ese producto. |
| **Producto** | tipo: Formato comercializado: 10 kg, 15 kg o 45 kg. |
| **Producto** | peso en kilos: Kilos de gas del formato. |
| **Producto** | precio: Precio de venta vigente. |
| **Producto** | stock: Unidades que se pueden vender: lo lleno en depósitos y camiones menos lo reservado por pedidos abiertos. El stock físico por ubicación está en SaldoDeStock. |
| **Producto** | activo: Si está a la venta. |
| **Promocion** | cantidad: Cantidad mínima a partir de la cual se aplica el descuento. |
| **Promocion** | descuento: Porcentaje que se descuenta al alcanzar esa cantidad. |
| **Envase** | número de serie: Número grabado en el botellón. Lo identifica unívocamente. |
| **Envase** | estado: Situación actual: en depósito, lleno, despachado, en poder del cliente o devuelto vacío. |
| **Envase** | monto del depósito: Importe en garantía que representa el envase. |
| **Envase** | /vencimiento: Fecha hasta la que el envase puede despacharse. Se deriva de la fecha de su última revisión aprobada. |
| **MovimientoEnvase** | desde / hacia: Situación anterior y posterior del envase. |
| **MovimientoEnvase** | fecha: Momento en que se produjo el movimiento. |
| **RevisionEnvase** | fecha: Cuándo se hizo la revisión. |
| **RevisionEnvase** | resultado: Apta, apta con salvedades o rechazada. |
| **RevisionEnvase** | próxima revisión: Hasta cuándo vale esta revisión. |
| **CasoRecupero** | escalón: Paso de la gestión en que está el caso. |
| **CasoRecupero** | depósito comprometido: Importe en juego. |
| **CasoRecupero** | estado: Abierto, devuelto, escalado, depósito cobrado, dado de baja o cerrado sin cargo. |
| **CasoRecupero** | resolución: Lo que decidió el administrador, si llegó a él. |
| **AvisoRecupero** | escalón: Paso de la gestión al que pertenece. |
| **AvisoRecupero** | tipo: Recordatorio, oferta de retiro o aviso de depósito. |
| **AvisoRecupero** | vence: Plazo del escalón. |
| **Carrito** | última modificación: Cuándo se tocó por última vez. |
| **ItemCarrito** | cantidad: Unidades cargadas. |
| **ItemCarrito** | precio unitario: Precio vigente al momento de agregarlo. |
| **Pedido** | estado: Ciclo de vida: reservado, pendiente, aceptado, en camino, entregado, cancelado. |
| **Pedido** | /total: Monto total. Se deriva de sus ítems, sus promociones y el recargo de la zona. |
| **Pedido** | modalidad de entrega: Reparto programado o express. |
| **Pedido** | fecha agendada: Fecha para la que el cliente programó la entrega. |
| **Pedido** | método de pago: Efectivo, MercadoPago o transferencia. |
| **Pedido** | seña: Importe adelantado en una reserva programada. Cero en un pedido normal. |
| **Pedido** | código de entrega: Código secreto que prueba, al escanearlo, que el chofer estuvo presente en la entrega. |
| **Pedido** | nombre de quien recibe: Si no es el cliente, nombre de la persona que recibe el pedido. |
| **Pedido** | documento de quien recibe: Documento de esa persona. |
| **Pedido** | vínculo con quien recibe: Relación con el cliente: familiar, encargado, vecino. |
| **ItemPedido** | cantidad: Unidades solicitadas. |
| **ItemPedido** | precio unitario: Precio con el que se vendió el renglón, con las promociones por volumen ya aplicadas y redondeado a centavos; se conserva aunque el producto cambie de precio. |
| **ItemPedido** | /subtotal: Cantidad por precio unitario. |
| **CambioEstadoPedido** | desde / hacia: Estado anterior y nuevo. |
| **CambioEstadoPedido** | motivo: Por qué, cuando la transición lo pide. |
| **CambioEstadoPedido** | fecha: Cuándo. |
| **CambioDireccion** | motivo: Motivo declarado del cambio. |
| **CambioDireccion** | fecha: Cuándo se cambió. |
| **ZonaCobertura** | nombre: Denominación de la zona. |
| **ZonaCobertura** | área: Polígono que delimita el área de cobertura. |
| **ZonaCobertura** | recargo: Valor adicional que se aplica a las entregas dentro de la zona. |
| **ZonaCobertura** | tipo de recargo: Si el recargo es un monto fijo o un porcentaje del pedido. |
| **ZonaCobertura** | vigente hasta: Momento en que la zona deja de aplicarse. Vacío, sin vencimiento. |
| **FranjaHoraria** | desde / hasta: Rango horario que abarca la franja. |
| **FranjaHoraria** | cupo: Máximo de pedidos que la franja acepta por día. |
| **FranjaHoraria** | activa: Si se puede elegir al armar un pedido. |
| **Pago** | importe: Importe de la transacción. |
| **Pago** | pasarela: Pasarela que procesa la transacción. |
| **Pago** | estado: Situación del cobro ante la pasarela. |
| **Pago** | es seña: Si este cobro corresponde a la seña de una reserva programada. |
| **Pago** | fecha: Cuándo se intentó el cobro. |
| **PropuestaConVigencia** | estado: Pendiente, aceptada, rechazada o vencida. |
| **PropuestaConVigencia** | vence: Momento en que la propuesta pierde vigencia. |
| **LoteRecorrido** | estado: En armado, ofrecido, asignado, deshecho o completado. |
| **LoteRecorrido** | /peso total: Suma del peso de los pedidos del lote. |
| **ParadaLote** | orden: Posición del pedido en el recorrido. |
| **Chofer** | disponible: Si está disponible para recibir ofertas en este momento. |
| **Chofer** | habilitado: Si el administrador lo habilitó para recibir pedidos. |
| **Chofer** | validado: Si superó la validación de su documentación al registrarse. |
| **Chofer** | /calificación: Promedio de las valoraciones que recibió de los clientes. |
| **Vehiculo** | patente: Dominio del vehículo. |
| **Vehiculo** | tipo: Moto, utilitario o camión. |
| **Vehiculo** | carga máxima: Kilos que puede llevar, descontada la tara. |
| **Vehiculo** | kilometraje: Última lectura del odómetro. Base de la proyección de mantenimiento. |
| **Vehiculo** | estado en la flota: Activo, en taller o inhabilitado. |
| **Vehiculo** | tipo de combustible: Combustible que usa el vehículo; es el que se propone en cada carga (planificado, I-12). |
| **Vehiculo** | capacidad del tanque: Litros que entran en el tanque; una carga no puede superarlos en más de un 5 % (planificado, I-12). |
| **AsignacionVehiculo** | asignado el: Fecha y hora en que el vehículo pasó a estar en uso de ese chofer. |
| **AsignacionVehiculo** | liberado el: Fecha y hora en que dejó de estarlo; vacío mientras sigue en uso. |
| **AsignacionVehiculo** | nota: Observación libre del administrador al asignar o liberar (opcional). |
| **UbicacionGPS** | latitud / longitud: Coordenadas actuales del chofer. |
| **PlanMantenimiento** | nombre: Seguro, verificación técnica, licencia, cambio de aceite... |
| **PlanMantenimiento** | disparo: Por kilómetros, por tiempo o por fecha fija. |
| **PlanMantenimiento** | intervalo: Cada cuántos kilómetros o meses se repite. |
| **PlanMantenimiento** | anticipación: Con cuánta anticipación se empieza a planificar. |
| **PlanMantenimiento** | criticidad: Si al vencer inhabilita al vehículo o al chofer. |
| **PlanMantenimiento** | documento que controla: Qué documento controla el plan (seguro, verificación técnica, licencia, curso, examen, alta en la ART): le dice al panel qué formulario mostrar. Planificado (I-11). |
| **PlanMantenimiento** | aplica a: Categorías de puesto a las que aplica el plan; vacío significa todas. Planificado (I-11). |
| **TareaMantenimiento** | estado: Proyectada, programada, en curso, hecha, vencida o cancelada. |
| **TareaMantenimiento** | vence: Fecha o kilometraje de vencimiento. |
| **TareaMantenimiento** | vencimiento proyectado: Fecha estimada por el planificador. |
| **TareaMantenimiento** | prestador: Aseguradora, taller o ente emisor. |
| **TareaMantenimiento** | número: Póliza, número de licencia u oblea. |
| **TareaMantenimiento** | costo: Importe del trabajo. |
| **TareaMantenimiento** | vigente desde: Inicio de la vigencia de la póliza o de la habilitación; lo usa el prorrateo de la prima (planificado, I-12). |
| **TareaMantenimiento** | detalle: Detalle de la póliza (cobertura, franquicia, cuotas) o de la habilitación (planificado, I-12). |
| **AdjuntoTarea** | nombre original: Nombre del archivo tal como lo subió quien lo cargó. |
| **AdjuntoTarea** | tipo de archivo: Formato del adjunto: imagen o PDF. |
| **AdjuntoTarea** | fecha de carga: Cuándo se subió. |
| **PropuestaVentanaTaller** | desde / hasta: Ventana de taller ofrecida. |
| **RegistroUsoVehiculo** | día: Día registrado. |
| **RegistroUsoVehiculo** | kilómetros: Kilómetros recorridos ese día. |
| **RegistroUsoVehiculo** | pedidos: Pedidos entregados ese día. |
| **PuestoDeTrabajo** | nombre: Nombre del puesto; único entre los vigentes de la distribuidora. |
| **PuestoDeTrabajo** | categoría: Chofer, ayudante, depósito, administración, ventas, dirección u otra: gobierna las reglas. |
| **PuestoDeTrabajo** | activo: Si el puesto se ofrece. |
| **Empleado** | legajo: Número de legajo, único por distribuidora. |
| **Empleado** | nombre: Nombre de pila. |
| **Empleado** | apellido: Apellido. |
| **Empleado** | documento: Tipo y número de documento, únicos por distribuidora. |
| **Empleado** | CUIL: Código de identificación laboral, con dígito verificador válido. |
| **Empleado** | fecha de nacimiento: Día de nacimiento. |
| **Empleado** | domicilio: Domicilio, localidad y provincia. |
| **Empleado** | teléfono: Teléfono de contacto. |
| **Empleado** | contacto de emergencia: Nombre, teléfono y vínculo de a quién avisar. |
| **Empleado** | fecha de ingreso: Día en que empezó a trabajar. |
| **Empleado** | fecha de egreso: Día en que dejó de trabajar; vacío mientras está activo. |
| **Empleado** | motivo de egreso: Renuncia, despido, fin de contrato, jubilación u otro. |
| **Empleado** | modalidad de contratación: Permanente, a plazo fijo, de jornada parcial o contratista. |
| **Empleado** | estado: Activo o egresado. |
| **JornadaDeTrabajo** | día: Día argentino del ingreso. |
| **JornadaDeTrabajo** | ingreso: Instante en que empezó. |
| **JornadaDeTrabajo** | egreso: Instante en que terminó; vacío mientras está abierta. |
| **JornadaDeTrabajo** | origen: Panel o aplicación del chofer. |
| **JornadaDeTrabajo** | observación: Nota que explica una corrección. |
| **LicenciaLaboral** | tipo: Vacaciones, enfermedad, accidente de trabajo, estudio, casamiento, nacimiento, duelo, sin goce, suspensión, ausencia injustificada u otra. |
| **LicenciaLaboral** | desde / hasta: Primer y último día, inclusive. |
| **LicenciaLaboral** | /días: Días corridos del período; derivado de las fechas. |
| **LicenciaLaboral** | estado: Solicitada, aprobada, rechazada o cancelada. |
| **LicenciaLaboral** | motivo: Razón de la solicitud. |
| **LicenciaLaboral** | motivo de rechazo: Razón por la que no se concedió; obligatoria al rechazar. |
| **LicenciaLaboral** | resuelta el: Instante en que se aprobó o rechazó. |
| **Adjunto** | nombre original: Nombre con que se subió el archivo. |
| **Adjunto** | tipo de archivo: Imagen o PDF. |
| **Adjunto** | etiqueta: Qué es el archivo («DNI frente»). |
| **Adjunto** | fecha de carga: Cuándo se subió. |
| **CargaCombustible** | fecha y hora: Cuándo se hizo la carga. |
| **CargaCombustible** | tipo de combustible: Diésel, nafta, gas natural comprimido o gas licuado. |
| **CargaCombustible** | litros: Litros cargados. |
| **CargaCombustible** | precio por litro: Precio de cada litro. |
| **CargaCombustible** | importe: Importe total; coincide con los litros por el precio, con un 1 % de tolerancia. |
| **CargaCombustible** | kilometraje: Kilometraje del tablero; no puede ser menor que el de la carga anterior. |
| **CargaCombustible** | tanque lleno: Si se llenó el tanque: es la base del cálculo de consumo. |
| **CargaCombustible** | estación: Estación de servicio. |
| **CargaCombustible** | medio de pago: Caja, efectivo del chofer, tarjeta o cuenta corriente de combustible. |
| **CargaCombustible** | comprobante: Número del comprobante. |
| **CargaCombustible** | anómala: Si el consumo del tramo se aparta más de un 25 % del promedio de las últimas cinco cargas. |
| **CargaCombustible** | observación: Nota de quien cargó. |
| **CargaCombustible** | anulada el: Cuándo se anuló; una carga anulada no cuenta en los cálculos. |
| **MultaTransito** | fecha de la infracción: Cuándo ocurrió la infracción. |
| **MultaTransito** | jurisdicción: Jurisdicción que labró el acta. |
| **MultaTransito** | número de acta: Número del acta; único por distribuidora y jurisdicción. |
| **MultaTransito** | infracción: Descripción de la infracción. |
| **MultaTransito** | importe: Importe de la multa. |
| **MultaTransito** | importe con pago voluntario: Importe con el descuento por pagar antes. |
| **MultaTransito** | vencimiento: Fecha límite del pago. |
| **MultaTransito** | estado: Pendiente, apelada, pagada o anulada. |
| **MultaTransito** | pagada el: Cuándo se pagó. |
| **MultaTransito** | importe pagado: Importe efectivamente pagado. |
| **MultaTransito** | imputada al chofer: Si la asume el empleado y no la distribuidora. |
| **MultaTransito** | avisada el: Cuándo se avisó del vencimiento, para no repetir el aviso. |
| **MultaTransito** | motivo de anulación: Motivo con el que se anuló; obligatorio al anular. |
| **Siniestro** | fecha: Cuándo ocurrió. |
| **Siniestro** | ubicación: Punto donde ocurrió. |
| **Siniestro** | domicilio: Domicilio aproximado. |
| **Siniestro** | descripción: Qué pasó. |
| **Siniestro** | hubo heridos: Si hubo personas heridas. |
| **Siniestro** | hubo terceros: Si hubo terceros involucrados. |
| **Siniestro** | derrame de GLP: Si hubo fuga o derrame de gas: obliga a avisar. |
| **Siniestro** | denuncia policial: Número de la denuncia. |
| **Siniestro** | reclamo al seguro: Número del reclamo a la aseguradora. |
| **Siniestro** | estado: Denunciado, en revisión, en reparación o cerrado. |
| **Siniestro** | vehículo inutilizable: Si el vehículo no puede circular y pasa a fuera de servicio. |
| **Siniestro** | costo de reparación: Costo de la reparación. |
| **Siniestro** | reintegro del seguro: Lo que reintegró la aseguradora. |
| **Siniestro** | franquicia: Franquicia a cargo de la distribuidora. |
| **Siniestro** | cerrado el: Cuándo se cerró. |
| **Neumatico** | número de serie: Número de serie, único en la distribuidora. |
| **Neumatico** | marca: Marca. |
| **Neumatico** | medida: Medida del neumático. |
| **Neumatico** | costo: Costo de compra. |
| **Neumatico** | estado: En depósito, montado o dado de baja. |
| **Neumatico** | posición: Código corto de la posición en el vehículo. |
| **Neumatico** | kilometraje de montaje: Kilometraje del vehículo al montarlo. |
| **MovimientoNeumatico** | tipo: Montaje, desmontaje, rotación, recapado o baja. |
| **MovimientoNeumatico** | kilometraje: Kilometraje del vehículo en el movimiento. |
| **MovimientoNeumatico** | fecha: Cuándo ocurrió. |
| **Reclamo** | motivo: Motivo del reclamo. |
| **Reclamo** | descripción: Detalle del reclamo. |
| **Reclamo** | estado: Pendiente, en proceso, resuelto o rechazado. |
| **Reclamo** | resolución: Nota del administrador al resolverlo. |
| **Reclamo** | fotografía: Imagen que el cliente adjunta como evidencia del reclamo (opcional). |
| **Incidencia** | tipo: Naturaleza del contratiempo. |
| **Incidencia** | momento: Si ocurrió antes, durante o después de la entrega. |
| **Incidencia** | descripción: Relato del contratiempo. |
| **Incidencia** | estado: Abierta o resuelta. |
| **Incidencia** | resolución: Nota del administrador al cerrarla. |
| **Incidencia** | fotografía: Imagen del contratiempo que adjunta quien lo reporta (opcional). |
| **Calificacion** | puntaje: Valoración numérica asignada a la otra parte. |
| **Calificacion** | comentario: Observación escrita de quien califica, si la dejó. |
| **Deposito** | nombre: Nombre del depósito. |
| **Deposito** | código: Código corto, único entre los depósitos vigentes de la distribuidora. |
| **Deposito** | tipo: Depósito o sucursal. |
| **Deposito** | dirección: Dónde queda. |
| **Deposito** | predeterminado: Si es el que se usa cuando un movimiento no indica otro. Hay uno solo por distribuidora. |
| **Deposito** | activo: Si está en uso. |
| **UbicacionDeStock** | tipo: Si es un depósito o un vehículo. |
| **SaldoDeStock** | condición: Llena, vacía o defectuosa. |
| **SaldoDeStock** | cantidad: Unidades de ese tipo de garrafa en esa condición; nunca negativa. |
| **MovimientoDeStock** | cantidad: Unidades movidas; siempre positiva. |
| **MovimientoDeStock** | condición de origen: Condición de las unidades en la ubicación de origen. |
| **MovimientoDeStock** | condición de destino: Condición de las unidades en la ubicación de destino. |
| **MovimientoDeStock** | motivo: Recepción, traslado, entrega, vacío recolectado, ajuste, merma, carga o regreso del camión, entre otros. |
| **MovimientoDeStock** | fecha: Cuándo ocurrió. |
| **UmbralDeStock** | mínimo de llenas: Cantidad de llenas por debajo de la cual se avisa. |
| **UmbralDeStock** | avisado el: Cuándo se emitió el aviso vigente; vacío si no hay ninguno. |
| **AjusteDeStock** | número: Número correlativo por distribuidora. |
| **AjusteDeStock** | motivo: Corrección de recuento, merma, fuga, daño, pérdida, hallazgo o recuento inicial. |
| **AjusteDeStock** | nota: Explicación obligatoria del ajuste. |
| **AjusteDeStock** | fecha: Cuándo se registró. |
| **ItemAjusteDeStock** | condición: Condición afectada. |
| **ItemAjusteDeStock** | diferencia: Unidades que se suman o se restan; nunca cero. |
| **CargaDeCamion** | número: Número correlativo por distribuidora. |
| **CargaDeCamion** | día: Día de negocio de la jornada. |
| **CargaDeCamion** | estado: Cargando, en ruta, regresó, cerrada, cerrada con diferencia o cancelada. |
| **CargaDeCamion** | abierta el: Cuándo se abrió la hoja. |
| **CargaDeCamion** | salió el: Cuándo salió el camión. |
| **CargaDeCamion** | regresó el: Cuándo regresó. |
| **CargaDeCamion** | cerrada el: Cuándo se cerró la rendición. |
| **CargaDeCamion** | nota de diferencia: Explicación de la diferencia; obligatoria si la hay. |
| **ItemCarga** | llenas cargadas: Llenas que salieron del depósito. |
| **ItemCarga** | llenas repuestas: Llenas que se repusieron en ruta. |
| **ItemCarga** | vacías cargadas: Vacías que salieron para el canje. |
| **ItemCarga** | llenas declaradas al regreso: Llenas que el chofer declara traer de vuelta. |
| **ItemCarga** | vacías declaradas al regreso: Vacías que el chofer declara traer de vuelta. |
| **ItemCarga** | llenas entregadas: Llenas entregadas a clientes durante la jornada. |
| **ItemCarga** | vacías recolectadas: Vacías recibidas de los clientes. |
| **ItemCarga** | /llenas esperadas: Llenas que deberían volver: cargadas y repuestas menos entregadas. |
| **ItemCarga** | /vacías esperadas: Vacías que deberían volver: cargadas más recolectadas. |
| **ItemCarga** | diferencia de llenas: Declaradas menos esperadas, al cerrar. |
| **ItemCarga** | diferencia de vacías: Declaradas menos esperadas, al cerrar. |
| **Proveedor** | razón social: Nombre legal. |
| **Proveedor** | CUIT: Identificación tributaria, única entre los proveedores vigentes. |
| **Proveedor** | tipo: Planta de llenado u otro. |
| **Proveedor** | contacto: Persona de contacto. |
| **Proveedor** | teléfono: Teléfono. |
| **Proveedor** | correo: Correo. |
| **Proveedor** | dirección: Dirección. |
| **Proveedor** | plazo de pago: Días de plazo que da el proveedor. |
| **Proveedor** | activo: Si está en uso. |
| **OrdenDeCompra** | número: Número correlativo por distribuidora. |
| **OrdenDeCompra** | estado: Borrador, enviada, parcialmente recibida, recibida o cancelada. |
| **OrdenDeCompra** | emitida el: Cuándo se envió. |
| **OrdenDeCompra** | fecha esperada: Cuándo se espera la mercadería. |
| **OrdenDeCompra** | total: Suma de cantidad por costo de los renglones. |
| **OrdenDeCompra** | motivo de cancelación: Por qué se canceló. |
| **OrdenDeCompra** | notas: Observaciones. |
| **ItemOrdenDeCompra** | cantidad: Unidades pedidas. |
| **ItemOrdenDeCompra** | costo unitario: Costo esperado por unidad. |
| **ItemOrdenDeCompra** | vacíos a canjear: Envases vacíos que se entregan a la planta. |
| **ItemOrdenDeCompra** | cantidad recibida: Unidades recibidas hasta ahora. |
| **RecepcionDeCompra** | número: Número interno correlativo. |
| **RecepcionDeCompra** | tipo de comprobante: Remito o factura del proveedor. |
| **RecepcionDeCompra** | número de comprobante: Número del comprobante; no se repite para un mismo proveedor. |
| **RecepcionDeCompra** | recibida el: Cuándo se recibió. |
| **RecepcionDeCompra** | total: Importe del remito. |
| **RecepcionDeCompra** | estado de pago: Impago o pagado. |
| **RecepcionDeCompra** | estado: Confirmada o anulada. |
| **RecepcionDeCompra** | motivo de anulación: Por qué se anuló. |
| **ItemRecepcion** | llenas recibidas: Llenas que llegaron. |
| **ItemRecepcion** | vacías entregadas: Vacías que se llevó la planta. |
| **ItemRecepcion** | costo unitario: Costo real por unidad. |
| **ConfiguracionModulo** | exigir carga de camión abierta: Si la distribuidora exige que un chofer tenga una carga de camión abierta para recibir pedidos; viene apagado (planificado, I-13). |
| **Producto** | costo promedio: Costo promedio ponderado de la garrafa, que se recalcula con cada recepción de compra (planificado, I-13). |
| **Caja** | nombre: Nombre de la caja. |
| **Caja** | tipo: Efectivo, banco o billetera. |
| **Caja** | saldo: Dinero que tiene la caja según su libro. |
| **Caja** | requiere sesión: Si sólo admite movimientos con una sesión abierta. |
| **Caja** | activa: Si se la puede usar. |
| **SesionDeCaja** | estado: Abierta o cerrada. |
| **SesionDeCaja** | abierta el: Momento de la apertura. |
| **SesionDeCaja** | monto inicial: Dinero con que se abrió. |
| **SesionDeCaja** | cerrada el: Momento del cierre. |
| **SesionDeCaja** | monto esperado: Saldo teórico de la caja según el libro al cerrar. |
| **SesionDeCaja** | monto contado: Dinero contado en el arqueo. |
| **SesionDeCaja** | diferencia: Contado menos esperado; negativa es faltante. |
| **SesionDeCaja** | observaciones: Nota del arqueo. |
| **CategoriaDeCaja** | nombre: Nombre de la categoría. |
| **CategoriaDeCaja** | sentido: Ingreso o egreso. |
| **CategoriaDeCaja** | código de sistema: Código con que los procesos automáticos la buscan; vacío en las propias. |
| **CategoriaDeCaja** | activa: Si se ofrece para movimientos nuevos. |
| **MovimientoDeCaja** | sentido: Ingreso o egreso. |
| **MovimientoDeCaja** | importe: Monto del movimiento, siempre mayor que cero. |
| **MovimientoDeCaja** | medio: Efectivo, transferencia, tarjeta, billetera o cheque. |
| **MovimientoDeCaja** | fecha: Momento en que ocurrió. |
| **MovimientoDeCaja** | descripción: Detalle libre. |
| **MovimientoDeCaja** | origen: Qué lo originó: carga manual, rendición, pago, liquidación, transferencia o anulación. |
| **RendicionChofer** | número: Correlativo por distribuidora. |
| **RendicionChofer** | fecha de negocio: Día argentino que se rinde. |
| **RendicionChofer** | estado: Abierta, presentada o aprobada. |
| **RendicionChofer** | efectivo esperado: Efectivo que el chofer debería entregar. |
| **RendicionChofer** | efectivo declarado: Efectivo que el chofer declara entregar. |
| **RendicionChofer** | /gastos del chofer: Gastos pagados con la cobranza. |
| **RendicionChofer** | /diferencia: Declarado más gastos menos esperado; negativa es faltante. |
| **RendicionChofer** | resolución de la diferencia: Sin diferencia, a cargo del chofer o absorbida. |
| **RendicionChofer** | presentada el: Momento en que se presentó. |
| **RendicionChofer** | aprobada el: Momento en que se aprobó. |
| **RendicionChofer** | observaciones: Nota libre. |
| **RendicionChofer** | aviso enviado el: Momento en que se avisó que seguía sin cerrar. |
| **PedidoRendido** | importe: Monto cobrado del pedido. |
| **PedidoRendido** | medio de pago: Medio de pago del pedido al rendirlo. |
| **GastoDeRendicion** | importe: Monto pagado. |
| **GastoDeRendicion** | descripción: Detalle del gasto. |
| **CuentaCorriente** | razón social: Nombre comercial con que se factura. |
| **CuentaCorriente** | CUIT: Clave de identificación tributaria. |
| **CuentaCorriente** | condición fiscal: Inscripto, monotributo, exento o consumidor final. |
| **CuentaCorriente** | límite de crédito: Deuda máxima permitida. |
| **CuentaCorriente** | plazo de pago en días: Días entre la entrega y el vencimiento. |
| **CuentaCorriente** | estado: Activa, bloqueada o cerrada. |
| **CuentaCorriente** | saldo: Lo que debe el cliente; negativo es a su favor. |
| **AsientoCuentaCorriente** | tipo: Cargo por venta, pago, nota de crédito, nota de débito o anulación. |
| **AsientoCuentaCorriente** | importe: Monto del asiento; el signo lo da el tipo. |
| **AsientoCuentaCorriente** | vence: Fecha de vencimiento de un cargo. |
| **AsientoCuentaCorriente** | medio de pago: Medio con que se pagó. |
| **AsientoCuentaCorriente** | fecha: Momento en que ocurrió. |
| **AsientoCuentaCorriente** | descripción: Detalle o motivo. |
| **ImputacionCuentaCorriente** | importe: Monto de un pago aplicado a un cargo. |
| **ReglaComision** | base: Por unidad, por pedido o porcentaje del total. |
| **ReglaComision** | valor: Monto o porcentaje, según la base. |
| **ReglaComision** | vigente desde: Inicio de la vigencia. |
| **ReglaComision** | vigente hasta: Fin de la vigencia; vacío si no tiene. |
| **ReglaComision** | activa: Si la regla se aplica. |
| **AsientoComision** | tipo: Comisión por entrega, faltante de rendición, multa, ajuste o saldo heredado. |
| **AsientoComision** | importe: Monto con signo; las deducciones son negativas. |
| **AsientoComision** | fecha: Momento en que ocurrió. |
| **AsientoComision** | descripción: Detalle o motivo. |
| **LiquidacionComisiones** | número: Correlativo por distribuidora. |
| **LiquidacionComisiones** | período desde: Inicio del período liquidado. |
| **LiquidacionComisiones** | período hasta: Fin del período liquidado. |
| **LiquidacionComisiones** | bruto: Suma de las comisiones. |
| **LiquidacionComisiones** | deducciones: Suma de los descuentos. |
| **LiquidacionComisiones** | neto: Bruto menos deducciones. |
| **LiquidacionComisiones** | estado: Borrador, aprobada, pagada, cerrada sin pago o anulada. |
| **LiquidacionComisiones** | aprobada el: Momento de la aprobación. |
| **LiquidacionComisiones** | pagada el: Momento del pago. |

**Atributos que guardan un valor compuesto.** `ConfiguracionModulo.parámetros` y
`AsientoAuditoria.cambios` no se desglosan en atributos simples: cada uno es un valor
atómico del dominio —«los parámetros vigentes del proceso», «lo que cambió esa
operación»— aunque el modelo de datos los guarde como JSON. Desglosarlos exigiría un
atributo por cada parámetro posible de cada uno de los cinco procesos automáticos, que
no es información que el negocio use por partes.

---

### 1.5 Diagrama Conceptual

El modelo conceptual es un **modelo del dominio** en la notación de Larman: los conceptos
llevan atributos pero **no operaciones**, ni tipos de implementación, ni claves foráneas;
esas cuestiones corresponden al modelo de datos del Documento 3 y al diagrama
entidad-relación. Cada asociación lleva un nombre en voz activa y una flecha («▸») que
indica el sentido de lectura, y la multiplicidad en sus dos extremos, en notación UML
(`1`, `0..1`, `0..*`, `1..*`, `0..2`). Un atributo con `/` adelante es derivado. Las
especializaciones llevan a la vista su restricción de conjunto de generalización:
`{overlapping, incomplete}` para Usuario y `{disjoint, complete}` para PropuestaConVigencia.
AsignacionVehiculo se dibuja como clase de asociación: la línea punteada la une con la
asociación «usa» entre Chofer y Vehiculo.

El modelo tiene 83 conceptos, demasiados para una sola lámina legible. Se presenta como una
**vista general**, sin atributos y sin nombres de asociación, y quince **vistas por área** con
atributos, nombres y multiplicidades. En cada vista por área, los conceptos en gris
pertenecen a otra vista y se muestran sólo como referencia. Toda entidad pertenece a una
distribuidora; para no cruzar los diagramas de líneas, las vistas por área dibujan sólo las
relaciones de la distribuidora que forman parte del negocio. El cliente no tiene atributo de
validación: se registra y compra sin aprobación previa.

La generalización de Usuario es `{overlapping}`: nada impide que la misma persona sea Cliente
y Chofer a la vez —cada perfil es una fila aparte, con su propia clave hacia Usuario—, y es
`{incomplete}` porque existen usuarios base que todavía no tienen perfil. La de
PropuestaConVigencia es `{disjoint, complete}`: toda propuesta es de exactamente uno de los
cinco tipos y el concepto abstracto no se instancia.

![Modelo conceptual: vista general](diagramas/modelo-conceptual/MC_General.png)

**Figura 1 — Diagrama Conceptual**

![Modelo conceptual: usuarios y cuentas](diagramas/modelo-conceptual/MC_Usuarios-y-cuentas.png)

**Figura 1.1 — Modelo conceptual: usuarios y cuentas**

![Modelo conceptual: pedidos y pagos](diagramas/modelo-conceptual/MC_Pedidos.png)

**Figura 1.2 — Modelo conceptual: pedidos y pagos**

![Modelo conceptual: despacho y propuestas con vigencia](diagramas/modelo-conceptual/MC_Despacho.png)

**Figura 1.3 — Modelo conceptual: despacho y propuestas con vigencia**

![Modelo conceptual: flota y choferes](diagramas/modelo-conceptual/MC_Flota.png)

**Figura 1.4 — Modelo conceptual: flota y choferes**

![Modelo conceptual: envases y catálogo](diagramas/modelo-conceptual/MC_Envases.png)

**Figura 1.5 — Modelo conceptual: envases y catálogo**

![Modelo conceptual: personal](diagramas/modelo-conceptual/MC_Personal.png)

**Figura 1.6 — Modelo conceptual: personal (puestos y legajos construidos; jornadas y licencias planificadas, I-11)**

![Modelo conceptual: posventa](diagramas/modelo-conceptual/MC_Posventa.png)

**Figura 1.7 — Modelo conceptual: posventa**

![Modelo conceptual: gastos de la flota](diagramas/modelo-conceptual/MC_Gastos-de-flota.png)

**Figura 1.8 — Modelo conceptual: gastos de la flota (planificado, I-12)**

![Modelo conceptual: stock físico](diagramas/modelo-conceptual/MC_Stock.png)

**Figura 1.9 — Modelo conceptual: stock físico (planificado, I-13)**

![Modelo conceptual: carga del camión](diagramas/modelo-conceptual/MC_Carga-del-camion.png)

**Figura 1.10 — Modelo conceptual: carga del camión (planificado, I-13)**

![Modelo conceptual: compras](diagramas/modelo-conceptual/MC_Compras.png)

**Figura 1.11 — Modelo conceptual: compras (planificado, I-13)**

![Modelo conceptual: caja y movimientos](diagramas/modelo-conceptual/MC_Caja.png)

**Figura 1.12 — Modelo conceptual: caja y movimientos (planificado, I-14)**

![Modelo conceptual: rendiciones de choferes](diagramas/modelo-conceptual/MC_Rendiciones.png)

**Figura 1.13 — Modelo conceptual: rendiciones de choferes (planificado, I-14)**

![Modelo conceptual: cuentas corrientes](diagramas/modelo-conceptual/MC_Cuentas-corrientes.png)

**Figura 1.14 — Modelo conceptual: cuentas corrientes (planificado, I-14)**

![Modelo conceptual: comisiones y liquidaciones](diagramas/modelo-conceptual/MC_Comisiones.png)

**Figura 1.15 — Modelo conceptual: comisiones y liquidaciones (planificado, I-14)**

---

## 2. Comportamiento del Sistema

### 2.1 Diagramas de Secuencia a Nivel de Sistema

Los diagramas de secuencia muestran la interacción entre el **actor** y el **sistema tratado como caja negra**. Solo se muestran los mensajes de entrada y salida, sin detallar la implementación interna.

El sistema se dibuja como la lifeline `:Sistema`, y cada actor lleva el código del catálogo (Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Sistema Automático (ACT-04), Administrador General (ACT-05), MercadoPago (ACT-06)). Los mensajes que van del actor al sistema son las operaciones del sistema, con una única firma por operación, que se cataloga en §2.2; el sistema responde con un retorno punteado. Lo que el sistema le envía a un actor sin que éste lo haya pedido, como una oferta o un aviso, se dibuja como un mensaje asíncrono con nombre (`notificarOferta(pedido)`). Lo que el sistema hace por dentro no es un mensaje: se anota con una `Note`.

---

#### Crítico DSS — CU-001: Iniciar Sesión

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `iniciarSesion(correo, contrasena)`

```mermaid
sequenceDiagram
    title DSS — CU-001 Iniciar Sesión
    autonumber
    actor USR as Cliente (ACT-01)
    participant SIS as :Sistema

    USR->>SIS: iniciarSesion(correo, contrasena)
    activate SIS
    alt Credenciales validas
        SIS-->>USR: sesion iniciada (credencial con token de acceso)
    else Credenciales incorrectas
        SIS-->>USR: error de solicitud (credenciales invalidas)
    end
    deactivate SIS
    Note over USR,SIS: También lo inician el Chofer (ACT-02) y el<br/>Administrador (ACT-03)
```

**Figura 2 — DSS CU-001: Iniciar Sesión**

---

#### Crítico DSS — CU-005: Crear Pedido

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `crearPedido(items, direccionId, franjaId, fechaAgendada, metodoDePago)`

```mermaid
sequenceDiagram
    title DSS — CU-005 Crear Pedido
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: crearPedido(items, direccionId, franjaId, fechaAgendada, metodoDePago)
    activate SIS
    alt Hay stock y la dirección está cubierta
        SIS-->>CLI: pedido creado (número, total, estado pendiente y, si el pago es por MercadoPago, enlace de pago)
        Note over CLI,SIS: El total incluye promociones por volumen,<br/>recargo por medio de pago y recargo de zona
        SIS-)CLI: notificarConfirmacionDePedido(pedido)
    else Sin stock suficiente
        SIS-->>CLI: rechazo (stock insuficiente para el producto)
    else Un producto del pedido no existe
        SIS-->>CLI: rechazo (producto no encontrado)
    else Dirección fuera de la zona de cobertura
        SIS-->>CLI: rechazo (domicilio no cubierto)
    else Franja horaria sin cupo
        SIS-->>CLI: rechazo (franja completa para esa fecha)
    end
    deactivate SIS
```

**Figura 3 — DSS CU-005: Crear Pedido**

---

#### Crítico · automático DSS — CU-013: Asignar Pedido Automáticamente por Proximidad

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `ofrecerAlSiguienteChofer(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-013 Asignar Pedido Automáticamente por Proximidad
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor CHO as Chofer (ACT-02)

    Note over SAU: Se dispara al crearse el<br/>pedido
    SAU->>SIS: ofrecerAlSiguienteChofer(pedidoId)
    activate SIS
    Note over SIS: Recorre los radios 5,<br/>10, 15 y 20 km y<br/>descarta los choferes ya<br/>contactados y los de<br/>otra distribuidora
    alt Hay un candidato disponible
        SIS-)CHO: notificarOferta(pedido)
        SIS-->>SAU: oferta registrada (vence en 30 s)
    else No quedan candidatos nuevos
        SIS-->>SAU: sin candidatos, el pedido queda a la espera
    end
    deactivate SIS
```

**Figura 4 — DSS CU-013: Asignar Pedido Automáticamente por Proximidad**

---

#### Crítico · automático DSS — CU-014: Reintentar Asignación con Radio Expandido (Cron)

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `vencerOfertasExpiradas()`

```mermaid
sequenceDiagram
    title DSS — CU-014 Reintentar Asignación con Radio Expandido (Cron)
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor CHO as Chofer (ACT-02)

    Note over SAU: Se ejecuta cada 15<br/>segundos
    SAU->>SIS: vencerOfertasExpiradas()
    activate SIS
    loop Por cada oferta cuya vigencia expiró
        Note over SIS: Marca la oferta como<br/>vencida
        opt El pedido sigue pendiente y sin chofer
            SIS-)CHO: notificarOferta(pedido)
            Note over SIS: Reutiliza la búsqueda de<br/>CU-013 con el siguiente<br/>chofer
        end
        Note over SIS: Si el pedido ya fue aceptado<br/>o cancelado, no se vuelve<br/>a ofrecer
    end
    SIS-->>SAU: ofertas procesadas
    deactivate SIS
```

**Figura 5 — DSS CU-014: Reintentar Asignación con Radio Expandido (Cron)**

---

#### DSS — CU-171: Configurar los Parámetros de Despacho de la Distribuidora

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `configurarParametrosDeDespacho(radiosKm, ventanaDeAceptacion)`

```mermaid
sequenceDiagram
    title DSS — CU-171 Configurar los Parámetros de Despacho de la Distribuidora
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: configurarParametrosDeDespacho(radiosKm, ventanaDeAceptacion)
    activate SIS
    alt los valores son válidos
        SIS-->>ADM: configuración de despacho guardada
    else los valores están fuera de rango
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS
```

**Figura 6 — DSS CU-171: Configurar los Parámetros de Despacho de la Distribuidora**

---

#### Crítico DSS — CU-015: Aceptar Pedido

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `aceptarPedido(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-015 Aceptar Pedido
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    CHO->>SIS: aceptarPedido(pedidoId)
    activate SIS
    alt La transición de estado es válida y el chofer está activo
        SIS-->>CHO: pedido asignado (datos de entrega y código de entrega)
        SIS-)CLI: notificarPedidoAceptado(pedido)
    else El pedido es de otra distribuidora
        SIS-->>CHO: recurso no encontrado
    else El pedido ya tiene asignado a otro chofer
        SIS-->>CHO: acceso denegado (el pedido no está asignado a este chofer)
    else El pedido ya está entregado o cancelado
        SIS-->>CHO: error de solicitud (transición no permitida)
    else El chofer no existe o está dado de baja
        SIS-->>CHO: error de solicitud (repartidor no encontrado o inactivo)
    end
    deactivate SIS
```

**Figura 7 — DSS CU-015: Aceptar Pedido**

---

#### Crítico · automático DSS — CU-017: Actualizar Ubicación GPS del Chofer

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `actualizarUbicacion(usuarioId, latitud, longitud)`

```mermaid
sequenceDiagram
    title DSS — CU-017 Actualizar Ubicación GPS del Chofer
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)
    actor ADM as Administrador (ACT-03)

    loop Mientras el chofer está conectado
        CHO->>SIS: actualizarUbicacion(usuarioId, latitud, longitud)
        activate SIS
        opt Los datos de posición son válidos
            opt El chofer tiene un pedido en curso
                SIS-)CLI: notificarUbicacionDelChofer(pedido, latitud, longitud)
                SIS-)ADM: notificarUbicacionDelChofer(pedido, latitud, longitud)
            end
        end
        Note over SIS: Si faltan el usuario o las<br/>coordenadas, se descarta el<br/>envío y no se registra la<br/>posición
        deactivate SIS
    end
```

**Figura 8 — DSS CU-017: Actualizar Ubicación GPS del Chofer**

---

#### Crítico DSS — CU-020: Confirmar Entrega

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `confirmarEntrega(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-020 Confirmar Entrega
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    CHO->>SIS: confirmarEntrega(pedidoId)
    activate SIS
    alt El pedido está en camino y está asignado al chofer
        SIS-->>CHO: entrega registrada (estado ENTREGADO)
        Note over SIS: Si el pago es en<br/>efectivo, queda saldado
        SIS-)CLI: notificarPedidoEntregado(pedido)
    else El pedido es de otra distribuidora
        SIS-->>CHO: recurso no encontrado
    else El pedido está asignado a otro chofer
        SIS-->>CHO: acceso denegado
    else El pedido no está en camino
        SIS-->>CHO: error de solicitud (transición no permitida)
    end
    deactivate SIS
    Note over CHO,CLI: La confirmación con código de entrega se<br/>modela en CU-078 y CU-079
```

**Figura 9 — DSS CU-020: Confirmar Entrega**

---

#### Importante DSS — CU-023: Registrar Reclamo

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `registrarReclamo(pedidoId, motivo, evidencia)`

```mermaid
sequenceDiagram
    title DSS — CU-023 Registrar Reclamo
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: registrarReclamo(pedidoId, motivo, evidencia)
    activate SIS
    alt El pedido existe y es del cliente
        SIS-->>CLI: reclamo registrado (número, estado pendiente)
    else El pedido no existe
        SIS-->>CLI: recurso no encontrado
    else El pedido no le pertenece
        SIS-->>CLI: rechazo (esta orden no pertenece al cliente indicado)
    end
    deactivate SIS
```

**Figura 10 — DSS CU-023: Registrar Reclamo**

---


---

#### Ampliación — DSS de los casos de uso incorporados

Los 95 diagramas que siguen completan la cobertura del comportamiento del sistema.
Se agrupan por subsistema y respetan la misma convención de caja negra: solo intervienen
el actor y el sistema, sin detalle interno.

#### DSS — CU-002: Registrarse como Cliente

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `registrarse(nombreCompleto, correo, telefono, contrasena, datosDelCliente)`

```mermaid
sequenceDiagram
    title DSS — CU-002 Registrarse como Cliente
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: registrarse(nombreCompleto, correo, telefono, contrasena, datosDelCliente)
    activate SIS
    alt datos válidos y correo y teléfono libres
        SIS-->>CLI: cuenta creada (usuarioId, perfil de cliente, rol CLIENTE)
    else correo o teléfono ya registrados
        SIS-->>CLI: conflicto (el correo o el teléfono ya están en uso)
    else datos incompletos o con formato inválido
        SIS-->>CLI: error de validación indicando el campo
    else demasiadas altas seguidas desde el mismo origen
        SIS-->>CLI: demasiadas solicitudes (reintentar en un minuto)
    end
    deactivate SIS
```

**Figura 11 — DSS CU-002: Registrarse como Cliente**

---

#### DSS — CU-003: Registrar Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarChofer(datosPersonales, datosDelChofer, distribuidoraId)`

```mermaid
sequenceDiagram
    title DSS — CU-003 Registrar Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarChofer(datosPersonales, datosDelChofer, distribuidoraId)
    activate SIS
    alt puede dar de alta en esa distribuidora y los datos son válidos
        SIS-->>ADM: chofer registrado (usuarioId, perfil de chofer, rol CHOFER)
    else la distribuidora no es la suya, o no tiene distribuidora asociada
        SIS-->>ADM: acceso denegado
    else correo o teléfono ya registrados
        SIS-->>ADM: conflicto (el correo o el teléfono ya están en uso)
    else datos inválidos o falta la distribuidora
        SIS-->>ADM: error de validación
    end
    deactivate SIS
```

**Figura 12 — DSS CU-003: Registrar Chofer**

> El chofer nace **no validado**: para poder operar necesita CU-032.

---

#### DSS — CU-004: Consultar el Perfil de Usuario

**Actor:** Cliente (ACT-01), Chofer (ACT-02)
**Operaciones del sistema:** `consultarPerfil(usuarioId)`, `consultarPerfilCliente(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-004 Consultar el Perfil de Usuario
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarPerfil(usuarioId)
    activate SIS
    SIS-->>CLI: datos de la cuenta (nombre, correo, teléfono, rol)
    deactivate SIS

    opt el perfil tiene datos de cliente
        CLI->>SIS: consultarPerfilCliente(usuarioId)
        activate SIS
        SIS-->>CLI: datos del cliente (documento, ubicación, validación)
        deactivate SIS
    end
    Note over CLI,SIS: También lo inicia el Chofer (ACT-02)
```

**Figura 13 — DSS CU-004: Consultar el Perfil de Usuario**

---


#### DSS — CU-251: Modificar el Perfil de Usuario

**Actor:** Cliente (ACT-01), Chofer (ACT-02)
**Operaciones del sistema:** `actualizarPerfil(usuarioId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-251 Modificar el Perfil de Usuario
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: actualizarPerfil(usuarioId, datos)
    activate SIS
    alt es su propio perfil o es administrador
        SIS-->>CLI: perfil actualizado
    else intenta modificar el perfil de otro usuario
        SIS-->>CLI: acceso denegado
    end
    deactivate SIS
    Note over CLI,SIS: También lo inicia el Chofer (ACT-02)
```

**Figura 14 — DSS CU-251: Modificar el Perfil de Usuario**

---

#### DSS — CU-047: Recuperar Contraseña

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `solicitarRecuperacionDeClave(correo)`, `cambiarCorreo(correoActual, correoNuevo)`

```mermaid
sequenceDiagram
    title DSS — CU-047 Recuperar Contraseña
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: solicitarRecuperacionDeClave(correo)
    activate SIS
    alt el correo corresponde a una cuenta
        SIS-->>CLI: solicitud aceptada (se envió el enlace de restablecimiento)
    else el correo no existe
        SIS-->>CLI: solicitud aceptada (respuesta indistinguible por seguridad)
    end
    deactivate SIS

    opt el usuario autenticado quiere cambiar su correo
        CLI->>SIS: cambiarCorreo(correoActual, correoNuevo)
        activate SIS
        SIS-->>CLI: correo actualizado (se envió la verificación al nuevo)
        deactivate SIS
    end
    Note over CLI,SIS: También lo inician el Chofer (ACT-02) y el<br/>Administrador (ACT-03)
```

**Figura 15 — DSS CU-047: Recuperar Contraseña**

---

#### DSS — CU-050: Bloquear un Usuario

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `bloquearUsuario(usuarioId, bloquear)`

```mermaid
sequenceDiagram
    title DSS — CU-050 Bloquear un Usuario
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: bloquearUsuario(usuarioId, bloquear)
    activate SIS
    alt el usuario existe
        SIS-->>ADM: usuario bloqueado
    else el usuario no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
    Note over ADM,SIS: bloquear = verdadero. La misma operación, con bloquear = falso, es CU-270
```

**Figura 16 — DSS CU-050: Bloquear un Usuario**

---


#### DSS — CU-270: Desbloquear un Usuario

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `bloquearUsuario(usuarioId, bloquear)`

```mermaid
sequenceDiagram
    title DSS — CU-270 Desbloquear un Usuario
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: bloquearUsuario(usuarioId, bloquear)
    activate SIS
    alt el usuario existe
        SIS-->>ADM: usuario desbloqueado
    else el usuario no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
    Note over ADM,SIS: bloquear = falso. La misma operación, con bloquear = verdadero, es CU-050
```

**Figura 17 — DSS CU-270: Desbloquear un Usuario**

---

#### DSS — CU-082: Crear Usuario Base

**Actor:** ninguno directo (caso incluido)

Caso incluido: no tiene diagrama de secuencia propio. Lo inician CU-002, CU-003, CU-031, CU-086 y CU-087, y su operación forma parte del diagrama de secuencia de cada uno de ellos (caso base).

---

#### DSS — CU-083: Listar los Usuarios

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `listarUsuarios(pagina, limite, textoDeBusqueda)`

```mermaid
sequenceDiagram
    title DSS — CU-083 Listar los Usuarios
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarUsuarios(pagina, limite, textoDeBusqueda)
    activate SIS
    SIS-->>ADM: página de usuarios (total, cantidad, listado)
    deactivate SIS
```

**Figura 18 — DSS CU-083: Listar los Usuarios**

---


#### DSS — CU-272: Buscar un Usuario

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `buscarUsuarioPorCorreo(correo)`, `buscarUsuarioPorTelefono(telefono)`

```mermaid
sequenceDiagram
    title DSS — CU-272 Buscar un Usuario
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    alt búsqueda por correo
        ADM->>SIS: buscarUsuarioPorCorreo(correo)
        activate SIS
        alt existe
            SIS-->>ADM: usuario encontrado
        else no existe
            SIS-->>ADM: recurso no encontrado
        end
        deactivate SIS
    else búsqueda por teléfono
        ADM->>SIS: buscarUsuarioPorTelefono(telefono)
        activate SIS
        SIS-->>ADM: usuario encontrado
        deactivate SIS
    end
```

**Figura 19 — DSS CU-272: Buscar un Usuario**

---

#### DSS — CU-084: Verificar Existencia de Usuario (pre-registro)

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Sistema Automático (ACT-04)
**Operaciones del sistema:** `verificarExistenciaDeUsuario(correo, telefono)`

```mermaid
sequenceDiagram
    title DSS — CU-084 Verificar Existencia de Usuario (pre-registro)
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: verificarExistenciaDeUsuario(correo, telefono)
    activate SIS
    SIS-->>CLI: resultado (existeCorreo, existeTelefono)
    deactivate SIS
```

**Figura 20 — DSS CU-084: Verificar Existencia de Usuario (pre-registro)**

> Se invoca **antes** de CU-002 para que la aplicación avise el conflicto sin llegar a intentar el alta.

---

#### DSS — CU-085: Eliminar Usuario (baja lógica)

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `eliminarUsuario(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-085 Eliminar Usuario (baja lógica)
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: eliminarUsuario(usuarioId)
    activate SIS
    alt el usuario existe y el administrador puede darlo de baja
        SIS-->>ADM: usuario dado de baja (baja lógica de la cuenta, su perfil y sus direcciones, vehículo en uso liberado y chofer fuera del radar si era chofer, y la cuenta de acceso queda deshabilitada)
    else un administrador de empresa sobre la cuenta de un cliente
        SIS-->>ADM: acceso denegado, la cuenta de un cliente la administra el administrador general
    else el usuario es un chofer con pedidos aceptados o en camino
        SIS-->>ADM: conflicto, el chofer tiene pedidos en curso
    else el usuario no existe o es de otra distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 21 — DSS CU-085: Eliminar Usuario (baja lógica)**

---

#### DSS — CU-091: Validar Vigencia del Token de Sesión

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `validarSesion()`

```mermaid
sequenceDiagram
    title DSS — CU-091 Validar Vigencia del Token de Sesión
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: validarSesion()
    activate SIS
    alt La sesion esta vigente
        SIS-->>CLI: sesion valida
    else La sesion vencio o el token es invalido
        SIS-->>CLI: no autorizado
    end
    deactivate SIS
    Note over CLI,SIS: También lo inician el Chofer (ACT-02), el<br/>Administrador (ACT-03) y el Administrador<br/>General (ACT-05)
```

**Figura 22 — DSS CU-091: Validar Vigencia del Token de Sesión**

---

### SS-02 — Gestión de Pedidos

#### DSS — CU-006: Consultar Detalle de Pedido

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `consultarPedido(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-006 Consultar Detalle de Pedido
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarPedido(pedidoId)
    activate SIS
    alt el pedido existe y le pertenece al solicitante
        SIS-->>CLI: detalle del pedido (ítems, total, estado, dirección, chofer)
    else el pedido es de otro cliente
        SIS-->>CLI: acceso denegado
    else el pedido no existe
        SIS-->>CLI: recurso no encontrado
    end
    deactivate SIS
```

**Figura 23 — DSS CU-006: Consultar Detalle de Pedido**

---

#### DSS — CU-007: Consultar Historial de Pedidos

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `consultarHistorialDePedidos(clienteId, pagina, limite)`

```mermaid
sequenceDiagram
    title DSS — CU-007 Consultar Historial de Pedidos
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarHistorialDePedidos(clienteId, pagina, limite)
    activate SIS
    alt consulta su propio historial
        SIS-->>CLI: página de pedidos (total, cantidad, listado)
    else consulta el historial de otro cliente
        SIS-->>CLI: acceso denegado
    end
    deactivate SIS
```

**Figura 24 — DSS CU-007: Consultar Historial de Pedidos**

> El cliente ve **todo** su historial aunque haya comprado a varias distribuidoras; el personal solo ve los pedidos de la suya.

---

#### DSS — CU-169: Registrar el Cambio de Estado de un Pedido

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `registrarCambioDeEstado(pedidoId, estadoAnterior, estadoNuevo, autor, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-169 Registrar el Cambio de Estado de un Pedido
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    Note over SAU: Se dispara en cada<br/>cambio de estado del<br/>pedido, dentro de la<br/>misma transacción
    SAU->>SIS: registrarCambioDeEstado(pedidoId, estadoAnterior, estadoNuevo, autor, motivo)
    activate SIS
    alt El cambio es válido y se guarda
        SIS-->>SAU: fila agregada al historial, junto con el cambio
    else No se puede escribir el historial
        SIS-->>SAU: cambio revertido
    end
    deactivate SIS
```

**Figura 25 — DSS CU-169: Registrar el Cambio de Estado de un Pedido**

---

#### DSS — CU-170: Consultar el Historial de Estados de un Pedido

**Actor:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarHistorialDeEstados(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-170 Consultar el Historial de Estados de un Pedido
    autonumber
    actor USR as Cliente (ACT-01)
    participant SIS as :Sistema

    USR->>SIS: consultarHistorialDeEstados(pedidoId)
    activate SIS
    alt el pedido existe y el usuario puede verlo
        SIS-->>USR: cambios de estado, del más antiguo al más reciente
    else el pedido no existe o no es del usuario
        SIS-->>USR: recurso no encontrado
    end
    deactivate SIS
    Note over USR,SIS: También lo inician el Administrador (ACT-03) y<br/>el Administrador General (ACT-05)
```

**Figura 26 — DSS CU-170: Consultar el Historial de Estados de un Pedido**

---

#### DSS — CU-143: Declarar el Consumo Promedio al Registrarse

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `declararConsumoPromedio(tipoGarrafa, cantidadPorMes)`

```mermaid
sequenceDiagram
    title DSS — CU-143 Declarar el Consumo Promedio al Registrarse
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: declararConsumoPromedio(tipoGarrafa, cantidadPorMes)
    activate SIS
    alt el valor es razonable
        SIS-->>CLI: consumo declarado y recompra estimada
    else el cliente no lo declara
        SIS-->>CLI: registro sin consumo declarado
    else el valor está fuera de rango
        SIS-->>CLI: se pide confirmación
    end
    deactivate SIS
```

**Figura 27 — DSS CU-143: Declarar el Consumo Promedio al Registrarse**

---

#### DSS — CU-144: Actualizar el Consumo Promedio Declarado

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `actualizarConsumoPromedio(cantidadPorMes)`

```mermaid
sequenceDiagram
    title DSS — CU-144 Actualizar el Consumo Promedio Declarado
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: actualizarConsumoPromedio(cantidadPorMes)
    activate SIS
    alt el valor es razonable
        SIS-->>CLI: consumo actualizado y recompra recalculada
    else el valor está fuera de rango
        SIS-->>CLI: se pide confirmación
    end
    deactivate SIS
```

**Figura 28 — DSS CU-144: Actualizar el Consumo Promedio Declarado**

---

#### DSS — CU-145: Configurar los Días de Aviso Previo a la Recompra

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `configurarDiasDeAviso(dias)`

```mermaid
sequenceDiagram
    title DSS — CU-145 Configurar los Días de Aviso Previo a la Recompra
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: configurarDiasDeAviso(dias)
    activate SIS
    alt el valor está dentro del rango
        SIS-->>CLI: preferencia guardada
    else el valor está fuera del rango
        SIS-->>CLI: operación rechazada
    end
    deactivate SIS
```

**Figura 29 — DSS CU-145: Configurar los Días de Aviso Previo a la Recompra**

---

#### DSS — CU-146: Consultar la Fecha Estimada de Recompra

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarRecomprasEstimadas(dias)`

```mermaid
sequenceDiagram
    title DSS — CU-146 Consultar la Fecha Estimada de Recompra
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarRecomprasEstimadas(dias)
    activate SIS
    alt hay clientes en la ventana
        SIS-->>ADM: listado ordenado por fecha estimada
    else no hay ninguno
        SIS-->>ADM: listado vacío
    end
    deactivate SIS
```

**Figura 30 — DSS CU-146: Consultar la Fecha Estimada de Recompra**

---

#### DSS — CU-147: Realizar una Compra Express

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `realizarCompraExpress(tipoGarrafa, medioDePago)`

```mermaid
sequenceDiagram
    title DSS — CU-147 Realizar una Compra Express
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: realizarCompraExpress(tipoGarrafa, medioDePago)
    activate SIS
    alt hay cobertura, horario y chofer
        SIS-->>CLI: pedido express creado y despachado (con MercadoPago, el enlace de pago)
    else no hay cobertura express o está fuera de horario
        SIS-->>CLI: se ofrece el flujo con franja horaria
    else no hay chofer en moto disponible
        SIS-->>CLI: se ofrece el flujo con franja horaria
    end
    deactivate SIS
```

**Figura 31 — DSS CU-147: Realizar una Compra Express**

---

#### DSS — CU-148: Elegir la Modalidad de Entrega del Pedido

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `consultarModalidadesDeEntrega(direccionId)`

```mermaid
sequenceDiagram
    title DSS — CU-148 Elegir la Modalidad de Entrega del Pedido
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarModalidadesDeEntrega(direccionId)
    activate SIS
    alt las dos modalidades están disponibles
        SIS-->>CLI: opciones con precio y tiempo estimado
    else sólo la programada está disponible
        SIS-->>CLI: opción programada con el motivo
    end
    deactivate SIS
```

**Figura 32 — DSS CU-148: Elegir la Modalidad de Entrega del Pedido**

---

#### DSS — CU-008: Cancelar Pedido (Cliente)

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `cancelarPedido(pedidoId, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-008 Cancelar Pedido (Cliente)
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema
    actor CHO as Chofer (ACT-02)
    actor ADM as Administrador (ACT-03)

    CLI->>SIS: cancelarPedido(pedidoId, motivo)
    activate SIS
    alt El pedido es del cliente y todavía no salió en camino
        SIS-->>CLI: pedido cancelado (estado CANCELADO, stock restituido)
        opt El pedido ya tenía chofer asignado
            SIS-)CHO: notificarPedidoCancelado(pedido)
        end
        SIS-)ADM: notificarPedidoCancelado(pedido)
        Note over SIS: Si el pedido tenía un<br/>pago aprobado por una<br/>pasarela (planificado,<br/>I-7), se reintegra con<br/>CU-168
    else El pedido es de otro cliente o de otra distribuidora
        SIS-->>CLI: recurso no encontrado
    else El pedido ya está entregado o cancelado
        SIS-->>CLI: error de solicitud (no se puede cancelar un pedido finalizado)
    else El pedido ya está en camino
        SIS-->>CLI: error de solicitud (contactar al soporte)
    end
    deactivate SIS
```

**Figura 33 — DSS CU-008: Cancelar Pedido (Cliente)**

> La identidad y el rol del cancelador salen **siempre** de la sesión, nunca del cuerpo del mensaje.

---

#### DSS — CU-009: Cancelar Pedido (Chofer)

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `liberarPedido(pedidoId, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-009 Cancelar Pedido (Chofer)
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    CHO->>SIS: liberarPedido(pedidoId, motivo)
    activate SIS
    alt El pedido está asignado al chofer y no está finalizado
        SIS-->>CHO: pedido liberado (vuelve a PENDIENTE y queda sin chofer)
        SIS-)CLI: notificarBusquedaDeNuevoChofer(pedido)
    else El pedido es de otra distribuidora
        SIS-->>CHO: recurso no encontrado
    else El pedido no está asignado a este chofer
        SIS-->>CHO: acceso denegado
    else El pedido ya está entregado o cancelado
        SIS-->>CHO: error de solicitud (no se puede cancelar un pedido finalizado)
    end
    deactivate SIS
```

**Figura 34 — DSS CU-009: Cancelar Pedido (Chofer)**

---

#### DSS — CU-010: Cancelar Pedido (Administrador)

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `cancelarPedido(pedidoId, motivo)`, `cancelarPedidoForzado(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-010 Cancelar Pedido (Administrador)
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    alt Cancelación ordinaria
        ADM->>SIS: cancelarPedido(pedidoId, motivo)
        activate SIS
        SIS-->>ADM: pedido cancelado (motivo registrado, stock restituido)
        deactivate SIS
    else Cancelación forzada
        ADM->>SIS: cancelarPedidoForzado(pedidoId)
        activate SIS
        SIS-->>ADM: pedido cancelado por decisión administrativa
        deactivate SIS
    end
    Note over ADM,SIS: Si el pedido tenía un pago aprobado por una<br/>pasarela (planificado, I-7), se reintegra con<br/>CU-168
```

**Figura 35 — DSS CU-010: Cancelar Pedido (Administrador)**

> El sistema ofrece **dos** vías para el administrador. La documentación previa describía una sola.

---

#### DSS — CU-011: Listar Todos los Pedidos

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `listarPedidos(pagina, limite)`

```mermaid
sequenceDiagram
    title DSS — CU-011 Listar Todos los Pedidos
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarPedidos(pagina, limite)
    activate SIS
    alt es administrador de una distribuidora
        SIS-->>ADM: página de pedidos de su distribuidora
    else es super administrador sin distribuidora seleccionada
        SIS-->>ADM: página de pedidos de todas las distribuidoras
    end
    deactivate SIS
```

**Figura 36 — DSS CU-011: Listar Todos los Pedidos**

---

#### DSS — CU-012: Asignar Chofer Manualmente

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `asignarChoferAPedido(pedidoId, choferId)`

```mermaid
sequenceDiagram
    title DSS — CU-012 Asignar Chofer Manualmente
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: asignarChoferAPedido(pedidoId, choferId)
    activate SIS
    alt el pedido está pendiente o aceptado por otro chofer, y el chofer es elegible
        SIS-->>ADM: pedido asignado (estado ACEPTADO, chofer vinculado, código de entrega nuevo)
    else el pedido o el chofer no existen o son de otra distribuidora
        SIS-->>ADM: recurso no encontrado
    else el chofer está deshabilitado, no está validado o tiene la flota inhabilitada
        SIS-->>ADM: asignación rechazada
    else el pedido no admite pasar a aceptado
        SIS-->>ADM: asignación rechazada por transición no permitida
    end
    deactivate SIS
```

**Figura 37 — DSS CU-012: Asignar Chofer Manualmente**

---

#### DSS — CU-149: Despachar un Pedido Express a un Chofer en Moto

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `despacharPedidoExpress(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-149 Despachar un Pedido Express a un Chofer en Moto
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    SAU->>SIS: despacharPedidoExpress(pedidoId)
    activate SIS
    Note over SIS: Ofrece el pedido al<br/>chofer en moto más<br/>cercano, con una ventana<br/>de aceptación más corta
    alt Un chofer en moto acepta
        SIS-->>SAU: pedido asignado
        SIS-)CLI: notificarPedidoAceptado(pedido)
    else Ninguno acepta
        SIS-->>SAU: modalidad express cancelada, recargo descontado del total y reintegrado si se pagó en línea
    end
    deactivate SIS
```

**Figura 38 — DSS CU-149: Despachar un Pedido Express a un Chofer en Moto**

---

#### DSS — CU-046: Consultar Direcciones de Entrega del Cliente

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `registrarDireccionDeEntrega(datos)`, `consultarDireccionesDeEntrega(usuarioId)`, `marcarDireccionPredeterminada(direccionId)`, `editarDireccionDeEntrega(direccionId, cambios)`, `eliminarDireccionDeEntrega(direccionId)`

```mermaid
sequenceDiagram
    title DSS — CU-046 Consultar Direcciones de Entrega del Cliente
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: registrarDireccionDeEntrega(datos)
    activate SIS
    SIS-->>CLI: dirección creada (direccionId)
    deactivate SIS

    CLI->>SIS: consultarDireccionesDeEntrega(usuarioId)
    activate SIS
    SIS-->>CLI: listado de direcciones
    deactivate SIS

    opt el cliente cambia su dirección habitual
        CLI->>SIS: marcarDireccionPredeterminada(direccionId)
        activate SIS
        SIS-->>CLI: dirección predeterminada actualizada (las demás dejan de serlo)
        deactivate SIS
    end

    opt corrección de datos
        CLI->>SIS: editarDireccionDeEntrega(direccionId, cambios)
        activate SIS
        SIS-->>CLI: dirección actualizada
        deactivate SIS
    end

    opt baja de una dirección
        CLI->>SIS: eliminarDireccionDeEntrega(direccionId)
        activate SIS
        alt la dirección existe y es del cliente
            SIS-->>CLI: dirección eliminada
        else la dirección no existe
            SIS-->>CLI: recurso no encontrado
        end
        deactivate SIS
    end
```

**Figura 39 — DSS CU-046: Consultar Direcciones de Entrega del Cliente**

---

#### DSS — CU-116: Registrar Dirección de Entrega

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `registrarDireccionDeEntrega(datos)`

```mermaid
sequenceDiagram
    title DSS — CU-116 Registrar Dirección de Entrega
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: registrarDireccionDeEntrega(datos)
    activate SIS
    alt los datos son válidos
        SIS-->>CLI: dirección registrada
    else la cuenta de usuario no existe
        SIS-->>CLI: recurso no encontrado
    end
    deactivate SIS
```

**Figura 40 — DSS CU-116: Registrar Dirección de Entrega**

---

#### DSS — CU-117: Consultar Detalle de una Dirección de Entrega

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `consultarDireccionDeEntrega(direccionId)`

```mermaid
sequenceDiagram
    title DSS — CU-117 Consultar Detalle de una Dirección de Entrega
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarDireccionDeEntrega(direccionId)
    activate SIS
    alt la dirección existe y es del cliente
        SIS-->>CLI: datos de la dirección
    else la dirección no existe
        SIS-->>CLI: recurso no encontrado
    else la dirección es de otro cliente
        SIS-->>CLI: acceso denegado
    end
    deactivate SIS
```

**Figura 41 — DSS CU-117: Consultar Detalle de una Dirección de Entrega**

---

#### DSS — CU-118: Editar Dirección de Entrega

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `editarDireccionDeEntrega(direccionId, cambios)`

```mermaid
sequenceDiagram
    title DSS — CU-118 Editar Dirección de Entrega
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: editarDireccionDeEntrega(direccionId, cambios)
    activate SIS
    alt la dirección existe y es del cliente
        SIS-->>CLI: dirección actualizada
    else la dirección no existe o es de otro
        SIS-->>CLI: operación rechazada
    end
    deactivate SIS
```

**Figura 42 — DSS CU-118: Editar Dirección de Entrega**

---

#### DSS — CU-119: Eliminar Dirección de Entrega

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `eliminarDireccionDeEntrega(direccionId)`

```mermaid
sequenceDiagram
    title DSS — CU-119 Eliminar Dirección de Entrega
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: eliminarDireccionDeEntrega(direccionId)
    activate SIS
    alt la dirección existe y es del cliente
        SIS-->>CLI: baja confirmada (baja lógica, los pedidos que la usaron la siguen mostrando)
    else la dirección no existe o es de otro
        SIS-->>CLI: operación rechazada
    end
    deactivate SIS
```

**Figura 43 — DSS CU-119: Eliminar Dirección de Entrega**

---

#### DSS — CU-120: Marcar una Dirección como Predeterminada

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `marcarDireccionPredeterminada(direccionId)`

```mermaid
sequenceDiagram
    title DSS — CU-120 Marcar una Dirección como Predeterminada
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: marcarDireccionPredeterminada(direccionId)
    activate SIS
    alt la dirección existe y es del cliente
        SIS-->>CLI: dirección marcada como predeterminada
    else la dirección no existe o es de otro
        SIS-->>CLI: operación rechazada
    end
    deactivate SIS
```

**Figura 44 — DSS CU-120: Marcar una Dirección como Predeterminada**

---

#### DSS — CU-121: Consultar la Dirección Predeterminada

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `consultarDireccionPredeterminada(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-121 Consultar la Dirección Predeterminada
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarDireccionPredeterminada(usuarioId)
    activate SIS
    alt el cliente tiene una dirección predeterminada
        SIS-->>CLI: datos de la dirección
    else el cliente no tiene ninguna
        SIS-->>CLI: recurso no encontrado
    end
    deactivate SIS
```

**Figura 45 — DSS CU-121: Consultar la Dirección Predeterminada**

---

#### DSS — CU-122: Agregar Ítem al Carrito

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `agregarItemAlCarrito(productoId, cantidad)`

```mermaid
sequenceDiagram
    title DSS — CU-122 Agregar Ítem al Carrito
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: agregarItemAlCarrito(productoId, cantidad)
    activate SIS
    alt el tipo de garrafa es válido
        SIS-->>CLI: carrito con el ítem agregado y el total
    else el tipo de garrafa no existe o está de baja
        SIS-->>CLI: operación rechazada
    end
    deactivate SIS
```

**Figura 46 — DSS CU-122: Agregar Ítem al Carrito**

---

#### DSS — CU-123: Modificar la Cantidad de un Ítem del Carrito

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `modificarCantidadDelItem(itemId, cantidad)`

```mermaid
sequenceDiagram
    title DSS — CU-123 Modificar la Cantidad de un Ítem del Carrito
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: modificarCantidadDelItem(itemId, cantidad)
    activate SIS
    alt el ítem es del carrito del cliente
        SIS-->>CLI: carrito con la cantidad actualizada
    else el ítem no es del carrito del cliente
        SIS-->>CLI: operación rechazada
    end
    deactivate SIS
```

**Figura 47 — DSS CU-123: Modificar la Cantidad de un Ítem del Carrito**

---

#### DSS — CU-124: Quitar Ítem del Carrito

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `quitarItemDelCarrito(itemId)`

```mermaid
sequenceDiagram
    title DSS — CU-124 Quitar Ítem del Carrito
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: quitarItemDelCarrito(itemId)
    activate SIS
    alt el ítem es del carrito del cliente
        SIS-->>CLI: carrito sin el ítem
    else el ítem no es del carrito del cliente
        SIS-->>CLI: operación rechazada
    end
    deactivate SIS
```

**Figura 48 — DSS CU-124: Quitar Ítem del Carrito**

---

#### DSS — CU-125: Consultar el Carrito

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `consultarCarrito()`

```mermaid
sequenceDiagram
    title DSS — CU-125 Consultar el Carrito
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarCarrito()
    activate SIS
    alt el cliente tiene carrito
        SIS-->>CLI: detalle del carrito, total a precio vigente y diferencias de precio
    else el cliente no tiene carrito
        SIS-->>CLI: carrito vacío
    end
    deactivate SIS
```

**Figura 49 — DSS CU-125: Consultar el Carrito**

---

#### DSS — CU-126: Vaciar el Carrito

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `vaciarCarrito()`

```mermaid
sequenceDiagram
    title DSS — CU-126 Vaciar el Carrito
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: vaciarCarrito()
    activate SIS
    alt el cliente tiene carrito
        SIS-->>CLI: carrito vacío
    else el cliente no tiene carrito
        SIS-->>CLI: carrito vacío
    end
    deactivate SIS
```

**Figura 50 — DSS CU-126: Vaciar el Carrito**

---

#### DSS — CU-127: Cambiar la Dirección de Entrega del Pedido

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `cambiarDireccionDeEntrega(pedidoId, direccionId, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-127 Cambiar la Dirección de Entrega del Pedido
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: cambiarDireccionDeEntrega(pedidoId, direccionId, motivo)
    activate SIS
    alt el pedido admite el cambio y la dirección es válida
        SIS-->>CLI: pedido actualizado
    else el pedido ya salió
        SIS-->>CLI: cambio rechazado
    else la dirección está fuera de la zona de cobertura
        SIS-->>CLI: cambio rechazado
    else el pedido está pagado en línea y el recargo de la zona nueva es distinto
        SIS-->>CLI: cambio rechazado
    end
    deactivate SIS
```

**Figura 51 — DSS CU-127: Cambiar la Dirección de Entrega del Pedido**

---

#### DSS — CU-128: Indicar Quién Recibe el Pedido

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `indicarQuienRecibe(pedidoId, nombre, documento, relacion)`

```mermaid
sequenceDiagram
    title DSS — CU-128 Indicar Quién Recibe el Pedido
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: indicarQuienRecibe(pedidoId, nombre, documento, relacion)
    activate SIS
    alt el pedido admite el dato
        SIS-->>CLI: pedido actualizado con quién recibe
    else el pedido ya fue entregado
        SIS-->>CLI: operación rechazada
    end
    deactivate SIS
```

**Figura 52 — DSS CU-128: Indicar Quién Recibe el Pedido**

---

#### DSS — CU-080: Consultar el Pool de Pedidos Disponibles

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarPedidosDisponibles(pagina, limite)`

```mermaid
sequenceDiagram
    title DSS — CU-080 Consultar el Pool de Pedidos Disponibles
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: consultarPedidosDisponibles(pagina, limite)
    activate SIS
    SIS-->>CHO: pedidos pendientes sin chofer de su distribuidora (dirección, ítems, total)
    deactivate SIS
```

**Figura 53 — DSS CU-080: Consultar el Pool de Pedidos Disponibles**

> Es la vista de respaldo del despacho automático (CU-013): si la oferta por proximidad no llega, el chofer puede consultar el pool.

---

#### DSS — CU-081: Consultar los Pedidos Asignados al Chofer

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarPedidosAsignados(choferId, pagina, limite)`

```mermaid
sequenceDiagram
    title DSS — CU-081 Consultar los Pedidos Asignados al Chofer
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: consultarPedidosAsignados(choferId, pagina, limite)
    activate SIS
    SIS-->>CHO: página de pedidos asignados (estado, cliente, dirección, total)
    deactivate SIS
```

**Figura 54 — DSS CU-081: Consultar los Pedidos Asignados al Chofer**

---

### SS-03 — Despacho y Asignación

#### DSS — CU-016: Rechazar / Ignorar Pedido

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `rechazarOferta(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-016 Rechazar / Ignorar Pedido
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema
    actor CH2 as Siguiente Chofer (ACT-02)

    CHO->>SIS: rechazarOferta(pedidoId)
    activate SIS
    alt El pedido existe
        SIS-->>CHO: rechazo registrado (se cierra la oferta si estaba activa)
        opt El pedido sigue pendiente y sin chofer asignado
            SIS-)CH2: notificarOferta(pedido)
        end
    else El pedido no existe
        SIS-->>CHO: sin efecto (rechazo no registrado)
    else El pedido es de otra distribuidora
        SIS-->>CHO: recurso no encontrado
    end
    deactivate SIS
```

**Figura 55 — DSS CU-016: Rechazar / Ignorar Pedido**

> El rechazo **no** espera el vencimiento de la ventana de 30 segundos: re-ofrece de inmediato al siguiente chofer más cercano.

---

### SS-04 — Seguimiento en Tiempo Real

#### DSS — CU-018: Marcar Pedido "En Camino"

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `marcarPedidoEnCamino(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-018 Marcar Pedido "En Camino"
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    CHO->>SIS: marcarPedidoEnCamino(pedidoId)
    activate SIS
    alt La transición es válida desde el estado actual
        SIS-->>CHO: pedido en camino (estado EN_CAMINO)
        SIS-)CLI: notificarPedidoEnCamino(pedido)
    else El pedido es de otra distribuidora
        SIS-->>CHO: recurso no encontrado
    else El pedido está asignado a otro chofer
        SIS-->>CHO: acceso denegado
    else La transición no está permitida
        SIS-->>CHO: error de solicitud (transición inválida)
    end
    deactivate SIS
```

**Figura 56 — DSS CU-018: Marcar Pedido "En Camino"**

---

#### DSS — CU-019: Avisar Llegada al Cliente

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `avisarLlegada(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-019 Avisar Llegada al Cliente
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    CHO->>SIS: avisarLlegada(pedidoId)
    activate SIS
    alt El pedido está en camino
        SIS-)CLI: notificarLlegadaDelChofer(pedido)
        Note over SIS: El aviso llega en tiempo<br/>real y como notificación<br/>al dispositivo
        SIS-->>CHO: cliente notificado
    else El pedido es de otra distribuidora
        SIS-->>CHO: recurso no encontrado
    else El pedido está asignado a otro chofer
        SIS-->>CHO: acceso denegado
    else El pedido no está en camino
        SIS-->>CHO: error de solicitud (el pedido no está en camino)
    end
    deactivate SIS
```

**Figura 57 — DSS CU-019: Avisar Llegada al Cliente**

> Este caso de uso **no** cambia el estado del pedido: solo notifica.

---

#### DSS — CU-021: Recibir Notificaciones en Tiempo Real

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `suscribirseAlSeguimiento(clienteId)`

```mermaid
sequenceDiagram
    title DSS — CU-021 Recibir Notificaciones en Tiempo Real
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: suscribirseAlSeguimiento(clienteId)
    activate SIS
    SIS-->>CLI: suscripción confirmada
    deactivate SIS

    loop Mientras el pedido esté en curso
        SIS-)CLI: notificarCambioDeEstado(pedido, estado)
        SIS-)CLI: notificarUbicacionDelChofer(pedido, latitud, longitud)
    end
    Note over CLI,SIS: Estados notificados: aceptado, en camino,<br/>entregado y cancelado
```

**Figura 58 — DSS CU-021: Recibir Notificaciones en Tiempo Real**

> El canal se cierra cuando el cliente cierra la aplicación o el pedido alcanza un estado terminal.

---

#### DSS — CU-022: Activar la Disponibilidad

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `cambiarDisponibilidad(usuarioId, disponible)`

```mermaid
sequenceDiagram
    title DSS — CU-022 Activar la Disponibilidad
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: cambiarDisponibilidad(usuarioId, disponible)
    activate SIS
    alt está habilitado y validado
        SIS-->>CHO: disponible (empieza a recibir ofertas de pedidos)
    else no está habilitado o validado
        SIS-->>CHO: acceso denegado
    end
    deactivate SIS
    Note over CHO,SIS: disponible = verdadero. La misma operación, con disponible = falso, es CU-266
```

**Figura 59 — DSS CU-022: Activar la Disponibilidad**

> **Observación de análisis:** el sistema almacena esta disponibilidad en el mismo atributo que el alta/baja administrativa (CU-033), por lo que "fuera de turno" y "dado de baja" son indistinguibles.

---


#### DSS — CU-266: Desactivar la Disponibilidad

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `cambiarDisponibilidad(usuarioId, disponible)`

```mermaid
sequenceDiagram
    title DSS — CU-266 Desactivar la Disponibilidad
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: cambiarDisponibilidad(usuarioId, disponible)
    activate SIS
    SIS-->>CHO: no disponible (deja de recibir ofertas)
    deactivate SIS
    Note over CHO,SIS: disponible = falso. Desconectarse se permite siempre.<br/>La misma operación, con disponible = verdadero, es CU-022
```

**Figura 60 — DSS CU-266: Desactivar la Disponibilidad**

---

#### DSS — CU-078: Obtener el Código de Entrega (QR del chofer)

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `obtenerCodigoDeEntrega(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-078 Obtener el Código de Entrega (QR del chofer)
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: obtenerCodigoDeEntrega(pedidoId)
    activate SIS
    alt el pedido está asignado a este chofer y ya fue aceptado
        SIS-->>CHO: código de entrega (para mostrarlo como QR al cliente)
    else el pedido no está asignado a este chofer
        SIS-->>CHO: acceso denegado
    else el pedido todavía no fue aceptado
        SIS-->>CHO: error de solicitud (el pedido aún no tiene código)
    else el pedido no existe o es de otra distribuidora
        SIS-->>CHO: recurso no encontrado
    end
    deactivate SIS
```

**Figura 61 — DSS CU-078: Obtener el Código de Entrega (QR del chofer)**

---

#### DSS — CU-079: Confirmar Entrega Escaneando el QR (cliente)

**Actor:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `confirmarEntregaConCodigo(pedidoId, codigo)`

```mermaid
sequenceDiagram
    title DSS — CU-079 Confirmar Entrega Escaneando el QR (cliente)
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: confirmarEntregaConCodigo(pedidoId, codigo)
    activate SIS
    alt el código coincide y el pedido está en camino
        SIS-->>CLI: entrega confirmada (estado ENTREGADO)
    else el código no coincide
        SIS-->>CLI: error de solicitud (código inválido)
    else el pedido no está en camino
        SIS-->>CLI: error de solicitud (el pedido no está en camino)
    else el pedido es de otro cliente
        SIS-->>CLI: acceso denegado
    end
    deactivate SIS
```

**Figura 62 — DSS CU-079: Confirmar Entrega Escaneando el QR (cliente)**

> Es el camino **anti-fraude** que invierte el actor de CU-020: confirma quien recibe, no quien entrega. Es idempotente frente a reintentos de red.

---

### SS-05 — Reclamos

#### DSS — CU-024: Listar Reclamos

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `listarReclamos()`

```mermaid
sequenceDiagram
    title DSS — CU-024 Listar Reclamos
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarReclamos()
    activate SIS
    SIS-->>ADM: reclamos de su distribuidora (pedido, cliente, motivo, estado)
    deactivate SIS
```

**Figura 63 — DSS CU-024: Listar Reclamos**

---

#### DSS — CU-025: Resolver Reclamo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `resolverReclamo(reclamoId, resolucion, estadoFinal)`

```mermaid
sequenceDiagram
    title DSS — CU-025 Resolver Reclamo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: resolverReclamo(reclamoId, resolucion, estadoFinal)
    activate SIS
    alt el reclamo existe y la transición es válida
        SIS-->>ADM: reclamo resuelto (estado y resolución registrados)
    else el reclamo no existe
        SIS-->>ADM: recurso no encontrado
    else la transición no es válida (resuelto/rechazado sin reabrir antes)
        SIS-->>ADM: transición de reclamo inválida
    end
    deactivate SIS
```

**Figura 64 — DSS CU-025: Resolver Reclamo**

---

#### DSS — CU-166: Tomar un Reclamo Pendiente

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `tomarReclamo(reclamoId)`

```mermaid
sequenceDiagram
    title DSS — CU-166 Tomar un Reclamo Pendiente
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: tomarReclamo(reclamoId)
    activate SIS
    alt el reclamo existe y está pendiente
        SIS-->>ADM: reclamo en proceso
    else el reclamo no existe
        SIS-->>ADM: recurso no encontrado
    else el reclamo no está pendiente
        SIS-->>ADM: solicitud inválida: sólo se toma un reclamo pendiente
    end
    deactivate SIS
```

**Figura 65 — DSS CU-166: Tomar un Reclamo Pendiente**

---

#### DSS — CU-167: Reabrir un Reclamo

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `reabrirReclamo(reclamoId, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-167 Reabrir un Reclamo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: reabrirReclamo(reclamoId, motivo)
    activate SIS
    alt el reclamo existe y está resuelto o rechazado
        SIS-->>ADM: reclamo en proceso, con el motivo de la reapertura
    else el reclamo no existe
        SIS-->>ADM: recurso no encontrado
    else el reclamo no está resuelto ni rechazado
        SIS-->>ADM: solicitud inválida: sólo se reabre un reclamo cerrado
    end
    deactivate SIS
```

**Figura 66 — DSS CU-167: Reabrir un Reclamo**

---

#### DSS — CU-174: Adjuntar la Fotografía de un Reclamo

**Actor:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `adjuntarFotoAlReclamo(reclamoId, imagen)`

```mermaid
sequenceDiagram
    title DSS — CU-174 Adjuntar la Fotografía de un Reclamo
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: adjuntarFotoAlReclamo(reclamoId, imagen)
    activate SIS
    alt la imagen es válida y el reclamo es del solicitante
        SIS-->>CLI: reclamo con su fotografía
    else el reclamo no existe o no es del solicitante
        SIS-->>CLI: recurso no encontrado
    else el reclamo está resuelto o rechazado
        SIS-->>CLI: conflicto, hay que reabrirlo
    else el tipo de archivo no está permitido
        SIS-->>CLI: tipo de archivo no soportado
    else el archivo supera el tamaño máximo
        SIS-->>CLI: archivo demasiado grande
    end
    deactivate SIS
```

**Figura 67 — DSS CU-174: Adjuntar la Fotografía de un Reclamo**

---

#### DSS — CU-175: Consultar la Fotografía de un Reclamo

**Actor:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarFotoDelReclamo(reclamoId)`

```mermaid
sequenceDiagram
    title DSS — CU-175 Consultar la Fotografía de un Reclamo
    autonumber
    actor USR as Cliente (ACT-01)
    participant SIS as :Sistema

    USR->>SIS: consultarFotoDelReclamo(reclamoId)
    activate SIS
    alt el reclamo tiene fotografía y el usuario puede verlo
        SIS-->>USR: fotografía del reclamo
    else el reclamo no existe o no es del usuario
        SIS-->>USR: recurso no encontrado
    else el reclamo no tiene fotografía
        SIS-->>USR: recurso no encontrado
    end
    deactivate SIS
    Note over USR,SIS: También lo inician el Administrador (ACT-03) y<br/>el Administrador General (ACT-05)
```

**Figura 68 — DSS CU-175: Consultar la Fotografía de un Reclamo**

---

### SS-06 — Reportes y Dashboard

#### DSS — CU-026: Ver Dashboard General

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarResumenDePedidos()`, `consultarGraficoDeVentas()`

```mermaid
sequenceDiagram
    title DSS — CU-026 Ver Dashboard General
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarResumenDePedidos()
    activate SIS
    SIS-->>ADM: totales del día, la semana y el mes (pedidos, facturación, estados)
    deactivate SIS

    ADM->>SIS: consultarGraficoDeVentas()
    activate SIS
    SIS-->>ADM: serie de ventas de los últimos siete días
    deactivate SIS
```

**Figura 69 — DSS CU-026: Ver Dashboard General**

---

#### DSS — CU-027: Ver Reporte de Ventas por Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarVentasPorChofer(fechaDesde, fechaHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-027 Ver Reporte de Ventas por Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarVentasPorChofer(fechaDesde, fechaHasta)
    activate SIS
    SIS-->>ADM: ranking por chofer (pedidos entregados, monto facturado)
    deactivate SIS
```

**Figura 70 — DSS CU-027: Ver Reporte de Ventas por Chofer**

---

#### DSS — CU-028: Ver Reporte de Ventas por Producto

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarVentasPorProducto(fechaDesde, fechaHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-028 Ver Reporte de Ventas por Producto
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarVentasPorProducto(fechaDesde, fechaHasta)
    activate SIS
    SIS-->>ADM: ventas por tipo de garrafa (unidades, monto)
    deactivate SIS
```

**Figura 71 — DSS CU-028: Ver Reporte de Ventas por Producto**

---

#### DSS — CU-029: Ver Reporte por Método de Pago

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarVentasPorMetodoDePago(fechaDesde, fechaHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-029 Ver Reporte por Método de Pago
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarVentasPorMetodoDePago(fechaDesde, fechaHasta)
    activate SIS
    SIS-->>ADM: distribución entre efectivo y pasarela (cantidad, monto)
    deactivate SIS
```

**Figura 72 — DSS CU-029: Ver Reporte por Método de Pago**

---

#### DSS — CU-030: Ver Gráfico de Ventas (últimos 7 días)

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarEvolucionDeVentas(fechaDesde, fechaHasta, granularidad)`

```mermaid
sequenceDiagram
    title DSS — CU-030 Ver Gráfico de Ventas (últimos 7 días)
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarEvolucionDeVentas(fechaDesde, fechaHasta, granularidad)
    activate SIS
    alt granularidad diaria
        SIS-->>ADM: serie por día del rango solicitado
    else granularidad mensual
        SIS-->>ADM: serie por mes del rango solicitado
    end
    deactivate SIS
```

**Figura 73 — DSS CU-030: Ver Gráfico de Ventas (últimos 7 días)**

---

### SS-07 — Gestión de Choferes y Vehículos

#### DSS — CU-031: Registrar Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarChofer(datosPersonales, datosDelChofer, distribuidoraId)`

```mermaid
sequenceDiagram
    title DSS — CU-031 Registrar Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarChofer(datosPersonales, datosDelChofer, distribuidoraId)
    activate SIS
    alt puede dar de alta en esa distribuidora y los datos son válidos
        SIS-->>ADM: chofer registrado (usuarioId, perfil de chofer, rol CHOFER)
    else la distribuidora no es la suya, o no tiene distribuidora asociada
        SIS-->>ADM: acceso denegado
    else correo o teléfono ya registrados
        SIS-->>ADM: conflicto (el correo o el teléfono ya están en uso)
    else datos inválidos o falta la distribuidora
        SIS-->>ADM: error de validación
    end
    deactivate SIS
```

**Figura 74 — DSS CU-031: Registrar Chofer**

> Realiza la misma operación del sistema que CU-003, vista desde el subsistema de gestión de flota.

---

#### DSS — CU-032: Validar un Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `validarChofer(choferId)`

```mermaid
sequenceDiagram
    title DSS — CU-032 Validar un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: validarChofer(choferId)
    activate SIS
    SIS-->>ADM: chofer validado (habilitado para recibir pedidos)
    deactivate SIS
```

**Figura 75 — DSS CU-032: Validar un Chofer**

---


#### DSS — CU-271: Invalidar un Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `invalidarChofer(choferId)`

```mermaid
sequenceDiagram
    title DSS — CU-271 Invalidar un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: invalidarChofer(choferId)
    activate SIS
    SIS-->>ADM: chofer invalidado (deja de sumar entre los habilitados)
    deactivate SIS
```

**Figura 76 — DSS CU-271: Invalidar un Chofer**

---

#### DSS — CU-033: Activar un Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `cambiarEstadoDelChofer(choferId, activo)`

```mermaid
sequenceDiagram
    title DSS — CU-033 Activar un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: cambiarEstadoDelChofer(choferId, activo)
    activate SIS
    alt el chofer existe
        SIS-->>ADM: chofer activado
    else el chofer no existe o es de otra distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
    Note over ADM,SIS: activo = verdadero. La misma operación, con activo = falso, es CU-267
```

**Figura 77 — DSS CU-033: Activar un Chofer**

---


#### DSS — CU-267: Desactivar un Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `cambiarEstadoDelChofer(choferId, activo)`

```mermaid
sequenceDiagram
    title DSS — CU-267 Desactivar un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: cambiarEstadoDelChofer(choferId, activo)
    activate SIS
    alt el chofer existe
        SIS-->>ADM: chofer desactivado (fuera de línea y fuera del radar)
    else el chofer no existe o es de otra distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
    Note over ADM,SIS: activo = falso. La misma operación, con activo = verdadero, es CU-033
```

**Figura 78 — DSS CU-267: Desactivar un Chofer**

---

#### DSS — CU-034: Registrar Vehículo del Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarVehiculo(usuarioId, tipo, capacidad, patente, marca, modelo, anio, color)`

```mermaid
sequenceDiagram
    title DSS — CU-034 Registrar Vehículo del Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarVehiculo(usuarioId, tipo, capacidad, patente, marca, modelo, anio, color)
    activate SIS
    alt datos válidos
        SIS-->>ADM: vehículo registrado (vehiculoId)
    else datos inválidos
        SIS-->>ADM: error de validación
    end
    deactivate SIS
```

**Figura 79 — DSS CU-034: Registrar Vehículo del Chofer**

---

#### DSS — CU-035: Consultar Listado de Choferes

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `listarChoferes(pagina, limite)`, `listarChoferesActivos(pagina, limite)`, `consultarDetalleDelChofer(choferId)`

```mermaid
sequenceDiagram
    title DSS — CU-035 Consultar Listado de Choferes
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarChoferes(pagina, limite)
    activate SIS
    SIS-->>ADM: página de choferes de su distribuidora
    deactivate SIS

    opt vista operativa del día
        ADM->>SIS: listarChoferesActivos(pagina, limite)
        activate SIS
        SIS-->>ADM: choferes activos
        deactivate SIS
    end

    opt ficha individual
        ADM->>SIS: consultarDetalleDelChofer(choferId)
        activate SIS
        alt el chofer existe
            SIS-->>ADM: ficha del chofer (validación, calificación, saldo, vehículo)
        else el chofer no existe
            SIS-->>ADM: recurso no encontrado
        end
        deactivate SIS
    end
```

**Figura 80 — DSS CU-035: Consultar Listado de Choferes**

---

#### DSS — CU-049: Consultar Balance / Ganancias del Chofer

**Actor:** Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `consultarPerfilDelChofer(usuarioId)`, `ajustarSaldoDelChofer(choferId, monto)`

```mermaid
sequenceDiagram
    title DSS — CU-049 Consultar Balance / Ganancias del Chofer
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema
    actor ADM as Administrador (ACT-03)

    CHO->>SIS: consultarPerfilDelChofer(usuarioId)
    activate SIS
    SIS-->>CHO: perfil con el saldo acumulado
    deactivate SIS

    opt liquidación o corrección
        ADM->>SIS: ajustarSaldoDelChofer(choferId, monto)
        activate SIS
        SIS-->>ADM: saldo actualizado
        deactivate SIS
    end
```

**Figura 81 — DSS CU-049: Consultar Balance / Ganancias del Chofer**

> **Observación de análisis:** no existe una operación dedicada de consulta de saldo; el chofer lo lee dentro de su propio perfil.

---

#### DSS — CU-051: Consultar Listado de Vehículos

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `listarVehiculos()`, `buscarVehiculoPorPatente(patente)`, `editarVehiculo(vehiculoId, datos)`, `eliminarVehiculo(vehiculoId)`

```mermaid
sequenceDiagram
    title DSS — CU-051 Consultar Listado de Vehículos
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarVehiculos()
    activate SIS
    SIS-->>ADM: vehículos de la distribuidora
    deactivate SIS

    opt búsqueda por patente
        ADM->>SIS: buscarVehiculoPorPatente(patente)
        activate SIS
        alt existe
            SIS-->>ADM: vehículo encontrado
        else no existe
            SIS-->>ADM: recurso no encontrado
        end
        deactivate SIS
    end

    opt modificación
        ADM->>SIS: editarVehiculo(vehiculoId, datos)
        activate SIS
        SIS-->>ADM: vehículo actualizado
        deactivate SIS
    end

    opt baja
        ADM->>SIS: eliminarVehiculo(vehiculoId)
        activate SIS
        SIS-->>ADM: vehículo eliminado
        deactivate SIS
    end
```

**Figura 82 — DSS CU-051: Consultar Listado de Vehículos**

---

#### DSS — CU-096: Actualizar Perfil del Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `actualizarPerfilDelChofer(choferId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-096 Actualizar Perfil del Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: actualizarPerfilDelChofer(choferId, datos)
    activate SIS
    alt el chofer existe
        SIS-->>ADM: perfil del chofer actualizado
    else el chofer no existe o es de otra distribuidora
        SIS-->>ADM: recurso no encontrado
    else los datos traen un campo distinto de la validación
        SIS-->>ADM: error de solicitud (campo no admitido)
    end
    deactivate SIS
```

**Figura 83 — DSS CU-096: Actualizar Perfil del Chofer**

---

#### DSS — CU-097: Eliminar Chofer (baja lógica)

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `eliminarChofer(choferId)`

```mermaid
sequenceDiagram
    title DSS — CU-097 Eliminar Chofer (baja lógica)
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: eliminarChofer(choferId)
    activate SIS
    alt el chofer existe y no tiene pedidos en curso
        SIS-->>ADM: chofer dado de baja junto con su cuenta, retirado del radar y con su vehículo en uso liberado (se conserva el histórico de entregas)
    else el chofer tiene pedidos aceptados o en camino
        SIS-->>ADM: conflicto, el chofer tiene pedidos en curso
    else el chofer no existe o es de otra distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 84 — DSS CU-097: Eliminar Chofer (baja lógica)**

---

#### DSS — CU-109: Consultar Detalle del Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarDetalleDelChofer(choferId)`

```mermaid
sequenceDiagram
    title DSS — CU-109 Consultar Detalle del Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarDetalleDelChofer(choferId)
    activate SIS
    alt el chofer existe
        SIS-->>ADM: ficha del chofer con vehículo y estado
    else el chofer no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 85 — DSS CU-109: Consultar Detalle del Chofer**

---

#### DSS — CU-110: Buscar Chofer por Usuario

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `buscarChoferPorUsuario(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-110 Buscar Chofer por Usuario
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: buscarChoferPorUsuario(usuarioId)
    activate SIS
    alt la cuenta tiene perfil de chofer
        SIS-->>ADM: perfil del chofer
    else la cuenta no tiene perfil
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 86 — DSS CU-110: Buscar Chofer por Usuario**

---

#### DSS — CU-111: Editar Vehículo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `editarVehiculo(vehiculoId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-111 Editar Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: editarVehiculo(vehiculoId, datos)
    activate SIS
    alt el vehículo existe y los cambios son admisibles
        SIS-->>ADM: vehículo actualizado
    else la patente ya pertenece a otro vehículo
        SIS-->>ADM: patente repetida
    else se cambia la patente o el tipo de un vehículo en uso
        SIS-->>ADM: conflicto (el vehículo está en uso: liberalo primero)
    else el vehículo no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 87 — DSS CU-111: Editar Vehículo**

---

#### DSS — CU-112: Eliminar Vehículo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `eliminarVehiculo(vehiculoId)`

```mermaid
sequenceDiagram
    title DSS — CU-112 Eliminar Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: eliminarVehiculo(vehiculoId)
    activate SIS
    alt el vehículo existe y está libre
        SIS-->>ADM: vehículo dado de baja (baja lógica, la patente queda libre)
    else el vehículo está en uso por un chofer
        SIS-->>ADM: conflicto, el vehículo está en uso: hay que liberarlo primero
    else el vehículo no existe o es de otra distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 88 — DSS CU-112: Eliminar Vehículo**

---

#### DSS — CU-113: Consultar Detalle del Vehículo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarDetalleDelVehiculo(vehiculoId)`

```mermaid
sequenceDiagram
    title DSS — CU-113 Consultar Detalle del Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarDetalleDelVehiculo(vehiculoId)
    activate SIS
    alt el vehículo existe
        SIS-->>ADM: ficha del vehículo con su chofer
    else el vehículo no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 89 — DSS CU-113: Consultar Detalle del Vehículo**

---

#### DSS — CU-114: Buscar Vehículo por Patente

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `buscarVehiculoPorPatente(patente)`

```mermaid
sequenceDiagram
    title DSS — CU-114 Buscar Vehículo por Patente
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: buscarVehiculoPorPatente(patente)
    activate SIS
    alt hay un vehículo con esa patente
        SIS-->>ADM: ficha del vehículo
    else ninguno coincide
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 90 — DSS CU-114: Buscar Vehículo por Patente**

---

#### DSS — CU-115: Consultar Vehículos de un Chofer

**Actor:** Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `consultarVehiculosDelChofer(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-115 Consultar Vehículos de un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarVehiculosDelChofer(usuarioId)
    activate SIS
    alt la cuenta tiene vehículos
        SIS-->>ADM: lista de vehículos
    else la cuenta no tiene ninguno
        SIS-->>ADM: lista vacía
    end
    deactivate SIS
```

**Figura 91 — DSS CU-115: Consultar Vehículos de un Chofer**

---

#### DSS — CU-136: Registrar el Seguro del Vehículo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearTareaDeFlota(planId, recursoId, vencimiento, detalle)`

```mermaid
sequenceDiagram
    title DSS — CU-136 Registrar el Seguro del Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearTareaDeFlota(planId, recursoId, vencimiento, detalle)
    activate SIS
    alt el seguro está vigente
        SIS-->>ADM: vehículo habilitado
    else el seguro está vencido
        SIS-->>ADM: dato guardado y vehículo no habilitado
    else el vehículo no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 92 — DSS CU-136: Registrar el Seguro del Vehículo**

---

#### DSS — CU-137: Registrar la Verificación Técnica Vehicular

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearTareaDeFlota(planId, recursoId, vencimiento, detalle)`

```mermaid
sequenceDiagram
    title DSS — CU-137 Registrar la Verificación Técnica Vehicular
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearTareaDeFlota(planId, recursoId, vencimiento, detalle)
    activate SIS
    alt la verificación está vigente
        SIS-->>ADM: vehículo habilitado
    else la verificación está vencida
        SIS-->>ADM: dato guardado y vehículo no habilitado
    else el vehículo no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 93 — DSS CU-137: Registrar la Verificación Técnica Vehicular**

---

#### DSS — CU-138: Registrar la Licencia de Conducir del Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearTareaDeFlota(planId, recursoId, vencimiento, detalle)`

```mermaid
sequenceDiagram
    title DSS — CU-138 Registrar la Licencia de Conducir del Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearTareaDeFlota(planId, recursoId, vencimiento, detalle)
    activate SIS
    alt los datos son validos
        SIS-->>ADM: tarea creada, categoria guardada sin verificar contra el vehiculo
    else la licencia ya esta vencida al cargarla
        SIS-->>ADM: tarea creada y chofer no habilitado
    end
    deactivate SIS
```

**Figura 94 — DSS CU-138: Registrar la Licencia de Conducir del Chofer**

---

#### DSS — CU-139: Consultar los Vencimientos de la Flota

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarVencimientosDeLaFlota(dias)`

```mermaid
sequenceDiagram
    title DSS — CU-139 Consultar los Vencimientos de la Flota
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarVencimientosDeLaFlota(dias)
    activate SIS
    alt hay vencimientos en la ventana
        SIS-->>ADM: listado ordenado por fecha
    else no hay ninguno
        SIS-->>ADM: listado vacío
    end
    deactivate SIS
```

**Figura 95 — DSS CU-139: Consultar los Vencimientos de la Flota**

---

#### DSS — CU-140: Programar un Mantenimiento de Vehículo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearTareaDeFlota(planId, recursoId, vencimiento, detalle)`

```mermaid
sequenceDiagram
    title DSS — CU-140 Programar un Mantenimiento de Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearTareaDeFlota(planId, recursoId, vencimiento, detalle)
    activate SIS
    alt los datos son válidos
        SIS-->>ADM: mantenimiento agendado
    else el vehículo o el plan no existen
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 96 — DSS CU-140: Programar un Mantenimiento de Vehículo**

---

#### DSS — CU-141: Registrar un Mantenimiento Realizado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `cerrarTareaDeFlota(tareaId, fecha, kilometraje, costo, observacion)`

```mermaid
sequenceDiagram
    title DSS — CU-141 Registrar un Mantenimiento Realizado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: cerrarTareaDeFlota(tareaId, fecha, kilometraje, costo, observacion)
    activate SIS
    alt la tarea esta abierta
        SIS-->>ADM: tarea cerrada
    else la tarea ya estaba hecha o cancelada
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 97 — DSS CU-141: Registrar un Mantenimiento Realizado**

---

#### DSS — CU-142: Avisar los Vencimientos Próximos de la Flota

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `avisarVencimientosPendientes()`

```mermaid
sequenceDiagram
    title DSS — CU-142 Avisar los Vencimientos Próximos de la Flota
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor ADM as Administrador (ACT-03)

    Note over SAU: Se ejecuta una vez por<br/>día
    SAU->>SIS: avisarVencimientosPendientes()
    activate SIS
    alt Hay habilitaciones por vencer sin avisar
        SIS-)ADM: notificarVencimientosDeLaFlota(tareas)
        Note over SIS: El aviso sale por correo<br/>a los administradores de<br/>cada distribuidora
        SIS-->>SAU: avisos enviados
    else No hay ninguna
        SIS-->>SAU: el ciclo termina sin avisos
    end
    deactivate SIS
```

**Figura 98 — DSS CU-142: Avisar los Vencimientos Próximos de la Flota**

---

#### DSS — CU-155: Adjuntar Archivo a una Tarea de Flota

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `adjuntarArchivoALaTarea(tareaId, archivo)`

```mermaid
sequenceDiagram
    title DSS — CU-155 Adjuntar Archivo a una Tarea de Flota
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: adjuntarArchivoALaTarea(tareaId, archivo)
    activate SIS
    alt el archivo es de un tipo y un tamaño permitidos
        SIS-->>ADM: adjunto creado
    else el tipo no está permitido
        SIS-->>ADM: tipo de archivo no soportado
    else el archivo supera el tamaño máximo
        SIS-->>ADM: archivo demasiado grande
    else la tarea no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 99 — DSS CU-155: Adjuntar Archivo a una Tarea de Flota**

---

#### DSS — CU-156: Consultar Adjuntos de una Tarea de Flota

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarAdjuntosDeLaTarea(tareaId)`

```mermaid
sequenceDiagram
    title DSS — CU-156 Consultar Adjuntos de una Tarea de Flota
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarAdjuntosDeLaTarea(tareaId)
    activate SIS
    alt la tarea existe
        SIS-->>ADM: listado de adjuntos
    else la tarea no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 100 — DSS CU-156: Consultar Adjuntos de una Tarea de Flota**

---

#### DSS — CU-157: Descargar un Adjunto de Flota

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `descargarAdjunto(tareaId, adjuntoId)`

```mermaid
sequenceDiagram
    title DSS — CU-157 Descargar un Adjunto de Flota
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: descargarAdjunto(tareaId, adjuntoId)
    activate SIS
    alt el adjunto existe
        SIS-->>ADM: dirección de descarga firmada, de corta vigencia, con la que se baja el archivo
    else el adjunto no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 101 — DSS CU-157: Descargar un Adjunto de Flota**

---

#### DSS — CU-158: Eliminar un Adjunto de Flota

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `eliminarAdjunto(tareaId, adjuntoId)`

```mermaid
sequenceDiagram
    title DSS — CU-158 Eliminar un Adjunto de Flota
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: eliminarAdjunto(tareaId, adjuntoId)
    activate SIS
    alt el adjunto existe
        SIS-->>ADM: adjunto eliminado
    else el adjunto no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 102 — DSS CU-158: Eliminar un Adjunto de Flota**

---

#### DSS — CU-159: Almacenar Archivo

**Actor:** ninguno directo (caso incluido)

Caso incluido: no tiene diagrama de secuencia propio. Lo incluyen CU-155 (Adjuntar Archivo a una Tarea de Flota) y CU-174 (Adjuntar la Fotografía de un Reclamo), cuyos diagramas de secuencia muestran el efecto de guardar el archivo (caso base).

---

#### DSS — CU-160: Recuperar Archivo

**Actor:** ninguno directo (caso incluido)

Caso incluido: no tiene diagrama de secuencia propio. Lo incluyen CU-157 (Descargar un Adjunto de Flota) y CU-175 (Consultar la Fotografía de un Reclamo), cuyos diagramas de secuencia muestran la entrega del archivo (caso base).

---

#### DSS — CU-161: Poner un Vehículo en Uso para un Chofer

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `ponerVehiculoEnUso(choferId, vehiculoId, nota)`

```mermaid
sequenceDiagram
    title DSS — CU-161 Poner un Vehículo en Uso para un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: ponerVehiculoEnUso(choferId, vehiculoId, nota)
    activate SIS
    alt el chofer y el vehículo son de la distribuidora, el vehículo está habilitado y no hay pedidos en curso
        SIS-->>ADM: vehículo en uso (asignación abierta, anteriores cerradas)
    else el chofer o el vehículo no existe
        SIS-->>ADM: recurso no encontrado
    else el vehículo está inhabilitado por documentación vencida
        SIS-->>ADM: asignación rechazada, con el motivo del vencimiento
    else el chofer, o el que usa el vehículo, tiene un pedido en curso
        SIS-->>ADM: conflicto: pedido en curso
    end
    deactivate SIS
```

**Figura 103 — DSS CU-161: Poner un Vehículo en Uso para un Chofer**

---

#### DSS — CU-162: Liberar el Vehículo en Uso de un Chofer

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `liberarVehiculoEnUso(choferId)`

```mermaid
sequenceDiagram
    title DSS — CU-162 Liberar el Vehículo en Uso de un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: liberarVehiculoEnUso(choferId)
    activate SIS
    alt el chofer es de la distribuidora, tiene un vehículo en uso y no tiene un pedido en curso
        SIS-->>ADM: vehículo liberado
    else el chofer no existe o no tiene un vehículo en uso
        SIS-->>ADM: recurso no encontrado
    else el chofer tiene un pedido en curso
        SIS-->>ADM: conflicto: pedido en curso
    end
    deactivate SIS
```

**Figura 104 — DSS CU-162: Liberar el Vehículo en Uso de un Chofer**

---

#### DSS — CU-163: Consultar el Vehículo en Uso de un Chofer

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarVehiculoEnUso(choferId)`, `consultarMiVehiculoEnUso()`

```mermaid
sequenceDiagram
    title DSS — CU-163 Consultar el Vehículo en Uso de un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    ADM->>SIS: consultarVehiculoEnUso(choferId)
    activate SIS
    alt el chofer es de la distribuidora y tiene un vehículo en uso
        SIS-->>ADM: vehículo en uso, con su estado de habilitación
    else el chofer es de la distribuidora y no tiene un vehículo en uso
        SIS-->>ADM: respuesta sin vehículo
    else el chofer no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
    CHO->>SIS: consultarMiVehiculoEnUso()
    activate SIS
    alt el chofer tiene un vehículo en uso
        SIS-->>CHO: vehículo en uso, con su estado de habilitación
    else el chofer no tiene un vehículo en uso
        SIS-->>CHO: respuesta sin vehículo
    end
    deactivate SIS
```

**Figura 105 — DSS CU-163: Consultar el Vehículo en Uso de un Chofer**

---

#### DSS — CU-164: Consultar el Historial de Vehículos de un Chofer

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarHistorialDeVehiculosDelChofer(choferId, pagina)`

```mermaid
sequenceDiagram
    title DSS — CU-164 Consultar el Historial de Vehículos de un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarHistorialDeVehiculosDelChofer(choferId, pagina)
    activate SIS
    alt el chofer es de la distribuidora
        SIS-->>ADM: página de asignaciones y total
    else el chofer no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 106 — DSS CU-164: Consultar el Historial de Vehículos de un Chofer**

---

#### DSS — CU-165: Consultar el Historial de Choferes de un Vehículo

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarHistorialDeChoferesDelVehiculo(vehiculoId, pagina)`

```mermaid
sequenceDiagram
    title DSS — CU-165 Consultar el Historial de Choferes de un Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarHistorialDeChoferesDelVehiculo(vehiculoId, pagina)
    activate SIS
    alt el vehículo es de la distribuidora
        SIS-->>ADM: página de asignaciones y total
    else el vehículo no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 107 — DSS CU-165: Consultar el Historial de Choferes de un Vehículo**

---

#### DSS — CU-195: Registrar una Carga de Combustible

**Actor:** Administrador (ACT-03), Chofer (ACT-02)
**Operaciones del sistema:** `registrarCargaDeCombustible(vehiculoId, datos)`, `modificarCargaDeCombustible(cargaId, datos)`, `anularCargaDeCombustible(cargaId)`, `consultarCargasDeCombustible(filtros)`

```mermaid
sequenceDiagram
    title DSS — CU-195 Registrar una Carga de Combustible
    autonumber
    actor ADM as Administrador (ACT-03)
    actor CHF as Chofer (ACT-02)
    participant SIS as :Sistema

    ADM->>SIS: registrarCargaDeCombustible(vehiculoId, datos)
    activate SIS
    alt la carga es válida
        SIS-->>ADM: carga registrada, con el kilometraje del vehículo actualizado
        opt el consumo del tramo se aparta del promedio
            SIS-)ADM: notificarCargaAnomala(carga)
        end
    else el vehículo no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el kilometraje es menor que el de la última carga, el importe no coincide o los litros superan el tanque
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS

    Note over CHF,SIS: El chofer no indica el vehículo:<br/>el sistema usa el que tiene en uso
    CHF->>SIS: registrarCargaDeCombustible(vehiculoId, datos)
    activate SIS
    alt la carga es válida
        SIS-->>CHF: carga registrada
    else el chofer no tiene un vehículo en uso
        SIS-->>CHF: conflicto: sin vehículo en uso
    else el kilometraje es menor que el de la última carga, el importe no coincide o los litros superan el tanque
        SIS-->>CHF: solicitud inválida, con el detalle del campo
    end
    deactivate SIS

    ADM->>SIS: modificarCargaDeCombustible(cargaId, datos)
    activate SIS
    alt la carga existe y no está anulada
        SIS-->>ADM: carga modificada
    else la carga no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else los datos no cumplen las reglas de la carga
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS

    ADM->>SIS: anularCargaDeCombustible(cargaId)
    activate SIS
    alt la carga existe y no está anulada
        SIS-->>ADM: carga anulada, con el kilometraje del vehículo recalculado
    else la carga no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS

    ADM->>SIS: consultarCargasDeCombustible(filtros)
    activate SIS
    SIS-->>ADM: cargas vigentes que cumplen los filtros, con el total
    deactivate SIS
```

**Figura 108 — DSS CU-195: Registrar una Carga de Combustible**

---

#### DSS — CU-196: Consultar el Consumo de Combustible de un Vehículo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarConsumoDeCombustible(vehiculoId, fechaDesde, fechaHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-196 Consultar el Consumo de Combustible de un Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarConsumoDeCombustible(vehiculoId, fechaDesde, fechaHasta)
    activate SIS
    alt el vehículo existe y el rango es válido
        SIS-->>ADM: tramos, kilómetros por litro, costo por kilómetro y anomalías del período
    else el vehículo no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el rango de fechas no es válido
        SIS-->>ADM: solicitud inválida
    end
    deactivate SIS
```

**Figura 109 — DSS CU-196: Consultar el Consumo de Combustible de un Vehículo**

---

#### DSS — CU-197: Registrar la Habilitación para Transportar Mercancías Peligrosas

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearTareaDeFlota(planId, recursoId, vencimiento, detalle)`

```mermaid
sequenceDiagram
    title DSS — CU-197 Registrar la Habilitación para Transportar Mercancías Peligrosas
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearTareaDeFlota(planId, recursoId, vencimiento, detalle)
    activate SIS
    alt el plan y el vehículo existen y los datos son válidos
        SIS-->>ADM: habilitación registrada, con su estado de vencimiento y si bloquea
    else el plan o el vehículo no existen en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else falta el vencimiento o la vigencia es incoherente
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS
```

**Figura 110 — DSS CU-197: Registrar la Habilitación para Transportar Mercancías Peligrosas**

---

#### DSS — CU-198: Registrar una Multa de Tránsito

**Actor:** Administrador (ACT-03), Sistema Automático (ACT-04)
**Operaciones del sistema:** `registrarMultaDeTransito(vehiculoId, datos)`, `modificarMultaDeTransito(multaId, datos)`, `anularMultaDeTransito(multaId, motivo)`, `consultarMultasDeTransito(filtros)`, `avisarMultasPorVencer()`

```mermaid
sequenceDiagram
    title DSS — CU-198 Registrar una Multa de Tránsito
    autonumber
    actor ADM as Administrador (ACT-03)
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    ADM->>SIS: registrarMultaDeTransito(vehiculoId, datos)
    activate SIS
    alt los datos son válidos y el acta no estaba registrada
        SIS-->>ADM: multa registrada, pendiente, con el chofer deducido
    else el vehículo no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else ya existe una multa con esa jurisdicción y ese número de acta
        SIS-->>ADM: conflicto: multa ya registrada
    else falta un dato o el importe no es positivo
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS

    ADM->>SIS: modificarMultaDeTransito(multaId, datos)
    activate SIS
    alt la multa existe y no está pagada ni anulada
        SIS-->>ADM: multa modificada
    else la multa no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else la multa está pagada o anulada
        SIS-->>ADM: solicitud inválida: la multa no admite cambios
    end
    deactivate SIS

    ADM->>SIS: anularMultaDeTransito(multaId, motivo)
    activate SIS
    alt la multa existe y no está pagada ni anulada
        SIS-->>ADM: multa anulada
    else la multa no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else la multa está pagada o anulada
        SIS-->>ADM: solicitud inválida: la multa no se puede anular
    else falta el motivo
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS

    ADM->>SIS: consultarMultasDeTransito(filtros)
    activate SIS
    SIS-->>ADM: multas que cumplen los filtros, con el total
    deactivate SIS

    Note over SAU,SIS: Se ejecuta una vez por día,<br/>a las 08:00 hora argentina
    SAU->>SIS: avisarMultasPorVencer()
    activate SIS
    alt hay multas pendientes que vencen en siete días o menos, o ya vencidas, sin aviso
        SIS-)ADM: notificarMultasPorVencer(multas)
        SIS-->>SAU: avisos enviados
    else no hay ninguna
        SIS-->>SAU: el ciclo termina sin avisos
    end
    deactivate SIS
```

**Figura 111 — DSS CU-198: Registrar una Multa de Tránsito**

---

#### DSS — CU-199: Registrar el Pago de una Multa

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarPagoDeMulta(multaId, fechaDePago, importePagado)`

```mermaid
sequenceDiagram
    title DSS — CU-199 Registrar el Pago de una Multa
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarPagoDeMulta(multaId, fechaDePago, importePagado)
    activate SIS
    alt la multa existe y está pendiente o apelada
        SIS-->>ADM: multa pagada, con su fecha y su importe pagado
    else la multa no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else la multa ya está pagada o anulada
        SIS-->>ADM: solicitud inválida: la multa no admite el pago
    end
    deactivate SIS
```

**Figura 112 — DSS CU-199: Registrar el Pago de una Multa**

---

#### DSS — CU-200: Imputar una Multa al Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `imputarMultaAlChofer(multaId, empleadoId)`

```mermaid
sequenceDiagram
    title DSS — CU-200 Imputar una Multa al Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: imputarMultaAlChofer(multaId, empleadoId)
    activate SIS
    alt la multa y el empleado existen y la multa no está anulada
        SIS-->>ADM: multa imputada al empleado
    else la multa o el empleado no existen en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else la multa está anulada
        SIS-->>ADM: solicitud inválida: la multa anulada no se imputa
    end
    deactivate SIS
```

**Figura 113 — DSS CU-200: Imputar una Multa al Chofer**

---

#### DSS — CU-201: Registrar un Siniestro

**Actor:** Administrador (ACT-03), Chofer (ACT-02)
**Operaciones del sistema:** `registrarSiniestro(vehiculoId, datos)`, `modificarSiniestro(siniestroId, datos)`, `consultarSiniestros(filtros)`

```mermaid
sequenceDiagram
    title DSS — CU-201 Registrar un Siniestro
    autonumber
    actor ADM as Administrador (ACT-03)
    actor CHF as Chofer (ACT-02)
    participant SIS as :Sistema

    ADM->>SIS: registrarSiniestro(vehiculoId, datos)
    activate SIS
    alt los datos son válidos
        SIS-->>ADM: siniestro denunciado, con el vehículo fuera de servicio y su asignación cerrada si quedó inutilizable
        opt hubo derrame de gas
            SIS-)ADM: notificarDerrameDeGas(siniestro)
        end
    else el vehículo no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else falta la fecha o la descripción, o el punto no es una coordenada válida
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS

    Note over CHF,SIS: El chofer no indica el vehículo:<br/>el sistema usa el que tiene en uso
    CHF->>SIS: registrarSiniestro(vehiculoId, datos)
    activate SIS
    alt los datos son válidos
        SIS-->>CHF: siniestro denunciado
    else el chofer no tiene un vehículo en uso
        SIS-->>CHF: conflicto: sin vehículo en uso
    else falta la fecha o la descripción, o el punto no es una coordenada válida
        SIS-->>CHF: solicitud inválida, con el detalle del campo
    end
    deactivate SIS

    ADM->>SIS: modificarSiniestro(siniestroId, datos)
    activate SIS
    alt el siniestro existe y no está cerrado
        SIS-->>ADM: siniestro modificado, con su estado avanzado
    else el siniestro no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el estado pedido no sigue al actual o el siniestro está cerrado
        SIS-->>ADM: solicitud inválida: transición no permitida
    end
    deactivate SIS

    ADM->>SIS: consultarSiniestros(filtros)
    activate SIS
    SIS-->>ADM: siniestros que cumplen los filtros, con el total
    deactivate SIS
```

**Figura 114 — DSS CU-201: Registrar un Siniestro**

---

#### DSS — CU-202: Cerrar un Siniestro

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `cerrarSiniestro(siniestroId, costoDeReparacion, reintegroDelSeguro, franquicia)`

```mermaid
sequenceDiagram
    title DSS — CU-202 Cerrar un Siniestro
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: cerrarSiniestro(siniestroId, costoDeReparacion, reintegroDelSeguro, franquicia)
    activate SIS
    alt el siniestro existe y no está cerrado
        SIS-->>ADM: siniestro cerrado, con sus importes y la fecha de cierre
    else el siniestro no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el siniestro ya está cerrado o algún importe es negativo
        SIS-->>ADM: solicitud inválida, con el motivo
    end
    deactivate SIS
```

**Figura 115 — DSS CU-202: Cerrar un Siniestro**

---

#### DSS — CU-203: Consultar el Costo Total de un Vehículo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarCostoDeUnVehiculo(vehiculoId, fechaDesde, fechaHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-203 Consultar el Costo Total de un Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarCostoDeUnVehiculo(vehiculoId, fechaDesde, fechaHasta)
    activate SIS
    alt el vehículo existe y el rango es válido
        SIS-->>ADM: costo por rubro, kilómetros, costo por kilómetro y evolución mensual
    else el vehículo no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el rango de fechas no es válido
        SIS-->>ADM: solicitud inválida
    end
    deactivate SIS
```

**Figura 116 — DSS CU-203: Consultar el Costo Total de un Vehículo**

---

#### DSS — CU-204: Consultar el Tablero de Costos de la Flota

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarTableroDeCostosDeLaFlota(fechaDesde, fechaHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-204 Consultar el Tablero de Costos de la Flota
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarTableroDeCostosDeLaFlota(fechaDesde, fechaHasta)
    activate SIS
    alt el rango es válido
        SIS-->>ADM: un renglón por vehículo, ordenado por costo por kilómetro
    else el rango de fechas no es válido
        SIS-->>ADM: solicitud inválida
    end
    deactivate SIS
```

**Figura 117 — DSS CU-204: Consultar el Tablero de Costos de la Flota**

---

#### DSS — CU-205: Registrar un Neumático

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarNeumatico(datos)`

```mermaid
sequenceDiagram
    title DSS — CU-205 Registrar un Neumático
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarNeumatico(datos)
    activate SIS
    alt los datos son válidos y el número de serie está libre
        SIS-->>ADM: neumático registrado, en depósito
    else ya existe un neumático con ese número de serie
        SIS-->>ADM: conflicto: neumático ya registrado
    else falta un dato obligatorio
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS
```

**Figura 118 — DSS CU-205: Registrar un Neumático**

---

#### DSS — CU-206: Registrar un Movimiento de Neumático

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarMovimientoDeNeumatico(neumaticoId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-206 Registrar un Movimiento de Neumático
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarMovimientoDeNeumatico(neumaticoId, datos)
    activate SIS
    alt el movimiento es válido para el estado del neumático
        SIS-->>ADM: movimiento registrado, con el neumático en su nuevo estado
    else el neumático o el vehículo no existen en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el movimiento no corresponde al estado del neumático
        SIS-->>ADM: solicitud inválida: movimiento no permitido
    end
    deactivate SIS
```

**Figura 119 — DSS CU-206: Registrar un Movimiento de Neumático**

---

#### DSS — CU-247: Reactivar un Vehículo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `reactivarVehiculo(vehiculoId)`

```mermaid
sequenceDiagram
    title DSS — CU-247 Reactivar un Vehículo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: reactivarVehiculo(vehiculoId)
    activate SIS
    alt el vehículo está fuera de servicio y su documentación bloqueante está en regla
        SIS-->>ADM: vehículo activo
    else el vehículo no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el vehículo no está fuera de servicio
        SIS-->>ADM: solicitud inválida: el vehículo no está fuera de servicio
    else hay documentación bloqueante vencida
        SIS-->>ADM: solicitud inválida, con el documento vencido
    end
    deactivate SIS
```

**Figura 120 — DSS CU-247: Reactivar un Vehículo**

---

### SS-08 — Gestión de Productos e Inventario

#### DSS — CU-036: Crear Producto (Garrafa)

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearProducto(tipo, peso, precio, stockInicial, descripcion, promociones)`

```mermaid
sequenceDiagram
    title DSS — CU-036 Crear Producto (Garrafa)
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearProducto(tipo, peso, precio, stockInicial, descripcion, promociones)
    activate SIS
    alt datos válidos
        SIS-->>ADM: producto creado (productoId, activo)
    else datos inválidos
        SIS-->>ADM: error de validación
    end
    deactivate SIS
```

**Figura 121 — DSS CU-036: Crear Producto (Garrafa)**

---

#### DSS — CU-037: Actualizar Precio de Producto

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `actualizarProducto(productoId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-037 Actualizar Precio de Producto
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: actualizarProducto(productoId, datos)
    activate SIS
    alt el producto pertenece a la distribuidora
        SIS-->>ADM: producto actualizado (precio vigente para los pedidos nuevos)
    else el producto no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 122 — DSS CU-037: Actualizar Precio de Producto**

> **Observación de análisis:** no existe una operación exclusiva de precio; el precio se modifica con la actualización general del producto.

---

#### DSS — CU-038: Actualizar Stock de Producto

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `actualizarStock(productoId, variacion)`

```mermaid
sequenceDiagram
    title DSS — CU-038 Actualizar Stock de Producto
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: actualizarStock(productoId, variacion)
    activate SIS
    alt el stock resultante es mayor o igual a cero
        SIS-->>ADM: stock actualizado (nuevo stock disponible)
    else el stock resultante sería negativo
        SIS-->>ADM: error de solicitud (stock insuficiente)
    else el producto no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 123 — DSS CU-038: Actualizar Stock de Producto**

> El parámetro es una **variación** (positiva o negativa), no un valor absoluto: ingresa mercadería con signo más y la ajusta con signo menos.

---

#### DSS — CU-039: Configurar Promociones por Cantidad

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `actualizarProducto(productoId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-039 Configurar Promociones por Cantidad
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: actualizarProducto(productoId, datos)
    activate SIS
    alt la tabla de promociones es válida
        SIS-->>ADM: promociones vigentes (cantidad mínima y porcentaje de descuento)
    else la tabla de promociones es inválida
        SIS-->>ADM: error de validación
    end
    deactivate SIS
```

**Figura 124 — DSS CU-039: Configurar Promociones por Cantidad**

> Al armar un pedido, cuando varias promociones aplican a la misma cantidad, el sistema toma **la más conveniente para el cliente**.

---

#### DSS — CU-040: Desactivar un Producto

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `desactivarProducto(productoId)`

```mermaid
sequenceDiagram
    title DSS — CU-040 Desactivar un Producto
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: desactivarProducto(productoId)
    activate SIS
    alt el producto existe en la distribuidora
        SIS-->>ADM: producto desactivado (deja de aparecer en el catálogo)
    else el producto no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 125 — DSS CU-040: Desactivar un Producto**

---


#### DSS — CU-268: Reactivar un Producto

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `reactivarProducto(productoId)`

```mermaid
sequenceDiagram
    title DSS — CU-268 Reactivar un Producto
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: reactivarProducto(productoId)
    activate SIS
    alt el producto existe en la distribuidora
        SIS-->>ADM: producto reactivado (vuelve a aparecer en el catálogo)
    else el producto no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 126 — DSS CU-268: Reactivar un Producto**

> **Planificado (I-1):** el sistema todavía no realiza la reactivación; el diagrama es la colaboración propuesta.

---


#### DSS — CU-269: Consultar los Productos Inactivos

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarProductosInactivos()`

```mermaid
sequenceDiagram
    title DSS — CU-269 Consultar los Productos Inactivos
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarProductosInactivos()
    activate SIS
    SIS-->>ADM: productos dados de baja de la distribuidora
    deactivate SIS
```

**Figura 127 — DSS CU-269: Consultar los Productos Inactivos**

> **Planificado (I-1):** el listado de productos inactivos todavía no existe; el diagrama es la colaboración propuesta.

---

#### DSS — CU-041: Consultar Catálogo de Productos

**Actor:** Cliente (ACT-01), Administrador (ACT-03)
**Operaciones del sistema:** `consultarCatalogo(pagina, limite, distribuidora)`, `consultarProductosDisponibles(distribuidora)`, `consultarProducto(productoId)`

```mermaid
sequenceDiagram
    title DSS — CU-041 Consultar Catálogo de Productos
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarCatalogo(pagina, limite, distribuidora)
    activate SIS
    SIS-->>CLI: productos activos (tipo, peso, precio, stock, promociones)
    deactivate SIS

    opt vista de compra rápida
        CLI->>SIS: consultarProductosDisponibles(distribuidora)
        activate SIS
        SIS-->>CLI: productos activos con stock disponible
        deactivate SIS
    end

    opt detalle de un producto
        CLI->>SIS: consultarProducto(productoId)
        activate SIS
        alt el producto existe
            SIS-->>CLI: detalle del producto
        else el producto no existe
            SIS-->>CLI: recurso no encontrado
        end
        deactivate SIS
    end
```

**Figura 128 — DSS CU-041: Consultar Catálogo de Productos**

---

### SS-09 — Franjas Horarias

#### DSS — CU-042: Crear Franja Horaria

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearFranjaHoraria(nombre, horaInicio, horaFin, capacidad)`

```mermaid
sequenceDiagram
    title DSS — CU-042 Crear Franja Horaria
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearFranjaHoraria(nombre, horaInicio, horaFin, capacidad)
    activate SIS
    alt el formato horario y la capacidad son válidos
        SIS-->>ADM: franja creada (franjaId, activa)
    else el formato horario es inválido
        SIS-->>ADM: error de validación
    end
    deactivate SIS
```

**Figura 129 — DSS CU-042: Crear Franja Horaria**

---

#### DSS — CU-044: Seleccionar Franja Horaria al Crear Pedido

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `consultarDisponibilidadDeFranjas(fecha, distribuidora)`, `crearPedido(items, direccionId, franjaId, fechaAgendada, metodoDePago)`

```mermaid
sequenceDiagram
    title DSS — CU-044 Seleccionar Franja Horaria al Crear Pedido
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarDisponibilidadDeFranjas(fecha, distribuidora)
    activate SIS
    SIS-->>CLI: franjas con capacidad, reservados y cupos libres
    deactivate SIS

    CLI->>SIS: crearPedido(items, direccionId, franjaId, fechaAgendada, metodoDePago)
    activate SIS
    alt la franja está activa y tiene cupo para esa fecha
        SIS-->>CLI: pedido creado con la franja reservada (numero, total, estado)
    else la franja ya está completa
        SIS-->>CLI: error de solicitud (la franja del día está completa)
    else la fecha agendada es anterior a hoy
        SIS-->>CLI: error de solicitud (no se puede agendar en una fecha pasada)
    else la franja no existe o está inactiva
        SIS-->>CLI: error de solicitud (franja inválida o inactiva)
    end
    deactivate SIS
```

**Figura 130 — DSS CU-044: Seleccionar Franja Horaria al Crear Pedido**

> El cupo se toma dentro de la misma transacción que crea el pedido, de modo que dos clientes que eligen la última plaza de la misma franja no la obtienen los dos.

---

#### DSS — CU-045: Consultar Franjas Horarias Disponibles

**Actor:** Cliente (ACT-01)
**Operaciones del sistema:** `consultarDisponibilidadDeFranjas(fecha, distribuidora)`, `listarFranjas(distribuidora)`

```mermaid
sequenceDiagram
    title DSS — CU-045 Consultar Franjas Horarias Disponibles
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarDisponibilidadDeFranjas(fecha, distribuidora)
    activate SIS
    alt la fecha es válida
        SIS-->>CLI: por cada franja activa (nombre, horario, capacidad, reservados, cupos libres)
    else la fecha es inválida
        SIS-->>CLI: error de validación
    end
    deactivate SIS

    opt vista administrativa
        CLI->>SIS: listarFranjas(distribuidora)
        activate SIS
        SIS-->>CLI: franjas activas de la distribuidora
        deactivate SIS
    end
```

**Figura 131 — DSS CU-045: Consultar Franjas Horarias Disponibles**

---

#### DSS — CU-103: Eliminar Franja Horaria

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `eliminarFranjaHoraria(franjaId)`

```mermaid
sequenceDiagram
    title DSS — CU-103 Eliminar Franja Horaria
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: eliminarFranjaHoraria(franjaId)
    activate SIS
    alt la franja pertenece a la distribuidora
        SIS-->>ADM: franja desactivada (deja de ofrecerse para agendar)
    else la franja no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 132 — DSS CU-103: Eliminar Franja Horaria**

> **Asimetría:** el sistema permite dar de baja una franja pero **no** modificar su capacidad (CU-043, no implementado). Para cambiar la capacidad hay que eliminar y volver a crear.

---

#### DSS — CU-154: Consultar Listado de Franjas Horarias

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarFranjasHorarias()`

```mermaid
sequenceDiagram
    title DSS — CU-154 Consultar Listado de Franjas Horarias
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarFranjasHorarias()
    activate SIS
    SIS-->>ADM: listado de franjas de la distribuidora
    deactivate SIS
```

**Figura 133 — DSS CU-154: Consultar Listado de Franjas Horarias**

---

### SS-10 — Multi-Distribuidora (Multi-Tenancy)

#### DSS — CU-052: Registrar Distribuidora

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `registrarDistribuidora(nombre, identificadorCorto, razonSocial, cuit, correo, telefono, logo, plan)`

```mermaid
sequenceDiagram
    title DSS — CU-052 Registrar Distribuidora
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: registrarDistribuidora(nombre, identificadorCorto, razonSocial, cuit, correo, telefono, logo, plan)
    activate SIS
    alt el identificador corto está libre
        SIS-->>SUP: distribuidora creada (distribuidoraId, estado inicial)
    else el identificador corto ya está en uso
        SIS-->>SUP: conflicto (identificador duplicado)
    else datos inválidos
        SIS-->>SUP: error de validación
    end
    deactivate SIS
```

**Figura 134 — DSS CU-052: Registrar Distribuidora**

> Solo el Super Administrador opera este caso de uso: es una acción de **plataforma**, no de una empresa.

---

#### DSS — CU-053: Consultar Distribuidoras

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `listarDistribuidoras()`, `consultarDistribuidora(distribuidoraId)`

```mermaid
sequenceDiagram
    title DSS — CU-053 Consultar Distribuidoras
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: listarDistribuidoras()
    activate SIS
    SIS-->>SUP: listado de distribuidoras (nombre, identificador, estado, plan)
    deactivate SIS

    opt ficha de una distribuidora
        SUP->>SIS: consultarDistribuidora(distribuidoraId)
        activate SIS
        alt la distribuidora existe
            SIS-->>SUP: datos de la distribuidora
        else la distribuidora no existe
            SIS-->>SUP: recurso no encontrado
        end
        deactivate SIS
    end
```

**Figura 135 — DSS CU-053: Consultar Distribuidoras**

---

#### DSS — CU-054: Modificar Datos de la Distribuidora

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `modificarDistribuidora(distribuidoraId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-054 Modificar Datos de la Distribuidora
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: modificarDistribuidora(distribuidoraId, datos)
    activate SIS
    alt la distribuidora existe
        SIS-->>SUP: distribuidora actualizada
    else la distribuidora no existe
        SIS-->>SUP: recurso no encontrado
    end
    deactivate SIS
```

**Figura 136 — DSS CU-054: Modificar Datos de la Distribuidora**

---

#### DSS — CU-055: Dar de Baja una Distribuidora

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `darDeBajaDistribuidora(distribuidoraId)`

```mermaid
sequenceDiagram
    title DSS — CU-055 Dar de Baja una Distribuidora
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: darDeBajaDistribuidora(distribuidoraId)
    activate SIS
    alt la distribuidora existe
        SIS-->>SUP: distribuidora dada de baja (baja lógica, se conserva su histórico)
    else la distribuidora no existe
        SIS-->>SUP: recurso no encontrado
    end
    deactivate SIS
```

**Figura 137 — DSS CU-055: Dar de Baja una Distribuidora**

---

### SS-11 — Cobertura Geográfica

#### DSS — CU-056: Definir Zona de Cobertura

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `definirZonaDeCobertura(nombre, poligono, recargo, activa)`

```mermaid
sequenceDiagram
    title DSS — CU-056 Definir Zona de Cobertura
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: definirZonaDeCobertura(nombre, poligono, recargo, activa)
    activate SIS
    alt el polígono y el recargo son válidos
        SIS-->>ADM: zona creada (zonaId, recargo asociado)
    else el polígono es inválido
        SIS-->>ADM: error de validación
    end
    deactivate SIS
```

**Figura 138 — DSS CU-056: Definir Zona de Cobertura**

---

#### DSS — CU-057: Consultar Zonas de Cobertura

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `listarZonasDeCobertura()`

```mermaid
sequenceDiagram
    title DSS — CU-057 Consultar Zonas de Cobertura
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarZonasDeCobertura()
    activate SIS
    SIS-->>ADM: zonas de la distribuidora (nombre, polígono, recargo, estado)
    deactivate SIS
```

**Figura 139 — DSS CU-057: Consultar Zonas de Cobertura**

---

#### DSS — CU-058: Validar Cobertura de una Dirección

**Actor:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `validarCobertura(latitud, longitud)`

```mermaid
sequenceDiagram
    title DSS — CU-058 Validar Cobertura de una Dirección
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: validarCobertura(latitud, longitud)
    activate SIS
    alt el punto cae dentro de una zona activa y no dada de baja
        SIS-->>CLI: cubierta (zonaId, nombre de la zona, recargo aplicable)
    else la distribuidora no tiene zonas activas y vigentes
        SIS-->>CLI: cubierta sin recargo (cobertura irrestricta por omisión)
    else el punto está fuera de toda zona
        SIS-->>CLI: fuera de cobertura
    end
    deactivate SIS
```

**Figura 140 — DSS CU-058: Validar Cobertura de una Dirección**

> Es la **precondición** de CU-005: la aplicación la invoca antes de dejar confirmar el pedido, y de acá sale el recargo por zona que se suma al total.

---

#### DSS — CU-059: Eliminar Zona de Cobertura

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `eliminarZonaDeCobertura(zonaId)`

```mermaid
sequenceDiagram
    title DSS — CU-059 Eliminar Zona de Cobertura
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: eliminarZonaDeCobertura(zonaId)
    activate SIS
    alt la zona pertenece a la distribuidora
        SIS-->>ADM: zona dada de baja (baja lógica, deja de contar para la cobertura)
    else la zona no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 141 — DSS CU-059: Eliminar Zona de Cobertura**

---

#### DSS — CU-150: Programar la Vigencia de una Zona de Cobertura

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `programarVigenciaDeZona(zonaId, vigenteHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-150 Programar la Vigencia de una Zona de Cobertura
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: programarVigenciaDeZona(zonaId, vigenteHasta)
    activate SIS
    alt la zona no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else se indica una fecha ya pasada
        SIS-->>ADM: error de validación, la fecha debe ser futura
    else se indica una fecha futura
        SIS-->>ADM: vigencia programada (zonaId, vigenteHasta)
    else se indica una fecha vacía
        SIS-->>ADM: vigencia quitada, la zona rige sin vencimiento
    end
    deactivate SIS
```

**Figura 142 — DSS CU-150: Programar la Vigencia de una Zona de Cobertura**

---

#### DSS — CU-151: Desactivar las Zonas de Cobertura Vencidas

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `desactivarZonasVencidas()`

```mermaid
sequenceDiagram
    title DSS — CU-151 Desactivar las Zonas de Cobertura Vencidas
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    Note over SAU: Proceso temporal
    SAU->>SIS: desactivarZonasVencidas()
    activate SIS
    alt Otra instancia ya está ejecutando el barrido
        SIS-->>SAU: ejecución salteada
    else Hay zonas activas con vigencia vencida
        Note over SAU,SIS: Marca cada zona como inactiva
        SIS-->>SAU: zonas desactivadas (cantidad, identificadores)
    else No hay zonas vencidas
        SIS-->>SAU: sin cambios
    end
    deactivate SIS
```

**Figura 143 — DSS CU-151: Desactivar las Zonas de Cobertura Vencidas**

---


### SS-12 — Incidencias y Calidad de Servicio

#### DSS — CU-060: Registrar Incidencia de Entrega

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `registrarIncidencia(pedidoId, tipo, descripcion, foto)`

```mermaid
sequenceDiagram
    title DSS — CU-060 Registrar Incidencia de Entrega
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: registrarIncidencia(pedidoId, tipo, descripcion, foto)
    activate SIS
    alt el pedido existe
        SIS-->>CHO: incidencia registrada (incidenciaId, estado ABIERTA)
    else el pedido no existe o es de otra distribuidora
        SIS-->>CHO: recurso no encontrado
    else el pedido no está asignado al chofer
        SIS-->>CHO: acceso denegado
    end
    deactivate SIS
```

**Figura 144 — DSS CU-060: Registrar Incidencia de Entrega**

> Circuito **distinto** al de reclamos (SS-05): el reclamo lo abre el cliente después de la entrega, la incidencia la abre el chofer durante el reparto.

---

#### DSS — CU-061: Listar Incidencias

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `listarIncidencias()`

```mermaid
sequenceDiagram
    title DSS — CU-061 Listar Incidencias
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarIncidencias()
    activate SIS
    SIS-->>ADM: incidencias de su distribuidora (pedido, tipo, estado, chofer que la reportó)
    deactivate SIS
```

**Figura 145 — DSS CU-061: Listar Incidencias**

---

#### DSS — CU-062: Consultar Incidencias de un Pedido

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarIncidenciasDelPedido(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-062 Consultar Incidencias de un Pedido
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: consultarIncidenciasDelPedido(pedidoId)
    activate SIS
    alt el pedido existe y es de la distribuidora
        SIS-->>CHO: incidencias del pedido (tipo, descripción, estado, resolución)
    else el pedido no existe o es de otra distribuidora
        SIS-->>CHO: recurso no encontrado, sin revelar que existe
    end
    deactivate SIS
```

**Figura 146 — DSS CU-062: Consultar Incidencias de un Pedido**

---

#### DSS — CU-063: Resolver Incidencia

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `resolverIncidencia(incidenciaId, notaDeResolucion)`

```mermaid
sequenceDiagram
    title DSS — CU-063 Resolver Incidencia
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: resolverIncidencia(incidenciaId, notaDeResolucion)
    activate SIS
    alt la incidencia existe en la distribuidora
        SIS-->>ADM: incidencia resuelta (estado y nota registrados)
    else la incidencia no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 147 — DSS CU-063: Resolver Incidencia**

---

#### DSS — CU-064: Calificar Pedido (cliente↔chofer)

**Actor:** Cliente (ACT-01), Chofer (ACT-02)
**Operaciones del sistema:** `calificarPedido(pedidoId, estrellas, comentario)`

```mermaid
sequenceDiagram
    title DSS — CU-064 Calificar Pedido (cliente↔chofer)
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: calificarPedido(pedidoId, estrellas, comentario)
    activate SIS
    alt el pedido está entregado y el emisor participó de él
        SIS-->>CLI: calificación registrada (se recalcula el promedio del calificado)
    else el emisor ya calificó ese pedido
        SIS-->>CLI: conflicto (ya calificaste este pedido)
    else el pedido no está entregado o no tiene chofer
        SIS-->>CLI: error de solicitud (solo se califican pedidos entregados)
    else el pedido es de otro cliente o lo entregó otro chofer
        SIS-->>CLI: acceso denegado
    end
    deactivate SIS
```

**Figura 148 — DSS CU-064: Calificar Pedido (cliente↔chofer)**

> La calificación es **bidireccional**: el mismo mensaje lo emite el cliente hacia el chofer o el chofer hacia el cliente. El emisor sale de la sesión y el calificado se deriva del pedido, de modo que hay a lo sumo una calificación por pedido y por lado.

---

#### DSS — CU-065: Consultar Promedio de Calificaciones de un Usuario

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarResumenDeCalificaciones(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-065 Consultar Promedio de Calificaciones de un Usuario
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarResumenDeCalificaciones(usuarioId)
    activate SIS
    SIS-->>CLI: promedio de estrellas y cantidad de calificaciones recibidas
    deactivate SIS
```

**Figura 149 — DSS CU-065: Consultar Promedio de Calificaciones de un Usuario**

---

#### DSS — CU-066: Consultar Historial de Calificaciones Recibidas

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarHistorialDeCalificaciones(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-066 Consultar Historial de Calificaciones Recibidas
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarHistorialDeCalificaciones(usuarioId)
    activate SIS
    SIS-->>ADM: calificaciones recibidas (pedido, estrellas, comentario, fecha)
    deactivate SIS
```

**Figura 150 — DSS CU-066: Consultar Historial de Calificaciones Recibidas**

---

### SS-13 — Trazabilidad de Envases

#### DSS — CU-067: Dar de Alta un Envase Físico

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `darDeAltaEnvase(numeroDeSerie, tipoDeProducto, deposito)`

```mermaid
sequenceDiagram
    title DSS — CU-067 Dar de Alta un Envase Físico
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: darDeAltaEnvase(numeroDeSerie, tipoDeProducto, deposito)
    activate SIS
    alt el número de serie está libre en la distribuidora
        SIS-->>ADM: envase creado (envaseId, estado EN_DEPOSITO)
    else el número de serie ya existe en la distribuidora
        SIS-->>ADM: conflicto (serie duplicada)
    end
    deactivate SIS
```

**Figura 151 — DSS CU-067: Dar de Alta un Envase Físico**

> El número de serie es único **por distribuidora**, no globalmente: dos empresas pueden tener garrafas con la misma numeración de fábrica.

---

#### DSS — CU-068: Asignar Envases a un Pedido

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `asignarEnvasesAPedido(pedidoId, numerosDeSerie)`

```mermaid
sequenceDiagram
    title DSS — CU-068 Asignar Envases a un Pedido
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: asignarEnvasesAPedido(pedidoId, numerosDeSerie)
    activate SIS
    alt el pedido existe y todos los envases están llenos
        loop por cada número de serie recibido
            SIS-->>CHO: envase despachado (serie, estado DESPACHADO)
        end
        SIS-->>CHO: asignación completa (cantidad de envases despachados)
    else algún envase no está en estado LLENO
        SIS-->>CHO: error de solicitud (no se puede despachar un envase sin llenar)
    else el pedido o algún envase no existe
        SIS-->>CHO: recurso no encontrado
    end
    deactivate SIS
```

**Figura 152 — DSS CU-068: Asignar Envases a un Pedido**

---

#### DSS — CU-069: Consultar el Parque de Envases

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `listarEnvases(estado)`, `consultarEnvase(envaseId)`

```mermaid
sequenceDiagram
    title DSS — CU-069 Consultar el Parque de Envases
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarEnvases(estado)
    activate SIS
    SIS-->>ADM: envases de la distribuidora (serie, estado, pedido y cliente actuales)
    deactivate SIS

    opt ficha de un envase
        ADM->>SIS: consultarEnvase(envaseId)
        activate SIS
        alt el envase existe
            SIS-->>ADM: ficha del envase
        else el envase no existe
            SIS-->>ADM: recurso no encontrado
        end
        deactivate SIS
    end
```

**Figura 153 — DSS CU-069: Consultar el Parque de Envases**

---

#### DSS — CU-070: Registrar Movimiento de Envase (cambio de estado)

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `registrarMovimientoDeEnvase(envaseId, estadoDestino, pedidoId, observacion)`

```mermaid
sequenceDiagram
    title DSS — CU-070 Registrar Movimiento de Envase (cambio de estado)
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: registrarMovimientoDeEnvase(envaseId, estadoDestino, pedidoId, observacion)
    activate SIS
    alt la transición es válida desde el estado actual
        SIS-->>CHO: envase en el nuevo estado (movimiento asentado en su historial)
    else la transición no está permitida
        SIS-->>CHO: error de solicitud (transición inválida)
    else el envase no existe en la distribuidora
        SIS-->>CHO: recurso no encontrado
    end
    deactivate SIS
```

**Figura 154 — DSS CU-070: Registrar Movimiento de Envase (cambio de estado)**

> Ciclo de vida del envase: EN_DEPOSITO → LLENO → DESPACHADO → CON_EL_CLIENTE → VACIO_DEVUELTO. Al confirmarse la entrega del pedido (CU-020 / CU-079) el sistema avanza solo los envases despachados a CON_EL_CLIENTE.

---

#### DSS — CU-071: Consultar Historial de Movimientos de un Envase

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarHistorialDelEnvase(envaseId)`

```mermaid
sequenceDiagram
    title DSS — CU-071 Consultar Historial de Movimientos de un Envase
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarHistorialDelEnvase(envaseId)
    activate SIS
    SIS-->>ADM: movimientos en orden cronológico (estado origen, estado destino, pedido, responsable, fecha)
    deactivate SIS
```

**Figura 155 — DSS CU-071: Consultar Historial de Movimientos de un Envase**

> El historial es de **solo agregado**: los movimientos no se corrigen ni se borran, y por eso sirve como evidencia de trazabilidad.

---

#### DSS — CU-132: Registrar la Revisión Periódica de un Envase

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarRevisionDeEnvase(envaseId, fecha, resultado, vencimiento)`

```mermaid
sequenceDiagram
    title DSS — CU-132 Registrar la Revisión Periódica de un Envase
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarRevisionDeEnvase(envaseId, fecha, resultado, vencimiento)
    activate SIS
    alt los datos son válidos
        SIS-->>ADM: revisión registrada y envase actualizado
    else el resultado es de rechazo
        SIS-->>ADM: envase fuera de circulación
    else las fechas no son coherentes
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 156 — DSS CU-132: Registrar la Revisión Periódica de un Envase**

---

#### DSS — CU-133: Consultar la Vigencia de un Envase

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarVigenciaDelEnvase(envaseId)`

```mermaid
sequenceDiagram
    title DSS — CU-133 Consultar la Vigencia de un Envase
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarVigenciaDelEnvase(envaseId)
    activate SIS
    alt el envase tiene revisiones
        SIS-->>ADM: vigencia y historial
    else el envase no tiene revisiones
        SIS-->>ADM: vigencia no acreditada
    else el envase no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 157 — DSS CU-133: Consultar la Vigencia de un Envase**

---

#### DSS — CU-134: Consultar los Envases Próximos a Vencer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarEnvasesProximosAVencer(dias)`

```mermaid
sequenceDiagram
    title DSS — CU-134 Consultar los Envases Próximos a Vencer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarEnvasesProximosAVencer(dias)
    activate SIS
    alt hay envases en la ventana
        SIS-->>ADM: listado ordenado por vencimiento
    else no hay ninguno
        SIS-->>ADM: listado vacío
    end
    deactivate SIS
```

**Figura 158 — DSS CU-134: Consultar los Envases Próximos a Vencer**

---

#### DSS — CU-135: Bloquear el Despacho de un Envase Vencido

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `verificarVigenciaAlAsignar(pedidoId, series)`

```mermaid
sequenceDiagram
    title DSS — CU-135 Bloquear el Despacho de un Envase Vencido
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor ADM as Administrador (ACT-03)

    SAU->>SIS: verificarVigenciaAlAsignar(pedidoId, series)
    activate SIS
    alt Todos los envases están vigentes o sin fecha cargada
        SIS-->>SAU: asignación admitida (todos los envases están vigentes)
    else Alguno tiene la revisión vencida
        SIS-->>SAU: asignación rechazada con la lista de series vencidas
        SIS-)ADM: notificarEnvaseVencido(series)
    else El pedido o algún envase no existe
        SIS-->>SAU: recurso no encontrado
    end
    deactivate SIS
```

**Figura 159 — DSS CU-135: Bloquear el Despacho de un Envase Vencido**

---

### SS-14 — Pagos y Conciliación

#### DSS — CU-048: Procesar Pago con MercadoPago

**Actor:** MercadoPago (ACT-06)
**Operaciones del sistema:** `notificarResultadoDePago(tipoDeNotificacion, identificadorDelPago, firma)`

```mermaid
sequenceDiagram
    title DSS — CU-048 Procesar Pago con MercadoPago
    autonumber
    actor MP as MercadoPago (ACT-06)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)
    actor CHO as Chofer (ACT-02)

    Note over MP,SIS: El enlace de pago ya lo generó la creación del pedido o de la reserva,<br/>y el cliente paga en el sitio de la pasarela, fuera del límite del sistema

    MP->>SIS: notificarResultadoDePago(tipoDeNotificacion, identificadorDelPago, firma)
    activate SIS
    alt La firma no es válida
        SIS-->>MP: notificación recibida (se descarta sin procesar)
    else Pago aprobado de un pedido pendiente
        SIS-->>MP: notificación recibida
        SIS-)CLI: notificarPagoAcreditado(pedido)
        SIS-)CHO: notificarOferta(pedido)
    else Pago aprobado de la seña de una reserva
        SIS-->>MP: notificación recibida (la seña queda paga, la reserva no se despacha)
        SIS-)CLI: notificarPagoAcreditado(pedido)
    else Pago aprobado de un pedido ya cancelado o entregado
        SIS-->>MP: notificación recibida (se registra el pago, sin reactivar el pedido)
    else Pago rechazado o cancelado
        SIS-->>MP: notificación recibida (el pedido queda a la espera y el Cliente no recibe aviso)
    end
    deactivate SIS
```

**Figura 160 — DSS CU-048: Procesar Pago con MercadoPago**

> El sistema responde **siempre** con acuse de recibo, incluso ante una firma inválida, para no revelar si el pedido existe y para que la pasarela no reintente en bucle. El resultado del pago se asienta en un registro contable propio, independiente del estado del pedido. El aviso al Cliente (evento `order:payment-approved` y notificación push) sale sólo en la primera confirmación del pago aprobado, no en los reintentos de la pasarela. El enlace de pago no lo pide el Cliente en un mensaje aparte: lo genera la propia creación del pedido (`crearPedido`, CU-005) o de la reserva (`crearReserva`, CU-072) y viaja en su respuesta. Esa colaboración interna se diagrama en el Documento 3, con el nombre `crearCheckoutDePago`.

---

#### DSS — CU-168: Reintegrar el Pago de un Pedido

**Actor:** Administrador (ACT-03), Sistema Automático (ACT-04)
**Operaciones del sistema:** `reintegrarPagoDelPedido(pedidoId, importe)`

```mermaid
sequenceDiagram
    title DSS — CU-168 Reintegrar el Pago de un Pedido
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor ADM as Administrador (ACT-03)

    Note over SAU: Se dispara al cancelarse<br/>el pedido (CU-008,<br/>CU-010) o al degradarse<br/>un pedido express<br/>(CU-149)
    SAU->>SIS: reintegrarPagoDelPedido(pedidoId, importe)
    activate SIS
    alt Hay un pago aprobado por una pasarela
        alt La pasarela acepta la devolución
            SIS-->>SAU: pago reintegrado
        else La pasarela rechaza o no responde
            SIS-->>SAU: devolución fallida, avisada al panel
        end
    else No hay pago aprobado por una pasarela
        SIS-->>SAU: sin devolución
    end
    deactivate SIS

    opt El administrador reintenta una devolución fallida desde el detalle del pedido
        ADM->>SIS: reintegrarPagoDelPedido(pedidoId, importe)
        activate SIS
        SIS-->>ADM: pago reintegrado o devolución fallida, según responda la pasarela
        deactivate SIS
    end
```

**Figura 161 — DSS CU-168: Reintegrar el Pago de un Pedido**

---

### SS-15 — Reservas Programadas

#### DSS — CU-072: Crear Reserva Programada con Seña

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `crearReserva(items, direccionId, fechaAgendada, franjaId, metodoDePago, montoDeLaSenia)`

```mermaid
sequenceDiagram
    title DSS — CU-072 Crear Reserva Programada con Seña
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: crearReserva(items, direccionId, fechaAgendada, franjaId, metodoDePago, montoDeLaSenia)
    activate SIS
    alt hay stock y la franja tiene cupo para esa fecha
        SIS-->>CLI: reserva creada (numero, total, seña, estado RESERVADO)
        opt la seña se paga con la pasarela
            SIS-->>CLI: enlace de pago de la seña
        end
    else no hay stock suficiente
        SIS-->>CLI: error de solicitud (stock insuficiente)
    else la franja está completa o la fecha es pasada
        SIS-->>CLI: error de solicitud (no se puede agendar en esa franja)
    end
    deactivate SIS
```

**Figura 162 — DSS CU-072: Crear Reserva Programada con Seña**

> La reserva nace en estado **RESERVADO**: reserva stock y cupo desde el momento del alta, pero no se despacha hasta el día agendado (CU-075).

---

#### DSS — CU-073: Listar Reservas y Estado de la Seña

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `listarReservas()`

```mermaid
sequenceDiagram
    title DSS — CU-073 Listar Reservas y Estado de la Seña
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarReservas()
    activate SIS
    SIS-->>ADM: reservas ordenadas por fecha agendada (cliente, total, seña, si está paga, saldo)
    deactivate SIS
```

**Figura 163 — DSS CU-073: Listar Reservas y Estado de la Seña**

---

#### DSS — CU-074: Confirmar Seña Cobrada en Efectivo

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `confirmarSenia(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-074 Confirmar Seña Cobrada en Efectivo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: confirmarSenia(pedidoId)
    activate SIS
    alt el pedido es una reserva pendiente
        SIS-->>ADM: seña confirmada (la reserva queda lista para activarse sola)
    else el pedido no es una reserva pendiente
        SIS-->>ADM: error de solicitud (el pedido no es una reserva pendiente)
    else la reserva no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 164 — DSS CU-074: Confirmar Seña Cobrada en Efectivo**

> Es la **única acción humana** del ciclo de reservas: la seña pagada por la pasarela se confirma sola (CU-048).

---

#### DSS — CU-075: Activar Reservas Vencidas Automaticamente (Cron)

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `activarReservasDelDia()`

```mermaid
sequenceDiagram
    title DSS — CU-075 Activar Reservas Vencidas Automaticamente (Cron)
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor CHO as Chofer (ACT-02)

    Note over SAU: Proceso periódico.<br/>Frecuencia real cada 5<br/>minutos
    SAU->>SIS: activarReservasDelDia()
    activate SIS
    alt Hay reservas con la seña paga y el día cumplido
        loop Por cada reserva vencida (hasta 50 por corrida)
            SIS-)CHO: notificarOferta(pedido)
        end
        SIS-->>SAU: reservas activadas y enviadas a despacho
    else No hay reservas para activar
        SIS-->>SAU: sin trabajo por hacer
    end
    deactivate SIS
```

**Figura 165 — DSS CU-075: Activar Reservas Vencidas Automaticamente (Cron)**

> Solo se activan las reservas con la seña **efectivamente paga**. Una reserva cuya activación falla se registra y se reintenta en la corrida siguiente.

---

#### DSS — CU-076: Expirar Reservas sin Seña Pagada (Cron)

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `expirarReservasSinSenia()`

```mermaid
sequenceDiagram
    title DSS — CU-076 Expirar Reservas sin Seña Pagada (Cron)
    autonumber
    actor AUT as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    Note over AUT: Proceso periódico.<br/>Frecuencia real cada 1<br/>hora
    AUT->>SIS: expirarReservasSinSenia()
    activate SIS
    alt hay reservas sin seña más viejas que el plazo configurado
        loop por cada reserva vencida (hasta 50 por corrida)
            SIS-->>AUT: reserva cancelada y stock liberado
        end
    else no hay reservas vencidas
        SIS-->>AUT: sin trabajo por hacer
    end
    deactivate SIS
```

**Figura 166 — DSS CU-076: Expirar Reservas sin Seña Pagada (Cron)**

> El plazo de espera de la seña es un parámetro de configuración (valor por omisión, 48 horas). Cada expiración es atómica: si falla, la reserva queda intacta para la corrida siguiente.

---

#### DSS — CU-077: Expirar Pedidos de MercadoPago sin Pagar (Cron)

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `expirarPedidosSinPagar()`

```mermaid
sequenceDiagram
    title DSS — CU-077 Expirar Pedidos de MercadoPago sin Pagar (Cron)
    autonumber
    actor AUT as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    Note over AUT: Proceso periódico.<br/>Frecuencia real cada 30<br/>minutos
    AUT->>SIS: expirarPedidosSinPagar()
    activate SIS
    alt hay pedidos pendientes con pasarela más viejos que el plazo
        loop por cada pedido vencido (hasta 50 por corrida)
            alt el pago no llegó a acreditarse
                SIS-->>AUT: pedido cancelado por falta de pago y stock liberado
            else el pago se acreditó justo antes de la revisión
                SIS-->>AUT: pedido intacto (gana el pago, no la expiración)
            end
        end
    else no hay pedidos vencidos
        SIS-->>AUT: sin trabajo por hacer
    end
    deactivate SIS
```

**Figura 167 — DSS CU-077: Expirar Pedidos de MercadoPago sin Pagar (Cron)**

> Sin este proceso, el stock que se reserva al crear el pedido —antes de que el cliente pague— quedaría bloqueado para siempre si abandona el pago. El plazo por omisión es de 60 minutos.

---

### SS-16 — Administración de Cuentas y Roles

#### DSS — CU-086: Registrar Administrador

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `registrarAdministrador(nombreCompleto, correo, telefono, contrasena, rol, distribuidoraId)`

```mermaid
sequenceDiagram
    title DSS — CU-086 Registrar Administrador
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarAdministrador(nombreCompleto, correo, telefono, contrasena, rol, distribuidoraId)
    activate SIS
    alt es super administrador
        SIS-->>ADM: administrador creado en la distribuidora indicada, o super administrador sin distribuidora
    else es administrador de empresa y el alta es un admin de su propia distribuidora
        SIS-->>ADM: administrador creado en su distribuidora
    else intenta crear en otra distribuidora o con rol de super administrador
        SIS-->>ADM: acceso denegado
    else correo o teléfono ya registrados
        SIS-->>ADM: conflicto (el correo o el teléfono ya están en uso)
    end
    deactivate SIS
```

**Figura 168 — DSS CU-086: Registrar Administrador**

> Regla de negocio multi-empresa: un administrador de empresa **nunca** puede crear administradores de otra distribuidora ni escalar a super administrador.

---

#### DSS — CU-087: Crear el Primer Super Administrador (bootstrap)

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `crearPrimerSuperAdministrador(nombreCompleto, correo, telefono, contrasena)`

```mermaid
sequenceDiagram
    title DSS — CU-087 Crear el Primer Super Administrador (bootstrap)
    autonumber
    actor GEN as Administrador General (ACT-05)
    participant SIS as :Sistema

    GEN->>SIS: crearPrimerSuperAdministrador(nombreCompleto, correo, telefono, contrasena)
    activate SIS
    alt no existe ningún super administrador
        SIS-->>GEN: super administrador creado (queda habilitado el acceso al panel)
    else ya existe un super administrador
        SIS-->>GEN: rechazo (la operación de arranque ya fue usada)
    end
    deactivate SIS
    Note over GEN,SIS: Se ejecuta desde el servidor, no desde el<br/>panel ni las apps
```

**Figura 169 — DSS CU-087: Crear el Primer Super Administrador (bootstrap)**

> Es una operación de **una sola vez**: se autodeshabilita apenas existe el primer administrador.

---

#### DSS — CU-088: Consultar Administradores

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `listarAdministradores()`, `buscarAdministrador(termino)`

```mermaid
sequenceDiagram
    title DSS — CU-088 Consultar Administradores
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarAdministradores()
    activate SIS
    SIS-->>ADM: administradores de su distribuidora (nombre, correo, rol)
    deactivate SIS

    opt búsqueda puntual
        ADM->>SIS: buscarAdministrador(termino)
        activate SIS
        alt hay coincidencias
            SIS-->>ADM: administrador encontrado
        else no hay coincidencias, o el administrador es de otra distribuidora
            SIS-->>ADM: recurso no encontrado
        end
        deactivate SIS
    end
```

**Figura 170 — DSS CU-088: Consultar Administradores**

---

#### DSS — CU-089: Consultar los Roles

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `listarRoles()`

```mermaid
sequenceDiagram
    title DSS — CU-089 Consultar los Roles
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: listarRoles()
    activate SIS
    SIS-->>SUP: roles definidos en el sistema
    deactivate SIS
```

**Figura 171 — DSS CU-089: Consultar los Roles**

---


#### DSS — CU-252: Crear un Rol

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `crearRol(tipo)`

```mermaid
sequenceDiagram
    title DSS — CU-252 Crear un Rol
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: crearRol(tipo)
    activate SIS
    SIS-->>SUP: rol creado (rolId)
    deactivate SIS
```

**Figura 172 — DSS CU-252: Crear un Rol**

---


#### DSS — CU-253: Modificar un Rol

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `actualizarRol(rolId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-253 Modificar un Rol
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: actualizarRol(rolId, datos)
    activate SIS
    alt el rol existe y no es del sistema
        SIS-->>SUP: rol actualizado
    else el rol no existe
        SIS-->>SUP: recurso no encontrado
    else el rol es uno de los del sistema
        SIS-->>SUP: conflicto
    end
    deactivate SIS
```

**Figura 173 — DSS CU-253: Modificar un Rol**

---


#### DSS — CU-254: Eliminar un Rol

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `eliminarRol(rolId)`

```mermaid
sequenceDiagram
    title DSS — CU-254 Eliminar un Rol
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: eliminarRol(rolId)
    activate SIS
    alt el rol existe, no es del sistema y no tiene usuarios
        SIS-->>SUP: rol eliminado
    else el rol no existe
        SIS-->>SUP: recurso no encontrado
    else el rol es del sistema o tiene usuarios asignados
        SIS-->>SUP: conflicto
    end
    deactivate SIS
```

**Figura 174 — DSS CU-254: Eliminar un Rol**

---

#### DSS — CU-090: Sembrar los Roles Iniciales

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `sembrarRolesIniciales()`

```mermaid
sequenceDiagram
    title DSS — CU-090 Sembrar los Roles Iniciales
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: sembrarRolesIniciales()
    activate SIS
    SIS-->>SUP: roles base disponibles (cliente, chofer, administrador, super administrador)
    deactivate SIS
```

**Figura 175 — DSS CU-090: Sembrar los Roles Iniciales**

> Operación de puesta en marcha, idempotente: volver a ejecutarla no duplica los roles ya existentes.

---

#### DSS — CU-092: Consultar Listado de Clientes

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `listarClientes(pagina, limite)`

```mermaid
sequenceDiagram
    title DSS — CU-092 Consultar Listado de Clientes
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: listarClientes(pagina, limite)
    activate SIS
    SIS-->>ADM: página de clientes (nombre, contacto, validación, ubicación)
    deactivate SIS
```

**Figura 176 — DSS CU-092: Consultar Listado de Clientes**

---

#### DSS — CU-094: Actualizar Ubicación del Cliente

**Actor:** Cliente (ACT-01), Administrador (ACT-03)
**Operaciones del sistema:** `actualizarUbicacionDelCliente(clienteId, coordenadas)`

```mermaid
sequenceDiagram
    title DSS — CU-094 Actualizar Ubicación del Cliente
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: actualizarUbicacionDelCliente(clienteId, coordenadas)
    activate SIS
    alt las coordenadas no son un par latitud,longitud válido
        SIS-->>CLI: rechazo por coordenadas inválidas
    else el cliente existe
        SIS-->>CLI: ubicación actualizada, guardada como punto geográfico
    else el cliente no existe
        SIS-->>CLI: recurso no encontrado
    end
    deactivate SIS
```

**Figura 177 — DSS CU-094: Actualizar Ubicación del Cliente**

---

#### DSS — CU-095: Eliminar Cliente (baja lógica)

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `eliminarCliente(clienteId)`

```mermaid
sequenceDiagram
    title DSS — CU-095 Eliminar Cliente (baja lógica)
    autonumber
    actor ADM as Administrador General (ACT-05)
    participant SIS as :Sistema

    ADM->>SIS: eliminarCliente(clienteId)
    activate SIS
    alt el cliente existe
        SIS-->>ADM: cliente dado de baja (se conserva su histórico de pedidos)
    else el cliente no existe o nunca le compró a la distribuidora en contexto
        SIS-->>ADM: recurso no encontrado
    else quien pide es un administrador de empresa
        SIS-->>ADM: acceso denegado (la baja la hace el Administrador General)
    end
    deactivate SIS
```

**Figura 178 — DSS CU-095: Eliminar Cliente (baja lógica)**

---

#### DSS — CU-129: Consultar Detalle del Cliente

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarDetalleDelCliente(clienteId)`

```mermaid
sequenceDiagram
    title DSS — CU-129 Consultar Detalle del Cliente
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarDetalleDelCliente(clienteId)
    activate SIS
    alt el cliente existe
        SIS-->>ADM: ficha del cliente
    else el cliente no existe o nunca le compró a la distribuidora del administrador
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 179 — DSS CU-129: Consultar Detalle del Cliente**

---

#### DSS — CU-130: Buscar Cliente por Usuario

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `buscarClientePorUsuario(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-130 Buscar Cliente por Usuario
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: buscarClientePorUsuario(usuarioId)
    activate SIS
    alt la cuenta tiene ficha de cliente
        SIS-->>ADM: ficha del cliente
    else la cuenta no tiene ficha de cliente, o su cliente nunca le compró a la distribuidora del administrador
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 180 — DSS CU-130: Buscar Cliente por Usuario**

---

#### DSS — CU-131: Editar Datos del Cliente

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `editarDatosDelCliente(clienteId, cambios)`

```mermaid
sequenceDiagram
    title DSS — CU-131 Editar Datos del Cliente
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: editarDatosDelCliente(clienteId, cambios)
    activate SIS
    alt el cliente existe
        SIS-->>ADM: ficha actualizada
    else el cliente no existe o nunca le compró a la distribuidora del administrador
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 181 — DSS CU-131: Editar Datos del Cliente**

---

### SS-17 — Notificaciones y Mensajería

#### DSS — CU-098: Registrar el Token de Notificaciones del Dispositivo

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `registrarTokenDeNotificaciones(usuarioId, token, plataforma)`

```mermaid
sequenceDiagram
    title DSS — CU-098 Registrar el Token de Notificaciones del Dispositivo
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: registrarTokenDeNotificaciones(usuarioId, token, plataforma)
    activate SIS
    alt registra el token de su propio dispositivo o es administrador
        SIS-->>CLI: token registrado (el dispositivo empieza a recibir avisos)
    else intenta registrar un token a nombre de otro usuario
        SIS-->>CLI: acceso denegado
    end
    deactivate SIS
```

**Figura 182 — DSS CU-098: Registrar el Token de Notificaciones del Dispositivo**

> Es la **precondición técnica de CU-021**: sin token registrado no hay avisos al dispositivo.

---

#### DSS — CU-099: Consultar los Tokens de un Usuario

**Actor:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarTokensDelUsuario(usuarioId)`

```mermaid
sequenceDiagram
    title DSS — CU-099 Consultar los Tokens de un Usuario
    autonumber
    actor CLI as Cliente (ACT-01)
    participant SIS as :Sistema

    CLI->>SIS: consultarTokensDelUsuario(usuarioId)
    activate SIS
    alt consulta sus propios dispositivos o es el Administrador General
        SIS-->>CLI: dispositivos registrados (plataforma, fecha de alta)
    else consulta los dispositivos de otro usuario sin ser el Administrador General
        SIS-->>CLI: acceso denegado
    end
    deactivate SIS
    Note over CLI,SIS: También lo inician el Chofer (ACT-02) y el<br/>Administrador (ACT-03), sobre su propio<br/>usuario, y el Administrador General (ACT-05),<br/>sobre cualquiera
```

**Figura 183 — DSS CU-099: Consultar los Tokens de un Usuario**

---

#### DSS — CU-100: Enviar Notificación de Prueba

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `enviarNotificacionDePrueba(token, titulo, mensaje)`

```mermaid
sequenceDiagram
    title DSS — CU-100 Enviar Notificación de Prueba
    autonumber
    actor ADM as Administrador General (ACT-05)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    ADM->>SIS: enviarNotificacionDePrueba(token, titulo, mensaje)
    activate SIS
    alt el proveedor de mensajería acepta el envío al dispositivo del token
        SIS-)CLI: notificarPrueba(titulo, mensaje)
        SIS-->>ADM: notificación enviada
    else el proveedor rechaza el envío (token inválido)
        SIS-->>ADM: no se pudo enviar (resultado con el error del proveedor)
    else Quien pide no es el Administrador General
        SIS-->>ADM: acceso denegado
    end
    deactivate SIS
    Note over ADM,CLI: El dispositivo identificado por el token puede ser<br/>el de un Cliente (ACT-01) o el de un Chofer (ACT-02)
```

**Figura 184 — DSS CU-100: Enviar Notificación de Prueba**

---

#### DSS — CU-101: Reenviar Notificación de Confirmación de Pedido

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `reenviarConfirmacionDePedido(usuarioId, pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-101 Reenviar Notificación de Confirmación de Pedido
    autonumber
    actor ADM as Administrador General (ACT-05)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    ADM->>SIS: reenviarConfirmacionDePedido(usuarioId, pedidoId)
    activate SIS
    alt El cliente tiene dispositivos registrados
        SIS-)CLI: notificarConfirmacionDePedido(pedido)
        SIS-->>ADM: notificación reenviada
    else El cliente no tiene dispositivos registrados
        SIS-->>ADM: no se pudo enviar
    else Quien pide no es el Administrador General
        SIS-->>ADM: acceso denegado
    end
    deactivate SIS
```

**Figura 185 — DSS CU-101: Reenviar Notificación de Confirmación de Pedido**

> Se usa como acción de soporte cuando el cliente dice no haber recibido el aviso original.

---

#### DSS — CU-102: Probar el Servicio de Correo

**Actor:** Administrador General (ACT-05)
**Operaciones del sistema:** `probarServicioDeCorreo(destinatario)`

```mermaid
sequenceDiagram
    title DSS — CU-102 Probar el Servicio de Correo
    autonumber
    actor SUP as Administrador General (ACT-05)
    participant SIS as :Sistema

    SUP->>SIS: probarServicioDeCorreo(destinatario)
    activate SIS
    alt el servicio de correo responde
        SIS-->>SUP: correo de prueba enviado
    else el servicio de correo falla
        SIS-->>SUP: error del servicio de correo
    else Quien pide no es el Administrador General
        SIS-->>SUP: acceso denegado
    end
    deactivate SIS
```

**Figura 186 — DSS CU-102: Probar el Servicio de Correo**

> Es una herramienta de diagnóstico: exige sesión y es exclusiva del Administrador General, porque manda un correo real a la dirección que se le indica.

---

### SS-18 — Observabilidad y Operación

#### DSS — CU-104: Verificar la Salud del Sistema (liveness / readiness)

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `verificarVida()`, `verificarDisponibilidad()`, `verificarSalud()`

```mermaid
sequenceDiagram
    title DSS — CU-104 Verificar la Salud del Sistema (liveness / readiness)
    autonumber
    actor PLA as Plataforma de despliegue (ACT-09)
    participant SIS as :Sistema

    Note over PLA: Sondeo periódico de la<br/>plataforma de despliegue<br/>durante toda la vida de<br/>la instancia

    PLA->>SIS: verificarVida()
    activate SIS
    SIS-->>PLA: la instancia está viva
    deactivate SIS

    PLA->>SIS: verificarDisponibilidad()
    activate SIS
    alt Las dependencias responden
        SIS-->>PLA: lista para recibir tráfico
    else Alguna dependencia no responde
        SIS-->>PLA: no disponible (se le retira el tráfico a la instancia)
    end
    deactivate SIS

    opt Diagnóstico ampliado
        PLA->>SIS: verificarSalud()
        activate SIS
        SIS-->>PLA: estado de cada verificación (base de datos, memoria caché, memoria en uso, espacio en disco)
        deactivate SIS
    end
```

**Figura 187 — DSS CU-104: Verificar la Salud del Sistema (liveness / readiness)**

> Es el caso de uso que da soporte a los requisitos no funcionales de **disponibilidad** y **escalabilidad**, sin ningún caso de uso asociado en la matriz de rastreabilidad.

---

#### DSS — CU-152: Consultar el Registro de Auditoría

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `consultarAuditoria(autor, tipoDeRecurso, recurso, desde, hasta, resultado, limite, desplazamiento)`, `consultarAuditoriaDeDatos(entidad, registro, autor, tipoDeAccion, desde, hasta, pagina, limite)`

```mermaid
sequenceDiagram
    title DSS — CU-152 Consultar el Registro de Auditoría
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarAuditoria(autor, tipoDeRecurso, recurso, desde, hasta, resultado, limite, desplazamiento)
    activate SIS
    alt el solicitante no es administrador
        SIS-->>ADM: acceso denegado
    else algún filtro no tiene el formato esperado
        SIS-->>ADM: error de validación
    else filtros válidos
        Note over ADM,SIS: con una distribuidora en contexto, sólo los<br/>asientos de ella
        SIS-->>ADM: asientos del más reciente al más antiguo (autor, rol, operación, recurso, fecha, origen, resultado, cuerpo depurado) y total, o lista vacía si ninguno coincide
    end
    deactivate SIS

    ADM->>SIS: consultarAuditoriaDeDatos(entidad, registro, autor, tipoDeAccion, desde, hasta, pagina, limite)
    activate SIS
    alt el solicitante no es administrador
        SIS-->>ADM: acceso denegado
    else algún filtro no tiene el formato esperado
        SIS-->>ADM: error de validación
    else filtros válidos
        Note over ADM,SIS: con una distribuidora en contexto, sólo las<br/>auditorías de ella
        SIS-->>ADM: auditorías de la más reciente a la más antigua (acción, usuario, entidad, registro, fecha y hora, dirección IP, detalle de cada campo con su valor anterior y nuevo) y total, o lista vacía si ninguna coincide
    end
    deactivate SIS
```

**Figura 188 — DSS CU-152: Consultar el Registro de Auditoría**

---

#### DSS — CU-153: Registrar Toda Operación de Escritura

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `registrarOperacion(autor, rol, distribuidoraId, operacion, recurso, origen, resultado, codigo, motivo)`, `registrarAuditoriaDeDato(autor, ip, distribuidoraId, entidad, registro, tipoDeAccion, detalles)`

```mermaid
sequenceDiagram
    title DSS — CU-153 Registrar Toda Operación de Escritura
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    Note over SAU: Se dispara tras cada<br/>operación de escritura<br/>que pasó la<br/>autenticación y la<br/>autorización
    SAU->>SIS: registrarOperacion(autor, rol, distribuidoraId, operacion, recurso, origen, resultado, codigo, motivo)
    activate SIS
    Note over SAU,SIS: Depura las credenciales del cuerpo antes de<br/>guardar el asiento
    alt El asiento se guarda
        SIS-->>SAU: operación registrada
    else La base no acepta el asiento
        SIS-->>SAU: asiento volcado al registro de eventos,<br/>la operación original no se interrumpe
    end
    deactivate SIS

    Note over SAU: Se dispara cuando un registro<br/>de negocio se da de alta, se modifica,<br/>se da de baja o se reactiva
    SAU->>SIS: registrarAuditoriaDeDato(autor, ip, distribuidoraId, entidad, registro, tipoDeAccion, detalles)
    activate SIS
    Note over SAU,SIS: Escribe en la transacción del cambio, con un<br/>detalle por campo que cambió
    alt Cambió al menos un campo
        SIS-->>SAU: auditoría registrada
    else El guardado no cambió ningún campo
        SIS-->>SAU: nada que registrar
    end
    deactivate SIS
```

**Figura 189 — DSS CU-153: Registrar Toda Operación de Escritura**

---


#### DSS — CU-172: Configurar los Parámetros de un Proceso Automático

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `configurarParametrosDeProceso(proceso, parametros)`

```mermaid
sequenceDiagram
    title DSS — CU-172 Configurar los Parámetros de un Proceso Automático
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: configurarParametrosDeProceso(proceso, parametros)
    activate SIS
    alt el proceso es configurable y los parámetros son válidos
        SIS-->>ADM: parámetros del proceso guardados
    else el proceso no es configurable
        SIS-->>ADM: recurso no encontrado
    else los parámetros son inválidos
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS
```

**Figura 190 — DSS CU-172: Configurar los Parámetros de un Proceso Automático**

---

#### DSS — CU-173: Configurar la Frecuencia de las Tareas Programadas

**Actor:** Administrador (ACT-03), Administrador General (ACT-05)
**Operaciones del sistema:** `configurarFrecuenciaDeTareas(intervalos)`

```mermaid
sequenceDiagram
    title DSS — CU-173 Configurar la Frecuencia de las Tareas Programadas
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: configurarFrecuenciaDeTareas(intervalos)
    activate SIS
    alt los intervalos son válidos
        SIS-->>ADM: frecuencia de las tareas guardada
    else un intervalo es inválido
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS
```

**Figura 191 — DSS CU-173: Configurar la Frecuencia de las Tareas Programadas**

---

### SS-19 — Personal y Legajos

#### DSS — CU-176: Consultar los Puestos de Trabajo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarPuestosDeTrabajo()`

```mermaid
sequenceDiagram
    title DSS — CU-176 Consultar los Puestos de Trabajo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarPuestosDeTrabajo()
    activate SIS
    SIS-->>ADM: puestos de la distribuidora con su categoría y su cantidad de empleados activos
    deactivate SIS
```

**Figura 192 — DSS CU-176: Consultar los Puestos de Trabajo**

> La categoría del puesto, y no su nombre, gobierna las reglas que se le aplican al personal.

---


#### DSS — CU-255: Crear un Puesto de Trabajo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearPuestoDeTrabajo(nombre, categoria)`

```mermaid
sequenceDiagram
    title DSS — CU-255 Crear un Puesto de Trabajo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearPuestoDeTrabajo(nombre, categoria)
    activate SIS
    alt el nombre está disponible en la distribuidora
        SIS-->>ADM: puesto creado
    else ya existe un puesto vigente con ese nombre
        SIS-->>ADM: conflicto
    else el nombre o la categoría no son válidos
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 193 — DSS CU-255: Crear un Puesto de Trabajo**

---


#### DSS — CU-256: Modificar un Puesto de Trabajo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `modificarPuestoDeTrabajo(puestoId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-256 Modificar un Puesto de Trabajo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: modificarPuestoDeTrabajo(puestoId, datos)
    activate SIS
    alt el puesto existe y el nombre está disponible
        SIS-->>ADM: puesto modificado
    else el puesto no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else ya existe otro puesto vigente con ese nombre, la categoría nueva no corresponde a las cuentas de sus ocupantes, o es el último puesto activo de su categoría
        SIS-->>ADM: conflicto
    end
    deactivate SIS
```

**Figura 194 — DSS CU-256: Modificar un Puesto de Trabajo**

---


#### DSS — CU-257: Eliminar un Puesto de Trabajo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `eliminarPuestoDeTrabajo(puestoId)`

```mermaid
sequenceDiagram
    title DSS — CU-257 Eliminar un Puesto de Trabajo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: eliminarPuestoDeTrabajo(puestoId)
    activate SIS
    alt el puesto existe y ningún legajo lo ocupa
        SIS-->>ADM: puesto dado de baja
    else el puesto no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el puesto lo ocupa algún legajo, activo o egresado, o es el último activo de su categoría
        SIS-->>ADM: conflicto
    end
    deactivate SIS
```

**Figura 195 — DSS CU-257: Eliminar un Puesto de Trabajo**

---

#### DSS — CU-177: Registrar el Legajo de un Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarEmpleado(datos)`

```mermaid
sequenceDiagram
    title DSS — CU-177 Registrar el Legajo de un Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarEmpleado(datos)
    activate SIS
    alt los datos son válidos y el puesto existe y está activo
        SIS-->>ADM: legajo creado, activo y sin cuenta de acceso
    else el puesto no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el puesto está inactivo, o el documento, el CUIL o el legajo ya pertenecen a otro empleado vigente
        SIS-->>ADM: conflicto
    else falta un dato o el CUIL no es válido
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.1 — DSS CU-177: Registrar el Legajo de un Empleado**

---

#### DSS — CU-178: Modificar el Legajo de un Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `modificarEmpleado(empleadoId, datos)`, `eliminarEmpleado(empleadoId)`

```mermaid
sequenceDiagram
    title DSS — CU-178 Modificar el Legajo de un Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: modificarEmpleado(empleadoId, datos)
    activate SIS
    alt el empleado existe y los datos son válidos
        SIS-->>ADM: legajo modificado
    else el empleado o el puesto no existen en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el puesto está inactivo o no corresponde a la cuenta del empleado, o el documento, el CUIL o el legajo ya pertenecen a otro empleado vigente
        SIS-->>ADM: conflicto
    else el formato o el CUIL no son válidos, o la fecha de ingreso es posterior a la de egreso
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS

    ADM->>SIS: eliminarEmpleado(empleadoId)
    activate SIS
    alt el legajo es una alta errónea: no tiene cuenta de acceso ni, cuando existan, jornadas o documentación
        SIS-->>ADM: legajo dado de baja (alta errónea)
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el legajo tiene cuenta de acceso o, cuando existan, jornadas o documentación
        SIS-->>ADM: conflicto: corresponde registrar el egreso
    end
    deactivate SIS
```

**Figura 195.2 — DSS CU-178: Modificar el Legajo de un Empleado**

---

#### DSS — CU-179: Consultar el Legajo de un Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarEmpleado(empleadoId)`

```mermaid
sequenceDiagram
    title DSS — CU-179 Consultar el Legajo de un Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarEmpleado(empleadoId)
    activate SIS
    alt el empleado existe en la distribuidora
        SIS-->>ADM: legajo completo, con su cuenta de acceso y su ficha de chofer si las tiene
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 195.3 — DSS CU-179: Consultar el Legajo de un Empleado**

---

#### DSS — CU-180: Consultar el Listado de Empleados

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarEmpleados(filtros)`

```mermaid
sequenceDiagram
    title DSS — CU-180 Consultar el Listado de Empleados
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarEmpleados(filtros)
    activate SIS
    alt hay empleados que cumplen los filtros
        SIS-->>ADM: página de empleados con su puesto y su estado, sin datos sensibles
    else ninguno cumple los filtros
        SIS-->>ADM: página vacía
    else un filtro tiene un valor inválido
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.4 — DSS CU-180: Consultar el Listado de Empleados**

---

#### DSS — CU-181: Registrar el Egreso de un Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarEgresoDelEmpleado(empleadoId, fechaDeEgreso, motivo)`, `reingresarEmpleado(empleadoId, fechaDeIngreso)`

```mermaid
sequenceDiagram
    title DSS — CU-181 Registrar el Egreso de un Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarEgresoDelEmpleado(empleadoId, fechaDeEgreso, motivo)
    activate SIS
    alt el empleado está activo, la fecha es válida y el chofer no tiene pedidos en curso
        SIS-->>ADM: legajo egresado, cuenta bloqueada y vehículo liberado si era chofer
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el empleado ya está egresado o el chofer tiene pedidos en curso
        SIS-->>ADM: conflicto
    else la fecha es anterior a la de ingreso
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS

    ADM->>SIS: reingresarEmpleado(empleadoId, fechaDeIngreso)
    activate SIS
    alt el empleado está egresado
        SIS-->>ADM: legajo activo con la fecha de ingreso nueva
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el empleado no está egresado
        SIS-->>ADM: conflicto
    else la fecha de ingreso es anterior a la de egreso
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.5 — DSS CU-181: Registrar el Egreso de un Empleado**

> Registrar el egreso y reingresar son dos operaciones del mismo caso de uso: el reingreso no desbloquea la cuenta de acceso.

---

#### DSS — CU-182: Otorgar una Cuenta de Acceso a un Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `otorgarCuentaDeAcceso(empleadoId, datosDeAcceso)`

```mermaid
sequenceDiagram
    title DSS — CU-182 Otorgar una Cuenta de Acceso a un Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: otorgarCuentaDeAcceso(empleadoId, datosDeAcceso)
    activate SIS
    alt el empleado está activo, sin cuenta, y su puesto admite acceso
        SIS-->>ADM: cuenta creada con el rol del puesto y vinculada al legajo
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el empleado ya tiene cuenta, está egresado, o el correo o el teléfono ya están en uso
        SIS-->>ADM: conflicto
    else la categoría del puesto no admite cuenta, o faltan o son inválidos el teléfono o los datos de acceso
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.6 — DSS CU-182: Otorgar una Cuenta de Acceso a un Empleado**

---

#### DSS — CU-183: Registrar el Curso de Transporte de Mercancías Peligrosas del Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearTareaDelEmpleado(empleadoId, planId, vencimiento, detalle)`

```mermaid
sequenceDiagram
    title DSS — CU-183 Registrar el Curso de Transporte de Mercancías Peligrosas del Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearTareaDelEmpleado(empleadoId, planId, vencimiento, detalle)
    activate SIS
    alt el plan aplica al puesto del empleado y el vencimiento está vigente
        SIS-->>ADM: tarea creada, empleado habilitado
    else el vencimiento ya pasó al cargarlo
        SIS-->>ADM: tarea creada y empleado no habilitado para el despacho
    else el empleado o el plan no existen en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el empleado está egresado
        SIS-->>ADM: conflicto
    else el plan no es de sujeto empleado o no aplica a la categoría del puesto
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.7 — DSS CU-183: Registrar el Curso de Transporte de Mercancías Peligrosas del Empleado**

> Las tres tareas de documentación del personal (CU-183, CU-184 y CU-185) son la misma operación del sistema apuntada a un plan distinto.

---

#### DSS — CU-184: Registrar el Examen Psicofísico del Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearTareaDelEmpleado(empleadoId, planId, vencimiento, detalle)`

```mermaid
sequenceDiagram
    title DSS — CU-184 Registrar el Examen Psicofísico del Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearTareaDelEmpleado(empleadoId, planId, vencimiento, detalle)
    activate SIS
    alt el plan aplica al puesto del empleado y el vencimiento está vigente
        SIS-->>ADM: tarea creada, empleado habilitado
    else el vencimiento ya pasó al cargarlo
        SIS-->>ADM: tarea creada y empleado no habilitado para el despacho
    else el empleado o el plan no existen en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el empleado está egresado
        SIS-->>ADM: conflicto
    else el plan no es de sujeto empleado o no aplica a la categoría del puesto
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.8 — DSS CU-184: Registrar el Examen Psicofísico del Empleado**

> Misma operación que CU-183 y CU-185, con el plan «Examen psicofísico».

---

#### DSS — CU-185: Registrar el Alta en la ART del Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearTareaDelEmpleado(empleadoId, planId, vencimiento, detalle)`

```mermaid
sequenceDiagram
    title DSS — CU-185 Registrar el Alta en la ART del Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearTareaDelEmpleado(empleadoId, planId, vencimiento, detalle)
    activate SIS
    alt el plan aplica al puesto del empleado y el vencimiento está vigente
        SIS-->>ADM: tarea creada
    else el vencimiento ya pasó al cargarlo
        SIS-->>ADM: tarea creada y cobertura vencida
    else el empleado o el plan no existen en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el empleado está egresado
        SIS-->>ADM: conflicto
    else el plan no es de sujeto empleado o no aplica a la categoría del puesto
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.9 — DSS CU-185: Registrar el Alta en la ART del Empleado**

> Misma operación que CU-183 y CU-184, con el plan «Alta en ART», que no bloquea el despacho.

---

#### DSS — CU-186: Adjuntar un Archivo al Legajo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `adjuntarArchivoAlLegajo(empleadoId, archivo, etiqueta)`

```mermaid
sequenceDiagram
    title DSS — CU-186 Adjuntar un Archivo al Legajo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: adjuntarArchivoAlLegajo(empleadoId, archivo, etiqueta)
    activate SIS
    alt el empleado existe y el archivo es admisible
        SIS-->>ADM: adjunto registrado en el legajo
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el archivo falta, está vacío, es de un tipo no admitido o supera el tamaño máximo
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.10 — DSS CU-186: Adjuntar un Archivo al Legajo**

---

#### DSS — CU-187: Consultar los Vencimientos del Personal

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarVencimientosDelPersonal(dias, categoria)`, `consultarDocumentacionDelEmpleado(empleadoId)`

```mermaid
sequenceDiagram
    title DSS — CU-187 Consultar los Vencimientos del Personal
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarVencimientosDelPersonal(dias, categoria)
    activate SIS
    alt hay vencimientos en la ventana
        SIS-->>ADM: tareas por empleado ordenadas por urgencia, con la marca de inhabilitado
    else no hay ninguno
        SIS-->>ADM: listado vacío
    end
    deactivate SIS

    ADM->>SIS: consultarDocumentacionDelEmpleado(empleadoId)
    activate SIS
    alt el empleado existe en la distribuidora
        SIS-->>ADM: tareas con su estado de vencimiento, marca de inhabilitado y documentos faltantes
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 195.11 — DSS CU-187: Consultar los Vencimientos del Personal**

---

#### DSS — CU-188: Avisar los Vencimientos Próximos del Personal

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `avisarVencimientosPendientes()`

```mermaid
sequenceDiagram
    title DSS — CU-188 Avisar los Vencimientos Próximos del Personal
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor ADM as Administrador (ACT-03)

    Note over SAU: Se ejecuta una vez por<br/>día
    SAU->>SIS: avisarVencimientosPendientes()
    activate SIS
    alt Hay documentación del personal por vencer, vencida o faltante
        SIS-)ADM: notificarVencimientosDelPersonal(tareas)
        Note over SIS: El aviso sale por correo<br/>a los administradores de<br/>cada distribuidora
        SIS-->>SAU: avisos enviados
    else No hay ninguna
        SIS-->>SAU: el ciclo termina sin avisos
    end
    deactivate SIS
```

**Figura 195.12 — DSS CU-188: Avisar los Vencimientos Próximos del Personal**

---

#### DSS — CU-189: Registrar la Asistencia de un Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarAsistencias(desde, hasta)`, `registrarAsistencia(empleadoId, ingreso, egreso)`, `corregirAsistencia(asistenciaId, datos, nota)`

```mermaid
sequenceDiagram
    title DSS — CU-189 Registrar la Asistencia de un Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarAsistencias(desde, hasta)
    activate SIS
    alt hay jornadas en el período
        SIS-->>ADM: jornadas con su duración, incluidas las abiertas
    else no hay ninguna
        SIS-->>ADM: listado vacío
    end
    deactivate SIS

    ADM->>SIS: registrarAsistencia(empleadoId, ingreso, egreso)
    activate SIS
    alt el empleado está activo y no tiene otra jornada abierta
        SIS-->>ADM: jornada registrada
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el empleado está egresado o ya tiene una jornada abierta
        SIS-->>ADM: conflicto
    else el egreso no es posterior al ingreso
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS

    ADM->>SIS: corregirAsistencia(asistenciaId, datos, nota)
    activate SIS
    alt la jornada existe y la corrección tiene nota
        SIS-->>ADM: jornada corregida
    else la jornada no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else falta la nota
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.13 — DSS CU-189: Registrar la Asistencia de un Empleado**

---

#### DSS — CU-190: Registrar el Inicio y el Fin de la Jornada

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `registrarInicioDeJornada()`, `registrarFinDeJornada()`

```mermaid
sequenceDiagram
    title DSS — CU-190 Registrar el Inicio y el Fin de la Jornada
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: registrarInicioDeJornada()
    activate SIS
    alt el chofer tiene un legajo activo y ninguna jornada abierta
        SIS-->>CHO: jornada abierta
    else la cuenta no tiene legajo activo o ya hay una jornada abierta
        SIS-->>CHO: conflicto
    end
    deactivate SIS

    CHO->>SIS: registrarFinDeJornada()
    activate SIS
    alt el chofer tiene una jornada abierta
        SIS-->>CHO: jornada cerrada con la hora de la marca
    else no hay ninguna jornada abierta
        SIS-->>CHO: conflicto
    end
    deactivate SIS
```

**Figura 195.14 — DSS CU-190: Registrar el Inicio y el Fin de la Jornada**

---

#### DSS — CU-191: Registrar una Licencia o Ausencia

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarLicencia(empleadoId, tipo, desde, hasta, motivo)`, `modificarLicencia(licenciaId, datos)`, `cancelarLicencia(licenciaId)`

```mermaid
sequenceDiagram
    title DSS — CU-191 Registrar una Licencia o Ausencia
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarLicencia(empleadoId, tipo, desde, hasta, motivo)
    activate SIS
    alt el período no se superpone con otra licencia
        SIS-->>ADM: licencia solicitada
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else el empleado está egresado o el período se superpone con otra licencia
        SIS-->>ADM: conflicto
    else la fecha de fin es anterior a la de inicio
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS

    ADM->>SIS: modificarLicencia(licenciaId, datos)
    activate SIS
    alt la licencia está solicitada y el período es válido
        SIS-->>ADM: licencia modificada
    else la licencia no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else la licencia no está solicitada o el período se superpone
        SIS-->>ADM: conflicto
    end
    deactivate SIS

    ADM->>SIS: cancelarLicencia(licenciaId)
    activate SIS
    alt la licencia no está rechazada ni cancelada y no terminó
        SIS-->>ADM: licencia cancelada
    else la licencia no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else la licencia ya estaba rechazada o cancelada, o ya terminó
        SIS-->>ADM: conflicto
    end
    deactivate SIS
```

**Figura 195.15 — DSS CU-191: Registrar una Licencia o Ausencia**

---

#### DSS — CU-192: Resolver una Solicitud de Licencia

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarLicencias(estado, desde, hasta)`, `aprobarLicencia(licenciaId)`, `rechazarLicencia(licenciaId, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-192 Resolver una Solicitud de Licencia
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarLicencias(estado, desde, hasta)
    activate SIS
    alt hay licencias que cumplen los filtros
        SIS-->>ADM: licencias con el nombre del empleado
    else ninguna cumple los filtros
        SIS-->>ADM: listado vacío
    end
    deactivate SIS

    ADM->>SIS: aprobarLicencia(licenciaId)
    activate SIS
    alt la licencia está solicitada
        SIS-->>ADM: licencia aprobada, con su autor y su fecha
    else la licencia no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else la licencia no está solicitada
        SIS-->>ADM: conflicto
    end
    deactivate SIS

    ADM->>SIS: rechazarLicencia(licenciaId, motivo)
    activate SIS
    alt la licencia está solicitada y hay motivo
        SIS-->>ADM: licencia rechazada, con su motivo, su autor y su fecha
    else la licencia no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    else la licencia no está solicitada
        SIS-->>ADM: conflicto
    else falta el motivo
        SIS-->>ADM: datos inválidos
    end
    deactivate SIS
```

**Figura 195.16 — DSS CU-192: Resolver una Solicitud de Licencia**

---

#### DSS — CU-193: Consultar el Saldo de Vacaciones de un Empleado

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarSaldoDeVacaciones(empleadoId, anio)`

```mermaid
sequenceDiagram
    title DSS — CU-193 Consultar el Saldo de Vacaciones de un Empleado
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarSaldoDeVacaciones(empleadoId, anio)
    activate SIS
    alt el empleado existe en la distribuidora
        SIS-->>ADM: días que corresponden, días tomados y saldo
    else el empleado no existe en la distribuidora
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 195.17 — DSS CU-193: Consultar el Saldo de Vacaciones de un Empleado**

---

#### DSS — CU-194: Consultar el Tablero de Personal

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarTableroDePersonal()`

```mermaid
sequenceDiagram
    title DSS — CU-194 Consultar el Tablero de Personal
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarTableroDePersonal()
    activate SIS
    SIS-->>ADM: empleados activos por puesto, presentes hoy, de licencia hoy y documentos por estado de vencimiento
    deactivate SIS
```

**Figura 195.18 — DSS CU-194: Consultar el Tablero de Personal**

---

#### DSS — CU-246: Verificar la Habilitación Laboral del Chofer

**Actor:** ninguno directo (caso incluido)

Caso incluido: no tiene diagrama de secuencia propio. Lo inician CU-012, CU-013 y CU-015, y su operación forma parte del diagrama de secuencia de cada uno de ellos (caso base).

---

### SS-08 — Gestión de Productos e Inventario (ampliación: stock físico y carga del camión, I-13)

#### DSS — CU-207: Consultar los Depósitos

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarDepositos()`

```mermaid
sequenceDiagram
    title DSS — CU-207 Consultar los Depósitos
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarDepositos()
    activate SIS
    SIS-->>ADM: depósitos de la distribuidora
    deactivate SIS
```

**Figura 196 — DSS CU-207: Consultar los Depósitos**

---


#### DSS — CU-258: Registrar un Depósito

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarDeposito(nombre, codigo, tipo, direccion)`

```mermaid
sequenceDiagram
    title DSS — CU-258 Registrar un Depósito
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarDeposito(nombre, codigo, tipo, direccion)
    activate SIS
    alt el código está libre
        SIS-->>ADM: depósito creado
    else el código ya lo usa otro depósito vigente
        SIS-->>ADM: conflicto, con el detalle del campo
    end
    deactivate SIS
```

**Figura 197 — DSS CU-258: Registrar un Depósito**

---


#### DSS — CU-259: Modificar un Depósito

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `actualizarDeposito(depositoId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-259 Modificar un Depósito
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: actualizarDeposito(depositoId, datos)
    activate SIS
    alt el depósito existe
        SIS-->>ADM: depósito actualizado
    else el depósito no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 198 — DSS CU-259: Modificar un Depósito**

---


#### DSS — CU-260: Dar de Baja un Depósito

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `darDeBajaDeposito(depositoId)`

```mermaid
sequenceDiagram
    title DSS — CU-260 Dar de Baja un Depósito
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: darDeBajaDeposito(depositoId)
    activate SIS
    alt el depósito no tiene saldo
        SIS-->>ADM: baja confirmada
    else el depósito tiene saldo
        SIS-->>ADM: conflicto, con el saldo pendiente
    end
    deactivate SIS
```

**Figura 199 — DSS CU-260: Dar de Baja un Depósito**

---

#### DSS — CU-208: Consultar el Stock por Ubicación

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarStockPorUbicacion(ubicacionId, productoId)`, `consultarResumenDeStock()`

```mermaid
sequenceDiagram
    title DSS — CU-208 Consultar el Stock por Ubicación
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    opt resumen por tipo de garrafa
        ADM->>SIS: consultarResumenDeStock()
        activate SIS
        SIS-->>ADM: llenas, vacías, defectuosas, reservado, vendible y mínimo por tipo
        deactivate SIS
    end

    opt detalle de una ubicación
        ADM->>SIS: consultarStockPorUbicacion(ubicacionId, productoId)
        activate SIS
        alt la ubicación existe
            SIS-->>ADM: saldos por tipo de garrafa y condición
        else la ubicación no existe
            SIS-->>ADM: recurso no encontrado
        end
        deactivate SIS
    end
```

**Figura 200 — DSS CU-208: Consultar el Stock por Ubicación**

---

#### DSS — CU-209: Consultar los Movimientos de Stock

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarMovimientosDeStock(productoId, ubicacionId, motivo, desde, hasta, pagina)`

```mermaid
sequenceDiagram
    title DSS — CU-209 Consultar los Movimientos de Stock
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarMovimientosDeStock(productoId, ubicacionId, motivo, desde, hasta, pagina)
    activate SIS
    alt el rango de fechas es válido
        SIS-->>ADM: página de movimientos y total
    else el rango está invertido
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS
```

**Figura 201 — DSS CU-209: Consultar los Movimientos de Stock**

---

#### DSS — CU-210: Configurar el Stock Mínimo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `configurarStockMinimo(depositoId, minimos)`

```mermaid
sequenceDiagram
    title DSS — CU-210 Configurar el Stock Mínimo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: configurarStockMinimo(depositoId, minimos)
    activate SIS
    alt los mínimos son válidos
        SIS-->>ADM: umbrales vigentes del depósito
    else un mínimo es negativo
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    else el depósito o un tipo de garrafa no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 202 — DSS CU-210: Configurar el Stock Mínimo**

---

#### DSS — CU-211: Avisar el Stock Bajo

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `avisarStockBajo()`

```mermaid
sequenceDiagram
    title DSS — CU-211 Avisar el Stock Bajo
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor ADM as Administrador (ACT-03)

    Note over SAU: Se ejecuta cada hora
    SAU->>SIS: avisarStockBajo()
    activate SIS
    alt hay depósitos por debajo del mínimo sin aviso
        SIS-)ADM: notificarStockBajo(depositos)
        Note over SIS: El aviso sale por correo<br/>a los administradores de<br/>cada distribuidora
        SIS-->>SAU: avisos enviados
    else no hay ninguno
        SIS-->>SAU: el ciclo termina sin avisos
    end
    deactivate SIS
```

**Figura 203 — DSS CU-211: Avisar el Stock Bajo**

---

#### DSS — CU-212: Transferir Stock entre Depósitos

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `transferirStock(origenId, destinoId, productoId, condicion, cantidad)`

```mermaid
sequenceDiagram
    title DSS — CU-212 Transferir Stock entre Depósitos
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: transferirStock(origenId, destinoId, productoId, condicion, cantidad)
    activate SIS
    alt el origen tiene la cantidad
        SIS-->>ADM: transferencia registrada, con su lote
    else el origen no tiene la cantidad
        SIS-->>ADM: solicitud inválida, con el saldo disponible
    else origen y destino son la misma ubicación
        SIS-->>ADM: solicitud inválida
    else una ubicación no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 204 — DSS CU-212: Transferir Stock entre Depósitos**

---

#### DSS — CU-213: Registrar un Ajuste o una Merma de Stock

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarAjusteDeStock(ubicacionId, motivo, nota, items)`, `consultarAjustesDeStock(desde, hasta, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-213 Registrar un Ajuste o una Merma de Stock
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    opt registro de un ajuste
        ADM->>SIS: registrarAjusteDeStock(ubicacionId, motivo, nota, items)
        activate SIS
        alt el ajuste es válido
            SIS-->>ADM: ajuste registrado, con su número
        else la nota está vacía o un saldo quedaría negativo
            SIS-->>ADM: solicitud inválida, con el detalle
        else la ubicación no existe
            SIS-->>ADM: recurso no encontrado
        end
        deactivate SIS
    end

    opt consulta de los ajustes
        ADM->>SIS: consultarAjustesDeStock(desde, hasta, motivo)
        activate SIS
        SIS-->>ADM: ajustes del período
        deactivate SIS
    end
```

**Figura 205 — DSS CU-213: Registrar un Ajuste o una Merma de Stock**

---

#### DSS — CU-218: Registrar la Carga del Camión

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarCargaDelCamion(vehiculoId, depositoId, ayudanteId, items)`, `reponerCargaDelCamion(cargaId, items)`, `cancelarCargaDelCamion(cargaId)`, `consultarCargasDelCamion(estado, fecha, vehiculoId, choferId)`

```mermaid
sequenceDiagram
    title DSS — CU-218 Registrar la Carga del Camión
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarCargaDelCamion(vehiculoId, depositoId, ayudanteId, items)
    activate SIS
    alt el camión está en uso y el depósito tiene las unidades
        SIS-->>ADM: hoja de carga abierta
    else el vehículo o el chofer ya tienen una carga abierta
        SIS-->>ADM: conflicto
    else el depósito no tiene las unidades
        SIS-->>ADM: solicitud inválida, con el saldo disponible
    end
    deactivate SIS

    ADM->>SIS: reponerCargaDelCamion(cargaId, items)
    activate SIS
    alt la carga está abierta
        SIS-->>ADM: hoja de carga actualizada
    else la carga ya regresó o está cerrada
        SIS-->>ADM: conflicto
    end
    deactivate SIS

    ADM->>SIS: cancelarCargaDelCamion(cargaId)
    activate SIS
    alt la carga todavía no salió
        SIS-->>ADM: carga cancelada y stock devuelto
    else la carga ya salió
        SIS-->>ADM: conflicto
    end
    deactivate SIS

    ADM->>SIS: consultarCargasDelCamion(estado, fecha, vehiculoId, choferId)
    activate SIS
    SIS-->>ADM: cargas del camión
    deactivate SIS
```

**Figura 206 — DSS CU-218: Registrar la Carga del Camión**

---

#### DSS — CU-219: Registrar la Salida del Camión

**Actor:** Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `registrarSalidaDelCamion(cargaId)`

```mermaid
sequenceDiagram
    title DSS — CU-219 Registrar la Salida del Camión
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: registrarSalidaDelCamion(cargaId)
    activate SIS
    alt la carga está cargando
        SIS-->>CHO: carga en ruta
    else la carga no está cargando
        SIS-->>CHO: conflicto
    else la carga no existe o no es suya
        SIS-->>CHO: recurso no encontrado
    end
    deactivate SIS
    Note over CHO,SIS: También lo inicia el Administrador (ACT-03)
```

**Figura 207 — DSS CU-219: Registrar la Salida del Camión**

---

#### DSS — CU-220: Descontar del Camión lo Entregado

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `descontarStockDeLaEntrega(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-220 Descontar del Camión lo Entregado
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    Note over SAU: Reacciona a la entrega<br/>de cada pedido
    SAU->>SIS: descontarStockDeLaEntrega(pedidoId)
    activate SIS
    alt el pedido no tiene movimientos de stock
        SIS-->>SAU: stock descontado del origen
    else el pedido ya tiene movimientos
        SIS-->>SAU: nada que hacer
    else el camión con carga abierta no alcanza lo entregado
        SIS-->>SAU: nada registrado, queda para la conciliación
    end
    deactivate SIS
```

**Figura 208 — DSS CU-220: Descontar del Camión lo Entregado**

---

#### DSS — CU-221: Registrar el Regreso del Camión

**Actor:** Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `registrarRegresoDelCamion(cargaId, devueltos)`

```mermaid
sequenceDiagram
    title DSS — CU-221 Registrar el Regreso del Camión
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: registrarRegresoDelCamion(cargaId, devueltos)
    activate SIS
    alt la carga está en ruta
        SIS-->>CHO: lo declarado, lo esperado y la diferencia
    else la carga no está en ruta
        SIS-->>CHO: conflicto
    else una cantidad es negativa
        SIS-->>CHO: solicitud inválida, con el detalle del campo
    end
    deactivate SIS
    Note over CHO,SIS: También lo inicia el Administrador (ACT-03)
```

**Figura 209 — DSS CU-221: Registrar el Regreso del Camión**

---

#### DSS — CU-222: Cerrar la Rendición de Stock del Camión

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `cerrarRendicionDeStock(cargaId, nota)`

```mermaid
sequenceDiagram
    title DSS — CU-222 Cerrar la Rendición de Stock del Camión
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: cerrarRendicionDeStock(cargaId, nota)
    activate SIS
    alt la carga regresó y la rendición cierra sin diferencia
        SIS-->>ADM: carga cerrada
    else la carga regresó y hay diferencia con su nota
        SIS-->>ADM: carga cerrada con diferencia
    else hay diferencia y falta la nota
        SIS-->>ADM: solicitud inválida
    else el faltante dejaría negativo el stock vendible
        SIS-->>ADM: solicitud inválida
    else la carga no regresó
        SIS-->>ADM: conflicto
    end
    deactivate SIS
```

**Figura 210 — DSS CU-222: Cerrar la Rendición de Stock del Camión**

---

#### DSS — CU-223: Consultar la Carga Actual del Camión

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `consultarCargaActual()`

```mermaid
sequenceDiagram
    title DSS — CU-223 Consultar la Carga Actual del Camión
    autonumber
    actor CHO as Chofer (ACT-02)
    participant SIS as :Sistema

    CHO->>SIS: consultarCargaActual()
    activate SIS
    alt el chofer tiene una carga abierta
        SIS-->>CHO: carga con lo cargado, lo entregado y lo esperado
    else no tiene carga abierta
        SIS-->>CHO: ninguna carga
    end
    deactivate SIS
```

**Figura 211 — DSS CU-223: Consultar la Carga Actual del Camión**

---

#### DSS — CU-224: Conciliar el Stock Vendible con el Físico

**Actor:** Administrador (ACT-03), Sistema Automático (ACT-04)
**Operaciones del sistema:** `conciliarStock()`, `consultarConciliacionDeStock()`

```mermaid
sequenceDiagram
    title DSS — CU-224 Conciliar el Stock Vendible con el Físico
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor ADM as Administrador (ACT-03)

    opt proceso nocturno
        Note over SAU: Se ejecuta una vez por noche
        SAU->>SIS: conciliarStock()
        activate SIS
        alt hay diferencia entre el vendible y el físico
            SIS-)ADM: notificarDiferenciaDeStock(diferencias)
            Note over SIS: El aviso sale por correo<br/>a los administradores de<br/>cada distribuidora
            SIS-->>SAU: entregas aplicadas y diferencias avisadas
        else no hay diferencia
            SIS-->>SAU: entregas aplicadas
        end
        deactivate SIS
    end

    opt consulta de la conciliación
        ADM->>SIS: consultarConciliacionDeStock()
        activate SIS
        SIS-->>ADM: vendible, físico, reservado y diferencia por tipo de garrafa
        deactivate SIS
    end
```

**Figura 212 — DSS CU-224: Conciliar el Stock Vendible con el Físico**

---

#### DSS — CU-248: Verificar la Carga de Camión Abierta del Chofer

**Actor:** ninguno directo (caso incluido)

Caso incluido: no tiene diagrama de secuencia propio. Lo inician CU-012, CU-013 y CU-015, y su operación forma parte del diagrama de secuencia de cada uno de ellos (caso base).

---

#### DSS — CU-249: Configurar el Control de Carga de Camión Abierta

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `configurarControlDeCargaAbierta(exigirCargaDeCamionAbierta)`

```mermaid
sequenceDiagram
    title DSS — CU-249 Configurar el Control de Carga de Camión Abierta
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: configurarControlDeCargaAbierta(exigirCargaDeCamionAbierta)
    activate SIS
    alt el valor es válido
        SIS-->>ADM: configuración guardada
    else el valor no es booleano
        SIS-->>ADM: solicitud inválida, con el detalle del campo
    end
    deactivate SIS
```

**Figura 213 — DSS CU-249: Configurar el Control de Carga de Camión Abierta**

---

#### DSS — CU-250: Aplicar un Movimiento de Stock

**Actor:** ninguno directo (caso incluido)

Caso incluido: no tiene diagrama de secuencia propio. Lo inician CU-212, CU-213, CU-217, CU-218, CU-220 y CU-222, y su operación forma parte del diagrama de secuencia de cada uno de ellos (caso base).

---

### SS-20 — Compras (I-13)

#### DSS — CU-214: Consultar los Proveedores

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarProveedores(termino)`

```mermaid
sequenceDiagram
    title DSS — CU-214 Consultar los Proveedores
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarProveedores(termino)
    activate SIS
    SIS-->>ADM: proveedores vigentes
    deactivate SIS
```

**Figura 214 — DSS CU-214: Consultar los Proveedores**

---


#### DSS — CU-261: Registrar un Proveedor

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarProveedor(razonSocial, cuit, tipo, datosDeContacto, plazoDePago)`

```mermaid
sequenceDiagram
    title DSS — CU-261 Registrar un Proveedor
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: registrarProveedor(razonSocial, cuit, tipo, datosDeContacto, plazoDePago)
    activate SIS
    alt el CUIT está libre
        SIS-->>ADM: proveedor creado
    else el CUIT ya pertenece a un proveedor vigente
        SIS-->>ADM: conflicto, con el detalle del campo
    end
    deactivate SIS
```

**Figura 215 — DSS CU-261: Registrar un Proveedor**

---


#### DSS — CU-262: Modificar un Proveedor

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `actualizarProveedor(proveedorId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-262 Modificar un Proveedor
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: actualizarProveedor(proveedorId, datos)
    activate SIS
    alt el proveedor existe
        SIS-->>ADM: proveedor actualizado
    else el proveedor no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 216 — DSS CU-262: Modificar un Proveedor**

---


#### DSS — CU-263: Dar de Baja un Proveedor

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `darDeBajaProveedor(proveedorId)`

```mermaid
sequenceDiagram
    title DSS — CU-263 Dar de Baja un Proveedor
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: darDeBajaProveedor(proveedorId)
    activate SIS
    SIS-->>ADM: baja confirmada
    deactivate SIS
```

**Figura 217 — DSS CU-263: Dar de Baja un Proveedor**

---

#### DSS — CU-215: Emitir una Orden de Compra

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `emitirOrdenDeCompra(proveedorId, depositoId, items, fechaEsperada)`, `enviarOrdenDeCompra(ordenId)`, `consultarOrdenesDeCompra(estado, proveedorId, desde, hasta)`

```mermaid
sequenceDiagram
    title DSS — CU-215 Emitir una Orden de Compra
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    opt preparación de la orden
        ADM->>SIS: emitirOrdenDeCompra(proveedorId, depositoId, items, fechaEsperada)
        activate SIS
        alt los datos son válidos
            SIS-->>ADM: orden en borrador, con su número
        else un renglón es inválido
            SIS-->>ADM: solicitud inválida, con el detalle del campo
        else el proveedor o el depósito no existe
            SIS-->>ADM: recurso no encontrado
        end
        deactivate SIS
    end

    opt envío de la orden
        ADM->>SIS: enviarOrdenDeCompra(ordenId)
        activate SIS
        alt la orden está en borrador
            SIS-->>ADM: orden enviada
        else la orden ya no está en borrador
            SIS-->>ADM: conflicto
        end
        deactivate SIS
    end

    opt consulta de las órdenes
        ADM->>SIS: consultarOrdenesDeCompra(estado, proveedorId, desde, hasta)
        activate SIS
        SIS-->>ADM: órdenes de compra
        deactivate SIS
    end
```

**Figura 218 — DSS CU-215: Emitir una Orden de Compra**

---

#### DSS — CU-216: Cancelar una Orden de Compra

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `cancelarOrdenDeCompra(ordenId, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-216 Cancelar una Orden de Compra
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: cancelarOrdenDeCompra(ordenId, motivo)
    activate SIS
    alt la orden no tiene recepciones
        SIS-->>ADM: orden cancelada
    else la orden tiene recepciones o ya está cerrada
        SIS-->>ADM: conflicto
    else la orden no existe
        SIS-->>ADM: recurso no encontrado
    end
    deactivate SIS
```

**Figura 219 — DSS CU-216: Cancelar una Orden de Compra**

---

#### DSS — CU-217: Registrar la Recepción de una Compra

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarRecepcionDeCompra(ordenId, proveedorId, depositoId, tipoDeComprobante, numeroDeComprobante, items)`, `anularRecepcionDeCompra(recepcionId, motivo)`, `consultarRecepcionesDeCompra(proveedorId, desde, hasta, estadoDePago)`

```mermaid
sequenceDiagram
    title DSS — CU-217 Registrar la Recepción de una Compra
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    opt recepción de una compra
        ADM->>SIS: registrarRecepcionDeCompra(ordenId, proveedorId, depositoId, tipoDeComprobante, numeroDeComprobante, items)
        activate SIS
        alt la recepción es válida
            SIS-->>ADM: recepción registrada
        else el comprobante ya se registró para el proveedor
            SIS-->>ADM: conflicto
        else los vacíos entregados superan el saldo del depósito
            SIS-->>ADM: solicitud inválida, con el saldo disponible
        else la orden no existe
            SIS-->>ADM: recurso no encontrado
        else la orden está cancelada o ya recibida por completo
            SIS-->>ADM: conflicto
        end
        deactivate SIS
    end

    opt anulación de una recepción
        ADM->>SIS: anularRecepcionDeCompra(recepcionId, motivo)
        activate SIS
        alt el depósito todavía tiene lo ingresado
            SIS-->>ADM: recepción anulada
        else el depósito ya no tiene lo ingresado
            SIS-->>ADM: conflicto
        end
        deactivate SIS
    end

    opt consulta de las recepciones
        ADM->>SIS: consultarRecepcionesDeCompra(proveedorId, desde, hasta, estadoDePago)
        activate SIS
        SIS-->>ADM: recepciones de compra
        deactivate SIS
    end
```

**Figura 220 — DSS CU-217: Registrar la Recepción de una Compra**

---

### SS-21 — Caja, Rendiciones y Cuentas Corrientes

#### DSS — CU-225: Crear una Caja

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearCaja(nombre, tipo, requiereSesion)`

```mermaid
sequenceDiagram
    title DSS — CU-225 Crear una Caja
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearCaja(nombre, tipo, requiereSesion)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: caja creada con saldo cero
    else ya existe una caja con ese nombre
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 221 — DSS CU-225: Crear una Caja**

---


#### DSS — CU-264: Modificar una Caja

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `modificarCaja(cajaId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-264 Modificar una Caja
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: modificarCaja(cajaId, datos)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: caja con los datos nuevos
    else la caja tiene una sesión abierta y se pretende desactivarla
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 222 — DSS CU-264: Modificar una Caja**

---

#### DSS — CU-226: Abrir la Caja

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `abrirCaja(cajaId, montoInicial)`

```mermaid
sequenceDiagram
    title DSS — CU-226 Abrir la Caja
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: abrirCaja(cajaId, montoInicial)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: sesión abierta con su monto inicial
    else la caja ya tiene una sesión abierta
        SIS-->>ADM: operación rechazada
    else la caja no exige sesión
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 223 — DSS CU-226: Abrir la Caja**

---

#### DSS — CU-227: Cerrar la Caja con Arqueo

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `cerrarCajaConArqueo(sesionId, montoContado)`

```mermaid
sequenceDiagram
    title DSS — CU-227 Cerrar la Caja con Arqueo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: cerrarCajaConArqueo(sesionId, montoContado)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: sesión cerrada con el monto esperado, el contado y la diferencia
    else la sesión ya estaba cerrada
        SIS-->>ADM: operación rechazada
    else el monto contado es negativo
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 224 — DSS CU-227: Cerrar la Caja con Arqueo**

---

#### DSS — CU-228: Registrar un Ingreso o Egreso de Caja

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `registrarMovimientoDeCaja(cajaId, sentido, importe, categoriaId, medio, descripcion)`, `transferirEntreCajas(cajaOrigenId, cajaDestinoId, importe)`

```mermaid
sequenceDiagram
    title DSS — CU-228 Registrar un Ingreso o Egreso de Caja
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    alt Ingreso o egreso manual
        ADM->>SIS: registrarMovimientoDeCaja(cajaId, sentido, importe, categoriaId, medio, descripcion)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: movimiento registrado con el saldo actualizado
        else la caja exige sesión y no está abierta, o el saldo no alcanza
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    else Transferencia entre cajas
        ADM->>SIS: transferirEntreCajas(cajaOrigenId, cajaDestinoId, importe)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: los dos movimientos asentados
        else alguna caja no admite el movimiento
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    end
```

**Figura 225 — DSS CU-228: Registrar un Ingreso o Egreso de Caja**

---

#### DSS — CU-229: Anular un Movimiento de Caja

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `anularMovimientoDeCaja(movimientoId, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-229 Anular un Movimiento de Caja
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: anularMovimientoDeCaja(movimientoId, motivo)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: contraasiento registrado y saldo corregido
    else el movimiento ya fue anulado
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 226 — DSS CU-229: Anular un Movimiento de Caja**

---

#### DSS — CU-230: Crear una Categoría de Ingresos y Gastos

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearCategoriaDeCaja(nombre, sentido)`

```mermaid
sequenceDiagram
    title DSS — CU-230 Crear una Categoría de Ingresos y Gastos
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: crearCategoriaDeCaja(nombre, sentido)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: categoría creada
    else ya existe una categoría con ese nombre y sentido
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 227 — DSS CU-230: Crear una Categoría de Ingresos y Gastos**

---


#### DSS — CU-265: Modificar una Categoría de Ingresos y Gastos

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `modificarCategoriaDeCaja(categoriaId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-265 Modificar una Categoría de Ingresos y Gastos
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: modificarCategoriaDeCaja(categoriaId, datos)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: categoría con los datos nuevos
    else la categoría es de sistema
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 228 — DSS CU-265: Modificar una Categoría de Ingresos y Gastos**

---

#### DSS — CU-231: Generar la Rendición Diaria del Chofer

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `generarRendicionesDelDia()`

```mermaid
sequenceDiagram
    title DSS — CU-231 Generar la Rendición Diaria del Chofer
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    Note over SAU: Proceso temporal
    SAU->>SIS: generarRendicionesDelDia()
    activate SIS
    alt Otra instancia ya está ejecutando el proceso
        SIS-->>SAU: ejecución salteada
    else Hay choferes con efectivo sin rendir
        Note over SAU,SIS: Abre una rendición por chofer<br/>con sus pedidos y sus cobros
        SIS-->>SAU: rendiciones abiertas (cantidad)
    else El chofer ya tiene una rendición abierta
        SIS-->>SAU: rendición completada con lo nuevo
    else No hay efectivo sin rendir
        SIS-->>SAU: sin cambios
    end
    deactivate SIS
```

**Figura 229 — DSS CU-231: Generar la Rendición Diaria del Chofer**

---

#### DSS — CU-232: Declarar el Efectivo Rendido

**Actor:** Chofer (ACT-02), Administrador (ACT-03)
**Operaciones del sistema:** `declararEfectivoRendido(rendicionId, efectivoDeclarado, gastos)`

```mermaid
sequenceDiagram
    title DSS — CU-232 Declarar el Efectivo Rendido
    autonumber
    actor CHF as Chofer (ACT-02)
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    alt El chofer presenta su rendición
        CHF->>SIS: declararEfectivoRendido(rendicionId, efectivoDeclarado, gastos)
        activate SIS
        alt la operación es válida
            SIS-->>CHF: rendición presentada con el efectivo esperado y la diferencia
        else la rendición no está abierta
            SIS-->>CHF: operación rechazada
        else el efectivo o un gasto no es válido
            SIS-->>CHF: operación rechazada
        end
        deactivate SIS
    else El administrador presenta una rendición
        ADM->>SIS: declararEfectivoRendido(rendicionId, efectivoDeclarado, gastos)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: rendición presentada con el efectivo esperado y la diferencia
        else la rendición no está abierta
            SIS-->>ADM: operación rechazada
        else el efectivo o un gasto no es válido
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    end
```

**Figura 230 — DSS CU-232: Declarar el Efectivo Rendido**

---

#### DSS — CU-233: Aprobar la Rendición del Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `aprobarRendicion(rendicionId, cajaDestinoId, resolucionDeDiferencia)`, `reabrirRendicion(rendicionId)`

```mermaid
sequenceDiagram
    title DSS — CU-233 Aprobar la Rendición del Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    alt Operación aprobarRendicion
        ADM->>SIS: aprobarRendicion(rendicionId, cajaDestinoId, resolucionDeDiferencia)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: rendición aprobada con su movimiento de caja
        else la rendición no está presentada
            SIS-->>ADM: operación rechazada
        else hay diferencia y falta indicar cómo se resuelve
            SIS-->>ADM: operación rechazada
        else la caja destino exige sesión y no la tiene abierta
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    else Reapertura de la rendición
        ADM->>SIS: reabrirRendicion(rendicionId)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: rendición abierta otra vez
        else la rendición no está presentada
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    end
```

**Figura 231 — DSS CU-233: Aprobar la Rendición del Chofer**

---

#### DSS — CU-234: Avisar las Rendiciones sin Cerrar

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `avisarRendicionesSinCerrar()`

```mermaid
sequenceDiagram
    title DSS — CU-234 Avisar las Rendiciones sin Cerrar
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    Note over SAU: Proceso temporal
    SAU->>SIS: avisarRendicionesSinCerrar()
    activate SIS
    alt Otra instancia ya está ejecutando el proceso
        SIS-->>SAU: ejecución salteada
    else Hay rendiciones atrasadas
        Note over SAU,SIS: Marca cada rendición como avisada
        SIS-)ADM: notificarRendicionesSinCerrar(rendiciones)
        SIS-->>SAU: avisos enviados (cantidad)
    else No hay rendiciones atrasadas
        SIS-->>SAU: sin cambios
    end
    deactivate SIS
```

**Figura 232 — DSS CU-234: Avisar las Rendiciones sin Cerrar**

---

#### DSS — CU-235: Habilitar la Cuenta Corriente de un Cliente

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `habilitarCuentaCorriente(clienteId, razonSocial, cuit, condicionFiscal, limiteDeCredito, plazoEnDias)`, `modificarCuentaCorriente(cuentaId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-235 Habilitar la Cuenta Corriente de un Cliente
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    alt Habilitación de la cuenta
        ADM->>SIS: habilitarCuentaCorriente(clienteId, razonSocial, cuit, condicionFiscal, limiteDeCredito, plazoEnDias)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: cuenta corriente creada con saldo cero
        else el cliente ya tiene una cuenta vigente
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    else Modificación de la cuenta
        ADM->>SIS: modificarCuentaCorriente(cuentaId, datos)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: cuenta con los datos nuevos
        else se pretende cerrar una cuenta con saldo
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    end
```

**Figura 233 — DSS CU-235: Habilitar la Cuenta Corriente de un Cliente**

---

#### DSS — CU-236: Vender a Cuenta Corriente

**Actor:** Administrador (ACT-03), Sistema Automático (ACT-04)
**Operaciones del sistema:** `venderACuentaCorriente(clienteId, direccionId, items)`, `registrarCargoDeCuentaCorriente(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-236 Vender a Cuenta Corriente
    autonumber
    actor ADM as Administrador (ACT-03)
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    alt Venta a cuenta corriente
        ADM->>SIS: venderACuentaCorriente(clienteId, direccionId, items)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: pedido creado a cuenta, con el crédito que queda
        else el cliente no tiene crédito suficiente o su cuenta no está activa
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    else Operación registrarCargoDeCuentaCorriente
        Note over SAU: Evento: pedido entregado
        SAU->>SIS: registrarCargoDeCuentaCorriente(pedidoId)
        activate SIS
        alt El pedido es a cuenta y no tiene cargo
            Note over SAU,SIS: Asienta el cargo y actualiza el saldo de la cuenta
            SIS-->>SAU: cargo registrado
        else El pedido no es a cuenta o ya tiene su cargo
            SIS-->>SAU: sin cambios
        end
        deactivate SIS
    end
```

**Figura 234 — DSS CU-236: Vender a Cuenta Corriente**

---

#### DSS — CU-237: Registrar un Pago de Cuenta Corriente

**Actor:** Administrador (ACT-03), Chofer (ACT-02)
**Operaciones del sistema:** `registrarPagoDeCuentaCorriente(cuentaId, importe, medio, cajaId)`, `registrarAjusteDeCuentaCorriente(cuentaId, tipo, importe, motivo)`

```mermaid
sequenceDiagram
    title DSS — CU-237 Registrar un Pago de Cuenta Corriente
    autonumber
    actor CHF as Chofer (ACT-02)
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    alt El chofer registra el cobro en la calle
        CHF->>SIS: registrarPagoDeCuentaCorriente(cuentaId, importe, medio, cajaId)
        activate SIS
        alt la operación es válida
            SIS-->>CHF: pago registrado y aplicado a las deudas más antiguas
        else el cobro no se puede registrar (caja sin sesión, sin caja o sin rendición abierta)
            SIS-->>CHF: operación rechazada
        end
        deactivate SIS
    else El administrador registra el cobro en una caja
        ADM->>SIS: registrarPagoDeCuentaCorriente(cuentaId, importe, medio, cajaId)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: pago registrado y aplicado a las deudas más antiguas
        else el cobro no se puede registrar (caja sin sesión, sin caja o sin rendición abierta)
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    else Ajuste con una nota de crédito o de débito
        ADM->>SIS: registrarAjusteDeCuentaCorriente(cuentaId, tipo, importe, motivo)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: ajuste registrado y saldo actualizado
        else el ajuste no es válido
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    end
```

**Figura 235 — DSS CU-237: Registrar un Pago de Cuenta Corriente**

---

#### DSS — CU-238: Consultar el Estado de Cuenta de un Cliente

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarEstadoDeCuenta(cuentaId, fechaDesde, fechaHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-238 Consultar el Estado de Cuenta de un Cliente
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarEstadoDeCuenta(cuentaId, fechaDesde, fechaHasta)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: asientos del período con su saldo corrido y el saldo inicial
    else la cuenta no existe o es de otra distribuidora
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 236 — DSS CU-238: Consultar el Estado de Cuenta de un Cliente**

---

#### DSS — CU-239: Consultar la Antigüedad de la Deuda

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarAntiguedadDeDeuda()`

```mermaid
sequenceDiagram
    title DSS — CU-239 Consultar la Antigüedad de la Deuda
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarAntiguedadDeDeuda()
    activate SIS
    SIS-->>ADM: deuda de la distribuidora por tramos de antigüedad
    deactivate SIS
```

**Figura 237 — DSS CU-239: Consultar la Antigüedad de la Deuda**

---

#### DSS — CU-240: Configurar las Comisiones por Entrega

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `crearReglaDeComision(empleadoId, productoId, base, valor, vigenteDesde)`, `modificarReglaDeComision(reglaId, datos)`

```mermaid
sequenceDiagram
    title DSS — CU-240 Configurar las Comisiones por Entrega
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    alt Alta de la regla
        ADM->>SIS: crearReglaDeComision(empleadoId, productoId, base, valor, vigenteDesde)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: regla creada
        else la regla se solapa con otra vigente del mismo alcance
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    else Modificación de la regla
        ADM->>SIS: modificarReglaDeComision(reglaId, datos)
        activate SIS
        alt la operación es válida
            SIS-->>ADM: regla con los datos nuevos
        else el cambio la solapa con otra regla
            SIS-->>ADM: operación rechazada
        end
        deactivate SIS
    end
```

**Figura 238 — DSS CU-240: Configurar las Comisiones por Entrega**

---

#### DSS — CU-241: Registrar la Comisión de una Entrega

**Actor:** Sistema Automático (ACT-04)
**Operaciones del sistema:** `registrarComisionDeEntrega(pedidoId)`

```mermaid
sequenceDiagram
    title DSS — CU-241 Registrar la Comisión de una Entrega
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema

    Note over SAU: Evento: pedido entregado
    SAU->>SIS: registrarComisionDeEntrega(pedidoId)
    activate SIS
    alt Hay una regla aplicable
        Note over SAU,SIS: Asienta la comisión con una copia de la regla
        SIS-->>SAU: comisión registrada
    else No hay regla aplicable o el pedido ya devengó su comisión
        SIS-->>SAU: sin cambios
    end
    deactivate SIS
```

**Figura 239 — DSS CU-241: Registrar la Comisión de una Entrega**

---

#### DSS — CU-242: Liquidar las Comisiones de un Chofer

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `liquidarComisionesDelChofer(empleadoId, fechaDesde, fechaHasta)`, `aprobarLiquidacion(liquidacionId)`, `anularLiquidacion(liquidacionId)`

```mermaid
sequenceDiagram
    title DSS — CU-242 Liquidar las Comisiones de un Chofer
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: liquidarComisionesDelChofer(empleadoId, fechaDesde, fechaHasta)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: liquidación en borrador con el bruto, las deducciones y el neto
    else no hay asientos para liquidar
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS

    ADM->>SIS: aprobarLiquidacion(liquidacionId)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: liquidación aprobada, o cerrada sin pago si el neto no es positivo
    else la liquidación no está en borrador
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS

    ADM->>SIS: anularLiquidacion(liquidacionId)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: liquidación anulada y asientos liberados
    else la liquidación ya está pagada
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 240 — DSS CU-242: Liquidar las Comisiones de un Chofer**

---

#### DSS — CU-243: Registrar el Pago de una Liquidación

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `pagarLiquidacion(liquidacionId, cajaId)`

```mermaid
sequenceDiagram
    title DSS — CU-243 Registrar el Pago de una Liquidación
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: pagarLiquidacion(liquidacionId, cajaId)
    activate SIS
    alt la operación es válida
        SIS-->>ADM: liquidación pagada y movimiento de caja registrado
    else la liquidación no está aprobada
        SIS-->>ADM: operación rechazada
    else la caja no puede cubrir el pago
        SIS-->>ADM: operación rechazada
    end
    deactivate SIS
```

**Figura 241 — DSS CU-243: Registrar el Pago de una Liquidación**

---

#### DSS — CU-244: Consultar Mis Comisiones

**Actor:** Chofer (ACT-02)
**Operaciones del sistema:** `consultarMisComisiones(fechaDesde, fechaHasta)`

```mermaid
sequenceDiagram
    title DSS — CU-244 Consultar Mis Comisiones
    autonumber
    actor CHF as Chofer (ACT-02)
    participant SIS as :Sistema

    CHF->>SIS: consultarMisComisiones(fechaDesde, fechaHasta)
    activate SIS
    SIS-->>CHF: comisiones del período y saldo sin liquidar
    deactivate SIS
```

**Figura 242 — DSS CU-244: Consultar Mis Comisiones**

---

#### DSS — CU-245: Consultar el Tablero Financiero

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `consultarTableroFinanciero(fecha)`

```mermaid
sequenceDiagram
    title DSS — CU-245 Consultar el Tablero Financiero
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: consultarTableroFinanciero(fecha)
    activate SIS
    SIS-->>ADM: saldos por caja, rendiciones pendientes, deuda y comisiones a liquidar
    deactivate SIS
```

**Figura 243 — DSS CU-245: Consultar el Tablero Financiero**

---

### CU no modelados y por qué

Tres casos de uso no tienen diagrama de secuencia propio porque son casos incluidos: ningún actor los inicia y su operación forma parte del diagrama de secuencia de cada caso base que los incluye.

| CU | Nombre | Casos base |
|---|---|---|
| CU-082 | Crear Usuario Base | CU-002, CU-003, CU-031, CU-086 y CU-087 |
| CU-159 | Almacenar Archivo | CU-155 y CU-174 |
| CU-160 | Recuperar Archivo | CU-157 y CU-175 |

**Observaciones sobre casos de uso modelados con salvedades:**

1. **CU-268 (Reactivar un Producto) y CU-269 (Consultar los Productos Inactivos)** modelan la reactivación de un producto dado de baja, que el sistema todavía no realiza: están planificados (I-1) y marcados como tales en sus diagramas. CU-040 modela la desactivación, que sí está construida.
2. **CU-049 (Consultar Balance del Chofer)** no tiene una operación de consulta propia: se modela tal como ocurre, como una lectura del perfil del chofer.
3. **Conciliación de pagos:** el registro contable de pagos existe en el sistema pero no tiene una operación del sistema que lo exponga a ningún actor, de modo que no admite un diagrama de secuencia.

---


#### Módulos inteligentes en diseño (CU-105 a CU-108)

Diagramas de los procesos automáticos planificados.

##### DSS — CU-105: Planificar el mantenimiento y las habilitaciones de la flota

**Actor:** Chofer (ACT-02), Administrador (ACT-03), Sistema Automático (ACT-04)
**Operaciones del sistema:** `planificarMantenimientoDeFlota()`, `aceptarVentanaDeMantenimiento(propuestaId)`, `confirmarVentanaDeTaller(tareaId, ventanaElegida, gastoEstimado)`

```mermaid
sequenceDiagram
    title DSS — CU-105 Planificar el mantenimiento y las habilitaciones de la flota
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor CHO as Chofer (ACT-02)
    actor ADM as Administrador (ACT-03)

    Note over SAU: Se ejecuta una vez por<br/>día, a la hora<br/>configurada
    SAU->>SIS: planificarMantenimientoDeFlota()
    activate SIS
    Note over SIS: Estima el consumo diario<br/>de cada vehículo,<br/>proyecta los<br/>vencimientos y arma las<br/>ventanas que no dejan la<br/>zona bajo el mínimo

    loop Por cada tarea dentro de la ventana de anticipación
        loop Por cada ventana alternativa, de mejor a peor
            SIS-)CHO: notificarPropuestaDeVentana(propuesta)
            opt El chofer acepta
                CHO->>SIS: aceptarVentanaDeMantenimiento(propuestaId)
                SIS-->>CHO: ventana aceptada, pendiente de la confirmación del administrador
            end
            Note over SIS: Si rechaza o vence la<br/>vigencia, se cierra la<br/>propuesta y se pasa a la<br/>siguiente ventana
        end

        opt Se agotaron las ventanas sin acuerdo
            SIS-)ADM: notificarOpcionesEvaluadas(tarea, opciones)
            ADM->>SIS: confirmarVentanaDeTaller(tareaId, ventanaElegida, gastoEstimado)
            SIS-->>ADM: tarea programada
        end
        Note over SIS: Si la ventana quedó acordada<br/>con el chofer, se registra la<br/>tarea como programada
    end

    opt Hay una habilitación bloqueante vencida
        Note over SIS: Deja el vehículo fuera<br/>de servicio
        SIS-)ADM: notificarVehiculoInhabilitado(vehiculo)
    end
    SIS-->>SAU: planificación resuelta
    deactivate SIS
```

**Figura 244 — DSS CU-105: Planificar el mantenimiento y las habilitaciones de la flota**

---

##### DSS — CU-106: Anticipar la recompra por consumo estimado

**Actor:** Cliente (ACT-01), Sistema Automático (ACT-04)
**Operaciones del sistema:** `anticiparRecompras()`, `aceptarInvitacionDeRecompra(invitacionId)`

```mermaid
sequenceDiagram
    title DSS — CU-106 Anticipar la recompra por consumo estimado
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)

    Note over SAU: Se ejecuta una vez por<br/>día
    SAU->>SIS: anticiparRecompras()
    activate SIS
    Note over SIS: Estima el ritmo de<br/>consumo de cada cliente<br/>ponderado por kilaje y<br/>corregido por<br/>estacionalidad, y<br/>proyecta la fecha de<br/>agotamiento

    loop Por cada cliente dentro de la ventana de anticipación
        opt El cliente no tiene pedido activo ni invitación reciente
            SIS-)CLI: notificarInvitacionDeRecompra(invitacion)
            opt El cliente acepta dentro de la vigencia
                CLI->>SIS: aceptarInvitacionDeRecompra(invitacionId)
                SIS-->>CLI: pedido creado y en búsqueda de chofer
            end
            Note over SIS: Si rechaza o vence la<br/>vigencia, se cierra la<br/>invitación y se registra la<br/>fecha del intervalo mínimo
        end
        Note over SIS: Si el cliente está excluido,<br/>no se emite invitación
    end
    SIS-->>SAU: invitaciones emitidas y caducadas procesadas
    deactivate SIS
```

**Figura 245 — DSS CU-106: Anticipar la recompra por consumo estimado**

---

##### DSS — CU-107: Agrupar pedidos por recorrido

**Actor:** Chofer (ACT-02), Sistema Automático (ACT-04)
**Operaciones del sistema:** `agruparPedidosPorRecorrido()`, `aceptarRecorrido(recorridoId)`

```mermaid
sequenceDiagram
    title DSS — CU-107 Agrupar pedidos por recorrido
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor CHO as Chofer (ACT-02)

    Note over SAU: Se ejecuta con la<br/>periodicidad configurada
    SAU->>SIS: agruparPedidosPorRecorrido()
    activate SIS
    Note over SIS: Agrupa por zona,<br/>proximidad, franja<br/>horaria y capacidad de<br/>carga, y ordena las<br/>paradas por secuencia de<br/>entrega

    loop Por cada lote armado
        loop Por cada chofer candidato no contactado
            SIS-)CHO: notificarOfertaDeRecorrido(recorrido)
            opt El chofer acepta dentro de la vigencia
                CHO->>SIS: aceptarRecorrido(recorridoId)
                SIS-->>CHO: pedidos asignados en el orden establecido
            end
            Note over SIS: Si rechaza o vence la<br/>vigencia, se cierra la oferta<br/>y se pasa al candidato<br/>siguiente
        end

        alt Ningún chofer tomó el lote
            SIS-->>SAU: lote deshecho, pedidos al circuito individual
        else El lote quedó asignado
            SIS-->>SAU: recorrido asignado
        end
    end
    SIS-->>SAU: lotes procesados
    deactivate SIS
```

**Figura 246 — DSS CU-107: Agrupar pedidos por recorrido**

---

##### DSS — CU-108: Recuperar envases no devueltos

**Actor:** Cliente (ACT-01), Administrador (ACT-03), Sistema Automático (ACT-04)
**Operaciones del sistema:** `gestionarEnvasesNoDevueltos()`, `aceptarRetiroEnLaEntrega(ofertaId)`, `resolverCasoDeRecupero(casoId, decision)`

```mermaid
sequenceDiagram
    title DSS — CU-108 Recuperar envases no devueltos
    autonumber
    actor SAU as Sistema Automático (ACT-04)
    participant SIS as :Sistema
    actor CLI as Cliente (ACT-01)
    actor ADM as Administrador (ACT-03)

    Note over SAU: Se ejecuta con la<br/>periodicidad configurada
    SAU->>SIS: gestionarEnvasesNoDevueltos()
    activate SIS
    Note over SIS: Detecta los envases<br/>retenidos por encima del<br/>plazo de tolerancia<br/>configurado

    loop Por cada envase retenido
        loop Por cada escalón de la secuencia
            Note over SAU,SIS: Si el envase ya volvió, se cierra<br/>el caso y se libera el depósito
            opt El envase sigue retenido
                SIS-)CLI: notificarEscalonDeRecupero(caso, escalon)
                opt Hay una entrega programada al mismo cliente
                    SIS-)CLI: notificarOfertaDeRetiro(oferta)
                    opt El cliente acepta el retiro antes de la vigencia
                        CLI->>SIS: aceptarRetiroEnLaEntrega(ofertaId)
                        SIS-->>CLI: retiro acordado para esa entrega
                    end
                end
            end
        end

        opt Se agotaron los escalones y el importe supera el umbral
            SIS-)ADM: notificarLegajoDeRecupero(caso)
            ADM->>SIS: resolverCasoDeRecupero(casoId, decision)
            Note over SAU,ADM: decision: cobrar el depósito, dar de baja el<br/>envase o cerrar el caso sin cargo
            SIS-->>ADM: resolución registrada
        end
        Note over SAU,SIS: Si el envase volvió o el importe<br/>no llega al umbral, se cierra<br/>el caso según corresponda
    end
    SIS-->>SAU: casos de recupero procesados
    deactivate SIS
```

**Figura 247 — DSS CU-108: Recuperar envases no devueltos**

---

##### Planificado (I-1) · DSS — CU-043: Modificar Capacidad de Franja Horaria

**Actor:** Administrador (ACT-03)
**Operaciones del sistema:** `modificarFranjaHoraria(franjaId, nombre, horaInicio, horaFin, capacidad)`

> Caso de uso planificado (I-1): el sistema no expone una operación de modificación de la
> franja horaria. El diagrama especifica el comportamiento esperado.

```mermaid
sequenceDiagram
    title DSS — CU-043 Modificar Capacidad de Franja Horaria
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SIS as :Sistema

    ADM->>SIS: modificarFranjaHoraria(franjaId, nombre, horaInicio, horaFin, capacidad)
    activate SIS
    alt Los datos son válidos y la franja pertenece a la distribuidora
        SIS-->>ADM: franja actualizada (nombre, rango horario, capacidad)
    else La capacidad nueva es menor que los pedidos ya programados
        SIS-->>ADM: franja actualizada, con la advertencia de las fechas sobrecargadas
    else La hora de fin no es posterior a la de inicio
        SIS-->>ADM: rechazo (rango horario inválido)
    else La franja pertenece a otra distribuidora
        SIS-->>ADM: rechazo (franja no encontrada)
    end
    deactivate SIS
```

**Figura 248 — DSS CU-043: Modificar Capacidad de Franja Horaria**

---

### 2.2 Contratos de Operaciones del Sistema

Un contrato describe el efecto de una operación del sistema sobre el modelo conceptual de §1. Sus **postcondiciones** se expresan en esos términos: la instancia que se creó o se eliminó, la asociación que se formó o se rompió, el atributo que se modificó. Hay un contrato por cada operación que cambia el estado del sistema.

#### Catálogo de operaciones del sistema

Una operación del sistema es un mensaje que un actor le manda al sistema y que aparece como tal en un diagrama de secuencia de §2.1. El catálogo reúne **todas** las operaciones, cada una con una única firma: la que usan los diagramas de secuencia de §2.1, los contratos de esta sección y los diagramas de interacción del Documento 3. Los parámetros llevan su tipo; los diagramas de secuencia usan la misma firma sin los tipos, para no recargar el dibujo.

Son **312 operaciones**. **197** modifican el modelo conceptual y tienen contrato; las **115** restantes no modifican nada y por eso no llevan contrato.

| Operación | Casos de uso | Actor iniciador | Cambia estado |
|---|---|---|---|
| `abrirCaja(cajaId identificador, montoInicial moneda)` | CU-226 | Administrador (ACT-03) | Sí |
| `aceptarInvitacionDeRecompra(invitacionId identificador)` | CU-106 | Cliente (ACT-01) | Sí |
| `aceptarPedido(pedidoId identificador)` | CU-015 | Chofer (ACT-02) | Sí |
| `aceptarRecorrido(recorridoId identificador)` | CU-107 | Chofer (ACT-02) | Sí |
| `aceptarRetiroEnLaEntrega(ofertaId identificador)` | CU-108 | Cliente (ACT-01) | Sí |
| `aceptarVentanaDeMantenimiento(propuestaId identificador)` | CU-105 | Chofer (ACT-02) | Sí |
| `activarReservasDelDia()` | CU-075 | Sistema Automático (ACT-04) | Sí |
| `actualizarConsumoPromedio(cantidadPorMes decimal)` | CU-144 | Cliente (ACT-01) | Sí |
| `actualizarDeposito(depositoId identificador, datos registro)` | CU-259 | Administrador (ACT-03) | Sí |
| `actualizarPerfil(usuarioId identificador, datos registro)` | CU-251 | Cliente (ACT-01), Chofer (ACT-02) | Sí |
| `actualizarPerfilDelChofer(choferId identificador, datos registro)` | CU-096 | Administrador (ACT-03) | Sí |
| `actualizarProducto(productoId identificador, datos registro)` | CU-037, CU-039 | Administrador (ACT-03) | Sí |
| `actualizarProveedor(proveedorId identificador, datos registro)` | CU-262 | Administrador (ACT-03) | Sí |
| `actualizarRol(rolId identificador, datos registro)` | CU-253 | Administrador General (ACT-05) | Sí |
| `actualizarStock(productoId identificador, variacion entero)` | CU-038 | Administrador (ACT-03) | Sí |
| `actualizarUbicacion(usuarioId identificador, latitud decimal, longitud decimal)` | CU-017 | Chofer (ACT-02) | Sí |
| `actualizarUbicacionDelCliente(clienteId identificador, coordenadas coordenada)` | CU-094 | Cliente (ACT-01) | Sí |
| `adjuntarArchivoALaTarea(tareaId identificador, archivo archivo)` | CU-155 | Administrador (ACT-03) | Sí |
| `adjuntarArchivoAlLegajo(empleadoId identificador, archivo archivo, etiqueta cadena)` | CU-186 | Administrador (ACT-03) | Sí |
| `adjuntarFotoAlReclamo(reclamoId identificador, imagen archivo)` | CU-174 | Cliente (ACT-01) | Sí |
| `agregarItemAlCarrito(productoId identificador, cantidad entero)` | CU-122 | Cliente (ACT-01) | Sí |
| `agruparPedidosPorRecorrido()` | CU-107 | Sistema Automático (ACT-04) | Sí |
| `ajustarSaldoDelChofer(choferId identificador, monto moneda)` | CU-049 | Administrador (ACT-03) | Sí |
| `anticiparRecompras()` | CU-106 | Sistema Automático (ACT-04) | Sí |
| `anularCargaDeCombustible(cargaId identificador)` | CU-195 | Administrador (ACT-03) | Sí |
| `anularLiquidacion(liquidacionId identificador)` | CU-242 | Administrador (ACT-03) | Sí |
| `anularMovimientoDeCaja(movimientoId identificador, motivo cadena)` | CU-229 | Administrador (ACT-03) | Sí |
| `anularMultaDeTransito(multaId identificador, motivo cadena)` | CU-198 | Administrador (ACT-03) | Sí |
| `anularRecepcionDeCompra(recepcionId identificador, motivo cadena)` | CU-217 | Administrador (ACT-03) | Sí |
| `aprobarLicencia(licenciaId identificador)` | CU-192 | Administrador (ACT-03) | Sí |
| `aprobarLiquidacion(liquidacionId identificador)` | CU-242 | Administrador (ACT-03) | Sí |
| `aprobarRendicion(rendicionId identificador, cajaDestinoId identificador, resolucionDeDiferencia cadena)` | CU-233 | Administrador (ACT-03) | Sí |
| `asignarChoferAPedido(pedidoId identificador, choferId identificador)` | CU-012 | Administrador (ACT-03) | Sí |
| `asignarEnvasesAPedido(pedidoId identificador, numerosDeSerie lista)` | CU-068 | Chofer (ACT-02) | Sí |
| `avisarLlegada(pedidoId identificador)` | CU-019 | Chofer (ACT-02) | No |
| `avisarMultasPorVencer()` | CU-198 | Sistema Automático (ACT-04) | Sí |
| `avisarRendicionesSinCerrar()` | CU-234 | Sistema Automático (ACT-04) | Sí |
| `avisarStockBajo()` | CU-211 | Sistema Automático (ACT-04) | Sí |
| `avisarVencimientosPendientes()` | CU-142, CU-188 | Sistema Automático (ACT-04) | Sí |
| `bloquearUsuario(usuarioId identificador, bloquear booleano)` | CU-050, CU-270 | Administrador (ACT-03) | Sí |
| `buscarAdministrador(termino cadena)` | CU-088 | Administrador (ACT-03) | No |
| `buscarChoferPorUsuario(usuarioId identificador)` | CU-110 | Administrador (ACT-03) | No |
| `buscarClientePorUsuario(usuarioId identificador)` | CU-130 | Administrador (ACT-03) | No |
| `buscarUsuarioPorCorreo(correo cadena)` | CU-272 | Administrador (ACT-03) | No |
| `buscarUsuarioPorTelefono(telefono cadena)` | CU-272 | Administrador (ACT-03) | No |
| `buscarVehiculoPorPatente(patente cadena)` | CU-051, CU-114 | Administrador (ACT-03) | No |
| `calificarPedido(pedidoId identificador, estrellas entero, comentario cadena)` | CU-064 | Cliente (ACT-01) | Sí |
| `cambiarCorreo(correoActual cadena, correoNuevo cadena)` | CU-047 | Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03) | Sí |
| `cambiarDireccionDeEntrega(pedidoId identificador, direccionId identificador, motivo cadena)` | CU-127 | Cliente (ACT-01) | Sí |
| `cambiarDisponibilidad(usuarioId identificador, disponible booleano)` | CU-022, CU-266 | Chofer (ACT-02) | Sí |
| `cambiarEstadoDelChofer(choferId identificador, activo booleano)` | CU-033, CU-267 | Administrador (ACT-03) | Sí |
| `cancelarCargaDelCamion(cargaId identificador)` | CU-218 | Administrador (ACT-03) | Sí |
| `cancelarLicencia(licenciaId identificador)` | CU-191 | Administrador (ACT-03) | Sí |
| `cancelarOrdenDeCompra(ordenId identificador, motivo cadena)` | CU-216 | Administrador (ACT-03) | Sí |
| `cancelarPedido(pedidoId identificador, motivo cadena)` | CU-008, CU-010 | Cliente (ACT-01), Administrador (ACT-03) | Sí |
| `cancelarPedidoForzado(pedidoId identificador)` | CU-010 | Administrador (ACT-03) | Sí |
| `cerrarCajaConArqueo(sesionId identificador, montoContado moneda)` | CU-227 | Administrador (ACT-03) | Sí |
| `cerrarRendicionDeStock(cargaId identificador, nota cadena)` | CU-222 | Administrador (ACT-03) | Sí |
| `cerrarSiniestro(siniestroId identificador, costoDeReparacion moneda, reintegroDelSeguro moneda, franquicia moneda)` | CU-202 | Administrador (ACT-03) | Sí |
| `cerrarTareaDeFlota(tareaId identificador, fecha fecha, kilometraje entero, costo moneda, observacion cadena)` | CU-141 | Administrador (ACT-03) | Sí |
| `conciliarStock()` | CU-224 | Sistema Automático (ACT-04) | Sí |
| `configurarControlDeCargaAbierta(exigirCargaDeCamionAbierta booleano)` | CU-249 | Administrador (ACT-03) | Sí |
| `configurarDiasDeAviso(dias entero)` | CU-145 | Cliente (ACT-01) | Sí |
| `configurarFrecuenciaDeTareas(intervalos registro)` | CU-173 | Administrador (ACT-03) | Sí |
| `configurarParametrosDeDespacho(radiosKm lista, ventanaDeAceptacion entero)` | CU-171 | Administrador (ACT-03) | Sí |
| `configurarParametrosDeProceso(proceso cadena, parametros registro)` | CU-172 | Administrador (ACT-03) | Sí |
| `configurarStockMinimo(depositoId identificador, minimos lista)` | CU-210 | Administrador (ACT-03) | Sí |
| `confirmarEntrega(pedidoId identificador)` | CU-020 | Chofer (ACT-02) | Sí |
| `confirmarEntregaConCodigo(pedidoId identificador, codigo cadena)` | CU-079 | Cliente (ACT-01) | Sí |
| `confirmarSenia(pedidoId identificador)` | CU-074 | Administrador (ACT-03) | Sí |
| `confirmarVentanaDeTaller(tareaId identificador, ventanaElegida registro, gastoEstimado moneda)` | CU-105 | Administrador (ACT-03) | Sí |
| `consultarAdjuntosDeLaTarea(tareaId identificador)` | CU-156 | Administrador (ACT-03) | No |
| `consultarAjustesDeStock(desde fechaHora, hasta fechaHora, motivo cadena)` | CU-213 | Administrador (ACT-03) | No |
| `consultarAntiguedadDeDeuda()` | CU-239 | Administrador (ACT-03) | No |
| `consultarAsistencias(desde fecha, hasta fecha)` | CU-189 | Administrador (ACT-03) | No |
| `consultarAuditoria(autor identificador, tipoDeRecurso cadena, recurso cadena, desde fechaHora, hasta fechaHora, resultado cadena, limite entero, desplazamiento entero)` | CU-152 | Administrador (ACT-03) | No |
| `consultarAuditoriaDeDatos(entidad cadena, registro cadena, autor identificador, tipoDeAccion entero, desde fechaHora, hasta fechaHora, pagina entero, limite entero)` | CU-152 | Administrador (ACT-03), Administrador General (ACT-05) | No |
| `consultarCargaActual()` | CU-223 | Chofer (ACT-02) | No |
| `consultarCargasDeCombustible(filtros registro)` | CU-195 | Administrador (ACT-03) | No |
| `consultarCargasDelCamion(estado cadena, fecha fecha, vehiculoId identificador, choferId identificador)` | CU-218 | Administrador (ACT-03) | No |
| `consultarCarrito()` | CU-125 | Cliente (ACT-01) | No |
| `consultarCatalogo(pagina entero, limite entero, distribuidora cadena)` | CU-041 | Cliente (ACT-01) | No |
| `consultarConciliacionDeStock()` | CU-224 | Administrador (ACT-03) | No |
| `consultarConsumoDeCombustible(vehiculoId identificador, fechaDesde fecha, fechaHasta fecha)` | CU-196 | Administrador (ACT-03) | No |
| `consultarCostoDeUnVehiculo(vehiculoId identificador, fechaDesde fecha, fechaHasta fecha)` | CU-203 | Administrador (ACT-03) | No |
| `consultarDepositos()` | CU-207 | Administrador (ACT-03) | No |
| `consultarDetalleDelChofer(choferId identificador)` | CU-035, CU-109 | Administrador (ACT-03) | No |
| `consultarDetalleDelCliente(clienteId identificador)` | CU-129 | Administrador (ACT-03) | No |
| `consultarDetalleDelVehiculo(vehiculoId identificador)` | CU-113 | Administrador (ACT-03) | No |
| `consultarDireccionDeEntrega(direccionId identificador)` | CU-117 | Cliente (ACT-01) | No |
| `consultarDireccionesDeEntrega(usuarioId identificador)` | CU-046 | Cliente (ACT-01) | No |
| `consultarDireccionPredeterminada(usuarioId identificador)` | CU-121 | Cliente (ACT-01) | No |
| `consultarDisponibilidadDeFranjas(fecha fecha, distribuidora cadena)` | CU-044, CU-045 | Cliente (ACT-01) | No |
| `consultarDistribuidora(distribuidoraId identificador)` | CU-053 | Administrador General (ACT-05) | No |
| `consultarDocumentacionDelEmpleado(empleadoId identificador)` | CU-187 | Administrador (ACT-03) | No |
| `consultarEmpleado(empleadoId identificador)` | CU-179 | Administrador (ACT-03), Administrador General (ACT-05) | No |
| `consultarEmpleados(filtros registro)` | CU-180 | Administrador (ACT-03), Administrador General (ACT-05) | No |
| `consultarEnvase(envaseId identificador)` | CU-069 | Administrador (ACT-03) | No |
| `consultarEnvasesProximosAVencer(dias entero)` | CU-134 | Administrador (ACT-03) | No |
| `consultarEstadoDeCuenta(cuentaId identificador, fechaDesde fecha, fechaHasta fecha)` | CU-238 | Administrador (ACT-03) | No |
| `consultarEvolucionDeVentas(fechaDesde fecha, fechaHasta fecha, granularidad cadena)` | CU-030 | Administrador (ACT-03) | No |
| `consultarFotoDelReclamo(reclamoId identificador)` | CU-175 | Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05) | No |
| `consultarFranjasHorarias()` | CU-154 | Administrador (ACT-03) | No |
| `consultarGraficoDeVentas()` | CU-026 | Administrador (ACT-03) | No |
| `consultarHistorialDeCalificaciones(usuarioId identificador)` | CU-066 | Administrador (ACT-03) | No |
| `consultarHistorialDeChoferesDelVehiculo(vehiculoId identificador, pagina entero)` | CU-165 | Administrador (ACT-03) | No |
| `consultarHistorialDeEstados(pedidoId identificador)` | CU-170 | Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05) | No |
| `consultarHistorialDelEnvase(envaseId identificador)` | CU-071 | Administrador (ACT-03) | No |
| `consultarHistorialDePedidos(clienteId identificador, pagina entero, limite entero)` | CU-007 | Cliente (ACT-01) | No |
| `consultarHistorialDeVehiculosDelChofer(choferId identificador, pagina entero)` | CU-164 | Administrador (ACT-03) | No |
| `consultarIncidenciasDelPedido(pedidoId identificador)` | CU-062 | Chofer (ACT-02) | No |
| `consultarLicencias(estado cadena, desde fecha, hasta fecha)` | CU-192 | Administrador (ACT-03) | No |
| `consultarMisComisiones(fechaDesde fecha, fechaHasta fecha)` | CU-244 | Chofer (ACT-02) | No |
| `consultarMiVehiculoEnUso()` | CU-163 | Chofer (ACT-02) | No |
| `consultarModalidadesDeEntrega(direccionId identificador)` | CU-148 | Cliente (ACT-01) | No |
| `consultarMovimientosDeStock(productoId identificador, ubicacionId identificador, motivo cadena, desde fechaHora, hasta fechaHora, pagina entero)` | CU-209 | Administrador (ACT-03) | No |
| `consultarMultasDeTransito(filtros registro)` | CU-198 | Administrador (ACT-03) | No |
| `consultarOrdenesDeCompra(estado cadena, proveedorId identificador, desde fechaHora, hasta fechaHora)` | CU-215 | Administrador (ACT-03) | No |
| `consultarPedido(pedidoId identificador)` | CU-006 | Cliente (ACT-01) | No |
| `consultarPedidosAsignados(choferId identificador, pagina entero, limite entero)` | CU-081 | Chofer (ACT-02) | No |
| `consultarPedidosDisponibles(pagina entero, limite entero)` | CU-080 | Chofer (ACT-02) | No |
| `consultarPerfil(usuarioId identificador)` | CU-004 | Cliente (ACT-01) | No |
| `consultarPerfilCliente(usuarioId identificador)` | CU-004 | Cliente (ACT-01) | No |
| `consultarPerfilDelChofer(usuarioId identificador)` | CU-049 | Chofer (ACT-02) | No |
| `consultarProducto(productoId identificador)` | CU-041 | Cliente (ACT-01) | No |
| `consultarProductosDisponibles(distribuidora cadena)` | CU-041 | Cliente (ACT-01) | No |
| `consultarProductosInactivos()` | CU-269 | Administrador (ACT-03) | No |
| `consultarProveedores(termino cadena)` | CU-214 | Administrador (ACT-03) | No |
| `consultarPuestosDeTrabajo()` | CU-176 | Administrador (ACT-03) | No |
| `consultarRecepcionesDeCompra(proveedorId identificador, desde fechaHora, hasta fechaHora, estadoDePago cadena)` | CU-217 | Administrador (ACT-03) | No |
| `consultarRecomprasEstimadas(dias entero)` | CU-146 | Administrador (ACT-03) | No |
| `consultarResumenDeCalificaciones(usuarioId identificador)` | CU-065 | Cliente (ACT-01) | No |
| `consultarResumenDePedidos()` | CU-026 | Administrador (ACT-03) | No |
| `consultarResumenDeStock()` | CU-208 | Administrador (ACT-03) | No |
| `consultarSaldoDeVacaciones(empleadoId identificador, anio entero)` | CU-193 | Administrador (ACT-03) | No |
| `consultarSiniestros(filtros registro)` | CU-201 | Administrador (ACT-03) | No |
| `consultarStockPorUbicacion(ubicacionId identificador, productoId identificador)` | CU-208 | Administrador (ACT-03) | No |
| `consultarTableroDeCostosDeLaFlota(fechaDesde fecha, fechaHasta fecha)` | CU-204 | Administrador (ACT-03) | No |
| `consultarTableroDePersonal()` | CU-194 | Administrador (ACT-03) | No |
| `consultarTableroFinanciero(fecha fecha)` | CU-245 | Administrador (ACT-03) | No |
| `consultarTokensDelUsuario(usuarioId identificador)` | CU-099 | Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05) | No |
| `consultarVehiculoEnUso(choferId identificador)` | CU-163 | Administrador (ACT-03) | No |
| `consultarVehiculosDelChofer(usuarioId identificador)` | CU-115 | Administrador (ACT-03) | No |
| `consultarVencimientosDeLaFlota(dias entero)` | CU-139 | Administrador (ACT-03) | No |
| `consultarVencimientosDelPersonal(dias entero, categoria cadena)` | CU-187 | Administrador (ACT-03) | No |
| `consultarVentasPorChofer(fechaDesde fecha, fechaHasta fecha)` | CU-027 | Administrador (ACT-03) | No |
| `consultarVentasPorMetodoDePago(fechaDesde fecha, fechaHasta fecha)` | CU-029 | Administrador (ACT-03) | No |
| `consultarVentasPorProducto(fechaDesde fecha, fechaHasta fecha)` | CU-028 | Administrador (ACT-03) | No |
| `consultarVigenciaDelEnvase(envaseId identificador)` | CU-133 | Administrador (ACT-03) | No |
| `corregirAsistencia(asistenciaId identificador, datos registro, nota cadena)` | CU-189 | Administrador (ACT-03) | Sí |
| `crearCaja(nombre cadena, tipo cadena, requiereSesion booleano)` | CU-225 | Administrador (ACT-03) | Sí |
| `crearCategoriaDeCaja(nombre cadena, sentido cadena)` | CU-230 | Administrador (ACT-03) | Sí |
| `crearFranjaHoraria(nombre cadena, horaInicio hora, horaFin hora, capacidad entero)` | CU-042 | Administrador (ACT-03) | Sí |
| `crearPedido(items lista, direccionId identificador, franjaId identificador, fechaAgendada fecha, metodoDePago cadena)` | CU-005, CU-044 | Cliente (ACT-01) | Sí |
| `crearPrimerSuperAdministrador(nombreCompleto cadena, correo cadena, telefono cadena, contrasena cadena)` | CU-087 | Administrador General (ACT-05) | Sí |
| `crearProducto(tipo cadena, peso decimal, precio moneda, stockInicial entero, descripcion cadena, promociones lista)` | CU-036 | Administrador (ACT-03) | Sí |
| `crearPuestoDeTrabajo(nombre cadena, categoria cadena)` | CU-255 | Administrador (ACT-03) | Sí |
| `crearReglaDeComision(empleadoId identificador, productoId identificador, base cadena, valor decimal, vigenteDesde fecha)` | CU-240 | Administrador (ACT-03) | Sí |
| `crearReserva(items lista, direccionId identificador, fechaAgendada fecha, franjaId identificador, metodoDePago cadena, montoDeLaSenia moneda)` | CU-072 | Cliente (ACT-01) | Sí |
| `crearRol(tipo cadena)` | CU-252 | Administrador General (ACT-05) | Sí |
| `crearTareaDeFlota(planId identificador, recursoId identificador, vencimiento fecha, detalle registro)` | CU-136, CU-137, CU-138, CU-140, CU-197 | Administrador (ACT-03) | Sí |
| `crearTareaDelEmpleado(empleadoId identificador, planId identificador, vencimiento fecha, detalle registro)` | CU-183, CU-184, CU-185 | Administrador (ACT-03) | Sí |
| `darDeAltaEnvase(numeroDeSerie cadena, tipoDeProducto cadena, deposito cadena)` | CU-067 | Administrador (ACT-03) | Sí |
| `darDeBajaDeposito(depositoId identificador)` | CU-260 | Administrador (ACT-03) | Sí |
| `darDeBajaDistribuidora(distribuidoraId identificador)` | CU-055 | Administrador General (ACT-05) | Sí |
| `darDeBajaProveedor(proveedorId identificador)` | CU-263 | Administrador (ACT-03) | Sí |
| `declararConsumoPromedio(tipoGarrafa cadena, cantidadPorMes decimal)` | CU-143 | Cliente (ACT-01) | Sí |
| `declararEfectivoRendido(rendicionId identificador, efectivoDeclarado moneda, gastos lista)` | CU-232 | Chofer (ACT-02), Administrador (ACT-03) | Sí |
| `definirZonaDeCobertura(nombre cadena, poligono poligono, recargo moneda, activa booleano)` | CU-056 | Administrador (ACT-03) | Sí |
| `desactivarProducto(productoId identificador)` | CU-040 | Administrador (ACT-03) | Sí |
| `desactivarZonasVencidas()` | CU-151 | Sistema Automático (ACT-04) | Sí |
| `descargarAdjunto(tareaId identificador, adjuntoId identificador)` | CU-157 | Administrador (ACT-03) | No |
| `descontarStockDeLaEntrega(pedidoId identificador)` | CU-220 | Sistema Automático (ACT-04) | Sí |
| `despacharPedidoExpress(pedidoId identificador)` | CU-149 | Sistema Automático (ACT-04) | Sí |
| `editarDatosDelCliente(clienteId identificador, cambios registro)` | CU-131 | Administrador (ACT-03) | Sí |
| `editarDireccionDeEntrega(direccionId identificador, cambios registro)` | CU-046, CU-118 | Cliente (ACT-01) | Sí |
| `editarVehiculo(vehiculoId identificador, datos registro)` | CU-051, CU-111 | Administrador (ACT-03) | Sí |
| `eliminarAdjunto(tareaId identificador, adjuntoId identificador)` | CU-158 | Administrador (ACT-03) | Sí |
| `eliminarChofer(choferId identificador)` | CU-097 | Administrador (ACT-03) | Sí |
| `eliminarCliente(clienteId identificador)` | CU-095 | Administrador General (ACT-05) | Sí |
| `eliminarDireccionDeEntrega(direccionId identificador)` | CU-046, CU-119 | Cliente (ACT-01) | Sí |
| `eliminarEmpleado(empleadoId identificador)` | CU-178 | Administrador (ACT-03) | Sí |
| `eliminarFranjaHoraria(franjaId identificador)` | CU-103 | Administrador (ACT-03) | Sí |
| `eliminarPuestoDeTrabajo(puestoId identificador)` | CU-257 | Administrador (ACT-03) | Sí |
| `eliminarRol(rolId identificador)` | CU-254 | Administrador General (ACT-05) | Sí |
| `eliminarUsuario(usuarioId identificador)` | CU-085 | Administrador (ACT-03) | Sí |
| `eliminarVehiculo(vehiculoId identificador)` | CU-051, CU-112 | Administrador (ACT-03) | Sí |
| `eliminarZonaDeCobertura(zonaId identificador)` | CU-059 | Administrador (ACT-03) | Sí |
| `emitirOrdenDeCompra(proveedorId identificador, depositoId identificador, items lista, fechaEsperada fecha)` | CU-215 | Administrador (ACT-03) | Sí |
| `enviarNotificacionDePrueba(token cadena, titulo cadena, mensaje cadena)` | CU-100 | Administrador General (ACT-05) | No |
| `enviarOrdenDeCompra(ordenId identificador)` | CU-215 | Administrador (ACT-03) | Sí |
| `expirarPedidosSinPagar()` | CU-077 | Sistema Automático (ACT-04) | Sí |
| `expirarReservasSinSenia()` | CU-076 | Sistema Automático (ACT-04) | Sí |
| `generarRendicionesDelDia()` | CU-231 | Sistema Automático (ACT-04) | Sí |
| `gestionarEnvasesNoDevueltos()` | CU-108 | Sistema Automático (ACT-04) | Sí |
| `habilitarCuentaCorriente(clienteId identificador, razonSocial cadena, cuit cadena, condicionFiscal cadena, limiteDeCredito moneda, plazoEnDias entero)` | CU-235 | Administrador (ACT-03) | Sí |
| `imputarMultaAlChofer(multaId identificador, empleadoId identificador)` | CU-200 | Administrador (ACT-03) | Sí |
| `indicarQuienRecibe(pedidoId identificador, nombre cadena, documento cadena, relacion cadena)` | CU-128 | Cliente (ACT-01) | Sí |
| `iniciarSesion(correo cadena, contrasena cadena)` | CU-001 | Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03) | No |
| `invalidarChofer(choferId identificador)` | CU-271 | Administrador (ACT-03) | Sí |
| `liberarPedido(pedidoId identificador, motivo cadena)` | CU-009 | Chofer (ACT-02) | Sí |
| `liberarVehiculoEnUso(choferId identificador)` | CU-162 | Administrador (ACT-03) | Sí |
| `liquidarComisionesDelChofer(empleadoId identificador, fechaDesde fecha, fechaHasta fecha)` | CU-242 | Administrador (ACT-03) | Sí |
| `listarAdministradores()` | CU-088 | Administrador (ACT-03) | No |
| `listarChoferes(pagina entero, limite entero)` | CU-035 | Administrador (ACT-03) | No |
| `listarChoferesActivos(pagina entero, limite entero)` | CU-035 | Administrador (ACT-03) | No |
| `listarClientes(pagina entero, limite entero)` | CU-092 | Administrador (ACT-03) | No |
| `listarDistribuidoras()` | CU-053 | Administrador General (ACT-05) | No |
| `listarEnvases(estado cadena)` | CU-069 | Administrador (ACT-03) | No |
| `listarFranjas(distribuidora cadena)` | CU-045 | Cliente (ACT-01) | No |
| `listarIncidencias()` | CU-061 | Administrador (ACT-03) | No |
| `listarPedidos(pagina entero, limite entero)` | CU-011 | Administrador (ACT-03) | No |
| `listarReclamos()` | CU-024 | Administrador (ACT-03) | No |
| `listarReservas()` | CU-073 | Administrador (ACT-03) | No |
| `listarRoles()` | CU-089 | Administrador General (ACT-05) | No |
| `listarUsuarios(pagina entero, limite entero, textoDeBusqueda cadena)` | CU-083 | Administrador (ACT-03) | No |
| `listarVehiculos()` | CU-051 | Administrador (ACT-03) | No |
| `listarZonasDeCobertura()` | CU-057 | Administrador (ACT-03) | No |
| `marcarDireccionPredeterminada(direccionId identificador)` | CU-046, CU-120 | Cliente (ACT-01) | Sí |
| `marcarPedidoEnCamino(pedidoId identificador)` | CU-018 | Chofer (ACT-02) | Sí |
| `modificarCaja(cajaId identificador, datos registro)` | CU-264 | Administrador (ACT-03) | Sí |
| `modificarCantidadDelItem(itemId identificador, cantidad entero)` | CU-123 | Cliente (ACT-01) | Sí |
| `modificarCargaDeCombustible(cargaId identificador, datos registro)` | CU-195 | Administrador (ACT-03) | Sí |
| `modificarCategoriaDeCaja(categoriaId identificador, datos registro)` | CU-265 | Administrador (ACT-03) | Sí |
| `modificarCuentaCorriente(cuentaId identificador, datos registro)` | CU-235 | Administrador (ACT-03) | Sí |
| `modificarDistribuidora(distribuidoraId identificador, datos registro)` | CU-054 | Administrador General (ACT-05) | Sí |
| `modificarEmpleado(empleadoId identificador, datos registro)` | CU-178 | Administrador (ACT-03) | Sí |
| `modificarFranjaHoraria(franjaId identificador, nombre cadena, horaInicio hora, horaFin hora, capacidad entero)` | CU-043 | Administrador (ACT-03) | Sí |
| `modificarLicencia(licenciaId identificador, datos registro)` | CU-191 | Administrador (ACT-03) | Sí |
| `modificarMultaDeTransito(multaId identificador, datos registro)` | CU-198 | Administrador (ACT-03) | Sí |
| `modificarPuestoDeTrabajo(puestoId identificador, datos registro)` | CU-256 | Administrador (ACT-03) | Sí |
| `modificarReglaDeComision(reglaId identificador, datos registro)` | CU-240 | Administrador (ACT-03) | Sí |
| `modificarSiniestro(siniestroId identificador, datos registro)` | CU-201 | Administrador (ACT-03) | Sí |
| `notificarResultadoDePago(tipoDeNotificacion cadena, identificadorDelPago cadena, firma cadena)` | CU-048 | MercadoPago (ACT-06) | Sí |
| `obtenerCodigoDeEntrega(pedidoId identificador)` | CU-078 | Chofer (ACT-02) | No |
| `ofrecerAlSiguienteChofer(pedidoId identificador)` | CU-013 | Sistema Automático (ACT-04) | Sí |
| `otorgarCuentaDeAcceso(empleadoId identificador, datosDeAcceso registro)` | CU-182 | Administrador (ACT-03) | Sí |
| `pagarLiquidacion(liquidacionId identificador, cajaId identificador)` | CU-243 | Administrador (ACT-03) | Sí |
| `planificarMantenimientoDeFlota()` | CU-105 | Sistema Automático (ACT-04) | Sí |
| `ponerVehiculoEnUso(choferId identificador, vehiculoId identificador, nota cadena)` | CU-161 | Administrador (ACT-03) | Sí |
| `probarServicioDeCorreo(destinatario cadena)` | CU-102 | Administrador General (ACT-05) | No |
| `programarVigenciaDeZona(zonaId identificador, vigenteHasta fechaHora)` | CU-150 | Administrador (ACT-03) | Sí |
| `quitarItemDelCarrito(itemId identificador)` | CU-124 | Cliente (ACT-01) | Sí |
| `reabrirReclamo(reclamoId identificador, motivo cadena)` | CU-167 | Administrador (ACT-03) | Sí |
| `reabrirRendicion(rendicionId identificador)` | CU-233 | Administrador (ACT-03) | Sí |
| `reactivarProducto(productoId identificador)` | CU-268 | Administrador (ACT-03) | Sí |
| `reactivarVehiculo(vehiculoId identificador)` | CU-247 | Administrador (ACT-03) | Sí |
| `realizarCompraExpress(tipoGarrafa cadena, medioDePago cadena)` | CU-147 | Cliente (ACT-01) | Sí |
| `rechazarLicencia(licenciaId identificador, motivo cadena)` | CU-192 | Administrador (ACT-03) | Sí |
| `rechazarOferta(pedidoId identificador)` | CU-016 | Chofer (ACT-02) | Sí |
| `reenviarConfirmacionDePedido(usuarioId identificador, pedidoId identificador)` | CU-101 | Administrador General (ACT-05) | No |
| `registrarAdministrador(nombreCompleto cadena, correo cadena, telefono cadena, contrasena cadena, rol cadena, distribuidoraId identificador)` | CU-086 | Administrador (ACT-03) | Sí |
| `registrarAjusteDeCuentaCorriente(cuentaId identificador, tipo cadena, importe moneda, motivo cadena)` | CU-237 | Administrador (ACT-03) | Sí |
| `registrarAjusteDeStock(ubicacionId identificador, motivo cadena, nota cadena, items lista)` | CU-213 | Administrador (ACT-03) | Sí |
| `registrarAsistencia(empleadoId identificador, ingreso fechaHora, egreso fechaHora)` | CU-189 | Administrador (ACT-03) | Sí |
| `registrarAuditoriaDeDato(autor identificador, ip cadena, distribuidoraId identificador, entidad cadena, registro cadena, tipoDeAccion entero, detalles lista)` | CU-153 | Sistema Automático (ACT-04) | Sí |
| `registrarCambioDeEstado(pedidoId identificador, estadoAnterior cadena, estadoNuevo cadena, autor identificador, motivo cadena)` | CU-169 | Sistema Automático (ACT-04) | Sí |
| `registrarCargaDeCombustible(vehiculoId identificador, datos registro)` | CU-195 | Chofer (ACT-02), Administrador (ACT-03) | Sí |
| `registrarCargaDelCamion(vehiculoId identificador, depositoId identificador, ayudanteId identificador, items lista)` | CU-218 | Administrador (ACT-03) | Sí |
| `registrarCargoDeCuentaCorriente(pedidoId identificador)` | CU-236 | Sistema Automático (ACT-04) | Sí |
| `registrarChofer(datosPersonales registro, datosDelChofer registro, distribuidoraId identificador)` | CU-003, CU-031 | Administrador (ACT-03) | Sí |
| `registrarComisionDeEntrega(pedidoId identificador)` | CU-241 | Sistema Automático (ACT-04) | Sí |
| `registrarDeposito(nombre cadena, codigo cadena, tipo cadena, direccion cadena)` | CU-258 | Administrador (ACT-03) | Sí |
| `registrarDireccionDeEntrega(datos registro)` | CU-046, CU-116 | Cliente (ACT-01) | Sí |
| `registrarDistribuidora(nombre cadena, identificadorCorto cadena, razonSocial cadena, cuit cadena, correo cadena, telefono cadena, logo archivo, plan cadena)` | CU-052 | Administrador General (ACT-05) | Sí |
| `registrarEgresoDelEmpleado(empleadoId identificador, fechaDeEgreso fecha, motivo cadena)` | CU-181 | Administrador (ACT-03) | Sí |
| `registrarEmpleado(datos registro)` | CU-177 | Administrador (ACT-03) | Sí |
| `registrarFinDeJornada()` | CU-190 | Chofer (ACT-02) | Sí |
| `registrarIncidencia(pedidoId identificador, tipo cadena, descripcion cadena, foto archivo)` | CU-060 | Chofer (ACT-02) | Sí |
| `registrarInicioDeJornada()` | CU-190 | Chofer (ACT-02) | Sí |
| `registrarLicencia(empleadoId identificador, tipo cadena, desde fecha, hasta fecha, motivo cadena)` | CU-191 | Administrador (ACT-03) | Sí |
| `registrarMovimientoDeCaja(cajaId identificador, sentido cadena, importe moneda, categoriaId identificador, medio cadena, descripcion cadena)` | CU-228 | Administrador (ACT-03) | Sí |
| `registrarMovimientoDeEnvase(envaseId identificador, estadoDestino cadena, pedidoId identificador, observacion cadena)` | CU-070 | Chofer (ACT-02) | Sí |
| `registrarMovimientoDeNeumatico(neumaticoId identificador, datos registro)` | CU-206 | Administrador (ACT-03) | Sí |
| `registrarMultaDeTransito(vehiculoId identificador, datos registro)` | CU-198 | Administrador (ACT-03) | Sí |
| `registrarNeumatico(datos registro)` | CU-205 | Administrador (ACT-03) | Sí |
| `registrarOperacion(autor identificador, rol cadena, distribuidoraId identificador, operacion cadena, recurso cadena, origen cadena, resultado cadena, codigo cadena, motivo cadena)` | CU-153 | Sistema Automático (ACT-04) | Sí |
| `registrarPagoDeCuentaCorriente(cuentaId identificador, importe moneda, medio cadena, cajaId identificador)` | CU-237 | Chofer (ACT-02), Administrador (ACT-03) | Sí |
| `registrarPagoDeMulta(multaId identificador, fechaDePago fechaHora, importePagado moneda)` | CU-199 | Administrador (ACT-03) | Sí |
| `registrarProveedor(razonSocial cadena, cuit cadena, tipo cadena, datosDeContacto registro, plazoDePago entero)` | CU-261 | Administrador (ACT-03) | Sí |
| `registrarRecepcionDeCompra(ordenId identificador, proveedorId identificador, depositoId identificador, tipoDeComprobante cadena, numeroDeComprobante cadena, items lista)` | CU-217 | Administrador (ACT-03) | Sí |
| `registrarReclamo(pedidoId identificador, motivo cadena, evidencia archivo)` | CU-023 | Cliente (ACT-01) | Sí |
| `registrarRegresoDelCamion(cargaId identificador, devueltos lista)` | CU-221 | Chofer (ACT-02), Administrador (ACT-03) | Sí |
| `registrarRevisionDeEnvase(envaseId identificador, fecha fecha, resultado cadena, vencimiento fecha)` | CU-132 | Administrador (ACT-03) | Sí |
| `registrarSalidaDelCamion(cargaId identificador)` | CU-219 | Chofer (ACT-02), Administrador (ACT-03) | Sí |
| `registrarse(nombreCompleto cadena, correo cadena, telefono cadena, contrasena cadena, datosDelCliente registro)` | CU-002 | Cliente (ACT-01) | Sí |
| `registrarSiniestro(vehiculoId identificador, datos registro)` | CU-201 | Chofer (ACT-02), Administrador (ACT-03) | Sí |
| `registrarTokenDeNotificaciones(usuarioId identificador, token cadena, plataforma cadena)` | CU-098 | Cliente (ACT-01) | Sí |
| `registrarVehiculo(usuarioId identificador, tipo cadena, capacidad decimal, patente cadena, marca cadena, modelo cadena, anio entero, color cadena)` | CU-034 | Administrador (ACT-03) | Sí |
| `reingresarEmpleado(empleadoId identificador, fechaDeIngreso fecha)` | CU-181 | Administrador (ACT-03) | Sí |
| `reintegrarPagoDelPedido(pedidoId identificador, importe moneda)` | CU-168 | Administrador (ACT-03), Sistema Automático (ACT-04) | Sí |
| `reponerCargaDelCamion(cargaId identificador, items lista)` | CU-218 | Administrador (ACT-03) | Sí |
| `resolverCasoDeRecupero(casoId identificador, decision cadena)` | CU-108 | Administrador (ACT-03) | Sí |
| `resolverIncidencia(incidenciaId identificador, notaDeResolucion cadena)` | CU-063 | Administrador (ACT-03) | Sí |
| `resolverReclamo(reclamoId identificador, resolucion cadena, estadoFinal cadena)` | CU-025 | Administrador (ACT-03) | Sí |
| `sembrarRolesIniciales()` | CU-090 | Administrador General (ACT-05) | Sí |
| `solicitarRecuperacionDeClave(correo cadena)` | CU-047 | Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03) | No |
| `suscribirseAlSeguimiento(clienteId identificador)` | CU-021 | Cliente (ACT-01) | No |
| `tomarReclamo(reclamoId identificador)` | CU-166 | Administrador (ACT-03) | Sí |
| `transferirEntreCajas(cajaOrigenId identificador, cajaDestinoId identificador, importe moneda)` | CU-228 | Administrador (ACT-03) | Sí |
| `transferirStock(origenId identificador, destinoId identificador, productoId identificador, condicion cadena, cantidad entero)` | CU-212 | Administrador (ACT-03) | Sí |
| `vaciarCarrito()` | CU-126 | Cliente (ACT-01) | Sí |
| `validarChofer(choferId identificador)` | CU-032 | Administrador (ACT-03) | Sí |
| `validarCobertura(latitud decimal, longitud decimal)` | CU-058 | Cliente (ACT-01) | No |
| `validarSesion()` | CU-091 | Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05) | No |
| `vencerOfertasExpiradas()` | CU-014 | Sistema Automático (ACT-04) | Sí |
| `venderACuentaCorriente(clienteId identificador, direccionId identificador, items lista)` | CU-236 | Administrador (ACT-03) | Sí |
| `verificarDisponibilidad()` | CU-104 | Plataforma de despliegue (ACT-09) | No |
| `verificarExistenciaDeUsuario(correo cadena, telefono cadena)` | CU-084 | Cliente (ACT-01) | No |
| `verificarSalud()` | CU-104 | Plataforma de despliegue (ACT-09) | No |
| `verificarVida()` | CU-104 | Plataforma de despliegue (ACT-09) | No |
| `verificarVigenciaAlAsignar(pedidoId identificador, series lista)` | CU-135 | Sistema Automático (ACT-04) | No |

Las operaciones de sólo consulta, que devuelven información sin alterar ninguna instancia, asociación ni atributo del modelo conceptual, no llevan contrato. Tampoco lo llevan las que no modifican el modelo aunque no sean consultas: `avisarLlegada`, `enviarNotificacionDePrueba`, `iniciarSesion`, `probarServicioDeCorreo`, `reenviarConfirmacionDePedido`, `solicitarRecuperacionDeClave`, `suscribirseAlSeguimiento` y `verificarVigenciaAlAsignar`, que verifican una identidad, verifican una regla o envían un aviso sin registrar nada.

---

#### Crítico Contrato: `registrarse()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarse(nombreCompleto cadena, correo cadena, telefono cadena, contrasena cadena, datosDelCliente registro)` |
| **Responsabilidades** | Dar de alta a un nuevo Cliente desde la App Cliente: crea la cuenta de acceso y el perfil, sin abrir sesión. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-002. Funciones: IRQ-01, OBJ-01. |
| **Notas** | Es la única alta pública: siempre crea un Cliente, nunca otro rol. La creación del Usuario la resuelve el caso incluido CU-082. Después del registro el cliente inicia sesión por separado (CU-001). |
| **Excepciones** | Si el correo o el teléfono ya están en uso → error de conflicto y no se modifica la cuenta existente. Si falta algún dato o no tiene el formato esperado → error de solicitud con el detalle del campo. Si el proveedor de identidad rechaza la cuenta → error de solicitud y no se crea nada. Si el origen superó el cupo de altas → error de límite de peticiones. |
| **Salida** | Los datos del Usuario creado (identificador, rol, correo). |
| **Precondiciones** | No existe un Usuario, activo o dado de baja, con el mismo correo ni con el mismo teléfono. |
| **Postcondiciones** | Se creó una instancia de Usuario, con el rol Cliente, y una instancia de Cliente asociada a él. El Cliente no tiene sesión iniciada. Si la persistencia falla, no se creó ninguna instancia y la cuenta de acceso creada para este registro fue eliminada. |

---

#### Crítico Contrato: `registrarChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarChofer(datosPersonales registro, datosDelChofer registro, distribuidoraId identificador)` |
| **Responsabilidades** | Dar de alta a un Chofer y su cuenta de acceso, asociados a la distribuidora del administrador. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-003, CU-031. Funciones: IRQ-01, IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | Lo realiza siempre el Administrador (CU-003 se conserva como referencia de SS-01; la especificación canónica es CU-031). La creación del Usuario la resuelve el caso incluido CU-082. |
| **Excepciones** | Si el correo o el teléfono ya están en uso → error de conflicto. Si falta algún dato o no tiene el formato esperado → error de solicitud con el detalle del campo. Si el rol o la distribuidora no le corresponden al solicitante → acceso denegado. |
| **Salida** | Los datos del Chofer creado (identificador del usuario, identificador del chofer, estado). |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora asociada. No existe un Usuario con el mismo correo ni con el mismo teléfono. |
| **Postcondiciones** | Se creó una instancia de Usuario, con el rol Chofer, y una instancia de Chofer asociada a él y a la Distribuidora del Administrador. El Chofer quedó sin validar y sin vehículo en uso. |

---

#### Importante Contrato: `actualizarPerfil()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarPerfil(usuarioId identificador, datos registro)` |
| **Responsabilidades** | Modificar los datos de contacto del perfil de un usuario: nombre completo, teléfono y foto. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-251. Funciones: IRQ-01, OBJ-01, OBJ-02. |
| **Notas** | Cada usuario modifica sólo su propio perfil; el Administrador puede modificar el de cualquier usuario. Cualquier otro dato enviado se descarta. |
| **Excepciones** | Si el usuario indicado no es quien opera y quien opera no es Administrador → acceso denegado. Si el usuario no existe → recurso no encontrado. |
| **Salida** | El perfil actualizado. |
| **Precondiciones** | El usuario está autenticado y el perfil indicado existe. |
| **Postcondiciones** | Los atributos nombre completo, teléfono y foto de la instancia de Usuario tomaron los valores enviados. Ningún otro atributo se modificó. |

---

#### Crítico Contrato: `crearPedido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearPedido(items lista, direccionId identificador, franjaId identificador, fechaAgendada fecha, metodoDePago cadena)` |
| **Responsabilidades** | Crear un pedido reservando el stock de forma atómica, calcular el total con promociones y recargos, y disparar el despacho automático. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-005, CU-044. Funciones: IRQ-02, IRQ-04, IRQ-05, IRQ-07, IRQ-08, OBJ-01, OBJ-02, OBJ-04, OBJ-06, OBJ-07. |
| **Notas** | El total incluye las promociones por volumen, el recargo por medio de pago y el recargo de zona. Si el medio de pago es MercadoPago, la propia operación registra el intento de cobro y le pide a la pasarela el enlace de pago, que devuelve en su respuesta (colaboración interna, `crearCheckoutDePago`, cuyo diagrama de interacción está en el Documento 3, CU-048): el intento de cobro se registra antes de conocer la respuesta de la pasarela, y el estado del Pedido no cambia hasta que la pasarela notifica el resultado (notificarResultadoDePago). Si la pasarela no devuelve el enlace, el Pago queda «pendiente» sin enlace y el pedido queda creado igual. La reserva con fecha y seña es una operación distinta: crearReserva. Al confirmarse el pedido se notifica al Cliente. |
| **Excepciones** | Si algún producto no existe o no es de la distribuidora → error de solicitud (producto no encontrado). Si el stock es insuficiente → la operación se revierte por completo y se informa el producto. Si la dirección está fuera de la zona de cobertura → error de solicitud (domicilio no cubierto). Si la franja no tiene cupo para esa fecha → error de solicitud (franja completa). Si el cliente o la dirección no existen → recurso no encontrado. |
| **Salida** | El pedido creado con sus ítems (número, total, estado pendiente) y, si corresponde, el enlace de pago. |
| **Precondiciones** | El Cliente está autenticado. La DireccionEntrega pertenece al Cliente y está dentro de una ZonaCobertura. Cada Producto del pedido existe, es de la Distribuidora y tiene stock suficiente. Si se indica una FranjaHoraria, está activa y tiene cupo para la fecha. |
| **Postcondiciones** | Se creó una instancia de Pedido, en estado «pendiente», asociada al Cliente que lo realizó, a la DireccionEntrega elegida y, si se indicó, a la FranjaHoraria. Se crearon sus instancias de ItemPedido, cada una asociada a su Producto, con el precio unitario —con las promociones por volumen ya aplicadas y redondeado a centavos— y el subtotal, cantidad por ese precio, calculados en ese momento, que no cambian aunque el Producto cambie de precio. El atributo stock de cada Producto pedido se decrementó en la cantidad pedida. Si el medio de pago es MercadoPago, se creó una instancia de Pago, en estado «pendiente», asociada al Pedido y a la Distribuidora, con el importe del intento y el enlace de pago. Si el medio de pago no es MercadoPago y hubo Chofer elegible, se creó una OfertaDespacho dirigida al Chofer disponible más cercano. |

---

#### Importante Contrato: `cancelarPedido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cancelarPedido(pedidoId identificador, motivo cadena)` |
| **Responsabilidades** | Cancelar un pedido que todavía no salió hacia el domicilio, dejándolo en estado cancelado y devolviendo al inventario las unidades reservadas. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-008, CU-010. Funciones: IRQ-02, IRQ-04, OBJ-01, OBJ-05, OBJ-06. |
| **Notas** | Lo inician el Cliente sobre un pedido propio (CU-008) y el Administrador sobre cualquier pedido activo de su distribuidora (CU-010). El cambio de estado y la restitución del stock se confirman en una única transacción, con el pedido bloqueado: dos cancelaciones simultáneas no devuelven el stock dos veces. Si el pedido tenía un pago aprobado por una pasarela, el reintegro se pide con reintegrarPagoDelPedido (CU-168, planificado I-7). Si el Pedido tenía un Chofer asociado, se notifica al Cliente, al Administrador y a ese Chofer. |
| **Excepciones** | Si el pedido no existe, es de otro cliente o es de otra distribuidora → recurso no encontrado. Si el pedido ya está entregado o cancelado → error de solicitud (no se puede cancelar un pedido finalizado). Si el pedido ya está en camino y quien lo cancela es el Cliente → error de solicitud (contactar al soporte). |
| **Salida** | El pedido con estado cancelado y el motivo registrado. |
| **Precondiciones** | El pedido existe y es de la distribuidora de quien opera. Si lo cancela el Cliente, el pedido es suyo y su estado es «reservado», «pendiente» o «aceptado». Si lo cancela el Administrador, su estado es «reservado», «pendiente», «aceptado» o «en camino». |
| **Postcondiciones** | El atributo estado de la instancia de Pedido pasó a «cancelado», con el motivo de la cancelación registrado. Por cada ItemPedido, el atributo stock del Producto referenciado se incrementó en la cantidad reservada. |

---

#### Importante Contrato: `liberarPedido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `liberarPedido(pedidoId identificador, motivo cadena)` |
| **Responsabilidades** | Devolver a «pendiente» un pedido que el chofer había tomado y no puede realizar, para que otro chofer lo tome. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-009. Funciones: IRQ-02, OBJ-02. |
| **Notas** | El stock no se restituye, porque el pedido sigue vivo. El pedido se vuelve a ofrecer en la siguiente ejecución del proceso temporal de despacho (CU-014). Se notifica al Cliente de que se busca otro chofer. |
| **Excepciones** | Si el pedido no existe o es de otra distribuidora → recurso no encontrado. Si el pedido no está asignado al chofer que lo libera → acceso denegado. Si el pedido ya está entregado o cancelado → error de solicitud (no se puede cancelar un pedido finalizado). Si el estado del pedido no admite la vuelta a pendiente → error de solicitud (transición no permitida). |
| **Salida** | El pedido con estado pendiente y sin chofer. |
| **Precondiciones** | El Chofer está autenticado. El pedido es de su distribuidora, está asociado a él y su estado es «aceptado» o «en camino». |
| **Postcondiciones** | Se rompió la asociación entre el Pedido y el Chofer. El atributo estado de la instancia de Pedido pasó a «pendiente». Las OfertaDespacho del Pedido que seguían vigentes quedaron cerradas. El stock de los Productos no varió. |

---

#### Importante Contrato: `cancelarPedidoForzado()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cancelarPedidoForzado(pedidoId identificador)` |
| **Responsabilidades** | Cancelar un pedido por decisión administrativa, sin pedir motivo. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-010. Funciones: IRQ-02, IRQ-04, OBJ-05, OBJ-06. |
| **Notas** | Es la vía equivalente a cancelarPedido que ofrece el panel cuando el administrador no consigna el motivo. Produce los mismos efectos sobre el pedido y el stock. |
| **Excepciones** | Si el pedido no existe o es de otra distribuidora → recurso no encontrado. Si el pedido ya está entregado o cancelado → error de solicitud (no se puede cancelar un pedido finalizado). |
| **Salida** | El pedido con estado cancelado. |
| **Precondiciones** | El Administrador está autenticado. El pedido existe, es de su distribuidora y su estado es «reservado», «pendiente», «aceptado» o «en camino». |
| **Postcondiciones** | El atributo estado de la instancia de Pedido pasó a «cancelado». Por cada ItemPedido, el atributo stock del Producto referenciado se incrementó en la cantidad reservada. |

---

#### Secundario Contrato: `asignarChoferAPedido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `asignarChoferAPedido(pedidoId identificador, choferId identificador)` |
| **Responsabilidades** | Asignar manualmente un chofer a un pedido pendiente, o reasignarlo a otro chofer si ya lo había aceptado uno. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-012. Funciones: IRQ-02, IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | Es la salida del administrador cuando el despacho automático no encuentra candidatos. Tiene los mismos efectos que la aceptación del chofer (CU-015): genera el código de entrega, cierra las ofertas abiertas y guarda la copia del vehículo. En una reasignación, el código nuevo deja sin efecto el anterior. El Cliente no recibe aviso de la asignación manual. Se notifica al Chofer nuevo, al Chofer anterior (si lo hubo) y al panel. |
| **Excepciones** | Si el pedido o el chofer no existen o son de otra distribuidora → recurso no encontrado. Si el chofer está deshabilitado, no está validado, no tiene un vehículo en uso o tiene documentación vencida → error de solicitud (no se puede asignar). Si el pedido no admite pasar a «aceptado» (cancelado, en camino o entregado) → error de solicitud (transición no permitida). |
| **Salida** | El pedido con estado aceptado, el chofer vinculado y el código de entrega nuevo. |
| **Precondiciones** | El Administrador está autenticado. El Pedido es de su distribuidora y su estado es «pendiente», o «aceptado» por otro Chofer. El Chofer es de la misma distribuidora, está habilitado y validado, tiene un Vehículo en uso y ni su licencia ni ese Vehículo tienen documentación vencida. |
| **Postcondiciones** | Se formó la asociación entre el Pedido y el Chofer indicado; si el Pedido tenía otro Chofer, esa asociación se rompió. El atributo estado del Pedido pasó a «aceptado» y quedaron registrados el momento de la aceptación y un código de entrega nuevo. El Pedido guardó la patente, la marca y el modelo del Vehículo en uso del Chofer. Las OfertaDespacho vigentes del Pedido quedaron cerradas. |

---

#### Crítico · automático Contrato: `ofrecerAlSiguienteChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `ofrecerAlSiguienteChofer(pedidoId identificador)` |
| **Responsabilidades** | Ofrecer el pedido al chofer más cercano de la misma distribuidora que todavía no fue contactado, con una vigencia limitada para aceptarlo. |
| **Tipo** | Sistema (proceso automático) |
| **Referencias cruzadas** | Casos de uso: CU-013. Funciones: IRQ-02, IRQ-03, OBJ-02. |
| **Notas** | Busca por radios crecientes (5, 10, 15 y 20 km: `RADIUS_STEPS_KM`) y ofrece a un solo chofer por vez, con una vigencia de 30 segundos (`OFFER_TTL_SECONDS`). Los radios y la vigencia son constantes del programa; serán configurables por distribuidora con CU-171 (I-1). Sólo considera choferes habilitados y validados, con vehículo en uso y documentación vigente. Se notifica al Chofer elegido. |
| **Excepciones** | Si ningún radio produce un chofer nuevo → no se crea la oferta y el pedido queda pendiente; el proceso temporal lo reintenta (CU-014). Si falla el aviso push → se ignora y la oferta igual queda creada. |
| **Salida** | El chofer al que se ofreció el pedido, o ninguno si no hubo candidato. |
| **Precondiciones** | El Pedido tiene estado «pendiente», no tiene Chofer asociado y tiene punto de entrega. Existe al menos un Chofer disponible con UbicacionGPS registrada. |
| **Postcondiciones** | Se creó una instancia de OfertaDespacho, en estado «ofrecida», dirigida al Chofer elegido y asociada al Pedido y a la Distribuidora, con una vigencia de 30 segundos desde su creación. El Pedido no cambió de estado: sigue «pendiente». |

---

#### Crítico · automático Contrato: `vencerOfertasExpiradas()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `vencerOfertasExpiradas()` |
| **Responsabilidades** | Cerrar las ofertas cuya vigencia venció y volver a ofrecer cada pedido todavía pendiente al siguiente chofer más cercano, sin intervención humana. |
| **Tipo** | Sistema (proceso automático) |
| **Referencias cruzadas** | Casos de uso: CU-014. Funciones: IRQ-02, IRQ-03, OBJ-02. |
| **Notas** | Se ejecuta cada 15 segundos. Con más de una instancia del sistema en ejecución, sólo una procesa cada ciclo, para que no se dupliquen las ofertas. También ofrece los pedidos pendientes sin oferta activa y con más de 60 segundos de antigüedad. Se notifica a cada Chofer al que se le ofrece un Pedido. |
| **Excepciones** | Si otra instancia ya está procesando el ciclo → el ciclo se saltea. Si el pedido de una oferta vencida ya fue aceptado, cancelado o no existe → la oferta se cierra igual y no se vuelve a ofrecer. |
| **Salida** | Ninguna: es un proceso interno sin actor receptor. |
| **Precondiciones** | Existe al menos una OfertaDespacho en estado «ofrecida» cuya vigencia ya terminó. |
| **Postcondiciones** | Cada OfertaDespacho vencida pasó a estado «vencida». Por cada Pedido que sigue «pendiente» y sin Chofer, se creó una nueva OfertaDespacho dirigida a un Chofer que no había sido contactado. |

---

#### Crítico Contrato: `aceptarPedido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `aceptarPedido(pedidoId identificador)` |
| **Responsabilidades** | Asignar el pedido al chofer que lo acepta, pasarlo a «aceptado» y avisar al cliente. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-015. Funciones: IRQ-02, IRQ-03, OBJ-02, OBJ-03. |
| **Notas** | Si el pedido ya tiene otro chofer asignado, un segundo chofer no lo desplaza ni regenera el código de entrega. Si acepta el mismo chofer, la operación es idempotente: conserva el código y el momento de aceptación. Un chofer sin vehículo en uso no puede aceptar pedidos. La copia de patente, marca y modelo se borra si el pedido vuelve a pendiente. Se notifica al Cliente. |
| **Excepciones** | Si el pedido es de otra distribuidora o no existe → recurso no encontrado. Si el pedido ya tiene asignado a otro chofer → acceso denegado. Si el pedido ya está entregado o cancelado → error de solicitud (transición no permitida). Si el chofer está deshabilitado, no está validado, no tiene un vehículo en uso o tiene documentación vencida → error de solicitud. |
| **Salida** | El pedido con estado aceptado, los datos de entrega y el código de entrega. |
| **Precondiciones** | El Pedido tiene estado «pendiente». El Chofer está habilitado y validado, tiene un Vehículo en uso y ni su licencia ni ese Vehículo tienen documentación vencida. |
| **Postcondiciones** | Se formó la asociación entre el Pedido y el Chofer que lo aceptó. El atributo estado del Pedido pasó a «aceptado», con la fecha de aceptación y un código de entrega. La OfertaDespacho vigente del Chofer pasó a «aceptada». El Pedido guardó la patente, la marca y el modelo del Vehículo en uso del Chofer. |

---

#### Importante Contrato: `rechazarOferta()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `rechazarOferta(pedidoId identificador)` |
| **Responsabilidades** | Cerrar la oferta activa del chofer que rechaza y volver a ofrecer el pedido de inmediato al siguiente chofer, sin esperar el vencimiento. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-016. Funciones: IRQ-02, IRQ-04, OBJ-02. |
| **Notas** | Si el pedido ya fue tomado por otro chofer o se canceló mientras llegaba el rechazo, la oferta se cierra igual y no se devuelve error al chofer que rechazó tarde. Se notifica al Chofer al que se ofrece el Pedido. |
| **Excepciones** | Si el pedido no existe → el rechazo no se registra y no hay efecto. Si el pedido es de otra distribuidora → recurso no encontrado. Si el pedido ya no es re-ofertable → la oferta se cierra y no se vuelve a ofrecer. |
| **Salida** | Si el rechazo quedó registrado. |
| **Precondiciones** | El Chofer está autenticado. Existe una OfertaDespacho en estado «ofrecida» del Pedido dirigida a ese Chofer. |
| **Postcondiciones** | La OfertaDespacho del Chofer pasó a estado «rechazada». Si el Pedido sigue «pendiente» y sin Chofer, se creó una nueva OfertaDespacho dirigida al siguiente Chofer más cercano que no había sido contactado. El Chofer que rechazó queda como ya contactado y no vuelve a recibir este Pedido. |

---

#### Crítico Contrato: `actualizarUbicacion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarUbicacion(usuarioId identificador, latitud decimal, longitud decimal)` |
| **Responsabilidades** | Guardar la posición actual del chofer para que esté disponible en el despacho por proximidad y en el mapa del cliente. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-017. Funciones: IRQ-03, OBJ-02, OBJ-03. |
| **Notas** | Es una escritura pura sobre el índice geoespacial: no se guarda historial de posiciones. La frecuencia con que llega depende de la app del chofer. El evento no tiene respuesta hacia el chofer que lo emite. |
| **Excepciones** | Si faltan el usuario o las coordenadas, o no son válidos → el evento se descarta sin error visible. |
| **Salida** | Ninguna: es un evento sin acuse de recibo. |
| **Precondiciones** | El Chofer está autenticado y conectado en tiempo real. Latitud y longitud son valores válidos. |
| **Postcondiciones** | El atributo posición de la instancia de UbicacionGPS del Chofer tomó las coordenadas recibidas; si no existía, se creó la instancia. Si el Chofer tiene un Pedido en curso, el Cliente y el panel recibieron la posición nueva. |

---

#### Crítico Contrato: `marcarPedidoEnCamino()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `marcarPedidoEnCamino(pedidoId identificador)` |
| **Responsabilidades** | Registrar que el chofer salió hacia el domicilio del cliente: pasa el pedido a «en camino», abre el seguimiento en vivo y avisa al cliente. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-018. Funciones: IRQ-02, OBJ-03. |
| **Notas** | Un chofer sólo puede poner en camino un pedido que tiene asignado; el Administrador puede mover cualquier pedido de su distribuidora. Si el pedido no tiene chofer, el estado cambia pero no hay seguimiento. Se notifica al Cliente. |
| **Excepciones** | Si el pedido no existe o es de otra distribuidora → recurso no encontrado. Si quien opera es un Chofer y el pedido está asignado a otro → acceso denegado. Si el pedido no está «aceptado» → error de solicitud (transición no permitida). |
| **Salida** | El pedido con estado en camino. |
| **Precondiciones** | El Pedido tiene estado «aceptado». Si opera un Chofer, es el asociado al Pedido. |
| **Postcondiciones** | El atributo estado del Pedido pasó a «en camino», con el momento de la salida registrado. Quedó abierto el seguimiento de la UbicacionGPS del Chofer para este Pedido. |

---

#### Crítico Contrato: `confirmarEntrega()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `confirmarEntrega(pedidoId identificador)` |
| **Responsabilidades** | Cerrar el ciclo del pedido marcándolo como entregado, saldar el pago en efectivo si corresponde y avisar al cliente. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-020. Funciones: IRQ-02, IRQ-08, OBJ-03, OBJ-04. |
| **Notas** | El chofer que confirma es el asignado al pedido. La confirmación con código de entrega es una operación distinta: confirmarEntregaConCodigo (CU-079). Al entregarse, cada envase despachado en el pedido pasa a estar en poder del cliente. Reconfirmar una entrega ya registrada no es un error de transición: la máquina de estados del pedido acepta que el estado nuevo sea igual al actual, de modo que la operación es idempotente. Se notifica al Cliente. |
| **Excepciones** | Si el pedido no existe o es de otra distribuidora → recurso no encontrado. Si el pedido está asignado a otro chofer → acceso denegado. Si el pedido está cancelado o todavía no salió hacia el domicilio → error de solicitud (transición no permitida). |
| **Salida** | El pedido con estado entregado. |
| **Precondiciones** | El Pedido tiene estado «en camino» y está asociado al Chofer que confirma. |
| **Postcondiciones** | El atributo estado del Pedido pasó a «entregado». Si el método de pago es efectivo, el atributo estado del Pago asociado pasó a «pagado». Se cerró el seguimiento de la UbicacionGPS del Chofer para este Pedido. Cada Envase despachado en el Pedido pasó a «en poder del cliente», con su MovimientoEnvase registrado. |

---

#### Crítico Contrato: `cambiarDisponibilidad()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cambiarDisponibilidad(usuarioId identificador, disponible booleano)` |
| **Responsabilidades** | Indicar si el chofer está disponible para recibir pedidos y, al ponerse no disponible, retirarlo del radar del despacho. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-022, CU-266. Funciones: IRQ-03, OBJ-02. |
| **Notas** | Es el interruptor que maneja el propio chofer desde su app, o el administrador sobre los choferes de su distribuidora; ponerse disponible exige que el chofer esté habilitado y validado, y desconectarse siempre se permite. Es independiente de la activación administrativa (cambiarEstadoDelChofer) y de la validación (validarChofer). |
| **Excepciones** | Si el usuario indicado no tiene perfil de chofer, o es de otra distribuidora → recurso no encontrado. Si un chofer opera sobre otro, o intenta ponerse disponible estando deshabilitado o sin validar → acceso denegado y no se modifica nada. |
| **Salida** | El estado de disponibilidad resultante. |
| **Precondiciones** | El Usuario está autenticado, tiene una instancia de Chofer asociada y es ese mismo Chofer o un Administrador de su distribuidora. Para ponerse disponible, el Chofer está habilitado y validado. |
| **Postcondiciones** | El atributo disponible de la instancia de Chofer tomó el valor enviado. Si quedó no disponible, se eliminó su UbicacionGPS y dejó de recibir ofertas de pedidos. |

---

#### Importante Contrato: `registrarReclamo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarReclamo(pedidoId identificador, motivo cadena, evidencia archivo)` |
| **Responsabilidades** | Registrar un reclamo del cliente sobre un pedido, validando que el pedido le pertenece. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-023. Funciones: IRQ-06, OBJ-04. |
| **Notas** | El alta no notifica a la distribuidora ni al chofer. La resolución queda a cargo de otra operación (resolverReclamo, CU-025). La fotografía se adjunta por separado (adjuntarFotoAlReclamo, CU-174). |
| **Excepciones** | Si el pedido no pertenece al cliente → error de solicitud (no autorizado). Si el pedido no existe → recurso no encontrado. |
| **Salida** | El reclamo creado, con su identificador y estado pendiente. |
| **Precondiciones** | El Cliente está autenticado. El Pedido existe y está asociado a ese Cliente. |
| **Postcondiciones** | Se creó una instancia de Reclamo, en estado «pendiente», con el motivo y la evidencia indicados, asociada al Pedido y presentada por el Cliente. |

---

#### Importante Contrato: `resolverReclamo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `resolverReclamo(reclamoId identificador, resolucion cadena, estadoFinal cadena)` |
| **Responsabilidades** | Resolver o rechazar un reclamo pendiente o en proceso, con una nota de resolución obligatoria. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-025. Funciones: IRQ-06, OBJ-04, OBJ-05. |
| **Notas** | La transición se valida contra los estados del reclamo: un reclamo resuelto o rechazado no admite esta operación hasta que se lo reabre (reabrirReclamo, CU-167). El Administrador General indica la distribuidora sobre la que opera. |
| **Excepciones** | Si la nota de resolución falta o está vacía → error de solicitud. Si el estado final no es «resuelto» ni «rechazado» → error de solicitud. Si el reclamo no existe o es de otra distribuidora → recurso no encontrado. Si el reclamo ya está resuelto o rechazado → error de solicitud (transición inválida) y no se modifica. |
| **Salida** | El reclamo con el estado final y la nota de resolución. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Reclamo existe, es de su distribuidora y su estado es «pendiente» o «en proceso». |
| **Postcondiciones** | El atributo estado de la instancia de Reclamo pasó al estado final elegido, «resuelto» o «rechazado», y su atributo nota de resolución tomó el texto indicado. |

---

#### Crítico Contrato: `invalidarChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `invalidarChofer(choferId identificador)` |
| **Responsabilidades** | Retirar a un chofer la marca de validación administrativa. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-271. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | Es la operación inversa de validarChofer. La marca no cambia por sí sola lo que el chofer puede hacer en el sistema. |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el chofer no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | El chofer con la marca de validación actualizada. |
| **Precondiciones** | El Administrador está autenticado. El Chofer existe y, si hay distribuidora en contexto, pertenece a ella. |
| **Postcondiciones** | El atributo validado de la instancia de Chofer pasó a falso. |

---

#### Crítico Contrato: `validarChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `validarChofer(choferId identificador)` |
| **Responsabilidades** | Marcar a un chofer como validado administrativamente. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-032. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | La marca es declarativa y alimenta el contador de choferes habilitados del panel. Es distinta de la disponibilidad que maneja el chofer (cambiarDisponibilidad) y de la activación administrativa (cambiarEstadoDelChofer). |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el chofer no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | El chofer con la marca de validación actualizada. |
| **Precondiciones** | El Administrador está autenticado. El Chofer existe y, si hay distribuidora en contexto, pertenece a ella. |
| **Postcondiciones** | El atributo validado de la instancia de Chofer pasó a verdadero. |

---

#### Importante Contrato: `cambiarEstadoDelChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cambiarEstadoDelChofer(choferId identificador, activo booleano)` |
| **Responsabilidades** | Activar o desactivar a un chofer desde el panel: un chofer inactivo no puede aceptar pedidos. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-033, CU-267. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | Es la única marca del chofer que el sistema consulta al aceptar un pedido. Es independiente de la disponibilidad que el chofer maneja desde su app. |
| **Excepciones** | Si el identificador no es válido o el estado de actividad no es verdadero o falso → error de solicitud. Si el chofer no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | El chofer con su estado de actividad actualizado. |
| **Precondiciones** | El Administrador está autenticado. El Chofer existe y, si hay distribuidora en contexto, pertenece a ella. |
| **Postcondiciones** | El atributo activo de la instancia de Chofer tomó el valor indicado. Si quedó inactivo, el Chofer no puede aceptar pedidos. |

---

#### Importante Contrato: `registrarVehiculo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarVehiculo(usuarioId identificador, tipo cadena, capacidad decimal, patente cadena, marca cadena, modelo cadena, anio entero, color cadena)` |
| **Responsabilidades** | Registrar el vehículo operativo de un chofer en la flota de la distribuidora. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-034. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | El único dato obligatorio es el chofer al que pertenece; tipo, patente, marca, modelo, año, color y capacidad son opcionales. La patente es única en todo el sistema. |
| **Excepciones** | Si falta el chofer, no es válido o se envía un dato no declarado → error de solicitud con el detalle del campo. Si el administrador no tiene distribuidora en contexto → error de solicitud. Si el usuario indicado no existe → recurso no encontrado. Si la patente ya está registrada → error de solicitud. |
| **Salida** | El vehículo creado. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. El Chofer existe. |
| **Postcondiciones** | Se creó una instancia de Vehiculo con los datos indicados, asociada al Chofer y a la Distribuidora del Administrador. |

---

#### Crítico Contrato: `crearProducto()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearProducto(tipo cadena, peso decimal, precio moneda, stockInicial entero, descripcion cadena, promociones lista)` |
| **Responsabilidades** | Registrar un nuevo tipo de garrafa en el catálogo de la distribuidora. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-036. Funciones: IRQ-04, OBJ-05, OBJ-06. |
| **Notas** | El producto nace activo y se publica en el catálogo de la App Cliente si tiene stock. La unicidad del tipo es por distribuidora: dos empresas pueden tener cada una su «10kg». |
| **Excepciones** | Si falta el tipo, el peso o el precio, o alguno no tiene el tipo esperado → error de solicitud con el detalle del campo. Si el administrador no tiene distribuidora en contexto → error de solicitud. Si ya existe un producto de ese tipo en la distribuidora → error de solicitud. |
| **Salida** | El producto creado. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. No existe en esa Distribuidora un Producto del mismo tipo. |
| **Postcondiciones** | Se creó una instancia de Producto, activa, asociada a la Distribuidora, con el tipo, el peso, el precio, el stock inicial, la descripción y las Promocion indicados. |

---

#### Crítico Contrato: `actualizarProducto()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarProducto(productoId identificador, datos registro)` |
| **Responsabilidades** | Modificar los datos de venta de un producto de la distribuidora: su precio o sus promociones por cantidad. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-037, CU-039. Funciones: IRQ-04, OBJ-05, OBJ-06, OBJ-07. |
| **Notas** | El cambio de precio rige sólo para los pedidos futuros: cada ItemPedido conserva el precio unitario con el que se compró. Las promociones se envían como lista completa y reemplazan a las anteriores; cada regla fija una cantidad mínima y un porcentaje de descuento mayor que 0 y no mayor que 100, y no puede haber dos reglas para la misma cantidad. |
| **Excepciones** | Si el precio no es un número mayor que cero o las promociones no cumplen las reglas → error de solicitud con el detalle del campo. Si el administrador no tiene distribuidora en contexto → error de solicitud. Si el producto no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | El producto actualizado. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. El Producto pertenece a esa Distribuidora. |
| **Postcondiciones** | El atributo precio del Producto tomó el valor indicado, o el conjunto de Promocion del Producto fue reemplazado por el enviado (se crearon las nuevas instancias y se eliminaron las anteriores). Los ItemPedido ya registrados no se modificaron. |

---

#### Crítico Contrato: `actualizarStock()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarStock(productoId identificador, variacion entero)` |
| **Responsabilidades** | Ajustar el stock de un producto para reflejar una reposición o una corrección de inventario. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-038. Funciones: IRQ-04, OBJ-05, OBJ-06. |
| **Notas** | El valor ingresado es un ajuste, no el stock final: se suma al stock existente. Un valor positivo repone y uno negativo descuenta. Este caso cubre sólo el ajuste manual; el descuento al crear un pedido lo resuelve crearPedido. |
| **Excepciones** | Si la cantidad falta, no es un entero o está fuera de rango → error de solicitud. Si el producto no existe o es de otra distribuidora → recurso no encontrado. Si el ajuste dejaría el stock por debajo de cero → error de solicitud y no se modifica el stock. |
| **Salida** | El producto con el stock resultante. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. El Producto pertenece a esa Distribuidora. El stock resultante no es negativo. |
| **Postcondiciones** | El atributo stock del Producto se modificó en la variación indicada. Si correspondía, el Producto volvió a estar disponible en el catálogo. |

---

#### Importante Contrato: `desactivarProducto()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `desactivarProducto(productoId identificador)` |
| **Responsabilidades** | Retirar un producto del catálogo de la distribuidora mediante una baja lógica. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-040. Funciones: IRQ-04, OBJ-05, OBJ-06. |
| **Notas** | El producto deja de figurar en el catálogo y no puede seleccionarse en nuevos pedidos. El stock y el resto de los datos se conservan; los pedidos ya creados no se ven afectados. |
| **Excepciones** | Si el administrador no tiene distribuidora en contexto → error de solicitud. Si el producto no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | El producto desactivado. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. El Producto pertenece a esa Distribuidora y está activo. |
| **Postcondiciones** | El atributo activo de la instancia de Producto pasó a falso. El Producto dejó de ser visible en el catálogo del Cliente. No se eliminó ninguna instancia. |

---

#### Importante Contrato: `reactivarProducto()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `reactivarProducto(productoId identificador)` |
| **Responsabilidades** | Volver a publicar en el catálogo un producto dado de baja. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-268. Funciones: IRQ-04, OBJ-05, OBJ-06. |
| **Notas** | El producto vuelve con su stock y sus promociones intactos. |
| **Excepciones** | Si el producto no existe o es de otra distribuidora → recurso no encontrado. Si el producto ya estaba activo → no se modifica nada. |
| **Salida** | El producto reactivado. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. El Producto pertenece a esa Distribuidora y está inactivo. |
| **Postcondiciones** | El atributo activo de la instancia de Producto pasó a verdadero. El Producto vuelve a ser visible y seleccionable en nuevos pedidos. |

---

#### Importante Contrato: `crearFranjaHoraria()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearFranjaHoraria(nombre cadena, horaInicio hora, horaFin hora, capacidad entero)` |
| **Responsabilidades** | Crear una franja horaria de entrega para la distribuidora, que los clientes pueden elegir al agendar un pedido. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-042. Funciones: IRQ-05, OBJ-04, OBJ-05. |
| **Notas** | La capacidad máxima de pedidos por día es opcional. Las franjas activas con cupo remanente son las que se ofrecen al cliente. |
| **Excepciones** | Si el nombre está vacío, una hora no respeta el formato de horas y minutos o la capacidad no es un entero → error de solicitud con el detalle del campo. Si el administrador no tiene distribuidora en contexto → error de solicitud. |
| **Salida** | La franja creada. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. La hora de fin es posterior a la de inicio. |
| **Postcondiciones** | Se creó una instancia de FranjaHoraria, activa, asociada a la Distribuidora, con el nombre, las horas y la capacidad indicados. |

---

#### Importante Contrato: `modificarFranjaHoraria()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarFranjaHoraria(franjaId identificador, nombre cadena, horaInicio hora, horaFin hora, capacidad entero)` |
| **Responsabilidades** | Actualizar la capacidad máxima de pedidos por día de una franja existente. |
| **Tipo** | Sistema (planificado, I-1) |
| **Referencias cruzadas** | Casos de uso: CU-043. Funciones: IRQ-05, OBJ-04, OBJ-05. |
| **Notas** | Los pedidos ya agendados se conservan aunque superen la nueva capacidad; los que se agenden después se validan contra el nuevo límite. Si para alguna fecha próxima la franja ya excede la nueva capacidad, la respuesta lo informa. |
| **Excepciones** | Si la capacidad no es un entero mayor que cero → error de solicitud. Si el administrador no tiene distribuidora en contexto → error de solicitud. Si la franja no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | La franja actualizada y, si corresponde, las fechas próximas que superan la nueva capacidad. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. La FranjaHoraria pertenece a esa Distribuidora. |
| **Postcondiciones** | El atributo capacidad de la instancia de FranjaHoraria tomó el valor indicado. |

---

#### Importante Contrato: `editarDireccionDeEntrega()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `editarDireccionDeEntrega(direccionId identificador, cambios registro)` |
| **Responsabilidades** | Corregir los datos de una dirección ya registrada: calle, altura, piso y departamento, ciudad, código postal, coordenadas o indicaciones. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-046, CU-118. Funciones: IRQ-01, IRQ-07, OBJ-01, OBJ-02. |
| **Notas** | Si cambia algo que afecta la ubicación, el sistema vuelve a resolverla contra el servicio de mapas; si el servicio no responde, la edición continúa con las coordenadas disponibles y la precisión pasa a aproximada o sin resolver. La latitud y la longitud se cambian juntas. |
| **Excepciones** | Si viene la latitud sin la longitud, o al revés → error de solicitud. Si la dirección no existe o es de otro cliente → recurso no encontrado. Si quien opera es un administrador y el titular no es de su distribuidora → recurso no encontrado. Si quien opera es un Administrador de empresa → acceso denegado. |
| **Salida** | La dirección actualizada. |
| **Precondiciones** | El Cliente está autenticado. La DireccionEntrega existe y le pertenece. Si quien opera es un Administrador, es el Administrador General: un administrador de empresa no modifica direcciones. |
| **Postcondiciones** | Los atributos de la instancia de DireccionEntrega enviados tomaron los valores nuevos. Si cambió su ubicación, el atributo punto y el atributo precisión tomaron el mejor resultado de la nueva resolución. |

---

#### Importante Contrato: `eliminarDireccionDeEntrega()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarDireccionDeEntrega(direccionId identificador)` |
| **Responsabilidades** | Dar de baja una dirección que el cliente ya no usa, mediante una baja lógica. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-046, CU-119. Funciones: IRQ-01, IRQ-07, OBJ-01, OBJ-02. |
| **Notas** | Los pedidos que usaron la dirección la siguen mostrando. Si la dirección dada de baja era la predeterminada, pasa a predeterminada la más reciente de las que quedan, para que el cliente no se quede sin una. Para volver a usar una dirección dada de baja se la registra de nuevo. |
| **Excepciones** | Si la dirección no existe o es de otro cliente → recurso no encontrado. Si quien opera es un administrador y el titular no es de su distribuidora → recurso no encontrado. Si quien opera es un Administrador de empresa → acceso denegado. |
| **Salida** | Ninguna. |
| **Precondiciones** | El Cliente está autenticado. La DireccionEntrega existe y le pertenece. Si quien opera es un Administrador, es el Administrador General: un administrador de empresa no modifica direcciones. |
| **Postcondiciones** | El atributo fecha de baja de la instancia de DireccionEntrega tomó la fecha actual: dejó de aparecer entre las direcciones del Cliente y no puede elegirse para un pedido nuevo. Los Pedidos que la usaron conservan su asociación. Si era la predeterminada y el Cliente tiene otras direcciones, el atributo predeterminada de la más reciente pasó a verdadero. |

---

#### Importante Contrato: `marcarDireccionPredeterminada()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `marcarDireccionPredeterminada(direccionId identificador)` |
| **Responsabilidades** | Elegir cuál de las direcciones del cliente se propone sola al armar un pedido. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-046, CU-120. Funciones: IRQ-01, IRQ-07, OBJ-01, OBJ-02. |
| **Notas** | No cambia ningún dato de la dirección, sino su papel entre las demás. Siempre hay exactamente una dirección predeterminada. |
| **Excepciones** | Si la dirección no existe o es de otro cliente → recurso no encontrado. Si quien opera es un administrador y el titular no es de su distribuidora → recurso no encontrado. Si quien opera es un Administrador de empresa → acceso denegado. |
| **Salida** | La dirección predeterminada actualizada. |
| **Precondiciones** | El Cliente está autenticado. La DireccionEntrega existe y le pertenece. Si quien opera es un Administrador, es el Administrador General: un administrador de empresa no modifica direcciones. |
| **Postcondiciones** | El atributo predeterminada de la instancia de DireccionEntrega elegida pasó a verdadero y el de las demás direcciones del Cliente pasó a falso. |

---

#### Importante Contrato: `registrarDireccionDeEntrega()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarDireccionDeEntrega(datos registro)` |
| **Responsabilidades** | Dar de alta una dirección donde el cliente quiere recibir sus garrafas, resuelta contra el servicio de mapas, y marcarla como predeterminada si así se pide. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-046, CU-116. Funciones: IRQ-01, IRQ-07, OBJ-01, OBJ-02. |
| **Notas** | El servicio de mapas aporta el mejor punto disponible sin bloquear el alta: si no responde, la dirección queda registrada con las coordenadas que mandó la app y precisión «sin resolver»; si ubica la calle pero no la altura, queda con precisión «aproximada». El titular lo determina el sistema a partir de la sesión; sólo el Administrador General puede indicarlo. |
| **Excepciones** | Si falta la latitud o la longitud, o no son coordenadas válidas, o la precisión no es exacta, aproximada o sin resolver → error de solicitud. Si la cuenta del titular no existe → recurso no encontrado. Si quien opera es un administrador y el titular no es de su distribuidora → recurso no encontrado. Si quien opera es un Administrador de empresa → acceso denegado. |
| **Salida** | La dirección creada. |
| **Precondiciones** | El Cliente está autenticado y su Usuario existe. Si quien opera es un Administrador, es el Administrador General: un administrador de empresa no modifica direcciones. |
| **Postcondiciones** | Se creó una instancia de DireccionEntrega asociada al Cliente, con los datos, el punto resuelto y la precisión indicados. Si se pidió como predeterminada, el atributo predeterminada de esta instancia pasó a verdadero y el de las demás direcciones del Cliente pasó a falso. |

---

#### Importante Contrato: `cambiarCorreo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cambiarCorreo(correoActual cadena, correoNuevo cadena)` |
| **Responsabilidades** | Cambiar el correo de la cuenta del usuario autenticado, dejando la nueva dirección pendiente de verificación. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-047. Funciones: IRQ-01, OBJ-01. |
| **Notas** | Es la variante autenticada de CU-047. El token de identidad del usuario acredita que es el dueño de la cuenta. La contraseña no se almacena en el sistema. Se envía un correo de verificación a la dirección nueva. |
| **Excepciones** | Si el token de identidad es inválido o venció → error de solicitud. Si el correo del token no coincide con el correo actual declarado → error de solicitud. |
| **Salida** | Confirmación del cambio, con el envío de la verificación a la dirección nueva. |
| **Precondiciones** | El Usuario está autenticado y su correo actual coincide con el que declara. |
| **Postcondiciones** | El atributo correo de la instancia de Usuario tomó el valor nuevo, pendiente de verificación. |

---

#### Crítico Contrato: `notificarResultadoDePago()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `notificarResultadoDePago(tipoDeNotificacion cadena, identificadorDelPago cadena, firma cadena)` |
| **Responsabilidades** | Recibir la notificación de la pasarela, validar su firma, consultar el estado real del pago, actualizar el Pago y aplicar sus efectos sobre el pedido. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-048. Funciones: IRQ-02, IRQ-08, OBJ-02, OBJ-07. |
| **Notas** | La pasarela recibe siempre una respuesta de recibido, con o sin procesamiento, para que no reintente en bucle. La notificación es idempotente: repetirla no produce cambios adicionales, y el aviso al Cliente sale sólo en la primera confirmación. Un pago rechazado o cancelado deja el pedido a la espera sin avisarle al Cliente (limitación conocida, §10 del Documento 3); si vence el plazo sin pago, lo cancela expirarPedidosSinPagar. La primera vez que el pago se aprueba se notifica al Cliente; repetir la misma notificación no lo vuelve a avisar. |
| **Excepciones** | Si la firma es inválida → se descarta sin procesar y no se revela si el pedido existe. Si el tipo de notificación no es de pago o falta el identificador → se ignora. Si el pedido ya está cancelado o entregado → se registra el pago y no se reactiva el pedido. Si el pedido no existe → se registra la advertencia y se corta. |
| **Salida** | Confirmación de recibido hacia la pasarela. |
| **Precondiciones** | La notificación proviene de la pasarela y su firma es válida. Existe un Pago asociado al Pedido referenciado. |
| **Postcondiciones** | El atributo estado del Pago tomó el que informó la pasarela (aprobado, rechazado, cancelado, reembolsado o pendiente). Si el Pago fue aprobado y el Pedido es una reserva, se registró la seña como paga, el Pedido no se ofreció a ningún Chofer. Si fue aprobado y el Pedido es un pedido normal, el Pedido quedó pagado, se creó una OfertaDespacho dirigida al Chofer más cercano. |

---

#### Importante Contrato: `ajustarSaldoDelChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `ajustarSaldoDelChofer(choferId identificador, monto moneda)` |
| **Responsabilidades** | Ajustar el saldo acumulado de las ganancias de un chofer cuando el administrador liquida o descuenta. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-049. Funciones: IRQ-03, OBJ-05. |
| **Notas** | El saldo se guarda en el perfil del chofer. La única escritura del saldo es este ajuste manual; la consulta del saldo no modifica ningún dato (consultarPerfilDelChofer). |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el chofer no existe o es de otra distribuidora → recurso no encontrado. Si quien opera no es Administrador ni Administrador General → acceso denegado. |
| **Salida** | El saldo actualizado. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Chofer existe y, si hay distribuidora en contexto, pertenece a ella. |
| **Postcondiciones** | El atributo saldo de la instancia de Chofer se modificó en el monto indicado. |

---

#### Secundario Contrato: `bloquearUsuario()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `bloquearUsuario(usuarioId identificador, bloquear booleano)` |
| **Responsabilidades** | Marcar o desmarcar a un usuario, cliente o chofer, como bloqueado por motivos de moderación o seguridad. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-050, CU-270. Funciones: IRQ-01, OBJ-05. |
| **Notas** | Es un interruptor bidireccional: la misma operación bloquea o desbloquea según el valor enviado. |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si quien opera no es Administrador ni Administrador General → acceso denegado. Si el usuario no existe → recurso no encontrado. |
| **Salida** | El usuario con la marca de bloqueo actualizada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Usuario existe. |
| **Postcondiciones** | El atributo bloqueado de la instancia de Usuario tomó el valor indicado. |

---

#### Importante Contrato: `editarVehiculo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `editarVehiculo(vehiculoId identificador, datos registro)` |
| **Responsabilidades** | Corregir los datos de un vehículo de la flota: tipo, patente, marca, modelo, año, color o capacidad de carga. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-051, CU-111. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | La patente identifica al vehículo y no puede repetirse. Mientras un chofer lo tiene en uso no se puede cambiar su patente ni su tipo; los demás datos se editan sin esa restricción. |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el vehículo no existe o es de otra distribuidora → recurso no encontrado. Si la patente nueva ya pertenece a otro vehículo → se rechaza el cambio. Si cambia la patente o el tipo y algún chofer tiene el vehículo en uso → error de conflicto (hay que liberarlo antes) y no se modifica nada. |
| **Salida** | El vehículo actualizado. |
| **Precondiciones** | El Administrador está autenticado y opera sobre una distribuidora. El Vehiculo existe y es de esa Distribuidora. Si se cambia su patente o su tipo, ningún Chofer lo tiene en uso. |
| **Postcondiciones** | Los atributos del Vehiculo tomaron los valores enviados. La patente sigue siendo única. |

---

#### Importante Contrato: `eliminarVehiculo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarVehiculo(vehiculoId identificador)` |
| **Responsabilidades** | Dar de baja un vehículo de la flota mediante una baja lógica. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-051, CU-112. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | El vehículo se conserva para el historial. Su patente queda libre: la unicidad se exige sólo entre los vehículos vigentes. La comprobación y la baja se hacen en una sola transacción, con el mismo bloqueo del vehículo que usa ponerVehiculoEnUso. |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el vehículo no existe o es de otra distribuidora → recurso no encontrado. Si algún chofer tiene el vehículo en uso → error de conflicto (hay que liberarlo primero) y no se da de baja. |
| **Salida** | Ninguna. |
| **Precondiciones** | El Administrador está autenticado y opera sobre una distribuidora. El Vehiculo existe, es de esa Distribuidora y ningún Chofer lo tiene en uso. |
| **Postcondiciones** | El atributo fecha de baja de la instancia de Vehiculo tomó la fecha actual. El Vehiculo dejó de aparecer en las consultas y se conservó para el historial. No se eliminó ninguna instancia. |

---

#### Crítico Contrato: `registrarDistribuidora()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarDistribuidora(nombre cadena, identificadorCorto cadena, razonSocial cadena, cuit cadena, correo cadena, telefono cadena, logo archivo, plan cadena)` |
| **Responsabilidades** | Dar de alta una nueva distribuidora, validando sus datos y que su identificador corto sea único. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-052. Funciones: IRQ-09, OBJ-09. |
| **Notas** | El alta no envía aviso ni credencial a la distribuidora. La puesta en marcha operativa (usuarios, catálogo, franjas horarias) la hacen pasos posteriores. |
| **Excepciones** | Si los datos no cumplen el formato → error de validación. Si el identificador corto ya está en uso → error de conflicto. |
| **Salida** | La distribuidora creada, con su identificador y estado inicial. |
| **Precondiciones** | El solicitante es Administrador General autenticado. No existe una Distribuidora con el mismo identificador corto. |
| **Postcondiciones** | Se creó una instancia de Distribuidora, con el nombre, el identificador corto, la razón social, el CUIT, el correo, el teléfono, el logo y el plan indicados. La Distribuidora quedó lista para operar. |

---

#### Crítico Contrato: `modificarDistribuidora()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarDistribuidora(distribuidoraId identificador, datos registro)` |
| **Responsabilidades** | Actualizar parcialmente los datos o la configuración de una distribuidora: estado, plan y datos de contacto. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-054. Funciones: IRQ-09, OBJ-09. |
| **Notas** | Es una actualización parcial: sólo se modifican los atributos enviados. |
| **Excepciones** | Si la distribuidora no existe → recurso no encontrado. Si los datos no cumplen el formato → error de validación. |
| **Salida** | La distribuidora actualizada. |
| **Precondiciones** | El solicitante es Administrador General autenticado. La Distribuidora existe. |
| **Postcondiciones** | Los atributos de la instancia de Distribuidora enviados tomaron los valores nuevos. |

---

#### Importante Contrato: `darDeBajaDistribuidora()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `darDeBajaDistribuidora(distribuidoraId identificador)` |
| **Responsabilidades** | Dar de baja una distribuidora mediante una baja lógica, sin borrado físico. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-055. Funciones: IRQ-09, OBJ-09. |
| **Notas** | La baja lógica evita conflictos referenciales: los usuarios, choferes y pedidos de la distribuidora conservan su estado y sus datos. |
| **Excepciones** | Si la distribuidora no existe → recurso no encontrado. |
| **Salida** | Ninguna. |
| **Precondiciones** | El solicitante es Administrador General autenticado. La Distribuidora existe. |
| **Postcondiciones** | El atributo fecha de baja de la instancia de Distribuidora tomó la fecha actual. La Distribuidora dejó de aparecer en las consultas. No se eliminó ninguna instancia. |

---

#### Importante Contrato: `definirZonaDeCobertura()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `definirZonaDeCobertura(nombre cadena, poligono poligono, recargo moneda, activa booleano)` |
| **Responsabilidades** | Registrar una zona de cobertura delimitada por un polígono y asociarla a la distribuidora activa. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-056. Funciones: IRQ-09, IRQ-10, OBJ-10. |
| **Notas** | El recargo de la zona puede expresarse como un monto fijo o como un porcentaje del pedido. La zona nace activa. |
| **Excepciones** | Si las coordenadas o los campos no cumplen el formato → error de solicitud. Si no hay distribuidora en el contexto → error de contexto. |
| **Salida** | La zona creada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General y la petición indica la distribuidora. |
| **Postcondiciones** | Se creó una instancia de ZonaCobertura, activa, asociada a la Distribuidora, con el nombre, el polígono y el recargo indicados. |

---

#### Secundario Contrato: `eliminarZonaDeCobertura()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarZonaDeCobertura(zonaId identificador)` |
| **Responsabilidades** | Dar de baja una zona de cobertura de la distribuidora mediante una baja lógica. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-059. Funciones: IRQ-09, IRQ-10, OBJ-10. |
| **Notas** | La zona deja de contar para la validación de cobertura y se conserva para el historial. Si era la última zona vigente, la validación vuelve a considerar cubierta cualquier dirección, sin recargo. |
| **Excepciones** | Si la zona no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | Ninguna. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La ZonaCobertura existe y es de la Distribuidora en contexto. |
| **Postcondiciones** | El atributo fecha de baja de la instancia de ZonaCobertura tomó la fecha actual. La validación de cobertura la ignora. No se eliminó ninguna instancia. |

---

#### Crítico Contrato: `registrarIncidencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarIncidencia(pedidoId identificador, tipo cadena, descripcion cadena, foto archivo)` |
| **Responsabilidades** | Registrar una incidencia sobre un pedido: una demora, un siniestro o cualquier inconveniente surgido durante el reparto. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-060. Funciones: IRQ-02, IRQ-11, OBJ-04. |
| **Notas** | La distribuidora de la incidencia sale del pedido y no de quien la reporta. La foto es opcional. La incidencia queda abierta a la espera de resolución (resolverIncidencia). |
| **Excepciones** | Si el pedido no es válido, el tipo no es uno de los previstos o falta la descripción → error de solicitud. Si el pedido no existe o es de otra distribuidora → recurso no encontrado. Si quien reporta es un Chofer y el pedido no está asignado a él → acceso denegado. |
| **Salida** | La incidencia creada, en estado abierto. |
| **Precondiciones** | El solicitante es Chofer, Administrador o Administrador General. El Pedido existe y, si hay distribuidora en contexto, es de ella. Si reporta un Chofer, el Pedido está asociado a él. |
| **Postcondiciones** | Se creó una instancia de Incidencia, abierta, con el tipo, la descripción y la foto indicados, asociada al Pedido, a la Distribuidora del Pedido y al Usuario que la reportó. |

---

#### Importante Contrato: `resolverIncidencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `resolverIncidencia(incidenciaId identificador, notaDeResolucion cadena)` |
| **Responsabilidades** | Cerrar una incidencia de entrega dejando asentada la nota de resolución y el momento en que se resolvió. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-063. Funciones: IRQ-11, OBJ-05, OBJ-11. |
| **Notas** | La fecha de resolución es el dato con el que se mide el tiempo de atención. La incidencia resuelta deja de contar entre las abiertas del panel. |
| **Excepciones** | Si la nota de resolución falta o no es texto → error de solicitud. Si no hay distribuidora en el contexto → error de solicitud. Si la incidencia no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | La incidencia resuelta. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La Incidencia existe en la Distribuidora en contexto y está abierta. |
| **Postcondiciones** | Los atributos nota de resolución y fecha de resolución de la instancia de Incidencia tomaron los valores indicados y la Incidencia quedó resuelta. |

---

#### Crítico Contrato: `calificarPedido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `calificarPedido(pedidoId identificador, estrellas entero, comentario cadena)` |
| **Responsabilidades** | Registrar la calificación de una de las partes de un pedido entregado y, cuando califica el cliente, recalcular el promedio del chofer. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-064. Funciones: IRQ-02, IRQ-03, IRQ-12, OBJ-04. |
| **Notas** | A quién se califica se deriva del propio pedido. Hay a lo sumo una calificación por parte y por pedido. |
| **Excepciones** | Si el pedido no existe → recurso no encontrado. Si el pedido no está entregado → error de solicitud (sólo se califica un pedido entregado). Si quien califica no es una de las dos partes del pedido → acceso denegado. Si el cliente califica un pedido sin chofer → error de solicitud. Si ya calificó ese lado → error de conflicto. |
| **Salida** | La calificación creada. |
| **Precondiciones** | El solicitante está autenticado. El Pedido tiene estado «entregado». El solicitante es el Cliente del Pedido o el Chofer que lo entregó. No existe una Calificacion de ese lado. |
| **Postcondiciones** | Se creó una instancia de Calificacion, con su puntaje y su comentario, emitida por el Usuario que califica, dirigida al Usuario calificado y asociada al Pedido. Si calificó el Cliente, el atributo calificación del Chofer tomó el promedio de las valoraciones recibidas. El estado del Pedido no cambió. |

---

#### Importante Contrato: `darDeAltaEnvase()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `darDeAltaEnvase(numeroDeSerie cadena, tipoDeProducto cadena, deposito cadena)` |
| **Responsabilidades** | Incorporar una unidad física de envase al parque de la distribuidora, en estado inicial de depósito, abriendo su bitácora de movimientos. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-067. Funciones: IRQ-04, IRQ-13, OBJ-04. |
| **Notas** | El número de serie es único por distribuidora: dos distribuidoras pueden tener envases con el mismo número de serie. |
| **Excepciones** | Si ya existe un envase con ese número de serie en la distribuidora → error de conflicto. |
| **Salida** | El envase creado. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora asociada. El Producto indicado existe. No existe un Envase con ese número de serie en la Distribuidora. |
| **Postcondiciones** | Se creó una instancia de Envase, en estado «en depósito», asociada al Producto indicado y a la Distribuidora. Se creó su primera instancia de MovimientoEnvase, que inaugura su trazabilidad. |

---

#### Crítico Contrato: `asignarEnvasesAPedido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `asignarEnvasesAPedido(pedidoId identificador, numerosDeSerie lista)` |
| **Responsabilidades** | Vincular los envases físicos que salen a repartir con el pedido y despacharlos, dejando el rastro para que la confirmación de entrega los avance. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-068. Funciones: IRQ-02, IRQ-13, OBJ-04. |
| **Notas** | Se rechaza la asignación completa si algún envase tiene la revisión vencida; una asignación rechazada no deja envases asignados a medias (CU-135). Sólo se asignan envases de la distribuidora del pedido. |
| **Excepciones** | Si el pedido no existe → recurso no encontrado. Si algún número de serie no existe en la distribuidora → recurso no encontrado. Si algún envase no está lleno → error de solicitud (hay que llenarlo antes de despacharlo). Si algún envase tiene la revisión vencida → asignación rechazada con la lista de series vencidas. |
| **Salida** | Los envases despachados. |
| **Precondiciones** | El solicitante es Chofer, Administrador o Administrador General. El Pedido existe y es de su Distribuidora. Cada Envase indicado pertenece a esa Distribuidora, está «lleno» y tiene la revisión vigente. |
| **Postcondiciones** | Por cada Envase: su estado pasó de «lleno» a «despachado», se formó la asociación con el Pedido que lo lleva y se creó una instancia de MovimientoEnvase con el Pedido, el Usuario que asignó y una nota. |

---

#### Crítico Contrato: `registrarMovimientoDeEnvase()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarMovimientoDeEnvase(envaseId identificador, estadoDestino cadena, pedidoId identificador, observacion cadena)` |
| **Responsabilidades** | Ejecutar una transición legal del ciclo de vida físico del envase, actualizar quién lo tiene y registrar el movimiento en su bitácora. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-070. Funciones: IRQ-02, IRQ-13, OBJ-04. |
| **Notas** | Las transiciones válidas están definidas por la máquina de estados del envase: en depósito, lleno, despachado, en poder del cliente, devuelto vacío. Cualquier otra combinación se rechaza, sin excepciones por rol ni por distribuidora. |
| **Excepciones** | Si el envase no existe o es de otra distribuidora → recurso no encontrado. Si la transición no está permitida → error de solicitud. |
| **Salida** | El envase con su nuevo estado. |
| **Precondiciones** | El solicitante es Chofer, Administrador o Administrador General y el Envase pertenece a su Distribuidora. La transición del estado actual al estado destino está permitida. |
| **Postcondiciones** | El atributo estado del Envase pasó al estado destino. Si el destino es «en poder del cliente» y se indicó un Pedido, se formó la asociación entre el Envase y el Cliente de ese Pedido. Si el destino es «devuelto vacío» o «en depósito», se rompió la asociación con el Cliente. Se creó una instancia de MovimientoEnvase con el estado de origen, el de destino, el Pedido, el Usuario y la nota. |

---

#### Crítico Contrato: `crearReserva()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearReserva(items lista, direccionId identificador, fechaAgendada fecha, franjaId identificador, metodoDePago cadena, montoDeLaSenia moneda)` |
| **Responsabilidades** | Crear un pedido agendado para una fecha futura, reservando el stock de forma atómica y registrando el monto de la seña. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-072. Funciones: IRQ-02, IRQ-08, OBJ-01, OBJ-06. |
| **Notas** | Comparte con crearPedido el cálculo de precios con promociones y recargos. Si la seña se paga con la pasarela, se genera el checkout de la seña (crearCheckoutDePago); si la pasarela falla, la reserva queda creada igual, sin enlace de pago. El pedido no se ofrece a ningún chofer hasta el día agendado (activarReservasDelDia). Se notifica a los administradores de la Distribuidora. |
| **Excepciones** | Si falta la fecha agendada o es pasada → error de solicitud. Si la dirección está fuera de la zona de cobertura → error de solicitud. Si la franja no tiene cupo para esa fecha → error de solicitud. Si el stock es insuficiente → error de solicitud y la operación se revierte por completo. Si algún producto no es de la distribuidora → error de solicitud. |
| **Salida** | La reserva creada (número, total, seña, estado reservado) y, si corresponde, el enlace de pago de la seña. |
| **Precondiciones** | El Cliente está autenticado. La DireccionEntrega pertenece al Cliente y está dentro de una ZonaCobertura. La fecha agendada es futura y la FranjaHoraria tiene cupo para ella. Cada Producto existe, es de la Distribuidora y tiene stock suficiente. |
| **Postcondiciones** | Se creó una instancia de Pedido, en estado «reservado», con la fecha agendada y la seña pendiente de pago, asociada al Cliente, a la DireccionEntrega y a la FranjaHoraria. Se crearon sus instancias de ItemPedido, con el precio y el subtotal calculados con las promociones vigentes. El atributo stock de cada Producto pedido se decrementó. Si el pago es con pasarela y la seña es mayor que cero, se creó un Pago por ese importe, marcado como seña, en estado «pendiente». El Pedido no se ofreció a ningún Chofer. |

---

#### Crítico Contrato: `confirmarSenia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `confirmarSenia(pedidoId identificador)` |
| **Responsabilidades** | Registrar que el administrador cobró en efectivo la seña de una reserva, habilitando su activación automática el día agendado. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-074. Funciones: IRQ-08, OBJ-07. |
| **Notas** | Es la única acción humana del ciclo de reservas. Es declarativa: el sistema confía en el registro del administrador y no verifica un comprobante. |
| **Excepciones** | Si la reserva no existe o es de otra distribuidora → recurso no encontrado. Si el pedido no es una reserva con la seña pendiente → error de solicitud. |
| **Salida** | El pedido con la seña registrada. |
| **Precondiciones** | El Administrador está autenticado y la reserva pertenece a su distribuidora. El Pedido tiene estado «reservado» y su seña no está paga. |
| **Postcondiciones** | El atributo seña paga de la instancia de Pedido pasó a verdadero. El estado del Pedido no cambió: sigue «reservado» hasta que el proceso automático lo active. La reserva dejó de ser candidata a expirar por seña impaga. |

---

#### Crítico · automático Contrato: `activarReservasDelDia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `activarReservasDelDia()` |
| **Responsabilidades** | Detectar las reservas cuyo día agendado llegó y cuya seña está paga, pasarlas a pedido pendiente y lanzar su despacho automático. |
| **Tipo** | Sistema (proceso automático) |
| **Referencias cruzadas** | Casos de uso: CU-075. Funciones: IRQ-02, IRQ-14, OBJ-02. |
| **Notas** | Se ejecuta cada 5 minutos y procesa como máximo 50 reservas por corrida. Si el despacho de una reserva activada falla, la activación no se revierte: el proceso temporal de despacho la retoma. Se notifica a cada Chofer al que se le ofrece un Pedido. |
| **Excepciones** | Si la transición de una reserva es inválida → se registra el error y se continúa con las siguientes. Si falla el despacho → se ignora y la reserva queda pendiente. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existen Pedidos «reservados» con la seña paga y con fecha agendada igual o anterior a hoy. |
| **Postcondiciones** | El atributo estado de cada Pedido reservado cuyo día llegó pasó de «reservado» a «pendiente». Se creó una OfertaDespacho por cada Pedido activado que encontró un Chofer cercano. El stock reservado al crear la reserva no se modificó. |

---

#### Importante · automático Contrato: `expirarReservasSinSenia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `expirarReservasSinSenia()` |
| **Responsabilidades** | Cancelar las reservas cuya seña no se pagó dentro del plazo y devolver al inventario el stock que tenían comprometido. |
| **Tipo** | Sistema (proceso automático) |
| **Referencias cruzadas** | Casos de uso: CU-076. Funciones: IRQ-02, IRQ-04, IRQ-14, OBJ-06. |
| **Notas** | El plazo es de 48 horas desde la creación de la reserva. El cambio de estado y la restitución del stock se aplican en una misma transacción, con bloqueo por producto. Procesa como máximo 50 reservas por corrida. |
| **Excepciones** | Si falla la cancelación o la restitución de una reserva → se revierte esa reserva, que queda intacta, y el lote continúa con las demás. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existen Pedidos «reservados» con la seña impaga cuya creación es anterior al plazo. |
| **Postcondiciones** | El atributo estado de cada Pedido reservado sin seña dentro del plazo pasó a «cancelado». Por cada ItemPedido, el atributo stock del Producto se incrementó en la cantidad reservada. Ambos cambios se aplican juntos o no se aplica ninguno. |

---

#### Importante · automático Contrato: `expirarPedidosSinPagar()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `expirarPedidosSinPagar()` |
| **Responsabilidades** | Cancelar los pedidos normales con pago online cuyo checkout el cliente nunca completó, devolviendo al inventario el stock reservado al crearlos. |
| **Tipo** | Sistema (proceso automático) |
| **Referencias cruzadas** | Casos de uso: CU-077. Funciones: IRQ-02, IRQ-04, IRQ-08, OBJ-06. |
| **Notas** | El plazo es de 60 minutos desde la creación del pedido. Es la operación que resuelve por descarte los pagos que nunca llegaron o fueron rechazados. Un pago aprobado que llegue después de la cancelación no reactiva ni despacha el pedido. |
| **Excepciones** | Si al releer el pedido ya no está pendiente o ya tiene un pago confirmado → no se modifica el pedido. Si falla la transacción → se revierte y se continúa con los siguientes. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existen Pedidos «pendientes», con medio de pago MercadoPago y sin pago confirmado, cuya creación es anterior al plazo. |
| **Postcondiciones** | El atributo estado de cada Pedido sin pago confirmado dentro del plazo pasó a «cancelado», con el motivo registrado. Por cada ItemPedido, el atributo stock del Producto se incrementó en la cantidad reservada. |

---

#### Crítico Contrato: `confirmarEntregaConCodigo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `confirmarEntregaConCodigo(pedidoId identificador, codigo cadena)` |
| **Responsabilidades** | Validar que el código escaneado por el cliente coincida con el del pedido, como prueba de que el chofer estuvo presente, y cerrar el pedido como entregado. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-079. Funciones: IRQ-02, IRQ-08, OBJ-03, OBJ-04, OBJ-07. |
| **Notas** | La comparación del código se hace en tiempo constante. La operación es idempotente: una segunda confirmación sobre un pedido ya entregado no reprocesa nada y devuelve el pedido tal cual está. El código lo muestra el chofer con obtenerCodigoDeEntrega. Se notifica al Cliente y a los administradores de la Distribuidora. |
| **Excepciones** | Si el pedido no existe → recurso no encontrado. Si el pedido es de otro cliente → acceso denegado. Si el pedido no está en camino → error de solicitud. Si el código no coincide → error de solicitud (código inválido). Si el pedido ya está entregado → no es error: se devuelve sin reprocesar. |
| **Salida** | El pedido con estado entregado. |
| **Precondiciones** | El Cliente está autenticado y el Pedido es suyo. El Pedido tiene estado «en camino» y tiene un código de entrega. El código recibido coincide con el del Pedido. |
| **Postcondiciones** | El atributo estado del Pedido pasó a «entregado». Si el método de pago es efectivo, el atributo estado del Pago asociado pasó a «pagado». Se cerró el seguimiento de la UbicacionGPS del Chofer para este Pedido. Cada Envase despachado en el Pedido pasó a «en poder del cliente», con su MovimientoEnvase registrado. |

---

#### Importante Contrato: `eliminarUsuario()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarUsuario(usuarioId identificador)` |
| **Responsabilidades** | Dar de baja una cuenta de usuario mediante una baja lógica, junto con su perfil y sus direcciones, y deshabilitar su cuenta de acceso. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-085. Funciones: IRQ-01, OBJ-05. |
| **Notas** | La baja se conserva para el historial y la auditoría. Los vehículos no se dan de baja: la flota es de la distribuidora. Un Administrador de empresa sólo da de baja a su personal; la cuenta de un Cliente la da de baja el Administrador General. |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el usuario no existe o no es de la distribuidora en contexto → recurso no encontrado. Si un Administrador de empresa intenta dar de baja a un Cliente → acceso denegado. Si el usuario es un Chofer con pedidos aceptados o en camino → error de conflicto (hay que cancelarlos o reasignarlos antes). Si no se puede deshabilitar la cuenta de acceso → la baja lógica queda hecha y el sistema registra la cuenta pendiente. |
| **Salida** | Ninguna. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Usuario existe y, si hay distribuidora en contexto, pertenece a ella. Si el Usuario es un Chofer, no tiene Pedidos «aceptados» ni «en camino». |
| **Postcondiciones** | El atributo fecha de baja de la instancia de Usuario, de su Cliente o Chofer y de sus DireccionEntrega tomó la fecha actual; dejaron de aparecer en las consultas y se conservan para el historial. Si el Usuario era un Chofer, se cerró su AsignacionVehiculo abierta, dejó de tener un Vehiculo en uso y se eliminó su UbicacionGPS, de modo que no recibe más ofertas. La cuenta de acceso quedó deshabilitada. No se eliminó ninguna instancia de Vehiculo ni de Pedido. |

---

#### Importante Contrato: `registrarAdministrador()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarAdministrador(nombreCompleto cadena, correo cadena, telefono cadena, contrasena cadena, rol cadena, distribuidoraId identificador)` |
| **Responsabilidades** | Dar de alta a un administrador de empresa o a un Administrador General desde el panel, según las reglas de quien lo registra. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-086. Funciones: IRQ-01, OBJ-05. |
| **Notas** | El Administrador General crea administradores en cualquier distribuidora y también otros administradores generales. Un Administrador de empresa sólo crea administradores de su propia distribuidora y nunca administradores generales. La creación del Usuario la resuelve el caso incluido CU-082. |
| **Excepciones** | Si falta un dato o tiene un formato inválido → error de solicitud. Si un Administrador de empresa intenta crear un Administrador General, o indica otra distribuidora, o no tiene una asociada → acceso denegado. Si el Administrador General pide un administrador de empresa sin indicar distribuidora → error de solicitud. Si el correo o el teléfono ya están en uso → error de conflicto. |
| **Salida** | Los datos del administrador creado (identificador, rol, distribuidora). |
| **Precondiciones** | El solicitante es Administrador o Administrador General. Si es Administrador de empresa, tiene una Distribuidora asociada. No existe un Usuario con el mismo correo ni con el mismo teléfono. |
| **Postcondiciones** | Se creó una instancia de Usuario con el rol correspondiente y una instancia de Administrador asociada a él. Si es un administrador de empresa, el Administrador quedó asociado a la Distribuidora que corresponde según quién lo creó. |

---

#### Importante Contrato: `crearPrimerSuperAdministrador()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearPrimerSuperAdministrador(nombreCompleto cadena, correo cadena, telefono cadena, contrasena cadena)` |
| **Responsabilidades** | Crear la primera cuenta de Administrador General, en la puesta en marcha del sistema. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-087. Funciones: IRQ-01, OBJ-05. |
| **Notas** | No existe una operación pública para esto: se ejecuta desde el servidor, por quien tiene acceso a la máquina donde corre el sistema. Los roles del sistema deben haberse sembrado antes (sembrarRolesIniciales). |
| **Excepciones** | Si falta algún dato → no se crea nada y se informa. Si ya existe un Administrador General → se rechaza y no se crea nada. Si el correo o el teléfono ya están en uso, o el proveedor de identidad rechaza la cuenta → se informa el motivo. |
| **Salida** | Los datos del Administrador General creado. |
| **Precondiciones** | No existe ninguna instancia de Usuario con el rol Administrador General. El Rol Administrador General existe. |
| **Postcondiciones** | Se creó una instancia de Usuario con el rol Administrador General y una instancia de Administrador asociada a él. El sistema tiene su primer Administrador General, que puede entrar al panel y crear el resto de las cuentas. |

---

#### Importante Contrato: `actualizarRol()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarRol(rolId identificador, datos registro)` |
| **Responsabilidades** | Modificar los datos de un rol del catálogo. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-253. Funciones: IRQ-01, OBJ-05. |
| **Notas** | El cambio impacta de inmediato en la autorización de los usuarios que tienen el rol asignado. |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el rol no existe → recurso no encontrado. Si quien opera no es Administrador General → acceso denegado. |
| **Salida** | El rol actualizado. |
| **Precondiciones** | El solicitante es Administrador General autenticado. El Rol existe. |
| **Postcondiciones** | Los atributos de la instancia de Rol enviados tomaron los valores nuevos. |

---

#### Importante Contrato: `crearRol()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearRol(tipo cadena)` |
| **Responsabilidades** | Crear un rol en el catálogo que gobierna la autorización del sistema. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-252. Funciones: IRQ-01, OBJ-05. |
| **Notas** | El rol determina los permisos de las cuentas que lo tienen asignado. Es exclusivo del Administrador General. |
| **Excepciones** | Si los datos no cumplen el formato → error de solicitud. Si quien opera no es Administrador General → acceso denegado. |
| **Salida** | El rol creado. |
| **Precondiciones** | El solicitante es Administrador General autenticado. |
| **Postcondiciones** | Se creó una instancia de Rol con el tipo indicado, que no coincide con el de ningún otro Rol. |

---

#### Importante Contrato: `eliminarRol()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarRol(rolId identificador)` |
| **Responsabilidades** | Eliminar un rol del catálogo. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-254. Funciones: IRQ-01, OBJ-05. |
| **Notas** | Un rol del sistema o con usuarios asignados no se puede eliminar. La baja es lógica, como en todo el sistema. |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el rol no existe → recurso no encontrado. Si el rol es del sistema o tiene usuarios asignados → error de conflicto y no se elimina. Si quien opera no es Administrador General → acceso denegado. |
| **Salida** | Ninguna. |
| **Precondiciones** | El solicitante es Administrador General autenticado. El Rol existe y ningún Usuario lo tiene asignado. |
| **Postcondiciones** | La instancia de Rol quedó dada de baja lógica (se le asignó la fecha de baja); no se borra físicamente. |

---

#### Importante Contrato: `sembrarRolesIniciales()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `sembrarRolesIniciales()` |
| **Responsabilidades** | Inicializar el catálogo de roles con los cuatro roles que la autorización necesita: cliente, chofer, administrador y administrador general. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-090. Funciones: IRQ-01, OBJ-05. |
| **Notas** | La operación es repetible sin efectos secundarios: los roles que ya existen no se duplican. Debe ejecutarse antes de crear el primer Administrador General. |
| **Excepciones** | Si quien opera no es Administrador General → acceso denegado. Si la escritura de algún rol falla → error interno y los roles creados antes de la falla quedan guardados. |
| **Salida** | Los roles del catálogo. |
| **Precondiciones** | El solicitante es Administrador General autenticado. |
| **Postcondiciones** | Existe una instancia de Rol por cada uno de los cuatro roles del sistema; se crearon las que faltaban y las existentes no se modificaron. |

---

#### Secundario Contrato: `actualizarUbicacionDelCliente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarUbicacionDelCliente(clienteId identificador, coordenadas coordenada)` |
| **Responsabilidades** | Actualizar la coordenada de referencia guardada en el perfil del cliente. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-094. Funciones: IRQ-01, IRQ-07, OBJ-01, OBJ-02. |
| **Notas** | El Cliente actualiza la propia; el Administrador actualiza la de los clientes que le compraron a su distribuidora. Es distinta de la dirección de entrega de cada pedido. |
| **Excepciones** | Si el identificador no es válido o la coordenada no es un par latitud,longitud válido → error de solicitud. Si el cliente no existe, o es un cliente que nunca le compró a la distribuidora del Administrador → recurso no encontrado. Si un Cliente intenta modificar el perfil de otro → acceso denegado. |
| **Salida** | El cliente con la coordenada actualizada. |
| **Precondiciones** | El solicitante está autenticado. Si no es Administrador, el Cliente indicado es él mismo. Si es Administrador, el Cliente le compró alguna vez a su Distribuidora. |
| **Postcondiciones** | El atributo coordenadas de la instancia de Cliente tomó el valor enviado. |

---

#### Importante Contrato: `eliminarCliente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarCliente(clienteId identificador)` |
| **Responsabilidades** | Dar de baja el perfil de un cliente mediante una baja lógica. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-095. Funciones: IRQ-01, OBJ-05. |
| **Notas** | Sólo la hace el Administrador General: un cliente puede comprarle a varias distribuidoras y darlo de baja lo saca de todas. La baja alcanza al perfil de Cliente, no al Usuario base; para impedir el acceso se da de baja al Usuario (eliminarUsuario) o se lo bloquea (bloquearUsuario). |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el cliente no existe, o nunca le compró a la distribuidora en contexto → recurso no encontrado. Si quien opera es un Administrador de empresa → acceso denegado. |
| **Salida** | Ninguna. |
| **Precondiciones** | El solicitante es Administrador General autenticado. El Cliente existe y, si hay distribuidora en contexto, le compró alguna vez a ella. |
| **Postcondiciones** | El atributo fecha de baja de la instancia de Cliente tomó la fecha actual y dejó de aparecer en las consultas. La instancia de Usuario y las instancias de Pedido se conservaron. |

---

#### Importante Contrato: `actualizarPerfilDelChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarPerfilDelChofer(choferId identificador, datos registro)` |
| **Responsabilidades** | Cambiar, desde el panel, la marca de validación del perfil de un chofer. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-096. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | Es el único campo que la operación acepta; cualquier otro dato, incluido el estado de actividad, se rechaza. El estado de actividad se cambia con cambiarEstadoDelChofer. Tiene el mismo efecto que validarChofer e invalidarChofer. |
| **Excepciones** | Si el identificador no es válido, o el cuerpo trae otro campo, o la marca de validación no es verdadero o falso → error de solicitud y no se modifica nada. Si el chofer no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | El chofer actualizado. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Chofer existe y, si hay distribuidora en contexto, pertenece a ella. |
| **Postcondiciones** | El atributo validado de la instancia de Chofer tomó el valor enviado. Ningún otro atributo se modificó. |

---

#### Importante Contrato: `eliminarChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarChofer(choferId identificador)` |
| **Responsabilidades** | Dar de baja a un chofer: su perfil y su cuenta de usuario, mediante una baja lógica, y liberar el vehículo que tenía en uso. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-097. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Se conservan el perfil y el historial de entregas. El vehículo sigue vigente y puede asignarse a otro chofer. Si el proveedor de identidad o el radar fallan después de confirmada la baja, la baja no se revierte. |
| **Excepciones** | Si el identificador no es válido → error de solicitud. Si el chofer no existe o es de otra distribuidora → recurso no encontrado. Si el chofer tiene pedidos aceptados o en camino → error de conflicto (hay que cancelarlos o reasignarlos antes) y no se da de baja. |
| **Salida** | Ninguna. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Chofer existe, pertenece a la Distribuidora en contexto y no tiene Pedidos «aceptados» ni «en camino». |
| **Postcondiciones** | El atributo fecha de baja de las instancias de Chofer y de su Usuario tomó la fecha actual; dejaron de aparecer en las consultas y se conservaron con su historial. Se cerró su AsignacionVehiculo abierta, de modo que no tiene Vehiculo en uso, y se eliminó su UbicacionGPS. El Vehiculo se conservó. |

---

#### Crítico Contrato: `registrarTokenDeNotificaciones()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarTokenDeNotificaciones(usuarioId identificador, token cadena, plataforma cadena)` |
| **Responsabilidades** | Registrar el token de notificaciones push del dispositivo contra el perfil del usuario. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-098. Funciones: IRQ-01, IRQ-03, OBJ-01, OBJ-03. |
| **Notas** | Es la precondición técnica para que lleguen las notificaciones push. Cada perfil guarda un único token: registrar uno nuevo reemplaza al anterior, de modo que un usuario con dos dispositivos recibe las notificaciones en el último que registró. |
| **Excepciones** | Si el token está vacío → error de solicitud. Si el identificador no corresponde a un Cliente ni a un Chofer → la respuesta informa que el usuario no se encontró. |
| **Salida** | Si el registro tuvo éxito. |
| **Precondiciones** | El Usuario está autenticado y tiene una instancia de Cliente o de Chofer. El dispositivo concedió permiso de notificaciones a la app. |
| **Postcondiciones** | El atributo token de notificaciones de la instancia de Cliente o de Chofer tomó el valor enviado, y reemplazó al anterior. |

---

#### Importante Contrato: `eliminarFranjaHoraria()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarFranjaHoraria(franjaId identificador)` |
| **Responsabilidades** | Retirar del uso una franja horaria de entrega de la distribuidora, mediante una desactivación. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-103. Funciones: IRQ-05, OBJ-05, OBJ-08. |
| **Notas** | El registro se conserva para no romper los pedidos que la referencian: los pedidos ya agendados mantienen su franja. La franja deja de ofrecerse para agendar nuevos pedidos. |
| **Excepciones** | Si el identificador no es válido o no hay distribuidora en el contexto → error de solicitud. Si la franja no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | Ninguna. |
| **Precondiciones** | El Administrador está autenticado y tiene una distribuidora en contexto. La FranjaHoraria existe y pertenece a esa Distribuidora. |
| **Postcondiciones** | El atributo activa de la instancia de FranjaHoraria pasó a falso. La FranjaHoraria dejó de aparecer en el listado y en la consulta de disponibilidad. Los Pedidos agendados a ella conservan su asociación. |

---

#### Importante Contrato: `aceptarVentanaDeMantenimiento()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `aceptarVentanaDeMantenimiento(propuestaId identificador)` |
| **Responsabilidades** | Registrar que el chofer acepta la ventana de taller que se le propuso, a la espera de la confirmación del administrador. |
| **Tipo** | Sistema (planificado, I-10) |
| **Referencias cruzadas** | Casos de uso: CU-105. Funciones: IRQ-02, IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | Es la decisión del chofer dentro de la propuesta con vigencia limitada. Si la deja vencer o la rechaza, se pasa a la siguiente ventana. |
| **Excepciones** | Si la propuesta venció o ya fue cerrada → rechazo. |
| **Salida** | La propuesta aceptada, pendiente de la confirmación del administrador. |
| **Precondiciones** | El Chofer está autenticado. La PropuestaVentanaTaller está dirigida a él y su estado es «ofrecida», dentro de su vigencia. |
| **Postcondiciones** | El atributo estado de la instancia de PropuestaVentanaTaller pasó a «aceptada». La TareaMantenimiento quedó programada con esa ventana, pendiente de la confirmación del Administrador. |

---

#### Importante Contrato: `confirmarVentanaDeTaller()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `confirmarVentanaDeTaller(tareaId identificador, ventanaElegida registro, gastoEstimado moneda)` |
| **Responsabilidades** | Resolver, por decisión del administrador, la ventana de taller de una tarea cuando ninguna alternativa prosperó con el chofer. |
| **Tipo** | Sistema (planificado, I-10) |
| **Referencias cruzadas** | Casos de uso: CU-105. Funciones: IRQ-02, IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | El administrador decide con el cuadro de opciones evaluadas y el motivo de cada descarte a la vista. El sistema no contrata nada por su cuenta. |
| **Excepciones** | Si la tarea no existe o es de otra distribuidora → recurso no encontrado. Si la ventana elegida no está entre las evaluadas → error de solicitud. |
| **Salida** | La tarea programada. |
| **Precondiciones** | El Administrador está autenticado. La TareaMantenimiento es de su Distribuidora y está pendiente de su decisión. |
| **Postcondiciones** | La instancia de TareaMantenimiento quedó programada con la ventana elegida y el gasto estimado indicados. |

---

#### Importante · automático Contrato: `planificarMantenimientoDeFlota()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `planificarMantenimientoDeFlota()` |
| **Responsabilidades** | Proyectar el vencimiento de cada tarea de mantenimiento y de cada habilitación de la flota, y negociar con el chofer la ventana de taller que menos perjudica a la operación. |
| **Tipo** | Sistema (proceso automático) (planificado, I-10) |
| **Referencias cruzadas** | Casos de uso: CU-105. Funciones: IRQ-02, IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | Se ejecuta una vez por día, a la hora configurada. La ventana no se impone: se ofrece al chofer de a una alternativa por vez, con vigencia limitada. Si ninguna prospera, el caso queda a resolución del administrador con el cuadro completo. Un vehículo con una habilitación bloqueante vencida deja de recibir ofertas de pedidos. Se notifica al Chofer y al Administrador. |
| **Excepciones** | Si el vehículo no tiene historial de uso ni promedio de flota para su tipo → la tarea queda en observación y sólo se evalúan sus habilitaciones por fecha fija. Si ninguna ventana es factible o el vehículo no tiene chofer → se escala al administrador. Si la tarea llega a su fecha sin ventana acordada → se marca vencida. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | El Vehiculo existe y pertenece a una Distribuidora activa. Tiene al menos un PlanMantenimiento aplicable. |
| **Postcondiciones** | Cada TareaMantenimiento dentro de la ventana de anticipación tiene su fecha de vencimiento proyectada. Se creó una instancia de PropuestaVentanaTaller, en estado «ofrecida», por cada ventana propuesta a un Chofer. Si hay una habilitación bloqueante vencida, el Vehiculo quedó fuera de servicio. |

---

#### Importante Contrato: `aceptarInvitacionDeRecompra()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `aceptarInvitacionDeRecompra(invitacionId identificador)` |
| **Responsabilidades** | Crear el pedido sugerido cuando el cliente acepta la invitación de recompra dentro de su vigencia. |
| **Tipo** | Sistema (planificado, I-6) |
| **Referencias cruzadas** | Casos de uso: CU-106. Funciones: IRQ-01, IRQ-02, IRQ-04, OBJ-01. |
| **Notas** | Si el precio cambió entre la emisión y la aceptación, el cliente confirma sobre el importe vigente. Si compró por su cuenta mientras la invitación corría, la invitación se cierra sin efecto. |
| **Excepciones** | Si la invitación venció o ya fue cerrada → rechazo. Si el stock ya no alcanza → el pedido no se crea, se avisa al cliente y la invitación se cierra sin efecto. |
| **Salida** | El pedido creado, en búsqueda de chofer. |
| **Precondiciones** | El Cliente está autenticado. La InvitacionRecompra es suya, está «ofrecida» y dentro de su vigencia. Hay stock suficiente. |
| **Postcondiciones** | El atributo estado de la instancia de InvitacionRecompra pasó a «aceptada». Se creó una instancia de Pedido, «pendiente», con las ItemPedido de los ItemSugerido, asociada al Cliente, y se creó una OfertaDespacho para el Chofer más cercano. |

---

#### Importante · automático Contrato: `anticiparRecompras()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `anticiparRecompras()` |
| **Responsabilidades** | Estimar, para cada cliente con historial, cuándo se le termina el gas y ofrecerle la reposición con el pedido armado antes de que la necesite. |
| **Tipo** | Sistema (proceso automático) (planificado, I-6) |
| **Referencias cruzadas** | Casos de uso: CU-106. Funciones: IRQ-01, IRQ-02, IRQ-04, OBJ-01. |
| **Notas** | Se ejecuta una vez por día. La decisión es del cliente: el sistema no crea ningún pedido hasta que acepta. La caducidad y el intervalo mínimo entre invitaciones evitan que se vuelva insistencia. Se notifica al Cliente. |
| **Excepciones** | Si el cliente no llega al mínimo de pedidos, o su serie es demasiado irregular → queda fuera de la corrida. Si no hay stock del producto sugerido → no se emite la invitación. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | El Cliente tiene al menos la cantidad mínima configurada de Pedidos «entregados», no tiene un Pedido activo y no recibió una invitación dentro del intervalo mínimo. |
| **Postcondiciones** | Se creó una instancia de InvitacionRecompra, en estado «ofrecida», asociada al Cliente, con sus instancias de ItemSugerido y una vigencia limitada. Las invitaciones vencidas pasaron a «caducada». |

---

#### Importante Contrato: `aceptarRecorrido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `aceptarRecorrido(recorridoId identificador)` |
| **Responsabilidades** | Asignar al chofer que acepta el lote completo de pedidos, con sus paradas en el orden establecido. |
| **Tipo** | Sistema (planificado, I-9) |
| **Referencias cruzadas** | Casos de uso: CU-107. Funciones: IRQ-02, IRQ-03, IRQ-05, OBJ-02, OBJ-08. |
| **Notas** | Si al aceptar alguno de los pedidos ya no está disponible, se asigna el resto del lote y el faltante se descuenta del recorrido. |
| **Excepciones** | Si la oferta venció o ya fue cerrada → rechazo. |
| **Salida** | Los pedidos asignados en el orden establecido. |
| **Precondiciones** | El Chofer está autenticado. La OfertaLote está dirigida a él y está «ofrecida», dentro de su vigencia. |
| **Postcondiciones** | El atributo estado de la OfertaLote pasó a «aceptada». Se formó la asociación entre cada Pedido del LoteRecorrido y el Chofer, y cada Pedido pasó a «aceptado». |

---

#### Importante · automático Contrato: `agruparPedidosPorRecorrido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `agruparPedidosPorRecorrido()` |
| **Responsabilidades** | Armar lotes de pedidos programados que se pueden entregar en un mismo viaje y negociarlos con los choferes de a uno por vez. |
| **Tipo** | Sistema (proceso automático) (planificado, I-9) |
| **Referencias cruzadas** | Casos de uso: CU-107. Funciones: IRQ-02, IRQ-03, IRQ-05, OBJ-02, OBJ-08. |
| **Notas** | El lote nunca se impone: ante el silencio o el rechazo generalizado, los pedidos siguen su camino individual y ninguno queda retenido por la agrupación. Respeta el compromiso horario de cada pedido y la capacidad del vehículo. Se notifica a cada Chofer candidato. |
| **Excepciones** | Si no hay pedidos suficientes para un lote → no se hace nada. Si ningún vehículo tiene capacidad para el lote → se recorta o se descarta. Si un pedido es aceptado o cancelado mientras la oferta corre → se recalcula el lote. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Hay al menos dos Pedidos programados de la misma Distribuidora, dentro del radio de agrupación y con franjas compatibles, y al menos un Chofer activo con capacidad de carga disponible. |
| **Postcondiciones** | Se creó una instancia de LoteRecorrido con una instancia de ParadaLote por cada Pedido, en su orden de entrega, y una instancia de OfertaLote dirigida a cada Chofer candidato. Si ningún Chofer lo tomó, el LoteRecorrido se deshizo y los Pedidos volvieron al circuito individual. |

---

#### Importante Contrato: `aceptarRetiroEnLaEntrega()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `aceptarRetiroEnLaEntrega(ofertaId identificador)` |
| **Responsabilidades** | Registrar que el cliente acepta que el chofer retire el envase retenido en una entrega ya programada. |
| **Tipo** | Sistema (planificado, I-8) |
| **Referencias cruzadas** | Casos de uso: CU-108. Funciones: IRQ-01, IRQ-02, OBJ-04, OBJ-05. |
| **Notas** | Aprovecha una entrega programada como oportunidad de recupero sin costo adicional. |
| **Excepciones** | Si la oferta venció o ya fue cerrada → rechazo. Si el chofer no logra retirar el envase → el caso vuelve al escalón en el que estaba. |
| **Salida** | El retiro acordado para esa entrega. |
| **Precondiciones** | El Cliente está autenticado. El AvisoRecupero con la oferta de retiro es suyo y está vigente. Hay una entrega programada al Cliente. |
| **Postcondiciones** | El atributo estado del AvisoRecupero pasó a «aceptado» y quedó asociado al Pedido de esa entrega, que incluye el retiro del Envase. |

---

#### Importante · automático Contrato: `gestionarEnvasesNoDevueltos()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `gestionarEnvasesNoDevueltos()` |
| **Responsabilidades** | Detectar los envases retenidos por un cliente por encima del plazo de tolerancia y gestionar su recupero mediante una secuencia escalonada. |
| **Tipo** | Sistema (proceso automático) (planificado, I-8) |
| **Referencias cruzadas** | Casos de uso: CU-108. Funciones: IRQ-01, IRQ-02, OBJ-04, OBJ-05. |
| **Notas** | Cada escalón tiene su propio plazo y el caso se reevalúa antes de cada paso: el envase puede haber vuelto. El sistema nunca cobra un depósito por su cuenta: agotada la secuencia, el caso queda a resolución del administrador. |
| **Excepciones** | Si el último movimiento del envase no permite saber en poder de quién está → queda marcado para revisión manual. Si el envase vuelve en cualquier punto → el caso se cierra. Si el cliente no tiene una entrega programada → se saltea la oferta de retiro. Si el importe no supera el umbral → el caso queda registrado como envase perdido. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existe al menos un Envase en poder de un Cliente con una antigüedad mayor al plazo de tolerancia configurado. |
| **Postcondiciones** | Se creó una instancia de CasoRecupero por cada Envase retenido, con una instancia de AvisoRecupero por cada escalón ejecutado. Si el Envase volvió, el CasoRecupero se cerró. Si se agotó la secuencia y el importe supera el umbral, el CasoRecupero quedó escalado al Administrador. Ningún depósito se cobró ni se dio de baja ningún Envase. |

---

#### Importante Contrato: `resolverCasoDeRecupero()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `resolverCasoDeRecupero(casoId identificador, decision cadena)` |
| **Responsabilidades** | Resolver, por decisión del administrador, un caso de recupero escalado: cobrar el depósito, dar de baja el envase o cerrarlo sin cargo. |
| **Tipo** | Sistema (planificado, I-8) |
| **Referencias cruzadas** | Casos de uso: CU-108. Funciones: IRQ-01, IRQ-02, OBJ-04, OBJ-05. |
| **Notas** | El administrador decide con el legajo completo del caso (cliente, historial del envase, importe). El sistema nunca ejecuta el cobro ni la baja sin una decisión registrada. |
| **Excepciones** | Si el caso no existe o es de otra distribuidora → recurso no encontrado. Si el caso no está escalado → error de solicitud. |
| **Salida** | La resolución registrada. |
| **Precondiciones** | El Administrador está autenticado. El CasoRecupero es de su Distribuidora y está escalado. |
| **Postcondiciones** | El CasoRecupero quedó cerrado con la decisión registrada. Si la decisión fue dar de baja el Envase, el atributo estado del Envase pasó a «dado de baja». |

---

#### Importante Contrato: `agregarItemAlCarrito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `agregarItemAlCarrito(productoId identificador, cantidad entero)` |
| **Responsabilidades** | Sumar un tipo de garrafa al carrito del cliente con una cantidad, para armar la compra en varios momentos. |
| **Tipo** | Sistema (planificado, I-3) |
| **Referencias cruzadas** | Casos de uso: CU-122. Funciones: IRQ-02, OBJ-01. |
| **Notas** | El carrito sobrevive al cierre de la aplicación y al cambio de dispositivo. Es el primer paso del proceso de compra que termina en crearPedido. Si el tipo de garrafa ya está en el carrito, se suma la cantidad al ítem existente y no se agrega otro. |
| **Excepciones** | Si el tipo de garrafa no existe, está dado de baja o es de otra distribuidora → rechazo. Si la cantidad no es un entero positivo → rechazo. |
| **Salida** | El carrito con el total actualizado. |
| **Precondiciones** | El Cliente está autenticado. El Producto existe, está activo y pertenece a la Distribuidora. |
| **Postcondiciones** | Si el Cliente no tenía un Carrito en la Distribuidora, se creó una instancia de Carrito. Si el Producto ya estaba en el Carrito, el atributo cantidad de su ItemCarrito aumentó en la cantidad pedida; si no, se creó una instancia de ItemCarrito, asociada al Carrito y al Producto, con la cantidad pedida. El total del Carrito quedó actualizado. |

---

#### Importante Contrato: `modificarCantidadDelItem()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarCantidadDelItem(itemId identificador, cantidad entero)` |
| **Responsabilidades** | Cambiar cuántas garrafas de un tipo quiere el cliente sin sacar el ítem y volver a agregarlo. |
| **Tipo** | Sistema (planificado, I-3) |
| **Referencias cruzadas** | Casos de uso: CU-123. Funciones: IRQ-02, OBJ-01. |
| **Notas** | Poner la cantidad en cero y quitar el ítem son dos intenciones distintas: para dejarlo en cero hay que usar quitarItemDelCarrito. |
| **Excepciones** | Si el ítem no está en el carrito del cliente → rechazo. Si la cantidad es cero o negativa → rechazo. |
| **Salida** | El carrito con el total actualizado. |
| **Precondiciones** | El Cliente está autenticado y el ItemCarrito está en su Carrito. |
| **Postcondiciones** | El atributo cantidad de la instancia de ItemCarrito tomó el valor pedido y el total del Carrito reflejó el cambio. |

---

#### Importante Contrato: `quitarItemDelCarrito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `quitarItemDelCarrito(itemId identificador)` |
| **Responsabilidades** | Sacar del carrito un tipo de garrafa que el cliente había agregado. |
| **Tipo** | Sistema (planificado, I-3) |
| **Referencias cruzadas** | Casos de uso: CU-124. Funciones: IRQ-02, OBJ-01. |
| **Notas** | El ítem se borra físicamente: un carrito no es un documento contable y no hay nada que auditar en lo que el cliente descartó antes de comprar. |
| **Excepciones** | Si el ítem no está en el carrito del cliente → rechazo. |
| **Salida** | El carrito con el total actualizado. |
| **Precondiciones** | El Cliente está autenticado y el ItemCarrito está en su Carrito. |
| **Postcondiciones** | Se eliminó la instancia de ItemCarrito y el total del Carrito reflejó la baja. |

---

#### Menor Contrato: `vaciarCarrito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `vaciarCarrito()` |
| **Responsabilidades** | Descartar de una vez todo lo que el cliente había armado en su carrito. |
| **Tipo** | Sistema (planificado, I-3) |
| **Referencias cruzadas** | Casos de uso: CU-126. Funciones: IRQ-02, OBJ-01. |
| **Notas** | El sistema también vacía el carrito por su cuenta cuando crearPedido registra la compra, para que el cliente no arranque la próxima con lo que ya compró. |
| **Excepciones** | Si el cliente no tiene carrito → se devuelve un carrito vacío y no se hace nada. |
| **Salida** | El carrito vacío. |
| **Precondiciones** | El Cliente está autenticado y tiene un Carrito con ítems. |
| **Postcondiciones** | Se eliminaron las instancias de ItemCarrito del Carrito, que quedó sin ítems y con total en cero. |

---

#### Importante Contrato: `cambiarDireccionDeEntrega()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cambiarDireccionDeEntrega(pedidoId identificador, direccionId identificador, motivo cadena)` |
| **Responsabilidades** | Cambiar a dónde quiere el cliente que le lleven un pedido ya confirmado, mientras no salió el repartidor, dejando asentado el motivo. |
| **Tipo** | Sistema (planificado, I-4) |
| **Referencias cruzadas** | Casos de uso: CU-127. Funciones: IRQ-02, OBJ-01. |
| **Notas** | El pedido pagado en línea conserva su total: si el recargo de la zona nueva es distinto del de la zona original, se rechaza el cambio y el cliente debe cancelar y volver a pedir. El pedido pagado en efectivo recalcula el total si el recargo cambió. |
| **Excepciones** | Si el pedido ya está en camino o entregado → rechazo. Si la dirección es de otro cliente → rechazo. Si la dirección queda fuera de la zona de cobertura → rechazo con el motivo. Si el pedido está pagado en línea y el recargo de la zona nueva difiere → rechazo. |
| **Salida** | El pedido con la dirección nueva. |
| **Precondiciones** | El Cliente está autenticado, el Pedido es suyo y su estado es «pendiente» o «aceptado». La DireccionEntrega nueva es del Cliente y está dentro de una ZonaCobertura. |
| **Postcondiciones** | Se rompió la asociación entre el Pedido y su DireccionEntrega anterior y se formó con la nueva. Se creó una instancia de CambioDireccion con la dirección de origen, la de destino, el autor y el motivo. Si el pago es en efectivo y el recargo cambió, el atributo total del Pedido quedó recalculado. |

---

#### Importante Contrato: `indicarQuienRecibe()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `indicarQuienRecibe(pedidoId identificador, nombre cadena, documento cadena, relacion cadena)` |
| **Responsabilidades** | Dejar asentado que otra persona va a recibir el pedido: su nombre, su documento y su relación con el cliente. |
| **Tipo** | Sistema (planificado, I-4) |
| **Referencias cruzadas** | Casos de uso: CU-128. Funciones: IRQ-02, OBJ-01, OBJ-04. |
| **Notas** | El chofer ve los datos para saber a quién entregar. Los datos se conservan hasta que vence el plazo de reclamo del pedido y después quedan anulados. |
| **Excepciones** | Si el pedido ya fue entregado → rechazo. Si el documento no tiene un formato válido → rechazo. |
| **Salida** | El pedido con los datos de quien recibe. |
| **Precondiciones** | El Cliente está autenticado, el Pedido es suyo y su estado no es «entregado». |
| **Postcondiciones** | Los atributos nombre, documento y relación de quien recibe de la instancia de Pedido tomaron los valores indicados. |

---

#### Importante Contrato: `editarDatosDelCliente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `editarDatosDelCliente(clienteId identificador, cambios registro)` |
| **Responsabilidades** | Corregir los datos de la ficha de un cliente desde el panel. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-131. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Es la modificación del ABM de clientes, separada de la actualización de ubicación (actualizarUbicacionDelCliente) y de la baja (eliminarCliente). |
| **Excepciones** | Si el identificador no es válido o se envía un campo no declarado → error de solicitud. Si el cliente no existe o nunca le compró a la distribuidora del administrador → recurso no encontrado. |
| **Salida** | La ficha del cliente actualizada. |
| **Precondiciones** | El solicitante está autenticado. El Cliente existe y, si quien pide es un Administrador con distribuidora en contexto, le compró alguna vez a ella. |
| **Postcondiciones** | Los atributos de la instancia de Cliente enviados tomaron los valores corregidos. |

---

#### Crítico Contrato: `registrarRevisionDeEnvase()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarRevisionDeEnvase(envaseId identificador, fecha fecha, resultado cadena, vencimiento fecha)` |
| **Responsabilidades** | Asentar la prueba hidráulica periódica de un envase: la fecha en que se hizo, el resultado y cuándo vence. |
| **Tipo** | Sistema (planificado, I-2) |
| **Referencias cruzadas** | Casos de uso: CU-132. Funciones: IRQ-05, OBJ-06. |
| **Notas** | Un envase con la revisión vencida no se puede llenar ni despachar (CU-135). Si el resultado es el rechazo y el envase está en poder de un cliente, queda marcado para retirarlo y no se lo saca de circulación hasta que vuelva. |
| **Excepciones** | Si el envase no existe o es de otra distribuidora → rechazo. Si la fecha de revisión es futura o el vencimiento es anterior a ella → rechazo. |
| **Salida** | El envase con su revisión asentada. |
| **Precondiciones** | El Administrador está autenticado. El Envase existe y es de su Distribuidora. |
| **Postcondiciones** | Se creó una instancia de RevisionEnvase asociada al Envase, con la fecha, el resultado y el vencimiento. Los atributos última revisión y vencimiento del Envase tomaron los valores de la revisión. |

---

#### Crítico Contrato: `crearTareaDeFlota()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearTareaDeFlota(planId identificador, recursoId identificador, vencimiento fecha, detalle registro)` |
| **Responsabilidades** | Registrar una tarea de mantenimiento contra un plan: el seguro o la verificación técnica de un vehículo, la licencia de un chofer o un service programado. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-136, CU-137, CU-138, CU-140, CU-197. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Es una única operación parametrizada por plan: CU-136 (seguro, con aseguradora y póliza), CU-137 (verificación técnica), CU-138 (licencia, con número y categoría) y CU-140 (service, con fecha o kilometraje previstos) y CU-197 (habilitación para transportar mercancías peligrosas) la usan con distinto plan. Un vehículo o un chofer con un vencimiento bloqueante vencido queda inhabilitado. |
| **Excepciones** | Si el plan no existe o es de otra distribuidora → recurso no encontrado. Si el vehículo o el chofer no existen o son de otra distribuidora → recurso no encontrado. Si el plan es de vehículo y no se indica el vehículo, o se indica además un chofer (o al revés para un plan de chofer) → error de solicitud. |
| **Salida** | La tarea creada. |
| **Precondiciones** | El Administrador está autenticado. El PlanMantenimiento existe, está activo y es de su Distribuidora. El Vehiculo o el Chofer indicado existe y es de su Distribuidora. |
| **Postcondiciones** | Se creó una instancia de TareaMantenimiento asociada al PlanMantenimiento y al Vehiculo o al Chofer, con el vencimiento y el detalle indicados. Si el vencimiento ya pasó, la tarea queda creada igual y el Vehiculo o el Chofer figura inhabilitado. |

---

#### Importante Contrato: `cerrarTareaDeFlota()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cerrarTareaDeFlota(tareaId identificador, fecha fecha, kilometraje entero, costo moneda, observacion cadena)` |
| **Responsabilidades** | Cerrar una tarea de mantenimiento agendada: anotar cuándo se hizo, el kilometraje, el costo y el proveedor. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-141. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Construye el historial del vehículo o del chofer. La tarea cerrada deja de figurar entre las habilitaciones vencidas o por vencer. |
| **Excepciones** | Si la tarea no existe o es de otra distribuidora → recurso no encontrado. Si la tarea ya estaba hecha o cancelada → error de solicitud. |
| **Salida** | La tarea cerrada. |
| **Precondiciones** | El Administrador está autenticado. La TareaMantenimiento existe, es de su Distribuidora y está abierta, es decir ni hecha ni cancelada. |
| **Postcondiciones** | El atributo estado de la instancia de TareaMantenimiento pasó a «hecha», con la fecha de realización, el kilometraje, el costo y el proveedor registrados. |

---

#### Importante · automático Contrato: `avisarVencimientosPendientes()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `avisarVencimientosPendientes()` |
| **Responsabilidades** | Revisar cada día qué tareas de mantenimiento abiertas están por vencer o ya vencieron y avisar por correo a los administradores de cada distribuidora. |
| **Tipo** | Sistema (proceso automático) |
| **Referencias cruzadas** | Casos de uso: CU-142, CU-188. Funciones: IRQ-03, IRQ-17, OBJ-05. |
| **Notas** | Se ejecuta una vez por día, a las 8 de la mañana. La anticipación es la de cada plan. El aviso sale por correo, no por notificación push. Cada Administrador con correo cargado recibe un correo con el detalle de lo que vence o venció. Planificado (I-11, CU-188): el mismo proceso avisa también las tareas cuyo dueño es un empleado, con su nombre, y los documentos bloqueantes que le faltan a cada chofer; los faltantes no se marcan como avisados y se repiten hasta que se carguen. |
| **Excepciones** | Si el envío falla para una distribuidora → sus tareas no se marcan como avisadas y se reintentan en el ciclo siguiente. Si la distribuidora no tiene ningún administrador con correo cargado → las tareas se marcan como avisadas igual. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existen TareaMantenimiento abiertas, con fecha límite, que todavía no fueron avisadas y cuyo estado de vencimiento es «por vencer» o «vencida». |
| **Postcondiciones** | El atributo avisada de cada TareaMantenimiento alcanzada tomó el instante del envío, para no repetir el aviso al día siguiente. |

---

#### Importante Contrato: `declararConsumoPromedio()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `declararConsumoPromedio(tipoGarrafa cadena, cantidadPorMes decimal)` |
| **Responsabilidades** | Registrar el consumo mensual de gas y el tipo de garrafa habitual que el cliente declara al crear su cuenta. |
| **Tipo** | Sistema (planificado, I-5) |
| **Referencias cruzadas** | Casos de uso: CU-143. Funciones: IRQ-01, OBJ-01. |
| **Notas** | Con este dato el sistema estima cuándo se le va a acabar el gas y avisa antes, sin esperar a tener historial de compras. Si el cliente prefiere no declararlo, el registro continúa y el aviso de recompra queda inactivo hasta que haya historial. |
| **Excepciones** | Si el valor declarado está fuera de rango → rechazo con pedido de confirmación; si la solicitud vuelve confirmada, se acepta. |
| **Salida** | La ficha del cliente con el consumo declarado y la fecha estimada de recompra. |
| **Precondiciones** | El Cliente está completando su registro (registrarse). |
| **Postcondiciones** | Los atributos consumo promedio, tipo de garrafa habitual y fecha estimada de recompra de la instancia de Cliente tomaron los valores declarados y calculados. |

---

#### Importante Contrato: `actualizarConsumoPromedio()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarConsumoPromedio(cantidadPorMes decimal)` |
| **Responsabilidades** | Corregir el consumo mensual declarado cuando la situación del cliente cambia, y recalcular la fecha estimada de recompra. |
| **Tipo** | Sistema (planificado, I-5) |
| **Referencias cruzadas** | Casos de uso: CU-144. Funciones: IRQ-01, OBJ-01. |
| **Notas** | Es una corrección posterior al registro. Si el cliente nunca compró, la estimación parte de la fecha de la declaración. |
| **Excepciones** | Si el valor está fuera de rango → rechazo con pedido de confirmación. |
| **Salida** | La ficha del cliente con el consumo y la fecha estimada actualizados. |
| **Precondiciones** | El Cliente está autenticado. |
| **Postcondiciones** | Los atributos consumo promedio y fecha estimada de recompra de la instancia de Cliente tomaron los valores nuevos. |

---

#### Menor Contrato: `configurarDiasDeAviso()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `configurarDiasDeAviso(dias entero)` |
| **Responsabilidades** | Elegir con cuántos días de anticipación quiere el cliente que le avisen que se le está por acabar la garrafa, o desactivar el aviso. |
| **Tipo** | Sistema (planificado, I-5) |
| **Referencias cruzadas** | Casos de uso: CU-145. Funciones: IRQ-01, OBJ-01. |
| **Notas** | Un valor nulo significa que el cliente no eligió y rige el valor de la distribuidora, que se define con configurarParametrosDeProceso. El valor por omisión es de tres días. |
| **Excepciones** | Si el valor está fuera del rango permitido → rechazo. |
| **Salida** | La ficha del cliente con la anticipación elegida. |
| **Precondiciones** | El Cliente está autenticado. |
| **Postcondiciones** | El atributo días de aviso de la instancia de Cliente tomó el valor elegido, o nulo si el aviso se desactivó. |

---

#### Crítico Contrato: `realizarCompraExpress()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `realizarCompraExpress(tipoGarrafa cadena, medioDePago cadena)` |
| **Responsabilidades** | Crear en un solo paso un pedido express de una garrafa a la dirección predeterminada del cliente, sin elegir franja horaria, para entregarlo dentro de la hora por un chofer en moto. |
| **Tipo** | Sistema (planificado, I-7) |
| **Referencias cruzadas** | Casos de uso: CU-147. Funciones: IRQ-01, OBJ-02. |
| **Notas** | Es el segundo flujo de compra, en paralelo a crearPedido. Aplica un recargo express. Si ningún chofer en moto acepta, el despacho pasa el pedido a reparto común (despacharPedidoExpress). |
| **Excepciones** | Si el cliente no tiene dirección predeterminada → se lo lleva a elegir una. Si no hay cobertura express, está fuera de horario o no hay chofer en moto disponible → se ofrece el flujo con franja horaria. Si el cliente no confirma → no se crea ningún pedido. |
| **Salida** | El pedido express creado (número, total con recargo, estado). |
| **Precondiciones** | El Cliente está autenticado y tiene una DireccionEntrega predeterminada dentro de una ZonaCobertura. Hay cobertura express y stock suficiente del Producto elegido. |
| **Postcondiciones** | Se creó una instancia de Pedido en modalidad express y estado «pendiente», con una instancia de ItemPedido por la garrafa elegida, asociada al Cliente y a su DireccionEntrega predeterminada. El atributo stock del Producto se decrementó en una unidad. Si el pago es con pasarela, se creó un Pago en estado «pendiente». El Pedido quedó listo para ofrecerse a un Chofer en moto. |

---

#### Crítico · automático Contrato: `despacharPedidoExpress()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `despacharPedidoExpress(pedidoId identificador)` |
| **Responsabilidades** | Ofrecer el pedido express al chofer en moto más cercano con una ventana de aceptación más corta, y pasarlo a reparto común si nadie lo acepta. |
| **Tipo** | Sistema (proceso automático) (planificado, I-7) |
| **Referencias cruzadas** | Casos de uso: CU-149. Funciones: IRQ-02, OBJ-03. |
| **Notas** | A diferencia del despacho normal, no expande el radio: buscar más lejos rompería la promesa de entrega dentro de la hora. Si ningún chofer en moto tiene la licencia vigente, no ofrece el pedido y pasa directamente al reparto común. En ambos casos se notifica al Cliente. |
| **Excepciones** | Si ningún chofer en moto acepta → la modalidad express se cancela, el recargo se descuenta del total y, si ya se pagó en línea, se reintegra sólo esa parte (reintegrarPagoDelPedido). Si el cliente paga en efectivo, basta con descontar el recargo. |
| **Salida** | Si el pedido quedó asignado o pasó a reparto común. |
| **Precondiciones** | Existe un Pedido en modalidad express, en estado «pendiente» y sin Chofer asociado. |
| **Postcondiciones** | Si un Chofer en moto aceptó, se formó la asociación entre el Pedido y ese Chofer y el Pedido pasó a «aceptado». Si ninguno aceptó, el atributo modalidad del Pedido pasó a reparto común y el atributo total se redujo en el recargo express. |

---

#### Importante Contrato: `programarVigenciaDeZona()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `programarVigenciaDeZona(zonaId identificador, vigenteHasta fechaHora)` |
| **Responsabilidades** | Fijar a una zona de cobertura la fecha y hora en que debe dejar de aplicarse, para los recargos transitorios. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-150. Funciones: IRQ-09, IRQ-10, OBJ-10. |
| **Notas** | La vigencia no cambia cómo se calcula el recargo, sólo hasta cuándo se aplica. El comienzo de la vigencia se programa con la misma operación. Enviar nulo en una de las fechas elimina ese límite. La desactivación efectiva de la zona vencida la hace desactivarZonasVencidas. |
| **Excepciones** | Si la zona no existe o es de otra distribuidora → recurso no encontrado. Si la fecha de fin no es posterior a la de inicio → error de solicitud. |
| **Salida** | La zona con su vigencia. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La ZonaCobertura pertenece a su Distribuidora. |
| **Postcondiciones** | Los atributos vigente desde y vigente hasta de la instancia de ZonaCobertura tomaron los valores indicados. El cálculo de cobertura sólo considera la zona dentro de ese período. |

---

#### Importante · automático Contrato: `desactivarZonasVencidas()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `desactivarZonasVencidas()` |
| **Responsabilidades** | Buscar las zonas de cobertura cuya fecha de fin ya pasó y dejarlas inactivas, para que su recargo deje de aplicarse a los pedidos nuevos. |
| **Tipo** | Sistema (proceso automático) (planificado, I-1) |
| **Referencias cruzadas** | Casos de uso: CU-151. Funciones: IRQ-09, IRQ-10, OBJ-10. |
| **Notas** | Se ejecuta cada cinco minutos. Con más de una instancia del sistema, una sola toma el barrido. Una zona puede apagarse hasta cinco minutos tarde; los pedidos ya cobrados no se modifican. |
| **Excepciones** | Si otra instancia ya está ejecutando el barrido → se saltea. Si no hay zonas vencidas → termina sin hacer nada. Si la ejecución falla → se registra el error y se libera el bloqueo. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existe al menos una ZonaCobertura activa cuya fecha de fin es anterior al momento actual. |
| **Postcondiciones** | El atributo activa de cada ZonaCobertura vencida pasó a falso. Los Pedidos que se creen a partir de ese momento no reciben su recargo; los Pedidos ya cobrados no se modificaron. |

---

#### Crítico · automático Contrato: `registrarOperacion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarOperacion(autor identificador, rol cadena, distribuidoraId identificador, operacion cadena, recurso cadena, origen cadena, resultado cadena, codigo cadena, motivo cadena)` |
| **Responsabilidades** | Dejar constancia de cada operación que modifica datos, exitosa o rechazada, sin que ningún usuario lo solicite. |
| **Tipo** | Sistema (proceso automático) |
| **Referencias cruzadas** | Casos de uso: CU-153. Funciones: IRQ-16, OBJ-04, OBJ-05. |
| **Notas** | Alcanza a toda escritura (POST, PUT, PATCH o DELETE) que pasó la autenticación y la autorización; las operaciones de sólo lectura no generan asiento. Antes de guardar, se reemplazan las credenciales del cuerpo (contraseñas, tokens, códigos) por un marcador. El asiento no puede modificarse ni borrarse. Se guarda sin demorar la respuesta al usuario. |
| **Excepciones** | Si la operación fue rechazada → el asiento se guarda igual, con el resultado fallido y el motivo. Si la base no acepta el asiento → la operación del usuario no se interrumpe: el asiento completo queda en el registro de eventos del sistema. |
| **Salida** | Ninguna: no demora la respuesta al usuario. |
| **Precondiciones** | Se ejecutó una operación de escritura que pasó la autenticación y la autorización. |
| **Postcondiciones** | Se creó una instancia de AsientoAuditoria con la distribuidora, el autor y su rol, la operación, el recurso y su identificador, el origen, el resultado y el código. Las credenciales del cuerpo no quedaron guardadas. |

---

#### Crítico · automático Contrato: `registrarAuditoriaDeDato()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarAuditoriaDeDato(autor identificador, ip cadena, distribuidoraId identificador, entidad cadena, registro cadena, tipoDeAccion entero, detalles lista)` |
| **Responsabilidades** | Dejar constancia, por cada registro de una entidad de negocio que se da de alta, se modifica, se da de baja o se reactiva, de qué campos cambiaron y con qué valor anterior y nuevo, sin que ningún usuario lo solicite. |
| **Tipo** | Sistema (proceso automático) |
| **Referencias cruzadas** | Casos de uso: CU-153. Funciones: IRQ-16, OBJ-04, OBJ-05. |
| **Notas** | Se dispara con cada alta, modificación, baja lógica y reactivación que pasa por la capa de datos, también la que hace un proceso programado o una siembra. El usuario, la dirección de red y la distribuidora salen del contexto de la petición, no del cuerpo; fuera de una petición el usuario queda vacío. En una modificación sólo se registran los campos que realmente cambiaron; en una baja lógica o una reactivación, la fecha de baja. Los campos secretos se guardan como `[oculto]`. Se escribe con la transacción del cambio: si ésta se deshace, la auditoría también. Quedan afuera el carrito, los historiales que ya sólo se agregan, las ofertas de despacho y la posición del chofer. |
| **Excepciones** | Si el guardado no cambió ningún campo → no se registra nada. Si el registro llega sin identificador → no se registra una auditoría vacía y se deja un aviso. Si la transacción se deshace → no queda auditoría. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Un registro de una entidad de negocio se dio de alta, se modificó, se dio de baja o se reactivó. |
| **Postcondiciones** | Se creó una instancia de Auditoria con el tipo de acción, el usuario, la distribuidora, la entidad afectada, el identificador del registro y la dirección de red. Se creó una instancia de DetalleAuditoria, asociada a la Auditoria, por cada campo que cambió, con su valor anterior y el nuevo. Se asoció la Auditoria al Usuario y a la Distribuidora cuando los hay. |

---

#### Importante Contrato: `adjuntarArchivoALaTarea()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `adjuntarArchivoALaTarea(tareaId identificador, archivo archivo)` |
| **Responsabilidades** | Guardar un archivo —foto o PDF de una póliza, una verificación, una licencia o un comprobante— como adjunto de una tarea de mantenimiento de la flota. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-155. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Se aceptan PDF, JPG, PNG y WEBP de hasta diez megabytes. El archivo se guarda en S3 bajo una clave que incluye la distribuidora y la tarea, no el nombre original (caso incluido CU-159). Si falla el registro del adjunto después de guardar el archivo, el archivo se borra para no dejarlo huérfano. |
| **Excepciones** | Si la tarea no existe o es de otra distribuidora → recurso no encontrado. Si no se envía el archivo → error de solicitud. Si el tipo de archivo no es uno de los permitidos → tipo no admitido. Si el archivo supera los diez megabytes → archivo demasiado grande. |
| **Salida** | El adjunto creado, con el nombre original, el tipo y el tamaño. |
| **Precondiciones** | El Administrador está autenticado. La TareaMantenimiento existe y es de su Distribuidora. El archivo es de un tipo permitido y no supera el tamaño máximo. |
| **Postcondiciones** | El contenido del archivo quedó guardado en S3. Se creó una instancia de AdjuntoTarea asociada a la TareaMantenimiento, con su clave de almacenamiento, el nombre original, el tipo, el tamaño y el Usuario que la subió. |

---

#### Secundario Contrato: `eliminarAdjunto()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarAdjunto(tareaId identificador, adjuntoId identificador)` |
| **Responsabilidades** | Borrar un adjunto de una tarea de mantenimiento, por ejemplo si se subió equivocado. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-158. Funciones: IRQ-03, OBJ-05. |
| **Notas** | La baja es lógica, como en todo el sistema: nada se borra físicamente. El archivo queda en S3 como respaldo y la baja queda en la auditoría de datos. |
| **Excepciones** | Si la tarea o el adjunto no existen, o son de otra distribuidora → recurso no encontrado. |
| **Salida** | Ninguna. |
| **Precondiciones** | El Administrador está autenticado. La TareaMantenimiento y el AdjuntoTarea existen y son de su Distribuidora. |
| **Postcondiciones** | La instancia de AdjuntoTarea quedó dada de baja (se le asignó la fecha de baja); su contenido se conserva en S3. |

---

#### Importante Contrato: `ponerVehiculoEnUso()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `ponerVehiculoEnUso(choferId identificador, vehiculoId identificador, nota cadena)` |
| **Responsabilidades** | Registrar qué vehículo usa un chofer: cerrar la asignación abierta anterior del chofer y la del vehículo, y abrir la nueva. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-161. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | Nunca quedan dos asignaciones abiertas para el mismo chofer ni para el mismo vehículo. La operación corre en una única transacción que bloquea el vehículo y los choferes involucrados. Es idempotente: si el chofer ya usa ese vehículo, no cierra ni abre nada. |
| **Excepciones** | Si el chofer o el vehículo no existen o son de otra distribuidora → recurso no encontrado. Si el chofer, o quien usa el vehículo en ese momento, tiene un pedido aceptado o en camino → error de conflicto. Si la documentación del vehículo está vencida → error de solicitud (no se puede asignar). Si hay un conflicto de concurrencia que no se resuelve → error de conflicto. |
| **Salida** | La asignación creada, con el vehículo. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El Chofer y el Vehiculo son de esa Distribuidora. El Vehiculo está habilitado. Ni el Chofer ni el usuario actual del Vehiculo tienen un Pedido «aceptado» o «en camino». |
| **Postcondiciones** | Se creó una instancia de AsignacionVehiculo con la fecha de asignación, el Administrador que la hizo y la nota, asociada al Chofer y al Vehiculo. Las instancias de AsignacionVehiculo abiertas del Chofer y del Vehiculo se cerraron con su fecha de liberación y el Administrador que las cerró. Si el Chofer ya usaba ese Vehiculo, no se modificó nada. |

---

#### Secundario Contrato: `liberarVehiculoEnUso()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `liberarVehiculoEnUso(choferId identificador)` |
| **Responsabilidades** | Cerrar la asignación abierta de un chofer para que deje de tener un vehículo en uso, conservando el período en el historial. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-162. Funciones: IRQ-03, OBJ-02, OBJ-05. |
| **Notas** | La baja del chofer (eliminarChofer) usa otro camino: no falla si el chofer no tenía vehículo y no registra administrador responsable. |
| **Excepciones** | Si el chofer no existe o es de otra distribuidora → recurso no encontrado. Si tiene un pedido aceptado o en camino → error de conflicto. Si no tiene vehículo en uso → recurso no encontrado. |
| **Salida** | Ninguna. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El Chofer es de esa Distribuidora, no tiene un Pedido «aceptado» o «en camino» y tiene una AsignacionVehiculo abierta. |
| **Postcondiciones** | La instancia de AsignacionVehiculo abierta del Chofer se cerró con su fecha de liberación y el Administrador que la liberó. El Chofer no tiene Vehiculo en uso. |

---

#### Importante Contrato: `registrarCargaDeCombustible()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarCargaDeCombustible(vehiculoId identificador, datos registro)` |
| **Responsabilidades** | Registrar una carga de combustible de un vehículo, mantener al día su kilometraje y marcar la carga si su consumo es anómalo. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-195. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Lo ejecuta el Administrador o el Chofer; el chofer lo hace sobre el vehículo que tiene en uso. El kilometraje del vehículo se actualiza al mayor entre el vigente y el de la carga. La carga es anómala si el consumo del tramo se aparta más de un 25 % del promedio de las últimas cinco cargas de tanque lleno. |
| **Excepciones** | Si el vehículo no existe o es de otra distribuidora → recurso no encontrado. Si quien registra es un chofer sin vehículo en uso → error de conflicto. Si el kilometraje es menor que el de la última carga, si el importe no coincide con los litros por el precio o si los litros superan la capacidad del tanque → error de solicitud con el detalle del campo. |
| **Salida** | La carga creada. |
| **Precondiciones** | El solicitante es Administrador o Chofer, autenticado y con una distribuidora asociada. El Vehiculo existe y es de su Distribuidora; si quien registra es un Chofer, es el Vehiculo que tiene en uso. |
| **Postcondiciones** | Se creó una instancia de CargaCombustible con los datos indicados, asociada al Vehiculo y, si se identificó, al Empleado que cargó. El atributo kilometraje de la instancia de Vehiculo pasó a ser el mayor entre el que tenía y el de la carga. Si el consumo del tramo se aparta más de un 25 % del promedio, la carga quedó marcada como anómala. |

---

#### Importante Contrato: `modificarCargaDeCombustible()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarCargaDeCombustible(cargaId identificador, datos registro)` |
| **Responsabilidades** | Corregir los datos de una carga de combustible ya registrada. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-195. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Se revalidan las mismas reglas del alta. La marca de anomalía no se recalcula. El kilometraje del vehículo sólo sube. |
| **Excepciones** | Si la carga no existe o es de otra distribuidora → recurso no encontrado. Si la carga está anulada, o los datos no cumplen las reglas de la carga → error de solicitud con el detalle del campo. |
| **Salida** | La carga modificada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La CargaCombustible existe, es de su Distribuidora y no está anulada. |
| **Postcondiciones** | Los atributos de la instancia de CargaCombustible se modificaron con los datos indicados. El atributo kilometraje de la instancia de Vehiculo es el mayor entre el que tenía y el de la carga modificada. |

---

#### Importante Contrato: `anularCargaDeCombustible()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `anularCargaDeCombustible(cargaId identificador)` |
| **Responsabilidades** | Dar de baja una carga de combustible, sin borrarla, y recalcular el kilometraje del vehículo. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-195. Funciones: IRQ-03, OBJ-05. |
| **Notas** | La baja es lógica: la carga se conserva, queda fuera de los cálculos de consumo y de costo, y no se puede volver a anular. |
| **Excepciones** | Si la carga no existe o es de otra distribuidora → recurso no encontrado. Si la carga ya estaba anulada → error de solicitud. |
| **Salida** | La carga anulada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La CargaCombustible existe, es de su Distribuidora y no está anulada. |
| **Postcondiciones** | La instancia de CargaCombustible quedó anulada, con la fecha de anulación en su atributo anulada el. El atributo kilometraje de la instancia de Vehiculo volvió al de la última carga vigente, si la carga anulada era la última. |

---

#### Importante Contrato: `registrarMultaDeTransito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarMultaDeTransito(vehiculoId identificador, datos registro)` |
| **Responsabilidades** | Registrar una multa de tránsito de un vehículo y proponer como responsable al empleado que lo tenía en uso en el momento de la infracción. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-198. Funciones: IRQ-03, OBJ-05. |
| **Notas** | El acta es única por distribuidora y jurisdicción. La multa nace pendiente. El empleado se deduce de la asignación de vehículo abierta en el instante de la infracción y puede cambiarse. |
| **Excepciones** | Si el vehículo no existe o es de otra distribuidora → recurso no encontrado. Si ya existe una multa con esa jurisdicción y ese número de acta → error de conflicto. Si falta un dato obligatorio o el importe no es positivo → error de solicitud con el detalle del campo. |
| **Salida** | La multa creada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El Vehiculo existe y es de su Distribuidora. |
| **Postcondiciones** | Se creó una instancia de MultaTransito en estado «pendiente», asociada al Vehiculo y, si se identificó, al Empleado responsable. |

---

#### Importante Contrato: `modificarMultaDeTransito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarMultaDeTransito(multaId identificador, datos registro)` |
| **Responsabilidades** | Corregir los datos de una multa o pasarla a apelada. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-198. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Sólo una multa pendiente o apelada admite cambios. El pago, la anulación y la imputación al chofer tienen su propia operación. |
| **Excepciones** | Si la multa no existe o es de otra distribuidora → recurso no encontrado. Si la multa está pagada o anulada, o el estado pedido no sigue al actual → error de solicitud. |
| **Salida** | La multa modificada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La MultaTransito existe, es de su Distribuidora y está pendiente o apelada. |
| **Postcondiciones** | Los atributos de la instancia de MultaTransito se modificaron con los datos indicados; si se indicó, su estado pasó a «apelada». |

---

#### Importante Contrato: `anularMultaDeTransito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `anularMultaDeTransito(multaId identificador, motivo cadena)` |
| **Responsabilidades** | Dar de baja una multa que no corresponde, sin borrarla y con el motivo. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-198. Funciones: IRQ-03, OBJ-05. |
| **Notas** | La multa anulada se conserva para el historial y no cuenta como costo del vehículo. |
| **Excepciones** | Si la multa no existe o es de otra distribuidora → recurso no encontrado. Si la multa está pagada o ya anulada, o falta el motivo → error de solicitud. |
| **Salida** | La multa anulada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La MultaTransito existe, es de su Distribuidora y está pendiente o apelada. |
| **Postcondiciones** | El atributo estado de la instancia de MultaTransito pasó a «anulada», con el motivo registrado. |

---

#### Importante Contrato: `avisarMultasPorVencer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `avisarMultasPorVencer()` |
| **Responsabilidades** | Avisar a los administradores de cada distribuidora de las multas pendientes que vencen en siete días o menos, o que ya vencieron, y marcarlas para no repetir el aviso. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-198. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Corre una vez por día, a las 08:00 hora argentina. El aviso sale por correo. Si el correo falla, la multa no se marca y el aviso se reintenta en el ciclo siguiente. |
| **Excepciones** | Si no hay multas por vencer sin avisar, el ciclo termina sin enviar nada. Un fallo del correo de una distribuidora no detiene el aviso de las demás. |
| **Salida** | Ninguna: el sistema no responde a un actor humano. |
| **Precondiciones** | El proceso programado está activo. Hay multas pendientes con vencimiento en siete días o menos, o vencidas, sin aviso. |
| **Postcondiciones** | Cada instancia de MultaTransito avisada quedó con la fecha del aviso en su atributo avisada el. Los administradores de la Distribuidora recibieron el correo. |

---

#### Secundario Contrato: `registrarPagoDeMulta()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarPagoDeMulta(multaId identificador, fechaDePago fechaHora, importePagado moneda)` |
| **Responsabilidades** | Registrar que una multa se pagó, con la fecha y el importe pagado. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-199. Funciones: IRQ-03, OBJ-05. |
| **Notas** | El importe pagado puede ser el del pago voluntario, menor que el de la multa. El movimiento de caja se vincula cuando exista el módulo de caja. |
| **Excepciones** | Si la multa no existe o es de otra distribuidora → recurso no encontrado. Si la multa ya está pagada o anulada → error de solicitud. Si la fecha de pago es futura o el importe no es positivo → error de solicitud con el detalle del campo. |
| **Salida** | La multa pagada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La MultaTransito existe, es de su Distribuidora y está pendiente o apelada. |
| **Postcondiciones** | El atributo estado de la instancia de MultaTransito pasó a «pagada», con la fecha de pago y el importe pagado indicados. |

---

#### Secundario Contrato: `imputarMultaAlChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `imputarMultaAlChofer(multaId identificador, empleadoId identificador)` |
| **Responsabilidades** | Atribuir una multa al empleado que conducía, para que se le descuente en su liquidación. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-200. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Mientras no exista el módulo de caja, la imputación es sólo una marca. Una multa pagada también se imputa. Una multa imputada no cuenta como costo del vehículo. |
| **Excepciones** | Si la multa o el empleado no existen o son de otra distribuidora → recurso no encontrado. Si la multa está anulada → error de solicitud. |
| **Salida** | La multa imputada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La MultaTransito existe, es de su Distribuidora y no está anulada. El Empleado existe y es de su Distribuidora. |
| **Postcondiciones** | El atributo imputada al chofer de la instancia de MultaTransito quedó verdadero, y la multa quedó asociada al Empleado indicado. |

---

#### Importante Contrato: `registrarSiniestro()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarSiniestro(vehiculoId identificador, datos registro)` |
| **Responsabilidades** | Registrar un siniestro de un vehículo y, si lo dejó inutilizable, ponerlo fuera de servicio. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-201. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Lo ejecuta el Administrador o el Chofer; el chofer lo hace sobre el vehículo que tiene en uso. Un derrame de gas obliga a avisar de inmediato a los administradores. El vehículo fuera de servicio no recibe ofertas de pedidos. |
| **Excepciones** | Si el vehículo no existe o es de otra distribuidora → recurso no encontrado. Si quien registra es un chofer sin vehículo en uso → error de conflicto. Si falta la fecha o la descripción, o el punto no es una coordenada válida → error de solicitud con el detalle del campo. |
| **Salida** | El siniestro creado. |
| **Precondiciones** | El solicitante es Administrador o Chofer, autenticado y con una distribuidora asociada. El Vehiculo existe y es de su Distribuidora; si quien registra es un Chofer, es el Vehiculo que tiene en uso. |
| **Postcondiciones** | Se creó una instancia de Siniestro en estado «denunciado», asociada al Vehiculo y, si se identificó, al Empleado que conducía. Si el vehículo quedó inutilizable, el atributo estado en la flota de la instancia de Vehiculo pasó a «fuera de servicio» y las instancias de AsignacionVehiculo abiertas del Vehiculo se cerraron con su fecha de liberación. |

---

#### Importante Contrato: `modificarSiniestro()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarSiniestro(siniestroId identificador, datos registro)` |
| **Responsabilidades** | Corregir los datos de un siniestro y hacerlo avanzar de denunciado a en revisión y a en reparación. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-201. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Un siniestro cerrado no admite cambios. El cierre tiene su propia operación. |
| **Excepciones** | Si el siniestro no existe o es de otra distribuidora → recurso no encontrado. Si el siniestro está cerrado, o el estado pedido no sigue al actual → error de solicitud. |
| **Salida** | El siniestro modificado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El Siniestro existe, es de su Distribuidora y no está cerrado. |
| **Postcondiciones** | Los atributos de la instancia de Siniestro se modificaron con los datos indicados y, si se indicó, su estado avanzó a «en revisión» o a «en reparación». Si el vehículo quedó inutilizable, el atributo estado en la flota de la instancia de Vehiculo pasó a «fuera de servicio» y las instancias de AsignacionVehiculo abiertas del Vehiculo se cerraron con su fecha de liberación. |

---

#### Secundario Contrato: `cerrarSiniestro()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cerrarSiniestro(siniestroId identificador, costoDeReparacion moneda, reintegroDelSeguro moneda, franquicia moneda)` |
| **Responsabilidades** | Cerrar un siniestro resuelto, con el costo de la reparación, el reintegro del seguro y la franquicia. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-202. Funciones: IRQ-03, OBJ-05. |
| **Notas** | El costo neto es el de la reparación menos el reintegro del seguro. Cerrar el siniestro no devuelve el vehículo a la flota activa. |
| **Excepciones** | Si el siniestro no existe o es de otra distribuidora → recurso no encontrado. Si el siniestro ya está cerrado o algún importe es negativo → error de solicitud. |
| **Salida** | El siniestro cerrado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El Siniestro existe, es de su Distribuidora y no está cerrado. |
| **Postcondiciones** | El atributo estado de la instancia de Siniestro pasó a «cerrado», con el costo de reparación, el reintegro del seguro, la franquicia y la fecha de cierre registrados. |

---

#### Secundario Contrato: `registrarNeumatico()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarNeumatico(datos registro)` |
| **Responsabilidades** | Dar de alta un neumático de la distribuidora, en depósito. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-205. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Funcionalidad opcional del módulo. El número de serie es único por distribuidora. |
| **Excepciones** | Si ya existe un neumático con ese número de serie → error de conflicto. Si falta un dato obligatorio o el costo es negativo → error de solicitud con el detalle del campo. |
| **Salida** | El neumático creado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. |
| **Postcondiciones** | Se creó una instancia de Neumatico en estado «en depósito», con los datos indicados, asociada a la Distribuidora. |

---

#### Secundario Contrato: `registrarMovimientoDeNeumatico()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarMovimientoDeNeumatico(neumaticoId identificador, datos registro)` |
| **Responsabilidades** | Registrar un movimiento de un neumático —montaje, desmontaje, rotación, recapado o baja— y dejarlo en el estado que corresponde. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-206. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Funcionalidad opcional del módulo. Los movimientos no se modifican. Sólo se monta un neumático en depósito, y sólo se desmonta o rota uno montado. |
| **Excepciones** | Si el neumático o el vehículo no existen o son de otra distribuidora → recurso no encontrado. Si el movimiento no corresponde al estado del neumático → error de solicitud. Si falta el kilometraje, o en un montaje el vehículo o la posición → error de solicitud con el detalle del campo. |
| **Salida** | El movimiento creado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El Neumatico existe, es de su Distribuidora y su estado admite el movimiento. Si es un montaje, el Vehiculo existe y es de su Distribuidora. |
| **Postcondiciones** | Se creó una instancia de MovimientoNeumatico con el tipo, el kilometraje y la fecha indicados. El atributo estado de la instancia de Neumatico pasó al que corresponde al movimiento: «en depósito», «montado» o «dado de baja». |

---

#### Importante Contrato: `reactivarVehiculo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `reactivarVehiculo(vehiculoId identificador)` |
| **Responsabilidades** | Devolver a la flota activa un vehículo que estaba fuera de servicio, si su documentación bloqueante está en regla. |
| **Tipo** | Sistema (planificado, I-12) |
| **Referencias cruzadas** | Casos de uso: CU-247. Funciones: IRQ-03, OBJ-05. |
| **Notas** | Usa el mismo control de documentación que la asignación de un vehículo a un chofer. No asigna el vehículo a ningún chofer. |
| **Excepciones** | Si el vehículo no existe o es de otra distribuidora → recurso no encontrado. Si el vehículo no está fuera de servicio, o tiene una documentación bloqueante vencida → error de solicitud con el documento vencido. |
| **Salida** | El vehículo activo. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El Vehiculo existe, es de su Distribuidora y está fuera de servicio. Ninguna TareaMantenimiento bloqueante del Vehiculo está vencida. |
| **Postcondiciones** | El atributo estado en la flota de la instancia de Vehiculo pasó a «activo». |

---

#### Importante Contrato: `tomarReclamo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `tomarReclamo(reclamoId identificador)` |
| **Responsabilidades** | Pasar un reclamo pendiente a «en proceso», para dejar constancia de que un administrador ya lo está revisando. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-166. Funciones: IRQ-06, OBJ-04, OBJ-05. |
| **Notas** | La transición se valida contra los estados del reclamo y el reclamo se lee bajo bloqueo: dos operaciones simultáneas sobre el mismo reclamo se serializan. |
| **Excepciones** | Si el reclamo no existe o es de otra distribuidora → recurso no encontrado. Si el reclamo no está pendiente → error de solicitud (sólo se puede tomar un reclamo pendiente). |
| **Salida** | El reclamo con estado «en proceso». |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Reclamo existe, es de su Distribuidora y su estado es «pendiente». |
| **Postcondiciones** | El atributo estado de la instancia de Reclamo pasó de «pendiente» a «en proceso». La nota de resolución no se modificó. |

---

#### Importante Contrato: `reabrirReclamo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `reabrirReclamo(reclamoId identificador, motivo cadena)` |
| **Responsabilidades** | Devolver a «en proceso» un reclamo resuelto o rechazado, registrando el motivo de la reapertura. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-167. Funciones: IRQ-06, OBJ-04, OBJ-05. |
| **Notas** | El reclamo se lee bajo bloqueo dentro de una transacción. El motivo reemplaza la nota de resolución anterior; la nota anterior queda sólo en el registro de auditoría (CU-153). Nunca vuelve a «pendiente»: ese es el estado de alta. |
| **Excepciones** | Si el motivo falta, está vacío o es sólo de espacios → error de solicitud. Si el reclamo no existe o es de otra distribuidora → recurso no encontrado. Si el reclamo no está resuelto ni rechazado → error de solicitud. |
| **Salida** | El reclamo con estado «en proceso» y el motivo como nota. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Reclamo existe, es de su Distribuidora y su estado es «resuelto» o «rechazado». |
| **Postcondiciones** | El atributo estado de la instancia de Reclamo pasó a «en proceso» y su atributo nota de resolución tomó el motivo de la reapertura. |

---

#### Importante Contrato: `reintegrarPagoDelPedido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `reintegrarPagoDelPedido(pedidoId identificador, importe moneda)` |
| **Responsabilidades** | Devolver por la pasarela el importe de los pagos aprobados de un pedido cancelado, o el recargo de un pedido express pasado a reparto común, y dejar constancia en los pagos. |
| **Tipo** | Sistema (planificado, I-7) |
| **Referencias cruzadas** | Casos de uso: CU-168. Funciones: IRQ-08, OBJ-07. |
| **Notas** | Corre fuera de la transacción de la cancelación. La clave de idempotencia es el identificador del pago: repetir la solicitud no devuelve el dinero dos veces. Si no se indica el importe, se devuelve el del pago completo. No cambia el estado de pago del pedido: sigue indicando que se cobró. El administrador puede reintentar un reintegro fallido desde el detalle del pedido. Se notifica al panel y al Cliente. |
| **Excepciones** | Si el pedido no existe o es de otra distribuidora → recurso no encontrado. Si el pedido no está cancelado ni es un express degradado → error de conflicto. Si no hay un pago aprobado por una pasarela → el proceso termina sin devolución. Si la pasarela rechaza o no responde → el pago queda aprobado y se avisa al panel de la devolución fallida. |
| **Salida** | Si el pago fue reintegrado o la devolución falló. |
| **Precondiciones** | El Pedido está cancelado, o es un pedido express pasado a reparto común. Tiene al menos un Pago aprobado por una pasarela. |
| **Postcondiciones** | El atributo estado de cada Pago aprobado alcanzado pasó a «reintegrado», con su fecha de modificación actualizada. Si la pasarela rechazó la devolución, el Pago conserva el estado «aprobado». |

---

#### Importante · automático Contrato: `registrarCambioDeEstado()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarCambioDeEstado(pedidoId identificador, estadoAnterior cadena, estadoNuevo cadena, autor identificador, motivo cadena)` |
| **Responsabilidades** | Agregar al historial del pedido la fila de una transición de estado, dentro de la transacción que la produce. |
| **Tipo** | Sistema (proceso automático) (planificado, I-4) |
| **Referencias cruzadas** | Casos de uso: CU-169. Funciones: IRQ-02, OBJ-04. |
| **Notas** | Usa la transacción del llamador: no abre una propia. No valida la transición, que ya validó el ciclo de vida del pedido. Sólo agrega: no existe operación que modifique una fila del historial. |
| **Excepciones** | Si la inserción falla → el error se propaga y la transacción del llamador se revierte. |
| **Salida** | El cambio de estado registrado. |
| **Precondiciones** | El Pedido existe y su estado está cambiando dentro de una transacción abierta. |
| **Postcondiciones** | Se creó una instancia de CambioEstadoPedido asociada al Pedido, con el estado anterior, el estado nuevo, el autor (si lo hubo), el motivo y la fecha. |

---

#### Crítico Contrato: `configurarParametrosDeDespacho()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `configurarParametrosDeDespacho(radiosKm lista, ventanaDeAceptacion entero)` |
| **Responsabilidades** | Guardar los pasos de radio y la ventana de aceptación del despacho de una distribuidora, reemplazando la configuración anterior. |
| **Tipo** | Sistema (planificado, I-1) |
| **Referencias cruzadas** | Casos de uso: CU-171. Funciones: IRQ-09, OBJ-02, OBJ-05. |
| **Notas** | Hay una sola configuración por distribuidora y proceso. Los parámetros no enviados toman su valor por omisión al leerse. Las demás instancias del sistema renuevan su copia al vencer. |
| **Excepciones** | Si falta la distribuidora → error de solicitud. Si algún valor está fuera de rango, o los pasos no son estrictamente crecientes → error de solicitud con el detalle del campo. |
| **Salida** | La configuración guardada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. Los valores cumplen los rangos. |
| **Postcondiciones** | La instancia de ConfiguracionModulo de la Distribuidora para el despacho tiene los pasos de radio y la ventana indicados, con el Administrador que los modificó y la fecha. Las ofertas que se creen después usan esos valores. |

---

#### Importante Contrato: `configurarParametrosDeProceso()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `configurarParametrosDeProceso(proceso cadena, parametros registro)` |
| **Responsabilidades** | Guardar los parámetros de un proceso automático de una distribuidora, validados contra el esquema de ese proceso. |
| **Tipo** | Sistema (planificado, I-1) |
| **Referencias cruzadas** | Casos de uso: CU-172. Funciones: IRQ-09, OBJ-02, OBJ-05. |
| **Notas** | Hay una sola configuración por distribuidora y proceso. El esquema de validación es propio de cada proceso. Reemplaza la configuración anterior; los parámetros no enviados toman su valor por omisión. |
| **Excepciones** | Si falta la distribuidora → error de solicitud. Si el proceso no es configurable → recurso no encontrado. Si algún parámetro es inválido para ese proceso → error de solicitud con el detalle del campo. |
| **Salida** | La configuración guardada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El proceso es uno de los cinco configurables. |
| **Postcondiciones** | La instancia de ConfiguracionModulo de la Distribuidora para ese proceso tiene los parámetros indicados, con el Administrador que los modificó y la fecha. |

---

#### Importante Contrato: `configurarFrecuenciaDeTareas()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `configurarFrecuenciaDeTareas(intervalos registro)` |
| **Responsabilidades** | Guardar el intervalo de cada tarea programada de una distribuidora y reprogramarlas, de modo que el valor nuevo rija desde el ciclo siguiente. |
| **Tipo** | Sistema (planificado, I-1) |
| **Referencias cruzadas** | Casos de uso: CU-173. Funciones: IRQ-15, OBJ-05, OBJ-15. |
| **Notas** | Cada intervalo es múltiplo del ciclo de base de su tarea. La marca de última ejecución no se guarda en la base relacional. |
| **Excepciones** | Si falta la distribuidora → error de solicitud. Si un intervalo no es múltiplo del ciclo de base, supera las 24 horas o la hora está fuera de 0 a 23 → error de solicitud con el detalle del campo. |
| **Salida** | La configuración guardada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. Los intervalos cumplen las reglas. |
| **Postcondiciones** | La instancia de ConfiguracionModulo de la Distribuidora para las tareas programadas tiene los intervalos indicados, con el Administrador que los modificó y la fecha. Las marcas de última ejecución de esa Distribuidora se borraron. |

---

#### Importante Contrato: `adjuntarFotoAlReclamo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `adjuntarFotoAlReclamo(reclamoId identificador, imagen archivo)` |
| **Responsabilidades** | Guardar la fotografía de un reclamo y dejar su referencia en el reclamo, reemplazando la anterior. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-174. Funciones: IRQ-06, OBJ-04. |
| **Notas** | Un cliente sólo modifica sus propios reclamos. La clave de almacenamiento no incluye el nombre original (caso incluido CU-159). La clave se reserva antes de subir y se confirma con la referencia; la imagen anterior se anota para borrar en la misma transacción y se borra de S3 en segundo plano; si falla guardar la referencia, la imagen recién subida se borra. |
| **Excepciones** | Si el reclamo no existe, es de otra distribuidora o no es del cliente → recurso no encontrado. Si falta el archivo → error de solicitud. Si el tipo no es JPG, PNG ni WEBP, o el contenido no coincide con el tipo declarado → tipo no admitido. Si supera 10 MB → archivo demasiado grande. Si el reclamo está resuelto o rechazado → conflicto. |
| **Salida** | El reclamo con la referencia a la fotografía. |
| **Precondiciones** | El solicitante está autenticado y puede modificar el Reclamo. La imagen es de un tipo permitido y no supera el tamaño máximo. El reclamo no está resuelto ni rechazado. |
| **Postcondiciones** | El atributo fotografía de la instancia de Reclamo tomó la referencia a la imagen subida. La fotografía anterior, si la había, quedó anotada para borrarse de S3. |

---


#### Importante Contrato: `crearPuestoDeTrabajo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearPuestoDeTrabajo(nombre cadena, categoria cadena)` |
| **Responsabilidades** | Crear un puesto de trabajo en la distribuidora, con su nombre y su categoría. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-255. Funciones: IRQ-17, OBJ-05. |
| **Notas** | El nombre es único entre los puestos vigentes de la distribuidora, sin distinguir mayúsculas. La categoría —chofer, ayudante, depósito, administración, ventas, dirección u otra— gobierna las reglas que se aplican al personal que lo ocupe; el nombre es libre. El puesto nace activo, salvo que el pedido indique lo contrario. |
| **Excepciones** | Si ya existe un puesto vigente con ese nombre → error de conflicto. Si la categoría no es una de las admitidas, o el nombre falta o no tiene entre 2 y 80 caracteres → error de solicitud. |
| **Salida** | El puesto creado. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La Distribuidora existe y está activa. |
| **Postcondiciones** | Se creó una instancia de PuestoDeTrabajo con su atributo nombre, su categoría y su marca de activo (verdadera, salvo que se indique lo contrario). Se formó la asociación Distribuidora define PuestoDeTrabajo. |

---

#### Importante Contrato: `modificarPuestoDeTrabajo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarPuestoDeTrabajo(puestoId identificador, datos registro)` |
| **Responsabilidades** | Cambiar el nombre, la categoría o la marca de activo de un puesto. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-256. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Se repite el control de unicidad del nombre. Los empleados que ocupan el puesto no se modifican. Si cambia la categoría, los ocupantes con cuenta tienen que conservar un rol de acceso que corresponda a la categoría nueva; y el último puesto activo de categoría chofer o administración no se puede desactivar ni recategorizar, para que el alta de personal con cuenta siempre tenga dónde ubicarse. |
| **Excepciones** | Si el puesto no existe o es de otra distribuidora → recurso no encontrado. Si el nombre nuevo ya lo tiene otro puesto vigente, si la categoría nueva no corresponde al rol de la cuenta de algún ocupante o si es el último puesto activo de su categoría → error de conflicto. Si un dato no es válido → error de solicitud. |
| **Salida** | El puesto modificado. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El PuestoDeTrabajo existe y es de su Distribuidora. |
| **Postcondiciones** | El atributo nombre, categoría o activo de la instancia de PuestoDeTrabajo tomó los valores recibidos. |

---

#### Importante Contrato: `eliminarPuestoDeTrabajo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarPuestoDeTrabajo(puestoId identificador)` |
| **Responsabilidades** | Dar de baja un puesto que ya no se usa. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-257. Funciones: IRQ-17, OBJ-05. |
| **Notas** | La baja es lógica: el puesto se conserva con su fecha de baja y deja de ofrecerse. No procede mientras algún legajo, activo o egresado, lo ocupe: un puesto que ya se usó se desactiva en vez de eliminarse. |
| **Excepciones** | Si el puesto no existe o es de otra distribuidora → recurso no encontrado. Si el puesto tiene empleados activos → error de conflicto, con la cantidad. Si figura en legajos de empleados egresados o es el último puesto activo de su categoría chofer o administración → error de conflicto. |
| **Salida** | Mensaje de confirmación. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El PuestoDeTrabajo existe, es de su Distribuidora y ningún Empleado, activo o egresado, lo ocupa. |
| **Postcondiciones** | La instancia de PuestoDeTrabajo quedó dada de baja (baja lógica): dejó de ofrecerse y de listarse. |

---

#### Crítico Contrato: `registrarEmpleado()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarEmpleado(datos registro)` |
| **Responsabilidades** | Registrar el legajo de una persona que trabaja en la distribuidora, con su puesto y sus datos personales. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-177. Funciones: IRQ-17, OBJ-05. |
| **Notas** | El número de legajo es el que trae el pedido o, si falta, el siguiente de la distribuidora, que se asigna con bloqueo para no repetirlo. El CUIL se valida con su dígito verificador. El legajo no implica una cuenta de acceso: se otorga después (otorgarCuentaDeAcceso). El alta de un chofer por el registro de usuarios crea el legajo por este mismo camino, en la misma transacción. |
| **Excepciones** | Si falta un dato, el formato es inválido o el CUIL no es válido → error de solicitud. Si el puesto no existe o es de otra distribuidora → recurso no encontrado. Si el puesto está inactivo, o el documento, el CUIL o el número de legajo ya pertenecen a otro empleado vigente de la distribuidora → error de conflicto. |
| **Salida** | El legajo creado, activo y sin cuenta de acceso. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El PuestoDeTrabajo indicado existe, está activo y es de su Distribuidora. |
| **Postcondiciones** | Se creó una instancia de Empleado con su legajo, su estado «activo» y los datos personales recibidos, sin cuenta de acceso. Se formó la asociación Empleado ocupa PuestoDeTrabajo con el puesto indicado y la asociación Distribuidora emplea Empleado. |

---

#### Importante Contrato: `modificarEmpleado()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarEmpleado(empleadoId identificador, datos registro)` |
| **Responsabilidades** | Corregir los datos de un legajo, incluido su puesto. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-178. Funciones: IRQ-17, OBJ-05. |
| **Notas** | No cambia el estado del empleado ni sus fechas de egreso: eso lo hacen el egreso y el reingreso. Si cambia el CUIL se valida su dígito verificador; si cambia el documento o el CUIL se repite el control de unicidad. Si cambia el puesto, tiene que estar activo y, si el empleado tiene cuenta, corresponder al rol de ese usuario. La fecha de ingreso no puede ser posterior a la de egreso. |
| **Excepciones** | Si el empleado o el puesto no existen o son de otra distribuidora → recurso no encontrado. Si el documento, el CUIL o el número de legajo ya pertenecen a otro empleado vigente, o el puesto está inactivo o no corresponde a la cuenta del empleado → error de conflicto. Si el formato o el CUIL no son válidos, se envía en blanco un dato obligatorio o la fecha de ingreso es posterior a la de egreso → error de solicitud. |
| **Salida** | El legajo modificado. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado existe y es de su Distribuidora. |
| **Postcondiciones** | Los atributos domicilio, teléfono, contacto de emergencia, modalidad de contratación y los demás datos recibidos de la instancia de Empleado tomaron los valores nuevos. Si cambió el puesto, la asociación Empleado ocupa PuestoDeTrabajo apunta al puesto nuevo. |

---

#### Importante Contrato: `eliminarEmpleado()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `eliminarEmpleado(empleadoId identificador)` |
| **Responsabilidades** | Dar de baja un legajo cargado por error. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-178. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Sólo procede mientras el legajo no tenga cuenta de acceso; cuando existan las jornadas y la documentación del personal (I-11), también mientras no tenga ninguna. La salida normal de una persona es el egreso (registrarEgresoDelEmpleado), que conserva el legajo. |
| **Excepciones** | Si el empleado no existe o es de otra distribuidora → recurso no encontrado. Si el legajo tiene cuenta de acceso (o, cuando existan, jornadas o tareas de documentación) → error de conflicto. |
| **Salida** | Mensaje de confirmación. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado existe, es de su Distribuidora y no tiene cuenta de acceso ni, cuando existan, jornadas o tareas de documentación. |
| **Postcondiciones** | La instancia de Empleado quedó dada de baja como alta errónea y dejó de aparecer en los listados. |

---

#### Crítico Contrato: `registrarEgresoDelEmpleado()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarEgresoDelEmpleado(empleadoId identificador, fechaDeEgreso fecha, motivo cadena)` |
| **Responsabilidades** | Dar de baja a un empleado de la distribuidora con su fecha y su motivo, y cortar su acceso. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-181. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Ocurre en una única transacción, que toma los bloqueos en el mismo orden que la baja de un usuario. Si el empleado tiene cuenta de acceso, se la bloquea; si además es chofer, se lo deshabilita y se libera el vehículo que tenía en uso, por el mismo camino que la baja de un chofer, y con el egreso confirmado sale del radar de despacho. Un chofer con pedidos en curso no puede egresar. Cuando existan la carga de camión y la rendición de cuentas del chofer, el egreso exige no tener ninguna abierta ni pendiente. El motivo es uno de renuncia, despido, fin de contrato, jubilación u otro. |
| **Excepciones** | Si el empleado no existe o es de otra distribuidora → recurso no encontrado. Si ya está egresado → error de conflicto. Si la fecha de egreso es anterior a la de ingreso o el motivo no es válido → error de solicitud. Si el chofer tiene pedidos en curso → error de conflicto con la cantidad. Planificado (I-13): si tiene una carga de camión abierta o una rendición pendiente → error de conflicto con el detalle. |
| **Salida** | El legajo egresado. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado existe, es de su Distribuidora y su estado es «activo». |
| **Postcondiciones** | El atributo estado de la instancia de Empleado pasó a «egresado» y sus atributos fecha de egreso y motivo de egreso tomaron los valores recibidos. Si el empleado tiene cuenta de acceso, el atributo bloqueado de la instancia de Usuario asociada pasó a verdadero. Si esa cuenta tiene perfil de reparto, el atributo habilitado de la instancia de Chofer pasó a falso y su asignación de vehículo vigente quedó liberada. |

---

#### Crítico Contrato: `reingresarEmpleado()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `reingresarEmpleado(empleadoId identificador, fechaDeIngreso fecha)` |
| **Responsabilidades** | Reincorporar a un empleado egresado, con una fecha de ingreso nueva. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-181. Funciones: IRQ-17, OBJ-05. |
| **Notas** | No desbloquea la cuenta de acceso ni vuelve a habilitar al chofer: la reactivación de la cuenta es una decisión aparte del administrador. Si no se indica fecha de ingreso, es hoy. |
| **Excepciones** | Si el empleado no existe o es de otra distribuidora → recurso no encontrado. Si no está egresado → error de conflicto. Si la fecha de ingreso es anterior a la de egreso → error de solicitud. |
| **Salida** | El legajo activo. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado existe, es de su Distribuidora y su estado es «egresado». |
| **Postcondiciones** | El atributo estado de la instancia de Empleado volvió a «activo», sus atributos fecha de egreso y motivo de egreso quedaron vacíos y su atributo fecha de ingreso tomó la fecha recibida. |

---

#### Importante Contrato: `otorgarCuentaDeAcceso()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `otorgarCuentaDeAcceso(empleadoId identificador, datosDeAcceso registro)` |
| **Responsabilidades** | Darle acceso al sistema a un empleado que tiene legajo y no tiene cuenta. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-182. Funciones: IRQ-17, OBJ-05. |
| **Notas** | El rol lo decide la categoría de su puesto, y hoy sólo `driver` admite cuenta (rol chofer): los administrativos reciben su cuenta de administrador con el alta del usuario, y las demás categorías no admiten cuenta porque el sistema no define roles para ellas. Los datos de acceso son el correo, la contraseña inicial y, si el legajo no tiene teléfono, uno en formato E.164. La cuenta se crea por el mismo camino que el alta de cualquier usuario (crearUsuarioBase, CU-082). Si el rol es chofer, se crea además su perfil de reparto. |
| **Excepciones** | Si el empleado no existe o es de otra distribuidora → recurso no encontrado. Si ya tiene cuenta o está egresado → error de conflicto. Si la categoría del puesto no admite cuenta, falta un teléfono en formato E.164 o los datos de acceso no son válidos → error de solicitud. Si el correo o el teléfono ya están en uso → error de conflicto. |
| **Salida** | El legajo con su cuenta vinculada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado existe, es de su Distribuidora, está activo y no tiene cuenta de acceso. La categoría de su puesto admite una cuenta. |
| **Postcondiciones** | Se creó una instancia de Usuario, con el rol que corresponde a la categoría del puesto, en la distribuidora del empleado. Se formó la asociación Empleado accede con Usuario. |

---

#### Crítico Contrato: `crearTareaDelEmpleado()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearTareaDelEmpleado(empleadoId identificador, planId identificador, vencimiento fecha, detalle registro)` |
| **Responsabilidades** | Registrar la documentación con vencimiento de un empleado —curso de mercancías peligrosas, examen psicofísico, alta en la ART— como una tarea de un plan. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-183, CU-184, CU-185. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Es una única operación parametrizada por plan, la misma de crearTareaDeFlota con el empleado como dueño: CU-183 (curso, con número de certificado y emisor), CU-184 (examen psicofísico) y CU-185 (alta en la ART, con aseguradora y póliza) la usan con distinto plan. El plan dice a qué categorías de puesto aplica. Un chofer con un vencimiento bloqueante vencido queda inhabilitado para el despacho; el alta en la ART no bloquea. |
| **Excepciones** | Si el plan o el empleado no existen o son de otra distribuidora → recurso no encontrado. Si el plan no aplica a la categoría del puesto del empleado, o el detalle no tiene la forma que exige el tipo de documento → error de solicitud. Si el empleado está egresado → error de conflicto. |
| **Salida** | La tarea creada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El PlanMantenimiento existe, está activo, es de su Distribuidora y es de sujeto empleado. El Empleado existe, es de su Distribuidora y está activo. |
| **Postcondiciones** | Se creó una instancia de TareaMantenimiento en estado «programada», con su vencimiento y su detalle. Se formó la asociación PlanMantenimiento genera TareaMantenimiento y la asociación TareaMantenimiento habilita Empleado. |

---

#### Secundario Contrato: `adjuntarArchivoAlLegajo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `adjuntarArchivoAlLegajo(empleadoId identificador, archivo archivo, etiqueta cadena)` |
| **Responsabilidades** | Guardar un archivo en el legajo de un empleado, con una etiqueta que dice qué es. |
| **Tipo** | Sistema |
| **Referencias cruzadas** | Casos de uso: CU-186. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Sólo se admiten PDF, JPG, PNG y WEBP de hasta 10 MB, y el contenido tiene que coincidir con el tipo declarado. El contenido se guarda en S3 con una clave que incluye la distribuidora, el tipo de dueño y el empleado; en la base queda la clave y no una dirección. El dueño se valida por un puerto que registra el módulo de personal. |
| **Excepciones** | Si el empleado no existe o es de otra distribuidora → recurso no encontrado. Si falta el archivo o está vacío → error de solicitud. Si el tipo no está permitido o el contenido no coincide con el tipo declarado → tipo no admitido. Si supera los 10 MB → archivo demasiado grande. |
| **Salida** | El adjunto registrado. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado existe y es de su Distribuidora. |
| **Postcondiciones** | Se creó una instancia de Adjunto con su nombre original, su tipo de archivo, su etiqueta y su fecha de carga. Se formó la asociación Empleado conserva Adjunto. |

---

#### Importante Contrato: `registrarAsistencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarAsistencia(empleadoId identificador, ingreso fechaHora, egreso fechaHora)` |
| **Responsabilidades** | Cargar a mano la jornada de un empleado, con su ingreso y, si ya terminó, su egreso. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-189. Funciones: IRQ-17, OBJ-05. |
| **Notas** | El día de la jornada es el día argentino del ingreso. Hay una sola jornada abierta por empleado: una restricción de la base lo impide. La jornada nace con origen «panel». |
| **Excepciones** | Si el empleado no existe o es de otra distribuidora → recurso no encontrado. Si está egresado o ya tiene una jornada abierta → error de conflicto. Si el egreso no es posterior al ingreso → error de solicitud. |
| **Salida** | La jornada registrada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado existe, es de su Distribuidora, está activo y no tiene una jornada abierta (salvo que la jornada que se carga ya esté cerrada). |
| **Postcondiciones** | Se creó una instancia de JornadaDeTrabajo con su día, su ingreso, su egreso si se informó y el origen «panel». Se formó la asociación Empleado registra JornadaDeTrabajo. |

---

#### Importante Contrato: `corregirAsistencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `corregirAsistencia(asistenciaId identificador, datos registro, nota cadena)` |
| **Responsabilidades** | Corregir el ingreso o el egreso de una jornada ya cargada, dejando una nota que explique el cambio. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-189. Funciones: IRQ-17, OBJ-05. |
| **Notas** | La nota es obligatoria y reemplaza la observación anterior. El estado anterior de la jornada queda sólo en el registro de auditoría. |
| **Excepciones** | Si la jornada no existe o es de otra distribuidora → recurso no encontrado. Si falta la nota o el egreso no es posterior al ingreso → error de solicitud. |
| **Salida** | La jornada corregida. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La JornadaDeTrabajo existe y es de su Distribuidora. |
| **Postcondiciones** | Los atributos ingreso y egreso de la instancia de JornadaDeTrabajo tomaron los valores recibidos y su atributo observación tomó la nota. |

---

#### Secundario Contrato: `registrarInicioDeJornada()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarInicioDeJornada()` |
| **Responsabilidades** | Marcar desde la App Chofer el comienzo de la jornada del chofer autenticado. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-190. Funciones: IRQ-17, OBJ-05. |
| **Notas** | La jornada se registra en el legajo vinculado a la cuenta del chofer, con origen «aplicación del chofer». No condiciona la disponibilidad para el despacho. |
| **Excepciones** | Si la cuenta no está vinculada a un legajo activo → error de conflicto. Si el chofer ya tiene una jornada abierta → error de conflicto. |
| **Salida** | La jornada abierta. |
| **Precondiciones** | El solicitante es un Chofer autenticado cuya cuenta de acceso está vinculada a un Empleado activo sin jornada abierta. |
| **Postcondiciones** | Se creó una instancia de JornadaDeTrabajo con el instante actual como ingreso, sin egreso y el origen «aplicación del chofer». Se formó la asociación Empleado registra JornadaDeTrabajo con el empleado cuya cuenta de acceso es la del chofer. |

---

#### Secundario Contrato: `registrarFinDeJornada()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarFinDeJornada()` |
| **Responsabilidades** | Marcar desde la App Chofer el final de la jornada del chofer autenticado. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-190. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Cierra la jornada abierta del legajo vinculado a la cuenta del chofer. |
| **Excepciones** | Si la cuenta no está vinculada a un legajo activo o el chofer no tiene ninguna jornada abierta → error de conflicto. |
| **Salida** | La jornada cerrada. |
| **Precondiciones** | El solicitante es un Chofer autenticado cuya cuenta de acceso está vinculada a un Empleado activo con una JornadaDeTrabajo abierta. |
| **Postcondiciones** | El atributo egreso de la instancia de JornadaDeTrabajo abierta del empleado tomó el instante actual. |

---

#### Importante Contrato: `registrarLicencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarLicencia(empleadoId identificador, tipo cadena, desde fecha, hasta fecha, motivo cadena)` |
| **Responsabilidades** | Registrar una licencia o ausencia de un empleado con su tipo y su período. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-191. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Los días se calculan como días corridos. La licencia nace solicitada; la aprobación es otra operación (aprobarLicencia). Una restricción de exclusión de la base impide que dos licencias solicitadas o aprobadas del mismo empleado se superpongan, aun con pedidos simultáneos. |
| **Excepciones** | Si el empleado no existe o es de otra distribuidora → recurso no encontrado. Si está egresado o el período se superpone con otra licencia solicitada o aprobada → error de conflicto. Si la fecha de fin es anterior a la de inicio o el tipo no es válido → error de solicitud. |
| **Salida** | La licencia solicitada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado existe, es de su Distribuidora y está activo. |
| **Postcondiciones** | Se creó una instancia de LicenciaLaboral con su tipo, su período, sus días corridos y el estado «solicitada». Se formó la asociación Empleado solicita LicenciaLaboral. |

---

#### Importante Contrato: `modificarLicencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarLicencia(licenciaId identificador, datos registro)` |
| **Responsabilidades** | Cambiar el tipo, el período o el motivo de una licencia mientras está solicitada. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-191. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Se recalculan los días y se repite el control de superposición con las demás licencias del empleado. |
| **Excepciones** | Si la licencia no existe o es de otra distribuidora → recurso no encontrado. Si no está solicitada o el período nuevo se superpone con otra → error de conflicto. Si un dato no es válido → error de solicitud. |
| **Salida** | La licencia modificada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La LicenciaLaboral existe, es de su Distribuidora y su estado es «solicitada». |
| **Postcondiciones** | Los atributos tipo, desde, hasta y motivo de la instancia de LicenciaLaboral tomaron los valores recibidos y su atributo días se recalculó. |

---

#### Importante Contrato: `cancelarLicencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cancelarLicencia(licenciaId identificador)` |
| **Responsabilidades** | Cancelar una licencia solicitada o aprobada que no terminó. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-191. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Una licencia cancelada libera el período para otras. No se puede volver a solicitar: se registra una nueva. Una licencia ya terminada no se cancela. |
| **Excepciones** | Si la licencia no existe o es de otra distribuidora → recurso no encontrado. Si ya estaba rechazada o cancelada, o su último día ya pasó → error de conflicto. |
| **Salida** | La licencia cancelada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La LicenciaLaboral existe, es de su Distribuidora, su estado es «solicitada» o «aprobada» y su último día no pasó. |
| **Postcondiciones** | El atributo estado de la instancia de LicenciaLaboral pasó a «cancelada». |

---

#### Importante Contrato: `aprobarLicencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `aprobarLicencia(licenciaId identificador)` |
| **Responsabilidades** | Aprobar una licencia solicitada. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-192. Funciones: IRQ-17, OBJ-05. |
| **Notas** | Deja asentado quién la aprobó y cuándo. Una licencia aprobada que cubre el día de hoy inhabilita al chofer para el despacho y figura en el tablero de personal. |
| **Excepciones** | Si la licencia no existe o es de otra distribuidora → recurso no encontrado. Si no está solicitada → error de conflicto. |
| **Salida** | La licencia aprobada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La LicenciaLaboral existe, es de su Distribuidora y su estado es «solicitada». |
| **Postcondiciones** | El atributo estado de la instancia de LicenciaLaboral pasó a «aprobada» y su atributo resuelta el tomó el instante de la decisión. Se formó la asociación Usuario resuelve LicenciaLaboral con el administrador que la aprobó. |

---

#### Importante Contrato: `rechazarLicencia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `rechazarLicencia(licenciaId identificador, motivo cadena)` |
| **Responsabilidades** | Rechazar una licencia solicitada, con un motivo. |
| **Tipo** | Sistema (planificado, I-11) |
| **Referencias cruzadas** | Casos de uso: CU-192. Funciones: IRQ-17, OBJ-05. |
| **Notas** | El motivo es obligatorio y queda en la licencia, en un atributo propio distinto del motivo de la solicitud. Deja asentado quién la rechazó y cuándo. |
| **Excepciones** | Si la licencia no existe o es de otra distribuidora → recurso no encontrado. Si no está solicitada → error de conflicto. Si falta el motivo → error de solicitud. |
| **Salida** | La licencia rechazada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La LicenciaLaboral existe, es de su Distribuidora y su estado es «solicitada». |
| **Postcondiciones** | El atributo estado de la instancia de LicenciaLaboral pasó a «rechazada», su atributo motivo de rechazo tomó el motivo recibido y su atributo resuelta el tomó el instante de la decisión. Se formó la asociación Usuario resuelve LicenciaLaboral con el administrador que la rechazó. |
#### Importante Contrato: `registrarDeposito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarDeposito(nombre cadena, codigo cadena, tipo cadena, direccion cadena)` |
| **Responsabilidades** | Dar de alta un depósito o sucursal de la distribuidora, con su ubicación de stock. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-258. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | El código es único entre los depósitos vigentes de la distribuidora. El primer depósito de la distribuidora queda como predeterminado. La ubicación de stock se crea con el depósito y empieza sin saldo. |
| **Excepciones** | Si falta la distribuidora → error de solicitud. Si el código ya lo usa otro depósito vigente → conflicto. |
| **Salida** | El depósito creado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El código no lo usa otro depósito vigente. |
| **Postcondiciones** | Se creó una instancia de Deposito de la distribuidora, con su nombre, código, tipo y dirección. Se creó una instancia de UbicacionDeStock asociada a él, sin saldo. El atributo predeterminado de la instancia de Deposito pasó a verdadero si la distribuidora no tenía otro predeterminado. |

---

#### Importante Contrato: `actualizarDeposito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarDeposito(depositoId identificador, datos registro)` |
| **Responsabilidades** | Modificar los datos de un depósito vigente. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-259. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Sólo cambian los campos enviados. El código sigue siendo único entre los vigentes. |
| **Excepciones** | Si el depósito no existe o es de otra distribuidora → recurso no encontrado. Si el código ya lo usa otro → conflicto. |
| **Salida** | El depósito modificado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El depósito existe y es de la distribuidora. |
| **Postcondiciones** | El atributo nombre, código, tipo o dirección de la instancia de Deposito tiene el valor enviado. |

---

#### Importante Contrato: `darDeBajaDeposito()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `darDeBajaDeposito(depositoId identificador)` |
| **Responsabilidades** | Dar de baja un depósito sin saldo. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-260. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | La baja es lógica: el depósito conserva su historial de movimientos. El depósito predeterminado no se da de baja mientras haya otros vigentes. |
| **Excepciones** | Si el depósito no existe o es de otra distribuidora → recurso no encontrado. Si su ubicación tiene algún saldo distinto de cero, o si es el predeterminado → conflicto. |
| **Salida** | La confirmación de la baja. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El depósito existe y su ubicación de stock no tiene saldo. |
| **Postcondiciones** | El atributo activo de la instancia de Deposito pasó a falso y el depósito quedó con la fecha de baja. |

---

#### Secundario Contrato: `configurarStockMinimo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `configurarStockMinimo(depositoId identificador, minimos lista)` |
| **Responsabilidades** | Fijar el mínimo de unidades llenas de un depósito para cada tipo de garrafa indicado. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-210. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Hay un solo umbral por depósito y tipo de garrafa: se crea si no existía y se actualiza si ya estaba. Un mínimo en cero equivale a no controlar ese tipo. |
| **Excepciones** | Si el depósito o un tipo de garrafa no existen o son de otra distribuidora → recurso no encontrado. Si un mínimo es negativo → error de solicitud con el detalle del campo. |
| **Salida** | Los umbrales vigentes del depósito. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El depósito existe y es de la distribuidora. |
| **Postcondiciones** | Se creó una instancia de UmbralDeStock del depósito por cada tipo de garrafa que no tenía umbral. El atributo mínimo de llenas de cada instancia de UmbralDeStock tiene el valor indicado. |

---

#### Importante Contrato: `avisarStockBajo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `avisarStockBajo()` |
| **Responsabilidades** | Avisar a los administradores los depósitos que bajaron de su mínimo de unidades llenas. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-211. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | El aviso se emite una sola vez por umbral hasta que el depósito se recupere. Los administradores sin correo cargado no reciben el aviso. El correo es un efecto del sistema hacia el actor, no una postcondición del modelo. |
| **Excepciones** | Si el envío falla → el umbral no se marca y se reintenta en el ciclo siguiente. |
| **Salida** | Ninguna: es un proceso automático. |
| **Precondiciones** | Existen umbrales configurados (CU-210). |
| **Postcondiciones** | El atributo avisado el de cada instancia de UmbralDeStock que bajó de su mínimo tiene el instante del aviso. El atributo avisado el de cada umbral cuyo depósito se recuperó quedó vacío. |

---

#### Secundario Contrato: `transferirStock()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `transferirStock(origenId identificador, destinoId identificador, productoId identificador, condicion cadena, cantidad entero)` |
| **Responsabilidades** | Trasladar una cantidad de un tipo de garrafa y condición de un depósito a otro de la distribuidora. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-212. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Un movimiento con la ubicación de origen y la de destino. No cambia el stock vendible. Los saldos se bloquean en un orden fijo. Con la misma clave de idempotencia no se repite. |
| **Excepciones** | Si una ubicación no existe o es de otra distribuidora → recurso no encontrado. Si el origen no tiene la cantidad, o origen y destino son el mismo → error de solicitud. |
| **Salida** | El resultado de la operación. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. Las dos ubicaciones existen, son distintas y el origen tiene la cantidad. |
| **Postcondiciones** | Se creó una instancia de MovimientoDeStock con la ubicación de origen y la de destino. El saldo del origen disminuyó y el del destino aumentó en la cantidad indicada. |

---

#### Importante Contrato: `registrarAjusteDeStock()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarAjusteDeStock(ubicacionId identificador, motivo cadena, nota cadena, items lista)` |
| **Responsabilidades** | Registrar la corrección del stock de una ubicación, con su motivo y una nota obligatoria. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-213. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Cada ajuste lleva un número correlativo por distribuidora. Los renglones de unidades llenas mueven también el stock vendible. Ningún saldo ni el vendible quedan en negativo. Un daño pasa unidades de llenas a defectuosas dentro de la misma ubicación. |
| **Excepciones** | Si la nota está vacía o un renglón no tiene diferencia → error de solicitud. Si la ubicación no existe o es de otra distribuidora → recurso no encontrado. Si algún saldo quedaría negativo → error de solicitud con el detalle. |
| **Salida** | El ajuste registrado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La ubicación existe y es de la distribuidora. |
| **Postcondiciones** | Se creó una instancia de AjusteDeStock, con sus instancias de ItemAjusteDeStock. Se creó una instancia de MovimientoDeStock por cada renglón. El atributo stock de la instancia de Producto cambió, por las unidades llenas, en la diferencia del renglón. El saldo de la ubicación cambió en la diferencia de cada renglón. |

---

#### Importante Contrato: `registrarProveedor()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarProveedor(razonSocial cadena, cuit cadena, tipo cadena, datosDeContacto registro, plazoDePago entero)` |
| **Responsabilidades** | Dar de alta un proveedor de la distribuidora. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-261. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | El CUIT es único entre los proveedores vigentes de la distribuidora y se valida con su dígito verificador. |
| **Excepciones** | Si falta la distribuidora → error de solicitud. Si el CUIT es inválido → error de solicitud con el detalle del campo. Si el CUIT ya pertenece a un proveedor vigente → conflicto. |
| **Salida** | El proveedor creado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El CUIT no pertenece a otro proveedor vigente. |
| **Postcondiciones** | Se creó una instancia de Proveedor de la Distribuidora, con su razón social, CUIT, tipo, datos de contacto y plazo de pago. |

---

#### Importante Contrato: `actualizarProveedor()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `actualizarProveedor(proveedorId identificador, datos registro)` |
| **Responsabilidades** | Modificar los datos de un proveedor vigente. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-262. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Sólo cambian los campos enviados. El CUIT sigue siendo único entre los vigentes. |
| **Excepciones** | Si el proveedor no existe o es de otra distribuidora → recurso no encontrado. Si el CUIT ya pertenece a otro → conflicto. |
| **Salida** | El proveedor modificado. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El proveedor existe y es de la distribuidora. |
| **Postcondiciones** | El atributo razón social, CUIT, tipo, contacto, teléfono, correo, dirección o plazo de pago de la instancia de Proveedor tiene el valor enviado. |

---

#### Importante Contrato: `darDeBajaProveedor()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `darDeBajaProveedor(proveedorId identificador)` |
| **Responsabilidades** | Dar de baja un proveedor, conservando su historial de compras. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-263. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | La baja es lógica: las órdenes y las recepciones ya registradas siguen apuntando al proveedor. |
| **Excepciones** | Si el proveedor no existe o es de otra distribuidora → recurso no encontrado. |
| **Salida** | La confirmación de la baja. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El proveedor existe y es de la distribuidora. |
| **Postcondiciones** | El atributo activo de la instancia de Proveedor pasó a falso y el proveedor quedó con la fecha de baja. |

---

#### Importante Contrato: `emitirOrdenDeCompra()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `emitirOrdenDeCompra(proveedorId identificador, depositoId identificador, items lista, fechaEsperada fecha)` |
| **Responsabilidades** | Preparar una orden de compra a un proveedor para un depósito destino, en borrador. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-215. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | El número es correlativo por distribuidora. El total es la suma de cantidad por costo unitario de los renglones. Un tipo de garrafa no se repite dentro de la orden. Con la misma clave de idempotencia no se repite. |
| **Excepciones** | Si el proveedor o el depósito no existen o son de otra distribuidora → recurso no encontrado. Si un renglón repite un tipo de garrafa o tiene una cantidad no positiva → error de solicitud con el detalle del campo. |
| **Salida** | La orden de compra en borrador. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El proveedor y el depósito existen, son de la distribuidora y están vigentes. |
| **Postcondiciones** | Se creó una instancia de OrdenDeCompra del Proveedor, destinada al Deposito indicado, en estado borrador, con su número y su total, y una instancia de ItemOrdenDeCompra por cada tipo de garrafa pedido. |

---

#### Importante Contrato: `enviarOrdenDeCompra()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `enviarOrdenDeCompra(ordenId identificador)` |
| **Responsabilidades** | Pasar una orden de compra de borrador a enviada. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-215. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Sólo una orden en borrador puede enviarse. Registra el instante de emisión. |
| **Excepciones** | Si la orden no existe o es de otra distribuidora → recurso no encontrado. Si la orden no está en borrador → conflicto. |
| **Salida** | La orden enviada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La orden existe y está en borrador. |
| **Postcondiciones** | El atributo estado de la instancia de OrdenDeCompra pasó a enviada y su atributo emitida el tiene el instante del envío. |

---

#### Secundario Contrato: `cancelarOrdenDeCompra()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cancelarOrdenDeCompra(ordenId identificador, motivo cadena)` |
| **Responsabilidades** | Cancelar una orden de compra que todavía no tiene recepciones. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-216. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Sólo se cancela una orden en borrador o enviada y sin recepciones. La cancelación no mueve stock. |
| **Excepciones** | Si la orden no existe o es de otra distribuidora → recurso no encontrado. Si ya tiene recepciones, o está recibida o cancelada → conflicto. |
| **Salida** | La orden cancelada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La orden existe, está en borrador o enviada y no tiene recepciones. |
| **Postcondiciones** | El atributo estado de la instancia de OrdenDeCompra pasó a cancelada y su atributo motivo de cancelación tiene el motivo indicado. |

---

#### Crítico Contrato: `registrarRecepcionDeCompra()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarRecepcionDeCompra(ordenId identificador, proveedorId identificador, depositoId identificador, tipoDeComprobante cadena, numeroDeComprobante cadena, items lista)` |
| **Responsabilidades** | Registrar la recepción de una compra: lo llegado de la planta y los vacíos que ésta se llevó. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-217. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Es el remito de ingreso, con o sin orden de compra. El comprobante del proveedor no se repite para un mismo proveedor. Suma las llenas al stock vendible, recalcula el costo promedio ponderado y, si hay orden, acumula lo recibido. Con la misma clave de idempotencia no se repite. |
| **Excepciones** | Si el comprobante ya se registró para el proveedor → conflicto. Si la orden no existe → recurso no encontrado; si está cancelada o recibida → conflicto. Si los vacíos entregados dejarían negativo el saldo del depósito → error de solicitud. |
| **Salida** | La recepción registrada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El depósito existe y es de la distribuidora. Si hay orden, está enviada o parcialmente recibida. |
| **Postcondiciones** | Se creó una instancia de RecepcionDeCompra del depósito, con sus instancias de ItemRecepcion. Se creó una instancia de MovimientoDeStock por tipo de garrafa recibido, la entrada de las llenas y la salida de los vacíos canjeados. El atributo stock de la instancia de Producto aumentó en las llenas recibidas. El saldo del depósito cambió en esas diferencias y la orden acumuló lo recibido. |

---

#### Crítico Contrato: `anularRecepcionDeCompra()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `anularRecepcionDeCompra(recepcionId identificador, motivo cadena)` |
| **Responsabilidades** | Anular una recepción confirmada, con contraasientos. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-217. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Sólo se anula si el depósito todavía tiene las llenas que la recepción ingresó. La anulación no borra nada: registra los movimientos inversos. |
| **Excepciones** | Si la recepción no existe o es de otra distribuidora → recurso no encontrado. Si ya está anulada, o el depósito ya no tiene lo ingresado → conflicto. |
| **Salida** | La recepción anulada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La recepción existe, está confirmada y el depósito tiene aún las llenas ingresadas. |
| **Postcondiciones** | El atributo estado de la instancia de RecepcionDeCompra pasó a anulada y su atributo motivo de anulación tiene el motivo indicado. Se creó una instancia de MovimientoDeStock inversa por cada movimiento de la recepción. El atributo stock de la instancia de Producto disminuyó en las llenas ingresadas. |

---

#### Crítico Contrato: `registrarCargaDelCamion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarCargaDelCamion(vehiculoId identificador, depositoId identificador, ayudanteId identificador, items lista)` |
| **Responsabilidades** | Abrir la hoja de carga de un camión y trasladar las garrafas del depósito al vehículo. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-218. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | El vehículo tiene que estar en uso por un chofer. Un vehículo y un chofer tienen una sola carga abierta a la vez. El número es correlativo por distribuidora. Con la misma clave de idempotencia no se repite. |
| **Excepciones** | Si el vehículo no está en uso, o el vehículo o el chofer ya tienen una carga abierta → conflicto. Si el depósito no tiene las unidades → error de solicitud con el saldo disponible. Si el vehículo o el depósito no existen → recurso no encontrado. |
| **Salida** | La hoja de carga abierta. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. El vehículo está en uso por un chofer y sin otra carga abierta. El depósito tiene las unidades. |
| **Postcondiciones** | Se creó una instancia de CargaDeCamion del Vehiculo, en estado cargando, con una instancia de ItemCarga por cada tipo de garrafa. Se creó una instancia de MovimientoDeStock por renglón, del depósito al camión. El saldo del depósito disminuyó y el del camión aumentó. |

---

#### Crítico Contrato: `reponerCargaDelCamion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `reponerCargaDelCamion(cargaId identificador, items lista)` |
| **Responsabilidades** | Cargar más mercadería en un camión que tiene la carga abierta. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-218. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Aplica mientras la carga está cargando o en ruta. Las unidades se suman al renglón de reposición del tipo de garrafa. |
| **Excepciones** | Si la carga no existe o es de otra distribuidora → recurso no encontrado. Si la carga ya regresó o está cerrada → conflicto. Si el depósito no tiene las unidades → error de solicitud. |
| **Salida** | La hoja de carga actualizada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La carga está cargando o en ruta y el depósito tiene las unidades. |
| **Postcondiciones** | El atributo llenas repuestas de cada instancia de ItemCarga aumentó en lo repuesto. Se creó una instancia de MovimientoDeStock del depósito al camión por cada reposición. El saldo del depósito disminuyó y el del camión aumentó. |

---

#### Crítico Contrato: `cancelarCargaDelCamion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cancelarCargaDelCamion(cargaId identificador)` |
| **Responsabilidades** | Cancelar una carga que todavía no salió y devolver todo al depósito. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-218. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Sólo se cancela una carga en estado cargando. |
| **Excepciones** | Si la carga no existe o es de otra distribuidora → recurso no encontrado. Si la carga ya salió → conflicto. |
| **Salida** | La hoja de carga cancelada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La carga existe y está cargando. |
| **Postcondiciones** | El atributo estado de la instancia de CargaDeCamion pasó a cancelada. Se creó una instancia de MovimientoDeStock del camión al depósito por cada renglón. El saldo del camión quedó en cero. |

---

#### Importante Contrato: `registrarSalidaDelCamion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarSalidaDelCamion(cargaId identificador)` |
| **Responsabilidades** | Declarar que el camión salió a repartir. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-219. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Lo inicia el chofer, sólo sobre su propia carga, o el administrador. No mueve stock. |
| **Excepciones** | Si la carga no existe, es de otro chofer o de otra distribuidora → recurso no encontrado. Si la carga no está cargando → conflicto. |
| **Salida** | La hoja de carga en ruta. |
| **Precondiciones** | El solicitante es el chofer de la carga o un Administrador de la distribuidora. La carga está cargando. |
| **Postcondiciones** | El atributo estado de la instancia de CargaDeCamion pasó a en ruta y su atributo salió el tiene el instante de la salida. |

---

#### Crítico Contrato: `descontarStockDeLaEntrega()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `descontarStockDeLaEntrega(pedidoId identificador)` |
| **Responsabilidades** | Descontar del camión, o del depósito predeterminado, lo entregado en un pedido y acreditar los vacíos recolectados. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-220. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Reacciona al evento de pedido entregado. Es idempotente por pedido y tipo de garrafa. No toca el stock vendible, que ya se descontó al reservar. El canje es de uno a uno. |
| **Excepciones** | Si el movimiento del pedido ya existe → no hace nada. Si el camión con carga abierta no tiene lo entregado → no registra nada y deja el pedido para el barrido de conciliación. |
| **Salida** | Ninguna: es un proceso automático. |
| **Precondiciones** | El pedido está entregado. |
| **Postcondiciones** | Se creó una instancia de MovimientoDeStock de entrega y otra de recolección de vacíos por cada ítem del pedido, con el pedido como documento de origen. Las llenas de la ubicación de origen disminuyeron y las vacías aumentaron en lo entregado. |

---

#### Importante Contrato: `registrarRegresoDelCamion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarRegresoDelCamion(cargaId identificador, devueltos lista)` |
| **Responsabilidades** | Declarar lo que el camión trae de vuelta, por tipo de garrafa. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-221. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Sólo declara: no mueve stock hasta el cierre de la rendición. Lo esperado es lo cargado y repuesto menos lo entregado, y los vacíos cargados más los recolectados. |
| **Excepciones** | Si la carga no existe, es de otro chofer o de otra distribuidora → recurso no encontrado. Si la carga no está en ruta → conflicto. Si una cantidad es negativa → error de solicitud. |
| **Salida** | La hoja de carga con lo declarado, lo esperado y la diferencia por renglón. |
| **Precondiciones** | El solicitante es el chofer de la carga o un Administrador de la distribuidora. La carga está en ruta. |
| **Postcondiciones** | El atributo estado de la instancia de CargaDeCamion pasó a regresó y su atributo regresó el tiene el instante del regreso. Los atributos llenos y vacíos declarados al regreso de cada ItemCarga tienen lo declarado. |

---

#### Crítico Contrato: `cerrarRendicionDeStock()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cerrarRendicionDeStock(cargaId identificador, nota cadena)` |
| **Responsabilidades** | Cerrar la carga: devolver lo declarado al depósito y asentar la diferencia. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-222. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Al cerrar, el saldo del camión queda en cero. El faltante se asienta como merma y el sobrante como ajuste, con la carga como documento de origen. Si faltaron llenas, se descuentan del stock vendible. Con diferencia, la nota es obligatoria. |
| **Excepciones** | Si la carga no existe o es de otra distribuidora → recurso no encontrado. Si la carga no regresó → conflicto. Si hay diferencia y la nota está vacía → error de solicitud. Si el faltante dejaría negativo el vendible → error de solicitud. |
| **Salida** | La hoja de carga cerrada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. La carga regresó. |
| **Postcondiciones** | El atributo estado de la instancia de CargaDeCamion pasó a cerrada, o a cerrada con diferencia, y su atributo cerrada el tiene el instante del cierre. Se creó una instancia de MovimientoDeStock por lo declarado que vuelve al depósito y por cada diferencia. El saldo del camión quedó en cero. El atributo stock de la instancia de Producto disminuyó en el faltante de llenas. |

---

#### Importante Contrato: `conciliarStock()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `conciliarStock()` |
| **Responsabilidades** | Aplicar las entregas que quedaron sin movimiento de stock y avisar la diferencia entre el stock vendible y el físico menos lo reservado. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-224. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Corre una vez por noche. No corrige el vendible: una diferencia se resuelve con un ajuste. El aviso por correo es un efecto del sistema hacia el actor, no una postcondición del modelo. |
| **Excepciones** | Si la aplicación de una entrega falla → sigue con las demás y se reintenta la noche siguiente. |
| **Salida** | Ninguna: es un proceso automático. |
| **Precondiciones** | Existen pedidos entregados o tipos de garrafa con stock. |
| **Postcondiciones** | Se creó una instancia de MovimientoDeStock por cada pedido entregado que no tenía movimientos, con el procedimiento de la operación descontarStockDeLaEntrega. El stock vendible de cada Producto no cambia. |

---

#### Secundario Contrato: `configurarControlDeCargaAbierta()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `configurarControlDeCargaAbierta(exigirCargaDeCamionAbierta booleano)` |
| **Responsabilidades** | Prender o apagar, para la distribuidora, la exigencia de una carga de camión abierta para recibir pedidos. |
| **Tipo** | Sistema (planificado, I-13) |
| **Referencias cruzadas** | Casos de uso: CU-249. Funciones: IRQ-18, OBJ-05, OBJ-06. |
| **Notas** | Hay una sola configuración por distribuidora y proceso. Viene apagada. Los pedidos ya asignados no se revisan. |
| **Excepciones** | Si falta la distribuidora → error de solicitud. Si el valor no es booleano → error de solicitud con el detalle del campo. |
| **Salida** | La configuración guardada. |
| **Precondiciones** | El Administrador está autenticado, con una distribuidora asociada. |
| **Postcondiciones** | El atributo exigir carga de camión abierta de la instancia de ConfiguracionModulo de la distribuidora tiene el valor indicado, con el administrador que lo modificó y la fecha. |
#### Importante Contrato: `crearCaja()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearCaja(nombre cadena, tipo cadena, requiereSesion booleano)` |
| **Responsabilidades** | Dar de alta una caja de la distribuidora —efectivo, banco o billetera— para llevar su saldo y sus movimientos. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-225. Funciones: IRQ-19, OBJ-05. |
| **Notas** | El saldo nace en cero y sólo lo mueven los movimientos del libro. Una caja de efectivo exige sesión abierta para registrar movimientos, salvo que se indique lo contrario al crearla. Cada distribuidora tiene sembrada una «Caja central». |
| **Excepciones** | Si ya existe una caja vigente de la distribuidora con ese nombre → conflicto. Si el tipo no es efectivo, banco o billetera → error de solicitud. |
| **Salida** | La caja creada, con saldo cero. |
| **Precondiciones** | El solicitante es Administrador o Administrador General, con una Distribuidora en contexto. |
| **Postcondiciones** | Se creó una instancia de Caja, asociada a la Distribuidora, con saldo cero, el nombre, el tipo y la marca de sesión indicados, y activa. |

---

#### Importante Contrato: `modificarCaja()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarCaja(cajaId identificador, datos registro)` |
| **Responsabilidades** | Cambiar el nombre, la marca de sesión o el estado activo de una caja. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-264. Funciones: IRQ-19, OBJ-05. |
| **Notas** | El tipo y el saldo no se editan: el saldo sólo lo modifica el libro. Una caja con sesión abierta no se puede desactivar. |
| **Excepciones** | Si la caja no existe o es de otra distribuidora → recurso no encontrado. Si se la desactiva con una sesión abierta → conflicto. Si el nombre ya lo usa otra caja → conflicto. |
| **Salida** | La caja con los datos nuevos. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La Caja pertenece a su Distribuidora. |
| **Postcondiciones** | Los atributos nombre, requiere sesión y activa de la instancia de Caja tomaron los valores indicados. |

---

#### Importante Contrato: `abrirCaja()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `abrirCaja(cajaId identificador, montoInicial moneda)` |
| **Responsabilidades** | Abrir la sesión de trabajo de una caja con su monto inicial, para que el arqueo del cierre tenga con qué compararse. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-226. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Una caja tiene a lo sumo una sesión abierta (índice único parcial por estado). Las cajas de banco y de billetera, que no exigen sesión, no se abren. El monto inicial es lo que el administrador cuenta al abrir. Si no coincide con el saldo que el libro le da a la caja, el sistema asienta un ajuste de apertura, por el libro de movimientos (CU-228), para que el saldo de la caja sea el monto inicial. |
| **Excepciones** | Si la caja no existe o es de otra distribuidora → recurso no encontrado. Si la caja ya tiene una sesión abierta → conflicto. Si la caja no exige sesión → error de solicitud. Si el monto inicial es negativo → error de solicitud. |
| **Salida** | La sesión abierta. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La Caja pertenece a su Distribuidora, está activa y no tiene una sesión abierta. |
| **Postcondiciones** | Se creó una instancia de SesionDeCaja en estado «abierta», asociada a la Caja, con el monto inicial indicado y el Administrador que la abrió. Si el monto inicial difiere del saldo de la Caja, se creó una instancia de MovimientoDeCaja de ajuste de apertura y el saldo de la Caja quedó igual al monto inicial. |

---

#### Crítico Contrato: `cerrarCajaConArqueo()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `cerrarCajaConArqueo(sesionId identificador, montoContado moneda)` |
| **Responsabilidades** | Cerrar la sesión de una caja comparando el saldo que debería haber con lo que se contó, y dejar el saldo igual a lo contado. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-227. Funciones: IRQ-19, OBJ-05. |
| **Notas** | El monto esperado es el saldo teórico de la caja: el que el libro le da al momento de cerrar. La diferencia es el monto contado menos ese saldo: negativa es faltante y positiva, sobrante. Si no es cero, el sistema asienta primero un movimiento de ajuste con la categoría de sistema «diferencia de caja», por el libro de movimientos (CU-228), y después cierra la sesión: así el saldo refleja lo contado y la sesión se cierra con un libro ya consistente. |
| **Excepciones** | Si la sesión no existe o es de otra distribuidora → recurso no encontrado. Si la sesión ya está cerrada → conflicto. Si el monto contado es negativo → error de solicitud. |
| **Salida** | La sesión cerrada, con el monto esperado, el contado y la diferencia. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La SesionDeCaja pertenece a su Distribuidora y está abierta. |
| **Postcondiciones** | Si la diferencia no es cero, se creó una instancia de MovimientoDeCaja de ajuste y el saldo de la Caja quedó igual al monto contado. Los atributos estado, monto esperado, monto contado, diferencia y cerrada el de la instancia de SesionDeCaja tomaron sus valores de cierre. |

---

#### Crítico Contrato: `registrarMovimientoDeCaja()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarMovimientoDeCaja(cajaId identificador, sentido cadena, importe moneda, categoriaId identificador, medio cadena, descripcion cadena)` |
| **Responsabilidades** | Asentar un ingreso o un egreso manual en una caja, con su categoría y su medio, y actualizar el saldo. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-228. Funciones: IRQ-19, OBJ-05. |
| **Notas** | El libro es de sólo agregar: un movimiento no se edita ni se borra, se corrige con otro (CU-229). Toda escritura del saldo pasa por el mismo punto, que bloquea la caja, valida la sesión y actualiza el saldo en la misma transacción. Los movimientos que generan otros casos de uso (rendición, pago de cuenta corriente, liquidación) usan esta misma operación. Lleva clave de idempotencia: un reintento no duplica el asiento. |
| **Excepciones** | Si la caja o la categoría no existen o son de otra distribuidora → recurso no encontrado. Si la caja exige sesión y no la tiene abierta → conflicto. Si el sentido de la categoría no es el del movimiento → error de solicitud. Si el importe no es mayor que cero → error de solicitud. Si es un egreso de una caja de efectivo y el saldo no alcanza → conflicto. |
| **Salida** | El movimiento registrado. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La Caja y la CategoriaDeCaja pertenecen a su Distribuidora, la Caja está activa y, si exige sesión, tiene una abierta. |
| **Postcondiciones** | Se creó una instancia de MovimientoDeCaja, asociada a la Caja y a la CategoriaDeCaja, con el sentido, el importe, el medio y la descripción indicados. El atributo saldo de la Caja aumentó o disminuyó en el importe, según el sentido. |

---

#### Crítico Contrato: `transferirEntreCajas()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `transferirEntreCajas(cajaOrigenId identificador, cajaDestinoId identificador, importe moneda)` |
| **Responsabilidades** | Mover fondos de una caja a otra de la distribuidora, como un egreso en la de origen y un ingreso en la de destino. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-228. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Son dos movimientos con la categoría de sistema «transferencia entre cajas», en la misma transacción: se registran los dos o ninguno. Las dos cajas se bloquean en orden de identificador para que dos transferencias opuestas no se traben entre sí. |
| **Excepciones** | Si alguna de las cajas no existe o es de otra distribuidora → recurso no encontrado. Si el origen y el destino son la misma caja → error de solicitud. Si el importe no es mayor que cero → error de solicitud. Si el origen es de efectivo y su saldo no alcanza → conflicto. Si alguna caja exige sesión y no la tiene abierta → conflicto. |
| **Salida** | Los dos movimientos, el de salida y el de entrada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. Las dos Caja pertenecen a su Distribuidora, están activas y son distintas. |
| **Postcondiciones** | Se creó una instancia de MovimientoDeCaja de egreso en la Caja de origen y otra de ingreso en la Caja de destino, por el mismo importe. El saldo de cada Caja quedó actualizado. |

---

#### Importante Contrato: `anularMovimientoDeCaja()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `anularMovimientoDeCaja(movimientoId identificador, motivo cadena)` |
| **Responsabilidades** | Corregir un movimiento de caja asentando otro de sentido contrario, sin tocar el original. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-229. Funciones: IRQ-19, OBJ-05. |
| **Notas** | El libro no admite ediciones: la anulación es un contraasiento que apunta al movimiento original, y un movimiento se anula una sola vez. El motivo queda en la descripción del contraasiento. No se anula un movimiento que ya es una anulación. Si la caja exige sesión, el contraasiento entra en la sesión abierta. |
| **Excepciones** | Si el movimiento no existe o es de otra distribuidora → recurso no encontrado. Si ya fue anulado o es a su vez una anulación → conflicto. Si el contraasiento deja una caja de efectivo en saldo negativo → conflicto. Si el motivo falta → error de solicitud. |
| **Salida** | El movimiento de anulación. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El MovimientoDeCaja pertenece a su Distribuidora y no fue anulado. |
| **Postcondiciones** | Se creó una instancia de MovimientoDeCaja de sentido contrario al del movimiento original y asociada a él mediante «anula a». El saldo de la Caja quedó actualizado con el sentido inverso. |

---

#### Secundario Contrato: `crearCategoriaDeCaja()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearCategoriaDeCaja(nombre cadena, sentido cadena)` |
| **Responsabilidades** | Dar de alta una categoría para clasificar los ingresos o los gastos de caja. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-230. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Las categorías de sistema (rendición de chofer, cobro de cuenta corriente, compras, combustible, multas, pago de comisiones, diferencia de caja y transferencia entre cajas) se siembran con la distribuidora y no se crean desde acá; esta operación da de alta las propias de cada distribuidora. |
| **Excepciones** | Si ya existe una categoría con ese nombre y ese sentido → conflicto. Si el sentido no es ingreso o egreso → error de solicitud. |
| **Salida** | La categoría creada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General, con una Distribuidora en contexto. |
| **Postcondiciones** | Se creó una instancia de CategoriaDeCaja, asociada a la Distribuidora, con el nombre y el sentido indicados, activa y sin código de sistema. |

---

#### Secundario Contrato: `modificarCategoriaDeCaja()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarCategoriaDeCaja(categoriaId identificador, datos registro)` |
| **Responsabilidades** | Cambiar el nombre de una categoría o desactivarla, sin perder los movimientos que ya la usan. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-265. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Desactivar no borra: los movimientos anteriores conservan su categoría. Las categorías de sistema no se modifican ni se desactivan, porque los procesos automáticos las buscan por su código. La baja que ofrece el panel es una desactivación. |
| **Excepciones** | Si la categoría no existe o es de otra distribuidora → recurso no encontrado. Si es una categoría de sistema → conflicto. Si el nombre y el sentido ya los tiene otra categoría → conflicto. |
| **Salida** | La categoría con los datos nuevos. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La CategoriaDeCaja pertenece a su Distribuidora. |
| **Postcondiciones** | Los atributos nombre y activa de la instancia de CategoriaDeCaja tomaron los valores indicados. |

---

#### Importante · automático Contrato: `generarRendicionesDelDia()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `generarRendicionesDelDia()` |
| **Responsabilidades** | Abrir, al cierre de cada día, la rendición de cada chofer que entregó pedidos cobrados en efectivo y todavía no los rindió. |
| **Tipo** | Sistema (proceso automático) (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-231. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Se ejecuta todos los días a las 23:30, hora de Argentina. Una rendición reúne los pedidos que el chofer entregó en efectivo ese día —el día argentino de la entrega— y que no figuran en otra rendición, y los cobros de cuentas corrientes que hizo en la calle y que todavía no figuran en una rendición. Se abre rendición si el chofer tiene cualquiera de los dos. Un pedido o un cobro se rinde una sola vez: lo que se entrega o se cobra después de presentada la rendición cae en la del día siguiente. Con más de una instancia del sistema, una sola toma el proceso. |
| **Excepciones** | Si el chofer ya tiene una rendición abierta ese día → se completa con lo nuevo y no se crea otra. Si ningún chofer tiene efectivo ni cobros sin rendir → termina sin hacer nada. Si otra instancia ya ejecuta el proceso → se saltea. Si la ejecución falla → se registra el error y se libera el bloqueo. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existe al menos un Chofer con pedidos entregados en efectivo en el día, o con cobros de cuenta corriente hechos en la calle, que no integran ninguna rendición. |
| **Postcondiciones** | Por cada Chofer con efectivo o con cobros sin rendir se creó una instancia de RendicionChofer en estado «abierta», con la fecha del día, o se completó la que ya tenía abierta. Por cada pedido incluido se creó una instancia de PedidoRendido, asociada a la rendición y al Pedido, y cada AsientoCuentaCorriente cobrado en la calle quedó asociado a la rendición. El atributo efectivo esperado de la RendicionChofer quedó igual a la suma de los importes de sus pedidos y de sus cobros. |

---

#### Crítico Contrato: `declararEfectivoRendido()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `declararEfectivoRendido(rendicionId identificador, efectivoDeclarado moneda, gastos lista)` |
| **Responsabilidades** | Registrar cuánto efectivo entrega el chofer y qué gastos pagó con la cobranza, y dejar la rendición presentada con su diferencia. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-232. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Al presentar, el sistema recalcula el efectivo esperado bajo bloqueo de la rendición, para incluir lo entregado desde que se abrió. La diferencia es lo declarado más los gastos, menos lo esperado: negativa es faltante y positiva, sobrante. Los gastos son pagos hechos con la cobranza —combustible, peaje—; los de combustible se enlazan con la carga registrada en el módulo de flota. El chofer sólo presenta la suya; el administrador puede presentar la de cualquier chofer. Una vez presentada no se edita: se reabre (CU-233). |
| **Excepciones** | Si la rendición no existe, es de otra distribuidora o, para un chofer, es de otro chofer → recurso no encontrado. Si no está abierta → conflicto. Si el efectivo declarado o algún gasto es negativo → error de solicitud. Si un gasto no tiene una categoría de egreso → error de solicitud. |
| **Salida** | La rendición presentada, con el efectivo esperado, la diferencia y los gastos. |
| **Precondiciones** | El solicitante es Chofer, dueño de la rendición, o Administrador. La RendicionChofer pertenece a su Distribuidora y está abierta. |
| **Postcondiciones** | El atributo estado de la instancia de RendicionChofer pasó a «presentada», y los atributos efectivo esperado, efectivo declarado, gastos del chofer y diferencia tomaron sus valores. Por cada gasto declarado se creó una instancia de GastoDeRendicion, asociada a la rendición. |

---

#### Crítico Contrato: `aprobarRendicion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `aprobarRendicion(rendicionId identificador, cajaDestinoId identificador, resolucionDeDiferencia cadena)` |
| **Responsabilidades** | Aprobar una rendición presentada: ingresar el efectivo a la caja y resolver la diferencia, si la hay. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-233. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Al aprobar, el efectivo declarado entra a la caja destino con la categoría de sistema «rendición de chofer», por el libro de movimientos (CU-228). El efectivo declarado incluye lo que el chofer cobró de cuentas corrientes en la calle: los asientos de esos cobros pasan a estar rendidos. Si hay diferencia, el administrador la resuelve: la absorbe la distribuidora o se descuenta al chofer. El faltante a cargo del chofer genera un asiento negativo en el libro de comisiones de su empleado, que se descuenta en la próxima liquidación. Con el módulo de stock, la rendición está atada al turno del camión y no se puede aprobar si la carga no está cerrada. |
| **Excepciones** | Si la rendición o la caja no existen o son de otra distribuidora → recurso no encontrado. Si la rendición no está presentada → conflicto. Si hay diferencia y no se indica su resolución → error de solicitud. Si la caja exige sesión y no la tiene abierta → conflicto. Si la rendición está atada a un turno cuya carga no está cerrada → conflicto. |
| **Salida** | La rendición aprobada, con su movimiento de caja. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La RendicionChofer pertenece a su Distribuidora y está presentada. La Caja pertenece a la Distribuidora y está activa. |
| **Postcondiciones** | El atributo estado de la instancia de RendicionChofer pasó a «aprobada», y los atributos resolución de la diferencia y aprobada el tomaron sus valores. Se creó una instancia de MovimientoDeCaja de ingreso en la Caja destino, por el efectivo declarado. Si la diferencia es un faltante a cargo del chofer, se creó una instancia de AsientoComision negativa en el libro del Empleado. |

---

#### Crítico Contrato: `reabrirRendicion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `reabrirRendicion(rendicionId identificador)` |
| **Responsabilidades** | Volver a abrir una rendición presentada, para corregir lo que el chofer declaró. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-233. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Sólo se reabre una rendición presentada y no aprobada. Una rendición aprobada ya movió plata: se corrige anulando su movimiento de caja (CU-229) y no reabriéndola. |
| **Excepciones** | Si la rendición no existe o es de otra distribuidora → recurso no encontrado. Si no está presentada → conflicto. |
| **Salida** | La rendición abierta. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La RendicionChofer pertenece a su Distribuidora y está presentada. |
| **Postcondiciones** | El atributo estado de la instancia de RendicionChofer volvió a «abierta». |

---

#### Importante · automático Contrato: `avisarRendicionesSinCerrar()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `avisarRendicionesSinCerrar()` |
| **Responsabilidades** | Avisar a los administradores de cada distribuidora de las rendiciones de días anteriores que siguen abiertas o presentadas sin aprobar. |
| **Tipo** | Sistema (proceso automático) (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-234. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Se ejecuta todos los días a las 08:00, hora de Argentina. El aviso es un correo por distribuidora con la lista de rendiciones atrasadas; cada rendición se marca como avisada para no repetirlo. Con más de una instancia del sistema, una sola toma el proceso. |
| **Excepciones** | Si no hay rendiciones atrasadas → termina sin hacer nada. Si el correo no sale → se registra el error y la rendición queda sin marcar, de modo que se avisa al día siguiente. Si otra instancia ya ejecuta el proceso → se saltea. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existe al menos una RendicionChofer de un día anterior en estado «abierta» o «presentada» que todavía no fue avisada. |
| **Postcondiciones** | El atributo aviso enviado el de cada instancia de RendicionChofer atrasada quedó con el momento del envío. Los Administradores de la Distribuidora recibieron el correo con la lista de rendiciones. |

---

#### Importante Contrato: `habilitarCuentaCorriente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `habilitarCuentaCorriente(clienteId identificador, razonSocial cadena, cuit cadena, condicionFiscal cadena, limiteDeCredito moneda, plazoEnDias entero)` |
| **Responsabilidades** | Abrir la cuenta corriente de un cliente en la distribuidora, con su razón social, su condición fiscal, su límite de crédito y su plazo de pago. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-235. Funciones: IRQ-19, OBJ-05. |
| **Notas** | La cuenta es de la distribuidora y no del cliente: el cliente es compartido entre distribuidoras y cada una le da el crédito que quiere. Hay una sola cuenta vigente por cliente y distribuidora. El saldo nace en cero y es positivo cuando el cliente debe. La cuenta nace activa. |
| **Excepciones** | Si el cliente no existe → recurso no encontrado. Si el cliente ya tiene una cuenta vigente en la distribuidora → conflicto. Si el CUIT no tiene once dígitos o su dígito verificador es inválido → error de solicitud. Si el límite es negativo o el plazo no es un entero positivo → error de solicitud. |
| **Salida** | La cuenta corriente creada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General, con una Distribuidora en contexto. El Cliente existe y no tiene una cuenta vigente en la Distribuidora. |
| **Postcondiciones** | Se creó una instancia de CuentaCorriente, asociada a la Distribuidora y al Cliente, con saldo cero, estado «activa» y la razón social, el CUIT, la condición fiscal, el límite de crédito y el plazo de pago indicados. |

---

#### Importante Contrato: `modificarCuentaCorriente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarCuentaCorriente(cuentaId identificador, datos registro)` |
| **Responsabilidades** | Cambiar el límite de crédito, el plazo de pago o el estado de una cuenta corriente. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-235. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Bloquear una cuenta impide las ventas nuevas a cuenta pero no los cobros ni los ajustes. Una cuenta se cierra sólo con saldo cero. Bajar el límite por debajo del saldo actual es válido: no se pide plata de vuelta, sólo se impiden las compras nuevas. |
| **Excepciones** | Si la cuenta no existe o es de otra distribuidora → recurso no encontrado. Si se la cierra con saldo distinto de cero → conflicto. Si el límite es negativo o el plazo no es un entero positivo → error de solicitud. |
| **Salida** | La cuenta con los datos nuevos. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La CuentaCorriente pertenece a su Distribuidora. |
| **Postcondiciones** | Los atributos límite de crédito, plazo de pago en días y estado de la instancia de CuentaCorriente tomaron los valores indicados. |

---

#### Crítico Contrato: `registrarCargoDeCuentaCorriente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarCargoDeCuentaCorriente(pedidoId identificador)` |
| **Responsabilidades** | Asentar en la cuenta corriente del cliente el cargo de un pedido a cuenta apenas se entrega. |
| **Tipo** | Sistema (proceso automático) (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-236. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Lo dispara el evento de dominio «pedido entregado», y también el proceso de conciliación nocturno, que genera los cargos que se hayan perdido. Es idempotente: un pedido tiene a lo sumo un cargo (índice único parcial). El vencimiento es la fecha de entrega más el plazo de pago de la cuenta. El cargo y la actualización del saldo van en la misma transacción. |
| **Excepciones** | Si el pedido no se pagó a cuenta corriente → se ignora. Si el pedido ya tiene su cargo → termina sin hacer nada. Si la cuenta se cerró o no existe → se registra el error y el caso queda para la conciliación nocturna. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existe un Pedido entregado, pagado a cuenta corriente, que todavía no tiene cargo. |
| **Postcondiciones** | Se creó una instancia de AsientoCuentaCorriente de tipo «cargo por venta», asociada al Pedido y a la CuentaCorriente, con el total del pedido y su fecha de vencimiento. El atributo saldo de la CuentaCorriente aumentó en el total del Pedido. |

---

#### Crítico Contrato: `venderACuentaCorriente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `venderACuentaCorriente(clienteId identificador, direccionId identificador, items lista)` |
| **Responsabilidades** | Crear, desde el panel, un pedido pagado a cuenta corriente: verificar que el cliente tenga crédito y dejar el pedido en el circuito de entrega. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-236. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Sólo el administrador puede elegir este medio de pago, desde el panel; la app del cliente no lo ofrece. La verificación de crédito corre en la misma transacción que la creación del pedido y bloquea la cuenta, de modo que dos pedidos simultáneos del mismo cliente no pueden superar el límite entre los dos. El crédito disponible es el límite menos el saldo y menos los pedidos a cuenta que todavía no se entregaron. El cargo no se asienta acá sino al entregar el pedido (registrarCargoDeCuentaCorriente). El pedido no pasa por «pagado» al entregarse: es una venta a crédito y los reportes la muestran como «a cuenta». |
| **Excepciones** | Si el cliente no tiene cuenta corriente, o está bloqueada o cerrada → conflicto. Si el total supera el crédito disponible → conflicto, con el disponible en la respuesta. Las demás excepciones son las de crearPedido (CU-005): dirección inexistente, fuera de cobertura, sin stock. |
| **Salida** | El pedido creado y el crédito disponible que queda. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La CuentaCorriente del Cliente en la Distribuidora está activa. |
| **Postcondiciones** | Se creó una instancia de Pedido con el método de pago «cuenta corriente», asociada al Cliente y a su dirección de entrega. El crédito disponible de la CuentaCorriente quedó reducido en el total del Pedido. |

---

#### Crítico Contrato: `registrarAjusteDeCuentaCorriente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarAjusteDeCuentaCorriente(cuentaId identificador, tipo cadena, importe moneda, motivo cadena)` |
| **Responsabilidades** | Corregir el saldo de una cuenta corriente con una nota de crédito o de débito. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-237. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Una nota de crédito reduce lo que el cliente debe —una devolución, un descuento— y se imputa como un pago contra los cargos más antiguos; una nota de débito lo aumenta, por ejemplo un recargo por mora. El importe es siempre positivo y el tipo dice el sentido. No toca ninguna caja. Es la única forma de corregir un asiento, porque el libro no se edita. |
| **Excepciones** | Si la cuenta no existe o es de otra distribuidora → recurso no encontrado. Si el tipo no es crédito ni débito → error de solicitud. Si el importe no es mayor que cero o falta el motivo → error de solicitud. |
| **Salida** | El asiento del ajuste. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La CuentaCorriente pertenece a su Distribuidora y no está cerrada. |
| **Postcondiciones** | Se creó una instancia de AsientoCuentaCorriente de tipo «nota de crédito» o «nota de débito», por el importe indicado y con el motivo. Si es una nota de crédito, se creó una instancia de ImputacionCuentaCorriente por cada cargo cubierto. El atributo saldo de la CuentaCorriente quedó actualizado según el tipo. |

---

#### Crítico Contrato: `registrarPagoDeCuentaCorriente()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarPagoDeCuentaCorriente(cuentaId identificador, importe moneda, medio cadena, cajaId identificador)` |
| **Responsabilidades** | Registrar un cobro de un cliente a cuenta corriente, ingresarlo a una caja y aplicarlo a las deudas más antiguas. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-237. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Si el cobro lo registra el administrador, entra a la caja indicada: el asiento de pago y el movimiento de caja se registran en la misma transacción, por el libro de movimientos (CU-228). Si lo cobra el chofer en la calle, el parámetro de caja va vacío, no entra a ninguna caja y el asiento queda vinculado a la rendición abierta del chofer: la plata llega a la caja cuando el administrador aprueba esa rendición (CU-233), que es la única puerta del dinero que anda por la calle. El pago se imputa en orden de antigüedad contra los cargos impagos, con lo que la antigüedad de la deuda y los comprobantes pendientes se mantienen al día. Un pago que excede la deuda queda como saldo a favor. Lleva clave de idempotencia. |
| **Excepciones** | Si la cuenta no existe o es de otra distribuidora → recurso no encontrado. Si el importe no es mayor que cero → error de solicitud. Si lo registra el administrador y no indica caja, o la caja exige sesión y no la tiene abierta → conflicto. Si lo registra un chofer e indica caja → error de solicitud. Si lo registra un chofer sin rendición abierta → conflicto. |
| **Salida** | El asiento de pago. |
| **Precondiciones** | El solicitante es Administrador o Chofer. La CuentaCorriente pertenece a la Distribuidora y no está cerrada. Si el cobro lo registra el administrador, la Caja pertenece a su Distribuidora. |
| **Postcondiciones** | Se creó una instancia de AsientoCuentaCorriente de tipo «pago» por el importe cobrado y, por cada cargo impago cubierto, una instancia de ImputacionCuentaCorriente. Si el cobro entró a una caja, se creó una instancia de MovimientoDeCaja de ingreso, asociada al asiento; si lo cobró un chofer, el asiento quedó asociado a su RendicionChofer abierta y el atributo efectivo esperado de la rendición aumentó en el importe. El atributo saldo de la CuentaCorriente disminuyó en el importe. |

---

#### Importante Contrato: `crearReglaDeComision()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `crearReglaDeComision(empleadoId identificador, productoId identificador, base cadena, valor decimal, vigenteDesde fecha)` |
| **Responsabilidades** | Definir cuánto gana un empleado que reparte por entrega —por unidad, por pedido o como porcentaje del total—, para un empleado, para un producto o para todos. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-240. Funciones: IRQ-19, OBJ-05. |
| **Notas** | La regla más específica gana: chofer y producto, después chofer, después producto y por último la general. Para un mismo alcance no puede haber dos reglas vigentes que se solapen en el tiempo (restricción de exclusión sobre el rango de fechas). La regla rige para las entregas posteriores a su fecha de vigencia: las comisiones ya devengadas conservan una copia de la regla con que se calcularon. El valor es un monto por unidad o por pedido, o un porcentaje, según la base. |
| **Excepciones** | Si el empleado o el producto no existen o son de otra distribuidora → recurso no encontrado. Si la regla se solapa con otra vigente del mismo alcance → conflicto. Si la base no es una de las tres o el valor es negativo → error de solicitud. Si el porcentaje supera 100 → error de solicitud. |
| **Salida** | La regla creada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General, con una Distribuidora en contexto. Si se indica un Empleado o un Producto, pertenecen a la Distribuidora. |
| **Postcondiciones** | Se creó una instancia de ReglaComision, asociada a la Distribuidora y, si se indicaron, al Empleado y al Producto, con la base, el valor y la fecha de vigencia indicados, activa. |

---

#### Importante Contrato: `modificarReglaDeComision()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `modificarReglaDeComision(reglaId identificador, datos registro)` |
| **Responsabilidades** | Cambiar el valor, la vigencia o el estado de una regla de comisión. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-240. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Una regla que ya devengó comisiones no cambia lo devengado: cada asiento guarda una copia de la regla con que se calculó. Para cambiar el valor hacia adelante conviene cerrar la regla vigente y crear otra. |
| **Excepciones** | Si la regla no existe o es de otra distribuidora → recurso no encontrado. Si el cambio la solapa con otra del mismo alcance → conflicto. Si el valor es negativo o la vigencia no es válida → error de solicitud. |
| **Salida** | La regla con los datos nuevos. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La ReglaComision pertenece a su Distribuidora. |
| **Postcondiciones** | Los atributos valor, vigente hasta y activa de la instancia de ReglaComision tomaron los valores indicados. |

---

#### Importante · automático Contrato: `registrarComisionDeEntrega()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `registrarComisionDeEntrega(pedidoId identificador)` |
| **Responsabilidades** | Calcular y asentar la comisión que gana el chofer por una entrega, con la regla vigente en el momento de entregar. |
| **Tipo** | Sistema (proceso automático) (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-241. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Lo dispara el evento «pedido entregado», y el proceso de conciliación nocturno genera las que falten. Es idempotente: un pedido devenga una sola comisión. El asiento guarda una copia de la regla con que se calculó, de modo que un cambio posterior de la regla no altera lo devengado. Si no hay una regla aplicable, no se devenga nada y queda constancia. |
| **Excepciones** | Si el pedido no tiene chofer → se ignora. Si el pedido ya devengó su comisión → termina sin hacer nada. Si no hay regla vigente aplicable → no se asienta nada y se deja constancia. |
| **Salida** | Ninguna: es un proceso interno. |
| **Precondiciones** | Existe un Pedido entregado por un Chofer cuyo Empleado tiene una ReglaComision aplicable a la fecha de entrega, y el pedido todavía no devengó comisión. |
| **Postcondiciones** | Se creó una instancia de AsientoComision de tipo «comisión por entrega», asociada al Empleado del chofer, al Pedido y a la ReglaComision, con el importe que da la regla y una copia de ella. |

---

#### Importante Contrato: `anularLiquidacion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `anularLiquidacion(liquidacionId identificador)` |
| **Responsabilidades** | Anular una liquidación que todavía no se pagó y liberar sus asientos para que entren en otra. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-242. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Sólo se anula un borrador o una liquidación aprobada: una pagada ya movió plata y se corrige anulando su movimiento de caja (CU-229). |
| **Excepciones** | Si la liquidación no existe o es de otra distribuidora → recurso no encontrado. Si está pagada o ya anulada → conflicto. |
| **Salida** | La liquidación anulada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La LiquidacionComisiones pertenece a su Distribuidora y no está pagada ni anulada. |
| **Postcondiciones** | El atributo estado de la instancia de LiquidacionComisiones pasó a «anulada». Cada AsientoComision que incluía quedó libre de liquidación. |

---

#### Importante Contrato: `aprobarLiquidacion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `aprobarLiquidacion(liquidacionId identificador)` |
| **Responsabilidades** | Aprobar el borrador de una liquidación y congelarlo, o cerrarlo sin pago si el neto no es positivo. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-242. Funciones: IRQ-19, OBJ-05. |
| **Notas** | Una liquidación aprobada no admite cambios en sus asientos: lo que se devengue después va a la liquidación siguiente. Si el neto es cero, la liquidación se cierra sin pago. Si el neto es negativo, también se cierra sin pago y se crea un asiento de arrastre —un saldo deudor del empleado— que entra en la liquidación siguiente. |
| **Excepciones** | Si la liquidación no existe o es de otra distribuidora → recurso no encontrado. Si no está en borrador → conflicto. |
| **Salida** | La liquidación aprobada o cerrada. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La LiquidacionComisiones pertenece a su Distribuidora y está en borrador. |
| **Postcondiciones** | Si el neto es mayor que cero, el atributo estado de la instancia de LiquidacionComisiones pasó a «aprobada»; si no, pasó a «cerrada» sin pago. El atributo aprobada el tomó el momento de la decisión. Si el neto es negativo, se creó una instancia de AsientoComision de arrastre por el saldo deudor, asociada al Empleado. |

---

#### Importante Contrato: `liquidarComisionesDelChofer()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `liquidarComisionesDelChofer(empleadoId identificador, fechaDesde fecha, fechaHasta fecha)` |
| **Responsabilidades** | Reunir en una liquidación las comisiones y las deducciones de un empleado que reparte en un período, para aprobarla y pagarla. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-242. Funciones: IRQ-19, OBJ-05. |
| **Notas** | La liquidación toma, bajo bloqueo, los asientos del empleado en el período que no pertenecen a otra liquidación y los asigna a la nueva. Las deducciones —faltantes de rendición, multas imputadas y el arrastre de un período negativo anterior— son asientos negativos y restan. El bruto es la suma de las comisiones, las deducciones suman aparte y el neto es la diferencia. Nace como borrador y no mueve plata hasta pagarse. |
| **Excepciones** | Si el empleado no existe o es de otra distribuidora → recurso no encontrado. Si el período no es válido (desde posterior a hasta) → error de solicitud. Si no hay asientos para liquidar → conflicto. |
| **Salida** | La liquidación en borrador, con sus asientos. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. El Empleado pertenece a su Distribuidora y tiene asientos sin liquidar en el período. |
| **Postcondiciones** | Se creó una instancia de LiquidacionComisiones en estado «borrador», asociada al Empleado, con el período indicado y el bruto, las deducciones y el neto calculados. Cada AsientoComision sin liquidar del período quedó asociado a la nueva LiquidacionComisiones. |

---

#### Importante Contrato: `pagarLiquidacion()`

| Campo | Detalle |
|-------|---------|
| **Nombre** | `pagarLiquidacion(liquidacionId identificador, cajaId identificador)` |
| **Responsabilidades** | Pagar una liquidación aprobada: sacar el neto de una caja y dejar la liquidación pagada. |
| **Tipo** | Sistema (planificado, I-14) |
| **Referencias cruzadas** | Casos de uso: CU-243. Funciones: IRQ-19, OBJ-05. |
| **Notas** | El pago es un egreso de la caja con la categoría de sistema «pago de comisiones», por el libro de movimientos (CU-228). Una liquidación se paga una sola vez. Una liquidación con neto cero o negativo no llega acá: se cierra al aprobarla. |
| **Excepciones** | Si la liquidación o la caja no existen o son de otra distribuidora → recurso no encontrado. Si la liquidación no está aprobada → conflicto. Si la caja es de efectivo y su saldo no alcanza, o exige sesión y no la tiene abierta → conflicto. |
| **Salida** | La liquidación pagada, con su movimiento de caja. |
| **Precondiciones** | El solicitante es Administrador o Administrador General. La LiquidacionComisiones pertenece a su Distribuidora y está aprobada. La Caja pertenece a la Distribuidora y está activa. |
| **Postcondiciones** | El atributo estado de la instancia de LiquidacionComisiones pasó a «pagada» y el atributo pagada el tomó el momento del pago. Se creó una instancia de MovimientoDeCaja de egreso por el neto, asociada a la liquidación. |

---

## 3. Módulos Inteligentes del Sistema

Se denomina **módulo inteligente** al proceso que el sistema dispara y ejecuta por
iniciativa propia, sin que ningún empleado de la distribuidora lo solicite, y que
agrega valor económico al negocio —genera ingresos o reduce costos— más allá de lo
que el producto mínimo viable necesita para funcionar.

El criterio de selección excluye deliberadamente dos categorías: los automatismos
que son parte intrínseca del funcionamiento del sistema (descontar stock, emitir una
notificación, aplicar un descuento configurado) y los que se resuelven con una única
consulta a la base de datos. Ninguno de los dos constituye inteligencia: el primero
es una obligación funcional y el segundo, una sentencia `SELECT`.

### 3.1 Los cinco procesos automatizados

| # | Denominación | Disparador | Naturaleza del proceso | Aporte |
|---|--------------|-----------|------------------------|--------|
| **M1** | **Negociación secuencial de asignación de pedidos** | Alta de un pedido, y proceso temporal de revisión periódica | Ofrece el pedido a un chofer por vez con vigencia acotada; ante rechazo o vencimiento pasa al siguiente candidato y amplía el radio de búsqueda de forma progresiva. | Opera el presente |
| **M2** | **Planificación predictiva de mantenimiento y habilitaciones de flota** | Proceso temporal diario sobre el recorrido GPS acumulado | Estima el consumo diario de kilómetros por vehículo, proyecta vencimientos por kilometraje y por fecha, y negocia secuencialmente las ventanas de taller de menor impacto operativo. | Protege el activo vehículo — **costos** |
| **M3** | **Anticipación de recompra por consumo estimado** | Proceso temporal diario sobre el historial de compras | Estima el ritmo de consumo de cada cliente, proyecta la fecha de agotamiento del gas y emite una invitación a reponer con el pedido precargado y vigencia limitada. | Genera demanda — **ingresos** |
| **M4** | **Agrupación inteligente de pedidos por recorrido** | Proceso temporal sobre los pedidos pendientes y programados | Arma lotes de pedidos compatibles por zona, franja horaria y capacidad de carga, y los ofrece al chofer como un recorrido único ordenado por secuencia de entrega. | Reduce el costo por entrega — **costos** |
| **M5** | **Recuperación de envases no devueltos** | Proceso temporal sobre el ciclo de vida del envase | Detecta envases retenidos más allá del plazo previsto y ejecuta una secuencia escalonada de gestión, escalando al administrador el caso que no se resuelve. | Protege el activo envase — **costos** |

Un módulo orientado a ingresos, tres a la reducción de costos y uno a la operación
del presente.

### 3.2 Correspondencia con los casos de uso

Cada proceso automatizado está especificado como caso de uso, con sus cuatro artefactos:
descripción de alto nivel, especificación expandida, diagrama de secuencia del sistema y
diagrama de interacción de diseño.

| Módulo | Casos de uso | Estado |
|---|---|---|
| **M1** | CU-013, CU-014, CU-015, CU-016 | Implementado |
| **M2** | CU-105 | Planificado (I-10); tablas en la base, servicio sin construir |
| **M3** | CU-106 | Planificado (I-6); tablas en la base, servicio sin construir |
| **M4** | CU-107 | Planificado (I-9); tablas en la base, servicio sin construir |
| **M5** | CU-108 | Planificado (I-8); tablas en la base, servicio sin construir |

### 3.3 Intervención humana

Los cinco procesos se disparan y se ejecutan sin intervención de ningún empleado.
Donde aparece una persona es únicamente en las decisiones que comprometen dinero,
que el sistema prepara pero no ejecuta por sí mismo.

| Módulo | Ejecución | Decisión reservada a una persona |
|--------|-----------|----------------------------------|
| M1 — Negociación de asignación | Autónoma | Ninguna de gestión; el chofer es el destinatario de la oferta |
| M2 — Flota predictiva | Autónoma | El administrador confirma el gasto del taller |
| M3 — Recompra | Autónoma | Ninguna de gestión; el cliente es el destinatario |
| M4 — Agrupación por recorrido | Autónoma | Ninguna de gestión; el chofer acepta o rechaza el lote |
| M5 — Recuperación de envases | Autónoma | El administrador decide el cobro del depósito o la baja del envase |

### 3.4 Parámetros de configuración

Cada módulo es parametrizable por distribuidora. Como mínimo se configura la
frecuencia de ejecución del proceso y la vigencia de las ofertas que emite.

| Módulo | Parámetros configurables |
|--------|--------------------------|
| M1 | Pasos de radio de búsqueda, duración de la ventana de aceptación, frecuencia de revisión de ofertas vencidas |
| M2 | Anticipación por tipo de mantenimiento y de habilitación, mínimo de vehículos activos por zona, vigencia de la propuesta de taller |
| M3 | Anticipación sobre la fecha proyectada de agotamiento, vigencia de la invitación, intervalo mínimo entre invitaciones a un mismo cliente |
| M4 | Tamaño máximo de lote, radio de agrupación, tolerancia de franja horaria, frecuencia de evaluación |
| M5 | Plazo de tolerancia de devolución, plazos de cada escalón de la secuencia, umbral de importe para escalar al administrador |

### 3.5 Estado de implementación

| Módulo | Estado | Ubicación en el código |
|--------|--------|------------------------|
| M1 | **Implementado** | `DispatchOrchestratorService`, `DispatchService` |
| M2 | Planificado (I-10): Análisis y Diseño especificados | Documento 3 §6.2 |
| M3 | Planificado (I-6): Análisis y Diseño especificados | — |
| M4 | Planificado (I-9): Análisis y Diseño especificados | — |
| M5 | Planificado (I-8): Análisis y Diseño especificados | — |

### 3.6 Valores vigentes del módulo M1

Los siguientes valores son los que el sistema aplica. Se registran aquí porque
los diagramas de secuencia de la sección 2 y los contratos de operación los
referencian.

| Parámetro | Valor vigente | Constante en el código |
|-----------|---------------|------------------------|
| Pasos de radio de búsqueda | 5, 10, 15 y 20 km | `DispatchOrchestratorService.RADIUS_STEPS_KM` |
| Vigencia de la oferta al chofer | 30 segundos | `DispatchOrchestratorService.OFFER_TTL_SECONDS` |
| Frecuencia de revisión de ofertas vencidas | cada 15 segundos | `@Cron('*/15 * * * * *')` en `dispatch.service.ts` |
| Revisión de reservas de stock | cada 5 minutos, cada 30 minutos y cada hora | `@Cron` en `reservation.service.ts` |

> Los dos primeros parámetros son constantes de clase. Llevarlos a
> configuración por distribuidora es el caso de uso CU-171 (planificado, I-1).

> Esta sección se desarrolla con mayor detalle en el **Doc 3 — Diseño**, donde cada
> módulo inteligente tiene su especificación, su diagrama de interacción y su
> diagrama de clases asociado.

---

## 4. Glosario

| Término | Categoría | Definición |
|---------|-----------|------------|
| **SPLG** | Acrónimo | Sistema de Pedidos y Logística de Garrafas de Gas. Nombre formal del proyecto. |
| **UP** | Metodología | Unified Process. Proceso de desarrollo iterativo e incremental adoptado por la cátedra. |
| **CU** | Artefacto UML | Caso de Uso. Descripción de una secuencia de interacciones entre un actor y el sistema para alcanzar un objetivo. |
| **Actor** | Concepto UML | Entidad externa al sistema (humano o automático) que interactúa con él para cumplir un objetivo. |
| **DSS** | Artefacto UML | Diagrama de Secuencia a nivel de Sistema. Modelo del sistema como caja negra que muestra solo los mensajes entre actor y sistema. |
| **Contrato de Operación** | Artefacto UP | Especificación formal de una operación del sistema con responsabilidades, precondiciones, postcondiciones y excepciones. |
| **Modelo Conceptual** | Artefacto UML | Diagrama de clases del dominio del problema, sin métodos, que muestra los conceptos relevantes y sus relaciones. |
| **Concepto Idóneo** | Concepto UP | Concepto del dominio que se incluye finalmente en el Modelo Conceptual por ser relevante para los CUs. |
| **Token de identidad** | Tecnología | Credencial que emite Firebase Authentication al verificar al usuario. Es la única credencial de sesión del sistema: el backend la valida contra Firebase en cada solicitud y resuelve el rol contra la base. |

| **GEORADIUS** | Tecnología | Comando de Redis que retorna miembros de un Sorted Set GEO ordenados por distancia desde un punto. |
| **GEOADD** | Tecnología | Comando de Redis que agrega un miembro con sus coordenadas geográficas a un Sorted Set GEO. |
| **WebSocket** | Tecnología | Protocolo bidireccional de comunicación en tiempo real entre cliente y servidor sobre TCP. |
| **Socket.IO** | Tecnología | Librería sobre WebSocket que agrega reconexión automática, salas y fallback HTTP polling. |
| **FCM** | Tecnología | Firebase Cloud Messaging. Servicio de Google para envío de push notifications a dispositivos Android, iOS y Web. |
| **QueryRunner** | Tecnología | API de TypeORM para ejecutar transacciones manuales sobre PostgreSQL. |
| **SELECT FOR UPDATE** | Tecnología | Sentencia SQL que adquiere un lock pesimista sobre las filas seleccionadas hasta que termina la transacción. |
| **Stock fantasma** | Concepto | Stock comprometido en una transacción no finalizada que bloquea la disponibilidad real para otros pedidos. Se previene con rollback automático. |
| **Cron** | Concepto | Tarea programada que se ejecuta a intervalos regulares. En el sistema se usan cuatro: revisión de ofertas vencidas cada 15 segundos (`@Cron('*/15 * * * * *')`) y revisión de reservas de stock cada 5 minutos, cada 30 minutos y cada hora. |
| **JSONB** | Tecnología | Tipo de columna PostgreSQL para almacenar JSON binario indexable. Usado para `GasCylinder.promotions`. |
| **Soft-delete** | Concepto | Eliminación lógica que marca un registro como inactivo (`deletedAt`) sin borrarlo físicamente. |
| **Geohash** | Concepto | Codificación geográfica de coordenadas en strings cortos. Redis lo usa internamente para indexar posiciones. |
| **Pedido PENDING** | Estado | Pedido recién creado, sin chofer asignado. Esperando despacho automático o manual. |
| **Pedido ACCEPTED** | Estado | Pedido tomado por un chofer pero aún no en camino. |
| **Pedido ON_THE_WAY** | Estado | Pedido en tránsito. El chofer marca el inicio del envío. |
| **Pedido DELIVERED** | Estado | Pedido entregado. Cierra el ciclo de la transacción. |
| **Pedido CANCELLED** | Estado | Pedido cancelado por cliente, chofer o administrador. Restituye stock si correspondía. |
| **MVP** | Concepto | Minimum Viable Product. Versión mínima del sistema con las funcionalidades críticas del negocio. |
| **MVVM** | Patrón | Model-View-ViewModel. Arquitectura usada en las apps Flutter (Stacked) y Panel React. |
| **Stacked** | Tecnología | Framework MVVM para Flutter usado en las dos apps móviles del proyecto. |
| **NestJS** | Tecnología | Framework Node.js para construir APIs REST y WebSocket con TypeScript. Backend del sistema. |
| **TypeORM** | Tecnología | ORM de TypeScript usado para mapear las entities del dominio a tablas PostgreSQL. |
| **Despacho automático** | Concepto | Proceso por el cual el sistema ofrece un pedido a un chofer por vez, con vigencia acotada, usando GEORADIUS para ordenar los candidatos por cercanía. Corresponde al módulo inteligente M1. |
| **Radio expandido** | Concepto | Estrategia del proceso de negociación que amplía progresivamente el radio de búsqueda de choferes (5 → 10 → 15 → 20 km) a medida que se agotan los candidatos de cada paso. |
| **Promoción por volumen** | Concepto | Descuento aplicado automáticamente cuando la cantidad de un producto en el carrito alcanza un mínimo. |
| **Recargo por pago en línea** | Concepto | Aumento del 10 % al total cuando el método de pago es MERCADOPAGO o TRANSFER, que el servidor aplica automáticamente al calcular el pedido; el efectivo no lleva recargo. |
| **Validación de chofer** | Concepto | Habilitación permanente de un chofer por parte del administrador (`Delivery.validated = true`). Distinta de la disponibilidad operativa (`isActive`). |
| **Ventana de aceptación** | Concepto | Lapso durante el cual una oferta de pedido permanece vigente para el chofer al que se le ofreció. Vencida sin respuesta, el pedido pasa al siguiente candidato. |
| **Oferta de despacho** | Concepto | Propuesta de un pedido a un chofer determinado, con vigencia limitada. Se materializa en la entidad `DispatchOffer`. |
| **Distribuidora** | Concepto | Empresa comercializadora de garrafas que opera dentro del sistema. Es la unidad de aislamiento multi-tenant: cada distribuidora ve y gestiona únicamente sus propios datos. |
| **Multi-tenant** | Concepto | Arquitectura en la que una única instancia del sistema atiende a varias distribuidoras manteniendo sus datos aislados entre sí. |
| **Zona de cobertura** | Concepto | Área geográfica dentro de la cual una distribuidora acepta pedidos y planifica sus recorridos. |
| **Ciclo de envase** | Concepto | Recorrido de una garrafa física entre la distribuidora y los clientes: entrega, permanencia en poder del cliente y devolución. Se registra en `CylinderMovement`. |
| **Depósito de envase** | Concepto | Importe que el cliente deja en garantía por el envase que recibe y que se le restituye al devolverlo. |
| **Módulo inteligente** | Concepto UP | Proceso que el sistema dispara y ejecuta por iniciativa propia, con valor económico para el negocio, que excede lo que el producto mínimo viable necesita para funcionar y no se resuelve con una única consulta a la base de datos. |
| **RTO** | Normativa | Revisión Técnica Obligatoria. Verificación periódica de la aptitud de los vehículos exigida en la provincia de Misiones. |
| **FCEQyN – UNaM** | Institución | Facultad de Ciencias Exactas, Químicas y Naturales — Universidad Nacional de Misiones. Institución académica del proyecto. |
