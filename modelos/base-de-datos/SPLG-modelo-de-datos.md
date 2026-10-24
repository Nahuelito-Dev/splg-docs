# Modelo de Datos — SPLG

85 tablas y 293 claves foráneas: 238 simples y 55 compuestas `(id, distributor_id)` que fijan la distribuidora, leídas de la base en ejecución.

Cada FK compuesta `(id, distributor_id)` se suma a la FK simple sobre `id` y le impide a una fila apuntar a otra distribuidora; en el diagrama de base de datos es la misma relación que la simple, así que no lleva otra arista.

| Sección | Qué contiene |
|---|---|
| [Diccionario de datos](#diccionario-de-datos) | Las tablas tal cual están hoy en la base, con tipo, obligatoriedad, clave, referencia, default, descripción, `CHECK` e índices |
| [Relaciones no declaradas](#relaciones-no-declaradas) | Columnas que apuntan a otra tabla sin clave foránea |
| [Modelo propuesto](#modelo-propuesto) | Lo que falta agregar, por pedido de la cátedra |
| [Tipos enumerados](#tipos-enumerados) | Los valores admitidos por cada enumerado |

## Diccionario de datos

### `admin` — Administrador

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `admin_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | no | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | sí | FK | `user.user_id` |  | Un perfil por usuario. El rol no se guarda acá: es el del usuario (`user.role_id`). Repetirlo era redundante y permitía que los dos dijeran cosas distintas (H-77). |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_0fc586a3c26b9bb49e64e6ff1f`: `CREATE INDEX "IDX_0fc586a3c26b9bb49e64e6ff1f" ON public.admin USING btree (distributor_id)`
- `UQ_admin_user`: `CREATE UNIQUE INDEX "UQ_admin_user" ON public.admin USING btree (user_id)`

### `attachment` — Adjunto

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `attachment_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `owner_type` | attachment_owner_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `owner_id` | uuid | sí |  |  |  | Sin FK (ver la nota de la clase). |
| `label` | varchar(80) | no |  |  |  | Texto libre para distinguir adjuntos del mismo dueño: "DNI frente", "Póliza 2026". |
| `storage_key` | varchar(255) | sí |  |  |  | Clave del objeto dentro del bucket de S3. |
| `original_name` | varchar(255) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `mime_type` | varchar(100) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `size_bytes` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `uploaded_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `uploaded_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deleted_at` | timestamptz | no |  |  |  | Baja lógica: el registro queda para histórico y el archivo NO se borra del storage (queda de respaldo). Los listados y descargas no lo muestran. |

Índices (además de la clave primaria):
- `IDX_70d35b9e83fa8fca69e685f548`: `CREATE INDEX "IDX_70d35b9e83fa8fca69e685f548" ON public.attachment USING btree (distributor_id, owner_type, owner_id)`

### `audit` — Auditoria

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `audit_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `action_type_id` | smallint | sí | FK | `audit_action_type.action_type_id` |  | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | no | FK | `user.user_id` |  | Quién lo hizo; null si fue el sistema (cron, seed, webhook sin usuario). |
| `distributor_id` | uuid | no | FK | `distributor.distributor_id` |  | Distribuidora (tenant) del registro, para acotar la consulta. |
| `entity` | varchar(60) | sí |  |  |  | Nombre de la entidad de dominio (`Order`, `Employee`...), no la URL. |
| `record_id` | varchar(64) | sí |  |  |  | Id del registro afectado; en una clave compuesta, las partes con ':'. |
| `ip` | varchar(45) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `created_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_audit_distributor_created_at`: `CREATE INDEX "IDX_audit_distributor_created_at" ON public.audit USING btree (distributor_id, created_at)`
- `IDX_audit_entity_record`: `CREATE INDEX "IDX_audit_entity_record" ON public.audit USING btree (entity, record_id)`
- `IDX_audit_user`: `CREATE INDEX "IDX_audit_user" ON public.audit USING btree (user_id)`

### `audit_action_type` — TipoAccionAuditoria

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `action_type_id` | smallint | sí | PK |  |  | _(sin descripción documentada en el código)_ |
| `name` | varchar(40) | sí | U |  |  | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `UQ_920dea5fea6e965ccf619575f55`: `CREATE UNIQUE INDEX "UQ_920dea5fea6e965ccf619575f55" ON public.audit_action_type USING btree (name)`

### `audit_detail` — DetalleAuditoria

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `audit_detail_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `audit_id` | uuid | sí | FK | `audit.audit_id` |  | _(sin descripción documentada en el código)_ |
| `field` | varchar(80) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `old_value` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `new_value` | text | no |  |  |  | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_audit_detail_audit`: `CREATE INDEX "IDX_audit_detail_audit" ON public.audit_detail USING btree (audit_id)`
- `IDX_audit_detail_order_anterior`: `CREATE INDEX "IDX_audit_detail_order_anterior" ON public.audit_detail USING btree (old_value) WHERE ((field)::text = 'orderId'::text)`
- `IDX_audit_detail_order_nuevo`: `CREATE INDEX "IDX_audit_detail_order_nuevo" ON public.audit_detail USING btree (new_value) WHERE ((field)::text = 'orderId'::text)`

### `audit_log` — AsientoAuditoria

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `audit_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | no | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `actor_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `actor_role` | varchar(30) | no |  |  |  | Rol con que operó. |
| `http_method` | varchar(10) | sí |  |  |  | POST, PUT, PATCH o DELETE. |
| `resource` | varchar(60) | sí |  |  |  | Tipo de recurso afectado (el primer segmento de la ruta). |
| `resource_id` | varchar(64) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `path` | varchar(255) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `client_source` | varchar(30) | no |  |  |  | Panel, app de cliente o app de chofer (header X-Client-Source). |
| `ip` | varchar(45) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `result` | audit_result_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status_code` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `changes` | jsonb | no |  |  |  | _(sin descripción documentada en el código)_ |
| `error_message` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `created_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_audit_log_actor`: `CREATE INDEX "IDX_audit_log_actor" ON public.audit_log USING btree (actor_user_id)`
- `IDX_audit_log_created_at`: `CREATE INDEX "IDX_audit_log_created_at" ON public.audit_log USING btree (created_at)`
- `IDX_audit_log_distributor`: `CREATE INDEX "IDX_audit_log_distributor" ON public.audit_log USING btree (distributor_id)`

### `car` — Vehiculo

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `car_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `type_car` | varchar(50) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `car_capacity` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `car_patent` | varchar(20) | no |  |  |  | Única por distribuidora entre los vehículos vigentes (`UQ_car_patente_ distribuidora_vigente`): dar de baja uno no bloquea volver a registrar la misma patente. |
| `car_brand` | varchar(50) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `car_model` | varchar(50) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `car_year` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `car_color` | varchar(50) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | Baja lógica: la fila se conserva para el historial y la auditoría. |
| `tare_weight_kg` | numeric(10,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `max_load_kg` | numeric(10,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `odometer_km` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `fleet_status` | fleet_status_enum | sí |  |  | `'active'::fleet_status_enum` | _(sin descripción documentada en el código)_ |
| `in_service_since` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `photo_key` | varchar(512) | no |  |  |  | Key de la foto del vehículo en el bucket (`cars/{distribuidora}/{vehículo}/{uuid}.{ext}`). |
| `fuel_type` | fuel_type_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `tank_capacity_liters` | numeric(6,2) | no |  |  |  | Capacidad del tanque en litros: tope de cada carga de combustible (+5 %). |

Claves únicas compuestas: (`car_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_car_patente`: `CHECK (((car_patent IS NULL) OR ((car_patent)::text ~ '^([A-Z]{3}[0-9]{3}|[A-Z]{2}[0-9]{3}[A-Z]{2})$'::text)))`

Índices (además de la clave primaria):
- `IDX_e823ac113ba2af8cbe72ddcbe8`: `CREATE INDEX "IDX_e823ac113ba2af8cbe72ddcbe8" ON public.car USING btree (distributor_id)`
- `UQ_car_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_car_id_distribuidora" ON public.car USING btree (car_id, distributor_id)`
- `UQ_car_patente_distribuidora_vigente`: `CREATE UNIQUE INDEX "UQ_car_patente_distribuidora_vigente" ON public.car USING btree (distributor_id, car_patent) WHERE ("deletedAt" IS NULL)`

### `cart` — Carrito

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `cart_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `updated_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`user_id`, `distributor_id`).

Índices (además de la clave primaria):
- `UQ_cart_user_distributor`: `CREATE UNIQUE INDEX "UQ_cart_user_distributor" ON public.cart USING btree (user_id, distributor_id)`

### `cart_item` — ItemCarrito

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `cart_item_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `cart_id` | uuid | sí | FK | `cart.cart_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `quantity` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `unit_price` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`cart_id`, `gas_cylinder_id`).

Restricciones `CHECK`:
- `CHK_cart_item_cantidad`: `CHECK (((quantity >= 1) AND (quantity <= 999)))`
- `CHK_cart_item_precio`: `CHECK ((unit_price >= (0)::numeric))`

Índices (además de la clave primaria):
- `UQ_cart_item_cart_gascylinder`: `CREATE UNIQUE INDEX "UQ_cart_item_cart_gascylinder" ON public.cart_item USING btree (cart_id, gas_cylinder_id)`

### `cash_box` — Caja

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `cash_box_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `name` | varchar(80) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `kind` | cash_box_kind_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `balance` | numeric(14,2) | sí |  |  | `'0'::numeric` | _(sin descripción documentada en el código)_ |
| `requires_session` | boolean | sí |  |  | `false` | Si exige una sesión abierta (con arqueo al cerrar) para mover dinero. |
| `is_active` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`cash_box_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_cash_box_efectivo_no_negativo`: `CHECK (((kind <> 'cash'::cash_box_kind_enum) OR (balance >= (0)::numeric)))`

Índices (además de la clave primaria):
- `IDX_cash_box_distributor`: `CREATE INDEX "IDX_cash_box_distributor" ON public.cash_box USING btree (distributor_id)`
- `UQ_cash_box_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_cash_box_id_distribuidora" ON public.cash_box USING btree (cash_box_id, distributor_id)`
- `UQ_cash_box_nombre_vigente`: `CREATE UNIQUE INDEX "UQ_cash_box_nombre_vigente" ON public.cash_box USING btree (distributor_id, name) WHERE ("deletedAt" IS NULL)`

### `cash_category` — CategoriaDeCaja

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `category_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `name` | varchar(80) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `direction` | cash_category_direction_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `system_code` | cash_category_system_code_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `is_active` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`category_id`, `distributor_id`).

Índices (además de la clave primaria):
- `IDX_cash_category_distributor`: `CREATE INDEX "IDX_cash_category_distributor" ON public.cash_category USING btree (distributor_id)`
- `UQ_cash_category_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_cash_category_id_distribuidora" ON public.cash_category USING btree (category_id, distributor_id)`
- `UQ_cash_category_nombre_activa`: `CREATE UNIQUE INDEX "UQ_cash_category_nombre_activa" ON public.cash_category USING btree (distributor_id, direction, name) WHERE ((is_active = true) AND (system_code IS NULL))`
- `UQ_cash_category_sistema`: `CREATE UNIQUE INDEX "UQ_cash_category_sistema" ON public.cash_category USING btree (distributor_id, system_code) WHERE (system_code IS NOT NULL)`

### `cash_movement` — MovimientoDeCaja

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `movement_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `cash_box_id` | uuid | sí | FK | `cash_box.cash_box_id` |  | _(sin descripción documentada en el código)_ |
| `session_id` | uuid | no | FK | `cash_session.session_id` |  | _(sin descripción documentada en el código)_ |
| `direction` | cash_movement_direction_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `category_id` | uuid | sí | FK | `cash_category.category_id` |  | _(sin descripción documentada en el código)_ |
| `method` | cash_movement_method_enum | sí |  |  | `'cash'::cash_movement_method_enum` | _(sin descripción documentada en el código)_ |
| `occurred_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `description` | varchar(255) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `reference_type` | cash_movement_reference_type_enum | sí |  |  | `'manual'::cash_movement_reference_type_enum` | _(sin descripción documentada en el código)_ |
| `reference_id` | uuid | no |  |  |  | Documento que originó el movimiento (rendición, liquidación, pago…). Sin clave foránea a propósito: apunta a tablas de distintos módulos según `referenceType`. |
| `reverses_movement_id` | uuid | no | FK | `cash_movement.movement_id` |  | _(sin descripción documentada en el código)_ |
| `created_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`movement_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_cash_movement_importe`: `CHECK ((amount > (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_cash_movement_caja_fecha`: `CREATE INDEX "IDX_cash_movement_caja_fecha" ON public.cash_movement USING btree (cash_box_id, occurred_at)`
- `IDX_cash_movement_distribuidora_fecha`: `CREATE INDEX "IDX_cash_movement_distribuidora_fecha" ON public.cash_movement USING btree (distributor_id, occurred_at)`
- `IDX_cash_movement_referencia`: `CREATE INDEX "IDX_cash_movement_referencia" ON public.cash_movement USING btree (reference_type, reference_id)`
- `IDX_cash_movement_sesion`: `CREATE INDEX "IDX_cash_movement_sesion" ON public.cash_movement USING btree (session_id)`
- `UQ_cash_movement_anula`: `CREATE UNIQUE INDEX "UQ_cash_movement_anula" ON public.cash_movement USING btree (reverses_movement_id) WHERE (reverses_movement_id IS NOT NULL)`
- `UQ_cash_movement_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_cash_movement_id_distribuidora" ON public.cash_movement USING btree (movement_id, distributor_id)`

### `cash_session` — SesionDeCaja

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `session_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `cash_box_id` | uuid | sí | FK | `cash_box.cash_box_id` |  | _(sin descripción documentada en el código)_ |
| `status` | cash_session_status_enum | sí |  |  | `'open'::cash_session_status_enum` | _(sin descripción documentada en el código)_ |
| `opened_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `opened_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `opening_amount` | numeric(14,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `closed_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `closed_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `expected_amount` | numeric(14,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `counted_amount` | numeric(14,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `difference` | numeric(14,2) | no |  |  |  | Contado menos esperado: negativa es faltante, positiva sobrante. |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`session_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_cash_session_cierre_completo`: `CHECK (((status <> 'closed'::cash_session_status_enum) OR ((closed_by_user_id IS NOT NULL) AND (counted_amount IS NOT NULL) AND (expected_amount IS NOT NULL) AND (difference = (counted_amount - expected_amount)))))`
- `CHK_cash_session_cierre_fecha`: `CHECK (((status = 'closed'::cash_session_status_enum) = (closed_at IS NOT NULL)))`
- `CHK_cash_session_montos`: `CHECK (((opening_amount >= (0)::numeric) AND ((counted_amount IS NULL) OR (counted_amount >= (0)::numeric))))`
- `CHK_cash_session_periodo`: `CHECK (((closed_at IS NULL) OR (closed_at >= opened_at)))`

Índices (además de la clave primaria):
- `IDX_cash_session_caja_fecha`: `CREATE INDEX "IDX_cash_session_caja_fecha" ON public.cash_session USING btree (cash_box_id, opened_at)`
- `IDX_cash_session_distributor`: `CREATE INDEX "IDX_cash_session_distributor" ON public.cash_session USING btree (distributor_id)`
- `UQ_cash_session_abierta`: `CREATE UNIQUE INDEX "UQ_cash_session_abierta" ON public.cash_session USING btree (cash_box_id) WHERE (status = 'open'::cash_session_status_enum)`
- `UQ_cash_session_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_cash_session_id_distribuidora" ON public.cash_session USING btree (session_id, distributor_id)`

### `claims` — Reclamo

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `claim_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `customer_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `reason` | varchar | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `description` | text | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `photoUrl` | varchar | no |  |  |  | URL externa que mandaban las apps antes de que la foto se subiera a S3. |
| `status` | claims_status_enum | sí |  |  | `'pending'::claims_status_enum` | _(sin descripción documentada en el código)_ |
| `resolutionNote` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `photo_key` | varchar(512) | no |  |  |  | Key de la foto en el bucket (`claims/{distribuidora}/{reclamo}/{uuid}.{ext}`). |

Restricciones `CHECK`:
- `CHK_claims_largo_de_textos`: `CHECK (((char_length((reason)::text) <= 120) AND (char_length(description) <= 1000) AND (("resolutionNote" IS NULL) OR (char_length("resolutionNote") <= 1000))))`
- `CHK_claims_textos`: `CHECK (((btrim((reason)::text) <> ''::text) AND (btrim(description) <> ''::text)))`

Índices (además de la clave primaria):
- `IDX_870bf1e0dc6005837ff0643b5f`: `CREATE INDEX "IDX_870bf1e0dc6005837ff0643b5f" ON public.claims USING btree (distributor_id)`

### `commission_entry` — AsientoComision

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `entry_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `employee_id` | uuid | sí | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `delivery_id` | uuid | no | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `type` | commission_entry_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | no | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `rule_id` | uuid | no | FK | `commission_rule.rule_id` |  | _(sin descripción documentada en el código)_ |
| `rule_snapshot` | jsonb | no |  |  |  | _(sin descripción documentada en el código)_ |
| `liquidation_id` | uuid | no | FK | `driver_liquidation.liquidation_id` |  | _(sin descripción documentada en el código)_ |
| `reference_id` | uuid | no |  |  |  | Documento que originó la deducción (la rendición, la multa). Sin clave foránea a propósito: apunta a tablas de distintos módulos según `type`. |
| `description` | varchar(255) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `occurred_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `created_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_commission_entry_importe`: `CHECK ((amount <> (0)::numeric))`
- `CHK_commission_entry_signo`: `CHECK ((((type <> 'delivery_commission'::commission_entry_type_enum) OR (amount > (0)::numeric)) AND ((type <> 'settlement_shortage'::commission_entry_type_enum) OR (amount < (0)::numeric))))`

Índices (además de la clave primaria):
- `IDX_commission_entry_distributor`: `CREATE INDEX "IDX_commission_entry_distributor" ON public.commission_entry USING btree (distributor_id)`
- `IDX_commission_entry_empleado`: `CREATE INDEX "IDX_commission_entry_empleado" ON public.commission_entry USING btree (employee_id, occurred_at)`
- `IDX_commission_entry_liquidacion`: `CREATE INDEX "IDX_commission_entry_liquidacion" ON public.commission_entry USING btree (liquidation_id)`
- `UQ_commission_entry_faltante`: `CREATE UNIQUE INDEX "UQ_commission_entry_faltante" ON public.commission_entry USING btree (reference_id) WHERE (type = 'settlement_shortage'::commission_entry_type_enum)`
- `UQ_commission_entry_pedido`: `CREATE UNIQUE INDEX "UQ_commission_entry_pedido" ON public.commission_entry USING btree (order_id) WHERE (type = 'delivery_commission'::commission_entry_type_enum)`

### `commission_rule` — ReglaComision

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `rule_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `employee_id` | uuid | no | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | no | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `basis` | commission_rule_basis_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `value` | numeric(10,4) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `valid_from` | date | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `valid_to` | date | no |  |  |  | `null`: sin fecha de fin. |
| `is_active` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_commission_rule_porcentaje`: `CHECK (((basis <> 'percent_of_total'::commission_rule_basis_enum) OR (value <= (100)::numeric)))`
- `CHK_commission_rule_valor`: `CHECK ((value >= (0)::numeric))`
- `CHK_commission_rule_vigencia`: `CHECK (((valid_to IS NULL) OR (valid_to >= valid_from)))`

Índices (además de la clave primaria):
- `EXC_commission_rule_solapada`: `CREATE INDEX "EXC_commission_rule_solapada" ON public.commission_rule USING gist (distributor_id, COALESCE(employee_id, '00000000-0000-0000-0000-000000000000'::uuid), COALESCE(gas_cylinder_id, '00000000-0000-0000-0000-000000000000'::uuid), daterange(valid_from, valid_to, '[]'::text)) WHERE is_active`
- `IDX_commission_rule_distribuidora`: `CREATE INDEX "IDX_commission_rule_distribuidora" ON public.commission_rule USING btree (distributor_id, is_active)`

### `coverage_zone` — ZonaCobertura

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `coverage_zone_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `name` | varchar(120) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `area` | geometry | sí |  |  |  | Polígono del área (PostGIS geometry). spatialFeatureType 'Polygon' + SRID 4326. TypeORM lo lee/escribe como GeoJSON ({ type:'Polygon', coordinates }) con la columna de tipo geometry. |
| `surcharge_value` | numeric(10,2) | sí |  |  | `'0'::numeric` | Monto (fixed) o porcentaje (percentage) del recargo, según `surchargeType`. |
| `isActive` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | Baja lógica: la fila se conserva para el historial y la auditoría. |
| `surcharge_type` | coverage_zone_surcharge_type_enum | sí |  |  | `'percentage'::coverage_zone_surcharge_type_enum` | `fixed`: `surchargeValue` es un monto en la moneda del pedido. `percentage`: `surchargeValue` es un porcentaje (0-100) sobre el subtotal de los ítems. Default `percentage`: es el caso de uso que pidió el dueño ("tanto % más caro en Garupá"). |
| `label` | varchar(40) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `color` | varchar(7) | no |  |  |  | Color hexadecimal (`#RRGGBB`) para pintar la zona en el mapa del panel. |
| `valid_until` | timestamptz | no |  |  |  | Hasta cuándo rige la zona (exclusive). Null = no vence. |
| `priority` | integer | sí |  |  | `0` | Desempate entre zonas superpuestas: gana la de mayor `priority` (y, a igual prioridad, la de menor área). 0 = sin prioridad especial. |
| `valid_from` | timestamptz | no |  |  |  | Desde cuándo rige la zona. Null = rige desde siempre. |

Claves únicas compuestas: (`coverage_zone_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_coverage_zone_surcharge`: `CHECK ((((surcharge_type = 'fixed'::coverage_zone_surcharge_type_enum) AND (surcharge_value >= (0)::numeric)) OR ((surcharge_type = 'percentage'::coverage_zone_surcharge_type_enum) AND (surcharge_value >= (0)::numeric) AND (surcharge_value <= (100)::numeric))))`
- `CHK_coverage_zone_vigencia`: `CHECK (((valid_until IS NULL) OR (valid_from IS NULL) OR (valid_until > valid_from)))`

Índices (además de la clave primaria):
- `IDX_01a53f7455396839c245037c9f`: `CREATE INDEX "IDX_01a53f7455396839c245037c9f" ON public.coverage_zone USING gist (area)`
- `IDX_50ad99ebfb6554428f39160228`: `CREATE INDEX "IDX_50ad99ebfb6554428f39160228" ON public.coverage_zone USING btree (distributor_id)`
- `UQ_coverage_zone_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_coverage_zone_id_distribuidora" ON public.coverage_zone USING btree (coverage_zone_id, distributor_id)`
- `UQ_coverage_zone_nombre_activa`: `CREATE UNIQUE INDEX "UQ_coverage_zone_nombre_activa" ON public.coverage_zone USING btree (distributor_id, lower((name)::text)) WHERE ("isActive" AND ("deletedAt" IS NULL))`
- `UQ_coverage_zone_prioridad_activa`: `CREATE UNIQUE INDEX "UQ_coverage_zone_prioridad_activa" ON public.coverage_zone USING btree (distributor_id, priority) WHERE ("isActive" AND ("deletedAt" IS NULL))`

### `customer` — Cliente

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `customer_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `notification_token` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | no |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `location` | geometry | no |  |  |  | Última ubicación conocida (antes texto "lat,lng" en lat_lang). |
| `avg_monthly_consumption_kg` | numeric(10,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `declared_cylinder_type_id` | uuid | no | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `repurchase_notice_days` | integer | no |  |  | `3` | _(sin descripción documentada en el código)_ |
| `next_repurchase_estimate_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_customer_consumo`: `CHECK (((avg_monthly_consumption_kg IS NULL) OR (avg_monthly_consumption_kg > (0)::numeric)))`

Índices (además de la clave primaria):
- `IDX_0124ec56df62d9a9ba58cb41a2`: `CREATE INDEX "IDX_0124ec56df62d9a9ba58cb41a2" ON public.customer USING gist (location)`
- `REL_5d1f609371a285123294fddcf3`: `CREATE UNIQUE INDEX "REL_5d1f609371a285123294fddcf3" ON public.customer USING btree (user_id)`

### `customer_account` — CuentaCorriente

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `account_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `customer_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `business_name` | varchar(120) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `tax_id` | varchar(11) | no |  |  |  | CUIT: once dígitos, sin guiones. |
| `tax_condition` | customer_account_tax_condition_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `credit_limit` | numeric(12,2) | sí |  |  | `'0'::numeric` | _(sin descripción documentada en el código)_ |
| `payment_terms_days` | integer | sí |  |  | `30` | _(sin descripción documentada en el código)_ |
| `status` | customer_account_status_enum | sí |  |  | `'active'::customer_account_status_enum` | _(sin descripción documentada en el código)_ |
| `balance` | numeric(14,2) | sí |  |  | `'0'::numeric` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`account_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_customer_account_cerrada_sin_saldo`: `CHECK (((status <> 'closed'::customer_account_status_enum) OR (balance = (0)::numeric)))`
- `CHK_customer_account_cuit`: `CHECK (((tax_id IS NULL) OR es_cuit_valido((tax_id)::text)))`
- `CHK_customer_account_limite`: `CHECK ((credit_limit >= (0)::numeric))`
- `CHK_customer_account_plazo`: `CHECK ((payment_terms_days > 0))`
- `CHK_customer_account_plazo_maximo`: `CHECK ((payment_terms_days <= 365))`

Índices (además de la clave primaria):
- `IDX_customer_account_distributor`: `CREATE INDEX "IDX_customer_account_distributor" ON public.customer_account USING btree (distributor_id)`
- `UQ_customer_account_cliente_vigente`: `CREATE UNIQUE INDEX "UQ_customer_account_cliente_vigente" ON public.customer_account USING btree (distributor_id, customer_user_id) WHERE ("deletedAt" IS NULL)`
- `UQ_customer_account_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_customer_account_id_distribuidora" ON public.customer_account USING btree (account_id, distributor_id)`

### `customer_account_allocation` — ImputacionCuentaCorriente

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `allocation_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `account_id` | uuid | sí | FK | `customer_account.account_id` |  | _(sin descripción documentada en el código)_ |
| `debit_entry_id` | uuid | sí | FK | `customer_account_entry.entry_id` |  | _(sin descripción documentada en el código)_ |
| `credit_entry_id` | uuid | sí | FK | `customer_account_entry.entry_id` |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_customer_account_allocation_importe`: `CHECK ((amount > (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_customer_account_allocation_credito`: `CREATE INDEX "IDX_customer_account_allocation_credito" ON public.customer_account_allocation USING btree (credit_entry_id)`
- `IDX_customer_account_allocation_cuenta`: `CREATE INDEX "IDX_customer_account_allocation_cuenta" ON public.customer_account_allocation USING btree (account_id)`
- `IDX_customer_account_allocation_debito`: `CREATE INDEX "IDX_customer_account_allocation_debito" ON public.customer_account_allocation USING btree (debit_entry_id)`

### `customer_account_entry` — AsientoCuentaCorriente

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `entry_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `account_id` | uuid | sí | FK | `customer_account.account_id` |  | _(sin descripción documentada en el código)_ |
| `type` | customer_account_entry_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | no | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `due_date` | date | no |  |  |  | _(sin descripción documentada en el código)_ |
| `payment_method` | varchar(20) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `cash_movement_id` | uuid | no | FK | `cash_movement.movement_id` |  | _(sin descripción documentada en el código)_ |
| `collected_by_delivery_id` | uuid | no | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `description` | varchar(255) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `occurred_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `created_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_customer_account_entry_importe`: `CHECK ((amount > (0)::numeric))`
- `CHK_customer_account_entry_vencimiento`: `CHECK (((due_date IS NULL) OR (due_date >= ((occurred_at AT TIME ZONE 'America/Argentina/Buenos_Aires'::text))::date)))`

Índices (además de la clave primaria):
- `IDX_customer_account_entry_cuenta_fecha`: `CREATE INDEX "IDX_customer_account_entry_cuenta_fecha" ON public.customer_account_entry USING btree (account_id, occurred_at)`
- `IDX_customer_account_entry_distributor`: `CREATE INDEX "IDX_customer_account_entry_distributor" ON public.customer_account_entry USING btree (distributor_id)`
- `UQ_customer_account_entry_cargo_pedido`: `CREATE UNIQUE INDEX "UQ_customer_account_entry_cargo_pedido" ON public.customer_account_entry USING btree (order_id) WHERE (type = 'sale_charge'::customer_account_entry_type_enum)`

### `cylinder` — Envase

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `cylinder_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `serial` | varchar | sí |  |  |  | Número de serie físico grabado en el envase. Único por distribuidora. |
| `gas_cylinder_id` | uuid | no | FK | `gas_cylinder.gas_cylinder_id` |  | Tipo de producto al que corresponde (ej. "Garrafa 10kg"), sin relación para simplificar. |
| `state` | cylinder_state_enum | sí |  |  | `'in_depot'::cylinder_state_enum` | _(sin descripción documentada en el código)_ |
| `current_customer_id` | uuid | no | FK | `user.user_id` |  | Cliente que tiene actualmente el envase (User user_id), solo seteado en WITH_CUSTOMER. |
| `current_order_id` | uuid | no | FK | `order.order_id` |  | Pedido en el que el envase salió despachado. Se setea al asignarlo a un pedido (FILLED→DISPATCHED) y permite que, al pasar el pedido a DELIVERED, el sistema avance solo los envases de ESE pedido a WITH_CUSTOMER. Queda como referencia del último pedido en el que se entregó. |
| `deposit` | numeric(10,2) | sí |  |  | `'0'::numeric` | Monto de garantía/depósito cobrado por el envase. |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `manufactured_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `last_inspection_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `expires_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`distributor_id`, `serial`), (`cylinder_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_cylinder_cliente_segun_estado`: `CHECK (((state = 'with_customer'::cylinder_state_enum) = (current_customer_id IS NOT NULL)))`
- `CHK_cylinder_garantia`: `CHECK ((deposit >= (0)::numeric))`
- `CHK_cylinder_serial`: `CHECK ((btrim((serial)::text) <> ''::text))`
- `CHK_cylinder_vencimiento`: `CHECK (((expires_at IS NULL) OR (manufactured_at IS NULL) OR (expires_at >= manufactured_at)))`

Índices (además de la clave primaria):
- `IDX_7a848929dbfa5535e93e9494e7`: `CREATE INDEX "IDX_7a848929dbfa5535e93e9494e7" ON public.cylinder USING btree (serial)`
- `IDX_903b537f13281f56613047bcdc`: `CREATE INDEX "IDX_903b537f13281f56613047bcdc" ON public.cylinder USING btree (current_order_id)`
- `IDX_9e32d1c8fd5721ba71e98c5c93`: `CREATE INDEX "IDX_9e32d1c8fd5721ba71e98c5c93" ON public.cylinder USING btree (state)`
- `IDX_9e8b3d9c0ecf2651f6e836aca4`: `CREATE INDEX "IDX_9e8b3d9c0ecf2651f6e836aca4" ON public.cylinder USING btree (distributor_id)`
- `UQ_9e39bbb32ed614ddd09ac126e37`: `CREATE UNIQUE INDEX "UQ_9e39bbb32ed614ddd09ac126e37" ON public.cylinder USING btree (distributor_id, serial)`
- `UQ_cylinder_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_cylinder_id_distribuidora" ON public.cylinder USING btree (cylinder_id, distributor_id)`
- `UQ_cylinder_serial_normalizado`: `CREATE UNIQUE INDEX "UQ_cylinder_serial_normalizado" ON public.cylinder USING btree (distributor_id, upper(btrim((serial)::text)))`

### `cylinder_inspection` — RevisionEnvase

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `inspection_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `cylinder_id` | uuid | sí | FK | `cylinder.cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `inspected_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `result` | cylinder_inspection_result_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `next_due_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_cylinder_inspection_proxima`: `CHECK (((result = 'rejected'::cylinder_inspection_result_enum) OR (next_due_at IS NOT NULL)))`
- `CHK_cylinder_inspection_vencimiento`: `CHECK (((next_due_at IS NULL) OR (next_due_at > inspected_at)))`

Índices (además de la clave primaria):
- `IDX_1cbfd2007890911e8b42d207d4`: `CREATE INDEX "IDX_1cbfd2007890911e8b42d207d4" ON public.cylinder_inspection USING btree (distributor_id)`
- `IDX_531df2a7a7ab3fda4f1591e80d`: `CREATE INDEX "IDX_531df2a7a7ab3fda4f1591e80d" ON public.cylinder_inspection USING btree (cylinder_id)`

### `cylinder_movement` — MovimientoEnvase

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `movement_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `cylinder_id` | uuid | sí | FK | `cylinder.cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `from_state` | cylinder_movement_from_state_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `to_state` | cylinder_movement_to_state_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | no | FK | `order.order_id` |  | Pedido en cuyo contexto ocurrió la transición (dispatch/entrega), si aplica. |
| `actor_user_id` | uuid | no | FK | `user.user_id` |  | Usuario (chofer/admin) que ejecutó la transición, si aplica. |
| `note` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_cylinder_movement_cambio`: `CHECK (((from_state IS NULL) OR ((from_state)::text <> (to_state)::text) OR (note IS NOT NULL)))`

Índices (además de la clave primaria):
- `IDX_1c48ac355fa0315ba792b68045`: `CREATE INDEX "IDX_1c48ac355fa0315ba792b68045" ON public.cylinder_movement USING btree (cylinder_id)`
- `IDX_968ad11170db2741bb5c0c47bb`: `CREATE INDEX "IDX_968ad11170db2741bb5c0c47bb" ON public.cylinder_movement USING btree (distributor_id)`

### `cylinder_recovery_case` — CasoRecupero

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `case_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `cylinder_id` | uuid | sí | FK | `cylinder.cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `delivered_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `deposit_amount` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `step` | integer | sí |  |  | `1` | _(sin descripción documentada en el código)_ |
| `status` | recovery_case_status_enum | sí |  |  | `'open'::recovery_case_status_enum` | _(sin descripción documentada en el código)_ |
| `opened_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `closed_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `resolved_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `resolution_note` | text | no |  |  |  | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_32fe6a642ad74004e88561b07a`: `CREATE INDEX "IDX_32fe6a642ad74004e88561b07a" ON public.cylinder_recovery_case USING btree (cylinder_id)`
- `IDX_77cd8b4b3c44851b932ca9c12d`: `CREATE INDEX "IDX_77cd8b4b3c44851b932ca9c12d" ON public.cylinder_recovery_case USING btree (user_id)`
- `IDX_d6bb53d55c3556b23295d5ac5a`: `CREATE INDEX "IDX_d6bb53d55c3556b23295d5ac5a" ON public.cylinder_recovery_case USING btree (distributor_id)`

### `cylinder_recovery_notice` — AvisoRecupero

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `notice_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `case_id` | uuid | sí | FK | `cylinder_recovery_case.case_id` |  | _(sin descripción documentada en el código)_ |
| `step` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `kind` | recovery_notice_kind_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | proposal_status_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `sent_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `expires_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_ea6566148b8616520f5a1a7f1a`: `CREATE INDEX "IDX_ea6566148b8616520f5a1a7f1a" ON public.cylinder_recovery_notice USING btree (case_id)`

### `delivery` — Chofer

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `delivery_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | sí | FK | `user.user_id` |  | Indexado: el radar/dispatch y varios findOne buscan al chofer por user_id. |
| `calification` | double precision | no |  |  |  | _(sin descripción documentada en el código)_ |
| `actual_location` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `cancelledCharge` | real | no |  |  |  | _(sin descripción documentada en el código)_ |
| `validated` | boolean | sí |  |  | `false` | _(sin descripción documentada en el código)_ |
| `isActive` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `notification_token` | text | no |  |  |  | Token FCM del dispositivo del chofer, para push de ofertas/estado. |
| `balance` | numeric(12,2) | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | no |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `location` | geometry | no |  |  |  | Última ubicación conocida (antes texto "lat,lng" en latLng). |
| `isEnabled` | boolean | sí |  |  | `true` | Habilitación ADMINISTRATIVA: la pone/saca un admin con `PATCH /delivery/:id/status`. Un chofer deshabilitado no puede ponerse en línea aunque lo intente desde su app. Reemplaza a la vieja columna `isActive`, que mezclaba esto con la presencia del chofer (ver `isAvailable`): un chofer deshabilitado podía "conectarse" desde su app y volver a recibir pedidos. La columna `isActive` sigue existiendo en la base (no se borra ni se renombra: la sigue usando el proceso viejo mientras conviven ambos) pero este código ya no la lee ni la escribe. |
| `isAvailable` | boolean | sí |  |  | `false` | Presencia: true mientras el chofer está "en línea" en su app (`PATCH /delivery/user/:userId/availability`). Sale de línea al desconectarse, al deshabilitarlo un admin, o al cerrar la app (el gateway de sockets lo saca del radar al desconectar). |

Claves únicas compuestas: (`delivery_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_delivery_calificacion`: `CHECK (((calification IS NULL) OR ((calification >= (0)::double precision) AND (calification <= (5)::double precision))))`

Índices (además de la clave primaria):
- `IDX_8b64ee4e6e615c2082862f9e09`: `CREATE INDEX "IDX_8b64ee4e6e615c2082862f9e09" ON public.delivery USING btree (distributor_id)`
- `IDX_a3b8af1ce2f6e143d416d83080`: `CREATE INDEX "IDX_a3b8af1ce2f6e143d416d83080" ON public.delivery USING btree (user_id)`
- `IDX_c270386a78fdf46067bc9a94a7`: `CREATE INDEX "IDX_c270386a78fdf46067bc9a94a7" ON public.delivery USING gist (location)`
- `REL_a3b8af1ce2f6e143d416d83080`: `CREATE UNIQUE INDEX "REL_a3b8af1ce2f6e143d416d83080" ON public.delivery USING btree (user_id)`
- `UQ_delivery_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_delivery_id_distribuidora" ON public.delivery USING btree (delivery_id, distributor_id)`

### `distributor` — Distribuidora

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `distributor_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `name` | varchar(120) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `slug` | varchar(60) | sí | U |  |  | Identificador legible/estable para resolver el tenant (header/subdominio). |
| `legal_name` | varchar(160) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `tax_id` | varchar(20) | no |  |  |  | CUIT / identificación fiscal. |
| `email` | varchar | no |  |  |  | _(sin descripción documentada en el código)_ |
| `phone` | varchar | no |  |  |  | _(sin descripción documentada en el código)_ |
| `logo_url` | varchar | no |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | distributor_status_enum | sí |  |  | `'active'::distributor_status_enum` | _(sin descripción documentada en el código)_ |
| `plan` | varchar | no |  |  |  | Plan de suscripción SaaS (para facturación futura). |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `logo_key` | varchar(512) | no |  |  |  | Key de el logo en el bucket (`distributors/{distribuidora}/logo/{uuid}.{ext}`). |

Restricciones `CHECK`:
- `CHK_distributor_cuit`: `CHECK (((tax_id IS NULL) OR ((tax_id)::text ~ '^[0-9]{11}$'::text)))`
- `CHK_distributor_slug`: `CHECK (((slug)::text ~ '^[a-z0-9]+(-[a-z0-9]+)*$'::text))`

Índices (además de la clave primaria):
- `IDX_02331b27890084627684d99ec5`: `CREATE UNIQUE INDEX "IDX_02331b27890084627684d99ec5" ON public.distributor USING btree (slug)`
- `UQ_02331b27890084627684d99ec5b`: `CREATE UNIQUE INDEX "UQ_02331b27890084627684d99ec5b" ON public.distributor USING btree (slug)`

### `document_sequence` — Secuencia de documentos

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `distributor_id` | uuid | sí | PK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `doc_type` | varchar(40) | sí | PK |  |  | _(sin descripción documentada en el código)_ |
| `last_number` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_document_sequence_valores`: `CHECK (((last_number >= 0) AND ((doc_type)::text ~ '^[a-z][a-z0-9_]{0,39}$'::text)))`

### `driver_liquidation` — LiquidacionComisiones

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `liquidation_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `number` | integer | sí |  |  |  | Número correlativo por distribuidora (`document_sequence`). |
| `employee_id` | uuid | sí | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `period_from` | date | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `period_to` | date | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `gross` | numeric(12,2) | sí |  |  |  | Σ de los asientos que suman. |
| `deductions` | numeric(12,2) | sí |  |  |  | Σ (en positivo) de las deducciones. |
| `net` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | driver_liquidation_status_enum | sí |  |  | `'draft'::driver_liquidation_status_enum` | _(sin descripción documentada en el código)_ |
| `approved_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `approved_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `paid_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `paid_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `voided_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `cash_movement_id` | uuid | no | FK | `cash_movement.movement_id` |  | _(sin descripción documentada en el código)_ |
| `created_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`liquidation_id`, `distributor_id`), (`distributor_id`, `number`).

Restricciones `CHECK`:
- `CHK_driver_liquidation_anulada`: `CHECK (((status = 'voided'::driver_liquidation_status_enum) = (voided_at IS NOT NULL)))`
- `CHK_driver_liquidation_aprobada`: `CHECK (((status <> ALL (ARRAY['approved'::driver_liquidation_status_enum, 'paid'::driver_liquidation_status_enum])) OR (approved_at IS NOT NULL)))`
- `CHK_driver_liquidation_montos`: `CHECK (((gross >= (0)::numeric) AND (deductions >= (0)::numeric) AND (net = (gross - deductions))))`
- `CHK_driver_liquidation_pagada`: `CHECK (((status = 'paid'::driver_liquidation_status_enum) = (paid_at IS NOT NULL)))`
- `CHK_driver_liquidation_periodo`: `CHECK ((period_from <= period_to))`

Índices (además de la clave primaria):
- `EXC_driver_liquidation_periodo_solapado`: `CREATE INDEX "EXC_driver_liquidation_periodo_solapado" ON public.driver_liquidation USING gist (employee_id, daterange(period_from, period_to, '[]'::text)) WHERE (status <> 'voided'::driver_liquidation_status_enum)`
- `IDX_driver_liquidation_distributor`: `CREATE INDEX "IDX_driver_liquidation_distributor" ON public.driver_liquidation USING btree (distributor_id)`
- `IDX_driver_liquidation_empleado`: `CREATE INDEX "IDX_driver_liquidation_empleado" ON public.driver_liquidation USING btree (employee_id, status)`
- `UQ_driver_liquidation_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_driver_liquidation_id_distribuidora" ON public.driver_liquidation USING btree (liquidation_id, distributor_id)`
- `UQ_driver_liquidation_numero`: `CREATE UNIQUE INDEX "UQ_driver_liquidation_numero" ON public.driver_liquidation USING btree (distributor_id, number)`

### `driver_settlement` — RendicionChofer

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `settlement_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `delivery_id` | uuid | sí | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `number` | integer | sí |  |  |  | Número correlativo por distribuidora (`document_sequence`). |
| `truck_load_id` | uuid | no | FK | `truck_load.load_id` |  | _(sin descripción documentada en el código)_ |
| `business_date` | date | sí |  |  |  | Día de negocio en hora argentina (YYYY-MM-DD). |
| `status` | driver_settlement_status_enum | sí |  |  | `'open'::driver_settlement_status_enum` | _(sin descripción documentada en el código)_ |
| `expected_cash` | numeric(12,2) | sí |  |  | `'0'::numeric` | Efectivo que el chofer debería entregar. Se recalcula al presentar. |
| `declared_cash` | numeric(12,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `driver_expenses` | numeric(12,2) | sí |  |  | `'0'::numeric` | Gastos que el chofer pagó con la cobranza (combustible, peaje). |
| `difference` | numeric(12,2) | no |  |  |  | Declarado + gastos − esperado: negativa es faltante, positiva sobrante. |
| `difference_resolution` | driver_settlement_difference_resolution_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `destination_cash_box_id` | uuid | no | FK | `cash_box.cash_box_id` |  | _(sin descripción documentada en el código)_ |
| `cash_movement_id` | uuid | no | FK | `cash_movement.movement_id` |  | _(sin descripción documentada en el código)_ |
| `submitted_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `submitted_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `approved_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `approved_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `overdue_alerted_at` | timestamptz | no |  |  |  | Cuándo se avisó por mail que quedó sin cerrar; evita repetir el aviso. |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`delivery_id`, `business_date`), (`distributor_id`, `number`).

Restricciones `CHECK`:
- `CHK_driver_settlement_aprobada`: `CHECK (((status = 'approved'::driver_settlement_status_enum) = (approved_at IS NOT NULL)))`
- `CHK_driver_settlement_diferencia`: `CHECK (((difference IS NULL) OR (difference = ((declared_cash + driver_expenses) - expected_cash))))`
- `CHK_driver_settlement_montos`: `CHECK (((expected_cash >= (0)::numeric) AND (driver_expenses >= (0)::numeric) AND ((declared_cash IS NULL) OR (declared_cash >= (0)::numeric))))`
- `CHK_driver_settlement_presentada`: `CHECK (((status = 'open'::driver_settlement_status_enum) OR ((submitted_at IS NOT NULL) AND (declared_cash IS NOT NULL))))`

Índices (además de la clave primaria):
- `IDX_driver_settlement_chofer`: `CREATE INDEX "IDX_driver_settlement_chofer" ON public.driver_settlement USING btree (delivery_id)`
- `IDX_driver_settlement_estado`: `CREATE INDEX "IDX_driver_settlement_estado" ON public.driver_settlement USING btree (distributor_id, status)`
- `IDX_driver_settlement_fecha`: `CREATE INDEX "IDX_driver_settlement_fecha" ON public.driver_settlement USING btree (distributor_id, business_date)`
- `UQ_driver_settlement_carga`: `CREATE UNIQUE INDEX "UQ_driver_settlement_carga" ON public.driver_settlement USING btree (truck_load_id) WHERE (truck_load_id IS NOT NULL)`
- `UQ_driver_settlement_chofer_dia`: `CREATE UNIQUE INDEX "UQ_driver_settlement_chofer_dia" ON public.driver_settlement USING btree (delivery_id, business_date)`
- `UQ_driver_settlement_numero`: `CREATE UNIQUE INDEX "UQ_driver_settlement_numero" ON public.driver_settlement USING btree (distributor_id, number)`

### `driver_settlement_collection` — CobroDeRendicion

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `collection_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `settlement_id` | uuid | sí | FK | `driver_settlement.settlement_id` |  | _(sin descripción documentada en el código)_ |
| `entry_id` | uuid | sí | FK | `customer_account_entry.entry_id` |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_driver_settlement_collection_importe`: `CHECK ((amount > (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_driver_settlement_collection_rendicion`: `CREATE INDEX "IDX_driver_settlement_collection_rendicion" ON public.driver_settlement_collection USING btree (settlement_id)`
- `UQ_driver_settlement_collection_asiento`: `CREATE UNIQUE INDEX "UQ_driver_settlement_collection_asiento" ON public.driver_settlement_collection USING btree (entry_id)`

### `driver_settlement_expense` — GastoDeRendicion

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `expense_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `settlement_id` | uuid | sí | FK | `driver_settlement.settlement_id` |  | _(sin descripción documentada en el código)_ |
| `category_id` | uuid | sí | FK | `cash_category.category_id` |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `description` | varchar(255) | no |  |  |  | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_driver_settlement_expense_importe`: `CHECK ((amount > (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_driver_settlement_expense_rendicion`: `CREATE INDEX "IDX_driver_settlement_expense_rendicion" ON public.driver_settlement_expense USING btree (settlement_id)`

### `driver_settlement_order` — PedidoRendido

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `settlement_order_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `settlement_id` | uuid | sí | FK | `driver_settlement.settlement_id` |  | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(12,2) | sí |  |  |  | Lo que el chofer cobraba: el total menos la seña ya paga. |
| `payment_method` | varchar(20) | sí |  |  |  | Medio de pago del pedido al rendirlo (copia). |

Restricciones `CHECK`:
- `CHK_driver_settlement_order_importe`: `CHECK ((amount >= (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_driver_settlement_order_rendicion`: `CREATE INDEX "IDX_driver_settlement_order_rendicion" ON public.driver_settlement_order USING btree (settlement_id)`
- `UQ_driver_settlement_order_pedido`: `CREATE UNIQUE INDEX "UQ_driver_settlement_order_pedido" ON public.driver_settlement_order USING btree (order_id)`

### `employee` — Empleado

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `employee_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `position_id` | uuid | sí | FK | `job_position.position_id` |  | _(sin descripción documentada en el código)_ |
| `file_number` | varchar(20) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `first_name` | varchar(80) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `last_name` | varchar(80) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `document_type` | employee_document_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `document_number` | varchar(20) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `cuil` | varchar(11) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `birth_date` | date | no |  |  |  | _(sin descripción documentada en el código)_ |
| `address_line` | varchar(200) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `city` | varchar(80) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `province` | varchar(80) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `postal_code` | varchar(10) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `phone` | varchar(30) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `personal_email` | varchar(120) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `emergency_contact_name` | varchar(120) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `emergency_contact_phone` | varchar(30) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `emergency_contact_relationship` | varchar(40) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `hire_date` | date | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `termination_date` | date | no |  |  |  | _(sin descripción documentada en el código)_ |
| `termination_reason` | employee_termination_reason_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `employment_type` | employment_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | employee_status_enum | sí |  |  | `'active'::employee_status_enum` | _(sin descripción documentada en el código)_ |
| `bank_cbu` | varchar(22) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | Sólo para altas erróneas; la salida normal es el egreso. |
| `photo_key` | varchar(512) | no |  |  |  | Key de la foto del legajo en el bucket (`employees/{distribuidora}/{legajo}/{uuid}.{ext}`). Sólo la usa un legajo SIN cuenta: con cuenta, la foto es la del usuario. |

Claves únicas compuestas: (`employee_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_employee_cbu`: `CHECK (((bank_cbu IS NULL) OR ((bank_cbu)::text ~ '^[0-9]{22}$'::text)))`
- `CHK_employee_cuil`: `CHECK (((cuil IS NULL) OR es_cuil_valido((cuil)::text)))`
- `CHK_employee_email`: `CHECK (((personal_email IS NULL) OR ((personal_email)::text ~* '^[^@[:space:]]+@[^@[:space:]]+[.][^@[:space:]]+$'::text)))`
- `CHK_employee_nacimiento`: `CHECK (((birth_date IS NULL) OR (birth_date < hire_date)))`
- `CHK_employee_status_termination`: `CHECK (((status = 'terminated'::employee_status_enum) = (termination_date IS NOT NULL)))`
- `CHK_employee_termination_date`: `CHECK (((termination_date IS NULL) OR (termination_date >= hire_date)))`

Índices (además de la clave primaria):
- `IDX_employee_name`: `CREATE INDEX "IDX_employee_name" ON public.employee USING btree (distributor_id, last_name, first_name)`
- `IDX_employee_position`: `CREATE INDEX "IDX_employee_position" ON public.employee USING btree (position_id)`
- `IDX_employee_status`: `CREATE INDEX "IDX_employee_status" ON public.employee USING btree (distributor_id, status)`
- `UQ_employee_cuil_vigente`: `CREATE UNIQUE INDEX "UQ_employee_cuil_vigente" ON public.employee USING btree (distributor_id, cuil) WHERE ((cuil IS NOT NULL) AND ("deletedAt" IS NULL))`
- `UQ_employee_document_vigente`: `CREATE UNIQUE INDEX "UQ_employee_document_vigente" ON public.employee USING btree (distributor_id, document_number) WHERE ("deletedAt" IS NULL)`
- `UQ_employee_file_number_vigente`: `CREATE UNIQUE INDEX "UQ_employee_file_number_vigente" ON public.employee USING btree (distributor_id, file_number) WHERE ("deletedAt" IS NULL)`
- `UQ_employee_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_employee_id_distribuidora" ON public.employee USING btree (employee_id, distributor_id)`
- `UQ_employee_user_vigente`: `CREATE UNIQUE INDEX "UQ_employee_user_vigente" ON public.employee USING btree (user_id) WHERE ((user_id IS NOT NULL) AND ("deletedAt" IS NULL))`

### `employee_attendance` — JornadaDeTrabajo

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `attendance_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `employee_id` | uuid | sí | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `work_date` | date | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `check_in_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `check_out_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `source` | employee_attendance_source_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `recorded_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_employee_attendance_period`: `CHECK (((check_out_at IS NULL) OR (check_out_at > check_in_at)))`

Índices (además de la clave primaria):
- `EXC_employee_attendance_solapada`: `CREATE INDEX "EXC_employee_attendance_solapada" ON public.employee_attendance USING gist (employee_id, tstzrange(check_in_at, COALESCE(check_out_at, 'infinity'::timestamp with time zone)))`
- `IDX_employee_attendance_day`: `CREATE INDEX "IDX_employee_attendance_day" ON public.employee_attendance USING btree (distributor_id, work_date)`
- `IDX_employee_attendance_employee`: `CREATE INDEX "IDX_employee_attendance_employee" ON public.employee_attendance USING btree (employee_id, work_date)`
- `UQ_employee_attendance_abierta`: `CREATE UNIQUE INDEX "UQ_employee_attendance_abierta" ON public.employee_attendance USING btree (employee_id) WHERE (check_out_at IS NULL)`

### `employee_leave` — LicenciaLaboral

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `leave_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `employee_id` | uuid | sí | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `type` | employee_leave_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `start_date` | date | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `end_date` | date | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `days` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | employee_leave_status_enum | sí |  |  | `'requested'::employee_leave_status_enum` | _(sin descripción documentada en el código)_ |
| `reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `rejection_reason` | text | no |  |  |  | Por qué se rechazó (obligatorio al rechazar). |
| `requested_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `decided_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `decided_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_employee_leave_period`: `CHECK ((end_date >= start_date))`

Índices (además de la clave primaria):
- `IDX_employee_leave_distributor`: `CREATE INDEX "IDX_employee_leave_distributor" ON public.employee_leave USING btree (distributor_id, status)`
- `IDX_employee_leave_employee`: `CREATE INDEX "IDX_employee_leave_employee" ON public.employee_leave USING btree (employee_id, status, start_date, end_date)`

### `fuel_load` — CargaCombustible

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `fuel_load_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | sí | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `employee_id` | uuid | no | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `loaded_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `fuel_type` | fuel_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `liters` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `unit_price` | numeric(12,3) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `total_amount` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `odometer_km` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `is_full_tank` | boolean | sí |  |  | `true` | El consumo se mide entre cargas de tanque lleno. |
| `station` | varchar(120) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `payment_method` | fuel_payment_method_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `receipt_number` | varchar(40) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `anomaly` | boolean | sí |  |  | `false` | El consumo del tramo se apartó más de un 25 % del habitual. |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `odometer_correction_note` | text | no |  |  |  | Nota de quien forzó un kilometraje menor que el de la carga anterior. |
| `created_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `cash_movement_id` | uuid | no | FK | `cash_movement.movement_id` |  | _(sin descripción documentada en el código)_ |
| `registered_by_driver` | boolean | sí |  |  | `false` | La registró el chofer desde su app: no elige caja y su medio de pago no se cambia entre efectivo propio y caja. |
| `cash_payment_legacy` | boolean | sí |  |  | `false` | Carga `cash_box` anterior al asiento de caja: se resolvió fuera del libro y no se ofrece para asentar. |

Restricciones `CHECK`:
- `CHK_fuel_load_liters`: `CHECK ((liters > (0)::numeric))`
- `CHK_fuel_load_odometro`: `CHECK ((odometer_km >= 0))`
- `CHK_fuel_load_precio`: `CHECK ((unit_price > (0)::numeric))`
- `CHK_fuel_load_total`: `CHECK ((total_amount >= (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_fuel_load_car_loaded_at`: `CREATE INDEX "IDX_fuel_load_car_loaded_at" ON public.fuel_load USING btree (car_id, loaded_at)`
- `IDX_fuel_load_distributor_loaded_at`: `CREATE INDEX "IDX_fuel_load_distributor_loaded_at" ON public.fuel_load USING btree (distributor_id, loaded_at)`

### `gas_cylinder` — Producto

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `gas_cylinder_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `type` | varchar(50) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `weight` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `price` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `stock` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `description` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `isActive` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `photo_key` | varchar(512) | no |  |  |  | Key de la imagen del producto en el bucket (`gascylinders/{distribuidora}/{producto}/{uuid}.{ext}`). |
| `average_unit_cost` | numeric(12,2) | no |  |  |  | Costo promedio ponderado de las llenas compradas; lo mantiene la recepción de compras. |
| `reservation_deficit` | integer | sí |  |  | `0` | Unidades reservadas por pedidos abiertos que el físico no cubre (`max(0, reservadas − llenas)`). Lo escribe el módulo de stock cuando una pérdida física deja el vendible en cero: con esto el vendible vale siempre `llenas − reservadas + deficit` y una cancelación o una entrada de llenas primero cubre el déficit en lugar de inflar el vendible (sobreventa). |

Claves únicas compuestas: (`distributor_id`, `type`), (`gas_cylinder_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_gas_cylinder_tipo`: `CHECK ((btrim((type)::text) <> ''::text))`
- `CHK_gas_cylinder_valores`: `CHECK (((price > (0)::numeric) AND (weight > (0)::numeric) AND (stock >= 0) AND (reservation_deficit >= 0) AND ((average_unit_cost IS NULL) OR (average_unit_cost >= (0)::numeric))))`

Índices (además de la clave primaria):
- `IDX_990b829fdf06cb282d835a5d72`: `CREATE INDEX "IDX_990b829fdf06cb282d835a5d72" ON public.gas_cylinder USING btree (distributor_id)`
- `UQ_gas_cylinder_distribuidora_tipo`: `CREATE UNIQUE INDEX "UQ_gas_cylinder_distribuidora_tipo" ON public.gas_cylinder USING btree (distributor_id, type)`
- `UQ_gas_cylinder_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_gas_cylinder_id_distribuidora" ON public.gas_cylinder USING btree (gas_cylinder_id, distributor_id)`
- `UQ_gas_cylinder_tipo_normalizado`: `CREATE UNIQUE INDEX "UQ_gas_cylinder_tipo_normalizado" ON public.gas_cylinder USING btree (distributor_id, lower(btrim((type)::text)))`

### `gas_cylinder_promotion` — Promocion

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `promotion_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `quantity` | integer | sí |  |  |  | Unidades desde las que aplica. |
| `discount_percentage` | numeric(5,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_promocion_cantidad`: `CHECK ((quantity >= 2))`
- `CHK_promocion_descuento`: `CHECK (((discount_percentage > (0)::numeric) AND (discount_percentage <= (99)::numeric)))`

Índices (además de la clave primaria):
- `UQ_promocion_producto_cantidad`: `CREATE UNIQUE INDEX "UQ_promocion_producto_cantidad" ON public.gas_cylinder_promotion USING btree (gas_cylinder_id, quantity) WHERE ("deletedAt" IS NULL)`

### `incident` — Incidencia

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `incident_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `reported_by` | uuid | sí | FK | `user.user_id` |  | Usuario que reporta la incidencia (user_id), normalmente el chofer. |
| `type` | incident_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `description` | text | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `photo_url` | varchar | no |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | incident_status_enum | sí |  |  | `'open'::incident_status_enum` | _(sin descripción documentada en el código)_ |
| `resolution_note` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `resolvedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `moment` | incident_moment_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `photo_key` | varchar(512) | no |  |  |  | Key de la foto de la incidencia en el bucket (`incidents/{distribuidora}/{incidencia}/{uuid}.{ext}`). |

Restricciones `CHECK`:
- `CHK_incident_descripcion`: `CHECK ((btrim(description) <> ''::text))`
- `CHK_incident_largo_de_textos`: `CHECK (((char_length(description) <= 1000) AND ((resolution_note IS NULL) OR (char_length(resolution_note) <= 1000))))`

Índices (además de la clave primaria):
- `IDX_8a89ba6c226022354d0d8b4ada`: `CREATE INDEX "IDX_8a89ba6c226022354d0d8b4ada" ON public.incident USING btree (order_id)`
- `IDX_a2223c18baa97faf54118f95bd`: `CREATE INDEX "IDX_a2223c18baa97faf54118f95bd" ON public.incident USING btree (distributor_id)`
- `UQ_incident_cobro_impago`: `CREATE UNIQUE INDEX "UQ_incident_cobro_impago" ON public.incident USING btree (order_id) WHERE ((type = 'unpaid_collection'::incident_type_enum) AND (status = ANY (ARRAY['open'::incident_status_enum, 'resolved'::incident_status_enum])))`

### `job_position` — PuestoDeTrabajo

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `position_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `name` | varchar(80) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `category` | job_position_category_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `is_active` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_f63c2b78c253c8c92398d88fd5`: `CREATE INDEX "IDX_f63c2b78c253c8c92398d88fd5" ON public.job_position USING btree (distributor_id)`
- `UQ_job_position_name_vigente`: `CREATE UNIQUE INDEX "UQ_job_position_name_vigente" ON public.job_position USING btree (distributor_id, lower((name)::text)) WHERE ("deletedAt" IS NULL)`

### `maintenance_plan` — PlanMantenimiento

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `plan_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `name` | varchar(120) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `subject` | maintenance_subject_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `trigger` | maintenance_trigger_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `interval_km` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `interval_months` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `lead_time_days` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `criticality` | maintenance_criticality_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `car_type` | varchar | no |  |  |  | _(sin descripción documentada en el código)_ |
| `is_active` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `document_kind` | plan_document_kind_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `applies_to_categories` | _varchar | no |  |  |  | Categorías de puesto a las que aplica un plan de personal (CU-183 a CU-185). `null` = a todas. |

Índices (además de la clave primaria):
- `IDX_7ee5533ee6d3b24f7d74a2c61c`: `CREATE INDEX "IDX_7ee5533ee6d3b24f7d74a2c61c" ON public.maintenance_plan USING btree (distributor_id)`

### `maintenance_task` — TareaMantenimiento

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `task_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `plan_id` | uuid | sí | FK | `maintenance_plan.plan_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | no | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `delivery_id` | uuid | no | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `status` | maintenance_task_status_enum | sí |  |  | `'forecast'::maintenance_task_status_enum` | _(sin descripción documentada en el código)_ |
| `due_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `due_km` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `predicted_due_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `scheduled_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `performed_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `odometer_km` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `cost` | numeric(10,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `provider` | varchar(120) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `reference_number` | varchar(60) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `category` | varchar(10) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `alerted_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `valid_from` | timestamptz | no |  |  |  | Inicio de la vigencia del documento (póliza, habilitación). Fecha de calendario, normalizada como `dueAt`. Sin ella, el costo del vehículo prorratea la póliza con un año hacia atrás desde el vencimiento. |
| `employee_id` | uuid | no | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `details` | jsonb | no |  |  |  | Datos propios del tipo de documento (número de certificado, aseguradora, fecha del examen...). La forma la fija `plan.documentKind` (`domain/document-details.ts`). |

Restricciones `CHECK`:
- `CHK_maintenance_task_hecha_fecha`: `CHECK (((status <> 'done'::maintenance_task_status_enum) OR (performed_at IS NOT NULL)))`
- `CHK_maintenance_task_un_sujeto`: `CHECK ((num_nonnulls(car_id, delivery_id, employee_id) = 1))`
- `CHK_maintenance_task_valores`: `CHECK (((COALESCE(cost, (0)::numeric) >= (0)::numeric) AND (COALESCE(due_km, 0) >= 0) AND (COALESCE(odometer_km, 0) >= 0)))`

Índices (además de la clave primaria):
- `IDX_ec96001f6fe2869ae6b40f2dc8`: `CREATE INDEX "IDX_ec96001f6fe2869ae6b40f2dc8" ON public.maintenance_task USING btree (distributor_id)`
- `IDX_maintenance_task_employee`: `CREATE INDEX "IDX_maintenance_task_employee" ON public.maintenance_task USING btree (employee_id)`

### `maintenance_task_attachment` — AdjuntoTarea

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `attachment_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `task_id` | uuid | sí | FK | `maintenance_task.task_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `storage_key` | varchar(255) | sí |  |  |  | Clave del objeto dentro del bucket de S3. |
| `original_name` | varchar(255) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `mime_type` | varchar(100) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `size_bytes` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `uploaded_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `uploaded_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deleted_at` | timestamptz | no |  |  |  | Baja lógica: el registro queda para histórico y el archivo NO se borra del storage (queda de respaldo). Los listados y descargas no lo muestran. |

Índices (además de la clave primaria):
- `IDX_07f53564ec7d34fc7e69b96cab`: `CREATE INDEX "IDX_07f53564ec7d34fc7e69b96cab" ON public.maintenance_task_attachment USING btree (distributor_id)`

### `maintenance_window_proposal` — PropuestaVentanaTaller

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `proposal_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `task_id` | uuid | sí | FK | `maintenance_task.task_id` |  | _(sin descripción documentada en el código)_ |
| `delivery_id` | uuid | sí | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `window_start` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `window_end` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `rank` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | proposal_status_enum | sí |  |  | `'pending'::proposal_status_enum` | _(sin descripción documentada en el código)_ |
| `expires_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `responded_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

### `module_config` — ConfiguracionModulo

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `config_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `module` | configurable_process_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `params` | jsonb | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `updated_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updated_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`distributor_id`, `module`).

Índices (además de la clave primaria):
- `IDX_ba2e1f43e70ba77c13d6844ee8`: `CREATE INDEX "IDX_ba2e1f43e70ba77c13d6844ee8" ON public.module_config USING btree (distributor_id)`
- `UQ_module_config_distributor_module`: `CREATE UNIQUE INDEX "UQ_module_config_distributor_module" ON public.module_config USING btree (distributor_id, module)`

### `order` — Pedido

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `order_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `customer_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `time_slot_id` | uuid | no | FK | `time_slot.time_slot_id` |  | _(sin descripción documentada en el código)_ |
| `scheduled_date` | date | no |  |  |  | Fecha agendada de entrega (YYYY-MM-DD). Null = pedido inmediato ("lo antes posible", comportamiento previo). Con fecha + time_slot_id, el pedido está agendado a esa franja de ese día (valida capacidad al crear). |
| `deposit_amount` | numeric(10,2) | sí |  |  | `'0'::numeric` | Seña de la pre-reserva (0 = pedido normal, no reserva). |
| `deposit_paid` | boolean | sí |  |  | `false` | Si la seña ya fue pagada (habilita la activación automática de la reserva). |
| `delivery_id` | uuid | no | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `address_id` | uuid | sí | FK | `user_address.address_id` |  | _(sin descripción documentada en el código)_ |
| `status` | order_status_enum | sí |  |  | `'pending'::order_status_enum` | _(sin descripción documentada en el código)_ |
| `paymentMethod` | order_paymentmethod_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `paymentType` | order_paymenttype_enum | sí |  |  | `'cash'::order_paymenttype_enum` | _(sin descripción documentada en el código)_ |
| `paymentStatus` | order_paymentstatus_enum | sí |  |  | `'pending'::order_paymentstatus_enum` | _(sin descripción documentada en el código)_ |
| `totalAmount` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `deliveryInstructions` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `acceptedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `onTheWayAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `deliveredAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `cancellationReason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `gatewayPaymentId` | varchar(100) | no |  |  |  | ID del pago en la pasarela (MercadoPago) que marcó este pedido como PAID. Índice único PARCIAL (solo cuando no es null): garantiza idempotencia del webhook — un mismo `payment.id` no puede confirmar dos pedidos, y permite detectar reintentos (si ya está seteado, no se re-despacha). |
| `deliveryCode` | varchar(12) | no |  |  |  | Código secreto de la prueba de entrega con QR. Se genera al ACEPTAR el pedido (ver UpdateOrderStatusUseCase) y viaja embebido en el QR que el chofer muestra en su app. El cliente lo obtiene ÚNICAMENTE escaneando ese QR físico; si al confirmar la entrega el código matchea, es prueba de que el chofer estuvo presente (ConfirmDeliveryUseCase). |
| `receiver_name` | varchar(120) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `receiver_document` | varchar(20) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `receiver_relationship` | varchar(40) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `delivery_mode` | order_delivery_mode_enum | sí |  |  | `'standard'::order_delivery_mode_enum` | _(sin descripción documentada en el código)_ |
| `deliveryPoint` | geometry | no |  |  |  | Dónde se entrega: el punto de la dirección al momento de pedir. Es una copia a propósito, porque la dirección del cliente puede cambiar después (el cambio de dirección de un pedido queda en `order_address_change`). El despacho busca los choferes más cercanos a este punto. La posición del chofer no se guarda acá: vive en Redis (H-91). |
| `coverage_zone_id` | uuid | no | FK | `coverage_zone.coverage_zone_id` |  | _(sin descripción documentada en el código)_ |
| `zone_name` | varchar(120) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `zone_surcharge_type` | order_zone_surcharge_type_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `zone_surcharge_value` | numeric(10,2) | no |  |  |  | Valor crudo de la zona al momento de pedir (monto o %, según el tipo). |
| `zone_surcharge_amount` | numeric(10,2) | sí |  |  | `'0'::numeric` | Recargo YA calculado (monto en la moneda del pedido). 0 si no hay zona. |
| `subtotal_items` | numeric(10,2) | sí |  |  |  | Subtotal de los ítems (ya con promociones), antes de cualquier recargo. |
| `vehicle_car_id` | uuid | no | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `vehicle_patent` | varchar(20) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `vehicle_brand` | varchar(50) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `vehicle_model` | varchar(50) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `payment_confirmed_at` | timestamptz | no |  |  |  | Cuándo se confirmó el cobro (pago recibido por el chofer o resolución del admin). |
| `payment_confirmed_by` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `payment_resolution_note` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `payment_resolved_at` | timestamptz | no |  |  |  | Motivo con el que el admin resolvió un impago. |
| `payment_resolved_by` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `express_surcharge_amount` | numeric(10,2) | sí |  |  | `'0'::numeric` | Recargo express que se cobró al pedir (CU-147). Queda guardado aunque el pedido pase al reparto común (`express_degraded_at`), para poder explicar el total y saber cuánto reintegrar; el `total_amount` ya no lo incluye en ese caso. |
| `express_degraded_at` | timestamptz | no |  |  |  | Cuándo ningún chofer en moto aceptó y el pedido pasó al reparto común (CU-149). |
| `payment_surcharge_amount` | numeric(10,2) | sí |  |  | `'0'::numeric` | Recargo por medio de pago online (+10 % de MercadoPago o transferencia), calculado sobre el subtotal de los ítems más el recargo de zona. 0 si se paga en efectivo o a cuenta. Con el resto de los recargos explica el total (`CHK_order_total_formula`). |

Claves únicas compuestas: (`order_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_order_aceptado_fecha`: `CHECK (((status <> ALL (ARRAY['accepted'::order_status_enum, 'on_the_way'::order_status_enum, 'delivered'::order_status_enum])) OR ("acceptedAt" IS NOT NULL)))`
- `CHK_order_cancelado_motivo`: `CHECK (((status <> 'cancelled'::order_status_enum) OR (btrim(COALESCE("cancellationReason", ''::text)) <> ''::text)))`
- `CHK_order_chofer_asignado`: `CHECK (((status <> ALL (ARRAY['accepted'::order_status_enum, 'on_the_way'::order_status_enum, 'delivered'::order_status_enum])) OR (delivery_id IS NOT NULL)))`
- `CHK_order_en_camino_fecha`: `CHECK (((status <> ALL (ARRAY['on_the_way'::order_status_enum, 'delivered'::order_status_enum])) OR ("onTheWayAt" IS NOT NULL)))`
- `CHK_order_entregado_fecha`: `CHECK (((status = 'delivered'::order_status_enum) = ("deliveredAt" IS NOT NULL)))`
- `CHK_order_montos`: `CHECK ((("totalAmount" >= (0)::numeric) AND (subtotal_items >= (0)::numeric) AND (zone_surcharge_amount >= (0)::numeric) AND (express_surcharge_amount >= (0)::numeric) AND (payment_surcharge_amount >= (0)::numeric) AND (deposit_amount >= (0)::numeric)))`
- `CHK_order_nota_de_impago_largo`: `CHECK (((payment_resolution_note IS NULL) OR ((char_length(payment_resolution_note) <= 500) AND (char_length(btrim(payment_resolution_note)) >= 10))))`
- `CHK_order_pago_coherente`: `CHECK (((("paymentMethod" = 'cash'::order_paymentmethod_enum) = ("paymentType" = 'cash'::order_paymenttype_enum)) AND (("paymentMethod" = 'account'::order_paymentmethod_enum) = ("paymentType" = 'account'::order_paymenttype_enum))))`
- `CHK_order_total_formula`: `CHECK (("totalAmount" = (((subtotal_items + zone_surcharge_amount) + payment_surcharge_amount) + CASE WHEN (express_degraded_at IS NULL) THEN express_surcharge_amount ELSE (0)::numeric END)))`

Índices (además de la clave primaria):
- `IDX_3adf34152c77fdb4e8f7346c5f`: `CREATE UNIQUE INDEX "IDX_3adf34152c77fdb4e8f7346c5f" ON public."order" USING btree ("gatewayPaymentId") WHERE ("gatewayPaymentId" IS NOT NULL)`
- `IDX_775a36a19670c03781e60bbce9`: `CREATE INDEX "IDX_775a36a19670c03781e60bbce9" ON public."order" USING btree (scheduled_date)`
- `IDX_7a9573d6a1fb982772a9123320`: `CREATE INDEX "IDX_7a9573d6a1fb982772a9123320" ON public."order" USING btree (status)`
- `IDX_cd7812c96209c5bdd48a6b858b`: `CREATE INDEX "IDX_cd7812c96209c5bdd48a6b858b" ON public."order" USING btree (customer_id)`
- `IDX_df56039592a4bbbd3fa4a19f14`: `CREATE INDEX "IDX_df56039592a4bbbd3fa4a19f14" ON public."order" USING btree (distributor_id)`
- `IDX_f437a76442f23c89ad7652b2a4`: `CREATE INDEX "IDX_f437a76442f23c89ad7652b2a4" ON public."order" USING btree ("deliveredAt")`
- `UQ_order_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_order_id_distribuidora" ON public."order" USING btree (order_id, distributor_id)`
- `idx_order_dist_status_delivered`: `CREATE INDEX idx_order_dist_status_delivered ON public."order" USING btree (distributor_id, status, "deliveredAt")`
- `idx_order_status_delivery`: `CREATE INDEX idx_order_status_delivery ON public."order" USING btree (status, delivery_id)`

### `order_address_change` — CambioDireccion

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `change_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `from_address_id` | uuid | sí | FK | `user_address.address_id` |  | _(sin descripción documentada en el código)_ |
| `to_address_id` | uuid | sí | FK | `user_address.address_id` |  | _(sin descripción documentada en el código)_ |
| `changed_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `changed_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |

### `order_dispatch_offer` — OfertaDespacho

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `offer_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | Tenant dueño del despacho (denormalizado desde la orden). |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `driver_id` | uuid | sí | FK | `user.user_id` |  | ID del chofer al que se ofreció = `user_id` (el mismo que usa el GEO/WS). |
| `status` | order_dispatch_offer_status_enum | sí |  |  | `'offered'::order_dispatch_offer_status_enum` | _(sin descripción documentada en el código)_ |
| `expiresAt` | timestamptz | sí |  |  |  | Momento hasta el cual la oferta es válida (offered_at + TTL). timestamptz (UTC) para que la comparación `expiresAt < now()` del cron sea correcta sin importar la TZ del servidor — con `timestamp` naive el timeout se rompe. |
| `offeredAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_order_dispatch_offer_vencimiento`: `CHECK (("expiresAt" > "offeredAt"))`

Índices (además de la clave primaria):
- `IDX_1231f4249963aa2efb93749a8e`: `CREATE INDEX "IDX_1231f4249963aa2efb93749a8e" ON public.order_dispatch_offer USING btree (order_id)`
- `IDX_21b60d43f182e2b1e8a30ea0a5`: `CREATE INDEX "IDX_21b60d43f182e2b1e8a30ea0a5" ON public.order_dispatch_offer USING btree (status)`
- `IDX_830f3888d1424414675f1c184d`: `CREATE INDEX "IDX_830f3888d1424414675f1c184d" ON public.order_dispatch_offer USING btree (distributor_id)`
- `IDX_9ff85bc9c62717502d1ad68216`: `CREATE INDEX "IDX_9ff85bc9c62717502d1ad68216" ON public.order_dispatch_offer USING btree ("expiresAt")`
- `UQ_order_dispatch_offer_aceptada`: `CREATE UNIQUE INDEX "UQ_order_dispatch_offer_aceptada" ON public.order_dispatch_offer USING btree (order_id) WHERE (status = 'accepted'::order_dispatch_offer_status_enum)`
- `UQ_order_dispatch_offer_viva`: `CREATE UNIQUE INDEX "UQ_order_dispatch_offer_viva" ON public.order_dispatch_offer USING btree (order_id, driver_id) WHERE (status = 'offered'::order_dispatch_offer_status_enum)`
- `idx_offer_order_status`: `CREATE INDEX idx_offer_order_status ON public.order_dispatch_offer USING btree (order_id, status)`
- `idx_offer_status_expires`: `CREATE INDEX idx_offer_status_expires ON public.order_dispatch_offer USING btree (status, "expiresAt")`

### `order_item` — ItemPedido

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `order_item_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `quantity` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `unitPrice` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `subtotal` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`order_id`, `gas_cylinder_id`).

Restricciones `CHECK`:
- `CHK_order_item_cantidad`: `CHECK ((quantity > 0))`
- `CHK_order_item_importes`: `CHECK ((("unitPrice" >= (0)::numeric) AND (subtotal >= (0)::numeric)))`

Índices (además de la clave primaria):
- `UQ_order_item_pedido_producto`: `CREATE UNIQUE INDEX "UQ_order_item_pedido_producto" ON public.order_item USING btree (order_id, gas_cylinder_id)`

### `order_status_history` — CambioEstadoPedido

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `history_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `from_status` | order_status_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `to_status` | order_status_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `changed_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `changed_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_order_status_history_cancelacion`: `CREATE INDEX "IDX_order_status_history_cancelacion" ON public.order_status_history USING btree (order_id, changed_at) WHERE (to_status = 'cancelled'::order_status_enum)`

### `payment` — Pago

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `payment_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | Pedido al que pertenece este intento de cobro. |
| `distributor_id` | uuid | no | FK | `distributor.distributor_id` |  | Tenant dueño del pago (igual que el pedido). Nullable hasta backfill. |
| `gateway` | payment_gateway_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `integration` | payment_integration_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `method` | varchar(50) | no |  |  |  | Medio de pago concreto dentro de la pasarela (ej. 'credit_card', 'account_money'). |
| `gateway_payment_id` | varchar(100) | no |  |  |  | ID del pago en la pasarela. Null mientras el intento está PENDING (recién se conoce cuando el webhook confirma el pago real). Índice único PARCIAL (solo cuando no es null): un mismo pago de la pasarela no puede confirmar dos registros del ledger — garantiza la idempotencia del webhook del lado del ledger, igual que el índice análogo en `order.gatewayPaymentId`. |
| `external_reference` | varchar | no |  |  |  | Referencia externa enviada a la pasarela (= order_id). |
| `amount` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `currency` | varchar(10) | sí |  |  | `'ARS'::character varying` | _(sin descripción documentada en el código)_ |
| `status` | payment_status_enum | sí |  |  | `'pending'::payment_status_enum` | _(sin descripción documentada en el código)_ |
| `payment_url` | text | no |  |  |  | URL de checkout devuelta por la pasarela (Checkout Pro init_point). |
| `is_deposit` | boolean | sí |  |  | `false` | true = este intento cobra la SEÑA de una reserva, no el pedido completo. |
| `metadata` | jsonb | no |  |  |  | Datos crudos/auxiliares de la pasarela (preferenceId, status crudo, etc.). |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_payment_importe`: `CHECK ((amount > (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_05b8eaefed5471a643ee578c74`: `CREATE UNIQUE INDEX "IDX_05b8eaefed5471a643ee578c74" ON public.payment USING btree (gateway_payment_id) WHERE (gateway_payment_id IS NOT NULL)`
- `IDX_0cdad15fa39dd1ebace139096f`: `CREATE INDEX "IDX_0cdad15fa39dd1ebace139096f" ON public.payment USING btree (distributor_id)`
- `IDX_f5221735ace059250daac9d980`: `CREATE INDEX "IDX_f5221735ace059250daac9d980" ON public.payment USING btree (order_id)`

### `payment_refund` — ReintegroDePago

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `refund_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `payment_id` | uuid | sí | FK | `payment.payment_id` |  | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | no | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `kind` | payment_refund_kind_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | payment_refund_status_enum | sí |  |  | `'pending'::payment_refund_status_enum` | _(sin descripción documentada en el código)_ |
| `gateway_refund_id` | varchar(100) | no |  |  |  | Id de la devolución en la pasarela (null si no la hubo o ya estaba devuelto). |
| `error_message` | text | no |  |  |  | Por qué falló el último intento. |
| `attempts` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `refunded_at` | timestamptz | no |  |  |  | Cuándo la pasarela confirmó la devolución. |
| `requested_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `refunded_baseline` | numeric(10,2) | no |  |  |  | Lo que la pasarela ya había devuelto del pago antes del último intento: permite saber, después de un corte o un timeout, si ese intento se aplicó. |

Claves únicas compuestas: (`payment_id`, `kind`).

Restricciones `CHECK`:
- `CHK_payment_refund_exito_fecha`: `CHECK (((status <> 'succeeded'::payment_refund_status_enum) OR (refunded_at IS NOT NULL)))`
- `CHK_payment_refund_importe`: `CHECK ((amount > (0)::numeric))`
- `CHK_payment_refund_intentos`: `CHECK ((attempts >= 0))`

Índices (además de la clave primaria):
- `IDX_9649d0833082fad8f431ff1381`: `CREATE INDEX "IDX_9649d0833082fad8f431ff1381" ON public.payment_refund USING btree (distributor_id)`
- `IDX_9b1ba9fb797de22fc87b598f50`: `CREATE INDEX "IDX_9b1ba9fb797de22fc87b598f50" ON public.payment_refund USING btree (payment_id)`
- `IDX_a2ae8bef86602c9f97be8e0b41`: `CREATE INDEX "IDX_a2ae8bef86602c9f97be8e0b41" ON public.payment_refund USING btree (status)`
- `IDX_ddf9b0a3d9abeee97fa77f0f20`: `CREATE INDEX "IDX_ddf9b0a3d9abeee97fa77f0f20" ON public.payment_refund USING btree (order_id)`
- `UQ_payment_refund_payment_kind`: `CREATE UNIQUE INDEX "UQ_payment_refund_payment_kind" ON public.payment_refund USING btree (payment_id, kind)`

### `purchase_order` — OrdenDeCompra

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `purchase_order_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `number` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `supplier_id` | uuid | sí | FK | `supplier.supplier_id` |  | _(sin descripción documentada en el código)_ |
| `destination_warehouse_id` | uuid | sí | FK | `warehouse.warehouse_id` |  | _(sin descripción documentada en el código)_ |
| `status` | purchase_order_status_enum | sí |  |  | `'draft'::purchase_order_status_enum` | _(sin descripción documentada en el código)_ |
| `issued_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `expected_date` | date | no |  |  |  | Fecha calendario `YYYY-MM-DD`. |
| `total_amount` | numeric(12,2) | sí |  |  | `'0'::numeric` | _(sin descripción documentada en el código)_ |
| `cancel_reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `created_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `close_reason` | text | no |  |  |  | Motivo del cierre con faltante (`closed_short`). |

Claves únicas compuestas: (`purchase_order_id`, `distributor_id`), (`distributor_id`, `number`).

Restricciones `CHECK`:
- `CHK_purchase_order_cancelada`: `CHECK (((status <> 'cancelled'::purchase_order_status_enum) OR (cancel_reason IS NOT NULL)))`
- `CHK_purchase_order_cerrada_corta`: `CHECK (((status <> 'closed_short'::purchase_order_status_enum) OR (close_reason IS NOT NULL)))`
- `CHK_purchase_order_emitida`: `CHECK (((status = ANY (ARRAY['draft'::purchase_order_status_enum, 'cancelled'::purchase_order_status_enum])) OR (issued_at IS NOT NULL)))`
- `CHK_purchase_order_fecha_esperada`: `CHECK (((expected_date IS NULL) OR (expected_date >= (("createdAt" AT TIME ZONE 'America/Argentina/Buenos_Aires'::text))::date)))`
- `CHK_purchase_order_total`: `CHECK ((total_amount >= (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_purchase_order_estado`: `CREATE INDEX "IDX_purchase_order_estado" ON public.purchase_order USING btree (distributor_id, status)`
- `IDX_purchase_order_proveedor`: `CREATE INDEX "IDX_purchase_order_proveedor" ON public.purchase_order USING btree (supplier_id)`
- `UQ_purchase_order_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_purchase_order_id_distribuidora" ON public.purchase_order USING btree (purchase_order_id, distributor_id)`
- `UQ_purchase_order_numero`: `CREATE UNIQUE INDEX "UQ_purchase_order_numero" ON public.purchase_order USING btree (distributor_id, number)`

### `purchase_order_item` — ItemOrdenDeCompra

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `item_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `purchase_order_id` | uuid | sí | FK | `purchase_order.purchase_order_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `quantity` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `unit_cost` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `empties_to_exchange` | integer | sí |  |  | `0` | Vacíos que se entregan a la planta a cambio de las llenas. |
| `received_quantity` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`purchase_order_id`, `gas_cylinder_id`).

Restricciones `CHECK`:
- `CHK_purchase_order_item_cantidad`: `CHECK ((quantity > 0))`
- `CHK_purchase_order_item_costo`: `CHECK ((unit_cost >= (0)::numeric))`
- `CHK_purchase_order_item_recibido`: `CHECK (((received_quantity >= 0) AND (received_quantity <= quantity)))`
- `CHK_purchase_order_item_vacios`: `CHECK ((empties_to_exchange >= 0))`

Índices (además de la clave primaria):
- `IDX_purchase_order_item_garrafa`: `CREATE INDEX "IDX_purchase_order_item_garrafa" ON public.purchase_order_item USING btree (gas_cylinder_id)`
- `UQ_purchase_order_item_garrafa`: `CREATE UNIQUE INDEX "UQ_purchase_order_item_garrafa" ON public.purchase_order_item USING btree (purchase_order_id, gas_cylinder_id)`

### `purchase_receipt` — RecepcionDeCompra

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `receipt_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `number` | integer | sí |  |  |  | Número interno correlativo por distribuidora. |
| `supplier_id` | uuid | sí | FK | `supplier.supplier_id` |  | _(sin descripción documentada en el código)_ |
| `purchase_order_id` | uuid | no | FK | `purchase_order.purchase_order_id` |  | _(sin descripción documentada en el código)_ |
| `warehouse_id` | uuid | sí | FK | `warehouse.warehouse_id` |  | _(sin descripción documentada en el código)_ |
| `supplier_document_type` | supplier_document_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `supplier_document_number` | varchar(30) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `received_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `received_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `total_amount` | numeric(12,2) | sí |  |  | `'0'::numeric` | _(sin descripción documentada en el código)_ |
| `payment_status` | purchase_payment_status_enum | sí |  |  | `'unpaid'::purchase_payment_status_enum` | _(sin descripción documentada en el código)_ |
| `cash_movement_id` | uuid | no | FK | `cash_movement.movement_id` |  | _(sin descripción documentada en el código)_ |
| `status` | purchase_receipt_status_enum | sí |  |  | `'confirmed'::purchase_receipt_status_enum` | _(sin descripción documentada en el código)_ |
| `void_reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `voided_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `voided_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `batch_id` | uuid | sí |  |  |  | Lote del libro de movimientos que generó la recepción. |
| `void_batch_id` | uuid | no |  |  |  | Lote del contraasiento, si se anuló. |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`distributor_id`, `number`), (`distributor_id`, `supplier_id`, `supplier_document_type`, `supplier_document_number`).

Restricciones `CHECK`:
- `CHK_purchase_receipt_anulacion_datos`: `CHECK (((status <> 'voided'::purchase_receipt_status_enum) OR ((void_reason IS NOT NULL) AND (voided_by_user_id IS NOT NULL))))`
- `CHK_purchase_receipt_anulada_fecha`: `CHECK (((status = 'voided'::purchase_receipt_status_enum) = (voided_at IS NOT NULL)))`
- `CHK_purchase_receipt_total`: `CHECK ((total_amount >= (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_purchase_receipt_fecha`: `CREATE INDEX "IDX_purchase_receipt_fecha" ON public.purchase_receipt USING btree (distributor_id, received_at)`
- `IDX_purchase_receipt_orden`: `CREATE INDEX "IDX_purchase_receipt_orden" ON public.purchase_receipt USING btree (purchase_order_id)`
- `IDX_purchase_receipt_proveedor`: `CREATE INDEX "IDX_purchase_receipt_proveedor" ON public.purchase_receipt USING btree (supplier_id)`
- `UQ_purchase_receipt_documento_proveedor`: `CREATE UNIQUE INDEX "UQ_purchase_receipt_documento_proveedor" ON public.purchase_receipt USING btree (distributor_id, supplier_id, supplier_document_type, supplier_document_number)`
- `UQ_purchase_receipt_numero`: `CREATE UNIQUE INDEX "UQ_purchase_receipt_numero" ON public.purchase_receipt USING btree (distributor_id, number)`

### `purchase_receipt_item` — ItemRecepcion

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `item_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `receipt_id` | uuid | sí | FK | `purchase_receipt.receipt_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `quantity_full` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `quantity_empty_out` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `unit_cost` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `previous_average_cost` | numeric(12,2) | no |  |  |  | Costo promedio de la garrafa justo antes de esta recepción (para deshacerlo al anular). |
| `previous_on_hand` | integer | no |  |  |  | Llenas en depósitos y camiones justo antes de esta recepción. |
| `previous_on_hand_at` | timestamptz | no |  |  |  | Instante (reloj de la base, bajo el lock de la garrafa) en que se leyó `previous_on_hand`. Ordena la recepción contra las anulaciones al recalcular el costo promedio; `createdAt` no sirve: es el inicio de la transacción. |

Claves únicas compuestas: (`receipt_id`, `gas_cylinder_id`).

Restricciones `CHECK`:
- `CHK_purchase_receipt_item_cantidades`: `CHECK (((quantity_full >= 0) AND (quantity_empty_out >= 0) AND ((quantity_full + quantity_empty_out) > 0)))`
- `CHK_purchase_receipt_item_costo`: `CHECK ((unit_cost >= (0)::numeric))`

Índices (además de la clave primaria):
- `IDX_purchase_receipt_item_garrafa`: `CREATE INDEX "IDX_purchase_receipt_item_garrafa" ON public.purchase_receipt_item USING btree (gas_cylinder_id)`
- `UQ_purchase_receipt_item_garrafa`: `CREATE UNIQUE INDEX "UQ_purchase_receipt_item_garrafa" ON public.purchase_receipt_item USING btree (receipt_id, gas_cylinder_id)`

### `rating` — Calificacion

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `rating_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `from_user_id` | uuid | sí | FK | `user.user_id` |  | Usuario que emite la calificación (user_id). |
| `to_user_id` | uuid | sí | FK | `user.user_id` |  | Usuario calificado (el otro lado del pedido) (user_id). |
| `from_role` | rating_from_role_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `stars` | integer | sí |  |  |  | 1 a 5 estrellas. |
| `comment` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `hidden` | boolean | sí |  |  | `false` | Moderación: una calificación oculta no cuenta en promedios ni resúmenes ni se muestra a clientes; el admin la ve marcada. Nunca se borra. |
| `hidden_reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `hidden_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `hidden_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`order_id`, `from_role`).

Restricciones `CHECK`:
- `CHK_rating_largo_de_textos`: `CHECK ((((comment IS NULL) OR (char_length(comment) <= 500)) AND ((hidden_reason IS NULL) OR (char_length(hidden_reason) <= 500))))`
- `CHK_rating_valores`: `CHECK ((((stars >= 1) AND (stars <= 5)) AND (from_user_id <> to_user_id) AND ((NOT hidden) OR (hidden_at IS NOT NULL))))`

Índices (además de la clave primaria):
- `IDX_6f590ebbc097c4ed21d5d3e11e`: `CREATE INDEX "IDX_6f590ebbc097c4ed21d5d3e11e" ON public.rating USING btree (to_user_id)`
- `IDX_b46b63fc1ddf2135e1ed37069a`: `CREATE INDEX "IDX_b46b63fc1ddf2135e1ed37069a" ON public.rating USING btree (distributor_id)`
- `IDX_beb6f44b22a7f1ed7cad984a2e`: `CREATE INDEX "IDX_beb6f44b22a7f1ed7cad984a2e" ON public.rating USING btree (order_id)`
- `IDX_f5df1954571306276a5db7930f`: `CREATE INDEX "IDX_f5df1954571306276a5db7930f" ON public.rating USING btree (hidden)`
- `UQ_rating_order_role`: `CREATE UNIQUE INDEX "UQ_rating_order_role" ON public.rating USING btree (order_id, from_role)`

### `repurchase_invitation` — InvitacionRecompra

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `invitation_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `address_id` | uuid | no | FK | `user_address.address_id` |  | _(sin descripción documentada en el código)_ |
| `projected_depletion_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `suggested_items` | jsonb | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | repurchase_invitation_status_enum | sí |  |  | `'pending'::repurchase_invitation_status_enum` | _(sin descripción documentada en el código)_ |
| `expires_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `responded_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | no | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `created_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_17f0b53699f596f5eb43c0374f`: `CREATE INDEX "IDX_17f0b53699f596f5eb43c0374f" ON public.repurchase_invitation USING btree (user_id)`
- `IDX_ec297644c2db0dab5171e00f1f`: `CREATE INDEX "IDX_ec297644c2db0dab5171e00f1f" ON public.repurchase_invitation USING btree (distributor_id)`

### `role` — Rol

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `role_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `type` | text | sí |  |  |  | El código busca los roles por este texto: tiene que ser único. |
| `createdAt` | timestamptz | no |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | no |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | Baja lógica: el rol queda para histórico y deja de aparecer. |

Índices (además de la clave primaria):
- `UQ_role_type_vigente`: `CREATE UNIQUE INDEX "UQ_role_type_vigente" ON public.role USING btree (type) WHERE ("deletedAt" IS NULL)`

### `route_batch` — LoteRecorrido

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `batch_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `status` | route_batch_status_enum | sí |  |  | `'forming'::route_batch_status_enum` | _(sin descripción documentada en el código)_ |
| `total_weight_kg` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `delivery_id` | uuid | no | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `created_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_39b785b153c83c123bd9d19998`: `CREATE INDEX "IDX_39b785b153c83c123bd9d19998" ON public.route_batch USING btree (distributor_id)`

### `route_batch_offer` — OfertaLote

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `offer_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `batch_id` | uuid | sí | FK | `route_batch.batch_id` |  | _(sin descripción documentada en el código)_ |
| `delivery_id` | uuid | sí | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `status` | proposal_status_enum | sí |  |  | `'pending'::proposal_status_enum` | _(sin descripción documentada en el código)_ |
| `expires_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `responded_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

### `route_batch_stop` — ParadaLote

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `stop_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `batch_id` | uuid | sí | FK | `route_batch.batch_id` |  | _(sin descripción documentada en el código)_ |
| `order_id` | uuid | sí | FK | `order.order_id` |  | _(sin descripción documentada en el código)_ |
| `sequence` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`batch_id`, `order_id`), (`batch_id`, `sequence`).

Restricciones `CHECK`:
- `CHK_route_batch_stop_secuencia`: `CHECK ((sequence >= 1))`

Índices (además de la clave primaria):
- `UQ_route_batch_stop_batch_order`: `CREATE UNIQUE INDEX "UQ_route_batch_stop_batch_order" ON public.route_batch_stop USING btree (batch_id, order_id)`
- `UQ_route_batch_stop_secuencia`: `CREATE UNIQUE INDEX "UQ_route_batch_stop_secuencia" ON public.route_batch_stop USING btree (batch_id, sequence)`

### `stock_adjustment` — AjusteDeStock

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `adjustment_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `number` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `location_id` | uuid | sí | FK | `stock_location.location_id` |  | _(sin descripción documentada en el código)_ |
| `reason` | stock_adjustment_reason_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `notes` | text | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `batch_id` | uuid | sí |  |  |  | El lote del libro de movimientos que generó este ajuste. |
| `created_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`distributor_id`, `number`).

Restricciones `CHECK`:
- `CHK_stock_adjustment_notas`: `CHECK ((btrim(notes) <> ''::text))`

Índices (además de la clave primaria):
- `IDX_stock_adjustment_fecha`: `CREATE INDEX "IDX_stock_adjustment_fecha" ON public.stock_adjustment USING btree (distributor_id, "createdAt")`
- `IDX_stock_adjustment_ubicacion`: `CREATE INDEX "IDX_stock_adjustment_ubicacion" ON public.stock_adjustment USING btree (location_id)`
- `UQ_stock_adjustment_numero`: `CREATE UNIQUE INDEX "UQ_stock_adjustment_numero" ON public.stock_adjustment USING btree (distributor_id, number)`

### `stock_adjustment_item` — ItemAjusteDeStock

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `item_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `adjustment_id` | uuid | sí | FK | `stock_adjustment.adjustment_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `condition` | stock_condition_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `quantity_delta` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`adjustment_id`, `gas_cylinder_id`, `condition`).

Restricciones `CHECK`:
- `CHK_stock_adjustment_item_variacion`: `CHECK ((quantity_delta <> 0))`

Índices (además de la clave primaria):
- `UQ_stock_adjustment_item_garrafa_condicion`: `CREATE UNIQUE INDEX "UQ_stock_adjustment_item_garrafa_condicion" ON public.stock_adjustment_item USING btree (adjustment_id, gas_cylinder_id, condition)`

### `stock_balance` — SaldoDeStock

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `balance_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `location_id` | uuid | sí | FK | `stock_location.location_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `condition` | stock_condition_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `quantity` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`location_id`, `gas_cylinder_id`, `condition`).

Restricciones `CHECK`:
- `CHK_stock_balance_no_negativo`: `CHECK ((quantity >= 0))`

Índices (además de la clave primaria):
- `IDX_stock_balance_distributor`: `CREATE INDEX "IDX_stock_balance_distributor" ON public.stock_balance USING btree (distributor_id)`
- `IDX_stock_balance_gas_cylinder`: `CREATE INDEX "IDX_stock_balance_gas_cylinder" ON public.stock_balance USING btree (gas_cylinder_id)`
- `UQ_stock_balance_ubicacion_garrafa_condicion`: `CREATE UNIQUE INDEX "UQ_stock_balance_ubicacion_garrafa_condicion" ON public.stock_balance USING btree (location_id, gas_cylinder_id, condition)`

### `stock_location` — UbicacionDeStock

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `location_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `kind` | stock_location_kind_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `warehouse_id` | uuid | no | FK | `warehouse.warehouse_id` |  | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | no | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`location_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_stock_location_kind`: `CHECK (((kind = 'warehouse'::stock_location_kind_enum) = (warehouse_id IS NOT NULL)))`
- `CHK_stock_location_one_owner`: `CHECK ((num_nonnulls(warehouse_id, car_id) = 1))`

Índices (además de la clave primaria):
- `IDX_stock_location_distributor`: `CREATE INDEX "IDX_stock_location_distributor" ON public.stock_location USING btree (distributor_id)`
- `UQ_stock_location_car`: `CREATE UNIQUE INDEX "UQ_stock_location_car" ON public.stock_location USING btree (car_id)`
- `UQ_stock_location_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_stock_location_id_distribuidora" ON public.stock_location USING btree (location_id, distributor_id)`
- `UQ_stock_location_warehouse`: `CREATE UNIQUE INDEX "UQ_stock_location_warehouse" ON public.stock_location USING btree (warehouse_id)`

### `stock_movement` — MovimientoDeStock

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `movement_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `batch_id` | uuid | sí |  |  |  | Agrupa los movimientos de una misma operación. |
| `quantity` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `from_location_id` | uuid | no | FK | `stock_location.location_id` |  | _(sin descripción documentada en el código)_ |
| `from_condition` | stock_condition_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `to_location_id` | uuid | no | FK | `stock_location.location_id` |  | _(sin descripción documentada en el código)_ |
| `to_condition` | stock_condition_enum | no |  |  |  | _(sin descripción documentada en el código)_ |
| `reason` | stock_movement_reason_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `reference_type` | stock_movement_reference_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `reference_id` | uuid | no |  |  |  | Sin clave foránea, a propósito: apunta a tablas distintas según `referenceType`. |
| `reversed_movement_id` | uuid | no | FK | `stock_movement.movement_id` |  | _(sin descripción documentada en el código)_ |
| `notes` | varchar(300) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `actor_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `occurred_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`movement_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_stock_movement_cantidad`: `CHECK ((quantity > 0))`
- `CHK_stock_movement_destino_coherente`: `CHECK (((to_location_id IS NULL) = (to_condition IS NULL)))`
- `CHK_stock_movement_origen_coherente`: `CHECK (((from_location_id IS NULL) = (from_condition IS NULL)))`
- `CHK_stock_movement_origen_destino_distintos`: `CHECK ((NOT ((from_location_id = to_location_id) AND (from_condition = to_condition))))`
- `CHK_stock_movement_origen_o_destino`: `CHECK (((from_location_id IS NOT NULL) OR (to_location_id IS NOT NULL)))`

Índices (además de la clave primaria):
- `IDX_stock_movement_alta`: `CREATE INDEX "IDX_stock_movement_alta" ON public.stock_movement USING btree (distributor_id, "createdAt")`
- `IDX_stock_movement_destino`: `CREATE INDEX "IDX_stock_movement_destino" ON public.stock_movement USING btree (to_location_id, gas_cylinder_id, to_condition)`
- `IDX_stock_movement_fecha`: `CREATE INDEX "IDX_stock_movement_fecha" ON public.stock_movement USING btree (distributor_id, occurred_at)`
- `IDX_stock_movement_garrafa_fecha`: `CREATE INDEX "IDX_stock_movement_garrafa_fecha" ON public.stock_movement USING btree (gas_cylinder_id, occurred_at)`
- `IDX_stock_movement_lote`: `CREATE INDEX "IDX_stock_movement_lote" ON public.stock_movement USING btree (batch_id)`
- `IDX_stock_movement_origen`: `CREATE INDEX "IDX_stock_movement_origen" ON public.stock_movement USING btree (from_location_id, gas_cylinder_id, from_condition)`
- `IDX_stock_movement_referencia`: `CREATE INDEX "IDX_stock_movement_referencia" ON public.stock_movement USING btree (reference_type, reference_id)`
- `UQ_stock_movement_contraasiento`: `CREATE UNIQUE INDEX "UQ_stock_movement_contraasiento" ON public.stock_movement USING btree (reversed_movement_id) WHERE (reversed_movement_id IS NOT NULL)`
- `UQ_stock_movement_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_stock_movement_id_distribuidora" ON public.stock_movement USING btree (movement_id, distributor_id)`
- `UQ_stock_movement_pedido`: `CREATE UNIQUE INDEX "UQ_stock_movement_pedido" ON public.stock_movement USING btree (reference_id, gas_cylinder_id, reason) WHERE ((reference_type = 'order'::stock_movement_reference_type_enum) AND (reason <> 'reversal'::stock_movement_reason_enum))`

### `stock_reconciliation_alert` — Aviso de conciliación de stock

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `distributor_id` | uuid | sí | PK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `signature` | varchar(64) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `alerted_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

### `stock_threshold` — UmbralDeStock

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `threshold_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `warehouse_id` | uuid | sí | FK | `warehouse.warehouse_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `min_full` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `alerted_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`warehouse_id`, `gas_cylinder_id`).

Restricciones `CHECK`:
- `CHK_stock_threshold_minimo`: `CHECK ((min_full >= 0))`

Índices (además de la clave primaria):
- `IDX_stock_threshold_distributor`: `CREATE INDEX "IDX_stock_threshold_distributor" ON public.stock_threshold USING btree (distributor_id)`
- `UQ_stock_threshold_deposito_garrafa`: `CREATE UNIQUE INDEX "UQ_stock_threshold_deposito_garrafa" ON public.stock_threshold USING btree (warehouse_id, gas_cylinder_id)`

### `storage_orphan` — Archivo pendiente de borrado

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `orphan_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `storage_key` | varchar(512) | sí | U |  |  | _(sin descripción documentada en el código)_ |
| `attempts` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `last_error` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `created_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updated_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `kind` | varchar(10) | sí |  |  | `'remove'::character varying` | _(sin descripción documentada en el código)_ |
| `status` | varchar(10) | sí |  |  | `'pending'::character varying` | _(sin descripción documentada en el código)_ |
| `next_attempt_at` | timestamptz | sí |  |  | `now()` | Desde cuándo el cron puede (re)intentar el borrado. |

Índices (además de la clave primaria):
- `UQ_79763cafe43e9dcf31ea86b6f59`: `CREATE UNIQUE INDEX "UQ_79763cafe43e9dcf31ea86b6f59" ON public.storage_orphan USING btree (storage_key)`

### `supplier` — Proveedor

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `supplier_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `business_name` | varchar(120) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `cuit` | varchar(11) | sí |  |  |  | Once dígitos, sin guiones. |
| `kind` | supplier_kind_enum | sí |  |  | `'other'::supplier_kind_enum` | _(sin descripción documentada en el código)_ |
| `contact_name` | varchar(80) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `phone` | varchar(30) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `email` | varchar(120) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `address` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `payment_terms_days` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `is_active` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`supplier_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_supplier_cuit`: `CHECK (es_cuit_valido((cuit)::text))`

Índices (además de la clave primaria):
- `IDX_supplier_distributor`: `CREATE INDEX "IDX_supplier_distributor" ON public.supplier USING btree (distributor_id)`
- `UQ_supplier_cuit_vigente`: `CREATE UNIQUE INDEX "UQ_supplier_cuit_vigente" ON public.supplier USING btree (distributor_id, cuit) WHERE ("deletedAt" IS NULL)`
- `UQ_supplier_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_supplier_id_distribuidora" ON public.supplier USING btree (supplier_id, distributor_id)`

### `time_slot` — FranjaHoraria

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `time_slot_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `name` | varchar(50) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `startTime` | time | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `endTime` | time | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `capacity` | integer | sí |  |  | `50` | _(sin descripción documentada en el código)_ |
| `isActive` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`time_slot_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_time_slot_capacidad`: `CHECK ((capacity > 0))`
- `CHK_time_slot_horario`: `CHECK (("startTime" < "endTime"))`

Índices (además de la clave primaria):
- `EXC_time_slot_solapada`: `CREATE INDEX "EXC_time_slot_solapada" ON public.time_slot USING gist (distributor_id, tsrange(('2000-01-01 00:00:00'::timestamp without time zone + ("startTime")::interval), ('2000-01-01 00:00:00'::timestamp without time zone + ("endTime")::interval))) WHERE ("isActive" AND ("startTime" IS NOT NULL) AND ("endTime" IS NOT NULL))`
- `IDX_e87ae54beaee42b885813deb8e`: `CREATE INDEX "IDX_e87ae54beaee42b885813deb8e" ON public.time_slot USING btree (distributor_id)`
- `UQ_time_slot_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_time_slot_id_distribuidora" ON public.time_slot USING btree (time_slot_id, distributor_id)`
- `UQ_time_slot_nombre_activa`: `CREATE UNIQUE INDEX "UQ_time_slot_nombre_activa" ON public.time_slot USING btree (distributor_id, lower((name)::text)) WHERE "isActive"`

### `tire` — Neumatico

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `tire_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `serial_number` | varchar(60) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `brand` | varchar(60) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `size` | varchar(40) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `cost` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | tire_status_enum | sí |  |  | `'in_stock'::tire_status_enum` | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | no | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `position` | varchar(6) | no |  |  |  | Código corto de la posición en el vehículo (p. ej. DI = delantero izquierdo). |
| `mounted_odometer_km` | integer | no |  |  |  | Kilometraje del vehículo en el montaje vigente. |
| `km_traveled` | integer | sí |  |  | `0` | Km recorridos en los montajes ya cerrados (desmontaje, baja). |
| `retread_count` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`distributor_id`, `serial_number`).

Restricciones `CHECK`:
- `CHK_tire_montaje`: `CHECK (((status = 'mounted'::tire_status_enum) = ((car_id IS NOT NULL) AND ("position" IS NOT NULL))))`
- `CHK_tire_valores`: `CHECK (((cost >= (0)::numeric) AND (km_traveled >= 0) AND (retread_count >= 0)))`

Índices (además de la clave primaria):
- `UQ_tire_posicion_ocupada`: `CREATE UNIQUE INDEX "UQ_tire_posicion_ocupada" ON public.tire USING btree (car_id, "position") WHERE (status = 'mounted'::tire_status_enum)`
- `UQ_tire_serial`: `CREATE UNIQUE INDEX "UQ_tire_serial" ON public.tire USING btree (distributor_id, serial_number)`

### `tire_event` — MovimientoNeumatico

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `event_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `tire_id` | uuid | sí | FK | `tire.tire_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `type` | tire_event_type_enum | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | no | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `position` | varchar(6) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `odometer_km` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `created_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `IDX_tire_event_tire`: `CREATE INDEX "IDX_tire_event_tire" ON public.tire_event USING btree (tire_id, "createdAt")`

### `traffic_fine` — MultaTransito

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `fine_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | sí | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `employee_id` | uuid | no | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `occurred_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `jurisdiction` | varchar(80) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `act_number` | varchar(40) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `infraction` | text | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `amount` | numeric(12,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `voluntary_payment_amount` | numeric(12,2) | no |  |  |  | Importe con el descuento de pago voluntario. |
| `due_date` | date | no |  |  |  | Fecha de calendario `YYYY-MM-DD`. |
| `status` | traffic_fine_status_enum | sí |  |  | `'pending'::traffic_fine_status_enum` | _(sin descripción documentada en el código)_ |
| `paid_at` | timestamptz | no |  |  |  | Día del pago, como el inicio de ese día en hora argentina. |
| `paid_amount` | numeric(12,2) | no |  |  |  | Lo efectivamente pagado: suele ser el del pago voluntario, menor que `amount`. |
| `charged_to_employee` | boolean | sí |  |  | `false` | Imputada al chofer (CU-200): la asume el empleado y no cuenta como costo del vehículo. |
| `void_reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `voided_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `alerted_at` | timestamptz | no |  |  |  | Cuándo se avisó el vencimiento (CU-326); `null` = sin avisar. |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `cash_movement_id` | uuid | no | FK | `cash_movement.movement_id` |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`distributor_id`, `jurisdiction`, `act_number`).

Restricciones `CHECK`:
- `CHK_traffic_fine_amount`: `CHECK ((amount > (0)::numeric))`
- `CHK_traffic_fine_anulada_fecha`: `CHECK (((status <> 'voided'::traffic_fine_status_enum) OR (voided_at IS NOT NULL)))`
- `CHK_traffic_fine_importe_pagado`: `CHECK (((paid_amount IS NULL) OR (paid_amount > (0)::numeric)))`
- `CHK_traffic_fine_pagada_datos`: `CHECK (((status <> 'paid'::traffic_fine_status_enum) OR ((paid_at IS NOT NULL) AND (paid_amount IS NOT NULL))))`
- `CHK_traffic_fine_pago_contra_importe`: `CHECK (((paid_amount IS NULL) OR (paid_amount <= amount)))`
- `CHK_traffic_fine_pago_voluntario`: `CHECK (((voluntary_payment_amount IS NULL) OR ((voluntary_payment_amount > (0)::numeric) AND (voluntary_payment_amount <= amount))))`

Índices (además de la clave primaria):
- `IDX_traffic_fine_car`: `CREATE INDEX "IDX_traffic_fine_car" ON public.traffic_fine USING btree (car_id, occurred_at)`
- `IDX_traffic_fine_status_due`: `CREATE INDEX "IDX_traffic_fine_status_due" ON public.traffic_fine USING btree (distributor_id, status, due_date)`
- `UQ_traffic_fine_act`: `CREATE UNIQUE INDEX "UQ_traffic_fine_act" ON public.traffic_fine USING btree (distributor_id, jurisdiction, act_number)`

### `truck_load` — CargaDeCamion

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `load_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `number` | integer | sí |  |  |  | Número correlativo por distribuidora (`document_sequence`). |
| `car_id` | uuid | sí | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `delivery_id` | uuid | sí | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `helper_employee_id` | uuid | no | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `origin_location_id` | uuid | sí | FK | `stock_location.location_id` |  | _(sin descripción documentada en el código)_ |
| `business_date` | date | sí |  |  |  | Día de negocio en hora argentina (YYYY-MM-DD). |
| `status` | truck_load_status_enum | sí |  |  | `'loading'::truck_load_status_enum` | _(sin descripción documentada en el código)_ |
| `opened_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `departed_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `returned_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `closed_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `opened_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `closed_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `difference_note` | text | no |  |  |  | Obligatoria si la rendición cierra con diferencia. |
| `cancel_reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`load_id`, `distributor_id`), (`distributor_id`, `number`).

Restricciones `CHECK`:
- `CHK_truck_load_cancelada`: `CHECK (((status <> 'cancelled'::truck_load_status_enum) OR (cancel_reason IS NOT NULL)))`
- `CHK_truck_load_cierre`: `CHECK (((status <> ALL (ARRAY['closed'::truck_load_status_enum, 'closed_with_difference'::truck_load_status_enum, 'cancelled'::truck_load_status_enum])) OR (closed_at IS NOT NULL)))`
- `CHK_truck_load_regreso`: `CHECK (((status <> ALL (ARRAY['returned'::truck_load_status_enum, 'closed'::truck_load_status_enum, 'closed_with_difference'::truck_load_status_enum])) OR (returned_at IS NOT NULL)))`
- `CHK_truck_load_salida`: `CHECK (((status = ANY (ARRAY['loading'::truck_load_status_enum, 'cancelled'::truck_load_status_enum])) OR (departed_at IS NOT NULL)))`

Índices (además de la clave primaria):
- `IDX_truck_load_camion`: `CREATE INDEX "IDX_truck_load_camion" ON public.truck_load USING btree (car_id)`
- `IDX_truck_load_chofer`: `CREATE INDEX "IDX_truck_load_chofer" ON public.truck_load USING btree (delivery_id)`
- `IDX_truck_load_estado`: `CREATE INDEX "IDX_truck_load_estado" ON public.truck_load USING btree (distributor_id, status)`
- `IDX_truck_load_fecha`: `CREATE INDEX "IDX_truck_load_fecha" ON public.truck_load USING btree (distributor_id, business_date)`
- `UQ_truck_load_camion_abierta`: `CREATE UNIQUE INDEX "UQ_truck_load_camion_abierta" ON public.truck_load USING btree (car_id) WHERE (status = ANY (ARRAY['loading'::truck_load_status_enum, 'on_route'::truck_load_status_enum, 'returned'::truck_load_status_enum]))`
- `UQ_truck_load_chofer_abierta`: `CREATE UNIQUE INDEX "UQ_truck_load_chofer_abierta" ON public.truck_load USING btree (delivery_id) WHERE (status = ANY (ARRAY['loading'::truck_load_status_enum, 'on_route'::truck_load_status_enum, 'returned'::truck_load_status_enum]))`
- `UQ_truck_load_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_truck_load_id_distribuidora" ON public.truck_load USING btree (load_id, distributor_id)`
- `UQ_truck_load_numero`: `CREATE UNIQUE INDEX "UQ_truck_load_numero" ON public.truck_load USING btree (distributor_id, number)`

### `truck_load_item` — ItemCarga

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `item_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `load_id` | uuid | sí | FK | `truck_load.load_id` |  | _(sin descripción documentada en el código)_ |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |  | _(sin descripción documentada en el código)_ |
| `loaded_full` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `reloaded_full` | integer | sí |  |  | `0` | Llenas repuestas en ruta (suma de las reposiciones). |
| `loaded_empty` | integer | sí |  |  | `0` | Vacías con las que sale para canjear. |
| `declared_return_full` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `declared_return_empty` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `delivered_full` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `collected_empty` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `expected_full` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `expected_empty` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `difference_full` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |
| `difference_empty` | integer | no |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`load_id`, `gas_cylinder_id`).

Restricciones `CHECK`:
- `CHK_truck_load_item_cargado`: `CHECK (((loaded_full >= 0) AND (reloaded_full >= 0) AND (loaded_empty >= 0)))`
- `CHK_truck_load_item_declarado`: `CHECK ((((declared_return_full IS NULL) OR (declared_return_full >= 0)) AND ((declared_return_empty IS NULL) OR (declared_return_empty >= 0))))`

Índices (además de la clave primaria):
- `IDX_truck_load_item_garrafa`: `CREATE INDEX "IDX_truck_load_item_garrafa" ON public.truck_load_item USING btree (gas_cylinder_id)`
- `UQ_truck_load_item_garrafa`: `CREATE UNIQUE INDEX "UQ_truck_load_item_garrafa" ON public.truck_load_item USING btree (load_id, gas_cylinder_id)`

### `user` — Usuario

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `user_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `role_id` | uuid | no | FK | `role.role_id` |  | _(sin descripción documentada en el código)_ |
| `firebase_uid` | varchar | no | U |  |  | Una cuenta de acceso de Firebase corresponde a un solo usuario. |
| `full_name` | varchar | no |  |  |  | _(sin descripción documentada en el código)_ |
| `selfie` | varchar | no |  |  |  | _(sin descripción documentada en el código)_ |
| `email` | varchar | no | U |  |  | _(sin descripción documentada en el código)_ |
| `phone_number` | varchar | no | U |  |  | _(sin descripción documentada en el código)_ |
| `phone_verified` | boolean | sí |  |  | `false` | _(sin descripción documentada en el código)_ |
| `email_verified` | boolean | sí |  |  | `false` | _(sin descripción documentada en el código)_ |
| `blocked` | boolean | sí |  |  | `false` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `photo_key` | varchar(512) | no |  |  |  | Key de la foto de perfil en el bucket (`users/{usuario}/{uuid}.{ext}`). |

Restricciones `CHECK`:
- `CHK_user_email`: `CHECK (((email IS NULL) OR ((email)::text ~* '^[^@[:space:]]+@[^@[:space:]]+[.][^@[:space:]]+$'::text)))`
- `CHK_user_telefono`: `CHECK (((phone_number IS NULL) OR ((phone_number)::text ~ '^[+][1-9][0-9]{7,14}$'::text)))`

Índices (además de la clave primaria):
- `UQ_01eea41349b6c9275aec646eee0`: `CREATE UNIQUE INDEX "UQ_01eea41349b6c9275aec646eee0" ON public."user" USING btree (phone_number)`
- `UQ_40fe3048b17f675b652c1999270`: `CREATE UNIQUE INDEX "UQ_40fe3048b17f675b652c1999270" ON public."user" USING btree (firebase_uid)`
- `UQ_e12875dfb3b1d92d7d7c5377e22`: `CREATE UNIQUE INDEX "UQ_e12875dfb3b1d92d7d7c5377e22" ON public."user" USING btree (email)`
- `UQ_user_email_minusculas`: `CREATE UNIQUE INDEX "UQ_user_email_minusculas" ON public."user" USING btree (lower((email)::text))`

### `user_address` — DireccionEntrega

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `address_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `street` | varchar(255) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `city` | varchar(100) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `postalCode` | varchar(20) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `formattedAddress` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `isDefault` | boolean | sí |  |  | `false` | _(sin descripción documentada en el código)_ |
| `additionalInstructions` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | Baja lógica: la fila se conserva para el historial y la auditoría. |
| `floor` | varchar(10) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `apartment` | varchar(10) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `location` | geometry | no |  |  |  | Punto de la dirección (antes latitude y longitude como varchar). La API sigue recibiendo y devolviendo latitude y longitude por separado. |
| `place_id` | varchar(255) | no |  |  |  | Identificador estable del lugar en el servicio de mapas (CU-116). |
| `geocode_precision` | address_geocode_precision_enum | sí |  |  | `'unresolved'::address_geocode_precision_enum` | Con qué precisión resolvió el servicio de mapas la dirección (CU-118). |

Índices (además de la clave primaria):
- `IDX_ef8ba785cbfbb81849828b38e7`: `CREATE INDEX "IDX_ef8ba785cbfbb81849828b38e7" ON public.user_address USING gist (location)`
- `UQ_user_address_principal`: `CREATE UNIQUE INDEX "UQ_user_address_principal" ON public.user_address USING btree (user_id) WHERE ("isDefault" AND ("deletedAt" IS NULL))`

### `vehicle_accident` — Siniestro

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `accident_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | sí | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `employee_id` | uuid | no | FK | `employee.employee_id` |  | _(sin descripción documentada en el código)_ |
| `occurred_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `location` | geometry | no |  |  |  | _(sin descripción documentada en el código)_ |
| `address` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `description` | text | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `injuries` | boolean | sí |  |  | `false` | _(sin descripción documentada en el código)_ |
| `third_parties_involved` | boolean | sí |  |  | `false` | _(sin descripción documentada en el código)_ |
| `hazmat_release` | boolean | sí |  |  | `false` | Fuga o derrame de gas: obliga a avisar de inmediato a los administradores. |
| `police_report_number` | varchar(40) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `insurer_claim_number` | varchar(40) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | vehicle_accident_status_enum | sí |  |  | `'reported'::vehicle_accident_status_enum` | _(sin descripción documentada en el código)_ |
| `vehicle_unusable` | boolean | sí |  |  | `false` | Si quedó inutilizable, el vehículo pasó a fuera de servicio al registrarlo. |
| `repair_cost` | numeric(12,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `insurer_reimbursement` | numeric(12,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `deductible_amount` | numeric(12,2) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `closed_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `created_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_vehicle_accident_cerrado_fecha`: `CHECK (((status <> 'closed'::vehicle_accident_status_enum) OR (closed_at IS NOT NULL)))`
- `CHK_vehicle_accident_montos`: `CHECK (((COALESCE(repair_cost, (0)::numeric) >= (0)::numeric) AND (COALESCE(insurer_reimbursement, (0)::numeric) >= (0)::numeric) AND (COALESCE(deductible_amount, (0)::numeric) >= (0)::numeric) AND ((insurer_reimbursement IS NULL) OR (repair_cost IS NULL) OR (insurer_reimbursement <= repair_cost))))`

Índices (además de la clave primaria):
- `IDX_vehicle_accident_car`: `CREATE INDEX "IDX_vehicle_accident_car" ON public.vehicle_accident USING btree (car_id, occurred_at)`
- `IDX_vehicle_accident_status`: `CREATE INDEX "IDX_vehicle_accident_status" ON public.vehicle_accident USING btree (distributor_id, status)`

### `vehicle_assignment` — AsignacionVehiculo

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `assignment_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | sí | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `delivery_id` | uuid | sí | FK | `delivery.delivery_id` |  | _(sin descripción documentada en el código)_ |
| `assigned_at` | timestamptz | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `released_at` | timestamptz | no |  |  |  | `null` = todavía en uso. Se setea al liberar (manual, reasignación o baja del chofer). |
| `assigned_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `released_by_user_id` | uuid | no | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `note` | text | no |  |  |  | _(sin descripción documentada en el código)_ |

Restricciones `CHECK`:
- `CHK_vehicle_assignment_periodo`: `CHECK (((released_at IS NULL) OR (released_at >= assigned_at)))`

Índices (además de la clave primaria):
- `EXC_vehicle_assignment_chofer_solapada`: `CREATE INDEX "EXC_vehicle_assignment_chofer_solapada" ON public.vehicle_assignment USING gist (delivery_id, tstzrange(assigned_at, COALESCE(released_at, 'infinity'::timestamp with time zone)))`
- `EXC_vehicle_assignment_vehiculo_solapada`: `CREATE INDEX "EXC_vehicle_assignment_vehiculo_solapada" ON public.vehicle_assignment USING gist (car_id, tstzrange(assigned_at, COALESCE(released_at, 'infinity'::timestamp with time zone)))`
- `IDX_1f986e62c32ac5ee2d8d7eb133`: `CREATE INDEX "IDX_1f986e62c32ac5ee2d8d7eb133" ON public.vehicle_assignment USING btree (distributor_id)`
- `UQ_vehicle_assignment_car_abierta`: `CREATE UNIQUE INDEX "UQ_vehicle_assignment_car_abierta" ON public.vehicle_assignment USING btree (car_id) WHERE (released_at IS NULL)`
- `UQ_vehicle_assignment_delivery_abierta`: `CREATE UNIQUE INDEX "UQ_vehicle_assignment_delivery_abierta" ON public.vehicle_assignment USING btree (delivery_id) WHERE (released_at IS NULL)`

### `vehicle_usage_log` — RegistroUsoVehiculo

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `log_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `car_id` | uuid | sí | FK | `car.car_id` |  | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `day` | date | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `km` | numeric(10,2) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `orders` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |
| `route_hours` | numeric(6,2) | sí |  |  | `'0'::numeric` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`car_id`, `day`).

Restricciones `CHECK`:
- `CHK_vehicle_usage_log_valores`: `CHECK (((km >= (0)::numeric) AND (orders >= 0) AND (route_hours >= (0)::numeric)))`

Índices (además de la clave primaria):
- `IDX_8d4be9c7008fc808b4900a83a5`: `CREATE INDEX "IDX_8d4be9c7008fc808b4900a83a5" ON public.vehicle_usage_log USING btree (distributor_id)`
- `UQ_vehicle_usage_log_car_day`: `CREATE UNIQUE INDEX "UQ_vehicle_usage_log_car_day" ON public.vehicle_usage_log USING btree (car_id, day)`

### `warehouse` — Deposito

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `warehouse_id` | uuid | sí | PK |  | `uuid_generate_v4()` | _(sin descripción documentada en el código)_ |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `name` | varchar(80) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `code` | varchar(12) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `kind` | warehouse_kind_enum | sí |  |  | `'depot'::warehouse_kind_enum` | _(sin descripción documentada en el código)_ |
| `address` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `is_default` | boolean | sí |  |  | `false` | _(sin descripción documentada en el código)_ |
| `is_active` | boolean | sí |  |  | `true` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`warehouse_id`, `distributor_id`).

Restricciones `CHECK`:
- `CHK_warehouse_codigo`: `CHECK (((code)::text ~ '^[A-Z0-9_-]{1,12}$'::text))`

Índices (además de la clave primaria):
- `IDX_warehouse_distributor`: `CREATE INDEX "IDX_warehouse_distributor" ON public.warehouse USING btree (distributor_id)`
- `UQ_warehouse_code_vigente`: `CREATE UNIQUE INDEX "UQ_warehouse_code_vigente" ON public.warehouse USING btree (distributor_id, code) WHERE ("deletedAt" IS NULL)`
- `UQ_warehouse_default_vigente`: `CREATE UNIQUE INDEX "UQ_warehouse_default_vigente" ON public.warehouse USING btree (distributor_id) WHERE (is_default AND ("deletedAt" IS NULL))`
- `UQ_warehouse_id_distribuidora`: `CREATE UNIQUE INDEX "UQ_warehouse_id_distribuidora" ON public.warehouse USING btree (warehouse_id, distributor_id)`

> **Cobertura de las descripciones.** 152 de 977 columnas tienen descripción tomada del comentario de la entidad de TypeORM que las define; las que no la tienen en el código figuran arriba como «sin descripción documentada en el código» en lugar de inventarse una.

## Relaciones no declaradas

No hay ninguna: las 13 relaciones que en algún momento existieron sin `FOREIGN KEY` se declararon el 25/09/2026 (migración `DeclararRelacionesSinClaveForanea`). Hoy las 293 claves foráneas del dominio (238 simples y 55 compuestas por distribuidora) están todas declaradas.

### 1. Baja del envase y oferta de retiro

**Casos de uso:** CU-108 (C-15). **Qué resuelve:** Poder dar un envase de baja y atar la oferta de retiro a la entrega programada.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `cylinder` | `decommissioned_at` | timestamptz | no | Cuándo se dio de baja el envase; vacío mientras está en circulación. |
| `cylinder_recovery_notice` | `order_id` | uuid | no | Pedido de la entrega a la que se ató la oferta de retiro. |


> **Decisión de modelado.** El ciclo del envase no tiene un estado de baja: se agrega una baja lógica en vez de un valor de estado, para no tocar la máquina de estados que ya usan el despacho y la devolución. El aviso de recupero necesita saber a qué entrega se ató la oferta de retiro.

## Tipos enumerados

| Tipo | Valores | Estado |
|---|---|---|
| `address_geocode_precision_enum` | `exact`, `approximate`, `unresolved` | implementado |
| `attachment_owner_type_enum` | `employee`, `fuel_load`, `traffic_fine`, `vehicle_accident`, `purchase_receipt`, `stock_adjustment`, `driver_settlement`, `cash_movement`, `customer_account_entry` | implementado |
| `audit_result_enum` | `success`, `failure` | implementado |
| `cash_box_kind_enum` | `cash`, `bank`, `wallet` | implementado |
| `cash_category_direction_enum` | `income`, `expense` | implementado |
| `cash_category_system_code_enum` | `driver_settlement`, `customer_payment`, `commission_payment`, `cash_surplus`, `cash_shortage`, `transfer_in`, `transfer_out`, `purchase`, `fuel`, `traffic_fine`, `order_payment` | implementado |
| `cash_movement_direction_enum` | `in`, `out` | implementado |
| `cash_movement_method_enum` | `cash`, `transfer`, `card`, `mercadopago`, `check` | implementado |
| `cash_movement_reference_type_enum` | `manual`, `session_opening`, `session_closing`, `driver_settlement`, `customer_payment`, `purchase_receipt`, `fuel_load`, `traffic_fine`, `driver_liquidation`, `box_transfer`, `reversal`, `order_payment` | implementado |
| `cash_session_status_enum` | `open`, `closed` | implementado |
| `claims_status_enum` | `pending`, `in_process`, `resolved`, `rejected` | implementado |
| `commission_entry_type_enum` | `delivery_commission`, `settlement_shortage`, `traffic_fine`, `adjustment`, `legacy_balance` | implementado |
| `commission_rule_basis_enum` | `per_unit`, `per_order`, `percent_of_total` | implementado |
| `configurable_process_enum` | `fleet_planner`, `repurchase`, `route_batching`, `cylinder_recovery`, `express_dispatch`, `stock_control`, `dispatch`, `scheduled_tasks` | implementado |
| `coverage_zone_surcharge_type_enum` | `fixed`, `percentage` | implementado |
| `customer_account_entry_type_enum` | `sale_charge`, `payment`, `credit_note`, `debit_note` | implementado |
| `customer_account_status_enum` | `active`, `blocked`, `closed` | implementado |
| `customer_account_tax_condition_enum` | `registered`, `monotax`, `exempt`, `final_consumer` | implementado |
| `cylinder_inspection_result_enum` | `approved`, `conditional`, `rejected` | implementado |
| `cylinder_movement_from_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned`, `retired` | implementado |
| `cylinder_movement_to_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned`, `retired` | implementado |
| `cylinder_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned`, `retired` | implementado |
| `distributor_status_enum` | `active`, `suspended` | implementado |
| `driver_liquidation_status_enum` | `draft`, `approved`, `paid`, `voided` | implementado |
| `driver_settlement_difference_resolution_enum` | `none`, `charged_to_driver`, `absorbed` | implementado |
| `driver_settlement_status_enum` | `open`, `submitted`, `approved` | implementado |
| `employee_attendance_source_enum` | `panel`, `driver_app` | implementado |
| `employee_document_type_enum` | `dni`, `passport`, `other` | implementado |
| `employee_leave_status_enum` | `requested`, `approved`, `rejected`, `cancelled` | implementado |
| `employee_leave_type_enum` | `vacation`, `sick`, `work_accident`, `study`, `marriage`, `birth`, `bereavement`, `unpaid`, `suspension`, `unjustified_absence`, `other` | implementado |
| `employee_status_enum` | `active`, `terminated` | implementado |
| `employee_termination_reason_enum` | `resignation`, `dismissal`, `end_of_contract`, `retirement`, `other` | implementado |
| `employment_type_enum` | `permanent`, `fixed_term`, `part_time`, `contractor` | implementado |
| `fleet_status_enum` | `active`, `in_service`, `grounded` | implementado |
| `fuel_payment_method_enum` | `cash_box`, `driver_cash`, `card`, `fuel_account` | implementado |
| `fuel_type_enum` | `diesel`, `gasoline`, `cng`, `lpg` | implementado |
| `incident_moment_enum` | `pre_delivery`, `in_delivery`, `post_delivery` | implementado |
| `incident_status_enum` | `open`, `resolved`, `discarded` | implementado |
| `incident_type_enum` | `damaged`, `out_of_stock`, `no_show`, `unpaid_collection`, `other` | implementado |
| `job_position_category_enum` | `driver`, `helper`, `warehouse`, `administration`, `sales`, `management`, `other` | implementado |
| `maintenance_criticality_enum` | `blocking`, `non_blocking` | implementado |
| `maintenance_subject_enum` | `vehicle`, `driver`, `employee` | implementado |
| `maintenance_task_status_enum` | `forecast`, `scheduled`, `in_progress`, `done`, `overdue`, `cancelled` | implementado |
| `maintenance_trigger_enum` | `by_km`, `by_time`, `by_fixed_date` | implementado |
| `order_delivery_mode_enum` | `standard`, `express` | implementado |
| `order_dispatch_offer_status_enum` | `offered`, `accepted`, `rejected`, `expired`, `superseded` | implementado |
| `order_paymentmethod_enum` | `cash`, `mercadopago`, `transfer`, `account` | implementado |
| `order_paymentstatus_enum` | `pending`, `paid`, `failed`, `unpaid`, `written_off` | implementado |
| `order_paymenttype_enum` | `cash`, `online`, `account` | implementado |
| `order_status_enum` | `reserved`, `pending`, `accepted`, `on_the_way`, `delivered`, `cancelled` | implementado |
| `order_zone_surcharge_type_enum` | `fixed`, `percentage` | implementado |
| `payment_gateway_enum` | `mercadopago`, `cash` | implementado |
| `payment_integration_enum` | `checkout_pro`, `cash` | implementado |
| `payment_refund_kind_enum` | `full`, `express_surcharge` | implementado |
| `payment_refund_status_enum` | `pending`, `succeeded`, `failed` | implementado |
| `payment_status_enum` | `pending`, `approved`, `rejected`, `cancelled`, `refunded` | implementado |
| `plan_document_kind_enum` | `insurance`, `vtv`, `hazmat_vehicle_permit`, `driver_license`, `hazmat_driver_course`, `psychophysical`, `art_coverage`, `service`, `generic` | implementado |
| `proposal_status_enum` | `pending`, `accepted`, `rejected`, `expired` | implementado |
| `purchase_order_status_enum` | `draft`, `sent`, `partially_received`, `received`, `closed_short`, `cancelled` | implementado |
| `purchase_payment_status_enum` | `unpaid`, `paid` | implementado |
| `purchase_receipt_status_enum` | `confirmed`, `voided` | implementado |
| `rating_from_role_enum` | `customer`, `delivery` | implementado |
| `recovery_case_status_enum` | `open`, `returned`, `escalated`, `deposit_charged`, `written_off`, `closed_no_charge` | implementado |
| `recovery_notice_kind_enum` | `reminder`, `pickup_offer`, `deposit_warning` | implementado |
| `repurchase_invitation_status_enum` | `pending`, `accepted`, `rejected`, `expired` | implementado |
| `route_batch_status_enum` | `forming`, `offered`, `assigned`, `dissolved`, `completed` | implementado |
| `stock_adjustment_reason_enum` | `count_correction`, `shrinkage`, `leak`, `damaged`, `lost`, `found`, `initial_count`, `reconciliation` | implementado |
| `stock_condition_enum` | `full`, `empty`, `defective` | implementado |
| `stock_location_kind_enum` | `warehouse`, `vehicle` | implementado |
| `stock_movement_reason_enum` | `initial_count`, `purchase_receipt`, `plant_empty_out`, `truck_load`, `truck_return`, `delivery`, `empty_collected`, `transfer`, `adjustment`, `shrinkage`, `condition_change`, `reversal` | implementado |
| `stock_movement_reference_type_enum` | `order`, `purchase_receipt`, `truck_load`, `stock_adjustment`, `transfer`, `initial` | implementado |
| `supplier_document_type_enum` | `delivery_note`, `invoice` | implementado |
| `supplier_kind_enum` | `filling_plant`, `other` | implementado |
| `tire_event_type_enum` | `mount`, `unmount`, `rotate`, `retread`, `retire` | implementado |
| `tire_status_enum` | `in_stock`, `mounted`, `retired` | implementado |
| `traffic_fine_status_enum` | `pending`, `appealed`, `paid`, `voided` | implementado |
| `truck_load_status_enum` | `loading`, `on_route`, `returned`, `closed`, `closed_with_difference`, `cancelled` | implementado |
| `vehicle_accident_status_enum` | `reported`, `under_review`, `repairing`, `closed` | implementado |
| `warehouse_kind_enum` | `depot`, `branch` | implementado |
