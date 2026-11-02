# Transacciones, triggers y procedimientos en la base

Relevamiento de cómo el sistema mantiene la consistencia de los datos: qué hace la
aplicación dentro de una transacción (commit y rollback), qué garantiza la base por sí
misma con triggers y restricciones, y por qué no hay procedimientos almacenados.

La regla del proyecto es la de las tres capas (front, back y base): la aplicación decide
y la base **no deja** que quede un dato que viole una regla, aunque alguien escriba por
fuera del back.

## 1. Transacciones en la aplicación

Cada caso de uso que escribe más de una fila lo hace en una sola transacción de
PostgreSQL. Hay dos formas en el código:

| Forma | Cuándo se usa | Rollback |
|---|---|---|
| `DataSource.transaction(async (manager) => { … })` | La mayoría de los casos de uso | Automático: si el bloque lanza un error, TypeORM hace `ROLLBACK` y el error sube al controlador |
| `QueryRunner` con `startTransaction` / `commitTransaction` / `rollbackTransaction` | Pedidos (alta, cambio de estado, cancelación, liberación, confirmación de pago, despacho) | Explícito en el `catch`, y `release()` en el `finally` |

Dentro de la transacción se toman **locks** para que dos operaciones simultáneas no se
pisen:

- `SELECT … FOR UPDATE` (`pessimistic_write`) sobre la fila que se va a modificar: el
  pedido, la caja, la cuenta corriente, la orden de compra, el pago.
- `pg_advisory_xact_lock` cuando no hay una fila que bloquear: reglas de comisión, zonas
  de cobertura, franjas horarias, «siempre queda un administrador» y licencias del
  personal. Se libera solo al terminar la transacción.
- La conciliación de stock usa nivel de aislamiento `REPEATABLE READ`.

| Módulo | Operaciones dentro de una transacción |
|---|---|
| Pedidos | Alta (bloquea cuenta, franja, carrito y stock), modificación, cancelación con restitución de stock, cambio de estado, liberación, confirmación del pago, reserva, asignación de chofer, pase de express a reparto común |
| Cobros del pedido | Efectivo recibido, cobro registrado por el admin, transferencia confirmada, pedido impago resuelto |
| Stock y cargas | Conteo inicial, ajuste, transferencia, reversión de lote, conciliación y su ajuste, carga y descarga del camión |
| Caja y cuenta corriente | Movimientos de caja, apertura y cierre, débitos y créditos de la cuenta, imputaciones, rendición del chofer |
| Compras | Orden de compra, recepción (compra + ítems + stock + caja), pago y anulación de la recepción |
| Flota y gastos | Tareas de taller, cargas de combustible, neumáticos, pago de multas, siniestros, pólizas y cuotas de seguro, liquidación del chofer |
| Personal | Asistencia, licencias, legajo, baja del empleado y del usuario (libera vehículo y legajo en la misma transacción) |
| Otros | Reclamos, adjuntos, fotos, importación de datos, conciliación con Mercado Pago, planificador de taller |

Además, `ActorEnLaBase` abre una transacción incluso para una escritura suelta, para fijar
el usuario, la IP y la distribuidora que después lee el trigger de auditoría.

La idempotencia de los pedidos HTTP (`Idempotency-Key`, guardada en Redis 24 h) evita
que un reintento ejecute dos veces la misma operación; no reemplaza a la transacción.

**Procedimientos con `COMMIT`.** Un procedimiento que controla la transacción (`COMMIT`/`ROLLBACK`) no se puede llamar dentro de una: la base responde «invalid transaction termination». Por eso se invoca siempre con `dataSource.query('CALL …')` sin transacción abierta, y la capa de auditoría (`ActorEnLaBase`) no envuelve los `CALL` en una transacción de una sentencia como hace con los `INSERT`/`UPDATE`/`DELETE`. El actor de auditoría (`splg.user_id`, etc.) vive sólo en la transacción donde se fijó y no sobrevive al `COMMIT` inicial del procedimiento: por eso estos procedimientos **no escriben tablas auditadas** (la alerta de stock no lo es; los de verificación sólo leen).

## 2. Lo que garantiza la base

### Triggers de auditoría e inmutabilidad

| Trigger | Tabla | Qué hace |
|---|---|---|
| `TRG_auditoria` | Todas las tablas del mapa de auditoría | Registra en `audit` y `audit_detail` cada alta, modificación, baja lógica y reactivación, con el actor de la transacción |
| `audit_inmutable`, `audit_detail_inmutable`, `audit_log_inmutable` | Tablas de auditoría | No se puede modificar ni borrar un registro de auditoría |
| `audit_sin_truncate`, `audit_detail_sin_truncate` | Tablas de auditoría | Rechazan `TRUNCATE` |
| `cash_movement_solo_agregar`, `customer_account_entry_solo_agregar`, `commission_entry_solo_agregar` | Libros de caja, cuenta corriente y comisiones | Sólo se agregan asientos; un error se corrige con un contraasiento |
| `stock_movement_inmutable` | Movimientos de stock | Ídem para el stock |

Detalle en [AUDITORIA.md](AUDITORIA.md).

### Saldo contra libro (triggers diferidos)

Son `CONSTRAINT TRIGGER … DEFERRABLE INITIALLY DEFERRED`: no se evalúan en cada sentencia
sino **al hacer commit**. Así la transacción puede escribir el movimiento y el saldo en
cualquier orden, y si al final no coinciden, el commit falla y todo vuelve atrás.

| Regla | Tablas |
|---|---|
| El saldo de la caja es la suma de sus movimientos | `cash_box`, `cash_movement` |
| El saldo de la cuenta corriente es la suma de sus débitos y créditos | `customer_account`, `customer_account_entry` |
| La existencia por depósito, producto y condición coincide con su libro | `stock_balance`, `stock_movement` |
| Una imputación no supera el importe del débito ni del crédito | `customer_account_allocation` |

### Reglas de estado y de dominio

| Trigger | Regla |
|---|---|
| `TRG_payment_estado_no_retrocede` | Un pago no vuelve atrás de estado (sólo `pending → …` y `approved → refunded`) |
| `TRG_<tabla>_transicion_de_estado` | Copia de las máquinas de estado de pedido, envase, rendición, liquidación, orden de compra, carga del camión, reclamo, cuenta corriente y oferta de despacho: una actualización directa a un estado inválido falla |
| `TRG_customer_account_entry_cobro_maximo` | Un cobro no supera la deuda |
| `TRG_fuel_load_odometro_monotono`, `TRG_maintenance_task_odometro_monotono`, `TRG_tire_event_odometro_monotono` | El odómetro no retrocede |
| `TRG_cylinder_fabricacion_no_futura`, `TRG_driver_settlement_fecha_futura` | Sin fechas futuras |
| `employee_leave_no_overlap` | Licencias sin superposición |
| `TRG_cash_collection_settings_clase` | La caja de Mercado Pago es billetera y la de transferencias, bancaria |

A esto se suman los CHECK, únicos, claves foráneas y exclusiones de
[VALIDACIONES-BASE.md](VALIDACIONES-BASE.md).

## 3. Funciones y procedimientos almacenados

Las funciones de la base (`auditoria_trigger`, `verificar_saldo_de_caja`, `transicion_de_estado_<tabla>`, `es_cuit_valido`…) son funciones PL/pgSQL que sólo disparan los triggers o usan los CHECK.

Los casos de uso siguen viviendo en el dominio (controladores del back), donde se prueban y se versionan con la API: un procedimiento almacenado partiría el caso de uso en dos lugares sin ganar consistencia. La excepción son dos tareas nocturnas de **verificación**, que no corrigen datos y se resuelven mejor dentro de la base, con una sola ida y vuelta y una transacción propia:

| Procedimiento | Lo llama | Qué hace |
|---|---|---|
| `conciliar_stock_del_dia(distribuidora, INOUT consistente, avisar, firma, resultado)` | `StockReconciliationCron` (03:00) | Compara el vendible con el físico menos las reservas y busca entregas sin movimiento; si todo cierra borra la alerta vigente; si no, devuelve la huella y si corresponde avisar |
| `verificar_saldos_de_caja(distribuidora, INOUT desfasadas, detalle)` | `FinanceReconciliationCron` (03:30) | Informa las cajas y cuentas corrientes cuyo saldo no es la suma de su libro |

Se invocan con `CALL`, una vez por distribuidora, y devuelven lo encontrado por parámetros `INOUT`. Trabajan en `REPEATABLE READ` (las cifras son del mismo instante) y controlan la transacción: la lectura y las escrituras van en el cuerpo principal, los bloques `EXCEPTION` sólo capturan el error; si hubo error hacen `ROLLBACK` y relanzan con `RAISE EXCEPTION` conservando el SQLSTATE original. El cron de stock registra el fallo sin cortar a las demás distribuidoras; el de finanzas lo propaga. Reglas de uso: ver §1 (no se llaman dentro de una transacción y no escriben tablas auditadas). Se prueban contra un Postgres efímero (`test/integration/procedimientos-conciliacion.e2e-spec.ts`) mostrando `COMMIT`, `ROLLBACK`, la huella contra el algoritmo anterior y la llamada desde un contexto de request.

## 4. Operaciones con servicios externos

Mercado Pago, Firebase, Amazon S3 y el correo no participan de la transacción de la base:
un `ROLLBACK` no puede deshacer una preferencia de pago ni un archivo subido. Para esas
operaciones el sistema usa **compensación** (una saga): primero la parte externa, después
la transacción local, y si la local falla se deshace la externa. Nunca se llama a un
servicio externo con un lock de la base tomado.

| Operación | Cómo queda consistente | Riesgo que queda |
|---|---|---|
| Devolución de un pago (Mercado Pago) | La devolución se pide con clave de idempotencia; el cierre de la devolución y el egreso en la caja van en una sola transacción | El pago se marca como reintegrado después, fuera de esa transacción: si ese paso falla, queda la devolución cerrada con el pago aprobado. El arreglo (moverlo adentro) está listo y se integra cuando se pruebe con una devolución real |
| Checkout de Mercado Pago | Se guarda el pago pendiente, se crea la preferencia y se guarda su enlace | Si falla el último paso, la preferencia existe sin enlace local; el pago queda pendiente |
| Registro de usuario (Firebase) | Se crea la cuenta en Firebase y después el usuario en la base; si la base falla, se borra la cuenta de Firebase | Si también falla el borrado, queda una cuenta de Firebase sin usuario |
| Cambio de email (Firebase) | Se cambia en Firebase y después en la base | Sin compensación si la base falla |
| Baja de usuario | Se da de baja en la base y se deshabilita en Firebase con tres reintentos | Si fallan los tres, la API igual lo rechaza (la base manda), pero Firebase lo deja entrar hasta corregirlo |
| Adjuntos y fotos (S3) | Se sube el archivo, se registra en la transacción y, si falla, se borra lo subido | Si falla la limpieza, queda un archivo sin referencia (no accesible) |
| Correos | Se envían después del commit, desde un evento | Si el proceso cae entre el commit y el envío, el correo se pierde (no el dato) |

Mejoras posibles a futuro: una tabla de salida (*outbox*) escrita en la misma transacción
para los correos y las sincronizaciones con Firebase, y un endpoint para regenerar el
enlace de un checkout.

## 5. Cómo se prueba

- Unit tests de cada servicio con el doble del `EntityManager`.
- Los triggers se prueban contra la base en `test/integration` (contenedores efímeros) y
  con `scripts/verificar-constraints.sql`, que corre dentro de una transacción con
  `ROLLBACK`.
- `migraciones-sin-diff` verifica que las migraciones y las entidades no se desfasen.
