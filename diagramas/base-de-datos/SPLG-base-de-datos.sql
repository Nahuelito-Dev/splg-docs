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
-- Name: attachment_owner_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.attachment_owner_type_enum AS ENUM (
    'employee',
    'fuel_load',
    'traffic_fine',
    'vehicle_accident',
    'purchase_receipt',
    'stock_adjustment',
    'driver_settlement',
    'cash_movement',
    'customer_account_entry'
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
    'empty_returned',
    'retired'
);


--
-- Name: cylinder_movement_to_state_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cylinder_movement_to_state_enum AS ENUM (
    'in_depot',
    'filled',
    'dispatched',
    'with_customer',
    'empty_returned',
    'retired'
);


--
-- Name: cylinder_state_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cylinder_state_enum AS ENUM (
    'in_depot',
    'filled',
    'dispatched',
    'with_customer',
    'empty_returned',
    'retired'
);


--
-- Name: distributor_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.distributor_status_enum AS ENUM (
    'active',
    'suspended'
);


--
-- Name: employee_document_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.employee_document_type_enum AS ENUM (
    'dni',
    'passport',
    'other'
);


--
-- Name: employee_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.employee_status_enum AS ENUM (
    'active',
    'terminated'
);


--
-- Name: employee_termination_reason_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.employee_termination_reason_enum AS ENUM (
    'resignation',
    'dismissal',
    'end_of_contract',
    'retirement',
    'other'
);


--
-- Name: employment_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.employment_type_enum AS ENUM (
    'permanent',
    'fixed_term',
    'part_time',
    'contractor'
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
    'resolved',
    'discarded'
);


--
-- Name: incident_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.incident_type_enum AS ENUM (
    'damaged',
    'out_of_stock',
    'no_show',
    'unpaid_collection',
    'other'
);


--
-- Name: job_position_category_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.job_position_category_enum AS ENUM (
    'driver',
    'helper',
    'warehouse',
    'administration',
    'sales',
    'management',
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
    'expired',
    'superseded'
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
    'failed',
    'unpaid',
    'written_off'
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
-- Name: order_zone_surcharge_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.order_zone_surcharge_type_enum AS ENUM (
    'fixed',
    'percentage'
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
-- Name: purchase_order_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.purchase_order_status_enum AS ENUM (
    'draft',
    'sent',
    'partially_received',
    'received',
    'closed_short',
    'cancelled'
);


--
-- Name: purchase_payment_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.purchase_payment_status_enum AS ENUM (
    'unpaid',
    'paid'
);


--
-- Name: purchase_receipt_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.purchase_receipt_status_enum AS ENUM (
    'confirmed',
    'voided'
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
-- Name: stock_adjustment_reason_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.stock_adjustment_reason_enum AS ENUM (
    'count_correction',
    'shrinkage',
    'leak',
    'damaged',
    'lost',
    'found',
    'initial_count',
    'reconciliation'
);


--
-- Name: stock_condition_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.stock_condition_enum AS ENUM (
    'full',
    'empty',
    'defective'
);


--
-- Name: stock_location_kind_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.stock_location_kind_enum AS ENUM (
    'warehouse',
    'vehicle'
);


--
-- Name: stock_movement_reason_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.stock_movement_reason_enum AS ENUM (
    'initial_count',
    'purchase_receipt',
    'plant_empty_out',
    'truck_load',
    'truck_return',
    'delivery',
    'empty_collected',
    'transfer',
    'adjustment',
    'shrinkage',
    'condition_change',
    'reversal'
);


--
-- Name: stock_movement_reference_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.stock_movement_reference_type_enum AS ENUM (
    'order',
    'purchase_receipt',
    'truck_load',
    'stock_adjustment',
    'transfer',
    'initial'
);


--
-- Name: supplier_document_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.supplier_document_type_enum AS ENUM (
    'delivery_note',
    'invoice'
);


--
-- Name: supplier_kind_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.supplier_kind_enum AS ENUM (
    'filling_plant',
    'other'
);


--
-- Name: warehouse_kind_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.warehouse_kind_enum AS ENUM (
    'depot',
    'branch'
);


--
-- Name: audit_datos_inmutable(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.audit_datos_inmutable() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
            BEGIN
              IF TG_TABLE_NAME = 'audit' AND TG_OP = 'UPDATE' AND pg_trigger_depth() > 1 THEN
                IF (NEW.user_id IS NULL OR NEW.user_id = OLD.user_id)
                   AND (NEW.distributor_id IS NULL OR NEW.distributor_id = OLD.distributor_id)
                   AND (to_jsonb(NEW) - 'user_id' - 'distributor_id')
                     = (to_jsonb(OLD) - 'user_id' - 'distributor_id') THEN
                  RETURN NEW;
                END IF;
              END IF;
              RAISE EXCEPTION '% es de sólo escritura: no se modifican ni se borran auditorías', TG_TABLE_NAME;
            END;
            $$;


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


--
-- Name: stock_movement_inmutable(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.stock_movement_inmutable() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
      BEGIN
        RAISE EXCEPTION 'stock_movement es de sólo escritura: no se modifican ni se borran movimientos; se corrige con un contraasiento';
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
-- Name: attachment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.attachment (
    attachment_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    owner_type public.attachment_owner_type_enum NOT NULL,
    owner_id uuid NOT NULL,
    label character varying(80),
    storage_key character varying(255) NOT NULL,
    original_name character varying(255) NOT NULL,
    mime_type character varying(100) NOT NULL,
    size_bytes integer NOT NULL,
    uploaded_by_user_id uuid NOT NULL,
    uploaded_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone
);


--
-- Name: audit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit (
    audit_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    action_type_id smallint NOT NULL,
    user_id uuid,
    distributor_id uuid,
    entity character varying(60) NOT NULL,
    record_id character varying(64) NOT NULL,
    ip character varying(45),
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: audit_action_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_action_type (
    action_type_id smallint NOT NULL,
    name character varying(40) NOT NULL
);


--
-- Name: audit_detail; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_detail (
    audit_detail_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    audit_id uuid NOT NULL,
    field character varying(80) NOT NULL,
    old_value text,
    new_value text
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
    in_service_since timestamp with time zone,
    photo_key character varying(512)
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
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    photo_key character varying(512)
);


--
-- Name: coverage_zone; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.coverage_zone (
    coverage_zone_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    name character varying(120) NOT NULL,
    area public.geometry(Polygon,4326) NOT NULL,
    surcharge_value numeric(10,2) DEFAULT '0'::numeric NOT NULL,
    "isActive" boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone,
    surcharge_type public.coverage_zone_surcharge_type_enum DEFAULT 'percentage'::public.coverage_zone_surcharge_type_enum NOT NULL,
    label character varying(40),
    color character varying(7),
    valid_until timestamp with time zone,
    priority integer DEFAULT 0 NOT NULL,
    valid_from timestamp with time zone,
    CONSTRAINT "CHK_coverage_zone_surcharge" CHECK ((((surcharge_type = 'fixed'::public.coverage_zone_surcharge_type_enum) AND (surcharge_value >= (0)::numeric)) OR ((surcharge_type = 'percentage'::public.coverage_zone_surcharge_type_enum) AND (surcharge_value >= (0)::numeric) AND (surcharge_value <= (100)::numeric))))
);


--
-- Name: customer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer (
    customer_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    notification_token text,
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
    location public.geometry(Point,4326),
    "isEnabled" boolean DEFAULT true NOT NULL,
    "isAvailable" boolean DEFAULT false NOT NULL
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
    "deletedAt" timestamp with time zone,
    logo_key character varying(512)
);


--
-- Name: document_sequence; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_sequence (
    distributor_id uuid NOT NULL,
    doc_type character varying(40) NOT NULL,
    last_number integer DEFAULT 0 NOT NULL
);


--
-- Name: employee; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employee (
    employee_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    user_id uuid,
    position_id uuid NOT NULL,
    file_number character varying(20) NOT NULL,
    first_name character varying(80) NOT NULL,
    last_name character varying(80) NOT NULL,
    document_type public.employee_document_type_enum NOT NULL,
    document_number character varying(20) NOT NULL,
    cuil character varying(11),
    birth_date date,
    address_line character varying(200),
    city character varying(80),
    province character varying(80),
    postal_code character varying(10),
    phone character varying(30),
    personal_email character varying(120),
    emergency_contact_name character varying(120),
    emergency_contact_phone character varying(30),
    emergency_contact_relationship character varying(40),
    hire_date date NOT NULL,
    termination_date date,
    termination_reason public.employee_termination_reason_enum,
    employment_type public.employment_type_enum NOT NULL,
    status public.employee_status_enum DEFAULT 'active'::public.employee_status_enum NOT NULL,
    bank_cbu character varying(22),
    notes text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone,
    photo_key character varying(512),
    CONSTRAINT "CHK_employee_status_termination" CHECK (((status = 'terminated'::public.employee_status_enum) = (termination_date IS NOT NULL))),
    CONSTRAINT "CHK_employee_termination_date" CHECK (((termination_date IS NULL) OR (termination_date >= hire_date)))
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
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    photo_key character varying(512),
    average_unit_cost numeric(12,2)
);


--
-- Name: gas_cylinder_promotion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.gas_cylinder_promotion (
    promotion_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    quantity integer NOT NULL,
    discount_percentage numeric(5,2) NOT NULL,
    "deletedAt" timestamp with time zone,
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
    moment public.incident_moment_enum,
    photo_key character varying(512)
);


--
-- Name: job_position; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_position (
    position_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    name character varying(80) NOT NULL,
    category public.job_position_category_enum NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone
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
-- Name: maintenance_task_attachment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.maintenance_task_attachment (
    attachment_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    task_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    storage_key character varying(255) NOT NULL,
    original_name character varying(255) NOT NULL,
    mime_type character varying(100) NOT NULL,
    size_bytes integer NOT NULL,
    uploaded_by_user_id uuid NOT NULL,
    uploaded_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone
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
    "acceptedAt" timestamp with time zone,
    "onTheWayAt" timestamp with time zone,
    "deliveredAt" timestamp with time zone,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "cancellationReason" text,
    "gatewayPaymentId" character varying(100),
    "deliveryCode" character varying(12),
    receiver_name character varying(120),
    receiver_document character varying(20),
    receiver_relationship character varying(40),
    delivery_mode public.order_delivery_mode_enum DEFAULT 'standard'::public.order_delivery_mode_enum NOT NULL,
    "deliveryPoint" public.geometry(Point,4326),
    coverage_zone_id uuid,
    zone_name character varying(120),
    zone_surcharge_type public.order_zone_surcharge_type_enum,
    zone_surcharge_value numeric(10,2),
    zone_surcharge_amount numeric(10,2) DEFAULT '0'::numeric NOT NULL,
    subtotal_items numeric(10,2) NOT NULL,
    vehicle_car_id uuid,
    vehicle_patent character varying(20),
    vehicle_brand character varying(50),
    vehicle_model character varying(50),
    payment_confirmed_at timestamp with time zone,
    payment_confirmed_by uuid,
    payment_resolution_note text,
    payment_resolved_at timestamp with time zone,
    payment_resolved_by uuid
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
-- Name: purchase_order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchase_order (
    purchase_order_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    number integer NOT NULL,
    supplier_id uuid NOT NULL,
    destination_warehouse_id uuid NOT NULL,
    status public.purchase_order_status_enum DEFAULT 'draft'::public.purchase_order_status_enum NOT NULL,
    issued_at timestamp with time zone,
    expected_date date,
    total_amount numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    cancel_reason text,
    notes text,
    created_by_user_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    close_reason text
);


--
-- Name: purchase_order_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchase_order_item (
    item_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    purchase_order_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    quantity integer NOT NULL,
    unit_cost numeric(12,2) NOT NULL,
    empties_to_exchange integer DEFAULT 0 NOT NULL,
    received_quantity integer DEFAULT 0 NOT NULL,
    CONSTRAINT "CHK_purchase_order_item_cantidad" CHECK ((quantity > 0)),
    CONSTRAINT "CHK_purchase_order_item_costo" CHECK ((unit_cost >= (0)::numeric)),
    CONSTRAINT "CHK_purchase_order_item_recibido" CHECK (((received_quantity >= 0) AND (received_quantity <= quantity))),
    CONSTRAINT "CHK_purchase_order_item_vacios" CHECK ((empties_to_exchange >= 0))
);


--
-- Name: purchase_receipt; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchase_receipt (
    receipt_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    number integer NOT NULL,
    supplier_id uuid NOT NULL,
    purchase_order_id uuid,
    warehouse_id uuid NOT NULL,
    supplier_document_type public.supplier_document_type_enum NOT NULL,
    supplier_document_number character varying(30) NOT NULL,
    received_at timestamp with time zone NOT NULL,
    received_by_user_id uuid NOT NULL,
    total_amount numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    payment_status public.purchase_payment_status_enum DEFAULT 'unpaid'::public.purchase_payment_status_enum NOT NULL,
    cash_movement_id uuid,
    status public.purchase_receipt_status_enum DEFAULT 'confirmed'::public.purchase_receipt_status_enum NOT NULL,
    void_reason text,
    voided_at timestamp with time zone,
    voided_by_user_id uuid,
    batch_id uuid NOT NULL,
    void_batch_id uuid,
    notes text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: purchase_receipt_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchase_receipt_item (
    item_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    receipt_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    quantity_full integer NOT NULL,
    quantity_empty_out integer DEFAULT 0 NOT NULL,
    unit_cost numeric(12,2) NOT NULL,
    previous_average_cost numeric(12,2),
    previous_on_hand integer,
    CONSTRAINT "CHK_purchase_receipt_item_cantidades" CHECK (((quantity_full >= 0) AND (quantity_empty_out >= 0) AND ((quantity_full + quantity_empty_out) > 0))),
    CONSTRAINT "CHK_purchase_receipt_item_costo" CHECK ((unit_cost >= (0)::numeric))
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
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    hidden boolean DEFAULT false NOT NULL,
    hidden_reason text,
    hidden_at timestamp with time zone,
    hidden_by_user_id uuid
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
    "updatedAt" timestamp with time zone DEFAULT now(),
    "deletedAt" timestamp with time zone
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
-- Name: stock_adjustment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_adjustment (
    adjustment_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    number integer NOT NULL,
    location_id uuid NOT NULL,
    reason public.stock_adjustment_reason_enum NOT NULL,
    notes text NOT NULL,
    batch_id uuid NOT NULL,
    created_by_user_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: stock_adjustment_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_adjustment_item (
    item_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    adjustment_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    condition public.stock_condition_enum NOT NULL,
    quantity_delta integer NOT NULL,
    CONSTRAINT "CHK_stock_adjustment_item_variacion" CHECK ((quantity_delta <> 0))
);


--
-- Name: stock_balance; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_balance (
    balance_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    location_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    condition public.stock_condition_enum NOT NULL,
    quantity integer DEFAULT 0 NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_stock_balance_no_negativo" CHECK ((quantity >= 0))
);


--
-- Name: stock_location; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_location (
    location_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    kind public.stock_location_kind_enum NOT NULL,
    warehouse_id uuid,
    car_id uuid,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_stock_location_kind" CHECK (((kind = 'warehouse'::public.stock_location_kind_enum) = (warehouse_id IS NOT NULL))),
    CONSTRAINT "CHK_stock_location_one_owner" CHECK ((num_nonnulls(warehouse_id, car_id) = 1))
);


--
-- Name: stock_movement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_movement (
    movement_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    batch_id uuid NOT NULL,
    quantity integer NOT NULL,
    from_location_id uuid,
    from_condition public.stock_condition_enum,
    to_location_id uuid,
    to_condition public.stock_condition_enum,
    reason public.stock_movement_reason_enum NOT NULL,
    reference_type public.stock_movement_reference_type_enum NOT NULL,
    reference_id uuid,
    reversed_movement_id uuid,
    notes character varying(300),
    actor_user_id uuid,
    occurred_at timestamp with time zone DEFAULT now() NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_stock_movement_cantidad" CHECK ((quantity > 0)),
    CONSTRAINT "CHK_stock_movement_destino_coherente" CHECK (((to_location_id IS NULL) = (to_condition IS NULL))),
    CONSTRAINT "CHK_stock_movement_origen_coherente" CHECK (((from_location_id IS NULL) = (from_condition IS NULL))),
    CONSTRAINT "CHK_stock_movement_origen_o_destino" CHECK (((from_location_id IS NOT NULL) OR (to_location_id IS NOT NULL)))
);


--
-- Name: stock_reconciliation_alert; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_reconciliation_alert (
    distributor_id uuid NOT NULL,
    signature character varying(64) NOT NULL,
    alerted_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: stock_threshold; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_threshold (
    threshold_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    warehouse_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    min_full integer NOT NULL,
    alerted_at timestamp with time zone,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_stock_threshold_minimo" CHECK ((min_full >= 0))
);


--
-- Name: storage_orphan; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.storage_orphan (
    orphan_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    storage_key character varying(512) NOT NULL,
    attempts integer DEFAULT 0 NOT NULL,
    last_error text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    kind character varying(10) DEFAULT 'remove'::character varying NOT NULL,
    status character varying(10) DEFAULT 'pending'::character varying NOT NULL,
    next_attempt_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: supplier; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.supplier (
    supplier_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    business_name character varying(120) NOT NULL,
    cuit character varying(11) NOT NULL,
    kind public.supplier_kind_enum DEFAULT 'other'::public.supplier_kind_enum NOT NULL,
    contact_name character varying(80),
    phone character varying(30),
    email character varying(120),
    address text,
    payment_terms_days integer,
    is_active boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone
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
    "deletedAt" timestamp with time zone,
    photo_key character varying(512)
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
-- Name: vehicle_assignment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicle_assignment (
    assignment_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    car_id uuid NOT NULL,
    delivery_id uuid NOT NULL,
    assigned_at timestamp with time zone NOT NULL,
    released_at timestamp with time zone,
    assigned_by_user_id uuid,
    released_by_user_id uuid,
    note text
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
-- Name: warehouse; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.warehouse (
    warehouse_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    name character varying(80) NOT NULL,
    code character varying(12) NOT NULL,
    kind public.warehouse_kind_enum DEFAULT 'depot'::public.warehouse_kind_enum NOT NULL,
    address text,
    is_default boolean DEFAULT false NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone
);


--
-- Name: vehicle_assignment PK_03cbc11f348efffa59570945343; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "PK_03cbc11f348efffa59570945343" PRIMARY KEY (assignment_id);


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
-- Name: stock_threshold PK_111cca2010115947ad3ed0a00d5; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_threshold
    ADD CONSTRAINT "PK_111cca2010115947ad3ed0a00d5" PRIMARY KEY (threshold_id);


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
-- Name: stock_movement PK_208ac76bb0d2e300ce89781b22b; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "PK_208ac76bb0d2e300ce89781b22b" PRIMARY KEY (movement_id);


--
-- Name: purchase_order_item PK_279be0517e992507405a8370859; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_item
    ADD CONSTRAINT "PK_279be0517e992507405a8370859" PRIMARY KEY (item_id);


--
-- Name: attachment PK_31d5367aee6b3ad16c69cce1cde; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attachment
    ADD CONSTRAINT "PK_31d5367aee6b3ad16c69cce1cde" PRIMARY KEY (attachment_id);


--
-- Name: maintenance_task_attachment PK_368cf5b7606c8ff95e4b320c81d; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task_attachment
    ADD CONSTRAINT "PK_368cf5b7606c8ff95e4b320c81d" PRIMARY KEY (attachment_id);


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
-- Name: stock_balance PK_47028cd798909484a9f5f9b0bd2; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_balance
    ADD CONSTRAINT "PK_47028cd798909484a9f5f9b0bd2" PRIMARY KEY (balance_id);


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
-- Name: audit_action_type PK_66dcf5c5aab6bba8e40c9b16e86; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_action_type
    ADD CONSTRAINT "PK_66dcf5c5aab6bba8e40c9b16e86" PRIMARY KEY (action_type_id);


--
-- Name: gas_cylinder PK_6768507f2214b15ab4653ef28c9; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder
    ADD CONSTRAINT "PK_6768507f2214b15ab4653ef28c9" PRIMARY KEY (gas_cylinder_id);


--
-- Name: purchase_receipt_item PK_7337109e82b7ce3f2b240f3cf01; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt_item
    ADD CONSTRAINT "PK_7337109e82b7ce3f2b240f3cf01" PRIMARY KEY (item_id);


--
-- Name: user PK_758b8ce7c18b9d347461b30228d; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "PK_758b8ce7c18b9d347461b30228d" PRIMARY KEY (user_id);


--
-- Name: audit PK_75ad7632b08b4cfadec337a7c8d; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit
    ADD CONSTRAINT "PK_75ad7632b08b4cfadec337a7c8d" PRIMARY KEY (audit_id);


--
-- Name: storage_orphan PK_7875e03a159e8f5bbc0ddc30c1a; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.storage_orphan
    ADD CONSTRAINT "PK_7875e03a159e8f5bbc0ddc30c1a" PRIMARY KEY (orphan_id);


--
-- Name: incident PK_78e450f2684a57c80de36e5d411; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.incident
    ADD CONSTRAINT "PK_78e450f2684a57c80de36e5d411" PRIMARY KEY (incident_id);


--
-- Name: purchase_receipt PK_84843cd0babb399d9c6df92e785; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "PK_84843cd0babb399d9c6df92e785" PRIMARY KEY (receipt_id);


--
-- Name: warehouse PK_897d6a7341d8b835d3368b91b8c; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.warehouse
    ADD CONSTRAINT "PK_897d6a7341d8b835d3368b91b8c" PRIMARY KEY (warehouse_id);


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
-- Name: job_position PK_b76336b3450074bc7b4aa846b1e; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_position
    ADD CONSTRAINT "PK_b76336b3450074bc7b4aa846b1e" PRIMARY KEY (position_id);


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
-- Name: audit_detail PK_d7889dea20a563a7248592b9860; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_detail
    ADD CONSTRAINT "PK_d7889dea20a563a7248592b9860" PRIMARY KEY (audit_detail_id);


--
-- Name: route_batch_stop PK_d9ba16fd7aeaeb044ce2a375886; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_stop
    ADD CONSTRAINT "PK_d9ba16fd7aeaeb044ce2a375886" PRIMARY KEY (stop_id);


--
-- Name: stock_location PK_db70b5a5252bd3e2b11d488746c; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT "PK_db70b5a5252bd3e2b11d488746c" PRIMARY KEY (location_id);


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
-- Name: document_sequence PK_document_sequence; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_sequence
    ADD CONSTRAINT "PK_document_sequence" PRIMARY KEY (distributor_id, doc_type);


--
-- Name: supplier PK_e0f8ee60663218082b83251cd85; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT "PK_e0f8ee60663218082b83251cd85" PRIMARY KEY (supplier_id);


--
-- Name: claims PK_e8c55807de8dde683de34399da3; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "PK_e8c55807de8dde683de34399da3" PRIMARY KEY (claim_id);


--
-- Name: stock_adjustment PK_e922ad5f08b46b85d6a82156378; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment
    ADD CONSTRAINT "PK_e922ad5f08b46b85d6a82156378" PRIMARY KEY (adjustment_id);


--
-- Name: stock_adjustment_item PK_ed34c9fcbcbed4fe6d1bcff37c2; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment_item
    ADD CONSTRAINT "PK_ed34c9fcbcbed4fe6d1bcff37c2" PRIMARY KEY (item_id);


--
-- Name: order_item PK_f91441b7e69922a51a0d2917107; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT "PK_f91441b7e69922a51a0d2917107" PRIMARY KEY (order_item_id);


--
-- Name: employee PK_f9d306b968b54923539b3936b03; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT "PK_f9d306b968b54923539b3936b03" PRIMARY KEY (employee_id);


--
-- Name: purchase_order PK_fab0d2c491acac8ad11df9c5c35; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "PK_fab0d2c491acac8ad11df9c5c35" PRIMARY KEY (purchase_order_id);


--
-- Name: maintenance_plan PK_faeec4a9735696ac9d1c915b380; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_plan
    ADD CONSTRAINT "PK_faeec4a9735696ac9d1c915b380" PRIMARY KEY (plan_id);


--
-- Name: stock_reconciliation_alert PK_stock_reconciliation_alert; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_reconciliation_alert
    ADD CONSTRAINT "PK_stock_reconciliation_alert" PRIMARY KEY (distributor_id);


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
-- Name: user UQ_40fe3048b17f675b652c1999270; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "UQ_40fe3048b17f675b652c1999270" UNIQUE (firebase_uid);


--
-- Name: storage_orphan UQ_79763cafe43e9dcf31ea86b6f59; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.storage_orphan
    ADD CONSTRAINT "UQ_79763cafe43e9dcf31ea86b6f59" UNIQUE (storage_key);


--
-- Name: audit_action_type UQ_920dea5fea6e965ccf619575f55; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_action_type
    ADD CONSTRAINT "UQ_920dea5fea6e965ccf619575f55" UNIQUE (name);


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
-- Name: gas_cylinder UQ_gas_cylinder_distribuidora_tipo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder
    ADD CONSTRAINT "UQ_gas_cylinder_distribuidora_tipo" UNIQUE (distributor_id, type);


--
-- Name: module_config UQ_module_config_distributor_module; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_config
    ADD CONSTRAINT "UQ_module_config_distributor_module" UNIQUE (distributor_id, module);


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
-- Name: IDX_07f53564ec7d34fc7e69b96cab; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_07f53564ec7d34fc7e69b96cab" ON public.maintenance_task_attachment USING btree (distributor_id);


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
-- Name: IDX_1f986e62c32ac5ee2d8d7eb133; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_1f986e62c32ac5ee2d8d7eb133" ON public.vehicle_assignment USING btree (distributor_id);


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
-- Name: IDX_70d35b9e83fa8fca69e685f548; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_70d35b9e83fa8fca69e685f548" ON public.attachment USING btree (distributor_id, owner_type, owner_id);


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
-- Name: IDX_audit_detail_audit; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_detail_audit" ON public.audit_detail USING btree (audit_id);


--
-- Name: IDX_audit_detail_order_anterior; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_detail_order_anterior" ON public.audit_detail USING btree (old_value) WHERE ((field)::text = 'orderId'::text);


--
-- Name: IDX_audit_detail_order_nuevo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_detail_order_nuevo" ON public.audit_detail USING btree (new_value) WHERE ((field)::text = 'orderId'::text);


--
-- Name: IDX_audit_distributor_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_distributor_created_at" ON public.audit USING btree (distributor_id, created_at);


--
-- Name: IDX_audit_entity_record; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_entity_record" ON public.audit USING btree (entity, record_id);


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
-- Name: IDX_audit_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_audit_user" ON public.audit USING btree (user_id);


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
-- Name: IDX_employee_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_employee_name" ON public.employee USING btree (distributor_id, last_name, first_name);


--
-- Name: IDX_employee_position; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_employee_position" ON public.employee USING btree (position_id);


--
-- Name: IDX_employee_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_employee_status" ON public.employee USING btree (distributor_id, status);


--
-- Name: IDX_f437a76442f23c89ad7652b2a4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_f437a76442f23c89ad7652b2a4" ON public."order" USING btree ("deliveredAt");


--
-- Name: IDX_f5221735ace059250daac9d980; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_f5221735ace059250daac9d980" ON public.payment USING btree (order_id);


--
-- Name: IDX_f5df1954571306276a5db7930f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_f5df1954571306276a5db7930f" ON public.rating USING btree (hidden);


--
-- Name: IDX_f63c2b78c253c8c92398d88fd5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_f63c2b78c253c8c92398d88fd5" ON public.job_position USING btree (distributor_id);


--
-- Name: IDX_purchase_order_estado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_purchase_order_estado" ON public.purchase_order USING btree (distributor_id, status);


--
-- Name: IDX_purchase_order_item_garrafa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_purchase_order_item_garrafa" ON public.purchase_order_item USING btree (gas_cylinder_id);


--
-- Name: IDX_purchase_order_proveedor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_purchase_order_proveedor" ON public.purchase_order USING btree (supplier_id);


--
-- Name: IDX_purchase_receipt_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_purchase_receipt_fecha" ON public.purchase_receipt USING btree (distributor_id, received_at);


--
-- Name: IDX_purchase_receipt_item_garrafa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_purchase_receipt_item_garrafa" ON public.purchase_receipt_item USING btree (gas_cylinder_id);


--
-- Name: IDX_purchase_receipt_orden; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_purchase_receipt_orden" ON public.purchase_receipt USING btree (purchase_order_id);


--
-- Name: IDX_purchase_receipt_proveedor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_purchase_receipt_proveedor" ON public.purchase_receipt USING btree (supplier_id);


--
-- Name: IDX_stock_adjustment_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_adjustment_fecha" ON public.stock_adjustment USING btree (distributor_id, "createdAt");


--
-- Name: IDX_stock_adjustment_ubicacion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_adjustment_ubicacion" ON public.stock_adjustment USING btree (location_id);


--
-- Name: IDX_stock_balance_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_balance_distributor" ON public.stock_balance USING btree (distributor_id);


--
-- Name: IDX_stock_balance_gas_cylinder; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_balance_gas_cylinder" ON public.stock_balance USING btree (gas_cylinder_id);


--
-- Name: IDX_stock_location_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_location_distributor" ON public.stock_location USING btree (distributor_id);


--
-- Name: IDX_stock_movement_destino; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_movement_destino" ON public.stock_movement USING btree (to_location_id);


--
-- Name: IDX_stock_movement_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_movement_fecha" ON public.stock_movement USING btree (distributor_id, occurred_at);


--
-- Name: IDX_stock_movement_garrafa_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_movement_garrafa_fecha" ON public.stock_movement USING btree (gas_cylinder_id, occurred_at);


--
-- Name: IDX_stock_movement_lote; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_movement_lote" ON public.stock_movement USING btree (batch_id);


--
-- Name: IDX_stock_movement_origen; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_movement_origen" ON public.stock_movement USING btree (from_location_id);


--
-- Name: IDX_stock_movement_referencia; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_movement_referencia" ON public.stock_movement USING btree (reference_type, reference_id);


--
-- Name: IDX_stock_threshold_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_threshold_distributor" ON public.stock_threshold USING btree (distributor_id);


--
-- Name: IDX_supplier_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_supplier_distributor" ON public.supplier USING btree (distributor_id);


--
-- Name: IDX_user_email_lower; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_user_email_lower" ON public."user" USING btree (lower((email)::text));


--
-- Name: IDX_warehouse_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_warehouse_distributor" ON public.warehouse USING btree (distributor_id);


--
-- Name: UQ_admin_user; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_admin_user" ON public.admin USING btree (user_id);


--
-- Name: UQ_car_patente_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_car_patente_vigente" ON public.car USING btree (car_patent) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_employee_cuil_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_employee_cuil_vigente" ON public.employee USING btree (distributor_id, cuil) WHERE ((cuil IS NOT NULL) AND ("deletedAt" IS NULL));


--
-- Name: UQ_employee_document_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_employee_document_vigente" ON public.employee USING btree (distributor_id, document_number) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_employee_file_number_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_employee_file_number_vigente" ON public.employee USING btree (distributor_id, file_number) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_employee_user_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_employee_user_vigente" ON public.employee USING btree (user_id) WHERE ((user_id IS NOT NULL) AND ("deletedAt" IS NULL));


--
-- Name: UQ_incident_cobro_impago; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_incident_cobro_impago" ON public.incident USING btree (order_id) WHERE ((type = 'unpaid_collection'::public.incident_type_enum) AND (status = ANY (ARRAY['open'::public.incident_status_enum, 'resolved'::public.incident_status_enum])));


--
-- Name: UQ_job_position_name_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_job_position_name_vigente" ON public.job_position USING btree (distributor_id, lower((name)::text)) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_promocion_producto_cantidad; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_promocion_producto_cantidad" ON public.gas_cylinder_promotion USING btree (gas_cylinder_id, quantity) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_purchase_order_item_garrafa; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_purchase_order_item_garrafa" ON public.purchase_order_item USING btree (purchase_order_id, gas_cylinder_id);


--
-- Name: UQ_purchase_order_numero; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_purchase_order_numero" ON public.purchase_order USING btree (distributor_id, number);


--
-- Name: UQ_purchase_receipt_documento_proveedor; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_purchase_receipt_documento_proveedor" ON public.purchase_receipt USING btree (distributor_id, supplier_id, supplier_document_type, supplier_document_number);


--
-- Name: UQ_purchase_receipt_item_garrafa; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_purchase_receipt_item_garrafa" ON public.purchase_receipt_item USING btree (receipt_id, gas_cylinder_id);


--
-- Name: UQ_purchase_receipt_numero; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_purchase_receipt_numero" ON public.purchase_receipt USING btree (distributor_id, number);


--
-- Name: UQ_role_type_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_role_type_vigente" ON public.role USING btree (type) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_stock_adjustment_item_garrafa_condicion; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_stock_adjustment_item_garrafa_condicion" ON public.stock_adjustment_item USING btree (adjustment_id, gas_cylinder_id, condition);


--
-- Name: UQ_stock_adjustment_numero; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_stock_adjustment_numero" ON public.stock_adjustment USING btree (distributor_id, number);


--
-- Name: UQ_stock_balance_ubicacion_garrafa_condicion; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_stock_balance_ubicacion_garrafa_condicion" ON public.stock_balance USING btree (location_id, gas_cylinder_id, condition);


--
-- Name: UQ_stock_location_car; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_stock_location_car" ON public.stock_location USING btree (car_id);


--
-- Name: UQ_stock_location_warehouse; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_stock_location_warehouse" ON public.stock_location USING btree (warehouse_id);


--
-- Name: UQ_stock_movement_contraasiento; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_stock_movement_contraasiento" ON public.stock_movement USING btree (reversed_movement_id) WHERE (reversed_movement_id IS NOT NULL);


--
-- Name: UQ_stock_movement_pedido; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_stock_movement_pedido" ON public.stock_movement USING btree (reference_id, gas_cylinder_id, reason) WHERE ((reference_type = 'order'::public.stock_movement_reference_type_enum) AND (reason <> 'reversal'::public.stock_movement_reason_enum));


--
-- Name: UQ_stock_threshold_deposito_garrafa; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_stock_threshold_deposito_garrafa" ON public.stock_threshold USING btree (warehouse_id, gas_cylinder_id);


--
-- Name: UQ_supplier_cuit_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_supplier_cuit_vigente" ON public.supplier USING btree (distributor_id, cuit) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_vehicle_assignment_car_abierta; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_vehicle_assignment_car_abierta" ON public.vehicle_assignment USING btree (car_id) WHERE (released_at IS NULL);


--
-- Name: UQ_vehicle_assignment_delivery_abierta; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_vehicle_assignment_delivery_abierta" ON public.vehicle_assignment USING btree (delivery_id) WHERE (released_at IS NULL);


--
-- Name: UQ_warehouse_code_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_warehouse_code_vigente" ON public.warehouse USING btree (distributor_id, code) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_warehouse_default_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_warehouse_default_vigente" ON public.warehouse USING btree (distributor_id) WHERE (is_default AND ("deletedAt" IS NULL));


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
-- Name: audit_detail audit_detail_inmutable; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER audit_detail_inmutable BEFORE DELETE OR UPDATE ON public.audit_detail FOR EACH ROW EXECUTE FUNCTION public.audit_datos_inmutable();


--
-- Name: audit audit_inmutable; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER audit_inmutable BEFORE DELETE OR UPDATE ON public.audit FOR EACH ROW EXECUTE FUNCTION public.audit_datos_inmutable();


--
-- Name: audit_log audit_log_inmutable; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER audit_log_inmutable BEFORE DELETE OR UPDATE ON public.audit_log FOR EACH ROW EXECUTE FUNCTION public.audit_log_inmutable();


--
-- Name: stock_movement stock_movement_inmutable; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER stock_movement_inmutable BEFORE DELETE OR UPDATE ON public.stock_movement FOR EACH ROW EXECUTE FUNCTION public.stock_movement_inmutable();


--
-- Name: maintenance_task_attachment FK_07f53564ec7d34fc7e69b96cabf; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task_attachment
    ADD CONSTRAINT "FK_07f53564ec7d34fc7e69b96cabf" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: stock_location FK_088aef530fb37a7a19c6b9b4a39; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT "FK_088aef530fb37a7a19c6b9b4a39" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: attachment FK_0e9e069d0e8d22fab610a465c16; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attachment
    ADD CONSTRAINT "FK_0e9e069d0e8d22fab610a465c16" FOREIGN KEY (uploaded_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: vehicle_assignment FK_10efb252b7fde3ea22e9151b677; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "FK_10efb252b7fde3ea22e9151b677" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE CASCADE;


--
-- Name: stock_threshold FK_1156a89b5afe382c53f0a156649; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_threshold
    ADD CONSTRAINT "FK_1156a89b5afe382c53f0a156649" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: order_dispatch_offer FK_1231f4249963aa2efb93749a8ee; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_dispatch_offer
    ADD CONSTRAINT "FK_1231f4249963aa2efb93749a8ee" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE;


--
-- Name: purchase_order FK_135e724d2360c7c75d6ea398636; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "FK_135e724d2360c7c75d6ea398636" FOREIGN KEY (destination_warehouse_id) REFERENCES public.warehouse(warehouse_id) ON DELETE RESTRICT;


--
-- Name: stock_movement FK_17c6850bf48d727614da1067ed2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_17c6850bf48d727614da1067ed2" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: repurchase_invitation FK_17f0b53699f596f5eb43c0374f4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.repurchase_invitation
    ADD CONSTRAINT "FK_17f0b53699f596f5eb43c0374f4" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: audit_detail FK_1836695bfd4e04a29b66022fff1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_detail
    ADD CONSTRAINT "FK_1836695bfd4e04a29b66022fff1" FOREIGN KEY (audit_id) REFERENCES public.audit(audit_id) ON DELETE RESTRICT;


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
-- Name: purchase_order_item FK_1c77f592d2af177be137dac042a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_item
    ADD CONSTRAINT "FK_1c77f592d2af177be137dac042a" FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_order(purchase_order_id) ON DELETE CASCADE;


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
-- Name: order FK_1ec11b9220a926133a2e15dad92; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_1ec11b9220a926133a2e15dad92" FOREIGN KEY (coverage_zone_id) REFERENCES public.coverage_zone(coverage_zone_id) ON DELETE SET NULL;


--
-- Name: vehicle_assignment FK_1f986e62c32ac5ee2d8d7eb1330; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "FK_1f986e62c32ac5ee2d8d7eb1330" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: cylinder_movement FK_2130833c25a6c8ef1a1bf119ed0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_movement
    ADD CONSTRAINT "FK_2130833c25a6c8ef1a1bf119ed0" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE SET NULL;


--
-- Name: purchase_order FK_21c76d5dfdb1773bc03cc6db1f1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "FK_21c76d5dfdb1773bc03cc6db1f1" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: attachment FK_2a226377b800631ab8142a2fe8c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attachment
    ADD CONSTRAINT "FK_2a226377b800631ab8142a2fe8c" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: vehicle_usage_log FK_2eb120806e084673aa3ed255648; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_usage_log
    ADD CONSTRAINT "FK_2eb120806e084673aa3ed255648" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE CASCADE;


--
-- Name: stock_adjustment_item FK_2fa4ce3625472a3239024cc8312; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment_item
    ADD CONSTRAINT "FK_2fa4ce3625472a3239024cc8312" FOREIGN KEY (adjustment_id) REFERENCES public.stock_adjustment(adjustment_id) ON DELETE CASCADE;


--
-- Name: cylinder_recovery_case FK_32fe6a642ad74004e88561b07aa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_recovery_case
    ADD CONSTRAINT "FK_32fe6a642ad74004e88561b07aa" FOREIGN KEY (cylinder_id) REFERENCES public.cylinder(cylinder_id) ON DELETE CASCADE;


--
-- Name: stock_balance FK_32ff768a1b319c39cf48678a0af; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_balance
    ADD CONSTRAINT "FK_32ff768a1b319c39cf48678a0af" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: purchase_order FK_3dacab5c4a43cecc0e48f5edb12; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "FK_3dacab5c4a43cecc0e48f5edb12" FOREIGN KEY (supplier_id) REFERENCES public.supplier(supplier_id) ON DELETE RESTRICT;


--
-- Name: rating FK_3e5a121d120740dfd4ffa01164b; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_3e5a121d120740dfd4ffa01164b" FOREIGN KEY (hidden_by_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


--
-- Name: stock_balance FK_425c43cce61e9a14028ec1115d1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_balance
    ADD CONSTRAINT "FK_425c43cce61e9a14028ec1115d1" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


--
-- Name: route_batch_offer FK_473c8590cc59607b872737c10e7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.route_batch_offer
    ADD CONSTRAINT "FK_473c8590cc59607b872737c10e7" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE CASCADE;


--
-- Name: employee FK_498ca175e44d448913f05298825; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT "FK_498ca175e44d448913f05298825" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: stock_location FK_4b7804c17f9702172ce5c8807d9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT "FK_4b7804c17f9702172ce5c8807d9" FOREIGN KEY (warehouse_id) REFERENCES public.warehouse(warehouse_id) ON DELETE RESTRICT;


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
-- Name: stock_threshold FK_529ba90fe05ac147b100ec4df62; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_threshold
    ADD CONSTRAINT "FK_529ba90fe05ac147b100ec4df62" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


--
-- Name: cylinder_inspection FK_531df2a7a7ab3fda4f1591e80d6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_inspection
    ADD CONSTRAINT "FK_531df2a7a7ab3fda4f1591e80d6" FOREIGN KEY (cylinder_id) REFERENCES public.cylinder(cylinder_id) ON DELETE CASCADE;


--
-- Name: stock_movement FK_55497d12338255dc611b2f4fea1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_55497d12338255dc611b2f4fea1" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


--
-- Name: stock_adjustment FK_5579346ced7a6a447d8dee9bc27; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment
    ADD CONSTRAINT "FK_5579346ced7a6a447d8dee9bc27" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: claims FK_573f53b0981b244cd25223e3ce7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "FK_573f53b0981b244cd25223e3ce7" FOREIGN KEY (order_id) REFERENCES public."order"(order_id);


--
-- Name: vehicle_assignment FK_57f3c92c944f83e9d5d9fb24257; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "FK_57f3c92c944f83e9d5d9fb24257" FOREIGN KEY (released_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: purchase_receipt FK_655cac7fe6e17056c412e0164d0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_655cac7fe6e17056c412e0164d0" FOREIGN KEY (warehouse_id) REFERENCES public.warehouse(warehouse_id) ON DELETE RESTRICT;


--
-- Name: employee FK_6ab3ec557a640017d53ac0e0ab7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT "FK_6ab3ec557a640017d53ac0e0ab7" FOREIGN KEY (position_id) REFERENCES public.job_position(position_id) ON DELETE RESTRICT;


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
-- Name: stock_adjustment FK_86f79cf831d762c7171cd5c5e17; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment
    ADD CONSTRAINT "FK_86f79cf831d762c7171cd5c5e17" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: warehouse FK_8ad23df5bd4c6cd8260cfd1e077; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.warehouse
    ADD CONSTRAINT "FK_8ad23df5bd4c6cd8260cfd1e077" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: purchase_receipt_item FK_9309591adbb21562263e935c340; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt_item
    ADD CONSTRAINT "FK_9309591adbb21562263e935c340" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


--
-- Name: maintenance_task FK_953928a930bb8d120a8c3fe0a04; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "FK_953928a930bb8d120a8c3fe0a04" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE CASCADE;


--
-- Name: supplier FK_953a1f52f2a158e012b00e2627d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT "FK_953a1f52f2a158e012b00e2627d" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: stock_movement FK_9fdaeb1da2e012874563f44702c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_9fdaeb1da2e012874563f44702c" FOREIGN KEY (actor_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: audit FK_9ffdecf0e48efaf0ae09b844d43; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit
    ADD CONSTRAINT "FK_9ffdecf0e48efaf0ae09b844d43" FOREIGN KEY (action_type_id) REFERENCES public.audit_action_type(action_type_id) ON DELETE RESTRICT;


--
-- Name: maintenance_task_attachment FK_a13e7424735660fa5a1865781c6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task_attachment
    ADD CONSTRAINT "FK_a13e7424735660fa5a1865781c6" FOREIGN KEY (uploaded_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: purchase_order_item FK_a4196dc0466b5156def25a8ee12; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_item
    ADD CONSTRAINT "FK_a4196dc0466b5156def25a8ee12" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


--
-- Name: order FK_a4743951fe3b697adf8ce898cf4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_a4743951fe3b697adf8ce898cf4" FOREIGN KEY (time_slot_id) REFERENCES public.time_slot(time_slot_id);


--
-- Name: purchase_receipt FK_a5906b092909ffdf5c1a75b308b; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_a5906b092909ffdf5c1a75b308b" FOREIGN KEY (supplier_id) REFERENCES public.supplier(supplier_id) ON DELETE RESTRICT;


--
-- Name: stock_movement FK_a659cb2aa061b376744c6cb9029; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_a659cb2aa061b376744c6cb9029" FOREIGN KEY (to_location_id) REFERENCES public.stock_location(location_id) ON DELETE RESTRICT;


--
-- Name: vehicle_assignment FK_a7cb484055004c370b38d80e880; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "FK_a7cb484055004c370b38d80e880" FOREIGN KEY (assigned_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: purchase_receipt_item FK_b391d5552738cae006c0b9bf801; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt_item
    ADD CONSTRAINT "FK_b391d5552738cae006c0b9bf801" FOREIGN KEY (receipt_id) REFERENCES public.purchase_receipt(receipt_id) ON DELETE CASCADE;


--
-- Name: rating FK_b46b63fc1ddf2135e1ed37069a9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_b46b63fc1ddf2135e1ed37069a9" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: stock_adjustment_item FK_b5df54839d2bc61c3be8207b4ff; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment_item
    ADD CONSTRAINT "FK_b5df54839d2bc61c3be8207b4ff" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


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
-- Name: purchase_order FK_c00afbc3e2836ac46be7c45ca78; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "FK_c00afbc3e2836ac46be7c45ca78" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: audit FK_c0cfc23f3e46b9aaf5a40254330; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit
    ADD CONSTRAINT "FK_c0cfc23f3e46b9aaf5a40254330" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


--
-- Name: stock_adjustment FK_c5705d3d9d138fdefd333817dd1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment
    ADD CONSTRAINT "FK_c5705d3d9d138fdefd333817dd1" FOREIGN KEY (location_id) REFERENCES public.stock_location(location_id) ON DELETE RESTRICT;


--
-- Name: car FK_c8d34198d86de9e96aae03b8990; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT "FK_c8d34198d86de9e96aae03b8990" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: purchase_receipt FK_c92afda2aff490f63e02ea303bb; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_c92afda2aff490f63e02ea303bb" FOREIGN KEY (received_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: stock_movement FK_cd07883671bb2828c28130d261b; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_cd07883671bb2828c28130d261b" FOREIGN KEY (from_location_id) REFERENCES public.stock_location(location_id) ON DELETE RESTRICT;


--
-- Name: order FK_cd7812c96209c5bdd48a6b858b0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_cd7812c96209c5bdd48a6b858b0" FOREIGN KEY (customer_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: audit FK_d214d146099cc53049201a1efd5; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit
    ADD CONSTRAINT "FK_d214d146099cc53049201a1efd5" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE SET NULL;


--
-- Name: maintenance_task_attachment FK_d48d7736a7efef5c2a5c0b4b23d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task_attachment
    ADD CONSTRAINT "FK_d48d7736a7efef5c2a5c0b4b23d" FOREIGN KEY (task_id) REFERENCES public.maintenance_task(task_id) ON DELETE CASCADE;


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
-- Name: purchase_receipt FK_d8373964f8a5c4fa998a23fc0d2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_d8373964f8a5c4fa998a23fc0d2" FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_order(purchase_order_id) ON DELETE RESTRICT;


--
-- Name: stock_location FK_d88f225ec362c0b11c179a4e034; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT "FK_d88f225ec362c0b11c179a4e034" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE RESTRICT;


--
-- Name: order FK_df56039592a4bbbd3fa4a19f141; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_df56039592a4bbbd3fa4a19f141" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: document_sequence FK_document_sequence_distributor; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_sequence
    ADD CONSTRAINT "FK_document_sequence_distributor" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: stock_movement FK_e29e01a939f7c0a5ade184a3bf9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_e29e01a939f7c0a5ade184a3bf9" FOREIGN KEY (reversed_movement_id) REFERENCES public.stock_movement(movement_id) ON DELETE RESTRICT;


--
-- Name: vehicle_assignment FK_e553214db24f1d24bf12185dbb6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "FK_e553214db24f1d24bf12185dbb6" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE CASCADE;


--
-- Name: purchase_receipt FK_e5c3319a7128d4f1758e0f97d97; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_e5c3319a7128d4f1758e0f97d97" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: stock_threshold FK_ea56f87659c1c21bc76e2b31cd4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_threshold
    ADD CONSTRAINT "FK_ea56f87659c1c21bc76e2b31cd4" FOREIGN KEY (warehouse_id) REFERENCES public.warehouse(warehouse_id) ON DELETE RESTRICT;


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
-- Name: employee FK_f61258e58ed35475ce1dba03797; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT "FK_f61258e58ed35475ce1dba03797" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: job_position FK_f63c2b78c253c8c92398d88fd59; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_position
    ADD CONSTRAINT "FK_f63c2b78c253c8c92398d88fd59" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: stock_balance FK_f8b2b588f7e7c8868a2756192d4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_balance
    ADD CONSTRAINT "FK_f8b2b588f7e7c8868a2756192d4" FOREIGN KEY (location_id) REFERENCES public.stock_location(location_id) ON DELETE RESTRICT;


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
-- Name: stock_reconciliation_alert FK_stock_reconciliation_alert_distributor; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_reconciliation_alert
    ADD CONSTRAINT "FK_stock_reconciliation_alert_distributor" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

