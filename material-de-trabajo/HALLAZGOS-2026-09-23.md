# Hallazgos — revisión del 23/09/2026

Probado contra el entorno corriendo (`./splg-dev.sh`), backend en `:3000`, base
`splg_db` con 36 usuarios, 25 clientes, 180 pedidos, 6 choferes.

**Nada de esto está arreglado.** Se corrigen de a uno, en el orden que se decida.

## Estado general

El backend está sano: de los 59 GET del OpenAPI, **47 responden bien y ninguno
devuelve 500**. De los 12 restantes, 5 son 403 correctos (piden `super_admin`),
2 fueron culpa de los datos de prueba y el resto son reglas de negocio legítimas.
Health da verde en Postgres, Redis, memoria y disco.

---

## Verificados uno por uno

### H-01 · El panel nunca se entera de que el pedido salió — **funcional, alto**
`splg-app-admin/src/hooks/useSocket.ts` escucha `order:on_the_way` (guion bajo).
El backend emite `order:on-the-way` (guion medio), en
`splg-app-backend/src/order/application/update-order-status.use-case.ts`.
El evento nunca llega. La app del cliente sí lo escucha bien, así que el defecto
es sólo del panel. Falla en silencio: no hay error, simplemente no pasa nada.

### H-02 · El login devuelve el objeto crudo de Firebase — **seguridad, alto**
Las cuatro rutas de acceso devuelven el `UserCredential` completo, que incluye
`refreshToken`, el `apiKey` de Firebase y el campo interno `_tokenResponse`.
El `refreshToken` es de vida larga: con él se emiten tokens nuevos.
No hay DTO de respuesta: el controlador devuelve lo que le da el proveedor.
Ya está cubierto por un test de la colección de Postman, que hoy falla a propósito.

### H-03 · Un 404 revela la ruta absoluta del servidor — **seguridad, medio**
Pedir una ruta inexistente contesta con un `ENOENT` que incluye la ruta completa
en disco (`/Users/…/splg-app-backend/…`). Expone la estructura de la máquina.

### H-04 · `OwnershipGuard` existe y no se usa — **arquitectura, medio**
`src/auth/guards/ownership.guard.ts` está escrito y no se aplica en ningún lado.
La pertenencia se controla a mano en los servicios (ver H-05). Es código muerto
que además aparenta una protección que no está puesta.

### H-05 · La pertenencia se controla en el servicio, no en un guard — **arquitectura, medio**
En `user-addres` la protección **sí funciona**: `scope(user)` devuelve `undefined`
para admin y super admin, y el id del que pide para el resto; `assertOwnership`
tira 403 si no coincide. Pero está resuelto servicio por servicio, duplicado
(aparece igual en `customer.service.ts`), en vez de estar en el guard que ya existe.
*Nota: el censo automático reportó esto como agujero de autorización. Lo verifiqué
y no lo es, al menos en `user-addres`. Falta revisar los demás módulos.*

### H-06 · `TimeoutInterceptor` se registra dos veces — **arquitectura, bajo**
`src/main.ts:37` con `useGlobalInterceptors` y `src/app.module.ts:171` como
`APP_INTERCEPTOR`. Se aplica dos veces a cada request.

### H-07 · Los parámetros del despacho no se pueden configurar — **tesis, alto**
`OFFER_TTL_SECONDS = 30` y `RADIUS_STEPS_KM = [5,10,15,20]` son constantes de
clase en `dispatch-orchestrator.service.ts`. La cátedra exige (criterio C4) que
el módulo inteligente sea parametrizable desde el sistema. Hoy se cambia recompilando.

### H-08 · Cuatro discrepancias entre la documentación y el código — **tesis, alto**
La tabla de procesos automatizados dice "5 → 10 → 15 km" (son cuatro pasos hasta
20), "2 minutos" (el TTL es de 30 segundos), "cron cada 1 minuto" (es cada 15
segundos) y "si supera el máximo de intentos notifica al administrador" — **esto
último no existe**: no hay máximo de intentos ni aviso. El reintento es indefinido.

### H-09 · El OpenAPI miente sobre `GET /coverage-zones/check` — **documentación, medio**
No declara ningún parámetro, pero el endpoint exige `lat` y `lng` y responde 400
sin ellos. Afecta a Swagger y a cualquier cosa generada desde ahí.

### H-10 · El backend no compila los tests — **calidad, medio**
`src/order/application/update-order-status.use-case.spec.ts:43` rompe `tsc --noEmit`:
`notifyAdmins` no existe en el tipo del mock. Es previo a esta revisión.

### H-11 · No hay `.env.example` — **operación, medio**
El backend no versiona ninguna plantilla de variables. Quien clone el repo no
sabe qué configurar, y la `DB_LOGGING` nueva no está documentada en ningún lado.

### H-12 · El nombre propio sigue en los datos — **marca, medio**
La distribuidora sembrada se llama **Jeny Gas**, con slug **`jeny-gas`**, que es
el identificador que usa el backend por defecto. El administrador se llama
**"Admin Jeny"**. El panel ya no lo lleva; los datos sí.

### H-13 · Dos usuarios huérfanos en la siembra — **datos, bajo**
`admin@gasandino.com` y `chofer@gasandino.com` pueden autenticarse pero no tienen
fila de administrador (`distributor` en NULL). No pueden entrar al panel y no
pertenecen a ninguna distribuidora.

### H-14 · El aislamiento multi-distribuidora no está probado — **tesis, medio**
Hay **una sola** distribuidora en la base. La documentación sostiene que el
sistema es multi-distribuidora, pero no hay una segunda con datos propios contra
la cual demostrar que una no ve lo de la otra.

### H-15 · El despacho gira en vacío — **funcional, a investigar**
El cron corre cada 15 segundos sobre una docena de pedidos pendientes y siempre
registra "Sin choferes nuevos (ya contactados: 0)", aunque hay 6 choferes
cargados. Falta determinar si es por falta de posición GPS, por estado, o por
la zona de cobertura.

### H-16 · Comentario de trabajo olvidado en un DTO — **prolijidad, bajo**
`src/auth/dto/login.dto.ts`: `@IsOptional() // ← AGREGAR ESTO`.

---

## Reportados por el censo automático, **todavía sin verificar**

No los tomo por ciertos hasta abrirlos uno por uno:

- 11 endpoints reciben el cuerpo con un tipo literal en vez de un DTO, así que
  `class-validator` no corre sobre ellos.
- 27 endpoints autenticados no declaran `@Roles`. `RolesGuard` deja pasar cuando
  no hay metadata — eso **sí** lo verifiqué. Falta ver, módulo por módulo, cuáles
  compensan con un control en el servicio (como `user-addres`) y cuáles no.
- Dos entidades vacías sin `@Entity`: `email.entity.ts` y `notification.entity.ts`.
- `registerWithUser` está duplicado casi idéntico entre `delivery.service.ts` y
  `customer.service.ts`; `handleDBExceptions` aparece en 6 servicios.
- `DispatchOrchestratorService` inyecta `NotificationsService` concreto aunque
  `NotificationPort` está registrado en su propio módulo.
- Cinco clases inyectan `Repository<T>` o `DataSource` crudos teniendo un puerto
  en el mismo constructor.
- Nueve DTOs no se referencian desde ningún lado.

---

## Segunda tanda — de la batería completa (131 endpoints, escrituras incluidas)

Corrida con los 131 endpoints en orden CRUD, con los cuatro roles, contra la
base respaldada antes (`.db-backups/splg_db-20260923-100402-pre-pruebas.sql`).
Resultado: **79 OK · 37 rechazos · 8 no encontrados · 2 sin permiso · 1 error 500**.

### H-17 · `DELETE /api/role/{id}` devuelve 500 — **defecto, alto**
Borrar un rol que tiene usuarios asociados lanza un `QueryFailedError` crudo que
nadie atrapa:
`update or delete on table "role" violates foreign key constraint "FK_fb2e442d14add3cefbdf33c4561" on table "user"`.
El cliente recibe `500 Internal server error`. Tendría que ser un **409** con un
mensaje que explique que el rol está en uso. El helper `handleDBExceptions` que
existe en otros seis servicios no se aplica acá. **Es el único 5xx de los 131.**

### H-18 · Un usuario borrado lógicamente puede obtener token — **seguridad, medio**
`chofer@splg.com` tiene `deletedAt` desde el 06/09 y `POST /api/auth/login`
igual devuelve **200 con un `idToken` válido**. El guard después lo rechaza con
401 en cada llamada, así que no se puede operar — pero la app muestra "sesión
iniciada" y falla en todo lo que sigue. El login debería negar el acceso a una
cuenta dada de baja.

### H-19 · No hay ningún chofer que pueda usarse — **entorno, alto**
Los 6 choferes de la base (`chofer1..6@demo.splg.com`) están activos, validados
y con GPS, pero **ninguno tiene cuenta en Firebase**: el seed de demostración
los crea sólo en la base, a propósito. Los únicos usuarios con login que dicen
"chofer" (`chofer@splg.com`, `chofer@gasandino.com`) están borrados y además no
tienen fila en `delivery`.

Consecuencias: la app del chofer no se puede ejercitar, y todos los endpoints
exclusivos de chofer quedan sin probar de verdad.

### H-20 · El despacho automático no puede demostrarse — **tesis, alto**
Es consecuencia de H-19. El cron corre cada 15 segundos y siempre registra
"Sin choferes nuevos (ya contactados: 0)". La causa es que **Redis no tiene
ningún chofer conectado** — sólo hay claves de rate-limit. El orquestador busca
candidatos entre los choferes en línea, y nadie puede conectarse porque nadie
puede autenticarse. El código no tiene la culpa; el entorno no permite mostrarlo.

Para la presentación hace falta al menos un chofer con cuenta real que pueda
loguearse y abrir el socket.

### H-21 · Dos maneras distintas de decir la misma distribuidora — **arquitectura, medio**
En el mismo módulo `time-slot`: `GET /time-slot` la recibe como query param
`distributor`, mientras que `POST /time-slot` y `DELETE /time-slot/{id}` la
exigen en la cabecera `X-Distributor`. Además el query param acepta **sólo el
slug**: pasarle el UUID de la distribuidora da 404.

### Nota metodológica
Durante la batería, el `DELETE /api/distributor/{id}` **borró lógicamente la
única distribuidora**, lo que hizo fallar a todo lo que la resuelve. No es un
defecto del backend: fue daño de la propia prueba. Se restauró y se verificó
contra la API. El resto de los datos quedó intacto (180 pedidos, 25 clientes,
6 choferes, 4 franjas, 3 zonas, 4 productos, 4 roles).

Conviene que la colección marque los borrados destructivos, o que la batería
corra siempre sobre lo que ella misma crea.

---

## Tercera tanda — con los cuatro roles reales y la cabecera `X-Distributor`

Se creó por la propia API un cliente y un chofer de verdad (con cuenta en
Firebase), y se agregó la cabecera `X-Distributor` que casi todas las escrituras
exigen. Resultado final: **91 andan · 8 responden con una regla de negocio ·
29 pendientes por datos de prueba · 2 rotos**.

### H-22 · `POST /users/delivery-registration` devuelve 500 — **defecto, alto**
Dar de alta un chofer **sin** `distributorId` revienta con 500. La causa:
`delivery.distributor_id` es **NOT NULL sin default**, pero en `CreateDeliveryDto`
el campo es `@IsOptional()`. Postgres tira violación de NOT NULL (código 23502),
que `handleDBExceptions` no contempla, y sale un 500.

Comprobado en los dos sentidos: sin el campo da 500; con
`"distributorId": "af0c1b75-…"` el chofer se crea perfecto.

Contraste que conviene mirar: `POST /users/customer-registration` **sí** funciona
sin `distributorId`. Los dos registros no resuelven la distribuidora igual.

Arreglo: o el DTO lo exige (400 diciendo qué falta), o el servicio resuelve la
distribuidora por defecto como hace el registro de clientes.

### H-23 · `handleDBExceptions` se traga la causa — **diagnóstico, alto**
Sólo contempla los códigos `23505` (duplicado) y `23503` (clave foránea).
Cualquier otro error se convierte en `InternalServerErrorException('Unexpected
error, check server logs')` **y nunca se registra el error original**. El mensaje
manda a mirar unos logs donde la causa no está.

Es lo que hizo que H-22 tardara en aparecer, y está repetido en 6 servicios.
Arreglo: registrar el error antes de convertirlo, y contemplar `23502` (NOT NULL)
y `22P02` (sintaxis de entrada inválida).

### H-24 · `PATCH /gascylinder/{id}/stock` devuelve 500 — **defecto, alto**
`QueryFailedError: invalid input syntax for type integer: "NaN"` en
`gascylinder.service.ts:152`. El valor no numérico viaja desde el cuerpo hasta
Postgres sin que nadie lo valide, porque el endpoint declara:

```ts
@Body() body: { quantity: number },   // gascylinder.controller.ts:108
```

Un tipo literal de TypeScript **no existe en tiempo de ejecución**: el
`ValidationPipe` global no tiene clase contra la cual validar y deja pasar
cualquier cosa. Es la consecuencia concreta de los 11 endpoints sin DTO: no es
una objeción de estilo, produce un 500.

Arreglo: un `UpdateStockDto` con `@IsInt()` y `@Min(0)`. Pasa a ser un 400.

### Los 29 pendientes por datos de prueba
No son defectos: son cuerpos de ejemplo que el generador arma desde el OpenAPI y
que no cumplen las reglas reales. Se resuelven afinando la colección:

- **Admin, Auth, Incidents, Distributors** — el cuerpo generado no respeta el DTO
  (faltan campos, o el largo o el enum no coinciden).
- **User Addresses (5)** — hacen falta direcciones del usuario que pide.
- **Orders** — `POST /orders` pide un cliente existente en el cuerpo.
- **Cylinders (3)** — necesitan un envase en el estado correcto para la transición.

### H-25 · `order.customer_id` apunta a `user`, no a `customer` — **modelado, alto**
La clave foránea real es `order.customer_id → user.user_id`. La columna lleva el
nombre de una entidad y guarda el identificador de otra.

Consecuencias medidas:
- `POST /orders` con un `customer_id` real responde **"Cliente no encontrado"**,
  porque espera un `user_id`.
- Cualquier `JOIN order ↔ customer` por `customer_id` devuelve **cero filas**.
  Es un error silencioso: no falla, da vacío.
- El mismo nombre significa dos cosas según el módulo: en `customers/{id}` es un
  `customer_id`, y en el cuerpo de un pedido es un `user_id`.

Arreglo posible sin migrar datos: renombrar la propiedad a `customerUserId` en
los DTOs y en la entidad, dejando la columna como está, para que el nombre diga
la verdad. Migrar la FK a `customer.customer_id` es más correcto pero toca datos.

---

## Cuarta tanda — barrido de autenticación endpoint por endpoint

Se llamó a los 131 endpoints **sin cabecera de autorización** y con un cuerpo
inválido, para ver cuáles exigen token de verdad. Resultado: **115 lo exigen,
15 no**.

### H-26 · `GET /users/email/{email}` expone el usuario completo sin token — **seguridad, crítico**
Sin autenticación alguna devuelve **200** con el registro entero:

```
user_id · firebase_uid · role.type ("super_admin") · full_name
email · phone_number · phone_verified · email_verified · blocked
```

Comprobado contra `superadmin@splg.com`: se obtiene el `firebase_uid` y el
teléfono del super administrador con una sola petición y sin credenciales.

Está marcado `@Public()` en `users.controller.ts`. Probablemente se abrió para
que el registro pudiera comprobar si un email ya existe, pero para eso ya está
`check-exists`, que devuelve sólo booleanos.

Arreglo: sacarle el `@Public()`, o que devuelva únicamente `{ exists: boolean }`.

### H-27 · `POST /users/check-exists` permite enumerar cuentas — **seguridad, medio**
Es público y responde `{"exists":true,...}`. Permite averiguar qué correos y
teléfonos están registrados. Es el complemento de H-26 y conviene resolverlos
juntos (limitar por IP, o exigir token).

### H-28 · `check-exists` no valida nada — **calidad, medio**
Recibe `@Body() body: { email?: string; phoneNumber?: string }`, un tipo literal
sin DTO. Enviándole `{"email": 12345}` responde **201**, no 400. Es otro de los
11 endpoints sin DTO, y la consecuencia es la misma que en H-24.

### Los 15 que no exigen token
Cinco son correctos y esperables: los tres de salud, los dos de login. Los otros
diez conviene revisarlos uno por uno:

`POST /admin/first-superadmin` · `POST /email/password-reset` · `POST /email/test` ·
`GET /gascylinder` · `GET /gascylinder/available/list` · `GET /time-slot/availability` ·
`POST /users` · `POST /users/check-exists` · `GET /users/email/{email}`

`GET /gascylinder` y `GET /time-slot/availability` son catálogo público y tienen
sentido. `POST /users` crea un usuario sin autenticación y `POST /email/test`
manda correos sin autenticación: los dos merecen una mirada.

---

## Quinta tanda — cuerpos de petición escritos a mano para los 41 endpoints con cuerpo

### H-29 · Los roles se buscan por su texto, no por su identificador — **arquitectura, alto**
`CustomersService.registerWithUser` y sus equivalentes resuelven el rol haciendo
`findOne({ where: { type: 'customer' } })`. Si alguien **renombra** el rol desde
`PATCH /role/{id}`, el registro de clientes deja de funcionar con un
`500 — Customer role not found`.

Lo comprobé sin querer: la batería renombró el rol `customer` y el registro se
cayó hasta que lo restauré. No hay nada en el sistema que impida renombrar o
borrar un rol del que depende el código.

Arreglo: una constante o un enum como única fuente, y que los roles del sistema
no se puedan renombrar ni borrar desde la API (o que el endpoint los proteja).

### H-30 · El reseteo de contraseña no está configurado — **entorno, medio**
`POST /email/password-reset` responde
`400 — Error generating reset link: Domain not allowlisted by project`.
Es configuración de Firebase: falta autorizar el dominio en el proyecto
`splg-gas`. El endpoint está bien; el proyecto no está terminado de configurar.

### Reglas de negocio que impiden probar el camino feliz con datos estáticos
No son defectos. Quedan documentados en la colección para que se sepa qué hace
falta antes de ejecutarlos:

| Endpoint | Qué necesita |
|---|---|
| `POST /ratings` | El pedido tiene que estar entregado **y** el token ser el del cliente dueño |
| `POST /admin/first-superadmin` | Sólo funciona si todavía no existe ningún super admin |
| `POST /cylinders/assign` | El envase tiene que estar en `filled`, no en `in_depot` |
| `PATCH /cylinders/{id}/transition` | La transición tiene que ser válida desde el estado actual |
| `PATCH /orders/{id}/status` | La transición tiene que ser válida desde el estado actual |
| `PATCH /orders/{id}/cancel` | El pedido no puede estar finalizado |
| `POST /orders/{id}/confirm-delivery` | Hace falta el código real de `GET /orders/{id}/delivery-code` |
| `POST /email/change-email` | Hace falta un `idToken` real de Firebase |

---

## Sexta tanda — la colección completa corrida con newman

369 peticiones, **1246 aserciones, 72 fallos**. Al mirarlos apareció el hallazgo
que ata todo lo anterior.

### H-31 · Los 11 endpoints sin DTO devuelven 500 si se los llama sin cuerpo — **defecto, crítico**

La cadena completa, verificada paso por paso:

1. El endpoint declara el cuerpo con un tipo literal en línea
   (`@Body() body: { block: boolean }`) en vez de una clase DTO.
2. Como no hay clase, **Swagger no puede inferir el esquema**: el OpenAPI
   generado **no declara `requestBody`** para ninguno de los 11. Comprobado:
   `PATCH /users/{id}/block`, `PATCH /gascylinder/{id}/stock`,
   `PATCH /delivery/{id}/balance`, `POST /notifications/token`,
   `POST /users/check-exists` y `PATCH /customers/{id}/location` salen todos
   con `requestBody: NO`, mientras que `POST /orders` y `POST /gascylinder`,
   que sí tienen DTO, salen con `requestBody: SI`.
3. Quien lea la documentación no sabe que hay que mandar un cuerpo.
4. Si lo llama sin cuerpo, el handler recibe `undefined` y revienta.

Prueba directa sobre `PATCH /users/{id}/block`:

```
sin cuerpo        -> 500 {"statusCode":500,"message":"Internal server error"}
{"block": false}  -> 200
```

**Los 23 errores 500 de la corrida completa salen todos de acá.** Son los mismos
11 endpoints, contados una vez por su caso correcto y otra por el de identificador
inexistente:

`PATCH /customers/{id}/location` · `PATCH /delivery/{id}/balance` ·
`PATCH /delivery/{id}/location` · `PATCH /delivery/{id}/status` ·
`PATCH /delivery/user/{id}/availability` · `PATCH /gascylinder/{id}/stock` ·
`PATCH /users/{id}/block` · `POST /notifications/order-confirmation` ·
`POST /notifications/send-test` · `POST /notifications/token` ·
`POST /users/check-exists`

**Por qué importa más de lo que parece:** no es que el endpoint sea frágil ante
una llamada rara. Es que la única documentación que tiene el sistema —el
OpenAPI— **no dice que haya que mandar un cuerpo**, así que la llamada
equivocada es la que uno haría leyendo la documentación. El panel y las apps no
lo sufren porque mandan el cuerpo "de memoria", pero cualquiera que se integre
desde afuera pega contra un 500 en el primer intento.

Escribir los 11 DTOs arregla las tres cosas de una vez: valida la entrada,
documenta el contrato en Swagger, y convierte el 500 en un 400 con motivo.

### H-32 · Descartado
En la corrida completa, `POST /users` y `GET /time-slot/availability` dieron 500,
pero **no se reproducen aislados**: llamados uno por uno responden 201 y 200.
Fueron fallos dependientes del estado que dejó la propia corrida (un dato
borrado un momento antes, o el mismo cuerpo enviado dos veces seguidas).

Se verificó además que la creación de un usuario duplicado responde
**400 "Duplicate entry"**, que es lo correcto: `handleDBExceptions` sí contempla
el código `23505`. No hay defecto acá.

---

## Séptima tanda — los 8 casos de uso sin endpoint propio

Ninguno de estos ocho tenía un endpoint mapeado en la auditoría de cobertura,
pero siete de ellos **sí son funcionalidad dentro de otros endpoints** (una
franja horaria en el alta de pedido, una seña, un estado, un campo de
promociones). Se los ejercitó de verdad y se miró el efecto en la base.

| CU | Cómo se probó | Resultado |
|---|---|---|
| CU-031 Registrar Chofer | `POST /users/delivery-registration` | **Anda.** 201 y queda la fila en `delivery` |
| CU-039 Promociones por cantidad | `POST /gascylinder` con `promotions` | **Anda.** Se guarda `[{"quantity":3,"discountPercentage":10}]` |
| CU-044 Franja horaria al crear pedido | `POST /orders` con `timeSlotId` | **Anda.** El pedido queda con su `time_slot_id` |
| CU-072 Reserva programada con seña | `POST /orders` con `isReservation` y `depositAmount` | **Anda.** Queda `status=reserved`, `deposit_amount=2000`, `deposit_paid=false`, con fecha y franja |
| CU-018 Marcar "En Camino" | `PATCH /orders/{id}/status` como chofer | **Anda.** El pedido pasa a `on_the_way` |
| CU-020 Confirmar Entrega | `GET /orders/{id}/delivery-code` + `POST /orders/{id}/confirm-delivery` | **Anda.** El pedido queda `delivered` |
| CU-009 Cancelar Pedido (Chofer) | `PATCH /orders/{id}/cancel` como chofer | **Anda, pero el nombre engaña** (ver H-33) |
| CU-013 Ofrecer al chofer más cercano | Alta de pedido y espera del cron | **No se puede probar** (ver H-20) |

### H-33 · El chofer no cancela el pedido: lo libera — **naming, medio**
`PATCH /orders/{id}/cancel` llamado por un chofer devuelve **200** y el pedido
queda en **`pending`**, no en `cancelled`. Es deliberado y está bien hecho:

```ts
// cancel-order.use-case.ts
if (role === 'driver') {
  transitionOrder(order, OrderStatus.PENDING);
  order.delivery_id = null;
  order.acceptedAt = null;
  order.onTheWayAt = null;
  return false;   // no devuelve el stock
}
```

El chofer suelta el pedido para que lo tome otro. El problema es que **el
endpoint, el caso de uso y la documentación lo llaman "cancelar"**, y quien lea
la respuesta ve un 200 y supone que el pedido se canceló.

Además, al pedido liberado se le graba igual un `cancellationReason`, así que
queda un pedido vivo en `pending` con un motivo de cancelación escrito.

Arreglo: separarlo en `POST /orders/{id}/release` (o `/reject`, que ya existe),
dejar `/cancel` para cancelar de verdad, y no escribir `cancellationReason`
cuando el pedido sigue vivo.

### H-34 · `POST /coverage-zones` no valida el orden de las coordenadas — **defecto, medio**
El DTO declara `polygon` sólo con `@IsArray()`. Pasando los puntos como
`[lat, lng]` en vez de `[lng, lat]`, el endpoint responde **201** y guarda una
zona cuyo centro queda en `lat=-55.88, lng=-27.36` — o sea, en medio del
Atlántico Sur en vez de Posadas.

Lo comprobé sin querer: las zonas de prueba que creó la batería quedaron todas
invertidas, y ninguna cubre nada. No hay error, no hay aviso: la zona queda
inservible y sólo se nota cuando un pedido se rechaza por "fuera de la zona de
cobertura".

Arreglo: un DTO que valide la forma del polígono (pares numéricos, latitud
entre -90 y 90, longitud entre -180 y 180, primer punto igual al último) y que
documente el orden esperado.

---

## Octava tanda — la colección corrida entera con newman

380 peticiones, 1319 aserciones, 62 fallos. Catorce de esos fallos son
**intencionales**: documentan H-02 y H-31 y pasan solos cuando se arreglen.
De los demás salió un hallazgo nuevo.

### H-35 · Ningún parámetro de consulta se valida — **defecto, alto**

Los parámetros de **ruta** sí se validan: **66 de 72 `@Param` usan un pipe**
(`ParseUUIDPipe` sobre todo). Los de **consulta**, ninguno:
**0 de 27 `@Query` usa un pipe**.

La consecuencia, verificada:

```
GET /api/time-slot/availability?date=&distributor=jeny-gas
  -> 500  invalid input syntax for type date: ""
```

El `date` vacío viaja crudo hasta Postgres. Debería ser un 400 diciendo que la
fecha es obligatoria y con qué formato.

Lo llamativo es que **el equipo ya sabe hacerlo**: lo aplica en 66 parámetros de
ruta. Nunca se llevó a los de consulta. Nest trae los pipes hechos
(`ParseUUIDPipe`, `ParseIntPipe`, `ParseBoolPipe`, `ParseDatePipe`) y también se
puede usar un DTO de consulta con `@Query()` y `class-validator`, que es lo
razonable donde hay más de un parámetro.

Es el mismo problema que H-31 pero en la otra puerta de entrada: sin validación
en el borde, la base termina siendo el validador, y la base contesta con 500.

### H-36 · Recuento de las tres puertas de entrada

| Puerta | Cuántas | Validadas | Consecuencia medida |
|---|---:|---:|---|
| Parámetros de ruta (`@Param`) | 72 | **66** | — |
| Cuerpo (`@Body`) | 50 | **39** | 11 sin DTO: 500 sin cuerpo (H-31) |
| Consulta (`@Query`) | 27 | **0** | `?date=` vacío da 500 (H-35) |

Resumen: **de 149 puntos de entrada de datos, 44 no se validan.** Todos los 500
encontrados en toda la revisión salen de ahí.

### H-37 · `POST /users` con un rol inexistente devuelve 500 — **defecto, alto**
Reproducible en una sola llamada:

```
POST /api/users  { ..., "role_id": "00000000-0000-4000-8000-000000000000" }
  -> 500 {"message":"Unexpected error, check server logs"}
```

Debería ser un 400 o un 404 diciendo que el rol no existe. Y el log **no
registra la causa**, otra vez por H-23: `handleDBExceptions` convierte cualquier
error que no reconozca en un 500 opaco sin escribir el original.

Apareció solo: la colección crea un rol en el módulo Role, lo borra al final del
módulo, y después el módulo Users intenta crear un usuario con ese rol. Es
exactamente lo que pasaría en producción si se borra un rol que todavía se está
usando en un formulario abierto.

### H-38 · El código de respuesta declarado no coincide con el real — **contrato, medio**
Cuatro endpoints declaran `200` en el OpenAPI y devuelven `201`:

`POST /notifications/token` · `POST /notifications/send-test` ·
`POST /notifications/order-confirmation` · `POST /users/check-exists`

Los cuatro son de los once sin DTO (H-31), así que la declaración de Swagger sale
incompleta y además equivocada. Un cliente generado desde ese OpenAPI que valide
el código de respuesta se rompe.

`check-exists` es el más discutible: no crea nada, es una consulta; devolver 201
no corresponde.

---

## Novena tanda — al empezar a arreglar

### H-39 · La respuesta del login no se puede ni serializar — **seguridad, crítico**
Amplía y confirma H-02.

Al registrar `ClassSerializerInterceptor` como interceptor **global** —que es lo
que Nest propone para no devolver entidades crudas— el login pasó a responder
**500**:

```
RangeError: Maximum call stack size exceeded
  at TransformOperationExecutor.getKeys (class-transformer)
```

El objeto `UserCredential` que devuelve el SDK de Firebase tiene **referencias
circulares**, así que `class-transformer` entra en recursión infinita al
intentar convertirlo.

Lo que esto demuestra: no es que al login "se le escape" un campo de más. Es que
**devuelve un objeto del proveedor entero, tan crudo que ni siquiera es
serializable**. Cualquier cosa que quiera procesar esa respuesta —un
interceptor, un log estructurado, un cliente generado— se rompe.

**Consecuencia para el orden de trabajo:** el `ClassSerializerInterceptor`
global **no se puede habilitar hasta que el login devuelva un DTO**. Se movió
del paso transversal al módulo de Auth, donde se hacen las dos cosas juntas.

### Hecho en el paso transversal

- **Versionado por URI con `VERSION_NEUTRAL`** (`main.ts`). Las rutas de hoy
  siguen respondiendo en `/api/...` sin cambiar nada; cuando haya que corregir
  el contrato de un endpoint se marca el nuevo con `@Version('2')` y conviven.
  Es lo que permite arreglar el login sin romper las apps publicadas.
- **H-06 resuelto:** `TimeoutInterceptor` se registraba dos veces (en `main.ts`
  con `useGlobalInterceptors` y en `AppModule` como `APP_INTERCEPTOR`). Queda
  sólo el de `AppModule`.

Verificado: la colección da los mismos 31 fallos conocidos, ninguno nuevo.
