-- Modelo propuesto — SPLG
-- Los agregados que pidió la cátedra, sobre el esquema que hoy está en la base.
-- PostgreSQL. Se ejecuta en este orden: tipos, columnas nuevas, tablas nuevas,
-- claves foráneas. Generado por generar-modelo-datos.py.

-- ---------- tipos enumerados nuevos ----------
CREATE TYPE "cylinder_inspection_result_enum" AS ENUM ('approved', 'conditional', 'rejected');
CREATE TYPE "fleet_maintenance_type_enum" AS ENUM ('preventive', 'corrective', 'inspection');
CREATE TYPE "fleet_maintenance_status_enum" AS ENUM ('scheduled', 'in_progress', 'done', 'cancelled');
CREATE TYPE "incident_moment_enum" AS ENUM ('pre_delivery', 'in_delivery', 'post_delivery');
CREATE TYPE "order_delivery_mode_enum" AS ENUM ('standard', 'express_moto');

-- ---------- Vencimiento de garrafas ----------
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

-- ---------- Consumo promedio y aviso de recompra ----------
ALTER TABLE "customer" ADD COLUMN IF NOT EXISTS "avg_monthly_consumption_kg" numeric(10,2);
ALTER TABLE "customer" ADD COLUMN IF NOT EXISTS "declared_cylinder_type_id" uuid;
ALTER TABLE "customer" ADD COLUMN IF NOT EXISTS "repurchase_notice_days" integer DEFAULT 3;
ALTER TABLE "customer" ADD COLUMN IF NOT EXISTS "next_repurchase_estimate_at" timestamptz;

-- ---------- Datos de carga del vehículo ----------
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "tare_weight_kg" numeric(10,2);
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "max_load_kg" numeric(10,2);

-- ---------- Mantenimiento y habilitaciones de la flota ----------
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "insurance_company" varchar(120);
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "insurance_policy" varchar(60);
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "insurance_expires_at" timestamptz;
ALTER TABLE "car" ADD COLUMN IF NOT EXISTS "vtv_expires_at" timestamptz;
ALTER TABLE "delivery" ADD COLUMN IF NOT EXISTS "license_number" varchar(30);
ALTER TABLE "delivery" ADD COLUMN IF NOT EXISTS "license_category" varchar(10);
ALTER TABLE "delivery" ADD COLUMN IF NOT EXISTS "license_expires_at" timestamptz;
CREATE TABLE IF NOT EXISTS "fleet_maintenance" (
  "maintenance_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "car_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "type" fleet_maintenance_type_enum NOT NULL,
  "scheduled_at" timestamptz NOT NULL,
  "performed_at" timestamptz,
  "odometer_km" integer,
  "cost" numeric(10,2),
  "notes" text,
  "status" fleet_maintenance_status_enum NOT NULL DEFAULT 'scheduled',
  CONSTRAINT "PK_fleet_maintenance" PRIMARY KEY ("maintenance_id")
);

-- ---------- Carrito de compra ----------
CREATE TABLE IF NOT EXISTS "cart" (
  "cart_id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "user_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "updatedAt" timestamptz NOT NULL DEFAULT now(),
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

-- ---------- Momento de la incidencia ----------
ALTER TABLE "incident" ADD COLUMN IF NOT EXISTS "moment" incident_moment_enum;

-- ---------- Compra directa express en moto ----------
ALTER TABLE "order" ADD COLUMN IF NOT EXISTS "delivery_mode" order_delivery_mode_enum NOT NULL DEFAULT 'standard';
ALTER TABLE "order" ADD COLUMN IF NOT EXISTS "is_express" boolean NOT NULL DEFAULT false;

-- ---------- claves foráneas de lo propuesto ----------
ALTER TABLE "cart" ADD CONSTRAINT "FK_cart_user_id" FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE;
ALTER TABLE "cart" ADD CONSTRAINT "FK_cart_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "customer" ADD CONSTRAINT "FK_customer_declared_cylinder_type_id" FOREIGN KEY ("declared_cylinder_type_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE SET NULL;
ALTER TABLE "cart_item" ADD CONSTRAINT "FK_cart_item_cart_id" FOREIGN KEY ("cart_id") REFERENCES "cart" ("cart_id") ON DELETE CASCADE;
ALTER TABLE "cart_item" ADD CONSTRAINT "FK_cart_item_gas_cylinder_id" FOREIGN KEY ("gas_cylinder_id") REFERENCES "gas_cylinder" ("gas_cylinder_id") ON DELETE CASCADE;
ALTER TABLE "fleet_maintenance" ADD CONSTRAINT "FK_fleet_maintenance_car_id" FOREIGN KEY ("car_id") REFERENCES "car" ("car_id") ON DELETE CASCADE;
ALTER TABLE "fleet_maintenance" ADD CONSTRAINT "FK_fleet_maintenance_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
ALTER TABLE "order_address_change" ADD CONSTRAINT "FK_order_address_change_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE;
ALTER TABLE "order_address_change" ADD CONSTRAINT "FK_order_address_change_from_address_id" FOREIGN KEY ("from_address_id") REFERENCES "user_address" ("address_id") ON DELETE RESTRICT;
ALTER TABLE "order_address_change" ADD CONSTRAINT "FK_order_address_change_to_address_id" FOREIGN KEY ("to_address_id") REFERENCES "user_address" ("address_id") ON DELETE RESTRICT;
ALTER TABLE "order_address_change" ADD CONSTRAINT "FK_order_address_change_changed_by_user_id" FOREIGN KEY ("changed_by_user_id") REFERENCES "user" ("user_id") ON DELETE RESTRICT;
ALTER TABLE "cylinder_inspection" ADD CONSTRAINT "FK_cylinder_inspection_cylinder_id" FOREIGN KEY ("cylinder_id") REFERENCES "cylinder" ("cylinder_id") ON DELETE CASCADE;
ALTER TABLE "cylinder_inspection" ADD CONSTRAINT "FK_cylinder_inspection_distributor_id" FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE;
