# Modelo de Datos — SPLG

63 tablas y 150 claves foráneas, leídas de la base en ejecución.

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
| `car_patent` | varchar(20) | no |  |  |  | Única entre los vehículos vigentes: dar de baja uno no bloquea volver a registrar la misma patente. |
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

Índices (además de la clave primaria):
- `IDX_e823ac113ba2af8cbe72ddcbe8`: `CREATE INDEX "IDX_e823ac113ba2af8cbe72ddcbe8" ON public.car USING btree (distributor_id)`
- `UQ_car_patente_vigente`: `CREATE UNIQUE INDEX "UQ_car_patente_vigente" ON public.car USING btree (car_patent) WHERE ("deletedAt" IS NULL)`

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

Índices (además de la clave primaria):
- `UQ_cart_item_cart_gascylinder`: `CREATE UNIQUE INDEX "UQ_cart_item_cart_gascylinder" ON public.cart_item USING btree (cart_id, gas_cylinder_id)`

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

Índices (además de la clave primaria):
- `IDX_870bf1e0dc6005837ff0643b5f`: `CREATE INDEX "IDX_870bf1e0dc6005837ff0643b5f" ON public.claims USING btree (distributor_id)`

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

Restricciones `CHECK`:
- `CHK_coverage_zone_surcharge`: `CHECK ((((surcharge_type = 'fixed'::coverage_zone_surcharge_type_enum) AND (surcharge_value >= (0)::numeric)) OR ((surcharge_type = 'percentage'::coverage_zone_surcharge_type_enum) AND (surcharge_value >= (0)::numeric) AND (surcharge_value <= (100)::numeric))))`

Índices (además de la clave primaria):
- `IDX_01a53f7455396839c245037c9f`: `CREATE INDEX "IDX_01a53f7455396839c245037c9f" ON public.coverage_zone USING gist (area)`
- `IDX_50ad99ebfb6554428f39160228`: `CREATE INDEX "IDX_50ad99ebfb6554428f39160228" ON public.coverage_zone USING btree (distributor_id)`

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

Índices (además de la clave primaria):
- `IDX_0124ec56df62d9a9ba58cb41a2`: `CREATE INDEX "IDX_0124ec56df62d9a9ba58cb41a2" ON public.customer USING gist (location)`
- `REL_5d1f609371a285123294fddcf3`: `CREATE UNIQUE INDEX "REL_5d1f609371a285123294fddcf3" ON public.customer USING btree (user_id)`

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

Claves únicas compuestas: (`distributor_id`, `serial`).

Índices (además de la clave primaria):
- `IDX_7a848929dbfa5535e93e9494e7`: `CREATE INDEX "IDX_7a848929dbfa5535e93e9494e7" ON public.cylinder USING btree (serial)`
- `IDX_903b537f13281f56613047bcdc`: `CREATE INDEX "IDX_903b537f13281f56613047bcdc" ON public.cylinder USING btree (current_order_id)`
- `IDX_9e32d1c8fd5721ba71e98c5c93`: `CREATE INDEX "IDX_9e32d1c8fd5721ba71e98c5c93" ON public.cylinder USING btree (state)`
- `IDX_9e8b3d9c0ecf2651f6e836aca4`: `CREATE INDEX "IDX_9e8b3d9c0ecf2651f6e836aca4" ON public.cylinder USING btree (distributor_id)`
- `UQ_9e39bbb32ed614ddd09ac126e37`: `CREATE UNIQUE INDEX "UQ_9e39bbb32ed614ddd09ac126e37" ON public.cylinder USING btree (distributor_id, serial)`

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
| `balance` | double precision | sí |  |  | `'0'::double precision` | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | no |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `deletedAt` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `location` | geometry | no |  |  |  | Última ubicación conocida (antes texto "lat,lng" en latLng). |
| `isEnabled` | boolean | sí |  |  | `true` | Habilitación ADMINISTRATIVA: la pone/saca un admin con `PATCH /delivery/:id/status`. Un chofer deshabilitado no puede ponerse en línea aunque lo intente desde su app. Reemplaza a la vieja columna `isActive`, que mezclaba esto con la presencia del chofer (ver `isAvailable`): un chofer deshabilitado podía "conectarse" desde su app y volver a recibir pedidos. La columna `isActive` sigue existiendo en la base (no se borra ni se renombra: la sigue usando el proceso viejo mientras conviven ambos) pero este código ya no la lee ni la escribe. |
| `isAvailable` | boolean | sí |  |  | `false` | Presencia: true mientras el chofer está "en línea" en su app (`PATCH /delivery/user/:userId/availability`). Sale de línea al desconectarse, al deshabilitarlo un admin, o al cerrar la app (el gateway de sockets lo saca del radar al desconectar). |

Índices (además de la clave primaria):
- `IDX_8b64ee4e6e615c2082862f9e09`: `CREATE INDEX "IDX_8b64ee4e6e615c2082862f9e09" ON public.delivery USING btree (distributor_id)`
- `IDX_a3b8af1ce2f6e143d416d83080`: `CREATE INDEX "IDX_a3b8af1ce2f6e143d416d83080" ON public.delivery USING btree (user_id)`
- `IDX_c270386a78fdf46067bc9a94a7`: `CREATE INDEX "IDX_c270386a78fdf46067bc9a94a7" ON public.delivery USING gist (location)`
- `REL_a3b8af1ce2f6e143d416d83080`: `CREATE UNIQUE INDEX "REL_a3b8af1ce2f6e143d416d83080" ON public.delivery USING btree (user_id)`

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

Índices (además de la clave primaria):
- `IDX_02331b27890084627684d99ec5`: `CREATE UNIQUE INDEX "IDX_02331b27890084627684d99ec5" ON public.distributor USING btree (slug)`
- `UQ_02331b27890084627684d99ec5b`: `CREATE UNIQUE INDEX "UQ_02331b27890084627684d99ec5b" ON public.distributor USING btree (slug)`

### `document_sequence` — Secuencia de documentos

| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |
|---|---|:-:|:-:|---|---|---|
| `distributor_id` | uuid | sí | PK | `distributor.distributor_id` |  | _(sin descripción documentada en el código)_ |
| `doc_type` | varchar(40) | sí | PK |  |  | _(sin descripción documentada en el código)_ |
| `last_number` | integer | sí |  |  | `0` | _(sin descripción documentada en el código)_ |

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

Restricciones `CHECK`:
- `CHK_employee_status_termination`: `CHECK (((status = 'terminated'::employee_status_enum) = (termination_date IS NOT NULL)))`
- `CHK_employee_termination_date`: `CHECK (((termination_date IS NULL) OR (termination_date >= hire_date)))`

Índices (además de la clave primaria):
- `IDX_employee_name`: `CREATE INDEX "IDX_employee_name" ON public.employee USING btree (distributor_id, last_name, first_name)`
- `IDX_employee_position`: `CREATE INDEX "IDX_employee_position" ON public.employee USING btree (position_id)`
- `IDX_employee_status`: `CREATE INDEX "IDX_employee_status" ON public.employee USING btree (distributor_id, status)`
- `UQ_employee_cuil_vigente`: `CREATE UNIQUE INDEX "UQ_employee_cuil_vigente" ON public.employee USING btree (distributor_id, cuil) WHERE ((cuil IS NOT NULL) AND ("deletedAt" IS NULL))`
- `UQ_employee_document_vigente`: `CREATE UNIQUE INDEX "UQ_employee_document_vigente" ON public.employee USING btree (distributor_id, document_number) WHERE ("deletedAt" IS NULL)`
- `UQ_employee_file_number_vigente`: `CREATE UNIQUE INDEX "UQ_employee_file_number_vigente" ON public.employee USING btree (distributor_id, file_number) WHERE ("deletedAt" IS NULL)`
- `UQ_employee_user_vigente`: `CREATE UNIQUE INDEX "UQ_employee_user_vigente" ON public.employee USING btree (user_id) WHERE ((user_id IS NOT NULL) AND ("deletedAt" IS NULL))`

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

Claves únicas compuestas: (`distributor_id`, `type`).

Índices (además de la clave primaria):
- `IDX_990b829fdf06cb282d835a5d72`: `CREATE INDEX "IDX_990b829fdf06cb282d835a5d72" ON public.gas_cylinder USING btree (distributor_id)`
- `UQ_gas_cylinder_distribuidora_tipo`: `CREATE UNIQUE INDEX "UQ_gas_cylinder_distribuidora_tipo" ON public.gas_cylinder USING btree (distributor_id, type)`

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
- `CHK_promocion_descuento`: `CHECK (((discount_percentage > (0)::numeric) AND (discount_percentage <= (100)::numeric)))`

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

Índices (además de la clave primaria):
- `IDX_ec96001f6fe2869ae6b40f2dc8`: `CREATE INDEX "IDX_ec96001f6fe2869ae6b40f2dc8" ON public.maintenance_task USING btree (distributor_id)`

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
| `vehicle_car_id` | uuid | no |  |  |  | Snapshot del vehículo con el que se entrega, tomado al aceptar el pedido (manual, `PATCH /orders/:id/status` o despacho automático): el vehículo EN USO del chofer en ese momento (decisión de nahue del 30/09, "vehículo en uso"). Igual que `zone_name`/`zone_surcharge_ `, es una copia a propósito: si el chofer cambia de vehículo después, o el auto se edita o se borra, este pedido no cambia — queda la trazabilidad de con qué vehículo se entregó de verdad. `null` en pedidos sin chofer asignado todavía, o de antes de esta funcionalidad. |
| `vehicle_patent` | varchar(20) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `vehicle_brand` | varchar(50) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `vehicle_model` | varchar(50) | no |  |  |  | _(sin descripción documentada en el código)_ |
| `payment_confirmed_at` | timestamptz | no |  |  |  | Cuándo se confirmó el cobro (pago recibido por el chofer o resolución del admin). |
| `payment_confirmed_by` | uuid | no |  |  |  | Usuario que confirmó el cobro (el chofer, o el admin que resolvió el impago). |
| `payment_resolution_note` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `payment_resolved_at` | timestamptz | no |  |  |  | Motivo con el que el admin resolvió un impago. |
| `payment_resolved_by` | uuid | no |  |  |  | Admin que resolvió el impago. |

Índices (además de la clave primaria):
- `IDX_3adf34152c77fdb4e8f7346c5f`: `CREATE UNIQUE INDEX "IDX_3adf34152c77fdb4e8f7346c5f" ON public."order" USING btree ("gatewayPaymentId") WHERE ("gatewayPaymentId" IS NOT NULL)`
- `IDX_775a36a19670c03781e60bbce9`: `CREATE INDEX "IDX_775a36a19670c03781e60bbce9" ON public."order" USING btree (scheduled_date)`
- `IDX_7a9573d6a1fb982772a9123320`: `CREATE INDEX "IDX_7a9573d6a1fb982772a9123320" ON public."order" USING btree (status)`
- `IDX_cd7812c96209c5bdd48a6b858b`: `CREATE INDEX "IDX_cd7812c96209c5bdd48a6b858b" ON public."order" USING btree (customer_id)`
- `IDX_df56039592a4bbbd3fa4a19f14`: `CREATE INDEX "IDX_df56039592a4bbbd3fa4a19f14" ON public."order" USING btree (distributor_id)`
- `IDX_f437a76442f23c89ad7652b2a4`: `CREATE INDEX "IDX_f437a76442f23c89ad7652b2a4" ON public."order" USING btree ("deliveredAt")`
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

Índices (además de la clave primaria):
- `IDX_1231f4249963aa2efb93749a8e`: `CREATE INDEX "IDX_1231f4249963aa2efb93749a8e" ON public.order_dispatch_offer USING btree (order_id)`
- `IDX_21b60d43f182e2b1e8a30ea0a5`: `CREATE INDEX "IDX_21b60d43f182e2b1e8a30ea0a5" ON public.order_dispatch_offer USING btree (status)`
- `IDX_830f3888d1424414675f1c184d`: `CREATE INDEX "IDX_830f3888d1424414675f1c184d" ON public.order_dispatch_offer USING btree (distributor_id)`
- `IDX_9ff85bc9c62717502d1ad68216`: `CREATE INDEX "IDX_9ff85bc9c62717502d1ad68216" ON public.order_dispatch_offer USING btree ("expiresAt")`
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

Índices (además de la clave primaria):
- `IDX_05b8eaefed5471a643ee578c74`: `CREATE UNIQUE INDEX "IDX_05b8eaefed5471a643ee578c74" ON public.payment USING btree (gateway_payment_id) WHERE (gateway_payment_id IS NOT NULL)`
- `IDX_0cdad15fa39dd1ebace139096f`: `CREATE INDEX "IDX_0cdad15fa39dd1ebace139096f" ON public.payment USING btree (distributor_id)`
- `IDX_f5221735ace059250daac9d980`: `CREATE INDEX "IDX_f5221735ace059250daac9d980" ON public.payment USING btree (order_id)`

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

Claves únicas compuestas: (`distributor_id`, `number`).

Índices (además de la clave primaria):
- `IDX_purchase_order_estado`: `CREATE INDEX "IDX_purchase_order_estado" ON public.purchase_order USING btree (distributor_id, status)`
- `IDX_purchase_order_proveedor`: `CREATE INDEX "IDX_purchase_order_proveedor" ON public.purchase_order USING btree (supplier_id)`
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
| `cash_movement_id` | uuid | no |  |  |  | Lo completa la caja (M-D); sin clave foránea hasta que exista la tabla. |
| `status` | purchase_receipt_status_enum | sí |  |  | `'confirmed'::purchase_receipt_status_enum` | _(sin descripción documentada en el código)_ |
| `void_reason` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `voided_at` | timestamptz | no |  |  |  | _(sin descripción documentada en el código)_ |
| `voided_by_user_id` | uuid | no |  |  |  | _(sin descripción documentada en el código)_ |
| `batch_id` | uuid | sí |  |  |  | Lote del libro de movimientos que generó la recepción. |
| `void_batch_id` | uuid | no |  |  |  | Lote del contraasiento, si se anuló. |
| `notes` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

Claves únicas compuestas: (`distributor_id`, `number`), (`distributor_id`, `supplier_id`, `supplier_document_type`, `supplier_document_number`).

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

Claves únicas compuestas: (`batch_id`, `order_id`).

Índices (además de la clave primaria):
- `UQ_route_batch_stop_batch_order`: `CREATE UNIQUE INDEX "UQ_route_batch_stop_batch_order" ON public.route_batch_stop USING btree (batch_id, order_id)`

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

Restricciones `CHECK`:
- `CHK_stock_location_kind`: `CHECK (((kind = 'warehouse'::stock_location_kind_enum) = (warehouse_id IS NOT NULL)))`
- `CHK_stock_location_one_owner`: `CHECK ((num_nonnulls(warehouse_id, car_id) = 1))`

Índices (además de la clave primaria):
- `IDX_stock_location_distributor`: `CREATE INDEX "IDX_stock_location_distributor" ON public.stock_location USING btree (distributor_id)`
- `UQ_stock_location_car`: `CREATE UNIQUE INDEX "UQ_stock_location_car" ON public.stock_location USING btree (car_id)`
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

Restricciones `CHECK`:
- `CHK_stock_movement_cantidad`: `CHECK ((quantity > 0))`
- `CHK_stock_movement_destino_coherente`: `CHECK (((to_location_id IS NULL) = (to_condition IS NULL)))`
- `CHK_stock_movement_origen_coherente`: `CHECK (((from_location_id IS NULL) = (from_condition IS NULL)))`
- `CHK_stock_movement_origen_o_destino`: `CHECK (((from_location_id IS NOT NULL) OR (to_location_id IS NOT NULL)))`

Índices (además de la clave primaria):
- `IDX_stock_movement_destino`: `CREATE INDEX "IDX_stock_movement_destino" ON public.stock_movement USING btree (to_location_id)`
- `IDX_stock_movement_fecha`: `CREATE INDEX "IDX_stock_movement_fecha" ON public.stock_movement USING btree (distributor_id, occurred_at)`
- `IDX_stock_movement_garrafa_fecha`: `CREATE INDEX "IDX_stock_movement_garrafa_fecha" ON public.stock_movement USING btree (gas_cylinder_id, occurred_at)`
- `IDX_stock_movement_lote`: `CREATE INDEX "IDX_stock_movement_lote" ON public.stock_movement USING btree (batch_id)`
- `IDX_stock_movement_origen`: `CREATE INDEX "IDX_stock_movement_origen" ON public.stock_movement USING btree (from_location_id)`
- `IDX_stock_movement_referencia`: `CREATE INDEX "IDX_stock_movement_referencia" ON public.stock_movement USING btree (reference_type, reference_id)`
- `UQ_stock_movement_contraasiento`: `CREATE UNIQUE INDEX "UQ_stock_movement_contraasiento" ON public.stock_movement USING btree (reversed_movement_id) WHERE (reversed_movement_id IS NOT NULL)`
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

Índices (además de la clave primaria):
- `IDX_supplier_distributor`: `CREATE INDEX "IDX_supplier_distributor" ON public.supplier USING btree (distributor_id)`
- `UQ_supplier_cuit_vigente`: `CREATE UNIQUE INDEX "UQ_supplier_cuit_vigente" ON public.supplier USING btree (distributor_id, cuit) WHERE ("deletedAt" IS NULL)`

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

Índices (además de la clave primaria):
- `IDX_e87ae54beaee42b885813deb8e`: `CREATE INDEX "IDX_e87ae54beaee42b885813deb8e" ON public.time_slot USING btree (distributor_id)`

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

Claves únicas compuestas: (`distributor_id`, `number`).

Índices (además de la clave primaria):
- `IDX_truck_load_camion`: `CREATE INDEX "IDX_truck_load_camion" ON public.truck_load USING btree (car_id)`
- `IDX_truck_load_chofer`: `CREATE INDEX "IDX_truck_load_chofer" ON public.truck_load USING btree (delivery_id)`
- `IDX_truck_load_estado`: `CREATE INDEX "IDX_truck_load_estado" ON public.truck_load USING btree (distributor_id, status)`
- `IDX_truck_load_fecha`: `CREATE INDEX "IDX_truck_load_fecha" ON public.truck_load USING btree (distributor_id, business_date)`
- `UQ_truck_load_camion_abierta`: `CREATE UNIQUE INDEX "UQ_truck_load_camion_abierta" ON public.truck_load USING btree (car_id) WHERE (status = ANY (ARRAY['loading'::truck_load_status_enum, 'on_route'::truck_load_status_enum, 'returned'::truck_load_status_enum]))`
- `UQ_truck_load_chofer_abierta`: `CREATE UNIQUE INDEX "UQ_truck_load_chofer_abierta" ON public.truck_load USING btree (delivery_id) WHERE (status = ANY (ARRAY['loading'::truck_load_status_enum, 'on_route'::truck_load_status_enum, 'returned'::truck_load_status_enum]))`
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

Índices (además de la clave primaria):
- `IDX_user_email_lower`: `CREATE INDEX "IDX_user_email_lower" ON public."user" USING btree (lower((email)::text))`
- `UQ_01eea41349b6c9275aec646eee0`: `CREATE UNIQUE INDEX "UQ_01eea41349b6c9275aec646eee0" ON public."user" USING btree (phone_number)`
- `UQ_40fe3048b17f675b652c1999270`: `CREATE UNIQUE INDEX "UQ_40fe3048b17f675b652c1999270" ON public."user" USING btree (firebase_uid)`
- `UQ_e12875dfb3b1d92d7d7c5377e22`: `CREATE UNIQUE INDEX "UQ_e12875dfb3b1d92d7d7c5377e22" ON public."user" USING btree (email)`

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

Índices (además de la clave primaria):
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

Índices (además de la clave primaria):
- `IDX_warehouse_distributor`: `CREATE INDEX "IDX_warehouse_distributor" ON public.warehouse USING btree (distributor_id)`
- `UQ_warehouse_code_vigente`: `CREATE UNIQUE INDEX "UQ_warehouse_code_vigente" ON public.warehouse USING btree (distributor_id, code) WHERE ("deletedAt" IS NULL)`
- `UQ_warehouse_default_vigente`: `CREATE UNIQUE INDEX "UQ_warehouse_default_vigente" ON public.warehouse USING btree (distributor_id) WHERE (is_default AND ("deletedAt" IS NULL))`

> **Cobertura de las descripciones.** 109 de 674 columnas tienen descripción tomada del comentario de la entidad de TypeORM que las define; las que no la tienen en el código figuran arriba como «sin descripción documentada en el código» en lugar de inventarse una.

## Relaciones no declaradas

No hay ninguna: las 13 relaciones que en algún momento existieron sin `FOREIGN KEY` se declararon el 25/09/2026 (migración `DeclararRelacionesSinClaveForanea`). Hoy las 150 relaciones del dominio están todas declaradas.

### 1. Recargo express y tipo de vehículo

**Casos de uso:** CU-147 a CU-149 (I-7). **Qué resuelve:** Explicar el total de un pedido express y reconocer la moto sin depender de un texto libre.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `order` | `express_surcharge_amount` | numeric(12,2) | sí | Recargo de la modalidad express incluido en el total; cero en el reparto común. |
| `car` | `vehicle_type` | vehicle_type_enum | no | Tipo de vehículo normalizado, rellenado desde `type_car`; vacío hasta el relleno. |


Tipo enumerado `vehicle_type_enum`: `motorcycle`, `car`, `van`.

> **Decisión de modelado.** La compra express guarda el recargo para poder explicar el total después, igual que el pedido guarda la zona que lo originó. El tipo de vehículo es hoy texto libre (`type_car`: «Moto», «Auto»…) y la express depende de reconocer una moto: se agrega una columna enumerada y se rellena desde `type_car`.

### 2. Baja del envase y oferta de retiro

**Casos de uso:** CU-108 (I-8). **Qué resuelve:** Poder dar un envase de baja y atar la oferta de retiro a la entrega programada.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `cylinder` | `decommissioned_at` | timestamptz | no | Cuándo se dio de baja el envase; vacío mientras está en circulación. |
| `cylinder_recovery_notice` | `order_id` | uuid | no | Pedido de la entrega a la que se ató la oferta de retiro. |


> **Decisión de modelado.** El ciclo del envase no tiene un estado de baja: se agrega una baja lógica en vez de un valor de estado, para no tocar la máquina de estados que ya usan el despacho y la devolución. El aviso de recupero necesita saber a qué entrega se ató la oferta de retiro.

### 3. Configuración del despacho y de las tareas programadas

**Casos de uso:** CU-171 y CU-173 (I-1). **Qué resuelve:** Que el administrador configure el despacho y la frecuencia de las tareas de su distribuidora.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|


Valores nuevos del tipo enumerado `configurable_process_enum`: `dispatch`, `scheduled_tasks`.

> **Decisión de modelado.** Los parámetros del despacho y la frecuencia de las tareas programadas usan la misma tabla de configuración por distribuidora que los módulos inteligentes: sólo hace falta ampliar el tipo enumerado de procesos configurables.

### 4. Caja, rendición del chofer, cuentas corrientes y comisiones

**Casos de uso:** CU-225 a CU-245 (I-14). **Qué resuelve:** Llevar el dinero de la distribuidora —cajas con arqueo, rendición diaria del chofer, venta a crédito y comisiones por entrega— con un libro auditable en vez de saldos sueltos.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `cash_box` **(tabla nueva)** | `cash_box_id` | uuid | sí | Identificador. |
| `cash_box` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `cash_box` **(tabla nueva)** | `name` | varchar(80) | sí | Nombre de la caja. |
| `cash_box` **(tabla nueva)** | `kind` | cash_box_kind_enum | sí | Efectivo, banco o billetera. |
| `cash_box` **(tabla nueva)** | `balance` | numeric(14,2) | sí | Saldo; una restricción impide que una caja de efectivo quede en negativo. |
| `cash_box` **(tabla nueva)** | `requires_session` | boolean | sí | Si exige una sesión abierta para registrar movimientos. |
| `cash_box` **(tabla nueva)** | `is_active` | boolean | sí | Si la caja está activa. |
| `cash_box` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |
| `cash_box` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Última modificación. |
| `cash_box` **(tabla nueva)** | `deletedAt` | timestamptz | no | Baja lógica. |
| `cash_session` **(tabla nueva)** | `session_id` | uuid | sí | Identificador. |
| `cash_session` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `cash_session` **(tabla nueva)** | `cash_box_id` | uuid | sí | Caja que se abre. |
| `cash_session` **(tabla nueva)** | `status` | cash_session_status_enum | sí | Abierta o cerrada. |
| `cash_session` **(tabla nueva)** | `opened_at` | timestamptz | sí | Apertura. |
| `cash_session` **(tabla nueva)** | `opened_by_user_id` | uuid | sí | Administrador que la abrió. |
| `cash_session` **(tabla nueva)** | `opening_amount` | numeric(12,2) | sí | Monto con que se abrió. |
| `cash_session` **(tabla nueva)** | `closed_at` | timestamptz | no | Cierre. |
| `cash_session` **(tabla nueva)** | `closed_by_user_id` | uuid | no | Administrador que la cerró. |
| `cash_session` **(tabla nueva)** | `expected_amount` | numeric(12,2) | no | Monto que debía haber: el inicial más los movimientos de la sesión. |
| `cash_session` **(tabla nueva)** | `counted_amount` | numeric(12,2) | no | Monto contado en el arqueo. |
| `cash_session` **(tabla nueva)** | `difference` | numeric(12,2) | no | Contado menos esperado; negativa es faltante. |
| `cash_session` **(tabla nueva)** | `notes` | text | no | Observaciones del arqueo. |
| `cash_category` **(tabla nueva)** | `category_id` | uuid | sí | Identificador. |
| `cash_category` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `cash_category` **(tabla nueva)** | `name` | varchar(80) | sí | Nombre de la categoría. |
| `cash_category` **(tabla nueva)** | `direction` | cash_direction_enum | sí | Ingreso o egreso. |
| `cash_category` **(tabla nueva)** | `system_code` | cash_system_code_enum | no | Código con que los procesos automáticos la buscan; vacío en las propias. |
| `cash_category` **(tabla nueva)** | `is_active` | boolean | sí | Si se ofrece para movimientos nuevos. |
| `cash_category` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |
| `cash_category` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Última modificación. |
| `cash_movement` **(tabla nueva)** | `movement_id` | uuid | sí | Identificador. |
| `cash_movement` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `cash_movement` **(tabla nueva)** | `cash_box_id` | uuid | sí | Caja del asiento. |
| `cash_movement` **(tabla nueva)** | `session_id` | uuid | no | Sesión en que se asentó. |
| `cash_movement` **(tabla nueva)** | `direction` | cash_direction_enum | sí | Ingreso o egreso. |
| `cash_movement` **(tabla nueva)** | `amount` | numeric(12,2) | sí | Importe, siempre mayor que cero. |
| `cash_movement` **(tabla nueva)** | `category_id` | uuid | sí | Categoría del movimiento. |
| `cash_movement` **(tabla nueva)** | `method` | cash_method_enum | sí | Medio, informativo. |
| `cash_movement` **(tabla nueva)** | `occurred_at` | timestamptz | sí | Cuándo ocurrió. |
| `cash_movement` **(tabla nueva)** | `description` | varchar(255) | no | Descripción libre. |
| `cash_movement` **(tabla nueva)** | `reference_type` | cash_reference_type_enum | sí | Qué lo originó: carga manual, rendición, pago, liquidación, transferencia o anulación. |
| `cash_movement` **(tabla nueva)** | `reference_id` | uuid | no | Identificador de lo que lo originó. |
| `cash_movement` **(tabla nueva)** | `reverses_movement_id` | uuid | no | Movimiento al que anula; único: un movimiento se anula una sola vez. |
| `cash_movement` **(tabla nueva)** | `created_by_user_id` | uuid | sí | Quien lo asentó. |
| `cash_movement` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |
| `driver_settlement` **(tabla nueva)** | `settlement_id` | uuid | sí | Identificador. |
| `driver_settlement` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `driver_settlement` **(tabla nueva)** | `delivery_id` | uuid | sí | Chofer que rinde. |
| `driver_settlement` **(tabla nueva)** | `number` | integer | sí | Número correlativo por distribuidora. |
| `driver_settlement` **(tabla nueva)** | `business_date` | date | sí | Día argentino que se rinde. |
| `driver_settlement` **(tabla nueva)** | `status` | driver_settlement_status_enum | sí | Abierta, presentada o aprobada. |
| `driver_settlement` **(tabla nueva)** | `expected_cash` | numeric(12,2) | sí | Efectivo que debería entregar. |
| `driver_settlement` **(tabla nueva)** | `declared_cash` | numeric(12,2) | no | Efectivo que declara entregar. |
| `driver_settlement` **(tabla nueva)** | `driver_expenses` | numeric(12,2) | sí | Gastos pagados con la cobranza. |
| `driver_settlement` **(tabla nueva)** | `difference` | numeric(12,2) | no | Declarado más gastos menos esperado; negativa es faltante. |
| `driver_settlement` **(tabla nueva)** | `difference_resolution` | settlement_difference_resolution_enum | no | Cómo se resolvió la diferencia. |
| `driver_settlement` **(tabla nueva)** | `destination_cash_box_id` | uuid | no | Caja donde entró el efectivo. |
| `driver_settlement` **(tabla nueva)** | `cash_movement_id` | uuid | no | Ingreso a caja de la aprobación. |
| `driver_settlement` **(tabla nueva)** | `submitted_at` | timestamptz | no | Cuándo se presentó. |
| `driver_settlement` **(tabla nueva)** | `submitted_by_user_id` | uuid | no | Quien la presentó. |
| `driver_settlement` **(tabla nueva)** | `approved_at` | timestamptz | no | Cuándo se aprobó. |
| `driver_settlement` **(tabla nueva)** | `approved_by_user_id` | uuid | no | Administrador que la aprobó. |
| `driver_settlement` **(tabla nueva)** | `alerted_at` | timestamptz | no | Cuándo se avisó que seguía sin cerrar. |
| `driver_settlement` **(tabla nueva)** | `notes` | text | no | Observaciones. |
| `driver_settlement` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |
| `driver_settlement_order` **(tabla nueva)** | `settlement_order_id` | uuid | sí | Identificador. |
| `driver_settlement_order` **(tabla nueva)** | `settlement_id` | uuid | sí | Rendición que lo incluye. |
| `driver_settlement_order` **(tabla nueva)** | `order_id` | uuid | sí | Pedido rendido; único. |
| `driver_settlement_order` **(tabla nueva)** | `amount` | numeric(12,2) | sí | Importe cobrado. |
| `driver_settlement_order` **(tabla nueva)** | `payment_method` | order_paymentmethod_enum | sí | Medio de pago del pedido al rendirlo. |
| `driver_settlement_expense` **(tabla nueva)** | `expense_id` | uuid | sí | Identificador. |
| `driver_settlement_expense` **(tabla nueva)** | `settlement_id` | uuid | sí | Rendición que lo declara. |
| `driver_settlement_expense` **(tabla nueva)** | `category_id` | uuid | sí | Categoría del gasto. |
| `driver_settlement_expense` **(tabla nueva)** | `amount` | numeric(12,2) | sí | Importe pagado. |
| `driver_settlement_expense` **(tabla nueva)** | `description` | varchar(255) | no | Descripción libre. |
| `customer_account` **(tabla nueva)** | `account_id` | uuid | sí | Identificador. |
| `customer_account` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `customer_account` **(tabla nueva)** | `customer_user_id` | uuid | sí | Cliente titular. |
| `customer_account` **(tabla nueva)** | `business_name` | varchar(120) | sí | Razón social. |
| `customer_account` **(tabla nueva)** | `tax_id` | varchar(11) | no | CUIT. |
| `customer_account` **(tabla nueva)** | `tax_condition` | tax_condition_enum | sí | Condición fiscal. |
| `customer_account` **(tabla nueva)** | `credit_limit` | numeric(12,2) | sí | Límite de crédito. |
| `customer_account` **(tabla nueva)** | `payment_terms_days` | integer | sí | Plazo de pago en días. |
| `customer_account` **(tabla nueva)** | `status` | customer_account_status_enum | sí | Activa, bloqueada o cerrada. |
| `customer_account` **(tabla nueva)** | `balance` | numeric(14,2) | sí | Saldo; positivo es deuda del cliente. |
| `customer_account` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |
| `customer_account` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Última modificación. |
| `customer_account` **(tabla nueva)** | `deletedAt` | timestamptz | no | Baja lógica. |
| `customer_account_entry` **(tabla nueva)** | `entry_id` | uuid | sí | Identificador. |
| `customer_account_entry` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `customer_account_entry` **(tabla nueva)** | `account_id` | uuid | sí | Cuenta del asiento. |
| `customer_account_entry` **(tabla nueva)** | `type` | customer_entry_type_enum | sí | Cargo, pago, nota o anulación. |
| `customer_account_entry` **(tabla nueva)** | `amount` | numeric(12,2) | sí | Importe; el signo lo da el tipo. |
| `customer_account_entry` **(tabla nueva)** | `order_id` | uuid | no | Pedido que originó el cargo. |
| `customer_account_entry` **(tabla nueva)** | `due_date` | date | no | Vencimiento del cargo. |
| `customer_account_entry` **(tabla nueva)** | `payment_method` | cash_method_enum | no | Medio del pago. |
| `customer_account_entry` **(tabla nueva)** | `cash_movement_id` | uuid | no | Ingreso a caja del pago. |
| `customer_account_entry` **(tabla nueva)** | `collected_by_delivery_id` | uuid | no | Chofer que cobró en la calle. |
| `customer_account_entry` **(tabla nueva)** | `settlement_id` | uuid | no | Rendición en que entró lo cobrado. |
| `customer_account_entry` **(tabla nueva)** | `reverses_entry_id` | uuid | no | Asiento al que anula; único. |
| `customer_account_entry` **(tabla nueva)** | `description` | varchar(255) | no | Descripción o motivo. |
| `customer_account_entry` **(tabla nueva)** | `occurred_at` | timestamptz | sí | Cuándo ocurrió. |
| `customer_account_entry` **(tabla nueva)** | `created_by_user_id` | uuid | no | Quien lo asentó. |
| `customer_account_entry` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |
| `customer_account_allocation` **(tabla nueva)** | `allocation_id` | uuid | sí | Identificador. |
| `customer_account_allocation` **(tabla nueva)** | `debit_entry_id` | uuid | sí | Cargo que se cancela. |
| `customer_account_allocation` **(tabla nueva)** | `credit_entry_id` | uuid | sí | Pago o nota que lo cancela. |
| `customer_account_allocation` **(tabla nueva)** | `amount` | numeric(12,2) | sí | Importe aplicado. |
| `commission_rule` **(tabla nueva)** | `rule_id` | uuid | sí | Identificador. |
| `commission_rule` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `commission_rule` **(tabla nueva)** | `employee_id` | uuid | no | Empleado de la regla; vacío vale para todos los choferes. |
| `commission_rule` **(tabla nueva)** | `gas_cylinder_id` | uuid | no | Producto de la regla; vacío vale para todos. |
| `commission_rule` **(tabla nueva)** | `basis` | commission_basis_enum | sí | Por unidad, por pedido o porcentaje del total. |
| `commission_rule` **(tabla nueva)** | `value` | numeric(10,4) | sí | Monto o porcentaje, según la base. |
| `commission_rule` **(tabla nueva)** | `valid_from` | date | sí | Inicio de la vigencia. |
| `commission_rule` **(tabla nueva)** | `valid_to` | date | no | Fin de la vigencia. |
| `commission_rule` **(tabla nueva)** | `is_active` | boolean | sí | Si la regla está activa. |
| `commission_rule` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |
| `commission_rule` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Última modificación. |
| `commission_entry` **(tabla nueva)** | `entry_id` | uuid | sí | Identificador. |
| `commission_entry` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `commission_entry` **(tabla nueva)** | `employee_id` | uuid | sí | Empleado del asiento. |
| `commission_entry` **(tabla nueva)** | `type` | commission_entry_type_enum | sí | Comisión, faltante, multa, ajuste, saldo heredado o arrastre. |
| `commission_entry` **(tabla nueva)** | `amount` | numeric(12,2) | sí | Importe con signo; las deducciones son negativas. |
| `commission_entry` **(tabla nueva)** | `order_id` | uuid | no | Pedido que devengó la comisión. |
| `commission_entry` **(tabla nueva)** | `rule_id` | uuid | no | Regla aplicada. |
| `commission_entry` **(tabla nueva)** | `rule_snapshot` | jsonb | no | Copia de la regla con que se calculó. |
| `commission_entry` **(tabla nueva)** | `settlement_id` | uuid | no | Rendición que originó un faltante. |
| `commission_entry` **(tabla nueva)** | `liquidation_id` | uuid | no | Liquidación que lo incluye; vacío si está libre. |
| `commission_entry` **(tabla nueva)** | `description` | varchar(255) | no | Descripción o motivo. |
| `commission_entry` **(tabla nueva)** | `occurred_at` | timestamptz | sí | Cuándo ocurrió. |
| `commission_entry` **(tabla nueva)** | `created_by_user_id` | uuid | no | Quien lo asentó; vacío si fue el sistema. |
| `commission_entry` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |
| `driver_liquidation` **(tabla nueva)** | `liquidation_id` | uuid | sí | Identificador. |
| `driver_liquidation` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `driver_liquidation` **(tabla nueva)** | `number` | integer | sí | Número correlativo por distribuidora. |
| `driver_liquidation` **(tabla nueva)** | `employee_id` | uuid | sí | Empleado liquidado. |
| `driver_liquidation` **(tabla nueva)** | `period_from` | date | sí | Inicio del período. |
| `driver_liquidation` **(tabla nueva)** | `period_to` | date | sí | Fin del período. |
| `driver_liquidation` **(tabla nueva)** | `gross` | numeric(12,2) | sí | Suma de las comisiones. |
| `driver_liquidation` **(tabla nueva)** | `deductions` | numeric(12,2) | sí | Suma de las deducciones. |
| `driver_liquidation` **(tabla nueva)** | `net` | numeric(12,2) | sí | Neto a pagar. |
| `driver_liquidation` **(tabla nueva)** | `status` | driver_liquidation_status_enum | sí | Borrador, aprobada, pagada, cerrada sin pago o anulada. |
| `driver_liquidation` **(tabla nueva)** | `approved_at` | timestamptz | no | Cuándo se aprobó. |
| `driver_liquidation` **(tabla nueva)** | `approved_by_user_id` | uuid | no | Administrador que la aprobó. |
| `driver_liquidation` **(tabla nueva)** | `paid_at` | timestamptz | no | Cuándo se pagó. |
| `driver_liquidation` **(tabla nueva)** | `cash_movement_id` | uuid | no | Egreso de caja del pago. |
| `driver_liquidation` **(tabla nueva)** | `createdAt` | timestamptz | sí | Alta. |

`cash_box` — Cuenta de fondos de la distribuidora: efectivo, banco o billetera. Su saldo sólo cambia por el libro. Clave primaria `cash_box_id`. Referencias: `distributor_id` → `distributor`.
`cash_session` — Período entre una apertura y un cierre con arqueo de una caja. Clave primaria `session_id`. Referencias: `distributor_id` → `distributor`, `cash_box_id` → `cash_box`, `opened_by_user_id` → `user`, `closed_by_user_id` → `user`.
`cash_category` — Categoría de ingreso o de gasto; las de sistema se siembran y no se modifican. Clave primaria `category_id`. Referencias: `distributor_id` → `distributor`. Única: (`distributor_id`, `system_code`).
`cash_movement` — Asiento del libro de una caja; de sólo agregar, se corrige con un contraasiento. Clave primaria `movement_id`. Referencias: `distributor_id` → `distributor`, `cash_box_id` → `cash_box`, `session_id` → `cash_session`, `category_id` → `cash_category`, `reverses_movement_id` → `cash_movement`, `created_by_user_id` → `user`. Única: (`reverses_movement_id`).
`driver_settlement` — Rendición diaria del efectivo que cobró un chofer. Clave primaria `settlement_id`. Referencias: `distributor_id` → `distributor`, `delivery_id` → `delivery`, `destination_cash_box_id` → `cash_box`, `cash_movement_id` → `cash_movement`, `submitted_by_user_id` → `user`, `approved_by_user_id` → `user`.
`driver_settlement_order` — Pedido en efectivo incluido en una rendición; un pedido se rinde una sola vez. Clave primaria `settlement_order_id`. Referencias: `settlement_id` → `driver_settlement`, `order_id` → `order`. Única: (`order_id`).
`driver_settlement_expense` — Gasto que el chofer pagó con la cobranza. Clave primaria `expense_id`. Referencias: `settlement_id` → `driver_settlement`, `category_id` → `cash_category`.
`customer_account` — Cuenta corriente de un cliente en una distribuidora: crédito, plazo y saldo. Clave primaria `account_id`. Referencias: `distributor_id` → `distributor`, `customer_user_id` → `user`.
`customer_account_entry` — Asiento del libro de una cuenta corriente: cargo, pago, nota de crédito o de débito. Clave primaria `entry_id`. Referencias: `distributor_id` → `distributor`, `account_id` → `customer_account`, `order_id` → `order`, `cash_movement_id` → `cash_movement`, `collected_by_delivery_id` → `delivery`, `settlement_id` → `driver_settlement`, `reverses_entry_id` → `customer_account_entry`, `created_by_user_id` → `user`. Única: (`reverses_entry_id`).
`customer_account_allocation` — Aplicación de un pago o una nota de crédito a un cargo; alimenta la antigüedad de la deuda. Clave primaria `allocation_id`. Referencias: `debit_entry_id` → `customer_account_entry`, `credit_entry_id` → `customer_account_entry`.
`commission_rule` — Cuánto gana un chofer por entrega, con su alcance y su vigencia. Clave primaria `rule_id`. Referencias: `distributor_id` → `distributor`, `employee_id` → `employee`, `gas_cylinder_id` → `gas_cylinder`.
`commission_entry` — Asiento del libro de comisiones de un chofer: comisión, deducción o saldo heredado. Clave primaria `entry_id`. Referencias: `distributor_id` → `distributor`, `employee_id` → `employee`, `order_id` → `order`, `rule_id` → `commission_rule`, `settlement_id` → `driver_settlement`, `liquidation_id` → `driver_liquidation`, `created_by_user_id` → `user`.
`driver_liquidation` — Liquidación de las comisiones y las deducciones de un chofer en un período. Clave primaria `liquidation_id`. Referencias: `distributor_id` → `distributor`, `employee_id` → `employee`, `approved_by_user_id` → `user`, `cash_movement_id` → `cash_movement`.

Tipo enumerado `cash_box_kind_enum`: `cash`, `bank`, `wallet`.
Tipo enumerado `cash_session_status_enum`: `open`, `closed`.
Tipo enumerado `cash_direction_enum`: `income`, `expense`.
Tipo enumerado `cash_system_code_enum`: `driver_settlement`, `customer_payment`, `purchase`, `fuel`, `traffic_fine`, `commission_payment`, `cash_difference`, `box_transfer`.
Tipo enumerado `cash_method_enum`: `cash`, `transfer`, `card`, `mercadopago`, `check`.
Tipo enumerado `cash_reference_type_enum`: `manual`, `driver_settlement`, `customer_payment`, `purchase_receipt`, `fuel_load`, `traffic_fine`, `driver_liquidation`, `box_transfer`, `reversal`.
Tipo enumerado `driver_settlement_status_enum`: `open`, `submitted`, `approved`.
Tipo enumerado `settlement_difference_resolution_enum`: `none`, `charged_to_driver`, `absorbed`.
Tipo enumerado `tax_condition_enum`: `registered`, `monotax`, `exempt`, `final_consumer`.
Tipo enumerado `customer_account_status_enum`: `active`, `blocked`, `closed`.
Tipo enumerado `customer_entry_type_enum`: `sale_charge`, `payment`, `credit_note`, `debit_note`, `reversal`.
Tipo enumerado `commission_basis_enum`: `per_unit`, `per_order`, `percent_of_total`.
Tipo enumerado `commission_entry_type_enum`: `delivery_commission`, `settlement_shortage`, `traffic_fine`, `adjustment`, `legacy_balance`, `carry_forward`.
Tipo enumerado `driver_liquidation_status_enum`: `draft`, `approved`, `paid`, `closed`, `voided`.

Valores nuevos del tipo enumerado `order_paymentmethod_enum`: `account`.
Valores nuevos del tipo enumerado `order_paymenttype_enum`: `account`.

> **Decisión de modelado.** Cinco libros de sólo agregar (`cash_movement`, `customer_account_entry`, `commission_entry`, y las rendiciones y liquidaciones que los alimentan) sostienen el dinero de la distribuidora. Los libros se corrigen con contraasiento y rechazan todo `UPDATE` y todo `DELETE` por un disparador, igual que `audit_log`. El saldo de `cash_box` y de `customer_account` es una copia del libro que sólo cambia por el punto único de escritura, y una conciliación nocturna compara las dos. Hay dos índices únicos parciales que este modelo no puede dibujar: una sesión abierta por caja (`WHERE status = 'open'`) y una cuenta vigente por cliente y distribuidora (`WHERE "deletedAt" IS NULL`). El turno del camión (`truck_load_id`) y la carga de combustible (`fuel_load_id`) se agregan a la rendición y a sus gastos cuando se integren los módulos de stock y de flota ampliada; hoy esas tablas no existen. Las comisiones cuelgan del empleado (`employee`, del módulo de personal, que ya está construido), de modo que un chofer cobra comisión como empleado.

### 5. Personal y legajos

**Casos de uso:** CU-183 a CU-194 y CU-246 (I-11). **Qué resuelve:** Llevar la asistencia, las licencias y la documentación con vencimiento de cada persona que trabaja en la distribuidora, y que ese control inhabilite para el despacho a quien no esté en regla.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `maintenance_plan` | `document_kind` | maintenance_document_kind_enum | no | Qué documento controla el plan: le dice al panel qué formulario mostrar y al sistema qué forma de detalle validar. |
| `maintenance_plan` | `applies_to_categories` | job_position_category_enum[] | no | Categorías de puesto a las que aplica el plan; vacío significa todas. |
| `maintenance_task` | `employee_id` | uuid | no | Empleado dueño de la tarea; obligatorio si el plan es de sujeto empleado. |
| `maintenance_task` | `valid_from` | timestamptz | no | Inicio de la vigencia del documento (póliza, habilitación o documentación del personal); lo usa el prorrateo de la prima. |
| `maintenance_task` | `details` | jsonb | no | Datos propios del tipo de documento (número de certificado, aseguradora, póliza, cobertura, franquicia, cuotas), con la forma que fija cada plan. |
| `employee_attendance` **(tabla nueva)** | `attendance_id` | uuid | sí | Identificador. |
| `employee_attendance` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `employee_attendance` **(tabla nueva)** | `employee_id` | uuid | sí | Empleado de la jornada. |
| `employee_attendance` **(tabla nueva)** | `work_date` | date | sí | Día argentino del ingreso. |
| `employee_attendance` **(tabla nueva)** | `check_in_at` | timestamptz | sí | Ingreso. |
| `employee_attendance` **(tabla nueva)** | `check_out_at` | timestamptz | no | Egreso; vacío mientras la jornada está abierta. |
| `employee_attendance` **(tabla nueva)** | `source` | attendance_source_enum | sí | Panel o aplicación del chofer. |
| `employee_attendance` **(tabla nueva)** | `recorded_by_user_id` | uuid | no | Usuario que la cargó. |
| `employee_attendance` **(tabla nueva)** | `notes` | text | no | Observación; obligatoria al corregir. |
| `employee_attendance` **(tabla nueva)** | `createdAt` | timestamptz | sí | Cuándo se creó. |
| `employee_attendance` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Cuándo se modificó por última vez. |
| `employee_leave` **(tabla nueva)** | `leave_id` | uuid | sí | Identificador. |
| `employee_leave` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `employee_leave` **(tabla nueva)** | `employee_id` | uuid | sí | Empleado de la licencia. |
| `employee_leave` **(tabla nueva)** | `type` | employee_leave_type_enum | sí | Tipo de licencia o ausencia. |
| `employee_leave` **(tabla nueva)** | `start_date` | date | sí | Primer día. |
| `employee_leave` **(tabla nueva)** | `end_date` | date | sí | Último día, inclusive. |
| `employee_leave` **(tabla nueva)** | `days` | integer | sí | Días corridos del período. |
| `employee_leave` **(tabla nueva)** | `status` | employee_leave_status_enum | sí | Solicitada, aprobada, rechazada o cancelada. |
| `employee_leave` **(tabla nueva)** | `reason` | text | no | Motivo de la solicitud. |
| `employee_leave` **(tabla nueva)** | `rejection_reason` | text | no | Motivo del rechazo; obligatorio al rechazar. |
| `employee_leave` **(tabla nueva)** | `requested_by_user_id` | uuid | no | Usuario que la cargó. |
| `employee_leave` **(tabla nueva)** | `decided_by_user_id` | uuid | no | Administrador que la resolvió. |
| `employee_leave` **(tabla nueva)** | `decided_at` | timestamptz | no | Cuándo se resolvió. |
| `employee_leave` **(tabla nueva)** | `createdAt` | timestamptz | sí | Cuándo se creó. |
| `employee_leave` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Cuándo se modificó por última vez. |

`employee_attendance` — Una jornada de un empleado: su ingreso y su egreso. Clave primaria `attendance_id`. Referencias: `distributor_id` → `distributor`, `employee_id` → `employee`, `recorded_by_user_id` → `user`.
`employee_leave` — Licencia o ausencia de un empleado, con su período y su estado. Clave primaria `leave_id`. Referencias: `distributor_id` → `distributor`, `employee_id` → `employee`, `requested_by_user_id` → `user`, `decided_by_user_id` → `user`.

Tipo enumerado `attendance_source_enum`: `panel`, `driver_app`.
Tipo enumerado `employee_leave_type_enum`: `vacation`, `sick`, `work_accident`, `study`, `marriage`, `birth`, `bereavement`, `unpaid`, `suspension`, `unjustified_absence`, `other`.
Tipo enumerado `employee_leave_status_enum`: `requested`, `approved`, `rejected`, `cancelled`.
Tipo enumerado `maintenance_document_kind_enum`: `insurance`, `vtv`, `hazmat_vehicle_permit`, `driver_license`, `hazmat_driver_course`, `psychophysical`, `art_coverage`, `service`, `generic`.

Valores nuevos del tipo enumerado `maintenance_subject_enum`: `employee`.

> **Decisión de modelado.** Los puestos (`job_position`) y los legajos (`employee`) ya están construidos y salen de la base: todo empleado existe como legajo, tenga o no cuenta de acceso, un chofer es un empleado cuya cuenta tiene el perfil de reparto, y ayudantes, depósito y vendedores son legajos sin cuenta (sin roles nuevos). Falta construir lo que cuelga del legajo. La documentación con vencimiento del personal —licencia de conducir, curso de mercancías peligrosas, examen psicofísico, alta en la ART— no tiene tabla propia: reutiliza el plan y la tarea de mantenimiento con un dueño empleado, y hereda los adjuntos, la pantalla de vencimientos, el aviso diario y el bloqueo de despacho que ya leen esas tablas; `delivery_id` queda como columna heredada. Los adjuntos del legajo van en una tabla genérica con dueño (`owner_type`, `owner_id`), sin clave foránea a propósito porque el dueño es polimórfico: lo valida un puerto que registra cada módulo. Dos licencias del mismo empleado no pueden superponerse: lo impide una restricción de exclusión de la base (`btree_gist`), no sólo el servicio.

### 6. Flota ampliada: combustible, multas y siniestros

**Casos de uso:** CU-195 a CU-202 (I-12). **Qué resuelve:** Llevar las cargas de combustible, las multas de tránsito y los siniestros de cada vehículo, para conocer su consumo y su costo.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `car` | `fuel_type` | fuel_type_enum | no | Combustible que usa el vehículo; es el que se propone en cada carga. |
| `car` | `tank_capacity_liters` | numeric(6,2) | no | Litros que entran en el tanque; una carga no puede superarlos en más de un 5 %. |
| `fuel_load` **(tabla nueva)** | `fuel_load_id` | uuid | sí | Identificador. |
| `fuel_load` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `fuel_load` **(tabla nueva)** | `car_id` | uuid | sí | Vehículo que cargó. |
| `fuel_load` **(tabla nueva)** | `employee_id` | uuid | no | Empleado que hizo la carga. |
| `fuel_load` **(tabla nueva)** | `loaded_at` | timestamptz | sí | Cuándo se hizo la carga. |
| `fuel_load` **(tabla nueva)** | `fuel_type` | fuel_type_enum | sí | Combustible cargado; por omisión el del vehículo. |
| `fuel_load` **(tabla nueva)** | `liters` | numeric(10,2) | sí | Litros cargados; mayores que cero. |
| `fuel_load` **(tabla nueva)** | `unit_price` | numeric(12,3) | sí | Precio de cada litro. |
| `fuel_load` **(tabla nueva)** | `total_amount` | numeric(12,2) | sí | Importe total; coincide con litros por precio, con un 1 % de tolerancia. |
| `fuel_load` **(tabla nueva)** | `odometer_km` | integer | sí | Kilometraje del tablero; no puede ser menor que el de la carga anterior. |
| `fuel_load` **(tabla nueva)** | `is_full_tank` | boolean | sí | Si se llenó el tanque: base del cálculo de consumo. |
| `fuel_load` **(tabla nueva)** | `station` | varchar(120) | no | Estación de servicio. |
| `fuel_load` **(tabla nueva)** | `payment_method` | fuel_payment_method_enum | sí | Caja, efectivo del chofer, tarjeta o cuenta corriente de combustible. |
| `fuel_load` **(tabla nueva)** | `receipt_number` | varchar(40) | no | Número del comprobante. |
| `fuel_load` **(tabla nueva)** | `cash_movement_id` | uuid | no | Movimiento de caja que originó el pago; lo completa el módulo de caja. |
| `fuel_load` **(tabla nueva)** | `anomaly` | boolean | sí | El consumo del tramo se aparta más de un 25 % del promedio. |
| `fuel_load` **(tabla nueva)** | `notes` | text | no | Observaciones de quien cargó. |
| `fuel_load` **(tabla nueva)** | `created_by_user_id` | uuid | no | Quién la registró. |
| `fuel_load` **(tabla nueva)** | `createdAt` | timestamptz | sí | Cuándo se registró. |
| `fuel_load` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Última modificación. |
| `fuel_load` **(tabla nueva)** | `deletedAt` | timestamptz | no | Cuándo se anuló; una carga anulada no cuenta en los cálculos. |
| `traffic_fine` **(tabla nueva)** | `fine_id` | uuid | sí | Identificador. |
| `traffic_fine` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `traffic_fine` **(tabla nueva)** | `car_id` | uuid | sí | Vehículo multado. |
| `traffic_fine` **(tabla nueva)** | `employee_id` | uuid | no | Empleado responsable; se deduce de la asignación de vehículo abierta al momento de la infracción. |
| `traffic_fine` **(tabla nueva)** | `occurred_at` | timestamptz | sí | Cuándo ocurrió la infracción. |
| `traffic_fine` **(tabla nueva)** | `jurisdiction` | varchar(80) | sí | Jurisdicción que labró el acta. |
| `traffic_fine` **(tabla nueva)** | `act_number` | varchar(40) | sí | Número del acta; único por distribuidora y jurisdicción. |
| `traffic_fine` **(tabla nueva)** | `infraction` | text | sí | Descripción de la infracción. |
| `traffic_fine` **(tabla nueva)** | `amount` | numeric(12,2) | sí | Importe de la multa. |
| `traffic_fine` **(tabla nueva)** | `voluntary_payment_amount` | numeric(12,2) | no | Importe con el descuento por pagar antes. |
| `traffic_fine` **(tabla nueva)** | `due_date` | date | no | Fecha de vencimiento del pago. |
| `traffic_fine` **(tabla nueva)** | `status` | traffic_fine_status_enum | sí | Pendiente, apelada, pagada o anulada. |
| `traffic_fine` **(tabla nueva)** | `paid_at` | timestamptz | no | Cuándo se pagó. |
| `traffic_fine` **(tabla nueva)** | `paid_amount` | numeric(12,2) | no | Importe efectivamente pagado. |
| `traffic_fine` **(tabla nueva)** | `charged_to_employee` | boolean | sí | Si la asume el empleado: se descuenta en su liquidación. |
| `traffic_fine` **(tabla nueva)** | `cash_movement_id` | uuid | no | Movimiento de caja del pago; lo completa el módulo de caja. |
| `traffic_fine` **(tabla nueva)** | `void_reason` | text | no | Motivo con el que se anuló; obligatorio al anular. |
| `traffic_fine` **(tabla nueva)** | `alerted_at` | timestamptz | no | Cuándo se avisó del vencimiento, para no repetir el aviso. |
| `traffic_fine` **(tabla nueva)** | `createdAt` | timestamptz | sí | Cuándo se registró. |
| `traffic_fine` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Última modificación. |
| `vehicle_accident` **(tabla nueva)** | `accident_id` | uuid | sí | Identificador. |
| `vehicle_accident` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `vehicle_accident` **(tabla nueva)** | `car_id` | uuid | sí | Vehículo siniestrado. |
| `vehicle_accident` **(tabla nueva)** | `employee_id` | uuid | no | Empleado que conducía. |
| `vehicle_accident` **(tabla nueva)** | `occurred_at` | timestamptz | sí | Cuándo ocurrió. |
| `vehicle_accident` **(tabla nueva)** | `location` | geometry(Point,4326) | no | Punto donde ocurrió. |
| `vehicle_accident` **(tabla nueva)** | `address` | text | no | Domicilio aproximado. |
| `vehicle_accident` **(tabla nueva)** | `description` | text | sí | Qué pasó. |
| `vehicle_accident` **(tabla nueva)** | `injuries` | boolean | sí | Si hubo personas heridas. |
| `vehicle_accident` **(tabla nueva)** | `third_parties_involved` | boolean | sí | Si hubo terceros involucrados. |
| `vehicle_accident` **(tabla nueva)** | `hazmat_release` | boolean | sí | Si hubo fuga o derrame de gas: obliga a avisar a los administradores. |
| `vehicle_accident` **(tabla nueva)** | `police_report_number` | varchar(40) | no | Número de la denuncia policial. |
| `vehicle_accident` **(tabla nueva)** | `insurer_claim_number` | varchar(40) | no | Número del reclamo a la aseguradora. |
| `vehicle_accident` **(tabla nueva)** | `status` | vehicle_accident_status_enum | sí | Denunciado, en revisión, en reparación o cerrado. |
| `vehicle_accident` **(tabla nueva)** | `vehicle_unusable` | boolean | sí | Si el vehículo no puede circular: pasa a fuera de servicio. |
| `vehicle_accident` **(tabla nueva)** | `repair_cost` | numeric(12,2) | no | Costo de la reparación. |
| `vehicle_accident` **(tabla nueva)** | `insurer_reimbursement` | numeric(12,2) | no | Lo que reintegró la aseguradora. |
| `vehicle_accident` **(tabla nueva)** | `deductible_amount` | numeric(12,2) | no | Franquicia a cargo de la distribuidora. |
| `vehicle_accident` **(tabla nueva)** | `closed_at` | timestamptz | no | Cuándo se cerró. |
| `vehicle_accident` **(tabla nueva)** | `createdAt` | timestamptz | sí | Cuándo se registró. |
| `vehicle_accident` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Última modificación. |

`fuel_load` — Una carga de combustible de un vehículo, con su kilometraje y su importe. Clave primaria `fuel_load_id`. Referencias: `distributor_id` → `distributor`, `car_id` → `car`, `employee_id` → `employee`, `created_by_user_id` → `user`.
`traffic_fine` — Una multa de tránsito de un vehículo, con su ciclo de pendiente a pagada o anulada. Clave primaria `fine_id`. Referencias: `distributor_id` → `distributor`, `car_id` → `car`, `employee_id` → `employee`. Única: (`distributor_id`, `jurisdiction`, `act_number`).
`vehicle_accident` — Un siniestro de un vehículo, de denunciado a cerrado, con sus costos. Clave primaria `accident_id`. Referencias: `distributor_id` → `distributor`, `car_id` → `car`, `employee_id` → `employee`.

Tipo enumerado `fuel_type_enum`: `diesel`, `gasoline`, `cng`, `lpg`.
Tipo enumerado `fuel_payment_method_enum`: `cash_box`, `driver_cash`, `card`, `fuel_account`.
Tipo enumerado `traffic_fine_status_enum`: `pending`, `appealed`, `paid`, `voided`.
Tipo enumerado `vehicle_accident_status_enum`: `reported`, `under_review`, `repairing`, `closed`.

> **Decisión de modelado.** La carga de combustible, la multa y el siniestro son registros propios del vehículo y no columnas de `car`: cada uno tiene fecha, importe y ciclo de vida, y alimentan el costo por vehículo. El siniestro no se mezcla con `incident`, que es el contratiempo de calidad de un pedido. El empleado se referencia por `employee_id` y no por `delivery`, porque el responsable de una multa o el que carga combustible puede ser un empleado sin cuenta de acceso. `cash_movement_id` queda sin clave foránea hasta que exista el módulo de caja (I-14).

### 7. Flota ampliada: neumáticos

**Casos de uso:** CU-205 y CU-206 (I-12, opcional). **Qué resuelve:** Llevar cada neumático y sus movimientos —montaje, desmontaje, rotación, recapado y baja— para saber cuántos kilómetros recorrió.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `tire` **(tabla nueva)** | `tire_id` | uuid | sí | Identificador. |
| `tire` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `tire` **(tabla nueva)** | `car_id` | uuid | no | Vehículo en el que está montado, si lo está. |
| `tire` **(tabla nueva)** | `serial` | varchar(40) | sí | Número de serie del neumático; único por distribuidora. |
| `tire` **(tabla nueva)** | `brand` | varchar(60) | sí | Marca. |
| `tire` **(tabla nueva)** | `size` | varchar(30) | sí | Medida del neumático. |
| `tire` **(tabla nueva)** | `cost` | numeric(12,2) | sí | Costo de compra. |
| `tire` **(tabla nueva)** | `status` | tire_status_enum | sí | En depósito, montado o dado de baja. |
| `tire` **(tabla nueva)** | `position` | varchar(6) | no | Código corto de la posición en el vehículo. |
| `tire` **(tabla nueva)** | `mounted_odometer_km` | integer | no | Kilometraje del vehículo al montarlo. |
| `tire` **(tabla nueva)** | `createdAt` | timestamptz | sí | Cuándo se registró. |
| `tire` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Última modificación. |
| `tire_event` **(tabla nueva)** | `event_id` | uuid | sí | Identificador. |
| `tire_event` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `tire_event` **(tabla nueva)** | `tire_id` | uuid | sí | Neumático movido. |
| `tire_event` **(tabla nueva)** | `car_id` | uuid | no | Vehículo del movimiento, si corresponde. |
| `tire_event` **(tabla nueva)** | `event_type` | tire_event_type_enum | sí | Montaje, desmontaje, rotación, recapado o baja. |
| `tire_event` **(tabla nueva)** | `odometer_km` | integer | sí | Kilometraje del vehículo en el movimiento. |
| `tire_event` **(tabla nueva)** | `position` | varchar(6) | no | Posición de destino, en un montaje o una rotación. |
| `tire_event` **(tabla nueva)** | `occurred_at` | timestamptz | sí | Cuándo ocurrió. |
| `tire_event` **(tabla nueva)** | `created_by_user_id` | uuid | no | Quién lo registró. |

`tire` — Un neumático de la distribuidora, en depósito, montado en un vehículo o dado de baja. Clave primaria `tire_id`. Referencias: `distributor_id` → `distributor`, `car_id` → `car`. Única: (`distributor_id`, `serial`).
`tire_event` — Un movimiento de un neumático; el libro no se modifica. Clave primaria `event_id`. Referencias: `distributor_id` → `distributor`, `tire_id` → `tire`, `car_id` → `car`, `created_by_user_id` → `user`.

Tipo enumerado `tire_status_enum`: `in_stock`, `mounted`, `retired`.
Tipo enumerado `tire_event_type_enum`: `mount`, `unmount`, `rotate`, `retread`, `retire`.

> **Decisión de modelado.** Funcionalidad opcional del módulo, que se puede construir aparte. Los movimientos del neumático son un libro que no se modifica: el estado y la posición actuales del neumático se guardan en `tire` para no recorrer el historial en cada consulta.

## Tipos enumerados

| Tipo | Valores | Estado |
|---|---|---|
| `address_geocode_precision_enum` | `exact`, `approximate`, `unresolved` | implementado |
| `attachment_owner_type_enum` | `employee`, `fuel_load`, `traffic_fine`, `vehicle_accident`, `purchase_receipt`, `stock_adjustment`, `driver_settlement`, `cash_movement`, `customer_account_entry` | implementado |
| `audit_result_enum` | `success`, `failure` | implementado |
| `claims_status_enum` | `pending`, `in_process`, `resolved`, `rejected` | implementado |
| `configurable_process_enum` | `fleet_planner`, `repurchase`, `route_batching`, `cylinder_recovery`, `express_dispatch`, `stock_control` | implementado |
| `coverage_zone_surcharge_type_enum` | `fixed`, `percentage` | implementado |
| `cylinder_inspection_result_enum` | `approved`, `conditional`, `rejected` | implementado |
| `cylinder_movement_from_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned`, `retired` | implementado |
| `cylinder_movement_to_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned`, `retired` | implementado |
| `cylinder_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned`, `retired` | implementado |
| `distributor_status_enum` | `active`, `suspended` | implementado |
| `employee_document_type_enum` | `dni`, `passport`, `other` | implementado |
| `employee_status_enum` | `active`, `terminated` | implementado |
| `employee_termination_reason_enum` | `resignation`, `dismissal`, `end_of_contract`, `retirement`, `other` | implementado |
| `employment_type_enum` | `permanent`, `fixed_term`, `part_time`, `contractor` | implementado |
| `fleet_status_enum` | `active`, `in_service`, `grounded` | implementado |
| `incident_moment_enum` | `pre_delivery`, `in_delivery`, `post_delivery` | implementado |
| `incident_status_enum` | `open`, `resolved`, `discarded` | implementado |
| `incident_type_enum` | `damaged`, `out_of_stock`, `no_show`, `unpaid_collection`, `other` | implementado |
| `job_position_category_enum` | `driver`, `helper`, `warehouse`, `administration`, `sales`, `management`, `other` | implementado |
| `maintenance_criticality_enum` | `blocking`, `non_blocking` | implementado |
| `maintenance_subject_enum` | `vehicle`, `driver` | implementado |
| `maintenance_task_status_enum` | `forecast`, `scheduled`, `in_progress`, `done`, `overdue`, `cancelled` | implementado |
| `maintenance_trigger_enum` | `by_km`, `by_time`, `by_fixed_date` | implementado |
| `order_delivery_mode_enum` | `standard`, `express` | implementado |
| `order_dispatch_offer_status_enum` | `offered`, `accepted`, `rejected`, `expired`, `superseded` | implementado |
| `order_paymentmethod_enum` | `cash`, `mercadopago`, `transfer` | implementado |
| `order_paymentstatus_enum` | `pending`, `paid`, `failed`, `unpaid`, `written_off` | implementado |
| `order_paymenttype_enum` | `cash`, `online` | implementado |
| `order_status_enum` | `reserved`, `pending`, `accepted`, `on_the_way`, `delivered`, `cancelled` | implementado |
| `order_zone_surcharge_type_enum` | `fixed`, `percentage` | implementado |
| `payment_gateway_enum` | `mercadopago`, `cash` | implementado |
| `payment_integration_enum` | `checkout_pro`, `cash` | implementado |
| `payment_status_enum` | `pending`, `approved`, `rejected`, `cancelled`, `refunded` | implementado |
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
| `truck_load_status_enum` | `loading`, `on_route`, `returned`, `closed`, `closed_with_difference`, `cancelled` | implementado |
| `warehouse_kind_enum` | `depot`, `branch` | implementado |
| `attendance_source_enum` | `panel`, `driver_app` | propuesto |
| `cash_box_kind_enum` | `cash`, `bank`, `wallet` | propuesto |
| `cash_direction_enum` | `income`, `expense` | propuesto |
| `cash_method_enum` | `cash`, `transfer`, `card`, `mercadopago`, `check` | propuesto |
| `cash_reference_type_enum` | `manual`, `driver_settlement`, `customer_payment`, `purchase_receipt`, `fuel_load`, `traffic_fine`, `driver_liquidation`, `box_transfer`, `reversal` | propuesto |
| `cash_session_status_enum` | `open`, `closed` | propuesto |
| `cash_system_code_enum` | `driver_settlement`, `customer_payment`, `purchase`, `fuel`, `traffic_fine`, `commission_payment`, `cash_difference`, `box_transfer` | propuesto |
| `commission_basis_enum` | `per_unit`, `per_order`, `percent_of_total` | propuesto |
| `commission_entry_type_enum` | `delivery_commission`, `settlement_shortage`, `traffic_fine`, `adjustment`, `legacy_balance`, `carry_forward` | propuesto |
| `customer_account_status_enum` | `active`, `blocked`, `closed` | propuesto |
| `customer_entry_type_enum` | `sale_charge`, `payment`, `credit_note`, `debit_note`, `reversal` | propuesto |
| `driver_liquidation_status_enum` | `draft`, `approved`, `paid`, `closed`, `voided` | propuesto |
| `driver_settlement_status_enum` | `open`, `submitted`, `approved` | propuesto |
| `employee_leave_status_enum` | `requested`, `approved`, `rejected`, `cancelled` | propuesto |
| `employee_leave_type_enum` | `vacation`, `sick`, `work_accident`, `study`, `marriage`, `birth`, `bereavement`, `unpaid`, `suspension`, `unjustified_absence`, `other` | propuesto |
| `fuel_payment_method_enum` | `cash_box`, `driver_cash`, `card`, `fuel_account` | propuesto |
| `fuel_type_enum` | `diesel`, `gasoline`, `cng`, `lpg` | propuesto |
| `maintenance_document_kind_enum` | `insurance`, `vtv`, `hazmat_vehicle_permit`, `driver_license`, `hazmat_driver_course`, `psychophysical`, `art_coverage`, `service`, `generic` | propuesto |
| `settlement_difference_resolution_enum` | `none`, `charged_to_driver`, `absorbed` | propuesto |
| `tax_condition_enum` | `registered`, `monotax`, `exempt`, `final_consumer` | propuesto |
| `tire_event_type_enum` | `mount`, `unmount`, `rotate`, `retread`, `retire` | propuesto |
| `tire_status_enum` | `in_stock`, `mounted`, `retired` | propuesto |
| `traffic_fine_status_enum` | `pending`, `appealed`, `paid`, `voided` | propuesto |
| `vehicle_accident_status_enum` | `reported`, `under_review`, `repairing`, `closed` | propuesto |
| `vehicle_type_enum` | `motorcycle`, `car`, `van` | propuesto |
