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
| `payment` | `order_id` | `order.order_id` | sí | 0 | `ON DELETE RESTRICT` |
| `payment` | `distributor_id` | `distributor.distributor_id` | no | 0 | `ON DELETE CASCADE` |
| `cylinder_movement` | `cylinder_id` | `cylinder.cylinder_id` | sí | 0 | `ON DELETE RESTRICT` |
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
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE RESTRICT;
ALTER TABLE "payment" ADD CONSTRAINT "FK_payment_distributor_id"
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_cylinder_id"
  FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id") ON DELETE RESTRICT;
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

14 agregados pedidos por la cátedra: 17 tablas nuevas, 26 columnas nuevas sobre tablas existentes y 17 tipos enumerados nuevos. El DDL completo está en `SPLG-base-de-datos-propuesta.sql`.

### 1. Vigencia de envases

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

### 2. Consumo declarado y recompra

**Pedido de la cátedra:** Que el cliente declare cuánto consume por mes, estimar cuándo se le acaba el gas y ofrecerle la reposición antes, con el pedido armado.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `customer` | `avg_monthly_consumption_kg` | numeric(10,2) | no | Kilos de gas por mes que declara el cliente. |
| `customer` | `declared_cylinder_type_id` | uuid | no | Tipo de garrafa que usa habitualmente. |
| `customer` | `repurchase_notice_days` | integer | no | Con cuántos días de anticipación quiere el aviso. |
| `customer` | `next_repurchase_estimate_at` | timestamptz | no | Fecha estimada de la próxima compra. |
| `repurchase_invitation` **(tabla nueva)** | `invitation_id` | uuid | sí | Identificador. |
| `repurchase_invitation` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `repurchase_invitation` **(tabla nueva)** | `user_id` | uuid | sí | Cliente invitado. |
| `repurchase_invitation` **(tabla nueva)** | `address_id` | uuid | no | Dirección sugerida para la entrega. |
| `repurchase_invitation` **(tabla nueva)** | `projected_depletion_at` | timestamptz | sí | Cuándo se estima que se le acaba el gas. |
| `repurchase_invitation` **(tabla nueva)** | `suggested_items` | jsonb | sí | Productos y cantidades que sugiere el historial. |
| `repurchase_invitation` **(tabla nueva)** | `status` | repurchase_invitation_status_enum | sí | Pendiente, aceptada, rechazada o caducada. |
| `repurchase_invitation` **(tabla nueva)** | `expires_at` | timestamptz | sí | Fin de la vigencia de la invitación. |
| `repurchase_invitation` **(tabla nueva)** | `responded_at` | timestamptz | no | Cuándo respondió el cliente. |
| `repurchase_invitation` **(tabla nueva)** | `order_id` | uuid | no | Pedido creado al aceptar. |
| `repurchase_invitation` **(tabla nueva)** | `created_at` | timestamptz | sí | Cuándo se emitió. |

`repurchase_invitation` — Una oferta de reposición al cliente, con el pedido sugerido y una vigencia. Clave primaria `invitation_id`. Referencias: `distributor_id` → `distributor`, `user_id` → `user`, `address_id` → `user_address`, `order_id` → `order`.

Tipo enumerado `repurchase_invitation_status_enum`: `pending`, `accepted`, `rejected`, `expired`.

> **Decisión de modelado.** Las columnas van en `customer`, pero el resto del sistema identifica al cliente por `user.user_id` (`order.customer_id` apunta a `user`). Por eso la invitación apunta a `user`. La invitación guarda el pedido sugerido como JSON porque todavía no es un pedido: recién al aceptarla se crean `order` y `order_item`.

### 3. Flota: habilitaciones, mantenimiento y uso

**Pedido de la cátedra:** Llevar seguro, verificación técnica, licencia y mantenimientos, y planificar el taller antes de que algo venza.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `car` | `tare_weight_kg` | numeric(10,2) | no | Peso del vehículo vacío, en kilos. |
| `car` | `max_load_kg` | numeric(10,2) | no | Carga máxima admitida, en kilos. |
| `car` | `odometer_km` | integer | no | Última lectura conocida del odómetro. |
| `car` | `fleet_status` | fleet_status_enum | sí | Activo, en taller o inhabilitado. Un vehículo inhabilitado no recibe ofertas. |
| `car` | `in_service_since` | timestamptz | no | Desde cuándo está en taller o inhabilitado. |
| `maintenance_plan` **(tabla nueva)** | `plan_id` | uuid | sí | Identificador. |
| `maintenance_plan` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `maintenance_plan` **(tabla nueva)** | `name` | varchar(120) | sí | Seguro, VTV, cambio de aceite, licencia... |
| `maintenance_plan` **(tabla nueva)** | `subject` | maintenance_subject_enum | sí | Vehículo o chofer. |
| `maintenance_plan` **(tabla nueva)** | `trigger` | maintenance_trigger_enum | sí | Por kilómetros, por tiempo o por fecha fija. |
| `maintenance_plan` **(tabla nueva)** | `interval_km` | integer | no | Intervalo, si el disparo es por kilómetros. |
| `maintenance_plan` **(tabla nueva)** | `interval_months` | integer | no | Intervalo, si el disparo es por tiempo. |
| `maintenance_plan` **(tabla nueva)** | `lead_time_days` | integer | sí | Con cuántos días de anticipación se planifica. |
| `maintenance_plan` **(tabla nueva)** | `criticality` | maintenance_criticality_enum | sí | Si al vencer inhabilita o no. |
| `maintenance_plan` **(tabla nueva)** | `car_type` | varchar | no | Tipo de vehículo al que aplica; vacío, a todos. |
| `maintenance_plan` **(tabla nueva)** | `is_active` | boolean | sí | Si el plan está vigente. |
| `maintenance_task` **(tabla nueva)** | `task_id` | uuid | sí | Identificador. |
| `maintenance_task` **(tabla nueva)** | `plan_id` | uuid | sí | Plan del que sale. |
| `maintenance_task` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `maintenance_task` **(tabla nueva)** | `car_id` | uuid | no | Vehículo, si el plan es de vehículo. |
| `maintenance_task` **(tabla nueva)** | `delivery_id` | uuid | no | Chofer, si el plan es de chofer. |
| `maintenance_task` **(tabla nueva)** | `status` | maintenance_task_status_enum | sí | Proyectada, programada, en curso, hecha, vencida o cancelada. |
| `maintenance_task` **(tabla nueva)** | `due_at` | timestamptz | no | Fecha de vencimiento, si es de fecha fija. |
| `maintenance_task` **(tabla nueva)** | `due_km` | integer | no | Kilometraje al que vence, si es por kilómetros. |
| `maintenance_task` **(tabla nueva)** | `predicted_due_at` | timestamptz | no | Fecha estimada por el planificador. |
| `maintenance_task` **(tabla nueva)** | `scheduled_at` | timestamptz | no | Ventana de taller acordada. |
| `maintenance_task` **(tabla nueva)** | `performed_at` | timestamptz | no | Cuándo se hizo. |
| `maintenance_task` **(tabla nueva)** | `odometer_km` | integer | no | Odómetro al hacerla. |
| `maintenance_task` **(tabla nueva)** | `cost` | numeric(10,2) | no | Importe del trabajo. |
| `maintenance_task` **(tabla nueva)** | `provider` | varchar(120) | no | Aseguradora, taller o ente emisor. |
| `maintenance_task` **(tabla nueva)** | `reference_number` | varchar(60) | no | Póliza, número de licencia u oblea. |
| `maintenance_task` **(tabla nueva)** | `category` | varchar(10) | no | Categoría habilitante, para la licencia. |
| `maintenance_task` **(tabla nueva)** | `alerted_at` | timestamptz | no | Cuándo se avisó que vence (CU-142); vacío, sin aviso. |
| `maintenance_task` **(tabla nueva)** | `notes` | text | no | Detalle. |
| `maintenance_window_proposal` **(tabla nueva)** | `proposal_id` | uuid | sí | Identificador. |
| `maintenance_window_proposal` **(tabla nueva)** | `task_id` | uuid | sí | Tarea a programar. |
| `maintenance_window_proposal` **(tabla nueva)** | `delivery_id` | uuid | sí | Chofer que decide. |
| `maintenance_window_proposal` **(tabla nueva)** | `window_start` | timestamptz | sí | Comienzo de la ventana. |
| `maintenance_window_proposal` **(tabla nueva)** | `window_end` | timestamptz | sí | Fin de la ventana. |
| `maintenance_window_proposal` **(tabla nueva)** | `rank` | integer | sí | Orden en que se ofrece. |
| `maintenance_window_proposal` **(tabla nueva)** | `status` | proposal_status_enum | sí | Pendiente, aceptada, rechazada o vencida. |
| `maintenance_window_proposal` **(tabla nueva)** | `expires_at` | timestamptz | sí | Fin de la vigencia. |
| `maintenance_window_proposal` **(tabla nueva)** | `responded_at` | timestamptz | no | Cuándo respondió. |
| `vehicle_usage_log` **(tabla nueva)** | `log_id` | uuid | sí | Identificador. |
| `vehicle_usage_log` **(tabla nueva)** | `car_id` | uuid | sí | Vehículo. |
| `vehicle_usage_log` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `vehicle_usage_log` **(tabla nueva)** | `day` | date | sí | Día registrado. |
| `vehicle_usage_log` **(tabla nueva)** | `km` | numeric(10,2) | sí | Kilómetros recorridos ese día. |
| `vehicle_usage_log` **(tabla nueva)** | `orders` | integer | sí | Pedidos entregados ese día. |
| `vehicle_usage_log` **(tabla nueva)** | `route_hours` | numeric(6,2) | sí | Horas en ruta. |

`maintenance_plan` — La regla: qué se controla, cada cuánto, con qué anticipación y si inhabilita. Clave primaria `plan_id`. Referencias: `distributor_id` → `distributor`.
`maintenance_task` — Cada vencimiento concreto de un plan: una póliza, una VTV, un service. Clave primaria `task_id`. Referencias: `plan_id` → `maintenance_plan`, `distributor_id` → `distributor`, `car_id` → `car`, `delivery_id` → `delivery`.
`maintenance_window_proposal` — Una ventana ofrecida al chofer, de a una por vez, con vigencia. Clave primaria `proposal_id`. Referencias: `task_id` → `maintenance_task`, `delivery_id` → `delivery`.
`vehicle_usage_log` — Kilómetros, pedidos y horas en ruta por vehículo y día. Sólo se agrega. Clave primaria `log_id`. Referencias: `car_id` → `car`, `distributor_id` → `distributor`. Única: (`car_id`, `day`).

Tipo enumerado `fleet_status_enum`: `active`, `in_service`, `grounded`.
Tipo enumerado `maintenance_subject_enum`: `vehicle`, `driver`.
Tipo enumerado `maintenance_trigger_enum`: `by_km`, `by_time`, `by_fixed_date`.
Tipo enumerado `maintenance_criticality_enum`: `blocking`, `non_blocking`.
Tipo enumerado `maintenance_task_status_enum`: `forecast`, `scheduled`, `in_progress`, `done`, `overdue`, `cancelled`.
Tipo enumerado `proposal_status_enum`: `pending`, `accepted`, `rejected`, `expired`.

> **Decisión de modelado.** Seguro, verificación técnica, licencia y mantenimientos son la misma abstracción: un **plan** (la regla: cada cuánto, con qué anticipación, si inhabilita) y sus **tareas** (cada vencimiento concreto). El seguro es un plan de fecha fija que bloquea; el cambio de aceite, uno por kilómetros que no bloquea. La licencia es de la persona y no del vehículo: por eso la tarea apunta a un vehículo **o** a un chofer. Reemplaza la propuesta anterior de columnas sueltas en `car` y `delivery` más una tabla `fleet_maintenance`, que no podía expresar la regla ni alimentar al planificador de M1.

### 4. Carrito de compra

**Pedido de la cátedra:** Que el cliente arme el pedido de a varios productos y lo deje guardado antes de confirmarlo.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `cart` **(tabla nueva)** | `cart_id` | uuid | sí | Identificador. |
| `cart` **(tabla nueva)** | `user_id` | uuid | sí | Cliente dueño del carrito. |
| `cart` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora a la que le compra. |
| `cart` **(tabla nueva)** | `updated_at` | timestamptz | sí | Cuándo se tocó por última vez. |
| `cart_item` **(tabla nueva)** | `cart_item_id` | uuid | sí | Identificador. |
| `cart_item` **(tabla nueva)** | `cart_id` | uuid | sí | Carrito al que pertenece. |
| `cart_item` **(tabla nueva)** | `gas_cylinder_id` | uuid | sí | Tipo de garrafa elegido. |
| `cart_item` **(tabla nueva)** | `quantity` | integer | sí | Unidades cargadas. |
| `cart_item` **(tabla nueva)** | `unit_price` | numeric(10,2) | sí | Precio vigente al agregarlo. |

`cart` — Un carrito abierto por cliente y distribuidora. Clave primaria `cart_id`. Referencias: `user_id` → `user`, `distributor_id` → `distributor`. Única: (`user_id`, `distributor_id`).
`cart_item` — Cada producto cargado en el carrito, con su cantidad. Clave primaria `cart_item_id`. Referencias: `cart_id` → `cart`, `gas_cylinder_id` → `gas_cylinder`. Única: (`cart_id`, `gas_cylinder_id`).

> **Decisión de modelado.** El carrito es uno solo por cliente y distribuidora: al confirmarse se vuelca a `order` y `order_item`, que siguen siendo el registro definitivo. `unit_price` guarda el precio del momento en que se agregó el producto, que puede diferir del precio vigente al confirmar.

### 5. Cambio de dirección y quién recibe

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

### 6. Historial de estados del pedido

**Pedido de la cátedra:** Dejar registro de cada cambio de estado de un pedido: de cuál a cuál, quién lo hizo, cuándo y por qué.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `order_status_history` **(tabla nueva)** | `history_id` | uuid | sí | Identificador. |
| `order_status_history` **(tabla nueva)** | `order_id` | uuid | sí | Pedido. |
| `order_status_history` **(tabla nueva)** | `from_status` | order_status_enum | no | Estado anterior; vacío en el alta. |
| `order_status_history` **(tabla nueva)** | `to_status` | order_status_enum | sí | Estado nuevo. |
| `order_status_history` **(tabla nueva)** | `changed_by_user_id` | uuid | no | Quién lo cambió; vacío si fue un proceso automático. |
| `order_status_history` **(tabla nueva)** | `reason` | text | no | Motivo, cuando la transición lo pide. |
| `order_status_history` **(tabla nueva)** | `changed_at` | timestamptz | sí | Cuándo. |

`order_status_history` — Una fila por transición de estado de un pedido. Clave primaria `history_id`. Referencias: `order_id` → `order`, `changed_by_user_id` → `user`.

> **Decisión de modelado.** Hoy el pedido guarda sólo su estado actual y algunas marcas de tiempo sueltas (`acceptedAt`, `onTheWayAt`, `deliveredAt`): no queda quién hizo cada cambio ni por qué. Las marcas de tiempo se conservan porque los listados las leen sin unir tablas.

### 7. Momento de la incidencia

**Pedido de la cátedra:** Distinguir si la incidencia ocurrió antes, durante o después de la entrega, para saber a quién corresponde resolverla.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `incident` | `moment` | incident_moment_enum | no | Antes, durante o después de la entrega. |


Tipo enumerado `incident_moment_enum`: `pre_delivery`, `in_delivery`, `post_delivery`.

### 8. Entrega express

**Pedido de la cátedra:** Ofrecer una modalidad de entrega inmediata en moto, separada del reparto programado.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `order` | `delivery_mode` | order_delivery_mode_enum | sí | Reparto programado o express. |


Tipo enumerado `order_delivery_mode_enum`: `standard`, `express`.

> **Decisión de modelado.** La propuesta anterior sumaba además `is_express`, que repetía lo que ya dice `delivery_mode`. Se saca: con una sola columna no hay forma de que las dos digan cosas distintas.

### 9. Recargo porcentual y vigencia de zonas

**Pedido de la cátedra:** Que el recargo de una zona pueda ser un porcentaje, que la zona tenga etiqueta y color, y que se pueda programar hasta cuándo rige.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `coverage_zone` | `surcharge_type` | coverage_zone_surcharge_type_enum | sí | Monto fijo o porcentaje del pedido. |
| `coverage_zone` | `label` | varchar(40) | no | Etiqueta corta para el mapa del panel. |
| `coverage_zone` | `color` | varchar(7) | no | Color hexadecimal para el mapa del panel. |
| `coverage_zone` | `valid_until` | timestamptz | no | Cuándo deja de aplicarse. Vacío, sin vencimiento. |


Tipo enumerado `coverage_zone_surcharge_type_enum`: `fixed`, `percentage`.

> **Decisión de modelado.** Una zona usa recargo fijo o porcentual, nunca los dos: `surcharge` guarda el valor y `surcharge_type` dice cómo leerlo. La vigencia sólo tiene fin; el comienzo programado quedó como decisión pendiente en CU-150.

### 10. Dirección resuelta contra el mapa

**Pedido de la cátedra:** Piso y departamento, y guardar el punto que devuelve el servicio de mapas junto con la precisión con que se resolvió.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `user_address` | `floor` | varchar(10) | no | Piso. |
| `user_address` | `apartment` | varchar(10) | no | Departamento. |
| `user_address` | `location` | geography(Point,4326) | no | Punto resuelto, en PostGIS. |
| `user_address` | `place_id` | varchar(255) | no | Identificador estable del lugar en el servicio de mapas. |
| `user_address` | `geocode_precision` | address_geocode_precision_enum | sí | Exacta, aproximada o sin resolver. |


Tipo enumerado `address_geocode_precision_enum`: `exact`, `approximate`, `unresolved`.

> **Decisión de modelado.** `location` reemplaza a `latitude` y `longitude`, que hoy son `varchar` y no se pueden indexar ni consultar por cercanía. Las dos columnas viejas se conservan hasta que los clientes dejen de mandarlas y después se borran.

### 11. Agrupación de pedidos por recorrido

**Pedido de la cátedra:** Armar lotes de pedidos que se entregan en un mismo viaje y ofrecerlos a los choferes de a uno.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `route_batch` **(tabla nueva)** | `batch_id` | uuid | sí | Identificador. |
| `route_batch` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `route_batch` **(tabla nueva)** | `status` | route_batch_status_enum | sí | Ciclo del lote. |
| `route_batch` **(tabla nueva)** | `total_weight_kg` | numeric(10,2) | sí | Suma del peso de los pedidos. |
| `route_batch` **(tabla nueva)** | `delivery_id` | uuid | no | Chofer que lo aceptó. |
| `route_batch` **(tabla nueva)** | `created_at` | timestamptz | sí | Cuándo se armó. |
| `route_batch_stop` **(tabla nueva)** | `stop_id` | uuid | sí | Identificador. |
| `route_batch_stop` **(tabla nueva)** | `batch_id` | uuid | sí | Lote. |
| `route_batch_stop` **(tabla nueva)** | `order_id` | uuid | sí | Pedido. |
| `route_batch_stop` **(tabla nueva)** | `sequence` | integer | sí | Posición en el recorrido. |
| `route_batch_offer` **(tabla nueva)** | `offer_id` | uuid | sí | Identificador. |
| `route_batch_offer` **(tabla nueva)** | `batch_id` | uuid | sí | Lote ofrecido. |
| `route_batch_offer` **(tabla nueva)** | `delivery_id` | uuid | sí | Chofer. |
| `route_batch_offer` **(tabla nueva)** | `status` | proposal_status_enum | sí | Pendiente, aceptada, rechazada o vencida. |
| `route_batch_offer` **(tabla nueva)** | `expires_at` | timestamptz | sí | Fin de la vigencia. |
| `route_batch_offer` **(tabla nueva)** | `responded_at` | timestamptz | no | Cuándo respondió. |

`route_batch` — Un grupo de pedidos que se entregan en un mismo viaje. Clave primaria `batch_id`. Referencias: `distributor_id` → `distributor`, `delivery_id` → `delivery`.
`route_batch_stop` — Cada pedido del lote, en su orden de entrega. Clave primaria `stop_id`. Referencias: `batch_id` → `route_batch`, `order_id` → `order`. Única: (`batch_id`, `order_id`).
`route_batch_offer` — El lote ofrecido a un chofer, con vigencia. Clave primaria `offer_id`. Referencias: `batch_id` → `route_batch`, `delivery_id` → `delivery`.

Tipo enumerado `route_batch_status_enum`: `forming`, `offered`, `assigned`, `dissolved`, `completed`.

> **Decisión de modelado.** El lote no reemplaza al pedido: cada pedido sigue su ciclo de entrega. El lote sólo decide a quién se asignan juntos y en qué orden. Si no se acepta, se deshace y los pedidos vuelven al despacho individual.

### 12. Recupero de envases no devueltos

**Pedido de la cátedra:** Gestionar la devolución de los envases retenidos por escalones, y escalar al administrador cuando no vuelven.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `cylinder_recovery_case` **(tabla nueva)** | `case_id` | uuid | sí | Identificador. |
| `cylinder_recovery_case` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `cylinder_recovery_case` **(tabla nueva)** | `cylinder_id` | uuid | sí | Envase retenido. |
| `cylinder_recovery_case` **(tabla nueva)** | `user_id` | uuid | sí | Cliente que lo tiene. |
| `cylinder_recovery_case` **(tabla nueva)** | `delivered_at` | timestamptz | sí | Cuándo se le entregó el envase. |
| `cylinder_recovery_case` **(tabla nueva)** | `deposit_amount` | numeric(10,2) | sí | Importe comprometido. |
| `cylinder_recovery_case` **(tabla nueva)** | `step` | integer | sí | Escalón en curso. |
| `cylinder_recovery_case` **(tabla nueva)** | `status` | recovery_case_status_enum | sí | Ciclo del caso. |
| `cylinder_recovery_case` **(tabla nueva)** | `opened_at` | timestamptz | sí | Cuándo se abrió. |
| `cylinder_recovery_case` **(tabla nueva)** | `closed_at` | timestamptz | no | Cuándo se cerró. |
| `cylinder_recovery_case` **(tabla nueva)** | `resolved_by_user_id` | uuid | no | Administrador que resolvió. |
| `cylinder_recovery_case` **(tabla nueva)** | `resolution_note` | text | no | Lo que decidió el administrador. |
| `cylinder_recovery_notice` **(tabla nueva)** | `notice_id` | uuid | sí | Identificador. |
| `cylinder_recovery_notice` **(tabla nueva)** | `case_id` | uuid | sí | Caso. |
| `cylinder_recovery_notice` **(tabla nueva)** | `step` | integer | sí | Escalón al que pertenece. |
| `cylinder_recovery_notice` **(tabla nueva)** | `kind` | recovery_notice_kind_enum | sí | Recordatorio, oferta de retiro o aviso de depósito. |
| `cylinder_recovery_notice` **(tabla nueva)** | `status` | proposal_status_enum | no | Respuesta, sólo para la oferta de retiro. |
| `cylinder_recovery_notice` **(tabla nueva)** | `sent_at` | timestamptz | sí | Cuándo se envió. |
| `cylinder_recovery_notice` **(tabla nueva)** | `expires_at` | timestamptz | sí | Plazo del escalón. |

`cylinder_recovery_case` — La gestión de un envase retenido por un cliente. Clave primaria `case_id`. Referencias: `distributor_id` → `distributor`, `cylinder_id` → `cylinder`, `user_id` → `user`, `resolved_by_user_id` → `user`.
`cylinder_recovery_notice` — Cada aviso u oferta de retiro enviados dentro de un caso. Clave primaria `notice_id`. Referencias: `case_id` → `cylinder_recovery_case`.

Tipo enumerado `recovery_case_status_enum`: `open`, `returned`, `escalated`, `deposit_charged`, `written_off`, `closed_no_charge`.
Tipo enumerado `recovery_notice_kind_enum`: `reminder`, `pickup_offer`, `deposit_warning`.

> **Decisión de modelado.** El caso se abre sobre un envase que sigue en poder del cliente pasado el plazo, y cada escalón deja su aviso. Ningún depósito se cobra ni ningún envase se da de baja sin una resolución registrada del administrador.

### 13. Configuración de los procesos automáticos

**Pedido de la cátedra:** Que el administrador ajuste los parámetros de cada proceso automático de su distribuidora.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `module_config` **(tabla nueva)** | `config_id` | uuid | sí | Identificador. |
| `module_config` **(tabla nueva)** | `distributor_id` | uuid | sí | Distribuidora dueña. |
| `module_config` **(tabla nueva)** | `module` | configurable_process_enum | sí | Qué proceso configura: uno de los módulos inteligentes o el despacho express. |
| `module_config` **(tabla nueva)** | `params` | jsonb | sí | Parámetros, validados por el DTO del módulo. |
| `module_config` **(tabla nueva)** | `updated_at` | timestamptz | sí | Última modificación. |
| `module_config` **(tabla nueva)** | `updated_by_user_id` | uuid | no | Quién la modificó. |

`module_config` — Los parámetros de un proceso automático para una distribuidora. Clave primaria `config_id`. Referencias: `distributor_id` → `distributor`, `updated_by_user_id` → `user`. Única: (`distributor_id`, `module`).

Tipo enumerado `configurable_process_enum`: `fleet_planner`, `repurchase`, `route_batching`, `cylinder_recovery`, `express_dispatch`.

> **Decisión de modelado.** La cátedra exige que un proceso automatizado sea configurable desde el sistema. Cada módulo guarda sus parámetros en un JSON validado por su propio DTO: los parámetros de M1 no se parecen a los de M3, y una tabla por módulo sería una tabla de una sola fila.

### 14. Registro de auditoría

**Pedido de la cátedra:** Dejar constancia de toda operación que modifica datos: quién, qué, sobre qué, cuándo, desde dónde y con qué resultado.

| Tabla | Columna | Tipo | Obligatoria | Qué guarda |
|---|---|---|:-:|---|
| `audit_log` **(tabla nueva)** | `audit_id` | uuid | sí | Identificador. |
| `audit_log` **(tabla nueva)** | `distributor_id` | uuid | no | Distribuidora de la operación. |
| `audit_log` **(tabla nueva)** | `actor_user_id` | uuid | no | Quién la originó, según su credencial. |
| `audit_log` **(tabla nueva)** | `actor_role` | varchar(30) | no | Rol con que operó. |
| `audit_log` **(tabla nueva)** | `http_method` | varchar(10) | sí | POST, PUT, PATCH o DELETE. |
| `audit_log` **(tabla nueva)** | `resource` | varchar(60) | sí | Tipo de recurso afectado. |
| `audit_log` **(tabla nueva)** | `resource_id` | varchar(64) | no | Identificador del recurso, si lo hay. |
| `audit_log` **(tabla nueva)** | `path` | varchar(255) | sí | Ruta invocada. |
| `audit_log` **(tabla nueva)** | `client_source` | varchar(30) | no | Panel, app de cliente o app de chofer. |
| `audit_log` **(tabla nueva)** | `ip` | varchar(45) | no | Dirección de red. |
| `audit_log` **(tabla nueva)** | `result` | audit_result_enum | sí | Exitosa o fallida. |
| `audit_log` **(tabla nueva)** | `status_code` | integer | sí | Código HTTP. |
| `audit_log` **(tabla nueva)** | `changes` | jsonb | no | Lo que cambió, con credenciales depuradas. |
| `audit_log` **(tabla nueva)** | `error_message` | text | no | Motivo del rechazo. |
| `audit_log` **(tabla nueva)** | `created_at` | timestamptz | sí | Cuándo. |

`audit_log` — Una fila por operación de escritura, exitosa o fallida. Clave primaria `audit_id`. Referencias: `distributor_id` → `distributor`, `actor_user_id` → `user`.

Tipo enumerado `audit_result_enum`: `success`, `failure`.

> **Decisión de modelado.** El registro es de sólo escritura: no hay modificación ni baja para ningún rol. Las referencias al autor y a la distribuidora quedan vacías si esos registros se borran, pero el asiento no se pierde. Necesita índices por fecha, por autor y por distribuidora (CU-152, rendimiento).

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
| `address_geocode_precision_enum` | `exact`, `approximate`, `unresolved` | propuesto |
| `audit_result_enum` | `success`, `failure` | propuesto |
| `configurable_process_enum` | `fleet_planner`, `repurchase`, `route_batching`, `cylinder_recovery`, `express_dispatch` | propuesto |
| `coverage_zone_surcharge_type_enum` | `fixed`, `percentage` | propuesto |
| `cylinder_inspection_result_enum` | `approved`, `conditional`, `rejected` | propuesto |
| `fleet_status_enum` | `active`, `in_service`, `grounded` | propuesto |
| `incident_moment_enum` | `pre_delivery`, `in_delivery`, `post_delivery` | propuesto |
| `maintenance_criticality_enum` | `blocking`, `non_blocking` | propuesto |
| `maintenance_subject_enum` | `vehicle`, `driver` | propuesto |
| `maintenance_task_status_enum` | `forecast`, `scheduled`, `in_progress`, `done`, `overdue`, `cancelled` | propuesto |
| `maintenance_trigger_enum` | `by_km`, `by_time`, `by_fixed_date` | propuesto |
| `order_delivery_mode_enum` | `standard`, `express` | propuesto |
| `proposal_status_enum` | `pending`, `accepted`, `rejected`, `expired` | propuesto |
| `recovery_case_status_enum` | `open`, `returned`, `escalated`, `deposit_charged`, `written_off`, `closed_no_charge` | propuesto |
| `recovery_notice_kind_enum` | `reminder`, `pickup_offer`, `deposit_warning` | propuesto |
| `repurchase_invitation_status_enum` | `pending`, `accepted`, `rejected`, `expired` | propuesto |
| `route_batch_status_enum` | `forming`, `offered`, `assigned`, `dissolved`, `completed` | propuesto |
