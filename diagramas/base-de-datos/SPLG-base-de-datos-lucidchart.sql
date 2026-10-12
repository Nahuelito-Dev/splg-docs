-- Esquema de SPLG — Sistema de Pedidos y Logística de Garrafas de Gas
-- Estado actual de la base: 61 tablas, 141 claves foráneas.
-- Generado por generar-modelo-datos.py
-- Los tipos enumerados y los geográficos de PostGIS se escriben como varchar para
-- que cualquier herramienta de diagramación pueda leer el archivo.
-- Las tablas van en orden de dependencia: se puede ejecutar de corrido.

CREATE TABLE "audit_action_type" (
  "action_type_id" smallint NOT NULL,
  "name" varchar(40) NOT NULL,
  PRIMARY KEY ("action_type_id"),
  UNIQUE ("name")
);

CREATE TABLE "distributor" (
  "distributor_id" uuid NOT NULL,
  "name" varchar(120) NOT NULL,
  "slug" varchar(60) NOT NULL,
  "legal_name" varchar(160),
  "tax_id" varchar(20),
  "email" varchar,
  "phone" varchar,
  "logo_url" varchar,
  "status" varchar(32) NOT NULL,
  "plan" varchar,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  "logo_key" varchar(512),
  PRIMARY KEY ("distributor_id"),
  UNIQUE ("slug")
);

CREATE TABLE "role" (
  "role_id" uuid NOT NULL,
  "type" text NOT NULL,
  "createdAt" timestamptz,
  "updatedAt" timestamptz,
  "deletedAt" timestamptz,
  PRIMARY KEY ("role_id")
);

CREATE TABLE "storage_orphan" (
  "orphan_id" uuid NOT NULL,
  "storage_key" varchar(512) NOT NULL,
  "attempts" integer NOT NULL,
  "last_error" text,
  "created_at" timestamptz NOT NULL,
  "updated_at" timestamptz NOT NULL,
  "kind" varchar(10) NOT NULL,
  "status" varchar(10) NOT NULL,
  "next_attempt_at" timestamptz NOT NULL,
  PRIMARY KEY ("orphan_id"),
  UNIQUE ("storage_key")
);

CREATE TABLE "coverage_zone" (
  "coverage_zone_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "name" varchar(120) NOT NULL,
  "area" varchar(255) NOT NULL,
  "surcharge_value" numeric(10,2) NOT NULL,
  "isActive" boolean NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  "surcharge_type" varchar(32) NOT NULL,
  "label" varchar(40),
  "color" varchar(7),
  "valid_until" timestamptz,
  "priority" integer NOT NULL,
  "valid_from" timestamptz,
  PRIMARY KEY ("coverage_zone_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "document_sequence" (
  "distributor_id" uuid NOT NULL,
  "doc_type" varchar(40) NOT NULL,
  "last_number" integer NOT NULL,
  PRIMARY KEY ("distributor_id", "doc_type"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "gas_cylinder" (
  "gas_cylinder_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "type" varchar(50) NOT NULL,
  "weight" numeric(10,2) NOT NULL,
  "price" numeric(10,2) NOT NULL,
  "stock" integer NOT NULL,
  "description" text,
  "isActive" boolean NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "photo_key" varchar(512),
  "average_unit_cost" numeric(12,2),
  PRIMARY KEY ("gas_cylinder_id"),
  UNIQUE ("distributor_id", "type"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id")
);

CREATE TABLE "job_position" (
  "position_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "name" varchar(80) NOT NULL,
  "category" varchar(32) NOT NULL,
  "is_active" boolean NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  PRIMARY KEY ("position_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "maintenance_plan" (
  "plan_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "name" varchar(120) NOT NULL,
  "subject" varchar(32) NOT NULL,
  "trigger" varchar(32) NOT NULL,
  "interval_km" integer,
  "interval_months" integer,
  "lead_time_days" integer NOT NULL,
  "criticality" varchar(32) NOT NULL,
  "car_type" varchar,
  "is_active" boolean NOT NULL,
  PRIMARY KEY ("plan_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "stock_reconciliation_alert" (
  "distributor_id" uuid NOT NULL,
  "signature" varchar(64) NOT NULL,
  "alerted_at" timestamptz NOT NULL,
  PRIMARY KEY ("distributor_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "supplier" (
  "supplier_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "business_name" varchar(120) NOT NULL,
  "cuit" varchar(11) NOT NULL,
  "kind" varchar(32) NOT NULL,
  "contact_name" varchar(80),
  "phone" varchar(30),
  "email" varchar(120),
  "address" text,
  "payment_terms_days" integer,
  "is_active" boolean NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  PRIMARY KEY ("supplier_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "time_slot" (
  "time_slot_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "name" varchar(50) NOT NULL,
  "startTime" time NOT NULL,
  "endTime" time NOT NULL,
  "capacity" integer NOT NULL,
  "isActive" boolean NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  PRIMARY KEY ("time_slot_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id")
);

CREATE TABLE "user" (
  "user_id" uuid NOT NULL,
  "role_id" uuid,
  "firebase_uid" varchar,
  "full_name" varchar,
  "selfie" varchar,
  "email" varchar,
  "phone_number" varchar,
  "phone_verified" boolean NOT NULL,
  "email_verified" boolean NOT NULL,
  "blocked" boolean NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  "photo_key" varchar(512),
  PRIMARY KEY ("user_id"),
  UNIQUE ("phone_number"),
  UNIQUE ("firebase_uid"),
  UNIQUE ("email"),
  FOREIGN KEY ("role_id") REFERENCES "role" ("role_id")
);

CREATE TABLE "warehouse" (
  "warehouse_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "name" varchar(80) NOT NULL,
  "code" varchar(12) NOT NULL,
  "kind" varchar(32) NOT NULL,
  "address" text,
  "is_default" boolean NOT NULL,
  "is_active" boolean NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  PRIMARY KEY ("warehouse_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "admin" (
  "admin_id" uuid NOT NULL,
  "distributor_id" uuid,
  "user_id" uuid NOT NULL,
  "createdAt" timestamptz NOT NULL,
  PRIMARY KEY ("admin_id"),
  UNIQUE ("user_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "attachment" (
  "attachment_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "owner_type" varchar(32) NOT NULL,
  "owner_id" uuid NOT NULL,
  "label" varchar(80),
  "storage_key" varchar(255) NOT NULL,
  "original_name" varchar(255) NOT NULL,
  "mime_type" varchar(100) NOT NULL,
  "size_bytes" integer NOT NULL,
  "uploaded_by_user_id" uuid NOT NULL,
  "uploaded_at" timestamptz NOT NULL,
  "deleted_at" timestamptz,
  PRIMARY KEY ("attachment_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("uploaded_by_user_id") REFERENCES "user" ("user_id")
);

CREATE TABLE "audit" (
  "audit_id" uuid NOT NULL,
  "action_type_id" smallint NOT NULL,
  "user_id" uuid,
  "distributor_id" uuid,
  "entity" varchar(60) NOT NULL,
  "record_id" varchar(64) NOT NULL,
  "ip" varchar(45),
  "created_at" timestamptz NOT NULL,
  PRIMARY KEY ("audit_id"),
  FOREIGN KEY ("action_type_id") REFERENCES "audit_action_type" ("action_type_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE SET NULL,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL
);

CREATE TABLE "audit_log" (
  "audit_id" uuid NOT NULL,
  "distributor_id" uuid,
  "actor_user_id" uuid,
  "actor_role" varchar(30),
  "http_method" varchar(10) NOT NULL,
  "resource" varchar(60) NOT NULL,
  "resource_id" varchar(64),
  "path" varchar(255) NOT NULL,
  "client_source" varchar(30),
  "ip" varchar(45),
  "result" varchar(32) NOT NULL,
  "status_code" integer NOT NULL,
  "changes" jsonb,
  "error_message" text,
  "created_at" timestamptz NOT NULL,
  PRIMARY KEY ("audit_id"),
  FOREIGN KEY ("actor_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE SET NULL
);

CREATE TABLE "car" (
  "car_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "type_car" varchar(50),
  "car_capacity" integer,
  "car_patent" varchar(20),
  "car_brand" varchar(50),
  "car_model" varchar(50),
  "car_year" integer,
  "car_color" varchar(50),
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  "tare_weight_kg" numeric(10,2),
  "max_load_kg" numeric(10,2),
  "odometer_km" integer,
  "fleet_status" varchar(32) NOT NULL,
  "in_service_since" timestamptz,
  "photo_key" varchar(512),
  PRIMARY KEY ("car_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "cart" (
  "cart_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "updated_at" timestamptz NOT NULL,
  PRIMARY KEY ("cart_id"),
  UNIQUE ("user_id", "distributor_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "customer" (
  "customer_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "notification_token" text,
  "createdAt" timestamptz,
  "deletedAt" timestamptz,
  "location" varchar(255),
  "avg_monthly_consumption_kg" numeric(10,2),
  "declared_cylinder_type_id" uuid,
  "repurchase_notice_days" integer,
  "next_repurchase_estimate_at" timestamptz,
  PRIMARY KEY ("customer_id"),
  UNIQUE ("user_id"),
  FOREIGN KEY ("declared_cylinder_type_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE SET NULL,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "delivery" (
  "delivery_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "calification" double precision,
  "actual_location" text,
  "cancelledCharge" real,
  "validated" boolean NOT NULL,
  "isActive" boolean NOT NULL,
  "notification_token" text,
  "balance" double precision NOT NULL,
  "createdAt" timestamptz,
  "deletedAt" timestamptz,
  "location" varchar(255),
  "isEnabled" boolean NOT NULL,
  "isAvailable" boolean NOT NULL,
  PRIMARY KEY ("delivery_id"),
  UNIQUE ("user_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "employee" (
  "employee_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "user_id" uuid,
  "position_id" uuid NOT NULL,
  "file_number" varchar(20) NOT NULL,
  "first_name" varchar(80) NOT NULL,
  "last_name" varchar(80) NOT NULL,
  "document_type" varchar(32) NOT NULL,
  "document_number" varchar(20) NOT NULL,
  "cuil" varchar(11),
  "birth_date" date,
  "address_line" varchar(200),
  "city" varchar(80),
  "province" varchar(80),
  "postal_code" varchar(10),
  "phone" varchar(30),
  "personal_email" varchar(120),
  "emergency_contact_name" varchar(120),
  "emergency_contact_phone" varchar(30),
  "emergency_contact_relationship" varchar(40),
  "hire_date" date NOT NULL,
  "termination_date" date,
  "termination_reason" varchar(32),
  "employment_type" varchar(32) NOT NULL,
  "status" varchar(32) NOT NULL,
  "bank_cbu" varchar(22),
  "notes" text,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  "photo_key" varchar(512),
  PRIMARY KEY ("employee_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("position_id") REFERENCES "job_position" ("position_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id")
);

CREATE TABLE "gas_cylinder_promotion" (
  "promotion_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "quantity" integer NOT NULL,
  "discount_percentage" numeric(5,2) NOT NULL,
  "deletedAt" timestamptz,
  PRIMARY KEY ("promotion_id"),
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE CASCADE
);

CREATE TABLE "module_config" (
  "config_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "module" varchar(32) NOT NULL,
  "params" jsonb NOT NULL,
  "updated_at" timestamptz NOT NULL,
  "updated_by_user_id" uuid,
  PRIMARY KEY ("config_id"),
  UNIQUE ("distributor_id", "module"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("updated_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL
);

CREATE TABLE "purchase_order" (
  "purchase_order_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "number" integer NOT NULL,
  "supplier_id" uuid NOT NULL,
  "destination_warehouse_id" uuid NOT NULL,
  "status" varchar(32) NOT NULL,
  "issued_at" timestamptz,
  "expected_date" date,
  "total_amount" numeric(12,2) NOT NULL,
  "cancel_reason" text,
  "notes" text,
  "created_by_user_id" uuid NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "close_reason" text,
  PRIMARY KEY ("purchase_order_id"),
  UNIQUE ("distributor_id", "number"),
  FOREIGN KEY ("created_by_user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("destination_warehouse_id") REFERENCES "warehouse" ("warehouse_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("supplier_id") REFERENCES "supplier" ("supplier_id")
);

CREATE TABLE "stock_threshold" (
  "threshold_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "warehouse_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "min_full" integer NOT NULL,
  "alerted_at" timestamptz,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  PRIMARY KEY ("threshold_id"),
  UNIQUE ("warehouse_id", "gas_cylinder_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id"),
  FOREIGN KEY ("warehouse_id") REFERENCES "warehouse" ("warehouse_id")
);

CREATE TABLE "user_address" (
  "address_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "street" varchar(255) NOT NULL,
  "city" varchar(100) NOT NULL,
  "postalCode" varchar(20),
  "formattedAddress" text,
  "isDefault" boolean NOT NULL,
  "additionalInstructions" text,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  "floor" varchar(10),
  "apartment" varchar(10),
  "location" varchar(255),
  "place_id" varchar(255),
  "geocode_precision" varchar(32) NOT NULL,
  PRIMARY KEY ("address_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "audit_detail" (
  "audit_detail_id" uuid NOT NULL,
  "audit_id" uuid NOT NULL,
  "field" varchar(80) NOT NULL,
  "old_value" text,
  "new_value" text,
  PRIMARY KEY ("audit_detail_id"),
  FOREIGN KEY ("audit_id") REFERENCES "audit" ("audit_id")
);

CREATE TABLE "cart_item" (
  "cart_item_id" uuid NOT NULL,
  "cart_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "quantity" integer NOT NULL,
  "unit_price" numeric(10,2) NOT NULL,
  PRIMARY KEY ("cart_item_id"),
  UNIQUE ("cart_id", "gas_cylinder_id"),
  FOREIGN KEY ("cart_id") REFERENCES "cart" ("cart_id") ON DELETE CASCADE,
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE CASCADE
);

CREATE TABLE "maintenance_task" (
  "task_id" uuid NOT NULL,
  "plan_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "car_id" uuid,
  "delivery_id" uuid,
  "status" varchar(32) NOT NULL,
  "due_at" timestamptz,
  "due_km" integer,
  "predicted_due_at" timestamptz,
  "scheduled_at" timestamptz,
  "performed_at" timestamptz,
  "odometer_km" integer,
  "cost" numeric(10,2),
  "provider" varchar(120),
  "reference_number" varchar(60),
  "category" varchar(10),
  "alerted_at" timestamptz,
  "notes" text,
  PRIMARY KEY ("task_id"),
  FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE,
  FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE CASCADE,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("plan_id") REFERENCES "maintenance_plan" ("plan_id")
);

CREATE TABLE "order" (
  "order_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "time_slot_id" uuid,
  "scheduled_date" date,
  "deposit_amount" numeric(10,2) NOT NULL,
  "deposit_paid" boolean NOT NULL,
  "delivery_id" uuid,
  "address_id" uuid NOT NULL,
  "status" varchar(32) NOT NULL,
  "paymentMethod" varchar(32) NOT NULL,
  "paymentType" varchar(32) NOT NULL,
  "paymentStatus" varchar(32) NOT NULL,
  "totalAmount" numeric(10,2) NOT NULL,
  "notes" text,
  "deliveryInstructions" text,
  "acceptedAt" timestamptz,
  "onTheWayAt" timestamptz,
  "deliveredAt" timestamptz,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "cancellationReason" text,
  "gatewayPaymentId" varchar(100),
  "deliveryCode" varchar(12),
  "receiver_name" varchar(120),
  "receiver_document" varchar(20),
  "receiver_relationship" varchar(40),
  "delivery_mode" varchar(32) NOT NULL,
  "deliveryPoint" varchar(255),
  "coverage_zone_id" uuid,
  "zone_name" varchar(120),
  "zone_surcharge_type" varchar(32),
  "zone_surcharge_value" numeric(10,2),
  "zone_surcharge_amount" numeric(10,2) NOT NULL,
  "subtotal_items" numeric(10,2) NOT NULL,
  "vehicle_car_id" uuid,
  "vehicle_patent" varchar(20),
  "vehicle_brand" varchar(50),
  "vehicle_model" varchar(50),
  "payment_confirmed_at" timestamptz,
  "payment_confirmed_by" uuid,
  "payment_resolution_note" text,
  "payment_resolved_at" timestamptz,
  "payment_resolved_by" uuid,
  PRIMARY KEY ("order_id"),
  FOREIGN KEY ("address_id") REFERENCES "user_address" ("address_id"),
  FOREIGN KEY ("coverage_zone_id") REFERENCES "coverage_zone" ("coverage_zone_id") ON DELETE SET NULL,
  FOREIGN KEY ("customer_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("time_slot_id") REFERENCES "time_slot" ("time_slot_id")
);

CREATE TABLE "purchase_order_item" (
  "item_id" uuid NOT NULL,
  "purchase_order_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "quantity" integer NOT NULL,
  "unit_cost" numeric(12,2) NOT NULL,
  "empties_to_exchange" integer NOT NULL,
  "received_quantity" integer NOT NULL,
  PRIMARY KEY ("item_id"),
  UNIQUE ("purchase_order_id", "gas_cylinder_id"),
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id"),
  FOREIGN KEY ("purchase_order_id") REFERENCES "purchase_order" ("purchase_order_id") ON DELETE CASCADE
);

CREATE TABLE "purchase_receipt" (
  "receipt_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "number" integer NOT NULL,
  "supplier_id" uuid NOT NULL,
  "purchase_order_id" uuid,
  "warehouse_id" uuid NOT NULL,
  "supplier_document_type" varchar(32) NOT NULL,
  "supplier_document_number" varchar(30) NOT NULL,
  "received_at" timestamptz NOT NULL,
  "received_by_user_id" uuid NOT NULL,
  "total_amount" numeric(12,2) NOT NULL,
  "payment_status" varchar(32) NOT NULL,
  "cash_movement_id" uuid,
  "status" varchar(32) NOT NULL,
  "void_reason" text,
  "voided_at" timestamptz,
  "voided_by_user_id" uuid,
  "batch_id" uuid NOT NULL,
  "void_batch_id" uuid,
  "notes" text,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  PRIMARY KEY ("receipt_id"),
  UNIQUE ("distributor_id", "number"),
  UNIQUE ("distributor_id", "supplier_id", "supplier_document_type", "supplier_document_number"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("purchase_order_id") REFERENCES "purchase_order" ("purchase_order_id"),
  FOREIGN KEY ("received_by_user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("supplier_id") REFERENCES "supplier" ("supplier_id"),
  FOREIGN KEY ("warehouse_id") REFERENCES "warehouse" ("warehouse_id")
);

CREATE TABLE "route_batch" (
  "batch_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "status" varchar(32) NOT NULL,
  "total_weight_kg" numeric(10,2) NOT NULL,
  "delivery_id" uuid,
  "created_at" timestamptz NOT NULL,
  PRIMARY KEY ("batch_id"),
  FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE SET NULL,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "stock_location" (
  "location_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "kind" varchar(32) NOT NULL,
  "warehouse_id" uuid,
  "car_id" uuid,
  "createdAt" timestamptz NOT NULL,
  PRIMARY KEY ("location_id"),
  UNIQUE ("car_id"),
  UNIQUE ("warehouse_id"),
  FOREIGN KEY ("car_id") REFERENCES "car" ("car_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("warehouse_id") REFERENCES "warehouse" ("warehouse_id")
);

CREATE TABLE "vehicle_assignment" (
  "assignment_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "car_id" uuid NOT NULL,
  "delivery_id" uuid NOT NULL,
  "assigned_at" timestamptz NOT NULL,
  "released_at" timestamptz,
  "assigned_by_user_id" uuid,
  "released_by_user_id" uuid,
  "note" text,
  PRIMARY KEY ("assignment_id"),
  FOREIGN KEY ("assigned_by_user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE,
  FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE CASCADE,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("released_by_user_id") REFERENCES "user" ("user_id")
);

CREATE TABLE "vehicle_usage_log" (
  "log_id" uuid NOT NULL,
  "car_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "day" date NOT NULL,
  "km" numeric(10,2) NOT NULL,
  "orders" integer NOT NULL,
  "route_hours" numeric(6,2) NOT NULL,
  PRIMARY KEY ("log_id"),
  UNIQUE ("car_id", "day"),
  FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "claims" (
  "claim_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "reason" varchar NOT NULL,
  "description" text NOT NULL,
  "photoUrl" varchar,
  "status" varchar(32) NOT NULL,
  "resolutionNote" text,
  "createdAt" timestamptz NOT NULL,
  "photo_key" varchar(512),
  PRIMARY KEY ("claim_id"),
  FOREIGN KEY ("customer_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id")
);

CREATE TABLE "cylinder" (
  "cylinder_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "serial" varchar NOT NULL,
  "gas_cylinder_id" uuid,
  "state" varchar(32) NOT NULL,
  "current_customer_id" uuid,
  "current_order_id" uuid,
  "deposit" numeric(10,2) NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "manufactured_at" timestamptz,
  "last_inspection_at" timestamptz,
  "expires_at" timestamptz,
  PRIMARY KEY ("cylinder_id"),
  UNIQUE ("distributor_id", "serial"),
  FOREIGN KEY ("current_customer_id") REFERENCES "user" ("user_id") ON DELETE SET NULL,
  FOREIGN KEY ("current_order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE SET NULL
);

CREATE TABLE "incident" (
  "incident_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "reported_by" uuid NOT NULL,
  "type" varchar(32) NOT NULL,
  "description" text NOT NULL,
  "photo_url" varchar,
  "status" varchar(32) NOT NULL,
  "resolution_note" text,
  "createdAt" timestamptz NOT NULL,
  "resolvedAt" timestamptz,
  "moment" varchar(32),
  "photo_key" varchar(512),
  PRIMARY KEY ("incident_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE,
  FOREIGN KEY ("reported_by") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "maintenance_task_attachment" (
  "attachment_id" uuid NOT NULL,
  "task_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "storage_key" varchar(255) NOT NULL,
  "original_name" varchar(255) NOT NULL,
  "mime_type" varchar(100) NOT NULL,
  "size_bytes" integer NOT NULL,
  "uploaded_by_user_id" uuid NOT NULL,
  "uploaded_at" timestamptz NOT NULL,
  "deleted_at" timestamptz,
  PRIMARY KEY ("attachment_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("task_id") REFERENCES "maintenance_task" ("task_id") ON DELETE CASCADE,
  FOREIGN KEY ("uploaded_by_user_id") REFERENCES "user" ("user_id")
);

CREATE TABLE "maintenance_window_proposal" (
  "proposal_id" uuid NOT NULL,
  "task_id" uuid NOT NULL,
  "delivery_id" uuid NOT NULL,
  "window_start" timestamptz NOT NULL,
  "window_end" timestamptz NOT NULL,
  "rank" integer NOT NULL,
  "status" varchar(32) NOT NULL,
  "expires_at" timestamptz NOT NULL,
  "responded_at" timestamptz,
  PRIMARY KEY ("proposal_id"),
  FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE CASCADE,
  FOREIGN KEY ("task_id") REFERENCES "maintenance_task" ("task_id") ON DELETE CASCADE
);

CREATE TABLE "order_address_change" (
  "change_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "from_address_id" uuid NOT NULL,
  "to_address_id" uuid NOT NULL,
  "changed_by_user_id" uuid NOT NULL,
  "changed_at" timestamptz NOT NULL,
  "reason" text,
  PRIMARY KEY ("change_id"),
  FOREIGN KEY ("changed_by_user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("from_address_id") REFERENCES "user_address" ("address_id"),
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE,
  FOREIGN KEY ("to_address_id") REFERENCES "user_address" ("address_id")
);

CREATE TABLE "order_dispatch_offer" (
  "offer_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "driver_id" uuid NOT NULL,
  "status" varchar(32) NOT NULL,
  "expiresAt" timestamptz NOT NULL,
  "offeredAt" timestamptz NOT NULL,
  PRIMARY KEY ("offer_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("driver_id") REFERENCES "user" ("user_id") ON DELETE CASCADE,
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE
);

CREATE TABLE "order_item" (
  "order_item_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "quantity" integer NOT NULL,
  "unitPrice" numeric(10,2) NOT NULL,
  "subtotal" numeric(10,2) NOT NULL,
  PRIMARY KEY ("order_item_id"),
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id"),
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE
);

CREATE TABLE "order_status_history" (
  "history_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "from_status" varchar(32),
  "to_status" varchar(32) NOT NULL,
  "changed_by_user_id" uuid,
  "reason" text,
  "changed_at" timestamptz NOT NULL,
  PRIMARY KEY ("history_id"),
  FOREIGN KEY ("changed_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL,
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE
);

CREATE TABLE "payment" (
  "payment_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "distributor_id" uuid,
  "gateway" varchar(32) NOT NULL,
  "integration" varchar(32) NOT NULL,
  "method" varchar(50),
  "gateway_payment_id" varchar(100),
  "external_reference" varchar,
  "amount" numeric(10,2) NOT NULL,
  "currency" varchar(10) NOT NULL,
  "status" varchar(32) NOT NULL,
  "payment_url" text,
  "is_deposit" boolean NOT NULL,
  "metadata" jsonb,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  PRIMARY KEY ("payment_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id")
);

CREATE TABLE "purchase_receipt_item" (
  "item_id" uuid NOT NULL,
  "receipt_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "quantity_full" integer NOT NULL,
  "quantity_empty_out" integer NOT NULL,
  "unit_cost" numeric(12,2) NOT NULL,
  "previous_average_cost" numeric(12,2),
  "previous_on_hand" integer,
  PRIMARY KEY ("item_id"),
  UNIQUE ("receipt_id", "gas_cylinder_id"),
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id"),
  FOREIGN KEY ("receipt_id") REFERENCES "purchase_receipt" ("receipt_id") ON DELETE CASCADE
);

CREATE TABLE "rating" (
  "rating_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "from_user_id" uuid NOT NULL,
  "to_user_id" uuid NOT NULL,
  "from_role" varchar(32) NOT NULL,
  "stars" integer NOT NULL,
  "comment" text,
  "createdAt" timestamptz NOT NULL,
  "hidden" boolean NOT NULL,
  "hidden_reason" text,
  "hidden_at" timestamptz,
  "hidden_by_user_id" uuid,
  PRIMARY KEY ("rating_id"),
  UNIQUE ("order_id", "from_role"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("from_user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("hidden_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL,
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE,
  FOREIGN KEY ("to_user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "repurchase_invitation" (
  "invitation_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "address_id" uuid,
  "projected_depletion_at" timestamptz NOT NULL,
  "suggested_items" jsonb NOT NULL,
  "status" varchar(32) NOT NULL,
  "expires_at" timestamptz NOT NULL,
  "responded_at" timestamptz,
  "order_id" uuid,
  "created_at" timestamptz NOT NULL,
  PRIMARY KEY ("invitation_id"),
  FOREIGN KEY ("address_id") REFERENCES "user_address" ("address_id") ON DELETE SET NULL,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "route_batch_offer" (
  "offer_id" uuid NOT NULL,
  "batch_id" uuid NOT NULL,
  "delivery_id" uuid NOT NULL,
  "status" varchar(32) NOT NULL,
  "expires_at" timestamptz NOT NULL,
  "responded_at" timestamptz,
  PRIMARY KEY ("offer_id"),
  FOREIGN KEY ("batch_id") REFERENCES "route_batch" ("batch_id") ON DELETE CASCADE,
  FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE CASCADE
);

CREATE TABLE "route_batch_stop" (
  "stop_id" uuid NOT NULL,
  "batch_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "sequence" integer NOT NULL,
  PRIMARY KEY ("stop_id"),
  UNIQUE ("batch_id", "order_id"),
  FOREIGN KEY ("batch_id") REFERENCES "route_batch" ("batch_id") ON DELETE CASCADE,
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE
);

CREATE TABLE "stock_adjustment" (
  "adjustment_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "number" integer NOT NULL,
  "location_id" uuid NOT NULL,
  "reason" varchar(32) NOT NULL,
  "notes" text NOT NULL,
  "batch_id" uuid NOT NULL,
  "created_by_user_id" uuid NOT NULL,
  "createdAt" timestamptz NOT NULL,
  PRIMARY KEY ("adjustment_id"),
  UNIQUE ("distributor_id", "number"),
  FOREIGN KEY ("created_by_user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("location_id") REFERENCES "stock_location" ("location_id")
);

CREATE TABLE "stock_balance" (
  "balance_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "location_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "condition" varchar(32) NOT NULL,
  "quantity" integer NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  PRIMARY KEY ("balance_id"),
  UNIQUE ("location_id", "gas_cylinder_id", "condition"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id"),
  FOREIGN KEY ("location_id") REFERENCES "stock_location" ("location_id")
);

CREATE TABLE "stock_movement" (
  "movement_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "batch_id" uuid NOT NULL,
  "quantity" integer NOT NULL,
  "from_location_id" uuid,
  "from_condition" varchar(32),
  "to_location_id" uuid,
  "to_condition" varchar(32),
  "reason" varchar(32) NOT NULL,
  "reference_type" varchar(32) NOT NULL,
  "reference_id" uuid,
  "reversed_movement_id" uuid,
  "notes" varchar(300),
  "actor_user_id" uuid,
  "occurred_at" timestamptz NOT NULL,
  "createdAt" timestamptz NOT NULL,
  PRIMARY KEY ("movement_id"),
  FOREIGN KEY ("actor_user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("from_location_id") REFERENCES "stock_location" ("location_id"),
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id"),
  FOREIGN KEY ("reversed_movement_id") REFERENCES "stock_movement" ("movement_id"),
  FOREIGN KEY ("to_location_id") REFERENCES "stock_location" ("location_id")
);

CREATE TABLE "cylinder_inspection" (
  "inspection_id" uuid NOT NULL,
  "cylinder_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "inspected_at" timestamptz NOT NULL,
  "result" varchar(32) NOT NULL,
  "next_due_at" timestamptz,
  "notes" text,
  PRIMARY KEY ("inspection_id"),
  FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id") ON DELETE CASCADE,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
);

CREATE TABLE "cylinder_movement" (
  "movement_id" uuid NOT NULL,
  "cylinder_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "from_state" varchar(32),
  "to_state" varchar(32) NOT NULL,
  "order_id" uuid,
  "actor_user_id" uuid,
  "note" text,
  "createdAt" timestamptz NOT NULL,
  PRIMARY KEY ("movement_id"),
  FOREIGN KEY ("actor_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL,
  FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL
);

CREATE TABLE "cylinder_recovery_case" (
  "case_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "cylinder_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "delivered_at" timestamptz NOT NULL,
  "deposit_amount" numeric(10,2) NOT NULL,
  "step" integer NOT NULL,
  "status" varchar(32) NOT NULL,
  "opened_at" timestamptz NOT NULL,
  "closed_at" timestamptz,
  "resolved_by_user_id" uuid,
  "resolution_note" text,
  PRIMARY KEY ("case_id"),
  FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id") ON DELETE CASCADE,
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE,
  FOREIGN KEY ("resolved_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "stock_adjustment_item" (
  "item_id" uuid NOT NULL,
  "adjustment_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "condition" varchar(32) NOT NULL,
  "quantity_delta" integer NOT NULL,
  PRIMARY KEY ("item_id"),
  UNIQUE ("adjustment_id", "gas_cylinder_id", "condition"),
  FOREIGN KEY ("adjustment_id") REFERENCES "stock_adjustment" ("adjustment_id") ON DELETE CASCADE,
  FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id")
);

CREATE TABLE "cylinder_recovery_notice" (
  "notice_id" uuid NOT NULL,
  "case_id" uuid NOT NULL,
  "step" integer NOT NULL,
  "kind" varchar(32) NOT NULL,
  "status" varchar(32),
  "sent_at" timestamptz NOT NULL,
  "expires_at" timestamptz NOT NULL,
  PRIMARY KEY ("notice_id"),
  FOREIGN KEY ("case_id") REFERENCES "cylinder_recovery_case" ("case_id") ON DELETE CASCADE
);
