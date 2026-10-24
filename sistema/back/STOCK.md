# Stock físico

Módulo `src/stock/` (M-C parte 1; el diseño completo está en
`.orquesta/runs/2026-10-03-modulos-empresa/DISENO-MODULOS.md`, sección 4).

## Modelo

| Tabla                        | Qué es                                                                                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `warehouse`                  | Depósito de una distribuidora. Baja lógica; uno predeterminado vigente por distribuidora.                                                  |
| `stock_location`             | Una ubicación = un depósito **o** un vehículo (se crea la primera vez que recibe stock).                                                   |
| `stock_balance`              | Saldo materializado por ubicación, tipo de garrafa y condición (`full`, `empty`, `defective`). `quantity >= 0` por CHECK.                  |
| `stock_movement`             | Libro **append-only** (trigger `stock_movement_inmutable`). Se corrige con un contraasiento (`reason = reversal`, `reversed_movement_id`). |
| `stock_adjustment` + `_item` | Documento numerado (`document_sequence`) con nota obligatoria.                                                                             |
| `stock_threshold`            | Mínimo de llenas por depósito y tipo; `alerted_at` evita repetir el aviso.                                                                 |

## Reglas

- **`StockLedgerPort` (`StockLedgerService`) es el único que mueve stock.** Valida
  ubicaciones y garrafas contra la distribuidora (404), rechaza saldos negativos (400 con el
  detalle), actualiza saldos e inserta el libro, todo en la transacción de quien lo llama.
- **Orden de locks real** (lo siguen el ajuste, la transferencia, la entrega, la recepción y la anulación de compras,
  los contraasientos y el conteo inicial; el conteo es el único que además toma el depósito en EXCLUSIVO, pero recién
  después de las garrafas):
  1. `gas_cylinder` de todas las garrafas de la operación, por id ascendente: `FOR UPDATE` si el
     vendible acompaña al físico (lo toma `ajustarVendible`, el mismo lock que `reservarStock`) y
     `FOR KEY SHARE` si no (entrega, transferencia). `KEY SHARE` es lo que la clave foránea del
     libro pide igual al insertar: se toma ANTES de los saldos, no choca con otras entregas ni
     transferencias y sólo espera a quien tenga `FOR UPDATE`. Nunca se sube de un modo a otro.
  2. `warehouse` con `FOR SHARE` (frena la baja del depósito mientras se usa).
  3. `stock_balance` de las filas involucradas, `FOR UPDATE` ordenadas por (ubicación, tipo, condición).
  4. `document_sequence` (número del ajuste), al final.
     El conteo inicial también empieza por `gas_cylinder` (`FOR UPDATE`, por id) y recién después toma el depósito
     en exclusiva: tomarlo antes se cruzaba con un ajuste o una transferencia (garrafas y después depósito
     `FOR SHARE`) y daba deadlock; hay un test de integración con 12 conteos y 12 ajustes simultáneos.
     Sin el paso 1 una entrega tomaba saldos y recién al insertar el libro pedía `gas_cylinder`, al
     revés que un ajuste: deadlock. La entrega además reintenta su savepoint ante `40P01`.
- **Vendible (D4):** `gas_cylinder.stock = max(0, Σ llenas (depósitos y camiones) − Σ pedidos abiertos)`
  (`reserved`, `pending`, `accepted`, `on_the_way`). Entrar o sacar llenas mueve el vendible lo
  mismo y nunca lo deja negativo; las transferencias no lo tocan.
  **Una pérdida física se registra siempre** (merma, faltante de una rendición, ajuste, anulación de una compra,
  conteo): si el vendible no alcanza queda en 0 y el libro asienta igual (`ajustarVendible` con `recortarEnCero`;
  queda un warning en el log). El físico es la verdad; lo que las reservas pasan del físico no se oculta:
  la conciliación lo informa como `overReserved` (`max(0, reservadas − llenas)`), marca `consistent: false`, entra en el
  mail de las 03:00 y se resuelve cancelando pedidos o reponiendo stock.
  **Sin sobreventa al cancelar:** el recorte se recuerda en `gas_cylinder.reservation_deficit` (= `overReserved`, las reservas que
  el físico no cubre). Cualquier suma al vendible en modo "el físico manda" (una cancelación o expiración que restituye stock, un
  hallazgo, una recepción, una anulación) cubre PRIMERO ese déficit y sólo el resto sube el vendible. Ejemplo: llenas 20, reservadas
  15 (vendible 5), merma de 10 → vendible 0 y déficit 5; se cancelan 5 → llenas 10, reservadas 10: el vendible sigue en 0 (no 5);
  se cancelan 3 más → vendible 3. Se eligió persistir el déficit y no recalcular desde el físico y las reservas porque el
  vendible se mueve desde varios módulos (pedidos, stock) dentro de sus propias transacciones y el déficit se actualiza bajo el
  mismo lock de `gas_cylinder`, sin que `gascylinder` lea pedidos. Invariante: `vendible − déficit = llenas − reservadas`.
  `POST /stock/reconciliation/adjustments` deja el vendible exacto y reescribe el déficit con `overReserved`.
  **Editar un pedido** (`PATCH /orders/:id` con renglones) ajusta la reserva por la **diferencia neta por garrafa**
  (`GasCylinderService.reajustarReserva`, bajo el lock de cada garrafa en orden de id): pide más → reserva sólo el aumento (400 si
  el vendible no alcanza); pide menos → devuelve sólo lo que sobra, cubriendo primero el déficit; igual → no toca nada. Devolver todo y
  reservar de nuevo fallaba con una garrafa en déficit (lo devuelto cubría el déficit y la nueva reserva no encontraba vendible).
  `reservarRenglones(…, stockYaReservado = true)` sólo bloquea y lee el precio. **El ABM del catálogo nunca escribe `stock` ni
  `reservation_deficit`** (`update` y baja lógica los dejan `undefined` en el `save`): una reserva o un recorte confirmados entre la
  lectura y el guardado ya no se pisan con el valor viejo.
  **Conciliación y déficit:** `GET /stock/reconciliation` trae por garrafa `reservationDeficit` (el guardado) y `deficitDifference =
reservationDeficit − overReserved`; un desfasaje del déficit con `difference = 0` deja `consistent: false`, entra en el mail del cron y se
  corrige con `POST /stock/reconciliation/adjustments` (queda un documento sin renglón, porque la variación 0 no es válida). El ajuste se
  **rechaza con 409 mientras haya entregas sin descontar el físico** de esa garrafa ("primero reaplicá las entregas"): con el físico de más,
  el esperado sale mal y, al reaplicarlas, quedaría sobreventa. Se eligió rechazar y no descontar las pendientes del esperado porque la
  reaplicación es una acción explícita del administrador y puede dejar entregas pendientes sin saldo de dónde sacar.
  Sólo las reservas de pedidos (`reservarStock`) y la corrección de conciliación siguen siendo estrictas. La entrega no lo toca (ya se
  descontó al reservar). `GET /stock/reconciliation` y el cron de las 03:00 ART lo verifican y
  avisan; **no corrigen**.
- **Entrega (D5 y D6):** al pasar un pedido a `delivered`, `UpdateOrderStatusUseCase` llama a
  `StockDeliveryPort` por el **mismo manager** de la transacción del pedido. Sale la llena del
  camión del pedido (`order.vehicle_car_id`) si tiene saldo; si no, del depósito predeterminado;
  entra una vacía de canje 1 a 1. Nunca bloquea la entrega: sin saldo en ningún lado queda para
  la conciliación (`deliveriesWithoutMovement`) y se reaplica con
  `POST /stock/reconciliation/reapply-deliveries`. Idempotente por pedido y garrafa.
- **Entrega manual del administrador:** un `admin`/`super_admin` que pasa un pedido a `delivered` tiene que dar
  un motivo (`reason`, 10 a 500 caracteres, 400 si falta) por LAS DOS vías: `PATCH /orders/:id/status` con
  `{ status: 'delivered', reason }` y `POST /orders/:id/confirm-delivery` con `{ code, reason }` (el admin obtiene
  el código con `GET /orders/:id/delivery-code`, y por eso el QR tampoco lo exime). Queda en `order_status_history`
  (estado anterior, nuevo, quién y el motivo) y en la auditoría de datos (`GET /audit/entries?orderId=`, campo
  `manualDeliveryReason` del `Order`), en la misma transacción de la entrega y del movimiento de stock: si falla
  el asiento, se deshace todo. El cliente que confirma con el QR no manda `reason` y, si lo manda, se ignora. En
  `PATCH .../status` el largo máximo sólo se valida con `delivered`.
- **Ofertas de despacho al asignar:** cuando el admin asigna un pedido a mano (`assignDelivery`) o un chofer lo
  toma del pool (`status: accepted`), las ofertas `offered` abiertas a los demás choferes pasan a `superseded`
  (no cuenta como intento vencido ni bloquea una oferta futura) EN la transacción de la asignación, y después
  del commit cada chofer recibe `order:cancelled` por su socket. La del chofer que se queda la cierra la
  constancia `accepted`.
- **Piso de la reaplicación:** `reapply-deliveries` y la conciliación sólo miran entregas desde que se asentó el primer
  movimiento del libro (`MIN(stock_movement."createdAt")`, el momento real del asiento). **No** usan `occurred_at`, que el
  usuario puede elegir (la fecha de una recepción): con una recepción fechada antes del módulo el piso retrocedía y se
  reaplicaban pedidos anteriores al stock físico, destruyendo el saldo.
- **Conteo inicial:** una vez por depósito; registra las diferencias contra el saldo actual como
  un ajuste `initial_count`. Los depósitos existentes arrancan con la migración `StockFisico`
  (llenas = vendible + pedidos abiertos, vacías en cero).
- **Ajustes:** `count_correction`, `shrinkage`, `leak`, `damaged` (llena a defectuosa), `lost`
  y `found`. Nota obligatoria. Un ajuste no se contraasienta: se corrige con otro ajuste.
- **Catálogo:** `PATCH /gascylinder/:id/stock` ahora es un ajuste `count_correction` de llenas en
  el depósito predeterminado; si restando no alcanzan las llenas ahí, el 400 dice dónde están las
  demás (camiones u otros depósitos). Un producto nuevo con `stock` registra el físico en la MISMA
  transacción del alta (`garrafa.creada` con `emitAsync` y el `manager`; si falla, no se crea).
  Editar un producto con `stock` responde 400: el stock se cambia con un ajuste.
- **Desvío del vendible:** `GET /stock/reconciliation` ofrece `correction` por garrafa y
  `POST /stock/reconciliation/adjustments` lo aplica: ajuste numerado y auditado con motivo
  `reconciliation`, nota obligatoria, que corrige SÓLO `gas_cylinder.stock` (sin movimientos
  físicos: el físico no cambió). El cron avisa una vez por diferencia (firma en
  `stock_reconciliation_alert`).
- **Depósito de origen de una carga:** no se da de baja (`DELETE /warehouses/:id`) ni se desactiva (`PATCH {isActive:false}`)
  mientras sea el origen de una carga abierta (`loading`, `on_route` o `returned`): **409** con el número de la carga. La
  rendición le devuelve las garrafas, así que sin depósito (o inactivo) la carga quedaba trabada. Abrir una carga desde un
  depósito inactivo es **400**. La apertura toma el depósito `FOR SHARE` (después de las garrafas, es el orden global) y la
  baja o desactivación `FOR UPDATE`: una carga que se abre en paralelo se ve o espera.
- **Depósito predeterminado:** no puede estar inactivo (400 al marcarlo si está inactivo o al marcarlo junto con
  `isActive: false`; desactivarlo o sacarle la marca da 409). La entrega acredita ahí la vacía de canje y un depósito
  inactivo no recibe stock: omitiría todo el pedido.
- **Entrega con carrera de saldo:** las lecturas de la entrega son sin lock a propósito. Si entre la lectura y el libro
  otra operación vacía un saldo (`StockInsuficienteError`), o hay deadlock, la entrega reintenta (3 veces, en un savepoint
  nuevo) RELEYENDO los saldos: se descuentan las garrafas que alcanzan y se omite sólo la que no. Se eligió el reintento
  y no partir la operación garrafa por garrafa porque conserva una sola operación del libro por pedido.
- **Estados:** un depósito inactivo o un vehículo dado de baja no reciben stock pero pueden
  entregar el que les queda.
- **Crons (zona `America/Argentina/Buenos_Aires`):** stock bajo 08:00 (mail a los admins, una
  vez por bajada) y conciliación 03:00 (mail si hay diferencias o reservas por encima del físico). Corren bajo un lock
  distribuido de Redis (`cron:stock-low`, `cron:stock-reconciliation`): con varias instancias sale un solo mail.

## Endpoints

Todos `@Auth(ADMIN, SUPER_ADMIN)` con la distribuidora en contexto; lo de otra responde 404.
Las escrituras que crean movimientos con ids nuevos **exigen** `Idempotency-Key` (UUID v4) y responden **400** sin ella:
`POST /stock/transfers`, `/stock/adjustments`, `/stock/initial-counts`, `/stock/movements/batches/:batchId/reverse`,
`/stock/reconciliation/adjustments`, `PATCH /gascylinder/:id/stock` (suma o resta relativa), `POST /purchase-receipts`
y `PATCH /purchase-receipts/:id/void` (`reload` de la carga ya lo exigía); el OpenAPI la declara como header requerido
(`@IdempotencyKeyObligatoria`). `reapply-deliveries` y las acciones de la carga (`depart`, `return`, `close`, `cancel`) la aceptan
pero no la exigen: no repiten el efecto porque el estado ya cambió, pero **un reintento sin clave responde 409** (conflicto de
estado, p. ej. "La carga N° 7 está en ruta…"); con la misma clave devuelve la respuesta guardada, que es lo que conviene mandar. La clave queda atada al body (SHA-256 del JSON con
las claves ordenadas): repetirla con el mismo body devuelve la respuesta guardada; con otro body responde **422**
("Esa clave de idempotencia ya se usó con otros datos…") y no ejecuta nada. Vale para todo `@Idempotent`.
Swagger: `GET /docs-json`. Rutas: `/warehouses`, `/stock`, `/stock/summary`, `/stock/locations`,
`/stock/movements`, `/stock/transfers`, `/stock/initial-counts`, `/stock/adjustments`,
`/stock/thresholds`, `/stock/reconciliation` (+ `/adjustments`, `/reapply-deliveries`),
`/stock/movements/batches/:batchId/reverse`.

## Compras (parte 2)

Módulo `src/purchase/`. Proveedores, órdenes de compra y recepciones (remito de ingreso). Toda
entrada y salida de garrafas pasa por `StockLedgerPort`; el módulo no escribe saldos.

| Tabla                            | Qué es                                                                                                                                                                     |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `supplier`                       | Proveedor. Baja lógica; CUIT único entre los vigentes de la distribuidora (formato y dígito verificador validados). Tipo `filling_plant` (planta fraccionadora) u `other`. |
| `purchase_order` + `_item`       | Orden de compra numerada (`document_sequence`, tipo `purchase_order`). `received_quantity` por renglón, CHECK `0 <= recibido <= pedido`.                                   |
| `purchase_receipt` + `_item`     | Remito de ingreso, con o sin orden. Único `(distribuidora, proveedor, nº de documento del proveedor)`; la numeración interna usa el tipo `purchase_receipt`.               |
| `gas_cylinder.average_unit_cost` | Costo promedio ponderado de las llenas compradas.                                                                                                                          |

**Estados de la orden:** `draft -> sent -> partially_received -> received`; `cancelled` (con motivo) desde
`draft` o `sent`; `closed_short` (cerrada con faltante, con motivo) desde `partially_received`. Las
transiciones viven en `domain/purchase-rules.ts`. Sólo se edita en borrador.

- **Cancelar** una orden con recepciones confirmadas —cualquiera, incluso sólo de vacías— responde **409**;
  se anulan primero, o se cierra con faltante. Con todas anuladas se puede cancelar.
- **Cerrar con faltante** (`PATCH /purchase-orders/:id/close-short`, motivo obligatorio): lo que falta ya no
  llega. Se eligió un estado propio y no `cancelled` porque la orden SÍ recibió mercadería: cancelada
  significaría "no se compró nada" y mezclaría los dos casos en los reportes. `pendingQuantity` pasa a 0 y
  deja de bloquear la baja del proveedor. Sus recepciones se siguen pudiendo anular y la orden conserva el estado.
- Anular una recepción de una orden `sent`/`partially_received`/`received` recalcula su estado (puede volver a
  `partially_received` o `sent`); en una `cancelled` o `closed_short` el estado no cambia.

**Recepción (`POST /purchase-receipts`), una transacción:**

1. lock de la orden (`FOR UPDATE`) y validación: sólo `sent` o `partially_received`, garrafas de la orden,
   cada renglón <= lo pendiente (400 con el detalle);
2. ledger: `+llenas` (`purchase_receipt`) en el depósito destino, que sube el vendible (D4), y `-vacías`
   (`plant_empty_out`) que se lleva la planta. Si las vacías no alcanzan: 400 con el detalle y no se escribe nada;
3. costo promedio: `(existencia previa x costo previo + llenas x costo nuevo) / (existencia previa + llenas)`,
   redondeado a 2 decimales; la existencia son las llenas de depósitos y camiones antes de la recepción. En
   cada renglón se guardan `previous_average_cost` y `previous_on_hand` (el promedio y la existencia de antes);
4. `received_quantity` y estado de la orden; 5. número interno y remito.
   Documento del proveedor: único por `(distribuidora, proveedor, tipo, número)`: remito y factura numeran aparte.
   Límites de los DTO (`dto/purchase-limits.ts`): 20 renglones, 5.000 unidades y $90.000 por garrafa, para que
   ningún total desborde `numeric(12,2)`; `traducirErrorDeBase` además traduce `22003` a 400 y, en compras, `22001` (texto más largo
   que la columna) también es 400.
   **Fecha de la recepción:** `receivedAt` no puede ser futura ni anterior al **conteo inicial** del depósito, si lo tuvo (400: esas
   garrafas ya están en el conteo). Sin conteo inicial no hay piso: se acepta una fecha pasada, porque el piso de la reaplicación de
   entregas ya no depende de `occurred_at`.

**Anular (`PATCH /purchase-receipts/:id/void`):** contraasiento del lote por el ledger (las llenas salen del
depósito, las vacías vuelven). Si las llenas ya no están en el depósito (vendidas, cargadas a un camión,
transferidas) responde **409** y dice dónde están hoy. No se anula una recepción marcada como pagada (400).
Si el depósito donde entró la recepción fue dado de baja tampoco se anula: **409** (el contraasiento devuelve las garrafas a la ubicación original y un depósito dado de baja no recibe ni entrega nada). Un depósito inactivo, que no recibe stock, da **400** si el contraasiento tiene que devolverle vacías.

**Costo promedio al anular** (`recalcularCostoPromedio`, exacto y determinístico). Las ventas, mermas y ajustes NO cambian el
promedio (sólo una compra lo cambia), así que al anular se **repiten, en orden de número, las recepciones de llenas que siguen
confirmadas** con la misma fórmula de la recepción y se fija el resultado:

1. parte del promedio que había antes de la primera recepción de esa garrafa (`previous_average_cost` guardado);
2. de cada recepción vigente usa su `previous_on_hand` (existencia previa que se guardó, ya con las ventas del medio) y le
   resta las llenas de las recepciones anteriores que se anularon **después** de que ésta leyó esa existencia (si se anularon
   antes, la existencia guardada ya no las incluía); piso 0. El instante de la lectura es `previous_on_hand_at`
   (`clock_timestamp()` de la base, bajo el lock de la garrafa); `createdAt` no sirve porque es el inicio de la transacción y una
   anulación puede cruzarse en el medio. Una recepción anterior a esa columna usa su `createdAt`;
3. sin ninguna recepción vigente vuelve al promedio de partida (`null` si nunca hubo costo);
4. si alguna recepción necesaria es anterior a las columnas `previous_*` no se puede reconstruir: el promedio queda como está.
   El resultado no depende del orden en que se anulen varias: R1 $100, R2 $300 y R3 $100 (10 c/u, 25 llenas sin costo antes) dejan
   136,36; anular R2 deja 100 (antes 91,92), anular R3 deja 144,44, anular las dos deja 100. La fecha de anulación (`voided_at`)
   sale del reloj de la base. El texto de `stock_movement.notes` (varchar 300) se arma con el motivo y se corta con `…` si
   no entra; el motivo completo queda entero en `purchase_receipt.void_reason`.

**Pago:** `PATCH /purchase-receipts/:id/payment-status` con `paymentStatus` `unpaid`/`paid`. Pagada **en efectivo**
(`paidInCash: true`) el total sale de una caja de efectivo en la misma transacción: `cashBoxId` es obligatorio si la
distribuidora tiene alguna caja de efectivo activa (400), tiene que ser de efectivo (400), de la distribuidora (404) y con
sesión abierta si la exige (409; la recepción no cambia). El asiento usa la categoría de sistema `purchase`, el origen
`purchase_receipt` y la recepción como referencia; `cash_movement_id` guarda la salida (sin clave foránea). Marcarla
`unpaid` asienta el contraasiento y deja `cash_movement_id` en `null`; repetir el estado actual es un no-op (no asienta
dos veces). Pagada sin `paidInCash` es sólo la marca. Una recepción que ya figura pagada sin salida de caja y recibe `paidInCash` responde 409 (se marca impaga y se vuelve a pagar). Sin cajas de efectivo activas, el pago en efectivo es sólo la marca.
Una recepción pagada no se anula: se marca impaga (devuelve el efectivo a la caja) y después se anula. El movimiento de
caja no se anula a mano (`POST /cash-movements/:id/reverse` responde 400 y dice cómo corregirlo). Ver `FINANZAS.md`.

**Orden de locks de compras** (se suma al de arriba, empezando antes):
`purchase_order` -> `purchase_receipt` -> `gas_cylinder` (los toma el ledger) -> `warehouse` -> `stock_balance` ->
`document_sequence` (el número del remito y de la orden, al final). Anular toma la orden y después el remito.
Nada toma `gas_cylinder` y luego `purchase_order`. Crear/editar una orden toma las garrafas con `FOR KEY SHARE`
(lo que pide la clave foránea del renglón) antes de la secuencia, y el proveedor con `FOR SHARE` (frena su baja).
Dos recepciones simultáneas de la misma orden se serializan en el lock de la orden: la segunda ve lo recibido por
la primera.

**Endpoints** (`@Auth(ADMIN, SUPER_ADMIN)`, distribuidora en contexto, lo de otra responde 404; los `POST`/`void`
que mueven stock o numeran aceptan `Idempotency-Key`):

| Método             | Ruta                                                                                            |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| GET, POST          | `/suppliers`                                                                                    |
| GET, PATCH, DELETE | `/suppliers/:id`                                                                                |
| GET                | `/suppliers/:id/purchase-history`                                                               |
| GET, POST          | `/purchase-orders` (`status`, `supplierId`, `from`, `to`)                                       |
| GET, PATCH         | `/purchase-orders/:id`                                                                          |
| GET                | `/purchase-orders/:id/pending`                                                                  |
| PATCH              | `/purchase-orders/:id/send`, `/purchase-orders/:id/cancel`, `/purchase-orders/:id/close-short`  |
| GET, POST          | `/purchase-receipts` (`supplierId`, `purchaseOrderId`, `paymentStatus`, `status`, `from`, `to`) |
| GET                | `/purchase-receipts/average-costs`, `/purchase-receipts/:id`                                    |
| PATCH              | `/purchase-receipts/:id/void`, `/purchase-receipts/:id/payment-status`                          |
| GET, POST          | `/attachments/purchase_receipt/:receiptId` (foto o PDF del remito del proveedor; ver abajo)     |

**Foto del remito.** El dueño `purchase_receipt` del módulo de adjuntos (`PurchaseReceiptAttachmentOwnerResolver`)
cuelga de la recepción: subida multipart por el back con token (`POST /attachments/purchase_receipt/:receiptId`,
campo `file` y `label` opcional), JPG/PNG/WEBP/PDF de hasta 10 MB validados por tipo y contenido, cifrado SSE
AES256 en S3 y lectura sólo por URL firmada (`GET /attachments/:id/download?modo=url`). Una recepción de otra
distribuidora responde 404 (en alta, listado y descarga) y el chofer no accede (403). Las recepciones anuladas
conservan su foto. Reglas generales en `S3.md`.

## Carga y rendición del camión (parte 3)

Módulo `src/truck-load/`. La jornada de un camión: se abre la carga, se carga, sale, se repone en
ruta, se entrega, vuelve y se rinde. Toda salida y entrada de garrafas pasa por `StockLedgerPort`; el
módulo guarda el documento y las reglas (`domain/truck-load-rules.ts`).

| Tabla             | Qué es                                                                                                                                                                                                                                                                                                                                 |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `truck_load`      | Hoja de carga: camión, chofer, ayudante (legajo, opcional), depósito de origen, día de negocio (hora argentina), número (`document_sequence`, tipo `truck_load`) y estado. Únicos parciales `(car_id)` y `(delivery_id)` `WHERE status IN ('loading','on_route','returned')`: un camión y un chofer tienen **una sola** carga abierta. |
| `truck_load_item` | Un renglón por tipo de garrafa: cargadas (`loaded_full`, `loaded_empty`), repuestas (`reloaded_full`), lo declarado al volver y, al cerrar, lo congelado (entregado, recolectado, esperado y diferencia).                                                                                                                              |

**Estados:** `loading -> on_route -> returned -> closed | closed_with_difference`; `cancelled` sólo desde
`loading`. Pedir una acción que el estado no permite es **409** (conflicto de estado), igual que en compras; los 400 quedan
para datos inválidos. Se puede volver a declarar la vuelta (`returned -> returned`) hasta cerrar.

**Qué mueve el ledger y cuándo:**

| Acción                       | Movimientos                                                                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Abrir (`POST /truck-loads`)  | Ninguno: guarda renglones y numera. Exige que el camión esté en uso por el chofer (`vehicle_assignment` abierta).                                                                    |
| Salir (`PATCH .../depart`)   | `truck_load`: depósito de origen -> camión, llenas y vacías (para canje). Si no alcanza el depósito, 400 y no sale nada.                                                             |
| Reponer (`PATCH .../reload`) | `truck_load`: más llenas del depósito al camión, sobre la misma carga y sólo en ruta.                                                                                                |
| Entregar                     | Ya existe (parte 1): sale la llena del camión del pedido y entra la vacía de canje 1 a 1.                                                                                            |
| Rendir (`PATCH .../close`)   | `truck_return`: lo declarado vuelve camión -> depósito. La diferencia, en la misma operación: faltante = `shrinkage` (baja el vendible), sobrante = `adjustment` (sube el vendible). |
| Defectuosas del camión       | Vuelven al depósito tal cual (`truck_return`, condición `defective`) sin declaración ni diferencia: el camión queda en cero en TODAS las condiciones.                                |
| Cancelar                     | Ninguno: en `loading` todavía no se movió nada; sólo libera camión y chofer.                                                                                                         |

**Rendición (D6).** Por tipo de garrafa, `esperado llenas = cargadas + repuestas - entregadas` y `esperado
vacías = cargadas + recolectadas`. Lo entregado y recolectado se leen del libro: los movimientos
`delivery` y `empty_collected` del camión desde que se abrió la carga, netos de contraasientos. La
diferencia es `declarado - esperado`; el detalle la muestra en vivo apenas el chofer declara y al cerrar queda
congelada. **Invariante: al cerrar, el saldo del camión queda en cero.** Los ajustes se calculan contra el
saldo real del camión bajo lock (coincide con el esperado salvo que alguien lo haya movido a mano), y
cualquier ajuste del libro cuenta como diferencia. Con diferencia, `differenceNote` es obligatoria (400
sin ella, antes de tocar el ledger) y la carga queda `closed_with_difference`. Lo que el camión tenga y la carga
no liste (una transferencia manual) se rinde con un renglón propio declarado en cero.

**Efectivo de la jornada (informativo).** El detalle trae `cash`: de los pedidos que el chofer entregó con ese
camión durante la carga, el efectivo cobrado (`paid`, confirmado por el chofer), el impago (`unpaid` y
`written_off`) y el pendiente de confirmar. No mueve nada: la caja (M-D) no existe.
**Los importes en efectivo son el saldo que el chofer cobra al entregar**, no el total: `remainingBalance = total − seña`
(la seña sólo si `deposit_paid`), la misma regla que `OrderMapper`. Una reserva de $20.000 con $5.000 de seña paga por
adelantado suma $15.000 a `cashCollectedAmount`, `unpaidAmount` o `pendingConfirmationAmount` según su estado de pago. Cada
pedido de `orders` trae `totalAmount` y `remainingBalance`. `nonCashAmount` sigue sumando el total de lo cobrado por otro medio.
El cierre de la carga (`PATCH …/close`) no calcula efectivo: sólo rinde stock, así que no hay otro cálculo que corregir.
Nota: `CashCollectionUseCase.confirmReceived` (módulo `order`) pasa el pedido a `paid` pero no registra el monto cobrado; la
rendición lo deduce del pedido. Si algún día el chofer cobra un monto distinto del saldo, hay que guardarlo ahí.

**Orden de locks de la carga** (se suma al de arriba): `car` (`FOR SHARE`, frena a `ponerEnUso`) -> `delivery` ->
`gas_cylinder` (`FOR KEY SHARE`, por id) -> `document_sequence`, al abrir. Para operar una carga abierta, el
**primer** lock es la fila de `truck_load` y después va el del ledger. La rendición toma ella misma, en el
orden del ledger, `gas_cylinder FOR UPDATE` (puede mover el vendible; no se sube de modo después) ->
depósito `FOR SHARE` -> saldos del depósito y del camión `FOR UPDATE` ordenados, ANTES de leer lo entregado:
una entrega en curso se ve completa y una posterior ya no encuentra stock en el camión y sale del depósito.
Una entrega que se asienta entre la declaración del chofer y el cierre aparece como diferencia en la
rendición (el cierre recalcula bajo lock).

**Vista previa del cierre.** `GET /truck-loads/:id` devuelve `hayDiferencia`: para una carga abierta
(`loading`, `on_route`, `returned`) con la vuelta declarada en TODOS los renglones, es lo que daría el cierre
(`true` si la rendición necesitaría la nota de diferencia). Usa el mismo cálculo que `PATCH .../close`
(`renglonesDeCierre` + `planDeCierre`, en `domain/truck-load-rules.ts`) sobre los saldos y entregas del
momento: cuenta también un camión con garrafas que la carga no lista o con una cifra distinta de la
declarada, no sólo declarado - esperado. Por renglón siguen `expectedFull/Empty`, `declaredReturnFull/Empty`
y `differenceFull/Empty`. Es `null` mientras falte declarar y en cargas cerradas o canceladas (ahí valen el
estado y las diferencias congeladas).

`requiereVolverADeclarar` (boolean, siempre presente): `true` si el camión entregó garrafas DESPUÉS de
`returnedAt`; es el mismo criterio con que `PATCH .../close` responde 409 ("Se entregaron N garrafas... volver a
declarar", `entregasTardias` en `truck-load-rules.ts`). En ese caso `hayDiferencia` es `null` hasta que el chofer
declare de nuevo. En cualquier otro caso es `false`.

**Quién recibe y acepta pedidos** (`motivoSinPedidos`, puerto `TruckLoadGatePort`; se aplica a las ofertas del despacho
automático, a la aceptación del chofer o del administrador con `deliveryId`, a la asignación manual
`PATCH /orders/:id/assign/:deliveryId` y al pool `GET /orders/available`):

- **con carga abierta, sólo en ruta** (`on_route`), con o sin D5: en `loading` todavía no salió el stock y en `returned` ya
  declaró la vuelta, así que lo que entregara después sería stock fantasma en la rendición. Además su vehículo en uso tiene que ser el
  camión de la carga;
- **sin carga**: recibe y acepta como siempre, salvo que la distribuidora active D5. `stock_control.requireOpenTruckLoad`
  (por distribuidora, `module_config`, proceso `stock_control`; por defecto `false`) exige tenerla; se lee y cambia con
  `GET|PUT /truck-loads/settings`.
  Aceptar o asignar sin poder responde 400 con el motivo ("Tu distribuidora exige una carga de camión abierta...", "El chofer no tiene la
  carga del día abierta", "La carga N° n todavía no salió...", "...ya volvió..."). `GET /orders/available` devuelve la lista vacía con
  `openLoadRequired: true` y `message` (por ejemplo "Abrí tu carga para recibir pedidos"); la app también lo sabe por
  `GET /truck-loads/mine` (`requireOpenTruckLoad`, y la carga con su estado). Repetir una aceptación que ya era del chofer no se vuelve a controlar.

**Reglas de la jornada**

- **El stock del camión sólo entra y sale por la carga.** `POST /stock/transfers` rechaza (400) transferir a un vehículo: "El camión se
  carga y se rinde desde la carga del día". La única excepción es **regularizar**: devolver al depósito lo que un vehículo tiene suelto,
  con transferencia vehículo -> depósito, sólo si el camión no tiene carga abierta (409 si la tiene) y con nota obligatoria.
  El **contraasiento** de esa regularización devolvería las garrafas al camión (y el de una transferencia desde un camión con
  carga abierta las sacaría): **409**, con las mismas reglas que la transferencia. Se contraasientan las transferencias entre depósitos y, por los datos históricos, una depósito -> camión
  (el contraasiento vuelve del camión al depósito: sólo si el camión no tiene carga abierta). Nunca hacia un camión. Se eligió
  esa vía y no un endpoint aparte porque deja el mismo rastro (lote, libro, auditoría, idempotencia). Un camión sale vacío: `depart` responde
  400 si todavía tiene garrafas.
- **No se declara la vuelta con pedidos en curso:** `return` responde 409 si el chofer tiene pedidos `accepted` u `on_the_way`
  ("Tenés N pedidos en curso: entregalos o liberalos antes de volver").
- **Entrega después de declarar:** si el libro tiene entregas del camión posteriores a `returned_at`, `close` responde 409 y el
  chofer vuelve a declarar. Se eligió rechazar y no recalcular porque recalcular daría por buena una cuenta que el chofer no hizo.
- **Cambio de vehículo:** `PUT|DELETE /delivery/:id/vehicle` responde 409 mientras el chofer, o el camión, tengan una carga abierta.
- **Reposición:** `reload` exige `Idempotency-Key` (400 sin ella): repetirla suma otra vez. `depart`, `return`, `close` y `cancel` no
  repiten el efecto (el estado ya cambió), pero un reintento sin clave es 409; con la misma `Idempotency-Key` devuelve lo guardado.
- **Reloj:** un solo reloj, el de la base (`clock_timestamp()`), para todo lo que se compara en la ventana de la carga:
  `opened_at`, `departed_at`, `returned_at`, `closed_at` y el `occurred_at` de los movimientos del libro (que no traen fecha
  propia). Delimitan qué entregas son de la carga. Sólo la recepción de compras puede llevar una fecha elegida por el usuario.
  **Pendiente:** `order.deliveredAt` se sigue grabando con el reloj del proceso (`new Date()`, módulo `order`); la ventana de la carga
  compara contra el reloj de la base, así que un servidor desfasado podría dejar una entrega adentro o afuera. Lo arregla quien
  tenga `src/order`; hasta que se integre queda pendiente.
- **Reposición y tipos:** declarar la vuelta lista todos los tipos de la carga y el DTO admite 20: una reposición que haría
  pasar la carga de 20 tipos distintos es 400.
- **Baja del chofer o egreso del legajo con una carga abierta:** 409 y la baja se revierte (cerrá o cancelá la carga antes). Liberar
  el vehículo dejaría el stock cargado en un camión que nadie usa; la rendición la puede declarar y cerrar el administrador.
- **Mismo criterio para stock y efectivo:** lo entregado en stock es lo que salió del camión de la carga en `[opened_at, ahora o cierre]`; el
  efectivo (`cash`) y la lista `orders` son los pedidos entregados por el chofer de la carga CON ese camión (`order.vehicle_car_id`) en la
  misma ventana. "Cobrado" es `paid` (cualquier medio); `unpaid` y `written_off` son impago; el efectivo `pending` está sin confirmar. Un pedido
  entregado con otro vehículo no cuenta en ninguno de los dos.

**Endpoints** (`@Auth(ADMIN, SUPER_ADMIN)` salvo indicación; un chofer sólo ve y toca las cargas suyas, lo ajeno
es 404; los `POST`/`PATCH` que mueven stock aceptan `Idempotency-Key`):

| Método   | Ruta                                                                                                                                             |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| POST     | `/truck-loads` (abre y numera)                                                                                                                   |
| GET      | `/truck-loads` (`status`, `date`, `from`, `to`, `carId`, `deliveryId`, `page`, `limit`)                                                          |
| GET      | `/truck-loads/mine` (`DELIVERY`: su carga abierta y `requireOpenTruckLoad`)                                                                      |
| GET, PUT | `/truck-loads/settings`                                                                                                                          |
| GET      | `/truck-loads/cars/:carId/stock` (stock actual del camión)                                                                                       |
| GET      | `/truck-loads/:id` (admin o el chofer de la carga: renglones, esperado, diferencias, `hayDiferencia`, pedidos, `cash` y movimientos)             |
| PUT      | `/truck-loads/:id/items` (sólo en `loading`)                                                                                                     |
| PATCH    | `/truck-loads/:id/depart` (admin o el chofer de la carga), `/reload` (con `Idempotency-Key`), `/return` (admin o el chofer), `/close`, `/cancel` |

## Pendiente

La diferencia de una rendición a cargo del chofer se descuenta por el libro de comisiones (`FINANZAS.md`). El pago
en efectivo de una recepción ya sale de una caja (arriba).
