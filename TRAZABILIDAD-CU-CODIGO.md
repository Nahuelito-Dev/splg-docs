# Trazabilidad Casos de Uso ↔ Código

**Proyecto:** SPLG — Sistema de Pedidos y Logística de Garrafas de Gas (Jeny Gas)
**Alcance:** backend `jennygas-app-backend`
**Fuentes documentales:** `docs/1-Requisitos.md` (§6, CU expandidos) y `docs/CU-APP-DELIVERY.md` (CU-001..CU-051, SS-01..SS-09)
**Fuente de verdad del código:** controllers `src/**/*.controller.ts`, gateways `src/gateways/*.gateway.ts`, servicios de despacho y crons `@Cron`
**Fecha de la auditoría:** 2026-08-30
**Estado documental de referencia:** mayo 2026 · **Estado del código:** agosto 2026

> Todas las referencias son `archivo:línea` verificadas sobre el árbol actual. Donde la evidencia no alcanza para afirmar, se marca **⚠️ verificar**.

---

## 1. Resumen numérico

| Métrica | Valor |
|---|---|
| CU documentados (CU-001..CU-051) | **51** |
| CU implementados (SÍ) | **49** |
| CU implementados parcialmente (PARCIAL) | **1** (CU-040) |
| CU documentados sin implementar (NO) | **1** (CU-043) |
| Cobertura documental del código | **~45 %** |
| Endpoints HTTP reales en controllers | **132** |
| Handlers WebSocket (`@SubscribeMessage`) | **3** |
| Crons (`@Cron`) | **4** |
| Endpoints HTTP **sin CU documentado** | **60** |
| Crons **sin CU documentado** | **3** (de 4) |
| CU nuevos propuestos (huérfanos del código) | **53** (CU-052 … CU-104) |
| Total de CU tras la actualización | **104** |
| Subsistemas documentados | **9** (SS-01..SS-09) |
| Módulos reales registrados en `app.module.ts` | **23** |
| Subsistemas nuevos propuestos | **9** (SS-10..SS-18) |

**Lectura rápida del desfasaje:** el código no *perdió* funcionalidad respecto de la documentación —prácticamente todo lo escrito está construido— sino que **creció el doble** de lo documentado. De 132 endpoints, 72 responden a algún CU y 60 no tienen ningún CU que los describa. La documentación UP de mayo describe un sistema mono-distribuidora; el código de agosto es multi-tenant, con trazabilidad de envases, cobertura geográfica, incidencias, calificaciones y reservas programadas con seña.

---

## 2. Tabla maestra — CU documentados vs. código

Leyenda: **SÍ** = realizado íntegramente · **PARCIAL** = realizado a medias o con divergencia funcional · **NO** = sin implementación.

| CU | Nombre | Subsistema doc. | ¿Impl.? | Endpoints / servicios reales (`archivo:línea`) | Observación |
|---|---|---|---|---|---|
| CU-001 | Iniciar Sesión | SS-01 | SÍ | `POST /auth/login` — `src/auth/auth.controller.ts:32`<br>`POST /auth/login/dashboard` — `src/auth/auth.controller.ts:40` | Hay **dos** puertas de login: la de las apps y la del panel (esta última setea cookie httpOnly y valida `x-client-source`, `auth.controller.ts:44-47`). El CU documenta una sola. Throttle estricto 8/min en ambas (`auth.controller.ts:31,38`). |
| CU-002 | Registrarse como Cliente | SS-01 | SÍ | `POST /users/customer-registration` — `src/users/users.controller.ts:66` | Endpoint `@Public()`; crea User + Customer + Firebase en un paso (`users.controller.ts:76-81`). |
| CU-003 | Registrarse como Chofer | SS-01 | SÍ | `POST /users/delivery-registration` — `src/users/users.controller.ts:83` | Es el mismo endpoint que realiza CU-031. Solo ADMIN/SUPER_ADMIN (`users.controller.ts:84`). El chofer se asocia a una distribuidora (`users.controller.ts:105-113`), dimensión ausente en el CU documentado. |
| CU-004 | Gestionar Perfil de Usuario | SS-01 | SÍ | `GET /users/:id` — `src/users/users.controller.ts:130`<br>`PATCH /users/:id` — `src/users/users.controller.ts:160`<br>`GET /customers/:id` — `src/customer/customer.controller.ts:51`<br>`GET /customers/user/:userId` — `src/customer/customer.controller.ts:63`<br>`PATCH /customers/:id` — `src/customer/customer.controller.ts:75` | El perfil está partido en dos entidades (User y Customer/Delivery); el CU habla de una sola pantalla. |
| CU-005 | Crear Pedido | SS-02 | SÍ | `POST /orders` — `src/order/order.controller.ts:71`<br>`src/order/application/create-order.use-case.ts` | El caso de uso real hace mucho más que lo documentado: aplica promociones por volumen (`create-order.use-case.ts:196`), crea checkout de MercadoPago (`create-order.use-case.ts:363,390`) y admite el camino de **reserva programada** (ver CU-072). |
| CU-006 | Consultar Detalle de Pedido | SS-02 | SÍ | `GET /orders/:id` — `src/order/order.controller.ts:219` | Aplica ownership: un CUSTOMER solo lee sus pedidos (`order.controller.ts:230-232`). |
| CU-007 | Consultar Historial de Pedidos | SS-02 | SÍ | `GET /orders/customer/:customerId` — `src/order/order.controller.ts:132` | — |
| CU-008 | Cancelar Pedido (Cliente) | SS-02 | SÍ | `PATCH /orders/:id/cancel` — `src/order/order.controller.ts:386` | Los tres CU de cancelación (008/009/010) se realizan con **un único endpoint**; el actor sale del token, nunca del body (`order.controller.ts:401-402`). Idempotente. |
| CU-009 | Cancelar Pedido (Chofer) | SS-02 | SÍ | `PATCH /orders/:id/cancel` — `src/order/order.controller.ts:386` (rol DELIVERY en `:387`) | Ídem CU-008. |
| CU-010 | Cancelar Pedido (Administrador) | SS-02 | SÍ | `PATCH /orders/:id/cancel` — `src/order/order.controller.ts:386`<br>`DELETE /orders/:id` — `src/order/order.controller.ts:371` | Hay **dos** vías para el admin: la cancelación normal y una "cancelación forzada" (`order.controller.ts:373`). El CU documenta una sola. |
| CU-011 | Listar Todos los Pedidos | SS-02 | SÍ | `GET /orders` — `src/order/order.controller.ts:116` | Scopeado por distribuidora, dimensión no documentada. |
| CU-012 | Asignar Chofer Manualmente | SS-02 | SÍ | `PATCH /orders/:id/assign/:deliveryId` — `src/order/order.controller.ts:331` | — |
| CU-013 | Asignar Pedido Automáticamente por Proximidad | SS-03 | SÍ | `src/order/application/dispatch-orchestrator.service.ts:46` (`offerToNextDriver`)<br>`dispatch-orchestrator.service.ts:158` (`findNearestAvailable`) | El modelo real es de **oferta secuencial** (uno a uno, ventana de 30 s), no de asignación directa. El CU no describe el concepto de "oferta". |
| CU-014 | Reintentar Asignación con Radio Expandido (Cron) | SS-03 | SÍ | `@Cron('*/15 * * * * *')` — `src/order/dispatch.service.ts:31` (`tick`)<br>Escalera de radios `[5,10,15,20] km` — `src/order/application/dispatch-orchestrator.service.ts:30,164-165`<br>`handleExpiredOffers` — `dispatch-orchestrator.service.ts:98` | Corre con lock distribuido en Redis para no duplicar en multi-instancia (`dispatch.service.ts:34-35`). |
| CU-015 | Aceptar Pedido | SS-03 | SÍ | `PATCH /orders/:id/status` con `ACCEPTED` — `src/order/order.controller.ts:235`<br>`src/order/application/update-order-status.use-case.ts:98` | El chofer solo puede operar en su nombre: se ignora el `deliveryId` del body (`order.controller.ts:253-255`). Cierra la oferta de despacho (`update-order-status.use-case.ts:127`). |
| CU-016 | Rechazar / Ignorar Pedido | SS-03 | SÍ | `POST /orders/:id/reject` — `src/order/order.controller.ts:265`<br>`src/order/order.service.ts:52` | Único CU cuyo número aparece citado en el código (`order.controller.ts:269`). Re-oferta inmediata al siguiente chofer, sin esperar el timeout. |
| CU-017 | Actualizar Ubicación GPS del Chofer | SS-04 | SÍ | WS `driver:update-location` — `src/gateways/drivers.gateway.ts:87`<br>`PATCH /orders/:id/location` — `src/order/order.controller.ts:346`<br>`PATCH /delivery/:id/location` — `src/delivery/delivery.controller.ts:112` | **Tres** caminos distintos para la misma información (WebSocket + dos REST). El CU documenta solo el WebSocket. El WS además reenvía la posición al cliente del pedido activo (`drivers.gateway.ts:112-121`). |
| CU-018 | Marcar Pedido "En Camino" | SS-04 | SÍ | `PATCH /orders/:id/status` con `ON_THE_WAY` — `src/order/order.controller.ts:235`<br>`src/order/application/update-order-status.use-case.ts:136` | Evento `order:on-the-way` al cliente (`update-order-status.use-case.ts:29`). |
| CU-019 | Avisar Llegada al Cliente | SS-04 | SÍ | `PATCH /orders/:id/arrived` — `src/order/order.controller.ts:408` | No cambia el estado del pedido, solo notifica (`order.controller.ts:413-414`), consistente con el CU. |
| CU-020 | Confirmar Entrega | SS-04 | SÍ | `PATCH /orders/:id/status` con `DELIVERED` — `src/order/order.controller.ts:235`<br>`src/order/application/update-order-status.use-case.ts:155`<br>`src/order/application/confirm-delivery.use-case.ts` | El camino documentado existe, pero el código agregó un **segundo camino anti-fraude por QR** que el CU no contempla y que invierte el actor: lo confirma el **cliente** escaneando el código del chofer (`order.controller.ts:302-303`). Ver CU-078/CU-079. |
| CU-021 | Recibir Notificaciones en Tiempo Real | SS-04 | SÍ | WS `customer:join` — `src/gateways/customers.gateway.ts:55`<br>`notifyCustomer` — `src/gateways/customers.gateway.ts:69`<br>`POST /notifications/token` — `src/notifications/notifications.controller.ts:70`<br>Mapa evento↔estado — `src/order/application/update-order-status.use-case.ts:28-30` | Existen además los gateways `drivers` (`src/gateways/drivers.gateway.ts:17`) y `admin` (`src/gateways/admin.gateway.ts:18`); el CU solo documenta el canal del cliente. |
| CU-022 | Activar / Desactivar Disponibilidad | SS-04 | SÍ | `PATCH /delivery/user/:userId/availability` — `src/delivery/delivery.controller.ts:165`<br>`src/delivery/delivery.service.ts:244` | Al apagarse, se saca al chofer del radar Redis (`delivery.service.ts:266`, comentario cita CU-022 en `:265`). **Nota de diseño:** usa el mismo campo `isActive` que CU-033 (`src/delivery/entities/delivery.entity.ts:54`), o sea que "no disponible ahora" y "dado de baja por el admin" son el mismo bit. |
| CU-023 | Registrar Reclamo | SS-05 | SÍ | `POST /claims` — `src/claims/claims.controller.ts:25` | — |
| CU-024 | Listar Reclamos | SS-05 | SÍ | `GET /claims` — `src/claims/claims.controller.ts:44` | Scopeado por distribuidora (`claims.controller.ts:47`). |
| CU-025 | Resolver Reclamo | SS-05 | SÍ | `PATCH /claims/:id/resolve` — `src/claims/claims.controller.ts:51` | — |
| CU-026 | Ver Dashboard General | SS-06 | SÍ | `GET /orders/stats/summary` — `src/order/order.controller.ts:363`<br>`src/order/order.service.ts:214` (`getOrderStats`)<br>`GET /orders/stats/chart` — `src/order/order.controller.ts:441` | **Divergencia de rutas:** el CU documenta `GET /stats/overview` y `GET /stats/sales-chart?days=7` (`docs/1-Requisitos.md:1266`); las rutas reales cuelgan de `/orders`. El cálculo día/semana/mes existe (`order.service.ts:217-238`). El ítem "choferes activos en tiempo real" del CU **⚠️ verificar** si está en el payload. |
| CU-027 | Ver Reporte de Ventas por Chofer | SS-06 | SÍ | `GET /reports/sales-by-driver` — `src/reports/reports.controller.ts:26` | — |
| CU-028 | Ver Reporte de Ventas por Producto | SS-06 | SÍ | `GET /reports/sales-by-product` — `src/reports/reports.controller.ts:40` | — |
| CU-029 | Ver Reporte por Método de Pago | SS-06 | SÍ | `GET /reports/sales-by-payment` — `src/reports/reports.controller.ts:53` | — |
| CU-030 | Ver Gráfico de Ventas (últimos 7 días) | SS-06 | SÍ | `GET /reports/sales-evolution` — `src/reports/reports.controller.ts:66`<br>`GET /orders/stats/chart` — `src/order/order.controller.ts:441` | Implementado **dos veces**: el reporte real acepta rango y granularidad día/mes (`reports.controller.ts:70-79`), superando lo documentado; el de `/orders` es el fijo de 7 días. |
| CU-031 | Registrar Chofer | SS-07 | SÍ | `POST /users/delivery-registration` — `src/users/users.controller.ts:83` | Mismo endpoint que CU-003. |
| CU-032 | Validar / Invalidar Chofer | SS-07 | SÍ | `PATCH /delivery/:id/validate` — `src/delivery/delivery.controller.ts:89`<br>`PATCH /delivery/:id/invalidate` — `src/delivery/delivery.controller.ts:99` | Campo `validated` en `src/delivery/entities/delivery.entity.ts:51`. |
| CU-033 | Activar / Desactivar Chofer (Admin) | SS-07 | SÍ | `PATCH /delivery/:id/status` — `src/delivery/delivery.controller.ts:141` | Comparte el campo `isActive` con CU-022 (ver observación allí). |
| CU-034 | Registrar Vehículo del Chofer | SS-07 | SÍ | `POST /car` — `src/car/car.controller.ts:33` | — |
| CU-035 | Consultar Listado de Choferes | SS-07 | SÍ | `GET /delivery` — `src/delivery/delivery.controller.ts:41`<br>`GET /delivery/active` — `src/delivery/delivery.controller.ts:52`<br>`GET /delivery/:id` — `src/delivery/delivery.controller.ts:59`<br>`GET /delivery/user/:userId` — `src/delivery/delivery.controller.ts:68` | `GET /delivery/active` **no exige rol** (no tiene `@Roles`, a diferencia de `:42`) — **⚠️ verificar** si es intencional. |
| CU-036 | Crear Producto (Garrafa) | SS-08 | SÍ | `POST /gascylinder` — `src/gascylinder/gascylinder.controller.ts:28` | — |
| CU-037 | Actualizar Precio de Producto | SS-08 | SÍ | `PATCH /gascylinder/:id` — `src/gascylinder/gascylinder.controller.ts:81`<br>`src/gascylinder/gascylinder.service.ts:124` | No hay endpoint dedicado a precio; se actualiza con el PATCH general. |
| CU-038 | Actualizar Stock de Producto | SS-08 | SÍ | `PATCH /gascylinder/:id/stock` — `src/gascylinder/gascylinder.controller.ts:101`<br>`src/gascylinder/gascylinder.service.ts:144` | Es un **delta**, no un valor absoluto (`gascylinder.service.ts:146`), y rechaza stock negativo (`:148-150`). |
| CU-039 | Configurar Promociones por Cantidad | SS-08 | SÍ | `PATCH /gascylinder/:id` con `promotions` — `src/gascylinder/dto/update-gascylinder.dto.ts:15`<br>Campo JSONB — `src/gascylinder/entities/gascylinder.entity.ts:48`<br>Aplicación en el precio — `src/order/domain/order-pricing.service.ts:40,73` | El CU no dice cómo se elige la promoción cuando aplican varias; el código toma **la mejor aplicable** (`order-pricing.service.ts:76-78`). |
| CU-040 | Activar / Desactivar Producto | SS-08 | **PARCIAL** | Desactivación: `DELETE /gascylinder/:id` — `src/gascylinder/gascylinder.controller.ts:114` → `isActive = false` (`src/gascylinder/gascylinder.service.ts:155-157`) | **No existe forma de reactivar un producto.** `UpdateGasCylinderDto` no expone `isActive` (`src/gascylinder/dto/update-gascylinder.dto.ts:7-15`, extiende `CreateGasCylinderDto` que tampoco lo tiene, `create-gascylinder.dto.ts:5-36`) y el pipe global corre con `whitelist: true` + `forbidNonWhitelisted: true` (`src/main.ts:41-42`), así que enviarlo por el PATCH da 400. El CU pide un toggle bidireccional. |
| CU-041 | Consultar Catálogo de Productos | SS-08 | SÍ | `GET /gascylinder` — `src/gascylinder/gascylinder.controller.ts:42`<br>`GET /gascylinder/:id` — `:50`<br>`GET /gascylinder/type/:type` — `:59`<br>`GET /gascylinder/available/list` — `:73` | Cuatro vistas del catálogo; el CU describe una. El listado filtra por `isActive: true` (`gascylinder.service.ts:77`). |
| CU-042 | Crear Franja Horaria | SS-09 | SÍ | `POST /time-slot` — `src/time-slot/time-slot.controller.ts:15` | — |
| CU-043 | Modificar Capacidad de Franja Horaria | SS-09 | **NO** | — | **No existe ningún `@Patch` ni `@Put` en `src/time-slot/time-slot.controller.ts`** (solo `@Post:15`, `@Get:25`, `@Get('availability'):39`, `@Get(':id'):56`, `@Delete(':id'):65`), y `src/time-slot/dto/` contiene únicamente `create-time-slot.dto.ts`. El campo `capacity` existe en la entidad (`src/time-slot/entities/time-slot.entity.ts:37`) pero es inmutable vía API: para cambiar la capacidad hay que borrar y recrear la franja. **Único CU documentado sin código.** |
| CU-044 | Seleccionar Franja Horaria al Crear Pedido | SS-09 | SÍ | `timeSlotId` en `src/order/dto/create-order.dto.ts:70`<br>Reserva de cupo con control de concurrencia — `src/time-slot/time-slot.service.ts:178,190,224` | El código agrega `scheduledDate` (`create-order.dto.ts:81`), no documentado en el CU. |
| CU-045 | Consultar Franjas Horarias Disponibles | SS-09 | SÍ | `GET /time-slot/availability` — `src/time-slot/time-slot.controller.ts:39`<br>`src/time-slot/time-slot.service.ts:142-144` (`remaining`)<br>`GET /time-slot` — `:25` · `GET /time-slot/:id` — `:56` | — |
| CU-046 | Gestionar Direcciones de Entrega | SS-02 | SÍ | `POST /user-address` — `src/user-addres/user-addres.controller.ts:39`<br>`GET /user-address` — `:49` · `GET /user-address/:id` — `:59`<br>`GET /user-address/user/:userId` — `:71`<br>`GET /user-address/user/:userId/default` — `:82`<br>`PATCH /user-address/:id` — `:94`<br>`PATCH /user-address/:id/set-default` — `:106`<br>`DELETE /user-address/:id` — `:117` | CU con la mejor cobertura documental: los 8 endpoints caen dentro del CU. |
| CU-047 | Recuperar Contraseña | SS-01 | SÍ | `POST /email/password-reset` — `src/email/email.controller.ts:24`<br>`POST /email/change-email` — `src/email/email.controller.ts:35` | El reset es `@Public()` (`email.controller.ts:23`); el cambio de email exige sesión. |
| CU-048 | Procesar Pago con MercadoPago | SS-02 | SÍ | `POST /webhook/mercadopago` — `src/order/mercadopago-webhook.controller.ts:41`<br>`src/payments/application/payments.service.ts:113` (`confirmFromGateway`)<br>Creación del checkout — `src/payments/application/payments.service.ts:77`, invocado en `src/order/application/create-order.use-case.ts:363,390` | El código valida firma HMAC del webhook (`mercadopago-webhook.controller.ts:52-66`) y mantiene un **ledger de pagos** propio (`payments.service.ts:162`, entidad `src/payments/entities/payment.entity.ts`) que el CU no menciona. Ver SS-14 propuesto. |
| CU-049 | Consultar Balance / Ganancias del Chofer | SS-07 | SÍ | `PATCH /delivery/:id/balance` — `src/delivery/delivery.controller.ts:128`<br>Consulta vía `GET /delivery/user/:userId` — `src/delivery/delivery.controller.ts:68`<br>Campo `balance` — `src/delivery/entities/delivery.entity.ts:64` | No hay endpoint dedicado de consulta de balance: el chofer lo lee dentro de su perfil. **⚠️ verificar** si el mapper del perfil expone `balance` a la app del chofer. |
| CU-050 | Bloquear / Desbloquear Usuario | SS-01 | SÍ | `PATCH /users/:id/block` — `src/users/users.controller.ts:217`<br>`toggleBlockUser` — `users.controller.ts:223` | Toggle bidireccional real (`{ block: true|false }`). |
| CU-051 | Gestionar Vehículos (editar / eliminar / consultar) | SS-07 | SÍ | `GET /car` — `src/car/car.controller.ts:44`<br>`GET /car/:id` — `:51`<br>`GET /car/user/:userId` — `:63`<br>`GET /car/patent/:patent` — `:74`<br>`PATCH /car/:id` — `:85`<br>`DELETE /car/:id` — `:97` | Todo el módulo `car` queda cubierto entre CU-034 y CU-051. |

---

## 3. Funcionalidad en el código SIN Caso de Uso documentado

60 endpoints HTTP y 3 crons no se corresponden con ningún CU de CU-001..CU-051. Se agrupan por módulo y se les propone código y nombre.

### 3.1 Módulo `distributor` — multi-tenancy (NO existe en la documentación)

Es el hueco documental más grave: **todo el sistema es multi-empresa** y la documentación UP describe una única distribuidora. El decorador `@CurrentDistributor()` atraviesa prácticamente todos los controllers.

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-052 | Registrar Distribuidora | `POST /distributor` — `src/distributor/distributor.controller.ts:36` |
| CU-053 | Consultar Distribuidoras | `GET /distributor` — `src/distributor/distributor.controller.ts:44`<br>`GET /distributor/:id` — `:50` |
| CU-054 | Modificar Datos de la Distribuidora | `PATCH /distributor/:id` — `src/distributor/distributor.controller.ts:57` |
| CU-055 | Dar de Baja una Distribuidora | `DELETE /distributor/:id` — `src/distributor/distributor.controller.ts:67` |

Todo el controller es exclusivo de SUPER_ADMIN (`distributor.controller.ts:31`).

### 3.2 Módulo `coverage-zone` — cobertura geográfica (NO documentado)

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-056 | Definir Zona de Cobertura | `POST /coverage-zones` — `src/coverage-zone/coverage-zone.controller.ts:31` |
| CU-057 | Consultar Zonas de Cobertura | `GET /coverage-zones` — `src/coverage-zone/coverage-zone.controller.ts:42` |
| CU-058 | Validar Cobertura de una Dirección | `GET /coverage-zones/check` — `src/coverage-zone/coverage-zone.controller.ts:49` |
| CU-059 | Eliminar Zona de Cobertura | `DELETE /coverage-zones/:id` — `src/coverage-zone/coverage-zone.controller.ts:66` |

CU-058 es funcionalmente una **precondición de CU-005 (Crear Pedido)**: devuelve `{ covered, zoneId, zoneName, surcharge }` y agrega el concepto de **recargo por zona** (`coverage-zone.controller.ts:52-57`), inexistente en la documentación de precios.

### 3.3 Módulo `incident` — incidencias de entrega (NO documentado)

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-060 | Registrar Incidencia de Entrega | `POST /incidents` — `src/incident/incident.controller.ts:32` (rol DELIVERY incluido, `:33`) |
| CU-061 | Listar Incidencias | `GET /incidents` — `src/incident/incident.controller.ts:46` |
| CU-062 | Consultar Incidencias de un Pedido | `GET /incidents/order/:orderId` — `src/incident/incident.controller.ts:53` |
| CU-063 | Resolver Incidencia | `PATCH /incidents/:id/resolve` — `src/incident/incident.controller.ts:64` |

Entidad con enums propios `IncidentType` / `IncidentStatus` (`src/incident/entities/incident.entity.ts:14,21`). Es un circuito paralelo y distinto al de Reclamos (SS-05): el reclamo lo abre el **cliente**, la incidencia la abre el **chofer**.

### 3.4 Módulo `rating` — calificaciones (NO documentado)

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-064 | Calificar Pedido (cliente↔chofer) | `POST /ratings` — `src/rating/rating.controller.ts:23` (roles CUSTOMER y DELIVERY, `:24`) |
| CU-065 | Consultar Promedio de Calificaciones de un Usuario | `GET /ratings/user/:userId/summary` — `src/rating/rating.controller.ts:42` |
| CU-066 | Consultar Historial de Calificaciones Recibidas | `GET /ratings/user/:userId` — `src/rating/rating.controller.ts:60` |

La calificación es **bidireccional** y recalcula el promedio del chofer (`src/rating/rating.service.ts:155`, `refreshDeliveryAverage`), que se persiste en `delivery.calification` (`src/delivery/entities/delivery.entity.ts:39`).

### 3.5 Módulo `cylinder` — trazabilidad de envases físicos (NO documentado)

Distinto de `gascylinder` (que es el **producto/SKU** del catálogo): `cylinder` es la **unidad física con número de serie**, con máquina de estados propia.

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-067 | Dar de Alta un Envase Físico | `POST /cylinders` — `src/cylinder/cylinder.controller.ts:36` |
| CU-068 | Asignar Envases a un Pedido | `POST /cylinders/assign` — `src/cylinder/cylinder.controller.ts:48`<br>`src/cylinder/cylinder.service.ts:150` (`assignToOrder`) |
| CU-069 | Consultar el Parque de Envases | `GET /cylinders` — `src/cylinder/cylinder.controller.ts:73`<br>`GET /cylinders/:id` — `:84` |
| CU-070 | Registrar Movimiento de Envase (cambio de estado) | `PATCH /cylinders/:id/transition` — `src/cylinder/cylinder.controller.ts:107`<br>`src/cylinder/cylinder.service.ts:118` |
| CU-071 | Consultar Historial de Movimientos de un Envase | `GET /cylinders/:id/history` — `src/cylinder/cylinder.controller.ts:96`<br>`src/cylinder/cylinder.service.ts:263` |

Estados del envase: `IN_DEPOT → FILLED → DISPATCHED → WITH_CUSTOMER → EMPTY_RETURNED` (`src/cylinder/entities/cylinder.entity.ts:20-26`). El cierre del circuito al entregar está en `src/cylinder/cylinder.service.ts:188` (`onOrderDelivered`). Serial único **por distribuidora**, no global (`cylinder.entity.ts:35`).

### 3.6 Módulo `order` — reservas programadas con seña (NO documentado)

La documentación UP menciona "reserva de stock" como `«include»` de CU-005 (`docs/1-Requisitos.md:1717`), pero el código construyó algo distinto y mucho mayor: **pre-reservas a futuro con seña**, con estado `RESERVED` propio (`src/order/entities/order.entity.ts:27`).

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-072 | Crear Reserva Programada con Seña | `POST /orders` con `scheduledDate` + `depositAmount` — `src/order/dto/create-order.dto.ts:81,101`; estado `RESERVED` — `src/order/entities/order.entity.ts:22-27` |
| CU-073 | Listar Reservas y Estado de la Seña | `GET /orders/reservations` — `src/order/order.controller.ts:207`<br>`src/order/application/reservation.service.ts:72` |
| CU-074 | Confirmar Seña Cobrada en Efectivo | `PATCH /orders/:id/confirm-deposit` — `src/order/order.controller.ts:423`<br>`src/order/application/reservation.service.ts:105` |
| CU-075 | Activar Reservas Vencidas Automáticamente (Cron) | `@Cron('0 */5 * * * *')` — `src/order/application/reservation.service.ts:127` (`activateDueReservations`) |
| CU-076 | Expirar Reservas sin Seña Pagada (Cron) | `@Cron('0 0 * * * *')` — `src/order/application/reservation.service.ts:165` (`expireUnpaidReservations`) |
| CU-077 | Expirar Pedidos de MercadoPago sin Pagar (Cron) | `@Cron('0 */30 * * * *')` — `src/order/application/reservation.service.ts:225` (`expireUnpaidMercadoPagoOrders`) |

CU-075/076/077 son procesos del actor ACT-04 (Sistema Automático) totalmente ausentes de la documentación: de los 4 crons del sistema, **solo uno (el de despacho) está documentado** (CU-014).

### 3.7 Módulo `order` — entrega verificada por QR

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-078 | Obtener el Código de Entrega (QR del chofer) | `GET /orders/:id/delivery-code` — `src/order/order.controller.ts:282` |
| CU-079 | Confirmar Entrega Escaneando el QR (cliente) | `POST /orders/:id/confirm-delivery` — `src/order/order.controller.ts:302` |

Es un mecanismo **anti-fraude** que invierte el actor de CU-020: el chofer muestra un QR y el **cliente** lo escanea (`order.controller.ts:307-311`). El código secreto vive en `order.deliveryCode` (`src/order/entities/order.entity.ts:202`).

### 3.8 Módulo `order` — vistas operativas del chofer

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-080 | Consultar el Pool de Pedidos Disponibles | `GET /orders/available` — `src/order/order.controller.ts:188` |
| CU-081 | Consultar los Pedidos Asignados al Chofer | `GET /orders/delivery/:deliveryId` — `src/order/order.controller.ts:167` |

CU-080 es además la fuente del bootstrap del cron de despacho (`src/order/dispatch.service.ts:50-53`).

### 3.9 Módulos `users`, `admin`, `role`, `auth` — administración de cuentas

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-082 | Crear Usuario Base | `POST /users` — `src/users/users.controller.ts:46` (`@Public()`, `:45`) |
| CU-083 | Buscar / Listar Usuarios | `GET /users` — `src/users/users.controller.ts:120`<br>`GET /users/email/:email` — `:55` (`@Public()`, `:54`)<br>`GET /users/phone/:phoneNumber` — `:139` |
| CU-084 | Verificar Existencia de Usuario (pre-registro) | `POST /users/check-exists` — `src/users/users.controller.ts:148` |
| CU-085 | Eliminar Usuario (baja lógica) | `DELETE /users/:id` — `src/users/users.controller.ts:206` |
| CU-086 | Registrar Administrador | `POST /admin` — `src/admin/admin.controller.ts:18`<br>`POST /admin/register` — `src/admin/admin.controller.ts:52` |
| CU-087 | Crear el Primer Super Administrador (bootstrap) | `POST /admin/first-superadmin` — `src/admin/admin.controller.ts:33` (`@Public()`, `:32`) |
| CU-088 | Consultar Administradores | `GET /admin` — `src/admin/admin.controller.ts:91`<br>`GET /admin/term/:term` — `src/admin/admin.controller.ts:25` |
| CU-089 | Gestionar Roles del Sistema | `POST /role` — `src/role/role.controller.ts:23`<br>`GET /role` — `:28` · `GET /role/:id` — `:33`<br>`PATCH /role/:id` — `:39` · `DELETE /role/:id` — `:47` |
| CU-090 | Sembrar los Roles Iniciales | `POST /role/seed` — `src/role/role.controller.ts:52` |
| CU-091 | Validar Vigencia del Token de Sesión | `POST /auth` — `src/auth/auth.controller.ts:22` |

CU-086 contiene reglas de negocio multi-tenant no documentadas: un admin de empresa solo puede crear admins de su propia distribuidora y nunca super_admins (`src/admin/admin.controller.ts:74-85`).

**⚠️ verificar (riesgo, fuera del alcance de este informe):** `GET /users/email/:email` es `@Public()` (`users.controller.ts:54-55`), lo que expone datos de usuario sin autenticación.

### 3.10 Módulo `customer` — gestión de clientes por el administrador

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-092 | Consultar Listado de Clientes | `GET /customers` — `src/customer/customer.controller.ts:37` |
| CU-093 | Validar / Invalidar Cliente | `PATCH /customers/:id/validate` — `src/customer/customer.controller.ts:88`<br>`PATCH /customers/:id/invalidate` — `:98` |
| CU-094 | Actualizar Ubicación del Cliente | `PATCH /customers/:id/location` — `src/customer/customer.controller.ts:111` |
| CU-095 | Eliminar Cliente (baja lógica) | `DELETE /customers/:id` — `src/customer/customer.controller.ts:124` |

Existe un CU-035 "Consultar Listado de Choferes" pero **ningún equivalente para clientes**, y CU-032 valida choferes pero no hay CU para la validación de clientes, que el código sí implementa.

### 3.11 Módulo `delivery` — huecos

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-096 | Actualizar Perfil del Chofer | `PATCH /delivery/:id` — `src/delivery/delivery.controller.ts:77` |
| CU-097 | Eliminar Chofer (baja lógica) | `DELETE /delivery/:id` — `src/delivery/delivery.controller.ts:154` |

### 3.12 Módulo `notifications`

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-098 | Registrar el Token de Notificaciones del Dispositivo | `POST /notifications/token` — `src/notifications/notifications.controller.ts:70` |
| CU-099 | Consultar los Tokens de un Usuario | `GET /notifications/user/:userId` — `src/notifications/notifications.controller.ts:57` |
| CU-100 | Enviar Notificación de Prueba | `POST /notifications/send-test` — `src/notifications/notifications.controller.ts:27` |
| CU-101 | Reenviar Notificación de Confirmación de Pedido | `POST /notifications/order-confirmation` — `src/notifications/notifications.controller.ts:43` |

CU-098 es la **precondición técnica de CU-021** (sin token registrado no hay push) y el CU-021 documentado no la menciona. Ambos endpoints tienen control anti-secuestro: un no-admin solo opera sobre su propio token (`notifications.controller.ts:65-67,79-81`).

### 3.13 Módulo `email`

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-102 | Probar el Servicio de Correo | `POST /email/test` — `src/email/email.controller.ts:51` (`@Public()`, `:50`) |

El propio código lo marca como "ENDPOINT TEMPORAL" (`src/email/email.controller.ts:49`). **⚠️ verificar** antes de producción: es público y dispara envío de mail.

### 3.14 Módulo `time-slot` — hueco

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-103 | Eliminar Franja Horaria | `DELETE /time-slot/:id` — `src/time-slot/time-slot.controller.ts:65` |

Nótese la asimetría: el código permite **borrar** una franja pero no **modificarla** (ver CU-043, NO implementado).

### 3.15 Módulo `health` — operación

| Nuevo CU | Nombre propuesto | Evidencia |
|---|---|---|
| CU-104 | Verificar la Salud del Sistema (liveness / readiness) | `GET /health` — `src/health/health.controller.ts:42`<br>`GET /health/live` — `:60`<br>`GET /health/ready` — `:72` |

Chequea Postgres, Redis y memoria RSS (`health.controller.ts:48-51`). Es el CU de soporte a NFR-03 (Disponibilidad) y NFR-04 (Escalabilidad) — hoy los NFR no tienen ningún CU que los realice.

### 3.16 Módulo `payments` — sin endpoints propios, pero con lógica sin CU

`src/payments/` no está registrado en `app.module.ts`: lo importa `src/order/order.module.ts:40,61`. Expone su superficie HTTP a través del webhook (CU-048), pero el **ledger de pagos** (`src/payments/application/payments.service.ts:162`, entidad `src/payments/entities/payment.entity.ts`) y el puerto de pasarela (`src/payments/domain/ports/payment-gateway.port.ts:48`) constituyen lógica de negocio de conciliación que ningún CU describe. Se recomienda cubrirla al ampliar CU-048 o crear un CU de conciliación de pagos en una próxima iteración (**⚠️ verificar** el alcance antes de asignarle código, para no inventar funcionalidad).

---

## 4. CU documentados que el código NO implementa

| CU | Nombre | Subsistema | Evidencia de la ausencia |
|---|---|---|---|
| CU-043 | Modificar Capacidad de Franja Horaria | SS-09 | `src/time-slot/time-slot.controller.ts` no contiene `@Patch` ni `@Put`: sus únicas operaciones son `@Post():15`, `@Get():25`, `@Get('availability'):39`, `@Get(':id'):56` y `@Delete(':id'):65`. `src/time-slot/dto/` contiene un solo archivo, `create-time-slot.dto.ts` (no hay `update-time-slot.dto.ts`). El campo `capacity` existe (`src/time-slot/entities/time-slot.entity.ts:37`) y se lee para el control de cupo (`src/time-slot/time-slot.service.ts:178,224`), pero no hay camino de escritura posterior al alta. |

**Parcialmente no implementado:**

| CU | Nombre | Qué falta |
|---|---|---|
| CU-040 | Activar / Desactivar Producto | La **reactivación**. Solo existe la desactivación por `DELETE /gascylinder/:id` (`src/gascylinder/gascylinder.controller.ts:114` → `gascylinder.service.ts:157`). `isActive` no es escribible por el PATCH: no está en `UpdateGasCylinderDto` (`src/gascylinder/dto/update-gascylinder.dto.ts:7-15`) ni en `CreateGasCylinderDto` (`src/gascylinder/dto/create-gascylinder.dto.ts:5-36`), y el `ValidationPipe` global rechaza propiedades no declaradas (`src/main.ts:41-42`). |

**Conclusión de esta sección:** el desfasaje **no** es de funcionalidad faltante. Es de funcionalidad **no documentada**. Solo 1 de 51 CU quedó en el papel; en cambio 53 comportamientos reales no tienen CU.

---

## 5. Subsistemas — documentados vs. módulos reales

### 5.1 Los 23 módulos registrados en `src/app.module.ts`

`FirebaseModule`, `UsersModule`, `AdminModule`, `AuthModule`, `CarModule`, `RoleModule`, `DeliveryModule`, `CustomersModule`, `OrderModule`, `GasCylinderModule`, `EmailModule`, `NotificationsModule`, `UserAddresModule`, `RedisModule`, `ClaimsModule`, `TimeSlotModule`, `ReportsModule`, `HealthModule`, `DistributorModule`, `RatingModule`, `IncidentModule`, `CoverageZoneModule`, `CylinderModule` (`src/app.module.ts:127-149`).

`PaymentsModule` no figura ahí: se importa desde `src/order/order.module.ts:40,61`. Los gateways WebSocket (`src/gateways/`) tampoco son módulos propios.

### 5.2 Contraste

| Subsistema documentado | Módulos reales que lo realizan | Estado |
|---|---|---|
| SS-01 Autenticación y Usuarios | `AuthModule`, `UsersModule`, `FirebaseModule`, `EmailModule` (reset de clave) | Cubierto, pero le faltan `AdminModule` y `RoleModule` |
| SS-02 Gestión de Pedidos | `OrderModule` | Cubierto; el módulo real desborda el subsistema (reservas, QR, pagos) |
| SS-03 Despacho y Asignación | `OrderModule` (`dispatch.service.ts`, `application/dispatch-orchestrator.service.ts`), `RedisModule` | Cubierto |
| SS-04 Seguimiento en Tiempo Real | `src/gateways/` (3 gateways), `RedisModule`, `NotificationsModule` | Cubierto |
| SS-05 Reclamos | `ClaimsModule` | Cubierto |
| SS-06 Reportes y Dashboard | `ReportsModule`, parte de `OrderModule` (`stats/*`) | Cubierto; las rutas del dashboard divergen de lo documentado |
| SS-07 Gestión de Choferes y Vehículos | `DeliveryModule`, `CarModule` | Cubierto |
| SS-08 Gestión de Productos e Inventario | `GasCylinderModule` | Cubierto solo el catálogo; el inventario **físico** (`CylinderModule`) quedó afuera |
| SS-09 Franjas Horarias | `TimeSlotModule` | Cubierto salvo CU-043 |
| **(sin subsistema)** | `DistributorModule` | **Huérfano** |
| **(sin subsistema)** | `CoverageZoneModule` | **Huérfano** |
| **(sin subsistema)** | `IncidentModule` | **Huérfano** |
| **(sin subsistema)** | `RatingModule` | **Huérfano** |
| **(sin subsistema)** | `CylinderModule` | **Huérfano** |
| **(sin subsistema)** | `PaymentsModule` | **Huérfano** (parcialmente tocado por CU-048) |
| **(sin subsistema)** | `AdminModule`, `RoleModule` | **Huérfanos** (asimilables a SS-01) |
| **(sin subsistema)** | `HealthModule`, `RedisModule` | **Huérfanos** (infraestructura / operación) |
| **(sin subsistema)** | `CustomersModule` | Parcialmente en SS-01 vía CU-004; su cara administrativa no tiene subsistema |

### 5.3 Mapeo actualizado propuesto

| Código | Subsistema | Módulos reales | Actores | CU incluidos |
|---|---|---|---|---|
| SS-01 | Autenticación y Usuarios | `AuthModule`, `UsersModule`, `FirebaseModule` | ACT-01, ACT-02, ACT-03 | CU-001..004, 047, 050, 082..085, 091 |
| SS-02 | Gestión de Pedidos | `OrderModule` | ACT-01..04 | CU-005..012, 046, 080, 081 |
| SS-03 | Despacho y Asignación | `OrderModule` (dispatch), `RedisModule` | ACT-02, ACT-03, ACT-04 | CU-013..016 |
| SS-04 | Seguimiento en Tiempo Real | `src/gateways/`, `RedisModule` | ACT-01, ACT-02 | CU-017..022, 078, 079 |
| SS-05 | Reclamos | `ClaimsModule` | ACT-01, ACT-03 | CU-023..025 |
| SS-06 | Reportes y Dashboard | `ReportsModule`, `OrderModule` (stats) | ACT-03 | CU-026..030 |
| SS-07 | Gestión de Choferes y Vehículos | `DeliveryModule`, `CarModule` | ACT-03 | CU-031..035, 049, 051, 096, 097 |
| SS-08 | Gestión de Productos (Catálogo) | `GasCylinderModule` | ACT-01, ACT-03 | CU-036..041 |
| SS-09 | Franjas Horarias | `TimeSlotModule` | ACT-01, ACT-03 | CU-042..045, 103 |
| **SS-10** | **Multi-Distribuidora (Multi-Tenancy)** | `DistributorModule` + decorador `@CurrentDistributor` transversal | ACT-03 (SUPER_ADMIN) | CU-052..055 |
| **SS-11** | **Cobertura Geográfica** | `CoverageZoneModule` | ACT-01, ACT-03 | CU-056..059 |
| **SS-12** | **Incidencias y Calidad de Servicio** | `IncidentModule`, `RatingModule` | ACT-01, ACT-02, ACT-03 | CU-060..066 |
| **SS-13** | **Trazabilidad de Envases** | `CylinderModule` | ACT-02, ACT-03 | CU-067..071 |
| **SS-14** | **Pagos y Conciliación** | `PaymentsModule` | ACT-01, ACT-04 | CU-048 (se reubica desde SS-02) |
| **SS-15** | **Reservas Programadas** | `OrderModule` (`application/reservation.service.ts`) | ACT-01, ACT-03, ACT-04 | CU-072..077 |
| **SS-16** | **Administración de Cuentas y Roles** | `AdminModule`, `RoleModule`, `CustomersModule` (cara admin) | ACT-03 | CU-086..090, 092..095 |
| **SS-17** | **Notificaciones y Mensajería** | `NotificationsModule`, `EmailModule`, `FirebaseModule` | ACT-01, ACT-02, ACT-03 | CU-098..102 |
| **SS-18** | **Observabilidad y Operación** | `HealthModule`, `RedisModule` | ACT-04 | CU-104 |

**Notas del mapeo:**

1. **SS-08 conviene renombrarse a "Gestión de Productos (Catálogo)"** y separarse de SS-13: `gascylinder` es el SKU comercial; `cylinder` es el activo físico con serie. Hoy la documentación los confunde bajo "Productos e Inventario".
2. **SS-10 no es un subsistema más: es una dimensión transversal.** Todo CU de SS-02, SS-06, SS-07, SS-08 y SS-11 está scopeado por distribuidora. Conviene documentarlo también como restricción arquitectónica, no solo como 4 CU de ABM.
3. **SS-14 justifica el traslado de CU-048 fuera de SS-02**: `payments` es un módulo con puerto/adaptador propio (`src/payments/domain/ports/payment-gateway.port.ts`), pensado para más de una pasarela.
4. **SS-18 es el que respalda NFR-03 y NFR-04**, hoy sin ningún CU asociado en la matriz de rastreabilidad (`docs/1-Requisitos.md:1816`).

---

## 6. Observaciones transversales para la defensa de tesis

1. **La documentación no está mal, está atrasada.** 49/51 CU implementados es una tasa de realización altísima. El problema es inverso al habitual: el código creció y no se re-documentó.
2. **El actor ACT-04 (Sistema Automático) está gravemente sub-documentado.** Tiene 4 crons reales (`src/order/dispatch.service.ts:31` y `src/order/application/reservation.service.ts:127,165,225`) y solo 1 CU (CU-014).
3. **Divergencias funcionales concretas a corregir en el documento**, no solo faltantes: CU-020 (el confirmador real puede ser el cliente vía QR), CU-026 (rutas), CU-017 (tres caminos, no uno), CU-013 (modelo de oferta secuencial, no de asignación directa).
4. **Dos deudas reales del código detectadas al trazar:** CU-043 sin implementar y CU-040 sin reactivación. Ambas son de bajo esfuerzo y cerrarían la brecha a 51/51.
5. **Colisión de semántica en `delivery.isActive`** (`src/delivery/entities/delivery.entity.ts:54`): CU-022 (disponibilidad del chofer, self-service) y CU-033 (alta/baja por el admin) escriben el mismo bit. Un admin que desactiva a un chofer y un chofer que se pone "offline" son indistinguibles en la base.

---

*Informe generado en modo solo lectura. Ningún archivo del código fue modificado.*
