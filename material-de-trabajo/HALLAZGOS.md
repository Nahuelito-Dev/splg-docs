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

> **Corrección del 2026-09-23.** La segunda parte de este hallazgo estaba mal.
> Decía que al pedido liberado se le grababa igual un `cancellationReason`.
> **No es así:** el motivo se escribe sólo cuando el pedido realmente se
> cancela, y el código lo comenta explícitamente
> (`cancel-order.use-case.ts`: *"driver solo lo libera a PENDING y no lleva
> motivo de cancelación"*). Verificado contra los datos: **0 pedidos vivos
> tienen motivo de cancelación**, y el `acceptedAt` se limpia correctamente al
> liberar.
>
> Lo que queda de este hallazgo es **sólo el nombre**: la operación se llama
> "cancelar" y para el chofer libera. El comportamiento es correcto y
> deliberado.
>
> De paso apareció otra cosa: hay **3 pedidos cancelados sin motivo**
> (`cancellationReason` en NULL). El motivo es opcional en el DTO, así que se
> puede cancelar sin decir por qué.

Arreglo: separarlo en `POST /orders/{id}/release` (o `/reject`, que ya existe),
dejar `/cancel` para cancelar de verdad, y no escribir `cancellationReason`
cuando el pedido sigue vivo.

### H-34 · `POST /coverage-zones` no validaba el contenido del polígono — **defecto, medio · CORREGIDO Y REENCUADRADO**

> **Corrección del 2026-09-23.** El encuadre original de este hallazgo estaba
> mal. Decía que el endpoint permitía crear zonas inservibles por invertir las
> coordenadas, y que eso pasaba en la práctica. **No es así:** el panel convierte
> correctamente de `[lat, lng]` (Leaflet) a `[lng, lat]` (GeoJSON) en
> `CoverageZones.tsx:117`, con el comentario que lo explica. Las zonas invertidas
> que aparecieron en la base **las creó el script de pruebas, no la aplicación**.
>
> Lo que sí era cierto, y se corrigió: el DTO declaraba el polígono sólo con
> `@IsArray()` y `@ArrayMinSize(3)`, sin mirar el contenido. Un punto con un
> solo valor, o una latitud de -999, pasaban de largo hasta PostGIS.
>
> Además hay un límite que conviene tener presente: **invertir las coordenadas
> no se puede detectar por rango** cuando los dos valores son plausibles.
> `[-27.36, -55.90]` leído como `[lng, lat]` es un punto válido en el Atlántico
> Sur. La validación atrapa lo imposible, no lo improbable. Si en algún momento
> se quiere que el error sea irrepresentable, hay que cambiar el contrato a
> puntos con nombre: `{"lat": -27.36, "lng": -55.90}`.

#### Texto original del hallazgo
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

### H-40 · Bloquear un usuario no hacía nada — **seguridad, crítico**
El panel tiene un botón para bloquear usuarios y `PATCH /users/{id}/block`
escribía `blocked = true` en la base. **Nadie leía ese campo**: ni el guard, ni
el login, ni ningún servicio.

Comprobado en vivo antes de arreglarlo, con un cliente bloqueado:

```
PATCH /users/{id}/block  {"block": true}      -> 200  (blocked = true en la base)
POST  /auth/login                             -> 200  con token
GET   /customers/user/{id}                    -> 200
GET   /user-address/user/{id}                 -> 200
GET   /orders/customer/{id}                   -> 200
```

El usuario bloqueado seguía operando con normalidad en todos sus endpoints.

**Arreglado en el guard, no en el login.** Es importante que sea así: el panel y
las dos apps se autentican con el SDK de Firebase y **nunca pasan por
`/auth/login`**; el guard es el único punto por el que pasan todas las
peticiones. Puesto ahí, el bloqueo corta el acceso **en el acto**, incluso para
un token ya emitido, sin esperar a que expire.

Verificado después del arreglo:

```
con el token que ya tenía   -> 401 "La cuenta está bloqueada..."
volviendo a loguearse       -> 401 "La cuenta no está habilitada"
tras desbloquear            -> 200
```

### H-41 · Nadie consume los endpoints de acceso — **hallazgo de contexto**
Ni el panel ni las dos apps llaman a `POST /api/auth/login` ni a
`/auth/login/dashboard`. Los tres se autentican con el SDK de Firebase
(`signInWithEmailAndPassword`) y le mandan a la API sólo el token resultante.

Se verificó buscando llamadas HTTP a `/auth` en `splg-app-admin/src` y en
`lib/` de las dos apps: no hay ninguna.

Esto tiene dos consecuencias:
1. Corregir la respuesta del login **no rompía a ningún cliente**, así que se
   pudo hacer directo sin necesidad de versionar ese endpoint.
2. Toda validación de acceso tiene que vivir en el **guard**, no en el login,
   porque el login es un camino que en la práctica nadie recorre.

---

## Décima tanda — el front contra la API, llamada por llamada

Se extrajeron todas las rutas que llaman el panel y las dos apps, y se
compararon contra las que la API realmente expone. Lo que dio sospechoso se
verificó llamándolo de verdad, porque el extractor tiene falsos positivos.

| Cliente | Rutas distintas | Que no existen |
|---|---:|---:|
| Panel | 59 | **2** |
| App cliente | 20 | **2** |
| App chofer | 11 | 0 |

### H-42 · El botón de cancelar pedido del panel no funciona — **defecto, alto**

El panel manda en el cuerpo `userId: 'ADMIN_PANEL'` y `role: 'admin'`, además
del motivo. El `ValidationPipe` global tiene `forbidNonWhitelisted: true`, así
que responde:

```
400 {"message":["property userId should not exist","property role should not exist"]}
```

El backend toma el actor del token —lo dice su propia descripción, *"El actor
(id + rol) sale SIEMPRE del token autenticado, nunca del body (evita IDOR)"*—,
así que esos dos campos sobran desde que se hizo ese cambio y nadie actualizó
el panel.

**Corregido** en `splg-app-admin/src/services/api/orders.ts`. Verificado dos
veces: el pedido queda `cancelled` y el motivo se guarda.

### H-43 · El botón de crear cliente del panel apunta a un endpoint inexistente — **defecto, alto**

`createCustomer` llama a `POST /users/customer-registration-admin`, que **no
existe**: responde 404. Está conectado al formulario en
`Customers.tsx:40`, así que el alta de clientes desde el panel no funciona.

La API sí tiene `POST /users/customer-registration`, pero es público y no
recibe distribuidora. **No se corrigió acá** porque apuntarlo sin más implica
decidir qué debe hacer el alta desde el panel: si asigna la distribuidora del
admin, si exige verificación de correo, si permite fijar la contraseña. Es una
decisión de producto, no un cambio mecánico. Queda como ítem de desarrollo.

### H-44 · La app cliente llama a dos rutas que no existen — **defecto, medio**

`PATCH /orders/{id}` y `PUT /orders/{id}`, desde
`order_remote_datasource.dart`. Las dos responden 404: la API no expone
actualización genérica de un pedido, sólo las transiciones específicas
(`/status`, `/cancel`, `/arrived`, `/confirm-delivery`).

Falta determinar qué pantalla de la app las dispara y qué esperaba hacer.

### H-45 · El panel llama a `/users/validate`, que no existe — **código muerto**

`checkToken()` apunta a `POST /users/validate` → 404. Pero `checkIfTokenExpired`,
que es quien lo usa, **no se llama desde ninguna pantalla**. Es código muerto:
la llamada rota nunca se ejecuta.

Conviene borrarlo o conectarlo, pero no urge.

### H-46 · El motivo de cancelación no vuelve en la respuesta — **contrato, bajo**

El motivo **se guarda bien** en la base, pero el DTO de respuesta del pedido no
lo incluye, y el panel lo tiene declarado en su tipo
(`cancellationReason?: string | null`). Siempre lo vería vacío.

### H-47 · Se puede cancelar un pedido sin decir por qué — **datos, bajo**

`reason` es opcional en `CancelOrderDto`. Hay **3 pedidos cancelados con el
motivo en NULL**. Para una cancelación de admin, el motivo debería ser
obligatorio.

---

## Camino crítico de la demo — verificado contra la API corriendo

Tres corridas consecutivas de `demo_e2e.py`, **19/19 pasos en verde** en las tres:
registro de cliente desde la app y de chofer desde el panel, login de ambos, alta
de garrafa, dirección del cliente, pedido desde el cliente, pool del chofer,
asignación, aceptación, en camino, tres posiciones de tracking, aviso de llegada,
código de entrega, confirmación y calificación.

Las dos fallas de la primera corrida **eran del guion de prueba, no del sistema**:
la dirección caía fuera de la única zona activa, y el assign recibía un `user_id`
donde espera un `delivery_id`. Quedan anotadas abajo como H-48 y H-49.

### H-48 · El chofer se identifica con dos claves distintas en el mismo módulo — **contrato, medio**

`PATCH /orders/:id/assign/:deliveryId` resuelve al chofer por `delivery_id`, pero
el gateway de tiempo real lo identifica por `user_id` (sala `driver_<userId>`, y
Redis GEO indexado por `user_id`). Quien integra contra el módulo de pedidos tiene
que saber cuál de las dos claves va en cada llamada, y no hay nada en el contrato
que lo diga: el parámetro se llama `deliveryId` en un lado y `userId` en el otro
sin que la diferencia esté documentada.

No es un bug — cada endpoint hace lo que dice su código — pero es la clase de
inconsistencia que hace fallar una integración y cuesta encontrar. Conviene
unificar o, como mínimo, dejarlo explícito en el Swagger de ambos.

### H-49 · Una sola zona de cobertura activa — **dato, informativo**

La única zona activa es **Itaembé Miní** (centro `-27.41, -55.965`). Cualquier
dirección fuera de ese polígono hace fallar el alta de pedido con 400 "La
dirección está fuera de la zona de cobertura". No es un defecto: el control
funciona como debe. Se anota porque condiciona los datos de la demo — las
direcciones de prueba tienen que caer adentro.

### H-50 · El DTO de registro de token FCM pide un `userId` que después ignora — **contrato, bajo**

`POST /notifications/token` fuerza el `userId` al del token autenticado cuando
quien llama no es admin (protección anti-secuestro, correcta). Pero el DTO sigue
exigiendo `userId` como UUID obligatorio, así que la app cliente tiene que mandar
un dato que el backend descarta, y si lo omite recibe un 400 confuso
("userId debe ser un UUID"). Debería ser opcional y documentado como "solo admin".

## CU-011 (aviso de llegada) — dos de los tres pendientes, resueltos

El CU registraba tres limitaciones. Decisión tomada: **no se agrega el estado
ARRIVED**, el ciclo de vida sigue teniendo cinco estados operativos como dice la
documentación. El aviso de llegada se mantiene como notificación, no como estado.

Los otros dos sí se resolvieron:

1. **Solo el chofer asignado puede avisar la llegada.** Antes, cualquier chofer
   autenticado podía disparar el aviso de un pedido ajeno. Ahora se verifica la
   pertenencia reutilizando el mismo criterio que ya aplicaba el código de
   entrega, extraído a un helper (`assertPedidoDelChofer`) en vez de duplicarlo.
   El administrador sigue habilitado, que es lo que el CU describe.
   Verificado contra la API: chofer ajeno → 403, chofer asignado → 200, admin → 200.

2. **El aviso ahora también sale por push, no solo por socket.** Con la app
   cerrada el socket no llega y el aviso se perdía, que era justamente el caso
   que el CU quería cubrir. El push es best-effort detrás del puerto de
   notificaciones (el service no conoce Firebase) y nunca rompe el flujo: si
   falla, el aviso en tiempo real ya salió.

---

## Decisiones tomadas el 23/09 — pendientes del lado de los clientes

Las tres están decididas pero **no ejecutadas**: primero se termina el backend.

### D-1 · El panel no da de alta clientes

SS-16 tiene consultar, editar, validar y dar de baja, pero **ningún caso de uso
de alta de cliente por el administrador**: CU-002 dice que el cliente se registra
desde la App Cliente. El botón "Nuevo Cliente" del panel llama a
`/users/customer-registration-admin`, que no existe (404), así que hoy tampoco
funciona. Se saca el botón, no se construye el endpoint. La propia página ya se
describe como "clientes registrados desde la App", así que queda coherente.

Toca: `Customers.tsx` (botón y rama de alta de la mutation) y `customers.ts`
(`createCustomer`).

### D-2 · Un pedido no se modifica: se cancela

No existe caso de uso de modificar un pedido ya hecho. La app cliente tiene una
pantalla que lo intenta contra `PATCH`/`PUT /orders/{id}`, dos rutas que no
existen (H-44), así que hoy muestra "No se pudo modificar la orden". Se saca el
flujo completo, no se construye el endpoint.

Toca en la app cliente: el botón "Modificar" de `history.dart`, `modifyOrder` en
`history_model.dart`, el estado de edición en `cart_service.dart`, la rama de
edición de `checkout_viewmodel.dart` y `updateOrder` en `history_service.dart`,
el repositorio y el datasource.

**Lo que se creía que faltaba, ya está.** El caso real detrás del pedido "editable"
era otro: poder mandar el pedido a una dirección distinta de la del registro —
comprarle una garrafa a la madre, por ejemplo. Eso **ya funciona**, verificado
contra la API: un cliente puede tener varias direcciones, listarlas (CU-046) y
crear el pedido apuntando a la que quiera; usar la dirección de otra persona
devuelve 404. La app además ya tiene el selector de direcciones en el checkout.

### D-3 · Cancelar devuelve el 90% — **regla nueva, falta en el CU**

Decisión de negocio del 23/09: cuando el cliente cancela, se le devuelve el
**90% del costo del pedido** y la distribuidora retiene el 10%.

CU-008 hoy **no dice nada de reembolso**: sólo marca el pedido como cancelado y
restituye el stock. Hay que incorporar la regla al caso de uso, y al DSS y DSD
correspondientes.

No se puede implementar todavía: el reembolso necesita la integración de cobro,
que está fuera del alcance de la demo. Para los pedidos en efectivo no aplica
(no hubo cobro previo). Queda pendiente de definir qué pasa con una cancelación
del administrador y si el 10% se retiene igual cuando cancela la distribuidora.

### H-51 · Cualquiera puede escuchar el pedido de otro en vivo — **seguridad, ALTO**

Los dos gateways validan el token al conectar y después **lo ignoran**: la sala
se arma con el identificador que manda el cliente en el cuerpo del mensaje.

- `drivers.gateway.ts:75-84` — `client.join(\`driver_${data.driverId}\`)`
- `customers.gateway.ts:55-66` — `client.join(\`customer_${data.customerId}\`)`

**Verificado contra la API corriendo**, no leído: se crearon dos clientes, se
dejó un pedido de uno en camino, y el otro —autenticado con SU propio token— se
unió a la sala ajena y recibió el aviso de llegada del pedido que no era suyo:

```
>>> ESPIO EL PEDIDO AJENO: {"orderId":"567e4b83-...","message":"El repartidor
    esta afuera!","driverName":"Chofer"}
```

Con un `user_id` ajeno se sigue en vivo la entrega de cualquier persona: su
posición, su domicilio y sus avisos. Los `user_id` no son secretos —aparecen en
respuestas de la API que otros roles sí pueden ver—, así que no hace falta
adivinarlos.

**Por qué está así y por qué el arreglo no es de una línea:** el token de
Firebase trae el `uid` y el email, no el `user_id` interno de la base
(`auth.service.ts:115-129`), que es con lo que se arman las salas. Por eso el
código lo toma del payload. El arreglo correcto es resolver el usuario interno
en `handleConnection`, una sola vez por conexión, guardarlo en el socket e
ignorar lo que mande el cliente. De paso conviene validar el rol: hoy un cliente
puede conectarse al namespace de choferes.

Es el mismo defecto que tiene Tutu con sus salas nombradas por email. No se
importó de ahí: los dos lo tienen por separado.

---

## Encontrados durante la alineación a Nest — 24/09

Aparecieron mientras se alineaban los módulos. Se anotan y **no** se corrigen
sobre la marcha, porque arreglarlos cambia el comportamiento de la API.

### H-52 · Un cliente se puede validar a sí mismo — **seguridad, ALTO**

> **Resuelto el 24/09.** `validated` sólo lo manda un administrador (un cliente recibe 403) y `user_id` salió del DTO. Verificado contra la API.

`UpdateCustomerDto` deriva de `CreateCustomerDto` con todos sus campos, así que
`PATCH /customers/:id` acepta `validated` y `user_id` de parte del propio
cliente. El control de propiedad sólo mira que el perfil sea suyo, no qué campos
toca.

**Verificado contra la API corriendo:** un cliente con `validated: "false"`
mandó `PATCH /customers/{su id}` con `{"validated":"true"}`, recibió 200 y quedó
validado. Se le devolvió el valor original después de la prueba.

El arreglo es un DTO de modificación propio para el cliente, sin `validated` ni
`user_id`. La validación ya tiene su endpoint de administrador
(`PATCH /customers/:id/validate`).

### H-53 · El chequeo de salud se cae bajo carga normal — **operación, medio**

`/health` exige que el proceso use menos de 300 MB de memoria residente. Con la
batería de Postman completa el proceso los pasa y el chequeo responde 503. Un
balanceador de carga lo tomaría como una instancia caída y la sacaría de
servicio justo cuando hay tráfico. El umbral es de un proceso vacío, no de uno
trabajando.

### H-54 · El mismo evento de tiempo real tiene dos nombres — **contrato, bajo**

Cuando un pedido sale en camino, el cliente recibe `order:on-the-way` y el panel
`order:on_the_way`. Medido con sockets reales durante el recorrido del pedido.
Quien integre tiene que saber que cambia según el namespace.

### H-55 · La asignación manual no le avisa al chofer por tiempo real — **a revisar contra CU-012**

Cuando el administrador asigna un pedido a mano, el socket del chofer no recibe
ningún evento (sí lo recibe en el despacho automático). Puede ser correcto si el
aviso va sólo por push; hay que contrastarlo con lo que especifica CU-012.

### H-56 · El informe de ventas por producto sale vacío — **defecto, ALTO para el panel**

> **Resuelto el 24/09.** Los alias se entrecomillan con `select(expresión, alias)`. Verificado contra la base: Garrafa 10kg en 2026, 182 unidades y $2.711.800.

`GET /reports/sales-by-product` responde cada fila sin el tipo de producto y con
`totalQuantity` y `totalSales` en `null`. La causa: Postgres pasa a minúsculas
los alias sin comillas (`AS productType` llega como `producttype`) y el servicio
lee `row.productType`, que no existe. `Number(undefined)` da `NaN`, que en el
JSON sale `null`. Se ve en la corrida de referencia de Postman, no sólo en el
código. El arreglo es entrecomillar los alias o leerlos en minúsculas. Afecta
CU-028.

### H-57 · La granularidad semanal se acepta y se ignora — **contrato, bajo**

`GET /reports/sales-evolution?granularity=week` pasa la validación (el DTO
admite `week`) pero el controlador trata todo lo que no es `month` como `day`.
Quien pide la evolución semanal recibe la diaria sin aviso. Afecta CU-030.

### H-58 · Un endpoint público manda mails a cualquier dirección — **seguridad, medio**

> **Resuelto el 24/09.** `POST /email/test` exige super administrador.

`POST /email/test` es `@Public()` y, con sólo pasarle un correo, genera dos
links de restablecimiento en Firebase y manda un mail real a esa dirección. Un
tercero puede usar el backend para mandar correos a quien quiera y gastar el
cupo de Firebase y de Resend. Es un endpoint de prueba que quedó publicado: o
se saca, o se restringe a administradores.

### H-59 · Los links y el mail de bienvenida apuntan a otro proyecto — **defecto, ALTO**

> **Resuelto el 24/09.** Los links salen de `APP_URL` o, si falta, del dominio del propio proyecto de Firebase (`EnlacesDeLaApp`). Verificado: con el dominio nuevo Firebase genera el link sin error.

El link de "olvidé mi contraseña" se genera con `url:
'https://taolistic-courses.firebaseapp.com/__/auth/action'`
(`email.service.ts`), y el botón del mail de bienvenida lleva a
`https://taolistic-courses.firebaseapp.com/` (`email-template.provider.ts`). Es
el dominio de otro sistema: quien restablece su clave en SPLG termina en esa
página. Las plantillas además firman como "Yeni Gass". Hay que llevar la URL a
la configuración (`ConfigService`, con su entrada en Joi) y usar el nombre del
producto.

### H-60 · Una dirección se podía pasar a la cuenta de otro — **seguridad, ALTO**

> **Resuelto el 24/09.** `user_id` salió de `UpdateUserAddressDto`.

`PATCH /user-address/:id` aceptaba `user_id`. El control de propiedad miraba de
quién era la dirección *antes* del cambio, no a quién pasaba. **Verificado
contra la API:** un cliente pasó su dirección a otro cliente con 200, y la
dirección aparecía en la lista del otro, donde podía terminar elegida para un
pedido. Es el mismo patrón que H-52: un DTO de modificación que hereda todos
los campos del alta.

### H-61 · Cualquier usuario podía editar a cualquier chofer — **seguridad, CRÍTICO**

> **Resuelto el 24/09.** `PATCH /delivery/:id` exige administrador, y el de empresa sólo edita choferes de su distribuidora.

El endpoint no tenía restricción de rol. **Verificado contra la API:** un
cliente cambió la calificación de un chofer ajeno y recibió 200. También podía
cambiarle `validated` (habilitarlo para operar) e `isActive`.

### H-62 · Un admin de empresa podía hacerse super administrador — **seguridad, CRÍTICO**

> **Resuelto el 24/09.** Un admin que no es super_admin no puede asignar ese rol ni modificar a un super administrador.

`PATCH /users/:id` le pasaba al admin todos los campos, `role_id` incluido.
**Verificado contra la API:** el admin de una distribuidora se asignó el rol
de super administrador con 200 y pasó a ver todas las distribuidoras. Se le
restituyó el rol después de la prueba.

**Los cuatro (H-52, H-60, H-61, H-62) salieron de la misma revisión:** DTOs de
modificación que heredan todos los campos del alta, y endpoints que controlan
quién es el dueño del recurso pero no qué campos puede tocar.

### H-63 · Cualquiera podía darse de alta como super administrador — **seguridad, CRÍTICO**

> **Resuelto el 24/09.** `POST /users` exige administrador y un admin de empresa no puede crear un super administrador.

El endpoint era `@Public()` y guardaba el `role_id` que llegara en el cuerpo.
**Verificado contra la API:** sin token, se creó un usuario con rol
`super_admin` (201). Con una cuenta de Firebase creada con la clave pública que
viajan en las apps, eso bastaba para entrar al panel con todos los permisos.
La fila de prueba se borró.

### H-64 · Cualquier usuario manejaba a los choferes de cualquier distribuidora — **seguridad, ALTO**

> **Resuelto el 24/09.** Disponibilidad y ubicación: sólo el propio chofer o un admin. Lecturas de choferes: admin de la misma distribuidora o el propio chofer.

Los endpoints de `/delivery` sólo pedían estar autenticado. Un cliente podía
listar los choferes activos con su ubicación, leer el perfil de cualquiera,
moverle la posición y sacarlo de servicio.
**Verificado contra la API, después del arreglo:** el cliente recibe 403 en los
cuatro casos; un chofer, 403 sobre otro chofer; el propio chofer cambia su
disponibilidad (200) y el admin lee y lista (200).

### H-65 · Cualquier usuario leía la cuenta completa de cualquier otro — **seguridad, ALTO**

> **Resuelto el 24/09.** `/users/:id` y `/users/email/:email`: el propio usuario o un admin. `/users/phone/:phone`: sólo admin.

Los tres endpoints sólo pedían estar autenticado y devolvían la cuenta con
`firebase_uid`, direcciones, autos y perfiles de cliente y chofer.
**Verificado contra la API:** un cliente leyó la cuenta de otro usuario con
200. Después del arreglo, 403; las apps siguen leyendo su propia cuenta al
entrar (200).

### H-66 · Un admin de empresa lista usuarios de todas las distribuidoras — **seguridad, ALTO**

> **Resuelto el 24/09.** Decisión de nahue: cada distribuidora ve y administra sólo lo suyo. Con distribuidora en contexto, `users` muestra sólo sus choferes, sus admins y los clientes que le compraron; lo ajeno es 404. La cuenta de un cliente (compartido entre distribuidoras) la administra el administrador general. Verificado con dos distribuidoras: 20 casos.

Además de listar, un admin de empresa podía ver, editar, **bloquear y borrar** usuarios de cualquier distribuidora.

`GET /users` y `GET /users/:id` no se acotan a la distribuidora del admin. Los
clientes no pertenecen a ninguna distribuidora (sólo choferes y admins), así
que qué le corresponde ver es **decisión de producto**. Propuesta: sus
choferes, sus admins y los clientes que le compraron. Va con `users` en la
tanda 3.

### H-67 · El error de Firebase llegaba crudo al llamante — **seguridad, bajo**

> **Resuelto el 24/09.** El detalle queda en el log; el llamante recibe un mensaje fijo.

`POST /email/password-reset` devolvía la respuesta interna de Firebase
(`RESET_PASSWORD_EXCEED_LIMIT` y el JSON completo).

### H-68 · El reseteo de contraseña revelaba qué correos tienen cuenta — **seguridad, medio**

> **Resuelto el 24/09.** Mismo mensaje exista o no la cuenta.

Contestaba "sent successfully" si existía e "If the email exists…" si no;
Swagger decía que el mensaje era el mismo.

### H-69 · Un vehículo se le podía asignar a cualquier usuario — **seguridad, medio**

> **Resuelto el 24/09.** El dueño tiene que ser chofer de la misma distribuidora; si no, 404.

**Verificado contra la API:** asignarle el auto a un cliente o a un chofer de
otra distribuidora da 404. De paso: al editar, el control de patente
duplicada comparaba contra el auto ya mezclado por `preload` y nunca corría;
el duplicado sólo lo frenaba la restricción única de la base. DSD CU-034,
CU-051 y CU-111 actualizados (CU-111 además decía `ConflictException`).

### H-70 · Un alta repetida borraba la cuenta del usuario existente — **seguridad, CRÍTICO**

> **Resuelto el 24/09.** La compensación borra sólo la cuenta de Firebase que creó la misma llamada, por su uid.

`registerWithUser` (clientes y choferes) compensaba cualquier error con
`deleteUserByEmailSafe(dto.email)`. Con un email ya registrado, el alta fallaba
y el rollback borraba de Firebase la cuenta de quien ya existía. El alta de
clientes es pública: sin token, cualquiera dejaba sin acceso a cualquier
usuario, super administrador incluido, sabiendo sólo su email.
**Verificado contra la API:** después del alta repetida, la víctima (cuenta
descartable) ya no podía entrar. Con el arreglo, sigue entrando. La propia
batería lo disparaba en cada corrida (el paso 3 repite el alta del paso 1).

### H-71 · El panel no puede crear clientes — **defecto, ALTO**

> **Resuelto el 24/09** con la unificación de las altas: el panel crea clientes por `POST /users` con rol `customer` (rama `feature/alta-unificada` del panel).

El panel llama a `POST /users/customer-registration-admin`, que no existe en el
back (404). Se resuelve con la unificación de las altas.

### H-72 · `POST /users` crea usuarios que no pueden entrar — **defecto, ALTO**

> **Resuelto el 24/09.** Toda alta crea la cuenta de acceso en la misma operación. Decisión de nahue: los usuarios viejos sin cuenta se borraron (14 en la base de desarrollo: 10 de `qa_pruebas` que creaba la batería vieja, 3 clientes de prueba y 1 sin rol ni correo). **No se tocaron** los 30 de `@demo.splg.com`: son los datos de `seed:demo`, que no tienen cuenta a propósito y sostienen 183 pedidos de muestra.

CU-082 guarda la fila en la base pero no crea la cuenta en Firebase; la
contraseña que manda el panel se descarta. Hoy hay 43 usuarios sin
`firebase_uid` (27 clientes, 6 choferes, 10 de QA). Además el DTO acepta
`firebase_uid` del cuerpo. Se resuelve con la unificación de las altas.

### H-73 · Un admin de empresa podía hacerse pasar por usuarios de otra distribuidora — **seguridad, CRÍTICO**

> **Resuelto el 24/09.** `PATCH /users/:id` tiene DTO propio (sin correo, rol ni cuenta de acceso) y un admin de empresa sólo modifica choferes y admins de su distribuidora.

`UpdateUserDto` heredaba todos los campos del alta.
**Verificado contra la API:** el admin de Jeny Gas le cambió el correo a un
chofer de otra distribuidora (200). El acceso identifica al usuario por el
correo del token, así que alcanzaba con poner un correo propio para entrar como
esa persona. Se restauró el correo después de la prueba. Con el arreglo: 404.

### H-74 · Borrados físicos y soft delete parcial — **auditoría, ALTO, ABIERTO**

Sólo 4 de 20 entidades tienen borrado lógico (`user`, `customer`, `delivery`,
`distributor`). Hay 6 borrados físicos: `DELETE /users/:id` (usuario y cuenta de
acceso, irreversible), admin, vehículo, rol, zona de cobertura y dirección. No
hay registro de quién creó, modificó o borró cada dato. Pedidos, pagos,
reclamos e incidencias no tienen borrado lógico. Va con la pasada de
normalización del modelo de datos.

### H-75 · El reseteo de contraseña del panel no hacía nada — **defecto, ALTO**

> **Resuelto el 24/09.** La contraseña se cambia en el proveedor de identidad.

El panel mandaba `password` a `PATCH /users/:id`, que la descartaba (no es una
columna) y respondía 200: el administrador creía haberla cambiado.
**Verificado contra la API:** después del arreglo el chofer entra con la nueva
y ya no con la vieja. Quien no es admin y manda `password` recibe 403.

### H-76 · Un admin de empresa podía bloquear al super administrador — **seguridad, CRÍTICO**

> **Resuelto el 24/09.** El seed ya no le carga distribuidora al super admin, la pertenencia sólo cuenta perfiles con rol `admin`, y un admin de empresa nunca administra a un super admin.

El backfill de `seed.ts` completaba con la distribuidora por defecto toda fila
de `admin` sin distribuidora, también la del super admin. Así el super admin
"pertenecía" a Jeny Gas. **Verificado contra la API:** el admin de Jeny Gas lo
bloqueó (200) y el super admin quedó sin acceso; se desbloqueó y se corrigió el
dato. **Revisar la base de producción:** si se corrió el seed allá, el super
admin tiene el mismo dato.

## Barrido de aislamiento entre distribuidoras — 25/09

Regla de nahue (24/09): la empresa A no ve ni hace nada sobre la B; lo ajeno
responde 404. `users` ya cumplía (H-66). Se probó el resto de la API con una
batería de 205 casos (`splg-app-backend/scripts/alineacion/aislamiento/`):
admin, chofer y cliente de A, y el super admin "viendo como" A, contra cada
recurso sembrado en B. **Antes de los arreglos: 66 fallas. Después: 0.** La
colección completa de Postman sigue sin regresiones sobre la distribuidora base.

### H-77 · A un cliente o un chofer se le podía colgar un perfil de admin — **seguridad, ALTO**

> **Resuelto el 25/09.** `POST /admin` exige que el perfil tenga el mismo rol que el usuario (admin o super_admin), distribuidora sólo para el admin de empresa, y uno por usuario. La pertenencia sólo cuenta el perfil si el usuario tiene ese rol.

El alta no miraba el rol del usuario. La colección de Postman se lo hacía en
cada corrida a un usuario cualquiera, así que en la base local había **85
clientes y choferes con perfil de admin de Jeny Gas** (borrados). Con ese
perfil, un cliente que sólo le compró a B pasaba a "pertenecer" a A, y el admin
de A veía sus direcciones. **Revisar la base de producción** con:
`SELECT count(*) FROM admin a JOIN "user" u USING (user_id) WHERE u.role_id IS DISTINCT FROM a.role_id;`

### H-78 · Admin y chofer de una empresa operaban los pedidos de otra — **seguridad, CRÍTICO**

> **Resuelto el 25/09.** Toda acción sobre `/orders/:id` controla primero la distribuidora del pedido; el chofer que acepta o al que se asigna un pedido tiene que ser de la misma.

**Verificado contra la API:** el admin de A leyó el código de entrega de un
pedido de B (el que el cliente escanea para confirmar), lo aceptó, lo asignó a
un chofer y lo canceló; el chofer de A aceptó un pedido pendiente de B, le mandó
su ubicación y lo rechazó. Todo 200/201. Con el arreglo: 404.

### H-79 · Un chofer liberaba el pedido asignado a otro chofer — **seguridad, ALTO**

> **Resuelto el 25/09.** Liberar (`PATCH /orders/:id/cancel`) y mandar la ubicación del pedido sólo lo hace el chofer asignado (403).

Dentro de la misma empresa, cualquier chofer devolvía a pendiente el pedido que
otro tenía en curso. Además el cliente que cancelaba un pedido ajeno recibía
400 "No autorizado" **después** de que el servidor le revelara si estaba en
camino; ahora es 404 y el control va primero.

### H-80 · Los choferes de otra distribuidora se administraban — **seguridad, CRÍTICO**

> **Resuelto el 25/09.** Validar, invalidar, activar, saldo, ubicación y baja de `/delivery/:id` controlan la distribuidora (404).

**Verificado:** el admin de A validó, desactivó, le cambió el saldo y dio de
baja al chofer de B.

### H-81 · Clientes y direcciones de otras distribuidoras — **seguridad, ALTO**

> **Resuelto el 25/09.** Un admin de empresa sólo llega a los clientes que le compraron. Dar de baja a un cliente y modificar sus direcciones pasa a ser del administrador general (403), como su cuenta en `users`.

El admin de A leía, validaba, editaba y daba de baja a un cliente que sólo le
había comprado a B, y leía sus direcciones.

### H-82 · Incidencias y reclamos sobre pedidos ajenos — **seguridad, MEDIO**

> **Resuelto el 25/09.** El pedido tiene que ser de la distribuidora en contexto; el chofer sólo reporta sobre el que tiene asignado.

### H-83 · Un admin de empresa mandaba pushes arbitrarios y leía tokens de cualquiera — **seguridad, MEDIO**

> **Resuelto el 25/09.** `send-test`, `order-confirmation` y los tokens de otro usuario, sólo el super admin. Las apps registran su propio token como siempre.

### H-84 · La búsqueda de admins por correo cruzaba distribuidoras — **seguridad, BAJO**

> **Resuelto el 25/09.** `GET /admin/term/:term` con distribuidora en contexto sólo encuentra a los suyos.

**Se dejó así, a propósito:** `GET /gascylinder/:id` muestra un producto de
otra distribuidora porque el catálogo es público (`GET /gascylinder` no pide
sesión). `GET /car/user/:id` y `/car/patent/:p` de otra distribuidora dan lista
vacía / `null`, no 404: ya estaban acotados y no filtran nada.
