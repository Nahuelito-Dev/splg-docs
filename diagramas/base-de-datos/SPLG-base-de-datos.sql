--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Debian 14.13-1.pgdg110+1)
-- Dumped by pg_dump version 14.13 (Debian 14.13-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: claims_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.claims_status_enum AS ENUM (
    'pending',
    'in_process',
    'resolved',
    'rejected'
);


--
-- Name: cylinder_movement_from_state_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cylinder_movement_from_state_enum AS ENUM (
    'in_depot',
    'filled',
    'dispatched',
    'with_customer',
    'empty_returned'
);


--
-- Name: cylinder_movement_to_state_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cylinder_movement_to_state_enum AS ENUM (
    'in_depot',
    'filled',
    'dispatched',
    'with_customer',
    'empty_returned'
);


--
-- Name: cylinder_state_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cylinder_state_enum AS ENUM (
    'in_depot',
    'filled',
    'dispatched',
    'with_customer',
    'empty_returned'
);


--
-- Name: distributor_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.distributor_status_enum AS ENUM (
    'active',
    'suspended'
);


--
-- Name: incident_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.incident_status_enum AS ENUM (
    'open',
    'resolved'
);


--
-- Name: incident_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.incident_type_enum AS ENUM (
    'damaged',
    'out_of_stock',
    'no_show',
    'other'
);


--
-- Name: order_dispatch_offer_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.order_dispatch_offer_status_enum AS ENUM (
    'offered',
    'accepted',
    'rejected',
    'expired'
);


--
-- Name: order_paymentmethod_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.order_paymentmethod_enum AS ENUM (
    'cash',
    'mercadopago',
    'transfer'
);


--
-- Name: order_paymentstatus_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.order_paymentstatus_enum AS ENUM (
    'pending',
    'paid',
    'failed'
);


--
-- Name: order_paymenttype_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.order_paymenttype_enum AS ENUM (
    'cash',
    'online'
);


--
-- Name: order_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.order_status_enum AS ENUM (
    'reserved',
    'pending',
    'accepted',
    'on_the_way',
    'delivered',
    'cancelled'
);


--
-- Name: payment_gateway_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.payment_gateway_enum AS ENUM (
    'mercadopago',
    'cash'
);


--
-- Name: payment_integration_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.payment_integration_enum AS ENUM (
    'checkout_pro',
    'cash'
);


--
-- Name: payment_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.payment_status_enum AS ENUM (
    'pending',
    'approved',
    'rejected',
    'cancelled',
    'refunded'
);


--
-- Name: rating_from_role_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.rating_from_role_enum AS ENUM (
    'customer',
    'delivery'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin (
    admin_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid,
    user_id uuid NOT NULL,
    role_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: car; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.car (
    car_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    user_id uuid NOT NULL,
    type_car character varying(50),
    car_capacity integer,
    car_patent character varying(20),
    car_brand character varying(50),
    car_model character varying(50),
    car_year integer,
    car_color character varying(50),
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: claims; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.claims (
    claim_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    order_id uuid NOT NULL,
    customer_id uuid NOT NULL,
    reason character varying NOT NULL,
    description text NOT NULL,
    "photoUrl" character varying,
    status public.claims_status_enum DEFAULT 'pending'::public.claims_status_enum NOT NULL,
    "resolutionNote" text,
    "createdAt" timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: coverage_zone; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.coverage_zone (
    coverage_zone_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    name character varying(120) NOT NULL,
    area public.geometry(Polygon,4326) NOT NULL,
    surcharge numeric(10,2) DEFAULT '0'::numeric NOT NULL,
    "isActive" boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: customer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer (
    customer_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    notification_token text,
    lat_lang text,
    validated text,
    "createdAt" timestamp with time zone DEFAULT now(),
    "deletedAt" timestamp with time zone
);


--
-- Name: cylinder; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cylinder (
    cylinder_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    serial character varying NOT NULL,
    gas_cylinder_id uuid,
    state public.cylinder_state_enum DEFAULT 'in_depot'::public.cylinder_state_enum NOT NULL,
    current_customer_id uuid,
    current_order_id uuid,
    deposit numeric(10,2) DEFAULT '0'::numeric NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: cylinder_movement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cylinder_movement (
    movement_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    cylinder_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    from_state public.cylinder_movement_from_state_enum,
    to_state public.cylinder_movement_to_state_enum NOT NULL,
    order_id uuid,
    actor_user_id uuid,
    note text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: delivery; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.delivery (
    delivery_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    user_id uuid NOT NULL,
    calification double precision,
    "latLng" text,
    actual_location text,
    "cancelledCharge" real,
    validated boolean DEFAULT false NOT NULL,
    "isActive" boolean DEFAULT true NOT NULL,
    notification_token text,
    "isTraveling" text,
    balance double precision DEFAULT '0'::double precision NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now(),
    "deletedAt" timestamp with time zone
);


--
-- Name: distributor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.distributor (
    distributor_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(120) NOT NULL,
    slug character varying(60) NOT NULL,
    legal_name character varying(160),
    tax_id character varying(20),
    email character varying,
    phone character varying,
    logo_url character varying,
    status public.distributor_status_enum DEFAULT 'active'::public.distributor_status_enum NOT NULL,
    plan character varying,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone
);


--
-- Name: gas_cylinder; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.gas_cylinder (
    gas_cylinder_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    type character varying(50) NOT NULL,
    weight numeric(10,2) NOT NULL,
    price numeric(10,2) NOT NULL,
    stock integer DEFAULT 0 NOT NULL,
    description text,
    "isActive" boolean DEFAULT true NOT NULL,
    promotions jsonb,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: incident; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.incident (
    incident_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    order_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    reported_by uuid NOT NULL,
    type public.incident_type_enum NOT NULL,
    description text NOT NULL,
    photo_url character varying,
    status public.incident_status_enum DEFAULT 'open'::public.incident_status_enum NOT NULL,
    resolution_note text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "resolvedAt" timestamp with time zone
);


--
-- Name: migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."order" (
    order_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    customer_id uuid NOT NULL,
    time_slot_id uuid,
    scheduled_date date,
    deposit_amount numeric(10,2) DEFAULT '0'::numeric NOT NULL,
    deposit_paid boolean DEFAULT false NOT NULL,
    delivery_id uuid,
    address_id uuid NOT NULL,
    status public.order_status_enum DEFAULT 'pending'::public.order_status_enum NOT NULL,
    "paymentMethod" public.order_paymentmethod_enum NOT NULL,
    "paymentType" public.order_paymenttype_enum DEFAULT 'cash'::public.order_paymenttype_enum NOT NULL,
    "paymentStatus" public.order_paymentstatus_enum DEFAULT 'pending'::public.order_paymentstatus_enum NOT NULL,
    "totalAmount" numeric(10,2) NOT NULL,
    notes text,
    "deliveryInstructions" text,
    "deliveryLatitude" character varying(50),
    "deliveryLongitude" character varying(50),
    "acceptedAt" timestamp without time zone,
    "onTheWayAt" timestamp without time zone,
    "deliveredAt" timestamp without time zone,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "cancellationReason" text,
    "gatewayPaymentId" character varying(100),
    "deliveryCode" character varying(12)
);


--
-- Name: order_dispatch_offer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_dispatch_offer (
    offer_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    order_id uuid NOT NULL,
    driver_id uuid NOT NULL,
    status public.order_dispatch_offer_status_enum DEFAULT 'offered'::public.order_dispatch_offer_status_enum NOT NULL,
    "expiresAt" timestamp with time zone NOT NULL,
    "offeredAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: order_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_item (
    order_item_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    order_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    quantity integer NOT NULL,
    "unitPrice" numeric(10,2) NOT NULL,
    subtotal numeric(10,2) NOT NULL
);


--
-- Name: payment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.payment (
    payment_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    order_id uuid NOT NULL,
    distributor_id uuid,
    gateway public.payment_gateway_enum NOT NULL,
    integration public.payment_integration_enum NOT NULL,
    method character varying(50),
    gateway_payment_id character varying(100),
    external_reference character varying,
    amount numeric(10,2) NOT NULL,
    currency character varying(10) DEFAULT 'ARS'::character varying NOT NULL,
    status public.payment_status_enum DEFAULT 'pending'::public.payment_status_enum NOT NULL,
    payment_url text,
    is_deposit boolean DEFAULT false NOT NULL,
    metadata jsonb,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: rating; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rating (
    rating_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    order_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    from_user_id uuid NOT NULL,
    to_user_id uuid NOT NULL,
    from_role public.rating_from_role_enum NOT NULL,
    stars integer NOT NULL,
    comment text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role (
    role_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    type text NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now(),
    "updatedAt" timestamp with time zone DEFAULT now()
);


--
-- Name: time_slot; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.time_slot (
    time_slot_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    name character varying(50) NOT NULL,
    "startTime" time without time zone NOT NULL,
    "endTime" time without time zone NOT NULL,
    capacity integer DEFAULT 50 NOT NULL,
    "isActive" boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    user_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    role_id uuid,
    firebase_uid character varying,
    full_name character varying,
    selfie character varying,
    email character varying,
    phone_number character varying,
    phone_verified boolean DEFAULT false NOT NULL,
    email_verified boolean DEFAULT false NOT NULL,
    blocked boolean DEFAULT false NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone
);


--
-- Name: user_address; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_address (
    address_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    street character varying(255) NOT NULL,
    city character varying(100) NOT NULL,
    "postalCode" character varying(20),
    latitude character varying(50),
    longitude character varying(50),
    "formattedAddress" text,
    "isDefault" boolean DEFAULT false NOT NULL,
    "additionalInstructions" text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: admin PK_08603203f2c50664bda27b1ff89; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT "PK_08603203f2c50664bda27b1ff89" PRIMARY KEY (admin_id);


--
-- Name: order_dispatch_offer PK_0aff47b29f1a507ac9ed28618dd; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_dispatch_offer
    ADD CONSTRAINT "PK_0aff47b29f1a507ac9ed28618dd" PRIMARY KEY (offer_id);


--
-- Name: car PK_1755d5edaf7738f5780f57a445f; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT "PK_1755d5edaf7738f5780f57a445f" PRIMARY KEY (car_id);


--
-- Name: rating PK_1ba02007f1315301d9553a6839a; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "PK_1ba02007f1315301d9553a6839a" PRIMARY KEY (rating_id);


--
-- Name: cylinder PK_3b2102a9e7f6077898af87911f9; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "PK_3b2102a9e7f6077898af87911f9" PRIMARY KEY (cylinder_id);


--
-- Name: coverage_zone PK_3f757c582bbdc9b4f5fd48b57d9; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coverage_zone
    ADD CONSTRAINT "PK_3f757c582bbdc9b4f5fd48b57d9" PRIMARY KEY (coverage_zone_id);


--
-- Name: order PK_58998c5eaeaacdd004dec8b5d86; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "PK_58998c5eaeaacdd004dec8b5d86" PRIMARY KEY (order_id);


--
-- Name: gas_cylinder PK_6768507f2214b15ab4653ef28c9; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder
    ADD CONSTRAINT "PK_6768507f2214b15ab4653ef28c9" PRIMARY KEY (gas_cylinder_id);


--
-- Name: user PK_758b8ce7c18b9d347461b30228d; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "PK_758b8ce7c18b9d347461b30228d" PRIMARY KEY (user_id);


--
-- Name: incident PK_78e450f2684a57c80de36e5d411; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.incident
    ADD CONSTRAINT "PK_78e450f2684a57c80de36e5d411" PRIMARY KEY (incident_id);


--
-- Name: cylinder_movement PK_8a8e801aea031583dea87867f7a; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_movement
    ADD CONSTRAINT "PK_8a8e801aea031583dea87867f7a" PRIMARY KEY (movement_id);


--
-- Name: time_slot PK_9dbd485d0299b8adccf7f933acb; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.time_slot
    ADD CONSTRAINT "PK_9dbd485d0299b8adccf7f933acb" PRIMARY KEY (time_slot_id);


--
-- Name: delivery PK_9f4d2062bce95d9b75e00d145ee; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delivery
    ADD CONSTRAINT "PK_9f4d2062bce95d9b75e00d145ee" PRIMARY KEY (delivery_id);


--
-- Name: payment PK_9fff60ac6ac1844ea4e0cfba67a; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT "PK_9fff60ac6ac1844ea4e0cfba67a" PRIMARY KEY (payment_id);


--
-- Name: distributor PK_a4d4d9b8c62c00011a67eba1abb; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distributor
    ADD CONSTRAINT "PK_a4d4d9b8c62c00011a67eba1abb" PRIMARY KEY (distributor_id);


--
-- Name: user_address PK_b3bdd98c49956021c44c23a48c4; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_address
    ADD CONSTRAINT "PK_b3bdd98c49956021c44c23a48c4" PRIMARY KEY (address_id);


--
-- Name: customer PK_cde3d123fc6077bcd75eb051226; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT "PK_cde3d123fc6077bcd75eb051226" PRIMARY KEY (customer_id);


--
-- Name: role PK_df46160e6aa79943b83c81e496e; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT "PK_df46160e6aa79943b83c81e496e" PRIMARY KEY (role_id);


--
-- Name: claims PK_e8c55807de8dde683de34399da3; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "PK_e8c55807de8dde683de34399da3" PRIMARY KEY (claim_id);


--
-- Name: order_item PK_f91441b7e69922a51a0d2917107; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT "PK_f91441b7e69922a51a0d2917107" PRIMARY KEY (order_item_id);


--
-- Name: customer REL_5d1f609371a285123294fddcf3; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT "REL_5d1f609371a285123294fddcf3" UNIQUE (user_id);


--
-- Name: delivery REL_a3b8af1ce2f6e143d416d83080; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delivery
    ADD CONSTRAINT "REL_a3b8af1ce2f6e143d416d83080" UNIQUE (user_id);


--
-- Name: user UQ_01eea41349b6c9275aec646eee0; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "UQ_01eea41349b6c9275aec646eee0" UNIQUE (phone_number);


--
-- Name: distributor UQ_02331b27890084627684d99ec5b; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distributor
    ADD CONSTRAINT "UQ_02331b27890084627684d99ec5b" UNIQUE (slug);


--
-- Name: car UQ_81fec581f526499deff9677050e; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT "UQ_81fec581f526499deff9677050e" UNIQUE (car_patent);


--
-- Name: cylinder UQ_9e39bbb32ed614ddd09ac126e37; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "UQ_9e39bbb32ed614ddd09ac126e37" UNIQUE (distributor_id, serial);


--
-- Name: user UQ_e12875dfb3b1d92d7d7c5377e22; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "UQ_e12875dfb3b1d92d7d7c5377e22" UNIQUE (email);


--
-- Name: rating UQ_rating_order_role; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "UQ_rating_order_role" UNIQUE (order_id, from_role);


--
-- Name: IDX_01a53f7455396839c245037c9f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_01a53f7455396839c245037c9f" ON public.coverage_zone USING gist (area);


--
-- Name: IDX_02331b27890084627684d99ec5; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "IDX_02331b27890084627684d99ec5" ON public.distributor USING btree (slug);


--
-- Name: IDX_05b8eaefed5471a643ee578c74; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "IDX_05b8eaefed5471a643ee578c74" ON public.payment USING btree (gateway_payment_id) WHERE (gateway_payment_id IS NOT NULL);


--
-- Name: IDX_0cdad15fa39dd1ebace139096f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_0cdad15fa39dd1ebace139096f" ON public.payment USING btree (distributor_id);


--
-- Name: IDX_0fc586a3c26b9bb49e64e6ff1f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_0fc586a3c26b9bb49e64e6ff1f" ON public.admin USING btree (distributor_id);


--
-- Name: IDX_1231f4249963aa2efb93749a8e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_1231f4249963aa2efb93749a8e" ON public.order_dispatch_offer USING btree (order_id);


--
-- Name: IDX_1c48ac355fa0315ba792b68045; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_1c48ac355fa0315ba792b68045" ON public.cylinder_movement USING btree (cylinder_id);


--
-- Name: IDX_21b60d43f182e2b1e8a30ea0a5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_21b60d43f182e2b1e8a30ea0a5" ON public.order_dispatch_offer USING btree (status);


--
-- Name: IDX_3adf34152c77fdb4e8f7346c5f; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "IDX_3adf34152c77fdb4e8f7346c5f" ON public."order" USING btree ("gatewayPaymentId") WHERE ("gatewayPaymentId" IS NOT NULL);


--
-- Name: IDX_50ad99ebfb6554428f39160228; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_50ad99ebfb6554428f39160228" ON public.coverage_zone USING btree (distributor_id);


--
-- Name: IDX_6f590ebbc097c4ed21d5d3e11e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_6f590ebbc097c4ed21d5d3e11e" ON public.rating USING btree (to_user_id);


--
-- Name: IDX_775a36a19670c03781e60bbce9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_775a36a19670c03781e60bbce9" ON public."order" USING btree (scheduled_date);


--
-- Name: IDX_7a848929dbfa5535e93e9494e7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_7a848929dbfa5535e93e9494e7" ON public.cylinder USING btree (serial);


--
-- Name: IDX_7a9573d6a1fb982772a9123320; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_7a9573d6a1fb982772a9123320" ON public."order" USING btree (status);


--
-- Name: IDX_830f3888d1424414675f1c184d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_830f3888d1424414675f1c184d" ON public.order_dispatch_offer USING btree (distributor_id);


--
-- Name: IDX_870bf1e0dc6005837ff0643b5f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_870bf1e0dc6005837ff0643b5f" ON public.claims USING btree (distributor_id);


--
-- Name: IDX_8a89ba6c226022354d0d8b4ada; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_8a89ba6c226022354d0d8b4ada" ON public.incident USING btree (order_id);


--
-- Name: IDX_8b64ee4e6e615c2082862f9e09; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_8b64ee4e6e615c2082862f9e09" ON public.delivery USING btree (distributor_id);


--
-- Name: IDX_903b537f13281f56613047bcdc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_903b537f13281f56613047bcdc" ON public.cylinder USING btree (current_order_id);


--
-- Name: IDX_968ad11170db2741bb5c0c47bb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_968ad11170db2741bb5c0c47bb" ON public.cylinder_movement USING btree (distributor_id);


--
-- Name: IDX_990b829fdf06cb282d835a5d72; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_990b829fdf06cb282d835a5d72" ON public.gas_cylinder USING btree (distributor_id);


--
-- Name: IDX_9e32d1c8fd5721ba71e98c5c93; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_9e32d1c8fd5721ba71e98c5c93" ON public.cylinder USING btree (state);


--
-- Name: IDX_9e8b3d9c0ecf2651f6e836aca4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_9e8b3d9c0ecf2651f6e836aca4" ON public.cylinder USING btree (distributor_id);


--
-- Name: IDX_9ff85bc9c62717502d1ad68216; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_9ff85bc9c62717502d1ad68216" ON public.order_dispatch_offer USING btree ("expiresAt");


--
-- Name: IDX_a2223c18baa97faf54118f95bd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_a2223c18baa97faf54118f95bd" ON public.incident USING btree (distributor_id);


--
-- Name: IDX_a3b8af1ce2f6e143d416d83080; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_a3b8af1ce2f6e143d416d83080" ON public.delivery USING btree (user_id);


--
-- Name: IDX_b46b63fc1ddf2135e1ed37069a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_b46b63fc1ddf2135e1ed37069a" ON public.rating USING btree (distributor_id);


--
-- Name: IDX_beb6f44b22a7f1ed7cad984a2e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_beb6f44b22a7f1ed7cad984a2e" ON public.rating USING btree (order_id);


--
-- Name: IDX_cd7812c96209c5bdd48a6b858b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cd7812c96209c5bdd48a6b858b" ON public."order" USING btree (customer_id);


--
-- Name: IDX_df56039592a4bbbd3fa4a19f14; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_df56039592a4bbbd3fa4a19f14" ON public."order" USING btree (distributor_id);


--
-- Name: IDX_e823ac113ba2af8cbe72ddcbe8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_e823ac113ba2af8cbe72ddcbe8" ON public.car USING btree (distributor_id);


--
-- Name: IDX_e87ae54beaee42b885813deb8e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_e87ae54beaee42b885813deb8e" ON public.time_slot USING btree (distributor_id);


--
-- Name: IDX_f437a76442f23c89ad7652b2a4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_f437a76442f23c89ad7652b2a4" ON public."order" USING btree ("deliveredAt");


--
-- Name: IDX_f5221735ace059250daac9d980; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_f5221735ace059250daac9d980" ON public.payment USING btree (order_id);


--
-- Name: idx_offer_order_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_offer_order_status ON public.order_dispatch_offer USING btree (order_id, status);


--
-- Name: idx_offer_status_expires; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_offer_status_expires ON public.order_dispatch_offer USING btree (status, "expiresAt");


--
-- Name: idx_order_dist_status_delivered; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_order_dist_status_delivered ON public."order" USING btree (distributor_id, status, "deliveredAt");


--
-- Name: idx_order_status_delivery; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_order_status_delivery ON public."order" USING btree (status, delivery_id);


--
-- Name: admin FK_0fc586a3c26b9bb49e64e6ff1f4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT "FK_0fc586a3c26b9bb49e64e6ff1f4" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: order_dispatch_offer FK_1231f4249963aa2efb93749a8ee; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_dispatch_offer
    ADD CONSTRAINT "FK_1231f4249963aa2efb93749a8ee" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE;


--
-- Name: user_address FK_29d6df815a78e4c8291d3cf5e53; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_address
    ADD CONSTRAINT "FK_29d6df815a78e4c8291d3cf5e53" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: coverage_zone FK_50ad99ebfb6554428f39160228a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coverage_zone
    ADD CONSTRAINT "FK_50ad99ebfb6554428f39160228a" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: claims FK_573f53b0981b244cd25223e3ce7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "FK_573f53b0981b244cd25223e3ce7" FOREIGN KEY (order_id) REFERENCES public."order"(order_id);


--
-- Name: customer FK_5d1f609371a285123294fddcf3a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT "FK_5d1f609371a285123294fddcf3a" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: claims FK_870bf1e0dc6005837ff0643b5fc; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "FK_870bf1e0dc6005837ff0643b5fc" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: incident FK_8a89ba6c226022354d0d8b4ada0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.incident
    ADD CONSTRAINT "FK_8a89ba6c226022354d0d8b4ada0" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE;


--
-- Name: delivery FK_8b64ee4e6e615c2082862f9e09a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delivery
    ADD CONSTRAINT "FK_8b64ee4e6e615c2082862f9e09a" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: order_item FK_8ea8fa760695e81b4624345fc72; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT "FK_8ea8fa760695e81b4624345fc72" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id);


--
-- Name: order FK_962eec87d3d029c51525f259fba; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_962eec87d3d029c51525f259fba" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id);


--
-- Name: gas_cylinder FK_990b829fdf06cb282d835a5d729; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder
    ADD CONSTRAINT "FK_990b829fdf06cb282d835a5d729" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: cylinder FK_9e8b3d9c0ecf2651f6e836aca46; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "FK_9e8b3d9c0ecf2651f6e836aca46" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: incident FK_a2223c18baa97faf54118f95bd2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.incident
    ADD CONSTRAINT "FK_a2223c18baa97faf54118f95bd2" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: admin FK_a28028ba709cd7e5053a86857b4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT "FK_a28028ba709cd7e5053a86857b4" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: delivery FK_a3b8af1ce2f6e143d416d83080a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delivery
    ADD CONSTRAINT "FK_a3b8af1ce2f6e143d416d83080a" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: order FK_a4743951fe3b697adf8ce898cf4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_a4743951fe3b697adf8ce898cf4" FOREIGN KEY (time_slot_id) REFERENCES public.time_slot(time_slot_id);


--
-- Name: claims FK_af79ab775a51930eb21951a3c95; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "FK_af79ab775a51930eb21951a3c95" FOREIGN KEY (customer_id) REFERENCES public."user"(user_id);


--
-- Name: rating FK_b46b63fc1ddf2135e1ed37069a9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_b46b63fc1ddf2135e1ed37069a9" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: rating FK_beb6f44b22a7f1ed7cad984a2e1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_beb6f44b22a7f1ed7cad984a2e1" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE;


--
-- Name: car FK_c8d34198d86de9e96aae03b8990; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT "FK_c8d34198d86de9e96aae03b8990" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: order FK_cd7812c96209c5bdd48a6b858b0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_cd7812c96209c5bdd48a6b858b0" FOREIGN KEY (customer_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: rating FK_d613d840f71f5ab083af2ceb1cf; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_d613d840f71f5ab083af2ceb1cf" FOREIGN KEY (from_user_id) REFERENCES public."user"(user_id);


--
-- Name: order FK_df56039592a4bbbd3fa4a19f141; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_df56039592a4bbbd3fa4a19f141" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: car FK_e823ac113ba2af8cbe72ddcbe84; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT "FK_e823ac113ba2af8cbe72ddcbe84" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: time_slot FK_e87ae54beaee42b885813deb8e9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.time_slot
    ADD CONSTRAINT "FK_e87ae54beaee42b885813deb8e9" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: order_item FK_e9674a6053adbaa1057848cddfa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT "FK_e9674a6053adbaa1057848cddfa" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE;


--
-- Name: order FK_f07603e96b068aae820d4590270; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_f07603e96b068aae820d4590270" FOREIGN KEY (address_id) REFERENCES public.user_address(address_id);


--
-- Name: user FK_fb2e442d14add3cefbdf33c4561; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "FK_fb2e442d14add3cefbdf33c4561" FOREIGN KEY (role_id) REFERENCES public.role(role_id);


--
-- Name: admin FK_fd32421f2d93414e46a8fcfd86b; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT "FK_fd32421f2d93414e46a8fcfd86b" FOREIGN KEY (role_id) REFERENCES public.role(role_id);


--
-- PostgreSQL database dump complete
--

