# Modelo de datos del diseño

Documentación técnica del diseño del sistema. No forma parte del Documento 3 de la cátedra, que lleva sólo lo que pide su plantilla; el sitio la publica.

### 7.4 Diagrama Entidad-Relación y Diccionario de Datos

Modelo de datos de las **85 tablas** de la base (977 columnas y **293 claves foráneas, todas declaradas**: no quedan relaciones sin `FOREIGN KEY`). Las 293 son 238 simples (las 230 de las migraciones originales y las 8 que cerró la validación V1 sobre columnas que ya existían) y 55 compuestas `(id, distributor_id)` que impiden que una fila apunte a algo de otra distribuidora. A diferencia del modelo conceptual
del Documento 2 —que describe el dominio del problema—, éste es el modelo de la solución:
incluye claves primarias y foráneas, tipos de dato, restricciones e índices.

Por el tamaño, esta sección da el inventario completo y el diagrama entidad-relación completo,
partido por contexto de negocio para que cada lámina se pueda leer. El diccionario columna por
columna, con descripción, valor por defecto, `CHECK`, índices y claves únicas de cada tabla,
acompaña a la documentación como el archivo `SPLG-modelo-de-datos.md`.

**Cardinalidades.** Cada relación se lee de la clave foránea simple (la compuesta `(id, distributor_id)` se suma a la simple sobre `id`, es la misma relación y no se dibuja dos veces): el lado del padre es obligatorio
(`||`) si la columna no admite nulos y opcional (`o|`) si los admite; el lado del hijo es
«muchos» (`}o`) salvo que la columna sea única, en cuyo caso es «cero o uno» (`|o`). Por eso
`user` se relaciona con `admin`, `customer` y `delivery` de uno a cero-o-uno: un usuario tiene
a lo sumo un perfil de cada clase (`UQ_admin_user` en `admin`; restricciones únicas sobre
`user_id` en `customer` y `delivery`), y un mismo usuario puede tener más de un perfil.

**Convenciones de nombres.** Los nombres reflejan la base real y no están unificados: conviven
columnas en camelCase (`paymentMethod`, `createdAt`, `isActive`, `unitPrice`, `photoUrl`), que
son las de las primeras tablas, y en snake_case (`scheduled_date`, `delivery_mode`,
`photo_url`), que son las de las migraciones posteriores; la tabla `claims` está en plural
y el resto en singular. Unificarlas exigiría renombrar columnas en una base en uso, y no se
hizo; el modelo conceptual no se ve afectado porque nombra los atributos en lenguaje natural.

**Alcance del modelo.** Las tablas y los diagramas de esta sección corresponden a las migraciones de `develop` hasta el reintegro de pagos y la rendición de cobros de cuenta corriente (85 tablas), que incluyen las cinco de compras (`supplier`, `purchase_order`, `purchase_order_item`, `purchase_receipt` y `purchase_receipt_item`) y las dos de la carga del camión (`truck_load` y `truck_load_item`).

**Módulos de gestión de la distribuidora.** Las 85 tablas, las 293 claves foráneas (238 simples y 55 compuestas por distribuidora) y los 79 tipos enumerados que cuenta esta sección son los de la base actual, que ya incluye los módulos de personal (`job_position`, `employee`, `employee_attendance` y `employee_leave`), flota ampliada (`fuel_load`, `traffic_fine`, `vehicle_accident`, `tire` y `tire_event`), stock físico, compras, carga del camión y caja y rendición (§7.4.8), además de `payment_refund` (reintegros de pagos), `attachment` (adjuntos genéricos), `document_sequence` (numeración de comprobantes), `storage_orphan` (archivos pendientes de borrar), la auditoría de datos (`audit`, `audit_detail` y `audit_action_type`) y las columnas `claims.photo_key` y `gas_cylinder.average_unit_cost`. Lo único que sigue propuesto son dos columnas del módulo inteligente M5 (recupero de envases): `cylinder.decommissioned_at` y `cylinder_recovery_notice.order_id`.

#### 7.4.1 Inventario de Entidades

| Contexto | Tabla | Columnas | Qué guarda |
|---|---|:-:|---|
| Organización y acceso | `distributor` | 14 | La distribuidora: la distribuidora. |
| Organización y acceso | `role` | 5 | Catálogo de roles del sistema. |
| Organización y acceso | `user` | 13 | Cuenta global de usuario, base de los tres perfiles. |
| Organización y acceso | `admin` | 4 | Perfil de administrador (de una distribuidora, o superadministrador sin ninguna). |
| Organización y acceso | `module_config` | 6 | Parámetros de cada proceso automático, por distribuidora. |
| Organización y acceso | `audit_log` | 15 | Un asiento por operación de escritura, exitosa o fallida. |
| Organización y acceso | `audit` | 8 | Auditoria: una fila por registro de negocio que se dio de alta, se modificó, se dio de baja o se reactivó (entidad afectada, id del registro, usuario, distribuidora, dirección de red, fecha y hora). De solo escritura. |
| Organización y acceso | `audit_detail` | 5 | DetalleAuditoria: un campo que cambió en una auditoría, con su valor anterior y el nuevo. De solo escritura. |
| Organización y acceso | `audit_action_type` | 2 | TipoAccionAuditoria: catálogo fijo de las acciones (1 Alta, 2 Modificación, 3 Baja lógica, 4 Reactivación, 5 Baja física). |
| Clientes | `customer` | 10 | Perfil de cliente y sus datos de recompra declarados. |
| Clientes | `user_address` | 16 | Dirección de entrega de un usuario. |
| Clientes | `repurchase_invitation` | 11 | Invitación de recompra con el pedido sugerido. |
| Catálogo e inventario de envases | `gas_cylinder` | 13 | Producto: el tipo de garrafa que vende una distribuidora. |
| Catálogo e inventario de envases | `gas_cylinder_promotion` | 5 | Promoción: descuento por cantidad de un producto. |
| Catálogo e inventario de envases | `cylinder` | 13 | Envase físico único, rastreable por número de serie. |
| Catálogo e inventario de envases | `cylinder_movement` | 9 | Historial inmutable de cambios de estado de un envase. |
| Catálogo e inventario de envases | `cylinder_inspection` | 7 | Revisión técnica periódica de un envase. |
| Catálogo e inventario de envases | `cylinder_recovery_case` | 12 | Gestión de un envase retenido por un cliente. |
| Catálogo e inventario de envases | `cylinder_recovery_notice` | 7 | Aviso u oferta de retiro dentro de un caso de recupero. |
| Venta y pedidos | `cart` | 4 | Carrito abierto de un cliente para una distribuidora. |
| Venta y pedidos | `cart_item` | 5 | Ítem cargado en un carrito. |
| Venta y pedidos | `order` | 47 | El pedido (incluye el snapshot `vehicle_*` del vehículo en uso del chofer al aceptarlo). |
| Venta y pedidos | `order_item` | 6 | Ítem de un pedido. |
| Venta y pedidos | `order_status_history` | 7 | Historial de cambios de estado de un pedido. |
| Venta y pedidos | `order_address_change` | 7 | Historial de cambios de dirección de un pedido. |
| Venta y pedidos | `coverage_zone` | 15 | Zona de cobertura (polígono) y su recargo. |
| Venta y pedidos | `time_slot` | 9 | Franja horaria de entrega. |
| Pagos | `payment` | 16 | Intento de pago o transacción en el ledger. |
| Pagos | `payment_refund` | 15 | Devolución de dinero de un pago: el recargo express o lo devuelto de un pedido cancelado, con sus reintentos hasta que la pasarela la confirma. |
| Despacho y logística | `order_dispatch_offer` | 7 | Oferta temporal de un pedido a un chofer. |
| Despacho y logística | `route_batch` | 6 | Lote de pedidos que se entregan en un mismo viaje. |
| Despacho y logística | `route_batch_stop` | 4 | Cada pedido del lote, en su orden de entrega. |
| Despacho y logística | `route_batch_offer` | 6 | El lote ofrecido a un chofer. |
| Flota y choferes | `delivery` | 15 | Perfil de chofer de una distribuidora. |
| Flota y choferes | `car` | 21 | Vehículo de la flota de la distribuidora. |
| Flota y choferes | `vehicle_assignment` | 9 | Qué chofer tiene en uso cada vehículo, con historial (`released_at` null = en uso). |
| Flota y choferes | `maintenance_plan` | 13 | Regla de mantenimiento: qué, cada cuánto, si inhabilita. |
| Flota y choferes | `maintenance_task` | 21 | Vencimiento concreto de un plan (póliza, VTV, service). |
| Flota y choferes | `maintenance_task_attachment` | 10 | Adjunto (comprobante) de una tarea de mantenimiento. |
| Flota y choferes | `maintenance_window_proposal` | 9 | Ventana de taller ofrecida a un chofer. |
| Flota y choferes | `vehicle_usage_log` | 7 | Kilómetros, pedidos y horas en ruta por vehículo y día. |
| Posventa | `claims` | 11 | Reclamo de un cliente sobre un pedido. |
| Posventa | `incident` | 13 | Incidencia reportada sobre un pedido. |
| Posventa | `rating` | 13 | Calificación bidireccional cliente ↔ chofer. |
| Personal | `job_position` | 8 | Puesto de trabajo de una distribuidora: el cargo que ocupa un empleado. |
| Personal | `employee` | 31 | Legajo de un empleado de la distribuidora, con o sin cuenta de usuario. |
| Personal | `employee_attendance` | 11 | Una jornada de un empleado: su ingreso y su egreso, marcados por él o cargados por un administrador. |
| Personal | `employee_leave` | 15 | Licencia o ausencia de un empleado, con su período y su estado. |
| Personal | `attachment` | 12 | Archivo adjunto a un dueño de otro módulo; el dueño es polimórfico (`owner_type`, `owner_id`) y no lleva clave foránea. |
| Gastos de la flota | `fuel_load` | 24 | Una carga de combustible de un vehículo, con su kilometraje y su importe. |
| Gastos de la flota | `traffic_fine` | 21 | Una multa de tránsito de un vehículo, con su ciclo de pendiente a pagada o anulada. |
| Gastos de la flota | `vehicle_accident` | 22 | Un siniestro de un vehículo, de denunciado a cerrado, con sus costos. |
| Gastos de la flota | `tire` | 14 | Un neumático de la distribuidora, en depósito, montado en un vehículo o dado de baja. |
| Gastos de la flota | `tire_event` | 9 | Un movimiento de un neumático; el libro no se modifica. |
| Stock físico y carga del camión | `warehouse` | 11 | Depósito o sucursal de la distribuidora donde se guarda el stock físico; baja lógica y uno solo predeterminado. |
| Stock físico y carga del camión | `stock_location` | 6 | Lugar donde puede haber stock: un depósito o un vehículo. Concentra saldos y movimientos. |
| Stock físico y carga del camión | `stock_balance` | 7 | Cantidad de un tipo de garrafa en una condición (llena, vacía, defectuosa) dentro de una ubicación; nunca negativa. |
| Stock físico y carga del camión | `stock_movement` | 17 | Libro de movimientos de stock, de solo agregado (un disparador impide modificarlo); lo corrige un contraasiento. |
| Stock físico y carga del camión | `stock_threshold` | 8 | Mínimo de llenas de un tipo de garrafa en un depósito, para avisar cuando baja. |
| Stock físico y carga del camión | `stock_adjustment` | 9 | Ajuste de stock numerado, con su motivo y una nota obligatoria. |
| Stock físico y carga del camión | `stock_adjustment_item` | 5 | Diferencia de un tipo de garrafa y condición dentro de un ajuste. |
| Stock físico y carga del camión | `truck_load` | 20 | Hoja de carga del camión: el turno de un vehículo y un chofer, desde que se abre hasta que se rinde, con su número, su día de negocio y su estado; un solo camión y un solo chofer con la carga abierta. |
| Stock físico y carga del camión | `truck_load_item` | 14 | Renglón de la hoja de carga por tipo de garrafa: lo cargado y repuesto, lo declarado al regreso y, al cerrar, lo entregado, lo esperado y la diferencia. |
| Compras | `supplier` | 14 | Proveedor de la distribuidora, principalmente una planta de llenado; baja lógica y CUIT único entre los vigentes. |
| Compras | `purchase_order` | 15 | Orden de compra numerada a un proveedor para un depósito destino, con su estado: borrador, enviada, parcialmente recibida, recibida, cerrada con faltante o cancelada. |
| Compras | `purchase_order_item` | 7 | Tipo de garrafa pedido en una orden, con su costo esperado, los vacíos a canjear y lo recibido. |
| Compras | `purchase_receipt` | 22 | Recepción de compra (remito de ingreso), con o sin orden: comprobante del proveedor, estado de pago y lote del libro de stock. |
| Compras | `purchase_receipt_item` | 9 | Tipo de garrafa recibido en un remito, con los vacíos que se llevó la planta, el costo real y el promedio y la existencia previos. |
| Tablas técnicas | `document_sequence` | 3 | Último número asignado a cada tipo de documento, por distribuidora, para numerar comprobantes correlativos. |
| Tablas técnicas | `stock_reconciliation_alert` | 3 | Última diferencia de conciliación avisada a una distribuidora (su firma), para no repetir el aviso. |
| Tablas técnicas | `storage_orphan` | 9 | Cola de reintento del almacenamiento: archivos que hay que borrar, con intentos y estado. |
| Caja y finanzas | `cash_box` | 10 | Cuenta de fondos de la distribuidora —efectivo, banco o billetera— con su saldo. |
| Caja y finanzas | `cash_session` | 13 | Período de trabajo de una caja entre una apertura y un cierre con arqueo. |
| Caja y finanzas | `cash_category` | 8 | Clasificación de los ingresos y de los gastos de caja, propia o de sistema. |
| Caja y finanzas | `cash_movement` | 15 | Asiento inmutable del libro de una caja: una entrada o una salida de dinero. |
| Caja y finanzas | `driver_settlement` | 22 | Rendición diaria del efectivo que cobró un chofer, con lo esperado, lo declarado y la diferencia. |
| Caja y finanzas | `driver_settlement_order` | 5 | Pedido cobrado en efectivo que integra una rendición; un pedido se rinde una sola vez. |
| Caja y finanzas | `driver_settlement_expense` | 5 | Gasto que el chofer pagó con la cobranza y declara al rendir. |
| Caja y finanzas | `driver_settlement_collection` | 5 | Cobro de cuenta corriente que el chofer recibió en la calle y rinde con el efectivo; cada asiento se rinde una sola vez. |
| Caja y finanzas | `customer_account` | 13 | Cuenta de un cliente en una distribuidora, con su límite de crédito, su plazo de pago y su saldo. |
| Caja y finanzas | `customer_account_entry` | 14 | Asiento inmutable del libro de una cuenta corriente: cargo, pago, nota de crédito o de débito. |
| Caja y finanzas | `customer_account_allocation` | 5 | Aplicación de un pago o una nota de crédito a un cargo, por orden de antigüedad. |
| Caja y finanzas | `commission_rule` | 11 | Regla que dice cuánto gana un chofer por entrega, con su alcance y su vigencia. |
| Caja y finanzas | `commission_entry` | 15 | Asiento inmutable del libro de comisiones de un chofer: una comisión o una deducción. |
| Caja y finanzas | `driver_liquidation` | 19 | Liquidación de las comisiones y las deducciones de un chofer en un período, con su neto a pagar. |

La base completa en una sola lámina: las 85 tablas implementadas agrupadas por contexto de negocio, cada una con su clave primaria y sus claves foráneas, y todas sus relaciones con cardinalidad. Las columnas de cada tabla están en la lámina de su contexto (abajo) y en el diccionario de datos (§7.4.3).

![Modelo físico de la base de datos: vista general](../modelos/base-de-datos/fisico/SPLG-fisico-00-general.png)

**Figura 513 — Modelo físico de la base de datos: vista general**

#### 7.4.2 Diagrama Entidad-Relación (Mermaid)

##### Organización y acceso

![Organización y acceso](../diagramas/png/ER_01_Organizacion-y-acceso.png)

**Figura 514 — Organización y acceso**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    USER }o--o| ROLE : "role_id"
    ADMIN }o--o| DISTRIBUTOR : "distributor_id"
    ADMIN |o--|| USER : "user_id"
    AUDIT }o--|| AUDIT_ACTION_TYPE : "action_type_id"
    AUDIT }o--o| USER : "user_id"
    AUDIT }o--o| DISTRIBUTOR : "distributor_id"
    AUDIT_LOG }o--o| USER : "actor_user_id"
    AUDIT_LOG }o--o| DISTRIBUTOR : "distributor_id"
    MODULE_CONFIG }o--|| DISTRIBUTOR : "distributor_id"
    MODULE_CONFIG }o--o| USER : "updated_by_user_id"
    AUDIT_DETAIL }o--|| AUDIT : "audit_id"

    AUDIT_ACTION_TYPE {
        smallint action_type_id PK
        varchar name UK
    }
    DISTRIBUTOR {
        uuid distributor_id PK
        varchar name
        varchar slug UK
        varchar legal_name "nullable"
        varchar tax_id "nullable"
        varchar email "nullable"
        varchar phone "nullable"
        varchar logo_url "nullable"
        enum status
        varchar plan "nullable"
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
        varchar logo_key "nullable"
    }
    ROLE {
        uuid role_id PK
        text type
        timestamptz createdAt "nullable"
        timestamptz updatedAt "nullable"
        timestamptz deletedAt "nullable"
    }
    USER {
        uuid user_id PK
        uuid role_id FK "nullable"
        varchar firebase_uid UK "nullable"
        varchar full_name "nullable"
        varchar selfie "nullable"
        varchar email UK "nullable"
        varchar phone_number UK "nullable"
        boolean phone_verified
        boolean email_verified
        boolean blocked
        timestamptz createdAt
        timestamptz deletedAt "nullable"
        varchar photo_key "nullable"
    }
    ADMIN {
        uuid admin_id PK
        uuid distributor_id FK "nullable"
        uuid user_id FK, UK
        timestamptz createdAt
    }
    AUDIT {
        uuid audit_id PK
        smallint action_type_id FK
        uuid user_id FK "nullable"
        uuid distributor_id FK "nullable"
        varchar entity
        varchar record_id
        varchar ip "nullable"
        timestamptz created_at
    }
    AUDIT_LOG {
        uuid audit_id PK
        uuid distributor_id FK "nullable"
        uuid actor_user_id FK "nullable"
        varchar actor_role "nullable"
        varchar http_method
        varchar resource
        varchar resource_id "nullable"
        varchar path
        varchar client_source "nullable"
        varchar ip "nullable"
        enum result
        int status_code
        jsonb changes "nullable"
        text error_message "nullable"
        timestamptz created_at
    }
    MODULE_CONFIG {
        uuid config_id PK
        uuid distributor_id FK
        enum module
        jsonb params
        timestamptz updated_at
        uuid updated_by_user_id FK "nullable"
    }
    AUDIT_DETAIL {
        uuid audit_detail_id PK
        uuid audit_id FK
        varchar field
        text old_value "nullable"
        text new_value "nullable"
    }
```

</details>

##### Clientes

![Clientes](../diagramas/png/ER_02_Clientes.png)

**Figura 515 — Clientes**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    REPURCHASE_INVITATION }o--o| USER_ADDRESS : "address_id"

    CUSTOMER {
        uuid customer_id PK
        uuid user_id FK, UK
        text notification_token "nullable"
        timestamptz createdAt "nullable"
        timestamptz deletedAt "nullable"
        geometry location "nullable"
        decimal avg_monthly_consumption_kg "nullable"
        uuid declared_cylinder_type_id FK "nullable"
        int repurchase_notice_days "nullable"
        timestamptz next_repurchase_estimate_at "nullable"
    }
    USER_ADDRESS {
        uuid address_id PK
        uuid user_id FK
        varchar street
        varchar city
        varchar postalCode "nullable"
        text formattedAddress "nullable"
        boolean isDefault
        text additionalInstructions "nullable"
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
        varchar floor "nullable"
        varchar apartment "nullable"
        geometry location "nullable"
        varchar place_id "nullable"
        enum geocode_precision
    }
    REPURCHASE_INVITATION {
        uuid invitation_id PK
        uuid distributor_id FK
        uuid user_id FK
        uuid address_id FK "nullable"
        timestamptz projected_depletion_at
        jsonb suggested_items
        enum status
        timestamptz expires_at
        timestamptz responded_at "nullable"
        uuid order_id FK "nullable"
        timestamptz created_at
    }
```

</details>

##### Catálogo e inventario de envases

![Catálogo e inventario de envases](../diagramas/png/ER_03_Catalogo-e-inventario-de-envases.png)

**Figura 516 — Catálogo e inventario de envases**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    GAS_CYLINDER_PROMOTION }o--|| GAS_CYLINDER : "gas_cylinder_id"
    CYLINDER }o--o| GAS_CYLINDER : "gas_cylinder_id"
    CYLINDER_INSPECTION }o--|| CYLINDER : "cylinder_id"
    CYLINDER_MOVEMENT }o--|| CYLINDER : "cylinder_id"
    CYLINDER_RECOVERY_CASE }o--|| CYLINDER : "cylinder_id"
    CYLINDER_RECOVERY_NOTICE }o--|| CYLINDER_RECOVERY_CASE : "case_id"

    GAS_CYLINDER {
        uuid gas_cylinder_id PK
        uuid distributor_id FK
        varchar type
        decimal weight
        decimal price
        int stock
        text description "nullable"
        boolean isActive
        timestamptz createdAt
        timestamptz updatedAt
        varchar photo_key "nullable"
        decimal average_unit_cost "nullable"
        int reservation_deficit
    }
    GAS_CYLINDER_PROMOTION {
        uuid promotion_id PK
        uuid gas_cylinder_id FK
        int quantity
        decimal discount_percentage
        timestamptz deletedAt "nullable"
    }
    CYLINDER {
        uuid cylinder_id PK
        uuid distributor_id FK
        varchar serial
        uuid gas_cylinder_id FK "nullable"
        enum state
        uuid current_customer_id FK "nullable"
        uuid current_order_id FK "nullable"
        decimal deposit
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz manufactured_at "nullable"
        timestamptz last_inspection_at "nullable"
        timestamptz expires_at "nullable"
    }
    CYLINDER_INSPECTION {
        uuid inspection_id PK
        uuid cylinder_id FK
        uuid distributor_id FK
        timestamptz inspected_at
        enum result
        timestamptz next_due_at "nullable"
        text notes "nullable"
    }
    CYLINDER_MOVEMENT {
        uuid movement_id PK
        uuid cylinder_id FK
        uuid distributor_id FK
        enum from_state "nullable"
        enum to_state
        uuid order_id FK "nullable"
        uuid actor_user_id FK "nullable"
        text note "nullable"
        timestamptz createdAt
    }
    CYLINDER_RECOVERY_CASE {
        uuid case_id PK
        uuid distributor_id FK
        uuid cylinder_id FK
        uuid user_id FK
        timestamptz delivered_at
        decimal deposit_amount
        int step
        enum status
        timestamptz opened_at
        timestamptz closed_at "nullable"
        uuid resolved_by_user_id FK "nullable"
        text resolution_note "nullable"
    }
    CYLINDER_RECOVERY_NOTICE {
        uuid notice_id PK
        uuid case_id FK
        int step
        enum kind
        enum status "nullable"
        timestamptz sent_at
        timestamptz expires_at
    }
```

</details>

##### Venta y pedidos

![Venta y pedidos](../diagramas/png/ER_04_Venta-y-pedidos.png)

**Figura 517 — Venta y pedidos**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    CART_ITEM }o--|| CART : "cart_id"
    ORDER }o--o| COVERAGE_ZONE : "coverage_zone_id"
    ORDER }o--o| TIME_SLOT : "time_slot_id"
    ORDER_ADDRESS_CHANGE }o--|| ORDER : "order_id"
    ORDER_ITEM }o--|| ORDER : "order_id"
    ORDER_STATUS_HISTORY }o--|| ORDER : "order_id"

    COVERAGE_ZONE {
        uuid coverage_zone_id PK
        uuid distributor_id FK
        varchar name
        geometry area
        decimal surcharge_value
        boolean isActive
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
        enum surcharge_type
        varchar label "nullable"
        varchar color "nullable"
        timestamptz valid_until "nullable"
        int priority
        timestamptz valid_from "nullable"
    }
    TIME_SLOT {
        uuid time_slot_id PK
        uuid distributor_id FK
        varchar name
        time startTime
        time endTime
        int capacity
        boolean isActive
        timestamptz createdAt
        timestamptz updatedAt
    }
    CART {
        uuid cart_id PK
        uuid user_id FK
        uuid distributor_id FK
        timestamptz updated_at
    }
    CART_ITEM {
        uuid cart_item_id PK
        uuid cart_id FK
        uuid gas_cylinder_id FK
        int quantity
        decimal unit_price
    }
    ORDER {
        uuid order_id PK
        uuid distributor_id FK
        uuid customer_id FK
        uuid time_slot_id FK "nullable"
        date scheduled_date "nullable"
        decimal deposit_amount
        boolean deposit_paid
        uuid delivery_id FK "nullable"
        uuid address_id FK
        enum status
        enum paymentMethod
        enum paymentType
        enum paymentStatus
        decimal totalAmount
        text notes "nullable"
        text deliveryInstructions "nullable"
        timestamptz acceptedAt "nullable"
        timestamptz onTheWayAt "nullable"
        timestamptz deliveredAt "nullable"
        timestamptz createdAt
        timestamptz updatedAt
        text cancellationReason "nullable"
        varchar gatewayPaymentId "nullable"
        varchar deliveryCode "nullable"
        varchar receiver_name "nullable"
        varchar receiver_document "nullable"
        varchar receiver_relationship "nullable"
        enum delivery_mode
        geometry deliveryPoint "nullable"
        uuid coverage_zone_id FK "nullable"
        varchar zone_name "nullable"
        enum zone_surcharge_type "nullable"
        decimal zone_surcharge_value "nullable"
        decimal zone_surcharge_amount
        decimal subtotal_items
        uuid vehicle_car_id FK "nullable"
        varchar vehicle_patent "nullable"
        varchar vehicle_brand "nullable"
        varchar vehicle_model "nullable"
        timestamptz payment_confirmed_at "nullable"
        uuid payment_confirmed_by FK "nullable"
        text payment_resolution_note "nullable"
        timestamptz payment_resolved_at "nullable"
        uuid payment_resolved_by FK "nullable"
        decimal express_surcharge_amount
        timestamptz express_degraded_at "nullable"
        decimal payment_surcharge_amount
    }
    ORDER_ADDRESS_CHANGE {
        uuid change_id PK
        uuid order_id FK
        uuid from_address_id FK
        uuid to_address_id FK
        uuid changed_by_user_id FK
        timestamptz changed_at
        text reason "nullable"
    }
    ORDER_ITEM {
        uuid order_item_id PK
        uuid order_id FK
        uuid gas_cylinder_id FK
        int quantity
        decimal unitPrice
        decimal subtotal
    }
    ORDER_STATUS_HISTORY {
        uuid history_id PK
        uuid order_id FK
        enum from_status "nullable"
        enum to_status
        uuid changed_by_user_id FK "nullable"
        text reason "nullable"
        timestamptz changed_at
    }
```

</details>

##### Pagos

![Pagos](../diagramas/png/ER_05_Pagos.png)

**Figura 518 — Pagos**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    PAYMENT_REFUND }o--|| PAYMENT : "payment_id"

    PAYMENT {
        uuid payment_id PK
        uuid order_id FK
        uuid distributor_id FK "nullable"
        enum gateway
        enum integration
        varchar method "nullable"
        varchar gateway_payment_id "nullable"
        varchar external_reference "nullable"
        decimal amount
        varchar currency
        enum status
        text payment_url "nullable"
        boolean is_deposit
        jsonb metadata "nullable"
        timestamptz createdAt
        timestamptz updatedAt
    }
    PAYMENT_REFUND {
        uuid refund_id PK
        uuid payment_id FK
        uuid order_id FK
        uuid distributor_id FK "nullable"
        enum kind
        decimal amount
        enum status
        varchar gateway_refund_id "nullable"
        text error_message "nullable"
        int attempts
        timestamptz refunded_at "nullable"
        uuid requested_by_user_id FK "nullable"
        timestamptz createdAt
        timestamptz updatedAt
        decimal refunded_baseline "nullable"
    }
```

</details>

##### Despacho y logística

![Despacho y logística](../diagramas/png/ER_06_Despacho-y-logistica.png)

**Figura 519 — Despacho y logística**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    ROUTE_BATCH_OFFER }o--|| ROUTE_BATCH : "batch_id"
    ROUTE_BATCH_STOP }o--|| ROUTE_BATCH : "batch_id"

    ROUTE_BATCH {
        uuid batch_id PK
        uuid distributor_id FK
        enum status
        decimal total_weight_kg
        uuid delivery_id FK "nullable"
        timestamptz created_at
    }
    ORDER_DISPATCH_OFFER {
        uuid offer_id PK
        uuid distributor_id FK
        uuid order_id FK
        uuid driver_id FK
        enum status
        timestamptz expiresAt
        timestamptz offeredAt
    }
    ROUTE_BATCH_OFFER {
        uuid offer_id PK
        uuid batch_id FK
        uuid delivery_id FK
        enum status
        timestamptz expires_at
        timestamptz responded_at "nullable"
    }
    ROUTE_BATCH_STOP {
        uuid stop_id PK
        uuid batch_id FK
        uuid order_id FK
        int sequence
    }
```

</details>

##### Flota y choferes

![Flota y choferes](../diagramas/png/ER_07_Flota-y-choferes.png)

**Figura 520 — Flota y choferes**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    MAINTENANCE_TASK }o--o| DELIVERY : "delivery_id"
    MAINTENANCE_TASK }o--|| MAINTENANCE_PLAN : "plan_id"
    MAINTENANCE_TASK }o--o| CAR : "car_id"
    VEHICLE_ASSIGNMENT }o--|| DELIVERY : "delivery_id"
    VEHICLE_ASSIGNMENT }o--|| CAR : "car_id"
    VEHICLE_USAGE_LOG }o--|| CAR : "car_id"
    MAINTENANCE_TASK_ATTACHMENT }o--|| MAINTENANCE_TASK : "task_id"
    MAINTENANCE_WINDOW_PROPOSAL }o--|| MAINTENANCE_TASK : "task_id"
    MAINTENANCE_WINDOW_PROPOSAL }o--|| DELIVERY : "delivery_id"

    MAINTENANCE_PLAN {
        uuid plan_id PK
        uuid distributor_id FK
        varchar name
        enum subject
        enum trigger
        int interval_km "nullable"
        int interval_months "nullable"
        int lead_time_days
        enum criticality
        varchar car_type "nullable"
        boolean is_active
        enum document_kind "nullable"
        _varchar applies_to_categories "nullable"
    }
    CAR {
        uuid car_id PK
        uuid distributor_id FK
        uuid user_id FK
        varchar type_car "nullable"
        int car_capacity "nullable"
        varchar car_patent "nullable"
        varchar car_brand "nullable"
        varchar car_model "nullable"
        int car_year "nullable"
        varchar car_color "nullable"
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
        decimal tare_weight_kg "nullable"
        decimal max_load_kg "nullable"
        int odometer_km "nullable"
        enum fleet_status
        timestamptz in_service_since "nullable"
        varchar photo_key "nullable"
        enum fuel_type "nullable"
        decimal tank_capacity_liters "nullable"
    }
    DELIVERY {
        uuid delivery_id PK
        uuid distributor_id FK
        uuid user_id FK, UK
        float calification "nullable"
        text actual_location "nullable"
        real cancelledCharge "nullable"
        boolean validated
        boolean isActive
        text notification_token "nullable"
        decimal balance
        timestamptz createdAt "nullable"
        timestamptz deletedAt "nullable"
        geometry location "nullable"
        boolean isEnabled
        boolean isAvailable
    }
    MAINTENANCE_TASK {
        uuid task_id PK
        uuid plan_id FK
        uuid distributor_id FK
        uuid car_id FK "nullable"
        uuid delivery_id FK "nullable"
        enum status
        timestamptz due_at "nullable"
        int due_km "nullable"
        timestamptz predicted_due_at "nullable"
        timestamptz scheduled_at "nullable"
        timestamptz performed_at "nullable"
        int odometer_km "nullable"
        decimal cost "nullable"
        varchar provider "nullable"
        varchar reference_number "nullable"
        varchar category "nullable"
        timestamptz alerted_at "nullable"
        text notes "nullable"
        timestamptz valid_from "nullable"
        uuid employee_id FK "nullable"
        jsonb details "nullable"
    }
    VEHICLE_ASSIGNMENT {
        uuid assignment_id PK
        uuid distributor_id FK
        uuid car_id FK
        uuid delivery_id FK
        timestamptz assigned_at
        timestamptz released_at "nullable"
        uuid assigned_by_user_id FK "nullable"
        uuid released_by_user_id FK "nullable"
        text note "nullable"
    }
    VEHICLE_USAGE_LOG {
        uuid log_id PK
        uuid car_id FK
        uuid distributor_id FK
        date day
        decimal km
        int orders
        decimal route_hours
    }
    MAINTENANCE_TASK_ATTACHMENT {
        uuid attachment_id PK
        uuid task_id FK
        uuid distributor_id FK
        varchar storage_key
        varchar original_name
        varchar mime_type
        int size_bytes
        uuid uploaded_by_user_id FK
        timestamptz uploaded_at
        timestamptz deleted_at "nullable"
    }
    MAINTENANCE_WINDOW_PROPOSAL {
        uuid proposal_id PK
        uuid task_id FK
        uuid delivery_id FK
        timestamptz window_start
        timestamptz window_end
        int rank
        enum status
        timestamptz expires_at
        timestamptz responded_at "nullable"
    }
```

</details>

##### Posventa

![Posventa](../diagramas/png/ER_08_Posventa.png)

**Figura 521 — Posventa**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram

    CLAIMS {
        uuid claim_id PK
        uuid distributor_id FK
        uuid order_id FK
        uuid customer_id FK
        varchar reason
        text description
        varchar photoUrl "nullable"
        enum status
        text resolutionNote "nullable"
        timestamptz createdAt
        varchar photo_key "nullable"
    }
    INCIDENT {
        uuid incident_id PK
        uuid order_id FK
        uuid distributor_id FK
        uuid reported_by FK
        enum type
        text description
        varchar photo_url "nullable"
        enum status
        text resolution_note "nullable"
        timestamptz createdAt
        timestamptz resolvedAt "nullable"
        enum moment "nullable"
        varchar photo_key "nullable"
    }
    RATING {
        uuid rating_id PK
        uuid order_id FK
        uuid distributor_id FK
        uuid from_user_id FK
        uuid to_user_id FK
        enum from_role
        int stars
        text comment "nullable"
        timestamptz createdAt
        boolean hidden
        text hidden_reason "nullable"
        timestamptz hidden_at "nullable"
        uuid hidden_by_user_id FK "nullable"
    }
```

</details>

##### Personal

![Personal](../diagramas/png/ER_09_Personal.png)

**Figura 522 — Personal**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    EMPLOYEE }o--|| JOB_POSITION : "position_id"
    EMPLOYEE_ATTENDANCE }o--|| EMPLOYEE : "employee_id"
    EMPLOYEE_LEAVE }o--|| EMPLOYEE : "employee_id"

    JOB_POSITION {
        uuid position_id PK
        uuid distributor_id FK
        varchar name
        enum category
        boolean is_active
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
    }
    ATTACHMENT {
        uuid attachment_id PK
        uuid distributor_id FK
        enum owner_type
        uuid owner_id
        varchar label "nullable"
        varchar storage_key
        varchar original_name
        varchar mime_type
        int size_bytes
        uuid uploaded_by_user_id FK
        timestamptz uploaded_at
        timestamptz deleted_at "nullable"
    }
    EMPLOYEE {
        uuid employee_id PK
        uuid distributor_id FK
        uuid user_id FK "nullable"
        uuid position_id FK
        varchar file_number
        varchar first_name
        varchar last_name
        enum document_type
        varchar document_number
        varchar cuil "nullable"
        date birth_date "nullable"
        varchar address_line "nullable"
        varchar city "nullable"
        varchar province "nullable"
        varchar postal_code "nullable"
        varchar phone "nullable"
        varchar personal_email "nullable"
        varchar emergency_contact_name "nullable"
        varchar emergency_contact_phone "nullable"
        varchar emergency_contact_relationship "nullable"
        date hire_date
        date termination_date "nullable"
        enum termination_reason "nullable"
        enum employment_type
        enum status
        varchar bank_cbu "nullable"
        text notes "nullable"
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
        varchar photo_key "nullable"
    }
    EMPLOYEE_ATTENDANCE {
        uuid attendance_id PK
        uuid distributor_id FK
        uuid employee_id FK
        date work_date
        timestamptz check_in_at
        timestamptz check_out_at "nullable"
        enum source
        uuid recorded_by_user_id FK "nullable"
        text notes "nullable"
        timestamptz createdAt
        timestamptz updatedAt
    }
    EMPLOYEE_LEAVE {
        uuid leave_id PK
        uuid distributor_id FK
        uuid employee_id FK
        enum type
        date start_date
        date end_date
        int days
        enum status
        text reason "nullable"
        text rejection_reason "nullable"
        uuid requested_by_user_id FK "nullable"
        uuid decided_by_user_id FK "nullable"
        timestamptz decided_at "nullable"
        timestamptz createdAt
        timestamptz updatedAt
    }
```

</details>

##### Gastos de la flota

![Gastos de la flota](../diagramas/png/ER_10_Gastos-de-la-flota.png)

**Figura 523 — Gastos de la flota**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    TIRE_EVENT }o--|| TIRE : "tire_id"

    TIRE {
        uuid tire_id PK
        uuid distributor_id FK
        varchar serial_number
        varchar brand
        varchar size
        decimal cost
        enum status
        uuid car_id FK "nullable"
        varchar position "nullable"
        int mounted_odometer_km "nullable"
        int km_traveled
        int retread_count
        timestamptz createdAt
        timestamptz updatedAt
    }
    VEHICLE_ACCIDENT {
        uuid accident_id PK
        uuid distributor_id FK
        uuid car_id FK
        uuid employee_id FK "nullable"
        timestamptz occurred_at
        geometry location "nullable"
        text address "nullable"
        text description
        boolean injuries
        boolean third_parties_involved
        boolean hazmat_release
        varchar police_report_number "nullable"
        varchar insurer_claim_number "nullable"
        enum status
        boolean vehicle_unusable
        decimal repair_cost "nullable"
        decimal insurer_reimbursement "nullable"
        decimal deductible_amount "nullable"
        timestamptz closed_at "nullable"
        uuid created_by_user_id FK
        timestamptz createdAt
        timestamptz updatedAt
    }
    FUEL_LOAD {
        uuid fuel_load_id PK
        uuid distributor_id FK
        uuid car_id FK
        uuid employee_id FK "nullable"
        timestamptz loaded_at
        enum fuel_type
        decimal liters
        decimal unit_price
        decimal total_amount
        int odometer_km
        boolean is_full_tank
        varchar station "nullable"
        enum payment_method
        varchar receipt_number "nullable"
        boolean anomaly
        text notes "nullable"
        text odometer_correction_note "nullable"
        uuid created_by_user_id FK
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
        uuid cash_movement_id FK "nullable"
        boolean registered_by_driver
        boolean cash_payment_legacy
    }
    TIRE_EVENT {
        uuid event_id PK
        uuid tire_id FK
        uuid distributor_id FK
        enum type
        uuid car_id FK "nullable"
        varchar position "nullable"
        int odometer_km
        uuid created_by_user_id FK
        timestamptz createdAt
    }
    TRAFFIC_FINE {
        uuid fine_id PK
        uuid distributor_id FK
        uuid car_id FK
        uuid employee_id FK "nullable"
        timestamptz occurred_at
        varchar jurisdiction
        varchar act_number
        text infraction
        decimal amount
        decimal voluntary_payment_amount "nullable"
        date due_date "nullable"
        enum status
        timestamptz paid_at "nullable"
        decimal paid_amount "nullable"
        boolean charged_to_employee
        text void_reason "nullable"
        timestamptz voided_at "nullable"
        timestamptz alerted_at "nullable"
        timestamptz createdAt
        timestamptz updatedAt
        uuid cash_movement_id FK "nullable"
    }
```

</details>

##### Stock físico y carga del camión

![Stock físico y carga del camión](../diagramas/png/ER_11_Stock-fisico-y-carga-del-camion.png)

**Figura 524 — Stock físico y carga del camión**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    STOCK_THRESHOLD }o--|| WAREHOUSE : "warehouse_id"
    STOCK_LOCATION |o--o| WAREHOUSE : "warehouse_id"
    STOCK_ADJUSTMENT }o--|| STOCK_LOCATION : "location_id"
    STOCK_BALANCE }o--|| STOCK_LOCATION : "location_id"
    STOCK_MOVEMENT }o--o| STOCK_LOCATION : "to_location_id"
    STOCK_MOVEMENT }o--o| STOCK_LOCATION : "from_location_id"
    STOCK_MOVEMENT }o--o| STOCK_MOVEMENT : "reversed_movement_id"
    TRUCK_LOAD }o--|| STOCK_LOCATION : "origin_location_id"
    STOCK_ADJUSTMENT_ITEM }o--|| STOCK_ADJUSTMENT : "adjustment_id"
    TRUCK_LOAD_ITEM }o--|| TRUCK_LOAD : "load_id"

    WAREHOUSE {
        uuid warehouse_id PK
        uuid distributor_id FK
        varchar name
        varchar code
        enum kind
        text address "nullable"
        boolean is_default
        boolean is_active
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
    }
    STOCK_THRESHOLD {
        uuid threshold_id PK
        uuid distributor_id FK
        uuid warehouse_id FK
        uuid gas_cylinder_id FK
        int min_full
        timestamptz alerted_at "nullable"
        timestamptz createdAt
        timestamptz updatedAt
    }
    STOCK_LOCATION {
        uuid location_id PK
        uuid distributor_id FK
        enum kind
        uuid warehouse_id FK, UK "nullable"
        uuid car_id FK, UK "nullable"
        timestamptz createdAt
    }
    STOCK_ADJUSTMENT {
        uuid adjustment_id PK
        uuid distributor_id FK
        int number
        uuid location_id FK
        enum reason
        text notes
        uuid batch_id
        uuid created_by_user_id FK
        timestamptz createdAt
    }
    STOCK_BALANCE {
        uuid balance_id PK
        uuid distributor_id FK
        uuid location_id FK
        uuid gas_cylinder_id FK
        enum condition
        int quantity
        timestamptz updatedAt
    }
    STOCK_MOVEMENT {
        uuid movement_id PK
        uuid distributor_id FK
        uuid gas_cylinder_id FK
        uuid batch_id
        int quantity
        uuid from_location_id FK "nullable"
        enum from_condition "nullable"
        uuid to_location_id FK "nullable"
        enum to_condition "nullable"
        enum reason
        enum reference_type
        uuid reference_id "nullable"
        uuid reversed_movement_id FK "nullable"
        varchar notes "nullable"
        uuid actor_user_id FK "nullable"
        timestamptz occurred_at
        timestamptz createdAt
    }
    TRUCK_LOAD {
        uuid load_id PK
        uuid distributor_id FK
        int number
        uuid car_id FK
        uuid delivery_id FK
        uuid helper_employee_id FK "nullable"
        uuid origin_location_id FK
        date business_date
        enum status
        timestamptz opened_at
        timestamptz departed_at "nullable"
        timestamptz returned_at "nullable"
        timestamptz closed_at "nullable"
        uuid opened_by_user_id FK
        uuid closed_by_user_id FK "nullable"
        text difference_note "nullable"
        text cancel_reason "nullable"
        text notes "nullable"
        timestamptz createdAt
        timestamptz updatedAt
    }
    STOCK_ADJUSTMENT_ITEM {
        uuid item_id PK
        uuid adjustment_id FK
        uuid gas_cylinder_id FK
        enum condition
        int quantity_delta
    }
    TRUCK_LOAD_ITEM {
        uuid item_id PK
        uuid load_id FK
        uuid gas_cylinder_id FK
        int loaded_full
        int reloaded_full
        int loaded_empty
        int declared_return_full "nullable"
        int declared_return_empty "nullable"
        int delivered_full "nullable"
        int collected_empty "nullable"
        int expected_full "nullable"
        int expected_empty "nullable"
        int difference_full "nullable"
        int difference_empty "nullable"
    }
```

</details>

##### Compras

![Compras](../diagramas/png/ER_12_Compras.png)

**Figura 525 — Compras**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    PURCHASE_ORDER }o--|| SUPPLIER : "supplier_id"
    PURCHASE_ORDER_ITEM }o--|| PURCHASE_ORDER : "purchase_order_id"
    PURCHASE_RECEIPT }o--|| SUPPLIER : "supplier_id"
    PURCHASE_RECEIPT }o--o| PURCHASE_ORDER : "purchase_order_id"
    PURCHASE_RECEIPT_ITEM }o--|| PURCHASE_RECEIPT : "receipt_id"

    SUPPLIER {
        uuid supplier_id PK
        uuid distributor_id FK
        varchar business_name
        varchar cuit
        enum kind
        varchar contact_name "nullable"
        varchar phone "nullable"
        varchar email "nullable"
        text address "nullable"
        int payment_terms_days "nullable"
        boolean is_active
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
    }
    PURCHASE_ORDER {
        uuid purchase_order_id PK
        uuid distributor_id FK
        int number
        uuid supplier_id FK
        uuid destination_warehouse_id FK
        enum status
        timestamptz issued_at "nullable"
        date expected_date "nullable"
        decimal total_amount
        text cancel_reason "nullable"
        text notes "nullable"
        uuid created_by_user_id FK
        timestamptz createdAt
        timestamptz updatedAt
        text close_reason "nullable"
    }
    PURCHASE_ORDER_ITEM {
        uuid item_id PK
        uuid purchase_order_id FK
        uuid gas_cylinder_id FK
        int quantity
        decimal unit_cost
        int empties_to_exchange
        int received_quantity
    }
    PURCHASE_RECEIPT {
        uuid receipt_id PK
        uuid distributor_id FK
        int number
        uuid supplier_id FK
        uuid purchase_order_id FK "nullable"
        uuid warehouse_id FK
        enum supplier_document_type
        varchar supplier_document_number
        timestamptz received_at
        uuid received_by_user_id FK
        decimal total_amount
        enum payment_status
        uuid cash_movement_id FK "nullable"
        enum status
        text void_reason "nullable"
        timestamptz voided_at "nullable"
        uuid voided_by_user_id FK "nullable"
        uuid batch_id
        uuid void_batch_id "nullable"
        text notes "nullable"
        timestamptz createdAt
        timestamptz updatedAt
    }
    PURCHASE_RECEIPT_ITEM {
        uuid item_id PK
        uuid receipt_id FK
        uuid gas_cylinder_id FK
        int quantity_full
        int quantity_empty_out
        decimal unit_cost
        decimal previous_average_cost "nullable"
        int previous_on_hand "nullable"
        timestamptz previous_on_hand_at "nullable"
    }
```

</details>


![Modelo físico: compras](../modelos/base-de-datos/fisico/SPLG-fisico-12-compras.png)

##### Tablas técnicas

![Tablas técnicas](../diagramas/png/ER_13_Tablas-tecnicas.png)

**Figura 526 — Tablas técnicas**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram

    STORAGE_ORPHAN {
        uuid orphan_id PK
        varchar storage_key UK
        int attempts
        text last_error "nullable"
        timestamptz created_at
        timestamptz updated_at
        varchar kind
        varchar status
        timestamptz next_attempt_at
    }
    DOCUMENT_SEQUENCE {
        uuid distributor_id PK
        varchar doc_type PK
        int last_number
    }
    STOCK_RECONCILIATION_ALERT {
        uuid distributor_id PK
        varchar signature
        timestamptz alerted_at
    }
```

</details>

##### Caja y finanzas

![Caja y finanzas](../diagramas/png/ER_14_Caja-y-finanzas.png)

**Figura 527 — Caja y finanzas**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    CASH_SESSION }o--|| CASH_BOX : "cash_box_id"
    CASH_MOVEMENT }o--o| CASH_MOVEMENT : "reverses_movement_id"
    CASH_MOVEMENT }o--|| CASH_BOX : "cash_box_id"
    CASH_MOVEMENT }o--|| CASH_CATEGORY : "category_id"
    CASH_MOVEMENT }o--o| CASH_SESSION : "session_id"
    CUSTOMER_ACCOUNT_ENTRY }o--o| CASH_MOVEMENT : "cash_movement_id"
    CUSTOMER_ACCOUNT_ENTRY }o--|| CUSTOMER_ACCOUNT : "account_id"
    DRIVER_LIQUIDATION }o--o| CASH_MOVEMENT : "cash_movement_id"
    COMMISSION_ENTRY }o--o| COMMISSION_RULE : "rule_id"
    COMMISSION_ENTRY }o--o| DRIVER_LIQUIDATION : "liquidation_id"
    CUSTOMER_ACCOUNT_ALLOCATION }o--|| CUSTOMER_ACCOUNT_ENTRY : "debit_entry_id"
    CUSTOMER_ACCOUNT_ALLOCATION }o--|| CUSTOMER_ACCOUNT_ENTRY : "credit_entry_id"
    CUSTOMER_ACCOUNT_ALLOCATION }o--|| CUSTOMER_ACCOUNT : "account_id"
    DRIVER_SETTLEMENT }o--o| CASH_BOX : "destination_cash_box_id"
    DRIVER_SETTLEMENT }o--o| CASH_MOVEMENT : "cash_movement_id"
    DRIVER_SETTLEMENT_COLLECTION |o--|| CUSTOMER_ACCOUNT_ENTRY : "entry_id"
    DRIVER_SETTLEMENT_COLLECTION }o--|| DRIVER_SETTLEMENT : "settlement_id"
    DRIVER_SETTLEMENT_EXPENSE }o--|| DRIVER_SETTLEMENT : "settlement_id"
    DRIVER_SETTLEMENT_EXPENSE }o--|| CASH_CATEGORY : "category_id"
    DRIVER_SETTLEMENT_ORDER }o--|| DRIVER_SETTLEMENT : "settlement_id"

    CASH_BOX {
        uuid cash_box_id PK
        uuid distributor_id FK
        varchar name
        enum kind
        decimal balance
        boolean requires_session
        boolean is_active
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
    }
    CASH_CATEGORY {
        uuid category_id PK
        uuid distributor_id FK
        varchar name
        enum direction
        enum system_code "nullable"
        boolean is_active
        timestamptz createdAt
        timestamptz updatedAt
    }
    CASH_SESSION {
        uuid session_id PK
        uuid distributor_id FK
        uuid cash_box_id FK
        enum status
        timestamptz opened_at
        uuid opened_by_user_id FK
        decimal opening_amount
        timestamptz closed_at "nullable"
        uuid closed_by_user_id FK "nullable"
        decimal expected_amount "nullable"
        decimal counted_amount "nullable"
        decimal difference "nullable"
        text notes "nullable"
    }
    CUSTOMER_ACCOUNT {
        uuid account_id PK
        uuid distributor_id FK
        uuid customer_user_id FK
        varchar business_name
        varchar tax_id "nullable"
        enum tax_condition
        decimal credit_limit
        int payment_terms_days
        enum status
        decimal balance
        timestamptz createdAt
        timestamptz updatedAt
        timestamptz deletedAt "nullable"
    }
    CASH_MOVEMENT {
        uuid movement_id PK
        uuid distributor_id FK
        uuid cash_box_id FK
        uuid session_id FK "nullable"
        enum direction
        decimal amount
        uuid category_id FK
        enum method
        timestamptz occurred_at
        varchar description
        enum reference_type
        uuid reference_id "nullable"
        uuid reverses_movement_id FK "nullable"
        uuid created_by_user_id FK
        timestamptz createdAt
    }
    COMMISSION_RULE {
        uuid rule_id PK
        uuid distributor_id FK
        uuid employee_id FK "nullable"
        uuid gas_cylinder_id FK "nullable"
        enum basis
        decimal value
        date valid_from
        date valid_to "nullable"
        boolean is_active
        timestamptz createdAt
        timestamptz updatedAt
    }
    CUSTOMER_ACCOUNT_ENTRY {
        uuid entry_id PK
        uuid distributor_id FK
        uuid account_id FK
        enum type
        decimal amount
        uuid order_id FK "nullable"
        date due_date "nullable"
        varchar payment_method "nullable"
        uuid cash_movement_id FK "nullable"
        uuid collected_by_delivery_id FK "nullable"
        varchar description "nullable"
        timestamptz occurred_at
        uuid created_by_user_id FK "nullable"
        timestamptz createdAt
    }
    DRIVER_LIQUIDATION {
        uuid liquidation_id PK
        uuid distributor_id FK
        int number
        uuid employee_id FK
        date period_from
        date period_to
        decimal gross
        decimal deductions
        decimal net
        enum status
        timestamptz approved_at "nullable"
        uuid approved_by_user_id FK "nullable"
        timestamptz paid_at "nullable"
        uuid paid_by_user_id FK "nullable"
        timestamptz voided_at "nullable"
        uuid cash_movement_id FK "nullable"
        uuid created_by_user_id FK
        timestamptz createdAt
        timestamptz updatedAt
    }
    COMMISSION_ENTRY {
        uuid entry_id PK
        uuid distributor_id FK
        uuid employee_id FK
        uuid delivery_id FK "nullable"
        enum type
        decimal amount
        uuid order_id FK "nullable"
        uuid rule_id FK "nullable"
        jsonb rule_snapshot "nullable"
        uuid liquidation_id FK "nullable"
        uuid reference_id "nullable"
        varchar description
        timestamptz occurred_at
        uuid created_by_user_id FK "nullable"
        timestamptz createdAt
    }
    CUSTOMER_ACCOUNT_ALLOCATION {
        uuid allocation_id PK
        uuid account_id FK
        uuid debit_entry_id FK
        uuid credit_entry_id FK
        decimal amount
    }
    DRIVER_SETTLEMENT {
        uuid settlement_id PK
        uuid distributor_id FK
        uuid delivery_id FK
        int number
        uuid truck_load_id FK "nullable"
        date business_date
        enum status
        decimal expected_cash
        decimal declared_cash "nullable"
        decimal driver_expenses
        decimal difference "nullable"
        enum difference_resolution "nullable"
        uuid destination_cash_box_id FK "nullable"
        uuid cash_movement_id FK "nullable"
        timestamptz submitted_at "nullable"
        uuid submitted_by_user_id FK "nullable"
        timestamptz approved_at "nullable"
        uuid approved_by_user_id FK "nullable"
        text notes "nullable"
        timestamptz overdue_alerted_at "nullable"
        timestamptz createdAt
        timestamptz updatedAt
    }
    DRIVER_SETTLEMENT_COLLECTION {
        uuid collection_id PK
        uuid settlement_id FK
        uuid entry_id FK, UK
        decimal amount
        timestamptz createdAt
    }
    DRIVER_SETTLEMENT_EXPENSE {
        uuid expense_id PK
        uuid settlement_id FK
        uuid category_id FK
        decimal amount
        varchar description "nullable"
    }
    DRIVER_SETTLEMENT_ORDER {
        uuid settlement_order_id PK
        uuid settlement_id FK
        uuid order_id FK, UK
        decimal amount
        varchar payment_method
    }
```

</details>

##### Relaciones entre contextos

Las que cruzan de un contexto a otro (ya sin repetir la entidad completa; sus columnas están en la lámina de su propio contexto). La relación con `distributor` se omite acá también por lo mismo que en el conceptual: prácticamente todo pertenece a una distribuidora.

![Relaciones entre contextos](../diagramas/png/ER_15_Relaciones-entre-contextos.png)

**Figura 528 — Relaciones entre contextos**

<details><summary>Ver código del diagrama</summary>

```mermaid
erDiagram
    ATTACHMENT }o--|| USER : "uploaded_by_user_id"
    CAR }o--|| USER : "user_id"
    CART }o--|| USER : "user_id"
    CASH_SESSION }o--|| USER : "opened_by_user_id"
    CASH_SESSION }o--o| USER : "closed_by_user_id"
    CUSTOMER |o--|| USER : "user_id"
    CUSTOMER }o--o| GAS_CYLINDER : "declared_cylinder_type_id"
    CUSTOMER_ACCOUNT }o--|| USER : "customer_user_id"
    DELIVERY |o--|| USER : "user_id"
    EMPLOYEE }o--o| USER : "user_id"
    PURCHASE_ORDER }o--|| WAREHOUSE : "destination_warehouse_id"
    PURCHASE_ORDER }o--|| USER : "created_by_user_id"
    STOCK_THRESHOLD }o--|| GAS_CYLINDER : "gas_cylinder_id"
    USER_ADDRESS }o--|| USER : "user_id"
    CART_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    CASH_MOVEMENT }o--|| USER : "created_by_user_id"
    COMMISSION_RULE }o--o| EMPLOYEE : "employee_id"
    COMMISSION_RULE }o--o| GAS_CYLINDER : "gas_cylinder_id"
    EMPLOYEE_ATTENDANCE }o--o| USER : "recorded_by_user_id"
    EMPLOYEE_LEAVE }o--o| USER : "decided_by_user_id"
    EMPLOYEE_LEAVE }o--o| USER : "requested_by_user_id"
    MAINTENANCE_TASK }o--o| EMPLOYEE : "employee_id"
    ORDER }o--o| DELIVERY : "delivery_id"
    ORDER }o--|| USER : "customer_id"
    ORDER }o--|| USER_ADDRESS : "address_id"
    ORDER }o--o| USER : "payment_confirmed_by"
    ORDER }o--o| USER : "payment_resolved_by"
    ORDER }o--o| CAR : "vehicle_car_id"
    PURCHASE_ORDER_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    ROUTE_BATCH }o--o| DELIVERY : "delivery_id"
    STOCK_LOCATION |o--o| CAR : "car_id"
    TIRE }o--o| CAR : "car_id"
    VEHICLE_ACCIDENT }o--o| EMPLOYEE : "employee_id"
    VEHICLE_ACCIDENT }o--|| USER : "created_by_user_id"
    VEHICLE_ACCIDENT }o--|| CAR : "car_id"
    VEHICLE_ASSIGNMENT }o--o| USER : "released_by_user_id"
    VEHICLE_ASSIGNMENT }o--o| USER : "assigned_by_user_id"
    CLAIMS }o--|| ORDER : "order_id"
    CLAIMS }o--|| USER : "customer_id"
    CUSTOMER_ACCOUNT_ENTRY }o--o| DELIVERY : "collected_by_delivery_id"
    CUSTOMER_ACCOUNT_ENTRY }o--o| ORDER : "order_id"
    CUSTOMER_ACCOUNT_ENTRY }o--o| USER : "created_by_user_id"
    CYLINDER }o--o| USER : "current_customer_id"
    CYLINDER }o--o| ORDER : "current_order_id"
    DRIVER_LIQUIDATION }o--|| USER : "created_by_user_id"
    DRIVER_LIQUIDATION }o--o| USER : "paid_by_user_id"
    DRIVER_LIQUIDATION }o--o| USER : "approved_by_user_id"
    DRIVER_LIQUIDATION }o--|| EMPLOYEE : "employee_id"
    FUEL_LOAD }o--|| CAR : "car_id"
    FUEL_LOAD }o--|| USER : "created_by_user_id"
    FUEL_LOAD }o--o| EMPLOYEE : "employee_id"
    FUEL_LOAD }o--o| CASH_MOVEMENT : "cash_movement_id"
    INCIDENT }o--|| USER : "reported_by"
    INCIDENT }o--|| ORDER : "order_id"
    MAINTENANCE_TASK_ATTACHMENT }o--|| USER : "uploaded_by_user_id"
    ORDER_ADDRESS_CHANGE }o--|| USER_ADDRESS : "to_address_id"
    ORDER_ADDRESS_CHANGE }o--|| USER_ADDRESS : "from_address_id"
    ORDER_ADDRESS_CHANGE }o--|| USER : "changed_by_user_id"
    ORDER_DISPATCH_OFFER }o--|| USER : "driver_id"
    ORDER_DISPATCH_OFFER }o--|| ORDER : "order_id"
    ORDER_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    ORDER_STATUS_HISTORY }o--o| USER : "changed_by_user_id"
    PAYMENT }o--|| ORDER : "order_id"
    PURCHASE_RECEIPT }o--|| WAREHOUSE : "warehouse_id"
    PURCHASE_RECEIPT }o--|| USER : "received_by_user_id"
    PURCHASE_RECEIPT }o--o| CASH_MOVEMENT : "cash_movement_id"
    PURCHASE_RECEIPT }o--o| USER : "voided_by_user_id"
    RATING }o--o| USER : "hidden_by_user_id"
    RATING }o--|| USER : "to_user_id"
    RATING }o--|| ORDER : "order_id"
    RATING }o--|| USER : "from_user_id"
    REPURCHASE_INVITATION }o--|| USER : "user_id"
    REPURCHASE_INVITATION }o--o| ORDER : "order_id"
    ROUTE_BATCH_OFFER }o--|| DELIVERY : "delivery_id"
    ROUTE_BATCH_STOP }o--|| ORDER : "order_id"
    STOCK_ADJUSTMENT }o--|| USER : "created_by_user_id"
    STOCK_BALANCE }o--|| GAS_CYLINDER : "gas_cylinder_id"
    STOCK_MOVEMENT }o--|| GAS_CYLINDER : "gas_cylinder_id"
    STOCK_MOVEMENT }o--o| USER : "actor_user_id"
    TIRE_EVENT }o--o| CAR : "car_id"
    TIRE_EVENT }o--|| USER : "created_by_user_id"
    TRAFFIC_FINE }o--|| CAR : "car_id"
    TRAFFIC_FINE }o--o| EMPLOYEE : "employee_id"
    TRAFFIC_FINE }o--o| CASH_MOVEMENT : "cash_movement_id"
    TRUCK_LOAD }o--o| EMPLOYEE : "helper_employee_id"
    TRUCK_LOAD }o--|| USER : "opened_by_user_id"
    TRUCK_LOAD }o--o| USER : "closed_by_user_id"
    TRUCK_LOAD }o--|| CAR : "car_id"
    TRUCK_LOAD }o--|| DELIVERY : "delivery_id"
    COMMISSION_ENTRY }o--o| ORDER : "order_id"
    COMMISSION_ENTRY }o--o| DELIVERY : "delivery_id"
    COMMISSION_ENTRY }o--o| USER : "created_by_user_id"
    COMMISSION_ENTRY }o--|| EMPLOYEE : "employee_id"
    CYLINDER_MOVEMENT }o--o| ORDER : "order_id"
    CYLINDER_MOVEMENT }o--o| USER : "actor_user_id"
    CYLINDER_RECOVERY_CASE }o--|| USER : "user_id"
    CYLINDER_RECOVERY_CASE }o--o| USER : "resolved_by_user_id"
    DRIVER_SETTLEMENT }o--o| TRUCK_LOAD : "truck_load_id"
    DRIVER_SETTLEMENT }o--o| USER : "approved_by_user_id"
    DRIVER_SETTLEMENT }o--|| DELIVERY : "delivery_id"
    DRIVER_SETTLEMENT }o--o| USER : "submitted_by_user_id"
    PAYMENT_REFUND }o--|| ORDER : "order_id"
    PAYMENT_REFUND }o--o| USER : "requested_by_user_id"
    PURCHASE_RECEIPT_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    STOCK_ADJUSTMENT_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    TRUCK_LOAD_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    CYLINDER_RECOVERY_NOTICE }o--o| ORDER : "order_id"
    DRIVER_SETTLEMENT_ORDER |o--|| ORDER : "order_id"
```

</details>

#### 7.4.3 Diccionario de Datos

El diccionario completo de las 85 tablas —columna, tipo, obligatoriedad, clave, referencia,
default, descripción, restricciones `CHECK` e índices— acompaña a la documentación como el
archivo `SPLG-modelo-de-datos.md`. La descripción de cada columna se toma del comentario de la
entidad de TypeORM que la define; las columnas sin comentario en el código figuran allí como
«sin descripción documentada en el código» en vez de inventarse una (son 825 de 977).

#### 7.4.4 Tipos enumerados

**79 tipos enumerados**. El detalle de los
valores de cada uno está en la sección «Tipos enumerados» de
`SPLG-modelo-de-datos.md`; acá solo la lista, para no duplicar un dato que cambia con cada
migración:

`address_geocode_precision_enum`, `attachment_owner_type_enum`, `audit_result_enum`, `cash_box_kind_enum`, `cash_category_direction_enum`, `cash_category_system_code_enum`, `cash_movement_direction_enum`, `cash_movement_method_enum`, `cash_movement_reference_type_enum`, `cash_session_status_enum`, `claims_status_enum`, `commission_entry_type_enum`, `commission_rule_basis_enum`, `configurable_process_enum`, `coverage_zone_surcharge_type_enum`, `customer_account_entry_type_enum`, `customer_account_status_enum`, `customer_account_tax_condition_enum`, `cylinder_inspection_result_enum`, `cylinder_movement_from_state_enum`, `cylinder_movement_to_state_enum`, `cylinder_state_enum`, `distributor_status_enum`, `driver_liquidation_status_enum`, `driver_settlement_difference_resolution_enum`, `driver_settlement_status_enum`, `employee_attendance_source_enum`, `employee_document_type_enum`, `employee_leave_status_enum`, `employee_leave_type_enum`, `employee_status_enum`, `employee_termination_reason_enum`, `employment_type_enum`, `fleet_status_enum`, `fuel_payment_method_enum`, `fuel_type_enum`, `incident_moment_enum`, `incident_status_enum`, `incident_type_enum`, `job_position_category_enum`, `maintenance_criticality_enum`, `maintenance_subject_enum`, `maintenance_task_status_enum`, `maintenance_trigger_enum`, `order_delivery_mode_enum`, `order_dispatch_offer_status_enum`, `order_paymentmethod_enum`, `order_paymentstatus_enum`, `order_paymenttype_enum`, `order_status_enum`, `order_zone_surcharge_type_enum`, `payment_gateway_enum`, `payment_integration_enum`, `payment_refund_kind_enum`, `payment_refund_status_enum`, `payment_status_enum`, `plan_document_kind_enum`, `proposal_status_enum`, `purchase_order_status_enum`, `purchase_payment_status_enum`, `purchase_receipt_status_enum`, `rating_from_role_enum`, `recovery_case_status_enum`, `recovery_notice_kind_enum`, `repurchase_invitation_status_enum`, `route_batch_status_enum`, `stock_adjustment_reason_enum`, `stock_condition_enum`, `stock_location_kind_enum`, `stock_movement_reason_enum`, `stock_movement_reference_type_enum`, `supplier_document_type_enum`, `supplier_kind_enum`, `tire_event_type_enum`, `tire_status_enum`, `traffic_fine_status_enum`, `truck_load_status_enum`, `vehicle_accident_status_enum`, `warehouse_kind_enum`.

#### 7.4.5 Multidistribuidora

**61 de las 85 tablas tienen `distributor_id` directo:** todo lo que es catálogo, flota,
despacho o transacción de una distribuidora concreta (`order`, `payment`, `cylinder`,
`gas_cylinder`, `car`, `vehicle_assignment`, `delivery`, `coverage_zone`, `time_slot`,
`claims`, `incident`, `rating`, `admin`, `module_config`, `audit_log`, `audit`, `attachment`, `document_sequence`, las del stock físico (`warehouse`, `stock_location`,
`stock_balance`, `stock_movement`, `stock_adjustment`, `stock_threshold` y `stock_reconciliation_alert`), las de compras (`supplier`, `purchase_order` y `purchase_receipt`), la carga del camión (`truck_load`) y las de flota y
recupero, entre otras).

**24 tablas no tienen `distributor_id` propio**, por tres motivos distintos:

- **Son globales de verdad** (comparten el mismo registro entre distribuidoras):
  `user`, `customer`, `user_address`, `role` y el catálogo `audit_action_type`. Un cliente puede comprarle a varias
  distribuidoras con la misma cuenta y las mismas direcciones; el rol es del sistema, no de
  una empresa. El acotamiento por distribuidora, cuando hace falta, lo resuelve la aplicación
  (`common/tenancy/pertenencia.ts`): para una distribuidora, sus clientes son los que le
  compraron al menos una vez.
- **Son detalle de otra tabla que sí tiene distribuidora** (alcanzan el aislamiento uniéndose a su
  padre, nunca por columna propia): `order_item`, `order_status_history`,
  `order_address_change` (de `order`), `cart_item` (de `cart`), `gas_cylinder_promotion`
  (de `gas_cylinder`), `route_batch_stop`, `route_batch_offer` (de `route_batch`),
  `maintenance_window_proposal` (de `maintenance_task`), `cylinder_recovery_notice` (de
  `cylinder_recovery_case`), `audit_detail` (de `audit`), `stock_adjustment_item` (de `stock_adjustment`), `purchase_order_item` (de `purchase_order`), `purchase_receipt_item` (de `purchase_receipt`) y `truck_load_item` (de `truck_load`), `driver_settlement_order`, `driver_settlement_expense` y `driver_settlement_collection` (de `driver_settlement`) y `customer_account_allocation` (de `customer_account`). El acceso a estas dieciocho tiene que ser siempre por relación
  hacia su padre: consultarlas sueltas, sin ese `JOIN`, es el patrón de bug de aislamiento
  de las consultas sin filtro de distribuidora.
- **Es técnica y no pertenece a ninguna distribuidora:** `storage_orphan`, la cola de archivos pendientes de borrar del almacenamiento; guarda la clave del archivo y no sabe de quién es.

`admin.distributor_id` es la columna de distribuidora **anulable** de un perfil: el
superadministrador (`role.type = 'superadmin'`) no tiene distribuidora. También lo son la de `audit_log` y la de `audit`, que quedan vacías si se borra la distribuidora para conservar el registro; en `audit`, además, lo que es de la persona o global (usuarios, clientes, direcciones, roles) se registra sin distribuidora y solo lo ve el Administrador General.

#### 7.4.6 Decisiones de modelado y deuda técnica documentada

Esto es sobre el **esquema real** de la base, no sobre esta documentación. Son puntos que
un profesor marcaría como mejora del modelo físico; no se tocó el backend para corregirlos
(está fuera del alcance de esta tarea: la base es de solo lectura) y quedan anotados acá
como deuda, con su corrección concreta:

- **Faltan `CHECK` de rango.** `rating.stars` dice «de 1 a 5» en la descripción pero nada
  lo impide en la base (correspondería `CHECK (stars BETWEEN 1 AND 5)`); lo mismo
  `order_item.quantity > 0`, montos `>= 0` y `time_slot."endTime" > "startTime"` con
  `capacity > 0`. Solo hay `CHECK` en `gas_cylinder_promotion` (2), `coverage_zone` (1), `employee` (2), las tablas de stock (`stock_threshold`, `stock_location`, `stock_movement`, `stock_balance` y `stock_adjustment_item`), los renglones de compra (`purchase_order_item` y `purchase_receipt_item`, de cantidades y costos no negativos), `truck_load_item` (2) y las tablas de los módulos de gestión (`employee_attendance`, `employee_leave`, `fuel_load`, `traffic_fine`, `cash_box`, `cash_movement`, `customer_account`, `customer_account_entry`, `customer_account_allocation`, `driver_settlement_expense` y `commission_rule`).
- **Faltan `UNIQUE` de negocio.** `distributor.tax_id` (CUIT) no es único: hay 136
  filas con CUIT y solo 5 valores distintos—, ni `user_address` tiene
  `UNIQUE (user_id) WHERE "isDefault"`, ni `time_slot` tiene
  `UNIQUE (distributor_id, name)`.
- **`car.type_car` es texto libre.** En la base conviven «Camión», «camioneta», «Camioneta»,
  «moto», «Moto», «Utilitario» para lo que el dominio modela como tres valores
  (§1.4 del Documento 2). Correspondería un tipo enumerado o un `CHECK`.
- **Fechas con zona horaria.** Todas las columnas de fecha y hora son `timestamptz`, incluidas `order.acceptedAt`, `order.onTheWayAt`, `order.deliveredAt` y `claims.createdAt`: no queda ninguna `marca de tiempo without time zone`, y no hay deuda en este punto.
- **Montos en punto flotante en vez de `numeric`:** `delivery.balance` (`double precision`)
  y `delivery."cancelledCharge"` (`real`). El resto del esquema usa `numeric(10,2)`.
- **Nombres de columna mezclados** entre `camelCase` (`createdAt`, `isActive`) y
  `snake_case` (`distributor_id`, `zone_name`), que obliga a comillas en SQL crudo. Es el
  de menor impacto de esta lista: no rompe ninguna regla de negocio.
- **Índices duplicados** sobre `distributor.slug` (una `UNIQUE` y un índice simple que ya
  es redundante con ella).

Esta lista es el complemento físico de la normalización (1FN a 5FN): reúne las
restricciones (`CHECK`, `UNIQUE`, tipos) que no son tema de normalización pero sí de
integridad.


#### 7.4.7 Modelo Entidad-Relación Conceptual y Correspondencia con el Modelo Conceptual

El modelo entidad-relación conceptual cuenta lo mismo que el modelo conceptual del Documento 2
con el vocabulario de los datos: **una entidad por concepto que tiene tabla**, con el mismo
nombre y con los mismos atributos, y **una relación por cada asociación** que la base sostiene
con una clave foránea, con el nombre y el sentido de lectura de la asociación. Las
cardinalidades son las que impone la base (ver 7.4.2). La Distribuidora está relacionada con
todos los conceptos que le pertenecen; las demás claves a `distributor` son la pertenencia de
cada fila a su distribuidora y no se dibujan, igual que en el Documento 2.

Varias relaciones salen de Usuario y no de Cliente o de Chofer, porque la clave foránea de la base apunta a `user`: el perfil (cliente, chofer o administrador) y el usuario son la misma persona, y un usuario tiene a lo sumo un perfil de cada clase. Por eso, en las vistas por área, un concepto de perfil que no tiene ninguna relación propia en la vista no se dibuja. Cada entidad lleva su identificador, y los atributos derivados se marcan con `/`.

Tres conceptos no tienen tabla propia: PropuestaConVigencia es abstracto, UbicacionGPS es la
columna `actual_location` de `delivery` e ItemSugerido se guarda como JSON dentro de
`repurchase_invitation`. Los otros 82 conceptos corresponden uno a uno con las 82 tablas de dominio de la base, como muestra la tabla de correspondencia (los módulos de gestión de §7.4.8 ya están construidos). Tres tablas de la base no tienen concepto, porque no son algo del negocio sino mecanismos del sistema, y se dibujan en el modelo físico dentro del contexto «Tablas técnicas»:

- `document_sequence` (Secuencia de documentos): Último número asignado a cada tipo de documento, por distribuidora: un contador para numerar comprobantes correlativos sin repetir ni saltear. Es un mecanismo, no algo del negocio con identidad propia.
- `stock_reconciliation_alert` (Aviso de conciliación de stock): Firma de la última diferencia de conciliación que se avisó a cada distribuidora, para no repetir el correo de la noche siguiente. Es un mecanismo del proceso nocturno, no algo del negocio con identidad propia.
- `storage_orphan` (Archivo pendiente de borrado): Cola de reintento del almacenamiento: la clave de un archivo que se subió o se reemplazó y todavía hay que borrar del almacenamiento externo. Es una tarea de mantenimiento del sistema, no un concepto del dominio.

La correspondencia de las relaciones y de
los atributos también se comprueba contra la base.

| Concepto (Doc 2) | Entidad (DER conceptual) | Tabla (modelo físico) | Observación |
|---|---|---|---|
| Distribuidora | Distribuidora | `distributor` |  |
| Usuario | Usuario | `user` |  |
| Rol | Rol | `role` |  |
| Administrador | Administrador | `admin` |  |
| ConfiguracionModulo | ConfiguracionModulo | `module_config` |  |
| AsientoAuditoria | AsientoAuditoria | `audit_log` |  |
| Auditoria | Auditoria | `audit` | Tipo, usuario, distribuidora, entidad afectada, id del registro, dirección de red y fecha y hora; sin clave foránea al registro afectado, que es polimórfico. |
| DetalleAuditoria | DetalleAuditoria | `audit_detail` |  |
| TipoAccionAuditoria | TipoAccionAuditoria | `audit_action_type` |  |
| Cliente | Cliente | `customer` |  |
| DireccionEntrega | DireccionEntrega | `user_address` | Pertenece al usuario (`user_id`), no al perfil de cliente. |
| InvitacionRecompra | InvitacionRecompra | `repurchase_invitation` |  |
| ItemSugerido | — | — | Sin tabla: las líneas sugeridas se guardan como JSON en `repurchase_invitation.suggested_items`. |
| Producto | Producto | `gas_cylinder` | La base lo llama `gas_cylinder` (tipo de garrafa); el modelo conceptual y los documentos lo llaman Producto, y esa es la única denominación del dominio. |
| Promocion | Promocion | `gas_cylinder_promotion` |  |
| Envase | Envase | `cylinder` |  |
| MovimientoEnvase | MovimientoEnvase | `cylinder_movement` |  |
| RevisionEnvase | RevisionEnvase | `cylinder_inspection` |  |
| CasoRecupero | CasoRecupero | `cylinder_recovery_case` |  |
| AvisoRecupero | AvisoRecupero | `cylinder_recovery_notice` |  |
| Carrito | Carrito | `cart` | Pertenece al usuario (`user_id`), no al perfil de cliente. |
| ItemCarrito | ItemCarrito | `cart_item` |  |
| Pedido | Pedido | `order` |  |
| ItemPedido | ItemPedido | `order_item` |  |
| CambioEstadoPedido | CambioEstadoPedido | `order_status_history` |  |
| CambioDireccion | CambioDireccion | `order_address_change` |  |
| ZonaCobertura | ZonaCobertura | `coverage_zone` |  |
| FranjaHoraria | FranjaHoraria | `time_slot` |  |
| Pago | Pago | `payment` |  |
| ReintegroDePago | ReintegroDePago | `payment_refund` |  |
| PropuestaConVigencia | — | — | Concepto abstracto: sin tabla. Sus atributos `estado` y `vence` están en cada tabla de sus cinco especializaciones. |
| OfertaDespacho | OfertaDespacho | `order_dispatch_offer` |  |
| LoteRecorrido | LoteRecorrido | `route_batch` |  |
| ParadaLote | ParadaLote | `route_batch_stop` |  |
| OfertaLote | OfertaLote | `route_batch_offer` |  |
| Chofer | Chofer | `delivery` | La tabla se llama `delivery` por historia del proyecto. |
| Vehiculo | Vehiculo | `car` | La tabla se llama `car` por historia del proyecto. |
| AsignacionVehiculo | AsignacionVehiculo | `vehicle_assignment` |  |
| PlanMantenimiento | PlanMantenimiento | `maintenance_plan` |  |
| TareaMantenimiento | TareaMantenimiento | `maintenance_task` |  |
| AdjuntoTarea | AdjuntoTarea | `maintenance_task_attachment` |  |
| PropuestaVentanaTaller | PropuestaVentanaTaller | `maintenance_window_proposal` |  |
| UbicacionGPS | — | — | Sin tabla: la posición vigente es la columna `delivery.actual_location`. |
| RegistroUsoVehiculo | RegistroUsoVehiculo | `vehicle_usage_log` |  |
| PuestoDeTrabajo | PuestoDeTrabajo | `job_position` |  |
| Empleado | Empleado | `employee` |  |
| JornadaDeTrabajo | JornadaDeTrabajo | `employee_attendance` | |
| LicenciaLaboral | LicenciaLaboral | `employee_leave` | |
| Adjunto | Adjunto | `attachment` |  |
| CargaCombustible | CargaCombustible | `fuel_load` | |
| MultaTransito | MultaTransito | `traffic_fine` | |
| Siniestro | Siniestro | `vehicle_accident` | |
| Neumatico | Neumatico | `tire` | |
| MovimientoNeumatico | MovimientoNeumatico | `tire_event` | |
| Reclamo | Reclamo | `claims` |  |
| Incidencia | Incidencia | `incident` |  |
| Calificacion | Calificacion | `rating` |  |
| Deposito | Deposito | `warehouse` |  |
| UbicacionDeStock | UbicacionDeStock | `stock_location` |  |
| SaldoDeStock | SaldoDeStock | `stock_balance` |  |
| MovimientoDeStock | MovimientoDeStock | `stock_movement` |  |
| UmbralDeStock | UmbralDeStock | `stock_threshold` |  |
| AjusteDeStock | AjusteDeStock | `stock_adjustment` |  |
| ItemAjusteDeStock | ItemAjusteDeStock | `stock_adjustment_item` |  |
| CargaDeCamion | CargaDeCamion | `truck_load` |  |
| ItemCarga | ItemCarga | `truck_load_item` |  |
| Proveedor | Proveedor | `supplier` |  |
| OrdenDeCompra | OrdenDeCompra | `purchase_order` |  |
| ItemOrdenDeCompra | ItemOrdenDeCompra | `purchase_order_item` |  |
| RecepcionDeCompra | RecepcionDeCompra | `purchase_receipt` |  |
| ItemRecepcion | ItemRecepcion | `purchase_receipt_item` |  |
| Caja | Caja | `cash_box` | |
| SesionDeCaja | SesionDeCaja | `cash_session` | |
| CategoriaDeCaja | CategoriaDeCaja | `cash_category` | |
| MovimientoDeCaja | MovimientoDeCaja | `cash_movement` | |
| RendicionChofer | RendicionChofer | `driver_settlement` | |
| PedidoRendido | PedidoRendido | `driver_settlement_order` | |
| CobroDeRendicion | CobroDeRendicion | `driver_settlement_collection` |  |
| GastoDeRendicion | GastoDeRendicion | `driver_settlement_expense` | |
| CuentaCorriente | CuentaCorriente | `customer_account` | |
| AsientoCuentaCorriente | AsientoCuentaCorriente | `customer_account_entry` | |
| ImputacionCuentaCorriente | ImputacionCuentaCorriente | `customer_account_allocation` | |
| ReglaComision | ReglaComision | `commission_rule` | |
| AsientoComision | AsientoComision | `commission_entry` | |
| LiquidacionComisiones | LiquidacionComisiones | `driver_liquidation` | |

![DER conceptual: vista general](../modelos/base-de-datos/conceptual/SPLG-der-00-general.png)

**Figura 529 — Modelo entidad-relación conceptual: vista general**

![DER conceptual: usuarios y cuentas](../modelos/base-de-datos/conceptual/SPLG-der-01-usuarios-y-cuentas.png)

**Figura 530 — Modelo entidad-relación conceptual: usuarios y cuentas**

![DER conceptual: pedidos y pagos](../modelos/base-de-datos/conceptual/SPLG-der-02-pedidos-y-pagos.png)

**Figura 531 — Modelo entidad-relación conceptual: pedidos y pagos**

![DER conceptual: despacho y propuestas con vigencia](../modelos/base-de-datos/conceptual/SPLG-der-03-despacho-y-propuestas-con-vigencia.png)

**Figura 532 — Modelo entidad-relación conceptual: despacho y propuestas con vigencia**

![DER conceptual: flota y choferes](../modelos/base-de-datos/conceptual/SPLG-der-04-flota-y-choferes.png)

**Figura 533 — Modelo entidad-relación conceptual: flota y choferes**

![DER conceptual: envases y catálogo](../modelos/base-de-datos/conceptual/SPLG-der-05-envases-y-catalogo.png)

**Figura 534 — Modelo entidad-relación conceptual: envases y catálogo**

![DER conceptual: personal](../modelos/base-de-datos/conceptual/SPLG-der-06-personal.png)

**Figura 535 — Modelo entidad-relación conceptual: personal**

![DER conceptual: posventa](../modelos/base-de-datos/conceptual/SPLG-der-07-posventa.png)

**Figura 536 — Modelo entidad-relación conceptual: posventa**

![DER conceptual: gastos de la flota](../modelos/base-de-datos/conceptual/SPLG-der-08-gastos-de-la-flota.png)

**Figura 537 — Modelo entidad-relación conceptual: gastos de la flota**

![DER conceptual: stock físico](../modelos/base-de-datos/conceptual/SPLG-der-09-stock-fisico.png)

**Figura 538 — Modelo entidad-relación conceptual: stock físico**

![DER conceptual: carga del camión](../modelos/base-de-datos/conceptual/SPLG-der-10-carga-del-camion.png)

**Figura 539 — Modelo entidad-relación conceptual: carga del camión**

![DER conceptual: compras](../modelos/base-de-datos/conceptual/SPLG-der-11-compras.png)

**Figura 540 — Modelo entidad-relación conceptual: compras**

![DER conceptual: caja y movimientos](../modelos/base-de-datos/conceptual/SPLG-der-12-caja-y-movimientos.png)

**Figura 541 — Modelo entidad-relación conceptual: caja y movimientos**

![DER conceptual: rendiciones de choferes](../modelos/base-de-datos/conceptual/SPLG-der-13-rendiciones-de-choferes.png)

**Figura 542 — Modelo entidad-relación conceptual: rendiciones de choferes**

![DER conceptual: cuentas corrientes](../modelos/base-de-datos/conceptual/SPLG-der-14-cuentas-corrientes.png)

**Figura 543 — Modelo entidad-relación conceptual: cuentas corrientes**

![DER conceptual: comisiones y liquidaciones](../modelos/base-de-datos/conceptual/SPLG-der-15-comisiones-y-liquidaciones.png)

**Figura 544 — Modelo entidad-relación conceptual: comisiones y liquidaciones**

#### 7.4.8 Tablas de los módulos de gestión de la distribuidora

Las 22 tablas de los módulos de personal, flota ampliada, caja y rendición, y los reintegros de pagos están construidas y figuran en el inventario (§7.4.1), en los diagramas por contexto (§7.4.2) y en el diccionario de datos (§7.4.3). Esta sección dice qué trae cada módulo y qué decisiones de modelado lo sostienen. Lo único que sigue propuesto es el modelo de datos del módulo inteligente M5 (recupero de envases): la columna `cylinder.decommissioned_at` y la columna `cylinder_recovery_notice.order_id`, que se crean con la migración de la iteración C-15 (`modelos/base-de-datos/SPLG-base-de-datos-propuesta.sql`).

Las compras, los combustibles y las multas todavía no generan movimientos de caja: `fuel_load` y `traffic_fine` no tienen columna `cash_movement_id`, y `purchase_receipt.cash_movement_id` no tiene clave foránea declarada. La columna de los pagos de compra existe, pero el egreso de caja de lo que se paga fuera del libro queda para una iteración posterior.

##### 7.4.8.1 Personal y legajos (iteración C-08)

Las cuatro tablas del módulo: `job_position` y `employee` (puestos y legajos, CU-176 a CU-182, CU-186 y CU-255 a CU-257), y `employee_attendance` y `employee_leave` (jornadas y licencias, CU-189 a CU-193 y CU-246).

| Contexto | Tabla | Columnas | Qué guarda |
|---|---|:-:|---|
| Personal | `employee_attendance` | 11 | Una jornada de un empleado: su ingreso y su egreso. |
| Personal | `employee_leave` | 15 | Licencia o ausencia de un empleado, con su período y su estado. |

Además el módulo agregó a `maintenance_plan` el documento que controla y las categorías de puesto a las que aplica, y a `maintenance_task` el empleado dueño (`employee_id`, con `delivery_id` como columna heredada), el inicio de vigencia (`valid_from`) y el detalle (`details`), de modo que el seguro, la licencia de conducir y la habilitación del vehículo se registran como tareas con vencimiento.

![Modelo físico: personal](../modelos/base-de-datos/fisico/SPLG-fisico-09-personal.png)

**Figura 545 — Modelo físico: personal**

![DER conceptual: personal](../modelos/base-de-datos/conceptual/SPLG-der-06-personal.png)

**Figura 546 — Modelo entidad-relación conceptual: personal**

##### 7.4.8.2 Flota ampliada (iteración C-18)

Las tablas de esta sección (CU-195 a CU-206 y CU-247) referencian al legajo del empleado (`employee_id`) del módulo de personal, sin una tabla propia de empleado.

| Contexto | Tabla | Columnas | Qué guarda |
|---|---|:-:|---|
| Gastos de la flota | `fuel_load` | 24 | Una carga de combustible de un vehículo, con su kilometraje y su importe. |
| Gastos de la flota | `traffic_fine` | 21 | Una multa de tránsito de un vehículo, con su ciclo de pendiente a pagada o anulada. |
| Gastos de la flota | `vehicle_accident` | 22 | Un siniestro de un vehículo, de denunciado a cerrado, con sus costos. |
| Gastos de la flota | `tire` | 14 | Un neumático de la distribuidora, en depósito, montado en un vehículo o dado de baja. |
| Gastos de la flota | `tire_event` | 9 | Un movimiento de un neumático; el libro no se modifica. |

**Cambios a la tabla `car`:** `fuel_type` (`fuel_type_enum`, nula), el combustible que usa el vehículo, y
`tank_capacity_liters` (`numeric(6,2)`, nula), la capacidad del tanque.

Tipos enumerados nuevos:

| Tipo | Valores |
|---|---|
| `fuel_type_enum` | `diesel`, `gasoline`, `cng`, `lpg` |
| `fuel_payment_method_enum` | `cash_box`, `driver_cash`, `card`, `fuel_account` |
| `traffic_fine_status_enum` | `pending`, `appealed`, `paid`, `voided` |
| `vehicle_accident_status_enum` | `reported`, `under_review`, `repairing`, `closed` |
| `tire_status_enum` | `in_stock`, `mounted`, `retired` |
| `tire_event_type_enum` | `mount`, `unmount`, `rotate`, `retread`, `retire` |

![Modelo físico: gastos de la flota](../modelos/base-de-datos/fisico/SPLG-fisico-10-gastos-de-la-flota.png)

**Figura 547 — Modelo físico: gastos de la flota**

![DER conceptual: gastos de la flota](../modelos/base-de-datos/conceptual/SPLG-der-08-gastos-de-la-flota.png)

**Figura 548 — Modelo entidad-relación conceptual: gastos de la flota**

**Decisiones de modelado.** (1) La carga, la multa y el siniestro son registros propios del vehículo y no
columnas de `car`: cada uno tiene fecha, importe y ciclo de vida, y alimentan el costo por vehículo.
(2) El siniestro no se mezcla con `incident`, que es el contratiempo de calidad de un pedido. (3) El
empleado se referencia por `employee_id`, no por `delivery`: quien carga combustible o conduce puede ser
un empleado sin cuenta de acceso. (4) Los comprobantes, el acta y las fotos se guardan con el mecanismo de adjuntos
genéricos y no con tablas propias. (5) El acta de una multa es única por distribuidora y jurisdicción,
y el número de serie de un neumático es único por distribuidora: ambas restricciones están en la base.

##### 7.4.8.3 Caja, rendición, cuentas corrientes y comisiones (iteración C-20)

El módulo de caja y rendición agrega **catorce tablas** y los tipos enumerados que las sostienen, más el valor `account` en los dos tipos enumerados del medio de pago del pedido. Los asientos de `cash_movement`, `customer_account_entry` y `commission_entry` solo se agregan: se corrigen con un contraasiento y un disparador rechaza todo `UPDATE` y todo `DELETE`.

| Contexto | Tabla | Concepto | Qué guarda |
|---|---|---|---|
| Caja y finanzas | `cash_box` | Caja | Cuenta de fondos de la distribuidora —efectivo, banco o billetera— con su saldo. |
| Caja y finanzas | `cash_session` | SesionDeCaja | Período de trabajo de una caja entre una apertura y un cierre con arqueo. |
| Caja y finanzas | `cash_category` | CategoriaDeCaja | Clasificación de los ingresos y de los gastos de caja, propia o de sistema. |
| Caja y finanzas | `cash_movement` | MovimientoDeCaja | Asiento inmutable del libro de una caja: una entrada o una salida de dinero. |
| Caja y finanzas | `driver_settlement` | RendicionChofer | Rendición diaria del efectivo que cobró un chofer, con lo esperado, lo declarado y la diferencia. |
| Caja y finanzas | `driver_settlement_order` | PedidoRendido | Pedido cobrado en efectivo que integra una rendición; un pedido se rinde una sola vez. |
| Caja y finanzas | `driver_settlement_expense` | GastoDeRendicion | Gasto que el chofer pagó con la cobranza y declara al rendir. |
| Caja y finanzas | `driver_settlement_collection` | CobroDeRendicion | Cobro de cuenta corriente que el chofer recibió en la calle y rinde con el efectivo; cada asiento se rinde una sola vez. |
| Caja y finanzas | `customer_account` | CuentaCorriente | Cuenta de un cliente en una distribuidora, con su límite de crédito, su plazo de pago y su saldo. |
| Caja y finanzas | `customer_account_entry` | AsientoCuentaCorriente | Asiento inmutable del libro de una cuenta corriente: cargo, pago, nota de crédito o de débito. |
| Caja y finanzas | `customer_account_allocation` | ImputacionCuentaCorriente | Aplicación de un pago o una nota de crédito a un cargo, por orden de antigüedad. |
| Caja y finanzas | `commission_rule` | ReglaComision | Regla que dice cuánto gana un chofer por entrega, con su alcance y su vigencia. |
| Caja y finanzas | `commission_entry` | AsientoComision | Asiento inmutable del libro de comisiones de un chofer: una comisión o una deducción. |
| Caja y finanzas | `driver_liquidation` | LiquidacionComisiones | Liquidación de las comisiones y las deducciones de un chofer en un período, con su neto a pagar. |

A estas se suma `payment_refund` (ReintegroDePago), del contexto «Pagos»: la devolución de un pago a través de la pasarela, con sus reintentos.

![Modelo físico: caja y finanzas](../modelos/base-de-datos/fisico/SPLG-fisico-14-caja-y-finanzas.png)

**Figura 549 — Modelo físico: caja y finanzas**

![DER conceptual: caja y movimientos](../modelos/base-de-datos/conceptual/SPLG-der-12-caja-y-movimientos.png)

**Figura 550 — Modelo entidad-relación conceptual: caja y movimientos**

![DER conceptual: rendiciones de choferes](../modelos/base-de-datos/conceptual/SPLG-der-13-rendiciones-de-choferes.png)

**Figura 551 — Modelo entidad-relación conceptual: rendiciones de choferes**

![DER conceptual: cuentas corrientes](../modelos/base-de-datos/conceptual/SPLG-der-14-cuentas-corrientes.png)

**Figura 552 — Modelo entidad-relación conceptual: cuentas corrientes**

![DER conceptual: comisiones y liquidaciones](../modelos/base-de-datos/conceptual/SPLG-der-15-comisiones-y-liquidaciones.png)

**Figura 553 — Modelo entidad-relación conceptual: comisiones y liquidaciones**
