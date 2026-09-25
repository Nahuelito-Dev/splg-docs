# Modelo de Datos — SPLG

38 tablas y 84 claves foráneas, leídas de la base en ejecución.

Además de lo implementado, este documento registra 0 relaciones que el sistema usa pero que la base no declara, y los agregados que pidió la cátedra.

| Sección | Qué contiene |
|---|---|
| [Diccionario de datos](#diccionario-de-datos) | Las tablas tal cual están hoy en la base |
| [Relaciones no declaradas](#relaciones-no-declaradas) | Columnas que apuntan a otra tabla sin clave foránea |
| [Modelo propuesto](#modelo-propuesto) | Lo que hay que agregar, por pedido de la cátedra |
| [Tipos enumerados](#tipos-enumerados) | Los valores admitidos por cada enumerado |

## Diccionario de datos

### `admin` — Administrador

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `admin_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | no | FK | `distributor.distributor_id` |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `createdAt` | timestamptz | sí |  |  |

### `audit_log` — Asiento de auditoría

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `audit_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | no | FK | `distributor.distributor_id` |
| `actor_user_id` | uuid | no | FK | `user.user_id` |
| `actor_role` | varchar(30) | no |  |  |
| `http_method` | varchar(10) | sí |  |  |
| `resource` | varchar(60) | sí |  |  |
| `resource_id` | varchar(64) | no |  |  |
| `path` | varchar(255) | sí |  |  |
| `client_source` | varchar(30) | no |  |  |
| `ip` | varchar(45) | no |  |  |
| `result` | audit_result_enum | sí |  |  |
| `status_code` | integer | sí |  |  |
| `changes` | jsonb | no |  |  |
| `error_message` | text | no |  |  |
| `created_at` | timestamptz | sí |  |  |

### `car` — Vehículo

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `car_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `type_car` | varchar(50) | no |  |  |
| `car_capacity` | integer | no |  |  |
| `car_patent` | varchar(20) | no |  |  |
| `car_brand` | varchar(50) | no |  |  |
| `car_model` | varchar(50) | no |  |  |
| `car_year` | integer | no |  |  |
| `car_color` | varchar(50) | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |
| `deletedAt` | timestamptz | no |  |  |
| `tare_weight_kg` | numeric(10,2) | no |  |  |
| `max_load_kg` | numeric(10,2) | no |  |  |
| `odometer_km` | integer | no |  |  |
| `fleet_status` | fleet_status_enum | sí |  |  |
| `in_service_since` | timestamptz | no |  |  |

### `cart` — Carrito

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `cart_id` | uuid | sí | PK |  |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `updated_at` | timestamptz | sí |  |  |

Claves únicas compuestas: (`user_id`, `distributor_id`).

### `cart_item` — Ítem del carrito

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `cart_item_id` | uuid | sí | PK |  |
| `cart_id` | uuid | sí | FK | `cart.cart_id` |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |
| `quantity` | integer | sí |  |  |
| `unit_price` | numeric(10,2) | sí |  |  |

Claves únicas compuestas: (`cart_id`, `gas_cylinder_id`).

### `claims` — Reclamo

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `claim_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `customer_id` | uuid | sí | FK | `user.user_id` |
| `reason` | varchar | sí |  |  |
| `description` | text | sí |  |  |
| `photoUrl` | varchar | no |  |  |
| `status` | claims_status_enum | sí |  |  |
| `resolutionNote` | text | no |  |  |
| `createdAt` | timestamp | sí |  |  |

### `coverage_zone` — Zona de cobertura

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `coverage_zone_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `name` | varchar(120) | sí |  |  |
| `area` | geometry | sí |  |  |
| `surcharge` | numeric(10,2) | sí |  |  |
| `isActive` | boolean | sí |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |
| `deletedAt` | timestamptz | no |  |  |
| `surcharge_type` | coverage_zone_surcharge_type_enum | sí |  |  |
| `label` | varchar(40) | no |  |  |
| `color` | varchar(7) | no |  |  |
| `valid_until` | timestamptz | no |  |  |

### `customer` — Cliente

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `customer_id` | uuid | sí | PK |  |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `notification_token` | text | no |  |  |
| `validated` | boolean | sí |  |  |
| `createdAt` | timestamptz | no |  |  |
| `deletedAt` | timestamptz | no |  |  |
| `location` | geometry | no |  |  |
| `avg_monthly_consumption_kg` | numeric(10,2) | no |  |  |
| `declared_cylinder_type_id` | uuid | no | FK | `gas_cylinder.gas_cylinder_id` |
| `repurchase_notice_days` | integer | no |  |  |
| `next_repurchase_estimate_at` | timestamptz | no |  |  |

### `cylinder` — Envase

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `cylinder_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `serial` | varchar | sí |  |  |
| `gas_cylinder_id` | uuid | no | FK | `gas_cylinder.gas_cylinder_id` |
| `state` | cylinder_state_enum | sí |  |  |
| `current_customer_id` | uuid | no | FK | `user.user_id` |
| `current_order_id` | uuid | no | FK | `order.order_id` |
| `deposit` | numeric(10,2) | sí |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |
| `manufactured_at` | timestamptz | no |  |  |
| `last_inspection_at` | timestamptz | no |  |  |
| `expires_at` | timestamptz | no |  |  |

Claves únicas compuestas: (`distributor_id`, `serial`).

### `cylinder_inspection` — Revisión de envase

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `inspection_id` | uuid | sí | PK |  |
| `cylinder_id` | uuid | sí | FK | `cylinder.cylinder_id` |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `inspected_at` | timestamptz | sí |  |  |
| `result` | cylinder_inspection_result_enum | sí |  |  |
| `next_due_at` | timestamptz | no |  |  |
| `notes` | text | no |  |  |

### `cylinder_movement` — Movimiento de envase

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `movement_id` | uuid | sí | PK |  |
| `cylinder_id` | uuid | sí | FK | `cylinder.cylinder_id` |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `from_state` | cylinder_movement_from_state_enum | no |  |  |
| `to_state` | cylinder_movement_to_state_enum | sí |  |  |
| `order_id` | uuid | no | FK | `order.order_id` |
| `actor_user_id` | uuid | no | FK | `user.user_id` |
| `note` | text | no |  |  |
| `createdAt` | timestamptz | sí |  |  |

### `cylinder_recovery_case` — Caso de recupero

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `case_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `cylinder_id` | uuid | sí | FK | `cylinder.cylinder_id` |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `delivered_at` | timestamptz | sí |  |  |
| `deposit_amount` | numeric(10,2) | sí |  |  |
| `step` | integer | sí |  |  |
| `status` | recovery_case_status_enum | sí |  |  |
| `opened_at` | timestamptz | sí |  |  |
| `closed_at` | timestamptz | no |  |  |
| `resolved_by_user_id` | uuid | no | FK | `user.user_id` |
| `resolution_note` | text | no |  |  |

### `cylinder_recovery_notice` — Aviso de recupero

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `notice_id` | uuid | sí | PK |  |
| `case_id` | uuid | sí | FK | `cylinder_recovery_case.case_id` |
| `step` | integer | sí |  |  |
| `kind` | recovery_notice_kind_enum | sí |  |  |
| `status` | proposal_status_enum | no |  |  |
| `sent_at` | timestamptz | sí |  |  |
| `expires_at` | timestamptz | sí |  |  |

### `delivery` — Chofer

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `delivery_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `calification` | double precision | no |  |  |
| `actual_location` | text | no |  |  |
| `cancelledCharge` | real | no |  |  |
| `validated` | boolean | sí |  |  |
| `isActive` | boolean | sí |  |  |
| `notification_token` | text | no |  |  |
| `balance` | double precision | sí |  |  |
| `createdAt` | timestamptz | no |  |  |
| `deletedAt` | timestamptz | no |  |  |
| `location` | geometry | no |  |  |

### `distributor` — Distribuidora

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `distributor_id` | uuid | sí | PK |  |
| `name` | varchar(120) | sí |  |  |
| `slug` | varchar(60) | sí | U |  |
| `legal_name` | varchar(160) | no |  |  |
| `tax_id` | varchar(20) | no |  |  |
| `email` | varchar | no |  |  |
| `phone` | varchar | no |  |  |
| `logo_url` | varchar | no |  |  |
| `status` | distributor_status_enum | sí |  |  |
| `plan` | varchar | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |
| `deletedAt` | timestamptz | no |  |  |

### `gas_cylinder` — Tipo de garrafa

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `gas_cylinder_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `type` | varchar(50) | sí |  |  |
| `weight` | numeric(10,2) | sí |  |  |
| `price` | numeric(10,2) | sí |  |  |
| `stock` | integer | sí |  |  |
| `description` | text | no |  |  |
| `isActive` | boolean | sí |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |

Claves únicas compuestas: (`distributor_id`, `type`).

### `gas_cylinder_promotion` — Promoción

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `promotion_id` | uuid | sí | PK |  |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |
| `quantity` | integer | sí |  |  |
| `discount_percentage` | numeric(5,2) | sí |  |  |

Claves únicas compuestas: (`gas_cylinder_id`, `quantity`).

### `incident` — Incidencia

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `incident_id` | uuid | sí | PK |  |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `reported_by` | uuid | sí | FK | `user.user_id` |
| `type` | incident_type_enum | sí |  |  |
| `description` | text | sí |  |  |
| `photo_url` | varchar | no |  |  |
| `status` | incident_status_enum | sí |  |  |
| `resolution_note` | text | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `resolvedAt` | timestamptz | no |  |  |
| `moment` | incident_moment_enum | no |  |  |

### `maintenance_plan` — Plan de mantenimiento

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `plan_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `name` | varchar(120) | sí |  |  |
| `subject` | maintenance_subject_enum | sí |  |  |
| `trigger` | maintenance_trigger_enum | sí |  |  |
| `interval_km` | integer | no |  |  |
| `interval_months` | integer | no |  |  |
| `lead_time_days` | integer | sí |  |  |
| `criticality` | maintenance_criticality_enum | sí |  |  |
| `car_type` | varchar | no |  |  |
| `is_active` | boolean | sí |  |  |

### `maintenance_task` — Tarea de mantenimiento

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `task_id` | uuid | sí | PK |  |
| `plan_id` | uuid | sí | FK | `maintenance_plan.plan_id` |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `car_id` | uuid | no | FK | `car.car_id` |
| `delivery_id` | uuid | no | FK | `delivery.delivery_id` |
| `status` | maintenance_task_status_enum | sí |  |  |
| `due_at` | timestamptz | no |  |  |
| `due_km` | integer | no |  |  |
| `predicted_due_at` | timestamptz | no |  |  |
| `scheduled_at` | timestamptz | no |  |  |
| `performed_at` | timestamptz | no |  |  |
| `odometer_km` | integer | no |  |  |
| `cost` | numeric(10,2) | no |  |  |
| `provider` | varchar(120) | no |  |  |
| `reference_number` | varchar(60) | no |  |  |
| `category` | varchar(10) | no |  |  |
| `alerted_at` | timestamptz | no |  |  |
| `notes` | text | no |  |  |

### `maintenance_window_proposal` — Propuesta de ventana de taller

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `proposal_id` | uuid | sí | PK |  |
| `task_id` | uuid | sí | FK | `maintenance_task.task_id` |
| `delivery_id` | uuid | sí | FK | `delivery.delivery_id` |
| `window_start` | timestamptz | sí |  |  |
| `window_end` | timestamptz | sí |  |  |
| `rank` | integer | sí |  |  |
| `status` | proposal_status_enum | sí |  |  |
| `expires_at` | timestamptz | sí |  |  |
| `responded_at` | timestamptz | no |  |  |

### `module_config` — Configuración de módulo

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `config_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `module` | configurable_process_enum | sí |  |  |
| `params` | jsonb | sí |  |  |
| `updated_at` | timestamptz | sí |  |  |
| `updated_by_user_id` | uuid | no | FK | `user.user_id` |

Claves únicas compuestas: (`distributor_id`, `module`).

### `order` — Pedido

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `order_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `customer_id` | uuid | sí | FK | `user.user_id` |
| `time_slot_id` | uuid | no | FK | `time_slot.time_slot_id` |
| `scheduled_date` | date | no |  |  |
| `deposit_amount` | numeric(10,2) | sí |  |  |
| `deposit_paid` | boolean | sí |  |  |
| `delivery_id` | uuid | no | FK | `delivery.delivery_id` |
| `address_id` | uuid | sí | FK | `user_address.address_id` |
| `status` | order_status_enum | sí |  |  |
| `paymentMethod` | order_paymentmethod_enum | sí |  |  |
| `paymentType` | order_paymenttype_enum | sí |  |  |
| `paymentStatus` | order_paymentstatus_enum | sí |  |  |
| `totalAmount` | numeric(10,2) | sí |  |  |
| `notes` | text | no |  |  |
| `deliveryInstructions` | text | no |  |  |
| `deliveryLatitude` | varchar(50) | no |  |  |
| `deliveryLongitude` | varchar(50) | no |  |  |
| `acceptedAt` | timestamp | no |  |  |
| `onTheWayAt` | timestamp | no |  |  |
| `deliveredAt` | timestamp | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |
| `cancellationReason` | text | no |  |  |
| `gatewayPaymentId` | varchar(100) | no |  |  |
| `deliveryCode` | varchar(12) | no |  |  |
| `receiver_name` | varchar(120) | no |  |  |
| `receiver_document` | varchar(20) | no |  |  |
| `receiver_relationship` | varchar(40) | no |  |  |
| `delivery_mode` | order_delivery_mode_enum | sí |  |  |

### `order_address_change` — Cambio de dirección

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `change_id` | uuid | sí | PK |  |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `from_address_id` | uuid | sí | FK | `user_address.address_id` |
| `to_address_id` | uuid | sí | FK | `user_address.address_id` |
| `changed_by_user_id` | uuid | sí | FK | `user.user_id` |
| `changed_at` | timestamptz | sí |  |  |
| `reason` | text | no |  |  |

### `order_dispatch_offer` — Oferta de despacho

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `offer_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `driver_id` | uuid | sí | FK | `user.user_id` |
| `status` | order_dispatch_offer_status_enum | sí |  |  |
| `expiresAt` | timestamptz | sí |  |  |
| `offeredAt` | timestamptz | sí |  |  |

### `order_item` — Ítem del pedido

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `order_item_id` | uuid | sí | PK |  |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `gas_cylinder_id` | uuid | sí | FK | `gas_cylinder.gas_cylinder_id` |
| `quantity` | integer | sí |  |  |
| `unitPrice` | numeric(10,2) | sí |  |  |
| `subtotal` | numeric(10,2) | sí |  |  |

### `order_status_history` — Cambio de estado del pedido

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `history_id` | uuid | sí | PK |  |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `from_status` | order_status_enum | no |  |  |
| `to_status` | order_status_enum | sí |  |  |
| `changed_by_user_id` | uuid | no | FK | `user.user_id` |
| `reason` | text | no |  |  |
| `changed_at` | timestamptz | sí |  |  |

### `payment` — Pago

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `payment_id` | uuid | sí | PK |  |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `distributor_id` | uuid | no | FK | `distributor.distributor_id` |
| `gateway` | payment_gateway_enum | sí |  |  |
| `integration` | payment_integration_enum | sí |  |  |
| `method` | varchar(50) | no |  |  |
| `gateway_payment_id` | varchar(100) | no |  |  |
| `external_reference` | varchar | no |  |  |
| `amount` | numeric(10,2) | sí |  |  |
| `currency` | varchar(10) | sí |  |  |
| `status` | payment_status_enum | sí |  |  |
| `payment_url` | text | no |  |  |
| `is_deposit` | boolean | sí |  |  |
| `metadata` | jsonb | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |

### `rating` — Calificación

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `rating_id` | uuid | sí | PK |  |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `from_user_id` | uuid | sí | FK | `user.user_id` |
| `to_user_id` | uuid | sí | FK | `user.user_id` |
| `from_role` | rating_from_role_enum | sí |  |  |
| `stars` | integer | sí |  |  |
| `comment` | text | no |  |  |
| `createdAt` | timestamptz | sí |  |  |

Claves únicas compuestas: (`order_id`, `from_role`).

### `repurchase_invitation` — Invitación de recompra

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `invitation_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `address_id` | uuid | no | FK | `user_address.address_id` |
| `projected_depletion_at` | timestamptz | sí |  |  |
| `suggested_items` | jsonb | sí |  |  |
| `status` | repurchase_invitation_status_enum | sí |  |  |
| `expires_at` | timestamptz | sí |  |  |
| `responded_at` | timestamptz | no |  |  |
| `order_id` | uuid | no | FK | `order.order_id` |
| `created_at` | timestamptz | sí |  |  |

### `role` — Rol

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `role_id` | uuid | sí | PK |  |
| `type` | text | sí | U |  |
| `createdAt` | timestamptz | no |  |  |
| `updatedAt` | timestamptz | no |  |  |

### `route_batch` — Lote de recorrido

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `batch_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `status` | route_batch_status_enum | sí |  |  |
| `total_weight_kg` | numeric(10,2) | sí |  |  |
| `delivery_id` | uuid | no | FK | `delivery.delivery_id` |
| `created_at` | timestamptz | sí |  |  |

### `route_batch_offer` — Oferta de lote

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `offer_id` | uuid | sí | PK |  |
| `batch_id` | uuid | sí | FK | `route_batch.batch_id` |
| `delivery_id` | uuid | sí | FK | `delivery.delivery_id` |
| `status` | proposal_status_enum | sí |  |  |
| `expires_at` | timestamptz | sí |  |  |
| `responded_at` | timestamptz | no |  |  |

### `route_batch_stop` — Parada del lote

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `stop_id` | uuid | sí | PK |  |
| `batch_id` | uuid | sí | FK | `route_batch.batch_id` |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `sequence` | integer | sí |  |  |

Claves únicas compuestas: (`batch_id`, `order_id`).

### `time_slot` — Franja horaria

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `time_slot_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `name` | varchar(50) | sí |  |  |
| `startTime` | time | sí |  |  |
| `endTime` | time | sí |  |  |
| `capacity` | integer | sí |  |  |
| `isActive` | boolean | sí |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |

### `user` — Usuario

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `user_id` | uuid | sí | PK |  |
| `role_id` | uuid | no | FK | `role.role_id` |
| `firebase_uid` | varchar | no | U |  |
| `full_name` | varchar | no |  |  |
| `selfie` | varchar | no |  |  |
| `email` | varchar | no | U |  |
| `phone_number` | varchar | no | U |  |
| `phone_verified` | boolean | sí |  |  |
| `email_verified` | boolean | sí |  |  |
| `blocked` | boolean | sí |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `deletedAt` | timestamptz | no |  |  |

### `user_address` — Dirección de entrega

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `address_id` | uuid | sí | PK |  |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `street` | varchar(255) | sí |  |  |
| `city` | varchar(100) | sí |  |  |
| `postalCode` | varchar(20) | no |  |  |
| `formattedAddress` | text | no |  |  |
| `isDefault` | boolean | sí |  |  |
| `additionalInstructions` | text | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |
| `deletedAt` | timestamptz | no |  |  |
| `floor` | varchar(10) | no |  |  |
| `apartment` | varchar(10) | no |  |  |
| `location` | geometry | no |  |  |
| `place_id` | varchar(255) | no |  |  |
| `geocode_precision` | address_geocode_precision_enum | sí |  |  |

### `vehicle_usage_log` — Registro de uso del vehículo

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `log_id` | uuid | sí | PK |  |
| `car_id` | uuid | sí | FK | `car.car_id` |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `day` | date | sí |  |  |
| `km` | numeric(10,2) | sí |  |  |
| `orders` | integer | sí |  |  |
| `route_hours` | numeric(6,2) | sí |  |  |

Claves únicas compuestas: (`car_id`, `day`).

## Relaciones no declaradas

0 columnas apuntan a otra tabla y el sistema las usa como referencia, pero la base no las declara como `FOREIGN KEY`. La consecuencia práctica es que PostgreSQL no valida que el destino exista ni propaga el borrado: la integridad queda a cargo de la aplicación. En los diagramas se dibujan con línea punteada y la etiqueta «sin FK».

El destino de cada columna se tomó de la entidad de TypeORM que la define. La regla de borrado propuesta sigue el patrón del resto del esquema: `CASCADE` para las columnas obligatorias y para el tenant, `SET NULL` para los punteros opcionales, `RESTRICT` donde el borrado no debería propagarse.

| Tabla | Columna | Apunta a | Obligatoria | Filas huérfanas | Borrado propuesto |
|---|---|---|:-:|:-:|---|

El DDL que las declararía:

```sql
```

> La columna «filas huérfanas» se midió contra los datos que hoy tiene la base: no hay ninguna, así que el DDL se puede aplicar tal cual.

## Modelo propuesto

0 agregados pedidos por la cátedra: 0 tablas nuevas, 0 columnas nuevas sobre tablas existentes y 0 tipos enumerados nuevos. El DDL completo está en `SPLG-base-de-datos-propuesta.sql`.

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
| `payment_gateway_enum` | `mercadopago`, `cash` | implementado |
| `payment_integration_enum` | `checkout_pro`, `cash` | implementado |
| `payment_status_enum` | `pending`, `approved`, `rejected`, `cancelled`, `refunded` | implementado |
| `proposal_status_enum` | `pending`, `accepted`, `rejected`, `expired` | implementado |
| `rating_from_role_enum` | `customer`, `delivery` | implementado |
| `recovery_case_status_enum` | `open`, `returned`, `escalated`, `deposit_charged`, `written_off`, `closed_no_charge` | implementado |
| `recovery_notice_kind_enum` | `reminder`, `pickup_offer`, `deposit_warning` | implementado |
| `repurchase_invitation_status_enum` | `pending`, `accepted`, `rejected`, `expired` | implementado |
| `route_batch_status_enum` | `forming`, `offered`, `assigned`, `dissolved`, `completed` | implementado |
