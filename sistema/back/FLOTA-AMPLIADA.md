# Flota ampliada (C-18)

Combustible, habilitación de mercancías peligrosas, multas, siniestros, neumáticos, costo por
vehículo y reactivación: CU-195 a CU-206, CU-247 y CU-320 a CU-328. Módulo `fleet-expense/`
(registra lo que cuesta mantener la flota); se apoya en `fleet/` (mantenimiento y habilitaciones)
y `car/` (vehículos). Todo está también en Swagger (`/docs`, tags "Fleet · Combustible",
"Fleet · Multas", "Fleet · Siniestros", "Fleet · Neumáticos", "Fleet · Costos" y "Fleet · Vehicle status").

## Acceso y aislamiento

Rol `admin` o `super_admin` salvo `POST /fleet/fuel-loads/mine` y `POST /fleet/accidents/mine`,
que son de `delivery`. Toda ruta exige distribuidora (el admin, la suya; el super admin,
`X-Distributor`, y sin él **400**). Lo de otra distribuidora responde **404**. Los `POST`
aceptan `Idempotency-Key`. Los listados devuelven `{ data, total }` y se paginan con `limit` y
`offset`. Las fechas de filtro son `YYYY-MM-DD` en hora argentina, con `to` inclusivo; un valor
inválido o `from` posterior a `to` es **400**.

## Vehículo (CU-034 y CU-111 reciben estos datos)

| Campo (`/car`)         | Regla                                                              |
| ---------------------- | ------------------------------------------------------------------ |
| `fuel_type`            | `diesel`, `gasoline`, `cng` o `lpg`; es el de las cargas que no indican otro. `null` lo borra |
| `tank_capacity_liters` | de 1 a 9999 con hasta 2 decimales; una carga no la supera en más de un 5 %. `null` la borra   |

La respuesta de `/car` suma `fuel_type`, `tank_capacity_liters`, `odometer_km` y `fleet_status`
(`active`, `in_service`, `grounded` = fuera de servicio).

**Kilometraje del vehículo.** Se escribe desde un único punto (`CarService.actualizarOdometro`,
`GREATEST` entre el vigente y el nuevo): lo comparten las cargas de combustible y el cierre de las
tareas de mantenimiento (`PATCH /fleet/tasks/:id/close` con `odometerKm`), y ninguno pisa al otro.
Sólo baja (`bajarOdometro`) cuando el valor vigente lo había puesto la carga que se anula o se
corrige hacia abajo, y vuelve al **mayor kilometraje entre las cargas vigentes y las tareas de
mantenimiento hechas con `odometerKm`** (las dos fuentes que lo escriben). Si no queda ninguna de
las dos, el vehículo conserva el kilometraje que tenía. El kilometraje de una carga, de un cierre
de tarea y de un movimiento de neumático no pasa de 2.000.000 km (**400**).

## Combustible (CU-195, CU-320, CU-321, CU-322, CU-196)

| Método y ruta                                  | Qué hace                                                       |
| ---------------------------------------------- | -------------------------------------------------------------- |
| `POST /fleet/fuel-loads`                       | Registra (administrador). 201                                  |
| `POST /fleet/fuel-loads/mine`                  | Registra el chofer, siempre en su vehículo en uso. 201         |
| `GET /fleet/fuel-loads?carId&employeeId&from&to&anomaly` | Vigentes, con `total`, `totalLiters` y `totalAmount` de lo filtrado |
| `GET /api/v2/fleet/fuel-loads/quote?liters&unitPrice` | Calcula el importe de una carga: `{ liters, unitPrice, totalAmount }`, litros × precio a 2 decimales (administrador). **400** con litros o precio no positivos o con más decimales de los permitidos |
| `GET /fleet/fuel-loads/:id`                    | Una carga, también la anulada (`voidedAt`)                     |
| `PATCH /fleet/fuel-loads/:id`                  | Modifica y revalida                                            |
| `DELETE /fleet/fuel-loads/:id`                 | Anula (baja lógica); si salió de una caja asienta el contraasiento |
| `PATCH /fleet/fuel-loads/:id/cash-payment`     | Asienta en una caja la carga `cash_box` que registró el chofer (`cashBoxId`) |
| `GET /cars/:carId/fuel-efficiency?from&to`     | Tramos, totales y cargas anómalas                              |

El panel no hace la cuenta: pide el importe a `quote` y lo ofrece como importe de la carga. Es la misma
cuenta (`importeEsperado`) con la que el alta valida `totalAmount`.

Reglas al registrar y al modificar:

1. `totalAmount` coincide con `liters × unitPrice` con una tolerancia del 1 % (**400**, campo `totalAmount`).
2. `liters` no supera en más de un 5 % la capacidad del tanque, si está cargada (**400**, campo `liters`).
3. El kilometraje no es menor que el de la última carga vigente anterior (por fecha). **400**
   «El kilometraje es menor que el de la última carga». Sólo el administrador lo fuerza con
   `odometerCorrection: true` y `odometerCorrectionNote` (sin nota, **400**). El chofer no puede.
4. Sin `fuelType` en la carga ni en el vehículo, **400**. `loadedAt` futura, **400**.
5. El consumo se mide por el método del tanque lleno: entre dos cargas llenas, km sobre litros
   cargados después de la primera. Una carga que cierra un tramo se marca `anomaly` si su km/L se
   aparta más de un 25 % del promedio de los cinco tramos anteriores (por kilometraje); avisa por
   correo a los administradores. Modificar una carga recalcula sólo la suya.
6. `employeeId` es el legajo de quien cargó: el del chofer en `/mine`; en el alta del administrador,
   el del chofer que tenía el vehículo en uso en `loadedAt` (o `null`).
7. Anulada o modificada: **409** «La carga de combustible está anulada» si ya estaba anulada.

`/mine` sin vehículo en uso: **404** «No tenés un vehículo en uso».

`GET /cars/:carId/fuel-efficiency`: con menos de dos cargas llenas en el rango, `tranches` vacío,
`km`, `liters` y `amount` en 0 y `kmPerLiter`/`costPerKm` en `null` (no es un error).

## Habilitación para transportar mercancías peligrosas (CU-197)

Es una tarea del plan «Habilitación para transporte de mercancías peligrosas» (`documentKind:
hazmat_vehicle_permit`; de vehículo, fecha fija, 30 días, bloqueante), sembrado con cada
distribuidora y agregado por la migración a las existentes. Se registra con la misma operación
que el seguro y la VTV: `POST /fleet/tasks` con `planId`, `carId`, `referenceNumber` (número),
`provider` (autoridad), `validFrom` (inicio) y `dueAt` (vencimiento).

- Sin `dueAt` en este plan, **400** (`dueAt`). En cualquier plan, `validFrom` posterior a `dueAt`, **400** (`validFrom`).
- Vencida, el vehículo queda inhabilitado: aparece así en `GET /cars/:id/documents`, el despacho
  lo excluye y `PUT /delivery/:id/vehicle` lo rechaza (**400**, con el nombre del documento).
- Entra sola en el aviso diario de vencimientos (CU-142).

Cambios compartidos de `fleet`: las tareas ganan `validFrom` y se pueden crear y modificar con
`cost` (la prima de la póliza); los planes ganan `documentKind` (`insurance`, `vtv`,
`hazmat_vehicle_permit` o `null`), que la migración completa por nombre para seguro y VTV.

## Multas (CU-198, CU-199, CU-200, CU-323, CU-324, CU-325, CU-326)

| Método y ruta                                    | Qué hace                                                |
| ------------------------------------------------ | ------------------------------------------------------- |
| `POST /fleet/fines`                              | Registra; nace `pending`. 201                           |
| `GET /fleet/fines?carId&employeeId&status&from&to` | Lista (por fecha de la infracción), con `total`       |
| `GET /fleet/fines/:id`                           | Una multa                                               |
| `PATCH /fleet/fines/:id`                         | Modifica; `appeal: true` la pasa a `appealed`           |
| `PATCH /fleet/fines/:id/pay`                     | `paidAt` (no futura) y `paidAmount` > 0 → `paid`; con `paidInCash` y `cashBoxId` sale de una caja de efectivo. La v2 paga con comprobante y desde cualquier caja (abajo) |
| `PATCH /fleet/fines/:id/charge-to-employee`      | Imputa al chofer (`chargedToEmployee`)                  |
| `PATCH /fleet/fines/:id/void`                    | `reason` obligatorio → `voided`                         |

Ciclo: `pending` → `appealed` → `paid` o `voided`; pagada y anulada no vuelven atrás.

- Alta: acta única por distribuidora y jurisdicción (**409** «La multa ya está registrada», también al
  modificar); `amount` > 0; `voluntaryPaymentAmount` no supera `amount` (**400**). El responsable se
  deduce del chofer que tenía el vehículo en uso en `occurredAt`; se puede indicar `employeeId`
  (un legajo de otra distribuidora, **404**). Si ese chofer ya no tiene legajo vigente queda en `null`.
- Modificar o anular una pagada/anulada, **409**. Pagar una pagada/anulada, **409** «La multa no admite el pago».
- Imputar: una pagada también se imputa; una anulada no (**409** «La multa anulada no se puede imputar»).
  Sin responsable deducido y sin `employeeId`, **400**. Es sólo una marca: el descuento en la
  liquidación llegará con el módulo de caja.
- Dos pagos simultáneos: uno gana, el otro **409** (la transición toma el lock de la fila).
- La copia del acta va con los adjuntos genéricos: `/attachments/traffic_fine/:id`.

### Pago por enlace con comprobante (API v2)

La distribuidora paga la multa afuera (portal del municipio, Mercado Pago o Pago Fácil) y registra el pago con el
comprobante, igual que la cuota del seguro (`SEGUROS.md`). El pago es un **egreso de Caja** desde efectivo, banco o
billetera.

| Método y ruta (`/api/v2`)                    | Qué hace                                                                |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| `POST /traffic-fines`, `PATCH /traffic-fines/:id` | Alta y edición con, además, `paymentUrl` (https) y `paymentCode`   |
| `GET /traffic-fines`, `GET /traffic-fines/:id` | Lo mismo que la v1 más `paymentUrl`, `paymentCode`, `operationNumber` y `receiptAttachmentId` |
| `POST /traffic-fines/:id/receipt`            | Sube el comprobante (multipart `file`: PDF, JPG, PNG o WEBP, 10 MB) y lo escanea en el mismo pedido → `{ attachmentId, scan: { available, data } }` |
| `POST /traffic-fines/:id/pay`                | `{ attachmentId, paidAt, amount, operationNumber?, cashBoxId }` con `Idempotency-Key` → la multa paga y el egreso |

- **Comprobante:** es un adjunto de dueño propio (`traffic_fine_payment`), distinto de la copia del acta
  (`traffic_fine`). Sólo se sube por `/receipt` y no se puede subir ni borrar por `/attachments`. El pago acepta sólo
  un comprobante de **esa** multa: con la copia del acta, otro adjunto o uno de otra multa, **400**.
- **Escaneo:** con el lector de comprobantes (`ReceiptReaderPort`); el importe esperado es el del pago voluntario si
  todavía vale (sin vencimiento o no vencido) y si no el total. Un escaneo que falla no corta la subida
  (`available: false`, los datos se cargan a mano).
- **Pago:** en una transacción con el lock de la multa. Sólo `pending` o `appealed` (pagada o anulada, **409**).
  `amount` no supera el importe de la multa; `paidAt` no puede ser futuro (**400**). La caja es obligatoria: efectivo
  (con su sesión abierta y saldo), banco o billetera. El egreso va con la categoría «Multas» (`traffic_fine`) y la
  descripción «Multa <acta> — <jurisdicción> (<patente>)». Otra distribuidora, **404**. La misma `Idempotency-Key`
  no paga dos veces.
- Las multas pagadas por la v1 (`PATCH /fleet/fines/:id/pay`) siguen siendo válidas sin comprobante.

**Aviso de vencimiento (CU-326).** A la hora del aviso de flota de cada distribuidora, `FineDueAlertsCron` avisa por
la **bandeja del admin, con mail** (`BANDEJA-ADMIN.md`): `traffic_fine_due` cuando una multa `pending` vence en 5 días
o menos (con el importe del pago voluntario si todavía vale) y `traffic_fine_overdue` cuando ya venció sin pagar
(hasta 30 días después de vencida). Cada aviso sale una vez por multa y vencimiento: si se corrige la fecha, se
vuelve a avisar. Las multas que ya había avisado el correo anterior (`alertedAt`) no se repiten. Una `appealed` no se
avisa: está en discusión; si la apelación se rechaza, se corrige el vencimiento y vuelve a entrar. El aviso abre la
multa en el panel (`/fleet/fines?fine=<id>`), con **Pagar** (el enlace) y **Registrar pago**.

## Siniestros (CU-201, CU-202, CU-327, CU-328)

| Método y ruta                                  | Qué hace                                                    |
| ---------------------------------------------- | ----------------------------------------------------------- |
| `POST /fleet/accidents`                        | Registra (administrador); nace `reported`. 201              |
| `POST /fleet/accidents/mine`                   | Registra el chofer, en su vehículo en uso. 201              |
| `GET /fleet/accidents?carId&status&from&to`    | Lista (por fecha del hecho), con `total`                    |
| `GET /fleet/accidents/:id`                     | Uno                                                         |
| `PATCH /fleet/accidents/:id`                   | Corrige y avanza el ciclo                                   |
| `PATCH /fleet/accidents/:id/close`             | `repairCost`, `insurerReimbursement`, `deductibleAmount` ≥ 0 → `closed` |

- `location` es `"latitud,longitud"` (punto PostGIS); inválido, **400**. `occurredAt` no puede ser futuro.
- `vehicleUnusable: true`: el siniestro **se registra siempre** y el vehículo pasa a `grounded` (no se
  puede volver a poner en uso ni asignar; el despacho no le ofrece pedidos a su chofer). En la misma
  transacción, tomando el lock de la fila del chofer, se cierra la asignación abierta **salvo que el
  chofer tenga un pedido en curso o una carga de camión abierta**: entonces la asignación se mantiene,
  la respuesta del alta trae `assignmentKept: true` y `assignmentKeptReason` (sólo en el alta) y se
  avisa por correo a los administradores para que resuelvan el pedido o la carga y liberen el vehículo.
  Sin pedido en curso ni carga abierta, se libera y `assignmentKept` es `false`.
- `hazmatRelease: true`: aviso inmediato por correo a los administradores, siempre. Al modificar,
  pasar `hazmatRelease` de `false` a `true` emite el mismo aviso; un derrame ya informado no se puede
  retirar (**400**).
- Ciclo: `reported` → `under_review` → `repairing`, de a un paso (**409** si saltea o retrocede). El
  cierre es sólo `PATCH …/close`. Un siniestro cerrado no se modifica ni se vuelve a cerrar
  (**409** «El siniestro ya está cerrado»). `vehicleUnusable`, `carId` y el conductor no se editan.
- Cerrar **no** reactiva el vehículo. El reintegro del seguro no puede superar la reparación (**400**). `netCost` = reparación − reintegro (calculado con `decimal.js`).
- Adjuntos (fotos, denuncia): `/attachments/vehicle_accident/:id`. El chofer accede a los que reportó él.

## Reactivar un vehículo (CU-247)

`POST /car/:id/reactivate` pasa un vehículo `grounded` a `active`. **404** si no es de la
distribuidora; **409** «El vehículo no está fuera de servicio»; **400** «No se puede reactivar: …»
con el documento bloqueante vencido (seguro, VTV, habilitación): es el mismo control que
`PUT /delivery/:id/vehicle`. No asigna el vehículo a nadie. Un vehículo `grounded` no se asigna a un
chofer (**409**) hasta reactivarlo.

## Costos (CU-203, CU-204)

| Método y ruta                         | Qué hace                                                           |
| ------------------------------------- | ------------------------------------------------------------------ |
| `GET /cars/:carId/costs?from&to`      | Costo de un vehículo: rubros, km, costo por km y evolución mensual |
| `GET /fleet/costs?from&to`            | Un renglón por vehículo, de mayor a menor costo por km             |
| `GET /api/v2/fleet/costs?from&to`     | Igual, más los totales de la flota (`summary`)                     |

`from` y `to` son obligatorios y el rango no pasa de 5 años (**400**). Los cinco rubros, sin
datos propios (se calculan en cada consulta):

1. `maintenance`: tareas `done` con `cost` y `performedAt` en el rango, sin los seguros.
2. `insurance`: prima de cada póliza **vigente o pagada** (plan `insurance`; no cuentan las canceladas ni las previstas, que son renovaciones pendientes con un importe estimado) × días de su vigencia
   `[validFrom, dueAt]` que caen en el rango / días de la vigencia. Sin `validFrom`, un año hacia
   atrás desde `dueAt` y `insuranceEstimated: true`.
3. `fuel`: cargas vigentes del rango.
4. `fines`: multas `paid` con `paidAt` en el rango y **sin imputar** al chofer (`paidAmount`).
5. `accidents`: siniestros `closed` con `closedAt` en el rango (reparación − reintegro). El costo de la reparación se carga **en el siniestro**; no hay que cargarlo además como tarea de mantenimiento con costo, porque se contaría dos veces.

`km`: suma del registro de uso diario (`vehicle_usage_log`) y, si no hay, la diferencia de
kilometraje entre las cargas del rango (`kmSource`: `usage_log`, `odometer` o `none`).
`costPerKm` es `null` sin km. El tablero toma los vehículos no dados de baja de la distribuidora y
ordena por `costPerKm` descendente, los de `null` al final (por `total`).

### Totales del tablero (API v2)

`GET /api/v2/fleet/costs?from&to` devuelve `{ from, to, summary, vehicles }`: `vehicles` son los mismos renglones de la v1 y
`summary` los totales que antes sumaba el panel (`resumirTablero`, en `domain/vehicle-cost.ts`): `vehicles` (cantidad),
`maintenance`, `insurance`, `fuel`, `fines`, `accidents` y `total` (suma de los vehículos, con o sin km), `km` (suma de los
vehículos que tienen km), `costPerKm` y `withoutKm`. **El costo por km de la flota sólo cuenta los vehículos con km**
(costo de esos vehículos ÷ sus km, a 2 decimales; `null` si ninguno tiene km): sumar el costo de uno sin km y dividirlo
por los km de los demás inflaría el promedio, y `withoutKm` los informa aparte. La v1 sigue devolviendo la lista sola
(congelada); el panel usa la v2. Mismos límites de rango (400).

## Neumáticos (CU-205, CU-206; opcional)

| Método y ruta                         | Qué hace                                                           |
| ------------------------------------- | ------------------------------------------------------------------ |
| `POST /fleet/tires`                   | Registra; nace `in_stock`. Serie única por distribuidora (**409** «El neumático ya está registrado») |
| `GET /fleet/tires?status&carId`       | Lista con `total`                                                  |
| `GET /fleet/tires/:id`                | Con su historial (`events`)                                        |
| `POST /fleet/tires/:id/events`        | Registra un movimiento; devuelve `{ event, tire }`                 |
| `GET /cars/:carId/tires`              | Los de un vehículo                                                 |

Movimientos (`type`, siempre con `odometerKm`):

| Tipo       | Admite el estado | Datos          | Resultado                                              |
| ---------- | ---------------- | -------------- | ------------------------------------------------------ |
| `mount`    | `in_stock`       | `carId`, `position` | `mounted`; guarda el km del montaje                |
| `unmount`  | `mounted`        | —              | `in_stock`; suma los km del montaje a `kmTraveled`    |
| `rotate`   | `mounted`        | `position` nueva | misma posición no; suma los km y reinicia el montaje |
| `retread`  | `in_stock`       | —              | suma `retreadCount`                                    |
| `retire`   | `in_stock`, `mounted` | —         | `retired`, definitivo                                  |

Un movimiento que no corresponde al estado es **409** «Movimiento inválido para el estado del
neumático»; la posición ocupada del vehículo, **409**; falta de `carId`/`position` en montaje o
rotación, **400**; `odometerKm` menor que el del montaje, **400**. `position` es un código corto
(hasta 6 letras o números, en mayúsculas: `DI`, `TD`…). El movimiento es un asiento: no se modifica.

## Migración `FlotaAmpliada`

Tablas `fuel_load`, `traffic_fine`, `vehicle_accident`, `tire` y `tire_event`; `car.fuel_type` y
`car.tank_capacity_liters`; `maintenance_task.valid_from`; `maintenance_plan.document_kind` y su
backfill por nombre; el plan de la habilitación para las distribuidoras que ya existen. El enum
`fuel_type_enum` lo comparten `car` y `fuel_load`. `down` deshace todo y borra los planes de
habilitación; si ya tienen tareas **frena con un mensaje claro** («hay habilitaciones de mercancías
peligrosas cargadas…») en vez de fallar por la clave foránea. `document_kind` lo comparte la
documentación del personal (`1792080000000`): si ese `down` corre con la flota aplicada (en una base
donde la flota corrió antes), deja la columna, achica el tipo a los tres valores de flota y frena con
un mensaje claro si algún plan tiene un tipo del personal; si la flota no está, la borra con su tipo.

## Decisiones y límites

- El kilometraje de una carga se compara con la carga anterior **por fecha**; no se revalida contra
  las posteriores (cargar con fecha pasada puede dejar una posterior con kilometraje menor).
- Las multas de un chofer dado de baja con egreso (sin cuenta) no deducen responsable.
- **Pagos en efectivo desde una caja** (`cash_movement_id` en `traffic_fine` y `fuel_load`, sin clave foránea;
  categorías de sistema `traffic_fine` y `fuel`, orígenes `traffic_fine` y `fuel_load`):
  - **Multa** (`PATCH /fleet/fines/:id/pay`): con `paidInCash: true` el `paidAmount` sale de la caja `cashBoxId` en la
    misma transacción. Obligatoria si hay cajas de efectivo activas (400), de efectivo (400), de la distribuidora (404),
    con sesión abierta si la exige y saldo (409: la multa queda sin pagar). `cashBoxId` sin `paidInCash`, 400. Una multa
    pagada no se paga de nuevo (409, sin segundo asiento) ni se anula: el asiento se corrige con un movimiento manual.
  - **Carga del administrador** (`POST /fleet/fuel-loads` con `paymentMethod: cash_box`): el `totalAmount` sale de
    `cashBoxId` con las mismas reglas. `cashBoxId` con otro medio de pago, 400. Una carga ya asentada no cambia de
    importe ni de medio (409: se anula y se registra de nuevo); anularla (`DELETE`) asienta el contraasiento. Con
    `driver_cash`, `card` o `fuel_account` no se toca ninguna caja.
  - **Carga del chofer** (`POST /fleet/fuel-loads/mine`): el chofer no elige caja (no manda `cashBoxId`). Con
    `driver_cash` pagó con su efectivo: no hay asiento y lo declara como gasto en su rendición. Con `cash_box` la carga
    queda **pendiente de asentar** (`cashMovementId: null`) hasta que un administrador indica la caja con
    `PATCH /fleet/fuel-loads/:id/cash-payment` (409 si ya salió de una caja o está anulada, 400 si no es `cash_box`);
    la rendición del chofer no la toma, porque no la pagó él.
    **Riesgo de doble descuento:** el gasto que el chofer declara en su rendición no está ligado a la carga. Una carga
    `cash_box` hay que resolverla por UNA sola vía: o el administrador la asienta en una caja, o el chofer la rinde como
    gasto; nunca las dos (la caja saldría dos veces). Por eso una carga del chofer no cambia entre `driver_cash` y
    `cash_box` al modificarla (**409**: se anula y se registra de nuevo).
  - **Cargas `cash_box` anteriores a la migración** (`cash_payment_legacy = true`): se resolvieron fuera del libro, no se
    asientan (**409** en `cash-payment`) y el panel no ofrece «Asentar en caja»; si hace falta, un egreso manual con motivo.
    `registered_by_driver` marca las que registró el chofer.
  - Concurrencia: la carga se lee con `FOR UPDATE` y `cashMovementId` se relee con el lock tomado; dos `cash-payment`
    simultáneos dan un 200 y un 409 con un solo movimiento. Orden de locks: carga → vehículo → caja.
    - Migración `1792600000000-EgresosDeEfectivoACaja`: agrega `cash_movement_id` a `traffic_fine` y `fuel_load`, y
    `registered_by_driver` y `cash_payment_legacy` a `fuel_load`.
- La imputación de una multa es una marca (`chargedToEmployee`) hasta que exista el libro de comisiones.
