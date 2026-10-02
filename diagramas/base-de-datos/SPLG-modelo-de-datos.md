# Modelo de Datos — SPLG

40 tablas y 93 claves foráneas, leídas de la base en ejecución.

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
| `photoUrl` | varchar | no |  |  |  | _(sin descripción documentada en el código)_ |
| `status` | claims_status_enum | sí |  |  | `'pending'::claims_status_enum` | _(sin descripción documentada en el código)_ |
| `resolutionNote` | text | no |  |  |  | _(sin descripción documentada en el código)_ |
| `createdAt` | timestamp | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

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

Índices (además de la clave primaria):
- `IDX_02331b27890084627684d99ec5`: `CREATE UNIQUE INDEX "IDX_02331b27890084627684d99ec5" ON public.distributor USING btree (slug)`
- `UQ_02331b27890084627684d99ec5b`: `CREATE UNIQUE INDEX "UQ_02331b27890084627684d99ec5b" ON public.distributor USING btree (slug)`

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

Claves únicas compuestas: (`gas_cylinder_id`, `quantity`).

Restricciones `CHECK`:
- `CHK_promocion_cantidad`: `CHECK ((quantity >= 2))`
- `CHK_promocion_descuento`: `CHECK (((discount_percentage > (0)::numeric) AND (discount_percentage <= (100)::numeric)))`

Índices (además de la clave primaria):
- `UQ_promocion_producto_cantidad`: `CREATE UNIQUE INDEX "UQ_promocion_producto_cantidad" ON public.gas_cylinder_promotion USING btree (gas_cylinder_id, quantity)`

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

Índices (además de la clave primaria):
- `IDX_8a89ba6c226022354d0d8b4ada`: `CREATE INDEX "IDX_8a89ba6c226022354d0d8b4ada" ON public.incident USING btree (order_id)`
- `IDX_a2223c18baa97faf54118f95bd`: `CREATE INDEX "IDX_a2223c18baa97faf54118f95bd" ON public.incident USING btree (distributor_id)`

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
| `storage_key` | varchar(255) | sí |  |  |  | Clave dentro del `StoragePort` activo (disco local o S3). |
| `original_name` | varchar(255) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `mime_type` | varchar(100) | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `size_bytes` | integer | sí |  |  |  | _(sin descripción documentada en el código)_ |
| `uploaded_by_user_id` | uuid | sí | FK | `user.user_id` |  | _(sin descripción documentada en el código)_ |
| `uploaded_at` | timestamptz | sí |  |  | `now()` | _(sin descripción documentada en el código)_ |

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
| `acceptedAt` | timestamp | no |  |  |  | _(sin descripción documentada en el código)_ |
| `onTheWayAt` | timestamp | no |  |  |  | _(sin descripción documentada en el código)_ |
| `deliveredAt` | timestamp | no |  |  |  | _(sin descripción documentada en el código)_ |
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

Claves únicas compuestas: (`order_id`, `from_role`).

Índices (además de la clave primaria):
- `IDX_6f590ebbc097c4ed21d5d3e11e`: `CREATE INDEX "IDX_6f590ebbc097c4ed21d5d3e11e" ON public.rating USING btree (to_user_id)`
- `IDX_b46b63fc1ddf2135e1ed37069a`: `CREATE INDEX "IDX_b46b63fc1ddf2135e1ed37069a" ON public.rating USING btree (distributor_id)`
- `IDX_beb6f44b22a7f1ed7cad984a2e`: `CREATE INDEX "IDX_beb6f44b22a7f1ed7cad984a2e" ON public.rating USING btree (order_id)`
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
| `type` | text | sí | U |  |  | El código busca los roles por este texto: tiene que ser único. |
| `createdAt` | timestamptz | no |  |  | `now()` | _(sin descripción documentada en el código)_ |
| `updatedAt` | timestamptz | no |  |  | `now()` | _(sin descripción documentada en el código)_ |

Índices (además de la clave primaria):
- `UQ_9a0c91c218a16e604951ff1c099`: `CREATE UNIQUE INDEX "UQ_9a0c91c218a16e604951ff1c099" ON public.role USING btree (type)`

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

> **Cobertura de las descripciones.** 65 de 411 columnas tienen descripción tomada del comentario de la entidad de TypeORM que las define; las que no la tienen en el código figuran arriba como «sin descripción documentada en el código» en lugar de inventarse una.

## Relaciones no declaradas

No hay ninguna: las 13 relaciones que en algún momento existieron sin `FOREIGN KEY` se declararon el 25/09/2026 (migración `DeclararRelacionesSinClaveForanea`). Hoy las 93 relaciones del dominio están todas declaradas.

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

## Tipos enumerados

| Tipo | Valores | Estado |
|---|---|---|
| `address_geocode_precision_enum` | `exact`, `approximate`, `unresolved` | implementado |
| `audit_result_enum` | `success`, `failure` | implementado |
| `claims_status_enum` | `pending`, `in_process`, `resolved`, `rejected` | implementado |
| `configurable_process_enum` | `fleet_planner`, `repurchase`, `route_batching`, `cylinder_recovery`, `express_dispatch` | implementado |
| `coverage_zone_surcharge_type_enum` | `fixed`, `percentage` | implementado |
| `cylinder_inspection_result_enum` | `approved`, `conditional`, `rejected` | implementado |
| `cylinder_movement_from_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned` | implementado |
| `cylinder_movement_to_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned` | implementado |
| `cylinder_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned` | implementado |
| `distributor_status_enum` | `active`, `suspended` | implementado |
| `fleet_status_enum` | `active`, `in_service`, `grounded` | implementado |
| `incident_moment_enum` | `pre_delivery`, `in_delivery`, `post_delivery` | implementado |
| `incident_status_enum` | `open`, `resolved` | implementado |
| `incident_type_enum` | `damaged`, `out_of_stock`, `no_show`, `other` | implementado |
| `maintenance_criticality_enum` | `blocking`, `non_blocking` | implementado |
| `maintenance_subject_enum` | `vehicle`, `driver` | implementado |
| `maintenance_task_status_enum` | `forecast`, `scheduled`, `in_progress`, `done`, `overdue`, `cancelled` | implementado |
| `maintenance_trigger_enum` | `by_km`, `by_time`, `by_fixed_date` | implementado |
| `order_delivery_mode_enum` | `standard`, `express` | implementado |
| `order_dispatch_offer_status_enum` | `offered`, `accepted`, `rejected`, `expired` | implementado |
| `order_paymentmethod_enum` | `cash`, `mercadopago`, `transfer` | implementado |
| `order_paymentstatus_enum` | `pending`, `paid`, `failed` | implementado |
| `order_paymenttype_enum` | `cash`, `online` | implementado |
| `order_status_enum` | `reserved`, `pending`, `accepted`, `on_the_way`, `delivered`, `cancelled` | implementado |
| `order_zone_surcharge_type_enum` | `fixed`, `percentage` | implementado |
| `payment_gateway_enum` | `mercadopago`, `cash` | implementado |
| `payment_integration_enum` | `checkout_pro`, `cash` | implementado |
| `payment_status_enum` | `pending`, `approved`, `rejected`, `cancelled`, `refunded` | implementado |
| `proposal_status_enum` | `pending`, `accepted`, `rejected`, `expired` | implementado |
| `rating_from_role_enum` | `customer`, `delivery` | implementado |
| `recovery_case_status_enum` | `open`, `returned`, `escalated`, `deposit_charged`, `written_off`, `closed_no_charge` | implementado |
| `recovery_notice_kind_enum` | `reminder`, `pickup_offer`, `deposit_warning` | implementado |
| `repurchase_invitation_status_enum` | `pending`, `accepted`, `rejected`, `expired` | implementado |
| `route_batch_status_enum` | `forming`, `offered`, `assigned`, `dissolved`, `completed` | implementado |
| `vehicle_type_enum` | `motorcycle`, `car`, `van` | propuesto |
