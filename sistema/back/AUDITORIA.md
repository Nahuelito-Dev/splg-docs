# Auditoría

Hay dos registros, con propósitos distintos. Los dos son de sólo escritura (un
trigger de la base rechaza `UPDATE` y `DELETE`).

|                     | Bitácora de operaciones (`audit_log`)               | Auditoría de datos (`audit`, `audit_detail`)                                                           |
| ------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Caso de uso         | CU-152 / CU-153                                     | Modelo de la cátedra                                                                                   |
| Qué registra        | Cada request HTTP de escritura, exitoso o rechazado | Cada registro de una entidad de negocio que se dio de alta, se modificó, se dio de baja o se reactivó  |
| Granularidad        | Una fila por request, con el cuerpo en `changes`    | Una `audit` por registro afectado y un `audit_detail` por campo que cambió, con valor anterior y nuevo |
| Quién la escribe    | `AuditInterceptor` (global)                         | La base: trigger `TRG_auditoria` en cada tabla, en la misma transacción del cambio                     |
| Consulta            | `GET /audit`                                        | `GET /audit/entries`, `GET /audit/entries/:id`, `GET /audit/action-types`                              |
| Ve los rechazos     | Sí (`result = failure`)                             | No: sólo hay auditoría si el cambio se confirmó                                                        |
| Fuera de un request | No (depende del request)                            | Sí, con usuario null: crons, scripts y también SQL escrito a mano                                      |

En la bitácora de operaciones, `resource` es el primer segmento de la ruta después de `/api/` y de la
versión (`/api/v2/insurance-policies/:id` → `insurance-policies`). Los asientos anteriores al 30/10/2026 de
las rutas versionadas quedaron con `v1` o `v2` como recurso (la bitácora no se modifica); su `path` sí
tiene la ruta completa.

## Auditoría de datos

Tablas (nombres de la cátedra entre paréntesis):

- `audit_action_type` (TipoAccionAuditoria): `action_type_id`, `name`. Fija: 1 Alta,
  2 Modificación, 3 Baja lógica, 4 Reactivación, 5 Baja física, 6 Ingreso, 7 Ingreso fallido, 8 Salida
  (`AuditActionTypeId`).
- `audit` (Auditoria): `audit_id`, `action_type_id`, `user_id` (idUsuario, null =
  sistema), `distributor_id` (tenant), `entity` (entidadAfectada, nombre de la
  entidad de dominio: `Order`, `Car`...), `record_id` (idRegistro, también en
  las altas), `ip` (ipUsuario), `created_at` (fechaHora).
- `audit_detail` (DetalleAuditoria): `audit_detail_id`, `audit_id`, `field`
  (campo, nombre de la propiedad de la entidad), `old_value` (valorAnterior),
  `new_value` (valorNuevo).

### Cómo se captura (triggers en la base)

La auditoría de datos la escribe **la base de datos**, no la aplicación. Cada tabla de `public` (74, todas
menos las de «Qué no se audita») tiene el trigger `TRG_auditoria` (`AFTER INSERT OR UPDATE OR DELETE FOR
EACH ROW`), que llama a la función plpgsql `auditoria_trigger()`. Así queda registrado todo cambio, lo haga
la API, un cron, un script o alguien con SQL directo. Migración: `1793700000000-AuditoriaPorTriggers`.

- **INSERT** → Alta: un detalle por campo con valor (anterior null).
- **UPDATE** → Modificación, con un detalle por columna que cambió de verdad (un UPDATE sin cambios no
  escribe nada). Si la columna que cambió es la de baja lógica (`deletedAt` y equivalentes) es **Baja
  lógica** o **Reactivación**. Ejemplo pedido por la cátedra: un chofer que pasa de un tipo a otro deja una
  Modificación con el campo, el valor anterior y el nuevo.
- **DELETE** → Baja física, con los valores que tenía (red de seguridad: la regla sigue siendo que nada se
  borra físicamente).
- **Nombres:** `entity` y `field` siguen siendo los del dominio (`Warehouse`, `deletedAt`), no los de la
  tabla: el trigger los traduce con `audit_entity_map` (tabla → entidad) y `audit_field_map` (tabla +
  columna → propiedad). Los mapas se generan de la metadata de TypeORM con `npm run auditoria:mapa`, y un
  test falla si una entidad nueva no tiene trigger o falta en el mapa.
- **Quién lo hizo:** la API le pasa a la base el usuario, la IP y la distribuidora del request con
  `set_config('splg.user_id' | 'splg.ip' | 'splg.distributor_id', …, true)` al empezar cada transacción
  (`src/audit/data/actor-en-la-base.ts`). Las escrituras sueltas (`update()`, `insert()`, query builders) se
  envuelven en una transacción para que también lleven el actor. El valor es local a la transacción: no
  pasa de un request a otro por el pool de conexiones.
- **Columnas nuevas de `audit`:** `source` (quién escribió el asiento: `db` = el trigger; `app` = asientos
  de la aplicación, como las sesiones o los anteriores al 28/10/2026), `table_name` (tabla física), `db_user`
  (usuario de Postgres) y `app_name` (`application_name` de la conexión). Un cambio por SQL directo queda
  con `user_id` null y el usuario de la base que lo hizo.
- **Valores en texto:** fechas ISO, números y decimales como texto, booleanos `true`/`false`, jsonb y
  puntos como JSON, relaciones por su id. Secretos (contraseñas, hashes, tokens FCM, claves,
  `deliveryCode`) se guardan como `[oculto]`. `createdAt`/`updatedAt` no se registran.
- **Distribuidora del asiento:** la columna propia del registro; si no la tiene, la del request; las de la
  persona o globales (User, Customer, UserAddress, Role) quedan sin distribuidora y sólo las ve el super
  admin.
- **Rendimiento:** ~0,3 ms extra por fila escrita.

### Sesiones (Ingreso, Ingreso fallido, Salida)

`audit_action_type` suma 6 Ingreso, 7 Ingreso fallido y 8 Salida, con entidad `Sesion`. Cada ingreso al
panel o a las apps (`POST /auth/login`, `/auth/login/dashboard`), correcto o no, deja un asiento con el
email, la IP, el canal y el origen (`X-Client-Source`); el fallido, además, el motivo. Nunca se guardan
contraseñas ni tokens.

### Inmutabilidad

Los triggers `audit_inmutable` rechazan todo `UPDATE` o `DELETE` sobre `audit` y `audit_detail`, y otro
`BEFORE TRUNCATE` rechaza vaciarlas (también en cascada): la auditoría no se corrige ni se borra, ni siquiera
por SQL.

### Mantenimiento: el seed de la demo

Re-sembrar la demo borra y vuelve a crear miles de filas. Para no llenar la auditoría de asientos «sistema», el
seed conecta con `splg.audit_off = on`. El trigger lo respeta **sólo** si el usuario de la base que escribe es
miembro del rol `splg_mantenimiento` (un superusuario lo es); cualquier otra conexión que lo intente queda
auditada igual. Por eso, en producción la API se conecta con un usuario de la base que **no** es superusuario
ni miembro de ese rol. Cada proceso se identifica con su `application_name`: `splg-api`, `splg-script:<archivo>`
o `splg-migraciones`.

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

### API (admin y super admin)

**v2 (la que usa el panel desde el 30/10/2026):** `GET /api/v2/audit/entries`, `GET /api/v2/audit/entries/:id` y
`GET /api/v2/audit/action-types`. Mismos filtros y respuesta que la v1, más:

- filtro `origin`: `user` (lo hizo un usuario), `system` (automático: crons, webhooks, ingresos fallidos, sin
  usuario y desde la API) o `direct` (sin usuario y desde otra aplicación: SQL a mano o scripts);
- en cada entrada, `origin`, `source`, `tableName`, `dbUser` y `appName`.

El exporte (`GET /api/v2/exports/auditoria-datos?format=csv|xlsx`) acepta los mismos filtros, `origin`
incluido, y suma las columnas Origen, Escrito por, Tabla, Usuario de la base y Aplicación.

**v1 (congelada):**

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

La auditoría arranca con la migración `AuditoriaDeDatos`: no hay historia previa. Lo anterior al 28/10/2026 lo escribió la aplicación (`source = app`).
