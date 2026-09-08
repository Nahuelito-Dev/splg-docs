-- Esquema de SPLG — Sistema de Pedidos y Logística de Garrafas de Gas
-- Estado actual de la base: 20 tablas, 30 claves foráneas.
-- Generado por generar-modelo-datos.py
-- Los tipos enumerados y los geográficos de PostGIS se escriben como varchar para
-- que cualquier herramienta de diagramación pueda leer el archivo.
-- Las tablas van en orden de dependencia: se puede ejecutar de corrido.

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
  PRIMARY KEY ("movement_id")
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
  PRIMARY KEY ("distributor_id"),
  UNIQUE ("slug")
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
  PRIMARY KEY ("payment_id")
);

CREATE TABLE "role" (
  "role_id" uuid NOT NULL,
  "type" text NOT NULL,
  "createdAt" timestamptz,
  "updatedAt" timestamptz,
  PRIMARY KEY ("role_id")
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
  PRIMARY KEY ("coverage_zone_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id") ON DELETE CASCADE
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
  PRIMARY KEY ("cylinder_id"),
  UNIQUE ("distributor_id", "serial"),
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
  "promotions" jsonb,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  PRIMARY KEY ("gas_cylinder_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id")
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
  UNIQUE ("email"),
  FOREIGN KEY ("role_id") REFERENCES "role" ("role_id")
);

CREATE TABLE "admin" (
  "admin_id" uuid NOT NULL,
  "distributor_id" uuid,
  "user_id" uuid NOT NULL,
  "role_id" uuid NOT NULL,
  "createdAt" timestamptz NOT NULL,
  PRIMARY KEY ("admin_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("role_id") REFERENCES "role" ("role_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
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
  PRIMARY KEY ("car_id"),
  UNIQUE ("car_patent"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "customer" (
  "customer_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "notification_token" text,
  "lat_lang" text,
  "validated" text,
  "createdAt" timestamptz,
  "deletedAt" timestamptz,
  PRIMARY KEY ("customer_id"),
  UNIQUE ("user_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "delivery" (
  "delivery_id" uuid NOT NULL,
  "distributor_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "calification" double precision,
  "latLng" text,
  "actual_location" text,
  "cancelledCharge" real,
  "validated" boolean NOT NULL,
  "isActive" boolean NOT NULL,
  "notification_token" text,
  "isTraveling" text,
  "balance" double precision NOT NULL,
  "createdAt" timestamptz,
  "deletedAt" timestamptz,
  PRIMARY KEY ("delivery_id"),
  UNIQUE ("user_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
);

CREATE TABLE "user_address" (
  "address_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "street" varchar(255) NOT NULL,
  "city" varchar(100) NOT NULL,
  "postalCode" varchar(20),
  "latitude" varchar(50),
  "longitude" varchar(50),
  "formattedAddress" text,
  "isDefault" boolean NOT NULL,
  "additionalInstructions" text,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  PRIMARY KEY ("address_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE
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
  "deliveryLatitude" varchar(50),
  "deliveryLongitude" varchar(50),
  "acceptedAt" timestamp,
  "onTheWayAt" timestamp,
  "deliveredAt" timestamp,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "cancellationReason" text,
  "gatewayPaymentId" varchar(100),
  "deliveryCode" varchar(12),
  PRIMARY KEY ("order_id"),
  FOREIGN KEY ("address_id") REFERENCES "user_address" ("address_id"),
  FOREIGN KEY ("customer_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("delivery_id") REFERENCES "delivery" ("delivery_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("time_slot_id") REFERENCES "time_slot" ("time_slot_id")
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
  PRIMARY KEY ("incident_id"),
  FOREIGN KEY ("distributor_id") REFERENCES "distributor" ("distributor_id"),
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE
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
  FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE
);
