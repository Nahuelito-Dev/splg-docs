-- Esquema de SPLG — Sistema de Pedidos y Logística de Garrafas de Gas
-- Estado actual de la base: 38 tablas, 84 claves foráneas.
-- Generado por generar-modelo-datos.py
-- Los tipos enumerados y los geográficos de PostGIS se escriben como varchar para
-- que cualquier herramienta de diagramación pueda leer el archivo.
-- Las tablas van en orden de dependencia: se puede ejecutar de corrido.

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
  PRIMARY KEY ("distributor_id"),
  UNIQUE ("slug")
);

CREATE TABLE "role" (
  "role_id" uuid NOT NULL,
  "type" text NOT NULL,
  "createdAt" timestamptz,
  "updatedAt" timestamptz,
  PRIMARY KEY ("role_id"),
  UNIQUE ("type")
);

CREATE TABLE "coverage_zone" (
  "coverage_zone_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "name" varchar(120) NOT NULL,
  "area" varchar(255) NOT NULL,
  "surcharge" numeric(10,2) NOT NULL,
  "isActive" boolean NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "deletedAt" timestamptz,
  "surcharge_type" varchar(32) NOT NULL,
  "label" varchar(40),
  "color" varchar(7),
  "valid_until" timestamptz,
  PRIMARY KEY ("coverage_zone_id"),
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
  PRIMARY KEY ("gas_cylinder_id"),
  UNIQUE ("distributor_id", "type"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id")
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
  PRIMARY KEY ("user_id"),
  UNIQUE ("phone_number"),
  UNIQUE ("firebase_uid"),
  UNIQUE ("email"),
  FOREIGN KEY ("role_id") REFERENCES "role" ("role_id")
);

CREATE TABLE "admin" (
  "admin_id" uuid NOT NULL,
  "distributor_id" uuid,
  "user_id" uuid NOT NULL,
  "createdAt" timestamptz NOT NULL,
  PRIMARY KEY ("admin_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
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
  PRIMARY KEY ("delivery_id"),
  UNIQUE ("user_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "gas_cylinder_promotion" (
  "promotion_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "quantity" integer NOT NULL,
  "discount_percentage" numeric(5,2) NOT NULL,
  PRIMARY KEY ("promotion_id"),
  UNIQUE ("gas_cylinder_id", "quantity"),
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
  "acceptedAt" timestamp,
  "onTheWayAt" timestamp,
  "deliveredAt" timestamp,
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
  PRIMARY KEY ("order_id"),
  FOREIGN KEY ("address_id") REFERENCES "user_address" ("address_id"),
  FOREIGN KEY ("customer_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("time_slot_id") REFERENCES "time_slot" ("time_slot_id")
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
  "createdAt" timestamp NOT NULL,
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
  PRIMARY KEY ("incident_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE,
  FOREIGN KEY ("reported_by") REFERENCES "user" ("user_id") ON DELETE CASCADE
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
  PRIMARY KEY ("rating_id"),
  UNIQUE ("order_id", "from_role"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("from_user_id") REFERENCES "user" ("user_id"),
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
