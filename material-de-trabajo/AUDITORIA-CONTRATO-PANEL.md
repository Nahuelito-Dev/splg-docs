# Auditoría del contrato panel ↔ API

Hecha llamada por llamada contra la API corriendo en `localhost:3100` (back en
watch, sin tocar), con los dos roles del seed (`superadmin@splg.com` con
`X-Distributor: jeny-gas`, `admin@splg.com`). Evidencia con `curl` (headers
`X-Client-Source: panel-app` + `Authorization`) y lectura del código del back
en `../../splg-app-backend/src`.

Alcance respetado: no se tocó `src/pages/CoverageZones/**`, ni
`src/pages/Orders/components/details/**`, ni la columna de zona de la tabla de
pedidos (lo trabaja otro agente en paralelo). Tampoco se tocó
`src/pages/Home/**` (en rediseño en paralelo): esos endpoints se auditaron
igual, por pedido explícito, y quedan documentados sin editar código.

Leyenda de veredicto: **OK** (panel refleja la API) · **Panel** (desajuste del
lado del panel, arreglado en esta tanda) · **API** (desajuste o rareza del
lado del back, pendiente, con propuesta) · **Semántica** (funciona, pero el
significado no es el que parece o no está documentado).

## Resumen

- Filas auditadas: 41 endpoints + 2 eventos de socket.
- OK: 34.
- Desajustes de panel arreglados: 4 (detalle abajo).
- Desajustes/semántica de API pendientes (para el back, no tocados): 4.
- Fuera de alcance pero con hallazgo para el otro agente: 1 (CoverageZones).

---

## Pedidos (`services/api/orders.ts`, `services/queries/orders.ts`)

| Endpoint / evento | Qué hace el panel | Qué hace la API | Veredicto | Evidencia |
|---|---|---|---|---|
| `GET /orders` (filtros `term/status/from/to`) | Lista pedidos paginados; filtro de estado con `ORDER_STATUSES` (`reserved,pending,accepted,out_for_delivery,delivered,cancelled`) | Acepta exactamente esos 6 valores (`QueryOrdersDto` los traduce a `OrderStatus` interno); `term` busca cliente/id; `from/to` inclusive | OK | `curl .../orders?status=out_for_delivery` → 200, 20 resultados con `status:"out_for_delivery"`. Los 6 valores probados dan 200 y el status esperado. |
| `PATCH /orders/:id/cancel` | Cancelación por rol (admin fuerza) | Actor sale del token, nunca del body | OK | Coincide con `CancelOrderBody` (`reason?`). |
| `PATCH /orders/:id/assign/:deliveryId` | Asignación manual, para pisar la automática | Sólo exige `delivery.isActive` (no `validated`) | OK | Ver nota de semántica de `isActive` más abajo. |
| `GET /delivery/active` (para el modal de asignación manual) | **Antes:** `listActiveDeliveries()` sin parámetros, ignoraba `X-Total-Count`. **Ahora:** pagina con `pageSize:100` + `search`, muestra "Mostrando X de Y" y deja buscar por nombre/teléfono/patente | Pagina (`limit`/`offset`/`term`), default `limit=10` | **Panel (arreglado)** | Con el seed actual hay **160** choferes activos (`X-Total-Count: 160`); sin este fix, el modal sólo mostraba los primeros 10 y no había forma de llegar a los otros 150. Ver "Arreglos" abajo. |
| `GET /orders/customer/:userId` | Historial de un cliente | Ownership: cliente ve el suyo, staff con scope de tenant | OK | — |
| `order:created`, `order:accepted`, `order:on_the_way`, `order:delivered`, `order:cancelled` (namespace `/admin`) | `NotificationBell` escucha los 5 y arma un mensaje | `AdminGateway.notifyAdmins` emite exactamente esos 5 nombres (`\`order:${status}\`` con el valor crudo del enum, y `'order:cancelled'` literal) | **Panel (arreglado)** | El payload real es `{orderId, status, totalAmount}` (creación agrega `distributorId, paymentMethod`; cancelación agrega `reason`, no `status`≠cancelled). **Nunca** viaja `customerName` ni `address`: el `TODO(backend)` y la interfaz `OrderSocketPayload` los asumían y la cláusula "de {cliente}" nunca se mostraba (siempre `undefined`). Corregido: interfaz con los campos reales + mensaje con id corto y monto/motivo. |
| Handshake del socket admin (`connect(auth)`) | Comentario decía "TODO(backend): reemplazar por el handshake real... hoy `auth` viaja como contexto informativo nomás" | `AdminGateway.handleConnection` **ya** valida `auth.token` (`tokenDelHandshake` + `authService.decodeToken`) y desconecta si falta o es inválido | **Panel (arreglado)** | El comentario mentía sobre el estado actual del contrato (el handshake real ya existe y se aplica desde hace tiempo). Corregido el comentario en `useSocket.ts`. |
| `order:driver-location` | `Tracking` pinta `{orderId, driverId, lat, lng, at}` | `DriversGateway` emite exactamente esos 5 campos a `adminGateway.notifyAdmins('order:driver-location', payload)` | OK | Coincide 1 a 1, sin campos de más ni de menos. |

---

## Tablero / Inicio (auditado por pedido explícito; **no se tocó código de `src/pages/Home/**`**)

| Endpoint | Qué devuelve la API | Semántica exacta (mirando `order.service.ts` / `delivery.service.ts`) | Veredicto |
|---|---|---|---|
| `GET /orders/stats/summary` → `ordersSummary` | `{pending, accepted, onTheWay, deliveredToday}` | `pending/accepted/onTheWay` son conteos **totales históricos** por estado actual (sin filtro de fecha); sólo `deliveredToday` filtra por `deliveredAt` de hoy. Un pedido `pending` de hace 3 días sigue sumando acá. | Semántica: el nombre no avisa que `pending/accepted/onTheWay` no son "de hoy". |
| `sales.today` | Suma de `totalAmount` de pedidos `DELIVERED` con `deliveredAt` de **hoy** (00:00 a 23:59 hora del server) | — | OK |
| `sales.week` | Suma de `DELIVERED` con `deliveredAt` entre el **domingo 00:00 de la semana calendario en curso** y el sábado siguiente (`weekStart = hoy - hoy.getDay()`) | **Es semana calendario (domingo a sábado), NO "últimos 7 días"** | Semántica: distinto del gráfico (`stats/chart`), que sí es "últimos 7 días corridos". Confundible si se muestran juntos. |
| `sales.month` | Suma de `DELIVERED` con `deliveredAt` entre el día 1 del mes en curso y el día 1 del mes siguiente | Mes calendario | OK, documentar |
| `sales.total` | Suma de **todos** los `DELIVERED` de siempre (sin filtro de fecha) | "Total histórico", no "total del período" | OK, documentar |
| Qué estados cuentan como venta | **Sólo `DELIVERED`** (por `deliveredAt`, no por `createdAt`) | `pending/accepted/on_the_way/cancelled` nunca suman a `sales.*` | OK |
| `performance.activeDeliveries` | `DeliveryService.contarDisponibles`: `COUNT(*) WHERE isActive=true AND validated=true` (scopeado por distribuidora) | **No es "choferes conectados ahora"**: `isActive` es la MISMA columna que (a) el admin prende/apaga con `PATCH /delivery/:id/status` y (b) el chofer prende/apaga con su propio toggle "ir en línea" (`PATCH /delivery/user/:id/availability`, ver `delivery.service.ts:378`). Un chofer habilitado por el admin pero que nunca se puso "en línea" hoy, si nunca se desconectó, sigue contando. | Semántica dudosa (ver nota general de `isActive` abajo) |
| `performance.avgOrderValue` | `todaySales / deliveredToday` (0 si no hubo entregas hoy) | Es el ticket promedio **de hoy**, no histórico | OK, documentar |
| `performance.ordersPerDay` | Literal `= deliveredToday` (el mismo número que `ordersSummary.deliveredToday`) | El nombre sugiere una tasa/promedio diario; es exactamente "entregados hoy" duplicado. El propio Swagger lo describe bien (`"Entregados hoy"`), pero el nombre del campo no. | **API (semántica)**: no confunde a quien mira el doc, pero si el front deriva algo de "por día" a futuro (ej. mostrar como una métrica distinta) el nombre induce a error. Propuesta: renombrar a algo como `deliveredTodayCount` (duplicado explícito) o calcular un promedio real (ej. total histórico / días desde el alta de la distribuidora). |
| `paymentMethods.{cash,mercadopago}` | `COUNT` de `DELIVERED` con ese método de pago, `deliveredAt >= inicio del mes en curso` | **Es "este mes", no "hoy" ni "histórico"** — el DTO (`MediosDePagoDto`) no lo dice en su `@ApiProperty`, sólo trae `example` | **API (semántica)**: agregar `description: 'Del mes en curso'` en `src/order/dto/order-stats-response.dto.ts` (clase `MediosDePagoDto`), para que quien mire el Swagger no asuma "hoy". |
| `GET /orders/stats/chart` | Un punto por cada uno de los **últimos 7 días corridos** (hoy incluido, hoy - 6 hasta hoy), ventas `DELIVERED` por `deliveredAt`, agrupadas por día | Coincide con el comentario del panel (`stats.ts`: "ventas de los últimos 7 días") | OK |
| `GET /delivery/active` vs `activeDeliveries` del tablero | El pool de "activos" para asignar a mano (`isActive` solo) es más grande que el "activeDeliveries" del tablero (`isActive AND validated`) | No es inconsistencia: son dos preguntas distintas ("¿a quién le puedo asignar un pedido a mano?" vs "¿cuántos choferes tengo operativos y aprobados?") | OK, documentar la diferencia si el tablero linkea a la lista de choferes activos |

**Nota general sobre `Delivery.isActive`:** es una sola columna booleana que
significa "puede recibir pedidos ahora", y la escriben tres actores distintos
sin coordinarse entre sí: (1) el admin con `PATCH /delivery/:id/status`
("habilitado para recibir ofertas"), (2) el propio chofer con
`PATCH /delivery/user/:userId/availability` ("ir en línea"/"desconectarme"), y
(3) el alta (`POST /users` con `isActive`). El panel ya la etiqueta con
honestidad ("Activo"/"Inactivo" en la tabla de choferes, no "En línea"), así
que no hay nada que arreglar del lado del panel — queda anotado por si el back
en algún momento quiere separar "habilitado por el admin" (columna nueva) de
"conectado ahora" (estado efímero, ya existe en Redis GEO vía
`RedisService`).

---

## Choferes y vehículos

| Endpoint | Qué hace el panel | Qué hace la API | Veredicto | Evidencia |
|---|---|---|---|---|
| `GET /delivery` (+ `term`, "Sólo activos") | Pagina con `X-Total-Count`, checkbox "Sólo activos" pega a `/delivery/active` | Ambos endpoints paginan igual (`limit/offset/term`) | OK | `X-Total-Count: 160` en ambos con este seed; el panel lo lee bien. |
| `PATCH /delivery/:id` (`validated`, `isActive`) | Formulario de edición, sólo esos 2 campos | Rechaza cualquier otro campo (400 "property X should not exist") | OK | — |
| `GET /car` | Flota completa sin paginar | El endpoint no pagina (no tiene `Query`/`ApiTotal`) | OK | 16 vehículos en el seed actual, todos devueltos. |
| `useDeliveryOptions()` (select "Chofer asignado" en Vehículos) | **Antes:** `listDeliveries({page:0, pageSize:100}, '')`, comentario "son pocos", sin aviso de corte. **Ahora:** expone `total` y el formulario muestra un aviso si faltan choferes por mostrar | `GET /delivery` pagina; con el seed actual hay 160 choferes, el combo sólo carga 100 (el máximo que acepta la API) | **Panel (mitigado, no resuelto del todo)** | Con 160 choferes, 60 no entran en el `<select>` nativo y no hay forma de tipear para buscarlos: se agregó un aviso honesto ("Se muestran X de Y…") con una vía alternativa (asignar el vehículo desde la ficha del chofer, que sí soporta cualquier chofer). Una solución completa necesita un combobox con búsqueda server-side en el kit — no existe hoy y es un cambio de componente, no de contrato; lo dejo marcado para una tarea aparte. |
| `POST /users` (alta de chofer, `rol:'delivery'`) | `registerUser('delivery', {..., distributorId, validated, isActive})` | `RegistrarUsuarioDto` acepta exactamente esos campos opcionales | OK | — |

---

## Reclamos, incidencias y reservas

| Endpoint | Qué hace el panel | Qué hace la API | Veredicto | Evidencia |
|---|---|---|---|---|
| `GET /claims` | Lista completa, sin paginar | No pagina (130 reclamos en el seed actual, todos vuelven) | OK | — |
| `PATCH /claims/:id/resolve` (`resolution`, `status: resolved\|in_process\|rejected`) | Formulario con esos 3 valores | `ResolveClaimDto` usa `ClaimStatus` con exactamente esos 3 valores | OK | — |
| `GET /incidents` | Lista completa, sin paginar | No pagina | OK | 148 incidencias, todas vuelven. |
| `PATCH /incidents/:id/resolve` (`resolutionNote`) | — | Coincide | OK | — |
| `GET /orders/reservations` | Lista reservas (`RESERVED`) | No pagina | OK | 0 reservas en este momento del seed; probado igual con el DTO. |
| `PATCH /orders/:id/confirm-deposit` | Confirma seña en efectivo | — | OK | — |
| `paymentMethod` en `ReservaResponseDto` | El panel ya lo sabía y lo resolvió con un type guard (`isKnownPaymentMethod`) en `Reservations/components/paymentMethod.ts` | El campo llega tipado como `string` suelto en el Swagger (`@ApiProperty({ example: 'cash' })` sin `enum`), a diferencia de `OrderRecordResponseDto.paymentMethod` que sí usa el enum | **API (pendiente)** | Propuesta: en `splg-app-backend/src/order/dto/order-listados-response.dto.ts:26`, cambiar `@ApiProperty({ example: 'cash' }) paymentMethod!: string;` por `@ApiProperty({ enum: PaymentMethod, example: PaymentMethod.CASH }) paymentMethod!: PaymentMethod;` (mismo patrón que ya usa el DTO de reportes). El panel no necesita cambios: seguiría funcionando igual, sólo se pondría más estricto el tipo generado. |

---

## Clientes, administradores, usuarios

| Endpoint | Qué hace el panel | Qué hace la API | Veredicto | Evidencia |
|---|---|---|---|---|
| `GET /customers` (+ `term`) | Pagina con `X-Total-Count` | Igual | OK | `X-Total-Count: 41`. |
| `PATCH /customers/:id`, `DELETE /customers/:id` | Sólo el administrador general | 403 a un admin de empresa | OK | — |
| `GET /admin` | Lista completa sin paginar | No pagina (90 admins hoy) | OK | — |
| `POST /users` (`rol: admin\|super_admin`) | `createAdmin` | Coincide con `RegistrarUsuarioDto` | OK | — |
| `GET /users` (+ `term`) | Lee `{rows: data.users, total: data.maxUsers}` | `ListadoDeUsuariosDto = {users, maxUsers}` | OK | `maxUsers: 422` con `limit=1`. |
| `PATCH /users/:id`, `/block`, `DELETE /users/:id` | Sólo el administrador general sobre cuentas de cliente (403 a admin de empresa) | Igual, scope por tenant ya resuelto (H-66) | OK | — |
| `GET /users/email/:email` (login: `getAdmin`) | Verifica rol admin/super_admin y `blocked` | Coincide | OK | — |

---

## Catálogo, envases físicos y franjas horarias

| Endpoint | Qué hace el panel | Qué hace la API | Veredicto | Evidencia |
|---|---|---|---|---|
| `GET /gascylinder` (+ `term`) | Lee `{rows: data.gasCylinders, total: data.total}` (total en el CUERPO, no en el header) | `CatalogoDto = {gasCylinders, total}`, sin `X-Total-Count` | OK | Confirmado con `curl`: no hay header de total, sí `total` en el JSON. |
| `PATCH /gascylinder/:id/stock` | Comentario: "suma (+) o resta (–) del stock actual" | `gasCylinder.stock += quantity` (con `BadRequestException` si queda negativo) | OK | — |
| Promociones por cantidad (`discountedPrice`, umbral `quantity`) | "Llevando N u." → aplica si `cantidad >= N` (la de mayor `N` que alcanza) | `OrderPricingService.bestApplicablePromotion`: exactamente `>=`, toma la de mayor `quantity` alcanzada | OK | — |
| `GET /cylinders` (+ `state`), transición, asignación | Espejo de la máquina de estados (`cylinderTransitions.ts`) | `CYLINDER_TRANSITIONS` del back: idéntica | OK | Comparado campo a campo con `cylinder-state.machine.ts`. |
| `GET /time-slot`, `GET /time-slot/availability` | Franjas + cupos por fecha | Coincide | OK | — |

---

## Reportes, calificaciones, auditoría, distribuidoras

| Endpoint | Qué hace el panel | Qué hace la API | Veredicto | Evidencia |
|---|---|---|---|---|
| `GET /reports/sales-by-driver\|product\|payment` | Sin filtro de fecha usa "hoy" (comentario del panel) | Coincide (ventas `DELIVERED`) | OK | — |
| `GET /reports/sales-evolution?granularity=day\|week\|month` | 3 opciones | Rechaza cualquier otro valor con 400 claro | OK | Probado con `granularity=quarter` → 400 "debe ser day, week o month". |
| `GET /ratings/user/:id/summary`, `/user/:id` | `{average, count}` + historial | Coincide | OK | — |
| `GET /audit` (+ filtros) | `{rows: data.items, total: data.total}` | Coincide | OK | — |
| `GET /distributor`, `POST`, `PATCH`, `/current` | CRUD + "empresa activa" | Coincide, incluido el 404 de `/current` sin "Ver como" | OK | — |
| Login (`Firebase` client SDK, no `/auth/login`) | El panel autentica contra Firebase directo y usa el ID token como Bearer | `/auth/login` y `/auth/login/dashboard` existen en el Swagger pero son para otro consumidor (apps); el panel no los llama, y eso es intencional | OK | No es un desajuste: confirmado que el panel nunca referencia esas rutas. |

---

## Fuera de mi alcance, pero con hallazgo para el otro agente (CoverageZones)

`services/api/coverageZones.ts` ya documenta que `CreateCoverageZoneBody`
(generado del Swagger) está mal anotado y por eso se tipa `CreateCoverageZonePayload`
a mano. Al revisar `splg-app-backend/src/coverage-zone/dto/create-coverage-zone.dto.ts`
hoy, el DTO real es bastante más grande que ese tipo a mano:

- No es `surcharge?: number` — son **dos campos**: `surchargeType?: 'fixed'|'percentage'`
  y `surchargeValue?: number`.
- Hay campos que el tipo a mano no contempla: `label?`, `color?` (hex
  `#RRGGBB`), `priority?`, `validFrom?`/`validUntil?` (ISO 8601, con
  validación de que `validUntil` sea posterior).
- `isActive?` sí está bien.

No toqué `coverageZones.ts` ni nada de `src/pages/CoverageZones/**` (fuera de
mi alcance), pero si el formulario de zonas ya está mandando sólo
`name/polygon/surcharge/isActive`, se le están perdiendo recargo por
porcentaje vs. fijo, color, prioridad entre zonas superpuestas y vigencia
temporal — dejo esto para quien esté en esa rama.

---

## Arreglos hechos (lado del panel)

1. **`AssignDriverModal` no mostraba a todos los choferes activos.**
   `listActiveDeliveries()` (en `services/api/orders.ts`) llamaba a
   `GET /delivery/active` sin paginar ni buscar: con el límite por defecto de
   la API (10), sólo se veían los primeros 10 choferes activos de 160. Se
   unificó con la versión paginada de `services/api/deliveries.ts`, se subió
   el `pageSize` al máximo que acepta la API (100) y se agregó un buscador
   (`SearchInput` + `useDebounce`, mismo patrón que el resto del panel) más un
   aviso cuando quedan choferes sin mostrar.
   - `src/services/api/orders.ts`: se borró la función duplicada y el
     comentario muerto que quedó al final del archivo (mencionaba un alias que
     ya no existe; `RecentOrdersWidget` usa `useOrders` desde hace rato).
   - `src/services/queries/orders.ts`: `useActiveDeliveries` ahora acepta
     `search` y usa `listActiveDeliveries` de `deliveries.ts`.
   - `src/pages/Orders/components/AssignDriverModal.tsx`: buscador + aviso de
     "mostrando X de Y".

2. **`NotificationBell` asumía un payload de socket que la API nunca manda.**
   La interfaz `OrderSocketPayload` tenía `customerName` y `address` con un
   `TODO(backend)` pidiendo "ajustar esta interfaz al payload real". El
   payload real (`AdminGateway.notifyAdmins`, visto en
   `update-order-status.use-case.ts`, `create-order.use-case.ts` y
   `cancel-order.use-case.ts`) nunca trae esos dos campos, así que la cláusula
   "de {cliente}" del mensaje nunca se mostraba. Se reemplazó la interfaz por
   la real (`orderId`, `totalAmount`, `reason`) y el mensaje ahora muestra el
   id corto (con `formatShortId`, el mismo util que usa el resto del panel) y
   el monto o el motivo de cancelación.
   - `src/common/components/Navbar/components/NotificationBell.tsx`.

3. **Comentario mentiroso sobre el handshake del socket.**
   `useSocket.ts` decía "TODO(backend): reemplazar por el handshake real
   (JWT/rol) cuando el gateway lo valide. Hoy `auth` viaja como contexto
   informativo nomás." El `AdminGateway` **ya** valida `auth.token` (lo
   decodifica y desconecta al cliente si falta o es inválido); el comentario
   describía un estado viejo del contrato. Se corrigió para reflejar lo que
   realmente hace el back.
   - `src/hooks/useSocket.ts`.

4. **`useDeliveryOptions` (select de "Vehículos") truncaba sin avisar.**
   Mismo patrón que (1) pero en el alta/edición de vehículos: pedía 100
   choferes con el comentario "son pocos", que dejó de ser cierto (160 en el
   seed actual). Como el `<select>` nativo del kit no tiene buscador
   server-side, no se podía aplicar la misma solución que en (1) sin agregar
   un componente nuevo (combobox asíncrono), así que se hizo la mejora
   proporcional: se expone `total` desde el hook y el formulario avisa cuántos
   choferes quedan afuera, con una alternativa real (asignar el vehículo desde
   la ficha del chofer, que no tiene este límite).
   - `src/services/queries/deliveries.ts`, `src/pages/Cars/Cars.tsx`,
     `src/pages/Cars/components/CarFormModal.tsx`.

## Desajustes de API pendientes (propuesta para el back)

1. `ReservaResponseDto.paymentMethod` sin enum — `order-listados-response.dto.ts:26`,
   cambiar `string` por `PaymentMethod`.
2. `MediosDePagoDto` (stats del tablero) no documenta que `cash`/`mercadopago`
   son del **mes en curso** — agregar `description` en
   `order-stats-response.dto.ts`.
3. `RendimientoDto.ordersPerDay` es un duplicado exacto de
   `ordersSummary.deliveredToday`, con un nombre que sugiere una tasa/promedio
   que no calcula — renombrar o calcular un promedio real.
4. `Delivery.isActive` conflacionado (habilitado por admin + "en línea" del
   propio chofer, misma columna) — separar en dos campos si se quiere que
   `activeDeliveries`/`/delivery/active` reflejen "conectado ahora" de verdad.

## No pude probar

- El evento `order:driver-location` en vivo (requiere un chofer real con la
  app moviéndose); se verificó por código que el payload coincide 1 a 1.
- Los flujos de pago online (MercadoPago) de reservas/pedidos: no forman parte
  del contrato panel↔API stricto sentido (el panel no inicia el pago), no se
  ejercitaron.
- No probé el formulario de zonas de cobertura en el navegador (fuera de
  alcance).

## Verificación

- `npm run verify` (typecheck + lint + format:check + colors + test + build):
  **verde**.
- `npx knip`: **sin hallazgos**.
- Levanté el dev server propio (`VITE_APP_API_URL=http://localhost:3100/api
  VITE_APP_SOCKET_URL=http://localhost:3100 npx vite --port 3012`) y confirmé
  que sirve (200, sin errores de arranque), pero no tengo un navegador/Chrome
  disponible en este entorno para hacer clic y ver los cuatro cambios
  visualmente. Los cuatro cambios son chicos, tipados de punta a punta
  (typecheck en verde) y la lógica de datos está cubierta por los tests
  existentes (`npm run test` en verde, 79 tests). Recomiendo abrir una vez el
  modal de asignación manual de Pedidos y el formulario de alta de vehículo
  para confirmar visualmente el aviso de "mostrando X de Y" antes de dar la
  tanda por cerrada.

## Archivos tocados

- `src/services/api/orders.ts`
- `src/services/queries/orders.ts`
- `src/services/queries/deliveries.ts`
- `src/pages/Orders/components/AssignDriverModal.tsx`
- `src/pages/Cars/Cars.tsx`
- `src/pages/Cars/components/CarFormModal.tsx`
- `src/common/components/Navbar/components/NotificationBell.tsx`
- `src/hooks/useSocket.ts`
- `AUDITORIA-CONTRATO.md` (nuevo)
