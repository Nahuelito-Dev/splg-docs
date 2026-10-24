# Auditoría

Hay dos registros, con propósitos distintos. Los dos son de sólo escritura (un
trigger de la base rechaza `UPDATE` y `DELETE`).

|                     | Bitácora de operaciones (`audit_log`)               | Auditoría de datos (`audit`, `audit_detail`)                                                           |
| ------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Caso de uso         | CU-152 / CU-153                                     | Modelo de la cátedra                                                                                   |
| Qué registra        | Cada request HTTP de escritura, exitoso o rechazado | Cada registro de una entidad de negocio que se dio de alta, se modificó, se dio de baja o se reactivó  |
| Granularidad        | Una fila por request, con el cuerpo en `changes`    | Una `audit` por registro afectado y un `audit_detail` por campo que cambió, con valor anterior y nuevo |
| Quién la escribe    | `AuditInterceptor` (global)                         | `DataAuditSubscriber` (global, TypeORM), en la misma transacción del cambio                            |
| Consulta            | `GET /audit`                                        | `GET /audit/entries`, `GET /audit/entries/:id`, `GET /audit/action-types`                              |
| Ve los rechazos     | Sí (`result = failure`)                             | No: sólo hay auditoría si el cambio se confirmó                                                        |
| Fuera de un request | No (depende del request)                            | Sí, con usuario null (crons, seeds, webhooks sin usuario)                                              |

## Auditoría de datos

Tablas (nombres de la cátedra entre paréntesis):

- `audit_action_type` (TipoAccionAuditoria): `action_type_id`, `name`. Fija: 1 Alta,
  2 Modificación, 3 Baja lógica, 4 Reactivación, 5 Baja física (`AuditActionTypeId`).
- `audit` (Auditoria): `audit_id`, `action_type_id`, `user_id` (idUsuario, null =
  sistema), `distributor_id` (tenant), `entity` (entidadAfectada, nombre de la
  entidad de dominio: `Order`, `Car`...), `record_id` (idRegistro, también en
  las altas), `ip` (ipUsuario), `created_at` (fechaHora).
- `audit_detail` (DetalleAuditoria): `audit_detail_id`, `audit_id`, `field`
  (campo, nombre de la propiedad de la entidad), `old_value` (valorAnterior),
  `new_value` (valorNuevo).

### Cómo se captura

`DataAuditSubscriber` escucha `afterInsert`, `afterUpdate`, `afterSoftRemove` y
`afterRecover` de todas las entidades y escribe con el `manager` del evento: si
la transacción hace rollback, la auditoría también. Usuario, IP y distribuidora
del request llegan por `AsyncLocalStorage` (`AuditContextInterceptor`, que corre
después de los guards).

- Alta: un detalle por campo con valor (anterior null).
- Modificación: un detalle por columna realmente cambiada. Si no cambió nada, no
  se escribe nada.
- Baja lógica y reactivación: detalle del campo `deletedAt`.
- Valores en texto: fechas ISO, números y decimales como string, booleanos
  `true`/`false`, jsonb y puntos como JSON, relaciones por su id.
- Secretos (contraseñas, hashes, tokens FCM, claves, `deliveryCode`): el campo
  se registra con `[oculto]`. DNI, CUIL y CBU sí se auditan.
- `createdAt`/`updatedAt` no se registran (son de sistema).
- Baja física (`afterRemove`): si algo se borra de verdad con `remove`, queda una
  Auditoria tipo 5 con los valores que tenía (anterior = valor, nuevo = null).
  La regla sigue siendo que nada se borra físicamente: esto es la red de
  seguridad. Las promociones de una garrafa que salen de la lista se dan de baja
  (`deletedAt`), no se borran.
- Un insert/upsert por query builder que llega sin id no escribe una Auditoria
  con `record_id` vacío: se loguea un warn y se omite.
- Distribuidora de la auditoría: la columna propia del registro; las entidades de
  una distribuidora sin columna (renglón de pedido, promoción...) toman la del
  request; las de la persona o globales (User, Customer, UserAddress, Role)
  quedan sin distribuidora y sólo las ve el super admin.

Los depósitos (`Warehouse`) quedan auditados con el resto: alta, edición (incluido el cambio del
predeterminado, que son dos asientos) y baja lógica; `GET /audit/entries?entity=Warehouse&recordId=` devuelve
su historial. La entrega manual de un pedido (por `PATCH /orders/:id/status` o por `POST /orders/:id/confirm-delivery` de un admin) agrega al `Order` el detalle `manualDeliveryReason` (ver
`STOCK.md`).

### Qué no se audita

Una sola lista, con el porqué, en `src/audit/data/audit-exclusions.ts`: las
tablas de auditoría y `audit_log`, `document_sequence`, `storage_orphan`,
`order_dispatch_offer`, `route_batch_offer`, los historiales que sólo se agregan
(`order_status_history`, `cylinder_movement`, `vehicle_usage_log`), el libro de
stock físico (`stock_movement`, su saldo materializado `stock_balance` y el
renglón `stock_adjustment_item`, que cubre la cabecera del ajuste), el carrito
(`cart`, `cart_item`), la posición del chofer (`Delivery.location` y
`actualLocation`) y la marca `MaintenanceTask.alertedAt`.

### Lo que el subscriber no ve

TypeORM no anuncia `update()`, `softDelete()`, `delete()` ni los query builders.
Para una entidad de negocio se escribe con `save`/`softRemove` sobre la entidad
cargada, o se llama a `AuditoriaDeDatos.registrar(manager, ...)` en la misma
transacción. El borrado físico con `remove` sí queda (Baja física, tipo 5, vía
`afterRemove`); `delete()` y los query builders no.

### API (admin y super admin)

- `GET /audit/entries?entity&recordId&orderId&userId&actionType&from&to&page&limit` →
  `{ data, total }`. Cada entrada: `auditId`, `actionType {id, name}`,
  `user {userId, fullName, email} | null`, `distributorId`, `entity`,
  `recordId`, `ip`, `dateTime`, `details[] {auditDetailId, field, oldValue, newValue}`.
- `orderId` (uuid, mayúsculas o minúsculas) trae el historial de un pedido: los asientos del `Order`, de sus
  renglones (`OrderItem`) y de sus pagos (`Payment`), que se reconocen por el campo
  `orderId` de su detalle. Todo asiento de un `OrderItem` o un `Payment` (alta,
  modificación, baja) lleva además un detalle `orderId` aunque no haya cambiado
  (`CONTEXTO_DE_PEDIDO` en `audit-exclusions.ts`), para que una modificación como la
  del webhook de pago también aparezca. Los hijos se acotan por la distribuidora del pedido, no por
  la del request (el renglón no tiene columna propia). Se combina con `entity`
  (`Order`, `OrderItem`, `Payment`), las fechas y la paginación. Los renglones que una
  edición de `PATCH /orders/:id` reemplaza se borran con `remove` y quedan como Baja
  física (tipo 5) con los valores que tenían (el `orderId` en el valor anterior), así
  que el historial del pedido muestra alta, modificación y baja de cada renglón. La
  búsqueda usa dos índices parciales sobre `audit_detail` (`field = 'orderId'`).
- `GET /audit/entries/:id` → una entrada. Otra distribuidora: 404.
- `GET /audit/action-types` → el catálogo.

El admin de empresa ve sólo su distribuidora. El super admin ve todo, o la que
elige con `X-Distributor`. Los registros sin distribuidora (por ejemplo, roles)
sólo los ve el super admin.

La auditoría arranca con la migración `AuditoriaDeDatos`: no hay historia previa.
