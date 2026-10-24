# Compra express y reintegros (C-17)

CU-147 (compra express), CU-148 (modalidad de entrega), CU-149 (despacho a una moto) y CU-168
(reintegro del pago), más el reintegro de la cancelación del cliente (CU-008) y del
administrador (CU-010). Todo está también en Swagger (`/docs`, tags "Orders · Express",
"Pagos · Reintegros" y "Configuración · Parámetros por distribuidora").

## Parámetros de la distribuidora (CU-172)

`GET` / `PUT /module-config/express_dispatch`. Rol `admin` o `super_admin` (el super admin
manda `X-Distributor`; sin él, 400). `PUT` **reemplaza** la configuración: lo que no se manda
toma su valor por omisión. Copia en memoria de 1 minuto por distribuidora, igual que el despacho.

| Campo                      | Tipo      | Regla                                             | Por omisión       |
| -------------------------- | --------- | ------------------------------------------------- | ----------------- |
| `enabled`                  | `boolean` | la distribuidora ofrece la modalidad              | `false`           |
| `surchargeAmount`          | `number`  | recargo fijo en pesos, 0 a 1.000.000, 2 decimales | `0`               |
| `maxRadiusKm`              | `number`  | radio donde se busca la moto, 1 a 50 km           | `5`               |
| `offerTtlSeconds`          | `integer` | ventana de cada oferta express, 10 a 120 s        | `20`              |
| `serviceFrom`/`serviceTo`  | `HH:mm`   | horario de servicio (hora argentina), `from < to` | `08:00` / `20:00` |
| `estimatedMinutes`         | `integer` | tiempo estimado del express, 5 a 240              | `45`              |
| `standardEstimatedMinutes` | `integer` | tiempo estimado del reparto común, 30 a 1440      | `180`             |

La respuesta suma `isDefault`, `updatedAt` y `updatedByUserId`. Sin configuración la modalidad
está **apagada**: hay que definir recargo y horario.

## Modalidades disponibles (CU-148)

`GET /orders/delivery-options?addressId=<uuid>` (cliente; el admin suma `customerId`). No
escribe nada.

```json
{
  "addressId": "…",
  "options": [
    {
      "mode": "standard",
      "available": true,
      "reason": null,
      "message": null,
      "surchargeAmount": 0,
      "estimatedMinutes": 180
    },
    {
      "mode": "express",
      "available": false,
      "reason": "no_motorcycle_driver",
      "message": "No hay un chofer en moto disponible cerca",
      "surchargeAmount": 0,
      "estimatedMinutes": 45
    }
  ]
}
```

El express está disponible cuando se cumplen, en este orden: la distribuidora lo habilitó
(`disabled`), la dirección tiene ubicación (`no_location`) y está dentro de la cobertura
(`out_of_coverage`), es horario de servicio (`out_of_hours`) y hay al menos un chofer **en moto**
dentro del radio express, habilitado (licencia y documentos del vehículo) y con carga de camión
en regla (`no_motorcycle_driver`). "En moto" = el vehículo **en uso** del chofer tiene `type_car`
que contiene "moto" (sin distinguir mayúsculas ni tildes).

`POST /orders/quote` y `POST /orders` aceptan `deliveryMode: "standard" | "express"`. La cotización
suma `deliveryMode` y `expressSurcharge`. **La disponibilidad se vuelve a evaluar al crear el pedido**:
si dejó de estar disponible, **409** con el cuerpo

```json
{
  "statusCode": 409,
  "error": "Conflict",
  "code": "EXPRESS_NOT_AVAILABLE",
  "reason": "out_of_hours",
  "message": "…"
}
```

y no se reserva stock ni se crea nada. El express no se combina con reserva, franja ni fecha
agendada (400). Un pedido express **no es editable** (`editable: false`, `PATCH` → 409).

### Precio

`total = (subtotal + recargo de zona) × (1 + recargo por medio de pago) + recargo express`. El
recargo express se suma **al final** y no lleva el recargo por medio de pago, así lo que se devuelve
si el pedido pierde el express es exactamente lo que se cobró de más. Con MercadoPago el checkout
cobra el recargo como un renglón más (`express-surcharge`).

## Compra express en un paso (CU-147)

Sólo el cliente. Usa la **dirección predeterminada** y la **garrafa habitual** (la del último
pedido no cancelado del cliente en esa distribuidora; `gasCylinderId` la pisa y es obligatorio
si no hay compras). `quantity` (1 a 10, por omisión 1).

- `POST /orders/express/quote` `{ paymentMethod, gasCylinderId?, quantity? }` → **200**
  `{ available, reason, message, fallback, address, item, quote, estimatedMinutes }`. Sin
  cobertura, horario o moto: `available: false` y `fallback: "scheduled"` (la app ofrece el flujo
  con franja horaria); `quote` es `null`.
- `POST /orders/express` `{ paymentMethod, gasCylinderId?, quantity?, notificationToken? }`
  (idempotente con `Idempotency-Key`) → **201** con el pedido (`OrderResponseDto`, con
  `deliveryMode`, `expressSurchargeAmount`, `expressDegradedAt`) y `payment_url` si es
  MercadoPago. Sin dirección predeterminada: **404**. Ya no disponible: **409** `EXPRESS_NOT_AVAILABLE`.

`OrderResponseDto` suma `deliveryMode` (`standard`/`express`), `expressSurchargeAmount` (se
conserva aunque el pedido pase al reparto común) y `expressDegradedAt` (`null` si no pasó).

## Despacho a una moto (CU-149)

`DispatchOrchestratorService` aplica una política propia a los pedidos `express`:

- Ofrece **de a uno** a los choferes en moto del radio express (`maxRadiusKm`), del más cercano al
  más lejano, con la ventana `offerTtlSeconds`. **No amplía el radio y no re-ofrece** a quien ya
  vio el pedido (aunque su oferta haya vencido). El tic del despacho es de 15 s: una ventana de
  20 s se vence, en la práctica, entre 20 y 35 s.
- Un express por MercadoPago sin pagar **no se despacha** hasta que el pago se aprueba.
- Sólo un chofer con una moto en uso lo acepta (`PATCH /orders/:id/status` → `accepted`) o se lo
  asignan (`PATCH /orders/:id/assign/:deliveryId`): si no, **400**. No figura en el pool de
  `GET /orders/available` (sí lo ve el despacho para no dejarlo sin oferta).
- La oferta (`NEW_ORDER`) trae `deliveryMode: "express"`.
- Al agotarse la lista **pasa al reparto común** (`ExpressDegradeService`, con el pedido
  bloqueado y una sola vez): `delivery_mode = standard`, `total_amount` sin el recargo,
  `express_degraded_at`, y sigue por el despacho normal. Avisa al cliente por socket
  `order:express-degraded` `{ orderId, surchargeRemoved, total, refundRequested, message }` y
  por push, y al panel por el mismo evento. Si el cliente había pagado en línea, pide la devolución
  del recargo (CU-168); en efectivo o transferencia basta con descontarlo.

## Reintegro del pago (CU-168)

La devolución es un efecto **posterior** a la cancelación: corre fuera de su transacción y un
fallo de la pasarela no la revierte. Se dispara en:

- cancelación del cliente o del administrador (`PATCH /orders/:id/cancel`, `DELETE /orders/:id`,
  `PATCH /orders/:id/status` con `cancelled`): **todo lo que falte devolver** de cada pago
  aprobado por una pasarela (seña incluida);
- un pago aprobado que llega **después** de la cancelación (webhook tardío);
- el pase de un express al reparto común: **sólo el recargo express**.

Los pagos en efectivo o transferencia, y los que nunca se aprobaron, no hacen nada. El estado de
cobro del pedido no cambia (`paymentStatus` sigue `paid`).

Cada devolución es una fila de `payment_refund` (única por pago y tipo): `kind` (`full` |
`express_surcharge`), `amount`, `status` (`pending` | `succeeded` | `failed`),
`gatewayRefundId`, `errorMessage`, `attempts`. Su `refund_id` viaja a la pasarela como **clave de
idempotencia**: repetir o reintentar no devuelve el dinero dos veces. Nunca se pide más de lo que la
pasarela cobró y no devolvió (el importe del ledger puede incluir recargos que no pasaron por
ella). Si la pasarela informa que el pago ya estaba devuelto, se marca `succeeded` sin repetir la
solicitud. Una devolución total deja el pago del ledger en `refunded`; la parcial lo deja `approved`.

Endpoints (admin o super admin con `X-Distributor`; el cliente recibe 403):

| Endpoint                              | Qué hace                                                                                                                                                                                                                                                                       |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GET /refunds?status=&limit=&offset=` | Devoluciones de la distribuidora, las más nuevas primero (`status=failed`: las que esperan reintento). `{ items, total, limit, offset }`                                                                                                                                       |
| `GET /orders/:id/refunds`             | Las del pedido. 404 si no existe o es de otra distribuidora                                                                                                                                                                                                                    |
| `POST /orders/:id/refunds/retry`      | Reintenta las fallidas y pide la del pedido cancelado que nunca se pidió. Idempotente (`Idempotency-Key`). **409** si el pedido no está cancelado ni tiene pendiente la devolución del recargo express. Una devolución que sigue fallando queda `failed` (la respuesta es 200) |

El cliente dueño del pedido ve las suyas con `GET /orders/:id/refunds/mine` (rol `customer`, sin
`X-Distributor`: el cliente es uno solo para todas): `[{ kind, amount, status, requestedAt, completedAt }]`, de la más
vieja a la más nueva, vacío si no hubo ninguna. Si el pedido se canceló después de pasar al reparto común, el recargo express no acreditado se omite: la devolución total del mismo pago ya lo incluye. `status`: `pending` (en trámite), `succeeded` (acreditada, con
`completedAt`), `failed` (la pasarela la rechazó; todavía no se acreditó y la distribuidora la revisa). No expone ids de pasarela, intentos ni el texto del
error. Un pedido ajeno o inexistente es 404.

Avisos en tiempo real: `order:payment-refunded` `{ orderId, refundId, kind, amount, at }` al cliente
(socket y push) y al panel; `order:refund-failed` `{ …, reason }` al panel.

### Pasarelas

El puerto `PaymentGatewayPort` suma `refundPayment({ gatewayPaymentId, amount, idempotencyKey })`
y `getPayment` informa `amount` y `refundedAmount`. Hoy hay **un solo adaptador**
(`MercadoPagoAdapter`, `PaymentRefund` del SDK). Stripe no existe en este back: incorporarlo
es un adaptador nuevo con su `refundPayment` y su resolución por `payment.gateway`.

## Migración

`1792244000000-ExpressYReintegros`: `order.express_surcharge_amount` (`numeric(10,2)`, 0),
`order.express_degraded_at` y la tabla `payment_refund`.
