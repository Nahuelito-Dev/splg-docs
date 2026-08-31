# Auditoría adversarial de fidelidad documentación ↔ código — CU-061 a CU-104

Alcance: Casos de Uso Expandidos CU-061 a CU-104 de `docs/1-Requisitos.md` (§7.5), contrastados
contra el código real del backend (controladores, servicios, casos de uso, DTOs, guards, entidades).
Método: refutación. Cada afirmación se verificó con `archivo:línea`. Auditoría de solo lectura.

Nota: los siguientes hallazgos ya estaban confirmados antes de esta auditoría y **no** se cuentan
como nuevos: `PATCH /delivery/:id` sin `@Roles` (CU-096), `GET /users/email/:email` y `POST /email/test`
como `@Public()`, borrado físico en `DELETE /users/:id` (CU-085), y el TODO del pago rechazado (CU-048).

---

## Resumen

| CU | Veredicto | Observación |
|----|-----------|-------------|
| CU-061 | DISCREPANCIA MENOR | La postcondición afirma un recorte por distribuidora que no se aplica cuando no hay tenant en contexto. |
| CU-062 | FIEL | Roles, scope condicional y forma de la consulta coinciden. |
| CU-063 | DISCREPANCIA MENOR | Falta la excepción 400 por distribuidora obligatoria y el paso que sella `resolvedAt`. |
| CU-064 | DISCREPANCIA MENOR | Falta el 404 por pedido inexistente y el paso 5 describe una verificación previa que el código no hace. |
| CU-065 | FIEL | Cualquier rol autenticado, agregado SQL y scope por tenant coinciden. |
| CU-066 | FIEL | Solo administradores, scope por tenant, listado ordenado. |
| CU-067 | DISCREPANCIA MENOR | El paso 3 (consulta previa de unicidad) no existe; el 409 lo produce el índice único al guardar. |
| CU-068 | **DISCREPANCIA GRAVE** | El pedido no se valida contra la distribuidora y la operación no es atómica: no hay "aborto total del tramo". |
| CU-069 | FIEL | Roles, filtro por estado y scope por tenant coinciden. |
| CU-070 | DISCREPANCIA MENOR | Falta el 400 por distribuidora obligatoria y el efecto sobre `current_customer_id`. |
| CU-071 | FIEL | Roles, validación de pertenencia previa y orden cronológico coinciden. |
| CU-072 | **DISCREPANCIA GRAVE** | El estado RESERVED no se decide "por tener fecha" sino por el flag `isReservation`; y la falta de stock devuelve 500, no 400. |
| CU-073 | FIEL | Roles, orden por fecha agendada y cálculo en memoria del saldo coinciden. |
| CU-074 | FIEL | Roles, scope por tenant, 404 y 400 coinciden. |
| CU-075 | DISCREPANCIA MENOR | La frecuencia queda sin declarar ("cada X min"); el cron corre cada 5 minutos y toma hasta 50 reservas. |
| CU-076 | FIEL | `@Cron('0 0 * * * *')` = cada hora, tal como se declara. |
| CU-077 | FIEL | `@Cron('0 */30 * * * *')` = cada 30 minutos, tal como se declara. |
| CU-078 | FIEL | Actor (chofer emisor), roles, ownership y las tres excepciones coinciden. |
| CU-079 | FIEL | Actor (cliente confirma), roles, idempotencia y los once pasos coinciden. |
| CU-080 | FIEL | Ruta, roles, orden ascendente y uso desde el cron de despacho coinciden. |
| CU-081 | FIEL | Ruta, roles, orden descendente y ausencia de control de pertenencia coinciden. |
| CU-082 | FIEL | Endpoint público, DTO con todos los campos opcionales, 400 por duplicado y 500 genérico. |
| CU-083 | FIEL | Tres endpoints, roles, `ILIKE` triple y la asimetría 404/`null` coinciden. |
| CU-084 | FIEL | Endpoint público, ausencia de DTO y respuesta `{ exists, email, phoneNumber }` coinciden. |
| CU-085 | FIEL | La ficha describe correctamente el borrado físico, el orden base-antes-que-proveedor y el 409. |
| CU-086 | FIEL | Reglas de alcance multi-empresa, orden de pasos y excepciones coinciden. |
| CU-087 | FIEL | Endpoint público, verificación de listado vacío y delegación en el alta de CU-086. |
| CU-088 | FIEL | Ambos endpoints, scope condicional del listado y término sin acotar coinciden. |
| CU-089 | FIEL | `@Roles(SUPER_ADMIN)` a nivel de clase, cinco rutas y el 500 no mapeado del borrado. |
| CU-090 | FIEL | Lista fija de cuatro roles, idempotencia por búsqueda previa y recorrido no transaccional. |
| CU-091 | FIEL | Endpoint, guard implícito y el retorno (no lanzamiento) de la excepción `CONTINUE`. |
| CU-092 | FIEL | Recorte por existencia de pedidos, tres relaciones y ausencia de total coinciden. |
| CU-093 | FIEL | Ambos endpoints, `validated` como texto y ausencia de scope por distribuidora. |
| CU-094 | FIEL | Resolución de alcance en el controlador, pertenencia en el servicio y cuerpo sin DTO. |
| CU-095 | FIEL | Borrado lógico sobre el perfil de cliente, mensaje y excepciones coinciden. |
| CU-096 | FIEL | La ficha ya declara la ausencia de `@Roles` y de control de pertenencia (hallazgo previo). |
| CU-097 | FIEL | Roles, borrado lógico y mensaje coinciden. |
| CU-098 | FIEL | Control anti-secuestro, búsqueda cliente-luego-chofer y respuestas sin error HTTP. |
| CU-099 | FIEL | Autorización self-o-admin y la asimetría con el alta (solo mira cliente) coinciden. |
| CU-100 | FIEL | Roles, marca `TEST` con timestamp y respuesta `{ success: false }` con 201. |
| CU-101 | FIEL | Roles, resolución del token, cuerpo del mensaje y ausencia de validación del pedido. |
| CU-102 | FIEL | Endpoint público temporal, doble enlace de recuperación y diagnóstico devuelto. |
| CU-103 | FIEL | Desactivación, recorte por tenant en la lectura y 400 por falta de `X-Distributor`. |
| CU-104 | FIEL | Tres sondas públicas y exentas del límite, cuatro indicadores y umbrales 300 MB / 90 %. |

**Conteo:** FIEL 36 · DISCREPANCIA MENOR 6 · DISCREPANCIA GRAVE 2 · NO VERIFICABLE 0.

---

## Discrepancias encontradas

### CU-068 — Asignar Envases a un Pedido — **GRAVE**

**Qué dice la documentación**

> Paso 3: «El sistema cruza IDs validando que pedido y envases correspondan a la orbita del tenant y del universo operable.»
>
> Excepción al paso 4: «Si una sola garrafa se hallase vacia o en desuso, aborta total del tramo emitiendo 400 Bad Request.»

**Qué hace el código**

1. El pedido **no** se acota por distribuidora. `CylinderService.assignToOrder` lo busca solo por
   clave primaria (`src/cylinder/cylinder.service.ts:156-158`):

   ```ts
   const order = await this.orderRepository.findOne({
     where: { order_id: orderId },
   });
   ```

   Solo los envases se validan contra el tenant, vía `findBySerial`
   (`src/cylinder/cylinder.service.ts:102-104`). Un administrador puede así asignar envases
   propios a un pedido de otra distribuidora.

2. **No hay transacción ni aborto total.** El recorrido asigna y transiciona envase por envase,
   guardando cada uno antes de pasar al siguiente (`src/cylinder/cylinder.service.ts:164-178`); la
   validación de estado ocurre dentro de `recordTransition` → `assertTransition`
   (`src/cylinder/cylinder.service.ts:233`). Si el tercer serial de la lista no está `FILLED`, los dos
   primeros ya quedaron persistidos en `DISPATCHED` con su movimiento registrado, y la respuesta es
   igualmente un 400. El estado del inventario queda a mitad de camino.

**Gravedad:** Grave. La primera parte es una falla de aislamiento multi-empresa que la documentación
afirma cubierta; la segunda promete atomicidad inexistente sobre datos de inventario.

**Corrección propuesta**

- Paso 3: «El sistema recupera el pedido **por identificador, sin acotarlo a la distribuidora**, y
  recupera cada envase por serial **dentro de la distribuidora del solicitante**
  (`cylinder.service.ts:156-158` y `:102-104`). **⚠️ verificar**: el pedido no se valida contra el
  tenant, de modo que es posible asignar envases de una empresa a un pedido de otra.»
- Excepción al paso 4: «Si alguna garrafa no está `FILLED`, la máquina de estados rechaza esa
  transición y el sistema retorna error 400. **La operación no es transaccional**: los envases
  procesados antes de la falla quedan asignados al pedido y en estado `DISPATCHED`
  (`cylinder.service.ts:164-178`). **⚠️ verificar**: falta envolver el recorrido en una transacción.»

---

### CU-072 — Crear Reserva Programada con Seña — **GRAVE**

**Qué dice la documentación**

> Paso 5: «El sistema salva el orden en BD y determina (**por ver que tiene fecha**) otorgarle
> clasificacion RESERVED con **deposit_paid nulo**.»
>
> Excepción al paso 4: «Si ocurre un deadlock o **no queda saldo comercial en inventario**, rollbackea
> y estampa **Bad Request**.»
>
> Precondición: «Usuario de frente (Cliente) o Administrador.»

**Qué hace el código**

1. Lo que decide el estado `RESERVED` es el flag `isReservation` del DTO, **no** la presencia de
   `scheduledDate` (`src/order/application/create-order.use-case.ts:236` y `:245`):

   ```ts
   const isReservation = !!createOrderDto.isReservation;
   ...
   status: isReservation ? OrderStatus.RESERVED : OrderStatus.PENDING,
   ```

   La relación es la inversa de la que describe el paso 5: una reserva **exige** `scheduledDate`
   (`create-order.use-case.ts:102-106`, error 400), pero un pedido con fecha agendada y sin el flag
   nace `PENDING` y se despacha de inmediato. Además `deposit_paid` se inicializa en `false`, no en
   nulo (`create-order.use-case.ts:252`).

2. La falta de stock **no** produce 400. `StockReservationService.reserve` lanza
   `InsufficientStockError` (`src/order/domain/stock-reservation.service.ts:50`), que es un error de
   dominio sin propiedad `status` (`src/common/errors/domain.error.ts:17-25`). El `catch` del caso de
   uso solo repropaga errores con `status` 404 o 400 y convierte todo lo demás en 500
   (`create-order.use-case.ts:321-325`):

   ```ts
   if (error.status === 404 || error.status === 400) {
     throw error;
   }
   this.logger.error(`create order falló: ${error?.message}`);
   throw new InternalServerErrorException('Error al crear el pedido');
   ```

   El error de dominio nunca llega al `GlobalExceptionFilter`, que es quien lo mapearía a 400
   (`src/common/filters/global-exception.filter.ts:43`). Lo mismo ocurre con
   `GasCylinderNotFoundError`, que debería ser 404. Ningún test cubre este camino
   (`src/order/application/create-order.use-case.spec.ts`).

3. `POST /orders` **no declara `@Roles`** (`src/order/order.controller.ts:71-72`): como el `RolesGuard`
   deja pasar cuando el handler no declara roles (`src/common/guards/roles.guard.ts:40-42`), también un
   chofer autenticado puede crear la reserva. El único control es el anti-impersonación del cliente
   (`order.controller.ts:94-101`).

**Gravedad:** Grave. El paso 5 describe mal el mecanismo que da origen al caso de uso completo, y la
excepción 4 promete un 400 que en la práctica es un 500 sin mensaje de negocio.

**Corrección propuesta**

- Precondición: «El solicitante está autenticado. El endpoint `POST /orders` no declara restricción de
  roles (`order.controller.ts:71-72`), de modo que también un chofer puede crearla; un cliente solo
  puede crear pedidos a su propio nombre (`order.controller.ts:94-101`).»
- Paso 5: «El sistema persiste el pedido y, **si el cuerpo trae el indicador `isReservation`**, lo crea
  en estado RESERVED con `deposit_amount` y `deposit_paid = false`; sin ese indicador nace PENDING
  aunque tenga fecha agendada (`create-order.use-case.ts:236-253`). Una reserva sin `scheduledDate` se
  rechaza con 400 antes de abrir la transacción (`create-order.use-case.ts:102-106`).»
- Excepción al paso 4: «Si no queda stock, el dominio lanza `InsufficientStockError`
  (`stock-reservation.service.ts:50`); como el `catch` del caso de uso solo repropaga errores con
  status 404 o 400, el error de dominio se convierte en **500 "Error al crear el pedido"**
  (`create-order.use-case.ts:321-325`). **⚠️ verificar**: es un mapeo de error perdido; el
  `GlobalExceptionFilter` lo devolvería como 400 si no se lo tragara antes el caso de uso. Un deadlock
  se reintenta en `withTransactionRetry` (`order.controller.ts:106-109`) y, agotados los reintentos,
  también termina en 500.»

---

### CU-061 — Listar Incidencias — MENOR

**Qué dice la documentación**

> Paso 2: «El sistema consulta BD enlazando la query por CurrentDistributor.»
>
> Postcondición: «Se visualiza **toda** la bolsa de incidencias **acotada a la distribuidora activa**.»

**Qué hace el código**

`@CurrentDistributor()` se usa **sin** `{ required: true }` (`src/incident/incident.controller.ts:49`),
por lo que devuelve `null` para un Administrador General sin cabecera `X-Distributor`
(`src/common/decorators/current-distributor.decorator.ts:14`). El servicio arma el `where` de forma
condicional (`src/incident/incident.service.ts:49-51`):

```ts
const where: FindOptionsWhere<Incident> = {
  ...(distributorId ? { distributor_id: distributorId } : {}),
};
```

Con tenant nulo la consulta devuelve las incidencias de **todas** las distribuidoras. El paso 2 tampoco
menciona que la consulta trae `order` y `order.customer` y ordena por fecha descendente
(`incident.service.ts:57-58`). Las fichas CU-088 y CU-092 sí documentan explícitamente este caso
cross-tenant; esta no.

**Gravedad:** Menor (documentación incompleta, comportamiento intencional del rol SUPER_ADMIN).

**Corrección propuesta**

- Paso 2: «El sistema consulta la base filtrando por la distribuidora del contexto, y trae el pedido y
  su cliente para que el panel muestre a quién afecta cada incidencia (`incident.service.ts:53-59`).»
- Postcondición: «Se visualiza la bolsa de incidencias de la distribuidora activa, ordenada de la más
  reciente a la más antigua. Si el solicitante es Administrador General sin empresa en contexto, la
  consulta no se acota y devuelve las incidencias de todas las distribuidoras
  (`incident.service.ts:49-51`).»

---

### CU-063 — Resolver Incidencia — MENOR

**Qué dice la documentación**

> Paso 3: «El sistema edita el flag de estatus y graba el comentario resolutivo.»
>
> Excepciones: solo el 404 del paso 2.

**Qué hace el código**

El controlador exige distribuidora en contexto con `@CurrentDistributor({ required: true })`
(`src/incident/incident.controller.ts:72`), lo que produce un **400 "Falta la distribuidora: enviá el
header X-Distributor (slug o id)"** para un Administrador General que no la envíe
(`src/common/decorators/current-distributor.decorator.ts:36-40`). Esa excepción no está documentada.
Además el servicio sella la marca temporal `resolvedAt` junto con el estado y la nota
(`src/incident/incident.service.ts:101-103`), efecto que el paso 3 y la postcondición omiten.

**Gravedad:** Menor.

**Corrección propuesta**

- Paso 3: «El sistema fija el estado en RESOLVED, graba la nota de resolución y sella la fecha de
  resolución (`incident.service.ts:101-103`).»
- Agregar excepción: «Paso 1 — Si el solicitante no tiene distribuidora en el contexto de la petición
  (Administrador General sin cabecera `X-Distributor`), el sistema retorna error 400 "Falta la
  distribuidora: enviá el header X-Distributor (slug o id)"
  (`current-distributor.decorator.ts:36-40`).»

---

### CU-064 — Calificar Pedido (cliente↔chofer) — MENOR

**Qué dice la documentación**

> Paso 5: «El sistema **avala que no exista un registro duplicado** (una votacion por cabeza).»
>
> Excepciones: 400 (paso 3), 403 (paso 4), 409 (paso 5). No figura ningún 404.

**Qué hace el código**

1. No hay comprobación previa de duplicado: el servicio intenta guardar y traduce la violación del
   índice único `UQ_rating_order_role` (`src/rating/entities/rating.entity.ts:29`) al 409
   (`src/rating/rating.service.ts:93-100`):

   ```ts
   } catch (error: any) {
     if (error.code === '23505') {
       throw new ConflictException('Ya calificaste este pedido');
     }
   ```

2. Si el pedido no existe, el servicio lanza **404 "Pedido no encontrado"**
   (`src/rating/rating.service.ts:50-52`), excepción ausente en la ficha.

3. El orden real de validaciones es: existencia (404) → estado DELIVERED (400) → pertenencia según
   rol (403) → chofer presente (400) (`rating.service.ts:50-80`); la ficha ubica la comprobación del
   chofer en el paso 3, junto con el estado, cuando en el código solo se evalúa en la rama del cliente
   (`rating.service.ts:67-69`).

**Gravedad:** Menor (los códigos de estado documentados son correctos; falta uno y el paso 5 describe
una verificación optimista como si fuera previa).

**Corrección propuesta**

- Paso 5: «El sistema intenta persistir la calificación y delega la unicidad en el índice
  `(order_id, from_role)` de la base: una violación de ese índice se traduce en conflicto
  (`rating.service.ts:93-100`, `rating.entity.ts:29`).»
- Agregar excepción: «Paso 3 — Si el pedido no existe, el sistema retorna error 404 "Pedido no
  encontrado" (`rating.service.ts:50-52`).»
- Excepción del paso 3, precisión: «"El pedido no tiene chofer para calificar" (400) solo se evalúa
  cuando quien califica es el cliente; para el chofer, no haber sido el repartidor del pedido produce
  403 (`rating.service.ts:67-75`).»

---

### CU-067 — Dar de Alta un Envase Físico — MENOR

**Qué dice la documentación**

> Paso 2: «El sistema verifica el formato exigido.»
>
> Paso 3: «El sistema **se cerciora con consulta en tabla local (mismo tenant) que el identificador es
> único irrepetible**.»

**Qué hace el código**

No existe ninguna consulta previa de unicidad. `CylinderService.create` construye la entidad y la
guarda directamente, capturando la violación del índice único compuesto
(`src/cylinder/cylinder.service.ts:43-53`):

```ts
} catch (error: any) {
  if (error.code === '23505') {
    throw new ConflictException('El serial ya existe en tu distribuidora');
  }
```

El índice es `@Unique(['distributor_id', 'serial'])` (`src/cylinder/entities/cylinder.entity.ts:36`).
La validación del paso 2 se reduce a `@IsString()` sobre el serial
(`src/cylinder/dto/create-cylinder.dto.ts:5-6`): no hay formato exigido. Falta además un paso: el alta
registra el movimiento inicial `null → IN_DEPOT` en la tabla de auditoría
(`cylinder.service.ts:55-62`). Y como el controlador usa `@CurrentDistributor({ required: true })`
(`src/cylinder/cylinder.controller.ts:43`), un Administrador General sin cabecera recibe 400, excepción
no documentada.

**Gravedad:** Menor.

**Corrección propuesta**

- Paso 2: «El sistema valida que el serial sea una cadena y, si vienen, que el identificador de
  producto sea un UUID y el depósito un número no negativo (`create-cylinder.dto.ts`).»
- Paso 3: «El sistema le otorga el estado inicial IN_DEPOT y lo persiste; la unicidad del serial
  dentro de la distribuidora la garantiza el índice único compuesto `(distributor_id, serial)`
  (`cylinder.entity.ts:36`), cuya violación el servicio traduce a conflicto
  (`cylinder.service.ts:43-53`).»
- Agregar paso: «El sistema registra el movimiento inicial `null → IN_DEPOT` en el historial del envase
  (`cylinder.service.ts:55-62`).»
- Agregar excepción: «Paso 1 — Si no hay distribuidora en el contexto, el sistema retorna error 400
  "Falta la distribuidora: enviá el header X-Distributor (slug o id)"
  (`cylinder.controller.ts:43`, `current-distributor.decorator.ts:36-40`).»

---

### CU-070 — Registrar Movimiento de Envase — MENOR

**Qué dice la documentación**

> Paso 5: «Si corresponde, guarda status, registra historial (HistoryLog) y responde exitoso.»
>
> Excepciones: 404 (paso 3) y 400 (paso 4).

**Qué hace el código**

La transición aplica un efecto adicional sobre la titularidad del envase que la ficha no menciona
(`src/cylinder/cylinder.service.ts:235-242`): al pasar a `WITH_CUSTOMER` se asigna
`current_customer_id` con el cliente del pedido indicado (`cylinder.service.ts:127-132`), y al pasar a
`EMPTY_RETURNED` o `IN_DEPOT` ese campo se limpia. Ese efecto es parte de la postcondición real
(«el material físico se localiza en nuevo estadio logístico» no lo cubre).

Falta también la excepción por distribuidora obligatoria: el controlador usa
`@CurrentDistributor({ required: true })` (`src/cylinder/cylinder.controller.ts:119`), de modo que sin
cabecera `X-Distributor` el Administrador General recibe 400
(`current-distributor.decorator.ts:36-40`).

**Gravedad:** Menor.

**Corrección propuesta**

- Paso 5: «Si la transición es válida, el sistema actualiza el estado, ajusta la titularidad del envase
  (`current_customer_id` se asigna al pasar a WITH_CUSTOMER y se limpia al volver a EMPTY_RETURNED o
  IN_DEPOT), persiste el envase y registra el movimiento en el historial append-only
  (`cylinder.service.ts:235-257`).»
- Agregar excepción: «Paso 1 — Si no hay distribuidora en el contexto, el sistema retorna error 400
  "Falta la distribuidora: enviá el header X-Distributor (slug o id)"
  (`cylinder.controller.ts:119`).»

---

### CU-075 — Activar Reservas Vencidas Automáticamente (Cron) — MENOR

**Qué dice la documentación**

> Paso 1: «El daemon @Cron se levanta en modulo background **cada X min**.»
>
> Paso 4: «El sistema acopla **en paralelo** el orchestrador de envios…»
>
> Frecuencia: «Frecuente (cron).»

**Qué hace el código**

La expresión real es `@Cron('0 */5 * * * *')`, es decir **cada 5 minutos**
(`src/order/application/reservation.service.ts:127`). El barrido toma como máximo **50 reservas por
vuelta** (`reservation.service.ts:137`) y **no se acota por distribuidora**: la consulta filtra solo por
estado, seña paga y fecha agendada (`reservation.service.ts:130-137`). El despacho se dispara **dentro
del mismo recorrido secuencial**, una reserva después de otra, no en paralelo
(`reservation.service.ts:141-158`). Las otras dos fichas de cron sí declaran su frecuencia y coinciden
con el código: CU-076 «Hora a hora» = `@Cron('0 0 * * * *')` (`reservation.service.ts:165`) y CU-077
«Cada 30 min» = `@Cron('0 */30 * * * *')` (`reservation.service.ts:225`).

**Gravedad:** Menor (la ficha no afirma una frecuencia falsa, la omite; el "en paralelo" sí es
impreciso).

**Corrección propuesta**

- Paso 1: «El proceso automático se ejecuta **cada 5 minutos** (`reservation.service.ts:127`).»
- Paso 2: «El sistema busca hasta 50 reservas en estado RESERVED con la seña paga y fecha agendada
  menor o igual a la de hoy, sin acotar por distribuidora (`reservation.service.ts:130-137`).»
- Paso 4: «Por cada reserva activada, y **de forma secuencial**, el sistema recupera el pedido completo
  y se lo ofrece al chofer más cercano mediante el orquestador de despacho, en modo best-effort
  (`reservation.service.ts:146-151`).»
- Frecuencia: «Cada 5 minutos (cron).»

---

## Casos de uso sin respaldo en el código

Ninguno. Los 44 casos de uso del rango CU-061 a CU-104 tienen endpoint, proceso automático o
componente implementado y localizable:

- Los 42 casos con endpoint HTTP resuelven a una ruta existente con el método declarado
  (incidencias, calificaciones, envases, reservas, pedidos, usuarios, administradores, roles,
  clientes, choferes, notificaciones, correo, franjas y salud).
- CU-075, CU-076 y CU-077 corresponden a los tres métodos anotados con `@Cron` de
  `src/order/application/reservation.service.ts` (líneas 127, 165 y 225 respectivamente).
- CU-104 corresponde a las tres rutas de `src/health/health.controller.ts` (líneas 42, 60 y 72).

Sí quedan señalados en las fichas —y se confirman contra el código— dos endpoints declarados
"temporales" o "de desarrollo" que siguen expuestos: `POST /email/test`, público
(`src/email/email.controller.ts:49-51`), y `POST /admin/first-superadmin`, público y rotulado
"development only" (`src/admin/admin.controller.ts:32-35`).
