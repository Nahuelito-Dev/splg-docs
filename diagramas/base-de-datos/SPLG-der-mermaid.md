# DER de SPLG, en Mermaid — generado

Generado por `generar-modelo-datos.py` desde la base en ejecución: 40 tablas, 93 relaciones. Se pega tal cual en `3-Diseño.md` §7.4.2 (los `.md` son la fuente; esto se corre de nuevo y se vuelve a pegar si la base cambia). Cada lámina es un `erDiagram` válido por separado (uno por contexto de negocio) más una lámina final con las relaciones que cruzan de un contexto a otro.

### Organización y acceso

```mermaid
erDiagram
    USER }o--o| ROLE : "role_id"
    ADMIN }o--o| DISTRIBUTOR : "distributor_id"
    ADMIN |o--|| USER : "user_id"
    AUDIT_LOG }o--o| USER : "actor_user_id"
    AUDIT_LOG }o--o| DISTRIBUTOR : "distributor_id"
    MODULE_CONFIG }o--|| DISTRIBUTOR : "distributor_id"
    MODULE_CONFIG }o--o| USER : "updated_by_user_id"

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
    }
    ROLE {
        uuid role_id PK
        text type UK
        timestamptz createdAt "nullable"
        timestamptz updatedAt "nullable"
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
    }
    ADMIN {
        uuid admin_id PK
        uuid distributor_id FK "nullable"
        uuid user_id FK, UK
        timestamptz createdAt
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
```

### Clientes

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

### Catálogo e inventario de envases

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
    }
    GAS_CYLINDER_PROMOTION {
        uuid promotion_id PK
        uuid gas_cylinder_id FK
        int quantity
        decimal discount_percentage
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

### Venta y pedidos

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
        timestamp acceptedAt "nullable"
        timestamp onTheWayAt "nullable"
        timestamp deliveredAt "nullable"
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
        uuid vehicle_car_id "nullable"
        varchar vehicle_patent "nullable"
        varchar vehicle_brand "nullable"
        varchar vehicle_model "nullable"
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

### Pagos

```mermaid
erDiagram

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
```

### Despacho y logística

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

### Flota y choferes

```mermaid
erDiagram
    MAINTENANCE_TASK }o--o| CAR : "car_id"
    MAINTENANCE_TASK }o--o| DELIVERY : "delivery_id"
    MAINTENANCE_TASK }o--|| MAINTENANCE_PLAN : "plan_id"
    VEHICLE_ASSIGNMENT }o--|| CAR : "car_id"
    VEHICLE_ASSIGNMENT }o--|| DELIVERY : "delivery_id"
    VEHICLE_USAGE_LOG }o--|| CAR : "car_id"
    MAINTENANCE_TASK_ATTACHMENT }o--|| MAINTENANCE_TASK : "task_id"
    MAINTENANCE_WINDOW_PROPOSAL }o--|| DELIVERY : "delivery_id"
    MAINTENANCE_WINDOW_PROPOSAL }o--|| MAINTENANCE_TASK : "task_id"

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
        float balance
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

### Posventa

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
        timestamp createdAt
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
    }
```

### Relaciones entre contextos

Las que cruzan de un contexto a otro (ya sin repetir la entidad completa; sus columnas están en la lámina de su propio contexto). La relación con `distributor` se omite acá también por lo mismo que en el conceptual: prácticamente todo pertenece a una distribuidora.

```mermaid
erDiagram
    CAR }o--|| USER : "user_id"
    CART }o--|| USER : "user_id"
    CUSTOMER }o--o| GAS_CYLINDER : "declared_cylinder_type_id"
    CUSTOMER |o--|| USER : "user_id"
    DELIVERY |o--|| USER : "user_id"
    USER_ADDRESS }o--|| USER : "user_id"
    CART_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    ORDER }o--|| USER_ADDRESS : "address_id"
    ORDER }o--|| USER : "customer_id"
    ORDER }o--o| DELIVERY : "delivery_id"
    ROUTE_BATCH }o--o| DELIVERY : "delivery_id"
    VEHICLE_ASSIGNMENT }o--o| USER : "assigned_by_user_id"
    VEHICLE_ASSIGNMENT }o--o| USER : "released_by_user_id"
    CLAIMS }o--|| USER : "customer_id"
    CLAIMS }o--|| ORDER : "order_id"
    CYLINDER }o--o| USER : "current_customer_id"
    CYLINDER }o--o| ORDER : "current_order_id"
    INCIDENT }o--|| ORDER : "order_id"
    INCIDENT }o--|| USER : "reported_by"
    MAINTENANCE_TASK_ATTACHMENT }o--|| USER : "uploaded_by_user_id"
    ORDER_ADDRESS_CHANGE }o--|| USER : "changed_by_user_id"
    ORDER_ADDRESS_CHANGE }o--|| USER_ADDRESS : "from_address_id"
    ORDER_ADDRESS_CHANGE }o--|| USER_ADDRESS : "to_address_id"
    ORDER_DISPATCH_OFFER }o--|| USER : "driver_id"
    ORDER_DISPATCH_OFFER }o--|| ORDER : "order_id"
    ORDER_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    ORDER_STATUS_HISTORY }o--o| USER : "changed_by_user_id"
    PAYMENT }o--|| ORDER : "order_id"
    RATING }o--|| USER : "from_user_id"
    RATING }o--|| ORDER : "order_id"
    RATING }o--|| USER : "to_user_id"
    REPURCHASE_INVITATION }o--o| ORDER : "order_id"
    REPURCHASE_INVITATION }o--|| USER : "user_id"
    ROUTE_BATCH_OFFER }o--|| DELIVERY : "delivery_id"
    ROUTE_BATCH_STOP }o--|| ORDER : "order_id"
    CYLINDER_MOVEMENT }o--o| USER : "actor_user_id"
    CYLINDER_MOVEMENT }o--o| ORDER : "order_id"
    CYLINDER_RECOVERY_CASE }o--o| USER : "resolved_by_user_id"
    CYLINDER_RECOVERY_CASE }o--|| USER : "user_id"
```
