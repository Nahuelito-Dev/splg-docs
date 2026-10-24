# DER de SPLG, en Mermaid — generado

Generado por `generar-modelo-datos.py` desde la base en ejecución: 85 tablas, 230 relaciones. Se pega tal cual en `3-Diseño.md` §7.4.2 (los `.md` son la fuente; esto se corre de nuevo y se vuelve a pegar si la base cambia). Cada lámina es un `erDiagram` válido por separado (uno por contexto de negocio) más una lámina final con las relaciones que cruzan de un contexto a otro.

### Organización y acceso

```mermaid
erDiagram
    USER }o--o| ROLE : "role_id"
    ADMIN }o--o| DISTRIBUTOR : "distributor_id"
    ADMIN |o--|| USER : "user_id"
    AUDIT }o--|| AUDIT_ACTION_TYPE : "action_type_id"
    AUDIT }o--o| DISTRIBUTOR : "distributor_id"
    AUDIT }o--o| USER : "user_id"
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
        uuid vehicle_car_id "nullable"
        varchar vehicle_patent "nullable"
        varchar vehicle_brand "nullable"
        varchar vehicle_model "nullable"
        timestamptz payment_confirmed_at "nullable"
        uuid payment_confirmed_by "nullable"
        text payment_resolution_note "nullable"
        timestamptz payment_resolved_at "nullable"
        uuid payment_resolved_by "nullable"
        decimal express_surcharge_amount
        timestamptz express_degraded_at "nullable"
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
        uuid requested_by_user_id "nullable"
        timestamptz createdAt
        timestamptz updatedAt
        decimal refunded_baseline "nullable"
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

### Personal

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

### Gastos de la flota

```mermaid
erDiagram
    TIRE_EVENT }o--|| TIRE : "tire_id"

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
    }
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
```

### Stock físico y carga del camión

```mermaid
erDiagram
    STOCK_THRESHOLD }o--|| WAREHOUSE : "warehouse_id"
    STOCK_LOCATION |o--o| WAREHOUSE : "warehouse_id"
    STOCK_ADJUSTMENT }o--|| STOCK_LOCATION : "location_id"
    STOCK_BALANCE }o--|| STOCK_LOCATION : "location_id"
    STOCK_MOVEMENT }o--o| STOCK_LOCATION : "from_location_id"
    STOCK_MOVEMENT }o--o| STOCK_MOVEMENT : "reversed_movement_id"
    STOCK_MOVEMENT }o--o| STOCK_LOCATION : "to_location_id"
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

### Compras

```mermaid
erDiagram
    PURCHASE_ORDER }o--|| SUPPLIER : "supplier_id"
    PURCHASE_ORDER_ITEM }o--|| PURCHASE_ORDER : "purchase_order_id"
    PURCHASE_RECEIPT }o--o| PURCHASE_ORDER : "purchase_order_id"
    PURCHASE_RECEIPT }o--|| SUPPLIER : "supplier_id"
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
        uuid cash_movement_id "nullable"
        enum status
        text void_reason "nullable"
        timestamptz voided_at "nullable"
        uuid voided_by_user_id "nullable"
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

### Tablas técnicas

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

### Caja y finanzas

```mermaid
erDiagram
    CASH_SESSION }o--|| CASH_BOX : "cash_box_id"
    CASH_MOVEMENT }o--|| CASH_BOX : "cash_box_id"
    CASH_MOVEMENT }o--|| CASH_CATEGORY : "category_id"
    CASH_MOVEMENT }o--o| CASH_MOVEMENT : "reverses_movement_id"
    CASH_MOVEMENT }o--o| CASH_SESSION : "session_id"
    CUSTOMER_ACCOUNT_ENTRY }o--|| CUSTOMER_ACCOUNT : "account_id"
    CUSTOMER_ACCOUNT_ENTRY }o--o| CASH_MOVEMENT : "cash_movement_id"
    DRIVER_LIQUIDATION }o--o| CASH_MOVEMENT : "cash_movement_id"
    COMMISSION_ENTRY }o--o| DRIVER_LIQUIDATION : "liquidation_id"
    COMMISSION_ENTRY }o--o| COMMISSION_RULE : "rule_id"
    CUSTOMER_ACCOUNT_ALLOCATION }o--|| CUSTOMER_ACCOUNT : "account_id"
    CUSTOMER_ACCOUNT_ALLOCATION }o--|| CUSTOMER_ACCOUNT_ENTRY : "credit_entry_id"
    CUSTOMER_ACCOUNT_ALLOCATION }o--|| CUSTOMER_ACCOUNT_ENTRY : "debit_entry_id"
    DRIVER_SETTLEMENT }o--o| CASH_MOVEMENT : "cash_movement_id"
    DRIVER_SETTLEMENT }o--o| CASH_BOX : "destination_cash_box_id"
    DRIVER_SETTLEMENT_COLLECTION |o--|| CUSTOMER_ACCOUNT_ENTRY : "entry_id"
    DRIVER_SETTLEMENT_COLLECTION }o--|| DRIVER_SETTLEMENT : "settlement_id"
    DRIVER_SETTLEMENT_EXPENSE }o--|| CASH_CATEGORY : "category_id"
    DRIVER_SETTLEMENT_EXPENSE }o--|| DRIVER_SETTLEMENT : "settlement_id"
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

### Relaciones entre contextos

Las que cruzan de un contexto a otro (ya sin repetir la entidad completa; sus columnas están en la lámina de su propio contexto). La relación con `distributor` se omite acá también por lo mismo que en el conceptual: prácticamente todo pertenece a una distribuidora.

```mermaid
erDiagram
    ATTACHMENT }o--|| USER : "uploaded_by_user_id"
    CAR }o--|| USER : "user_id"
    CART }o--|| USER : "user_id"
    CASH_SESSION }o--o| USER : "closed_by_user_id"
    CASH_SESSION }o--|| USER : "opened_by_user_id"
    CUSTOMER }o--o| GAS_CYLINDER : "declared_cylinder_type_id"
    CUSTOMER |o--|| USER : "user_id"
    CUSTOMER_ACCOUNT }o--|| USER : "customer_user_id"
    DELIVERY |o--|| USER : "user_id"
    EMPLOYEE }o--o| USER : "user_id"
    PURCHASE_ORDER }o--|| USER : "created_by_user_id"
    PURCHASE_ORDER }o--|| WAREHOUSE : "destination_warehouse_id"
    STOCK_THRESHOLD }o--|| GAS_CYLINDER : "gas_cylinder_id"
    USER_ADDRESS }o--|| USER : "user_id"
    CART_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    CASH_MOVEMENT }o--|| USER : "created_by_user_id"
    COMMISSION_RULE }o--o| EMPLOYEE : "employee_id"
    COMMISSION_RULE }o--o| GAS_CYLINDER : "gas_cylinder_id"
    EMPLOYEE_ATTENDANCE }o--o| USER : "recorded_by_user_id"
    EMPLOYEE_LEAVE }o--o| USER : "decided_by_user_id"
    EMPLOYEE_LEAVE }o--o| USER : "requested_by_user_id"
    FUEL_LOAD }o--|| CAR : "car_id"
    FUEL_LOAD }o--|| USER : "created_by_user_id"
    FUEL_LOAD }o--o| EMPLOYEE : "employee_id"
    MAINTENANCE_TASK }o--o| EMPLOYEE : "employee_id"
    ORDER }o--|| USER_ADDRESS : "address_id"
    ORDER }o--|| USER : "customer_id"
    ORDER }o--o| DELIVERY : "delivery_id"
    PURCHASE_ORDER_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    PURCHASE_RECEIPT }o--|| USER : "received_by_user_id"
    PURCHASE_RECEIPT }o--|| WAREHOUSE : "warehouse_id"
    ROUTE_BATCH }o--o| DELIVERY : "delivery_id"
    STOCK_LOCATION |o--o| CAR : "car_id"
    TIRE }o--o| CAR : "car_id"
    TRAFFIC_FINE }o--|| CAR : "car_id"
    TRAFFIC_FINE }o--o| EMPLOYEE : "employee_id"
    VEHICLE_ACCIDENT }o--|| CAR : "car_id"
    VEHICLE_ACCIDENT }o--|| USER : "created_by_user_id"
    VEHICLE_ACCIDENT }o--o| EMPLOYEE : "employee_id"
    VEHICLE_ASSIGNMENT }o--o| USER : "assigned_by_user_id"
    VEHICLE_ASSIGNMENT }o--o| USER : "released_by_user_id"
    CLAIMS }o--|| USER : "customer_id"
    CLAIMS }o--|| ORDER : "order_id"
    CUSTOMER_ACCOUNT_ENTRY }o--o| DELIVERY : "collected_by_delivery_id"
    CUSTOMER_ACCOUNT_ENTRY }o--o| USER : "created_by_user_id"
    CUSTOMER_ACCOUNT_ENTRY }o--o| ORDER : "order_id"
    CYLINDER }o--o| USER : "current_customer_id"
    CYLINDER }o--o| ORDER : "current_order_id"
    DRIVER_LIQUIDATION }o--o| USER : "approved_by_user_id"
    DRIVER_LIQUIDATION }o--|| USER : "created_by_user_id"
    DRIVER_LIQUIDATION }o--|| EMPLOYEE : "employee_id"
    DRIVER_LIQUIDATION }o--o| USER : "paid_by_user_id"
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
    PURCHASE_RECEIPT_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    RATING }o--|| USER : "from_user_id"
    RATING }o--o| USER : "hidden_by_user_id"
    RATING }o--|| ORDER : "order_id"
    RATING }o--|| USER : "to_user_id"
    REPURCHASE_INVITATION }o--o| ORDER : "order_id"
    REPURCHASE_INVITATION }o--|| USER : "user_id"
    ROUTE_BATCH_OFFER }o--|| DELIVERY : "delivery_id"
    ROUTE_BATCH_STOP }o--|| ORDER : "order_id"
    STOCK_ADJUSTMENT }o--|| USER : "created_by_user_id"
    STOCK_BALANCE }o--|| GAS_CYLINDER : "gas_cylinder_id"
    STOCK_MOVEMENT }o--o| USER : "actor_user_id"
    STOCK_MOVEMENT }o--|| GAS_CYLINDER : "gas_cylinder_id"
    TIRE_EVENT }o--o| CAR : "car_id"
    TIRE_EVENT }o--|| USER : "created_by_user_id"
    TRUCK_LOAD }o--|| CAR : "car_id"
    TRUCK_LOAD }o--o| USER : "closed_by_user_id"
    TRUCK_LOAD }o--|| DELIVERY : "delivery_id"
    TRUCK_LOAD }o--o| EMPLOYEE : "helper_employee_id"
    TRUCK_LOAD }o--|| USER : "opened_by_user_id"
    COMMISSION_ENTRY }o--o| USER : "created_by_user_id"
    COMMISSION_ENTRY }o--o| DELIVERY : "delivery_id"
    COMMISSION_ENTRY }o--|| EMPLOYEE : "employee_id"
    COMMISSION_ENTRY }o--o| ORDER : "order_id"
    CYLINDER_MOVEMENT }o--o| USER : "actor_user_id"
    CYLINDER_MOVEMENT }o--o| ORDER : "order_id"
    CYLINDER_RECOVERY_CASE }o--o| USER : "resolved_by_user_id"
    CYLINDER_RECOVERY_CASE }o--|| USER : "user_id"
    DRIVER_SETTLEMENT }o--o| USER : "approved_by_user_id"
    DRIVER_SETTLEMENT }o--|| DELIVERY : "delivery_id"
    DRIVER_SETTLEMENT }o--o| USER : "submitted_by_user_id"
    DRIVER_SETTLEMENT }o--o| TRUCK_LOAD : "truck_load_id"
    PAYMENT_REFUND }o--|| ORDER : "order_id"
    STOCK_ADJUSTMENT_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    TRUCK_LOAD_ITEM }o--|| GAS_CYLINDER : "gas_cylinder_id"
    CYLINDER_RECOVERY_NOTICE }o--o| ORDER : "order_id"
    DRIVER_SETTLEMENT_ORDER |o--|| ORDER : "order_id"
```
