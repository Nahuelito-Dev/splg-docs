# Jeny Gas Backend — Revisión de Arquitectura (SOLID · DDD · Escalabilidad)

_Revisión hecha por 3 arquitectos en paralelo (lentes: SOLID/estructura, DDD/hexagonal, escalabilidad/performance). Fecha: 2026-07-16. Objetivo: sistema mantenible y escalable para salida a prod nov/dic 2026._

---

## ✅ ESTADO DE RESOLUCIÓN (2026-07-16)

**Toda la revisión fue RESUELTA en esta iteración, verificada en runtime y pusheada a `feat/f1-features`.**

- **P0 (10/10)** — bugs, fugas de tenant, bug de plata (decimals string), módulos muertos, choferes fantasma, recargo MP, DTOs, errores, naming.
- **P1 (6/6)** — Socket.io Redis (escala multi-instancia), disciplina de migraciones + índices calientes, `synchronize:false`, throttler con storage Redis, factory única de config Redis.
- **P2 (todos)** — P2-1 FirebaseModule único + `FirebaseAuthPort`/`FcmPort` · P2-2 EmailService descompuesto (rate-limit/cache → Redis + puerto Resend + template provider) · P2-3 creación cross-domain fuera de UsersService (corta forwardRef) · P2-4 invariante de estado del pedido en `transitionOrder` · P2-5 `distributor_id` NOT NULL + backfill · P2-6 coverage-zone integrado al pricing · P2-8 NotificationPort · P2-9 errores de dominio propios + mapeo HTTP · P2-10 onDelete RESTRICT (protege historial). **Único salteado a propósito:** rename `GasCylinder`/`Cylinder` (cosmético, alta churn).
- **Extra — sweep de seguridad/authz**: cerrados IDOR en user-address y customer, impersonación en create de claims/orders, secuestro de token en notifications, IDOR de lectura en `GET /orders/:id`. Ver el commit `68cd95d` y siguientes.

Suite backend **148 tests verde**. Migraciones aplicadas: `AddHotIndexes`, `DistributorIdNotNull`, `OrderCustomerRestrictOnDelete` (ver `docs/MIGRATIONS.md`).

**Follow-ups menores pendientes** (no bloqueantes): rename de entidades GasCylinder/Cylinder; `GET /users/email|:id|phone` permiten enumeración básica (se usan en el login de las apps); mapear a 409 finito si algún flujo dependía de hard-delete de usuarios; y los diferidos de prod en `../PENDIENTES-PROD.md` (AFIP, iOS APNs, rename de package a wagnerlabs, hosting de legales, rotar secretos, MP Fase 2).

_El detalle original de los hallazgos (cómo se detectaron y las recomendaciones) queda abajo como referencia histórica._

---

## Veredicto general

**El núcleo transaccional (`order` + `payments` + `cylinder`) es de calidad de producción** y no hay que tocarlo salvo para endurecerlo: arquitectura hexagonal real (puertos como `abstract class`, adapters de infra, domain services puros, state machines testeadas), reserva de stock atómica con lock pesimista, webhook MP idempotente (lock + índice único parcial + manejo de carrera pago-vs-expiración), despacho secuencial durable con lock distribuido y radio progresivo, `decimal.js` para plata, `QueryRunner` siempre liberado.

**La deuda está en dos lugares:**
1. **El anillo CRUD/infra transversal** (`users`, `email`, `notifications`, `auth`, `delivery`): acoplado al SDK de Firebase, god objects, `forwardRef` circular, errores tragados, sin tests.
2. **Los prerrequisitos de escala horizontal**: hoy el sistema **no escala a múltiples instancias** por dos motivos concretos (Socket.io sin adapter Redis, y esquema sin migraciones/índices).

**Con 1 instancia y poca carga, anda bien.** Para el objetivo ("varias distribuidoras, muchos pedidos/choferes concurrentes") hay que resolver los P0/P1 de abajo.

---

## P0 — Quick wins de alto impacto (hacer ya, bajo riesgo)

| # | Hallazgo | Archivo(s) | Acción |
|---|---|---|---|
| P0-1 | **Fuga multi-tenant + bug de plata en stats.** `getOrderStats`/`getSalesChartData` cargan TODAS las órdenes a memoria, suman en JS (los `decimal` son **string** → `sum + total` concatena) y NO filtran por `distributor_id` → un admin ve ventas de todas las empresas. | `order.service.ts:201,347` · `order.controller.ts:349,417` | Borrar de `OrderService` y consolidar en `ReportsService` (ya scopeado + agregados SQL). |
| P0-2 | **Decimales como string en todo el modelo.** Columnas `decimal` tipadas `number` que TypeORM hidrata como string → clase entera de bugs (P0-1 es uno). | `order.entity.ts:93,137` · `order-item.entity.ts` · `gascylinder.entity.ts:31` · `payment.entity.ts` | `ColumnNumericTransformer` (`from: Number`) en TODAS las columnas `decimal`. |
| P0-3 | **3 módulos scaffold muertos con endpoints vivos en prod.** `paymentgatway` (typo, fantasma del `payments` real), `webhook`, `seed` devuelven `"This action..."` y montan rutas reales. | `src/{paymentgatway,webhook,seed}/` + `app.module.ts:14,22,23` | Borrar los 3 (el seed real vive en `scripts/seed.ts`). |
| P0-4 | **Choferes fantasma en Redis GEO.** `handleDisconnect` vacío → el chofer offline sigue en el radar; el dispatch le ofrece el pedido y espera 30s a que expire. | `drivers.gateway.ts:58` · `redis.service.ts:150` | `removeDriver(userId)` en disconnect + heartbeat con TTL. Correctness + escala. |
| P0-5 | **Recargo MercadoPago inconsistente (plata).** El catálogo anuncia +10% para MP+Transferencia, pero el pricing lo aplica solo a `TRANSFER`. | `gascylinder.service.ts:184` vs `order-pricing.service.ts:57` | Decidir la regla y unificar. |
| P0-6 | **Deps muertas en `DeliveryService`** (inyecta userRepo/roleRepo/dataSource + init Firebase, nada se usa). | `delivery.service.ts:28-41` | Eliminar las 4 (cae un init de Firebase). |
| P0-7 | **Endpoints sin DTO/validación ni `@Roles`.** `updateLocation`, `cancel` (tipos inline), `notifyArrival` (sin `@Roles`). | `order.controller.ts:333,376,390` | `UpdateLocationDto`/`CancelOrderDto` + `@Roles` en `notifyArrival`. |
| P0-8 | **Errores tragados + `console.error`.** `catch (e) {}` mudos, `console` en vez de `Logger` (pese a tener `GlobalExceptionFilter`). | `users.service.ts:127,296` · `email.service.ts:286` · `delivery.service.ts:232` | Política única: dominio lanza; side-effects best-effort loguean con `Logger`, nunca tragan mudo. |
| P0-9 | **Timeout de MercadoPago SDK** ausente → `getPayment` puede colgar el webhook. | `mercadopago.adapter.ts:26` | `options: { timeout: 5000 }`. |
| P0-10 | Naming: `findOneByPhonee`, `timeOutInterceptor`, `roles.guard` bajo `common/decorators/`. | varios | Renombrar/reubicar en un barrido. |

---

## P1 — Prerrequisitos de escala horizontal (antes de correr multi-instancia)

| # | Hallazgo | Archivo(s) | Acción |
|---|---|---|---|
| P1-1 | 🔴 **Socket.io sin adapter Redis cableado.** `RedisIoAdapter` existe pero `main.ts` nunca lo usa → con N>1 instancias el tiempo real (ofertas, tracking) se rompe en silencio (room en el pod A, emit en el B). | `adapters/redis-io.adapter.ts` · `main.ts` | Cablear en `bootstrap()`: `useWebSocketAdapter(redisIoAdapter)` con la MISMA config Redis. |
| P1-2 | 🔴 **Sin migraciones; esquema por `synchronize`.** En prod los `@Index` no se materializan; no hay forma controlada de agregar índices. | `app.module.ts:93` (no existe `src/migrations`) | Adoptar migraciones TypeORM, `synchronize:false` salvo dev. Migración inicial = esquema actual + índices de abajo. **Prerrequisito de P1-3.** |
| P1-3 | 🔴 **Índices faltantes en columnas calientes** (ver lista dedicada). La query central del dispatch corre en cada pedido + cron cada 15s sin índice → seq scan. | `order.typeorm.repository.ts:65` | Migración con los índices de la sección "Índices". |
| P1-4 | 🟡 **Throttler in-memory** → con N pods el límite es N×límite. | `app.module.ts:57` | `ThrottlerStorageRedis`. |
| P1-5 | 🟡 **Rate-limit y cache de EmailService en memoria** (`Map` + `setInterval`) → rompen statelessness. | `email.service.ts` | Mover a Redis (parte del refactor P2-2). |
| P1-6 | 🟡 **Config Redis divergente** (RedisService, RedisIoAdapter, health crean clientes con config distinta; password comentada en uno). | `redis.service.ts:20` · `redis-io.adapter.ts:18` | Factory única de config Redis compartida. |

---

## P2 — Refactors estructurales (planificar, antes de prod)

| # | Hallazgo | Acción |
|---|---|---|
| P2-1 | 🔴 **Firebase Admin inicializado 5 veces, sin módulo ni puerto** (+ bug: `notifications` inicializa una app pero manda con la default). Impide testear users/notifications/email. | `FirebaseModule` global único + `FirebaseAuthPort`/`FcmPort`. **Primero en la fila** — destraba testeo y arregla el bug. |
| P2-2 | 🔴 **`EmailService` god object** (528 líneas: init Firebase + rate-limit + cache + templates HTML inline + Resend + update users). | Separar: `EmailService` (orquesta) / `EmailTemplateProvider` (templates a archivos) / `EmailSenderPort` (Resend). Rate-limit/cache a Redis. |
| P2-3 | 🔴 **`UsersService` god cross-domain** (crea Customer+Delivery+User) → cadena `forwardRef` en 4 módulos. | Mover creación a `CustomerService.registerWithUser()` / `DeliveryService.registerWithUser()`; `UsersService` queda en User+Firebase. Corta los `forwardRef`. |
| P2-4 | 🔴 **Invariante de estado del pedido desprotegido** — se muta `order.status` directo saltando `assertTransition`. | `assignDelivery` (`order.service.ts:186`) y activaciones de reserva (`reservation.service.ts:142,184`) deben pasar por un único punto de transición. |
| P2-5 | 🔴 **`distributor_id` nullable en todo el modelo tenant.** `null = default` es frágil (agujero de aislamiento). | Migración de backfill + `NOT NULL` en las entidades que ya nacen con tenant (Cylinder/CoverageZone ya lo hacen bien). |
| P2-6 | 🟡 **`coverage-zone` es dominio huérfano** — `checkCoverage` (ST_Contains + surcharge) no se llama en la creación de pedido; el recargo por zona nunca se cobra. | Integrar en `CreateOrderUseCase` (dentro de la tx) + sumar surcharge vía `OrderPricingService`. |
| P2-7 | 🟡 **Colisión de lenguaje ubicuo.** `GasCylinder` (producto) vs `Cylinder` (envase físico); `deposit` = seña vs garantía. | Renombrar entidades (`GasCylinder`→`Product/CylinderType`, `Cylinder`→`PhysicalCylinder`) + `Cylinder.deposit`→`container_deposit`. Migración con find/replace mientras hay poca data. |
| P2-8 | 🟡 **`DIP` asimétrico en order** — use-cases inyectan `NotificationsService` concreto (infra). | `NotificationPort` (mismo patrón que los otros puertos). |
| P2-9 | 🟡 **Excepciones HTTP en el "dominio puro"** (state machines, stock lanzan `BadRequestException`). | Errores de dominio propios (`InvalidTransitionError`…) mapeados a HTTP por filtro. Cosmético pero barato. |
| P2-10 | 🟡 **`onDelete: CASCADE` Order→User** — borrar un cliente borra sus pedidos (peligroso para historial contable). | `RESTRICT`/`SET NULL` + soft-delete coherente. |
| P2-11 | 🟢 **Jobs async sin cola** (FCM/email/conciliación inline best-effort). | Evaluar BullMQ (ya hay Redis): reintentos + backoff; a futuro, mover el motor de dispatch de cron-barrido a jobs con delay. |
| P2-12 | 🟢 **Caching de catálogo/slots/zonas** (`cache-manager` está en deps sin usar). | Redis TTL corto + invalidación al mutar. |

---

## Índices faltantes (para la migración inicial)

**`order`** (tabla más caliente):
- `order(status)`, `order(customer_id)`, `order(delivery_id)`, `order(deliveredAt)`
- compuesto `order(status, delivery_id)` — query central del dispatch (`PENDING AND delivery_id IS NULL`)
- compuesto `order(distributor_id, status, deliveredAt)` — reports/stats por tenant
- compuesto `order(time_slot_id, scheduled_date, status)` — cupo de agendamiento
- compuesto `order(status, deposit_paid, scheduled_date)` — activar reservas
- parcial `order(createdAt) WHERE status='pending' AND paymentMethod='mercadopago' AND gatewayPaymentId IS NULL` — expirar MP impagos

**`delivery`**: `delivery(user_id)`, compuesto `delivery(distributor_id, user_id)`

**`order_dispatch_offer`**: compuesto `(order_id, status)`, compuesto `(status, expiresAt)`

_Ya presentes y correctos (no tocar): GIST en `coverage_zone.area`, único parcial en `order.gatewayPaymentId` y `payment.gateway_payment_id`, índices de `distributor_id`._

---

## Otras mejoras de performance (P1/P2 menores)
- **N+1 en `TimeSlotService.getAvailability`** (`time-slot.service.ts:117`) → una query `GROUP BY`.
- **`getSalesByDriver` carga todo a memoria** (`reports.service.ts:22`) → `GROUP BY` en SQL como sus hermanos.
- **Doble carga de orden en `handleExpiredOffers`** → `findByIdForDispatch` liviano en vez de `FULL_RELATIONS`.
- **GPS sin throttle server-side** (`drivers.gateway.ts:74`) + bug `!data.lat` (falso positivo en lat=0) → throttle 3-5s + validar `== null`.
- **Listados sin paginación** (`findReservations`).

---

## NO hacer (over-engineering para este SaaS)
- Hexagonalizar `car`/`time-slot`/`claims`/`incident`/`rating`/`gascylinder` — es CRUD legítimo.
- Forzar un `Money` VO en el catálogo (sí vale en `payments`, que ya usa `decimal.js`).
- Unificar YA los dos modelos de inventario (`GasCylinder.stock` vs unidades `Cylinder`) — para MVP es defendible, documentarlo como decisión.
- Mover enums de dominio fuera del `.entity.ts` — idiomático NestJS, baja prioridad.

---

## Lo que está MUY BIEN (no romper al refactorizar)
Reserva de stock atómica (`SELECT FOR UPDATE` en la tx del use-case) · webhook MP idempotente (lock + índice único parcial + carrera pago-vs-expiración) · despacho secuencial durable (tabla de ofertas + lock distribuido + radio progresivo) · cupo de franjas con lock transaccional · `StockReservationService` recibiendo el `EntityManager` del caller · state machines puras y testeadas · GEO en Redis · PostGIS con GIST + corto-circuito "sin zonas = cubierto" · precios de servidor en checkout · puertos abstractos como token DI.

---

## Orden de ataque sugerido
1. **P0 completo** (quick wins, 1-2 días) — arregla la fuga de tenant + bug de plata + limpia muertos.
2. **P1-2 + P1-3** (migraciones + índices) — prerrequisito, desbloquea todo lo de datos.
3. **P1-1** (Socket.io Redis) — desbloquea multi-instancia.
4. **P2-1** (FirebaseModule) — destraba testeo del anillo CRUD.
5. Resto de P2 en incrementos, sin frenar el camino a features/prod.
</content>
