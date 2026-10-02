# Auditoría del DTO de pedidos contra sus casos de uso

`order` es el único módulo de los 22 que serializa su salida con un DTO propio.
Antes de replicar ese patrón en los otros 21, se lo contrastó contra lo que los
**casos de uso** dicen que el sistema debe devolver.

**El criterio:** la fuente de verdad son los casos de uso, sus DSS y las 177
operaciones del Documento 3. Lo que hoy consumen el panel y las apps es una
restricción —no romper lo que anda—, **no** el contrato: las apps están
incompletas, así que un campo que nadie usa hoy puede ser algo que el caso de
uso pide y la app todavía no implementó.

---

## El contrato, según los DSS

| CU | Operación | Lo que el documento dice que devuelve |
|---|---|---|
| CU-005 | `crearPedido(...)` | pedido creado (**número, total, estado**) |
| CU-006 | `consultarPedido(id)` | ítems, total, estado, dirección, **chofer** |
| CU-007 | `consultarHistorialDePedidos(...)` | página (**total, cantidad, listado**) |
| CU-008 | `cancelarPedido(id, motivo)` | estado CANCELADO, **stock restituido** |
| CU-015 | `aceptarPedido(pedido)` | datos de entrega **y código de entrega** |
| CU-018 | `actualizarEstadoDePedido(...)` | estado EN_CAMINO |
| CU-020 | `confirmarEntrega(...)` | código para QR, pedido entregado |
| CU-072 | `crearReserva(...)` | número, total, **seña**, estado + **enlace de pago** |
| CU-073 | `listarReservas()` | **cliente**, total, seña, **si está paga**, **saldo** |
| CU-080 | `consultarPedidosDisponibles(...)` | dirección, ítems, total |
| CU-081 | `consultarPedidosAsignados(...)` | estado, **cliente**, dirección, total |

---

## Qué cumple y qué no

### Cumple

Número, total, estado, ítems con su producto, dirección completa, método de
pago, fechas, seña (`depositAmount`), si está paga (`depositPaid`), saldo
(`remainingBalance`) y enlace de pago (`paymentUrl`). El sobre de paginación
devuelve `total`, `limit`, `offset` y `orders`, que satisface lo que pide CU-007.

### No cumple — tres brechas verificadas

**1. El cliente no se expone nunca.** CU-073 y CU-081 lo piden explícitamente, y
CU-006 pide el detalle completo. El DTO tiene `customer_notes` —las notas— pero
**ningún dato de identidad**: ni nombre ni teléfono.

Un chofer que consulta sus pedidos asignados **no puede saber a quién le está
entregando ni cómo llamarlo**.

Lo llamativo: la consulta **sí carga** `customer` y `customer.customer` de la
base. Se paga el costo de traerlo y después el DTO lo descarta.

**2. El chofer se expone pero siempre viene vacío.** El DTO declara
`delivery_name` y el mapper lo llena desde `order.delivery.user.full_name`, pero
`findByDelivery` **no carga las relaciones `delivery` ni `delivery.user`**:

```ts
relations: ['customer', 'customer.customer', 'items',
            'items.gasCylinder', 'address', 'timeSlot']
```

Verificado contra datos reales: un chofer con **32 pedidos** asignados, cuyo
usuario se llama "QA Chofer Automatico", devuelve `delivery_name: null` en los
32. El campo existe en el contrato y nunca tiene valor.

Está exactamente al revés: **se carga lo que no se expone y se expone lo que no
se carga.**

**3. El código de entrega no vuelve al aceptar.** CU-015 dice que aceptar un
pedido devuelve *"datos de entrega **y código de entrega**"*. El DTO no lo
incluye: el chofer tiene que hacer una segunda llamada a
`GET /orders/{id}/delivery-code`. Es lo que hace la app hoy, así que funciona,
pero **no es lo que dice el documento** y cuesta un viaje de red de más en el
momento justo en que el chofer arranca el reparto.

### Sin verificar todavía

CU-008 dice que cancelar devuelve *"estado CANCELADO, **stock restituido**"*. El
stock se restituye —está en el caso de uso de cancelación— pero **la respuesta
no informa nada al respecto**. Falta decidir si el documento pide que se
informe o si alcanza con que ocurra.

---

## Qué significa para el paso siguiente

El DTO de `order` **no se puede usar como molde tal cual**: replicarlo en los
otros 21 módulos propagaría el criterio de "exponer lo que había a mano" en vez
de "exponer lo que el caso de uso pide".

El orden que se desprende:

1. **Corregir las tres brechas de `order`** y recién entonces usarlo de molde.
2. Para cada módulo siguiente, **leer primero sus DSS**, después mirar la
   entidad, y diseñar el DTO desde el caso de uso.
3. Anotar, por cada campo que el CU pide y ningún cliente consume, **qué app
   tiene ese trabajo pendiente**. Eso arma solo el backlog de las apps.

## Lo que esta auditoría deja como método

Sirvió para encontrar un bug que ninguna prueba de la colección podía detectar:
`delivery_name: null` es una respuesta perfectamente válida —200, JSON correcto,
el campo presente— y sólo se ve como defecto **cuando se la compara contra lo
que el caso de uso dice que tiene que traer**.

Ninguna cantidad de tests de contrato HTTP lo hubiera encontrado. El documento
sí.
