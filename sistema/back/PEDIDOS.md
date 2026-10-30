# Pedidos, cobros, cotización, historial y rutas

Contratos del back que consumen el panel y las apps. Todo está también en Swagger
(`/docs`).

## Documentación de la API

`/docs`, `/docs-json` y `/docs-yaml` van detrás de la misma Basic Auth
(`SWAGGER_USER` / `SWAGGER_PASSWORD`). Con `NODE_ENV=production` y sin esas variables la
documentación **no se sirve**; fuera de producción y sin credenciales queda abierta y el
back avisa en el log. Código: `src/common/config/documentacion.ts`.

## Quién lee qué (accesos del chofer)

| Endpoint                           | Chofer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET /orders/:id`                  | Sólo si el pedido es **suyo** (asignado), si tiene una **oferta de despacho vigente** para él, o si está en el **pool** que ve en `GET /orders/available` (pendiente, sin chofer, de su distribuidora, y con la carga del día en regla). Cualquier otro: **404**, como si no existiera. Si el chofer **tuvo** el pedido (lo aceptó o se lo asignaron) y ya no es suyo —lo liberó el admin, lo reasignaron o el control de carga lo sacó del pool—: **410** `Este pedido ya no está asignado a tu usuario`, sin datos del pedido, para que la app salga de la pantalla en vez de quedarse con el estado viejo. |
| `GET /orders/customer/:customerId` | **403**. El chofer lista lo suyo con `GET /orders/delivery/:deliveryId`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

**Super admin sin `X-Distributor` (lectura de pedidos).** El super admin es el dueño de la plataforma: sin el
header lee los pedidos de **todas** las distribuidoras (`GET /orders/:id` y los listados de pedidos); con el
header ve sólo los de esa distribuidora. Es a propósito y no cambia. En cambio el **historial de estados**
(`GET /orders/:id/status-history`) y **toda escritura** exigen distribuidora: sin `X-Distributor`, 400.

**Incidencias del chofer (`POST /incidents`).** El chofer sólo reporta sobre un pedido **suyo** (asignado). Mismo
criterio que la lectura: un pedido ajeno, sin chofer o inexistente es **404**; si el chofer lo tuvo y ya no es
suyo, **410** `Este pedido ya no está asignado a tu usuario`. En ningún caso se crea la incidencia.

## Distribuidora obligatoria en las escrituras

El admin y el chofer traen su distribuidora del perfil. El **super admin** y el cliente la
mandan con `X-Distributor`. Todas las escrituras de pedidos, cobros, incidencias, reclamos y
adjuntos exigen distribuidora: el super admin sin el header recibe **400**
`Falta la distribuidora: enviá el header X-Distributor (slug o id)`. El cliente sin header
sigue funcionando en lo que abre (crear, cancelar o confirmar **lo suyo**; el dueño lo
controla el caso de uso). Los locks del pedido en los cobros y en la asignación manual
filtran por `distributor_id`: un pedido de otra distribuidora es 404.

Se revisaron, en este cambio, `POST /orders`, `PATCH /orders/:id` (+ `status`, `cancel`,
`assign`, `location`, `arrived`, `confirm-deposit`), `DELETE /orders/:id`,
`POST /orders/:id/reject`, `POST /orders/:id/confirm-delivery`, todos los
`/orders/:id/payment/*`, `POST|PATCH|PUT|DELETE /incidents*`, `POST|PATCH|DELETE /claims*`
(foto incluida), y las escrituras por UUID de otros módulos que el super admin podía
ejecutar sin distribuidora: `PATCH /delivery/:id` (+ `balance`, `invalidate`, `validate`,
`status`, `location`, `availability`), `DELETE /delivery/:id`, `PATCH|DELETE /customers/:id`,
`PUT|DELETE /car/:id/photo`. La lista completa está fijada en
`src/common/decorators/tenant-en-escrituras.spec.ts`.

**Excepción por destino** (`PATCH /users/:id`, `PATCH /users/:id/block`, `DELETE /users/:id`,
`PUT|DELETE /users/:id/photo`, `PATCH|DELETE /admin/:id`): el super admin sin `X-Distributor`
recibe **400** si la cuenta de destino es del personal de una distribuidora (chofer o admin de
empresa). Sobre otro **super admin** (no es de ninguna distribuidora) o un **cliente** (puede
comprarle a varias; lo administra el administrador general, H-66/H-73) opera sin header. Con el
header, la cuenta tiene que ser de esa distribuidora (404 si no). Cubierto por
`users.controller.tenant.spec.ts` y `admin.controller.tenant.spec.ts`.

`attachments`, `fleet-tasks`, `employee` y `cylinder` ya la exigían.
`stock`, `purchase` y `truck-load` los revisa otra tanda.

## Idempotencia (`Idempotency-Key`)

El alcance de la clave es **usuario + distribuidora + método + ruta + parámetros**: un super
admin que cambia de `X-Distributor` con la misma clave ejecuta de nuevo. En un multipart, el
archivo entra en la huella (otra imagen con la misma clave: 422). Una entrada de caché
corrupta se descarta y la operación se ejecuta. El lock de la clave se renueva solo mientras
corre el handler. Si la operación pasa los 120 s responde **503** (antes 500).

Son idempotentes (aceptan la clave): `POST /orders`, `PATCH /orders/:id/status|cancel|
assign/:deliveryId|confirm-deposit`, `POST /orders/:id/reject|confirm-delivery`, todos los
`/orders/:id/payment/*`, `POST /incidents`, `POST /claims`, `POST /claims/:id/photo`,
`POST /attachments/:ownerType/:ownerId`, `POST /fleet-tasks`, `POST /fleet-tasks/:id/attachments`,
`POST /user-address`, `POST /cylinder/assign`, `POST /employee/:id/termination` y
`/reinstatement`. Las apps deben mandar la clave en cada reintento.

Si falla algo **después** del commit (relectura del pedido, aviso al panel, checkout), la
operación no devuelve error: responde con lo ya confirmado, así el reintento con la misma clave
no duplica.

## Cobros manuales del administrador

Todos con `reason` obligatorio (10 a 500 caracteres), idempotentes y auditados. Se registran
en `order_status_history` como una fila de mismo estado de origen y destino con el motivo.

| Endpoint                                                            | Qué hace                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PATCH /orders/:id/payment/register-cash` `{ reason, cashBoxId? }`  | Efectivo entregado con pago `pending` → `paid`. `paymentConfirmedBy` es el admin; el motivo queda en `paymentResolutionNote`. `cashBoxId`: caja donde entra el efectivo (obligatoria si la distribuidora tiene cajas activas; ver `FINANZAS.md`). 409 si ya es impago.                                                                                                                                                             |
| `PATCH /orders/:id/payment/register-unpaid` `{ reason }`            | Lo mismo que el aviso del chofer: pago `unpaid` + **una** incidencia `unpaid_collection` (reportada por el admin). Responde como `PATCH .../unpaid`. El motivo queda también en el pedido (`paymentResolutionNote`, con `paymentResolvedBy/At`), igual que en `register-cash`; `resolve-unpaid` lo reemplaza cuando el impago se cierra (el motivo original sigue en el historial). Si el pago ya estaba `unpaid` no se toca nada. |
| `PATCH /orders/:id/payment/confirm-transfer` `{ received, reason }` | Pedido `transfer`, no cancelado. `received: true` → `paid` (recién ahí cuenta como venta), desde `pending` **o desde `failed`** (la transferencia llegó después de marcarla no recibida: se corrige con motivo). `received: false` → `failed`, sólo desde `pending` y **sólo sobre un pedido entregado** (409 si no lo está: marcarla antes no frenaría nada). Repetir lo mismo: no-op; `paid` → `failed`: 409.                    |

**Transferencia confirmada y pedido cancelado después.** La cancelación no se bloquea (el cliente
o el admin pueden cancelar un pedido todavía no entregado), pero el dinero ya está en la
distribuidora: `GET /reports/collections` lo informa en `pendingRefund` (pedidos `cancelled` con
pago `paid`, por el día en que se cancelaron: la última transición a `cancelled` del historial; un
pedido cancelado antes de que existiera el historial cae a la fecha de última modificación; la consulta usa
el índice parcial `IDX_order_status_history_cancelacion`, migración `1792000000000`) y el pedido sigue con `paymentStatus: paid`.
**El sistema no gestiona el reintegro de una transferencia**: lo hace la distribuidora por fuera y
el panel debe mostrarlo como "reintegro pendiente". Los pagos por una pasarela (MercadoPago) sí se
devuelven solos al cancelar: ver `EXPRESS-REINTEGROS.md`.

Una transferencia sin confirmar **no suma a las ventas**: `GET /reports/collections` ahora trae
`pendingTransfer` y `notReceivedTransfer` junto a `pendingCash`, `unpaid` y `writtenOff`.

La incidencia de cobro impago **se cierra sólo con `resolve-unpaid`**: por
`PATCH /incidents/:id/resolve` (resuelta o descartada) responde 409 mientras el pedido siga
`unpaid`. El cierre y la edición de una incidencia son un `UPDATE` condicional a `open`: si
otro la cerró en paralelo, 409 y no se pisa su resolución.

## Listado del panel — `GET /orders`

Además de `term`, `status`, `paymentStatus`, `from`/`to` (fecha de **creación**) y la paginación:

- `deliveredFrom` / `deliveredTo` (`YYYY-MM-DD`, día en hora argentina, `deliveredTo` inclusivo): filtran por
  `deliveredAt`, así que dejan afuera lo que no se entregó. Un rango invertido es 400.
- `sort` (`createdAt` por defecto | `deliveredAt`) y `order` (`desc` por defecto | `asc`). Con `deliveredAt`
  los pedidos sin entregar quedan al final en cualquiera de los dos sentidos. El id desempata, así que la
  paginación es estable.

Sin ninguno de los parámetros nuevos el listado es el de siempre (más nuevos primero).

## Historial de estados

`order_status_history` registra **toda** transición del pedido (incluido el alta,
`from_status = null`), en la misma transacción que el cambio: quién (el usuario del request;
`null` si lo hizo el sistema: cron, webhook), cuándo, desde, hasta y el motivo si lo hay
(cancelación o entrega manual). Además, sin cambio de estado, asienta notas (origen = destino,
`isNote: true`): los cobros manuales del admin y la **reasignación** de un pedido aceptado a otro
chofer (`accepted → accepted`, motivo «Reasignación de chofer»; sin nombres, porque el historial
también lo leen el cliente y el chofer). Lo asienta `OrderStatusHistorySubscriber`, que escucha los
`save` del pedido; las transiciones pasan por `transitionOrder`, así ningún caso de uso puede
olvidarse. **No hay backfill:** los pedidos anteriores a este cambio no tienen el historial de
sus transiciones pasadas; el historial empieza el día que se despliega.

**Lectura — `GET /orders/:id/status-history`.** Devuelve las filas del pedido del más viejo al más
nuevo: `{ id, fromStatus, toStatus, isNote, reason, changedAt, changedBy }`. Los estados usan los
mismos valores que `status` del pedido (`on_the_way` sale como `out_for_delivery`); `isNote` es
`true` en las filas de anotación (origen = destino); `changedBy` es `{ userId, role, fullName }` o
`null` si lo hizo el sistema, y `fullName` sólo se completa para admin y super admin. Misma regla de
lectura que `GET /orders/:id`: el cliente sólo los suyos, el chofer los que ve en el detalle
(410 si lo tuvo y ya no es suyo), admin y super admin los de su distribuidora (el super admin tiene que mandar `X-Distributor`: sin él, 400); lo ajeno, 404. Dos filas
asentadas en la misma transacción comparten `changedAt`: entre ellas el orden no está garantizado.

**Filas de anotación.** Los cobros manuales (`register-cash`, `register-unpaid`,
`confirm-transfer`) no cambian el estado del pedido, pero dejan su motivo en el historial como
una fila con `from_status = to_status` (p. ej. `delivered → delivered`) y el texto en `reason`
(`Transferencia confirmada por un administrador: …`). No son una transición: quien muestre la
línea de tiempo del pedido tiene que distinguirlas (origen = destino) y mostrarlas como una
nota, no como un cambio de estado.

**Respuesta incompleta.** Si un cobro, un alta o una asignación ya se confirmaron pero falla
la relectura del pedido, el back responde 2xx con lo que tiene y la `Idempotency-Key` guarda esa
respuesta **5 minutos** en vez de 24 h: cubre el reintento inmediato (no repite la operación) y
no deja un pedido a medias como "la respuesta" de esa clave.

## Pedido en curso del chofer — `GET /orders/delivery/me/active`

Sólo rol `delivery`; el chofer y la distribuidora salen del token. Devuelve el pedido que el chofer
tiene en curso **sin importar cuándo se creó**: el que lleva `out_for_delivery` o, si no hay, el
`accepted` más antiguo. Sin activos, el pedido entregado **hoy** (día argentino) en efectivo con el
cobro `pending`, para que confirme el cobro. Si no tiene ninguno responde `204` sin cuerpo. La app
lo usa para retomar al abrir en lugar de recorrer `GET /orders/delivery/:deliveryId`.

## Cancelación

`PATCH /orders/:id/cancel` (y el viejo `DELETE /orders/:id`) responden el pedido con `cancelledBy`
(`customer` o `admin`) igual que la lectura posterior. Si cancela el chofer el pedido vuelve a
`pending` y `cancelledBy` es `null`.

## Editar un pedido — `PATCH /orders/:id`

Lo pueden usar el **cliente dueño**, el admin y el super admin (el chofer: 403). Idempotente
(`Idempotency-Key`). Cuerpo (todo opcional): `items` (reemplaza TODOS los renglones),
`addressId`, `timeSlotId` (`null` la saca), `scheduledDate`, `paymentMethod` y `notes`.

- **Cuándo:** sólo con el pedido `pending` **sin chofer** (ni oferta aceptada) y sin pago
  online (`mercadopago` o cobro ya generado/pagado). Si no, **409**. Al cliente, si el pedido
  ya lo tomó un repartidor, el mensaje es `El pedido ya fue tomado por un repartidor: no se
puede modificar`. No se puede pasar un pedido a MercadoPago al editarlo (400).
- **Dueño:** el cliente sólo edita lo suyo; un pedido ajeno responde **404** (igual que
  `GET /orders/:id`). La distribuidora (`X-Distributor`) es opcional para el cliente.
- **Precio:** siempre del servidor. El cuerpo no lleva precios (`unitPrice`/`totalAmount` no
  se usan): el total se recalcula con las mismas funciones que el alta y `POST /orders/quote`
  (promociones, recargo de zona —si cambia la dirección—, recargo del medio de pago).
- **Stock:** la reserva se ajusta por la diferencia neta de cada garrafa (400 si no alcanza).
- **Carrera con la aceptación del chofer:** la edición toma `FOR UPDATE` sobre el pedido y
  re-chequea el estado adentro; la aceptación y la asignación manual también lo toman y
  **releen los renglones después del lock** (un JOIN que espera el lock los traía viejos y
  el `save` desvinculaba los nuevos). Gana quien toma el lock primero: o el chofer se queda
  con el pedido original y la edición responde 409, o la edición entra y el chofer acepta el
  pedido ya editado.
- **Lock del despacho:** la edición corre bajo el lock Redis `dispatch:offer:<id>`, el mismo de
  `offerToNextDriver`. Si lo tiene el despacho u otra edición, **reintenta hasta ~3 s** (con
  jitter) y recién entonces responde **409** `El pedido se está despachando en este momento`.
  Dos ediciones simultáneas se aplican en serie con el stock exacto; el despacho no reintenta.
- **Cupo:** con la misma franja y fecha del pedido no se valida el cupo (ni "terminó"); si
  cambian, se valida el cupo nuevo. Sin `scheduledDate` en el pedido ni en el cuerpo no se
  asigna fecha. Lo mismo hace la cotización de edición.
- **Despacho:** si había ofertas en curso se vencen (`superseded`), se avisa a esos choferes
  (`order:cancelled` al chofer) y el pedido se vuelve a ofrecer con los datos nuevos.
- **Historial:** cuando edita el cliente queda una fila de anotación (origen = destino):
  `Pedido modificado por el cliente: renglones, notas. Total: 2000 → 5000`.
- **Avisos:** `order:updated` al panel (admins de la distribuidora) y, si cambió el total, al
  cliente (`{ orderId, totalAmount, previousTotalAmount }`).
- **Auditoría:** el pedido y sus renglones pasan por `save`/`remove`: el subscriber de
  auditoría los registra, y el request entero queda en el log de auditoría HTTP.

## Crear desde el carrito — `fromCart: true` (CU-126)

`POST /orders` y `POST /orders/quote` aceptan `fromCart: true` (opcional; sin él todo funciona como
siempre). Es el **checkout del carrito persistente** (`CARRITO-Y-CONSUMO.md`):

- Los ítems salen del carrito del cliente en la distribuidora de `X-Distributor`. El cuerpo **no
  lleva `items`**: con ambos, 400. `fromCart` y `orderId` (cotización de edición) tampoco se
  combinan (400).
- Se cobra el **precio vigente del catálogo** (más promociones, zona y recargos de pago, como
  cualquier pedido), no el guardado en el carrito.
- El carrito se vacía **dentro de la transacción del pedido** (con su fila bloqueada): si el pedido
  falla (sin stock, fuera de cobertura, etc.) el carrito queda intacto. La cotización no bloquea ni
  toca el carrito.
- Carrito vacío (o inexistente en esa distribuidora): **400** `Tu carrito está vacío`. Con
  productos dados de baja: **400** que nombra cuáles; hay que quitarlos para continuar.
- Sólo el cliente (rol `customer`); el personal que carga un pedido a nombre de un cliente manda
  `items` (403 con `fromCart`).
- Idempotencia: un reintento con la misma `Idempotency-Key` devuelve la respuesta guardada sin
  ejecutar nada: no duplica el pedido ni vacía de nuevo el carrito.
- **Contrato para la app:** el checkout del carrito es `fromCart: true`; la app **no borra ítems**
  del carrito al confirmar. La compra exprés (sin carrito) sigue mandando `items`.

## Cambiar la dirección de entrega — `PATCH /orders/:id/address` (CU-127)

Sólo el **cliente dueño** (un pedido ajeno es **404**; admin, super admin y chofer: **403**). Idempotente
(`Idempotency-Key`). Cuerpo: `{ addressId, reason? }` (`reason` hasta 500 caracteres). Responde el pedido completo
(`OrderResponseDto`).

- **Cuándo:** pedido `pending` o `accepted`. `on_the_way` o `delivered`: **409** `El pedido ya salió o fue entregado: no se
puede cambiar la dirección`. `cancelled` o `reserved`: **409** con el estado actual.
- **Dirección:** tiene que ser otra de las del cliente (de otro cliente o inexistente: **404** `Dirección no encontrada`;
  la misma que ya tiene: **400**) y caer dentro de una zona de cobertura de la distribuidora del pedido (misma consulta del alta;
  si no: **400** `La dirección está fuera de la zona de cobertura de la distribuidora`).
- **Recargo y total:** se calcula el recargo de la zona nueva sobre `subtotalItems` y se compara con el del pedido.
  - Pedido de **pago en línea** (`paymentType = online`: MercadoPago o transferencia): el importe ya está definido, así que si el
    recargo cambia responde **409** `El recargo de la zona nueva es distinto del original y el pedido es de pago en línea:
cancelalo y hacelo de nuevo con la dirección que querés`. Si el recargo es el mismo, cambia la dirección y conserva el total.
  - Pedido en **efectivo**: recalcula `zoneSurchargeAmount` y `totalAmount`. Con seña paga, el total no puede quedar por
    debajo de la seña (**409**).
- **Qué se guarda (una sola transacción, con lock sobre el pedido y re-chequeo del estado adentro):** `addressId`, `deliveryPoint`
  (el punto contra el que se mide la llegada del chofer), el snapshot de la zona (`coverage_zone_id`, `zone_name`,
  `zone_surcharge_*`), una fila en `order_address_change` (dirección anterior, nueva, quién y el motivo) y una anotación en el
  historial de estados (`Dirección de entrega cambiada por el cliente (<motivo>). Total: 2200 → 2500`).
- **Carrera:** corre bajo el lock Redis `dispatch:offer:<id>` (el del despacho y la edición). Si el pedido sale en camino en
  paralelo, gana uno solo: o el cambio entra antes, o responde 409 sin escribir.
- **Avisos:** al chofer asignado (leído después del lock, en una consulta aparte), por su **id de usuario** (no el de su perfil), `order:address-changed`
  (`{ orderId, distributorId, fromAddressId, toAddressId, totalAmount, status, message }`); a los admins de la distribuidora,
  `order:address-changed` con el mismo payload. Si el pedido está `pending`, las ofertas vivas pasan a `superseded`, se avisa a esos
  choferes (`order:cancelled`) y el pedido se vuelve a ofrecer con el punto nuevo.
- **Auditoría:** el pedido y `order_address_change` pasan por `save`; el request queda en el log HTTP.

## Quién recibe el pedido — `PATCH /orders/:id/receiver` (CU-128)

Sólo el **cliente dueño** (ajeno: **404**; admin, super admin y chofer: **403**). Idempotente. Cuerpo, todo obligatorio:
`receiverName` (hasta 120), `receiverDocument` (hasta 20; se normaliza sin puntos, guiones ni espacios y en mayúsculas; DNI,
CUIT/CUIL o pasaporte: 6 a 15 letras o dígitos con al menos un dígito, si no **400**) y `receiverRelationship` (hasta 40).
Reemplaza lo anterior. Responde el pedido completo.

- **Cuándo:** mientras el pedido no esté `delivered` (**409** `El pedido ya fue entregado: no se puede indicar quién lo recibe`)
  ni `cancelled` (**409**). Lock sobre el pedido y estado re-chequeado adentro.
- **Dónde se ve:** la respuesta del pedido trae `receiver: { name, document, relationship } | null`. Lo ven el **cliente dueño**,
  el **chofer asignado** y el **administrador** de la distribuidora. Un chofer que mira el pedido desde el pool
  (`GET /orders/available`) o como oferta recibe `receiver: null`.
- **Desde el alta:** `POST /orders` acepta `receiver: { receiverName, receiverDocument, receiverRelationship }` (opcional) con las
  mismas validaciones y la misma visibilidad.
- **Datos de un tercero:** se conservan sólo hasta que vence el plazo de reclamo y después se anulan. Un pedido con un **reclamo
  abierto** (`pending` o `in_process`) conserva los datos hasta que el reclamo se cierre.
  `ReceiverRetentionCron` corre todos los días a las 03:40 (hora de Argentina), con cerrojo distribuido
  (`cron:order-receiver-retention`), y deja en `NULL` los tres campos de los pedidos `delivered` o `cancelled` cuya fecha de
  entrega (`deliveredAt`, o `updatedAt` si se canceló) tenga más de `PLAZO_DE_RECLAMO_DIAS` (30) días. Es mantenimiento
  del sistema, no una tarea configurable.
- **Nada de esto entra en la auditoría** (es inmutable y la anulación tiene que ser real): `receiverName`, `receiverDocument` y
  `receiverRelationship` están en `PROPIEDADES_EXCLUIDAS.Order` (auditoría de datos), sus claves en `SENSIBLES` de `depurarCambios`
  (bitácora HTTP: `[depurado]`) y en la lista de `cuerpoParaLog` (log de morgan: `******`, también anidados en `receiver`).
  `ReceiverRetentionCron` registra la anulación en la auditoría de datos (`receiver: [datos de quien recibe] → [anulados por plazo
de reclamo vencido]`) sin los valores.

## Cotización — `POST /orders/quote`

Mismo cuerpo que `POST /orders`; sólo `paymentMethod` es obligatorio, más `items` (salvo con `fromCart: true`, ver «Crear desde el carrito»). Con `addressId`
(el admin además manda `customerId`) incluye el recargo de la zona. Respuesta `200`.

**Cotización de edición:** con `orderId` en el cuerpo cotiza cómo quedaría ese pedido al editarlo
con `PATCH /orders/:id`, con las mismas reglas (lo que cotiza bien, se guarda): el pedido tiene
que ser del cliente que cotiza (o de la distribuidora del staff), si no **404**; si no es
editable, **409** con el mensaje del PATCH. El stock se compara por la **diferencia** contra lo
que el pedido ya tiene reservado (cantidad igual o menor siempre alcanza); la franja y la fecha
sólo se validan si cambian; lo que el cuerpo no trae (dirección y zona, seña) se toma del pedido.
No escribe nada.

```json
{
  "items": [
    {
      "gasCylinderId": "…",
      "title": "Garrafa 10kg",
      "quantity": 3,
      "unitPrice": 8500,
      "subtotal": 25500
    }
  ],
  "subtotal": 25500,
  "zone": {
    "coverageZoneId": "…",
    "name": "Centro",
    "type": "fixed",
    "value": 0,
    "amount": 0
  },
  "zoneSurcharge": 0,
  "paymentMethod": "transfer",
  "paymentSurcharge": 2550,
  "deposit": 0,
  "total": 28050,
  "balance": 28050
}
```

`paymentSurcharge` es el +10% de `mercadopago` y `transfer` sobre **subtotal + recargo de zona**
(0 en `cash`). `total` es el del pedido que se crea con el mismo cuerpo; `balance = total −
deposit`. Usa las mismas funciones que el alta (`valorizarRenglon`, `resolverZona`,
`calcularTotales`); no escribe nada ni reserva stock, pero rechaza lo que el alta rechazaría
(otra distribuidora —se valida antes que el stock—, sin stock, franja inválida, fuera de cobertura, y la misma garrafa en dos renglones: 400, igual que `POST /orders`). Roles: cliente (para sí), admin, super admin.

## El chofer en el pedido — `GET /orders/:id`

Para el **cliente dueño** y el **admin**, mientras el pedido está `accepted` o
`out_for_delivery` y tiene chofer:

```json
"driver": { "userId": "…", "fullName": "Ana Gómez", "phoneNumber": "+54911…", "ratingAverage": 4.8, "ratingCount": 37 }
```

Con el pedido cerrado, sin chofer, o visto por el propio chofer, `driver` es `null` (el teléfono
no se expone). Sólo viene en la lectura individual, no en los listados. La patente está en
`vehicle.patent` (snapshot al aceptar). Las calificaciones ocultas no cuentan.

`driver.location` es la **última ubicación conocida**: `{ "lat": -34.61, "lng": -58.40, "at":
"2026-10-12T20:15:00.000Z" }`. Es más sensible que el nombre o el teléfono, así que tiene reglas
más estrictas:

- **Sólo con el pedido `out_for_delivery`** y siendo **ese** el pedido activo del chofer (el que
  lleva en el radar). Con el pedido `accepted` el chofer puede estar entregando otro y su
  posición no es de este cliente: `location` es `null` (el teléfono sí viene desde `accepted`).
- **Sólo si es reciente**: la hora (`at`) no puede tener más de `DRIVER_LOCATION_MAX_AGE_MIN`
  minutos (10 por defecto). Una posición más vieja, o sin hora anotada (anterior al despliegue),
  no se devuelve: `location` es `null`. El cliente debe tratar `null` como "sin posición
  reciente", no como error.
- Si el radar (Redis) no responde, el pedido se lee igual y `location` es `null`.

Sale del radar de despacho (Redis GEO), el mismo que alimenta el chofer por socket
(`driver:update-location`) o por `PATCH /orders/:id/location`; no hay tabla nueva. La hora se
anota aparte en Redis (`driver:location-at:<userId>`, 24 h). Con el pedido cerrado no se expone.
Sirve para redibujar la camioneta si se cae el socket.

## Quién canceló — `cancelledBy`

`GET /orders/:id` trae `cancelledBy` (`customer` · `admin` · `driver` · `system`, o `null` si el
pedido no está cancelado o es anterior al historial) y el evento de socket `order:cancelled`
lleva el mismo campo. Se saca de `order_status_history`: el rol del usuario que hizo la última
transición a `cancelled` (el super admin cuenta como `admin`); sin usuario (vencimiento de pago,
cron) es `system`, que sólo se ve al leer el pedido: el evento `order:cancelled` no se emite
en esos casos y lleva `customer` o `admin`. Un chofer que "cancela" no cancela: libera el pedido a `pending`
(`order:searching-driver`), por eso `driver` sólo aparece si un pedido lo cancela un usuario con
rol chofer por otra vía.

## Eventos de socket que recibe el cliente

| Evento                   | Cuándo                                                                                                                                                                  | Payload                                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `order:accepted`         | un chofer acepta, o el admin asigna                                                                                                                                     | `{ orderId, status: "accepted", updatedAt, paymentStatus, driver: { name, phone, photoUrl } \| null }` |
| `order:on-the-way`       | el chofer sale                                                                                                                                                          | igual que `order:accepted`, con `status: "on_the_way"`                                                 |
| `order:arrived`          | el chofer avisa que llegó                                                                                                                                               | `{ orderId, message, driverName }`                                                                     |
| `order:delivered`        | se entrega                                                                                                                                                              | igual que `order:accepted`, con `status: "delivered"`                                                  |
| `order:cancelled`        | cancela el cliente o un admin (los vencimientos automáticos —pago, reserva— **no** emiten el evento: el cliente se entera al leer el pedido, con `cancelledBy: system`) | `{ orderId, status: "cancelled", reason, cancelledBy }`                                                |
| `order:searching-driver` | el chofer libera el pedido y vuelve a buscarse                                                                                                                          | `{ orderId, status: "pending" }`                                                                       |
| `order:driver-location`  | cada posición del chofer mientras el pedido está en camino                                                                                                              | `{ orderId, driverId, lat, lng, at }`                                                                  |
| `order:updated`          | el cliente o un admin editan el pedido y cambia el total                                                                                                                | `{ orderId, totalAmount, previousTotalAmount }`                                                        |
| `order:payment-approved` | MercadoPago aprueba el pago o la seña                                                                                                                                   | `{ orderId, tipo: "deposit" \| "payment", paymentStatus, updatedAt }`                                  |

`reason` de `order:cancelled` es el motivo que se dio, o `Cancelado por <rol>` si no hubo.
`status` viaja con el valor del enum (`on_the_way`), no con el `out_for_delivery` del REST.

## Aceptar un pedido y volver con el camión

La aceptación del chofer (`PATCH /orders/:id/status` → `accepted`) y la asignación manual
(`PATCH /orders/:id/assign/:deliveryId`) toman `FOR SHARE` sobre la carga abierta del chofer
**dentro de su transacción**, antes de leer su estado (`TruckLoadGatePort`, con el `manager`);
la vuelta del camión (`PATCH /truck-loads/:id/return`) la toma `FOR UPDATE`. Si pasan a la vez,
una espera a la otra: o la aceptación termina antes (y la vuelta ve el pedido en curso y responde 409) o la vuelta termina antes (y la aceptación ve la carga `returned` y responde 400). Nunca queda
un pedido aceptado sobre una carga devuelta. Orden de locks: pedido → chofer → carga (compartido).

## Pedido de Mercado Pago sin pagar: no sale hasta que se apruebe el pago

Una sola regla (`esperaPagoOnline`, en `src/order/domain/`): un pedido **espera el pago online** si
es de Mercado Pago, su pago no está aprobado y no es una reserva con la seña paga (ahí el saldo se
cobra al entregar y `paymentStatus` sigue `pending` a propósito). Mientras espera:

- el despacho no lo ofrece (ni el común ni el express; tampoco el cron de pendientes ni el cambio
  de dirección): se despacha cuando el webhook aprueba el pago;
- no figura en `GET /orders/available`;
- el chofer no lo acepta (`PATCH /orders/:id/status` → `accepted`: **409**);
- el admin no lo asigna (`PATCH /orders/:id/assign/:deliveryId`: **409** «El pedido se paga con
  Mercado Pago y todavía no está pago: se le asigna chofer cuando se apruebe el pago»), dentro de la
  transacción y sin tocar nada. Un chofer de otra distribuidora sigue dando 404 antes, y un pedido
  cerrado sigue dando la transición inválida.

Antes de este cambio el despacho común sí ofrecía estos pedidos: en la base había pedidos de Mercado
Pago impagos con ofertas a choferes. El panel apaga «Asignar chofer» con el mismo motivo en la
ficha, el tablero de despacho, la vista rápida, el menú de la fila de Pedidos y el pool de
Seguimiento. En la asignación en lote esos pedidos quedan afuera, con aviso. Lo lee de
`paymentMethodDetail`, `paymentStatus` y `depositPaid` de la respuesta.

Probado el 28/10/2026 contra la API con pedidos reales de Mercado Pago impagos:
- no figuraron entre los disponibles;
- asignar y aceptar dieron 409;
- el pedido siguió pendiente, sin chofer y sin ofertas, y el intento quedó en la auditoría como
  rechazado;
- en el panel, el botón y el ítem del menú quedaron apagados con el motivo y no llegó ningún pedido
  a `/assign`.

Los pedidos de prueba quedaron cancelados.

## Un solo reloj

`acceptedAt`, `onTheWayAt` y `deliveredAt` del pedido se toman con `clock_timestamp()` de la base
(`src/common/utils/ahora-de-la-base.ts`), en la transacción del cambio de estado, igual que
`opened_at` / `closed_at` de la carga del camión: los dos módulos comparan momentos del mismo
reloj. Los cobros (`paymentConfirmedAt`, `paymentResolvedAt`) y las fechas de las ofertas de
despacho siguen con el reloj de Node: no se comparan contra la carga.

## Rutas por calles — `GET /routes/driving?orderId=<uuid>[&from=lat,lng]`

La ruta es **de un pedido**, no un trazador de mapas abierto: el destino es siempre la dirección
de entrega del pedido y el origen la última posición reciente del chofer (la hora de la posición
no puede tener más de `DRIVER_LOCATION_MAX_AGE_MIN`; si no hay, 409). `from` es opcional y se
acepta sólo a menos de `ROUTES_FROM_MAX_DISTANCE_M` (300 m) de esa posición (400 si no).

| Quién              | Cuándo                                                                               | Si no                                 |
| ------------------ | ------------------------------------------------------------------------------------ | ------------------------------------- |
| Chofer asignado    | pedido `accepted` u `on_the_way`                                                     | pedido de otro: 404; otro estado: 403 |
| Cliente dueño      | pedido `on_the_way` y el pedido que el chofer lleva (su posición no se expone antes) | 404 / 403                             |
| Admin, super admin | no piden rutas                                                                       | 404                                   |

**Cupos** (429): 30 pedidos por minuto y usuario; y, por cada consulta que llega al proveedor
(la caché de 60 s por origen y destino redondeados a 4 decimales no cuenta), 100 por usuario y
3000 por distribuidora cada 24 h (`ROUTES_DAILY_LIMIT_PER_USER`,
`ROUTES_DAILY_LIMIT_PER_DISTRIBUTOR`). Con Redis caído no hay 500: los cupos se cuentan en
memoria de cada proceso, no hay caché y, sin radar, el chofer (sólo él) puede mandar su propio
`from`; el cliente recibe 409.

**Proveedor**: Google Directions con `GOOGLE_DIRECTIONS_API_KEY` (clave **del servidor**,
restringida por IP, no la de las apps). Sin clave, o si Google falla, OSRM propio
(`OSRM_BASE_URL`); el OSRM público sólo se usa con `NODE_ENV=development` o `test`: en producción
sin ninguno de los dos, 503. Si el proveedor no responde: 502.

**Costo y alerta en Google** (a configurar en la consola, el back no lo puede hacer): fijar una
cuota diaria del API Directions en Google Cloud (Cuotas y límites de la API) igual o apenas mayor
a la suma esperada de los topes por distribuidora, y una alerta de presupuesto
(Facturación → Presupuestos y alertas) al 50 %, 90 % y 100 % del gasto mensual previsto. Los
topes del back acotan a un usuario o a una distribuidora; la cuota de Google es la última línea.

```json
{
  "provider": "osrm",
  "distanceMeters": 4621,
  "durationSeconds": 465,
  "encodedPolyline": "loerE`ticJ…",
  "points": [{ "lat": -34.60371, "lng": -58.38161 }]
}
```

`encodedPolyline` es el formato de Google (precisión 5); `points` es la misma ruta decodificada.

## Tope de la seña de una reserva

`POST /orders` con `isReservation: true` (y `POST /orders/quote` con el mismo cuerpo) rechaza con **400**
`La seña ($X) no puede superar el total del pedido ($Y)` cuando `depositAmount` es mayor al total calculado en el
servidor (ítems con promociones, recargo de zona y de medio de pago, redondeado a 2 decimales). Una seña igual al
total se acepta. Una reserva no se edita (sólo se edita un pedido `pending`): para cambiarla se cancela y se crea otra,
así que el tope corre sólo en el alta y su cotización. Con la seña ya paga, el total de un pedido editable no puede
quedar por debajo de ella (409); esa comparación usa el mismo total redondeado a 2 decimales que la cotización.

Una reserva con **MercadoPago** exige `depositAmount` mayor a cero (**400** `Una reserva con MercadoPago necesita una
seña mayor a cero...`, también en la cotización): la seña se cobra online y su aprobación es lo que activa la reserva,
que no se confirma a mano. Con otros medios, omitirla equivale a 0. `depositAmount` admite como máximo 2 decimales (400 si trae más) y la regla de «mayor a cero» mira el importe redondeado a centavos.

`GET /orders/reservations` agrega `timeSlot` (`name`, `startTime`, `endTime` en HH:MM, o `null` si la reserva es sólo
por día) y `paymentUrl` (ver abajo).

## Enlace de pago de MercadoPago

El enlace de Checkout Pro se guarda en el registro de cobros al crear el pedido (o la seña de una reserva). Además de la
respuesta del alta, `GET /orders/:id` devuelve `payment_url` mientras el cobro siga pendiente (pedido de MercadoPago no
cancelado ni pagado; no se le devuelve al chofer), y `GET /orders/reservations` devuelve `paymentUrl` de la seña mientras
esté pendiente (`null` en efectivo o transferencia, con la seña paga o si la pasarela no lo generó). Una seña en efectivo
o por transferencia la confirma el admin con `PATCH /orders/:id/confirm-deposit`, sea cual sea el medio.

El checkout de MercadoPago cobra exactamente lo que queda en el registro de cobros: los renglones de los productos
(precio con promoción) más un renglón por cada recargo del total (`Recargo de zona`, `Recargo por pago online`, `Recargo
express`; los que valen 0 no se mandan). En una reserva el checkout es un único renglón `Seña de reserva` por la seña.
Si la pasarela aprobara otro importe, el webhook no da el pedido por pagado ni lo despacha.

## Recargo online guardado, motivo de cancelación y fecha agendada (tanda V1)

- El recargo del medio de pago se guarda en `order.payment_surcharge_amount` (redondeado a 2 decimales) y el
  total es exactamente ítems + zona + recargo online + express (el express no cuenta si el pedido pasó al
  reparto común). Lo completan el alta, la edición y el cambio de dirección; la base lo controla con
  `CHK_order_total_formula`. Detalle de la tanda: `VALIDACIONES-BASE.md`.
- Cancelar (`PATCH /orders/:id/cancel`, `PATCH /orders/:id/status` con `cancelled`) exige `reason` (400 si falta o
  está en blanco) para cliente y administrador; el chofer, que libera el pedido, no lo manda.
- `scheduledDate` no puede ser una fecha pasada (día argentino), con o sin `timeSlotId`, en el alta y en la edición.
- `items: []` en el alta es 400.
