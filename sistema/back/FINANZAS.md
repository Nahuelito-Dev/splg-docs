# Caja, rendiciones, cuentas corrientes y comisiones

Iteración C-20 (M-D; el diseño completo está en
`.orquesta/runs/2026-10-03-modulos-empresa/DISENO-MODULOS.md`, sección 5). Cinco módulos:

| Módulo                   | Qué hace                                                             | CU                               |
| ------------------------ | -------------------------------------------------------------------- | -------------------------------- |
| `src/cash/`              | Cajas, sesiones con arqueo, categorías y el **libro de movimientos** | 225-230, 264, 265, 309, 310, 340 |
| `src/driver-settlement/` | Rendición diaria del chofer                                          | 231-234, 330                     |
| `src/customer-account/`  | Cuentas corrientes de clientes y su libro                            | 235-239, 329, 331, 332           |
| `src/commission/`        | Reglas, libro de comisiones y liquidaciones                          | 240-244, 333-335                 |
| `src/finance/`           | Tablero financiero y conciliación nocturna                           | 245                              |

Toda tabla lleva `distributor_id`; todo endpoint filtra por la distribuidora en contexto
(`X-Distributor` para el superadmin) y lo de otra distribuidora responde **404**. Todo importe
es `numeric` en la base y `decimal.js` en el dominio (nunca `float`); los `POST`/`PATCH` que
mueven plata llevan `@Idempotent()` (header `Idempotency-Key`).

## Modelo

| Tabla                                                       | Qué es                                                                                                                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cash_box`                                                  | Caja: `cash` (no admite saldo negativo, CHECK), `bank` o `wallet`. `balance` = Σ del libro. `requires_session` por caja.                               |
| `cash_session`                                              | Apertura/cierre con arqueo. Único parcial `WHERE status = 'open'`: una abierta por caja.                                                               |
| `cash_category`                                             | Ingresos y gastos. Diez **de sistema** (`system_code`) por distribuidora: no se editan ni se desactivan.                                               |
| `cash_movement`                                             | Libro **de solo agregar** (disparador). Importe > 0 y sentido `in`/`out`. Se corrige con un contraasiento (`reverses_movement_id`, único).             |
| `driver_settlement` (+ `_order`, `_expense`, `_collection`) | Rendición del chofer; `_order.order_id` es único: un pedido se rinde una sola vez.                                                                     |
| `customer_account`                                          | Cuenta del cliente con **una** distribuidora (único vigente por distribuidora y cliente). `balance` positivo = el cliente debe.                        |
| `customer_account_entry`                                    | Libro **de solo agregar**: `sale_charge` (único por pedido), `payment`, `credit_note`, `debit_note`. Importe siempre positivo; el signo lo da el tipo. |
| `customer_account_allocation`                               | Imputación FIFO de pagos y notas de crédito a cargos.                                                                                                  |
| `commission_rule`                                           | Regla por entrega: `per_unit`, `per_order`, `percent_of_total`.                                                                                        |
| `commission_entry`                                          | Libro de comisiones **con signo**; sólo deja asignar/liberar `liquidation_id`.                                                                         |
| `driver_liquidation`                                        | Liquidación en borrador → aprobada → pagada, o anulada. Numerada por `document_sequence`.                                                              |

La migración `CajaYRendicion` crea las tablas, los tres disparadores de solo agregar y siembra la
"Caja central" y las categorías de sistema de cada distribuidora existente (las nuevas las siembra el
evento `distribuidora.creada`). Una migración aparte, `VentaACuentaEnPedido`, agrega `account` a
`order.paymentMethod` y `order.paymentType` (un valor de enum no se usa en la transacción que lo agrega).

## Reglas centrales

- **`CashLedgerService.registrar` es el único punto por el que el dinero entra o sale de una caja.**
  Bloquea la caja (`FOR UPDATE`), valida sesión (si la caja la exige), que la categoría sea del mismo
  sentido, que una caja de efectivo no quede en negativo, inserta el movimiento y actualiza `balance`, todo
  en la transacción de quien llama. La rendición, el cobro de cuenta corriente y el pago de liquidaciones
  registran por acá. Invariante: `balance = Σ entradas − Σ salidas` (la conciliación nocturna lo verifica).
- **Arqueo:** `esperado = apertura + Σ movimientos de la sesión` (sin el ajuste de apertura);
  `diferencia = contado − esperado`. Si no es cero se asienta un ajuste (categoría de sistema "sobrante" o
  "faltante de caja") y el saldo queda igual a lo contado. Abrir con un monto distinto del saldo del libro
  asienta un ajuste de apertura.
- **Anular** = contraasiento con la misma categoría y el sentido opuesto. Un movimiento se anula una sola vez
  (índice único), una anulación no se anula, y no exige sesión abierta (si hay una, se le asigna). **Sólo se
  anulan los movimientos manuales** (`POST /cash-movements/:id/reverse`); los demás responden 400 y el mensaje
  dice por dónde se corrigen:
  - pata de una transferencia: `POST /cash-movements/:id/reverse-transfer` (revierte las dos patas);
  - pago de una liquidación: `PATCH /driver-liquidations/:id/unpay`;
  - cobro de cuenta corriente: un ajuste (nota de crédito/débito) en la cuenta del cliente;
  - rendición aprobada (no se reabre) y ajustes de apertura o de arqueo: un movimiento manual que lo explique.
- **Transferir** = salida + entrada en una sola transacción; las dos cajas se bloquean ordenadas por id.
  **Anular una transferencia** revierte las dos patas juntas en una transacción, con las dos cajas bloqueadas en el
  mismo orden: primero se devuelve lo que entró al destino (si es de efectivo y ya no alcanza, 409 y no se anula
  nada) y después se repone el origen. Se puede pedir por cualquiera de las dos patas.
- **Categorías**: una desactivada no se usa en movimientos nuevos ni en gastos de rendición (400); la anulación
  de un movimiento viejo sí puede usarla. **Cajas**: una caja con saldo distinto de cero no se desactiva (409);
  el tablero suma también las desactivadas que conserven saldo.
- **Rendición:** una por chofer y día de negocio (hora argentina). `expected_cash = Σ saldo a cobrar de los
pedidos en efectivo entregados y sin rendir + Σ cobros de cuenta corriente hechos en la calle`.
  El saldo a cobrar es el total menos la seña ya paga (la misma regla que la rendición del camión): esto
  cierra el "Problema a resolver 1" de la iteración. Cuentan los pedidos `paid` y `pending` (el chofer aún no
  confirmó); los `unpaid` y `written_off` no se cobraron y quedan afuera. Lo entregado después de presentar
  cae en la rendición del día siguiente; los pedidos de un día anterior cuya rendición sigue abierta son de
  esa. Un pedido cuyo cobro registró o resolvió un administrador (`paymentResolvedBy`: `register-cash`,
  `resolve-unpaid` como cobrado) lo cobró el admin, no el chofer: no entra en lo esperado. El proceso nocturno
  (23:30) usa la misma regla para elegir a quién abrirle rendición, con el día argentino como instante, así que no
  abre rendiciones que quedarían vacías.
  `diferencia = declarado + gastos − esperado` (negativa: faltante). Aprobar: entrada a la caja por el
  efectivo declarado; con diferencia hay que resolverla (`absorbed` o `charged_to_driver`, esta última sólo
  para faltantes, que genera la deducción negativa en el libro de comisiones). Si está atada a una carga del
  camión, no se aprueba hasta que la carga esté cerrada. Una aprobada no se reabre.
- **Venta a cuenta:** `POST /orders` con `paymentMethod: account`, sólo administrador. En la misma transacción
  del pedido (después de reservar el stock) `CustomerAccountPort.assertCredito` bloquea la cuenta y exige que
  esté activa y que `total ≤ límite − saldo − pedidos a cuenta aún sin cargo`. El cargo se asienta al
  entregar (evento `pedido.entregado`, idempotente por pedido) con vencimiento a `payment_terms_days`. Un pedido
  a cuenta no se edita. `paymentStatus` queda `pending`: no entra en "venta cobrada" de los reportes.
- **Pago de cuenta corriente:** el administrador indica la caja (entrada por el libro de caja); el chofer en la
  calle no manda caja: el cobro queda atado a su rendición abierta y entra a la caja al aprobarla. Imputación FIFO
  automática. Pagar de más deja saldo a favor.
- **Comisión por entrega:** al entregar (`pedido.entregado`) se resuelve la regla vigente el día de la entrega
  (empleado y producto > empleado > producto > general) renglón por renglón; el asiento guarda una copia de las
  reglas aplicadas (`rule_snapshot`), así que modificar una regla no recalcula nada. Único por pedido.
- **Liquidación:** toma bajo lock los asientos sin liquidar del chofer en el período (el número de documento
  se toma al final). Aprobar congela; pagar asienta el egreso del neto en una caja; anular libera los asientos.
  Una pagada no se anula directo: **anular el pago** (`PATCH /driver-liquidations/:id/unpay`, con motivo) asienta
  el contraasiento en la misma caja y la deja aprobada, lista para pagarse de nuevo o anularse.

### Orden de locks

`pedido → chofer → carga del camión → rendición → caja → cuenta corriente → numeración`. El cobro del chofer
toma la rendición antes que la cuenta; el pago del administrador, la caja antes que la cuenta; la liquidación
toma sus asientos y deja la numeración para el final. Los tests de concurrencia verifican que no haya
deadlocks (`withTransactionRetry` no tiene que haber reintentado).

### Procesos programados (hora argentina, con bloqueo en Redis)

| Hora  | Proceso                                                                                                                                                                       | CU       |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| 23:30 | `DriverSettlementCron`: abre la rendición de cada chofer con efectivo sin rendir                                                                                              | 231      |
| 08:00 | `DriverSettlementCron`: mail a los admins con las rendiciones de días anteriores sin cerrar (`overdue_alerted_at` evita repetir)                                              | 234      |
| 03:30 | `FinanceReconciliationCron`: recupera comisiones y cargos de las entregas de los últimos 7 días que quedaron sin asiento, y registra los saldos que no coinciden con su libro | 241, 332 |

## Endpoints

`@Auth(ADMIN, SUPER_ADMIN)` salvo indicación. Listados: `{ data, total }`.

| Método                                    | Ruta                                                             | CU                                                                      | Errores principales                                                                                                       |
| ----------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| GET / POST                                | `/cash-boxes`                                                    | 225                                                                     | 409 nombre repetido · 400 tipo inválido                                                                                   |
| GET / PATCH                               | `/cash-boxes/:id`                                                | 264                                                                     | 404 · 409 desactivar con sesión abierta o con saldo                                                                       |
| POST / GET                                | `/cash-boxes/:id/sessions`                                       | 226                                                                     | 409 ya abierta · 400 no exige sesión o monto negativo                                                                     |
| GET                                       | `/cash-sessions/:id`                                             | 227                                                                     | 404                                                                                                                       |
| PATCH                                     | `/cash-sessions/:id/close`                                       | 227                                                                     | 409 ya cerrada · 400 contado negativo                                                                                     |
| GET / POST                                | `/cash-movements`                                                | 340 / 228, 309                                                          | 409 sin sesión o saldo insuficiente · 400 categoría de otro sentido o importe ≤ 0 · 422 clave de idempotencia reutilizada |
| POST                                      | `/cash-movements/transfer`                                       | 310                                                                     | 400 mismo origen y destino · 409 saldo/sesión                                                                             |
| POST                                      | `/cash-movements/:id/reverse`                                    | 229                                                                     | 409 ya anulado, es anulación o deja efectivo negativo · 400 sin motivo o no es manual                                     |
| POST                                      | `/cash-movements/:id/reverse-transfer`                           | 310                                                                     | 409 ya anulada o el destino no tiene el saldo · 400 sin motivo o no es transferencia                                      |
| GET / POST / PATCH / DELETE               | `/cash-categories` (el GET también para `DELIVERY`: gastos de la rendición) | 230, 265                                                                | 409 duplicada o de sistema                                                                                                |
| GET / POST                                | `/driver-settlements`                                            | 231 (alta manual)                                                       | 409 ya existe · 404 chofer                                                                                                |
| GET                                       | `/driver-settlements/mine?date`                                  | 232 (`DELIVERY`)                                                        | abre la del día si no existe                                                                                              |
| GET                                       | `/driver-settlements/:id`                                        | 232, 233                                                                | el chofer sólo ve las suyas                                                                                               |
| POST                                      | `/driver-settlements/:id/submit`                                 | 232 (`DELIVERY` o admin)                                                | 409 no abierta · 400 negativos o gasto sin categoría de egreso                                                            |
| PATCH                                     | `/driver-settlements/:id/approve`                                | 233                                                                     | 409 no presentada, sin sesión o carga abierta · 400 diferencia sin resolver                                               |
| PATCH                                     | `/driver-settlements/:id/reopen`                                 | 330                                                                     | 409 no presentada                                                                                                         |
| GET / POST                                | `/customer-accounts`                                             | 235, 238                                                                | 409 ya hay cuenta · 400 CUIT/límite/plazo · 404 cliente                                                                   |
| GET                                       | `/customer-accounts/aging`                                       | 239                                                                     |                                                                                                                           |
| GET / PATCH                               | `/customer-accounts/:id`                                         | 331                                                                     | 409 cerrar con saldo ≠ 0                                                                                                  |
| GET                                       | `/customer-accounts/:id/entries?from&to`                         | 238                                                                     | saldo corrido, apertura y cierre                                                                                          |
| POST                                      | `/customer-accounts/:id/payments`                                | 237 (admin o `DELIVERY`; al chofer se le devuelve `balanceAfter: null`) | 409 sin caja/sesión/rendición abierta · 400 el chofer manda caja u otro medio                                             |
| POST                                      | `/customer-accounts/:id/adjustments`                             | 329                                                                     | 409 cuenta cerrada · 400 sin motivo                                                                                       |
| POST `/orders` (`paymentMethod: account`) |                                                                  | 236                                                                     | 409 sin cuenta/bloqueada/crédito (informa el disponible) · 403 no admin                                                   |
| GET / POST / PATCH                        | `/commission-rules`                                              | 240, 333                                                                | 409 solapada · 400 base/valor/vigencia                                                                                    |
| GET                                       | `/commissions`                                                   |                                                                         | filtros empleado, tipo, período, liquidadas                                                                               |
| GET                                       | `/commissions/mine?from&to`                                      | 244 (`DELIVERY`)                                                        | 404 sin legajo                                                                                                            |
| GET / POST                                | `/driver-liquidations`                                           | 242                                                                     | 409 sin asientos · 400 período                                                                                            |
| GET                                       | `/driver-liquidations/:id`                                       |                                                                         | con sus asientos                                                                                                          |
| PATCH                                     | `/driver-liquidations/:id/approve` · `/pay` · `/unpay` · `/void` | 334, 243, 243 (anular el pago), 335                                     | 409 estado · 409 caja sin saldo/sesión · 400 `unpay` sin motivo                                                           |
| GET                                       | `/finance/dashboard?date`                                        | 245                                                                     | 400 fecha                                                                                                                 |

## Contrato para la app del chofer (tanda posterior)

La app del chofer todavía no consume nada de esto. Lo que le toca, ya disponible:

- **Mi rendición:** `GET /driver-settlements/mine?date` (abre la del día) y
  `POST /driver-settlements/:id/submit` con `{ declaredCash, expenses: [{ categoryId, amount, description? }], notes? }`.
  Las categorías de gasto se piden a un administrador (el chofer no lista `/cash-categories`: la app debería
  recibir una lista fija, o se habilita una lectura para `DELIVERY`).
  Cada entrega de `orders` trae `customerName` y `deliveryAddress` (la dirección formateada, o calle, piso,
  depto y ciudad; `null` si falta) para reconocerla en la rendición. No incluye teléfono, coordenadas ni
  indicaciones.
- **Cobrar cuenta corriente en la calle:** `POST /customer-accounts/:id/payments` con `{ amount, method: 'cash' }`
  (sin `cashBoxId`). Requiere la rendición del día abierta.
- **Mis comisiones:** `GET /commissions/mine?from&to` → `{ data, total, totalAmount, pendingAmount, liquidatedAmount }`.
- **Pedidos a cuenta en la app:** `order.payment_method` ahora puede ser `account` (antes sólo `cash`/`online`).
  Un pedido a cuenta **no se cobra en la entrega**: la app no debe pedir confirmar el efectivo.

## Desvíos del diseño

- El solapamiento de reglas de comisión se valida en el servicio bajo un lock por distribuidora (advisory lock)
  y no con una restricción de exclusión `gist`: esa necesita `btree_gist` y TypeORM no la modela, así que el
  chequeo de diferencias del esquema la querría borrar.
- `delivery.balance` (D8) **no** se migró al libro de comisiones: queda como está. Los faltantes de rendición
  a cargo del chofer ya van al libro nuevo (`settlement_shortage`).
- Las multas imputadas y la carga de combustible no generan egreso de caja todavía (M-B no tiene esos módulos
  en esta rama); las categorías de sistema `fuel`, `traffic_fine` y `purchase` ya están sembradas.
- Un chofer puede registrar un cobro en cualquier cuenta de su distribuidora (no se limita a los clientes que atiende); lo que no ve es el saldo de la cuenta.
- Los gastos que el chofer paga con la cobranza reducen lo que entrega pero no generan egreso en la caja.
- Los adjuntos (`attachment`) de movimientos y rendiciones no están conectados.

## Cobro del administrador sobre un pedido en efectivo

`PATCH /orders/:id/payment/register-cash` y `PATCH /orders/:id/payment/resolve-unpaid` (con `resolution: paid`)
reciben `cashBoxId` y asientan el efectivo en la **misma transacción** que marca el pedido pagado, por
`CashLedgerService.registrar`: entrada por el **saldo a cobrar** (total menos la seña ya paga, la misma
`saldoACobrar` de la rendición del chofer; si da 0 no se asienta), `method: cash`, categoría de sistema
`order_payment` "Cobro de pedido", `referenceType: order_payment`, `referenceId` = el pedido. Regla:

- Sólo entran a cajas de **efectivo** (`kind = cash`). La caja elegida de otro tipo es 400.
- La distribuidora tiene alguna caja de efectivo activa: `cashBoxId` es **obligatorio** (400 si falta; se chequea antes de tocar el pedido).
- No tiene ninguna: se cobra sin movimiento. Carrera conocida: si otro administrador crea la primera caja de efectivo entre el chequeo y el asiento, el cobro queda sin movimiento; se corrige con un ingreso manual.
- Caja de otra distribuidora o inexistente: 404. Caja que exige sesión sin sesión abierta, o desactivada: 409 y el pedido no cambia.
- Repetir la operación sobre un pedido ya cobrado es un no-op: no asienta otra entrada. `written_off` no es un cobro y no toca ninguna caja.
- **Un pedido que la rendición del chofer ya tomó** (`driver_settlement_order`) no se cobra ni se marca impago desde el administrador, ni se resuelve como cobrado (`resolve-unpaid` con `paid`), ni el chofer lo informa impago (`unpaid`): 409 «El chofer ya rindió este pedido» (si no, el dinero entraría dos veces). La carrera contraria la cubre `presentar` de la rendición, que bloquea (`FOR UPDATE`) los pedidos que toma y reevalúa `payment_resolved_by`.
- Un movimiento `order_payment` no se anula a mano. Si la caja fue la equivocada se corrige con una transferencia entre cajas (CU-310); el importe no se corrige desde caja: se registra un ajuste o egreso manual con motivo.

Migración `1792500000000-CobroDePedidoACaja`: suma `order_payment` a los enums de categoría de sistema y de origen
del movimiento (la categoría se siembra al usarse en las distribuidoras existentes).

## Pagos en efectivo de la distribuidora (compras, multas y combustible)

El efectivo que la distribuidora paga por un documento sale de una caja de efectivo por el libro (`CashLedgerService`, vía
`CashDocumentPaymentService`), en la **misma transacción** del documento. Usa las categorías de sistema `purchase`,
`traffic_fine` y `fuel` y los orígenes `purchase_receipt`, `traffic_fine` y `fuel_load`, con el documento como referencia.

| Documento | Endpoint | Entrada | Anulación |
| --- | --- | --- | --- |
| Recepción de compra | `PATCH /purchase-receipts/:id/payment-status` | `paymentStatus: paid`, `paidInCash`, `cashBoxId` | Marcarla `unpaid` asienta el contraasiento |
| Multa (CU-199) | `PATCH /fleet/fines/:id/pay` | `paidInCash`, `cashBoxId` | Una pagada no se anula: movimiento manual |
| Combustible (CU-195, CU-320) | `POST /fleet/fuel-loads` (`cash_box`); la del chofer, `PATCH /fleet/fuel-loads/:id/cash-payment` | `cashBoxId` | `DELETE /fleet/fuel-loads/:id` asienta el contraasiento |

Reglas comunes: con cajas de efectivo activas `cashBoxId` es obligatorio cuando el pago es en efectivo (400); sin ninguna,
se paga sin movimiento. Sólo cajas `kind = cash` (400 si no), de la distribuidora (404), con sesión abierta si la exige y
saldo suficiente (409, y el documento no cambia: rollback). `cashBoxId` sin pago en efectivo, 400. Repetir la operación no
asienta dos veces. Un movimiento de estos orígenes no se anula con `POST /cash-movements/:id/reverse` (400 con el mensaje
de cómo se corrige desde el documento). Orden de locks: documento → caja.

Combustible del chofer: `driver_cash` es el efectivo del propio chofer (sin asiento; lo rinde como gasto en su rendición);
`cash_box` queda pendiente de asentar hasta que un administrador elige la caja. Detalle en `FLOTA-AMPLIADA.md`.

**Riesgo de doble salida:** el gasto que el chofer declara en su rendición no está ligado a la carga. Una carga `cash_box`
se resuelve por una sola vía: el administrador la asienta en una caja **o** el chofer la rinde como gasto, no ambas. Por eso
una carga del chofer no cambia entre `driver_cash` y `cash_box` (409). Las `cash_box` anteriores a la migración
(`cash_payment_legacy`) no se asientan (409): se corrigen, si hace falta, con un egreso manual con motivo.

Migración `1792600000000-EgresosDeEfectivoACaja`: `cash_movement_id` en `traffic_fine` y `fuel_load`, más
`registered_by_driver` y `cash_payment_legacy` en `fuel_load`.

## Gastos de la flota y compras desde cualquier caja (API v2)

Todo gasto de la flota es un egreso de Caja y el reintegro del seguro de un siniestro es un ingreso. En la v2 cada gasto
se paga **una sola vez** desde una caja de **efectivo, banco o billetera** (caja obligatoria; el medio sale de la clase de
la caja: banco → transferencia, billetera → Mercado Pago), con `Idempotency-Key`, en una transacción con el lock del
documento. Cuerpo común: `{ cashBoxId, paidAt }` (`paidAt` no futuro ni anterior al gasto).

| Gasto | Endpoint (`/api/v2`) | Movimiento |
| --- | --- | --- |
| Tarea de flota hecha con costo (service, VTV, frenos…) | `POST /fleet/tasks/:id/pay` `{ cashBoxId, paidAt, amount? }`, o al cerrarla: `POST /fleet/tasks/:id/close` con `payment: { cashBoxId, paidAt? }` | egreso «Mantenimiento de flota» (`fleet_maintenance`), «<plan> — <patente o chofer>» |
| Neumático (la compra) | `POST /fleet/tires/:id/pay` | egreso «Neumáticos» (`tires`) por su costo |
| Siniestro: lo que pagó la empresa | `POST /fleet/accidents/:id/pay` `{ cashBoxId, paidAt, amount }` | egreso «Siniestros» (`vehicle_accident`) |
| Siniestro: reintegro del seguro | `POST /fleet/accidents/:id/reimbursement` `{ cashBoxId, receivedAt, amount }` | **ingreso** «Reintegros de seguros» (`insurance_reimbursement`) |
| Carga de combustible con tarjeta, cuenta de combustible o `cash_box` sin asentar | `POST /fleet/fuel-loads/:id/pay` | egreso `fuel` |
| Recepción de compra | `POST /purchase-receipts/:id/pay` | egreso `purchase` |

Los `GET` v2 de tareas, neumáticos, siniestros, cargas y recepciones dicen si el gasto está pago (`isPaid`, `paidAt`,
`cashMovementId`; las tareas, además, `payable` y `notPayableReason`).

Reglas:

- **El seguro se paga por sus cuotas** (`SEGUROS.md`): una tarea del plan de seguro no se paga por acá (409 «El seguro se
  paga por sus cuotas»); si no, la misma prima saldría dos veces. Cancelar una póliza no reabre una tarea que ya tiene un
  pago registrado: la saltea con una nota.
- Un gasto ya pago, **409**. Un pago parcial (`amount` menor que el costo) deja el resto sin pagar y el gasto figura pago.
- Importe: la tarea no supera su costo; el siniestro cerrado no supera el mayor entre reparación y franquicia, y el
  reintegro no supera el que se cargó al cerrar (409 si se cerró sin reintegro); con el siniestro abierto no hay tope.
  Cerrar un siniestro (`PATCH /fleet/accidents/:id/close`) con importes menores que un pago o reintegro ya registrado,
  **409**.
- Una carga del chofer (`driver_cash`) no se paga acá: la rinde en su rendición (409 con el motivo). Las cargas
  `cash_payment_legacy`, anuladas o ya pagas, 409.
- Caja de efectivo sin sesión abierta o sin saldo, **409**; caja de otra distribuidora o inexistente, **404**; clase no
  admitida, **400**.
- Corrección: anular una carga y volver impaga una recepción asientan el contraasiento (también de un pago v2). Una tarea,
  un neumático o un siniestro pago no se reabre: su movimiento no se anula con `POST /cash-movements/:id/reverse` (400 con
  el motivo) y se corrige con un movimiento manual.
- En la v1, sin cambio de contrato: `PATCH /purchase-receipts/:id/payment-status` guarda la fecha del pago, y
  `PATCH /fleet/fuel-loads/:id` deja editar una carga de tarjeta ya paga.

Migraciones `1793900000000-GastosDeFlotaEnumsDeCaja`, `1793900000001-GastosDeFlotaPago` (columnas de pago en
`maintenance_task`, `tire`, `vehicle_accident`, `fuel_load` y `purchase_receipt`, con FK compuestas con la distribuidora y
CHECK de pago completo o ausente; las cuatro categorías de sistema nuevas, sembradas en todas las distribuidoras) y
`1793900000002-AuditoriaDeGastosDeFlota` (mapa de auditoría).

## Lo que se cobra por las ventas entra a su caja (API v2)

Además del efectivo (rendición del chofer, cobro del admin) y la cuenta corriente, que ya entraban a caja, ahora entran
los cobros de **Mercado Pago**, las **transferencias** y las **señas** de reservas.

**Cajas de cobro** (por distribuidora): `GET/PATCH /api/v2/cash-settings` `{ mercadoPagoCashBoxId?, transferCashBoxId? }`.
Mercado Pago entra a una caja `wallet` y las transferencias a una `bank`, de la distribuidora y activas (400 si la clase no
corresponde o está inactiva, 404 si es de otra empresa; `null` la quita). Elegir una caja no asienta nada hacia atrás.
Una caja configurada como caja de cobro no se puede desactivar (409: hay que cambiarla primero). En el panel:
Finanzas → «Cajas de cobro».

| Cobro | Cuándo | Movimiento |
| --- | --- | --- |
| Pago de Mercado Pago aprobado (también la seña de una reserva) | En la misma transacción en que el pago pasa a aprobado (webhook) | ingreso `order_payment` (método Mercado Pago) por lo que MP cobró, y egreso «Comisiones de Mercado Pago» (`mercadopago_fee`) por su comisión: el saldo de la billetera es el neto |
| Devolución propia (`RefundsService`) | Al cerrarse con éxito | egreso «Devoluciones a clientes» (`customer_refund`) desde la caja donde entró el cobro, nunca más que lo ingresado |
| Devolución desde la cuenta de Mercado Pago o contracargo | Cuando el webhook informa lo devuelto | egreso `customer_refund` por la diferencia con lo ya egresado («Contracargo» / «Devolución desde Mercado Pago») |
| Transferencia confirmada (`confirmTransfer`) | Al confirmarla | ingreso `order_payment` (método transferencia) por el saldo (total menos la seña ya paga) |
| Seña de reserva por transferencia o efectivo | Al confirmarla: `PATCH /api/v2/orders/:id/confirm-deposit { cashBoxId? }` | ingreso a la caja de transferencias, o a la caja de efectivo elegida (con su sesión) |

- **Nunca se frena un cobro:** sin caja configurada, o si la caja lo rechaza (inactiva, efectivo sin sesión abierta), el
  cobro se confirma igual y queda **«sin asentar»**, con un aviso a la bandeja (`sales_cash_unsettled`, uno por día).
- **Cobros sin asentar:** `GET /api/v2/cash-settings/pending?from=` los cuenta (cobros, señas, devoluciones sin su
  egreso) y `POST /api/v2/cash-settings/settle-pending { from }` los asienta, uno por transacción e idempotente (`from`
  hasta 365 días atrás). Para un pago viejo sin el importe cobrado guardado, consulta el pago a Mercado Pago; si no
  responde, lo asienta por el importe del pedido «(sin comisión informada)» y la comisión se asienta después, aparte. Si
  la distribuidora ya cargaba esos cobros a mano, asentar hacia atrás los duplica: el panel lo advierte.
- **Nada se cuenta dos veces:** cada asiento tiene referencia única (`UQ_cash_movement_cobro_de_venta` sobre `payment`,
  `payment_fee`, `payment_refund`, `order_transfer`), los webhooks repetidos o simultáneos toman el lock del pago y el
  efectivo sigue por su camino (rendición o cobro del admin).
- **Autor:** las devoluciones quedan a nombre de quien las pidió; lo que asienta el sistema solo (webhook, cobro tardío)
  queda sin usuario y el panel lo muestra como «Sistema» (un CHECK sólo lo permite en esos orígenes).
- `GET /api/v2/orders/:id/cash-settlement` dice, por cobro del pedido, si entró y a qué caja; `GET /api/v2/cash-movements`
  es el listado de movimientos con el pedido del que nace cada cobro (`orderId`). La v1 de movimientos no cambia.
- Si Mercado Pago reintegra la comisión en una devolución total, lo detecta la conciliación (abajo) como «Reintegro de
  Mercado Pago».

## Conciliación de la caja de Mercado Pago (API v2)

Mercado Pago no entrega un comprobante por pago, pero sí el **reporte de liberaciones** de la cuenta: cada movimiento con
su bruto, comisión, impuestos, neto y los retiros. Con ese reporte se concilia la caja «Mercado Pago» contra la realidad,
y el CSV queda guardado como comprobante de los egresos de Mercado Pago. En el panel: Finanzas → «Conciliación MP».

| Endpoint (`/api/v2/mercadopago/reconciliations`) | Qué hace |
| --- | --- |
| `POST` `{ from, to }` (`Idempotency-Key`) | Crea la corrida (días argentinos, hasta 31, sin futuro) y le pide el reporte a Mercado Pago. 409 si ya hay una corrida pendiente para ese rango |
| `GET`, `GET /:id` | Lista y detalle con las diferencias. Una corrida `requested` se vuelve a consultar sola (cron cada 2 minutos) y su `statusNote` dice en qué está («Mercado Pago todavía no generó el reporte…»); a las 24 h sin reporte queda `failed` con el motivo |
| `POST /:id/apply` `{ items: [{ itemId, cashBoxId? }], distributorId? }` (`Idempotency-Key`) | Asienta los ajustes elegidos, cada uno una sola vez. **Nada se asienta solo** |
| `GET /:id/report` | Enlace firmado al CSV: la distribuidora baja el filtrado a sus cobros; el super admin, el completo |

Diferencias que encuentra y qué asienta «Aplicar» (en la caja de Mercado Pago):

| Diferencia | Asienta |
| --- | --- |
| Cobro de MP que no entró a la caja | el ingreso y su comisión, con el bruto y la comisión del reporte |
| Comisión pendiente («sin comisión informada») o distinta de la asentada | egreso «Comisiones de Mercado Pago» o ingreso «Reintegros de Mercado Pago» por la diferencia; si comisión e impuestos difieren a la vez, es una sola diferencia |
| Impuestos y retenciones de un cobro | egreso «Impuestos y retenciones» (`taxes_withholdings`) |
| Devolución o contracargo sin egreso | egreso por el **bruto**, sin pasar de lo ingresado y descontando lo ya comprometido (devoluciones propias en curso); la comisión y los impuestos devueltos entran aparte como «Reintegros de Mercado Pago» |
| Retiro de la billetera a un banco (de la cuenta) | transferencia billetera → la caja de banco que elija el admin, más la comisión del retiro |
| Impuesto suelto de la cuenta | egreso «Impuestos y retenciones» (o ingreso si es una devolución del impuesto) |
| Importe distinto, ingreso que el reporte no trae, cobro desconocido, otros movimientos | informativos (el libro es de sólo agregar: se corrigen a mano) |

- **Una cuenta para todo el sistema:** las credenciales de Mercado Pago son globales. Cada corrida compara sólo con los
  pagos de su distribuidora; lo que no es de ninguna (retiros, impuestos sueltos, cobros desconocidos) lo ve y lo asienta
  sólo el super admin, **una sola vez en todo el sistema**, indicando la distribuidora (`distributorId`). El admin no ve
  ni los importes ni los conteos de la cuenta global.
- **Sin repeticiones:** cada diferencia tiene una clave estable (`row_key`, por día argentino e importes) y un índice
  único: una fila ya aplicada no se vuelve a asentar aunque otra corrida pise el rango. Varias filas de liberación del
  mismo cobro se suman antes de comparar.
- **El pedido a Mercado Pago** va con fechas sin milisegundos (`AAAA-MM-DDT03:00:00Z` es el comienzo del día argentino;
  con milisegundos Mercado Pago responde 400). El reporte de la cuenta usa `;` y las columnas `DATE`, `SOURCE_ID`,
  `DESCRIPTION`, `NET_CREDIT_AMOUNT`, `NET_DEBIT_AMOUNT`, `GROSS_AMOUNT`, `MP_FEE_AMOUNT`, `TAXES_AMOUNT`,
  `BALANCE_AMOUNT`…; las demás son opcionales. Las llamadas a Mercado Pago y a S3 se hacen fuera de la transacción.
- Variables opcionales: `MP_REPORTS_DRIVER` (`real` por omisión; `fake` sirve un CSV de ejemplo, sólo con `NODE_ENV`
  `development` o `test`) y `MP_REPORTS_FAKE_CSV`.
- Migraciones `1794200000000`–`1794200000002` (corridas, diferencias, categorías y auditoría) y
  `1794300000000-ConciliacionMpRonda2`.
