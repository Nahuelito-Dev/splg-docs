# Estado de los 151 casos de uso

Cruce entre el catálogo de casos de uso, el mapeo caso↔endpoint de la auditoría de
cobertura, y la batería ejecutada contra la API corriendo con los cuatro roles reales
y los 50 cuerpos de petición escritos a mano.

Los casos que no tenían endpoint propio, o que necesitaban una condición previa
(un pedido entregado, un envase cargado, una distribuidora que se pueda dar de baja),
se verificaron creando esa condición y mirando el efecto en la base.

| Veredicto | Qué quiere decir | Qué hacer |
|---|---|---|
| **ANDA** | Verificado contra la API corriendo | Nada |
| **ARREGLAR** | Alguno de sus endpoints devuelve 500 | Corregir |
| **PARCIAL** | Una parte responde y otra no | Completar |
| **NO SE PUEDE PROBAR** | El entorno no lo permite | Habilitar el entorno |
| **COMPLETAR** | El sistema resuelve sólo una parte | Terminar |
| **PROGRAMAR DESDE CERO** | Especificado, sin código | Construir |
| **MÓDULO INTELIGENTE PENDIENTE** | Los cuatro de la tesis, diseñados y sin construir | Construir |

## Resumen

| Veredicto | Casos |
|---|---:|
| NO SE PUEDE PROBAR | 2 |
| COMPLETAR | 1 |
| MÓDULO INTELIGENTE PENDIENTE | 4 |
| PROGRAMAR DESDE CERO | 28 |
| ANDA | 116 |
| **Total** | **151** |

**116 de los 151 andan y están verificados contra la API corriendo.** 32 hay que programarlos desde cero, de los cuales 4 son los módulos inteligentes de la tesis.

Los dos últimos (CU-150 y CU-151) se especificaron el 23/09 a partir del análisis del backend de Tutu: la vigencia temporal de una zona de cobertura, que hoy hay que apagar a mano. Ver `TUTU-QUE-SIRVE.md`.

## NO SE PUEDE PROBAR — 2 casos

| CU | Título | Qué se vio |
|---|---|---|
| CU-013 | Ofrecer el Pedido al Chofer Más Cercano | `el orquestador busca choferes conectados por WebSocket y no hay ninguno en linea (H-20)` → verificado a mano |
| CU-047 | Recuperar Contraseña | `responde 400 — {"message":"Too many password_reset attempts. Please try again later.","error":"Bad Reques` → verificado a mano |

## COMPLETAR — 1 casos

| CU | Título | Qué se vio |
|---|---|---|
| CU-040 | Activar / Desactivar Producto | `DELETE /gascylinder/:id` → anda |

## MÓDULO INTELIGENTE PENDIENTE — 4 casos

| CU | Título | Qué se vio |
|---|---|---|
| CU-105 | Planificar el mantenimiento y las habilitaciones de la flo | sin endpoint HTTP asociado |
| CU-106 | Anticipar la recompra por consumo estimado | sin endpoint HTTP asociado |
| CU-107 | Agrupar pedidos por recorrido | sin endpoint HTTP asociado |
| CU-108 | Recuperar envases no devueltos | sin endpoint HTTP asociado |

## PROGRAMAR DESDE CERO — 26 casos

| CU | Título | Qué se vio |
|---|---|---|
| CU-043 | Modificar Capacidad de Franja Horaria | sin endpoint HTTP asociado |
| CU-122 | Agregar Ítem al Carrito | sin endpoint HTTP asociado |
| CU-123 | Modificar la Cantidad de un Ítem del Carrito | sin endpoint HTTP asociado |
| CU-124 | Quitar Ítem del Carrito | sin endpoint HTTP asociado |
| CU-125 | Consultar el Carrito | sin endpoint HTTP asociado |
| CU-126 | Vaciar el Carrito | sin endpoint HTTP asociado |
| CU-127 | Cambiar la Dirección de Entrega del Pedido | sin endpoint HTTP asociado |
| CU-128 | Indicar Quién Recibe el Pedido | sin endpoint HTTP asociado |
| CU-132 | Registrar la Revisión Periódica de un Envase | sin endpoint HTTP asociado |
| CU-133 | Consultar la Vigencia de un Envase | sin endpoint HTTP asociado |
| CU-134 | Consultar los Envases Próximos a Vencer | sin endpoint HTTP asociado |
| CU-135 | Bloquear el Despacho de un Envase Vencido | sin endpoint HTTP asociado |
| CU-136 | Registrar el Seguro del Vehículo | sin endpoint HTTP asociado |
| CU-137 | Registrar la Verificación Técnica Vehicular | sin endpoint HTTP asociado |
| CU-138 | Registrar la Licencia de Conducir del Chofer | sin endpoint HTTP asociado |
| CU-139 | Consultar los Vencimientos de la Flota | sin endpoint HTTP asociado |
| CU-140 | Programar un Mantenimiento de Vehículo | sin endpoint HTTP asociado |
| CU-141 | Registrar un Mantenimiento Realizado | sin endpoint HTTP asociado |
| CU-142 | Avisar los Vencimientos Próximos de la Flota | sin endpoint HTTP asociado |
| CU-143 | Declarar el Consumo Promedio al Registrarse | sin endpoint HTTP asociado |
| CU-144 | Actualizar el Consumo Promedio Declarado | sin endpoint HTTP asociado |
| CU-145 | Configurar los Días de Aviso Previo a la Recompra | sin endpoint HTTP asociado |
| CU-146 | Consultar la Fecha Estimada de Recompra | sin endpoint HTTP asociado |
| CU-147 | Realizar una Compra Express | sin endpoint HTTP asociado |
| CU-148 | Elegir la Modalidad de Entrega del Pedido | sin endpoint HTTP asociado |
| CU-149 | Despachar un Pedido Express a un Chofer en Moto |
| CU-150 | Programar la Vigencia de una Zona de Cobertura |
| CU-151 | Desactivar las Zonas de Cobertura Vencidas | sin endpoint HTTP asociado |

## ANDA — 116 casos

| CU | Título | Qué se vio |
|---|---|---|
| CU-001 | Iniciar Sesión | `POST /auth/login` → anda; `POST /auth/login/dashboard` → anda |
| CU-002 | Registrarse como Cliente | `POST /users/customer-registration` → anda |
| CU-003 | Registrar Chofer *(ver CU-031)* | `POST /users/delivery-registration` → anda |
| CU-004 | Gestionar Perfil de Usuario | `GET /users/:id` → anda; `PATCH /users/:id` → anda |
| CU-005 | Crear Pedido | `POST /orders` → anda |
| CU-006 | Consultar Detalle de Pedido | `GET /orders/:id` → anda |
| CU-007 | Consultar Historial de Pedidos | `GET /orders/customer/:customerId` → anda |
| CU-008 | Cancelar Pedido (Cliente) | `PATCH /orders/:id/cancel` → anda |
| CU-009 | Cancelar Pedido (Chofer) | `PATCH /orders/{id}/cancel como chofer: libera el pedido a pending (ver H-33)` → verificado a mano |
| CU-010 | Cancelar Pedido (Administrador) | `DELETE /orders/:id` → anda |
| CU-011 | Listar Todos los Pedidos | `GET /orders` → anda |
| CU-012 | Asignar Chofer Manualmente | `PATCH /orders/:id/assign/:deliveryId` → anda |
| CU-014 | Vencer la Oferta y Ofrecer al Siguiente Chofer | `CRON */15 * * * * *` → no aplica |
| CU-015 | Aceptar Pedido | `200: el pedido queda en 'accepted'` → verificado a mano |
| CU-016 | Rechazar / Ignorar Pedido | `POST /orders/:id/reject` → anda |
| CU-017 | Actualizar Ubicación GPS del Chofer | `PATCH /orders/:id/location` → anda; `WS driver:update-location` → no aplica; `PATCH /delivery/:id/location` → anda |
| CU-018 | Marcar Pedido "En Camino" | `PATCH /orders/{id}/status como chofer: el pedido pasa a on_the_way` → verificado a mano |
| CU-019 | Avisar Llegada al Cliente | `PATCH /orders/:id/arrived` → anda |
| CU-020 | Confirmar Entrega | `delivery-code + confirm-delivery: el pedido queda delivered` → verificado a mano |
| CU-021 | Recibir Notificaciones en Tiempo Real | `WS driver:join` → no aplica; `WS customer:join` → no aplica |
| CU-022 | Activar / Desactivar Disponibilidad (Chofer) | `PATCH /delivery/user/:userId/availability` → anda |
| CU-023 | Registrar Reclamo | `POST /claims` → anda |
| CU-024 | Listar Reclamos | `GET /claims` → anda |
| CU-025 | Resolver Reclamo | `PATCH /claims/:id/resolve` → anda |
| CU-026 | Ver Dashboard General | `GET /orders/stats/summary` → anda |
| CU-027 | Ver Reporte de Ventas por Chofer | `GET /reports/sales-by-driver` → anda |
| CU-028 | Ver Reporte de Ventas por Producto | `GET /reports/sales-by-product` → anda |
| CU-029 | Ver Reporte por Método de Pago | `GET /reports/sales-by-payment` → anda |
| CU-030 | Ver Gráfico de Ventas (últimos 7 días) | `GET /orders/stats/chart` → anda; `GET /reports/sales-evolution` → anda |
| CU-031 | Registrar Chofer | `POST /users/delivery-registration: 201 y queda la fila en delivery` → verificado a mano |
| CU-032 | Validar / Invalidar Chofer | `PATCH /delivery/:id/validate` → anda; `PATCH /delivery/:id/invalidate` → anda |
| CU-033 | Activar / Desactivar Chofer (Admin) | `PATCH /delivery/:id/status` → anda |
| CU-034 | Registrar Vehículo del Chofer | `POST /car` → anda |
| CU-035 | Consultar Listado de Choferes | `GET /delivery` → anda; `GET /delivery/active` → anda |
| CU-036 | Crear Producto (Garrafa) | `POST /gascylinder` → anda |
| CU-037 | Actualizar Precio de Producto | `PATCH /gascylinder/:id` → anda |
| CU-038 | Actualizar Stock de Producto | `PATCH /gascylinder/:id/stock` → anda |
| CU-039 | Configurar Promociones por Cantidad | `POST /gascylinder con promotions: la promocion se guarda en la base` → verificado a mano |
| CU-041 | Consultar Catálogo de Productos | `GET /gascylinder` → anda; `GET /gascylinder/:id` → anda; `GET /gascylinder/type/:type` → anda |
| CU-042 | Crear Franja Horaria | `POST /time-slot` → anda |
| CU-044 | Seleccionar Franja Horaria al Crear Pedido | `POST /orders con timeSlotId: el pedido queda con su franja` → verificado a mano |
| CU-045 | Consultar Franjas Horarias Disponibles | `GET /time-slot/availability` → anda |
| CU-046 | Consultar Direcciones de Entrega del Cliente | `GET /user-address/user/:userId` → anda |
| CU-048 | Procesar Pago con MercadoPago | `el webhook responde 200 sin token (es publico y debe ser idempotente) — {"received":true}` → verificado a mano |
| CU-049 | Consultar Balance / Ganancias del Chofer | `PATCH /delivery/:id/balance` → anda |
| CU-050 | Bloquear / Desbloquear Usuario | `PATCH /users/:id/block` → anda |
| CU-051 | Consultar Listado de Vehículos | `GET /car` → anda |
| CU-052 | Registrar Distribuidora | `POST /distributor` → anda |
| CU-053 | Consultar Distribuidoras | `GET /distributor` → anda; `GET /distributor/:id` → anda |
| CU-054 | Modificar Datos de la Distribuidora | `PATCH /distributor/:id` → anda |
| CU-055 | Dar de Baja una Distribuidora | `alta=201, baja=200, queda 'dada de baja'` → verificado a mano |
| CU-056 | Definir Zona de Cobertura | `POST /coverage-zones` → anda |
| CU-057 | Consultar Zonas de Cobertura | `GET /coverage-zones` → anda |
| CU-058 | Validar Cobertura de una Dirección | `GET /coverage-zones/check` → anda |
| CU-059 | Eliminar Zona de Cobertura | `DELETE /coverage-zones/:id` → anda |
| CU-060 | Registrar Incidencia de Entrega | `POST /incidents` → anda |
| CU-061 | Listar Incidencias | `GET /incidents` → anda |
| CU-062 | Consultar Incidencias de un Pedido | `GET /incidents/order/:orderId` → anda |
| CU-063 | Resolver Incidencia | `PATCH /incidents/:id/resolve` → anda |
| CU-064 | Calificar Pedido (cliente↔chofer) | `pedido delivered, calificar=201, calificaciones guardadas=1 — {"rating_id":"9b491d9b-4796-4871-8e10-7ee16b312e6c","order_id":"2080ea` → verificado a mano |
| CU-065 | Consultar Promedio de Calificaciones de un Usuario | `GET /ratings/user/:userId/summary` → anda |
| CU-066 | Consultar Historial de Calificaciones Recibidas | `GET /ratings/user/:userId` → anda |
| CU-067 | Dar de Alta un Envase Físico | `POST /cylinders` → anda |
| CU-068 | Asignar Envases a un Pedido | `transicion a filled=200, asignar=201, el envase queda en 'dispatched' — [{"cylinder_id":"20f834c1-aca5-44e7-a4fa-0f887e18e64b","distributor_id` → verificado a mano |
| CU-069 | Consultar el Parque de Envases | `GET /cylinders` → anda; `GET /cylinders/:id` → anda |
| CU-070 | Registrar Movimiento de Envase (cambio de estado) | `PATCH /cylinders/:id/transition` → anda |
| CU-071 | Consultar Historial de Movimientos de un Envase | `GET /cylinders/:id/history` → anda |
| CU-072 | Crear Reserva Programada con Seña | `POST /orders con isReservation y depositAmount: queda reserved, sena 2000, con fecha y franja` → verificado a mano |
| CU-073 | Listar Reservas y Estado de la Seña | `GET /orders/reservations` → anda |
| CU-074 | Confirmar Seña Cobrada en Efectivo | `PATCH /orders/:id/confirm-deposit` → anda |
| CU-075 | Activar Reservas Vencidas Automáticamente (Cron) | `CRON 0 */5 * * * *` → no aplica |
| CU-076 | Expirar Reservas sin Seña Pagada (Cron) | `CRON 0 0 * * * *` → no aplica |
| CU-077 | Expirar Pedidos de MercadoPago sin Pagar (Cron) | `CRON 0 */30 * * * *` → no aplica |
| CU-078 | Obtener el Código de Entrega | `GET /orders/:id/delivery-code` → anda |
| CU-079 | Confirmar Entrega Escaneando el QR | `POST /orders/:id/confirm-delivery` → anda |
| CU-080 | Consultar el Pool de Pedidos Disponibles | `GET /orders/available` → anda |
| CU-081 | Consultar los Pedidos Asignados al Chofer | `GET /orders/delivery/:deliveryId` → anda |
| CU-082 | Crear Usuario Base | `POST /users` → anda |
| CU-083 | Buscar y Listar Usuarios | `GET /users/email/:email` → anda; `GET /users` → anda; `GET /users/phone/:phoneNumber` → anda |
| CU-084 | Verificar Existencia de Usuario | `POST /users/check-exists` → anda |
| CU-085 | Eliminar Usuario | `DELETE /users/:id` → anda |
| CU-086 | Registrar Administrador | `POST /admin` → anda; `POST /admin/register` → anda |
| CU-087 | Crear el Primer Administrador General | `con un super admin ya existente responde 403, que es lo correcto — {"message":"Ya existen administradores en el sistema","error":"Forbidd` → verificado a mano |
| CU-088 | Consultar Administradores | `GET /admin/term/:term` → anda; `GET /admin` → anda |
| CU-089 | Gestionar Roles del Sistema | `POST /role` → anda; `GET /role` → anda; `GET /role/:id` → anda |
| CU-090 | Sembrar los Roles Iniciales | `POST /role/seed` → anda |
| CU-091 | Validar Vigencia del Token de Sesión | `POST /auth` → anda |
| CU-092 | Consultar Listado de Clientes | `GET /customers` → anda |
| CU-093 | Validar o Invalidar Cliente | `PATCH /customers/:id/validate` → anda; `PATCH /customers/:id/invalidate` → anda |
| CU-094 | Actualizar Ubicación del Cliente | `PATCH /customers/:id/location` → anda |
| CU-095 | Eliminar Cliente | `DELETE /customers/:id` → anda |
| CU-096 | Actualizar Perfil del Chofer | `PATCH /delivery/:id` → anda |
| CU-097 | Eliminar Chofer | `DELETE /delivery/:id` → anda |
| CU-098 | Registrar el Token de Notificaciones del Dispositivo | `POST /notifications/token` → anda |
| CU-099 | Consultar los Tokens de un Usuario | `GET /notifications/user/:userId` → anda |
| CU-100 | Enviar Notificación de Prueba | `POST /notifications/send-test` → anda |
| CU-101 | Reenviar Notificación de Confirmación de Pedido | `POST /notifications/order-confirmation` → anda |
| CU-102 | Probar el Servicio de Correo | `POST /email/test` → anda |
| CU-103 | Eliminar Franja Horaria | `DELETE /time-slot/:id` → anda |
| CU-104 | Verificar la Salud del Sistema | `GET /health` → anda; `GET /health/live` → anda; `GET /health/ready` → anda |
| CU-109 | Consultar Detalle del Chofer | `GET /delivery/:id` → anda |
| CU-110 | Buscar Chofer por Usuario | `GET /delivery/user/:userId` → anda |
| CU-111 | Editar Vehículo | `PATCH /car/:id` → anda |
| CU-112 | Eliminar Vehículo | `DELETE /car/:id` → anda |
| CU-113 | Consultar Detalle del Vehículo | `GET /car/:id` → anda |
| CU-114 | Buscar Vehículo por Patente | `GET /car/patent/:patent` → anda |
| CU-115 | Consultar Vehículos de un Chofer | `GET /car/user/:userId` → anda |
| CU-116 | Registrar Dirección de Entrega | `POST /user-address` → anda |
| CU-117 | Consultar Detalle de una Dirección de Entrega | `GET /user-address/:id` → anda |
| CU-118 | Editar Dirección de Entrega | `PATCH /user-address/:id` → anda |
| CU-119 | Eliminar Dirección de Entrega | `DELETE /user-address/:id` → anda |
| CU-120 | Marcar una Dirección como Predeterminada | `PATCH /user-address/:id/set-default` → anda |
| CU-121 | Consultar la Dirección Predeterminada | `GET /user-address/user/:userId/default` → anda |
| CU-129 | Consultar Detalle del Cliente | `GET /customers/:id` → anda |
| CU-130 | Buscar Cliente por Usuario | `GET /customers/user/:userId` → anda |
| CU-131 | Editar Datos del Cliente | `PATCH /customers/:id` → anda |
