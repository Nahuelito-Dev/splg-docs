# Auditoría de fidelidad documentación ↔ código — CU-001 a CU-030

**Alcance:** Casos de Uso Expandidos CU-001 … CU-030 de `docs/1-Requisitos.md` (sección 7).
**Método:** adversarial. Cada afirmación sobre el sistema se contrastó contra el código real
(controllers, use-cases, servicios, DTOs, entidades, guards y gateways). Toda referencia lleva
`archivo:línea` verificado.
**Fecha:** 2026-08-30.

> **Hallazgos previos ya confirmados que NO se repiten acá:** la reescritura de CU-013/CU-014
> (oferta secuencial, ventana de 30 s, radios [5,10,15,20], cron de 15 s, sin escalamiento al
> administrador), la secuencia alternativa por QR de CU-020 con el cliente como actor,
> CU-043 no implementado y CU-040 parcial. Lo que se reporta acá sobre CU-013 y CU-014 es
> material distinto del ya cerrado.

---

## Resumen

| CU | Veredicto | Síntesis |
|----|-----------|----------|
| CU-001 | **DISCREPANCIA GRAVE** | El sistema no genera ningún JWT propio (usa el ID token de Firebase) y nunca verifica `validated` del chofer al loguear. |
| CU-002 | **DISCREPANCIA GRAVE** | El registro no devuelve token ni autentica al usuario: retorna la entidad `User`. |
| CU-003 | **FIEL** | Es un puntero a CU-031; el endpoint existe y está restringido a administrador. |
| CU-004 | **DISCREPANCIA GRAVE** | `PATCH /users/me` no existe (es `PATCH /users/:id`) y no hay ninguna de las validaciones que declara. |
| CU-005 | **DISCREPANCIA GRAVE** | El despacho no se dispara con MERCADOPAGO, el recargo del 10 % también aplica a MP, el pedido puede nacer `RESERVED` y faltan tres excepciones reales. |
| CU-006 | DISCREPANCIA MENOR | Ante un pedido ajeno el código responde 404, no el 403 documentado. |
| CU-007 | **FIEL** | Endpoint, filtro por cliente y orden `createdAt DESC` coinciden. |
| CU-008 | **DISCREPANCIA GRAVE** | La cancelación NO es atómica: estado y restitución de stock corren en transacciones separadas. Además responde 400, no 403. |
| CU-009 | **DISCREPANCIA GRAVE** | No se verifica que el chofer sea el asignado; el motivo no es obligatorio ni se guarda; no se dispara re-despacho. |
| CU-010 | DISCREPANCIA MENOR | El motivo es opcional y no se envía push FCM al cliente (solo WebSocket). |
| CU-011 | **DISCREPANCIA GRAVE** | No existe ningún filtro: el listado solo acepta `limit`/`offset`. |
| CU-012 | **DISCREPANCIA GRAVE** | El endpoint es otro, no valida `validated` y no notifica ni al chofer ni al cliente. |
| CU-013 | **DISCREPANCIA GRAVE** | La elegibilidad por `validated`/`isActive` que declara el CU no existe en el código. |
| CU-014 | DISCREPANCIA MENOR | El barrido de pendientes sin oferta está acotado a 50 pedidos y a los de más de 60 s de antigüedad; el CU no lo dice. |
| CU-015 | **DISCREPANCIA GRAVE** | No se verifica `validated`; el push que recibe el cliente es el de creación de pedido, no el de aceptación. |
| CU-016 | **DISCREPANCIA GRAVE** | `Order.rejectedDriverIds[]` no existe; el endpoint no acepta `reason`; no produce 409 ni 410. |
| CU-017 | DISCREPANCIA MENOR | El evento al cliente es `order:driver-location`, no `driver:location`; no se valida rango de coordenadas. |
| CU-018 | **DISCREPANCIA GRAVE** | Cualquier chofer puede pasar a ON_THE_WAY un pedido ajeno: el 403 documentado no existe. Push equivocado. |
| CU-019 | **DISCREPANCIA GRAVE** | No existe el estado `ARRIVED` ni el campo `arrivedAt`; el endpoint es otro, no hay push y no hay control de propiedad. |
| CU-020 | **DISCREPANCIA GRAVE** | En la vía normal cualquier chofer puede entregar un pedido ajeno; push equivocado. (La vía alternativa por QR sí es fiel.) |
| CU-021 | DISCREPANCIA MENOR | El push FCM se envía siempre, no solo con la app en segundo plano. |
| CU-022 | **DISCREPANCIA GRAVE** | El endpoint es otro, no tiene `@Roles` (cualquier usuario autenticado puede desconectar a cualquier chofer) y no reinserta al chofer en el radar al reactivarse. |
| CU-023 | **DISCREPANCIA GRAVE** | No se exige que el pedido esté DELIVERED, no se notifica al administrador y el error es 400, no 403. |
| CU-024 | **DISCREPANCIA GRAVE** | No hay paginación ni filtro por estado ni por fechas. |
| CU-025 | **DISCREPANCIA GRAVE** | No valida que el reclamo esté PENDING, no existe `resolvedAt` y no se notifica al cliente. |
| CU-026 | **DISCREPANCIA GRAVE** | `GET /stats/overview` y `GET /stats/sales-chart` no existen; el KPI de top productos tampoco. |
| CU-027 | **DISCREPANCIA GRAVE** | El endpoint es otro y el reporte no calcula `avgRating` ni `avgDeliveryTime`; no valida el rango de fechas. |
| CU-028 | **DISCREPANCIA GRAVE** | El endpoint es otro y faltan `productId`, `totalDiscounts` y `percentageOfSales`. |
| CU-029 | **DISCREPANCIA GRAVE** | El endpoint es otro, falta `percentageOfTotal` y solo se cuentan pedidos DELIVERED. |
| CU-030 | **DISCREPANCIA GRAVE** | `GET /stats/sales-chart?days=7` no existe; la respuesta no trae `ordersCount` y los nombres de campo son otros. |

**Conteo:** FIEL 2 · DISCREPANCIA MENOR 5 · DISCREPANCIA GRAVE 23 · NO VERIFICABLE 0.

---

## Discrepancias encontradas

### CU-001 — Iniciar Sesión

**Qué dice la documentación**

> Paso 4: «El sistema valida el token de Firebase, consulta el rol del usuario en la base de datos
> y **genera un JWT propio con `userId`, `email` y `role` en el payload**.»
> Paso 5: «El sistema retorna el JWT al cliente.»
> Precondición: «Si es chofer, debe estar validado por el administrador.»
> Excepción paso 3: «Si el usuario Chofer tiene `validated = false`, el sistema informa "Tu cuenta
> aún no fue habilitada por el administrador" y deniega el acceso.»

**Qué hace el código**

- `AuthService.login` (`src/auth/auth.service.ts:43-59`) llama a `signInWithEmailAndPassword` y
  **devuelve tal cual el `UserCredential` de Firebase**. No hay firma de ningún token propio.
- El token que se guarda en la cookie del panel es `creds.user.stsTokenManager.accessToken`, es
  decir el **ID token de Firebase** (`src/auth/auth.controller.ts:51-61`).
- El guard de entrada no verifica un JWT propio: llama a `authService.decodeToken`
  (`src/auth/guards/jwt-auth.guard.ts:67`), que delega en `firebaseAuth.verifyIdToken`
  (`src/auth/auth.service.ts:61-75`).
- `@nestjs/jwt` figura en `package.json:39` pero **no se importa en ningún archivo de `src/`**
  (verificado por búsqueda de `JwtService`, `jwt.sign`, `jsonwebtoken` y `@nestjs/jwt`).
- En todo el flujo de login **no se lee `Delivery.validated` en ninguna parte**
  (`src/auth/auth.service.ts:43-93`). La única validación adicional del login de panel es que el
  email corresponda a un administrador (`src/auth/auth.service.ts:77-93`).
- Precondición real no documentada: el guard exige el header `X-Client-Source`
  (`src/auth/guards/jwt-auth.guard.ts:40-44`); sin él el login falla con 401.

**Gravedad:** grave. Un lector concluye que el sistema emite y controla sus propias credenciales
(decisión de arquitectura de seguridad central en una tesis) y que el chofer no validado no puede
entrar. Ninguna de las dos cosas es cierta.

**Corrección propuesta**

> Paso 4: «El sistema valida el ID token emitido por Firebase contra el SDK Admin, resuelve el
> usuario local por email y adjunta a la request su `user_id`, `email`, rol y distribuidora. El
> sistema **no emite un token propio**: la credencial de sesión es el ID token de Firebase.»
> Paso 5: «El cliente conserva el ID token de Firebase y lo envía en `Authorization: Bearer`. El
> panel web además lo recibe en una cookie `httpOnly`.»
> Precondición: «El usuario está registrado y la app envía el header `X-Client-Source` que
> identifica el origen (app cliente / app chofer / panel).»
> Excepción paso 3: eliminar. El estado `validated` del chofer **no** se controla en el login; se
> controla —parcialmente— más adelante, al aceptar pedidos.

---

### CU-002 — Registrarse como Cliente

**Qué dice la documentación**

> Paso 6: «El sistema genera un JWT y retorna el token. **El usuario queda autenticado
> automáticamente**.»
> Paso 2: «…y contraseña (mínimo 6 caracteres)».
> Paso 3: «El sistema valida el formato de los campos (email válido, **teléfono con formato
> correcto**).»

**Qué hace el código**

- `CustomersService.registerWithUser` termina devolviendo la entidad `User` con sus relaciones
  (`src/customer/customer.service.ts:106-111`). **No genera ni devuelve token alguno**; el cliente
  debe hacer login aparte.
- `CompleteCustomerRegistrationDto` valida `password` solo con `@IsString()` + `@IsNotEmpty()`
  (`src/customer/dto/complete-customer-registration.dto.ts:10-13`): el mínimo de 6 caracteres lo
  impone Firebase, no el backend.
- `phone_number` se valida solo con `@IsString()` + `@IsNotEmpty()`
  (`src/customer/dto/complete-customer-registration.dto.ts:20-23`): no hay validación de formato.

Lo que **sí** es fiel: la comprobación de email duplicado (`src/customer/customer.service.ts:50-56`),
la creación en Firebase (`:58-63`), el alta de `User` con rol `customer` y el perfil `Customer`
(`:65-93`) y el rollback que borra el usuario de Firebase si la transacción falla (`:112-119`).

**Gravedad:** grave. La postcondición «listo para realizar pedidos» sin sesión activa describe un
flujo de app que no es el implementado.

**Corrección propuesta**

> Paso 6: «El sistema persiste el usuario y su perfil `Customer` y devuelve los datos del usuario
> creado. **No se emite sesión**: la app debe ejecutar a continuación el login de CU-001 con las
> mismas credenciales.»
> Paso 2: «…y contraseña. El mínimo de 6 caracteres lo impone Firebase Auth al crear la cuenta.»
> Paso 3: «El sistema valida que los campos no estén vacíos y que el email tenga formato válido. El
> teléfono se acepta como texto libre.»
> Postcondición: «Existe un nuevo usuario con rol CLIENTE y perfil Customer. El usuario **aún no
> tiene sesión**.»

---

### CU-004 — Gestionar Perfil de Usuario

**Qué dice la documentación**

> Paso 4: «La app envía `PATCH /users/me` con los campos modificados.»
> Paso 5: «El backend valida los datos: nombre no vacío, teléfono con formato válido.»
> Excepciones: «Si el formato del teléfono es inválido → 400 "Formato de teléfono inválido."» ·
> «Si el nombre está vacío → 400 "El nombre es requerido."»

**Qué hace el código**

- **No existe ninguna ruta `me`** en todo el proyecto (búsqueda de `@Get('me'`, `@Patch('me'` y
  `users/me` sin resultados). La actualización de perfil es `PATCH /users/:id`
  (`src/users/users.controller.ts:160-188`).
- El control de propiedad se hace comparando el `:id` de la URL con el del token
  (`src/users/users.controller.ts:176-178`) y se aplica una whitelist de campos autoeditables
  `full_name`, `phone_number`, `selfie` (`src/users/users.controller.ts:191-204`) — mecanismo real
  que el CU no menciona.
- `UpdateUserDto` es `PartialType(CreateUserDto)` (`src/users/dto/update-user.dto.ts:1-4`), y en
  `CreateUserDto` tanto `full_name` como `phone_number` son `@IsOptional() @IsString()`
  (`src/users/dto/create-user.dto.ts:18-32`). **Ninguna de las dos excepciones documentadas puede
  ocurrir**: un nombre vacío y un teléfono con cualquier formato pasan la validación.

**Gravedad:** grave. El endpoint documentado no existe, y las dos únicas excepciones del CU son
inalcanzables.

**Corrección propuesta**

> Paso 4: «La app envía `PATCH /users/:id` con el id del propio usuario y los campos modificados.»
> Paso 5: «El backend verifica que el usuario solo se modifique a sí mismo (salvo administrador) y
> descarta todo campo fuera de la whitelist `full_name`, `phone_number`, `selfie`.»
> Excepciones: «Si el `:id` no es el del usuario autenticado y este no es administrador → 403 "No
> podés modificar a otro usuario". Si el usuario no existe → 404.» (Eliminar las dos excepciones de
> formato: no están implementadas.)

---

### CU-005 — Crear Pedido

**Qué dice la documentación**

> Paso 5: «Si elige TRANSFERENCIA, el sistema muestra **el recargo del 10 %**.»
> Paso 7: «…aplica recargo **si TRANSFER**…»
> Paso 10: «El sistema dispara el algoritmo de despacho automático (CU-013).»
> Postcondición: «Existe un pedido con estado PENDING. … **Los choferes cercanos fueron notificados
> por WebSocket**.»
> Excepción paso 10: «Si no hay choferes en el radio de 5 km, el sistema **notifica al cliente
> "Buscando repartidor disponible…"**.»

**Qué hace el código**

1. **El recargo también aplica a MercadoPago.** `applyPaymentSurcharge` multiplica por 1.1 cuando el
   método es `MERCADOPAGO` **o** `TRANSFER` (`src/order/domain/order-pricing.service.ts:61-69`); la
   constante se llama `ONLINE_SURCHARGE_FACTOR` (`:32`).
2. **Con MERCADOPAGO el despacho NO se dispara.** El pedido se crea, se reserva el stock y se genera
   el checkout, pero `offerToNextDriver` solo se llama en la rama `else`
   (`src/order/application/create-order.use-case.ts:282-297`). El despacho queda a cargo del webhook
   de pago.
3. **El pedido puede nacer `RESERVED`, no PENDING**, cuando `isReservation` es verdadero
   (`src/order/application/create-order.use-case.ts:236-245`), y en ese caso tampoco se despacha
   (`:266-281`).
4. **Nunca se notifica al cliente "Buscando repartidor disponible…".** Si no hay candidato,
   `offerToNextDriver` solo escribe un log de debug y retorna `null`
   (`src/order/application/dispatch-orchestrator.service.ts:58-63`).
5. **Excepciones reales que el CU no documenta:**
   - Dirección fuera de la zona de cobertura → 400 "La dirección está fuera de la zona de cobertura
     de la distribuidora" (`src/order/application/create-order.use-case.ts:139-151`), con recargo por
     zona sumado al total (`:150`, `:221`).
   - Garrafa de otra distribuidora → 400 (`src/order/application/create-order.use-case.ts:184-191`).
   - Franja horaria sin cupo: se valida dentro de la transacción con lock pesimista
     (`src/order/application/create-order.use-case.ts:156-163`).
   - Reserva sin `scheduledDate` → 400 (`:102-106`).
6. **Actor.** `POST /orders` no declara `@Roles` (`src/order/order.controller.ts:71-114`) y el
   `RolesGuard` deja pasar cuando no hay metadata (`src/common/guards/roles.guard.ts:40-42`): también
   un administrador o un chofer pueden crear pedidos a nombre de un cliente (`order.controller.ts:92-101`).

**Gravedad:** grave. El punto 2 es el más serio: la documentación afirma que todo pedido se despacha
al crearse, y en el método de pago online eso no ocurre — un lector no entendería por qué un pedido
pagado por MercadoPago queda sin chofer.

**Corrección propuesta**

> Paso 5: «Selecciona el método de pago. Si elige **MERCADOPAGO o TRANSFERENCIA**, el sistema aplica
> un recargo del 10 % sobre el total (los pagos en efectivo no tienen recargo).»
> Paso 7: «…aplica el recargo por zona de cobertura si la distribuidora lo definió y el recargo del
> 10 % si el pago es online…»
> Paso 10: «Si el pago es en efectivo o por transferencia, el sistema dispara el despacho automático
> (CU-013). **Si el pago es por MercadoPago, el pedido no se ofrece a ningún chofer hasta que el
> webhook confirme el cobro (CU-05x); si el pedido es una pre-reserva, el despacho lo dispara el
> proceso temporal el día agendado.**»
> Postcondición: «Existe un pedido con estado PENDING —o RESERVED si es una pre-reserva—. El stock
> fue decrementado atómicamente. **Se abrió una oferta a un único chofer** (ver CU-013), salvo en
> los casos de pago online y pre-reserva.»
> Excepciones (agregar): «Si la dirección cae fuera de la zona de cobertura de la distribuidora, el
> sistema rechaza el pedido antes de reservar stock.» · «Si alguna garrafa no pertenece a la
> distribuidora elegida, el sistema rechaza el pedido.» · «Si la franja horaria elegida no tiene
> cupo para esa fecha, el sistema rechaza el pedido.»
> Excepción paso 10 (reemplazar): «Si no hay choferes elegibles en ningún paso de radio, el pedido
> queda pendiente sin oferta y el proceso temporal de CU-014 lo reintenta. **El cliente no recibe
> aviso de esta situación.**»

---

### CU-006 — Consultar Detalle de Pedido

**Qué dice la documentación**

> Excepción paso 2: «Si el cliente intenta ver un pedido que no le pertenece, el sistema retorna
> **error 403 "No autorizado"**.»

**Qué hace el código**

`OrderService.getOne` lanza `NotFoundException` —404— tanto si el pedido es de otra distribuidora
como si es de otro cliente, deliberadamente para no revelar su existencia
(`src/order/order.service.ts:94-106`).

**Gravedad:** menor. La decisión del código es la correcta desde seguridad; solo el código de estado
documentado está mal.

**Corrección propuesta**

> Excepción paso 2: «Si el cliente intenta ver un pedido que no le pertenece —o de otra
> distribuidora—, el sistema retorna **404**, sin distinguirlo de un pedido inexistente, para no
> revelar la existencia del recurso.»

---

### CU-008 — Cancelar Pedido (Cliente)

**Qué dice la documentación**

> Paso 4: «**Inicia una transacción**: actualiza el estado del pedido a CANCELLED con el motivo, **y**
> por cada OrderItem devuelve la cantidad al stock…»
> Paso 5: «Hace commit de la transacción.»
> Postcondición: «…El stock de todos los ítems fue restituido al inventario **dentro de una
> transacción atómica**.»
> Excepción paso 3: «Si el pedido no pertenece al cliente autenticado, el sistema retorna **error 403**.»

**Qué hace el código**

- Son **dos unidades de trabajo distintas**: `restoreStock` abre su propio `QueryRunner`, restituye y
  **hace commit** (`src/order/application/cancel-order.use-case.ts:109-122`); recién después, y fuera
  de esa transacción, se persiste el pedido cancelado con
  `await this.orders.save(order)` (`src/order/application/cancel-order.use-case.ts:69`). Si ese
  guardado falla, el stock ya volvió al inventario y el pedido sigue activo: stock duplicado.
- El pedido ajeno se rechaza con `BadRequestException('No autorizado')` → **400, no 403**
  (`src/order/application/cancel-order.use-case.ts:98-100`).
- Además, el orden de las comprobaciones es inverso al documentado: primero se evalúa
  `ON_THE_WAY` y recién después la pertenencia (`src/order/application/cancel-order.use-case.ts:92-101`),
  de modo que un cliente que intenta cancelar un pedido ajeno en camino recibe «El pedido ya está en
  camino» en lugar de «No autorizado».
- El aviso al chofer previo es solo por WebSocket (`:146-151`); **no hay push FCM** en este caso de uso.

**Gravedad:** grave. La atomicidad de la restitución de stock es una propiedad que la tesis afirma
explícitamente y que el código no garantiza.

**Corrección propuesta**

> Paso 4: «El sistema marca el pedido como CANCELLED con su motivo y, **en una transacción propia con
> lock pesimista sobre cada garrafa**, devuelve al inventario la cantidad de cada `OrderItem`.»
> Paso 5: «El sistema persiste el pedido cancelado. **La restitución de stock y el guardado del
> pedido son operaciones separadas: no comparten transacción.**»
> Paso 6: «Si había chofer asignado, se le emite `order:cancelled` por WebSocket.» (quitar el push FCM)
> Postcondición: «El pedido tiene estado CANCELLED. El stock de todos los ítems fue restituido con
> lock pesimista. **La consistencia entre ambos efectos no está protegida por una transacción
> única** (pendiente registrado en el Documento 3).»
> Excepción paso 3: «Si el pedido no pertenece al cliente autenticado, el sistema retorna **400 "No
> autorizado"**. La comprobación de estado ON_THE_WAY se evalúa **antes** que la de pertenencia.»

---

### CU-009 — Cancelar Pedido (Chofer)

**Qué dice la documentación**

> Precondición: «El chofer está autenticado. El pedido está en estado ACCEPTED **y el chofer es el
> asignado**.»
> Paso 2: «Ingresa **obligatoriamente** un motivo.»
> Paso 5: «El sistema dispara nuevamente CU-013 para buscar otro chofer disponible.»

**Qué hace el código**

- La rama `driver` de `applyCancellationPolicy` **no compara al usuario autenticado con
  `order.delivery_id`**: pasa el pedido a PENDING, lo desasigna y limpia los timestamps sin ninguna
  verificación de propiedad (`src/order/application/cancel-order.use-case.ts:84-90`). Cualquier
  chofer autenticado puede liberar el pedido de otro chofer.
- El motivo es **opcional** en el DTO (`src/order/dto/cancel-order.dto.ts:15-18`) y además, para el
  actor chofer, **se descarta**: `cancellationReason` solo se escribe si hay restitución de stock,
  cosa que la rama `driver` no hace (`src/order/application/cancel-order.use-case.ts:61-63`, `:89`).
- **No se dispara ningún re-despacho.** El caso de uso solo emite `order:searching-driver` al cliente
  (`src/order/application/cancel-order.use-case.ts:136-141`); `CancelOrderUseCase` ni siquiera inyecta
  el `DispatchOrchestratorService` (constructor en `:31-36`). El pedido vuelve a circular recién en el
  siguiente tick del cron (`src/order/dispatch.service.ts:31-46`), es decir hasta ~15 s después y,
  por la antigüedad mínima, solo si tiene más de 60 s (`src/order/dispatch.service.ts:23`, `:54-58`).
- La máquina de estados permite también `ON_THE_WAY → PENDING`
  (`src/order/domain/order-status.machine.ts:30-34`), o sea que la precondición «está en estado
  ACCEPTED» es más restrictiva que el código.

**Gravedad:** grave. Un lector cree que existe un control de propiedad que no existe, y que el
re-despacho es inmediato cuando en realidad depende del cron.

**Corrección propuesta**

> Precondición: «El chofer está autenticado. El pedido está en estado ACCEPTED **u ON_THE_WAY**.
> **El sistema no verifica que el chofer que libera el pedido sea el asignado** (falencia registrada
> en el Documento 3).»
> Paso 2: «Puede ingresar un motivo. **Para este actor el motivo no se persiste**: el pedido vuelve
> al circuito sin razón de cancelación.»
> Paso 5: «El sistema avisa al cliente con el evento `order:searching-driver`. **El re-despacho no
> es inmediato**: el pedido queda pendiente sin oferta y lo retoma el proceso temporal de CU-014 en
> su siguiente ejecución.»

---

### CU-010 — Cancelar Pedido (Administrador)

**Qué dice la documentación**

> Paso 2: «Ingresa **obligatoriamente** el motivo de cancelación.»
> Paso 5: «Notifica al cliente por **FCM push**: "Tu pedido fue cancelado por el operador…"»

**Qué hace el código**

- `reason` es opcional (`src/order/dto/cancel-order.dto.ts:15-18`); si falta, se guarda el literal
  `Cancelado por admin` (`src/order/application/cancel-order.use-case.ts:62`).
- La notificación es **solo WebSocket** (`notifyCustomer` con `order:cancelled`,
  `src/order/application/cancel-order.use-case.ts:143`, adaptador en
  `src/order/infrastructure/realtime-dispatch.adapter.ts:41-43`). `CancelOrderUseCase` no inyecta
  ningún puerto de notificación push (constructor en `:31-36`).
- Existe además un segundo endpoint no documentado que cancela: `DELETE /orders/:id`
  (`src/order/order.controller.ts:371-384`), «Cancel order (Admin Force)».

**Gravedad:** menor. El circuito y el estado final son correctos; falla el canal de aviso y la
obligatoriedad del motivo.

**Corrección propuesta**

> Paso 2: «Puede ingresar el motivo de cancelación. Si lo omite, el sistema registra "Cancelado por
> admin".»
> Paso 5: «Notifica al cliente **por WebSocket** (`order:cancelled`) con el motivo. **No se envía
> push FCM.**»
> Comentarios (agregar): «El panel dispone de dos vías equivalentes: `PATCH /orders/:id/cancel` y
> `DELETE /orders/:id` (cancelación forzada).»

---

### CU-011 — Listar Todos los Pedidos

**Qué dice la documentación**

> Paso 3: «El administrador puede **filtrar por: estado del pedido, rango de fechas (startDate /
> endDate), chofer asignado**.»

**Qué hace el código**

`OrderController.findAll` recibe un `PaginationDto` (`src/order/order.controller.ts:116-130`) que
solo declara `limit`, `offset`, `role`, `page` y `term`
(`src/common/dtos/pagination.dto.ts:4-29`). `OrderService.findAll` desestructura únicamente
`limit` y `offset` (`src/order/order.service.ts:72-75`) y el adaptador arma el `where` solo con
`distributor_id` (`src/order/infrastructure/order.typeorm.repository.ts:50-63`). **Ninguno de los
tres filtros existe.** Lo que sí es fiel es el orden `createdAt DESC` (`:60`) y el scope por
distribuidora (`src/order/order.controller.ts:117`, `:122-125`).

**Gravedad:** grave: es la funcionalidad central que el paso describe.

**Corrección propuesta**

> Paso 3: «El listado admite únicamente paginación (`limit`, `offset`) y queda acotado a la
> distribuidora del administrador. **El filtrado por estado, rango de fechas o chofer asignado no
> está implementado** y se registra como pendiente en el Documento 3.»

---

### CU-012 — Asignar Chofer Manualmente

**Qué dice la documentación**

> Precondición: «…Existe al menos un chofer con `validated = true` y `isActive = true`.»
> Paso 3: «El sistema muestra el listado de choferes con `validated = true` y `isActive = true`.»
> Paso 5: «El backend ejecuta **`POST /orders/:id/assign-driver`** con `{ driverId }`.»
> Paso 7: «**Notifica al chofer asignado** por WebSocket (`order:assigned`) y FCM push.»
> Paso 8: «**Notifica al cliente** por WebSocket (`order:accepted`) con datos del chofer.»

**Qué hace el código**

- El endpoint real es **`PATCH /orders/:id/assign/:deliveryId`**, con el chofer en la URL y sin body
  (`src/order/order.controller.ts:331-344`). No existe ninguna ruta `assign-driver`.
- `OrderService.assignDelivery` valida que el repartidor exista y que `isActive` sea verdadero, pero
  **no consulta `validated`** (`src/order/order.service.ts:186-199`).
- **No hay ninguna notificación**: el método asigna, transiciona a ACCEPTED, guarda y retorna
  (`src/order/order.service.ts:194-198`). No se emite `order:assigned` ni `order:accepted`, ni push.
- Tampoco se genera el `deliveryCode` que sí genera la aceptación por parte del chofer
  (`src/order/application/update-order-status.use-case.ts:125`): un pedido asignado a mano queda sin
  código de entrega, y por lo tanto **la confirmación por QR de CU-020 es imposible sobre él**.

**Gravedad:** grave. Endpoint inexistente, control de habilitación inexistente y los dos pasos de
notificación son ficción.

**Corrección propuesta**

> Precondición: «…Existe al menos un chofer con `isActive = true`. **El sistema no comprueba
> `validated` en esta operación.**»
> Paso 5: «El panel ejecuta `PATCH /orders/:id/assign/:deliveryId`.»
> Paso 6: «El sistema verifica que el repartidor exista y esté activo, le asigna el pedido y lo pasa
> a ACCEPTED registrando `acceptedAt`.»
> Pasos 7 y 8 (reemplazar por uno solo): «**La asignación manual no emite avisos**: ni el chofer ni
> el cliente reciben notificación por WebSocket ni push. **Tampoco se genera el código de entrega**,
> por lo que un pedido asignado manualmente no puede cerrarse por la vía del QR (CU-020, secuencia
> alternativa).»
> Postcondición: «El pedido tiene estado ACCEPTED con el chofer seleccionado. **Nadie fue
> notificado.**»

---

### CU-013 — Ofrecer el Pedido al Chofer Más Cercano

> *(La mecánica de oferta secuencial ya fue auditada y reescrita; lo que sigue es un hallazgo
> distinto, sobre la elegibilidad del chofer.)*

**Qué dice la documentación**

> Precondición: «Al menos un chofer de la misma distribuidora está **activo** con su posición
> registrada.»
> Comentarios: «**Solo son elegibles los choferes habilitados por el administrador y activos en ese
> momento.**»

**Qué hace el código**

La búsqueda de candidatos consulta el índice GEO de Redis y lo filtra **únicamente por
distribuidora**: `findNearestAvailable` llama a `findNearbyDrivers`
(`src/order/application/dispatch-orchestrator.service.ts:158-171`) y a `filterByDistributor`, cuyo
`where` es solo `{ user_id: In(driverIds), distributor_id }`
(`src/order/application/dispatch-orchestrator.service.ts:178-189`). **Ni `validated` ni `isActive`
aparecen en la consulta.** La única forma de salir del radar es el borrado explícito por el toggle
de disponibilidad (`src/delivery/delivery.service.ts:261-267`) o la desconexión del socket
(`src/gateways/drivers.gateway.ts:58-73`). En consecuencia, un chofer con `validated = false` que
emita su GPS recibe ofertas de pedidos.

**Gravedad:** grave. La habilitación por parte del administrador es la garantía que sostiene CU-031
y CU-032; el CU afirma que el despacho la respeta y el código no la consulta.

**Corrección propuesta**

> Precondición: «Al menos un chofer de la misma distribuidora tiene su posición registrada en el
> radar.»
> Comentarios (reemplazar la frase): «**La elegibilidad se resuelve por presencia en el radar y
> pertenencia a la distribuidora: el despacho no consulta `validated` ni `isActive`.** Un chofer sale
> del radar al apagar su disponibilidad o al desconectarse; un chofer no habilitado que emita GPS
> puede recibir ofertas. Cerrar esa brecha es un pendiente registrado en el Documento 3.»

---

### CU-014 — Vencer la Oferta y Ofrecer al Siguiente Chofer

**Qué dice la documentación**

> Paso 6: «**Recorre además los pedidos pendientes** que no tienen ninguna oferta vigente y les abre
> una, sin pisar las ofertas en curso.»

**Qué hace el código**

`bootstrapPendingWithoutOffer` toma **como máximo 50 pedidos por tick**
(`src/order/dispatch.service.ts:50-53`) y **descarta los creados hace menos de 60 segundos**
(`MIN_AGE_MS`, `src/order/dispatch.service.ts:22-23`, `:54-57`). Además todo el tick corre bajo un
lock distribuido de Redis con TTL de 12 s, de modo que solo una instancia lo ejecuta
(`src/order/dispatch.service.ts:33-36`).

**Gravedad:** menor. La mecánica es la documentada; faltan dos acotaciones que importan para el
análisis de escala.

**Corrección propuesta**

> Paso 6: «Recorre además hasta **50** pedidos pendientes sin oferta vigente **y con más de 60
> segundos de antigüedad** —los recién creados ya fueron ofrecidos por CU-005— y les abre una oferta
> sin pisar las en curso.»
> Comentarios (agregar): «Cada ejecución toma un lock distribuido en Redis (TTL 12 s), de modo que
> con varias instancias del backend solo una procesa el tick.»

---

### CU-015 — Aceptar Pedido

**Qué dice la documentación**

> Precondición: «…El chofer tiene `isActive = true` **y `validated = true`**.»
> Paso 4: «El sistema verifica que el chofer está activo **y validado**.»
> Paso 7: «El sistema envía una notificación FCM push al cliente: "**¡Tu pedido fue aceptado por
> [nombre del chofer]!**"»
> Excepción paso 4: «Si el chofer tiene `isActive = false` **o `validated = false`**, el sistema
> retorna error 400.»

**Qué hace el código**

- La rama ACCEPTED comprueba que el repartidor exista y que `isActive` sea verdadero
  (`src/order/application/update-order-status.use-case.ts:105-117`). **`validated` no se lee.**
- El push que recibe el cliente es siempre el de **confirmación de creación**: `notifyCustomer` llama
  a `sendOrderConfirmation` (`src/order/application/update-order-status.use-case.ts:235`), cuyo texto
  fijo es «¡Pedido Confirmado! / Tu pedido #xxxxxxxx ha sido creado exitosamente.»
  (`src/notifications/notifications.service.ts:75-85`). Existe un método
  `sendOrderStatusUpdate` con los mensajes por estado que el CU cita
  (`src/notifications/notifications.service.ts:96-136`), pero **no lo invoca nadie** (búsqueda de
  `sendOrderStatusUpdate` en `src/`: única aparición, su propia declaración).

Lo que sí es fiel: transición validada por la máquina de estados (`:70`), asignación del chofer y
`acceptedAt` (`:119-120`), evento `order:accepted` con nombre y teléfono del chofer (`:28`, `:206-217`)
y el cierre de la oferta de despacho (`:129-131`).

**Gravedad:** grave. El control de habilitación del chofer —requisito funcional del subsistema de
choferes— no existe en el punto donde el CU dice que se aplica, y el mensaje que le llega al cliente
es engañoso («tu pedido ha sido creado» cuando lo que pasó fue una aceptación).

**Corrección propuesta**

> Precondición: «…El chofer tiene `isActive = true`. **El sistema no verifica `validated` al aceptar.**»
> Paso 4: «El sistema verifica que el repartidor exista y esté activo.»
> Paso 7: «El sistema envía al cliente una notificación FCM push genérica de pedido ("¡Pedido
> Confirmado!"). **El texto no distingue el estado alcanzado**: el mensaje específico por estado está
> implementado pero no se usa.»
> Excepción paso 4: «Si el chofer no existe → 404. Si tiene `isActive = false` → 400 "El repartidor
> no está activo". **Un chofer con `validated = false` puede aceptar pedidos.**»

---

### CU-016 — Rechazar / Ignorar Pedido

**Qué dice la documentación**

> Paso 3: «La app envía `POST /orders/:id/reject` con `{ reason }` (opcional).»
> Paso 4: «El backend registra el rechazo en **`Order.rejectedDriverIds[]`** para no reintentarle al
> mismo chofer.»
> Paso 6: «**`DispatchService`** busca el siguiente chofer cercano excluyendo los ya rechazados.»
> Precondición: «El chofer recibió un evento **`order:new`** por WebSocket o FCM.»
> Excepciones: «Si el pedido ya fue aceptado por otro chofer → **409** "El pedido ya fue tomado."» ·
> «Si el pedido fue cancelado → **410** "El pedido ya no está disponible."»

**Qué hace el código**

- El endpoint **no recibe body alguno**: la firma es `rejectOffer(@CurrentUser() user, @Param('id') id)`
  (`src/order/order.controller.ts:265-280`). No hay `reason`.
- **El campo `Order.rejectedDriverIds` no existe.** La entidad `Order` no lo declara
  (`src/order/entities/order.entity.ts:52-209`, revisada completa) y no aparece en ningún archivo de
  `src/`. La exclusión de choferes ya contactados se hace contra la **tabla de ofertas**:
  `findOfferedDriverIds` (`src/order/application/dispatch-orchestrator.service.ts:47-49`) y el
  `exclude` de `findNearestAvailable` (`:158-171`). El rechazo se materializa cerrando la oferta con
  estado `REJECTED` (`:136-145`).
- La clase que busca al siguiente chofer es **`DispatchOrchestratorService`**
  (`src/order/application/dispatch-orchestrator.service.ts:23`). `DispatchService`
  (`src/order/dispatch.service.ts:19`) es solo el reloj del cron.
- **No se producen 409 ni 410.** Si el pedido no existe, el servicio retorna `{ rejected: false }`
  (`src/order/order.service.ts:57-62`); si ya fue tomado o cancelado, `onDriverRejected` cierra la
  oferta y `isReofferable` corta silenciosamente
  (`src/order/application/dispatch-orchestrator.service.ts:136-150`), devolviendo 200.
- El evento que recibe el chofer se llama **`server:new-order-request`**
  (`src/gateways/drivers.gateway.ts:128-136`), no `order:new`.

**Gravedad:** grave. El paso 4 describe un mecanismo de persistencia que no existe, y es justamente
el que sostiene la propiedad «no se le vuelve a ofrecer al mismo chofer».

**Corrección propuesta**

> Precondición: «El chofer recibió el evento `server:new-order-request` por WebSocket, o el push
> complementario. El pedido está en estado PENDING.»
> Paso 3: «La app envía `POST /orders/:id/reject`. **La solicitud no lleva cuerpo**: el chofer sale
> del token.»
> Paso 4: «El backend cierra la oferta activa de ese chofer con estado RECHAZADA **en la tabla de
> ofertas de despacho**. Esa tabla es la que impide volver a ofrecerle el mismo pedido.»
> Paso 6: «El `DispatchOrchestratorService` busca de inmediato el siguiente chofer más cercano,
> excluyendo a todos los que ya tienen una oferta registrada para ese pedido.»
> Excepciones (reemplazar): «Si el pedido ya fue aceptado por otro chofer o fue cancelado, la
> operación **es un no-op silencioso que responde 200**: se cierra la oferta y no se re-ofrece. El
> sistema no devuelve 409 ni 410.»

---

### CU-017 — Actualizar Ubicación GPS del Chofer

**Qué dice la documentación**

> Paso 5: «…el sistema emite **`driver:location`** al cliente por el `CustomersGateway`…»
> Excepción paso 2: «Si lat o lng son inválidos (nulos **o fuera de rango**), el servidor registra el
> error y descarta el evento silenciosamente.»

**Qué hace el código**

- El evento emitido al cliente es **`order:driver-location`** (`src/gateways/drivers.gateway.ts:119-123`),
  y en paralelo el mismo payload va al panel con `order:driver-location`
  (`src/gateways/drivers.gateway.ts:124`) — este segundo destinatario el CU no lo menciona.
- La validación es solo de nulos: `if (!data.userId || data.lat == null || data.lng == null)`
  (`src/gateways/drivers.gateway.ts:93-96`). **No hay control de rango**: una latitud de 900 se
  escribe en Redis.
- El disparador del reenvío no es «el pedido está en ON_THE_WAY» sino la existencia de un mapeo
  chofer→pedido en Redis, que se crea al pasar a ON_THE_WAY y se borra al entregar
  (`src/gateways/drivers.gateway.ts:110-111`;
  `src/order/application/update-order-status.use-case.ts:146-151`, `:161-167`) — equivalente en la
  práctica, pero conviene decirlo.
- El nombre de la llave GEO sí coincide: `drivers:locations`
  (`src/redis/redis.service.ts:164-171`), aunque el método se llama `updateDriverLocation`, no
  `geoAdd`, y el miembro es el `userId`.
- **Observación adversarial no documentada:** el `userId` se toma del cuerpo del mensaje
  (`src/gateways/drivers.gateway.ts:88-99`) y no de la identidad del socket autenticado en
  `handleConnection` (`:36-56`). Un chofer conectado puede escribir la posición de otro.

**Gravedad:** menor en lo documental (nombres y validaciones), aunque la observación de suplantación
merece pasar al Documento 3.

**Corrección propuesta**

> Paso 5: «Si el chofer tiene un pedido en curso, el sistema emite **`order:driver-location`** al
> cliente de ese pedido y al panel de administración. El vínculo chofer→pedido se registra en Redis
> al pasar a ON_THE_WAY y se borra al confirmar la entrega.»
> Excepción paso 2: «Si falta el identificador del chofer o alguna coordenada es nula, el servidor
> registra el error y descarta el evento. **No se valida que las coordenadas estén dentro de rango.**»
> Comentarios (agregar): «El identificador del chofer viaja en el mensaje y no se contrasta con la
> identidad del socket; cerrar esa brecha es un pendiente registrado en el Documento 3.»

---

### CU-018 — Marcar Pedido "En Camino"

**Qué dice la documentación**

> Precondición: «El pedido tiene estado ACCEPTED. **El chofer autenticado es el asignado al pedido.**»
> Paso 5: «Envía notificación FCM push al cliente: "**¡Tu pedido está en camino!**"»
> Excepción paso 2: «Si el chofer **no es el asignado** al pedido, el sistema retorna **error 403**.»

**Qué hace el código**

- El controller entrega el `user_id` del chofer como `deliveryId`
  (`src/order/order.controller.ts:254-261`), pero en la rama `ON_THE_WAY` del use-case **ese
  parámetro no se usa nunca**: el código lee `order.delivery_id` para buscar al chofer del pedido y
  arrancar el tracking (`src/order/application/update-order-status.use-case.ts:136-153`). El
  parámetro `deliveryId` solo interviene en la rama ACCEPTED (`:97-134`). **No existe ninguna
  comparación entre el chofer autenticado y el asignado**, de modo que cualquier chofer puede poner
  en camino el pedido de otro. El 403 documentado es inalcanzable.
- El push es el genérico de creación (`sendOrderConfirmation`,
  `src/order/application/update-order-status.use-case.ts:235`;
  `src/notifications/notifications.service.ts:75-85`), no «¡Tu pedido está en camino!».

Sí es fiel: la transición ACCEPTED→ON_THE_WAY validada (`src/order/domain/order-status.machine.ts:23-27`),
`onTheWayAt` (`:137`) y el evento `order:on-the-way` (`:29`).

**Gravedad:** grave. Es un control de autorización que la documentación afirma y el código no tiene.

**Corrección propuesta**

> Precondición: «El pedido tiene estado ACCEPTED.»
> Paso 5: «Envía al cliente el push FCM genérico de pedido. **El texto no es específico del estado.**»
> Excepciones (reemplazar): «Si el pedido no está en ACCEPTED, el sistema retorna 400 "Transición de
> estado no permitida". **El sistema no verifica que el chofer que dispara la transición sea el
> asignado**: cualquier usuario con rol chofer puede avanzar el estado de cualquier pedido (falencia
> registrada en el Documento 3).»

---

### CU-019 — Avisar Llegada al Cliente

**Qué dice la documentación**

> Paso 2: «La app envía `PATCH /orders/:id/status` con `{ status: "ARRIVED" }`.»
> Paso 3: «El backend **actualiza el estado del pedido a `ARRIVED`** y **registra `arrivedAt = now()`**.»
> Paso 5: «Envía notificación **FCM push** al cliente…»
> Postcondición: «**El pedido tiene estado ARRIVED.**»
> Excepciones: «…Si el chofer no es el asignado al pedido, el sistema retorna **error 403**.»

**Qué hace el código**

- **El estado `ARRIVED` no existe.** El enum `OrderStatus` tiene exactamente RESERVED, PENDING,
  ACCEPTED, ON_THE_WAY, DELIVERED y CANCELLED (`src/order/entities/order.entity.ts:21-33`), y la
  máquina de estados lo hace explícito: «los estados ARRIVED y SIN_COBERTURA aún no existen en el
  enum» (`src/order/domain/order-status.machine.ts:15-16`). Enviar `{status:"ARRIVED"}` a
  `PATCH /orders/:id/status` falla en el DTO con 400 (`src/order/dto/update-order-status.dto.ts:19-22`).
- **Tampoco existe la columna `arrivedAt`** (entidad revisada completa,
  `src/order/entities/order.entity.ts:52-209`: solo `acceptedAt`, `onTheWayAt`, `deliveredAt`).
- El endpoint real es **`PATCH /orders/:id/arrived`** (`src/order/order.controller.ts:408-421`), y su
  propia descripción dice «**no cambia el estado del pedido**» (`:414`).
- `notifyDriverArrived` exige que el pedido esté ON_THE_WAY y emite `order:arrived` **solo por
  WebSocket** (`src/order/order.service.ts:322-338`). **No hay push FCM.**
- El handler **no recibe el usuario autenticado** (`src/order/order.controller.ts:419`) y admite rol
  ADMIN además de DELIVERY (`:409`): no hay ninguna verificación de que el chofer sea el asignado, y
  el 403 documentado no puede producirse.

**Gravedad:** grave. El caso de uso describe una transición de estado y un campo de auditoría que el
modelo de datos no tiene; un lector deduciría un ciclo de vida del pedido con seis estados
operativos cuando hay cinco.

**Corrección propuesta**

> Paso 2: «La app envía `PATCH /orders/:id/arrived`.»
> Paso 3: «El backend verifica que el pedido esté en ON_THE_WAY. **El aviso de llegada no es un
> estado del pedido: no cambia `status` ni registra timestamp alguno.**»
> Paso 4: «Emite `order:arrived` al cliente por WebSocket con el nombre del repartidor.»
> Paso 5: eliminar (no hay push FCM).
> Postcondición: «El cliente fue notificado de la llegada. **El pedido sigue en estado ON_THE_WAY.**»
> Excepciones: «Si el pedido no está en ON_THE_WAY → 400 "El pedido debe estar en camino para avisar
> llegada". **El sistema no verifica que quien avisa sea el chofer asignado.**»
> Comentarios (agregar): «Incorporar `ARRIVED` como estado propio y su timestamp es un pendiente
> registrado en el Documento 3.»

---

### CU-020 — Confirmar Entrega (secuencia normal)

> *(La secuencia alternativa por código QR fue verificada y **es fiel**: generación del código al
> aceptar (`src/order/application/update-order-status.use-case.ts:125`), lectura por el chofer con
> control de propiedad (`src/order/order.service.ts:149-170`), confirmación por el cliente con
> control de propiedad, exigencia de ON_THE_WAY, comparación del código e idempotencia
> (`src/order/application/confirm-delivery.use-case.ts:41-71`). Lo que sigue afecta solo a la
> secuencia normal.)*

**Qué dice la documentación**

> Precondición: «El pedido tiene estado ON_THE_WAY. **El chofer autenticado es el asignado.**»
> Paso 6: «Envía notificación FCM push al cliente: "**¡Pedido entregado! Gracias por tu compra.**"»
> Excepción paso 2: «Si el chofer **no es el asignado**, el sistema retorna **error 403**.»

**Qué hace el código**

- Igual que en CU-018: la rama DELIVERED de `applyStatusEffects` **no usa el `deliveryId` del
  llamador** (`src/order/application/update-order-status.use-case.ts:155-189`); solo lee
  `order.delivery_id` para cortar el tracking. **Ningún chequeo de propiedad.** Cualquier chofer
  autenticado puede marcar entregado el pedido de otro —y, si el pago es en efectivo, marcarlo PAID
  (`:157-159`)—. El 403 documentado no existe.
- El push es de nuevo el genérico de creación (`:235`;
  `src/notifications/notifications.service.ts:75-85`).
- Efecto real no documentado: al entregar, el sistema avanza los envases del pedido al estado
  «con el cliente» (`src/order/application/update-order-status.use-case.ts:171-187`).

Sí es fiel: `deliveredAt` (`:156`), CASH→PAID (`:157-159`), evento `order:delivered` (`:30`) y el
rechazo por transición inválida desde estados terminales
(`src/order/domain/order-status.machine.ts:35-36`).

**Gravedad:** grave. Marcar un pedido como entregado y cobrado es la operación de mayor impacto
económico del sistema, y el control de autorización que la documentación promete no está.

**Corrección propuesta**

> Precondición: «El pedido tiene estado ON_THE_WAY.»
> Paso 6: «Envía al cliente el push FCM genérico de pedido.»
> Paso 7 (agregar): «El sistema avanza los envases despachados en el pedido al estado "con el
> cliente" (best-effort: si falla, la entrega no se revierte).»
> Excepciones (reemplazar): «Si el pedido ya está DELIVERED o CANCELLED → 400 por transición
> inválida. **El sistema no verifica que el chofer que confirma sea el asignado**: ese control solo
> existe en la secuencia alternativa por QR, donde se valida contra el cliente dueño del pedido
> (falencia registrada en el Documento 3).»

---

### CU-021 — Recibir Notificaciones en Tiempo Real

**Qué dice la documentación**

> Paso 3: «**Si** la App Cliente está en primer plano y conectada al WebSocket: recibe el evento…»
> Paso 4: «**Si** la App Cliente está cerrada o en segundo plano: el sistema envía una notificación
> FCM push…»
> Paso 1: «Ocurre un evento en el pedido activo del cliente: **creación confirmada**, chofer
> asignado, pedido en camino, chofer llegó, entrega confirmada.»

**Qué hace el código**

Los dos canales son **incondicionales y simultáneos**: en cada cambio de estado se emite el evento
de socket y, acto seguido, se envía el push, sin ninguna consulta sobre el estado de la app
(`src/order/application/update-order-status.use-case.ts:75-83`). El backend no tiene forma de saber
si la app está en primer plano. Además, en la creación del pedido el aviso por socket va **solo al
panel de administración** (`order:created`, `src/order/application/create-order.use-case.ts:302-308`);
al cliente le llega únicamente el push (`:299`).

**Gravedad:** menor. Los avisos llegan; lo que la documentación describe mal es el criterio de
selección del canal.

**Corrección propuesta**

> Paso 3: «El sistema emite **siempre** el evento por WebSocket a la sala del cliente; si la app está
> en primer plano y conectada, actualiza la UI del seguimiento sin recargar.»
> Paso 4: «El sistema envía **además y siempre** el push FCM al token del cliente. **La elección del
> canal la resuelve el dispositivo, no el backend**: este no distingue si la app está abierta.»
> Paso 1 (aclarar): «…**En la creación del pedido el cliente recibe solo el push**; el evento de
> socket de alta va al panel de administración.»

---

### CU-022 — Activar / Desactivar Disponibilidad (Chofer)

**Qué dice la documentación**

> Paso 2: «La app envía **`PATCH /delivery/toggle-availability`**.»
> Paso 4: «Actualiza el campo `isActive` **al valor opuesto**.»
> Paso 6: «Si `isActive` pasa a `true` y tiene posición GPS disponible: **ejecuta `GEOADD` para
> registrarlo en el radar**.»
> Precondición: «El chofer está autenticado **y validado**.»

**Qué hace el código**

- La ruta real es **`PATCH /delivery/user/:userId/availability`** con body `{ available: boolean }`
  (`src/delivery/delivery.controller.ts:165-173`). No existe ninguna ruta `toggle-availability`.
- **No es un toggle**: se asigna el booleano recibido, `delivery.isActive = isAvailable`
  (`src/delivery/delivery.service.ts:257`).
- **No hay re-alta en el radar.** El servicio solo ejecuta el borrado cuando pasa a no disponible
  (`src/delivery/delivery.service.ts:261-267`); la rama `true` no hace nada con Redis. El chofer
  vuelve al radar recién cuando su app emite la siguiente posición GPS
  (`src/gateways/drivers.gateway.ts:101-105`).
- **El endpoint no declara `@Roles` ni verifica identidad** (`src/delivery/delivery.controller.ts:165-173`),
  y el `RolesGuard` deja pasar cuando no hay metadata (`src/common/guards/roles.guard.ts:40-42`):
  **cualquier usuario autenticado —incluido un cliente— puede activar o desactivar a cualquier
  chofer** pasando su `userId`. Tampoco se consulta `validated`
  (`src/delivery/delivery.service.ts:244-275`).

**Gravedad:** grave. Endpoint inexistente, semántica distinta (asignación vs. alternancia), un paso
inventado y una brecha de autorización que la documentación oculta al declarar al chofer como único
actor.

**Corrección propuesta**

> Actor: «Chofer. **En la implementación actual el endpoint no restringe rol ni identidad**:
> cualquier usuario autenticado puede cambiar la disponibilidad de cualquier chofer indicando su
> identificador (falencia registrada en el Documento 3).»
> Precondición: «El chofer está autenticado. **El sistema no verifica `validated` en esta operación.**»
> Paso 2: «La app envía `PATCH /delivery/user/:userId/availability` con `{ available: true|false }`.»
> Paso 4: «Asigna a `isActive` **el valor recibido** (no alterna el actual).»
> Paso 5: «Si pasa a no disponible, elimina al chofer del radar GEO de Redis por su `user_id`.»
> Paso 6 (reemplazar): «Si pasa a disponible, **no se hace nada sobre el radar**: el chofer reingresa
> cuando su app emite la siguiente posición GPS.»

---

### CU-023 — Registrar Reclamo

**Qué dice la documentación**

> Precondición: «El pedido existe, **está DELIVERED** y pertenece al cliente.»
> Paso 6: «Crea el registro `Claim` con estado `PENDING`.»
> Paso 7: «**Notifica al administrador por FCM push** que hay un nuevo reclamo pendiente.»
> Excepción paso 5: «Si el pedido no pertenece al cliente autenticado, el sistema retorna **error
> 403** "No autorizado."»

**Qué hace el código**

- `ClaimsService.create` **no consulta el estado del pedido en ningún momento**
  (`src/claims/claims.service.ts:19-41`): se puede reclamar un pedido PENDING, ACCEPTED o incluso
  CANCELLED.
- El pedido ajeno se rechaza con `BadRequestException` → **400, no 403**
  (`src/claims/claims.service.ts:23-27`).
- **No hay ninguna notificación al administrador**: el servicio crea y guarda el reclamo y termina
  (`src/claims/claims.service.ts:31-40`); el módulo no inyecta ningún servicio de notificaciones
  (constructor en `:14-17`).

Sí es fiel: el estado inicial PENDING por defecto de la entidad
(`src/claims/entities/claim.entity.ts:60-65`), la denormalización de la distribuidora desde el pedido
(`src/claims/claims.service.ts:34`) y la anti-impersonación que fuerza el `customerId` del token
(`src/claims/claims.controller.ts:36-41`).

**Gravedad:** grave. La precondición de pedido entregado es la regla de negocio del caso de uso, y no
existe; el aviso al administrador —que es lo que conecta CU-023 con CU-024— tampoco.

**Corrección propuesta**

> Precondición: «El cliente está autenticado. El pedido existe y pertenece al cliente. **El sistema
> no exige que el pedido esté entregado**: se puede reclamar un pedido en cualquier estado.»
> Paso 7 (reemplazar): «El reclamo queda en la bandeja del administrador. **No se emite ninguna
> notificación**: el administrador lo descubre al consultar el listado (CU-024).»
> Postcondición: «Existe un reclamo con estado PENDING asociado al pedido, al cliente y a la
> distribuidora del pedido. **El administrador no fue notificado.**»
> Excepción paso 5: «Si el pedido no pertenece al cliente indicado → **400** "Esta orden no pertenece
> al cliente indicado".»

---

### CU-024 — Listar Reclamos

**Qué dice la documentación**

> Paso 2: «El sistema ejecuta **`GET /claims?status=&page=` con paginación**.»
> Paso 4: «El administrador puede **filtrar por estado** (PENDING / RESOLVED / REJECTED) **o por
> rango de fechas**.»

**Qué hace el código**

`ClaimsController.findAll` no declara ningún `@Query`: su única entrada es la distribuidora del
contexto (`src/claims/claims.controller.ts:44-49`). `ClaimsService.findAll` arma el `where` solo con
`distributor_id` y devuelve **todos** los reclamos, sin `take` ni `skip`
(`src/claims/claims.service.ts:43-52`). **No hay paginación, ni filtro por estado, ni por fechas.**
Además el enum de estados incluye un cuarto valor, `IN_PROCESS`, que el CU no menciona
(`src/claims/entities/claim.entity.ts:14-19`).

Sí es fiel: el orden `createdAt DESC` (`src/claims/claims.service.ts:49`) y el rol administrador
(`src/claims/claims.controller.ts:45`).

**Gravedad:** grave: los dos pasos operativos del caso de uso describen funciones inexistentes, y la
ausencia de paginación es además un problema de escala que la tesis debería declarar.

**Corrección propuesta**

> Paso 2: «El sistema ejecuta `GET /claims`, **sin parámetros**.»
> Paso 3: «El backend retorna **el listado completo** de reclamos de la distribuidora, ordenado por
> fecha de creación descendente, con el pedido y el cliente asociados.»
> Paso 4 (reemplazar): «**El filtrado por estado o por fechas y la paginación no están
> implementados**; el recorte se resuelve en el panel. Los estados posibles son PENDING, IN_PROCESS,
> RESOLVED y REJECTED. Paginar el listado es un pendiente registrado en el Documento 3.»

---

### CU-025 — Resolver Reclamo

**Qué dice la documentación**

> Paso 4: «…envía `PATCH /claims/:id/resolve` con `{ status, **resolutionNote** }`.»
> Paso 5: «El backend valida que **el reclamo está en PENDING** y que la nota no esté vacía.»
> Paso 6: «Actualiza `Claim.status` y `Claim.resolutionNote` y **registra `resolvedAt = now()`**.»
> Paso 7: «**Envía notificación FCM push al cliente** con el resultado…»
> Excepción paso 5: «Si el reclamo **ya está resuelto** → 400 "El reclamo ya fue procesado."»

**Qué hace el código**

- El campo del cuerpo se llama **`resolution`**, no `resolutionNote`
  (`src/claims/dto/resolve-claim.dto.ts:11-14`; se mapea a `claim.resolutionNote` en
  `src/claims/claims.service.ts:77`).
- **No se valida el estado de partida.** `ClaimsService.resolve` busca el reclamo, escribe nota y
  estado y guarda (`src/claims/claims.service.ts:68-81`): un reclamo ya RESOLVED puede reescribirse
  cuantas veces se quiera. La excepción documentada es inalcanzable.
- **No existe `resolvedAt`.** La entidad `Claim` solo tiene `createdAt`
  (`src/claims/entities/claim.entity.ts:22-72`, revisada completa).
- **No se notifica al cliente**: el servicio no inyecta ningún puerto de notificación
  (`src/claims/claims.service.ts:14-17`).

Sí es fiel: la nota obligatoria y no vacía (`src/claims/dto/resolve-claim.dto.ts:12-13`), el estado
validado contra el enum (`:21-23`), el rol administrador (`src/claims/claims.controller.ts:52`) y el
aislamiento por distribuidora (`src/claims/claims.service.ts:74-75`).

**Gravedad:** grave. Tres de los siete pasos y la única excepción describen comportamiento
inexistente, incluido un campo del modelo de datos.

**Corrección propuesta**

> Paso 4: «…envía `PATCH /claims/:id/resolve` con `{ status, **resolution** }`.»
> Paso 5: «El backend verifica que el reclamo pertenezca a la distribuidora del administrador y que
> la nota no esté vacía. **No verifica el estado de partida.**»
> Paso 6: «Actualiza `Claim.status` y `Claim.resolutionNote`. **No se registra fecha de resolución:
> el modelo no tiene ese campo.**»
> Paso 7 (reemplazar): «**El cliente no recibe ninguna notificación del resultado.**»
> Postcondición: «El reclamo tiene estado RESOLVED, REJECTED o IN_PROCESS con la nota registrada.
> **El cliente no fue notificado.**»
> Excepción paso 5 (reemplazar): «Si la nota está vacía → 400. Si el reclamo no existe o es de otra
> distribuidora → 404. **Un reclamo ya resuelto puede volver a resolverse**: no hay control de
> reprocesamiento (pendiente registrado en el Documento 3).»

---

### CU-026 — Ver Dashboard General

**Qué dice la documentación**

> Paso 2: «El frontend ejecuta **`GET /stats/overview`** en paralelo con **`GET /stats/sales-chart?days=7`**.»
> Paso 3: «Backend **`ReportsService`** calcula: pedidos del día, ventas día/semana/mes, choferes
> activos (con `isActive = true`), **top productos**.»

**Qué hace el código**

- **Ninguna de las dos rutas existe.** Las únicas rutas de estadísticas del proyecto son
  `GET /orders/stats/summary` (`src/order/order.controller.ts:363-369`) y
  `GET /orders/stats/chart` (`src/order/order.controller.ts:441-446`) — búsqueda de `stats` sobre
  todos los `*.controller.ts`, dos resultados.
- El cálculo lo hace **`OrderService.getOrderStats`** (`src/order/order.service.ts:214-307`), no
  `ReportsService`.
- **No hay ningún KPI de top productos.** La respuesta se compone de `ordersSummary`, `sales`,
  `performance` y `paymentMethods` (`src/order/order.service.ts:287-306`).
- El contador de choferes activos exige `isActive = true` **y `validated = true`**
  (`src/order/order.service.ts:264-266`) — más restrictivo que lo documentado.

**Gravedad:** grave. Los endpoints citados no existen y se atribuye el cálculo a un servicio que no
interviene.

**Corrección propuesta**

> Paso 2: «El panel ejecuta `GET /orders/stats/summary` en paralelo con `GET /orders/stats/chart`.»
> Paso 3: «`OrderService.getOrderStats` calcula con agregados SQL, acotado a la distribuidora del
> administrador: pedidos por estado, entregados del día, ventas del día/semana/mes/total, cantidad de
> choferes **activos y validados**, valor promedio de pedido y el reparto entre efectivo y
> MercadoPago del mes.»
> Paso 4: «El backend retorna los KPIs y, en la segunda llamada, la serie de los últimos 7 días.
> **No se calcula un ranking de productos**; ese dato se obtiene por separado del reporte por
> producto (CU-028).»

---

### CU-027 — Ver Reporte de Ventas por Chofer

**Qué dice la documentación**

> Paso 3: «La app envía **`GET /stats/by-driver?startDate=&endDate=`**.»
> Paso 5: «Retorna un array con `{ driverId, driverName, **deliveriesCount**, **totalAmount**,
> **avgRating**, **avgDeliveryTime** }`.»
> Excepción paso 4: «Si **`endDate < startDate` → 400** "Rango de fechas inválido."»

**Qué hace el código**

- El endpoint real es **`GET /reports/sales-by-driver?from=&to=`**
  (`src/reports/reports.controller.ts:26-38`); los parámetros se llaman `from` y `to`.
- El resultado es `{ driverId, driverName, totalOrders, totalSales }`
  (`src/reports/reports.service.ts:40-57`). **No se calcula `avgRating` ni `avgDeliveryTime`**: el
  servicio no consulta calificaciones ni diferencias de timestamps (método completo en
  `src/reports/reports.service.ts:22-58`).
- `parseDates` solo verifica que las fechas sean parseables
  (`src/reports/reports.controller.ts:15-24`). **No se compara `to` contra `from`**: la excepción
  documentada no existe; con un rango invertido `Between` devuelve simplemente un array vacío.
- Detalle no documentado: si el rango se omite, el reporte cubre **solo el día de hoy**
  (`src/reports/reports.controller.ts:16-17`), no «el último mes».

Sí es fiel: el rol administrador (`src/reports/reports.controller.ts:10`), el filtro por DELIVERED y
por distribuidora (`src/reports/reports.service.ts:23-30`) y el uso de `decimal.js` para los importes
(`:45`, `:50`).

**Gravedad:** grave: dos de las seis métricas prometidas no se calculan, y son las que justifican el
reporte como herramienta de «performance» del chofer.

**Corrección propuesta**

> Paso 2: «Configura el rango de fechas (`from`, `to`). **Por defecto el reporte cubre el día en
> curso.**»
> Paso 3: «El panel envía `GET /reports/sales-by-driver?from=&to=`.»
> Paso 5: «Retorna un array con `{ driverId, driverName, totalOrders, totalSales }`. **La
> calificación promedio y el tiempo promedio de entrega no están implementados** y quedan
> registrados como pendientes en el Documento 3.»
> Excepciones (reemplazar): «Si alguna fecha no es parseable → 400 "Invalid date format
> (YYYY-MM-DD)". **Un rango invertido no se rechaza**: devuelve un resultado vacío.»

---

### CU-028 — Ver Reporte de Ventas por Producto

**Qué dice la documentación**

> Paso 3: «La app envía **`GET /stats/by-product?startDate=&endDate=`**.»
> Paso 4: «El backend agrupa `OrderItems` de pedidos DELIVERED **por `gasCylinderId`**…»
> Paso 5: «Retorna un array con `{ **productId**, productType, **unitsSold**, **totalAmount**,
> **totalDiscounts**, **percentageOfSales** }`.»

**Qué hace el código**

- El endpoint real es **`GET /reports/sales-by-product?from=&to=`**
  (`src/reports/reports.controller.ts:40-51`).
- La agrupación es **por `product.type` y `product.description`**, no por el id de la garrafa
  (`src/reports/reports.service.ts:80-82`).
- El resultado es `{ productType, description, totalQuantity, totalSales }`
  (`src/reports/reports.service.ts:84-89`). **No hay `productId`, ni `totalDiscounts`, ni
  `percentageOfSales`.** Los descuentos se aplican al calcular el precio unitario en la creación del
  pedido (`src/order/domain/order-pricing.service.ts:45-51`), pero el monto descontado **no se
  persiste en ningún lado**, por lo que `totalDiscounts` no es siquiera calculable con el modelo
  actual.

**Gravedad:** grave. Uno de los campos prometidos es directamente imposible con el modelo de datos
vigente; conviene que la tesis lo declare.

**Corrección propuesta**

> Paso 3: «El panel envía `GET /reports/sales-by-product?from=&to=`.»
> Paso 4: «El backend agrupa los ítems de pedidos DELIVERED **por tipo y descripción de garrafa** y
> suma cantidades y subtotales.»
> Paso 5: «Retorna un array con `{ productType, description, totalQuantity, totalSales }`. **El
> porcentaje de participación se calcula en el panel. El monto de descuentos aplicados no se informa:
> el descuento por volumen se absorbe en el precio unitario y no se persiste por separado**
> (pendiente de modelo registrado en el Documento 3).»

---

### CU-029 — Ver Reporte por Método de Pago

**Qué dice la documentación**

> Descripción: «…la distribución **de pedidos** y montos totales por método de pago…»
> Precondición: «…**Existen pedidos** en el rango de fechas.»
> Paso 3: «La app envía **`GET /stats/by-payment-method?startDate=&endDate=`**.»
> Paso 4: «El backend agrupa **pedidos** por `paymentMethod`…»
> Paso 5: «Retorna `[{ method, count, totalAmount, **percentageOfTotal** }]`.»

**Qué hace el código**

- El endpoint real es **`GET /reports/sales-by-payment?from=&to=`**
  (`src/reports/reports.controller.ts:53-64`).
- La consulta filtra `status = DELIVERED` y agrupa por `deliveredAt`
  (`src/reports/reports.service.ts:97-98`): **solo entran pedidos entregados**, no «pedidos en el
  rango».
- El resultado es `{ method, totalOrders, totalSales }`
  (`src/reports/reports.service.ts:108-112`). **No se devuelve `percentageOfTotal`.**

**Gravedad:** grave. El recorte a pedidos entregados cambia el sentido del reporte —un pedido pagado
por MercadoPago y cancelado no aparece—, y el endpoint documentado no existe.

**Corrección propuesta**

> Descripción: «…la distribución de **pedidos entregados** y montos totales por método de pago…»
> Precondición: «…Existen pedidos **entregados** en el rango de fechas.»
> Paso 3: «El panel envía `GET /reports/sales-by-payment?from=&to=`.»
> Paso 4: «El backend agrupa los pedidos **DELIVERED** por `paymentMethod` y suma cantidad y monto.»
> Paso 5: «Retorna `[{ method, totalOrders, totalSales }]`. **El porcentaje sobre el total se calcula
> en el panel.**»

---

### CU-030 — Ver Gráfico de Ventas (últimos 7 días)

**Qué dice la documentación**

> Paso 2: «El frontend ejecuta **`GET /stats/sales-chart?days=7`** automáticamente.»
> Paso 4: «Retorna `[{ **date**: "YYYY-MM-DD", **totalAmount**, **ordersCount** }]`.»

**Qué hace el código**

- El endpoint real es **`GET /orders/stats/chart`**, **sin parámetro `days`**
  (`src/order/order.controller.ts:441-446`): la ventana de 7 días está fija en el servicio
  (`src/order/order.service.ts:346-348`, `:373`).
- La respuesta es `[{ name, date, sales }]` (`src/order/order.service.ts:379-383`), donde `name` es
  el día de la semana abreviado en español (`:378`). **No se devuelve `ordersCount`**: la consulta
  agrega únicamente `SUM(totalAmount)` (`src/order/order.service.ts:352-357`).

Sí es fiel: la suma sobre pedidos DELIVERED (`:356`), el scope por distribuidora (`:359-361`), el
relleno con cero de los días sin ventas (`:365-384`) y que la serie sea de 7 días.

**Gravedad:** grave: ruta inexistente y contrato de respuesta distinto, lo que invalida el paso 5 de
CU-026 que consume estos datos.

**Corrección propuesta**

> Paso 2: «El panel ejecuta `GET /orders/stats/chart` automáticamente. **La ventana de 7 días es fija
> en el backend, no parametrizable.**»
> Paso 3: «El backend suma, en una única consulta agregada (`date_trunc` + `GROUP BY`), el
> `totalAmount` de los pedidos DELIVERED de cada uno de los últimos 7 días de la distribuidora, y
> rellena con cero los días sin ventas.»
> Paso 4: «Retorna `[{ name: "Lun", date: "YYYY-MM-DD", sales }]`. **No se informa la cantidad de
> pedidos por día.**»

---

## Casos de uso sin respaldo en el código

Comportamiento o endpoints que la documentación describe y que **no existen** en el proyecto:

| Referencia | Lo que la documentación dice que existe | Estado real |
|---|---|---|
| CU-001 pasos 4-5 | JWT propio con `userId`, `email` y `role` | No se emite ningún token propio; la credencial es el ID token de Firebase (`src/auth/auth.service.ts:43-59`; `src/auth/guards/jwt-auth.guard.ts:67`). `@nestjs/jwt` está en `package.json:39` pero no se usa en `src/`. |
| CU-001 excepción 3 | Bloqueo de login del chofer no validado | Inexistente: el login no lee `validated` (`src/auth/auth.service.ts:43-93`). |
| CU-002 paso 6 | Autologin tras el registro | Inexistente: se devuelve la entidad `User` (`src/customer/customer.service.ts:106-111`). |
| CU-004 paso 4 | `PATCH /users/me` | Ruta inexistente. Es `PATCH /users/:id` (`src/users/users.controller.ts:160`). |
| CU-004 excepciones | Validación de nombre no vacío y formato de teléfono | Inexistentes (`src/users/dto/create-user.dto.ts:18-32`). |
| CU-005 excepción 10 | Aviso al cliente «Buscando repartidor disponible…» | Inexistente: solo un log de debug (`src/order/application/dispatch-orchestrator.service.ts:58-63`). |
| CU-009 paso 5 | Re-despacho inmediato tras la liberación del chofer | Inexistente: `CancelOrderUseCase` no invoca al orquestador (`src/order/application/cancel-order.use-case.ts:31-36`, `:136-141`). |
| CU-011 paso 3 | Filtros por estado, rango de fechas y chofer | Inexistentes (`src/common/dtos/pagination.dto.ts:4-29`; `src/order/order.service.ts:72-75`). |
| CU-012 paso 5 | `POST /orders/:id/assign-driver` | Ruta inexistente. Es `PATCH /orders/:id/assign/:deliveryId` (`src/order/order.controller.ts:331`). |
| CU-012 pasos 7-8 | Eventos `order:assigned` y `order:accepted` en la asignación manual | Inexistentes (`src/order/order.service.ts:186-199`). |
| CU-016 paso 4 | Campo `Order.rejectedDriverIds[]` | **El campo no existe** en la entidad (`src/order/entities/order.entity.ts:52-209`) ni en el resto de `src/`. |
| CU-016 excepciones | Respuestas 409 y 410 | Inexistentes: la operación responde 200 en todos los casos (`src/order/order.service.ts:57-62`). |
| CU-019 | Estado `ARRIVED` y campo `arrivedAt` | **No existen** en el modelo (`src/order/entities/order.entity.ts:21-33`, `:167-176`; declarado como pendiente en `src/order/domain/order-status.machine.ts:15-16`). |
| CU-018 / CU-020 | 403 cuando el chofer no es el asignado | Inexistente: el `deliveryId` del llamador no se usa fuera de la rama ACCEPTED (`src/order/application/update-order-status.use-case.ts:136-189`). |
| CU-022 paso 2 | `PATCH /delivery/toggle-availability` | Ruta inexistente. Es `PATCH /delivery/user/:userId/availability` (`src/delivery/delivery.controller.ts:165`). |
| CU-022 paso 6 | Re-alta en el radar GEO al volver a estar disponible | Inexistente (`src/delivery/delivery.service.ts:261-267`). |
| CU-023 paso 7 | Aviso al administrador de un reclamo nuevo | Inexistente (`src/claims/claims.service.ts:19-41`). |
| CU-024 pasos 2 y 4 | Paginación y filtros de reclamos | Inexistentes (`src/claims/claims.controller.ts:44-49`; `src/claims/claims.service.ts:43-52`). |
| CU-025 paso 6 | Campo `Claim.resolvedAt` | **El campo no existe** (`src/claims/entities/claim.entity.ts:22-72`). |
| CU-025 paso 7 | Aviso al cliente con el resultado del reclamo | Inexistente (`src/claims/claims.service.ts:68-81`). |
| CU-026 paso 2 | `GET /stats/overview` | Ruta inexistente. Es `GET /orders/stats/summary` (`src/order/order.controller.ts:363`). |
| CU-026 paso 3 | KPI de top productos | Inexistente (`src/order/order.service.ts:287-306`). |
| CU-027 paso 3 | `GET /stats/by-driver` | Ruta inexistente. Es `GET /reports/sales-by-driver` (`src/reports/reports.controller.ts:26`). |
| CU-027 paso 5 | Métricas `avgRating` y `avgDeliveryTime` | Inexistentes (`src/reports/reports.service.ts:22-58`). |
| CU-027 excepción | 400 por rango de fechas invertido | Inexistente (`src/reports/reports.controller.ts:15-24`). |
| CU-028 paso 3 | `GET /stats/by-product` | Ruta inexistente. Es `GET /reports/sales-by-product` (`src/reports/reports.controller.ts:40`). |
| CU-028 paso 5 | Campos `productId`, `totalDiscounts`, `percentageOfSales` | Inexistentes; `totalDiscounts` **no es calculable** con el modelo actual (`src/reports/reports.service.ts:84-89`; `src/order/domain/order-pricing.service.ts:45-51`). |
| CU-029 paso 3 | `GET /stats/by-payment-method` | Ruta inexistente. Es `GET /reports/sales-by-payment` (`src/reports/reports.controller.ts:53`). |
| CU-030 paso 2 | `GET /stats/sales-chart?days=7` | Ruta inexistente y sin parámetro. Es `GET /orders/stats/chart` (`src/order/order.controller.ts:441`). |
| CU-015 / CU-018 / CU-020 | Textos de push por estado ("¡Tu pedido está en camino!", "¡Pedido entregado!") | El método que los produce, `sendOrderStatusUpdate` (`src/notifications/notifications.service.ts:96-136`), **no lo llama nadie**; siempre se envía el push de creación (`src/order/application/update-order-status.use-case.ts:235`). |

---

## Anexo — Brechas de autorización detectadas al verificar los actores

No son discrepancias documentales en sí, pero los CU las presentan como resueltas y conviene
llevarlas al Documento 3:

1. **Transiciones de estado sin control de propiedad** (CU-018, CU-020): cualquier usuario con rol
   chofer puede poner en camino, entregar y —si el pago es en efectivo— marcar como pagado el pedido
   de otro chofer (`src/order/application/update-order-status.use-case.ts:136-189`).
2. **Liberación de pedido sin control de propiedad** (CU-009):
   `src/order/application/cancel-order.use-case.ts:84-90`.
3. **Disponibilidad del chofer sin `@Roles` ni control de identidad** (CU-022): cualquier usuario
   autenticado puede desconectar del radar a cualquier chofer
   (`src/delivery/delivery.controller.ts:165-173` + `src/common/guards/roles.guard.ts:40-42`).
4. **Aviso de llegada sin control de propiedad** (CU-019):
   `src/order/order.controller.ts:408-421` no recibe el usuario autenticado.
5. **Posición GPS tomada del cuerpo del mensaje y no de la identidad del socket** (CU-017):
   `src/gateways/drivers.gateway.ts:88-99`.
6. **`validated` nunca se consulta en el circuito operativo** (CU-001, CU-013, CU-015, CU-022):
   la habilitación del chofer que otorga el administrador en CU-032 no tiene efecto sobre el login,
   el despacho ni la aceptación de pedidos.
