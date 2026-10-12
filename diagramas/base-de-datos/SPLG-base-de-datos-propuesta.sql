-- Modelo propuesto — SPLG
-- Los cambios de modelo de los casos de uso planificados, sobre el esquema que hoy está en la base.
-- PostgreSQL. Se ejecuta en este orden: tipos, columnas nuevas, tablas nuevas,
-- claves foráneas. Generado por generar-modelo-datos.py.

-- ---------- tipos enumerados nuevos ----------
CREATE TYPE "vehicle_type_enum" AS ENUM ('motorcycle', 'car', 'van');
CREATE TYPE "cash_box_kind_enum" AS ENUM ('cash', 'bank', 'wallet');
CREATE TYPE "cash_session_status_enum" AS ENUM ('open', 'closed');
CREATE TYPE "cash_direction_enum" AS ENUM ('income', 'expense');
CREATE TYPE "cash_system_code_enum" AS ENUM ('driver_settlement', 'customer_payment', 'purchase', 'fuel', 'traffic_fine', 'commission_payment', 'cash_difference', 'box_transfer');
CREATE TYPE "cash_method_enum" AS ENUM ('cash', 'transfer', 'card', 'mercadopago', 'check');
CREATE TYPE "cash_reference_type_enum" AS ENUM ('manual', 'driver_settlement', 'customer_payment', 'purchase_receipt', 'fuel_load', 'traffic_fine', 'driver_liquidation', 'box_transfer', 'reversal');
CREATE TYPE "driver_settlement_status_enum" AS ENUM ('open', 'submitted', 'approved');
CREATE TYPE "settlement_difference_resolution_enum" AS ENUM ('none', 'charged_to_driver', 'absorbed');
CREATE TYPE "tax_condition_enum" AS ENUM ('registered', 'monotax', 'exempt', 'final_consumer');
CREATE TYPE "customer_account_status_enum" AS ENUM ('active', 'blocked', 'closed');
CREATE TYPE "customer_entry_type_enum" AS ENUM ('sale_charge', 'payment', 'credit_note', 'debit_note', 'reversal');
CREATE TYPE "commission_basis_enum" AS ENUM ('per_unit', 'per_order', 'percent_of_total');
CREATE TYPE "commission_entry_type_enum" AS ENUM ('delivery_commission', 'settlement_shortage', 'traffic_fine', 'adjustment', 'legacy_balance', 'carry_forward');
CREATE TYPE "driver_liquidation_status_enum" AS ENUM ('draft', 'approved', 'paid', 'closed', 'voided');
CREATE TYPE "attendance_source_enum" AS ENUM ('panel', 'driver_app');
CREATE TYPE "employee_leave_type_enum" AS ENUM ('vacation', 'sick', 'work_accident', 'study', 'marriage', 'birth', 'bereavement', 'unpaid', 'suspension', 'unjustified_absence', 'other');
CREATE TYPE "employee_leave_status_enum" AS ENUM ('requested', 'approved', 'rejected', 'cancelled');
CREATE TYPE "maintenance_document_kind_enum" AS ENUM ('insurance', 'vtv', 'hazmat_vehicle_permit', 'driver_license', 'hazmat_driver_course', 'psychophysical', 'art_coverage', 'service', 'generic');
CREATE TYPE "fuel_type_enum" AS ENUM ('diesel', 'gasoline', 'cng', 'lpg');
CREATE TYPE "fuel_payment_method_enum" AS ENUM ('cash_box', 'driver_cash', 'card', 'fuel_account');
CREATE TYPE "traffic_fine_status_enum" AS ENUM ('pending', 'appealed', 'paid', 'voided');
CREATE TYPE "vehicle_accident_status_enum" AS ENUM ('reported', 'under_review', 'repairing', 'closed');
CREATE TYPE "tire_status_enum" AS ENUM ('in_stock', 'mounted', 'retired');
CREATE TYPE "tire_event_type_enum" AS ENUM ('mount', 'unmount', 'rotate', 'retread', 'retire');

-- ---------- valores nuevos de tipos enumerados existentes ----------
ALTER TYPE "configurable_process_enum" ADD VALUE IF NOT EXISTS 'dispatch';
ALTER TYPE "configurable_process_enum" ADD VALUE IF NOT EXISTS 'scheduled_tasks';
ALTER TYPE "order_paymentmethod_enum" ADD VALUE IF NOT EXISTS 'account';
ALTER TYPE "order_paymenttype_enum" ADD VALUE IF NOT EXISTS 'account';
ALTER TYPE "maintenance_subject_enum" ADD VALUE IF NOT EXISTS 'employee';

-- ---------- Recargo express y tipo de vehículo ----------
ALTER TABLE "order" ADD COLUMN IF NOT EXISTS "express_surcharge_amount" numeric(12,2) NOT NULL DEFAULT 0;
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "vehicle_type" vehicle_type_enum;

-- ---------- Baja del envase y oferta de retiro ----------
ALTER TABLE "cylinder" ADD COLUMN IF NOT EXISTS "decommissioned_at" timestamptz;
ALTER TABLE "cylinder_recovery_notice" ADD COLUMN IF NOT EXISTS "order_id" uuid;

-- ---------- Caja, rendición del chofer, cuentas corrientes y comisiones ----------
CREATE TABLE IF NOT EXISTS "cash_box" (
  "cash_box_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "name" varchar(80) NOT NULL,
  "kind" cash_box_kind_enum NOT NULL,
  "balance" numeric(14,2) NOT NULL DEFAULT 0,
  "requires_session" boolean NOT NULL DEFAULT false,
  "is_active" boolean NOT NULL DEFAULT true,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  "deletedAt" timestamptz,
  CONSTRAINT "PK_cash_box" PRIMARY KEY ("cash_box_id")
);
CREATE TABLE IF NOT EXISTS "cash_session" (
  "session_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "cash_box_id" uuid NOT NULL,
  "status" cash_session_status_enum NOT NULL DEFAULT 'open',
  "opened_at" timestamptz NOT NULL DEFAULT now(),
  "opened_by_user_id" uuid NOT NULL,
  "opening_amount" numeric(12,2) NOT NULL DEFAULT 0,
  "closed_at" timestamptz,
  "closed_by_user_id" uuid,
  "expected_amount" numeric(12,2),
  "counted_amount" numeric(12,2),
  "difference" numeric(12,2),
  "notes" text,
  CONSTRAINT "PK_cash_session" PRIMARY KEY ("session_id")
);
CREATE TABLE IF NOT EXISTS "cash_category" (
  "category_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "name" varchar(80) NOT NULL,
  "direction" cash_direction_enum NOT NULL,
  "system_code" cash_system_code_enum,
  "is_active" boolean NOT NULL DEFAULT true,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_cash_category" PRIMARY KEY ("category_id"),
  CONSTRAINT "UQ_cash_category_distributor_id_system_code" UNIQUE ("distributor_id", "system_code")
);
CREATE TABLE IF NOT EXISTS "cash_movement" (
  "movement_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "cash_box_id" uuid NOT NULL,
  "session_id" uuid,
  "direction" cash_direction_enum NOT NULL,
  "amount" numeric(12,2) NOT NULL,
  "category_id" uuid NOT NULL,
  "method" cash_method_enum NOT NULL,
  "occurred_at" timestamptz NOT NULL DEFAULT now(),
  "description" varchar(255),
  "reference_type" cash_reference_type_enum NOT NULL DEFAULT 'manual',
  "reference_id" uuid,
  "reverses_movement_id" uuid,
  "created_by_user_id" uuid NOT NULL,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_cash_movement" PRIMARY KEY ("movement_id"),
  CONSTRAINT "UQ_cash_movement_reverses_movement_id" UNIQUE ("reverses_movement_id")
);
CREATE TABLE IF NOT EXISTS "driver_settlement" (
  "settlement_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "delivery_id" uuid NOT NULL,
  "number" integer NOT NULL,
  "business_date" date NOT NULL,
  "status" driver_settlement_status_enum NOT NULL DEFAULT 'open',
  "expected_cash" numeric(12,2) NOT NULL DEFAULT 0,
  "declared_cash" numeric(12,2),
  "driver_expenses" numeric(12,2) NOT NULL DEFAULT 0,
  "difference" numeric(12,2),
  "difference_resolution" settlement_difference_resolution_enum,
  "destination_cash_box_id" uuid,
  "cash_movement_id" uuid,
  "submitted_at" timestamptz,
  "submitted_by_user_id" uuid,
  "approved_at" timestamptz,
  "approved_by_user_id" uuid,
  "alerted_at" timestamptz,
  "notes" text,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_driver_settlement" PRIMARY KEY ("settlement_id")
);
CREATE TABLE IF NOT EXISTS "driver_settlement_order" (
  "settlement_order_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "settlement_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "amount" numeric(12,2) NOT NULL,
  "payment_method" order_paymentmethod_enum NOT NULL,
  CONSTRAINT "PK_driver_settlement_order" PRIMARY KEY ("settlement_order_id"),
  CONSTRAINT "UQ_driver_settlement_order_order_id" UNIQUE ("order_id")
);
CREATE TABLE IF NOT EXISTS "driver_settlement_expense" (
  "expense_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "settlement_id" uuid NOT NULL,
  "category_id" uuid NOT NULL,
  "amount" numeric(12,2) NOT NULL,
  "description" varchar(255),
  CONSTRAINT "PK_driver_settlement_expense" PRIMARY KEY ("expense_id")
);
CREATE TABLE IF NOT EXISTS "customer_account" (
  "account_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "customer_user_id" uuid NOT NULL,
  "business_name" varchar(120) NOT NULL,
  "tax_id" varchar(11),
  "tax_condition" tax_condition_enum NOT NULL,
  "credit_limit" numeric(12,2) NOT NULL DEFAULT 0,
  "payment_terms_days" integer NOT NULL DEFAULT 30,
  "status" customer_account_status_enum NOT NULL DEFAULT 'active',
  "balance" numeric(14,2) NOT NULL DEFAULT 0,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  "deletedAt" timestamptz,
  CONSTRAINT "PK_customer_account" PRIMARY KEY ("account_id")
);
CREATE TABLE IF NOT EXISTS "customer_account_entry" (
  "entry_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "account_id" uuid NOT NULL,
  "type" customer_entry_type_enum NOT NULL,
  "amount" numeric(12,2) NOT NULL,
  "order_id" uuid,
  "due_date" date,
  "payment_method" cash_method_enum,
  "cash_movement_id" uuid,
  "collected_by_delivery_id" uuid,
  "settlement_id" uuid,
  "reverses_entry_id" uuid,
  "description" varchar(255),
  "occurred_at" timestamptz NOT NULL DEFAULT now(),
  "created_by_user_id" uuid,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_customer_account_entry" PRIMARY KEY ("entry_id"),
  CONSTRAINT "UQ_customer_account_entry_reverses_entry_id" UNIQUE ("reverses_entry_id")
);
CREATE TABLE IF NOT EXISTS "customer_account_allocation" (
  "allocation_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "debit_entry_id" uuid NOT NULL,
  "credit_entry_id" uuid NOT NULL,
  "amount" numeric(12,2) NOT NULL,
  CONSTRAINT "PK_customer_account_allocation" PRIMARY KEY ("allocation_id")
);
CREATE TABLE IF NOT EXISTS "commission_rule" (
  "rule_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "employee_id" uuid,
  "gas_cylinder_id" uuid,
  "basis" commission_basis_enum NOT NULL,
  "value" numeric(10,4) NOT NULL,
  "valid_from" date NOT NULL,
  "valid_to" date,
  "is_active" boolean NOT NULL DEFAULT true,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_commission_rule" PRIMARY KEY ("rule_id")
);
CREATE TABLE IF NOT EXISTS "commission_entry" (
  "entry_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "employee_id" uuid NOT NULL,
  "type" commission_entry_type_enum NOT NULL,
  "amount" numeric(12,2) NOT NULL,
  "order_id" uuid,
  "rule_id" uuid,
  "rule_snapshot" jsonb,
  "settlement_id" uuid,
  "liquidation_id" uuid,
  "description" varchar(255),
  "occurred_at" timestamptz NOT NULL DEFAULT now(),
  "created_by_user_id" uuid,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_commission_entry" PRIMARY KEY ("entry_id")
);
CREATE TABLE IF NOT EXISTS "driver_liquidation" (
  "liquidation_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "number" integer NOT NULL,
  "employee_id" uuid NOT NULL,
  "period_from" date NOT NULL,
  "period_to" date NOT NULL,
  "gross" numeric(12,2) NOT NULL,
  "deductions" numeric(12,2) NOT NULL,
  "net" numeric(12,2) NOT NULL,
  "status" driver_liquidation_status_enum NOT NULL DEFAULT 'draft',
  "approved_at" timestamptz,
  "approved_by_user_id" uuid,
  "paid_at" timestamptz,
  "cash_movement_id" uuid,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_driver_liquidation" PRIMARY KEY ("liquidation_id")
);

-- ---------- Personal y legajos ----------
ALTER TABLE "maintenance_plan" ADD COLUMN IF NOT EXISTS "document_kind" maintenance_document_kind_enum;
ALTER TABLE "maintenance_plan" ADD COLUMN IF NOT EXISTS "applies_to_categories" job_position_category_enum[];
ALTER TABLE "maintenance_task" ADD COLUMN IF NOT EXISTS "employee_id" uuid;
ALTER TABLE "maintenance_task" ADD COLUMN IF NOT EXISTS "valid_from" timestamptz;
ALTER TABLE "maintenance_task" ADD COLUMN IF NOT EXISTS "details" jsonb;
CREATE TABLE IF NOT EXISTS "employee_attendance" (
  "attendance_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "employee_id" uuid NOT NULL,
  "work_date" date NOT NULL,
  "check_in_at" timestamptz NOT NULL,
  "check_out_at" timestamptz,
  "source" attendance_source_enum NOT NULL,
  "recorded_by_user_id" uuid,
  "notes" text,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_employee_attendance" PRIMARY KEY ("attendance_id")
);
CREATE TABLE IF NOT EXISTS "employee_leave" (
  "leave_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "employee_id" uuid NOT NULL,
  "type" employee_leave_type_enum NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date NOT NULL,
  "days" integer NOT NULL,
  "status" employee_leave_status_enum NOT NULL DEFAULT 'requested',
  "reason" text,
  "rejection_reason" text,
  "requested_by_user_id" uuid,
  "decided_by_user_id" uuid,
  "decided_at" timestamptz,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_employee_leave" PRIMARY KEY ("leave_id")
);

-- ---------- Flota ampliada: combustible, multas y siniestros ----------
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "fuel_type" fuel_type_enum;
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "tank_capacity_liters" numeric(6,2);
CREATE TABLE IF NOT EXISTS "fuel_load" (
  "fuel_load_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "car_id" uuid NOT NULL,
  "employee_id" uuid,
  "loaded_at" timestamptz NOT NULL,
  "fuel_type" fuel_type_enum NOT NULL,
  "liters" numeric(10,2) NOT NULL,
  "unit_price" numeric(12,3) NOT NULL,
  "total_amount" numeric(12,2) NOT NULL,
  "odometer_km" integer NOT NULL,
  "is_full_tank" boolean NOT NULL DEFAULT true,
  "station" varchar(120),
  "payment_method" fuel_payment_method_enum NOT NULL,
  "receipt_number" varchar(40),
  "cash_movement_id" uuid,
  "anomaly" boolean NOT NULL DEFAULT false,
  "notes" text,
  "created_by_user_id" uuid,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  "deletedAt" timestamptz,
  CONSTRAINT "PK_fuel_load" PRIMARY KEY ("fuel_load_id")
);
CREATE TABLE IF NOT EXISTS "traffic_fine" (
  "fine_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "car_id" uuid NOT NULL,
  "employee_id" uuid,
  "occurred_at" timestamptz NOT NULL,
  "jurisdiction" varchar(80) NOT NULL,
  "act_number" varchar(40) NOT NULL,
  "infraction" text NOT NULL,
  "amount" numeric(12,2) NOT NULL,
  "voluntary_payment_amount" numeric(12,2),
  "due_date" date,
  "status" traffic_fine_status_enum NOT NULL DEFAULT 'pending',
  "paid_at" timestamptz,
  "paid_amount" numeric(12,2),
  "charged_to_employee" boolean NOT NULL DEFAULT false,
  "cash_movement_id" uuid,
  "void_reason" text,
  "alerted_at" timestamptz,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_traffic_fine" PRIMARY KEY ("fine_id"),
  CONSTRAINT "UQ_traffic_fine_distributor_id_jurisdiction_act_number" UNIQUE ("distributor_id", "jurisdiction", "act_number")
);
CREATE TABLE IF NOT EXISTS "vehicle_accident" (
  "accident_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "car_id" uuid NOT NULL,
  "employee_id" uuid,
  "occurred_at" timestamptz NOT NULL,
  "location" geometry(Point,4326),
  "address" text,
  "description" text NOT NULL,
  "injuries" boolean NOT NULL DEFAULT false,
  "third_parties_involved" boolean NOT NULL DEFAULT false,
  "hazmat_release" boolean NOT NULL DEFAULT false,
  "police_report_number" varchar(40),
  "insurer_claim_number" varchar(40),
  "status" vehicle_accident_status_enum NOT NULL DEFAULT 'reported',
  "vehicle_unusable" boolean NOT NULL DEFAULT false,
  "repair_cost" numeric(12,2),
  "insurer_reimbursement" numeric(12,2),
  "deductible_amount" numeric(12,2),
  "closed_at" timestamptz,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_vehicle_accident" PRIMARY KEY ("accident_id")
);

-- ---------- Flota ampliada: neumáticos ----------
CREATE TABLE IF NOT EXISTS "tire" (
  "tire_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "car_id" uuid,
  "serial" varchar(40) NOT NULL,
  "brand" varchar(60) NOT NULL,
  "size" varchar(30) NOT NULL,
  "cost" numeric(12,2) NOT NULL,
  "status" tire_status_enum NOT NULL DEFAULT 'in_stock',
  "position" varchar(6),
  "mounted_odometer_km" integer,
  "createdAt" timestamptz NOT NULL DEFAULT now(),
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT "PK_tire" PRIMARY KEY ("tire_id"),
  CONSTRAINT "UQ_tire_distributor_id_serial" UNIQUE ("distributor_id", "serial")
);
CREATE TABLE IF NOT EXISTS "tire_event" (
  "event_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "distributor_id" uuid NOT NULL,
  "tire_id" uuid NOT NULL,
  "car_id" uuid,
  "event_type" tire_event_type_enum NOT NULL,
  "odometer_km" integer NOT NULL,
  "position" varchar(6),
  "occurred_at" timestamptz NOT NULL DEFAULT now(),
  "created_by_user_id" uuid,
  CONSTRAINT "PK_tire_event" PRIMARY KEY ("event_id")
);

-- ---------- claves foráneas de lo propuesto ----------
ALTER TABLE "cash_box" ADD CONSTRAINT "FK_cash_box_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cash_category" ADD CONSTRAINT "FK_cash_category_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cash_session" ADD CONSTRAINT "FK_cash_session_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cash_session" ADD CONSTRAINT "FK_cash_session_cash_box_id" FOREIGN KEY ("cash_box_id") REFERENCES "cash_box" ("cash_box_id") ON DELETE CASCADE;
ALTER TABLE "cash_session" ADD CONSTRAINT "FK_cash_session_opened_by_user_id" FOREIGN KEY ("opened_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "cash_session" ADD CONSTRAINT "FK_cash_session_closed_by_user_id" FOREIGN KEY ("closed_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "customer_account" ADD CONSTRAINT "FK_customer_account_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "customer_account" ADD CONSTRAINT "FK_customer_account_customer_user_id" FOREIGN KEY ("customer_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "cash_movement" ADD CONSTRAINT "FK_cash_movement_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "cash_movement" ADD CONSTRAINT "FK_cash_movement_cash_box_id" FOREIGN KEY ("cash_box_id") REFERENCES "cash_box" ("cash_box_id") ON DELETE CASCADE;
ALTER TABLE "cash_movement" ADD CONSTRAINT "FK_cash_movement_session_id" FOREIGN KEY ("session_id") REFERENCES "cash_session" ("session_id") ON DELETE SET NULL;
ALTER TABLE "cash_movement" ADD CONSTRAINT "FK_cash_movement_category_id" FOREIGN KEY ("category_id") REFERENCES "cash_category" ("category_id") ON DELETE RESTRICT;
ALTER TABLE "cash_movement" ADD CONSTRAINT "FK_cash_movement_reverses_movement_id" FOREIGN KEY ("reverses_movement_id") REFERENCES "cash_movement" ("movement_id") ON DELETE RESTRICT;
ALTER TABLE "cash_movement" ADD CONSTRAINT "FK_cash_movement_created_by_user_id" FOREIGN KEY ("created_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "commission_rule" ADD CONSTRAINT "FK_commission_rule_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "commission_rule" ADD CONSTRAINT "FK_commission_rule_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE CASCADE;
ALTER TABLE "commission_rule" ADD CONSTRAINT "FK_commission_rule_gas_cylinder_id" FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE CASCADE;
ALTER TABLE "employee_attendance" ADD CONSTRAINT "FK_employee_attendance_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "employee_attendance" ADD CONSTRAINT "FK_employee_attendance_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE CASCADE;
ALTER TABLE "employee_attendance" ADD CONSTRAINT "FK_employee_attendance_recorded_by_user_id" FOREIGN KEY ("recorded_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "employee_leave" ADD CONSTRAINT "FK_employee_leave_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "employee_leave" ADD CONSTRAINT "FK_employee_leave_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE CASCADE;
ALTER TABLE "employee_leave" ADD CONSTRAINT "FK_employee_leave_requested_by_user_id" FOREIGN KEY ("requested_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "employee_leave" ADD CONSTRAINT "FK_employee_leave_decided_by_user_id" FOREIGN KEY ("decided_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "fuel_load" ADD CONSTRAINT "FK_fuel_load_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "fuel_load" ADD CONSTRAINT "FK_fuel_load_car_id" FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE;
ALTER TABLE "fuel_load" ADD CONSTRAINT "FK_fuel_load_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE SET NULL;
ALTER TABLE "fuel_load" ADD CONSTRAINT "FK_fuel_load_created_by_user_id" FOREIGN KEY ("created_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "maintenance_task" ADD CONSTRAINT "FK_maintenance_task_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE CASCADE;
ALTER TABLE "tire" ADD CONSTRAINT "FK_tire_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "tire" ADD CONSTRAINT "FK_tire_car_id" FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE SET NULL;
ALTER TABLE "traffic_fine" ADD CONSTRAINT "FK_traffic_fine_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "traffic_fine" ADD CONSTRAINT "FK_traffic_fine_car_id" FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE;
ALTER TABLE "traffic_fine" ADD CONSTRAINT "FK_traffic_fine_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE SET NULL;
ALTER TABLE "vehicle_accident" ADD CONSTRAINT "FK_vehicle_accident_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "vehicle_accident" ADD CONSTRAINT "FK_vehicle_accident_car_id" FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE;
ALTER TABLE "vehicle_accident" ADD CONSTRAINT "FK_vehicle_accident_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE SET NULL;
ALTER TABLE "driver_liquidation" ADD CONSTRAINT "FK_driver_liquidation_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "driver_liquidation" ADD CONSTRAINT "FK_driver_liquidation_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE RESTRICT;
ALTER TABLE "driver_liquidation" ADD CONSTRAINT "FK_driver_liquidation_approved_by_user_id" FOREIGN KEY ("approved_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "driver_liquidation" ADD CONSTRAINT "FK_driver_liquidation_cash_movement_id" FOREIGN KEY ("cash_movement_id") REFERENCES "cash_movement" ("movement_id") ON DELETE SET NULL;
ALTER TABLE "driver_settlement" ADD CONSTRAINT "FK_driver_settlement_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "driver_settlement" ADD CONSTRAINT "FK_driver_settlement_delivery_id" FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE RESTRICT;
ALTER TABLE "driver_settlement" ADD CONSTRAINT "FK_driver_settlement_destination_cash_box_id" FOREIGN KEY ("destination_cash_box_id") REFERENCES "cash_box" ("cash_box_id") ON DELETE SET NULL;
ALTER TABLE "driver_settlement" ADD CONSTRAINT "FK_driver_settlement_cash_movement_id" FOREIGN KEY ("cash_movement_id") REFERENCES "cash_movement" ("movement_id") ON DELETE SET NULL;
ALTER TABLE "driver_settlement" ADD CONSTRAINT "FK_driver_settlement_submitted_by_user_id" FOREIGN KEY ("submitted_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "driver_settlement" ADD CONSTRAINT "FK_driver_settlement_approved_by_user_id" FOREIGN KEY ("approved_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "tire_event" ADD CONSTRAINT "FK_tire_event_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "tire_event" ADD CONSTRAINT "FK_tire_event_tire_id" FOREIGN KEY ("tire_id") REFERENCES "tire" ("tire_id") ON DELETE CASCADE;
ALTER TABLE "tire_event" ADD CONSTRAINT "FK_tire_event_car_id" FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE SET NULL;
ALTER TABLE "tire_event" ADD CONSTRAINT "FK_tire_event_created_by_user_id" FOREIGN KEY ("created_by_user_id") REFERENCES "user" ("user_id") ON DELETE SET NULL;
ALTER TABLE "commission_entry" ADD CONSTRAINT "FK_commission_entry_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "commission_entry" ADD CONSTRAINT "FK_commission_entry_employee_id" FOREIGN KEY ("employee_id") REFERENCES "employee" ("employee_id") ON DELETE RESTRICT;
ALTER TABLE "commission_entry" ADD CONSTRAINT "FK_commission_entry_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;
ALTER TABLE "commission_entry" ADD CONSTRAINT "FK_commission_entry_rule_id" FOREIGN KEY ("rule_id") REFERENCES "commission_rule" ("rule_id") ON DELETE SET NULL;
ALTER TABLE "commission_entry" ADD CONSTRAINT "FK_commission_entry_settlement_id" FOREIGN KEY ("settlement_id") REFERENCES "driver_settlement" ("settlement_id") ON DELETE SET NULL;
ALTER TABLE "commission_entry" ADD CONSTRAINT "FK_commission_entry_liquidation_id" FOREIGN KEY ("liquidation_id") REFERENCES "driver_liquidation" ("liquidation_id") ON DELETE SET NULL;
ALTER TABLE "commission_entry" ADD CONSTRAINT "FK_commission_entry_created_by_user_id" FOREIGN KEY ("created_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "customer_account_entry" ADD CONSTRAINT "FK_customer_account_entry_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "customer_account_entry" ADD CONSTRAINT "FK_customer_account_entry_account_id" FOREIGN KEY ("account_id") REFERENCES "customer_account" ("account_id") ON DELETE CASCADE;
ALTER TABLE "customer_account_entry" ADD CONSTRAINT "FK_customer_account_entry_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;
ALTER TABLE "customer_account_entry" ADD CONSTRAINT "FK_customer_account_entry_cash_movement_id" FOREIGN KEY ("cash_movement_id") REFERENCES "cash_movement" ("movement_id") ON DELETE SET NULL;
ALTER TABLE "customer_account_entry" ADD CONSTRAINT "FK_customer_account_entry_collected_by_delivery_id" FOREIGN KEY ("collected_by_delivery_id") REFERENCES "delivery" ("delivery_id") ON DELETE SET NULL;
ALTER TABLE "customer_account_entry" ADD CONSTRAINT "FK_customer_account_entry_settlement_id" FOREIGN KEY ("settlement_id") REFERENCES "driver_settlement" ("settlement_id") ON DELETE SET NULL;
ALTER TABLE "customer_account_entry" ADD CONSTRAINT "FK_customer_account_entry_reverses_entry_id" FOREIGN KEY ("reverses_entry_id") REFERENCES "customer_account_entry" ("entry_id") ON DELETE RESTRICT;
ALTER TABLE "customer_account_entry" ADD CONSTRAINT "FK_customer_account_entry_created_by_user_id" FOREIGN KEY ("created_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "driver_settlement_expense" ADD CONSTRAINT "FK_driver_settlement_expense_settlement_id" FOREIGN KEY ("settlement_id") REFERENCES "driver_settlement" ("settlement_id") ON DELETE CASCADE;
ALTER TABLE "driver_settlement_expense" ADD CONSTRAINT "FK_driver_settlement_expense_category_id" FOREIGN KEY ("category_id") REFERENCES "cash_category" ("category_id") ON DELETE RESTRICT;
ALTER TABLE "driver_settlement_order" ADD CONSTRAINT "FK_driver_settlement_order_settlement_id" FOREIGN KEY ("settlement_id") REFERENCES "driver_settlement" ("settlement_id") ON DELETE CASCADE;
ALTER TABLE "driver_settlement_order" ADD CONSTRAINT "FK_driver_settlement_order_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE RESTRICT;
ALTER TABLE "customer_account_allocation" ADD CONSTRAINT "FK_customer_account_allocation_debit_entry_id" FOREIGN KEY ("debit_entry_id") REFERENCES "customer_account_entry" ("entry_id") ON DELETE CASCADE;
ALTER TABLE "customer_account_allocation" ADD CONSTRAINT "FK_customer_account_allocation_credit_entry_id" FOREIGN KEY ("credit_entry_id") REFERENCES "customer_account_entry" ("entry_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_recovery_notice" ADD CONSTRAINT "FK_cylinder_recovery_notice_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;

-- ---------- relaciones que hoy existen sin clave foránea ----------
-- Las filas huérfanas harían fallar el ALTER: se limpian antes, en la misma migración.
