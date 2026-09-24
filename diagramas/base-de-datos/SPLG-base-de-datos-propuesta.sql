-- Modelo propuesto — SPLG
-- Los agregados que pidió la cátedra, sobre el esquema que hoy está en la base.
-- PostgreSQL. Se ejecuta en este orden: tipos, columnas nuevas, tablas nuevas,
-- claves foráneas. Generado por generar-modelo-datos.py.

-- ---------- tipos enumerados nuevos ----------
CREATE TYPE "cylinder_inspection_result_enum" AS ENUM ('approved', 'conditional', 'rejected');
CREATE TYPE "repurchase_invitation_status_enum" AS ENUM ('pending', 'accepted', 'rejected', 'expired');
CREATE TYPE "fleet_status_enum" AS ENUM ('active', 'in_service', 'grounded');
CREATE TYPE "maintenance_subject_enum" AS ENUM ('vehicle', 'driver');
CREATE TYPE "maintenance_trigger_enum" AS ENUM ('by_km', 'by_time', 'by_fixed_date');
CREATE TYPE "maintenance_criticality_enum" AS ENUM ('blocking', 'non_blocking');
CREATE TYPE "maintenance_task_status_enum" AS ENUM ('forecast', 'scheduled', 'in_progress', 'done', 'overdue', 'cancelled');
CREATE TYPE "proposal_status_enum" AS ENUM ('pending', 'accepted', 'rejected', 'expired');
CREATE TYPE "incident_moment_enum" AS ENUM ('pre_delivery', 'in_delivery', 'post_delivery');
CREATE TYPE "order_delivery_mode_enum" AS ENUM ('standard', 'express');
CREATE TYPE "coverage_zone_surcharge_type_enum" AS ENUM ('fixed', 'percentage');
CREATE TYPE "address_geocode_precision_enum" AS ENUM ('exact', 'approximate', 'unresolved');
CREATE TYPE "route_batch_status_enum" AS ENUM ('forming', 'offered', 'assigned', 'dissolved', 'completed');
CREATE TYPE "recovery_case_status_enum" AS ENUM ('open', 'returned', 'escalated', 'deposit_charged', 'written_off', 'closed_no_charge');
CREATE TYPE "recovery_notice_kind_enum" AS ENUM ('reminder', 'pickup_offer', 'deposit_warning');
CREATE TYPE "configurable_process_enum" AS ENUM ('fleet_planner', 'repurchase', 'route_batching', 'cylinder_recovery', 'express_dispatch');
CREATE TYPE "audit_result_enum" AS ENUM ('success', 'failure');

-- ---------- Vigencia de envases ----------
ALTER TABLE "cylinder" ADD COLUMN IF NOT EXISTS "manufactured_at" timestamptz;
ALTER TABLE "cylinder" ADD COLUMN IF NOT EXISTS "last_inspection_at" timestamptz;
ALTER TABLE "cylinder" ADD COLUMN IF NOT EXISTS "expires_at" timestamptz;
CREATE TABLE IF NOT EXISTS "cylinder_inspection" (
  "inspection_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "cylinder_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "inspected_at" timestamptz NOT NULL DEFAULT now(),
  "result" cylinder_inspection_result_enum NOT NULL,
  "next_due_at" timestamptz,
  "notes" text,
  CONSTRAINT "PK_cylinder_inspection" PRIMARY KEY ("inspection_id")
);

-- ---------- Consumo declarado y recompra ----------
ALTER TABLE "customer" ADD COLUMN IF NOT EXISTS "avg_monthly_consumption_kg" numeric(10,2);
ALTER TABLE "customer" ADD COLUMN IF NOT EXISTS "declared_cylinder_type_id" uuid;
ALTER TABLE "customer" ADD COLUMN IF NOT EXISTS "repurchase_notice_days" integer DEFAULT 3;
ALTER TABLE "customer" ADD COLUMN IF NOT EXISTS "next_repurchase_estimate_at" timestamptz;
CREATE TABLE IF NOT EXISTS "repurchase_invitation" (
  "invitation_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "address_id" uuid,
  "projected_depletion_at" timestamptz NOT NULL,
  "suggested_items" jsonb NOT NULL,
  "status" repurchase_invitation_status_enum NOT NULL DEFAULT 'pending',
  "expires_at" timestamptz NOT NULL,
  "responded_at" timestamptz,
  "order_id" uuid,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_repurchase_invitation" PRIMARY KEY ("invitation_id")
);

-- ---------- Flota: habilitaciones, mantenimiento y uso ----------
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "tare_weight_kg" numeric(10,2);
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "max_load_kg" numeric(10,2);
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "odometer_km" integer;
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "fleet_status" fleet_status_enum NOT NULL DEFAULT 'active';
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "in_service_since" timestamptz;
CREATE TABLE IF NOT EXISTS "maintenance_plan" (
  "plan_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "name" varchar(120) NOT NULL,
  "subject" maintenance_subject_enum NOT NULL,
  "trigger" maintenance_trigger_enum NOT NULL,
  "interval_km" integer,
  "interval_months" integer,
  "lead_time_days" integer NOT NULL,
  "criticality" maintenance_criticality_enum NOT NULL,
  "car_type" varchar,
  "is_active" boolean NOT NULL DEFAULT true,
  CONSTRAINT "PK_maintenance_plan" PRIMARY KEY ("plan_id")
);
CREATE TABLE IF NOT EXISTS "maintenance_task" (
  "task_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "plan_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "car_id" uuid,
  "delivery_id" uuid,
  "status" maintenance_task_status_enum NOT NULL DEFAULT 'forecast',
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
  "notes" text,
  CONSTRAINT "PK_maintenance_task" PRIMARY KEY ("task_id")
);
CREATE TABLE IF NOT EXISTS "maintenance_window_proposal" (
  "proposal_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "task_id" uuid NOT NULL,
  "delivery_id" uuid NOT NULL,
  "window_start" timestamptz NOT NULL,
  "window_end" timestamptz NOT NULL,
  "rank" integer NOT NULL,
  "status" proposal_status_enum NOT NULL DEFAULT 'pending',
  "expires_at" timestamptz NOT NULL,
  "responded_at" timestamptz,
  CONSTRAINT "PK_maintenance_window_proposal" PRIMARY KEY ("proposal_id")
);
CREATE TABLE IF NOT EXISTS "vehicle_usage_log" (
  "log_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "car_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "day" date NOT NULL,
  "km" numeric(10,2) NOT NULL,
  "orders" integer NOT NULL DEFAULT 0,
  "route_hours" numeric(6,2) NOT NULL DEFAULT 0,
  CONSTRAINT "PK_vehicle_usage_log" PRIMARY KEY ("log_id"),
  CONSTRAINT "UQ_vehicle_usage_log_car_id_day" UNIQUE ("car_id", "day")
);

-- ---------- Carrito de compra ----------
CREATE TABLE IF NOT EXISTS "cart" (
  "cart_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "user_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "updated_at" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_cart" PRIMARY KEY ("cart_id"),
  CONSTRAINT "UQ_cart_user_id_distributor_id" UNIQUE ("user_id", "distributor_id")
);
CREATE TABLE IF NOT EXISTS "cart_item" (
  "cart_item_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "cart_id" uuid NOT NULL,
  "gas_cylinder_id" uuid NOT NULL,
  "quantity" integer NOT NULL,
  "unit_price" numeric(10,2) NOT NULL,
  CONSTRAINT "PK_cart_item" PRIMARY KEY ("cart_item_id"),
  CONSTRAINT "UQ_cart_item_cart_id_gas_cylinder_id" UNIQUE ("cart_id", "gas_cylinder_id")
);

-- ---------- Cambio de dirección y quién recibe ----------
ALTER TABLE "order" ADD COLUMN IF NOT EXISTS "receiver_name" varchar(120);
ALTER TABLE "order" ADD COLUMN IF NOT EXISTS "receiver_document" varchar(20);
ALTER TABLE "order" ADD COLUMN IF NOT EXISTS "receiver_relationship" varchar(40);
CREATE TABLE IF NOT EXISTS "order_address_change" (
  "change_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "order_id" uuid NOT NULL,
  "from_address_id" uuid NOT NULL,
  "to_address_id" uuid NOT NULL,
  "changed_by_user_id" uuid NOT NULL,
  "changed_at" timestamptz NOT NULL DEFAULT now(),
  "reason" text,
  CONSTRAINT "PK_order_address_change" PRIMARY KEY ("change_id")
);

-- ---------- Historial de estados del pedido ----------
CREATE TABLE IF NOT EXISTS "order_status_history" (
  "history_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "order_id" uuid NOT NULL,
  "from_status" order_status_enum,
  "to_status" order_status_enum NOT NULL,
  "changed_by_user_id" uuid,
  "reason" text,
  "changed_at" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_order_status_history" PRIMARY KEY ("history_id")
);

-- ---------- Momento de la incidencia ----------
ALTER TABLE "incident" ADD COLUMN IF NOT EXISTS "moment" incident_moment_enum;

-- ---------- Entrega express ----------
ALTER TABLE "order" ADD COLUMN IF NOT EXISTS "delivery_mode" order_delivery_mode_enum NOT NULL DEFAULT 'standard';

-- ---------- Recargo porcentual y vigencia de zonas ----------
ALTER TABLE "coverage_zone" ADD COLUMN IF NOT EXISTS "surcharge_type" coverage_zone_surcharge_type_enum NOT NULL DEFAULT 'fixed';
ALTER TABLE "coverage_zone" ADD COLUMN IF NOT EXISTS "label" varchar(40);
ALTER TABLE "coverage_zone" ADD COLUMN IF NOT EXISTS "color" varchar(7);
ALTER TABLE "coverage_zone" ADD COLUMN IF NOT EXISTS "valid_until" timestamptz;

-- ---------- Dirección resuelta contra el mapa ----------
ALTER TABLE "user_address" ADD COLUMN IF NOT EXISTS "floor" varchar(10);
ALTER TABLE "user_address" ADD COLUMN IF NOT EXISTS "apartment" varchar(10);
ALTER TABLE "user_address" ADD COLUMN IF NOT EXISTS "location" geography(Point,4326);
ALTER TABLE "user_address" ADD COLUMN IF NOT EXISTS "place_id" varchar(255);
ALTER TABLE "user_address" ADD COLUMN IF NOT EXISTS "geocode_precision" address_geocode_precision_enum NOT NULL DEFAULT 'unresolved';

-- ---------- Agrupación de pedidos por recorrido ----------
CREATE TABLE IF NOT EXISTS "route_batch" (
  "batch_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "status" route_batch_status_enum NOT NULL DEFAULT 'forming',
  "total_weight_kg" numeric(10,2) NOT NULL,
  "delivery_id" uuid,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_route_batch" PRIMARY KEY ("batch_id")
);
CREATE TABLE IF NOT EXISTS "route_batch_stop" (
  "stop_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "batch_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "sequence" integer NOT NULL,
  CONSTRAINT "PK_route_batch_stop" PRIMARY KEY ("stop_id"),
  CONSTRAINT "UQ_route_batch_stop_batch_id_order_id" UNIQUE ("batch_id", "order_id")
);
CREATE TABLE IF NOT EXISTS "route_batch_offer" (
  "offer_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "batch_id" uuid NOT NULL,
  "delivery_id" uuid NOT NULL,
  "status" proposal_status_enum NOT NULL DEFAULT 'pending',
  "expires_at" timestamptz NOT NULL,
  "responded_at" timestamptz,
  CONSTRAINT "PK_route_batch_offer" PRIMARY KEY ("offer_id")
);

-- ---------- Recupero de envases no devueltos ----------
CREATE TABLE IF NOT EXISTS "cylinder_recovery_case" (
  "case_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "cylinder_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "delivered_at" timestamptz NOT NULL,
  "deposit_amount" numeric(10,2) NOT NULL,
  "step" integer NOT NULL DEFAULT 1,
  "status" recovery_case_status_enum NOT NULL DEFAULT 'open',
  "opened_at" timestamptz NOT NULL DEFAULT now(),
  "closed_at" timestamptz,
  "resolved_by_user_id" uuid,
  "resolution_note" text,
  CONSTRAINT "PK_cylinder_recovery_case" PRIMARY KEY ("case_id")
);
CREATE TABLE IF NOT EXISTS "cylinder_recovery_notice" (
  "notice_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "case_id" uuid NOT NULL,
  "step" integer NOT NULL,
  "kind" recovery_notice_kind_enum NOT NULL,
  "status" proposal_status_enum,
  "sent_at" timestamptz NOT NULL DEFAULT now(),
  "expires_at" timestamptz NOT NULL,
  CONSTRAINT "PK_cylinder_recovery_notice" PRIMARY KEY ("notice_id")
);

-- ---------- Configuración de los procesos automáticos ----------
CREATE TABLE IF NOT EXISTS "module_config" (
  "config_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "module" configurable_process_enum NOT NULL,
  "params" jsonb NOT NULL,
  "updated_at" timestamptz NOT NULL DEFAULT now(),
  "updated_by_user_id" uuid,
  CONSTRAINT "PK_module_config" PRIMARY KEY ("config_id"),
  CONSTRAINT "UQ_module_config_distributor_id_module" UNIQUE ("distributor_id", "module")
);

-- ---------- Registro de auditoría ----------
CREATE TABLE IF NOT EXISTS "audit_log" (
  "audit_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid,
  "actor_user_id" uuid,
  "actor_role" varchar(30),
  "http_method" varchar(10) NOT NULL,
  "resource" varchar(60) NOT NULL,
  "resource_id" varchar(64),
  "path" varchar(255) NOT NULL,
  "client_source" varchar(30),
  "ip" varchar(45),
  "result" audit_result_enum NOT NULL,
  "status_code" integer NOT NULL,
  "changes" jsonb,
  "error_message" text,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_audit_log" PRIMARY KEY ("audit_id")
);

-- ---------- claves foráneas de lo propuesto ----------
ALTER TABLE "maintenance_plan" ADD CONSTRAINT "FK_maintenance_plan_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "audit_log" ADD CONSTRAINT "FK_audit_log_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE SET NULL;
ALTER TABLE "audit_log" ADD CONSTRAINT "FK_audit_log_actor_user_id" FOREIGN KEY ("actor_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "cart" ADD CONSTRAINT "FK_cart_user_id" FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE;
ALTER TABLE "cart" ADD CONSTRAINT "FK_cart_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "customer" ADD CONSTRAINT "FK_customer_declared_cylinder_type_id" FOREIGN KEY ("declared_cylinder_type_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE SET NULL;
ALTER TABLE "module_config" ADD CONSTRAINT "FK_module_config_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "module_config" ADD CONSTRAINT "FK_module_config_updated_by_user_id" FOREIGN KEY ("updated_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "cart_item" ADD CONSTRAINT "FK_cart_item_cart_id" FOREIGN KEY ("cart_id") REFERENCES "cart" ("cart_id") ON DELETE CASCADE;
ALTER TABLE "cart_item" ADD CONSTRAINT "FK_cart_item_gas_cylinder_id" FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE CASCADE;
ALTER TABLE "maintenance_task" ADD CONSTRAINT "FK_maintenance_task_plan_id" FOREIGN KEY ("plan_id") REFERENCES "maintenance_plan" ("plan_id") ON DELETE RESTRICT;
ALTER TABLE "maintenance_task" ADD CONSTRAINT "FK_maintenance_task_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "maintenance_task" ADD CONSTRAINT "FK_maintenance_task_car_id" FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE;
ALTER TABLE "maintenance_task" ADD CONSTRAINT "FK_maintenance_task_delivery_id" FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE CASCADE;
ALTER TABLE "route_batch" ADD CONSTRAINT "FK_route_batch_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "route_batch" ADD CONSTRAINT "FK_route_batch_delivery_id" FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE SET NULL;
ALTER TABLE "vehicle_usage_log" ADD CONSTRAINT "FK_vehicle_usage_log_car_id" FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE;
ALTER TABLE "vehicle_usage_log" ADD CONSTRAINT "FK_vehicle_usage_log_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "maintenance_window_proposal" ADD CONSTRAINT "FK_maintenance_window_proposal_task_id" FOREIGN KEY ("task_id") REFERENCES "maintenance_task" ("task_id") ON DELETE CASCADE;
ALTER TABLE "maintenance_window_proposal" ADD CONSTRAINT "FK_maintenance_window_proposal_delivery_id" FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE CASCADE;
ALTER TABLE "order_address_change" ADD CONSTRAINT "FK_order_address_change_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE;
ALTER TABLE "order_address_change" ADD CONSTRAINT "FK_order_address_change_from_address_id" FOREIGN KEY ("from_address_id") REFERENCES "user_address" ("address_id") ON DELETE RESTRICT;
ALTER TABLE "order_address_change" ADD CONSTRAINT "FK_order_address_change_to_address_id" FOREIGN KEY ("to_address_id") REFERENCES "user_address" ("address_id") ON DELETE RESTRICT;
ALTER TABLE "order_address_change" ADD CONSTRAINT "FK_order_address_change_changed_by_user_id" FOREIGN KEY ("changed_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "order_status_history" ADD CONSTRAINT "FK_order_status_history_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE;
ALTER TABLE "order_status_history" ADD CONSTRAINT "FK_order_status_history_changed_by_user_id" FOREIGN KEY ("changed_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "repurchase_invitation" ADD CONSTRAINT "FK_repurchase_invitation_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "repurchase_invitation" ADD CONSTRAINT "FK_repurchase_invitation_user_id" FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE;
ALTER TABLE "repurchase_invitation" ADD CONSTRAINT "FK_repurchase_invitation_address_id" FOREIGN KEY ("address_id") REFERENCES "user_address" ("address_id") ON DELETE SET NULL;
ALTER TABLE "repurchase_invitation" ADD CONSTRAINT "FK_repurchase_invitation_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;
ALTER TABLE "route_batch_offer" ADD CONSTRAINT "FK_route_batch_offer_batch_id" FOREIGN KEY ("batch_id") REFERENCES "route_batch" ("batch_id") ON DELETE CASCADE;
ALTER TABLE "route_batch_offer" ADD CONSTRAINT "FK_route_batch_offer_delivery_id" FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE CASCADE;
ALTER TABLE "route_batch_stop" ADD CONSTRAINT "FK_route_batch_stop_batch_id" FOREIGN KEY ("batch_id") REFERENCES "route_batch" ("batch_id") ON DELETE CASCADE;
ALTER TABLE "route_batch_stop" ADD CONSTRAINT "FK_route_batch_stop_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_inspection" ADD CONSTRAINT "FK_cylinder_inspection_cylinder_id" FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_inspection" ADD CONSTRAINT "FK_cylinder_inspection_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_recovery_case" ADD CONSTRAINT "FK_cylinder_recovery_case_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_recovery_case" ADD CONSTRAINT "FK_cylinder_recovery_case_cylinder_id" FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_recovery_case" ADD CONSTRAINT "FK_cylinder_recovery_case_user_id" FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_recovery_case" ADD CONSTRAINT "FK_cylinder_recovery_case_resolved_by_user_id" FOREIGN KEY ("resolved_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "cylinder_recovery_notice" ADD CONSTRAINT "FK_cylinder_recovery_notice_case_id" FOREIGN KEY ("case_id") REFERENCES "cylinder_recovery_case" ("case_id") ON DELETE CASCADE;

-- ---------- relaciones que hoy existen sin clave foránea ----------
-- Las filas huérfanas harían fallar el ALTER: se limpian antes, en la misma migración.
ALTER TABLE "payment" ADD CONSTRAINT "FK_payment_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE RESTRICT;
ALTER TABLE "payment" ADD CONSTRAINT "FK_payment_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_cylinder_id" FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id") ON DELETE RESTRICT;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;
ALTER TABLE "cylinder_movement" ADD CONSTRAINT "FK_cylinder_movement_actor_user_id" FOREIGN KEY ("actor_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "cylinder" ADD CONSTRAINT "FK_cylinder_gas_cylinder_id" FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE SET NULL;
ALTER TABLE "cylinder" ADD CONSTRAINT "FK_cylinder_current_customer_id" FOREIGN KEY ("current_customer_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "cylinder" ADD CONSTRAINT "FK_cylinder_current_order_id" FOREIGN KEY ("current_order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;
ALTER TABLE "order_dispatch_offer" ADD CONSTRAINT "FK_order_dispatch_offer_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "order_dispatch_offer" ADD CONSTRAINT "FK_order_dispatch_offer_driver_id" FOREIGN KEY ("driver_id") REFERENCES "user" ("user_id") ON DELETE CASCADE;
ALTER TABLE "incident" ADD CONSTRAINT "FK_incident_reported_by" FOREIGN KEY ("reported_by") REFERENCES "user" ("user_id") ON DELETE CASCADE;
ALTER TABLE "rating" ADD CONSTRAINT "FK_rating_to_user_id" FOREIGN KEY ("to_user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE;
