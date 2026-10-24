# Validaciones en la base (tandas V1 y V2)

Regla del proyecto: toda regla de negocio se valida en el front, en el back y en la
base. Esta tanda lleva a la base las reglas de datos (CHECK, únicos, exclusiones,
claves foráneas) y cierra huecos del back. El back responde un 400/409 legible
**antes** de que salte la restricción; si algo se escapa (dos operaciones a la vez),
`traducirErrorDeBase` y el filtro global traducen la violación con el mensaje de
`src/common/errors/restricciones-de-base.ts` (23514 → 400; 23505 y 23P01 → 409).

Verificación de la base: `scripts/verificar-constraints.sql` (transacción con ROLLBACK):

    docker exec -i splg-bd psql -U postgres -d splg_db -v ON_ERROR_STOP=1 < scripts/verificar-constraints.sql

## Migraciones (en orden)

| Migración | Qué hace |
|---|---|
| `NormalizarCuitDeDistribuidora` | `distributor.tax_id` queda sólo con dígitos. |
| `RecargoPorMedioDePagoEnPedido` | Columna `order.payment_surcharge_amount` (numeric(10,2) NOT NULL DEFAULT 0) y carga de los pedidos existentes (total menos ítems, zona y express). |
| `DatosDeLasValidacionesDeLaBase` | Cancelados sin motivo → «Sin motivo registrado»; prioridad de zonas activas renumerada sin repetidos (conserva quién gana); patentes en mayúsculas sin espacios; ofertas de despacho: de varias `accepted` del mismo pedido sólo queda la más reciente (las anteriores pasan a `rejected`, como lo escribe hoy el back al liberar, así ese chofer no se reofrece) y un `expiresAt` igual o anterior a `offeredAt` pasa a un segundo después. |
| `ChecksDeLaBase` | ~90 CHECK (NOT VALID + VALIDATE; `CHK_cylinder_movement_cambio` ya nace en su forma final, que admite mismo estado con nota), funciones `es_cuit_valido` / `es_cuil_valido`, promoción máxima 99 %. |
| `UnicidadesDeLaBase` | Únicos: `lower(email)`, patente por distribuidora, dirección principal, oferta viva/aceptada, renglón por garrafa, franja y zona por nombre (activas), prioridad de zona (activas), serial y tipo normalizados, orden de parada. |
| `ClavesForaneasFaltantes` | 8 FK que faltaban (`order.payment_confirmed_by`, `payment_resolved_by`, `vehicle_car_id`, `payment_refund.requested_by_user_id`, `purchase_receipt.voided_by_user_id` y `cash_movement_id`, `fuel_load.cash_movement_id`, `traffic_fine.cash_movement_id`). |
| `SaldoDelChoferNumerico` | `delivery.balance` pasa a numeric(12,2). |
| `ExclusionesDeLaBase` | `btree_gist` y EXCLUDE: franjas, jornadas, asignación de vehículo (por vehículo y por chofer), reglas de comisión. |
| `BorradoRestrictivoDeUsuariosYPedidos` | `user` → customer/delivery/car/user_address/admin y `order` → rating/incident/historial/cambios de dirección pasan a RESTRICT. |
| `EstadoDelPagoYMovimientoDeEnvase` | `CHK_cylinder_movement_cambio` (ya creado así por `ChecksDeLaBase`; acá se vuelve a dejar idempotente) admite un movimiento sin cambio de estado si trae nota (la anotación de una revisión rechazada de un envase que está afuera); trigger `TRG_payment_estado_no_retrocede` (un pago aprobado sólo pasa a devuelto; rechazado, cancelado y devuelto no cambian). |
| `FormulaDelTotalDelPedido` | `CHK_order_total_formula`: total = ítems + zona + recargo online + express (el express no cuenta si el pedido pasó al reparto común). Va última porque exige que todo el back que crea o edita pedidos complete `payment_surcharge_amount`. |
| `NormalizarSerialesDeEnvase` | `cylinder.serial` existente en su forma canónica (`upper(btrim(serial))`: sin espacios en los bordes y en mayúsculas; JS y la base recortan sólo espacios U+0020, no tabulaciones); si otro envase de la distribuidora ya tuviera esa forma, no lo toca y lo avisa en el log (el índice único usa la misma expresión, así que no debería pasar; si pasara, se resuelve a mano: `SELECT * FROM cylinder WHERE upper(btrim(serial)) = '<SERIAL>'` y se da de baja o corrige uno). |

**Instalación desde cero:** el `data-source` corre cada migración en su propia transacción (`migrationsTransactionMode: 'each'`); con una sola transacción para todas, la base rechaza usar un valor de enum agregado en la misma corrida (`account` en `order_paymentmethod_enum`, usado por `ChecksDeLaBase`).

**Orden de las migraciones y bases ya migradas:** TypeORM no deja intercalar una migración nueva antes de otra ya ejecutada, por eso los arreglos de datos y del CHECK de movimientos se hicieron dentro de `DatosDeLasValidacionesDeLaBase` y `ChecksDeLaBase`. En una base donde ya corrieron (como `splg_db`) esos cambios no se reaplican, y no hace falta: el esquema final es idéntico (verificado comparando el volcado de esquema de `splg_db` con el de una base vacía migrada de punta a punta) y las filas que corregirían eran 0 en `splg_db`.

## Reglas del back que cambian

- **Pedido**: `items` no puede ser vacío; el recargo online se guarda aparte (`paymentSurchargeAmount`) en alta, edición y cambio de dirección, y el total es la suma exacta; `scheduledDate` no puede ser pasada (día argentino), con o sin franja; cancelar exige motivo (cliente y admin; el chofer, que libera, no): `PATCH /orders/:id/cancel`, `PATCH /orders/:id/status` con `cancelled` (usa `reason`) y las cancelaciones automáticas dejan su motivo. `DELETE /orders/:id` (deprecado) manda un motivo fijo.
- **Pagos**: un pago aprobado no retrocede (pending/rejected/cancelled atrasados se ignoran; sólo puede pasar a refunded); si la pasarela aprueba un importe distinto del esperado, el pago queda marcado en `metadata.montoDistinto`, se registra una alerta (log ERROR) y el pedido no se da por pagado ni se despacha.
- **Despacho**: una oferta sólo se cierra desde `offered` (el vencimiento no pisa una aceptada); un pedido tiene un solo chofer que lo sostiene.
- **Franjas**: inicio < fin, capacidad 1–10000, nombre único y sin solaparse entre activas (409).
- **Zonas**: nombre y prioridad únicos entre activas (409); sin prioridad en el alta, queda la siguiente.
- **Catálogo**: tipo sin blancos y único sin distinguir mayúsculas/espacios; precio hasta 10.000.000 y peso hasta 1000 kg, 2 decimales; promoción 0,01–99 %.
- **Envases**: serial no vacío, recortado y en mayúsculas (alta, edición y asignación; la asignación y las lecturas por serial buscan por esa forma canónica); fabricación ≤ vencimiento; una revisión no puede ser anterior a la fabricación.
- **Cuentas corrientes**: máquina de estados `active ↔ blocked`, `active|blocked → closed`, `closed → active` (cerrada no pasa a bloqueada).
- **Flota**: patente argentina `AAA123` o `AA123AA` (409 si ya existe en la distribuidora); odómetro de combustible contra la carga anterior **y la siguiente**; multas: infracción no futura, vencimiento ≥ infracción, pago ≥ infracción; cerrar/cancelar una tarea bloquea la fila y la fecha de cierre no es futura; el saldo del chofer se ajusta con la fila bloqueada y en decimal.
- **Personas**: teléfono E.164 también al editar y único; nacimiento anterior al ingreso; CUIT de la distribuidora con 11 dígitos (acepta guiones y los quita).
- **Direcciones**: una sola principal; al mover la principal se desmarca la vieja antes de marcar la nueva.

## Deshacer las migraciones

Política: un `down` nunca pierde datos en silencio. Si volver atrás exige descartar o decidir sobre datos que el esquema nuevo permitía, **aborta antes de tocar nada** con un diagnóstico (qué filas y cómo consultarlas); quien revierte decide, borra o corrige a mano y reintenta.

- `UnicidadesDeLaBase.down` vuelve la patente a única en todo el sistema. Si ya hay patentes vigentes repetidas entre distribuidoras (algo legítimo con V1), **aborta antes de tocar nada** con un mensaje que lista las patentes: hay que dar de baja o cambiar las repetidas y reintentar.
- `EstadoDelPagoYMovimientoDeEnvase.down` restaura el CHECK estricto de `cylinder_movement`: si hay movimientos con mismo estado de origen y destino (anotaciones de revisiones rechazadas) aborta con la cantidad y la consulta para verlos.
- `btree_gist` queda instalada al deshacer `ExclusionesDeLaBase`.
- Las migraciones de datos (`NormalizarCuitDeDistribuidora`, `DatosDeLasValidacionesDeLaBase`) no se pueden revertir: su `down` no hace nada.
- `FormulaDelTotalDelPedido` completa `payment_surcharge_amount` en los pedidos creados mientras tanto con la diferencia.

## Pruebas de integración

El esquema de las suites sale de las entidades (`DB_SYNC`), así que el arranque del Postgres efímero (`test/integration/setup/test-env.ts`) corre un script inicial que crea `btree_gist` y las funciones `es_cuit_valido` / `es_cuil_valido` (la misma definición que usa la migración, en `src/migrations/sql/funciones-cuit.ts`) antes de que la app sincronice; y, una vez creado el esquema, instala el trigger `TRG_payment_estado_no_retrocede` desde las mismas definiciones (`src/migrations/sql/estado-del-pago.ts`). Los pedidos de los fixtures cumplen las reglas nuevas con `test/integration/setup/pedido-valido.ts` (chofer y fechas según el estado, motivo al cancelar).

## Pago: atomicidad y alerta de monto

`PaymentsService.updateLedger` lee, valida y escribe dentro de una transacción con el pago bloqueado (`FOR UPDATE`); el trigger de la base es la segunda barrera. La marca `metadata.montoDistinto` es persistente: cualquier notificación posterior del mismo pago (aun un `pending` atrasado) la sigue informando y `ConfirmPaymentUseCase` no despacha.

## Tanda V2: transiciones, saldos contra el libro, tenant y reglas del back

Cinco migraciones más (van después de `NormalizarSerialesDeEnvase`, en este orden):

| Migración | Qué hace |
|---|---|
| `TransicionesDeEstado` | Un trigger `BEFORE UPDATE OF <estado>` por máquina de estado: pedido, envase, rendición, liquidación, orden de compra, carga del camión, reclamo, cuenta corriente y oferta de despacho. Una transición que no está en la tabla falla con SQLSTATE 23514 y la restricción `CHK_<tabla>_transicion_de_estado` (409 en castellano). Repetir el mismo estado pasa. La tabla de pares válidos sale de `src/migrations/sql/transiciones-de-estado.ts`, copia congelada de las constantes del dominio; `transiciones-de-estado.spec.ts` falla si una máquina del dominio cambia sin actualizar la copia (y su migración). |
| `SaldosContraLibro` | CONSTRAINT TRIGGER DEFERRABLE INITIALLY DEFERRED (se verifica al commit, por fila tocada, desde el saldo y desde el movimiento): `cash_box.balance` = Σ `cash_movement`, `customer_account.balance` = Σ asientos (cargo y nota de débito suman; cobro y nota de crédito restan), `stock_balance.quantity` = Σ entradas − Σ salidas de `stock_movement` por (ubicación, garrafa, condición). Falla con `CHK_cash_box_saldo_contra_libro`, `CHK_customer_account_saldo_contra_libro` o `CHK_stock_balance_saldo_contra_libro` y deshace toda la operación (409). También `CHK_customer_account_allocation_tope`: lo imputado a un asiento no pasa de su importe. Antes de crearlos verifica que hoy todo cierra; si no, aborta con el diagnóstico. Los índices de destino/origen de `stock_movement` pasan a (ubicación, garrafa, condición). El saldo del chofer (`delivery.balance`) no tiene libro (se ajusta a mano con `PATCH /delivery/:id/balance`): no se controla. |
| `TenantCruzado` | 55 FK compuestas `(id, distributor_id)` `FK_<hijo>_<columna>_distribuidora` (pedido ↔ chofer/zona/franja/vehículo, movimientos de caja ↔ caja/sesión/categoría, movimientos y existencias de stock ↔ ubicación/garrafa, cuenta corriente, rendiciones, liquidaciones, comisiones, cargas del camión, compras, envases, etc.) más 20 únicos `UQ_<padre>_id_distribuidora`. Se agregan a la FK simple, que conserva su `ON DELETE`. Antes de crearlas cuenta las filas que hoy las violarían y, si hay alguna, aborta con la lista. Quedan fuera `payment` y `payment_refund` (MercadoPago). `tenant-cruzado.spec.ts` verifica que las entidades declaran las mismas claves. |
| `ExclusionDeLiquidaciones` | `EXC_driver_liquidation_periodo_solapado`: los períodos de un mismo chofer no se pisan (días cerrados; las anuladas no cuentan). |
| `ReglasDelBackEnLaBase` | CHECK de largo (`CHK_claims_largo_de_textos`, `CHK_incident_largo_de_textos`, `CHK_rating_largo_de_textos`, `CHK_order_nota_de_impago_largo`), `CHK_traffic_fine_pago_contra_importe`, `CHK_purchase_order_fecha_esperada`; y triggers: cobro de cuenta corriente no mayor que la deuda (`..._cobro_mayor_a_la_deuda`, 409), fabricación de envase no futura, rendición no abierta para un día futuro, odómetros monótonos (carga de combustible, cierre de tarea de mantenimiento y movimiento de neumático). |

Bypass explícito, sólo para seeds y fixtures de integración (el back nunca lo usa): `SET LOCAL splg.bypass_transiciones = on`, `splg.bypass_saldos = on` o `splg.bypass_reglas = on` dentro de la transacción. Los helpers de las pruebas están en `test/integration/setup/bypass.ts`. El seed demo escribe el stock por el servicio del libro (movimiento y existencia en la misma transacción) y no toca la caja, así que no usa bypass.

### Contrato que cambia

- Largos máximos (400 si se pasan; el mismo valor en el DTO y en el CHECK): motivo del reclamo 120; descripción y resolución de reclamo (alta, resolución, reapertura) y de incidencia (alta, edición, resolución) 1000; nota de resolución del impago 500, y ahora también **mínimo 10** (`PATCH /orders/:id/payment/resolve-unpaid`, campo `note`). Constantes en `src/common/constants/largos-de-texto.ts`.
- `POST /customer-accounts/:id/payments`: un cobro mayor que la deuda responde 409 («registrá una nota de crédito por la diferencia»).
- `PATCH /fleet/fines/:id/pay`: `paidAmount` no puede superar el importe de la multa (400).
- Orden de compra: `expectedDate` no puede ser anterior a hoy (400); al editar sólo se valida si la fecha cambia.
- Envases: `manufacturedAt` no puede ser futuro (400, margen de 5 minutos por el reloj del cliente).
- Rendición: `businessDate` no puede ser un día futuro (día argentino, 400).
- Odómetros: carga de combustible (salvo corrección con nota), cierre de tarea de mantenimiento y evento de neumático no pueden ir hacia atrás respecto del anterior (ni pasarse del siguiente) del mismo vehículo (400).
- Liquidaciones: un período que se pisa con otro no anulado del mismo chofer responde 409.
- Cualquier transición de estado inválida que llegue a la base responde 409 con el mensaje de `restricciones-de-base.ts`; una referencia a una fila de otra distribuidora, 409 «El registro elegido pertenece a otra distribuidora».
- Alinear el panel (`npm run api:types` y los esquemas zod): máximos de los textos de reclamo, incidencia, resolución y nota de impago, mínimo 10 de la nota de impago, `paidAmount` ≤ importe de la multa, `expectedDate` ≥ hoy, `manufacturedAt` no futuro, tope del cobro de cuenta corriente, fecha de rendición, odómetros.

### Costo medido

`pgbench` sobre una copia de `splg_db`, un cliente, una transacción = un asiento más el ajuste del saldo, 1500 corridas: con el libro de la copia, caja 0,77 → 1,01 ms y stock 0,78 → 1,05 ms; con 50 000 asientos en la misma caja o existencia, caja 0,89 → 1,51 ms y stock 0,76 → 1,26 ms. El control suma el libro de la fila tocada una vez por commit: crece con el largo del libro de esa caja/existencia, no con el de la tabla.

### Aplicar en `splg_db`

    docker exec splg-bd pg_dump -U postgres -Fc splg_db > splg_db-pre-v2.dump
    npm run migration:run      # con el back que trae este código; apagar antes el que corre con código viejo
    docker exec -i splg-bd psql -U postgres -d splg_db -v ON_ERROR_STOP=1 < scripts/verificar-constraints.sql

Deshacer: `npm run migration:revert` cinco veces (las migraciones nuevas son reversibles).
