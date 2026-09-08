# Modelo de Datos — SPLG

20 tablas y 30 claves foráneas, leídas de la base en ejecución.

Además de lo implementado, este documento registra 13 relaciones que el sistema usa pero que la base no declara, y los agregados que pidió la cátedra.

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
| `role_id` | uuid | sí | FK | `role.role_id` |
| `createdAt` | timestamptz | sí |  |  |

### `car` — Vehículo

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `car_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `type_car` | varchar(50) | no |  |  |
| `car_capacity` | integer | no |  |  |
| `car_patent` | varchar(20) | no | U |  |
| `car_brand` | varchar(50) | no |  |  |
| `car_model` | varchar(50) | no |  |  |
| `car_year` | integer | no |  |  |
| `car_color` | varchar(50) | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |

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

### `customer` — Cliente

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `customer_id` | uuid | sí | PK |  |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `notification_token` | text | no |  |  |
| `lat_lang` | text | no |  |  |
| `validated` | text | no |  |  |
| `createdAt` | timestamptz | no |  |  |
| `deletedAt` | timestamptz | no |  |  |

### `cylinder` — Envase

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `cylinder_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `serial` | varchar | sí |  |  |
| `gas_cylinder_id` | uuid | no |  | `gas_cylinder.gas_cylinder_id` (sin FK) |
| `state` | cylinder_state_enum | sí |  |  |
| `current_customer_id` | uuid | no |  | `user.user_id` (sin FK) |
| `current_order_id` | uuid | no |  | `order.order_id` (sin FK) |
| `deposit` | numeric(10,2) | sí |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |

Claves únicas compuestas: (`distributor_id`, `serial`).

### `cylinder_movement` — Movimiento de envase

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `movement_id` | uuid | sí | PK |  |
| `cylinder_id` | uuid | sí |  | `cylinder.cylinder_id` (sin FK) |
| `distributor_id` | uuid | sí |  | `distributor.distributor_id` (sin FK) |
| `from_state` | cylinder_movement_from_state_enum | no |  |  |
| `to_state` | cylinder_movement_to_state_enum | sí |  |  |
| `order_id` | uuid | no |  | `order.order_id` (sin FK) |
| `actor_user_id` | uuid | no |  | `user.user_id` (sin FK) |
| `note` | text | no |  |  |
| `createdAt` | timestamptz | sí |  |  |

### `delivery` — Chofer

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `delivery_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `user_id` | uuid | sí | FK | `user.user_id` |
| `calification` | double precision | no |  |  |
| `latLng` | text | no |  |  |
| `actual_location` | text | no |  |  |
| `cancelledCharge` | real | no |  |  |
| `validated` | boolean | sí |  |  |
| `isActive` | boolean | sí |  |  |
| `notification_token` | text | no |  |  |
| `isTraveling` | text | no |  |  |
| `balance` | double precision | sí |  |  |
| `createdAt` | timestamptz | no |  |  |
| `deletedAt` | timestamptz | no |  |  |

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
| `promotions` | jsonb | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |

### `incident` — Incidencia

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `incident_id` | uuid | sí | PK |  |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `distributor_id` | uuid | sí | FK | `distributor.distributor_id` |
| `reported_by` | uuid | sí |  | `user.user_id` (sin FK) |
| `type` | incident_type_enum | sí |  |  |
| `description` | text | sí |  |  |
| `photo_url` | varchar | no |  |  |
| `status` | incident_status_enum | sí |  |  |
| `resolution_note` | text | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `resolvedAt` | timestamptz | no |  |  |

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

### `order_dispatch_offer` — Oferta de despacho

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `offer_id` | uuid | sí | PK |  |
| `distributor_id` | uuid | sí |  | `distributor.distributor_id` (sin FK) |
| `order_id` | uuid | sí | FK | `order.order_id` |
| `driver_id` | uuid | sí |  | `user.user_id` (sin FK) |
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

### `payment` — Pago

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `payment_id` | uuid | sí | PK |  |
| `order_id` | uuid | sí |  | `order.order_id` (sin FK) |
| `distributor_id` | uuid | no |  | `distributor.distributor_id` (sin FK) |
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
| `to_user_id` | uuid | sí |  | `user.user_id` (sin FK) |
| `from_role` | rating_from_role_enum | sí |  |  |
| `stars` | integer | sí |  |  |
| `comment` | text | no |  |  |
| `createdAt` | timestamptz | sí |  |  |

Claves únicas compuestas: (`order_id`, `from_role`).

### `role` — Rol

| Columna | Tipo | Obligatoria | Clave | Referencia |
|---|---|:-:|:-:|---|
| `role_id` | uuid | sí | PK |  |
| `type` | text | sí |  |  |
| `createdAt` | timestamptz | no |  |  |
| `updatedAt` | timestamptz | no |  |  |

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
| `firebase_uid` | varchar | no |  |  |
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
| `latitude` | varchar(50) | no |  |  |
| `longitude` | varchar(50) | no |  |  |
| `formattedAddress` | text | no |  |  |
| `isDefault` | boolean | sí |  |  |
| `additionalInstructions` | text | no |  |  |
| `createdAt` | timestamptz | sí |  |  |
| `updatedAt` | timestamptz | sí |  |  |

## Relaciones no declaradas

13 columnas apuntan a otra tabla y el sistema las usa como referencia, pero la base no las declara como `FOREIGN KEY`. La consecuencia práctica es que PostgreSQL no valida que el destino exista ni propaga el borrado: la integridad queda a cargo de la aplicación. En los diagramas se dibujan con línea punteada y la etiqueta «sin FK».

El destino de cada columna se tomó de la entidad de TypeORM que la define. La regla de borrado propuesta sigue el patrón del resto del esquema: `CASCADE` para las columnas obligatorias y para el tenant, `SET NULL` para los punteros opcionales, `RESTRICT` donde el borrado no debería propagarse.

| Tabla | Columna | Apunta a | Obligatoria | Filas huérfanas | Borrado propuesto |
|---|---|---|:-:|:-:|---|
| `payment` | `order_id` | `order.order_id` | sí | 0 | `ON DELETE CASCADE` |
| `payment` | `distributor_id` | `distributor.distributor_id` | no | 0 | `ON DELETE CASCADE` |
| `cylinder_movement` | `cylinder_id` | `cylinder.cylinder_id` | sí | 0 | `ON DELETE CASCADE` |
| `cylinder_movement` | `distributor_id` | `distributor.distributor_id` | sí | 0 | `ON DELETE CASCADE` |
| `cylinder_movement` | `order_id` | `order.order_id` | no | 0 | `ON DELETE SET NULL` |
| `cylinder_movement` | `actor_user_id` | `user.user_id` | no | 0 | `ON DELETE SET NULL` |
| `cylinder` | `gas_cylinder_id` | `gas_cylinder.gas_cylinder_id` | no | 0 | `ON DELETE SET NULL` |
| `cylinder` | `current_customer_id` | `user.user_id` | no | 0 | `ON DELETE SET NULL` |
| `cylinder` | `current_order_id` | `order.order_id` | no | 0 | `ON DELETE SET NULL` |
| `order_dispatch_offer` | `distributor_id` | `distributor.distributor_id` | sí | 0 | `ON DELETE CASCADE` |
| `order_dispatch_offer` | `driver_id` | `user.user_id` | sí | 0 | `ON DELETE CASCADE` |
| `incident` | `reported_by` | `user.user_id` | sí | 0 | `ON DELETE CASCADE` |
| `rating` | `to_user_id` | `user.user_id` | sí | 0 | `ON DELETE CASCADE` |

El DDL que las declararía:

```sql
ALTER TABLE "payment" ADD CONSTRAINT "FK_payment_order_id"
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE;
ALTER TABLE "payment" ADD CONSTRAINT "FK_payment_distributor_id"
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_cylinder_id"
  FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_distributor_id"
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_order_id"
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_actor_user_id"
  FOREIGN KEY ("actor_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "cylinder" ADD CONSTRAINT "FK_cylinder_gas_cylinder_id"
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE SET NULL;
ALTER TABLE "cylinder" ADD CONSTRAINT "FK_cylinder_current_customer_id"
  FOREIGN KEY ("current_customer_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "cylinder" ADD CONSTRAINT "FK_cylinder_current_order_id"
  FOREIGN KEY ("current_order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;
ALTER TABLE "order_dispatch_offer" ADD CONSTRAINT "FK_order_dispatch_offer_distributor_id"
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "order_dispatch_offer" ADD CONSTRAINT "FK_order_dispatch_offer_driver_id"
  FOREIGN KEY ("driver_id") REFERENCES "user" ("user_id") ON DELETE CASCADE;
ALTER TABLE "incident" ADD CONSTRAINT "FK_incident_reported_by"
  FOREIGN KEY ("reported_by") REFERENCES "user" ("user_id") ON DELETE CASCADE;
ALTER TABLE "rating" ADD CONSTRAINT "FK_rating_to_user_id"
  FOREIGN KEY ("to_user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE;
```

> La columna «filas huérfanas» se midió contra los datos que hoy tiene la base: no hay ninguna, así que el DDL se puede aplicar tal cual.

## Modelo propuesto

8 agregados pedidos por la cátedra: 5 tablas nuevas, 22 columnas nuevas sobre tablas existentes y 5 tipos enumerados nuevos. El DDL completo está en `SPLG-base-de-datos-propuesta.sql`.

### 1. Vencimiento de garrafas

**Pedido de la cátedra:** Registrar el vencimiento del envase y las revisiones periódicas que lo renuevan, para no despachar garrafas fuera de norma.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `cylinder` | `manufactured_at` | timestamptz | no | Fecha de fabricación grabada en el envase. |
| `cylinder` | `last_inspection_at` | timestamptz | no | Fecha de la última revisión aprobada. |
| `cylinder` | `expires_at` | timestamptz | no | Fecha hasta la cual el envase puede despacharse. |
| `cylinder_inspection` **(tabla nueva)** | `inspection_id` | uuid | sí | Identificador. |
| `cylinder_inspection` **(tabla nueva)** | `cylinder_id` | uuid | sí | Envase revisado. |
| `cylinder_inspection` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `cylinder_inspection` **(tabla nueva)** | `inspected_at` | timestamptz | sí | Cuándo se hizo la revisión. |
| `cylinder_inspection` **(tabla nueva)** | `result` | cylinder_inspection_result_enum | sí | Apta, apta con salvedades o rechazada. |
| `cylinder_inspection` **(tabla nueva)** | `next_due_at` | timestamptz | no | Vencimiento de esta revisión. |
| `cylinder_inspection` **(tabla nueva)** | `notes` | text | no | Detalle del técnico. |

`cylinder_inspection` — Una fila por revisión técnica del envase. Clave primaria `inspection_id`. Referencias: `cylinder_id` → `cylinder`, `distributor_id` → `distributor`.

Tipo enumerado `cylinder_inspection_result_enum`: `approved`, `conditional`, `rejected`.

> **Decisión de modelado.** `cylinder.expires_at` y `cylinder.last_inspection_at` se derivan de la última fila de `cylinder_inspection`. Se guardan desnormalizadas a propósito: el despacho consulta el vencimiento en cada asignación y no conviene recalcularlo por subconsulta.

### 2. Consumo promedio y aviso de recompra

**Pedido de la cátedra:** Que el cliente declare al registrarse cuánto consume por mes, para estimar cuándo se le acaba la garrafa y avisarle antes.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `customer` | `avg_monthly_consumption_kg` | numeric(10,2) | no | Kilos de gas por mes que declara el cliente. |
| `customer` | `declared_cylinder_type_id` | uuid | no | Tipo de garrafa que usa habitualmente. |
| `customer` | `repurchase_notice_days` | integer | no | Con cuántos días de anticipación quiere el aviso. |
| `customer` | `next_repurchase_estimate_at` | timestamptz | no | Fecha estimada de la próxima compra. |


> **Decisión de modelado.** Las columnas van en `customer`, pero conviene saber que el resto del sistema identifica al cliente por `user.user_id` (`order.customer_id` apunta a `user`, no a `customer`). `customer` hoy es una tabla satélite uno a uno con `user`.

### 3. Datos de carga del vehículo

**Pedido de la cátedra:** Sumar al vehículo la tara y la carga máxima, para saber cuántas garrafas puede llevar sin pasarse del peso permitido.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `car` | `tare_weight_kg` | numeric(10,2) | no | Peso del vehículo vacío, en kilos. |
| `car` | `max_load_kg` | numeric(10,2) | no | Carga máxima admitida, en kilos. |


### 4. Mantenimiento y habilitaciones de la flota

**Pedido de la cátedra:** Llevar seguro y VTV del vehículo, licencia del chofer y el historial de mantenimientos, para no despachar unidades vencidas.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `car` | `insurance_company` | varchar(120) | no | Compañía que asegura la unidad. |
| `car` | `insurance_policy` | varchar(60) | no | Número de póliza. |
| `car` | `insurance_expires_at` | timestamptz | no | Vencimiento de la póliza. |
| `car` | `vtv_expires_at` | timestamptz | no | Vencimiento de la verificación técnica. |
| `delivery` | `license_number` | varchar(30) | no | Número de licencia de conducir. |
| `delivery` | `license_category` | varchar(10) | no | Categoría habilitante. |
| `delivery` | `license_expires_at` | timestamptz | no | Vencimiento de la licencia. |
| `fleet_maintenance` **(tabla nueva)** | `maintenance_id` | uuid | sí | Identificador. |
| `fleet_maintenance` **(tabla nueva)** | `car_id` | uuid | sí | Unidad intervenida. |
| `fleet_maintenance` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `fleet_maintenance` **(tabla nueva)** | `type` | fleet_maintenance_type_enum | sí | Preventivo, correctivo o revisión. |
| `fleet_maintenance` **(tabla nueva)** | `scheduled_at` | timestamptz | sí | Fecha para la que se agendó. |
| `fleet_maintenance` **(tabla nueva)** | `performed_at` | timestamptz | no | Fecha en la que efectivamente se hizo. |
| `fleet_maintenance` **(tabla nueva)** | `odometer_km` | integer | no | Odómetro al momento del trabajo. |
| `fleet_maintenance` **(tabla nueva)** | `cost` | numeric(10,2) | no | Importe del trabajo. |
| `fleet_maintenance` **(tabla nueva)** | `notes` | text | no | Detalle del taller. |
| `fleet_maintenance` **(tabla nueva)** | `status` | fleet_maintenance_status_enum | sí | Estado del trabajo. |

`fleet_maintenance` — Una fila por service, reparación o revisión de una unidad. Clave primaria `maintenance_id`. Referencias: `car_id` → `car`, `distributor_id` → `distributor`.

Tipo enumerado `fleet_maintenance_type_enum`: `preventive`, `corrective`, `inspection`.
Tipo enumerado `fleet_maintenance_status_enum`: `scheduled`, `in_progress`, `done`, `cancelled`.

### 5. Carrito de compra

**Pedido de la cátedra:** Que el cliente arme el pedido de a varios productos y lo deje guardado antes de confirmarlo.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `cart` **(tabla nueva)** | `cart_id` | uuid | sí | Identificador. |
| `cart` **(tabla nueva)** | `user_id` | uuid | sí | Cliente dueño del carrito. |
| `cart` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora a la que le compra. |
| `cart` **(tabla nueva)** | `updatedAt` | timestamptz | sí | Cuándo se tocó por última vez. |
| `cart_item` **(tabla nueva)** | `cart_item_id` | uuid | sí | Identificador. |
| `cart_item` **(tabla nueva)** | `cart_id` | uuid | sí | Carrito al que pertenece. |
| `cart_item` **(tabla nueva)** | `gas_cylinder_id` | uuid | sí | Tipo de garrafa elegido. |
| `cart_item` **(tabla nueva)** | `quantity` | integer | sí | Unidades cargadas. |
| `cart_item` **(tabla nueva)** | `unit_price` | numeric(10,2) | sí | Precio vigente al agregarlo. |

`cart` — Un carrito abierto por cliente y distribuidora. Clave primaria `cart_id`. Referencias: `user_id` → `user`, `distributor_id` → `distributor`. Única: (`user_id`, `distributor_id`).
`cart_item` — Cada producto cargado en el carrito, con su cantidad. Clave primaria `cart_item_id`. Referencias: `cart_id` → `cart`, `gas_cylinder_id` → `gas_cylinder`. Única: (`cart_id`, `gas_cylinder_id`).

> **Decisión de modelado.** El carrito es uno solo por cliente y distribuidora (clave única sobre `user_id` + `distributor_id`): al confirmarse se vuelca a `order` y `order_item`, que siguen siendo el registro definitivo. `unit_price` guarda el precio del momento en que se agregó el producto, que puede diferir del precio vigente al confirmar.

### 6. Cambio de dirección y quién recibe

**Pedido de la cátedra:** Poder cambiar la dirección de entrega de un pedido ya hecho y registrar quién lo recibe si no es el cliente.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `order` | `receiver_name` | varchar(120) | no | Nombre de quien recibe si no es el cliente. |
| `order` | `receiver_document` | varchar(20) | no | Documento de quien recibe. |
| `order` | `receiver_relationship` | varchar(40) | no | Vínculo con el cliente (familiar, encargado, vecino). |
| `order_address_change` **(tabla nueva)** | `change_id` | uuid | sí | Identificador. |
| `order_address_change` **(tabla nueva)** | `order_id` | uuid | sí | Pedido afectado. |
| `order_address_change` **(tabla nueva)** | `from_address_id` | uuid | sí | Dirección anterior. |
| `order_address_change` **(tabla nueva)** | `to_address_id` | uuid | sí | Dirección nueva. |
| `order_address_change` **(tabla nueva)** | `changed_by_user_id` | uuid | sí | Quién hizo el cambio. |
| `order_address_change` **(tabla nueva)** | `changed_at` | timestamptz | sí | Cuándo se cambió. |
| `order_address_change` **(tabla nueva)** | `reason` | text | no | Motivo declarado del cambio. |

`order_address_change` — Historial de cambios de dirección de entrega sobre un pedido. Clave primaria `change_id`. Referencias: `order_id` → `order`, `from_address_id` → `user_address`, `to_address_id` → `user_address`, `changed_by_user_id` → `user`.

### 7. Momento de la incidencia

**Pedido de la cátedra:** Distinguir si la incidencia ocurrió antes, durante o después de la entrega, para saber a quién corresponde resolverla.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `incident` | `moment` | incident_moment_enum | no | Antes, durante o después de la entrega. |


Tipo enumerado `incident_moment_enum`: `pre_delivery`, `in_delivery`, `post_delivery`.

### 8. Compra directa express en moto

**Pedido de la cátedra:** Ofrecer una modalidad de entrega inmediata en moto, separada del reparto programado.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `order` | `delivery_mode` | order_delivery_mode_enum | sí | Reparto programado o express en moto. |
| `order` | `is_express` | boolean | sí | Atajo booleano para filtrar los express. |


Tipo enumerado `order_delivery_mode_enum`: `standard`, `express_moto`.

> **Decisión de modelado.** `is_express` repite lo que ya dice `delivery_mode`. Se deja porque el pedido la nombra por separado y simplifica los filtros, pero es una redundancia consciente: con `delivery_mode` sola alcanza.

## Tipos enumerados

| Tipo | Valores | Estado |
|---|---|---|
| `claims_status_enum` | `pending`, `in_process`, `resolved`, `rejected` | implementado |
| `cylinder_movement_from_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned` | implementado |
| `cylinder_movement_to_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned` | implementado |
| `cylinder_state_enum` | `in_depot`, `filled`, `dispatched`, `with_customer`, `empty_returned` | implementado |
| `distributor_status_enum` | `active`, `suspended` | implementado |
| `incident_status_enum` | `open`, `resolved` | implementado |
| `incident_type_enum` | `damaged`, `out_of_stock`, `no_show`, `other` | implementado |
| `order_dispatch_offer_status_enum` | `offered`, `accepted`, `rejected`, `expired` | implementado |
| `order_paymentmethod_enum` | `cash`, `mercadopago`, `transfer` | implementado |
| `order_paymentstatus_enum` | `pending`, `paid`, `failed` | implementado |
| `order_paymenttype_enum` | `cash`, `online` | implementado |
| `order_status_enum` | `reserved`, `pending`, `accepted`, `on_the_way`, `delivered`, `cancelled` | implementado |
| `payment_gateway_enum` | `mercadopago`, `cash` | implementado |
| `payment_integration_enum` | `checkout_pro`, `cash` | implementado |
| `payment_status_enum` | `pending`, `approved`, `rejected`, `cancelled`, `refunded` | implementado |
| `rating_from_role_enum` | `customer`, `delivery` | implementado |
| `cylinder_inspection_result_enum` | `approved`, `conditional`, `rejected` | propuesto |
| `fleet_maintenance_status_enum` | `scheduled`, `in_progress`, `done`, `cancelled` | propuesto |
| `fleet_maintenance_type_enum` | `preventive`, `corrective`, `inspection` | propuesto |
| `incident_moment_enum` | `pre_delivery`, `in_delivery`, `post_delivery` | propuesto |
| `order_delivery_mode_enum` | `standard`, `express_moto` | propuesto |
