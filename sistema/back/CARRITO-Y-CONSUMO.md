# Carrito persistente y consumo declarado (C-12 y C-13)

CU-122 a CU-126 (carrito) y CU-143 y CU-144 (consumo promedio declarado). Todo está también en
Swagger (`/docs`, tags "Cart" y "Customers"). No incluye CU-145 ni CU-146 (módulo M3).

## Carrito (`/cart`)

Rol `customer`. El dueño sale siempre del token. **`X-Distributor` es obligatorio** (sin él, 400):
hay un carrito por cliente y distribuidora (`UQ_cart_user_distributor`), así que el mismo cliente
tiene carritos separados en cada empresa. Administrador y chofer: 403.

Todas las operaciones responden el carrito completo (`CartResponseDto`):

| Campo                 | Tipo              | Qué es                                                                      |
| --------------------- | ----------------- | --------------------------------------------------------------------------- |
| `cartId`              | `uuid \| null`    | `null` si el cliente todavía no tiene carrito (se ve vacío, no es un error) |
| `distributorId`       | `uuid`            | La del header                                                               |
| `items[]`             | `CartItem[]`      | Ordenados por tipo de garrafa                                               |
| `totalUnits`          | `integer`         | Unidades de los ítems disponibles                                           |
| `total`               | `number`          | Suma de los subtotales, sobre los **precios vigentes del catálogo**         |
| `hasPriceChanges`     | `boolean`         | Algún ítem tiene un precio guardado distinto del vigente                    |
| `hasUnavailableItems` | `boolean`         | Algún tipo se dio de baja después de agregarlo                              |
| `updatedAt`           | `date-time\|null` | Última modificación                                                         |

Cada ítem: `cartItemId`, `gasCylinderId`, `type`, `quantity`, `savedUnitPrice` (lo que vio el
cliente al agregar), `currentUnitPrice` (catálogo hoy), `priceDifference` (vigente menos guardado),
`subtotal` (cantidad por vigente; 0 si no está disponible), `available` (`false` si el tipo se dio
de baja: se muestra marcado y no suma) y `hasEnoughStock` (`false` si el stock vendible no alcanza
para la cantidad).

| Método y ruta                | CU     | Cuerpo                        | Respuesta | Errores                                                                                                                                      |
| ---------------------------- | ------ | ----------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET /cart`                  | CU-125 | —                             | 200       | —                                                                                                                                            |
| `POST /cart/items`           | CU-122 | `{ gasCylinderId, quantity }` | 201       | 400 cantidad no entera, menor que 1 o que supera 999 (sumando lo que ya había); 404 tipo inexistente, dado de baja o de otra distribuidora   |
| `PATCH /cart/items/:itemId`  | CU-123 | `{ quantity }`                | 200       | 400 cantidad cero, negativa o no entera (el mensaje manda a quitar el ítem); 404 ítem que no es del carrito del cliente en esa distribuidora |
| `DELETE /cart/items/:itemId` | CU-124 | —                             | 200       | 404 ítem que no es del carrito del cliente en esa distribuidora                                                                              |
| `DELETE /cart`               | CU-126 | —                             | 200       | — (sin carrito no hace nada y responde uno vacío)                                                                                            |

Reglas:

- **El carrito no fija el precio.** Al agregar guarda el vigente como referencia de lo que vio el
  cliente (y lo renueva si vuelve a agregar el mismo tipo). El pedido se cobra al precio vigente
  del catálogo; el cliente se entera de la diferencia en `GET /cart` antes de confirmar.
- **El carrito no reserva stock.** `hasEnoughStock` es sólo informativo; el stock se controla al
  crear el pedido.
- El total usa el precio de lista del catálogo; las promociones por volumen y los recargos de pago
  los aplica el pedido (`POST /orders/quote`), no el carrito.
- Agregar un tipo que ya está suma la cantidad (no hay ítems repetidos).
- Concurrencia: toda escritura toma el candado de la fila del carrito; diez altas simultáneas del
  mismo tipo suman diez.
- Quitar borra el ítem de verdad. `cart` y `cart_item` están excluidas de la auditoría de datos.
- **Checkout (CU-126 invocado por el sistema):** `POST /orders` y `POST /orders/quote` con
  `fromCart: true` toman los ítems del carrito y lo vacían con `CartService.vaciarEnTransaccion`
  dentro de la transacción del pedido (ver «Crear desde el carrito» en `PEDIDOS.md`). Carrito
  vacío o con productos dados de baja: 400.
- Modificar la cantidad de un tipo dado de baja es 400 (igual que agregarlo); hay que quitarlo.

### Contrato que necesita la app del cliente

1. Mandar `X-Distributor` en todas las llamadas de `/cart`.
2. Cada tap de "agregar" es `POST /cart/items`; el stepper del carrito es `PATCH` (mínimo 1) y el
   tacho `DELETE /cart/items/:itemId`; "vaciar" es `DELETE /cart`.
3. Mostrar `priceDifference` y `hasPriceChanges` antes de confirmar; mostrar los ítems con
   `available: false` como no disponibles (no suman) y `hasEnoughStock: false` como aviso.
4. Al confirmar, `POST /orders` con `fromCart: true` y **sin `items`** (el servidor toma el carrito, cobra el precio vigente y lo vacía en la misma transacción). **La app no borra ítems.** `POST /orders/quote` con `fromCart: true` cotiza el carrito. La compra exprés, sin carrito, sigue mandando `items`.

## Consumo promedio declarado

Los datos viven en la ficha del cliente (`customer`): `avg_monthly_consumption_kg`,
`declared_cylinder_type_id` y `next_repurchase_estimate_at` (ya migrados, sin migración nueva).

Regla de cálculo (`repurchase/domain/consumption.ts`):

- `kg por mes = peso del tipo de garrafa × garrafas por mes`, a 2 decimales. Se guarda en kilos
  para que siga sirviendo si el cliente cambia de tipo.
- Rango razonable: **5 a 500 kg por mes**. Fuera de rango el sistema responde **400** y pide
  confirmación; se acepta reenviando `confirmOutOfRange: true`.
- Fecha estimada de recompra = inicio + (kg de la compra ÷ kg por mes) × 30 días. Con compras, el
  inicio es la entrega del último pedido entregado del cliente (de cualquier distribuidora) y los
  kg son los de ese pedido. Sin compras, el inicio es el momento de la declaración y los kg son los
  de una garrafa llena del tipo habitual.

### CU-143: al registrarse

`POST /auth/registro` acepta `consumption` (opcional):

```json
{
  "consumption": {
    "cylinderTypeId": "uuid",
    "quantityPerMonth": 2,
    "confirmOutOfRange": false
  }
}
```

- Si se omite, el registro sigue igual y el dato queda vacío.
- Se valida **antes** de crear la cuenta en Firebase: un consumo inválido (400) no deja usuario ni
  cuenta. Si es válido, se guarda en la misma transacción que la ficha.
- `cylinderTypeId` tiene que existir y estar activo (400 si no). Como el cliente se registra sin
  distribuidora, no se acota por distribuidora: la app ofrece los tipos de la distribuidora en
  contexto.
- Sólo vale para clientes; en el alta de otros roles se ignora.

### CU-144: modificarlo

Rol `customer`.

| Método y ruta                     | Cuerpo                                                      | Respuesta                    |
| --------------------------------- | ----------------------------------------------------------- | ---------------------------- |
| `GET /customers/me/consumption`   | —                                                           | 200 `ConsumptionResponseDto` |
| `PATCH /customers/me/consumption` | `{ cylinderTypeId?, quantityPerMonth, confirmOutOfRange? }` | 200 `ConsumptionResponseDto` |

`ConsumptionResponseDto`: `cylinderTypeId`, `cylinderType` (p. ej. `10kg`), `avgMonthlyConsumptionKg`
y `nextRepurchaseEstimateAt`; todo `null` si nunca declaró.

- `cylinderTypeId` es opcional si el cliente ya tiene uno habitual (se mantiene); si nunca declaró
  uno y no lo manda, **400**. Si lo manda y hay `X-Distributor`, tiene que ser de esa distribuidora.
- `quantityPerMonth`: número de 0,01 a 1000 con hasta 2 decimales (400 si no). Es opcional si se manda
  `cylinderTypeId` y el cliente ya declaró su consumo: se cambia sólo la garrafa y se mantienen los
  kg por mes. Un cuerpo sin ninguno de los dos es 400.
- Un consumo que da 0 kg por mes es 400 aun con `confirmOutOfRange`.
- Tipo inexistente o dado de baja: 400. Valor fuera de rango sin confirmar: 400 y no se guarda.
- Recalcula la estimación desde la última compra entregada; sin compras, desde ahora.

### Lo que ve el administrador

`CustomerResponseDto` (`GET /customers`, `/customers/:id`, `/customers/user/:userId`, y el
`customer` anidado de `GET /users/email/:email`, el alta y demás lecturas de usuario) suma
`avgMonthlyConsumptionKg`, `declaredCylinderTypeId`, `declaredCylinderType` (nombre del tipo, p. ej.
`10kg`) y `nextRepurchaseEstimateAt`, todos `null` si el cliente no declaró. El panel muestra en la
pestaña "Resumen" de la ficha el consumo y la garrafa habitual, esta última sólo si el tipo es de la
distribuidora del admin (el catálogo es por distribuidora; si es de otra, «Sin declarar»). **No muestra la
recompra estimada**: sale de compras en cualquier distribuidora y revelaría actividad ajena a la empresa. El administrador no modifica el consumo: es una declaración del
cliente.

### Contrato que necesita la app del cliente

1. Registro: enviar `consumption` si el cliente lo completa (ofreciendo los tipos de la
   distribuidora en contexto, `GET /gascylinder/available/list`); ante el 400 de "fuera de rango", pedir
   confirmación y reenviar con `confirmOutOfRange: true`.
2. Perfil: leer con `GET /customers/me/consumption` y corregir con `PATCH` (mismo manejo del
   400 de rango).

## Pendiente (fuera de C-12 y C-13)

- `pedido.entregado` no vuelve a correr la estimación: lo toma el módulo M3 (CU-146).
