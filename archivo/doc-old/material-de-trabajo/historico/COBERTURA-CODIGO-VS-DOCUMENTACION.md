# Análisis de Cobertura: Código vs Documentación

## Resumen Numérico

- **Total de endpoints HTTP encontrados:** 132
- **Manejadores WebSocket (`@SubscribeMessage`):** 3
- **Tareas programadas (`@Cron`):** 4
- **Total general inspeccionado:** 139

- **A. CUBIERTOS:** 130
- **B. SIN DOCUMENTAR:** 3
- **C. DUDOSOS:** 6
- **CU sin implementar (sólo en papel):** 39

La sospecha de que se agregó mucha funcionalidad sin documentar no se sostiene en los números: la documentación reciente (`Casos-de-Uso.md` actualizado con 149 casos) ya cubrió casi todo el código existente. Lo que sí hay es una gran cantidad de casos de uso nuevos que **todavía no tienen código**.

## Grupo B: SIN DOCUMENTAR (Existen en código, sin CU)

Estos endpoints existen en el código y están expuestos, pero ningún caso de uso de los 149 los describe.

### Módulo: `user-addres`

| Método y ruta | Archivo:línea | Rol que exige | Qué hace | Subsistema al que pertenecería |
|---|---|---|---|---|
| `GET /user-address` | `src/user-addres/user-addres.controller.ts:55` | RoleType.SUPER_ADMIN | Lista todas las direcciones del sistema (vista administrativa). | SS-02 (o uno de admin) |

### Módulo: `time-slot`

| Método y ruta | Archivo:línea | Rol que exige | Qué hace | Subsistema al que pertenecería |
|---|---|---|---|---|
| `GET /time-slot` | `src/time-slot/time-slot.controller.ts:32` | RoleType.ADMIN,RoleType.SUPER_ADMIN | Lista todas las franjas horarias (vista administrativa). | SS-09 |
| `GET /time-slot/:id` | `src/time-slot/time-slot.controller.ts:58` | None (Requires auth but no specific role) | Consulta el detalle de una franja horaria específica. | SS-09 |

## Grupo C: DUDOSOS (Cubiertos parcialmente o con diferencias)

| Endpoint | Archivo:línea | CU más parecido | Diferencia |
|---|---|---|---|
| `GET /orders/stats/chart` | `src/order/order.controller.ts:444` | CU-030 - Ver Gráfico de Ventas (últimos 7 días) | El CU describe un gráfico fijo de 7 días, pero el endpoint devuelve datos por rango y granularidad. |
| `GET /users/:id` | `src/users/users.controller.ts:135` | CU-004 - Gestionar Perfil de Usuario | CU-004 es gestionar el propio perfil, pero los endpoints son genéricos y permiten que el Admin los use. |
| `PATCH /users/:id` | `src/users/users.controller.ts:166` | CU-004 - Gestionar Perfil de Usuario | CU-004 es gestionar el propio perfil, pero los endpoints son genéricos y permiten que el Admin los use. |
| `WS driver:join` | `src/gateways/drivers.gateway.ts:76` | CU-021 - Recibir Notificaciones en Tiempo Real | Conexión técnica de WebSocket (paso implícito de los CU en tiempo real). |
| `WS customer:join` | `src/gateways/customers.gateway.ts:56` | CU-021 - Recibir Notificaciones en Tiempo Real | Conexión técnica de WebSocket (paso implícito de los CU en tiempo real). |
| `GET /reports/sales-evolution` | `src/reports/reports.controller.ts:71` | CU-030 - Ver Gráfico de Ventas (últimos 7 días) | El CU describe un gráfico de 7 días, el endpoint acepta rango/granularidad. |

## Grupo A: CUBIERTOS (Documentación al día)

La inmensa mayoría de los endpoints cruzan perfectamente con los casos de uso documentados tras la última actualización.

<details><summary>Ver listado completo de endpoints cubiertos</summary>

| Endpoint | Archivo:línea | CU que lo cubre |
|---|---|---|
| `POST /orders` | `src/order/order.controller.ts:84` | CU-005 - Crear Pedido |
| `GET /orders` | `src/order/order.controller.ts:120` | CU-011 - Listar Todos los Pedidos |
| `GET /orders/customer/:customerId` | `src/order/order.controller.ts:142` | CU-007 - Consultar Historial de Pedidos |
| `GET /orders/delivery/:deliveryId` | `src/order/order.controller.ts:172` | CU-081 - Consultar los Pedidos Asignados al Chofer |
| `GET /orders/available` | `src/order/order.controller.ts:192` | CU-080 - Consultar el Pool de Pedidos Disponibles |
| `GET /orders/reservations` | `src/order/order.controller.ts:213` | CU-073 - Listar Reservas y Estado de la Seña |
| `GET /orders/:id` | `src/order/order.controller.ts:224` | CU-006 - Consultar Detalle de Pedido |
| `PATCH /orders/:id/status` | `src/order/order.controller.ts:246` | CU-015 - Aceptar Pedido |
| `POST /orders/:id/reject` | `src/order/order.controller.ts:275` | CU-016 - Rechazar / Ignorar Pedido |
| `GET /orders/:id/delivery-code` | `src/order/order.controller.ts:295` | CU-078 - Obtener el Código de Entrega (QR del chofer) |
| `POST /orders/:id/confirm-delivery` | `src/order/order.controller.ts:317` | CU-079 - Confirmar Entrega Escaneando el QR (cliente) |
| `PATCH /orders/:id/assign/:deliveryId` | `src/order/order.controller.ts:338` | CU-012 - Asignar Chofer Manualmente |
| `PATCH /orders/:id/location` | `src/order/order.controller.ts:351` | CU-017 - Actualizar Ubicación GPS del Chofer |
| `GET /orders/stats/summary` | `src/order/order.controller.ts:367` | CU-026 - Ver Dashboard General |
| `DELETE /orders/:id` | `src/order/order.controller.ts:376` | CU-010 - Cancelar Pedido (Administrador) |
| `PATCH /orders/:id/cancel` | `src/order/order.controller.ts:394` | CU-008 - Cancelar Pedido (Cliente) |
| `PATCH /orders/:id/arrived` | `src/order/order.controller.ts:419` | CU-019 - Avisar Llegada al Cliente |
| `PATCH /orders/:id/confirm-deposit` | `src/order/order.controller.ts:433` | CU-074 - Confirmar Seña Cobrada en Efectivo |
| `CRON */15 * * * * *` | `src/order/dispatch.service.ts:32` | CU-014 - Reintentar Asignación con Radio Expandido (Cron) |
| `POST /webhook/mercadopago` | `src/order/mercadopago-webhook.controller.ts:45` | CU-048 - Procesar Pago con MercadoPago |
| `CRON 0 */5 * * * *` | `src/order/application/reservation.service.ts:128` | CU-075 - Activar Reservas Vencidas Automaticamente (Cron) |
| `CRON 0 0 * * * *` | `src/order/application/reservation.service.ts:166` | CU-076 - Expirar Reservas sin Seña Pagada (Cron) |
| `CRON 0 */30 * * * *` | `src/order/application/reservation.service.ts:226` | CU-077 - Expirar Pedidos de MercadoPago sin Pagar (Cron) |
| `POST /car` | `src/car/car.controller.ts:37` | CU-034 - Registrar Vehículo del Chofer |
| `GET /car` | `src/car/car.controller.ts:47` | CU-051 - Consultar Listado de Vehículos |
| `GET /car/:id` | `src/car/car.controller.ts:56` | CU-113 - Consultar Detalle del Vehículo |
| `GET /car/user/:userId` | `src/car/car.controller.ts:67` | CU-115 - Consultar Vehículos de un Chofer |
| `GET /car/patent/:patent` | `src/car/car.controller.ts:78` | CU-114 - Buscar Vehículo por Patente |
| `PATCH /car/:id` | `src/car/car.controller.ts:89` | CU-111 - Editar Vehículo |
| `DELETE /car/:id` | `src/car/car.controller.ts:101` | CU-112 - Eliminar Vehículo |
| `POST /role` | `src/role/role.controller.ts:24` | CU-089 - Gestionar Roles del Sistema |
| `GET /role` | `src/role/role.controller.ts:29` | CU-089 - Gestionar Roles del Sistema |
| `GET /role/:id` | `src/role/role.controller.ts:34` | CU-089 - Gestionar Roles del Sistema |
| `PATCH /role/:id` | `src/role/role.controller.ts:40` | CU-089 - Gestionar Roles del Sistema |
| `DELETE /role/:id` | `src/role/role.controller.ts:48` | CU-089 - Gestionar Roles del Sistema |
| `POST /role/seed` | `src/role/role.controller.ts:53` | CU-090 - Sembrar los Roles Iniciales |
| `POST /ratings` | `src/rating/rating.controller.ts:35` | CU-064 - Calificar Pedido (cliente↔chofer) |
| `GET /ratings/user/:userId/summary` | `src/rating/rating.controller.ts:53` | CU-065 - Consultar Promedio de Calificaciones de un Usuario |
| `GET /ratings/user/:userId` | `src/rating/rating.controller.ts:64` | CU-066 - Consultar Historial de Calificaciones Recibidas |
| `POST /auth` | `src/auth/auth.controller.ts:23` | CU-091 - Validar Vigencia del Token de Sesión |
| `POST /auth/login` | `src/auth/auth.controller.ts:34` | CU-001 - Iniciar Sesión |
| `POST /auth/login/dashboard` | `src/auth/auth.controller.ts:42` | CU-001 - Iniciar Sesión |
| `GET /health` | `src/health/health.controller.ts:46` | CU-104 - Verificar la Salud del Sistema (liveness / readiness) |
| `GET /health/live` | `src/health/health.controller.ts:63` | CU-104 - Verificar la Salud del Sistema (liveness / readiness) |
| `GET /health/ready` | `src/health/health.controller.ts:76` | CU-104 - Verificar la Salud del Sistema (liveness / readiness) |
| `POST /admin` | `src/admin/admin.controller.ts:21` | CU-086 - Registrar Administrador |
| `GET /admin/term/:term` | `src/admin/admin.controller.ts:28` | CU-088 - Consultar Administradores |
| `POST /admin/first-superadmin` | `src/admin/admin.controller.ts:41` | CU-087 - Crear el Primer Super Administrador (bootstrap) |
| `POST /admin/register` | `src/admin/admin.controller.ts:59` | CU-086 - Registrar Administrador |
| `GET /admin` | `src/admin/admin.controller.ts:94` | CU-088 - Consultar Administradores |
| `POST /coverage-zones` | `src/coverage-zone/coverage-zone.controller.ts:35` | CU-056 - Definir Zona de Cobertura |
| `GET /coverage-zones` | `src/coverage-zone/coverage-zone.controller.ts:45` | CU-057 - Consultar Zonas de Cobertura |
| `GET /coverage-zones/check` | `src/coverage-zone/coverage-zone.controller.ts:59` | CU-058 - Validar Cobertura de una Dirección |
| `DELETE /coverage-zones/:id` | `src/coverage-zone/coverage-zone.controller.ts:70` | CU-059 - Eliminar Zona de Cobertura |
| `POST /user-address` | `src/user-addres/user-addres.controller.ts:42` | CU-116 - Registrar Dirección de Entrega |
| `GET /user-address/:id` | `src/user-addres/user-addres.controller.ts:64` | CU-117 - Consultar Detalle de una Dirección de Entrega |
| `GET /user-address/user/:userId` | `src/user-addres/user-addres.controller.ts:75` | CU-046 - Consultar Direcciones de Entrega del Cliente |
| `GET /user-address/user/:userId/default` | `src/user-addres/user-addres.controller.ts:87` | CU-121 - Consultar la Dirección Predeterminada |
| `PATCH /user-address/:id` | `src/user-addres/user-addres.controller.ts:98` | CU-118 - Editar Dirección de Entrega |
| `PATCH /user-address/:id/set-default` | `src/user-addres/user-addres.controller.ts:110` | CU-120 - Marcar una Dirección como Predeterminada |
| `DELETE /user-address/:id` | `src/user-addres/user-addres.controller.ts:121` | CU-119 - Eliminar Dirección de Entrega |
| `POST /users` | `src/users/users.controller.ts:50` | CU-082 - Crear Usuario Base |
| `GET /users/email/:email` | `src/users/users.controller.ts:60` | CU-083 - Buscar / Listar Usuarios |
| `POST /users/customer-registration` | `src/users/users.controller.ts:75` | CU-002 - Registrarse como Cliente |
| `POST /users/delivery-registration` | `src/users/users.controller.ts:95` | CU-003 - Registrar Chofer |
| `GET /users` | `src/users/users.controller.ts:123` | CU-083 - Buscar / Listar Usuarios |
| `GET /users/phone/:phoneNumber` | `src/users/users.controller.ts:143` | CU-083 - Buscar / Listar Usuarios |
| `POST /users/check-exists` | `src/users/users.controller.ts:151` | CU-084 - Verificar Existencia de Usuario (pre-registro) |
| `DELETE /users/:id` | `src/users/users.controller.ts:213` | CU-085 - Eliminar Usuario (baja lógica) |
| `PATCH /users/:id/block` | `src/users/users.controller.ts:220` | CU-050 - Bloquear / Desbloquear Usuario |
| `WS driver:update-location` | `src/gateways/drivers.gateway.ts:88` | CU-017 - Actualizar Ubicación GPS del Chofer |
| `POST /distributor` | `src/distributor/distributor.controller.ts:40` | CU-052 - Registrar Distribuidora |
| `GET /distributor` | `src/distributor/distributor.controller.ts:46` | CU-053 - Consultar Distribuidoras |
| `GET /distributor/:id` | `src/distributor/distributor.controller.ts:53` | CU-053 - Consultar Distribuidoras |
| `PATCH /distributor/:id` | `src/distributor/distributor.controller.ts:60` | CU-054 - Modificar Datos de la Distribuidora |
| `DELETE /distributor/:id` | `src/distributor/distributor.controller.ts:70` | CU-055 - Dar de Baja una Distribuidora |
| `GET /delivery` | `src/delivery/delivery.controller.ts:45` | CU-035 - Consultar Listado de Choferes |
| `GET /delivery/active` | `src/delivery/delivery.controller.ts:55` | CU-035 - Consultar Listado de Choferes |
| `GET /delivery/:id` | `src/delivery/delivery.controller.ts:64` | CU-109 - Consultar Detalle del Chofer |
| `GET /delivery/user/:userId` | `src/delivery/delivery.controller.ts:73` | CU-110 - Buscar Chofer por Usuario |
| `PATCH /delivery/:id` | `src/delivery/delivery.controller.ts:82` | CU-096 - Actualizar Perfil del Chofer |
| `PATCH /delivery/:id/validate` | `src/delivery/delivery.controller.ts:95` | CU-032 - Validar / Invalidar Chofer |
| `PATCH /delivery/:id/invalidate` | `src/delivery/delivery.controller.ts:108` | CU-032 - Validar / Invalidar Chofer |
| `PATCH /delivery/:id/location` | `src/delivery/delivery.controller.ts:117` | CU-017 - Actualizar Ubicación GPS del Chofer |
| `PATCH /delivery/:id/balance` | `src/delivery/delivery.controller.ts:134` | CU-049 - Consultar Balance / Ganancias del Chofer |
| `PATCH /delivery/:id/status` | `src/delivery/delivery.controller.ts:147` | CU-033 - Activar / Desactivar Chofer (Admin) |
| `DELETE /delivery/:id` | `src/delivery/delivery.controller.ts:161` | CU-097 - Eliminar Chofer (baja lógica) |
| `PATCH /delivery/user/:userId/availability` | `src/delivery/delivery.controller.ts:168` | CU-022 - Activar / Desactivar Disponibilidad |
| `POST /incidents` | `src/incident/incident.controller.ts:39` | CU-060 - Registrar Incidencia de Entrega |
| `GET /incidents` | `src/incident/incident.controller.ts:49` | CU-061 - Listar Incidencias |
| `GET /incidents/order/:orderId` | `src/incident/incident.controller.ts:57` | CU-062 - Consultar Incidencias de un Pedido |
| `PATCH /incidents/:id/resolve` | `src/incident/incident.controller.ts:69` | CU-063 - Resolver Incidencia |
| `POST /gascylinder` | `src/gascylinder/gascylinder.controller.ts:35` | CU-036 - Crear Producto (Garrafa) |
| `GET /gascylinder` | `src/gascylinder/gascylinder.controller.ts:46` | CU-041 - Consultar Catálogo de Productos |
| `GET /gascylinder/:id` | `src/gascylinder/gascylinder.controller.ts:55` | CU-041 - Consultar Catálogo de Productos |
| `GET /gascylinder/type/:type` | `src/gascylinder/gascylinder.controller.ts:66` | CU-041 - Consultar Catálogo de Productos |
| `GET /gascylinder/available/list` | `src/gascylinder/gascylinder.controller.ts:77` | CU-041 - Consultar Catálogo de Productos |
| `PATCH /gascylinder/:id` | `src/gascylinder/gascylinder.controller.ts:89` | CU-037 - Actualizar Precio de Producto |
| `PATCH /gascylinder/:id/stock` | `src/gascylinder/gascylinder.controller.ts:106` | CU-038 - Actualizar Stock de Producto |
| `DELETE /gascylinder/:id` | `src/gascylinder/gascylinder.controller.ts:122` | CU-040 - Activar / Desactivar Producto |
| `POST /time-slot` | `src/time-slot/time-slot.controller.ts:18` | CU-042 - Crear Franja Horaria |
| `GET /time-slot/availability` | `src/time-slot/time-slot.controller.ts:49` | CU-045 - Consultar Franjas Horarias Disponibles |
| `DELETE /time-slot/:id` | `src/time-slot/time-slot.controller.ts:68` | CU-103 - Eliminar Franja Horaria |
| `POST /cylinders` | `src/cylinder/cylinder.controller.ts:41` | CU-067 - Dar de Alta un Envase Físico |
| `POST /cylinders/assign` | `src/cylinder/cylinder.controller.ts:60` | CU-068 - Asignar Envases a un Pedido |
| `GET /cylinders` | `src/cylinder/cylinder.controller.ts:77` | CU-069 - Consultar el Parque de Envases |
| `GET /cylinders/:id` | `src/cylinder/cylinder.controller.ts:89` | CU-069 - Consultar el Parque de Envases |
| `GET /cylinders/:id/history` | `src/cylinder/cylinder.controller.ts:100` | CU-071 - Consultar Historial de Movimientos de un Envase |
| `PATCH /cylinders/:id/transition` | `src/cylinder/cylinder.controller.ts:116` | CU-070 - Registrar Movimiento de Envase (cambio de estado) |
| `POST /notifications/send-test` | `src/notifications/notifications.controller.ts:31` | CU-100 - Enviar Notificación de Prueba |
| `POST /notifications/order-confirmation` | `src/notifications/notifications.controller.ts:47` | CU-101 - Reenviar Notificación de Confirmación de Pedido |
| `GET /notifications/user/:userId` | `src/notifications/notifications.controller.ts:60` | CU-099 - Consultar los Tokens de un Usuario |
| `POST /notifications/token` | `src/notifications/notifications.controller.ts:73` | CU-098 - Registrar el Token de Notificaciones del Dispositivo |
| `POST /email/password-reset` | `src/email/email.controller.ts:31` | CU-047 - Recuperar Contraseña |
| `POST /email/change-email` | `src/email/email.controller.ts:41` | CU-047 - Recuperar Contraseña |
| `POST /email/test` | `src/email/email.controller.ts:53` | CU-102 - Probar el Servicio de Correo |
| `GET /customers` | `src/customer/customer.controller.ts:44` | CU-092 - Consultar Listado de Clientes |
| `GET /customers/:id` | `src/customer/customer.controller.ts:56` | CU-129 - Consultar Detalle del Cliente |
| `GET /customers/user/:userId` | `src/customer/customer.controller.ts:68` | CU-130 - Buscar Cliente por Usuario |
| `PATCH /customers/:id` | `src/customer/customer.controller.ts:80` | CU-131 - Editar Datos del Cliente |
| `PATCH /customers/:id/validate` | `src/customer/customer.controller.ts:94` | CU-093 - Validar / Invalidar Cliente |
| `PATCH /customers/:id/invalidate` | `src/customer/customer.controller.ts:107` | CU-093 - Validar / Invalidar Cliente |
| `PATCH /customers/:id/location` | `src/customer/customer.controller.ts:116` | CU-094 - Actualizar Ubicación del Cliente |
| `DELETE /customers/:id` | `src/customer/customer.controller.ts:131` | CU-095 - Eliminar Cliente (baja lógica) |
| `GET /reports/sales-by-driver` | `src/reports/reports.controller.ts:30` | CU-027 - Ver Reporte de Ventas por Chofer |
| `GET /reports/sales-by-product` | `src/reports/reports.controller.ts:44` | CU-028 - Ver Reporte de Ventas por Producto |
| `GET /reports/sales-by-payment` | `src/reports/reports.controller.ts:57` | CU-029 - Ver Reporte por Método de Pago |
| `POST /claims` | `src/claims/claims.controller.ts:28` | CU-023 - Registrar Reclamo |
| `GET /claims` | `src/claims/claims.controller.ts:47` | CU-024 - Listar Reclamos |
| `PATCH /claims/:id/resolve` | `src/claims/claims.controller.ts:54` | CU-025 - Resolver Reclamo |

</details>

## PASO 4: Casos de Uso No Implementados (Sólo en papel)

Estos casos de uso figuran en `Casos-de-Uso.md` pero **no tienen ningún endpoint, WebSocket ni cron** en el código que los respalde. Son requerimientos a futuro o funcionalidad que quedó pendiente.

| CU | Nombre | Motivo de ausencia |
|---|---|---|
| CU-009 | Cancelar Pedido (Chofer) | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-013 | Asignar Pedido Automáticamente por Proximidad | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-018 | Marcar Pedido "En Camino" | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-020 | Confirmar Entrega | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-021 | Recibir Notificaciones en Tiempo Real | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-031 | Registrar Chofer | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-039 | Configurar Promociones por Cantidad | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-043 | Modificar Capacidad de Franja Horaria | No hay endpoint `@Patch` o `@Put` en el controlador de franjas horarias. |
| CU-044 | Seleccionar Franja Horaria al Crear Pedido | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-072 | Crear Reserva Programada con Seña | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-105 | Planificar el mantenimiento y las habilitaciones de la flota | Son procesos automáticos (ACT-04) que no tienen ninguna tarea `@Cron` ni servicio asignado. |
| CU-106 | Anticipar la recompra por consumo estimado | Son procesos automáticos (ACT-04) que no tienen ninguna tarea `@Cron` ni servicio asignado. |
| CU-107 | Agrupar pedidos por recorrido | Son procesos automáticos (ACT-04) que no tienen ninguna tarea `@Cron` ni servicio asignado. |
| CU-108 | Recuperar envases no devueltos | Son procesos automáticos (ACT-04) que no tienen ninguna tarea `@Cron` ni servicio asignado. |
| CU-122 | Agregar Ítem al Carrito | No existe el módulo de Carrito de Compras en el backend. |
| CU-123 | Modificar la Cantidad de un Ítem del Carrito | No existe el módulo de Carrito de Compras en el backend. |
| CU-124 | Quitar Ítem del Carrito | No existe el módulo de Carrito de Compras en el backend. |
| CU-125 | Consultar el Carrito | No existe el módulo de Carrito de Compras en el backend. |
| CU-126 | Vaciar el Carrito | No existe el módulo de Carrito de Compras en el backend. |
| CU-127 | Cambiar la Dirección de Entrega del Pedido | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-128 | Indicar Quién Recibe el Pedido | No existe endpoint ni cron en el código que ejecute esta funcionalidad. |
| CU-132 | Registrar la Revisión Periódica de un Envase | El módulo de trazabilidad física (`cylinder`) no implementa revisiones periódicas ni vencimientos. |
| CU-133 | Consultar la Vigencia de un Envase | El módulo de trazabilidad física (`cylinder`) no implementa revisiones periódicas ni vencimientos. |
| CU-134 | Consultar los Envases Próximos a Vencer | El módulo de trazabilidad física (`cylinder`) no implementa revisiones periódicas ni vencimientos. |
| CU-135 | Bloquear el Despacho de un Envase Vencido | El módulo de trazabilidad física (`cylinder`) no implementa revisiones periódicas ni vencimientos. |
| CU-136 | Registrar el Seguro del Vehículo | El módulo de flota (`car`) es un CRUD simple, sin gestión de mantenimientos, seguro o licencias. |
| CU-137 | Registrar la Verificación Técnica Vehicular | El módulo de flota (`car`) es un CRUD simple, sin gestión de mantenimientos, seguro o licencias. |
| CU-138 | Registrar la Licencia de Conducir del Chofer | El módulo de flota (`car`) es un CRUD simple, sin gestión de mantenimientos, seguro o licencias. |
| CU-139 | Consultar los Vencimientos de la Flota | El módulo de flota (`car`) es un CRUD simple, sin gestión de mantenimientos, seguro o licencias. |
| CU-140 | Programar un Mantenimiento de Vehículo | El módulo de flota (`car`) es un CRUD simple, sin gestión de mantenimientos, seguro o licencias. |
| CU-141 | Registrar un Mantenimiento Realizado | El módulo de flota (`car`) es un CRUD simple, sin gestión de mantenimientos, seguro o licencias. |
| CU-142 | Avisar los Vencimientos Próximos de la Flota | El módulo de flota (`car`) es un CRUD simple, sin gestión de mantenimientos, seguro o licencias. |
| CU-143 | Declarar el Consumo Promedio al Registrarse | No existen endpoints de configuración de consumos promedios ni fechas estimadas. |
| CU-144 | Actualizar el Consumo Promedio Declarado | No existen endpoints de configuración de consumos promedios ni fechas estimadas. |
| CU-145 | Configurar los Días de Aviso Previo a la Recompra | No existen endpoints de configuración de consumos promedios ni fechas estimadas. |
| CU-146 | Consultar la Fecha Estimada de Recompra | No existen endpoints de configuración de consumos promedios ni fechas estimadas. |
| CU-147 | Realizar una Compra Express | El circuito de compra express y modalidad de entrega no está expuesto en la API actual. |
| CU-148 | Elegir la Modalidad de Entrega del Pedido | El circuito de compra express y modalidad de entrega no está expuesto en la API actual. |
| CU-149 | Despachar un Pedido Express a un Chofer en Moto | El circuito de compra express y modalidad de entrega no está expuesto en la API actual. |
