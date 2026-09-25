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
-- Name: address_geocode_precision_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.address_geocode_precision_enum AS ENUM (
    'exact',
    'approximate',
    'unresolved'
);


--
-- Name: audit_result_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.audit_result_enum AS ENUM (
    'success',
    'failure'
);


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
-- Name: configurable_process_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.configurable_process_enum AS ENUM (
    'fleet_planner',
    'repurchase',
    'route_batching',
    'cylinder_recovery',
    'express_dispatch'
);


--
-- Name: coverage_zone_surcharge_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.coverage_zone_surcharge_type_enum AS ENUM (
    'fixed',
    'percentage'
);


--
-- Name: cylinder_inspection_result_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cylinder_inspection_result_enum AS ENUM (
    'approved',
    'conditional',
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
-- Name: fleet_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.fleet_status_enum AS ENUM (
    'active',
    'in_service',
    'grounded'
);


--
-- Name: incident_moment_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.incident_moment_enum AS ENUM (
    'pre_delivery',
    'in_delivery',
    'post_delivery'
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
-- Name: maintenance_criticality_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.maintenance_criticality_enum AS ENUM (
    'blocking',
    'non_blocking'
);


--
-- Name: maintenance_subject_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.maintenance_subject_enum AS ENUM (
    'vehicle',
    'driver'
);


--
-- Name: maintenance_task_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.maintenance_task_status_enum AS ENUM (
    'forecast',
    'scheduled',
    'in_progress',
    'done',
    'overdue',
    'cancelled'
);


--
-- Name: maintenance_trigger_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.maintenance_trigger_enum AS ENUM (
    'by_km',
    'by_time',
    'by_fixed_date'
);


--
-- Name: order_delivery_mode_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.order_delivery_mode_enum AS ENUM (
    'standard',
    'express'
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
-- Name: proposal_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.proposal_status_enum AS ENUM (
    'pending',
    'accepted',
    'rejected',
    'expired'
);


--
-- Name: rating_from_role_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.rating_from_role_enum AS ENUM (
    'customer',
    'delivery'
);


--
-- Name: recovery_case_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.recovery_case_status_enum AS ENUM (
    'open',
    'returned',
    'escalated',
    'deposit_charged',
    'written_off',
    'closed_no_charge'
);


--
-- Name: recovery_notice_kind_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.recovery_notice_kind_enum AS ENUM (
    'reminder',
    'pickup_offer',
    'deposit_warning'
);


--
-- Name: repurchase_invitation_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.repurchase_invitation_status_enum AS ENUM (
    'pending',
    'accepted',
    'rejected',
    'expired'
);


--
-- Name: route_batch_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.route_batch_status_enum AS ENUM (
    'forming',
    'offered',
    'assigned',
    'dissolved',
    'completed'
);


--
-- Name: audit_log_inmutable(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.audit_log_inmutable() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
      BEGIN
        IF TG_OP = 'UPDATE'
           AND (NEW.distributor_id IS NULL OR NEW.distributor_id = OLD.distributor_id)
           AND (NEW.actor_user_id IS NULL OR NEW.actor_user_id = OLD.actor_user_id)
           AND (to_jsonb(NEW) - 'distributor_id' - 'actor_user_id')
             = (to_jsonb(OLD) - 'distributor_id' - 'actor_user_id') THEN
          RETURN NEW;
        END IF;
        RAISE EXCEPTION 'audit_log es de sólo escritura: no se modifican ni se borran asientos';
      END;
      $$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin (
    admin_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid,
    user_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_log (
    audit_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid,
    actor_user_id uuid,
    actor_role character varying(30),
    http_method character varying(10) NOT NULL,
    resource character varying(60) NOT NULL,
    resource_id character varying(64),
    path character varying(255) NOT NULL,
    client_source character varying(30),
    ip character varying(45),
    result public.audit_result_enum NOT NULL,
    status_code integer NOT NULL,
    changes jsonb,
    error_message text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
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
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone,
    tare_weight_kg numeric(10,2),
    max_load_kg numeric(10,2),
    odometer_km integer,
    fleet_status public.fleet_status_enum DEFAULT 'active'::public.fleet_status_enum NOT NULL,
    in_service_since timestamp with time zone
);


--
-- Name: cart; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cart (
    cart_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: cart_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cart_item (
    cart_item_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    cart_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(10,2) NOT NULL
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
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone,
    surcharge_type public.coverage_zone_surcharge_type_enum DEFAULT 'fixed'::public.coverage_zone_surcharge_type_enum NOT NULL,
    label character varying(40),
    color character varying(7),
    valid_until timestamp with time zone
);


--
-- Name: customer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer (
    customer_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    notification_token text,
    validated boolean DEFAULT false NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now(),
    "deletedAt" timestamp with time zone,
    location public.geometry(Point,4326),
    avg_monthly_consumption_kg numeric(10,2),
    declared_cylinder_type_id uuid,
    repurchase_notice_days integer DEFAULT 3,
    next_repurchase_estimate_at timestamp with time zone
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
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    manufactured_at timestamp with time zone,
    last_inspection_at timestamp with time zone,
    expires_at timestamp with time zone
);


--
-- Name: cylinder_inspection; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cylinder_inspection (
    inspection_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    cylinder_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    inspected_at timestamp with time zone DEFAULT now() NOT NULL,
    result public.cylinder_inspection_result_enum NOT NULL,
    next_due_at timestamp with time zone,
    notes text
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
-- Name: cylinder_recovery_case; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cylinder_recovery_case (
    case_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    cylinder_id uuid NOT NULL,
    user_id uuid NOT NULL,
    delivered_at timestamp with time zone NOT NULL,
    deposit_amount numeric(10,2) NOT NULL,
    step integer DEFAULT 1 NOT NULL,
    status public.recovery_case_status_enum DEFAULT 'open'::public.recovery_case_status_enum NOT NULL,
    opened_at timestamp with time zone DEFAULT now() NOT NULL,
    closed_at timestamp with time zone,
    resolved_by_user_id uuid,
    resolution_note text
);


--
-- Name: cylinder_recovery_notice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cylinder_recovery_notice (
    notice_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    case_id uuid NOT NULL,
    step integer NOT NULL,
    kind public.recovery_notice_kind_enum NOT NULL,
    status public.proposal_status_enum,
    sent_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone NOT NULL
);


--
-- Name: delivery; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.delivery (
    delivery_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    user_id uuid NOT NULL,
    calification double precision,
    actual_location text,
    "cancelledCharge" real,
    validated boolean DEFAULT false NOT NULL,
    "isActive" boolean DEFAULT true NOT NULL,
    notification_token text,
    balance double precision DEFAULT '0'::double precision NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now(),
    "deletedAt" timestamp with time zone,
    location public.geometry(Point,4326)
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
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: gas_cylinder_promotion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.gas_cylinder_promotion (
    promotion_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    quantity integer NOT NULL,
    discount_percentage numeric(5,2) NOT NULL,
    CONSTRAINT "CHK_promocion_cantidad" CHECK ((quantity >= 2)),
    CONSTRAINT "CHK_promocion_descuento" CHECK (((discount_percentage > (0)::numeric) AND (discount_percentage <= (100)::numeric)))
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
    "resolvedAt" timestamp with time zone,
    moment public.incident_moment_enum
);


--
-- Name: maintenance_plan; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.maintenance_plan (
    plan_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    name character varying(120) NOT NULL,
    subject public.maintenance_subject_enum NOT NULL,
    trigger public.maintenance_trigger_enum NOT NULL,
    interval_km integer,
    interval_months integer,
    lead_time_days integer NOT NULL,
    criticality public.maintenance_criticality_enum NOT NULL,
    car_type character varying,
    is_active boolean DEFAULT true NOT NULL
);


--
-- Name: maintenance_task; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.maintenance_task (
    task_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    plan_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    car_id uuid,
    delivery_id uuid,
    status public.maintenance_task_status_enum DEFAULT 'forecast'::public.maintenance_task_status_enum NOT NULL,
    due_at timestamp with time zone,
    due_km integer,
    predicted_due_at timestamp with time zone,
    scheduled_at timestamp with time zone,
    performed_at timestamp with time zone,
    odometer_km integer,
    cost numeric(10,2),
    provider character varying(120),
    reference_number character varying(60),
    category character varying(10),
    alerted_at timestamp with time zone,
    notes text
);


--
-- Name: maintenance_window_proposal; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.maintenance_window_proposal (
    proposal_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    task_id uuid NOT NULL,
    delivery_id uuid NOT NULL,
    window_start timestamp with time zone NOT NULL,
    window_end timestamp with time zone NOT NULL,
    rank integer NOT NULL,
    status public.proposal_status_enum DEFAULT 'pending'::public.proposal_status_enum NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    responded_at timestamp with time zone
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
-- Name: module_config; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.module_config (
    config_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    module public.configurable_process_enum NOT NULL,
    params jsonb NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_by_user_id uuid
);


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
    "deliveryCode" character varying(12),
    receiver_name character varying(120),
    receiver_document character varying(20),
    receiver_relationship character varying(40),
    delivery_mode public.order_delivery_mode_enum DEFAULT 'standard'::public.order_delivery_mode_enum NOT NULL
);


--
-- Name: order_address_change; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_address_change (
    change_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    order_id uuid NOT NULL,
    from_address_id uuid NOT NULL,
    to_address_id uuid NOT NULL,
    changed_by_user_id uuid NOT NULL,
    changed_at timestamp with time zone DEFAULT now() NOT NULL,
    reason text
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
-- Name: order_status_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_status_history (
    history_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    order_id uuid NOT NULL,
    from_status public.order_status_enum,
    to_status public.order_status_enum NOT NULL,
    changed_by_user_id uuid,
    reason text,
    changed_at timestamp with time zone DEFAULT now() NOT NULL
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
-- Name: repurchase_invitation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.repurchase_invitation (
    invitation_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    user_id uuid NOT NULL,
    address_id uuid,
    projected_depletion_at timestamp with time zone NOT NULL,
    suggested_items jsonb NOT NULL,
    status public.repurchase_invitation_status_enum DEFAULT 'pending'::public.repurchase_invitation_status_enum NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    responded_at timestamp with time zone,
    order_id uuid,
    created_at timestamp with time zone DEFAULT now() NOT NULL
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
-- Name: route_batch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.route_batch (
    batch_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    status public.route_batch_status_enum DEFAULT 'forming'::public.route_batch_status_enum NOT NULL,
    total_weight_kg numeric(10,2) NOT NULL,
    delivery_id uuid,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: route_batch_offer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.route_batch_offer (
    offer_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    batch_id uuid NOT NULL,
    delivery_id uuid NOT NULL,
    status public.proposal_status_enum DEFAULT 'pending'::public.proposal_status_enum NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    responded_at timestamp with time zone
);


--
-- Name: route_batch_stop; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.route_batch_stop (
    stop_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    batch_id uuid NOT NULL,
    order_id uuid NOT NULL,
    sequence integer NOT NULL
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
    "formattedAddress" text,
    "isDefault" boolean DEFAULT false NOT NULL,
    "additionalInstructions" text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone,
    floor character varying(10),
    apartment character varying(10),
    location public.geometry(Point,4326),
    place_id character varying(255),
    geocode_precision public.address_geocode_precision_enum DEFAULT 'unresolved'::public.address_geocode_precision_enum NOT NULL
);


--
-- Name: vehicle_usage_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicle_usage_log (
    log_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    car_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    day date NOT NULL,
    km numeric(10,2) NOT NULL,
    orders integer DEFAULT 0 NOT NULL,
    route_hours numeric(6,2) DEFAULT '0'::numeric NOT NULL
);


--
-- Name: admin PK_08603203f2c50664bda27b1ff89; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT "PK_08603203f2c50664bda27b1ff89" PRIMARY KEY (admin_id);


--
-- Name: order_address_change PK_08efe70bd1c403b83bdec195f68; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_address_change
    ADD CONSTRAINT "PK_08efe70bd1c403b83bdec195f68" PRIMARY KEY (change_id);


--
-- Name: order_dispatch_offer PK_0aff47b29f1a507ac9ed28618dd; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_dispatch_offer
    ADD CONSTRAINT "PK_0aff47b29f1a507ac9ed28618dd" PRIMARY KEY (offer_id);


--
-- Name: route_batch PK_0c6ffda2ea4ea9b9fce72b79e67; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch
    ADD CONSTRAINT "PK_0c6ffda2ea4ea9b9fce72b79e67" PRIMARY KEY (batch_id);


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
-- Name: maintenance_task PK_470104a71d4cef9fdebb18367bf; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "PK_470104a71d4cef9fdebb18367bf" PRIMARY KEY (task_id);


--
-- Name: vehicle_usage_log PK_53aa08b240936d6d339c9ef4fd9; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_usage_log
    ADD CONSTRAINT "PK_53aa08b240936d6d339c9ef4fd9" PRIMARY KEY (log_id);


--
-- Name: cylinder_recovery_case PK_57f617559d6ec3f36ff939b3f33; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_recovery_case
    ADD CONSTRAINT "PK_57f617559d6ec3f36ff939b3f33" PRIMARY KEY (case_id);


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
-- Name: cylinder_recovery_notice PK_8bf6cdcdc12feb57a8514f5550d; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_recovery_notice
    ADD CONSTRAINT "PK_8bf6cdcdc12feb57a8514f5550d" PRIMARY KEY (notice_id);


--
-- Name: audit_log PK_90d705dc65e834a7bfc79ea4df0; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT "PK_90d705dc65e834a7bfc79ea4df0" PRIMARY KEY (audit_id);


--
-- Name: maintenance_window_proposal PK_93c5f2c747e191c299906a6afd1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_window_proposal
    ADD CONSTRAINT "PK_93c5f2c747e191c299906a6afd1" PRIMARY KEY (proposal_id);


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
-- Name: order_status_history PK_a4248a149d1835f67729d493bab; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status_history
    ADD CONSTRAINT "PK_a4248a149d1835f67729d493bab" PRIMARY KEY (history_id);


--
-- Name: distributor PK_a4d4d9b8c62c00011a67eba1abb; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distributor
    ADD CONSTRAINT "PK_a4d4d9b8c62c00011a67eba1abb" PRIMARY KEY (distributor_id);


--
-- Name: cart_item PK_a96f2f9a014485fe47477c26c4a; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT "PK_a96f2f9a014485fe47477c26c4a" PRIMARY KEY (cart_item_id);


--
-- Name: user_address PK_b3bdd98c49956021c44c23a48c4; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_address
    ADD CONSTRAINT "PK_b3bdd98c49956021c44c23a48c4" PRIMARY KEY (address_id);


--
-- Name: route_batch_offer PK_b7ec066a1beaa3fceff509de72d; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_offer
    ADD CONSTRAINT "PK_b7ec066a1beaa3fceff509de72d" PRIMARY KEY (offer_id);


--
-- Name: cart PK_c741cd2adcfb2f2d1c2743d76b6; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT "PK_c741cd2adcfb2f2d1c2743d76b6" PRIMARY KEY (cart_id);


--
-- Name: cylinder_inspection PK_ccd91038cdcafc7f43a46c9ca16; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_inspection
    ADD CONSTRAINT "PK_ccd91038cdcafc7f43a46c9ca16" PRIMARY KEY (inspection_id);


--
-- Name: customer PK_cde3d123fc6077bcd75eb051226; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT "PK_cde3d123fc6077bcd75eb051226" PRIMARY KEY (customer_id);


--
-- Name: repurchase_invitation PK_cf3829957696955e53d5f45a192; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.repurchase_invitation
    ADD CONSTRAINT "PK_cf3829957696955e53d5f45a192" PRIMARY KEY (invitation_id);


--
-- Name: gas_cylinder_promotion PK_cf52f52e1b6843b4de1496556b1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder_promotion
    ADD CONSTRAINT "PK_cf52f52e1b6843b4de1496556b1" PRIMARY KEY (promotion_id);


--
-- Name: route_batch_stop PK_d9ba16fd7aeaeb044ce2a375886; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_stop
    ADD CONSTRAINT "PK_d9ba16fd7aeaeb044ce2a375886" PRIMARY KEY (stop_id);


--
-- Name: module_config PK_dc79262c913215440d9bf442d65; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_config
    ADD CONSTRAINT "PK_dc79262c913215440d9bf442d65" PRIMARY KEY (config_id);


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
-- Name: maintenance_plan PK_faeec4a9735696ac9d1c915b380; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_plan
    ADD CONSTRAINT "PK_faeec4a9735696ac9d1c915b380" PRIMARY KEY (plan_id);


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
-- Name: cylinder UQ_9e39bbb32ed614ddd09ac126e37; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "UQ_9e39bbb32ed614ddd09ac126e37" UNIQUE (distributor_id, serial);


--
-- Name: cart_item UQ_cart_item_cart_gascylinder; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT "UQ_cart_item_cart_gascylinder" UNIQUE (cart_id, gas_cylinder_id);


--
-- Name: cart UQ_cart_user_distributor; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT "UQ_cart_user_distributor" UNIQUE (user_id, distributor_id);


--
-- Name: user UQ_e12875dfb3b1d92d7d7c5377e22; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "UQ_e12875dfb3b1d92d7d7c5377e22" UNIQUE (email);


--
-- Name: module_config UQ_module_config_distributor_module; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_config
    ADD CONSTRAINT "UQ_module_config_distributor_module" UNIQUE (distributor_id, module);


--
-- Name: gas_cylinder_promotion UQ_promocion_producto_cantidad; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder_promotion
    ADD CONSTRAINT "UQ_promocion_producto_cantidad" UNIQUE (gas_cylinder_id, quantity);


--
-- Name: rating UQ_rating_order_role; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "UQ_rating_order_role" UNIQUE (order_id, from_role);


--
-- Name: route_batch_stop UQ_route_batch_stop_batch_order; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_stop
    ADD CONSTRAINT "UQ_route_batch_stop_batch_order" UNIQUE (batch_id, order_id);


--
-- Name: vehicle_usage_log UQ_vehicle_usage_log_car_day; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_usage_log
    ADD CONSTRAINT "UQ_vehicle_usage_log_car_day" UNIQUE (car_id, day);


--
-- Name: IDX_0124ec56df62d9a9ba58cb41a2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_0124ec56df62d9a9ba58cb41a2" ON public.customer USING gist (location);


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
-- Name: IDX_17f0b53699f596f5eb43c0374f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_17f0b53699f596f5eb43c0374f" ON public.repurchase_invitation USING btree (user_id);


--
-- Name: IDX_1c48ac355fa0315ba792b68045; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_1c48ac355fa0315ba792b68045" ON public.cylinder_movement USING btree (cylinder_id);


--
-- Name: IDX_1cbfd2007890911e8b42d207d4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_1cbfd2007890911e8b42d207d4" ON public.cylinder_inspection USING btree (distributor_id);


--
-- Name: IDX_21b60d43f182e2b1e8a30ea0a5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_21b60d43f182e2b1e8a30ea0a5" ON public.order_dispatch_offer USING btree (status);


--
-- Name: IDX_32fe6a642ad74004e88561b07a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_32fe6a642ad74004e88561b07a" ON public.cylinder_recovery_case USING btree (cylinder_id);


--
-- Name: IDX_39b785b153c83c123bd9d19998; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_39b785b153c83c123bd9d19998" ON public.route_batch USING btree (distributor_id);


--
-- Name: IDX_3adf34152c77fdb4e8f7346c5f; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "IDX_3adf34152c77fdb4e8f7346c5f" ON public."order" USING btree ("gatewayPaymentId") WHERE ("gatewayPaymentId" IS NOT NULL);


--
-- Name: IDX_50ad99ebfb6554428f39160228; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_50ad99ebfb6554428f39160228" ON public.coverage_zone USING btree (distributor_id);


--
-- Name: IDX_531df2a7a7ab3fda4f1591e80d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_531df2a7a7ab3fda4f1591e80d" ON public.cylinder_inspection USING btree (cylinder_id);


--
-- Name: IDX_6f590ebbc097c4ed21d5d3e11e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_6f590ebbc097c4ed21d5d3e11e" ON public.rating USING btree (to_user_id);


--
-- Name: IDX_775a36a19670c03781e60bbce9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_775a36a19670c03781e60bbce9" ON public."order" USING btree (scheduled_date);


--
-- Name: IDX_77cd8b4b3c44851b932ca9c12d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_77cd8b4b3c44851b932ca9c12d" ON public.cylinder_recovery_case USING btree (user_id);


--
-- Name: IDX_7a848929dbfa5535e93e9494e7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_7a848929dbfa5535e93e9494e7" ON public.cylinder USING btree (serial);


--
-- Name: IDX_7a9573d6a1fb982772a9123320; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_7a9573d6a1fb982772a9123320" ON public."order" USING btree (status);


--
-- Name: IDX_7ee5533ee6d3b24f7d74a2c61c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_7ee5533ee6d3b24f7d74a2c61c" ON public.maintenance_plan USING btree (distributor_id);


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
-- Name: IDX_8d4be9c7008fc808b4900a83a5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_8d4be9c7008fc808b4900a83a5" ON public.vehicle_usage_log USING btree (distributor_id);


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
-- Name: IDX_audit_log_actor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_log_actor" ON public.audit_log USING btree (actor_user_id);


--
-- Name: IDX_audit_log_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_log_created_at" ON public.audit_log USING btree (created_at);


--
-- Name: IDX_audit_log_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_log_distributor" ON public.audit_log USING btree (distributor_id);


--
-- Name: IDX_b46b63fc1ddf2135e1ed37069a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_b46b63fc1ddf2135e1ed37069a" ON public.rating USING btree (distributor_id);


--
-- Name: IDX_ba2e1f43e70ba77c13d6844ee8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_ba2e1f43e70ba77c13d6844ee8" ON public.module_config USING btree (distributor_id);


--
-- Name: IDX_beb6f44b22a7f1ed7cad984a2e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_beb6f44b22a7f1ed7cad984a2e" ON public.rating USING btree (order_id);


--
-- Name: IDX_c270386a78fdf46067bc9a94a7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_c270386a78fdf46067bc9a94a7" ON public.delivery USING gist (location);


--
-- Name: IDX_cd7812c96209c5bdd48a6b858b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cd7812c96209c5bdd48a6b858b" ON public."order" USING btree (customer_id);


--
-- Name: IDX_d6bb53d55c3556b23295d5ac5a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_d6bb53d55c3556b23295d5ac5a" ON public.cylinder_recovery_case USING btree (distributor_id);


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
-- Name: IDX_ea6566148b8616520f5a1a7f1a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_ea6566148b8616520f5a1a7f1a" ON public.cylinder_recovery_notice USING btree (case_id);


--
-- Name: IDX_ec297644c2db0dab5171e00f1f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_ec297644c2db0dab5171e00f1f" ON public.repurchase_invitation USING btree (distributor_id);


--
-- Name: IDX_ec96001f6fe2869ae6b40f2dc8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_ec96001f6fe2869ae6b40f2dc8" ON public.maintenance_task USING btree (distributor_id);


--
-- Name: IDX_ef8ba785cbfbb81849828b38e7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_ef8ba785cbfbb81849828b38e7" ON public.user_address USING gist (location);


--
-- Name: IDX_f437a76442f23c89ad7652b2a4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_f437a76442f23c89ad7652b2a4" ON public."order" USING btree ("deliveredAt");


--
-- Name: IDX_f5221735ace059250daac9d980; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_f5221735ace059250daac9d980" ON public.payment USING btree (order_id);


--
-- Name: UQ_admin_user; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_admin_user" ON public.admin USING btree (user_id);


--
-- Name: UQ_car_patente_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_car_patente_vigente" ON public.car USING btree (car_patent) WHERE ("deletedAt" IS NULL);


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
-- Name: audit_log audit_log_inmutable; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER audit_log_inmutable BEFORE DELETE OR UPDATE ON public.audit_log FOR EACH ROW EXECUTE FUNCTION public.audit_log_inmutable();


--
-- Name: repurchase_invitation FK_08d87c5a7e23297e7658f341f68; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.repurchase_invitation
    ADD CONSTRAINT "FK_08d87c5a7e23297e7658f341f68" FOREIGN KEY (address_id) REFERENCES public.user_address(address_id) ON DELETE SET NULL;


--
-- Name: gas_cylinder_promotion FK_0a42c125880d87457584a8155d1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder_promotion
    ADD CONSTRAINT "FK_0a42c125880d87457584a8155d1" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE CASCADE;


--
-- Name: maintenance_task FK_0c10df10892879498bf6037f951; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "FK_0c10df10892879498bf6037f951" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE CASCADE;


--
-- Name: payment FK_0cdad15fa39dd1ebace139096fe; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT "FK_0cdad15fa39dd1ebace139096fe" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: order_address_change FK_0df2b04b370f3e43a31ba1bf92d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_address_change
    ADD CONSTRAINT "FK_0df2b04b370f3e43a31ba1bf92d" FOREIGN KEY (to_address_id) REFERENCES public.user_address(address_id) ON DELETE RESTRICT;


--
-- Name: order_dispatch_offer FK_0f0f1167f4d0249c579b32b10ce; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_dispatch_offer
    ADD CONSTRAINT "FK_0f0f1167f4d0249c579b32b10ce" FOREIGN KEY (driver_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


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
-- Name: repurchase_invitation FK_17f0b53699f596f5eb43c0374f4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.repurchase_invitation
    ADD CONSTRAINT "FK_17f0b53699f596f5eb43c0374f4" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: route_batch_offer FK_18e6affa6e02d38211d2c66bbc6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_offer
    ADD CONSTRAINT "FK_18e6affa6e02d38211d2c66bbc6" FOREIGN KEY (batch_id) REFERENCES public.route_batch(batch_id) ON DELETE CASCADE;


--
-- Name: maintenance_window_proposal FK_199a2b630307c31e90bf0545c26; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_window_proposal
    ADD CONSTRAINT "FK_199a2b630307c31e90bf0545c26" FOREIGN KEY (task_id) REFERENCES public.maintenance_task(task_id) ON DELETE CASCADE;


--
-- Name: cylinder_movement FK_1c48ac355fa0315ba792b680456; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_movement
    ADD CONSTRAINT "FK_1c48ac355fa0315ba792b680456" FOREIGN KEY (cylinder_id) REFERENCES public.cylinder(cylinder_id) ON DELETE RESTRICT;


--
-- Name: audit_log FK_1c4c8c76598008ea972a84e7834; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT "FK_1c4c8c76598008ea972a84e7834" FOREIGN KEY (actor_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


--
-- Name: order_status_history FK_1ca7d5228cf9dc589b60243933c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status_history
    ADD CONSTRAINT "FK_1ca7d5228cf9dc589b60243933c" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE;


--
-- Name: cylinder_inspection FK_1cbfd2007890911e8b42d207d4b; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_inspection
    ADD CONSTRAINT "FK_1cbfd2007890911e8b42d207d4b" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: cylinder_movement FK_2130833c25a6c8ef1a1bf119ed0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_movement
    ADD CONSTRAINT "FK_2130833c25a6c8ef1a1bf119ed0" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE SET NULL;


--
-- Name: maintenance_window_proposal FK_24b20b6fcfe92abf85bc56c9072; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_window_proposal
    ADD CONSTRAINT "FK_24b20b6fcfe92abf85bc56c9072" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE CASCADE;


--
-- Name: maintenance_task FK_296b62bd1680483d20f2652e62f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "FK_296b62bd1680483d20f2652e62f" FOREIGN KEY (plan_id) REFERENCES public.maintenance_plan(plan_id) ON DELETE RESTRICT;


--
-- Name: user_address FK_29d6df815a78e4c8291d3cf5e53; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_address
    ADD CONSTRAINT "FK_29d6df815a78e4c8291d3cf5e53" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: vehicle_usage_log FK_2eb120806e084673aa3ed255648; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_usage_log
    ADD CONSTRAINT "FK_2eb120806e084673aa3ed255648" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE CASCADE;


--
-- Name: cylinder_recovery_case FK_32fe6a642ad74004e88561b07aa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_recovery_case
    ADD CONSTRAINT "FK_32fe6a642ad74004e88561b07aa" FOREIGN KEY (cylinder_id) REFERENCES public.cylinder(cylinder_id) ON DELETE CASCADE;


--
-- Name: cart_item FK_38a83baf23c61fcb6a28521e4cd; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT "FK_38a83baf23c61fcb6a28521e4cd" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE CASCADE;


--
-- Name: route_batch FK_39b785b153c83c123bd9d19998b; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch
    ADD CONSTRAINT "FK_39b785b153c83c123bd9d19998b" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: route_batch FK_3d79cb7510a1e307205011172e1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch
    ADD CONSTRAINT "FK_3d79cb7510a1e307205011172e1" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE SET NULL;


--
-- Name: route_batch_offer FK_473c8590cc59607b872737c10e7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_offer
    ADD CONSTRAINT "FK_473c8590cc59607b872737c10e7" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE CASCADE;


--
-- Name: order_address_change FK_4c82c1fe16612f55a925ec87741; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_address_change
    ADD CONSTRAINT "FK_4c82c1fe16612f55a925ec87741" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE;


--
-- Name: order_address_change FK_4edcddc447d5f54977484558f13; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_address_change
    ADD CONSTRAINT "FK_4edcddc447d5f54977484558f13" FOREIGN KEY (from_address_id) REFERENCES public.user_address(address_id) ON DELETE RESTRICT;


--
-- Name: coverage_zone FK_50ad99ebfb6554428f39160228a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coverage_zone
    ADD CONSTRAINT "FK_50ad99ebfb6554428f39160228a" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: cylinder_inspection FK_531df2a7a7ab3fda4f1591e80d6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_inspection
    ADD CONSTRAINT "FK_531df2a7a7ab3fda4f1591e80d6" FOREIGN KEY (cylinder_id) REFERENCES public.cylinder(cylinder_id) ON DELETE CASCADE;


--
-- Name: claims FK_573f53b0981b244cd25223e3ce7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "FK_573f53b0981b244cd25223e3ce7" FOREIGN KEY (order_id) REFERENCES public."order"(order_id);


--
-- Name: incident FK_583453357cb3e8da99d4bc5a28c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.incident
    ADD CONSTRAINT "FK_583453357cb3e8da99d4bc5a28c" FOREIGN KEY (reported_by) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: customer FK_5d1f609371a285123294fddcf3a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT "FK_5d1f609371a285123294fddcf3a" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: audit_log FK_617015cb20b8887ecb699504a84; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT "FK_617015cb20b8887ecb699504a84" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE SET NULL;


--
-- Name: cylinder FK_623bf3b34c3d9586cf2ae461573; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "FK_623bf3b34c3d9586cf2ae461573" FOREIGN KEY (current_customer_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


--
-- Name: rating FK_6f590ebbc097c4ed21d5d3e11ed; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_6f590ebbc097c4ed21d5d3e11ed" FOREIGN KEY (to_user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: cylinder_recovery_case FK_77cd8b4b3c44851b932ca9c12df; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_recovery_case
    ADD CONSTRAINT "FK_77cd8b4b3c44851b932ca9c12df" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: route_batch_stop FK_7b0e52715d563cbd42bbba07611; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_stop
    ADD CONSTRAINT "FK_7b0e52715d563cbd42bbba07611" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE;


--
-- Name: maintenance_plan FK_7ee5533ee6d3b24f7d74a2c61ce; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_plan
    ADD CONSTRAINT "FK_7ee5533ee6d3b24f7d74a2c61ce" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: order_dispatch_offer FK_830f3888d1424414675f1c184d9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_dispatch_offer
    ADD CONSTRAINT "FK_830f3888d1424414675f1c184d9" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: vehicle_usage_log FK_8d4be9c7008fc808b4900a83a5d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_usage_log
    ADD CONSTRAINT "FK_8d4be9c7008fc808b4900a83a5d" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: order_item FK_8ea8fa760695e81b4624345fc72; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT "FK_8ea8fa760695e81b4624345fc72" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id);


--
-- Name: cylinder FK_903b537f13281f56613047bcdce; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "FK_903b537f13281f56613047bcdce" FOREIGN KEY (current_order_id) REFERENCES public."order"(order_id) ON DELETE SET NULL;


--
-- Name: cylinder_recovery_case FK_91d1e55b673db38c8f99d08f4d2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_recovery_case
    ADD CONSTRAINT "FK_91d1e55b673db38c8f99d08f4d2" FOREIGN KEY (resolved_by_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


--
-- Name: maintenance_task FK_953928a930bb8d120a8c3fe0a04; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "FK_953928a930bb8d120a8c3fe0a04" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE CASCADE;


--
-- Name: order FK_962eec87d3d029c51525f259fba; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_962eec87d3d029c51525f259fba" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id);


--
-- Name: order_status_history FK_965678b54f0a0361ca72c541b20; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status_history
    ADD CONSTRAINT "FK_965678b54f0a0361ca72c541b20" FOREIGN KEY (changed_by_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


--
-- Name: cylinder_movement FK_968ad11170db2741bb5c0c47bb3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_movement
    ADD CONSTRAINT "FK_968ad11170db2741bb5c0c47bb3" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: route_batch_stop FK_972a5539c274d0faff237b4bb9f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_stop
    ADD CONSTRAINT "FK_972a5539c274d0faff237b4bb9f" FOREIGN KEY (batch_id) REFERENCES public.route_batch(batch_id) ON DELETE CASCADE;


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
-- Name: repurchase_invitation FK_a1798ae7c0a36f272fa9ec34208; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.repurchase_invitation
    ADD CONSTRAINT "FK_a1798ae7c0a36f272fa9ec34208" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE SET NULL;


--
-- Name: customer FK_a2106c82437ec332b5088caf6b1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT "FK_a2106c82437ec332b5088caf6b1" FOREIGN KEY (declared_cylinder_type_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE SET NULL;


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
-- Name: order_address_change FK_a8e249e6f7a18773fba8dba6abb; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_address_change
    ADD CONSTRAINT "FK_a8e249e6f7a18773fba8dba6abb" FOREIGN KEY (changed_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: cart_item FK_b6b2a4f1f533d89d218e70db941; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT "FK_b6b2a4f1f533d89d218e70db941" FOREIGN KEY (cart_id) REFERENCES public.cart(cart_id) ON DELETE CASCADE;


--
-- Name: module_config FK_ba2e1f43e70ba77c13d6844ee84; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_config
    ADD CONSTRAINT "FK_ba2e1f43e70ba77c13d6844ee84" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: cylinder_recovery_case FK_d6bb53d55c3556b23295d5ac5a2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_recovery_case
    ADD CONSTRAINT "FK_d6bb53d55c3556b23295d5ac5a2" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: order FK_df56039592a4bbbd3fa4a19f141; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_df56039592a4bbbd3fa4a19f141" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: cylinder_movement FK_e69720a167d0129aa6dbe492cb2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_movement
    ADD CONSTRAINT "FK_e69720a167d0129aa6dbe492cb2" FOREIGN KEY (actor_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


--
-- Name: module_config FK_e7a90d274237d2c001539efd653; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_config
    ADD CONSTRAINT "FK_e7a90d274237d2c001539efd653" FOREIGN KEY (updated_by_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


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
-- Name: cylinder_recovery_notice FK_ea6566148b8616520f5a1a7f1ad; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_recovery_notice
    ADD CONSTRAINT "FK_ea6566148b8616520f5a1a7f1ad" FOREIGN KEY (case_id) REFERENCES public.cylinder_recovery_case(case_id) ON DELETE CASCADE;


--
-- Name: repurchase_invitation FK_ec297644c2db0dab5171e00f1f1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.repurchase_invitation
    ADD CONSTRAINT "FK_ec297644c2db0dab5171e00f1f1" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: maintenance_task FK_ec96001f6fe2869ae6b40f2dc8a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "FK_ec96001f6fe2869ae6b40f2dc8a" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: order FK_f07603e96b068aae820d4590270; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_f07603e96b068aae820d4590270" FOREIGN KEY (address_id) REFERENCES public.user_address(address_id);


--
-- Name: cart FK_f091e86a234693a49084b4c2c86; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT "FK_f091e86a234693a49084b4c2c86" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: payment FK_f5221735ace059250daac9d9803; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT "FK_f5221735ace059250daac9d9803" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


--
-- Name: cylinder FK_f5b98a008ff9f846381bb5494d5; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "FK_f5b98a008ff9f846381bb5494d5" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE SET NULL;


--
-- Name: user FK_fb2e442d14add3cefbdf33c4561; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "FK_fb2e442d14add3cefbdf33c4561" FOREIGN KEY (role_id) REFERENCES public.role(role_id);


--
-- Name: cart FK_fe7495dc822eabf84bf1dc84e0f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT "FK_fe7495dc822eabf84bf1dc84e0f" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

